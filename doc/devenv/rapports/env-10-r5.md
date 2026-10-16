# Reprise 5 — ENV-10 D3, D4, O6, O12 + noyau O9 — 2026-10-16

Renvois du bilan ENV-11 (`env-11-bilan.md` §3). Branches `devenv/env-10-r5` : lepton-tools (depuis
`main` 353c3e7, fusion de R4) et clone noyau (depuis `master` 9ea1b2a). Décisions de l'utilisateur
(début de session) : O9 lepton + noyau ; O6 défaut CMake ; O12 comparaison du contenu ; D4 Debian et Mac.

## 1. Corrections

| ID | Dépôt | Commit | Correction |
| --- | --- | --- | --- |
| D3 | clone noyau | b52e656 | `install-macos.sh` : `pkg_install libxml2:libxml2` ; `install-debian.sh` : `libxml2-utils` ; `xmllint` au récapitulatif des versions (Debian : version lue sur stderr) ; `doc/BUILDING.md` §1. |
| D4 | clone noyau | b52e656 | `install-debian.sh` : `clangd` ; `install-macos.sh` : port `clang-21` (`clangd-mp-21`), Homebrew `llvm` (« keg-only » : `lepton generate --clangd`, Apple Silicon en revue) ; récapitulatifs. |
| O9 | clone noyau | e50479d | `debug/gdbinit-lepton` : bloc Python sous `if $_isvoid($_streq)` (`$_streq` est une fonction de commodité écrite en Python, vide sans Python) ; sans Python : message au chargement et `lepton-stacks` remplacée par un message ; `lepton-load`, `lepton-fault` inchangées. |
| O9 | lepton-tools | ffd98e1 | `generate.find_gdb()` : parmi les `arm-none-eabi-gdb` puis `gdb-multiarch` du PATH (doublons par chemin réel écartés), le premier qui répond à `python print('ok')` ; sinon le premier trouvé + avertissement ; aucun : code 2. `cortex-debug.armToolchainPath` = dossier du compilateur (et non plus du gdb). 2 tests ; README. |
| O6 | clone noyau | ed46f71 | `cmake/kal/embos.cmake` : `LEPTON_EMBOS_ROOT` vide (variable d'environnement absente ; le preset du noyau passe `$env{LEPTON_EMBOS_ROOT}`) → `${CMAKE_SOURCE_DIR}/../third_party/embos/cortexm-gcc/5.20.0.0`, défaut de `scripts/lepton-env.sh`. Valeur non vide : inchangé. |
| O12 | lepton-tools | 8e4ba59 | `install-vscodium.sh` `lepton_identique()` : « déjà installé » seulement si le paquet du venv pipx (`pipx environment --value PIPX_LOCAL_VENVS`) est identique à `lepton/` (`diff -rq`, `__pycache__`, `.DS_Store` exclus) et aux trois schémas copiés ; sinon `pipx install --force`. |

Propositions appliquées (non validées) : message de `gdbinit-lepton` ; `armToolchainPath` vers le
dossier du compilateur (inchangé sur le Mac : même dossier qu'avant) ; `pyproject.toml` non comparé
par O12 (dépendances) ; cache CMake laissé vide et défaut en variable normale (réévalué à chaque
configuration).

## 2. Non-régression d'O6 (skill `lepton-oracle`)

Référence : `oracles/env-8-r3-apres/` (noyau aee4618 ; entre aee4618 et ed46f71 seuls changent des
fichiers non compilés — scripts, `doc/`, `gdbinit-lepton` — et `embos.cmake`). Capture :
`scripts/oracle/rejouer-oracle.sh ~/lepton oracles/env-10-r5-apres` sur host + les 7 presets embOS
(variable exportée par `lepton-env.sh`). Même chaîne (Arm GNU Toolchain 14.2.Rel1, `outils.txt`).

| Preset | Sections/symboles | Empreinte | Fumée | Banc KAL | Écarts expliqués |
| --- | --- | --- | --- | --- | --- |
| host | – | – | – | ctest 7/7 = 7/7 ; mklepton identiques | – |
| qemu-mps2-an386-embos | identiques | différente | passée | 18/18 = 18/18 | E1 (démontré) |
| qemu-mps2-an386-embos-soft | identiques | différente | passée | 14/14 = 14/14 | E1 |
| qemu-mps2-an500-embos | identiques | différente | passée | 18/18 = 18/18 | E1 |
| nucleo-f429zi-embos | identiques | différente | – | – | E1 |
| nucleo-wl55jc1-embos | identiques | différente | – | – | E1 |
| stm32f746g-disco-embos | identiques | différente | – | – | E1 |
| samd21-xplained-pro-embos | identiques | différente | – | – | E1 |

`comparer-oracle.py` : code 0 sur les 7 presets. Banc KAL : lignes `Test #` identiques (durées
ignorées). Presets FreeRTOS non rejoués : `embos.cmake` n'est inclus qu'avec `LEPTON_KAL_BACKEND=embos`.

**E1** — date de construction embarquée, comme en R2/R3. Démonstration
(`env-10-r5-preuve-empreintes.sh`, copie du rootstock, `SOURCE_DATE_EPOCH=1760536800`,
qemu-mps2-an386-embos) : `lepton.elf`, `.bin`, `.hex` identiques entre 9ea1b2a et ed46f71
(`oracles/env-10-r5-apres/preuve-e1.log`).

**Sans variable** : `env -u LEPTON_EMBOS_ROOT cmake -S trunk -B build/env-10-r5-o6 --preset
nucleo-f429zi-embos` puis construction : réussies, cache `LEPTON_EMBOS_ROOT:PATH=` vide, bibliothèque
`~/lepton/third_party/embos/cortexm-gcc/5.20.0.0/Start/Lib/libosT7VHLSP.a`. Comparaison à
`env-10-r5-apres/nucleo-f429zi-embos` : symboles et sections de code identiques ; `.debug_line` et
`.debug_str` −28 octets = nom du répertoire de construction (`env-10-r5-o6`, 7 caractères de moins que
`nucleo-f429zi-embos`, 4 occurrences) (`oracles/env-10-r5-apres/o6-sans-variable/`). Répertoire supprimé.

## 3. Validation Mac Intel

| Essai | Résultat |
| --- | --- |
| `pytest` (venv de développement) | 139 verts (137 + 2) |
| `scripts/bout-en-bout.sh` (lepton de la branche) | succès ; `~/lepton` inchangé |
| `shellcheck` `install-vscodium.sh`, `install-macos.sh`, `install-debian.sh` | sans erreur |
| O9, gdb seul (`gdbinit-lepton` sans `target`) | Arm 14.2 : message, `help lepton-stacks` = message ; MacPorts 17.2 : commandes Python présentes |
| O9, NUCLEO-F429ZI (attache sans écriture flash, `env-10-r5-essai-o9.py`) | Arm 14.2 : arrêt dans `OS_Idle`, message « gdb sans Python », `lepton-stacks indisponible` ; MacPorts 17.2 : `lepton-stacks` liste 6 tâches + MSP ; `monitor resume` (`oracles/env-10-r5-apres/essai-o9.log`) |
| O9, `lepton generate` (`essais/env-11/{qemu,f429zi,wl55jc1}`) | `gdbPath` = `/opt/local/bin/arm-none-eabi-gdb` (avant : gdb d'Arm) ; `armToolchainPath` inchangé ; seconde génération sans diff |
| O12, `install-vscodium.sh --dry-run --skip-toolchain` (pipx = `main`, sources = branche) | « paquet installé différent des sources : réinstallation » |
| `install-vscodium.sh --lepton-clone ~/lepton/depots/lepton/original/master --seed-scions …` (utilisateur), 1re | code 0, **2 changements** : lepton réinstallé ; `extensions.autoUpdate` `"off"` → `false` (dérive des réglages de VSCodium d'origine inconnue, corrigée par le script) |
| idem, 2e | **0 changement** ; « lepton 0.1.0 : déjà installé, identique aux sources » ; réglages conformes |
| D3, D4 sur le Mac | `libxml2 @2.15.4` et `clang-21 @21.1.8_3` déjà actifs (`port installed`) : `pkg_install` sans action ; la section `install-macos.sh` de la sortie n'a pas été recopiée par l'utilisateur, le compte global vaut 0 |

VSCodium, Cortex-Debug avec gdb 17.2 (MacPorts) au lieu de 14.2 (Arm), espaces régénérés
(utilisateur, 2026-10-16) :

| Cible | Résultat |
| --- | --- |
| QEMU an386 (`essais/env-11/qemu`, FreeRTOS) | conforme : arrêt sur point d'arrêt `_start_kernel` (`…/qemu/trunk/…/core-freertos/kernel.c:1213`), chemin par le trunk |
| NUCLEO-F429ZI (`essais/env-11/f429zi`, embOS) | conforme : flash, arrêt temporaire sur `main` (`…/f429zi/trunk/…/armv7m/embos_main.c:13`) |
| NUCLEO-WL55JC1 | non rejoué (facultatif) |

## 4. Reste

- Passage VM Debian unique (`consignes/env-10-r5-debian.md`) : D3, D4, O12 (et O9 sous
  `gdb-multiarch`, O6 sans variable), après push (PA-P).
- Fusions locales de `devenv/env-10-r5` (lepton-tools, clone noyau), puis PA-12.
