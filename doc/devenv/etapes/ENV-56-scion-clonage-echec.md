# Étape ENV-56 — scion : répertoires laissés par un clonage en échec (D14)

## Contexte
Révision du plan du 2026-11-12, faite à partir de `HORS-PLAN.md` : D14 est à traiter (décision de
l'utilisateur du 2026-11-12, fin du plan). Après l'échec d'un `seed add` (clonage impossible), un
répertoire vide `depots/<étagère>/<greffon>` reste dans le rootstock, par exemple
`depots/lepton/library-absent`. La graine et le trunk sont, eux, restaurés. Constaté au Mac
(relevés 03 et 06) et deux fois sur la VM (`rapports/env-53-mac.md` §1.5, O-2 ;
`rapports/env-53-debian.md` §5.2, §5.3, §7, constat 8).

Fait relevé à la révision (`<SEED_SCIONS>` `master` 6416c33, numéros indicatifs) :
- `scion/gitops.py` : `clone` (l. 70) et `clone_partial` (l. 80) créent le répertoire parent par
  `dest.parent.mkdir(parents=True, exist_ok=True)`, puis lancent `git clone`. En cas d'échec,
  git retire `<version>/`, mais pas ce parent.
- Appelants : `scion/cli.py` `_clone_seed` (l. 110, graine distante) ; `scion/graft.py` `_fetch`
  (l. 290 `clone`, l. 292 `clone_partial`).
- Même forme dans `scion/mirror.py` `sync_one` (l. 271 : `work.parent.mkdir`, puis
  `git clone --mirror`).

Décision de l'utilisateur (révision du 2026-11-12) : la correction se fait dans scion. Elle est
générique et couvre tout appelant, pas seulement lepton. scion reste générique (NF-2).
Archétype : infrastructure. Iso-fonctionnel quand le clonage réussit : aucun clone, aucun lien du
trunk ni aucun binaire ne change.

## Prérequis
- ENV-53 terminée ; ENV-54 conseillée avant (règles de permission pour les essais). Indépendante
  d'ENV-55.
- `<SEED_SCIONS>` : `master` 6416c33, tag `0.6.3.0` ; 282 tests (ENV-52).
- lepton : `add_scion` (`lepton/seed.py` l. 605) lance `seed-scion-add`, puis `seed-clone`. En
  cas d'échec, `_undo_add` (l. 637) lance `seed-scion-remove` et écrit « ajout de … annulé
  (graine et trunk restaurés) ». `seed replace` (l. 686) suit le même chemin, par `_attach`.
- Procédure de version : `rapports/env-29-scion.md`, `rapports/env-44-residus.md` §3.1,
  `rapports/env-52-scion.md`. Précédent d'une version corrective : 0.6.2.0 (`CHANGELOG.md`,
  « Corrections »).
- Références de version :
  - seed.scions : `scion/__init__.py`, `CHANGELOG.md`, test de version, `README.md` (sections par
    version), ligne « Versions » de `doc/projection-miroir.md` ;
  - lepton : `SCION_MIN_VERSION` (`lepton/__init__.py:12`, (0, 6, 2, 0)), `README.md`,
    `SCION_REF` de `scripts/install-vscodium.sh` (l. 56, `0.6.3.0`) ;
  - clone noyau : `scripts/install-{macos,debian}.sh`, `README.md`, `README-PAQUET.md`,
    `doc/BUILDING.md`.
- Skill `lepton-rootstock`.
- Branches `devenv/env-56` : `<SEED_SCIONS>`, lepton-tools ; clone noyau si `SCION_REF` change.

## Tâches

### 1. Audit (lecture seule) → PA-99
- Recenser dans scion chaque répertoire créé avant une opération qui peut échouer : clonage
  complet, clonage partiel, travail d'un miroir, et tout autre cas trouvé. Pour chacun :
  - ce qui reste après l'échec ;
  - si le parent existait déjà (autre version du même greffon, étagère déjà présente) ;
  - si l'étagère `depots/<étagère>/` elle-même peut être créée par l'appel.
  Tableau au rapport `rapports/env-56-scion.md` §1.
