#!/usr/bin/env python3
"""ENV-60 : checkout en échec après un clone réussi (D18), sur des rootstocks temporaires.

Usage : fixture.py <seed.scions> <exécutable scion> <base> <sortie versionnée>

Forme de env-56-scion/fixture.py (rootstocks bâtis comme les fixtures de scion, dépôts sous
<base>/repos, aucune URL réseau). Chaque commande relevée donne <cas>.cmd, .out, .err, .code,
.depots, et l'état de ses clones et du trunk (etat.py : <cas>.clones, <cas>.trunk). Les cas
« passage suivant » relancent la commande sur le même rootstock.

graft-update n'est jamais lancé ici (D20, ORCHESTRATION §2bis) : le cas u01 est préparé, la
commande à lancer par la session est écrite dans <sortie>/u01.a-lancer, puis l'état se relève par
etat.py. Rien n'est nettoyé : <base> est supprimé entier (scripts/supprimer-essai.sh).
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

SEED_SCIONS, SCION, BASE, OUT = (Path(a) for a in sys.argv[1:5])
sys.path.insert(0, str(SEED_SCIONS / "tests"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import etat  # noqa: E402
import make_fixture  # noqa: E402

BASE = BASE.resolve()
OUT.mkdir(parents=True, exist_ok=True)
REPOS = BASE / "repos"
ENV = {**os.environ, "LC_ALL": "C"}


def g(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, env=ENV)


PLAIN = make_fixture.make_repo(REPOS / "plain", {"scion/f.txt": "f\n"})
SHA = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPOS / "plain", capture_output=True,
                     text=True, check=True).stdout.strip()   # change à chaque construction : <SHA>
PLAIN2 = make_fixture.make_repo(REPOS / "plain2", {"scion/g.txt": "g\n"})
# ambi : branche « doc » et répertoire doc/ ; tag léger « tests » et répertoire tests/
AMBI = make_fixture.make_repo(REPOS / "ambi", {"scion/f.txt": "f\n", "doc/d.txt": "d\n",
                                               "tests/t.txt": "t\n"})
g(REPOS / "ambi", "checkout", "-q", "-b", "doc")
(REPOS / "ambi/scion/doc.txt").write_text("branche doc\n")
make_fixture.commit_all(REPOS / "ambi", "branche doc")
g(REPOS / "ambi", "checkout", "-q", "master")
g(REPOS / "ambi", "tag", "tests")
EMPTY = REPOS / "vide.git"
EMPTY.mkdir(parents=True)
g(EMPTY, "init", "-q", "--bare")
EMPTY_URL = "file://localhost" + str(EMPTY)
# graine distante : sa branche master déclare own/plain master
GRAINE = make_fixture.make_repo(REPOS / "graine", {
    "scion/.scion/.scion.sources.list": f"own\tplain\tmaster\t{PLAIN}\n",
    "scion/.scion/.scion.ramifications": "own\tplain\tmaster\n",
})

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


def seed(name: str, scions) -> Path:
    dot = BASE / name / "seed/scion/.scion"
    write(dot / ".scion.sources.list", "".join("\t".join(s) + "\n" for s in scions))
    write(dot / ".scion.ramifications", "".join("\t".join(s[:3]) + "\n" for s in scions))
    return dot.parent.parent


def dirs(r: Path) -> list[str]:
    return [str(d.relative_to(r)) for d in sorted((r / "depots").rglob("*"))
            if d.is_dir() and ".git" not in d.relative_to(r).parts]


def norm(text: str) -> str:
    return (text.replace(str(BASE), "<B>").replace(str(Path.home()), "<HOME>")
            .replace(SHA, "<SHA>"))


def case(name: str, r: Path, label: str, *argv: str) -> None:
    p = subprocess.run([str(SCION), *argv], cwd=r, capture_output=True, text=True, env=ENV)
    (OUT / f"{name}.cmd").write_text(norm("scion " + " ".join(argv)) + "\n")
    (OUT / f"{name}.err").write_text(norm(p.stderr))
    (OUT / f"{name}.out").write_text(norm(p.stdout))
    (OUT / f"{name}.code").write_text(f"{p.returncode}\n")
    (OUT / f"{name}.depots").write_text(norm("".join(f"{d}\n" for d in dirs(r))))
    etat.releve(r, OUT, name, BASE, {SHA: "<SHA>"})
    branches = []
    for c in etat.clones(r):
        b = etat.git(c, "branch", "--show-current") or "détaché"
        branches.append(f"{c.relative_to(r)}:{b}")
    last = (p.stderr.strip().splitlines() or ["—"])[-1]
    links = sum(1 for _ in (r / "trunk").rglob("*") if _.is_symlink())
    rows.append("\t".join([name, label, str(p.returncode), " ".join(branches) or "—",
                           str(links), norm(last)[:160]]))


def seed_add(name: str, label: str, scions, *extra: str) -> Path:
    r = rootstock(name)
    case(name, r, label, "seed-add", *extra, str(seed(name, scions)))
    return r


# --- D18 : clé ordinaire, version absente, sans --single-branch (f06 d'ENV-56)
r = seed_add("k01", "ordinaire, version absente, sans --single-branch (f06)",
             [("own", "plain", "nope", PLAIN)])
case("k02", r, "passage suivant de k01 (seed-add relancé)", "seed-add", str(BASE / "k01/seed"))
case("k03", r, "graft après k01", "graft")
# chemin de lepton (seed-scion-add → seed-clone → graft --scion) : seed-clone sans contrôle
r = seed_add("k18", "comme k01 (préparation de k18b, k18c)", [("own", "plain", "nope", PLAIN)])
case("k18b", r, "seed-clone après k18 (clone gardé en place)", "seed-clone", "--seed",
     str(BASE / "k18/seed"))
case("k18c", r, "graft après k18b", "graft")

# --- graine distante (cli._clone_seed)
r = rootstock("k04")
case("k04", r, "graine distante, version absente", "seed-add", "--version", "nope", GRAINE)
case("k05", r, "passage suivant de k04", "seed-add", "--version", "nope", GRAINE)
case("k06", r, "graft après k05", "graft")
r = rootstock("k07")
case("k07", r, "voisin : graine distante, --single-branch, version absente",
     "seed-add", "--single-branch", "--version", "nope", GRAINE)

# --- version qui n'est qu'un chemin du dépôt (« git checkout scion » = restauration de chemin)
r = seed_add("k08", "ordinaire, version = chemin du dépôt (scion), sans ref de ce nom",
             [("own", "plain", "scion", PLAIN)])
case("k09", r, "graft après k08", "graft")
case("k10", r, "passage suivant de k08", "seed-add", str(BASE / "k08/seed"))
r = rootstock("k17")
case("k17", r, "graine distante, version = chemin du dépôt (scion)",
     "seed-add", "--version", "scion", GRAINE)
case("k17b", r, "graft après k17", "graft")

# --- version présente, homonyme d'un chemin
r = seed_add("k11", "ordinaire, branche distante « doc » et répertoire doc/",
             [("own", "ambi", "doc", AMBI)])
case("k12", r, "passage suivant de k11", "seed-add", str(BASE / "k11/seed"))
seed_add("k13", "voisin : k11 avec --single-branch", [("own", "ambi", "doc", AMBI)],
         "--single-branch")
seed_add("k14", "voisin : tag « tests » et répertoire tests/", [("own", "ambi", "tests", AMBI)])

# --- origine vide
r = seed_add("k15", "ordinaire, origine vide, version master", [("own", "vide", "master", EMPTY_URL)])
case("k16", r, "passage suivant de k15", "seed-add", str(BASE / "k15/seed"))

# --- version commit complet (clé ordinaire : le contrôle de 0.5.4.0 ne connaît que branche et tag)
r = seed_add("k19", "ordinaire, version = commit complet de master", [("own", "plain", SHA, PLAIN)])
case("k19b", r, "passage suivant de k19", "seed-add", str(BASE / "k19/seed"))

# --- graft-update (préparé ici, lancé par la session)
r = rootstock("u01")
seed("u01", [("own", "plain", "master", PLAIN)])
case("u01a", r, "préparation de u01 : seed-add réussi", "seed-add", str(BASE / "u01/seed"))
case("u01b", r, "préparation de u01 : graft", "graft")
seed("u01", [("own", "plain", "master", PLAIN), ("own", "plain2", "nope", PLAIN2)])
etat.releve(r, OUT, "u01-depart", BASE)
(OUT / "u01.a-lancer").write_text(
    "# graine réécrite : own/plain2 « nope » ajoutée (absente de plain2)\n"
    f"scion graft-update {norm(str(r))}\n")

(OUT / "fixture.tsv").write_text(norm(
    "cas\tlibellé\tcode\tclones:branche\tliens du trunk\tdernière ligne du stderr\n"
    + "\n".join(rows) + "\n"))
print((OUT / "fixture.tsv").read_text())
print("u01 :", r)
