#!/usr/bin/env bash
# preparer-copies.sh — ENV-37 : copies de travail de la famille STM32WL remises aux chemins amont.
# Usage : preparer-copies.sh <src de la famille> <destination>
# <src> = .../family-stm32wlxx/master/scion/sys/root/src ; <destination> vidée puis remplie.
# Chaque sous-répertoire de <destination> est une pseudo-racine d'un dépôt amont, à passer à
# scripts/tiers/verifier-import.sh. Le clone de la famille n'est que lu.
set -euo pipefail
src="$1"; dst="$2"
hal="$src/kernel/dev/arch/cortexm/stm32wlxx/cubemx_hal_driver"
cms="$src/kernel/core/ucore/cmsis/Device/st/stm32wlxx"
rad="$src/kernel/dev/arch/cortexm/stm32wlxx/radio_subghz_phy"
uti="$src/kernel/dev/arch/cortexm/stm32wlxx/Utilities"
rm -rf "$dst"; mkdir -p "$dst"
cp_arbre() { # <de> <vers> : copie sans .DS_Store
  mkdir -p "$2"; (cd "$1" && find . -type f ! -name .DS_Store -print0 | cpio -0pdm --quiet "$2"); }
# HAL : inc -> Inc, src -> Src (dépôt stm32wlxx-hal-driver, et STM32CubeWL Drivers/STM32WLxx_HAL_Driver)
for racine in "$dst/hal" "$dst/cube-hal/Drivers/STM32WLxx_HAL_Driver"; do
  cp_arbre "$hal/inc" "$racine/Inc"; cp_arbre "$hal/src" "$racine/Src"
  for f in LICENSE.txt README.md Release_Notes.html; do cp -p "$hal/$f" "$racine/$f"; done
done
# CMSIS device : en-têtes -> Include, system -> Source/Templates, startup/iar -> Source/Templates/iar
for racine in "$dst/cmsis" "$dst/cube-cmsis/Drivers/CMSIS/Device/ST/STM32WLxx"; do
  mkdir -p "$racine/Include" "$racine/Source/Templates/iar"
  for f in stm32wl55xx.h stm32wlxx.h system_stm32wlxx.h; do cp -p "$cms/$f" "$racine/Include/$f"; done
  cp -p "$cms/system_stm32wlxx.c" "$racine/Source/Templates/system_stm32wlxx.c"
  cp -p "$cms/startup/iar/startup_stm32wl55xx_cm4.s" "$racine/Source/Templates/iar/startup_stm32wl55xx_cm4.s"
done
# Pile radio et utilitaires : chemins identiques sous STM32CubeWL
cp_arbre "$rad" "$dst/cube-radio/Middlewares/Third_Party/SubGHz_Phy"
cp_arbre "$uti" "$dst/cube-util/Utilities"
