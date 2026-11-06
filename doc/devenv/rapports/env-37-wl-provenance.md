# ENV-37 — Famille STM32WL : audit et provenance du code tiers

Session du 2026-11-06, hôte Mac. Clone de la famille `depots/lepton/family-stm32wlxx/master`
(`master` dbc58d7) **lu seulement** pendant l'audit. Listes et diffs :
`rapports/env-37-wl-provenance/`.

## 1. Audit (lecture seule) — état au PA-61

### 1.1 Méthode
- Clones amont dans `~/lepton-tools-dev/tiers/` (hors rootstock) : `stm32wlxx-hal-driver`,
  `cmsis-device-wl`, `stm32-mw-subghz-phy`, `stm32-util-sequencer`, `stm32-util-advanced-trace`
  (complets) ; `STM32CubeWL` (partiel, `--filter=blob:none`, objets rapatriés à la demande).
- Copies de travail remises aux chemins amont : `~/lepton-tools-dev/essais/env-37-compare/`, par
  `rapports/env-37-wl-provenance/preparer-copies.sh <src de la famille> <destination>` (copie
  sans `.DS_Store` ; `inc` → `Inc`, `src` → `Src` ; CMSIS device réparti en `Include/`,
  `Source/Templates/`, `Source/Templates/iar/`). Pile radio comparée sans copie (chemins identiques
  au dépôt `stm32-mw-subghz-phy`).
- Comparaison : `scripts/tiers/verifier-import.sh` (ENV-34), **inchangé**, contre chaque tag
  candidat ; classement de la meilleure révision enregistré (`classement-*.txt`). Fichiers amont
  absents de la copie : `absents-*.txt`. Fichiers `TROP` recherchés par empreinte git
  (`git hash-object`) dans les tags `v1.0.0` à `v1.3.0` de STM32CubeWL.
- Casse : le volume du Mac est **APFS insensible à la casse** (`diskutil info /` : personnalité
  « APFS ») ; la VM Debian la distingue. La recherche `git show <rév>:<chemin>` du script est
  sensible à la casse : chaque `OK` prouve aussi la casse exacte du nom sous la racine remise aux
  chemins amont. Seules différences de casse : les répertoires renommés listés au §3.
- Compilé et inclus : `compile_commands.json` et `ninja -t deps` (en-têtes réellement lus,
  équivalent de `gcc -H`) des presets `nucleo-wl55jc1-embos` et `nucleo-wl55jc1-freertos`
  (répertoires de construction du 2026-11-05, trunk inchangé depuis). Les deux presets donnent
  les mêmes listes (`compiles-*.txt`, `inclus-*.txt`).

### 1.2 Révisions amont (tags résolus en commits, `^{commit}`)
| Dépôt | Tags utiles → commit |
| --- | --- |
| `STMicroelectronics/STM32CubeWL` | `v1.2.0` 6d27fec2e59e2032d3d6cd55909b0bc73bae9356 (2022-12-07) ; `v1.3.0` 378e461e469ef9826e857f8eda3346cea525b2fa (2022-12-08) ; `v1.3.1` 9d77b66f25362a849ef48fd2369060e3718fc99d |
| `STMicroelectronics/stm32wlxx-hal-driver` | `v1.3.0` e3966ab429c1711e5dd2b40918e1d987eed7a249 ; `v1.3.1` 8188d40505f5f77cb6ff9cea404b661d445acbd2 |
| `STMicroelectronics/cmsis-device-wl` | `v1.1.1` d248c5514fe294fec6eb52f49ed3f1a53cea45b0 ; `v1.2.0` baa994d7bd83d7984675d6fce847cb7538118bf0 |
| `STMicroelectronics/stm32-mw-subghz-phy` | `v1.3.0` 1cad76816effd9679a056e57c02dd4b23d7cb772 (tags `v1.0.0` à `v1.4.0` créés le 2026-04-15) |
| `STMicroelectronics/stm32-util-sequencer`, `stm32-util-advanced-trace` | `2.0.0` à `2.1.2` seulement (2026) |

