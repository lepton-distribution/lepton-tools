# Étape ENV-39 — scion : projection d'un dépôt tiers

## Contexte
ENV-38 a produit la spécification de la projection : un dépôt tiers sans répertoire `scion/`
devient un greffon par des lignes de `.scion.projections` déclarées dans la graine (principes du
2026-11-04, détails tranchés au PA-63, spécification validée au PA-64).

Cette étape implémente la projection dans scion, sans rien basculer dans Lepton : la bascule de la
famille STM32F4 est l'objet d'ENV-41. Le miroir de conservation est l'objet d'ENV-40.

scion reste générique (NF-2) : aucune chaîne propre à Lepton dans `seed.scions`. Archétype :
infrastructure. La procédure de version est celle d'ENV-15, d'ENV-23 et d'ENV-29.

## Prérequis
- ENV-38 terminée. Lire la spécification et `rapports/env-38-projection.md` §2 à §4 ; leurs
  chemins sont dans `handoff/env-38.md`.
- `<SEED_SCIONS>` : `master` 1173d6d, tag `0.5.4.0` sur 99aa973 ; 159 fonctions de test relevées
  le 2026-11-05 (`grep -c 'def test_' tests/*.py`), à confirmer par `pytest`. Si ENV-40 a été
  faite avant, partir de son `master` et de son tag.
- Procédures de référence : `rapports/env-29-scion.md`, `rapports/env-23-scion.md`,
  `rapports/env-15-scion.md` §4-§9.
- Clones amont pour les essais : `~/lepton-tools-dev/tiers/stm32f4xx-hal-driver` et
  `~/lepton-tools-dev/tiers/cmsis_device_f4` (ENV-34).
- Skills `lepton-rootstock` et `lepton-oracle`.
- Branches `devenv/env-39` dans `<SEED_SCIONS>` et lepton-tools. Dans le clone noyau, seulement si
  `SCION_REF` change (§4).

## Tâches

### 1. Audit (lecture seule) → PA-65
- Confronter la spécification au code : modules touchés, fonctions à créer, tests existants
  concernés. Relever tout point de la spécification impossible ou ambigu à l'implémentation.
- Rapport `rapports/env-39-scion.md`, §1.
- **PA-65** : l'utilisateur valide :
  - Les écarts à la spécification relevés par l'audit : <À CONFIRMER au PA-65>. Un écart accepté
    est reporté dans la spécification, par un commit séparé.
  - Le numéro de version : <À CONFIRMER au PA-65 : `0.5.5.0` ou `0.6.0.0`>.
  - `SCION_MIN_VERSION` de lepton : relevé dans cette étape ou en ENV-41 :
    <À CONFIRMER au PA-65>.
  - Effets sur lepton listés au §4 du rapport d'ENV-38 : lesquels sont traités ici, lesquels en
    ENV-41 : <À CONFIRMER au PA-65>.
- Aucune modification avant la réponse.

### 2. Implémentation (`<SEED_SCIONS>`, `devenv/env-39`)
- Écrire les tests d'abord : un test par cas nommé du plan de tests (`rapports/env-38-projection.md`
  §3, partie projection). Les tests existants restent verts.
- Fixtures : dépôts git locaux créés par les tests (`tests/make_fixture.py`, `tests/support.py`).
  Aucun accès réseau hors de `tests/test_network.py`.
- Couvrir au moins : chaque forme de motif, le motif sans correspondance, le conflit avec un
  fichier d'un autre greffon, la révision introuvable, le rootstock sans projection.
- Commits séparés : un par comportement, puis un pour la version (`CHANGELOG.md`, `README.md`).

### 3. Essai sur une copie (skill `lepton-rootstock`)
- Créer une copie d'essai de `<ROOTSTOCK>` (`cp -RP`), puis installer scion par
  `pipx install --force "git+file://<SEED_SCIONS>@devenv/env-39"`.
- Non-régression, sans projection : `scion graft` de la copie donne une liste de liens identique à
  celle de `<ROOTSTOCK>` (`sha256` de la liste triée).
- Essai à blanc de la projection, dans la copie seulement, rien n'est publié :
  - écrire dans la graine de la copie les lignes du cas d'épreuve F4 (`rapports/env-38-projection.md`
    §2), avec les clones de `~/lepton-tools-dev/tiers/` en `file://` ;
  - retirer la copie de la HAL et du CMSIS device du clone famille de la copie ;
  - regreffer ; comparer la liste des **chemins** du trunk à celle d'avant : identique, seules les
    cibles des liens changent.
- Consigner l'écart éventuel : il est l'entrée d'ENV-41.

### 4. Version, lepton, `<ROOTSTOCK>` → PA-66
- Préparer le tag annoté de la version, puis
  `pipx install --force "git+file://<SEED_SCIONS>@<version>"`.
- lepton-tools, selon le PA-65 : `SCION_MIN_VERSION` (`lepton/__init__.py`), `SCION_REF`
  d'`scripts/install-vscodium.sh`, `README.md`, tests.
- Clone noyau, si la version change le défaut : `SCION_REF` d'`install-{macos,debian}.sh`,
  `doc/BUILDING.md` et `README-PAQUET.md`.
- Regreffer `<ROOTSTOCK>` (PA-P) : liste inchangée, 0 fichier régulier, 0 lien cassé.
- `pytest` de lepton vert ; `lepton check` code 0.
- **PA-66** : rapport ; publication (PA-P) : tag et `master` de `<SEED_SCIONS>`, branches
  `devenv/env-39`, fusions. La validation Debian est reportée à ENV-43.

## Critères de validation
- [ ] PA-65 et PA-66 tranchés et consignés.
- [ ] Tests de scion verts, dont un par cas nommé du plan de tests ; aucune chaîne propre à Lepton
      dans `seed.scions` (`grep -ri lepton scion/` : 0).
- [ ] Rootstock sans projection : liste des liens identique avant et après (`sha256`).
- [ ] Essai à blanc F4 sur la copie : liste des chemins du trunk identique, ou écart consigné.
- [ ] Toutes les références de version (lepton, `install-vscodium.sh`, scripts du noyau,
      documentation) désignent la même version.

## Pièges connus
- `scion` installé par pipx avant le PA-66 change l'outil de **tous** les rootstocks. Point de
  retour : `pipx install --force "git+file://<SEED_SCIONS>@0.5.4.0"`.
- Toute regreffe de `<ROOTSTOCK>` et tout `graft-update` sont soumis à PA-P : attendre l'accord.
- L'essai à blanc ne touche que la copie. Ne modifier ni la graine `original-tree` ni le clone
  `family-stm32f4xx` de `<ROOTSTOCK>` : c'est l'objet d'ENV-41.
- Les noms ST, STM32 et Lepton n'entrent ni dans le code, ni dans les tests, ni dans la
  documentation de `seed.scions`.
- La copie d'essai a ses propres clones : la resynchroniser avant chaque essai (`rsync -a
  --delete` des clones touchés, puis `scion graft` ; piège relevé dans `handoff/env-35.md`).
- Un tag de dépôt tiers peut être annoté : résoudre en commit avant de comparer.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, branches, §Versions (scion), décisions PA-65 et PA-66, journal.
Passation `handoff/env-39.md`.
