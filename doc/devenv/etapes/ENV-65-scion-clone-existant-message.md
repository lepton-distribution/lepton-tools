# Étape ENV-65 — scion : clone existant hors version, message de `git clone` (D25, D22)

## Contexte
Révision du plan du 2026-11-18, faite à partir de `HORS-PLAN.md`. D25 et D22 sont à traiter
(décision de l'utilisateur du 2026-11-17, fin du plan, après ENV-61). Ce ne sont pas des tickets :
seed.scions n'est pas un greffon du rootstock (décision du 2026-11-18). Décision de l'utilisateur
(révision du 2026-11-18) : une seule étape, deux lots, un seul tag.
- **D25** (`rapports/env-60-scion.md` §1.2, §1.3 : k18, k05, l03 ; PA-107) : un clone existant
  est réutilisé sans contrôle de sa version :
  - par `seed-clone` (`graft.sync`), qu'appellent `lepton seed add`, `seed replace` et la greffe
    du projet ;
  - pour une graine distante, par `seed-add` (`cli._clone_seed`), car `seed_updates` n'avance que
    par avance rapide.
  Un clone resté hors de sa version est alors greffé : c'est une greffe fausse, avec le code 0,
  jamais signalée pour une graine. Exemple : un clone laissé par un checkout en échec de scion
  ≤ 0.6.3.1. ENV-60 a corrigé la cause de ces clones (`git clone -b`). Les clones déjà laissés
  restent. Le lot change un comportement : c'est sa variable.
- **D22** (`rapports/env-59-tilde.md` §1.6, O-1 ; déjà vu en ENV-53 C5 et en
  `rapports/env-56-scion.md` §3) : le message d'échec de `git clone` ne garde que la dernière
  ligne de git (« … (code 128) : and the repository exists. »). La cause est perdue (« fatal:
  '…' does not appear to be a git repository »). Le lot ne change qu'un message.

Faits relevés à la révision (`<SEED_SCIONS>` `master` 975caf6, tag `0.6.3.2` ; numéros
indicatifs) :
- `scion/gitops.py:37`, `_run` : sur `CalledProcessError`,
  `detail = stderr.strip().splitlines()`, puis `… (code N) : {detail[-1]}` (l. 53-56). Ce texte
  sert à toutes les commandes git, pas seulement au clonage.
- `scion/graft.py:57`, `sync` : sa docstring dit « An existing clone is left as it is ».
  `_fetch` (l. 275) ne clone que les destinations sans `.git` (l. 281-282).
- `scion/cli.py:96`, `_clone_seed` : une graine distante dont `local/.git` existe est rendue telle
  quelle (l. 108-109).
- Contrôle existant, à réutiliser : `graft.py:342` `clone_updates` (message « N clone(s) à
  remettre à leur version déclarée … », l. 377) et `graft.py:383` `_check_clone`. Ils servent à
  `graft-update`, `seed-update` et `seed-add` depuis 0.5.4.0 (ORCHESTRATION §2bis).
- Références de version :
  - seed.scions : `scion/__init__.py:3`, `tests/test_cli.py:17`, `CHANGELOG.md`, `README.md`
    (l. 367 cite 0.6.3.2) ;
  - lepton-tools : `SCION_MIN_VERSION` (`lepton/__init__.py:16`, (0, 6, 2, 0)), `SCION_REF`
    (`scripts/install-vscodium.sh:56`, `0.6.3.2`), `README.md:11`, note de
    `lepton/__init__.py:14` ;
  - clone noyau : `scripts/install-{macos,debian}.sh`, `README.md`, `README-PAQUET.md`,
    `doc/BUILDING.md`.
- lepton : `tests/test_projection.py:362` (`test_echec_de_scion_sans_double_affichage`) compte
  les lignes `erreur :` du stderr de scion. Un appel en échec les reprend une fois dans
  `lepton: erreur:`, sans relais `scion: …` (ENV-51).

Archétype : infrastructure. Iso-fonctionnel quand le clone existant est à sa version : aucun
clone, aucun lien du trunk ni aucun binaire ne change. scion reste générique (NF-2).

## Prérequis
- ENV-62 terminée. Indépendante d'ENV-63 et d'ENV-64.
- `<SEED_SCIONS>` : `master` 975caf6, tag `0.6.3.2` ; 313 tests de scion.
- Relevés et outils à rejouer : `rapports/env-60-scion.md` §1 (k01 à k19, l01 à l04) et ses
  scripts ; `rapports/env-56-scion/fixture.py`, `essai.sh`, `succes.sh` ; outils d'ENV-62 (D27)
  pour les comparaisons.
- Procédure de version : `rapports/env-60-scion.md` §1.9, §2 (0.6.3.2, correction seule).
- Skill `lepton-rootstock`.
- Branches `devenv/env-65` : `<SEED_SCIONS>`, lepton-tools ; clone noyau si `SCION_REF` change.

## Tâches

### 1. Audit (lecture seule) → PA-117
Rapport `rapports/env-65-scion.md`.
- **D25** : reproduire k18 (clé ordinaire) et k05 (graine distante) avec scion 0.6.3.2, sur des
  rootstocks temporaires sous `essais/env-65-fixture/avant/`. Le clone hors version est mis en
  place à la main par `git -C <clone> checkout <autre>`. Relever message, code, liste greffée,
  liens.
- Relever tous les appelants qui réutilisent un clone existant sans contrôle : `seed-clone`,
  `_clone_seed`, `graft`, `seed-add`, et tout autre trouvé. Pour chacun, relever si le contrôle
  de `_check_clone` s'applique déjà.
- Relever les clones hors de leur version sur `<ROOTSTOCK>` et sur les 7 rootstocks d'essai du
  Mac (liste de `handoff/env-61.md`), en lecture seule (`git -C <clone> rev-parse HEAD` contre la
  version déclarée). Deux attendus distincts :
  - clones de greffons : 0, puisque `graft-update` les refuse depuis 0.5.4.0 ;
  - clones de graine (`depots/lepton-seed.scions/original-tree`, graines distantes) : à relever,
    sans attendu. Le contrôle de 0.5.4.0 ne les vise pas, et `seed_updates` n'avance qu'en
    avance rapide (`rapports/env-60-scion.md` §1.3).
- Scripts de l'audit versionnés sous `rapports/env-65-scion/`, pour être repris en ENV-66.
- **D22** : relever les messages d'échec de git que montre scion, pour un clonage en échec (URL
  absente, dépôt non git, version absente, réseau), et pour d'autres commandes (`checkout`,
  `fetch`). Sorties en anglais (`LC_ALL=C`) et en français (traductions de `po/fr.po`, D27).
  Relever les consignes et outils qui comparent ces messages (`fr()` de
  `consignes/env-61-debian.md:172`, qui ramène « and the repository exists. »).