Sous-modules de STM32CubeWL : jusqu'à `v1.3.0`, HAL et CMSIS device sont des **arbres** du dépôt ;
à partir de `v1.3.1`, des sous-modules (`stm32wlxx_hal_driver` 8188d40 = `v1.3.1`,
`cmsis_device_wl` f005e57, commit sans tag entre `v1.2.0` et `v1.3.0`). Versions portées :
STM32CubeWL `v1.2.0` = HAL 1.2.0 + CMSIS device 1.1.1 + SubGHz_Phy 1.2.0 ; `v1.3.0` = HAL 1.3.0 +
CMSIS device 1.2.0 + SubGHz_Phy 1.3.0.

### 1.3 Classement par ensemble (225 fichiers)
Chemins relatifs à `sys/root/src/kernel/` de la famille.

| Ensemble | Fichiers | Meilleure révision | OK | DIFF | TROP | Absents de la copie (amont) |
| --- | --- | --- | --- | --- | --- | --- |
| HAL `dev/arch/cortexm/stm32wlxx/cubemx_hal_driver/` | 157 | STM32CubeWL `v1.3.0` `Drivers/STM32WLxx_HAL_Driver` | 156 | 0 | 1 | 4 : `LICENSE.md`, `_htmresc/` ×3 |
| idem | 157 | `stm32wlxx-hal-driver` `v1.3.0` | 155 | 1 | 1 | — |
| CMSIS device `core/ucore/cmsis/Device/st/stm32wlxx/` | 5 | `cmsis-device-wl` `v1.1.1` (= STM32CubeWL `v1.2.0`) | 5 | 0 | 0 | 71 : autres puces, démarrages `arm`/`gcc`, scripts d'édition de liens, `LICENSE.md`, `README.md`, notes de version |
| Pile radio `dev/arch/cortexm/stm32wlxx/radio_subghz_phy/` | 24 | `stm32-mw-subghz-phy` `v1.3.0` (= STM32CubeWL `v1.3.0` `Middlewares/Third_Party/SubGHz_Phy`) | 18 | 1 | 5 | `LICENSE.md`, `README.md`, `Release_Notes.*`, `SECURITY.md`, `_htmresc/`… |
| Utilitaires `dev/arch/cortexm/stm32wlxx/Utilities/` | 39 | STM32CubeWL `v1.3.0` `Utilities` (`v1.3.1` : même résultat) | 32 | 1 | 6 | 156 : `sequencer/html/` (122), `_htmresc/`, notes de version, `LICENSE.md` ×6, `PC_Software/*.zip` |

Total à la meilleure révision : 211 `OK`, 2 `DIFF`, 12 `TROP`, 0 `CR`, 0 `MANQUE` (aucune liste
attendue). Fins de ligne : 0 fichier CRLF dans les quatre ensembles.

