# ENV-2 — Code de carte

Relevé du 2026-10-13, lecture seule, clone noyau `master` 6b62af5.
Conventions : chemins relatifs à `scion/` du clone ; `src/…` = `scion/sys/root/src/…` ;
`$B` = `<ROOTSTOCK>/build` (`CMakePresets.json:13` : `${sourceDir}/../build/<preset>`).
Volumes « utilisés » : fichiers réellement compilés ou inclus, relevés dans `$B/<preset>/.ninja_deps`
(constructions du 8 au 12 octobre) et recoupés avec `compile_commands.json` ; ce n'est pas une
analyse des sources.

## 0. F429ZI ou F439ZI

- Aucun fichier ni preset `nucleo-f429zi`. Tout est nommé `nucleo-f439zi` : `cmake/boards/nucleo-f439zi.cmake`,
  `ld/mem_nucleo-f439zi.ld`, `debug/openocd-nucleo-f439zi.cfg`, `debug/gdbinit-nucleo-f439zi`,
  `src/kernel/dev/bsp/nucleo_f439zi/`, `sys/user/tauon-basic/etc/mkconf_tauon_basic_nucleo_f439zi.xml`,
  presets `nucleo-f439zi-{embos,freertos}`.
- La carte validée est une NUCLEO-F429ZI : `cmake/boards/nucleo-f439zi.cmake:2-3` (« Validée sur
  NUCLEO-F429ZI (décision 2026-10-01) … la puce est déclarée STM32F429xx ») ; `:51`
  `STM32F429xx USE_STDPERIPH_DRIVER` ; puce relue STM32F429ZI rév. 3 (`DBGMCU_IDCODE 0x20016419`),
  ST-LINK/V2-1 `V2J27M15` (`doc/migration/validation-nucleo-f439zi.md:3-5`).
- **Question pour ENV-6** : nom du greffon BSP et des presets (`nucleo-f429zi` conforme à la carte
  réelle et à la décision du chantier, ou conservation de `nucleo-f439zi`, conforme à la décision du
  portage `doc/migration/MIGRATION-STATUS.md:110` : F439ZI carte de base nominale, noms conservés).

## 1. Socle commun Cortex-M (hors greffons de carte)

| Fichier | Lignes |
| --- | --- |
| `src/kernel/core/arch/cortexm/startup_armv7m.c` (table `.isr_vector` générique, IRQ0-63 faibles, l. 27-68) | 117 |
| `src/kernel/core/arch/cortexm/startup_armv6m.c` | 93 |
| `src/kernel/core/arch/cortexm/sbrk_cortexm.c`, `lepton_irq.h` | 27 + 40 |
| `ld/common-cortexm.ld` | 128 |
| `src/kernel/core/core-segger/arch/armv7m/embos_init_hw.c` (SysTick sur `SystemCoreClock`), `embos_main.c` | 85 + 19 |
| `kernel/core/core-freertos/arch/armv7m/freertos_hooks.c` (`cmake/kal/freertos.cmake:23`) | — |
| `cmake/isa/*`, `cmake/cpu/*`, `cmake/kal/*`, `cmake/toolchains/arm-none-eabi.cmake`, `cmake/components/firmware.cmake` | — |

Contrat implicite carte ↔ noyau : `SystemInit` et `SystemCoreClock` fournis par la carte ;
`IRQ<n>_Handler` forts dans le code de carte ; bibliothèque `lepton_bsp_<nom>` créée par
`cmake/components/kernel.cmake:148-150`. Démarrage et vecteurs sont aujourd'hui **dans le noyau**
(`src/kernel/core/arch/cortexm/`), pas dans un BSP (écart avec la décision 4 de la spécification).

## 2. QEMU `mps2-an386` (Cortex-M4F)

