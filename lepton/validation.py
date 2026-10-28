"""Validation des manifestes : JSON Schema (greffon, graine) et XSD mklepton par xmllint (GRF-2)."""

import json
import re
import shutil
from dataclasses import asdict, dataclass
from functools import cache
from importlib import resources
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

from lepton import jsonpos, scion_runner
from lepton.errors import EXIT_TOOL, LeptonError

SCION_MANIFEST = "lepton-greffon.json"
SEED_MANIFEST = "lepton-graine.json"

# Type de manifeste → fichier de schéma
# Ligne d'anomalie de xmllint, préfixe du fichier retiré : « <ligne>: <message> »
_XMLLINT_LINE = re.compile(r"(\d+): (.*)")

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
    # Portée dans le fichier (ENV-12 lot 4, diagnostics de l'éditeur) : à partir de 1, fin exclue ;
    # None si inconnue (XML : ligne seule)
    line: int | None = None
    column: int | None = None
    end_line: int | None = None
    end_column: int | None = None

    def __str__(self) -> str:
        return f"{self.file}: {self.location}: {self.message}" if self.location else f"{self.file}: {self.message}"

    def as_dict(self) -> dict:
        return asdict(self)

    def place(self, text: str, span: "jsonpos.Span | None") -> "Anomaly":
        if span is not None:
            self.line, self.column = jsonpos.line_col(text, span.start)
            self.end_line, self.end_column = jsonpos.line_col(text, span.end)
        return self


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


def validate_data(data, kind: str, label: str, text: str | None = None) -> list[Anomaly]:
    """Valide un manifeste déjà chargé (`label` : nom affiché dans les anomalies) ; `text`, le texte
    dont il provient, situe chaque anomalie. Champs non autorisés : une anomalie par champ, située
    sur sa clé."""
    errors = sorted(_validator(kind).iter_errors(data), key=lambda e: list(e.absolute_path))
    try:
        found = jsonpos.members(text) if text is not None else None
    except (IndexError, ValueError):        # texte différent des données (fichier modifié entre-temps)
        found = None
    result = []
    for e in errors:
        pointer = _pointer(e)
        if e.validator == "additionalProperties" and isinstance(e.instance, dict):
            connus = set(e.schema.get("properties", {}))
            for k in sorted(k for k in e.instance if k not in connus):
                a = Anomaly(label, pointer, f"champ non autorisé : {k}")
                where = f"{pointer.rstrip('/')}/{k.replace('~', '~0').replace('/', '~1')}"
                result.append(a.place(text, jsonpos.span_of(found, where, on_key=True)) if found else a)
            continue
        a = Anomaly(label, pointer, _message(e))
        result.append(a.place(text, jsonpos.span_of(found, pointer)) if found else a)
    return result


def locate(anomalies: list[Anomaly], text: str) -> list[Anomaly]:
    """Situe dans `text` les anomalies à pointeur JSON pas encore situées (contrôles non
    exprimables en JSON Schema) ; texte non JSON : inchangées."""
    try:
        json.loads(text)
    except ValueError:
        return anomalies
    found = jsonpos.members(text)
    for a in anomalies:
        if a.line is None and a.location.startswith("/"):
            a.place(text, jsonpos.span_of(found, a.location))
    return anomalies


def validate_json(path: Path, kind: str, text: str | None = None) -> list[Anomaly]:
    """`text` : contenu à valider à la place du fichier (contenu non enregistré de l'éditeur)."""
    try:
        if text is None:
            text = path.read_text(encoding="utf-8")
        data = json.loads(text)
    except OSError as e:
        return [Anomaly(str(path), "", f"lecture impossible : {e.strerror}")]
    except json.JSONDecodeError as e:
        a = Anomaly(str(path), "", f"JSON mal formé : {e}", e.lineno, e.colno)
        a.end_line, a.end_column = e.lineno, e.colno + 1
        return [a]
    return validate_data(data, kind, str(path), text)


def validate_xml(path: Path, text: str | None = None) -> list[Anomaly]:
    """XSD mklepton par xmllint (`text` : contenu à valider à la place du fichier, sur l'entrée
    standard) ; xmllint absent : LeptonError (code 2), signalée par l'appelant. Ligne de chaque
    anomalie lue dans la sortie de xmllint (« <fichier>:<ligne>: … »), colonne inconnue."""
    exe = shutil.which("xmllint")
    if exe is None:
        raise LeptonError("xmllint absent : XML mklepton non validé",
                          "installer libxml2 (MacPorts : port install libxml2 ; Debian : apt install libxml2-utils)",
                          EXIT_TOOL)
    if text is None and not path.is_file():
        return [Anomaly(str(path), "", "fichier introuvable")]
    source = "-" if text is not None else str(path)
    # par scion_runner.run : commande affichée sous -v
    res = scion_runner.run(["xmllint", "--noout", "--schema", str(schemas_dir() / SCHEMA_FILES["mklepton"]), source],
                           check=False, input=text)
    if res.returncode == 0:
        return []
    found = []
    for l in res.stderr.splitlines():
        m = _XMLLINT_LINE.match(l.removeprefix(source + ":")) if l.startswith(source + ":") else None
        if m:
            found.append(Anomaly(str(path), "", f"{m[1]}: {m[2].strip()}", int(m[1])))
    if not found:       # sortie d'une autre forme : lignes telles quelles, sans position
        found = [Anomaly(str(path), "", l.strip()) for l in res.stderr.splitlines()
                 if l.strip() and not l.endswith("fails to validate")]
    return found or [Anomaly(str(path), "", "refusé par le XSD mklepton")]


def validate_file(path: Path, text: str | None = None) -> list[Anomaly]:
    """`text` : contenu non enregistré de `path` (`lepton check --stdin`) ; type par le nom seul."""
    if text is None and not path.exists():
        return [Anomaly(str(path), "", "fichier introuvable")]
    kind = kind_of(path)
    return validate_xml(path, text) if kind == "mklepton" else validate_json(path, kind, text)
