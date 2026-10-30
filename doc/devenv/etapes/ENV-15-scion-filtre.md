# Étape ENV-15 — Fichiers ignorés et fichiers étrangers dans scion

## Contexte
scion 0.5.1.1 greffe tout le contenu de `scion/` d'un clone, sauf `.scion/` (`_walk`,
`scion/graft.py`), y compris les fichiers ignorés par git. Les `.DS_Store` du Finder ignorés de
deux clones au même chemin ont ainsi provoqué un conflit de greffe en ENV-13, puis l'échec du
`graft-update` de `essais/env-11/qemu`, avec un trunk laissé vide (2026-10-30). Par ailleurs,
`_check_stray` refuse le dégreffage dès qu'un fichier régulier se trouve dans le trunk, ce qui
arrive avec les `.DS_Store` que le Finder y crée : il faut alors une suppression manuelle ou
`--force`. Cette étape corrige les deux points dans scion, de façon générique (NF-2). Besoin
relevé dès PA-9 Q8 (`DEVENV-STATUS.md` §Décisions, 2026-10-14). Archétype : infrastructure ; le
greffage d'un clone propre ne doit pas changer.

## Prérequis
- ENV-14 terminée. scion 0.5.1.1 (`master` f1d1f3c de `<SEED_SCIONS>`, tag poussé), lepton 0.1.0
  (`SCION_MIN_VERSION = (0, 5, 1, 1)` dans `lepton/__init__.py`, `SCION_REF="0.5.1.1"` dans
  `scripts/install-vscodium.sh`).
- Décisions de l'utilisateur du 2026-10-30 (`DEVENV-STATUS.md` §Décisions) :
  - filtre : **exclure du greffage les fichiers ignorés par git** (règles de `git check-ignore`,
    exclusions globales comprises). Un fichier nouveau, non suivi et non ignoré, reste greffé
    (règle « créer dans le clone, puis `scion graft` » avant le commit) ;
  - fichiers réguliers du trunk : traités dans cette étape ; le mécanisme est à faire valider au
    PA-17 ;
  - validation Debian par l'ordre `R15-1`.
- Branches `devenv/env-15` : `<SEED_SCIONS>` (depuis `master` f1d1f3c), lepton-tools (depuis
  `main`).

## Tâches

### 1. Audit (lecture seule) → PA-17
- Lire `scion/graft.py` (`_walk`, `graft`, `graft_scions`, `ungraft`, `_check_stray`, `sync`),
  `scion/gitops.py` et les tests (`tests/test_graft.py`, `tests/test_partial.py`).
- Recenser les sources de scion qui ne sont pas des dépôts git (exemple : `building` →
  `depots/generation/building`) : comportement attendu pour elles.
- Proposer au **PA-17**, par évolution :
  - **E1, filtre** : point d'application (`_walk` ou appelant) ; un seul appel
    `git check-ignore --stdin -z` (ou équivalent) par clone ; comportement pour une source non git
    (<À CONFIRMER au PA-17 : aucun filtre, comportement inchangé>) ; journal `-v` des fichiers
    exclus ; effet sur les liens déjà présents dans le trunk vers un fichier devenu ignoré.
  - **E2, fichiers étrangers du trunk** : mécanisme générique, sans nom propre à macOS ni à
    Lepton dans le code. Options à présenter : motifs tolérés par le rootstock (fichier de
    configuration, emplacement et format <À CONFIRMER au PA-17>), ou fichiers tolérés s'ils sont
    ignorés par les règles git globales de l'utilisateur. Un fichier toléré est-il laissé en place
    ou supprimé au dégreffage <À CONFIRMER au PA-17> ?
  - code de retour, messages, tests, mise à jour de `README.md` et de `CHANGELOG.md` ;
  - numéro de version <À CONFIRMER au PA-17 : 0.5.1.2 ou 0.5.2.0>.
- Aucune modification avant la réponse.

### 2. Implémentation
- `devenv/env-15` de `<SEED_SCIONS>`. Structure de la 0.5 : `pathlib`, `subprocess.run` avec
  liste d'arguments, aucun `shell=True`, `ScionError` pour les refus.
- Un commit par évolution (E1, E2), avec ses tests ; tests existants inchangés.
- `python3 -m unittest discover -s tests` vert ; `grep -ri lepton scion/` vide.

