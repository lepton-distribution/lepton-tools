"""Lecture d'un rootstock scion : trunk, listes `.scion.*`, graine, manifestes, contrôle du trunk.

Lecture seule : toute écriture des fichiers `.scion.*` passe par scion (interface PA-9 §1). Le
format reproduit celui de scion 0.5.1.0 (`scion/model.py`) : champs séparés par des blancs, `#`
commence un commentaire, ligne trop courte ignorée. Depuis scion 0.6.0.0 (projection d'un dépôt
tiers, ENV-41) : 6ᵉ colonne facultative de la liste greffée (`.scion/` porteur, P-P3) et
`.scion.projections` d'une graine ou d'un porteur.
"""

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

from lepton.errors import LeptonError
from lepton.validation import SCION_MANIFEST, SEED_MANIFEST

SIGNATURE = ".scion.rootstock.signature"
GRAFTED_LIST = ".scion.grafted.list"
SOURCES_LIST = ".scion.sources.list"
RAMIFICATIONS = ".scion.ramifications"
PROJECTIONS = ".scion.projections"
STEM_DIR = "scion"
SOURCE_ROOT = Path("sys/root/src")   # racine des destinations des manifestes (lecteur CMake)

SHELF = "lepton"
KERNEL_KEY = f"{SHELF}@original::tree"
# Type de greffon (enum des schémas) → préfixe de clé scion créée par lepton (décision S2 d'ENV-8)
KEY_PREFIX = {"famille": "family", "bsp": "bsp", "application": "application", "bibliotheque": "library"}

# Greffon local du projet (ENV-9) : fichiers générés versionnés dans la graine, sous project/scion/
PROJECT_SUBPATH = "project"

_WHITESPACE = re.compile(r"[ \t\n]+")


def is_system_file(name: str) -> bool:
    """Fichiers système ignorés par lepton (PA-9 Q8)."""
    return name == ".DS_Store" or name.startswith("._")


def scion_key(kind: str, name: str) -> str:
    """Clé scion d'un greffon créé par lepton : un préfixe par greffon, donc un clone distinct."""
    return f"{SHELF}@{KEY_PREFIX[kind]}-{name}"


def project_key(project: str) -> str:
    """Clé scion du greffon local du projet (presets générés par lepton generate)."""
    return f"{SHELF}@{PROJECT_SUBPATH}-{project}"


def _fields(line: str) -> list[str]:
    return _WHITESPACE.sub(" ", line).split("#", 1)[0].split()


def _lines(path: Path) -> list[list[str]]:
    if not path.exists():
        return []
    return [f for f in (_fields(l) for l in path.read_text(encoding="utf-8").splitlines()) if f]


@dataclass(frozen=True)
class GraftedEntry:
    shelf: str
    name: str
    version: str
    local_path: str
    seed_dot: str = ""
    porter: str = ""        # 6ᵉ colonne : `.scion/` du scion porteur d'une clé projetée (P-P3)

    @property
    def key(self) -> str:
        return f"{self.shelf}@{self.name}"

    @property
    def dot(self) -> str:
        """`.scion/` qui déclare l'entrée : porteur (6ᵉ colonne), sinon graine (5ᵉ)."""
        return self.porter or self.seed_dot


@dataclass(frozen=True)
class SourceEntry:
    shelf: str
    name: str
    version: str
    location: str
    subpath: str = ""

    @property
    def key(self) -> str:
        return f"{self.shelf}@{self.name}"


def read_grafted(path: Path) -> list[GraftedEntry]:
    return [GraftedEntry(f[0], f[1], f[2], f[3], f[4] if len(f) > 4 else "", f[5] if len(f) > 5 else "")
            for f in _lines(path) if len(f) >= 4]


def read_sources(path: Path) -> list[SourceEntry]:
    return [SourceEntry(f[0], f[1], f[2], f[3], f[4] if len(f) > 4 else "") for f in _lines(path) if len(f) >= 4]


