#!/usr/bin/env bash
# ENV-55 : état d'un rootstock d'essai (lecture seule), pour comparer avant / après chaque essai.
# Usage : etat.sh <rootstock> <répertoire de sortie>
# Écrit : liens.txt (chemin -> cible, trié LC_ALL=C), casses.txt, reguliers.txt, graine.txt
# (empreintes des fichiers de la graine, état git de son dépôt), grafted.txt, depots.txt
# (répertoires de depots/ jusqu'à 3 niveaux, vides marqués). Résumé sur stdout.
set -u
export LC_ALL=C
r=$1 out=$2
mkdir -p "$out"
cd "$r" || exit 2
find trunk -type l | sort | while IFS= read -r l; do printf '%s -> %s\n' "$l" "$(readlink "$l")"; done >"$out/liens.txt"
find -L trunk -type l | sort >"$out/casses.txt"
find trunk -type f ! -name .scion.grafted.list | sort >"$out/reguliers.txt"
seed=$(find depots/lepton-seed -mindepth 1 -maxdepth 1 -type d | head -1)
{ (cd "$seed" && find scion/.scion -type f | sort | xargs shasum -a 256)
  printf -- '-- git status\n'; git -C "$seed" status --short
  printf -- '-- HEAD\n'; git -C "$seed" rev-parse HEAD; } >"$out/graine.txt"
cp trunk/.scion.grafted.list "$out/grafted.txt"
find depots -mindepth 1 -maxdepth 3 -type d ! -path '*/.git*' | sort | while IFS= read -r d; do
  if [ -z "$(ls -A "$d")" ]; then printf '%s (vide)\n' "$d"; else printf '%s\n' "$d"; fi
done >"$out/depots.txt"
printf 'liens %s, cassés %s, réguliers %s, graine %s\n' "$(wc -l <"$out/liens.txt" | tr -d ' ')" \
  "$(wc -l <"$out/casses.txt" | tr -d ' ')" "$(wc -l <"$out/reguliers.txt" | tr -d ' ')" \
  "$(shasum -a 256 "$out/graine.txt" | cut -c1-12)"
