"""Greffons : scion new, scion remove (GRF-1, GRF-4 ; interface §3.6, amendements S3).

`scion new` crée un dépôt git local depuis `lepton/templates/<kind>/` (application, bibliothèque)
ou par copie d'un BSP greffé (`--from`, décisions S3-1 et S3-2), le commite, puis l'ajoute à la
graine comme `lepton seed add` (origine locale, version `*`).
"""

import json
import re
import shutil
from pathlib import Path

from lepton import seed
from lepton.errors import EXIT_OK, LeptonError
from lepton.rootstock import SOURCE_ROOT, STEM_DIR, Rootstock, find_manifest, is_system_file, scion_key
from lepton.scion_runner import git, run
from lepton.templates import SCION_KIND, c_identifier, render_text, render_tree, templates_dir
from lepton.validation import SCION_MANIFEST, validate_data

# Destination par défaut d'un greffon créé (PA-7 Q12, PA-9 Q6)
DEFAULT_DESTINATION = {"bsp": "kernel/dev/bsp/{name}", "application": "bin/{name}", "bibliotheque": "lib/{name}"}

# Champ du manifeste BSP → jeton de `templates/bsp/lepton-greffon.json` (champs matériels repris de --from)
BSP_FIELDS = {
    "famille": "family", "coeur": "core", "abi_flottante": "float_abi", "mcu": "mcu",
    "frequence_cpu": "cpu_frequency", "entete_config_noyau": "kernel_config_header",
    "script_liens": "link_script", "demarrage": "startup", "sources": "sources",
    "dependances": "dependencies", "openocd": "openocd", "sonde": "probe", "svd": "svd",
    "qemu": "qemu", "compilation": "compilation", "options": "options",
}


def _destination_pattern(old: str) -> re.Pattern:
    """`old` comme chemin entier : `kernel/dev/bsp/a` ne remplace pas dans `kernel/dev/bsp/a-b`."""
    return re.compile(re.escape(old) + r"(?![\w.-])")


def _replace_in(value, pattern: re.Pattern, new: str):
    if isinstance(value, str):
        return pattern.sub(new, value)
    if isinstance(value, list):
        return [_replace_in(v, pattern, new) for v in value]
    if isinstance(value, dict):
        return {k: _replace_in(v, pattern, new) for k, v in value.items()}
    return value


def _check_repo(repo: Path) -> None:
    if repo.exists() and (not repo.is_dir() or any(repo.iterdir())):
        raise LeptonError(f"{repo} existe et n'est pas un répertoire vide", "choisir un autre --repo")


def _check_destination(dest: str) -> None:
    parts = Path(dest).parts
    if not dest or Path(dest).is_absolute() or ".." in parts:
        raise LeptonError(f"--destination « {dest} » invalide", "chemin relatif à sys/root/src, sans « .. »")


def _validated(data: dict, label: str) -> dict:
    anomalies = validate_data(data, "scion", label)
    if anomalies:
        raise LeptonError("manifeste refusé :\n" + "\n".join(f"  {a.location}: {a.message}" for a in anomalies),
                          "corriger NAME ou --destination")
    return data


def _bsp_source(rs: Rootstock, src_name: str):
    """Manifeste du BSP greffé `src_name` et fichiers suivis par git de son répertoire (S3-2)."""
    key = rs.key_of(src_name)
    manifest = None
    if key is not None:
        entry = next(e for e in rs.grafted() if e.key == key)
        manifest = find_manifest(rs.clone(entry))
    if manifest is None or manifest.kind != "bsp":
        raise LeptonError(f"--from « {src_name} » : aucun BSP greffé de ce nom",
                          "lepton seed status (colonne greffon, rôle bsp)")
    src_dir = manifest.path.parent
    listed = git(src_dir, "ls-files", "-z").stdout.split("\0")
    files = [Path(f) for f in listed if f and f != SCION_MANIFEST and not is_system_file(Path(f).name)
             and (src_dir / f).is_file()]
    return manifest, src_dir, files


def _bsp_values(name: str, dest: str, src) -> dict:
    """Valeurs du modèle BSP : champs matériels de `src`, destination source remplacée (S3-1)."""
    pattern = _destination_pattern(src.data["destination"])
    values = {token: _replace_in(src.data.get(field), pattern, dest) for field, token in BSP_FIELDS.items()}
    values.update(name=name, version="0.1.0", destination=dest,
                  description=f"BSP {name}, dérivé de {src.name}.")
    return values


def _manifest_from_template(kind: str, values: dict) -> dict:
    text = (templates_dir() / kind / SCION_MANIFEST).read_text(encoding="utf-8")
    return json.loads(render_text(text, values, json_file=True, where=f"{kind}/{SCION_MANIFEST}"))


