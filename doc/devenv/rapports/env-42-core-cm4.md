# ENV-42 — `core_cm4.h` : un seul CMSIS-Core pour les Cortex-M4

Session du 2026-11-06. Point de départ : clone noyau `master` 885696c, lepton-tools `main` d6366d1,
oracle de référence `oracles/env-41-apres/`. Pièces : `env-42-core-cm4/audit/`.

## 1. Audit (lecture seule sur `<ROOTSTOCK>`)

Méthode : `ninja -t deps` sur les répertoires de construction de l'oracle d'ENV-41
(`audit/entetes-cmsis.sh`, liste exacte des en-têtes de chaque objet) ; ordre des `-I` tiré de
`compile_commands.json` (`audit/ordre-inclusions.py`). Essais sur la copie
`~/lepton-tools-dev/essais/env-42-copie` (`cp -RP` de `depots/`, `trunk/`, `third_party/` et des
deux fichiers `.scion.*` de la racine), construction à neuf des 16 presets par
`audit/oracle-16.sh` (= `rejouer-oracle.sh`, arguments d'ENV-41 : 6 QEMU, 10 cartes).

### 1.1 En-têtes CMSIS-Core retenus

| Presets | Cœur | En-têtes CMSIS-Core inclus (objets) | `-I` CMSIS (position) |
| --- | --- | --- | --- |
| `qemu-mps2-an386-*` (4) | M4F | V3.30 : `core_cm4.h`, `core_cmInstr.h`, `core_cmFunc.h`, `core_cm4_simd.h` (1 objet : `qemu_mps2_board.c`) | `cmsis/CMSIS/Include` (2) |
| `nucleo-f429zi-*`, `nucleo-f439zi-*` (4) | M4F | V3.30, mêmes 4 en-têtes (10 objets : HAL GPIO, RCC, CORTEX, ETH, `gpio.c`, `uart.c`, `dev_stm32f4xx_{uart_x,eth_x,hal_tick}.c`, carte) | V3.30 (2) ; device F4 `cmsis-5/Device/ST/STM32F4xx/Include` (7) |
| `nucleo-wl55jc1-*` (2) | M4 | V3.30, mêmes 4 en-têtes (24 objets : HAL WL, radio, BSP) | V3.30 (2) ; device WL `cmsis/Device/st/stm32wlxx` (7) |
| `qemu-mps2-an500-*`, `stm32f746g-disco-*` (4) | M7 | CMSIS 5 seul : `core_cm7.h`, `cmsis_compiler.h`, `cmsis_gcc.h`, `cmsis_version.h`, `mpu_armv7.h`, `cachel1_armv7.h` ; **aucun en-tête V3.30** | V3.30 (2, inutilisé) ; `cmsis-5/CMSIS/Core/Include` (5) |
| `samd21-xplained-pro-*` (2, armv6m) | M0+ | CMSIS 5 seul : `core_cm0plus.h` et 3 en-têtes communs | `cmsis-5` (1, `BEFORE` du BSP, PA-25 Q4) ; V3.30 (3) |

- Le `core_cm4.h` 5.9.0 n'est inclus par aucun preset (constat d'ENV-34 §1.5 confirmé).
- `arm_math.h`, `arm_common_tables.h`, `arm_const_structs.h`, `core_cm3.h`, `core_cm0*.h`,
  `core_sc*.h` de V3.30 : inclus par aucun preset. Les M7 n'utilisent rien de V3.30.
- Micro-noyau, KAL (`kal/arch/armv7m`), `kernel/core/arch/cortexm`, ports embOS
  (`core-segger/arch/armv7m`) et FreeRTOS (`core-freertos`) : **aucune** inclusion CMSIS.
- Version : l'en-tête des 4 fichiers V3.30 dit `V3.30` (17-24 février 2014), mais la macro
  `__CM4_CMSIS_VERSION_SUB` vaut `0x20` (3.20) ; le commentaire de `cmake/cpu/cortex-m7.cmake`
  parle de « CMSIS 3.20 ». Le paquet est noté « Version 2.10 » dans `cmsis/source.txt`.
- Les 8 fichiers de `cmsis-5/CMSIS/Core/Include` sont au niveau de CMSIS_5 `5.9.0`
  (`cmsis_gcc.h` V5.4.1, `cmsis_compiler.h` V5.1.0, `cmsis_version.h` V5.0.5, `core_cm4.h`
  V5.1.2) : ensemble cohérent, `core_cm4.h` y trouve ses dépendances.

