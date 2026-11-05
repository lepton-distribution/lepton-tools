# ENV-34 — HAL et CMSIS device STM32F4 : rapport

Session du 2026-11-05, hôte Mac. Branches `devenv/env-34` : lepton-tools (depuis `main` a97675c),
`family-stm32f4xx` (depuis `master` 8364493), clone noyau (depuis `master` b3a5415).

## 1. Audit (lecture seule)

### 1.1 Références amont (`git ls-remote`, `gh api`, 2026-11-05)

| Élément | Dépôt | Révision retenue | Tête actuelle | Sous-module de STM32CubeF4 `v1.28.3` (94cae6e) |
| --- | --- | --- | --- | --- |
| HAL | `STMicroelectronics/stm32f4xx-hal-driver` | `b6f0ed3829f3829eb358a2e7417d80bba1a42db7` = `v1.8.5^{}` (tag annoté 6b55d2c) | `HEAD` 6ef30cf (au-delà de v1.8.5) | `Drivers/STM32F4xx_HAL_Driver` = b6f0ed3 ✔ |
| CMSIS device | `STMicroelectronics/cmsis_device_f4` | `3c77349ce04c8af401454cc51f85ea9a50e34fc1` (sans tag ; `v2.6.11^{}` = 0fa0e48) | `master` 9192c7b | `Drivers/CMSIS/Device/ST/STM32F4xx` = 3c77349 ✔ |
| CMSIS Core | `ARM-software/CMSIS_5` | `5.9.0^{}` = 2b7495b (tag annoté 61e3644) ; `CMSIS/Core/Include/core_cm4.h` blob e21cd14, 120 975 octets | — | — |

Les révisions du 2026-11-04 sont confirmées.

### 1.2 Contenu actuel de `cubemx_hal_driver/` (famille)

190 fichiers suivis : `inc` 99, `inc/Legacy` 2, `src` 89 ; en-tête `stm32f4xx_hal.h` V1.7.1.
HAL `v1.8.5` : 209 fichiers, dont `Inc` 99, `Inc/Legacy` 3, `Src` 94, `Src/Legacy` 2, plus
`LICENSE.md`, `README.md`, `Release_Notes.html`, `_htmresc/` (3), `.github/` (2),
`CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`.

- 6 fichiers absents du dépôt HAL (confirmés) : `inc/stm32f4xx.h`, `inc/stm32f407xx.h`,
  `inc/stm32f429xx.h`, `inc/stm32f469xx.h`, `inc/system_stm32f4xx.h`,
  `inc/Legacy/stm32f4xx_hal_conf.h`.
- 14 fichiers nouveaux en v1.8.5 : `Inc/Legacy/stm32f4xx_hal_{can,eth}_legacy.h`,
  `Src/Legacy/stm32f4xx_hal_{can,eth}.c`, `stm32f4xx_hal_exti.{h,c}`,
  `stm32f4xx_hal_fmpsmbus{,_ex}.{h,c}`, `stm32f4xx_hal_smbus.{h,c}`, `stm32f4xx_ll_fmpi2c.{h,c}`.
- Bilan : 184 fichiers communs, 198 fichiers `Inc`/`Src` à importer.

CMSIS device `3c77349` : 152 fichiers ; `Include/stm32f4xx.h`, `Include/system_stm32f4xx.h`,
`Include/stm32f429xx.h`, `Include/stm32f439xx.h` présents ; `LICENSE.md`, `README.md` à la racine.

### 1.3 Références à `cubemx_hal_driver` et à `stm32f4xx_hal.h`

| Où | Fichier | Nature | Compilé |
| --- | --- | --- | --- |
| famille | `lepton-greffon.json`, `description` | texte « cubemx_hal_driver et les pilotes non listés ne sont pas compilés » | — (texte) |
| famille | `dev_stm32f4xx/dev_stm32f4xx_{cpu_x,cubemx_eth,dac_x,flash,i2c_x,sdio,sdio-1.16}.c` (7) | `#include "stm32f4xx_hal.h"` | non |
| BSP `nucleo-f429zi`, `nucleo-f439zi` | — | aucune référence | — |
| noyau | `kernel/usb/stm32f4-usb-core/core/{usb_device.h,usbd_conf.h,usbd_conf.c}` (3) | `#include "stm32f4xx_hal.h"` | non (hors plan) |
| noyau | `kernel/dev/bsp/discovery_f4-baseboard-modem/…/{dev_discovery_f4_i2c_1,dev_discovery_f4_sdio}.c` (2), `kernel/dev/bsp/stm32f469i-eval/…/dev_stm32f469i_eval_i2c_1.c` (1) | `#include "stm32f4xx_hal.h"` | non (hors plan) |
| noyau | `kernel/fs/fatfs/core/ffconf_template.h` | commentaire | — |
| noyau | `sys/user/tauon-basic/src/arch/{st-stm32f407-discovery,olimex-stm32-p407,st-stm32f469i-eval}/kernel_mkconf/include/user_kernel_mkconf.h` (3) | commentaire « see in …\cubemx_hal_driver\inc\legacy\stm32f4xx_hal_conf.h » | non (hors plan) |
| noyau | `tools/migration/*.py` (5), `doc/migration/*` (12) | historique de la migration | — |
| lepton-tools | `schemas/exemples/greffon-famille-stm32wlxx.json` | `cubemx_hal_driver` du **WL**, sans rapport | — |
| lepton-tools | skills, documents vivants | aucune référence F4 | — |

