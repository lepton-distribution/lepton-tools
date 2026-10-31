# Étape ENV-26 — DBG-4 : vues des périphériques et des tâches

## Contexte
L'exigence DBG-4 de `SPECIFICATION.md` (P2) demande deux vues :
- les périphériques, à partir du fichier SVD du MCU déclaré par le BSP ;
- les tâches embOS.

Critère : « Registres périphériques lisibles ».

Côté outils, le schéma du greffon (`schemas/greffon.schema.json`, GRF-3) prévoit déjà un champ
`svd`, contrôlé par `lepton check` (`checks.py`, `SINGLE_FILE_FIELDS`). `lepton generate` écrit
`svdFile` dans les lancements quand le BSP le déclare (`generate.py`). Les extensions
peripheral-viewer 1.6.4 et rtos-views 0.0.16 sont installées. En revanche, aucun BSP ne déclare
de `svd` : DBG-4 est « non vérifiable » dans `rapports/env-12-bilan.md`.

Cette étape fournit les fichiers SVD et la vue des tâches, puis valide les deux sur carte.
Archétype : création ; les binaires des cibles restent inchangés.

## Prérequis
- ENV-25 terminée : `generate.py` est modifié par les deux étapes.
- Greffons famille et BSP des cartes : clones `<ROOTSTOCK>/depots/lepton/<clé>/master`.
- Skills `lepton-rootstock` et `lepton-cibles`.
- Branches `devenv/env-26` : lepton-tools, et chaque greffon qui reçoit un SVD.

## Tâches

### 1. Audit (lecture seule) → PA-39
- Fichiers SVD par MCU : STM32F429, STM32F439, STM32F746, STM32WL55 (cœur M4), SAMD21.
  - Source officielle : ST, Microchip, paquets CMSIS.
  - Licence et conditions de redistribution dans un dépôt public.
  - Version et taille.
  - Ne reprendre aucune URL ni licence de mémoire : citer la source consultée.
- Emplacement du SVD : famille (un fichier par MCU, comme la règle PA-2 Q3 des tables de
  vecteurs) ou BSP. Le champ `svd` étant porté par le BSP, établir comment un BSP désigne un
  fichier de sa famille.
- Vue des tâches :
  - prise en charge d'embOS et de FreeRTOS par OpenOCD 0.12.0 (`rtos`) et par Cortex-Debug
    1.13.0-pre6 ;
  - symboles requis dans les images embOS de Lepton (paquet Segger 5.20.0.0) ;
  - champ du lancement à écrire.
- QEMU : intérêt d'un SVD pour `mps2-an386`/`an500`, <À CONFIRMER au PA-39>.
- Rapport `rapports/env-26-dbg4.md`.
- **PA-39** : l'utilisateur valide :
  - les SVD retenus, leur source et leur licence ; si la licence interdit la redistribution, la
    conduite à tenir : <À CONFIRMER au PA-39 : téléchargement à l'installation, ou abandon pour
    ce MCU> ;
  - l'emplacement (famille ou BSP) et la forme du champ `svd` ; toute modification du schéma
    passe par ce point ;
  - la vue des tâches : embOS seul (exigence), ou embOS et FreeRTOS ;
  - les cartes disponibles pour l'essai : <À CONFIRMER au PA-39>.
- Aucune modification avant la réponse.

### 2. Implémentation
- Greffons : ajouter le fichier SVD et le champ `svd` du manifeste ; `check-jsonschema` passe.
- `scion graft` : copie d'essai d'abord, puis `<ROOTSTOCK>`.
- lepton (`generate.py`) : champ de la vue des tâches dans les lancements de carte ; tests écrits
  d'abord ; `pytest` vert ; `pipx install --force`.
- Graine `original-tree` : à modifier seulement si un greffon nouveau est créé (non prévu).

### 3. Contrôles → PA-40
- `lepton check` code 0 sur `<ROOTSTOCK>` : nombre de fichiers conformes relevé.
- `lepton generate` code 0 : `svdFile` présent dans les lancements des cartes retenues.
- Oracle partiel des presets de carte : symboles identiques (les SVD et les manifestes ne
  changent pas les binaires).
- Essai VSCodium sur chaque carte accordée, fait par l'utilisateur :
  - un registre de périphérique est lisible (par exemple `RCC` ou `GPIOx`) ;
  - la liste des tâches embOS s'affiche à l'arrêt.
- **PA-40** : rapport ; push des greffons et des branches ; fusions (PA-P).

## Critères de validation
- [ ] PA-39 et PA-40 tranchés et consignés.
- [ ] Un SVD déclaré par chaque BSP retenu ; `lepton check` code 0.
- [ ] Registres lisibles et vue des tâches embOS constatés sur au moins une carte, sous VSCodium.
- [ ] Symboles des presets de carte inchangés.

## Pièges connus
- Les fichiers SVD sont volumineux (plusieurs Mo pour un STM32) : vérifier les limites des dépôts
  et le `.gitignore` (les fichiers ignorés ne sont pas greffés depuis scion 0.5.2.0, E1).
- NUCLEO-WL55JC1 : le SVD décrit les deux cœurs, mais seul le M4 est utilisé (DBG-3).
- `ctest -L board` et OpenOCD prennent la première sonde ST-LINK : brancher une seule carte ST.
- En-têtes ST en Latin-1 : utiliser `LC_ALL=C grep -a`.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, branches, emplacements (SVD), décisions PA-39 et PA-40, journal.
Passation `handoff/env-26.md`.
