# Reprise 5 — Validation Debian (D3, D4, O9, O12) — 2026-10-16

Session VM Debian conduite selon `doc/devenv/consignes/env-10-r5-debian.md`. Journaux :
`~/env-10-r5-journaux/` sur la VM (hors git).

Bilan : D3, D4, O9, O12 conformes. Un défaut commun relevé (§5, A) : le récapitulatif des
versions d'`install-debian.sh` meurt par intermittence sur SIGPIPE (code 141) ; deux exécutions
sur quatre ont dû être relancées. Aucune correction Debian.

## 1. Hôte

| Élément | Valeur |
| --- | --- |
| Système | Linux x86_64, Debian 13.7, noyau 6.12.107+deb13-amd64, utilisateur `lepton-user` |
| VSCodium | 1.135.06055 |
| scion | 0.5.1.0 avant, 0.5.1.1 après |
| lepton | 0.1.0 avant et après (paquet pipx, `site-packages`) ; réinstallé depuis les sources de `c5286be` |
| `lepton --version` après | `lepton 0.1.0` / `scion 0.5.1.1 (requis ≥ 0.5.1.1)` |
| xmllint, clangd, arm-none-eabi-gdb avant | absents |
| gdb-multiarch | GNU gdb (Debian 16.3-1) 16.3 ; `python print('ok')` → `ok` |
| Espace | `/tmp` 747 Mo (647 Mo libres) ; `/home` 26 Go (20 Go libres) |
| Rootstock d'essai | `~/lepton-tools-dev/essais/env-11/qemu` présent |

Têtes des clones : lepton-tools `devenv/env-10-r5` c5286be ; lepton-noyau `devenv/env-10-r5`
ed46f71 ; seed.scions tag `0.5.1.1` = f1d1f3c (copie de travail laissée sur 79f4f96, 0.5.1.0 ;
`install-vscodium.sh` installe scion depuis le tag).

## 2. Scénario

| Étape | Commande (résumé) | Résultat | Correction validée |
| --- | --- | --- | --- |
| 5.1 | `install-vscodium.sh` n° 1 | **code 141** : arrêt dans le récapitulatif d'`install-debian.sh`, après la ligne `openocd` (§5, A). Avant l'arrêt : `libxml2-utils`, `clangd`, `clangd-19` installés (section « Environnement de développement (xmllint, clangd) ») ; scion 0.5.1.0 → 0.5.1.1 ; `libexpat1` mis à jour (correctif de sécurité Debian). Partie VSCodium/extensions/lepton non exécutée | D3, D4 (paquets) |
| 5.1 bis | relance de n° 1 | fin normale (`Terminé.`, bilan) ; code non relevé (ligne `echo code=` non exécutée), journal écrit sur celui de 5.1. Récapitulatif : xmllint et clangd présents ; « lepton 0.1.0 : paquet installé différent des sources (ou hors pipx) : réinstallation » ; **`changements 1`** | O12 (1re exécution) |
| 5.2 | `install-vscodium.sh` n° 2 | **code 141**, même endroit, aucun paquet installé | — |
| 5.2 bis | relance de n° 2 | code 0 ; tout « déjà installé » ; « lepton 0.1.0 : déjà installé, identique aux sources » ; **`changements 0`** | O12 (2e exécution), INS-4 |
| 5.3 | `lepton check -C $R` | code 0, « 5 fichier(s) conforme(s) » dont `trunk/sys/user/tauon-basic/etc/mkconf_tauon_basic_qemu_mps2.xml` (`--json`) ; aucun avertissement « xmllint absent ». Contre-preuve : `xmllint --noout --schema …/mklepton.xsd <xml>` → « validates », code 0 | D3 |
| 5.4 | `lepton generate -C $R` | code 0 ; aucun avertissement clangd ni gdb. `clangd.path` = `/usr/bin/clangd` (→ `/usr/lib/llvm-19/bin/clangd`) ; `cortex-debug.gdbPath` et `gdbPath` = `/usr/bin/gdb-multiarch` ; `armToolchainPath` = `/usr/bin`. Diff : `clangd.path`, `json.schemas`, `xml.fileAssociations`, tâche « lepton : vérifier », `cmake.options.statusBarVisibility` (§5, D) ; idempotent | D4, O9 |
| 5.5 | `gdb-multiarch -x gdbinit-lepton` (sans `target`) | code 0 ; aucune ligne « gdb sans Python » ; `help lepton-stacks` → « Par tâche embOS : taille de pile, tas de thread Lepton, usage maximal de pile, marge. » ; `help lepton-fault` → docstring | O9 |
| 5.6 | `pytest -q -rs` (venv `~/lepton-tools-dev/venv-test`, `TMPDIR` sous ~) | **139 passed** en 52,8 s ; aucun test ignoré | D3 |
| 5.7 | `find trunk -type f` / `find -L trunk -type l` | vides | — |

