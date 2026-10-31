# ENV-17 — Cohérence de la documentation et des messages : audit (tâche 1)

Session du 2026-10-31. Lecture seule, avant le PA-21. Références : clone noyau
`<ROOTSTOCK>/depots/lepton/original/master` (`devenv/env-17` = `master` 6f1801d), lepton-tools
`devenv/env-17` (depuis `main` a7bd611), trunk `<ROOTSTOCK>/trunk`.

## 1. Méthode

- Documents relus : noyau `doc/BUILDING.md`, `README.md`, `README-PAQUET.md`, `CLAUDE.md`,
  `scripts/*.sh`, `debug/*` du trunk et `debug/` des BSP, descriptions de `CMakePresets.json` ;
  lepton-tools `README.md`, `extension/README.md`, `doc/devenv/SPECIFICATION.md`,
  `doc/devenv/ORCHESTRATION.md`, `.claude/skills/*/SKILL.md` ; champ `description` des
  7 manifestes famille/BSP.
- Confrontés à : presets de `trunk/CMakePresets.json` (15 presets visibles : `host` + 7 machines ×
  `embos`/`freertos`, + `-soft` an386), existence des chemins (`test -e` dans le trunk ou le
  clone), `DEVENV-STATUS.md` §Versions, sorties de `lepton --help`.
- Messages : `grep -rn 'message(' scion/cmake scion/CMakeLists.txt` du clone noyau (hors
  `FATAL_ERROR`) et des 7 greffons famille/BSP (aucun message dans ces derniers).
- Non relus (PA-15, jamais réécrits) : rapports, passations, `doc/migration/` du noyau
  (`MIGRATION-STATUS.md`, `debug-gcc.md`, `validation-*.md`).

Résultat : les 7 descriptions de manifestes et les descriptions de `CMakePresets.json` sont
exactes ; aucune correction proposée pour eux.

## 2. Corrections proposées

Identifiants `C-n` (documentation) et `M-n` (message CMake). Un commit par dépôt et par nature.

### 2.1 Clone noyau — documentation

| ID | Fichier:ligne | Texte actuel | Correction proposée | Motif |
| --- | --- | --- | --- | --- |
| C-1 | `doc/BUILDING.md:13` | `NUCLEO-F439ZI (validée sur NUCLEO-F429ZI) \| nucleo-f439zi-embos` | `NUCLEO-F429ZI (BSP nucleo-f429zi) \| nucleo-f429zi-embos` | presets renommés en ENV-6 (PA-7 Q7) ; aucun preset `nucleo-f439zi-*` |
| C-2 | `doc/BUILDING.md:10-18, 20` | table limitée aux presets `-embos` ; « Micro-noyau : embOS (port GCC Segger) sur toutes les cibles ARM » | colonne Preset : `…-embos`, `…-freertos` (et `-soft` an386) ; l. 20 : « Micro-noyau : embOS (port GCC Segger 5.20) ou FreeRTOS (V11.3.0), un preset par micro-noyau ; SAMD21 sous FreeRTOS : système complet non supporté (RAM) » | 7 presets `-freertos` dans `CMakePresets.json` ; décision migration 2026-10-06 (deux backends) |
| C-3 | `doc/BUILDING.md:137` | `## 4. Carte NUCLEO-F439ZI (validée sur NUCLEO-F429ZI)` | `## 4. Carte NUCLEO-F429ZI` | idem C-1 ; ENV-20 ajoutera la NUCLEO-F439ZI |
| C-4 | `doc/BUILDING.md:144-146, 154, 163-164, 180-183` | `--preset nucleo-f439zi-embos` (9 occurrences) | `--preset nucleo-f429zi-embos` | idem C-1 |
| C-5 | `doc/BUILDING.md:170` | « Débogage (gdb, OpenOCD, registres de faute) : `doc/migration/debug-gcc.md`. » | ajouter : « Fichiers OpenOCD et gdb de la carte : `sys/root/src/kernel/dev/bsp/nucleo-f429zi/debug/` (`openocd-nucleo-f439zi.cfg`, `gdbinit-nucleo-f439zi`) ; `debug-gcc.md` cite les chemins de la migration (`debug/…`). » | `debug/openocd-nucleo-f439zi.cfg` n'existe plus dans le trunk (déplacé dans le BSP en ENV-6) |
| C-6 | `doc/BUILDING.md:258-259, 275` | `debug/openocd-nucleo-wl55jc1.cfg`, `debug/gdbinit-nucleo-wl55jc1` | `sys/root/src/kernel/dev/bsp/nucleo-wl55jc1/debug/openocd-nucleo-wl55jc1.cfg`, `…/debug/gdbinit-nucleo-wl55jc1` | chemins absents du trunk (`test -e` : NON) ; présents dans le BSP |
| C-7 | `scripts/install-debian.sh:51` | « Épinglé sur le tag 0.5.0.1 (la tête de master lui est postérieure). » | « Épinglé par défaut sur le tag 0.5.2.0 (`SCION_REF`). » | valeur réelle l. 55 (`SCION_REF:-0.5.2.0`, ENV-15) |
| C-8 | `scion/cmake/lepton_greffons.cmake:303` (commentaire) | « champ openocd : un seul fichier jusqu'à ENV-9 » | « champ openocd : un seul fichier » | ENV-9 passée, règle inchangée (l. 340) ; lié à P-2 |