### 1.2 Différences V3.30 / 5.9.0 sur le code compilé

API relevées dans les fichiers inclus par les objets M4 (`audit/comparer-fonctions.py`) :
`NVIC_{Set,Get}Priority`, `NVIC_{Enable,Disable,ClearPending,SetPending}IRQ`,
`NVIC_{Set,Get}PriorityGrouping`, `NVIC_EncodePriority`, `NVIC_SystemReset`, `SysTick_Config`,
`__DMB/__DSB/__ISB`, `__LDREX*/__STREX*`, `__RBIT`, `__CLZ`, `__{get,set}_PRIMASK`, `__WFE/__SEV/__WFI`,
`__disable_irq` ; `SCB->{AIRCR,SHCSR,SCR}`, `MPU->*`, `SysTick->CTRL`, `DWT->*`, `CoreDebug->DEMCR`.

| Élément | V3.30 | 5.9.0 | Effet |
| --- | --- | --- | --- |
| `NVIC_EnableIRQ` | écriture `ISER` | `__NVIC_EnableIRQ` : test `IRQn >= 0`, barrières de compilation | +4 octets (copie hors ligne : 0x18 → 0x1c) |
| `NVIC_DisableIRQ` | écriture `ICER` | idem + `__DSB(); __ISB()` après l'écriture | +12 octets (0x18 → 0x24) ; l'IRQ est effectivement masquée au retour (comportement plus sûr) |
| `NVIC_SetPriority`, `ClearPendingIRQ` | même calcul | test `IRQn >= 0`, casts | renommage `__NVIC_*`, taille identique |
| `NVIC_SystemReset` | `while(1);` | `for(;;) __NOP();` | non atteint en fonctionnement normal |
| `__DMB/__DSB/__ISB` | `"dmb"` sans clobber | `"dmb 0xF":::"memory"` | même instruction ; barrière de compilation en plus |
| `__set/get_PRIMASK` | variable registre | `MSR`/`MRS` explicites, clobber `memory` | même instruction |
| `__CLZ` | `clz` | `__builtin_clz`, 32 pour 0 | même résultat sur M4 |
| `__RBIT`, `LDREX/STREX`, `__disable_irq`, `SysTick_Config` | — | — | équivalents |
| Macros d'abstraction | `__ASM`, `__INLINE`, `__STATIC_INLINE` | + `__STATIC_FORCEINLINE`, `__UNALIGNED_UINT32_*`, `__PACKED`… | permet `stm32f4xx_ll_usb.c` |
| FPU | `__FPU_USED` selon `__FPU_PRESENT` et `__VFP_FP__` | idem | aucun écart |

### 1.3 Essais sur la copie

Base de la copie (`option0`) contre `oracles/env-41-apres/` : 16 presets en code 1, écarts limités à
`.debug_line` et `.debug_str` (chemin de la copie plus long). La copie sert donc de référence aux
essais (`audit/comparaisons/copie-vs-env41-*`).

- **Option 1a** : `cmake/cpu/cortex-m4f.cmake` ajoute
  `target_include_directories(lepton_options BEFORE INTERFACE …/cmsis-5/CMSIS/Core/Include)`
  (mécanisme du BSP SAMD21). Un seul fichier modifié.
