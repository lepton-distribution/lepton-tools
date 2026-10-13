# ENV-6 — Validation (non-régression des extractions)

## Commandes

Oracle : `scripts/oracle/rejouer-oracle.sh` (lepton-tools), constructions neuves. Le script attend un
drapeau par preset ; la forme à accolades de `env-5-validation.md` (`--qemu a b c`) est refusée
(« argument inconnu ») : la liste est construite ainsi.

```
args=()
for p in qemu-mps2-an386-{embos,embos-soft,freertos,freertos-soft} qemu-mps2-an500-{embos,freertos}; do args+=(--qemu $p); done
for p in nucleo-f439zi-{embos,freertos} nucleo-wl55jc1-{embos,freertos} stm32f746g-disco-{embos,freertos} samd21-xplained-pro-{embos,freertos}; do args+=(--carte $p); done
scripts/oracle/rejouer-oracle.sh ~/lepton doc/devenv/rapports/oracles/env-6-<avant|lot-…> "${args[@]}"
```

## Oracle avant (`oracles/env-6-avant/`, clone noyau 1551afb = fusion de e564714)

Comparaison avec `oracles/env-5-apres/` (même code) : `comparer-oracle.py` code 0 sur les 14 presets
(sections et symboles identiques) ; host : ctest 7/7, empreintes mklepton identiques à la référence.

| Preset | Sections/symboles | Empreinte | Fumée | Banc KAL | Écarts expliqués |
| --- | --- | --- | --- | --- | --- |
| qemu-mps2-an386-embos | code 0 | différente | identique | 18/18, même liste | date |
| qemu-mps2-an386-embos-soft | code 0 | différente | identique | 14/14, même liste | date |
| qemu-mps2-an386-freertos | code 0 | différente | identique | 18/18, même liste | date |
| qemu-mps2-an386-freertos-soft | code 0 | différente | identique | 14/14, même liste | date |
| qemu-mps2-an500-embos | code 0 | différente | identique | 18/18, même liste | date |
| qemu-mps2-an500-freertos | code 0 | différente | identique | 18/18, même liste | date |
| nucleo-f439zi-embos, -freertos | code 0 | différente | – | – | date |
| nucleo-wl55jc1-embos, -freertos | code 0 | différente | – | – | date |
| stm32f746g-disco-embos, -freertos | code 0 | différente | – | – | date |
| samd21-xplained-pro-embos, -freertos | code 0 | différente | – | – | date |

Écarts ignorés dans les journaux de fumée : date de compilation (`__DATE__`/`__TIME__` de
`kernel.c`), jeton aléatoire du test UART1 (`lepton-uart1-<n>`), position du message asynchrone
`rcv SIGCHLD` (avant ou après l'invite suivante). Banc KAL : lignes de résultat identiques, durées
ignorées.

## Lot QEMU (session 1)

### Réalisation

| Dépôt | Branche | Commits |
| --- | --- | --- |
| clone noyau | `devenv/env-6` | fa03c8e lecteur famille/BSP, carte par manifeste, `LEPTON_MKCONF`, OBJECT `bsp_demarrage` ; 1fe7ac0 retrait des fichiers déplacés (mécanique) ; 7942413 modules `cmake/boards/qemu-*` retirés, presets, tests hôte ; cd53527 nouvelle référence d'empreintes mklepton |
| `depots/lepton-famille/qemu-mps2` | `devenv/env-6` (sur `master` vide) | 7b03f7c import à l'identique depuis fa03c8e (mécanique) ; 0927646 manifeste |
| `depots/lepton-bsp/qemu-mps2-an386` | idem | 56e3cfe import ; d979c6e manifeste, `CMakeLists.txt`, deux `#include` et l'en-tête de commentaire de `qemu_mps2_board.c` (nombre de lignes inchangé) |
| `depots/lepton-bsp/qemu-mps2-an500` | idem | 3d7f73d import ; eb52230 idem an386 |
| graine `depots/lepton-seed.scions/original-tree` | `devenv/env-6` | f6f4805 trois lignes `*` dans `.scion.sources.list` et `.scion.ramifications` |
| lepton-tools | `devenv/env-6` | 1831232 schéma : `inclusions`, fichier dans `sources`, portée publique famille/BSP ; exemple invalide `greffon-inclusion-absolue.json` |

Inscription : `scion seed-clone --seed depots/lepton-seed.scions/original-tree` (aucun fetch ni pull,
versions `*`), puis `scion graft` : 4 032 feuilles (4 027 − 12 retirées + 17 ajoutées) ; aucun fichier
régulier ni lien cassé dans le trunk. Manifestes valides (`check-jsonschema` 0.38.2,
`schemas/greffon.schema.json`) ; `scripts/valider-schemas.sh` conforme (45 contrôles).

Construction : `greffons : qemu-mps2;qemu-mps2-an386;qemu-mps2-an500;lepton-noyau`,
`carte qemu-mps2-an386 : famille qemu-mps2, cœur cortex-m4f` ; pilotes de la famille dans `kernel` ;
`qemu_mps2_board.c` dans l'OBJECT `bsp_demarrage`, lié à `lepton` et à `kal_bench` (le banc KAL
recevait ce fichier par l'archive `bsp`, qu'il ne lie pas comme objet) ; plus de bibliothèque `bsp`
pour QEMU (aucune autre source de carte).

