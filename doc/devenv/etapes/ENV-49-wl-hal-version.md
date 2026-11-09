# Étape ENV-49 — Famille STM32WL : montée de version de la HAL

## Contexte
La famille STM32WL compile la HAL ST `v1.3.0`. En amont, la dernière version est `v1.6.0`. Le couple
actuel n'est pas cohérent : HAL de STM32CubeWL `v1.3.0`, CMSIS device `v1.1.1` (soit STM32CubeWL
`v1.2.0`). En plus, le manifeste ne donne pas la version du CMSIS device
(`rapports/env-37-wl-provenance.md` §1.8, constats 1 et 7). Décision du 2026-11-09 (B2 de
`HORS-PLAN.md`) : monter de version.

Depuis ENV-48, le code tiers WL est projeté. La montée de version consiste donc à :
- changer les révisions épinglées dans le porteur ;
- reporter sur les nouvelles versions les fichiers modifiés par Lepton, qui restent dans la famille ;
- adapter la couche Lepton aux changements d'API.

Une seule variable : la version du code tiers WL. **Les binaires des 2 presets WL55 changent.**

Archétype : migration avec écart accepté. Oracle : critère d'écart fixé au PA-85 ; validation par
exécution sur les cartes (banc WL55 A/B, radio comprise).

## Prérequis
- ENV-48 terminée : porteur `scion/.scion/` de `family-stm32wlxx`, miroirs WL.
- Tags amont relevés le 2026-11-09 par `git ls-remote` (à relever de nouveau au §1) :
  - `stm32wlxx-hal-driver` jusqu'à `v1.6.0` ;
  - `cmsis-device-wl` jusqu'à `v1.4.0` ;
  - `stm32-mw-subghz-phy` jusqu'à `v1.5.0` ;
  - `STM32CubeWL` jusqu'à `v1.6.0`.
  À `v1.6.0`, STM32CubeWL désigne ses composants par sous-modules (relevé `git ls-tree` du clone
  partiel `~/lepton-tools-dev/tiers/STM32CubeWL`) : HAL 5c87cf0 = `v1.6.0`, CMSIS device 71a0b78 =
  `v1.4.0`, SubGHz_Phy 7dc059f = `v1.5.0` ; les utilitaires restent dans son arbre. Le couple de
  `v1.4.0` et de `v1.5.0` reste à relever.
- Fichiers modifiés par Lepton ou dérivés (`rapports/env-38-projection.md` §5,
  `rapports/env-37-wl-provenance.md`) :
  - `radio.c`, avec `RadioIsChannelFree` neutralisée (documentée en ENV-48, C1) ;
  - `stm32_timer.h`, `subghz.h`, `utilities_conf.h`, `platform.h` ;
  - `stm32_hal_legacy.h`, qui vient d'une autre révision.
- Presets WL55 (`CMakePresets.json` du trunk) : `nucleo-wl55jc1-embos`, `nucleo-wl55jc1-freertos`.
- Banc radio : `rapports/env-42-core-cm4/banc-wl55.sh`, WL55 A n° 002700253431510837393937 et B
  n° 004F003E3431510937393937 sur le Mac (`rapports/env-42-core-cm4.md`). Le banc passe
  `-DLEPTON_BOARD_STLINK_SERIAL` : prendre la variable en vigueur après ENV-45.
- Skills `lepton-rootstock`, `lepton-oracle`, `lepton-cibles`.

## Tâches

### 1. Audit (lecture seule) → PA-85
- Pour chaque version de STM32CubeWL de `v1.3.0` à `v1.6.0` : versions de la HAL, du CMSIS device,
  de SubGHz_Phy et des utilitaires (notes de version, sous-modules). En tirer les couples cohérents.
- Diff de la version actuelle à la version candidate, pour chaque ensemble projeté :
  - API utilisées par la couche Lepton (`dev_stm32wlxx*`, BSP `nucleo-wl55jc1`) ;
  - fichiers ajoutés ou retirés en amont, motifs de projection touchés ;
  - les 6 fichiers que la famille garde (`stm32_hal_legacy.h` compris). Si le couple retenu est celui
    d'une version à sous-modules, `stm32_hal_legacy.h` peut venir de la HAL séparée elle-même :
    l'exception « autre révision » d'ENV-38 §5 tombe peut-être.
- Report des modifications Lepton : pour chaque fichier modifié, diff amont ancienne → nouvelle
  version, et application de la modification Lepton sur la nouvelle.
