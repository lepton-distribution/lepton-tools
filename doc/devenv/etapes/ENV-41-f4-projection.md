# Étape ENV-41 — Famille STM32F4 : copie d'ENV-34 remplacée par la projection

## Contexte
ENV-34 a copié dans `family-stm32f4xx` la HAL ST `v1.8.5` et le CMSIS device F4, avec provenance.
Décision du 2026-11-04 : cette copie sera remplacée par la projection scion. Décision du
2026-11-05 : le F4 bascule seul, en pilote ; le F7 et le WL attendent la révision suivante du plan.

La projection (ENV-39) et les deux miroirs (ENV-40) existent. Cette étape déclare la projection
dans le `scion/.scion/` de la famille, qui la porte (PA-63 Q9, P-P1 de la spécification), et retire
la copie de la famille. La graine `original-tree` ne change pas. **Rien de compilé ne change** :
les fichiers gardent le même chemin dans le trunk, seule la cible des liens change.

Archétype : migration iso-fonctionnelle. Oracle : binaires identiques.

## Prérequis
- ENV-39 et ENV-40 terminées et publiées : version de scion et URL des miroirs dans
  `DEVENV-STATUS.md` §Versions et §Emplacements.
- Spécification d'ENV-38 ; `rapports/env-38-projection.md` §2 (cas d'épreuve F4 dans le format
  final) et §4 (effets sur lepton) ; résultat de l'essai à blanc d'ENV-39 (`rapports/env-39-scion.md`).
- Copie à remplacer, dans `<ROOTSTOCK>/depots/lepton/family-stm32f4xx/master/scion/sys/root/src/` :
  - `kernel/dev/arch/cortexm/stm32f4xx/hal_driver/` : `Inc/`, `Src/`, `LICENSE.md`, `README.md`,
    `LEPTON-PROVENANCE.md` (201 fichiers) ;
  - `kernel/core/ucore/cmsis-5/Device/ST/STM32F4xx/` : `Include/stm32f4xx.h`,
    `Include/system_stm32f4xx.h`, `Include/stm32f429xx.h`, `Include/stm32f439xx.h`, `LICENSE.md`,
    `README.md`, `LEPTON-PROVENANCE.md`.
- Révisions : HAL `v1.8.5` = b6f0ed3829f3829eb358a2e7417d80bba1a42db7 ; CMSIS device
  3c77349ce04c8af401454cc51f85ea9a50e34fc1 (`v2.6.11-1`, sans tag).
- Listes de référence : `rapports/env-34-hal-f4/listes/hal.txt`, `cmsis-device-f4.txt`.
- Graine : clone `<ROOTSTOCK>/depots/lepton-seed.scions/original-tree`, `original-tree` 15740f9 ;
  non modifiée (la projection voyage avec la famille).
- Famille : `master` 0fd8b2a. Dernier oracle Mac : celui d'ENV-37 (`env-37-avant`, conforme à
  `env-35-apres`).
- Scripts `scripts/tiers/verifier-import.sh`, `scripts/tiers/compiler-hal-f4-a-blanc.sh`.
- Skills `lepton-rootstock`, `lepton-oracle`, `lepton-cibles`.
- Branches `devenv/env-41` : lepton-tools, `family-stm32f4xx`.

## Tâches

### 1. Audit (lecture seule) → PA-69
- Écrire le `scion/.scion/` de la famille (sources, ramifications, projections) de la HAL et du
  CMSIS device, d'après le cas d'épreuve F4 (`rapports/env-38-projection.md` §2.1) et l'essai à
  blanc d'ENV-39. Les URL sont celles des miroirs (M-D2). Noms de clé et shelf : à arrêter.
- Établir la liste attendue des chemins du trunk : elle doit être celle d'aujourd'hui, aux
  fichiers `LEPTON-PROVENANCE.md` près (sort tranché au PA-69).
