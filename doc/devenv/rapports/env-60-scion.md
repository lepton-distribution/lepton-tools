# ENV-60 — scion : clone gardé après un checkout en échec (D18)

Branches `devenv/env-60` : seed.scions (depuis `master` d650414, tag 0.6.3.1) et lepton-tools
(depuis `main` 67dbb04). État de départ : scion 0.6.3.1 et lepton 0.1.0 (pipx), git 2.50.1
(`/usr/bin/git`), Python 3.11.5. Tests de scion : 298, verts, 1 sauté (`test_network`). pytest de
lepton-tools : 508. Noyau `master` ed2a41f.

Scripts et relevés : `env-60-scion/`.
- `fixture.py` : cas k01 à k19 et préparation de u01, sur des rootstocks temporaires
  (`essais/env-60-fixture/avant/`), forme d'`env-56-scion/fixture.py`. Chaque cas donne `.cmd`,
  `.out`, `.err`, `.code`, `.depots`, plus l'état des clones et du trunk (`etat.py` : `.clones`,
  `.trunk`). Tableau : `fixture-avant/fixture.tsv`.
- `etat.py` : état des clones (branche, références qui désignent `HEAD`, fichiers extraits, état
  git) et du trunk (liste greffée, liens).
- u01 (`graft-update`) : préparé par `fixture.py`, lancé directement par la session (PA-P au plan,
  invite `ask`), relevé par `etat.py` (`u01c`, `u01d`).
- `essai.sh` : cas lepton l01 à l03 sur `essais/env-60-essai` (copie d'`essais/env-11/qemu` par
  `rsync -a`, sans `build/`), dépôt `essais/env-60-depot` (greffon `bibliotheque` `env60lib`,
  `lepton scion new env60lib --type bibliotheque --repo <P> --no-seed --no-cmake`, un commit
  c059196 sur `master`) ; l04 (retrait de l03) lancé par la session. Relevés : `avant/`.
- `fixture56-avant/` : `env-56-scion/fixture.py` rejoué tel quel avec 0.6.3.1.

Dans les relevés : `<B>` base de la fixture, `<C>` rootstock d'essai, `<P>` dépôt `env60lib`,
`<HOME>` répertoire personnel, `<SHA>` commit de `master` du dépôt `plain`.

## 1. Audit (scion 0.6.3.1)

### 1.1 D18 : clé ordinaire, version absente (k01 à k03, u01)

| Cas | Commande | Code | Message (dernière ligne) | Clone |
| --- | --- | --- | --- | --- |
| k01 (= f06) | `seed-add <graine>`, clé `own/plain` `nope` | 2 | `erreur : échec de « git checkout nope » (code 1) : error: pathspec 'nope' did not match any file(s) known to git` | `depots/own/plain/nope` gardé, branche `master`, `HEAD` = `origin/master`, `scion/f.txt` extrait, propre |
| k02 | k01 relancé | 1 | `1 clone(s) à remettre à leur version déclarée … version déclarée « nope » introuvable dans le clone` | inchangé |
| k03 | `graft` | 1 | liste greffée vide | inchangé, trunk vide |
| u01c | `graft-update` qui ajoute `own/plain2` `nope` à une graine greffée | 2 | message de k01, puis `trunk rétabli dans son état antérieur (1 lien(s))` | `depots/own/plain2/nope` gardé sur `master` ; trunk = départ |
| u01d | u01c relancé | 1 | message de k02, « trunk et clones inchangés » | inchangé ; trunk = départ |

Le fichier d'étape est confirmé pour ces chemins : le message ne dit pas que le clone reste, ni
sur quelle branche ; le passage suivant par `seed-add` ou `graft-update` refuse.

u01c a été lancé deux fois sur des bases successives. Le tout premier lancement portait un préfixe
`cd … && LC_ALL=C` : c'est un écart à la forme de l'ORCHESTRATION §2bis, qui a pu le faire juger
par le classifieur plutôt que par la règle `ask`. Il ne visait que le rootstock temporaire. Les
deux bases ont été supprimées et refaites. Les relevés versionnés viennent de la dernière base,
lancée dans la forme exacte (commande seule, redirections et `echo`). Ils sont identiques au
premier lancement, chemins normalisés.

