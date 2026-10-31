"""Contrôles d'un rootstock : `lepton check` sans argument (interface §3.9, jalon 6).

Graine et manifestes greffés validés par leurs schémas, puis contrôles non exprimables en JSON
Schema, GRA-2, GRF-5 (P2) et CFG-5 (P2). Lecture seule ; une anomalie par constat.

CFG-5 (décision S4-2) : recherche textuelle des définitions `dev_map_t dev_X_map =` (pilote) et
`int X_main(` (binaire) dans les fichiers .c des greffons greffés, sans construction. Fichiers
d'un greffon : ceux de ses `sources` (répertoire non récursif, comme le lecteur CMake) et ses
fichiers objets (`demarrage`, `vecteurs`, `remplacants_forts`) ; sans `sources` (noyau, compilé
par ses composants) ou avec un `CMakeLists.txt` à sa destination : tout l'arbre de sa destination.
Une définition dans une macro par collage de lexèmes (`dev_cmsdk_uart_##n##_map`) vaut motif.

Graine de référence (PA-19 C, ENV-16) : ni `lepton-graine.json` ni greffon local de projet ; les
contrôles de graine sont déduits des greffons greffés et des presets du noyau.
"""

import json
import re
import xml.etree.ElementTree as ET
from dataclasses import replace
from pathlib import Path

from lepton.errors import EXIT_TOOL, LeptonError
from lepton.rootstock import PROJECT_SUBPATH, SOURCE_ROOT, STEM_DIR, Manifest, Rootstock
from lepton.validation import Anomaly, locate, validate_data, validate_json, validate_xml

KERNEL_PRESETS = "CMakePresets.json"   # presets du greffon noyau, à la racine du trunk
# Champs de manifeste qui désignent des fichiers relatifs à la destination
FILE_FIELDS = ("vecteurs", "remplacants_forts", "demarrage", "openocd")
SINGLE_FILE_FIELDS = ("script_liens", "entete_config_noyau", "svd")
OBJECT_FIELDS = ("demarrage", "vecteurs", "remplacants_forts")
# Caractères qu'une définition de compilation ne transmet pas (O16) : séparateur de liste CMake,
# « # » (définition retirée par CMake), fin de ligne ; « " » et « \ » sont échappés par le lecteur
UNSENDABLE = ";#\n\r"

_DEV_DEF = re.compile(r"^[ \t]*(?:static[ \t]+)?(?:const[ \t]+)?dev_map_t[ \t]+(dev_[\w#]+_map)[ \t]*=", re.M)
_BIN_DEF = re.compile(r"^[ \t]*int[ \t]+(\w+)_main[ \t]*\([^;{)]*\)[ \t]*(?:\{|$)", re.M)


def _rel(rs: Rootstock, path: Path) -> str:
    """Chemin affiché : relatif au rootstock s'il y est, absolu sinon (origine locale en place)."""
    try:
        return str(path.relative_to(rs.path))
    except ValueError:
        return str(path)


# --------------------------------------------------------------------------
# contrôles d'un manifeste de greffon (non exprimables en JSON Schema)
# --------------------------------------------------------------------------
def check_options(m: Manifest, label: str) -> list[Anomaly]:
    found, seen = [], set()
    for i, opt in enumerate(m.data.get("options", [])):
        if not isinstance(opt, dict):
            continue
        where, name, default = f"/options/{i}", opt.get("nom"), opt.get("defaut")
        if name in seen:
            found.append(Anomaly(label, f"{where}/nom", f"option « {name} » déclarée deux fois"))
        seen.add(name)
        if opt.get("type") == "entier" and isinstance(default, int):
            lo, hi = opt.get("min"), opt.get("max")
            if isinstance(lo, int) and isinstance(hi, int) and lo > hi:
                found.append(Anomaly(label, where, f"bornes inversées : min {lo} > max {hi}"))
            elif isinstance(lo, int) and isinstance(hi, int) and not lo <= default <= hi:
                found.append(Anomaly(label, f"{where}/defaut", f"défaut {default} hors des bornes [{lo}, {hi}]"))
        if opt.get("type") == "enumeration" and isinstance(opt.get("valeurs"), list) \
                and default not in opt["valeurs"]:
            found.append(Anomaly(label, f"{where}/defaut",
                                 f"défaut « {default} » absent des valeurs ({', '.join(opt['valeurs'])})"))
    return found


