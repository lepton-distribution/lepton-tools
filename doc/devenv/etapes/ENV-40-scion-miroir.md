# Étape ENV-40 — scion : miroir de conservation

## Contexte
Une projection (ENV-39) fait dépendre un rootstock d'un dépôt tiers que le projet ne maîtrise pas :
il peut disparaître, être réécrit, ou voir un tag déplacé. Principe retenu le 2026-11-04 : un
**miroir de conservation** sous `lepton-distribution/`, tenu par une commande scion générique :
avance rapide seulement, tag déplacé signalé, jamais propagé. Deux dépôts ST séparés sont visés
(HAL et CMSIS device), pas STM32CubeF4 entier.

Le détail (nom de la commande, arguments, déclaration des miroirs) a été tranché au PA-63 et écrit
dans la spécification d'ENV-38. Cette étape implémente la commande, puis crée les deux miroirs du
F4, dont ENV-41 a besoin.

scion reste générique (NF-2). Archétype : infrastructure.

## Prérequis
- ENV-38 terminée. Lire la spécification (partie miroir) et `rapports/env-38-projection.md` §3 ;
  chemins dans `handoff/env-38.md`.
- ENV-39 et ENV-40 sont permutables. Partir du dernier `master` et du dernier tag de
  `<SEED_SCIONS>` : 1173d6d et `0.5.4.0` si ENV-39 n'est pas faite, sinon ceux d'ENV-39.
- Amont des deux miroirs (`DEVENV-STATUS.md` §Versions) :
  - `https://github.com/STMicroelectronics/stm32f4xx-hal-driver.git`, tag `v1.8.5` =
    b6f0ed3829f3829eb358a2e7417d80bba1a42db7 ;
  - `https://github.com/STMicroelectronics/cmsis_device_f4.git`, commit
    3c77349ce04c8af401454cc51f85ea9a50e34fc1 (`v2.6.11-1`, sans tag).
- Clones locaux : `~/lepton-tools-dev/tiers/stm32f4xx-hal-driver`,
  `~/lepton-tools-dev/tiers/cmsis_device_f4`.
- `gh` authentifié sur l'organisation `lepton-distribution` (précédent : dépôt
  `lepton-bsp-nucleo-f439zi` créé le 2026-10-31).
- Procédures de référence : `rapports/env-29-scion.md`, `rapports/env-23-scion.md`.
- Branches `devenv/env-40` dans `<SEED_SCIONS>` et lepton-tools ; clone noyau seulement si
  `SCION_REF` change.

## Tâches

### 1. Audit (lecture seule) → PA-67
- Confronter la partie miroir de la spécification au code (`scion/gitops.py`, `scion/cli.py`) :
  fonctions à créer, écarts ou ambiguïtés.
- Relever l'état des deux amonts : branches, tags, tags annotés (`git ls-remote`), taille.
- Rapport `rapports/env-40-miroir.md`, §1.
- **PA-67** : l'utilisateur valide :
  - Les écarts à la spécification : <À CONFIRMER au PA-67>.
  - Le numéro de version : <À CONFIRMER au PA-67 : version propre, ou celle d'ENV-39 si le PA-63
    a retenu une seule version>.
  - `SCION_MIN_VERSION` de lepton relevé ou non : <À CONFIRMER au PA-67>.
- Aucune modification avant la réponse.

### 2. Implémentation (`<SEED_SCIONS>`, `devenv/env-40`)
- Écrire les tests d'abord, sur des dépôts git locaux, sans accès réseau : un test par cas nommé du
  plan de tests (partie miroir). Couvrir au moins :
  - première synchronisation d'un miroir vide ;
  - avance rapide d'une branche ;
  - historique réécrit en amont : refus, miroir intact ;
  - tag déplacé en amont : signalé, non propagé, code de retour selon la spécification ;
  - tag supprimé en amont : conservé dans le miroir ;
  - nouvelle branche et nouveau tag.
