#!/usr/bin/env python3
"""liens.py <rootstock> : « chemin -> cible résolue relative au rootstock », trié."""
import os, sys
rs = os.path.realpath(sys.argv[1]); t = os.path.join(rs, 'trunk')
for d, _, fs in os.walk(t):
    for f in fs:
        p = os.path.join(d, f)
        if os.path.islink(p):
            print(os.path.relpath(p, t), '->', os.path.relpath(os.path.realpath(p), rs))