- **Option 1b** : `cortex-m4f.cmake` ajoute `cmsis-5/CMSIS/Core/Include` sans `BEFORE` ; la ligne
  V3.30 de `cmake/isa/armv7m.cmake:18` passe dans `cmake/cpu/cortex-m3.cmake` (le seul cœur
  armv7m qui en a besoin, `core_cm3.h` n'existant pas dans `cmsis-5`). Chaque cœur choisit son
  CMSIS-Core, comme le M7 ; plus aucun preset M4 ou M7 ne voit V3.30.
- **Options 2 et 3** : aucun preset n'inclut le `core_cm4.h` 5.9.0 → binaires identiques par
  construction (rien à construire).

| Preset | Option 1a / base | `.text` (octets) | `.data`, `.bss`, autres sections chargées | Symboles | Option 1b / 1a | Fumée, banc KAL |
| --- | --- | --- | --- | --- | --- | --- |
| `qemu-mps2-an386-embos` | code 1 | 152652 → 152668 (+16) | identiques | `qemu_mps2_{eth,uart}_irq_enable` +8 | code 0 | identiques (19/19) |
| `qemu-mps2-an386-embos-soft` | code 1 | 152364 → 152380 (+16) | identiques | idem | code 0 | identiques (15/15) |
| `qemu-mps2-an386-freertos` | code 1 | 159568 → 159584 (+16) | identiques | idem | code 0 | identiques (19/19) |
| `qemu-mps2-an386-freertos-soft` | code 1 | 159212 → 159228 (+16) | identiques | idem | code 0 | identiques (15/15) |
| `nucleo-f429zi-embos` | code 1 | 161204 → 161236 (+32) | identiques | `NVIC_{En,Dis}ableIRQ` → `__NVIC_*` (+4, +12) ; `uart_{open,close,get_char,irq_handler}`, `nucleo_f439zi_eth_irq_enable` +4 à +10 | code 0 | — (carte) |
| `nucleo-f429zi-freertos` | code 1 | 167240 → 167288 (+48) | identiques | idem | code 0 | — |
| `nucleo-f439zi-embos` | code 1 | 161204 → 161236 (+32) | identiques | idem | code 0 | — |
| `nucleo-f439zi-freertos` | code 1 | 167240 → 167288 (+48) | identiques | idem | code 0 | — |
| `nucleo-wl55jc1-embos` | code 1 | 102480 → 102496 (+16) | identiques | `HAL_NVIC_{En,Dis}ableIRQ` +4, +12 ; `NVIC_SetPriority.constprop.0` renommé | code 0 | — |
| `nucleo-wl55jc1-freertos` | code 1 | 108004 → 108020 (+16) | identiques | idem | code 0 | — |
| `qemu-mps2-an500-*`, `stm32f746g-disco-*` (M7) | code 0 | — | — | — | code 0 | identiques (18/18) |
| `samd21-xplained-pro-*` | code 0 | — | — | — | code 0 | — |
| `host` | mklepton identiques, ctest 7/7 | | | | identiques | |

Écart maximal : `.text` +48 octets (+0,03 %) ; aucune donnée, aucune pile, aucun tas modifiés.
Avec l'option 1, les presets M4 n'incluent plus aucun en-tête V3.30 (`audit/entetes-option1/`).
Les écarts de `.debug_*` suivent ceux du code.

Compilation à blanc de la HAL F4 (`scripts/tiers/compiler-hal-f4-a-blanc.sh`, `audit/compilation-a-blanc/resume.txt`) :
ordre `v330` (actuel, options 2 et 3) : 1 échec (`stm32f4xx_ll_usb.c`) par puce ; ordre `cmsis5` :
0 échec. Ordre de l'option 1 (`cmsis-5` puis V3.30) : `stm32f4xx_ll_usb.c` compile (F429 et F439,
code 0). Option 2 : l'ordre `cmsis5` du script devient impossible (fichier retiré).

### 1.4 Code non configuré par les presets qui dépend de V3.30 (relevé, non traité)

- `cmsis/Device/ARM/ARMCM0`, `ARMCM3`, `atmel/samd20`, `lm3s`, `st/stm32f2xx` (noyau) : en-têtes de
  périphérique de l'époque V3.x.
- `kernel/dev/arch/cortexm/stm32f4xx/driverlib/stm32f469xx.h` (SPL conservée, ENV-35) :
  `#include "core_cm4.h"` ; avec l'option 1 il prendrait 5.9.0.
- `kernel/dev/arch/at91/softpack-lib/samv71/` (27 fichiers, `core_cm7.h`), `at91/asf/sam0/`
  (`core_cm0plus.h`) : résolus par CMSIS 5 s'ils étaient compilés.
- Cœur `cortex-m3` (`cmake/cpu/cortex-m3.cmake`, aucun preset) : seul utilisateur armv7m de V3.30
  (`core_cm3.h`).
