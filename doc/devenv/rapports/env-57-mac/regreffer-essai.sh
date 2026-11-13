#!/usr/bin/env bash
# ENV-57, tâche 3 : regreffe d'un rootstock d'essai du Mac, en deux phases autour d'un
# « scion graft-update » lancé par la session elle-même (règle `ask` de .claude/settings.json,
# ENV-54 : une commande scion lancée depuis un script échapperait à la règle).
# Repris de rapports/env-53-mac/regreffer-essai.sh (relevés et bilan identiques).
#
# Usage :
#   bash regreffer-essai.sh avant <rootstock> <journaux>
#   # la session lance alors, dans cette forme (invite de Claude Code, PA-P) :
#   #   scion graft-update -v <rootstock> > <journaux>/<nom>-graft-update.log 2>&1; echo "code=$?" >> <journaux>/<nom>-graft-update.log
#   # et, s'il faut retirer une clé (qemu-gra2) :
#   #   scion graft-remove <clé> <rootstock> > <journaux>/<nom>-graft-remove.log 2>&1; echo "code=$?" >> <journaux>/<nom>-graft-remove.log
#   bash regreffer-essai.sh apres <rootstock> <journaux> [clé retirée]
# <nom> = chemin sous essais/, « / » → « _ » (affiché par la phase « avant »).
# Écrit dans <journaux>/<nom>-* : clones-{avant,apres}.txt, generate-{avant,apres}.log,
# espace-avant.code-workspace, espace.diff, liens-{avant,apres}.txt, controle/ (controler-trunk.py,
# attendu = liens d'avant), tiers-{avant,apres}/ (releve-clones.sh), check.log, bilan.txt.
# Rien n'écrit dans le rootstock que lepton generate (et scion, lancé hors du script).
set -u
export LC_ALL=C
PHASE=${1:?avant|apres}
R=$(cd "${2:?rootstock}" && pwd)
J=${3:?journaux}
RETIRE=${4:-}
X=$(cd "$(dirname "$0")" && pwd)
T=$(cd "$X/../../../.." && pwd)
Y=$T/doc/devenv/rapports/env-53-mac
C=$T/doc/devenv/rapports/env-43-mac/controler-trunk.py
A=$Y/attendu
nom=$(echo "${R#*/essais/}" | tr / _)
P=$J/$nom
mkdir -p "$J"
W=$(find "$R" -maxdepth 1 -name "*.code-workspace" | head -1)
tiers=non; [ -d "$R/depots/tiers" ] && tiers=oui

case $PHASE in
avant)
  bash "$Y/inventaire-clones.sh" "$R" > "$P-clones-avant.txt"
  lepton generate -C "$R" > "$P-generate-avant.log" 2>&1; echo "code=$?" >> "$P-generate-avant.log"
  cp "$W" "$P-espace-avant.code-workspace"
  python3 -I "$Y/liens.py" "$R/trunk" > "$P-liens-avant.txt" 2> "$P-liens-avant.compte"
  if [ $tiers = oui ]; then
    bash "$Y/releve-clones.sh" "$R" "$P-tiers-avant" > /dev/null
    du -sk "$R/depots/tiers" | cut -f1 > "$P-tiers-avant.ko"
  fi
  echo "nom $nom ; liens avant $(cat "$P-liens-avant.compte") ; generate $(tail -1 "$P-generate-avant.log") ; tiers $tiers"
  echo "journal du graft-update : $P-graft-update.log"
  ;;
apres)
  [ -f "$P-graft-update.log" ] || { echo "absent : $P-graft-update.log" >&2; exit 2; }
  bash "$Y/inventaire-clones.sh" "$R" > "$P-clones-apres.txt"
  python3 -I "$Y/liens.py" "$R/trunk" > "$P-liens-apres.txt" 2> "$P-liens-apres.compte"
  python3 -I "$C" "$R" "$P-liens-avant.txt" "$P-controle" > "$P-controle.log" 2>&1; echo "code=$?" >> "$P-controle.log"
  if [ $tiers = oui ]; then
    bash "$Y/releve-clones.sh" "$R" "$P-tiers-apres" > /dev/null; kp=$(du -sk "$R/depots/tiers" | cut -f1)
    ka=$(cat "$P-tiers-avant.ko")
    e=0; n=0; : > "$P-tiers-ecarts.txt"
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
  ;;
*)
  echo "phase inconnue : $PHASE (avant|apres)" >&2; exit 1 ;;
esac
