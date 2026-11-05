# Étape ENV-38 — scion : conception de la projection et du miroir

## Contexte
Un dépôt tiers (HAL ST, CMSIS device) n'est pas structuré en greffon : il n'a pas de répertoire
`scion/`. Aujourd'hui son contenu est copié dans un greffon famille, avec une provenance écrite à
la main (F7 en migration, F4 en ENV-34, WL audité en ENV-37).

Principes retenus par l'utilisateur le 2026-11-04 (`DEVENV-STATUS.md` §Décisions), qui ne se
rediscutent pas ici :
- greffon d'un dépôt tiers par une **projection déclarée dans la graine** : fichier
  `.scion.projections` en colonnes, destinations à préfixe `scion/` obligatoire, motifs récursif,
  non récursif, filtre et fichier ;
- **miroir de conservation** sous `lepton-distribution/` : avance rapide, tag déplacé signalé,
  jamais propagé, par une commande scion générique ;
- deux dépôts ST séparés (HAL et CMSIS device), pas STM32CubeF4 entier ;
- la copie d'ENV-34 sera remplacée par la projection ;
- scion reste générique (NF-2).

Restent à confirmer depuis cette date : la sémantique exacte des motifs, et la règle « motif sans
correspondance = erreur ».

Cette étape produit une **spécification écrite, validée avant toute ligne de code**. Elle est
l'entrée d'ENV-39 (projection) et d'ENV-40 (miroir). Archétype : infrastructure. Aucun code.

## Prérequis
- ENV-37 terminée : `rapports/env-37-wl-provenance.md`, section « Cas d'épreuve pour ENV-38 ».
- `<SEED_SCIONS>` : `master` 1173d6d, tag `0.5.4.0` sur 99aa973.
- Code à lire : `scion/seed.py`, `scion/model.py`, `scion/graft.py`, `scion/gitops.py`,
  `scion/rootstock.py`, `scion/cli.py`.
- Format actuel de la graine : `scion/.scion/.scion.sources.list` et
  `scion/.scion/.scion.ramifications` du clone
  `<ROOTSTOCK>/depots/lepton-seed.scions/original-tree`. L'en-tête de `.scion.sources.list` annonce
  une cinquième colonne « scion location in depot ».
- Exigences : NF-2, NF-5, GRA-3, GRA-5 de `SPECIFICATION.md`.
- Cas d'épreuve :
  - F4 : `rapports/env-34-hal-f4.md`, listes `rapports/env-34-hal-f4/listes/` (`hal.txt`,
    `cmsis-device-f4.txt`) ;
  - F7 : `cmsis-device-f7.txt` de ces listes, et les `LEPTON-PROVENANCE.md` de
    `family-stm32f7xx` ;
  - WL : rapport d'ENV-37.
- Branches `devenv/env-38` : lepton-tools, et `<SEED_SCIONS>` si le PA-63 y place le document.

## Tâches

### 1. Audit (lecture seule) → PA-63
- Code de scion :
  - lecture d'une graine : sources, ramifications, rôle réel de la colonne « scion location in
    depot » ;
  - localisation du sous-arbre `scion/` d'un clone, création des liens, détection des conflits ;
  - filtre des fichiers ignorés (ENV-15), `.scion.trunk.tolerated`, contrôle de la version
    déclarée (ENV-29), `seed-update`, `graft-update`, `seed-scion-add`, `seed-scion-remove`,
    greffe partielle (`tests/test_partial.py`).
- Clients de scion : `lepton/scion_runner.py`, `lepton check`, `seed status`, `seed lock`,
  `seed new`, `file owner`, l'extension ; hook `.claude/hooks/proteger-trunk.py` ; skill
  `lepton-rootstock`.
- Écrire chaque cas d'épreuve (F4, F7, WL) sous la forme candidate du format, pour faire
  apparaître ce que le format ne sait pas dire.