| Fichier | Rôle | Statut | Lignes |
| --- | --- | --- | --- |
| `cmake/boards/qemu-mps2-an386.cmake` | module de carte | propre | 28 |
| `ld/mem_qemu-mps2-an386.ld` | CODE 4M @0x0, RAM 4M @0x20000000 | propre | 12 |
| `src/kernel/dev/bsp/qemu_mps2/an386/qemu_mps2_machine.h` | adresses, IRQ | propre | 33 |
| `src/kernel/dev/bsp/qemu_mps2/qemu_mps2_board.c` | `SystemInit`, IRQ0-5, 12, 13 | partagé avec an500 | 139 |
| `src/kernel/dev/arch/all/uart/dev_cmsdk_uart/` | UART CMSDK | générique MPS2 | 205 |
| `src/kernel/dev/arch/all/eth/dev_eth_lan9118/` | LAN9118 | générique | 393 |
| `sys/user/tauon-basic/etc/mkconf_tauon_basic_qemu_mps2.xml` | mklepton | partagé avec an500 | 99 |
| `sys/user/tauon-basic/etc/qemu-mps2/.boot`, `.init` | rootfs | partagé avec an500 | 3 + 2 |
| `sys/user/tauon-basic/src/arch/qemu-mps2/kernel_mkconf/include/user_kernel_mkconf.h` | config noyau | partagé avec an500 | 26 |
| CMSIS `Device/ARM/ARMCM4/Include/{ARMCM4.h,system_ARMCM4.h}` | en-têtes | tiers | 176 |

Presets : `qemu-mps2-an386-embos`, `-embos-soft`, `-freertos`, `-freertos-soft`
(`CMakePresets.json:41-82`). Ni OpenOCD ni gdbinit.
Volume utilisé : 9 fichiers, 972 lignes ; propres à an386 : 3 fichiers, ~73 lignes.

## 3. NUCLEO-F429ZI (presets `nucleo-f439zi-*`, Cortex-M4F)

| Fichier | Rôle | Statut | Lignes |
| --- | --- | --- | --- |
| `cmake/boards/nucleo-f439zi.cmake` | module de carte | propre | 56 |
| `ld/mem_nucleo-f439zi.ld` | FLASH 2048K, RAM 192K, CCM 64K | propre | 14 |
| `src/kernel/dev/bsp/nucleo_f439zi/nucleo_f439zi_board.c` | `SystemInit` (HSE 8 MHz bypass, PLL 168 MHz), GPIO, descripteur Ethernet | propre | 254 |
| `src/kernel/dev/bsp/nucleo_f439zi/nucleo_f439zi_vectors.c` | IRQ12, 39, 57, 61 ; lié comme objet de l'exécutable (`cmake/boards/nucleo-f439zi.cmake:31`) | propre | 38 |
| `src/kernel/dev/bsp/nucleo_f439zi/nucleo_f439zi.h` | en-tête | propre | 73 |
| `src/kernel/dev/arch/cortexm/stm32f4xx/{gpio,uart,eth}.[ch]`, `dev_stm32f4xx/*`, `dma.h`, `types.h`, `stm32f4x7_eth_conf.h` | couche STM32F4 de Lepton | générique famille F4 | ~2 900 |
| `src/kernel/dev/arch/cortexm/stm32f4xx/driverlib/` (SPL ST, 7 .c compilés) | pilotes ST | tiers F4 | ~30 450 utilisées (répertoire : 72 fichiers, 92 928 l.) |
| `sys/user/tauon-basic/etc/mkconf_tauon_basic_nucleo_f439zi.xml` (`cpu freq=168000000`, l. 20) | mklepton | propre | 101 |
| `sys/user/tauon-basic/etc/nucleo-f439zi/.boot`, `.init` (`ifconfig 192.168.2.5 192.168.2.20`) | rootfs | propre | 3 + 2 |
| `sys/user/tauon-basic/src/arch/nucleo-f439zi/kernel_mkconf/include/user_kernel_mkconf.h` | config noyau | propre | 30 |
| `debug/openocd-nucleo-f439zi.cfg` (`source [find board/st_nucleo_f4.cfg]`) | sonde | propre | 8 |
| `debug/gdbinit-nucleo-f439zi` (`lepton-load`, `lepton-fault`, `lepton-stacks`) | débogage | **commun de fait** : sourcé par les gdbinit WL55, F746, SAMD21 | 145 |

Volume utilisé : 54 fichiers, 33 751 lignes (carte 4 / 395 ; couche F4 12 / 2 899 ; SPL 38 / 30 457),
plus ~9 fichiers / 360 lignes (cmake, ld, mkconf, etc, debug). Répertoire `stm32f4xx/` complet :
293 fichiers, 369 488 lignes (dont `cubemx_hal_driver` inutilisé). Startups IAR seulement pour
F429/F439 (`ucore/cmsis/Device/st/stm32f4xx/startup/iar/`), non utilisées.