def check_declared_files(m: Manifest, label: str) -> list[Anomaly]:
    """Fichiers et répertoires déclarés présents dans le clone (relatifs à la destination)."""
    base, found = m.path.parent, []
    for i, rel in enumerate(m.data.get("sources", [])):
        if isinstance(rel, str) and not (base / rel).exists():
            found.append(Anomaly(label, f"/sources/{i}", f"« {rel} » introuvable dans {base}"))
    for field in FILE_FIELDS:
        for i, rel in enumerate(m.data.get(field, [])):
            if isinstance(rel, str) and not (base / rel).is_file():
                found.append(Anomaly(label, f"/{field}/{i}", f"fichier « {rel} » introuvable dans {base}"))
    for field in SINGLE_FILE_FIELDS:
        rel = m.data.get(field)
        if isinstance(rel, str) and not (base / rel).is_file():
            found.append(Anomaly(label, f"/{field}", f"fichier « {rel} » introuvable dans {base}"))
    return found


# --------------------------------------------------------------------------
# contrôles de la graine : GRA-2, GRF-5
# --------------------------------------------------------------------------
def check_seed(graine: dict, by_name: dict[str, Manifest], label: str) -> list[Anomaly]:
    found = []

    def role(field: str, name: str, kind: str, where: str) -> Manifest | None:
        m = by_name.get(name)
        if m is None:
            found.append(Anomaly(label, where, f"{field} « {name} » non greffé (GRA-2)"))
        elif m.kind != kind:
            found.append(Anomaly(label, where, f"« {name} » est de type « {m.kind} », attendu « {kind} »"))
            return None
        return m

    names = [c.get("nom") for c in graine.get("configurations", []) if isinstance(c, dict)]
    for i, n in enumerate(names):
        if n in names[:i]:
            found.append(Anomaly(label, f"/configurations/{i}/nom", f"configuration « {n} » déclarée deux fois"))

    kernel = role("noyau", graine.get("noyau"), "noyau", "/noyau")
    bsp = role("BSP", graine.get("bsp"), "bsp", "/bsp")
    for field, kind in (("applications", "application"), ("bibliotheques", "bibliotheque")):
        for i, n in enumerate(graine.get(field, [])):
            role(kind, n, kind, f"/{field}/{i}")
    if bsp is not None:
        found.extend(Anomaly(label, "/bsp", message) for _, message in check_bsp(bsp, kernel, by_name))
        for i, conf in enumerate(graine.get("configurations", [])):
            mode = conf.get("execution") if isinstance(conf, dict) else None
            if mode == "qemu" and "qemu" not in bsp.data:
                found.append(Anomaly(label, f"/configurations/{i}/execution",
                                     f"exécution qemu : le BSP {bsp.name} ne déclare pas « qemu »"))
            if mode == "carte":
                missing = [f for f in ("openocd", "sonde") if f not in bsp.data]
                if missing:
                    found.append(Anomaly(label, f"/configurations/{i}/execution",
                                         f"exécution carte : le BSP {bsp.name} ne déclare pas {', '.join(missing)}"))

    # GRF-5 : backend (cœur : check_bsp)
    if kernel is not None and graine.get("backend") not in kernel.data.get("backends", []):
        found.append(Anomaly(label, "/backend", f"backend « {graine.get('backend')} » non fourni par "
                             f"{kernel.name} ({', '.join(kernel.data.get('backends', []))}) (GRF-5)"))
    found.extend(check_seed_options(graine, by_name, label))
    return found


def check_bsp(bsp: Manifest, kernel: Manifest | None, by_name: dict[str, Manifest]) -> list[tuple[str, str]]:
    """GRA-2, GRF-5 d'un BSP : famille greffée, cœur dans les cœurs de la famille et du noyau ;
    (champ du manifeste du BSP, message)."""
    found = []
    fam_name = bsp.data.get("famille")
    family = by_name.get(fam_name)
    if family is None:
        found.append(("/famille", f"famille « {fam_name} » du BSP {bsp.name} non greffée (GRA-2)"))
    elif family.kind != "famille":
        found.append(("/famille", f"famille « {fam_name} » du BSP de type « {family.kind} »"))
        family = None
    core = bsp.data.get("coeur")
    for owner in (kernel, family):
        if owner is not None and core not in owner.data.get("coeurs", []):
            found.append(("/coeur", f"cœur « {core} » du BSP {bsp.name} absent des cœurs de "
                          f"{owner.name} ({', '.join(owner.data.get('coeurs', []))}) (GRF-5)"))
    return found


