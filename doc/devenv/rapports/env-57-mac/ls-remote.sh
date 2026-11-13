#!/usr/bin/env bash
# ENV-57 (repris d'ENV-53) : têtes publiées (lecture seule). Usage : ls-remote.sh > ls-remote-<hôte>.txt
set -u
G=https://github.com/lepton-distribution
court() { cut -c1-7; }
tete() { git ls-remote "$G/$1.git" "$2" | awk '{print $1}' | court; }
tag() { local r; r=$(git ls-remote "$G/$1.git" "refs/tags/$2^{}" | awk '{print $1}'); [ -n "$r" ] || r=$(git ls-remote "$G/$1.git" "refs/tags/$2" | awk '{print $1}'); echo "$r" | court; }
echo "lepton-tools main $(tete lepton-tools refs/heads/main)"
echo "seed.scions tag 0.6.3.1 $(tag seed.scions 0.6.3.1) master $(tete seed.scions refs/heads/master)"
echo "lepton-seed.scions original-tree $(tete lepton-seed.scions refs/heads/original-tree)"
for d in lepton-original-tree.scions lepton-famille-qemu-mps2 lepton-bsp-qemu-mps2-an386 lepton-bsp-qemu-mps2-an500 \
         lepton-famille-stm32f4xx lepton-bsp-nucleo-f429zi lepton-bsp-nucleo-f439zi lepton-famille-stm32wlxx \
         lepton-bsp-nucleo-wl55jc1 lepton-famille-stm32f7xx lepton-bsp-stm32f746g-disco lepton-famille-samd21 \
         lepton-bsp-samd21-xplained-pro; do
  echo "$d master $(tete $d refs/heads/master)"
done
echo "mirror-cmsis_device_f4 HEAD $(tete mirror-cmsis_device_f4 HEAD) ; 3c77349 épinglé"
for m in "mirror-stm32f4xx-hal-driver v1.8.5" "mirror-stm32f7xx-hal-driver v1.3.3" "mirror-cmsis_device_f7 v1.2.10" \
         "mirror-stm32wlxx-hal-driver v1.6.0" "mirror-cmsis-device-wl v1.4.0" "mirror-stm32-mw-subghz-phy v1.5.0" \
         "mirror-STM32CubeWL v1.6.0"; do
  # shellcheck disable=SC2086  # découpage voulu : « dépôt tag »
  set -- $m
  echo "$1 tag $2 $(tag "$1" "$2") ; HEAD $(tete "$1" HEAD)"
done