- Le BSP `qemu-mps2-an386` inclut `cmsis/Device/ARM/ARMCM4/Include/ARMCM4.h` (arbre V3.30) par
  chemin ; ce fichier fonctionne avec le `core_cm4.h` 5.9.0 (essai ci-dessus). Son commentaire
  `qemu_mps2_machine.h:9` (« CMSIS-Core V3.30 de l'arbre ») deviendrait inexact avec l'option 1
  (greffon `bsp-qemu-mps2-an386`, hors des dépôts prévus par l'étape). Un `ARMCM4` CMSIS 5 existe
  dans `cmsis-5/Device/ARM/ARMCM4` ; changer d'en-tête de périphérique n'est pas proposé ici.

### 1.5 Conséquences pour le PA-71

- Option 1 (1a ou 1b) : même résultat binaire ; touche les 10 presets M4F/M4, écarts bornés et
  expliqués (§1.3) ; les M7 et M0+ inchangés (vérifié) ; la HAL F4 complète compile ; les
  presets M4 ne voient plus qu'un `core_cm4.h`. Aucune condition propre à une famille (BLD-6).
  - 1a : un fichier, `BEFORE` ; V3.30 reste dans les `-I` des M4 et M7 (masqué pour les M4).
  - 1b : trois fichiers CMake ; V3.30 sort des `-I` des M4 et M7 ; seul le M3 (sans preset) le garde.
- Option 2 : binaires identiques ; supprime l'importation d'ENV-34 et le seul moyen de compiler
  `stm32f4xx_ll_usb.c` ; contraire au sens d'ENV-34 (HAL complète).
- Option 3 : binaires identiques ; laisse deux `core_cm4.h` possibles (raison écrite dans la
  provenance).
- Sort de V3.30 (si option 1) : le supprimer casserait le M3, l'armv6m (`-I` de
  `cmake/isa/armv6m.cmake`) et le code du §1.4 → le garder dans l'arbre.
- Critère d'écart : mesuré +48 octets de `.text` au plus, données identiques ; précédent PA-57
  (`.text` ≤ +10 %, SRAM et CCM ≤ +5 %).
- Cartes : aucune sonde visible au démarrage de la session (`/dev/cu.usbmodem*` absent) ; la
  NUCLEO-F429ZI porte l'image `nucleo-f439zi-embos` de la VM (reflasher avant le banc de
  référence) ; le contrôle XPERIPHERALS du §4 exige la F429.

## 2. PA-71 (2026-11-06, décisions de l'utilisateur)

| Question | Décision |
| --- | --- |
| Option | 1b : `cortex-m4f.cmake` ajoute `cmsis-5/CMSIS/Core/Include` ; la ligne V3.30 d'`armv7m.cmake` passe dans `cortex-m3.cmake` |
| Sort de V3.30 | fichiers conservés dans l'arbre (M3, armv6m, code du §1.4) ; hors des `-I` des M4 et M7 |
| Critère d'écart | écarts mesurés exacts du §1.3 ; M7, M0+, host : code 0 ; tout autre écart bloque |
| Cartes et flash (PA-11) | NUCLEO-F429ZI et deux NUCLEO-WL55JC1, flash accordé ; banc de référence avant, banc après, vue XPERIPHERALS F429 |
| Commentaire du BSP an386 | corrigé dans `bsp-qemu-mps2-an386` (branche `devenv/env-42`) |

## 3. Oracle avant, banc de référence, modification

### 3.1 Oracle avant

`oracles/env-42-avant/` (`audit/oracle-16.sh <ROOTSTOCK>`, construction à neuf, host et 16 presets) :
16 × code 0 contre `oracles/env-41-apres/` ; mklepton identiques ; host 7/7 ; bancs KAL 19/15/19/15
(an386) et 18/18 (an500), 100 %.

### 3.2 Banc de référence sur carte (PA-11 accordé)

Sondes : WL55 A n° 002700253431510837393937 (`/dev/cu.usbmodem145103`), B n° 004F003E3431510937393937
(`/dev/cu.usbmodem1454403`), F429 n° 0672FF495252717267243842 (`/dev/cu.usbmodem1454303`) ; hôte du
test réseau 192.168.2.10 (`en0`). ELF reconstruits avec les variables de carte identiques à l'oracle
avant (`carte-oracle.txt`, code 0).

| Preset | Script | Résultat | Journaux (`oracles/env-42-avant/<P>/`) |
| --- | --- | --- | --- |
| `nucleo-wl55jc1-embos` | `env-42-core-cm4/banc-wl55.sh` (A et B flashées) | 16/16 ; radio A→B et B→A reçue | `carte.log`, `carte-detail.log`, `fumee-carte.log`, `radio-carte.log` |
| `nucleo-wl55jc1-freertos` | idem | 16/16 ; radio reçue dans les deux sens | idem |
| `nucleo-f429zi-embos` | `env-35-hal-f4/banc-carte.sh` (WL55 débranchées : le BSP F429 ne choisit pas sa sonde) | 20/20 (fumée, KAL, réseau) | `carte.log`, `carte-detail.log`, `fumee-carte.log`, `reseau-carte.log` |
| `nucleo-f429zi-freertos` | idem | 20/20 | idem |

