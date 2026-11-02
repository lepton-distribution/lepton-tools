# ENV-23 — Évolutions de scion : mise à jour de la graine, sources non git — 2026-11-02

Session Mac. Branches `devenv/env-23` : lepton-tools (depuis `main` 5aa0882), `<SEED_SCIONS>`
(depuis `master` 472c12e, tag 0.5.2.0). Fichier d'étape : `etapes/ENV-23-scion-0-5-3.md`.

État de départ : lepton-tools `main` 5aa0882, clone noyau `master` 40d7197, graine `original-tree`
15740f9, seed.scions `master` 472c12e, tous propres et alignés sur leurs distants ; scion 0.5.2.0,
lepton 0.1.0 (« requis ≥ 0.5.2.0 »).

## 1. Audit (tâche 1, lecture seule)

### 1.1 `sync`, `seed-update`, `graft-update` (scion 0.5.2.0)

- `cmd_graft_update` (`scion/cli.py:155`) : `ungraft` **d'abord**, puis pour chaque graine de la
  liste greffée (`graft.seeds`, colonne 5 de `.scion.grafted.list`) `sync(update=True)`, puis `graft`.
- `sync` (`scion/graft.py:44`) lit `.scion.ramifications` et `.scion.sources.list` **de la graine
  locale**, puis `_fetch` fait `git pull` (simple, sans `--ff-only`) dans chaque clone de greffon
  distant. **Le dépôt de la graine n'est jamais avancé.**
- Seul `seed-add <URL>` avance la graine (`_clone_seed`, `cli.py:86` : `git pull` si le clone
  existe). `seed-update --seed X` a la même limite que `graft-update`.
- La liste greffée ne garde que le chemin local de la graine (`…/scion/.scion`), pas son URL :
  l'amont se lit sur le dépôt git qui contient la graine (`@{u}`).
- Graine avec modifications ou commits non publiés : aucun contrôle aujourd'hui (rien n'est tiré).
- Ordre : `ungraft` précède tout `pull`. Un échec de `pull` laisse le trunk vide (cas observé en
  ENV-14 : « regreffe en échec … trunk laissé vide »).
- Test existant : `tests/test_graft.py:222` `test_graft_update_pulls_and_regrafts` (graine locale).

### 1.2 Filtre E1 et sources non git

- `_ignored` (`graft.py:150`) : `gitops.toplevel(stem)` ; source hors git **ou** dépôt englobant le
  rootstock → aucun filtre. Sinon `git ls-files --others --ignored --exclude-standard --directory`.
- `_walk` saute ensuite les chemins exclus. `graft` et `graft --scion` retirent d'abord tous les
  liens du greffon (`ungraft` / `_unlink`) : un lien vers un fichier désormais exclu disparaît à la
  regreffe suivante, sans traitement particulier.
- Seule source non git des rootstocks actuels : `building` (`depots/generation/building`, créé par
  `rootstock-install`, `INSTALL_LAYOUT` de `scion/rootstock.py`).
- Essai (dépôt jetable vide, `git --git-dir=<vide> --work-tree=<source> -c core.bare=false ls-files
  --others --ignored --exclude-standard --directory`) : les règles de git s'appliquent aussi à une
  source non git : `a/.DS_Store` (`core.excludesFile` = `~/.gitignore_global` : `*~`, `.DS_Store`,
  `*.swp`, …) et `gen/` (`.gitignore` de la source) exclus ; `._y` non exclu (absent des règles).

### 1.3 Mesures

| Rootstock | Graine | Amont | Locale / publiée | Modifs | Fichiers dans `depots/generation` | Liens du trunk vers `building` |
| --- | --- | --- | --- | --- | --- | --- |
| `<ROOTSTOCK>` | `depots/lepton-seed.scions/original-tree` | `origin/original-tree` (GitHub) | 15740f9 / 15740f9 | 0 | 0 (4 répertoires vides) | 0 |
| `essais/env-13-vierge` | idem | idem | 15740f9 / 15740f9 | 0 | 0 | 0 |
| `essais/env-9`, `env-11/{f429zi,qemu,qemu-gra2,wl55jc1}` | `depots/lepton-seed/<projet>` (git local, `main`) | aucun | — | 0 | — | 0 |

- Aucun écart aujourd'hui : l'essai de la tâche 3 doit reculer la graine d'un commit sur la copie.
- Les `.DS_Store` des rootstocks d'essai (8 à 17 chacun) sont dans des clones git : déjà exclus par
  E1 ; 0 lien `.DS_Store` dans les trunks. Les 4 `.DS_Store` de `building` d'ENV-20 ont été
  supprimés à la main : le cas est à reproduire sur la copie.
