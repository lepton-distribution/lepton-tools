# ENV-9 — Validation dans VSCodium (session S2)

Session du 2026-10-14. Mode mixte : manipulations GUI par l'utilisateur, contrôles CLI par Claude.
Fichiers générés et règles : `env-9-generation.md`. Rootstock d'essai `~/lepton-tools-dev/essais/env-9`
(graine `env9` 9e93cdc ; configurations `debug-qemu`, `release-qemu` ; BSP `qemu-mps2-an386`,
backend freertos).

## 1. Versions

| Élément | Version |
| --- | --- |
| lepton / scion | 0.1.0 (pipx, depuis 4604b26) / 0.5.1.0 |
| VSCodium | 1.135.06055 (commit 1a46a584), x64 |
| Extensions | clangd 0.6.0 ; CMake Tools 1.24.42 ; Cortex-Debug 1.13.0-pre6 (+ mcu-debug rtos-views 0.0.16, peripheral-viewer 1.6.4, memory-view 0.0.29, debug-tracker 0.0.15) |
| clangd | 21.1.8 (`/opt/local/bin/clangd-mp-21` → `/opt/local/libexec/llvm-21/bin/clangd`) |
| QEMU / arm-none-eabi-gdb | 11.1.2 / 14.2.Rel1 |

## 2. Procédure et résultats

