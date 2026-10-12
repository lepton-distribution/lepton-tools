# Passation ENV-0 — Cadrage — session du 2026-10-12 (session 2)

## Statut
terminée — tous les critères d'ENV-0 sont remplis : hook vérifié, oracle de départ capturé sur les
4 presets QEMU mps2-an386.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `devenv/env-0` (non fusionnée dans `main` 0a11458) | commit `devenv(env-0): état et passation`, précédé de 454833a (oracle) | oui |
| clone noyau `depots/lepton/original/master` | `master` | 6b62af5 Merge branch 'migration/etape-10' | oui |
| seed.scions (`~/lepton-tools-dev/seed.scions`) | `master` | e0adb2c README: document the installation routes | oui |

Aucun distant, aucun push.

## Fait pendant la session
- Session 1 (rappel) : PA-0 tranché, dépôt initialisé, seed.scions cloné, rootstock et versions
  vérifiés.
- Tâche 5 : le `Write` de `~/lepton/trunk/zz-test-hook-env0.txt` a été **refusé** par
  `proteger-trunk.py`, et aucun fichier n'a été créé.
- Tâche 6 : constructions neuves des presets `qemu-mps2-an386-{embos,freertos,embos-soft,freertos-soft}`
  dans `~/lepton/build/<preset>`. ctest est à 100 % sur chacun (18, 18, 14 et 14 tests).
- Oracles capturés dans `doc/devenv/rapports/oracles/env-0/<preset>/` : empreintes, sections,
  symboles, outils, `fumee.log`, `banc-kal.log`, `construction.log`. L'auto-comparaison de chaque
  oracle renvoie le code 0.
- Commandes exactes et table de synthèse : `doc/devenv/rapports/env-0-reference.md`.
- Trunk contrôlé en fin de session : aucun fichier réel. Clone noyau propre.

## Reste à faire dans l'étape
- Rien.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Emplacements, branche noyau `master`, échange Mac/VM par GitHub (PA-0) | utilisateur | oui |
| Oracle sur les 4 presets an386 | utilisateur | oui |
| Suppression puis reconstruction des sorties de migration dans `~/lepton/build/` | utilisateur | oui |
| Chemin `oracles/env-0/<preset>/` (fichier d'étape), plutôt que `env-0-avant/` (skill lepton-oracle) | utilisateur | oui |
| ENV-1 avant ENV-2 | utilisateur | oui |
| Sourcer `scripts/lepton-env.sh` du clone noyau avant de construire (procédure du portage, prescrite par le message d'erreur CMake) | proposition non validée | non (consigné dans le rapport) |
| `.gitignore` limité à `.DS_Store` | proposition non validée | non |
| Ancien clone `~/MyDocuments/temp/seed/seed.scions` laissé intact | proposition non validée | non |
| Base de `devenv/env-1` (`main` ou `devenv/env-0`) | à demander | non |

## Pièges rencontrés
- Presets embOS : erreur « embOS introuvable : LEPTON_EMBOS_ROOT= » → l'environnement n'est pas
  défini → `source ~/lepton/depots/lepton/original/master/scripts/lepton-env.sh` avant `cmake`. Ce
  script n'est pas greffé dans le trunk.
- `ctest` renvoie 0 même s'il affiche « No tests were found!!! » → contrôler la ligne
  « 100% tests passed … out of N », et non le seul code de retour.
- Convention de chemin des oracles : la skill `lepton-oracle` utilise `<étape>-<avant|apres>`, le
  fichier ENV-0 utilise `env-0`. À harmoniser dans la skill, sur décision de l'utilisateur.

## Critères de validation
- [x] PA-0 tranché ; valeurs recopiées dans `DEVENV-STATUS.md` §Emplacements.
- [x] `lepton-tools` est un dépôt git, branche `devenv/env-0`, arbre propre.
- [x] Contrôles de la tâche 3 conformes.
- [x] Versions de la tâche 4 consignées dans `DEVENV-STATUS.md` §Versions.
- [x] Hook vérifié (refus constaté).
- [x] Construction QEMU de référence réussie ; commande consignée ; oracle capturé.

## Reprise
```
cd /Users/cle_d_anton/lepton-tools-dev/lepton-tools && claude
# puis : « Démarre la session sur l'étape indiquée dans DEVENV-STATUS » (ENV-1)
```
