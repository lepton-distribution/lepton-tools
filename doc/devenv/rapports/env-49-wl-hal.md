# ENV-49 — Famille STM32WL : montée de version du code tiers

Session du 2026-11-10, Mac. Branche lepton-tools `devenv/env-49` (depuis `main` facb32d). Fichiers
joints : `env-49-wl-hal/` (`audit/` : scripts, relevés, essai ; `propose/` : porteur et reports).

## 1. Audit (lecture seule)

### 1.1 État de départ
- Dépôts aux commits de `handoff/env-48.md`, propres :
  - lepton-tools `main` facb32d ;
  - `family-stm32wlxx` `master` dfaf331 ;
  - BSP `nucleo-wl55jc1` 4d7cf80 ;
  - clone noyau 76f28bd ;
  - graine 15740f9 ;
  - F4 acdd24c, F7 12280a5 ;
  - seed.scions 7e8a0cc.
- Outils : scion 0.6.2.0, lepton 0.1.0, arm-none-eabi-gcc 14.2.1.
- Porteur `family-stm32wlxx/master/scion/.scion/` : 5 clés, 34 lignes de projection, 220 fichiers
  projetés.

  | Clé | Version | Fichiers projetés |
  | --- | --- | --- |
  | `stm32wlxx-hal-driver` | `v1.3.0` | 156 |
  | `cmsis-device-wl` | `v1.1.1` | 6 |
  | `stm32-mw-subghz-phy` | `v1.3.0` | 19 |
  | `stm32cubewl::utilities` | `v1.3.0` | 38 |
  | `stm32cubewl::radio-core-inc` | `v1.3.0` | 1 |

- Tags amont relevés par `git ls-remote` le 2026-11-10 ; les 4 miroirs ont **les mêmes tags**.
  Aucun `mirror-sync` n'est nécessaire avant le `seed-clone`.

  | Dépôt | Tags | Remarque |
  | --- | --- | --- |
  | HAL | `v1.0.0` à `v1.6.0` | dont `v1.3.1` |
  | CMSIS device | `v1.0.0` à `v1.4.0` | |
  | SubGHz_Phy | `v1.0.0` à `v1.5.0` | tous posés le 2026-04-15, sauf `v1.5.0` |
  | STM32CubeWL | `v1.0.0` à `v1.6.0` | dont `v1.3.1` |

- Clones de lecture `~/lepton-tools-dev/tiers/` : HAL `v1.6.0`, CMSIS `v1.4.0`, SubGHz `v1.5.0`,
  STM32CubeWL `v1.6.0`.
  - Écart sans conséquence : l'index du clone partiel STM32CubeWL ne correspond à aucun tag (429
    fichiers, état laissé par ENV-37).
  - L'audit lit par `git show` et `git ls-tree`, sans passer par l'index. Le clone n'a pas été
    touché.
- Cartes : les deux STLINK-V3 sont branchées.
  - A 002700253431510837393937 et B 004F003E3431510937393937 ;
  - ports présents : `/dev/cu.usbmodem1454303` et `/dev/cu.usbmodem145103` ;
  - l'association port → numéro sera relevée par `ioreg` avant chaque banc.

### 1.2 Couples de STM32CubeWL, de `v1.3.0` à `v1.6.0`
Relevé : `env-49-wl-hal/audit/couples.txt`, produit par `couples.sh` et `cmptree.py`, qui compare
les blobs git. Notation :
- sm : sous-module, décrit par le tag de son dépôt séparé ;
- arbre : contenu dans l'arbre de STM32CubeWL, comparé ensuite au tag le plus proche.

