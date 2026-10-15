# Passation ENV-10 — Script d'installation de VSCodium — session du 2026-10-15 (S1)

## Statut
en cours — PA-10 tranché, script écrit et validé sur Mac Intel (5 changements puis 0) ; validation
Debian (VM) reste, après accord de push (PA-P).

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `devenv/env-10` | `devenv(env-10): état et passation`, précédé de d78afcf (script, liste, README) ; `main` = f6bb974 (fusion env-9) | oui |
| clone noyau `depots/lepton/original/master` | `devenv/env-10` (extraite dans `~/lepton`) | 1b2f7b6 `SCION_REF` et `SCION_SPEC` surchargeables ; `master` = 42733ce | oui |
| BSP `depots/lepton-bsp/nucleo-wl55jc1` | `master` (extraite) | a329f4d fusion de `devenv/env-9` ; regreffé, trunk 4 037 feuilles, propre | oui |
| seed.scions, graine de travail, autres greffons | inchangés | — | oui |

Aucun push. Scripts du noyau à la racine du clone (`scripts/`), non greffés : aucune regreffe.

## Fait pendant la session
- Fusions locales `--no-ff` de `devenv/env-9` (lepton-tools, BSP WL) ; `scion graft --scion
  lepton@bsp::nucleo-wl55jc1` ; contrôles du trunk vides.
- Relevé Open VSX, VSCodium, CodeLLDB : `rapports/env-10-validation.md` §1 ; PA-10 tranché.
- Clone noyau : `SCION_REF` / `SCION_SPEC` surchargeables dans `install-macos.sh` et
  `install-debian.sh` ; Debian ne réinstalle plus scion s'il est à jour (1b2f7b6).
- `scripts/install-vscodium.sh` et `scripts/extensions.lst` (d78afcf) ; README.
- Mac Intel : cask retiré, exécution n° 1 (5 changements), n° 2 (0) ; `diff` liste installée /
  `extensions.lst` vide ; grep INS-5 vide ; `shellcheck` 0.11.0 sans remarque (3 scripts) ;
  `pytest -q` 116 passed. Rapport §2-§3.
- `~/.local/bin/codium` → binaire de l'app (décision utilisateur).

## Reste à faire dans l'étape
- [ ] PA-P : accord de push (lepton-tools `devenv/env-10`, clone noyau `devenv/env-10`,
      seed.scions `master` + tag `0.5.1.0`) pour la VM.
- [ ] Session VM Debian (ENV-10 §3) : branche `devenv/env-10-debian`, deux exécutions, rapport
      `rapports/env-10-debian.md` ; vérifier `dpkg-query` = `1.135.06055` (rapport §4).
- [ ] Session Mac : intégrer le rapport Debian, clore ENV-10 (statut, versions, hôtes validés).
- Hors ENV-10 : choix effectif de lemminx natif (Java présent sur le Mac) à constater en ENV-11
  (CFG-7) ; défaut 0.5.0.1 des scripts du noyau à relever une fois 0.5.1.0 poussé.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Plan de session | utilisateur | — |
| D1 `SCION_SPEC` dans les scripts du noyau ; D2 `--lepton-clone` ; D3 migration vers le `.dmg` | utilisateur | oui |
| PA-10 : liste d'extensions, VSCodium 1.135.06055, CodeLLDB par paquet GitHub, `.dmg` arm64 sur Apple Silicon, réglages utilisateur fusionnés | utilisateur | oui |
| Lien `~/.local/bin/codium` | utilisateur | oui |
| Pas de push en fin de session | utilisateur | oui |
| `--with-debug-tools` toujours passé aux scripts du noyau | proposition non validée | oui (à confirmer) |
| `--seed-scions DIR` (source `git+file://` de scion) en plus de D1 | proposition appliquée (mise en œuvre de D1) | non (rapport) |
| VSCodium d'une autre version présent → arrêt avec marche à suivre (pas de remplacement) | proposition non validée | non (rapport, en-tête du script) |

## Pièges rencontrés
- `brew uninstall --cask` → nettoyage automatique Homebrew de formules inutilisées (imath 3.1.12,
  libdeflate 1.22 au moins) → pour un prochain retrait : `HOMEBREW_NO_AUTOREMOVE=1` et garder la
  sortie entière.
- Version de lepton : `pyproject.toml` en version dynamique → lue dans `lepton/__init__.py`.
- `codium --install-extension` d'une extension dont les dépendances ne sont pas installées tire
  leur dernière version → ordre de `extensions.lst` : dépendances d'abord.
- CodeLLDB d'Open VSX = amorce sans adaptateur ; contrôle par `adapter/codelldb` dans
  `~/.vscode-oss/extensions/vadimcn.vscode-lldb-<version>*`.

## Critères de validation
- [x] PA-10 tranché ; `extensions.lst` épinglé.
- [ ] `codium --list-extensions --show-versions` = `extensions.lst` sur Mac (oui) et Debian (à faire).
- [ ] Deux exécutions successives sans erreur ni changement (INS-4) : Mac oui, Debian à faire.
- [x] `grep -n '/usr/local\|/opt/homebrew\|/opt/local' scripts/install-vscodium.sh` vide (INS-5).
- [x] Le gestionnaire de paquets utilisé est celui d'`install-macos.sh` sur le même hôte.
- [x] Aucune commande d'installation de la chaîne dans le script (INS-3).
- [x] `shellcheck` sans erreur.

## Reprise
```
cd /Users/cle_d_anton/lepton-tools-dev/lepton-tools && claude
# « Démarre la session sur l'étape indiquée dans DEVENV-STATUS » (ENV-10, validation Debian : PA-P d'abord)
```
