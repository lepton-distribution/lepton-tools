# ENV-2 — Construction CMake actuelle

Relevé du 2026-10-13, lecture seule, clone noyau `master` 6b62af5. Chemins relatifs à `scion/` ;
`src/…` = `scion/sys/root/src/…`. Il n'existe pas de `prj/` à la racine de `scion/` ; seuls des
sous-projets SCons hérités (`tools/mklepton/prj/scons/`, `sys/user/tauon_sampleapp/prj/scons/`,
`src/kernel/net/lwip/prj`), ignorés.

## 1. Fichiers

| Fichier | Rôle |
| --- | --- |
| `CMakeLists.txt` | Entrée ; `cmake_minimum_required(VERSION 3.24)` (l. 10) ; 4 axes en cache `LEPTON_ISA`, `LEPTON_CPU`, `LEPTON_BOARD`, `LEPTON_KAL_BACKEND` (l. 14-17) ; inclut `isa/`, `cpu/`, `boards/`, `kal/` (l. 30-37), `components/kernel` et `mklepton` (l. 40-41), `components/firmware` hors hôte (l. 42-44), `components/mklepton` et `tests/host` sur l'hôte (l. 46-49) |
| `tests/host/CMakeLists.txt` | Tests hôte (label `host`) |
| `tests/kal/CMakeLists.txt` | Banc KAL (ajouté par `firmware.cmake:127` ou `:144`) |
| `src/kernel/core/ucore/freeRTOS_11-3-0/include/CMakeLists.txt` | Fichier tiers FreeRTOS, non référencé |
| `cmake/lepton_target.cmake` | INTERFACE `lepton_options` (l. 7-8) ; `lepton_freestanding()` (l. 17-24) ; `lepton_add_library()` STATIC (l. 28-35) |
| `cmake/mklepton.cmake` | `lepton_generate()` (§5) |
| `cmake/isa/{host,armv7m,armv6m}.cmake` | Flags, specs nano/nosys, `LEPTON_KAL_ARCH_DIR`, démarrage et `sbrk` dans `LEPTON_FIRMWARE_SOURCES` (`armv7m.cmake:26-28`) ; BSP `host` (`host.cmake:44-48`) |
| `cmake/cpu/{cortex-m0plus,cortex-m3,cortex-m4f,cortex-m7}.cmake` | Flags cœur, `LEPTON_EMBOS_LIB_FAMILY`, `LEPTON_FREERTOS_PORT` ; `LEPTON_FLOAT_ABI` (m4f, l. 6-19) ; `LEPTON_M7_FPU` (m7, l. 12-20) |
| `cmake/kal/{static,embos,freertos}.cmake` | Backend : `static` hôte seul (l. 8-10) ; embOS = archive binaire sous `$LEPTON_EMBOS_ROOT` (l. 13-22) + 14 sources ; FreeRTOS 11.3.0 compilé (l. 45-72) ; `main` dans `LEPTON_FIRMWARE_SOURCES` |
| `cmake/boards/*.cmake` (6) | `LEPTON_BOARD_MEMORY_LD`, `LEPTON_BSP_NAME`, `LEPTON_BSP_SOURCES`, `LEPTON_NET_STACK`, `LEPTON_BOARD_MKCONF[_TARGET]`, `LEPTON_QEMU_MACHINE`, OpenOCD, tests carte |
| `cmake/components/kernel.cmake` | Bibliothèques noyau, libc, lwIP, BSP, INTERFACE `lepton_kernel` |
| `cmake/components/firmware.cmake` | Génération mklepton, `lepton_generated`, `lepton_sbin`/`lepton_bin`, exécutable `lepton`, `flash`, tests |
| `cmake/components/mklepton.cmake` | Exécutable hôte `mklepton` (l. 7-10) |
| `cmake/toolchains/arm-none-eabi.cmake` | `-Os` (l. 15), `LINK_GROUP:RESCAN` = `--start-group/--end-group` (l. 19-20) |

## 2. Presets (`CMakePresets.json`, version 6, `cmakeMinimumRequired` 3.24)

Cachés : `base` (Ninja, `binaryDir ${sourceDir}/../build/${presetName}`, `CMAKE_EXPORT_COMPILE_COMMANDS=ON`,
l. 9-17) ; `cross` (toolchain, `Debug`, `LEPTON_EMBOS_ROOT=$env{…}`,
`LEPTON_MKLEPTON=${sourceDir}/../build/host/mklepton`, l. 28-39).

