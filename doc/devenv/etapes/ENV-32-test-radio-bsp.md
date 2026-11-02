# Étape ENV-32 — Test `board.radio` fourni par le BSP `nucleo-wl55jc1`

## Contexte
ENV-27 a réalisé TST-2 : un greffon déclare ses tests par le champ `tests` de son manifeste, et
`lepton_greffon_test` les déclare à CTest. Le rapport d'ENV-27 (`rapports/env-27-tst2.md` §3) a
relevé `board.radio` comme le seul test propre à une carte. Il a été laissé en place.

État actuel :
- Le script `tests/board_radio.py` est dans le greffon noyau. Il importe `smoke_lsh` du noyau
  par `os.path.realpath(__file__)` (K4).
- Le test est déclaré par le `CMakeLists.txt` facultatif du BSP, inclus par `include()` (K1).
- Il exige deux NUCLEO-WL55JC1 : `LEPTON_BOARD_SERIAL_PORT`, `LEPTON_RADIO_PEER_STLINK_SERIAL`
  et `LEPTON_RADIO_PEER_SERIAL_PORT`.

Cette étape fait du BSP le fournisseur de son test, par le mécanisme de TST-2. C'est le premier
test de carte fourni par un greffon. Archétype : déplacement iso-fonctionnel. Les binaires sont
inchangés, et le test reste le même (même scénario, même résultat sur les deux cartes).

## Prérequis
- ENV-28 terminée. ENV-30 conseillée avant : selon son PA-47, la tâche « tests des greffons »
  couvre aussi les configurations de carte.
- Clone du BSP : `<ROOTSTOCK>/depots/lepton/bsp-nucleo-wl55jc1/master`, `master` c9183de. Fichiers
  `scion/sys/root/src/kernel/dev/bsp/nucleo-wl55jc1/CMakeLists.txt` et `lepton-greffon.json`.
- Clone noyau : `scion/tests/board_radio.py`, `scion/tests/smoke_lsh.py` ; lecteur
  `scion/cmake/lepton_greffons.cmake`. Variable `LEPTON_TESTS_NOYAU` : vérifier au §1 qu'elle est
  exposée, comme le proposait ENV-27 §4.
- Banc radio d'ENV-24 : deux NUCLEO-WL55JC1, sondes et consoles décrites dans
  `rapports/env-24-cpufs.md`, test vert (16/16 avec la radio).
- Skills `lepton-rootstock`, `lepton-oracle` et `lepton-cibles`.
- Branches `devenv/env-32` : lepton-tools, clone noyau, `bsp-nucleo-wl55jc1`.

## Tâches

### 1. Audit (lecture seule) → PA-51
- Déclaration actuelle de `board.radio`, dans le `CMakeLists.txt` du BSP : variables de cache,
  configurations OpenOCD générées (carte et paire), étiquettes (`board;radio;…`), propriétés.
- Dépendances du script : `smoke_lsh` et autres imports ; chemins résolus depuis le trunk.
- Contexte offert par le lecteur aux tests des greffons : `LEPTON_GREFFON_TEST_NOM`,
  `LEPTON_TESTS_NOYAU`, fixture `board_t0`.
- Références à `board.radio` et `board_radio.py` : skill `lepton-cibles`, documentation du noyau,
  rapports vivants, tâches de l'éditeur, scripts `scripts/oracle/`.
- Listes `ctest -N` des presets WL55 (embOS, FreeRTOS), configurés avec les ports du banc et avec
  des ports fictifs : ce sera la référence avant.
