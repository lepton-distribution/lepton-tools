# Étape ENV-48 — Famille STM32WL : copie remplacée par la projection

## Contexte
ENV-37 a établi la provenance du code tiers de la famille STM32WL, sans rien recopier. ENV-38 a
écrit ce cas dans le format de projection (`rapports/env-38-projection.md` §2.3). Décision du
2026-11-09 (B1 de `HORS-PLAN.md`) : le WL bascule à son tour sur la projection, après le F7
(ENV-47).

C'est le cas le plus riche :
- renommage de casse (`Inc` → `inc`) ;
- aplatissement de chemins ;
- exclusion des fichiers modifiés par Lepton, qui restent dans la famille ;
- deux clés qui partagent un clone partiel de STM32CubeWL ;
- deux dépôts amont pour `radio_subghz_phy/`.

Le cas F4 (ENV-41) n'utilise aucune de ces fonctions de scion : elles n'ont passé que les tests
d'ENV-39 et l'essai à blanc du F4. La version reste celle
d'aujourd'hui (HAL `v1.3.0`) : la montée de version est l'objet d'ENV-49. **Rien de compilé ne
change.**

Décisions du 2026-11-09 prises dans cette étape :
- C1 : documenter en l'état la neutralisation de `RadioIsChannelFree` ; le binaire ne change pas.
- C2 : décider ici du sort des 8 `LICENSE.txt` hors amont.

Archétype : migration iso-fonctionnelle. Oracle : binaires identiques.

## Prérequis
- ENV-47 terminée (méthode éprouvée sur le F7, miroirs créés selon le PA-81).
- Famille : `<ROOTSTOCK>/depots/lepton/family-stm32wlxx/master`, `master` 2340b25 ; 4
  `LEPTON-PROVENANCE.md` :
  - `kernel/dev/arch/cortexm/stm32wlxx/cubemx_hal_driver/` ;
  - `kernel/dev/arch/cortexm/stm32wlxx/Utilities/` ;
  - `kernel/dev/arch/cortexm/stm32wlxx/radio_subghz_phy/` ;
  - `kernel/core/ucore/cmsis/Device/st/stm32wlxx/`.
- Révisions (`DEVENV-STATUS.md` §Versions, ENV-37) :
  - HAL `stm32wlxx-hal-driver` `v1.3.0` e3966ab ;
  - CMSIS device `cmsis-device-wl` `v1.1.1` d248c55 ;
  - SubGHz_Phy `stm32-mw-subghz-phy` `v1.3.0` 1cad768 ;
  - utilitaires et `stm32_radio_core_inc/` : STM32CubeWL `v1.3.0` 378e461.
- Cas d'épreuve et attendus (`rapports/env-38-projection/attendus/`) : `wl-hal.txt` (155),
  `wl-cmsis-device.txt` (5), `wl-radio.txt` (18), `wl-stm32cubewl.txt` (32 + 1).
- Restent dans la famille d'après le §2.3 :
  - `stm32_hal_legacy.h` ;
  - `radio.c`, `stm32_timer.h` et 3 fichiers de `stm32_radio_core_inc/` (modifiés) ;
  - les `LICENSE.txt` ×8 ;
  - les 4 `LEPTON-PROVENANCE.md`.
- C1 : `radio_subghz_phy/stm32_radio_driver/radio.c`, corps de `RadioIsChannelFree` sous `#if 0`
  (`rapports/env-37-wl-provenance.md` §1.8 constat 6, `diffs/radio.c.diff`).
- C2 : `rapports/env-37-wl-provenance.md` §1.4.
- Clones amont : `~/lepton-tools-dev/tiers/` (ENV-37), tous à leur dernière version et non aux
  révisions épinglées : comparer contre les tags. Copies de comparaison :
  `~/lepton-tools-dev/essais/env-37-compare/`.
- Méthode de la première synchronisation des miroirs : E13 d'ENV-40, reprise en ENV-47 §2 (graine
  de publication `essais/env-40-publication/`, `mirror-sync --seed`).
- Effets d'un correctif de scion : `SCION_MIN_VERSION` de lepton, `SCION_REF` d'`install-vscodium.sh`
  et d'`install-{macos,debian}.sh` du clone noyau (`DEVENV-STATUS.md` §Versions, ligne scion).
- Skills `lepton-rootstock`, `lepton-oracle`, `lepton-cibles`.

## Tâches

### 1. Audit (lecture seule) → PA-83
- Écrire le `scion/.scion/` de la famille d'après le §2.3, avec les URL des miroirs.
- Essai à blanc sur une copie d'essai de `<ROOTSTOCK>` : chaque fonction de scion que le cas
  sollicite (renommage de casse, clone partagé, exclusions, deux amonts) donne la liste attendue.
  Un écart est un défaut de scion ou du cas : le décrire au rapport, sans le corriger.
- Taille de STM32CubeWL. Faisabilité d'un miroir complet, ou d'une autre forme compatible avec la
  spécification (règles M-*) : relever, sans choisir.
