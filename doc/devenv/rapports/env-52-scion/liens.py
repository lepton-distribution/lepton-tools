"""Liste triée « chemin -> cible » des liens d'un trunk (lecture seule)."""
import os, sys
trunk = sys.argv[1]
out = []
for d, dn, fn in os.walk(trunk):
    for n in dn + fn:
        p = os.path.join(d, n)
        if os.path.islink(p):
            out.append(f"{os.path.relpath(p, trunk)} -> {os.readlink(p)}")
print("\n".join(sorted(out)))
