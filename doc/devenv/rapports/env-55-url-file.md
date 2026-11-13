# ENV-55 — lepton : URL `file:///` reconnue (D13) — rapport

Branche lepton-tools `devenv/env-55` (depuis `main` 7d55bf1). lepton 0.1.0, scion 0.6.3.0,
git 2.50.1 (Apple Git-155). Constat d'origine : O-1 de `rapports/env-53-mac.md` §1.5 ; D13 de
`HORS-PLAN.md`.

Notations des relevés : `<C>` rootstock d'essai `~/lepton-tools-dev/essais/env-55-essai`, `<P>`
dépôt présent `~/lepton-tools-dev/essais/env-55-depot`, `<A>` dépôt absent
`~/lepton-tools-dev/essais/env-55-absent.git`, `<HOME>` `/Users/cle_d_anton`. Ainsi
`file://<P>` se lit `file:///Users/…/env-55-depot` (trois barres).

## 1. Comportement avant correction

### 1.1 Méthode

- Code lu : `lepton/seed.py` (`_ORIGIN` l. 35, `Origin.remote` l. 66-67, `parse_location` l. 73-104,
  relectures l. 698, 706, 747, 865), `lepton/scions.py:166`, `extension/src/commands.ts` ;
  scion : `mirror.py:37` (`is_remote`), `graft.py` (l. 47, 117, 137, 744), `cli.py` (l. 104, 184),
  `seed.py:63`, `rootstock.py:62` (`resolve`), `gitops.py:61` (`clone`).
- Classement mécanique : `env-55-url-file/classer.py`, lancé par l'interpréteur pipx de lepton,
  `is_remote` par celui de scion ; 8 formes × 2 cibles (présent, absent) × 6 variantes = 96 lignes,
  `env-55-url-file/avant/classer.tsv`. Rien n'est écrit.
- git seul : `env-55-url-file/git-formes.sh` (`git ls-remote`, ssh neutralisé),
  `avant/git-formes.tsv`.
- Essai : `env-55-url-file/essai.sh` sur `<C>`, `rsync -a` d'`essais/env-11/qemu` sans `build/`
  (graine de projet `env11`, QEMU). Dépôt présent `<P>` : greffon `bibliotheque` `env55lib` créé
  par `lepton scion new env55lib --type bibliotheque --repo <P> --no-seed --no-cmake` (un commit
  2f3e70d sur `master`, `scion/sys/root/src/lib/env55lib/`). Relevés par
  `env-51-messages/releve.sh` dans `avant/` (`.cmd`, `.out`, `.err`, `.code`) ; état comparé au
  départ après chaque cas par `env-55-url-file/etat.sh` (`<cas>.etat`).
- État de départ de `<C>` : 3059 liens, 0 cassé, 0 fichier régulier ; `lepton check` code 0 ; graine
  propre (HEAD 124db52). Répertoire vide préexistant : `depots/origin/scion/sources`.

### 1.2 Classement par forme (variante nue)

| Forme | lepton `parse_location` | `Origin.remote` / scion `is_remote` de la valeur | git (`ls-remote <P>`) | `seed add` absent | `seed add` présent |
| --- | --- | --- | --- | --- | --- |
| `file:///abs` | chemin local `<cwd>/file:/abs` → « absent » | — (refusé avant) ; scion seul : `False`, chemin `<C>/file:/abs` | 0 (lu) | a01 : 1, « `<C>/file:<A>/scion` absent » | p01 : 1, même message |
| `file://localhost/abs` | URL, `master` | `True` / `True` | 0 | a02 : 2 (échec de `git clone`, ajout annulé) | p03 : 0, clone `depots/lepton/library-env55lib/master` |
| `file:/abs` | chemin local → « absent » | — | 128 (lu comme `hôte:chemin` ssh, hôte `file`) | a03 : 1 | p07 : 1 |
| `file://autre/abs` | URL, `master` | `True` / `True` | **0 : git ignore l'hôte** et lit `/abs` local | a04 : 2 | p04 : 0 (clone du dépôt local) |
| `FILE:///abs` | chemin local → « absent » | — | 128 (`remote-FILE` inconnu : schéma sensible à la casse) | a05 : 1 | p06 : 1 |
| `FILE://localhost/abs` | URL, `master` | `True` / `True` | 128 (`remote-FILE`) | a06 : 2 (échec de `git clone`) | p05 : 2 (échec de `git clone`) |
| chemin absolu | local, `*` (en place) | `False` / `False` | 0 | a07 : 1, « absent » | p08 : 0, en place, emplacement absolu |
| chemin relatif | local, `*`, rendu absolu (hors rootstock) | `False` / `False` | — | a08 : 1 | p09 : 0, emplacement absolu |

