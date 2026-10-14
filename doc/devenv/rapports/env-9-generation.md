# ENV-9 — `lepton generate` : fichiers générés, règles, essais (session S1)

Session du 2026-10-14. Code : `lepton/generate.py` ; tests : `tests/test_generate.py` ; interface :
`env-8-interface.md` §3.10. Validation dans VSCodium : session S2, `env-9-validation.md`.

## 1. Décisions de l'utilisateur (2026-10-14)

| # | Décision |
| --- | --- |
| D1 | `CMakeUserPresets.json` versionné dans le dépôt de la graine sous `project/scion/`, greffé à la racine du trunk par le greffon local `lepton@project-<projet>` (version `*`, chemin dans le dépôt `project`) ; hérite des presets cachés du `CMakePresets.json` du noyau. |
| D2 | `<ROOTSTOCK>/<projet>.code-workspace`, non versionné, `launch` et `tasks` intégrés ; aucun `.vscode/` dans le trunk ni dans un clone. |
| D3 | Rootstock de validation durable `~/lepton-tools-dev/essais/env-9` (§5). |
| D4 | S1 : code, tests, essais CLI ; S2 : validation GUI. |
| D5 | Débogage carte : `configFiles` = champ `openocd` du BSP tel quel. Cfg du BSP `nucleo-wl55jc1` rendue autonome (elle source `interface/stlink.cfg`) ; l'enveloppe générée par son `CMakeLists.txt` n'ajoute plus que `adapter serial` (§6). |
| — | Tâche 2 de l'étape (`-ffile-prefix-map`) sans objet : PA-1 (ni option, ni `substitute-path`). |

## 2. Sources des données (CFG-1)

`lepton generate` lit : `lepton-graine.json` (projet, BSP, backend, configurations, chemin du XML),
les manifestes greffés (BSP : `coeur`, `abi_flottante`, `qemu.machine`, `openocd`, `svd`,
`destination`), le `CMakePresets.json` du noyau (présence des presets `cross` et `host`
seulement) et le PATH (outils, NF-3). Le XML mklepton n'est jamais ouvert : seul son chemin
(`mklepton_xml`) est recopié dans `LEPTON_MKCONF` (test `test_generate_never_reads_mklepton_xml`,
XML rendu illisible).

## 3. Fichiers générés

| Fichier | Emplacement | Versionné | Mention « ne pas éditer » |
| --- | --- | --- | --- |
| `CMakeUserPresets.json` | `<graine>/project/scion/`, lien `trunk/CMakeUserPresets.json` | oui (graine ; commit par l'utilisateur) | champ `vendor.lepton.note` |
| `<projet>.code-workspace` | `<ROOTSTOCK>/` | non | commentaire en première ligne |

Écriture seulement si le contenu change ; aucun horodatage. Premier appel : `scion seed-scion-add`
du greffon projet, `scion seed-clone`, suppression des fichiers système réguliers du trunk (Q8),
`scion graft --scion` ; appels suivants : regreffe seulement si le lien du trunk manque. Contrôle
final du trunk (`finish`) ; pas de reconfiguration CMake (aucun manifeste ni greffon compilé
modifié). Rappel de commit de la graine si elle a changé.

### 3.1 Presets (CFG-6, BLD-5)

Par configuration `C` de la graine : preset de configuration, de construction et de test
`<projet>-<C>`, `inherits: cross` (chaîne croisée, `LEPTON_MKLEPTON`, `binaryDir`
`${sourceDir}/../build/${presetName}`, `CMAKE_EXPORT_COMPILE_COMMANDS` hérités de `base`).

| Variable | Valeur |
| --- | --- |
| `CMAKE_BUILD_TYPE` | `construction` |
| `LEPTON_ISA` | table fixe du cœur (§4, P1) |
| `LEPTON_CPU` | `coeur` du BSP |
| `LEPTON_BOARD` | `bsp` de la graine |
| `LEPTON_KAL_BACKEND` | `backend` |
| `LEPTON_MKCONF` | `mklepton_xml` |
| `LEPTON_FLOAT_ABI` | `abi_flottante` du BSP, si présent (sinon défaut du cœur, `cmake/cpu/*.cmake`) |

`cmake --list-presets` (trunk) liste les presets de la graine puis ceux du noyau.

### 3.2 Espace de travail

- `folders` : `trunk` d'abord (seul chemin d'ouverture des fichiers, PA-1), puis un dossier
  `git · <nom>` par dépôt git distinct : graine, puis greffons greffés (racine git de chaque
  clone, dédoublonnée ; `building`, hors git, omis ; greffon projet = dépôt de la graine).
