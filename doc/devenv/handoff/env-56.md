# Passation ENV-56 — scion : répertoires laissés par un clonage en échec (D14) — session du 2026-11-13

## Statut
Terminée (2026-11-13). Depuis scion 0.6.3.1, un clonage en échec ne laisse plus de répertoire
dans `depots/`. PA-99 et PA-100 sont tranchés ; tout est fusionné et poussé (PA-P).

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| seed.scions | `master` | d650414, fusion de `devenv/env-56` (95d55eb tests, 54fc27b gitops, b8767dc miroir, c51ee1a 0.6.3.1) ; tag annoté `0.6.3.1` sur c51ee1a ; `master`, branche et tag poussés | oui |
| clone noyau `depots/lepton/original/master` | `master` | ed2a41f, fusion de `devenv/env-56` (79354a0 : `SCION_REF` 0.6.3.1) ; `master` et branche poussés | oui |
| lepton-tools | `devenv/env-56` (depuis `main` 298de7a), fusionnée `--no-ff` dans `main`, les deux poussées | commit « état et passation » au-dessus de d1028d4 (HORS-PLAN), edcdc5f (rapport), 01d4991 (`SCION_REF`), d9b48b9 (audit) | oui |
| autres | — | non touchés (graine `original-tree` 15740f9, familles, BSP, miroirs) | — |

Outils au Mac :
- scion 0.6.3.1 (pipx `git+file://<SEED_SCIONS>@0.6.3.1`, 10 modules identiques au tag) ;
- lepton 0.1.0, non réinstallé (seul un commentaire change) ; `lepton --version` donne
  `scion 0.6.3.1 (requis ≥ 0.6.2.0)` ;
- extension 0.5.2, inchangée.

La VM a encore scion 0.6.3.0.

Hors dépôt :
- supprimés au PA-100 par `scripts/supprimer-essai.sh` : `essais/env-56-essai`, `env-56-fixture`,
  `env-56-releves`, `env-56-succes-0630`, `env-56-succes-0631`, `env-56-venv` ;
- jamais créé : `essais/env-56-absent.git` (dépôt absent par construction) ;
- `<ROOTSTOCK>` n'est pas regreffé. Son trunk n'a aucun lien cassé, et seulement les 7 `.DS_Store`
  tolérés, datés du 12 novembre.

