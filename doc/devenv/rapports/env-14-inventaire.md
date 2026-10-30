# ENV-14 — Inventaire du nettoyage de l'arbre (tâche 1, PA-15)

Session du 2026-10-30. Lecture seule : aucun fichier de l'arbre n'a été modifié.
Rootstock `~/lepton` (trunk 4 037 liens + 26 fichiers réguliers), clone noyau `devenv/env-14` =
`master` 16a331b, 7 greffons famille/BSP à `master`.

## 1. Méthode

| Critère | Source | Outil |
| --- | --- | --- |
| Greffon propriétaire | cible du lien (`realpath`) comparée aux clones de `trunk/.scion.grafted.list` | `env-14-inventaire.py` |
| Versionné | `git -C <clone> ls-files` | `env-14-inventaire.py` |
| Lu (direct) | 15 répertoires `~/lepton/build/<preset>` (host + 14 presets d'`oracles/env-13-apres`) : `ninja -t deps` et tout chemin absolu du trunk cité dans `build.ninja`, `*.cmake`, `CTestTestfile.cmake`, `compile_commands.json`, `*.rsp`, fichiers générés, `*.map` | `env-14-inventaire.py` |
| Lu (indirect) | chemin relatif d'une feuille cité dans un fichier texte lu (XML mkconf, CMake, scripts de test), jusqu'au point fixe | `env-14-classer.py` |
| Ensemble de la migration | `doc/migration/perimetre.csv` du clone noyau (actif, différé, hors-projet ; « absent » = fichier non source) | `env-14-classer.py` |
| Références | `grep -rIF` du chemin (ou de son nom) dans le clone noyau (hors `doc/migration/`, historique), les 7 greffons, lepton-tools (`lepton/`, `extension/src/`, `scripts/`, `schemas/`, `doc/` hors `rapports/` et `handoff/`, `tests/`) | manuel, résultats §4-§5 |

`tools/migration/build_closure.py` n'est pas réutilisable : il calcule la fermeture des projets
IAR (`.ewp`), retirés à la migration. Le repli prévu par le fichier d'étape (`ninja -t deps`) est
employé.

L'usage indirect corrige un manque de la seule lecture de ninja : `tests/host` (ctest du preset
host) passe à mklepton le XML `mkconf_tauon_basic_lwip_stm32f4-olimex-p407.xml` par un chemin
relatif, qui embarque à son tour `etc/.init_olimex_with_net`, `.boot`, `.mount`, les pages
`src/bin/net/html/*` et les scripts `cgi-bin/*.sh` de tauon-basic. Ces 21 fichiers sont conservés.

Reproduire :
```
python3 -I rapports/env-14-inventaire.py ~/lepton host <14 presets> > feuilles.tsv
python3 -I rapports/env-14-classer.py feuilles.tsv <clone noyau>/doc/migration/perimetre.csv ~/lepton/trunk
```
Annexe, une ligne par feuille du trunk (4 063) : `rapports/env-14-inventaire-feuilles.tsv`
(chemin, greffon, versionné, lu, ensemble de la migration, classement, lot, motif).

## 2. Synthèse

| Classement | Lot | Fichiers | Octets | Motif |
| --- | --- | ---: | ---: | --- |
| conserver | C-lu | 782 | 15 609 649 | lu par une construction ou un test (761 directs, 21 indirects) |
| conserver | C-ref | 7 | 22 388 | référencé par CMake, un BSP, `lepton` ou `doc/BUILDING.md` (§3) |
| conserver | C-lic | 43 | 419 286 | licence, provenance, notice du code tiers |
| conserver | C-fonc | 2 103 | 51 029 789 | code du système non configuré par les presets actuels (§3.6) |
| conserver, hors périmètre | C-bsp | 982 | 20 571 895 | BSP et familles sans preset, FreeRTOS 8/9 de leurs configurations |
| conserver, hors périmètre | C-gel | 4 | 1 859 | architecture gelée (ARM9, simulation Windows) |
| **supprimer** | L1 | 16 | 2 374 930 | outillage SCons / Windows hérité (§4) |
| **supprimer** | L2 | 51 | 1 027 020 | application `tauon_sampleapp` (§4, arbitrage A0) |
| **supprimer** | L3 | 3 | 697 | fichiers isolés périmés (§4) |
| **supprimer** | DS | 52 | 334 032 | `.DS_Store` du Finder : 26 réguliers + 26 liens vers le clone noyau (§6) |
| **à arbitrer** | A1-A5 | 20 | 503 847 | §5 |

