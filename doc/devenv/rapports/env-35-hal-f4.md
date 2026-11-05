# ENV-35 — Famille STM32F4 : passage de la SPL à la HAL — rapport

Session du 2026-11-05. Branches `devenv/env-35` : lepton-tools (depuis `main` 5ce58de),
`family-stm32f4xx` (c5de4a5), `bsp-nucleo-f429zi` (2b2dfdd), `bsp-nucleo-f439zi` (bdbfa06).
Clone noyau non branché (aucun besoin établi par l'audit, voir §1.7).

## 1. Audit (lecture seule)

Méthode : lecture des clones ; `gcc -fsyntax-only -H` sur chaque unité de compilation des presets
F4, à partir de `compile_commands.json` de `<ROOTSTOCK>/build/<preset>` (script
`env-35-hal-f4/audit/hscan.py`, résultats `hscan-*.tsv`) ; essai de coexistence hors du trunk
(`audit/coex.py`, journaux `audit/coexistence/`).

### 1.1 Qui voit un en-tête ST

Sur les 169 unités de `nucleo-f429zi-embos` (176 en FreeRTOS, 169 pour `nucleo-f439zi-embos`),
**13 seulement** incluent un en-tête ST (`stm32*`, `core_cm*`, `system_stm32*`) : les 12 sources
de la famille listées dans `sources` et `nucleo_f439zi_board.c`. Aucune source du noyau, de lwIP
ni des applications. La table de vecteurs (`vecteurs/stm32f429xx_vectors.c`) n'en inclut aucun.
Le changement est donc confiné à la famille et aux deux BSP.

Chemin retenu aujourd'hui (`-H`) : `driverlib/stm32f4xx.h` (SPL V1.0.2 modifiée : inclut
`kernel/core/kernelconf.h`, aiguille vers `driverlib/stm32f429xx.h` V2.3.0) → `core_cm4.h` V3.30
de `cmsis/CMSIS/Include` → `driverlib/system_stm32f4xx.h` → `stm32f4xx_conf.h` (SPL).

### 1.2 Table SPL → HAL ou registres (sources compilées)

