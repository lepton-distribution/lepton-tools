#!/usr/bin/env python3
"""D2 d'ENV-44 : chaîne gdb → table de l'extension → lien du trunk, sans carte.

Usage : d2-table.py <ROOTSTOCK> <srcmap.js> <preset>...
Pour chaque preset : `-file-list-exec-source-files` de gdb (MI) sur build/<preset>/lepton.elf ;
chaque `fullname` sous <ROOTSTOCK>/depots/tiers/ est passé à `toTrunk` du module compilé de
l'extension (srcmap.js), avec la table de `lepton seed status --json` construite comme
`debug.ts` (load). Attendu : chemin rendu sous le trunk, existant, de realpath = fullname.
Code 0 si tout est conforme et qu'au moins une source tierce est trouvée, 1 sinon.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

GDB = "/opt/local/bin/arm-none-eabi-gdb"
NODE = r"""
const { sourceMap, toTrunk } = require(process.argv[1]);
const fs = require("node:fs");
const status = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const files = JSON.parse(fs.readFileSync(process.argv[3], "utf8"));
const map = sourceMap(status.trunk, status.scions.filter((s) => !s.projected_by).map((s) => s.stem),
  status.scions.filter((s) => s.projected_by && s.root && s.projection)
    .map((s) => ({ root: s.root, projection: s.projection })));
process.stdout.write(JSON.stringify(files.map((f) => [f, toTrunk(map, f, fs.existsSync)])));
"""


def sources(elf: Path) -> list[str]:
    out = subprocess.run([GDB, "-nx", "-batch", "-ex",
                          'interpreter-exec mi "-file-list-exec-source-files"', str(elf)],
                         capture_output=True, text=True).stdout
    return sorted(set(re.findall(r'fullname="([^"]+)"', out)))


def main() -> int:
    rootstock, srcmap, presets = Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3:]
    tiers, trunk = str(rootstock / "depots" / "tiers") + "/", str(rootstock / "trunk") + "/"
    work = Path(os.environ.get("TMPDIR", "/tmp")) / "env-44-d2"
    work.mkdir(parents=True, exist_ok=True)
    status = subprocess.run(["lepton", "seed", "status", "--json"], cwd=rootstock / "trunk",
                            capture_output=True, text=True, check=True).stdout
    (work / "status.json").write_text(status)
    ok, total = True, 0
    for p in presets:
        noms = [f for f in sources(rootstock / "build" / p / "lepton.elf") if f.startswith(tiers)]
        (work / "files.json").write_text(json.dumps(noms))
        res = json.loads(subprocess.run(["node", "-e", NODE, srcmap, str(work / "status.json"),
                                         str(work / "files.json")],
                                        capture_output=True, text=True, check=True).stdout)
        bons = [f for f, t in res if t.startswith(trunk) and os.path.exists(t)
                and os.path.realpath(t) == os.path.realpath(f)]
        print(f"{p:26} sources tierces vues par gdb : {len(noms):3} ; ramenées au trunk : {len(bons):3}")
        for f, t in res:
            print(f"    {f[len(str(rootstock)) + 1:]}\n      -> {t[len(str(rootstock)) + 1:] if t.startswith(trunk) else t}")
        ok = ok and len(bons) == len(noms)
        total += len(noms)
    return 0 if ok and total else 1


if __name__ == "__main__":
    sys.exit(main())
