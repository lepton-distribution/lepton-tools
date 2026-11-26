# Étape EP-1 — Greffon de type `projet` dans lepton

## Contexte
C4 : un projet de développement est une graine à dépôt propre qui intègre noyau, famille, BSP,
applications, et un greffon **projet** portant `trunk/sys/user/<projet>/` (XML mklepton, `.boot`,
`.init`, plus tard le fichier de poste ; l'espace reste à la racine du rootstock, C2 révisée au
PA-E1). Ce greffon a un dépôt propre, ou partagé
avec le BSP et les applications. Il **remplace** le `project/` du dépôt de la graine : un seul
concept.

Existant (`CADRAGE.md` §2.1, §2.3, §2.4) :
- `lepton seed new` crée une graine de projet (`depots/lepton-seed/<nom>` ou `--seed-repo`),
  manifeste `lepton-graine.json`, un seul BSP, un seul backend ; son répertoire `project/` est le
  greffon local `lepton@project-<projet>` (version `*`) : presets, XML copié par `--mkconf`,
  `.boot`, `.init` sous `sys/user/<projet>/etc/` ;
- `lepton generate` écrit `CMakeUserPresets.json` dans `project/scion/`, greffé à la racine du
  trunk ;
- types de greffon de `schemas/greffon.schema.json` : `noyau`, `famille`, `bsp`, `application`,
  `bibliotheque` ;
- plusieurs greffons dans un même dépôt : déjà possible (colonne « scion location in depot » de
  `.scion.sources.list` ; option `--origin nom=LOCATION[@VERSION][:PATH]`) ;
- graine de référence : reconnue par « ni `lepton-graine.json` ni `project/` » (PA-19 C
  d'ENV-16) ; les commandes qui modifient la graine y sont refusées (PA-23 d'ENV-18).

Cette étape ne change **que** le porteur des fichiers du projet. L'emplacement de l'espace de
travail reste la racine du rootstock (C2 révisée au PA-E1 ; EP-4 rend l'espace portable). Archétype : infrastructure, avec
contrainte iso-fonctionnelle pour une graine migrée.

## Prérequis
- EP-0 terminée, C2 et C3 confirmées ou révisées au PA-E1.
- lepton 0.1.0, extension 0.5.4, scion 0.6.3.4 ; venv de développement et `pytest` :
  `doc/devenv/DEVENV-STATUS.md` §Versions épinglées (lignes lepton, pytest).
- Skills `lepton-rootstock`, `lepton-oracle`, `lepton-cibles`.
- Branche `espace-projet/ep-1` de lepton-tools. Aucun autre dépôt n'est modifié, sauf le clone
  noyau si le PA-E2 retient de changer son lecteur CMake (tâche 1).

## Tâches

### 1. Audit et conception (lecture seule) → PA-E2
Rapport `doc/espace-projet/rapports/ep-1-type-projet.md`.

Relever :
- chaque endroit de `lepton/` qui crée, lit ou teste `project/`, `lepton@project-`, le greffon
  local, `CMakeUserPresets.json` : `seed new`, `seed mkconf import`, `generate`, `check`,
  `seed status`, `seed tree`, critère de la graine de référence, refus de PA-23 ;
- schémas et exemples : `schemas/greffon.schema.json`, schéma de la graine, `schemas/exemples/`
  (valides et invalides), `scripts/valider-schemas.sh` ;
- les deux lecteurs de manifeste : `lepton/rootstock.py` `find_manifest` ne cherche que sous
  `<clone>/scion/sys/root/src/` ; `scion/cmake/lepton_greffons.cmake` du clone noyau lit tout
  `lepton-greffon.json` sous `sys/root/src` et s'arrête en erreur fatale sur un type hors de
  `LEPTON_GREFFON_TYPES` (`noyau famille bsp application bibliotheque`) ;
- extension (`extension/`), tests (`tests/`), `scripts/bout-en-bout.sh`, `README.md` : ce qui
  dépend de `project/` ;
- le compte de départ de `pytest` ;
- les graines à `project/` existantes : rootstocks d'essai du Mac (`~/lepton-tools-dev/essais/`),
  ceux de la VM d'après `doc/devenv/rapports/env-72-debian.md`, et toute graine de projet publiée
  sur un distant.

Proposer, sans rien modifier :
- manifeste d'un greffon `projet` : champs, emplacement du manifeste dans le greffon (sous
  `sys/user/<projet>/`, lepton ne le trouve pas aujourd'hui ; sous `sys/root/src/`, le lecteur
  CMake du noyau le refuse), et modification ou non du noyau ;
- emplacement du greffon projet dans `lepton-graine.json` (nom de la clé, requis ou non) ;
- interface de `seed new` : dépôt du greffon projet créé ou désigné, emplacement par défaut du
  clone, nom de clé, version ; cas du dépôt partagé avec BSP et applications ;
- `CMakeUserPresets.json` à la racine `scion/` du greffon projet ; cible de `seed mkconf
  import` ; règles de `check` ; affichage de `seed status` et `seed tree` ; messages ;
