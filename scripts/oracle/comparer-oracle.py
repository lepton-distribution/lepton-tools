#!/usr/bin/env python3
"""comparer-oracle.py — compare deux captures de capturer-oracle.sh.

Usage : comparer-oracle.py <oracle-référence> <oracle-nouveau>

Compare les empreintes, les tailles de sections et l'ensemble des symboles
(nom, type, taille). Les adresses ne sont pas comparées : un changement d'ordre
d'édition de liens ne compte pas comme régression.

Code de retour :
  0  symboles et sections identiques (les empreintes peuvent différer)
  1  écart de symboles ou de sections (détail sur la sortie standard)
  2  capture incomplète ou illisible
"""
import sys
from pathlib import Path


def lire_paires(fichier: Path) -> dict:
    """Lit un fichier 'clé valeur...' en dictionnaire clé -> reste de la ligne."""
    table = {}
    for ligne in fichier.read_text().splitlines():
        champs = ligne.split()
        if not champs:
            continue
        cle = champs[0]
        valeur = " ".join(champs[1:])
        # Un même nom peut exister plusieurs fois (symboles locaux static) : on garde une liste.
        table.setdefault(cle, []).append(valeur)
    return {cle: sorted(vals) for cle, vals in table.items()}


def lire_empreintes(fichier: Path) -> dict:
    table = {}
    for ligne in fichier.read_text().splitlines():
        champs = ligne.split()
        if len(champs) == 2:
            # Clé = extension (elf, bin, hex) : les noms peuvent différer entre deux constructions.
            table[Path(champs[1].lstrip("*")).suffix or champs[1]] = champs[0]
    return table


def comparer_tables(nom: str, ref: dict, nouv: dict) -> int:
    absents = sorted(set(ref) - set(nouv))
    ajoutes = sorted(set(nouv) - set(ref))
    modifies = sorted(k for k in set(ref) & set(nouv) if ref[k] != nouv[k])
    for k in absents:
        print(f"{nom} retiré   : {k} {ref[k]}")
    for k in ajoutes:
        print(f"{nom} ajouté   : {k} {nouv[k]}")
    for k in modifies:
        print(f"{nom} modifié  : {k} {ref[k]} -> {nouv[k]}")
    return len(absents) + len(ajoutes) + len(modifies)


def main(argv: list) -> int:
    if len(argv) != 3:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    ref, nouv = Path(argv[1]), Path(argv[2])
    attendus = ("empreintes.txt", "sections.txt", "symboles.txt")
    for dossier in (ref, nouv):
        for f in attendus:
            if not (dossier / f).is_file():
                print(f"capture incomplète : {dossier / f}", file=sys.stderr)
                return 2

    emp_ref = lire_empreintes(ref / "empreintes.txt")
    emp_nouv = lire_empreintes(nouv / "empreintes.txt")
    for fichier in sorted(set(emp_ref) | set(emp_nouv)):
        etat = "identique" if emp_ref.get(fichier) == emp_nouv.get(fichier) else "différente"
        print(f"empreinte {fichier} : {etat}")

    ecarts = comparer_tables("section", lire_paires(ref / "sections.txt"),
                             lire_paires(nouv / "sections.txt"))
    ecarts += comparer_tables("symbole", lire_paires(ref / "symboles.txt"),
                              lire_paires(nouv / "symboles.txt"))
    print(f"bilan : {ecarts} écart(s) de sections ou de symboles")
    return 0 if ecarts == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
