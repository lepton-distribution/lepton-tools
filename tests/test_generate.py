"""ENV-9 : lepton generate — presets CMake (graine), espace de travail VSCodium (rootstock).

Exigences : CFG-1 (aucune lecture du XML mklepton), CFG-6 (un preset par configuration), BLD-5
(mêmes presets partout), IDE-2 (un dossier par dépôt git), IDE-3/IDE-4 (trunk seul chemin
d'ouverture, clangd), DBG-1 à DBG-3 (launch, tasks), NF-3 (outils résolus par le PATH).
"""

import json
import os
import re
import subprocess
from pathlib import Path

import pytest

from conftest import MKCONF, PROJECT_XML, assert_trunk_clean, url
from lepton import generate as gen
from lepton.cli import main
from lepton.rootstock import Rootstock, project_key

KERNEL_PRESETS = {
    "version": 6,
    "configurePresets": [
        {"name": "base", "hidden": True, "binaryDir": "${sourceDir}/../build/${presetName}"},
        {"name": "host", "inherits": "base"},
        {"name": "cross", "hidden": True, "inherits": "base"},
    ],
}
# arm-none-eabi-gdb : « ok » = réponse d'un gdb avec Python à python print('ok') (find_gdb, O9)
TOOLS = {"arm-none-eabi-gcc": "", "arm-none-eabi-gdb": "ok", "qemu-system-arm": "", "openocd": "",
         "clangd": "Apple clangd version 17.0.0", "clangd-mp-21": "clangd version 21.1.8",
         "clangd-19": "clangd version 19.1.0"}


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout


@pytest.fixture
def repos(repos):
    """Noyau de conftest complété par un CMakePresets.json (presets cachés base, cross ; host)."""
    (repos["kernel"] / "scion" / "CMakePresets.json").write_text(json.dumps(KERNEL_PRESETS))
    _git(repos["kernel"], "add", "-A")
    _git(repos["kernel"], "commit", "-q", "-m", "presets")
    return repos


@pytest.fixture
def tools(tmp_path, monkeypatch):
    """Outils de l'hôte factices en tête du PATH (NF-3 : résolus par le PATH)."""
    bindir = tmp_path / "tools"
    bindir.mkdir()
    for name, version in TOOLS.items():
        (bindir / name).write_text(f"#!/bin/sh\necho '{version}'\n")
        (bindir / name).chmod(0o755)
    monkeypatch.setenv("PATH", f"{bindir}{os.pathsep}{os.environ['PATH']}")
    return bindir


def _workspace(root: Path, project: str = "demo") -> dict:
    text = (root / f"{project}.code-workspace").read_text(encoding="utf-8")
    first, rest = text.split("\n", 1)
    assert first == f"// {gen.NOTE}"
    return json.loads(rest)


def _seed(root: Path) -> Path:
    return root / "depots" / "lepton-seed" / "demo"


def _graine(root: Path) -> Path:
    return _seed(root) / "scion" / ".scion" / "lepton-graine.json"


def _set_graine(root: Path, **fields) -> None:
    path = _graine(root)
    data = json.loads(path.read_text(encoding="utf-8"))
    data.update(fields)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _snapshot(root: Path) -> dict:
    files = [_seed(root) / "project" / "scion" / gen.PRESETS_FILE, root / "demo.code-workspace",
             _seed(root) / "scion" / ".scion" / ".scion.sources.list", root / "trunk" / ".scion.grafted.list"]
    return {str(p): (p.read_bytes(), p.stat().st_mtime_ns) for p in files}