- `settings` : `files.exclude` (`.DS_Store`, `._*`) ; CMake Tools : `useCMakePresets: always`,
  `configureOnOpen: false`, `ignoreCMakeListsMissing: true`,
  `copyCompileCommands: <ROOTSTOCK>/build/.active/compile_commands.json` ; clangd : `clangd.path`
  (§4, P3), `--compile-commands-dir=<ROOTSTOCK>/build/.active`, `--background-index`,
  `--query-driver=<arm-none-eabi-gcc>` ; Cortex-Debug : `gdbPath`, `armToolchainPath`,
  `openocdPath` (si configuration carte).
- `launch` : une configuration Cortex-Debug par configuration de la graine, `runToEntryPoint:
  main`, `preLaunchTask` = construction du preset, `executable` `build/<preset>/lepton.elf`,
  `svdFile` si le BSP déclare `svd` (aucun BSP actuel : DBG-4 non vérifiable, PA-7 Q11).
  - `qemu` : `servertype: qemu`, `machine` du BSP, `cpu` (§4, P2), `serverpath` résolu.
    Cortex-Debug lance `qemu-system-arm -cpu … -machine … -nographic -semihosting-config … -gdb
    tcp::<port> -S -kernel <elf>` (lu dans `dist/debugadapter.js` de 1.13.0-pre6).
  - `carte` : `servertype: openocd`, `configFiles` = fichiers `openocd` du BSP par le trunk.
- `tasks` (type `process`, `cwd` = trunk) : `regreffer` (`lepton graft`), `configurer host`,
  `mklepton (preset host)`, puis par configuration `configurer`, `construire` (groupe build,
  `$gcc`), et pour `qemu` : `QEMU … (console série)` (`-M <machine> -kernel <elf> -nographic
  -monitor none -serial stdio`, terminal dédié, DBG-1), `test de fumée` et `banc KAL`
  (`ctest --preset … -L smoke|kal`, `PYTHONDONTWRITEBYTECODE=1`, TST-1) ; pour `carte` :
  `flasher` (`openocd -f … -c "program <elf> verify reset exit"`).
- `extensions.recommendations` : clangd, CMake Tools, Cortex-Debug.

## 4. Propositions appliquées, à confirmer

