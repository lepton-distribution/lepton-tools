# Passation ENV-34 — HAL et CMSIS device STM32F4 importés par la méthode du F7 — session du 2026-11-05

## Statut
terminée — HAL F4 v1.8.5, CMSIS device 3c77349 et `core_cm4.h` 5.9.0 importés avec provenance,
sans changement de compilation ; fusionnés et poussés (PA-56).

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` (après fusion) | fusion de `devenv/env-34` (voir `git log`) ; `main` et `devenv/env-34` poussées | oui |
| `family-stm32f4xx` (`depots/lepton/family-stm32f4xx/master`) | `master` | c5de4a5 « Fusion de devenv/env-34 … » ; `master` et `devenv/env-34` poussées | oui (hors `.DS_Store`) |
| clone noyau (`depots/lepton/original/master`) | `master` | 2893297 « Fusion de devenv/env-34 … » ; `master` et `devenv/env-34` poussées | oui |
| BSP `nucleo-f429zi`, `nucleo-f439zi`, graine, seed.scions | `master` / — | non touchés | oui |

`<ROOTSTOCK>` : 3977 liens, 0 cassé, 0 fichier régulier hors `.DS_Store`, `lepton check` 0.
Compile : host et les 16 presets construits à neuf (oracle `env-34-apres`), binaires inchangés.

## Fait pendant la session
- Audit (rapport §1) : références amont confirmées (`ls-remote`, sous-modules de STM32CubeF4
  v1.28.3) ; 190 fichiers, 6 hors amont, 14 nouveaux en v1.8.5 ; références relevées, aucune
  compilée ; fins de ligne ; `core_cm4.h` V3.30 retenu par F429 et WL55 (`-H`, position 2 des `-I`).
- PA-55 tranché (rapport §2, `DEVENV-STATUS.md` §Décisions).
- Oracle avant `oracles/env-34-avant/` conforme à `env-32-apres` ; listes `ctest -N` de host et
  des 16 presets (nouvelle référence).
- Import : famille (5 commits), noyau (2 commits) ; regreffe sur copie puis `<ROOTSTOCK>`.
- Oracle après : code 0 ×16, host 7/7, mklepton, KAL, `ctest -N` identiques (rapport §5.1).
- `scripts/tiers/verifier-import.sh` : F4 et F7 0 écart ; noyau `core_cm4.h` OK, 7 voisins `CR`.
- `scripts/tiers/compiler-hal-f4-a-blanc.sh` : CMSIS 5 seul 0 échec (90 sources ×2 puces) ;
  V3.30 en tête 1 échec (`stm32f4xx_ll_usb.c`, `__UNALIGNED_UINT32_READ/WRITE`).
- Fichiers d'étapes : ENV-35 §1 (dépendants hors plan de la SPL, `.ccm_bss`, `core_cm4.h`,
  `driverlib/`), ENV-36 C2 (nombre de liens).
- PA-56 : fusions et push.

## Reste à faire dans l'étape
- [ ] Rien. Écart renvoyé à ENV-35 : 4 en-têtes HAL V1.3.0 sans provenance dans `driverlib/`.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-55 : destination `hal_driver/{Inc,Src}`, contenu, sous-ensemble CMSIS, 6 fichiers supprimés, clones dans `~/lepton-tools-dev/tiers/`, `core_cm4.h` LF + provenance, script, compilation à blanc dans les deux ordres, `core_cm4.h` du F4 renvoyé au PA-57, points 3, 6, 7 reportés | utilisateur | oui |
| PA-56 : fusions et push ; écart `driverlib/` renvoyé à ENV-35 | utilisateur | oui |
| Critère d'ENV-36 C4 : ligne `cmsis5` à 0 échec et lignes `v330` identiques au Mac (le script rend 1 tant que `v330` échoue) | proposition non validée (rapport §5.3) | non |
| Provenance de `cmsis-5/CMSIS/Core/` : 7 fichiers attribués au paquet embOS (commentaire de `cortex-m7.cmake`) | proposition validée au PA-55 (point 5) | oui |

## Pièges rencontrés
- Le hook `proteger-trunk.py` refuse toute commande contenant `sed -i` et une chaîne `trunk/`,
  même sur un fichier de `doc/` : copier sans réécrire.
- `cmsis-5/` du noyau contient aussi un `Device/` volumineux : `verifier-import.sh` sur ce
  répertoire exige `--liste-seule`.
- Empreintes et console de fumée varient d'une construction à l'autre (date, jeton UART,
  `rcv SIGCHLD`) : comparer hors de ces éléments (rapport §5.1, E-1, E-2).
- zsh : `echo =====` échoue (développement `=cmd`) ; utiliser `echo '---'`.

## Critères de validation
- [x] PA-55 et PA-56 tranchés et consignés.
- [x] Binaires identiques sur host et les 16 presets (code 0).
- [x] HAL et CMSIS device identiques octet pour octet à leurs révisions amont, provenance à côté.
- [ ] Aucune copie de HAL F4 sans provenance dans l'arbre : écart `driverlib/` (4 en-têtes), renvoyé
      à ENV-35 par décision de l'utilisateur.

## Reprise
Commande ou première action de la session suivante :
```
démarre la session   # ENV-35 : audit §1 (core_cm4.h : rapport env-34 §5.3 ; driverlib : §5.4), puis PA-57
```
