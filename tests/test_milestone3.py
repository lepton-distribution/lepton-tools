"""Jalon 3 d'ENV-8 : graine — seed new, status, add, remove, replace (GRA-1 à GRA-4, GRA-6)."""

import json
import subprocess
from pathlib import Path

import pytest

from conftest import MKCONF, assert_trunk_clean, url
from lepton.cli import main
from lepton.rootstock import Rootstock, scion_key
from lepton.seed import parse_location
from lepton.errors import LeptonError
from lepton.validation import validate_file


def _graine(root: Path) -> dict:
    return json.loads(Rootstock(root).seed_manifest_path().read_text())


def _status(root: Path, capsys) -> tuple[int, dict]:
    capsys.readouterr()
    code = main(["seed", "status", "--json", "-C", str(root)])
    return code, json.loads(capsys.readouterr().out)


def _by_name(status: dict) -> dict:
    return {s["name"]: s for s in status["scions"]}


# --- GRA-1 ---------------------------------------------------------------------------------------
def test_gra1_seed_new(project):
    rs = Rootstock(project)
    trunk = rs.trunk
    assert (trunk / MKCONF).is_symlink() and (trunk / MKCONF).exists()
    assert (trunk / "sys/root/src/kernel/dev/bsp/board-q/board.c").is_symlink()
    assert (trunk / "sys/root/src/kernel/dev/arch/cortexm/fam-test/uart.c").is_symlink()
    graine_path = rs.seed_manifest_path()
    assert validate_file(graine_path) == []
    graine = _graine(project)
    assert (graine["noyau"], graine["bsp"], graine["mklepton_xml"]) == ("lepton-noyau", "board-q", MKCONF)
    assert graine["configurations"] == [{"nom": "debug-qemu", "construction": "Debug", "execution": "qemu"}]
    seed_root = rs.seed_root()
    assert seed_root == project / "depots" / "lepton-seed" / "demo"
    assert subprocess.run(["git", "-C", str(seed_root), "status", "--porcelain"],
                          capture_output=True, text=True).stdout == ""
    assert_trunk_clean(project)


def test_gra1_seed_new_refuses_non_empty_dir(tmp_path, repos, capsys):
    root = tmp_path / "busy"
    root.mkdir()
    (root / "file").write_text("x")
    assert main(["seed", "new", "demo", "-C", str(root), "--bsp", "board-q", "--mkconf", MKCONF,
                 "--origin", f"lepton-noyau={repos['kernel']}", "--origin", f"fam-test={repos['family']}",
                 "--origin", f"board-q={repos['bsp']}"]) == 1
    assert "n'est pas un répertoire vide" in capsys.readouterr().err
    assert sorted(p.name for p in root.iterdir()) == ["file"]


# --- GRA-2 ---------------------------------------------------------------------------------------
def test_gra2_kernel_bsp_required(tmp_path, repos, project, capsys):
    # BSP sans origine : refus avant toute action
    root = tmp_path / "no-bsp"
    assert main(["seed", "new", "demo", "-C", str(root), "--bsp", "board-q", "--mkconf", MKCONF,
                 "--origin", f"lepton-noyau={repos['kernel']}", "--origin", f"fam-test={repos['family']}"]) == 1
    assert "origine du BSP" in capsys.readouterr().err and not root.exists()
    # noyau, BSP et famille du BSP ne se retirent pas
    for name in ("lepton-noyau", "board-q", "fam-test"):
        assert main(["seed", "remove", name, "-C", str(project), "--no-cmake"]) == 1
    assert "GRA-2" in capsys.readouterr().err
    assert set(_by_name(_status(project, capsys)[1])) >= {"lepton-noyau", "board-q", "fam-test"}


def test_gra2_bsp_family_mismatch(tmp_path, repos, capsys):
    root = tmp_path / "mismatch"
    code = main(["seed", "new", "demo", "-C", str(root), "--bsp", "board-q", "--mkconf", MKCONF,
                 "--origin", f"lepton-noyau={repos['kernel']}",
                 "--origin", f"other-fam={repos['family']}", "--origin", f"board-q={repos['bsp']}"])
    assert code == 1
    err = capsys.readouterr().err
    assert "attendu « other-fam » de type « famille »" in err and "état laissé" in err