- Essais, jamais dans `<ROOTSTOCK>`, de clonages en échec :
  - sur `essais/env-56-essai` (§3) : nouvelle étagère, étagère existante, parent qui porte déjà
    une autre version ;
  - sur un rootstock temporaire construit comme les fixtures de `<SEED_SCIONS>/tests/`
    (`support.py`, `make_fixture.py`), avec une URL d'amont ou de miroir absente
    (`file://localhost/…`) :
    - clé projetée (`clone_partial`) ;
    - miroir inaccessible, par `mirror-sync --dry-run`. Le clonage du dépôt de travail a lieu
      avant le test de `dry_run` (`mirror.py` l. 270-276). Jamais `mirror-sync` sans
      `--dry-run`, qui pousse vers les miroirs.
  `essais/env-11/qemu` n'a ni projections, ni miroirs, ni `depots/tiers/`.
- Distinguer D14 des cas où un clone réussi est gardé exprès : par exemple « clone laissé en
  place » dans `_fetch`, quand la version épinglée manque. Ces cas restent inchangés.
- Spécification : chercher si une règle de `doc/projection-miroir.md` ou de `README.md` décrit le
  sort d'un clonage en échec.
- Effets sur lepton : `_undo_add` et son message ; rien d'autre ne doit changer.
- **PA-99** : l'utilisateur tranche :
  - portée : seuls les répertoires vides créés par l'appel en échec ; jamais un répertoire
    préexistant ou non vide. <À CONFIRMER au PA-99> ;
  - cas couverts (clonage, clonage partiel, miroir, autres trouvés) : <À CONFIRMER au PA-99> ;
  - message de scion à l'utilisateur (retrait signalé ou silencieux) : <À CONFIRMER au PA-99> ;
  - amendement éventuel de la spécification ou du `README.md` ;
  - numéro de version : <À CONFIRMER au PA-99 : `0.6.3.1` ou `0.6.4.0`> ;
  - `SCION_MIN_VERSION` de lepton relevé ou non ; `SCION_REF` : <À CONFIRMER au PA-99>.
