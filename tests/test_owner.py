"""ENV-12 lot 3 : propriétaire d'un chemin (file owner), adoption d'un fichier du trunk (file add
--adopt, FIC-3), regreffe par chemin (graft --path, FIC-1) et champ stem de seed status."""

import json
from pathlib import Path

from conftest import assert_trunk_clean
from lepton.cli import main

SRC = "trunk/sys/root/src"
BOARD = f"{SRC}/kernel/dev/bsp/board-q"
BOARD_CLONE = "scion/sys/root/src/kernel/dev/bsp/board-q"


def _lepton(project: Path, *argv: str) -> int:
    return main([*argv, "-C", str(project)])


def _owner(project: Path, capsys, path: Path) -> tuple[int, dict]:
    capsys.readouterr()
    code = _lepton(project, "file", "owner", str(path), "--json")
    return code, json.loads(capsys.readouterr().out)


# --- file owner ----------------------------------------------------------------------------------
def test_owner_link_clone_directory(project, repos, capsys):
    clone = (repos["bsp"] / BOARD_CLONE).resolve()
    code, r = _owner(project, capsys, project / BOARD / "board.c")
    assert code == 0 and r["status"] == "owned" and r["kind"] == "link" and r["source"] == "link"
    assert r["owner"] == {"name": "board-q", "key": r["owner"]["key"], "in_seed": True,
                          "clone_path": str(clone / "board.c")}
    assert r["relative"] == "sys/root/src/kernel/dev/bsp/board-q/board.c"
    code, r = _owner(project, capsys, clone / "board.c")
    assert code == 0 and r["kind"] == "clone" and r["source"] == "clone"
    assert r["trunk_path"] == str(project / BOARD / "board.c")
    code, r = _owner(project, capsys, project / BOARD / "new/deep.c")          # chemin nouveau
    assert code == 0 and r["kind"] == "absent" and r["source"] == "directory"
    assert r["owner"]["clone_path"] == str(clone / "new/deep.c")
    code, r = _owner(project, capsys, project / BOARD)                         # répertoire du trunk
    assert code == 0 and r["kind"] == "directory" and r["owner"]["name"] == "board-q"


def test_owner_ambiguous_none_outside(project, tmp_path, monkeypatch, capsys):
    code, r = _owner(project, capsys, project / SRC / "kernel/dev/new.c")
    assert code == 1 and r["status"] == "ambiguous" and r["owner"] is None
    assert {c["name"] for c in r["candidates"]} == {"fam-test", "board-q"}
    # répertoires sans feuille créés dans le trunk : propriétaire du premier parent qui en a
    (project / BOARD / "a/b").mkdir(parents=True)
    code, r = _owner(project, capsys, project / BOARD / "a/b/x.c")
    assert code == 0 and r["owner"]["name"] == "board-q"
    code, r = _owner(project, capsys, project / BOARD / "a")
    assert code == 0 and r["kind"] == "directory" and r["owner"]["name"] == "board-q"
    (project / BOARD / "a/b").rmdir()
    (project / BOARD / "a").rmdir()
    monkeypatch.setattr("lepton.files._owners_under", lambda owners, d: [])   # trunk sans feuille
    code, r = _owner(project, capsys, project / BOARD / "x.c")
    assert code == 1 and r["status"] == "none" and r["candidates"] == [] and r["source"] is None
    monkeypatch.undo()
    assert _lepton(project, "file", "owner", str(tmp_path / "elsewhere.c")) == 1
    assert "ni dans le trunk" in capsys.readouterr().err
    assert _lepton(project, "file", "owner", str(project / BOARD / "board.c")) == 0   # sortie texte
    assert "board-q" in capsys.readouterr().out
    # liste de scion et fichiers système du trunk : ignorés (F3 ne les déplace pas)
    for p in (project / "trunk/.scion.grafted.list", project / BOARD / ".DS_Store"):
        p.touch()
        code, r = _owner(project, capsys, p)
        assert code == 1 and r["kind"] == "ignored" and r["owner"] is None
    (project / BOARD / ".DS_Store").unlink()
    assert _lepton(project, "file", "owner", str(project / BOARD / "board.c")) == 0
    assert "board-q" in capsys.readouterr().out


# --- file add --adopt (FIC-3) --------------------------------------------------------------------
def test_adopt_moves_regular_file(project, repos, capsys):
    stray = project / BOARD / "drivers/spi.c"
    stray.parent.mkdir()
    stray.write_text("/* créé dans le trunk par l'éditeur */\n")
    assert _lepton(project, "file", "add", str(stray), "--adopt") == 0
    clone = repos["bsp"] / BOARD_CLONE / "drivers/spi.c"
    assert clone.read_text() == "/* créé dans le trunk par l'éditeur */\n"
    assert stray.is_symlink() and stray.resolve() == clone.resolve()
    assert_trunk_clean(project)


