"""Jalon 2 d'ENV-8 : modèles de graine et de greffons conformes aux schémas (GRF-1, GRF-2)."""

import json
from pathlib import Path

import pytest

from lepton.errors import LeptonError
from lepton.templates import KINDS, render_text, render_tree, template_files, templates_dir, tokens
from lepton.validation import validate_file

REPO = Path(__file__).resolve().parent.parent

SEED_VALUES = {
    "name": "demo", "version": "0.1.0", "description": "Projet d'essai.",
    "kernel": "lepton-noyau", "bsp": "qemu-mps2-an386", "backend": "embos",
    "configurations": [{"nom": "debug-qemu", "construction": "Debug", "execution": "qemu"}],
    "mkconf": "sys/user/tauon-basic/etc/mkconf_tauon_basic_qemu_mps2.xml",
}

SCION_VALUES = {
    "name": "my-app", "c_name": "my_app", "c_guard": "MY_APP_H", "kernel": "lepton-noyau",
    "description": "Greffon d'essai.",
}

# BSP : champs matériels repris d'un BSP existant (jalon 4, --from) ; ici ceux de l'exemple an386
BSP_QEMU = {
    "name": "my-board", "version": "0.1.0", "description": "Carte d'essai.",
    "destination": "kernel/dev/bsp/my-board", "family": "qemu-mps2", "core": "cortex-m4f",
    "float_abi": None, "mcu": "ARMCM4", "cpu_frequency": 25000000,
    "kernel_config_header": "include/user_kernel_mkconf.h", "link_script": "ld/mem_my-board.ld",
    "startup": ["qemu_mps2_board.c"], "sources": None, "dependencies": None,
    "openocd": None, "probe": None, "svd": None, "qemu": {"machine": "mps2-an386"},
    "compilation": None, "options": None,
}
BSP_BOARD = dict(BSP_QEMU, qemu=None, openocd=["openocd/my-board.cfg"], probe="stlink", float_abi="soft")


@pytest.mark.parametrize("kind", KINDS)
def test_template_present(kind):
    assert template_files(kind), f"modèle {kind} vide"


def test_seed_template_valid(tmp_path):
    written = render_tree("seed", tmp_path, SEED_VALUES)
    dot = tmp_path / "scion" / ".scion"
    assert dot / "lepton-graine.json" in written
    assert validate_file(dot / "lepton-graine.json") == []
    for name in (".scion.sources.list", ".scion.ramifications"):
        text = (dot / name).read_text()
        assert "{{" not in text and "building" in text


@pytest.mark.parametrize("kind,typ,dest", [("application", "application", "bin/my-app"),
                                           ("library", "bibliotheque", "lib/my-app")])
def test_grf1_scion_template_valid(tmp_path, kind, typ, dest):
    written = render_tree(kind, tmp_path, dict(SCION_VALUES, destination=dest))
    manifest = tmp_path / "lepton-greffon.json"
    assert validate_file(manifest) == []
    data = json.loads(manifest.read_text())
    assert (data["nom"], data["type"], data["destination"]) == ("my-app", typ, dest)
    assert tmp_path / "my-app.c" in written
    for path in written:
        assert "{{" not in path.read_text(), path
    assert "int my_app_" in (tmp_path / "my-app.c").read_text()


@pytest.mark.parametrize("values", [BSP_QEMU, BSP_BOARD], ids=["qemu", "board"])
def test_grf1_bsp_template_valid(tmp_path, values):
    render_tree("bsp", tmp_path, values)
    manifest = tmp_path / "lepton-greffon.json"
    assert validate_file(manifest) == []
    data = json.loads(manifest.read_text())
    assert not [k for k, v in data.items() if v is None]
    assert ("qemu" in data) == (values["qemu"] is not None)


def test_bsp_template_covers_schema_fields():
    """Le squelette BSP porte tous les champs que le schéma autorise pour un BSP."""
    schema = json.loads((REPO / "schemas" / "greffon.schema.json").read_text())
    bsp = next(r["then"] for r in schema["allOf"] if r["if"]["properties"]["type"]["const"] == "bsp")
    allowed = {k for k in schema["properties"] if k != "$schema"} - \
        {k for k, v in bsp["properties"].items() if v is False}
    data = json.loads(render_text((templates_dir() / "bsp" / "lepton-greffon.json").read_text(),
                                  {t: "x" for t in tokens((templates_dir() / "bsp" / "lepton-greffon.json").read_text())},
                                  json_file=True))
    assert set(data) == allowed


def test_missing_token_refused(tmp_path):
    with pytest.raises(LeptonError, match="jeton"):
        render_tree("application", tmp_path, {"name": "x"})


def test_existing_file_not_overwritten(tmp_path):
    (tmp_path / "lepton-greffon.json").write_text("{}")
    with pytest.raises(LeptonError, match="existe déjà"):
        render_tree("application", tmp_path, dict(SCION_VALUES, destination="bin/my-app"))
    assert (tmp_path / "lepton-greffon.json").read_text() == "{}"

