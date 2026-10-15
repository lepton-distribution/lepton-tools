"""lepton generate : presets CMake et espace de travail VSCodium (ENV-9, rapports/env-9-generation.md).

Sources : manifeste de graine et manifestes des greffons greffés (CFG-1 : jamais le XML mklepton,
dont seul le chemin est recopié). Emplacements (décisions ENV-9 du 2026-10-14) :

- `CMakeUserPresets.json` dans le dépôt de la graine, sous `project/scion/`, greffé à la racine du
  trunk par le greffon local `lepton@project-<projet>` ; il hérite des presets cachés du noyau ;
- `<ROOTSTOCK>/<projet>.code-workspace`, non versionné, avec `launch` et `tasks` intégrés.

Écriture seulement si le contenu change ; aucun horodatage : deux appels successifs ne changent rien.
"""

import json
import os
import re
import shutil
import subprocess
from pathlib import Path

from lepton.errors import EXIT_OK, EXIT_TOOL, LeptonError
from lepton.rootstock import PROJECT_SUBPATH, STEM_DIR, Rootstock, SOURCE_ROOT, project_key
from lepton.scion_runner import run, scion
from lepton.seed import LOCAL_VERSION, _info, _remind_commit, _warn, finish, load_graine, scion_on_trunk

PRESETS_FILE = "CMakeUserPresets.json"
KERNEL_PRESETS = "CMakePresets.json"
BASE_PRESET = "cross"              # preset caché du CMakePresets.json du noyau (chaîne croisée)
HOST_PRESET = "host"               # preset du noyau qui construit mklepton (LEPTON_MKLEPTON de cross)
NOTE = "généré par lepton generate, ne pas éditer"
ACTIVE_DIR = ".active"             # build/.active : compile_commands.json du preset actif (clangd)

# Cœur (enum du schéma) → famille d'ISA du noyau (cmake/isa/) et cœur QEMU (-cpu)
ISA_OF_CORE = {"cortex-m0plus": "armv6m", "cortex-m3": "armv7m", "cortex-m4f": "armv7m", "cortex-m7": "armv7m"}
QEMU_CPU_OF_CORE = {"cortex-m0plus": "cortex-m0", "cortex-m3": "cortex-m3", "cortex-m4f": "cortex-m4",
                    "cortex-m7": "cortex-m7"}

_CLANGD_NAME = re.compile(r"^clangd(?:-mp)?(?:-(\d+))?$")
_CLANGD_VERSION = re.compile(r"clangd version (\d+)\.")


# --------------------------------------------------------------------------
# outils de l'hôte (NF-3 : résolus par le PATH, aucun préfixe codé en dur)
# --------------------------------------------------------------------------
def require_tool(name: str, why: str, *fallbacks: str) -> str:
    """Premier de `name`, `fallbacks` trouvé dans le PATH ; sinon code 2 (EXIT_TOOL)."""
    for candidate in (name, *fallbacks):
        path = shutil.which(candidate)
        if path is not None:
            return path
    names = " ou ".join((name, *fallbacks))
    raise LeptonError(f"{name} absent du PATH ({why})", f"installer {names} et vérifier le PATH", EXIT_TOOL)


