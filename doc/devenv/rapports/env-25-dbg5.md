# ENV-25 — DBG-5 : déboguer `mklepton` sur l'hôte

Session du 2026-11-02, branche lepton-tools `devenv/env-25` (depuis `main` 95f30e3). Clone noyau
`master` 0bdce87, non touché.

## 1. Audit (lecture seule)

### 1.1 Invocation de `mklepton` par la construction
Règle : `lepton_generate()` de `cmake/mklepton.cmake` (clone noyau), `add_custom_command` :

```
cd <ROOTSTOCK>/build/<preset>/generated/board
cmake -E make_directory <ROOTSTOCK>/build/<preset>/generated/board
cmake -E env SOURCE_DATE_EPOCH=0 <ROOTSTOCK>/trunk/../build/host/mklepton \
  -s <ROOTSTOCK>/trunk -o <ROOTSTOCK>/build/<preset>/generated/board \
  --cpu-freq <frequence_cpu> --kernel-config-header <SOURCE_ROOT>/<destination>/<entete_config_noyau> \
  <LEPTON_MKCONF>
```

Relevé par `ninja -t commands` :

| Preset | `--cpu-freq` | `--kernel-config-header` | XML |
| --- | --- | --- | --- |
| `qemu-mps2-an386-embos` | 25000000 | `sys/root/src/kernel/dev/bsp/qemu-mps2-an386/include/user_kernel_mkconf.h` | `sys/user/tauon-basic/etc/mkconf_tauon_basic_qemu_mps2.xml` |
| `nucleo-f429zi-embos` | 168000000 | `sys/root/src/kernel/dev/bsp/nucleo-f429zi/include/user_kernel_mkconf.h` | `sys/user/tauon-basic/etc/mkconf_tauon_basic_nucleo_f439zi.xml` |

- Une invocation par preset ; tous les arguments sont connus de lepton : XML (`mklepton_xml` de la
  graine de projet, `LEPTON_MKCONF` des presets du noyau pour la graine de référence), BSP
  (`frequence_cpu`, `destination`, `entete_config_noyau` du manifeste).
- `mklepton` fait `chdir(-o)` : le répertoire de sortie doit exister (créé par `make_directory`
  dans la règle CMake). `-s` passe par `realpath`.
- Sorties : `kernel_mkconf.h`, `dev_mkconf.c`, `bin_mkconf.c`, `dev_dskimg.c/.h`, `.boot`,
  `.mount` dans `-o`. Lancé sur la sortie de la construction, un essai réécrit ces fichiers
  (contenu identique, `SOURCE_DATE_EPOCH=0`, mais dates nouvelles → recompilation, et fichiers
  partiels si la session de débogage est interrompue).
- Le preset `host` lui-même n'invoque pas `mklepton -s` (aucune ligne dans `ninja -t commands`).

### 1.2 Informations de débogage de `build/host/mklepton`
- Preset `host` : `CMAKE_BUILD_TYPE` `Debug`, `CMAKE_C_FLAGS_DEBUG` `-g`, compilateur
  `/Library/Developer/CommandLineTools/usr/bin/cc` (Apple clang).
- macOS : DWARF laissé dans les `.o` (carte de débogage, 29 entrées `OSO` :
  `build/host/CMakeFiles/mklepton.dir/…/mklepton.c.o`, `build/host/libkernel.a(…)`), lu par lldb
  sans `dsymutil`.
- Chemins des sources : **trunk** (`DW_AT_name`
  `/Users/cle_d_anton/lepton/trunk/tools/mklepton/src/mklepton.c`, `comp_dir`
  `<ROOTSTOCK>/build/host`, `SO /Users/cle_d_anton/lepton/trunk/sys/root/src/kernel/core/`).
  Comparaison avec F8 d'ENV-12 : pas d'écart clone/trunk dans le DWARF ; un point d'arrêt posé par
  le trunk correspond tel quel, aucun `sourceMap` nécessaire. Le traceur F8 de l'extension (tous
  types de débogage) reste sans objet ici ; constat à faire lors de l'essai.

