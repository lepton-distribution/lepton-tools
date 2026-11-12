"""Ensemble extrait par mode : exact (non-cône) et cône minimal (répertoires parents des sources)."""
import os, subprocess, sys
from collections import defaultdict
from pathlib import Path
root = Path(sys.argv[1]).resolve()
clones = sorted(p for p in (root/"depots"/"tiers").glob("*/*") if (p/".git").exists())
src = defaultdict(set)
for dp, dn, fn in os.walk(root/"trunk"):
    for n in dn+fn:
        p = Path(dp)/n
        if p.is_symlink():
            t = Path(os.path.normpath(Path(dp)/os.readlink(p)))
            for c in clones:
                if t.is_relative_to(c): src[c].add(str(t.relative_to(c)))
def tree(c):
    out = subprocess.run(["git","-C",str(c),"ls-tree","-r","-l","HEAD"],capture_output=True,text=True).stdout
    res = {}
    for line in out.splitlines():
        meta, path = line.split("\t",1)
        mode, typ, oid, size = meta.split()
        if typ == "blob": res[path] = int(size)
    return res
print("| clone | exact : fichiers / Mo | cône minimal : répertoires / fichiers / Mo | tout : fichiers / Mo |")
print("| --- | --- | --- | --- |")
for c in clones:
    t = tree(c); s = src[c]
    dirs = sorted({str(Path(x).parent) for x in s} - {"."})
    dirs = [d for d in dirs if not any(d.startswith(o+"/") for o in dirs if o != d)]
    anc = {""}
    for d in dirs:
        parts = d.split("/")
        for i in range(1, len(parts)): anc.add("/".join(parts[:i]))
    cone = {p for p in t if any(p.startswith(d+"/") for d in dirs) or str(Path(p).parent).replace(".","",1 if str(Path(p).parent)=="." else 0) in anc}
    mb = lambda ps: sum(t[p] for p in ps)/1e6
    print(f"| `{c.parent.name}/{c.name[:10]}` | {len(s)} / {mb(s):.2f} | {len(dirs)} / {len(cone)} / {mb(cone):.1f} | {len(t)} / {mb(t):.1f} |")
    if c.parent.name == "stm32cubewl":
        print("\n".join("    "+d for d in dirs))
