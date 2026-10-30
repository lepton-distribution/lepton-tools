#!/usr/bin/env python3
"""ENV-14 tâche 1 : feuilles du trunk × propriétaire × versionné × lu par les 15 constructions.

Lecture seule. Sortie : TSV par feuille (stdout) ; résumé par répertoire sur stderr.
Usage : env-14-inventaire.py <ROOTSTOCK> <preset>... > feuilles.tsv
"""
import collections
import os
import re
import subprocess
import sys

root = os.path.realpath(sys.argv[1])
presets = sys.argv[2:]
trunk = os.path.join(root, "trunk")

# Greffons : clé -> chemin du clone (liste greffée)
grafts = {}
for line in open(os.path.join(trunk, ".scion.grafted.list")):
    f = line.split()
    if len(f) >= 4:
        grafts[f[1]] = os.path.join(root, f[3])

# Fichiers versionnés de chaque clone
versioned = {}
for key, clone in grafts.items():
    try:
        out = subprocess.run(["git", "-C", clone, "ls-files", "-z"], capture_output=True,
                             check=True).stdout.decode()
        versioned[key] = {os.path.join(clone, p) for p in out.split("\0") if p}
    except subprocess.CalledProcessError:
        versioned[key] = None  # pas un dépôt git

# Feuilles du trunk
leaves = {}
for d, dirs, files in os.walk(trunk):
    for n in files + [x for x in dirs if os.path.islink(os.path.join(d, x))]:
        p = os.path.join(d, n)
        rel = os.path.relpath(p, trunk)
        if rel == ".scion.grafted.list":
            continue
        if not os.path.islink(p):
            leaves[rel] = ("REGULIER", "-", p)
            continue
        real = os.path.realpath(p)
        owner = next((k for k, c in grafts.items() if real.startswith(c + os.sep)), "?")
        leaves[rel] = (owner, real, p)

# Chemins lus par les constructions
pat = re.compile(re.escape(trunk) + r"/[^\s\"';:,)(\]\[=]+")
used = collections.defaultdict(set)
for pr in presets:
    b = os.path.join(root, "build", pr)
    texts = []
    deps = subprocess.run(["ninja", "-C", b, "-t", "deps"], capture_output=True, text=True).stdout
    texts.append(deps)
    for d, _, files in os.walk(b):
        for n in files:
            if n.endswith((".ninja", ".cmake", ".json", ".txt", ".rsp", ".xml", ".h", ".c", ".ld",
                           ".cfg", ".map")) or n in ("CMakeCache.txt",):
                try:
                    texts.append(open(os.path.join(d, n), errors="replace").read())
                except OSError:
                    pass
    for t in texts:
        for m in pat.findall(t):
            m = os.path.normpath(m)
            used[os.path.relpath(m, trunk)].add(pr)

def is_used(rel):
    if rel in used:
        return True
    return False

w = sys.stdout
w.write("chemin\tgreffon\tversionne\tlu\tpresets\n")
for rel in sorted(leaves):
    owner, real, _ = leaves[rel]
    v = "-" if owner in ("REGULIER", "?") or versioned.get(owner) is None else \
        ("oui" if real in versioned[owner] else "non")
    u = used.get(rel, set())
    w.write(f"{rel}\t{owner}\t{v}\t{'oui' if u else 'non'}\t{len(u)}\n")

# Répertoires cités par les constructions (include dirs) : utile pour les en-têtes non lus
dirs_used = {r for r in used if os.path.isdir(os.path.join(trunk, r))}
with open(os.environ.get("DIRS_OUT", "/dev/null"), "w") as f:
    for r in sorted(dirs_used):
        f.write(r + "\n")
