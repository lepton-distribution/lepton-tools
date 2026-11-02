# Passation ENV-26 — DBG-4 : vues des périphériques et des tâches — session du 2026-11-02

## Statut
terminée — SVD officiels dans les greffons famille, désignés par les 5 BSP de carte ; registres
lisibles sur 4 cartes sous VSCodium ; tâches embOS (contournement O-1) et FreeRTOS constatées.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` (fusion `--no-ff` de `devenv/env-26`, poussées toutes deux) | « Fusion de devenv/env-26 » ; fond : « devenv(env-26): état et passation » | oui |
| clone noyau `depots/lepton/original/master` | `master` 0bdce87, non touché | « Fusion de devenv/env-24 » | oui |
| `family-stm32f4xx`, `-stm32f7xx`, `-stm32wlxx`, `-samd21` | `master` 8364493, d2d9aa9, dbc58d7, a262e81 (fusions de `devenv/env-26`, poussées avec la branche) | « Fusion de devenv/env-26 (ENV-26 DBG-4 : SVD du MCU dans la famille, PA-40) » | oui |
| `bsp-nucleo-f429zi`, `-nucleo-f439zi`, `-stm32f746g-disco`, `-nucleo-wl55jc1`, `-samd21-xplained-pro` | `master` 2b2dfdd, bdbfa06, 6266908, c9183de, f3cffa2 (idem) | idem | oui |
| graine `original-tree`, `family-qemu-mps2`, BSP QEMU | inchangés | | oui |
| `<ROOTSTOCK>` | regreffé (13 feuilles `svd/` ajoutées) ; `lepton check` code 0 (19 fichiers) ; trunk : seul fichier régulier `.scion.grafted.list`, 0 lien cassé | | oui |

Hors dépôts : copie d'essai `~/lepton-tools-dev/essais/env-26-copie` (rootstock sans `build/` ni
`third_party/`) ; `<ROOTSTOCK>/build/` reconstruit à neuf pour `host` et les 10 presets de carte
(oracle après) ; `original-tree.code-workspace` régénéré par lepton 13633f5.

## Fait pendant la session
- Audit (`rapports/env-26-dbg4.md` §1) : SVD des packs `Keil::STM32F4xx_DFP` 3.1.1,
  `Keil::STM32F7xx_DFP` 3.1.1, `Keil::STM32WLxx_DFP` 2.1.0, `Microchip::SAMD21_DFP` 3.8.270,
  en-têtes Apache-2.0 relus ; anciens SVD de st.com (EULA ST) écartés ; OpenOCD 0.12.0 sans embOS ;
  rtos-views lit embOS et FreeRTOS par gdb ; symboles présents dans les ELF.
- lepton-tools 13633f5 : `svd` = chemin ou `{"famille": chemin}` (schéma), `check_family_files`
  (`checks.py`), `Context.svd_file` (`generate.py`), exemples, 2 tests ; `pytest` 222 verts ;
  `env-8-interface.md` §18 ; pipx depuis 13633f5.
- Greffons : `svd/` (SVD, `LICENSE-Apache-2.0`, `README.md` de provenance) dans 4 familles ;
  `"svd": {"famille": …}` dans 5 BSP ; `check-jsonschema` conforme.
- Contrôles (§3) : copie d'essai puis `<ROOTSTOCK>` regreffés (13 feuilles) ; `check` 0 ;
  `svdFile` dans les 10 lancements de carte ; oracle `oracles/env-26-{avant,apres}` (10 presets de
  carte, sections et symboles identiques ; empreintes : `__TIME__` seul, vérifié par une
  reconstruction sans modification).
- Essai VSCodium de l'utilisateur (§4) ; O-1, O-2 ; skill `lepton-cibles` §Vues (bf25879).
- PA-40 : fusions et push.

## Reste à faire dans l'étape
- Aucune tâche du fichier d'étape. Validation Debian (`svd` de famille, SVD greffés, vues) : ENV-28.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-39 : SVD versionnés (packs CMSIS), dans la famille, `svd` objet `{"famille": …}`, vue des tâches embOS + FreeRTOS par rtos-views sans champ `rtos`, pas de SVD QEMU, 4 cartes d'essai | utilisateur | oui |
| O-1 : contournement documenté (mode hexadécimal), `generate` inchangé, pas de signalement amont ; essai FreeRTOS ajouté | utilisateur | oui |
| PA-40 : fusions et push | utilisateur | oui |
| O-2 : activer `configRECORD_STACK_HIGH_ADDRESS` et `configUSE_TRACE_FACILITY` (piles FreeRTOS dans rtos-views) dans une étape qui accepte un changement des binaires | proposition non validée | prochaine action |
| `svdFile` omis si la famille du BSP n'est pas greffée (pas d'erreur de `generate`) | proposition de la session | `env-8-interface.md` §18 |

## Pièges rencontrés
- zsh : `G="git -C …"; $G switch` → « no such file or directory » (pas de découpage des mots) →
  fonction shell `g() { git -C "$clone" "$@"; }` ; aucune commande n'avait été exécutée.
- Le motif `chemin_relatif` interdit `..` : un BSP ne peut désigner un fichier de sa famille que
  par la forme objet.
- Oracle avant : les manifestes BSP sont des liens vers les clones ; les clones ont été repassés
  sur `master` pour capturer l'état de départ, puis remis sur `devenv/env-26` avant la regreffe.
- Arrêt initial dans `main` : avant `OS_Start`, rtos-views n'a rien à lister ; et en embOS, liste
  vide au format naturel (O-1) → « Enable Hex mode » puis nouvel arrêt.
- SAMD21 : le mauvais connecteur USB (pas l'EDBG) donne « GDB Server Quit Unexpectedly » ; la
  sonde CMSIS-DAP reste prise tant qu'une session VSCodium est ouverte.

## Critères de validation
- [x] PA-39 et PA-40 tranchés et consignés.
- [x] Un SVD déclaré par chaque BSP retenu ; `lepton check` code 0.
- [x] Registres lisibles et vue des tâches embOS constatés sur au moins une carte, sous VSCodium
  (SAMD21 ; tâches embOS avec le contournement O-1).
- [x] Symboles des presets de carte inchangés.

## Reprise
Commande ou première action de la session suivante :
```
démarre la session   # skill devenv-session ; ENV-27 (etapes/ENV-27-tst2-tests-greffon.md), audit jusqu'au PA-41
```
