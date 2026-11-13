# ENV-56 — scion : répertoires laissés par un clonage en échec (D14)

Branches `devenv/env-56` : seed.scions (depuis `master` 6416c33, tag 0.6.3.0) et lepton-tools
(depuis `main` 298de7a). État de départ : scion 0.6.3.0 et lepton 0.1.0 (pipx), git 2.50.1
(`/usr/bin/git`), Python 3.11.5. 282 tests de scion. Noyau `master` 58e421e.

Scripts et relevés : `env-56-scion/`.
- `essai.sh` : cas e01 à e06 sur le rootstock d'essai. Il reprend `env-51-messages/releve.sh` et
  `env-55-url-file/etat.sh`.
- `fixture.py` : cas f01 à f12b sur des rootstocks temporaires.
- Relevés « avant » : `avant/` et `fixture-avant/`.

Dans les relevés, les chemins sont remplacés : `<C>` pour le rootstock d'essai, `<A>` pour le dépôt
absent, `<B>` pour la base de la fixture, `<HOME>` pour le répertoire personnel.

## 1. Audit (scion 0.6.3.0)

### 1.1 Répertoires créés avant une opération qui peut échouer

| # | Lieu | Création, puis opération | Appelants | Reste après l'échec | Parent préexistant | Étagère créée par l'appel |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | `scion/gitops.py:70`, `clone` | `dest.parent.mkdir(parents=True, exist_ok=True)`, puis `git clone` (ou `git clone -b <v> --single-branch`), puis `git checkout <v>` | `graft._fetch`, clés ordinaires (`seed-add`, `seed-clone`, `seed-update`, `graft-update`, par `sync`) ; `cli._clone_seed`, graine distante de `seed-add` | Échec du `git clone` : chaque ancêtre créé, de l'étagère au greffon, vide (f01, f02, f05, f10, e01 à e03, e06). Échec du `checkout` après un clone réussi : le clone entier (f06, §1.5) | gardé, car jamais retiré (f03, f04, e04, e05) | oui : `depots/own` (f01, f05), `depots/essai` (e03) ; graine : `depots/<nom>` (f10, e06) |
| R2 | `scion/gitops.py:80`, `clone_partial` | même `mkdir`, puis `git clone --filter=blob:none --no-checkout` ; ensuite, dans `_fetch` : `sparse_set`, `_pinned`, `checkout_detached` | `graft._fetch`, clés projetées distantes | Échec du `git clone` : `depots/tiers/<clé>`, et `depots/tiers` s'il est créé (f07, f09b). Version absente : clone gardé exprès, avec le message « clone laissé en place » (f08, P-V1) | gardé (f09c) | oui : `depots/tiers` (f07) |
| R3 | `scion/mirror.py:271`, `sync_one` | `work.parent.mkdir(parents=True, exist_ok=True)`, puis `git clone --mirror`, puis `git fetch` | `mirror-sync`, `--dry-run` compris | Échec du `git clone --mirror` : toute la chaîne `depots/.mirrors/<hôte>/<chemin de l'URL>` sans le dernier élément, soit 10 répertoires en f11. Échec du `fetch` : dépôt de travail gardé exprès (f12a, M-C6) | gardé (f12b) | oui : `depots/.mirrors` (f11) |

Autres `mkdir` de scion, hors D14 :
- `rootstock.install` (`rootstock-install`) refuse un répertoire non vide et ne clone rien.
- `graft._mkdir` (l. 576) relève déjà les ancêtres absents, et `_rollback` les retire par `rmdir`
  si la greffe échoue.
- `_put_back` et `_restore` sont des restaurations.
- `grafted_list.parent` et `trunk.mkdir` sont des répertoires du rootstock lui-même.

`git clone` n'est lancé que par R1, R2 et R3 (`grep '"clone"' scion/*.py`).

### 1.2 Comportement de git 2.50.1 sur un clonage en échec

Essai dans un répertoire de session, hors dépôts.

| Cas | Code | Reste |
| --- | --- | --- |
| Destination absente, URL absente | 128 | destination retirée par git ; parent gardé (vide) |
| Destination présente et vide, URL absente | 128 | destination gardée, vide (git ne retire pas un répertoire qu'il n'a pas créé) |
| `git clone` réussi, `git checkout <absente>` | 1 | clone entier |
| `-b <absente> --single-branch` | 128 | destination retirée ; parent gardé |
| `--mirror`, URL absente | 128 | destination retirée ; parent gardé |
| `--filter=blob:none --no-checkout`, URL absente | 128 | destination retirée ; parent gardé |
| Destination non vide | 128 | refus ; destination intacte |

