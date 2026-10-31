# Étape ENV-27 — TST-2 : tests fournis par un greffon

## Contexte
L'exigence TST-2 de `SPECIFICATION.md` (P2) prévoit qu'un greffon puisse fournir ses propres
tests, découverts sans configuration supplémentaire. Critère : « Tests du greffon exécutés ».

Aujourd'hui, tous les tests sont dans le greffon noyau, sous `scion/tests/` du clone noyau :
- `host/` : tests de mklepton, ufs, vfs ;
- `kal/` ;
- scripts `smoke_lsh.py`, `board_net.py`, `board_radio.py`, `endurance_board.py`,
  `kal_openocd.py`, `net_qemu.py`.

Ils sont déclarés à CTest avec des étiquettes (`kal`, `board`). Le lecteur des manifestes,
`scion/cmake/lepton_greffons.cmake`, ne découvre aucun test.

Cette étape ajoute la découverte des tests des greffons. Archétype : création. Les tests
existants et les binaires restent inchangés.

## Prérequis
- ENV-26 terminée : le schéma du greffon peut être modifié par les deux étapes.
- Schéma `schemas/greffon.schema.json` ; lecteur `lepton_greffons.cmake`. Les ajouts de cartes
  ont été faits sans modifier le système de construction commun (BLD-6, ENV-19 et ENV-20) : une
  modification du lecteur est ici attendue, mais doit être bornée.
- Skills `lepton-rootstock`, `lepton-oracle` et `lepton-cibles`.
- Branches `devenv/env-27` : lepton-tools, clone noyau, et le greffon d'essai.

## Tâches

### 1. Audit (lecture seule) → PA-41
- Déclaration actuelle des tests :
  - `add_test`, étiquettes, fixtures (`board_t0`) ;
  - presets de test de `CMakePresets.json` ;
  - différence entre les tests hôte (preset `host`), QEMU et carte.
- Liste des tests (`ctest --preset <P> -N`) pour host, un preset QEMU et un preset de carte : ce
  sera la référence avant.
- Tests du noyau propres à une carte ou à une famille, candidats à un déplacement :
  `board_radio.py` (WL55), `board_net.py`, par exemple. Les relever, sans rien déplacer.
- Formes possibles de la découverte :
  - convention de répertoire (`tests/` dans la destination du greffon) ;
  - champ du manifeste ;
  - fichier CMake inclus par le lecteur.
- Modèles de `lepton scion new` (`lepton/templates/`) : un squelette de test est-il utile ?
- Rapport `rapports/env-27-tst2.md`.
- **PA-41** : l'utilisateur valide :
  - la forme de la découverte et toute modification du schéma ;
  - les types de tests pris en charge (hôte, QEMU, carte) et leurs étiquettes ;
  - le greffon d'essai et ses tests : <À CONFIRMER au PA-41 : test nouveau, ou déplacement d'un
    test de carte du noyau vers son BSP> ;
  - le squelette dans les modèles de `scion new` : <À CONFIRMER au PA-41>.
- Aucune modification avant la réponse.

### 2. Oracle avant
Skill `lepton-oracle` : host et les 16 presets → `rapports/oracles/env-27-avant/`. Y ajouter la
liste `ctest -N` de chaque preset.

### 3. Implémentation
- Clone noyau : découverte dans `lepton_greffons.cmake`, selon le PA-41 ; commits séparés et
  commentaires au niveau du code voisin.
- lepton-tools : schéma, exemples valides et invalides (`scripts/valider-schemas.sh`), `lepton
  check`, modèles. Tests de lepton écrits d'abord ; `pytest` vert.
- Greffon d'essai : tests et manifeste ; `scion graft` sur une copie d'essai, puis sur
  `<ROOTSTOCK>`.

### 4. Contrôles → PA-42
- Oracle après : `comparer-oracle.py` code 0 sur host et les 16 presets (binaires inchangés).
- Listes `ctest -N` : celles d'avant, plus les seuls tests du greffon d'essai, dans les presets
  qui le greffent.
- Les tests du greffon s'exécutent et passent : QEMU, ou carte si le PA-41 le prévoit.
- Un rootstock sans le greffon d'essai : listes `ctest -N` inchangées.
- `lepton check` code 0.
- **PA-42** : rapport ; push et fusions (PA-P). La validation Debian est reportée à ENV-28.

## Critères de validation
- [ ] PA-41 et PA-42 tranchés et consignés.
- [ ] Tests du greffon d'essai découverts sans configuration de la graine, et exécutés avec
      succès.
- [ ] `comparer-oracle.py` code 0 sur 17 constructions ; tests existants inchangés.
- [ ] Modification du lecteur limitée à la découverte : constat dans le rapport (BLD-6).

## Pièges connus
- `ctest -L kal -FS board_t0` sélectionne encore `board.smoke_lsh` (étiquette `kal`) : ajouter
  `-E board.smoke_lsh`.
- Un test `.py` écrit dans un greffon est greffé en lien : son répertoire de travail et ses
  chemins relatifs se résolvent depuis le trunk, pas depuis le clone.
- Les fichiers ignorés par git ne sont plus greffés (E1) : vérifier le `.gitignore` du greffon
  d'essai.
- Les tests de la migration (`doc/migration/`) sont figés (PA-15) : ne pas les déplacer.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, branches, décisions PA-41 et PA-42, journal. Passation
`handoff/env-27.md`.
