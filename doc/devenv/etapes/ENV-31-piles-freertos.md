# Étape ENV-31 — Piles FreeRTOS lisibles par rtos-views

## Contexte
ENV-26 a réalisé DBG-4. Sous VSCodium, rtos-views 0.0.16 affiche la liste des tâches FreeRTOS sur
NUCLEO-WL55JC1, mais la taille et l'usage des piles restent « ??? » (O-2 de
`rapports/env-26-dbg4.md`). Cause : le TCB n'a ni `pxEndOfStack` ni `uxTCBNumber`, car
`kal/backend/freertos/FreeRTOSConfig.h` (FreeRTOS V11.3.0) pose `configUSE_TRACE_FACILITY` à 0 et
ne définit pas `configRECORD_STACK_HIGH_ADDRESS`.

Cette étape active ces options pour rendre les piles lisibles. Elle **modifie les binaires** des
presets FreeRTOS, car la structure du TCB change. Depuis ENV-17, chaque étape a tenu « binaires
inchangés » ou des écarts bornés et classés (ENV-20 : table de vecteurs ; ENV-24 : cpufs). La même
discipline s'applique ici : écart attendu, borné, classé, puis nouvel oracle de référence.
Archétype : modification contrôlée du greffon noyau.

## Prérequis
- ENV-28 terminée. Étape indépendante d'ENV-29 et d'ENV-30.
- Fichier : `<ROOTSTOCK>/depots/lepton/original/master/scion/sys/root/src/kernel/core/kal/backend/freertos/FreeRTOSConfig.h`.
  Il fixe deux exigences : allocation statique uniquement (TCB, piles et objets fournis par
  Lepton), et `configCHECK_FOR_STACK_OVERFLOW` à 2 (lignes 12, 76 et 77).
- Presets FreeRTOS (`CMakePresets.json` du noyau), au nombre de 8 :
  - QEMU : `qemu-mps2-an386-freertos`, `qemu-mps2-an386-freertos-soft`,
    `qemu-mps2-an500-freertos` ;
  - cartes : `nucleo-f429zi-freertos`, `nucleo-f439zi-freertos`, `stm32f746g-disco-freertos`,
    `samd21-xplained-pro-freertos`, `nucleo-wl55jc1-freertos`.
- Oracle de référence Mac : `rapports/oracles/env-27-apres/`.
- Contournement de rtos-views : skill `lepton-cibles` §Vues (mode hexadécimal, O-1).
- Skills `lepton-rootstock`, `lepton-oracle` et `lepton-cibles`.
- Branches `devenv/env-31` : lepton-tools et clone noyau.

## Tâches

### 1. Audit (lecture seule) → PA-49
- Effet des deux options dans FreeRTOS V11.3.0 (`ucore/freeRTOS_11-3-0/tasks.c`, `include/FreeRTOS.h`) :
  - champs ajoutés au TCB ;
  - fonctions compilées : `uxTaskGetSystemState`, `vTaskList` (avec
    `configUSE_STATS_FORMATTING_FUNCTIONS`) ;
  - autres options entraînées.
- Lepton fournit les TCB (`StaticTask_t`, `kal/backend/freertos/kal_backend.h`) : relever la taille de la structure
  avant et après, et où elle est réservée.
- Marge RAM de chaque preset FreeRTOS (`arm-none-eabi-size`, carte mémoire) : SAMD21 est la cible
  la plus petite.
- Champs lus par rtos-views 0.0.16 pour FreeRTOS : confirmer qu'ils suffisent.
- Rapport `rapports/env-31-freertos.md`.
- **PA-49** : l'utilisateur valide :
  - Options activées : <À CONFIRMER au PA-49 : `configUSE_TRACE_FACILITY` 1 et
    `configRECORD_STACK_HIGH_ADDRESS` 1, ou davantage>.
  - Portée : <À CONFIRMER au PA-49>.
    - Option 1 : tous les presets FreeRTOS.
    - Option 2 : debug seulement.
    - Option 3 : surcharge par carte (`#ifndef`).
  - Critère d'écart accepté par preset : sections et symboles qui peuvent changer, et ceux qui
    doivent rester identiques.
  - Les 8 presets embOS et `host` restent identiques.
  - Cartes disponibles pour les essais : <À CONFIRMER au PA-49>.
- Aucune modification avant la réponse.

### 2. Oracle avant
Skill `lepton-oracle` : `host` et les 16 presets → `rapports/oracles/env-31-avant/`. Vérifier que
cet oracle est conforme à `env-27-apres`.

### 3. Implémentation (clone noyau, `devenv/env-31`)
- `FreeRTOSConfig.h`, selon le PA-49. Mettre à jour le commentaire d'en-tête : « Exigences de
  l'étape 7 ».
- Garder un commit dédié.
- Construire les 8 presets FreeRTOS, puis comparer à `env-31-avant` (`comparer-oracle.py`). Classer
  chaque écart contre le critère du PA-49 ; un écart hors critère est un arrêt.

### 4. Contrôles → PA-50
- Oracle après `rapports/oracles/env-31-apres/` :
  - embOS et `host` : code 0 ;
  - FreeRTOS : écarts limités au critère du PA-49.
- QEMU (`lepton-cibles`) : fumée et banc KAL des 3 presets FreeRTOS QEMU, mêmes résultats que
  `env-27-apres`. Le test du greffon `qemu-mps2-an386.peripheriques` reste vert.
- Cartes selon le PA-49 : fumée et banc KAL FreeRTOS, mêmes comptes qu'en ENV-24 :
  - F429 et F746 : 20/20 ;
  - WL55 : 16/16 ;
  - SAMD21 : 15/15 ou 14/14 (E-5 hérité).
- Essai VSCodium par l'utilisateur sur NUCLEO-WL55JC1 FreeRTOS : rtos-views affiche la taille et
  l'usage de pile de chaque tâche.
- `lepton check` code 0.
- **PA-50** : rapport ; nouvel oracle de référence (`env-31-apres`) ; fusion de `devenv/env-31`
  dans `master` du clone noyau et dans `main`, push (PA-P). La validation Debian est reportée à
  ENV-33.

## Critères de validation
- [ ] PA-49 et PA-50 tranchés et consignés.
- [ ] embOS et `host` : `comparer-oracle.py` code 0.
- [ ] FreeRTOS : chaque écart classé dans le critère du PA-49.
- [ ] Fumée et banc KAL FreeRTOS : comptes inchangés (QEMU, et cartes du PA-49).
- [ ] Piles affichées par rtos-views sur WL55 FreeRTOS (constat de l'utilisateur).

## Pièges connus
- `configCHECK_FOR_STACK_OVERFLOW` 2 et `configASSERT` restent actifs : ne pas les toucher.
- Une option de trace peut faire compiler des fonctions de formatage (`sprintf`) et grossir
  `.text` : relever l'écart, ne pas l'accepter par défaut.
- Le banc KAL embOS ne doit pas bouger : un écart embOS signale que la modification sort du
  backend FreeRTOS.
- `ctest -L kal -FS board_t0` sélectionne encore `board.smoke_lsh` : ajouter
  `-E board.smoke_lsh` (piège d'ENV-27).
- Vue embOS de rtos-views : le contournement du mode hexadécimal (O-1) est sans rapport avec cette
  étape.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, branches, oracle de référence, décisions PA-49 et PA-50, journal.
Passation `handoff/env-31.md`.