def _copy_bsp(src_dir: Path, files: list[Path], target: Path, old_dest: str, new_dest: str) -> None:
    pattern = _destination_pattern(old_dest)
    for rel in files:
        source, copy = src_dir / rel, target / rel
        copy.parent.mkdir(parents=True, exist_ok=True)
        try:
            text = source.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            shutil.copyfile(source, copy)            # binaire : copie telle quelle
        else:
            copy.write_text(pattern.sub(new_dest, text), encoding="utf-8")
        shutil.copymode(source, copy)


def scion_new(args) -> int:
    rs = Rootstock.discover(args.rootstock)
    name, kind = args.name, args.type
    seed.check_new_scion(rs, name, kind)
    dest = args.destination or DEFAULT_DESTINATION[kind].format(name=name)
    _check_destination(dest)
    repo = Path(args.repo).resolve() if args.repo else rs.depots / f"lepton-{SCION_KIND[kind]}" / name
    _check_repo(repo)
    target = repo / STEM_DIR / SOURCE_ROOT / dest

    # manifeste calculé et validé avant toute écriture
    if kind == "bsp":
        if not args.from_bsp:
            raise LeptonError("--from BSP obligatoire pour un BSP (copie d'un BSP greffé, renommée)",
                              f"lepton scion new {name} --type bsp --from <BSP greffé>")
        src, src_dir, files = _bsp_source(rs, args.from_bsp)
        manifest = _validated(_manifest_from_template("bsp", _bsp_values(name, dest, src)), SCION_MANIFEST)
    else:
        if args.from_bsp:
            raise LeptonError("--from réservé au type bsp", "retirer --from")
        values = {"name": name, "c_name": c_identifier(name), "c_guard": f"{c_identifier(name).upper()}_H",
                  "kernel": seed.KERNEL_NAME, "destination": dest,
                  "description": f"{'Application' if kind == 'application' else 'Bibliothèque'} {name}."}
        _validated(_manifest_from_template(SCION_KIND[kind], values), SCION_MANIFEST)

    # dépôt : fichiers, commit initial
    if kind == "bsp":
        _copy_bsp(src_dir, files, target, src.data["destination"], dest)
        target.mkdir(parents=True, exist_ok=True)
        (target / SCION_MANIFEST).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                                             encoding="utf-8")
        message = f"Greffon {name} créé par lepton scion new depuis {src.name}"
    else:
        render_tree(SCION_KIND[kind], target, values)
        message = f"Greffon {name} créé par lepton scion new"
    run(["git", "init", "-q", "-b", "master", str(repo)])
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", message)
    seed._info(f"dépôt créé : {repo} ({dest})")

    add_cmd = f"lepton seed add {name} {repo} --type {kind}"
    if args.no_seed:
        seed._info(f"ajout à la graine : {add_cmd}")
        return EXIT_OK
    origin = seed.parse_location(str(repo), rootstock=rs.path)
    try:
        return seed.add_scion(rs, name, kind, origin, args.no_cmake)
    except LeptonError as e:
        left = f"état laissé : {_left_state(rs, name, kind, repo, add_cmd)}"
        e.action = f"{e.action} ; {left}" if e.action else left
        raise


def _left_state(rs: Rootstock, name: str, kind: str, repo: Path, add_cmd: str) -> str:
    """État laissé par un ajout en échec, lu sur disque (O3) : l'annulation peut être incomplète,
    ou l'échec survenir après l'ajout (contrôle du trunk, reconfiguration CMake)."""
    key = scion_key(kind, name)
    declared = key in {s.key for s in rs.sources()}
    grafted = key in {e.key for e in rs.grafted()}
    graine = seed.load_graine(rs.seed_manifest_path())
    listed = name in graine.get("applications", []) + graine.get("bibliotheques", []) + [graine.get("bsp")]
    head = f"dépôt {repo} créé et commité"
    if declared and grafted and listed:
        return f"{head}, greffon ajouté à la graine (corriger la cause, puis lepton graft)"
    if not (declared or grafted or listed):
        return f"{head}, hors graine ({add_cmd})"
    where = [w for w, b in (("déclaré dans .scion.sources.list", declared), ("greffé", grafted),
                            ("cité dans lepton-graine.json", listed)) if b]
    undo = (f"lepton seed remove {name}" if grafted else
            f"scion seed-scion-remove --seed {rs.seed_root()} {key}" if declared else
            f"retirer {name} de {rs.seed_manifest_path()}")
    return f"{head}, greffon {', '.join(where)} (annulation incomplète : {undo}, puis {add_cmd})"


def scion_remove(args) -> int:
    """GRF-4 : comme `seed remove` sans `--purge` ; le dépôt du greffon n'est jamais touché."""
    args.purge = False
    return seed.seed_remove(args)
