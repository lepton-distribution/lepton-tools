# ENV-65 — scion : clone existant hors version (D25), message d'échec de git (D22)

Branches `devenv/env-65` : seed.scions (depuis `master` 975caf6, tag 0.6.3.2 + 1) et
lepton-tools (depuis `main` f715f87). État de départ :
- scion 0.6.3.2 (pipx, `~/.local/bin/scion`) et lepton 0.1.0 ;
- git 2.50.1 (`/usr/bin/git`, Apple Git-155, **non traduit** : `LC_ALL=fr_FR.UTF-8` donne
  l'anglais), Python 3.11.5, Claude Code 2.1.328 ;
- tests de scion sur `master` : 313, verts, 1 sauté (`test_network`) ; noyau `master` dfc960b.

Scripts et relevés, dans `env-65-scion/` :
- `inventaire.py <rootstock>…` : clones, graines et orphelins de `depots/`, comparés à leur
  version déclarée. Lecture seule : `rev-parse`, `branch`, `for-each-ref`, `remote get-url`.
  Relevé dans `avant/inventaire.tsv` ;
- `fixture.py` : cas a01 à f05 (D25) et n01 à n07b (D22), sur des rootstocks temporaires
  (`essais/env-65-fixture/avant/`), forme d'`env-60-scion/fixture.py` dont il reprend `etat.py`.
  Un clone est mis hors de sa version à la main ; la commande est écrite dans `<cas>.prep`.
  Pour D22, la commande git de scion est rejouée hors de scion, avec son stderr complet dans
  `<cas>.git-err`. Tableau : `fixture-avant/fixture.tsv`, avec le contenu de `trunk/f.txt` lu
  par son lien ;
- `fixture56-avant/`, `fixture60-avant/` : fixtures d'ENV-56 et d'ENV-60 rejouées telles quelles
  avec 0.6.3.2. Ce sont les références des cas non visés pour l'essai après correction. Elles
  sont identiques à `env-60-scion/fixture56-apres/` et `fixture-apres/`. Les seuls écarts sont la
  normalisation des ancêtres de `<HOME>` (ENV-62), le nom de la base (`env-65-fixture`) et les
  cas u01c et u01d, qui ne sont pas lancés ici.

Dans les relevés : `<B>` base de la fixture, `<HOME>` répertoire personnel ; `<V1>`, `<MASTER>`,
`<DEV>` commits du dépôt `plain`.

Dépôts de la fixture :
- `plain` : tag annoté `v1` (`f.txt` = « v1 »), `master` (« master »), branche `dev` (« dev ») ;
- `graine` : `master` déclare `own/plain master`, la branche `autre` déclare `own/plain dev`.

## 1. Audit D25 (scion 0.6.3.2)

### 1.1 Clé ordinaire

| Cas | Situation, commande | Code | Effet |
| --- | --- | --- | --- |
| a01, a02 | `seed-add` (`own/plain dev`), `graft` | 0, 0 | `f.txt` = « dev » |
| a03 | clone remis sur `master` (`git checkout master`), puis `seed-clone --seed` | **0** | rien n'est signalé |
| a04 | `graft` | **0** | `f.txt` = « master » sous la version `dev` : **greffe fausse** |
| a05 | `graft --scion own@plain` | **0** | idem |
| a06 | `seed-add` relancé | 1 | `branche « master », version déclarée « dev » ; git -C … switch dev` (contrôle de 0.5.4.0) |
| b01 | clone `depots/own/plain/dev` préexistant sur `master`, fait par `git clone` sans `-b` (forme du clone laissé par ≤ 0.6.3.1, l03 d'ENV-60) ; `seed-clone` | **0** | la clé est écrite dans la liste greffée, version `dev` |
| b02 | `graft` | **0** | `f.txt` = « master » : **greffe fausse** |
| b03 | même clone préexistant ; `seed-add` | 1 | refus (forme a06) |
| c01, c02 | clone du tag `v1` préexistant sur `master` ; `seed-clone`, `graft` | **0**, **0** | `f.txt` = « master » sous `v1` |
| c03 | même clone ; `seed-add` | 1 | `version déclarée : tag « v1 » ; git -C … switch --detach v1` |

Le fichier d'étape est confirmé pour `seed-clone` (k18). Fait nouveau : `graft` et
`graft --scion` greffent aussi, en code 0, un clone ordinaire hors de sa version. Pour une clé
ordinaire, `seed-add` refuse déjà (a06, b03, c03).

### 1.2 Graine distante (`cli._clone_seed`, k05)

| Cas | Situation, commande | Code | Effet |
| --- | --- | --- | --- |
| d01 | `seed-add --version autre <graine>` | 0 | clone `depots/graine/autre` sur `autre` ; `own/plain/dev` cloné |
| d02 | graine remise sur `master`, puis `seed-add` relancé | **0** | la graine de `master` est lue : `own/plain/master` cloné, liste greffée `own plain master …` (graine `depots/graine/autre/scion/.scion`) |
| d03 | `graft` | **0** | `f.txt` = « master », contenu déclaré par la graine de `master` |
| d04, d05 | graine `autre` préexistante sur `master`, faite par `git clone` sans `-b` ; `seed-add`, `graft` | **0**, **0** | même effet, jamais signalé |

`_clone_seed` réutilise le clone (`cli.py:108`). Puis `seed_updates` l'avance par avance rapide
depuis l'amont de sa branche courante. Rien ne compare cette branche à `--version`.

### 1.3 Témoins et branche de travail

| Cas | Situation | Codes | Effet |
| --- | --- | --- | --- |
| e01 à e07 | clones et graine à leur version (branche `dev`, tag `v1`, graine `autre`) : `seed-add`, `seed-clone`, `graft`, graine relancée | tous 0 | clones sur leur version ; ces cas doivent rester identiques après correction |
| f01, f02 | `own/plain master`, `seed-add`, `graft` | 0, 0 | — |
| f03, f04 | `git checkout -b travail` dans le clone (forme du clone noyau sur `devenv/env-N`) ; `seed-clone`, `graft` | **0**, **0** | la branche de travail est greffée |
| f05 | `seed-add` relancé | 1 | `branche « travail », version déclarée « master » ; git -C … switch master` |

Un clone déplacé par l'utilisateur après la greffe (a03) et un clone mis sur une branche de
travail (f03) ont le même état : scion ne peut pas les distinguer. Les commandes de mise à jour
(`seed-add`, `seed-update`, `graft-update`) refusent les deux. Les commandes de greffe
(`seed-clone`, `graft`) acceptent les deux. C'est sur ce second comportement que repose le
travail dans les clones (ORCHESTRATION §5) : on édite sur une branche `devenv/env-N`, puis on
regreffe.

### 1.4 Appelants qui réutilisent un clone existant

| Appelant | Ce qu'il réutilise | Contrôle de version aujourd'hui |
| --- | --- | --- |
| `seed-add` : clés de la graine | clones de `depots/` | **oui**, `update_sources` → `clone_updates` → `_check_clone` (clé ordinaire) ou `_check_projected_clone` (clé projetée) : a06, b03, c03 |
| `seed-add` : graine distante (`_clone_seed`) | `depots/<nom>/<version>` | **non**, `seed_updates` n'avance qu'en avance rapide : d02, d04 |
| `seed-update`, `graft-update` : clés | clones | **oui**, `update_sources` |
| `seed-update`, `graft-update` : graines | dépôt de la graine | **non** (`seed_updates`). Sans objet pour une graine donnée par un chemin. Pour une graine clonée, la version n'est inscrite nulle part, sauf dans le nom de son répertoire |
| `seed-clone` (`graft.sync` → `_fetch`) | clones des clés et des porteurs | **non** : a03, b01, c01 ; clé projetée réutilisée, puis refusée par la greffe |
| `graft`, `graft --scion` (`regraft`, `graft_scions`) | clones de la liste greffée | clé ordinaire : **non** (a04, a05, b02, c02, f04) ; clé projetée : **oui**, `_projected_state` (P-E1), test `test_clone_hors_commit_refuse` |
| `mirror-sync` | `depots/.mirrors/…` (dépôts `--mirror`, sans version) | sans objet |
| lepton : `seed add` (`seed.py:634`), `seed replace` (`_attach`, l. 746), greffe du projet (`graft_project`, l. 235) | `seed-clone` puis `graft --scion` | non : ils passent par `seed-clone` |
| lepton : `seed new`, initialisation (`seed.py:394`) | `seed-add <chemin>` puis `graft` | graine donnée par un chemin : sans objet ; clés : oui |

### 1.5 Clones hors version sur les rootstocks du Mac (lecture seule)

`avant/inventaire.tsv` (`inventaire.py`), sur `<ROOTSTOCK>` et les 7 rootstocks d'essai
d'`handoff/env-61.md` :

| Catégorie | Nombre | Hors version |
| --- | --- | --- |
| clones de la liste greffée (projetés compris) | 65 | **0** |
| graines distantes clonées (`depots/lepton-seed.scions/original-tree`, `<ROOTSTOCK>` et `env-13-vierge`) | 2 | **0**, branche `original-tree` |
| graines locales (graines de projet `depots/lepton-seed/<projet>`, sans `origin`, données par un chemin) | 6 | sans objet |
| orphelins sous `depots/` avec `origin` (`env-11/qemu-gra2` : `bsp-qemu-mps2-an386/master`) | 1 | 0 |
| orphelin local (`env-11/qemu` : `lepton-application/salut`, sans `origin`) | 1 | sans objet |

Attendu des clones de greffons (0) confirmé. Graines : 0. Aucun `<ROOTSTOCK>` ni rootstock d'essai
à remettre en version : la regreffe de `<ROOTSTOCK>` n'est pas nécessaire (fichier d'étape §4).

## 2. Audit D22

### 2.1 Messages de scion et stderr de git

| Cas | Commande git | Message de scion aujourd'hui (fin) | stderr complet de git (`.git-err`) |
| --- | --- | --- | --- |
| n01 | `clone -b master <absent>` | `(code 128) : and the repository exists.` | `Cloning into 'd'...` / `fatal: '<B>/repos/absent' does not appear to be a git repository` / `fatal: Could not read from remote repository.` / *(vide)* / `Please make sure you have the correct access rights` / `and the repository exists.` |
| n02 | idem, répertoire non git | idem | idem (`'<B>/repos/nongit'`) |
| n03 | `clone -b nope <plain>` | `fatal: Remote branch nope not found in upstream origin` | `Cloning into 'd'...` puis cette ligne |
| n04 | `clone -b master https://scion-essai.invalid/…` | `fatal: unable to access '…': Could not resolve host: scion-essai.invalid` | `Cloning into 'd'...` puis cette ligne |
| n05 | graine distante absente | `and the repository exists.` | comme n01 |
| n06b | `fetch --quiet` (contrôle de 0.5.4.0, origine repointée vers l'absente) | `and the repository exists.` | comme n01, sans `Cloning into` |
| n07b | `ls-remote --tags origin …` (contrôle d'un tag) | `and the repository exists.` | idem |

La cause est perdue dès que git finit par son conseil générique : URL absente, dépôt non git,
`fetch` ou `ls-remote` vers une origine disparue. `_run` sert à toutes les commandes, les
rapports de `mirror-sync` compris (« miroir inaccessible : … », f12a et f12b d'ENV-56).

Essai, hors de scion : avec `git clone --quiet -b …`, la ligne `Cloning into` disparaît. La
**première ligne** du stderr est alors la cause, dans les 4 cas de clonage (n01 à n04). Elle
l'est déjà pour `fetch --quiet` et `ls-remote`.

### 2.2 Français (VM) : textes tirés de `po/fr.po` v2.47.3

Le git du Mac n'est pas traduit. Le français de la VM se déduit de `po/fr.po` de git `v2.47.3`
(sha256 `62fbd300…cb8b8`, identique à ENV-62 ; U+00A0 noté `⍽`) :

| Anglais | `fr.po` |
| --- | --- |
| `fatal: ` (l. 22994) | `fatal⍽: ` |
| `error: ` (l. 22997) | `erreur⍽: ` |
| `Cloning into '%s'...` (l. 4492) | `Clonage dans '%s'...` |
| `'%s' does not appear to be a git repository` | **absent de `fr.po`** : reste en anglais derrière `fatal⍽: ` (déduction, à vérifier en ENV-66) |
| `Could not read from remote repository. … and the repository exists.` (l. 15855) | `Impossible de lire le dépôt distant. … et que le dépôt existe.` |
| `Remote branch %s not found in upstream %s` (l. 4549) | `La branche distante %s n'a pas été trouvée dans le dépôt amont %s` |
| `unable to access '%s': %s` (l. 20309) | `impossible d'accéder à '%s'⍽: %s` (fin donnée par curl, non traduite) |

Conséquences :
- reconnaître une ligne par son préfixe anglais (`fatal:`, `error:`) échoue en français, et dans
  toute autre langue ;
- la ligne `erreur⍽: ` de git porte une espace insécable. `"erreur :" in line` (test de lepton,
  espace ordinaire) ne la compte pas, mais un message à plusieurs lignes de git resterait fragile ;
- `scripts/comparer-releves.py` (`TRADUCTIONS`) ramène déjà `fatal⍽: ` et la branche distante.
  Il lui manquerait `impossible d'accéder à '%s'⍽: ` pour comparer un cas n04 de la VM.

### 2.3 Ce qui compare ces messages

- `consignes/env-61-debian.md:172`, `fr()` : ramène « et que le dépôt existe. » et la branche
  distante (espace ordinaire, défaut relevé en ENV-62). Consigne passée, non rejouée.
- `scripts/comparer-releves.py:36` : règle `(?<=: )et que le dépôt existe\.$`. Après D22, elle ne
  s'appliquera plus aux nouveaux relevés ; les anciens en ont encore besoin.
- `tests/test_comparer_releves.py:48` : texte d'essai de l'outil. Il ne dépend pas de scion.
- Relevés dont le `.err` change avec D22 : fixture d'ENV-56, f01 à f04, f07, f09b, f09c, f10,
  f11, f12a, f12b (11 fichiers) ; `env-60-scion/essai.sh` ; ENV-53 C5 ; ENV-61 (VM).
- Tests de scion : `test_seed.py:124` (`"git clone -b master"` dans le message) ;
  `test_cli.py:157` (`scion git`, message après la sortie de git). Ni l'un ni l'autre ne lit la
  dernière ligne.
- lepton : `test_echec_de_scion_sans_double_affichage` (URL absente) compte les lignes qui
  contiennent `erreur :` et ne viennent pas de lepton. Il passe tant que le message de scion
  n'a qu'une ligne `erreur :`.

## 3. Propositions pour le PA-117 (non validées)

1. **D25, correction** : refus, avec le texte de `_check_clone` (forme P-V1 : clone laissé en
   place, commande à lancer donnée). Pas de checkout : il déplacerait le travail de
   l'utilisateur. Pas de reclonage : il supprimerait un clone qui peut porter des commits.
2. **D25, cas couverts** :
   - `seed-clone` (`sync`) : contrôle d'un clone **adopté**, c'est-à-dire un clone existant dont
     la clé n'est pas inscrite dans la liste greffée avec ce clone et cette version (b01, c01).
     C'est la forme d'un clone laissé par une version antérieure, et c'est le chemin de lepton
     (l03 d'ENV-60).
     - Le contrôle lit seulement la version : branche courante ou commit du tag. Il ne fait ni
       `fetch` ni contrôle du retard. Il passe avant tout clonage, nomme tous les clones fautifs
       et laisse la liste greffée inchangée. Code 1.
     - Un clone déjà greffé reste accepté (a03, f03), puisque c'est le travail sur une branche.
       Sinon, `lepton seed add` et `seed replace` seraient refusés dès qu'un clone de la graine
       (le noyau, par exemple) est sur `devenv/env-N`.
   - `seed-add`, graine distante : la graine existante est contrôlée par la même lecture de
     version (d02, d04), avant `update_sources`. Code 1, rien n'est modifié.
   - Non couverts, avec la raison au rapport et dans la documentation :
     - `graft` et `graft --scion` (a04, f04), qui servent au travail en branche ; `seed-add`,
       `seed-update` et `graft-update` refusent déjà ces clones ;
     - les graines de `seed-update` et `graft-update`, dont la version n'est inscrite nulle
       part. Point écarté du plan à proposer (hors plan : scion n'est pas un greffon du
       rootstock).
   - Clé projetée exclue : la greffe la refuse déjà (P-E1, `_projected_state`), et P-V1 est
     inchangée.
3. **D22, message** : la **première ligne non vide** du stderr de git, avec `--quiet` ajouté à
   `git clone -b` (`gitops.clone`) pour ôter la ligne de progression. Ce choix est indépendant
   de la langue et garde une seule ligne `erreur :`. Sous `-v`, le stderr complet de git est
   journalisé (`log.debug`), comme il l'est déjà quand la commande réussit. Les options
   écartées :
   - la ligne `fatal:` ou `error:`, qui dépend de la langue (§2.2) ;
   - toute la sortie sur la ligne d'erreur, trop longue, avec le conseil générique.
4. **D22, portée** : toutes les commandes de `_run` (n06b et n07b ont le même défaut). Seul le
   texte change : codes et comportements sont inchangés. `scion git` affiche déjà la sortie
   complète de git avant le message.
5. **Documentation** : docstrings de `sync`, `_clone_seed` et `gitops._run` ; `CHANGELOG.md` ;
   `README.md` (la version en l. 367, et une phrase sur le contrôle des clones adoptés et sur
   les cas non couverts).
6. **Version** : `0.6.3.3`, une correction dont les formats et les commandes sont inchangés,
   comme pour 0.6.3.1 et 0.6.3.2. L'autre option est `0.6.4.0`, si le nouveau refus de
   `seed-clone` est tenu pour un changement de comportement, comme les contrôles de 0.5.4.0.
7. **`SCION_MIN_VERSION`** inchangé, (0, 6, 2, 0) : lepton ne dépend d'aucun des deux lots.
   `SCION_REF` passe à la nouvelle version dans lepton-tools (`install-vscodium.sh`,
   `README.md`, note de `lepton/__init__.py`) et dans le clone noyau
   (`install-{macos,debian}.sh`, `README.md`, `README-PAQUET.md`, `doc/BUILDING.md`) : branche
   `devenv/env-65` du noyau, comme en ENV-60.
8. **Effets sur lepton** : aucun code. lepton relaie le refus de `seed-clone` : `lepton seed
   add` affiche le message et annule (« graine et trunk restaurés »), et le clone préexistant
   reste. `test_echec_de_scion_sans_double_affichage` reste vert : une seule ligne `erreur :`.
   À vérifier par `pytest` avec le nouveau scion.
9. **Outils** : `scripts/comparer-releves.py` n'est pas touché dans cette étape. ENV-66 relèvera
   ses attendus avec le nouveau scion (fichier d'étape, pièges), et y ajoutera au besoin la
   règle `impossible d'accéder à`. Écarts attendus à l'essai : les `.err` du §2.3.
