#!/usr/bin/env bash
# bancs.sh <ROOTSTOCK> <répertoire-oracle> — ENV-47 : bancs STM32F746G-DISCO embOS et FreeRTOS
# (PA-11), réseau compris, sonde choisie par numéro (banc-sonde.sh d'ENV-45). Port relevé par ioreg
# le 2026-11-10 (seule sonde branchée).
set -u
ROOT=$1 ORACLE=$2
H=$(cd "$(dirname "$0")" && pwd)
F746=0671FF495351885087181231 F746_PORT=/dev/cu.usbmodem1454303 IP=192.168.2.10
S=$H/../env-45-sonde/banc-sonde.sh
code=0
for p in stm32f746g-disco-embos stm32f746g-disco-freertos; do
  echo "== $p"; "$S" "$ROOT" "$ORACLE" "$p" "$F746_PORT" "$F746" "$IP"; r=$?; echo "   code $r"
  [ $r -eq 0 ] || code=1
done
exit $code