Aucun `CMakeLists.txt`, module CMake, manifeste (`sources`, `compilation`) ni XML ne cite
`cubemx_hal_driver` du F4. Les références hors plan restent pendantes après suppression : c'est
déjà le cas aujourd'hui (fichiers non compilés).

### 1.4 Fins de ligne

| Ensemble | Fins de ligne |
| --- | --- |
| HAL et CMSIS device amont | LF (relevé du 2026-11-04 ; pas de `.gitattributes`) |
| `cubemx_hal_driver/` F4 actuel | LF (0/190 CRLF) |
| F7 `hal_driver/` | LF (0/197) |
| F7 `cmsis-5/Device/ST/STM32F7xx` | LF (0/6) |
| noyau `cmsis-5/CMSIS/Core/Include` (7 fichiers) | CRLF (7/7, `i/crlf` dans l'index) ; pas de `.gitattributes`, `core.autocrlf` non défini |

### 1.5 Les deux `core_cm4.h` (ajout de la passation de préparation)

- Un seul `core_cm4.h` dans l'arbre : `kernel/core/ucore/cmsis/CMSIS/Include/core_cm4.h` (V3.30).
- `scion/cmake/isa/armv7m.cmake:18` ajoute `cmsis/CMSIS/Include` pour tous les presets armv7m ;
  `scion/cmake/cpu/cortex-m7.cmake:35` ajoute `cmsis-5/CMSIS/Core/Include` pour le M7 seul
  (commentaire : copie non modifiée du paquet embOS, CoreSupport STM32F769I-Discovery, V5.6,
  décision 2026-10-05).
- Ordre des `-I` (`compile_commands.json` de `<ROOTSTOCK>/build/<preset>`) :

| Preset | 1 | 2 | … | CMSIS 5 |
| --- | --- | --- | --- | --- |
| `nucleo-f429zi-embos` | `sys/root/src` | `cmsis/CMSIS/Include` (V3.30) | `driverlib`, `dev_stm32f4xx` | absent |
| `nucleo-wl55jc1-embos` | `sys/root/src` | `cmsis/CMSIS/Include` (V3.30) | `cubemx_hal_driver/inc` (WL), `cmsis/Device/st/stm32wlxx` | absent |
| `stm32f746g-disco-embos` | `sys/root/src` | `cmsis/CMSIS/Include` (V3.30) | — | `cmsis-5/CMSIS/Core/Include` en 5 |

- `gcc -H -fsyntax-only` : `stm32f4xx/gpio.c` (F429) et `dev_stm32wlxx_uart_x.c` (WL55) retiennent
  `cmsis/CMSIS/Include/core_cm4.h` V3.30. Le F7 n'est pas concerné (`core_cm7.h` n'existe que
  dans CMSIS 5).
- Conséquence : le `core_cm4.h` 5.9.0 importé en ENV-34 ne sera vu par aucun preset. En ENV-35,
  la HAL F4 prendra V3.30 tant que `armv7m.cmake` n'est pas modifié ou que les inclusions de la
  famille ne passent pas avant (`cmake/lepton_greffons.cmake:272` les ajoute après).

## 2. PA-55 (2026-11-05, décisions de l'utilisateur)

| Question | Décision |
| --- | --- |
| Destination de la HAL | option 1 : `stm32f4xx/hal_driver/{Inc,Src}` (convention F7, casse de l'amont) |
| Contenu HAL | `Inc/`, `Src/` complets (`Legacy/`, modèles compris), `LICENSE.md`, `README.md` ; notes de version non reprises |
| CMSIS device | `stm32f4xx.h`, `system_stm32f4xx.h`, `stm32f429xx.h`, `stm32f439xx.h` sous `kernel/core/ucore/cmsis-5/Device/ST/STM32F4xx/Include` de la famille ; `LICENSE.md`, `README.md` à `STM32F4xx/` ; `Source/Templates` non repris |
| 6 fichiers hors amont | supprimés avec la copie |
| Clones amont | `~/lepton-tools-dev/tiers/` |
| `core_cm4.h` | CMSIS_5 `5.9.0`, fins de ligne de l'amont (LF) ; `cmsis-5/CMSIS/Core/LEPTON-PROVENANCE.md` ajouté (origine embOS V5.6 des 7 fichiers existants, équivalence 5.9.0 aux CR près, `core_cm4.h` tiré de 5.9.0) |
| `scripts/tiers/verifier-import.sh` | accordé |
| Compilation à blanc | accordée, dans les deux ordres d'inclusion (V3.30 en tête comme aujourd'hui ; CMSIS 5 seul) |
| Double `core_cm4.h` | rien en ENV-34 ; choix renvoyé au PA-57 avec le résultat des deux compilations |
| Propositions 3, 6, 7 de la passation de préparation | reportées dans `etapes/ENV-35-*.md` (§1 dépendants hors plan de la SPL, constat `.ccm_bss`) et `etapes/ENV-36-*.md` (C2, nombre de liens) |
