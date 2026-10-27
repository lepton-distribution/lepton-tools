"""Graine : seed new, status, add, remove, replace, lock (GRA-1 à GRA-6 ; interface §3.2-§3.5).

Toute écriture des listes `.scion.*` et du trunk passe par scion ; lepton écrit seulement les
manifestes `lepton-graine.json`, `lepton-graine.lock.json`, à la création les fichiers du modèle de
graine, et les fichiers du greffon local du projet (`project/scion/` : XML mklepton du projet, O5).
"""

import json
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from lepton import __version__, cmake, mkconf
from lepton.checks import removal_unprovided
from lepton.errors import EXIT_OK, EXIT_TOOL, EXIT_USER, LeptonError
from lepton.rootstock import (KERNEL_KEY, PROJECT_SUBPATH, STEM_DIR, Manifest, Rootstock, TrunkReport,
                              find_manifest, is_system_file, project_key, scion_key)
from lepton.scion_runner import git, run, scion
from lepton.templates import c_identifier, render_text, render_tree, templates_dir
from lepton.validation import SEED_MANIFEST, validate_data, validate_xml

KERNEL_NAME = "lepton-noyau"
DEFAULT_KERNEL_ORIGIN = "https://github.com/lepton-distribution/lepton-original-tree.scions.git@master"
DEFAULT_VERSION = "master"
LOCAL_VERSION = "*"
SEED_DOT = Path("scion/.scion")
GRAINE_REL = SEED_DOT / SEED_MANIFEST

# LOCATION[@VERSION][:PATH] ; VERSION sans « : » ni « @ », « / » admis (branche `devenv/x`, O14) ;
# PATH ne commence pas par « / ». L'autorité d'une URL (`scheme://[user@]hôte`) appartient à
# LOCATION : son « @ » ne sépare pas de version.
_ORIGIN = re.compile(r"^(?P<loc>(?:[A-Za-z][A-Za-z0-9+.-]*://[^/]*)?.+?)(?:@(?P<ver>[^@:]+))?"
                     r"(?::(?P<path>[^:@/][^:@]*))?$")
_IDENT = re.compile(r"^[a-z0-9][a-z0-9._-]*$")


def _info(message: str) -> None:
    print(message)


def scion_on_trunk(rs: Rootstock, *args: str):
    """scion graft / graft-remove sur le rootstock, après suppression des fichiers système réguliers du
    trunk (PA-9 Q8) : le Finder en recrée à tout moment, et scion refuse un trunk qui en contient."""
    for p in rs.purge_system_files():
        _info(f"fichier système supprimé du trunk : {p}")
    return scion(*args, cwd=rs.path)


def _warn(message: str) -> None:
    print(f"lepton: attention: {message}", file=sys.stderr)


# --------------------------------------------------------------------------
# origines (GRA-3)
# --------------------------------------------------------------------------
@dataclass
class Origin:
    location: str      # URL (avec netloc) ou chemin local (absolu, ou relatif au rootstock)
    version: str
    subpath: str = ""

    @property
    def remote(self) -> bool:
        return bool(urlparse(self.location).netloc)

    def scion_args(self) -> list[str]:
        return [self.version, self.location] + ([self.subpath] if self.subpath else [])


def parse_location(text: str, version: str | None = None, subpath: str | None = None,
                   rootstock: Path | None = None) -> Origin:
    """`LOCATION[@VERSION][:PATH]` (ou options séparées) → origine contrôlée.

    URL : version par défaut `master`. Chemin local (relatif au répertoire courant) : version `*`
    (scion l'utilise en place, sans clone), `@VERSION` refusé ; le chemin doit porter `scion/` ;
    il est rendu relatif au rootstock s'il s'y trouve, absolu sinon.
    """
    m = _ORIGIN.match(text)
    if m is None:
        raise LeptonError(f"origine « {text} » illisible", "forme attendue : LOCATION[@VERSION][:PATH]")
    loc, ver, path = m.group("loc"), m.group("ver") or version, m.group("path") or subpath or ""
    if ver and any(part in ("", ".", "..") for part in ver.split("/")):
        # scion range le clone sous depots/<étagère>/<préfixe>/<version> : chemin imbriqué, jamais remontant
        raise LeptonError(f"version « {ver} » invalide", "branche ou tag git : segments non vides, ni « . » ni « .. »")
    if urlparse(loc).netloc:
        return Origin(loc, ver or DEFAULT_VERSION, path)
    if ver and ver != LOCAL_VERSION:
        raise LeptonError(f"origine locale « {loc} » : version « {ver} » sans effet (scion utilise un "
                          "répertoire local en place)",
                          f"retirer la version, ou désigner le dépôt git par une URL : file://localhost{Path(loc).resolve()}@{ver}")
    local = Path(loc).expanduser().resolve()
    stem = local / path / "scion" if path else local / "scion"
    if not stem.is_dir():
        raise LeptonError(f"origine locale « {loc} » : {stem} absent",
                          "désigner la racine du dépôt du greffon (qui contient scion/), ou préciser :PATH")
    if rootstock is not None:
        try:
            local = local.relative_to(rootstock)
        except ValueError:
            pass
    return Origin(str(local), LOCAL_VERSION, path)


