# Étape EP-6 — Sondes par carte

## Contexte
Axe 4 (`CADRAGE.md` §1, §3) : avec plusieurs sondes branchées, une par carte, l'interface est
choisie par carte et mémorisée, ou demandée au lancement comme IAR le fait quand plusieurs sondes
répondent.

Existant (`CADRAGE.md` §2.1 ; `doc/devenv/DEVENV-STATUS.md` §Emplacements, ligne « Sondes des
cartes (ENV-45) ») : un seul numéro de série pour toutes les configurations carte de l'espace
(`lepton.probeSerial`, `lepton generate --probe-serial <n°>`), à redonner séparément à CMake
(`-DLEPTON_BOARD_PROBE_SERIAL=<n°>`, lecteur du noyau `cmake/lepton_greffons.cmake`,
`_lepton_sonde_cfg`, cfg générée `<build>/openocd-<bsp>.cfg`).

Les directions de `CADRAGE.md` §6 « Sondes » sont des propositions : numéro de série par carte
dans le fichier de poste, lu par `generate` et par le lecteur CMake du noyau ; à défaut, choix au
lancement par une commande de l'extension qui mémorise ; `lepton probe list` et `lepton probe
set` en ligne de commande (NF-1). Le numéro de série est une valeur de **poste** : il ne paraît
dans aucun fichier versionné. Archétype : infrastructure.

## Prérequis
- EP-5 terminée et publiée.
- Fichier de poste d'EP-4 (nom, schéma, portée retenus au PA-E8).
- Cartes et numéros de série connus : `doc/devenv/DEVENV-STATUS.md` §Emplacements, ligne
  « Sondes des cartes (ENV-45) » (NUCLEO-F429ZI, STM32F746G-DISCO, SAMD21 Xplained Pro,
  NUCLEO-WL55JC1 A et B). Présence sur table : à confirmer au plan de session.
- Skills `lepton-cibles`, `lepton-rootstock`, `lepton-oracle`.
- Branches `espace-projet/ep-6` : lepton-tools, clone noyau.

## Tâches

### 1. Audit et conception (lecture seule) → PA-E12
Rapport `doc/espace-projet/rapports/ep-6-sondes.md`.

Relever :
- tous les lecteurs du numéro de série : `generate`, réglage `lepton.probeSerial`, extension,
  lecteur CMake du noyau, tâches de flash, scripts de banc (`tests/` du noyau, bancs d'ENV) ;
- comment lister les sondes connectées sur macOS et sur Debian (OpenOCD, `system_profiler`,
  `lsusb`), et ce que chaque moyen rend pour ST-LINK/V2-1, STLINK-V3 et EDBG ;
- le comportement actuel d'OpenOCD avec plusieurs sondes sans numéro de série.

Proposer, sans rien modifier :
- la clé du réglage dans le fichier de poste. T7 : `sondes: {<bsp>: <série>}` ne distingue pas
  les deux NUCLEO-WL55JC1 (A et B, même BSP) ;
- source unique : comment le lecteur CMake du noyau obtient le numéro (lecture du fichier de
  poste, variable écrite par `generate`), sans que le noyau dépende de la forme d'un projet ;
- sort de `-DLEPTON_BOARD_PROBE_SERIAL` et de `--probe-serial` : conservés en surcharge, ou
  retirés ; sort du réglage `lepton.probeSerial` ;
- `lepton probe list` et `lepton probe set` : sortie, codes de retour ;
- choix au lancement : commande de l'extension servie par un `inputs` de type `command`,
  mémorisation ; cas d'aucune sonde, d'une seule, de plusieurs, d'une sonde mémorisée absente ;
- versions de lepton et de l'extension : `<À CONFIRMER au PA-E12>`.

**PA-E12** : l'utilisateur valide. Aucune modification avant la réponse.

### 2. Implémentation
Seulement ce que le PA-E12 retient. Tests d'abord (listes de sondes simulées : aucun test de
`pytest` ne dépend d'un matériel branché). Commits séparés, selon le PA-E12 : schéma du fichier
de poste ; `lepton probe` ; `generate` ; lecteur CMake du noyau (clone noyau, skill
`lepton-rootstock`) ; extension (version à part).

### 3. Validation à plusieurs sondes → PA-E13
Avant la première écriture flash : accord explicite de l'utilisateur, consigné (premier temps du
PA-E13). Cartes disponibles branchées **en même temps**. Relever, pour ce que le PA-E12 a
retenu :
- liste des sondes (`lepton probe list`) : chaque sonde, son type, son numéro ;
- sonde mémorisée par carte : chaque configuration de débogage et chaque tâche de flash atteint
  sa carte, sans question ;
- sans sonde mémorisée : choix demandé au lancement, mémorisé ou non ;
- flash par CMake : même sonde que le débogage, par la source unique retenue ;
- les deux NUCLEO-WL55JC1, si elles sont disponibles : chacune atteinte selon le PA-E12.
Non-régression : une seule carte branchée, aucun numéro mémorisé : comportement d'EP-5.
Oracle (skill `lepton-oracle`) : binaires identiques avant et après la modification du lecteur
CMake.

### 4. Clôture
**PA-E13** (second temps) : rapport ; sort des essais ; fusion et publication (PA-P) :
lepton-tools, noyau.

## Critères de validation
- [ ] PA-E12 et PA-E13 tranchés et consignés ; autorisation de flash consignée.
- [ ] Plusieurs sondes branchées : chaque configuration atteint sa carte ; preuve par carte dans
      le rapport.
- [ ] Un seul endroit où saisir le numéro de série d'une carte, lu par le débogage et par le
      flash.
- [ ] Aucun numéro de série ajouté à un fichier versionné : `git diff <départ> | grep -c <série>`
      → 0 dans lepton-tools, le greffon projet, la graine et le noyau (`doc/migration/` du noyau
      en porte déjà).
- [ ] Binaires identiques à l'oracle avant.
- [ ] `pytest` vert sans matériel branché ; `scripts/valider-schemas.sh` vert.

## Pièges connus
- Les numéros de série de `DEVENV-STATUS.md` datent du 2026-11-10 : les relever au banc.
- Deux STLINK-V3 identiques ne se distinguent que par le numéro de série.
- `system_profiler` n'existe pas sur Debian, `lsusb` peut manquer sur macOS : la liste des sondes
  a un moyen par hôte ; la preuve Debian relève d'EP-8, si des cartes passent par la VM.
- Le noyau reste utilisable sans lepton : le lecteur CMake garde un moyen de recevoir le numéro
  quand aucun fichier de poste n'existe.
- NUCLEO-F429ZI : Ethernet muet possible (D12 du hors-plan d'ENV).
- Clone noyau sur `espace-projet/ep-6` : `graft-update` le refuse jusqu'à la fusion dans `master`.

## À la fin de l'étape
`STATUS.md` : statut, branches, §Versions, décisions PA-E12 et PA-E13, journal. `HORS-PLAN.md` :
tout point écarté. Passation `handoff/ep-6.md`.
