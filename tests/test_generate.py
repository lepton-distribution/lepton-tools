"""ENV-9 : lepton generate — presets CMake (graine), espace de travail VSCodium (rootstock).

Exigences : CFG-1 (aucune lecture du XML mklepton), CFG-6 (un preset par configuration), BLD-5
(mêmes presets partout), IDE-2 (un dossier par dépôt git), IDE-3/IDE-4 (trunk seul chemin
d'ouverture, clangd), DBG-1 à DBG-3 (launch, tasks), NF-3 (outils résolus par le PATH).
"""

import json
import os
import subprocess
from pathlib import Path

import pytest

from conftest import MKCONF, assert_trunk_clean, url
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
TOOLS = {"arm-none-eabi-gcc": "", "arm-none-eabi-gdb": "", "qemu-system-arm": "", "openocd": "",
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
        "LEPTON_BOARD": "board-q", "LEPTON_KAL_BACKEND": "embos", "LEPTON_MKCONF": MKCONF}
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


def test_qemu_configuration_needs_qemu_bsp(project, repos, tools, capsys):
    assert main(["seed", "add", "board-c", str(repos["bsp2"]), "--type", "bsp", "-C", str(project),
                 "--no-cmake"]) == 0
    assert main(["generate", "-C", str(project)]) == 1         # graine : debug-qemu, BSP sans qemu
    assert "ne déclare pas qemu" in capsys.readouterr().err
    assert not (project / "demo.code-workspace").exists()


def test_missing_tool_is_exit_2(project, tools, monkeypatch, capsys):
    """NF-3 : outil introuvable dans le PATH → code 2, rien d'écrit."""
    which = gen.shutil.which
    monkeypatch.setattr(gen.shutil, "which", lambda n, *a, **k: None if n == "arm-none-eabi-gdb" else which(n, *a, **k))
    assert main(["generate", "-C", str(project)]) == 2
    assert "arm-none-eabi-gdb absent" in capsys.readouterr().err
    assert not (project / "demo.code-workspace").exists()


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
