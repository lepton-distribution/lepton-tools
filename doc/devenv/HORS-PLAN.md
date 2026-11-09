# Points hors plan et non traités — à rappeler en fin de chantier

Liste tenue par la session principale (demande de l'utilisateur du 2026-11-06). Elle regroupe ce qui
a été écarté du plan, laissé en l'état ou relevé sans suite, avec sa source. À présenter à
l'utilisateur à la fin du chantier (après la dernière étape du plan), pour décision : traiter, garder
hors plan, ou abandonner. Toute session qui écarte un nouveau point l'ajoute ici.

État au 2026-11-09 (après ENV-43, dernière étape du plan). Révision du plan du 2026-11-09 : colonne « Suite ». Un point traité reste dans la liste : sa colonne « Suite » renvoie au rapport de l'étape qui le clôt (décision du 2026-11-09). Un point nouvellement écarté s'y ajoute.

## A. Hors plan par décision de l'utilisateur

| # | Point | Source | Suite |
| --- | --- | --- | --- |
| A1 | Hôte Apple Silicon : non validé (annoté « hors plan, non validé » dans la documentation) | révisions du 2026-10-31 ; PA-21 A-3 | hors plan (décision du 2026-11-09) |
| A2 | Démarrage réel sur une NUCLEO-F439ZI : BSP `nucleo-f439zi` validé par construction et symboles seulement (aucune carte) | révision du 2026-10-31 ; ENV-20 | hors plan (décision du 2026-11-09) |
| A3 | Code non configuré par les presets : SPL F4 (`stm32f4xx/driverlib/`, dont `stm32f469xx.h`) ; dépendants de la HAL F4 (`kernel/usb/stm32f4-usb-core/core/`, BSP `discovery_f4-baseboard-modem`, `stm32f469i-eval`, `user_kernel_mkconf.h` de `sys/user/tauon-basic`) ; `at91/softpack-lib/samv71`, `at91/asf/sam0` ; en-têtes de périphérique V3.x du noyau (`ucore/cmsis/Device/{ARM/ARMCM0,ARM/ARMCM3,atmel/samd20,lm3s,st/stm32f2xx}`) ; cœur `cortex-m3` sans preset | révisions du 2026-10-31 ; `rapports/env-34-hal-f4.md` §1, `env-35-hal-f4.md` §1.7, `env-42-core-cm4.md` §1.4 | hors plan (décision du 2026-11-09) ; dépendants de la SPL : sort tranché au PA-79 (ENV-46) |
| A4 | Publication de l'extension Lepton sur Open VSX (aujourd'hui `.vsix` versionné) | révisions du 2026-10-31 | hors plan (décision du 2026-11-09) |

## B. Écartés à une révision du plan, « à la révision suivante »

