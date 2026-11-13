# Étape ENV-60 — scion : clone gardé après un checkout en échec (D18)

## Contexte
Révision du plan du 2026-11-13, faite à partir de `HORS-PLAN.md` : D18 est à traiter (décision de
l'utilisateur du 2026-11-13, fin du plan, après ENV-57). Constat f06 d'ENV-56
(`rapports/env-56-scion.md` §1.5), ajouté au hors-plan au PA-99.

Cas : une clé ordinaire dont la version manque à l'origine, sans `--single-branch`.
- Le `git clone` réussit, puis le `git checkout` échoue (code 1 de git ; `seed-add` sort avec le
  code 2).
- Le clone reste sur la branche de l'origine. Le message ne le dit pas :
  `erreur : échec de « git checkout nope » (code 1) : error: pathspec 'nope' did not match any
  file(s) known to git` (`rapports/env-56-scion/fixture-avant/f06.err`).
- Au passage suivant, le contrôle de version arrête la commande (code 1, « 1 clone(s) à remettre à
  leur version déclarée … introuvable dans le clone ») : il n'y a jamais de greffe fausse.
- Une clé projetée, dans le même cas, le dit : « clone laissé en place » (P-V1).

Faits relevés à la révision (`<SEED_SCIONS>` `master` d650414, tag `0.6.3.1` ; numéros
indicatifs) :
- `scion/gitops.py:94`, `clone()` :
  - sans `single_branch`, il lance `git clone`, puis `git checkout <version>` (l. 110), dans
    `clone_parents` ;
  - sa docstring (l. 102-103) dit « a clone whose checkout fails is kept ». Le parent n'est pas
    vide, donc rien n'est retiré (ENV-56, §3).
- Appelants de `clone()` :
  - `scion/graft.py:290` (`_fetch`, clés ordinaires) ;
  - `scion/cli.py:110` (`_clone_seed`, graine distante).
- Clé projetée : `graft.py:300`, `ScionError(… (clone laissé en place)…)`. Spécification :
  P-V1 de `doc/projection-miroir.md` (« Le clone reste alors en place, comme le clone d'une
  version introuvable en 0.5.4.0 »).
- Contrôle du passage suivant : `graft.py:377` et `graft.py:410`.
- La conservation est documentée :
  - `CHANGELOG.md` 0.6.3.1 (l. 17-19) : « Un clone réussi reste en place comme avant : version
    introuvable (P-V1), checkout en échec, … » ;
  - `README.md` (l. 361-365) : « … de même qu'un clone réussi dont la version est
    introuvable ».
  Retirer le clone, ou ne plus le garder, renverse donc une règle écrite, à laquelle P-V1 renvoie.

Archétype : infrastructure. Iso-fonctionnel quand la version existe : aucun clone, aucun lien du
trunk ni aucun binaire ne change. scion reste générique (NF-2).

## Prérequis
- ENV-57 terminée ; ENV-58 conseillée avant (formes des commandes). Indépendante d'ENV-59.
- `<SEED_SCIONS>` : `master` d650414, tag `0.6.3.1` ; 298 tests verts, 1 sauté (`test_network`).
- Relevés d'ENV-56 à rejouer : `rapports/env-56-scion/fixture.py` (cas f01 à f12b, dont f06),
  `essai.sh`, `succes.sh`, et les relevés `fixture-avant/`, `fixture-apres/`.
- lepton :
  - `_undo_add` (`lepton/seed.py:654`) : sa docstring dit « le clone éventuel est conservé » ;
  - `tests/test_projection.py:362` (`test_echec_de_scion_sans_double_affichage`) compte les
    lignes `erreur :` du stderr de scion ;
  - lepton relaie le stderr de scion en lignes `scion: …` (ENV-51).
- Procédure de version : `rapports/env-56-scion.md` §3, §5. Précédent d'une correction seule :
  0.6.3.1.
- Références de version :
  - seed.scions : `scion/__init__.py`, `tests/test_cli.py`, `CHANGELOG.md`, `README.md` ;
  - lepton-tools : `SCION_MIN_VERSION` (`lepton/__init__.py:14`, (0, 6, 2, 0)), `SCION_REF`
    (`scripts/install-vscodium.sh:56`, `0.6.3.1`), `README.md:11`, note de
    `lepton/__init__.py` ;
  - clone noyau : `scripts/install-{macos,debian}.sh`, `README.md`, `README-PAQUET.md`,
    `doc/BUILDING.md`.
- Skill `lepton-rootstock`.
- Branches `devenv/env-60` : `<SEED_SCIONS>`, lepton-tools ; clone noyau si `SCION_REF` change.

## Tâches

### 1. Audit (lecture seule) → PA-107
- Rejouer f06 avec scion 0.6.3.1 (`fixture.py`, base sous `essais/env-60-fixture/avant/`).
  Relever au rapport `rapports/env-60-scion.md` §1 :
  - message, code, état du clone : branche, `HEAD`, fichiers extraits ;
  - puis le passage suivant (`seed-add` relancé) et son message.
- Mêmes relevés, toujours sur des rootstocks temporaires :
  - graine distante dont la version manque : `scion seed-add --version <absente> <URL d'un dépôt
    présent>` (`_clone_seed`). Une URL absente relèverait f10 (D14), pas D18 ;
  - `graft-update` qui ajoute une clé ordinaire de version absente :
    - sur accord PA-P, donné au plan de session ;
    - lancé par la session hors script, jamais par `fixture.py` (D20, ORCHESTRATION §2bis) ;
    - invite `ask` confirmée par l'utilisateur, la cible étant le rootstock temporaire ;
  - lepton : `lepton seed add <nom> file://localhost<dépôt>@<absente>` sur `essais/env-60-essai`
    (copie d'`essais/env-11/qemu` par `rsync -a`, sans `build/`), message relayé et annulation.
- Distinguer les cas : version absente de l'origine, et version présente dont le checkout échoue
  pour une autre raison (fichiers non suivis, droits). Chercher si le second cas peut se produire
  sur un clone neuf.
- Documentation : relever chaque texte qui fixe le sort d'un clone dont la version est
  introuvable ou dont le checkout échoue (`CHANGELOG.md`, `README.md`, P-V1, docstring de
  `clone()`), et la version qui l'a introduit.
- **PA-107** : l'utilisateur tranche :
  - correction. Options :
    - un message qui dit que le clone est laissé en place, et sur quelle branche (forme P-V1) ;
    - le retrait du clone créé par l'appel ;
    - un contrôle de la version avant le checkout, sans clone gardé.
    <À CONFIRMER au PA-107> ;
  - cas couverts (clé ordinaire, graine distante, autres trouvés) ;
  - niveau du message (normal, ou sous `-v`) et texte ; sans `erreur :` supplémentaire, à cause du
    test de lepton ;
  - documentation : `CHANGELOG.md`, `README.md` et docstring de `clone()` ; P-V1 si le sort du
    clone ou la forme de la clé projetée change ;
  - numéro de version : <À CONFIRMER au PA-107 : `0.6.3.2` ou `0.6.4.0`> ;
  - `SCION_MIN_VERSION` relevé ou non ; `SCION_REF` : <À CONFIRMER au PA-107> ;
  - effets sur lepton : docstring de `_undo_add`, message d'annulation.
- Aucune modification avant la réponse.

### 2. Implémentation (`<SEED_SCIONS>`, `devenv/env-60`)
- Tests d'abord : un test par cas retenu au PA-107, qui échoue sur `master`. Plus un test qui
  prouve qu'un clone dont la version existe est inchangé. Les 298 tests existants restent verts.
- Commits séparés : un par comportement, puis un pour la version (`scion/__init__.py`,
  `tests/test_cli.py`, `CHANGELOG.md`, `README.md`).

### 3. Essai (skill `lepton-rootstock`)
- scion de la branche, sans pipx : venv `~/lepton-tools-dev/essais/env-60-venv`
  (`pip install "git+file://<SEED_SCIONS>@devenv/env-60"`, forme d'ENV-56), son `bin/` en tête du
  PATH pour lepton.
- `fixture.py` rejoué avec la branche (`essais/env-60-fixture/apres/`) :
  - f06 et les cas du §1 suivent le PA-107 ;
  - les cas d'ENV-56 non visés par le PA-107 sont identiques à l'avant (`.cmd`, `.out`, `.err`,
    `.code`, `.depots`).
- `essais/env-60-essai` : cas lepton du §1, avant et après. Liens du trunk et graine égaux au
  départ après chaque essai.
- Un `seed add` réussi, puis `seed remove` (`succes.sh` d'ENV-56) : clones et liens identiques à
  ceux de 0.6.3.1.

### 4. Version, lepton, noyau → PA-108
- Tag annoté local ; `pipx install --force "git+file://<SEED_SCIONS>@<version>"`.
- lepton-tools et clone noyau : références de version selon le PA-107 ; docstring de `_undo_add`
  si le PA-107 change le sort du clone. `pytest` de lepton-tools vert avec le nouveau scion (453
  après ENV-57, plus les tests d'ENV-59 si elle a précédé).
- `<ROOTSTOCK>` n'est pas regreffé : la correction ne touche que des chemins d'échec. Si l'audit
  montre le contraire, le PA-107 tranche.
- Binaires : pas d'oracle, puisque l'arbre composé ne change pas. Consigner le raisonnement
  (forme de `rapports/env-56-scion.md` §6).
- **PA-108** : rapport ; sort d'`essais/env-60-essai`, d'`essais/env-60-fixture` et du venv ;
  publication (PA-P) : tag et `master` de `<SEED_SCIONS>`, branches `devenv/env-60`, fusions. La
  validation Debian est faite en ENV-61.

## Critères de validation
- [ ] PA-107 et PA-108 tranchés et consignés.
- [ ] Aucun nom propre à Lepton ajouté à scion :
      `git diff 0.6.3.1 -- scion tests | grep -ci '^+.*lepton'` → 0.
- [ ] Tests de scion verts, dont les nouveaux (échec sur `master`, réussite sur la branche).
- [ ] f06 suit le PA-107 ; les cas d'ENV-56 non visés par le PA-107 sont identiques à l'avant.
- [ ] `seed add` réussi identique à 0.6.3.1.
- [ ] Références de version conformes au PA-107 ; `pytest` de lepton-tools vert.
- [ ] `HORS-PLAN.md` : D18 marqué traité, avec renvoi au rapport.

## Pièges connus
- Le hook refuse toute écriture shell sous le `depots/tiers/` de tout rootstock, temporaire
  compris. Observer par des lectures ; supprimer la base de la fixture entière, par
  `scripts/supprimer-essai.sh`.
- Un retrait du clone toucherait un répertoire non vide créé par l'appel. Ce n'est pas la règle
  d'ENV-56, qui ne retire que des répertoires vides : ne jamais étendre `clone_parents` sans
  décision du PA-107.
- `graft-update` refuse un clone hors de sa version déclarée avant tout dégreffage
  (ORCHESTRATION §2bis). Un clone laissé par f06 bloque donc les passes suivantes tant qu'il
  n'est pas remis ou retiré.
- `test_echec_de_scion_sans_double_affichage` casse si un nouveau message de scion contient
  `erreur :`.
- lepton trouve scion par le PATH : placer le `bin/` du venv en tête du PATH de la commande.
- Point de retour après le tag : `pipx install --force "git+file://<SEED_SCIONS>@0.6.3.1"`.
- Si `SCION_REF` change dans le clone noyau, celui-ci passe sur `devenv/env-60`, et
  `graft-update` refuse un clone hors de sa version déclarée jusqu'à la fusion dans `master`
  (`rapports/env-29-scion.md` §4).

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, branches, §Versions (scion, et lepton s'il est réinstallé),
décisions PA-107 et PA-108, journal. `HORS-PLAN.md` : D18. Passation `handoff/env-60.md`.