### 1.2 Greffe fausse après un checkout en échec (k18, l01 à l04)

`seed-clone` (`graft.sync`) ne contrôle pas les clones existants : seuls `seed-add`,
`seed-update` et `graft-update` le font (`update_sources`, depuis 0.5.4.0). Or lepton ajoute un
greffon par `seed-scion-add`, `seed-clone` puis `graft --scion` (`lepton/seed.py:636`).
`seed replace` (`_attach`, l. 744) et la greffe du projet (`graft_project`, l. 238) passent aussi
par `seed-clone`.

| Cas | Commande | Code | Effet |
| --- | --- | --- | --- |
| k18 | comme k01 | 2 | clone gardé sur `master` |
| k18b | `seed-clone --seed <graine>` | **0** | clé écrite dans la liste greffée, version `nope` |
| k18c | `graft` | **0** | `trunk/f.txt -> …/own/plain/nope/scion/f.txt` : contenu de `master` greffé sous `nope` |
| l02 | `lepton seed add env60lib file://localhost<P>@nope --type bibliotheque --no-cmake` | 2 | `scion: … déclaré … (version nope)`, `scion: … retiré …`, `lepton: attention: ajout de lepton@library-env60lib annulé (graine et trunk restaurés)`, puis `lepton: erreur: échec de « scion seed-clone … » (code 2) :` et le message de k01. Graine, trunk et liste greffée = départ ; clone `depots/lepton/library-env60lib/nope` gardé sur `master` (non dit) |
| l03 | l02 relancé | **0** | `env60lib ajouté (lepton@library-env60lib, nope, …)`, 3 liens vers `…/library-env60lib/nope/…` : greffe de `master` sous `nope` |
| l04 | `lepton seed remove env60lib --no-cmake --purge` | 0 | clone supprimé ; liens, graine, liste greffée et `depots/` = départ |

« Il n'y a jamais de greffe fausse » (fichier d'étape, `HORS-PLAN.md` D18) ne vaut donc que pour
`seed-add`, `seed-update` et `graft-update`. Par lepton, la seconde tentative réussit et greffe
la branche de l'origine sous la version déclarée. Rien ne le signale ensuite, sauf le prochain
`graft-update` (refus, forme k02).

### 1.3 Graine distante (k04 à k07)

| Cas | Commande | Code | Effet |
| --- | --- | --- | --- |
| k04 | `seed-add --version nope file://localhost<B>/repos/graine` | 2 | message de k01 ; clone `depots/graine/nope` gardé sur `master` |
| k05 | k04 relancé | **0** | `_clone_seed` réutilise le clone (`cli.py:108`), sans contrôle de sa version ; la graine lue est celle de `master` : `own/plain` `master` cloné, liste greffée écrite (graine `depots/graine/nope/scion/.scion`) |
| k06 | `graft` | 0 | 1 lien : contenu de la graine de `master` greffé |
| k07 | k04 avec `--single-branch` | 2 | `git clone -b nope --single-branch` refusé ; aucun répertoire (D14) |

Le contrôle de 0.5.4.0 ne porte que sur les clones nommés par les graines (`clone_updates`).
`seed_updates` avance la graine par avance rapide sans comparer sa branche à la version
demandée. Une graine restée sur `master` n'est donc jamais signalée, même par `graft-update`.

### 1.4 Autres causes : la version n'est pas une branche ni un tag de l'origine (k08 à k17, k19)

`git checkout <version>`, sans `--`, accepte un chemin. C'est la seconde cause trouvée, plus
grave que D18 parce que silencieuse :

