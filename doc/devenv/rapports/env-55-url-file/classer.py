#!/usr/bin/env python3
"""ENV-55 : classement mécanique des formes d'origine par lepton, scion et git (lecture seule).

Usage (depuis le rootstock d'essai, pour que les chemins relatifs s'y rapportent) :
  <python de lepton> -I classer.py <rootstock> <dépôt présent> <dépôt absent> <python de scion>

Pour chaque forme × variante : groupes de `_ORIGIN`, `urlparse`, résultat de
`lepton.seed.parse_location` (origine rendue ou erreur), `Origin.remote`, puis
`scion.mirror.is_remote` de la valeur que lepton écrirait dans la graine. Sortie TSV sur stdout ;
rien n'est écrit sur disque.
"""
import json
import os
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

from lepton import seed
from lepton.errors import LeptonError

rootstock, present, absent, scion_python = Path(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]


def forms(abs_path: str, rel_path: str) -> list[tuple[str, str]]:
    return [
        ("file:///abs", f"file://{abs_path}"),
        ("file://localhost/abs", f"file://localhost{abs_path}"),
        ("file:/abs", f"file:{abs_path}"),
        ("file://autre/abs", f"file://autre{abs_path}"),
        ("FILE:///abs", f"FILE://{abs_path}"),
        ("FILE://localhost/abs", f"FILE://localhost{abs_path}"),
        ("abs", abs_path),
        ("rel", rel_path),
    ]


VARIANTS = [  # (libellé, suffixe collé, --version, --path)
    ("nue", "", None, None),
    ("@master", "@master", None, None),
    (":sous", ":sous", None, None),
    ("@master:sous", "@master:sous", None, None),
    ("--version master", "", "master", None),
    ("--path sous", "", None, "sous"),
]


def rel(p: str) -> str:
    return os.path.relpath(p, rootstock)


rows = []
for target, abs_path in (("présent", present), ("absent", absent)):
    for form, text in forms(abs_path, rel(abs_path)):
        for vlabel, suffix, version, subpath in VARIANTS:
            arg = text + suffix
            m = seed._ORIGIN.match(arg)
            groups = (m.group("loc"), m.group("ver") or "", m.group("path") or "") if m else ("—", "—", "—")
            u = urlparse(groups[0]) if m else None
            row = {"cible": target, "forme": form, "variante": vlabel, "argument": arg,
                   "re.loc": groups[0], "re.ver": groups[1], "re.path": groups[2],
                   "u.scheme": u.scheme if u else "", "u.netloc": u.netloc if u else "",
                   "u.path": u.path if u else ""}
            try:
                o = seed.parse_location(arg, version, subpath, rootstock=rootstock)
                row.update({"lepton": "origine", "remote": str(o.remote), "location": o.location,
                            "version": o.version, "subpath": o.subpath, "message": ""})
            except LeptonError as e:
                row.update({"lepton": "erreur", "remote": "", "location": "", "version": "", "subpath": "",
                            "message": f"{e.message} → {e.action}"})
            rows.append(row)

# scion : is_remote de chaque emplacement que lepton écrirait (et de chaque loc brut, pour la table)
values = sorted({r["location"] for r in rows if r["location"]} | {r["re.loc"] for r in rows})
out = subprocess.run([scion_python, "-I", "-c",
                      "import json,sys\nfrom scion.mirror import is_remote\n"
                      "print(json.dumps({v: is_remote(v) for v in json.load(sys.stdin)}))"],
                     input=json.dumps(values), capture_output=True, text=True, check=True)
scion_remote = json.loads(out.stdout)
for r in rows:
    r["scion.is_remote(loc)"] = str(scion_remote[r["re.loc"]])
    r["scion.is_remote(écrit)"] = str(scion_remote[r["location"]]) if r["location"] else ""

cols = list(rows[0])
print("\t".join(cols))
for r in rows:
    print("\t".join(r[c] for c in cols))