def test_generate_presets_grafted_in_trunk(project, tools):
    """CFG-6, BLD-5 : un preset par configuration, hérité du noyau, greffé à la racine du trunk."""
    _set_graine(project, configurations=[
        {"nom": "debug-qemu", "construction": "Debug", "execution": "qemu"},
        {"nom": "release-qemu", "construction": "Release", "execution": "qemu"}])
    assert main(["generate", "-C", str(project)]) == 0

    link = project / "trunk" / gen.PRESETS_FILE
    source = _seed(project) / "project" / "scion" / gen.PRESETS_FILE
    assert link.is_symlink() and link.resolve() == source.resolve()
    presets = json.loads(source.read_text(encoding="utf-8"))
    assert presets["vendor"]["lepton"]["note"] == gen.NOTE
    assert [p["name"] for p in presets["configurePresets"]] == ["demo-debug-qemu", "demo-release-qemu"]
    debug = presets["configurePresets"][0]
    assert debug["inherits"] == "cross"
    assert debug["cacheVariables"] == {
        "CMAKE_BUILD_TYPE": "Debug", "LEPTON_ISA": "armv7m", "LEPTON_CPU": "cortex-m4f",
        "LEPTON_BOARD": "board-q", "LEPTON_KAL_BACKEND": "embos", "LEPTON_MKCONF": PROJECT_XML}
    assert presets["configurePresets"][1]["cacheVariables"]["CMAKE_BUILD_TYPE"] == "Release"
    assert [p["configurePreset"] for p in presets["buildPresets"]] == ["demo-debug-qemu", "demo-release-qemu"]
    assert [p["name"] for p in presets["testPresets"]] == ["demo-debug-qemu", "demo-release-qemu"]

    rs = Rootstock(project)
    key = project_key("demo")
    assert any(s.key == key and s.subpath == "project" and s.version == "*" for s in rs.sources())
    assert key in {e.key for e in rs.grafted()}
    assert_trunk_clean(project)


def test_generate_twice_changes_nothing(project, tools, capsys):
    """Critère ENV-9 : deux générations de suite, aucun diff (ni contenu ni réécriture)."""
    assert main(["generate", "-C", str(project)]) == 0
    before = _snapshot(project)
    capsys.readouterr()
    assert main(["generate", "-C", str(project)]) == 0
    assert _snapshot(project) == before
    out = capsys.readouterr().out
    assert out.count("inchangé") == 2 and "graine modifiée" not in out


def test_generate_regrafts_missing_link(project, tools):
    """Lien du trunk retiré (greffe interrompue) : regreffé ; fichiers système du trunk supprimés (Q8)."""
    assert main(["generate", "-C", str(project)]) == 0
    link = project / "trunk" / gen.PRESETS_FILE
    link.unlink()
    (project / "trunk" / ".DS_Store").write_bytes(b"\0")
    assert main(["generate", "-C", str(project)]) == 0
    assert link.is_symlink()
    assert not (project / "trunk" / ".DS_Store").exists()


def test_presets_link_touched_when_changed(project, tools):
    """L6-5 (ENV-12) : presets réécrits → date du lien du trunk avancée (observateur de l'éditeur) ;
    presets inchangés → lien intact."""
    assert main(["generate", "-C", str(project)]) == 0
    link = project / "trunk" / gen.PRESETS_FILE
    os.utime(link, (1_000_000, 1_000_000), follow_symlinks=False)
    assert main(["generate", "-C", str(project)]) == 0
    assert os.lstat(link).st_mtime == 1_000_000
    assert main(["seed", "config", "add", "rel", "--build-type", "MinSizeRel", "--run", "qemu",
                 "-C", str(project)]) == 0
    assert link.is_symlink() and os.lstat(link).st_mtime > 1_000_000
    assert_trunk_clean(project)


def test_generate_never_reads_mklepton_xml(project, tools):
    """CFG-1 : le XML mklepton n'est jamais lu (seul son chemin est recopié)."""
    xml = (project / "trunk" / MKCONF).resolve()
    xml.chmod(0)
    try:
        assert main(["generate", "-C", str(project)]) == 0
    finally:
        xml.chmod(0o644)


