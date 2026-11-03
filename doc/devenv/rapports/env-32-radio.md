# ENV-32 — Test radio fourni par le BSP `nucleo-wl55jc1` : audit et rapport

Session du 2026-11-03. Branches `devenv/env-32` : lepton-tools (depuis `main` df32bf4), clone noyau
(depuis `master` 7fe3757), `bsp-nucleo-wl55jc1` (depuis `master` c9183de).
Chemins : `<BSP-WL>` = `<ROOTSTOCK>/depots/lepton/bsp-nucleo-wl55jc1/master/scion/sys/root/src/kernel/dev/bsp/nucleo-wl55jc1`,
`<NOYAU>` = `<ROOTSTOCK>/depots/lepton/original/master/scion`.

## 1. Déclaration actuelle de `board.radio`

`<BSP-WL>/CMakeLists.txt` (53 lignes), inclus par `include(${LEPTON_BOARD_CMAKE})` du
`CMakeLists.txt` racine, l. 43, avant `enable_testing()` (l. 56) et `components/firmware` (l. 60).

| Lignes | Contenu | Rôle |
| --- | --- | --- |
| 5-8 | `LEPTON_BOARD_UNAME_MACHINE`, définition `__KERNEL_CPU_DEVICE_NAME` | carte (construction) |
| 15-26 | cache `LEPTON_BOARD_STLINK_SERIAL` ; `lepton_wl_cfg_bsp` = cfg statique ; `LEPTON_BOARD_OPENOCD_CFG` remplacé par `${CMAKE_BINARY_DIR}/openocd-nucleo-wl55jc1.cfg` (`source` + `adapter serial`) | carte (flash, débogage, fumée, banc KAL) |
| 27-28 | cache `LEPTON_BOARD_SERIAL_PORT` | carte (fumée, banc KAL, radio) |
| 30-36 | cache `LEPTON_RADIO_PEER_STLINK_SERIAL`, `LEPTON_RADIO_PEER_SERIAL_PORT` | test radio seul |
| 37-53 | si les 3 variables : `find_program(LEPTON_OPENOCD)`, `find_package(Python3)`, cfg `${CMAKE_BINARY_DIR}/openocd-nucleo-wl55jc1-paire.cfg`, `add_test(board.radio …)`, propriétés | test radio seul |

Test relevé (`ctest --show-only=json-v1`, configuration du banc) :
- commande : `python3 <trunk>/tests/board_radio.py --port-a <A> --port-b <B>
  --reset-a "openocd -f <build>/openocd-nucleo-wl55jc1.cfg -c \"program <build>/lepton.elf verify reset exit\""
  --reset-b "openocd -f <build>/openocd-nucleo-wl55jc1-paire.cfg -c \"program … \"" --log <build>/board_radio.log` ;
- étiquettes `board`, `radio`, `arch:cortex-m4f`, `backend:<embos|freertos>` ;
- propriétés `TIMEOUT 300`, `RUN_SERIAL TRUE`, `ENVIRONMENT PYTHONDONTWRITEBYTECODE=1` ; aucune
  fixture (ni `board_t0` requise) ; répertoire de travail `<build>`.

## 2. Dépendances du script

