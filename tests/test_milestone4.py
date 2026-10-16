"""Jalon 4 d'ENV-8 : greffons — scion new, scion remove (GRF-1, GRF-4)."""

import json
import subprocess
from pathlib import Path

from conftest import assert_trunk_clean
from lepton import seed
from lepton.cli import main
from lepton.errors import LeptonError
from lepton.rootstock import Rootstock, scion_key
from lepton.validation import validate_file

BSP_DIR = "scion/sys/root/src/kernel/dev/bsp"


def _graine(root: Path) -> dict:
    return json.loads(Rootstock(root).seed_manifest_path().read_text())


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout


# --- GRF-1 ---------------------------------------------------------------------------------------
def test_grf1_scion_new_application(project, capsys):
    assert main(["scion", "new", "hello", "--type", "application", "-C", str(project), "--no-cmake"]) == 0
    repo = project / "depots/lepton-application/hello"
    manifest = repo / "scion/sys/root/src/bin/hello/lepton-greffon.json"
    assert validate_file(manifest) == []
    assert json.loads(manifest.read_text())["nom"] == "hello"
    source = (repo / "scion/sys/root/src/bin/hello/hello.c").read_text()
    assert "int hello_main(" in source
    # inclusions relatives à sys/root/src, comme les binaires du noyau (défaut N3 d'ENV-11)
    assert '#include "kernel/core/libstd.h"' in source and '#include "lib/libc/stdio/stdio.h"' in source
    assert _git(repo, "status", "--porcelain") == "" and _git(repo, "rev-parse", "--abbrev-ref", "HEAD").strip() == "master"
    assert (project / "trunk/sys/root/src/bin/hello/hello.c").is_symlink()
    assert _graine(project)["applications"] == ["hello"]
    src = {s.key: s for s in Rootstock(project).sources()}[scion_key("application", "hello")]
    assert (src.version, src.location) == ("*", "depots/lepton-application/hello")
    assert_trunk_clean(project)


def test_grf1_scion_new_bibliotheque(project):
    assert main(["scion", "new", "my-util", "--type", "bibliotheque", "-C", str(project), "--no-cmake"]) == 0
    lib = project / "trunk/sys/root/src/lib/my-util"
    assert (lib / "my-util.h").is_symlink() and "MY_UTIL_H" in (lib / "my-util.h").read_text()
    assert _graine(project)["bibliotheques"] == ["my-util"]
    assert_trunk_clean(project)


def test_grf1_scion_new_bsp_from(project, repos, capsys):
    # BSP source : en-tête suivi qui inclut par la destination ; fichier non suivi (exclu, S3-2)
    src = repos["bsp"] / BSP_DIR / "board-q"
    (src / "include").mkdir()
    (src / "include/config.h").write_text('#include "kernel/dev/bsp/board-q/board.h"\n'
                                          '/* kernel/dev/bsp/board-q-other inchangé */\n')
    (src / "board.h").write_text("#define BOARD_Q 1\n")
    (src / "blob.bin").write_bytes(b"\xff\xfe\x00kernel/dev/bsp/board-q")
    _git(repos["bsp"], "add", "-A")
    _git(repos["bsp"], "commit", "-q", "-m", "en-têtes")
    (src / "untracked.c").write_text("/* non suivi */\n")
    (src / ".DS_Store").write_bytes(b"\0")

    assert main(["scion", "new", "board-n", "--type", "bsp", "--from", "board-q", "-C", str(project),
                 "--no-cmake"]) == 0
    repo = project / "depots/lepton-bsp/board-n"
    new = repo / BSP_DIR / "board-n"
    assert sorted(str(p.relative_to(new)) for p in new.rglob("*") if p.is_file()) == \
        ["blob.bin", "board.c", "board.h", "include/config.h", "lepton-greffon.json"]
    assert (new / "include/config.h").read_text() == ('#include "kernel/dev/bsp/board-n/board.h"\n'
                                                      '/* kernel/dev/bsp/board-q-other inchangé */\n')
    assert (new / "blob.bin").read_bytes() == b"\xff\xfe\x00kernel/dev/bsp/board-q"
    manifest = json.loads((new / "lepton-greffon.json").read_text())
    assert validate_file(new / "lepton-greffon.json") == []
    old = json.loads((src / "lepton-greffon.json").read_text())
    assert (manifest["nom"], manifest["destination"], manifest["version"]) == \
        ("board-n", "kernel/dev/bsp/board-n", "0.1.0")
    for field in ("famille", "coeur", "mcu", "frequence_cpu", "script_liens", "demarrage", "qemu"):
        assert manifest[field] == old[field], field
    assert _git(repo, "status", "--porcelain") == ""
    assert _graine(project)["bsp"] == "board-n"
    assert "reste greffé" in capsys.readouterr().err
    assert (project / "trunk/sys/root/src/kernel/dev/bsp/board-n/include/config.h").is_symlink()
    assert_trunk_clean(project)


def test_grf1_scion_new_bsp_rewrites_manifest_paths(project, repos):
    src = repos["bsp"] / BSP_DIR / "board-q"
    data = json.loads((src / "lepton-greffon.json").read_text())
    data["compilation"] = {"publique": {"inclusions": ["kernel/dev/bsp/board-q/include"]}}
    (src / "lepton-greffon.json").write_text(json.dumps(data))
    assert main(["scion", "new", "board-n", "--type", "bsp", "--from", "board-q", "-C", str(project),
                 "--no-seed"]) == 0
    manifest = json.loads((project / "depots/lepton-bsp/board-n" / BSP_DIR / "board-n/lepton-greffon.json").read_text())
    assert manifest["compilation"] == {"publique": {"inclusions": ["kernel/dev/bsp/board-n/include"]}}