def test_workspace_folders_settings_launch_tasks(project, tools):
    """IDE-2 à IDE-4, DBG-1, DBG-2, TST-1 : dossiers, clangd, Cortex-Debug QEMU, tâches."""
    assert main(["generate", "-C", str(project)]) == 0
    ws = _workspace(project)
    folders = ws["folders"]
    assert folders[0] == {"name": "trunk", "path": "trunk"}
    paths = [f["path"] for f in folders[1:]]
    assert paths[0] == "depots/lepton-seed/demo"                 # graine (git), une seule fois
    assert len(paths) == len(set(paths)) == 4                     # graine, noyau, famille, BSP
    assert "depots/generation/building" not in paths              # pas un dépôt git

    s = ws["settings"]
    active = project / "build" / gen.ACTIVE_DIR
    assert s["files.exclude"] == {"**/.DS_Store": True, "**/._*": True,       # fichiers greffés masqués
                                  "scion/[!.]*": True, "project/scion": True}  # dans les clones (P5)
    assert s["cmake.useCMakePresets"] == "always" and s["cmake.configureOnOpen"] is False
    assert s["cmake.options.statusBarVisibility"] == "visible"                 # IDE-5 (O11)
    assert gen.PROBE_SERIAL_SETTING not in s
    assert s["cmake.copyCompileCommands"] == str(active / "compile_commands.json")
    assert s["clangd.path"] == str(tools / "clangd-mp-21")
    assert s["clangd.arguments"] == [f"--compile-commands-dir={active}", "--background-index",
                                     f"--query-driver={tools / 'arm-none-eabi-gcc'}"]

    [launch] = ws["launch"]["configurations"]
    assert launch["type"] == "cortex-debug" and launch["servertype"] == "qemu"
    assert launch["machine"] == "mps2-an386" and launch["cpu"] == "cortex-m4"
    assert launch["serverpath"] == str(tools / "qemu-system-arm")
    assert launch["gdbPath"] == str(tools / "arm-none-eabi-gdb")
    assert launch["executable"] == str(project / "build" / "demo-debug-qemu" / "lepton.elf")
    assert launch["runToEntryPoint"] == "main"
    assert "configFiles" not in launch and "svdFile" not in launch

    tasks = {t["label"]: t for t in ws["tasks"]["tasks"]}
    assert launch["preLaunchTask"] in tasks
    qemu = tasks["lepton : QEMU demo-debug-qemu (console série)"]
    assert qemu["args"][:2] == ["-M", "mps2-an386"] and "stdio" in qemu["args"]
    kal = tasks["lepton : banc KAL demo-debug-qemu"]
    assert kal["args"] == ["--preset", "demo-debug-qemu", "-L", "kal", "--output-on-failure"]
    assert kal["options"]["env"]["PYTHONDONTWRITEBYTECODE"] == "1"
    assert all(t["options"]["cwd"] for t in tasks.values())


def test_board_configuration_uses_bsp_openocd(project, repos, tools):
    """DBG-3 : configuration carte → Cortex-Debug OpenOCD, fichiers du champ openocd par le trunk."""
    assert main(["seed", "add", "board-c", str(repos["bsp2"]), "--type", "bsp", "-C", str(project),
                 "--no-cmake"]) == 0
    _set_graine(project, configurations=[{"nom": "debug-board", "construction": "Debug", "execution": "carte"}])
    assert main(["generate", "-C", str(project)]) == 0
    [launch] = _workspace(project)["launch"]["configurations"]
    cfg = project / "trunk" / "sys/root/src/kernel/dev/bsp/board-c/openocd/board-c.cfg"
    assert launch["servertype"] == "openocd" and launch["configFiles"] == [str(cfg)]
    assert launch["serverpath"] == str(tools / "openocd")
    tasks = {t["label"]: t for t in _workspace(project)["tasks"]["tasks"]}
    flash = tasks["lepton : flasher demo-debug-board"]
    assert flash["args"][:2] == ["-f", str(cfg)] and "verify reset exit" in flash["args"][-1]
    presets = json.loads((project / "trunk" / gen.PRESETS_FILE).read_text(encoding="utf-8"))
    assert presets["configurePresets"][0]["cacheVariables"]["LEPTON_BOARD"] == "board-c"


def _board_project(project, repos) -> None:
    assert main(["seed", "add", "board-c", str(repos["bsp2"]), "--type", "bsp", "-C", str(project),
                 "--no-cmake"]) == 0
    _set_graine(project, configurations=[{"nom": "debug-board", "construction": "Debug", "execution": "carte"}])


