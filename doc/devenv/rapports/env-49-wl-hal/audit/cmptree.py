#!/usr/bin/env python3
"""cmptree.py <repoA> <revA>[:<sousdir>] <repoB> <revB>[:<sousdir>]
Compare les blobs de deux arbres git : communs identiques, différents, propres à A, propres à B."""
import subprocess, sys
def tree(repo, spec):
    rev, _, sub = spec.partition(':')
    out = subprocess.run(['git','-C',repo,'ls-tree','-r',f'{rev}:{sub}' if sub else rev],
                         capture_output=True, text=True, check=True).stdout
    d = {}
    for l in out.splitlines():
        meta, path = l.split('\t',1)
        mode, typ, sha = meta.split()
        d[path] = (typ, sha)
    return d
a = tree(sys.argv[1], sys.argv[2]); b = tree(sys.argv[3], sys.argv[4])
same = [p for p in a if p in b and a[p]==b[p]]
diff = sorted(p for p in a if p in b and a[p]!=b[p])
oa = sorted(p for p in a if p not in b); ob = sorted(p for p in b if p not in a)
print(f'identiques {len(same)} ; différents {len(diff)} ; seulement A {len(oa)} ; seulement B {len(ob)}')
v = '-v' in sys.argv
for lab, l in (('≠', diff), ('A', oa), ('B', ob)):
    for p in (l if v else l[:15]): print(f'  {lab} {p}')
    if not v and len(l) > 15: print(f'  {lab} … ({len(l)-15} de plus)')
