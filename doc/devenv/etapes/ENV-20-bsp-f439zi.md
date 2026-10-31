# Étape ENV-20 — BSP `nucleo-f439zi`

## Contexte
La NUCLEO-F439ZI est la carte nominale du portage ; la NUCLEO-F429ZI en est la carte de
validation. PA-2 Q4 a prévu deux BSP sur le greffon famille `stm32f4xx`. Le BSP `nucleo-f439zi`
a été reporté en ENV-6 (PA-7 Q7). Deux conditions préalables ont été notées : la table de vecteurs
`vecteurs/stm32f429xx_vectors.c` de la famille ne relie que les IRQ 12, 39, 57 et 61 ; elle est à
compléter avant un second BSP F4 (`rapports/env-6-validation.md`, « Point signalé (non bloquant) »). L'utilisateur n'a pas de
NUCLEO-F439ZI (2026-10-31) : pas de validation par exécution sur cette carte.
Archétype : création (second BSP d'une famille existante).

## Prérequis
- ENV-19 fusionnée (la graine `original-tree` et les presets du noyau ont changé).
- Greffons `family-stm32f4xx` et `bsp-nucleo-f429zi` : clones `<ROOTSTOCK>/depots/lepton/<clé>/master`.
- Commande `lepton scion new NAME --type bsp --from BSP` (ENV-8 S3-1 : remplacement de la
  destination dans les fichiers texte copiés).
- Branches `devenv/env-20` : lepton-tools, clone noyau (presets, `BUILDING.md`),
  `family-stm32f4xx`, graine `original-tree`, nouveau dépôt du BSP.

## Tâches

### 1. Audit (lecture seule) → PA-27
- Différences STM32F429 / STM32F439 qui touchent le BSP et la famille : définition de la puce,
  en-tête CMSIS du device (présence dans `kernel/core/ucore/cmsis/Device/st/stm32f4xx`), table de
  vecteurs (IRQ propres au F439), script de liens, configuration OpenOCD. Sources : en-têtes CMSIS
  du greffon famille, documentation ST citée dans le clone ; aucune valeur reprise de mémoire.
- Fichiers du BSP `nucleo-f429zi` et ce que `lepton scion new --from` en ferait (destination,
  emplacement du dépôt : défaut `depots/lepton-bsp/NAME`, différent de la convention ENV-13).
- XML mkconf : `mkconf_tauon_basic_nucleo_f439zi.xml` sert aujourd'hui à `nucleo-f429zi`.
- Rapport `doc/devenv/rapports/env-20-bsp.md`.
- **PA-27** : l'utilisateur valide :
  - la forme de la table de vecteurs complète (tous les vecteurs vers des noms CMSIS faibles, ou
    autre), et son emplacement (une table par MCU dans la famille, règle PA-2 Q3) ;
  - la création du BSP par `lepton scion new --from nucleo-f429zi` puis déplacement vers la
    convention de ENV-13, ou par copie manuelle : <À CONFIRMER au PA-27> ;
  - les fichiers propres au F439 et le XML utilisé ;
  - les noms des presets (`nucleo-f439zi-embos`, `nucleo-f439zi-freertos` proposés) ;
  - un essai du binaire F439 sur la NUCLEO-F429ZI : <À CONFIRMER au PA-27 ; compatibilité à
    établir par l'audit ; écriture flash soumise à une autorisation de type PA-11>.
- Aucune modification avant la réponse.

### 2. Oracle avant
Skill `lepton-oracle`, presets de l'oracle d'ENV-19 → `rapports/oracles/env-20-avant/`.

### 3. Table de vecteurs de la famille (premier temps)
- `family-stm32f4xx`, `devenv/env-20` : table complète selon le PA-27.
- Nouvelle référence pour `nucleo-f429zi-*` : écart de symboles limité à la table de vecteurs,
  démontré (méthode d'ENV-4, deux temps) ; fumée sur NUCLEO-F429ZI si l'utilisateur l'accorde.

### 4. BSP et presets (second temps)
- Dépôt `<ROOTSTOCK>/depots/lepton/bsp-nucleo-f439zi/master` ; manifeste `lepton-greffon.json`
  (`lepton check`).
- Noyau : 2 presets ; `doc/BUILDING.md` mis à jour (table des cartes, commandes).
- Graine `original-tree` : entrée `bsp-nucleo-f439zi` ; regreffe sur une copie d'essai, puis
  `<ROOTSTOCK>` (séquence PA-13).

### 5. Contrôles → PA-28
- Constructions `nucleo-f439zi-*` : code 0 ; symboles comparés à `nucleo-f429zi-*` : écarts
  limités à la liste du PA-27.
- `comparer-oracle.py` sur les autres presets : code 0 ; QEMU : fumée et banc KAL identiques.
- `lepton check` sur `<ROOTSTOCK>` : code 0 ; `lepton generate` d'un projet `nucleo-f439zi` sur
  un rootstock d'essai : code 0.
- **PA-28** : rapport ; push du nouveau dépôt (créé par l'utilisateur ou par `gh` sur son
  accord) et des branches `devenv/env-20` ; fusions (PA-P).

## Critères de validation
- [ ] PA-27 et PA-28 tranchés et consignés.
- [ ] Table de vecteurs F4 complète ; écart de `nucleo-f429zi-*` démontré et limité à la table.
- [ ] BSP `nucleo-f439zi` publié, inscrit dans `original-tree` ; 2 presets construits.
- [ ] Aucune modification du système de construction commun (BLD-6) : constat dans le rapport.

## Pièges connus
- Pas de carte F439 : une construction correcte ne prouve pas le démarrage. Le rapport le dit.
- Les noms de fichiers `nucleo_f439zi_*` du BSP `nucleo-f429zi` (R3, ENV-6) prêtent à confusion :
  ne pas les renommer dans cette étape.
- La table de vecteurs complète change les binaires F429 : c'est le seul écart admis.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, branches, emplacements, décisions PA-27 et PA-28, journal. Passation
`handoff/env-20.md`.