| Cas | Situation | Code | Effet |
| --- | --- | --- | --- |
| k08 | clé ordinaire, version `scion`, aucune ref de ce nom (répertoire `scion/` présent dans tout greffon) | **0** | `git checkout scion` restaure des fichiers (« Updated 0 paths from the index ») ; clone sur `master` ; liste greffée `own plain scion` |
| k09 | `graft` | 0 | contenu de `master` greffé sous `scion` |
| k10 | k08 relancé | 1 | « version déclarée « scion » introuvable dans le clone » |
| k17 | graine distante, version `scion` | **0** | graine de `master` lue ; `graft` (k17b) la greffe ; jamais signalé |
| k11 | version présente : branche distante `doc` et répertoire `doc/` | 2 | `fatal: 'doc' could be both a local file and a tracking branch` (code 128) ; clone gardé sur `master` |
| k12 | k11 relancé | 1 | `branche « master », version déclarée « doc » ; git -C … switch doc` |
| k13 | k11 avec `--single-branch` | 0 | branche `doc` |
| k14 | tag `tests` et répertoire `tests/` | 0 | `HEAD` détaché sur le tag (le tag l'emporte) |
| k15 | origine vide, version `master` | 2 | `git clone` réussit (dépôt vide), checkout en échec ; clone vide gardé |
| k16 | k15 relancé | 1 | « introuvable » |
| k19 | clé ordinaire, version = commit complet | 0 | `HEAD` détaché sur le commit |
| k19b | k19 relancé | 1 | « introuvable » : `_check_clone` ne connaît que branche et tag |

Causes recherchées sans cas trouvé sur un clone neuf :
- fichiers non suivis : impossibles, l'arbre de travail est exactement celui de l'origine ;
- droits : les fichiers sont créés par l'utilisateur qui lance scion ;
- chemin refusé par l'hôte (`.git`, `core.protectNTFS`, `core.protectHFS`) : `git checkout`
  échouerait (« invalid path »). Non essayé : un tel arbre est refusé par git à la création et
  par le `fsck` des hébergeurs ;
- casse (APFS insensible à la casse) : collision signalée par git, mais pas d'échec.

### 1.5 Textes qui fixent le sort du clone

| Texte | Contenu | Introduit |
| --- | --- | --- |
| `scion/gitops.py:94`, `clone()` | `git clone`, puis `git checkout <version>` | réécriture d88c714 (avant 0.5.0.1) ; checkout de `master` compris depuis 0.5.1.1 (255964b) |
| docstring de `clone()` (l. 102-103) | « a clone whose checkout fails is kept » | 0.6.3.1 (54fc27b) |
| `CHANGELOG.md` 0.6.3.1 (l. 18-19) | « Un clone réussi reste en place comme avant : version introuvable (P-V1), checkout en échec, … » | 0.6.3.1 (c51ee1a) |
| `README.md` (l. 361-365) | « … de même qu'un clone réussi dont la version est introuvable » | 0.6.3.1 (c51ee1a) |
| `doc/projection-miroir.md`, P-V1 (l. 143) | clé projetée : « Le clone reste alors en place, comme le clone d'une version introuvable en 0.5.4.0 » | 0.6.0.0 (f5c71ce) |
| `tests/test_failed_clone.py:99` | `test_clone_whose_checkout_fails_is_kept` | 0.6.3.1 (95d55eb) |

Le clone gardé n'a jamais été voulu pour lui-même : c'est l'effet de `git clone` suivi d'un
`git checkout` séparé. Il a été décrit en 0.6.3.1, quand D14 a borné le retrait aux répertoires
vides. P-V1 (clé projetée) en est indépendant : `clone_partial` puis `_pinned` gardent le clone et
le disent.

### 1.6 Comportement de git 2.50.1 avec `git clone -b <version>`, sans `--single-branch`

Sonde dans le scratchpad, sur le dépôt des cas k08, k11, k14, k15 et k19 :

| Version | `git clone -b` | Effet |
| --- | --- | --- |
| absente (`nope`) | 128, `fatal: Remote branch nope not found in upstream origin` | destination retirée par git |
| chemin seul (`scion`) | 128, même message | destination retirée |
| branche distante homonyme d'un chemin (`doc`) | 0 | branche `doc`, amont `origin/doc`, toutes les branches distantes reçues |
| tag homonyme d'un chemin (`tests`) | 0 | `HEAD` détaché sur le tag |
| `master` | 0 | branche `master`, amont `origin/master` |
| commit complet | 128, `Remote branch <sha> not found` | destination retirée |
| origine vide, `master` | 128 | destination retirée |

Une branche s'obtient comme après `git checkout` (branche locale qui suit l'origine), et un tag
aussi (`HEAD` détaché). L'option `--single-branch` n'est pas en jeu : toutes les branches restent
disponibles. Les parents créés pour le clone sont retirés par `clone_parents` (D14), comme pour
f05 et k07.

