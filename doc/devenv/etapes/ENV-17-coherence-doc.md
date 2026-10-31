# Étape ENV-17 — Cohérence de la documentation et des messages

## Contexte
Des documents vivants et un message de construction ne correspondent plus à l'arbre. Exemples
relevés le 2026-10-31 : `doc/BUILDING.md` du clone noyau cite les presets `nucleo-f439zi-embos`
(l. 13, 144-163), renommés `nucleo-f429zi-*` en ENV-6 (PA-7 Q7) ; `scion/cmake/components/kernel.cmake:167`
affiche « bsp : aucune source pour la carte ${LEPTON_BOARD} » pour tout BSP décrit par manifeste
(signalé en ENV-6) ; la note L6-10 du bilan ENV-12 (flash prouvé par `verify_image`) n'est pas
dans la skill `lepton-cibles`. Cette étape corrige les documents vivants et les messages, sans
changer aucun binaire ni aucune image mklepton. Archétype : migration (iso-fonctionnel, oracle).

## Prérequis
- ENV-16 terminée. scion 0.5.2.0, lepton 0.1.0 (`DEVENV-STATUS.md` §Versions).
- Clone noyau `<ROOTSTOCK>/depots/lepton/original/master` sur `master` 6f1801d = `origin/master`.
- Décision PA-15 (2026-10-30) : rapports, passations et `doc/migration/` du noyau ne sont jamais
  réécrits.
- Branches `devenv/env-17` : lepton-tools (depuis `main`), clone noyau (depuis `master`).

## Tâches

### 1. Audit (lecture seule) → PA-21
- Documents vivants à relire : clone noyau (`doc/BUILDING.md`, `README*`, `README-PAQUET.md`,
  `scripts/`, `debug/`, commentaires de `CMakePresets.json`) ; lepton-tools (`README.md`,
  `doc/devenv/SPECIFICATION.md`, `.claude/skills/*/SKILL.md`, `extension/README*`) ; manifestes
  des 7 greffons famille/BSP (`description`).
- Pour chacun : noms de presets, chemins, versions, commandes cités. Confronter à
  `CMakePresets.json` du noyau, au trunk (`test -e`) et à `DEVENV-STATUS.md` §Versions.
- Messages de construction : `grep -rn 'message(STATUS' scion/cmake` du clone noyau ; relever ceux
  qu'un BSP par manifeste, une famille ou un preset actuel rend faux.
- Propositions jamais confirmées formellement, à soumettre pour clôture : ENV-8 S2-1 à S4-4
  (`rapports/env-8-interface.md` §8-§10), OBJECT `bsp_demarrage` d'ENV-6, protocole §2bis
  d'ORCHESTRATION (`DEVENV-STATUS.md` §Décisions, lignes « à confirmer »).
- Rapport `doc/devenv/rapports/env-17-coherence.md` : une table (fichier, ligne, texte actuel,
  correction proposée, motif).
- **PA-21** : l'utilisateur valide la liste des corrections, le nouveau texte des messages, et
  confirme ou amende chaque proposition en attente. Aucune modification avant sa réponse.

### 2. Oracle avant
Skill `lepton-oracle` : `scripts/oracle/rejouer-oracle.sh <ROOTSTOCK>
doc/devenv/rapports/oracles/env-17-avant` avec les arguments d'ENV-14 (`rapports/env-14-nettoyage.md`).
Seul le CMake du noyau l'exige ; aucune modification du noyau avant la fin de la capture.

### 3. Corrections
- Un commit par dépôt et par nature (documentation, message CMake, skill).
- Message `kernel.cmake:167` : ne l'afficher que si aucun BSP par manifeste n'est choisi, ou le
  reformuler (texte validé au PA-21).
- Skill `lepton-cibles` : ajouter L6-10 (preuve du flash par `verify_image`), commit dédié et ligne
  de journal (ORCHESTRATION §5bis).
- Après le commit du noyau : `scion graft --scion lepton@original::tree`, contrôles de la skill
  `lepton-rootstock`.

### 4. Contrôles → PA-22
- Oracle après (`env-17-apres/`) ; `comparer-oracle.py` code 0 sur les 14 presets ; empreintes
  mklepton identiques ; fumée et banc KAL identiques.
- Journal de configuration d'un preset à BSP par manifeste (`nucleo-f429zi-embos`) : message
  faux absent.
- `grep` de la tâche 1 rejoué : aucune occurrence restante des textes corrigés.
- **PA-22** : présenter le rapport ; push de `devenv/env-17` (lepton-tools, clone noyau), fusion
  dans `main` et `master`, push (PA-P).

## Critères de validation
- [ ] PA-21 et PA-22 tranchés et consignés.
- [ ] Toutes les corrections validées appliquées ; aucun rapport, passation ou `doc/migration/` modifié.
- [ ] `comparer-oracle.py` code 0 sur 14 presets ; empreintes mklepton identiques.
- [ ] Propositions en attente : chacune confirmée ou amendée dans `DEVENV-STATUS.md` §Décisions.

## Pièges connus
- `BUILDING.md` présente la NUCLEO-F439ZI comme carte nominale : ENV-20 ajoutera un BSP
  `nucleo-f439zi`. Décrire ici l'état actuel (`nucleo-f429zi-*`) ; ENV-20 mettra la table à jour.
- Un message CMake modifié change le journal de configuration, pas les binaires : un écart
  d'empreinte signale une autre modification.
- Le hook `proteger-trunk.py` refuse toute écriture sous `trunk/` : corriger dans les clones.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, branches, décisions PA-21 et PA-22, journal. Passation
`handoff/env-17.md`.
