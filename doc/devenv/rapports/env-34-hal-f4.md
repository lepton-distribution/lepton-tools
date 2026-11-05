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

## 3. Oracle avant (tâche 2)

`rapports/oracles/env-34-avant/` : `rejouer-oracle.sh <ROOTSTOCK> … --qemu` ×6 `--carte` ×10
(constructions à neuf, journal `rejouer-oracle.log`) : « tout a réussi ». Contre `env-32-apres` :
`comparer-oracle.py` code 0 ×16, host 7/7, empreintes mklepton identiques, bancs KAL QEMU
identiques (19, 15, 19, 15, 18, 18 tests, 100 %). Listes `ctest -N` de host et des 16 presets :
`env-34-avant/ctest-N/` (17 fichiers ; nouvelle référence, `env-32` ne relevait que le WL55).

## 4. Import (tâche 3)

Clones amont (PA-55) : `~/lepton-tools-dev/tiers/{stm32f4xx-hal-driver,cmsis_device_f4,CMSIS_5}`
(CMSIS_5 en clone partiel `--filter=blob:none`) ; pour la vérification du F7 :
`~/lepton-tools-dev/tiers/{stm32f7xx-hal-driver,cmsis_device_f7}`. `git describe` : HAL
`v1.8.5`, CMSIS device `v2.6.11-1-g3c77349`, F7 `v1.3.3` et `v1.2.10`.

| Dépôt (`devenv/env-34`) | Commit | Contenu |
| --- | --- | --- |
| `family-stm32f4xx` | e260213 | `git rm -r cubemx_hal_driver/` (190 fichiers), répertoire supprimé du disque (`.DS_Store`) |
| `family-stm32f4xx` | 1d6a86e | HAL `b6f0ed3` : `git archive … Inc Src LICENSE.md README.md` → `hal_driver/` (200 fichiers ; liste de l'archive = `git ls-tree -r`) |
| `family-stm32f4xx` | ac6119c | CMSIS device `3c77349` : 6 fichiers → `kernel/core/ucore/cmsis-5/Device/ST/STM32F4xx/` (archive = `ls-tree`) |
| `family-stm32f4xx` | 6ce57c9 | `LEPTON-PROVENANCE.md` des deux répertoires |
| `family-stm32f4xx` | 13a82bc | `description` du manifeste (texte seul ; `sources`, `compilation` inchangés) |
| clone noyau | eee09e7 | `core_cm4.h` de CMSIS_5 `5.9.0` (V5.1.2, LF, `i/lf`) |
| clone noyau | 6d600ca | `cmsis-5/CMSIS/Core/LEPTON-PROVENANCE.md` |
| lepton-tools | ec0fa87 | `scripts/tiers/verifier-import.sh` |
| lepton-tools | (ce commit) | `scripts/tiers/compiler-hal-f4-a-blanc.sh` |

`git status --ignored` du clone famille : rien d'autre que des `.DS_Store` sous les répertoires
importés.

Regreffe : copie d'essai `~/lepton-tools-dev/essais/env-34-copie` (`cp -RP` de
`.scion.rootstock.signature`, `.scion.trunk.tolerated`, `depots`, `trunk` ; aucun lien du trunk
ne vise hors de `depots/`), `scion graft --scion lepton@family-stm32f4xx` (336 feuilles) puis
`--scion lepton@original::tree` (3041 feuilles), code 0 ; mêmes commandes sur `<ROOTSTOCK>`,
code 0. Liste des liens de `<ROOTSTOCK>` identique à celle de la copie.

| Contrôle du trunk | Avant | Après |
| --- | --- | --- |
| Liens | 3957 | **3977** (−190 `cubemx_hal_driver`, +201 `hal_driver`, +7 CMSIS device, +2 noyau) |
| Liens cassés | 0 | 0 |
| Fichiers réguliers hors `.DS_Store` | 0 | 0 (34 `.DS_Store`, tolérés par `.scion.trunk.tolerated`, inchangés) |
| Liens sous `stm32f4xx/cubemx_hal_driver/` | 190 | 0 |
| `lepton check` | — | code 0, 19 fichiers conformes |

## 5. Contrôles (tâche 4)

### 5.1 Oracle après

`rapports/oracles/env-34-apres/` : mêmes commandes, « tout a réussi ». Comparaisons
`env-34-apres/comparaisons/<preset>.txt`.

| Preset | Sections/symboles | Empreinte | Fumée | Banc KAL | Écarts expliqués |
| --- | --- | --- | --- | --- | --- |
| host | — | mklepton identique | — | 7/7 | — |
| `qemu-mps2-an386-{embos,embos-soft,freertos,freertos-soft}` | code 0 | ≠ | identique (E-1) | 19, 15, 19, 15 / 100 % | E-1, E-2 |
| `qemu-mps2-an500-{embos,freertos}` | code 0 | ≠ | identique (E-1) | 18, 18 / 100 % | E-1, E-2 |
| `nucleo-f429zi-*`, `nucleo-f439zi-*`, `nucleo-wl55jc1-*`, `samd21-xplained-pro-*`, `stm32f746g-disco-*` (10) | code 0 | ≠ | — | — | E-2 |

