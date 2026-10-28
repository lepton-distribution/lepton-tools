"""ENV-12 lot 4 (F5, CFG-7) : anomalies situées (ligne, colonne) pour les diagnostics de l'éditeur,
`lepton check --stdin FILE` (contenu non enregistré) ; espace généré : test_generate."""

import io
import json
import shutil
from pathlib import Path

import pytest

from lepton import jsonpos
from lepton.cli import main
from test_milestone6 import XML, _check, _edit_json, _graine_path, _manifest_path, repos  # noqa: F401

REPO = Path(__file__).resolve().parent.parent
EXAMPLES = REPO / "schemas" / "exemples"
needs_xmllint = pytest.mark.skipif(shutil.which("xmllint") is None, reason="xmllint absent")


def _stdin(monkeypatch, text: str) -> None:
    monkeypatch.setattr("sys.stdin", io.StringIO(text))


def _anomalies(capsys) -> list[dict]:
    return json.loads(capsys.readouterr().out)["anomalies"]


def _at(a: dict) -> tuple:
    return a["line"], a["column"], a["end_line"], a["end_column"]


# --- positions -----------------------------------------------------------------------------------
def test_jsonpos_members():
    text = '{\n  "a": {"b": [1, "x\\"y"]},\n  "c/d": true\n}'
    found = jsonpos.members(text)
    assert set(found) == {"", "/a", "/a/b", "/a/b/0", "/a/b/1", "/c~1d"}
    assert text[found["/a/b/1"].value.start:found["/a/b/1"].value.end] == '"x\\"y"'
    assert text[found["/c~1d"].key.start:found["/c~1d"].key.end] == '"c/d"'
    # objet ou liste : clé (crochet ouvrant à défaut) ; pointeur absent : plus proche ancêtre
    assert jsonpos.span_of(found, "/a") == found["/a"].key
    assert jsonpos.span_of(found, "/a/b/7") == found["/a/b"].key
    assert jsonpos.span_of(found, "/") == jsonpos.Span(0, 1)
    assert jsonpos.line_col(text, found["/c~1d"].value.start) == (3, 10)


def test_stdin_schema_positions(monkeypatch, capsys):
    """Contenu non enregistré : champ absent sur l'objet, champ non autorisé sur sa clé (un par champ),
    valeur fautive sur la valeur ; le fichier sur disque n'est pas lu."""
    data = json.loads((EXAMPLES / "graine.json").read_text(encoding="utf-8"))
    del data["noyau"]
    data["projet"]["inconnu"] = 1
    data["zz"] = 2
    data["backend"] = "autre"
    text = json.dumps(data, ensure_ascii=False, indent=2)
    _stdin(monkeypatch, text)
    assert main(["check", "--json", "--stdin", "absent/lepton-graine.json"]) == 1
    by_msg = {a["message"]: a for a in _anomalies(capsys)}
    lines = text.splitlines()
    assert _at(by_msg["champ obligatoire absent : noyau"]) == (1, 1, 1, 2)
    a = by_msg["champ non autorisé : inconnu"]
    assert a["location"] == "/projet" and lines[a["line"] - 1][a["column"] - 1:a["end_column"] - 1] == '"inconnu"'
    a = by_msg["champ non autorisé : zz"]
    assert lines[a["line"] - 1][a["column"] - 1:a["end_column"] - 1] == '"zz"'
    a = next(a for m, a in by_msg.items() if m.startswith('valeur "autre"'))
    assert a["location"] == "/backend" and lines[a["line"] - 1][a["column"] - 1:a["end_column"] - 1] == '"autre"'


def test_stdin_malformed_json(monkeypatch, capsys):
    _stdin(monkeypatch, '{\n  "nom": ,\n}')
    assert main(["check", "--json", "--stdin", "lepton-greffon.json"]) == 1
    [a] = _anomalies(capsys)
    assert a["message"].startswith("JSON mal formé") and _at(a) == (2, 10, 2, 11)


def test_stdin_valid_and_text_output(monkeypatch, capsys):
    _stdin(monkeypatch, (EXAMPLES / "graine.json").read_text(encoding="utf-8"))
    assert main(["check", "--stdin", "lepton-graine.json"]) == 0
    assert "1 fichier(s) conforme(s)." in capsys.readouterr().out


@pytest.mark.parametrize("argv", [["check", "--stdin"], ["check", "--stdin", "a.json", "b.json"]])
def test_stdin_one_file(argv, monkeypatch, capsys):
    _stdin(monkeypatch, "{}")
    assert main(argv) == 1
    assert "--stdin : un seul FILE" in capsys.readouterr().err


