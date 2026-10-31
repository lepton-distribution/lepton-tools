---
name: lepton-cibles
description: Construire Lepton, l'exécuter sous QEMU (mps2-an386), le flasher et le déboguer sur NUCLEO-F429ZI et NUCLEO-WL55JC1 (cœur M4) depuis l'hôte macOS Intel ou Debian. Utiliser pour toute construction, test de fumée, lancement du banc KAL, écriture flash ou session GDB.
---

# Construire, exécuter, flasher, déboguer

Les commandes de ce fichier reprennent celles du portage, relevées en ENV-2
(`doc/devenv/rapports/env-2-outillage.md`, `env-2-cartes.md`). Chemins de source relatifs à
`scion/` du clone noyau. Toute valeur absente : la relever dans le dépôt, ne jamais la deviner.

## Construire

```bash
cmake -S <ROOTSTOCK>/trunk --list-presets
cmake -S <ROOTSTOCK>/trunk -B <ROOTSTOCK>/build/<preset> --preset <preset>
cmake --build <ROOTSTOCK>/build/<preset>
```
Les presets fixent eux-mêmes le répertoire `${sourceDir}/../build/<preset>` = `<ROOTSTOCK>/build/<preset>`
(`CMakePresets.json:13`). Le preset `host` (mklepton hôte, `<ROOTSTOCK>/build/host/mklepton`) est
prérequis de tout preset croisé (`CMakePresets.json:37`). embOS : `source <clone>/scripts/lepton-env.sh`
(exporte `LEPTON_EMBOS_ROOT`). Avant tout `ctest` à la main : `export PYTHONDONTWRITEBYTECODE=1`.
Répertoire de construction neuf pour un oracle (`rm -rf <ROOTSTOCK>/build/<preset>` avant).
Jamais de répertoire de construction dans le trunk.

| Cible | Preset | Exécutable |
| --- | --- | --- |
| QEMU `mps2-an386` | `qemu-mps2-an386-embos`, `-embos-soft`, `-freertos`, `-freertos-soft` | `<ROOTSTOCK>/build/<preset>/lepton.elf` |
| NUCLEO-F429ZI | `nucleo-f429zi-embos`, `nucleo-f429zi-freertos` (BSP `nucleo-f429zi`, ENV-6 ; `nucleo-f439zi-*` avant) | `<ROOTSTOCK>/build/<preset>/lepton.elf` |
| NUCLEO-WL55JC1 (M4) | `nucleo-wl55jc1-embos`, `nucleo-wl55jc1-freertos` (ABI soft) | `<ROOTSTOCK>/build/<preset>/lepton.elf` |

<!-- Sources : CMakePresets.json (presets par nom) ; cmake/components/firmware.cmake (lepton.elf,
     lepton.bin et lepton.hex par objcopy, lepton.map, lepton.occupation.txt : flash/RAM par
     bibliothèque ; tests/kal/kal_bench.elf) ; cibles kernel, lib, sbin, bin, bsp. -->

## QEMU

```bash
qemu-system-arm -M mps2-an386 -kernel <ROOTSTOCK>/build/<preset>/lepton.elf -nographic -monitor none -serial stdio -serial file:<tmp>/uart1.log
```
<!-- Source : tests/smoke_lsh.py (commande QEMU de --transport qemu) ; qemu-system-arm = /opt/local/bin (MacPorts). -->
Test de fumée : attendre l'invite `lepton#<n>$ `, taper `uname -a` (doit contenir
`cortexM4-qemu-mps2-an386`), conserver la console complète. Automatisé :
`ctest --preset <preset> -L smoke` (test `smoke.lsh` de `cmake/components/firmware.cmake`).
Banc KAL : `ctest --preset <preset> -L kal` (18 tests en hard, 14 en soft ; `tests/kal/CMakeLists.txt`,
`ci/run.sh`, étape « banc KAL »). Un test isolé :
`qemu-system-arm -M mps2-an386 -kernel <build>/tests/kal/kal_bench.elf -nographic -monitor none -serial null -semihosting-config enable=on,target=native,arg=kal_bench,arg=<T>`
(variable `kal_run` de `tests/kal/CMakeLists.txt`).
Débogage : QEMU avec `-s -S`, puis `arm-none-eabi-gdb <elf>` et `target remote :1234`.

## Cartes réelles

Écriture flash : uniquement après autorisation de l'utilisateur pour la session (PA-11 ou point
d'arrêt de l'étape). Vérifier d'abord quelle carte est branchée :
```bash
openocd -f <cfg> -c "init; targets; shutdown"
```

