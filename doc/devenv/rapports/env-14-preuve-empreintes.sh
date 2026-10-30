#!/usr/bin/env bash
# E1 (ENV-14) : même SOURCE_DATE_EPOCH, même rootstock (copie) ; état après (clone noyau et
# family-stm32f4xx sur devenv/env-14), puis état avant (les deux sur master) : empreintes comparées.
# Usage : env-14-preuve-empreintes.sh <copie du rootstock, état après, sans build/>
set -u
C=$1; cd "$C" || exit 1
set --
source depots/lepton/original/master/scripts/lepton-env.sh "$C" >/dev/null || exit 1
export SOURCE_DATE_EPOCH=1760536800 PYTHONDONTWRITEBYTECODE=1
presets="qemu-mps2-an386-embos nucleo-f429zi-freertos nucleo-wl55jc1-freertos"
clones="depots/lepton/original/master depots/lepton/family-stm32f4xx/master"

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

for c in $clones; do echo "$c : $(git -C "$c" branch --show-current)"; done
echo "liens : $(find trunk -type l | wc -l | tr -d ' ')"
construire apres
for c in $clones; do git -C "$c" checkout -q master || exit 1; done
scion graft --scion lepton@original::tree --scion lepton@family-stm32f4xx 2>&1 | tail -1
echo "liens : $(find trunk -type l | wc -l | tr -d ' ') ; cassés : $(find -L trunk -type l | wc -l | tr -d ' ')"
construire avant
for p in $presets; do
    if diff -r -q "preuve-avant/$p" "preuve-apres/$p" > /dev/null; then echo "$p : identiques"; else echo "$p : DIFFÉRENTS"; fi
done
