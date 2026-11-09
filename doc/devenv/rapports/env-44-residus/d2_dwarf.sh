#!/usr/bin/env bash
# D2 d'ENV-44 : chemins des clones tiers dans les DWARF des binaires de <ROOTSTOCK>/build/*.
# Lecture seule. Usage : d2_dwarf.sh <ROOTSTOCK>
set -uo pipefail
R="$1"
motif_tiers="depots/tiers"
motif_trunk="$R/trunk/sys/root/src/kernel/dev/arch/cortexm/stm32f4xx/hal_driver"
printf '%-32s %-40s %8s %8s %8s\n' preset elf tiers hal_trunk debug_sect
for b in "$R"/build/*/; do
    p="$(basename "$b")"
    for elf in $(find "$b" -maxdepth 2 -name '*.elf' -type f 2>/dev/null); do
        sect="$(arm-none-eabi-readelf -S -W "$elf" 2>/dev/null | grep -oE '\.debug_[a-z_]+' | sort -u | tr '\n' ',')"
        dump="$(arm-none-eabi-readelf --string-dump=.debug_str --string-dump=.debug_line_str \
                 --debug-dump=rawline "$elf" 2>/dev/null)"
        nt="$(grep -c "$motif_tiers" <<< "$dump")"
        nh="$(grep -c "$motif_trunk" <<< "$dump")"
        printf '%-32s %-40s %8s %8s %s\n' "$p" "$(basename "$elf")" "$nt" "$nh" "$sect"
    done
done
