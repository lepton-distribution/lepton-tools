# Passation ENV-32 — Test `board.radio` fourni par le BSP `nucleo-wl55jc1` — session du 2026-11-03

## Statut
terminée — le test radio entre deux cartes est le test `nucleo-wl55jc1.radio` du BSP (champ
`tests`, TST-2) ; binaires inchangés ; banc radio vert sur deux WL55 en embOS et en FreeRTOS.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` : fusion `--no-ff` de `devenv/env-32` (PA-52) ; `main` et `devenv/env-32` poussées | « Fusion de devenv/env-32 (ENV-32 test radio fourni par le BSP nucleo-wl55jc1, PA-52) » | oui |
| clone noyau `depots/lepton/original/master` | `master` b3a5415 (fusion de `devenv/env-32`, 57cee41 et c19d05b) ; `master` et `devenv/env-32` poussées | « Fusion de devenv/env-32 (ENV-32 …, PA-52) » | oui |
| `depots/lepton/bsp-nucleo-wl55jc1/master` | `master` ef51ec1 (fusion de `devenv/env-32`, e9fc2b9 et cefd09d) ; `master` et `devenv/env-32` poussées | « Fusion de devenv/env-32 (ENV-32 …, PA-52) » | oui (`.DS_Store` non suivi à la racine du clone, hors `scion/`) |
| autres (seed.scions, graine, autres greffons) | non touchés | — | oui |

Hors dépôts :
- `<ROOTSTOCK>` regreffé (`lepton@original::tree`, `lepton@bsp-nucleo-wl55jc1`) : 3957 liens, 0 cassé,
  aucun fichier régulier hors `.scion.grafted.list` et `.DS_Store` tolérés ; `lepton check` 0 ;
- `<ROOTSTOCK>/build/<preset>` reconstruits à neuf par l'oracle après (16 presets + host) ;
  `nucleo-wl55jc1-embos` et `-freertos` reconfigurés avec le banc (A `/dev/cu.usbmodem145103`
  n° …3937, B `/dev/cu.usbmodem1454303` n° …9937) ;
- images en flash : `nucleo-wl55jc1-freertos` (= ENV-31) sur WL55 A et B ;
- copie d'essai `essais/env-32-copie` supprimée ; lepton non réinstallé (aucun code de lepton modifié).

## Fait pendant la session
- Tâche 1 : audit `rapports/env-32-radio.md` §1-§7 ; PA-51 (recommandations Q1-Q9 retenues).
- Tâche 2 : oracle `rapports/oracles/env-32-avant/` (host + WL55 ×2, code 0 contre `env-31-apres`),
  listes `ctest -N` en 4 variantes × 2 backends (`ctest-N/relever-ctest-N.sh`).
- Tâche 3 : BSP (copie mécanique, puis champ `tests`, `tests/CMakeLists.txt`, `radio.py`
  `--tests-noyau`, déclaration retirée du `CMakeLists.txt` de carte) ; noyau (`board_radio.py` retiré,
  `BUILDING.md` §7, `CLAUDE.md`) ; lepton-tools (skill `lepton-cibles`, exemple de schéma) ; regreffe
  copie puis `<ROOTSTOCK>`.
- Tâche 4 : `rapports/oracles/env-32-apres/` (code 0 ×16, host 7/7, QEMU identiques) ; `ctest -N`
  identiques au renommage et au rang près ; banc `banc-carte/` 16/16 embOS et FreeRTOS ; rapport §8-§10.
- PA-52 : fusions et push.

## Reste à faire dans l'étape
- Aucun. Validation Debian (découverte du test, pas de carte) : ENV-33.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-51 Q1-Q9 : `tests/` du BSP, `radio.py`, `--tests-noyau`, nom `nucleo-wl55jc1.radio`, étiquettes et propriétés conservées, script du noyau retiré, découpage du `CMakeLists.txt`, ordre changé accepté, deux WL55, documents | utilisateur | oui |
| Graft simple de `<ROOTSTOCK>` ; écriture flash des deux WL55 | utilisateur | oui (PA-52) |
| PA-52 : fusions `--no-ff`, push, clones sur `master`, copie d'essai supprimée | utilisateur | oui |

## Pièges rencontrés
- `python3 -I` ignore `PYTHONDONTWRITEBYTECODE` : un import de `smoke_lsh` par le chemin du trunk
  écrit `trunk/tests/__pycache__/` → `scion graft` refuse (« fichiers qui ne sont pas des greffes »).
  Parade : ne pas importer depuis le trunk avec `-I`, ou ajouter `-B`.
- Une VM qui prend les cartes USB coupe la liaison SWD en plein banc (« jtag status contains invalid
  mode value ») et fait disparaître les consoles `/dev/cu.usbmodem*` ; les sondes restent
  énumérées. Parade : rendre les cartes au Mac, relever consoles et Location ID, relancer.
- La console de B a changé (`…1454403` en ENV-31, `…1454303` ici) : relever par Location ID
  (`system_profiler SPUSBDataType`) à chaque banc.
- zsh ne découpe pas une variable non citée (`$o`) : utiliser un tableau ou `${=o}`.
- `sed` de macOS ne connaît pas `\S`.
- Le Finder recrée des `.DS_Store` pendant un `rm -rf` : relancer la suppression.

## Critères de validation
- [x] PA-51 et PA-52 tranchés et consignés.
- [x] Le test radio est déclaré par le BSP (champ `tests`), plus par le noyau ni par `include()`.
- [x] Banc radio vert sur deux cartes, embOS et FreeRTOS ; binaires identiques (code 0).
- [x] Aucune copie de `smoke_lsh.py` hors du noyau.

## Reprise
Commande ou première action de la session suivante :
```
démarre la session   # ENV-33 (etapes/ENV-33-validation-debian.md), consigne jusqu'au PA-53
```
