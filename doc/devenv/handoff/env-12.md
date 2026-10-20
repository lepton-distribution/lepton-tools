# Passation ENV-12 — Extension VSCodium (phase 2) — session du 2026-10-20

## Statut
en cours — PA-12 tranché ; lot 1 (F0 socle, F1 palette) fait et validé dans VSCodium ; lots 2 à 6
restent.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `devenv/env-12` (depuis `main` 361b337) | `devenv(env-12): état et passation (lot 1)` ; avant : 40e0c2a commandes de palette, ed960cb squelette | oui (`extension/node_modules`, `out/`, `*.vsix` ignorés) |
| clone noyau `~/lepton/depots/lepton/original/master` | `master` 16a331b | non touché | oui |
| seed.scions | `master` f1d1f3c (tag 0.5.1.1) | non touché | oui |
| VSCodium (Mac) | — | `lepton-distribution.lepton@0.1.0` installé depuis `extension/lepton-0.1.0.vsix` | — |

Rien n'est poussé (PA-P).

## Fait pendant la session
- PA-12 présenté (fonctions F0-F9, coûts) et tranché : `DEVENV-STATUS.md` §Décisions (2026-10-20).
- O5 expliqué et décidé : XML mklepton du projet dans le greffon local `project-<projet>` de la
  graine, lot 2.
- `extension/` : `package.json` (15 commandes « Lepton : … », menu de l'explorateur, réglage
  `lepton.path`), `src/lepton.ts` (seul point d'appel, sous-processus, codes 0/1/2/130,
  annulation SIGINT), `src/commands.ts` (graine, greffons, fichiers, répertoires, regreffe,
  vérification, génération), `test/lepton.test.ts`, `README.md`.
- `npm ci && npm test` : 4 tests verts ; `npm run package` : `lepton-0.1.0.vsix` (7 fichiers,
  8 Ko) ; `codium --install-extension` ; `codium --list-extensions --show-versions` le liste.
- Essai par l'utilisateur dans `essais/env-11/qemu/env11.code-workspace` : 15 commandes visibles ;
  `seed status`, `check` (5 fichiers conformes), `graft` (code 0, 4 répertoires reconfigurés) ;
  `file add` depuis le menu d'un dossier du trunk (fichier dans le clone du BSP, lien visible) puis
  `file remove` (lien et fichier disparus) ; liste des greffons de `seed status --json` affichée.
- `pytest` de lepton : 140 verts (aucun changement de lepton).

## Reste à faire dans l'étape
- [ ] Lot 2 — O5 + F7 (lepton seul) : forme exacte soumise à l'utilisateur avant implémentation
  (emplacement `<graine>/project/scion/…`, champ de graine et schéma, `seed new` copie le XML de
  référence du noyau, `generate` → `LEPTON_MKCONF`, `check`, `scion new/remove --type application`
  déclare / retire l'application, migration des rootstocks d'essai ; `lepton seed config add`) ;
  `pytest`, bout en bout.
- [ ] Lot 3 — F2 regreffe automatique (observateur temporisé), F3 redirection des créations du
  trunk (lepton : propriétaire en JSON, remplace le couplage au texte `--scion`), F4 relance de
  clangd (O10, R1) ; bilinguisme EN/FR de l'extension (`package.nls*.json`, `vscode.l10n`), pack de
  langue français dans `extensions.lst` et locale par `install-vscodium.sh` (amendement PA-10).
- [ ] Lot 4 — F5 diagnostics en erreur à la saisie (CFG-7 §2bis ; lepton : contenu non enregistré,
  positions).
- [ ] Lot 5 — F6 vue IDE-1 (lepton : répartition bibliothèque / greffon / fichiers en JSON).
- [ ] Lot 6 — F8 essai borné (R3) ; F7 en palette si non fait ; validation VSCodium et cartes ;
  intégration du `.vsix` à l'installation (à décider) ; passage VM Debian (§2bis) ; bilan.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-12 : ENV-12 lancée, F0-F8 retenues | utilisateur | oui |
| O5 : XML du projet dans `project-<projet>` de la graine, lot 2 d'ENV-12 | utilisateur (lot : proposition acceptée avec le plan) | oui |
| Découpage en 6 lots | utilisateur (accord du plan) | oui |
| Outillage épinglé, sans esbuild ni ovsx ; éditeur `lepton-distribution` | utilisateur | oui |
| Bilinguisme EN par défaut + FR, pack de langue FR épinglé, au lot 3 | utilisateur | oui |
| `cwd` = dossier de l'espace ; résolution de `lepton.path` ; nouvel essai `--scion` sur le texte du message ; `--type` repris de la CLI ; tests `node:test` | proposition appliquée, à confirmer | oui |
| PA-12 non marqué « tranché » dans `ORCHESTRATION.md` §4 (aucun PA ne l'est : convention conservée) | proposition appliquée | non |

## Pièges rencontrés
- `node --test out/test/` (répertoire) échoue sous Node 22.15 (MODULE_NOT_FOUND) → motif
  `out/test/*.test.js`.
- `@types/vscode` n'a pas de 1.135 : 1.134.0 (doit rester ≤ `engines.vscode` pour `vsce`).
- `vsce package` demande une confirmation sans `LICENSE` → `--skip-license` (script `package`) ;
  licence du dépôt à décider avant toute publication.
- Deux Node sur l'hôte (nvm 22.15.0 en tête du PATH, `/usr/local/bin/node` 24.13.1).

## Critères de validation
- [x] PA-12 tranché.
- [ ] Aucune logique de graine ou de greffon dans `extension/` (revue : uniquement des appels à
      `lepton`) — respecté au lot 1, revue finale au lot 6.
- [ ] Création de fichier depuis l'explorateur : lien présent dans le trunk sans action manuelle
      (FIC-1) ; aucun fichier régulier dans le trunk (FIC-3) — par commande au lot 1 ; automatique
      au lot 3.
- [ ] Vue IDE-1 cohérente avec `lepton seed status`.
- [ ] Installation du `.vsix` par `codium --install-extension` sur Mac et Debian — Mac fait.

## Reprise
```
cd /Users/cle_d_anton/lepton-tools-dev/lepton-tools && claude
# « Démarre la session sur l'étape indiquée dans DEVENV-STATUS » (ENV-12 lot 2 : O5 + F7)
# Construction de l'extension : cd extension && npm ci && npm test && npm run package
```
