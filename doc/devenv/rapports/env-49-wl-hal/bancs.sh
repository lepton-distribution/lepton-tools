#!/usr/bin/env bash
# bancs.sh <ROOTSTOCK> <répertoire-oracle> <étiquette> — ENV-49 : bancs de la paire NUCLEO-WL55JC1,
# embOS et FreeRTOS, radio comprise, deux passes par preset (banc-wl55.sh d'ENV-42 ; PA-11 accordé
# au PA-85). Chaque passe recopie ses journaux dans env-49-wl-hal/bancs/<étiquette>-<n>/<preset>/.
# Ports relevés par ioreg le 2026-11-10 (A …1454303, B …145103, comme en ENV-48).
set -u
ROOT=$1 ORACLE=$2 ETIQ=$3
H=$(cd "$(dirname "$0")" && pwd)
WLA=002700253431510837393937 WLA_PORT=/dev/cu.usbmodem1454303
WLB=004F003E3431510937393937 WLB_PORT=/dev/cu.usbmodem145103
W=$H/../env-42-core-cm4/banc-wl55.sh
code=0
for n in 1 2; do
  for p in nucleo-wl55jc1-embos nucleo-wl55jc1-freertos; do
    echo "== passe $n $p"; "$W" "$ROOT" "$ORACLE" "$p" "$WLA_PORT" "$WLA" "$WLB_PORT" "$WLB"; r=$?
    echo "   code $r"; [ $r -eq 0 ] || code=1
    J=$H/bancs/$ETIQ-$n/$p; mkdir -p "$J"
    for f in carte-config.log carte-oracle.txt carte.log carte-detail.log fumee-carte.log radio-carte.log; do
      [ -f "$ORACLE/$p/$f" ] && cp "$ORACLE/$p/$f" "$J/"
    done
    grep -hE 'tests passed|tests failed' "$J/carte.log" 2>/dev/null | sed 's/^ */   ctest : /'
    LC_ALL=C grep -a -hE 'radiotst (tx|rx|ping|pong) :' "$J/radio-carte.log" 2>/dev/null | sed 's/^/   radio : /'
    LC_ALL=C grep -a -cE '^lepton#[0-9]+\$ +lepton-radio-(A-vers-B|B-vers-A)' "$J/radio-carte.log" 2>/dev/null | sed 's/^/   jetons reçus : /'
  done
done
exit $code
