#!/bin/bash
# reporter.sh <sortie> — ENV-49 : fichiers modifiés par Lepton reportés sur la nouvelle version amont.
# Base amont (clones de lecture ~/lepton-tools-dev/tiers) + correctif Lepton (diff contre l'ancienne base).
set -eu
O=$1; H=$(cd "$(dirname "$0")" && pwd); T=/Users/cle_d_anton/lepton-tools-dev/tiers; mkdir -p "$O"
git -C $T/stm32-mw-subghz-phy show v1.5.0:radio_driver/radio.c > "$O/radio.c"
git -C $T/STM32CubeWL show v1.6.0:Utilities/timer/stm32_timer.h > "$O/stm32_timer.h"
patch -s --no-backup-if-mismatch "$O/radio.c" "$H/lepton-radio.patch"
patch -s --no-backup-if-mismatch "$O/stm32_timer.h" "$H/lepton-timer.patch"
echo "reportés dans $O : radio.c (SubGHz_Phy v1.5.0 + #if 0 de RadioIsChannelFree), stm32_timer.h (STM32CubeWL v1.6.0 + cmsis_compiler.h en commentaire)"
