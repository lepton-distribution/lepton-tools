"""Jalon 1 d'ENV-8 : version (INS-6), validation des manifestes (GRF-2), codes de retour."""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from lepton import __version__
from lepton.cli import main
from lepton.validation import SCHEMA_FILES, schemas_dir

REPO = Path(__file__).resolve().parent.parent
EXAMPLES = REPO / "schemas" / "exemples"
VALID = sorted(EXAMPLES.glob("*.json")) + sorted(EXAMPLES.glob("*.xml"))
INVALID = sorted((EXAMPLES / "invalides").glob("*.json")) + sorted((EXAMPLES / "invalides").glob("*.xml"))
needs_xmllint = pytest.mark.skipif(shutil.which("xmllint") is None, reason="xmllint absent")


def _marks(path):
    return [needs_xmllint] if path.suffix == ".xml" else []


def test_ins6_version(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    out = capsys.readouterr().out.splitlines()
    assert out[0] == f"lepton {__version__}"
    assert out[1].startswith("scion ")


def test_ins6_version_without_scion(capsys, monkeypatch):
    monkeypatch.setenv("PATH", "")
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert "scion absent" in capsys.readouterr().out


def test_ins6_module_entry_point():
    res = subprocess.run([sys.executable, "-m", "lepton", "--version"], capture_output=True, text=True)
    assert res.returncode == 0 and res.stdout.startswith(f"lepton {__version__}\n")


def test_packaged_schemas_match_repo():
    for name in SCHEMA_FILES.values():
        assert (schemas_dir() / name).read_bytes() == (REPO / "schemas" / name).read_bytes()


@pytest.mark.parametrize("path", [pytest.param(p, id=p.name, marks=_marks(p)) for p in VALID])
def test_grf2_valid_example(path, capsys):
    assert main(["check", str(path)]) == 0, capsys.readouterr().out


@pytest.mark.parametrize("path", [pytest.param(p, id=p.name, marks=_marks(p)) for p in INVALID])
def test_grf2_invalid_example(path, capsys):
    assert main(["check", str(path)]) == 1
    assert capsys.readouterr().out.startswith(str(path))


def test_grf2_kind_from_manifest_name(tmp_path):
    data = json.loads((EXAMPLES / "greffon-noyau.json").read_text(encoding="utf-8"))
    del data["$schema"]
    f = tmp_path / "lepton-greffon.json"
    f.write_text(json.dumps(data), encoding="utf-8")
    assert main(["check", str(f)]) == 0
    del data["nom"]
    f.write_text(json.dumps(data), encoding="utf-8")
    assert main(["check", str(f)]) == 1


def test_grf2_french_messages(tmp_path, capsys):
    f = tmp_path / "lepton-graine.json"
    data = json.loads((EXAMPLES / "graine.json").read_text(encoding="utf-8"))
    del data["noyau"]
    data["inconnu"] = 1
    f.write_text(json.dumps(data), encoding="utf-8")
    assert main(["check", str(f)]) == 1
    out = capsys.readouterr().out
    assert "champ obligatoire absent : noyau" in out
    assert "champ non autorisé : inconnu" in out


def test_grf2_json_output(tmp_path, capsys):
    bad = tmp_path / "lepton-graine.json"
    bad.write_text("{}", encoding="utf-8")
    good = EXAMPLES / "graine.json"
    assert main(["check", "--json", str(good), str(bad)]) == 1
    out = json.loads(capsys.readouterr().out)
    assert out["files"] == [str(good), str(bad)]
    assert {a["file"] for a in out["anomalies"]} == {str(bad)}
    assert set(out["anomalies"][0]) == {"file", "location", "message", "line", "column", "end_line", "end_column"}


def test_check_malformed_json(tmp_path, capsys):
    f = tmp_path / "lepton-greffon.json"
    f.write_text("{", encoding="utf-8")
    assert main(["check", str(f)]) == 1
    assert "JSON mal formé" in capsys.readouterr().out


def test_check_unknown_kind(tmp_path, capsys):
    f = tmp_path / "x.json"
    f.write_text("{}", encoding="utf-8")
    assert main(["check", str(f)]) == 1
    err = capsys.readouterr().err
    assert "type de manifeste indéterminé" in err and "→" in err


def test_check_missing_file(tmp_path, capsys):
    assert main(["check", str(tmp_path / "lepton-greffon.json")]) == 1
    assert "fichier introuvable" in capsys.readouterr().out


def test_check_without_xmllint(capsys, monkeypatch):
    monkeypatch.setenv("PATH", "")
    assert main(["check", str(EXAMPLES / "mklepton.xml")]) == 0
    assert "xmllint absent" in capsys.readouterr().err


@needs_xmllint
def test_check_verbose_shows_xmllint(capsys):
    """-v : l'appel à xmllint est affiché comme les autres commandes externes (rapport Debian R5, C)."""
    assert main(["check", "-v", str(EXAMPLES / "mklepton.xml")]) == 0
    err = capsys.readouterr().err
    assert "lepton: exécute : xmllint --noout --schema" in err and "mklepton.xml" in err
    assert main(["check", str(EXAMPLES / "mklepton.xml")]) == 0
    assert "exécute" not in capsys.readouterr().err


@pytest.mark.parametrize("argv", [["check"], ["inconnue"], ["check", "--option-inconnue", "x"], []])
def test_usage_error_exit_1(argv, capsys):
    try:
        code = main(argv)
    except SystemExit as exc:
        code = exc.code
    assert code == 1
    assert capsys.readouterr().err
