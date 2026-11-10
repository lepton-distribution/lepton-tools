#!/usr/bin/env bash
# bancs.sh <ROOTSTOCK> <répertoire-oracle> — bancs sur carte d'ENV-45, cinq sondes branchées
# ensemble, sonde choisie par numéro (PA-77). Ports relevés le 2026-11-10 (rapport §1.7).
# Écrit en flash sur les cinq cartes (PA-11 accordé au PA-77).
set -u
ROOT=$1 ORACLE=$2
H=$(cd "$(dirname "$0")" && pwd)
F429=0672FF495252717267243842 F429_PORT=/dev/cu.usbmodem1454403
F746=0671FF495351885087181231 F746_PORT=/dev/cu.usbmodem14303
SAMD=ATML2130021800003505 SAMD_PORT=/dev/cu.usbmodem14602
WLA=002700253431510837393937 WLA_PORT=/dev/cu.usbmodem145103
WLB=004F003E3431510937393937 WLB_PORT=/dev/cu.usbmodem1454303
IP=192.168.2.10
banc() { echo "== $1"; "$@"; echo "   code $?"; }
S=$H/banc-sonde.sh
banc "$S" "$ROOT" "$ORACLE" nucleo-f429zi-freertos "$F429_PORT" "$F429" "$IP"
banc "$S" "$ROOT" "$ORACLE" nucleo-f439zi-embos "$F429_PORT" "$F429" "$IP"   # image F439 sur la F429
banc "$S" "$ROOT" "$ORACLE" stm32f746g-disco-embos "$F746_PORT" "$F746"
banc "$S" "$ROOT" "$ORACLE" stm32f746g-disco-freertos "$F746_PORT" "$F746"
banc "$S" "$ROOT" "$ORACLE" samd21-xplained-pro-embos "$SAMD_PORT" "$SAMD"
banc "$S" "$ROOT" "$ORACLE" samd21-xplained-pro-freertos "$SAMD_PORT" "$SAMD"
W=$H/../env-42-core-cm4/banc-wl55.sh
banc "$W" "$ROOT" "$ORACLE" nucleo-wl55jc1-embos "$WLA_PORT" "$WLA" "$WLB_PORT" "$WLB"
banc "$W" "$ROOT" "$ORACLE" nucleo-wl55jc1-freertos "$WLA_PORT" "$WLA" "$WLB_PORT" "$WLB"
