#!/usr/bin/env python3
"""ENV-70 : graine clonée hors de sa version (D33) et cause de l'échec de git (D35).

Usage : fixture.py <seed.scions> <exécutable scion> <base> <sortie versionnée>

Forme d'env-65-scion/fixture.py : rootstocks temporaires sous <base>, bâtis comme les fixtures
de scion, dépôts sous <base>/repos, aucune URL réseau. Chaque commande relevée donne <cas>.cmd,
.out, .err, .code, .depots, l'état des clones et du trunk (env-60-scion/etat.py) et <cas>.graine :
branche et commit de la graine avant et après. Le tableau <sortie>/fixture.tsv les résume.

D33 : la graine distante est clonée par `seed-add --version`, puis mise hors de sa version à la
main (`git checkout`, consigné dans <cas>.prep). `seed-update` et `graft-update` sont lancés ici,
en processus, sur ces rootstocks temporaires seulement (fichier d'étape ENV-70, tâche 1) : aucun
rootstock existant n'est touché. L'amont de la graine reçoit un commit après le clonage, pour que
l'avance rapide soit visible.

D35 : les appels git qui portent --single-branch passent, par l'enveloppe bin/git en tête du PATH
($ENV70_GIT_SINGLE), par git 2.18.0, qui écrit l'avertissement de la VM (git 2.47.3).

Rien n'est nettoyé : <base> est supprimé entier (scripts/supprimer-essai.sh). git en anglais
(LC_ALL=C).
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

SEED_SCIONS, SCION, BASE, OUT = (Path(a) for a in sys.argv[1:5])
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(SEED_SCIONS / "tests"))
sys.path.insert(0, str(HERE.parent / "env-60-scion"))
import etat  # noqa: E402
import make_fixture  # noqa: E402

BASE = BASE.resolve()
OUT.mkdir(parents=True, exist_ok=True)
REPOS = BASE / "repos"
GIT218 = "/usr/local/git/bin/git"
ENV = {**os.environ, "LC_ALL": "C", "GIT_TERMINAL_PROMPT": "0",
       "PATH": f"{HERE / 'bin'}{os.pathsep}{os.environ['PATH']}",
       "ENV70_GIT": "/usr/bin/git", "ENV70_GITLOG": str(BASE / "gitlog.jsonl")}
ENV_SINGLE = {**ENV, "ENV70_GIT_SINGLE": GIT218}


def g(repo: Path, *args: str) -> str:
    return subprocess.run(["/usr/bin/git", *args], cwd=repo, check=True, capture_output=True,
                          text=True, env=ENV).stdout.strip()


# plain : tag v1, master, dev (forme d'ENV-65)
PLAIN = make_fixture.make_repo(REPOS / "plain", {"scion/f.txt": "v1\n"})
g(REPOS / "plain", "tag", "-a", "v1", "-m", "v1")
(REPOS / "plain/scion/f.txt").write_text("master\n")
make_fixture.commit_all(REPOS / "plain", "master")
g(REPOS / "plain", "checkout", "-q", "-b", "dev")
(REPOS / "plain/scion/f.txt").write_text("dev\n")
make_fixture.commit_all(REPOS / "plain", "dev")
g(REPOS / "plain", "checkout", "-q", "master")
# graine distante : master déclare own/plain master ; autre déclare own/plain dev ; tag t1 sur autre
GRAINE = make_fixture.make_repo(REPOS / "graine", {
    "scion/.scion/.scion.sources.list": f"own\tplain\tmaster\t{PLAIN}\n",
    "scion/.scion/.scion.ramifications": "own\tplain\tmaster\n",
})
g(REPOS / "graine", "checkout", "-q", "-b", "autre")
(REPOS / "graine/scion/.scion/.scion.sources.list").write_text(f"own\tplain\tdev\t{PLAIN}\n")
(REPOS / "graine/scion/.scion/.scion.ramifications").write_text("own\tplain\tdev\n")
make_fixture.commit_all(REPOS / "graine", "autre")
g(REPOS / "graine", "tag", "-a", "t1", "-m", "t1")
g(REPOS / "graine", "checkout", "-q", "master")
SHAS: dict[str, str] = {}


def name_commits() -> None:
    for repo, refs in (("plain", ("v1^{commit}", "master", "dev")),
                       ("graine", ("master", "autre", "t1^{commit}"))):
        for ref in refs:
            sha = g(REPOS / repo, "rev-parse", ref)
            if sha not in SHAS:
                n = sum(1 for v in SHAS.values() if v.startswith(f"<{repo}:{ref.split('^')[0]}"))
                SHAS[sha] = f"<{repo}:{ref.split('^')[0]}{'+' * n}>"


name_commits()


def advance_upstream(branch: str, label: str) -> None:
    """Un commit de plus sur <branch> de l'amont de la graine (fichier hors de scion/)."""
    g(REPOS / "graine", "checkout", "-q", branch)
    (REPOS / "graine" / f"{label}.txt").write_text(label + "\n")
    make_fixture.commit_all(REPOS / "graine", label)
    g(REPOS / "graine", "checkout", "-q", "master")
    name_commits()


