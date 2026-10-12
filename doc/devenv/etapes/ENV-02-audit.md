# Étape ENV-2 — Audit de l'existant

## Contexte
Les étapes ENV-3 à ENV-8 dépendent de faits non établis : structure CMake actuelle, format et
analyseur du XML mklepton, emplacement du code propre aux cartes, capacités réelles de scion 0.5.
Cette étape les relève en lecture seule et produit les rapports sur lesquels l'utilisateur fixe le
périmètre (PA-2). Aucune modification de code.

## Prérequis
- ENV-0 terminée. Rootstock greffé, clone noyau propre.

## Tâches
Rapports dans `doc/devenv/rapports/`. Lire dans le clone ou le trunk ; ne rien écrire hors de
`lepton-tools`.

### 1. CMake actuel → `env-2-cmake.md`
- Arborescence des `CMakeLists.txt` et des modules `cmake/` ; presets existants.
- Cibles produites (bibliothèques, exécutable), leur liste de sources (glob ou liste), options et
  variables de sélection KAL (`arch` × `backend`).
- Appel de mklepton (`add_custom_command`) : entrées, sorties, répertoire.
- Démarrage, vecteurs, scripts `.ld` : où ils sont, comment ils sont liés.
- Écart avec BLD-1 (bibliothèques `kernel`, `lib`, `sbin`, `bin`, `bsp`, exécutif).

### 2. XML mklepton → `env-2-mklepton.md`
- Analyseur utilisé (bibliothèque ou maison), fichiers sources concernés.
- Liste des fichiers XML de configuration existants et de leurs éléments / attributs (table
  élément × fréquence × fichiers).
- Éléments liés au cœur, à l'architecture, au backend ou aux cibles gelées (ARM7, ARM9, M16C) :
  candidats au retrait (CFG-8).
- Ce que mklepton génère (fichiers C, image UFS) et la table des périphériques (décision 2).

### 3. Code de carte → `env-2-cartes.md`
- Où se trouve aujourd'hui le code propre à chaque carte retenue : QEMU `mps2-an386`,
  NUCLEO-F429ZI, NUCLEO-WL55JC1 (cœur M4). Les trois cartes sont supportées et ont été testées
  pendant le portage : relever les fichiers et la configuration (OpenOCD, sonde) utilisés alors.
- Pour chaque fichier : générique ou propre à la carte. Estimation du volume à extraire (ENV-6).
- Commandes OpenOCD utilisées pendant le portage pour chaque carte (fichiers `interface/…`,
  `target/…`, `board/…`) et version d'OpenOCD correspondante.

### 4. scion 0.5 → `env-2-scion.md`
Pour chaque besoin, dire si scion 0.5.0.1 le couvre (commande exacte) ou non :
ajout / retrait d'un scion dans `.scion.sources.list` ; regreffe d'un seul chemin ; greffon local
hors git ; regreffe idempotente après création de fichier ; suppression propre d'un greffon.

### 5. Scripts et bancs existants → `env-2-outillage.md`
Emplacement et usage de `install-macos.sh`, `install-debian.sh`, du test de fumée QEMU et du banc
KAL (`BANC-TEST-KAL-QEMU.md`) ; commandes exactes pour les lancer.

### 6. Compléter la skill `lepton-cibles`
Remplacer chaque `<RELEVÉ ENV-2>` de `.claude/skills/lepton-cibles/SKILL.md` par la valeur relevée
(preset, exécutable, commande QEMU, commande du banc KAL, fichiers OpenOCD, port série), avec en
commentaire le fichier source de chaque valeur. Commit dédié.

### 7. Point d'arrêt PA-2
Synthèse d'une page : pour ENV-4, ENV-5, ENV-6, ENV-7, périmètre estimé et risques. Attendre la
validation du périmètre.

## Critères de validation
- [ ] Cinq rapports présents, chaque affirmation appuyée par un chemin de fichier ou une commande.
- [ ] Plus aucun `<RELEVÉ ENV-2>` dans la skill `lepton-cibles`.
- [ ] Clone noyau et `seed.scions` inchangés (`git status` propre).
- [ ] PA-2 tranché et consigné.

## Pièges connus
- Lire via le trunk peut donner des chemins trunk ; citer les chemins relatifs à `sys/root/` pour
  qu'ils valent dans les deux vues.
- Les projets `prj/iar`, `prj/scons`, `prj/vc-2010` ne font plus foi : ne pas en déduire la
  structure actuelle.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, périmètres validés pour ENV-4 à ENV-7. Passation `handoff/env-2.md`.
