# Étape ENV-9 — Génération des fichiers de l'éditeur

## Contexte
En phase 1, l'intégration à VSCodium repose sur les extensions standard et sur des fichiers
générés par `lepton` à partir des manifestes de la graine et des BSP (CFG-1 : jamais à partir du
XML mklepton). Cette étape ajoute `lepton generate` et les réglages issus des essais d'ENV-1.

## Prérequis
- ENV-1 terminée : décisions PA-1 (mode d'ouverture des fichiers, réglages clangd, chemins de
  débogage).
- ENV-6 terminée : manifestes BSP avec OpenOCD, sonde, SVD, machine QEMU.
- ENV-8 terminée. Branche `devenv/env-9` dans `lepton-tools`.

## Tâches

### 1. `lepton generate`
Produit dans la graine (fichiers versionnés) ou dans le rootstock <À CONFIRMER en PA-9 ou au
début de l'étape : emplacement de chaque fichier généré> :

| Fichier | Contenu | Exigences |
| --- | --- | --- |
| `CMakePresets.json` | un preset par configuration de la graine (debug, release, QEMU, chaque carte), répertoire de construction hors trunk, `CMAKE_EXPORT_COMPILE_COMMANDS=ON` | CFG-6, BLD-5, IDE-5 |
| `<projet>.code-workspace` | un dossier par clone de greffon, le trunk selon PA-1, réglages CMake Tools et clangd | IDE-2, IDE-3, IDE-4 |
| `.vscode/launch.json` | QEMU (Cortex-Debug, `mps2-an386`) ; chaque carte via OpenOCD ; SVD ; correspondance des chemins décidée en PA-1 | DBG-1, DBG-2, DBG-3, DBG-4 |
| `.vscode/tasks.json` | `lepton graft`, construction, lancement QEMU avec console série, banc KAL | DBG-1, TST-1 |
| `.clangd` ou réglages | options issues d'ENV-1 | IDE-3, IDE-4 |

Règle : un fichier généré porte en tête (ou dans un champ prévu) la mention « généré par
`lepton generate`, ne pas éditer » ; `lepton generate` est idempotent.

### 2. Option `-ffile-prefix-map`
Si PA-1 l'a retenue : l'appliquer dans la construction (module CMake du noyau, branche
`devenv/env-9` du clone noyau), sinon générer `substitute-path` dans `launch.json`.

### 3. Validation dans VSCodium (hôte Mac)
- Ouvrir le `.code-workspace` ; CMake Tools montre les cibles exécutif, `kernel`, `lib`, `sbin`,
  `bin`, `bsp`.
- Changer de preset depuis la barre d'état ; clangd réindexe.
- Lancer QEMU : invite `lsh` dans le terminal intégré ; arrêt sur `main` en débogage.
- Point d'arrêt posé depuis un fichier de greffon : atteint.

## Critères de validation
- [ ] `lepton generate` deux fois de suite : aucun diff.
- [ ] `cmake --list-presets` liste toutes les configurations de la graine.
- [ ] DBG-1, DBG-2 vérifiés sous QEMU ; IDE-2 à IDE-5 vérifiés (procédure et résultat dans
      `doc/devenv/rapports/env-9-validation.md`).
- [ ] Aucune donnée lue dans le XML mklepton par `lepton generate`.

## Pièges connus
- Cortex-Debug attend des chemins d'exécutables GDB et OpenOCD : les résoudre à la génération
  (`command -v`), pas en dur (NF-3).
- Les fichiers générés dans un clone de greffon sont commités par l'utilisateur : ne générer dans
  un clone que ce qui doit y être versionné.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, emplacement des fichiers générés. Passation `handoff/env-9.md`.
