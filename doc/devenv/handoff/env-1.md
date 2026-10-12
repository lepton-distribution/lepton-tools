# Passation ENV-1 — Levée des risques éditeur — session du 2026-10-12

## Statut
terminée — essais réalisés, rapport `rapports/env-1-essais.md` rédigé, PA-1 tranché.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `devenv/env-1` (non fusionnée ; `main` = df8e5dc, fusion locale de `devenv/env-0`) | commit `devenv(env-1): essais, PA-1, état et passation` | oui |
| clone noyau `depots/lepton/original/master` | `master` | 6b62af5 Merge branch 'migration/etape-10' | oui (non touché) |
| seed.scions (`~/lepton-tools-dev/seed.scions`) | `master` | e0adb2c | non touché |

Aucun push.

## Fait pendant la session
- Fusion locale `devenv/env-0` → `main` (df8e5dc), branche `devenv/env-1`.
- Installés : extensions VSCodium clangd 0.6.0, CMake Tools 1.24.42, Cortex-Debug 1.13.0-pre6
  (`codium --install-extension`) ; clangd 21.1.8 (`sudo port install clang-21`, par l'utilisateur).
- Montage d'essai sous `~/lepton/build/essais-env1/` : constructions `sans-prefixe/` et
  `avec-prefixe/` (preset `qemu-mps2-an386-embos`), copie jetable `rootstock/`, espaces
  `espaces/{1-trunk-seul,2-multi-racines,3-sauvegarde-copie}.code-workspace`.
- Essais GDB en ligne de commande (9 cas + contrôle MI), essais LSP clangd (Apple 17 puis LLVM 21),
  essais GUI G1 à G5 relevés par l'utilisateur. Résultats et synthèse : `rapports/env-1-essais.md`.
- Contrôle final : `find ~/lepton/trunk -type f ! -name .scion.grafted.list` vide ; clone noyau
  propre.

## Reste à faire dans l'étape
- Rien. Nettoyage facultatif, sur accord : `~/lepton/build/essais-env1/` (copie jetable du
  rootstock, constructions d'essai, cache clangd). La copie jetable contient la modification FIC-5
  dans son clone ; elle ne doit pas être réutilisée.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Fusion locale de `devenv/env-0` dans `main`, `devenv/env-1` depuis `main` | utilisateur | oui |
| Essais en mode mixte (CLI Claude, GUI utilisateur) | utilisateur | oui |
| clangd LLVM via MacPorts | utilisateur | oui |
| PA-1 : ouverture par le trunk | utilisateur | oui |
| PA-1 : clangd LLVM, `--compile-commands-dir` hors trunk, `--background-index`, `--query-driver` | utilisateur | oui |
| PA-1 : pas de `-ffile-prefix-map`, écart « onglet clone à l'arrêt » accepté en phase 1 | utilisateur | oui |
| Pistes pour éviter l'ouverture par les clones en ENV-9 (`files.exclude`, `git.scanRepositories`) | proposition non validée (non essayée) | non |
| Réécriture des chemins de pile clone → trunk par l'extension (ENV-12) | proposition non validée (non essayée) | non |
| Cortex-Debug stable plutôt que la pré-version servie par Open VSX (à trancher en PA-10) | proposition non validée | non |

## Pièges rencontrés
- `grep -r` ne suit pas les liens du trunk → aucun résultat → utiliser `grep -R`.
- clangd : F12 renvoie la déclaration `extern` locale tant que l'index de fond n'est pas prêt
  (> 180 s au premier lancement sur ce preset).
- GDB : `fullname` (MI) est toujours le chemin réel (clone), même pour un point d'arrêt posé via le
  trunk ; Cortex-Debug ouvre ce chemin à l'arrêt et n'a pas de `sourceFileMap`.
- Avec `-ffile-prefix-map` sans `substitute-path` : « No source file named … » et, dans l'éditeur,
  « The editor could not be opened because the file was not found ».
- QEMU lancés en série sur le même port gdbstub : « Address already in use » → un port par essai.
- `timeout` absent sur macOS.
- Open VSX sert Cortex-Debug en pré-version (1.13.0-pre6).

## Critères de validation
- [x] Rapport `env-1-essais.md` : pour chaque essai, versions, procédure, résultat observé.
- [x] Aucun fichier régulier ajouté au trunk réel (`find trunk -type f ! -name .scion.grafted.list` vide).
- [x] PA-1 tranché et consigné.

## Reprise
```
cd /Users/cle_d_anton/lepton-tools-dev/lepton-tools && claude
# puis : « Démarre la session sur l'étape indiquée dans DEVENV-STATUS » (ENV-2)
```
