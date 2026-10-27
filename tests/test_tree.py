"""ENV-12 lot 5 : lepton seed tree (vue IDE-1) — réponse de l'API fichier CMake (codemodel-v2) du
preset actif, rattachement des sources aux greffons par le lien du trunk, en-têtes, repli sans réponse,
greffons identiques à ceux de seed status."""

import json
from pathlib import Path

from conftest import assert_trunk_clean
from lepton import tree
from lepton.cli import main
from lepton.rootstock import Rootstock

SRC = "sys/root/src"
KERNEL_C = f"{SRC}/kernel/core/kernel.c"
UART_C = f"{SRC}/kernel/dev/arch/cortexm/fam-test/uart.c"
BOARD_C = f"{SRC}/kernel/dev/bsp/board-q/board.c"
BOARD_CLONE = "scion/sys/root/src/kernel/dev/bsp/board-q"


def _tree(project: Path, capsys, *argv: str) -> tuple[int, dict]:
    capsys.readouterr()
    code = main(["seed", "tree", "--json", "-C", str(project), *argv])
    return code, json.loads(capsys.readouterr().out)


def _write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data))


def _reply(project: Path, preset: str) -> Path:
    """Réponse codemodel-v2 factice : exécutif lepton, bibliothèques kernel et bsp_demarrage, OBJECT
    generated (source hors trunk), utilitaire ignoré, second exécutif kal_bench."""
    build = project / "build" / preset
    reply = build / ".cmake/api/v1/reply"
    generated = build / "generated/board/dev_mkconf.c"
    targets = {
        "lepton": {"type": "EXECUTABLE", "sources": [{"path": KERNEL_C, "compileGroupIndex": 0},
                                                      {"path": "objets.o"}],
                   "dependencies": [{"id": "kernel::@1"}, {"id": "generated::@1"}, {"id": "board_mkconf::@1"}]},
        "kernel": {"type": "STATIC_LIBRARY", "sources": [{"path": KERNEL_C, "compileGroupIndex": 0},
                                                         {"path": UART_C, "compileGroupIndex": 0}],
                   "dependencies": [{"id": "bsp_demarrage::@1"}]},
        "bsp_demarrage": {"type": "OBJECT_LIBRARY", "sources": [{"path": BOARD_C, "compileGroupIndex": 0}]},
        "generated": {"type": "OBJECT_LIBRARY", "sources": [{"path": str(generated), "compileGroupIndex": 0}]},
        "board_mkconf": {"type": "UTILITY", "sources": [{"path": str(build / "CMakeFiles/board_mkconf")}]},
        "kal_bench": {"type": "EXECUTABLE", "sources": [], "dependencies": [{"id": "kernel::@1"}]},
    }
    entries = []
    for name, t in targets.items():
        _write(reply / f"target-{name}.json", {"name": name, "id": f"{name}::@1", **t})
        entries.append({"name": name, "id": f"{name}::@1", "jsonFile": f"target-{name}.json"})
    _write(reply / "codemodel-v2-1.json", {"paths": {"source": str(project / "trunk"), "build": str(build)},
                                           "configurations": [{"name": "Debug", "targets": entries}]})
    _write(reply / "index-2026-10-27T10-00-00-0000.json",
           {"objects": [{"kind": "codemodel", "version": {"major": 2, "minor": 6},
                         "jsonFile": "codemodel-v2-1.json"}]})
    return build


def _presets(project: Path) -> list[str]:
    return tree._presets(Rootstock.discover(project))


def _groups(lib: dict) -> dict:
    return {g["name"]: [f["relative"] for f in g["files"]] for g in lib["scions"]}


