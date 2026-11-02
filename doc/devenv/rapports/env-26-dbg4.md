# ENV-26 — DBG-4 : vues des périphériques et des tâches — rapport

Session du 2026-11-02, hôte Mac. Branche lepton-tools `devenv/env-26` (depuis `main` 65da9d8).

## 1. Audit (lecture seule) → PA-39

### 1.1 État de départ

- Schéma : `svd` (`schemas/greffon.schema.json:158`) est un `chemin_relatif` du BSP, relatif à sa
  `destination` ; le motif interdit `..` (`$defs/chemin_relatif`) : un BSP ne peut pas désigner un
  fichier de sa famille sans modifier le schéma.
- `lepton check` : `svd` dans `SINGLE_FILE_FIELDS` (`lepton/checks.py:30`), fichier contrôlé dans la
  destination du greffon.
- `lepton generate` : `svdFile` = `<trunk>/sys/root/src/<destination du BSP>/<svd>`
  (`lepton/generate.py:398`, lancements QEMU et carte).
- Aucun BSP ne déclare `svd` ; aucun `.gitignore` dans les clones famille et BSP, aucun motif
  `*.svd` dans `~/.gitignore_global` : un SVD suivi est greffé (E1 de scion 0.5.2.0 sans effet).

| BSP | MCU (manifeste) | Famille | Sonde |
| --- | --- | --- | --- |
| `nucleo-f429zi` | STM32F429ZI | `stm32f4xx` | stlink |
| `nucleo-f439zi` | STM32F439ZI | `stm32f4xx` | stlink |
| `stm32f746g-disco` | STM32F746NG | `stm32f7xx` | stlink |
| `nucleo-wl55jc1` | STM32WL55JC (M4) | `stm32wlxx` | stlink |
| `samd21-xplained-pro` | ATSAMD21J18A | `samd21` | cmsis-dap |
| `qemu-mps2-an386` / `an500` | ARMCM4 / ARMCM7 | `qemu-mps2` | — (QEMU) |

### 1.2 Fichiers SVD : source, licence, taille

Sources consultées le 2026-11-02 (index `https://www.keil.com/pack/index.pidx`, packs téléchargés,
dépôts Open-CMSIS-Pack). En-têtes de licence relus par la session dans les fichiers extraits des
packs (`unzip`, aucun exécutable lancé).

