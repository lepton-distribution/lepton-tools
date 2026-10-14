"""Modèles de graine et de greffons (jalon 2 d'ENV-8) : lepton/templates/<kind>/.

Jetons `{{token}}` dans le contenu et dans les noms de fichiers. Règles de rendu :
- fichier `.json` : chaque jeton est remplacé par sa valeur encodée en JSON (le modèle n'écrit
  donc pas de guillemets autour du jeton) ; une clé dont la valeur rendue est `null` est omise
  (champs facultatifs, ex. `qemu` ou `openocd` d'un BSP) ;
- autre fichier et nom de fichier : valeur insérée telle quelle (texte).
Un jeton sans valeur est une erreur : aucun modèle ne laisse de jeton dans le fichier produit.
"""

import json
import re
from importlib import resources
from pathlib import Path

from lepton.errors import EXIT_TOOL, LeptonError

KINDS = ("seed", "bsp", "application", "library")

# Type de greffon (enum des schémas) → modèle et répertoire de dépôt créés par lepton (PA-9 Q10)
SCION_KIND = {"bsp": "bsp", "application": "application", "bibliotheque": "library"}

_TOKEN = re.compile(r"\{\{([a-z_]+)\}\}")


def templates_dir() -> Path:
    path = Path(str(resources.files("lepton") / "templates"))
    if not path.is_dir():
        raise LeptonError("modèles introuvables dans le paquet lepton",
                          "réinstaller lepton : pipx install --force <LEPTON_TOOLS>", EXIT_TOOL)
    return path


def c_identifier(name: str) -> str:
    """Nom de greffon → identifiant C (point d'entrée `<id>_main`, garde d'en-tête)."""
    ident = re.sub(r"[^A-Za-z0-9_]", "_", name)
    return ident if not ident[:1].isdigit() else "_" + ident


def tokens(text: str) -> set[str]:
    return set(_TOKEN.findall(text))


def _substitute(text: str, values: dict, encode, where: str) -> str:
    missing = sorted(tokens(text) - set(values))
    if missing:
        raise LeptonError(f"modèle {where} : jeton(s) sans valeur : {', '.join(missing)}",
                          "signaler l'anomalie (modèle et appelant de lepton incohérents)", EXIT_TOOL)
    return _TOKEN.sub(lambda m: encode(values[m.group(1)]), text)


def _drop_nulls(data):
    if isinstance(data, dict):
        return {k: _drop_nulls(v) for k, v in data.items() if v is not None}
    if isinstance(data, list):
        return [_drop_nulls(v) for v in data]
    return data


def render_text(text: str, values: dict, json_file: bool, where: str = "") -> str:
    if not json_file:
        return _substitute(text, values, str, where)
    rendered = _substitute(text, values, lambda v: json.dumps(v, ensure_ascii=False), where)
    try:
        data = json.loads(rendered)
    except ValueError as e:
        raise LeptonError(f"modèle {where} : JSON rendu mal formé ({e})",
                          "signaler l'anomalie (valeur de jeton incohérente)", EXIT_TOOL) from e
    return json.dumps(_drop_nulls(data), ensure_ascii=False, indent=2) + "\n"


def template_files(kind: str) -> list[Path]:
    """Fichiers d'un modèle, chemins relatifs à lepton/templates/<kind>/ (ordre stable)."""
    root = templates_dir() / kind
    return sorted(p.relative_to(root) for p in root.rglob("*") if p.is_file())


def render_tree(kind: str, destination: Path, values: dict) -> list[Path]:
    """Écrit le modèle `kind` sous `destination` ; refuse d'écraser un fichier existant."""
    root = templates_dir() / kind
    written = []
    for rel in template_files(kind):
        target = destination / _substitute(str(rel), values, str, f"{kind}/{rel}")
        if target.exists() or target.is_symlink():
            raise LeptonError(f"{target} existe déjà", "choisir un autre nom ou un répertoire vide")
        text = (root / rel).read_text(encoding="utf-8")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_text(text, values, rel.suffix == ".json", f"{kind}/{rel}"), encoding="utf-8")
        written.append(target)
    return written
