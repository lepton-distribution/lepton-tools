#!/usr/bin/env bash
# comparer-oracle-apres.sh : compare oracles/env-52-apres à oracles/env-49-apres (ENV-52, PA-91).
# Même forme que les comparaisons d'ENV-49 : binaires (comparer-oracle.py), empreintes mklepton,
# journaux de fumée et banc KAL (env-45-sonde/comparer-journaux.py), ctest du host, ctest -N.
# À lancer depuis la racine de lepton-tools, après rejouer-oracle.sh (env-45-sonde/oracle-16.sh).
set -u
R=/Users/cle_d_anton/lepton
A=doc/devenv/rapports/oracles/env-49-apres
B=doc/devenv/rapports/oracles/env-52-apres
QEMU="qemu-mps2-an386-embos qemu-mps2-an386-embos-soft qemu-mps2-an386-freertos
      qemu-mps2-an386-freertos-soft qemu-mps2-an500-embos qemu-mps2-an500-freertos"
CARTES="nucleo-f429zi-embos nucleo-f429zi-freertos nucleo-f439zi-embos nucleo-f439zi-freertos
        nucleo-wl55jc1-embos nucleo-wl55jc1-freertos stm32f746g-disco-embos stm32f746g-disco-freertos
        samd21-xplained-pro-embos samd21-xplained-pro-freertos"
mkdir -p "$B/comparaisons" "$B/ctest-N"
for p in $QEMU $CARTES; do
    python3 scripts/oracle/comparer-oracle.py "$A/$p" "$B/$p" > "$B/comparaisons/$p.txt" 2>&1
    printf '%-30s code %s\n' "$p" "$?"
done
python3 doc/devenv/rapports/env-45-sonde/comparer-journaux.py "$A" "$B" $QEMU \
    > "$B/comparaisons/journaux.txt" 2>&1
cat "$B/comparaisons/journaux.txt"
if diff "$A/host/mklepton-empreintes.sha256" "$B/host/mklepton-empreintes.sha256" \
        > "$B/comparaisons/host-mklepton.diff"; then
    echo "host mklepton identiques"
else
    echo "host mklepton DIFFÉRENTS"
fi
echo "host ctest : $(grep -h 'tests passed' "$A/host/ctest.log") | $(grep -h 'tests passed' "$B/host/ctest.log")"
n=0; ok=0
for p in host $QEMU $CARTES; do
    # depuis le répertoire de construction, comme en ENV-49 (--test-dir ajoute une ligne)
    (cd "$R/build/$p" && ctest -N) > "$B/ctest-N/$p.txt" 2>&1
    n=$((n + 1))
    cmp -s "$A/ctest-N/$p.txt" "$B/ctest-N/$p.txt" && ok=$((ok + 1)) || echo "ctest -N différent : $p"
done
echo "ctest -N : $ok/$n identiques"