## 4. NUCLEO-WL55JC1 (cœur M4 / CPU1, ABI soft)

| Fichier | Rôle | Statut | Lignes |
| --- | --- | --- | --- |
| `cmake/boards/nucleo-wl55jc1.cmake` | module ; écrit une cfg OpenOCD dans le build (l. 56-65) ; test `board.radio` (l. 72-93) ; refuse toute ABI autre que soft (l. 8) | propre | 111 |
| `ld/mem_nucleo-wl55jc1.ld` | FLASH 256K, RAM 64K, MSP 4 Ko | propre | 16 |
| `src/kernel/dev/bsp/stm32wl55jci_nucleo/stm32wl55jci_nucleo_system.c` | `SystemInit` (MSI 48 MHz), IRQ11, 12, 37, 50 | propre | 90 |
| `…/dev_stm32wl55jci_nucleo_peripherals/dev_stm32wl55jci_nucleo_usart_2.c` | console USART2 | propre | 205 |
| `…/dev_stm32wl55jci_nucleo_radio/*` | radio | propre | ~720 |
| `…/dev_stm32wl55jci_nucleo_board/*` | — | présent, **non compilé** | 380 |
| `src/kernel/dev/arch/cortexm/stm32wlxx/dev_stm32wlxx/*` | couche WL de Lepton | générique famille WL | ~1 650 |
| `…/stm32wlxx/{cubemx_hal_driver,radio_subghz_phy,Utilities}`, CMSIS `ucore/cmsis/Device/st/stm32wlxx` | HAL, SubGHz_Phy, CMSIS | tiers WL | ~72 500 utilisées |
| `sys/user/tauon-basic/etc/mkconf_tauon_basic_nucleo_wl55jc1.xml` | mklepton | propre | 85 |
| `sys/user/tauon-basic/etc/nucleo-wl55jc1/.boot`, `.init` | rootfs | propre | 3 + 1 |
| `sys/user/tauon-basic/src/arch/nucleo-wl55jc1/…/user_kernel_mkconf.h` | config noyau | propre | 33 |
| `debug/openocd-nucleo-wl55jc1.cfg` (`transport select hla_swd`, `target/stm32wlx.cfg`, `reset_config srst_only srst_nogate`) | sonde | propre | 7 |
| `debug/gdbinit-nucleo-wl55jc1` (source le gdbinit F439) | débogage | propre | 7 |

Presets `nucleo-wl55jc1-embos`, `-freertos` (`CMakePresets.json:165-186`).
Volume utilisé : 84 fichiers, 75 179 lignes (carte 9 / 999 ; couche WL 8 / 1 646 ; tiers 67 / 72 534),
plus ~8 fichiers / 260 lignes. Répertoire `stm32wlxx/` complet : 234 fichiers, 212 247 lignes.
Doublons IAR non utilisés : `etc/mkconf_tauon_basic_stm32wl55jci_nucleo.xml` (cible `win32_lepton`),
`src/arch/st-stm32wl55jci-nucleo/`.

## 5. OpenOCD, sondes, consoles (portage)

OpenOCD 0.12.0 sur Debian et macOS (`doc/migration/MIGRATION-STATUS.md:217,225` ;
`doc/migration/validation-macos.md:13` : MacPorts `+ftdi +cmsis`). Console 115200 8N1
(`tests/smoke_lsh.py:126`).