### 1.7 Effets sur lepton

- `_undo_add` (`lepton/seed.py:660`) : « le clone éventuel est conservé ». C'est vrai du clone
  réussi suivi d'une greffe en échec. Le message « ajout … annulé (graine et trunk restaurés) »
  ne parle pas du clone : il reste vrai.
- `tests/test_projection.py:362` compte les lignes `erreur :` de scion (1 attendue). Les messages
  de `git clone -b` en échec en donnent une seule (forme f05, k07).
- Les clones déjà laissés sur disque par 0.6.3.1 ou une version antérieure restent réutilisés
  sans contrôle par `seed-clone` et par `_clone_seed` (§1.2, §1.3). Corriger le clonage n'y
  change rien.
- Références de version : comme en ENV-56 (`env-56-scion.md` §1.7). lepton-tools : `SCION_REF`
  (`scripts/install-vscodium.sh:56`), `README.md:11`, note de `lepton/__init__.py`. Clone
  noyau : `scripts/install-{macos,debian}.sh`, `README.md`, `README-PAQUET.md`,
  `doc/BUILDING.md`. seed.scions : `scion/__init__.py`, `tests/test_cli.py`, `CHANGELOG.md`,
  `README.md`.

### 1.8 Rejeu d'ENV-56 (`fixture56-avant/`)

`env-56-scion/fixture.py`, rejoué tel quel avec 0.6.3.1, est identique à
`env-56-scion/fixture-apres/` (15 cas, `.cmd`, `.out`, `.err`, `.code`, `.depots`). Seule
exception : le nom de la base dans le chemin d'un dépôt de travail de miroir (f12a, f12b,
`env-56-fixture` → `env-60-fixture`). C'est la base de comparaison de l'essai.

### 1.9 Propositions pour le PA-107 (non validées)

1. **Correction** : dans `gitops.clone`, sans `single_branch`, remplacer `git clone` puis
   `git checkout <version>` par `git clone -b <version> <url> <dest>`. C'est l'option « contrôle
   de la version avant le checkout, sans clone gardé » : git refuse la version avant de créer
   l'arbre de travail, et retire la destination. Règle d'un coup :
   - D18 (k01, k04, k15, u01) : aucun clone gardé ;
   - les greffes fausses de §1.2 et §1.3 : chaque tentative reclone et échoue de la même façon ;
   - la version qui n'est qu'un chemin (k08, k17), refusée au lieu d'être greffée en silence ;
   - la branche homonyme d'un chemin (k11), clonée au lieu d'échouer.
   Les options « message seul » et « retrait du clone après un checkout en échec » laissent la
   version-chemin réussir en silence (k08, k17). Le message seul laisse aussi les greffes fausses
   de §1.2 et §1.3.
2. **Cas couverts** : clé ordinaire (`_fetch`) et graine distante (`_clone_seed`), tous deux par
   `gitops.clone`. Sans changement : `--single-branch`, déjà sous cette forme ; clé projetée
   (P-V1).
3. **Version commit complet d'une clé ordinaire** (k19) : refusée dès le premier passage, au lieu
   d'être acceptée puis refusée au suivant. Changement de comportement, aligné sur le contrôle de
   0.5.4.0. À écrire dans `CHANGELOG.md`.
4. **Message** : celui de git, sans texte ajouté, comme f05 et k07 :
   `erreur : échec de « git clone -b nope … » (code 128) : fatal: Remote branch nope not found in
   upstream origin`. Une seule ligne `erreur :`. Sous `-v`, la ligne de D14 nomme les répertoires
   retirés.
5. **Clones déjà laissés sur disque par une version antérieure** (§1.7) : contrôle de version
   dans `seed-clone` et pour le clone de graine de `_clone_seed`. Hors de cette étape, ajouté au
   hors-plan (D25). C'est un changement de comportement de `seed-clone`, que lepton appelle à
   chaque ajout.
6. **Documentation** :
   - docstring de `clone()` ;
   - `CHANGELOG.md`, nouvelle section « Corrections » ;
   - `README.md` l. 361-365 : la conservation ne vaut plus que pour une clé projetée ;
   - P-V1 inchangé : sa phrase compare avec 0.5.4.0 et reste vraie de cette version ;
   - `test_clone_whose_checkout_fails_is_kept` inversé : aucun répertoire laissé.
