# Étape ENV-45 — Sonde choisie par numéro de série

## Contexte
Seul le BSP `nucleo-wl55jc1` choisit sa sonde par numéro de série (`LEPTON_BOARD_STLINK_SERIAL`).
Les autres BSP de carte prennent la première sonde qu'OpenOCD trouve. Conséquence : les bancs F429
et F746 sont passés avec les WL55 débranchées (`rapports/env-42-core-cm4.md` O-1,
`handoff/env-31.md` pièges). Décision du 2026-11-09 (point B4 de `HORS-PLAN.md`) : donner ce choix
aux BSP qui ne l'ont pas.

Archétype : infrastructure. Les binaires ne changent pas : seuls la configuration OpenOCD générée et
les tests changent.

## Prérequis
- ENV-44 terminée.
- Mécanisme existant, dans
  `<ROOTSTOCK>/depots/lepton/bsp-nucleo-wl55jc1/master/scion/sys/root/src/kernel/dev/bsp/nucleo-wl55jc1/CMakeLists.txt` :
  - variable de cache `LEPTON_BOARD_STLINK_SERIAL` ;
  - cfg générée `${CMAKE_BINARY_DIR}/openocd-nucleo-wl55jc1.cfg`, qui source la cfg du BSP et ajoute
    `adapter serial` ;
  - `LEPTON_BOARD_OPENOCD_CFG` remplacée par la cfg générée ;
  - test radio : variables `LEPTON_RADIO_PEER_*` (`tests/CMakeLists.txt`).
- Lecteur du noyau : `cmake/lepton_greffons.cmake` (champ `openocd` → `LEPTON_BOARD_OPENOCD_CFG`,
  l. 311 à 353), utilisé par `cmake/components/firmware.cmake` (cible flash) et
  `tests/kal/CMakeLists.txt` (banc KAL).
- Éditeur : `lepton generate --probe-serial` (`lepton/generate.py`, réglage `lepton.probeSerial`,
  `openOCDLaunchCommands` et tâches).
- BSP visés : `nucleo-f429zi`, `nucleo-f439zi`, `stm32f746g-disco` (ST-LINK), `samd21-xplained-pro`
  (EDBG, CMSIS-DAP).
- Sondes connues : WL55 A n° 002700253431510837393937, B n° 004F003E3431510937393937
  (`rapports/env-42-core-cm4.md`) ; NUCLEO-F429ZI, ST-LINK/V2-1 n° 0672FF495252717267243842
  (`rapports/env-35-hal-f4.md` §2). F746, SAMD21 : <À CONFIRMER au PA-77>.
- Pas de carte NUCLEO-F439ZI (A2 de `HORS-PLAN.md`). En R43-1, l'image `nucleo-f439zi-embos` a tourné
  sur la NUCLEO-F429ZI.
- Skills `lepton-rootstock`, `lepton-oracle`, `lepton-cibles`.

## Tâches

### 1. Audit (lecture seule) → PA-77
- Pour chaque BSP visé : champ `openocd` du manifeste, `CMakeLists.txt`, consommateurs de
  `LEPTON_BOARD_OPENOCD_CFG` (flash, KAL, fumée sur carte, tests de greffon, `board_net`).
- Consommateurs de `LEPTON_BOARD_STLINK_SERIAL` hors du BSP WL55 : banc
  `rapports/env-42-core-cm4/banc-wl55.sh` (l. 23, `-DLEPTON_BOARD_STLINK_SERIAL`), bancs des
  rapports antérieurs, skill `lepton-cibles`. Un renommage les casse.
- Comparer deux formes :
  - **par BSP** : recopier le mécanisme du WL55 dans chaque BSP ;
  - **générique** : une seule variable dans le lecteur du noyau, qui génère la cfg pour tout BSP à
    champ `openocd`. Le WL55 la reprend alors, et `LEPTON_BOARD_STLINK_SERIAL` devient un alias ou
    disparaît.
