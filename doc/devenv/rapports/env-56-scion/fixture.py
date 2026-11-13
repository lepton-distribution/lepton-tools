#!/usr/bin/env python3
"""ENV-56 : clonages en échec sur des rootstocks temporaires bâtis comme les fixtures de scion.

Usage : fixture.py <seed.scions> <exécutable scion> <base> <sortie versionnée>

Chaque cas reçoit son propre rootstock sous <base>/<cas>/ (forme de ProjectionCase et MirrorCase
des tests de scion : signature, depots/, trunk/ avec sa liste greffée, dépôts sous repos/). Le scion
désigné est lancé par sous-processus, dans le rootstock. Avant et après chaque commande relevée, la
liste des répertoires de depots/ (hors .git) est prise ; les répertoires nouveaux sont classés
« résidu » s'ils sont vides, « non vide » sinon. Rien n'est nettoyé : <base> est supprimé entier
(scripts/supprimer-essai.sh), le hook refusant toute écriture shell sous depots/tiers/.

Aucune URL réseau : amonts, miroirs et dépôts absents sont des chemins file://localhost sous <base>.
`mirror-sync` n'est lancé qu'avec --dry-run.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SEED_SCIONS, SCION, BASE, OUT = (Path(a) for a in sys.argv[1:5])
sys.path.insert(0, str(SEED_SCIONS / "tests"))
import make_fixture  # noqa: E402

BASE = BASE.resolve()
OUT.mkdir(parents=True, exist_ok=True)
REPOS = BASE / "repos"
TIERS = make_fixture.build_tiers(REPOS / "tiers")
PLAIN = make_fixture.make_repo(REPOS / "plain", {"scion/f.txt": "f\n"})
ABSENT = "file://localhost" + str(REPOS / "absent.git")        # jamais créé
ABSENT2 = "file://localhost" + str(REPOS / "absent2.git")      # jamais créé
UPSTREAM = make_fixture.make_repo(REPOS / "amont", {"README.md": "amont\n"})
MIRROR_PRESENT = REPOS / "miroirs/present.git"
MIRROR_ABSENT = "file://localhost" + str(REPOS / "miroirs/absent.git")  # jamais créé
MIRROR_PRESENT.mkdir(parents=True)
subprocess.run(["git", "init", "-q", "--bare"], cwd=MIRROR_PRESENT, check=True)

rows: list[str] = []


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def rootstock(name: str) -> Path:
    r = BASE / name / "rootstock"
    (r / "depots").mkdir(parents=True)
    (r / ".scion.rootstock.signature").touch()
    (r / "trunk").mkdir()
    (r / "trunk/.scion.grafted.list").touch()
    return r


def seed(name: str, scions, projections: str = "", mirrors: str = "") -> Path:
    dot = BASE / name / "seed/scion/.scion"
    write(dot / ".scion.sources.list", "".join("\t".join(s) + "\n" for s in scions))
    write(dot / ".scion.ramifications", "".join("\t".join(s[:3]) + "\n" for s in scions))
    if projections:
        write(dot / ".scion.projections", projections)
    if mirrors:
        write(dot / ".scion.mirrors", mirrors)
    return dot.parent.parent


def dirs(r: Path) -> dict[str, bool]:
    """Répertoires de depots/ hors .git : chemin relatif -> vide ?"""
    found = {}
    for d in sorted((r / "depots").rglob("*")):
        if not d.is_dir() or ".git" in d.relative_to(r).parts:
            continue
        if any(p.endswith(".git") for p in d.relative_to(r).parts[:-1]):
            continue  # intérieur d'un dépôt nu (miroir de travail)
        found[str(d.relative_to(r))] = not any(d.iterdir())
    return found


def norm(text: str) -> str:
    """<B> pour la base, y compris dans un chemin de dépôt de travail de miroir (sans « / » initial)."""
    return (text.replace(str(BASE), "<B>").replace(str(BASE).lstrip("/"), "<B>")
            .replace(str(Path.home()), "<HOME>"))


def case(name: str, r: Path, label: str, *argv: str) -> None:
    before = dirs(r)
    p = subprocess.run([str(SCION), *argv], cwd=r, capture_output=True, text=True)
    after = dirs(r)
    new = [d for d in after if d not in before]
    residues = [d for d in new if after[d]]
    top = [d for d in new if str(Path(d).parent) not in new]
    clones = [d for d in new if (r / d / ".git").exists() or (r / d / "config").is_file()]
    kept = [d for d in before if d in after]
    gone = [d for d in before if d not in after]
    (OUT / f"{name}.cmd").write_text(norm("scion " + " ".join(argv)) + "\n")
    (OUT / f"{name}.err").write_text(norm(p.stderr))
    (OUT / f"{name}.out").write_text(norm(p.stdout))
    (OUT / f"{name}.code").write_text(f"{p.returncode}\n")
    (OUT / f"{name}.depots").write_text(norm(
        "".join(f"{d}{' (vide)' if v else ''}\n" for d, v in after.items())))
    rows.append("\t".join([
        name, label, str(p.returncode),
        str(len(new)),
        " ".join(top) or "—",
        " ".join(residues) or "—",
        " ".join(clones) or "—",
        " ".join(gone) or "—",
        str(len(kept)),
    ]))


def seed_add(name: str, label: str, scions, *extra: str, projections: str = "",
             prep: list[tuple[str, bool]] = ()) -> Path:
    r = rootstock(name)
    for d, temoin in prep:
        (r / d).mkdir(parents=True)
        if temoin:
            (r / d / "temoin").write_text("autre version\n")
    s = seed(name, scions, projections)
    case(name, r, label, "seed-add", *extra, str(s))
    return r


PROJ = "tiers hal Inc/* scion/inc/\n"

# --- clé ordinaire (gitops.clone, _fetch)
seed_add("f01", "ordinaire, étagère nouvelle", [("own", "plain", "master", ABSENT)])
seed_add("f02", "ordinaire, étagère existante", [("own", "plain", "master", ABSENT)],
         prep=[("depots/own/autre/master", True)])
seed_add("f03", "ordinaire, parent porteur d'une autre version", [("own", "plain", "master", ABSENT)],
         prep=[("depots/own/plain/v0", True)])
seed_add("f04", "ordinaire, parent préexistant vide", [("own", "plain", "master", ABSENT)],
         prep=[("depots/own/plain", False)])
seed_add("f05", "ordinaire, --single-branch, version absente d'un dépôt présent",
         [("own", "plain", "nope", PLAIN)], "--single-branch")
seed_add("f06", "voisin : ordinaire sans --single-branch, version absente (clone puis checkout)",
         [("own", "plain", "nope", PLAIN)])

# --- clé projetée (gitops.clone_partial, _fetch)
seed_add("f07", "projetée, étagère tiers nouvelle", [("tiers", "hal", "v1.0", ABSENT)],
         projections=PROJ)
seed_add("f08", "voisin : projetée, version absente (« clone laissé en place »)",
         [("tiers", "hal", "v9.9", TIERS.url)], projections=PROJ)
# étagère tiers et parent créés par un premier seed-add réussi, puis seed réécrit
r = seed_add("f09a", "projetée, premier ajout réussi (préparation de f09b, f09c)",
             [("tiers", "hal", "v1.0", TIERS.url)], projections=PROJ)
s = seed("f09a", [("tiers", "hal", "v1.0", TIERS.url), ("tiers", "hal2", "v1.0", ABSENT)],
         projections=PROJ + "tiers hal2 Inc/* scion/inc2/\n")
case("f09b", r, "projetée, étagère tiers existante (autre clé déjà clonée)", "seed-add", str(s))
s = seed("f09a", [("tiers", "hal", "v2.0", ABSENT)], projections=PROJ)
case("f09c", r, "projetée, parent porteur d'une autre version (v1.0 cloné, v2.0 absent)",
     "seed-add", str(s))

# --- graine distante (cli._clone_seed)
r = rootstock("f10")
case("f10", r, "graine distante absente", "seed-add", ABSENT2)

# --- miroirs (mirror.sync_one), --dry-run seulement
r = rootstock("f11")
s = seed("f11", [("own", "plain", "master", PLAIN)],
         mirrors=f"{MIRROR_ABSENT}\t{UPSTREAM}\n")
case("f11", r, "miroir absent, aucun dépôt de travail", "mirror-sync", "--dry-run", "--seed", str(s))
r = rootstock("f12")
s = seed("f12", [("own", "plain", "master", PLAIN)],
         mirrors=f"file://localhost{MIRROR_PRESENT}\t{ABSENT}\n")
case("f12a", r, "voisin : miroir présent, amont absent (dépôt de travail cloné, fetch en échec)",
     "mirror-sync", "--dry-run", "--seed", str(s))
s = seed("f12", [("own", "plain", "master", PLAIN)],
         mirrors=f"file://localhost{MIRROR_PRESENT}\t{ABSENT}\n{MIRROR_ABSENT}\t{UPSTREAM}\n")
case("f12b", r, "miroir absent, ancêtres déjà créés par un autre miroir", "mirror-sync",
     "--dry-run", "--seed", str(s))

(OUT / "fixture.tsv").write_text(norm(
    "cas\tlibellé\tcode\tcréés\tplus haut créé\trésidus vides\tclones gardés\tdisparus\t"
    "préexistants gardés\n"
    + "\n".join(rows) + "\n"))
print((OUT / "fixture.tsv").read_text())