def test_grf1_scion_new_no_seed(project, capsys):
    before = (Rootstock(project).seed_dot() / ".scion.sources.list").read_text()
    assert main(["scion", "new", "hello", "--type", "application", "-C", str(project), "--no-seed",
                 "--destination", "bin/demos/hello"]) == 0
    assert (project / "depots/lepton-application/hello/scion/sys/root/src/bin/demos/hello/hello.c").is_file()
    assert "lepton seed add hello" in capsys.readouterr().out
    assert (Rootstock(project).seed_dot() / ".scion.sources.list").read_text() == before
    assert not (project / "trunk/sys/root/src/bin/demos").exists()


def test_grf1_scion_new_refusals(project, tmp_path, capsys):
    cases = [
        (["board-n", "--type", "bsp"], "--from BSP obligatoire"),
        (["board-n", "--type", "bsp", "--from", "unknown"], "aucun BSP greffé"),
        (["board-n", "--type", "bsp", "--from", "fam-test"], "aucun BSP greffé"),
        (["hello", "--type", "application", "--from", "board-q"], "réservé au type bsp"),
        (["board-q", "--type", "bsp", "--from", "board-q"], "déjà greffé"),
        (["Hello", "--type", "application"], "invalide"),
        (["hello", "--type", "application", "--destination", "../x"], "invalide"),
    ]
    busy = tmp_path / "busy"
    busy.mkdir()
    (busy / "f").write_text("x")
    cases.append((["hello", "--type", "application", "--repo", str(busy)], "n'est pas un répertoire vide"))
    for argv, message in cases:
        capsys.readouterr()
        assert main(["scion", "new", *argv, "-C", str(project), "--no-cmake"]) == 1, argv
        assert message in capsys.readouterr().err, argv
    assert not (project / "depots/lepton-bsp").exists() and not (project / "depots/lepton-application").exists()
    assert_trunk_clean(project)


def _fail(*_args, **_kwargs):
    raise LeptonError("échec simulé")


def test_o3_scion_new_undone_left_out_of_seed(project, monkeypatch, capsys):
    monkeypatch.setattr(seed, "_expect", _fail)          # échec après seed-clone, annulation complète
    assert main(["scion", "new", "hello", "--type", "application", "-C", str(project), "--no-cmake"]) == 1
    err = capsys.readouterr().err
    assert "hors graine (lepton seed add hello" in err and "annulation incomplète" not in err
    assert scion_key("application", "hello") not in {s.key for s in Rootstock(project).sources()}
    assert_trunk_clean(project)


def test_o3_scion_new_incomplete_undo_reports_state(project, monkeypatch, capsys):
    monkeypatch.setattr(seed, "_expect", _fail)
    monkeypatch.setattr(seed, "_undo_add", lambda *_a: None)   # annulation sans effet
    assert main(["scion", "new", "hello", "--type", "application", "-C", str(project), "--no-cmake"]) == 1
    err = capsys.readouterr().err
    key = scion_key("application", "hello")
    assert "hors graine" not in err
    assert "greffon déclaré dans .scion.sources.list, greffé (annulation incomplète : lepton seed remove hello" in err
    assert key in {s.key for s in Rootstock(project).sources()}
    # la reprise annoncée aboutit
    assert main(["seed", "remove", "hello", "-C", str(project), "--no-cmake"]) == 0
    assert key not in {s.key for s in Rootstock(project).sources()}
    assert_trunk_clean(project)


def test_o3_scion_new_failure_after_add(project, monkeypatch, capsys):
    monkeypatch.setattr(seed, "finish", _fail)           # ajout fait, échec au contrôle final
    assert main(["scion", "new", "hello", "--type", "application", "-C", str(project), "--no-cmake"]) == 1
    err = capsys.readouterr().err
    assert "greffon ajouté à la graine (corriger la cause, puis lepton graft)" in err and "hors graine" not in err
    assert _graine(project)["applications"] == ["hello"]


# --- GRF-4 ---------------------------------------------------------------------------------------
def test_grf4_remove(project):
    assert main(["scion", "new", "hello", "--type", "application", "-C", str(project), "--no-cmake"]) == 0
    repo = project / "depots/lepton-application/hello"
    head = _git(repo, "rev-parse", "HEAD")
    assert main(["scion", "remove", "hello", "-C", str(project), "--no-cmake"]) == 0
    assert not (project / "trunk/sys/root/src/bin/hello").exists()
    assert _graine(project)["applications"] == []
    assert scion_key("application", "hello") not in {s.key for s in Rootstock(project).sources()}
    assert _git(repo, "rev-parse", "HEAD") == head and _git(repo, "status", "--porcelain") == ""
    assert (repo / "scion/sys/root/src/bin/hello/hello.c").is_file()       # dépôt intact
    assert_trunk_clean(project)
    # noyau et BSP courant : refus (GRA-2)
    assert main(["scion", "remove", "board-q", "-C", str(project), "--no-cmake"]) == 1