@needs_xmllint
def test_stdin_xml_line(monkeypatch, capsys):
    text = (EXAMPLES / "mklepton.xml").read_text(encoding="utf-8")
    lines = text.splitlines()
    i = next(n for n, l in enumerate(lines) if "<kernel" in l)
    lines.insert(i, "<inconnu/>")
    _stdin(monkeypatch, "\n".join(lines) + "\n")
    assert main(["check", "--json", "--stdin", "etc/mkconf_x.xml"]) == 1
    [a] = _anomalies(capsys)
    assert a["file"] == "etc/mkconf_x.xml" and a["line"] == i + 1 and a["column"] is None
    assert a["message"].startswith(f"{i + 1}: ") and "inconnu" in a["message"]


@needs_xmllint
def test_xml_file_line_and_text_unchanged(tmp_path, capsys):
    """Fichier sur disque : message inchangé (« <ligne>: … », filtre de la tâche) et ligne relevée."""
    f = tmp_path / "mkconf_x.xml"
    f.write_text('<?xml version="1.0"?>\n<mklepton version="2">\n<inconnu/>\n</mklepton>\n')
    assert main(["check", "--json", str(f)]) == 1
    anomalies = _anomalies(capsys)
    assert anomalies and all(a["line"] == 3 and a["message"].startswith("3: ") for a in anomalies)


# --- contrôles du rootstock situés ---------------------------------------------------------------
def test_rootstock_anomalies_located(project, capsys):
    graine = _graine_path(project)
    _edit_json(graine, bsp="board-absent")
    code, out = _check(project, capsys, "--json")
    assert code == 1
    [a] = [a for a in json.loads(out)["anomalies"] if "board-absent" in a["message"]]
    line = graine.read_text().splitlines()[a["line"] - 1]
    assert a["location"] == "/bsp" and line[a["column"] - 1:a["end_column"] - 1] == '"board-absent"'

    m = _manifest_path(project, "fam-test")
    _edit_json(m, dependances=["absent"], inconnu=1)
    _edit_json(graine, bsp="board-q")
    code, out = _check(project, capsys, "--json")
    found = {a["message"]: a for a in json.loads(out)["anomalies"]}
    lines = m.read_text().splitlines()
    for message, token in (("dépendance « absent » non greffée (GRF-5)", '"absent"'),
                           ("champ non autorisé : inconnu", '"inconnu"')):
        a = found[message]
        assert lines[a["line"] - 1][a["column"] - 1:a["end_column"] - 1] == token


def test_rootstock_xml_cfg5_line(project, capsys):
    from conftest import PROJECT_XML
    xml = (project / "trunk" / PROJECT_XML).resolve()
    xml.write_text(XML.format(extra_dev='<dev name="dev_ghost_map" use="on"/>', extra_bin=""))
    code, out = _check(project, capsys, "--json")
    [a] = [a for a in json.loads(out)["anomalies"] if "dev_ghost_map" in a["location"]]
    assert "dev_ghost_map" in xml.read_text().splitlines()[a["line"] - 1]


@needs_xmllint
def test_rootstock_xml_xsd_line(project, capsys):
    """D-a (ENV-12 lot 6 S3) : refus du XSD au contrôle complet situé à la ligne de xmllint."""
    from conftest import PROJECT_XML
    xml = (project / "trunk" / PROJECT_XML).resolve()
    lines = xml.read_text().splitlines()
    i = next(n for n, l in enumerate(lines) if "<mklepton" in l) + 1
    lines.insert(i, "<inconnu/>")
    xml.write_text("\n".join(lines) + "\n")
    code, out = _check(project, capsys, "--json")
    assert code == 1
    [a] = [a for a in json.loads(out)["anomalies"] if "inconnu" in a["message"]]
    assert a["line"] == i + 1 and a["message"].startswith(f"{i + 1}: ")



# --- D-b (ENV-12 R1) : discriminant « type » absent, champ interdit pour le type ---------------------
def test_scion_without_type_single_anomaly(monkeypatch, capsys):
    data = json.loads((EXAMPLES / "greffon-application.json").read_text(encoding="utf-8"))
    del data["type"]
    _stdin(monkeypatch, json.dumps(data, ensure_ascii=False, indent=2))
    assert main(["check", "--json", "--stdin", "lepton-greffon.json"]) == 1
    assert [a["message"] for a in _anomalies(capsys)] == ["champ obligatoire absent : type"]


def test_scion_field_forbidden_for_type(monkeypatch, capsys):
    """Schéma false : une anomalie par champ (même valeur pour deux champs), située sur sa clé,
    message en français ; idem par une référence locale (sans_champ_materiel)."""
    data = json.loads((EXAMPLES / "greffon-noyau.json").read_text(encoding="utf-8"))
    data["bibliotheque"] = data["mcu"] = "lib"
    text = json.dumps(data, ensure_ascii=False, indent=2)
    _stdin(monkeypatch, text)
    assert main(["check", "--json", "--stdin", "lepton-greffon.json"]) == 1
    found = _anomalies(capsys)
    lines = text.splitlines()
    assert [a["message"] for a in found] == [f"champ non autorisé pour le type « noyau » : {k}" for k in ("bibliotheque", "mcu")]
    for a, k in zip(found, ("bibliotheque", "mcu")):
        assert a["location"] == f"/{k}" and lines[a["line"] - 1][a["column"] - 1:a["end_column"] - 1] == f'"{k}"'
    data = json.loads((EXAMPLES / "greffon-application.json").read_text(encoding="utf-8"))
    data["coeur"] = "cortex-m4f"
    _stdin(monkeypatch, json.dumps(data, ensure_ascii=False, indent=2))
    assert main(["check", "--json", "--stdin", "lepton-greffon.json"]) == 1
    assert [a["message"] for a in _anomalies(capsys)] == ["champ non autorisé pour le type « application » : coeur"]


