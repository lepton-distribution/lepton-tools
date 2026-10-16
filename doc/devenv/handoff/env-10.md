# Passation ENV-10 — Script d'installation de VSCodium — reprise 5 (D3, D4, O6, O12 ; noyau O9) — session du 2026-10-16

ENV-10 est terminée depuis le 2026-10-15 (`rapports/env-10-validation.md`, `env-10-debian.md`).
Cette passation remplace celle de S2 et porte sur la reprise 5 du bilan ENV-11
(`rapports/env-11-bilan.md` §3), dernière reprise avant PA-12. Rapports : `rapports/env-10-r5.md`
(Mac), `rapports/env-10-r5-debian.md` (VM).

## Statut
terminée — D3, D4, O6, O9, O12 corrigés et validés (Mac, VM Debian, VSCodium, NUCLEO-F429ZI) ;
défauts A, B, C du passage VM et dérive `extensions.autoUpdate` corrigés ; fusions de
`devenv/env-10-r5` au début de la session suivante.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `devenv/env-10-r5` (depuis `main` 353c3e7 = fusion `--no-ff` de `devenv/env-9-r4`) | `devenv(env-10-r5): état et passation` ; avant : ae10f08 (`autoUpdate` `"off"`), 80e2b27 (C), 2b08c09 (fusion du rapport VM), 8e4ba59 (O12), ffd98e1 (O9) | oui |
| lepton-tools | `devenv/env-10-r5-debian` (VM, distante) | d7d939b rapport Debian — fusionnée dans `devenv/env-10-r5` (2b08c09) | — |
| clone noyau `~/lepton/depots/lepton/original/master` | `devenv/env-10-r5` (extraite dans `~/lepton`, depuis `master` 9ea1b2a) | 3e9a8e0 (A, B) ; ed46f71 (O6), e50479d (O9), b52e656 (D3, D4) | oui |
| seed.scions | `master` f1d1f3c, tag 0.5.1.1 (poussés) | — | oui |
| `~/lepton` trunk | — | 4 037 feuilles, aucun fichier régulier, aucun lien cassé, sans regreffe (fichiers modifiés seulement) | oui |
| rootstocks d'essai `essais/env-11/{qemu,f429zi,wl55jc1}` | graines et clones inchangés | espaces régénérés par le lepton installé : `gdbPath` = `/opt/local/bin/arm-none-eabi-gdb`, schémas du paquet pipx, `~/.local/bin/lepton` | — |

Poussés le 2026-10-16 (PA-P) : lepton-tools `main` 353c3e7 et `devenv/env-10-r5` jusqu'à c5286be ;
clone noyau `devenv/env-10-r5` jusqu'à ed46f71. Non poussés : les commits suivants des deux
branches (noyau : 3e9a8e0 ; lepton-tools : de 5e8376e au commit de clôture). lepton pipx = `devenv/env-10-r5`
ae10f08 (installé par `install-vscodium.sh`).

## Fait pendant la session
- Fusion `--no-ff` de `devenv/env-9-r4` (lepton-tools `main` 353c3e7), `pipx install --force`,
  `lepton generate` des trois rootstocks d'essai.
- D3, D4 (b52e656) : `libxml2`/`clang-21` (MacPorts), `libxml2-utils`/`clangd` (Debian), récapitulatifs, `doc/BUILDING.md`.
- O9 : `gdbinit-lepton` gardé par `if $_isvoid($_streq)` (e50479d) ; `generate.find_gdb()` (ffd98e1),
  2 tests. Essais : gdb seul, NUCLEO-F429ZI (`rapports/env-10-r5-essai-o9.py`), VSCodium QEMU et F429ZI.
- O6 (ed46f71) : défaut CMake ; oracle embOS `oracles/env-10-r5-apres/` contre `env-8-r3-apres/`,
  preuve E1 (`rapports/env-10-r5-preuve-empreintes.sh`), configuration et construction sans variable.