- Graines de projet de lepton : dépôts git **sans amont** → la mise à jour doit les laisser telles
  quelles.

### 1.4 Usages par lepton

- lepton n'appelle ni `graft-update` ni `seed-update` (`grep` sur `lepton/`, `extension/src`) ;
  il appelle `graft` (complet ou `--scion`), `seed-add`, `seed-scion-add/remove`.
- Purge de `.DS_Store`/`._*` réguliers du trunk avant `graft` (`is_system_file`,
  `lepton/rootstock.py:34`) : redondante avec E2 quand le fichier de tolérance les liste (décision
  PA-31 (1)), nécessaire sinon (rootstocks sans motif, ex. `bout-en-bout`).
- `SCION_MIN_VERSION = (0, 5, 2, 0)` (`lepton/__init__.py:7`).
- Références « 0.5.2.0 » : lepton-tools `lepton/__init__.py`, `scripts/install-vscodium.sh`,
  `README.md`, `tests/test_milestone5.py` ; clone noyau `scripts/install-{macos,debian}.sh`,
  `doc/BUILDING.md`, `README-PAQUET.md`, `README.md`.
- **N-2** : `lepton/scions.py:121` défaut `depots/lepton-<kind>/<nom>` (`kind` : `bsp`,
  `application`, `library`) ; convention d'ENV-13 `depots/lepton/<kind>-<nom>/master` ; `README.md`
  l. 31 décrit l'ancien défaut.

## 2. Propositions (PA-33)

### G — mise à jour de la graine

- **Forme proposée (G-a)** : comportement par défaut de `graft-update` **et** de `seed-update`
  (« mettre à jour » couvre déjà les clones des greffons). Alternative (G-b) : option explicite
  `--seed` / `--with-seed`.
