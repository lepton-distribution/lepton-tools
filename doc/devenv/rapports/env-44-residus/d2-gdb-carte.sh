#!/usr/bin/env bash
# D2 d'ENV-44 : sur NUCLEO-F429ZI déjà flashée avec <ELF>, sans écriture : reset halt, arrêt sur
# main, puis sur HAL_GPIO_Init ; pile d'appels et fullname de gdb à chaque arrêt.
# Usage : d2-gdb-carte.sh <ROOTSTOCK> <ELF> <journal> [reset_config]
set -uo pipefail
r="$1"; elf="$2"; log="$3"; rc="${4:-none}"
cfg="$r/trunk/sys/root/src/kernel/dev/bsp/nucleo-f429zi/debug/openocd-nucleo-f439zi.cfg"
openocd -f "$cfg" -c "reset_config $rc" > "$log.openocd" 2>&1 &
ocd=$!
sleep 2
cd "$r/trunk" && /opt/local/bin/arm-none-eabi-gdb -nx -batch "$elf" \
    -ex "set pagination off" -ex "set confirm off" \
    -ex "target extended-remote :3333" -ex "monitor reset halt" \
    -ex "break main" -ex "break HAL_GPIO_Init" -ex "info breakpoints" \
    -ex "continue" -ex "bt 3" \
    -ex "continue" -ex "bt 6" -ex "interpreter-exec mi \"-stack-info-frame\"" \
    -ex "next" -ex "next" -ex "interpreter-exec mi \"-stack-info-frame\"" \
    -ex "monitor reset run" -ex "detach" > "$log" 2>&1
kill "$ocd" 2>/dev/null; wait "$ocd" 2>/dev/null
cat "$log"