## 3. Tables par répertoire

Colonnes : fichiers ; lus (directs + indirects) ; classement des non-lus.

### 3.1 Racine du trunk
| Chemin | Greffon | Fichiers | Lus | Classement | Motif |
| --- | --- | ---: | ---: | --- | --- |
| `CMakeLists.txt` | original::tree | 1 | 1 | conserver | construction |
| `CMakePresets.json` | original::tree | 1 | 1 (ind.) | conserver | presets (`cmake --preset`, `lepton`) |
| `tauon_make_link.bat` | original::tree | 1 | 0 | **supprimer (L1)** | jonction Windows `c:\tauon`, aucune référence |
| `building/` | building (`depots/generation/building`, non git) | 0 + 2 `.DS_Store` | – | conserver (`.DS_Store` : DS) | aire de construction de scion |
| `cmake/` (19) | original::tree | 19 | 18 | conserver | `cmake/cpu/cortex-m3.cmake` non lu : valeur documentée de `LEPTON_CPU` (`CMakeLists.txt` l. 5), familles M3 différées (C-ref) |
| `ld/` | original::tree | 3 | 3 | conserver | construction |
| `debug/` | original::tree | 5 | 2 | conserver | `gdbinit-lepton` : `lepton generate` et gdbinit des BSP ; `gdbinit-samd21-…`, `gdbinit-stm32f746…` : `doc/BUILDING.md` (C-ref) |
| `tests/` (27) | original::tree | 27 | 24 | conserver | `board_net.py`, `board_radio.py`, `kal_openocd.py`, `net_qemu.py` cités par CMake et les BSP ; `endurance_board.py` par `BUILDING.md`, `install-macos.sh` ; `tests/kal/arch/armv6m/*` : banc KAL par ISA (C-ref, C-fonc) |

### 3.2 `tools/`
| Chemin | Fichiers | Lus | Classement | Motif / références |
| --- | ---: | ---: | --- | --- |
| `tools/bin/` (`mklepton.exe`, `msvcr100d.dll`, `mklepton_gnu`, `mklepton_gnu.sh`) | 4 | 0 | **supprimer (L1)** | binaires précompilés (2,3 Mo) ; mklepton construit par le preset host ; cités seulement par `tools/config/SConstruct`, `tools/mklepton/prj/scons/SConstruct`, `tools/host/debian/scripts/build_fifo.sh` (tous L1) |
| `tools/config/` (`SConstruct`, `configure_opts.py`, `t-arm-elf`) | 3 | 0 | **supprimer (L1)** | construction SCons héritée ; aucune référence |
| `tools/host/debian/` (2 scripts de taille, 3 scripts réseau `build_fifo`/`start_br`/`stop_br`) | 5 | 0 | **supprimer (L1)** | outillage hôte hérité (`virtual_cpu` gelé, retiré) ; cité par `tools/config/SConstruct` seulement |
| `tools/mklepton/prj/scons/SConstruct` | 1 | 0 | **supprimer (L1)** | SCons de mklepton, remplacé par CMake |
| `tools/mklepton/` (reste) | 3 | 3 | conserver | sources de mklepton |
| `tools/occupation/` | 1 | 1 | conserver | construction |

