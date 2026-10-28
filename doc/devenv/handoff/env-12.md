# Passation ENV-12 — Extension VSCodium (phase 2) — session du 2026-10-28 (lot 6, S3)

## Statut
terminée (2026-10-28) — extension 0.5.1 validée sur Mac (QEMU, NUCLEO-F429ZI, NUCLEO-WL55JC1) et
Debian (R12-1) ; D-a et O-b corrigés ; bilan `rapports/env-12-bilan.md` ; renvoi D-b ouvert.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `devenv/env-12`, fusionnée `--no-ff` dans `main` après ce commit, les deux poussées (PA-P) | `devenv(env-12): état et passation (lot 6 S3 …)` ; avant : 7e74c6d O-b, c0374c9 D-a, c89d963 et a6fc55a fusions de `devenv/env-12-debian` | oui |
| lepton-tools (VM) | `origin/devenv/env-12-debian` | bc95a6a rapport, `max_user_watches` remis (a1a7dbe rapport de validation Debian) | fusionnée |
| clone noyau `~/lepton/depots/lepton/original/master` | `master` 16a331b | non touché | oui |
| seed.scions | `master` f1d1f3c (tag 0.5.1.1) | non touché | oui |
| graines d'essai Mac `essais/env-11/{qemu,f429zi,wl55jc1}` | `main` | 107cd57, e7b8eed, b43e523 (inchangées) ; espaces `.code-workspace` régénérés (`cmake.modifyLists.*`) | oui |
| graine d'essai VM `essais/env-11/qemu` (env11) | `master` | 6d3d2a5 O5, 8539dfa presets d'ENV-11 (locales, non poussées) | oui |
| lepton (pipx, Mac) | `~/.local/bin/lepton` | réinstallé par `install-vscodium.sh --skip-toolchain` depuis 7e74c6d (1 puis 0) | — |

## Fait pendant la session
- Ordre `R12-1` à la session VM `debian-linux-vm-groovy-liskov` (§2bis) : ACCUSÉ, 15 AVANCEMENT,
  FIN-SUCCÈS ; table des messages : `rapports/env-12-debian.md` §6.
- Debian 13.7 : INS (4 puis 0 changement), O5 (graine migrée), F1 (français au second lancement),
  F2, F3, L3-4, F4 (avec `essai-s3`), F5, F6, F7, L6-5, L6-6, L6-7, F8 sous `gdb-multiarch`, témoin,
  `pytest` 191 : conformes (`rapports/env-12-debian.md` §2).
- D-a corrigé (c0374c9, `lepton/checks.py` : ligne de xmllint gardée ; test
  `test_rootstock_xml_xsd_line`, rouge sans la correction).
- O-b corrigé (7e74c6d, `lepton/generate.py` : `cmake.modifyLists.addNewSourceFiles` et
  `removeDeletedSourceFiles` à `no`) ; essai VSCodium Mac : création par le trunk et « Supprimer du
  greffon » sans notification de CMake Tools, trunk et clones propres.
- `pytest` 192 verts ; `install-vscodium.sh --skip-toolchain` 1 puis 0 changement.
- Bilan `rapports/env-12-bilan.md` : critères, exigences reclassées, défauts, observations,
  propositions.

## Reste à faire dans l'étape
- Rien. Renvoi hors étape : D-b (`rapports/env-12-bilan.md` §3).

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Graine VM commitée à part (8539dfa) ; `max_user_watches` relevé puis remis ; F4 avec `essai-s3` ; `build/env11-essai-s3` supprimé ; push `devenv/env-12-debian` | utilisateur | oui |
| D-a corrigé ; D-b renvoyé ; O-b corrigé ; O-a laissé | utilisateur | oui |
| `removeDeletedSourceFiles` à `no` en plus d'`addNewSourceFiles` | proposition de la session, appliquée (même cause, à la suppression) | oui (signalée) |
| Propositions des lots 1 à 6 et suites « laisser » des observations confirmées en bloc | utilisateur | oui |
| Clôture d'ENV-12, fusion dans `main`, push de `devenv/env-12` et `main` (PA-P) | utilisateur | oui |

## Pièges rencontrés
- zsh ne découpe pas une variable non citée en arguments (`$A`) → « option inconnue » d'`install-vscodium.sh` ;
  écrire les options en clair.
- Messages Remote Control vers la VM : « delivery is not confirmed » ; seul l'accusé suivant de la VM
  prouve la lecture.
- Création F3 par le trunk : rien ne change à l'écran (onglet sous le trunk, même nom) ; le
  déplacement se vérifie par `ls -l` (lien dans le trunk, fichier dans le clone) ou le canal « Lepton ».
- VM : premier lancement de VSCodium après l'installation du pack de langue en anglais (O-a).

## Critères de validation
- [x] PA-12 tranché.
- [x] Aucune logique de graine ou de greffon dans `extension/` (revue S2, `rapports/env-12-lot6.md` §12).
- [x] Création de fichier depuis l'explorateur : lien présent dans le trunk sans action manuelle
      (FIC-1) ; aucun fichier régulier dans le trunk (FIC-3) — Mac et Debian.
- [x] Vue IDE-1 cohérente avec `lepton seed status` — Mac et Debian.
- [x] Installation du `.vsix` par `codium --install-extension` sur Mac et Debian.

## Reprise
```
cd /Users/cle_d_anton/lepton-tools-dev/lepton-tools && claude
# Chantier terminé (ENV-0 à ENV-12). Sur décision de l'utilisateur : renvoi D-b sur devenv/env-12-r1
# depuis main, ou révision du plan (skill lepton-portage-instructions).
# Tests de lepton : ~/lepton-tools-dev/venv-lepton-tools/bin/python -m pytest -q (≈ 5 min)
```
