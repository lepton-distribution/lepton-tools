#!/usr/bin/env python3
"""proj.py <projections> <clé> <dépôt> <rév>  — simule la résolution d'une clé (projection-miroir.md §A.3-A.6).
Sortie : « chemin-du-trunk<TAB>source », triée ; motifs sans correspondance sur stderr."""
import fnmatch, subprocess, sys
proj, cle, repo, rev = sys.argv[1:5]
out = subprocess.run(['git','-C',repo,'ls-tree','-r','--full-tree',rev], capture_output=True, text=True, check=True).stdout
files = [l.split('\t',1)[1] for l in out.splitlines() if l.split()[1] == 'blob']
def match(m):
    if m == '**': return [(f, '') for f in files]
    d, _, last = m.rpartition('/')
    if last == '**': return [(f, d) for f in files if f.startswith(d + '/')]
    if any(c in last for c in '*?['):
        return [(f, d) for f in files if f.rpartition('/')[0] == d and fnmatch.fnmatchcase(f.rpartition('/')[2], last)]
    return [(f, d) for f in files if f == m]
inc, exc = [], set()
for n, l in enumerate(open(proj, encoding='utf-8'), 1):
    l = l.split('#', 1)[0].split()
    if not l or l[1] != cle.split('@')[-1] and l[0] + '@' + l[1] != cle and l[1] != cle: continue
    if len(l) == 3 and l[2].startswith('!'): exc |= {f for f, _ in match(l[2][1:])}
    elif len(l) == 4: inc.append((n, l[2], l[3]))
res = {}
for n, m, dest in inc:
    hits = [(f, b) for f, b in match(m) if f not in exc]
    if not hits: print(f'ligne {n} : motif sans correspondance : {m}', file=sys.stderr)
    for f, b in hits:
        rel = f[len(b)+1:] if b else f
        t = dest[len('scion/'):] + rel if dest.endswith('/') else dest[len('scion/'):]
        res[t] = f
for t in sorted(res): print(f'{t}\t{res[t]}')
