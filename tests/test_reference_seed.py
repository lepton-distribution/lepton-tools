"""ENV-18 : graine de référence gérée par lepton (PA-23) — lecture et generate acceptés, commandes qui
modifient la graine refusées avant toute action ; rien n'est écrit dans la graine."""

import json
import subprocess
from pathlib import Path

import pytest

from conftest import MKCONF, assert_trunk_clean
from lepton import tree
from lepton.cli import main
from lepton.rootstock import Rootstock
from test_generate import tools  # noqa: F401  (fixture : outils de l'hôte factices)
from test_milestone6 import _preset, _reference

PRESETS = [_preset("board-q-freertos", "board-q", MKCONF),
           {"name": "board-q-embos", "inherits": "board-q-freertos"},
           _preset("board-c-embos", "board-c", MKCONF),
           _preset("absente-embos", "absente", MKCONF)]


@pytest.fixture
def reference(tmp_path, repos) -> Path:
    root = _reference(tmp_path, repos, PRESETS)
    seed = Rootstock(root).seed_root()            # graine commitée, comme original-tree
    for args in (["add", "-A"], ["commit", "-q", "-m", "graine de référence"]):
        subprocess.run(["git", "-C", str(seed), *args], check=True, capture_output=True)
    return root


def _seed_state(root: Path) -> tuple[str, str, list[str]]:
    """État de la graine : fichiers suivis et non suivis, liste des sources, contenu du dépôt."""
    seed = Rootstock(root).seed_root()
    status = subprocess.run(["git", "-C", str(seed), "status", "--porcelain", "--untracked-files=all"],
                            check=True, capture_output=True, text=True).stdout
    sources = (seed / "scion" / ".scion" / ".scion.sources.list").read_text()
    return status, sources, sorted(str(p.relative_to(seed)) for p in seed.rglob("*") if ".git" not in p.parts)


def _workspace(root: Path) -> dict:
    text = (root / "graine.code-workspace").read_text(encoding="utf-8")
    return json.loads(text.split("\n", 1)[1])


def test_reference_status_et_tree(reference, capsys):
    capsys.readouterr()
    assert main(["seed", "status", "-C", str(reference)]) == 0
    out = capsys.readouterr().out
    assert "graine de référence (ni lepton-graine.json ni project/)" in out
    assert "graine hors lepton" not in out
    assert main(["seed", "status", "--json", "-C", str(reference)]) == 0
    status = json.loads(capsys.readouterr().out)
    assert status["configurations"] == [] and status["seed"]["manifest"] is None
    assert {s["name"]: s["role"] for s in status["scions"]}["board-q"] == "bsp"
    # seed tree : presets de carte du noyau, BSP greffé ou non, dans l'ordre du fichier
    assert tree._presets(Rootstock(reference)) == ["board-q-freertos", "board-q-embos", "board-c-embos",
                                                   "absente-embos"]
    assert main(["seed", "tree", "-C", str(reference)]) == 0
    assert main(["file", "owner", str(reference / "trunk" / "CMakePresets.json"), "-C", str(reference)]) == 0


