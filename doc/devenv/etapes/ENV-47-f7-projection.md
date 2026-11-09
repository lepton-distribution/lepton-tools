# Étape ENV-47 — Famille STM32F7 : copie remplacée par la projection

## Contexte
ENV-41 a remplacé par la projection scion la copie de la HAL et du CMSIS device F4. La famille F4
servait de pilote ; le F7 et le WL étaient renvoyés à la révision suivante. Décision du 2026-11-09
(B1 de `HORS-PLAN.md`) : basculer le F7, puis le WL (ENV-48), chacun avec ses miroirs de conservation
sous `lepton-distribution/`.

Le F7 vient en premier parce que c'est le cas le plus simple : même forme que le F4
(`rapports/env-38-projection.md` §2.2), et copies déjà identiques à l'amont (vérification d'ENV-34).
**Rien de compilé ne change** : les chemins du trunk restent les mêmes, seule la cible des liens
change.

Archétype : migration iso-fonctionnelle. Oracle : binaires identiques.

## Prérequis
- ENV-44 terminée. scion 0.6.1.0 (projection et miroir) ; lepton reconnaît les clés projetées
  depuis ENV-41.
- Copie à remplacer, dans `<ROOTSTOCK>/depots/lepton/family-stm32f7xx/master/scion/sys/root/src/`
  (`master` d2d9aa9) :
  - `kernel/dev/arch/cortexm/stm32f7xx/hal_driver/` : 197 fichiers, soit 196 fichiers amont et
    `LEPTON-PROVENANCE.md` ;
  - `kernel/core/ucore/cmsis-5/Device/ST/STM32F7xx/` : `Include/stm32f7xx.h`,
    `Include/system_stm32f7xx.h`, `Include/stm32f746xx.h`, `LICENSE.md`, `README.md`,
    `LEPTON-PROVENANCE.md`.
- Révisions : `stm32f7xx-hal-driver` `v1.3.3` = e1446fa12ffda80ea1016faf349e45b2047fff12 ;
  `cmsis_device_f7` `v1.2.10` = 2352e888e821aa0f4fe549bd5ea81d29c67a3222 (`DEVENV-STATUS.md`
  §Versions, relevés dans les clones amont).
- Cas d'épreuve : `rapports/env-38-projection.md` §2.2 ; attendus
  `rapports/env-38-projection/attendus/f7-hal.txt` (196) et `f7-cmsis-device.txt` (5).
- Modèle d'exécution : `etapes/ENV-41-f4-projection.md`, `rapports/env-41-f4-projection.md`. Le
  `scion/.scion/` de `family-stm32f4xx` sert d'exemple.
- Miroirs F4 existants (`DEVENV-STATUS.md` §Emplacements, ENV-40) ; envoi par la configuration
  `pushInsteadOf` de l'utilisateur (PA-68).
- Clones amont : `~/lepton-tools-dev/tiers/stm32f7xx-hal-driver` (HEAD e860c4f = `v1.3.3-19`, pas
  le tag), `cmsis_device_f7`. Toute comparaison se fait contre le tag, pas contre HEAD.
- Première synchronisation de miroirs neufs : méthode E13 d'ENV-40 (`rapports/env-40-miroir.md`).
  La graine de publication `~/lepton-tools-dev/essais/env-40-publication/` (rootstock `--bare`,
  `.scion.mirrors` seul dans le `.scion/` de la graine) se synchronise par `mirror-sync --seed`.
- Skills `lepton-rootstock`, `lepton-oracle`, `lepton-cibles`.

## Tâches

### 1. Audit (lecture seule) → PA-81
- Écrire le `scion/.scion/` de la famille (sources, ramifications, projections, miroirs) d'après le
  §2.2 et le porteur F4. Les URL sont celles des miroirs.
- Liste attendue des chemins du trunk : celle d'aujourd'hui, au sort des `LEPTON-PROVENANCE.md`
  près (conduite du PA-69 pour le F4).
- Recenser les rootstocks et les graines qui greffent `family-stm32f7xx` (Mac et VM) et la version de
  scion de chacun.
- Contrôler le contenu actuel contre l'amont (`scripts/tiers/verifier-import.sh`, F7) : 0 écart
  attendu.
- Rapport `rapports/env-47-f7-projection.md`, §1.
- **PA-81** : l'utilisateur valide :
  - les lignes de projection, URL et révisions ;
  - les miroirs `lepton-distribution/mirror-stm32f7xx-hal-driver` et
    `lepton-distribution/mirror-cmsis_device_f7` : noms, visibilité, création par qui (forme du
    PA-68) : <À CONFIRMER au PA-81> ;
  - le sort des `LEPTON-PROVENANCE.md` (même conduite que le F4 ou autre) ;
  - les modifications de lepton, de la skill ou du hook, s'il en faut (attendu : aucune) :
    <À CONFIRMER au PA-81>.
- Aucune modification avant la réponse.

