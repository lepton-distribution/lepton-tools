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

from lepton.checks import check_seed_options
from lepton.errors import EXIT_OK, EXIT_TOOL, LeptonError
from lepton.rootstock import PROJECT_SUBPATH, STEM_DIR, Rootstock, SOURCE_ROOT, project_key
from lepton.scion_runner import run
from lepton.seed import _info, _remind_commit, _warn, finish, graft_project, load_graine, project_stem
from lepton.validation import SCHEMA_FILES, SCION_MANIFEST, SEED_MANIFEST, schemas_dir

PRESETS_FILE = "CMakeUserPresets.json"
KERNEL_PRESETS = "CMakePresets.json"
BASE_PRESET = "cross"              # preset caché du CMakePresets.json du noyau (chaîne croisée)
HOST_PRESET = "host"               # preset du noyau qui construit mklepton (LEPTON_MKLEPTON de cross)
NOTE = "généré par lepton generate, ne pas éditer"
ACTIVE_DIR = ".active"             # build/.active : compile_commands.json du preset actif (clangd)
OPTION_PREFIX = "LEPTON_OPTION_"   # + <greffon>_<NOM> : valeur d'option de la graine (CFG-4)
COMPILE_COMMANDS = "compile_commands.json"
PROBE_SERIAL_SETTING = "lepton.probeSerial"   # réglage de l'espace : série de sonde conservée (O8)
MKCONF_PATTERN = "**/mkconf_*.xml"            # XML mklepton du noyau (xml.fileAssociations, CFG-7)
# Sortie de `lepton check` (« <fichier>: [<ligne xmllint>: ]<emplacement et message> ») → panneau Problems,
# en erreur (CFG-7 : le service JSON intégré signale les fautes de schéma en avertissement seulement)
CHECK_MATCHER = {"owner": "lepton", "source": "lepton check", "severity": "error",
                 "pattern": {"regexp": r"^(?!lepton: )(\S[^:]*): (?:(\d+): )?(.*)$",
                             "file": 1, "line": 2, "message": 3}}
# API fichier CMake : requête propre à lepton (seed tree), relative au répertoire de construction
API_QUERY = Path(".cmake/api/v1/query/client-lepton/query.json")
API_REQUESTS = {"requests": [{"kind": "codemodel", "version": 2}]}
_PROBE_SERIAL = re.compile(r"""^[^\s"'\\]+$""")

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


def _gdb_has_python(gdb: str) -> bool:
    try:
        out = subprocess.run([gdb, "-nx", "-batch", "-ex", "python print('ok')"],
                             capture_output=True, text=True, timeout=30).stdout
    except (OSError, subprocess.SubprocessError):
        return False
    return out.strip() == "ok"


def find_gdb() -> str:
    """gdb de débogage (O9) : parmi les `arm-none-eabi-gdb` puis `gdb-multiarch` du PATH, le premier
    construit avec Python (lepton-stacks de debug/gdbinit-lepton ; le gdb de l'Arm GNU Toolchain n'en a
    pas) ; à défaut, le premier trouvé (avertissement) ; aucun : code 2."""
    candidates: list[str] = []
    seen = set()
    for name in ("arm-none-eabi-gdb", "gdb-multiarch"):
        for d in os.environ.get("PATH", "").split(os.pathsep):
            path = shutil.which(name, path=d) if d else None
            if path is not None and os.path.realpath(path) not in seen:
                seen.add(os.path.realpath(path))
                candidates.append(path)
    if not candidates:
        return require_tool("arm-none-eabi-gdb", "débogage", "gdb-multiarch")   # code 2 (EXIT_TOOL)
    for gdb in candidates:
        if _gdb_has_python(gdb):
            return gdb
    _warn(f"aucun gdb avec Python dans le PATH ; {candidates[0]} retenu (lepton-stacks indisponible ; "
          "MacPorts arm-none-eabi-gdb +python313, Debian gdb-multiarch)")
    return candidates[0]


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
def check_configuration(c: dict, bsp_name: str, bsp: dict, action: str) -> None:
    """Exécution de la configuration `c` permise par le BSP (qemu : machine ; carte : openocd)."""
    if c["execution"] == "qemu" and not bsp.get("qemu", {}).get("machine"):
        raise LeptonError(f"configuration {c['nom']} : exécution qemu, le BSP {bsp_name} ne déclare pas qemu", action)
    if c["execution"] == "carte" and not bsp.get("openocd"):
        raise LeptonError(f"configuration {c['nom']} : exécution carte, le BSP {bsp_name} ne déclare pas openocd", action)


def preset_name(project: str, configuration: dict) -> str:
    """Preset CMake d'une configuration de la graine : <projet>-<nom>."""
    return f"{project}-{configuration['nom']}"


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
            check_configuration(c, bsp.name, self.bsp, f"corriger « execution » dans {rs.seed_manifest_path()}")
        anomalies = check_seed_options(self.graine, by_name, str(rs.seed_manifest_path()))
        if anomalies:
            raise LeptonError("valeurs d'options de la graine refusées (CFG-4) :\n"
                              + "\n".join(str(a) for a in anomalies), "corriger « options », puis lepton check")
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
        return preset_name(self.project, configuration)

    def bsp_file(self, rel: str) -> Path:
        """Fichier déclaré par le BSP, par le chemin du trunk (chemin canonique, PA-1)."""
        return self.rs.trunk / SOURCE_ROOT / self.bsp["destination"] / rel

    def build_dir(self, configuration: dict) -> Path:
        return self.rs.build / self.preset(configuration)


