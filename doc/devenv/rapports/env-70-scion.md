# ENV-70 — scion : cause de l'échec de git (D35), version de la graine clonée (D33)

Session du 2026-11-23, hôte Mac. Point de départ : seed.scions `master` 49ca4ae (tag 0.6.3.3),
scion 0.6.3.3 (pipx), git 2.50.1 (Apple Git-155) et git 2.18.0 (`/usr/local/git/bin/git`).
Branches `devenv/env-70` : lepton-tools (depuis `main` fa7b883), seed.scions (depuis `master`
49ca4ae).

Outils (`env-70-scion/`) :
- `bin/git` : enveloppe de git, placée en tête du PATH. Elle journalise chaque appel (arguments,
  code, stderr complet) dans `$ENV70_GITLOG`. Un appel qui porte `--single-branch` passe par
  `$ENV70_GIT_SINGLE` : git 2.18.0, qui écrit l'avertissement de la VM.
- `fixture.py` : cas D33 (g01-g21) et D35 (k01-k03), sur des rootstocks temporaires
  (`essais/env-70-fixture/<phase>/fixture70`). Forme d'`env-65-scion/fixture.py`.
- `rejouer.sh <scion> <avant|apres>` : rejoue la fixture 70, puis celles d'ENV-65, ENV-60 et
  ENV-56 sous l'enveloppe.
- `classer.py` : classe les lignes du stderr des appels git en échec.
- `construits.sh <base> <git> <sortie>` : échecs construits des commandes git de scion.
- Relevés : `fixture{70,65,60,56}-avant/`, `git-echecs-avant.tsv`,
  `construits-git{250,218}.txt`, `inventaire-avant.tsv`.
- Traductions : `po/fr.po` de git `v2.47.3`, téléchargé de `raw.githubusercontent.com/git/git`
  dans `essais/env-70-fixture/po/`. sha256 `62fbd300…cb8b8`, identique à ENV-62 et ENV-65.

