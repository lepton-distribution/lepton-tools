# ENV-12 lot 3 — F2, F3, F4, bilinguisme (2026-10-20)

Session Mac Intel, mode mixte (actions de l'éditeur par l'utilisateur, terminal et contrôles par
Claude). Rootstock d'essai `~/lepton-tools-dev/essais/env-11/qemu` (graine `env11`, an386,
freertos), VSCodium 1.135.06055, extension 0.2.0, lepton 0.1.0 (`devenv/env-12`).

## 1. Réalisé

| Élément | Contenu | Commit |
| --- | --- | --- |
| lepton | `file owner PATH [--json]`, `file add --adopt`, `graft --path`, champ `stem` de `seed status --json`, remontée au-delà des répertoires sans feuille | c80f525 |
| lepton (essai) | `check` contrôle le trunk ; filtre de la tâche « lepton : vérifier » élargi à tout fichier | commit de clôture du lot |
| Extension 0.2.0 | `watch.ts` (F2, F3), `clangd.ts` (F4), `runner.ts` (file unique), `batch.ts` ; bilinguisme `vscode.l10n` | 857754e, corrections de l'essai au commit de clôture |
| Installation | `MS-CEINTL.vscode-language-pack-fr@1.131.0` ; `"locale": "fr"` dans `~/.vscode-oss/argv.json` | 3e commit du lot |

Interface : `rapports/env-8-interface.md` §12.

## 2. Essais

| # | Fonction | Action | Résultat |
| --- | --- | --- | --- |
| 1 | Bilinguisme | Installation (2 changements puis 0), redémarrage de VSCodium | Interface et palette « Lepton : … » en français |
| 2 | Activation | Ouverture de l'espace | Canal « Lepton » : observation de 5 greffons et du trunk ; base clangd observée |
| 3 | F2 | `echo > clone/f2_terminal.c` au terminal | Lien dans le trunk, une regreffe |
| 4 | F2 | Répertoire + 3 en-têtes en rafale | Une seule regreffe (4 chemins) |
| 5 | F2 | Suppression d'un fichier, puis d'un répertoire | Liens retirés ; le répertoire seul est remonté par l'observateur |
| 6 | F2 | `git checkout` d'une branche à fichier en plus, retour, suppression de la branche | Lien présent / absent selon la branche ; une regreffe par checkout ; clone propre |
| 7 | F2 | `CMakeLists.txt` créé dans le clone | Regreffe + reconfiguration des 4 répertoires `build/*` ; un `.c` : aucune reconfiguration |
| 8 | F3 a | « Nouveau fichier » dans le BSP (trunk), texte saisi, enregistré | Fichier dans le clone du BSP, lien dans le trunk, onglet conservé |
| 9 | F3 b | « Nouveau dossier » puis « Nouveau fichier » dedans | Propriétaire = BSP (remontée au-delà du répertoire vide) |
| 10 | F3 c | « Nouveau fichier » dans `kernel/dev/` | Liste des candidats ; `qemu-mps2` choisi : fichier dans la famille |
| 11 | F3 d | « Nouveau fichier » à la racine du trunk, Échap | Fichier laissé (régulier) ; message rangé seul dans le centre de notifications → corrigé (§3, D-a) |
| 12 | F3 d | Tâche « lepton : vérifier » | Après correction (§3, D-b) : erreur « lepton check » sur `trunk/f3_racine3.txt` dans *Problèmes* |
| 13 | F4 | Changement de preset debug → release (configuration seule) | « …/compile_commands.json a changé : clangd relancé » ; base active = release |
| 14 | F4 | F12 sur `__KERNEL_HEAP_SIZE` dans `heap.c` ouvert | Avant correction : `kernelconf.h` même après modification et construction (§3, D-c) ; après relance manuelle : `build/env11-release-qemu/generated/board/kernel_mkconf.h` |
| 15 | F4 | Après correction : `build/env11-release-qemu` supprimé, debug puis release, F12, construction, F12 | `kernelconf.h` (en-tête absent), puis relance « 2 en-tête(s) créé(s) … » et `…/env11-release-qemu/generated/board/kernel_mkconf.h` sans réouverture |

## 3. Défauts trouvés et corrigés pendant l'essai

| Id | Constat | Correction | Décision |
| --- | --- | --- | --- |
| D-a | Canal « Lepton » : JSON complet de `seed status --json` recopié à chaque rafraîchissement, message de clangd noyé | Sortie standard des appels `--json` gardée hors du canal | — |
| D-b | Fichier régulier laissé dans le trunk : bloque toute regreffe (`scion graft` refuse) ; signalé par `seed status` seul, alors que le message annonçait `lepton check` (affirmation inexacte de Claude, aussi dans la question d'ouverture) | `lepton check` contrôle le trunk ; filtre de la tâche élargi (il ne retenait que `.json` / `.xml`) ; message « regreffe bloquée » | utilisateur |
| D-c | clangd relancé à la configuration ne relit pas un en-tête généré apparu ensuite (préambule construit avec `#include` introuvable) | Relance aussi à la création d'un en-tête sous les répertoires `directory` de la base active ; une construction sans changement ne recrée pas l'en-tête (inode et date inchangés) | utilisateur |
| D-d | Avertissement « reste un fichier régulier » rangé seul ; avec bouton aussi : VSCodium 1.135 ne garde affichée qu'une notification **d'erreur** munie d'un bouton (`get sticky()`) | Notification d'erreur + « Supprimer du trunk » | utilisateur (pas de boîte modale) |

## 4. Observations (non corrigées)

| Id | Constat | Proposition |
| --- | --- | --- |
| L3-1 | Suppression d'un répertoire qui contenait un `CMakeLists.txt` : l'observateur ne remonte que le répertoire, regreffe sans reconfiguration CMake | Documenté (§12) ; `lepton graft` complet si besoin |
| L3-2 | Le greffon `building` (génération de scion, sans manifeste) est observé comme les autres | Aucune regreffe parasite constatée ; laissé |
| L3-3 | La notification d'erreur persistante a disparu quand la fenêtre principale a été déplacée ; la cloche du centre de notifications n'est pas visible dans la barre d'état de l'utilisateur | Laissé (décision : notification conservée) ; `lepton check` et *Problèmes* restent le filet |
| L3-4 | Suppression d'un lien du trunk depuis l'explorateur : aucun observateur (F3 ne traite que les créations), le lien revient à la regreffe suivante | À examiner avec F6 / lot 6 |
| L3-5 | La commande de palette « Lepton : vérifier » ne remplit pas *Problèmes* (la tâche seule le fait) | Lot 4 (F5) |
| L3-6 | Une création faite par l'extension (adoption) déclenche aussi une regreffe par l'observateur F2 (redondante, sans effet) | Laissé |

## 5. Contrôles

- `pytest` : voir `DEVENV-STATUS.md` §Journal (lot 3).
- `npm test` : 11 verts (regroupement, file, arguments de clangd, répertoires de la base,
  lepton.ts, complétude des traductions).
- `scripts/bout-en-bout.sh` vert ; `~/lepton` inchangé.
- `shellcheck scripts/install-vscodium.sh` sans remarque ; installation Mac : 2 puis 0 changement.
