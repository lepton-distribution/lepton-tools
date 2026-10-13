# Étape ENV-5 — Restructuration CMake du greffon noyau

## Contexte
BLD-1 et BLD-2 imposent une structure de construction : bibliothèques statiques `kernel`, `lib`,
`sbin`, `bin`, `bsp`, puis un exécutif ; chaque greffon contribue ses sources par son manifeste
JSON sans modifier les `CMakeLists.txt` du noyau. Cette étape modifie un arbre porté et validé :
archétype migration, non-régression stricte, aucune refactorisation d'opportunité.

## Prérequis
- ENV-3 terminée (schéma de manifeste validé).
- `env-2-cmake.md` : structure actuelle et écarts avec BLD-1.
- CMake ≥ 3.24 (PA-2 Q6). Branche `devenv/env-5` dans le clone noyau.
- Session principale seule ; aucun sous-agent en écriture.

## Tâches

### 1. Oracle — point d'arrêt PA-5
Skill `lepton-oracle`, sur l'état de départ, dans `doc/devenv/rapports/oracles/env-5-avant/` :
- presets QEMU, NUCLEO-F429ZI et NUCLEO-WL55JC1 : capture binaire (§1) ;
- QEMU : test de fumée (`lsh`, `uname -a`) et banc KAL (§3).
Présenter, attendre PA-5.

### 2. Lecteur de manifestes CMake
Module `cmake/lepton_greffons.cmake` (dans le greffon noyau) :
- découvre les manifestes `lepton-greffon.json` (décision 2026-10-13) dans le trunk ;
- lit les champs par `string(JSON …)` ; refuse un manifeste sans champ obligatoire, message citant
  le fichier ;
- ajoute les sources des répertoires déclarés (`file(GLOB … CONFIGURE_DEPENDS)`) à la
  bibliothèque déclarée ;
- applique les options : portée `privee` → `PRIVATE`, `publique` → `PUBLIC` (CFG-3).

### 3. Cibles
- `kernel` (`kernel/`, `kernel/dev/arch`), `lib`, `sbin`, `bin`, `bsp` : bibliothèques statiques.
- Démarrage et vecteurs du BSP : bibliothèque `OBJECT` liée directement à l'exécutif (BLD-1).
- Exécutif : `main` (greffon noyau), table des périphériques et sources générées par mklepton
  (décision 2), lié en premier.
- Sorties ELF, HEX, BIN, MAP, rapport d'occupation par bibliothèque (BLD-4).
- mklepton reste une `add_custom_command`, sorties dans le répertoire de construction (BLD-3).

### 4. Manifeste du greffon noyau
Écrire le manifeste du greffon noyau. Les BSP restent provisoirement là où ils sont : un
manifeste BSP transitoire par carte, sans déplacement de fichiers (le déplacement est ENV-6).

### 5. Non-régression — point d'arrêt PA-6
Rejouer l'oracle dans `env-5-apres/` et comparer (`scripts/oracle/comparer-oracle.py`). Exigé :
test de fumée et banc KAL identiques ; code 0 de la comparaison, ou chaque écart expliqué. Les
empreintes peuvent changer (ordre d'édition de liens). Présenter, attendre PA-6 avant fusion.

## Critères de validation
- [ ] `cmake --build` réussit pour les presets QEMU, NUCLEO-F429ZI et NUCLEO-WL55JC1.
- [ ] Cibles `kernel`, `lib`, `sbin`, `bin`, `bsp` et exécutif visibles (`cmake --build … --target help`).
- [ ] Banc KAL et test de fumée QEMU identiques à l'oracle.
- [ ] Ensemble des symboles de la MAP identique, à l'exception des écarts expliqués.
- [ ] Ajout d'un greffon d'essai (un `.c` + manifeste) compilé sans toucher aux `CMakeLists.txt`
      du noyau (BLD-2), puis retiré.
- [ ] PA-5 et PA-6 tranchés.

## Pièges connus
- Vecteurs dans une archive statique : non référencés, ils sont écartés par l'éditeur de liens ;
  d'où la bibliothèque OBJECT.
- Dépendance croisée `kernel` ↔ `bsp` : la table des périphériques dans l'exécutif l'évite ; si
  une référence croisée subsiste, la signaler plutôt que d'ajouter `--start-group`.
- `file(GLOB)` sur des liens symboliques : vérifier que les chemins produits restent ceux du trunk
  (cohérence avec la décision PA-1).
- Ne modifier que la construction : aucun changement de code C dans cette étape.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, résultats de non-régression, nom du fichier manifeste. Passation
`handoff/env-5.md`.