| MCU | Pack (le plus récent de l'index) | Fichier dans le pack | Version SVD | Taille (o) | SHA-256 (16 premiers) | En-tête du fichier |
| --- | --- | --- | --- | --- | --- | --- |
| STM32F429ZI | `Keil::STM32F4xx_DFP` 3.1.1 (2025-08-18) | `CMSIS/SVD/STM32F429.svd` | 1.8 | 2 118 587 | `185ddfe09ebec697` | « Copyright (c) 2024 STMicroelectronics. SPDX-License-Identifier: Apache-2.0 » |
| STM32F439ZI | `Keil::STM32F4xx_DFP` 3.1.1 | `CMSIS/SVD/STM32F439.svd` | 1.3 | 2 071 506 | `c3de4e42c9fa2e01` | idem |
| STM32F746NG | `Keil::STM32F7xx_DFP` 3.1.1 (2025-07-29) | `CMSIS/SVD/STM32F746.svd` | 1.6 | 2 737 859 | `6fc35eb5b44199f5` | idem |
| STM32WL55JC (M4) | `Keil::STM32WLxx_DFP` 2.1.0 (2025-09-17) | `CMSIS/SVD/STM32WL5x_CM4.svd` (le pack fournit à part `STM32WL5x_CM0P.svd`) | 2.2 | 1 066 385 | `bc8642b4f6c1de77` | idem |
| ATSAMD21J18A | `Microchip::SAMD21_DFP` 3.8.270 (2026-02-11) | `samd21a/svd/ATSAMD21J18A.svd` | 0 | 990 887 | `1fba37ed6aacf969` | « Copyright (c) 2026 Microchip Technology Inc. SPDX-License-Identifier: Apache-2.0 » |

URL des packs : `https://www.keil.com/pack/Keil.STM32F4xx_DFP.3.1.1.pack`,
`…/Keil.STM32F7xx_DFP.3.1.1.pack`, `…/Keil.STM32WLxx_DFP.2.1.0.pack`,
`https://packs.download.microchip.com/Microchip.SAMD21_DFP.3.8.270.atpack`. Les mêmes SVD ST sont
publiés dans `github.com/Open-CMSIS-Pack/STM32F4xx_DFP`, `STM32F7xx_DFP`, `STM32WLxx_DFP`
(Apache-2.0 ; F429 : empreinte identique au pack). Fichier `LICENSES` du pack F4 :
« SPDX-License-Identifier: Apache-2.0 AND BSD-3-Clause … CMSIS add-ons are licensed under the
Apache-2.0 license » ; textes `LICENSE-Apache-2.0` joints aux packs.

Redistribution dans un dépôt public : **permise** pour les cinq fichiers (Apache-2.0 §4 : conserver
l'en-tête, joindre le texte de la licence, signaler toute modification ; aucun `NOTICE` dans les
packs).

Sources écartées :
- `cmsis-svd/cmsis-svd-data`, `data/STMicro/` (anciens SVD ST, F429 v1.2 sans FPU ni MPU, sans
  en-tête) : « End User License Agreement for STMicroelectronics (Version 1.0) », usage « solely for
  the purpose of » outils de développement → republication douteuse. F439 et WL absents.
- Page SVD de st.com (`stm32f4_svd.zip`…) : non vérifiée (serveur injoignable pendant la session).
- `Keil::SAMD21_DFP` 1.3.2 : marqué `deprecated="2020-10-21"` dans l'index.
- `STMicroelectronics/cmsis_device_f4`, `_f7`, `_wl` : aucun SVD.

Total à verser : F4 4,19 Mo (deux fichiers), F7 2,74 Mo, WL 1,07 Mo, SAMD21 0,99 Mo ; sous les
limites de GitHub (avertissement à 50 Mo par fichier).

### 1.3 Variante sans fichier versionné : service de packs

`mcu-debug.peripheral-viewer` 1.6.4 (README installé, code `src/cmsis-pack/pack-utils.ts`) accepte
une référence `<vendor>::<pack>@<version>` dans le chemin SVD et télécharge le SVD depuis
`https://pack-content.cmsis.io/<vendor>/<pack>/<version>/…`, avec `deviceName` et
`processorName`. Les 5 SVD et pdsc y répondent (HTTP 200, mêmes tailles). Exemple : `svdFile`
`Keil::STM32WLxx_DFP@2.1.0`, `deviceName` `STM32WL55JCIx`, `processorName` `CM4`. Non essayé sous
VSCodium. Inconvénients : réseau requis à chaque session de débogage, service tiers sans
documentation publique trouvée, champ `svd` du schéma à changer de nature (référence et non
fichier), `lepton check` ne peut plus vérifier.

### 1.4 Emplacement du SVD

- Un SVD décrit un MCU (sous-famille ST : `STM32F429` couvre tous les boîtiers F429). Il ne dépend
  pas de la carte.
- Règle PA-2 Q3 : la table de vecteurs par MCU est dans le greffon famille ; les fichiers ST/Microchip
  (CMSIS device, SPL, HAL) y sont déjà, avec leurs licences.
- Chaque BSP actuel a un MCU distinct ; F429 et F439 ont deux SVD distincts. Placé dans le BSP, un
  SVD n'est pas dupliqué aujourd'hui ; il le serait pour toute nouvelle carte du même MCU (BSP
  utilisateur créé par `lepton scion new`).
- Placé dans la famille, le BSP doit le désigner : le schéma doit changer (`..` interdit).

### 1.5 Vue des tâches

Deux mécanismes distincts :

1. **Extension `mcu-debug.rtos-views` 0.0.16** : lit les structures du RTOS par gdb
   (expressions évaluées dans la session de débogage), indépendamment du serveur gdb. Prend en
   charge embOS, FreeRTOS, ChibiOS, RTX5, ThreadX, uC/OS-II, Zephyr (`dist/extension.js`). Détection
   automatique ; aucun champ de lancement requis (réglage `mcu-debug.rtos-views.showRTOS`, vrai par
   défaut ; Cortex-Debug suivi par défaut). embOS : évalue `OS_Global`, `OS_Global.pTask`,
   `OS_Global.pObjNameRoot` ; noms des tâches si `OS_SUPPORT_TRACKNAME`, pile si
   `OS_SUPPORT_STACKCHECK`. Fonctionne aussi sous QEMU (même session gdb).
2. **Champ `rtos` de Cortex-Debug 1.13.0-pre6** (fils gdb, `info threads`, pile par tâche) : pour
   OpenOCD, « auto, FreeRTOS, ThreadX, chibios, Chromium-EC, eCos, embKernel, linux, mqx, nuttx,
   RIOT, uCOS-III, Zephyr » ; embOS seulement avec J-Link. OpenOCD 0.12.0 installé (chaînes du
   binaire et `openocd.info-2` §« RTOS Support ») : **pas d'embOS** (« embKernel » est un autre
   RTOS) ; FreeRTOS exige `pxCurrentTCB`, `pxReadyTasksLists`, `xDelayedTaskList1/2`,
   `pxDelayedTaskList`, `pxOverflowDelayedTaskList`, `xPendingReadyList`,
   `uxCurrentNumberOfTasks`, `uxTopUsedPriority`.

