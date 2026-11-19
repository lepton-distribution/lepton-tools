#!/usr/bin/env python3
"""ENV-65 : clone existant hors de sa version (D25) et messages d'échec de git (D22).

Usage : fixture.py <seed.scions> <exécutable scion> <base> <sortie versionnée>

Forme d'env-60-scion/fixture.py (rootstocks bâtis comme les fixtures de scion, dépôts sous
<base>/repos, aucune URL réseau sauf n04, nom en `.invalid`). Chaque commande relevée donne
<cas>.cmd, .out, .err, .code, .depots, l'état des clones et du trunk (env-60-scion/etat.py :
<cas>.clones, <cas>.trunk) ; le tableau <sortie>/fixture.tsv ajoute le contenu de trunk/f.txt
lu par son lien (ce que la greffe montre). Un clone est mis hors de sa version à la main
(`git checkout`, `git clone` sans `-b`) : la préparation est écrite dans <cas>.prep. Pour D22,
la commande git que scion lance est rejouée telle quelle hors de scion : son stderr complet est
écrit dans <cas>.git-err (ce que le message de scion pourrait garder).

graft-update n'est jamais lancé ici (ORCHESTRATION §2bis). Rien n'est nettoyé : <base> est
supprimé entier (scripts/supprimer-essai.sh). git en anglais (LC_ALL=C) ; le français se déduit
de po/fr.po (scripts/comparer-releves.py), le git d'Apple n'étant pas traduit.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

SEED_SCIONS, SCION, BASE, OUT = (Path(a) for a in sys.argv[1:5])
sys.path.insert(0, str(SEED_SCIONS / "tests"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "env-60-scion"))
import etat  # noqa: E402
import make_fixture  # noqa: E402

BASE = BASE.resolve()
OUT.mkdir(parents=True, exist_ok=True)
REPOS = BASE / "repos"
ENV = {**os.environ, "LC_ALL": "C", "GIT_TERMINAL_PROMPT": "0"}


def g(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True,
                          env=ENV).stdout.strip()


# plain : tag v1 (f.txt = « v1 »), master (« master »), branche dev (« dev »)
PLAIN = make_fixture.make_repo(REPOS / "plain", {"scion/f.txt": "v1\n"})
g(REPOS / "plain", "tag", "-a", "v1", "-m", "v1")
(REPOS / "plain/scion/f.txt").write_text("master\n")
make_fixture.commit_all(REPOS / "plain", "master")
g(REPOS / "plain", "checkout", "-q", "-b", "dev")
(REPOS / "plain/scion/f.txt").write_text("dev\n")
make_fixture.commit_all(REPOS / "plain", "dev")
g(REPOS / "plain", "checkout", "-q", "master")
SHAS = {g(REPOS / "plain", "rev-parse", r): f"<{n}>" for r, n in
        (("v1^{commit}", "V1"), ("master", "MASTER"), ("dev", "DEV"))}
# graine distante : master déclare own/plain master ; autre déclare own/plain dev
GRAINE = make_fixture.make_repo(REPOS / "graine", {
    "scion/.scion/.scion.sources.list": f"own\tplain\tmaster\t{PLAIN}\n",
    "scion/.scion/.scion.ramifications": "own\tplain\tmaster\n",
})
g(REPOS / "graine", "checkout", "-q", "-b", "autre")
(REPOS / "graine/scion/.scion/.scion.sources.list").write_text(f"own\tplain\tdev\t{PLAIN}\n")
(REPOS / "graine/scion/.scion/.scion.ramifications").write_text("own\tplain\tdev\n")
make_fixture.commit_all(REPOS / "graine", "autre")
g(REPOS / "graine", "checkout", "-q", "master")
NONGIT = REPOS / "nongit"
(NONGIT / "scion").mkdir(parents=True)
ABSENT = "file://localhost" + str(REPOS / "absent")
NONGIT_URL = "file://localhost" + str(NONGIT)
RESEAU = "https://scion-essai.invalid/plain.git"

rows: list[str] = []


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def norm(text: str) -> str:
    text = text.replace(str(BASE), "<B>").replace(str(Path.home()), "<HOME>")
    for sha, name in SHAS.items():
        text = text.replace(sha, name).replace(sha[:7], name)
    return text


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


def prep(name: str, r: Path, *steps: tuple[Path, list[str]]) -> None:
    """Préparation à la main (hors scion) : chaque commande git est consignée."""
    lines = []
    for cwd, args in steps:
        cwd.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, env=ENV)
        lines.append(f"(cd {cwd}) git {' '.join(args)}")
    (OUT / f"{name}.prep").write_text(norm("\n".join(lines) + "\n"))


def git_err(name: str, cwd: Path, *args: str) -> None:
    """La commande git de scion, rejouée hors de scion : stderr complet."""
    cwd.mkdir(parents=True, exist_ok=True)
    p = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, env=ENV)
    (OUT / f"{name}.git-err").write_text(norm(f"$ git {' '.join(args)}\ncode {p.returncode}\n"
                                              + p.stderr))


def case(name: str, r: Path, label: str, *argv: str) -> None:
    p = subprocess.run([str(SCION), *argv], cwd=r, capture_output=True, text=True, env=ENV)
    (OUT / f"{name}.cmd").write_text(norm("scion " + " ".join(argv)) + "\n")
    (OUT / f"{name}.err").write_text(norm(p.stderr))
    (OUT / f"{name}.out").write_text(norm(p.stdout))
    (OUT / f"{name}.code").write_text(f"{p.returncode}\n")
    (OUT / f"{name}.depots").write_text(norm("".join(f"{d}\n" for d in dirs(r))))
    etat.releve(r, OUT, name, BASE, {sha: n for sha, n in SHAS.items()})
    branches = []
    for c in etat.clones(r):
        b = etat.git(c, "branch", "--show-current") or "détaché"
        branches.append(f"{c.relative_to(r)}:{b}")
    f = r / "trunk/f.txt"
    shown = f.read_text().strip() if f.is_symlink() and f.exists() else "—"
    last = (p.stderr.strip().splitlines() or ["—"])[-1]
    rows.append("\t".join([name, label, str(p.returncode), " ".join(branches) or "—",
                           shown, norm(last)[:200]]))


def seed_add(name: str, label: str, scions, *extra: str) -> Path:
    r = rootstock(name)
    case(name, r, label, "seed-add", *extra, str(seed(name, scions)))
    return r


# ==========================================================================
# D25 : clone existant hors de sa version
# ==========================================================================
# a : clé ordinaire, branche, greffée puis déplacée (git checkout)
r = seed_add("a01", "clé own/plain dev : seed-add", [("own", "plain", "dev", PLAIN)])
case("a02", r, "graft", "graft")
prep("a03", r, (r / "depots/own/plain/dev", ["checkout", "-q", "master"]))
case("a03", r, "seed-clone, clone dev sur master (chemin de lepton seed add)",
     "seed-clone", "--seed", str(BASE / "a01/seed"))
case("a04", r, "graft après a03", "graft")
case("a05", r, "graft --scion own@plain", "graft", "--scion", "own@plain")
case("a06", r, "seed-add relancé (contrôle de 0.5.4.0)", "seed-add", str(BASE / "a01/seed"))

# b : clé ordinaire, clone préexistant jamais greffé (forme du clone laissé par ≤ 0.6.3.1)
r = rootstock("b01")
seed("b01", [("own", "plain", "dev", PLAIN)])
prep("b01", r, (r / "depots/own/plain", ["clone", "-q", PLAIN, "dev"]))
case("b01", r, "seed-clone, clone dev préexistant sur master (l03 d'ENV-60)",
     "seed-clone", "--seed", str(BASE / "b01/seed"))
case("b02", r, "graft après b01", "graft")
r = rootstock("b03")
seed("b03", [("own", "plain", "dev", PLAIN)])
prep("b03", r, (r / "depots/own/plain", ["clone", "-q", PLAIN, "dev"]))
case("b03", r, "seed-add, même clone préexistant", "seed-add", str(BASE / "b03/seed"))

# c : clé ordinaire, tag
r = rootstock("c01")
seed("c01", [("own", "plain", "v1", PLAIN)])
prep("c01", r, (r / "depots/own/plain", ["clone", "-q", PLAIN, "v1"]))
case("c01", r, "seed-clone, clone du tag v1 préexistant sur master",
     "seed-clone", "--seed", str(BASE / "c01/seed"))
case("c02", r, "graft après c01", "graft")
r = rootstock("c03")
seed("c03", [("own", "plain", "v1", PLAIN)])
prep("c03", r, (r / "depots/own/plain", ["clone", "-q", PLAIN, "v1"]))
case("c03", r, "seed-add, même clone", "seed-add", str(BASE / "c03/seed"))

# d : graine distante (cli._clone_seed)
r = rootstock("d01")
case("d01", r, "graine distante --version autre : seed-add", "seed-add", "--version", "autre",
     GRAINE)
prep("d02", r, (r / "depots/graine/autre", ["checkout", "-q", "master"]))
case("d02", r, "seed-add relancé, graine sur master (k05)", "seed-add", "--version", "autre",
     GRAINE)
case("d03", r, "graft après d02", "graft")
r = rootstock("d04")
prep("d04", r, (r / "depots/graine", ["clone", "-q", GRAINE, "autre"]))
case("d04", r, "seed-add, graine autre préexistante sur master (forme ≤ 0.6.3.1)",
     "seed-add", "--version", "autre", GRAINE)
case("d05", r, "graft après d04", "graft")

# e : témoins à leur version (doivent rester identiques après correction)
r = seed_add("e01", "témoin : seed-add own/plain dev", [("own", "plain", "dev", PLAIN)])
case("e02", r, "témoin : seed-clone", "seed-clone", "--seed", str(BASE / "e01/seed"))
case("e03", r, "témoin : graft", "graft")
r = seed_add("e04", "témoin : seed-add own/plain v1", [("own", "plain", "v1", PLAIN)])
case("e05", r, "témoin : seed-clone (tag)", "seed-clone", "--seed", str(BASE / "e04/seed"))
r = rootstock("e06")
case("e06", r, "témoin : graine distante --version autre", "seed-add", "--version", "autre",
     GRAINE)
case("e07", r, "témoin : graine relancée", "seed-add", "--version", "autre", GRAINE)

# f : branche de travail dans un clone greffé (forme du clone noyau sur devenv/env-N)
r = seed_add("f01", "clé own/plain master : seed-add", [("own", "plain", "master", PLAIN)])
case("f02", r, "graft", "graft")
prep("f03", r, (r / "depots/own/plain/master", ["checkout", "-q", "-b", "travail"]))
case("f03", r, "seed-clone, clone master sur la branche travail",
     "seed-clone", "--seed", str(BASE / "f01/seed"))
case("f04", r, "graft, branche travail", "graft")
case("f05", r, "seed-add relancé, branche travail", "seed-add", str(BASE / "f01/seed"))

# ==========================================================================
# D22 : messages d'échec de git
# ==========================================================================
scratch = BASE / "git-err"
seed_add("n01", "clonage : URL absente", [("own", "x", "master", ABSENT)])
git_err("n01", scratch / "n01", "clone", "-b", "master", ABSENT, "d")
seed_add("n02", "clonage : répertoire non git", [("own", "x", "master", NONGIT_URL)])
git_err("n02", scratch / "n02", "clone", "-b", "master", NONGIT_URL, "d")
seed_add("n03", "clonage : version absente", [("own", "plain", "nope", PLAIN)])
git_err("n03", scratch / "n03", "clone", "-b", "nope", PLAIN, "d")
seed_add("n04", "clonage : hôte introuvable (réseau)", [("own", "x", "master", RESEAU)])
git_err("n04", scratch / "n04", "clone", "-b", "master", RESEAU, "d")
r = rootstock("n05")
case("n05", r, "graine distante absente", "seed-add", ABSENT)
git_err("n05", scratch / "n05", "clone", "-b", "master", ABSENT, "d")
# fetch en échec (contrôle de 0.5.4.0, branche) : origine du clone repointée vers l'absente
r = seed_add("n06", "préparation : seed-add own/plain dev", [("own", "plain", "dev", PLAIN)])
clone = r / "depots/own/plain/dev"
prep("n06b", r, (clone, ["remote", "set-url", "origin", ABSENT]))
case("n06b", r, "fetch en échec : seed-add relancé", "seed-add", str(BASE / "n06/seed"))
git_err("n06b", clone, "fetch", "--quiet")
# ls-remote en échec (contrôle de 0.5.4.0, tag)
r = seed_add("n07", "préparation : seed-add own/plain v1", [("own", "plain", "v1", PLAIN)])
clone = r / "depots/own/plain/v1"
prep("n07b", r, (clone, ["remote", "set-url", "origin", ABSENT]))
case("n07b", r, "ls-remote en échec : seed-add relancé", "seed-add", str(BASE / "n07/seed"))
git_err("n07b", clone, "ls-remote", "--tags", "origin", "refs/tags/v1", "refs/tags/v1^{}")
# checkout en échec : clé projetée dont le commit épinglé manque (checkout_detached)
#   non provoqué ici : _pinned refuse avant le checkout (rapport, §2).

(OUT / "fixture.tsv").write_text(norm(
    "cas\tlibellé\tcode\tclones:branche\ttrunk/f.txt\tdernière ligne du stderr\n"
    + "\n".join(rows) + "\n"))
print((OUT / "fixture.tsv").read_text())