### 3.3 `sys/user/`
| Chemin | Fichiers | Lus | Classement | Motif / références |
| --- | ---: | ---: | --- | --- |
| `sys/user/build/SConstruct` | 1 | 0 | **supprimer (L1)** | cité par `tools/config/SConstruct` (lien symbolique créé par SCons) seulement |
| `sys/user/tauon_sampleapp/` | 51 | 0 | **supprimer (L2)** | application d'exemple jamais construite par CMake : `prj/scons` (5), `etc` + `etc/scripts` (14, K60/SAMD20), `data/net` (4), `src` (19), `hal/board_freescale_twrk60n512` (8, annexes eCos K60), `bin/.bin` (vide) ; cité par `tools/config/SConstruct` et par un commentaire de provenance de `mkconf_tauon_basic_samd21_xplained_pro.xml` (fichier déjà retiré en ENV-4) ; voir A0 |
| `sys/user/tauon-basic/etc/` | 28 | 21 | conserver, sauf L3, A2 | XML mkconf des presets et de `tests/host` ; `.init_olimex*`, `.boot`, `.mount` lus par le test host ; `.init_win32*` C-gel ; `.init_samv71_with_net` C-bsp ; `memo.txt`, `readme.txt` L3 ; `.init_stm32_with_net`, `.init_with_net` A2 |
| `sys/user/tauon-basic/src/arch/` | 10 | 3 | conserver hors périmètre, sauf A1 | `olimex-stm32-p407` lu par `tests/host` ; samd21, stm32f746 lus ; at91sam9261-ek et win32 : C-gel ; samd20, samv71, f407-discovery, f469i-eval : C-bsp ; `st-stm32wl55jci-nucleo` : A1 |
| `sys/user/tauon-basic/src/bin/` | 22 | 9 | conserver, sauf A3 | `net/html`, `cgi-bin/*.sh` lus par `tests/host` ; dhrystone, free, sdramtest, `tstcgi2.c`, `tstpost.c` : programmes de l'application (C-fonc) ; `lepton_mini.*` : A3 |

### 3.4 `sys/root/src/kernel/core/ucore/` (715 fichiers, 113 lus)
| Sous-répertoire | Fichiers | Lus | Classement des non-lus |
| --- | ---: | ---: | --- |
| `cmsis/` (CMSIS 2.10 ; `Device/st` dans les greffons famille F4/WL) | 159 | 9 | C-fonc, C-lic ; `CMSIS/Documentation/` + `index.htm` : A4 ; `system_stm32f4xx.c.old` : A5 |
| `cmsis-5/` | 368 | 76 | C-fonc (en-têtes et gabarits CMSIS 5 des autres cœurs), C-lic |
| `freeRTOS_11-3-0/` | 52 | 28 | C-fonc (portages des autres cœurs), C-lic |
| `freeRTOS_8-0-0/`, `freeRTOS_9-0-0/` | 136 | 0 | C-bsp : cités par les `user_kernel_mkconf.h` des BSP hors presets (samd20, samv71, f407, f469i, olimex) — règle « référence de code gelé ou hors presets » |

### 3.5 `sys/root/src/kernel/dev/`
| Sous-répertoire | Fichiers | Lus | Classement des non-lus |
| --- | ---: | ---: | --- |
| `arch/cortexm/{qemu-mps2,stm32f4xx,stm32wlxx}` (greffons famille) | 530 | 126 | C-fonc (HAL/SPL non utilisés par les cartes actuelles), C-lic |
| `arch/cortexm/stm32f7xx`, `samd21`, `host/*` | 208 | 28 | C-fonc |
| `arch/at91/*`, `arch/cortexm/{at91samd20,at91samv7x,stellaris,stm32f1xx}` | 799 | 0 | C-bsp, C-lic (familles différées) ; les fichiers de projet `stellaris/driverlib/{Makefile,driverlib.ewp,cr_project.xml}` restent avec leur famille |
| `arch/all/*`, `arch/cmsis/*` | 94 | 0 | C-fonc (pilotes génériques i2c, flash, lcd, ppp, usb, sd…) |
| `bsp/{qemu-mps2-an386,qemu-mps2-an500,nucleo-f429zi,nucleo-wl55jc1}` (greffons BSP) | 42 | 37 | conserver (C-lu, C-fonc) |
| `bsp/{samd21_xplained_pro,stm32f746g_disco}` | 5 | 5 | conserver |
| `bsp/{discovery_f4,discovery_f4-baseboard-modem,olimex_p407,samd20xplained_pro,same70xplained,samv71xplained_ultra,stm32f469i-eval}` | 49 | 0 | C-bsp |
| `dev_*` | 17 | 12 | C-fonc |

