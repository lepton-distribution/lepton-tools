#!/usr/bin/env python3
"""Contrôle du trunk d'un rootstock scion et du contenu projeté (ENV-43, C2 et C4).

Usage : python3 -I controler-trunk.py <rootstock> <attendu-liens.txt> <sortie>

Lecture seule dans le rootstock. Écrit dans <sortie> :
  liens.txt          liste « ./chemin -> cible » du trunk, triée par octets
  projetes.txt       chemins du trunk dont la cible est sous depots/tiers/
  controles.txt      bilan (une ligne par contrôle)
Code de retour : 0 si tous les contrôles sont conformes, 1 sinon, 2 sur erreur d'usage.

Contrôles :
  - liste « chemin -> cible » identique à l'attendu (casse comprise) ; à défaut, chemins seuls ;
  - aucun fichier régulier (hors .scion.grafted.list et .DS_Store), aucun lien cassé ;
  - pour chaque lien vers depots/tiers/<clé>/<version>/<rel> : <rel> suivi par git au HEAD du
    clone sous ce nom exact, et contenu du fichier = blob du HEAD (git hash-object) ;
  - état de chaque clone tiers : HEAD, origin, modifications, filtre de clone partiel.
"""
import os
import subprocess
import sys

TOLERES = {".scion.grafted.list", ".DS_Store"}


def git(clone, *args):
    return subprocess.run(["git", "-C", clone, *args], check=True,
                          capture_output=True, text=True).stdout


def main():
    if len(sys.argv) != 4:
        print(__doc__, file=sys.stderr)
        return 2
    rootstock = os.path.abspath(sys.argv[1])
    attendu, sortie = sys.argv[2], sys.argv[3]
    trunk = os.path.join(rootstock, "trunk")
    tiers = os.path.join(rootstock, "depots", "tiers")
    os.makedirs(sortie, exist_ok=True)

    liens, reguliers, casses, projetes = [], [], [], []
    for d, ds, fs in os.walk(trunk):
        for n in ds + fs:
            p = os.path.join(d, n)
            rel = "." + p[len(trunk):]
            if os.path.islink(p):
                liens.append(f"{rel} -> {os.readlink(p)}")
                if not os.path.exists(p):
                    casses.append(rel)
                cible = os.path.realpath(p)
                if cible.startswith(tiers + os.sep):
                    projetes.append((rel, cible))
            elif n in fs and n not in TOLERES:
                reguliers.append(rel)
    liens.sort(key=lambda s: s.encode())
    projetes.sort(key=lambda t: t[0].encode())

    with open(os.path.join(sortie, "liens.txt"), "w") as f:
        f.write("\n".join(liens) + "\n")
    with open(os.path.join(sortie, "projetes.txt"), "w") as f:
        f.write("".join(r + "\n" for r, _ in projetes))

    bilan, ok = [], True
    with open(attendu) as f:
        att = [l.rstrip("\n") for l in f if l.strip()]
    chemins = [l.split(" -> ")[0] for l in liens]
    chemins_att = [l.split(" -> ")[0] for l in att]
    if liens == att:
        bilan.append(f"liste chemin -> cible : identique à l'attendu ({len(liens)} liens)")
    else:
        ajoutes = sorted(set(chemins) - set(chemins_att))
        retires = sorted(set(chemins_att) - set(chemins))
        cibles = sorted(set(liens) - set(att))
        bilan.append(f"liste chemin -> cible : DIFFÈRE ({len(liens)} liens, attendu {len(att)}) ;"
                     f" chemins ajoutés {len(ajoutes)}, retirés {len(retires)},"
                     f" lignes différentes {len(cibles)}")
        bilan += [f"  + {c}" for c in ajoutes[:20]] + [f"  - {c}" for c in retires[:20]]
        bilan += [f"  ≠ {c}" for c in cibles[:20]]
        ok = False
    bilan.append(f"fichiers réguliers {len(reguliers)} {reguliers[:10]}")
    bilan.append(f"liens cassés {len(casses)} {casses[:10]}")
    ok = ok and not reguliers and not casses

    clones, ecarts_contenu, ecarts_nom = {}, [], []
    for rel, cible in projetes:
        parties = cible[len(tiers) + 1:].split(os.sep)
        clone = os.path.join(tiers, parties[0], parties[1])
        chemin = "/".join(parties[2:])
        if clone not in clones:
            arbre = {}
            for ligne in git(clone, "ls-tree", "-r", "HEAD").splitlines():
                meta, nom = ligne.split("\t", 1)
                arbre[nom] = meta.split()[2]
            clones[clone] = arbre
        blob = clones[clone].get(chemin)
        if blob is None:
            ecarts_nom.append(rel)
            continue
        h = git(clone, "hash-object", "--no-filters", cible).strip()
        if h != blob:
            ecarts_contenu.append(rel)
    bilan.append(f"projetés {len(projetes)} ; nom non suivi au HEAD (casse) {len(ecarts_nom)}"
                 f" {ecarts_nom[:10]} ; contenu ≠ HEAD {len(ecarts_contenu)} {ecarts_contenu[:10]}")
    ok = ok and not ecarts_nom and not ecarts_contenu

    for clone in sorted(clones):
        head = git(clone, "rev-parse", "HEAD").strip()
        origin = git(clone, "config", "--get", "remote.origin.url").strip()
        modifs = len(git(clone, "status", "--porcelain").splitlines())
        try:
            filtre = git(clone, "config", "--get", "remote.origin.partialclonefilter").strip()
        except subprocess.CalledProcessError:
            filtre = "aucun"
        bilan.append(f"{os.path.relpath(clone, rootstock)} HEAD {head} origin {origin}"
                     f" modifs {modifs} filtre {filtre}")
        ok = ok and modifs == 0

    bilan.append("CONFORME" if ok else "NON CONFORME")
    with open(os.path.join(sortie, "controles.txt"), "w") as f:
        f.write("\n".join(bilan) + "\n")
    print("\n".join(bilan))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