def test_probe_serial_kept_in_workspace(project, repos, tools, capsys):
    """DBG-3 (O8) : --probe-serial → adapter serial (lancement, tâche « flasher ») ; conservé sans
    l'option ; "" le retire ; sans série : avertissement (une carte à la fois)."""
    _board_project(project, repos)
    assert main(["generate", "-C", str(project)]) == 0
    assert "sans --probe-serial" in capsys.readouterr().err
    [launch] = _workspace(project)["launch"]["configurations"]
    assert "openOCDLaunchCommands" not in launch

    assert main(["generate", "-C", str(project), "--probe-serial", "066DFF3A"]) == 0
    capsys.readouterr()
    assert main(["generate", "-C", str(project)]) == 0                  # reprise sans l'option
    assert "sans --probe-serial" not in capsys.readouterr().err
    ws = _workspace(project)
    assert ws["settings"][gen.PROBE_SERIAL_SETTING] == "066DFF3A"
    [launch] = ws["launch"]["configurations"]
    assert launch["openOCDLaunchCommands"] == ["adapter serial 066DFF3A"]
    flash = {t["label"]: t for t in ws["tasks"]["tasks"]}["lepton : flasher demo-debug-board"]
    cfg = project / "trunk" / "sys/root/src/kernel/dev/bsp/board-c/openocd/board-c.cfg"
    assert flash["args"][:4] == ["-f", str(cfg), "-c", "adapter serial 066DFF3A"]
    assert flash["args"][-2] == "-c" and flash["args"][-1].startswith("program ")

    assert main(["generate", "-C", str(project), "--probe-serial", ""]) == 0
    ws = _workspace(project)
    assert gen.PROBE_SERIAL_SETTING not in ws["settings"]
    assert "openOCDLaunchCommands" not in ws["launch"]["configurations"][0]

    before = _snapshot(project)
    capsys.readouterr()
    assert main(["generate", "-C", str(project), "--probe-serial", "a b"]) == 1
    assert "--probe-serial « a b »" in capsys.readouterr().err
    assert _snapshot(project) == before


def test_schema_associations(project, tools):
    """CFG-7 (N4) : manifestes JSON et XML mklepton associés aux schémas du paquet lepton."""
    assert main(["generate", "-C", str(project)]) == 0
    s = _workspace(project)["settings"]
    schemas = gen.schemas_dir()
    assert s["json.schemas"] == [
        {"fileMatch": ["**/lepton-greffon.json"], "url": (schemas / "greffon.schema.json").as_uri()},
        {"fileMatch": ["**/lepton-graine.json"], "url": (schemas / "graine.schema.json").as_uri()}]
    xsd = schemas / "mklepton.xsd"
    assert xsd.is_file() and all(Path(e["url"][len("file://"):]).is_file() for e in s["json.schemas"])
    patterns = [e["pattern"] for e in s["xml.fileAssociations"]]
    assert {e["systemId"] for e in s["xml.fileAssociations"]} == {str(xsd)}
    assert patterns == ["**/mkconf_*.xml"]                               # XML de la graine compris
    assert s["json.validate.enable"] is False      # ENV-12 lot 4 : erreurs par l'extension (lepton check --stdin)
    # O-b (ENV-12 lot 6 S3) : CMake Tools n'édite pas les CMakeLists à la création ou à la suppression
    assert s["cmake.modifyLists.addNewSourceFiles"] == s["cmake.modifyLists.removeDeletedSourceFiles"] == "no"
    _set_graine(project, mklepton_xml="sys/user/demo/etc/projet.xml")
    assert main(["generate", "-C", str(project)]) == 0
    patterns = [e["pattern"] for e in _workspace(project)["settings"]["xml.fileAssociations"]]
    assert patterns == ["**/mkconf_*.xml", "**/sys/user/demo/etc/projet.xml"]


