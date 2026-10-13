# État du chantier « environnement de développement Lepton »

Source unique de l'état. Mis à jour en fin de chaque session (ORCHESTRATION §3).
Dernière mise à jour : 2026-10-13 — ENV-5 en cours.

## Prochaine action

Démarrer ENV-5 (restructuration CMake du greffon noyau) d'après `etapes/ENV-05-cmake.md` et `handoff/env-4.md` : d'abord fusionner localement `devenv/env-4` dans `main` (lepton-tools) et dans `master` (clone noyau), puis créer `devenv/env-5` depuis ces branches ; PA-5 (oracle) avant toute modification CMake.

## Étapes

| Étape | Titre | Statut | Branche(s) | Passation |
| --- | --- | --- | --- | --- |
| ENV-0 | Cadrage | terminée (2026-10-12) | lepton-tools `devenv/env-0` | `handoff/env-0.md` |
| ENV-1 | Levée des risques éditeur | terminée (2026-10-12) | lepton-tools `devenv/env-1` | `handoff/env-1.md` |
| ENV-2 | Audit de l'existant | terminée (2026-10-13) | lepton-tools `devenv/env-2` | `handoff/env-2.md` |
| ENV-3 | Schémas | terminée (2026-10-13) | lepton-tools `devenv/env-3` | `handoff/env-3.md` |
| ENV-4 | Format XML de mklepton | terminée (2026-10-13) | lepton-tools `devenv/env-4` ; clone noyau `devenv/env-4` | `handoff/env-4.md` |
| ENV-5 | Restructuration CMake | en cours | lepton-tools `devenv/env-5` ; clone noyau `devenv/env-5` | — |
| ENV-6 | Greffons BSP de référence | à faire | — | — |
| ENV-7 | Évolutions de scion | à faire | — | — |
| ENV-8 | Outil `lepton` | à faire | — | — |
| ENV-9 | Fichiers de l'éditeur | à faire | — | — |
| ENV-10 | Script d'installation VSCodium | à faire | — | — |
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

## Versions épinglées

| Outil | Version | Relevé le |
| --- | --- | --- |
| scion | 0.5.0.1 (tag 54dc319) — `~/.local/bin/scion` (pipx), code identique au tag | 2026-10-13 |
| CMake (minimum requis) | 3.24 | décision 2026-10-13 (PA-2 Q6 ; 3.19 le 2026-10-12) |
| CMake (hôte Mac) | 3.31.12 — `/opt/local/bin/cmake` (MacPorts) | 2026-10-12 |
| arm-none-eabi-gcc | 14.2.Rel1 (14.2.1 20241119) — Arm GNU Toolchain, `~/opt/arm-gnu-toolchain-14.2.rel1-darwin-x86_64-arm-none-eabi` (hors MacPorts) | 2026-10-12 |
| QEMU | 11.1.2 — `/opt/local/bin` (MacPorts) | 2026-10-12 |
| OpenOCD | 0.12.0 — `/opt/local/bin` (MacPorts) | 2026-10-12 |
| Python | 3.11.5 — python.org, `/Library/Frameworks/Python.framework` (hors MacPorts) | 2026-10-12 |
| ninja | 1.13.2 — `/opt/local/bin` (MacPorts) | 2026-10-12 |
| MacPorts | 2.12.6 | 2026-10-12 |
| embOS (paquet Segger, hors git) | 5.20.0.0 — `~/lepton/third_party/embos/cortexm-gcc/5.20.0.0`, via `LEPTON_EMBOS_ROOT` (`scripts/lepton-env.sh` du clone noyau) | 2026-10-12 |
| VSCodium (essai ENV-1, installé à la main) | 1.135.06055 (commit 1a46a584) — `/Applications/VSCodium.app` ; version épinglée à fixer en ENV-10 | 2026-10-12 |
| Format XML mklepton | 2 (`<mklepton version="2">`, `schemas/mklepton.xsd`) ; format 1 refusé | 2026-10-13 |
| clangd | 21.1.8 — `/opt/local/bin/clangd-mp-21`, MacPorts `clang-21 @21.1.8_3` | 2026-10-12 |
| check-jsonschema | 0.38.2 — pipx (`~/.local/bin`), Python 3.11.5 | 2026-10-13 |
| xmllint (libxml2) | 2.15.4 (21504) — `/opt/local/bin` (MacPorts) | 2026-10-13 |
| Extensions VSCodium (essai ENV-1, Open VSX) | clangd 0.6.0 ; CMake Tools 1.24.42 ; Cortex-Debug 1.13.0-pre6 (pré-version) + mcu-debug rtos-views 0.0.16, peripheral-viewer 1.6.4, memory-view 0.0.29, debug-tracker 0.0.15 | 2026-10-12 |

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