Après chaque cas, et après le `seed remove` de chaque ajout réussi (`--purge` pour un clone fait
par scion) : liens, liens cassés, fichiers réguliers, graine, liste greffée et `depots/` égaux au
départ. Seule exception : chaque échec de `git clone` (a02, a04, a06, a10, p05) laisse
`depots/lepton/library-<nom>` vide (D14), retiré par `rmdir` et noté dans le `.etat` du cas.

`file://127.0.0.1/abs` et `file://LOCALHOST/abs` sont lus par git comme `file://localhost/abs`
(`avant/git-formes.tsv`).

### 1.3 Variantes

`avant/classer.tsv`, colonnes `re.*` (groupes de `_ORIGIN`), `u.*` (`urlparse`), `lepton`,
`message` :
- `_ORIGIN` sépare correctement `@VERSION` et `:PATH` dans toutes les formes, autorité vide
  (`file:///`) comprise : `loc` reste `file:///abs`, `ver` et `path` sont pris en fin.
- Forme URL (`netloc` non vide) : `@master`, `:sous`, `--version`, `--path` repris tels quels.
- Forme lue comme chemin (`file:///`, `file:/`, `FILE:///`, chemins) : `@VERSION` ou `--version`
  → « version « master » sans effet (scion utilise un répertoire local en place) », sinon
  « `<stem>` absent ».
- **Indice faux** (l. 93) : pour `file:///abs@master`, l'action proposée est
  `file://localhost<C>/file:<P>@master` (a09, p02) : `Path(loc).resolve()` d'une URL. Pour un
  chemin, l'indice est juste (`file://localhost<P>@master`).

### 1.4 scion seul, `file:///` transmis tel quel (s01 à s05)

`scion seed-scion-add --seed depots/lepton-seed/env11 lepton@library-env55lib master file://<P>` :
code 0, déclaré. `scion seed-clone` : code 1, « `<C>/file:<P>/scion` est absent. Vérifiez la
colonne « chemin dans le dépôt » ». `graft --scion` et `graft-remove` : code 1, « absent de la
liste greffée ». `seed-scion-remove` : code 0 ; état égal au départ.

scion classe donc `file:///abs` comme lepton : chemin local, résolu contre le rootstock
(`rootstock.resolve`, `Path("file:///abs")` → `file:/abs` relatif). Une forme `file:///` acceptée
par lepton et transmise telle quelle échouerait dans scion.

### 1.5 Relectures d'une origine enregistrée

| Endroit | Usage | Classement |
| --- | --- | --- |
| `seed replace` l. 698, 706 | `--purge` du `graft-remove` si l'origine ancienne (ou nouvelle, à l'annulation) est distante | `Origin.remote` |
| `seed lock`, `_locked_entries` l. 747 | répertoire hors git admis seulement pour une origine locale | `Origin.remote` |
| `seed lock --restore`, `_restore` l. 865 | origine locale signalée, jamais déplacée ; distante remise au commit figé | `Origin.remote` |
| `seed status` (l. 480, 531), `seed new` (affichage l. 415) | affichage de l'emplacement | aucun |
| `check`, `generate`, `file …` | ne lisent pas l'emplacement | aucun |
| `scion new` (`scions.py:166`) | `parse_location(str(repo))` : toujours un chemin | inchangé |

Les emplacements écrits dans la graine sont ceux que rend `parse_location` ; `Origin.remote` et
`is_remote` de scion appliquent le même test (`netloc` non vide) à la même valeur : lepton et scion
classent aujourd'hui toute origine enregistrée de la même façon.

### 1.6 Effets

