# ENV-31 — Piles FreeRTOS lisibles par rtos-views

Session du 2026-11-03. Clone noyau `master` be25cd0 (non modifié pendant l'audit). Mesures sur
`<ROOTSTOCK>/build/<preset>` (constructions en place) et sur des constructions jetables hors dépôts
(scratchpad de la session, script `env31/mesure.sh` : `cmake -S <ROOTSTOCK>/trunk --preset <P> -B
<scratch>` ; variante `rec` par `-DconfigRECORD_STACK_HIGH_ADDRESS=1`, variante `trace` par une copie
de `FreeRTOSConfig.h` placée en `-iquote`). Aucune écriture dans le trunk ni dans un clone.

## 1. Effet des options dans FreeRTOS V11.3.0

| Option | Champs ajoutés | Code compilé en plus | Options entraînées |
| --- | --- | --- | --- |
| `configRECORD_STACK_HIGH_ADDRESS` 1 | TCB : `pxEndOfStack` (`tasks.c:401`) ; `StaticTask_t` : `pxDummy8` (`FreeRTOS.h:3184`) | une affectation dans `prvInitialiseNewTask` (`tasks.c:1863`), en ligne dans `xTaskCreateStatic` | aucune ; défaut 0 sous `#ifndef` (`FreeRTOS.h:715`) |
| `configUSE_TRACE_FACILITY` 1 | TCB : `uxTCBNumber`, `uxTaskNumber` (`tasks.c:409`) ; file/sémaphore : `uxQueueNumber`, `ucQueueType` (`queue.c:132`) ; temporisateur : `uxTimerNumber` (`timers.c:90`) ; groupe d'événements : `uxEventGroupNumber` (`event_groups.c:59`) ; tampons de flux | `uxTaskGetSystemState`, `vTaskGetInfo`, `uxTaskGetTaskNumber`, `vTaskSetTaskNumber`, accesseurs `*Number` des files, temporisateurs, groupes ; numérotation dans chaque création | `tskSET_NEW_STACKS_TO_KNOWN_VALUE` déjà à 1 (par `configCHECK_FOR_STACK_OVERFLOW` 2, `tasks.c:131`) |

- `vTaskList` / `vTaskListTasks` exigent `configUSE_STATS_FORMATTING_FUNCTIONS`, qui exige
  l'allocation dynamique (`#error`, `FreeRTOS.h:2843`) : **exclu** par l'exigence « allocation
  statique uniquement ». Aucune fonction de formatage (`sprintf`) ne peut donc entrer.
- Édition de liens avec `-ffunction-sections -fdata-sections --gc-sections` : les fonctions de
  trace non appelées sont retirées.
- `configCHECK_FOR_STACK_OVERFLOW` 2 et `configASSERT` : non touchés.

## 2. TCB et objets fournis par Lepton

- `freertos_tcb_t` = `StaticTask_t` + `StaticEventGroup_t` (`kal/backend/freertos/kal_backend.h:47`),
  alloué par tâche dans `kernel_pthread_create` : `_sys_malloc(sizeof(tcb_t))`
  (`core-freertos/kernel_pthread.c:345`). `_sys_malloc` appelle `malloc` de newlib-nano : tas entre
  `__heap_start__` et `__stack_limit__`.
- TCB des tâches idle et de service des temporisateurs : statiques (`xIdleTaskTCB`,
  `xTimerTaskTCB`, `configKERNEL_PROVIDED_STATIC_MEMORY`), en `.ccm_bss`.
- Accès internes de Lepton au TCB : I1 seulement (`pxTopOfStack`, premier membre) ; inchangé par
  les deux options.
- `StaticSemaphore_t` (= `StaticQueue_t`), `StaticTimer_t`, `StaticEventGroup_t` sont intégrés à
  des structures du noyau (`kernel_sem.h`, `kernel_pthread_mutex.h`, `kernel_timer.h`,
  `rttimer.h`, `kernel_pthread_t`, `lwip/ports/freertos/sys_arch.h`).

Tailles (DWARF, `arm-none-eabi-gdb` 17.2, SAMD21 et WL55 identiques) :

| Structure | Actuel | `rec` | `trace` (trace + rec) |
| --- | --- | --- | --- |
| `StaticTask_t` | 84 | 88 | 96 |
| `freertos_tcb_t` | 108 | 112 | 124 |
| `StaticQueue_t` | 72 | 72 | 80 |
| `StaticTimer_t` | 40 | 40 | 44 |
| `StaticEventGroup_t` | 24 | 24 | 28 |
| `kernel_pthread_t` | 2380 (SAMD21) / 2372 (WL55) | inchangé | +8 |

Tas newlib-nano (bloc arrondi à 8 octets) : `freertos_tcb_t` 108 → 112 ne change pas le bloc
alloué (estimation d'après la granularité, non mesurée à l'exécution) ; 124 ajoute 16 octets par tâche.

## 3. Marge RAM des presets FreeRTOS

Relevé sur `<ROOTSTOCK>/build/<preset>` (sections en RAM hors `.heap`, symboles de l'édition de liens) :

| Preset | RAM | Statique | Tas newlib libre | Pile principale |
| --- | --- | --- | --- | --- |
| `qemu-mps2-an386-freertos` | 4 Mio | 141192 | 4044920 | 8192 |
| `qemu-mps2-an386-freertos-soft` | 4 Mio | 140632 | 4045480 | 8192 |
| `qemu-mps2-an500-freertos` | 4 Mio | 141192 | 4044920 | 8192 |
| `nucleo-f429zi-freertos` | 192 Kio | 100160 | 88256 | 8192 |
| `nucleo-f439zi-freertos` | 192 Kio | 100160 | 88256 | 8192 |
| `stm32f746g-disco-freertos` | 320 Kio | 167584 | 143944 | 8192 |
| `samd21-xplained-pro-freertos` | 32 Kio | 18408 | 12824 | 1536 |
| `nucleo-wl55jc1-freertos` | 64 Kio | 33008 | 28432 | 4096 |

Tous les presets du noyau sont en `CMAKE_BUILD_TYPE` Debug.

## 4. Effet mesuré (constructions jetables, `base` → variante)

| Preset | Variante | `.text` | `.ccm_bss` | `.bss` | Autres sections | Symboles changés (nom, type, taille) |
| --- | --- | --- | --- | --- | --- | --- |
| SAMD21 | `rec` | 0 | +8 | 0 | `.debug_info` +721, `.debug_str` +18, `.debug_loclists` −3 | 3 : `xTaskCreateStatic` 496 → 500, `xIdleTaskTCB` et `xTimerTaskTCB` 84 → 88 |
| SAMD21 | `trace` | +1552 | +232 | +24 | 8 sections `.debug_*` | 214 |
| WL55 | `rec` | 0 | +8 | 0 | `.debug_info` +735, `.debug_str` +18, `.debug_line` +4, `.debug_loclists` +9 | 3 : `xTaskCreateStatic` 504 → 508, mêmes TCB |
| WL55 | `trace` | +528 | +296 | +28 | `.noinit` +4, 8 sections `.debug_*` | 101 |

- `rec` : écart limité à la tâche (+4 octets de code absorbés par l'alignement de `.text`, +4 octets
  par TCB).
- `trace` : écart diffus. Les champs ajoutés aux sémaphores et temporisateurs intégrés déplacent
  des membres de structures du noyau. Une trentaine de fonctions hors FreeRTOS grossissent
  (`kernel_io_read_args` +76, `kernel_io_write_args` +72, `select` +56, …).

## 5. Champs lus par rtos-views 0.0.16 (FreeRTOS)

Lecture de `~/.vscode-oss/extensions/mcu-debug.rtos-views-0.0.16-universal/dist/extension.js` :

- `getStackInfo` : `pxStack`, `pxTopOfStack`, `pxEndOfStack`. Sans `pxEndOfStack`, ni taille, ni
  usage, ni pic (« ??? »). Avec lui : taille = |`pxStack` − `pxEndOfStack`|, usage = taille −
  |`pxTopOfStack` − `pxStack`|, pic par recherche de l'octet 0xA5 (165). Le remplissage 0xA5 est
  déjà actif (§1).
- `uxTCBNumber` sert seulement à la colonne ID (« ?? » sinon) et au message d'aide « Enable macro
  configUSE_TRACE_FACILITY ».
- `uxQueueNumber`, `ucQueueType` : vue des files (« ??? » sinon ; type déduit autrement pour les
  sémaphores).
- Conclusion : `configRECORD_STACK_HIGH_ADDRESS` 1 suffit pour la taille, l'usage et le pic de
  pile. `configUSE_TRACE_FACILITY` 1 n'ajoute que l'identifiant des tâches et le numéro des files.

## 6. PA-49 (réponses de l'utilisateur, 2026-11-03)

| Question | Décision |
| --- | --- |
| Options | `configRECORD_STACK_HIGH_ADDRESS` 1 seul ; `configUSE_TRACE_FACILITY` reste 0 (colonne ID « ?? » acceptée) |
| Portée | tous les presets FreeRTOS, valeur définie sous `#ifndef` (une carte peut la surcharger) |
| Critère, par preset FreeRTOS | admis : `xTaskCreateStatic` +4, `xIdleTaskTCB` et `xTimerTaskTCB` 84 → 88, `.ccm_bss` +8, `.text` 0 ou +4, sections `.debug_*`, empreintes ; tout le reste identique (aucun symbole ajouté ou retiré ; `.data`, `.bss`, `.noinit` inchangés). Écart hors critère = arrêt |
| embOS (8) et host | `comparer-oracle.py` code 0 |
| Cartes | NUCLEO-WL55JC1 (banc 16/16, essai rtos-views) et STM32F746G-DISCO (20/20) ; NUCLEO-F429ZI et SAMD21 non essayées |

## 7. Oracle avant et implémentation

Oracle avant `oracles/env-31-avant/` (`rejouer-oracle.sh`, host + 6 QEMU + 10 carte, constructions
à neuf, journal `env-31-avant/rejouer-oracle.log`) : « tout a réussi ». Contre `env-27-apres` :
`comparer-oracle.py` code 0 sur les 16 presets (empreintes seules différentes), host 7/7,
empreintes mklepton identiques, bancs QEMU 19/19/15/15/18/18 identiques.

| Dépôt | Branche | Commit | Contenu |
| --- | --- | --- | --- |
| clone noyau | `devenv/env-31` (depuis `master` be25cd0) | fc71632 | `FreeRTOSConfig.h` : `configRECORD_STACK_HIGH_ADDRESS` 1 sous `#ifndef` ; en-tête complété (exigences de l'étape 7, ENV-31) |

## 8. Contrôles

Oracle après `oracles/env-31-apres/` (mêmes arguments) : « tout a réussi ». Comparaisons
`env-31-avant` → `env-31-apres` : `env-31-apres/comparaisons/<preset>.txt`.

| Preset | Sections/symboles | Empreinte | Fumée | Banc KAL | Écarts expliqués |
| --- | --- | --- | --- | --- | --- |
| `host` | — | mklepton identiques | — | `ctest` 7/7 | — |
| 8 presets embOS | code 0 | diffère | QEMU : verte | QEMU : 19/15/18, identiques | aucun |
| `qemu-mps2-an386-freertos` | code 1 : 9 écarts | diffère | verte | 19/19 | E-1, E-2 |
| `qemu-mps2-an386-freertos-soft` | code 1 : 8 écarts | diffère | verte | 15/15 | E-1 |
| `qemu-mps2-an500-freertos` | code 1 : 8 écarts | diffère | verte | 18/18 | E-1 |
| `nucleo-f429zi-freertos`, `nucleo-f439zi-freertos` | code 1 : 8 écarts | diffère | non essayée (PA-49) | non essayé | E-1 |
| `stm32f746g-disco-freertos` | code 1 : 8 écarts | diffère | `cortexM7-stm32f7` | 20/20 | E-1 |
| `samd21-xplained-pro-freertos` | code 1 : 8 écarts | diffère | non essayée (PA-49) | non essayé | E-1 |
| `nucleo-wl55jc1-freertos` | code 1 : 8 écarts | diffère | `cortexM4-stm32wlxx` | 16/16 | E-1 |

- **E-1** (8 presets FreeRTOS, dans le critère du PA-49) : `xTaskCreateStatic` +4 (0x1f8 → 0x1fc ;
  SAMD21 0x1f0 → 0x1f4), `xIdleTaskTCB.3` et `xTimerTaskTCB.1` 0x54 → 0x58, `.ccm_bss` +8,
  sections `.debug_info`, `.debug_line`, `.debug_loclists`, `.debug_str`. Aucun symbole ajouté ou
  retiré ; `.data`, `.bss`, `.noinit` inchangés.
- **E-2** (`qemu-mps2-an386-freertos` seul) : `.text` 159400 → 159416 (+16), hors du critère
  initial (0 ou +4) : arrêt. Cause vérifiée par une construction témoin
  (`-DconfigRECORD_STACK_HIGH_ADDRESS=0`, scratchpad) : le code décale de +4 à partir de
  `vTaskDelete`, de +8 à `__vfscanf` (objet newlib aligné sur 8), de +16 à `_close` (aligné sur 16) ;
  aucune autre taille de symbole changée. Critère amendé par l'utilisateur (PA-49 (2)) : +4 de code
  plus le bourrage d'alignement qui en résulte. Les 7 autres presets FreeRTOS : `.text` inchangé.
- Test du greffon `qemu-mps2-an386.peripheriques` : vert dans les 4 presets an386.

Cartes (procédure d'ENV-24 §6 : reconfiguration de `<ROOTSTOCK>/build/<P>` avec les options de
carte, construction, recapture de `lepton.elf` comparée à `env-31-apres/<P>` : code 0, puis
`ctest --preset <P> -L board` ; journaux `carte.log`, `carte-detail.log`, `carte-config.log`) :

| Carte | Sondes, ports | Résultat | Détail |
| --- | --- | --- | --- |
| NUCLEO-WL55JC1 (A testée, B paire radio) | A STLINK-V3 002700253431510837393937 `/dev/cu.usbmodem145103` ; B 004F003E3431510937393937 `/dev/cu.usbmodem1454403` | 16/16 | radio A→B 20/20, B→A 20/20, ping/pong 20/20, 0 perdu (comme ENV-24) |
| STM32F746G-DISCO | ST-LINK/V2-1 0671FF495351885087181231 `/dev/cu.usbmodem1454303` ; Mac 192.168.2.10 sur `en0` | 20/20 | ping 3/3, `LIST` 13 entrées, `RETR /usr/etc/.boot` 57 octets, ECONNRESET=15 (comme ENV-24) |

Incidents :
- La cfg OpenOCD du F746 n'a pas de numéro de sonde (`set` simple de `lepton_greffons.cmake`,
  non surchargeable) et `interface/stlink.cfg` accepte aussi les STLINK-V3 : essai F746 fait avec
  les WL55 débranchées (à la demande de la session), après celui des WL55 (qui désignent leur sonde).
- Premier essai F746 : `board.smoke_lsh` en échec en 0,63 s. OpenOCD a rendu le code 1 avant toute
  écriture, car un OpenOCD de Cortex-Debug (session VSCodium F746) tenait la sonde. L'utilisateur
  l'a arrêté ; le second essai est vert.
- Images laissées en flash : `nucleo-wl55jc1-freertos` d'ENV-31 sur A et B, `stm32f746g-disco-freertos`
  d'ENV-31 sur le F746.

VSCodium (utilisateur, NUCLEO-WL55JC1 A, `nucleo-wl55jc1-freertos`, onglet *xRTOS*) : taille, usage
et pic de pile affichés pour chaque tâche ; constat « fonctionne ». O-2 d'ENV-26 levé.

`lepton check` (`<ROOTSTOCK>`) : code 0, 19 fichiers conformes. Trunk : aucun fichier régulier hors
`.DS_Store` tolérés, aucun lien cassé.

## 9. PA-50

Nouvel oracle de référence Mac : `oracles/env-31-apres/`. Fusion de `devenv/env-31` dans `master` du
clone noyau et dans `main` de lepton-tools, push (PA-P) : voir `DEVENV-STATUS.md` §Décisions.
