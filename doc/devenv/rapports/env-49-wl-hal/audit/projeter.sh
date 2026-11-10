#!/bin/bash
# projeter.sh <projections> <suffixe> <hal> <cmsis> <subghz> <cube> [<sortie>]
# ENV-49 : simule la résolution des 5 clés WL (proj.py) ; écrit <sortie>/<suffixe>-<clé>.txt (« :: » → « -- »).
# Clones de lecture : ~/lepton-tools-dev/tiers/.
S=$(cd "$(dirname "$0")" && pwd); P=$1; X=$2; O=${7:-$S/simulation}; T=/Users/cle_d_anton/lepton-tools-dev/tiers
cd $T
while read -r cle repo rev; do
  f="$O/$X-${cle//::/--}"
  python3 -I $S/proj.py "$P" "$cle" "$repo" "$rev" > "$f.txt" 2> "$f.err"
  echo "$cle $rev : $(wc -l < "$f.txt") fichiers ; $(cat "$f.err")"; [ -s "$f.err" ] || rm -f "$f.err"
done <<L
stm32wlxx-hal-driver stm32wlxx-hal-driver $3
cmsis-device-wl cmsis-device-wl $4
stm32-mw-subghz-phy stm32-mw-subghz-phy $5
stm32cubewl::utilities STM32CubeWL $6
stm32cubewl::radio-core-inc STM32CubeWL $6
L
cat "$O/$X"-*.txt | wc -l
