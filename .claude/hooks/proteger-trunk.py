#!/usr/bin/env python3
"""Hook PreToolUse : refuse toute écriture directe dans le trunk d'un rootstock scion, et dans les
clones tiers projetés (`depots/tiers/`, ENV-41).

Le trunk est une vue de liens symboliques ; écrire dedans remplace un lien par un fichier
régulier non versionné et fait échouer `scion graft`. Les écritures se font dans le clone du
greffon (skill lepton-rootstock). Un clone tiers projeté est un dépôt tiers à une version
épinglée : ses fichiers ne se modifient jamais (P-E1 de la projection, PA-69 d'ENV-41).

Entrée : JSON Claude Code sur stdin (tool_name, tool_input, cwd).
Sortie : code 2 + message sur stderr pour bloquer ; code 0 sinon.
Un trunk est un répertoire nommé `trunk` dont le parent contient `.scion.rootstock.signature` ;
un clone tiers est sous `depots/tiers/` de ce même parent.
"""
import json
import os
import re
import sys

OUTILS_FICHIER = {"Write", "Edit", "MultiEdit", "NotebookEdit"}

# Commandes shell qui écrivent, suivies plus loin d'un chemin contenant trunk/.
ECRITURE_SHELL = re.compile(
    r"(^|[;&|(]\s*|\s)(sed\s+(-[a-zA-Z]*\s+)*-i|perl\s+-[a-zA-Z]*i|rm|mv|cp|touch|mkdir|ln|tee|"
    r"truncate|install|chmod|patch|spatch\s[^;&|]*--in-place)\b[^;&|]*\b(trunk|depots/tiers)/"
)
REDIRECTION = re.compile(r">>?\s*['\"]?[^\s;&|]*\b(trunk|depots/tiers)/")

MESSAGE = (
    "Écriture refusée dans le trunk scion ({}). Le trunk est une vue de liens : écrire dans le "
    "clone du greffon (realpath du fichier, sous depots/ mais jamais sous depots/tiers/), puis "
    "`scion graft` pour un fichier nouveau. Voir la skill lepton-rootstock."
)
MESSAGE_TIERS = (
    "Écriture refusée dans un clone tiers projeté ({}). Ses fichiers viennent d'un dépôt tiers à "
    "une version épinglée : ne jamais les modifier. Changer la version ou les motifs dans le "
    "scion/.scion/ du greffon porteur, ou fournir un fichier local par un autre greffon "
    "(exclusion !motif). Voir la skill lepton-rootstock."
)


def zone_protegee(chemin: str, cwd: str) -> str | None:
    """« trunk » si chemin (sans suivre les liens) est sous <rootstock>/trunk/, « tiers » s'il est
    sous <rootstock>/depots/tiers/, None sinon."""
    absolu = os.path.normpath(os.path.join(cwd, os.path.expanduser(chemin)))
    parties = absolu.split(os.sep)
    for i, nom in enumerate(parties):
        if i == 0:
            continue
        parent = os.sep.join(parties[:i]) or os.sep
        if nom == "trunk" and os.path.isfile(os.path.join(parent, ".scion.rootstock.signature")):
            return "trunk"
        if (nom == "depots" and parties[i + 1:i + 2] == ["tiers"]
                and os.path.isfile(os.path.join(parent, ".scion.rootstock.signature"))):
            return "tiers"
    return None


def est_dans_trunk(chemin: str, cwd: str) -> bool:
    """Vrai si chemin (sans suivre les liens) est sous <rootstock>/trunk/."""
    return zone_protegee(chemin, cwd) == "trunk"


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
        zone = zone_protegee(chemin, cwd) if chemin else None
        if zone:
            print((MESSAGE_TIERS if zone == "tiers" else MESSAGE).format(chemin), file=sys.stderr)
            return 2
    elif outil == "Bash":
        commande = entree.get("command", "")
        trouve = ECRITURE_SHELL.search(commande) or REDIRECTION.search(commande)
        if trouve:
            message = MESSAGE_TIERS if trouve.group(trouve.re.groups) == "depots/tiers" else MESSAGE
            print(message.format(commande.strip()[:200]), file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
