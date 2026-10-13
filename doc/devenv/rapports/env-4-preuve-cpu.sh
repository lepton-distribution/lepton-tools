#!/bin/bash
# preuve-cpu.sh <mklepton> <trunk> <oracle.sha256> : écart kernel_mkconf.h limité à //#define CPU_…
set -u
M=$1; T=$2; ORA=$3; W=$(mktemp -d)
while read -r xml freq hdr cpu; do
  n=$(basename $xml .xml); mkdir -p $W/$n
  (cd $W/$n && SOURCE_DATE_EPOCH=0 $M -s $T -o $W/$n --cpu-freq $freq --kernel-config-header $hdr $xml >/dev/null 2>&1) || { echo "échec $n"; continue; }
  grep -q "^//#define CPU_" $W/$n/kernel_mkconf.h && echo "$n : ligne CPU encore présente"
  rec=$(awk -v c="$cpu" '/^#define __KERNEL_CPU_FREQ/ && !d {printf "//#define %s \n\n", c; d=1} {print}' $W/$n/kernel_mkconf.h | shasum -a 256 | cut -d' ' -f1)
  ref=$(grep " $n/kernel_mkconf.h$" $ORA | cut -d' ' -f1)
  [ "$rec" = "$ref" ] && echo "$n : identique à l'oracle après réinsertion de //#define $cpu" || echo "$n : ÉCART NON EXPLIQUÉ"
done <<L
sys/user/tauon-basic/etc/mkconf_tauon_basic_lwip_stm32f4-olimex-p407.xml 80000000 sys/user/tauon-basic/src/arch/olimex-stm32-p407/kernel_mkconf/include/user_kernel_mkconf.h CPU_ARM7
sys/user/tauon-basic/etc/mkconf_tauon_basic_qemu_mps2.xml 25000000 sys/user/tauon-basic/src/arch/qemu-mps2/kernel_mkconf/include/user_kernel_mkconf.h CPU_GNU32
sys/user/tauon-basic/etc/mkconf_tauon_basic_nucleo_f439zi.xml 168000000 sys/user/tauon-basic/src/arch/nucleo-f439zi/kernel_mkconf/include/user_kernel_mkconf.h CPU_GNU32
sys/user/tauon-basic/etc/mkconf_tauon_basic_nucleo_wl55jc1.xml 48000000 sys/user/tauon-basic/src/arch/nucleo-wl55jc1/kernel_mkconf/include/user_kernel_mkconf.h CPU_GNU32
sys/user/tauon-basic/etc/mkconf_tauon_basic_samd21_xplained_pro.xml 48000000 sys/user/tauon-basic/src/arch/samd21-xplained-pro/kernel_mkconf/include/user_kernel_mkconf.h CPU_GNU32
sys/user/tauon-basic/etc/mkconf_tauon_basic_stm32f746g_disco.xml 216000000 sys/user/tauon-basic/src/arch/stm32f746g-disco/kernel_mkconf/include/user_kernel_mkconf.h CPU_GNU32
L
rm -rf $W
