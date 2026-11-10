# ENV-45 — Sonde choisie par numéro de série

Session du 2026-11-10. Branche lepton-tools `devenv/env-45` (depuis `main` fbfe076).

## 0. État de départ
Conforme à `handoff/env-44.md` :

- lepton-tools `main` fbfe076 ; clone noyau `master` cde728f ; BSP `nucleo-wl55jc1` ef51ec1,
  `nucleo-f429zi` b9fe2bf, `nucleo-f439zi` 314f91b, `stm32f746g-disco` 6266908,
  `samd21-xplained-pro` f3cffa2 ; seed.scions `master` 7e8a0cc. Tous sur `master`, propres.
- Trunk : 3983 liens. Outils : scion 0.6.2.0, lepton 0.1.0.
- Sondes visibles par USB au démarrage : aucune.

## 1. Audit (lecture seule) → PA-77

### 1.1 Mécanisme existant (BSP `nucleo-wl55jc1`)
`<BSP-WL>/CMakeLists.txt` l. 10-26, inclus par le `CMakeLists.txt` racine du noyau (l. 41-43)
**après** `lepton_greffons_carte()` :

1. variable de cache `LEPTON_BOARD_STLINK_SERIAL` (vide par défaut) ;
2. `lepton_wl_cfg_bsp` ← cfg statique du manifeste (`LEPTON_BOARD_OPENOCD_CFG` posé par le
   lecteur) ;
3. `LEPTON_BOARD_OPENOCD_CFG` ← `${CMAKE_BINARY_DIR}/openocd-nucleo-wl55jc1.cfg`, écrite
   **toujours** : `source <cfg statique>` puis `adapter serial <n°>` si la variable est posée.

`<BSP-WL>/tests/CMakeLists.txt` (test `nucleo-wl55jc1.radio`) réutilise `lepton_wl_cfg_bsp`
pour la cfg de la carte paire (`openocd-nucleo-wl55jc1-paire.cfg`, `adapter serial
${LEPTON_RADIO_PEER_STLINK_SERIAL}`).

### 1.2 BSP visés
| BSP | champ `openocd` | `"sonde"` | cfg statique (contenu) | `CMakeLists.txt` |
| --- | --- | --- | --- | --- |
| `nucleo-f429zi` | `debug/openocd-nucleo-f439zi.cfg` (nom historique) | `stlink` | `source [find board/st_nucleo_f4.cfg]` | `LEPTON_BOARD_SERIAL_PORT`, `LEPTON_NET_TEST_*` ; aucune sonde |
| `nucleo-f439zi` | `debug/openocd-nucleo-f439zi.cfg` | `stlink` | idem | idem |
| `stm32f746g-disco` | `debug/openocd-stm32f746g-disco.cfg` | `stlink` | `source [find board/stm32f746g-disco.cfg]` | idem |
| `samd21-xplained-pro` | `debug/openocd-samd21-xplained-pro.cfg` | `cmsis-dap` | `source [find board/atmel_samd21_xplained_pro.cfg]` | `LEPTON_BOARD_SERIAL_PORT` |

Aucun de ces BSP ne pose de numéro : OpenOCD prend la première sonde de son pilote.

### 1.3 Consommateurs de `LEPTON_BOARD_OPENOCD_CFG` (clone noyau)
Tous lisent la variable après l'inclusion du `CMakeLists.txt` du BSP, donc la cfg générée :

- `cmake/components/firmware.cmake` l. 145-181 : cible `flash`, `board.smoke_lsh`, `board.net` ;
- `tests/kal/CMakeLists.txt` l. 55 : `kal.board_flash` et le banc KAL sur carte
  (`kal_openocd.py --cfg`) ;
- `cmake/lepton_greffons.cmake` l. 511 (`lepton_greffons_tests`) : variable offerte aux tests de
  greffon (seul usage : `nucleo-wl55jc1.radio`).

### 1.4 Consommateurs de `LEPTON_BOARD_STLINK_SERIAL` hors du BSP WL55
- `rapports/env-42-core-cm4/banc-wl55.sh` l. 23 (`-DLEPTON_BOARD_STLINK_SERIAL="$SA"`) ;
- skill `lepton-cibles` l. 62, 79, 116 ;
- relevés historiques `oracles/env-32-avant|apres`, `oracles/env-33-debian` (`relever-ctest-N.sh`,
  non rejoués) ; rapports `env-2-*`, `env-24`, `env-32`, `env-42` (texte).
- Aucun preset : `CMakeUserPresets.json` est généré par lepton dans la graine de projet (versionné,
  partagé entre hôtes) et ne contient aucun numéro ; les numéros passent par `-D` en ligne de
  commande. Les caches CMake existants `<ROOTSTOCK>/build/nucleo-wl55jc1-*` peuvent contenir
  `LEPTON_BOARD_STLINK_SERIAL`.
- Oracle `env-44-apres/ctest-N` : presets de carte relevés sans port série (0 test), donc
  insensibles au nom de la variable.

### 1.5 Éditeur (`lepton generate --probe-serial`)
- `lepton/generate.py` : réglage `lepton.probeSerial` de l'espace (non versionné), repris d'une
  génération à l'autre ; lancement Cortex-Debug par `openOCDLaunchCommands: ["adapter serial
  <n°>"]` (O8) et tâche « flasher » par `-c "adapter serial <n°>"`.
- L'éditeur passe la **cfg statique** du BSP (`configFiles`), jamais la cfg générée du build : les
  deux chemins sont indépendants aujourd'hui. Un numéro unique, propre à l'hôte, ne peut pas aller
  dans `CMakeUserPresets.json` (versionné) sans y mettre une donnée locale.

