"""lepton seed tree : architecture du projet, exécutif → bibliothèques → greffons → fichiers (IDE-1 ;
ENV-12 lot 5, décisions du 2026-10-27).

Source : réponse de l'API fichier CMake (codemodel-v2) du preset actif — cibles réellement construites,
sources dans l'ordre de CMake ; chaque source est rattachée à son greffon par le lien du trunk. Les
en-têtes `.h` des répertoires où un greffon compile des sources s'y ajoutent, puis les sources de ces
répertoires compilées par aucune cible (`unbuilt`). Sans réponse (preset non
configuré) : repli sur les liens du trunk, par greffon, sans exécutif ni bibliothèque. Les greffons sont
ceux de `seed status` (même calcul), pour une vue cohérente avec l'état de la graine.
"""

import json
import os
import sys
from pathlib import Path

from lepton.errors import EXIT_OK, LeptonError
from lepton.files import Owner, _owner_of, _owners
from lepton.generate import ACTIVE_DIR, COMPILE_COMMANDS, preset_name
from lepton.rootstock import Rootstock
from lepton.seed import _info, load_graine, status_data

API_REPLY = Path(".cmake/api/v1/reply")
MAIN_EXECUTABLE = "lepton"                      # exécutif du projet, affiché en premier (P4)
LIBRARY_TYPES = {"STATIC_LIBRARY", "OBJECT_LIBRARY", "SHARED_LIBRARY", "MODULE_LIBRARY"}
SOURCE_SUFFIXES = {".c", ".cpp", ".S", ".s"}
HEADER_SUFFIX = ".h"


# --------------------------------------------------------------------------
# preset et réponse de l'API fichier
# --------------------------------------------------------------------------
def _presets(rs: Rootstock) -> list[str]:
    path = rs.seed_manifest_path()
    if not path.exists():
        return []
    graine = load_graine(path)
    return [preset_name(graine["projet"]["nom"], c) for c in graine.get("configurations", [])]


def _active_preset(rs: Rootstock) -> str | None:
    """Preset dont le répertoire de construction est cité par build/.active (base de clangd, copiée
    par CMake Tools au changement de preset, amorcée par lepton generate)."""
    try:
        entries = json.loads((rs.build / ACTIVE_DIR / COMPILE_COMMANDS).read_text(encoding="utf-8"))
        directory = Path(entries[0]["directory"])
    except (OSError, ValueError, LookupError, TypeError):
        return None
    if directory.parent == rs.build:
        return directory.name
    return directory.relative_to(rs.build).parts[0] if rs.build in directory.parents else None


def _reply_index(build: Path) -> Path | None:
    reply = build / API_REPLY
    indexes = sorted(reply.glob("index-*.json")) if reply.is_dir() else []
    return indexes[-1] if indexes else None      # le plus récent (nom horodaté, ordre lexical)


def choose_preset(rs: Rootstock, explicit: str | None) -> tuple[str | None, str]:
    """Preset retenu et raison : --preset, sinon preset actif, sinon premier preset configuré."""
    if explicit:
        return explicit, "--preset"
    active = _active_preset(rs)
    if active:
        return active, "actif (build/.active)"
    for p in _presets(rs):
        if _reply_index(rs.build / p):
            return p, "premier preset configuré"
    return None, "aucun preset configuré"


