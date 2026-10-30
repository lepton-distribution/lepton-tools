"""Jalon 5 d'ENV-8 : fichiers et regreffe — file, dir, graft (FIC-1, FIC-2, FIC-3, FIC-6)."""

import os
import subprocess
from pathlib import Path

from conftest import assert_trunk_clean
from lepton.cli import main

SRC = "trunk/sys/root/src"
BOARD = f"{SRC}/kernel/dev/bsp/board-q"
BOARD_CLONE = "scion/sys/root/src/kernel/dev/bsp/board-q"


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout


def _lepton(project: Path, *argv: str) -> int:
    return main([*argv, "-C", str(project)])


# --- FIC-1 ---------------------------------------------------------------------------------------
def test_fic1_file_add_remove(project, repos, monkeypatch, capsys):
    clone = repos["bsp"] / BOARD_CLONE
    # chemin du trunk absolu : propriétaire = greffon des feuilles du répertoire
    assert _lepton(project, "file", "add", str(project / BOARD / "uart.c")) == 0
    assert (clone / "uart.c").is_file() and (project / BOARD / "uart.c").is_symlink()
    assert "?? " in _git(repos["bsp"], "status", "--porcelain")          # pas de git add (Q7)
    assert_trunk_clean(project)
    # chemin relatif au répertoire courant, dans un sous-répertoire nouveau
    monkeypatch.chdir(project / BOARD)
    assert main(["file", "add", "drivers/spi.c"]) == 0
    assert (clone / "drivers/spi.c").is_file() and (project / BOARD / "drivers/spi.c").is_symlink()
    # chemin donné dans le clone
    assert _lepton(project, "file", "add", str(clone / "in_clone.c")) == 0
    assert (project / BOARD / "in_clone.c").is_symlink()
    # déjà présent : refus
    capsys.readouterr()
    assert _lepton(project, "file", "add", str(project / BOARD / "board.c")) == 1
    assert "existe déjà" in capsys.readouterr().err
    # retrait d'un fichier non suivi, puis d'un fichier suivi (git rm)
    assert _lepton(project, "file", "remove", str(project / BOARD / "uart.c")) == 0
    assert not (clone / "uart.c").exists() and not (project / BOARD / "uart.c").exists()
    assert _lepton(project, "file", "remove", str(project / BOARD / "board.c")) == 0
    assert "D  scion/sys/root/src/kernel/dev/bsp/board-q/board.c" in _git(repos["bsp"], "status", "--porcelain")
    assert not (project / BOARD / "board.c").exists()
    # retrait d'un chemin absent : refus
    assert _lepton(project, "file", "remove", str(project / BOARD / "absent.c")) == 1
    assert_trunk_clean(project)


def test_fic1_cmake_reconfigured_only_for_cmake_files(project, fake_build):
    assert _lepton(project, "file", "add", str(project / BOARD / "x.c")) == 0
    assert not fake_build.exists()
    assert _lepton(project, "file", "add", str(project / BOARD / "CMakeLists.txt")) == 0
    assert fake_build.read_text().count("-S") == 1


# --- FIC-2 ---------------------------------------------------------------------------------------
def test_fic2_dir_add_remove(project, repos, capsys):
    clone = repos["bsp"] / BOARD_CLONE
    assert _lepton(project, "dir", "add", str(project / BOARD / "sub/deep")) == 0
    assert (clone / "sub/deep/.gitkeep").is_file()
    assert (project / BOARD / "sub/deep/.gitkeep").is_symlink()
    assert _lepton(project, "file", "add", str(project / BOARD / "sub/a.c")) == 0
    assert _lepton(project, "dir", "add", str(project / BOARD / "sub")) == 1          # existe
    # répertoire non suivi
    assert _lepton(project, "dir", "remove", str(project / BOARD / "sub")) == 0
    assert not (clone / "sub").exists() and not (project / BOARD / "sub").exists()
    assert_trunk_clean(project)
    # répertoire suivi (git rm -r), avec un fichier non suivi en plus
    assert _lepton(project, "dir", "add", str(project / BOARD / "drv")) == 0
    _git(repos["bsp"], "add", "-A")
    _git(repos["bsp"], "commit", "-q", "-m", "drv")
    assert _lepton(project, "file", "add", str(project / BOARD / "drv/tmp.c")) == 0
    assert _lepton(project, "dir", "remove", str(project / BOARD / "drv")) == 0
    assert not (clone / "drv").exists() and not (project / BOARD / "drv").exists()
    assert "D  scion/sys/root/src/kernel/dev/bsp/board-q/drv/.gitkeep" in _git(repos["bsp"], "status", "--porcelain")
    assert_trunk_clean(project)


def test_fic2_dir_remove_several_owners(project, repos, capsys):
    kdev = project / SRC / "kernel/dev"
    assert _lepton(project, "dir", "remove", str(kdev)) == 1
    err = capsys.readouterr().err
    assert "plusieurs greffons" in err and "fam-test" in err and "board-q" in err
    assert _lepton(project, "dir", "remove", str(kdev), "--scion", "lepton-noyau") == 1
    assert (repos["family"] / "scion/sys/root/src/kernel/dev/arch/cortexm/fam-test/uart.c").is_file()