### 1.3 Débogueur par hôte
- Mac : CodeLLDB `vadimcn.vscode-lldb@1.12.3` installé (`type` `lldb`, `request` `launch`,
  `program`, `args`, `cwd`, `env`).
- Debian : `scripts/extensions.lst` contient déjà CodeLLDB ; `install-vscodium.sh` installe le
  paquet `linux-x64` à somme épinglée (`CODELLDB_SHA256_LINUX_X64`). CodeLLDB embarque son lldb et
  lit le DWARF de gcc. Aucune extension à ajouter (PA-10 inchangé). gdb de Debian
  (`gdb-multiarch`) exigerait une autre extension (cpptools absent d'Open VSX, ou Native Debug).
- Recommandations de l'espace (`extensions.recommendations`) : clangd, CMake Tools, Cortex-Debug ;
  CodeLLDB absent.

### 1.4 Espaces concernés
| Espace | Configurations | Combinaisons (BSP, XML) distinctes |
| --- | --- | --- |
| Graine de projet (ex. `essais/env-9/env9.code-workspace`, `essais/env-11/*/`) | N configurations, un BSP, un `mklepton_xml` | 1 |
| Graine de référence `<ROOTSTOCK>/original-tree.code-workspace` | 16 presets de carte | 7 (an386, an500, f429zi, f439zi, f746g, samd21, wl55jc1) |
| `essais/env-13-vierge/original-tree.code-workspace` | graine de référence | idem selon BSP greffés |

Tâche existante réutilisable : `lepton : mklepton (preset host)` (configurer `host`, construire la
cible `mklepton`), dont dépendent déjà les tâches `configurer <preset>`.

### 1.5 Propositions pour le PA-37
| Question | Proposition |
| --- | --- |
| Nombre et nom | Un lancement par combinaison (BSP, XML) distincte des configurations dont le BSP est greffé : 1 pour une graine de projet, 7 pour `<ROOTSTOCK>` ; nom `Déboguer mklepton <BSP> (<fichier XML>)` |
| Arguments | Ceux de la construction (`-s`, `--cpu-freq`, `--kernel-config-header`, XML, `SOURCE_DATE_EPOCH=0`), sauf `-o` : `<ROOTSTOCK>/build/.mklepton/<BSP>/` (hors trunk, aucune sortie de preset touchée) ; `cwd` = ce répertoire |
| Débogueur | CodeLLDB (`type` `lldb`) sur le Mac et sur Debian ; `extensions.lst` inchangé ; CodeLLDB ajouté aux recommandations de l'espace |
| Tâche préalable | Une tâche `lepton : préparer le débogage de mklepton` : `cmake -E make_directory` des répertoires de sortie, `dependsOn` `lepton : mklepton (preset host)` ; `preLaunchTask` de chaque lancement |
| `build/host/mklepton` absent | Lancement écrit quand même (la tâche préalable le construit), sans ligne d'information |

PA-37 tranché le 2026-11-02 : propositions §1.5 retenues en bloc (`DEVENV-STATUS.md` §Décisions).

## 2. Implémentation (lepton-tools, `devenv/env-25` ac0cfc1)
- `lepton/generate.py` : `Configuration.mkconf` (graine de projet : `mklepton_xml` ; graine de
  référence : `LEPTON_MKCONF`) ; `mklepton_runs()` (combinaisons (BSP, XML) distinctes, BSP greffé),
  `mklepton_launch()` (CodeLLDB), tâche `lepton : préparer le débogage de mklepton`,
  recommandation `vadimcn.vscode-lldb`. Règle : `rapports/env-8-interface.md` §17.
- Tests écrits d'abord : `test_mklepton_host_launch` (graine de projet ; option
  `--kernel-config-header` absente puis présente selon le BSP) et
  `test_reference_mklepton_host_launches` (graine de référence ; BSP non greffé sans lancement).
- Tests existants ajustés, sans changement de ce qu'ils vérifient : sélection des lancements
  Cortex-Debug (`_target_launches`, 6 lignes de `test_generate.py`, 1 de `test_reference_seed.py`) ;
  `test_build_tasks_gcc_matcher` sélectionne la tâche mklepton par son libellé exact (le libellé de
  la tâche ajoutée contient « mklepton »).