def test_adopt_ambiguous_then_scion(project, repos, capsys):
    stray = project / SRC / "kernel/dev/new.c"
    stray.write_text("x\n")
    assert _lepton(project, "file", "add", str(stray), "--adopt") == 1
    assert "plusieurs greffons" in capsys.readouterr().err
    assert stray.is_file() and not stray.is_symlink()                    # laissé tel quel
    assert _lepton(project, "file", "add", str(stray), "--adopt", "--scion", "fam-test") == 0
    assert (repos["family"] / "scion/sys/root/src/kernel/dev/new.c").read_text() == "x\n"
    assert_trunk_clean(project)


def test_adopt_refusals(project, repos, capsys):
    assert _lepton(project, "file", "add", str(project / BOARD / "board.c"), "--adopt") == 1      # lien
    assert "pas un fichier régulier" in capsys.readouterr().err
    assert _lepton(project, "file", "add", str(project / BOARD / "absent.c"), "--adopt") == 1     # absent
    assert _lepton(project, "file", "add", str(repos["bsp"] / BOARD_CLONE / "board.c"), "--adopt") == 1
    # homonyme déjà présent dans le clone (non greffé) : refus, fichier du trunk conservé
    (repos["bsp"] / BOARD_CLONE / "dup.c").write_text("clone\n")
    (project / BOARD / "dup.c").write_text("trunk\n")
    capsys.readouterr()
    assert _lepton(project, "file", "add", str(project / BOARD / "dup.c"), "--adopt") == 1
    assert "existe déjà" in capsys.readouterr().err
    assert (project / BOARD / "dup.c").read_text() == "trunk\n"
    (project / BOARD / "dup.c").unlink()
    assert _lepton(project, "graft") == 0
    assert_trunk_clean(project)


def test_adopt_cmake_file_reconfigures(project, fake_build):
    (project / BOARD / "x.c").write_text("")
    assert _lepton(project, "file", "add", str(project / BOARD / "x.c"), "--adopt") == 0
    assert not fake_build.exists()
    (project / BOARD / "CMakeLists.txt").write_text("# vide\n")
    assert _lepton(project, "file", "add", str(project / BOARD / "CMakeLists.txt"), "--adopt") == 0
    assert fake_build.read_text().count("-S") == 1


# --- graft --path (FIC-1, observateur F2) --------------------------------------------------------
def test_graft_path_created_and_deleted(project, repos, fake_build, capsys):
    clone = repos["bsp"] / BOARD_CLONE
    (clone / "new.c").write_text("")
    (clone / "sub").mkdir()
    (clone / "sub/deep.h").write_text("")
    assert _lepton(project, "graft", "--path", str(clone / "new.c"), "--path", str(clone / "sub/deep.h")) == 0
    assert (project / BOARD / "new.c").is_symlink() and (project / BOARD / "sub/deep.h").is_symlink()
    assert not fake_build.exists()                                       # pas de CMake pour un .c
    (clone / "new.c").unlink()
    assert _lepton(project, "graft", "--path", str(clone / "new.c")) == 0   # chemin supprimé
    assert not (project / BOARD / "new.c").exists() and not (project / BOARD / "new.c").is_symlink()
    assert not fake_build.exists()
    (clone / "CMakeLists.txt").write_text("")
    assert _lepton(project, "graft", "--path", str(clone / "CMakeLists.txt")) == 0
    assert fake_build.read_text().count("-S") == 1
    assert_trunk_clean(project)


def test_graft_path_refusals(project, tmp_path, capsys):
    assert _lepton(project, "graft", "--path", str(tmp_path / "x.c")) == 1
    assert _lepton(project, "graft", "--path", str(project / BOARD / "absent.c")) == 1
    assert "greffon non déterminé" in capsys.readouterr().err


# --- seed status --json : stem -------------------------------------------------------------------
def test_status_stem(project, repos, capsys):
    capsys.readouterr()
    _lepton(project, "seed", "status", "--json")
    scions = {s["name"]: s for s in json.loads(capsys.readouterr().out)["scions"]}
    assert scions["board-q"]["stem"] == str((repos["bsp"] / "scion").resolve())
    assert all(Path(s["stem"]).name == "scion" for s in scions.values())