- C1 : chercher la raison de la neutralisation. Dans la famille, l'historique de `radio.c`
  commence à l'import d'ENV-6. L'origine est dans le clone noyau : efa8106 « added files from
  stm32cubemx-win-v6-11-0 and stm32cubewl-v1-3-0 », puis 8d5a082 (extraction d'ENV-6). La
  modification est donc antérieure ou égale à l'import efa8106. Voir aussi
  `<ROOTSTOCK>/depots/lepton/original/master/doc/migration/MIGRATION-STATUS.md` (elle n'y figure pas,
  `rapports/env-37-wl-provenance.md`) et les appelants de `RadioIsChannelFree` dans Lepton.
- Rapport `rapports/env-48-wl-projection.md`, §1.
- **PA-83** : l'utilisateur valide :
  - les lignes de projection, URL et révisions ;
  - les 4 miroirs (noms, visibilité, création), dont celui de STM32CubeWL : <À CONFIRMER au PA-83> ;
  - un correctif de scion s'il en faut un : <À CONFIRMER au PA-83>. Option recommandée par le plan :
    étape scion insérée (forme d'ENV-29, ENV-39), la bascule restant suspendue jusqu'à elle. Sinon,
    l'étape changerait deux variables. Le correctif entraîne une nouvelle version, sa publication
    (PA-P), `SCION_MIN_VERSION` et `SCION_REF` ;
  - C1 : la raison de la neutralisation à écrire dans `radio_subghz_phy/LEPTON-PROVENANCE.md`. Si
    aucune n'est établie, l'écrire comme non établie : <À CONFIRMER au PA-83> ;
  - C2 : sort des 8 `LICENSE.txt`, et ajout ou non des `LICENSE.md` amont aux projections :
    <À CONFIRMER au PA-83> ;
  - sort des `LEPTON-PROVENANCE.md`.
- Aucune modification avant la réponse.

### 2. Miroirs
Méthode d'ENV-47 §2 (le porteur n'existe pas encore) : dépôts créés selon le PA-83 ; lignes WL
ajoutées au `.scion.mirrors` de la graine de publication ; `scion mirror-sync --seed <graine>`,
d'abord `--dry-run`, puis l'envoi (PA-P). Contrôle `git ls-remote` ; révisions épinglées
atteignables.

### 3. Oracle avant
Skill `lepton-oracle` : host et les 16 presets → `rapports/oracles/env-48-avant/` ; liste triée des
chemins du trunk, casse comprise, et son `sha256`.

### 4. Bascule
D'abord sur la copie d'essai (`rsync -a` sans `build/` ni `third_party/`), puis sur `<ROOTSTOCK>`
(PA-P) :
1. Famille : `scion/.scion/`, commit.
2. Famille : `git rm` des fichiers projetés, un commit mécanique par ensemble tiers. Les fichiers
   qui restent dans la famille ne bougent pas.
3. Famille : `LEPTON-PROVENANCE.md` (C1 compris), `LICENSE.txt` (C2), `description` du manifeste.
4. Regreffe comme en ENV-41 §3.5 et ENV-47 §5 : `scion seed-clone --seed
   depots/lepton-seed.scions/original-tree`, puis `scion graft`. Pas de `graft-update` : la famille
   est sur `devenv/env-48`, hors de sa version déclarée.

### 5. Contrôles → PA-84
- Liste des chemins du trunk identique à celle du §3, casse comprise, aux écarts accordés près ;
  +211 cibles WL sous `depots/tiers/`, 618 en tout (F4 206, F7 201), au sort des `LICENSE.md` près
  (C2) ; 0 lien cassé, 0 fichier régulier.
- Oracle après : code 0 sur host et les 16 presets ; `ctest -N`, fumée et KAL identiques.
- Contenu projeté = commits épinglés.
- Rootstock neuf `~/lepton-tools-dev/essais/env-48-vierge`, depuis une graine d'essai locale (famille
  en `file://` de `devenv/env-48`, forme d'ENV-41 §3.4) : même liste, `lepton check` code 0.
- `lepton check`, `generate`, `seed status`, `file owner` sur `<ROOTSTOCK>` ; `seed lock` sur un
  rootstock à graine de projet qui greffe la famille WL (refusé sur la graine de référence,
  `lepton/seed.py:823`) : clés WL reconnues, clone partagé compris.
- Banc WL55 A/B, en embOS et en FreeRTOS, radio comprise : identique à la référence (PA-11).
- **PA-84** : rapport ; publication (miroirs, scion s'il a changé, famille), push et fusions (PA-P).

## Critères de validation
- [ ] PA-83 et PA-84 tranchés et consignés.
- [ ] Binaires identiques (code 0) ; liste des chemins identique, casse comprise.
- [ ] Ne restent dans la famille que les fichiers modifiés ou hors amont, et la provenance.
- [ ] `RadioIsChannelFree` documentée dans la provenance (C1) ; C2 tranché et appliqué.

## Pièges connus
- Casse : le volume du Mac ne distingue pas `Inc` de `inc`. Seule la VM (ENV-50) prouve la casse.
  Comparer ici les noms dans la liste des liens, pas par `ls`.
- `stm32_hal_legacy.h` vient d'une autre révision (STM32CubeWL) que la HAL séparée : il reste copié
  (rapport d'ENV-38 §5). Ne pas en faire une clé.
- Deux clés `stm32cubewl::*` partagent `depots/tiers/stm32cubewl/v1.3.0` (P-V2) : un `graft-remove`
  de l'une ne doit pas retirer le clone de l'autre.
- Compter les liens projetés par ensemble (HAL, CMSIS device, radio, STM32CubeWL), pas par
  répertoire : `radio_subghz_phy/` mêle deux amonts et des fichiers de la famille.
- Ne pas monter de version ici : c'est ENV-49.
- Si scion change : la famille publiée exige ce scion. Un rootstock qui fait `graft-update` avec un
  scion plus ancien greffe la famille sans code tiers. Publier scion et lepton d'abord (piège
  d'ENV-41).
- Les rootstocks d'essai du Mac et de la VM ne sont pas regreffés avant ENV-50.

## À la fin de l'étape
`DEVENV-STATUS.md` :
- statut et branches ;
- décisions PA-83 et PA-84 ;
- §Emplacements : code tiers WL projeté, miroirs ;
- §Versions : scion s'il a changé ;
- journal.

`HORS-PLAN.md` : B1, C1, C2. Passation `handoff/env-48.md`.