### 1.4 Qualification des écarts (`diffs/`)
| Fichier | Classe | Qualification |
| --- | --- | --- |
| `cubemx_hal_driver/inc/Legacy/stm32_hal_legacy.h` | DIFF contre `stm32wlxx-hal-driver` `v1.3.0` seulement | **autre version** : la copie est celle de STM32CubeWL `v1.3.0` (`#if defined(STM32U5) \|\| defined(STM32MP2)`) ; le tag du dépôt séparé porte `#if defined(STM32U5)` (`diffs/stm32_hal_legacy.h.diff`) |
| `radio_subghz_phy/stm32_radio_driver/radio.c` | DIFF | **modification Lepton, non signalée** : corps de `RadioIsChannelFree` mis sous `#if 0`, la fonction rend toujours `false` (`diffs/radio.c.diff`). Fichier compilé. Absente de la liste des retouches de `doc/migration/MIGRATION-STATUS.md` (2026-10-05) et du `grep` du 2026-11-05 (aucune marque « lepton ») |
| `Utilities/timer/stm32_timer.h` | DIFF | modification Lepton : `#include <cmsis_compiler.h>` mis en commentaire (« lepton removed »), espaces de fin modifiés. Inclus |
| `radio_subghz_phy/stm32_radio_core_inc/utilities_def.h` | TROP | hors amont de la pile : identique à `Projects/NUCLEO-WL55JC/Applications/SubGHz_Phy/SubGHz_Phy_PingPong/Core/Inc/utilities_def.h` de STM32CubeWL `v1.3.0` (fichier d'application généré par STM32CubeMX). Inclus |
| `radio_subghz_phy/stm32_radio_core_inc/subghz.h` | TROP | même origine, **modifié par Lepton** : `main.h` remplacé par `stm32wlxx_hal.h` (`diffs/subghz.h.diff`). Inclus |
| `radio_subghz_phy/stm32_radio_core_inc/utilities_conf.h` | TROP | même origine, **modifié par Lepton** : `cmsis_compiler.h` retiré, branches `__CC_ARM`, `__ICCARM__`, `WIN32` supprimées (`diffs/utilities_conf.h.diff`). Inclus |
| `radio_subghz_phy/stm32_radio_core_inc/platform.h` | TROP | même origine, **modifié par Lepton** : `main.h` et deux en-têtes BSP ST mis en commentaire (`diffs/platform.h.diff`). **Ni compilé ni inclus** |
| `LICENSE.txt` ×8 (`cubemx_hal_driver/`, `radio_subghz_phy/`, `Utilities/{conf,misc,sequencer,timer,lpm/tiny_lpm,trace/adv_trace}/`) | TROP | 8 copies identiques (empreinte git 3edc4d1) de l'avis court ST « Package_license … BSD-3-Clause » ; absentes de tous les tags clonés (STM32CubeWL `v1.0.0`-`v1.3.0`, dépôts HAL et CMSIS WL, F4, F7) : **origine non établie**. L'amont porte à la place `LICENSE.md` (texte BSD-3 complet), absent de la copie |

Modifications Lepton : 5 fichiers (`radio.c`, `stm32_timer.h`, `subghz.h`, `utilities_conf.h`,
`platform.h`) ; les trois fichiers « à marque Lepton » du 2026-11-05 en font partie. La liste est
complète : chaque fichier des quatre ensembles est `OK` contre l'amont ou a son diff ci-dessus.

### 1.5 Compilé et inclus (presets `nucleo-wl55jc1-embos` et `-freertos`, identiques)
| Ensemble | Compilés | En-têtes lus | Jamais lus |
| --- | --- | --- | --- |
| HAL | 12 `.c` de `src/` (= `sources` du manifeste) | 26 de `inc/`, dont `Legacy/stm32_hal_legacy.h` | 60 `.c`, 56 `.h`, `README.md`, `LICENSE.txt`, `Release_Notes.html` |
| CMSIS device | aucun | `stm32wl55xx.h`, `stm32wlxx.h`, `system_stm32wlxx.h` | `system_stm32wlxx.c`, `startup/iar/startup_stm32wl55xx_cm4.s` (démarrage IAR) |
| Pile radio | 5 `.c` de `stm32_radio_driver/` (dont `radio.c` modifié) | `radio.h`, `radio_def.h`, `radio_ex.h`, `lr_fhss_v1_base_types.h`, 4 `.h` de `stm32_radio_driver/`, `subghz.h`, `utilities_conf.h`, `utilities_def.h` | `Conf/` (4 gabarits), `platform.h`, `subghz_phy_version.h`, `LICENSE`, `LICENSE.txt` |
| Utilitaires | `misc/stm32_mem.c` | `misc/stm32_mem.h`, `misc/stm32_tiny_vsnprintf.h`, `timer/stm32_timer.h`, `trace/adv_trace/stm32_adv_trace.h` | 34 autres fichiers |

### 1.6 Références hors des répertoires tiers
- Famille : `lepton-greffon.json` (21 `sources`, 9 inclusions publiques vers les quatre
  ensembles) ; `dev_stm32wlxx/dev_stm32wlxx_bsp_radio_if.c` inclut `radio_subghz_phy/radio.h`.
- BSP `nucleo-wl55jc1` : aucune référence par chemin.
- Clone noyau : documents figés de la migration (`doc/migration/MIGRATION-STATUS.md` l. 129, 142,
  145 ; `audit-iar.csv` ; `validation-nucleo-wl55jc1.md` l. 45). Aucun code.
- lepton-tools : `schemas/exemples/greffon-famille-stm32wlxx.json` (exemple de schéma) ; documents
  de `doc/devenv/` (rapports, oracles). Aucun code ni skill.

### 1.7 Licences
| Ensemble | Licence amont | Fichier dans la copie |
| --- | --- | --- |
| HAL | BSD-3-Clause ST (`LICENSE.md`) | `LICENSE.txt` (avis court, origine non établie) |
| CMSIS device | Apache-2.0 (`LICENSE.md` de `cmsis-device-wl`) ; en-têtes : « LICENSE file » | aucun |
| Pile radio | Clear BSD Semtech (`LICENSE`, copié, `OK`) pour les fichiers Semtech ; BSD-3 ST (`LICENSE.md`, absent) | `LICENSE`, `LICENSE.txt` |
| Utilitaires | BSD-3-Clause ST (`LICENSE.md` par sous-répertoire) | `LICENSE.txt` ×6 |

### 1.8 Constats pour le PA-61
1. **Couple incohérent** : la HAL est celle de STM32CubeWL `v1.3.0`, le CMSIS device celui de
   `v1.2.0` (1.1.1). La copie ne correspond donc à aucun tag unique de STM32CubeWL.
2. **HAL** : exacte contre STM32CubeWL `v1.3.0` ; contre le dépôt séparé `v1.3.0`, un fichier
   diffère (`stm32_hal_legacy.h`, version Cube). La décision du 2026-11-04 exclut STM32Cube entier
   comme source.
3. **Pile radio** : un dépôt séparé existe (`stm32-mw-subghz-phy`, contrairement à la passation),
   `v1.3.0` 1cad768, contenu identique à STM32CubeWL `v1.3.0` pour les 18 fichiers `OK`.
4. **Utilitaires** : seuls `sequencer` et `advanced-trace` ont un dépôt séparé, en versions 2.x
   réécrites (fichiers renommés : `sequencer.c` au lieu de `stm32_seq.c` ; 958 lignes de diff
   sur 550). STM32CubeWL est le seul amont des révisions copiées.
5. **`stm32_radio_core_inc/`** : fichiers d'application STM32CubeMX (exemple PingPong), pas de la
   pile ; 3 sur 4 modifiés par Lepton.
6. **`radio.c`** : modification fonctionnelle compilée et non documentée (`RadioIsChannelFree`
   rend toujours `false`).
7. Texte du manifeste « HAL ST STM32CubeWL V1.3.0 », « SubGHz_Phy 1.3.0 » : exact ; il ne donne
   pas la version du CMSIS device (1.1.1, STM32CubeWL V1.2.0).
8. `verifier-import.sh` a suffi tel quel (copies remises aux chemins amont) : aucune évolution
   proposée.

### 1.9 Décisions du PA-61 (utilisateur, 2026-11-06)
- Révisions citées : HAL `stm32wlxx-hal-driver` `v1.3.0` (écart `stm32_hal_legacy.h` consigné,
  identité à STM32CubeWL `v1.3.0` mentionnée) ; CMSIS device `cmsis-device-wl` `v1.1.1` ; pile
  radio `stm32-mw-subghz-phy` `v1.3.0` ; utilitaires et `stm32_radio_core_inc/` : STM32CubeWL
  `v1.3.0` admis, exception étroite à la décision du 2026-11-04.
- Fichiers modifiés par Lepton : option 1, laissés et décrits un par un (écart à D1a consigné).
- Fichiers `TROP` : tous laissés et listés, aucune suppression.
- Forme : un `LEPTON-PROVENANCE.md` par ensemble (4), un commit chacun.
- Texte `description` du manifeste : inchangé.

## 2. Oracle avant
`rapports/oracles/env-37-avant/` : `rejouer-oracle.sh <ROOTSTOCK> … --qemu` ×6 `--carte` ×10
(constructions à neuf, `rejouer-oracle.log`) : « tout a réussi ». Contre `env-35-apres`
(`env-37-avant/comparaisons/`) : `comparer-oracle.py` code 0 ×16 ; host 7/7 ; empreintes mklepton
identiques ; bancs KAL QEMU identiques (19, 15, 19, 15, 18, 18 tests, 100 %, mêmes listes, durées
ignorées). Listes `ctest -N` (`env-37-avant/ctest-N/`, lancées depuis `<ROOTSTOCK>/trunk`)
identiques pour host et les 16 presets (17/17), hors la ligne informative « Internal ctest
changing into directory » présente dans `env-35-apres` (dépend du répertoire de lancement).

## 3. Provenance et regreffe
Clone `family-stm32wlxx`, branche `devenv/env-37` (depuis `master` dbc58d7), un commit par
ensemble, aucun fichier tiers déplacé, renommé, recopié ni supprimé ; `lepton-greffon.json`
inchangé :

| Commit | Fichier |
| --- | --- |
| 2255483 | `kernel/dev/arch/cortexm/stm32wlxx/cubemx_hal_driver/LEPTON-PROVENANCE.md` |
| a6f517f | `kernel/core/ucore/cmsis/Device/st/stm32wlxx/LEPTON-PROVENANCE.md` |
| d2d5e95 | `kernel/dev/arch/cortexm/stm32wlxx/radio_subghz_phy/LEPTON-PROVENANCE.md` |
| 6107dd8 | `kernel/dev/arch/cortexm/stm32wlxx/Utilities/LEPTON-PROVENANCE.md` |

`verifier-import.sh` ignore `LEPTON-PROVENANCE.md` : classements inchangés (radio : 18 identiques,
6 écarts, relancé après commit).

Regreffe : copie d'essai `~/lepton-tools-dev/essais/env-37-copie` (`cp -RP` de
`.scion.rootstock.signature`, `.scion.trunk.tolerated`, `depots`, `trunk`),
`scion graft --scion lepton@family-stm32wlxx` (243 feuilles), code 0 ; même commande sur
`<ROOTSTOCK>`, code 0. Liste des liens de `<ROOTSTOCK>` identique à celle de la copie.