Symboles relevés (`arm-none-eabi-nm`, `arm-none-eabi-gdb -batch`) dans les ELF de
`<ROOTSTOCK>/build/` (construits le 2026-11-02) :

| Preset | embOS : `OS_Global` (type DWARF) | `OS_Global.pTask`, `.pObjNameRoot` | FreeRTOS : 9 symboles OpenOCD + listes de rtos-views |
| --- | --- | --- | --- |
| nucleo-f429zi | oui (104 o) | évaluables | tous présents, `uxTopUsedPriority` compris |
| nucleo-wl55jc1 | oui | évaluables | tous présents |
| stm32f746g-disco | oui | évaluables | tous présents |
| samd21-xplained-pro | oui | évaluables | tous présents |
| qemu-mps2-an386 | oui | évaluables | tous présents |

Bibliothèque embOS liée : `libosT7VHLSP.a` (F429, mode `OS_LIBMODE_SP`), `libosT6LSP.a` (SAMD21) ;
`RTOS.h` 5.20.0.0 l.691-700 : `SP` active `OS_SUPPORT_STACKCHECK` et `OS_SUPPORT_TRACKNAME`. Les
images actuelles suffisent : aucune modification du noyau ni des binaires.

### 1.6 QEMU

Le noyau contient `cmsis-5/Device/ARM/SVD/ARMCM4.svd` et `ARMCM7.svd` (BSD, ARM 2012, 11 829 o) :
exemples génériques, 2 périphériques (`SysTick` 0xE000E010, `WDT` fictif 0x40001000). Ils ne
décrivent ni les UART ni les temporisateurs CMSDK de `mps2-an386`/`an500` ; aucun SVD officiel
MPS2 trouvé dans les sources consultées. Intérêt faible ; la vue des tâches, elle, fonctionne sous
QEMU et permet un essai sans carte.

### 1.7 Propositions (soumises au PA-39)

- P-1 : SVD versionnés, tirés des packs du §1.2 (pas de service de packs).
- P-2 : SVD dans le greffon famille, sous `svd/` (un fichier par MCU, `LICENSE-Apache-2.0` et
  `README` de provenance : pack, version, empreinte), désigné par le BSP via une forme étendue du
  champ `svd` : chaîne = fichier du BSP (inchangé) ; objet `{"famille": "svd/STM32F429.svd"}` =
  fichier de la famille du BSP. `lepton check` contrôle le fichier dans la destination de la
  famille ; `generate` résout le chemin du trunk correspondant.
- P-3 : vue des tâches par rtos-views pour embOS et FreeRTOS, sans champ de lancement ; champ
  `rtos` de Cortex-Debug non écrit (embOS non pris en charge par OpenOCD 0.12.0).
- P-4 : pas de SVD pour QEMU.
- P-5 : SVD pour les 5 BSP de carte (F429, F439, F746, WL55 M4, SAMD21) ; essai sur les cartes
  disponibles, F439 sans carte (décision du 2026-10-31).

### 1.8 PA-39 (2026-11-02, décision de l'utilisateur)

P-1 à P-5 retenues ; cartes de l'essai : NUCLEO-F429ZI, NUCLEO-WL55JC1, STM32F746G-DISCO,
SAMD21 Xplained Pro.

## 2. Implémentation

