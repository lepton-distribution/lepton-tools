#!/usr/bin/env python3
"""Migration des XML mklepton du format 1 (implicite) vers le format 2 (ENV-4, CFG-8).

Usage :
    migrer-xml-mklepton.py [--cible cortexm_lepton] [--verifier] FICHIER.xml...

Transformations (rapports/env-4-changements.md, PA-4) :
- <target name="<cible>"> : contenu conservé à sa place, balise retirée ; autres <target> supprimés ;
- <arch> et <cpu> supprimés ; leurs valeurs (include_absolute_path, freq) sont affichées, elles
  relèvent du module de carte CMake (LEPTON_BOARD_KERNEL_CONFIG_HEADER, LEPTON_BOARD_CPU_FREQ) ;
- attributs block et option de <cpufs> supprimés ; dest_path de <mklepton> supprimé ;
- sections <devices> fusionnées dans la première, ordre conservé ;
- version="2" ajouté à <mklepton>.

Le prologue (déclaration, commentaires avant <mklepton>) et l'épilogue sont recopiés tels quels ;
une balise par ligne est conservée (lecture ligne à ligne par cmake/components/firmware.cmake).
Idempotent : un fichier déjà au format 2 n'est pas réécrit. --verifier : n'écrit rien, code 1 si
un fichier serait modifié. Codes : 0 succès, 1 fichier à migrer (--verifier), 2 erreur.
"""
import argparse
import re
import sys
import xml.etree.ElementTree as ET

VERSION = "2"
RETIRES = ("target", "arch", "cpu")


def lire(chemin):
    with open(chemin, encoding="utf-8") as f:
        texte = f.read()
    debut = re.search(r"<mklepton[\s>/]", texte)
    fin = texte.rfind("</mklepton>")
    if not debut or fin < 0:
        raise ValueError("élément racine <mklepton> introuvable")
    fin += len("</mklepton>")
    parseur = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
    racine = ET.fromstring(texte, parser=parseur)
    return texte[:debut.start()], racine, texte[fin:]


def parent_de(racine):
    return {e: p for p in racine.iter() for e in p}


def retirer(parent, e):
    """Retire e ; l'espacement qui précède e reste celui de l'élément suivant."""
    enfants = list(parent)
    i = enfants.index(e)
    if i == len(enfants) - 1:
        # dernier enfant : sa fin (retour à la ligne avant la balise fermante) passe au précédent
        if i > 0:
            enfants[i - 1].tail = e.tail
        else:
            parent.text = e.tail
    parent.remove(e)


def deballer(parent, e):
    """Remplace e par ses enfants, à la même place."""
    enfants = list(e)
    if not enfants:
        retirer(parent, e)
        return
    i = list(parent).index(e)
    enfants[-1].tail = e.tail
    parent.remove(e)
    for k, c in enumerate(enfants):
        parent.insert(i + k, c)


def migrer(racine, cible, releves):
    if racine.get("version") == VERSION:
        restes = [e.tag for e in racine.iter() if e.tag in RETIRES]
        if restes:
            raise ValueError(f"version {VERSION} mais éléments retirés présents : {sorted(set(restes))}")
        return False
    if racine.get("version") is not None:
        raise ValueError(f"version inconnue : {racine.get('version')!r}")

    # 1. <target> : déballage de la cible retenue, suppression des autres (les plus profonds d'abord)
    while True:
        cibles = [e for e in racine.iter("target")]
        if not cibles:
            break
        t = cibles[-1]
        p = parent_de(racine)[t]
        if t.get("name") == cible:
            deballer(p, t)
        else:
            retirer(p, t)

    # 2. <arch>, <cpu> : valeurs relevées puis suppression, avec le commentaire qui les précède
    for tag in ("arch", "cpu"):
        for e in list(racine.iter(tag)):
            for a in ("include_absolute_path", "freq", "type", "dest_path"):
                if e.get(a) is not None:
                    releves.append(f"<{tag} {a}=\"{e.get(a)}\">")
            p = parent_de(racine)[e]
            freres = list(p)
            i = freres.index(e)
            if i + 1 < len(freres) and freres[i + 1].tag is ET.Comment and "\n" not in (e.tail or ""):
                retirer(p, freres[i + 1])          # commentaire sur la même ligne
            if i > 0 and freres[i - 1].tag is ET.Comment and not (freres[i - 1].tail or "").strip():
                retirer(p, freres[i - 1])          # commentaire de la ligne précédente
            retirer(p, e)

    # 3. attributs retirés
    for e in racine.iter("cpufs"):
        for a in ("block", "option"):
            e.attrib.pop(a, None)
    racine.attrib.pop("dest_path", None)

    # 4. fusion des <devices>
    sections = [e for e in racine if e.tag == "devices"]
    if len(sections) > 1:
        premiere = sections[0]
        for s in sections[1:]:
            enfants = list(s)
            if enfants:
                presents = list(premiere)
                if presents:
                    fin = presents[-1].tail                       # avant </devices>
                    sep = presents[-2].tail if len(presents) > 1 else premiere.text
                    presents[-1].tail = sep
                else:
                    fin, sep = premiere.text, premiere.text
                # indentation de la première section pour les éléments absorbés
                for c in enfants:
                    c.tail = sep
                    premiere.append(c)
                enfants[-1].tail = fin
            retirer(racine, s)

    # 5. version en premier attribut
    attrs = dict(racine.attrib)
    racine.attrib.clear()
    racine.set("version", VERSION)
    racine.attrib.update(attrs)
    return True


def ecrire(prologue, racine, epilogue):
    corps = ET.tostring(racine, encoding="unicode")
    texte = prologue + corps + epilogue
    # lignes vides laissées par les suppressions : au plus une ligne vide consécutive
    texte = re.sub(r"\n[ \t]*\n(?:[ \t]*\n)+", "\n\n", texte)
    texte = re.sub(r"[ \t]+\n", "\n", texte)
    return texte


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("fichiers", nargs="+")
    ap.add_argument("--cible", default="cortexm_lepton", help="<target name> conservé (défaut : %(default)s)")
    ap.add_argument("--verifier", action="store_true", help="n'écrit rien ; code 1 si une migration est nécessaire")
    args = ap.parse_args()

    a_migrer = 0
    for chemin in args.fichiers:
        try:
            prologue, racine, epilogue = lire(chemin)
            releves = []
            modifie = migrer(racine, args.cible, releves)
        except (ET.ParseError, ValueError, OSError) as err:
            print(f"{chemin} : erreur : {err}", file=sys.stderr)
            return 2
        if not modifie:
            print(f"{chemin} : déjà au format {VERSION}")
            continue
        a_migrer += 1
        if args.verifier:
            print(f"{chemin} : à migrer")
            continue
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(ecrire(prologue, racine, epilogue))
        print(f"{chemin} : migré ; valeurs retirées : {' '.join(releves) or 'aucune'}")
    return 1 if (args.verifier and a_migrer) else 0


if __name__ == "__main__":
    sys.exit(main())
