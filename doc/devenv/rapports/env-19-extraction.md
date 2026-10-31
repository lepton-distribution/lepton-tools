# ENV-19 — Extraction des cartes STM32F746G-DISCO et SAMD21 Xplained Pro (PA-25)

Relevé du 2026-10-31, lecture seule. Clone noyau `master` 8ba904b, graine `original-tree` 0f1275a,
scion 0.5.2.0. Chemins relatifs à `scion/` du clone ; `src/…` = `scion/sys/root/src/…`.
Méthode d'ENV-6 : `ninja -t deps` et `ninja -t inputs` des 15 builds de `<ROOTSTOCK>/build/`
(14 presets + `host`, configurés le 2026-10-31), chemins ramenés au trunk ; fichiers propres à une
carte = lus par ses 2 presets et par aucun des 11 autres builds. Listes brutes :
`<scratchpad>/audit/{F746,SAMD21}-seul.txt` (non versionnées ; rejouables par la même commande).

## 1. Constats

| # | Constat | Conséquence |
| --- | --- | --- |
| K1 | F746 : 32 fichiers propres ; SAMD21 : 81 (dont 62 en-têtes `component/`, `instance/`, `pio/` du DFP). Aucun fichier commun aux deux cartes et absent des autres builds. | Pas de partage F746 ↔ SAMD21. |
| K2 | Fichiers propres de nature générique (cœur, ISA, micro-noyau) : port FreeRTOS `ARM_CM7/r0p1` (F746) ; `startup_armv6m.c`, `embos_init_hw.c` armv6m, `kal/arch/armv6m/*`, `kal_freertos_frame.h` armv6m, `cmsis-5/CMSIS/Core/Include/core_cm0plus.h`, port FreeRTOS `ARM_CM0`, `mpu_syscall_numbers.h` (SAMD21). | Restent dans le noyau (R5 d'ENV-6, PA-2 Q3) : ils dépendent du cœur, pas de la carte. |
| K3 | Aucun fichier des répertoires candidats n'est inclus par du code hors périmètre (`git grep '#include'`), sauf les deux `user_kernel_mkconf.h` des cartes, qui partent avec elles. `at91samd20`, `samd20xplained_pro` et l'ASF `at91/asf` n'utilisent ni `dev_samd21` ni le DFP SAMD21 (mentions « SAMD21 » = macros ASF). | `at91samd20` et le BSP hérité `samd20xplained_pro` restent dans le noyau (R9), non touchés. |
| K4 | Vecteurs : les gestionnaires `IRQ37_Handler`, `IRQ61_Handler` (F746) et `IRQ12_Handler` (SAMD21) sont dans le `*_board.c` de la carte et appellent les instances de la carte (`&stm32f746g_disco_uart1`…). Toutes les IRQ utilisées sont < 64 : aucune extension `.isr_vector_ext`. | Pas de fichier `vecteurs` dans les familles ; table générique du noyau inchangée ; `*_board.c` en `demarrage`. |
| K5 | `HAL_GetTick`, `HAL_Delay` : forts dans `dev_stm32f7xx_hal_tick.c`, faibles dans `stm32f7xx_hal.c`, non compilé. Symboles `T` dans `lepton.elf`. | Source ordinaire de la famille ; pas de `remplacants_forts`. |
| K6 | `stm32f7xx_hal_conf.h` (configuration de la HAL, inclus par la HAL de la famille) est dans le répertoire du BSP, trouvé par l'inclusion publique du BSP. | Reste dans le BSP (convention ST : fichier propre au projet ou à la carte) ; la famille dépend d'un en-tête que tout BSP STM32F7 fournit. |
| K7 | Les presets `stm32f746g-disco-embos` et `samd21-xplained-pro-embos` n'ont pas `LEPTON_MKCONF` : le XML vient du module `cmake/boards` (`LEPTON_BOARD_MKCONF`). Une fois le BSP greffé, `lepton check` afficherait « LEPTON_MKCONF absent, XML non contrôlé » (`checks.py:417`) et `mklepton_empreintes.sh` ne trouverait pas le XML (il lit `LEPTON_MKCONF` du preset pour un BSP). | Question Q3. |
| K8 | SAMD21 : inclusion `BEFORE` de `cmsis-5/CMSIS/Core/Include` (CMSIS-Core 5 exigé par le DFP, avant le CMSIS 3.30 de l'ISA). Le manifeste n'exprime pas `BEFORE` ; seul le BSP a un `CMakeLists.txt` inclus par le lecteur. | Dans le `CMakeLists.txt` du BSP (question Q4). |
| K9 | `mklepton_empreintes.sh` nomme les sorties `<xml>` pour une carte transitoire et `<xml>-<carte>` pour un BSP ; `kernel_mkconf.h` contient le chemin de l'en-tête de carte. | Pour les 2 XML : noms de sortie et une ligne de `kernel_mkconf.h` changent ; autres sorties identiques ; nouvelle référence `tests/host/mklepton_empreintes.sha256` (écart démontré, comme ENV-6). Amende le critère « empreintes identiques » de l'étape. |
| K10 | Repli `cmake/boards` : branche `elseif` de `CMakeLists.txt:46-47`, boucle de `tests/host/mklepton_empreintes.sh:79` (une boucle sur un répertoire vide échoue : motif non développé → « illisible », code 2), commentaires dans `CMakeLists.txt`, `cmake/cpu/cortex-m7.cmake:23`, `cmake/kal/{embos,freertos}.cmake`, `cmake/components/kernel.cmake:144,162`. | Question Q5. |
| K11 | `scion seed-clone` ne clone pas si `depots/lepton/<clé>/master/.git` existe (`graft.py:_fetch`) : dépôts locaux créés d'abord, `origin` = URL `https://` publique, pushurl SSH. | Regreffe possible avant toute création GitHub ; création et push au PA-26 (PA-P). |
| K12 | lepton : aucun code propre à ces cartes ; les tests utilisent des fixtures (`absente-embos`, `board-absent`). Après greffe, `generate` produit tâches et `launch` OpenOCD pour les 4 presets (sonde lue dans le manifeste) ; l'information « BSP non greffé » disparaît. | Pas de modification de lepton attendue ; constat dans le rapport final. |
| K13 | `git` : `~/.gitignore_global` ignore `*~`, `.DS_Store`, `*.swp` ; aucun fichier candidat concerné ; greffons F4 et WL sans `.gitignore`. | Pas de `.gitignore` dans les nouveaux dépôts (E1 sans effet). |

## 2. Règles reprises d'ENV-6 et d'ENV-13

- Dépôts : `<ROOTSTOCK>/depots/lepton/<clé>/master`, `master` (commit d'import à l'identique citant
  8ba904b), puis `devenv/env-19` (manifeste, `CMakeLists.txt`, retouches de chemins).
  `origin` `https://github.com/lepton-distribution/lepton-{famille,bsp}-<nom>.git`, pushurl `ssh://git@github.com/…`.
- Graine : 2 lignes par carte dans `.scion.sources.list` et `.scion.ramifications` (version `master`).
- Destinations : famille au chemin actuel (`kernel/dev/arch/cortexm/<famille>`) ; CMSIS device au
  même chemin de trunk dans le greffon famille (comme `stm32f4xx`) ; BSP sous
  `kernel/dev/bsp/<nom du greffon>` (Q12 d'ENV-6 : `stm32f746g_disco` → `stm32f746g-disco`).
- Restent dans le noyau : K2 ; XML `sys/user/tauon-basic/etc/mkconf_tauon_basic_{stm32f746g_disco,samd21_xplained_pro}.xml`
  et `etc/{stm32f746g-disco,samd21-xplained-pro}/{.boot,.init}` (PA-7 Q4) ; `debug/gdbinit-lepton`.
- Historique : `git rm` dans le clone noyau (commit mécanique), import dans le greffon.

## 3. Liste d'extraction

### 3.1 Famille `stm32f7xx` (clé `family-stm32f7xx`, bibliothèque `kernel`)

| Origine (clone noyau) | Destination (trunk inchangé) |
| --- | --- |
| `src/kernel/dev/arch/cortexm/stm32f7xx/` (202 fichiers : `dev_stm32f7xx/` 5, `hal_driver/` STM32CubeF7 1.17.4 : `Inc/` 101, `Src/` 93, `LEPTON-PROVENANCE.md`, `LICENSE.md`, `README.md`) | même chemin |
| `src/kernel/core/ucore/cmsis-5/Device/ST/STM32F7xx/` (6 fichiers) | même chemin |
| — | `lepton-greffon.json` (ci-dessous) |

Manifeste : `sources` = les 7 fichiers du module (`dev_stm32f7xx_{uart_x,eth_x,hal_tick}.c`,
`hal_driver/Src/stm32f7xx_hal_{gpio,eth,rcc,cortex}.c`) ; `coeurs` `[cortex-m7]` ; `mcu`
`[STM32F746xx]` ; `dependances` `[lepton-noyau]` ; publique : définition `USE_HAL_DRIVER`,
inclusions `…/stm32f7xx/dev_stm32f7xx`, `…/stm32f7xx/hal_driver/Inc`,
`kernel/core/ucore/cmsis-5/Device/ST/STM32F7xx/Include`. Ni `vecteurs` (K4) ni `remplacants_forts` (K5).

### 3.2 BSP `stm32f746g-disco` (clé `bsp-stm32f746g-disco`, destination `kernel/dev/bsp/stm32f746g-disco`)

| Origine | Destination |
| --- | --- |
| `src/kernel/dev/bsp/stm32f746g_disco/stm32f746g_disco_board.c` | `stm32f746g_disco_board.c` (`demarrage` : horloges 216 MHz, caches, USART1, Ethernet, IRQ 37 et 61) |
| `src/kernel/dev/bsp/stm32f746g_disco/{stm32f746g_disco.h,stm32f7xx_hal_conf.h}` | même nom (K6) |
| `ld/mem_stm32f746g-disco.ld` | `ld/mem_stm32f746g-disco.ld` |
| `sys/user/tauon-basic/src/arch/stm32f746g-disco/kernel_mkconf/include/user_kernel_mkconf.h` | `include/user_kernel_mkconf.h` (une ligne : `#include "kernel/dev/bsp/stm32f746g-disco/stm32f746g_disco.h"`) |
| `debug/openocd-stm32f746g-disco.cfg`, `debug/gdbinit-stm32f746g-disco` | `debug/…` (commentaires d'en-tête : chemins) |
| `cmake/boards/stm32f746g-disco.cmake` | supprimé : manifeste + `CMakeLists.txt` du BSP |

Manifeste : `famille` `stm32f7xx`, `coeur` `cortex-m7`, `mcu` `STM32F746NG`, `frequence_cpu`
216000000, `entete_config_noyau`, `script_liens`, `demarrage`, `openocd`, `sonde` `stlink` ;
publique : `STM32F746xx`, `HSE_VALUE=25000000`, `USE_ERRATUM_837070=1`, inclusion
`kernel/dev/bsp/stm32f746g-disco`.
`CMakeLists.txt` : contrôle `LEPTON_M7_FPU=sp` (message actuel), `LEPTON_NET_STACK lwip`,
`LEPTON_EMBOS_LIB_VARIANT _837070`, `LEPTON_FREERTOS_PORT ARM_CM7/r0p1`,
`LEPTON_BOARD_UNAME_MACHINE cortexM7-stm32f7` et `__KERNEL_CPU_DEVICE_NAME`, caches
`LEPTON_BOARD_SERIAL_PORT`, `LEPTON_NET_TEST_HOST_IP`, variables `LEPTON_NET_TEST_*` (modèle : BSP `nucleo-f429zi`).

### 3.3 Famille `samd21` (clé `family-samd21`, bibliothèque `kernel`)

| Origine | Destination (trunk inchangé) |
| --- | --- |
| `src/kernel/dev/arch/cortexm/samd21/dev_samd21/dev_samd21_uart_x.{c,h}` | même chemin |
| `src/kernel/core/ucore/cmsis-5/Device/Microchip/SAMD21/` (67 fichiers : DFP 3.8.270, `LEPTON-PROVENANCE.md`, `LICENSE.txt`) | même chemin |

Manifeste : `sources` `[dev_samd21/dev_samd21_uart_x.c]` ; `coeurs` `[cortex-m0plus]` ; `mcu`
`[ATSAMD21J18A]` ; publique : inclusions `…/samd21/dev_samd21`,
`kernel/core/ucore/cmsis-5/Device/Microchip/SAMD21/include`.

### 3.4 BSP `samd21-xplained-pro` (clé `bsp-samd21-xplained-pro`, destination `kernel/dev/bsp/samd21-xplained-pro`)

| Origine | Destination |
| --- | --- |
| `src/kernel/dev/bsp/samd21_xplained_pro/samd21_xplained_pro_board.c` | même nom (`demarrage` : horloges 48 MHz, SERCOM3, IRQ 12) |
| `src/kernel/dev/bsp/samd21_xplained_pro/samd21_xplained_pro.h` | même nom |
| `ld/mem_samd21-xplained-pro.ld` | `ld/…` |
| `sys/user/tauon-basic/src/arch/samd21-xplained-pro/kernel_mkconf/include/user_kernel_mkconf.h` | `include/user_kernel_mkconf.h` (une ligne d'inclusion) |
| `debug/openocd-samd21-xplained-pro.cfg`, `debug/gdbinit-samd21-xplained-pro` | `debug/…` |
| `cmake/boards/samd21-xplained-pro.cmake` | supprimé : manifeste + `CMakeLists.txt` |

Manifeste : `famille` `samd21`, `coeur` `cortex-m0plus`, `mcu` `ATSAMD21J18A`, `frequence_cpu`
48000000, `sonde` `cmsis-dap` ; publique : `__SAMD21J18A__`, inclusion `kernel/dev/bsp/samd21-xplained-pro`.
`CMakeLists.txt` : contrôle `LEPTON_CPU=cortex-m0plus` (redondant avec le lecteur, conservé ou
retiré : proposition retiré), `LEPTON_FREERTOS_CONFIG`, `LEPTON_BOARD_UNAME_MACHINE cortexM0p-samd21` et
`__KERNEL_CPU_DEVICE_NAME`, inclusion `BEFORE` de CMSIS-Core 5 (K8), cache `LEPTON_BOARD_SERIAL_PORT`.

### 3.5 Clone noyau (`devenv/env-19`)

- Commits mécaniques : `git rm` de tout ce qui est listé en 3.1-3.4, `cmake/boards/*.cmake` compris.
- Presets : Q3. Repli `cmake/boards` : Q5.
- `tests/host/mklepton_empreintes.sha256` : nouvelle référence (K9).
- `doc/BUILDING.md` §5, §6 : chemins `debug/` → `sys/root/src/kernel/dev/bsp/<carte>/debug/` (H-2 d'ENV-17).
- Non touchés : `ci/run.sh` (presets inchangés de nom), `CLAUDE.md` du noyau (A-2 d'ENV-17), `doc/migration/` (figés).

## 4. BLD-6 (constat attendu)

Ajout des 4 greffons sans modification fonctionnelle du système de construction commun : lecteur
`lepton_greffons.cmake`, `kernel.cmake`, `cpu/`, `kal/`, `isa/` inchangés. Seules modifications
communes envisagées : presets (Q3), retrait du repli et commentaires (Q5), décidés ici et non
imposés par l'ajout.

## 5. Questions pour PA-25

| Q | Sujet | Proposition |
| --- | --- | --- |
| Q1 | Liste d'extraction §3 (y compris K2 : ports FreeRTOS, démarrage armv6m, CMSIS-Core restent ; K4 : IRQ dans le `board.c` ; K6 : `hal_conf` dans le BSP) | Valider telle quelle. |
| Q2 | Noms des greffons et dépôts | `family-stm32f7xx` / `lepton-famille-stm32f7xx`, `bsp-stm32f746g-disco` / `lepton-bsp-stm32f746g-disco`, `family-samd21` / `lepton-famille-samd21`, `bsp-samd21-xplained-pro` / `lepton-bsp-samd21-xplained-pro` ; dépôts GitHub publics créés au PA-26 (par l'utilisateur ou `gh` sur accord). |
| Q3 | `LEPTON_MKCONF` des presets F746 et SAMD21 (K7) | Ajouter `LEPTON_MKCONF` aux 2 presets `-embos` (les `-freertos` héritent), comme les autres cartes (PA-7 Q4) ; variante : le `CMakeLists.txt` du BSP pose `LEPTON_BOARD_MKCONF`, presets inchangés mais XML non contrôlé par `lepton check`. |
| Q4 | Inclusion `BEFORE` de CMSIS-Core 5 (K8) | Dans le `CMakeLists.txt` du BSP SAMD21, commentée ; pas d'extension du schéma. |
| Q5 | Repli `cmake/boards` (K10) | Retiré : branche `elseif` de `CMakeLists.txt`, boucle de `mklepton_empreintes.sh`, commentaires ; message O1 sans « carte transitoire ». Toute carte future = greffon BSP (BLD-6). |
| Q6 | Cartes disponibles (flash, fumée, banc KAL) | À indiquer ; à défaut, construction, symboles et empreintes seulement (comme ENV-6). |
| Q7 | Critère « empreintes mklepton identiques » (K9) | Amendé : identiques hors noms de sortie et ligne d'en-tête de `kernel_mkconf.h` des 2 XML, écart démontré par `diff`. |

## 6. Réponses du PA-25 (2026-10-31, utilisateur)

Q1, Q4, Q7 : validées telles que proposées. Q2 : noms proposés ; dépôts locaux d'abord, création
GitHub et push au PA-26. Q3 et Q5 : `LEPTON_MKCONF` ajouté aux 2 presets `-embos`, repli
`cmake/boards` retiré. Q6 : STM32F746G-DISCO et SAMD21 Xplained Pro disponibles (flash, fumée,
banc KAL sur carte).
