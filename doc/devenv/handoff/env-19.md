# Passation ENV-19 — Extraction des cartes STM32F746G-DISCO et SAMD21 Xplained Pro — session du 2026-10-31

## Statut
terminée — F746 et SAMD21 sont des greffons famille et BSP publiés (`family-stm32f7xx`,
`bsp-stm32f746g-disco`, `family-samd21`, `bsp-samd21-xplained-pro`), inscrits dans `original-tree` ;
repli `cmake/boards` retiré ; symboles identiques sur 14 presets ; cartes vertes.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` (fusion `--no-ff` de `devenv/env-19`, poussées toutes deux) | commit d'état et passation, puis « Fusion de devenv/env-19 » | oui |
| clone noyau `depots/lepton/original/master` | `master` 35b117b (poussé, `devenv/env-19` poussée) | Fusion de devenv/env-19 (ENV-19 extraction…) | oui |
| graine `depots/lepton-seed.scions/original-tree` | `original-tree` f4ff07b (poussé, `devenv/env-19` poussée) | Fusion de devenv/env-19 (ENV-19 : greffons…) | oui (`.DS_Store` ignoré) |
| `depots/lepton/family-stm32f7xx/master` | `master` 34ccaf8 (poussé) | Fusion de devenv/env-19 | oui |
| `depots/lepton/bsp-stm32f746g-disco/master` | `master` 9f81c1b (poussé) | Fusion de devenv/env-19 | oui |
| `depots/lepton/family-samd21/master` | `master` a389592 (poussé) | Fusion de devenv/env-19 | oui |
| `depots/lepton/bsp-samd21-xplained-pro/master` | `master` 46337d1 (poussé) | Fusion de devenv/env-19 | oui |
| `<ROOTSTOCK>` | trunk regreffé : 3935 feuilles, 0 fichier régulier, 0 lien cassé, 13 greffons ; `original-tree.code-workspace` régénéré (14 lancements) | | oui |
| copie d'essai `~/lepton-tools-dev/essais/env-19` | clones sur `devenv/env-19` ; `build-lots/`, `build-avant/`, `build-apres/` (220 Mo) | | à supprimer sur demande |

## Fait pendant la session
- Tâche 1 : audit `rapports/env-19-extraction.md` §1-§5 (`ninja -t deps/inputs` des 15 builds) ; PA-25 (§6).
- Tâche 2 : oracle `rapports/oracles/env-19-avant/` (= `env-17-apres`).
- Tâche 3 : 4 dépôts (import à l'identique depuis 8ba904b, manifestes validés par
  `check-jsonschema`, `CMakeLists.txt` des BSP) ; clone noyau 7 commits (§7 du rapport) ; graine
  2 commits ; regreffe copie puis `<ROOTSTOCK>` ; oracles `env-19-lot-f746`, `env-19-lot-samd21`.
- Tâche 4 : oracle `env-19-apres` et §8 du rapport (E-1 à E-6) ; cartes : F746 19/19 embOS et
  FreeRTOS, SAMD21 embOS 15/15, SAMD21 FreeRTOS écart accepté identique + banc KAL 14/14 ;
  `lepton check` 0, `lepton generate` 0 ; PA-26 : `gh repo create` ×4 (publics, branche par défaut
  remise à `master`), fusions et push.

## Reste à faire dans l'étape
- Aucune tâche du fichier d'étape.
- Hors étape : validation Debian (ENV-21) ; `.DS_Store` de la copie et des clones (ignorés par git).

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-25 Q1-Q7 (liste, noms, `LEPTON_MKCONF` des presets, CMSIS-Core `BEFORE` dans le BSP, repli retiré, cartes disponibles, critère d'empreintes amendé) | utilisateur | oui |
| PA-26 : dépôts créés par `gh`, publics ; fusion maintenant, push | utilisateur | oui |
| Branche par défaut GitHub des 4 dépôts remise à `master` (devenue `devenv/env-19` au premier push) | proposition appliquée (conformité aux 7 greffons existants) | non (rapport : passation) |
| Contrôle `LEPTON_CPU` du module SAMD21 retiré (redondant avec le cœur du manifeste) ; message du contrôle FPU de F746 conservé | proposition du rapport §3.4, non contestée au PA-25 | rapport |
| Fumée SAMD21 FreeRTOS acceptée en échec (écart de la migration), banc par `-FS board_t0 -E board.smoke_lsh` | référence de la migration (`validation-macos.md:114-115`) | rapport §8 |

## Pièges rencontrés
- Copie d'essai au chemin plus long : chaînes `__FILE__` de FreeRTOS plus longues → `.text` +120 → mesurer à chemin égal (avant et après reconstruits dans la copie).
- Empreintes des binaires différentes à chaque construction (`__DATE__`/`__TIME__`) → seules sections et symboles comptent.
- Le hook refuse toute redirection vers un `trunk/`, même d'une copie → `scion graft-remove` (sans `--purge`) pour dégreffer.
- `kernelconf.h` est en Latin-1 → éditer en octets.
- `gh repo create` puis push de deux branches : la branche par défaut devient la première listée → `gh repo edit --default-branch master`.
- `ctest -L kal -FS board_t0` sélectionne encore `board.smoke_lsh` (label `kal`) → ajouter `-E board.smoke_lsh`.

## Critères de validation
- [x] PA-25 et PA-26 tranchés et consignés.
- [x] `cmake/boards/` du noyau sans F746 ni SAMD21 ; 4 greffons publiés, inscrits dans `original-tree`.
- [x] Symboles identiques sur 14 presets ; empreintes mklepton identiques (hors E-6, PA-25 Q7) ; trunk : 0 fichier régulier, 0 lien cassé.
- [x] Ajout des cartes sans modification du système de construction commun (BLD-6) : constat dans le rapport §8.

## Reprise
Commande ou première action de la session suivante :
```
démarre la session   # skill devenv-session ; ENV-20, voir « Prochaine action »
```