`<NOYAU>/tests/board_radio.py` (116 lignes) : `argparse, os, re, shlex, subprocess, sys, time` ;
`sys.path.insert(0, dirname(realpath(__file__)))` puis `from smoke_lsh import Console, SerialLink,
PROMPT, run_command`. Appelé par le chemin du trunk (`${CMAKE_SOURCE_DIR}/tests/…`) : `realpath`
mène au clone noyau, où est `smoke_lsh.py`. Déplacé dans le BSP, `realpath` mènerait au clone du
BSP : `smoke_lsh` introuvable (K4 d'ENV-27). Chemins de fichiers : tous passés en arguments absolus
(`--log` a un défaut relatif `board_radio.log`, non utilisé).

## 3. Contexte offert par le lecteur (`<NOYAU>/cmake/lepton_greffons.cmake`)

- `lepton_greffons_tests()` (l. 512-528), appelée l. 61 de la racine, après `components/firmware`,
  pour les seules constructions croisées : `add_subdirectory(<destination>/<tests>
  ${CMAKE_BINARY_DIR}/greffons/<nom>/tests)` pour chaque greffon actif dont le manifeste déclare
  `tests` (BSP = `LEPTON_BOARD`). Variables : `LEPTON_GREFFON_TEST_NOM`, `LEPTON_TESTS_NOYAU`
  (= `${CMAKE_SOURCE_DIR}/tests`, **exposée**, comme le proposait ENV-27 §4), et par portée héritée
  celles de la carte : `LEPTON_BOARD_SERIAL_PORT`, `LEPTON_OPENOCD`, `LEPTON_BOARD_OPENOCD_CFG`
  (déjà la cfg générée de la l. 18 du BSP), `lepton_wl_cfg_bsp`, `Python3_EXECUTABLE`
  (`find_package` de `firmware.cmake` l. 133).
- `lepton_greffon_test(NAME COMMAND [LABELS] [PROPERTIES])` (l. 534-546) : nom
  `<greffon>.<NAME>` **imposé**, étiquettes `greffon:<nom>`, `LABELS`, `arch:`, `backend:` ;
  `WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}`.
- Fixture `board_t0` : posée par `board.smoke_lsh` (`firmware.cmake` l. 167) ; le test radio n'en
  dépend pas aujourd'hui.
- Modèle existant : `bsp-qemu-mps2-an386`, `tests/CMakeLists.txt` + `peripheriques.py`
  (`--tests-noyau ${LEPTON_TESTS_NOYAU}`, puis `sys.path.insert(0, args.tests_noyau)`).

## 4. Références à `board.radio` / `board_radio.py`

| Dépôt | Fichier | Nature | À mettre à jour |
| --- | --- | --- | --- |
| BSP | `<BSP-WL>/CMakeLists.txt` l. 30-53 | déclaration | oui (retrait) |
| noyau | `scion/tests/board_radio.py` | script | selon Q5 |
| noyau | `doc/BUILDING.md` l. 268-286 (§7) | documentation vivante : nom, variables, `-L board` 16 tests | oui (nom, emplacement) |
| noyau | `CLAUDE.md` l. 186 | liste des tests de carte | oui (nom) |
| noyau | `doc/migration/*` (ETAPE-10, MIGRATION-STATUS, handoff, validation-*) | historique de la migration | non (archives datées) |
| lepton-tools | skill `lepton-cibles` | aucune mention du test radio (seulement ports A/B, n° de sondes) | ajout proposé : commande du test radio |
| lepton-tools | `scripts/oracle/*`, `lepton/*.py`, `extension/` | aucune référence ; aucun filtre `-R`/`-E` sur `board.radio` | non |
| lepton-tools | `schemas/exemples/greffon-bsp-nucleo-wl55jc1.json` | exemple de schéma (déjà distinct du manifeste réel) | à trancher (Q6) |
| lepton-tools | `doc/devenv/etapes`, `rapports`, `handoff`, `DEVENV-STATUS.md` | historique | non |

Tâche de l'éditeur « tests des greffons » (`lepton/generate.py` l. 502-512) : créée pour les seules
configurations QEMU (PA-47 Q1 d'ENV-30). Le champ `tests` du BSP WL55 ne crée donc aucune tâche ;
`lepton generate` inchangé pour les configurations de carte. `lepton check` (`checks.py` l. 87-92)
contrôle le répertoire et son `CMakeLists.txt`.

`.gitignore` : le clone du BSP n'en a pas (E1 sans effet) ; seul fichier non suivi : `.DS_Store` à
la racine du clone, hors `scion/`.

## 5. Listes `ctest -N` (référence avant)

Configurations neuves dans le scratchpad de la session (`cmake -S <ROOTSTOCK>/trunk -B <scratch>
--preset <P> …`), sans toucher à `<ROOTSTOCK>/build` :

| Configuration | embOS | FreeRTOS |
| --- | --- | --- |
| banc (A `/dev/cu.usbmodem145103` n° …3937, B `/dev/cu.usbmodem1454403` n° …9937) | 16 | 16 |
| ports fictifs (A, B, sondes fictives) | 16 | 16 |
| port de A seul | 15 (sans `board.radio`) | 15 |
| sans port | 0 | 0 |

Liste à 16, dans l'ordre de déclaration : `board.radio`, `board.smoke_lsh`, `kal.board_flash`,
`kal.T1`…`kal.T8`, `kal.TICI`, `kal.TCLK`, `kal.TSBRK`, `kal.IRQ`, `kal.harness_fail`. Liste
FreeRTOS « banc » identique à celle de `<ROOTSTOCK>/build/nucleo-wl55jc1-freertos` (configurée en
ENV-31). Avertissement FreeRTOS préexistant : `LEPTON_EMBOS_ROOT` non utilisé (variable du preset).

Port de la carte A : `/dev/cu.usbmodem145103` dans le cache d'ENV-31, `/dev/cu.usbmodem1454303`
dans la skill `lepton-cibles` (relevé ENV-11) : les consoles dépendent du port USB ; à relever au
moment du banc.

## 6. Constats

- **R1** — Le déplacement est faisable sans modifier le lecteur (BLD-6 respectée) : variables de
  carte héritées, `LEPTON_TESTS_NOYAU` exposée, `$<TARGET_FILE:lepton>` disponible.
- **R2** — Le nom `board.radio` ne peut pas être conservé avec `lepton_greffon_test` (préfixe imposé).
  Seul usage du nom : la documentation (`BUILDING.md`, `CLAUDE.md`) ; les sélections usuelles passent
  par les étiquettes (`-L board`, `-L radio`), conservables.
- **R3** — Ordre : le test est aujourd'hui déclaré en premier (inclusion du BSP avant
  `firmware.cmake`) ; par `lepton_greffons_tests()`, il le sera en dernier. Avec `RUN_SERIAL`, il
  s'exécutera après le banc KAL au lieu d'avant. Conséquence : liste `ctest -N` identique au nom et
  au rang près ; image finale de A et B = même `lepton.elf` dans les deux cas.
- **R4** — Le déplacement d'un dépôt à l'autre n'est pas un `git mv` : copie dans le BSP (commit
  mécanique citant l'origine `<NOYAU>/tests/board_radio.py` @ 7fe3757), puis `git rm` dans le noyau.
- **R5** — La cfg de la paire et ses deux variables de cache ne servent qu'au test radio ; elles
  peuvent suivre le test dans `tests/CMakeLists.txt` (une variable de cache se déclare aussi dans un
  sous-répertoire). Le chemin `${CMAKE_BINARY_DIR}/openocd-nucleo-wl55jc1-paire.cfg`, cité par
  `BUILDING.md` §7, peut être gardé tel quel.

## 7. Questions du PA-51 (recommandations de la session, non validées)

| Q | Objet | Recommandation |
| --- | --- | --- |
| Q1 | Emplacement | `<BSP-WL>/tests/` (champ `"tests": "tests"`), `tests/CMakeLists.txt` + `tests/radio.py` (script renommé comme le test, modèle an386) |
| Q2 | Accès à `smoke_lsh` | option 1 : `--tests-noyau ${LEPTON_TESTS_NOYAU}`, `sys.path.insert(0, args.tests_noyau)` (modèle `peripheriques.py`) ; aucune copie |
| Q3 | Nom | option 1 : `nucleo-wl55jc1.radio` (lecteur inchangé) ; documentation mise à jour |
| Q4 | Étiquettes | `board`, `radio` conservées ; `greffon:nucleo-wl55jc1`, `arch:`, `backend:` ajoutées par le lecteur ; mêmes propriétés (`TIMEOUT 300`, `RUN_SERIAL`, `PYTHONDONTWRITEBYTECODE=1`), pas de fixture (iso-fonctionnel) |
| Q5 | Script du noyau | retiré (`git rm`) : aucun autre consommateur |
| Q6 | Reste du `CMakeLists.txt` de carte | l. 1-28 (uname, sonde et cfg de A, port de A) ; variables de la paire, cfg de la paire (même chemin) et test dans `tests/CMakeLists.txt` ; journal `${CMAKE_BINARY_DIR}/board_radio.log` gardé. Exemple de schéma `greffon-bsp-nucleo-wl55jc1.json` : ajouter `"tests": "tests"` |
| Q7 | Ordre (R3) | accepté : le test radio passe après le banc KAL |
| Q8 | Cartes disponibles | deux NUCLEO-WL55JC1 seules branchées (piège d'ENV-20) ; ports à relever |
| Q9 | Documents vivants | noyau `BUILDING.md` §7 et `CLAUDE.md` ; skill `lepton-cibles` : ligne « test radio » ; archives de la migration inchangées |

**PA-51 (2026-11-03, décision de l'utilisateur)** : recommandations Q1 à Q9 retenues telles quelles.