rows: list[str] = []


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def norm(text: str) -> str:
    text = text.replace(str(BASE), "<B>").replace(str(Path.home()), "<HOME>")
    for sha, name in sorted(SHAS.items(), key=lambda kv: kv[1]):
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


def prep(name: str, *steps: tuple[Path, list[str]]) -> None:
    lines = []
    for cwd, args in steps:
        cwd.mkdir(parents=True, exist_ok=True)
        subprocess.run(["/usr/bin/git", *args], cwd=cwd, check=True, capture_output=True,
                       env=ENV)
        lines.append(f"(cd {cwd}) git {' '.join(args)}")
    (OUT / f"{name}.prep").write_text(norm("\n".join(lines) + "\n"))


def seed_state(top: Path | None) -> str:
    if top is None or not (top / ".git").exists():
        return "—"
    branch = g(top, "branch", "--show-current") or "détaché"
    return f"{branch}@{g(top, 'rev-parse', 'HEAD')}"


def case(name: str, r: Path, label: str, *argv: str, seed_top: Path | None = None,
         env: dict | None = None) -> None:
    before = seed_state(seed_top)
    p = subprocess.run([str(SCION), *argv], cwd=r, capture_output=True, text=True,
                       env=env or ENV)
    after = seed_state(seed_top)
    (OUT / f"{name}.cmd").write_text(norm("scion " + " ".join(argv)) + "\n")
    (OUT / f"{name}.err").write_text(norm(p.stderr))
    (OUT / f"{name}.out").write_text(norm(p.stdout))
    (OUT / f"{name}.code").write_text(f"{p.returncode}\n")
    (OUT / f"{name}.depots").write_text(norm("".join(f"{d}\n" for d in dirs(r))))
    (OUT / f"{name}.graine").write_text(norm(f"avant {before}\naprès {after}\n"))
    etat.releve(r, OUT, name, BASE, dict(SHAS))
    grafted = (r / "trunk/.scion.grafted.list").read_text().splitlines()
    last = (p.stderr.strip().splitlines() or ["—"])[-1]
    rows.append("\t".join([name, label, str(p.returncode), norm(before), norm(after),
                           str(len(grafted)), norm(" ".join(dirs(r)))[:160], norm(last)[:220]]))


def git_err(name: str, cwd: Path, git: str, *args: str) -> None:
    """Une commande git de scion, rejouée hors de scion par <git> : stderr complet."""
    cwd.mkdir(parents=True, exist_ok=True)
    p = subprocess.run([git, *args], cwd=cwd, capture_output=True, text=True, env=ENV)
    (OUT / f"{name}.git-err").write_text(norm(f"$ {git} {' '.join(args)}\ncode {p.returncode}\n"
                                              + p.stderr))


def remote_seed(name: str, label: str, version: str) -> tuple[Path, Path]:
    r = rootstock(name)
    case(name, r, label, "seed-add", "--version", version, GRAINE,
         seed_top=r / "depots/graine" / version)
    return r, r / "depots/graine" / version


# ==========================================================================
# D33 : graine distante clonée, puis hors de sa version
# ==========================================================================
SU = ("seed-update", "--seed")

# g01-g02 : témoin, graine à sa version (branche autre), l'amont avance : seed-update
r, top = remote_seed("g01", "témoin : seed-add --version autre", "autre")
advance_upstream("autre", "g01")
case("g02", r, "témoin : seed-update, graine à sa version, amont avancé", *SU, str(top / "scion"),
     seed_top=top)

# g03-g04 : graine autre remise sur master (branche locale qui suit origin/master), amont avancé
r, top = remote_seed("g03", "seed-add --version autre", "autre")
prep("g04", (top, ["checkout", "-q", "master"]))
advance_upstream("master", "g04")
case("g04", r, "seed-update, graine autre sur la branche master", *SU, str(top / "scion"),
     seed_top=top)

# g05-g06 : même forme, graft-update (graines lues dans la liste greffée)
r, top = remote_seed("g05", "seed-add --version autre", "autre")
prep("g06", (top, ["checkout", "-q", "master"]))
advance_upstream("master", "g06")
case("g06", r, "graft-update, graine autre sur la branche master", "graft-update",
     seed_top=top)

# g07-g08 : témoin graft-update, graine à sa version, amont avancé
r, top = remote_seed("g07", "témoin : seed-add --version autre", "autre")
advance_upstream("autre", "g08")
case("g08", r, "témoin : graft-update, graine à sa version, amont avancé", "graft-update",
     seed_top=top)