Clones du rootstock d'essai : modifications suivies dans `depots/lepton-seed/env11`
(`.scion.ramifications`, `.scion.sources.list`) et `depots/lepton-application/salut` (`salut.c`),
datées du 2026-10-15 (ENV-11), antérieures à la session ; non touchées.

## 3. Versions relevées

| Outil | Version |
| --- | --- |
| xmllint (libxml2-utils) | 2.12.7+dfsg+really2.9.14-2.1+deb13u3 ; `xmllint: using libxml version 20914` |
| clangd | paquet `clangd` 1:19.0-63 → `clangd-19` 1:19.1.7-3+b1 ; « Debian clangd version 19.1.7 (3+b1) » |
| scion | 0.5.1.1 |
| gdb-multiarch | 16.3-1 (avec Python) |

## 4. Corrections propres à Debian

Aucune.

## 5. Défauts et observations

**A. Défaut commun — SIGPIPE dans le récapitulatif des versions (pour la session Mac).**
`lepton-noyau/scripts/install-debian.sh:134` (`b52e656`, D3), sous `set -euo pipefail` :
`v="$(xmllint --version 2>&1 | head -1)"`. `xmllint` écrit sa version (259 octets) sur stderr non
tamponné, en plusieurs `write` ; si `head -1` s'est fermé, l'écriture suivante reçoit SIGPIPE,
`pipefail` rend 141 et `set -e` arrête le script ; `install-vscodium.sh` s'arrête avec lui avant
VSCodium, les extensions et lepton. Reproduit hors script : 18 échecs sur 300 appels
(`bash -c 'set -euo pipefail; v="$(xmllint --version 2>&1 | head -1)"'`) ; en conditions réelles,
2 échecs sur 4 exécutions. `install-macos.sh` emploie la même forme pour tous les outils
(`"$c" --version 2>&1 | head -1`) : défaut commun, non corrigé ici (clone noyau en lecture seule).
Pistes : `| sed -n 1p` (lit tout), ou `|| true` dans la substitution.

**B. Observation — ligne `openocd` vide dans le récapitulatif Debian.** openocd écrit sa version
sur stderr, redirigé vers `/dev/null` par `install-debian.sh` (antérieur à la reprise 5 ;
`install-macos.sh` utilise `2>&1`).

**C. Observation — `lepton check -v` n'affiche pas l'appel à xmllint.** `validation.validate_xml`
appelle `subprocess.run` directement, sans la trace des commandes externes promise par `-v`.

**D. Observation — consigne §5.4.** Le diff du `.code-workspace` contient aussi
`"cmake.options.statusBarVisibility": "visible"`, ajouté en reprise 4 (`0ede3ee`, O11) comme les
schémas et la tâche ; conforme, mais absent de la liste attendue.

**E. Observation — compte de changements de l'installation n° 1.** Mac : 2 ; Debian : 1 sur la
relance (lepton), les paquets et scion ayant été installés par l'exécution interrompue.

Question pour l'utilisateur : aucune.
