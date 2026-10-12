# ENV-1 — Essais de levée des risques éditeur

Session du 2026-10-12. Essais jetables sous `~/lepton/build/essais-env1/` ; aucun dépôt modifié.

## Versions

| Élément | Version |
| --- | --- |
| VSCodium | 1.135.06055 (commit 1a46a584), x64 |
| Extension clangd (`llvm-vs-code-extensions.vscode-clangd`) | 0.6.0 (Open VSX) |
| Extension CMake Tools (`ms-vscode.cmake-tools`) | 1.24.42 (Open VSX) |
| Extension Cortex-Debug (`marus25.cortex-debug`) | **1.13.0-pre6** (pré-version servie par Open VSX) + dépendances `mcu-debug.*` (rtos-views 0.0.16, peripheral-viewer 1.6.4, memory-view 0.0.29, debug-tracker 0.0.15) |
| clangd (essai préliminaire) | Apple clangd 17.0.0 (`/usr/bin/clangd`) |
| clangd (essai retenu) | 21.1.8 — `/opt/local/bin/clangd-mp-21`, MacPorts `clang-21 @21.1.8_3+analyzer` |
| arm-none-eabi-gcc / gdb | 14.2.Rel1 |
| QEMU | 11.1.2 |

## Montage d'essai

| Élément | Emplacement |
| --- | --- |
| Construction sans préfixe | `essais-env1/sans-prefixe/` — preset `qemu-mps2-an386-embos`, `cmake -S trunk -B … --preset …` |
| Construction avec préfixe | `essais-env1/avec-prefixe/` — idem avec `CFLAGS=-ffile-prefix-map=/Users/cle_d_anton/lepton/trunk=/lepton/trunk` (163 entrées sur 166 de `compile_commands.json` portent l'option ; les 3 sans sont les fichiers générés de `build/`) |
| Copie jetable du rootstock | `essais-env1/rootstock/{depots,trunk}` par `rsync -a` ; liens relatifs résolus dans la copie (vérifié par `test -L` et `realpath`) |
| Espaces de travail | `essais-env1/espaces/1-trunk-seul`, `2-multi-racines` (trunk + clone lepton + clone seed.scions + build), `3-sauvegarde-copie` (`.code-workspace`) ; CMake Tools neutralisé (pas de configuration à l'ouverture), clangd pointé sur `sans-prefixe/compile_commands.json` |
| Scripts d'essai | scratchpad de session (non versionnés) : `essai-gdb.sh` (QEMU `-S -gdb` + `arm-none-eabi-gdb --batch`), `essai_clangd.py` (client LSP minimal) |

Structure du trunk constatée : liens **par fichier**, relatifs (`trunk/…/embos_main.c ->
../../…/depots/lepton/original/master/scion/…/embos_main.c`) ; les répertoires du trunk sont réels.
`compile_commands.json` référence les sources par le **chemin trunk** (163/166) et les 3 sources
générées par mklepton par le chemin `build/…/generated/board/`.

## Essai 3 — Chemins de débogage (GDB en ligne de commande)

Point d'arrêt : `embos_main.c:16` (appel `_start_kernel`, adresse 0x292), image `lepton.elf`.

| Cas | Construction | Réglage GDB | Spécification du point d'arrêt | Résolu | Atteint | Chemin `file` (DWARF) | Chemin `fullname` / « Located in » |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | sans préfixe | — | chemin trunk | oui | oui | trunk | **clone** |
| S2 | sans préfixe | — | chemin clone | oui | oui | trunk | clone |
| S3 | sans préfixe | — | `embos_main.c:16` | oui | oui | trunk | clone |
| S4 | sans préfixe | `substitute-path trunk→clone` | chemin clone | oui | oui | trunk | clone |
| A1 | avec préfixe | — | chemin trunk | **non** (« No source file named ») | non | — | — |
| A2 | avec préfixe | — | chemin clone | **non** | non | — | — |
| A3 | avec préfixe | — | `/lepton/trunk/…` | oui | oui | `/lepton/trunk/…` | **introuvable** (« No such file or directory ») |
| A4 | avec préfixe | `substitute-path /lepton/trunk ~/lepton/trunk` | chemin trunk | oui | oui | `/lepton/trunk/…` | clone |
| A5 | avec préfixe | idem | chemin clone | oui | oui | `/lepton/trunk/…` | clone |

Contrôle GDB/MI (`--interpreter=mi2`, cas S1) : `-break-insert` et `*stopped` renvoient
`file="<trunk>/…"` et **`fullname="<clone>/…"`**. GDB résout les liens symboliques pour
`fullname` ; c'est ce champ que les extensions de débogage utilisent pour ouvrir le source à l'arrêt.

Conclusions CLI :
- Sans `-ffile-prefix-map`, aucun réglage n'est nécessaire côté GDB : un point d'arrêt posé par le
  chemin trunk comme par le chemin clone est résolu et atteint.
- Avec `-ffile-prefix-map`, un `set substitute-path <préfixe> <ROOTSTOCK>/trunk` est
  **indispensable** ; il suffit alors pour les deux chemins.
- Dans tous les cas, l'arrêt est signalé avec le **chemin du clone** (`fullname`). Si l'éditeur
  ouvre ce chemin, un fichier ouvert via le trunk sera rouvert sous un second chemin (IDE-4) : à
  vérifier dans VSCodium (essai 3 GUI).

## Essai 1 — clangd et liens symboliques

### Essai préliminaire LSP (clangd Apple 17, sans VSCodium)
Client LSP minimal, `--compile-commands-dir=sans-prefixe`, index d'arrière-plan, 90 s d'attente.

| Fichier ouvert par | Symbole | definition | declaration |
| --- | --- | --- | --- |
| trunk `embos_main.c` | `_start_kernel` | trunk `embos_main.c:10` (déclaration `extern` locale ; définition `core-segger/kernel.c:1158` non trouvée) | idem |
| clone `embos_main.c` | `_start_kernel` | clone `embos_main.c:10` (idem) | idem |
| généré `build/…/dev_mkconf.c` | `dev_null_map` | **trunk** `kernel/dev/dev_null/dev_null.c:58` | `dev_mkconf.c:41` |

Observations : la navigation depuis un fichier généré aboutit au **chemin trunk** (chemin de
`compile_commands.json`), pas au clone. La définition de `_start_kernel` n'est pas trouvée en
90 s (index incomplet, voir ci-dessous).

### Essai LSP avec clangd LLVM 21.1.8 (`/opt/local/bin/clangd-mp-21`, MacPorts `clang-21 @21.1.8_3`)
Même client, même base de compilation. Le message `libomp` affiché en fin d'installation concerne
OpenMP et n'a pas d'effet sur clangd.

| Lancement | Fichier ouvert par | Symbole | definition | declaration |
| --- | --- | --- | --- | --- |
| 1 (index vide, 180 s) | trunk / clone / généré | `_start_kernel`, `dev_null_map` | déclaration locale seulement (index pas encore prêt) | idem |
| 2 (index en cache) | trunk `embos_main.c` | `_start_kernel` | **trunk** `core-segger/kernel.c:1158` | trunk `embos_main.c:10` |
| 2 | généré `dev_mkconf.c` | `dev_null_map` | **trunk** `dev_null/dev_null.c:58` | `dev_mkconf.c:41` |
| 2 | `workspace/symbol` | `_start_kernel`, `dev_null_map` | **trunk** (mêmes emplacements) | — |
| 3 (index en cache) | clone `embos_main.c` (1re requête) | `_start_kernel` | déclaration locale (index en cours de chargement) | clone `embos_main.c:10` |
| 3 | trunk `embos_main.c` | `_start_kernel` | **trunk** `kernel.c:1158` | trunk `embos_main.c:10` |
| 3 | clone `embos_main.c` | `_start_kernel` | **trunk** `kernel.c:1158` | clone `embos_main.c:10` |
| 3 | clone `kernel.c` | `_start_kernel` (sur la définition) | **trunk** `kernel.h:211` | trunk `kernel.h:211` |
| — | clone `embos_main.c` | `OS_Init` | `third_party/embos/…/RTOS.h:508` (hors arbre) | idem |

Conclusions clangd :
- Les chemins renvoyés par clangd sont ceux de `compile_commands.json` et des `-I` : **chemins du
  trunk**, quel que soit le chemin du fichier de départ. Un fichier ouvert via le clone obtient une
  commande interpolée et fonctionne, mais la navigation le fait sortir vers le trunk : deux chemins
  pour un même fichier (IDE-4) dès qu'on ouvre un fichier par le clone.
- Les fichiers générés par mklepton (`build/…/generated/`) sont indexés et naviguent vers le trunk.
- L'index initial de ce preset prend **plus de 180 s** sur le Mac ; tant qu'il n'est pas prêt, F12
  renvoie la déclaration `extern` locale. Index en cache : 2,3 Mo dans
  `<build>/.cache/clangd` (hors trunk, grâce à `--compile-commands-dir`).
- Les canoniques divergent : clangd → **trunk**, GDB `fullname` → **clone**.

### Essai dans VSCodium (relevés de l'utilisateur)

| Essai | Action | Résultat observé |
| --- | --- | --- |
| G1.3 | `1-trunk-seul`, `embos_main.c` ouvert via le trunk, F12 sur `_start_kernel` | Fichier ouvert dans le **trunk** (conforme à l'essai LSP) |
| G1.4 | Même fichier ouvert par le chemin clone | **Deux onglets** `embos_main.c` (trunk et clone) ; **diagnostics dans les deux** (« Included header stdint.h is not used directly », clangd unused-includes) → double jeu de diagnostics, IDE-4 non respectée si l'on ouvre par le clone |
| G1.4b | F12 sur `_start_kernel` depuis l'onglet du clone | Ouvre `kernel.c` dans le **trunk** (conforme à l'essai LSP) |
| G1.5 | `dev_mkconf.c` (généré) ouvert | Diagnostic « Included header kernelconf.h is not used directly » : fichier généré pris en charge par clangd |
| G1.5b | F12 sur `dev_null_map` (ligne 54) | Ouvre `dev_null.c` dans le **trunk** (conforme à l'essai LSP) : navigation correcte depuis un source généré par mklepton |
| G2 | `2-multi-racines` : mêmes actions via la racine « trunk » puis la racine « clone lepton » | Même comportement que G1 (relevé de l'utilisateur) : deux onglets et deux jeux de diagnostics si le fichier est ouvert par les deux racines ; F12 mène au **trunk** depuis l'une comme depuis l'autre. L'espace multi-racines ne change pas le chemin canonique de clangd. |

## Essai 2 — Sauvegarde à travers un lien (FIC-5)

Procédure : espace `3-sauvegarde-copie`, racine « trunk (copie) », ouverture de
`sys/root/src/kernel/core/core-segger/arch/armv7m/embos_main.c`, ajout d'une ligne
`/* essai FIC-5 */` après la ligne 6, Cmd+S (utilisateur). Réglage `files.saveConflictResolution`
à sa valeur par défaut (`askUser`).

Contrôles (Claude) :
- `test -L trunk/…/embos_main.c` : **lien préservé**, cible et date du lien inchangées
  (`../../…/depots/lepton/original/master/scion/…/embos_main.c`, 8 oct 12:53).
- `git -C depots/lepton/original/master status` (copie) : ` M scion/…/embos_main.c` ; `git diff`
  montre exactement la ligne ajoutée → la sauvegarde a écrit **dans la cible du lien**.
- Aucun fichier régulier apparu dans le trunk de la copie ; trunk réel et clone réel intacts.

Résultat : **FIC-5 satisfaite** avec le réglage par défaut de VSCodium 1.135 ; aucun réglage
particulier nécessaire. L'essai de `files.saveConflictResolution` n'a pas lieu d'être (comportement
conforme).

## Essai 3 (suite) — Débogage dans VSCodium (Cortex-Debug 1.13.0-pre6, relevés de l'utilisateur)

Espace `2-multi-racines`, point d'arrêt ligne 16 de `embos_main.c`, configurations « QEMU sans
préfixe », « QEMU avec préfixe + substitute-path », « QEMU avec préfixe seul ».

| Point d'arrêt posé dans | Profil | Arrêt ligne 16 | Onglet présenté à l'arrêt |
| --- | --- | --- | --- |
| onglet trunk | sans préfixe ; avec préfixe + substitute-path | oui | **onglet du clone** (`depots/…/scion/…/embos_main.c`), ouvert en plus de l'onglet trunk |
| onglet clone | sans préfixe ; avec préfixe + substitute-path | oui | onglet du clone |
| trunk ou clone | avec préfixe seul | **non** | Échec à l'arrêt d'entrée : « The editor could not be opened because the file was not found » (chemin `/lepton/trunk/…` inexistant) — premier relevé erroné, corrigé par l'utilisateur |

Cohérent avec GDB/MI (`fullname` = chemin du clone) : à l'arrêt, Cortex-Debug ouvre toujours le
fichier sous le chemin du clone. Un point d'arrêt posé via le trunk est bien atteint (critère
IDE-4 « Point d'arrêt posé via le trunk atteint » rempli), mais l'arrêt s'affiche sous un second
chemin (IDE-4 « un seul chemin » non rempli en ouvrant par le trunk).

Contre-essai (Claude) : Cortex-Debug pose ses points d'arrêt par `break-insert "<chemin complet>:<ligne>"`
(`dist/debugadapter.js`). Reproduit en GDB/MI sur l'image « avec préfixe » sans `substitute-path` :
`^error,msg="No source file named <trunk>/…/embos_main.c."`, idem pour le chemin clone. Confirmé
par le second relevé de l'utilisateur : avec `-ffile-prefix-map` sans `substitute-path`, le
débogage depuis l'éditeur est inutilisable.

## Essai 4 — Git multi-dépôts

Espace `2-multi-racines` (racines : trunk, clone lepton, clone seed.scions, build). Relevé de
l'utilisateur : le panneau Source Control affiche **deux dépôts**, clone lepton et clone
seed.scions ; **aucun pour le trunk** ni pour le répertoire de construction. Conforme.

## Procédure GUI (à exécuter par l'utilisateur)

Prérequis : clangd LLVM installé (`sudo port install clang-21` → `/opt/local/bin/clangd-mp-21`).
Ouvrir chaque espace par `codium <fichier>.code-workspace` (dossier
`~/lepton/build/essais-env1/espaces/`). Ne pas accepter de proposition de CMake Tools de
configurer le projet. Relever pour chaque point : **chemin affiché dans l'onglet / la barre de
titre** (survol de l'onglet), nombre d'onglets, présence de diagnostics.

**G1 — Aller à la définition, trunk seul** (`1-trunk-seul`)
1. Attendre la fin de l'indexation clangd (barre d'état).
2. Ouvrir `sys/root/src/kernel/core/core-segger/arch/armv7m/embos_main.c` (explorateur).
3. Ligne 16 : F12 sur `_start_kernel`. Relever le fichier ouvert et son chemin complet (trunk ou
   `depots/…`).
4. Ouvrir le même `embos_main.c` par le chemin clone (Ctrl/Cmd+P ne suffit pas : Fichier › Ouvrir…
   `~/lepton/depots/lepton/original/master/scion/sys/root/src/kernel/core/core-segger/arch/armv7m/embos_main.c`).
   Relever : un ou deux onglets ? diagnostics dans les deux ?
5. Ouvrir `~/lepton/build/essais-env1/sans-prefixe/generated/board/dev_mkconf.c`, F12 sur
   `dev_null_map` (ligne 54). Relever le chemin ouvert.

**G2 — Aller à la définition, multi-racines** (`2-multi-racines`) : refaire G1 3 à 5, en ouvrant
`embos_main.c` d'abord dans la racine « trunk », puis dans la racine « clone lepton ». Relever le
chemin ouvert par F12 dans chaque cas et si deux onglets coexistent.

**G3 — Sauvegarde via le lien** (`3-sauvegarde-copie`)
1. Dans la racine « trunk (copie) », ouvrir `sys/root/src/kernel/core/core-segger/arch/armv7m/embos_main.c`.
2. Ajouter une ligne `/* essai FIC-5 */` après la ligne 6, Cmd+S.
3. Me le signaler : je contrôle `test -L` sur le trunk de la copie et `git diff` du clone copie.

**G4 — Débogage Cortex-Debug** (`2-multi-racines`, vue Exécuter et déboguer)
1. Configuration « QEMU sans préfixe ». Poser un point d'arrêt ligne 16 de `embos_main.c` ouvert
   **via le trunk** ; F5. Relever : arrêt sur `main` (entrée) puis, après F5, arrêt ligne 16 ?
   Quel fichier/onglet est mis en surbrillance (trunk ou clone, nouvel onglet ?).
2. Arrêter. Retirer le point d'arrêt, le reposer ligne 16 dans `embos_main.c` ouvert **via le
   clone** ; F5. Mêmes relevés.
3. Refaire 1 avec « QEMU avec préfixe + substitute-path », puis « QEMU avec préfixe seul ».

**G5 — Source Control** (`2-multi-racines`) : relever les dépôts listés dans le panneau Source
Control (attendu : clone lepton, clone seed.scions ; aucun pour le trunk).

## Synthèse

| Risque | Résultat |
| --- | --- |
| Navigation clangd (IDE-3) | Conforme : définitions trouvées, y compris depuis les sources générées ; chemins rendus = **trunk** (ceux de `compile_commands.json` et des `-I`), quel que soit le chemin du fichier de départ. Index initial > 180 s. |
| Un seul chemin par fichier (IDE-4) | **Non garanti** : un fichier ouvert par le trunk et par le clone donne deux onglets et deux jeux de diagnostics ; à l'arrêt du débogueur, Cortex-Debug ouvre toujours le **chemin du clone** (`fullname` GDB = chemin réel). Le point d'arrêt posé via le trunk est atteint. |
| Sauvegarde via un lien (FIC-5) | Conforme avec les réglages par défaut. |
| Chemins de débogage | Sans `-ffile-prefix-map` : aucun réglage nécessaire. Avec : `set substitute-path` obligatoire, sinon débogage inutilisable. Cortex-Debug n'offre aucune table de correspondance de chemins (`sourceFileMap` absent). |
| Git multi-dépôts | Conforme en multi-racines : un dépôt par clone, aucun pour le trunk. |

## Recommandations (PA-1)

1. **Mode d'ouverture des fichiers : par le trunk.** Le trunk est le chemin canonique de clangd et
   de la construction ; la sauvegarde écrit dans le clone (FIC-5). Les clones ne servent que pour
   git ; leur présence comme racines de l'espace permet d'ouvrir un fichier sous un second chemin :
   ENV-9 devra soit les masquer de l'explorateur, soit obtenir le panneau Source Control sans les
   ajouter comme racines (pistes non essayées : `files.exclude` sur les racines des clones,
   `git.scanRepositories`).
2. **Réglage clangd** : clangd LLVM (MacPorts `clang-21` sur macOS ; paquet Debian en ENV-10),
   `--compile-commands-dir=<ROOTSTOCK>/build/<preset>` (cache d'index hors trunk, aucun fichier
   `.clangd` ni lien `compile_commands.json` dans le trunk), `--background-index`,
   `--query-driver=<chemin>/arm-none-eabi-gcc`.
3. **Chemins de débogage : pas de `-ffile-prefix-map`** ; aucun `substitute-path`. Les points
   d'arrêt posés via le trunk sont atteints. Écart résiduel accepté pour la phase 1 : à l'arrêt, le
   source s'affiche dans un onglet du clone (le contenu est le même fichier). Résorption possible
   en phase 2 (ENV-12) par l'extension, qui peut réécrire les chemins de pile clone → trunk — non
   essayé.

## Décision PA-1 (utilisateur, 2026-10-12)
Les trois recommandations ci-dessus sont retenues telles quelles ; consignées dans
`DEVENV-STATUS.md` §Décisions.
