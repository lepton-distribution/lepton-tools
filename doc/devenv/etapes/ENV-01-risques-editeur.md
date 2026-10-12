# Étape ENV-1 — Levée des risques éditeur

## Contexte
L'architecture retenue (SPECIFICATION §Architecture) suppose que VSCodium, clangd et GDB
fonctionnent correctement sur un trunk fait de liens symboliques. Trois points ne sont pas
vérifiés. Cette étape les teste par des essais jetables, avant toute conception d'ENV-9. Elle ne
modifie aucun dépôt existant.

## Prérequis
- ENV-0 terminée ; construction QEMU de référence disponible.
- VSCodium installé à la main pour l'essai (ENV-10 automatisera) avec clangd, CMake Tools,
  Cortex-Debug depuis Open VSX ; versions consignées dans le rapport.

## Tâches
Travailler dans `<ROOTSTOCK>/build/essais-env1/` et sur une copie jetable du rootstock si un essai
risque d'écrire dans le trunk. Rapport : `doc/devenv/rapports/env-1-essais.md`.

### 1. clangd et liens symboliques (IDE-3, IDE-4)
- Produire `compile_commands.json` (`-DCMAKE_EXPORT_COMPILE_COMMANDS=ON`).
- Ouvrir le trunk dans VSCodium ; « aller à la définition » sur un symbole du noyau défini dans un
  autre fichier. Relever le chemin ouvert : trunk ou clone.
- Ouvrir le même fichier par l'autre chemin : relever si deux onglets et deux jeux de diagnostics
  existent.
- Refaire l'essai avec un espace de travail multi-racines (un dossier par clone + le trunk).

### 2. Sauvegarde à travers un lien (FIC-5)
Sur la copie jetable : ouvrir un fichier via le trunk, le modifier, sauvegarder. Vérifier
`test -L <chemin trunk>` et la modification dans le clone. Tester aussi les réglages
`files.saveConflictResolution` si le comportement diffère.

### 3. Chemins de débogage
- Construire avec et sans `-ffile-prefix-map=<ROOTSTOCK>/trunk=…`.
- Sous QEMU (`mps2-an386`) avec Cortex-Debug : poser un point d'arrêt depuis un fichier ouvert
  via le trunk, puis via le clone ; relever lequel est atteint.
- Relever la configuration minimale qui fonctionne dans les deux cas (`substitute-path` ou
  préfixe).

### 4. Git multi-dépôts
Vérifier que le panneau source control de VSCodium affiche un dépôt par clone de l'espace de
travail multi-racines et aucun pour le trunk.

### 5. Point d'arrêt PA-1
Présenter le rapport et une recommandation unique par risque : mode d'ouverture des fichiers
(trunk ou clones), réglage clangd, correspondance des chemins de débogage. Attendre la décision.

## Critères de validation
- [ ] Rapport `env-1-essais.md` : pour chaque essai, versions, procédure, résultat observé.
- [ ] Aucun fichier régulier ajouté au trunk réel (`find trunk -type f ! -name .scion.grafted.list` vide).
- [ ] PA-1 tranché et consigné.

## Pièges connus
- clangd met en cache son index (`.cache/clangd`) : le vider entre deux essais.
- Une copie du rootstock par `cp -R` sans `-P` suit les liens et produit un trunk de fichiers
  réguliers : copier avec `cp -RP` (ou `rsync -a`).
- Un essai concluant sur un seul fichier ne prouve rien pour les fichiers générés par mklepton :
  tester aussi un fichier du répertoire de construction.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, décisions PA-1, versions des extensions testées. Passation
`handoff/env-1.md`.