def test_reference_generate(reference, tools, capsys):  # noqa: F811
    before = _seed_state(reference)
    capsys.readouterr()
    assert main(["generate", "-C", str(reference)]) == 0
    out = capsys.readouterr().out
    assert "aucun CMakeUserPresets.json écrit" in out
    assert "BSP « absente » non greffé : preset(s) absente-embos : tâches configurer et construire seulement" in out
    assert _seed_state(reference) == before                    # rien dans la graine (PA-23 Q3)
    assert not (reference / "trunk" / "CMakeUserPresets.json").exists()
    assert_trunk_clean(reference)

    ws = _workspace(reference)
    assert ws["folders"][1]["name"] == "git · graine graine"   # nom du répertoire de la graine (Q2)
    launch = {c["name"]: c for c in ws["launch"]["configurations"]}
    assert set(launch) == {"Déboguer board-q-freertos (QEMU mps2-an386)", "Déboguer board-q-embos (QEMU mps2-an386)",
                           "Déboguer board-c-embos (carte, OpenOCD)"}
    q = launch["Déboguer board-q-embos (QEMU mps2-an386)"]
    assert q["cpu"] == "cortex-m4" and q["executable"] == str(reference / "build" / "board-q-embos" / "lepton.elf")
    assert launch["Déboguer board-c-embos (carte, OpenOCD)"]["configFiles"] == [
        str(reference / "trunk/sys/root/src/kernel/dev/bsp/board-c/openocd/board-c.cfg")]
    labels = [t["label"] for t in ws["tasks"]["tasks"]]
    assert [l for l in labels if "absente" in l] == ["lepton : configurer absente-embos",
                                                     "lepton : construire absente-embos"]
    assert "lepton : QEMU board-q-freertos (console série)" in labels
    assert "lepton : flasher board-c-embos" in labels
    configure = next(t for t in ws["tasks"]["tasks"] if t["label"] == "lepton : configurer board-q-embos")
    assert configure["args"] == ["--preset", "board-q-embos"]     # preset du noyau tel quel
    assert ws["settings"]["xml.fileAssociations"][0]["pattern"] == "**/mkconf_*.xml"
    assert len(ws["settings"]["xml.fileAssociations"]) == 1
    for p in ("board-q-freertos", "board-q-embos", "board-c-embos", "absente-embos"):
        assert (reference / "build" / p / ".cmake/api/v1/query/client-lepton/query.json").is_file()

    assert main(["generate", "-C", str(reference)]) == 0           # deux appels : rien ne change
    assert f"inchangé  {reference / 'graine.code-workspace'}" in capsys.readouterr().out


@pytest.mark.parametrize("argv, command", [
    (["seed", "add", "x", "/nulle/part", "--type", "application"], "seed add"),
    (["seed", "remove", "board-c"], "seed remove"),
    (["seed", "replace", "board-c", "/nulle/part"], "seed replace"),
    (["seed", "lock"], "seed lock"),
    (["seed", "lock", "--verify"], "seed lock"),
    (["seed", "lock", "--restore"], "seed lock"),
    (["seed", "mkconf", "import", MKCONF], "seed mkconf import"),
    (["seed", "config", "add", "release", "--build-type", "Release", "--run", "qemu"], "seed config add"),
    (["seed", "config", "remove", "debug"], "seed config remove"),
    (["scion", "new", "demo-app", "--type", "application"], "scion new"),
    (["scion", "remove", "board-c"], "scion remove"),
])
def test_reference_refus(reference, capsys, argv, command):
    before = _seed_state(reference)
    grafted = (reference / "trunk" / ".scion.grafted.list").read_text()
    capsys.readouterr()
    assert main([*argv, "-C", str(reference)]) == 1
    err = capsys.readouterr().err
    assert f"lepton: erreur: graine de référence {Rootstock(reference).seed_root()} (ni lepton-graine.json " \
           f"ni project/) : lepton {command} modifie la graine, refusé" in err
    assert ("--no-seed" if command == "scion new" else "lepton seed new") in err
    assert _seed_state(reference) == before
    assert (reference / "trunk" / ".scion.grafted.list").read_text() == grafted
    assert not (reference / "depots" / "lepton-application").exists()


def test_reference_scion_new_no_seed(reference, tmp_path, capsys):
    """scion new --no-seed n'écrit pas dans la graine : accepté (PA-23 Q1)."""
    before = _seed_state(reference)
    repo = tmp_path / "demo-app"
    assert main(["scion", "new", "demo-app", "--type", "application", "--no-seed", "--repo", str(repo),
                 "-C", str(reference)]) == 0
    assert (repo / ".git").is_dir()
    assert _seed_state(reference) == before
