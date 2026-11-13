#!/usr/bin/env bash
# ENV-56 : seed add réussi puis seed remove (forme des relevés 01 et 02 d'ENV-53), sur une copie
# neuve d'essais/env-11/qemu, pour comparer le scion du PATH (0.6.3.0 ou la branche) à l'autre.
# Usage : succes.sh <rootstock d'essai> <sortie brute> <sortie versionnée>
#
# Relevés : commandes (env-51-messages/releve.sh), état du rootstock (env-55-url-file/etat.sh :
# liens, liens cassés, fichiers réguliers, graine, liste greffée, depots/) après chaque commande,
# clones tiers projetés (env-53-mac/releve-clones.sh), tête et branche du clone de la famille.
# Réseau : clone public de GitHub (famille F7 et ses miroirs), comme en ENV-53.
set -u
export LC_ALL=C
C=$1 brut=$2 vers=$3
here=$(cd "$(dirname "$0")" && pwd)
RL=$here/../env-51-messages/releve.sh
ETAT=$here/../env-55-url-file/etat.sh
CLONES=$here/../env-53-mac/releve-clones.sh
URL=https://github.com/lepton-distribution/lepton-famille-stm32f7xx.git
FAM=depots/lepton/family-stm32f7xx/master
mkdir -p "$brut" "$vers"
py=$(dirname "$(realpath "$(command -v scion)")")/python
{ command -v scion; "$py" -c 'import scion; print(scion.__version__)'; } >"$brut/scion.txt"

cas() {
  local nom=$1; shift
  bash "$RL" "$brut" "$nom" "$C" "$@" >>"$brut/journal.txt" 2>&1
  printf '%s\tcode %s\t%s\n' "$nom" "$(cat "$brut/$nom.code")" "$*"
}

bash "$ETAT" "$C" "$brut/etat-depart"
cas r01 lepton seed add stm32f7xx --type famille "$URL@master" --no-cmake
bash "$ETAT" "$C" "$brut/etat-r01"
bash "$CLONES" "$C" "$brut/clones-r01" >/dev/null
{ git -C "$C/$FAM" rev-parse HEAD; git -C "$C/$FAM" branch --show-current; } >"$brut/famille-r01.txt"
cas r02 lepton seed remove stm32f7xx --no-cmake
bash "$ETAT" "$C" "$brut/etat-r02"
for f in liens casses reguliers graine grafted depots; do
  if cmp -s "$brut/etat-depart/$f.txt" "$brut/etat-r02/$f.txt"; then printf '%s = départ\n' "$f"
  else printf '%s ≠ départ (%s lignes de diff)\n' "$f" \
    "$(diff "$brut/etat-depart/$f.txt" "$brut/etat-r02/$f.txt" | grep -c '^[<>]')"; fi
done >"$brut/r02.etat"
cat "$brut/r02.etat"

# sortie versionnée : relevés normalisés (<C>, <HOME>) ; .DS_Store du Finder retiré (ENV-53 §1.5)
for f in "$brut"/r0*.* "$brut"/famille-r01.txt "$brut"/scion.txt; do
  sed -e "s#$C#<C>#g" -e "s#$HOME#<HOME>#g" "$f" | grep -v 'trunk/\.DS_Store' >"$vers/$(basename "$f")"
done
for d in etat-depart etat-r01 etat-r02 clones-r01; do
  mkdir -p "$vers/$d"
  for f in "$brut/$d"/*; do sed -e "s#$C#<C>#g" -e "s#$HOME#<HOME>#g" "$f" >"$vers/$d/$(basename "$f")"; done
done
