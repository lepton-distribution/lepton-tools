#!/usr/bin/env python3
"""ENV-60 : état des clones et du trunk d'un rootstock temporaire (lecture seule).

Usage : etat.py <rootstock> <sortie> <nom> [<base à remplacer par <B>>]

Écrit <nom>.clones et <nom>.trunk dans <sortie>.
- .clones : pour chaque clone de depots/ (répertoire qui contient .git, hors depots/.mirrors) :
  branche courante, références qui désignent HEAD (déterministe d'un passage à l'autre, les
  empreintes des fixtures changeant à chaque construction), branches locales, fichiers suivis et
  extraits, état git (porcelain).
- .trunk : liste greffée, puis liens du trunk (chemin -> cible).
Lancé aussi par fixture.py après chaque cas.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def git(clone: Path, *args: str) -> str:
    p = subprocess.run(["git", *args], cwd=clone, capture_output=True, text=True,
                       env={**os.environ, "LC_ALL": "C"})
    return p.stdout.strip() if p.returncode == 0 else f"(git {args[0]} : code {p.returncode})"


def clones(r: Path) -> list[Path]:
    found = []
    for dirpath, dirnames, _ in os.walk(r / "depots"):
        d = Path(dirpath)
        if ".mirrors" in d.relative_to(r).parts:
            dirnames[:] = []
            continue
        if (d / ".git").exists():
            found.append(d)
            dirnames[:] = []
    return sorted(found)


def clone_state(r: Path, c: Path) -> str:
    rel = c.relative_to(r)
    branch = git(c, "branch", "--show-current") or "(HEAD détaché)"
    points = git(c, "for-each-ref", "--points-at", "HEAD", "--format=%(refname)") or "(aucune)"
    if git(c, "rev-parse", "--verify", "--quiet", "HEAD").startswith("(git"):
        points = "(HEAD sans commit)"
    local = git(c, "for-each-ref", "--format=%(refname:short)", "refs/heads") or "(aucune)"
    tracked = git(c, "ls-files")
    files = sorted(str(p.relative_to(c)) for p in c.rglob("*")
                   if p.is_file() and ".git" not in p.relative_to(c).parts)
    status = git(c, "status", "--porcelain")
    return (f"{rel}\n"
            f"  branche : {branch}\n"
            f"  HEAD = {' '.join(points.split())}\n"
            f"  branches locales : {' '.join(local.split())}\n"
            f"  fichiers suivis : {len(tracked.splitlines()) if tracked else 0}\n"
            f"  fichiers extraits : {' '.join(files) or '(aucun)'}\n"
            f"  git status : {' ; '.join(status.splitlines()) or '(propre)'}\n")


def trunk_state(r: Path) -> str:
    grafted = r / "trunk/.scion.grafted.list"
    text = "-- liste greffée\n" + (grafted.read_text() if grafted.exists() else "(absente)\n")
    links = []
    for dirpath, dirnames, filenames in os.walk(r / "trunk"):
        for name in sorted(dirnames + filenames):
            p = Path(dirpath) / name
            if p.is_symlink():
                links.append(f"{p.relative_to(r)} -> {os.readlink(p)}")
    return text + f"-- liens du trunk : {len(links)}\n" + "".join(f"{l}\n" for l in sorted(links))


def releve(r: Path, out: Path, name: str, base: Path | None = None,
           subs: dict[str, str] | None = None) -> None:
    def norm(text: str) -> str:
        if base is not None:
            text = text.replace(str(base), "<B>")
        for old, new in (subs or {}).items():
            text = text.replace(old, new)
        return text.replace(str(Path.home()), "<HOME>")
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{name}.clones").write_text(norm("".join(clone_state(r, c) for c in clones(r))
                                             or "(aucun clone)\n"))
    (out / f"{name}.trunk").write_text(norm(trunk_state(r)))


if __name__ == "__main__":
    root, out, name = Path(sys.argv[1]).resolve(), Path(sys.argv[2]), sys.argv[3]
    releve(root, out, name, Path(sys.argv[4]).resolve() if len(sys.argv) > 4 else None)
