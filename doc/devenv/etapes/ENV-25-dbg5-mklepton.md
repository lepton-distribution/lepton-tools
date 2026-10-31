# Étape ENV-25 — DBG-5 : déboguer `mklepton` sur l'hôte

## Contexte
L'exigence DBG-5 de `SPECIFICATION.md` (P2), « Déboguer `mklepton` sur l'hôte », a pour
critère « Arrêt dans `mklepton` ». Elle n'est pas couverte aujourd'hui.

État actuel :
- `mklepton` est construit par le preset `host` du noyau (`CMAKE_BUILD_TYPE` `Debug`) et
  utilisé par les presets croisés (`LEPTON_MKLEPTON` = `${sourceDir}/../build/host/mklepton`).
- `lepton generate` n'écrit que des lancements `cortex-debug` (cible), dans
  `lepton/generate.py`.
- Les débogueurs hôtes sont installés : CodeLLDB 1.12.3 sur le Mac (`scripts/extensions.lst`),
  gdb sur Debian.

Cette étape ajoute un lancement hôte de `mklepton` aux fichiers générés. Archétype : création
(fonction nouvelle de lepton) ; les fichiers générés existants restent inchangés en dehors du
lancement ajouté.

## Prérequis
- ENV-22 terminée.
- Fichiers de l'éditeur : `rapports/env-9-generation.md`, `rapports/env-8-interface.md` §16
  (graine de référence, ENV-18).
- Skill `lepton-cibles`.
- Branche `devenv/env-25` dans lepton-tools. Dans le clone noyau seulement si le PA-37 l'exige.

## Tâches

### 1. Audit (lecture seule) → PA-37
- Invocation réelle de `mklepton` par la construction : commande CMake, arguments, XML, répertoire
  de travail et sorties. Source : `ninja -C <ROOTSTOCK>/build/<preset> -t commands`, pour un
  preset QEMU et un preset de carte.
- Informations de débogage de `build/host/mklepton` (`Debug`, `-g`) et chemins des sources dans
  le DWARF : clone ou trunk (comparaison avec F8 d'ENV-12).
- Débogueur par hôte :
  - Mac : CodeLLDB (`type` `lldb`) ;
  - Debian : gdb (`type` à établir, extension disponible ou non dans `scripts/extensions.lst`).
- Espaces concernés : graine de projet, et graine de référence (`original-tree.code-workspace`).
- **PA-37** : l'utilisateur valide :
  - le nom et le nombre des lancements (un par XML du preset actif, ou un seul) : <À CONFIRMER au
    PA-37> ;
  - les arguments : ceux de la construction, ou une sortie vers un répertoire temporaire pour ne
    pas écraser la construction : <À CONFIRMER au PA-37> ;
  - le débogueur Debian et l'ajout éventuel d'une extension à `scripts/extensions.lst` (PA-10) ;
  - la tâche préalable : construction du preset `host` avant le lancement ;
  - la conduite si `build/host/mklepton` est absent : lancement écrit quand même, ou ligne
    d'information.
- Aucune modification avant la réponse.

### 2. Implémentation (lepton-tools)
- `lepton/generate.py` : lancement hôte et tâche préalable, selon le PA-37.
- Tests de lepton : écrire d'abord les tests du lancement ajouté (graine de projet et graine de
  référence). Les 216 tests existants restent verts.
- `rapports/env-8-interface.md` : section consacrée à DBG-5.
- `pipx install --force <LEPTON_TOOLS>`, à partir de `devenv/env-25`.

### 3. Contrôles → PA-38
- Graines de projet des rootstocks d'essai et `<ROOTSTOCK>` : `lepton generate`, code 0.
  Régénérer avant le relevé (E-1 d'ENV-21), puis faire le `diff` des fichiers générés contre le
  relevé : seul le lancement ajouté diffère.
- Essai VSCodium sur le Mac : point d'arrêt dans `main` de `mklepton`, arrêt atteint, variables
  lisibles (essai fait par l'utilisateur, comme en ENV-12).
- Aucune modification de binaire de cible (fichiers de construction non touchés) : constat.
- **PA-38** : rapport `rapports/env-25-dbg5.md` ; fusion et push (PA-P). L'essai Debian est
  reporté à ENV-28.

## Critères de validation
- [ ] PA-37 et PA-38 tranchés et consignés.
- [ ] `pytest` vert, nouveaux tests compris.
- [ ] Fichiers générés : `diff` limité au lancement et à la tâche ajoutés.
- [ ] Arrêt dans `mklepton` constaté sous VSCodium (Mac).

## Pièges connus
- `mklepton` lancé avec les sorties de la construction écrase les fichiers générés d'un preset :
  la reconstruction suivante les régénère, mais un essai peut fausser un oracle en cours.
- Chemins DWARF : un point d'arrêt posé dans le trunk peut ne pas correspondre au chemin du
  clone résolu par le débogueur (F8 d'ENV-12, correspondance faite par l'extension pour
  Cortex-Debug seulement).
- Ne pas confondre le gdb de l'éditeur (`arm-none-eabi-gdb`, cible) avec le débogueur hôte.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, branche, §Versions (lepton réinstallé), décisions PA-37 et PA-38,
journal. Passation `handoff/env-25.md`.