def test_check_task_reports_errors(project, tools):
    """CFG-7 (option 2) : tâche « lepton : vérifier », anomalies de lepton check en erreur (Problems)."""
    assert main(["generate", "-C", str(project)]) == 0
    task = {t["label"]: t for t in _workspace(project)["tasks"]["tasks"]}["lepton : vérifier"]
    assert task["args"] == ["check", "-C", str(project)]
    matcher = task["problemMatcher"]
    assert matcher["severity"] == "error" and matcher["fileLocation"] == ["autoDetect", str(project)]
    regexp = re.compile(matcher["pattern"]["regexp"])
    group = lambda line, n: regexp.match(line) and regexp.match(line).group(n)
    json_line = "trunk/sys/root/src/lepton-greffon.json: /type: 'xyz' is not one of ['noyau']"
    xml_line = "trunk/sys/user/demo/etc/mkconf_demo.xml: 12: element inconnu: Schemas validity error"
    assert [group(json_line, n) for n in (1, 2, 3)] == [
        "trunk/sys/root/src/lepton-greffon.json", None, "/type: 'xyz' is not one of ['noyau']"]
    assert [group(xml_line, n) for n in (1, 2)] == ["trunk/sys/user/demo/etc/mkconf_demo.xml", "12"]
    assert regexp.match("5 fichier(s) conforme(s).") is None
    assert regexp.match("lepton: attention: xmllint absent : XML mklepton non validé") is None


def test_build_tasks_gcc_matcher(project, tools):
    """L6-7 (ENV-12) : aucun matcher fourni par une extension absente (`$gcc`) ; diagnostics de gcc lus
    par le matcher écrit dans la tâche."""
    assert main(["generate", "-C", str(project)]) == 0
    tasks = _workspace(project)["tasks"]["tasks"]
    assert "$gcc" not in json.dumps(tasks)
    builds = [t for t in tasks if t["label"].startswith("lepton : construire") or "mklepton" in t["label"]]
    assert len(builds) == 2
    for task in builds:
        matcher = task["problemMatcher"]
        assert matcher["fileLocation"] == ["autoDetect", str(project / "trunk")]
        regexp = re.compile(matcher["pattern"]["regexp"])
        m = regexp.match("/r/trunk/sys/root/src/a.c:12:5: error: 'x' undeclared (first use in this function)")
        assert m and m.groups() == ("/r/trunk/sys/root/src/a.c", "12", "5", "error",
                                    "'x' undeclared (first use in this function)")
        assert regexp.match("/r/trunk/b.h:3:1: fatal error: c.h: No such file or directory").group(4) == "error"
        assert regexp.match("a.c:7:2: warning: unused variable 'y' [-Wunused-variable]").group(4) == "warning"
        assert regexp.match("[12/40] Building C object …") is None


def test_check_names_grafted_manifests_by_trunk(project, capsys):
    """IDE-4 : lepton check désigne un manifeste greffé par le trunk (chemin ouvert par la tâche)."""
    capsys.readouterr()
    main(["check", "--json", "-C", str(project)])
    files = json.loads(capsys.readouterr().out)["files"]
    manifests = [f for f in files if f.endswith("lepton-greffon.json")]
    assert manifests and all(f.startswith("trunk/sys/root/src/") for f in manifests)
    assert all((project / f).is_symlink() for f in manifests)


def test_active_compile_commands_primed(project, tools, capsys):
    """IDE-3 (O10) : build/.active amorcé depuis le premier preset configuré, jamais écrasé ;
    aucun preset configuré → avertissement."""
    _set_graine(project, configurations=[
        {"nom": "debug-qemu", "construction": "Debug", "execution": "qemu"},
        {"nom": "release-qemu", "construction": "Release", "execution": "qemu"}])
    active = project / "build" / gen.ACTIVE_DIR / gen.COMPILE_COMMANDS
    assert main(["generate", "-C", str(project)]) == 0
    assert not active.exists() and "aucun preset configuré" in capsys.readouterr().err

    release = project / "build" / "demo-release-qemu" / gen.COMPILE_COMMANDS
    release.parent.mkdir(parents=True, exist_ok=True)
    release.write_text("[]\n")
    assert main(["generate", "-C", str(project)]) == 0
    assert active.read_text() == "[]\n" and "aucun preset configuré" not in capsys.readouterr().err

    debug = project / "build" / "demo-debug-qemu" / gen.COMPILE_COMMANDS
    debug.parent.mkdir(parents=True, exist_ok=True)
    debug.write_text('[{"file": "x.c"}]\n')
    assert main(["generate", "-C", str(project)]) == 0
    assert active.read_text() == "[]\n"                                 # base de CMake Tools gardée
    active.unlink()
    assert main(["generate", "-C", str(project)]) == 0
    assert active.read_text() == debug.read_text()                      # premier preset de la graine
    assert_trunk_clean(project)