`banc-wl55.sh` (nouveau) : forme de `banc-carte.sh` avec les variables de la paire d'ENV-32
(`LEPTON_BOARD_STLINK_SERIAL`, `LEPTON_RADIO_PEER_*`).

### 3.3 Modification

Commits faits dans la copie d'essai, puis repris dans `<ROOTSTOCK>` par `git fetch <copie>` et
`merge --ff-only` sur `devenv/env-42` :

| Dépôt | Commit | Contenu |
| --- | --- | --- |
| clone noyau | 484c44e | `cmake/cpu/cortex-m4f.cmake` (+ `cmsis-5/CMSIS/Core/Include`), `cmake/isa/armv7m.cmake` (ligne V3.30 retirée), `cmake/cpu/cortex-m3.cmake` (ligne V3.30 ajoutée), commentaire de `cmake/cpu/cortex-m7.cmake` |
| clone noyau | eb6c6c5 | `cmsis-5/CMSIS/Core/LEPTON-PROVENANCE.md` (inclusion, historique), `doc/migration/ajout-coeur.md` (CMSIS-Core posé par le cœur) |
| `bsp-qemu-mps2-an386` | 21ca883 | commentaire de `qemu_mps2_machine.h:9` |
| lepton-tools | c67b409 | aide de `scripts/tiers/compiler-hal-f4-a-blanc.sh` (ordre `cmsis5` = presets M4) |

Aucun fichier ajouté, déplacé ni supprimé : liens du trunk inchangés, pas de regreffe. Copie d'essai
avec ces commits : 16 presets identiques à l'essai 1b (code 0), mklepton identiques. `<ROOTSTOCK>` :
0 fichier régulier hors `.scion.grafted.list`, 0 lien cassé, `lepton check` code 0 (19 fichiers).

## 4. Contrôles

### 4.1 Oracle après

`oracles/env-42-apres/` (mêmes commandes) ; comparaisons `oracles/env-42-apres/comparaisons/<P>.txt`.

| Preset | Sections/symboles | `.text` | Empreinte | Fumée | Banc KAL | Écarts expliqués |
| --- | --- | --- | --- | --- | --- | --- |
| `qemu-mps2-an386-embos` | code 1, 8 écarts | +16 | différente | identique | 19/19 identique | oui (§1.3) |
| `qemu-mps2-an386-embos-soft` | code 1, 8 | +16 | différente | identique | 15/15 identique | oui |
| `qemu-mps2-an386-freertos` | code 1, 8 | +16 | différente | identique | 19/19 identique | oui |
| `qemu-mps2-an386-freertos-soft` | code 1, 8 | +16 | différente | identique | 15/15 identique | oui |
| `nucleo-f429zi-embos` | code 1, 17 | +32 | différente | — | — | oui |
| `nucleo-f429zi-freertos` | code 1, 17 | +48 | différente | — | — | oui |
| `nucleo-f439zi-embos` | code 1, 17 | +32 | différente | — | — | oui |
| `nucleo-f439zi-freertos` | code 1, 17 | +48 | différente | — | — | oui |
| `nucleo-wl55jc1-embos` | code 1, 10 | +16 | différente | — | — | oui |
| `nucleo-wl55jc1-freertos` | code 1, 10 | +16 | différente | — | — | oui |
| `qemu-mps2-an500-{embos,freertos}` | code 0 | = | — | identique | 18/18 identique | — |
| `stm32f746g-disco-{embos,freertos}` | code 0 | = | — | — | — | — |
| `samd21-xplained-pro-{embos,freertos}` | code 0 | = | — | — | — | — |
| `host` | mklepton identiques | | | | ctest 7/7 | — |

Critère du PA-71 : pour chacun des 10 presets concernés, la liste des écarts (sections hors
`.debug_*`, symboles) et le delta de `.text` sont **identiques** à ceux de l'essai 1a/1b du §1.3 ;
`.data`, `.bss` et les autres sections chargées sont inchangés. Les presets FreeRTOS ont un `.text`
plus court de 152 octets dans `<ROOTSTOCK>` que dans la copie, avant comme après (chaînes de chemin
`__FILE__`, chemin du rootstock plus court) : le delta n'en dépend pas. Hors périmètre : code 0.