### Empreintes mklepton (PA-7 Q5)

Référence `tests/host/mklepton_empreintes.sha256` renouvelée : sorties QEMU rangées par carte
(`mkconf_tauon_basic_qemu_mps2-qemu-mps2-{an386,an500}/`) ; `.fsflash.o`, `bin_mkconf.c`,
`dev_dskimg.{c,h}`, `dev_mkconf.c` identiques à l'ancienne référence ; `kernel_mkconf.h` : seule la
ligne 15 change (`#include` de l'en-tête de carte, nouveau chemin dans le BSP). Contre-épreuve : le
même mklepton avec l'ancien chemin d'en-tête redonne l'empreinte d'origine `1e9fecf8…`. Les en-têtes
`user_kernel_mkconf.h` d'an386 et an500 sont identiques (`cmp`).

### Recherche des restes dans le noyau

`git ls-files` et `git grep -i 'mps2|an386|an500|cmsdk|lan9118'` (clone noyau, hors `*.md`) :
- restent, par décision : presets QEMU (`CMakePresets.json`, graine en ENV-8), XML
  `mkconf_tauon_basic_qemu_mps2.xml` et `etc/qemu-mps2/{.boot,.init}` (Q4), test `host.mklepton_format`
  (en-tête du BSP an386), référence d'empreintes ;
- code générique qui nomme la carte, signalé et non inversé : `kernel/core/kernelconf.h:68,126`
  (identifiant `__tauon_cpu_device_cortexM4_qemu_mps2_an386__` et nom `uname` associé ; an500 pose
  `__KERNEL_CPU_DEVICE_NAME` par son manifeste) ;
- commentaires seulement : `cmake/cpu/*.cmake`, `cmake/isa/armv7m.cmake`,
  `cmake/boards/nucleo-wl55jc1.cmake`, pilotes F7, exemples d'usage de `tests/*.py`.
Aucun fichier source, en-tête, script de liens ou module CMake propre aux machines MPS2.

### Oracle après le lot (`oracles/env-6-lot-qemu/`, clone noyau cd53527)

Mêmes commandes que l'oracle avant ; `rejouer-oracle.sh` : tout a réussi. host : ctest 7/7, dont
`host.mklepton_empreintes` sur la nouvelle référence. Comparaison avec `oracles/env-6-avant/` :

| Preset | Sections/symboles | Empreinte | Fumée | Banc KAL | Écarts expliqués |
| --- | --- | --- | --- | --- | --- |
| qemu-mps2-an386-embos | `.debug_str` 129045→129048 | différente | identique | 18/18, même liste | chemins de sources (DWARF), ordre d'édition de liens, date |
| qemu-mps2-an386-embos-soft | `.debug_str` +3 | différente | identique | 14/14, même liste | idem |
| qemu-mps2-an386-freertos | `.debug_str` +3 | différente | identique | 18/18, même liste | idem |
| qemu-mps2-an386-freertos-soft | `.debug_str` +3 | différente | identique | 14/14, même liste | idem |
| qemu-mps2-an500-embos | `.debug_str` +3 | différente | identique | 18/18, même liste | idem |
| qemu-mps2-an500-freertos | `.debug_str` +3 | différente | identique | 18/18, même liste | idem |
| 8 presets de carte (F439, WL55, F746, SAMD21) | code 0 | différente | – | – | date |

- Sections chargées (`.text`, `.data`, `.bss`, etc.) : tailles identiques sur les 14 presets ; symboles :
  aucun écart (nom, type, taille).
- `.debug_str` (+3 octets, non chargé) : noms des fichiers sources (`DW_AT_name`, chemins absolus du
  trunk) de `qemu_mps2_board.c` (`bsp/qemu_mps2/` → `bsp/qemu-mps2-<machine>/` : +6),
  `dev_cmsdk_uart_x.c` (`arch/all/uart/dev_cmsdk_uart/` → `arch/cortexm/qemu-mps2/uart/` : −1),
  `dev_eth_lan9118_x.c` (`arch/all/eth/dev_eth_lan9118/` → `arch/cortexm/qemu-mps2/eth/` : −2) ;
  total +3, nouveaux chemins relevés dans `.debug_str` de `lepton.elf` (an386-embos).
- Empreintes : date de compilation, et adresses déplacées par le nouvel ordre d'édition de liens
  (`qemu_mps2_board.c` lié comme objet avant le groupe, pilotes de la famille en fin d'archive `kernel`).
- Fumée : écarts limités à la date, au jeton UART1 et à la place de `rcv SIGCHLD` (variable d'une
  exécution à l'autre, déjà observée entre `env-5-apres` et `env-6-avant`).
- Avertissements de compilation : même nombre sur les 14 presets (`construction.log`).
- `scion ungraft && scion graft` : sans erreur, 4 032 feuilles, aucun fichier régulier ni lien cassé.

## Lot F4 (session 2)

PA-7 Q7 (utilisateur, 2026-10-13) : BSP `nucleo-f439zi` reporté après ENV-6 ; lot F4 = famille `stm32f4xx`
et BSP `nucleo-f429zi` ; presets `nucleo-f439zi-*` renommés `nucleo-f429zi-*`.

### Liste revérifiée

`ninja -C ~/lepton/build/nucleo-f439zi-embos -t deps` (avant extraction) : identique à
`env-6-extraction.md` §3 — compilés : `gpio.c`, `uart.c`, `eth.c`, `dev_stm32f4xx/dev_stm32f4xx_{uart_x,eth}.c`,
7 `.c` de `driverlib/` (`misc`, `rcc`, `gpio`, `usart`, `dma`, `syscfg`, `stm32f4x7_eth`),
`nucleo_f439zi_board.c`, `nucleo_f439zi_vectors.c`. `kernel/core/ucore/cmsis/Device/st/stm32f4xx`
n'est lu par aucune construction (`stm32f429xx.h` vient de `driverlib/`) ; déplacé dans la famille
conformément à la liste validée.

### Réalisation

| Dépôt | Branche | Commits |
| --- | --- | --- |
| `depots/lepton-famille/stm32f4xx` (nouveau) | `devenv/env-6` (sur `master` 1c3d789, vide) | 3ef8e46 import à l'identique depuis cd53527 (313 fichiers + vecteurs renommés `vecteurs/stm32f429xx_vectors.c`) ; fc8b5b9 manifeste (`sources` : 12 fichiers, Q2 ; `vecteurs` ; `USE_STDPERIPH_DRIVER` et inclusions `driverlib`, `dev_stm32f4xx` en portée publique, Q1), commentaire d'en-tête des vecteurs |
| `depots/lepton-bsp/nucleo-f429zi` (nouveau) | `devenv/env-6` (sur `master` a279c7a, vide) | 7203f76 import (`nucleo_f439zi_board.c`, `nucleo_f439zi.h`, `ld/mem_nucleo-f439zi.ld`, `include/user_kernel_mkconf.h`, `debug/openocd-nucleo-f439zi.cfg`, `debug/gdbinit-nucleo-f439zi`) ; 702adda manifeste (`demarrage`, `openocd`, `sonde` stlink ; `__tauon_cpu_device__`, `STM32F429xx`, `HSE_VALUE=8000000` publics), `CMakeLists.txt` (Q3), `#include` de `nucleo_f439zi.h` par le chemin du BSP (Q12), gdbinit réduit à la partie de carte, commentaires à nombre de lignes constant |
| clone noyau | `devenv/env-6` | c34d53e retrait des fichiers déplacés et renommage `debug/gdbinit-nucleo-f439zi` → `debug/gdbinit-lepton` (mécanique) ; 78878f9 module `cmake/boards/nucleo-f439zi.cmake` retiré, presets `nucleo-f429zi-*` (`LEPTON_MKCONF`), lecteur : champ `openocd` → `LEPTON_BOARD_OPENOCD_CFG`, `gdbinit-lepton` générique (Q8) sourcé par les gdbinit WL55, F746, SAMD21, `ci/run.sh`, exemples de `tests/*.py` ; e0895ee nouvelle référence d'empreintes mklepton |
| graine `depots/lepton-seed.scions/original-tree` | `devenv/env-6` | 268c0e8 deux lignes `*` |
| lepton-tools | `devenv/env-6` | 053cc43 skill `lepton-cibles` (presets, chemins OpenOCD et gdbinit) |

Lecteur (proposition appliquée, non couverte par R6) : `openocd` du BSP choisi → `LEPTON_BOARD_OPENOCD_CFG`
(chemin absolu dans le trunk) ; plus d'un fichier → erreur jusqu'à ENV-9 (la cible `flash` et le banc
KAL sur carte passent un seul `-f`). Vérifié : la cible `flash` de `nucleo-f429zi-embos` appelle
`openocd -f …/trunk/sys/root/src/kernel/dev/bsp/nucleo-f429zi/debug/openocd-nucleo-f439zi.cfg`.

Greffe : `scion ungraft`, `scion seed-clone --seed depots/lepton-seed.scions/original-tree`, `scion graft` :
4 034 feuilles (4 032 − 320 fichiers retirés du noyau − 1 `.DS_Store` non suivi supprimé du clone
+ 315 famille + 8 BSP) ; `.scion.grafted.list` à 7 lignes ; aucun fichier régulier ni lien cassé ;
`scion ungraft && scion graft` sans erreur. Manifestes valides (`check-jsonschema` 0.38.2) ;
`scripts/valider-schemas.sh` conforme.

### Empreintes mklepton (PA-7 Q5)

Sorties F4 rangées `mkconf_tauon_basic_nucleo_f439zi-nucleo-f429zi/` ; 5 fichiers identiques à
l'ancienne référence ; `kernel_mkconf.h` : ligne 15 seule (`#include
"sys/root/src/kernel/dev/bsp/nucleo-f429zi/include/user_kernel_mkconf.h"`). Contre-épreuve : même mklepton,
ancien chemin d'en-tête → `3eee0536…` (ancienne référence) ; nouveau chemin → `2140fe49…`. Les 38
autres empreintes sont inchangées.

### Oracle après le lot (`oracles/env-6-lot-f4/`, clone noyau e0895ee)

`rejouer-oracle.sh` (commande du §Commandes, `nucleo-f429zi-*` au lieu de `nucleo-f439zi-*`) : tout a
réussi ; host ctest 7/7. Comparaison avec `oracles/env-6-lot-qemu/` (F4 : `nucleo-f439zi-*` →
`nucleo-f429zi-*`) :

| Preset | Sections/symboles | Empreinte | Fumée | Banc KAL | Écarts expliqués |
| --- | --- | --- | --- | --- | --- |
| qemu-mps2-an386 ×4, an500 ×2 | code 0 | différente | identique | 18/18 (hard), 14/14 (soft), même liste | date |
| nucleo-f429zi-embos | `.debug_line` 308592→308604, `.debug_str` 142270→142282 | différente | – | – | chemin du fichier de vecteurs (DWARF), date |
| nucleo-f429zi-freertos | `.debug_line` +12, `.debug_str` +12 | différente | – | – | idem |
| WL55, F746, SAMD21 ×2 | code 0 | différente | – | – | date |

- F429ZI : sections chargées de tailles identiques, symboles identiques (nom, type, taille). +12 octets non
  chargés : `kernel/dev/bsp/nucleo_f439zi/nucleo_f439zi_vectors.c` (52 caractères) →
  `kernel/dev/arch/cortexm/stm32f4xx/vecteurs/stm32f429xx_vectors.c` (64) dans `.debug_str` ; dans la table
  de lignes, répertoire +14, nom −2. Les autres chemins (`nucleo_f439zi` → `nucleo-f429zi`, nom du
  répertoire de construction) ont la même longueur.
- Fumée : écarts limités à la date, au jeton UART1 et à la place de `rcv SIGCHLD` (et du chiffre qu'il
  préfixe à l'invite suivante).
- Avertissements de compilation : même nombre sur les 15 constructions.

### Recherche des restes dans le noyau

`git ls-files scion | grep -i -E 'f439|f429|stm32f4|nucleo_f4|nucleo-f4'` et `git grep -l` des chemins
`kernel/dev/arch/cortexm/stm32f4xx`, `kernel/dev/bsp/nucleo_f439zi` (clone noyau e0895ee) :
- restent, par décision : `etc/mkconf_tauon_basic_nucleo_f439zi.xml`, `etc/nucleo-f439zi/{.boot,.init}` (Q4) ;
  BSP hérités non construits qui incluent la famille par le trunk : `discovery_f4`,
  `discovery_f4-baseboard-modem`, `olimex_p407`, `stm32f469i-eval`, et leurs `user_kernel_mkconf.h`
  et XML (R9) ;
- **hors liste PA-7, signalé, non déplacé** : `kernel/usb/stm32f4-usb-core/` (pile USB device ST pour F4,
  non compilée) et `kernel/core/ucore/freeRTOS_{8-0-0,9-0-0}/source/arch/cortex-m4/stm32f4/` (démos
  FreeRTOS amont, non compilées) ;
- aucun fichier source, en-tête, script de liens, configuration de débogage ni module CMake propre à
  la NUCLEO-F429ZI.

### Point signalé (non bloquant)

`vecteurs/stm32f429xx_vectors.c` (famille) ne relie que les IRQ utilisées par la NUCLEO-F429ZI (12, 39,
57, 61, 71) à des gestionnaires aux noms CMSIS, dont quatre sont définis par le BSP
(`nucleo_f439zi_board.c:127-130`, `USART3_IRQHandler`…). Dépendance par symbole, pas par `#include`,
conforme à la liste validée. Une autre carte F429 qui utiliserait d'autres IRQ demanderait une table
complète (tous les vecteurs vers des noms CMSIS faibles) : à décider avant un second BSP F4.

## Lot WL (session 3)

PA-7 lot WL (utilisateur, 2026-10-13) : relais IRQ11/12/37/50 sortis de `stm32wl55jci_nucleo_system.c`
vers la famille ; manifeste `openocd` = cfg statique du BSP, cfg enveloppe générée par le `CMakeLists.txt`
du BSP ; `dev_stm32wlxx_bsp_radio_if.c` inclut `radio_board_if.h` par nom ;
`sys/user/tauon-basic/src/arch/st-stm32wl55jci-nucleo/` laissé, signalé.

### Liste revérifiée

`ninja -C ~/lepton/build/nucleo-wl55jc1-{embos,freertos} -t deps` (avant extraction, e0895ee) : identique à
`env-6-extraction.md` §4 — compilés : HAL 12 `.c`, `dev_stm32wlxx/` 3 `.c` + `dev_stm32wlxx_hal_tick.c`
(remplaçant fort), `Utilities/misc/stm32_mem.c`, SubGHz_Phy 5 `.c`, `stm32_radio_target/radio_board_if.c`,
BSP 4 `.c` (`stm32wl55jci_nucleo_system.c`, USART2, 2 radio). CMSIS device : 3 en-têtes lus.

### Réalisation

| Dépôt | Branche | Commits |
| --- | --- | --- |
| `depots/lepton-famille/stm32wlxx` (nouveau) | `devenv/env-6` (sur `master` 709bada, vide) | 8ea1490 import à l'identique depuis e0895ee (234 fichiers : `dev_stm32wlxx/`, `cubemx_hal_driver/`, `radio_subghz_phy/` sans `stm32_radio_target/`, `Utilities/`, CMSIS device `stm32wlxx` au même chemin de trunk) ; fa31306 manifeste (`sources` : 21 fichiers, Q2 ; `vecteurs` ; `remplacants_forts` `dev_stm32wlxx_hal_tick.c` ; `USE_HAL_DRIVER` et 9 inclusions publiques, Q1), `vecteurs/stm32wl55xx_vectors.c` (relais IRQ ; 62 IRQ < 64 : pas de table étendue), `radio_board_if.h` inclus par nom |
| `depots/lepton-bsp/nucleo-wl55jc1` (nouveau) | `devenv/env-6` (sur `master` a5200b4, vide) | 5653f97 import (20 fichiers : contenu de `kernel/dev/bsp/stm32wl55jci_nucleo/`, `stm32_radio_target/` (Q10), `ld/mem_nucleo-wl55jc1.ld`, `include/user_kernel_mkconf.h`, `debug/openocd-nucleo-wl55jc1.cfg`, `debug/gdbinit-nucleo-wl55jc1`) ; 58ff413 manifeste (`demarrage` système, `sources` 4 fichiers, ABI soft, `openocd` statique, `sonde` stlink ; `STM32WL55xx`, `CORE_CM4` et inclusions radio publiques), `CMakeLists.txt` (Q3 : nom uname, cfg OpenOCD générée qui remplace `LEPTON_BOARD_OPENOCD_CFG`, test `board.radio`), relais IRQ retirés, `#include` par le chemin du BSP (Q12), commentaires à nombre de lignes constant |
| clone noyau | `devenv/env-6` | 8d5a082 retrait des 254 fichiers déplacés (mécanique) ; 2b9bfc2 module `cmake/boards/nucleo-wl55jc1.cmake` retiré, presets WL (`LEPTON_MKCONF`), commentaire des cartes transitoires ; 94ea0e3 nouvelle référence d'empreintes mklepton |
| graine `depots/lepton-seed.scions/original-tree` | `devenv/env-6` | d6605f0 deux lignes `*` |
| lepton-tools | `devenv/env-6` | ad4374c skill `lepton-cibles` (cfg OpenOCD et gdbinit du BSP WL) |

Vérifié : la cfg générée (`build/nucleo-wl55jc1-embos/openocd-nucleo-wl55jc1.cfg`) source
`interface/stlink.cfg` puis `…/trunk/sys/root/src/kernel/dev/bsp/nucleo-wl55jc1/debug/openocd-nucleo-wl55jc1.cfg`.
Le message de configuration « bsp : aucune source pour la carte » (`cmake/components/kernel.cmake:167`)
porte sur la liste transitoire `LEPTON_BSP_SOURCES` ; il apparaît aussi pour les BSP QEMU et F4 ; les
4 sources du BSP sont bien compilées dans `bsp` (`CMakeFiles/bsp.dir/…`).

Greffe : `scion ungraft`, `scion seed-clone --seed depots/lepton-seed.scions/original-tree`, `scion graft` :
4 037 feuilles (4 034 − 255 retirés du noyau + 236 famille + 22 BSP) ; `.scion.grafted.list` à 9 lignes ;
aucun fichier régulier ni lien cassé ; `scion ungraft && scion graft` sans erreur. 8 manifestes du trunk
valides (`check-jsonschema` 0.38.2) ; `scripts/valider-schemas.sh` conforme.

### Empreintes mklepton (PA-7 Q5)

Sorties WL rangées `mkconf_tauon_basic_nucleo_wl55jc1-nucleo-wl55jc1/` ; 5 fichiers identiques à
l'ancienne référence ; `kernel_mkconf.h` : ligne 15 seule (`#include
"sys/root/src/kernel/dev/bsp/nucleo-wl55jc1/include/user_kernel_mkconf.h"`). Contre-épreuve : même mklepton,
ancien chemin d'en-tête → `04d6f4ce…` (ancienne référence) ; nouveau chemin → `f71ede49…`. Les 38 autres
empreintes sont inchangées.

### Oracle après le lot (`oracles/env-6-lot-wl/`, clone noyau 2b9bfc2 ; host rejoué sur 94ea0e3)

`rejouer-oracle.sh` (commande du §Commandes, `nucleo-f429zi-*`) : 14 presets croisés construits et capturés ;
seul échec `host:ctest` (`host.mklepton_empreintes`, référence pas encore mise à jour) ; host rejoué après
94ea0e3 : ctest 7/7. Comparaison avec `oracles/env-6-lot-f4/` :

| Preset | Sections/symboles | Empreinte | Fumée | Banc KAL | Écarts expliqués |
| --- | --- | --- | --- | --- | --- |
| qemu-mps2-an386 ×4, an500 ×2 | code 0 | différente | identique | 18/18 (hard), 14/14 (soft), même liste | date |
| nucleo-f429zi ×2, F746 ×2, SAMD21 ×2 | code 0 | différente | – | – | date |
| nucleo-wl55jc1-embos | symboles identiques ; `.data` 832→828 ; DWARF (`.debug_*`) | différente | – | – | remplissage de `.data` ; unité de compilation des vecteurs et chemins (DWARF) |
| nucleo-wl55jc1-freertos | symboles identiques ; `.data` 836→832, `.bss` 6892→6896 ; DWARF | différente | – | – | remplissage de `.data` et `.bss` ; idem |

- WL, sections chargées : démontré sur les cartes d'édition (`lepton.map`) de l'état précédent, reconstruit
  dans une copie d'essai du rootstock (scratchpad : clone noyau e0895ee, greffons WL absents, 4 034 feuilles ;
  `.data`/`.bss` identiques à `env-6-lot-f4`). Mêmes sections d'entrée (nom, taille, objet) avant et après
  dans `.data` et `.bss`, dans un autre ordre : `.data.SystemCoreClock` (4 octets) passe de `libbsp.a` à
  l'OBJECT `bsp_demarrage`, lié en tête, et les objets radio de `libkernel.a` (descripteurs de 2 octets,
  `MaxPayloadLength` 1 octet) sont extraits plus tôt ; les petites sections se regroupent : remplissage de
  `.data` 6 → 2 octets (avant : 1 après `_buf.0` de `lsh`, 2 après `printk_trace_desc_w`, 3 après `MaxPayloadLength` ; après : 1 après
  `_buf.0`, 1 après `MaxPayloadLength`) ; FreeRTOS,
  `.bss` : début avancé de 4 octets (0x20006604 → 0x20006600), remplissage 37 → 41 octets, fin inchangée.
  `.text` et les autres sections chargées : tailles identiques.
- WL, DWARF : une unité de compilation de plus (`vecteurs/stm32wl55xx_vectors.c`) et chemins changés
  (`stm32_radio_target` et répertoire du BSP) : `.debug_abbrev`, `.debug_aranges`, `.debug_frame`,
  `.debug_info`, `.debug_line`, `.debug_rnglists`, `.debug_str` ; sections non chargées.
- Fumée : écarts limités à la date, au jeton UART1 et à la place de `rcv SIGCHLD` (et du chiffre qu'il
  préfixe à l'invite suivante).
- Avertissements de compilation : même nombre sur les 15 constructions ; `outils.txt` identiques (hors
  horodatage).
- Copie d'essai : les écarts DWARF et `.text` FreeRTOS (+480) entre la copie et `env-6-lot-f4` viennent du
  chemin plus long du scratchpad (chaînes de chemin) ; seules `.data`/`.bss` y ont été exploitées.

### Recherche des restes dans le noyau

`git ls-files scion | grep -i -E 'wl55|stm32wl|wlxx'` et `git grep -l` des chemins
`kernel/dev/arch/cortexm/stm32wlxx`, `kernel/dev/bsp/stm32wl55jci_nucleo`, `cmsis/Device/st/stm32wlxx`
(clone noyau 94ea0e3) :
- restent, par décision : `etc/mkconf_tauon_basic_nucleo_wl55jc1.xml`, `etc/nucleo-wl55jc1/{.boot,.init}` (Q4) ;
  `sys/user/tauon-basic/src/arch/st-stm32wl55jci-nucleo/` (en-tête du portage IAR, non utilisé ; PA-7 lot WL) ;
- génériques, non propres à la carte : entrée `__tauon_cpu_device_cortexM4_stm32wlxx__` de
  `kernel/core/kernelconf.h` (table des puces), programme de test `bin/radiotst.c` (utilise `/dev/radio`),
  `tests/board_radio.py` ;
- historiques, chemins périmés (non construits, comme au lot F4) : `doc/BUILDING.md`, `doc/migration/*`,
  `tools/migration/*.py` ;
- aucun fichier source, en-tête, script de liens, configuration de débogage ni module CMake propre à
  la NUCLEO-WL55JC1.

### Points signalés (non bloquants)

- Comme pour F4 : `vecteurs/stm32wl55xx_vectors.c` (famille) ne relie que les IRQ utilisées par la carte
  (11, 12, 37, 50), vers des gestionnaires aux noms CMSIS dont trois sont définis par le BSP (USART2 et
  DMA) et un par la famille (`SUBGHZ_Radio_IRQHandler`, `dev_stm32wlxx_bsp_radio_if.c`). À compléter avant
  un second BSP WL.
- Dépendance famille → carte par nom d'en-tête (schéma ST) : SubGHz_Phy et `dev_stm32wlxx_bsp_radio_if.c`
  (famille) incluent `radio_conf.h`, `timer.h`, `mw_log_conf.h`, `radio_board_if.h`, fournis par le BSP
  (`stm32_radio_target`, inclusion publique). `dev_stm32wlxx_bsp_radio_if.c` porte aussi les paramètres
  FSK 868 MHz : candidat au BSP si une seconde carte WL apparaît.