## Fait pendant la session
- Audit, `rapports/env-56-scion.md` §1 :
  - trois lieux : R1 `gitops.clone` (clés ordinaires, graine distante de `seed-add`), R2
    `gitops.clone_partial` (clés projetées), R3 `mirror.sync_one` (dépôt de travail d'un miroir,
    jusqu'à 10 répertoires laissés) ;
  - git 2.50.1 retire la destination d'un clone en échec, jamais ses parents, et garde une
    destination préexistante vide (§1.2) ;
  - essais « avant » : e01 à e06 sur une copie d'`essais/env-11/qemu` (`essai.sh`), f01 à f12b
    sur des rootstocks bâtis comme les fixtures de scion (`fixture.py`, `mirror-sync --dry-run`
    seul) ;
  - clones gardés exprès, hors D14 : f06 (checkout en échec), f08 (P-V1), f12a (M-C6) ;
  - spécification : aucune règle sur le sort de ces répertoires ; lepton : aucun effet.
- PA-99 : propositions du §1.8 retenues (décision de l'utilisateur).
- seed.scions :
  - tests d'abord, 95d55eb : `tests/test_failed_clone.py`, 16 tests, dont 8 en échec sur 0.6.3.0
    (`rapports/env-56-scion/tests-avant-correction.txt`) ;
  - 54fc27b : `gitops.clone_parents`, gestionnaire de contexte (relevé des ancêtres absents,
    `rmdir` du plus profond au plus haut en cas d'exception, `log.debug`) ;
  - b8767dc : le miroir passe par `clone_parents` ;
  - c51ee1a : 0.6.3.1, `CHANGELOG.md`, `README.md` §Utilisation, test de version ;
  - 298 tests verts (1 sauté : `test_network`) ; NF-2 : 0.
- Essais avec la branche (venv), §4 :
  - aucun résidu ; préexistants gardés ; stdout, stderr et codes identiques à 0.6.3.0 ;
  - ligne sous `-v` relevée (`apres/e07-verbeux.err`) ;
  - `seed add` F7 réussi puis `seed remove` (`succes.sh`, deux copies neuves) : identiques à
    0.6.3.0.
- Version et références, §5 :
  - tag local, puis pipx ;
  - `SCION_REF` 0.6.3.1 dans lepton-tools (01d4991) et dans le clone noyau (79354a0) ;
  - `SCION_MIN_VERSION` inchangé ;
  - `pytest` de lepton-tools : 453 verts avec 0.6.3.1.
- Pas d'oracle (§6) : l'arbre composé ne change pas.
- `HORS-PLAN.md` : D14 traité ; D18 ajouté (f06 : clone gardé sans que le message le dise).
- PA-100 : essais supprimés ; publication des trois dépôts.

## Reste à faire dans l'étape
- Rien. La validation Debian se fait en ENV-57 : installer d'abord 0.6.3.1 sur la VM (C1).

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Plan de session ; essais sur `essais/env-56-essai` et `essais/env-56-fixture` ; aucun `graft-update` | utilisateur (plan approuvé) | oui |
| PA-99 : `rmdir` des seuls répertoires vides créés par l'appel ; R1, R2, R3 ; clones gardés exprès inchangés ; ligne sous `-v` ; `README.md` et `CHANGELOG.md`, spécification inchangée ; 0.6.3.1 ; `SCION_REF` relevé, `SCION_MIN_VERSION` inchangé ; D18 au hors-plan | utilisateur | oui |
| Comparaison du `seed add` réussi sur deux copies neuves (et non sur `env-56-essai`), parce que `seed remove` garde les clones tiers du porteur (P-P6) | session, mise en œuvre de la tâche 3 (rapport §4) | oui (rapport) |
| lepton non réinstallé par pipx (code inchangé, commentaire seul) | session (rapport §5) | oui (rapport) |
| PA-100 : tous les essais supprimés ; fusions et pushs dans l'ordre seed.scions (tag compris), noyau, lepton-tools | utilisateur | oui |

## Pièges rencontrés
- Le lanceur pipx de scion commence par `#!/bin/sh`. Pour trouver le Python du venv :
  `dirname "$(realpath "$(command -v scion)")"`/python.
- `fixture.py` : le chemin du dépôt de travail d'un miroir reprend celui de l'URL sans le `/`
  initial. Il faut le normaliser aussi (`<B>`), sinon le chemin absolu de l'utilisateur entre
  dans les relevés.
- `seed remove --purge` d'un porteur garde les clones de ses clés projetées. Pour comparer deux
  versions de scion sur un `seed add` réussi qui reclone, il faut deux copies neuves.
- `essai.sh` retire les résidus de 0.6.3.0 par `rmdir` après chaque cas, et défait ce qu'il a
  préparé. Les états finaux se comparent au départ (`*.etat`).
- f09c compte 3 préexistants au lieu de 4 après la correction : il hérite du rootstock de f09b,
  qui ne laisse plus `depots/tiers/hal2`.
- Avant la correction, `test_existing_shelf_keeps_only_what_was_there` échoue aussi : le résidu
  s'ajoute au préexistant. C'est un cas de D14, pas un garde.

## Critères de validation
- [x] PA-99 et PA-100 tranchés et consignés.
- [x] Aucun nom propre à Lepton ajouté à scion : `git diff 0.6.3.0 -- scion tests | grep -ci '^+.*lepton'` → 0.
- [x] Tests de scion verts (298), dont les nouveaux : 8 en échec sur `master`, tous verts sur la branche.
- [x] Essai : aucun répertoire résiduel après chaque échec retenu ; répertoire préexistant gardé ;
      `seed add` réussi identique à 0.6.3.0.
- [x] Références de version conformes au PA-99.
- [x] `HORS-PLAN.md` : D14 marqué traité, avec renvoi au rapport.

## Reprise
Commande ou première action de la session suivante :
```
démarrer ENV-57 (skill devenv-session) : lire DEVENV-STATUS.md (Prochaine action), cette passation
et doc/devenv/etapes/ENV-57-*.md ; branche devenv/env-57 depuis main (lepton-tools) ; sur la VM,
installer scion 0.6.3.1 (C1) avant tout essai de D14
```
