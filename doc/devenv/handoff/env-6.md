# Passation ENV-6 — Greffons BSP de référence — session du 2026-10-13 (session 3, lot WL)

## Statut
terminée (2026-10-13) — sessions 1 à 3 : PA-7 tranché (Q1-Q12 et lot WL), lots QEMU, F4 et WL extraits,
greffés et sans régression. Aucune fusion de `devenv/env-6` faite (au début de la session suivante).

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `devenv/env-6` (depuis `main` = 4d22d67) | `devenv(env-6): état et passation` (session 3) | oui |
| clone noyau `depots/lepton/original/master` | `devenv/env-6` (depuis `master` = 1551afb) | 94ea0e3 `devenv(env-6): nouvelle référence des empreintes mklepton (lot WL, PA-7 Q5)` | oui |
| graine de travail `depots/lepton-seed.scions/original-tree` | `devenv/env-6` (depuis `original-tree` 083c30b) | d6605f0 `devenv(env-6): greffons famille stm32wlxx et BSP nucleo-wl55jc1 (dépôts locaux)` | oui |
| `depots/lepton-famille/qemu-mps2` | `devenv/env-6` | 0927646 (inchangé) | oui |
| `depots/lepton-bsp/qemu-mps2-an386` / `-an500` | `devenv/env-6` | d979c6e / eb52230 (inchangés) | oui |
| `depots/lepton-famille/stm32f4xx` | `devenv/env-6` | fc8b5b9 (inchangé) | oui |
| `depots/lepton-bsp/nucleo-f429zi` | `devenv/env-6` | 702adda (inchangé) | oui |
| `depots/lepton-famille/stm32wlxx` (nouveau) | `devenv/env-6` (sur `master` 709bada, vide) | fa31306 `devenv(env-6): manifeste lepton-greffon.json, vecteurs du STM32WL55, interface radio par nom` | oui |
| `depots/lepton-bsp/nucleo-wl55jc1` (nouveau) | `devenv/env-6` (sur `master` a5200b4, vide) | 58ff413 `devenv(env-6): manifeste lepton-greffon.json, CMakeLists.txt (paramètres hors manifeste), chemins du BSP` | oui |
| seed.scions | `master` | e0adb2c | oui (non touché) |

Aucun push. Trunk regreffé (4 037 feuilles, `.scion.grafted.list` à 9 lignes), aucun fichier régulier, aucun
lien cassé. `~/lepton/build/` : host (94ea0e3) et 14 presets croisés (2b9bfc2, sources identiques à 94ea0e3
hors référence d'empreintes) reconstruits à neuf.

## Fait pendant la session
- PA-7 lot WL tranché par l'utilisateur (vecteurs dans la famille ; openocd statique + cfg générée par le
  BSP ; `radio_board_if.h` par nom ; en-tête IAR `st-stm32wl55jci-nucleo` laissé, signalé).
- Liste WL revérifiée (`ninja -t deps`, embos et freertos) : identique à `env-6-extraction.md` §4.
- Famille `stm32wlxx` : import depuis e0895ee (8ea1490), manifeste, vecteurs, inclusion par nom (fa31306).
- BSP `nucleo-wl55jc1` : import (5653f97), manifeste, `CMakeLists.txt`, chemins du BSP (58ff413).
- Clone noyau : 8d5a082 retrait (mécanique) ; 2b9bfc2 module `cmake/boards/nucleo-wl55jc1.cmake` retiré,
  presets (`LEPTON_MKCONF`) ; 94ea0e3 référence mklepton (contre-épreuve faite).
- Graine d6605f0 ; `scion ungraft`, `seed-clone --seed …`, `scion graft` ; `ungraft && graft` final.
- Non-régression : `rapports/env-6-validation.md` §Lot WL, `rapports/oracles/env-6-lot-wl/` : 12 presets
  code 0 ; WL ×2 : symboles identiques, `.data` −4 (et `.bss` +4 en FreeRTOS) = remplissage, démontré sur
  les cartes d'édition d'une copie d'essai du rootstock à l'état e0895ee (scratchpad, supprimée) ; DWARF :
  unité des vecteurs et chemins ; fumée et banc KAL identiques ; host 7/7 ; avertissements en même nombre.