# --- GRA-3 ---------------------------------------------------------------------------------------
def test_gra3_git_and_local_origin(project, repos):
    rs = Rootstock(project)
    sources = {s.key: s for s in rs.sources()}
    kernel = sources["lepton@original::tree"]
    assert (kernel.version, kernel.location) == ("master", url(repos["kernel"]))
    assert (project / "depots/lepton/original/master/.git").is_dir()          # forme git : cloné
    bsp = sources[scion_key("bsp", "board-q")]
    assert (bsp.version, bsp.location) == ("*", str(repos["bsp"]))              # forme locale : en place
    grafted = {e.key: e for e in rs.grafted()}
    assert rs.clone(grafted[scion_key("bsp", "board-q")]) == repos["bsp"]


def test_gra3_parse_location(tmp_path, repos):
    o = parse_location("https://example.org/a/b.git@v1.2:sub/dir")
    assert (o.location, o.version, o.subpath, o.remote) == ("https://example.org/a/b.git", "v1.2", "sub/dir", True)
    o = parse_location("https://example.org/a/b.git")
    assert (o.location, o.version, o.subpath) == ("https://example.org/a/b.git", "master", "")
    o = parse_location(str(repos["app"]))
    assert (o.location, o.version, o.remote) == (str(repos["app"]), "*", False)
    with pytest.raises(LeptonError, match="sans effet"):
        parse_location(f"{repos['app']}@master")
    with pytest.raises(LeptonError, match="absent"):
        parse_location(str(tmp_path))


# --- GRA-4 ---------------------------------------------------------------------------------------
def test_gra4_add(project, repos, fake_build, capsys):
    assert main(["seed", "add", "my-app", str(repos["app"]), "--type", "application", "-C", str(project)]) == 0
    assert (project / "trunk/sys/root/src/bin/my-app/my-app.c").is_symlink()
    assert _graine(project)["applications"] == ["my-app"]
    assert validate_file(Rootstock(project).seed_manifest_path()) == []
    assert fake_build.read_text().split() == ["-S", str(project / "trunk"), "-B", str(project / "build/demo-debug")]
    assert "non commitée" in capsys.readouterr().out
    # bibliothèque en forme git (clonée)
    assert main(["seed", "add", "my-lib", url(repos["lib"]), "--type", "bibliotheque", "-C", str(project),
                 "--no-cmake"]) == 0
    assert (project / "depots/lepton/library-my-lib/master/.git").is_dir()
    assert _graine(project)["bibliotheques"] == ["my-lib"]
    assert_trunk_clean(project)


def test_gra4_add_wrong_type_is_undone(project, repos, capsys):
    before = (Rootstock(project).seed_dot() / ".scion.sources.list").read_text()
    assert main(["seed", "add", "my-app", str(repos["app"]), "--type", "bibliotheque", "-C", str(project),
                 "--no-cmake"]) == 1
    assert "de type « application », attendu « my-app » de type « bibliotheque »" in capsys.readouterr().err
    assert (Rootstock(project).seed_dot() / ".scion.sources.list").read_text() == before
    assert "my-app" not in _by_name(_status(project, capsys)[1])
    assert not (project / "trunk/sys/root/src/bin/my-app").exists()
    assert_trunk_clean(project)


def test_gra4_remove(project, repos, fake_build, capsys):
    assert main(["seed", "add", "my-app", str(repos["app"]), "--type", "application", "-C", str(project),
                 "--no-cmake"]) == 0
    assert main(["seed", "remove", "my-app", "-C", str(project)]) == 0
    assert not (project / "trunk/sys/root/src/bin/my-app").exists()
    assert _graine(project)["applications"] == []
    assert scion_key("application", "my-app") not in {s.key for s in Rootstock(project).sources()}
    assert (repos["app"] / "scion/sys/root/src/bin/my-app/my-app.c").is_file()     # dépôt intact
    assert fake_build.read_text().count("-S") == 1
    assert_trunk_clean(project)


