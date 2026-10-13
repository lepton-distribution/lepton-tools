# Passation ENV-2 — Audit de l'existant — session du 2026-10-13

## Statut
terminée — six rapports d'audit et une synthèse rédigés, skill `lepton-cibles` complétée, PA-2 tranché (Q1 à Q8).

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `devenv/env-2` (non fusionnée ; `main` = e43a151, fusion locale de `devenv/env-1`) | commit `devenv(env-2): état et passation` | oui |
| clone noyau `depots/lepton/original/master` | `master` | 6b62af5 Merge branch 'migration/etape-10' | oui (non touché) |
| seed.scions (`~/lepton-tools-dev/seed.scions`) | `master` | e0adb2c | oui (non touché) |

Aucun push. Trunk : `find ~/lepton/trunk -type f ! -name .scion.grafted.list` vide.

## Fait pendant la session
- Fusion locale `devenv/env-1` → `main` (e43a151), branche `devenv/env-2`.
- Rapports (`doc/devenv/rapports/`) : `env-2-cmake.md`, `env-2-mklepton.md`, `env-2-cartes.md`,
  `env-2-scion.md`, `env-2-outillage.md`, `env-2-doc-portage.md` (lecture intégrale de `doc/BUILDING.md`,
  `doc/migration/` et des 37 passations du portage), `env-2-synthese.md` (PA-2 et §Périmètres validés).
- Skill `lepton-cibles` : plus aucun `<RELEVÉ ENV-2>` (commit 71bb429), chemins de doc corrigés.
- Lecture faite par sous-agents Explore (lecture seule), affirmations clés vérifiées par sondage dans
  les sources ; aucune construction, aucun QEMU, aucun OpenOCD lancé.

## Reste à faire dans l'étape
- Rien.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Fusion locale de `devenv/env-1`, `devenv/env-2` depuis `main` | utilisateur | oui |
| Q1 : périmètres ENV-4 à ENV-7 validés (`env-2-synthese.md` §Périmètres validés) | utilisateur | oui |
| Q2 : greffon commun par famille (couche Lepton + pilotes ST + CMSIS device) ; BSP = horloge (`SystemInit`) et GPIO de la carte | utilisateur | oui |
| Q3 : règle du portage — démarrage générique Cortex-M dans le greffon noyau, vecteurs par MCU dans le greffon famille, liaison OBJECT (amende la décision 4 de la spécification) | utilisateur | oui |
| Q4 : deux BSP F4, `nucleo-f429zi` et `nucleo-f439zi` | utilisateur | oui |
| Q5 : an500, F746, SAMD21 construisibles pendant ENV-5/ENV-6 | utilisateur | oui |
| Q6 : CMake minimum 3.24 | utilisateur | oui (§Versions) |
| Q7 : critère NF-2 d'ENV-7 limité au code fonctionnel | utilisateur | oui |
| Q8 : ENV-3 ensuite | utilisateur | oui |
| `SPECIFICATION.md` décision 4 à amender en conséquence de Q2/Q3 (non fait : fichier réservé, à faire en ENV-3 avec accord) | proposition non validée | non |
| Greffons an500 / F746 / SAMD21 en ENV-6 ou transitoires ; place de `ld/mem`, mkconf, `user_kernel_mkconf.h`, cfg OpenOCD | ouvert, PA-7 | non |
| `<cpu freq>`, `<arch include_absolute_path>`, sort des 23 XML hérités | ouvert, PA-4 | non |

## Pièges rencontrés
- Lecture partielle de la doc du portage en première passe → synthèse fausse sur les empreintes
  mklepton (dites « à régénérer ») → lire `doc/BUILDING.md` et `doc/migration/` **avant** toute
  synthèse ; les empreintes `mklepton_empreintes.sha256` ne se régénèrent jamais sans décision.
- `BUILDING.md` est sous `doc/`, pas à la racine du clone.
- Plusieurs documents du portage sont périmés (`README.md`, `ajout-coeur.md`, `mklepton-ref.md`,
  `mass-compile.md`, `audit-iar.md`) : voir `env-2-doc-portage.md` §4.
- zsh : `echo =====` échoue (« ==== not found ») → éviter ou passer par `bash`.

## Critères de validation
- [x] Cinq rapports présents (six, avec la lecture de la doc), chaque affirmation appuyée par un chemin ou une commande.
- [x] Plus aucun `<RELEVÉ ENV-2>` dans la skill `lepton-cibles`.
- [x] Clone noyau et `seed.scions` inchangés (`git status` propre).
- [x] PA-2 tranché et consigné.

## Reprise
```
cd /Users/cle_d_anton/lepton-tools-dev/lepton-tools && claude
# puis : « Démarre la session sur l'étape indiquée dans DEVENV-STATUS » (ENV-3)
# demander la base de devenv/env-3 (devenv/env-2 non fusionnée dans main)
```
