#!/usr/bin/env bash
# E1 (ENV-13) : même SOURCE_DATE_EPOCH, même rootstock (copie), greffons famille/BSP regreffés
# depuis les nouveaux clones (après) puis depuis les anciens (avant) : empreintes comparées.
# Usage : env-13-preuve-empreintes.sh <copie du rootstock, déjà regreffée (état après)>
set -u
C=$1; cd "$C" || exit 1
set --
source depots/lepton/original/master/scripts/lepton-env.sh "$C" >/dev/null || exit 1
export SOURCE_DATE_EPOCH=1760536800 PYTHONDONTWRITEBYTECODE=1
presets="qemu-mps2-an386-embos nucleo-wl55jc1-freertos"
nouvelles="family-qemu-mps2 bsp-qemu-mps2-an386 bsp-qemu-mps2-an500 family-stm32f4xx bsp-nucleo-f429zi family-stm32wlxx bsp-nucleo-wl55jc1"
anciennes="famille::qemu-mps2 bsp::qemu-mps2-an386 bsp::qemu-mps2-an500 famille::stm32f4xx bsp::nucleo-f429zi famille::stm32wlxx bsp::nucleo-wl55jc1"

construire() {   # construire <état>
    rm -rf build/host; for p in $presets; do rm -rf "build/$p"; done
    cmake -S trunk --preset host > "build-$1.log" 2>&1 && cmake --build build/host >> "build-$1.log" 2>&1 || { echo "échec host $1"; exit 1; }
    for p in $presets; do
        { cmake -S trunk --preset "$p" && cmake --build "build/$p"; } >> "build-$1.log" 2>&1 || { echo "échec $p $1"; exit 1; }
        mkdir -p "preuve-$1/$p"
        cp "build/$p/lepton.elf" "build/$p/lepton.bin" "build/$p/lepton.hex" "preuve-$1/$p/"
        echo "== $1 $p"; (cd "preuve-$1/$p" && shasum -a 256 lepton.elf lepton.bin lepton.hex)
    done
}

construire apres
git -C depots/lepton-seed.scions/original-tree checkout -q 43d12e6 || exit 1
for k in $nouvelles; do scion graft-remove --force "lepton@$k" > /dev/null 2>&1 || { echo "échec retrait $k"; exit 1; }; done
scion seed-clone --seed depots/lepton-seed.scions/original-tree > /dev/null 2>&1 || { echo "échec seed-clone"; exit 1; }
# .DS_Store ignorés sous scion/ des anciens clones (qemu-mps2-an500 : scion/sys/.DS_Store) : conflit
# de greffe avec le noyau ; supprimés dans la copie seulement.
find depots/lepton-famille depots/lepton-bsp -path '*/scion/*' -name .DS_Store -print -delete
args=(); for k in $anciennes; do args+=(--scion "lepton@$k"); done
scion graft --force "${args[@]}" 2>&1 | tail -1
echo "liens vers anciens clones : $(find trunk -type l -exec readlink {} + | grep -c -E 'lepton-(famille|bsp)/')"
construire avant