7. **Numéro de version** : `0.6.3.2`. C'est une correction ; formats et commandes inchangés
   (précédent : 0.6.3.1).
8. **`SCION_MIN_VERSION`** inchangé, (0, 6, 2, 0) (précédent : PA-99). **`SCION_REF`** →
   `0.6.3.2` dans lepton-tools et dans le clone noyau (branche `devenv/env-60` du clone noyau).
9. **lepton** : pas de changement de code. Docstring de `_undo_add` précisée : le clone conservé
   est celui d'un clonage réussi. l02 et l03 donneront tous deux le code 2, avec le message de
   git.

## 2. Décisions du PA-107 (2026-11-17, utilisateur)

Propositions du §1.9 retenues telles quelles (questions posées) :
1. Correction : `git clone -b <version> <url> <dest>` dans `gitops.clone`, sans `single_branch`.
2. Cas couverts : clé ordinaire (`_fetch`) et graine distante (`_clone_seed`). `--single-branch`
   et clé projetée (P-V1) inchangés.
3. Version commit complet d'une clé ordinaire : refusée dès le premier passage, et écrit au
   `CHANGELOG.md`.
4. Message : celui de git, sans texte ajouté.
5. Clones déjà laissés sur disque, réutilisés sans contrôle par `seed-clone` et `_clone_seed` :
   hors-plan, D25.
6. Documentation : docstring de `clone()`, `CHANGELOG.md`, `README.md` l. 361-365. P-V1 reste
   inchangé ; `test_clone_whose_checkout_fails_is_kept` est inversé.
7. Version 0.6.3.2.
8. `SCION_MIN_VERSION` inchangé (0, 6, 2, 0). `SCION_REF` passe à 0.6.3.2 dans lepton-tools et le
   clone noyau.
9. lepton : aucun code changé ; docstring de `_undo_add` précisée.

## 3. Implémentation (seed.scions, `devenv/env-60`)

| Commit | Contenu |
| --- | --- |
| cd1ed8a | Tests d'abord. `tests/test_clone_checkout.py` : 15 tests. `test_failed_clone.py` : `test_clone_whose_checkout_fails_is_kept` inversé en `test_version_missing_upstream_leaves_nothing`. Sur 0.6.3.1, 11 échouent : version absente, passage suivant, `seed-clone` après un échec, version-chemin, commit complet, origine vide, branche homonyme d'un répertoire, 3 cas de graine distante, test inversé. Les 5 cas de versions présentes réussissent : branche autre que celle de l'origine, `master`, tag, passage suivant, graine à sa branche (`env-60-scion/tests-avant-correction.txt`) |
| 0fc156c | `gitops.clone` : `git clone -b <version>`, plus `--single-branch` si demandé, à la place de `git clone` puis `git checkout`. Docstring réécrite. `tests/test_seed.py:124` (0.5.1.1) : l'assertion `checkout master` devient `git clone -b master`, et le test vérifie qu'aucun clone ne reste. Le comportement visé (code 2) est inchangé ; seul le texte de la commande change (point 4 du PA-107) |
| fb4d55d | 0.6.3.2 : `scion/__init__.py`, `tests/test_cli.py`, `CHANGELOG.md` (« Corrections » : clone à sa version ou pas du tout, commit complet refusé dès le clonage, cas inchangés), `README.md` l. 361-366 |
| 08a1460 | Docstring d'un test sans nom de client : la première version nommait lepton, et le contrôle NF-2 donnait 1 |

Contrôles :
- tests de scion : 313 (298 + 15), tous verts, plus 1 sauté (`test_network`) ;
  `env-60-scion/tests-apres-correction.txt` : 42 tests des trois fichiers touchés, verts ;
- NF-2 : `git diff 0.6.3.1 -- scion tests | grep -ci '^+.*lepton'` donne 0 ;
- `git diff --stat 0.6.3.1 0.6.3.2` : 8 fichiers, +247 −21 ;
- P-V1 et `doc/projection-miroir.md` : inchangés.