def parse_origin_option(text: str) -> tuple[str, str]:
    name, sep, rest = text.partition("=")
    if not sep or not _IDENT.match(name) or not rest:
        raise LeptonError(f"--origin « {text} » invalide", "forme attendue : --origin SCION=LOCATION[@VERSION][:PATH]")
    return name, rest


# --------------------------------------------------------------------------
# manifeste de graine
# --------------------------------------------------------------------------
def load_graine(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise LeptonError(f"{path} absent : la graine n'est pas une graine lepton",
                          "créer le projet par lepton seed new") from None
    except ValueError as e:
        raise LeptonError(f"{path} : JSON mal formé ({e})", f"lepton check {path}") from e


def save_graine(path: Path, data: dict) -> None:
    anomalies = validate_data(data, "seed", str(path))
    if anomalies:
        raise LeptonError("manifeste de graine refusé :\n" + "\n".join(str(a) for a in anomalies),
                          "signaler l'anomalie (lepton a produit un manifeste invalide)")
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def graine_values(name: str, bsp: str, backend: str, mkconf: str, configurations: list) -> dict:
    return {"name": name, "version": "0.1.0", "description": f"Projet Lepton {name}.",
            "kernel": KERNEL_NAME, "bsp": bsp, "backend": backend,
            "configurations": configurations, "mkconf": mkconf}


def configurations_for(bsp: Manifest) -> list[dict]:
    """Configuration initiale : debug-qemu si le BSP déclare qemu, sinon debug-board (§3.2)."""
    if "qemu" in bsp.data:
        return [{"nom": "debug-qemu", "construction": "Debug", "execution": "qemu"}]
    return [{"nom": "debug-board", "construction": "Debug", "execution": "carte"}]


# --------------------------------------------------------------------------
# contrôles communs
# --------------------------------------------------------------------------
def finish(rs: Rootstock, no_cmake: bool) -> int:
    """Contrôle final du trunk (FIC-3, critère ENV-8) puis reconfiguration CMake (GRA-4)."""
    report = rs.check_trunk()
    if not report.clean:
        lines = [f"  fichier régulier : {p}" for p in report.regular_files] + \
                [f"  lien cassé : {p}" for p in report.broken_links]
        raise LeptonError("trunk incohérent après l'opération :\n" + "\n".join(lines),
                          "déplacer les fichiers réguliers dans le clone de leur greffon, puis lepton graft")
    if not no_cmake:
        for d in cmake.reconfigure(rs):
            _info(f"CMake reconfiguré : {d}")
    return EXIT_OK


def _manifest_of(rs: Rootstock, key: str) -> Manifest | None:
    for e in rs.grafted():
        if e.key == key:
            return find_manifest(rs.clone(e))
    return None


def _expect(rs: Rootstock, key: str, name: str, kind: str) -> Manifest:
    m = _manifest_of(rs, key)
    if m is None:
        raise LeptonError(f"greffon « {name} » ({key}) : aucun lepton-greffon.json sous scion/sys/root/src/",
                          "vérifier l'origine (racine du dépôt, :PATH)")
    if m.name != name or m.kind != kind:
        raise LeptonError(f"greffon {key} : manifeste « {m.name} » de type « {m.kind} », "
                          f"attendu « {name} » de type « {kind} » ({m.path})",
                          "vérifier le nom donné et l'origine")
    return m


# --------------------------------------------------------------------------
# greffon local du projet (ENV-9 : presets ; O5 : XML mklepton du projet)
# --------------------------------------------------------------------------
def project_stem(seed_root: Path) -> Path:
    """`<graine>/project/scion/` : racine greffée à la racine du trunk."""
    return seed_root / PROJECT_SUBPATH / STEM_DIR


def _project_links_missing(rs: Rootstock, stem: Path) -> bool:
    for p in stem.rglob("*"):
        if p.is_file() and not is_system_file(p.name):
            link = rs.trunk / p.relative_to(stem)
            if not (link.is_symlink() and link.resolve() == p.resolve()):
                return True
    return False


def graft_project(rs: Rootstock, seed_root: Path, project: str) -> bool:
    """Greffon local du projet : déclaré, inscrit puis greffé tant qu'un lien du trunk manque ;
    rend vrai si la graine ou le trunk a changé."""
    key = project_key(project)
    changed = False
    if key not in {s.key for s in rs.sources()}:
        try:
            location = str(seed_root.relative_to(rs.path))
        except ValueError:
            location = str(seed_root)
        scion("seed-scion-add", "--seed", str(seed_root), key, LOCAL_VERSION, location, PROJECT_SUBPATH,
              cwd=rs.path)
        changed = True
    if key not in {e.key for e in rs.grafted()}:
        scion("seed-clone", "--seed", str(seed_root), cwd=rs.path)   # inscrit la clé dans la liste greffée
        changed = True
    if _project_links_missing(rs, project_stem(seed_root)):
        scion_on_trunk(rs, "graft", "--scion", key)
        changed = True
    return changed


def in_project(rs: Rootstock, seed_root: Path, rel: str) -> Path | None:
    """Fichier du greffon projet désigné par `rel` (relatif au trunk), si le trunk y mène."""
    target = (rs.trunk / rel).resolve()
    stem = project_stem(seed_root).resolve()
    return target if target.is_file() and target.is_relative_to(stem) else None


def _validate_project_xml(xml: Path, label: str) -> None:
    try:
        anomalies = validate_xml(xml)
    except LeptonError as e:
        if e.code != EXIT_TOOL:
            raise
        _warn(f"{label} : {e.message}" + (f" ({e.action})" if e.action else ""))
        return
    for a in anomalies:
        _warn(f"{label}: {a.message} (lepton check)")


def import_mkconf(rs: Rootstock, seed_root: Path, project: str, reference: str) -> str:
    """O5 : copie du XML de référence `reference` (relatif au trunk) et de ses `<file src_file>` dans
    le greffon projet, `src_file` réécrits ; greffe ; rend le chemin du XML du projet (trunk).
    Chemin absolu admis sous le trunk (désigné dans l'explorateur, F7 d'ENV-12), ramené au trunk."""
    if Path(reference).is_absolute():
        try:
            reference = str(Path(reference).relative_to(rs.trunk))
        except ValueError:
            raise LeptonError(f"XML « {reference} » hors du trunk {rs.trunk}",
                              "désigner le XML par le trunk (lien greffé), pas par le clone") from None
    ref = rs.trunk / reference
    if not ref.is_file():
        raise LeptonError(f"XML « {reference} » absent du trunk greffé",
                          "donner le chemin, relatif au trunk, d'un XML mklepton fourni par un greffon")
    text = mkconf.read(ref)
    target_rel = mkconf.project_xml(project)
    copies = mkconf.project_copies(text, project)
    stem = project_stem(seed_root)
    plan = [(ref, target_rel)] + [(rs.trunk / src, dest) for src, dest in copies.items()]
    for source, dest in plan:
        if (stem / dest).exists():
            raise LeptonError(f"{stem / dest} existe déjà : XML du projet déjà présent dans la graine",
                              "le modifier en place (lepton seed status : champ XML)")
        if (rs.trunk / dest).exists() or (rs.trunk / dest).is_symlink():
            raise LeptonError(f"{rs.trunk / dest} fourni par un autre greffon : conflit avec le XML du projet",
                              f"nom de projet distinct des répertoires de sys/user/ ({mkconf.project_etc(project)})")
        if not source.is_file():
            raise LeptonError(f"XML « {reference} » : src_file « {source.relative_to(rs.trunk)} » absent du trunk",
                              "corriger le XML de référence")
    for source, dest in plan[1:]:
        (stem / dest).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, stem / dest)
        shutil.copymode(source, stem / dest)
    (stem / target_rel).parent.mkdir(parents=True, exist_ok=True)
    (stem / target_rel).write_text(mkconf.rewrite_src_files(text, copies), encoding="utf-8")
    _validate_project_xml(stem / target_rel, target_rel)
    graft_project(rs, seed_root, project)
    _info(f"XML du projet : {target_rel} (copie de {reference}"
          + (f", avec {', '.join(Path(d).name for d in copies.values())}" if copies else "") + ")")
    return target_rel