- **PA-117** : l'utilisateur tranche :
  - D25, correction. Options :
    - refus, avec le message de `_check_clone` (forme P-V1), clone laissé tel quel ;
    - checkout de la version déclarée ;
    - reclonage.
    <À CONFIRMER au PA-117> ;
  - D25, cas couverts (clé ordinaire, graine distante, autres trouvés) ; clé projetée exclue ou
    non (P-V1) ;
  - D22 : message gardé. Options : la ligne `fatal:` (ou `error:`) de git, la première ligne, ou
    toute la sortie de git sous `-v`. Une seule ligne `erreur :`, à cause du test de lepton.
    <À CONFIRMER au PA-117> ;
  - D22, portée : `git clone` seul, ou toutes les commandes git de `_run` ;
  - documentation : docstring de `sync`, `CHANGELOG.md`, `README.md` ;
  - numéro de version : <À CONFIRMER au PA-117 : `0.6.3.3` ou `0.6.4.0`> ;
  - `SCION_MIN_VERSION` relevé ou non ; `SCION_REF` ;
  - effets sur lepton : messages relayés, attendus des tests.
- Aucune modification avant la réponse.

### 2. Implémentation (`<SEED_SCIONS>`, `devenv/env-65`)
- Tests d'abord : un test par cas retenu au PA-117, qui échoue sur `master`. Plus un test qui
  prouve qu'un clone existant à sa version est inchangé. Les 313 tests existants restent verts,
  sauf ceux que le PA-117 inverse.