def read_ramifications(path: Path) -> list[str]:
    """Clés `shelf@nom` déclarées dans `.scion.ramifications`."""
    return [f"{f[0]}@{f[1]}" for f in _lines(path) if len(f) >= 3]


def read_projection_keys(path: Path) -> set[str]:
    """Clés `shelf@nom` qui ont au moins une ligne dans `.scion.projections` (clés projetées)."""
    return {f"{f[0]}@{f[1]}" for f in _lines(path) if len(f) >= 4}


@dataclass
class Manifest:
    path: Path
    data: dict
    trunk_dir: Path | None = None   # répertoire du manifeste dans le trunk (greffon greffé)

    @property
    def name(self) -> str:
        return self.data.get("nom", "")

    @property
    def kind(self) -> str:
        return self.data.get("type", "")


def find_manifest(clone: Path) -> Manifest | None:
    """Manifeste d'un greffon : le moins profond sous `<clone>/scion/sys/root/src/`."""
    root = clone / STEM_DIR / SOURCE_ROOT
    if not root.is_dir():
        return None
    found = sorted(root.rglob(SCION_MANIFEST), key=lambda p: (len(p.parts), str(p)))
    if not found:
        return None
    try:
        data = json.loads(found[0].read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise LeptonError(f"{found[0]} : manifeste illisible ({e})", f"lepton check {found[0]}") from e
    return Manifest(found[0], data if isinstance(data, dict) else {})


@dataclass
class TrunkReport:
    regular_files: list[Path]
    broken_links: list[Path]

    @property
    def clean(self) -> bool:
        return not (self.regular_files or self.broken_links)


class Rootstock:
    def __init__(self, path: Path):
        self.path = Path(path).resolve()
        candidates = sorted(c for c in self.path.iterdir() if c.is_dir() and (c / GRAFTED_LIST).exists())
        if len(candidates) != 1:
            raise LeptonError(f"{self.path} : trunk introuvable ou ambigu ({len(candidates)} répertoire(s) "
                              f"portant {GRAFTED_LIST})", "scion rootstock-information")
        self.trunk = candidates[0]

    @classmethod
    def discover(cls, explicit: str | Path | None = None, start: Path | None = None) -> "Rootstock":
        """`-C DIR`, sinon le premier répertoire portant la signature en remontant (trunk ou clone)."""
        if explicit is not None:
            path = Path(explicit).resolve()
            if not (path / SIGNATURE).exists():
                raise LeptonError(f"{path} n'est pas un rootstock ({SIGNATURE} absent)",
                                  "indiquer la racine du rootstock avec -C DIR")
            return cls(path)
        current = Path(start or Path.cwd()).resolve()
        for candidate in (current, *current.parents):
            if (candidate / SIGNATURE).exists():
                return cls(candidate)
        raise LeptonError(f"aucun rootstock trouvé depuis {current}",
                          "se placer dans un rootstock ou utiliser -C DIR ; nouveau projet : lepton seed new")

    def resolve(self, location: str) -> Path:
        p = Path(location)
        return p if p.is_absolute() else self.path / p

    @property
    def depots(self) -> Path:
        return self.path / "depots"

    @property
    def build(self) -> Path:
        return self.path / "build"

    def grafted(self) -> list[GraftedEntry]:
        return read_grafted(self.trunk / GRAFTED_LIST)

    def seed_dot(self) -> Path:
        """Répertoire `.scion/` de la graine courante (unique ; 5ᵉ colonne de la liste greffée)."""
        seeds = []
        for e in self.grafted():
            if e.seed_dot and e.seed_dot not in seeds:
                seeds.append(e.seed_dot)
        if len(seeds) != 1:
            raise LeptonError(f"{self.path} : {len(seeds)} graine(s) dans {GRAFTED_LIST}, une seule attendue",
                              "lepton seed new pour un nouveau projet")
        return self.resolve(seeds[0])

    def seed_root(self) -> Path:
        """Racine du dépôt de la graine (parent de `scion/.scion/`)."""
        return self.seed_dot().parent.parent

    def seed_manifest_path(self) -> Path:
        return self.seed_dot() / SEED_MANIFEST

    def is_reference_seed(self) -> bool:
        """Graine de référence (PA-19 C d'ENV-16, PA-23 d'ENV-18) : ni `lepton-graine.json` ni greffon
        local de projet (`project/`) ; une graine de projet abîmée garde `project/`."""
        return not self.seed_manifest_path().exists() and not (self.seed_root() / PROJECT_SUBPATH).exists()

    def sources(self) -> list[SourceEntry]:
        return read_sources(self.seed_dot() / SOURCES_LIST)

    def clone(self, entry: GraftedEntry) -> Path:
        return self.resolve(entry.local_path)

    def manifests(self) -> dict[str, Manifest]:
        """Manifeste de chaque greffon greffé, par clé scion (greffons sans manifeste omis)."""
        found = {}
        for e in self.grafted():
            m = find_manifest(self.clone(e))
            if m is not None:
                m.trunk_dir = self.trunk / m.path.parent.relative_to(self.clone(e) / STEM_DIR)
                found[e.key] = m
        return found

    # --- clés projetées (scion 0.6.0.0, ENV-41) ---------------------------------------------------
    def projected_keys(self) -> set[str]:
        """Clés projetées greffées : 6ᵉ colonne présente, ou ligne dans le `.scion.projections` du
        `.scion/` qui les déclare (graine ou porteur)."""
        grafted = self.grafted()
        declared = set()
        for dot in {e.dot for e in grafted if e.dot}:
            declared |= read_projection_keys(self.resolve(dot) / PROJECTIONS)
        return {e.key for e in grafted if e.porter or e.key in declared}

    def porter_of(self, entry: GraftedEntry) -> GraftedEntry | None:
        """Scion greffé dont le `scion/.scion/` porte la clé projetée `entry` (None : la graine)."""
        if not entry.porter:
            return None
        clone = self.resolve(entry.porter).resolve().parent.parent
        return next((e for e in self.grafted() if self.clone(e).resolve() == clone), None)

    def projection_tables(self) -> dict[str, dict[str, str]]:
        """Par clé projetée : chemin relatif au clone tiers → chemin relatif au trunk, d'après les
        liens du trunk (résultat réel de la greffe, P-G3 ; aucune relecture des motifs)."""
        roots = {e.key: os.path.realpath(self.clone(e)) for e in self.grafted() if e.key in self.projected_keys()}
        tables: dict[str, dict[str, str]] = {key: {} for key in roots}
        if not roots:
            return tables
        trunk = str(self.trunk)
        for directory, dirs, files in os.walk(trunk):
            for name in dirs + files:
                p = os.path.join(directory, name)
                if not os.path.islink(p):
                    continue
                real = os.path.realpath(p)
                for key, root in roots.items():
                    if real.startswith(root + os.sep):
                        tables[key][os.path.relpath(real, root)] = os.path.relpath(p, trunk)
                        break
        return tables

    def key_of(self, name: str) -> str | None:
        """Clé scion du greffon greffé dont le manifeste porte `nom` = name."""
        for key, m in self.manifests().items():
            if m.name == name:
                return key
        return None

    def check_trunk(self) -> TrunkReport:
        """Fichiers réguliers (hors liste greffée et fichiers système) et liens cassés du trunk."""
        regular, broken = [], []
        for p in sorted(self.trunk.rglob("*")):
            if p.is_symlink():
                if not p.exists():
                    broken.append(p)
            elif p.is_file() and p.name != GRAFTED_LIST and not is_system_file(p.name):
                regular.append(p)
        return TrunkReport(regular, broken)

    def system_files_in_trunk(self) -> list[Path]:
        """Fichiers système réguliers du trunk (supprimés par lepton graft, Q8)."""
        return [p for p in self.trunk.rglob("*") if is_system_file(p.name) and p.is_file() and not p.is_symlink()]

    def purge_system_files(self) -> list[Path]:
        """Supprime les fichiers système réguliers du trunk (Q8) : scion graft et graft-remove les refusent."""
        found = self.system_files_in_trunk()
        for p in found:
            p.unlink()
        return found
