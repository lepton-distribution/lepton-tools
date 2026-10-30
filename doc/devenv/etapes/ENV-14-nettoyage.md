# Étape ENV-14 — Nettoyage de l'arbre

## Contexte
Après ENV-5, ENV-6 et ENV-13, l'arbre Lepton assemblé par la graine publiée `original-tree`
contient encore des fichiers et répertoires qui ne servent plus. Exemples cités par l'utilisateur :
`trunk/sys/user/build`, `trunk/sys/user/tauon_sampleapp`, `trunk/tools/bin`, `trunk/tools/config`,
`trunk/tools/host`. Cette étape les inventorie dans tout l'arbre, puis retire ceux dont la liste est
validée. Nettoyage iso-fonctionnel : aucun binaire, aucune image mklepton, aucun comportement ne
change ; l'oracle fait foi. L'historique git conserve tout ce qui est retiré.

## Prérequis
- ENV-13 terminée. scion 0.5.1.1, lepton 0.1.0 (`DEVENV-STATUS.md` §Versions).
- Graine `original-tree` 0f1275a publiée ; clone noyau `<ROOTSTOCK>/depots/lepton/original/master`
  sur `master` 16a331b = `origin/master` ; 7 greffons famille/BSP sous `depots/lepton/<clé>/master`.
- Décisions de l'utilisateur du 2026-10-30 (`DEVENV-STATUS.md` §Décisions) :
  - périmètre : audit de tout l'arbre, les 5 répertoires cités compris ;
  - **hors périmètre, conservés tels quels** : le code des architectures gelées (ARM7, ARM9, M16C,
    simulations) et les BSP qui ne font pas partie des presets actuels ;
  - validation : oracle Mac, puis validation Debian par ordre à la VM, puis push (PA-P) ;
  - `.DS_Store` du Finder retirés du trunk et des clones.
- Branches `devenv/env-14` : lepton-tools (depuis `main`), clone noyau (depuis `master` 16a331b) ;
  autre greffon seulement si la liste du PA-15 en touche un.

## Tâches

### 1. Audit (lecture seule) → PA-15
- Pour chaque entrée de premier et second niveau du trunk (`sys/user/*`, `tools/*`, `sys/root/*`,
  racine), puis plus bas dans tout répertoire suspect : greffon propriétaire (`lepton file owner`
  ou `realpath`), fichiers versionnés ou non (`git -C <clone> ls-files`).
- Usage par la construction : fichiers réellement lus par les 15 constructions (host + 14 presets
  de `oracles/env-13-apres/`). Réutiliser l'outillage existant (`build_closure.py` s'il existe dans
  le clone noyau, voir `rapports/env-2-outillage.md`), sinon les dépendances de ninja
  (`ninja -C <build> -t deps`, `-t inputs`). Ne pas écrire un second mécanisme.
- Références textuelles, pour tout candidat non lu par la construction : `grep -rn` du chemin
  dans le clone noyau (CMake, `CMakePresets.json`, XML mklepton, `scripts/`, `tests/`, `ci/`,
  `doc/`), dans les 7 greffons et dans lepton-tools (`lepton/`, `extension/`, `scripts/`,
  `schemas/`, `doc/`).
- Classer chaque candidat : **supprimer** (aucun usage, aucune référence vivante), **conserver**
  (motif), **à arbitrer** (référencé seulement par du code gelé, par une documentation, ou doute).
  Un candidat qui relève du code gelé ou d'un BSP hors presets est classé « conserver, hors
  périmètre ».
- Relever les `.DS_Store` : fichiers réguliers du trunk, fichiers ignorés des clones (`git status
  --ignored`), et la présence de `.DS_Store` dans le `.gitignore` de chaque clone.
- Rapport `doc/devenv/rapports/env-14-inventaire.md` : une table par répertoire (chemin trunk,
  greffon, versionné, lu par la construction, références, classement, motif) ; lots de
  suppression proposés.
- **PA-15** : présenter l'inventaire. L'utilisateur valide la liste à supprimer, tranche chaque
  « à arbitrer », et indique si les documents qui citent un chemin retiré sont corrigés
  (`<À CONFIRMER au PA-15 : documents vivants seulement, rapports historiques jamais réécrits>`).
  Aucune suppression avant sa réponse.

### 2. Oracle avant
Skill `lepton-oracle`, mêmes commandes qu'en ENV-13 :
`scripts/oracle/rejouer-oracle.sh <ROOTSTOCK> doc/devenv/rapports/oracles/env-14-avant --qemu …×6
--carte …×8` (liste des presets : `rapports/env-13-graine.md` §4). Aucune modification avant la fin
de la capture.

### 3. `.DS_Store`
- Clones : supprimer les `.DS_Store` ignorés (`find <clone> -name .DS_Store -not -path '*/.git/*'
  -delete`) ; ajouter `.DS_Store` au `.gitignore` du clone qui ne l'ignore pas (commit dédié).