def _load(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise LeptonError(f"{path} illisible ({e})", "reconfigurer le preset (cmake --preset …)") from e


def read_codemodel(build: Path) -> dict[str, dict] | None:
    """Cibles de la réponse codemodel-v2 (nom → objet cible), ou None sans réponse."""
    index_path = _reply_index(build)
    if index_path is None:
        return None
    reply = index_path.parent
    codemodel = next((o for o in _load(index_path).get("objects", [])
                      if o.get("kind") == "codemodel" and o.get("version", {}).get("major") == 2), None)
    if codemodel is None:
        return None
    model = _load(reply / codemodel["jsonFile"])
    configuration = model["configurations"][0]
    targets = {}
    for t in configuration.get("targets", []):
        data = _load(reply / t["jsonFile"])
        data["_source_root"] = model["paths"]["source"]
        targets[t["name"]] = data
    return targets


# --------------------------------------------------------------------------
# rattachement des fichiers
# --------------------------------------------------------------------------
class _Files:
    """Fichiers d'un (bibliothèque, greffon) dans l'ordre de première apparition."""

    def __init__(self) -> None:
        self.by_owner: dict[str | None, dict] = {}

    def add(self, owner: Owner | None, generated: bool, entry: dict) -> None:
        key = owner.key if owner else ("generated" if generated else None)
        group = self.by_owner.setdefault(key, {"key": owner.key if owner else None,
                                                "name": owner.name if owner else None,
                                                "generated": generated, "files": []})
        if all(f["relative"] != entry["relative"] for f in group["files"]):
            group["files"].append(entry)


def _entry(rs: Rootstock, trunk_path: Path, kind: str) -> dict:
    return {"relative": str(trunk_path.relative_to(rs.trunk)), "trunk_path": str(trunk_path),
            "clone_path": str(trunk_path.resolve()), "kind": kind}


def _neighbours(rs: Rootstock, owners: list[Owner], owner: Owner, directories: list[Path],
                compiled: set[Path]) -> list[dict]:
    """Liens vers le clone du même greffon dans les répertoires du trunk donnés : en-têtes .h, puis
    sources compilées par aucune cible (`unbuilt` : pas encore configurées, ou hors des `sources` du
    manifeste ; décision du 2026-10-27, essai du lot 5)."""
    headers, unbuilt = [], []
    for d in directories:
        try:
            names = sorted(e.name for e in os.scandir(d) if e.is_symlink())
        except OSError:
            continue
        for n in names:
            p = d / n
            if p.suffix == HEADER_SUFFIX and _owner_of(owners, p.resolve()) == owner:
                headers.append(_entry(rs, p, "header"))
            elif p.suffix in SOURCE_SUFFIXES and p not in compiled and _owner_of(owners, p.resolve()) == owner:
                unbuilt.append(_entry(rs, p, "unbuilt"))
    return headers + unbuilt


def _compiled_paths(target: dict) -> list[Path]:
    """Sources compilées d'une cible (`compileGroupIndex`), chemins absolus."""
    root = Path(target["_source_root"])
    return [Path(s["path"]) if os.path.isabs(s["path"]) else root / s["path"]
            for s in target.get("sources", []) if "compileGroupIndex" in s]


def _library(rs: Rootstock, owners: list[Owner], name: str, target: dict, compiled: set[Path]) -> dict:
    files = _Files()
    for path in _compiled_paths(target):            # sources non compilées (règles, en-têtes listés) omises
        if rs.trunk in path.parents:
            owner = _owner_of(owners, path.resolve()) if path.is_symlink() else None
            files.add(owner, False, _entry(rs, path, "compiled"))
        else:                                        # source générée dans le répertoire de construction
            files.add(None, True, {"relative": str(path), "trunk_path": None, "clone_path": str(path),
                                   "kind": "compiled"})
    scions = list(files.by_owner.values())
    by_key = {o.key: o for o in owners}
    for group in scions:
        owner = by_key.get(group["key"])
        if owner is None:
            continue
        directories = list(dict.fromkeys(Path(f["trunk_path"]).parent for f in group["files"]))
        group["files"] += _neighbours(rs, owners, owner, directories, compiled)
    return {"name": name, "type": target["type"], "scions": scions}


def _dependencies(targets: dict[str, dict], name: str) -> list[str]:
    """Bibliothèques dont dépend une cible (fermeture transitive, ordre de découverte de CMake)."""
    ids = {t["id"]: n for n, t in targets.items() if "id" in t}
    order: list[str] = []
    pending = [name]
    while pending:
        current = pending.pop(0)
        for d in targets[current].get("dependencies", []):
            dep = ids.get(d["id"])
            if dep and dep not in order and targets[dep]["type"] in LIBRARY_TYPES:
                order.append(dep)
                pending.append(dep)
    return order


def executables(rs: Rootstock, owners: list[Owner], targets: dict[str, dict]) -> list[dict]:
    names = sorted((n for n, t in targets.items() if t["type"] == "EXECUTABLE"),
                   key=lambda n: (n != MAIN_EXECUTABLE, n))
    compiled = {p for t in targets.values() for p in _compiled_paths(t)}     # par toutes les cibles
    result = []
    for n in names:
        libraries = [_library(rs, owners, n, targets[n], compiled)]          # sources propres de l'exécutif
        libraries += [_library(rs, owners, d, targets[d], compiled) for d in _dependencies(targets, n)]
        result.append({"name": n, "libraries": [lib for lib in libraries if lib["scions"]]})
    return result


def by_scion(rs: Rootstock, owners: list[Owner]) -> list[dict]:
    """Repli sans réponse CMake : sources et en-têtes liés dans le trunk, par greffon."""
    files = {o.key: [] for o in owners}
    for directory, dirnames, filenames in os.walk(rs.trunk):
        dirnames.sort()
        base = Path(directory)
        for n in sorted(filenames + [d for d in dirnames if (base / d).is_symlink()]):
            p = base / n
            if p.is_symlink() and (p.suffix in SOURCE_SUFFIXES or p.suffix == HEADER_SUFFIX):
                o = _owner_of(owners, p.resolve())
                if o is not None:
                    files[o.key].append(_entry(rs, p, "header" if p.suffix == HEADER_SUFFIX else "compiled"))
    return [{"key": o.key, "name": o.name, "generated": False, "files": files[o.key]}
            for o in owners if files[o.key]]


# --------------------------------------------------------------------------
# commande
# --------------------------------------------------------------------------
def tree_data(rs: Rootstock, explicit: str | None) -> dict:
    status, _graine, _roles, _missing, _report = status_data(rs)
    owners = _owners(rs)
    preset, why = choose_preset(rs, explicit)
    build = rs.build / preset if preset else None
    targets = read_codemodel(build) if build else None
    result = {"rootstock": str(rs.path), "trunk": str(rs.trunk), "preset": preset, "preset_reason": why,
              "build": str(build) if build else None, "build_root": str(rs.build), "scions": status["scions"]}
    if targets is not None:
        result.update(source="codemodel", message=None, executables=executables(rs, owners, targets),
                      by_scion=[])
    else:
        message = (f"preset {preset} non configuré (aucune réponse de l'API fichier CMake dans {build})"
                   if preset else "aucun preset configuré") + " : greffons et fichiers du trunk seulement"
        result.update(source="manifests", message=message, executables=[], by_scion=by_scion(rs, owners))
    return result


def _print_group(group: dict, indent: str, verbose: bool) -> None:
    name = group["name"] or ("(généré)" if group["generated"] else "(hors greffon)")
    count = {k: sum(1 for f in group["files"] if f["kind"] == k) for k in ("compiled", "header", "unbuilt")}
    unbuilt = f", {count['unbuilt']} hors construction" if count["unbuilt"] else ""
    _info(f"{indent}{name} : {count['compiled']} source(s), {count['header']} en-tête(s){unbuilt}")
    if verbose:
        for f in group["files"]:
            _info(f"{indent}    {f['relative']}")


def seed_tree(args) -> int:
    rs = Rootstock.discover(args.rootstock)
    data = tree_data(rs, args.preset)
    if args.preset and data["source"] != "codemodel":
        raise LeptonError(f"preset {args.preset} non configuré : aucune réponse de l'API fichier CMake dans "
                          f"{data['build']}", f"lepton generate, puis cmake --preset {args.preset} (dans le trunk)")
    if args.json:
        json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return EXIT_OK
    _info(f"preset : {data['preset'] or '—'} ({data['preset_reason']})")
    if data["message"]:
        _info(data["message"])
        for g in data["by_scion"]:
            _print_group(g, "  ", args.verbose)
        return EXIT_OK
    for exe in data["executables"]:
        _info(f"{exe['name']}")
        for lib in exe["libraries"]:
            _info(f"  {lib['name']} ({lib['type']})")
            for g in lib["scions"]:
                _print_group(g, "    ", args.verbose)
    return EXIT_OK