def seed_scions(graine: dict, by_name: dict[str, Manifest]) -> set[str]:
    """Noms des greffons de la graine : noyau, BSP, famille du BSP, applications, bibliothèques."""
    names = {graine.get("noyau"), graine.get("bsp"), *graine.get("applications", []),
             *graine.get("bibliotheques", [])}
    bsp = by_name.get(graine.get("bsp"))
    if bsp is not None:
        names.add(bsp.data.get("famille"))
    return {n for n in names if isinstance(n, str)}


def _option_value_error(opt: dict, value) -> str | None:
    """Motif du refus d'une valeur de la graine pour l'option déclarée `opt` (CFG-4), sinon None."""
    kind = opt.get("type")
    if kind == "booleen":
        return None if isinstance(value, bool) else "booléen attendu"
    if kind == "entier":
        if not isinstance(value, int) or isinstance(value, bool):
            return "entier attendu"
        lo, hi = opt.get("min"), opt.get("max")
        if isinstance(lo, int) and isinstance(hi, int) and not lo <= value <= hi:
            return f"{value} hors des bornes [{lo}, {hi}]"
        return None
    if kind == "enumeration":
        if not isinstance(value, str):
            return "chaîne attendue (énumération)"
        allowed = opt.get("valeurs", [])
        return None if value in allowed else f"« {value} » absent des valeurs ({', '.join(allowed)})"
    if kind == "chaine":
        if not isinstance(value, str):
            return "chaîne attendue"
        bad = sorted({c for c in value if c in UNSENDABLE})
        return (f"caractère(s) {' '.join(repr(c) for c in bad)} non transmissible(s) par une définition de "
                "compilation (« ; », « # », saut de ligne)") if bad else None
    return None                     # type inconnu : signalé par le schéma du greffon


def check_seed_options(graine: dict, by_name: dict[str, Manifest], label: str) -> list[Anomaly]:
    """Valeurs d'options fixées par la graine (CFG-4, N5) contre les manifestes de leurs greffons."""
    options = graine.get("options", {})
    if not isinstance(options, dict):
        return [Anomaly(label, "/options", "objet attendu")]
    found, members = [], seed_scions(graine, by_name)
    for scion_name, values in options.items():
        where = f"/options/{scion_name}"
        if scion_name not in members:
            found.append(Anomaly(label, where, f"« {scion_name} » n'est pas un greffon de la graine"))
            continue
        if not isinstance(values, dict):
            found.append(Anomaly(label, where, "objet attendu (<NOM> → valeur)"))
            continue
        m = by_name.get(scion_name)
        if m is None:
            continue                # non greffé : signalé par GRA-2
        declared = {o.get("nom"): o for o in m.data.get("options", []) if isinstance(o, dict)}
        for name, value in values.items():
            opt = declared.get(name)
            if opt is None:
                found.append(Anomaly(label, f"{where}/{name}", f"option « {name} » non déclarée par {scion_name}"
                                     + (f" ({', '.join(declared)})" if declared else " (aucune option)")))
                continue
            error = _option_value_error(opt, value)
            if error:
                found.append(Anomaly(label, f"{where}/{name}", f"valeur refusée : {error}"))
    return found


def check_dependencies(manifests: dict[str, tuple[Manifest, str]]) -> list[Anomaly]:
    """GRF-5 : dépendances déclarées greffées ; noms de greffons uniques."""
    found, names = [], {}
    for m, label in manifests.values():
        if m.name in names:
            found.append(Anomaly(label, "/nom", f"nom « {m.name} » déjà porté par {names[m.name]}"))
        names.setdefault(m.name, label)
    for m, label in manifests.values():
        for i, dep in enumerate(m.data.get("dependances", [])):
            if dep not in names:
                found.append(Anomaly(label, f"/dependances/{i}", f"dépendance « {dep} » non greffée (GRF-5)"))
    return found


