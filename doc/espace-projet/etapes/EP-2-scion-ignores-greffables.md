# Étape EP-2 — scion : fichiers ignorés greffables déclarés par le greffon

## Contexte
C5, solution (a) : les fichiers de poste d'un projet vivent dans le greffon projet, ignorés par
git, et doivent paraître dans le trunk. Or, depuis le filtre E1 (ENV-15, PA-17, scion 0.5.2.0),
un fichier **ignoré par git** dans un clone n'est pas greffé (`git ls-files --others --ignored
--exclude-standard --directory`) ; un fichier non suivi mais non ignoré est greffé.

L'étape ajoute à scion une évolution **générique** (NF-2) : un greffon déclare des motifs de
fichiers ignorés par git que scion greffe quand même. Sans déclaration, rien ne change : aucun
lien d'aucun rootstock existant ne bouge. Les solutions (b) fichiers tolérés du trunk et (c)
fichier à la racine du rootstock sont écartées par C5 : ne pas les réintroduire.

Archétype : infrastructure, iso-fonctionnel en l'absence de déclaration. Forme : celle
d'ENV-70 (`doc/devenv/etapes/ENV-70-scion-cause-git-version-graine.md`).

## Prérequis
- Indépendante d'EP-1. Conseillée après le PA-E1 d'EP-0 : si C2 est révisée, relire C5 avec
  l'utilisateur avant de commencer.
- `<SEED_SCIONS>` `master` 929c01a, tag `0.6.3.4` ; compte des tests de scion à relever.
- `SCION_MIN_VERSION` = (0, 6, 2, 0) (`lepton/__init__.py`) ; `SCION_REF` = `0.6.3.4`
  (`scripts/install-vscodium.sh`, et `scripts/install-{macos,debian}.sh` du clone noyau).
- Références : `doc/devenv/rapports/env-15-scion.md` (filtre E1, raison du PA-17),
  `doc/devenv/rapports/env-22-residus.md` (`.scion.trunk.tolerated`),
  `doc/devenv/rapports/env-65-scion.md` §7 et §8 (procédure de version), outils
  `doc/devenv/rapports/env-65-scion/fixture.py` et `scripts/comparer-releves.py`.
- Skill `lepton-rootstock`. Branches `espace-projet/ep-2` : `<SEED_SCIONS>`, lepton-tools, clone
  noyau si `SCION_REF` change.

## Tâches

### 1. Audit et conception (lecture seule) → PA-E4
Rapport `doc/espace-projet/rapports/ep-2-scion.md`. Fixtures sous
`~/lepton-tools-dev/essais/ep-2-fixture/avant/`.

Relever :
- où le filtre E1 est appliqué, et la raison retenue au PA-17 pour écarter les fichiers ignorés ;
- les fichiers de déclaration qu'un greffon porte déjà (`scion/.scion/` : `.scion.sources.list`,
  `.scion.ramifications`, `.scion.projections`, `.scion.mirrors`) et leur lecture ;
- les effets de `--directory` (répertoire ignoré rendu en une ligne), des clés projetées, des
  clones en extraction partielle, de `graft-remove --purge`, du contrôle de conformité du trunk ;
- le comportement actuel pour un fichier ignoré créé après la greffe, puis regreffé ;
- les références de version (liste d'ENV-70 : `scion/__init__.py`, `tests/test_cli.py`,
  `CHANGELOG.md`, `README.md` ; lepton-tools ; clone noyau).

Proposer, sans rien modifier :
- nom et emplacement de la déclaration dans le greffon, syntaxe des motifs (chemins exacts ou
  motifs), portée (le greffon seul) ;
- cas limites : motif sans fichier présent, motif qui couvre un répertoire, fichier déclaré mais
  suivi par git, fichier déclaré et non ignoré, conflit entre deux greffons ;
- messages, documentation (`<SEED_SCIONS>/doc/`), `CHANGELOG.md` ;
- numéro de version : `<À CONFIRMER au PA-E4>` ; `SCION_MIN_VERSION` relevé ou non ;
  `SCION_REF` ; effets sur lepton (`check`, liste des fichiers greffés).

**PA-E4** : l'utilisateur valide. Aucune modification avant la réponse.

### 2. Implémentation (`<SEED_SCIONS>`, `espace-projet/ep-2`)
- Tests d'abord, pour chaque cas retenu, qui échouent sur `master`. Plus un test qui prouve qu'un
  greffon sans déclaration se greffe comme avant, fichiers ignorés compris.
- Les tests existants restent verts.
- Commits séparés : évolution, documentation, version.

### 3. Essai (skill `lepton-rootstock`)
- scion de la branche dans un venv `~/lepton-tools-dev/essais/ep-2-venv` (forme d'ENV-65), son
  `bin/` en tête du PATH pour lepton.
- Fixtures rejouées sous `essais/ep-2-fixture/apres/` : sans déclaration, relevés identiques à
  l'avant (`scripts/comparer-releves.py`) ; avec déclaration, le fichier ignoré déclaré est lié,
  le fichier ignoré non déclaré ne l'est pas.
- Sur une copie de `<ROOTSTOCK>` (`essais/ep-2-copie`) : `scion graft` avec le scion de la
  branche, liste `chemin -> cible` identique à celle d'avant.

### 4. Version, lepton, noyau → PA-E5
- Tag annoté local ; `pipx install --force "git+file://<SEED_SCIONS>@<version>"`.
- Références de version selon le PA-E4 ; `pytest` de lepton-tools vert avec le nouveau scion.
- Binaires : pas d'oracle si l'arbre composé ne change pas (raisonnement consigné, forme de
  `doc/devenv/rapports/env-56-scion.md` §6).
- **PA-E5** : rapport ; sort des essais, fixtures et venv ; publication (PA-P) : tag et `master`
  de `<SEED_SCIONS>`, branches `espace-projet/ep-2`, fusions.

## Critères de validation
- [ ] PA-E4 et PA-E5 tranchés et consignés.
- [ ] Aucun nom propre à Lepton ajouté à scion :
      `git -C <SEED_SCIONS> diff 0.6.3.4 -- scion tests | grep -ci '^+.*lepton'` → 0.
- [ ] Tests de scion verts, dont les nouveaux (échec sur `master`, réussite sur la branche).
- [ ] Sans déclaration : fixtures identiques avant et après ; liste `chemin -> cible` de la copie
      de `<ROOTSTOCK>` inchangée.
- [ ] Avec déclaration : ignoré déclaré lié ; ignoré non déclaré absent du trunk.
- [ ] Références de version conformes au PA-E4 ; `pytest` de lepton-tools vert.

## Pièges connus
- Un motif trop large greffe des produits de construction ou des fichiers d'éditeur : c'est ce
  que le filtre E1 empêche. La proposition borne la syntaxe en conséquence.
- `--directory` rend un répertoire ignoré en une seule ligne : un fichier déclaré situé dans un
  répertoire ignoré peut ne pas apparaître dans la sortie de git.
- Si `SCION_REF` change dans le clone noyau, `graft-update` refuse ce clone hors de sa version
  déclarée jusqu'à la fusion dans `master` (`doc/devenv/rapports/env-29-scion.md` §4).
- Les messages de git sont traduits sur la VM (français, espace insécable) : comparer par
  `scripts/comparer-releves.py`.
- Point de retour : `pipx install --force "git+file://<SEED_SCIONS>@0.6.3.4"`.
- Le fichier de poste lui-même (nom, contenu, création par lepton) n'est pas de cette étape :
  EP-4. Les fixtures emploient des noms neutres.

## À la fin de l'étape
`STATUS.md` : statut, branches, §Versions (scion, `SCION_MIN_VERSION`, `SCION_REF`), décisions
PA-E4 et PA-E5, journal. `HORS-PLAN.md` : tout point écarté. Passation `handoff/ep-2.md`.
