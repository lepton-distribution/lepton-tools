#!/usr/bin/env bash
# bancs.sh <ROOTSTOCK> <répertoire-oracle> — ENV-46 : bancs NUCLEO-F429ZI embOS et FreeRTOS (PA-11),
# sonde choisie par numéro (banc-sonde.sh d'ENV-45). Port relevé par ioreg le 2026-11-10.
set -u
ROOT=$1 ORACLE=$2
H=$(cd "$(dirname "$0")" && pwd)
F429=0672FF495252717267243842 F429_PORT=/dev/cu.usbmodem1454403 IP=192.168.2.10
S=$H/../env-45-sonde/banc-sonde.sh
for p in nucleo-f429zi-embos nucleo-f429zi-freertos; do
  echo "== $p"; "$S" "$ROOT" "$ORACLE" "$p" "$F429_PORT" "$F429" "$IP"; echo "   code $?"
done