# --------------------------------------------------------------------------
# CFG-5 : pilotes et binaires du XML fournis par un greffon
# --------------------------------------------------------------------------
def scion_c_files(m: Manifest) -> list[Path]:
    base = m.path.parent
    sources = m.data.get("sources")
    if sources is None or (base / "CMakeLists.txt").is_file():
        return sorted(base.rglob("*.c"))
    files = []
    for rel in sources:
        p = base / rel
        if p.is_dir():
            files.extend(sorted(p.glob("*.c")))
        elif p.suffix == ".c":
            files.append(p)
    for field in OBJECT_FIELDS:
        files.extend(base / rel for rel in m.data.get(field, [])
                     if isinstance(rel, str) and rel.endswith(".c"))
    return files


def _pasted(name: str) -> re.Pattern:
    """Définition par collage de lexèmes dans une macro (`dev_cmsdk_uart_##n##_map`) : motif dont
    les paramètres de la macro valent `\\w+` (préfixe `dev_…` et suffixe `…_map` littéraux)."""
    parts = name.split("##")
    rx = [re.escape(p) if (i == 0 and p.startswith("dev_")) or (i == len(parts) - 1 and p.endswith("_map"))
          else r"\w+" for i, p in enumerate(parts)]
    return re.compile("".join(rx))


def provided_symbols(manifests: list[Manifest]) -> tuple[set[str], list[re.Pattern], set[str]]:
    """Pilotes définis (noms, motifs de macros) et binaires définis (`X` de `X_main`)."""
    devices, patterns, binaries = set(), [], set()
    for m in manifests:
        for f in scion_c_files(m):
            try:
                text = f.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for name in _DEV_DEF.findall(text):
                if "##" in name:
                    patterns.append(_pasted(name))
                else:
                    devices.add(name)
            binaries.update(_BIN_DEF.findall(text))
    return devices, patterns, binaries


def _xml_line(text: str, tag: str, name: str) -> int | None:
    """Ligne de la balise `<tag … name="name"` (diagnostics de l'éditeur ; ElementTree ne la donne pas)."""
    m = re.search(rf"<{tag}\b[^>]*\bname\s*=\s*[\"']{re.escape(name)}[\"']", text)
    return text.count("\n", 0, m.start()) + 1 if m else None


def check_mkconf_provided(xml: Path, label: str, manifests: list[Manifest]) -> list[Anomaly]:
    try:
        text = xml.read_text(encoding="utf-8", errors="replace")
        root = ET.fromstring(text)
    except (OSError, ET.ParseError) as e:
        return [Anomaly(label, "", f"XML illisible : {e}")]
    devices, patterns, binaries = provided_symbols(manifests)
    found = []
    for dev in root.iter("dev"):
        name = dev.get("name")
        if dev.get("use") == "on" and name not in devices and not any(p.fullmatch(name) for p in patterns):
            found.append(Anomaly(label, f"devices/dev[@name='{name}']",
                                 "pilote déclaré dans le XML, défini par aucun greffon greffé (CFG-5)",
                                 _xml_line(text, "dev", name)))
    for b in root.iter("bin"):
        name = b.get("name")
        if name not in binaries:
            found.append(Anomaly(label, f"binaries/bin[@name='{name}']",
                                 f"binaire déclaré dans le XML, {name}_main défini par aucun greffon greffé (CFG-5)",
                                 _xml_line(text, "bin", name)))
    return found


def removal_unprovided(rs: Rootstock, graine: dict, key: str) -> list[Anomaly]:
    """CFG-5 avant `seed remove` / `scion remove` (O4) : déclarations du XML de la graine que seul
    le greffon `key` fournit, donc sans fournisseur après son retrait."""
    rel = graine.get("mklepton_xml")
    xml = rs.trunk / rel if rel else None
    if xml is None or not xml.is_file():
        return []
    manifests = rs.manifests()
    label = _rel(rs, xml)
    before = {a.location for a in check_mkconf_provided(xml, label, list(manifests.values()))}
    after = check_mkconf_provided(xml, label, [m for k, m in manifests.items() if k != key])
    return [a for a in after if a.location not in before]


def _manifest_label(rs: Rootstock, m: Manifest) -> str:
    """Manifeste de greffon désigné par le trunk (seul chemin d'ouverture, PA-1, IDE-4 : la tâche
    « lepton : vérifier » de l'éditeur ouvre ce chemin) quand le lien y mène ; sinon par le clone."""
    parts, src = m.path.parts, (STEM_DIR, *Path(SOURCE_ROOT).parts)
    for i in range(len(parts) - len(src), -1, -1):
        if parts[i:i + len(src)] == src:
            in_trunk = rs.trunk.joinpath(*parts[i + 1:])
            if in_trunk.is_symlink() and in_trunk.resolve() == m.path.resolve():
                return _rel(rs, in_trunk)
            break
    return _rel(rs, m.path)