- Compilation à blanc de la nouvelle HAL dans les presets WL55, sur une copie d'essai.
- Rapport `rapports/env-49-wl-hal.md`, §1.
- **PA-85** : l'utilisateur valide :
  - les versions cibles (couple d'une seule version de STM32CubeWL) et le périmètre (HAL seule, ou
    HAL, CMSIS device, SubGHz_Phy et utilitaires) : <À CONFIRMER au PA-85> ;
  - le report de chaque fichier modifié par Lepton ;
  - les changements de la couche Lepton ;
  - le critère d'écart des presets WL55, et `code 0` exigé pour host et les 14 autres presets ;
  - les cartes et l'écriture flash (PA-11) ;
  - la version du CMSIS device dans `description` du manifeste.
- Aucune modification avant la réponse.

### 2. Oracle avant
Skill `lepton-oracle` : host et les 16 presets → `rapports/oracles/env-49-avant/`, conforme à la
référence ; banc WL55 A/B de référence relevé.

### 3. Montée de version
Copie d'essai d'abord (`rsync -a` sans `build/` ni `third_party/`), puis `<ROOTSTOCK>` (PA-P). Un
commit par lot :
1. Révisions épinglées du porteur (`.scion.sources.list`, `.scion.ramifications`), motifs de
   projection si l'amont a changé. Les miroirs doivent contenir les nouvelles révisions : faire un
   `scion mirror-sync` avant tout (`--dry-run` d'abord ; l'envoi est un push, PA-P).
2. Fichiers modifiés par Lepton, reportés.
3. Couche Lepton et BSP, si l'API a changé.
4. `LEPTON-PROVENANCE.md`, `description` du manifeste.
5. Regreffe comme en ENV-41 §3.5 : `scion seed-clone --seed depots/lepton-seed.scions/original-tree`
   (crée les clones tiers des nouvelles révisions), puis `scion graft` ; pas de `graft-update`.

### 4. Contrôles → PA-86
- Oracle après : code 0 sur host et les 14 presets hors WL55 ; presets WL55 dans le critère du PA-85,
  écarts expliqués symbole par symbole au rapport.
- Banc WL55 A/B, en embOS et en FreeRTOS, radio comprise : nombre de tests et résultats identiques
  à la référence. Une variation est expliquée ou bloque.
- Contenu projeté = nouveaux commits épinglés ; liste des chemins conforme aux ajouts et retraits
  de l'amont ; 0 lien cassé.
- Vue des périphériques (SVD) et rtos-views sur la WL55 : toujours lisibles.
- Nouvel oracle de référence `oracles/env-49-apres/`.
- **PA-86** : rapport ; publication (miroirs, famille, BSP s'il est touché), push et fusions
  (PA-P).

## Critères de validation
- [ ] PA-85 et PA-86 tranchés et consignés.
- [ ] Code tiers WL à la version retenue, couple cohérent, version du CMSIS device inscrite.
- [ ] Modifications Lepton reportées et documentées dans la provenance.
- [ ] Banc WL55 A/B radio comprise identique à la référence ; host et 14 presets non WL code 0.

## Pièges connus
- Une nouvelle HAL peut changer les noms de macros de `stm32_hal_legacy.h` : la copie de la famille
  vient d'une autre révision. La remplacer ou la garder fait partie du PA-85.
- Le tick HAL, les priorités d'IRQ et l'horloge de la radio sont sensibles : un banc radio en échec
  intermittent n'est pas « identique ». Lancer chaque banc deux fois.
- `RadioIsChannelFree` reste neutralisée : le report garde le `#if 0`, sauf décision contraire.
- Un écart de `.text` absorbé par le bourrage d'alignement efface la ligne `section modifié` :
  comparer d'abord la croissance des symboles (`handoff/env-43.md`).
- Le miroir de STM32CubeWL ne contient pas le contenu des sous-modules : sans effet tant que seules
  les utilitaires y sont projetées ; à revoir si une projection vise un sous-module.
- Les rootstocks d'essai du Mac et de la VM ne sont pas regreffés avant ENV-50.
- Ne toucher ni au F4 ni au F7.

## À la fin de l'étape
`DEVENV-STATUS.md` :
- statut et branches ;
- décisions PA-85 et PA-86 ;
- §Versions : code tiers STM32WL ;
- oracle de référence ;
- journal.

`HORS-PLAN.md` : B2. Passation `handoff/env-49.md`.