### 3. Essai sur une copie du rootstock
Skill `lepton-rootstock` : `cp -RP ~/lepton <essais>/env-15` (sans `build/`), nouvelle version de
scion depuis la branche (venv d'essai ou `pipx install --force` depuis le chemin local, <À
CONFIRMER au PA-17>).
- Relever avant : liste triée (lien, cible) du trunk de la copie.
- Regreffe complète : liste identique, octet pour octet.
- Placer un `.DS_Store` ignoré au même chemin sous `scion/` du clone noyau et d'un BSP : greffe
  sans conflit, aucun lien vers eux.
- Fichier nouveau non suivi dans un clone : greffé.
- `.DS_Store` régulier dans le trunk : comportement E2 validé au PA-17, sans `--force`.
- `graft-update` n'est pas utilisé (PA-P) : rejouer `ungraft` puis `graft` à la place.

### 4. Version, `lepton`, rapport → PA-18
- Fusion de `devenv/env-15` dans `master` de `<SEED_SCIONS>`, tag annoté de la version, installation
  `pipx install --force "git+file://<SEED_SCIONS>@<version>"`, `scion version`.
- lepton-tools `devenv/env-15` : `SCION_MIN_VERSION` (`lepton/__init__.py`) et `SCION_REF`
  (`scripts/install-vscodium.sh`) à la nouvelle version ; tests de lepton (`pytest`, venv
  `~/lepton-tools-dev/venv-lepton-tools`) ; réinstallation pipx de lepton.
- Regreffe de `<ROOTSTOCK>` : liste (lien, cible) identique à celle d'avant ; 0 fichier régulier,
  0 lien cassé.
- Rapport `doc/devenv/rapports/env-15-scion.md` : évolutions, tests, essais, versions.
- **PA-18**, première question : push du tag et de `master` de `<SEED_SCIONS>`, push de
  `devenv/env-15` de lepton-tools (PA-P), puis ordre `R15-1`.

### 5. Validation Debian → PA-18
- Consigne `consignes/env-15-debian.md`, reprise de `consignes/env-14-debian.md` : installation de
  scion depuis le tag publié, rootstock neuf depuis la graine `original-tree`, greffe (3929 liens),
  `.DS_Store` ignoré placé dans deux clones, regreffe sans conflit, `rejouer-oracle.sh` sur host et
  un preset QEMU au moins (<À CONFIRMER au PA-18 : 15 presets ou sous-ensemble>).
- Ordre `R15-1` (ORCHESTRATION §2bis).
- **PA-18**, seconde question, après `FIN-SUCCÈS R15-1` : fusion de `devenv/env-15` de
  lepton-tools dans `main` et push.

## Critères de validation
- [ ] PA-17 et PA-18 tranchés et consignés.
- [ ] Tests de scion verts ; `grep -ri lepton scion/` vide ; tests de lepton verts.
- [ ] Copie et `<ROOTSTOCK>` : liste (lien, cible) du trunk identique avant et après la nouvelle version.
- [ ] Fichier ignoré au même chemin dans deux clones : greffe sans conflit, non greffé.
- [ ] Fichier nouveau non suivi : greffé.
- [ ] `.DS_Store` régulier dans le trunk : comportement validé au PA-17, sans `--force`.
- [ ] Nouvelle version taguée, installée, relevée par `scion version` ; `SCION_MIN_VERSION` et `SCION_REF` alignés.
- [ ] `FIN-SUCCÈS R15-1`.

## Pièges connus
- `git check-ignore` lit `core.excludesfile` : sur un poste sans `~/.gitignore_global`, les
  `.DS_Store` ne sont pas ignorés (aucun `.gitignore` des greffons ne les cite, PA-15). La VM
  Debian n'a pas de Finder : l'essai y place le fichier à la main et ajoute la règle d'exclusion
  dans la consigne.
- Un fichier suivi par git puis ajouté à `.gitignore` reste suivi : `check-ignore` sans
  `--no-index` ne l'exclut pas. Ne pas changer ce comportement sans décision.
- Un `graft-update` qui échoue après le dégreffage laisse le trunk vide (constat du 2026-10-30) :
  l'essai se fait sur une copie, jamais sur `<ROOTSTOCK>` en premier.
- Le hook `proteger-trunk.py` refuse aussi un `cp` qui lit le trunk : relever les listes par
  redirection (`find … -exec readlink`, `< fichier`).
- Tag, push et `graft-update` : PA-P.
- Rootstocks d'essai (`essais/env-9`, `env-11/*`, `env-13-vierge`) : non touchés par l'étape.

## À la fin de l'étape
`DEVENV-STATUS.md` : version de scion (§Versions), `SCION_MIN_VERSION`, statut, décisions PA-17 et
PA-18, journal (ordre R15-1 compris). Passation `handoff/env-15.md`.
