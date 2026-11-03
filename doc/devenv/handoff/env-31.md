# Passation ENV-31 — Piles FreeRTOS lisibles par rtos-views — session du 2026-11-03

## Statut
terminée — `configRECORD_STACK_HIGH_ADDRESS` 1 dans `FreeRTOSConfig.h` : rtos-views affiche taille,
usage et pic de pile des tâches FreeRTOS (WL55 constaté par l'utilisateur) ; nouvel oracle de
référence `rapports/oracles/env-31-apres/`.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` : fusion `--no-ff` de `devenv/env-31` (PA-50) ; `main` et `devenv/env-31` poussées | fusion « Fusion de devenv/env-31 (ENV-31 piles FreeRTOS lisibles par rtos-views, PA-50) » | oui |
| clone noyau `depots/lepton/original/master` | `master` 7fe3757 (fusion de `devenv/env-31`, fc71632) ; `master` et `devenv/env-31` poussées | « Fusion de devenv/env-31 (ENV-31 piles FreeRTOS lisibles par rtos-views, PA-50) » | oui |
| autres (seed.scions, graine, greffons) | non touchés | — | oui |

Hors dépôts :
- `<ROOTSTOCK>/build/<preset>` reconstruits à neuf par l'oracle après (16 presets + host) ;
  `nucleo-wl55jc1-freertos` et `stm32f746g-disco-freertos` reconfigurés avec les options de carte
  (port série, sondes WL55 A/B, IP réseau) ;
- images en flash : `nucleo-wl55jc1-freertos` d'ENV-31 sur WL55 A et B,
  `stm32f746g-disco-freertos` d'ENV-31 sur le F746 ;
- lepton non réinstallé (aucun changement de lepton-tools/lepton) ;
- constructions jetables de mesure dans le scratchpad de la session (non conservées).

## Fait pendant la session
- Tâche 1 : audit `rapports/env-31-freertos.md` §1-§5 (rtos-views 0.0.16 : `pxEndOfStack` suffit
  pour les piles, `uxTCBNumber` seulement pour l'ID ; mesures jetables RECORD seul / RECORD + TRACE
  sur SAMD21 et WL55) ; PA-49 (§6).
- Tâche 2 : oracle `env-31-avant` (host + 6 QEMU + 10 carte), conforme à `env-27-apres` (code 0 ×16,
  host 7/7, mklepton identiques, bancs QEMU identiques).
- Tâche 3 : clone noyau fc71632 (`FreeRTOSConfig.h`, en-tête mis à jour).
- Tâche 4 : oracle `env-31-apres` ; comparaisons `env-31-apres/comparaisons/` ; embOS (8) code 0 ;
  FreeRTOS E-1 (8 presets) et E-2 (an386-freertos `.text` +16, arrêt puis critère amendé, PA-49 (2)) ;
  QEMU 19/19/15/15/18/18 et `peripheriques` vert ; WL55 16/16 (radio 20/20) ; F746 20/20 (réseau) ;
  VSCodium WL55 : piles affichées (utilisateur) ; `lepton check` 0 ; skill `lepton-cibles` (7ce98d8).
- PA-50 : fusions et push.

## Reste à faire dans l'étape
- Aucun. Validation Debian : ENV-33. NUCLEO-F429ZI et SAMD21 non essayées sur carte (PA-49 Q4) :
  binaires couverts par l'oracle (E-1 seul).

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-49 Q1 : `configRECORD_STACK_HIGH_ADDRESS` 1 seul, trace à 0 | utilisateur | oui |
| PA-49 Q2 : tous les presets FreeRTOS, sous `#ifndef` | utilisateur | oui |
| PA-49 Q3 : critère d'écart par preset FreeRTOS ; embOS et host code 0 | utilisateur | oui |
| PA-49 Q4 : cartes WL55 et F746 | utilisateur | oui |
| PA-49 (2) : `.text` = +4 de code plus le bourrage d'alignement qui en résulte | utilisateur | oui |
| PA-50 : nouvel oracle de référence, fusions `--no-ff`, push | utilisateur | oui |
| Essai F746 avec les WL55 débranchées | proposition de la session, suivie par l'utilisateur | rapport §8, skill `lepton-cibles` |

## Pièges rencontrés
- Sondes multiples : la cfg OpenOCD du F746 (et de tout BSP sans `LEPTON_BOARD_STLINK_SERIAL`) n'a
  pas d'`adapter serial`, `LEPTON_BOARD_OPENOCD_CFG` est posé par `set` simple (non surchargeable)
  et `interface/stlink.cfg` accepte aussi les STLINK-V3 → risque de flasher une WL55 → essai avec le
  F746 seul branché. Une option de numéro de sonde pour ces BSP serait une proposition (non validée).
- OpenOCD de Cortex-Debug resté actif (session VSCodium) : `board.smoke_lsh` échoue en 0,6 s
  (OpenOCD code 1, sans message utile) → `pgrep -fl openocd`, arrêt de la session par l'utilisateur.
- Le message d'échec d'OpenOCD n'est pas conservé par `smoke_lsh.py` : relancer
  `openocd -f <cfg réelle du clone> -c "init; targets; shutdown"` (lecture seule) pour diagnostiquer.
- Construction témoin « avant » possible sans toucher au clone : `-DconfigRECORD_STACK_HIGH_ADDRESS=0`
  (valeur sous `#ifndef`).
- Fichiers sources en ISO-8859 (`kernel_pthread.c`) : `grep` sans `LC_ALL=C grep -a` ne trouve rien.

## Critères de validation
- [x] PA-49 et PA-50 tranchés et consignés.
- [x] embOS et `host` : `comparer-oracle.py` code 0.
- [x] FreeRTOS : chaque écart classé dans le critère du PA-49 (amendé, PA-49 (2)).
- [x] Fumée et banc KAL FreeRTOS : comptes inchangés (QEMU, WL55 16/16, F746 20/20).
- [x] Piles affichées par rtos-views sur WL55 FreeRTOS (constat de l'utilisateur).

## Reprise
Commande ou première action de la session suivante :
```
démarre la session   # ENV-32 (etapes/ENV-32-test-radio-bsp.md), audit jusqu'au PA-51
```