| Dépôt | Branche (depuis) | Commit | Contenu |
| --- | --- | --- | --- |
| lepton-tools | `devenv/env-26` (`main` 65da9d8) | 13633f5 | schéma : `svd` = chemin ou `{"famille": chemin}` ; `checks.check_family_files` ; `Context.svd_file` de `generate.py` ; exemple `greffon-bsp-nucleo-f429zi.json` (forme famille), invalides `bsp-svd-famille-remonte.json`, `bsp-svd-cle-inconnue.json` ; tests `test_svd_file_of_bsp_or_family`, `test_check_svd_bsp_ou_famille` ; `env-8-interface.md` §18 |
| `family-stm32f4xx` | `devenv/env-26` (`master` 2b21340) | 1f3f8bd | `svd/STM32F429.svd`, `svd/STM32F439.svd`, `LICENSE-Apache-2.0`, `README.md` (provenance, SHA-256) |
| `family-stm32f7xx` | `devenv/env-26` (`master` 34ccaf8) | 4893540 | `svd/STM32F746.svd`, licence, README |
| `family-stm32wlxx` | `devenv/env-26` (`master` 1eccc2f) | 714b725 | `svd/STM32WL5x_CM4.svd`, licence, README |
| `family-samd21` | `devenv/env-26` (`master` a389592) | 11e85ad | `svd/ATSAMD21J18A.svd`, licence, README |
| `bsp-nucleo-f429zi` | `devenv/env-26` (`master` 8ea7ee5) | cd9862c | `"svd": {"famille": "svd/STM32F429.svd"}` |
| `bsp-nucleo-f439zi` | `devenv/env-26` (`master` f866283) | 34a0291 | `svd/STM32F439.svd` |
| `bsp-stm32f746g-disco` | `devenv/env-26` (`master` 9f81c1b) | 88456c7 | `svd/STM32F746.svd` |
| `bsp-nucleo-wl55jc1` | `devenv/env-26` (`master` a329f4d) | 92612b0 | `svd/STM32WL5x_CM4.svd` |
| `bsp-samd21-xplained-pro` | `devenv/env-26` (`master` 46337d1) | c267463 | `svd/ATSAMD21J18A.svd` |

Fichiers SVD copiés sans modification (empreintes du §1.2, relevées dans les README).
`LICENSE-Apache-2.0` : texte du pack F4 (identique, SHA-256 `c71d239d…`, à ceux des packs F7 et
WL ; le pack SAMD21 ne joint qu'une notice de 569 o). Graine `original-tree` et clone noyau non
touchés. Champ `rtos` non écrit (P-3).

`pytest` : 222 verts (218 + 2 tests + 2 exemples invalides). `check-jsonschema` : 5 manifestes BSP
et 4 manifestes famille conformes au schéma modifié. lepton réinstallé par `pipx install --force`
depuis 13633f5.

## 3. Contrôles

### 3.1 Greffe

- Copie d'essai `~/lepton-tools-dev/essais/env-26-copie` (`cp -RP` hors `build/`, `third_party/`),
  `scion graft` : 13 feuilles ajoutées (les fichiers `svd/` des 4 familles), rien d'autre ; chemins
  ignorés : 11 `.DS_Store` (inchangé) ; `lepton check` code 0 (19 fichiers).
- `<ROOTSTOCK>` : même résultat (13 feuilles ajoutées, aucun fichier régulier, aucun lien cassé,
  clone noyau propre) ; `lepton check` code 0, 19 fichier(s) conforme(s) ; `lepton generate`
  code 0 : `svdFile` présent et existant dans les 10 lancements de carte, absent des 6 lancements
  QEMU ; aucun champ `rtos`.

### 3.2 Oracle partiel (presets de carte)

Avant : clones famille et BSP repassés sur `master` (état de départ, trunk sans `svd`), puis
`scripts/oracle/rejouer-oracle.sh <ROOTSTOCK> rapports/oracles/env-26-avant --carte …` (10 presets,
`host` d'abord) ; après : clones sur `devenv/env-26`, regreffe, mêmes commandes vers
`rapports/oracles/env-26-apres`. Tout a réussi.

| Preset | Sections/symboles | Empreinte | Fumée | Banc KAL | Écarts expliqués |
| --- | --- | --- | --- | --- | --- |
| nucleo-f429zi-embos / -freertos | identiques | différente | — (carte) | — | E-1 |
| nucleo-f439zi-embos / -freertos | identiques | différente | — | — | E-1 |
| stm32f746g-disco-embos / -freertos | identiques | différente | — | — | E-1 |
| nucleo-wl55jc1-embos / -freertos | identiques | différente | — | — | E-1 |
| samd21-xplained-pro-embos / -freertos | identiques | différente | — | — | E-1 |
| host (mklepton) | — | `mklepton-empreintes.sha256` identiques | — | ctest | — |

- **E-1** (connu, `env-19-extraction.md` E-1) : `__TIME__` dans l'image. Vérifié : reconstruction à
  neuf de `nucleo-f429zi-embos` sans modification → 3 octets différents, tous dans la chaîne
  `14:42:52` / `14:44:35` (`.rodata`, à côté de `Nov  2 2026`).