- Extension : `seedAdd` / `seedReplace` transmettent l'origine saisie telle quelle (aucun contrôle
  en TypeScript) avec `--version master` par défaut (`originOptions`). Une origine `file:///` y
  aboutit au message « version « master » sans effet », avec l'indice faux du §1.3 (a09, p02).
- `README.md` et `rapports/env-8-interface.md` ne décrivent pas les formes d'URL ; l'aide de la CLI
  dit « URL git[@VERSION][:PATH] ou répertoire local ». Rien n'y devient faux.

## 2. PA-97 (2026-11-13, décisions de l'utilisateur)

| Question | Décision |
| --- | --- |
| Forme `file:///abs` | normalisée par lepton en `file://localhost/abs` avant écriture dans la graine ; scion et l'extension inchangés |
| `file:/abs`, schéma en majuscules | même traitement : schéma `file` reconnu sans tenir compte de la casse, réécrit `file` ; sans hôte → `localhost` |
| `file://<autre hôte>/abs` | inchangé (accepté ; git ignore l'hôte, §1.2) |
| Tests | `tests/test_milestone3.py`, à côté de `test_gra3_parse_location` |

Conséquence de conception : la normalisation ne s'applique qu'à la saisie (`parse_location`). Le
classement, lui, reste le test de scion (`netloc` non vide), appliqué par une seule fonction à la
saisie normalisée comme aux emplacements relus dans la graine (`Origin.remote`). Une graine écrite
à la main avec `file:///abs` reste donc lue comme un chemin par lepton, comme par scion.

## 3. Correction (`devenv/env-55`)

| Commit | Contenu |
| --- | --- |
| 71fba49 | `tests/test_milestone3.py` : 17 tests (`test_d13_*`), écrits avant la correction |
| 6b6470b | `lepton/seed.py` : `_FILE_URL`, `normalize_location`, `is_url` ; `parse_location` normalise la saisie puis classe par `is_url` ; `Origin.remote` = `is_url` |
| f5144d6 | `env-55-url-file/essai.sh` : `--purge` choisi d'après le clone fait par scion (les formes désormais lues comme URL font un clone) ; rejoué « avant » avant la réinstallation : relevés identiques au premier passage |

Normalisation (`_FILE_URL`, `^file:(?://(?P<host>[^/]*))?(?P<path>/.*)$`, casse ignorée) :
`file:///abs`, `file:/abs`, `FILE:///abs`, `File:/abs` → `file://localhost/abs` ; `FILE://h/abs` →
`file://h/abs` (hôte conservé). Toute autre valeur est rendue telle quelle : `file://localhost/…`,
`file://autre/…`, `https://…`, `ssh://…`, chemins, et `file:x` (sans « / » : chemin `file` suivi de
`:PATH`, comme avant). Le découpage `@VERSION` et `:PATH` par `_ORIGIN` précède la normalisation
et ne change pas.

Message de la l. 91-93 (« version sans effet », indice `file://localhost<chemin>@<version>`) : non
modifié. Les formes `file:` n'y arrivent plus ; pour un chemin, l'indice était déjà juste (§1.3), à
l'exception du constat O-1 (§6). `README.md` : rien à modifier (§1.6). Extension : aucun changement
(origine transmise telle quelle).

Tests (`tests-avant-correction.txt`) : avant la correction, 11 échecs (les 9 formes normalisées
de `test_d13_file_url_normalized`, les 2 `test_d13_seed_add_file_url`) et 6 réussites (garde des
formes inchangées). Après : 17 réussites ; `pytest` complet **453 verts** (436 à ENV-54 + 17),
`~/lepton-tools-dev/venv-lepton-tools/bin/pytest`, 504 s.

lepton réinstallé depuis la branche : `pipx install --force ~/lepton-tools-dev/lepton-tools`
(règle `allow`), lepton 0.1.0, `normalize_location` présent dans l'interpréteur pipx.

## 4. Contrôles : table du §1 rejouée (`apres/`)

Même script (`essai.sh`, f5144d6), même rootstock d'essai, même état de départ (3059 liens,
graine 8a6a9d74d306). Comparaison fichier par fichier de `avant/` et `apres/` :