| STM32CubeWL | Date | HAL | CMSIS device | SubGHz_Phy |
| --- | --- | --- | --- | --- |
| `v1.3.0` 378e461 | 2022-12-08 | arbre = `v1.3.0`, sauf `stm32_hal_legacy.h` | arbre = `v1.2.0`, sauf `README.md` | arbre = `v1.3.0`, sauf `LICENSE.md` |
| `v1.3.1` 9d77b66 | 2025-01-30 | sm `v1.3.1` | sm f005e57 = `v1.2.0` + `SECURITY.md` (sans tag) | arbre = V1.3.1 des notes de version, **sans tag** (3 sources ≠ `v1.3.0`) |
| `v1.4.0` cbbd003 | 2025-11-19 | sm `v1.4.0` | sm `v1.3.0` | arbre = idem `v1.3.1` (sans tag) |
| `v1.5.0` d28c690 | 2026-03-25 | sm `v1.5.0` | sm `v1.4.0` | arbre = `v1.4.0`, sauf `LICENSE.md` |
| **`v1.6.0`** f934cd2 | 2026-07-01 | **sm `v1.6.0`** 5c87cf0 | **sm `v1.4.0`** 71a0b78 | **sm `v1.5.0`** 7dc059f |

Constats :
- **`v1.6.0` est la seule version dont les trois composants sont exactement des tags** de leurs
  dépôts séparés. Pour toutes les autres versions, au moins un composant n'est égal à aucun tag.
- Le couple actuel n'appartient à aucune version de STM32CubeWL : HAL `v1.3.0` avec CMSIS
  `v1.1.1`. C'est le constat B2.
- Les utilitaires et les fichiers d'application (`Projects/…/SubGHz_Phy_PingPong/Core/Inc/`)
  restent dans l'arbre de STM32CubeWL, à toutes les versions.
- Extraction de STM32CubeWL `v1.6.0` : **156 Mo**, contre 358 Mo en `v1.3.0` (les composants
  sont devenus des sous-modules, que scion ne clone pas). D11 s'en trouve atténué.

### 1.3 Ensembles projetés : liste des fichiers, de l'ancienne version à la candidate
Simulation des motifs (`proj.py`, règles P-M et P-T de `projection-miroir.md`), sur la liste git du
commit épinglé. Résultats dans `audit/simulation/`. La simulation des motifs actuels donne 220
fichiers, comme le `seed status` d'ENV-48.

| Ensemble | Noms de fichiers (ancienne → candidate) | Contenu |
| --- | --- | --- |
| HAL `v1.3.0` → `v1.6.0` | mêmes 156 noms | 135 fichiers changent (6311+/4702−, beaucoup de MISRA et de `const`) |
| CMSIS `v1.1.1` → `v1.4.0` | mêmes 6 noms | `stm32wl55xx.h`, `stm32wlxx.h`, `system_stm32wlxx.c` |
| SubGHz `v1.3.0` → `v1.5.0` | **restructuré en `v1.4.0`** : `stm32_radio_driver/` devient `radio_driver/` ; les 4 en-têtes de la racine (`radio.h`, `radio_def.h`, `radio_ex.h`, `lr_fhss_v1_base_types.h`) passent dans `radio_driver/` ; ajouts `lorawan/` (108 fichiers, pile LBM) et `Conf/radio_template.h` | `radio.c` (2 corrections), `radio_driver.c` |
| utilitaires `v1.3.0` → `v1.6.0` | mêmes 38 noms | `stm32_seq.c/h`, `stm32_timer.c/h` |
| `utilities_def.h` | même fichier | identique (même blob) |

Avec les motifs actuels, `v1.6.0` laisse 2 motifs SubGHz sans correspondance (`*.h` et
`stm32_radio_driver/*`), et 13 fichiers disparaissent. **Les lignes SubGHz du porteur doivent
changer** (§1.8, Q2).

Lignes proposées (`propose/porteur/.scion.projections`, 41 lignes) :
- 6 lignes SubGHz remplacées par 14. Les 4 en-têtes de la racine sont nommés un à un vers
  `radio_subghz_phy/`. `radio_driver/*.c` et 5 en-têtes nommés vont vers
  `radio_subghz_phy/stm32_radio_driver/`. Viennent ensuite `LICENSE`, `LICENSE.md`, `Conf/*` et
  l'exclusion `!radio_driver/radio.c`.
- Les **chemins du trunk sont inchangés**, ainsi que les `sources` et `inclusions` du manifeste.
  Seul s'ajoute `Conf/radio_template.h`, un gabarit amont ni compilé ni inclus (`Conf/` n'est pas
  un répertoire d'inclusion).
