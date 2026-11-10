# Passation ENV-49 — Famille STM32WL : montée de version de la HAL — session du 2026-11-10

## Statut
Terminée. Le code tiers WL est monté au couple de STM32CubeWL `v1.6.0` :
- HAL `v1.6.0` ;
- CMSIS device `v1.4.0` ;
- SubGHz_Phy `v1.5.0` ;
- utilitaires et `utilities_def.h` de STM32CubeWL `v1.6.0`.

La couche Lepton et le BSP n'ont pas changé. Les binaires WL55 changent dans le critère du PA-85.
Le banc WL55 A/B donne 16/16 sur 4 passes avant comme après, radio comprise. PA-85 et PA-86 sont
tranchés, et tout est publié.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` | fusion de `devenv/env-49` ; `main` et la branche poussés | oui |
| `family-stm32wlxx` | `master` | 9349be2 Fusion de devenv/env-49 (ENV-49 couple de STM32CubeWL v1.6.0 …, PA-86). Branche bfbeb1b, poussée | oui |
| clone noyau `depots/lepton/original/master` | `master` | 76f28bd, non touché | oui |
| autres | `master` / `original-tree` | non touchés : F7 12280a5, F4 acdd24c, WL55 4d7cf80, graine 15740f9, seed.scions 7e8a0cc ; miroirs WL inchangés (les tags visés y étaient déjà) | oui |

État de `<ROOTSTOCK>` :
- liens : 3889, soit les 3888 d'ENV-48 plus `radio_subghz_phy/Conf/radio_template.h` ;
- `chemins-cibles.txt` 5dbbc69f… ; 0 lien cassé, 0 fichier régulier ;
- 629 liens projetés (F4 206, F7 201, WL 222) ; liste greffée : 23 entrées ;
- clones tiers WL actifs : `depots/tiers/stm32wlxx-hal-driver/v1.6.0`, `cmsis-device-wl/v1.4.0`,
  `stm32-mw-subghz-phy/v1.5.0`, `stm32cubewl/v1.6.0` (partagé par les deux clés `stm32cubewl::*`,
  156 Mo) ;
- anciens clones `stm32wlxx-hal-driver/v1.3.0`, `cmsis-device-wl/v1.1.1`, `stm32-mw-subghz-phy/v1.3.0`,
  `stm32cubewl/v1.3.0` (372 Mo, P-V5) : **supprimés par l'utilisateur** le 2026-11-10, absence
  contrôlée par la session (0 lien cassé, `lepton check` code 0) ;
- `lepton check` code 0 ; espace de travail inchangé ; tous les clones sur `master` et propres.

Outils : scion 0.6.2.0 et lepton 0.1.0, inchangés (pas de réinstallation). La VM a toujours
scion 0.6.1.0 (ENV-50).

Oracle de référence Mac : `oracles/env-49-apres/`.

Cartes : les deux NUCLEO-WL55JC1 sont branchées, avec l'image `nucleo-wl55jc1-freertos`.
- A 002700253431510837393937 : `/dev/cu.usbmodem1454303` ;
- B 004F003E3431510937393937 : `/dev/cu.usbmodem145103`.

Ports relevés par `ioreg` deux fois dans la session, identiques à ENV-48.

## Fait pendant la session
- **Audit** (rapport §1, `rapports/env-49-wl-hal/audit/`) :
  - couples de STM32CubeWL de `v1.3.0` à `v1.6.0` (`couples.txt`) : seul `v1.6.0` a 3
    sous-modules égaux à des tags ;
  - simulation des projections (`proj.py`, `projeter.sh`) : la HAL, le CMSIS device et les
    utilitaires gardent leurs noms ;
  - SubGHz_Phy est restructuré en `v1.4.0` (`radio_driver/`) ;
  - reports `radio.c` et `stm32_timer.h` sans conflit (`propose/reports/reporter.sh`) ;
  - `stm32_hal_legacy.h` n'est plus inclus en HAL `v1.6.0` ;
  - essai sur une copie d'essai : WL55 code 0, 26 symboles.
- **PA-85** (rapport §1.8, §1.9) et **PA-11**.
- **Oracle avant** (§2) : `env-49-avant` = `env-48-apres`. Banc de référence (§2.1) : 16/16 ×4,
  radio 20/20.
- **Famille** (§3.1), 4 commits sur la copie :
  - c85859b : porteur ;
  - b86aaf3 : `git rm` de `stm32_hal_legacy.h`, mécanique ;
  - 9377ad1 : reports ;
  - bfbeb1b : provenances et `description`.
- **Bascule de `<ROOTSTOCK>`** (§3.2, PA-P accordé) :
  - fetch de la branche depuis la copie ;
  - `scion seed-clone --seed depots/lepton-seed.scions/original-tree` ;
  - `scion graft` ;
  - liste `chemin -> cible` = attendu.
- **Contrôles** (§4) :
  - oracle après : 14 presets et host code 0 ; WL55 conformes au critère (`.text` +48 ×2) ;
  - banc après : 16/16 ×4 ;
  - GDB sur la WL55 A : tâches FreeRTOS et `RCC_CR` lus (`rootstock/gdb-rtos-freertos.log`).
- **PA-86** :
  - famille publiée (9349be2 et la branche), puis lepton-tools ;
  - `essais/env-49-copie` supprimée ;
  - `HORS-PLAN.md` : B2 traité, D11 atténué.

## Reste à faire dans l'étape
- [x] Rien pour la session.
- [x] **Action de l'utilisateur** (PA-85 Q4), faite le 2026-11-10 et contrôlée : supprimer les 4 anciens clones WL de `<ROOTSTOCK>`.
  Le hook interdit à la session d'écrire sous `depots/tiers/`. Aucun lien ne les vise (vérifié). Commande :
  ```
  ! rm -rf ~/lepton/depots/tiers/stm32wlxx-hal-driver/v1.3.0 ~/lepton/depots/tiers/cmsis-device-wl/v1.1.1 ~/lepton/depots/tiers/stm32-mw-subghz-phy/v1.3.0 ~/lepton/depots/tiers/stm32cubewl/v1.3.0
  ```
  Ensuite, contrôler par `cd ~/lepton && find -L trunk -type l | wc -l` (attendu 0) et
  `lepton check` (code 0).

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-85 Q1 : couple de STM32CubeWL `v1.6.0`, périmètre complet | utilisateur | oui |
| PA-85 Q2 : lignes SubGHz « A », chemins du trunk conservés, `Conf/radio_template.h` projeté (+1) | utilisateur | oui |
| PA-85 Q3 : `stm32_hal_legacy.h` de la HAL `v1.6.0` projeté, copie de la famille retirée | utilisateur | oui |
| PA-85 Q4 : reports, couche Lepton et BSP inchangés, critère d'écart WL55, description et provenances, anciens clones supprimés par l'utilisateur | utilisateur | oui |
| PA-11 : flash des deux WL55, bancs avant et après, deux passes | utilisateur | oui |
| PA-P : bascule de `<ROOTSTOCK>` (`seed-clone`, `graft`) | utilisateur | oui |
| PA-86 : référence `env-49-apres`, publication, copie supprimée, B2 traité, D11 atténué | utilisateur | oui |
| Correctifs Lepton gardés en `.patch` avec un script de report, sans copie du code ST dans lepton-tools | proposition de la session | rapport §1.4 |
| Contrôle SVD et rtos-views fait par GDB en lot (FreeRTOS, `RCC_CR`) et par un contrôle statique, sans ouvrir les vues de VSCodium | proposition de la session | rapport §4.4 |

## Pièges rencontrés
- **`__FILE__` dans les `configASSERT` de FreeRTOS** : sur une copie d'essai, le chemin absolu du
  trunk est plus long et `.text` gagne 30 octets par fichier FreeRTOS. Il faut comparer les
  binaires d'une copie à la référence par objet (`map-objets.py`), ou sur `<ROOTSTOCK>`.
- **zsh** :
  - `set -- $var` ne découpe pas les mots ;
  - `local path=…` écrase `PATH` (la variable `path` y est liée à `PATH`) ;
  - `r` est une commande interne.
  Écrire les boucles dans des scripts bash.
- **Exclusion de projection** : `!motif` retire le fichier de toutes les lignes de la clé (P-X1).
  Pour placer certains fichiers d'un répertoire ailleurs, il faut les nommer un à un, et non
  exclure puis réinclure.
- **P-V5** : un changement de version laisse l'ancien clone en place. Le hook interdit à la session
  de le supprimer : c'est à l'utilisateur.
- **Clone de lecture `~/lepton-tools-dev/tiers/STM32CubeWL`** : son index ne correspond à aucun tag
  (laissé par ENV-37). Lire par `git show` et `git ls-tree`, jamais par l'index.

## Critères de validation
- [x] PA-85 et PA-86 tranchés et consignés.
- [x] Code tiers WL à la version retenue, couple cohérent, version du CMSIS device inscrite.
- [x] Modifications Lepton reportées et documentées dans la provenance.
- [x] Banc WL55 A/B radio comprise identique à la référence ; host et 14 presets non WL code 0.

## Rootstocks à regreffer en ENV-50
Tous ont encore la famille WL en 2340b25, l'état d'avant ENV-48. Un `graft-update` les mène
directement à 9349be2, et crée les 4 clones WL `v1.6.0`, `v1.4.0`, `v1.5.0` et `v1.6.0` depuis les
miroirs (STM32CubeWL : environ 156 Mo). Il exige scion ≥ 0.6.1.0.

Les liens du trunk sont ceux d'ENV-48 (−8 `LICENSE.txt`, +9 `LICENSE.md`), plus
`Conf/radio_template.h`.
- Mac : `essais/env-13-vierge`, `essais/env-41-vierge` (s'il est gardé), `essais/env-11/wl55jc1`.
- VM : `essais/env-28-debian` et `essais/env-43-debian`, après l'installation de scion 0.6.2.0 et
  de lepton depuis `main`.

## Reprise
Commande ou première action de la session suivante :
```
démarre la session ENV-50 (skill devenv-session) ; référence Mac oracles/env-49-apres ;
méthode et scripts de rapports/env-49-wl-hal.md (bancs.sh, liens.py) ; relever les ports des WL55
par ioreg avant le banc
```
