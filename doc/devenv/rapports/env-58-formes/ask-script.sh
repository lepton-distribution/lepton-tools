#!/usr/bin/env bash
# ENV-58 (D20), essai témoin, forme « script » : une commande soumise à la règle `ask`
# (`Bash(scion graft-update:*)`) lancée depuis un script, sur une cible absente.
# Usage (une commande par appel, depuis la racine de lepton-tools) :
#   bash doc/devenv/rapports/env-58-formes/ask-script.sh [<cible absente>]
# Défaut : ~/lepton-tools-dev/essais/env-58-absent (ENV-61 : env-61-absent, en argument).
# Garde : refuse une cible présente (code 2), pour qu'une acceptation par erreur reste sans effet.
# La décision (invite, classifieur) se lit dans le journal de session (env-57-mac/decisions.py).
set -u
cible="${1:-$HOME/lepton-tools-dev/essais/env-58-absent}"
if [ -e "$cible" ]; then
  echo "cible présente, rien lancé : $cible" >&2
  exit 2
fi
scion graft-update -v "$cible"
echo "code=$?"
