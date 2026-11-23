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
