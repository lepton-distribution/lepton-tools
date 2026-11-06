# Passation ENV-38 — scion : conception de la projection et du miroir — session du 2026-11-06

## Statut
terminée — la spécification de la projection et du miroir est écrite, validée au PA-64, sans
aucune ligne de code ; PA-63 et PA-64 tranchés.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` | fusion de `devenv/env-38` (commit de cette passation compris), poussée avec `devenv/env-38` (PA-64) | oui |
| `<SEED_SCIONS>` | `master` | fusion de `devenv/env-38` (e084009 « doc : spécification… »), poussée avec `devenv/env-38` ; **aucun tag** (dernier : `0.5.4.0` sur 99aa973) | oui |
| clone noyau, familles, BSP, graine `original-tree` | — | non touchés (2893297 ; graine 15740f9) | oui |

`<ROOTSTOCK>` non touché (aucune greffe, aucun `graft-update`). scion installé : 0.5.4.0.

## Fait pendant la session
- §1 audit, lecture seule (`rapports/env-38-projection.md` §1) :
  - code de scion (`model`, `seed`, `graft`, `gitops`, `rootstock`, `cli`) ;
  - clients lepton relevés par un sous-agent Explore ; les points sensibles ont été contrôlés à la
    main (`rootstock.py:177-186`, `checks.py:73-93`, `seed.py` `rs.sources()`, `generate.py:384`) ;
  - cas F4, F7 et WL écrits sous forme candidate ; 10 constats C1-C10 (§1.6).
- PA-63 tranché en 16 points (§1.7 du rapport, `DEVENV-STATUS.md` §Décisions, une ligne par point).
- Spécification `<SEED_SCIONS>/doc/projection-miroir.md` :
  - 67 règles : P-C, D, F, M, T, X, R, K, V, E, P, G et M-D, C, R, K ;
  - `grep -i lepton` : 0 ; `git diff --stat master -- scion tests` : vide.
- Rapport :
  - §2 : cas dans le format final, avec 618 chemins attendus (`rapports/env-38-projection/attendus/`).
    Contrôle : chacun est aujourd'hui un lien du trunk. F4 et F7 : liste amont = copie, fichier par
    fichier ;
  - §3 : un cas de test nommé par règle ;
  - §4 : effets hors scion, tous portés par ENV-41 (sauf les miroirs : ENV-40) ;
  - §5 : ce que le format ne couvre pas.
- Fichiers d'étape ENV-39, ENV-40, ENV-41 alignés sur le PA-63 (5563b36) :
  - greffon porteur ; la graine `original-tree` n'est plus touchée en ENV-41 ;
  - versions 0.6.x ; `SCION_MIN_VERSION` relevé en ENV-41.
- PA-64 : spécification validée ; fusions et push.

## Ce qu'ENV-39 et ENV-40 doivent lire
- ENV-39 :
  - spécification, partie A (§0, §1, §A.1-§A.12) ;
  - rapport §2.1 (cas F4 de l'essai à blanc) ;
  - rapport §3, lignes P-* (tests) ;
  - rapport §4 (rien n'est traité dans lepton en ENV-39, PA-63 Q13).
- ENV-40 :
  - spécification, partie B ;
  - rapport §3, lignes M-* ;
  - rapport §4, ligne « miroirs » (PA-68).
- ENV-41 : rapport §2.1, §4 et §5 ; fichier d'étape corrigé.

## Reste à faire dans l'étape
- [x] Rien.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Plan de session (audit, PA-63, spécification, PA-64) | utilisateur (plan accepté) | oui (journal) |
| PA-63 Q1-Q16 (dont Q9 : le greffon porte ses projections, écart au principe du 2026-11-04 ; 9a `.scion/` complet ; 9b projections seules ; 10a `.scion.mirrors` à côté de la source) | utilisateur | oui |
| PA-64 : spécification validée telle quelle, y compris les précisions de rédaction hors PA-63 | utilisateur | oui |
| PA-64 : corriger ENV-39 à ENV-41 dans cette étape | utilisateur | oui |
| PA-64 : fusions et push (lepton-tools, seed.scions) | utilisateur | oui |
| Noms de clé (`tiers stm32f4xx-hal-driver`, `tiers cmsis-device-f4`…), shelf `tiers`, URL amont dans les cas du §2 | proposition non validée (PA-69, PA-68) | non (rapport §2) |
| Fichiers de tests proposés `tests/test_projection.py`, `tests/test_mirror.py` et noms des cas du §3 | proposition non validée (ENV-39, ENV-40) | non (rapport §3) |
| Exemple de clé périmé dans la skill `lepton-rootstock` (`lepton@bsp::nucleo-f429zi`) à corriger | proposition non validée (ENV-41) | non (rapport §4) |
| Sort fonctionnel de `RadioIsChannelFree` neutralisée (ENV-37) | à poser à l'utilisateur hors étape | oui (prochaine action) |

## Pièges rencontrés
- Le fichier `DEVENV-STATUS.md` dépasse 190 Ko : le lire par sections (`grep -n '^#'`, puis `sed -n`).
- `git tag --contains 3c77349` dans `cmsis_device_f4` est vide : le CMSIS device F4 ne peut être
  épinglé que par commit (P-V1).
- Le volume du Mac ne distingue pas la casse : `[ -L trunk/<chemin> ]` réussit aussi sur une casse
  fausse. Les listes attendues du WL tiennent leur casse des classements d'ENV-37 (`git show`,
  sensible à la casse).
- Un fichier amont porte un blanc dans son nom (`_htmresc/Add button.svg`) : on ne peut le désigner
  que par un joker (P-F2).
- lepton lit lui-même `.scion.grafted.list` et `.scion.sources.list` (`lepton/rootstock.py`). Une
  seconde graine en 5ᵉ colonne bloquerait `seed_dot()`, d'où la 6ᵉ colonne du porteur (P-P3).

## Critères de validation
- [x] PA-63 et PA-64 tranchés et consignés.
- [x] Chaque cas d'épreuve F4, F7, WL est écrit dans le format (§2) ; ce qui reste hors format est
      au §5.
- [x] Chaque règle de la spécification a au moins un cas de test nommé au §3 du rapport.
- [x] Aucun fichier de `scion/` ni de `tests/` modifié dans `<SEED_SCIONS>`
      (`git diff --stat master -- scion tests` vide).
- [x] Document dans `<SEED_SCIONS>` : `grep -i lepton` → 0.

## Reprise
Commande ou première action de la session suivante :
```
démarre la session   # ENV-39 : lire cette passation, la spécification (partie A), le rapport env-38 §2.1, §3, §4, puis PA-65
```
