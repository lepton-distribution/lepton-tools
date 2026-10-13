# ENV-2 — Synthèse pour PA-2

Relevé du 2026-10-13. Détails et preuves dans `env-2-cmake.md`, `env-2-mklepton.md`,
`env-2-cartes.md`, `env-2-scion.md`, `env-2-outillage.md`.

## Constats transverses

1. **CMake minimum effectif 3.24**, pas 3.19 : `cmake_minimum_required(VERSION 3.24)`, presets v6,
   `$<LINK_GROUP:RESCAN>` (`env-2-cmake.md` §2).
2. **F429ZI** : le dépôt nomme tout `nucleo-f439zi` (presets, BSP, mkconf, OpenOCD), la puce est
   déclarée `STM32F429xx` et la carte validée est une F429ZI (`env-2-cartes.md` §0).
3. Démarrage et vecteurs sont **dans le noyau** (`kernel/core/arch/cortexm`, génériques Cortex-M),
   pas dans un BSP (écart avec la décision 4 et BLD-1).
4. Le BSP actuel (`lepton_bsp_<nom>`) mélange carte, couche famille (STM32F4, STM32WL) et HAL/SPL
   tiers ; les couches famille + tiers pèsent ~30 000 l. (F4) et ~74 000 l. (WL) contre < 1 000 l.
   propres à chaque carte.
5. Non-régression déjà outillée : `host.mklepton_empreintes`, `smoke.lsh`, banc KAL, `ci/run.sh`.

## ENV-4 — Format XML de mklepton

| | |
| --- | --- |
| Périmètre estimé | Analyseur expat conservé. Ajout `version` sur `<mklepton>`. Retrait : `<target>` comme sélecteur (seul `cortexm_lepton` sert), `<arch dest_path>`, `<cpu type>`, `cpufs block/option`, code `CPU_*`/`MK_DEV_*` M16C/ARM7, `_mk_rtc`. À trancher : `<arch include_absolute_path>` et `<cpu freq>` (propriétés de carte). 6 XML actifs à migrer ; 23 hérités à migrer ou supprimer. |
| Volume | `mklepton.c` 2 572 l. ; 6 XML actifs |
| Risques | Les sources `sbin`/`bin` sont aussi lues **par CMake** au moyen de regex sur le XML (`firmware.cmake:26-47`, `mklepton_check.cmake:77-86`) : tout changement de format doit y être répercuté. Retrait de `<target>` : modifie le filtrage `-t` et la signature de `lepton_generate`. Empreintes `.sha256` à régénérer si une sortie change. |

## ENV-5 — Restructuration CMake du greffon noyau

| | |
| --- | --- |
| Périmètre estimé | Passer de ~9 archives + `lepton_kernel` INTERFACE à `kernel`, `lib`, `sbin`, `bin`, `bsp` ; déplacer `kernel/dev/arch` du BSP vers `kernel` (BLD-1) ; `lepton_generated` → sources de l'exécutif ; démarrage/vecteurs → bibliothèque OBJECT ; ajouter HEX et rapport d'occupation (BLD-4) ; lecteur de manifestes. 15 presets existants (6 cartes) à garder construisibles. |
| Risques | Ordre de liaison : tout repose aujourd'hui sur `LINK_GROUP RESCAN` (dépendances croisées noyau ↔ BSP ↔ générés) ; symboles faibles (vecteurs F4 et `hal_tick` WL liés en sources pour cette raison). `kernel/dev/arch` contient les HAL/SPL tiers : les mettre dans `kernel` contredit l'extraction ENV-6. Sources `sbin`/`bin` dérivées du XML, pas de l'arborescence. Hors cartes retenues : an500, f746, samd21 (à garder ou à geler ?). |

## ENV-6 — Greffons BSP

| | |
| --- | --- |
| Périmètre estimé | Par carte : module `cmake/boards`, `ld/mem_*.ld`, `kernel/dev/bsp/<carte>/`, mkconf, `etc/<carte>/`, `user_kernel_mkconf.h`, cfg OpenOCD, gdbinit. Propre : an386 ~4 fichiers (~75 l.), F429 ~12 (~750 l.), WL55 ~16 (~1 250 l.). |
| À décider | Couches famille (`stm32f4xx`, `stm32wlxx`) et HAL/SPL : greffon famille, greffon BSP, ou noyau. BSP `qemu_mps2` partagé an386/an500. `gdbinit-nucleo-f439zi` commun de fait (sourcé par les autres). Nom `nucleo-f429zi` ou `nucleo-f439zi`. Démarrage générique Cortex-M : BSP (décision 4, dupliqué par carte) ou greffon commun. |
| Risques | scion n'a aucune priorité : un fichier présent à la fois dans le noyau et dans un BSP fait échouer la greffe → extraction et retrait du noyau dans un même mouvement (`env-2-scion.md` §3). |

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

Risque : le critère d'ENV-7 « `grep -ri lepton scion/` vide » **échoue déjà** (URL et auteur dans
`scion/__init__.py:4,6`) ; `INSTALL_LAYOUT` (`rootstock.py:23-29`) reflète le layout du seed Lepton.
ENV-7 peut suivre directement ENV-2 (ORCHESTRATION §6) ; ENV-6 bénéficierait d'ajout / retrait de
scion, mais l'édition manuelle suffit.

## Questions pour PA-2

1. Périmètres ENV-4 à ENV-7 ci-dessus : validés, ou à amender ?
2. Emplacement du code de carte (ENV-6) : couches famille et HAL/SPL dans le greffon BSP de chaque
   carte, dans un greffon famille, ou dans le noyau ?
3. Démarrage et vecteurs génériques Cortex-M : dans le BSP (décision 4) ou dans un emplacement commun ?
4. Nom de la carte F4 : `nucleo-f429zi` ou `nucleo-f439zi` ?
5. Cartes hors périmètre (an500, f746, samd21) : maintenues construisibles en ENV-5/6, ou gelées ?
6. CMake minimum : corriger `DEVENV-STATUS.md` à 3.24 ?
7. Critère « `grep -ri lepton` vide » d'ENV-7 : restreint au code fonctionnel (métadonnées exclues) ?
8. Ordre des étapes suivantes : ENV-3 ensuite, ou ENV-7 d'abord ?