def test_cmake_api_query_per_preset(project, tools):
    """ENV-12 lot 5 : requête codemodel-v2 propre à lepton dans chaque répertoire de construction de la
    graine (seed tree lit la réponse, même après une configuration sans CMake Tools)."""
    _set_graine(project, configurations=[
        {"nom": "debug-qemu", "construction": "Debug", "execution": "qemu"},
        {"nom": "release-qemu", "construction": "Release", "execution": "qemu"}])
    assert main(["generate", "-C", str(project)]) == 0
    for preset in ("demo-debug-qemu", "demo-release-qemu"):
        query = project / "build" / preset / gen.API_QUERY
        assert json.loads(query.read_text()) == {"requests": [{"kind": "codemodel", "version": 2}]}
    assert_trunk_clean(project)


def test_qemu_configuration_needs_qemu_bsp(project, repos, tools, capsys):
    assert main(["seed", "add", "board-c", str(repos["bsp2"]), "--type", "bsp", "-C", str(project),
                 "--no-cmake"]) == 0
    assert main(["generate", "-C", str(project)]) == 1         # graine : debug-qemu, BSP sans qemu
    assert "ne déclare pas qemu" in capsys.readouterr().err
    assert not (project / "demo.code-workspace").exists()


def test_cfg4_option_values_in_presets(project, tools, capsys):
    """CFG-4 (N5) : valeurs de la graine → LEPTON_OPTION_<greffon>_<NOM> ; valeur refusée → code 1."""
    bsp = next(m.path for m in Rootstock(project).manifests().values() if m.name == "board-q")
    data = json.loads(bsp.read_text(encoding="utf-8"))
    data["options"] = [
        {"nom": "BAUDS", "type": "entier", "defaut": 9600, "min": 1200, "max": 115200,
         "portee": "privee", "description": "Débit."},
        {"nom": "TRACE", "type": "booleen", "defaut": False, "portee": "privee", "description": "Traces."},
        {"nom": "NOM_CARTE", "type": "chaine", "defaut": "q", "portee": "privee", "description": "Nom."}]
    bsp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    _set_graine(project, options={"board-q": {"BAUDS": 115200, "TRACE": True, "NOM_CARTE": "carte q"}})
    assert main(["generate", "-C", str(project)]) == 0
    presets = json.loads((project / "trunk" / gen.PRESETS_FILE).read_text(encoding="utf-8"))
    cache = presets["configurePresets"][0]["cacheVariables"]
    assert {k: v for k, v in cache.items() if k.startswith(gen.OPTION_PREFIX)} == {
        "LEPTON_OPTION_board-q_BAUDS": "115200", "LEPTON_OPTION_board-q_TRACE": "1",
        "LEPTON_OPTION_board-q_NOM_CARTE": "carte q"}

    before = _snapshot(project)
    _set_graine(project, options={"board-q": {"BAUDS": 300}})
    capsys.readouterr()
    assert main(["generate", "-C", str(project)]) == 1
    err = capsys.readouterr().err
    assert "valeurs d'options de la graine refusées (CFG-4)" in err and "300 hors des bornes [1200, 115200]" in err
    after = _snapshot(project)
    after.pop(str(_graine(project)), None)
    assert {k: v for k, v in before.items()} == after          # rien d'écrit


def test_missing_tool_is_exit_2(project, tools, monkeypatch, capsys):
    """NF-3 : outil introuvable dans le PATH → code 2, rien d'écrit."""
    which = gen.shutil.which
    absent = {"arm-none-eabi-gdb", "gdb-multiarch"}
    monkeypatch.setattr(gen.shutil, "which", lambda n, *a, **k: None if n in absent else which(n, *a, **k))
    assert main(["generate", "-C", str(project)]) == 2
    err = capsys.readouterr().err
    assert "arm-none-eabi-gdb absent" in err and "arm-none-eabi-gdb ou gdb-multiarch" in err
    assert not (project / "demo.code-workspace").exists()


