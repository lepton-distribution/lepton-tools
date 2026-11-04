# Passation ENV-34 — HAL et CMSIS device STM32F4 importés par la méthode du F7 — session du 2026-11-04 (préparation)

## Statut
à démarrer — session hors étape : analyse des fichiers d'étapes ENV-34 à ENV-36 avant exécution.
Aucune tâche d'ENV-34 exécutée, aucun fichier de l'arbre Lepton touché, aucune branche `devenv/env-34`.
Cette passation sera remplacée par celle de la session qui exécutera ENV-34.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` | 5ce29db « devenv: push de main consigné (PA-P) » ; 5da8502, ca5339a, 5ce29db poussés le 2026-11-04 | oui |
| clone noyau `depots/lepton/original/master` | `master` | b3a5415 « Fusion de devenv/env-32 … » (non touché) | oui |
| famille `depots/lepton/family-stm32f4xx/master` | `master` | 8364493 « Fusion de devenv/env-26 … » (non touché) | oui |
| BSP `depots/lepton/bsp-nucleo-f429zi/master`, `bsp-nucleo-f439zi/master` | `master` | 2b2dfdd, bdbfa06 (non touchés) | oui |
| seed.scions, graine, autres greffons | — | non touchés | oui |

## Fait pendant la session
- Fichiers d'étapes ENV-34, ENV-35, ENV-36 confrontés aux clones et aux dépôts amont. Confirmé :
  HAL `v1.8.5` = `b6f0ed3` ; `cmsis_device_f4` `3c77349` = `v2.6.11` + 1 commit, sans tag ; les
  deux sont bien les sous-modules de STM32CubeF4 `v1.28.3` (API GitHub `contents/…?ref=v1.28.3`) ;
  CMSIS_5 `5.9.0` ; les 7 en-têtes de `cmsis-5/CMSIS/Core/Include` du noyau sont identiques à
  `5.9.0` aux fins de ligne près (SHA-256 après retrait des CR) ; `core_cm4.h` 5.9.0 est V5.1.2 et
  ses inclusions (`cmsis_version.h`, `cmsis_compiler.h`, `mpu_armv7.h`) sont déjà présentes.
- Confirmé aussi : `cubemx_hal_driver/` V1.7.1 / V2.6.1, 190 fichiers suivis (99 `inc`, 2 `inc/Legacy`,
  89 `src`), 6 fichiers hors amont ; SPL compilée 2 222 lignes sur 5 fichiers ; `nucleo_f439zi_board.c`
  254 lignes ; F7 : 4 modules HAL compilés, `dev_stm32f7xx_{hal_tick,eth_x,uart_x}.c` 29/432/153
  lignes, hal_conf du BSP avec HAL, ETH, FLASH, GPIO, PWR, RCC, CORTEX ; HAL F4 v1.8.5 : nouvelle API
  ETH présente, `Src/Legacy/stm32f4xx_hal_eth.c` présent ; `CRYP_IRQn` = 79 dans `stm32f439xx.h` ;
  `stm32f429xx.h` amont n'emploie aucun qualificateur propre à CMSIS 5 (`__IM`, `__OM`, `__IOM`).
- Constat non traité par les étapes (ordre des `-I`, `compile_commands.json` de `<ROOTSTOCK>/build/`) :
  `cmake/isa/armv7m.cmake` place `kernel/core/ucore/cmsis/CMSIS/Include` (CMSIS-Core V3.30, seul
  `core_cm4.h` de l'arbre aujourd'hui) en première position pour tous les presets armv7m ;
  `cmsis-5/CMSIS/Core/Include` n'est ajouté que par `cmake/cpu/cortex-m7.cmake` (position 4 sur le
  F7) ; les inclusions des manifestes de greffon sont ajoutées après (`cmake/lepton_greffons.cmake:272`).
  Le preset `nucleo-wl55jc1-embos` résout `core_cm4.h` vers V3.30 : la HAL WL compile ainsi. ENV-34
  n'en est pas affectée (aucun preset M4 ne voit `cmsis-5/CMSIS/Core`). ENV-35 le sera : la HAL F4
  prendrait V3.30, pas le `core_cm4.h` importé ; la compilation à blanc d'ENV-34 §4 ne reflète pas
  cet ordre.
- Corrections commitées (ca5339a, `main`) : ENV-34 §1, 7 fichiers non compilés incluent
  `stm32f4xx_hal.h` (`flash_if.h` retiré de la liste, il n'inclut rien) ; ENV-34 §3, suppression du
  répertoire `cubemx_hal_driver/` après `git rm -r` (`.DS_Store` ignoré) ; ENV-35 §Pièges, 8 → 7.
- `DEVENV-STATUS.md` : lignes de journal (analyse, PA-P, fin de session), prochaine action.

## Reste à faire dans l'étape
- [ ] Tout ENV-34 (§1 à §4) : rien n'est commencé.
- [ ] Proposition non validée, à intégrer à l'audit §1 : relever le `core_cm4.h` effectivement
      retenu (`-H`) et l'ordre des `-I` d'un preset F4 ; poser au PA-55 le choix V3.30 pour le F4
      (comme le WL55) ou CMSIS 5 avec modification d'`armv7m.cmake` ou du lecteur ; faire la
      compilation à blanc du §4 dans l'ordre réel ou dans les deux ordres.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Corriger les points 2 (décompte) et 4 (résidu `.DS_Store`) dans les fichiers d'étapes | utilisateur | oui (journal) |
| Commit sur `main` et push de `main` (PA-P) | utilisateur | oui (journal) |
| Point 1 : deux `core_cm4.h`, à trancher au PA-55 ou au PA-57 | proposition non validée | signalé au journal |
| Point 3 : ENV-35 §1, dépendants hors plan de la SPL à compléter : `kernel/dev/bsp/discovery_f4` (1), `discovery_f4-baseboard-modem` (13), `olimex_p407` (2), en plus de `stm32f469i-eval` (3), `kernel/usb/stm32f4-usb-core` (4), `kernel/core/ucore/cmsis/Device/st/stm32f4xx` (2) | proposition non validée | non |
| Point 5 : `LEPTON-PROVENANCE.md` de `cmsis-5/CMSIS/Core` : origine réelle paquet embOS (commentaire de `cortex-m7.cmake`), équivalence CMSIS_5 5.9.0 vérifiée | proposition non validée | non |
| Point 6 : constat pour l'audit ENV-35 : `ld/common-cortexm.ld` place en `.ccm_bss` les pools lwIP sauf `PBUF_POOL`, les piles noyau et lwIP, la mémoire statique FreeRTOS ; le pilote ETH F4 actuel n'a aucun attribut de section | constat | non |
| Point 7 : ENV-36 C2, fixer le nombre de liens attendu dans la consigne (3957 avant ENV-34) | proposition non validée | non |

## Pièges rencontrés
- `timeout` absent sur macOS : `git ls-remote` et `curl --max-time` suffisent pour relever les têtes
  amont ; `gh api repos/<org>/<dépôt>/contents/<chemin>?ref=<tag>` donne le commit d'un sous-module.
- `git status --ignored` sur le clone famille liste un `.DS_Store` par répertoire visité par le
  Finder : le contrôle d'ENV-34 §Pièges porte sur les fichiers autres que `.DS_Store`.
- `grep driverlib` dans le noyau rend aussi les 36 fichiers du `driverlib` Stellaris : filtrer sur
  `stm32f4xx/driverlib` ou `USE_STDPERIPH_DRIVER`.

## Critères de validation
- [ ] PA-55 et PA-56 tranchés et consignés.
- [ ] Binaires identiques sur host et les 16 presets (code 0).
- [ ] HAL et CMSIS device identiques octet pour octet à leurs révisions amont, provenance à côté.
- [ ] Aucune copie de HAL F4 sans provenance dans l'arbre.

## Reprise
Commande ou première action de la session suivante :
```
démarre la session   # ENV-34 : lire cette passation, puis audit §1 (ajouter le relevé des core_cm4.h) et PA-55
```
