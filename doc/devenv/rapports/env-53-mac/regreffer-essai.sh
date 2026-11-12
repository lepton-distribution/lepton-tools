#!/usr/bin/env bash
# ENV-53, tâche 3 : regreffe d'un rootstock d'essai du Mac (forme de rapports/env-50-mac.md §4).
# Usage : bash regreffer-essai.sh <rootstock> <journaux> [clé à retirer après graft-update]
# Écrit dans <journaux>/<nom>-* (nom = chemin sous essais/, « / » → « _ ») :
#   clones-{avant,apres}.txt, generate-{avant,apres}.log, espace-avant.code-workspace, espace.diff,
#   liens-{avant,apres}.txt, graft-update.log, graft-remove.log, controle/ (controler-trunk.py,
#   attendu = liens d'avant), tiers-{avant,apres}/ (releve-clones.sh), check.log, bilan.txt.
# Lance « scion graft-update -v » (accord de l'utilisateur requis, PA-P) ; rien d'autre n'écrit
# dans le rootstock que scion et lepton generate.
set -u
export LC_ALL=C
R=$(cd "${1:?rootstock}" && pwd)
J=${2:?journaux}
RETIRE=${3:-}
X=$(cd "$(dirname "$0")" && pwd)
T=$(cd "$X/../../../.." && pwd)
C=$T/doc/devenv/rapports/env-43-mac/controler-trunk.py
A=$X/attendu
nom=$(echo "${R#*/essais/}" | tr / _)
P=$J/$nom
mkdir -p "$J"
W=$(find "$R" -maxdepth 1 -name "*.code-workspace" | head -1)

bash "$X/inventaire-clones.sh" "$R" > "$P-clones-avant.txt"
lepton generate -C "$R" > "$P-generate-avant.log" 2>&1; echo "code=$?" >> "$P-generate-avant.log"
cp "$W" "$P-espace-avant.code-workspace"
python3 -I "$X/liens.py" "$R/trunk" > "$P-liens-avant.txt" 2> "$P-liens-avant.compte"
tiers=non; [ -d "$R/depots/tiers" ] && tiers=oui
if [ $tiers = oui ]; then bash "$X/releve-clones.sh" "$R" "$P-tiers-avant" > /dev/null; ka=$(du -sk "$R/depots/tiers" | cut -f1); fi

(cd "$R" && scion graft-update -v) > "$P-graft-update.log" 2>&1; echo "code=$?" >> "$P-graft-update.log"
if [ -n "$RETIRE" ]; then
  (cd "$R" && scion graft-remove "$RETIRE") > "$P-graft-remove.log" 2>&1; echo "code=$?" >> "$P-graft-remove.log"
fi

bash "$X/inventaire-clones.sh" "$R" > "$P-clones-apres.txt"
python3 -I "$X/liens.py" "$R/trunk" > "$P-liens-apres.txt" 2> "$P-liens-apres.compte"
python3 -I "$C" "$R" "$P-liens-avant.txt" "$P-controle" > "$P-controle.log" 2>&1; echo "code=$?" >> "$P-controle.log"
if [ $tiers = oui ]; then
  bash "$X/releve-clones.sh" "$R" "$P-tiers-apres" > /dev/null; kp=$(du -sk "$R/depots/tiers" | cut -f1)
  e=0; n=0
  for f in "$P-tiers-apres"/*.extraits.txt "$P-tiers-apres"/*.sparse-checkout; do
    n=$((n+1)); cmp -s "$f" "$A/clones/${f##*/}" || { echo "ÉCART ${f##*/}" >> "$P-tiers-ecarts.txt"; e=$((e+1)); }
  done
fi
lepton check -C "$R" > "$P-check.log" 2>&1; echo "code=$?" >> "$P-check.log"
lepton generate -C "$R" > "$P-generate-apres.log" 2>&1; echo "code=$?" >> "$P-generate-apres.log"
diff "$P-espace-avant.code-workspace" "$W" > "$P-espace.diff"; de=$?

{
  echo "rootstock $R"
  echo "graft-update $(tail -1 "$P-graft-update.log") ; avancés : $(grep -c ' avancé : ' "$P-graft-update.log") ; git clone : $(grep -c 'git clone' "$P-graft-update.log") ; extraction partielle : $(grep -c 'extraction partielle,' "$P-graft-update.log") ; conflit/refus : $(grep -i -c -E 'conflit|refus' "$P-graft-update.log")"
  grep ' avancé : ' "$P-graft-update.log" | sed 's|.*/depots/|  depots/|'
  [ -n "$RETIRE" ] && echo "graft-remove $RETIRE $(tail -1 "$P-graft-remove.log")"
  echo "clones : $(diff "$P-clones-avant.txt" "$P-clones-apres.txt" | grep -c '^>') ligne(s) changée(s)"
  echo "liens avant $(cat "$P-liens-avant.compte") ; après $(cat "$P-liens-apres.compte")"
  echo "liens ajoutés $(comm -13 "$P-liens-avant.txt" "$P-liens-apres.txt" | wc -l | tr -d ' ') retirés $(comm -23 "$P-liens-avant.txt" "$P-liens-apres.txt" | wc -l | tr -d ' ')"
  echo "controler-trunk $(tail -2 "$P-controle.log" | tr '\n' ' ')"
  if [ $tiers = oui ]; then
    echo "tiers : $(wc -l < "$P-tiers-apres/clones.txt" | tr -d ' ') clone(s) ; depots/tiers ${ka} → ${kp} Ko ; extraits et sparse-checkout ≠ attendu : $e / $n"
    awk '{print "  " $1, $4, $5, $7, $8, $10, $11, $12}' "$P-tiers-apres/clones.txt"
  fi
  echo "check $(tail -1 "$P-check.log") ; generate avant $(tail -1 "$P-generate-avant.log") après $(tail -1 "$P-generate-apres.log") ; espace diff=$de"
  echo "trunk : réguliers hors .DS_Store $(find "$R/trunk" -type f ! -name .scion.grafted.list ! -name .DS_Store | wc -l | tr -d ' ') ; .DS_Store $(find "$R/trunk" -name .DS_Store | wc -l | tr -d ' ') ; cassés $(find -L "$R/trunk" -type l | wc -l | tr -d ' ')"
} > "$P-bilan.txt"
cat "$P-bilan.txt"
