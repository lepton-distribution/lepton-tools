#!/usr/bin/env python3
"""map-objets.py <ref.map> <new.map> [section-prefix] — octets par fichier objet dans les sections de sortie (.text par défaut), et différences."""
import re, sys
from collections import defaultdict
def lire(p, pref):
    d = defaultdict(int); sortie = None; pend = None
    for l in open(p, errors='replace'):
        m = re.match(r'^(\.\S+)\s', l)
        if m and not l.startswith(' '): sortie = m.group(1)
        if sortie != pref: pend = None; continue
        m = re.match(r'^ (\.\S+)\s+0x[0-9a-f]+\s+0x([0-9a-f]+)\s+(\S+)', l)
        if m: d[re.sub(r'.*/', '', m.group(3))] += int(m.group(2), 16); pend = None; continue
        m = re.match(r'^ (\.\S+)$', l.rstrip())
        if m: pend = True; continue
        m = re.match(r'^\s+0x[0-9a-f]+\s+0x([0-9a-f]+)\s+(\S+)', l)
        if pend and m: d[re.sub(r'.*/', '', m.group(2))] += int(m.group(1), 16); pend = None; continue
        m = re.match(r'^ \*fill\*\s+0x[0-9a-f]+\s+0x([0-9a-f]+)', l)
        if m: d['*fill*'] += int(m.group(1), 16)
    return d
pref = sys.argv[3] if len(sys.argv) > 3 else '.text'
a, b = lire(sys.argv[1], pref), lire(sys.argv[2], pref)
print('total', sum(a.values()), '->', sum(b.values()))
for k in sorted(set(a) | set(b)):
    if a.get(k, 0) != b.get(k, 0): print(f'  {k}: {a.get(k,0)} -> {b.get(k,0)} ({b.get(k,0)-a.get(k,0):+d})')
