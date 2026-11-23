# ENV-68 — lepton : chemins saisis et cohérence de la graine (D29, D30, D32, D37)

Session du 2026-11-23. Branche lepton-tools `devenv/env-68` (depuis `main` 58ed8f1).
Mac : Claude Code 2.1.330, scion 0.6.3.3, lepton 0.1.0 (code de `main`).

Essais :
- copie `essais/env-68-essai/rs` : `rsync -a` d'`essais/env-11/qemu`, sans `build/` (graine de
  projet `env11`, noyau 2b4a647) ; jamais `<ROOTSTOCK>` ;
- scripts versionnés pour ENV-72 :
  - `env-68-lepton/chemins.sh` : D29, D30 (forme d'`env-63-tilde/chemins.sh`) ;
  - `env-68-lepton/graine.sh` : D32, D37.
- relevés normalisés : `env-68-lepton/avant/`, `env-68-lepton/avant-graine/` (`resume.tsv` et un
  fichier par cas).

## 1. Audit (code de `main`)

### 1.1 D29 : `check FILE`, `seed mkconf import PATH`, `seed new --mkconf PATH`

Formes :
- `t` : `~/…` ;
- `u` : `~<U>/…` ;
- `x` : `~inconnu68/…` ;
- `a` : absolu ;
- `d` : `~/…` développé par bash ;
- `r` : relatif ;
- `rc` : relatif au répertoire courant ;
- `h` : absolu hors du trunk (clone) ;
- `th` : `~/…` hors du trunk.

Le chemin est transmis tel quel, comme le fait l'extension. « R » compare le rootstock avant et
après chaque cas.

| Cas | Formes | Code | Message, état |
| --- | --- | --- | --- |
| `check FILE` hors du trunk (`lepton-graine.json`) | t, u, x | 1 | `~/…/lepton-graine.json: fichier introuvable` ; R = |
| idem | a, d, r | 0 | `1 fichier(s) conforme(s).` |
| `check FILE` sous le trunk (`trunk/sys/root/src/lepton-greffon.json`) | t | 1 | `fichier introuvable` |
| idem | a, r | 0 | conforme |
| `seed mkconf import` (graine non migrée, une copie par cas) | t, u, x | 1 | `XML « ~/…/trunk/sys/user/tauon-basic/etc/… » absent du trunk greffé` ; R = |
| idem | a (sous le trunk), d, r (relatif au trunk) | 0 | `XML du projet : sys/user/env11/etc/mkconf_env11.xml (copie de …, avec .boot, .init)` ; liens et graine modifiés (attendu) |
| idem | rc (relatif au répertoire courant, cwd `trunk/sys/user/tauon-basic/etc`) | 1 | `XML « mkconf_tauon_basic_qemu_mps2.xml » absent du trunk greffé` : relatif = relatif au trunk |
| idem | h (absolu, clone) | 1 | `XML « …/depots/…/scion/… » hors du trunk …` |
| idem | th (`~/…`, clone) | 1 | `absent du trunk greffé` (le `~` n'est pas lu comme absolu) |
| `seed new --mkconf` (`-C <T>/n1-<f>`) | t, u, x, a, d | 1 | `graine refusée : /mklepton_xml: valeur "…" non conforme au motif …` ; rien n'est créé (contrôle du schéma, avant toute action) |
| idem | r | 0 | rootstock créé, XML du projet importé |

Constats :
- **`check FILE`** : `Path(name)` lu sans `expand_user`. Un `~` est refusé en « fichier
  introuvable », même pour `~inconnu68`.
- **`mkconf import`** (`seed.py:262-271`) : `~/…` n'est pas absolu pour `Path.is_absolute()`. Il
  est donc lu relatif au trunk : « absent du trunk greffé ». Un absolu sous le trunk est ramené au
  trunk. Un absolu hors du trunk est refusé. Le relatif est relatif au trunk, pas au répertoire
  courant (forme documentée ; inchangée sauf décision).
- **`seed new --mkconf`** : la valeur est contrôlée par le motif `chemin_relatif` du schéma de
  graine (`seed.py:349-356`) avant toute création. `~` et l'absolu y sont refusés, avec le motif
  pour seul message. Le trunk n'existe pas encore à ce moment : un absolu ne peut être ramené
  qu'au futur `<-C>/trunk`.
- Extension : `seedMkconfImport` (`commands.ts:186-191`) transmet le chemin désigné ou saisi. Une
  saisie `~/…` suit donc la ligne t. L'extension ne lance pas `seed new`.

### 1.2 D30 : `generate --clangd` relatif

Le chemin écrit est relevé dans `clangd.path` de l'espace de travail. La colonne « Trouvé »
indique s'il se résout depuis la racine du rootstock.

| Cas | Répertoire courant | Argument | `clangd.path` écrit | Trouvé |
| --- | --- | --- | --- | --- |
| a | racine | absolu | absolu | oui |
| t | racine | `~/…` | absolu (D21) | oui |
| nom | racine | `clangd-mp-21` | `/opt/local/bin/clangd-mp-21` (`which`) | oui |
| r | racine | `../w/outils/clangd` | `../w/outils/clangd` | oui |
| rs | `trunk/sys` | `../../../w/outils/clangd` | tel quel | **non** |
| rw | hors du rootstock, `-C` | `../outils/clangd` | tel quel | **non** |
| rd | hors du rootstock, `-C` | `./outils/clangd` | tel quel | **non** |

Cause (`generate.py:119`) : `shutil.which(explicit)` rend tel quel un chemin qui contient un `/`.
Le chemin relatif n'est juste que si lepton est lancé à la racine du rootstock, dans le cas où
VSCodium le résout depuis le dossier de l'espace.

### 1.3 D32 : retrait refusé entre les deux appels de scion

Origine `file://` : une URL donne un clone `depots/lepton/library-env68lib/master`. Un chemin
local sans version est greffé en place (version `*`, aucun clone). Les états sont comparés à
« ajouté », c'est-à-dire après `seed add`.

| Cas | Code | Graine (`sources`) | `lepton-graine.json` | Greffé | Message |
| --- | --- | --- | --- | --- | --- |
| r1 `seed remove --purge`, fichier non suivi dans le clone | 2 | **retiré** | gardé | oui | `… contient des modifications non commitées ; --purge refusé` |
| r1 puis `file remove` | 1 | — | — | — | `greffon « env68lib » (lepton@library-env68lib) hors de la graine` |
| r1 puis relance après nettoyage | 0 | — | retiré | non | `greffé hors de la graine : retiré du trunk seulement` ; état = départ |
| r2 `--purge`, commit local absent de l'amont | 2 | **retiré** | gardé | oui | `… contient des commits absents de l'amont ; --purge refusé` |
| r5 `--purge`, origine locale greffée en place | 2 | **retiré** | gardé | oui | `… n'a pas été cloné par scion (attendu sous …) ; --purge refusé` |
| r3 sans `--purge`, clone modifié | 0 | retiré | retiré | non | retrait normal ; clone gardé (attendu) |
| r4 `seed replace`, origine URL, clone modifié | 2 | = | = | = | `--purge refusé` ; état = « ajouté » (le `graft-remove` vient en premier) |

Contrôles de scion (`seed.scions/scion/graft.py:1274-1345`, `remove`) : `_purgeable_clone` vérifie
les cinq causes de refus avant tout changement :
- non cloné par scion ;
- clone partagé ;
- pas un clone git ;
- modifications non commitées ;
- commits absents de l'amont.

`_check_stray` (fichier régulier du trunk) est aussi vérifié avant. Un `graft-remove` refusé ne
change donc rien : le demi-état vient du seul `seed-scion-remove` lancé avant lui
(`seed.py:688-694`). `seed replace` n'est pas atteint (r4).

### 1.4 D37 : greffon déclaré dont le clone a disparu

Clone `depots/lepton/library-env68lib/master` supprimé par `scripts/supprimer-essai.sh`. Il reste
3 liens cassés, et le répertoire vide `depots/lepton/library-env68lib/`.

| Commande | Code | Message |
| --- | --- | --- |
| `seed status --json` | 1 | entrée `{"name": "library-env68lib", "role": "sans manifeste", "in_seed": true}` ; `missing: ["env68lib"]` ; 3 liens cassés |
| `check` | 1 | `trunk/sys/root/src/lib/env68lib/env68lib.c: lien cassé dans le trunk : lepton graft` |
| `seed remove env68lib` (avec ou sans `--purge`) | 1 | `greffon « env68lib » non greffé` |
| `seed remove library-env68lib` (nom montré par `seed status` et `pickScion`) | 1 | `greffon « library-env68lib » non greffé` |
| `seed add env68lib file://…` | 1 | `lepton@library-env68lib déjà déclaré dans la graine sans être greffé` → `lepton seed remove env68lib, ou scion seed-scion-remove …` |
| `seed replace env68lib` / `library-env68lib` | 1 | `absent de la graine ou non greffé` |
| `graft` | 2 | scion : `…/master/scion est absent` ; trunk rétabli (3062 liens) |
| `scion graft-remove lepton@library-env68lib` | **0** | `retiré : 3 feuilles` ; liste greffée sans l'entrée ; 0 lien cassé ; graine inchangée |
| `scion graft-remove --purge …` | 1 | `… n'est pas un clone git ; --purge refusé` ; rien de changé |
| après `graft-remove` : `seed remove env68lib` | 1 | `non greffé` |
| après `graft-remove` : `seed add` | 1 | `déjà déclaré …` |

Constats :
- `key_of` ne lit que les manifestes des clones présents (`rootstock.py:352`), d'où le message
  `non greffé` ;
- `scion graft-remove` sans `--purge` retire bien un greffon sans clone (liens cassés compris) :
  le retrait par lepton peut s'y appuyer ;
- l'extension propose `library-env68lib` (`pickScion`, `commands.ts:72-80` : `label` = `name` de
  `seed status`), qui est le suffixe de la clé.

## 2. PA-123 (2026-11-23) — décisions de l'utilisateur

- **D29** : `expand_user` (forme d'ENV-63) pour les 3 chemins.
  - `mkconf import` : le chemin développé suit la règle « absolu sous le trunk → ramené au trunk,
    sinon refus ».
  - `seed new --mkconf` : `~` et l'absolu sont développés, puis ramenés au futur `<-C>/trunk`
    avant le contrôle du schéma. Hors de ce trunk : refus par un message clair (« relatif au
    trunk attendu »), au lieu du motif.
- **D30** : un `--clangd` relatif qui contient un `/` est rendu absolu depuis le répertoire
  courant. Un nom sans `/` reste cherché dans le PATH.
- **D32** : ordre inversé dans `seed remove`, `graft-remove` d'abord, puis `seed-scion-remove`.
  `seed replace` est inchangé.
- **D37** : `seed remove` admet un greffon déclaré sans clone.
  - Noms acceptés : le nom de la graine et le suffixe de clé.
  - Opérations : `scion graft-remove` sans `--purge` (`--purge` sans objet, signalé), puis
    `seed-scion-remove`, puis retrait de la ligne de `lepton-graine.json`.
  - Le message de `seed add` est inchangé.
  - `seed replace` est refusé : « clone absent : lepton seed remove, puis lepton seed add ».
  - L'extension est inchangée.
- **Tests, `README.md`** : proposition de la session, sans objection de l'utilisateur.
  - Tests pytest dans les fichiers existants, avec les formes `D21_FORMS`.
  - `README.md` inchangé, sauf la phrase d'usage de `seed new --mkconf`.

## 3. Corrections (`devenv/env-68`)

Tests écrits d'abord. Chaque nouveau test a échoué sur le code de `main` pour la cause visée ; les
formes inchangées passaient déjà.

| Commit | Objet | Tests ajoutés (modifiés) | En échec sur `main` |
| --- | --- | --- |
| edde54f | D29, D30 | 19 (1) | 17 |
| 80ed13b | D32 | 3 | 3 |
| 9051000 | D37 | 6 | 5 (le 6ᵉ, greffon du projet non admis, garde une forme inchangée) |

**D29, D30 (edde54f)**
- `cli.py` : `check FILE` lit `expand_user(name, "FILE")`.
- `seed.py` :
  - `import_mkconf` développe `~` (`expand_user(reference, "XML")`), puis applique la même règle
    « absolu sous le trunk » ;
  - `_new_mkconf` : `seed new --mkconf` développe `~` ; un absolu sous `<-C>/trunk` (chemin
    absolu ou résolu) est ramené à ce trunk avant le contrôle du schéma ; sinon, refus
    `--mkconf « … » hors du trunk … du rootstock à créer`, « chemin relatif au trunk attendu ».
    Le relatif est inchangé.
- `generate.py` : `find_clangd` rend absolu (`os.path.abspath`) un chemin qui contient un `/`.
- Aide de `--mkconf` : « (ou absolu sous le trunk de -C) ». `README.md` inchangé : il ne dit pas
  la forme du chemin.
- Tests :
  - `test_milestone1.py` : `test_d29_check_file_*` ;
  - `test_project_mkconf.py` : `test_d29_mkconf_import_*`, `test_d29_seed_new_mkconf_*` ;
  - `test_generate.py` : `test_d30_*`. `test_d21_find_clangd_tilde[relatif]` attend désormais
    un absolu.

**D32 (80ed13b)**
- `seed_remove` lance `graft-remove` (avec `--purge` le cas échéant), puis `seed-scion-remove`.
- `scion remove` passe par la même fonction.
- Test `test_milestone3.py::test_d32_*` :
  - causes : modification non commitée, commit local, origine locale ;
  - état comparé octet pour octet : fichiers de `.scion/`, liste greffée, liens ;
  - relance après nettoyage.

**D37 (9051000)**
- `seed.py:declared_without_clone(rs, name)` repère un greffon déclaré sans manifeste lisible :
  - désigné par son nom de graine ou par le suffixe de sa clé ;
  - clés de type famille, BSP, application ou bibliothèque seulement : ni le greffon du projet,
    ni `original::tree`, ni `building` ;
  - deux candidats donnent un refus.
- `seed_remove`, pour un tel greffon :
  - avertit : `<nom> (<clé>) : clone absent, déclaration retirée de la graine`, plus
    `; --purge sans objet` le cas échéant ;
  - lance `graft-remove` sans `--purge` si l'entrée est greffée, puis `seed-scion-remove` ;
  - retire la ligne de `lepton-graine.json`, et le `<bin>` d'une application.
- `seed replace` refuse : `clone absent, remplacement impossible` →
  `lepton seed remove <g>, puis lepton seed add <g> LOCATION`.
- `seed add` est inchangé : le renvoi qu'il donne devient juste.
- Tests `test_d37_*` :
  - nom et suffixe, puis réajout ;
  - application avec `--purge` ;
  - entrée déjà dégreffée ;
  - `seed replace` refusé ;
  - greffon du projet non admis.

`pytest` complet : **616** verts (588 au départ). lepton réinstallé au Mac par
`pipx install --force ~/lepton-tools-dev/lepton-tools`, depuis 9051000 : 18 modules du venv
identiques à la branche, relevés hors du dépôt (`python -I`).

## 4. Contrôles (lepton installé depuis 9051000)

### 4.1 Table D29, D30 rejouée (`env-68-lepton/apres/`)
Comparé à `avant/`, les lignes visées suivent le PA-123 et toutes les autres sont identiques.
- c1-t, c1-u, c2-t (`check FILE` en `~`) : code 0, « conforme ». c1-x : `FILE « ~inconnu68/… » :
  répertoire personnel de « ~inconnu68 » introuvable`.
- m1-t, m1-u (`mkconf import` en `~`, sous le trunk) : code 0, XML du projet importé.
  - m1-x : message d'`expand_user`.
  - m1-th (`~` vers le clone) : `hors du trunk …`, comme m1-h.
  - m1-rc (relatif au répertoire courant) : toujours refusé, car le relatif est relatif au trunk.
- n1-t, n1-u, n1-a, n1-d (`seed new --mkconf` en `~` ou absolu sous `<-C>/trunk`) : code 0,
  rootstock créé, XML importé. n1-x : message d'`expand_user`, rien n'est créé.
- p6-r, p6-rs, p6-rw, p6-rd (`--clangd` relatif, avec un répertoire courant quelconque) :
  `clangd.path` absolu, qui se résout depuis la racine.
- Chaque cas laisse son rootstock égal à son départ, sauf les imports réussis (liens et graine,
  attendus).

### 4.2 D32, D37 rejoués (`env-68-lepton/apres-graine/`)
Séquence de `graine.sh` redécoupée après correction : une copie par retrait (g1, g3, g4, g5), et
la conséquence `file remove` dans un cas à part (r6). Le relevé `avant-graine/` (séquence de
l'audit) reste la référence de l'état d'avant. Les états sont comparés à « ajouté », c'est-à-dire
après `seed add`.

| Cas | Code | État |
| --- | --- | --- |
| r1, r2, r5 `--purge` refusé (modification, commit local, origine locale) | 2 | **= ajouté** (graine, `lepton-graine.json`, liste greffée, liens) |
| r1 relance après nettoyage | 0 | **= départ**, sans « hors de la graine » |
| r6 `file remove` après un `--purge` refusé | 0 | accepté (graine cohérente) |
| r3 sans `--purge`, r4 `seed replace` | 0, 2 | inchangés |
| g1 `seed status`, `check`, `graft` sans clone | 1, 1, 2 | inchangés (constats) |
| g1 `seed add` | 1 | `déjà déclaré …` → `lepton seed remove env68lib` (renvoi juste) |
| g1 `seed replace` (nom ou suffixe) | 1 | `clone absent, remplacement impossible` → `lepton seed remove env68lib, puis lepton seed add env68lib LOCATION` ; état inchangé |
| g1 `seed remove env68lib`, puis `seed add` | 0, 0 | retrait : liens cassés retirés ; réajout = ajouté |
| g3 `seed remove library-env68lib` | 0 | retrait complet |
| g4 `seed remove env68lib --purge` | 0 | `… clone absent, déclaration retirée de la graine ; --purge sans objet` |
| g5 après `scion graft-remove` : `seed remove`, puis `seed add` | 0, 0 | retrait, puis réajout |

Après chaque retrait sans clone, l'état diffère du départ par un seul point : le répertoire vide
`depots/lepton/library-env68lib/`. Il est laissé par la suppression du clone `…/master` hors de
lepton ; lepton ne le crée pas, et un réajout le réutilise. Les liens cassés sont égaux au départ.

### 4.3 D21 inchangé (`env-63-tilde/chemins.sh`, relevés `env-68-lepton/d21/`)
Comparaison avec `env-63-tilde/apres/` : 9 écarts sur 289 fichiers, tous expliqués.
- c1-t (`check FILE`) : code 0, conforme (D29).
- p6-r (`clangd.path` absolu, D30) :
  - `.out` « inchangé », car les cas a et d qui le précèdent ont écrit le même chemin ;
  - `.cmd` : nom de phase.
- p2-r, p3-r, p4-r `.cmd` : nom de phase (`cibles-d21`) dans le chemin relatif.
- `resume.tsv` : ligne c1-t.

### 4.4 D17 inchangé (`env-59-tilde/essai.sh`, relevés `env-68-lepton/d17/`)
Dépôt présent `<E>/d17-depot` (`env59lib`, `scion new --no-seed`), absent `<E>/d17-absent`.
Comparaison avec `env-63-tilde/d17/` (547 fichiers) : 82 écarts bruts. Après normalisation, il en
reste 12, étrangers à lepton :
- normalisation :
  - noms d'essai `env-63-essai` → `env-68-essai` ;
  - commits (noyau 2b4a647 depuis ENV-65, dépôt `<P>` recréé) ;
  - 18 `*-remove.err` : mêmes lignes dans un autre ordre (D32 : `graft-remove`, puis
    `seed-scion-remove`) ;
- 12 `a*-i.err` restants : scion 0.6.3.3 (D22, ENV-65), `git clone -b master --quiet` et
  première ligne non vide du message de git.

Tous les `.etat` sont égaux au départ.