Arbitrages du noyau : §4 (A-1, A-2, A-4).

### 2.2 Clone noyau — messages CMake

| ID | Fichier:ligne | Texte actuel | Correction proposée | Motif |
| --- | --- | --- | --- | --- |
| M-1 | `scion/cmake/components/kernel.cmake:166-168` | `else()` → `message(STATUS "bsp : aucune source pour la carte ${LEPTON_BOARD}")` | `elseif(LEPTON_BOARD AND NOT LEPTON_BOARD_FAMILLE)` ; texte inchangé | affiché à tort pour les 5 BSP par manifeste (leurs sources sont dans la bibliothèque du greffon, `lepton_greffons_appliquer`) et pour `host` (« pour la carte  », nom vide). `LEPTON_BOARD_FAMILLE` est posé par `lepton_greffons_carte` (`lepton_greffons.cmake:365`) avant `include(components/kernel)` (`CMakeLists.txt:39-60`). Reste affiché pour une carte transitoire `cmake/boards` sans `LEPTON_BSP_SOURCES` (aucune aujourd'hui) |
| M-2 | `scion/cmake/components/kernel.cmake:159` | `"lib : aucune source pour LEPTON_ISA=${LEPTON_ISA} (étape 3)"` | retirer « (étape 3) » | renvoi à une étape de la migration ; branche inatteignable aujourd'hui (`LEPTON_LIBC_SOURCES` toujours défini, l. 88 et `isa/host.cmake:30`) |

Les autres messages (`lepton_greffons.cmake:369, 439, 482, 498, 502`, `firmware.cmake:13, 206`,
`tests/kal/CMakeLists.txt:27`) sont exacts.

Effet attendu : journal de configuration seul ; binaires et images mklepton identiques
(oracle avant/après, tâches 2 et 4).

### 2.3 lepton-tools

| ID | Fichier:ligne | Texte actuel | Correction proposée | Motif |
| --- | --- | --- | --- | --- |
| C-9 | `README.md:7` | « État : outil `lepton` 0.1.0 (ENV-8, jalons 1 à 6 ; `lepton generate` ajouté en ENV-9). » | « État : outil `lepton` 0.1.0 (ENV-8 à ENV-16 ; interface : `doc/devenv/rapports/env-8-interface.md`) ; extension Lepton 0.5.1 (`extension/`). » | état arrêté à ENV-9 |
| C-10 | `README.md:14-15` | « macOS Intel et Apple Silicon, Debian » | « macOS Intel et Debian 13 (Apple Silicon : non validé) » | Apple Silicon hors plan (décision 2026-10-31), jamais exécuté |
| C-11 | `README.md:19-22` | liste des commandes sans `seed tree` | ajouter `seed tree` à la liste `lepton seed …` | `lepton seed --help` (ENV-12 lot 5) |
| C-12 | `extension/README.md:36` (après le bloc 0.5.0) | — | « Version 0.5.1 (lot 6 S2) : traceur F8 sans attente (L6-6). » | `package.json` 0.5.1, `dist/lepton-0.5.1.vsix` |
| C-13 | `doc/devenv/ORCHESTRATION.md:21-23, 43` | `<À CONFIRMER en ENV-0>` (4 occurrences) | « résolu en ENV-0 (PA-0) : `DEVENV-STATUS.md` §Emplacements » | marqueurs levés au PA-0 du 2026-10-12, jamais retirés |

### 2.4 Skills (lepton-tools, commit dédié, ligne de journal)

| ID | Fichier:ligne | Texte actuel | Correction proposée | Motif |
| --- | --- | --- | --- | --- |
| C-14 | `.claude/skills/lepton-cibles/SKILL.md:77-80` (après « Flash puis vérification ») | — | « Débogage par l'éditeur (Cortex-Debug) : l'image est écrite par `load` de gdb, sans « verified » dans la console ; preuve du flash, en lecture seule : `openocd -f <cfg> -c "init; reset halt; verify_image <elf>; shutdown"`. NUCLEO-F429ZI : 4 octets `0x080001ac-af` diffèrent (bourrage d'alignement entre `.isr_vector` et `.text`, non écrit par `load`) — attendu ; NUCLEO-WL55JC1 : aucun écart (`rapports/env-12-lot6.md` §10, L6-10). » | L6-10 du bilan ENV-12 |
| C-15 | `.claude/skills/lepton-cibles/SKILL.md:32-34, 41, 44, 46, 48, 70` | références par numéro de ligne : `firmware.cmake:66-86`, `:90-95`, `:131-143` ; `smoke_lsh.py:143-144` ; `tests/kal/CMakeLists.txt:44-45` | références par nom : sorties `lepton.bin`/`.hex` (`firmware.cmake`, `objcopy`), cible `flash`, test `smoke.lsh`, variable `kal_run` ; `smoke_lsh.py` (`--transport qemu`) | numéros décalés (réels : 135-140, 148, 190-197, 144-145, 45-46) |
| C-16 | `.claude/skills/lepton-cibles/SKILL.md:82-83` | « (`doc/migration/debug-gcc.md:18-19`) » | ajouter : « (chemins `debug/…` de la migration : remplacer par ceux du BSP) » | `debug-gcc.md` figé (PA-15), cite `debug/openocd-nucleo-f439zi.cfg` |
| C-17 | `.claude/skills/lepton-oracle/SKILL.md` §1 | — (seule la capture unitaire est décrite) | ajouter : « Série complète : `scripts/oracle/rejouer-oracle.sh <ROOTSTOCK> <oracle> --qemu <P>… --carte <P>…` (construction à neuf, `host` d'abord, fumée et banc KAL des presets QEMU ; liste des 14 presets : `rapports/env-13-graine.md` §4). » | outil utilisé depuis ENV-13, absent de la skill |

## 3. Hors périmètre ou reporté (aucune correction en ENV-17)

| ID | Constat | Renvoi |
| --- | --- | --- |
| H-1 | BSP `nucleo-f429zi` : fichiers `openocd-nucleo-f439zi.cfg` (commentaire l. 1 « NUCLEO-F439ZI (validée sur NUCLEO-F429ZI) »), `gdbinit-nucleo-f439zi`, `nucleo_f439zi_board.c` ; XML `mkconf_tauon_basic_nucleo_f439zi.xml`, `etc/nucleo-f439zi/` | ENV-20 (BSP `nucleo-f439zi`) |
| H-2 | `debug/` du noyau (F746, SAMD21), `cmake/boards/` (2 cartes transitoires), §5-§6 de `BUILDING.md` | ENV-19 |
| H-3 | `tools/migration/mass_compile.py:94-98`, `perimetre_complement.py:90-92` : chemins `bsp/nucleo_f439zi/` de la migration (outils hors CI) | laisser (outils de la migration) |
| H-4 | `doc/migration/debug-gcc.md`, `MIGRATION-STATUS.md` : chemins et versions de la migration | figés (PA-15) ; C-5, C-16, A-1 les signalent |

## 4. Arbitrages demandés

| ID | Sujet | Options | Proposition |
| --- | --- | --- | --- |
| A-1 | `BUILDING.md:5-6, 96-97` et `install-{debian,macos}.sh:105, 126-127, 218-219` renvoient les versions à `doc/migration/MIGRATION-STATUS.md` (figé, scion 0.5.0.1) | (a) renvoyer aux scripts d'installation (`SCION_REF`, toolchain) et à `DEVENV-STATUS.md` §Versions de lepton-tools ; (b) laisser | (a) dans `BUILDING.md` ; scripts : « Versions installées » sans destination |
| A-2 | `CLAUDE.md` du noyau (« État final au 2026-10-06 ») : scion 0.5.0.1 (l. 32, 237), presets `nucleo-f439zi-*` (l. 78), structure sans greffons famille/BSP (l. 87-100) | (a) laisser : document de la migration, assimilé à `doc/migration/` ; (b) corriger les faits cités | (a), avec une ligne en tête renvoyant à `BUILDING.md` et à lepton-tools pour l'état actuel |
| A-3 | `SPECIFICATION.md:10, 67, 71, 169` : Apple Silicon exigé (INS-1, INS-5, NF-3) | (a) annoter « hors plan (décision 2026-10-31), non validé » ; (b) laisser (la spécification décrit la cible) | (a) |
| A-4 | `README.md` du noyau : texte d'origine (anglais, Windows, FreeRTOS 9.0, plateformes anciennes) | (a) laisser ; (b) ajouter en tête un renvoi à `doc/BUILDING.md` (construction GCC/CMake, Linux et macOS, cartes actuelles) | (b), texte d'origine conservé |

## 5. Propositions en attente de confirmation

Les propositions d'ENV-9 (S2, 2026-10-14) et d'ENV-12 (bilan, 2026-10-28) sont déjà confirmées.
Restent :

| ID | Origine | Proposition appliquée | État dans l'arbre |
| --- | --- | --- | --- |
| P-1 | ENV-6, `DEVENV-STATUS.md` l. 147 | démarrage de carte (`demarrage` du BSP) dans l'OBJECT `bsp_demarrage`, lié par `lepton_link_firmware` (exécutif et banc KAL) ; vecteurs et remplaçants forts dans `bsp_objets` (exécutif seul) | en service depuis ENV-6 (`firmware.cmake` l. 1-10) |
| P-2 | ENV-6 lot F4, l. 148 | champ `openocd` du BSP → `LEPTON_BOARD_OPENOCD_CFG`, un seul fichier | inchangé après ENV-9 ; C-8 |
| P-3 | ENV-8 S2, l. 163 ; `rapports/env-8-interface.md` §8 | 8 propositions : préfixe `family-` (repris par ENV-13), configurations `debug-qemu`/`debug-board`, commit de la graine après greffe, ordre de `seed replace`, échec de `seed add`, `-v`/`-C` placés librement, modèles application/bibliothèque sans `CMakeLists.txt`, chemin local relatif au rootstock | en service |
| P-4 | ENV-8 S3, l. 164 ; §9 | 7 propositions : manifeste du BSP dérivé, contrôles et commit de `scion new`, BSP neuf devenu BSP de la graine, règle de destination de `file mv`, `dir remove`, reconfiguration des commandes `file`/`dir`, `graft --scion` par nom de manifeste | en service |
| P-5 | ENV-8 S4, l. 165 ; §10 | 4 propositions : format du verrou, contrôles de `--restore`, fichiers parcourus par CFG-5, contrôles de `check` sans argument | en service |
| P-6 | ENV-10, l. 186 | `install-vscodium.sh` passe `--with-debug-tools` aux scripts du noyau | en service (Mac, Debian) |
| P-7 | après R5, l. 248 | rédaction du protocole §2bis d'ORCHESTRATION | appliqué aux ordres R12-1 à R15-1 |

Proposition : confirmer P-1 à P-7 en bloc, comme le bilan d'ENV-12, sauf amendement.

## 6. Suite (après PA-21)

Tâche 2 (oracle avant, 14 presets, `env-17-avant/`), puis corrections validées, regreffe
`lepton@original::tree`, oracle après et contrôles (tâche 4, PA-22).