- Une éventuelle part scion de D13 n'est pas traitée ici : elle va dans une étape scion insérée
  (PA-97 d'ENV-55).
- Aucune modification avant la réponse.

### 2. Implémentation (`<SEED_SCIONS>`, `devenv/env-56`)
- Tests d'abord : un test par cas retenu au PA-99, qui échoue sur `master`. Plus un test qui
  prouve qu'un répertoire préexistant est gardé. Les 282 tests existants restent verts.
- Commits séparés : un par comportement, puis un pour la version (`CHANGELOG.md`, test de
  version, `README.md`, ligne « Versions » de la spécification si elle s'applique).

### 3. Essai (skill `lepton-rootstock`)
- scion de la branche, sans pipx : venv `~/lepton-tools-dev/essais/env-56-venv`
  (`pip install <SEED_SCIONS>`, forme d'ENV-29), ou `PYTHONPATH=<SEED_SCIONS> python3 -m scion.cli`.
- Rootstock d'essai `essais/env-56-essai` : copie d'`essais/env-11/qemu` par `rsync -a`, sans
  `build/` (forme d'`essais/env-53-c5`, `rapports/env-53-mac.md` §1.5).
- Essais, d'abord avec scion 0.6.3.0 (attendu : résidu présent), puis avec la branche (attendu :
  aucun résidu) :
  - `lepton seed add absent file://localhost<…>/env-56-absent.git --type bibliotheque --no-cmake` :
    code 2 ; présence de `depots/lepton/library-absent` relevée ;
  - même essai par `scion seed-scion-add`, puis `seed-clone`, lancés à la main, puis annulé par
    `seed-scion-remove` ;
  - après chaque essai : liens du trunk et graine égaux à l'avant ; avec 0.6.3.0, le résidu est
    retiré par `rmdir`.
- Avec la branche : un `seed add` qui réussit (forme du relevé 01 d'ENV-53), puis `seed remove` :
  clones et liens identiques à ceux obtenus avec scion 0.6.3.0.
- Cas de la clé projetée et du miroir : sur le rootstock temporaire de la tâche 1, mêmes
  attendus.

### 4. Version, lepton, noyau → PA-100
- Tag annoté local de la version ; `pipx install --force "git+file://<SEED_SCIONS>@<version>"`.
- lepton-tools et clone noyau : références de version selon le PA-99 ; `pytest` vert avec le
  nouveau scion (384 après ENV-53, plus les tests d'ENV-55 si elle a précédé).
- `<ROOTSTOCK>` n'est pas regreffé : la correction ne touche que les chemins d'échec. Si l'audit
  montre le contraire, le PA-99 tranche.
- Binaires : pas d'oracle, puisque l'arbre composé ne change pas. Consigner le raisonnement
  (forme de `rapports/env-15-scion.md` §6).
- **PA-100** : rapport ; sort d'`essais/env-56-essai` et du venv ; publication (PA-P) : tag et
  `master` de `<SEED_SCIONS>`, branches `devenv/env-56`, fusions. La validation Debian est faite
  en ENV-57.

## Critères de validation
- [ ] PA-99 et PA-100 tranchés et consignés.
- [ ] Aucun nom propre à Lepton ajouté à scion :
      `git diff 0.6.3.0 -- scion tests | grep -ci '^+.*lepton'` → 0 (forme d'ENV-39 et
      d'ENV-52).
- [ ] Tests de scion verts, dont les nouveaux (échec sur `master`, réussite sur la branche).
- [ ] Essai : aucun répertoire résiduel après chaque échec retenu ; répertoire préexistant gardé ;
      `seed add` réussi identique à 0.6.3.0.
- [ ] Références de version conformes au PA-99.
- [ ] `HORS-PLAN.md` : D14 marqué traité, avec renvoi au rapport.

## Pièges connus
- `exist_ok=True` : le parent peut déjà exister et porter une autre version du même greffon
  (`depots/<étagère>/<greffon>/<autre version>`). Ne jamais retirer un répertoire préexistant ou
  non vide.
- Retirer seulement ce que l'appel a créé : relever, avant `mkdir`, le premier ancêtre absent.
- Le hook refuse toute écriture shell sous le `depots/tiers/` de tout rootstock, temporaire
  compris (`proteger-trunk.py`, `zone_protegee`). Observer par des lectures ; nettoyer par scion,
  ou en supprimant le rootstock temporaire entier.
- `tests/test_projection.py` l. 362-370 (`test_echec_de_scion_sans_double_affichage`) compte les
  lignes `erreur :` du stderr de scion. Un nouveau message d'échec de scion peut le casser : lancer
  le `pytest` de lepton-tools avec le nouveau scion.
- `_fetch` ajoute au message d'erreur la suggestion d'un miroir (`_mirror_hint`) : la garder.
- lepton trouve scion par le PATH : pour un essai par lepton avec le scion du venv, placer le
  `bin/` du venv en tête du PATH de la commande.
- Point de retour après le tag : `pipx install --force "git+file://<SEED_SCIONS>@0.6.3.0"`.
- Si `SCION_REF` change dans le clone noyau, celui-ci passe sur `devenv/env-56`, et
  `graft-update` refuse un clone hors de sa version déclarée jusqu'à la fusion dans `master`
  (`rapports/env-29-scion.md` §4).

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, branches, §Versions (scion, et lepton s'il est réinstallé),
décisions PA-99 et PA-100, journal. `HORS-PLAN.md` : D14. Passation `handoff/env-56.md`.
