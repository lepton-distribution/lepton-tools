#!/bin/bash
# couples.sh — ENV-49 §1.1 : composants de STM32CubeWL par version (sous-module → tag du dépôt séparé).
T=/Users/cle_d_anton/lepton-tools-dev/tiers
comp() { local t=$1 chemin=$2 depot=$3 e
  e=$(git -C $T/STM32CubeWL ls-tree "$t" "$chemin" | awk '{print $2, $3}'); set -- $e
  if [ "$1" = commit ]; then echo "sm $(git -C $T/$depot describe --tags "$2" 2>/dev/null) (${2:0:7})"; else echo "arbre"; fi; }
for t in v1.3.0 v1.3.1 v1.4.0 v1.5.0 v1.6.0; do
  echo "$t | $(git -C $T/STM32CubeWL rev-parse --short=7 $t^{commit}) | $(git -C $T/STM32CubeWL log -1 --format=%cs $t) | $(comp $t Drivers/STM32WLxx_HAL_Driver stm32wlxx-hal-driver) | $(comp $t Drivers/CMSIS/Device/ST/STM32WLxx cmsis-device-wl) | $(comp $t Middlewares/Third_Party/SubGHz_Phy stm32-mw-subghz-phy)"
done