# --- FIC-3 ---------------------------------------------------------------------------------------
def test_fic3_refus_sans_proprietaire(project, tmp_path, capsys):
    (project / "trunk/empty").mkdir()                 # répertoire du trunk sans aucune feuille : on remonte
    assert _lepton(project, "file", "add", str(project / "trunk/empty/x.c")) == 1
    assert "plusieurs greffons possèdent trunk " in capsys.readouterr().err
    assert not (project / "trunk/empty/x.c").exists()
    assert _lepton(project, "file", "add", str(tmp_path / "elsewhere.c")) == 1
    assert "ni dans le trunk" in capsys.readouterr().err
    assert _lepton(project, "dir", "add", str(project / "trunk/empty/d")) == 1
    (project / "trunk/empty").rmdir()
    assert_trunk_clean(project)


def test_fic3_ambigu_scion_requis(project, repos, capsys):
    path = str(project / SRC / "kernel/dev/new.c")
    assert _lepton(project, "file", "add", path) == 1
    err = capsys.readouterr().err
    assert "plusieurs greffons" in err and "--scion" in err
    assert _lepton(project, "file", "add", path, "--scion", "unknown") == 1
    assert _lepton(project, "file", "add", path, "--scion", "fam-test") == 0
    assert (repos["family"] / "scion/sys/root/src/kernel/dev/new.c").is_file()
    assert (project / SRC / "kernel/dev/new.c").is_symlink()
    # chemin donné dans un clone, --scion contradictoire
    assert _lepton(project, "file", "add", str(repos["bsp"] / BOARD_CLONE / "y.c"), "--scion", "fam-test") == 1
    assert_trunk_clean(project)


# --- FIC-6 ---------------------------------------------------------------------------------------
def test_fic6_git_log_follow(project, repos, capsys):
    assert _lepton(project, "file", "mv", str(project / BOARD / "board.c"), str(project / BOARD / "hw/board_q.c")) == 0
    clone = repos["bsp"] / BOARD_CLONE
    assert (clone / "hw/board_q.c").is_file() and not (clone / "board.c").exists()
    assert (project / BOARD / "hw/board_q.c").is_symlink() and not (project / BOARD / "board.c").exists()
    _git(repos["bsp"], "commit", "-q", "-m", "renommage")
    log = _git(repos["bsp"], "log", "--follow", "--format=%s", "--", f"{BOARD_CLONE}/hw/board_q.c").split("\n")
    assert [l for l in log if l] == ["renommage", "initial"]
    # fichier non suivi : simple renommage
    assert _lepton(project, "file", "add", str(project / BOARD / "u.c")) == 0
    assert _lepton(project, "file", "mv", str(project / BOARD / "u.c"), str(project / BOARD / "v.c")) == 0
    assert (clone / "v.c").is_file() and (project / BOARD / "v.c").is_symlink()
    # destination dans un autre greffon : refus
    capsys.readouterr()
    fam = project / SRC / "kernel/dev/arch/cortexm/fam-test"
    assert _lepton(project, "file", "mv", str(project / BOARD / "v.c"), str(fam / "v.c")) == 1
    assert "déplacement limité à un greffon" in capsys.readouterr().err
    assert_trunk_clean(project)


# --- lepton graft (§3.8, PA-9 Q8) ----------------------------------------------------------------
def test_graft_removes_system_files(project, repos, tmp_path, monkeypatch, capsys):
    # exclusions git globales du test, indépendantes du poste (scion ≥ 0.5.2.0, ENV-15)
    (tmp_path / "excludes").write_text(".DS_Store\n")
    (tmp_path / "gitconfig").write_text(f"[core]\n\texcludesFile = {tmp_path / 'excludes'}\n")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(tmp_path / "gitconfig"))
    for p in (project / "trunk/.DS_Store", project / BOARD / "._board.c"):
        p.write_bytes(b"\0")
    (repos["bsp"] / BOARD_CLONE / ".DS_Store").write_bytes(b"\0")       # venu du clone, ignoré par git
    assert _lepton(project, "graft") == 0
    assert not (project / "trunk/.DS_Store").exists() and not (project / BOARD / "._board.c").exists()
    assert not os.path.lexists(project / BOARD / ".DS_Store")           # non greffé (scion E1)
    assert_trunk_clean(project)
    assert _lepton(project, "graft", "--scion", "board-q") == 0
    assert _lepton(project, "graft", "--scion", "unknown") == 1


def test_graft_refuses_other_regular_files(project, capsys):
    stray = project / BOARD / "stray.c"
    stray.write_text("/* écrit dans le trunk */\n")
    assert _lepton(project, "graft") != 0
    assert stray.is_file() and not stray.is_symlink()                  # jamais supprimé par lepton
    assert _lepton(project, "graft", "--force") == 1                   # contrôle final du trunk
    assert "fichier régulier" in capsys.readouterr().err
    stray.unlink()