Listes `ctest -N` : identiques pour host et les 16 presets (17/17).

- E-1 : la console de fumée diffère par la date de compilation, le jeton aléatoire de
  `echo lepton-uart1-<n>` et l'apparition de messages asynchrones `rcv SIGCHLD` entre deux
  commandes ; la même variation existe entre `env-32-apres` et `env-34-avant`. Ignorés : date,
  jeton, lignes `rcv SIGCHLD`.
- E-2 : empreintes des `.elf`, `.bin`, `.hex` différentes (date de compilation dans l'image),
  comme entre `env-32-apres` et `env-34-avant`.

### 5.2 `verifier-import.sh` (`env-34-hal-f4/verifications/`, listes `env-34-hal-f4/listes/`)

| Copie | Révision | Résultat |
| --- | --- | --- |
| F4 `hal_driver/` | `v1.8.5` | 200 identiques, 0 écart |
| F4 `cmsis-5/Device/ST/STM32F4xx/` | `3c77349` | 6 identiques, 0 écart |
| F7 `hal_driver/` (lecture seule) | `e1446fa` (`v1.3.3`) | 196 identiques, 0 écart |
| F7 `cmsis-5/Device/ST/STM32F7xx/` (lecture seule) | `2352e88` (`v1.2.10`) | 5 identiques, 0 écart |
| noyau `cmsis-5/CMSIS/Core/Include` (`--liste-seule`, 8 fichiers) | `5.9.0` | `core_cm4.h` `OK` ; 7 `CR` (fins de ligne seules, attendu, provenance) |

Test négatif du script sur une copie altérée du CMSIS device F7 : `TROP`, `DIFF`, `CR`,
`MANQUE` détectés, code 1 ; usage incorrect : code 2.

### 5.3 Compilation à blanc (`scripts/tiers/compiler-hal-f4-a-blanc.sh`)

Hors du trunk et des presets (`~/lepton-tools-dev/essais/env-34-hal-blanc`), 90 sources
(`Src/*.c` hors modèles et `Legacy/`), `stm32f4xx_hal_conf.h` = modèle copié sans modification
(tous modules activés), `-mcpu=cortex-m4 -mthumb -mfpu=fpv4-sp-d16 -mfloat-abi=hard -O2 -Wall`,
arm-none-eabi-gcc 14.2.1. Résumé `env-34-hal-f4/compilation-a-blanc/resume.txt` :

| Puce | Ordre | Échecs | Avertissements | `core_cm4.h` retenu (`-H`) |
| --- | --- | --- | --- | --- |
| `STM32F429xx` | `v330` (V3.30 en tête, ordre actuel des presets) | 1 | 0 | `cmsis/CMSIS/Include` (V3.30) |
| `STM32F429xx` | `cmsis5` (CMSIS 5 seul) | **0** | 0 | `cmsis-5/CMSIS/Core/Include` (5.9.0) |
| `STM32F439xx` | `v330` | 1 | 0 | V3.30 |
| `STM32F439xx` | `cmsis5` | **0** | 0 | 5.9.0 |

Échec de l'ordre `v330` : `stm32f4xx_ll_usb.c`, `__UNALIGNED_UINT32_READ` et
`__UNALIGNED_UINT32_WRITE` non déclarés (macros de `cmsis_gcc.h` de CMSIS 5, absentes de V3.30) ;
journal `compilation-a-blanc/STM32F429xx-v330-stm32f4xx_ll_usb.log`. L'ensemble importé est
complet avec CMSIS 5 ; avec V3.30 en tête, seul le module USB bas niveau échoue. Donnée pour le
PA-57. Le code de retour du script est 1 tant que l'ordre `v330` échoue : le critère d'ENV-36 C4
est la ligne `cmsis5` à 0 échec et les lignes `v330` identiques au Mac.

### 5.4 Copies de HAL F4 dans l'arbre

`find -L trunk` : `stm32f4xx_hal*` seulement sous `hal_driver/` (avec provenance) et sous
`driverlib/` : `stm32_hal_legacy.h`, `stm32f4xx_hal_def.h`, `stm32f4xx_hal_gpio.h`,
`stm32f4xx_hal_gpio_ex.h` (V1.3.0, sans provenance). Aucun n'est inclus par une source compilée
de la famille, des BSP ou du noyau (`grep`). L'étape interdit de modifier `driverlib/` : écart au
critère « aucune copie de HAL F4 sans provenance », renvoyé à ENV-35 (sort de la SPL, PA-57).
`stm32f4xx.h` : trois copies (`cmsis-5/Device/ST/STM32F4xx/Include` importée,
`cmsis/Device/st/stm32f4xx/` et `driverlib/` de la SPL compilée).