def _xml_anomalies(xml: Path, xml_label: str, manifests: list[Manifest], warn) -> list[Anomaly]:
    """XSD (xmllint absent : avertissement) puis CFG-5 d'un XML mklepton du trunk."""
    found = []
    try:
        # ligne de xmllint gardée (D-a, ENV-12 lot 6 S3)
        found.extend(replace(a, file=xml_label) for a in validate_xml(xml))
    except LeptonError as e:
        if e.code != EXIT_TOOL:
            raise
        warn(f"{xml_label} : {e.message}" + (f" ({e.action})" if e.action else ""))
    found.extend(check_mkconf_provided(xml, xml_label, manifests))
    return found


# --------------------------------------------------------------------------
# graine de référence (PA-19, ENV-16) : ni lepton-graine.json ni greffon local de projet
# --------------------------------------------------------------------------
def kernel_presets(path: Path) -> dict[str, dict]:
    """Presets de configuration visibles du noyau → variables de cache, héritage résolu (le premier
    parent l'emporte, comme CMake)."""
    raw = {p["name"]: p for p in json.loads(path.read_text(encoding="utf-8")).get("configurePresets", [])
           if isinstance(p, dict) and isinstance(p.get("name"), str)}

    def variables(name: str, seen: frozenset) -> dict:
        p = raw.get(name)
        if p is None or name in seen:
            return {}
        parents = p.get("inherits", [])
        merged = {}
        for parent in reversed([parents] if isinstance(parents, str) else parents):
            merged.update(variables(parent, seen | {name}))
        merged.update({k: v.get("value") if isinstance(v, dict) else v
                       for k, v in p.get("cacheVariables", {}).items()})
        return merged

    return {name: variables(name, frozenset()) for name, p in raw.items() if not p.get("hidden")}


def check_reference_seed(rs: Rootstock, manifests: list[tuple[Manifest, str]], warn, info
                         ) -> tuple[list[str], list[Anomaly]]:
    """Contrôles déduits des greffons greffés : GRF-5 de chaque BSP ; XSD et CFG-5 des XML cités par
    les presets du noyau dont le BSP est greffé (CFG-5 : greffons hors BSP et famille, plus les BSP
    du XML et leurs familles)."""
    checked, found = [], []
    by_name = {m.name: m for m, _ in manifests}
    kernels = [m for m, _ in manifests if m.kind == "noyau"]
    if len(kernels) != 1:
        found.append(Anomaly(_rel(rs, rs.seed_root()), "", f"{len(kernels)} greffon(s) noyau greffé(s), "
                             "un attendu (GRA-2)"))
        return checked, found
    for m, label in manifests:
        if m.kind == "bsp":
            found.extend(Anomaly(label, where, message) for where, message in check_bsp(m, kernels[0], by_name))

    path = rs.trunk / KERNEL_PRESETS
    presets_label = _rel(rs, path)
    checked.append(presets_label)
    try:
        presets = kernel_presets(path)
    except (OSError, ValueError, AttributeError, TypeError) as e:
        found.append(Anomaly(presets_label, "", f"presets du noyau illisibles ({e})"))
        return checked, found
    xmls, ungrafted = {}, {}
    for name, variables in presets.items():
        board, rel = variables.get("LEPTON_BOARD"), variables.get("LEPTON_MKCONF")
        if not board:
            continue
        if board not in by_name or by_name[board].kind != "bsp":
            ungrafted.setdefault(board, []).append(name)
        elif rel:
            xmls.setdefault(rel, set()).add(board)
        else:
            info(f"preset {name} : LEPTON_MKCONF absent, XML non contrôlé")
    for board, names in sorted(ungrafted.items()):
        info(f"BSP « {board} » non greffé : preset(s) {', '.join(names)} non contrôlé(s)")
    for rel, boards in sorted(xmls.items()):
        xml = rs.trunk / rel
        xml_label = _rel(rs, xml)
        checked.append(xml_label)
        if not xml.exists():
            found.append(Anomaly(presets_label, "", f"LEPTON_MKCONF « {rel} » absent du trunk"))
            continue
        families = {by_name[b].data.get("famille") for b in boards}
        providers = [m for m, _ in manifests if m.kind not in ("bsp", "famille") or m.name in boards | families]
        found.extend(_xml_anomalies(xml, xml_label, providers, warn))
    return checked, found


