#!/usr/bin/env python3
"""Croissance du code entre deux captures d'oracle (leçon E-1 de R43-1, ENV-43).

Usage : croissance.py <capture avant> <capture après>

Lecture seule. Lit `symboles.txt` (nom, type, taille hexadécimale ou `-`) et `sections.txt`
(nom, taille décimale) des deux captures. Écrit une ligne :

  code_symboles <Δ> .text <Δ> [<section> <Δ> ...]

- `code_symboles` : variation de la somme des tailles des symboles de code (types t, T, W) ;
- `.text` : variation de la section ;
- puis chaque autre section chargée (hors `.debug_*`) dont la taille change.

Sur Debian, `.text` varie par pas de 64 octets (bourrage d'alignement de la chaîne APT, E-1
admis au PA-74) : la non-régression se lit sur `code_symboles`, pas sur `.text` seule.
"""
import sys


def code(chemin):
    total = 0
    with open(chemin, encoding="utf-8") as f:
        for ligne in f:
            champs = ligne.split()
            if len(champs) == 3 and champs[1] in ("t", "T", "W") and champs[2] != "-":
                total += int(champs[2], 16)
    return total


def sections(chemin):
    tailles = {}
    with open(chemin, encoding="utf-8") as f:
        for ligne in f:
            champs = ligne.split()
            if len(champs) == 2 and champs[1].isdigit():
                tailles[champs[0]] = int(champs[1])
    return tailles


def main():
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    a, b = sys.argv[1], sys.argv[2]
    ca, cb = code(a + "/symboles.txt"), code(b + "/symboles.txt")
    sa, sb = sections(a + "/sections.txt"), sections(b + "/sections.txt")
    autres = [
        f"{k} {sb.get(k, 0) - sa.get(k, 0):+d}"
        for k in sorted(set(sa) | set(sb))
        if not k.startswith(".debug") and k != ".text" and sb.get(k, 0) != sa.get(k, 0)
    ]
    print(" ".join([f"code_symboles {cb - ca:+d}", f".text {sb.get('.text', 0) - sa.get('.text', 0):+d}"] + autres))
    return 0


if __name__ == "__main__":
    sys.exit(main())