def find_clangd(explicit: str | None) -> str | None:
    """clangd LLVM (PA-1) : `--clangd`, sinon le plus récent des `clangd`, `clangd-N`, `clangd-mp-N` du
    PATH dont la version n'est pas celle d'Apple ; à défaut, `clangd` tel quel (avertissement)."""
    if explicit:
        path = shutil.which(explicit) or (explicit if Path(explicit).is_file() else None)
        if path is None:
            raise LeptonError(f"--clangd « {explicit} » introuvable", "donner le chemin d'un exécutable clangd")
        return path
    best: tuple[int, str] | None = None
    seen = set()
    for d in os.environ.get("PATH", "").split(os.pathsep):
        if not d or not Path(d).is_dir():
            continue
        for p in sorted(Path(d).iterdir()):
            if not _CLANGD_NAME.match(p.name) or p.name in seen or not os.access(p, os.X_OK):
                continue
            seen.add(p.name)
            try:
                out = subprocess.run([str(p), "--version"], capture_output=True, text=True, timeout=10).stdout
            except (OSError, subprocess.SubprocessError):
                continue
            m = _CLANGD_VERSION.search(out)
            if m is None or "Apple" in out:
                continue
            if best is None or int(m.group(1)) > best[0]:
                best = (int(m.group(1)), str(p))
    if best is not None:
        return best[1]
    fallback = shutil.which("clangd")
    _warn("aucun clangd LLVM trouvé dans le PATH" + (f" ; {fallback} retenu" if fallback else " ; clangd.path omis")
          + " (PA-1 : clangd LLVM, ex. MacPorts clang-21, Debian clangd)")
    return fallback


# --------------------------------------------------------------------------
# contexte : graine, BSP, presets du noyau
# --------------------------------------------------------------------------
class Context:
    def __init__(self, rs: Rootstock):
        self.rs = rs
        self.seed_root = rs.seed_root()
        self.graine = load_graine(rs.seed_manifest_path())
        self.project = self.graine["projet"]["nom"]
        by_name = {m.name: m for m in rs.manifests().values()}
        bsp = by_name.get(self.graine["bsp"])
        if bsp is None:
            raise LeptonError(f"BSP « {self.graine['bsp']} » de la graine non greffé", "lepton seed status")
        self.bsp = bsp.data
        self.core = self.bsp.get("coeur")
        if self.core not in ISA_OF_CORE:
            raise LeptonError(f"BSP {bsp.name} : cœur « {self.core} » inconnu de lepton generate",
                              f"cœurs pris en charge : {', '.join(ISA_OF_CORE)}")
        self.configurations = self.graine["configurations"]
        for c in self.configurations:
            if c["execution"] == "qemu" and not self.bsp.get("qemu", {}).get("machine"):
                raise LeptonError(f"configuration {c['nom']} : exécution qemu, le BSP {bsp.name} ne déclare pas qemu",
                                  f"corriger « execution » dans {rs.seed_manifest_path()}")
            if c["execution"] == "carte" and not self.bsp.get("openocd"):
                raise LeptonError(f"configuration {c['nom']} : exécution carte, le BSP {bsp.name} ne déclare pas openocd",
                                  f"corriger « execution » dans {rs.seed_manifest_path()}")
        self._check_kernel_presets()

    def _check_kernel_presets(self) -> None:
        path = self.rs.trunk / KERNEL_PRESETS
        try:
            names = {p.get("name") for p in json.loads(path.read_text(encoding="utf-8")).get("configurePresets", [])}
        except (OSError, ValueError) as e:
            raise LeptonError(f"{path} illisible ({e})", "le greffon noyau doit fournir CMakePresets.json") from e
        missing = {BASE_PRESET, HOST_PRESET} - names
        if missing:
            raise LeptonError(f"{path} : preset(s) {', '.join(sorted(missing))} absent(s)",
                              "greffon noyau d'ENV-5 ou plus récent")

    def preset(self, configuration: dict) -> str:
        return f"{self.project}-{configuration['nom']}"

    def bsp_file(self, rel: str) -> Path:
        """Fichier déclaré par le BSP, par le chemin du trunk (chemin canonique, PA-1)."""
        return self.rs.trunk / SOURCE_ROOT / self.bsp["destination"] / rel

    def build_dir(self, configuration: dict) -> Path:
        return self.rs.build / self.preset(configuration)


