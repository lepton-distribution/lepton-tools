# Étape ENV-70 — scion : cause de l'échec de git, version de la graine clonée (D35, D33)

## Contexte
Révision du plan du 2026-11-23, faite à partir de `HORS-PLAN.md`. D35 et D33 sont à traiter.
Décision de l'utilisateur du 2026-11-23, à la fin du plan après ENV-66 : une seule étape, deux
lots, un seul tag, `0.6.3.4`. Ce ne sont pas des tickets : seed.scions n'est pas un greffon du
rootstock.
- **D35** (`rapports/env-66-debian.md` §5.3 : k07, f05 ; `rapports/env-66-mac.md` §4) : le
  message d'échec garde la première ligne non vide du stderr de git (D22, ENV-65). Cas de la VM,
  avec git 2.47.3 et `seed-add --single-branch` sur une version absente :
  - git écrit d'abord « warning: Could not find remote branch <v> to clone. », puis la cause ;
  - le message de scion montre donc l'avertissement, et non la cause.

  git 2.50.1 (Mac) n'écrit pas l'avertissement. Piste notée à ENV-66 : retenir la première ligne
  `fatal:` (ou `error:`) si elle existe. Ce lot ne change qu'un message.
- **D33** (`rapports/env-65-scion.md` §1.4, §3, point 2) : `seed-update` et `graft-update`
  avancent une graine clonée (`depots/<nom>/<version>`, `cli._clone_seed`) par avance rapide sur
  sa branche courante. Ils ne la comparent pas à la version demandée au `seed-add`, qui n'est
  écrite que dans le nom du répertoire. Une graine restée hors de sa version n'est pas signalée
  par ces commandes ; `seed-add` la contrôle depuis ENV-65. Ce lot change un comportement.

Faits relevés à la révision (`<SEED_SCIONS>` `master` 49ca4ae, tag `0.6.3.3` ; numéros
indicatifs) :
- `scion/gitops.py:37`, `_run` : `detail` = lignes non vides du stderr, puis `detail[0]`
  (l. 62-65). Ce texte sert à toutes les commandes git.
- `scion/graft.py:515`, `seed_updates` : ne voit que le dépôt de chaque graine (hors git, sans
  amont, dans le dépôt du rootstock : laissée). Appelé par la l. 374.
- `scion/cli.py:96`, `_clone_seed` : `local = rootstock.depots / name / version`. Il contrôle une
  graine existante par `graft.version_fault(local, version, declared="demandée")`
  (`graft.py:424`), le contrôle à réutiliser.
- Références de version, d'après ENV-65 :
  - seed.scions : `scion/__init__.py:3`, `tests/test_cli.py`, `CHANGELOG.md`, `README.md` ;
  - lepton-tools : `SCION_MIN_VERSION` (`lepton/__init__.py:18`, (0, 6, 2, 0)) et `SCION_REF`
    (`scripts/install-vscodium.sh:56`, `0.6.3.3`) ;
  - clone noyau : `scripts/install-{macos,debian}.sh`, `README.md`, `README-PAQUET.md`,
    `doc/BUILDING.md`.

Archétype : infrastructure. Iso-fonctionnel quand la graine est à sa version : aucun clone, aucun
lien du trunk ni aucun binaire ne change. scion reste générique (NF-2).

## Prérequis
- ENV-66 terminée ; ENV-67 conseillée avant. Indépendante d'ENV-68, ENV-69, ENV-71.
- `<SEED_SCIONS>` `master` 49ca4ae, tag `0.6.3.3` ; 340 tests de scion ; `pytest` de lepton-tools :
  570, plus ceux des étapes faites avant.
- Outils à rejouer : `rapports/env-65-scion/fixture.py`, `essai.sh` et leurs relevés ;
  `rapports/env-56-scion/fixture.py` ; `scripts/comparer-releves.py` (D27).
- Traductions de git : `po/fr.po` v2.47.3, octet pour octet (ORCHESTRATION §2bis).
- Procédure de version : `rapports/env-65-scion.md` §7 (version, lepton, noyau), §8 (binaires).
- Skill `lepton-rootstock`. Branches `devenv/env-70` : `<SEED_SCIONS>`, lepton-tools, clone noyau
  si `SCION_REF` change.

## Tâches

### 1. Audit (lecture seule) → PA-127
Rapport `rapports/env-70-scion.md`. Fixtures sous `essais/env-70-fixture/avant/`.
- **D35** : relever, pour les cas k07 et f05 et pour les autres échecs des fixtures, toutes les
  lignes du stderr de git. Relever leur préfixe (`fatal:`, `error:`, `warning:`, `hint:`) en
  anglais (`LC_ALL=C`) et en français (traductions de `po/fr.po` v2.47.3). Relever les préfixes
  traduits et les espaces qu'ils portent (U+00A0).
