# Passation ENV-11 — Validation de bout en bout — session du 2026-10-15 (S1)

## Statut
en cours — S1 (scénario Mac en ligne de commande) faite ; S2 (cartes, VSCodium) et S3 (VM Debian,
bilan) restent.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `devenv/env-11` (non poussée) | `devenv(env-11): état et passation (S1)` ; avant : 7d191aa modèle d'application, 338ff5b purge des fichiers du Finder ; `main` = 657c395 (fusion de `devenv/env-10`, non poussée) | oui |
| clone noyau `depots/lepton/original/master` | `devenv/env-11` (extraite dans `~/lepton`, non poussée) | a572f00 défaut `SCION_REF` relevé à 0.5.1.0 ; `master` = 1dde0af (fusion de `devenv/env-10`, non poussée) | oui |
| seed.scions | `master` 79f4f96, tag 0.5.1.0 | inchangé | oui |
| BSP, familles, graine de travail de `~/lepton` | `master` / `original-tree` | inchangés (`essais/env-11/ref-{avant,apres}.txt`) | oui |
| Rootstocks d'essai (hors git) | `~/lepton-tools-dev/essais/env-11/{qemu,f429zi,wl55jc1}` ; copie `qemu-gra2` (BSP dégreffé, jetable) ; `bout-en-bout/` | graines commitées dans chacun ; clones noyau d'essai extraits sur `master` à la main (N1) | — |

## Fait pendant la session
- Fusions locales `--no-ff` de `devenv/env-10` (lepton-tools `main` 657c395, noyau `master` 1dde0af) ;
  `~/lepton` : trunk 4 037 feuilles, propre, sans regreffe.
- PA-11 accordé (deux cartes). Reliquat ENV-10 : `SCION_REF` 0.5.1.0 dans `install-{macos,debian}.sh`,
  `doc/BUILDING.md`, `README-PAQUET.md` (a572f00, `shellcheck` sans remarque, tag présent sur GitHub).
- Scénario Mac §2.1-2.4, 2.8, 2.9 (CLI) : `doc/devenv/rapports/env-11-mac.md` §2 — install sans effet,
  graine sans application, fumée, KAL 18/18, application + `lepton file add` construite sans édition
  CMake et exécutée sous QEMU, `scion remove` sans lien orphelin, `lepton.bin` identique sur 3
  constructions.
- Défauts : N1 scion (renvoyé ENV-7) ; N2 et N3 lepton corrigés (338ff5b, 7d191aa ; `pytest` 117
  verts ; `bout-en-bout.sh` succès ; lepton réinstallé par pipx).
- Préparation S2 : graines `env11f4` (embOS) et `env11wl` (FreeRTOS) créées, générées, construites
  (`env11f4-debug-board`, `env11wl-debug-board`).

## Reste à faire dans l'étape
- [ ] S2 §2.5-2.6 : brancher les cartes (aucune sonde vue en S1), `openocd -c "init; targets; shutdown"`,
      flash (`lepton : flasher` ou `openocd … program`), arrêt sur `main`, console série (DBG-3).
- [ ] S2 §2.7 : VSCodium sur `essais/env-11/*/<projet>.code-workspace` (IDE-1 à IDE-5, DBG-1 à DBG-3,
      lemminx natif / CFG-7) ; vérifier O6 (embOS depuis l'éditeur).
- [ ] S2 §2.9 éditeur : construction depuis VSCodium avec `SOURCE_DATE_EPOCH=1760536800`, empreinte
      attendue `lepton.bin` 25d50f61…, `lepton.hex` 7e29c21c… (graine `env11`, preset `env11-debug-qemu`).
- [ ] S3 §3 : consigne VM Debian (étapes 1-4 et 9), push soumis à PA-P (`main`, `devenv/env-11` des
      deux dépôts), rapport `rapports/env-11-debian.md`.
- [ ] S3 §4 : bilan exigences P1 × résultat ; classement de N1 et O1-O7.
- Reliquats hors étape : Apple Silicon (revue seule) ; ligne « openocd » vide du récapitulatif
  d'`install-debian.sh`.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-11 : flash autorisé sur les deux cartes (M4, octets d'option et M0+ intouchés) | utilisateur | oui |
| Une graine par carte pour §2.5-2.6 | utilisateur | oui |
| Découpage S1 / S2 / S3 | utilisateur | oui |
| `SCION_REF` corrigé dans ENV-11 | utilisateur | oui |
| N1 : consigner, `checkout master` dans les clones d'essai, renvoi ENV-7 | utilisateur | oui |
| N2, N3 : corriger lepton dans ENV-11 | utilisateur | oui |
| Forme de la correction N2 (`scion_on_trunk` dans `seed.py`, purge avant `graft` et `graft-remove`) | proposition appliquée | oui (commit 338ff5b) |
| Backends des graines d'essai (an386 FreeRTOS, F429 embOS, WL55 FreeRTOS) ; application `salut` déclarée dans le XML du clone noyau d'essai | proposition appliquée | non (rapport §1-§2) |
| Renvois des observations O1-O7 | propositions non validées | oui (à classer en S3) |

## Pièges rencontrés
- Le Finder recrée des `.DS_Store` dans les trunks pendant la session → scion refuse de greffer
  (corrigé par N2 pour toutes les commandes lepton ; `scion` employé directement les refuse toujours).
- `seed new … @master` depuis `~/lepton` : le clone suit la branche extraite de l'origine (N1) →
  `git -C <rootstock>/depots/lepton/original/master checkout master` après `seed new`.
- `lepton file add` crée le fichier : il refuse un fichier déjà présent dans le clone.
- Une application n'est liée que déclarée dans le XML (`<binaries src_path="bin/<nom>" dest_path="bin">`) ;
  la retirer du XML avant `lepton scion remove`, sinon la reconfiguration CMake échoue (O4).
- embOS : `export LEPTON_EMBOS_ROOT=~/lepton/third_party/embos/cortexm-gcc/5.20.0.0` puis
  `cmake --preset … --fresh` (valeur vide sinon conservée dans le cache).
- Bash de l'outil = zsh : `source lepton-env.sh` hors rootstock ne trouve rien ; ne pas s'y fier.
- `cmake -B <autre>` pour une construction parallèle : supprimer ce répertoire ensuite, `lepton`
  reconfigure tous les `build/*`.

## Critères de validation
- [x] PA-11 tranché.
- [ ] Toutes les exigences P1 conformes sur Mac, ou écart accepté par l'utilisateur (S2, bilan S3).
- [ ] Scénario Debian conforme, ou report consigné (S3).
- [ ] Aucun fichier régulier dans le trunk à la fin du scénario (S1 : vrai pour les trois rootstocks
      d'essai, hors `.DS_Store` ignorés par Q8 ; à refaire en fin de S2).

## Reprise
```
cd /Users/cle_d_anton/lepton-tools-dev/lepton-tools && claude
# « Démarre la session sur l'étape indiquée dans DEVENV-STATUS » (ENV-11 S2 : cartes branchées, VSCodium)
```