- Nom de la variable (`LEPTON_BOARD_PROBE_SERIAL` ou autre), compatibilité des presets utilisateur
  existants (`CMakeUserPresets.json`).
- Cohérence avec `lepton generate --probe-serial` : une même valeur pour la construction et pour
  l'éditeur, ou deux réglages séparés.
- EDBG (SAMD21) : `adapter serial` est-il accepté par le pilote CMSIS-DAP d'OpenOCD 0.12.0 ? Le
  vérifier sur la carte, pas dans la documentation seule.
- Rapport `rapports/env-45-sonde.md`, §1.
- **PA-77** : l'utilisateur valide :
  - la forme (par BSP ou générique) et le nom de la variable ;
  - le sort de `LEPTON_BOARD_STLINK_SERIAL` ;
  - le lien avec `lepton generate --probe-serial` : <À CONFIRMER au PA-77> ;
  - les cartes disponibles et leurs numéros ; l'écriture flash (PA-11) ;
  - le contrôle de `nucleo-f439zi`, sans carte : image F439 sur la NUCLEO-F429ZI (forme de R43-1),
    ou cfg générée seulement : <À CONFIRMER au PA-77>.
- Aucune modification avant la réponse.

### 2. Oracle avant
Skill `lepton-oracle` : host et les 16 presets → `rapports/oracles/env-45-avant/`, conforme à
l'oracle de référence en vigueur après ENV-44.

### 3. Mise en œuvre
- Commits dans les clones désignés (noyau et/ou BSP), puis regreffe si des fichiers sont ajoutés.
- lepton-tools : modifications retenues au PA-77, tests compris ; documentation (`README.md`,
  skill `lepton-cibles` : choix de la sonde) ; bancs de `rapports/` encore utilisés
  (`banc-wl55.sh`), si la variable change de nom.

### 4. Contrôles → PA-78
- Oracle après : code 0 sur host et les 16 presets.
- Banc à plusieurs sondes branchées en même temps (WL55 A et B, plus la carte visée) :
  - bancs F429, F746 et SAMD21 verts, avec la sonde choisie par son numéro ;
  - `nucleo-f439zi` : contrôle retenu au PA-77 ;
  - banc WL55 A/B radio comprise : identique à la référence ;
  - variable vide : comportement d'avant (première sonde trouvée).
- Numéro absent ou faux : message d'OpenOCD clair, pas de flash sur une autre carte.
- **PA-78** : rapport ; push et fusions des branches `devenv/env-45` (PA-P).

## Critères de validation
- [ ] PA-77 et PA-78 tranchés et consignés.
- [ ] Chaque BSP de carte visé choisit sa sonde par numéro ; bancs F429, F746, SAMD21 et WL55 verts
      avec plusieurs sondes branchées ; `nucleo-f439zi` selon le PA-77.
- [ ] Binaires identiques (code 0).
- [ ] Variable vide : comportement inchangé.

## Pièges connus
- `LEPTON_BOARD_OPENOCD_CFG` est posé par un `set` simple, impossible à surcharger depuis un preset
  (`handoff/env-31.md`) : il faut la cfg générée, pas une variable de cache.
- Cortex-Debug n'applique pas `serialNumber` à OpenOCD (O8) : l'éditeur passe par
  `openOCDLaunchCommands`.
- Un flash sur la mauvaise carte écrase l'image de la WL55 B, qui sert de pair radio : vérifier le
  numéro avant chaque `flash`.
- La NUCLEO-F429ZI doit être de retour sur le Mac (laissée sur la VM après R43-1).
- Les rootstocks d'essai du Mac et de la VM ne sont pas regreffés avant ENV-50.

## À la fin de l'étape
`DEVENV-STATUS.md` :
- statut et branches ;
- décisions PA-77 et PA-78 ;
- numéros des sondes dans §Emplacements ;
- journal.

`HORS-PLAN.md` : B4 marqué, avec renvoi au rapport. Passation `handoff/env-45.md`.