- Trunk : les 24 fichiers réguliers sont retirés **par l'utilisateur**. Le hook
  `proteger-trunk.py` refuse toute écriture sous `trunk/` : ne pas le contourner. Commande à lui
  proposer : `find <ROOTSTOCK>/trunk -name .DS_Store -type f -delete`.
- Puis `scion graft --scion lepton@original::tree` (et chaque clé touchée) **sans `--force`** :
  les liens vers les `.DS_Store` supprimés disparaissent.

### 4. Suppressions
Dans le clone noyau, sur `devenv/env-14`, un lot du PA-15 par commit mécanique :
`git -C <clone> rm -r <chemins scion/…>`. Après chaque lot : `scion graft --scion
lepton@original::tree`, puis les contrôles de la skill `lepton-rootstock` (0 fichier régulier, 0
lien cassé). Une construction qui échoue après un lot : s'arrêter, rétablir le lot (`git revert`),
le reclasser « conserver » et le signaler.

### 5. Contrôles et oracle après
- Oracle après (`env-14-apres/`), mêmes commandes ; `comparer-oracle.py` sur les 14 presets ;
  empreintes mklepton de host **identiques**, banc KAL et fumée identiques.
- `lepton check` sur `<ROOTSTOCK>` : seul avertissement admis, « manifeste de graine absent ».
- Aucune référence restante aux chemins retirés : rejouer les `grep` de la tâche 1.
- Rapport `doc/devenv/rapports/env-14-nettoyage.md` : lots, volumes retirés (fichiers, octets),
  table de la skill oracle, écarts.

### 6. Validation Debian et publication → PA-16
- **PA-16**, première question : présenter le rapport ; push de `devenv/env-14` du noyau pour la
  validation Debian (PA-P).
- Ordre `R14-1` à la session VM (protocole §2bis), consigne `consignes/env-14-debian.md` reprise
  de `consignes/env-13-debian.md` : rootstock neuf depuis la graine publiée, clone noyau basculé
  sur `devenv/env-14` puis `scion graft --scion lepton@original::tree`, reconstruction des 15
  presets, critères C1 à C6. Référence Debian : `rapports/env-13-debian.md`.
- **PA-16**, seconde question, après `FIN-SUCCÈS R14-1` : fusion de `devenv/env-14` dans `master`
  du noyau et push (PA-P). La graine `original-tree` suit `master` : le nettoyage atteint alors
  tout rootstock au prochain `graft-update`.

## Critères de validation
- [ ] PA-15 et PA-16 tranchés et consignés.
- [ ] Inventaire `rapports/env-14-inventaire.md` complet : chaque entrée classée, avec son motif.
- [ ] Tous les chemins validés au PA-15 sont absents du clone et du trunk ; aucun autre fichier versionné retiré.
- [ ] Code gelé et BSP hors presets intacts (`git diff --stat master..devenv/env-14` limité aux lots).
- [ ] Trunk : 0 fichier régulier, 0 lien cassé, 0 `.DS_Store` ; regreffe sans `--force`.
- [ ] `comparer-oracle.py` code 0 sur les 14 presets ; empreintes mklepton identiques ; fumée et
      banc KAL identiques sur les 6 presets QEMU.
- [ ] `FIN-SUCCÈS R14-1` (Debian) ; `master` du noyau poussé si accordé.

## Pièges connus
- Un fichier non compilé peut être lu ailleurs : image UFS de mklepton (`sys/user/*/etc`),
  scripts, `lepton generate`, extension. Empreintes mklepton changées → un fichier retiré était
  utilisé : rétablir le lot.
- Une référence venant seulement d'un XML ou d'un CMake de code gelé maintient le candidat :
  « conserver, hors périmètre », pas « supprimer ».
- `scion graft` greffe aussi les fichiers ignorés par git (`.DS_Store` d'un clone : conflit avec un
  autre greffon, constaté en ENV-13). Le Finder en recrée dès qu'un dossier du trunk est ouvert :
  ne pas parcourir le trunk dans le Finder pendant l'étape.
- `rapports/` et `handoff/` sont l'historique : un chemin retiré qui y est cité reste tel quel.
- `lepton check` signale « manifeste de graine absent » sur `<ROOTSTOCK>` (constat d'ENV-12) :
  sans rapport avec l'étape.
- Les rootstocks d'essai (`essais/env-9`, `env-11/*`, `env-13-vierge`) ne sont pas mis à jour par
  cette étape : leurs clones noyau ne bougent qu'à un `graft-update` (PA-P).

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, branches, décisions PA-15 et PA-16, journal (ordre R14-1 compris),
volumes retirés. Passation `handoff/env-14.md`.
