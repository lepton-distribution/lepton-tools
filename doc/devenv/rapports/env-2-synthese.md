# ENV-2 — Synthèse pour PA-2

Relevé du 2026-10-13 (révisé après lecture intégrale de la documentation du portage). Détails et
preuves dans `env-2-cmake.md`, `env-2-mklepton.md`, `env-2-cartes.md`, `env-2-scion.md`,
`env-2-outillage.md`, `env-2-doc-portage.md`.

## Constats transverses

1. **CMake minimum effectif 3.24**, pas 3.19 : `cmake_minimum_required(VERSION 3.24)`, presets v6,
   `$<LINK_GROUP:RESCAN>` — choix documenté du portage (`ETAPE-2-build-cmake.md:20`).
2. **F439 / F429** : la décision du portage (MS:110, 2026-10-01) garde la F439ZI comme carte de base
   nominale et **conserve les noms `nucleo-f439zi`** ; la F429ZI n'est qu'une remplaçante, puce
   déclarée `STM32F429xx`. Le chantier ENV nomme la carte « NUCLEO-F429ZI » : renommer est une
   décision à acter.
3. **Démarrage** : le portage a décidé « un démarrage par famille (`kernel/core/arch/<famille>/startup_<isa>.c`),
   une table de vecteurs par MCU » ; la décision 4 de la spécification place démarrage et vecteurs
   dans le BSP. Seule la F4 a une table propre (`*_vectors.c`, IRQ 64-90).
4. **Symboles faibles** : les remplaçants forts (vecteurs F4, `HAL_GetTick`/`HAL_Delay` WL) sont liés
   comme objets de l'exécutable, sinon l'archive n'est pas tirée. La bibliothèque OBJECT d'ENV-5 doit
   couvrir les deux cas.
5. **Cycle de liaison** noyau ↔ libc ↔ vfs ↔ fs ↔ dev (376 symboles) traité par `LINK_GROUP RESCAN`,
   « pas de fusion » : séparer `kernel` et `lib` (BLD-1) ne supprime pas le cycle.
6. Le BSP actuel (`lepton_bsp_<nom>`) mélange carte, couche famille (STM32F4, STM32WL) et HAL/SPL
   tiers ; famille + tiers ≈ 30 000 l. (F4) et ≈ 74 000 l. (WL) contre < 1 000 l. propres à chaque carte.
   La configuration d'une carte est en outre répartie en trois lieux (`cmake/boards`+`ld`+BSP ;
   `tauon-basic/etc/` ; `tauon-basic/src/arch/<carte>/`), plus `debug/`, et 12 directives
   `__tauon_cpu_device__` restent dans le noyau.
7. Le portage maintient **6 cartes** (an386, an500, F439/F429, F746, SAMD21, WL55), validées ; le
   chantier n'en vise que 3.
8. Non-régression outillée : `host.mklepton_empreintes` (38 sorties de référence `-m32`, **jamais
   régénérées** ; changement d'un octet = point d'arrêt), `smoke.lsh`, banc KAL, `ci/run.sh`.

## ENV-4 — Format XML de mklepton

| | |
| --- | --- |
| Périmètre estimé | Analyseur expat conservé. Ajout `version` sur `<mklepton>`. Retrait : `<target>` comme sélecteur (seul `cortexm_lepton` sert), `<arch dest_path>`, `<cpu type>` **avec** l'énumération `CPU_*` (dont `CPU_TYPE_M16C62`, conservé en portage pour ne pas décaler l'énumération), `cpufs block/option`, `MK_DEV_*` M16C, `_mk_rtc`. À trancher : `<arch include_absolute_path>` et `<cpu freq>` (propriétés de carte). 6 XML actifs à migrer (dont Olimex, support des empreintes) ; 23 hérités à migrer ou supprimer. Défauts connus à corriger ou non (`mklepton.md:21-25`). |
| Risques | Sources `sbin`/`bin` et dépendances lues **par CMake** au moyen de regex sur le XML (`firmware.cmake:26-47`, `cmake/mklepton.cmake:40-44`, `mklepton_check.cmake:77-86`) ; `mklepton_empreintes.sh:43` relit `cmake/boards/*.cmake` par `sed`. Si une sortie change d'un octet : nouvelle référence d'empreintes à décider (PA). Retrait de `<target>` : `LEPTON_BOARD_MKCONF_TARGET`, `-t`, empreintes. |

## ENV-5 — Restructuration CMake du greffon noyau

| | |
| --- | --- |
| Périmètre estimé | ~9 archives + INTERFACE `lepton_kernel` → `kernel`, `lib`, `sbin`, `bin`, `bsp` ; `kernel/dev/arch` vers `kernel` (BLD-1) ; `lepton_generated` → sources de l'exécutif ; démarrage / vecteurs / remplaçants forts → OBJECT ; HEX et occupation par bibliothèque (BLD-4) ; lecteur de manifestes. |
| Risques | Groupe RESCAN indispensable tant que le cycle existe ; ordre de liaison → octets des `.bin` (fusion de littéraux) : l'oracle tolère des empreintes différentes mais pas un comportement différent. `kernel/dev/arch` contient les HAL/SPL tiers : les mettre dans `kernel` contredit l'extraction ENV-6. Tests compilés hors `lepton_options` à reprendre. `perimetre.csv` à rejouer. 15 presets à garder construisibles (ou moins, selon Q5). |

