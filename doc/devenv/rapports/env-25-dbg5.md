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
