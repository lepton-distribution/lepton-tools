# Passation ENV-20 — BSP `nucleo-f439zi` — session du 2026-10-31

## Statut
terminée — BSP `nucleo-f439zi` publié (`lepton-bsp-nucleo-f439zi`), inscrit dans `original-tree` ;
table de vecteurs F4 complète dans `family-stm32f4xx` ; presets `nucleo-f439zi-{embos,freertos}` ;
binaire F439 essayé sur NUCLEO-F429ZI (19/19). Pas de NUCLEO-F439ZI : démarrage sur F439 non prouvé.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` (fusion `--no-ff` de `devenv/env-20`, poussées toutes deux) | commit d'état et passation, puis « Fusion de devenv/env-20 » | oui |
| clone noyau `depots/lepton/original/master` | `master` 40d7197 (poussé, `devenv/env-20` f571d02 poussée) | Fusion de devenv/env-20 | oui |
| `depots/lepton/family-stm32f4xx/master` | `master` 2b21340 (poussé, `devenv/env-20` 2fb7cfe poussée) | Fusion de devenv/env-20 | oui |
| `depots/lepton/bsp-nucleo-f439zi/master` (nouveau) | `master` f866283 (poussé, `devenv/env-20` 7119dfd poussée) | Fusion de devenv/env-20 | oui |
| graine `depots/lepton-seed.scions/original-tree` | `original-tree` 15740f9 (poussé, `devenv/env-20` d2adddf poussée) | Fusion de devenv/env-20 | oui |
| `<ROOTSTOCK>` | trunk regreffé : 3941 feuilles, 0 fichier régulier, 0 lien cassé, 14 greffons ; `original-tree.code-workspace` régénéré (16 lancements) | | oui |
| copie d'essai `~/lepton-tools-dev/essais/env-20` | supprimée le 2026-10-31 à la demande de l'utilisateur | | — |
| NUCLEO-F429ZI | image `nucleo-f429zi-embos` en flash (« Verified OK ») ; seule sonde branchée | | — |

## Fait pendant la session
- Préalable : 4 `.DS_Store` de `depots/generation/` (source non git du greffon `building`) supprimés, `scion graft --scion lepton@building` (décision de l'utilisateur).
- Tâche 1 : audit `rapports/env-20-bsp.md` §1-§4 ; PA-27 (§5).
- Tâche 2 : oracle `rapports/oracles/env-20-avant/` (= `env-19-apres`).
- Tâche 3 : table de vecteurs (famille 2fb7cfe) ; oracle `env-20-lot-table` (écart F429 limité à la table, classé mécaniquement).
- Tâche 4 : BSP par `lepton scion new --from nucleo-f429zi --no-seed --repo …` puis 7119dfd ; clone noyau cb7020d, 2b78e3b, f571d02 ; graine d2adddf ; regreffe copie puis `<ROOTSTOCK>` ; oracle `env-20-lot-bsp`.
- Tâche 5 : oracle `env-20-apres`, §7 du rapport (E-1 à E-5) ; cartes : NUCLEO-F429ZI 19/19 ×3 ; `check` 0, `generate` 0 ; PA-28 : `gh repo create`, fusions, push (§8).

## Reste à faire dans l'étape
- Aucune tâche du fichier d'étape.
- Hors étape : validation Debian (ENV-21).

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| `.DS_Store` de la source `building` supprimés, regreffe | utilisateur | oui (journal) |
| PA-27 Q1-Q8 (table unique F429/F439, Q3-a `STM32F429xx`, création par `scion new`, presets, CI, graine, essais sur F429 avec flash) | utilisateur | oui |
| NUCLEO-F429ZI branchée seule pour les essais | utilisateur | oui |
| PA-28 : dépôt créé par `gh`, public ; fusion maintenant, push | utilisateur | oui |
| Alias faibles vers un relais local `stm32f4xx_irq_default` (un alias exige une cible de la même unité) ; table étendue renommée `stm32f4xx_vector_table_ext` | proposition appliquée (mise en œuvre de Q1) | rapport §6 |
| Description du dépôt GitHub « lepton bsp nucleo f439zi » (modèle du F429) | proposition appliquée | non (rapport §8) |

## Pièges rencontrés
- Un `alias` GCC exige une cible définie dans la même unité : `Default_Handler` (démarrage générique) ne peut pas être la cible directe.
- À `-Os`, l'appel d'un nom faible n'est pas changé en saut : relais `push/bl/pop` (8 octets) ; estimation de l'audit (+240) corrigée (+496 / +512 mesurés).
- Un nom CMSIS faible défini dans un objet n'entraîne plus l'extraction du membre d'archive qui le définit fort : vérifier par `nm` que chaque gestionnaire utilisé reste `T` (`ETH_IRQHandler` tiré par `dev_stm32f4xx_eth_map`).
- `ctest -L board` prend la première sonde ST-LINK : une seule carte ST branchée (ou `adapter serial` à la main).
- `grep` sur les en-têtes ST (Latin-1) sous locale UTF-8 : rien d'affiché → `LC_ALL=C grep -a`.
- `.DS_Store` du Finder dans une source non git (`depots/generation/building`) : greffés en liens (E1 d'ENV-15 ne filtre que les sources git).

## Critères de validation
- [x] PA-27 et PA-28 tranchés et consignés.
- [x] Table de vecteurs F4 complète ; écart de `nucleo-f429zi-*` démontré et limité à la table.
- [x] BSP `nucleo-f439zi` publié, inscrit dans `original-tree` ; 2 presets construits.
- [x] Aucune modification du système de construction commun (BLD-6) : constat dans le rapport §7.

## Reprise
Commande ou première action de la session suivante :
```
démarre la session   # skill devenv-session ; ENV-21, voir « Prochaine action »
```
