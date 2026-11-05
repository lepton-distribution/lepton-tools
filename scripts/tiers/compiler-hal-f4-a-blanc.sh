#!/usr/bin/env bash
# compiler-hal-f4-a-blanc.sh — compile à blanc la HAL STM32F4 importée (ENV-34), hors du trunk
# et hors des presets, pour prouver que l'ensemble importé est complet.
#
# Usage : compiler-hal-f4-a-blanc.sh <ROOTSTOCK> <répertoire-de-sortie>
#
# Pour chaque puce (STM32F429xx, STM32F439xx) et chaque ordre d'inclusion du CMSIS-Core :
#   v330    kernel/core/ucore/cmsis/CMSIS/Include (V3.30) en tête, comme cmake/isa/armv7m.cmake
#           le fait aujourd'hui pour tous les presets M4, puis cmsis-5/CMSIS/Core/Include ;
#   cmsis5  cmsis-5/CMSIS/Core/Include seul (core_cm4.h 5.9.0) ;
# compile chaque hal_driver/Src/*.c (hors modèles *_template.c et Legacy/) avec
# -D<puce> -DUSE_HAL_DRIVER, le stm32f4xx_hal_conf.h copié sans modification du modèle
# stm32f4xx_hal_conf_template.h dans <sortie>/conf, et les inclusions <sortie>/conf,
# hal_driver/Inc, cmsis-5/Device/ST/STM32F4xx/Include, puis le CMSIS-Core de l'ordre.
# Options du cœur : celles de cmake/cpu/cortex-m4f.cmake (FPU matérielle).
#
# Produit dans <sortie>/<puce>-<ordre>/ : un .o et un .log par source, core_cm4.txt (en-tête
# retenu, relevé par -H sur stm32f4xx_hal.c), et <sortie>/resume.txt (erreurs, avertissements).
# Variable : CC (défaut arm-none-eabi-gcc).
# Code de retour : 0 si aucune erreur, 1 sinon, 2 si usage incorrect.
set -uo pipefail

erreur() { echo "compiler-hal-f4-a-blanc: $1" >&2; exit 2; }
[ $# -eq 2 ] || erreur "usage : compiler-hal-f4-a-blanc.sh <ROOTSTOCK> <répertoire-de-sortie>"
CC="${CC:-arm-none-eabi-gcc}"
command -v "$CC" > /dev/null || erreur "compilateur absent : $CC"
src="$(cd "$1" && pwd)/trunk/sys/root/src" || erreur "rootstock absent : $1"
hal="$src/kernel/dev/arch/cortexm/stm32f4xx/hal_driver"
device="$src/kernel/core/ucore/cmsis-5/Device/ST/STM32F4xx/Include"
core5="$src/kernel/core/ucore/cmsis-5/CMSIS/Core/Include"
core3="$src/kernel/core/ucore/cmsis/CMSIS/Include"
for d in "$hal/Inc" "$hal/Src" "$device" "$core5" "$core3"; do [ -d "$d" ] || erreur "absent : $d"; done
case "$2" in "$1"/trunk|"$1"/trunk/*) erreur "sortie dans le trunk interdite" ;; esac
mkdir -p "$2/conf"; sortie="$(cd "$2" && pwd)"
cp "$hal/Inc/stm32f4xx_hal_conf_template.h" "$sortie/conf/stm32f4xx_hal_conf.h"

cpu=(-mcpu=cortex-m4 -mthumb -mfpu=fpv4-sp-d16 -mfloat-abi=hard)
sources=()
for f in "$hal"/Src/*.c; do
    case "$(basename "$f")" in *_template.c) continue ;; esac
    sources+=("$f")
done

total_erreurs=0
: > "$sortie/resume.txt"
{ echo "# $("$CC" --version | head -1)"; echo "# ${#sources[@]} sources, ${cpu[*]} -O2 -Wall"; } >> "$sortie/resume.txt"
for puce in STM32F429xx STM32F439xx; do
    for ordre in v330 cmsis5; do
        d="$sortie/$puce-$ordre"; rm -rf "$d"; mkdir -p "$d"
        if [ "$ordre" = v330 ]; then cores=(-I"$core3" -I"$core5"); else cores=(-I"$core5"); fi
        opts=("${cpu[@]}" -O2 -Wall -D"$puce" -DUSE_HAL_DRIVER
              -I"$sortie/conf" -I"$hal/Inc" -I"$device" "${cores[@]}")
        ko=0; avert=0
        for f in "${sources[@]}"; do
            b="$(basename "$f" .c)"
            if ! "$CC" "${opts[@]}" -c "$f" -o "$d/$b.o" > "$d/$b.log" 2>&1; then
                ko=$((ko + 1)); echo "ÉCHEC $b" >> "$d/echecs.txt"
            fi
            n="$(grep -c 'warning:' "$d/$b.log")"; avert=$((avert + n))
        done
        "$CC" "${opts[@]}" -H -fsyntax-only "$hal/Src/stm32f4xx_hal.c" 2>&1 \
            | grep -m1 'core_cm4\.h' | sed 's/^\.* //' > "$d/core_cm4.txt"
        echo "$puce $ordre : ${#sources[@]} sources, $ko en échec, $avert avertissement(s), core_cm4.h = $(sed "s#^$src/##" "$d/core_cm4.txt")" >> "$sortie/resume.txt"
        total_erreurs=$((total_erreurs + ko))
    done
done
cat "$sortie/resume.txt"
[ "$total_erreurs" -eq 0 ]
