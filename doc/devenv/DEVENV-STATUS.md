# État du chantier « environnement de développement Lepton »

Source unique de l'état. Mis à jour en fin de chaque session (ORCHESTRATION §3).
Dernière mise à jour : 2026-10-15 — ENV-10 en cours (S2 : PA-P accordé, push pour la VM Debian ; validation Debian en attente).

## Prochaine action

ENV-10, session VM Debian (ORCHESTRATION §2) : cloner depuis GitHub `lepton-distribution/lepton-tools` (branche `devenv/env-10`), `lepton-distribution/lepton-original-tree.scions` (branche `devenv/env-10`) et `lepton-distribution/seed.scions` (tag `0.5.1.0`) ; dans lepton-tools, créer `devenv/env-10-debian` ; lancer deux fois `scripts/install-vscodium.sh --lepton-clone <clone noyau> --seed-scions <clone seed.scions>` ; vérifier les critères de `rapports/env-10-validation.md` §3-§4 (`codium --list-extensions --show-versions` = `scripts/extensions.lst`, seconde exécution sans changement, `dpkg-query -W codium` = `1.135.06055`, `codium --version`, `scion version`, `lepton --version`, `shellcheck`) ; écrire `doc/devenv/rapports/env-10-debian.md` (et seulement des corrections propres à Debian), commiter, demander l'accord PA-P puis pousser `devenv/env-10-debian`. Ne pas modifier `DEVENV-STATUS.md` : la session Mac intègre le rapport et clôt ENV-10.

## Étapes

| Étape | Titre | Statut | Branche(s) | Passation |
| --- | --- | --- | --- | --- |
| ENV-0 | Cadrage | terminée (2026-10-12) | lepton-tools `devenv/env-0` | `handoff/env-0.md` |
| ENV-1 | Levée des risques éditeur | terminée (2026-10-12) | lepton-tools `devenv/env-1` | `handoff/env-1.md` |
| ENV-2 | Audit de l'existant | terminée (2026-10-13) | lepton-tools `devenv/env-2` | `handoff/env-2.md` |
| ENV-3 | Schémas | terminée (2026-10-13) | lepton-tools `devenv/env-3` | `handoff/env-3.md` |
| ENV-4 | Format XML de mklepton | terminée (2026-10-13) | lepton-tools `devenv/env-4` ; clone noyau `devenv/env-4` | `handoff/env-4.md` |
| ENV-5 | Restructuration CMake | terminée (2026-10-13) | lepton-tools `devenv/env-5` ; clone noyau `devenv/env-5` | `handoff/env-5.md` |
| ENV-6 | Greffons BSP de référence | terminée (2026-10-13) | `devenv/env-6` : lepton-tools, clone noyau, graine de travail, greffons `qemu-mps2`, `qemu-mps2-an386`, `qemu-mps2-an500`, `stm32f4xx`, `nucleo-f429zi`, `stm32wlxx`, `nucleo-wl55jc1` | `handoff/env-6.md` |
| ENV-7 | Évolutions de scion | terminée (2026-10-13) | lepton-tools `devenv/env-7` ; seed.scions `devenv/env-7` (fusionnée dans `master`, tag 0.5.1.0) | `handoff/env-7.md` |
| ENV-8 | Outil `lepton` | terminée (2026-10-14) | lepton-tools `devenv/env-8` | `handoff/env-8.md` |
| ENV-9 | Fichiers de l'éditeur | terminée (2026-10-14) | lepton-tools `devenv/env-9` ; BSP `nucleo-wl55jc1` `devenv/env-9` | `handoff/env-9.md` |
| ENV-10 | Script d'installation VSCodium | en cours (Mac Intel validé ; Debian reste) | lepton-tools `devenv/env-10` ; clone noyau `devenv/env-10` | `handoff/env-10.md` |
| ENV-11 | Validation de bout en bout | à faire | — | — |
| ENV-12 | Extension VSCodium | à faire | — | — |

Statuts possibles : à faire, en cours, bloquée (raison), terminée (date), abandonnée (décision).

## Emplacements (résolus en ENV-0)

