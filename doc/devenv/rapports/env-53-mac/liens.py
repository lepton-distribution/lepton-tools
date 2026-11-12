#!/usr/bin/env python3
"""ENV-53 : liste « ./chemin -> cible » d'un trunk, triée par octets (lecture seule).

Usage : python3 -I liens.py <trunk>   (sortie sur stdout)
Puis sur stderr : nombre de liens, de liens cassés et de fichiers réguliers (hors
.scion.grafted.list et .DS_Store).
"""
import os
import sys

trunk = os.path.abspath(sys.argv[1])
liens, casses, reguliers = [], 0, 0
for d, ds, fs in os.walk(trunk):
    for n in ds + fs:
        p = os.path.join(d, n)
        if os.path.islink(p):
            liens.append(f".{p[len(trunk):]} -> {os.readlink(p)}")
            casses += not os.path.exists(p)
        elif n in fs and n not in (".scion.grafted.list", ".DS_Store"):
            reguliers += 1
liens.sort(key=lambda s: s.encode())
sys.stdout.write("".join(l + "\n" for l in liens))
print(f"liens={len(liens)} casses={casses} reguliers={reguliers}", file=sys.stderr)