| Cas | Avant | Après | Conforme au PA-97 |
| --- | --- | --- | --- |
| a01 `file:///A`, a03 `file:/A`, a05 `FILE:///A`, a09 `file:///A --version master` | 1 (« `<C>/file:<A>/scion` absent » ; a09 : « sans effet » à indice faux) | 2, relevés **identiques à a02** (`file://localhost<A>`) : échec de `git clone`, ajout annulé, D14 | oui |
| a06 `FILE://localhost/A` | 2, `remote helper 'FILE' aborted session` | 2, identique à a02 (`git clone file://localhost<A>`) | oui |
| p01 `file:///P`, p02 `+ --version master`, p06 `FILE:///P`, p07 `file:/P` | 1 | 0, relevés **identiques à p03** (`file://localhost<P>`) : `.out`, `.err`, `seed status --json`, `check`, `remove --purge`, état | oui |
| p05 `FILE://localhost/P` | 2 (`remote-FILE`) | 0, identique à p03 | oui |
| a02, a04, a07, a08, a10, p03, p04, p08, p09, p10 | — | octet pour octet identiques à l'avant | inchangé |
| s01 à s05 (scion seul, `file:///` transmis tel quel) | — | identiques à l'avant (scion inchangé) | inchangé |
| `classer.tsv` | 96 lignes | seules diffèrent les lignes `file:///`, `file:/`, `FILE:` (colonnes `lepton`, `remote`, `location`, `version`, `subpath`, `message`, `scion.is_remote(écrit)`) | oui |
| `git-formes.tsv` | — | identique | — |

Après chaque cas, et après chaque annulation : liens, cassés, réguliers, graine, liste greffée et
`depots/` égaux au départ (les `.etat` ne diffèrent que par les `rmdir` de D14, présents dès qu'un
`git clone` échoue, donc aussi pour les formes normalisées en échec).

## 5. Extension

Code : `seedAdd` lance `seed add <nom> <origine> --type <type> --version <v>` (`master` par défaut,
`originOptions`), sans contrôle de l'origine en TypeScript ; `seedRemove` lance `seed remove <nom>`.
La correction n'y change rien.

Commandes rejouées en ligne de commande, telles que les lance l'extension (`apres/x01`, `x02`) :
- x01 `lepton seed add env55lib file://<P> --type bibliotheque --version master` (sans
  `--no-cmake`) : code 0, `env55lib ajouté (lepton@library-env55lib, master, file://localhost<P>)`,
  2 lignes `scion:` ;
- x02 `lepton seed remove env55lib` : code 0 ; clone `depots/lepton/library-env55lib/master`
  conservé (comportement de `seed remove` sans `--purge`, identique pour `file://localhost/`),
  retiré ensuite par `scripts/supprimer-essai.sh` ; état final = départ, `lepton check` code 0,
  graine propre.

Essai dans VSCodium (PA-98 : fait par l'utilisateur, 2026-11-13), `apres/vscodium-canal.txt` :
espace de l'essai régénéré d'abord par `lepton generate` (l'`env11.code-workspace` copié visait
`essais/env-11/qemu/build/.active`) ; `CMakeUserPresets.json` « inchangé », graine inchangée.
Extension 0.5.2. « ajouter un greffon à la graine » avec `file://<P>` (trois barres), version
`master` : notification « terminé », canal identique à x01 (`env55lib ajouté (…, master,
file://localhost<P>)`, 2 lignes `scion:`, `→ code 0`) ; 3 appels `seed status --json` code 0 ;
« retirer » : « terminé », identique à x02. État après : liens, graine, liste greffée = départ ; clone
conservé (sans `--purge`), comme x02.

## 6. Constats hors périmètre

- **O-1** : l'indice du message « version sans effet » (l. 110 après ENV-55) calcule
  `Path(loc).resolve()` sans `expanduser()`, alors que le contrôle d'existence (l. 111) le fait.
  Une origine `~/…@master` transmise sans shell (saisie dans l'extension) donne l'indice
  `file://localhost<cwd>/~/…@master`. Forme non `file:`, laissée inchangée (iso-fonctionnel) ;
  reportée dans `HORS-PLAN.md` en D17 (PA-98).
- `file://<autre hôte>/abs` reste accepté et git lit le chemin local (PA-97) ; un dépôt de même
  chemin sur un autre hôte n'est donc jamais atteint.