- Commits séparés : lot D25, lot D22, puis la version (`scion/__init__.py`, `tests/test_cli.py`,
  `CHANGELOG.md`, `README.md`).

### 3. Essai (skill `lepton-rootstock`)
- scion de la branche, sans pipx : venv `~/lepton-tools-dev/essais/env-65-venv`
  (`pip install "git+file://<SEED_SCIONS>@devenv/env-65"`, forme d'ENV-60), son `bin/` en tête
  du PATH pour lepton.
- Cas du §1 rejoués sous `essais/env-65-fixture/apres/` : ceux visés par le PA-117 suivent la
  décision. Les cas d'ENV-56 et d'ENV-60 non visés sont identiques à l'avant, au texte du message
  D22 près.
- lepton : `lepton seed add` sur une copie d'`essais/env-11/qemu` (`essais/env-65-essai`, par
  `rsync -a`, sans `build/`) avec un clone hors version ; message relayé et annulation. Un
  `seed add` réussi, puis `seed remove` : clones et liens identiques à ceux de 0.6.3.2.

### 4. Version, lepton, noyau → PA-118
- Tag annoté local ; `pipx install --force "git+file://<SEED_SCIONS>@<version>"`.
- lepton-tools et clone noyau : références de version selon le PA-117. `pytest` de lepton-tools
  vert avec le nouveau scion.
- `<ROOTSTOCK>` n'est pas regreffé si l'audit n'y trouve aucun clone hors version. Sinon, le
  PA-117 tranche.
- Binaires : pas d'oracle, puisque l'arbre composé ne change pas. Consigner le raisonnement
  (forme de `rapports/env-56-scion.md` §6).
- **PA-118** : rapport ; sort d'`essais/env-65-essai`, d'`essais/env-65-fixture` et du venv ;
  publication (PA-P) : tag et `master` de `<SEED_SCIONS>`, branches `devenv/env-65`, fusions. La
  validation Debian est faite en ENV-66.

## Critères de validation
- [ ] PA-117 et PA-118 tranchés et consignés.
- [ ] Aucun nom propre à Lepton ajouté à scion :
      `git diff 0.6.3.2 -- scion tests | grep -ci '^+.*lepton'` → 0.
- [ ] Tests de scion verts, dont les nouveaux (échec sur `master`, réussite sur la branche).
- [ ] k18 et k05 suivent le PA-117 ; plus aucune greffe fausse d'un clone hors version.
- [ ] Message D22 : la cause donnée par git paraît ; une seule ligne `erreur :`.
- [ ] Références de version conformes au PA-117 ; `pytest` de lepton-tools vert.
- [ ] `HORS-PLAN.md` : D22 et D25 marqués traités, avec renvoi au rapport.

## Pièges connus
- Le hook refuse toute écriture shell sous le `depots/tiers/` de tout rootstock, temporaire
  compris, et `git config` même en lecture. Observer par des lectures ; supprimer la base de la
  fixture entière, par `scripts/supprimer-essai.sh`.
- Mettre un clone hors de sa version sous un rootstock du Mac autre que les temporaires de
  l'étape fausserait les passes suivantes : `graft-update` le refuserait.
- `_run` sert à toutes les commandes git : un message de D22 changé partout change aussi les
  relevés de `checkout` et `fetch` des étapes passées. Ce sont des écarts attendus, à lister.
- D22 change le texte que `fr()` ramène (« and the repository exists. ») : la consigne d'ENV-66
  suit les règles d'ENV-62 (D27), et ses attendus sont relevés avec le nouveau scion.
- `test_echec_de_scion_sans_double_affichage` casse si un nouveau message de scion contient une
  seconde ligne `erreur :`.
- Point de retour après le tag : `pipx install --force "git+file://<SEED_SCIONS>@0.6.3.2"`.
- Si `SCION_REF` change dans le clone noyau, celui-ci passe sur `devenv/env-65`, et
  `graft-update` refuse un clone hors de sa version déclarée jusqu'à la fusion dans `master`
  (`rapports/env-29-scion.md` §4).

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, branches, §Versions (scion), décisions PA-117 et PA-118, journal.
`HORS-PLAN.md` : D22, D25. Passation `handoff/env-65.md`.
