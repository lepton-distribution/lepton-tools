"""Fichiers et regreffe : file add/remove/mv, dir add/remove, graft (FIC-1 à FIC-3, FIC-6 ;
interface §3.7, §3.8).

Toute création se fait dans le clone du greffon propriétaire, jamais dans le trunk (FIC-3), puis
`scion graft --scion <clé>` ; le contrôle final du trunk suit chaque commande.
"""

import os
import shutil
from dataclasses import dataclass
from pathlib import Path

from lepton.errors import EXIT_OK, LeptonError
from lepton.rootstock import STEM_DIR, Rootstock, find_manifest
from lepton.scion_runner import git, scion
from lepton.seed import _info, finish, scion_on_trunk

# Fichiers dont l'ajout, le retrait ou le déplacement impose une reconfiguration CMake (§3.7)
CMAKE_FILES = {"CMakeLists.txt", "lepton-greffon.json"}
GITKEEP = ".gitkeep"


@dataclass(frozen=True)
class Owner:
    key: str
    name: str
    stem: Path          # <clone>/scion, résolu


@dataclass
class Target:
    rs: Rootstock
    rel: Path                    # chemin relatif au trunk (et à scion/ du clone)
    owner: Owner | None          # connu si le chemin est donné dans un clone ou est un lien du trunk

    @property
    def trunk_path(self) -> Path:
        return self.rs.trunk / self.rel

    def clone_path(self, owner: Owner) -> Path:
        return owner.stem / self.rel


def _owners(rs: Rootstock) -> list[Owner]:
    found = []
    for e in rs.grafted():
        m = find_manifest(rs.clone(e))
        found.append(Owner(e.key, m.name if m else e.name, (rs.clone(e) / STEM_DIR).resolve()))
    return found


def _owner_of(owners: list[Owner], real: Path) -> Owner | None:
    for o in owners:
        if real == o.stem or o.stem in real.parents:
            return o
    return None


def _locate(rs: Rootstock, owners: list[Owner], raw: str) -> Target:
    """Chemin du trunk (absolu ou relatif au cwd) ou chemin dans un clone greffé."""
    path = Path(os.path.abspath(raw))
    path = path.parent.resolve() / path.name        # répertoires du trunk : vrais répertoires (E6)
    if path == rs.trunk or rs.trunk in path.parents:
        rel = path.relative_to(rs.trunk)
        owner = _owner_of(owners, path.resolve()) if path.is_symlink() else None
        return Target(rs, rel, owner)
    owner = _owner_of(owners, path)
    if owner is None or path == owner.stem:
        raise LeptonError(f"{raw} : ni dans le trunk {rs.trunk}, ni dans un greffon greffé",
                          "donner un chemin du trunk, ou d'un clone sous scion/")
    return Target(rs, path.relative_to(owner.stem), owner)


def _owners_under(owners: list[Owner], directory: Path) -> list[Owner]:
    """Greffons des feuilles (liens) sous un répertoire du trunk, dans l'ordre des greffons."""
    found = set()
    for p in directory.rglob("*"):
        if p.is_symlink():
            o = _owner_of(owners, p.resolve())
            if o is not None:
                found.add(o)
    return [o for o in owners if o in found]


def _by_name(rs: Rootstock, owners: list[Owner], name: str) -> Owner:
    o = next((o for o in owners if o.name == name), None)
    if o is None:
        raise LeptonError(f"--scion « {name} » : greffon non greffé", "lepton seed status")
    return o


def _in_seed(rs: Rootstock, owner: Owner) -> Owner:
    if owner.key not in {s.key for s in rs.sources()}:
        raise LeptonError(f"greffon « {owner.name} » ({owner.key}) hors de la graine",
                          f"lepton seed add {owner.name} … pour l'y déclarer")
    return owner