| Preset | ISA | CPU | Carte | KAL | Particularité |
| --- | --- | --- | --- | --- | --- |
| `host` | host | – | – | static | l. 18-27 |
| `qemu-mps2-an386-{embos,freertos}` | armv7m | cortex-m4f | qemu-mps2-an386 | embos / freertos | ABI hard |
| `qemu-mps2-an386-{embos,freertos}-soft` | armv7m | cortex-m4f | qemu-mps2-an386 | embos / freertos | ABI soft |
| `nucleo-f439zi-{embos,freertos}` | armv7m | cortex-m4f | nucleo-f439zi | embos / freertos | hard |
| `nucleo-wl55jc1-{embos,freertos}` | armv7m | cortex-m4f | nucleo-wl55jc1 | embos / freertos | soft |
| `qemu-mps2-an500-{embos,freertos}` | armv7m | cortex-m7 | qemu-mps2-an500 | | `M7_FPU=dp` |
| `stm32f746g-disco-{embos,freertos}` | armv7m | cortex-m7 | stm32f746g-disco | | `M7_FPU=sp` |
| `samd21-xplained-pro-{embos,freertos}` | armv6m | cortex-m0plus | samd21-xplained-pro | | |

15 presets de configuration, 15 de build, 15 de test (`outputOnFailure`). Aucun preset ne fixe
`LEPTON_BOARD_SERIAL_PORT`, `LEPTON_NET_TEST_HOST_IP`, `LEPTON_BOARD_STLINK_SERIAL` (cache, vides).
Écarts commentaire / code : `CMakeLists.txt:9` (`$LEPTON_BUILD/<preset>`) et `cmake/mklepton.cmake:13`
(« superbuild », en fait une variable de cache).

**Version de CMake** : le code exige 3.24 (`cmake_minimum_required`, presets v6, `$<LINK_GROUP:RESCAN>`
introduit en 3.24), alors que `DEVENV-STATUS.md` consigne un minimum de 3.19 (borne de `string(JSON)`,
GRF-2). Minimum effectif : **3.24**.

## 3. Cibles

Listes de sources **explicites** partout, sauf `file(GLOB …*.c)` pour un binaire répertoire
(`firmware.cmake:36`) et `GLOB_RECURSE` des dépendances de mklepton (`mklepton.cmake:46`).

| Cible | Type | Définition | Sources | Répertoires (`src/…`) |
| --- | --- | --- | --- | --- |
| `lepton_options` | INTERFACE | `lepton_target.cmake:7` | – | options, includes |
| `lepton_core` | STATIC | `kernel.cmake:39` | 26 (13 en static) | `kernel/core`, `core-generic` |
| `lepton_kal_<backend>` | STATIC | `kernel.cmake:42` | static 3, embos 14, freertos 21 | `core-static`, `core-segger`, `core-freertos`, `ucore/freeRTOS_11-3-0` |
| `lepton_dev` | STATIC | `kernel.cmake:45-53` | 8 | `kernel/dev/dev_*` |
| `lepton_vfs`, `lepton_fs_rootfs`, `lepton_fs_ufs`, `lepton_fs_kofs` | STATIC | `kernel.cmake:56-77` | 4, 2, 7, 1 | `kernel/fs/*` |
| `lepton_net_lwip` | STATIC (si lwIP) | `kernel.cmake:104-133` | ~42 | `kernel/net/lwip`, `kernel/core/net` |
| `lepton_libc` | STATIC | `kernel.cmake:140-142` | 26 (+3 lwIP) | `lib/libc`, `lib/pthread`, `lib/librt` (`lib/lib-nxpnfc` non compilé) |
| `lepton_bsp_<nom>` | STATIC | `kernel.cmake:148-150` | an386 3, f439 14, wl55 26 | `kernel/dev/bsp/<carte>`, `kernel/dev/arch/…`, HAL/SPL |
| `lepton_kernel` | INTERFACE | `kernel.cmake:161-165` | – | `$<LINK_GROUP:RESCAN,…>` |
| `board_mkconf` | custom | `mklepton.cmake:65` | – | sorties mklepton |
| `lepton_generated` | STATIC | `firmware.cmake:17-22` | 3 générés | `dev_mkconf.c`, `bin_mkconf.c`, `dev_dskimg.c` |
| `lepton_sbin` | STATIC | `firmware.cmake:49-53` | 13 (9 wl55, samd21) | `sbin`, `sbin/net` |
| `lepton_bin` | STATIC (si non vide) | `firmware.cmake:54-58` | 2 (wl55 1, samd21 0) | `bin`, `bin/net` |
| `lepton` | EXECUTABLE `.elf` | `firmware.cmake:79-86` | 4-5 (démarrage, sbrk, main, matériel KAL, + vecteurs f439 ou `hal_tick` wl55) | POST_BUILD `objcopy` → `.bin`, `size` |
| `flash` | custom | `firmware.cmake:89-97` | – | openocd |
| `mklepton` | EXECUTABLE hôte | `components/mklepton.cmake:7-10` | `tools/mklepton/src/mklepton.c` | lié à `lepton_kernel` et `expat` |
| `kal_bench` | EXECUTABLE `.elf` | `tests/kal/CMakeLists.txt:33-38` | banc + démarrage + matériel KAL | `tests/kal` |
| `test_vfs_ufs`, `test_ufs_check`, `test_stub_check`, … | hôte | `tests/host/CMakeLists.txt` | 1 chacun | `tests/host` |