### 2. Miroirs
Le porteur n'existe pas encore (il est créé au §5.1) : un `mirror-sync` lancé depuis `<ROOTSTOCK>`
ne verrait aucun miroir. Méthode E13 d'ENV-40 :
1. création des dépôts vides sur GitHub, selon le PA-81 ;
2. ajout des deux lignes F7 au `.scion.mirrors` de la graine de publication
   `essais/env-40-publication/graine/scion/.scion/` ;
3. `scion mirror-sync --seed <graine> --dry-run`, puis sans `--dry-run` (PA-P).
Contrôle : `git ls-remote` du miroir = celui de l'amont ; les révisions épinglées y sont
atteignables. Les mêmes lignes sont ensuite recopiées dans le `scion/.scion/` de la famille (§5.1).

### 3. Rootstock à graine de projet
Choisir le rootstock d'essai qui servira aux contrôles des commandes de graine (`seed lock` est
refusé sur la graine de référence de `<ROOTSTOCK>`, `lepton/seed.py:823`) : copie d'un rootstock à
graine de projet qui greffe `family-stm32f7xx`, ou graine créée par `lepton seed new`.

### 4. Oracle avant
Skill `lepton-oracle` : host et les 16 presets → `rapports/oracles/env-47-avant/` ; liste triée des
chemins du trunk et son `sha256`.

### 5. Bascule
D'abord sur une copie d'essai de `<ROOTSTOCK>` (`rsync -a` sans `build/` ni `third_party/`, forme
d'ENV-41 §3.3), puis sur `<ROOTSTOCK>` (PA-P) :
1. Famille : `scion/.scion/` (sources, ramifications, projections, miroirs), commit.
2. Famille : `git rm -r` de `hal_driver/`, puis du CMSIS device, un commit mécanique chacun.
   Supprimer ensuite les répertoires restés sur le disque.
3. Famille : texte `description` du manifeste.
4. Regreffe comme en ENV-41 §3.5 : `scion seed-clone --seed depots/lepton-seed.scions/original-tree`
   (crée les clones tiers depuis les miroirs), puis `scion graft`. Pas de `graft-update` ni de
   `seed-update` : la famille est sur `devenv/env-47`, hors de sa version déclarée, et
   `graft-update` la refuserait (règle « Branche des clones » du §2bis) ou ferait avancer les autres
   clones.

### 6. Contrôles → PA-82
- Liste des chemins du trunk identique à celle du §4, aux écarts accordés près ; +201 cibles F7 sous
  `depots/tiers/`, 407 en tout (206 du F4) ; 0 lien cassé, 0 fichier régulier.
- Oracle après : code 0 sur host et les 16 presets ; `ctest -N`, fumée et KAL identiques.
- Contenu projeté = commits épinglés, octet pour octet.
- Rootstock neuf `~/lepton-tools-dev/essais/env-47-vierge`, depuis une graine d'essai locale où la
  famille est en `file://` de la branche `devenv/env-47` (forme d'ENV-41 §3.4) : même liste,
  `lepton check` code 0.
- `lepton check`, `lepton generate`, `seed status`, `file owner` sur `<ROOTSTOCK>` ; `seed lock`
  (écriture et `--verify`) sur le rootstock du §3 : clés F7 reconnues.
- Carte STM32F746G-DISCO : banc 20/20 réseau compris, si elle est disponible (PA-11).
- **PA-82** : rapport ; ordre de publication (famille après le miroir) ; push et fusions
  (PA-P). Validation Debian : ENV-50.

## Critères de validation
- [ ] PA-81 et PA-82 tranchés et consignés.
- [ ] Miroirs F7 créés, égaux à l'amont.
- [ ] Binaires identiques (code 0) ; liste des chemins identique aux écarts accordés près.
- [ ] Plus aucun fichier de la HAL ni du CMSIS device F7 dans le clone `family-stm32f7xx`.

## Pièges connus
- Les rootstocks d'essai ne sont pas regreffés ici : c'est ENV-50. Ne pas y lancer `graft-update`
  entre-temps.
- `scion mirror-sync` dans un rootstock `--bare` non greffé, sans `--seed`, répond « aucun miroir
  déclaré » (`handoff/env-43.md`) : pour la première synchronisation, passer `--seed` (§2) ;
  ensuite, partir d'un rootstock qui greffe le porteur.
- Si ENV-45 n'est pas faite, le banc STM32F746G-DISCO se passe WL55 débranchées : le BSP prend la
  première sonde trouvée (`handoff/env-31.md`).
- Le volume du Mac ne distingue pas la casse : comparer les noms à ceux de l'amont (`Inc`, `Src`).
- Le hook peut refuser une lecture qui cite `depots/tiers/` (D3, selon ENV-44) : passer par un
  script.
- Ne toucher ni au F4, ni au WL.

## À la fin de l'étape
`DEVENV-STATUS.md` :
- statut et branches ;
- décisions PA-81 et PA-82 ;
- §Emplacements : HAL F7 projetée, miroirs F7 ;
- journal.

Passation `handoff/env-47.md`, avec la liste des rootstocks à regreffer en ENV-50.
