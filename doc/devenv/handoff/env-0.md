# Passation ENV-0 — Cadrage — session du 2026-10-12

## Statut
bloquée : le hook `proteger-trunk.py` n'est pas chargé, car la session a été lancée depuis
`~/lepton-tools-dev` au lieu de `<LEPTON_TOOLS>`. Arrêt en tâche 5, comme le prévoit le fichier d'étape.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools (`~/lepton-tools-dev/lepton-tools`) | `devenv/env-0` (depuis `main` 0a11458) | commit de passation `devenv(env-0): état et passation` | oui après commit |
| clone noyau `~/lepton/depots/lepton/original/master` | `master` | 6b62af5 Merge branch 'migration/etape-10' | oui |
| seed.scions (`~/lepton-tools-dev/seed.scions`) | `master` | e0adb2c README: document the installation routes | oui (clone neuf, tags 0.1.2 à 0.5.0.1) |

## Fait pendant la session
- PA-0 tranché par l'utilisateur ; valeurs consignées dans `DEVENV-STATUS.md` §Emplacements et §Décisions.
- `git init -b main` dans lepton-tools, puis commit 0a11458 « devenv: plan de réalisation » et
  création de la branche `devenv/env-0`. Ajouts : `.gitignore` (`.DS_Store`) et
  `doc/devenv/rapports/.gitkeep`. Aucun distant.
- Clone neuf de `seed.scions` depuis GitHub.
- Tâche 3 conforme : `scion version` donne 0.5.0.1 ; `rootstock-information` indique 2 scions
  greffés ; `kal.h` est résolu (`trunk/sys/root/src/kernel/core/kal.h`) ; le trunk ne contient aucun
  fichier réel ; le clone noyau est propre.
- Tâche 4 : versions consignées dans `DEVENV-STATUS.md` §Versions. cmake 3.31.12 ≥ 3.19.
  arm-none-eabi-gcc (Arm GNU Toolchain, `~/opt`) et python3 (python.org) ne viennent pas de
  MacPorts ; tous les autres outils viennent de `/opt/local/bin`.
- Tâche 5 : le `Write` de `~/lepton/trunk/zz-test-hook-env0.txt` a été **accepté**. Le fichier a été
  supprimé aussitôt et le trunk contrôlé ensuite (aucun fichier réel). Appelé directement avec un
  JSON PreToolUse, le script refuse bien l'écriture (exit 2) : il fonctionne, c'est sa configuration
  qui n'est pas prise en compte.

## Reste à faire dans l'étape
- [ ] Tâche 5 : relancer Claude Code depuis `<LEPTON_TOOLS>`, refaire le test et constater le refus.
- [ ] Tâche 6 : construction QEMU de référence (relever le preset par `cmake --list-presets` dans
  le trunk), dans `~/lepton/build/<preset>`, puis capture de l'oracle dans
  `doc/devenv/rapports/oracles/env-0/<preset>/` (skill `lepton-oracle`).
- [ ] Clôture : statut ENV-0 « terminée », prochaine action ENV-1 ou ENV-2.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Emplacements, branche noyau `master`, échange Mac/VM par distant GitHub (PA-0) | utilisateur | oui |
| `.gitignore` limité à `.DS_Store` | proposition non validée | non |
| Ancien clone `~/MyDocuments/temp/seed/seed.scions` (sans tags) laissé intact et inutilisé | proposition non validée | non |

## Pièges rencontrés
- Hook inactif → Claude Code lancé dans le dossier parent `~/lepton-tools-dev` : le fichier
  `.claude/settings.json` du dépôt n'est pas lu, et `${CLAUDE_PROJECT_DIR}` désigne un autre dossier
  → toujours lancer `claude` depuis `<LEPTON_TOOLS>`.

## Critères de validation
- [x] PA-0 tranché ; valeurs recopiées dans `DEVENV-STATUS.md` §Emplacements.
- [x] `lepton-tools` est un dépôt git, branche `devenv/env-0`, arbre propre.
- [x] Contrôles de la tâche 3 conformes.
- [x] Versions de la tâche 4 consignées dans `DEVENV-STATUS.md` §Versions.
- [ ] Hook vérifié (refus constaté).
- [ ] Construction QEMU de référence réussie ; commande consignée ; oracle capturé.

## Reprise
```
cd /Users/cle_d_anton/lepton-tools-dev/lepton-tools && claude
# puis : « Démarre la session sur l'étape indiquée dans DEVENV-STATUS » (reprise ENV-0, tâche 5)
```
