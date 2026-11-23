#!/usr/bin/env python3
"""ENV-69 : instantané d'un rootstock d'essai, pour relever les fichiers qu'une opération change.

Usage : instantane.py <rootstock> <sortie.tsv>
Ligne : <chemin relatif> <type f|l|d> <empreinte> ; f : sha256 du contenu, l : cible du lien,
d : liste triée des entrées (un répertoire change si une entrée apparaît ou disparaît).
Exclus : contenu des `.git/`, `build/`, `.DS_Store`. Les répertoires sous `trunk/` ne sont pas
relevés (seuls les liens et fichiers le sont).
"""
import hashlib
import os
import sys


def main(root: str, out: str) -> None:
    lines = []
    for d, dirs, files in os.walk(root, followlinks=False):
        rel_d = os.path.relpath(d, root)
        dirs[:] = sorted(x for x in dirs if x not in (".git",) and not (rel_d == "." and x == "build"))
        entries = sorted(dirs + [f for f in files if f != ".DS_Store"])
        if not rel_d.startswith("trunk"):
            lines.append(f"{rel_d}\td\t{hashlib.sha256(chr(0).join(entries).encode()).hexdigest()[:16]}")
        for name in sorted(files):
            if name == ".DS_Store":
                continue
            p = os.path.join(d, name)
            rel = os.path.normpath(os.path.join(rel_d, name))
            if os.path.islink(p):
                lines.append(f"{rel}\tl\t{os.readlink(p)}")
            else:
                with open(p, "rb") as fh:
                    lines.append(f"{rel}\tf\t{hashlib.sha256(fh.read()).hexdigest()[:16]}")
        # liens vers des répertoires : listés par os.walk dans dirs, jamais suivis
        for name in list(dirs):
            p = os.path.join(d, name)
            if os.path.islink(p):
                lines.append(f"{os.path.normpath(os.path.join(rel_d, name))}\tl\t{os.readlink(p)}")
    with open(out, "w") as fh:
        fh.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
