# ENV-46 — Famille STM32F4 : retrait de la SPL

Session du 2026-11-10, hôte Mac. Fichier d'étape : `etapes/ENV-46-retrait-spl-f4.md`.
Relevés bruts : `env-46-spl/audit/`.

## 1. Audit (lecture seule)

### 1.1 Méthode

Recherche sur le trunk de `<ROOTSTOCK>` (3983 liens), en suivant les liens :
`LC_ALL=C grep -RIa`, car plusieurs fichiers de la famille sont en ISO-8859 et un `grep` en UTF-8
les saute sans le signaler. Chaque fichier trouvé est rattaché à son greffon par la cible de son
lien (`references-par-fichier.tsv`).

Motifs recherchés :
- `driverlib`, avec `/` et `\` comme séparateurs ;
- `stm32f4x7_eth` ;
- `Device/st/stm32f4xx` (CMSIS V3.x, casse exacte) ;
- `stm32f4xx/eth.[ch]`, `dev_stm32f4xx_eth.[ch]` ;
- `stm32f4xx_<périph>.h` pour les 25 en-têtes de la SPL ;
- `USART_ChangeBaudrate` ;
- et, à part, les inclusions sans chemin de `stm32f4xx.h`, `misc.h`, `stm32f4NNxx.h`,
  `system_stm32f4xx.h`, `stm32f4xx_conf.h` (`inclusions-sans-chemin.txt`).

Les fichiers non compilés de la famille sont classés de deux façons :
- par leurs `#include` ;
- par les appels à l'API de la SPL (`RCC_*PeriphClockCmd`, `GPIO_Init`, `SPI_I2S_*`, `ETH_*`,
  `FLASH_*`, `USART_*`, `DMA_*`, `NVIC_Init`, `EXTI_Init`, …).

### 1.2 Fichiers candidats de la famille `family-stm32f4xx` (7afd7f1)