| Clé | Valeur |
| --- | --- |
| `<LEPTON_TOOLS>` | `/Users/cle_d_anton/lepton-tools-dev/lepton-tools` |
| `<ROOTSTOCK>` | `/Users/cle_d_anton/lepton` (rootstock de la migration) |
| `<SEED_SCIONS>` | `/Users/cle_d_anton/lepton-tools-dev/seed.scions` (clone neuf, `master` e0adb2c, tags jusqu'à 0.5.0.1) |
| Branche de départ du clone noyau | `master` (6b62af5) |
| Échange git Mac / VM | Distant GitHub ; chaque push soumis à accord (PA-P) |
| Fichiers générés (ENV-9) | `CMakeUserPresets.json` : `<graine>/project/scion/`, greffé à la racine du trunk (greffon local `lepton@project-<projet>`) ; `<ROOTSTOCK>/<projet>.code-workspace` (non versionné, `launch` et `tasks` intégrés) ; index clangd et `compile_commands.json` du preset actif : `<ROOTSTOCK>/build/.active/` |
| Rootstock de validation (ENV-9) | `~/lepton-tools-dev/essais/env-9` (graine `env9` : an386, freertos, `debug-qemu` + `release-qemu` ; greffons clonés de `~/lepton/depots` en `file://`) |
| Greffons famille et BSP (ENV-6) | Dépôts git locaux `<ROOTSTOCK>/depots/lepton-famille/<nom>` et `<ROOTSTOCK>/depots/lepton-bsp/<nom>` (`master` vide, travail sur `devenv/env-6`), inscrits en version `*` dans la graine de travail `depots/lepton-seed.scions/original-tree` ; familles `qemu-mps2`, `stm32f4xx`, `stm32wlxx` ; BSP `qemu-mps2-an386`, `qemu-mps2-an500`, `nucleo-f429zi`, `nucleo-wl55jc1` |

## Versions épinglées

| Outil | Version | Relevé le |
| --- | --- | --- |
| scion | 0.5.1.0 (tag annoté sur 79f4f96, `master` de `<SEED_SCIONS>`, non poussé) — `~/.local/bin/scion` (pipx `git+file://<SEED_SCIONS>@0.5.1.0`), modules identiques au tag ; 0.5.0.1 (54dc319) auparavant | 2026-10-13 |
| CMake (minimum requis) | 3.24 | décision 2026-10-13 (PA-2 Q6 ; 3.19 le 2026-10-12) |
| CMake (hôte Mac) | 3.31.12 — `/opt/local/bin/cmake` (MacPorts) | 2026-10-12 |
| arm-none-eabi-gcc | 14.2.Rel1 (14.2.1 20241119) — Arm GNU Toolchain, `~/opt/arm-gnu-toolchain-14.2.rel1-darwin-x86_64-arm-none-eabi` (hors MacPorts) | 2026-10-12 |
| QEMU | 11.1.2 — `/opt/local/bin` (MacPorts) | 2026-10-12 |
| OpenOCD | 0.12.0 — `/opt/local/bin` (MacPorts) | 2026-10-12 |
| Python | 3.11.5 — python.org, `/Library/Frameworks/Python.framework` (hors MacPorts) | 2026-10-12 |
| ninja | 1.13.2 — `/opt/local/bin` (MacPorts) | 2026-10-12 |
| MacPorts | 2.12.6 | 2026-10-12 |
| embOS (paquet Segger, hors git) | 5.20.0.0 — `~/lepton/third_party/embos/cortexm-gcc/5.20.0.0`, via `LEPTON_EMBOS_ROOT` (`scripts/lepton-env.sh` du clone noyau) | 2026-10-12 |
| VSCodium | 1.135.06055 (commit 1a46a584) épinglé (PA-10) — `/Applications/VSCodium.app` par `.dmg` vérifié SHA-256 (`scripts/install-vscodium.sh`) ; cask Homebrew retiré ; `codium` = lien `~/.local/bin/codium` | 2026-10-15 |
| Manifeste de greffon | `lepton-greffon.json` dans `sys/root/src/<destination>/` (noyau : `sys/root/src/`), lu par `cmake/lepton_greffons.cmake` du clone noyau ; schéma amendé en ENV-6 (`compilation.<portée>.inclusions`, fichier dans `sources`) ; BSP choisi par `LEPTON_BOARD` = `nom`, XML par `LEPTON_MKCONF` ; champ `openocd` lu (un fichier) | 2026-10-13 |
| Format XML mklepton | 2 (`<mklepton version="2">`, `schemas/mklepton.xsd`) ; format 1 refusé | 2026-10-13 |
| clangd | 21.1.8 — `/opt/local/bin/clangd-mp-21`, MacPorts `clang-21 @21.1.8_3` | 2026-10-12 |
| check-jsonschema | 0.38.2 — pipx (`~/.local/bin`), Python 3.11.5 | 2026-10-13 |
| xmllint (libxml2) | 2.15.4 (21504) — `/opt/local/bin` (MacPorts) | 2026-10-13 |
| lepton | 0.1.0 (jalons 1-6 + `generate` d'ENV-9) — `lepton-tools/pyproject.toml`, build hatchling 1.32.4 ; installé pour l'utilisateur par `pipx install --force <LEPTON_TOOLS>` (`~/.local/bin/lepton`, Python 3.11.5, depuis `devenv/env-9` ffd618c) | 2026-10-14 |
| jsonschema (dépendance de lepton) | 4.26.0 (épinglée dans `pyproject.toml`) | 2026-10-14 |
| pytest | 9.1.1 — extra `[test]`, venv de développement `~/lepton-tools-dev/venv-lepton-tools` (Python 3.11.5, `pip install -e '.[test]'`) | 2026-10-14 |
| Extensions VSCodium | `scripts/extensions.lst` (PA-10) : clangd 0.6.0 ; CMake Tools 1.24.42 ; Cortex-Debug 1.13.0-pre6 + mcu-debug debug-tracker 0.0.15, memory-view 0.0.29, rtos-views 0.0.16, peripheral-viewer 1.6.4 ; CodeLLDB 1.12.3 (paquet de plateforme GitHub) ; vscode-xml 0.29.3 (lemminx natif) ; Claude Code 2.1.300 — Mac Intel conforme | 2026-10-15 |
| shellcheck | 0.11.0 — MacPorts | 2026-10-15 |

## Décisions

Décisions de la spécification : voir `SPECIFICATION.md` §Décisions (1 à 11).
Décisions prises pendant le chantier (une ligne chacune, avec date et point d'arrêt) :

| Date | Point d'arrêt | Décision |
| --- | --- | --- |
| 2026-10-12 | — | Outil `lepton` en Python, dans un nouveau dépôt `lepton-tools` ; orchestration dans `doc/devenv/` de ce dépôt. |
| 2026-10-12 | — | Développement sur l'hôte macOS Intel ; VM Debian réservée à la validation. |
| 2026-10-12 | — | NUCLEO-WL55JC1 : Lepton sur le cœur M4, M0+ non utilisé. Carte supportée et testée pendant le portage. |
| 2026-10-12 | — | Carte STM32F4 de validation : NUCLEO-F429ZI (et non F439ZI). |
| 2026-10-12 | PA-0 | `<LEPTON_TOOLS>` = `~/lepton-tools-dev/lepton-tools` ; `<ROOTSTOCK>` = `~/lepton` (réutilisé) ; `<SEED_SCIONS>` = clone neuf `~/lepton-tools-dev/seed.scions` ; branche noyau `master` ; échange Mac/VM par distant GitHub, push soumis à accord. |
| 2026-10-12 | — (ENV-0) | Oracle de départ sur les 4 presets QEMU mps2-an386 (embos, freertos, embos-soft, freertos-soft), rangé dans `rapports/oracles/env-0/<preset>/` ; sorties de la migration dans `~/lepton/build/` supprimées et reconstruites. |
| 2026-10-12 | — | Après ENV-0 : ENV-1 avant ENV-2. |
| 2026-10-12 | — (ENV-1) | `devenv/env-0` fusionnée localement dans `main` ; `devenv/env-1` créée depuis `main`. Essais ENV-1 en mode mixte (CLI par Claude, GUI par l'utilisateur) ; clangd LLVM via MacPorts. |
| 2026-10-12 | PA-1 | Fichiers ouverts **par le trunk** ; clones pour git seulement (ENV-9 évite leur ouverture sous un second chemin). |
| 2026-10-12 | PA-1 | clangd LLVM, `--compile-commands-dir=<ROOTSTOCK>/build/<preset>`, `--background-index`, `--query-driver=…/arm-none-eabi-gcc` ; rien dans le trunk. |
| 2026-10-13 | — (ENV-2) | `devenv/env-1` fusionnée localement dans `main` ; `devenv/env-2` créée depuis `main`. |
| 2026-10-13 | PA-2 (Q2) | Un greffon commun par famille de puces (couche famille Lepton, ex. `stm32f4xx`, `stm32wlxx`) ; le BSP se limite à l'adaptation à la configuration matérielle de la carte utilisateur (GPIO). |
| 2026-10-13 | PA-2 (Q2) | Le greffon famille porte aussi les pilotes tiers de la famille (SPL F4, HAL CubeWL, SubGHz_Phy, CMSIS device) ; l'initialisation d'horloge (`SystemInit`, PLL/HSE, MSI) reste dans le BSP (dépend de la carte). |
| 2026-10-13 | PA-2 (Q3) | Règle du portage : démarrage générique par ISA/famille (`startup_<isa>.c`) hors BSP ; table de vecteurs par MCU dans le greffon famille ; liaison en bibliothèque OBJECT (remplaçants forts compris). Amende la décision 4 de la spécification. |
| 2026-10-13 | PA-2 (Q4) | Deux BSP sur le greffon famille F4 : `nucleo-f429zi` (carte de validation) et `nucleo-f439zi` (nominal du portage, à rejouer). |
| 2026-10-13 | PA-2 (Q5) | an500, F746, SAMD21 restent construisibles pendant ENV-5/ENV-6 (BSP transitoire) ; non-régression : construction + QEMU an500. |
| 2026-10-13 | PA-2 (Q3) | Le démarrage générique Cortex-M (`startup_armv7m.c`, `startup_armv6m.c`, `sbrk_cortexm.c`, `ld/common-cortexm.ld`) reste dans le greffon noyau (`kernel/core/arch/cortexm`). |
| 2026-10-13 | PA-2 (Q6) | CMake minimum du chantier : 3.24 (`LINK_GROUP`, presets v6), au lieu de 3.19. |
| 2026-10-13 | PA-2 (Q7) | Critère NF-2 d'ENV-7 limité au code fonctionnel : métadonnées (URL, auteur) tolérées ; `INSTALL_LAYOUT` de `rootstock-install` examiné en PA-8. |
| 2026-10-13 | PA-2 (Q8) | Étape suivante : ENV-3. |
| 2026-10-13 | PA-2 (Q1) | Périmètres ENV-4 à ENV-7 validés : `rapports/env-2-synthese.md` §Périmètres validés. |
| 2026-10-13 | — (ENV-3) | `devenv/env-2` fusionnée localement dans `main` (dbbf03e) ; `devenv/env-3` créée depuis `main`. |
| 2026-10-13 | — (ENV-3) | Nouveau type de greffon `famille` (couche Lepton, pilotes tiers, vecteurs par MCU, remplaçants forts), conséquence de PA-2 Q2/Q3. |
| 2026-10-13 | — (ENV-3) | `<cpu freq>` et `<arch include_absolute_path>` retirés du XSD, portés par le manifeste BSP (`frequence_cpu`, `entete_config_noyau`) ; confirmation finale en PA-4. |
| 2026-10-13 | — (ENV-3) | `check-jsonschema` installé par pipx, version épinglée. |
| 2026-10-13 | PA-3 | Schémas `greffon.schema.json`, `graine.schema.json`, `mklepton.xsd` (format 2) validés avec leurs exemples (`schemas/`). |
| 2026-10-13 | PA-3 | `<cpufs>` : `block` et `option` retirés (sans effet dans mklepton) ; `size` et `node` facultatifs — absents, mklepton dimensionne l'image au plus juste (cpufs en lecture seule), présents, valeurs imposées refusées si trop petites ; à implémenter en ENV-4. |
| 2026-10-13 | PA-3 | Origine des greffons (git ou local, GRA-3) portée par `.scion.sources.list` seul ; la graine JSON référence les greffons par nom et rôle. |
| 2026-10-13 | PA-3 | Champs retenus en plus de la liste d'ENV-3 : `abi_flottante`, `frequence_cpu`, `entete_config_noyau` (BSP), `compilation` (tous greffons, CFG-3). |
| 2026-10-13 | PA-3 | `SPECIFICATION.md` amendée (types, GRF-2 CMake 3.24, GRF-3, CFG-8, BLD-1, décision 4) : commit 6e1ef34. |
| 2026-10-13 | — (ENV-4) | ENV-4 avant ENV-5 ; `devenv/env-3` fusionnée localement dans `main` (16bd416) ; `devenv/env-4` créée depuis `main` (lepton-tools) et depuis `master` 6b62af5 (clone noyau). |
| 2026-10-13 | PA-4 | Changements du format XML validés : `rapports/env-4-changements.md` (ajout `version="2"` ; retrait `<target>`/`-t`, `<arch>`, `<cpu>`, `cpufs block/option`, code M16C/`_mk_rtc` ; fusion des `<devices>`). |
| 2026-10-13 | PA-4 | Fréquence et en-tête de carte passés à mklepton par `--cpu-freq` et `--kernel-config-header`, valeurs dans `cmake/boards/*.cmake` (`LEPTON_BOARD_CPU_FREQ`, `LEPTON_BOARD_KERNEL_CONFIG_HEADER`) jusqu'au manifeste BSP. |
| 2026-10-13 | PA-4 | Deux temps : (1) format 2 et migration, empreintes identiques à l'oracle ; (2) retrait de `CPU_*`, nouvelle référence pour `kernel_mkconf.h` seul (ligne `//#define CPU_…`), écart démontré. |
| 2026-10-13 | PA-4 | 23 XML hérités supprimés (aucun preset). Défauts corrigés : débordement `"%s/%s"`, `-r` seul ; `strncat` de `_mk_dir` et `kernel_stub.h` hors périmètre. |
| 2026-10-13 | PA-4 (amendement) | `_mk_rtc` conservé : horloge hôte `dev_host_rtc` (`SOURCE_DATE_EPOCH`), nécessaire à la reproductibilité de l'image ; seuls `MK_DEV_*` et `/dev/kb0` retirés. |
| 2026-10-13 | PA-4 (amendement) | Défaut `/dev/kb0` de `<boot dev>` conservé : écrit dans `.boot` quand `dev` est absent (Olimex). |
| 2026-10-13 | — (ENV-4) | Les 6 XML gardent `cpufs size/node` imposés (empreintes identiques) ; passage en dimensionnement automatique reporté (à décider avec essai sur cartes). |
| 2026-10-13 | — (ENV-4) | ENV-4 terminée ; fusions locales de `devenv/env-4` au début de la session suivante. Aucun push. |
| 2026-10-13 | — (ENV-5) | `devenv/env-4` fusionnée localement dans `main` (lepton-tools, bf95024) et `master` (clone noyau, 49ed8fe) ; `devenv/env-5` créée depuis ces branches. |
| 2026-10-13 | — (ENV-5) | Oracle ENV-5 : capture binaire du preset host et des 14 presets croisés ; fumée et banc KAL sur an386 ×4 et an500 ×2 ; pas de matériel. NUCLEO-F429ZI = presets `nucleo-f439zi-*`. |
| 2026-10-13 | — (ENV-5) | Nom du manifeste de greffon : `lepton-greffon.json` (graine : `lepton-graine.json`). |
| 2026-10-13 | PA-5 | Oracle avant validé : `rapports/env-5-validation.md`, `rapports/oracles/env-5-avant/` (script `scripts/oracle/rejouer-oracle.sh`). |
| 2026-10-13 | — (ENV-5) | Manifestes BSP transitoires : métadonnées seules (fréquence, en-tête de configuration, script de liens, machine QEMU, cœur, ABI, démarrage) lues par CMake ; listes de sources dans `cmake/boards` jusqu'à ENV-6 ; découverte par GLOB prouvée par le greffon d'essai. |
| 2026-10-13 | — (ENV-5) | Code de famille (`kernel/dev/arch`) dans la bibliothèque `kernel` dès ENV-5 ; `bsp` limitée à `kernel/dev/bsp`. |
| 2026-10-13 | — (ENV-5) | Manifestes BSP transitoires reportés à ENV-6 (conflit avec le schéma : chemins hors `kernel/dev/bsp`, répertoire `qemu_mps2` partagé) ; ENV-5 : manifeste du noyau, lecteur, greffon d'essai ; démarrage générique, vecteurs F4 et `hal_tick` WL en OBJECT ; démarrage de carte en OBJECT avec le découpage d'ENV-6. Amende la décision « métadonnées seules » du même jour. |
| 2026-10-13 | — (ENV-5) | Emplacement du manifeste : `sys/root/src/<destination>/lepton-greffon.json` (la racine `scion/` est commune aux greffons : conflit scion) ; `destination` contrôlée par CMake ; description du schéma mise à jour. |
| 2026-10-13 | PA-6 | Non-régression ENV-5 validée (`rapports/env-5-validation.md`) : symboles identiques sur 14 presets, écarts de sections = remplissage (démontré), fumée et banc KAL identiques ; ENV-5 terminée ; fusions locales au début de la session suivante. Aucun push. |
| 2026-10-13 | — (ENV-6) | `devenv/env-5` fusionnée localement dans `main` (lepton-tools, 4d22d67) et `master` (clone noyau, 1551afb) ; `devenv/env-6` créée depuis ces branches et dans la graine de travail `depots/lepton-seed.scions/original-tree` (depuis `original-tree` 083c30b). |
| 2026-10-13 | — (ENV-6) | ENV-6 par lots bornés : session 1 = PA-7 (toutes cartes), lecteur CMake, lot QEMU ; lots F4 puis WL dans les sessions suivantes. |
| 2026-10-13 | — (ENV-6) | Dépôts git des greffons famille et BSP locaux sous `<ROOTSTOCK>/depots/`, inscrits en version `*` ; graine de travail modifiée et commitée sur sa branche `devenv/env-6`, sans push. |
| 2026-10-13 | PA-7 | Liste d'extraction validée : `rapports/env-6-extraction.md` (règles R1-R9, lots QEMU, F4, WL). Q1 : `compilation.<portée>.inclusions` (relatifs à `sys/root/src`) ajouté au schéma ; Q2 : `sources` accepte un fichier ; Q3 : `CMakeLists.txt` facultatif du BSP inclus par le lecteur ; Q4 : XML mkconf, `.boot`, `.init` dans le noyau, choisis par `LEPTON_MKCONF` (preset) ; Q5 : `user_kernel_mkconf.h` dans le BSP, nouvelle référence d'empreintes mklepton ; Q6 : BSP an500 dans le lot QEMU (fichiers dupliqués) ; Q8 : `debug/gdbinit-lepton` générique dans le noyau ; Q9 : F746 et SAMD21 transitoires dans le noyau ; Q10 : `stm32_radio_target/` dans le BSP WL ; Q11 : `svd` omis en ENV-6 ; Q12 : `kernel/dev/bsp/<nom du greffon>`. |
| 2026-10-13 | PA-7 (Q7) | BSP `nucleo-f429zi` = code actuel ; sort du BSP `nucleo-f439zi` (copie déclarant `STM32F429xx` ou report après ENV-6) : à trancher au début du lot F4. |
| 2026-10-13 | PA-7 (Q7, tranché) | BSP `nucleo-f439zi` reporté après ENV-6 (PA-2 Q4 maintenue, échéance repoussée) ; lot F4 = famille `stm32f4xx` + BSP `nucleo-f429zi` seul ; presets renommés `nucleo-f429zi-*`. |
| 2026-10-13 | — (ENV-6) | Démarrage de carte (`demarrage` du BSP) dans l'OBJECT `bsp_demarrage`, lié par `lepton_link_firmware` (exécutif et banc KAL) ; vecteurs et remplaçants forts de la famille dans `bsp_objets`, lié à l'exécutif seul, comme avant. Proposition appliquée, à confirmer. |
| 2026-10-13 | — (ENV-6, lot F4) | Lecteur : champ `openocd` du BSP → `LEPTON_BOARD_OPENOCD_CFG` ; un seul fichier accepté jusqu'à ENV-9. Proposition appliquée, à confirmer. |
| 2026-10-13 | — (ENV-6, lot F4) | Noms de fichiers du BSP `nucleo-f429zi` conservés (`nucleo_f439zi_*`, `mem_nucleo-f439zi.ld`, `openocd-`/`gdbinit-nucleo-f439zi`, R3) ; XML mkconf et `etc/nucleo-f439zi/` inchangés (Q4). |
| 2026-10-13 | — (ENV-6, lot F4) | Signalés, non déplacés (hors liste PA-7, non compilés) : `kernel/usb/stm32f4-usb-core/`, démos `freeRTOS_{8-0-0,9-0-0}/…/stm32f4/` ; table de vecteurs de la famille liée par symbole aux gestionnaires du BSP (à revoir avant un second BSP F4). |
| 2026-10-13 | PA-7 (lot WL) | Liste WL revérifiée (`ninja -t deps`), identique au §4. Relais IRQ11/12/37/50 sortis de `stm32wl55jci_nucleo_system.c` vers la famille (`vecteurs/stm32wl55xx_vectors.c`). OpenOCD : manifeste `openocd` = cfg statique du BSP, cfg enveloppe générée par le `CMakeLists.txt` du BSP (remplace `LEPTON_BOARD_OPENOCD_CFG`). Radio : `dev_stm32wlxx_bsp_radio_if.c` (famille) inclut `radio_board_if.h` par nom, inclusions publiques radio dans le BSP. `sys/user/tauon-basic/src/arch/st-stm32wl55jci-nucleo/` (IAR, non utilisé) laissé, signalé. |
| 2026-10-13 | — (ENV-6) | ENV-6 terminée. Cartes validées : QEMU an386 ×4, an500 ×2 (construction, fumée, banc KAL identiques) ; NUCLEO-F429ZI ×2 et NUCLEO-WL55JC1 ×2 (construction, symboles identiques, écarts de sections expliqués : `rapports/env-6-validation.md`) ; flash et fumée série en ENV-11 (PA-11). Fusions locales de `devenv/env-6` au début de la session suivante. Aucun push. |
| 2026-10-13 | — (ENV-7) | `devenv/env-6` fusionnée localement (`--no-ff`) : lepton-tools `main` f4a8088, clone noyau `master` 42733ce, graine `original-tree` 43d12e6, 7 greffons famille/BSP `master` ; branches cibles extraites dans le rootstock (trunk inchangé, 4 037 feuilles) ; `devenv/env-7` créée depuis `main` (lepton-tools). |
| 2026-10-13 | PA-8 | Évolutions de scion retenues : E1 à E6 de `rapports/env-7-evolutions.md` §2 telles quelles (`seed-scion-add [--replace]`, `seed-scion-remove`, `graft-remove [--purge]`, `graft --scion`, sortie de `scion git`, conflits fichier / répertoire) ; E7 : option B, `rootstock-install --bare` (layout par défaut conservé). |
| 2026-10-13 | PA-8 | Version cible 0.5.1.0 ; `devenv/env-7` de `<SEED_SCIONS>` créée depuis `master` e0adb2c (et non le tag) ; critère de test : `python3 -m unittest discover -s tests` (pytest non installé). |
| 2026-10-13 | PA-8 (tag) | `devenv/env-7` de seed.scions fusionnée localement dans `master` (79f4f96, `--no-ff`), tag annoté `0.5.1.0`, installation pipx depuis le tag ; aucun push. |
| 2026-10-13 | — (ENV-7) | ENV-7 terminée : `rapports/env-7-evolutions.md` §6 (104 tests, NF-2, essai sur copie, regreffe de `<ROOTSTOCK>` identique). Fusion locale de `devenv/env-7` (lepton-tools) au début de la session suivante. Aucun push. |
| 2026-10-14 | — (ENV-8) | `devenv/env-7` fusionnée localement dans `main` (lepton-tools, a26c9b8, `--no-ff`) ; `devenv/env-8` créée depuis `main`. Session 1 d'ENV-8 : PA-9 puis jalon 1 si tranché. |
| 2026-10-14 | PA-9 | Interface de `lepton` 0.1 validée : `rapports/env-8-interface.md` (§1-§5, décisions §7). Options, métavariables, modules et répertoires créés par `lepton` en anglais US (§5bis) ; messages et documentation en français ; noms fixés par scion, les schémas (enums), les manifestes et ENV-6 inchangés en 0.1 (Q10). |
| 2026-10-14 | PA-9 (Q1-Q7, Q9, Q11) | Sous-commande `lepton scion` ; `jsonschema` dépendance d'exécution, `pytest` en extra `[test]` dans le venv `~/lepton-tools-dev/venv-lepton-tools` (accès PyPI accordé) ; graine créée dans `depots/lepton-seed/<NAME>` ; `--origin` obligatoire pour famille et BSP ; `--mkconf` obligatoire ; `scion new` : `bin/<NAME>`, `lib/<NAME>`, BSP `--from` ; pas de `git add` implicite ; sessions S1 (PA-9, jalon 1), S2 (jalons 2-3), S3 (4-5), S4 (6, bout en bout, pipx) ; clés `--json` en anglais. |
| 2026-10-14 | PA-9 (Q8) | `.DS_Store` et `._*` ignorés par `lepton` : jamais signalés ; supprimés du trunk avant `scion graft` s'ils sont réguliers (jamais un lien) ; liens venus des clones conservés en 0.1 ; filtre générique de scion (fichiers ignorés par git) = reliquat hors ENV-8. |
| 2026-10-14 | — (ENV-8 S2) | `--origin` : noyau désigné par `lepton-noyau` (nom du manifeste) ; `templates/bsp/` = manifeste squelette, champs matériels repris du BSP `--from` ; URL sans `@VERSION` → `master`, chemin local → `*` (`@VERSION` refusé). |
| 2026-10-14 | — (ENV-8 S2) | Clés scion des greffons créés par lepton : `<kind>-<nom>` sans suffixe (`bsp-`, `application-`, `library-`) au lieu de `<kind>::<nom>` : scion clone une origine distante dans `depots/<shelf>/<préfixe>/<version>`. Amende PA-9 Q10. Propositions à confirmer : `rapports/env-8-interface.md` §8. |
| 2026-10-14 | — (ENV-8 S3) | S3-1 : `scion new --type bsp --from SRC` remplace, dans les fichiers texte copiés, la destination `kernel/dev/bsp/<SRC>` par la destination neuve ; noms de fichiers et identifiants C conservés. S3-2 : fichiers copiés = suivis par git du répertoire du BSP source greffé (arbre de travail). Propositions à confirmer : `rapports/env-8-interface.md` §9. |
| 2026-10-14 | — (ENV-8 S4) | S4-1 : `seed lock` → `lepton-graine.lock.json`, `--verify` (code 1 si écart), `--restore` = `git checkout <commit>` des clones propres d'origine distante puis regreffe ; origine locale `*` vérifiée seulement, jamais modifiée. S4-2 : CFG-5 par recherche textuelle des définitions (`dev_map_t dev_X_map =`, `int X_main(`) dans les `.c` des greffons greffés. S4-3 : bout en bout `scripts/bout-en-bout.sh REPERTOIRE`. S4-4 : `pipx install` de lepton pour l'utilisateur. Propositions d'application à confirmer : `rapports/env-8-interface.md` §10. |
| 2026-10-14 | — (ENV-8) | ENV-8 terminée ; fusion locale de `devenv/env-8` au début de la session suivante. Aucun push. |
| 2026-10-14 | — (ENV-9) | `devenv/env-8` fusionnée localement dans `main` (lepton-tools, ba13caa, `--no-ff`) ; `devenv/env-9` créée depuis `main`. Tâche 2 (`-ffile-prefix-map`) sans objet (PA-1) : clone noyau non touché. |
| 2026-10-14 | — (ENV-9) | Emplacements : `CMakeUserPresets.json` versionné dans le dépôt de graine sous `project/scion/`, greffé dans le trunk par une entrée scion locale `project-<nom>` (chemin dans le dépôt `project`) et héritant des presets cachés du noyau ; `<ROOTSTOCK>/<projet>.code-workspace` non versionné, `launch` et `tasks` intégrés, aucun `.vscode/` dans le trunk ni dans un clone. |
| 2026-10-14 | — (ENV-9) | Rootstock de validation durable `~/lepton-tools-dev/essais/env-9` (`lepton seed new`, greffons clonés depuis `~/lepton` en `file://`) ; sessions S1 (`lepton generate`, tests, essais CLI) et S2 (validation VSCodium, `rapports/env-9-validation.md`). |
| 2026-10-14 | — (ENV-9) | Débogage carte : `configFiles` = champ `openocd` du BSP tel quel ; cfg OpenOCD du BSP `nucleo-wl55jc1` rendue autonome (`interface/stlink.cfg`), enveloppe générée réduite à `adapter serial` (branche `devenv/env-9` du clone, 9489e7d ; sans carte : `openocd -c shutdown` ; sections et symboles identiques à l'oracle `env-6-lot-wl`). Flash réel en ENV-11. |
| 2026-10-14 | — (ENV-9) | Propositions appliquées, à confirmer en S2 : `rapports/env-9-generation.md` §4 (P1 table cœur → ISA, P2 cœur QEMU, P3 choix de clangd, P4 `build/.active` pour clangd, P5 clones en dossiers, P6 noms, P7 pas de `--no-cmake`, P8 greffon projet hors verrou, P9 chemins absolus). |
| 2026-10-14 | — (ENV-9 S2) | P1-P4 et P6-P9 de `rapports/env-9-generation.md` §4 validées telles qu'appliquées. |
| 2026-10-14 | — (ENV-9 S2) | P5 : fichiers greffés masqués dans les dossiers `git · …` de l'espace (`files.exclude` `scion/[!.]*`, `project/scion`) ; P10 : diagnostics include-cleaner de clangd laissés ; R1 (fichiers ouverts gardant l'ancienne commande après changement de preset) documentée, solution intégrée en ENV-12 (`rapports/env-9-validation.md` §3-§4). |
| 2026-10-14 | — (ENV-9) | ENV-9 terminée ; fusions locales de `devenv/env-9` (lepton-tools, BSP `nucleo-wl55jc1`) au début de la session suivante. Aucun push. |
| 2026-10-15 | — (ENV-10) | `devenv/env-9` fusionnée localement (`--no-ff`) : lepton-tools `main` f6bb974, BSP `nucleo-wl55jc1` `master` a329f4d (extraite dans `~/lepton`, `scion graft --scion lepton@bsp::nucleo-wl55jc1`, trunk 4 037 feuilles, propre) ; `devenv/env-10` créée depuis `main` (lepton-tools) et `master` 42733ce (clone noyau). |
| 2026-10-15 | — (ENV-10) | Constat : VSCodium 1.135.06055 du Mac Intel installé par Homebrew cask (et non à la main) ; Homebrew 7.0.8 présent (`/usr/local`, dont `open-ocd` masqué par MacPorts) ; pas de port MacPorts `vscodium`. |
| 2026-10-15 | — (ENV-10, D1) | scion : variable `SCION_SPEC` (source pipx, défaut inchangé) dans `install-macos.sh` / `install-debian.sh` du clone noyau (branche `devenv/env-10`), réinstallation Debian seulement si la version diffère ; `install-vscodium.sh` passe `git+file://<SEED_SCIONS>@0.5.1.0`. |
| 2026-10-15 | — (ENV-10, D2) | Scripts de la chaîne trouvés par `--lepton-clone DIR` (défaut `$LEPTON_CLONE`) ; absents sans `--skip-toolchain` → arrêt avec la marche à suivre. |
| 2026-10-15 | — (ENV-10, D3) | Validation Mac Intel : VSCodium du cask désinstallé (accord au moment voulu) puis installé par le `.dmg` épinglé. |
| 2026-10-15 | PA-10 | Extensions (Open VSX) : clangd 0.6.0, cmake-tools 1.24.42, cortex-debug 1.13.0-pre6, mcu-debug debug-tracker 0.0.15 / memory-view 0.0.29 / rtos-views 0.0.16 / peripheral-viewer 1.6.4, vscode-lldb 1.12.3, vscode-xml 0.29.3 (lemminx natif par plateforme, sans Java), claude-code 2.1.300. |
| 2026-10-15 | PA-10 | VSCodium 1.135.06055 épinglé : `.dmg` x64 (Mac Intel) et arm64 (Apple Silicon, au lieu du cask non épinglable), `.deb` amd64 (Debian ; le dépôt APT ne sert que la dernière version), SHA-256 publiés vérifiés. |
| 2026-10-15 | PA-10 | CodeLLDB : `codelldb-<plateforme>.vsix` de la release GitHub v1.12.3, SHA-256 épinglé (l'amorce d'Open VSX télécharge au premier lancement). |
| 2026-10-15 | PA-10 | Réglages utilisateur de VSCodium fusionnés par le script (sauvegarde `.bak`) : `update.mode` `none`, `extensions.autoUpdate` et `extensions.autoCheckUpdates` `false`, `redhat.telemetry.enabled` `false`, `xml.server.preferBinary` `true`. |
| 2026-10-15 | — (ENV-10) | Effet de bord de `brew uninstall --cask vscodium` : nettoyage automatique de Homebrew (au moins `imath` 3.1.12, `libdeflate` 1.22 retirées ; chaîne MacPorts non concernée). `codium` lié dans `~/.local/bin` (décision utilisateur). |
| 2026-10-15 | PA-P | Pas de push en fin de S1 ; push pour la VM Debian décidé au début de la session suivante. |
| 2026-10-15 | — (ENV-10) | `install-vscodium.sh` passe `--with-debug-tools` aux scripts du noyau (OpenOCD et gdb font partie de la chaîne d'INS-3). Proposition appliquée, à confirmer. |
| 2026-10-15 | PA-P (ENV-10 S2) | Dépôt GitHub `lepton-distribution/lepton-tools` créé par l'utilisateur, distant `origin` en SSH. Push accordé : lepton-tools `main` + `devenv/env-10` ; clone noyau `master` (42733ce, avance rapide depuis 6b62af5) + `devenv/env-10` ; seed.scions `master` (79f4f96) + tag `0.5.1.0`, poussés par l'URL SSH (`origin` HTTPS inchangé). La session Mac attend le rapport Debian, l'intègre et clôt ENV-10. |
| 2026-10-12 | PA-1 | Débogage sans `-ffile-prefix-map` ni `substitute-path` ; écart accepté en phase 1 : à l'arrêt, source affiché sous le chemin du clone (`fullname` GDB) ; résorption éventuelle en ENV-12. |

## Journal

| Date | Étape | Résumé (une ligne) |
| --- | --- | --- |
| 2026-10-12 | — | Plan créé : 13 étapes ENV-0 à ENV-12. |
| 2026-10-12 | — | Ajout des skills devenv-session, lepton-rootstock, lepton-oracle, lepton-cibles, du hook proteger-trunk.py et des scripts d'oracle ; MacPorts sur Mac Intel. |
| 2026-10-12 | ENV-0 | Session 1 : PA-0 tranché, dépôt git initialisé, seed.scions cloné, rootstock et versions vérifiés ; arrêt en tâche 5 (hook non chargé, session lancée depuis le dossier parent). |
| 2026-10-12 | ENV-0 | Session 2 : hook vérifié (refus), oracle des 4 presets an386 capturé (ctest 100 %), rapport `rapports/env-0-reference.md` ; étape terminée. |
| 2026-10-12 | ENV-1 | Essais clangd, sauvegarde via lien, GDB/Cortex-Debug, git multi-racines ; rapport `rapports/env-1-essais.md` ; PA-1 tranché ; étape terminée. |
| 2026-10-13 | ENV-2 | Audit CMake, mklepton, cartes, scion, outillage et lecture intégrale de la doc du portage (`rapports/env-2-*.md`) ; skill `lepton-cibles` complétée ; PA-2 tranché (Q1-Q8) ; étape terminée. |
| 2026-10-13 | ENV-3 | Schémas greffon (type famille ajouté), graine, XSD mklepton format 2, 12 exemples valides et 28 invalides, `scripts/valider-schemas.sh` conforme ; PA-3 tranché (cpufs auto) ; spécification amendée ; étape terminée. |
| 2026-10-13 | ENV-4 | PA-4 tranché ; mklepton format 2 (version, `--cpu-freq`, `--kernel-config-header`, cpufs automatique, test `host.mklepton_format`) ; 6 XML migrés, 23 supprimés ; pilote hôte `dev_host_fileflash` (accès hors disque) ; non-régression `rapports/env-4-validation.md` ; étape terminée. |
| 2026-10-13 | ENV-5 | PA-5 et PA-6 tranchés ; bibliothèques `kernel`, `lib`, `sbin`, `bin`, `bsp`, OBJECT `generated`/`kernel_demarrage`/`bsp_objets`, lecteur `cmake/lepton_greffons.cmake`, manifeste noyau, HEX et occupation par bibliothèque ; greffon d'essai ; non-régression `rapports/env-5-validation.md` ; étape terminée. |
| 2026-10-13 | ENV-6 | Session 1 : oracle avant ; PA-7 tranché (`rapports/env-6-extraction.md`) ; schéma amendé ; lecteur famille/BSP ; lot QEMU (famille `qemu-mps2`, BSP an386 et an500) extrait et greffé ; non-régression `rapports/env-6-validation.md` ; lots F4 et WL restent. |
| 2026-10-13 | ENV-6 | Session 2 : Q7 tranché (BSP F439ZI reporté) ; lot F4 (famille `stm32f4xx`, BSP `nucleo-f429zi`, presets `nucleo-f429zi-*`, `gdbinit-lepton`, `openocd` lu par le lecteur) ; non-régression `env-6-validation.md` §Lot F4, `oracles/env-6-lot-f4/` ; skill `lepton-cibles` mise à jour ; lot WL reste. |
| 2026-10-13 | ENV-6 | Session 3 : PA-7 lot WL tranché ; lot WL (famille `stm32wlxx`, BSP `nucleo-wl55jc1`, vecteurs dans la famille, cfg OpenOCD générée par le BSP) ; non-régression `env-6-validation.md` §Lot WL, `oracles/env-6-lot-wl/` (`.data` WL : remplissage, démontré sur copie d'essai) ; skill `lepton-cibles` ; étape terminée. |
| 2026-10-13 | ENV-7 | Fusions locales de `devenv/env-6` ; PA-8 tranché (E1-E6, `--bare`, 0.5.1.0) ; scion 0.5.1.0 : `seed-scion-add/remove`, `graft --scion`, `graft-remove [--purge]`, `rootstock-install --bare`, sortie de `scion git`, conflits fichier / répertoire (écriture dans un clone corrigée) ; 104 tests ; tag et installation ; skill `lepton-rootstock` ; étape terminée. |
| 2026-10-14 | ENV-8 | Session 1 : fusion locale de `devenv/env-7` ; PA-9 tranché (`rapports/env-8-interface.md`, nommage anglais US des options et répertoires, `.DS_Store` ignorés) ; jalon 1 : paquet `lepton` 0.1.0, `--version`, `check FILE` (JSON Schema, XSD par xmllint), 56 tests pytest verts, pipx vérifié ; jalons 2-6 restent. |
| 2026-10-14 | ENV-8 | Session 2 : jalon 2 (modèles graine, BSP squelette, application, bibliothèque ; `templates.py`) ; jalon 3 (`rootstock.py`, `seed new/status/add/remove/replace`, clés `<kind>-<nom>`) ; 82 tests pytest verts ; `seed new` réel (noyau + famille + BSP an386) dans le scratchpad ; `~/lepton` lu seulement ; jalons 4-6 restent. |
| 2026-10-14 | ENV-8 | Session 3 : jalon 4 (`scions.py` : `scion new` application, bibliothèque, BSP `--from` ; `scion remove`) ; jalon 5 (`files.py` : `file add/remove/mv`, `dir add/remove`, `graft`) ; rôle « non utilisé » dans `seed status` ; 98 tests pytest verts ; essai réel : BSP dérivé d'an386 construit (freertos) et `smoke.lsh` passé ; jalon 6 reste. |
| 2026-10-14 | ENV-8 | Session 4 : jalon 6 (`check` sans argument : schémas, contrôles non exprimables, GRA-2, GRF-5, CFG-5 ; `seed lock [--verify \| --restore]`) ; 106 tests pytest verts ; `scripts/bout-en-bout.sh` (seed new an386 → check → lock → cmake → `smoke.lsh` passé, `~/lepton` inchangé) ; lepton installé par pipx ; étape terminée. |
| 2026-10-14 | ENV-9 | Session S1 : fusion locale de `devenv/env-8` ; emplacements décidés ; `lepton generate` (presets greffés depuis la graine, `.code-workspace` avec launch/tasks) ; 116 tests verts, bout en bout vert ; rootstock d'essai `essais/env-9` : `--list-presets`, idempotence, BLD-5 (binaires identiques à `SOURCE_DATE_EPOCH` égal), fumée, KAL 18/18, arrêt sur `main` en GDB ; cfg OpenOCD WL autonome ; rapport `rapports/env-9-generation.md` ; S2 (VSCodium) reste. |
| 2026-10-14 | ENV-9 | Session S2 : validation VSCodium (`rapports/env-9-validation.md`) — IDE-2 à IDE-5, DBG-1, DBG-2, TST-1 validés (réserves R1-R3, R3 = écart PA-1) ; P1-P10 tranchées ; P5 intégrée (`files.exclude`), 116 tests et bout en bout verts ; étape terminée. |
| 2026-10-15 | ENV-10 | Session S1 : fusions locales de `devenv/env-9` ; PA-10 tranché ; `SCION_REF`/`SCION_SPEC` dans les scripts du noyau ; `scripts/install-vscodium.sh` + `extensions.lst` ; Mac Intel : 5 changements puis 0, critères conformes (`rapports/env-10-validation.md`) ; Debian reste. |
| 2026-10-15 | ENV-10 | Session S2 : PA-P accordé (dépôt GitHub lepton-tools, push lepton-tools, clone noyau, seed.scions + tag 0.5.1.0) ; consigne de la session VM Debian. |
