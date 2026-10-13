"""contenu_sections.py <map> : par section de sortie allouée, taille, remplissage (*fill*), contenu."""
import re, sys
L = open(sys.argv[1], errors="replace").read().splitlines()
i = L.index("Linker script and memory map")
sec, tailles, fill = None, {}, {}
for l in L[i + 1:]:
    m = re.match(r"^(\.\S+)(?:\s+0x([0-9a-f]+)\s+0x([0-9a-f]+))?", l)
    if m:
        sec = m.group(1)
        if sec.startswith((".debug", ".comment", ".ARM.attributes")):
            sec = None
            continue
        if m.group(3):
            tailles[sec] = int(m.group(3), 16)
        continue
    m = re.match(r"^ \*fill\*\s+0x[0-9a-f]+\s+0x([0-9a-f]+)", l)
    if m and sec:
        fill[sec] = fill.get(sec, 0) + int(m.group(1), 16)
for s in sorted(tailles):
    if tailles[s]:
        print(f"{s} taille={tailles[s]} fill={fill.get(s,0)} contenu={tailles[s]-fill.get(s,0)}")