# --------------------------------------------------------------------------
# CMakeUserPresets.json (CFG-6, BLD-5)
# --------------------------------------------------------------------------
def render_presets(ctx: Context) -> dict:
    configure, build, test = [], [], []
    for c in ctx.configurations:
        name = ctx.preset(c)
        cache = {"CMAKE_BUILD_TYPE": c["construction"],
                 "LEPTON_ISA": ISA_OF_CORE[ctx.core],
                 "LEPTON_CPU": ctx.core,
                 "LEPTON_BOARD": ctx.graine["bsp"],
                 "LEPTON_KAL_BACKEND": ctx.graine["backend"],
                 "LEPTON_MKCONF": ctx.graine["mklepton_xml"]}
        if ctx.bsp.get("abi_flottante"):
            cache["LEPTON_FLOAT_ABI"] = ctx.bsp["abi_flottante"]
        where = f"QEMU {ctx.bsp['qemu']['machine']}" if c["execution"] == "qemu" else "carte"
        configure.append({"name": name,
                          "displayName": f"{ctx.project} — {c['nom']} ({ctx.graine['bsp']}, {where}, "
                                         f"{ctx.graine['backend']}, {c['construction']})",
                          "inherits": BASE_PRESET,
                          "cacheVariables": cache})
        build.append({"name": name, "configurePreset": name})
        test.append({"name": name, "configurePreset": name, "output": {"outputOnFailure": True}})
    return {"version": 6,
            "cmakeMinimumRequired": {"major": 3, "minor": 24, "patch": 0},
            "vendor": {"lepton": {"note": NOTE, "seed": ctx.project}},
            "configurePresets": configure, "buildPresets": build, "testPresets": test}


# --------------------------------------------------------------------------
# <projet>.code-workspace : dossiers, réglages, launch, tasks
# --------------------------------------------------------------------------
def _git_toplevel(path: Path) -> Path | None:
    res = run(["git", "-C", str(path), "rev-parse", "--show-toplevel"], check=False)
    return Path(res.stdout.strip()).resolve() if res.returncode == 0 else None


def _folder_path(ctx: Context, path: Path) -> str:
    try:
        return str(path.relative_to(ctx.rs.path))
    except ValueError:
        return str(path)


def workspace_folders(ctx: Context) -> list[dict]:
    """Trunk d'abord (seul chemin d'ouverture des fichiers, PA-1), puis un dossier par dépôt git (IDE-2)."""
    folders = [{"name": "trunk", "path": _folder_path(ctx, ctx.rs.trunk)}]
    names = {key: m.name for key, m in ctx.rs.manifests().items()}
    seen = set()
    repos = [(f"graine {ctx.project}", ctx.seed_root)]
    repos += [(names.get(e.key, e.name), ctx.rs.clone(e)) for e in ctx.rs.grafted() if e.key != project_key(ctx.project)]
    for label, path in repos:
        top = _git_toplevel(path) if path.is_dir() else None
        if top is None or top in seen:
            continue
        seen.add(top)
        folders.append({"name": f"git · {label}", "path": _folder_path(ctx, top)})
    return folders


def workspace_settings(ctx: Context, tools: dict) -> dict:
    active = ctx.rs.build / ACTIVE_DIR
    settings = {
        # Dossiers « git · … » : fichiers greffés masqués (ouverts par le trunk seul, IDE-4) ; restent
        # visibles les fichiers non greffés et `scion/.scion/` de la graine. Le trunk n'a ni `scion/`
        # ni `project/` à sa racine.
        "files.exclude": {"**/.DS_Store": True, "**/._*": True, f"{STEM_DIR}/[!.]*": True,
                          f"{PROJECT_SUBPATH}/{STEM_DIR}": True},
        "cmake.useCMakePresets": "always",
        "cmake.configureOnOpen": False,
        "cmake.ignoreCMakeListsMissing": True,
        "cmake.copyCompileCommands": str(active / "compile_commands.json"),
        "clangd.arguments": [f"--compile-commands-dir={active}", "--background-index",
                             f"--query-driver={tools['gcc']}"],
        "cortex-debug.armToolchainPath": str(Path(tools["gdb"]).parent),
        "cortex-debug.gdbPath": tools["gdb"],
    }
    if tools.get("clangd"):
        settings["clangd.path"] = tools["clangd"]
    if tools.get("openocd"):
        settings["cortex-debug.openocdPath"] = tools["openocd"]
    return settings


