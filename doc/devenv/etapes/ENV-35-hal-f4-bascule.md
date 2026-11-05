# Étape ENV-35 — Famille STM32F4 : passage de la SPL à la HAL, sur le modèle du F7

## Contexte
Après ENV-34, la famille `stm32f4xx` porte une HAL v1.8.5 et un CMSIS device tracés, mais elle
compile toujours la SPL de 2012. Cette SPL est formée de `driverlib/` V1.0.2 et de
`driverlib/stm32f4xx.h`, et elle sert les fichiers suivants :
- dans la famille : `gpio.c`, `uart.c`, `eth.c`, `dev_stm32f4xx/dev_stm32f4xx_uart_x.c`,
  `dev_stm32f4xx/dev_stm32f4xx_eth.c` ;
- dans le BSP : `nucleo_f439zi_board.c`, qui inclut `driverlib/stm32f4xx.h`.

Cette étape fait passer la famille et les BSP `nucleo-f429zi` et `nucleo-f439zi` à la HAL. C'est
le niveau 2 de la décision du 2026-11-04.

Modèle : la famille `stm32f7xx`, relevée le 2026-11-04 :
- HAL compilée pour GPIO, RCC, CORTEX et ETH seulement ;
- USART piloté par registres (`dev_stm32f7xx_uart_x.c`, module UART de la HAL désactivé) ;
- `SystemInit` par registres dans le BSP ;
- pas d'appel à `HAL_Init` ;
- `HAL_GetTick` fourni par Lepton (`dev_stm32f7xx_hal_tick.c`, depuis le tick du noyau) ;
- `stm32f7xx_hal_conf.h` dans le BSP ;
- `USE_HAL_DRIVER` et les inclusions publiques `hal_driver/Inc` et `cmsis-5/Device/ST/…`.

Archétype : portage, avec pour référence le comportement actuel sur NUCLEO-F429ZI. Les binaires
des 4 presets F4 changent ; ceux des 12 autres presets et de host ne doivent pas changer.

## Prérequis
- ENV-34 terminée et fusionnée : HAL, CMSIS device et `core_cm4.h` en place.
- Clones de `<ROOTSTOCK>` : `depots/lepton/family-stm32f4xx/master`,
  `depots/lepton/bsp-nucleo-f429zi/master`, `depots/lepton/bsp-nucleo-f439zi/master`,
  `depots/lepton/original/master`. Lecture seule : `depots/lepton/family-stm32f7xx/master`,
  `depots/lepton/bsp-stm32f746g-disco/master`.
