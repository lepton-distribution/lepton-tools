#!/usr/bin/env bash
# oracle-16.sh <ROOTSTOCK> <sortie> : rejouer-oracle.sh avec les arguments d'ENV-41 (6 QEMU, 10 cartes)
exec /Users/cle_d_anton/lepton-tools-dev/lepton-tools/scripts/oracle/rejouer-oracle.sh "$1" "$2" \
  --qemu qemu-mps2-an386-embos --qemu qemu-mps2-an386-embos-soft --qemu qemu-mps2-an386-freertos \
  --qemu qemu-mps2-an386-freertos-soft --qemu qemu-mps2-an500-embos --qemu qemu-mps2-an500-freertos \
  --carte nucleo-f429zi-embos --carte nucleo-f429zi-freertos --carte nucleo-f439zi-embos \
  --carte nucleo-f439zi-freertos --carte nucleo-wl55jc1-embos --carte nucleo-wl55jc1-freertos \
  --carte stm32f746g-disco-embos --carte stm32f746g-disco-freertos \
  --carte samd21-xplained-pro-embos --carte samd21-xplained-pro-freertos