- Graine concernée : le dépôt git qui contient la graine, s'il a un amont (`@{u}`). Sans amont
  (graines de projet), source non git, ou dépôt englobant le rootstock : laissée telle quelle
  (`-v` : une ligne d'information).
- Garde-fous : `git pull --ff-only` seulement ; refus avant toute action si la graine a des
  modifications suivies (`status --porcelain --untracked-files=no`) ; graine en avance seulement
  (commits non publiés) : rien à tirer, ligne d'information ; graine divergente : refus.
- **Ordre proposé** : contrôler et avancer toutes les graines **avant** `ungraft` ; un refus laisse
  le trunk intact. Les clones des greffons gardent leur `git pull` actuel (hors périmètre).

### N — fichiers étrangers des sources non git

- **Mécanisme proposé (N-a)** : appliquer à une source non git les règles de git du filtre E1
  (`.gitignore` présents dans la source, `core.excludesFile`), par un dépôt git vide temporaire
  (essai §1.2). Générique, aucun fichier nouveau, même règle que E1 (« ignoré par git → jamais
  greffé »). Limite : un nom absent des règles de git de l'hôte n'est pas exclu (ex. `._*` ici).
- Alternative (N-b) : les motifs de `.scion.trunk.tolerated` excluent aussi les noms des sources non
  git (couvre `.DS_Store` et `._*` de `<ROOTSTOCK>`, mais étend le sens du fichier).
- Alternative (N-c) : fichier d'exclusion propre à la source (`<source>/.scion.ignore`).
- Le dépôt englobant le rootstock reste sans filtre (règle d'ENV-15 inchangée).
- Liens déjà greffés : disparaissent à la regreffe suivante (§1.2) ; aucun traitement.
- Exclus listés en `-v`, compte en information (comme E1).

### V — version

- `0.5.3.0` (proposé par le fichier d'étape).

### L — lepton

- `SCION_MIN_VERSION` relevé à `(0, 5, 3, 0)` : une seule version dans tous les documents (critère
  de l'étape) ; `SCION_REF` d'`install-vscodium.sh`, `README.md`, test ; clone noyau
  `install-{macos,debian}.sh`, `doc/BUILDING.md`, `README-PAQUET.md`, `README.md` (branche
  `devenv/env-23` du noyau).
- Purge de `.DS_Store`/`._*` conservée (rootstocks sans motif de tolérance).
- N-2 : défaut de `--repo` aligné sur `depots/lepton/<kind>-<nom>/master`, `README.md` l. 31 et
  test(s) adaptés.

### Tests prévus (scion, écrits d'abord)

1. `graft-update` avance une graine en retard d'un commit (amont local `file://`) ; nouveau greffon
   de la graine greffé.
2. `graft-update` refuse une graine modifiée ; trunk intact, code ≠ 0.
3. `graft-update` refuse une graine divergente ; trunk intact.
4. Graine sans amont : inchangée, `graft-update` code 0 (comportement actuel).
5. `seed-update` avance la graine (si G-a).
6. Source non git : `.DS_Store` (règle globale isolée dans le test) et chemin d'un `.gitignore` de
   la source non greffés ; fichier ordinaire greffé.
7. Lien déjà greffé vers un fichier devenu exclu : retiré par `graft`.

## 3. Décisions PA-33 (2026-11-02, utilisateur)

1. G-a : mise à jour de la graine par défaut dans `graft-update` et `seed-update`, garde-fous du §2.
2. N-a : règles de git d'E1 appliquées aux sources non git (dépôt git vide temporaire).
3. V : 0.5.3.0.
4. L : `SCION_MIN_VERSION` relevé à 0.5.3.0 ; une seule version partout ; purge de lepton conservée.
5. N-2 : défaut de `--repo` aligné sur `depots/lepton/<kind>-<nom>/master` dans ENV-23.

## 4. Implémentation (tâche 2, `<SEED_SCIONS>` `devenv/env-23`)

Tests écrits d'abord et constatés rouges sur 0.5.2.0 (9 échecs : les 3 tests de comportements
inchangés passaient déjà).

| Commit | Objet |
| --- | --- |
| a2eb0cb | N-a : `gitops.ignored_outside` (dépôt vide temporaire, `--git-dir`/`--work-tree`, rien d'écrit dans la source), `_ignored` ; README ; `tests/test_ignored.py` |
| bf6bad3 | G-a : `graft.seed_updates` (contrôles, `fetch`), `graft.advance_seeds` (`merge --ff-only @{u}`) ; `cmd_graft_update` (contrôles → `ungraft` → avance → `sync` → `graft`), `cmd_seed_update` ; aides, README ; `tests/test_seed_update.py` (8 tests) |
| ad292ee | 0.5.3.0 : `__version__`, `CHANGELOG.md`, `tests/test_cli.py` |

- `python3 -m unittest discover -s tests` : **137 tests, OK** (1 ignoré, réseau) ; 126 d'ENV-15
  − 1 remplacé + 4 (N-a) + 8 (G-a).
- **Test changé (à signaler)** : `test_scion_outside_git_is_not_filtered` fixait l'ancien
  comportement (`.DS_Store` d'une source hors git greffé) ; remplacé par
  `test_scion_outside_git_follows_the_global_rules`, conséquence directe de N-a.
  `test_rules_of_a_repository_holding_the_rootstock_do_not_apply` inchangé et vert.
- `grep -ri lepton scion/` : les 2 lignes de métadonnées seules (`__url__`, `__email__`, PA-2 Q7).
- Refus : `ScionError`, code 1 ; échec de `git fetch` : `GitError`, code 2 ; dans les deux cas
  avant `ungraft`.

## 5. Essai sur une copie (tâche 3)

Copie `~/lepton-tools-dev/essais/env-23` (`cp -RP` de `depots/`, `trunk/`, signature et
`.scion.trunk.tolerated` ; sans `build/` ni `third_party/` ; 125 Mo). scion de la branche dans le
venv `~/lepton-tools-dev/essais/env-23-venv` (`pip install <SEED_SCIONS>`, `scion version`
0.5.3.0) **au lieu de `pipx install --force`** du fichier d'étape : le scion global reste 0.5.2.0
jusqu'à la tâche 4 (procédure d'ENV-15, piège du fichier d'étape ; proposition de la session).
Listes par `rapports/env-15-liste-trunk.sh`, dans `~/lepton-tools-dev/essais/env-23-mesures/`
(non versionnées). Référence `<ROOTSTOCK>` : 3941 liens, SHA-256 `9be3357c1d0d70c0…` ; copie
identique.

| Essai | Action | Résultat |
| --- | --- | --- |
| N, 0.5.2.0 | `.DS_Store`, `._resultat`, `resultat.bin` dans `building/output` ; `scion graft` (global) | 3 liens, dont `.DS_Store` (défaut reproduit) |
| N, 0.5.3.0 | `scion graft -v` (venv) | `.DS_Store` exclu (« exclu (ignoré par git) : lepton/building building/output/.DS_Store »), lien retiré ; `._resultat` greffé (`._*` absent de `~/.gitignore_global` : limite annoncée au PA-33) ; source inchangée, aucun `.git` créé |
| retour | fichiers d'essai retirés, `graft` | liste = référence |
| G, préparation | graine de la copie `reset --hard HEAD~1` (15740f9 → f4ff07b, 2 commits de retard) ; `graft-remove lepton@bsp-nucleo-f439zi` (sans `--purge`) | 13 greffons, 3933 liens |
| G, refus | ligne ajoutée à `.scion.ramifications` ; `graft-update` | code 1, « graine … : modifications non commitées … (rien n'a été modifié) » ; liste des liens identique avant/après ; graine à f4ff07b ; modification annulée |
| G, avance | `graft-update` | code 0, « graine … avancée : f4ff07b -> 15740f9 » ; 14 greffons, `.scion.grafted.list` = celle de `<ROOTSTOCK>` ; liens = référence (SHA-256 `9be3357c…`) ; 0 cassé, 0 régulier ; clones propres |

Arbre composé identique : aucune reconstruction requise (raisonnement d'ENV-15 §6).

## 6. Version, lepton, `<ROOTSTOCK>` (tâche 4)

- `<SEED_SCIONS>` : tag annoté local `0.5.3.0` sur ad292ee (commit de version de `devenv/env-23`,
  avant fusion ; 0.5.2.0 était sur la fusion 472c12e) ; `pipx install --force
  "git+file://<SEED_SCIONS>@0.5.3.0"` → `scion version` 0.5.3.0. Rien de poussé.
- lepton-tools `devenv/env-23` : 016a788 **N-2** (`lepton/scions.py:121` défaut
  `depots/lepton/<kind>-<nom>/master`, aide de `--repo`, `README.md` l. 31, `tests/test_milestone4.py`,
  `tests/test_reference_seed.py`) et 5e03b27 **version** (`SCION_MIN_VERSION` (0, 5, 3, 0),
  `SCION_REF="0.5.3.0"` d'`install-vscodium.sh`, `README.md` l. 10). `pytest` : **216 verts** ;
  `shellcheck` 0. lepton réinstallé par pipx : « scion 0.5.3.0 (requis ≥ 0.5.3.0) ».
  Commentaire de `tests/test_milestone5.py:142` (« scion ≥ 0.5.2.0, ENV-15 ») conservé : il date
  l'apparition des exclusions globales.
- Clone noyau `devenv/env-23` (depuis `master` 40d7197) : 62f3f86, `SCION_REF` d'`install-{macos,debian}.sh`,
  `doc/BUILDING.md`, `README-PAQUET.md`, `README.md` à 0.5.3.0 ; `shellcheck` 0 ; plus aucune
  occurrence de 0.5.2.0. Ces documents citent le tag GitHub `0.5.3.0`, à publier au PA-34.
- `<ROOTSTOCK>` regreffé (`scion graft`, 0.5.3.0) : code 0, 3941 liens, liste identique à la
  référence (SHA-256 `9be3357c…`), 0 régulier, 0 cassé ; clone noyau propre ; `lepton check` code
  0 (19 fichiers conformes).
- Validation Debian reportée à ENV-28.

### À signaler au PA-34

1. Test de scion remplacé : `test_scion_outside_git_is_not_filtered` (§4), conséquence de N-a.
2. Limite de N-a constatée : `._*` n'est exclu d'une source non git que s'il figure dans les
   règles de git de l'hôte (`~/.gitignore_global` n'a que `.DS_Store`) ; la purge de lepton ne
   traite que les fichiers réguliers du trunk.
3. Essai par venv au lieu de pipx (§5).
4. Tag sur le commit de version et non sur la fusion dans `master`.

### Publication proposée (PA-34, PA-P)

- `<SEED_SCIONS>` : fusion `--no-ff` de `devenv/env-23` dans `master`, push de `master`, du tag
  `0.5.3.0` (et de `devenv/env-23` si souhaité ; non poussée en ENV-15).
- Clone noyau : fusion `--no-ff` dans `master`, push de `master` et `devenv/env-23`.
- lepton-tools : état et passation commités, fusion `--no-ff` dans `main`, push de `main` et
  `devenv/env-23`.

## 7. Décisions PA-34 et clôture (2026-11-02, utilisateur)

- Points signalés (§6) acceptés.
- `<SEED_SCIONS>` : fusion `--no-ff` dans `master` e4d76b2 (contenu = tag `0.5.3.0`) ; push de
  `master` et du tag par `git@github.com:lepton-distribution/seed.scions.git` (l'`origin` HTTPS
  sans identifiants a échoué : « could not read Username ») ; `devenv/env-23` non poussée.
- Clone noyau : fusion `--no-ff` dans `master` 0a6df02 ; push de `master` et `devenv/env-23`.
- lepton-tools : état et passation commités sur `devenv/env-23`, fusion `--no-ff` dans `main`, push
  de `main` et `devenv/env-23`.
- Copie `essais/env-23` (14 dépôts propres, aucun commit non publié) et venv `essais/env-23-venv`
  supprimés ; `essais/env-23-mesures` conservé (listes de liens).