| Lot | Fichiers | Nombre | Dépend de la SPL | Utilisé par un preset |
| --- | --- | --- | --- | --- |
| a. SPL | `kernel/dev/arch/cortexm/stm32f4xx/driverlib/` | 68 | — (c'est la SPL) | non |
| b. Ethernet sur la SPL | `eth.c`, `eth.h`, `dev_stm32f4xx/dev_stm32f4xx_eth.c`, `stm32f4x7_eth_conf.h` | 4 | oui : `eth.c` inclut `driverlib/stm32f4x7_eth.h` (30 appels `ETH_*`, `RCC_*`) ; `eth.h` et `dev_stm32f4xx_eth.c` incluent `driverlib/stm32f4xx.h` et `stm32f4x7_eth.h` ; `stm32f4x7_eth_conf.h` est la configuration de `driverlib/stm32f4x7_eth.h`, qui l'inclut par son chemin | non |
| c. SPI sur la SPL | `spi.c`, `spi.h`, `dev_stm32f4xx/dev_stm32f4xx_spi_x.c`, `dev_stm32f4xx/dev_stm32f4xx_spi_x.h` | 4 | oui : `spi.c` (l. 30) et `dev_stm32f4xx_spi_x.c` (l. 46) incluent `driverlib/stm32f4xx.h`, `spi.c` appelle `SPI_Init`, `SPI_I2S_*` ; les deux `.h` ne servent qu'à eux et aux BSP hors plan du §1.3 | non |
| d. CMSIS device V3.x F4 | `kernel/core/ucore/cmsis/Device/st/stm32f4xx/` : `stm32f4xx.h`, `system_stm32f4xx.{c,h}`, `Release_Notes.html`, `startup/iar/` (13), `startup/keil/` (3) | 20 | oui : son `stm32f4xx.h` inclut `stm32f4xx_conf.h` sous `USE_STDPERIPH_DRIVER` (l. 6963), un fichier de la SPL | non ; aucune référence par chemin dans tout le trunk |

Total des quatre lots : 96 fichiers.

Fichiers non compilés de la famille **qui ne dépendent pas de la SPL** : ils incluent
`stm32f4xx_hal.h` et n'appellent aucune fonction de la SPL. Ce sont `dev_stm32f4xx_cpu_x.c`,
`dev_stm32f4xx_cubemx_eth.c`, `dev_stm32f4xx_dac_x.{c,h}`, `dev_stm32f4xx_flash.{c,h}`,
`dev_stm32f4xx_i2c_x.{c,h}`, `dev_stm32f4xx_sdio.{c,h}`, `dev_stm32f4xx_sdio-1.16.{c,h}`,
`flash_if.{c,h}`. Ils restent hors du retrait.

`gpio.c` et `uart.c` sont compilés et ne citent la SPL qu'en commentaire, ainsi que
`dev_stm32f4xx_eth_x.c` et `vecteurs/stm32f429xx_vectors.c`. Le commentaire des vecteurs
(l. 16-18) cite deux fichiers des lots b et d : `startup/iar/startup_stm32f439xx.s`, source des noms,
et `dev_stm32f4xx_eth.c`, qui tirait `ETH_IRQHandler` jusqu'à ENV-35.

### 1.3 Dépendants hors de la famille (clone noyau, hors plan A3)

Ils sont tous dans le clone noyau `original/master`. Aucun autre greffon n'est concerné : BSP
`nucleo-f429zi`, `nucleo-f439zi`, familles et BSP F7, WL, SAMD21, QEMU, graine.

| Dépendant | Fichiers | Référence | Déjà cassé depuis ENV-35 |
| --- | --- | --- | --- |
| BSP `discovery_f4-baseboard-modem` | 13 (`dev_discovery_f4_board{,-old}.c`, `*_uart_3/6.c`, `*_spi_1/2.c`, `*_oled_io.c`, `*_click_420{,r}_io.c`, `*_nfc_pn7150.c`, `dev_aedr8300_encoder_1/2.c`, `dev_rotary_encoder_x.c`) | `driverlib/stm32f4xx.h` ; `spi.h`, `dev_stm32f4xx_spi_x.h` | 5 fichiers : ils incluent aussi `driverlib/stm32f4xx_hal_gpio_ex.h`, retiré en ENV-35 (020db7b) |
| BSP `discovery_f4` | 2 (`dev_discovery_f4_board.c`, `dev_discovery_f4_uart_6.c`) | `driverlib/stm32f4xx.h` ; `spi.h`, `dev_stm32f4xx_spi_x.h` | non |
| BSP `olimex_p407` | 3 (`dev_olimex_p407_board.c`, `*_uart_3.c`, `*_spi_3.c`) | `driverlib/stm32f4xx.h` ; `spi.h`, `dev_stm32f4xx_spi_x.h`, `eth.h` | non |
| BSP `stm32f469i-eval` | 4 (`dev_stm32f469i_eval_board.c`, `*_usart_1.c`, `*_spi_1/2.c`) | `driverlib/stm32f4xx.h` ; `spi.h`, `dev_stm32f4xx_spi_x.h` | 1 fichier (`*_board.c`, `stm32f4xx_hal_gpio_ex.h`) |
| `ucore/freeRTOS_8-0-0` et `freeRTOS_9-0-0`, `source/arch/cortex-m4/stm32f4/` | 2 × 3 (`main.c`, `stm32f4xx_conf.h`, `stm32f4xx_it.h`) | `main.c:149` `kernel\dev\arch\cortexm\stm32f4xx\driverlib\misc.h` (barres inverses) ; `stm32f4xx_conf.h` : 25 en-têtes de la SPL sans chemin | non |
| XML `sys/user/tauon-basic/etc/mkconf_tauon_basic_lwip_stm32f4-olimex-p407.xml` | 1 | `dev_stm32f4xx_eth_map` (l. 68), défini dans la famille par le seul `dev_stm32f4xx_eth.c` (lot b) ; les deux BSP NUCLEO le définissent eux-mêmes depuis ENV-35 | non |

Les fichiers dont les références visent les lots b et c incluent tous déjà `driverlib/` : retirer
ces lots en plus de la SPL ne casse aucun fichier de plus. Seul le XML Olimex est touché par le lot
b uniquement, et le BSP Olimex qu'il désigne inclut déjà `driverlib/`.

Ne dépendent pas de la SPL :
- `kernel/usb/stm32f4-usb-core/core/` : `usb_device.h`, `usbd_conf.{c,h}` incluent `stm32f4xx.h`
  sans chemin, et le seul `stm32f4xx.h` sur un chemin d'inclusion de la famille est celui du CMSIS
  projeté ; ils incluent aussi `stm32f4xx_hal.h`. Ils dépendent de la HAL (A3), pas de la SPL.
- `stellaris/driverlib`, `cmsis/Device/lm3s`, `stm32f1xx` (`misc.h` de la SPL F1) : sans rapport.

### 1.4 Ce que les objets compilent réellement

La construction utilise Ninja : les `.d` sont absorbés dans `.ninja_deps` et supprimés. On les lit
par `ninja -C <build> -t deps` (relevé `dependances-objets.tsv`).

Résultats sur host et les 16 presets :
- une entrée par objet de `compile_commands.json`, toutes `VALID`, aucune `STALE` ;
- aucune dépendance vers `driverlib/`, `stm32f4x7_eth*`, `cmsis/Device/st/stm32f4xx/`,
  `stm32f4xx/{eth,spi}.*`, `dev_stm32f4xx_{eth,spi_x}.*` ;
- aucun drapeau `-I` vers `driverlib` ni vers le CMSIS V3.x dans les 17 `compile_commands.json` ;
- presets F4 (`nucleo-f429zi-*`, `nucleo-f439zi-*`) : `stm32f4xx.h`, `stm32f429xx.h`,
  `stm32f439xx.h` et `system_stm32f4xx.h` sont tous résolus vers
  `kernel/core/ucore/cmsis-5/Device/ST/STM32F4xx/Include/` (CMSIS projeté). Les autres presets
  n'incluent aucun `stm32f4xx.h`.

`ninja -n` ne prévoit que les deux étapes systématiques (« Re-checking globbed directories »,
« Re-running CMake ») : les relevés correspondent au trunk actuel.

### 1.5 `USART_ChangeBaudrate`

Ajout de Lepton à la SPL V1.0.2, dans `driverlib/stm32f4xx_usart.c` l. 1470-1516 (commit noyau
fbc16fb, « added ioctl command for change stm32f4 uart baudrate »). Elle calcule `BRR` à partir de
`RCC_GetClocksFreq`, avec une partie entière et une partie fractionnaire au centième, pour un
sur-échantillonnage de 8 ou de 16.

Aucun appel dans le trunk. Le calcul est déjà reproduit à l'identique, par registres, dans `uart.c`
(`uart_apb_clock` et `uart_set_brr`, appelés par `uart_set_baudrate`), depuis ENV-35 (commentaire
l. 64-66).

### 1.6 Documents qui citent la SPL

| Document | Greffon / dépôt | Mention | Nature |
| --- | --- | --- | --- |
| `lepton-greffon.json`, champ `description` | famille | « La SPL ST (driverlib), eth.c et dev_stm32f4xx_eth.c restent dans l'arbre, non compilés (ENV-35). » | vivant |
| `vecteurs/stm32f429xx_vectors.c` l. 16-18 (commentaire) | famille | `startup/iar/startup_stm32f439xx.s`, `dev_stm32f4xx_eth.c` | vivant, fichier compilé |
| `schemas/exemples/greffon-famille-stm32f4xx.json` | lepton-tools | `"driverlib/src"`, « SPL ST », `USE_STDPERIPH_DRIVER` | exemple d'ENV-3, validé par `scripts/valider-schemas.sh` |
| `schemas/greffon.schema.json` l. 305 | lepton-tools | exemple d'inclusion `…/stm32f4xx/driverlib` | vivant |
| `doc/migration/*.md`, `doc/migration/traces/*`, `tools/migration/*.py` (dont `mass_compile.py`, `-I…/driverlib`) | clone noyau | chantier IAR → GCC | historique |
| `LEPTON-PROVENANCE.md` (×2), `BUILDING.md`, skills, `README.md` | — | aucune mention | — |
| `HORS-PLAN.md` A3, B3 ; `DEVENV-STATUS.md` ; fichiers d'étape | lepton-tools | suivi du chantier | à mettre à jour en fin d'étape |

### 1.7 Historique

| Dépôt | Commits qui touchent la SPL |
| --- | --- |
| clone noyau | 7 commits, de 037cd59 (« initial commit. new original tree depot ») à 55d4c5f (« added stm32f469 definitions »), dont fbc16fb (`USART_ChangeBaudrate`) |
| `family-stm32f4xx` | 3ef8e46 (import d'ENV-6), af964c6 (ENV-14, `system_stm32f4xx.c.old`), 020db7b (ENV-35, 4 fragments HAL) |

La famille et le noyau sont publiés : `git rm` laisse cet historique entier et atteignable depuis
`master`.

### 1.8 PA-79 — décisions de l'utilisateur (2026-11-10)

| Question | Décision |
| --- | --- |
| Périmètre | Lots a, b, c et d : 96 fichiers. Les fichiers non compilés sur la HAL restent. |
| Dépendants hors plan | Laissés en l'état, avec des inclusions cassées. Ils sont inventoriés au §1.3 et dans `HORS-PLAN.md` A3, qui reste hors plan. Le clone noyau ne change que pour la note de migration. |
| `USART_ChangeBaudrate` | Perdue avec la SPL. Son calcul existe déjà dans `uart.c` (`uart_set_brr`), et l'historique git la garde. |
| Historique | Tag annoté `avant-retrait-spl` sur `family-stm32f4xx` `master` 7afd7f1, poussé au PA-80. |
| Documents | Corrigés : `description` du manifeste ; commentaire des vecteurs, l. 15-18, à nombre de lignes constant ; `schemas/greffon.schema.json` l. 305 ; `schemas/exemples/greffon-famille-stm32f4xx.json`. Dans le clone noyau, une note datée en fin de `doc/migration/MIGRATION-STATUS.md`, sans rien réécrire : la documentation de migration est arrêtée au 2026-10-06 (`ETAPE-8` §4). |

## 2. Oracle avant

`oracles/env-46-avant/` est produit par `env-46-spl/oracle-complet.sh`. Le script relève d'abord
les chemins du trunk, puis lance `oracle-16.sh`, qui est `rejouer-oracle.sh` aux arguments d'ENV-41
(6 presets QEMU, 10 de carte, constructions à neuf), et enfin `ctest -N` sur chaque preset. La
comparaison à la référence `oracles/env-45-apres/` se fait par `env-46-spl/comparer.sh`
(`comparaisons/`) :
- les 16 presets sont à code 0 ;
- bancs KAL (19/15/19/15/18/18) et fumée identiques. Seuls éléments ignorés, ceux de
  `comparer-journaux.py` repris d'ENV-44 : date de compilation, jeton `lepton-uart1-<n>`,
  `rcv SIGCHLD`, lignes vides ;
- mklepton identiques ; host 7/7 ;
- `ctest -N` 17/17 identiques.

Trunk (`oracles/env-46-avant/trunk/`) :
- 3983 liens, 0 lien cassé, aucun fichier régulier hors `.scion.grafted.list` ;
- `chemins.txt` : SHA-256 `54b0c9a7…` ;
- `chemins-cibles.txt` : SHA-256 `4d58553b…`.

## 3. Retrait

| Dépôt | Branche | Commit | Contenu |
| --- | --- | --- | --- |
| `family-stm32f4xx` | tag annoté `avant-retrait-spl` sur `master` 7afd7f1 | — | état d'avant le retrait (PA-79) |
| `family-stm32f4xx` | `devenv/env-46` (depuis `master` 7afd7f1) | 0ffae44 | commit mécanique : `git rm -r` des 96 fichiers des lots a à d (`env-46-spl/rootstock/chemins-retires.txt`). Ensuite, le répertoire `scion/sys/root/src/kernel/core/ucore/cmsis/`, qui ne contenait plus que des `.DS_Store` ignorés, est supprimé du disque. |
| `family-stm32f4xx` | `devenv/env-46` | 3503e42 | `description` du manifeste ; commentaire de `vecteurs/stm32f429xx_vectors.c` l. 15-18, à nombre de lignes constant |
| clone noyau | `devenv/env-46` (depuis `master` 6a56d4c) | 44e3e9c | `doc/migration/MIGRATION-STATUS.md` : une ligne datée du 2026-11-10 ajoutée en fin du tableau « Décisions actées », rien de réécrit. Ce fichier est hors du trunk. |
| lepton-tools | `devenv/env-46` (depuis `main` 8ab7bb1) | 8683faa | `schemas/greffon.schema.json` l. 305 : exemple `…/hal_driver/Inc` ; `schemas/exemples/greffon-famille-stm32f4xx.json` : « HAL ST », `hal_driver/Src/stm32f4xx_hal_gpio.c`, `USE_HAL_DRIVER`. `scripts/valider-schemas.sh` : conforme. |

Les dépendants hors plan ne sont pas touchés (§1.3) ; la projection, `hal_driver/` et le CMSIS
projeté non plus.

Regreffe de `<ROOTSTOCK>`, accord PA-P : `scion graft --scion lepton@family-stm32f4xx`. Résultat
(`env-46-spl/rootstock/graft.log`) : code 0, 239 feuilles. Les deux clés projetées sont regreffées
avec leur porteur. 11 chemins ignorés par git ne sont pas greffés : ce sont les `.DS_Store` de la
famille.

## 4. Contrôles → PA-80

### 4.1 Trunk de `<ROOTSTOCK>`

Relevés : `env-46-spl/rootstock/`, `oracles/env-46-apres/trunk/`.

| Contrôle | Résultat |
| --- | --- |
| liens | 3887, soit 3983 − 96 ; SHA-256 de `chemins.txt` `c65ee399…`, de `chemins-cibles.txt` `6cd0c0d4…` |
| chemins disparus | 96, égaux octet pour octet aux 96 chemins retirés (`chemins-retires.txt`), donc à la casse près (le volume du Mac ne la distingue pas) |
| chemins apparus | 0 ; cibles des 3887 chemins restants inchangées |
| liens cassés, fichiers réguliers | 0, 0 (hors `.scion.grafted.list`) ; aucun répertoire `driverlib/` ni `ucore/cmsis/Device/st/stm32f4xx/` dans le trunk |
| clone noyau | propre (`git status`) |
| `lepton check` | code 0, 19 fichiers conformes (`rootstock/check.log`) |

### 4.2 Oracle après

`oracles/env-46-apres/` est produit par les mêmes commandes que l'avant (`oracle-complet.sh`). La
comparaison à `oracles/env-46-avant/` se fait par `comparer.sh` (`comparaisons/`) :

| Preset | Sections/symboles | Empreinte | Fumée | Banc KAL | Écarts expliqués |
| --- | --- | --- | --- | --- | --- |
| 6 presets QEMU | code 0 | différente (date) | identique | identique (19/15/19/15/18/18) | — |
| 10 presets de carte, dont les 4 F4 | code 0 | différente (date) | — | — | — |
| `host` | mklepton identiques | | | ctest 7/7 | — |

- `ctest -N` : 17/17 identiques.
- Le commentaire des vecteurs, modifié à nombre de lignes constant, ne change aucune section ni
  aucun symbole.
- `ninja -t deps` après le retrait : aucune dépendance de la SPL dans les 17 constructions, et les
  F4 résolvent toujours `stm32f4xx.h` vers le CMSIS projeté (`audit/dependances-objets-apres.tsv`).
  Les nombres d'objets diffèrent de ceux du §1.4 pour les presets de carte : les répertoires lus
  en §1.4 étaient ceux des bancs d'ENV-45, configurés avec un port série et donc avec
  `kal_bench` ; l'oracle configure sans port.

Binaires identiques : critère atteint.

### 4.3 Rootstock neuf `~/lepton-tools-dev/essais/env-46-vierge`

Graine d'essai locale `~/lepton-tools-dev/essais/env-46-vierge-graine` : clone d'`original-tree`,
branche `devenv/env-46` 5284338, jamais publiée. `family-stm32f4xx` y est déclarée en
`devenv/env-46`, par `file://localhost/Users/cle_d_anton/lepton/depots/lepton/family-stm32f4xx/master`.

Installation (`env-46-spl/vierge/installation.log`) : `scion rootstock-install`,
`seed-add --version devenv/env-46`, puis `graft`, tous trois à code 0, 3887 feuilles.

Contrôles (`vierge/controles.log`, `vierge/check.log`) :
- 3887 liens, avec le même SHA-256 que `<ROOTSTOCK>` (`c65ee399…`) ;
- contenu identique à `<ROOTSTOCK>` chemin par chemin (0 écart) ;
- 0 lien cassé, 0 fichier régulier ;
- clones tiers aux commits épinglés (b6f0ed3, 3c77349), origine = miroirs, sans modification ;
- famille : `devenv/env-46` 3503e42 ;
- `lepton check` : code 0.

### 4.4 Carte NUCLEO-F429ZI (PA-11)

Le banc passe par `env-46-spl/bancs.sh`, c'est-à-dire `env-45-sonde/banc-sonde.sh`, avec :
- sonde 0672FF495252717267243842, choisie par `LEPTON_BOARD_PROBE_SERIAL` ;
- console `/dev/cu.usbmodem1454403`, relevée par `ioreg` ;
- hôte réseau 192.168.2.10.

Les WL55 A et B sont restées branchées, sans être touchées.

| Preset | Image = oracle après | Flash | Tests | Comparaison à ENV-45 |
| --- | --- | --- | --- | --- |
| `nucleo-f429zi-embos` | code 0, `.hex` identique | « Verified OK » | 20/20 : fumée, réseau, banc KAL | liste et résultats identiques ; journal réseau identique (heures et dates ignorées) |
| `nucleo-f429zi-freertos` | code 0, `.hex` identique | « Verified OK » | 20/20 | idem |

Journaux : `oracles/env-46-apres/nucleo-f429zi-*/carte*.log`, `fumee-carte.log`,
`reseau-carte.log`.

### 4.5 lepton-tools

- `scripts/valider-schemas.sh` : conforme.
- pytest : 362 réussis.
