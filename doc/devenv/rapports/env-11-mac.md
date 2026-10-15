# ENV-11 — Validation de bout en bout, hôte Mac Intel

Session S1 (2026-10-15) : scénario §2 étapes 1 à 4, 8 et 9 (partie ligne de commande), plus la
préparation des étapes 5-6. Session S2 (2026-10-15) : étapes 5, 6, 7 et partie éditeur de 9, en mode
mixte (ligne de commande par Claude, VSCodium manipulé par l'utilisateur) ; §2bis.

## 1. Cadre

| Élément | Valeur |
| --- | --- |
| Hôte | Mac mini Intel, macOS (Darwin 24.6.0) |
| Outils | scion 0.5.1.0, lepton 0.1.0 (pipx, depuis `devenv/env-11` après 7d191aa), CMake 3.31.12, GCC 14.2.Rel1, QEMU 11.1.2, OpenOCD 0.12.0, VSCodium 1.135.06055 |
| Rootstocks d'essai (non versionnés) | `~/lepton-tools-dev/essais/env-11/{qemu,f429zi,wl55jc1}` ; journaux `essais/env-11/logs/` |
| Origine des greffons | `file://localhost~/lepton/depots/…@master` (comme `scripts/bout-en-bout.sh`) |
| Graines | `env11` (an386, FreeRTOS), `env11f4` (NUCLEO-F429ZI, embOS), `env11wl` (NUCLEO-WL55JC1, FreeRTOS) : une graine par carte (décision du 2026-10-15) |
| Référence `~/lepton` | HEAD et `status` de 9 dépôts relevés avant et après : identiques (`essais/env-11/ref-{avant,apres}.txt`) |

## 2. Scénario

| Étape | Commande (résumé) | Résultat | Exigences |
| --- | --- | --- | --- |
| 2.1 | `scripts/install-vscodium.sh --lepton-clone ~/lepton/depots/lepton/original/master --seed-scions ~/lepton-tools-dev/seed.scions` | code 0, `install-macos.sh` appelé, **0 changement**, aucun `sudo` (5 s) | INS-1 à INS-6 |
| 2.2 | `lepton seed new env11 -C …/qemu --bsp qemu-mps2-an386 --backend freertos --mkconf sys/user/tauon-basic/etc/mkconf_tauon_basic_qemu_mps2.xml --origin …` (noyau, famille, BSP ; aucune application) | code 0 ; `lepton check` 5 fichiers conformes ; `seed status` : rôles, versions, commits, trunk propre. **Défaut N1** : noyau sur `devenv/env-11` au lieu de `master` (§3) ; contourné par `git checkout master` dans le clone d'essai | GRA-1, GRA-2, GRA-3, GRA-6 |
| 2.2 (GRA-2, copie) | `lepton seed remove qemu-mps2-an386` ; `lepton seed remove lepton-noyau` | refus code 1 : « est le BSP / le noyau de la graine, obligatoire (GRA-2) » | GRA-2 |
| 2.2 (GRA-2, copie) | BSP dégreffé (`scion graft-remove`), puis `lepton check` et `cmake --preset` | `lepton check` code 1 : « BSP « qemu-mps2-an386 » non greffé (GRA-2) » ; CMake code 1 mais message indirect (`boards/qemu-mps2-an386` introuvable, `LEPTON_BOARD_CPU_FREQ non défini`) : **O1** | GRA-2 |
| 2.3 | `lepton generate` ; `cmake --list-presets` | `env11-debug-qemu` + 15 presets du noyau ; `CMakeUserPresets.json` greffé (lien) ; `.DS_Store` du Finder supprimés (Q8) | CFG-6, GRF-3 |
| 2.3 | `cmake --preset host`, `cmake --preset env11-debug-qemu`, `cmake --build` | code 0 ; `lepton.{elf,bin,hex,map,occupation.txt}` ; cibles `kernel`, `lib`, `sbin`, `bin`, `generated`, `kernel_demarrage`, `bsp_demarrage` (pas de `bsp` ni `bsp_objets` pour an386 : un seul fichier de démarrage, comme la référence `~/lepton/build/qemu-mps2-an386-freertos`) ; aucune sortie dans le trunk | BLD-1, BLD-3, BLD-4 |
| 2.3 | `ctest --preset env11-debug-qemu -L smoke` puis `-L kal` | fumée : réussie ; banc KAL : **18/18** (`arch:cortex-m4f`, `backend:freertos`) | TST-1 (CLI) |
| 2.4 | `lepton scion new --type application salut` | 1ᵉʳ essai : **défaut N2** (refus de scion à cause des `.DS_Store`, annulation incomplète) ; corrigé (338ff5b), relancé : code 0, reconfiguration CMake | GRF-1 |
| 2.4 | `cmake --build` du modèle d'application | **défaut N3** : `kernel/libstd.h` introuvable ; modèle corrigé (7d191aa), greffon recréé : `salut.c.obj` compilé sans retouche | GRF-1 |
| 2.4 | `lepton file add <trunk>/sys/root/src/bin/salut/salut_message.c` ; contenu écrit dans le clone | lien créé dans le trunk, fichier non suivi dans le clone (pas de `git add`, PA-9) ; `cmake --build` : « Re-running CMake », `salut_message.c.obj` compilé, aucune liste CMake éditée | FIC-1, FIC-3, FIC-4, BLD-2 |
| 2.4 | `<bin name="salut">` ajouté au XML **du clone noyau d'essai** (PA-9 Q5) ; `lepton check` ; construction ; `smoke_lsh.py --command "ls /usr/bin" --command salut` | `salut_main`, `salut_message` liés ; `/usr/bin` : `net salut` ; sortie `salut depuis salut_message.c` : **O5** | CFG-1, CFG-5 |
| 2.8 | `lepton scion remove salut` | liens retirés, aucun lien orphelin ni fichier régulier, clone `salut` intact (HEAD 4e1df4c, propre) ; puis reconfiguration CMake en échec (code 2) tant que le XML déclare `salut` ; `lepton check` code 1 (CFG-5) : **O4**. Déclaration retirée du XML : construction et fumée réussies | GRF-4, CFG-5 |
| 2.9 (CLI) | `SOURCE_DATE_EPOCH=1760536800` ; `cmake --preset env11-debug-qemu -B build/bld5-a` puis `-B build/bld5-b`, et `--fresh` + `--clean-first` dans `build/env11-debug-qemu` | `lepton.bin` sha256 `25d50f61…` et `lepton.hex` `7e29c21c…` identiques sur les trois constructions ; partie éditeur en S2 | BLD-5 (CLI) |
| 5-6 (préparation) | `lepton seed new env11f4 … --bsp nucleo-f429zi --backend embos --mkconf …nucleo_f439zi.xml` ; `env11wl … --bsp nucleo-wl55jc1 --backend freertos --mkconf …nucleo_wl55jc1.xml` ; `lepton generate` ; construction | `env11f4-debug-board` et `env11wl-debug-board` construits (`openocd-nucleo-wl55jc1.cfg` généré) ; F429 embOS : échec tant que `LEPTON_EMBOS_ROOT` n'est pas exporté (**O6**), puis réussi ; espaces de travail : lancement OpenOCD et tâche « flasher » présents | GRA-1, GRF-3, CFG-6 |

Non-régression de `lepton` après N2 et N3 : `pytest -q` **117 passed** (116 + 1 nouveau) ;
`scripts/bout-en-bout.sh essais/env-11/bout-en-bout` : succès.

## 2bis. Session S2 — cartes réelles et VSCodium

Sondes : NUCLEO-F429ZI ST-LINK/V2-1 n° 0672FF495252717267243842, console `/dev/cu.usbmodem145103` ;
NUCLEO-WL55JC1 STLINK-V3 n° 002700253431510837393937 (carte A), console `/dev/cu.usbmodem1454303`
(115200 8N1). Journaux bruts : `essais/env-11/logs/s2-*.log`. Fichiers OpenOCD et gdbinit pris par
leur chemin réel dans le clone du BSP d'essai (`depots/lepton/bsp-<carte>/master/scion/…/debug/`).

### Ligne de commande (Claude)

| Étape | Commande (résumé) | Résultat | Exigences |
| --- | --- | --- | --- |
| 2.5 / 2.6 | `openocd -f <cfg BSP> -c "adapter serial <n°>" -c "init; targets; shutdown"` | F4 : `STLINK V2J27M15`, `[stm32f4x.cpu] Cortex-M4 r0p1` ; WL : `STLINK V3J7M3`, `[stm32wlx.cpu0] Cortex-M4 r0p1` (cœur M4) | DBG-3 |
| 2.5 / 2.6 | même chose **sans** `adapter serial`, deux cartes branchées | les deux cfg prennent la sonde V3 ; cfg F4 : `Error: expected 1 of 1: 0x2ba01477`, code 1, aucune écriture : **O8** | DBG-3 |
| 2.5 | `openocd … -c "program build/env11f4-debug-board/lepton.elf verify reset exit"` (embOS ; `lepton.bin` sha256 `eaa417cf…`) | `device id = 0x20016419`, 2048 KiB, « Verified OK », code 0 | DBG-3 |
| 2.5 | `tests/smoke_lsh.py --transport serial --port /dev/cu.usbmodem145103 --reset-command "openocd … reset run" --expect-machine cortexM4-stm32f4` | invite `lepton#2$`, `uname -a` = `… cortexM4-stm32f4`, code 0 | DBG-3 |
| 2.5 | `openocd` + `arm-none-eabi-gdb -x gdbinit-nucleo-f439zi lepton.elf` (`monitor reset halt`, `break main`, `continue`), cwd = trunk | `Breakpoint 1, main () at …/trunk/…/core-segger/arch/armv7m/embos_main.c:13` ; `gdbinit-lepton:147` : Python non pris en charge par ce GDB : **O9** | DBG-3, IDE-4 |
| 2.6 | `openocd … program build/env11wl-debug-board/lepton.elf verify reset exit` (FreeRTOS ; `lepton.bin` `0cb80f9e…`) | idcode `0x10036497`, `RDP level 0 (0xAA)`, 256 KiB, « Verified OK », code 0 ; octets d'option et M0+ non touchés | DBG-3 |
| 2.6 | `smoke_lsh.py --transport serial --port /dev/cu.usbmodem1454303 … --expect-machine cortexM4-stm32wl` | invite `lepton#2$`, `uname -a` = `… cortexM4-stm32wlxx`, code 0 | DBG-3 |
| 2.6 | `openocd` + `arm-none-eabi-gdb -x gdbinit-nucleo-wl55jc1` | `Breakpoint 1, main ()` (pc 0x8000378 ; ligne affichée `portmacro.h:216`, code inséré dans `main`) ; même message O9 | DBG-3 |

### VSCodium (constats de l'utilisateur ; vérifications sur disque par Claude)

VSCodium 1.135.06055 lancé depuis un terminal par `export LEPTON_EMBOS_ROOT=… SOURCE_DATE_EPOCH=1760536800; codium <espace>` (variables relevées dans l'environnement du processus), sauf A.
Essais carte : une seule carte branchée à la fois (O8).

| Essai | Manipulation | Résultat | Exigences |
| --- | --- | --- | --- |
| A (O6) | `env11f4.code-workspace` ouvert depuis le Finder ; preset `env11f4-debug-board` ; « CMake: Delete Cache and Reconfigure » | Configuration réussie : `LEPTON_EMBOS_ROOT` hérité de `~/.zshrc:15` (ligne manuelle ; VSCodium lit l'environnement du shell de connexion) ; cas sans variable démontré par lecture de `cmake/kal/embos.cmake:13-15` (erreur fatale), décision de l'utilisateur | — (O6) |
| B1 | F429ZI : tâche « lepton : flasher env11f4-debug-board » ; lancement « Déboguer env11f4-debug-board (carte, OpenOCD) » ; point d'arrêt posé via le trunk | flash réussi ; arrêt sur `main` ; point d'arrêt atteint | DBG-3, IDE-4 |
| B2 | WL55JC1 : idem avec `env11wl.code-workspace` | flash réussi ; arrêt sur `main` ; point d'arrêt atteint | DBG-3, IDE-4 |
| B3 | QEMU `env11.code-workspace` : tâche « lepton : QEMU env11-debug-qemu (console série) » | invite `lsh` dans le terminal intégré | DBG-1 |
| B3 | lancement « Déboguer env11-debug-qemu (QEMU mps2-an386) » | arrêt sur `main` | DBG-2 |
| B3 | tâche « lepton : banc KAL env11-debug-qemu » | `100% tests passed, 0 tests failed out of 18`, résumé par étiquette (`arch:cortex-m4f`, `backend:freertos`) | TST-1 |
| B3 | barre latérale | arborescence visible | IDE-1 |
| B3 | Source Control | 4 dépôts (graine `env11`, `lepton-noyau`, `qemu-mps2`, `qemu-mps2-an386`) ; `trunk` n'est pas un dépôt | IDE-2 |
| B3 | F12 sur `bin_lst` dans `trunk/…/kernel/core/bin.c` | 1ᵉʳ essai sans effet : clangd démarré à 18:23:17 alors que `build/.active/compile_commands.json` n'existait pas (écrit par CMake Tools à 18:33), aucun index de fond : **O10**. Après « clangd: Restart language server » : définition ouverte (`generated/board/bin_mkconf.c:98`) ; index `build/.active/.cache/clangd/index` 400 fichiers, rien dans le trunk | IDE-3 |
| B3 | point d'arrêt posé via le trunk, QEMU | atteint | IDE-4 |
| B3 | changement de preset `env11-debug-qemu` → `qemu-mps2-an386-freertos` → retour | sélecteur absent de la barre d'état (CMake Tools 1.24.42 : `cmake.options.statusBarVisibility` = `hidden` par défaut) : **O11** ; changement fait par le panneau CMake › Project Status ; reconfiguration (`build/qemu-mps2-an386-freertos` créé 18:47, retour 18:48) ; `build/.active/compile_commands.json` identique (`cmp`) à celui du preset actif | IDE-5 |
| B3 | faute de schéma (`<inconnu/>` sous `<mklepton>`, `"type": "xyz"`) puis de syntaxe, dans `mkconf_tauon_basic_qemu_mps2.xml` et `lepton-greffon.json` (non enregistrés) | faute de schéma **non signalée**, faute de syntaxe signalée ; aucune association de schéma (ni `xsi:noNamespaceSchemaLocation`, ni `"$schema"`, ni `xml.fileAssociations` / `json.schemas` dans l'espace) : **N4** ; lemminx natif actif (canal « XML Support ») ; clones d'essai propres après l'essai | CFG-7 (P2) |
| 2.9 éditeur | `env11-debug-qemu` : « CMake: Delete Cache and Reconfigure » (18:57) puis « CMake: Clean Rebuild » (18:58) | `lepton.bin` `25d50f614d44b35e…`, `lepton.hex` `7e29c21c50afdcc5…` : **identiques** aux trois constructions CLI de S1 | BLD-5 |

### Fin de scénario
- Trois trunks d'essai : aucun lien orphelin ; seul fichier régulier `.scion.grafted.list` (liste de
  scion), hors `.DS_Store` (Q8).
- `~/lepton` : branche, HEAD et état des 9 dépôts identiques à `essais/env-11/ref-avant.txt`.

## 3. Défauts

| ID | Composant (étape responsable) | Constat | Suite |
| --- | --- | --- | --- |
| N1 | scion `gitops.clone` (ENV-7 ; présent depuis 0.5.0.1) | Version `master` → `git clone` sans `checkout` : le clone reste sur la branche par défaut de l'origine (ici `devenv/env-11`, extraite dans `~/lepton`). Même effet avec une origine dont la branche par défaut est `main`. `seed lock` figerait un commit qui n'est pas celui de la version déclarée | Consigné, renvoyé à ENV-7 (correctif et version de scion à décider) ; contournement : `git -C <clone> checkout master` après `seed new` |
| N2 | lepton (ENV-8, PA-9 Q8) | Purge des `.DS_Store` faite par `lepton graft` et `generate` seulement ; `seed add/remove/replace`, `seed lock --restore`, `scion new/remove`, `file add` appelaient `scion graft` / `graft-remove` sans purge et échouaient dès que le Finder avait parcouru le trunk | **Corrigé** dans ENV-11 (décision de l'utilisateur) : `Rootstock.purge_system_files()` et `seed.scion_on_trunk()`, test `test_gra4_add_remove_with_finder_files` (échoue sans la correction) ; commit 338ff5b |
| N3 | lepton, modèle d'application (ENV-8) | `#include "kernel/libstd.h"` et `"stdio/stdio.h"` introuvables : l'application créée ne compile pas (tests d'ENV-8 à construction simulée) | **Corrigé** dans ENV-11 (décision de l'utilisateur) : `kernel/core/libstd.h`, `lib/libc/stdio/stdio.h` (forme de `sbin/uname.c`), assertion dans `test_grf1_scion_new_application` ; commit 7d191aa ; compilation réelle prouvée |
| N4 | CFG-7 (P2) ; aucune étape responsable (ENV-3 schémas, ENV-9 fichiers de l'éditeur) | Fautes de schéma non signalées à la saisie dans le XML mklepton et les manifestes JSON : aucun fichier ni réglage n'associe `schemas/mklepton.xsd`, `greffon.schema.json`, `graine.schema.json` ; seule la syntaxe est vérifiée (lemminx natif, JSON intégré) | Non conforme (P2) ; renvoi à décider au bilan (proposé : ENV-9, `xml.fileAssociations` et `json.schemas` générés par `lepton generate`) |

## 4. Observations (à classer au bilan)

| ID | Constat | Renvoi proposé (non validé) |
| --- | --- | --- |
| O1 | BSP de la graine non greffé : CMake refuse, mais par un message indirect (fichier `boards/<bsp>` absent, fréquence non définie) ; `lepton check` est explicite | ENV-6 (lecteur `cmake/lepton_greffons.cmake` : message « aucun manifeste BSP `<nom>` greffé ») |
| O2 | `lepton seed new` crée une seule configuration (`debug-qemu` ou `debug-board`, PA-9) ; aucune commande pour en ajouter (édition de `lepton-graine.json`) | ENV-8 / ENV-12 (commande ou palette) |
| O3 | Après annulation incomplète, le message de reprise de `scion new` annonce « hors graine » alors que le greffon reste dans `.scion.sources.list` et la liste greffée (cas devenu rare avec N2) | ENV-8 |
| O4 | `lepton scion remove` d'une application déclarée dans le XML : retrait fait, puis reconfiguration CMake en échec (« Cannot find source file …/salut.c ») sans avertissement préalable ; `lepton check` le signale | ENV-8 (avertissement CFG-5 dans `scion remove`) |
| O5 | Exécuter une application impose d'éditer le XML mklepton porté par le **greffon noyau** (PA-9 Q5) : une modification propre au projet entre dans un greffon partagé ; CFG-1 demande un XML versionné dans la graine | Décision de conception (ENV-8 / ENV-12) |
| O6 | Rootstock neuf : `LEPTON_EMBOS_ROOT` doit être exporté à la main (embOS hors git, `lepton-env.sh` le cherche sous `<rootstock>/third_party`) ; l'espace de travail généré ne le transmet pas. S2 : sur cet hôte, VSCodium lancé par le Finder l'hérite de `~/.zshrc:15` (ligne manuelle) ; sans cette ligne, échec démontré par lecture de `cmake/kal/embos.cmake:13-15` (décision de l'utilisateur) | ENV-10 (script ou documentation : export persistant) ou ENV-9 (espace généré) |
| O7 | Le Finder recrée des `.DS_Store` dans les trunks d'essai pendant la session | Traité par N2 (PA-9 Q8) |
| O8 | Tâche « flasher » et lancement Cortex-Debug générés sans numéro de série de sonde (`configFiles` = champ `openocd` du BSP, décision ENV-9) : deux cartes ST-Link branchées → OpenOCD prend la première sonde (ici la V3 pour la cfg F4 ; échec sur l'IDCODE, sans écriture). Essais éditeur faits une carte à la fois | ENV-9 (série de sonde dans l'espace : `serialNumber` Cortex-Debug, `adapter serial`) ou BSP F4 (enveloppe générée comme le WL) |
| O9 | `debug/gdbinit-lepton:147` (dernier bloc, commande Python de piles) : « Scripting in the "Python" language is not supported in this copy of GDB » avec `arm-none-eabi-gdb` 14.2.Rel1 darwin-x86_64 ; le reste du fichier est chargé | Noyau (`gdbinit-lepton` : bloc Python conditionnel) ou chaîne (GDB avec Python) |
| O10 | clangd lancé à l'ouverture de l'espace avant que CMake Tools ait configuré : `build/.active/compile_commands.json` absent (écrit seulement par `cmake.copyCompileCommands`, jamais par la ligne de commande ni par les tâches) → pas de base ni d'index, navigation inopérante jusqu'à « clangd: Restart language server » | ENV-9 (`lepton generate` ou tâche de configuration alimentant `build/.active`) ; ENV-12 (relance automatique) |
| O11 | IDE-5 « depuis la barre d'état » : CMake Tools 1.24.42 masque le sélecteur de preset par défaut (`cmake.options.statusBarVisibility` = `hidden`) ; changement possible par le panneau CMake › Project Status ou la palette. La mention « barre d'état » de `env-9-validation.md` lignes 23 et 29 désignait vraisemblablement ce panneau | ENV-9 (`"cmake.options.statusBarVisibility": "visible"` dans l'espace généré) |

## 5. Reste (S2, S3)

- S2 : faite (§2bis). DBG-1 à DBG-3, IDE-1 à IDE-5, TST-1, BLD-5 conformes sur Mac (réserves O8,
  O10, O11) ; CFG-7 (P2) non conforme (N4).
- S3 : scénario Debian (étapes 1-4 et 9, VM ; push soumis à PA-P), bilan des exigences P1,
  classement de N1, N4 et O1-O11.