Le résidu de D14 vient donc du seul `mkdir` de scion : git retire toujours la destination qu'il a
créée, jamais ce qui est au-dessus.

### 1.3 Essais sur `essais/env-56-essai` (`avant/`)

Rootstock d'essai : copie d'`essais/env-11/qemu` par `rsync -a --exclude /build/`, 3059 liens, aucun
lien cassé, aucun fichier régulier, noyau 58e421e. Dépôt absent :
`file://localhost/…/essais/env-56-absent.git`, jamais créé.

| Cas | Commande | Code | Après l'échec |
| --- | --- | --- | --- |
| e01 | `lepton seed add absent <URL> --type bibliotheque --no-cmake` (étagère `lepton` existante) | 2 | résidu `depots/lepton/library-absent` ; graine et trunk restaurés (« ajout de lepton@library-absent annulé ») |
| e02 | `scion seed-scion-add`, `seed-clone` (code 2), `seed-scion-remove`, lancés à la main, `lepton@library-absent` | 0, 2, 0 | même résidu |
| e03 | même suite, étagère nouvelle `essai@absent` | 0, 2, 0 | résidus `depots/essai` et `depots/essai/absent` |
| e04 | e01, avec `depots/lepton/library-absent/autre/temoin` préparé (autre version) | 2 | préexistant gardé, aucun résidu |
| e05 | e01, avec `depots/lepton/library-absent` préparé vide (résidu d'un échec antérieur) | 2 | préexistant gardé |
| e06 | `scion seed-add <URL>` (graine distante absente) | 2 | résidu `depots/env-56-absent` |

Après chaque cas, et après le retrait des résidus par `rmdir` : liens, liens cassés, fichiers
réguliers, graine, liste greffée et `depots/` sont égaux au départ (`*.etat`).

### 1.4 Essais sur des rootstocks temporaires (`fixture-avant/`)

Chaque rootstock est bâti comme `ProjectionCase` et `MirrorCase` dans les tests de scion, sous
`essais/env-56-fixture/avant/<cas>/`. Il n'y a aucune URL réseau, et `mirror-sync` n'est lancé
qu'avec `--dry-run`.

| Cas | Situation | Code | Créés | Plus haut créé | Résidu vide | Clone gardé |
| --- | --- | --- | --- | --- | --- | --- |
| f01 | ordinaire, étagère nouvelle | 2 | 2 | `depots/own` | `depots/own/plain` | — |
| f02 | ordinaire, étagère existante | 2 | 1 | `depots/own/plain` | `depots/own/plain` | — |
| f03 | ordinaire, parent qui porte une autre version | 2 | 0 | — | — | — |
| f04 | ordinaire, parent préexistant vide | 2 | 0 | — | — | — |
| f05 | ordinaire, `--single-branch`, version absente d'un dépôt présent | 2 | 2 | `depots/own` | `depots/own/plain` | — |
| f06 | voisin : ordinaire, version absente, sans `--single-branch` | 2 | 4 | `depots/own` | — | `depots/own/plain/nope` |
| f07 | projetée, étagère `tiers` nouvelle | 2 | 2 | `depots/tiers` | `depots/tiers/hal` | — |
| f08 | voisin : projetée, version absente | 1 | 3 | `depots/tiers` | — | `depots/tiers/hal/v9.9` |
| f09a | projetée, ajout réussi (préparation) | 0 | 3 | `depots/tiers` | — | `depots/tiers/hal/v1.0` |
| f09b | projetée, étagère `tiers` existante | 2 | 1 | `depots/tiers/hal2` | `depots/tiers/hal2` | — |
| f09c | projetée, parent qui porte une autre version (v1.0 cloné, v2.0 absent) | 2 | 0 | — | — | — |
| f10 | graine distante absente | 2 | 1 | `depots/absent2` | `depots/absent2` | — |
| f11 | miroir absent, aucun dépôt de travail | 1 | 10 | `depots/.mirrors` | `…/repos/miroirs` | — |
| f12a | voisin : miroir présent, amont absent | 1 | 11 | `depots/.mirrors` | — | dépôt de travail `…/present.git` |
| f12b | miroir absent, ancêtres déjà créés par un autre miroir | 1 | 0 | — | — | — |

Messages de scion :
- clonage en échec : `erreur : échec de « git clone … » (code 128) : and the repository exists.` ;
- miroir en échec : `miroir … : miroir inaccessible : échec de « git clone --quiet --mirror … »` ;
- aucun message ne nomme le répertoire laissé.

### 1.5 Cas où un clone réussi est gardé exprès (hors D14)

- **f08**, clé projetée, version introuvable : clone gardé, avec un message qui le dit (« clone
  laissé en place »). Spécification : P-V1 (« Le clone reste alors en place, comme le clone d'une
  version introuvable en 0.5.4.0 »).
- **f06**, clé ordinaire, version absente, sans `--single-branch` : le `git clone` réussit, le
  `checkout` échoue (code 2), et le clone reste sur `master`. Le message ne le dit pas. Au passage
  suivant, le contrôle de version de 0.5.4.0 arrête la commande : `seed-add` sort avec le code 1,
  « 1 clone(s) à remettre à leur version déclarée … version déclarée « nope » introuvable dans le
  clone ». Le clone ne produit donc jamais de greffe fausse.
- **f12a**, dépôt de travail d'un miroir dont l'amont est inaccessible : gardé pour la passe
  suivante. Spécification : M-C6 (« Le dépôt de travail local est créé ou rafraîchi »).

Dans ces trois cas, le parent contient un clone : il n'est pas vide. Un retrait limité aux
répertoires vides (`rmdir`) les laisse donc inchangés.

### 1.6 Spécification et `README.md` de seed.scions

Aucune règle ne fixe le sort des répertoires créés pour un clonage en échec.
- `doc/projection-miroir.md` : P-V1 et M-C6 (§1.5) traitent des clones réussis ; M-D5 traite du
  message (suggestion de `mirror-sync`) ; M-C5 dit qu'un miroir inaccessible est signalé.
- `README.md`, §Utilisation : « Si la regreffe de `graft` ou de `graft-update` échoue (conflit,
  git), le trunk est rétabli tel qu'il était ». Rien n'y concerne `depots/`.

### 1.7 Effets sur lepton

- `_undo_add` (`lepton/seed.py:654`) lance `seed-scion-remove`, puis écrit « ajout de … annulé
  (graine et trunk restaurés) ». Sa docstring dit « le clone éventuel est conservé » : c'est le cas
  d'un clone réussi suivi d'une greffe en échec, et cela reste vrai. Aucun code de lepton ne
  dépend du résidu.
- `tests/test_projection.py:362`, `test_echec_de_scion_sans_double_affichage`, compte les lignes
  du stderr de scion qui contiennent `erreur :`. Un nouveau message de scion ne doit pas contenir
  `erreur :`. Le contrôle se fait par le `pytest` de lepton-tools avec le nouveau scion.
- Références de version :
  - lepton-tools : `SCION_REF` (`scripts/install-vscodium.sh:56`), `README.md:11`, note de
    `lepton/__init__.py:10` ;
  - clone noyau : `scripts/install-{macos,debian}.sh`, `README.md:3`, `README-PAQUET.md:36`,
    `doc/BUILDING.md:48` ;
  - seed.scions : `scion/__init__.py`, `tests/test_cli.py:17`, `CHANGELOG.md`, `README.md`.
- ENV-57 (C1) installe sur la VM le scion désigné par `SCION_REF`. Si `SCION_REF` ne change pas,
  la VM garde 0.6.3.0, donc le défaut.

### 1.8 Propositions pour le PA-99 (non validées)

- **Portée.** Avant le `mkdir`, scion relève le premier ancêtre absent (motif de `graft._mkdir`).
  Si l'opération échoue, il retire les répertoires qu'il a créés, du plus profond au plus haut,
  par `rmdir` seul : un répertoire non vide reste. Un répertoire préexistant, vide ou non, n'est
  jamais touché (e04, e05, f03, f04, f09c, f12b inchangés). Conséquence : un résidu laissé par
  0.6.3.0 (forme d'e05) reste en place, car scion ne nettoie pas ce qu'il n'a pas créé dans l'appel.
- **Cas couverts.** R1 (clés ordinaires et graine distante), R2 (clés projetées), R3 (dépôt de
  travail d'un miroir). Les clones gardés exprès (§1.5) ne changent pas.
- **Message.** Rien de plus au niveau normal, une ligne de journal sous `-v`. L'état final est
  celui du départ, et le message d'erreur de git reste seul. La sortie relayée par lepton ne change
  donc pas.
- **Documentation.** Une phrase dans le `README.md` de seed.scions, §Utilisation, et une entrée
  « Corrections » au `CHANGELOG.md`. Pas de règle dans `doc/projection-miroir.md` : le correctif ne
  concerne pas seulement la projection et le miroir.
- **Version.** 0.6.3.1 : correction seule, formats et commandes inchangés (précédent : 0.5.1.1).
  0.6.4.0 suivrait le précédent de 0.6.2.0, correctif qui ajoutait une règle de spécification.
- **`SCION_MIN_VERSION`** inchangé, (0, 6, 2, 0) : lepton ne dépend pas du correctif.
  **`SCION_REF`** porté à la nouvelle version, dans lepton-tools (`install-vscodium.sh`,
  `README.md`) et dans le clone noyau (`install-{macos,debian}.sh`, `README.md`,
  `README-PAQUET.md`, `doc/BUILDING.md`), sur une branche `devenv/env-56`. ENV-57 l'installera
  ainsi sur la VM. Précédent : ENV-52 (PA-91).

## 2. Décisions du PA-99 (2026-11-13, utilisateur)

Les propositions du §1.8 sont retenues :
- **Portée.** Seuls les répertoires vides créés par l'appel sont retirés, par `rmdir`, du plus profond
  au plus haut. Un répertoire préexistant ou non vide n'est jamais touché.
- **Cas couverts.** R1, R2 et R3. Les clones gardés exprès (f06, f08, f12a) ne changent pas. f06, un
  clone gardé sans que le message le dise, est noté au hors-plan (D18).
- **Message.** Une ligne de journal sous `-v`, rien au niveau normal.
- **Documentation.** `README.md` (§Utilisation) et `CHANGELOG.md` de seed.scions ;
  `doc/projection-miroir.md` reste inchangé.
- **Version.** 0.6.3.1.
- **Références.** `SCION_MIN_VERSION` reste (0, 6, 2, 0). `SCION_REF` passe à 0.6.3.1 dans
  lepton-tools et dans le clone noyau.

## 3. Implémentation (seed.scions, `devenv/env-56`)

| Commit | Contenu |
| --- | --- |
| 95d55eb | Tests d'abord, `tests/test_failed_clone.py` : 16 tests. Sur 0.6.3.0, 8 échouent : clé ordinaire (étagère nouvelle, étagère existante, `--single-branch` sur une version absente), graine distante, clé projetée (étagère nouvelle, étagère existante), miroir absent (`--dry-run`), ligne de journal sous `-v`. Les 8 autres réussissent : répertoires préexistants et clones gardés exprès (`env-56-scion/tests-avant-correction.txt`) |
| 54fc27b | `gitops.clone_parents(dest)`, gestionnaire de contexte : relève les ancêtres absents de `dest`, crée le parent, et sur exception retire par `rmdir` les répertoires créés, du plus profond au plus haut ; arrêt au premier répertoire non vide. Ligne `log.debug` : « clonage en échec : répertoire(s) créé(s) pour <dest> retiré(s) : … ». Employé par `clone` et `clone_partial` : R1 (dont `cli._clone_seed`) et R2 |
| b8767dc | `mirror.sync_one` : `git clone --mirror` dans `gitops.clone_parents(work)` (R3) |
| c51ee1a | 0.6.3.1 : `scion/__init__.py`, `tests/test_cli.py`, `CHANGELOG.md` (« Corrections »), `README.md` (§Utilisation) |

Un clone réussi dont le `checkout` échoue (f06) laisse un parent non vide : `rmdir` échoue, et rien
n'est retiré. Les étapes qui suivent un clone réussi dans `_fetch` (`sparse_set`, `_pinned`,
`checkout_detached`) sont hors du gestionnaire : le clone reste en place (P-V1).

Contrôles :
- tests de scion : 298, tous verts, plus 1 sauté (`test_network`, désactivé sans
  `SCION_TEST_NETWORK=1`, comme sur `master`) ;
- NF-2 : `git diff 0.6.3.0 -- scion tests | grep -ci '^+.*lepton'` donne 0 ;
- `git diff --stat 0.6.3.0` : 7 fichiers, +272 −14.

## 4. Essais avec la branche (venv `essais/env-56-venv`, scion 0.6.3.1)

Le venv est installé par `pip install "git+file://<SEED_SCIONS>@devenv/env-56"`, et son `bin/` est
placé en tête du PATH pour lepton.

- **Rootstock d'essai, e01 à e06** (`apres/`) :
  - aucun résidu, et les préexistants sont gardés (e04, e05) ;
  - `diff -r avant apres` ne diffère que par les lignes `résidu` et `rmdir` des `*.etat` et par
    `scion.txt` : `.out`, `.err` et `.code` sont identiques ;
  - graine, trunk et liens sont égaux au départ.
- **Ligne sous `-v`** (`apres/e07-verbeux.err`, `scion seed-add -v <URL absente>`) :
  - `clonage en échec : répertoire(s) créé(s) pour <C>/depots/env-56-absent/master retiré(s) :
    <C>/depots/env-56-absent`, entre la commande git et l'erreur ;
  - aucun résidu.
- **Fixture, f01 à f12b** (`fixture-apres/`) :
  - chaque cas de D14 (f01, f02, f05, f07, f09b, f10, f11) crée 0 répertoire durable ;
  - préexistants gardés (f03, f04, f09c, f12b) et clones gardés exprès (f06, f08, f12a) : comme
    avant ;
  - `.cmd`, `.out`, `.err` et `.code` sont identiques à l'avant pour les 15 cas ;
  - les `.depots` ne diffèrent que pour f01, f02, f05, f07, f09b, f10, f11, et pour f09c, qui
    hérite du rootstock de f09b, sans le résidu `depots/tiers/hal2`.
- **`seed add` réussi, puis `seed remove`** (forme des relevés 01 et 02 d'ENV-53, `succes.sh`) :
  - `lepton seed add stm32f7xx --type famille https://github.com/lepton-distribution/lepton-famille-stm32f7xx.git@master --no-cmake`,
    puis `lepton seed remove stm32f7xx --no-cmake` ;
  - deux copies neuves d'`essais/env-11/qemu`, `essais/env-56-succes-0630` (scion 0.6.3.0) et
    `essais/env-56-succes-0631` (branche). `seed remove` garde les clones tiers d'un porteur
    (P-P6) : une seconde passe sur la même copie ne reclonerait pas ;
  - résultat, dans les deux cas : 3059 → 3271 → 3059 liens, 0 cassé, graine et liste greffée
    égales au départ ;
  - `diff -r succes-0630 succes-0631` ne diffère que par `scion.txt`. Sont donc identiques : les
    messages, les codes, les liens, les clones tiers (tête, `sparse-checkout`, fichiers extraits,
    tailles) et la tête du clone de la famille.

## 5. Version, lepton, noyau

- seed.scions :
  - tag annoté local `0.6.3.1` sur c51ee1a ;
  - `pipx install --force "git+file://<SEED_SCIONS>@0.6.3.1"` : `scion version: 0.6.3.1` ;
  - les 10 modules installés sont identiques au tag (`cmp`).
- lepton-tools, 01d4991 :
  - `SCION_REF="0.6.3.1"` (`scripts/install-vscodium.sh`), `README.md`, note dans
    `lepton/__init__.py` ;
  - `SCION_MIN_VERSION` inchangé, (0, 6, 2, 0) ;
  - `lepton --version` donne `scion 0.6.3.1 (requis ≥ 0.6.2.0)`.
- `pytest` de lepton-tools (venv `~/lepton-tools-dev/venv-lepton-tools`, scion 0.6.3.1 du PATH) :
  453 verts, `test_echec_de_scion_sans_double_affichage` compris.
- Clone noyau, branche `devenv/env-56` (depuis `master` 58e421e), 79354a0 :
  - `SCION_REF` 0.6.3.1 dans `scripts/install-{macos,debian}.sh`, `README.md`, `README-PAQUET.md`,
    `doc/BUILDING.md` ;
  - ces fichiers sont hors de `scion/` : rien n'est greffé, et le trunk ne change pas ;
  - contrôles de `<ROOTSTOCK>` : 0 lien cassé ; 7 fichiers réguliers, tous des `.DS_Store` du
    Finder datés du 12 novembre et tolérés (`.scion.trunk.tolerated`), antérieurs à la session.
- lepton n'est pas réinstallé par pipx : son code ne change pas, seul un commentaire change.

## 6. Binaires

Pas d'oracle :
- le correctif ne touche que les chemins d'échec d'un clonage ;
- `<ROOTSTOCK>` n'est pas regreffé ;
- le seul essai de greffe réussie (§4) donne, avec 0.6.3.0 et avec 0.6.3.1, des liens et des clones
  identiques ;
- l'arbre composé ne change donc pas, et aucune reconstruction n'est nécessaire (forme
  d'`env-15-scion.md` §6).