def _elf(ctx: Context, c: dict) -> str:
    return str(ctx.build_dir(c) / "lepton.elf")


def launch_configurations(ctx: Context, tools: dict) -> list[dict]:
    configs = []
    for c in ctx.configurations:
        preset = ctx.preset(c)
        common = {"type": "cortex-debug", "request": "launch", "cwd": str(ctx.rs.trunk),
                  "executable": _elf(ctx, c), "gdbPath": tools["gdb"], "runToEntryPoint": "main",
                  "preLaunchTask": f"lepton : construire {preset}"}
        if ctx.bsp.get("svd"):
            common["svdFile"] = str(ctx.bsp_file(ctx.bsp["svd"]))
        if c["execution"] == "qemu":
            configs.append({"name": f"Déboguer {preset} (QEMU {ctx.bsp['qemu']['machine']})", **common,
                            "servertype": "qemu", "serverpath": tools["qemu"],
                            "cpu": QEMU_CPU_OF_CORE[ctx.core], "machine": ctx.bsp["qemu"]["machine"]})
        else:
            configs.append({"name": f"Déboguer {preset} (carte, OpenOCD)", **common,
                            "servertype": "openocd", "serverpath": tools["openocd"],
                            "configFiles": [str(ctx.bsp_file(f)) for f in ctx.bsp["openocd"]]})
    return configs


def _task(label: str, command: str, args: list[str], cwd: Path, **extra) -> dict:
    task = {"label": label, "type": "process", "command": command, "args": args,
            "options": {"cwd": str(cwd)}, "problemMatcher": []}
    task.update(extra)
    return task


def tasks(ctx: Context, tools: dict) -> list[dict]:
    trunk = ctx.rs.trunk
    cmake = tools["cmake"]
    mk = "lepton : mklepton (preset host)"
    result = [
        _task("lepton : regreffer", tools["lepton"], ["graft", "-C", str(ctx.rs.path)], ctx.rs.path),
        _task("lepton : configurer host", cmake, ["--preset", HOST_PRESET], trunk),
        _task(mk, cmake, ["--build", "--preset", HOST_PRESET, "--target", "mklepton"], trunk,
              dependsOn=["lepton : configurer host"], dependsOrder="sequence", problemMatcher=["$gcc"]),
    ]
    env = {"env": {"PYTHONDONTWRITEBYTECODE": "1"}}   # tests servis par le trunk : aucun __pycache__
    for c in ctx.configurations:
        preset = ctx.preset(c)
        configure, build = f"lepton : configurer {preset}", f"lepton : construire {preset}"
        result.append(_task(configure, cmake, ["--preset", preset], trunk, dependsOn=[mk]))
        result.append(_task(build, cmake, ["--build", "--preset", preset], trunk,
                            dependsOn=[configure], group="build", problemMatcher=["$gcc"]))
        if c["execution"] == "qemu":
            result.append(_task(f"lepton : QEMU {preset} (console série)", tools["qemu"],
                                ["-M", ctx.bsp["qemu"]["machine"], "-kernel", _elf(ctx, c), "-nographic",
                                 "-monitor", "none", "-serial", "stdio"], trunk,
                                dependsOn=[build], isBackground=False,
                                presentation={"panel": "dedicated", "focus": True}))
            for label, test_label in (("test de fumée", "smoke"), ("banc KAL", "kal")):
                result.append(_task(f"lepton : {label} {preset}", tools["ctest"],
                                    ["--preset", preset, "-L", test_label, "--output-on-failure"], trunk,
                                    dependsOn=[build], group="test", options={"cwd": str(trunk), **env}))
        else:
            cfgs = [a for f in ctx.bsp["openocd"] for a in ("-f", str(ctx.bsp_file(f)))]
            result.append(_task(f"lepton : flasher {preset}", tools["openocd"],
                                [*cfgs, "-c", f"program {_elf(ctx, c)} verify reset exit"], trunk,
                                dependsOn=[build]))
    return result


