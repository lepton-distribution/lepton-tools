# Étape ENV-19 — Extraction des cartes STM32F746G-DISCO et SAMD21 Xplained Pro

## Contexte
Les cartes STM32F746G-DISCO (Cortex-M7, famille STM32F7) et SAMD21 Xplained Pro (Cortex-M0+,
famille SAMD21) sont restées « transitoires » dans le greffon noyau depuis ENV-6 (PA-7 Q9) :
`scion/cmake/boards/stm32f746g-disco.cmake` et `samd21-xplained-pro.cmake`, repli du lecteur
CMake (règle R6 de `rapports/env-6-extraction.md`), 4 presets (`stm32f746g-disco-{embos,freertos}`,
`samd21-xplained-pro-{embos,freertos}`). Décision de l'utilisateur (2026-10-31) : les extraire en
greffons famille et BSP, comme les cartes d'ENV-6. Migration iso-fonctionnelle : mêmes symboles,
mêmes images mklepton ; l'oracle fait foi.

## Prérequis
- ENV-14 terminée ; ENV-17 conseillée avant (documentation du noyau à jour).
- Règles d'extraction R1-R9 et décisions PA-7 (Q1-Q12) : `rapports/env-6-extraction.md`,
  `DEVENV-STATUS.md` §Décisions.
- Convention des greffons publiés (ENV-13) : clés `family-<nom>`, `bsp-<nom>` ; clones
  `<ROOTSTOCK>/depots/lepton/<clé>/master` ; dépôts `https://github.com/lepton-distribution/lepton-famille-<nom>.git`
  et `lepton-bsp-<nom>.git`, pushurl SSH.
- Branches `devenv/env-19` : lepton-tools, clone noyau, graine `depots/lepton-seed.scions/original-tree`,
  et chaque nouveau dépôt de greffon.

## Tâches

### 1. Audit (lecture seule) → PA-25
- Fichiers lus par les 4 constructions : `ninja -C <build> -t deps` / `-t inputs` (méthode
  d'ENV-6), à partir des builds de l'oracle.
- Point de départ, à vérifier fichier par fichier : F746 (`kernel/dev/bsp/stm32f746g_disco`,
  `kernel/dev/arch/cortexm/stm32f7xx`, `kernel/core/ucore/cmsis-5/Device/ST/STM32F7xx`,
  `ld/mem_stm32f746g-disco.ld`, `debug/openocd-stm32f746g-disco.cfg`, gdbinit de carte) ; SAMD21
  (`kernel/dev/bsp/samd21_xplained_pro`, `kernel/dev/arch/cortexm/samd21`,
  `kernel/core/ucore/cmsis-5/Device/Microchip/SAMD21`, `ld/mem_samd21-xplained-pro.ld`,
  `debug/openocd-samd21-xplained-pro.cfg`).
- Paramètres propres à reporter dans les manifestes ou le `CMakeLists.txt` du BSP : variante embOS
  `_837070`, port FreeRTOS `ARM_CM7/r0p1`, `LEPTON_M7_FPU=sp`, pile lwIP (F746) ;
  `LEPTON_FREERTOS_CONFIG` (SAMD21) ; définitions et inclusions de `lepton_options`.
- Partages à trancher : fichier aussi lu par une autre carte ou un code gelé (`cmsis-5`,
  `at91samd20`) → reste dans le noyau.
- Rapport `doc/devenv/rapports/env-19-extraction.md`, sur le modèle d'`env-6-extraction.md`.
- **PA-25** : l'utilisateur valide :
  - la liste d'extraction par greffon ;
  - les noms des 4 greffons et des dépôts : <À CONFIRMER au PA-25 : `family-stm32f7xx`,
    `bsp-stm32f746g-disco`, `family-samd21`, `bsp-samd21-xplained-pro`> ; les dépôts GitHub sont
    créés par l'utilisateur ou par `gh` sur son accord ;
  - le sort du repli `cmake/boards` du lecteur CMake une fois les deux cartes extraites (retiré
    ou conservé pour de futures cartes transitoires) ;
  - la disponibilité des cartes pour un essai de flash et de fumée : <À CONFIRMER au PA-25 ;
    à défaut, construction et symboles seulement, comme en ENV-6>.
- Aucune modification avant la réponse.

### 2. Oracle avant
Skill `lepton-oracle`, arguments d'ENV-14 (14 presets, host compris) →
`rapports/oracles/env-19-avant/`.

### 3. Extraction, un lot par carte (F746, puis SAMD21)
- Nouveaux dépôts sous `<ROOTSTOCK>/depots/lepton/<clé>/master` : import à l'identique (un
  commit), puis manifeste `lepton-greffon.json` (schéma `schemas/greffon.schema.json`, `lepton check`).
- Clone noyau : retrait des fichiers extraits et de `cmake/boards/<carte>.cmake` (commits
  mécaniques) ; presets inchangés.
- Graine : 2 entrées par carte dans `.scion.sources.list` (URL `https://`).
- Regreffe selon la séquence éprouvée du PA-13 (`DEVENV-STATUS.md` §Décisions), d'abord sur une
  copie d'essai du rootstock (skill `lepton-rootstock`), puis sur `<ROOTSTOCK>`.
- Après chaque lot : oracle partiel des 2 presets de la carte, `comparer-oracle.py`.

### 4. Contrôles → PA-26
- Oracle après (`env-19-apres/`) ; `comparer-oracle.py` sur les 14 presets : symboles identiques,
  écarts de sections expliqués (chemins DWARF, comme en ENV-6), empreintes mklepton identiques ;
  fumée et banc KAL QEMU identiques.
- `lepton check` sur `<ROOTSTOCK>` : code 0 ; l'information « BSP non greffé » d'ENV-16 disparaît
  pour ces 4 presets (test de lepton adapté).
- Rapport `doc/devenv/rapports/env-19-extraction.md` complété.
- **PA-26** : push des nouveaux dépôts et des branches `devenv/env-19` ; fusion dans `master` /
  `original-tree` / `main` avant ou après la validation Debian d'ENV-21 : <À ARBITRER au PA-26>.

## Critères de validation
- [ ] PA-25 et PA-26 tranchés et consignés.
- [ ] `cmake/boards/` du noyau sans F746 ni SAMD21 ; 4 greffons publiés, inscrits dans `original-tree`.
- [ ] Symboles identiques sur 14 presets ; empreintes mklepton identiques ; trunk : 0 fichier régulier, 0 lien cassé.
- [ ] Ajout des cartes sans modification du système de construction commun (BLD-6) : constat dans le rapport.

## Pièges connus
- `kernel/dev/bsp/<nom du greffon>` (PA-7 Q12) change le chemin du BSP : les sections DWARF
  diffèrent, les symboles non. Un symbole différent signale une erreur d'extraction.
- Un fichier partagé avec du code gelé (ARM7, ARM9, M16C) ou un BSP hors presets reste dans le
  noyau (ENV-14).
- Les fichiers ignorés par git ne sont plus greffés depuis scion 0.5.2.0 (E1) : vérifier le
  `.gitignore` des nouveaux dépôts.
- ENV-20 modifie aussi la graine `original-tree` : fusionner ENV-19 avant de commencer ENV-20.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, branches, emplacements (nouveaux greffons), décisions PA-25 et PA-26,
journal. Passation `handoff/env-19.md`.
