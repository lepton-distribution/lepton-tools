# Étape EP-5 — Débogage : serveur et interface par configuration

## Contexte
Axe 3 (`CADRAGE.md` §1, §3) : choisir dans VSCodium le serveur de débogage (OpenOCD, J-Link…) et
le modèle de sonde (ST-LINK, Segger, CMSIS-DAP…), comme la page « Debugger » d'IAR Embedded
Workbench (C1).

Existant (`CADRAGE.md` §2.1, §2.4) : `generate` émet une configuration Cortex-Debug par
configuration du projet, `servertype` `qemu` ou `openocd` seulement, `configFiles` = champ
`openocd` du BSP, plus le SVD. Un BSP déclare `openocd` + `sonde` (`stlink` | `jlink` |
`cmsis-dap`, GRF-3), ou `qemu` ; le champ `sonde` n'est **jamais lu** par `generate`.

C9 : J-Link est différé (H1). Le schéma garde `jlink` ; le chantier valide **OpenOCD avec
ST-LINK et CMSIS-DAP**. Les directions de `CADRAGE.md` §6 « Débogage » sont des propositions.
Le numéro de série et le choix entre plusieurs sondes branchées ne sont pas de cette étape
(EP-6) : ici, une seule carte branchée à la fois. Archétype : infrastructure.

## Prérequis
- EP-4 terminée et publiée (espace portable, fichier de poste).
- Cartes et sondes : `doc/devenv/DEVENV-STATUS.md` §Emplacements, ligne « Sondes des cartes
  (ENV-45) » : NUCLEO-F429ZI et STM32F746G-DISCO (ST-LINK/V2-1), NUCLEO-WL55JC1 (STLINK-V3),
  SAMD21 Xplained Pro (EDBG). Présence sur table : à confirmer au plan de session.
- OpenOCD 0.12.0, Cortex-Debug : `doc/devenv/DEVENV-STATUS.md` §Versions épinglées.
- Skills `lepton-cibles` (flash, débogage), `lepton-rootstock`, `lepton-oracle`.
- Branche `espace-projet/ep-5` de lepton-tools ; des clones BSP et du clone noyau selon le PA-E10.

## Tâches

### 1. Audit et conception (lecture seule) → PA-E10
Rapport `doc/espace-projet/rapports/ep-5-debogage.md`.

Relever :
- pour chacun des 7 BSP (5 portent `openocd` et `sonde`, 2 `qemu`) : champs du manifeste ;
  contenu du fichier cfg, lignes d'interface et lignes de cible séparées ;
- ce que le lecteur CMake du noyau fait du cfg pour le flash (`cmake/lepton_greffons.cmake`,
  `_lepton_sonde_cfg`, cfg générée `<build>/openocd-<bsp>.cfg`) : débogage et flash doivent
  rester cohérents ;
- les `servertype` et options de la version épinglée de Cortex-Debug ;
- les configurations `launch` et les tâches de flash actuellement émises.

Proposer, sans rien modifier :
- où se règlent serveur et interface : graine (`configurations[].debug`), fichier de poste,
  choix au lancement ; et comment le choix se fait « dans VSCodium » (commande de l'extension,
  liste de configurations, `${input:…}`) ;
- ce que `generate` émet : une configuration par serveur admis, ou une seule paramétrée ;
- rôle du champ `sonde` du BSP (liste des sondes admises) ; cfg OpenOCD scindée en cible et
  interface, ou interface substituée sans toucher aux BSP ;
- T3 : si les manifestes ou les cfg des BSP changent, la liste des dépôts touchés (schéma, BSP
  publiés, lecteur du noyau), la compatibilité avec les rootstocks restés à l'ancienne version
  des BSP, l'ordre de publication ;
- serveurs autres qu'OpenOCD (`stlink`, `pyocd` de Cortex-Debug) : dans le périmètre ou hors
  plan : `<À CONFIRMER au PA-E10>` ;
- T6 : configuration `jlink` émise sans validation, émise avec une marque, ou non émise ;
- versions de lepton et de l'extension : `<À CONFIRMER au PA-E10>`.

**PA-E10** : l'utilisateur valide. Aucune modification avant la réponse.

### 2. Implémentation
Tests d'abord. Commits séparés : schémas ; `generate` ; extension (version à part) ; BSP et
lecteur du noyau seulement si le PA-E10 les retient (un commit par dépôt, skill
`lepton-rootstock`). Les configurations QEMU ne changent pas.

### 3. Validation sur cartes → PA-E11
Avant la première écriture flash : accord explicite de l'utilisateur, consigné (premier temps du
PA-E11). Une carte branchée à la fois.
Par carte et par interface retenue (ST-LINK : NUCLEO-F429ZI, STM32F746G-DISCO, NUCLEO-WL55JC1 ;
CMSIS-DAP : SAMD21 Xplained Pro, d'après le champ `sonde` de son BSP), l'utilisateur lance depuis
VSCodium, après avoir fait son choix par le moyen retenu au PA-E10 :
- la tâche de flash ;
- la session de débogage : arrêt sur le point d'entrée, registres de périphériques par le SVD.
Relever configuration `launch` effective, commande du serveur, résultat. Non-régression :
session de débogage QEMU ; `launch` et tâches des configurations QEMU identiques à ceux d'avant
l'étape (`diff`).

### 4. Clôture
**PA-E11** (second temps) : rapport de validation ; sort des essais ; fusion et publication
(PA-P), dans l'ordre du PA-E10 si des BSP sont touchés.

## Critères de validation
- [ ] PA-E10 et PA-E11 tranchés et consignés ; autorisation de flash consignée.
- [ ] Par carte validée : flash et débogage depuis VSCodium avec le serveur et l'interface
      choisis ; résultat dans le rapport.
- [ ] ST-LINK et CMSIS-DAP couverts chacun par au moins une carte.
- [ ] Configurations QEMU : `launch` et tâches inchangés ; session de débogage QEMU verte.
- [ ] Si un manifeste ou un cfg de BSP change : binaires des presets concernés identiques à
      l'oracle avant (skill `lepton-oracle`) ; `lepton check` code 0 sur `<ROOTSTOCK>`.
- [ ] `pytest` et `scripts/valider-schemas.sh` verts.
- [ ] `jlink` : conforme au PA-E10 ; H1 de `HORS-PLAN.md` mis à jour.

## Pièges connus
- Le numéro de série reste unique pour toutes les configurations jusqu'à EP-6 : avec plusieurs
  cartes branchées, OpenOCD peut prendre la mauvaise sonde. Une carte à la fois.
- Changer le champ `sonde` du schéma fait échouer `lepton check` sur un rootstock dont les BSP
  sont à l'ancienne version (rootstocks d'essai, VM).
- Le cfg sert au flash par CMake et au débogage par Cortex-Debug : un changement d'un seul côté
  les désaccorde.
- NUCLEO-F429ZI : Ethernet muet possible après un passage par la VM (D12 du hors-plan d'ENV ;
  parade de `doc/devenv/handoff/env-50.md`).
- Ports série et USB : à relever à chaque banc (`doc/devenv/rapports/env-45-sonde.md` §1.7).

## À la fin de l'étape
`STATUS.md` : statut, branches, §Versions, décisions PA-E10 et PA-E11, journal. `HORS-PLAN.md` :
H1, serveurs écartés, tout point écarté. Passation `handoff/ep-5.md`.