## 4. Essais avec la branche (venv `essais/env-60-venv`, scion 0.6.3.2)

Venv installé par `pip install "git+file://<SEED_SCIONS>@devenv/env-60"`. Les cas u01 sont lancés
après le tag, avec le scion 0.6.3.2 de pipx (§5), pour que `scion graft-update` garde la forme
exacte de la règle `ask`. Un exécutable du venv appelé par son chemin ne serait pas couvert par la
règle.

- **Fixture d'ENV-60** (`fixture-apres/`) :

  | Cas | Avant | Après |
  | --- | --- | --- |
  | k01, k02 (D18) | 2, clone gardé sur `master` ; 1 « introuvable » | 2, 2 : `git clone -b nope` refusé (`fatal: Remote branch nope not found in upstream origin`), aucun répertoire |
  | k18, k18b, k18c (`seed-clone`) | 2 ; **0** ; **0**, greffe de `master` | 2 ; 2 ; 1 (liste greffée vide) |
  | k04, k05, k06 (graine distante) | 2 ; **0** ; **0**, graine de `master` greffée | 2 ; 2 ; 1 |
  | k08, k09, k10 (version-chemin) | **0** ; **0** ; 1 | 2 ; 1 ; 2 |
  | k17, k17b (graine, version-chemin) | **0** ; **0** | 2 ; 1 |
  | k11, k12 (branche homonyme d'un répertoire) | 2 ; 1 | 0, branche `doc` suivie d'`origin/doc` ; 0 |
  | k15, k16 (origine vide) | 2, clone vide gardé ; 1 | 2 ; 2, aucun répertoire |
  | k19, k19b (commit complet) | 0 ; 1 | 2 ; 2 |
  | u01c, u01d (`graft-update`) | 2, clone `plain2/nope` gardé ; 1 | 2 ; 2 ; trunk et clones = départ, aucun clone `plain2/nope` |

  Cas non visés, identiques à l'avant pour tous les fichiers : k07 (`--single-branch`), k13,
  u01a, u01b, u01-départ. k14 (tag) a les mêmes `.cmd`, `.out`, `.err`, `.code`, `.depots` et
  `.trunk`, et le même `HEAD` (tag, `origin/master`). Il n'a plus de branche locale `master` :
  `git clone -b <tag>` n'en crée aucune, alors que `git clone` créait celle de l'origine avant le
  `checkout`. De même, le clone d'une branche autre que celle de l'origine ne porte plus que sa
  propre branche locale ; les autres restent en `origin/*`. Le contrôle de 0.5.4.0 lit les
  branches locales et distantes (`is_branch`) : aucun effet sur lui.
- **Fixture d'ENV-56** (`fixture56-apres/`, contre `fixture56-avant/`) :
  - f06 : `.err` = message de `git clone -b nope`, `.depots` vide (avant : 4 répertoires, dont
    le clone `nope`) ;
  - f01 à f04, f10 (dépôt absent) : **`.err` changé**. Le message nomme
    `git clone -b master <url> <dest>` au lieu de `git clone <url> <dest>`, avec la même fin
    (`(code 128) : and the repository exists.`). `.cmd`, `.out`, `.code` et `.depots` sont
    identiques. C'est la commande retenue au PA-107 ; elle s'écarte du critère « identiques à
    l'avant » pour ces 5 `.err` ;
  - autres cas (f05, f07 à f12b) : identiques.
- **Rootstock d'essai, l01 à l03** (`apres/`) :
  - l01 (`@scion`), l02 et l03 (`@nope`) : code 2. lepton relaie
    `erreur : échec de « git clone -b … » (code 128) : fatal: Remote branch … not found in
    upstream origin`, puis annule (« graine et trunk restaurés ») ;
  - l02 = l03 ; après chaque cas, liens, graine, liste greffée et `depots/` sont égaux au
    départ, et aucun clone ne reste ;
  - avant : l01 code 0 (greffe de `master` sous `scion`), l03 code 0 (greffe sous `nope`).
- **`seed add` réussi, puis `seed remove`** (`env-56-scion/succes.sh`, famille F7 de GitHub) :
  - deux copies neuves d'`essais/env-11/qemu`, `essais/env-60-succes-0631` (0.6.3.1, pipx) et
    `essais/env-60-succes-0632` (branche) ;
  - dans les deux cas : 3059 liens au départ et après `seed remove`, 0 cassé, graine et liste
    greffée égales au départ ; `depots/` garde le clone de la famille et les clones tiers
    (P-P6), comme en ENV-56 ;
  - `diff -r succes-0631 succes-0632` ne diffère que par `scion.txt`. Sont donc identiques :
    les messages, les codes, les liens, les clones tiers et la tête de la famille (`master`).

## 5. Version, lepton, noyau

- seed.scions :
  - tag annoté local `0.6.3.2` sur 08a1460 (tête de `devenv/env-60`) ;
  - `pipx install --force "git+file://<SEED_SCIONS>@0.6.3.2"` : scion 0.6.3.2 ;
  - les 10 modules installés sont identiques au tag (`cmp`) ;
  - `lepton --version` donne `scion 0.6.3.2 (requis ≥ 0.6.2.0)`.
- lepton-tools, e7a589f :
  - `SCION_REF="0.6.3.2"` (`scripts/install-vscodium.sh`), `README.md`, note dans
    `lepton/__init__.py` ;
  - `SCION_MIN_VERSION` inchangé, (0, 6, 2, 0) ;
  - docstring de `_undo_add` : le clone conservé est celui d'un clonage réussi suivi d'une greffe
    en échec ; un clonage dont la version manque à l'origine n'en laisse plus aucun.
- `pytest` de lepton-tools (venv `~/lepton-tools-dev/venv-lepton-tools`, scion 0.6.3.2 du PATH) :
  508 verts, `test_echec_de_scion_sans_double_affichage` compris.
- Clone noyau, branche `devenv/env-60` (depuis `master` ed2a41f), 8563f90 :
  - `SCION_REF` 0.6.3.2 dans `scripts/install-{macos,debian}.sh`, `README.md`,
    `README-PAQUET.md`, `doc/BUILDING.md` ; `bash -n` des deux scripts sans erreur ;
  - ces fichiers sont hors de `scion/` : rien n'est greffé, et le trunk ne change pas ;
  - contrôles de `<ROOTSTOCK>` : 0 lien cassé ; 7 fichiers réguliers, les `.DS_Store` du Finder
    datés du 12 novembre, tolérés (`.scion.trunk.tolerated`) et déjà relevés en ENV-56.
- lepton n'est pas réinstallé par pipx : son code ne change pas, seule une docstring change.

## 6. Binaires

Pas d'oracle :
- la correction ne touche que le clonage d'un scion ordinaire ou d'un seed distant ;
- un clone dont la version existe est fait au même commit qu'avant, et l'essai de greffe réussie
  (§4) donne avec 0.6.3.1 et avec 0.6.3.2 des liens et des clones identiques ;
- `<ROOTSTOCK>` n'est pas regreffé, et ses clones existants ne sont pas touchés : aucune commande
  de clonage ne les vise ;
- l'arbre composé ne change donc pas, et aucune reconstruction n'est nécessaire (forme
  d'`env-56-scion.md` §6).

## 7. Écarts aux critères, à trancher au PA-108

1. Fixture d'ENV-56, f01 à f04 et f10 (dépôt absent) : le `.err` nomme `git clone -b master …`
   au lieu de `git clone …`. Le critère demandait des cas non visés « identiques à l'avant ».
   Codes, `.out` et `.depots` le sont.
2. `tests/test_seed.py:124` (0.5.1.1) : l'assertion sur le texte `checkout master` est adaptée
   à `git clone -b master`. Le fichier d'étape demandait que les 298 tests existants restent
   verts ; ils le sont, celui-ci après adaptation de son texte, et
   `test_clone_whose_checkout_fails_is_kept`, inversé au PA-107.
3. Clone d'un tag, ou d'une branche autre que celle de l'origine : plus de branche locale pour
   la branche de l'origine (k14). `HEAD`, arbre extrait et contrôle de version inchangés.
4. Forme : le tout premier `graft-update` de l'audit portait un préfixe `cd … && LC_ALL=C`
   (§1.1). La base a été refaite ; tous les relevés versionnés viennent de lancements dans la
   forme exacte.