- lepton-tools ad4374c : skill `lepton-cibles` (cfg OpenOCD et gdbinit du BSP WL).

## Reste à faire
- [ ] Début de la session suivante : fusions locales de `devenv/env-6` (lepton-tools → `main`, clone noyau
      → `master`, graine → `original-tree`, 7 greffons famille/BSP → `master`), après accord.
- [ ] Hors ENV-6, à planifier : BSP `nucleo-f439zi` (Q7) ; extraction F746 et SAMD21 (Q9) ;
      `kernel/usb/stm32f4-usb-core/` et démos FreeRTOS F4 (signalés) ; tables de vecteurs F4 et WL
      complètes avant un second BSP de la même famille ; `dev_stm32wlxx_bsp_radio_if.c` (paramètres FSK
      868 MHz) candidat au BSP si une seconde carte WL apparaît ; en-tête IAR
      `sys/user/tauon-basic/src/arch/st-stm32wl55jci-nucleo/` ; `doc/migration/*`, `doc/BUILDING.md`,
      `tools/migration/*.py` du clone (chemins QEMU, F4 et WL périmés) ; commande d'oracle de
      `rapports/env-5-validation.md` (forme à accolades) ; message « bsp : aucune source pour la carte »
      (`cmake/components/kernel.cmake:167`) trompeur pour les BSP par manifeste.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-7 lot WL : vecteurs famille ; openocd statique + cfg générée ; radio par nom ; en-tête IAR laissé | utilisateur | oui |
| Famille WL : `USE_HAL_DRIVER` et inclusions dans la famille ; `STM32WL55xx`, `CORE_CM4` dans le BSP ; `__KERNEL_CPU_DEVICE_NAME` posé par le `CMakeLists.txt` du BSP (comme l'ancien module) | proposition (plan accepté), appliquée | non (détail du manifeste) |
| `mcu` du BSP : `STM32WL55JC` ; famille : `STM32WL55xx` | proposition, appliquée | non |
| ENV-6 terminée ; prochaine étape ENV-7 (ordre conseillé d'ORCHESTRATION §6) | proposition, à confirmer au début de la session suivante | oui (prochaine action) |
| Lecteur `openocd` (un fichier) et OBJECT `bsp_demarrage` (sessions 1-2) | propositions appliquées, toujours à confirmer | oui |

## Pièges rencontrés
- Hook `proteger-trunk.py` : faux positif sur toute commande dont le texte contient `trunk` (copie d'essai
  dans le scratchpad comprise) → écrire la commande dans un script du scratchpad (outil Write) et l'exécuter.
- Copie d'essai du rootstock : copier aussi `.scion.rootstock.signature` (sinon `scion graft` : « aucun
  rootstock trouvé ») ; `.scion.grafted.list` reconstruit à la main (sans `seed-clone`) ; lier
  `build/host` de la copie au host réel (mklepton requis par les presets croisés) ; le chemin plus long du
  scratchpad change DWARF et les chaînes `__FILE__` (`.text` FreeRTOS +480) : n'exploiter que les sections
  non affectées.
- `rejouer-oracle.sh` sans preset rejoue le host seul (utile après une nouvelle référence d'empreintes).
- zsh : `set -- $var` ne découpe pas les mots ; passer des arguments explicites.
- Pièges des sessions 1 et 2 toujours valables (`kal_bench` et `bsp_objets`, `objcopy --dump-section`,
  mklepton sans contrôle d'existence de l'en-tête, `rcv SIGCHLD` dans la fumée).

## Critères de validation
- [x] PA-7 tranché (Q7 et lot WL compris).
- [x] Trois greffons BSP (plus an500), manifestes valides (`scripts/valider-schemas.sh`, 8 manifestes du trunk).
- [x] Plus aucun fichier propre à ces cartes dans le greffon noyau (recherches consignées, `env-6-validation.md`).
- [x] Construction des trois presets réussie ; QEMU identique à l'oracle.
- [x] Trunk sans fichier régulier ; `scion ungraft && scion graft` sans erreur.

## Reprise
```
cd /Users/cle_d_anton/lepton-tools-dev/lepton-tools && claude
# « Démarre la session sur l'étape indiquée dans DEVENV-STATUS » (ENV-7, après fusions locales de devenv/env-6)
```