def test_gra4_replace(project, repos, tmp_path, capsys):
    # BSP local → forme git du même dépôt avec un fichier en plus
    repo = repos["bsp"]
    (repo / "scion/sys/root/src/kernel/dev/bsp/board-q/extra.c").write_text("/* v2 */\n")
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", "v2"], check=True)
    subprocess.run(["git", "-C", str(repo), "branch", "v2"], check=True)
    assert main(["seed", "replace", "board-q", url(repo), "--version", "v2", "-C", str(project), "--no-cmake"]) == 0
    src = {s.key: s for s in Rootstock(project).sources()}[scion_key("bsp", "board-q")]
    assert (src.version, src.location) == ("v2", url(repo))
    assert (project / "trunk/sys/root/src/kernel/dev/bsp/board-q/extra.c").is_symlink()
    assert (project / "depots/lepton/bsp-board-q/v2/.git").is_dir()
    # retour en local
    assert main(["seed", "replace", "board-q", str(repo), "-C", str(project), "--no-cmake"]) == 0
    assert not (project / "depots/lepton/bsp-board-q").exists()          # clone purgé
    assert_trunk_clean(project)


def test_gra4_replace_wrong_scion_is_undone(project, repos, capsys):
    assert main(["seed", "replace", "board-q", str(repos["bsp2"]), "-C", str(project), "--no-cmake"]) == 1
    assert "restaurée" in capsys.readouterr().err
    src = {s.key: s for s in Rootstock(project).sources()}[scion_key("bsp", "board-q")]
    assert src.location == str(repos["bsp"])
    assert (project / "trunk/sys/root/src/kernel/dev/bsp/board-q/board.c").is_symlink()
    assert_trunk_clean(project)


def test_gra4_add_bsp_switches_seed_bsp(project, repos, capsys):
    assert main(["seed", "add", "board-c", str(repos["bsp2"]), "--type", "bsp", "-C", str(project),
                 "--no-cmake"]) == 0
    assert _graine(project)["bsp"] == "board-c"
    assert "reste greffé" in capsys.readouterr().err
    assert _by_name(_status(project, capsys)[1])["board-q"]["role"] == "non utilisé"
    assert main(["seed", "remove", "board-q", "-C", str(project), "--no-cmake"]) == 0
    assert_trunk_clean(project)


# --- GRA-6 ---------------------------------------------------------------------------------------
def test_gra6_status(project, repos, capsys):
    code, st = _status(project, capsys)
    assert code == 0 and st["missing"] == [] and st["trunk_check"] == {"regular_files": [], "broken_links": []}
    scions = _by_name(st)
    assert {n: s["role"] for n, s in scions.items() if n != "building"} == \
        {"lepton-noyau": "noyau", "fam-test": "famille", "board-q": "bsp"}
    assert scions["building"]["role"] == "sans manifeste" and scions["building"]["commit"] is None
    assert scions["board-q"]["branch"] == "master" and scions["board-q"]["dirty"] == 0
    assert scions["lepton-noyau"]["ahead"] == 0 and scions["lepton-noyau"]["behind"] == 0
    # modification locale non commitée (dans le clone) ; .DS_Store jamais signalé (Q8)
    (repos["bsp"] / "scion/sys/root/src/kernel/dev/bsp/board-q/board.c").write_text("/* modifié */\n")
    (repos["bsp"] / "scion/.DS_Store").write_text("")
    st = _status(project, capsys)[1]
    assert _by_name(st)["board-q"]["dirty"] == 1
    assert _by_name(st)["board-q"]["dirty_files"] == ["scion/sys/root/src/kernel/dev/bsp/board-q/board.c"]
    # texte, et fichier régulier dans le trunk → code 1
    (project / "trunk" / "stray.c").write_text("x")
    capsys.readouterr()
    assert main(["seed", "status", "-C", str(project)]) == 1
    out = capsys.readouterr().out
    assert "board-q" in out and "fichier régulier" in out


def test_gra6_status_from_clone_dir(project, monkeypatch, capsys):
    monkeypatch.chdir(project / "depots/lepton/original/master/scion")
    assert main(["seed", "status"]) == 0
    assert "lepton-noyau" in capsys.readouterr().out
