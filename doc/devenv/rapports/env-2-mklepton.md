# ENV-2 — mklepton et son format XML

Relevé du 2026-10-13, lecture seule, clone noyau `master` 6b62af5. Chemins relatifs à `scion/`.

## 1. Sources et analyseur

- C : `tools/mklepton/src/mklepton.c` (2 572 l.), `mklepton.h` (287 l. ; noms d'éléments et
  d'attributs l. 43-91), `kernel_stub.h` (175 l. ; vue minimale du VFS).
- Analyseur : **expat** (`mklepton.c:43` ; `XML_ParserCreate`, `XML_SetElementHandler`, `XML_Parse`
  par blocs de 8 Ko, l. 1550-1595). Aucune validation de schéma ; pas de version de format.
- Moteur : noyau Lepton statique hôte lié à mklepton (VFS, UFS, rootfs, disque hôte `/dev/hd/hdc`).
- Construction : preset `host` seul (`cmake/components/mklepton.cmake:7-10`, `expat` par nom brut).
- Ligne de commande (`mklepton.c:2370-2440`) : `-o` (chdir, `dest_path` ignorés), `-s` (racine des
  sources), masques `-a -b -d -f -k -r`, `-t <cible>` (sans `-t`, tout `<target>` est ignoré,
  l. 1436-1437).
- Hérités hors CMake : `tools/mklepton/prj/scons/SConstruct`, `tools/mklepton/mkconf{,_9260}.xml`,
  `tools/bin/mklepton_gnu` (ELF i386), `tools/bin/mklepton_gnu.sh`, `tools/bin/mklepton.exe` +
  `msvcr100d.dll`, `tools/config/SConstruct`.
- Dépôt parent : `tools/migration/{mklepton_oracle.sh, mklepton_oracle_rewrite.py, mklepton_ref_manifest.py, mkconf_relpaths.py}` ;
  doc `doc/migration/mklepton.md`, `mklepton-ref.md`, `handoff/etape-4-mklepton.md`.

## 2. Fichiers XML

29 fichiers, aucun sous un `prj/`.

| Usage | Fichiers |
| --- | --- |
| Presets (5) | `sys/user/tauon-basic/etc/mkconf_tauon_basic_{qemu_mps2, nucleo_f439zi, nucleo_wl55jc1, samd21_xplained_pro, stm32f746g_disco}.xml` |
| Test hôte (1) | `sys/user/tauon-basic/etc/mkconf_tauon_basic_lwip_stm32f4-olimex-p407.xml` |
| Hérités (23) | `sys/user/tauon-basic/etc/mkconf_{base, complet, tauon_basic, tauon_basic_at91samd20, _at91samv71, _cmsis, _lm3s, _lm3s_uip, _stm32f4, _stm32f4_lwip, _stm32f4_uip, _stm32f4-discovery, _stm32f469i-eval, _stm32f469i-eval_with-ethernet, _stm32wl55jci_nucleo, tauon_uip_basic, tauon_uip_trifecta}.xml` ; `sys/user/tauon_sampleapp/etc/mkconf_tauon_sampleapp_{at91samd20, gnu, gnu_k60, gnu_simple}.xml` ; `tools/mklepton/mkconf{,_9260}.xml` |

| Preset(s) | XML | `-t` |
| --- | --- | --- |
| `qemu-mps2-an386-*`, `qemu-mps2-an500-*` | `mkconf_tauon_basic_qemu_mps2.xml` | `cortexm_lepton` |
| `nucleo-f439zi-*` | `mkconf_tauon_basic_nucleo_f439zi.xml` | `cortexm_lepton` |
| `nucleo-wl55jc1-*` | `mkconf_tauon_basic_nucleo_wl55jc1.xml` | `cortexm_lepton` |
| `samd21-xplained-pro-*`, `stm32f746g-disco-*` | XML respectifs | `cortexm_lepton` |
| `host` | aucun (tables écrites à la main, `src/kernel/core/arch/host/static/`) ; tests sur Olimex et tous les XML de cartes | – |

Le XML ne dépend pas du backend KAL. `qemu_mps2` et `nucleo_f439zi` ne diffèrent que par
`include_absolute_path`, `cpu freq`, les `<dev>` et les `src_file`.

## 3. Éléments × fréquence × fichiers

Comptage par regex sur les balises ouvrantes, commentaires retirés. « Cartes » = 5 XML de presets ;
« Olimex » = test hôte ; « Hérités » = 23 autres.

| Élément | Total | Cartes | Olimex | Hérités | Fichiers | Attributs observés | Lus par mklepton |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `mklepton` | 29 | 5 | 1 | 23 | 29 | – | `dest_path` (l. 1264) |
| `target` | 304 | 25 | 13 | 266 | 29 | `name` | `name` (l. 1331) |
| `arch` | 82 | 10 | 4 | 68 | 29 | `dest_path` (55), `include_absolute_path` (27) | les deux (l. 1293, 1300) |
| `kernel` | 29 | 5 | 1 | 23 | 29 | – | – |
| `cpu` | 55 | 5 | 2 | 48 | 29 | `freq` (55), `type` (27) | `freq`, `type` (l. 506, 515) |
| `heap` | 29 | 5 | 1 | 23 | 29 | `size` | `size` |
| `process` | 29 | 5 | 1 | 23 | 29 | `max` | `max` |
| `thread` | 0 | – | – | – | 0 | – | `max` (l. 1450) |
| `openfiles` | 31 | 5 | 1 | 25 | 29 | `max` | `max` |
| `descriptors` | 31 | 5 | 1 | 25 | 29 | `max` | `max` |
| `cpufs` | 31 | 5 | 1 | 25 | 29 | `size`, `node`, `blocksz` | + `block`, `option` lus sans effet (l. 689-698) |
| `env` | 29 | 5 | 1 | 23 | 29 | `path` | `path` |
| `network` | 28 | 5 | 1 | 22 | 28 | `use` | `use` |
| `boot` | 47 | 0 | 2 | 45 | 24 | `dest_path` (47), `dev` (1), `delay` (1) | les trois (l. 787-794) |
| `command` | 47 | 0 | 2 | 45 | 24 | `arg` (47), `value` (2) | les deux |
| `mount` | 24 | 0 | 1 | 23 | 24 | `dest_path` | `dest_path` |
| `disk` | 30 | 0 | 1 | 29 | 24 | `type`, `dev`, `point` | idem |
| `devices` | 84 | 10 | 3 | 71 | 29 | – | – |
| `dev` | 612 | 43 | 22 | 547 | 29 | `name`, `use` | idem |
| `binaries` | 97 | 12 | 6 | 79 | 29 | `src_path`, `dest_path` | idem |
| `bin` | 723 | 61 | 28 | 634 | 29 | `name`, `stack`, `priority`, `timeslice` | idem, obligatoires (l. 1150-1155) |
| `files` | 44 | 5 | 3 | 36 | 29 | – | – |
| `file` | 126 | 10 | 13 | 103 | 29 | `name`, `src_file`, `dest_path` | idem |
| `directories` / `directory` | 0 | – | – | – | 0 | – | `src_path`, `dest_path` (l. 1376-1395) |

Valeurs de `<target name>` (occurrences / fichiers) : `cortexm_lepton` 124 / 20, `win32_lepton` 88 / 17,
`arm9_lepton` 35 / 7, `gnu32_lepton` 34 / 7, `arm7_lepton` 18 / 4, `cmsis_lepton` 5 / 1.
`cpu type` : `cpu_arm7` (19), `cpu_arm9` (8). `arch dest_path` : `generated` (cartes),
`sys/root/src/kernel/core/arch/{cortexm,win32,arm}`, chemins absolus anciens (`/home/…`, `/opt/lepton/…`,
`$(HOME)`), `../config/{arm7,arm9,x86}`.

## 4. Candidats au retrait (CFG-8)

| Élément | Raison |
| --- | --- |
| `<target name="…">` comme sélecteur d'architecture | Seul `cortexm_lepton` est utilisé ; `arm7_lepton`, `arm9_lepton`, `win32_lepton`, `gnu32_lepton`, `cmsis_lepton` = cibles gelées ou simulateurs |
| `<arch dest_path>` | Répertoire de sortie : relève de CMake (`-o`), déjà `generated` dans les cartes |
| `<arch include_absolute_path>` | Inclut le `user_kernel_mkconf.h` de la carte : lien vers le BSP, à reconsidérer (ENV-6) |
| `<cpu type>` | Architecture ; ne produit qu'un commentaire `//#define CPU_…` (`mklepton.c:401-406`) ; `cpu_arm9` hors liste → `NULL` (l. 516-524) |
| `<cpu freq>` | Propriété matérielle de la carte (`__KERNEL_CPU_FREQ`) : à déplacer vers le BSP ? (question) |
| `<cpufs block>`, `<cpufs option>` | Lus sans effet |
| `<dev name>` des cibles gelées dans les hérités | `dev_at91*`, `dev_atsam926*`, `dev_win32_*`, `dev_linux_*`, `dev_twrk60n512_*`, `dev_k60n512_*` |
| Code mklepton | `cpu_type_enum_t` (`CPU_GNU32`, `CPU_ARM7`, `CPU_M16C62`, `mklepton.h:96-107`) ; constantes `MK_DEV_*` M16C / LCD / RTC inutilisées (`mklepton.h:154-162`) ; `_mk_rtc()` (`/dev/rtc0` m41t81, `mklepton.c:2326-2357`) ; `boot_dev` par défaut `/dev/kb0` (l. 124) |
| 23 XML hérités | Aucun preset ; à migrer ou supprimer (« XML existants validés ou migrés », CFG-8) |

Éléments acceptés mais absents de tout XML : `thread`, `directories`, `directory`.

## 5. Sorties

| Sortie | Producteur | Contenu |
| --- | --- | --- |
| `kernel_mkconf.h` | `<kernel>` (`mklepton.c:358-484`) | inclut `include_absolute_path` et `dev_dskimg.h` ; `__KERNEL_CPU_FREQ`, `__KERNEL_HEAP_SIZE`, `__KERNEL_PTHREAD_MAX`, `__KERNEL_PROCESS_MAX`, `MAX_OPEN_FILE`, `OPEN_MAX`, `__KERNEL_ENV_PATH`, `__KERNEL_NET_IPSTACK` |
| `dev_mkconf.c` — **table des périphériques** | `<devices>/<dev use="on">` (`_mk_dev`, l. 2157-2208) | `extern dev_map_t <nom>;` ; `pdev_map_t const dev_lst[]`, `pdev_lst`, `max_dev` |
| `bin_mkconf.c` | `<binaries>/<bin>` (`_mk_binaries`, l. 1606-1776) | prototypes `<nom>_main` ; `_bin_lst[]`, `bin_lst_size`, `bin_lst` |
| `.fsflash.o` | image UFS 1.5 sur `/dev/hd/hdc` (`dev_host_fileflash.c:4,24`) | `_vfs_makefs` selon `<cpufs>` ; en-têtes `exec_file_t` par `<bin>`, `<file>`, `<directory>` |
| `dev_dskimg.c` / `.h` | `_mk_dskimg` (l. 2224-2315) | `filecpu_memory[]` (image en tableau C), `filecpu_memory_size` |
| `.boot`, `.mount` | `_mk_boot`, `_mk_mount` (l. 2076-2150) | seulement si `<boot>`/`<mount>` : jamais pour les 5 cartes |

Compilation et liaison : `dev_mkconf.c`, `bin_mkconf.c`, `dev_dskimg.c` → bibliothèque STATIC
`lepton_generated` (`firmware.cmake:17-22`) dans le groupe RESCAN de `lepton` et `kal_bench`.
`kernel_mkconf.h` inclus par `src/kernel/core/kernelconf.h:80`.
Consommateurs : `pdev_lst`/`max_dev` (`core-segger/kernel.c:325,388-401`, `core-freertos/kernel.c:392-401`,
`core-static/kernel_static.c:130-146`) ; `bin_lst` (`kernel/core/bin.c:69-78`,
`core-freertos/process.c:910-929`) ; `filecpu_memory` (`kernel/dev/dev_cpufs/dev_cpufs.c:158-161`).

**Décision 2** (table des périphériques dans l'exécutif) : aujourd'hui dans une archive
(`lepton_generated`) liée en groupe RESCAN avec noyau et BSP ; la dépendance croisée est absorbée par
`--start-group/--end-group`. La mettre en sources de l'exécutable est un changement local de
`firmware.cmake`.

## 6. Tests existants

`host.mklepton` (double exécution déterministe, 8 sorties, signature « ufs 1.5 », relecture par
`test_ufs_check`) et `host.mklepton_empreintes` (empreintes SHA-256 des sorties pour chaque XML de
carte et Olimex, `tests/host/mklepton_empreintes.sha256`) : base de non-régression directe pour ENV-4.