def declare_application(rs: Rootstock, graine: dict, name: str, add: bool) -> bool:
    """O5 : `<bin>` de l'application `name` ajouté au XML du projet ou retiré ; XML hors du greffon
    projet (graine non migrée) : rien n'est écrit. Rend vrai si le XML a changé."""
    rel = graine["mklepton_xml"]
    xml = in_project(rs, rs.seed_root(), rel)
    bin_name = c_identifier(name)
    if xml is None:
        _warn(f"{rel} hors du greffon du projet : <bin name=\"{bin_name}\"> non {'déclaré' if add else 'retiré'} "
              f"(lepton seed mkconf import {rel})")
        return False
    text = mkconf.read(xml)
    new = mkconf.add_bin(text, bin_name) if add else mkconf.remove_bin(text, bin_name)
    if new is None:
        return False
    xml.write_text(new, encoding="utf-8")
    _validate_project_xml(xml, rel)
    _info(f"XML du projet : <bin name=\"{bin_name}\"> {'déclaré' if add else 'retiré'} ({rel})")
    return True


def seed_mkconf_import(args) -> int:
    """Migration d'une graine (O5) : XML du projet copié depuis `PATH`, applications déclarées."""
    rs, seed_root, graine_path, graine = _seed_context(args)
    project = graine["projet"]["nom"]
    if in_project(rs, seed_root, graine["mklepton_xml"]) is not None:
        raise LeptonError(f"XML de la graine déjà fourni par le greffon du projet ({graine['mklepton_xml']})",
                          "le modifier en place")
    graine["mklepton_xml"] = import_mkconf(rs, seed_root, project, args.path)
    save_graine(graine_path, graine)
    for app in graine.get("applications", []):
        declare_application(rs, graine, app, add=True)
    finish(rs, no_cmake=True)
    _info(f"presets à régénérer (LEPTON_MKCONF) : lepton generate -C {rs.path}")
    _remind_commit(seed_root)
    return EXIT_OK