def test_gdb_multiarch_when_no_arm_gdb(project, tools, monkeypatch):
    """Debian : pas d'arm-none-eabi-gdb, gdb-multiarch retenu pour le débogage."""
    (tools / "gdb-multiarch").write_text("#!/bin/sh\necho ok\n")
    (tools / "gdb-multiarch").chmod(0o755)
    which = gen.shutil.which
    monkeypatch.setattr(gen.shutil, "which", lambda n, *a, **k: None if n == "arm-none-eabi-gdb" else which(n, *a, **k))
    assert main(["generate", "-C", str(project)]) == 0
    ws = _workspace(project)
    [launch] = ws["launch"]["configurations"]
    assert launch["gdbPath"] == str(tools / "gdb-multiarch")
    assert ws["settings"]["cortex-debug.gdbPath"] == str(tools / "gdb-multiarch")


def _fake_gdb(d: Path, name: str, python: bool) -> Path:
    d.mkdir(exist_ok=True)
    (d / name).write_text("#!/bin/sh\n" + ("echo ok\n" if python else "echo 'Python scripting is not supported' >&2\n"))
    (d / name).chmod(0o755)
    return d / name


def test_find_gdb_prefers_python(tmp_path, monkeypatch, capsys):
    """O9 : arm-none-eabi-gdb sans Python (Arm GNU Toolchain) en tête du PATH, gdb avec Python ensuite
    (MacPorts, lien gdb-multiarch) : le second est retenu, sans avertissement."""
    arm = _fake_gdb(tmp_path / "arm", "arm-none-eabi-gdb", python=False)
    ports = _fake_gdb(tmp_path / "ports", "arm-none-eabi-gdb", python=True)
    local = tmp_path / "local"
    local.mkdir()
    (local / "gdb-multiarch").symlink_to(ports)
    monkeypatch.setenv("PATH", os.pathsep.join(map(str, (arm.parent, local, ports.parent))))
    assert gen.find_gdb() == str(ports)
    assert "AVERTISSEMENT" not in capsys.readouterr().err
    monkeypatch.setenv("PATH", os.pathsep.join(map(str, (arm.parent, local))))
    assert gen.find_gdb() == str(local / "gdb-multiarch")          # Debian : gdb-multiarch seul avec Python


def test_find_gdb_without_python_warns(tmp_path, monkeypatch, capsys):
    """O9 : aucun gdb avec Python → le premier trouvé, avertissement ; aucun gdb → code 2."""
    arm = _fake_gdb(tmp_path / "arm", "arm-none-eabi-gdb", python=False)
    _fake_gdb(tmp_path / "multi", "gdb-multiarch", python=False)
    monkeypatch.setenv("PATH", os.pathsep.join(map(str, (tmp_path / "multi", arm.parent))))
    assert gen.find_gdb() == str(arm)
    assert "aucun gdb avec Python" in capsys.readouterr().err
    monkeypatch.setenv("PATH", str(tmp_path / "vide"))
    with pytest.raises(gen.LeptonError) as e:
        gen.find_gdb()
    assert e.value.code == 2


def test_find_clangd(tools, monkeypatch):
    """PA-1 : clangd LLVM le plus récent du PATH, jamais celui d'Apple ; --clangd prioritaire."""
    monkeypatch.setenv("PATH", str(tools))
    assert gen.find_clangd(None) == str(tools / "clangd-mp-21")
    assert gen.find_clangd(str(tools / "clangd-19")) == str(tools / "clangd-19")


def test_status_and_lock_with_project_scion(project, tools, capsys):
    """Greffon du projet : rôle « projet » dans seed status ; hors du verrou (dépôt de la graine)."""
    assert main(["generate", "-C", str(project)]) == 0
    _git(_seed(project), "add", "-A")
    _git(_seed(project), "commit", "-q", "-m", "presets")
    capsys.readouterr()
    assert main(["seed", "status", "--json", "-C", str(project)]) == 0
    roles = {s["key"]: s["role"] for s in json.loads(capsys.readouterr().out)["scions"]}
    assert roles[project_key("demo")] == "projet"
    assert main(["seed", "lock", "-C", str(project), "--no-cmake"]) == 0
    lock = json.loads((_seed(project) / "scion" / ".scion" / "lepton-graine.lock.json").read_text())
    assert project_key("demo") not in {e["key"] for e in lock["scions"]}
    _git(_seed(project), "add", "-A")
    _git(_seed(project), "commit", "-q", "-m", "verrou")
    assert main(["seed", "lock", "--verify", "-C", str(project)]) == 0
    capsys.readouterr()
    main(["check", "--json", "-C", str(project)])     # anomalies propres aux fixtures factices de conftest
    anomalies = json.dumps(json.loads(capsys.readouterr().out)["anomalies"])
    assert "project" not in anomalies and gen.PRESETS_FILE not in anomalies


