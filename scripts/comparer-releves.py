#!/usr/bin/env python3
"""Compare deux répertoires de relevés (attendu du Mac, obtenu sur la VM), après normalisation.

Usage : python3 -I scripts/comparer-releves.py [options] <attendu> <obtenu> [<fichier>...]

Chaque fichier régulier d'<attendu> (ou seulement les <fichier> nommés) est comparé à son
homonyme d'<obtenu>. Les deux textes sont d'abord normalisés :
  1. messages de git traduits en français ramenés à l'anglais (table TRADUCTIONS, tirée de
     `po/fr.po` de git, octet pour octet : « fatal » y est suivi d'une espace insécable U+00A0) ;
  2. ancêtres de <HOME> rangés sous `depots/.mirrors/<hôte>/` remplacés par `<HOME/..>`,
     `<HOME/../..>`… : chaque côté a son propre HOME (--home-attendu, --home-obtenu). Les relevés
     ont déjà `<HOME>` à la place du HOME ; seuls ses ancêtres (`/Users`, `/home`) restent.
Écrit une ligne par fichier (« identique », « écart », « absent »), le diff des écarts, puis
`écarts=<n> / <total>`.
Codes : 0 sans écart, 1 au moins un écart, 2 erreur d'usage.
Règle d'ORCHESTRATION §2bis (« Règles des consignes VM », ENV-62, PA-111).
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path, PurePosixPath

# git v2.47.3, po/fr.po (sha256 62fbd300…cb8b8) : msgid → msgstr, octet pour octet.
#   l. 4549-4550 : « Remote branch %s not found in upstream %s »
#   l. 22994-22995 : « fatal: » → « fatal : »
#   l. 15855-15864 : « Could not read from remote repository. … and the repository exists. » →
#   « Impossible de lire le dépôt distant. … et que le dépôt existe. » : bloc entier (stderr
#   complet, `*.git-err` d'ENV-65), puis dernière ligne seule (relayée par scion ≤ 0.6.3.2,
#   après « : »)
#   l. 4492-4493 : « Cloning into '%s'... » (ENV-66)
#   l. 20309-20310 : « unable to access '%s': %s », U+00A0 avant « : » (cas n04, ENV-66)
TRADUCTIONS: list[tuple[re.Pattern[str], str]] = [
    (re.compile("fatal : La branche distante (.*) n'a pas été trouvée dans le dépôt amont (.*)$",
                re.M),
     r"fatal: Remote branch \1 not found in upstream \2"),
    (re.compile("Impossible de lire le dépôt distant\\.\n\n"
                "Veuillez vérifier que vous avez les droits d'accès\n"
                "et que le dépôt existe\\.$", re.M),
     "Could not read from remote repository.\n\n"
     "Please make sure you have the correct access rights\n"
     "and the repository exists."),
    (re.compile(r"(?<=: )et que le dépôt existe\.$", re.M), "and the repository exists."),
    (re.compile(r"^Clonage dans '(.*)'\.\.\.$", re.M), r"Cloning into '\1'..."),
    (re.compile("impossible d'accéder à '(.*)'\u00a0: "), r"unable to access '\1': "),
    (re.compile("fatal : "), "fatal: "),
]

MIROIRS = re.compile(r"(depots/\.mirrors/[^/\s]+)(/[^\s<]*)")


def ancetres(home: str) -> list[str]:
    """Ancêtres stricts de `home`, du plus proche au plus lointain, sans la racine."""
    return [str(p) for p in PurePosixPath(home).parents if str(p) != "/"]


def normaliser(texte: str, home: str | None) -> str:
    for motif, remplacement in TRADUCTIONS:
        texte = motif.sub(remplacement, texte)
    if home:
        jetons = {a: "<HOME" + "/.." * (i + 1) + ">" for i, a in enumerate(ancetres(home))}

        def segment(m: re.Match[str]) -> str:
            chemin = m.group(2)
            for a, jeton in jetons.items():  # le plus proche d'abord
                if chemin == a or chemin.startswith(a + "/"):
                    return m.group(1) + jeton + chemin[len(a):]
            return m.group(0)

        texte = MIROIRS.sub(segment, texte)
    return texte


def lire(p: Path) -> str:
    return p.read_bytes().decode("utf-8", errors="surrogateescape")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(add_help=True, description=__doc__.splitlines()[0])
    ap.add_argument("--home-attendu", help="HOME de l'hôte qui a produit <attendu>")
    ap.add_argument("--home-obtenu", help="HOME de l'hôte qui a produit <obtenu>")
    ap.add_argument("attendu", type=Path)
    ap.add_argument("obtenu", type=Path)
    ap.add_argument("fichiers", nargs="*")
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 0 if e.code == 0 else 2
    if not a.attendu.is_dir() or not a.obtenu.is_dir():
        print("erreur : <attendu> et <obtenu> doivent être des répertoires", file=sys.stderr)
        return 2
    noms = a.fichiers or sorted(p.name for p in a.attendu.iterdir() if p.is_file())
    ecarts = 0
    for nom in noms:
        pa, po = a.attendu / nom, a.obtenu / nom
        if not pa.is_file():
            print(f"erreur : {pa} absent", file=sys.stderr)
            return 2
        if not po.is_file():
            print(f"{nom}\tabsent")
            ecarts += 1
            continue
        ta, to = normaliser(lire(pa), a.home_attendu), normaliser(lire(po), a.home_obtenu)
        if ta == to:
            print(f"{nom}\tidentique")
            continue
        ecarts += 1
        print(f"{nom}\técart")
        sys.stdout.writelines(difflib.unified_diff(
            ta.splitlines(keepends=True), to.splitlines(keepends=True),
            f"attendu/{nom}", f"obtenu/{nom}"))
    print(f"écarts={ecarts} / {len(noms)}")
    return 1 if ecarts else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
