"""Validation des manifestes : JSON Schema (greffon, graine) et XSD mklepton par xmllint (GRF-2)."""

import json
import shutil
import subprocess
from dataclasses import asdict, dataclass
from functools import cache
from importlib import resources
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

from lepton.errors import EXIT_TOOL, LeptonError

SCION_MANIFEST = "lepton-greffon.json"
SEED_MANIFEST = "lepton-graine.json"

# Type de manifeste → fichier de schéma
SCHEMA_FILES = {
    "scion": "greffon.schema.json",
    "seed": "graine.schema.json",
    "mklepton": "mklepton.xsd",
}


@dataclass
class Anomaly:
    file: str
    location: str
    message: str

    def __str__(self) -> str:
        return f"{self.file}: {self.location}: {self.message}" if self.location else f"{self.file}: {self.message}"

    def as_dict(self) -> dict:
        return asdict(self)


def schemas_dir() -> Path:
    """Schémas installés dans le paquet, sinon schemas/ du dépôt (installation éditable)."""
    installed = resources.files("lepton") / "schemas"
    if installed.is_dir():
        return Path(str(installed))
    repo = Path(__file__).resolve().parent.parent / "schemas"
    if repo.is_dir():
        return repo
    raise LeptonError("schémas introuvables (ni dans le paquet lepton, ni dans schemas/ du dépôt)",
                      "réinstaller lepton : pipx install --force <LEPTON_TOOLS>", EXIT_TOOL)


def kind_of(path: Path) -> str:
    """Type d'un manifeste : par l'extension, le nom, puis le champ $schema."""
    if path.suffix == ".xml":
        return "mklepton"
    if path.name == SCION_MANIFEST:
        return "scion"
    if path.name == SEED_MANIFEST:
        return "seed"
    ref = ""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict) and isinstance(data.get("$schema"), str):
            ref = data["$schema"]
    except (OSError, ValueError):
        pass
    for kind in ("scion", "seed"):
        if ref.endswith(SCHEMA_FILES[kind]):
            return kind
    raise LeptonError(f"{path} : type de manifeste indéterminé",
                      f"nommer le fichier {SCION_MANIFEST} ou {SEED_MANIFEST}, "
                      f"ou renseigner « $schema » ({SCHEMA_FILES['scion']} ou {SCHEMA_FILES['seed']})")


@cache
def _validator(kind: str) -> Draft202012Validator:
    schema = json.loads((schemas_dir() / SCHEMA_FILES[kind]).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def _pointer(err: ValidationError) -> str:
    return "/" + "/".join(str(p) for p in err.absolute_path)


def _message(err: ValidationError) -> str:
    """Message en français pour les mots-clés courants ; message de jsonschema sinon."""
    v, val, inst = err.validator, err.validator_value, err.instance
    if v == "required":
        manquants = [p for p in val if isinstance(inst, dict) and p not in inst]
        return "champ obligatoire absent : " + ", ".join(manquants)
    if v == "additionalProperties" and isinstance(inst, dict):
        connus = set(err.schema.get("properties", {}))
        return "champ non autorisé : " + ", ".join(sorted(k for k in inst if k not in connus))
    if v == "enum":
        return f"valeur {json.dumps(inst, ensure_ascii=False)} hors de la liste {json.dumps(val, ensure_ascii=False)}"
    if v == "const":
        return f"valeur {json.dumps(inst, ensure_ascii=False)} différente de {json.dumps(val, ensure_ascii=False)}"
    if v == "type":
        return f"type attendu : {val}"
    if v == "pattern":
        return f"valeur {json.dumps(inst, ensure_ascii=False)} non conforme au motif {val}"
    if v == "minLength":
        return f"texte trop court (au moins {val} caractère(s))"
    if v == "minItems":
        return f"liste trop courte (au moins {val} élément(s))"
    if v == "uniqueItems":
        return "éléments en double"
    return err.message


def validate_json(path: Path, kind: str) -> list[Anomaly]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as e:
        return [Anomaly(str(path), "", f"lecture impossible : {e.strerror}")]
    except ValueError as e:
        return [Anomaly(str(path), "", f"JSON mal formé : {e}")]
    errors = sorted(_validator(kind).iter_errors(data), key=lambda e: list(e.absolute_path))
    return [Anomaly(str(path), _pointer(e), _message(e)) for e in errors]


def validate_xml(path: Path) -> list[Anomaly]:
    """XSD mklepton par xmllint ; xmllint absent : LeptonError (code 2), signalée par l'appelant."""
    exe = shutil.which("xmllint")
    if exe is None:
        raise LeptonError("xmllint absent : XML mklepton non validé",
                          "installer libxml2 (MacPorts : port install libxml2 ; Debian : apt install libxml2-utils)",
                          EXIT_TOOL)
    if not path.is_file():
        return [Anomaly(str(path), "", "fichier introuvable")]
    res = subprocess.run([exe, "--noout", "--schema", str(schemas_dir() / SCHEMA_FILES["mklepton"]), str(path)],
                         capture_output=True, text=True, check=False)
    if res.returncode == 0:
        return []
    lignes = [l for l in res.stderr.splitlines() if l.strip() and not l.endswith("fails to validate")]
    return [Anomaly(str(path), "", l.removeprefix(str(path) + ":").strip()) for l in lignes] or \
        [Anomaly(str(path), "", "refusé par le XSD mklepton")]


def validate_file(path: Path) -> list[Anomaly]:
    if not path.exists():
        return [Anomaly(str(path), "", "fichier introuvable")]
    kind = kind_of(path)
    return validate_xml(path) if kind == "mklepton" else validate_json(path, kind)