# --------------------------------------------------------------------------
# F7 (O2) : seed config add / remove
# --------------------------------------------------------------------------
def _configs(root: Path) -> list[dict]:
    return json.loads(_graine(root).read_text(encoding="utf-8"))["configurations"]


def test_config_add_remove_regenere(project, tools, capsys):
    assert main(["seed", "config", "add", "release-qemu", "--build-type", "Release", "--run", "qemu",
                 "-C", str(project)]) == 0
    assert _configs(project)[-1] == {"nom": "release-qemu", "construction": "Release", "execution": "qemu"}
    presets = json.loads((project / "trunk" / gen.PRESETS_FILE).read_text())
    assert [p["name"] for p in presets["configurePresets"]] == ["demo-debug-qemu", "demo-release-qemu"]
    assert "demo-release-qemu" in json.dumps(_workspace(project))
    (project / "build" / "demo-release-qemu").mkdir(parents=True, exist_ok=True)
    capsys.readouterr()
    assert main(["seed", "config", "remove", "release-qemu", "-C", str(project)]) == 0
    out = capsys.readouterr().out
    assert f"répertoire de construction conservé : {project / 'build' / 'demo-release-qemu'}" in out
    presets = json.loads((project / "trunk" / gen.PRESETS_FILE).read_text())
    assert [p["name"] for p in presets["configurePresets"]] == ["demo-debug-qemu"]
    assert_trunk_clean(project)


def test_config_status_json(project, capsys):
    """Configurations listées par seed status (--json : choix de la palette, F7 d'ENV-12)."""
    assert main(["seed", "config", "add", "rel", "--build-type", "MinSizeRel", "--run", "qemu", "--no-generate",
                 "-C", str(project)]) == 0
    capsys.readouterr()
    main(["seed", "status", "--json", "-C", str(project)])
    assert json.loads(capsys.readouterr().out)["configurations"] == [
        {"name": "debug-qemu", "build_type": "Debug", "run": "qemu", "preset": "demo-debug-qemu"},
        {"name": "rel", "build_type": "MinSizeRel", "run": "qemu", "preset": "demo-rel"}]
    main(["seed", "status", "-C", str(project)])
    assert "configurations : debug-qemu (Debug, qemu), rel (MinSizeRel, qemu)" in capsys.readouterr().out


def test_config_no_generate(project, capsys):
    capsys.readouterr()
    assert main(["seed", "config", "add", "rel", "--build-type", "MinSizeRel", "--run", "qemu", "--no-generate",
                 "-C", str(project)]) == 0
    assert "lepton generate" in capsys.readouterr().out
    assert not (project / "trunk" / gen.PRESETS_FILE).exists()


@pytest.mark.parametrize("argv, message", [
    (["add", "debug-qemu", "--build-type", "Debug", "--run", "qemu"], "déjà dans la graine"),
    (["add", "debug-board", "--build-type", "Debug", "--run", "carte"], "le BSP board-q ne déclare pas openocd"),
    (["add", "Rel", "--build-type", "Release", "--run", "qemu"], "NAME « Rel » refusé"),
    (["remove", "absente"], "absente de la graine (debug-qemu)"),
    (["remove", "debug-qemu"], "seule configuration de la graine"),
])
def test_config_refus(project, capsys, argv, message):
    before = _graine(project).read_text(encoding="utf-8")
    capsys.readouterr()
    assert main(["seed", "config", *argv, "--no-generate", "-C", str(project)]) == 1
    assert message in capsys.readouterr().err
    assert _graine(project).read_text(encoding="utf-8") == before