| Contrôle du trunk | Avant | Après |
| --- | --- | --- |
| Liens | 3978 | **3982** (+4 `LEPTON-PROVENANCE.md`, `env-37-wl-provenance/liens-ajoutes.txt` ; 0 retrait) |
| Liens cassés | 0 | 0 |
| Fichiers réguliers hors `.DS_Store` | 0 | 0 |
| `lepton -C <ROOTSTOCK> check` | — | code 0 (19 fichiers conformes) |

## 4. Contrôles (oracle après)
`rapports/oracles/env-37-apres/` : mêmes commandes que l'oracle avant, sur `<ROOTSTOCK>` regreffé
(3982 liens), constructions à neuf : « tout a réussi ». Comparaisons contre `env-37-avant`
(`env-37-apres/comparaisons/`) :

| Preset | Sections/symboles | Empreinte | Fumée | Banc KAL | Écarts expliqués |
| --- | --- | --- | --- | --- | --- |
| `qemu-mps2-an386-embos` | code 0 | différente | `cortexM4-qemu-mps2-an386` | 19/19 identique | date, jeton UART |
| `qemu-mps2-an386-embos-soft` | code 0 | différente | idem | 15/15 identique | date, jeton UART |
| `qemu-mps2-an386-freertos` | code 0 | différente | idem | 19/19 identique | date, jeton UART, place de `rcv SIGCHLD` |
| `qemu-mps2-an386-freertos-soft` | code 0 | différente | idem | 15/15 identique | idem |
| `qemu-mps2-an500-embos` | code 0 | différente | `cortexM7-qemu-mps2-an500` | 18/18 identique | idem |
| `qemu-mps2-an500-freertos` | code 0 | différente | idem | 18/18 identique | idem |
| 10 presets de carte (F429, F439, WL55, SAMD21, F746 ; embOS et FreeRTOS) | code 0 ×10 | différente | — (construction seule) | — | date |