- `pytest` : 218 passés (216 + 2), 387,9 s.
- `pipx install --force <LEPTON_TOOLS>` depuis `devenv/env-25` ac0cfc1 (`lepton 0.1.0`).

## 3. Contrôles
### 3.1 Fichiers générés
Relevés `~/lepton-tools-dev/essais/env-25-releve/{avant,apres}/<rootstock>/` (script : régénération
par `lepton generate` juste avant chaque relevé, E-1 ; avant : lepton installé de `devenv/env-23`
5e03b27, code de `lepton/` identique à `main` 95f30e3) ; diff : `diff-avant-apres.txt`.

| Rootstock | `generate` avant / après | Lancements hôtes ajoutés | `CMakeUserPresets.json` |
| --- | --- | --- | --- |
| `<ROOTSTOCK>` (`original-tree`) | 0 / 0 | 7 | — (graine de référence) |
| `essais/env-13-vierge` | 0 / 0 | 7 | — |
| `essais/env-9` | 0 / 0 | 1 (`qemu-mps2-an386`, `mkconf_env9.xml`) | identique |
| `essais/env-11/qemu` | 0 / 0 | 1 | identique |
| `essais/env-11/f429zi` | 0 / 0 | 1 | identique |
| `essais/env-11/wl55jc1` | 0 / 0 | 1 | identique |
| `essais/env-11/qemu-gra2` | 1 / 1 (attendu : BSP retiré, essai GRA-2, comme en ENV-18 et ENV-21) | — | identique |

Diff : uniquement les lancements hôtes (en fin de `launch`), la tâche préalable (après
`lepton : mklepton (preset host)`) et `vadimcn.vscode-lldb` dans les recommandations ; les seules
lignes retirées sont `"marus25.cortex-debug"` (6), réécrite avec une virgule.

### 3.2 Arguments et exécution hors débogueur
- Arguments des 7 lancements de `<ROOTSTOCK>` comparés à `ninja -t commands` du preset embOS de
  chaque BSP : identiques hors `-o`.
- `mklepton` exécuté avec `program`, `args`, `cwd`, `env` des lancements an386 et f429zi : code 0 ;
  les 6 fichiers produits dans `build/.mklepton/<BSP>/` sont identiques octet pour octet à
  `build/<preset>/generated/board/` ; ces derniers ne sont pas touchés (date 11:32 inchangée).
- Aucun fichier de construction modifié (CMake, presets du noyau, clone noyau propre) : binaires de
  cible inchangés par construction.
- `<ROOTSTOCK>` : `lepton check` code 0 (19 fichiers) ; trunk : seul fichier régulier
  `.scion.grafted.list` (scion), 0 lien cassé.

### 3.3 Essai VSCodium (Mac, fait par l'utilisateur, 2026-11-02)
Espace `<ROOTSTOCK>/original-tree.code-workspace`, lancement « Déboguer mklepton qemu-mps2-an386
(mkconf_tauon_basic_qemu_mps2.xml) », point d'arrêt dans `main` de
`trunk/tools/mklepton/src/mklepton.c`.

| Critère | Résultat |
| --- | --- |
| Arrêt dans `mklepton` (DBG-5) | atteint |
| Variables `argc`, `argv` | lisibles |
| Fichier source ouvert à l'arrêt | par le trunk (DWARF en chemins du trunk, §1.2 ; aucun `sourceMap`) |
| Exécution de la tâche préalable | non rapportée |

## 4. Bilan (PA-38)
| Critère du fichier d'étape | État |
| --- | --- |
| PA-37 et PA-38 tranchés et consignés | PA-37 oui ; PA-38 : ce rapport |
| `pytest` vert, nouveaux tests compris | oui, 218 |
| Fichiers générés : diff limité au lancement et à la tâche ajoutés | oui (+ recommandation CodeLLDB, décidée au PA-37) |
| Arrêt dans `mklepton` constaté sous VSCodium (Mac) | oui |

Reporté à ENV-28 : essai Debian (CodeLLDB `linux-x64`, DWARF de gcc).