### 3.6 Reste de `sys/root/src/`
| Sous-répertoire | Fichiers | Lus | Classement des non-lus |
| --- | ---: | ---: | --- |
| `kernel/net/lwip` | 242 | 114 | C-fonc ; `prj/scons/SConscript` : **L1** |
| `kernel/net/uip`, `kernel/net/uip2.5` | 597 | 0 | C-fonc : pile alternative à lwIP, citée par `kernel/core/net/uip_core` |
| `kernel/fs/{fat,fatfs,yaffs}` | 84 | 4 | C-fonc (systèmes de fichiers non configurés) |
| `kernel/usb`, `kernel/core/usb` | 44 | 0 | C-fonc (pile USB STM32F4, signalée en ENV-6) |
| `kernel/core` (hors `ucore`, `usb`) | 202 | 164 | C-fonc |
| `lib` | 73 | 45 | C-fonc (`lib-nxpnfc` différé) |
| `bin` | 47 | 5 | C-fonc ; `bin/bin` : **L3** ; `bin/net/html/` : A3 |
| `sbin` | 46 | 13 | C-fonc ; `sbin/sh/*` (6 scripts lsh) : conserver, embarquables par une configuration |

## 4. Lots de suppression proposés

Tous dans le clone noyau (`original::tree`) ; un commit mécanique par lot (`git rm -r`), puis
`scion graft --scion lepton@original::tree` et les contrôles de la skill `lepton-rootstock`.

| Lot | Chemins (`scion/…`) | Fichiers | Octets |
| --- | --- | ---: | ---: |
| L1 | `tools/bin/`, `tools/config/`, `tools/host/`, `tools/mklepton/prj/`, `sys/user/build/`, `sys/root/src/kernel/net/lwip/prj/`, `tauon_make_link.bat` | 16 | 2 374 930 |
| L2 | `sys/user/tauon_sampleapp/` | 51 | 1 027 020 |
| L3 | `sys/user/tauon-basic/etc/memo.txt` (commandes `mklepton.exe` Windows, LM3S), `sys/user/tauon-basic/etc/readme.txt` (cite `mkconf_base.xml` AT91SAM9261, absent), `sys/root/src/bin/bin` (fichier factice CVS) | 3 | 697 |