# --------------------------------------------------------------------------
# seed new (GRA-1, GRA-2, GRA-3)
# --------------------------------------------------------------------------
def seed_new(args) -> int:
    name, bsp_name = args.name, args.bsp
    for label, value in (("NAME", name), ("--bsp", bsp_name)):
        if not _IDENT.match(value):
            raise LeptonError(f"{label} « {value} » invalide", "minuscules, chiffres, « . », « _ », « - »")
    # Manifeste de graine contrôlé avant toute action (nom, XML mklepton, backend)
    probe = validate_data(json.loads(render_text(
        (templates_dir() / "seed" / GRAINE_REL).read_text(encoding="utf-8"),
        graine_values(name, bsp_name, args.backend, args.mkconf,
                      [{"nom": "debug-qemu", "construction": "Debug", "execution": "qemu"}]),
        json_file=True)), "seed", SEED_MANIFEST)
    if probe:
        raise LeptonError("graine refusée :\n" + "\n".join(f"  {a.location}: {a.message}" for a in probe),
                          "corriger NAME, --bsp, --backend ou --mkconf (chemin relatif au trunk)")

    origins = dict(parse_origin_option(o) for o in args.origin or [])
    if len(origins) != len(args.origin or []):
        raise LeptonError("--origin donné deux fois pour le même greffon", "une origine par greffon")
    kernel_text = origins.pop(KERNEL_NAME, DEFAULT_KERNEL_ORIGIN)
    if bsp_name not in origins:
        raise LeptonError(f"origine du BSP « {bsp_name} » absente", f"--origin {bsp_name}=LOCATION[@VERSION][:PATH]")
    bsp_text = origins.pop(bsp_name)
    if len(origins) != 1:
        raise LeptonError("une et une seule origine de greffon famille attendue en plus du noyau et du BSP "
                          f"(reçu : {', '.join(origins) or 'aucune'})",
                          "--origin <famille du BSP>=LOCATION[@VERSION][:PATH]")
    family_name, family_text = next(iter(origins.items()))

    root = Path(args.rootstock or ".").resolve()
    if root.exists() and (not root.is_dir() or any(root.iterdir())):
        raise LeptonError(f"{root} existe et n'est pas un répertoire vide", "choisir un répertoire absent ou vide (-C DIR)")
    seed_repo = Path(args.seed_repo).resolve() if args.seed_repo else root / "depots" / "lepton-seed" / name
    if seed_repo.exists() and (not seed_repo.is_dir() or any(seed_repo.iterdir())):
        raise LeptonError(f"{seed_repo} existe et n'est pas vide", "choisir un autre --seed-repo")
    kernel = parse_location(kernel_text, rootstock=root)
    family = parse_location(family_text, rootstock=root)
    bsp = parse_location(bsp_text, rootstock=root)

    # 1. rootstock ; 2. dépôt de la graine (modèle sans manifeste) ; 3. déclaration des greffons
    root.mkdir(parents=True, exist_ok=True)
    scion("rootstock-install", cwd=root)
    values = graine_values(name, bsp_name, args.backend, args.mkconf, [])
    render_tree("seed", seed_repo, values, exclude={GRAINE_REL})
    git(seed_repo, "init", "-q")
    for key, origin in ((KERNEL_KEY, kernel), (scion_key("famille", family_name), family),
                        (scion_key("bsp", bsp_name), bsp)):
        scion("seed-scion-add", "--seed", str(seed_repo), key, *origin.scion_args(), cwd=root)

    # 4. clonage et greffe
    scion("seed-add", str(seed_repo), str(root), cwd=root)
    scion("graft", cwd=root)
    rs = Rootstock(root)
    left = (f"état laissé : rootstock {root} greffé, graine {seed_repo} non commitée sans {SEED_MANIFEST}")

    # 5. contrôles des manifestes (GRA-2, cœur et backend)
    try:
        k = _expect(rs, KERNEL_KEY, KERNEL_NAME, "noyau")
        b = _expect(rs, scion_key("bsp", bsp_name), bsp_name, "bsp")
        f = _expect(rs, scion_key("famille", family_name), family_name, "famille")
        if b.data.get("famille") != family_name:
            raise LeptonError(f"le BSP {bsp_name} déclare la famille « {b.data.get('famille')} », "
                              f"origine donnée pour « {family_name} »",
                              f"--origin {b.data.get('famille')}=LOCATION")
        core = b.data.get("coeur")
        for owner in (k, f):
            if core not in owner.data.get("coeurs", []):
                raise LeptonError(f"cœur « {core} » du BSP absent des cœurs de {owner.name} "
                                  f"({', '.join(owner.data.get('coeurs', []))})", "choisir un BSP compatible")
        if args.backend not in k.data.get("backends", []):
            raise LeptonError(f"backend « {args.backend} » non fourni par le noyau "
                              f"({', '.join(k.data.get('backends', []))})", "--backend embos|freertos")
        if not (rs.trunk / args.mkconf).exists():
            raise LeptonError(f"--mkconf « {args.mkconf} » absent du trunk greffé",
                              "donner le chemin, relatif au trunk, d'un XML mklepton fourni par un greffon")
        # 6. XML du projet (O5) : copie du XML de référence dans le greffon local du projet
        xml = import_mkconf(rs, seed_repo, name, args.mkconf)
    except LeptonError as e:
        e.action = f"{e.action} ; {left}"
        raise

    # 7. manifeste de graine, commit initial du dépôt de la graine
    render_tree("seed", seed_repo, dict(values, configurations=configurations_for(b), mkconf=xml),
                only={GRAINE_REL})
    finish(rs, no_cmake=True)
    git(seed_repo, "add", "-A")
    git(seed_repo, "commit", "-q", "-m", f"Graine {name} créée par lepton seed new")

    _info(f"rootstock : {root}")
    _info(f"graine    : {seed_repo}")
    for label, key, o in (("noyau", KERNEL_KEY, kernel), ("famille", scion_key("famille", family_name), family),
                          ("bsp", scion_key("bsp", bsp_name), bsp)):
        _info(f"  {label:8} {key:32} {o.version:8} {o.location}{(':' + o.subpath) if o.subpath else ''}")
    _info(f"presets et espace de travail VSCodium : lepton generate -C {root}")
    return EXIT_OK