# --------------------------------------------------------------------------
# lepton check sans argument
# --------------------------------------------------------------------------
def _text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


def _located(rs: Rootstock, anomalies: list[Anomaly]) -> list[Anomaly]:
    """Anomalies à pointeur JSON situées dans leur fichier (diagnostics de l'éditeur, lot 4)."""
    for label in {a.file for a in anomalies if a.line is None and a.location.startswith("/")}:
        text = _text(rs.path / label)            # label relatif au rootstock, ou absolu
        if text is not None:
            locate([a for a in anomalies if a.file == label], text)
    return anomalies


def check_rootstock(rs: Rootstock, warn, info) -> tuple[list[str], list[Anomaly]]:
    """Fichiers contrôlés et anomalies ; `warn` reçoit les contrôles impossibles (xmllint absent),
    `info` les constats sans anomalie (graine de référence)."""
    checked, anomalies = [], []
    report = rs.check_trunk()             # FIC-3 : un fichier régulier bloque aussi toute regreffe
    anomalies.extend(Anomaly(_rel(rs, p), "", "fichier régulier dans le trunk (FIC-3), regreffe bloquée : "
                             "lepton file add --adopt pour le déplacer dans son greffon, ou le supprimer")
                     for p in report.regular_files)
    anomalies.extend(Anomaly(_rel(rs, p), "", "lien cassé dans le trunk : lepton graft") for p in report.broken_links)
    manifests = {}
    for key, m in rs.manifests().items():
        label = _manifest_label(rs, m)
        checked.append(label)
        anomalies.extend(validate_data(m.data, "scion", label, _text(m.path)))
        anomalies.extend(check_options(m, label))
        anomalies.extend(check_declared_files(m, label))
        manifests[key] = (m, label)
    for e in rs.grafted():         # greffon Lepton (scion/sys/root/src) sans manifeste ; pas building
        if e.key not in manifests and (rs.clone(e) / "scion" / "sys" / "root" / "src").is_dir():
            warn(f"{e.key} greffé sans lepton-greffon.json : non contrôlé")
    anomalies.extend(check_dependencies(manifests))

    graine_path = rs.seed_manifest_path()
    label = _rel(rs, graine_path)
    if not graine_path.exists() and not (rs.seed_root() / PROJECT_SUBPATH).exists():
        info(f"graine de référence ({_rel(rs, rs.seed_root())} : ni {graine_path.name} ni {PROJECT_SUBPATH}/) : "
             "contrôles déduits des greffons greffés et des presets du noyau")
        found_checked, found = check_reference_seed(rs, list(manifests.values()), warn, info)
        checked.extend(found_checked)
        anomalies.extend(found)
        return checked, _located(rs, anomalies)
    checked.append(label)
    if not graine_path.exists():
        anomalies.append(Anomaly(label, "", "manifeste de graine absent (graine hors lepton)"))
        return checked, _located(rs, anomalies)
    found = validate_json(graine_path, "seed")
    anomalies.extend(found)
    if found:
        return checked, _located(rs, anomalies)    # rôles indéterminables sur une graine invalide
    graine = json.loads(graine_path.read_text(encoding="utf-8"))
    by_name = {m.name: m for m, _ in manifests.values()}
    anomalies.extend(check_seed(graine, by_name, label))

    xml = rs.trunk / graine["mklepton_xml"]
    xml_label = _rel(rs, xml)
    checked.append(xml_label)
    if not xml.exists():
        anomalies.append(Anomaly(label, "/mklepton_xml", f"« {graine['mklepton_xml']} » absent du trunk"))
        return checked, _located(rs, anomalies)
    if not xml.resolve().is_relative_to((rs.seed_root() / PROJECT_SUBPATH / STEM_DIR).resolve()):
        # O5 (CFG-1) : XML du projet versionné dans la graine ; ici XML d'un greffon partagé
        warn(f"{xml_label} : XML fourni par un greffon partagé, pas par la graine (CFG-1, O5) ; "
             f"lepton seed mkconf import {graine['mklepton_xml']}")
    anomalies.extend(_xml_anomalies(xml, xml_label, [m for m, _ in manifests.values()], warn))
    return checked, _located(rs, anomalies)
