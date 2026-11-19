#!/usr/bin/env python3
"""ENV-65 : clones et graines d'un rootstock comparés à leur version déclarée (lecture seule).

Usage : python3 -I inventaire.py <rootstock>...

Pour chaque rootstock, lit `trunk/.scion.grafted.list` (rootstock ordinaire) et, pour chaque
clone git distinct qu'il nomme, compare `HEAD` à la version déclarée :
- branche (locale ou distante de ce nom) : la branche courante doit être celle-là ;
- tag : `HEAD` doit être le commit du tag ;
- commit complet (40 caractères) : `HEAD` doit être ce commit ;
- `*` ou `?`, clone hors de `depots/`, dépôt du rootstock lui-même : sans objet.
Les graines (5ᵉ colonne) sont relevées de même quand elles sont clonées sous `depots/` : leur
version est le répertoire `depots/<nom>/<version>` (`cli._clone_seed`) ; une graine hors de
`depots/` est donnée par un chemin, sans version ; une graine sous `depots/` sans `origin` (graine
de projet) aussi. Enfin, les dépôts git de `depots/` (hors `.mirrors/`) que la liste ne nomme
pas (« orphelin ») sont comparés à la version que donne leur dernier répertoire : c'est le clone
qu'une greffe future réutiliserait (D25).
Seules des commandes git de lecture sont lancées (`rev-parse`, `branch --show-current`,
`for-each-ref`, `remote get-url`), avec `LC_ALL=C`. Une ligne par clone, puis un bilan par rootstock.
Codes : 0 aucun clone hors version, 1 au moins un, 2 erreur d'usage.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ENV = {**os.environ, "LC_ALL": "C"}
SHA = re.compile(r"^[0-9a-fA-F]{40}$")


def git(repo: Path, *args: str) -> str | None:
    p = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, env=ENV)
    return p.stdout.strip() if p.returncode == 0 else None


def toplevel(path: Path) -> Path | None:
    if not path.is_dir():
        return None
    top = git(path, "rev-parse", "--show-toplevel")
    return Path(top).resolve() if top else None


def verdict(clone: Path, version: str) -> tuple[str, str]:
    """(état, détail) : état « conforme », « HORS VERSION » ou « introuvable »."""
    branch = git(clone, "branch", "--show-current") or ""
    head = git(clone, "rev-parse", "HEAD") or ""
    where = f"branche {branch}" if branch else f"HEAD détaché {head[:7]}"
    if SHA.match(version):
        return ("conforme" if head.lower() == version.lower() else "HORS VERSION"), where
    if git(clone, "for-each-ref", "--count=1", "--format=%(refname)",
           f"refs/heads/{version}", f"refs/remotes/*/{version}"):
        return ("conforme" if branch == version else "HORS VERSION"), where
    tagged = git(clone, "rev-parse", "--verify", "--quiet", f"refs/tags/{version}^{{commit}}")
    if tagged:
        return ("conforme" if head == tagged else "HORS VERSION"), where + " (tag)"
    return "introuvable", where


def repositories(depots: Path) -> list[Path]:
    """Les dépôts git sous `depots/` (hors `.mirrors/`), sans descendre dans un dépôt."""
    found = []
    for dirpath, dirnames, _ in os.walk(depots):
        d = Path(dirpath)
        if d.name == ".mirrors":
            dirnames[:] = []
            continue
        if (d / ".git").exists():
            found.append(d.resolve())
            dirnames[:] = []
    return sorted(found)


def inventory(r: Path) -> int:
    r = r.resolve()
    grafted = r / "trunk/.scion.grafted.list"
    if not grafted.is_file():
        print(f"{r} : pas de trunk/.scion.grafted.list")
        return 0
    own = toplevel(r)
    clones: dict[Path, tuple[str, str]] = {}     # toplevel -> (version, clés)
    seeds: dict[Path, str] = {}
    local_seeds: set[Path] = set()
    for line in grafted.read_text().splitlines():
        f = line.split("#", 1)[0].split()           # découpage de scion (model.fields)
        if len(f) < 4:
            continue
        key, version = f"{f[0]}/{f[1]}", f[2]
        if version not in ("*", "?"):
            top = toplevel(r / f[3])
            if top is not None and top != own and top.is_relative_to(r / "depots"):
                v, keys = clones.get(top, (version, ""))
                clones[top] = (v, (keys + " " + key).strip())
        if len(f) > 4 and f[4]:
            top = toplevel(r / f[4])
            if top is not None and top != own and top.is_relative_to(r / "depots"):
                if git(top, "remote", "get-url", "origin") is None:
                    local_seeds.add(top)             # graine donnée par un chemin
                else:
                    seeds[top] = top.name            # depots/<nom>/<version>
    out = 0
    for kind, items in (("clone", {k: v for k, v in clones.items()}),
                        ("graine", {k: (v, "") for k, v in seeds.items()})):
        for top, (version, keys) in sorted(items.items()):
            state, where = verdict(top, version)
            out += state != "conforme"
            print(f"{kind}\t{top.relative_to(r)}\t{version}\t{state}\t{where}\t{keys}")
    for top in sorted(local_seeds):
        print(f"graine locale\t{top.relative_to(r)}\t-\tsans objet\t"
              f"branche {git(top, 'branch', '--show-current') or '?'}\tsans origin : chemin")
    known = set(clones) | set(seeds) | local_seeds
    orphans = [d for d in repositories(r / "depots") if d not in known]
    for top in orphans:
        if git(top, "remote", "get-url", "origin") is None:
            print(f"orphelin local\t{top.relative_to(r)}\t-\tsans objet\t"
                  f"branche {git(top, 'branch', '--show-current') or '?'}\tsans origin : dépôt local")
            continue
        state, where = verdict(top, top.name)      # depots/…/<version> (graft._wanted)
        out += state != "conforme"
        print(f"orphelin\t{top.relative_to(r)}\t{top.name}\t{state}\t{where}\thors liste greffée")
    print(f"bilan\t{r}\tclones={len(clones)}\tgraines={len(seeds)}\t"
          f"graines_locales={len(local_seeds)}\torphelins={len(orphans)}\thors_version={out}")
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    total = sum(inventory(Path(a)) for a in sys.argv[1:])
    sys.exit(1 if total else 0)
