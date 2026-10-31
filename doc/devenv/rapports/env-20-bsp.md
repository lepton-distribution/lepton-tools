# ENV-20 — BSP `nucleo-f439zi` (PA-27)

Relevé du 2026-10-31, lecture seule. Clone noyau `master` 35b117b, `family-stm32f4xx` `master`
7694ad5, `bsp-nucleo-f429zi` `master` 8ea7ee5, graine `original-tree` f4ff07b, scion 0.5.2.0,
lepton 0.1.0. Chemins : `fam:` = `family-stm32f4xx/master/scion/sys/root/src/`, `bsp:` =
`bsp-nucleo-f429zi/master/scion/sys/root/src/kernel/dev/bsp/nucleo-f429zi/`, `noy:` =
`original/master/scion/`. Sources : fichiers des greffons uniquement (aucune valeur reprise de
mémoire). Aucune carte NUCLEO-F439ZI disponible (2026-10-31).

## 0. Préalable de session

Deux liens `.DS_Store` dans le trunk, venus de la source non git `depots/generation/building`
(fichiers du Finder, hors filtre E1 d'ENV-15). Décision de l'utilisateur : 4 `.DS_Store` de
`depots/generation/` supprimés, `scion graft --scion lepton@building` ; trunk : 0 `.DS_Store`,
0 fichier régulier, 0 lien cassé.

## 1. Constats

| # | Constat | Source | Conséquence |
| --- | --- | --- | --- |
| K1 | F429 et F439 : même table de 91 IRQ (16 + 91 = 107 entrées) ; seule différence, l'IRQ 79 : réservée (`0`) sur le F429, `CRYP_IRQHandler` sur le F439. `HASH_RNG_IRQHandler` (80) existe sur les deux. | `diff` des tables de `fam:kernel/core/ucore/cmsis/Device/st/stm32f4xx/startup/iar/startup_stm32f4{29,39}xx.s` (V2.3.0, `startup_stm32f439xx.s:169-170`) | Une seule table couvre les deux MCU (IRQ 79 vers un nom faible `CRYP_IRQHandler`, sans effet sur le F429). |
| K2 | `stm32f429xx.h` de la famille (`driverlib/`, V2.3.0) : `DCMI_IRQn = 78`, `HASH_RNG_IRQn = 80`, pas de `CRYP_IRQn`. | `fam:kernel/dev/arch/cortexm/stm32f4xx/driverlib/stm32f429xx.h:174-176` | Conforme à K1. |
| K3 | **Aucun `stm32f439xx.h`** dans le greffon famille (ni `driverlib/`, ni `cubemx_hal_driver/inc/`, ni `ucore/cmsis/Device/st/stm32f4xx/`), ni ailleurs dans `<ROOTSTOCK>`, `third_party` ou `~/lepton-tools-dev`. `driverlib/stm32f4xx.h:148-149` inclut `"stm32f439xx.h"` (sans chemin) si `STM32F439xx` est défini : la compilation échouerait. | `find … -iname 'stm32f439*'` (vide) ; `driverlib/stm32f4xx.h:146-149` | Définir `STM32F439xx` exige d'importer un en-tête ST (source externe à désigner). La migration avait retenu `STM32F429xx` « faute d'en-tête F439 » (`noy:../tools/migration/dep_graph.py:138-153`). Question Q3. |
| K4 | `driverlib/stm32f4xx_gpio.h:333` : `#if !defined(STM32F429xx)` évite un doublon avec `stm32f4xx_hal_gpio_ex.h:68` (`STM32F429xx \|\| STM32F439xx`). Avec `STM32F439xx`, les définitions GPIO AF seraient en double. | lignes citées | Option Q3-b : retouche de cette condition aussi. |
| K5 | Pilotes compilés de la famille (`gpio.c`, `uart.c`, `eth.c`, `dev_stm32f4xx_{uart_x,eth}.c`, SPL `misc`, `rcc`, `gpio`, `usart`, `dma`, `syscfg`, `stm32f4x7_eth`) : aucune condition sur le device. CRYP et HASH (SPL `stm32f4xx_cryp*.c`, `stm32f4xx_hash*.c`) présents mais non compilés. | `lepton-greffon.json:8-21` de la famille | Aucun périphérique propre au F439 n'est utilisé : un binaire F439 a le même code qu'un binaire F429. |
| K6 | Démarrage générique : table des 16 exceptions + IRQ 0-63 sous les noms `IRQ<n>_Handler` faibles (alias `Default_Handler`) ; section `.isr_vector`. La famille prolonge par `.isr_vector_ext` (IRQ 64-90), contiguë (`common-cortexm.ld:12-19`). | `noy:sys/root/src/kernel/core/arch/cortexm/startup_armv7m.c:27,45-85` | La table complète se fait dans la famille sans toucher au démarrage générique (commun à 7 BSP). |
| K7 | Table actuelle de la famille : relais forts `IRQ12/39/57/61_Handler` → `DMA1_Stream1_IRQHandler`, `USART3_IRQHandler`, `DMA2_Stream1_IRQHandler`, `ETH_IRQHandler` ; table étendue : 27 entrées `Default_Handler` sauf l'IRQ 71 → `USART6_IRQHandler`. | `fam:kernel/dev/arch/cortexm/stm32f4xx/vecteurs/stm32f429xx_vectors.c:23-38` | Base de la table complète. |
| K8 | Définitions des 5 gestionnaires : 4 dans le BSP (`bsp:nucleo_f439zi_board.c:127-130`, `demarrage`, lié en OBJECT) ; `ETH_IRQHandler` dans `dev_stm32f4xx/dev_stm32f4xx_eth.c:101` (archive `libkernel.a`), membre tiré par `dev_stm32f4xx_eth_map` (table des périphériques mklepton, `lepton.map`). | `nm`, `lepton.map` de `build/nucleo-f429zi-embos` | Un nom CMSIS **faible** défini dans un objet n'entraîne plus l'extraction du membre d'archive qui le définit fort. Sans risque aujourd'hui (membre tiré par ailleurs) ; contrôle `nm` obligatoire après modification (chaque gestionnaire utilisé reste `T` à sa définition forte). |
| K9 | Le lecteur CMake lie **tous** les fichiers `vecteurs` de la famille pour toute carte de la famille, sans sélection par MCU. | `noy:cmake/lepton_greffons.cmake:355-358` | Deux tables (F429, F439) dans la famille = symboles en double. Une table par MCU sélectionnée par le `mcu` du BSP demanderait de modifier le lecteur commun (contraire à BLD-6). Question Q1. |
| K10 | Optimisation des cibles Cortex-M : `-Os` (Debug compris), surchargeable. | `noy:cmake/toolchains/arm-none-eabi.cmake:12-15` | Estimation de l'audit (saut `b.w`, ≈ +240 octets) **corrigée à la mise en œuvre** : l'appel d'un nom faible n'est pas remplacé par un saut, chaque relais fait `push/bl/pop` (8 octets) ; mesuré : `.text` +496 (embOS) et +512 octets (FreeRTOS), §6. |
| K11 | BSP `nucleo-f429zi` : 8 fichiers suivis (`CMakeLists.txt`, `debug/{gdbinit,openocd}-nucleo-f439zi*`, `include/user_kernel_mkconf.h`, `ld/mem_nucleo-f439zi.ld`, `lepton-greffon.json`, `nucleo_f439zi.h`, `nucleo_f439zi_board.c`), tous UTF-8. Mentions de la destination `kernel/dev/bsp/nucleo-f429zi` : manifeste, `user_kernel_mkconf.h:28` (`#include`), `gdbinit:3-4` (commentaires). Mentions « nucleo-f429zi » hors chemin : `CMakeLists.txt:1-2`, `user_kernel_mkconf.h:2`, `gdbinit:1` (commentaires). | `git ls-files`, `grep` | Copie par `scion new --from` : chemins remplacés (S3-1), commentaires « nucleo-f429zi » / « NUCLEO-F429ZI » à retoucher à la main. |
| K12 | `lepton scion new NAME --type bsp --from BSP` : copie les fichiers suivis du BSP greffé (S3-2), remplace la destination comme chemin entier dans les fichiers texte (S3-1), écrit le manifeste depuis `templates/bsp/` (version `0.1.0`, description « BSP NAME, dérivé de SRC. »), `git init -b master` et commit initial. `--repo DIR` fixe l'emplacement (défaut `depots/lepton-bsp/NAME`). Sur `<ROOTSTOCK>` (graine de référence), refus sans `--no-seed` (PA-23). | `lepton/scions.py:112-160`, `lepton/cli.py:200-210` | `--no-seed --repo <ROOTSTOCK>/depots/lepton/bsp-nucleo-f439zi/master` crée le dépôt directement à la convention d'ENV-13 : aucun déplacement. Question Q2. |
| K13 | Mémoire : `ld/mem_nucleo-f439zi.ld` déclare déjà le STM32F439ZI (flash 2 Mo, SRAM 192 Ko, CCM 64 Ko) ; OpenOCD : `board/st_nucleo_f4.cfg` (cible `stm32f4x`, commune F42x/F43x) ; horloges (`nucleo_f439zi.h:16-22`) : PLL 168 MHz, communes. | lignes citées | Fichiers repris tels quels. |
| K14 | XML `noy:sys/user/tauon-basic/etc/mkconf_tauon_basic_nucleo_f439zi.xml` : périphériques `dev_nucleo_f439zi_{board,uart_3,uart_6}_map` (identifiants C du BSP, conservés par la copie), `.boot`/`.init` de `etc/nucleo-f439zi/`. L'en-tête de configuration noyau vient du manifeste (`entete_config_noyau`), pas du XML. | `xml:40-44,77-78` | Le même XML sert aux deux BSP ; `mklepton_empreintes.sh` ajoutera les sorties `mkconf_tauon_basic_nucleo_f439zi-nucleo-f439zi/*`, identiques à celles de `-nucleo-f429zi` hors une ligne de `kernel_mkconf.h` (chemin de l'en-tête de carte, K9 d'ENV-19). |
| K15 | Presets F429 : `nucleo-f429zi-embos` (`LEPTON_BOARD`, `LEPTON_MKCONF` du XML F439) et `nucleo-f429zi-freertos` (hérite). CI : `ci/run.sh:86` `board_machines="nucleo-f429zi stm32f746g-disco samd21-xplained-pro nucleo-wl55jc1"`. `doc/BUILDING.md:15` (table des cartes), `:148-187` (commandes F429). | `noy:CMakePresets.json:85-100` | Presets `nucleo-f439zi-*` sur le même modèle. CI : question Q6. |
| K16 | Compatibilité d'un binaire `nucleo-f439zi` sur NUCLEO-F429ZI : même cœur, même carte NUCLEO-144, même mémoire, même table hors IRQ 79 (jamais levée sur le F429 : CRYP absent), aucun pilote CRYP/HASH compilé (K5). Avec Q3-a, code identique au binaire F429 hors noms. | K1, K5, K13 | Essai sur NUCLEO-F429ZI techniquement possible ; écriture flash soumise à autorisation (type PA-11). Ne prouve pas le démarrage sur un F439 (piège de l'étape). |

