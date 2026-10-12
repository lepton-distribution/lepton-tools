#!/usr/bin/env python3
"""Hook PreToolUse : refuse toute écriture directe dans le trunk d'un rootstock scion.

Le trunk est une vue de liens symboliques ; écrire dedans remplace un lien par un fichier
régulier non versionné et fait échouer `scion graft`. Les écritures se font dans le clone du
greffon (skill lepton-rootstock).

Entrée : JSON Claude Code sur stdin (tool_name, tool_input, cwd).
Sortie : code 2 + message sur stderr pour bloquer ; code 0 sinon.
Un trunk est un répertoire nommé `trunk` dont le parent contient `.scion.rootstock.signature`.
"""
import json
import os
import re
import sys

OUTILS_FICHIER = {"Write", "Edit", "MultiEdit", "NotebookEdit"}

# Commandes shell qui écrivent, suivies plus loin d'un chemin contenant trunk/.
ECRITURE_SHELL = re.compile(
    r"(^|[;&|(]\s*|\s)(sed\s+(-[a-zA-Z]*\s+)*-i|perl\s+-[a-zA-Z]*i|rm|mv|cp|touch|mkdir|ln|tee|"
    r"truncate|install|chmod|patch|spatch\s[^;&|]*--in-place)\b[^;&|]*\btrunk/"
)
REDIRECTION = re.compile(r">>?\s*['\"]?[^\s;&|]*\btrunk/")

MESSAGE = (
    "Écriture refusée dans le trunk scion ({}). Le trunk est une vue de liens : écrire dans le "
    "clone du greffon (realpath du fichier, sous depots/), puis `scion graft` pour un fichier "
    "nouveau. Voir la skill lepton-rootstock."
)


def est_dans_trunk(chemin: str, cwd: str) -> bool:
    """Vrai si chemin (sans suivre les liens) est sous <rootstock>/trunk/."""
    absolu = os.path.normpath(os.path.join(cwd, os.path.expanduser(chemin)))
    parties = absolu.split(os.sep)
    for i, nom in enumerate(parties):
        if nom == "trunk" and i > 0:
            parent = os.sep.join(parties[:i]) or os.sep
            if os.path.isfile(os.path.join(parent, ".scion.rootstock.signature")):
                return True
    return False


def main() -> int:
    try:
        donnees = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0  # entrée illisible : ne pas bloquer le travail, le hook ne juge pas
    outil = donnees.get("tool_name", "")
    entree = donnees.get("tool_input", {}) or {}
    cwd = donnees.get("cwd") or os.getcwd()

    if outil in OUTILS_FICHIER:
        chemin = entree.get("file_path") or entree.get("notebook_path") or ""
        if chemin and est_dans_trunk(chemin, cwd):
            print(MESSAGE.format(chemin), file=sys.stderr)
            return 2
    elif outil == "Bash":
        commande = entree.get("command", "")
        if ECRITURE_SHELL.search(commande) or REDIRECTION.search(commande):
            print(MESSAGE.format(commande.strip()[:200]), file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