- Référence carte (`rapports/env-24-cpufs.md` §6) : NUCLEO-F429ZI 20/20 en embOS et en FreeRTOS,
  `uname` `cortexM4-stm32f4`, ping 3/3, FTP LIST 13 entrées, RETR 57 octets identique. Le binaire
  F439 est essayé sur la F429 (E-5 d'ENV-20).
- Faits d'ENV-20 (`rapports/env-20-bsp.md`) :
  - K3 : aucun `stm32f439xx.h` avant ENV-34, d'où `STM32F429xx` dans le BSP F439 ;
  - K4 : garde de `driverlib/stm32f4xx_gpio.h` contre `stm32f4xx_hal_gpio_ex.h` ;
  - K7 et K8 : gestionnaires d'IRQ et extraction des membres d'archive ;
  - K9 : table de vecteurs unique.
- Skills `lepton-rootstock`, `lepton-oracle`, `lepton-cibles`. Branches `devenv/env-35` :
  lepton-tools, famille, les deux BSP, clone noyau si le §1 l'exige.

## Tâches

### 1. Audit (lecture seule) → PA-57
- Inventaire des appels SPL et des accès registres :
  - famille : 5 fichiers compilés, environ 2 200 lignes ;
  - BSP : `nucleo_f439zi_board.c` (254 lignes) et `nucleo_f439zi.h` des deux BSP.
  Produire une table SPL → HAL ou registres par fonction appelée.
- API Lepton F4 consommée par les BSP : `gpio.h`, `uart.h`, `eth.h`, `dma.h`, `types.h`, et la
  configuration de carte de `nucleo_f439zi.h`. La comparer à la structure F7 : `dev_stm32f7xx_
  {uart_x,eth_x,hal_tick}.c` (153, 432 et 29 lignes) ; le BSP F746 appelle `HAL_GPIO_Init` et
  définit `HAL_ETH_MspInit`.
- Ethernet : la HAL F4 v1.8.5 a la même API que la HAL F7 v1.3.3 (`HAL_ETH_Transmit`,
  `HAL_ETH_ReadData`, `HAL_ETH_RxAllocateCallback`, `HAL_ETH_RxLinkCallback`), et les deux cartes
  ont un PHY LAN8742A. Évaluer la reprise de `dev_stm32f7xx_eth_x.c` : écarts F4/F7 (cache et MPU
  sans objet sur le F4), interface lwIP, gestionnaire `ETH_IRQHandler`.
- Coexistence SPL/HAL dans une même construction. Deux `stm32f4xx.h` sont en jeu :
  `driverlib/` (SPL) et `cmsis-5/Device/ST/STM32F4xx/Include` (ENV-34). Relever l'ordre des
  inclusions publiques et chaque `#include "stm32f4xx.h"` sans chemin. Garde K4.
- Dépendants de `driverlib/` et de `kernel/core/ucore/cmsis/Device/st/stm32f4xx/` hors des
  4 presets (relevé du 2026-11-04, BSP recomptés le 2026-11-05, PA-55 d'ENV-34) : BSP du noyau
  `kernel/dev/bsp/stm32f469i-eval` (3 fichiers), `discovery_f4` (1), `discovery_f4-baseboard-modem`
  (13), `olimex_p407` (2) ; `kernel/usb/stm32f4-usb-core` (4) ;
  `kernel/core/ucore/cmsis/Device/st/stm32f4xx` (2) ; XML Olimex. Les inclusions de
  `stm32f4xx_hal.h` hors plan (`stm32f4-usb-core` 3, `discovery_f4-baseboard-modem` 2,
  `stm32f469i-eval` 1) : `rapports/env-34-hal-f4.md` §1.3.
- Mémoire :
  - la CCM (`0x10000000`, `.ccm_bss`) est inaccessible au DMA (`ld/mem_nucleo-f439zi.ld`) :
    relever où sont placés les descripteurs et les tampons ETH. Constat du 2026-11-04 :
    `ld/common-cortexm.ld` place en `.ccm_bss` les pools lwIP sauf `PBUF_POOL`, les piles du
    noyau et de lwIP, la mémoire statique FreeRTOS ; le pilote ETH F4 actuel n'a aucun attribut
    de section ;
  - `core_cm4.h` : `cmake/isa/armv7m.cmake` place CMSIS-Core V3.30 en tête des inclusions de tous
    les presets M4 ; le `core_cm4.h` 5.9.0 importé en ENV-34 n'est vu par aucun preset
    (`rapports/env-34-hal-f4.md` §1.5). Choix à poser au PA-57, avec le résultat de la
    compilation à blanc d'ENV-34 dans les deux ordres ;
  - occupation flash et RAM actuelle (`lepton.occupation.txt`).
- Rapport `rapports/env-35-hal-f4.md`.
- **PA-57** : l'utilisateur valide :
  - Architecture : <À CONFIRMER au PA-57>.
    - Option 1 : l'API Lepton F4 (`gpio.h`, `uart.h`, `eth.h`) est conservée et réimplémentée sur
      la HAL ; les BSP sont peu touchés.
    - Option 2 : la structure F7 est adoptée (`dev_stm32f4xx_*` repris du F7, appels HAL dans le
      BSP) ; les BSP sont réécrits.
  - Modules HAL compilés et `MODULE_ENABLED` du `stm32f4xx_hal_conf.h` de chaque BSP. Proposition :
    GPIO, RCC, CORTEX, ETH, et FLASH/PWR si `SystemInit` l'exige, comme pour le F7.
  - USART : par registres comme le F7 (proposition), ou par `HAL_UART`.
  - Découpage :
    - en lots validés sur carte chacun (socle et console, puis Ethernet, puis retrait de la SPL),
      **seulement si** la coexistence SPL/HAL est démontrée par l'audit ;
    - sinon, un seul lot.
  - BSP F439 : passage à `STM32F439xx`, possible depuis ENV-34 (K3) <À CONFIRMER au PA-57>.
  - Sort de la SPL après le passage : retirée de la compilation, et selon les dépendants hors
    plan, fichiers conservés ou supprimés <À CONFIRMER au PA-57>.
  - Critère d'occupation flash et RAM des 4 presets F4 : <À CONFIRMER au PA-57>.
  - Cartes : NUCLEO-F429ZI, écriture flash accordée pour la session, câble Ethernet et adresse de
    l'hôte (`LEPTON_NET_TEST_HOST_IP`) <À CONFIRMER au PA-57>.
- Aucune modification avant la réponse.

### 2. Oracle avant
- Skill `lepton-oracle` : host et les 16 presets → `rapports/oracles/env-35-avant/`. Doit être
  conforme à `env-34-apres`.
- Banc sur carte de référence, NUCLEO-F429ZI : `nucleo-f429zi-{embos,freertos}` et
  `nucleo-f439zi-embos` ; journaux complets de `ctest -L board`, réseau compris.

### 3. Implémentation (lots du PA-57)
- Socle :
  - `stm32f4xx_hal_conf.h` dans chaque BSP, tiré de `stm32f4xx_hal_conf_template.h` v1.8.5,
    avec les modules du PA-57 et `HSE_VALUE` pris dans le manifeste (8 MHz) ;
  - tick HAL, sur le modèle de `dev_stm32f7xx_hal_tick.c` ;
  - manifeste de la famille : `USE_HAL_DRIVER`, inclusions publiques, fichiers HAL dans
    `sources`, retrait de `USE_STDPERIPH_DRIVER` et des fichiers SPL selon le lot ;
  - `SystemInit` reste écrit par registres, seule l'inclusion change.
- Console : GPIO et USART selon le PA-57.
- Ethernet : HAL ETH, PHY LAN8742A, descripteurs et tampons hors CCM.
- Retrait de la SPL de la compilation ; BSP F439 selon le PA-57.
- Commits séparés par lot ; déplacements mécaniques séparés des commits de fond ; lecteur commun
  `cmake/lepton_greffons.cmake` inchangé (BLD-6), sinon arrêt.
- `scion graft` sur une copie d'essai, puis sur `<ROOTSTOCK>`.

### 4. Contrôles → PA-58
- Oracle après :
  - code 0 sur host et les 12 presets hors F4 ;
  - 4 presets F4 : écarts listés et expliqués ; plus aucun symbole SPL ;
  - `nm` : chaque gestionnaire d'IRQ utilisé reste `T` à sa définition forte (K8).
- Listes `ctest -N` identiques sur les 16 presets.
- Cartes (`lepton-cibles`), NUCLEO-F429ZI, flash « Verified OK » :
  - `nucleo-f429zi-embos` et `-freertos` : 20/20 ;
  - `uname` `cortexM4-stm32f4` ;
  - ping 3/3 ;
  - FTP LIST et RETR identiques à la référence ;
  - binaire `nucleo-f439zi-embos` essayé sur la F429, comme en ENV-20.
- Occupation flash et RAM dans le critère du PA-57.
- `lepton check` code 0 ; vue des périphériques (SVD, DBG-4) toujours lisible sur la F429.
- **PA-58** : rapport ; push et fusions des branches `devenv/env-35` (PA-P). Validation Debian :
  ENV-36.

## Critères de validation
- [ ] PA-57 et PA-58 tranchés et consignés.
- [ ] Aucun fichier SPL compilé pour les 4 presets F4 ; `USE_STDPERIPH_DRIVER` absent.
- [ ] NUCLEO-F429ZI 20/20 en embOS et en FreeRTOS, réseau compris.
- [ ] Binaires inchangés hors F4 (code 0 sur 12 presets et host).
- [ ] Aucun fichier de la HAL ni du CMSIS device modifié (règle D1a ; contrôle
      `verifier-import.sh` d'ENV-34).

## Pièges connus
- `HAL_GetTick` n'avance pas avant le démarrage de l'ordonnanceur. Aucune fonction HAL à délai
  d'attente (`HAL_RCC_OscConfig`, `HAL_ETH_Init`, `HAL_Delay`) dans `SystemInit` ni avant le
  noyau : seulement en contexte de processus, à l'ouverture d'un pilote (note du F7).
- `HAL_Init` et `HAL_InitTick` prendraient le SysTick du micro-noyau : ne pas les appeler. Ne pas
  compiler `stm32f4xx_hal_timebase_*_template.c`.
- Deux `stm32f4xx.h` sur le chemin d'inclusion : la HAL qui reçoit celui de la SPL échoue de façon
  confuse. Vérifier le chemin effectivement retenu (`-H`) pour un fichier HAL et un fichier SPL.
- Le DMA ETH ne lit pas la CCM : descripteurs et tampons placés en `.ccm_bss` provoquent un
  silence réseau sans erreur de construction.
- Un seul pilote ETH à la fois : `Src/stm32f4xx_hal_eth.c` (nouvelle API) ou
  `Src/Legacy/stm32f4xx_hal_eth.c`, jamais les deux.
- Avec `STM32F439xx`, l'IRQ 79 s'appelle `CRYP_IRQn` ; la table de vecteurs reste unique (K9).
- Deux sondes ST-LINK branchées : toujours `-c "adapter serial <n°>"`. Avant tout banc, vérifier
  qu'aucune VM ne tient les cartes USB (incident d'ENV-32).
- Le code non compilé qui inclut `stm32f4xx_hal.h` (7 fichiers, ENV-34 §1) reste hors périmètre :
  il ne doit pas entrer dans `sources` à cette occasion.

## À la fin de l'étape
`DEVENV-STATUS.md` :
- statut et branches ;
- décisions PA-57 et PA-58 ;
- nouvel oracle de référence ;
- occupation des presets F4 ;
- journal.

Passation `handoff/env-35.md`.