- Une exclusion porte sur toutes les inclusions de la clé (P-X1). Les en-têtes sont donc nommés un
  à un, et non exclus d'un `radio_driver/*`.
- HAL : la ligne `!Inc/Legacy/stm32_hal_legacy.h` est retirée (§1.4).

Simulation des lignes proposées : 157 + 6 + 20 + 38 + 1 = **222 fichiers projetés**.

### 1.4 Fichiers gardés par la famille et report des modifications Lepton
Correctifs Lepton et script de report : `propose/reports/` (`lepton-*.patch`, `reporter.sh`). Le
résultat est reproductible depuis les clones de lecture, et aucune copie de code ST n'est versionnée.

| Fichier | Modification Lepton (contre l'origine) | Amont, de l'ancienne à la nouvelle version | Report |
| --- | --- | --- | --- |
| `radio.c` | corps de `RadioIsChannelFree` sous `#if 0`, `return false` (3 lignes ; C1) | SubGHz `v1.3.0` → `v1.5.0` : 2 corrections, loin de la fonction. `SUBGRF_WriteRegister(SUBGHZ_AGCCFG,0x20)` en FSK dans `RadioSetRxConfig` ; `lora.MaxPayloadLength` au lieu de `fsk.` dans `RadioSetRxGenericConfig` | `patch` sans conflit ; le `#if 0` est gardé aux mêmes lignes 810 et 844-846 |
| `stm32_timer.h` | `cmsis_compiler.h` mis en commentaire (`// lepton removed`) | STM32CubeWL `v1.3.0` → `v1.6.0` : déclaration de `UTIL_TIMER_GetTimerList` ajoutée, coquille corrigée | `patch` sans conflit |
| `subghz.h`, `utilities_conf.h`, `platform.h` | ENV-37 (voir la provenance) | fichiers PingPong d'origine **identiques** de `v1.3.0` à `v1.6.0` (mêmes blobs) | **rien à reporter** ; fichiers inchangés |
| `stm32_hal_legacy.h` | aucune : c'est le fichier de STM32CubeWL `v1.3.0` (blob 241b54e), différent de celui de la HAL `v1.3.0` (71534e7) | en HAL `v1.6.0`, `stm32wlxx_hal_def.h` **n'inclut plus** ce fichier (ligne 30 en commentaire) | proposé : retirer la copie de la famille et projeter celui de la HAL `v1.6.0`, au même chemin. L'exception « autre révision » d'ENV-38 §5 tombe (Q3) |

Aucun fichier de Lepton n'inclut `stm32_hal_legacy.h` (recherche dans la famille, le BSP et le
noyau). Les deux presets compilent sans lui (§1.6).

### 1.5 API et comportement : couche Lepton et BSP
- **Compilation** : aucune modification de la couche Lepton ni du BSP n'est nécessaire. Les
  presets compilent, et l'édition de liens réussit.
- **Avertissements** : comptes identiques (embOS 134, FreeRTOS 42), et mêmes couples fichier et
  message que la référence.
- **Liens**, constat de l'édition de liens :
  - les fonctions SUBGHZ devenues `static` dans la HAL (`SUBGHZ_WaitOnBusy`,
    `SUBGHZ_CheckDeviceReady`, `SUBGHZSPI_*`) ne sont appelées ni par Lepton ni par le BSP ;
  - les nouvelles fonctions publiques `HAL_SUBGHZ_WaitOnBusy` et `HAL_SUBGHZ_CheckDeviceReady`
    ne sont pas liées.
- **Gabarit de configuration** : `stm32wlxx_hal_conf_template.h` est identique de `v1.3.0` à
  `v1.6.0`. Le `stm32wlxx_hal_conf.h` de Lepton n'a donc rien à reprendre.
- **CMSIS device** : aucun changement d'IRQ ni d'adresse pour le WL55 M4. Les renommages
  (`SVC_IRQn` → `SVCall_IRQn`, ADC `TRx` → `AWDxTR`) ont des alias de compatibilité. Les autres
  changements sont `STM32WL5Mxx` (nouveau) et `VECT_TAB_OFFSET` redéfinissable.