Édition de liens (`firmware.cmake:66-77`) : `$<LINK_GROUP:RESCAN, lepton_generated[, lepton_sbin, lepton_bin], <groupe noyau>>`
puis `${LEPTON_KAL_LINK_LIBS}` (archive embOS) et `${LEPTON_SYSTEM_LIBS}`. Toutes les bibliothèques
du noyau dépendent de `board_mkconf` (l. 13-15).

## 4. Sélection

- `LEPTON_ISA` = `host` | `armv7m` | `armv6m` → `cmake/isa/<isa>.cmake` ; dérive `LEPTON_KAL_ARCH_DIR`
  (`kernel/core/kal/arch/<isa>`), `LEPTON_ISA_ARCH_DIR` (`kernel/core/arch/cortexm`).
- `LEPTON_CPU` = `cortex-m0plus` | `cortex-m3` | `cortex-m4f` | `cortex-m7` ; sous-options
  `LEPTON_FLOAT_ABI`, `LEPTON_M7_FPU`.
- `LEPTON_BOARD` : 6 valeurs ; chaque module vérifie le CPU attendu (`nucleo-f439zi.cmake:7-9`).
- `LEPTON_KAL_BACKEND` = `static` | `embos` | `freertos` → `LEPTON_KAL_BACKEND_DIR`. « soft » n'est
  pas un backend mais l'ABI flottante.
- Labels de test `arch:${LEPTON_CPU};backend:${LEPTON_KAL_BACKEND}` (`firmware.cmake:110,142`).
- Surcharges par carte : `LEPTON_EMBOS_LIB_VARIANT`, `LEPTON_FREERTOS_PORT` (f746), `LEPTON_FREERTOS_CONFIG`
  (samd21), `LEPTON_NET_STACK`.

## 5. Appel de mklepton

`lepton_generate(board XML ${LEPTON_BOARD_MKCONF} MKCONF_TARGET ${LEPTON_BOARD_MKCONF_TARGET})`
(`firmware.cmake:10`) → `add_custom_command` (`cmake/mklepton.cmake:56-64`) :

```
cmake -E env SOURCE_DATE_EPOCH=${LEPTON_SOURCE_DATE_EPOCH} <mklepton> -s ${CMAKE_SOURCE_DIR} -o <build>/generated/board -t cortexm_lepton <xml>
```

- Outil : argument `MKLEPTON`, sinon cible `mklepton` du même build, sinon `${LEPTON_MKLEPTON}`
  (`../build/host/mklepton`) (l. 22-30). Pas d'ExternalProject : le preset `host` doit être construit
  avant (`ci/run.sh:73-76`).
- Dépendances : XML, chaque `src_file`/`src_path` relevé par regex (`GLOB_RECURSE` si répertoire,
  l. 39-51), l'outil ; `CMAKE_CONFIGURE_DEPENDS` sur le XML (l. 52).
- Sorties déclarées : `kernel_mkconf.h`, `dev_mkconf.c`, `bin_mkconf.c`, `dev_dskimg.c`, `dev_dskimg.h`
  (l. 54-55) ; `.fsflash.o` écrit mais non déclaré.