| Fichier (lignes) | Appels SPL (nombre d'occurrences) | Cible proposée |
| --- | --- | --- |
| `gpio.c` (314) | `GPIO_Init`×2, `GPIO_SetBits`/`ResetBits`/`ToggleBits`×2, `GPIO_WriteBit`, `GPIO_Write`, `GPIO_Read{Input,Output}DataBit`, `GPIO_ReadInputData`, `GPIO_PinAFConfig`, `GPIO_EXTILineConfig`, `EXTI_Init`×2, `EXTI_ClearITPendingBit`×2, `RCC_AHB1PeriphClockCmd`, `NVIC_{En,Dis}ableIRQ` | `HAL_GPIO_Init` (AF dans `GPIO_InitTypeDef.Alternate`, EXTI compris), `HAL_GPIO_{Write,Read,Toggle}Pin`, `__HAL_RCC_GPIOx_CLK_ENABLE`, `__HAL_GPIO_EXTI_CLEAR_IT` ; NVIC CMSIS inchangé |
| `uart.c` (557) | `USART_Init`/`StructInit`/`DeInit`/`Cmd`, `USART_ITConfig`×12, `USART_GetITStatus`×4, `USART_ClearITPendingBit`×2, `USART_{Send,Receive}Data`, `USART_DMACmd`×2, `USART_ChangeBaudrate` (**ajout Lepton dans `driverlib/stm32f4xx_usart.c:1471`**), `DMA_Init`/`StructInit`/`DeInit`/`Cmd`/`ITConfig`/`ClearITPendingBit`×4/`GetCurrDataCounter` (réception DMA circulaire + IDLE), `NVIC_*` | registres USART (SR, DR, BRR, CR1-3) et DMA (Sx CR/NDTR/PAR/M0AR, LIFCR/HIFCR), comme le F7 qui pilote l'USART par registres ; conception actuelle (DMA circulaire, IDLE, TXE/TC) conservée |
| `eth.c` (522) | API ETH de la SPL (`ETH_Init`, `ETH_DMA{Tx,Rx}DescChainInit`, `ETH_Start`, `ETH_ReadPHYRegister`×4, `ETH_Prepare_Transmit_Descriptors`, `ETH_Get_Received_Frame_interrupt`, …), `SYSCFG_ETH_MediaInterfaceConfig`, `GPIO_Init`/`PinAFConfig`, `RCC_*`, `NVIC_Init`, `NVIC_PriorityGroupConfig` | remplacé (voir §1.4) |
| `dev_stm32f4xx/dev_stm32f4xx_eth.c` (402) | aucun appel SPL ; `ETH_IRQHandler` (accès `ETH->DMASR`), couche `/dev/eth0` sur `eth.c` | remplacé (voir §1.4) |
| `dev_stm32f4xx/dev_stm32f4xx_uart_x.c` (427) | aucun appel SPL ; inclut `driverlib/stm32f4xx.h` (types) ; s'appuie sur `uart.c` | inclusion seule |
| `nucleo_f439zi_board.c` (254, BSP) | `SystemInit` par registres (inclusion seule) ; `SystemCoreClockUpdate` → `RCC_GetClocksFreq` ; `RCC_AHB1PeriphClockCmd` ; constantes SPL dans les descripteurs : `GPIO_Pin_n`, `RCC_APB{1,2}PeriphClockCmd` (pointeur de fonction), `RCC_APB1Periph_USART3`, `DMA_Channel_4/5`, `GPIO_AF_USART3/6`, `GPIO_PinSourceN`, `RCC_AHB1Periph_GPIOx`, `GPIO_Speed_100MHz` | `SystemInit` inchangé hors inclusion ; `SystemCoreClockUpdate` par registres ou `HAL_RCC_GetSysClockFreq` ; descripteurs réécrits sans constante SPL |
| `nucleo_f439zi.h` (BSP) | `_GPIO_DEFAULT_SPEED GPIO_Speed_50MHz` | constante HAL (`GPIO_SPEED_FREQ_*`) ou valeur Lepton |

`SystemInit` utilise `RCC_*`, `PWR_CR_VOS`, `FLASH_ACR_*` du `stm32f429xx.h` ; le CMSIS device
3c77349 les fournit (et les `_Pos` que le BSP redéfinit localement, `NUCLEO_F439ZI_PLLN_POS`…).

### 1.3 API Lepton F4 consommée par les BSP, comparée au F7

| Élément | F4 actuel | F7 (modèle) |
| --- | --- | --- |
| GPIO | `gpio.h` : `_Gpio_Descriptor` (port, broche SPL, mode Lepton), `gpio_init`/`set`/`reset`/… ; table `Gpio_Descriptor[]` du BSP | aucune couche : `HAL_GPIO_Init` dans le BSP |
| USART | `uart.h` : `_Uart_Descriptor` porte des **types et une fonction SPL** (`RCC_APBxPeriphClockCmd(uint32_t, FunctionalState)`, `DMA_Channel` SPL, `GPIO_AF`) ; `uart.c` + `dev_stm32f4xx_uart_x.c` ; DMA de réception | `dev_stm32f7xx_uart_x.c` (153 l.) : base, horloge, `irq_enable` du BSP, réception par IRQ dans un anneau de 256 octets, registres de l'USART **nouvelle génération** (ISR/ICR/RDR/TDR) : non transposable tel quel au F4 (USART SR/DR) |
| Ethernet | `eth.h` : `eth_stm32f4x7_bsp_t` (horloges `RCC_AHB1Periph_*`, `GPIOSpeed_TypeDef`, `GPIO_PinSourceN` : types SPL) ; `eth.c` + `dev_stm32f4xx_eth.c` sur l'ETH de la SPL ; `ETH_IRQHandler` dans la famille | `dev_stm32f7xx_eth_x.c` (432 l.) sur la HAL ETH nouvelle API ; `HAL_ETH_MspInit` (broches, horloges) et `irq_enable` dans le BSP ; gestionnaire d'IRQ du BSP |
| DMA | `dma.h` : `DMA_IT_ALL_n` (constantes SPL), `dma_startup_init` = `RCC_AHB1PeriphClockCmd` | — |
| Tick HAL | — | `dev_stm32f7xx_hal_tick.c` (29 l.) : `HAL_GetTick`, `HAL_Delay` depuis `__kernel_get_timer_ticks` |
| `hal_conf` | — | `stm32f7xx_hal_conf.h` du BSP, généré par `tools/migration/hal_conf_stm32f7.py` du clone noyau (CORTEX, ETH, FLASH, GPIO, PWR, RCC) |

Conséquence : quelle que soit l'option, les descripteurs des BSP contiennent des constantes et des
types SPL et doivent être réécrits. L'option 1 ne laisse donc pas les BSP « peu touchés » : seuls
la forme des tables (`Gpio_Descriptor[]`, instances `ttys3`/`ttys6`) et l'API `uart_*` sont
conservables.

Collision de noms : `gpio.h` définit `GPIO_MODE_AF_PP` (0x2, même valeur que la HAL) et
`GPIO_MODE_AF_OD` (0x102 ; HAL : 0x12). Toute unité qui inclut `gpio.h` et la HAL reçoit une
redéfinition de valeur différente : à renommer dans `gpio.h` (option 1).

### 1.4 Ethernet : reprise de `dev_stm32f7xx_eth_x.c`

- MAC et DMA ETH identiques F4/F7 (même IP) ; HAL F4 v1.8.5 et F7 v1.3.3 : même API
  (`HAL_ETH_Transmit`, `HAL_ETH_ReadData`, `HAL_ETH_RxAllocateCallback`, `HAL_ETH_RxLinkCallback`,
  `HAL_ETH_TxFreeCallback`, `HAL_ETH_{Read,Write}PHYRegister`, `HAL_ETH_{Get,Set}MACConfig`) ;
  PHY LAN8742A sur les deux cartes (RMII).
- Propre au F7, à retirer : région MPU non cachable (`HAL_MPU_*`, `SCB_CleanInvalidateDCache`,
  `aligned(ETH_DMA_REGION_SIZE)` 16 Ko, `_Static_assert` sur la région). Le F4 n'a ni cache D ni
  besoin de MPU ; un alignement sur 4 octets (descripteurs) suffit.
- Interface : couche `/dev/eth0` Lepton (lecture/écriture de trames, `ioctl_eth`), pas d'interface
  lwIP directe ; même contrat que le pilote F4 actuel. Le F7 corrige un défaut connu du pilote F4 de
  l'étape 5 (perte de la trame lue d'avance par `isset_read`, commentaire de
  `dev_stm32f7xx_eth_x.c:14-15`).