- Commits séparés : un par comportement, puis un pour la version (`CHANGELOG.md`, `README.md`).

### 3. Essai local
- Créer deux miroirs nus locaux dans `~/lepton-tools-dev/essais/env-40-miroirs/` depuis les clones
  de `tiers/`. Lancer la commande ; contrôle : `git ls-remote` du miroir identique à celui de
  l'amont, branches et tags.
- Dans une copie locale d'un amont, déplacer un tag, puis relancer : le déplacement est signalé et
  le miroir garde l'ancien commit.
- Rien n'est créé sur GitHub à ce stade.

### 4. Miroirs publiés, version → PA-68
- **PA-68** : l'utilisateur valide, avant toute création :
  - Nom de chaque dépôt miroir sous `lepton-distribution/` : <À CONFIRMER au PA-68>.
  - Visibilité, publique ou privée : <À CONFIRMER au PA-68>.
  - Contenu ajouté au miroir (aucun, ou une description du dépôt seulement) :
    <À CONFIRMER au PA-68>. Un fichier ajouté ferait diverger le miroir de l'amont.
  - Périmètre : les deux dépôts du F4 seuls ; F7 et WL à la révision suivante du plan :
    <À CONFIRMER au PA-68>.
  - Qui crée les dépôts : la session par `gh`, sur accord, ou l'utilisateur :
    <À CONFIRMER au PA-68>.
  - Publication : tag et `master` de `<SEED_SCIONS>`, branches `devenv/env-40`, fusions.
- Après accord (PA-P) : création des deux dépôts, première synchronisation par la commande.
- Contrôle : `git ls-remote` de chaque miroir identique à celui de son amont ; le commit `b6f0ed3…`
  et le commit `3c77349…` sont atteignables dans leur miroir.
- Version : tag annoté, `pipx install --force "git+file://<SEED_SCIONS>@<version>"`, références de
  version de lepton-tools et du clone noyau si le PA-67 l'a décidé ; `pytest` de lepton vert ;
  `lepton check` code 0 ; liste des liens de `<ROOTSTOCK>` inchangée.
- Rapport §4 ; validation Debian reportée à ENV-43.

## Critères de validation
- [ ] PA-67 et PA-68 tranchés et consignés.
- [ ] Tests de scion verts, dont un par cas nommé ; aucune chaîne propre à Lepton dans
      `seed.scions` (`grep -ri lepton scion/` : 0).
- [ ] Essai local : tag déplacé signalé, miroir inchangé.
- [ ] Les deux miroirs publiés ont les mêmes références que leur amont (`git ls-remote`), et les
      deux commits épinglés y sont atteignables.
- [ ] Toutes les références de version désignent la même version.

## Pièges connus
- Créer un dépôt sur GitHub et y pousser est une action publique, soumise à PA-P : rien avant le
  PA-68.
- Jamais de `push --force` vers un miroir : la conservation est sa raison d'être.
- `3c77349` n'a pas de tag : le contrôle porte sur le commit, atteignable depuis une branche.
- Le nom de l'organisation, des dépôts ST et de Lepton n'entre pas dans `seed.scions` : la liste des
  miroirs est une donnée, déclarée où la spécification le dit.
- Ne pas mettre STM32CubeF4 en miroir (décision du 2026-11-04).
- `scion` installé par pipx change l'outil de tous les rootstocks. Point de retour : la version
  précédente, `pipx install --force "git+file://<SEED_SCIONS>@<version précédente>"`.
- Push GitHub : deux refus « fatal error in commit_refs_rules » ont été passagers le 2026-11-05
  (R36-1). Réessayer une fois avant de conclure à un défaut.

## À la fin de l'étape
`DEVENV-STATUS.md` :
- statut et branches ;
- décisions PA-67 et PA-68 ;
- §Emplacements : URL des deux miroirs ;
- §Versions : scion ;
- journal.

Passation `handoff/env-40.md`.
