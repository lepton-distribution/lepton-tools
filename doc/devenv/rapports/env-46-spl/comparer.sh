#!/usr/bin/env bash
# comparer.sh <oracle-référence> <oracle-nouveau> — ENV-46 : 16 presets (comparer-oracle.py),
# journaux QEMU (comparer-journaux.py), host (mklepton, ctest), ctest -N ; sortie dans <nouveau>/comparaisons/.
set -uo pipefail
A="$1"; B="$2"; ici="$(cd "$(dirname "$0")" && pwd)"; t="$ici/../../../../scripts/oracle"
C="$B/comparaisons"; mkdir -p "$C"; code=0
Q="qemu-mps2-an386-embos qemu-mps2-an386-embos-soft qemu-mps2-an386-freertos qemu-mps2-an386-freertos-soft qemu-mps2-an500-embos qemu-mps2-an500-freertos"
K="nucleo-f429zi-embos nucleo-f429zi-freertos nucleo-f439zi-embos nucleo-f439zi-freertos nucleo-wl55jc1-embos nucleo-wl55jc1-freertos stm32f746g-disco-embos stm32f746g-disco-freertos samd21-xplained-pro-embos samd21-xplained-pro-freertos"
for p in $Q $K; do
  python3 "$t/comparer-oracle.py" "$A/$p" "$B/$p" > "$C/$p.txt" 2>&1; r=$?
  [ $r -eq 0 ] || code=1; printf '%-30s code %s\n' "$p" "$r"
done
# shellcheck disable=SC2086
python3 "$ici/comparer-journaux.py" "$A" "$B" $Q > "$C/journaux.txt" 2>&1 || code=1; cat "$C/journaux.txt"
if diff "$A/host/mklepton-empreintes.sha256" "$B/host/mklepton-empreintes.sha256" > "$C/host-mklepton.diff"; then echo "host mklepton identiques"; else echo "host mklepton DIFFÉRENTS"; code=1; fi
echo "host ctest : $(grep -h 'tests passed' "$A/host/ctest.log") | $(grep -h 'tests passed' "$B/host/ctest.log")"
n=0; d=0
for f in "$A"/ctest-N/*.txt; do p=$(basename "$f"); n=$((n+1))
  if diff <(sed 1d "$f") <(sed 1d "$B/ctest-N/$p") > /dev/null; then :; else d=$((d+1)); echo "ctest -N différent : $p"; code=1; fi
done
echo "ctest -N : $((n-d))/$n identiques"
exit $code