- O12 (8e4ba59) : `lepton_identique()` (comparaison du paquet pipx aux sources).
- PA-P ; consigne VM `consignes/env-10-r5-debian.md`, transmise par SendMessage ; rapport VM fusionné.
- A, B (3e9a8e0), C (80e2b27), `extensions.autoUpdate` `"off"` (ae10f08).
- `pytest` 140 verts ; bout en bout vert ; `install-vscodium.sh` Mac : 1 puis 0 changement.
- Bilan ENV-11 §3 : D3, D4, O6, O9, O12 marqués corrigés.

## Reste à faire
- [x] Fusions `--no-ff` de `devenv/env-10-r5` (2026-10-16, en clôture) : lepton-tools `main` 89a97a3 ;
  clone noyau `master` 16a331b, extrait dans `~/lepton` (trunk 4 037 feuilles, propre) ; lepton
  réinstallé depuis `main` ; `lepton check` / `generate` des rootstocks d'essai : code 0, espaces inchangés.
- [x] PA-P : push de `main`, `master` du clone noyau et des deux `devenv/env-10-r5` (accord de l'utilisateur).
- [ ] PA-12 : décision de lancer ENV-12 (renvois O2, O5, O10 relance, R1, §2bis erreurs à la saisie).

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| O9 lepton + noyau ; O6 défaut CMake ; O12 comparaison du contenu ; D4 Debian et Mac | utilisateur | oui |
| PA-P : push de `main` (R4), `devenv/env-10-r5` des deux dépôts | utilisateur | oui |
| Validation VSCodium de gdb 17.2 avant clôture | utilisateur | oui |
| A : `sed -n 1p` partout ; B et C traités dans R5 ; pas de nouveau passage VM | utilisateur | oui |
| `extensions.autoUpdate` : écrire `"off"`, accepter `false` | utilisateur | oui |
| Non-régression d'O6 sur les seuls presets embOS (FreeRTOS n'inclut pas `embos.cmake`) | proposition appliquée | oui (ligne équiv. PA-6) |
| Message de `gdbinit-lepton` ; `armToolchainPath` = dossier du compilateur ; `pyproject.toml` non comparé par O12 | proposition appliquée | non (rapport §1) |
| Garde Python par `$_isvoid($_streq)` | proposition appliquée, essayée sur gdb 14.2 et 17.2 | non (rapport §1) |

## Pièges rencontrés
- `git add` d'un fichier suivi sous un répertoire ignoré (`scion/debug`) refusé : `git add -u <chemin>`.
- Le récapitulatif de version `… | head -1` sous `set -euo pipefail` meurt par intermittence
  (SIGPIPE, code 141) : invisible sur le Mac (0/300), 18/300 sur Debian.
- VSCodium 1.135 réécrit `extensions.autoUpdate: false` en `"off"` à chaque lancement : le compte de
  changements d'`install-vscodium.sh` en dépendait.
- Le preset du noyau passe `LEPTON_EMBOS_ROOT=$env{…}` : sans variable, le cache vaut `""` (et non
  « indéfini ») ; le défaut doit traiter la valeur vide.
- La session VM (Remote Control) ne confirme pas la réception d'un SendMessage ; elle a répondu par
  message à la fin du passage.
- `pyproject` hors comparaison O12 : un changement de dépendance seul ne déclenche pas de réinstallation.

## Critères de validation (reprise 5)
- [x] `xmllint` et clangd LLVM installés par les scripts du noyau (Mac, Debian) ; `lepton check` valide le XML sur Debian.
- [x] `lepton generate` : `clangd.path` sur Debian, gdb avec Python sur les deux hôtes ; idempotent.
- [x] `lepton-stacks` disponible sous gdb avec Python, message explicite sinon (carte F429ZI).
- [x] Construction embOS sans `LEPTON_EMBOS_ROOT` ; non-régression embOS (7 presets).
- [x] `install-vscodium.sh` : réinstallation à contenu différent, puis 0 changement (Mac, Debian).
- [x] `shellcheck` sans erreur ; `pytest` 140 verts ; bout en bout vert ; trunk de référence propre.

## Reprise
```
cd /Users/cle_d_anton/lepton-tools-dev/lepton-tools && claude
# « Démarre la session sur l'étape indiquée dans DEVENV-STATUS » (PA-12, ENV-12)
```