# --------------------------------------------------------------------------
# CMakeUserPresets.json (CFG-6, BLD-5)
# --------------------------------------------------------------------------
def option_cache(graine: dict) -> dict[str, str]:
    """Valeurs d'options de la graine (CFG-4, N5) : LEPTON_OPTION_<greffon>_<NOM>, lue par le lecteur
    CMake du noyau à la place du défaut ; booléen : 1 ou 0."""
    cache = {}
    for scion_name, values in graine.get("options", {}).items():
        for name, value in values.items():
            if isinstance(value, bool):
                value = 1 if value else 0
            cache[f"{OPTION_PREFIX}{scion_name}_{name}"] = str(value)
    return cache


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
        cache.update(option_cache(ctx.graine))
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


def schema_settings(ctx: Context) -> dict:
    """CFG-7 (N4) : manifestes JSON et XML mklepton associés aux schémas du paquet lepton (chemin
    absolu résolu à la génération) ; complétion à la saisie (JSON intégré, lemminx), validation XML
    par lemminx. Validation JSON intégrée coupée (ENV-12 lot 4) : elle ne signale qu'en avertissement,
    l'extension Lepton signale en erreur (`lepton check --stdin`)."""
    schemas = schemas_dir()
    patterns = [MKCONF_PATTERN]
    seed_xml = f"**/{ctx.graine['mklepton_xml']}"
    if not Path(ctx.graine["mklepton_xml"]).match(MKCONF_PATTERN.removeprefix("**/")):
        patterns.append(seed_xml)
    return {
        "json.schemas": [{"fileMatch": [f"**/{name}"], "url": (schemas / SCHEMA_FILES[kind]).as_uri()}
                         for name, kind in ((SCION_MANIFEST, "scion"), (SEED_MANIFEST, "seed"))],
        "xml.fileAssociations": [{"pattern": p, "systemId": str(schemas / SCHEMA_FILES["mklepton"])}
                                 for p in patterns],
        "json.validate.enable": False,
    }


def workspace_settings(ctx: Context, tools: dict, probe_serial: str | None = None) -> dict:
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
        "cmake.options.statusBarVisibility": "visible",   # sélecteur de preset (IDE-5, O11)
        "cmake.copyCompileCommands": str(active / COMPILE_COMMANDS),
        "clangd.arguments": [f"--compile-commands-dir={active}", "--background-index",
                             f"--query-driver={tools['gcc']}"],
        "cortex-debug.armToolchainPath": str(Path(tools["gcc"]).parent),   # objdump, nm (gdb : gdbPath)
        "cortex-debug.gdbPath": tools["gdb"],
    }
    if tools.get("clangd"):
        settings["clangd.path"] = tools["clangd"]
    if tools.get("openocd"):
        settings["cortex-debug.openocdPath"] = tools["openocd"]
    if probe_serial:
        settings[PROBE_SERIAL_SETTING] = probe_serial
    settings.update(schema_settings(ctx))
    return settings


def _elf(ctx: Context, c: dict) -> str:
    return str(ctx.build_dir(c) / "lepton.elf")


def launch_configurations(ctx: Context, tools: dict, probe_serial: str | None = None) -> list[dict]:
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
            board = {"name": f"Déboguer {preset} (carte, OpenOCD)", **common,
                     "servertype": "openocd", "serverpath": tools["openocd"],
                     "configFiles": [str(ctx.bsp_file(f)) for f in ctx.bsp["openocd"]]}
            if probe_serial:   # O8 : Cortex-Debug n'applique pas serialNumber à OpenOCD
                board["openOCDLaunchCommands"] = [f"adapter serial {probe_serial}"]
            configs.append(board)
    return configs


def _task(label: str, command: str, args: list[str], cwd: Path, **extra) -> dict:
    task = {"label": label, "type": "process", "command": command, "args": args,
            "options": {"cwd": str(cwd)}, "problemMatcher": []}
    task.update(extra)
    return task