def test_tree_from_codemodel(project, repos, capsys):
    (repos["bsp"] / BOARD_CLONE / "board.h").write_text("")
    (repos["bsp"] / BOARD_CLONE / "essai.c").write_text("")              # hors construction (point 5)
    assert main(["graft", "--no-cmake", "-C", str(project)]) == 0
    first = _presets(project)[0]
    build = _reply(project, first)
    code, r = _tree(project, capsys)
    assert code == 0 and r["source"] == "codemodel" and r["preset"] == first and r["message"] is None
    assert r["preset_reason"] == "premier preset configuré" and r["build"] == str(build)
    assert r["build_root"] == str(project / "build")
    assert [e["name"] for e in r["executables"]] == ["lepton", "kal_bench"]         # lepton en premier
    libs = r["executables"][0]["libraries"]
    assert [(lib["name"], lib["type"]) for lib in libs] == [
        ("lepton", "EXECUTABLE"), ("kernel", "STATIC_LIBRARY"), ("generated", "OBJECT_LIBRARY"),
        ("bsp_demarrage", "OBJECT_LIBRARY")]                         # fermeture transitive, utilitaire omis
    assert _groups(libs[0]) == {"lepton-noyau": [KERNEL_C]}                        # objets.o non compilé
    assert _groups(libs[1]) == {"lepton-noyau": [KERNEL_C], "fam-test": [UART_C]}
    gen = libs[2]["scions"][0]
    assert gen["key"] is None and gen["generated"] and gen["files"][0]["trunk_path"] is None
    board = libs[3]["scions"][0]
    assert [(f["relative"], f["kind"]) for f in board["files"]] == [
        (BOARD_C, "compiled"), (f"{SRC}/kernel/dev/bsp/board-q/board.h", "header"),
        (f"{SRC}/kernel/dev/bsp/board-q/essai.c", "unbuilt")]
    assert all(f["kind"] != "unbuilt" for g in libs[1]["scions"] for f in g["files"])   # kernel.c : compilé ailleurs
    assert board["files"][0]["trunk_path"] == str(project / "trunk" / BOARD_C)
    assert board["files"][0]["clone_path"] == str((repos["bsp"] / BOARD_CLONE / "board.c").resolve())
    assert_trunk_clean(project)


def test_tree_scions_are_seed_status(project, capsys):
    """Critère d'ENV-12 : vue cohérente avec seed status (mêmes greffons, même état git)."""
    _reply(project, _presets(project)[0])
    _, r = _tree(project, capsys)
    capsys.readouterr()
    assert main(["seed", "status", "--json", "-C", str(project)]) == 0
    assert r["scions"] == json.loads(capsys.readouterr().out)["scions"]
    keys = {s["key"] for s in r["scions"]}
    shown = {g["key"] for e in r["executables"] for lib in e["libraries"] for g in lib["scions"] if g["key"]}
    assert shown and shown <= keys


def test_tree_active_preset(project, capsys):
    presets = _presets(project)
    for p in presets:
        _reply(project, p)
    last = presets[-1]
    active = project / "build/.active/compile_commands.json"
    _write(active, [{"directory": str(project / "build" / last), "file": "x.c"}])
    _, r = _tree(project, capsys)
    assert r["preset"] == last and r["preset_reason"] == "actif (build/.active)"
    _, r = _tree(project, capsys, "--preset", presets[0])
    assert r["preset"] == presets[0] and r["preset_reason"] == "--preset"


def test_tree_without_reply_falls_back(project, capsys):
    code, r = _tree(project, capsys)
    assert code == 0 and r["source"] == "manifests" and r["executables"] == []
    assert "aucun preset configuré" in r["message"]
    by_name = {g["name"]: [f["relative"] for f in g["files"]] for g in r["by_scion"]}
    assert by_name["lepton-noyau"] == [KERNEL_C]
    assert by_name["fam-test"] == [UART_C] and by_name["board-q"] == [BOARD_C]
    capsys.readouterr()
    assert main(["seed", "tree", "-C", str(project)]) == 0                         # sortie texte
    assert "board-q : 1 source(s), 0 en-tête(s)" in capsys.readouterr().out


def test_tree_unconfigured_preset_refused(project, capsys):
    capsys.readouterr()
    assert main(["seed", "tree", "--preset", "absent", "-C", str(project)]) == 1
    assert "preset absent non configuré" in capsys.readouterr().err