def _new_path_owner(rs: Rootstock, owners: list[Owner], t: Target, scion_name: str | None) -> Owner:
    """Propriétaire d'un chemin nouveau : clone donné, --scion, sinon greffon unique des feuilles du
    plus proche répertoire existant du trunk (§3.7)."""
    chosen = _by_name(rs, owners, scion_name) if scion_name else None
    if t.owner is not None:
        if chosen is not None and chosen != t.owner:
            raise LeptonError(f"{t.rel} est dans le clone de {t.owner.name}, --scion désigne {chosen.name}",
                              "retirer --scion ou donner le chemin du trunk")
        return _in_seed(rs, t.owner)
    if chosen is not None:
        return _in_seed(rs, chosen)
    existing = t.trunk_path.parent
    while not existing.is_dir():
        existing = existing.parent
    candidates = _owners_under(owners, existing)
    if not candidates:
        raise LeptonError(f"{t.rel} : chemin du trunk sans greffon propriétaire "
                          f"(aucune feuille sous {existing.relative_to(rs.trunk.parent)})",
                          "désigner le greffon par --scion NAME")
    if len(candidates) > 1:
        raise LeptonError(f"{t.rel} : plusieurs greffons possèdent {existing.relative_to(rs.trunk.parent)} "
                          f"({', '.join(o.name for o in candidates)})",
                          "désigner le greffon par --scion NAME")
    return _in_seed(rs, candidates[0])


def _existing_owner(t: Target, what: str) -> Owner:
    if t.owner is None:
        raise LeptonError(f"{t.rel} : {what} absent du trunk (lien vers un clone attendu)",
                          "lepton seed status ; ou donner le chemin dans le clone du greffon")
    return t.owner


def _tracked(repo_dir: Path, path: Path) -> bool:
    return bool(git(repo_dir, "ls-files", "--", str(path)).stdout.strip())


def _regraft(rs: Rootstock, owner: Owner, cmake: bool) -> int:
    scion_on_trunk(rs, "graft", "--scion", owner.key)
    return finish(rs, no_cmake=not cmake)


def _refuse_existing(t: Target, owner: Owner) -> None:
    for p in (t.trunk_path, t.clone_path(owner)):
        if p.exists() or p.is_symlink():
            raise LeptonError(f"{p} existe déjà", "choisir un autre nom")


# --------------------------------------------------------------------------
# file add / remove / mv (FIC-1, FIC-3, FIC-6)
# --------------------------------------------------------------------------
def file_add(args) -> int:
    rs = Rootstock.discover(args.rootstock)
    owners = _owners(rs)
    t = _locate(rs, owners, args.path)
    owner = _new_path_owner(rs, owners, t, args.scion)
    _refuse_existing(t, owner)
    target = t.clone_path(owner)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.touch()
    _info(f"créé dans {owner.name} : {target}")
    return _regraft(rs, owner, t.rel.name in CMAKE_FILES)


def file_remove(args) -> int:
    rs = Rootstock.discover(args.rootstock)
    t = _locate(rs, _owners(rs), args.path)
    owner = _in_seed(rs, _existing_owner(t, "fichier"))
    target = t.clone_path(owner)
    if not target.is_file() or target.is_symlink():
        raise LeptonError(f"{target} : fichier absent du clone de {owner.name}", "lepton dir remove pour un répertoire")
    if _tracked(target.parent, target):
        git(target.parent, "rm", "-q", "--", target.name)
    else:
        target.unlink()
    _info(f"retiré de {owner.name} : {target}")
    return _regraft(rs, owner, t.rel.name in CMAKE_FILES)