# --------------------------------------------------------------------------
# seed status (GRA-6)
# --------------------------------------------------------------------------
def _git_state(clone: Path) -> dict:
    state = {"branch": None, "commit": None, "dirty": None, "dirty_files": [], "ahead": None, "behind": None}
    if run(["git", "-C", str(clone), "rev-parse", "--is-inside-work-tree"], check=False).returncode != 0:
        return state
    state["branch"] = git(clone, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    state["commit"] = git(clone, "rev-parse", "--short", "HEAD").stdout.strip()
    files = [l[3:] for l in git(clone, "status", "--porcelain", "--", ".").stdout.splitlines()
             if not is_system_file(Path(l[3:].strip('"').rstrip("/")).name)]
    state["dirty"], state["dirty_files"] = len(files), files
    res = run(["git", "-C", str(clone), "rev-list", "--left-right", "--count", "@{u}...HEAD"], check=False)
    if res.returncode == 0 and len(res.stdout.split()) == 2:
        state["behind"], state["ahead"] = (int(x) for x in res.stdout.split())
    return state


def status_data(rs: Rootstock) -> tuple[dict, dict | None, dict, list[str], TrunkReport]:
    """État de la graine (GRA-6) : résultat JSON de `seed status`, graine, rôles, greffons absents et
    contrôle du trunk ; partagé avec `seed tree` (vue IDE-1 cohérente avec seed status)."""
    seed_dot = rs.seed_dot()
    graine_path = seed_dot / SEED_MANIFEST
    graine = load_graine(graine_path) if graine_path.exists() else None
    sources = {s.key: s for s in rs.sources()}
    manifests = rs.manifests()
    roles = {}
    project = project_key(graine["projet"]["nom"]) if graine else None
    if graine:
        roles[graine["noyau"]] = "noyau"
        roles[graine["bsp"]] = "bsp"
        bsp_m = next((m for m in manifests.values() if m.name == graine["bsp"]), None)
        if bsp_m and bsp_m.data.get("famille"):
            roles[bsp_m.data["famille"]] = "famille"
        roles.update({n: "application" for n in graine.get("applications", [])})
        roles.update({n: "bibliotheque" for n in graine.get("bibliotheques", [])})

    scions = []
    for e in rs.grafted():
        m = manifests.get(e.key)
        name = m.name if m else e.name
        src = sources.get(e.key)
        role = roles.get(name) if m else ("projet" if e.key == project else "sans manifeste")
        if role is None:
            # déclaré dans .scion.sources.list sans rôle dans lepton-graine.json (ex. ancien BSP)
            role = ("non utilisé" if src else "hors graine") if graine else (m.kind or "?")
        scions.append({"name": name, "role": role, "key": e.key,
                       "version": src.version if src else e.version,
                       "location": src.location if src else None,
                       "path": str(rs.clone(e)),
                       "stem": str((rs.clone(e) / STEM_DIR).resolve()),
                       "in_seed": src is not None,
                       **_git_state(rs.clone(e))})
    grafted_names = {s["name"] for s in scions}
    missing = sorted(n for n in roles if n not in grafted_names)
    report = rs.check_trunk()
    seed_state = {"path": str(rs.seed_root()), "manifest": str(graine_path) if graine else None,
                  **_git_state(rs.seed_root())}
    # configurations de la graine (F7 d'ENV-12 : choix de `seed config remove` dans la palette)
    configurations = [{"name": c["nom"], "build_type": c["construction"], "run": c["execution"],
                       "preset": f"{graine['projet']['nom']}-{c['nom']}"}
                      for c in graine.get("configurations", [])] if graine else []
    result = {"rootstock": str(rs.path), "trunk": str(rs.trunk), "seed": seed_state, "scions": scions,
              "configurations": configurations, "missing": missing,
              "trunk_check": {"regular_files": [str(p) for p in report.regular_files],
                              "broken_links": [str(p) for p in report.broken_links]}}
    return result, graine, roles, missing, report


def seed_status(args) -> int:
    rs = Rootstock.discover(args.rootstock)
    result, graine, roles, missing, report = status_data(rs)
    seed_state, scions = result["seed"], result["scions"]
    coherent = report.clean and not missing

    if args.json:
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return EXIT_OK if coherent else EXIT_USER

    _info(f"rootstock : {rs.path}")
    _info(f"graine    : {seed_state['path']}  {_fmt_git(seed_state)}")
    if graine is None:
        _info(f"            {SEED_MANIFEST} absent : rôles non déterminés (graine hors lepton)")
    else:
        _info(f"            projet {graine['projet']['nom']} {graine['projet']['version']}, "
              f"backend {graine['backend']}, XML {graine['mklepton_xml']}")
        _info("            configurations : " + ", ".join(
            f"{c['name']} ({c['build_type']}, {c['run']})" for c in result["configurations"]))
    # largeurs d'après le contenu (O17 : version ou branche longue, `devenv/env-6-r3`)
    width = max([len(s["name"]) for s in scions] + [7])
    vwidth = max([len(s["version"]) for s in scions] + [8])
    bwidth = max([len(s["branch"] or "") for s in scions] + [16])
    _info(f"{'greffon':{width}}  {'rôle':14} {'version':{vwidth}} {'branche':{bwidth}} {'commit':9} modif.  origine")
    for s in scions:
        _info(f"{s['name']:{width}}  {s['role']:14} {s['version']:{vwidth}} {_fmt_git(s, bwidth)}  "
              f"{s['location'] or '(hors graine)'}")
        if args.verbose:
            for f in s["dirty_files"]:
                _info(f"{'':{width}}    modifié : {f}")
    for n in missing:
        _info(f"absent du trunk : {n} ({roles[n]})")
    if report.clean:
        _info("trunk : aucun fichier régulier, aucun lien cassé")
    else:
        for p in report.regular_files:
            _info(f"trunk : fichier régulier {p}")
        for p in report.broken_links:
            _info(f"trunk : lien cassé {p}")
    return EXIT_OK if coherent else EXIT_USER


def _fmt_git(s: dict, bwidth: int = 16) -> str:
    if s["commit"] is None:
        return f"{'(hors git)':{bwidth}} {'':9} {'':6}"
    sync = ""
    if s["ahead"] or s["behind"]:
        sync = f" +{s['ahead']}/-{s['behind']}"
    return f"{s['branch']:{bwidth}} {s['commit']:9} {s['dirty']:<6}{sync}"


# --------------------------------------------------------------------------
# seed add / remove / replace (GRA-3, GRA-4)
# --------------------------------------------------------------------------
def _seed_context(args) -> tuple[Rootstock, Path, Path, dict]:
    rs = Rootstock.discover(args.rootstock)
    seed_root = rs.seed_root()
    graine_path = rs.seed_manifest_path()
    return rs, seed_root, graine_path, load_graine(graine_path)


def _remind_commit(seed_root: Path) -> None:
    _info(f"graine modifiée, non commitée : git -C {seed_root} commit -am \"…\"")


def check_new_scion(rs: Rootstock, name: str, kind: str) -> str:
    """Nom valide, ni greffé ni déclaré dans la graine ; rend la clé scion."""
    if not _IDENT.match(name):
        raise LeptonError(f"SCION « {name} » invalide", "minuscules, chiffres, « . », « _ », « - »")
    if rs.key_of(name) is not None:
        raise LeptonError(f"greffon « {name} » déjà greffé", f"lepton seed replace {name} LOCATION")
    key = scion_key(kind, name)
    if key in {s.key for s in rs.sources()}:
        raise LeptonError(f"{key} déjà déclaré dans la graine sans être greffé",
                          f"lepton seed remove {name}, ou scion seed-scion-remove --seed {rs.seed_root()} {key}")
    return key


def seed_add(args) -> int:
    rs = Rootstock.discover(args.rootstock)
    origin = parse_location(args.location, args.version, args.path, rootstock=rs.path)
    return add_scion(rs, args.scion, args.type, origin, args.no_cmake)


def add_scion(rs: Rootstock, name: str, kind: str, origin: Origin, no_cmake: bool) -> int:
    """Ajout d'un greffon à la graine (GRA-4) : `seed-scion-add` → `seed-clone` → `graft --scion`."""
    seed_root, graine_path = rs.seed_root(), rs.seed_manifest_path()
    graine = load_graine(graine_path)
    key = check_new_scion(rs, name, kind)

    scion("seed-scion-add", "--seed", str(seed_root), key, *origin.scion_args(), cwd=rs.path)
    try:
        scion("seed-clone", "--seed", str(seed_root), cwd=rs.path)
        _expect(rs, key, name, kind)
        scion_on_trunk(rs, "graft", "--scion", key)
    except LeptonError:
        _undo_add(rs, seed_root, key)
        raise

    if kind == "application":
        graine.setdefault("applications", []).append(name)
    elif kind == "bibliotheque":
        graine.setdefault("bibliotheques", []).append(name)
    elif kind == "bsp":
        _warn(f"BSP de la graine : {graine['bsp']} → {name} ; {graine['bsp']} reste greffé "
              f"(lepton seed remove {graine['bsp']} pour le retirer)")
        graine["bsp"] = name
    save_graine(graine_path, graine)
    _info(f"{name} ajouté ({key}, {origin.version}, {origin.location})")
    if kind == "application":
        declare_application(rs, graine, name, add=True)
    finish(rs, no_cmake)
    _remind_commit(seed_root)
    return EXIT_OK


def _undo_add(rs: Rootstock, seed_root: Path, key: str) -> None:
    """Annulation d'un ajout : retrait de la graine et du trunk (le clone éventuel est conservé)."""
    try:
        if key in {e.key for e in rs.grafted()}:
            scion_on_trunk(rs, "graft-remove", key)
        scion("seed-scion-remove", "--seed", str(seed_root), key, cwd=rs.path)
        _warn(f"ajout de {key} annulé (graine et trunk restaurés)")
    except LeptonError as e:
        _warn(f"annulation incomplète de {key} : {e.message}")


def seed_remove(args) -> int:
    rs, seed_root, graine_path, graine = _seed_context(args)
    name = args.scion
    key = rs.key_of(name)
    if key is None:
        raise LeptonError(f"greffon « {name} » non greffé", "lepton seed status")
    if name == graine["noyau"] or name == graine["bsp"]:
        raise LeptonError(f"« {name} » est le {'noyau' if name == graine['noyau'] else 'BSP'} de la graine, "
                          "obligatoire (GRA-2)", "lepton seed replace pour en changer l'origine")
    bsp_key = rs.key_of(graine["bsp"])
    bsp_m = _manifest_of(rs, bsp_key) if bsp_key else None
    if bsp_m is not None and bsp_m.data.get("famille") == name:
        raise LeptonError(f"« {name} » est la famille du BSP {graine['bsp']}", "changer de BSP avant de la retirer")

    unprovided = removal_unprovided(rs, graine, key)    # avant retrait : fichiers encore greffés
    if key in {s.key for s in rs.sources()}:
        scion("seed-scion-remove", "--seed", str(seed_root), key, cwd=rs.path)
    else:
        _warn(f"{key} greffé hors de la graine : retiré du trunk seulement")
    scion_on_trunk(rs, "graft-remove", key, *(["--purge"] if args.purge else []))

    application = name in graine.get("applications", [])
    for field in ("applications", "bibliotheques"):
        if name in graine.get(field, []):
            graine[field].remove(name)
    save_graine(graine_path, graine)
    _info(f"{name} retiré ({key})")
    if application and declare_application(rs, graine, name, add=False):
        # déclaration retirée du XML du projet (O5) : plus d'anomalie CFG-5 pour ce binaire
        unprovided = [a for a in unprovided if a.location != f"binaries/bin[@name='{c_identifier(name)}']"]
    for a in unprovided:
        _warn(f"{a.file}: {a.location} : fourni seulement par {name}, sans fournisseur désormais (CFG-5) ; "
              "retirer la déclaration du XML avant de construire (lepton check)")
    finish(rs, args.no_cmake)
    _remind_commit(seed_root)
    return EXIT_OK


def seed_replace(args) -> int:
    rs, seed_root, _, _ = _seed_context(args)
    name = args.scion
    key = rs.key_of(name)
    old = {s.key: s for s in rs.sources()}.get(key) if key else None
    if old is None:
        raise LeptonError(f"greffon « {name} » absent de la graine ou non greffé", "lepton seed status")
    kind = _manifest_of(rs, key).kind
    origin = parse_location(args.location, args.version, args.path, rootstock=rs.path)
    old_origin = Origin(old.location, old.version, old.subpath)

    # retrait d'abord (clone distant supprimé : la nouvelle origine est reclonée au même endroit)
    scion_on_trunk(rs, "graft-remove", key, *(["--purge"] if old_origin.remote else []))
    try:
        _attach(rs, seed_root, key, origin)
        _expect(rs, key, name, kind)
        scion_on_trunk(rs, "graft", "--scion", key)
    except LeptonError:
        try:
            if key in {e.key for e in rs.grafted()}:
                scion_on_trunk(rs, "graft-remove", key, *(["--purge"] if origin.remote else []))
            _attach(rs, seed_root, key, old_origin)
            scion_on_trunk(rs, "graft", "--scion", key)
            _warn(f"remplacement de {name} annulé : origine précédente restaurée")
        except LeptonError as e:
            _warn(f"restauration de {name} incomplète : {e.message}")
        raise
    _info(f"{name} remplacé ({key} : {old.version} {old.location} → {origin.version} {origin.location})")
    finish(rs, args.no_cmake)
    _remind_commit(seed_root)
    return EXIT_OK


def _attach(rs: Rootstock, seed_root: Path, key: str, origin: Origin) -> None:
    scion("seed-scion-add", "--replace", "--seed", str(seed_root), key, *origin.scion_args(), cwd=rs.path)
    scion("seed-clone", "--seed", str(seed_root), cwd=rs.path)


# --------------------------------------------------------------------------
# seed lock (GRA-5, P2 ; interface §3.5, décision S4-1)
# --------------------------------------------------------------------------
LOCK_FILE = "lepton-graine.lock.json"


def _locked_entries(rs: Rootstock) -> list[dict]:
    """Greffons de la graine : origine, version demandée, commit exact ; refus si clone modifié."""
    grafted = {e.key: e for e in rs.grafted()}
    names = {key: m.name for key, m in rs.manifests().items()}
    entries, refused = [], []
    graine = rs.seed_manifest_path()
    project = project_key(load_graine(graine)["projet"]["nom"]) if graine.exists() else None
    for s in rs.sources():
        if s.key == project:
            continue                       # greffon du projet = dépôt de la graine elle-même (ENV-9)
        e = grafted.get(s.key)
        if e is None:
            refused.append(f"  {s.key} : déclaré dans la graine, non greffé")
            continue
        state = _git_state(rs.clone(e))
        entry = {"key": s.key, "name": names.get(s.key, s.name), "location": s.location,
                 "version": s.version, "path": s.subpath, "commit": None}
        if state["commit"] is None and not Origin(s.location, s.version).remote:
            entries.append(entry)          # répertoire local hors git (ex. building) : rien à figer
        elif state["commit"] is None:
            refused.append(f"  {s.key} : {rs.clone(e)} n'est pas un dépôt git")
        elif state["dirty"]:
            refused.append(f"  {s.key} : {state['dirty']} fichier(s) modifié(s) non commité(s) dans {rs.clone(e)}")
        else:
            entries.append(dict(entry, commit=git(rs.clone(e), "rev-parse", "HEAD").stdout.strip()))
    if refused:
        raise LeptonError("graine non figeable :\n" + "\n".join(refused),
                          "commiter dans chaque clone (lepton seed status -v), puis lepton seed lock")
    return entries


def _lock_gaps(rs: Rootstock, locked: list[dict]) -> list[str]:
    """Écarts entre les clones et le verrou (`--verify`)."""
    grafted = {e.key: e for e in rs.grafted()}
    graine = rs.seed_manifest_path()
    project = project_key(load_graine(graine)["projet"]["nom"]) if graine.exists() else None
    declared = {s.key for s in rs.sources()} - {project}
    gaps = []
    for entry in locked:
        e = grafted.get(entry["key"])
        if e is None:
            gaps.append(f"{entry['name']} ({entry['key']}) : figé, non greffé")
            continue
        if entry["commit"] is None:
            continue
        state = _git_state(rs.clone(e))
        head = git(rs.clone(e), "rev-parse", "HEAD").stdout.strip() if state["commit"] else None
        if head != entry["commit"]:
            gaps.append(f"{entry['name']} : commit {head[:12] if head else '(hors git)'}, figé {entry['commit'][:12]}")
        if state["dirty"]:
            gaps.append(f"{entry['name']} : {state['dirty']} fichier(s) modifié(s) non commité(s)")
    for key in sorted(declared - {entry["key"] for entry in locked}):
        gaps.append(f"{key} : déclaré dans la graine, absent du verrou")
    return gaps


def _load_lock(path: Path) -> list[dict]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return list(data["scions"])
    except FileNotFoundError:
        raise LeptonError(f"{path} absent", "lepton seed lock") from None
    except (ValueError, KeyError, TypeError) as e:
        raise LeptonError(f"{path} : verrou illisible ({e})", "lepton seed lock pour le réécrire") from e


def seed_lock(args) -> int:
    rs = Rootstock.discover(args.rootstock)
    lock_path = rs.seed_dot() / LOCK_FILE
    if args.verify:
        gaps = _lock_gaps(rs, _load_lock(lock_path))
        for g in gaps:
            _info(f"écart : {g}")
        if not gaps:
            _info(f"clones conformes au verrou {lock_path}")
        return EXIT_USER if gaps else EXIT_OK
    if args.restore:
        return _restore(rs, _load_lock(lock_path), args.no_cmake)

    entries = _locked_entries(rs)
    lock_path.write_text(json.dumps({"lepton": __version__, "scions": entries}, ensure_ascii=False, indent=2)
                         + "\n", encoding="utf-8")
    for entry in entries:
        commit = entry["commit"][:12] if entry["commit"] else "(hors git)"
        _info(f"  {entry['name']:24} {commit:12}  {entry['version']:8} {entry['location']}")
    _info(f"verrou écrit : {lock_path}")
    _remind_commit(rs.seed_root())
    return EXIT_OK


def _restore(rs: Rootstock, locked: list[dict], no_cmake: bool) -> int:
    """Clones d'origine distante remis au commit figé ; origine locale (`*`) signalée, jamais modifiée."""
    grafted = {e.key: e for e in rs.grafted()}
    moved, local_gaps, refused = [], [], []
    for entry in locked:
        e = grafted.get(entry["key"])
        if e is None:
            refused.append(f"  {entry['name']} : non greffé (lepton seed status)")
            continue
        clone = rs.clone(e)
        if entry["commit"] is None:
            continue
        head = git(clone, "rev-parse", "HEAD").stdout.strip()
        if head == entry["commit"]:
            continue
        if not Origin(entry["location"], entry["version"]).remote:
            local_gaps.append(f"  {entry['name']} : origine locale {clone} au commit {head[:12]}, "
                              f"figé {entry['commit'][:12]} (non modifiée)")
            continue
        if _git_state(clone)["dirty"]:
            refused.append(f"  {entry['name']} : modifications non commitées dans {clone}")
            continue
        if run(["git", "-C", str(clone), "cat-file", "-e", f"{entry['commit']}^{{commit}}"], check=False).returncode:
            refused.append(f"  {entry['name']} : commit {entry['commit'][:12]} absent de {clone} "
                           f"(git -C {clone} fetch)")
            continue
        moved.append((entry, clone))
    if refused:
        raise LeptonError("restauration refusée, aucun clone modifié :\n" + "\n".join(refused),
                          "corriger chaque greffon, puis lepton seed lock --restore")
    for entry, clone in moved:
        git(clone, "checkout", "-q", entry["commit"])
        _info(f"{entry['name']} : {entry['commit'][:12]} (HEAD détachée)")
    if moved:
        scion_on_trunk(rs, "graft")
        finish(rs, no_cmake)
    for g in local_gaps:
        _warn(g.strip())
    if not moved and not local_gaps:
        _info("clones déjà au commit du verrou")
    return EXIT_USER if local_gaps else EXIT_OK