- Rapport `rapports/env-38-projection.md`, §1.
- **PA-63** : l'utilisateur tranche, point par point. Chaque point est <À CONFIRMER au PA-63> :
  - Syntaxe de `.scion.projections` : colonnes, écriture des quatre formes de motif.
  - Sémantique des motifs : renommage de répertoire (cas `Inc` → `inc` du WL), exclusion,
    recouvrement de deux motifs, casse des noms.
  - Règle « motif sans correspondance = erreur ».
  - Révision épinglée : tag, commit, ou les deux ; conduite si le tag a été déplacé.
  - Emplacement du clone du dépôt tiers dans le rootstock ; clone complet ou partiel.
  - Articulation avec `.scion.sources.list` et `.scion.ramifications` : déclaration, greffe,
    retrait, ordre de superposition, conflit avec un fichier d'un autre greffon.
  - Dépendance d'un greffon envers une projection : la projection est déclarée dans la graine,
    mais c'est la famille qui en a besoin. Conséquence pour toute graine qui référence cette
    famille (graines de projet, `lepton seed new`).
  - Fichier modifié localement dans un clone projeté : toléré, signalé ou refusé.
  - Miroir : nom de la commande (`mirror-sync` a été cité, rien n'est acté), arguments, lieu où la
    liste des miroirs est déclarée, conduite sur historique réécrit, tag déplacé, tag supprimé ;
    lien entre l'URL d'une projection et son miroir.
  - Versions de scion : une version pour la projection et une pour le miroir, ou une seule.
  - Sort de `LEPTON-PROVENANCE.md` et des fichiers de licence quand la copie disparaît.
  - Emplacement de la spécification : `<SEED_SCIONS>/doc/` (texte générique) ou lepton-tools.
- Aucune rédaction de la spécification avant la réponse.

### 2. Spécification → PA-64
- Rédiger la spécification selon le PA-63, à l'emplacement retenu :
  - format et grammaire de `.scion.projections`, avec un exemple par forme de motif ;
  - comportement de chaque commande touchée, messages et codes de retour ;
  - cas d'erreur ;
  - commande de miroir ;
  - compatibilité : un rootstock sans projection se comporte comme en 0.5.4.0.
- Dans `rapports/env-38-projection.md` (lepton-tools, propre à Lepton) :
  - §2 : les cas d'épreuve F4, F7 et WL écrits dans le format final ; pour chacun, la liste des
    chemins attendus dans le trunk ;
  - §3 : plan de tests pour ENV-39 et ENV-40, un cas nommé par règle de la spécification ;
  - §4 : effets à traiter sur lepton, l'extension, le hook et la skill `lepton-rootstock`, avec
    l'étape qui les porte (ENV-39 ou ENV-41) ;
  - §5 : ce que le format ne couvre pas (par exemple les fichiers WL modifiés par Lepton).
- **PA-64** : l'utilisateur valide la spécification ; fusions et push des branches `devenv/env-38`
  (PA-P).

## Critères de validation
- [ ] PA-63 et PA-64 tranchés et consignés.
- [ ] Chaque cas d'épreuve F4, F7, WL est écrit dans le format, ou son impossibilité est consignée
      au §5 du rapport.
- [ ] Chaque règle de la spécification a au moins un cas de test nommé au §3 du rapport.
- [ ] Aucun fichier de `scion/` ni de `tests/` modifié dans `<SEED_SCIONS>`
      (`git diff --stat master -- scion tests` vide).
- [ ] Si le document est dans `<SEED_SCIONS>` : aucune chaîne propre à Lepton
      (`grep -i lepton <document>` : 0).

## Pièges connus
- Ne rien implémenter, même un prototype : le code est l'objet d'ENV-39 et d'ENV-40.
- Les principes du 2026-11-04 ne se rediscutent pas. Si l'audit montre qu'un principe est
  intenable, c'est une question à l'utilisateur, pas une variante dans la spécification.
- Seule la bascule du F4 est planifiée (ENV-41). Le F7 et le WL servent de cas d'épreuve du
  format ; ne pas planifier leur bascule ici.
- Les noms ST, STM32 et Lepton n'entrent pas dans un document de `<SEED_SCIONS>` : employer des
  exemples neutres. Les cas réels vont dans le rapport de lepton-tools.
- Le volume du Mac peut ne pas distinguer la casse (relevé d'ENV-37) : la spécification doit dire
  ce qui se passe sur un système qui la distingue.
- `git ls-remote --tags` rend l'objet tag d'un tag annoté, pas le commit.

## À la fin de l'étape
`DEVENV-STATUS.md` :
- statut et branches ;
- décisions PA-63 et PA-64, une ligne par point tranché ;
- §Emplacements : chemin de la spécification ;
- journal.

Passation `handoff/env-38.md` : elle cite le chemin de la spécification et les sections du rapport
qu'ENV-39 et ENV-40 doivent lire.