Les fixtures d'ENV-65, ENV-60 et ENV-56, rejouées sur 0.6.3.3, égalent les relevés `-apres`
d'ENV-65, à un écart près : `fixture56` f12a et f12b (`.depots`, `fixture.tsv`). Ces lignes
listent les ancêtres du miroir, et leur nombre suit la profondeur de la base
(`env-70-fixture/avant/fixture56` au lieu d'`env-65-fixture`). L'écart vient du chemin, pas de
scion.

Incident de la session : un premier répertoire de sortie de la fixture
(`env-70-scion/fixture-avant/`, créé par la session quelques minutes plus tôt, jamais commité,
renommé depuis `fixture70-avant/`) a été supprimé par `rm -rf`, et non par
`scripts/supprimer-essai.sh` (CLAUDE.md). Il a été régénéré par `rejouer.sh`. Aucun autre fichier
n'a été touché.

## 1. Audit D35

### 1.1 Reproduction au Mac

git 2.18.0 écrit l'avertissement, comme git 2.47.3 de la VM ; git 2.50.1 ne l'écrit pas. Le cas
se reproduit donc au Mac, avec un vrai git, sans stderr fabriqué.

| Cas | Commande | git du clone | Message de scion 0.6.3.3 (après « code 128 : ») |
| --- | --- | --- | --- |
| k01 | `seed-add --single-branch`, clé `own/plain nope` | 2.18.0 | `warning: Could not find remote branch nope to clone.` |
| k02 | `seed-add --single-branch --version nope <graine distante>` | 2.18.0 | idem |
| k03 | k01 | 2.50.1 | `fatal: Remote branch nope not found in upstream origin` |

Stderr complet de git 2.18.0 (`fixture70-avant/k01-218.git-err`) :
```
warning: Could not find remote branch nope to clone.
fatal: Remote branch nope not found in upstream origin
fatal: The remote end hung up unexpectedly
```

### 1.2 Lignes des appels git en échec dans les fixtures

`git-echecs-avant.tsv` couvre 50 appels en échec sur 700 journalisés (fixtures 70, 65, 60, 56).

| Suite des classes | Nombre | Première ligne = cause `fatal:`/`error:` ? |
| --- | --- | --- |
| `F` | 22 | oui |
| `F F - -` (cause, « Could not read… », conseil) | 19 | oui |
| `W F F` (k01, k02, git 2.18.0) | 2 | **non** : avertissement |
| `- F F - -`, `- F` (rejeux de la fixture 65 sans `--quiet`, hors scion) | 5 | non : `Cloning into…` ; scion passe `--quiet` |
| vide (`rev-parse --verify --quiet`, `config --unset-all`) | 2 | sans objet : échecs muets, attendus |

Classes : F `fatal:`, E `error:`, W `warning:`, H `hint:`, `-` autre.

### 1.3 Échecs construits (`construits.sh`, `LC_ALL=C`)

| Commande de scion | git 2.50.1 | git 2.18.0 |
| --- | --- | --- |
| `merge --ff-only --quiet @{u}`, branche divergée (`gitops.fast_forward`) | **9 lignes `hint:`**, puis `fatal: Not possible to fast-forward, aborting.` | `fatal:` seule |
| `push --porcelain`, non rapide (`mirror._push`) | `error: failed to push…`, puis 5 `hint:` | idem |
| `rev-list … @{u}` sans amont | `fatal:` seule | idem |
| `checkout --detach <absent>` | `fatal:` seule | idem |
| `clone -b nope --single-branch` | `fatal:` seule | **`warning:`**, puis 2 `fatal:` |
| `clone` partiel, `--mirror`, `fetch`, `ls-remote` d'un dépôt absent | `fatal:` ×2, puis conseil | idem |

Le défaut de D35 touche aussi `fast_forward` avec git 2.50.1 (Mac), et pas seulement
`--single-branch` avec un git ancien. `seed_updates` et `_check_clone` écartent une branche
divergée avant l'avance, donc ce cas ne paraît que si l'amont change entre le contrôle et l'avance.
L'échec de `_push` n'est montré que si git ne rend aucun compte rendu par référence
(`mirror.py:251`) ; sa première ligne est alors `error:`.

### 1.4 Préfixes traduits (`po/fr.po` v2.47.3)

U+00A0 noté `⍽`.

| Anglais | `fr.po` (ligne) |
| --- | --- |
| `fatal: ` | `fatal⍽: ` (22995) |
| `error: ` | `erreur⍽: ` (22998) |
| `warning: ` | `avertissement⍽: ` (23001) |
| `%shint:%s…` | `%sastuce⍽:%s…` (720) |
| `usage: ` | `usage⍽: ` (22992) |
| `remote: ` | absent de `fr.po` : non traduit |
| `Could not find remote branch %s to clone.` | `Impossible de trouver la branche distante '%s' à cloner.` (4422) |

Sur la VM, R66-1 a relevé, en français et avec `--single-branch` :
`avertissement⍽: Impossible de trouver…`, puis `fatal⍽: La branche distante nope…`.

Une règle qui reconnaît les préfixes anglais et français laisse les autres langues de git à la
règle de repli. Avec `LC_ALL=C`, les messages de git sont en anglais pour tout le monde, causes
comprises. Aujourd'hui, sur la VM, ces causes paraissent en français.

## 2. Audit D33

### 2.1 Chemins qui mènent une graine à `seed_updates`

`graft.update_sources` (`graft.py:364`) → `seed_updates` (l. 515) ; trois appelants :

| Commande | Graines passées | Peuvent avancer |
| --- | --- | --- |
| `seed-add` (`cli.py:85`) | la graine désignée | seulement une graine distante déjà clonée (`movable`), contrôlée par `_clone_seed` depuis 0.6.3.3 |
| `seed-update` (`cli.py:127`) | `--seed`, ou la graine du répertoire courant | toutes |
| `graft-update` (`cli.py:175`) | les graines de la liste greffée (5ᵉ colonne, `graft.seeds`) | toutes |

lepton ne lance ni `seed-update` ni `graft-update` (aucune occurrence dans `lepton/`,
`extension/src/`, `scripts/`).

Distinguer une graine clonée par `_clone_seed` d'une graine donnée par un chemin : la liste
greffée n'enregistre que le chemin du `.scion/`, sous la même forme dans les deux cas.
`_clone_seed` clone dans `depots/<nom>/<version>`, où `<nom>` est la base de l'URL
(`Path(url.rstrip("/")).stem`), et git garde cette URL en `remote.origin.url`. Critère proposé :
le dépôt de la graine (`toplevel`) est `depots/<base de son URL origin>/<version>`. `<version>`
est le reste du chemin et peut porter une barre (g20). Le critère se lit sur le dépôt seul, sans
réseau. Il écarte les graines hors de `depots/`, les graines sans `origin` (graines de projet,
g18) et une graine placée sous `depots/` à la main sous un autre nom (g16). Un critère plus
simple, `depots/<x>/<y>` à deux niveaux, rate g20 et retient g16.

### 2.2 Cas de la fixture (`fixture70-avant/fixture.tsv`)

Graine distante `graine` : `master` déclare `own/plain master`, `autre` déclare
`own/plain dev`, tag `t1` sur `autre`. Avant chaque commande, l'amont reçoit un commit.

| Cas | État de la graine | Commande | 0.6.3.3 |
| --- | --- | --- | --- |
| g02 | à sa version `autre` | `seed-update` | avance sur `autre` (témoin) |
| g04 | `autre` sur la branche `master` | `seed-update` | code 0 ; **avance `master`** ; clone `own/plain/master` créé ; liste greffée réécrite sur `master` |
| g06 | idem | `graft-update` | code 0 ; idem, **et le trunk est greffé** sur `own/plain/master` |
| g08 | à sa version `autre` | `graft-update` | avance (témoin) |
| g10 | tag `t1`, HEAD détaché | `seed-update` | laissée, sans amont (témoin) |
| g11 | `t1` sur la branche `autre` | `seed-update` | code 0 ; **avance `autre`** au-delà du tag |
| g13 | `autre` détachée sur `origin/master` | `seed-update` | code 0, laissée sans message (pas d'amont) ; lue telle quelle |
| g15 | graine par chemin (clone hors `depots/`, `autre`) | `seed-update` | avance (témoin) |
| g17 | graine par chemin sous `depots/manuel/travail` | `seed-update` | avance (témoin) |
| g19 | graine locale sans `origin` sous `depots/projets/p1` | `seed-update` | laissée (témoin) |
| g21 | `f/x` sur la branche `master` | `seed-update` | code 0, rien à avancer ; lue sur `master` |

Dans g04, g06, g11, g13 et g21, la graine lue n'est pas à la version demandée, et rien ne le
signale.

### 2.3 Graines distantes clonées des rootstocks

Mac (`inventaire-avant.tsv`, `env-65-scion/inventaire.py`, lecture seule) : `<ROOTSTOCK>` et
12 rootstocks d'essai. 5 graines distantes, toutes `depots/lepton-seed.scions/original-tree` sur
la branche `original-tree` (`<ROOTSTOCK>`, `env-13-vierge`, `env-34-copie`, `env-35-copie`,
`env-37-copie`). 6 graines locales, sans objet. 0 graine hors version.

Les `hors_version` d'`env-34-copie` (2), d'`env-35-copie` (3) et d'`env-37-copie` (1) sont des
clones de greffons de ces copies figées, sur leurs branches de travail. Ce ne sont pas des
graines, et ils sont hors de D33.

VM (`rapports/env-66-debian.md` §9) : graine `original-tree` dans `env-13-debian`,
`env-28-debian` et `env-53-debian`. Sa branche n'est pas relevée. La preuve n'est
qu'indirecte : 4 `graft-update` conformes, liens inchangés (3889 → 3889). Une graine hors
version y ferait échouer C3 d'ENV-72 si le refus est retenu.

## 3. Propositions pour le PA-127 (non validées)

1. **D35, règle** : la première ligne non vide dont le préfixe est `fatal:` ou `error:`, en
   anglais ou dans sa traduction française (`fatal⍽: `, `erreur⍽: `). À défaut, la première
   ligne non vide (règle de 0.6.3.3). Une seule ligne, `-v` inchangé.
   - Effet : la règle donne la cause pour k01, k02 (W F F) et `fast_forward` (H… F), sans
     changer les 41 cas F en tête.
   - Avec git dans une autre langue, la règle retombe sur celle de 0.6.3.3 et ne régresse pas.
   - Écarté, `LC_ALL=C` pour git. Ce serait indépendant de la langue, mais les causes
     passeraient en anglais pour un utilisateur français, et les relevés de la VM
     (`comparer-releves.py`) changeraient. À choisir si l'indépendance de la langue prime.
   - Les lignes `warning:` et `hint:` n'ont pas besoin d'une règle à part : la recherche de
     `fatal:` ou `error:` les saute.
2. **D35, portée** : toutes les commandes de `_run`, comme D22. Codes et comportements
   inchangés.
3. **D33, correction** : refus, comme pour un clone hors version (même contrat
   d'`update_sources` : tous les contrôles d'abord, rien n'est modifié).
   - Le message reprend `version_fault(top, version, declared="demandée")` : branche courante
     ou HEAD détaché, version demandée, commande `git -C … switch …`. Code 1.
   - Le contrôle se fait dans `seed_updates`, avant les autres contrôles de la graine, et voit
     donc aussi une graine détachée (g13).
4. **D33, graines couvertes** : celles du critère du §2.1, à branche ou à tag (`version_fault`
   traite les deux). `seed-add` (déjà contrôlé par `_clone_seed`) n'en est pas changé.
   Non couvertes : graines données par un chemin, graines sans `origin`.
5. **Documentation** : docstrings de `_run`, `seed_updates`, `update_sources` ; `README.md` (la
   phrase « `seed-update` et `graft-update` avancent un seed sans le comparer à une version »
   est remplacée, la phrase sur le message de git est complétée) ; `CHANGELOG.md` 0.6.3.4,
   « Corrections ».
6. **Version** : `0.6.3.4` (décision du 2026-11-23).
7. **`SCION_MIN_VERSION`** inchangé (0, 6, 2, 0) : lepton ne dépend d'aucun des deux lots.
   `SCION_REF` passe à `0.6.3.4` :
   - lepton-tools : `install-vscodium.sh`, `README.md`, note de `lepton/__init__.py` ;
   - clone noyau : `install-{macos,debian}.sh`, `README.md`, `README-PAQUET.md`,
     `doc/BUILDING.md`, sur une branche `devenv/env-70` du noyau, comme en ENV-65.
8. **Effets sur lepton** : aucun code. `test_echec_de_scion_sans_double_affichage` reste vert
   (une ligne). `comparer-releves.py` ramène déjà `fatal⍽: ` et « La branche distante… » :
   k07 et f05 de la VM devraient égaler le Mac en ENV-72.
9. **ENV-72** (à porter dans sa consigne) : relever la branche de
   `depots/lepton-seed.scions/original-tree` de chaque rootstock de la VM avant C3.

## 4. Décisions du PA-127 (2026-11-23, utilisateur)

Les propositions du §3 sont retenues telles quelles :
1. D35 : première ligne non vide dont le préfixe est `fatal:` ou `error:` (anglais, ou
   `fatal⍽: `, `erreur⍽: `), sinon première ligne non vide ; une ligne ; toutes les commandes de
   `_run`.
2. D33 : refus au texte de `version_fault(…, declared="demandée")`, code 1, rien modifié ;
   contrôle dans `seed_updates` avant les autres contrôles de la graine.
3. Graines couvertes : dépôt = `depots/<base de l'URL origin>/<version>` (barre admise), branche
   ou tag ; non couvertes : graines par chemin, graines sans `origin`.
4. Documentation, version 0.6.3.4, `SCION_MIN_VERSION` inchangé, `SCION_REF` 0.6.3.4
   (lepton-tools, clone noyau), aucun code de lepton, relevé de la graine dans la consigne
   d'ENV-72.