| Carte | Fichiers OpenOCD | Console série |
| --- | --- | --- |
| NUCLEO-F429ZI | `-f <BSP>/debug/openocd-nucleo-f439zi.cfg` (→ `board/st_nucleo_f4.cfg`, ST-LINK/V2-1) | `/dev/cu.usbmodem145103` (relevé ENV-11 S2, deux cartes branchées), 115200 8N1 |
| NUCLEO-WL55JC1 | `-f <ROOTSTOCK>/build/<preset>/openocd-nucleo-wl55jc1.cfg` (généré par le `CMakeLists.txt` du BSP : `<BSP-WL>/debug/openocd-nucleo-wl55jc1.cfg` — autonome depuis ENV-9 : `interface/stlink.cfg` + `target/stm32wlx.cfg`, STLINK-V3 — puis `adapter serial` si `LEPTON_BOARD_STLINK_SERIAL`) (cœur M4 uniquement) | carte A `/dev/cu.usbmodem1454303` (relevé ENV-11 S2), carte B `/dev/cu.usbmodem1454403`, 115200 8N1 |

<!-- <BSP> = sys/root/src/kernel/dev/bsp/nucleo-f429zi, <BSP-WL> = sys/root/src/kernel/dev/bsp/nucleo-wl55jc1,
     relatifs au trunk (champ openocd du manifeste, ENV-6). Sources : debug/openocd-nucleo-f439zi.cfg du BSP F429 ;
     CMakeLists.txt du BSP nucleo-wl55jc1 (cfg générée) ;
     doc/migration/validation-macos.md:26-30 (ports relevés en étape 10, à revérifier : ils
     dépendent du port USB) ; tests/smoke_lsh.py:126 (débit). Sondes : F429 ST-LINK/V2-1
     n° 0672FF495252717267243842 ; WL55 A 002700253431510837393937, B 004F003E3431510937393937
     (doc/migration/validation-nucleo-wl55jc1.md:7-10). Cible CMake équivalente : `cmake --build <build> --target flash`
     (cible flash de cmake/components/firmware.cmake). -->

Deux cartes ST-Link branchées : `interface/stlink.cfg` prend la première sonde trouvée ; toujours
ajouter `-c "adapter serial <n°>"` après `-f <cfg>` (ENV-11 S2, O8). Console série en test :
`tests/smoke_lsh.py --transport serial --port <port> --reset-command "openocd -f <cfg> -c 'adapter serial <n°>' -c 'init; reset run; shutdown'" --expect-machine <machine>`.

Flash puis vérification :
```bash
openocd -f <cfg> -c "program <elf> verify reset exit"
```
Débogage par l'éditeur (Cortex-Debug) : l'image est écrite par `load` de gdb, sans « verified »
dans la console. Preuve du flash, en lecture seule :
`openocd -f <cfg> -c "init; reset halt; verify_image <elf>; shutdown"`. NUCLEO-F429ZI : 4 octets
`0x080001ac-af` diffèrent (bourrage d'alignement entre `.isr_vector` et `.text`, non écrit par
`load`) — attendu ; NUCLEO-WL55JC1 : aucun écart (`doc/devenv/rapports/env-12-lot6.md` §10, L6-10).
Débogage : `openocd -f <cfg>` dans un terminal, puis
depuis la racine du trunk, `arm-none-eabi-gdb -x <gdbinit de la carte> <elf> -ex "target extended-remote :3333" -ex "monitor reset halt"`
(`doc/migration/debug-gcc.md:18-19` ; ce document figé cite les chemins `debug/…` de la migration :
remplacer par ceux du BSP). gdbinit de carte : F429ZI `<BSP>/debug/gdbinit-nucleo-f439zi` ;
WL55JC1 `<BSP-WL>/debug/gdbinit-nucleo-wl55jc1` ; tous sourcent `debug/gdbinit-lepton`
(commandes communes, ENV-6 Q8).

## Pièges

- NUCLEO-WL55JC1 : Lepton tourne sur le cœur M4 ; ne jamais modifier les octets d'option ni le
  démarrage du M0+.
- Hôte Mac Intel : les outils viennent de MacPorts (pas de binaires Homebrew sur Intel) ; utiliser
  ceux qui répondent à `command -v` et consignés dans `DEVENV-STATUS.md` §Versions.
- Un échec de connexion de la sonde : relever le message OpenOCD complet avant toute autre action ;
  ne pas tenter de déverrouillage ni d'effacement de masse sans accord.
