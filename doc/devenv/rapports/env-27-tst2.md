# ENV-27 — TST-2 : tests fournis par un greffon — rapport

Session du 2026-11-02, hôte Mac. Clone noyau `master` 0bdce87, lepton-tools `devenv/env-27`
(depuis `main` 606ebd0). §1 à §4 : audit en lecture seule (tâche 1), avant le PA-41.

## 1. Déclaration actuelle des tests (clone noyau)

| Lieu | Tests | Condition de création | Étiquettes | Fixtures |
| --- | --- | --- | --- | --- |
| `CMakeLists.txt` racine | `enable_testing()` (l. 56) ; `add_subdirectory(tests/host)` si `LEPTON_ISA=host` | — | — | — |
| `tests/host/CMakeLists.txt` | `host.vfs_ufs`, `host.ufs_format_host`, `host.ufs_format_arm`, `host.kernel_stub`, `host.mklepton`, `host.mklepton_format`, `host.mklepton_empreintes` | preset `host` | `host` | — |
| `cmake/components/firmware.cmake` l. 190-221 | `smoke.lsh` (QEMU) ; `net.ping_ftpd` (QEMU, Linux seul) | `LEPTON_QEMU_MACHINE` (manifeste BSP) ; réseau : `LEPTON_NET_STACK`, `LEPTON_NET_TEST_FTP_FILE`, hôte non Apple | `smoke;kal;arch:<cœur>;backend:<b>` ; `net;…` | `smoke.lsh` : `FIXTURES_SETUP kal_t0` ; `net.ping_ftpd` : `REQUIRED kal_t0` |
| `cmake/components/firmware.cmake` l. 155-184 | `board.smoke_lsh`, `board.net` (carte) | `LEPTON_BOARD_SERIAL_PORT` (cache, vide par défaut) et `openocd` trouvé ; réseau : `LEPTON_NET_STACK`, `LEPTON_NET_TEST_HOST_IP` | `board;kal;…` ; `board;net;…` | `board.smoke_lsh` : `SETUP board_t0` ; `board.net` : `REQUIRED board_t0` |
| `tests/kal/CMakeLists.txt` | `kal.T1`…`kal.T8`, `kal.T1F/T4F/T6F/T7F` (ABI hard), `kal.TICI`, `TCLK`, `TSBRK`, `IRQ`, `kal.harness_fail` (`WILL_FAIL`) ; carte : `kal.board_flash` en plus | inclus par les deux branches de `firmware.cmake` | `kal;arch:…;backend:…` (+ `board` sur carte) | QEMU : `REQUIRED kal_t0` ; carte : `board_kal_flash` (posée par `kal.board_flash`, qui exige `board_t0`) |
| **BSP `nucleo-wl55jc1`, `CMakeLists.txt` du greffon** | `board.radio` (script `${CMAKE_SOURCE_DIR}/tests/board_radio.py` du noyau) | `LEPTON_BOARD_SERIAL_PORT`, `LEPTON_RADIO_PEER_STLINK_SERIAL`, `LEPTON_RADIO_PEER_SERIAL_PORT` | `board;radio;…` | — |

Constats :
- **K1** — Un mécanisme existe déjà pour le seul BSP de la carte : son `CMakeLists.txt` facultatif
  (`LEPTON_BOARD_CMAKE`, posé par `lepton_greffons_carte`, inclus par le `CMakeLists.txt` racine
  avant `enable_testing()` et avant `components/firmware`). `board.radio` y est déclaré. Il est
  inclus par `include()` (portée du répertoire racine), pas par `add_subdirectory()` ; aucun
  autre type de greffon (famille, application, bibliothèque) n'a d'équivalent.
- **K2** — Presets de test : un par preset de configuration (17), `output.outputOnFailure` seul,
  aucun filtre (`CMakePresets.json` du noyau, généré à l'identique par `lepton generate`,
  `generate.py` l. 290-313). Tâches de l'éditeur : `ctest --preset <P> -L smoke` et `-L kal` pour
  les configurations QEMU (`generate.py` l. 496-499), aucune tâche de test pour les cartes ni
  pour host.