- Rapport `rapports/env-32-radio.md`.
- **PA-51** : l'utilisateur valide :
  - Emplacement du script dans le BSP (répertoire du champ `tests`) : <À CONFIRMER au PA-51>.
  - Accès à `smoke_lsh` : <À CONFIRMER au PA-51>.
    - Option 1 : `LEPTON_TESTS_NOYAU` passé au script.
    - Option 2 : copie dans le BSP. Elle duplique un mécanisme : à éviter.
  - Nom du test : <À CONFIRMER au PA-51>.
    - Option 1 : `nucleo-wl55jc1.radio`, préfixe imposé par `lepton_greffon_test`.
    - Option 2 : `board.radio` conservé.
    - Conséquence à mesurer : les filtres `-R`/`-E` des scripts et de la documentation.
  - Étiquettes conservées (`board`, `radio`) en plus de `greffon:nucleo-wl55jc1`.
  - Sort du script dans le noyau : retiré, ou conservé le temps d'une transition.
  - Ce qui reste dans le `CMakeLists.txt` du BSP : paramètres de carte (K1).
  - Cartes disponibles (deux WL55) : <À CONFIRMER au PA-51>.
- Aucune modification avant la réponse.

### 2. Oracle avant
Skill `lepton-oracle` : les presets WL55 (embOS, FreeRTOS) et `host` →
`rapports/oracles/env-32-avant/`, listes `ctest -N` comprises. Conforme au dernier oracle
« après » (ENV-31 si elle précède, sinon `env-27-apres`).

### 3. Implémentation
- BSP `nucleo-wl55jc1` : répertoire de tests, `CMakeLists.txt` qui appelle `lepton_greffon_test`,
  script, champ `tests` du manifeste. Retirer la déclaration du `CMakeLists.txt` de carte.
- Clone noyau, selon le PA-51 : `board_radio.py` retiré, et références mises à jour. Le lecteur
  reste inchangé ; sinon, c'est un arrêt (BLD-6).
- lepton-tools : skill `lepton-cibles` et documents vivants, selon le relevé du §1.
- Commits séparés : déplacement mécanique d'abord, puis adaptations.
- `scion graft` sur une copie d'essai, puis sur `<ROOTSTOCK>` (PA-P).

### 4. Contrôles → PA-52
- Oracle après : `comparer-oracle.py` code 0 sur host et les 16 presets (binaires inchangés).
- Listes `ctest -N` des presets WL55 : identiques à celles d'avant, au nom près si le PA-51 le
  renomme. Ailleurs : inchangées.
- Banc radio (`lepton-cibles`), deux cartes : test radio vert en embOS et en FreeRTOS, mêmes
  comptes qu'en ENV-24 (16/16).
- `ctest -L greffon:` sur un preset WL55 configuré avec le banc : sélectionne le test radio.
- `lepton check` code 0 ; aucun lien cassé ni fichier régulier dans le trunk.
- **PA-52** : rapport ; push et fusions des branches `devenv/env-32` (PA-P). La validation Debian
  est reportée à ENV-33 (découverte seulement : pas de carte sur la VM).

## Critères de validation
- [ ] PA-51 et PA-52 tranchés et consignés.
- [ ] Le test radio est déclaré par le BSP (champ `tests`), plus par le noyau ni par
      `include()`.
- [ ] Banc radio vert sur deux cartes, embOS et FreeRTOS ; binaires identiques (code 0).
- [ ] Aucune copie de `smoke_lsh.py` hors du noyau, sauf décision contraire au PA-51.

## Pièges connus
- Un script déplacé dans un autre greffon ne trouve plus `smoke_lsh` par `realpath` : le lien du
  trunk mène au clone du BSP (K4).
- `ctest -L board` prend la première sonde ST-LINK : brancher seulement les deux WL55, et
  débrancher les autres cartes (décision d'ENV-20).
- `ctest -L kal -FS board_t0` sélectionne encore `board.smoke_lsh` : ajouter
  `-E board.smoke_lsh`.
- Le `CMakeLists.txt` de carte est inclus avant `enable_testing()` (K1), alors que le répertoire
  `tests` est ajouté après `components/firmware`. Vérifier que les configurations OpenOCD
  générées par le BSP existent toujours au moment de déclarer le test.
- Les fichiers ignorés par git ne sont pas greffés (E1) : vérifier le `.gitignore` du BSP.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, branches, décisions PA-51 et PA-52, journal. Passation
`handoff/env-32.md`.