| Carte | OpenOCD | Sonde | Console macOS (étape 10) | Console Debian |
| --- | --- | --- | --- | --- |
| NUCLEO-F429ZI | `-f debug/openocd-nucleo-f439zi.cfg` → `board/st_nucleo_f4.cfg` | ST-LINK/V2-1 `V2J27M15`, `0483:374b`, n° `0672FF495252717267243842` | `/dev/cu.usbmodem1454303` (`doc/migration/validation-macos.md:26,34`) | `/dev/ttyACM0` |
| NUCLEO-WL55JC1 (A / B) | `-f $B/<preset>/openocd-nucleo-wl55jc1.cfg` (généré : `interface/stlink.cfg` + `adapter serial <n°>` + `debug/openocd-nucleo-wl55jc1.cfg` → `target/stm32wlx.cfg`) | STLINK-V3 `0483:374e` ; A `002700253431510837393937`, B `004F003E3431510937393937` (`doc/migration/validation-nucleo-wl55jc1.md:7-10`) | A `/dev/cu.usbmodem1454303`, B `/dev/cu.usbmodem1454403` (`doc/migration/validation-macos.md:29-30`) | `/dev/ttyACM0`, `ttyACM1` |

Commandes du portage :
- Flash : cible CMake `flash` = `openocd -f <cfg> -c "program <lepton.elf> verify reset exit"`
  (`cmake/components/firmware.cmake:90-95`).
- Banc KAL sur carte : `-c init -c "reset halt" -c "arm semihosting enable" -c "arm semihosting_cmdline kal_bench <T>" -c resume`
  (`tests/kal_openocd.py:30-36`).
- Débogage : `openocd -f <cfg>` (port 3333) puis `gdb-multiarch -x debug/gdbinit-<carte> $LEPTON_BUILD/<preset>/lepton.elf`
  (`doc/migration/debug-gcc.md:18-19`) ; sur macOS `gdb-multiarch` = lien vers `arm-none-eabi-gdb` 17.2
  MacPorts `+python313` (`doc/migration/validation-macos.md:14`).
- Validation F429 depuis macOS : `cmake --preset nucleo-f439zi-embos -DLEPTON_BOARD_SERIAL_PORT=/dev/cu.usbmodem1454303 -DLEPTON_NET_TEST_HOST_IP=192.168.2.10`,
  `--target flash`, `ctest --preset … -L board` (`doc/BUILDING.md:178-181`). WL55 : `-DLEPTON_BOARD_STLINK_SERIAL`,
  `-DLEPTON_RADIO_PEER_STLINK_SERIAL`, `-DLEPTON_RADIO_PEER_SERIAL_PORT` (`doc/BUILDING.md:266-271`).
- Journal hors clone `$B/etape10-f429-embos-flash.log` : « Open On-Chip Debugger 0.12.0 », « ** Verified OK ** ».

## 6. Autres cartes

| Carte | État |
| --- | --- |
| `qemu-mps2-an500` (M7) | Partage BSP `qemu_mps2` et mkconf avec an386 ; fumée, réseau, KAL verts en CI (`doc/BUILDING.md:14`) |
| `stm32f746g-disco` (M7) | Validée sur carte et depuis macOS (`doc/migration/validation-macos.md:72-88`) |
| `samd21-xplained-pro` (M0+) | embOS validé ; FreeRTOS : fumée en échec (RAM), écart accepté (`doc/migration/validation-macos.md:101-117`) |
| BSP hérités sans module `cmake/boards` | `src/kernel/dev/bsp/{discovery_f4, discovery_f4-baseboard-modem, olimex_p407, samd20xplained_pro, same70xplained, samv71xplained_ultra, stm32f469i-eval}` |

## 7. Estimation pour ENV-6 (greffons BSP des trois cartes retenues)

| Greffon | Propre à la carte | Partagé à décider | Remarque |
| --- | --- | --- | --- |
| qemu-mps2-an386 | ~4 fichiers (cmake, ld, machine.h, …) | `qemu_mps2_board.c`, mkconf, etc, `user_kernel_mkconf.h` partagés avec an500 | an500 hors périmètre : greffon « qemu-mps2 » commun ou duplication |
| nucleo-f429zi | ~12 fichiers, ~750 l. | couche F4 (~2 900 l.) et SPL (~30 000 l.) : greffon famille ou noyau | gdbinit commun à extraire hors carte |
| nucleo-wl55jc1 | ~16 fichiers, ~1 250 l. | couche WL (~1 650 l.) et tiers (~72 500 l.) | test `board.radio` et cfg OpenOCD générée dans le module de carte |

Démarrage et vecteurs (`startup_armv7m.c`, `common-cortexm.ld`) : génériques Cortex-M, à placer
selon BLD-1 / décision 4 (BSP) — point à trancher en PA-2.