| # | Point | Source | Suite |
| --- | --- | --- | --- |
| B1 | Bascule des familles F7 et WL sur la projection scion (aujourd'hui copies dans les greffons), avec leurs miroirs de conservation sous `lepton-distribution/` | révision du 2026-11-05 ; PA-68 (ENV-40) | planifié : F7 en ENV-47, WL en ENV-48 |
| B2 | Montée de version de la HAL WL (V1.3.0 compilée, amont `v1.6.0`) ; couple incohérent HAL STM32CubeWL `v1.3.0` / CMSIS device `v1.1.1` (= STM32CubeWL `v1.2.0`), version du CMSIS device absente du texte du manifeste | révision du 2026-11-05 ; `rapports/env-37-wl-provenance.md` §1.8 (constats 1, 7) | planifié en ENV-49 |
| B3 | Retrait des fichiers SPL de `stm32f4xx/driverlib/` (conservés pour les dépendants hors plan, A3) | révision du 2026-11-05 ; PA-57 | planifié en ENV-46 |
| B4 | Choix de la sonde par numéro de série pour les BSP qui ne l'ont pas (`nucleo-f429zi`, `stm32f746g-disco`, …, comme `LEPTON_BOARD_STLINK_SERIAL` du BSP `nucleo-wl55jc1`) : aujourd'hui une seule sonde ST branchée pendant leurs bancs | PA-72 (ENV-42, O-1) ; proposition non validée d'ENV-31 (`handoff/env-31.md`, pièges) | planifié en ENV-45 |

## C. Questions à poser à l'utilisateur

| # | Point | Source | Suite |
| --- | --- | --- | --- |
| C1 | Sort fonctionnel de `RadioIsChannelFree` (WL, `radio.c`) : corps sous `#if 0`, rend toujours `false` ; modification Lepton compilée et non documentée avant ENV-37 | `rapports/env-37-wl-provenance.md` §1.8 (constat 6) | décision du 2026-11-09 : documenter en l'état, binaire inchangé ; planifié en ENV-48 (raison au PA-83) |
| C2 | Origine des 8 `LICENSE.txt` identiques de la famille WL (avis court ST BSD-3), absents de tous les tags amont ; le `LICENSE.md` amont (texte complet) manque. Laissés en l'état au PA-61 | `rapports/env-37-wl-provenance.md` §1.4 | décision du 2026-11-09 : tranché à la projection du WL, ENV-48 (PA-83) |

## D. Résidus et observations laissés sans suite

| # | Point | Source | Suite |
| --- | --- | --- | --- |
| D1 | `seed replace` / `seed remove` d'un greffon porteur de projections : non essayé (aucune graine de projet ne remplace la famille F4) | `rapports/env-41-f4-projection.md` §4.4 | planifié en ENV-44 |
| D2 | Extension 0.5.2 : table clone tiers → trunk non observée en session de débogage réelle (gdb rend le chemin du trunk pour les binaires F4) | `rapports/env-41-f4-projection.md` §4.4 ; `handoff/env-41.md` | planifié en ENV-44 |
| D3 | Hook `proteger-trunk.py` : lit le texte des commandes ; un script qui cite `trunk/` ou `depots/tiers/` après un verbe d'écriture est refusé même s'il n'y écrit pas (parade : passer par un fichier) | `rapports/env-41-f4-projection.md` §4.4 | planifié en ENV-44 |
| D4 | rtos-views 0.0.16 : liste embOS vide au format naturel (`OS_Global.IsRunning` rendu `1 '\001'`) ; contournement documenté (mode hexadécimal), pas de signalement amont | `rapports/env-26-dbg4.md` §4 (O-1) | hors plan (décision du 2026-11-09) |
| D5 | BSP `qemu-mps2-an386` : en-tête de périphérique `ucore/cmsis/Device/ARM/ARMCM4` de l'arbre V3.x, compilé avec le `core_cm4.h` 5.9.0 ; un `ARMCM4` CMSIS 5 existe sous `ucore/cmsis-5/Device/ARM/` | `rapports/env-42-core-cm4.md` §1.4, §4.4 (O-3) | planifié en ENV-44 |
| D6 | `scripts/tiers/compiler-hal-f4-a-blanc.sh` rend 1 tant qu'il essaie l'ordre `v330`, qui n'est plus celui d'aucun preset depuis ENV-42 (ligne gardée pour comparaison) | `rapports/env-42-core-cm4.md` §4.1 | planifié en ENV-44 |
| D7 | CMSIS-Core V3.30 : en-tête `V3.30`, macro `__CM4_CMSIS_VERSION_SUB` à `0x20` (3.20) ; `cmsis/source.txt` dit « Version 2.10 » | `rapports/env-42-core-cm4.md` §1.1, §4.4 (O-2) | planifié en ENV-44 |
| D8 | VM : `essais/env-13-debian` (graine `original-tree`, greffe la famille F4) non regreffé en R43-1. scion 0.6.1.0 y est installé : une regreffe clonera les dépôts tiers depuis les miroirs ; d'ici là, son trunk garde la HAL F4 copiée d'ENV-34 | `rapports/env-43-debian.md` §8 (constat 7) | planifié en ENV-50 |
| D9 | Messages entre sessions : les messages de la VM vers la session Mac (`ACCUSÉ`, `AVANCEMENT`) ne sont pas remis (bridge ECONNRESET, « bridge ID is stale ») ; perte du premier accusé en R33-1 et R36-1, puis de tous les messages sauf `FIN-SUCCÈS` en R43-1. L'utilisateur relaie de fait. Le protocole du §2bis suppose une remise fiable | `rapports/env-43-mac.md` §3 ; `rapports/env-43-debian.md` §9 | planifié en ENV-44 |