Références vivantes de ces chemins : aucune hors des lots eux-mêmes. Restent des mentions dans
l'historique (`doc/migration/` du clone noyau, `rapports/`, `handoff/`), dans `DEVENV-STATUS.md`
et `etapes/ENV-14-nettoyage.md` (plan), et le commentaire de provenance de
`mkconf_tauon_basic_samd21_xplained_pro.xml` (l. 5) : il cite un fichier déjà retiré en ENV-4 ;
le modifier changerait un XML lu par un preset (sans effet sur l'image, commentaire), il est laissé.

## 5. À arbitrer

| ID | Chemins | Fichiers | Constat | Proposition |
| --- | --- | ---: | --- | --- |
| A0 | `sys/user/tauon_sampleapp/` (lot L2) | 51 | Cité dans la demande ; contient 17 fichiers propres à des cibles gelées (2 `src/dev/board_atmel_at91sam9261-ek`, 15 K60 : `hal/…`, `src/dev/board_freescale_twrk60n512`). La règle « code gelé conservé » vise le code d'architecture du noyau ; ici, une application non construite. | supprimer en entier |
| A1 | `sys/user/tauon-basic/src/arch/st-stm32wl55jci-nucleo/` | 1 | Configuration IAR de la WL55 (cite `freeRTOS_8-0-0`), remplacée par `include/user_kernel_mkconf.h` du BSP `nucleo-wl55jc1` dont le commentaire d'en-tête (l. 4-5) la cite comme origine ; signalée en ENV-6. | supprimer ; laisser le commentaire du BSP (provenance), sans toucher le greffon |
| A2 | `sys/user/tauon-basic/etc/.init_stm32_with_net`, `.init_with_net` | 2 | Scripts d'init génériques, aucune référence (le XML Olimex prend `.init_olimex_with_net`). | supprimer |
| A3 | `sys/root/src/bin/net/html/` (6), `sys/user/tauon-basic/src/bin/net/html/lepton_mini.{gif,png}` (2) | 8 | Pages dupliquées de tauon-basic ; seul `lhttpd.c` (non construit) cite « net/html ». `lepton_mini.*` : aucune référence. | supprimer |
| A4 | `sys/root/src/kernel/core/ucore/cmsis/CMSIS/Documentation/` (7), `cmsis/CMSIS/index.htm` | 8 | Documentation CMSIS 2.10 embarquée (413 Ko) ; la licence (`CMSIS END USER LICENCE AGREEMENT.pdf`) et `README.txt` sont conservés. | conserver (paquet tiers tel que livré) |
| A5 | `sys/root/src/kernel/core/ucore/cmsis/Device/st/stm32f4xx/system_stm32f4xx.c.old` | 1 | Copie `.old` dans le greffon **family-stm32f4xx** : la retirer ouvre une branche `devenv/env-14` dans ce greffon et un push de plus (PA-P). | supprimer, dans le greffon famille |

Hors classement (pour mémoire, non proposé) : 2 103 fichiers C-fonc, dont `kernel/net/uip`
+ `uip2.5` (597), `dev/arch/all` + `arch/cmsis` (94), `kernel/fs/{fat,fatfs,yaffs}` (84) — code fonctionnel du
système non configuré par les presets. Le retirer changerait les capacités de l'arbre, pas son
seul nettoyage : sujet d'une décision distincte, pas de cette étape.

## 6. `.DS_Store`

| Emplacement | Nombre | État |
| --- | ---: | --- |
| Trunk, fichiers réguliers | 26 | 23 relevés en ENV-13 + 3 nouveaux (`building/`, `building/staging/`, `sys/user/tauon_sampleapp/`) ; le fichier d'étape en annonçait 24 |
| Trunk, liens vers le clone noyau | 26 | `.DS_Store` ignorés du clone noyau, greffés par scion (racine, `sys/`, `sys/root/…`, `tools/…`) |
| Clone noyau | 30 | 26 sous `scion/` (les liens ci-dessus) + `./`, `.claude/`, `doc/`, `doc/migration/` ; ignorés par son `.gitignore` |
| 7 greffons famille/BSP | 0 | `.DS_Store` absent de leur `.gitignore` |
| Graine `original-tree` | 2 | `./`, `scion/` ; ignorés par `.git/info/exclude` (local), absent du `.gitignore` versionné |
| `depots/generation/` (aire `building`), `depots/origin/` | 3 + 2 | hors git |
| `~/lepton/`, `build/`, `third_party/` | 1 + 5 + 1 | hors arbre greffé |

`core.excludesfile` global (`~/.gitignore_global`) présent sur le Mac ; il ne protège pas un clone
fait sur un autre poste.

## 7. Questions du PA-15

1. Lots L1, L2, L3 : supprimer tels quels ?
2. A0 à A5 : propositions du §5 ?
3. Documents qui citent un chemin retiré : aucun document vivant ne le fait (§4). Confirmer la
   règle : rapports, passations et `doc/migration/` jamais réécrits ; commentaire de provenance du
   XML samd21 laissé.
4. `.gitignore` : ajouter `.DS_Store` au `.gitignore` des 7 greffons et de la graine (8 dépôts
   publiés, 8 branches, 8 push PA-P), ou s'en tenir au clone noyau (déjà fait) et à
   `~/.gitignore_global` ?
5. `.DS_Store` hors trunk : supprimer aussi ceux de `depots/generation/`, `depots/origin/`, de la
   racine du clone noyau et de la graine (hors git, sans effet sur le greffage) ?