- Recenser les rootstocks qui greffent `family-stm32f4xx` (graine `original-tree`, graines de
  projet des rootstocks d'essai du Mac et de la VM, modèle de `lepton seed new`). Leurs graines
  n'ont rien à ajouter (porteur), mais un rootstock dont le scion est antérieur à la version de la
  projection ignore le porteur et perd la HAL : relever la version de scion de chacun.
- lepton : comportement actuel de `check`, `seed status`, `seed lock`, `seed new`, `file owner`,
  `generate` devant un greffon projeté (d'après `rapports/env-38-projection.md` §4 et le PA-65).
- Rapport `rapports/env-41-f4-projection.md`, §1.
- **PA-69** : l'utilisateur valide :
  - Les lignes de projection, URL et révisions comprises.
  - Sort des deux `LEPTON-PROVENANCE.md`, des `LICENSE.md` et des `README.md` :
    <À CONFIRMER au PA-69> (renvoyé ici par le PA-63 Q14).
  - Conduite pour les rootstocks dont le scion est trop ancien : <À CONFIRMER au PA-69>.
  - `SCION_MIN_VERSION` de lepton relevé à la version de la projection (PA-63 Q13) : confirmer la
    valeur.
  - Modifications de lepton dans cette étape : <À CONFIRMER au PA-69>.
  - Sort de `verifier-import.sh` et de `compiler-hal-f4-a-blanc.sh` pour le F4 : adaptés aux
    nouveaux emplacements, ou retirés : <À CONFIRMER au PA-69>.
  - Skill `lepton-rootstock` et hook `proteger-trunk.py` : règle d'écriture dans un clone
    projeté : <À CONFIRMER au PA-69>.
- Aucune modification avant la réponse.

### 2. Oracle avant
Skill `lepton-oracle` : host et les 16 presets → `rapports/oracles/env-41-avant/`, listes
`ctest -N` comprises. Doit être conforme au dernier oracle Mac. Relever la liste triée des chemins
du trunk de `<ROOTSTOCK>` et son `sha256`.

### 3. Bascule
D'abord sur une copie d'essai de `<ROOTSTOCK>` (`cp -RP`), puis sur `<ROOTSTOCK>` (PA-P).
1. Famille : `scion/.scion/` (sources, ramifications, projections), commit.
2. Famille : `git rm -r` de `hal_driver/`, puis du CMSIS device, un commit mécanique chacun.
   Supprimer ensuite les répertoires restés sur le disque : ils gardent un `.DS_Store` ignoré par
   git, que `git rm` ne retire pas.
3. Famille : texte `description` du manifeste. `sources` et `compilation` ne changent pas : les
   chemins sont les mêmes.
4. lepton-tools : modifications accordées au PA-69, tests compris.
5. Regreffe selon la spécification.

### 4. Contrôles → PA-70
- Liste triée des chemins du trunk : identique à celle du §2, aux écarts accordés au PA-69 près.
  Aucun lien cassé, aucun fichier régulier.
- Oracle après : `comparer-oracle.py` code 0 sur host et les 16 presets ; listes `ctest -N`
  identiques ; fumée et banc KAL QEMU identiques.
- Contenu projeté identique à l'amont : contrôle par `verifier-import.sh` ou par son remplaçant,
  selon le PA-69 ; 0 écart.
- Rootstock neuf dans `~/lepton-tools-dev/essais/env-41-vierge`, depuis la graine de la branche
  `devenv/env-41` en `file://` : même liste de chemins, `lepton check` code 0.
- `lepton check` et `lepton generate` sur `<ROOTSTOCK>` : code 0 ; espace de travail identique à
  celui d'avant, régénéré juste avant la bascule (règle « régénérer avant de relever »).
- `pytest` de lepton vert.
- **PA-70** : rapport ; publication (PA-P) de la famille et de lepton-tools ; ordre de
  publication : <À CONFIRMER au PA-70>. Validation Debian : ENV-43.

## Critères de validation
- [ ] PA-69 et PA-70 tranchés et consignés.
- [ ] Binaires identiques sur host et les 16 presets (code 0).
- [ ] Liste des chemins du trunk identique, aux écarts accordés près.
- [ ] Plus aucun fichier de la HAL ni du CMSIS device F4 dans le clone `family-stm32f4xx`.
- [ ] Fichiers projetés identiques octet pour octet à `v1.8.5` et à `3c77349`.
- [ ] Rootstock neuf conforme depuis la graine de la branche.

## Pièges connus
- La famille publiée exige le scion de la projection : un rootstock qui fait `graft-update` avec un
  scion plus ancien greffe la famille sans HAL (compilation en échec, pas de conflit). Fixer
  l'ordre au PA-70 (scion et lepton d'abord) et le dire dans le message de la famille.
- Les 7 rootstocks d'essai du Mac et ceux de la VM ne sont pas regreffés ici : c'est la tâche 3
  d'ENV-43. Ne pas y lancer `graft-update` entre-temps.
- Si `.debug_line` ou `.debug_str` diffèrent, chercher un chemin réel de clone tiers à la place du
  chemin du trunk : un outil a résolu le lien.
- Le volume du Mac peut ne pas distinguer la casse : comparer les noms des chemins du trunk à ceux
  de l'amont, `Inc` et `Src` compris. La VM la distingue.
- Ne pas toucher au F7 ni au WL. Ne pas toucher à `driverlib/` (SPL conservée, hors plan).
- `core_cm4.h` n'est pas concerné : il vient de CMSIS_5, dans le noyau ; son sort est ENV-42.
- `sed -i` est interdit sur le trunk ; un fichier créé directement dans le trunk est refusé par le
  hook.

## À la fin de l'étape
`DEVENV-STATUS.md` :
- statut et branches ;
- décisions PA-69 et PA-70 ;
- §Emplacements : ligne « HAL et CMSIS device F4 » réécrite (projection, clones tiers) ;
- journal.

Passation `handoff/env-41.md` : elle liste les graines de projet à traiter en ENV-43.