| # | Exigence | Manipulation | Résultat |
| --- | --- | --- | --- |
| 0 | — | `lepton generate -C …/essais/env-9` ; ouverture `codium …/env9.code-workspace` | Deux fichiers « inchangé », graine propre ; ouverture sans erreur |
| 1 | IDE-5 (CMake Tools) | Preset `env9-debug-qemu` choisi dans la barre d'état ; Configure ; Build ; vue CMake › Project Outline | Construction réussie ; 10 cibles : `bin`, `board_mkconf`, `bsp_demarrage`, `generated`, `kal_bench`, `kernel`, `kernel_demarrage`, `lepton`, `lib`, `sbin` (identiques au modèle de code `.cmake/api/v1/reply`) ; `build/.active/compile_commands.json` copié (CLI) |
| 1bis | — | Cible `bsp` attendue par la fiche d'étape | **Absente, justifié** : depuis ENV-6 la bibliothèque `bsp` n'existe que si la carte a des sources hors démarrage (`cmake/components/kernel.cmake`, `if(LEPTON_BSP_SOURCES)`) ; le BSP an386 ne déclare que `demarrage` (`qemu_mps2_board.c`) → OBJECT `bsp_demarrage`. Correspondance : liste de l'étape → `lepton`, `kernel`, `lib`, `sbin`, `bin`, `bsp_demarrage` |
| 2 | IDE-3, IDE-4 (clangd) | Ouverture de `trunk/…/kernel/core/cpu.c` | Processus `clangd` LLVM 21 avec les trois arguments générés ; index de fond dans `build/.active/.cache/clangd/index` (400 fichiers), rien dans le trunk ni dans `build/<preset>` ; 3 diagnostics « Included header … is not used directly » (include-cleaner de clangd, style ; aucune erreur d'en-tête ou de drapeau) → P10 |
| 3 | IDE-3 | F12 sur `__get_cpu` (`cpu.c:56`) | `trunk/sys/root/src/kernel/core/kernel_device.h` (chemin trunk) |
| 3 | IDE-3 (sources générées) | F12 sur `__KERNEL_HEAP_SIZE` (`heap.c:60`) | `build/env9-debug-qemu/generated/board/kernel_mkconf.h` |
| 3 | IDE-3 | ⇧F12 sur `__get_cpu` | 2 références, 2 fichiers, chemins trunk ; `grep` du trunk : exactement ces deux occurrences |
| 4 | IDE-5 | Preset `env9-release-qemu` depuis la barre d'état ; Configure ; Build | Réussi ; `build/.active/compile_commands.json` identique (`cmp`) à celui du preset release (`-Os`, `directory` release) ; même processus clangd, index 400 → 405 |
| 4 | IDE-5 | F12 sur `__KERNEL_HEAP_SIZE` | `build/env9-release-qemu/generated/…/kernel_mkconf.h` **après fermeture et réouverture de `heap.c`** ; sans réouverture, le fichier ouvert garde l'ancienne commande → réserve R1 |
| 5 | IDE-2 | Panneau Source Control ; commentaire ajouté à `trunk/…/cpu.c`, enregistré, puis *Discard Changes* | Dépôts : `graine env9`, `lepton-noyau`, `qemu-mps2`, `qemu-mps2-an386` ; modification sous `lepton-noyau` ; annulation effective ; clone propre et lien du trunk intact (CLI) |
| 5bis | IDE-4 (P5) | Essai de masquage, `files.exclude` ajouté à la main dans l'espace : `"scion/[!.]*": true`, `"project/scion": true` | Explorateur : `scion/` vide dans les clones, `scion/.scion/` (`lepton-graine.json`) visible dans la graine, `project/` vide, trunk inchangé ; ⌘P `cpu.c` : trunk seul après *Clear Editor History* ; recherche `__get_cpu` : trunk + `doc/migration/audit-iar.csv` (non greffé, légitime) ; Source Control inchangé |
| 6 | DBG-1 | Tâche `lepton : QEMU env9-debug-qemu (console série)` ; `ls /` ; *Terminate Task* | Invite `lsh` dans le terminal de la tâche ; `ls /` répond ; arrêt propre, aucun QEMU résiduel (CLI) |
| 7 | DBG-2 | Point d'arrêt posé via `trunk/…/kernel/dev/bsp/qemu-mps2-an386/qemu_mps2_board.c:48` (greffon BSP) ; lancement `Déboguer env9-debug-qemu (QEMU mps2-an386)` (F5) | Construction (`preLaunchTask`), QEMU, GDB ; arrêt dans la trame `main` (0x37c) affiché à `portmacro.h:217` : `portDISABLE_INTERRUPTS()` (ligne 16) est la `vPortRaiseBASEPRI` inlinée, première instruction après le prologue (0x37e, `objdump -l`) ; F10 → `freertos_main.c` ; vue Registers (`pc`, `sp`…) |
| 7 | DBG-2, IDE-4 | F5 | 1er lancement : arrêt inattendu à `kernel_printk.c:625` (code ordinaire, 0x4e0), raison non relevée, **non reproduit** ; 2ᵉ lancement : arrêt à `qemu_mps2_board.c:48` (résolu en CLI à 0x2dc, `qemu_mps2_uart_irq_enable`) → point d'arrêt posé via le trunk atteint ; affiché sous le chemin du clone → R3 |
| 8 | TST-1 | Tâche `lepton : banc KAL env9-debug-qemu` | `100% tests passed, 0 tests failed out of 18` ; une ligne par test ; résumé par étiquette `arch:cortex-m4f`, `backend:freertos` (case unique de la matrice de la graine) |

## 3. Réserves et constats

- **R1 (IDE-5)** : l'extension clangd ne surveille `compile_commands.json` que dans les dossiers de
  l'espace ; `build/.active` est hors de ces dossiers. Après changement de preset, les fichiers déjà
  ouverts gardent l'ancienne commande jusqu'à leur réouverture (ou *clangd: Restart language server*).
- **R2 (IDE-4)** : malgré le masquage, le diff ouvert depuis Source Control montre le fichier sous le
  chemin du clone, et l'historique *recently opened* de Quick Open le retient. Comportement de
  l'extension git de VSCodium.
- **R3 (IDE-4, écart PA-1)** : à l'arrêt, GDB renvoie le `fullname` résolu (chemin du clone) ;
  Cortex-Debug ouvre ce chemin : second onglet du même fichier, point rouge absent dans cet onglet ;
  la vue Breakpoints garde le chemin du trunk. Écart accepté en PA-1 (2026-10-12), résorption en
  ENV-12 (correspondance de chemins dans l'adaptateur).
- Le preset `debug-qemu` compile en `-g -Os` (drapeaux hérités des presets du noyau) : pas à pas et
  arrêts déroutants (code inliné). Hors ENV-9 ; à examiner (configuration debug en `-Og`).
- Le Finder recrée des `.DS_Store` réguliers dans le trunk d'essai (déjà connu, Q8).

## 4. Décisions de l'utilisateur (2026-10-14)

| # | Décision |
| --- | --- |
| P1-P4, P6-P9 | Validées telles qu'appliquées (`env-9-generation.md` §4). |
| P5 | Intégrée : `files.exclude` généré avec `scion/[!.]*` et `project/scion` en plus de `.DS_Store` et `._*` ; dossiers `git · …` conservés (Source Control, fichiers non greffés). `lepton/generate.py`, test `test_workspace_folders_settings_launch_tasks` ; sortie identique à l'essai manuel (« inchangé »). |
| P10 | Diagnostics include-cleaner de clangd laissés ; aucun `.clangd` généré. |
| R1 | Documentée (README : réouverture du fichier ou *clangd: Restart language server*) ; solution intégrée renvoyée à ENV-12. |

Contrôles après intégration de P5 : `pytest` 116 passed ; `lepton` réinstallé par pipx ;
`lepton generate` sur `essais/env-9` ×2 : « inchangé » ; `scripts/bout-en-bout.sh` : voir §6.

## 5. Bilan par exigence

| Exigence | Critère | Résultat |
| --- | --- | --- |
| IDE-2 | Panneau source control multi-dépôts | validé |
| IDE-3 | Aller à la définition ouvre le bon fichier, une seule fois | validé (sources du trunk et générées) |
| IDE-4 | Point d'arrêt posé via le trunk atteint | validé ; réserves R2, R3 (écart PA-1) |
| IDE-5 | Reconfiguration et réindexation | validé ; réserve R1 |
| DBG-1 | Invite `lsh` visible | validé |
| DBG-2 | Arrêt sur `main` | validé (pas à pas, registres) |
| TST-1 | Rapport par case de la matrice | validé (une case) |

## 6. Contrôles finals

| Contrôle | Résultat |
| --- | --- |
| `~/lepton-tools-dev/venv-lepton-tools/bin/python -m pytest -q` | 116 passed |
| `lepton generate -C ~/lepton-tools-dev/essais/env-9` ×2 (lepton réinstallé par pipx) | « inchangé » ×2 ; espace identique à l'essai manuel de l'étape 5bis |
| `LEPTON=<venv>/bin/lepton scripts/bout-en-bout.sh <scratchpad>/e2e-env9s2` | succès (cmake, fumée QEMU, trunk sain, rootstock de référence inchangé) |

Critères de l'étape : tous cochés (`handoff/env-9.md`).
