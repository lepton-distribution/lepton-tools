#!/usr/bin/env bash
# bancs.sh <ROOTSTOCK> <répertoire-oracle> — ENV-48 : bancs de la paire NUCLEO-WL55JC1, embOS et
# FreeRTOS, radio comprise (banc-wl55.sh d'ENV-42 ; PA-11 accordé au PA-83). Ports relevés par
# ioreg le 2026-11-10 (inversés depuis ENV-45 §1.7).
set -u
ROOT=$1 ORACLE=$2
H=$(cd "$(dirname "$0")" && pwd)
WLA=002700253431510837393937 WLA_PORT=/dev/cu.usbmodem1454303
WLB=004F003E3431510937393937 WLB_PORT=/dev/cu.usbmodem145103
W=$H/../env-42-core-cm4/banc-wl55.sh
code=0
for p in nucleo-wl55jc1-embos nucleo-wl55jc1-freertos; do
  echo "== $p"; "$W" "$ROOT" "$ORACLE" "$p" "$WLA_PORT" "$WLA" "$WLB_PORT" "$WLB"; r=$?; echo "   code $r"
  [ $r -eq 0 ] || code=1
done
exit $code