- Gestionnaire : F4 `ETH_IRQHandler` (table de vecteurs F4 de la famille, K9) ; F7
  `HAL_ETH_IRQHandler` appelé par `dev_stm32f7xx_eth_x_interrupt`, gestionnaire nommé dans le BSP
  (table générique du F7). Pour le F4 : `ETH_IRQHandler` fort, défini dans le BSP (comme
  `USART3_IRQHandler`), qui appelle `dev_stm32f4xx_eth_x_interrupt` (K8 : vérifier `T` au `nm`).
- Mémoire : aujourd'hui `DMARxDscrTab`, `DMATxDscrTab`, `Rx_Buff`, `Tx_Buff` (2 × 7620 o) sont en
  `.bss` (SRAM, `0x2000xxxx`), pas en CCM. Le pilote F7 déclare `eth_dma` et son réservoir en
  `static` sans section : `.bss`, donc SRAM sur le F4 aussi. À vérifier au `nm` après construction
  (piège du DMA sur la CCM).

### 1.5 Coexistence SPL/HAL dans une même construction (essai hors trunk)

Essai : options exactes de `gpio.c` du preset `nucleo-f429zi-embos`, plus `-DUSE_HAL_DRIVER`,
`stm32f4xx_hal_conf.h` = modèle v1.8.5 non modifié, inclusions `hal_driver/Inc` et
`cmsis-5/Device/ST/STM32F4xx/Include` placées **après** (ordre actuel : le lecteur ajoute la liste
`inclusions` de la famille dans l'ordre du manifeste, à la suite de `cmsis/CMSIS/Include`) ou
**avant** `driverlib`. Résumé `env-35-hal-f4/audit/coexistence/resume.tsv` :

| Unité | HAL après `driverlib` | HAL avant `driverlib` |
| --- | --- | --- |
| HAL `gpio`, `rcc`, `cortex`, `eth` | **échec** (48 à 67 erreurs : `stm32f4xx.h` de la SPL retenu ; `driverlib/stm32f4xx_hal_gpio.h` V1.3.0 masque celui de la HAL) | succès, 0 avertissement |
| SPL `stm32f4xx_gpio.c` | succès | succès |
| SPL `stm32f4x7_eth.c` | succès | **échec** (`stm32f4x7_eth.h` inclut `"stm32f4xx.h"` sans chemin : reçoit celui du CMSIS) |
| Lepton `gpio.c`, `uart.c` | succès | succès (inclusion par chemin complet) |
| Lepton `eth.c` | succès | **échec** (`ETH_InitTypeDef` de la SPL et de la HAL dans la même unité) |

Conclusion : la coexistence n'est pas démontrée pour un découpage socle-console puis Ethernet.
Le seul ordre où la HAL compile casse l'Ethernet de la SPL, et les inclusions sont publiques pour
toute la famille (pas de portée par fichier qui passe avant `cmsis/CMSIS/Include`, §1.6). Selon la
règle de l'étape : **un seul lot**, avec des commits internes séparés et une seule validation sur
carte à la fin.

Garde K4 (`driverlib/stm32f4xx_gpio.h:333`, `#if !defined(STM32F429xx)` autour d'`IS_GPIO_AF`) :
sans objet une fois `driverlib` hors des inclusions. Elle ne couvre pas `STM32F439xx`.

### 1.6 `core_cm4.h`

- `cmake/isa/armv7m.cmake:18` (noyau) place `cmsis/CMSIS/Include` (V3.30) en position 2 pour tous
  les presets armv7m ; les inclusions de la famille et du BSP viennent après
  (`cmake/lepton_greffons.cmake:270-272`), les inclusions privées aussi (propriété de source
  ajoutée). Aucun manifeste ne peut faire passer `cmsis-5/CMSIS/Core/Include` devant V3.30.
- Essai §1.5 « avant » : les quatre modules HAL visés (GPIO, RCC, CORTEX, ETH) compilent sans
  erreur ni avertissement avec V3.30. La compilation à blanc d'ENV-34 (§5.3) : seul
  `stm32f4xx_ll_usb.c` exige CMSIS 5, et il n'est pas visé.
- Retenir 5.9.0 exige de modifier le noyau (`armv7m.cmake` ou `cpu/cortex-m4f.cmake`), ce qui
  touche aussi WL55 et an386 (cortex-m4f), dont les binaires ne doivent pas changer (critère de
  l'étape), ou une condition propre à la famille dans le CMake commun (BLD-6).

### 1.7 Dépendants hors plan, fragments de HAL de `driverlib/`

- Hors des 4 presets, références à `driverlib/` ou à `cmsis/Device/st/stm32f4xx/` (relevé de
  l'étape confirmé, `grep -R` sur le trunk) : BSP du noyau `stm32f469i-eval` (3),
  `discovery_f4` (1), `discovery_f4-baseboard-modem` (13), `olimex_p407` (2) ;
  `kernel/usb/stm32f4-usb-core` (inclusions sans chemin) ; `cmsis/Device/st/stm32f4xx` (2) ; XML
  `mkconf_tauon_basic_lwip_stm32f4-olimex-p407.xml`. Aucun n'est compilé par un preset. Fichiers
  hors de la famille : le retrait de la SPL de la compilation ne touche pas le noyau.
- `driverlib/` n'est pas une copie amont intacte : `stm32f4xx.h` modifié (inclut `kernelconf.h`,
  chemins complets), `USART_ChangeBaudrate` ajoutée dans `stm32f4xx_usart.c`. Historique git :
  un seul commit (import ENV-6, 3ef8e46).
- Les 4 fragments HAL V1.3.0 (`stm32_hal_legacy.h`, `stm32f4xx_hal_def.h`,
  `stm32f4xx_hal_gpio.h`, `stm32f4xx_hal_gpio_ex.h`) ne sont inclus par aucune source compilée,
  mais **nuisent** dès que `driverlib` précède `hal_driver/Inc` (§1.5 : masquage de
  `stm32f4xx_hal_gpio.h`).
- `tools/migration/hal_conf_stm32f7.py` (clone noyau, 55 lignes) produit le `hal_conf` du F7 ; il
  est cité dans l'en-tête de `stm32f7xx_hal_conf.h`.

### 1.8 Mémoire et occupation actuelle (`<ROOTSTOCK>/build`, `arm-none-eabi-size -A`)

Régions (`ld/mem_nucleo-f439zi.ld`) : FLASH 2048 Ko, RAM 192 Ko, CCM 64 Ko.

| Preset | flash (`lepton.occupation.txt`) | RAM (idem) | `.text` | `.data` | `.bss` | `.ccm_bss` |
| --- | --- | --- | --- | --- | --- | --- |
| `nucleo-f429zi-embos` | 162209 | 144817 | 159864 | 1056 | 98568 | 45256 (69 %) |
| `nucleo-f429zi-freertos` | 169083 | 156504 | 166580 | 1180 | 98976 | 56408 (86 %) |
| `nucleo-f439zi-embos` | 162209 | 144817 | 159864 | 1056 | 98568 | 45256 |
| `nucleo-f439zi-freertos` | 169083 | 156504 | 166580 | 1180 | 98976 | 56408 |

SRAM (`.data` + `.bss`) : 52 % ; CCM FreeRTOS : 86 %. Le pilote ETH n'ajoute rien en CCM s'il
reste en `.bss`.

### 1.9 Propositions au PA-57 (non validées)

1. Architecture : **mixte**, la plus proche du comportement de référence.
   - Ethernet sur la structure F7 : `dev_stm32f4xx/dev_stm32f4xx_eth_x.{c,h}` dérivé de
     `dev_stm32f7xx_eth_x.c` (MPU retirée), `HAL_ETH_MspInit`, `irq_enable` et `ETH_IRQHandler` dans
     le BSP ; `eth.c`, `eth.h`, `dev_stm32f4xx_eth.c` retirés de `sources`.
   - GPIO et USART : API Lepton F4 conservée (`gpio.h`, `uart.h`, `dev_stm32f4xx_uart_x.c`),
     `gpio.c` sur `HAL_GPIO`, `uart.c` et `dma.h` par registres (DMA circulaire conservé),
     `_Uart_Descriptor` sans type ni fonction SPL ; collision `GPIO_MODE_AF_*` levée dans `gpio.h`.
   - BSP : descripteurs réécrits sans constante SPL, `HAL_ETH_MspInit`.
2. Modules HAL compilés : GPIO, RCC, CORTEX, ETH ; `MODULE_ENABLED` : CORTEX, ETH, FLASH, GPIO,
   PWR, RCC (comme le F7 : FLASH et PWR pour les en-têtes appelés par RCC, sans source) ;
   `stm32f4xx_hal_conf.h` dans chaque BSP, généré depuis le modèle v1.8.5 par un script dérivé de
   `hal_conf_stm32f7.py`, `HSE_VALUE` 8 MHz. Tick : `dev_stm32f4xx/dev_stm32f4xx_hal_tick.c`.
3. USART par registres (comme le F7).
4. Découpage : un seul lot (coexistence non démontrée, §1.5).
5. BSP F439 : `STM32F439xx` (en-tête présent depuis ENV-34 ; HAL et vecteurs prêts).
6. SPL : retirée de `sources` et des inclusions, `USE_STDPERIPH_DRIVER` retiré ; fichiers de
   `driverlib/` conservés pour les dépendants hors plan, sauf les 4 fragments HAL V1.3.0
   supprimés ; description du manifeste mise à jour.
7. `core_cm4.h` : V3.30 conservé en ENV-35 (aucune modification du noyau) ; 5.9.0 reste importé et
   inutilisé.
8. Occupation : écarts listés et expliqués ; `.text` ≤ +10 % ; SRAM et CCM ≤ +5 % ; CCM sans
   ajout dû au pilote ETH.
9. Cartes : NUCLEO-F429ZI, écriture flash pour la session, câble Ethernet et
   `LEPTON_NET_TEST_HOST_IP` à donner par l'utilisateur.

## 2. PA-57 (2026-11-05, décisions de l'utilisateur)

Propositions 1 à 9 du §1.9 retenues telles quelles : architecture mixte ; modules et
`MODULE_ENABLED` ; USART par registres ; un seul lot ; `STM32F439xx` ; SPL hors compilation,
fichiers conservés, 4 fragments HAL V1.3.0 supprimés ; `core_cm4.h` V3.30 ; critère
d'occupation. Ajouts : générateur `scripts/tiers/hal_conf_stm32f4.py` dans lepton-tools (clone
noyau non touché) ; NUCLEO-F429ZI branchée avec câble Ethernet, écriture flash accordée pour la
session, `LEPTON_NET_TEST_HOST_IP` = 192.168.2.10 (`en0` ; 192.168.2.20, donnée d'abord, n'était portée
par aucune interface : corrigée par l'utilisateur). Sonde F429 seule vue par le Mac
(0672FF495252717267243842, `/dev/cu.usbmodem1454303`) ; VMware Fusion actif.

## 3. Oracle avant (tâche 2)

`rapports/oracles/env-35-avant/` : `rejouer-oracle.sh <ROOTSTOCK> … --qemu` ×6 `--carte` ×10
(constructions à neuf, journal `rejouer-oracle.log`) : « tout a réussi ». Contre `env-34-apres`
(`env-35-avant/comparaisons/`) : `comparer-oracle.py` code 0 ×16, host 7/7, empreintes mklepton
identiques, bancs KAL QEMU identiques (19, 15, 19, 15, 18, 18 tests, 100 %, mêmes listes). Listes
`ctest -N` de host et des 16 presets (`env-35-avant/ctest-N/`) identiques à `env-34-apres` (17/17).

Banc sur carte de référence, NUCLEO-F429ZI (ST-LINK/V2-1 0672FF495252717267243842,
`/dev/cu.usbmodem1454303`, hôte 192.168.2.10 sur `en0`, carte 192.168.2.5) :
`env-35-hal-f4/banc-carte.sh` (forme d'ENV-24 §6 : reconfiguration avec
`LEPTON_BOARD_SERIAL_PORT` et `LEPTON_NET_TEST_HOST_IP`, construction, `lepton.elf` comparé à
l'oracle (code 0), `ctest -L board`). Journaux `env-35-avant/<P>/carte*.log`, `fumee-carte.log`,
`reseau-carte.log`.

| Binaire | `lepton.elf` / oracle avant | Résultat | Fumée | Réseau |
| --- | --- | --- | --- | --- |
| `nucleo-f429zi-embos` | 0 écart | 20/20 | `cortexM4-stm32f4` | ping 3/3, LIST 13 entrées, RETR 57 octets identique, ECONNRESET=15 |
| `nucleo-f429zi-freertos` | 0 écart | 20/20 | `cortexM4-stm32f4` | idem |
| `nucleo-f439zi-embos` (sur F429) | 0 écart | 20/20 | `cortexM4-stm32f4` | idem |

Incident : premier lancement du script en échec avant `ctest` (chemin relatif de l'oracle perdu
après `cd` dans le trunk ; aucune écriture flash) ; corrigé, relancé.

## 4. Implémentation (tâche 3, un seul lot)

### 4.1 Famille `family-stm32f4xx` (`devenv/env-35`, depuis `master` c5de4a5)

| Commit | Contenu |
| --- | --- |
| 020db7b | Suppression des 4 fragments HAL V1.3.0 sans provenance de `driverlib/` (mécanique) |
| 02d36d8 | `dev_stm32f4xx/dev_stm32f4xx_eth_x.{c,h}` repris de `dev_stm32f7xx_eth_x.{c,h}` (MPU, `SCB_*` et alignement 16 Ko retirés ; bloc DMA en `.bss`) ; `dev_stm32f4xx_hal_tick.c` repris de `dev_stm32f7xx_hal_tick.c` |
| e68e250 | `gpio.c` sur `HAL_GPIO_Init`/`WritePin`/`ReadPin`/`TogglePin` ; mode Lepton traduit en mode HAL, fonction alternative (AFR) conservée ; `gpio_set_function` et `gpio_read_output` par registres (pas d'équivalent HAL) ; `kernelconf.h` inclus explicitement (arrivait par le `stm32f4xx.h` modifié de la SPL) ; `GPIO_MODE_AF_PP`/`AF_OD` retirés de `gpio.h` |
| a83f3cd | `uart.c` par registres : calculs de la SPL repris (`RCC_GetClocksFreq`, BRR de `USART_Init`/`USART_ChangeBaudrate`), réglages de `USART_StructInit`/`DMA_StructInit` ; effacement des indicateurs DMA par `dma_stream_clear_flags` (`dma.h`, calculé d'après l'adresse du flux) ; `_Uart_Descriptor` : `RCC_APBxENR`, `RCC_APBxRSTR`, bit, `UART_DMA_CHANNEL(n)` |
| 7252fe6 | Manifeste : `sources` (couche Lepton, ETH, tick, HAL GPIO, ETH, RCC, CORTEX), `USE_HAL_DRIVER`, inclusions `dev_stm32f4xx`, `hal_driver/Inc`, `cmsis-5/Device/ST/STM32F4xx/Include`, `mcu` + `STM32F439xx`, description |

Non compilés désormais : `driverlib/` (fichiers conservés), `eth.c`, `eth.h`,
`dev_stm32f4xx/dev_stm32f4xx_eth.c`, `stm32f4x7_eth_conf.h`.

### 4.2 BSP `nucleo-f429zi` et `nucleo-f439zi` (`devenv/env-35`)

| BSP | Commits | Contenu |
| --- | --- | --- |
| `nucleo-f429zi` (depuis 2b2dfdd) | 7799dcf, f8cbde4 | `stm32f4xx_hal_conf.h` généré (mécanique) ; `nucleo_f439zi_board.c` : `stm32f4xx_hal.h`, `SystemInit` inchangé, `SystemCoreClockUpdate` par registres (forme du F746), `GPIO_PIN_n`, descripteurs USART sans SPL (`GPIO_AF7_USART3`, `GPIO_AF8_USART6`), `HAL_ETH_MspInit` (mêmes broches, AF11, sans tirage, vitesse maximale), `ETH_IRQHandler` fort, instance `dev_stm32f4xx_eth_info_t` ; `dev_stm32f4xx_eth_map` gardé de nom (XML mklepton du noyau inchangé) ; `nucleo_f439zi.h` : `_GPIO_DEFAULT_SPEED` = `GPIO_SPEED_FREQ_HIGH` (même valeur 2), `BOARD_ETH_PHY_ADDR` ; manifeste : inclusion du BSP (pour `stm32f4xx_hal_conf.h`) |
| `nucleo-f439zi` (depuis bdbfa06) | 936de82, ad9819f | mêmes fichiers (identiques) ; `STM32F439xx` ; description et commentaire de `user_kernel_mkconf.h` |

Noyau non touché ; `cmake/lepton_greffons.cmake` inchangé (BLD-6). lepton-tools :
`scripts/tiers/hal_conf_stm32f4.py` (471d468).

### 4.3 Écarts de comportement introduits (à valider au PA-58)

- E-A, adresse MAC par défaut : celle du pilote F7, dérivée de l'identifiant unique de la puce
  (`0x02:…`, administrée localement), au lieu de la constante `00:bd:3b:33:05:71` du pilote SPL.
  Aucune adresse n'est posée par `.init`. Conséquence : adresse propre à chaque carte.
- E-B, PHY : adresse MDIO fixe `BOARD_ETH_PHY_ADDR` (0), comme le F7 ; le pilote SPL
  parcourait les adresses à partir de 0 et contrôlait l'identifiant du PHY.
- E-C, moment de l'initialisation : broches RMII, horloges ETH, `SYSCFG` (RMII), MAC et DMA sont
  configurés à la première ouverture de `/dev/eth0` (`_eth_start` : `HAL_ETH_Init`, donc
  `HAL_ETH_MspInit`, négociation du PHY, `HAL_ETH_Start_IT`), comme sur le F7 ; le pilote SPL les
  configurait au chargement (`dev_stm32f4xx_eth_load` → `eth_bsp_init`) et ne démarrait le MAC
  qu'à l'ouverture (`eth_init`). La HAL a besoin du tick, qui n'avance qu'après le démarrage du
  noyau (piège de l'étape).
