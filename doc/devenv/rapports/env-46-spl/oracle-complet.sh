#!/usr/bin/env bash
# oracle-complet.sh <ROOTSTOCK> <sortie> — ENV-46 : liste des chemins du trunk (et sha256),
# puis oracle-16.sh (rejouer-oracle.sh aux arguments d'ENV-41), puis ctest -N de chaque preset.
set -uo pipefail
R="$1"; O="$2"; ici="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$O/trunk" "$O/ctest-N"
( cd "$R/trunk" && LC_ALL=C find . -type l | LC_ALL=C sort ) > "$O/trunk/chemins.txt"
( cd "$R/trunk" && LC_ALL=C find . -type l | LC_ALL=C sort | while IFS= read -r l; do printf '%s -> %s\n' "$l" "$(readlink "$l")"; done ) > "$O/trunk/chemins-cibles.txt"
( cd "$O/trunk" && shasum -a 256 chemins.txt chemins-cibles.txt > sha256.txt; wc -l < chemins.txt > nombre.txt )
( cd "$R/trunk" && { find . -type f ! -name .scion.grafted.list; find -L . -type l; } ) > "$O/trunk/anomalies.txt"
"$ici/oracle-16.sh" "$R" "$O"; code=$?
for b in "$R"/build/host "$R"/build/qemu-* "$R"/build/nucleo-* "$R"/build/stm32f746g-* "$R"/build/samd21-*; do
  [ -d "$b" ] || continue; p=$(basename "$b")
  [ -f "$O/$p/outils.txt" ] || [ "$p" = host ] || continue
  (cd "$b" && ctest -N) > "$O/ctest-N/$p.txt" 2>&1
done
exit $code