def file_mv(args) -> int:
    rs = Rootstock.discover(args.rootstock)
    owners = _owners(rs)
    src = _locate(rs, owners, args.source)
    owner = _in_seed(rs, _existing_owner(src, "fichier source"))
    if not src.clone_path(owner).is_file():
        raise LeptonError(f"{src.clone_path(owner)} : fichier absent du clone de {owner.name}",
                          "lepton file mv ne déplace que des fichiers")
    dst = _locate(rs, owners, args.destination)
    if dst.owner is not None and dst.owner != owner:
        raise LeptonError(f"source dans {owner.name}, destination dans {dst.owner.name}",
                          "déplacement limité à un greffon : lepton file add puis lepton file remove")
    if dst.owner is None:
        existing = dst.trunk_path.parent
        while not existing.is_dir():
            existing = existing.parent
        if owner not in _owners_under(owners, existing):
            raise LeptonError(f"{dst.rel} : hors des répertoires de {owner.name}",
                              "déplacement limité à un greffon : lepton file add puis lepton file remove")
    _refuse_existing(dst, owner)
    source, target = src.clone_path(owner), dst.clone_path(owner)
    target.parent.mkdir(parents=True, exist_ok=True)
    if _tracked(source.parent, source):
        git(owner.stem, "mv", "--", str(source), str(target))
    else:
        source.rename(target)
    _info(f"déplacé dans {owner.name} : {source} → {target}")
    return _regraft(rs, owner, bool({src.rel.name, dst.rel.name} & CMAKE_FILES))


# --------------------------------------------------------------------------
# dir add / remove (FIC-2, FIC-3)
# --------------------------------------------------------------------------
def dir_add(args) -> int:
    rs = Rootstock.discover(args.rootstock)
    owners = _owners(rs)
    t = _locate(rs, owners, args.path)
    owner = _new_path_owner(rs, owners, t, args.scion)
    _refuse_existing(t, owner)
    target = t.clone_path(owner)
    target.mkdir(parents=True)
    (target / GITKEEP).touch()
    _info(f"créé dans {owner.name} : {target}/ ({GITKEEP})")
    return _regraft(rs, owner, False)


def dir_remove(args) -> int:
    rs = Rootstock.discover(args.rootstock)
    owners = _owners(rs)
    t = _locate(rs, owners, args.path)
    if t.owner is not None:
        candidates = [t.owner]
    elif t.trunk_path.is_dir() and not t.trunk_path.is_symlink():
        candidates = _owners_under(owners, t.trunk_path)
    else:
        raise LeptonError(f"{t.rel} : répertoire absent du trunk", "lepton file remove pour un fichier")
    if args.scion:
        chosen = _by_name(rs, owners, args.scion)
        if chosen not in candidates:
            raise LeptonError(f"{t.rel} : aucune feuille de {chosen.name} ({', '.join(o.name for o in candidates)})",
                              "choisir un des greffons listés")
        candidates = [chosen]
    if not candidates:
        raise LeptonError(f"{t.rel} : répertoire du trunk sans greffon propriétaire", "rien à retirer")
    if len(candidates) > 1:
        raise LeptonError(f"{t.rel} : plusieurs greffons y ont des fichiers ({', '.join(o.name for o in candidates)})",
                          "désigner la part à retirer par --scion NAME")
    owner = _in_seed(rs, candidates[0])
    target = t.clone_path(owner)
    if not target.is_dir() or target.is_symlink():
        raise LeptonError(f"{target} : répertoire absent du clone de {owner.name}", "lepton seed status")
    cmake = any(p.name in CMAKE_FILES for p in target.rglob("*"))
    if _tracked(target, target):
        git(target, "rm", "-r", "-q", "--", ".")
    if target.exists():
        shutil.rmtree(target)                    # fichiers non suivis du greffon dans ce répertoire
    _info(f"retiré de {owner.name} : {target}/")
    return _regraft(rs, owner, cmake)


# --------------------------------------------------------------------------
# graft (§3.8)
# --------------------------------------------------------------------------
def graft(args) -> int:
    rs = Rootstock.discover(args.rootstock)
    owners = _owners(rs)
    keys = [_by_name(rs, owners, n).key for n in args.scion or []]
    scion_on_trunk(rs, "graft", *(["--force"] if args.force else []), *(a for k in keys for a in ("--scion", k)))
    _info("regreffe " + (f"de {', '.join(args.scion)}" if keys else "complète") + " faite")
    return finish(rs, args.no_cmake)