- **D33** : graine distante clonée, mise hors de sa version à la main
  (`git -C <graine> checkout <autre>`), puis `seed-update` et `graft-update`. Ces deux commandes
  sont lancées en processus par la fixture (`fixture.py`, forme d'ENV-65), sur ses rootstocks
  temporaires : elles ne sont pas tapées par la session et ne touchent aucun rootstock existant.
  Un lancement direct, s'il en faut un, passe par l'invite `ask` et l'accord PA-P donné au plan de
  session (forme d'ENV-60). Relever message, code, avance éventuelle, liste greffée. Relever tous les chemins par lesquels une graine arrive à
  `seed_updates`, et comment distinguer une graine clonée par `_clone_seed` d'une graine donnée
  par chemin.
- Relever les graines distantes clonées des rootstocks du Mac et leur version, en lecture seule,
  et, d'après leurs rapports, celles des rootstocks de la VM (`depots/lepton-seed.scions/original-tree`) :
  une graine hors de sa version y ferait échouer C3 d'ENV-72.
- **PA-127** : l'utilisateur tranche :
  - D35 : règle du message. Options :
    - première ligne dont le préfixe est `fatal:` ou `error:`, anglais et traductions, sinon la
      première ligne non vide ;
    - lignes `warning:` et `hint:` écartées ;
    - git lancé avec `LC_ALL=C`, ce qui change la langue des messages.

    Une seule ligne `erreur :`. <À CONFIRMER au PA-127> ;
  - D33 : correction. Options :
    - refus avec le message de `version_fault`, rien n'étant changé ;
    - signalement seul.

    Graines couvertes : celles clonées sous `depots/<nom>/<version>`. Tag ou branche.
    <À CONFIRMER au PA-127> ;
  - documentation ; `CHANGELOG.md` ; version `0.6.3.4` (décision du 2026-11-23) ;
    `SCION_MIN_VERSION` relevé ou non ; `SCION_REF` ; effets sur lepton.
- Aucune modification avant la réponse.

### 2. Implémentation (`<SEED_SCIONS>`, `devenv/env-70`)
- Tests d'abord, pour chaque cas retenu, qui échouent sur `master`. Plus un test qui prouve qu'une
  graine à sa version avance comme avant. Les 340 tests restent verts, sauf ceux que le PA-127
  inverse.
- Commits séparés : lot D35, lot D33, puis la version.

### 3. Essai (skill `lepton-rootstock`)
- scion de la branche dans un venv `~/lepton-tools-dev/essais/env-70-venv` (forme d'ENV-65),
  son `bin/` en tête du PATH pour lepton.
- Fixtures rejouées sous `essais/env-70-fixture/apres/` : les cas visés suivent le PA-127. Les
  autres sont identiques à l'avant, au texte du message de D35 près.
- Message de D35 en français, par les traductions de `po/fr.po` : la cause paraît.

### 4. Version, lepton, noyau → PA-128
- Tag annoté local ; `pipx install --force "git+file://<SEED_SCIONS>@0.6.3.4"`.
- Références de version selon le PA-127 ; `pytest` de lepton-tools vert avec le nouveau scion.
- Binaires : pas d'oracle, l'arbre composé ne change pas (raisonnement consigné, forme de
  `rapports/env-56-scion.md` §6).
- **PA-128** : rapport ; sort des essais, fixtures et venv ; publication (PA-P) : tag et `master`
  de `<SEED_SCIONS>`, branches `devenv/env-70`, fusions. La preuve avec git 2.47.3 se fait sur la
  VM, en ENV-72.

## Critères de validation
- [ ] PA-127 et PA-128 tranchés et consignés.
- [ ] Aucun nom propre à Lepton ajouté à scion :
      `git diff 0.6.3.3 -- scion tests | grep -ci '^+.*lepton'` → 0.
- [ ] Tests de scion verts, dont les nouveaux (échec sur `master`, réussite sur la branche).
- [ ] D35 : avec un stderr à avertissement d'abord (cas simulé), la cause paraît ; une seule ligne
      `erreur :`.
- [ ] D33 : une graine clonée hors de sa version suit le PA-127 ; à sa version, elle avance comme
      avant.
- [ ] Références de version conformes au PA-127 ; `pytest` de lepton-tools vert.
- [ ] `HORS-PLAN.md` : D33 et D35 marqués traités, avec renvoi au rapport.

## Pièges connus
- Le Mac a git 2.50.1, qui n'écrit pas l'avertissement de D35 : le cas se simule par un stderr
  fabriqué dans les tests, et se prouve sur la VM en ENV-72.
- Les préfixes de git sont traduits : « fatal » est suivi d'une espace insécable en français. Une
  règle par préfixe anglais seul ne tient pas dans une autre langue.
- `test_echec_de_scion_sans_double_affichage` (lepton-tools) casse si un message contient une
  seconde ligne `erreur :`.
- Une graine donnée par chemin n'a pas de version dans son nom : ne pas la refuser.
- Mettre une graine hors de sa version ailleurs que dans les fixtures de l'étape fausserait les
  passes suivantes.
- Si `SCION_REF` change dans le clone noyau, `graft-update` refuse ce clone hors de sa version
  déclarée jusqu'à la fusion dans `master` (`rapports/env-29-scion.md` §4).
- Point de retour : `pipx install --force "git+file://<SEED_SCIONS>@0.6.3.3"`.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, branches, §Versions (scion), décisions PA-127 et PA-128, journal.
`HORS-PLAN.md` : D33, D35. Passation `handoff/env-70.md`.