def render_workspace(ctx: Context, tools: dict) -> str:
    data = {"folders": workspace_folders(ctx),
            "settings": workspace_settings(ctx, tools),
            "launch": {"version": "0.2.0", "configurations": launch_configurations(ctx, tools)},
            "tasks": {"version": "2.0.0", "tasks": tasks(ctx, tools)},
            "extensions": {"recommendations": ["llvm-vs-code-extensions.vscode-clangd",
                                               "ms-vscode.cmake-tools", "marus25.cortex-debug"]}}
    return f"// {NOTE}\n" + json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def host_tools(ctx: Context, clangd: str | None) -> dict:
    executions = {c["execution"] for c in ctx.configurations}
    tools = {"cmake": require_tool("cmake", "presets"), "ctest": require_tool("ctest", "tests"),
             "gcc": require_tool("arm-none-eabi-gcc", "clangd --query-driver"),
             "gdb": require_tool("arm-none-eabi-gdb", "débogage", "gdb-multiarch"),   # Debian : gdb-multiarch
             "lepton": shutil.which("lepton") or "lepton",
             "clangd": find_clangd(clangd)}
    if "qemu" in executions:
        tools["qemu"] = require_tool("qemu-system-arm", "configuration qemu")
    if "carte" in executions:
        tools["openocd"] = require_tool("openocd", "configuration carte")
    return tools


# --------------------------------------------------------------------------
# commande
# --------------------------------------------------------------------------
def _write_if_changed(path: Path, text: str) -> bool:
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return True


def _graft_project(ctx: Context, presets: Path) -> bool:
    """Greffon local du projet (presets) : déclaré, inscrit puis greffé tant que le lien du trunk manque."""
    rs, key = ctx.rs, project_key(ctx.project)
    link = rs.trunk / PRESETS_FILE
    changed = False
    if key not in {s.key for s in rs.sources()}:
        try:
            location = str(ctx.seed_root.relative_to(rs.path))
        except ValueError:
            location = str(ctx.seed_root)
        scion("seed-scion-add", "--seed", str(ctx.seed_root), key, LOCAL_VERSION, location, PROJECT_SUBPATH,
              cwd=rs.path)
        changed = True
    if key not in {e.key for e in rs.grafted()}:
        scion("seed-clone", "--seed", str(ctx.seed_root), cwd=rs.path)   # inscrit la clé dans la liste greffée
        changed = True
    if not (link.is_symlink() and link.resolve() == presets.resolve()):
        scion_on_trunk(rs, "graft", "--scion", key)
        changed = True
    return changed


def generate(args) -> int:
    rs = Rootstock.discover(args.rootstock)
    ctx = Context(rs)
    tools = host_tools(ctx, args.clangd)

    presets = ctx.seed_root / PROJECT_SUBPATH / STEM_DIR / PRESETS_FILE
    seed_changed = _write_if_changed(presets, json.dumps(render_presets(ctx), ensure_ascii=False, indent=2) + "\n")
    seed_changed |= _graft_project(ctx, presets)
    workspace = rs.path / f"{ctx.project}.code-workspace"
    ws_changed = _write_if_changed(workspace, render_workspace(ctx, tools))
    finish(rs, no_cmake=True)

    _info(f"{'écrit    ' if seed_changed else 'inchangé '} {presets} (greffé : {rs.trunk / PRESETS_FILE})")
    _info(f"{'écrit    ' if ws_changed else 'inchangé '} {workspace}")
    _info(f"presets : {', '.join(ctx.preset(c) for c in ctx.configurations)} (cmake --list-presets dans {rs.trunk})")
    if seed_changed:
        _remind_commit(ctx.seed_root)
    return EXIT_OK