- **Changements de comportement dans le code compilé**, d'après les notes de version et les
  diffs ; tous seront éprouvés par le banc radio, lancé deux fois :
  - HAL SUBGHZ :
    - l'attente BUSY est réécrite d'après le code de référence Semtech (V1.6.0) : la boucle
      d'attente fixe `SUBGHZ_NSS_LOOP_TIME` de `SUBGHZ_CheckDeviceReady` disparaît ;
    - l'état `HAL_SUBGHZ_STATE_BUSY` est posé dans les accès ;
    - le statut CRC est remonté (`HAL_SUBGHZ_ERROR_CRC_MISMATCH`, V1.4.0).
  - HAL UART :
    - `UART_WaitOnFlagUntilTimeout` est réécrite pour ne plus rester bloquée sur une erreur de
      débordement (V1.4.0) ;
    - le compte de transfert DMA est corrigé (V1.5.0).
  - `radio_driver.c` :
    - sections critiques ajoutées autour des accès registre (`SUBGRF_ReadRegister`,
      `SUBGRF_WriteRegister`) ;
    - taille de commande corrigée dans `SUBGRF_ClearDeviceErrors`.
  - Hors du code compilé :
    - V1.4.0 corrige aussi l'ordre d'initialisation de la base de temps par TIM, mais seulement
      dans `timebase_tim_template.c` ; ce gabarit n'est pas compilé, et le tick de Lepton est
      `dev_stm32wlxx_hal_tick.c`, en remplaçant fort ;
    - le séquenceur et `stm32_timer.c` changent, mais ne sont pas compilés.

### 1.6 Essai sur une copie d'essai
Copie : `~/lepton-tools-dev/essais/env-49-copie`, faite par `rsync -a` de `<ROOTSTOCK>`, sans
`build/` ni `third_party/` (3888 liens, 0 cassé).

Dans le clone famille de la copie, branche `essai/env-49`, commit c3e6466 :
- les 3 fichiers du porteur de `propose/porteur/` ;
- `git rm` de `stm32_hal_legacy.h` ;
- `radio.c` et `stm32_timer.h` reportés.

Journaux : `audit/copie/`.

| Contrôle | Résultat |
| --- | --- |
| `scion seed-clone --seed depots/lepton-seed.scions/original-tree` | code 0, 18 s. 4 clones neufs, partiels `blob:none`, `origin` = miroirs : `stm32wlxx-hal-driver/v1.6.0` 5c87cf0, `cmsis-device-wl/v1.4.0` 71a0b78, `stm32-mw-subghz-phy/v1.5.0` 7dc059f, `stm32cubewl/v1.6.0` f934cd2 (156 Mo). Les clones `v1.3.0` et `v1.1.1` restent (P-V5) |
| `scion graft -v` | code 0 ; 3889 feuilles |
| trunk | 3889 liens, 0 cassé, 0 fichier régulier |
| liste des chemins, contre `<ROOTSTOCK>` (`liens.py`) | identique, **plus 1** : `radio_subghz_phy/Conf/radio_template.h` |
| cibles | **222 réorientées** : HAL 157, CMSIS 6, SubGHz 20, STM32CubeWL 39. Ce sont les 220 projetées, `stm32_hal_legacy.h` (famille → HAL `v1.6.0`) et le nouveau chemin. 0 cible vers les anciens clones |
| `lepton check` | code 0 (19 fichiers conformes) |
| `lepton seed status` | clés WL `v1.6.0` 157, `v1.4.0` 6, `v1.5.0` 20, `v1.6.0` 38 (et 1), « projeté par stm32wlxx » |
| `lepton generate` | code 0 ; espace de travail identique, aux chemins du rootstock près |
| construction : `host`, `nucleo-wl55jc1-embos`, `nucleo-wl55jc1-freertos` | code 0 ×3 ; avertissements identiques à la référence |