- Empreintes : différentes sur les 16 presets, du seul fait de la date de compilation incluse
  dans le noyau (`kernel compilation date`) ; sections et symboles identiques (nom, type, taille).
- Fumée : comparée en ignorant la date de compilation, le jeton `lepton-uart1-<n>` et la place
  du message asynchrone `rcv SIGCHLD` dans la console (`rapports/env-34-hal-f4.md` §5.1, E-1,
  E-2) ; aucun autre écart.
- host : 7/7 ; empreintes mklepton identiques. Listes `ctest -N` : 17/17 identiques à
  `env-37-avant`. Les tests sur carte n'ont pas été lancés : rien de compilé ne change, et les
  binaires de carte ont mêmes sections et mêmes symboles.
- Trunk : 3982 liens, 0 lien cassé, 0 fichier régulier ; `lepton check` code 0 (§3).

Bilan : rien de compilé ne change ; les quatre ensembles ont leur provenance.

## 5. Cas d'épreuve pour ENV-38
| Ensemble | Dépôt, révision | Chemin amont → chemin dans la famille | Exceptions |
| --- | --- | --- | --- |
| HAL | `stm32wlxx-hal-driver` `v1.3.0` e3966ab (PA-61 ; copie identique à STM32CubeWL `v1.3.0` `Drivers/STM32WLxx_HAL_Driver`) | `Inc/` → `cubemx_hal_driver/inc/` ; `Src/` → `cubemx_hal_driver/src/` ; `README.md`, `Release_Notes.html` → `cubemx_hal_driver/` (renommage de casse de répertoire) | `stm32_hal_legacy.h` d'une autre révision ; `LICENSE.md` non repris, `LICENSE.txt` hors amont ; `_htmresc/` non repris |
| CMSIS device | `cmsis-device-wl` `v1.1.1` d248c55 | `Include/{stm32wl55xx.h,stm32wlxx.h,system_stm32wlxx.h}` → `cmsis/Device/st/stm32wlxx/` ; `Source/Templates/system_stm32wlxx.c` → idem ; `Source/Templates/iar/startup_stm32wl55xx_cm4.s` → `…/startup/iar/` (aplatissement, sélection par fichier, casse `ST/STM32WLxx` → `st/stm32wlxx`) | sous-ensemble d'une puce ; 2 fichiers ni compilés ni inclus |
| Pile radio | `stm32-mw-subghz-phy` `v1.3.0` 1cad768 | racine → `radio_subghz_phy/` (sans renommage) | `radio.c` modifié ; `stm32_radio_core_inc/` (4 fichiers) d'un **autre dépôt** (STM32CubeWL `Projects/…/SubGHz_Phy_PingPong/Core/Inc`), 3 modifiés ; `LICENSE.txt` hors amont |
| Utilitaires | STM32CubeWL `v1.3.0` 378e461 (seul amont ; exception admise au PA-61) | `Utilities/<d>/` → `Utilities/<d>/` pour `conf`, `Fonts`, `lcd`, `lpm/tiny_lpm`, `misc`, `sequencer`, `timer`, `trace/adv_trace` (sous-arbre d'un gros dépôt) | `stm32_timer.h` modifié ; documentation (`html/`, `_htmresc/`, notes de version), `LICENSE.md`, `PC_Software/` exclus ; `LICENSE.txt` ×6 hors amont |

Exigences mises en évidence pour la projection : renommage de répertoire (casse), aplatissement
et sélection fichier par fichier, sous-arbre d'un dépôt volumineux, deux dépôts amont pour un même
répertoire de destination, fichiers modifiés localement, fichiers locaux hors amont, révisions
différentes d'ensembles venus du même paquet.
