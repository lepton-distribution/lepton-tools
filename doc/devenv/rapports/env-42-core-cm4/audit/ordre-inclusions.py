#!/usr/bin/env python3
"""ENV-42 §1 : ordre des -I (compile_commands.json) d'une unité par preset, entrées CMSIS repérées.
Usage : ordre-inclusions.py <ROOTSTOCK> <motif d'unité> <preset>..."""
import json, os, re, shlex, sys
R, motif, presets = sys.argv[1], sys.argv[2], sys.argv[3:]
for p in presets:
    cc = json.load(open(f"{R}/build/{p}/compile_commands.json"))
    unite = next((e for e in cc if re.search(motif, e["file"])), None)
    if unite is None:
        print(f"== {p} : aucune unité « {motif} »"); continue
    args = unite.get("arguments") or shlex.split(unite["command"])
    inc = []
    for i, a in enumerate(args):
        if a == "-I" or a == "-isystem": inc.append(args[i + 1])
        elif a.startswith("-I"): inc.append(a[2:])
        elif a.startswith("-isystem") and len(a) > 8: inc.append(a[8:])
    print(f"== {p} : {os.path.relpath(unite['file'], R)} ({len(inc)} -I)")
    for n, d in enumerate(inc, 1):
        d2 = re.sub(r".*/sys/root/src/", "", d)
        marque = " <==" if re.search(r"cmsis|CMSIS", d2) else ""
        if marque or n <= 3: print(f"  {n:3d} {d2}{marque}")
