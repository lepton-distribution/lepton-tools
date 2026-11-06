#!/bin/sh
# ENV-42 §1 : en-têtes CMSIS-Core réellement inclus par preset (ninja -t deps, lecture seule).
# Usage : entetes-cmsis.sh <ROOTSTOCK> <sortie> <preset>...
set -eu
R=$1; OUT=$2; shift 2
mkdir -p "$OUT"
for p in "$@"; do
  b="$R/build/$p"
  ninja -C "$b" -t deps > "$OUT/$p.deps"
  # chemins normalisés relatifs à ucore/, comptés par en-tête
  python3 - "$OUT/$p.deps" > "$OUT/$p.cmsis.txt" <<'PY'
import os, re, sys, collections
c = collections.Counter(); users = collections.defaultdict(set)
obj = None
for line in open(sys.argv[1]):
    if not line.startswith(' '):
        obj = line.split(':')[0]; continue
    h = os.path.normpath(line.strip())
    m = re.search(r'ucore/(cmsis(?:-5)?/CMSIS/.*)$', h)
    if m:
        c[m.group(1)] += 1; users[m.group(1)].add(obj)
for h, n in sorted(c.items()):
    print(f"{n:5d}  {h}")
PY
  echo "== $p"; cat "$OUT/$p.cmsis.txt"
done