## ENV-6 — Greffons BSP

| | |
| --- | --- |
| Périmètre estimé | Par carte : module `cmake/boards`, `ld/mem_*.ld`, `kernel/dev/bsp/<carte>/`, mkconf, `etc/<carte>/`, `src/arch/<carte>/user_kernel_mkconf.h`, cfg OpenOCD, gdbinit. Propre : an386 ~4 fichiers (~75 l.), F429 ~12 (~750 l.), WL55 ~16 (~1 250 l.). Base du manifeste : `doc/migration/ajout-coeur.md:65-104`. |
| À décider | Couches famille et HAL/SPL ; BSP `qemu_mps2` partagé an386/an500 ; `gdbinit-nucleo-f439zi` commun de fait ; nom F429/F439 ; directives `__tauon_cpu_device__` du noyau. |
| Risques | scion sans priorité : un fichier présent dans le noyau et dans un BSP fait échouer la greffe → extraction et retrait dans le même mouvement. `.gitignore` hérité ignore `debug/`, `bin/`, `*.bin`, `*.a`. |

## ENV-7 — Évolutions de scion

| Besoin | 0.5.0.1 | Évolution candidate |
| --- | --- | --- |
| Ajout / retrait d'un scion | non (édition manuelle de 2 fichiers du seed + `grafted.list`) | commande dédiée |
| Regreffe d'un chemin | non (`graft` reconstruit tout, ~4 000 liens) | `graft <chemin>` |
| Greffon local hors git | oui (version `*`) | – |
| Regreffe idempotente | oui | – (fichier régulier ou `.DS_Store` dans le trunk bloque) |
| Suppression d'un greffon | non | commande dédiée |
| `scion git` | sortie jetée | correction |
| Conflit fichier / répertoire | trace Python, sans annulation | correction |

Le critère d'ENV-7 « `grep -ri lepton scion/` vide » échoue déjà (URL et auteur,
`scion/__init__.py:4,6`) ; `INSTALL_LAYOUT` (`rootstock.py:23-29`) reflète le layout du seed Lepton.

## Questions pour PA-2

1. Périmètres ENV-4 à ENV-7 ci-dessus : validés, ou à amender ?
2. Couches famille (`stm32f4xx`, `stm32wlxx`) et HAL/SPL : greffon BSP de chaque carte, greffon famille,
   ou noyau ?
3. Démarrage et vecteurs : décision 4 (BSP) ou règle du portage (démarrage par famille dans le noyau,
   table de vecteurs par MCU dans le BSP) ?
4. Carte F4 : renommer en `nucleo-f429zi` (écart à la décision MS:110 du portage) ou conserver
   `nucleo-f439zi` ?
5. an500, F746, SAMD21 (maintenues et validées par le portage) : construisibles en ENV-5/6 avec un
   BSP transitoire, ou gelées ?
6. CMake minimum du chantier : corriger `DEVENV-STATUS.md` à 3.24 ?
7. Critère « `grep -ri lepton` vide » d'ENV-7 : restreint au code fonctionnel (métadonnées exclues) ?
8. Ordre des étapes suivantes : ENV-3 ensuite, ou ENV-7 d'abord ?

## Périmètres validés (PA-2, 2026-10-13)

Décisions Q1 à Q8 consignées dans `DEVENV-STATUS.md` §Décisions.

- **ENV-4** : attribut `version` ; expat conservé. Retrait de `<target>` comme sélecteur, de
  `<arch dest_path>`, de `<cpu type>` avec l'énumération `CPU_*` (dont `CPU_TYPE_M16C62`), de
  `cpufs block/option` et du code M16C (`MK_DEV_*`, `_mk_rtc`). `<cpu freq>` et
  `<arch include_absolute_path>` (propriétés de carte) : à trancher en PA-4. Migration des 6 XML actifs ;
  sort des 23 hérités en PA-4. Toute sortie modifiée d'un octet : nouvelle référence d'empreintes
  décidée explicitement.
- **ENV-5** : bibliothèques `kernel`, `lib`, `sbin`, `bin`, `bsp` ; `LINK_GROUP RESCAN` conservé tant
  que le cycle existe ; bibliothèque OBJECT pour démarrage générique (greffon noyau), vecteurs par MCU
  et remplaçants forts de la HAL ; sources générées dans l'exécutif ; HEX et occupation par
  bibliothèque ; 15 presets construisibles. Code des familles provisoirement dans `kernel/dev/arch`
  (extraction en ENV-6).
- **ENV-6** : greffons famille (`stm32f4xx`, `stm32wlxx`, `qemu-mps2`) avec couche Lepton, pilotes ST
  et table de vecteurs ; BSP réduits à l'horloge (`SystemInit`) et aux GPIO : `qemu-mps2-an386`,
  `nucleo-f429zi`, `nucleo-f439zi`, `nucleo-wl55jc1`. an500, F746, SAMD21 construisibles (greffons en
  ENV-6 ou transitoires : PA-7). Place de `ld/mem`, mkconf, `user_kernel_mkconf.h`, cfg OpenOCD : PA-7.
- **ENV-7** : ajout / retrait / suppression de greffon, regreffe d'un chemin, sortie de `scion git`,
  conflit fichier / répertoire ; critère NF-2 limité au code fonctionnel ; `INSTALL_LAYOUT` en PA-8.