def tasks(ctx: Context, tools: dict, probe_serial: str | None = None) -> list[dict]:
    trunk = ctx.rs.trunk
    cmake = tools["cmake"]
    mk = "lepton : mklepton (preset host)"
    result = [
        _task("lepton : regreffer", tools["lepton"], ["graft", "-C", str(ctx.rs.path)], ctx.rs.path),
        _task("lepton : vérifier", tools["lepton"], ["check", "-C", str(ctx.rs.path)], ctx.rs.path,
              problemMatcher={**CHECK_MATCHER, "fileLocation": ["autoDetect", str(ctx.rs.path)]}),
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
            if probe_serial:
                cfgs += ["-c", f"adapter serial {probe_serial}"]
            result.append(_task(f"lepton : flasher {preset}", tools["openocd"],
                                [*cfgs, "-c", f"program {_elf(ctx, c)} verify reset exit"], trunk,
                                dependsOn=[build]))
    return result


def render_workspace(ctx: Context, tools: dict, probe_serial: str | None = None) -> str:
    data = {"folders": workspace_folders(ctx),
            "settings": workspace_settings(ctx, tools, probe_serial),
            "launch": {"version": "0.2.0", "configurations": launch_configurations(ctx, tools, probe_serial)},
            "tasks": {"version": "2.0.0", "tasks": tasks(ctx, tools, probe_serial)},
            "extensions": {"recommendations": ["llvm-vs-code-extensions.vscode-clangd",
                                               "ms-vscode.cmake-tools", "marus25.cortex-debug"]}}
    return f"// {NOTE}\n" + json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def host_tools(ctx: Context, clangd: str | None) -> dict:
    executions = {c["execution"] for c in ctx.configurations}
    tools = {"cmake": require_tool("cmake", "presets"), "ctest": require_tool("ctest", "tests"),
             "gcc": require_tool("arm-none-eabi-gcc", "clangd --query-driver"),
             "gdb": find_gdb(),
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


def probe_serial(ctx: Context, workspace: Path, option: str | None) -> str | None:
    """O8 : série de sonde de l'option ; sans option, celle de l'espace existant ; "" la retire."""
    if option is not None:
        if option and not _PROBE_SERIAL.match(option):
            raise LeptonError(f"--probe-serial « {option} » : ni espace, ni guillemet, ni barre oblique inverse",
                              "donner le numéro de série de la sonde tel qu'OpenOCD l'affiche")
        return option or None
    try:
        text = workspace.read_text(encoding="utf-8")
        previous = json.loads(text.split("\n", 1)[1] if text.startswith("//") else text)
        return previous.get("settings", {}).get(PROBE_SERIAL_SETTING) or None
    except FileNotFoundError:
        return None
    except (OSError, ValueError, IndexError, AttributeError) as e:
        _warn(f"{workspace} illisible ({e}) : série de sonde précédente ignorée")
        return None


def prime_active(ctx: Context) -> None:
    """O10 : clangd démarre avec l'espace et ne relit pas une base apparue ensuite pour les fichiers
    ouverts ; build/.active est amorcé avec la base du premier preset de la graine déjà configuré
    (CMake Tools la remplace ensuite, cmake.copyCompileCommands)."""
    active = ctx.rs.build / ACTIVE_DIR / COMPILE_COMMANDS
    if active.exists():
        return
    for c in ctx.configurations:
        source = ctx.build_dir(c) / COMPILE_COMMANDS
        if source.is_file():
            active.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, active)
            _info(f"amorcé    {active} (preset {ctx.preset(c)})")
            return
    first = ctx.preset(ctx.configurations[0])
    _warn(f"{active} absent, aucun preset configuré : clangd sans base à l'ouverture de l'espace ; "
          f"configurer {first} (tâche « lepton : configurer {first} » ou CMake Tools), "
          "puis « clangd: Restart language server », ou relancer lepton generate avant l'ouverture")


def write_api_queries(ctx: Context) -> None:
    """Requête codemodel-v2 de l'API fichier CMake dans chaque répertoire de construction de la graine :
    la réponse lue par `lepton seed tree` (vue IDE-1) existe aussi après une configuration en ligne de
    commande, sans CMake Tools (ENV-12 lot 5)."""
    for c in ctx.configurations:
        _write_if_changed(ctx.build_dir(c) / API_QUERY, json.dumps(API_REQUESTS, indent=2) + "\n")


def generate(args) -> int:
    rs = Rootstock.discover(args.rootstock)
    ctx = Context(rs)
    tools = host_tools(ctx, args.clangd)

    presets = project_stem(ctx.seed_root) / PRESETS_FILE
    seed_changed = _write_if_changed(presets, json.dumps(render_presets(ctx), ensure_ascii=False, indent=2) + "\n")
    seed_changed |= graft_project(rs, ctx.seed_root, ctx.project)
    workspace = rs.path / f"{ctx.project}.code-workspace"
    serial = probe_serial(ctx, workspace, args.probe_serial)
    ws_changed = _write_if_changed(workspace, render_workspace(ctx, tools, serial))
    prime_active(ctx)
    write_api_queries(ctx)
    finish(rs, no_cmake=True)

    _info(f"{'écrit    ' if seed_changed else 'inchangé '} {presets} (greffé : {rs.trunk / PRESETS_FILE})")
    _info(f"{'écrit    ' if ws_changed else 'inchangé '} {workspace}")
    _info(f"presets : {', '.join(ctx.preset(c) for c in ctx.configurations)} (cmake --list-presets dans {rs.trunk})")
    if any(c["execution"] == "carte" for c in ctx.configurations):
        if serial:
            _info(f"sonde : adapter serial {serial} (lancement et tâche « flasher »)")
        else:
            _warn("configuration carte sans --probe-serial : OpenOCD prend la première sonde, "
                  "une seule carte branchée à la fois")
    if seed_changed:
        _remind_commit(ctx.seed_root)
    return EXIT_OK