- **K3** — Trois contextes d'exécution : host (`LEPTON_ISA=host`, `tests/host`, pas de carte, pas
  de manifeste BSP actif) ; QEMU (`LEPTON_QEMU_MACHINE` du manifeste BSP, `qemu-system-arm`
  trouvé) ; carte (`LEPTON_BOARD_SERIAL_PORT` donné à la configuration, OpenOCD trouvé, cfg du
  champ `openocd`). Sans port série, les presets de carte n'ont **aucun** test.
- **K4** — Les scripts Python sont désignés par `${CMAKE_SOURCE_DIR}/tests/…` (trunk) ;
  `board_radio.py` importe `smoke_lsh` par `os.path.dirname(os.path.realpath(__file__))` : le
  `realpath` résout le lien du trunk vers le clone noyau. Un script déplacé dans un autre greffon
  ne trouverait plus `smoke_lsh` (piège du fichier d'étape).
- **K5** — Aucun greffon application ou bibliothèque dans le trunk (13 manifestes : 1 noyau,
  7 BSP, 5 familles).

## 2. Listes `ctest -N` de référence (builds existants de `<ROOTSTOCK>/build`, 2026-11-02)

| Preset | Tests | Total |
| --- | --- | --- |
| `host` | `host.vfs_ufs`, `host.ufs_format_host`, `host.ufs_format_arm`, `host.kernel_stub`, `host.mklepton`, `host.mklepton_format`, `host.mklepton_empreintes` | 7 |
| `qemu-mps2-an386-embos` | `smoke.lsh`, `kal.T1`…`T8`, `kal.T1F`, `T4F`, `T6F`, `T7F`, `kal.TICI`, `TCLK`, `TSBRK`, `IRQ`, `kal.harness_fail` | 18 |
| `nucleo-wl55jc1-embos`, `nucleo-f429zi-embos` | — (pas de `LEPTON_BOARD_SERIAL_PORT` dans le cache) | 0 |

Les listes des 17 presets seront archivées avec l'oracle avant (tâche 2), et, pour les cartes,
complétées par une configuration avec `-DLEPTON_BOARD_SERIAL_PORT=…` si le PA-41 retient un
test de carte.

## 3. Tests du noyau propres à une carte ou une famille (relevés, rien déplacé)

| Script ou test | Portée réelle | Déclaré à CTest | Candidat au déplacement |
| --- | --- | --- | --- |
| `tests/board_radio.py` / `board.radio` | NUCLEO-WL55JC1 (radio FSK 868 MHz, deux cartes) | oui, par le BSP `nucleo-wl55jc1` | **oui** : seul test propre à une carte ; mais importe `smoke_lsh` du noyau (K4) et exige deux cartes |
| `tests/board_net.py` / `board.net` | toute carte à réseau (F429ZI, F439ZI, F746G) | oui, `firmware.cmake` | non : générique |
| `tests/net_qemu.py` / `net.ping_ftpd` | QEMU MPS2, Linux | oui | non : générique |
| `tests/endurance_board.py` | toute carte (v7m, v6m) | non (lancé à la main) | non |
| `tests/kal_openocd.py`, `smoke_lsh.py`, `tests/kal/` | générique | oui | non |

## 4. Formes possibles de la découverte

Contexte commun : la découverte se ferait dans `lepton_greffons.cmake`, appelée après
`components/firmware` (cibles `lepton` et `kal_bench`, variables `LEPTON_QEMU_ARM`,
`LEPTON_OPENOCD`, `Python3_EXECUTABLE` déjà posées). Greffons concernés : ceux qui sont actifs
dans la configuration (BSP = `LEPTON_BOARD`, sa famille, applications, bibliothèques), noyau
exclu (ses tests restent tels quels). Répertoire de construction :
`${CMAKE_BINARY_DIR}/greffons/<nom>/tests`, par `add_subdirectory` (portée propre, fixtures
`kal_t0` et `board_t0` utilisables, elles sont globales à CTest).

| Forme | Description | Schéma | `lepton check` | BLD-6 (lecteur commun) | Remarques |
| --- | --- | --- | --- | --- | --- |
| A. Convention | `<destination>/tests/CMakeLists.txt` présent → `add_subdirectory` | inchangé | rien à contrôler (absence = pas de tests) | une fonction + un appel | implicite : un répertoire `tests/` existant changerait de sens ; aucune erreur si mal nommé |
| **B. Champ du manifeste** (proposée) | `"tests": "<répertoire relatif à la destination>"` contenant un `CMakeLists.txt` → `add_subdirectory` | champ `tests` (`chemin_relatif`) | répertoire et `CMakeLists.txt` présents (comme `openocd`, `svd`) ; erreur située | une fonction + un appel | explicite, cohérent avec les champs de fichiers existants ; découvert sans configuration de la graine (TST-2) |
| C. Liste déclarative | `"tests": [{"nom", "commande", "etiquettes", "execution": "qemu|carte"}]` traduite par le lecteur | objet détaillé | contrôle complet | lecteur sensiblement plus long (substitution de `$<TARGET_FILE:lepton>`, port, cfg) | expressivité limitée (fixtures, conditions, fichiers générés : cf. `board.radio`) |

Fonction auxiliaire proposée avec B (ou A) : `lepton_greffon_test(NAME … COMMAND … [LABELS …]
[PROPERTIES …])`, définie par le lecteur, qui préfixe le nom par `<greffon>.` et ajoute
`greffon:<nom>;arch:<cœur>;backend:<b>` aux étiquettes, pour que `ctest -L greffon:` sélectionne
les tests des greffons. Contexte d'exécution exposé : `LEPTON_GREFFON_TEST_NOM`,
`LEPTON_TESTS_NOYAU` (= `${CMAKE_SOURCE_DIR}/tests`, pour réutiliser `smoke_lsh.py` sans copie,
K4). Le `CMakeLists.txt` de carte existant (K1) reste inchangé.

Types de tests possibles :
- QEMU : condition `LEPTON_QEMU_MACHINE` ; exécutable sur le Mac, en CI ; fixture `kal_t0`.
- Carte : condition `LEPTON_BOARD_SERIAL_PORT` ; fixture `board_t0`.
- Hôte : le preset `host` n'a ni carte ni greffon actif hors noyau ; un test hôte d'un greffon
  supposerait de compiler ses sources pour l'hôte : hors périmètre proposé.

## 5. Modèles de `lepton scion new` (`lepton/templates/`)

Modèles `application`, `library`, `bsp`, `seed` ; `template_files()` (`templates.py`) prend tous
les fichiers du répertoire du modèle. Un squelette `tests/CMakeLists.txt` (un test QEMU appelant
`smoke_lsh.py` avec une commande lsh) serait utile pour `application` (vérifier que la commande
répond) ; pour `bsp`, il dépend du mode d'exécution (QEMU ou carte). Les modèles actuels ne
créent aucun `CMakeLists.txt`.

Observation O-1 : `lepton/templates/.DS_Store` existe dans le dépôt de travail (ignoré par
`.gitignore`, non suivi) ; `template_files()` le prendrait en exécution depuis le dépôt (venv de
développement, `pip install -e`). L'installation pipx (roue hatchling, qui suit `.gitignore`)
n'est pas concernée : à vérifier, sans effet sur ENV-27.

## 6. PA-41 (2026-11-02, décisions de l'utilisateur)

| Question | Réponse |
| --- | --- |
| Forme de la découverte | B : champ `tests` du manifeste (répertoire relatif à la destination, contenant un `CMakeLists.txt`), `add_subdirectory` pour chaque greffon actif, noyau exclu ; schéma étendu ; `lepton check` contrôle le répertoire et le `CMakeLists.txt` ; fonction `lepton_greffon_test` |
| Types de tests | QEMU (`LEPTON_QEMU_MACHINE`, fixture `kal_t0`) et carte (`LEPTON_BOARD_SERIAL_PORT`, fixture `board_t0`) ; hôte hors périmètre ; étiquettes `greffon:<nom>`, `arch:<cœur>`, `backend:<b>` ajoutées par la fonction |
| Greffon d'essai | test QEMU neuf dans le BSP `qemu-mps2-an386` (4 presets an386) ; `board.radio` non déplacé |
| Modèles de `scion new` | squelette de test dans `application` et `bsp` |