## 2. Forme proposée de la table de vecteurs (famille)

Un seul fichier pour le F429 et le F439 (K1, K9), dans la famille (PA-2 Q3), au même nom
`vecteurs/stm32f429xx_vectors.c` (manifeste inchangé ; commentaire d'en-tête « F429/F439 ») :

- 91 noms CMSIS déclarés faibles, alias de `Default_Handler`
  (`void WWDG_IRQHandler(void) __attribute__((weak, alias("Default_Handler")));` …, noms de
  `startup_stm32f439xx.s`) ; `CRYP_IRQHandler` pour l'IRQ 79 (réservée sur le F429) ;
- IRQ 0-63 : un relais fort par IRQ, `void IRQ<n>_Handler(void) { <nom CMSIS>(); }` (64 relais,
  dont les 4 actuels) — forme imposée par la table générique (K6), qui n'est pas modifiée ;
- IRQ 64-90 : table `.isr_vector_ext` qui référence directement les noms CMSIS (sans relais) ;
- un BSP fournit un gestionnaire en définissant le nom CMSIS en fort, sans toucher à la famille.

Effet sur `nucleo-f429zi-*` (seul écart admis) : symboles ajoutés (91 noms CMSIS `W`, 60 relais
`IRQ<n>_Handler` passés de `W` à `T`), table `.isr_vector` modifiée, `.text` ≈ +240 octets (K10) ;
les 5 gestionnaires utilisés restent `T` à leur définition forte (contrôle `nm`, K8). Démonstration
en deux temps (méthode d'ENV-4) : nouvelle référence F429 après la table seule, puis ajout du BSP.

## 3. BLD-6 (constat attendu)

Ajout du BSP sans modification du système de construction commun : lecteur
`lepton_greffons.cmake`, `kernel.cmake`, `cpu/`, `kal/`, `isa/`, démarrage générique inchangés.
Modifications du clone noyau envisagées : 2 presets, `doc/BUILDING.md`, référence
`tests/host/mklepton_empreintes.sha256`, et `ci/run.sh` selon Q6.

## 4. Questions pour PA-27

| Q | Sujet | Proposition |
| --- | --- | --- |
| Q1 | Forme et emplacement de la table complète (K1, K6-K10) | §2 : une table F429/F439 dans la famille, noms CMSIS faibles, relais 0-63, extension 64-90 directe, nom de fichier inchangé ; pas de sélection par MCU (BLD-6). |
| Q2 | Création du BSP (K11, K12) | `lepton scion new nucleo-f439zi --type bsp --from nucleo-f429zi --no-seed --repo <ROOTSTOCK>/depots/lepton/bsp-nucleo-f439zi/master` (commit initial sur `master`, aucun déplacement) ; puis `devenv/env-20` : manifeste (`version` 1.0.0, description, `mcu` `STM32F439ZI`), commentaires « F429 » de `CMakeLists.txt`, `user_kernel_mkconf.h`, `gdbinit` ; `origin` `https://github.com/lepton-distribution/lepton-bsp-nucleo-f439zi.git`, pushurl SSH. Noms de fichiers `nucleo_f439zi_*` et identifiants C conservés. |
| Q3 | Définition de la puce (K3-K5) | **a** (proposée) : `STM32F429xx` conservé dans le BSP F439, comme la migration ; manifeste `mcu` `STM32F439ZI` ; famille inchangée hors table ; écart documenté (CRYP/HASH non décrits par l'en-tête, aucun pilote ne les utilise). **b** : importer `stm32f439xx.h` (source ST à désigner par l'utilisateur, version alignée sur V2.3.0) dans `driverlib/`, chemin complet dans `stm32f4xx.h:149`, condition `stm32f4xx_gpio.h:333` étendue, `mcu` de la famille `["STM32F429xx", "STM32F439xx"]`, BSP en `STM32F439xx`. |
| Q4 | XML et presets (K14, K15) | Même XML `mkconf_tauon_basic_nucleo_f439zi.xml` ; presets `nucleo-f439zi-embos` (`LEPTON_MKCONF` posé) et `nucleo-f439zi-freertos` (hérite) ; référence des empreintes mklepton étendue (écart démontré : une ligne de `kernel_mkconf.h`). |
| Q5 | Fichiers propres au F439 | Avec Q3-a : aucun fichier propre ; le BSP diffère du F429 par le manifeste et les commentaires. Avec Q3-b : `stm32f439xx.h` dans la famille. |
| Q6 | CI (`ci/run.sh:86`) | Ajouter `nucleo-f439zi` à `board_machines` (construction seule). |
| Q7 | Essais sur NUCLEO-F429ZI (K16) | Si la carte est branchée : flash, fumée et banc KAL de `nucleo-f429zi-*` après la table (nouvelle référence), et du binaire `nucleo-f439zi-embos` ; écriture flash à autoriser (cœur M4, octets d'option intouchés). Sinon : construction et symboles seulement. Le rapport dira que rien ne prouve le démarrage sur un F439. |
| Q8 | Graine `original-tree` | Entrée `bsp-nucleo-f439zi` (version `master`) dans `.scion.sources.list` et `.scion.ramifications` ; regreffe sur une copie d'essai puis `<ROOTSTOCK>` (séquence PA-13, `seed-clone` sans clonage car `.git` présent, K11 d'ENV-19). |

## 5. Réponses du PA-27 (2026-10-31, utilisateur)

Q1 : table unique F429/F439, nom de fichier conservé (§2). Q3 : option a (`STM32F429xx` dans le
BSP F439 ; `mcu` `STM32F439ZI`). Q5 : en conséquence, aucun fichier propre au F439. Q2, Q4, Q6,
Q8 : validées telles que rédigées. Q7 : NUCLEO-F429ZI disponible, écriture flash autorisée (cœur
M4, octets d'option non touchés) : flash, fumée et banc KAL de `nucleo-f429zi-*` après la table,
puis du binaire `nucleo-f439zi-embos`.

## 6. Mise en œuvre (2026-10-31)

Aucun dépôt GitHub créé, rien poussé (PA-28).

| Dépôt | Branche | Commits |
| --- | --- | --- |
| `depots/lepton/family-stm32f4xx/master` | `devenv/env-20` depuis `master` 7694ad5 | 2fb7cfe table de vecteurs complète (§2 ; tableau d'alias faibles vers un relais local `stm32f4xx_irq_default` → `Default_Handler`, un alias exigeant une cible de la même unité ; table étendue renommée `stm32f4xx_vector_table_ext`) |
| `depots/lepton/bsp-nucleo-f439zi/master` (nouveau) | `master` 18135b0 (commit de `lepton scion new`) ; `devenv/env-20` | 7119dfd manifeste (version 1.0.0, `mcu` `STM32F439ZI`, description), commentaires F439 de `CMakeLists.txt`, `user_kernel_mkconf.h`, `gdbinit`, `openocd` ; `origin` `https://github.com/lepton-distribution/lepton-bsp-nucleo-f439zi.git`, pushurl SSH |
| clone noyau | `devenv/env-20` depuis `master` 35b117b | cb7020d presets `nucleo-f439zi-{embos,freertos}` (configure, build, test) et `ci/run.sh:86` ; 2b78e3b `doc/BUILDING.md` (table des cartes, paragraphe NUCLEO-F439ZI en §4) ; f571d02 référence `tests/host/mklepton_empreintes.sha256` |
| graine `original-tree` | `devenv/env-20` depuis f4ff07b | d2adddf : `bsp-nucleo-f439zi` dans `.scion.sources.list` et `.scion.ramifications` |

Commande de création : `lepton scion new nucleo-f439zi --type bsp --from nucleo-f429zi --no-seed
--repo <ROOTSTOCK>/depots/lepton/bsp-nucleo-f439zi/master` (code 0 ; 8 fichiers, destination
remplacée dans le manifeste, `user_kernel_mkconf.h:28` et `gdbinit:3-4`). Manifeste validé par
`check-jsonschema` (`schemas/greffon.schema.json`).

Premier temps (table seule, oracle `env-20-lot-table`, construction à neuf sur `<ROOTSTOCK>`) :
`comparer-oracle` contre `env-20-avant` sur `nucleo-f429zi-{embos,freertos}` : code 1, écarts
classés mécaniquement (script de classement sur la liste des noms de `startup_stm32f439xx.s`) :
86 noms CMSIS ajoutés (`W`, les 5 autres étaient déjà définis forts), 64 relais `IRQ<n>_Handler`
modifiés (`W` de 4 octets → `T` de 8), `nucleo_f439zi_vector_table_ext` retiré,
`stm32f4xx_vector_table_ext` et `stm32f4xx_irq_default` ajoutés ; **0 symbole hors de la table**.
Sections : `.text` +496 (embOS) / +512 (FreeRTOS), `.isr_vector` inchangée, sections `.debug_*`.
Gestionnaires utilisés : `USART3`, `USART6`, `DMA1_Stream1`, `DMA2_Stream1`, `ETH_IRQHandler` restent
`T` (K8 : `ETH_IRQHandler` toujours tiré de `libkernel.a`).

Second temps (BSP, copie d'essai `~/lepton-tools-dev/essais/env-20`, `cp -RP depots trunk`,
`third_party` lié) : `scion seed-clone --seed depots/lepton-seed.scions/original-tree` (aucun
clonage, `.git` présent) puis `scion graft --scion lepton@bsp-nucleo-f439zi` : 8 feuilles,
3941 liens (3933 avant), 0 cassé, 0 fichier régulier, 14 greffons. Oracle `env-20-lot-bsp`
(dans la copie, même longueur de chemin pour les deux BSP) : `comparer-oracle`
`nucleo-f429zi-<b>` → `nucleo-f439zi-<b>` : **0 écart de sections ou de symboles** (embOS et
FreeRTOS). `host.mklepton_empreintes` en échec avant la nouvelle référence (6 sorties
`…-nucleo-f439zi/*` absentes) : 5 identiques à l'octet à celles de `…-nucleo-f429zi`,
`kernel_mkconf.h` diffère par la seule ligne 15 (`#include` de
`sys/root/src/kernel/dev/bsp/nucleo-f4{2,3}9zi/include/user_kernel_mkconf.h`) ; nouvelle référence
(50 fichiers) : test vert. `lepton check` sur la copie : code 0, 19 fichiers conformes.
Même `seed-clone` et `graft` sur `<ROOTSTOCK>` : arborescence du trunk identique à la copie.

## 7. Contrôles (PA-28)

Oracle après `rapports/oracles/env-20-apres/` sur `<ROOTSTOCK>` (construction à neuf, `host`
d'abord ; `rejouer-oracle.sh` avec les 14 presets d'`env-20-avant` et les 2 presets
`nucleo-f439zi-*`) : « tout a réussi ».

| Preset | Sections/symboles | Empreinte | Fumée | Banc KAL | Écarts expliqués |
| --- | --- | --- | --- | --- | --- |
| `host` | — | — | — | `ctest` 7/7 | mklepton : E-3 |
| `qemu-mps2-an386-{embos,freertos}` | identiques à `env-20-avant` | diffère (date) | identique | 18/18, même liste | E-4 |
| `qemu-mps2-an386-{embos,freertos}-soft` | identiques | diffère (date) | identique | 14/14, même liste | E-4 |
| `qemu-mps2-an500-{embos,freertos}` | identiques | diffère (date) | identique | 18/18, même liste | E-4 |
| `nucleo-f429zi-{embos,freertos}` | identiques à `env-20-lot-table` ; écart à `env-20-avant` limité à la table (E-1) | diffère | carte : `cortexM4-stm32f4` | carte : 19/19 (×2) | E-1 |
| `nucleo-f439zi-{embos,freertos}` | identiques à `nucleo-f429zi-*` (E-2) | diffère | carte F429 : `cortexM4-stm32f4` (embOS) | carte F429 : 19/19 (embOS) | E-2, E-5 |
| `stm32f746g-disco-*`, `samd21-xplained-pro-*`, `nucleo-wl55jc1-*` (×2 chacun) | identiques à `env-20-avant` | diffère (date) | — | — | — |

Écarts :
- **E-1** Table de vecteurs (§6, premier temps) : 86 noms CMSIS `W` ajoutés, 64 relais `W` → `T`,
  table étendue renommée, `stm32f4xx_irq_default` ; 0 symbole hors table ; `.text` +496 / +512.
- **E-2** `nucleo-f439zi-*` = `nucleo-f429zi-*` aux sections et symboles près (Q3-a : même
  définition de puce, mêmes identifiants C) ; seuls changent le manifeste et les chemins.
- **E-3** mklepton : 50 sorties (44 avant) ; les 6 nouvelles `…-nucleo-f439zi/*` : 5 identiques à
  `…-nucleo-f429zi/*`, `kernel_mkconf.h` diffère par la ligne 15 (chemin de l'en-tête de carte) ;
  nouvelle référence f571d02 ; `host.mklepton_empreintes` vert.
- **E-4** Fumée QEMU : seuls diffèrent la date de compilation (ligne de version et `uname`), le
  jeton aléatoire de `echo lepton-uart1-<n>` et la position du message asynchrone `rcv SIGCHLD`
  (an500, an386 soft) ; ignorés.
- **E-5** Aucune NUCLEO-F439ZI : le binaire `nucleo-f439zi-embos` a été essayé sur la
  NUCLEO-F429ZI (ST-LINK/V2-1 `0672FF495252717267243842`, seule sonde branchée, console
  `/dev/cu.usbmodem145103`), 19/19 (fumée, `kal.board_flash`, 17 cas). **Rien ne prouve le
  démarrage sur un STM32F439** ; l'essai montre que le binaire est correct sur un F429, conforme
  à K16.

Carte (PA-27 Q7, 2026-10-31) : `ctest --preset <P> -L board` avec
`-DLEPTON_BOARD_SERIAL_PORT=/dev/cu.usbmodem145103` ; journaux `env-20-apres/<P>/carte.log`,
`carte-detail.log`, `fumee-carte.log`. Fin : image `nucleo-f429zi-embos` remise en flash
(`program … verify reset exit`, `adapter serial` explicite) : « Verified OK ».

lepton : `check` code 0 sur `<ROOTSTOCK>` (19 fichiers conformes, 18 avant) ; `generate` code 0
sur la copie `essais/env-20` et sur `<ROOTSTOCK>` : 16 lancements (14 avant), dont
`Déboguer nucleo-f439zi-{embos,freertos} (carte, OpenOCD)`. Trunk : 3941 feuilles, 0 fichier
régulier, 0 lien cassé, 14 greffons. Aucun code de lepton modifié.

BLD-6 : clone noyau modifié dans `scion/CMakePresets.json` (2 presets), `ci/run.sh` (1 ligne),
`doc/BUILDING.md`, `scion/tests/host/mklepton_empreintes.sha256` ; famille : le seul fichier de
vecteurs ; graine : 2 lignes. Lecteur `lepton_greffons.cmake`, `kernel.cmake`, `cpu/`, `kal/`,
`isa/`, démarrage générique, script de liens commun : inchangés. **Le BSP s'ajoute sans
modification du système de construction commun.**

Critères de l'étape : table F4 complète, écart F429 démontré et limité à la table (E-1) ; BSP
`nucleo-f439zi` inscrit dans `original-tree` (branche `devenv/env-20`), **non publié** (PA-28) ;
2 presets construits ; BLD-6 constaté.
