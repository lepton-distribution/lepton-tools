# Étape ENV-52 — scion : extraction partielle des clones projetés (D11)

## Contexte
Révision du plan du 2026-11-12, faite à partir de `HORS-PLAN.md` : D11 est à traiter (décision de
l'utilisateur du 2026-11-10). Un clone projeté est extrait en entier, quel que soit le nombre de
fichiers projetés. P-V2 (`<SEED_SCIONS>/doc/projection-miroir.md` §A.8) crée le clone par
`git clone --filter=blob:none --no-checkout`, puis `git checkout --detach <version>` de l'arbre
entier ; le `sparse-checkout` est hors périmètre (§C). Cas qui fonde D11 : le clone
`depots/tiers/stm32cubewl/v1.6.0` compte 8 947 fichiers (hors sous-modules), environ 156 Mo, pour
39 fichiers projetés (`HORS-PLAN.md` D11 ; `DEVENV-STATUS.md` §Décisions, PA-86 ; 156 Mo :
`rapports/env-49-wl-hal.md` §1.2). Chaque rootstock qui greffe la famille WL le télécharge.

Décision de l'utilisateur (révision du 2026-11-12) : une seule étape. La spécification est amendée
et validée au PA-91, avant toute ligne de code (forme d'ENV-29).

scion reste générique (NF-2). Archétype : infrastructure, iso-fonctionnel : liens du trunk,
contenus projetés et binaires inchangés ; seuls changent les fichiers extraits dans les clones.

## Prérequis
- ENV-50 terminée ; indépendante d'ENV-51 (ordre du plan : après ENV-51).
- `<SEED_SCIONS>` : `master` 7e8a0cc, tag `0.6.2.0` ; 269 tests réussis, 1 sauté (réseau)
  (`rapports/env-44-residus.md` §3.1).
- Code (relevé au 2026-11-12) : `scion/graft.py` (`_fetch`, qui crée le clone par
  `gitops.clone_partial` puis `gitops.checkout_detached` ; `_remote_clones`, `_pinned`,
  `clone_updates`, `_check_projected_clone`, `_check_shared_clones`) ; `scion/gitops.py`
  (`tracked_changes` : contrôle P-E1) ; `scion/projection.py`.
- Spécification : `projection-miroir.md` §A.8 (P-V1 à P-V6, P-E1), §A.10 (P-G3), §A.11, §C.
- Procédure de version : `rapports/env-29-scion.md`, `rapports/env-44-residus.md` §3.1.
- Références de version : seed.scions `scion/__init__.py`, `CHANGELOG.md`, test de version,
  `README.md` (sections par version), ligne « Versions » de `projection-miroir.md` ; lepton
  `SCION_MIN_VERSION` (`lepton/__init__.py`), `README.md`, `SCION_REF` d'`install-vscodium.sh` ;
  clone noyau `scripts/install-{macos,debian}.sh`, `README.md`, `README-PAQUET.md`,
  `doc/BUILDING.md`.
- git : 2.50.1 au Mac (`/usr/bin/git`, Apple Git-155, premier dans le PATH ;
  `/usr/local/git/bin/git` 2.18.0 aussi présent, plus loin dans le PATH) ; 2.47.3 sur la VM
  (R50-1, `rapports/env-50-debian.md` §1).
- Rootstocks du Mac qui ont des clones projetés (relevé du 2026-11-12) : `<ROOTSTOCK>` (8),
  `essais/env-13-vierge` (8), `essais/env-11/f429zi` (2), `essais/env-11/wl55jc1` (4),
  `essais/env-39-copie` (2, copie d'essai d'ENV-39).
- Skills `lepton-rootstock`, `lepton-oracle`, `lepton-cibles`.
- Branches `devenv/env-52` : `<SEED_SCIONS>`, lepton-tools ; clone noyau si `SCION_REF` change.

## Tâches

### 1. Audit (lecture seule) → PA-91
- Pour chacun des 8 clones de `<ROOTSTOCK>/depots/tiers/` : fichiers suivis, fichiers projetés
  (union des tables des clés qui partagent le clone, P-V2), taille de l'arbre extrait et de `.git`.
  Tableau au rapport `rapports/env-52-scion.md` §1.
- Chemin du code de la création d'un clone projeté à sa greffe, puis à `graft-update` (P-P5, P-P7)
  et au changement de version (P-V5).
- Règles touchées et comportement attendu de chacune avec une extraction partielle : P-V2, P-V4,
  P-V5, P-E1 (`git status --porcelain --untracked-files=no`), P-G3 (lien du clone hors de toute
  table), P-M4 ; résolution des motifs sur la liste git (`git ls-tree -r`), indépendante de
  l'arbre extrait.
- Mécanisme git : `git sparse-checkout` (mode cône ou non, `--stdin`), réapplication quand les
  lignes de projection changent, effet de `core.ignoreCase` sur les motifs (vrai dans les clones du
  Mac, relevé le 2026-11-12 ; à relever sur la VM) ; version minimale de git, comparée aux deux git du Mac et à celui de la VM. Essai sur un
  clone temporaire hors rootstock (`git clone` d'un miroir sous le répertoire de session), jamais
  sous `depots/tiers/`.
- Effets sur : lepton (`check`, `seed status`, `generate`, `seed lock`) ; extension (table clone
  tiers → trunk) ; `mirror-sync` ; hook `proteger-trunk.py` ; `controler-trunk.py`
  (`rapports/env-43-mac/controler-trunk.py`) ; skill `lepton-rootstock` (section Projection).
- **PA-91** : l'utilisateur valide, avant toute modification :
  - le texte de l'amendement de `projection-miroir.md` (règle nouvelle, retrait de la ligne
    `sparse-checkout` du §C, table §A.11) ;
  - extraction partielle pour tout clone projeté, ou sur option : <À CONFIRMER au PA-91> ;
  - ensemble extrait : liste exacte des fichiers projetés, ou répertoires de base des motifs :
    <À CONFIRMER au PA-91> ;
  - clones existants : convertis par la prochaine greffe, par une commande, ou laissés entiers ;
    commande de regreffe de `<ROOTSTOCK>` qui en découle : <À CONFIRMER au PA-91> ;
  - version minimale de git et conduite si elle manque : <À CONFIRMER au PA-91> ;
  - effets relevés sur lepton et l'extension : corrigés ici, ou dans une étape insérée :
    <À CONFIRMER au PA-91> ;
  - numéro de version : <À CONFIRMER au PA-91 : `0.6.3.0` ou `0.7.0.0`> ;
  - `SCION_MIN_VERSION` de lepton relevé ou non ; `SCION_REF` : <À CONFIRMER au PA-91> ;
  - contrôle des binaires : oracle après, ou arbre composé identique (raisonnement de
    `rapports/env-15-scion.md` §6, repris par ENV-29) : <À CONFIRMER au PA-91>.
- Aucune modification avant la réponse.

### 2. Spécification et implémentation (`<SEED_SCIONS>`, `devenv/env-52`)
- Premier commit : l'amendement validé de `projection-miroir.md`.
- Tests d'abord : un test par règle nouvelle ou modifiée (clone neuf, clone partagé, lignes de
  projection changées, changement de version, clone existant selon le PA-91, P-E1). Les tests
  existants restent verts.
- Commits séparés : un par comportement, puis un pour la version (`CHANGELOG.md`, test de version,
  `README.md`, ligne « Versions » de la spécification).

### 3. Essai sur une copie d'essai (skill `lepton-rootstock`)
- scion de la branche, sans pipx (qui changerait l'outil de tous les rootstocks) : venv
  `~/lepton-tools-dev/essais/env-52-venv` (`pip install <SEED_SCIONS>`, forme d'ENV-29,
  `rapports/env-29-scion.md` §3), ou `PYTHONPATH=<SEED_SCIONS> python3 -m scion.cli` (forme
  d'ENV-39).
- Copie d'essai `essais/env-52-copie` de `<ROOTSTOCK>`, sans `build/` ni `third_party/`
  (`rsync -a`, forme d'ENV-41 §3.3). Sur la copie, constater :
  - liste `chemin -> cible` identique à celle de `<ROOTSTOCK>`, casse comprise ;
  - contenu projeté identique au commit épinglé (`controler-trunk.py`) ;
  - fichiers extraits par clone conformes à l'ensemble du PA-91, tailles avant et après, relevés
    par des lectures admises par le hook (`git ls-files -t`, `find -type f`,
    `cat .git/info/sparse-checkout`) ;
  - `lepton check` et `generate` code 0.
- Rootstock neuf `essais/env-52-vierge` depuis la graine `original-tree` (forme
  d'`essais/env-13-vierge`) : mêmes contrôles, taille de chaque clone neuf.

### 4. Version, lepton, `<ROOTSTOCK>` → PA-92
- Tag annoté local de la version ; `pipx install --force "git+file://<SEED_SCIONS>@<version>"`.
- lepton-tools et clone noyau : références de version selon le PA-91 ; `pytest` vert.
- Skill `lepton-rootstock`, section Projection : effet de l'extraction partielle (commit dédié,
  ORCHESTRATION §5bis).
- `<ROOTSTOCK>`, sur accord de l'utilisateur : regreffe par la commande du PA-91. Si `SCION_REF`
  change, le clone noyau passe sur `devenv/env-52` et `graft-update` le refuse jusqu'à la fusion
  dans `master` (`rapports/env-29-scion.md` §4). Liste `chemin -> cible` identique (`cmp`), 0 lien
  cassé, 0 fichier régulier, `lepton check` code 0 ; tailles des clones au rapport.
- Binaires selon le PA-91 : oracle après `oracles/env-52-apres/` = `env-49-apres` (code 0), ou
  raisonnement de `rapports/env-15-scion.md` §6 consigné.
- Les autres rootstocks d'essai du Mac sont regreffés en ENV-53, pas ici.
- **PA-92** : rapport ; sort d'`essais/env-52-copie`, `essais/env-52-vierge` et du venv ;
  publication (PA-P) : tag et `master` de `<SEED_SCIONS>`, branches `devenv/env-52`, fusions. La
  validation Debian est faite en ENV-53.

## Critères de validation
- [ ] PA-91 et PA-92 tranchés et consignés.
- [ ] Amendement de `projection-miroir.md` commité avant le code ; aucun nom propre à Lepton
      ajouté : `git diff 0.6.2.0 -- scion tests | grep -ci '^+.*lepton'` → 0 (forme d'ENV-39 ; les
      2 lignes de métadonnées de `scion/__init__.py` sont antérieures, PA-2 Q7).
- [ ] Tests de scion verts, dont les nouveaux.
- [ ] Copie d'essai, rootstock neuf et `<ROOTSTOCK>` : liste `chemin -> cible` identique, contenu
      projeté identique, fichiers extraits conformes au PA-91.
- [ ] Références de version conformes au PA-91.
- [ ] `HORS-PLAN.md` : D11 marqué traité, avec renvoi au rapport.

## Pièges connus
- Le hook refuse toute écriture shell sous `depots/tiers/`, et `git sparse-checkout` (même `list`)
  n'est pas une lecture admise : aucune commande `sparse-checkout` à la main sur un clone de
  `<ROOTSTOCK>`, passer par scion seulement. Un refus signale une erreur de chemin.
- Un clone `blob:none` déjà extrait en entier garde dans `.git` les blobs reçus : le gain d'un clone
  converti se mesure sur l'arbre extrait ; le gain de téléchargement, sur un clone neuf (à vérifier
  à l'audit).
- Des lignes de projection qui changent peuvent viser un fichier hors de l'ensemble extrait :
  l'ensemble doit être recalculé avant la greffe, sinon lien cassé.
- Deux clés qui partagent un clone (P-V2) : l'ensemble extrait est l'union de leurs tables.
- lepton trouve scion par le PATH : pour `lepton check` et `generate` avec le scion du venv, placer
  le `bin/` du venv en tête du PATH de la commande.
- Point de retour après le tag : `pipx install --force "git+file://<SEED_SCIONS>@0.6.2.0"`.
- `graft-update` et `seed-update` sont soumis à PA-P ; la regreffe de `<ROOTSTOCK>` se fait sur
  accord de l'utilisateur (ENV-29 §4). Relever d'abord la branche de chaque clone (§2bis).
- La casse : le Mac ne la distingue pas (`core.ignoreCase` vrai) ; elle se prouve sur la VM
  (ENV-53).

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, branches, §Versions (scion, lepton), §Emplacements (clones projetés),
décisions PA-91 et PA-92, journal. `HORS-PLAN.md` : D11. Passation `handoff/env-52.md`.