### 1.6 Formes comparées
| Critère | **Par BSP** (recopie du WL55) | **Générique** (lecteur du noyau) |
| --- | --- | --- |
| Dépôts touchés | 4 BSP (F429, F439, F746, SAMD21) ; WL55 inchangé | clone noyau (`lepton_greffons_carte`) + BSP WL55 (retire son mécanisme) |
| Code | ~12 lignes recopiées ×4, 5 copies au total | une fonction ; tout BSP à champ `openocd`, futur compris |
| Variable vide | cfg générée toujours (forme WL55) ou cfg statique | cfg statique inchangée (aucune cfg générée) : comportement d'avant à l'identique |
| Cfg statique pour la paire WL55 | `lepton_wl_cfg_bsp` (inchangé) | exposée par le lecteur (ex. `LEPTON_BOARD_OPENOCD_CFG_BSP`) |
| Ordre des fusions | indépendant | noyau et WL55 ensemble (sinon WL55 ré-encapsule la cfg générée : `adapter serial` en double) |
| EDBG SAMD21 | même question | même question |

Recommandation : **générique**, variable `LEPTON_BOARD_PROBE_SERIAL` (le manifeste parle de
`"sonde"` : `stlink`, `cmsis-dap` ; même mot que `--probe-serial` de lepton). Cfg générée
`${CMAKE_BINARY_DIR}/openocd-<bsp>.cfg` seulement si la variable est posée.

Sort de `LEPTON_BOARD_STLINK_SERIAL` : alias transitoire dans le lecteur du noyau (si posée et
`LEPTON_BOARD_PROBE_SERIAL` vide : reprise, avec message `DEPRECATION`), pour ne casser ni les
caches existants ni les commandes des rapports ; `banc-wl55.sh` et la skill passent au nouveau nom.
`LEPTON_RADIO_PEER_STLINK_SERIAL` (propre au test radio WL55) : inchangé, ou renommé
`LEPTON_RADIO_PEER_PROBE_SERIAL` par cohérence (question du PA-77).

Lien avec `--probe-serial` : deux réglages séparés (construction : cache CMake `-D` ; éditeur :
`lepton.probeSerial` de l'espace), documentés ensemble dans `README.md` et la skill. Raison : le
seul fichier partagé par les deux est `CMakeUserPresets.json`, versionné.

### 1.7 EDBG (SAMD21) et numéros des sondes
Cinq sondes branchées ensemble (2026-11-10). Numéros par `ioreg` (USB), ports par
`IOCalloutDevice` ; chaque sonde interrogée par `openocd -f <cfg statique du BSP, trunk> -c
"adapter serial <n°>" -c init -c shutdown` (attachement seul : ni reset, ni flash). Journaux :
scratchpad de session, non conservés ; extraits ci-dessous.

| Carte | Sonde (OpenOCD) | Numéro | Port console | `init` |
| --- | --- | --- | --- | --- |
| NUCLEO-F429ZI | ST-LINK/V2-1 V2J27M15, 0483:374B | 0672FF495252717267243842 | `/dev/cu.usbmodem1454403` | code 0, Cortex-M4 `stm32f4x.cpu` |
| STM32F746G-DISCO | ST-LINK/V2-1 V2J24M11, 0483:374B | 0671FF495351885087181231 | `/dev/cu.usbmodem14303` | code 0, Cortex-M7 `stm32f7x.cpu` |
| SAMD21 Xplained Pro | EDBG CMSIS-DAP FW 01.1A.00FB, 03EB:2111 | ATML2130021800003505 | `/dev/cu.usbmodem14602` | code 0, `CMSIS-DAP: Serial# = ATML2130021800003505`, Cortex-M0+ |
| NUCLEO-WL55JC1 A | STLINK-V3 V3J7M3, 0483:374E | 002700253431510837393937 | `/dev/cu.usbmodem145103` | code 0, `stm32wlx.cpu0` |
| NUCLEO-WL55JC1 B | STLINK-V3 V3J7M3, 0483:374E | 004F003E3431510937393937 | `/dev/cu.usbmodem1454303` | code 0, `stm32wlx.cpu0` |

Les ports diffèrent de ceux de la skill `lepton-cibles` (topologie USB changée) : ils se relèvent à
chaque banc.

Constats :
- **EDBG** : `adapter serial` est accepté par le pilote CMSIS-DAP d'OpenOCD 0.12.0 et choisit la
  sonde (vérifié sur la carte).
- **Numéro faux** : code 1, aucune autre sonde prise. ST-LINK : `Error: open failed` (laconique,
  ne nomme pas le numéro) ; CMSIS-DAP : `Error: unable to find a matching CMSIS-DAP device`.
- **Numéro vide** (comportement d'aujourd'hui) : la cfg F429 prend le ST-LINK du F746 (V2J24M11)
  et échoue sur l'IDCODE (`Error: expected 1 of 1: 0x2ba01477`, code 1). La cfg F746 tombe par
  chance sur la bonne sonde. Le défaut B4 est reproduit.

### 1.8 PA-77 (2026-11-10, décision de l'utilisateur)
Forme générique, `LEPTON_BOARD_PROBE_SERIAL` ; cfg générée seulement si le numéro est posé, avec un
`echo` du numéro demandé ; `LEPTON_BOARD_STLINK_SERIAL` alias transitoire (`DEPRECATION`),
`LEPTON_RADIO_PEER_STLINK_SERIAL` inchangée ; deux réglages (construction, éditeur) documentés
ensemble ; `nucleo-f439zi` contrôlé par son image sur la NUCLEO-F429ZI ; flash autorisé sur les
cinq cartes du §1.7.