- critère de la graine de référence réduit à « pas de `lepton-graine.json` » (C4) ;
- T8 : comportement de chaque commande quand un greffon `projet` est greffé sans
  `lepton-graine.json` (régime de référence, cas d'EP-3) : `generate` y écrit-il
  `CMakeUserPresets.json`, quelles commandes de PA-23 restent refusées ;
- sort des graines à `project/` existantes : commande de migration, procédure manuelle avec refus
  explicite de lepton, ou abandon de ces graines. Lire `project/` et le greffon projet côte à
  côte est exclu par C4 ;
- T9 : où consigner les exigences modifiées ;
- versions de lepton et de l'extension après l'étape : `<À CONFIRMER au PA-E2>`.

**PA-E2** : l'utilisateur valide schémas, noms, emplacement du manifeste et sort du lecteur
CMake du noyau, interface, T8, T9, sort des graines existantes, versions. Aucune modification
avant la réponse.

### 2. Schémas et exemples
Tests d'abord. Type `projet` dans `schemas/greffon.schema.json` ; schéma de la graine ; exemples
valides et invalides ; `scripts/valider-schemas.sh` vert. Commit séparé.

### 3. lepton
Tests d'abord, qui échouent sur `main`. Dans l'ordre retenu au PA-E2 : `seed new`, `seed mkconf
import`, `generate` (`CMakeUserPresets.json` seulement), `check`, `seed status`, `seed tree`,
critère de référence. Un commit par commande.

### 4. Extension
Seulement ce que l'audit montre lié à `project/`. Version et `.vsix` selon le PA-E2 ; sinon
l'extension n'est pas touchée.

### 5. Migration et non-régression
- Si le PA-E2 retient une migration : oracle avant (skill `lepton-oracle`) sur une copie, sans
  `build/`, d'un rootstock d'essai à graine de projet, sous `~/lepton-tools-dev/essais/ep-1/` ;
  migrer la copie ; oracle après : binaires identiques ; liste `chemin -> cible` du trunk : mêmes
  chemins, cibles déplacées vers le greffon projet, écarts expliqués un à un.
- Projet neuf par `seed new` : `check` code 0, `generate`, construction et test de fumée QEMU
  (skill `lepton-cibles`).
- Référence, sans greffon projet : dans une même copie de `<ROOTSTOCK>`, `lepton check` code 0,
  puis `generate` par le lepton de `main` et par celui de la branche : `diff` vide.

### 6. Clôture → PA-E3
Essai par l'utilisateur dans VSCodium des commandes de l'extension que l'étape touche
(`lepton.seedMkconfImport`, `lepton.generate`, `lepton.seedStatus`, vue de l'arbre) ; l'extension
n'a pas de commande de création de projet.
**PA-E3** : rapport ; graines migrées ; sort des essais ; fusion et publication (PA-P).

## Critères de validation
- [ ] PA-E2 et PA-E3 tranchés et consignés.
- [ ] `pytest` vert : compte de départ, plus les nouveaux, moins ceux que le PA-E2 inverse (listés).
- [ ] `scripts/valider-schemas.sh` vert ; un greffon `projet` valide et un invalide dans les
      exemples.
- [ ] `grep -rnE 'PROJECT_SUBPATH|project_key|project_stem|graft_project|project/' lepton
      --include='*.py'` : chaque occurrence restante est justifiée dans le rapport.
- [ ] Graine migrée, si le PA-E2 en retient une : binaires identiques à l'oracle avant.
- [ ] Projet neuf : fumée QEMU verte.
- [ ] Copie de `<ROOTSTOCK>` : `check` code 0 ; espace généré par `main` et par la branche
      identiques.
- [ ] `git -C <SEED_SCIONS> status --short` : vide (scion n'est pas touché).

## Pièges connus
- Un manifeste de type `projet` posé sous `sys/root/src/` casse la configuration CMake de tous
  les presets tant que le lecteur du noyau ne connaît pas ce type.
- Le greffon local `lepton@project-<projet>` est en version `*` ; un greffon projet à dépôt
  propre a une version : `graft-update` refuse un clone hors de sa version déclarée
  (`doc/devenv/rapports/env-29-scion.md` §4).
- Une graine désignée par `--seed-repo` n'est pas sous `depots/lepton-seed/` : ne pas déduire
  l'emplacement du greffon projet de celui de la graine.
- La graine de référence d'aujourd'hui n'a ni manifeste ni greffon projet : le critère réduit ne
  doit pas la faire changer de régime.
- Ne pas toucher à `render_workspace` hors de ce qu'impose le changement de porteur : c'est
  EP-4.
- lepton s'essaie par le venv de développement ; le lepton installé par pipx n'est remplacé
  qu'après le PA-E3 (`pipx install --force <LEPTON_TOOLS>`).

## À la fin de l'étape
`STATUS.md` : statut, branche, §Versions (lepton, extension), décisions PA-E2 et PA-E3, journal.
`HORS-PLAN.md` : graines non migrées et tout point écarté. Passation `handoff/ep-1.md`.