Binaires (`capturer-oracle.sh` sur l'ELF, `comparer-oracle.py` contre `oracles/env-48-apres/`) :
- `.data`, `.bss` et `.isr_vector` sont identiques ; les sections `.debug_*` changent.
- **26 symboles diffèrent, les mêmes sur les deux presets** (`audit/copie/oracle/*.cmp`). La
  somme des écarts de taille vaut **+36 octets**.
- **Symboles qui changent**, par origine :
  - HAL SUBGHZ :
    - retirés : `SUBGHZSPI_Init`, `SUBGHZSPI_Receive`, `SUBGHZSPI_Transmit` ;
    - ajoutés : `SUBGHZSPI_Receive.isra.0` et `SUBGHZSPI_Transmit.isra.0` (fonctions devenues
      `static`) ;
    - `SUBGHZ_CheckDeviceReady` (0x38 → 0x1e) et `SUBGHZ_WaitOnBusy` (0x44 → 0x3c) passent de
      `T` à `t` ;
    - 8 `HAL_SUBGHZ_*` modifiés ; au total, −48 octets.
  - HAL UART : `HAL_UART_IRQHandler`, `UART_CheckIdleState`, `UART_DMAAbortOnError`,
    `UART_DMAError`, `UART_DMAReceiveCplt`, `UART_DMARxHalfCplt`,
    `UART_WaitOnFlagUntilTimeout` ; +60 octets.
  - `radio.c` : `RadioSetRxConfig` +4 et `RadioSetRxGenericConfig` +4.
  - `radio_driver.c` : `SUBGRF_ReadRegister` +8 et `SUBGRF_WriteRegister` +8.
- **`.text`** (répartition par objet dans `lepton.map`, `audit/copie/oracle/map-objets.txt`) :
  - embOS : **+48** = +36 de symboles et +12 octets : +10 de bourrage, et +2 hors des symboles
    dimensionnés de l'objet `stm32wlxx_hal_uart.c` (+62 dans la carte, +60 de symboles) ;
  - FreeRTOS : +200 sur la copie. Il comprend **+150 qui ne viennent que de la copie** : les
    `configASSERT` de FreeRTOS incluent `__FILE__`, et le chemin absolu du trunk de la copie
    (`…/essais/env-49-copie/trunk/…`) a 30 caractères de plus. Cela fait 5 fichiers × 30,
    vérifié par `strings` sur l'image. **Écart attendu sur `<ROOTSTOCK>` : environ +50**, soit
    les mêmes 38 octets d'objets et environ +12 de bourrage.

### 1.7 Effets sur scion, lepton, l'éditeur, les miroirs et les autres rootstocks
- **scion** : aucun défaut, aucune modification. Les motifs proposés passent sous 0.6.2.0.
- **lepton** : aucune modification. `check`, `seed status` et `generate` sont conformes sur la
  copie.
- **Éditeur** : l'extension 0.5.2 calcule la table « clone tiers → trunk » d'après scion. Le
  chemin des clones change (`…/v1.6.0`), mais il n'y a rien à régénérer à la main.
- **Miroirs** : les tags visés y sont déjà ; aucun envoi.
- **Anciens clones** de `<ROOTSTOCK>` (P-V5, `graft-remove --purge` ne les touche pas) :
  - ils restent après la bascule : `stm32wlxx-hal-driver/v1.3.0` (8,4 Mo), `cmsis-device-wl/v1.1.1`
    (4,9 Mo), `stm32-mw-subghz-phy/v1.3.0` (0,7 Mo), `stm32cubewl/v1.3.0` (358 Mo) ;
  - le hook refuse toute écriture sous `depots/tiers/` : leur suppression revient à l'utilisateur
    (Q4).
- **Rootstocks d'essai** : ceux du Mac (`env-13-vierge`, `env-41-vierge`, `env-11/wl55jc1`) et de
  la VM ne sont pas regreffés avant ENV-50.
  - Leur famille WL est encore en 2340b25, l'état d'avant ENV-48.
  - Le `graft-update` d'ENV-50 passera directement à l'état d'ENV-49 : il créera les clones
    `v1.6.0`, et non plus les `v1.3.0`.

### 1.8 Propositions pour le PA-85
Q1. **Versions cibles et périmètre**. Couple de STM32CubeWL `v1.6.0`, périmètre complet :
- HAL `v1.6.0` (5c87cf0) ;
- CMSIS device `v1.4.0` (71a0b78) ;
- SubGHz_Phy `v1.5.0` (7dc059f) ;
- utilitaires et `utilities_def.h` de STM32CubeWL `v1.6.0` (f934cd2).

C'est le seul couple dont chaque composant est un tag. Une montée de la HAL seule garderait un
couple incohérent, ce qui est contraire à B2.

Q2. **Lignes SubGHz** :
- (A, proposé) chemins du trunk conservés, 14 lignes du §1.3, et `Conf/radio_template.h` projeté
  (+1 chemin, accordé) ;
- (A′) comme A, avec `!Conf/radio_template.h` : liste des chemins identique ;
- (B) suivre l'amont, `radio_subghz_phy/radio_driver/`. Il faudrait changer les `sources`, les
  `inclusions`, le chemin de `radio.c` dans la famille et 14 chemins du trunk (13 projetés, plus
  `radio.c`).

Q3. **`stm32_hal_legacy.h`** :
- (proposé) copie de la famille retirée (`git rm`, lot mécanique), fichier de la HAL `v1.6.0`
  projeté au même chemin ; exception d'ENV-38 §5 close ;
- autres choix : exclure le fichier (absent du trunk), ou garder la copie de STM32CubeWL `v1.3.0`.

Q4. **Reste du PA-85** :
- **reports** du §1.4 : `radio.c` (le `#if 0` est gardé), `stm32_timer.h` ; les 3 fichiers de
  `stm32_radio_core_inc` restent inchangés ;
- **couche Lepton et BSP** : aucune modification (lot 3 vide, BSP non touché) ;
- **critère d'écart des presets WL55 sur `<ROOTSTOCK>`** :
  - `.data`, `.bss` et `.isr_vector` identiques ;
  - les 26 symboles du §1.6 changent exactement comme sur la copie (noms, types, tailles) ;
  - `.text` = référence + 36 + bourrage, avec moins de 16 octets de bourrage (attendu : +48 en
    embOS, environ +50 en FreeRTOS) ;
  - les sections `.debug_*` sont libres ;
  - tout autre écart bloque, ou est expliqué au rapport ;
  - **code 0** exigé pour host et les 14 autres presets ;
- **cartes (PA-11)** : écriture flash sur les deux NUCLEO-WL55JC1, A et B :
  - banc de référence avant (embOS et FreeRTOS, deux fois chacun) ;
  - banc après (idem) ;
  - les ports sont relevés par `ioreg` ;
- **manifeste** : `description` réécrite (HAL ST V1.6.0, CMSIS device ST V1.4.0, SubGHz_Phy
  V1.5.0, utilitaires de STM32CubeWL V1.6.0, couple de STM32CubeWL v1.6.0) ;
  `stm32_hal_legacy.h` retiré de la liste des fichiers restés dans le greffon ; `sources` et
  `compilation` inchangés ;
- **provenances** : les 4 `LEPTON-PROVENANCE.md` sont mis à jour (versions, commits, couple,
  nouvelles lignes SubGHz, reports, `stm32_hal_legacy.h` projeté) ;
- **anciens clones** : leur suppression par l'utilisateur, après le PA-86, avec la commande exacte
  fournie ; ou leur conservation jusqu'à ENV-50.

### 1.9 Décisions du PA-85 (2026-11-10, utilisateur)
- Q1 : couple de STM32CubeWL `v1.6.0`, périmètre complet.
- Q2 : lignes « A », chemins du trunk conservés ; `Conf/radio_template.h` projeté (+1 accordé).
- Q3 : `stm32_hal_legacy.h` de la HAL `v1.6.0` projeté ; la copie de la famille est retirée.
- Q4 : propositions du §1.8 acceptées :
  - reports ;
  - couche Lepton et BSP non modifiés ;
  - critère d'écart ;
  - PA-11 sur les deux WL55 ;
  - description et provenances ;
  - anciens clones supprimés par l'utilisateur après le PA-86.

## 2. Oracle avant
`rapports/oracles/env-49-avant/` : `env-46-spl/oracle-complet.sh <ROOTSTOCK>`, repris sans
changement. Il fait la liste du trunk, 6 presets QEMU (fumée et KAL), 10 presets de carte, host,
des constructions à neuf (2 min 40), puis `ctest -N`. Résultat : « tout a réussi ».

La comparaison à `oracles/env-48-apres/` se fait par `env-46-spl/comparer.sh` (journal
`env-49-wl-hal/oracle-avant.out`) :

| Preset | Sections/symboles | Fumée | Banc KAL |
| --- | --- | --- | --- |
| host | mklepton identiques ; ctest 7/7 | — | — |
| 6 QEMU (an386 ×4, an500 ×2) | code 0 ×6 | identique | identique (19, 15, 19, 15, 18, 18) |
| 10 de carte (F429, F439, WL55, F746, SAMD21 ; embOS et FreeRTOS) | code 0 ×10 | — | — |

- `ctest -N` : 17/17 identiques.
- Trunk : 3888 chemins, `sha256.txt` identique à `env-48-apres`, 0 anomalie.

### 2.1 Banc de référence de la paire NUCLEO-WL55JC1 (PA-11)
Le script `env-49-wl-hal/bancs.sh` lance `banc-wl55.sh` d'ENV-42 : deux passes par preset, contre
l'oracle `env-49-avant`. Journaux : `env-49-wl-hal/bancs/avant-<n>/<preset>/` ; bilan :
`env-49-wl-hal/bancs-avant.out` (7 min 26).

Ports relevés par `ioreg` le 2026-11-10, identiques à ENV-48 :
- A 002700253431510837393937 : `/dev/cu.usbmodem1454303` ;
- B 004F003E3431510937393937 : `/dev/cu.usbmodem145103`.

| Preset | Passe | `lepton.elf` contre l'oracle | `ctest -L board` | Radio |
| --- | --- | --- | --- | --- |
| `nucleo-wl55jc1-embos` | 1, 2 | 0 écart ×2 | 16/16 ×2 | tx 20/20 et rx 20/20 dans les deux sens, ping-pong 20/20, 2 jetons reçus (×2) |
| `nucleo-wl55jc1-freertos` | 1, 2 | 0 écart ×2 | 16/16 ×2 | idem (×2) |

Le résultat est identique à la référence d'ENV-48.

## 3. Montée de version

### 3.1 Famille (`family-stm32wlxx`, branche `devenv/env-49`) sur la copie d'essai
Branche `devenv/env-49` créée depuis `master` dfaf331, dans le clone famille de
`essais/env-49-copie`. La branche d'essai `essai/env-49` du §1.6 est gardée pour comparaison.

| Commit | Lot | Contenu |
| --- | --- | --- |
| c85859b | 1 | `scion/.scion/` : sources et ramifications (`v1.6.0`, `v1.4.0`, `v1.5.0`, `v1.6.0` ×2), 41 lignes de projection (`propose/porteur/`) ; les miroirs sont inchangés et déjà à jour (§1.1) |
| b86aaf3 | mécanique | `git rm` de `stm32_hal_legacy.h` (Q3) |
| 9377ad1 | 2 | `radio.c` et `stm32_timer.h` reportés (`propose/reports/reporter.sh`) |
| — | 3 | couche Lepton et BSP : aucune modification (Q4) |
| bfbeb1b | 4 | 4 `LEPTON-PROVENANCE.md` ; `description` du manifeste (seul champ changé) |

Contrôles sur la copie, regreffée par `scion graft` (code 0, 3889 feuilles) :
- liste `chemin -> cible` identique à l'essai du §1.6 (`audit/copie/liens-copie.txt`) ;
- 0 lien cassé, 0 fichier régulier ;
- `lepton check` code 0 ;
- `nucleo-wl55jc1-embos` et `-freertos` reconstruits à neuf : 0 écart de sections et de symboles
  contre les captures du §1.6, mêmes avertissements.