| # | Proposition |
| --- | --- |
| P1 | `LEPTON_ISA` déduit du cœur par une table fixe de lepton : `cortex-m0plus` → `armv6m`, `cortex-m3`/`m4f`/`m7` → `armv7m` (le manifeste ne porte pas l'ISA). |
| P2 | Cœur QEMU (`-cpu` de Cortex-Debug) : `cortex-m4f` → `cortex-m4`, `cortex-m0plus` → `cortex-m0`, sinon identique. |
| P3 | clangd : `--clangd PATH`, sinon le plus récent des `clangd`, `clangd-N`, `clangd-mp-N` du PATH dont `--version` n'est pas celle d'Apple ; à défaut `clangd` avec avertissement. Mac : `/opt/local/bin/clangd-mp-21`. |
| P4 | Preset actif → clangd : `cmake.copyCompileCommands` vers `build/.active/` et `--compile-commands-dir` fixe ; index clangd unique dans `build/.active/.cache` (IDE-5 à vérifier en S2). |
| P5 | Clones en dossiers de l'espace (IDE-2) ; risque d'ouverture sous un second chemin (PA-1) : masquage à essayer en S2. |
| P6 | Noms : preset `<projet>-<configuration>`, tâches `lepton : …`, dossiers `git · <nom>`. |
| P7 | `lepton generate` n'a pas d'option `--no-cmake` : il ne reconfigure jamais. |
| P8 | Greffon projet hors du verrou `seed lock` (c'est le dépôt de la graine, qui porte le verrou) ; rôle `projet` dans `seed status`. |
| P9 | Chemins absolus dans l'espace de travail (non versionné, propre à la machine). |

## 5. Essais CLI (rootstock `~/lepton-tools-dev/essais/env-9`)

Création : `lepton seed new env9 -C ~/lepton-tools-dev/essais/env-9 --bsp qemu-mps2-an386
--backend freertos --mkconf sys/user/tauon-basic/etc/mkconf_tauon_basic_qemu_mps2.xml` avec les
trois greffons clonés de `~/lepton/depots/…` en `file://localhost…@master` (comme le bout en
bout) ; configuration `release-qemu` ajoutée ; graine commitée.

| Contrôle | Résultat |
| --- | --- |
| `lepton generate` ×2 | 2ᵉ appel : « inchangé » pour les deux fichiers, graine propre |
| `cmake --list-presets` (trunk) | `env9-debug-qemu`, `env9-release-qemu`, puis les 16 presets du noyau (CFG-6) |
| Construction `env9-debug-qemu` et `qemu-mps2-an386-freertos` (noyau) | caches CMake identiques (`LEPTON_*`, `CMAKE_BUILD_TYPE`, drapeaux) ; `lepton.bin` : 1 octet différent, la chaîne `__TIME__` (16:54:00 / 16:54:07) ; reconstruits avec le même `SOURCE_DATE_EPOCH` : `lepton.bin` et `lepton.hex` identiques (sha256 `2bdfaf23…`, `f75cce04…`) → BLD-5 |
| `ctest --preset env9-debug-qemu -L smoke` | `smoke.lsh` Passed |
| `ctest --preset env9-debug-qemu -L kal` | 18/18 |
| QEMU avec les arguments de Cortex-Debug + `arm-none-eabi-gdb --batch` (`break main`) | arrêt sur `main` (pc 0x37c), source sous le chemin du trunk (DBG-2 en CLI) |
| Trunk | aucun fichier régulier hors `.DS_Store` du Finder (supprimés par `generate`, Q8), aucun lien cassé |

`pytest` : 116 tests verts (10 nouveaux) ; `scripts/bout-en-bout.sh` : succès.

## 6. Correction du BSP `nucleo-wl55jc1` (D5)

Constat (sans carte, `openocd -f <cfg> -c shutdown`) : la cfg du BSP seule échoue (aucune
interface) ; ajouter `-f interface/stlink.cfg` partout casse le F429 (« already specified hl_layout
stlink », sa cfg source `board/st_nucleo_f4.cfg`). Correction, branche `devenv/env-9` du clone
`<ROOTSTOCK>/depots/lepton-bsp/nucleo-wl55jc1` (9489e7d) :
- `debug/openocd-nucleo-wl55jc1.cfg` : `source [find interface/stlink.cfg]` en tête ;
- `CMakeLists.txt` : enveloppe = `source <cfg du BSP>` puis `adapter serial …` (carte et paire).

Contrôles : cfg seule, enveloppe sans et avec numéro de série → `shutdown command invoked`, aucune
erreur ; reconstruction `nucleo-wl55jc1-{embos,freertos}` comparée à l'oracle
`oracles/env-6-lot-wl/` : 0 écart de sections ou de symboles, empreintes différentes (horodatage
`__TIME__`, cf. §5). Flash et débogage réels : ENV-11 (PA-11). Skill `lepton-cibles` mise à jour.

## 7. Reste pour S2 (VSCodium, avec l'utilisateur)

Ouvrir `codium ~/lepton-tools-dev/essais/env-9/env9.code-workspace` ; vérifier : CMake Tools
(presets, cibles `lepton`, `kernel`, `lib`, `sbin`, `bin`, `bsp`), changement de preset et
réindexation clangd (P4, IDE-5), panneau Source Control (IDE-2), masquage des clones (P5,
IDE-4), tâche QEMU (invite `lsh`, DBG-1), débogage QEMU (arrêt sur `main`, point d'arrêt posé
via le trunk, DBG-2), tâche banc KAL (TST-1). Résultats : `env-9-validation.md`.