`ctest -N` (`oracles/env-42-apres/ctest-N/`, `ctest --preset <P> -N` depuis le trunk sur les
répertoires neufs de l'oracle) : 17/17 identiques à `oracles/env-41-apres/ctest-N/` (état avant =
env-41-apres, §3.1).

En-têtes (`env-42-core-cm4/entetes-apres/`) : aucun en-tête V3.30 inclus par un preset ; les M4
n'incluent que le `core_cm4.h` 5.9.0, les M7 `core_cm7.h`, la M0+ `core_cm0plus.h` ;
`cmsis/CMSIS/Include` absent des `-I` des M4 et des M7 (présent pour la M0+, après `cmsis-5`).

Compilation à blanc de la HAL F4 (`env-42-core-cm4/compilation-a-blanc-apres/resume.txt`) : identique
à l'audit ; l'ordre des presets M4 est désormais `cmsis5` : **0 échec** (F429 et F439) ; la ligne
`v330`, gardée pour comparaison, reste à 1 échec (le script rend donc 1).

### 4.2 Cartes

| Preset | Résultat après | Comparaison au §3.2 |
| --- | --- | --- |
| `nucleo-f429zi-embos` | 20/20 | liste et résultats identiques |
| `nucleo-f429zi-freertos` | 20/20 | identiques |
| `nucleo-wl55jc1-embos` | 16/16 ; radio A→B, B→A reçue (4/4 lignes) | identiques |
| `nucleo-wl55jc1-freertos` | 16/16 ; radio reçue (4/4) | identiques |

ELF reconstruits avec les variables de carte : code 0 contre `oracles/env-42-apres/` (`carte-oracle.txt`).
Cartes laissées : F429 avec `nucleo-f429zi-embos` ENV-42 (écrite par `load` de la session de
débogage), WL55 A et B avec `nucleo-wl55jc1-freertos` ENV-42.

### 4.3 Vue des périphériques (VSCodium, utilisateur, 2026-11-06)

Espace `<ROOTSTOCK>/original-tree.code-workspace`, lancement « Déboguer nucleo-f429zi-embos (carte,
OpenOCD) » (`svdFile` `stm32f4xx/svd/STM32F429.svd`, inchangé depuis ENV-26), F429 seule branchée :
**registres `RCC` et `GPIOB` lisibles** dans XPERIPHERALS (confirmé par l'utilisateur). L'ELF après
la tâche de construction du lancement = oracle après (code 0). Référence : `env-26-dbg4.md` §4.
L'OpenOCD de Cortex-Debug est resté actif après la session jusqu'à la fermeture par l'utilisateur
(piège connu de la skill `lepton-cibles`).

### 4.4 Observations

- **O-1** : le BSP `nucleo-f429zi` ne choisit pas sa sonde (pas de `LEPTON_BOARD_STLINK_SERIAL`,
  contrairement au BSP `nucleo-wl55jc1`) : avec les WL55 branchées, OpenOCD prendrait la première
  sonde trouvée ; les bancs F429 ont été passés WL55 débranchées. Résidu, non traité.
- **O-2** : l'en-tête V3.30 se dit `V3.30` mais `__CM4_CMSIS_VERSION_SUB` vaut `0x20` ; le
  commentaire corrigé de `cortex-m7.cmake` dit désormais V3.30.
- **O-3** : le BSP an386 garde l'en-tête de périphérique `cmsis/Device/ARM/ARMCM4` de l'arbre V3.x,
  compilé avec le `core_cm4.h` 5.9.0 ; un `ARMCM4` CMSIS 5 existe sous `cmsis-5/Device/ARM/` (non
  proposé).
- **O-4** : copie d'essai `~/lepton-tools-dev/essais/env-42-copie` (487 Mo) conservée en attendant
  le PA-72.

## 5. PA-72 (2026-11-06, décisions de l'utilisateur)

Rapport accepté ; nouvel oracle de référence `oracles/env-42-apres/`. Publication : clone noyau,
puis `bsp-qemu-mps2-an386`, puis lepton-tools (fusions `--no-ff` de `devenv/env-42`, branches et
cibles poussées). Copie d'essai supprimée. O-1 : hors plan, révision suivante.
