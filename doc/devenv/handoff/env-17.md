# Passation ENV-17 — Cohérence de la documentation et des messages — session du 2026-10-31

## Statut
terminée — documents vivants (noyau, lepton-tools, skills) et messages CMake du noyau corrigés ;
binaires et images mklepton inchangés (oracle `env-17`, 14 presets).

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` (fusion `--no-ff` de `devenv/env-17`, poussées toutes deux) | commit d'état et passation, puis « Fusion de devenv/env-17 » | oui |
| clone noyau `depots/lepton/original/master` | `master` (fusion `--no-ff` de `devenv/env-17` : 350d914, 9ee9734 ; poussées toutes deux) | « Fusion de devenv/env-17 » | oui (`.DS_Store` ignorés par git seulement) |
| 7 greffons famille/BSP, graine `original-tree` | `master` / `original-tree`, inchangés | | oui |
| `<ROOTSTOCK>` trunk | regreffé (`lepton@original::tree`) | | oui : aucun fichier régulier, aucun lien cassé |

## Fait pendant la session
- Tâche 1 : audit, `rapports/env-17-coherence.md` §1-§5 (C-1 à C-17, M-1, M-2, arbitrages A-1 à
  A-4, reports H-1 à H-4, propositions en attente P-1 à P-7) ; PA-21.
- Tâche 2 : oracle `rapports/oracles/env-17-avant/` (`rejouer-oracle.sh`, host + 14 presets),
  conforme à `env-14-apres`.
- Tâche 3 : clone noyau 350d914 (`kernel.cmake` : message « bsp » sous
  `elseif(LEPTON_BOARD AND NOT LEPTON_BOARD_FAMILLE)`, « (étape 3) » retiré ;
  `lepton_greffons.cmake:303`), 9ee9734 (`BUILDING.md`, scripts d'installation, `CLAUDE.md`,
  `README.md`) ; lepton-tools 5a80a31 (README, extension, ORCHESTRATION §2, SPECIFICATION
  Apple Silicon), 9ced1e4 (skills), 7baa03e (oracles et rapport) ; regreffe après suppression de
  14 `.DS_Store` du trunk.
- Tâche 4 : `comparer-oracle.py` code 0 sur 14 presets ; mklepton identique ; fumée (E2) et banc
  KAL identiques ; message faux absent du journal de `nucleo-f429zi-embos` et de `host` ;
  `grep` rejoué sans occurrence (rapport §8) ; PA-22.

## Reste à faire dans l'étape
- Aucune tâche du fichier d'étape.
- Reporté, hors étape : H-1 (fichiers `*f439zi*` du BSP `nucleo-f429zi`, XML et `etc/` du F439)
  → ENV-20 ; H-2 (`debug/` du noyau, `cmake/boards/`, §5-§6 de `BUILDING.md`) → ENV-19.
- lepton non réinstallé (aucun code de lepton modifié) ; aucune validation Debian (ENV-21).

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-21 : C-1 à C-17, M-1 (condition), M-2 ; A-1 à A-4 selon le rapport ; P-1 à P-7 confirmées en bloc | utilisateur | oui |
| `.DS_Store` du trunk supprimés avant regreffe | utilisateur | oui |
| PA-22 : fusion dans `main` et `master`, push des deux branches et de `devenv/env-17` | utilisateur | oui |
| `ORCHESTRATION.md` §2 : distant de lepton-tools (« prévu » retiré), `seed.scions` en ENV-7 et ENV-15 (même nature que C-13, au-delà du texte validé) | proposition non validée séparément | non (rapport §7) |
| Commentaire explicatif ajouté au-dessus du message M-1 dans `kernel.cmake` | proposition non validée séparément | non (commit 350d914) |

## Pièges rencontrés
- `scion graft` refuse toute regreffe tant que le trunk contient un fichier régulier (Finder :
  `.DS_Store`) → les lister (`find trunk -type f ! -name .scion.grafted.list`), décider, puis
  regreffer. Ne pas ouvrir le trunk dans le Finder.
- Décompte d'occurrences fait à l'œil dans l'audit (9 au lieu de 10) → les remplacements par
  script vérifient le nombre exact avant d'écrire.
- zsh : `echo =====` interprété comme `=cmd` (rappel d'ENV-16).

## Critères de validation
- [x] PA-21 et PA-22 tranchés et consignés.
- [x] Toutes les corrections validées appliquées ; aucun rapport, passation ou `doc/migration/` modifié.
- [x] `comparer-oracle.py` code 0 sur 14 presets ; empreintes mklepton identiques.
- [x] Propositions en attente : chacune confirmée ou amendée dans `DEVENV-STATUS.md` §Décisions.

## Reprise
Commande ou première action de la session suivante :
```
démarre la session   # skill devenv-session ; ENV-18 (ou ENV-19), voir « Prochaine action »
```
