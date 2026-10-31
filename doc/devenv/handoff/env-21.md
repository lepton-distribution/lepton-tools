# Passation ENV-21 — Validation Debian groupée — session du 2026-10-31

## Statut
terminée — ordre R21-1 conforme sur Debian 13.7 (C1-C5, C7 ; C6 accepté avec réserve E-1) ;
6 rootstocks d'essai du Mac regreffés ; dernière étape du plan.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` (fusion `--no-ff` de `devenv/env-21`, poussées toutes deux) | commit d'état et passation, puis « Fusion de devenv/env-21 » | oui |
| lepton-tools `devenv/env-21-debian` (VM) | poussée, fusionnée dans `devenv/env-21` | 36d7a1f devenv(env-21-debian): validation Debian groupée ENV-17 à ENV-20 (R21-1) | — |
| clone noyau `depots/lepton/original/master` | `master` 40d7197 = origin | Fusion de devenv/env-20 (inchangé) | oui |
| graine `depots/lepton-seed.scions/original-tree` | `original-tree` 15740f9 = origin | inchangée | oui |
| `<ROOTSTOCK>` | inchangé (3941 liens, 14 greffons) | | oui |
| Rootstocks d'essai Mac | `env-9`, `env-11/{f429zi,qemu,qemu-gra2,wl55jc1}`, `env-13-vierge` regreffés ; `.scion.trunk.tolerated` ajouté dans chacun | noyau 40d7197, greffons aux têtes publiées | oui |
| VM | `~/lepton-tools-dev/essais/env-21-debian` conservé ; `env-15-debian`, `~/env-15-journaux` supprimés | | — |

## Fait pendant la session
- Tâche 1 : contrôle `.DS_Store` (0) ; têtes publiées relevées (`consignes/env-21-debian.md` §1) ;
  écarts Mac `env-14-apres` → `env-20-apres` calculés, ce qui donne l'attendu C4 ; consigne bb0702f ;
  PA-29 ; push de `devenv/env-21` ; ordre R21-1.
- Tâche 2 : R21-1 (ACCUSÉ, 4 AVANCEMENT, FIN-SUCCÈS) : `rapports/env-21-debian.md`, oracle
  `rapports/oracles/env-21-debian/` (host + 16).
- Tâche 3 : regreffe des 6 rootstocks d'essai (`rapports/env-21-mac.md` §3) : 0 cassé, 0 régulier ;
  `check`/`generate` 0 (`qemu-gra2` : 1, attendu) ; `env-13-vierge` = trunk de `<ROOTSTOCK>`.
- Tâche 4 : comparaisons recalculées sur l'oracle poussé (`rapports/env-21-mac.md` §2bis) ; PA-30 ;
  fusions, push.

## Reste à faire dans l'étape
- Aucune tâche du fichier d'étape.
- Hors étape : le plan n'a plus d'étape ; points ouverts dans la « Prochaine action » de
  `DEVENV-STATUS.md`.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-29 : consigne validée telle quelle ; C7 accordé ; push de `devenv/env-21`, ordre R21-1 | utilisateur | oui |
| Tâche 3 limitée aux 6 rootstocks d'ENV-14 (`env-11/bout-en-bout` exclu) | utilisateur | oui |
| Parade E2 : `.scion.trunk.tolerated` (`.DS_Store`, `._*`) dans les 6 rootstocks d'essai | utilisateur | oui (journal) |
| `env-13-vierge` : `git pull --ff-only` de la graine, puis `graft-update` | utilisateur | oui (journal) |
| `qemu-gra2` : BSP an386 retiré à nouveau par `graft-remove` sans `--purge` | proposition appliquée (reprise de la décision d'ENV-14) | oui (journal) |
| PA-30 : C6 accepté avec réserve E-1 ; fusions ; push | utilisateur | oui |
| C4 lu contre `env-14-debian` avec les écarts Mac `env-14-apres` → `env-20-apres` (consigne §8) | proposition validée au PA-29 | oui |
| Régénérer la graine de projet avant le relevé de C6 dans les prochaines consignes | proposition de la session VM, retenue au PA-30 | oui |

## Pièges rencontrés
- `scion graft-update` ne met pas à jour le dépôt de la graine (`sync` lit la graine locale) : un
  rootstock de la graine de référence ne reçoit pas les greffons ajoutés → `git -C <graine> pull
  --ff-only`, puis `graft-update`.
- Les rootstocks d'avant 0.5.2.0 n'ont pas de `.scion.trunk.tolerated` : les `.DS_Store` du Finder
  dans le trunk bloquent le dégreffage → fichier écrit à la racine du rootstock (motifs `.DS_Store`,
  `._*`), supprimés au `graft-update`.
- `sync` réinscrit le BSP an386 de `qemu-gra2` à chaque `graft-update` (essai GRA-2) → `graft-remove`
  sans `--purge`.
- VM : le classifieur de permissions refuse `rm -rf` à la session, malgré l'accord du PA-29 →
  commande lancée par l'utilisateur (E-2).
- C6 : un fichier généré longtemps avant le relevé fausse la comparaison avant/après → régénérer
  d'abord (E-1).
- zsh (Mac) : `PIPESTATUS` n'existe pas (`pipestatus`) ; les consignes VM restent en bash.

## Critères de validation
- [x] PA-29 et PA-30 tranchés et consignés.
- [x] `FIN-SUCCÈS R21-1` vérifié par la session Mac ; C1 à C7 conformes (C6 avec réserve E-1 acceptée).
- [x] Rootstocks d'essai regreffés : 0 lien cassé, 0 fichier régulier ; `check` code 0 (`qemu-gra2` : 1 attendu).
- [x] `DEVENV-STATUS.md` §Versions : lepton et scion sur Debian relevés.

## Reprise
Commande ou première action de la session suivante :
```
démarre la session   # skill devenv-session ; aucune étape planifiée : révision du plan, voir « Prochaine action »
```
