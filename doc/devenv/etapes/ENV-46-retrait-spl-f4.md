# Étape ENV-46 — Famille STM32F4 : retrait de la SPL

## Contexte
Depuis ENV-35, la famille STM32F4 et les BSP `nucleo-f429zi`, `nucleo-f439zi` compilent la HAL ST
`v1.8.5`. La SPL ST (`driverlib/`) est restée dans l'arbre sans être compilée (décision PA-57). On
l'avait gardée pour le code non configuré par les presets, mis hors plan (A3 de `HORS-PLAN.md`).
Décision du 2026-11-09 (B3) : retirer la SPL, alors qu'A3 reste hors plan.

Il y a donc une **tension**, à trancher au PA-79 : après le retrait, les dépendants hors plan
perdent des fichiers qu'ils incluent. Aujourd'hui, aucun preset ne les compile.

Archétype : migration iso-fonctionnelle. Oracle : binaires identiques (code 0), puisque rien de
compilé ne change.

## Prérequis
- ENV-44 terminée.
- Famille : `<ROOTSTOCK>/depots/lepton/family-stm32f4xx/master`, `master` 7afd7f1. SPL :
  `scion/sys/root/src/kernel/dev/arch/cortexm/stm32f4xx/driverlib/`, 68 fichiers. Elle contient
  `stm32f4xx.h` (V1.0.2 modifié par Lepton), `stm32f407xx.h`, `stm32f429xx.h`, `stm32f469xx.h`, la
  pile ETH `stm32f4x7_eth.*` et `stm32f4xx_usart.c`, où Lepton a ajouté `USART_ChangeBaudrate`
  (`rapports/env-35-hal-f4.md` §1.7). Historique git de `driverlib/` dans la famille : 2 commits,
  3ef8e46 (import d'ENV-6) et 020db7b (ENV-35, retrait de 4 fragments HAL V1.3.0) ; l'historique
  antérieur est dans le clone noyau.
- Restent aussi dans la famille, non compilés :
  - `eth.c` et `dev_stm32f4xx_eth.c` (ancienne pile Ethernet sur l'ETH de la SPL), d'après le texte
    `description` du manifeste ;
  - `spi.c` (l. 30) et `dev_stm32f4xx/dev_stm32f4xx_spi_x.c` (l. 46), qui incluent
    `driverlib/stm32f4xx.h` ;
  - le CMSIS device V3.x `kernel/core/ucore/cmsis/Device/st/stm32f4xx/` (20 fichiers suivis :
    `stm32f4xx.h`, `system_stm32f4xx.{c,h}`, `startup/`, `Release_Notes.html`).
- Dépendants hors plan (relevé `grep -R` d'ENV-35, `rapports/env-35-hal-f4.md` §1.7) :
  - BSP du noyau `stm32f469i-eval` (3 références), `discovery_f4` (1),
    `discovery_f4-baseboard-modem` (13), `olimex_p407` (2) ;
  - `kernel/usb/stm32f4-usb-core` (inclusions sans chemin) ;
  - `cmsis/Device/st/stm32f4xx` (2) ;
  - XML `mkconf_tauon_basic_lwip_stm32f4-olimex-p407.xml`.
- Oracle de référence en vigueur après ENV-44 ou ENV-45.
- Skills `lepton-rootstock`, `lepton-oracle`, `lepton-cibles`.

## Tâches

### 1. Audit (lecture seule) → PA-79
- Refaire le relevé des dépendants sur le trunk actuel, **famille comprise** (le relevé d'ENV-35
  ne portait que sur les fichiers hors de la famille) : toute référence à `driverlib`, à un en-tête
  de la SPL (`stm32f4xx_<périph>.h`, `misc.h`, `stm32f4x7_eth.h`), à `eth.c` / `dev_stm32f4xx_eth.c`
  ou au CMSIS device V3.x F4, avec le fichier et le greffon de chaque référence. Chaque fichier non
  compilé de la famille (`dev_stm32f4xx/*`, `spi.c`, …) est classé : dépend de la SPL ou non.
- Vérifier, au niveau des fichiers objets et pas seulement au `grep`, qu'aucun preset ne compile ni
  n'inclut un fichier de la SPL : lire les fichiers de dépendances `.d` de la construction des
  16 presets.
- Recenser les documents qui citent la SPL : `description` du manifeste, `LEPTON-PROVENANCE.md`,
  `BUILDING.md`, skills, rapports vivants.
- Rapport `rapports/env-46-spl.md`, §1.
- **PA-79** : l'utilisateur tranche :
  - périmètre du retrait : `driverlib/` entier ; `eth.c`, `dev_stm32f4xx_eth.c` ; `spi.c`,
    `dev_stm32f4xx_spi_x.c` et les autres fichiers non compilés qui dépendent de la SPL ; CMSIS
    device V3.x F4 : <À CONFIRMER au PA-79> ;
  - sort des dépendants hors plan (tension avec A3) : les laisser avec des inclusions cassées et le
    signaler, les retirer aussi, ou les archiver : <À CONFIRMER au PA-79> ;
  - `USART_ChangeBaudrate` (ajout Lepton) : perdue avec la SPL, ou conservée ailleurs : <À CONFIRMER
    au PA-79> ;
  - conservation de l'historique : archive ou tag avant suppression : <À CONFIRMER au PA-79>.
- Aucune modification avant la réponse.

### 2. Oracle avant
Skill `lepton-oracle` : host et les 16 presets → `rapports/oracles/env-46-avant/`, conforme à la
référence ; liste triée des chemins du trunk et son `sha256`.

### 3. Retrait
- Famille : `git rm -r` du périmètre retenu, en un commit mécanique. Supprimer ensuite les
  répertoires restés sur le disque (`.DS_Store` ignorés).
- Famille : texte `description` du manifeste ; `LEPTON-PROVENANCE.md` et documents désignés au PA-79.
- Dépendants : selon le PA-79, dans leur greffon (noyau pour les BSP du noyau et `stm32f4-usb-core`).
- Regreffe selon la skill `lepton-rootstock` (`scion graft`, PA-P pour `<ROOTSTOCK>`).

### 4. Contrôles → PA-80
- Oracle après : code 0 sur host et les 16 presets ; `ctest -N` identiques ; fumée et KAL QEMU
  identiques.
- Liste des chemins du trunk : celle du §2 moins exactement les chemins retirés. 0 lien cassé,
  0 fichier régulier.
- `lepton check` code 0 sur `<ROOTSTOCK>` et sur un rootstock neuf
  (`~/lepton-tools-dev/essais/env-46-vierge`). La famille n'étant pas publiée, il faut une graine
  d'essai locale, avec la famille en `file://` de la branche `devenv/env-46` (forme d'ENV-41 §3.4).
- Carte NUCLEO-F429ZI : banc 20/20 en embOS, réseau compris (contrôle de non-régression, PA-11).
- **PA-80** : rapport ; push et fusions des branches `devenv/env-46` (PA-P).

## Critères de validation
- [ ] PA-79 et PA-80 tranchés et consignés.
- [ ] Plus aucun fichier de la SPL dans `family-stm32f4xx`, dans le périmètre retenu.
- [ ] Binaires identiques (code 0).
- [ ] Dépendants hors plan traités selon le PA-79 et inscrits au rapport et dans `HORS-PLAN.md` A3.

## Pièges connus
- `stm32f4xx.h` existe en trois versions dans la famille ou par elle : SPL (`driverlib/`, modifiée),
  CMSIS device V3.x (`ucore/cmsis/Device/st/stm32f4xx/`), CMSIS device projeté
  (`ucore/cmsis-5/Device/ST/STM32F4xx/Include/`). Après le retrait, toute inclusion sans chemin doit
  trouver celle du CMSIS device projeté. Le vérifier dans les `.d`.
- Recherche des dépendants : `freeRTOS_8-0-0` et `freeRTOS_9-0-0`
  (`…/arch/cortex-m4/stm32f4/main.c`, clone noyau) incluent `kernel\dev\arch\cortexm\stm32f4xx\driverlib\misc.h`
  avec des barres obliques inverses : un `grep driverlib/` ne les voit pas. À l'inverse,
  `grep driverlib` attrape aussi `stellaris/driverlib`, sans rapport.
- Le volume du Mac ne distingue pas la casse : contrôler la liste des chemins retirés sur leur nom
  exact.
- Mettre à jour `description` du manifeste : texte exact, pour le lecteur (lepton ne lit pas ce
  champ).
- Si ENV-45 n'est pas faite, le banc NUCLEO-F429ZI se passe WL55 débranchées : le BSP F429 prend la
  première sonde trouvée (O-1 d'ENV-42).
- Les rootstocks d'essai du Mac et de la VM ne sont pas regreffés avant ENV-50.
- Ne toucher ni à la projection (`scion/.scion/`), ni à `hal_driver/`, ni au CMSIS device.

## À la fin de l'étape
`DEVENV-STATUS.md` :
- statut et branches ;
- décisions PA-79 et PA-80 ;
- nombre de liens de `<ROOTSTOCK>` ;
- journal.

`HORS-PLAN.md` : B3 et A3 mis à jour. Passation `handoff/env-46.md`.