- `<build>/generated/board` et `${CMAKE_SOURCE_DIR}` ajoutés aux includes de `lepton_options` (l. 12).
- Sans `LEPTON_BOARD_MKCONF`, pas de firmware (`firmware.cmake:4-7`).
- CMake relit lui-même le XML par regex pour dériver les sources `sbin`/`bin`
  (`firmware.cmake:26-47` ; idem `tests/host/mklepton_check.cmake:77-86`), en ignorant `<target>` et
  les commentaires.

## 6. Démarrage, vecteurs, scripts `.ld`

| Élément | Fichier | Liaison |
| --- | --- | --- |
| Démarrage ARMv7-M, `.isr_vector` (16 + 64) | `src/kernel/core/arch/cortexm/startup_armv7m.c` (`Reset_Handler` l. 90) | source de l'exécutable via `LEPTON_FIRMWARE_SOURCES` (`armv7m.cmake:26-28`) |
| Démarrage ARMv6-M | `src/kernel/core/arch/cortexm/startup_armv6m.c` | idem |
| `_sbrk` | `src/kernel/core/arch/cortexm/sbrk_cortexm.c` | idem |
| Vecteurs étendus F4 (IRQ 64-90, `.isr_vector_ext`) | `src/kernel/dev/bsp/nucleo_f439zi/nucleo_f439zi_vectors.c:33` | source de l'exécutable (`nucleo-f439zi.cmake:29-31` : symboles faibles non tirés d'une archive) |
| Base de temps HAL WL | `src/kernel/dev/arch/cortexm/stm32wlxx/dev_stm32wlxx/dev_stm32wlxx_hal_tick.c` | source de l'exécutable (`nucleo-wl55jc1.cmake:46-48`) |
| `main` | `core-segger/arch/armv7m/embos_main.c` ou `core-freertos/arch/armv7m/freertos_main.c` | source de l'exécutable (`embos.cmake:28-30`, `freertos.cmake:22-24`) |
| Script commun | `ld/common-cortexm.ld` (`ENTRY(Reset_Handler)`, `.isr_vector`, `.isr_vector_ext`, `.ccm_bss`) | `-T` (`firmware.cmake:72-76`), `LINK_DEPENDS` |
| Mémoire par carte | `ld/mem_<carte>.ld` (MEMORY + `REGION_ALIAS`) | `-T${LEPTON_BOARD_MEMORY_LD}` avant le script commun |

## 7. Écart avec BLD-1

| BLD-1 | Existant |
| --- | --- |
| `kernel` (`kernel/`, `kernel/dev/arch`) | 7 à 9 archives (`lepton_core`, `lepton_kal_<b>`, `lepton_dev`, `lepton_vfs`, `lepton_fs_*`, `lepton_net_lwip`, `lepton_libc`) regroupées par l'INTERFACE `lepton_kernel` (RESCAN). `kernel/dev/arch` est dans `lepton_bsp_<nom>`, pas dans le noyau. |
| `lib` | `lepton_libc` existe mais dans le groupe noyau. |
| `sbin`, `bin` | Existent ; sources dérivées du XML par regex, non de l'arborescence. `lepton_bin` absente pour samd21. |
| `bsp` | `lepton_bsp_<nom>` existe ; mélange `kernel/dev/bsp`, `kernel/dev/arch` et HAL/SPL tiers. |
| Exécutif : `main` du greffon noyau | `main` fourni par le backend KAL (source de l'exécutable). |
| Exécutif : table des périphériques et sources mklepton | Bibliothèque STATIC `lepton_generated`, non sources de l'exécutable. |
| Démarrage et vecteurs du BSP en OBJECT | Fournis par l'ISA (`kernel/core/arch/cortexm`) ; aucune bibliothèque OBJECT ; tout via `LEPTON_FIRMWARE_SOURCES`. |

## 8. Tests

- `tests/host` (preset `host`, label `host`) : `host.vfs_ufs`, `host.ufs_format_host`,
  `host.ufs_format_arm`, `host.kernel_stub`, `host.mklepton` (`mklepton_check.cmake` sur le XML Olimex),
  `host.mklepton_empreintes` (empreintes de mklepton sur chaque XML de carte,
  `mklepton_empreintes.sha256`).
- `tests/kal` : voir `env-2-outillage.md` §5.
- `firmware.cmake` : `smoke.lsh` (l. 131-143), `net.ping_ftpd` (Linux, l. 149-164), `board.smoke_lsh`,
  `board.net` (l. 98-126) ; `board.radio` (`nucleo-wl55jc1.cmake:84-92`).
- Filtre : `ctest --preset <p> -L host|smoke|kal|net|board|radio`.
