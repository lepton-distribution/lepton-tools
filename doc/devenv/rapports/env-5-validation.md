# ENV-5 — Restructuration CMake du greffon noyau : validation

Session du 2026-10-13. Clone noyau `devenv/env-5` depuis `master` 49ed8fe (fusion de `devenv/env-4`).
lepton-tools `devenv/env-5` depuis `main` bf95024.

## Commandes

Oracle avant et après : `scripts/oracle/rejouer-oracle.sh` (lepton-tools), constructions neuves
(`rm -rf <ROOTSTOCK>/build/<preset>`) :

```
scripts/oracle/rejouer-oracle.sh ~/lepton doc/devenv/rapports/oracles/env-5-<avant|apres> \
  --qemu qemu-mps2-an386-{embos,embos-soft,freertos,freertos-soft} --qemu qemu-mps2-an500-{embos,freertos} \
  --carte nucleo-f439zi-{embos,freertos} --carte nucleo-wl55jc1-{embos,freertos} \
  --carte stm32f746g-disco-{embos,freertos} --carte samd21-xplained-pro-{embos,freertos}
```

- `host` : construction, `ctest` complet (`ctest.log`), empreintes mklepton (`mklepton-empreintes.sha256`).
- Chaque preset : construction (`construction.log`), `scripts/oracle/capturer-oracle.sh` sur `lepton.elf`.
- Presets QEMU : `ctest` complet (`banc-kal.log` : fumée `smoke.lsh` = T0, puis banc KAL),
  console de fumée (`fumee.log` = `smoke_lsh_uart0.log`).
- Pas de matériel (décision 2026-10-13) ; NUCLEO-F429ZI = presets `nucleo-f439zi-*`.
- Compilateur : Arm GNU Toolchain 14.2.Rel1 (binutils 2.43.1), identique pour toutes les captures (`outils.txt`).

## Oracle avant (`oracles/env-5-avant/`, état de départ 49ed8fe)

| Preset | Symboles | Sections | Sorties | Fumée | Banc KAL (ctest) |
| --- | --- | --- | --- | --- | --- |
| host | – | – | – | – | 7/7 ; empreintes mklepton = `tests/host/mklepton_empreintes.sha256` |
| qemu-mps2-an386-embos | 1583 | 22 | elf, bin, map | OK | 18/18 |
| qemu-mps2-an386-embos-soft | 1580 | 22 | elf, bin, map | OK | 14/14 |
| qemu-mps2-an386-freertos | 1623 | 21 | elf, bin, map | OK | 18/18 |
| qemu-mps2-an386-freertos-soft | 1622 | 21 | elf, bin, map | OK | 14/14 |
| qemu-mps2-an500-embos | 1545 | 22 | elf, bin, map | OK | 18/18 |
| qemu-mps2-an500-freertos | 1585 | 21 | elf, bin, map | OK | 18/18 |
| nucleo-f439zi-embos | 1690 | 22 | elf, bin, map | – | – |
| nucleo-f439zi-freertos | 1730 | 21 | elf, bin, map | – | – |
| nucleo-wl55jc1-embos | 1215 | 22 | elf, bin, map | – | – |
| nucleo-wl55jc1-freertos | 1261 | 21 | elf, bin, map | – | – |
| stm32f746g-disco-embos | 1624 | 22 | elf, bin, map | – | – |
| stm32f746g-disco-freertos | 1660 | 21 | elf, bin, map | – | – |
| samd21-xplained-pro-embos | 926 | 22 | elf, bin, map | – | – |
| samd21-xplained-pro-freertos | 976 | 21 | elf, bin, map | – | – |

Contrôle de cohérence : `comparer-oracle.py oracles/env-4-apres/<p> oracles/env-5-avant/<p>` = code 0
pour les 4 presets an386 (la fusion de `devenv/env-4` n'a rien changé). Aucun `.hex` produit
aujourd'hui (BLD-4 : à ajouter).

## Oracle après

À rejouer après la restructuration (PA-6).