def test_invalid_examples_messages_translated(capsys):
    """Aucun message anglais de jsonschema pour les schémas false, anyOf et oneOf."""
    for p in sorted((EXAMPLES / "invalides").glob("*.json")):
        main(["check", "--json", str(p)])
        for a in _anomalies(capsys):
            assert "False schema" not in a["message"] and "is not valid under" not in a["message"], (p.name, a)
    p = EXAMPLES / "invalides" / "bsp-sans-openocd-ni-qemu.json"
    main(["check", "--json", str(p)])
    assert [a["message"] for a in _anomalies(capsys)] == ["champ obligatoire absent : openocd et sonde, ou qemu"]


# --- O-r1 (ENV-12 R1) : mots-clés des schémas tous traduits -------------------------------------
# Mots-clés qui produisent une anomalie, traduits par validation._message ou traités par
# validate_data ; un mot-clé nouveau dans un schéma fait échouer test_schema_keywords_translated.
TRANSLATED = {"required", "additionalProperties", "enum", "const", "type", "pattern", "minLength", "minItems",
              "uniqueItems", "anyOf", "oneOf", "minProperties", "minimum"}
# Applicateurs et annotations : pas d'anomalie propre (celles de leurs sous-schémas sont traduites)
STRUCTURE = {"properties", "items", "allOf", "if", "then", "$ref", "propertyNames", "$schema", "$id", "$comment",
             "title", "description", "$defs"}


def _keywords(node, found: set, under_names: bool = False) -> None:
    if isinstance(node, dict):
        for k, v in node.items():
            if not under_names:
                found.add(k)
            _keywords(v, found, under_names=not under_names and k in ("properties", "$defs"))
    elif isinstance(node, list):
        for v in node:
            _keywords(v, found)


def test_schema_keywords_translated():
    found = set()
    for name in ("greffon", "graine"):
        _keywords(json.loads((REPO / "schemas" / f"{name}.schema.json").read_text(encoding="utf-8")), found)
    assert found - TRANSLATED - STRUCTURE == set()


def test_messages_minproperties_minimum_type(capsys):
    from lepton.validation import validate_data
    data = json.loads((EXAMPLES / "greffon-bsp-nucleo-f429zi.json").read_text(encoding="utf-8"))
    data["frequence_cpu"] = 0
    assert [a.message for a in validate_data(data, "scion", "m")] == ["valeur 0 inférieure au minimum 1"]
    data["frequence_cpu"] = "180 MHz"
    assert [a.message for a in validate_data(data, "scion", "m")] == ["type attendu : entier"]
    p = EXAMPLES / "invalides" / "graine-option-greffon-vide.json"
    main(["check", "--json", str(p)])
    assert [a["message"] for a in _anomalies(capsys)] == ["objet vide (au moins 1 champ(s))"]
    p = EXAMPLES / "invalides" / "graine-option-valeur-objet.json"
    main(["check", "--json", str(p)])
    assert [a["message"] for a in _anomalies(capsys)] == ["type attendu : booléen, entier ou texte"]


def test_property_name_located_on_key(monkeypatch, capsys):
    """propertyNames : nom de champ refusé nommé comme tel, situé sur sa clé (pas sur l'objet)."""
    data = json.loads((EXAMPLES / "graine.json").read_text(encoding="utf-8"))
    data["options"] = {"mesure": {"MESURE_PERIODE_MS": 100, "periode_ms": 1}, "Mesure": {"A": 1}}
    text = json.dumps(data, ensure_ascii=False, indent=2)
    _stdin(monkeypatch, text)
    assert main(["check", "--json", "--stdin", "lepton-graine.json"]) == 1
    found = {a["location"]: a for a in _anomalies(capsys)}
    lines = text.splitlines()
    for where, key, motif in (("/options/Mesure", "Mesure", "^[a-z0-9][a-z0-9._-]*$"),
                              ("/options/mesure/periode_ms", "periode_ms", "^[A-Z][A-Z0-9_]*$")):
        a = found[where]
        assert a["message"] == f'nom de champ "{key}" non conforme au motif {motif}'
        assert lines[a["line"] - 1][a["column"] - 1:a["end_column"] - 1] == f'"{key}"'