# g09-g11 : graine au tag t1 (HEAD détaché), puis mise sur la branche autre
r, top = remote_seed("g09", "seed-add --version t1 (tag)", "t1")
case("g10", r, "témoin : seed-update, graine au tag t1", *SU, str(top / "scion"), seed_top=top)
prep("g11", (top, ["checkout", "-q", "autre"]))
advance_upstream("autre", "g11")
case("g11", r, "seed-update, graine t1 sur la branche autre", *SU, str(top / "scion"),
     seed_top=top)

# g12 : graine autre mise en HEAD détaché sur master (sans amont)
r, top = remote_seed("g12", "seed-add --version autre", "autre")
prep("g13", (top, ["checkout", "-q", "--detach", "origin/master"]))
case("g13", r, "seed-update, graine autre détachée sur origin/master", *SU, str(top / "scion"),
     seed_top=top)

# g14-g15 : graine donnée par chemin, clone hors de depots/, sur autre ; amont avancé (témoin)
r = rootstock("g14")
mine = BASE / "g14/graine-locale"
prep("g14", (mine.parent, ["clone", "-q", "-b", "autre", GRAINE, mine.name]))
case("g14", r, "témoin : seed-add d'une graine donnée par chemin (clone, branche autre)",
     "seed-add", str(mine), seed_top=mine)
advance_upstream("autre", "g15")
case("g15", r, "témoin : seed-update, graine par chemin, amont avancé", *SU, str(mine / "scion"),
     seed_top=mine)

# g16-g17 : graine donnée par chemin, placée à la main sous depots/<x>/<y> (nom ≠ dépôt)
r = rootstock("g16")
manuel = r / "depots/manuel/travail"
prep("g16", (manuel.parent, ["clone", "-q", "-b", "autre", GRAINE, manuel.name]))
case("g16", r, "seed-add d'une graine par chemin sous depots/manuel/travail (branche autre)",
     "seed-add", str(manuel), seed_top=manuel)
advance_upstream("autre", "g17")
case("g17", r, "seed-update, même graine, amont avancé", *SU, str(manuel / "scion"),
     seed_top=manuel)

# g18-g19 : graine locale sans origin sous depots/<x>/<y> (forme d'une graine de projet)
r = rootstock("g18")
projet = r / "depots/projets/p1"
make_fixture.make_repo(projet, {
    "scion/.scion/.scion.sources.list": f"own\tplain\tmaster\t{PLAIN}\n",
    "scion/.scion/.scion.ramifications": "own\tplain\tmaster\n",
})
SHAS[g(projet, "rev-parse", "HEAD")] = "<p1>"
case("g18", r, "témoin : seed-add d'une graine locale sans origin sous depots/projets/p1",
     "seed-add", str(projet), seed_top=projet)
case("g19", r, "témoin : seed-update, même graine", *SU, str(projet / "scion"), seed_top=projet)

# g20-g21 : graine distante dont la version porte une barre (branche f/x)
g(REPOS / "graine", "branch", "f/x", "autre")
name_commits()
r, top = remote_seed("g20", "seed-add --version f/x (branche à barre)", "f/x")
prep("g21", (top, ["checkout", "-q", "master"]))
case("g21", r, "seed-update, graine f/x sur la branche master", *SU, str(top / "scion"),
     seed_top=top)

# ==========================================================================
# D35 : --single-branch par git 2.18.0 (avertissement avant la cause)
# ==========================================================================
scratch = BASE / "git-err"
r = rootstock("k01")
case("k01", r, "clé own/plain nope : seed-add --single-branch (git 2.18 pour le clone)",
     "seed-add", "--single-branch", str(seed("k01", [("own", "plain", "nope", PLAIN)])),
     env=ENV_SINGLE)
git_err("k01-218", scratch / "k01a", GIT218, "clone", "-b", "nope", "--quiet",
        "--single-branch", PLAIN, "d")
git_err("k01-250", scratch / "k01b", "/usr/bin/git", "clone", "-b", "nope", "--quiet",
        "--single-branch", PLAIN, "d")
r = rootstock("k02")
case("k02", r, "graine distante --version nope --single-branch (git 2.18 pour le clone)",
     "seed-add", "--single-branch", "--version", "nope", GRAINE, env=ENV_SINGLE)
r = rootstock("k03")
case("k03", r, "témoin : même cas que k01 par git 2.50.1",
     "seed-add", "--single-branch", str(seed("k03", [("own", "plain", "nope", PLAIN)])))

(OUT / "fixture.tsv").write_text(norm(
    "cas\tlibellé\tcode\tgraine avant\tgraine après\tlignes greffées\tdepots\t"
    "dernière ligne du stderr\n" + "\n".join(rows) + "\n"))
print((OUT / "fixture.tsv").read_text())
