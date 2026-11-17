# ENV-59 — lepton : `~` dans l'indice « version sans effet » (D17) — rapport

Branche lepton-tools `devenv/env-59` (depuis `main` 2db6760). lepton 0.1.0 (pipx, code identique
à `main` : `seed.py`, `rootstock.py`, `files.py`, `scions.py`, `cli.py`, `errors.py` comparés),
scion 0.6.3.1, Claude Code 2.1.326. Constat d'origine : O-1 de `rapports/env-55-url-file.md` §6 ;
D17 de `HORS-PLAN.md`.

Notations : `<C>` rootstock d'essai `~/lepton-tools-dev/essais/env-59-essai`, `<P>` dépôt présent
`~/lepton-tools-dev/essais/env-59-depot`, `<A>` dépôt absent `~/lepton-tools-dev/essais/env-59-absent`,
`<W>` répertoire de travail vide `~/lepton-tools-dev/essais/env-59-cwd`, `<HOME>` le répertoire
personnel, `~<U>` le tilde suivi du nom de l'utilisateur.

## 1. Comportement avant correction

### 1.1 Méthode

- Code lu : `lepton/seed.py` (`parse_location` l. 89-120 : refus l. 107-110, indice l. 110,
  chemin local l. 111) ; appelants l. 375-377 (`seed new`), 618 (`seed add`), 711
  (`seed replace`), `scions.py:166` (`scion new`) ; `extension/src/commands.ts`
  (`seedAdd`, `seedReplace`, `originOptions`), `runner.ts`, `lepton.ts` (`spawn` sans shell).
- Classement : `env-59-tilde/classer.py` (repris d'`env-55-url-file/classer.py`), lancé par
  l'interpréteur pipx de lepton (`-I`), répertoire courant `<C>`. Formes : `~/…`, `~<U>/…`,
  relative, absolue, puis les deux formes `~` développées par bash (mot non cité,
  `bash -c "printf '%s' ~/…"`), et `~inconnu59/…` (utilisateur sans compte, §1.5) ; chacune nue,
  avec `@master`, avec `--version master` ; dépôt présent et absent : 42 lignes,
  `avant/classer.tsv`. L'origine est passée telle quelle, comme
  par un appel en liste (forme de l'extension). Pour chaque indice, l'URL est relue par
  `parse_location` et son chemin comparé au dépôt visé (colonne `indice→dépôt`).
- Essai : `env-59-tilde/essai.sh` (repris d'`env-55-url-file/essai.sh`) sur `<C>`, copie par
  `rsync -a` d'`essais/env-11/qemu` sans `build/` (graine de projet `env11`, QEMU). Dépôt présent
  `<P>` : greffon `bibliotheque` `env59lib`, créé par `lepton scion new env59lib --type
  bibliotheque --repo <P> --no-seed --no-cmake` (un commit 536b886 sur `master`). Mêmes 42 formes
  par `lepton seed add` (cas p01-p21, a01-a21), origine entre guillemets ; chaque indice affiché
  est suivi tel quel (cas `<nom>-i`). Relevés par `env-51-messages/releve.sh` (`.cmd`, `.out`, `.err`, `.code`) ; ajout
  réussi annulé par `seed remove` (`--purge` si scion a cloné) ; état comparé au départ après
  chaque cas par `env-55-url-file/etat.sh` (`<cas>.etat`). Relevés bruts sous
  `essais/env-59-releves/`, normalisés dans `env-59-tilde/avant/`.
- État de départ de `<C>` : 3059 liens, 0 cassé, 0 fichier régulier ; `lepton check` code 0 ;
  graine propre (HEAD 124db52).
- Deux passages (`essais/env-59-releves/avant`, puis `avant-2` après l'ajout de `~inconnu59`) :
  les 469 relevés communs (`.cmd`, `.out`, `.err`, `.code`, `.etat`) sont identiques octet pour
  octet ; `avant/` versionné est celui du second passage (70 cas, 112 commandes).
- Autres chemins : `env-59-tilde/autres.sh`, §1.4.

### 1.2 `parse_location` et `seed add` par forme

Origine transmise telle quelle (appel en liste, extension). Codes de `seed add` ; `<forme>` dans
un indice : chemin rendu par `Path(loc).resolve()`.

Dépôt présent `<P>` :

| Forme | nue | `@master` | `--version master` |
| --- | --- | --- | --- |
| `~/…` | p01 : 0, en place, emplacement `<P>` | p02 : 1, « sans effet », indice **`file://localhost<C>/~/…@master`** (faux) | p03 : 1, même indice faux |
| `~<U>/…` | p04 : 0, `<P>` | p05 : 1, indice **`file://localhost<C>/~<U>/…@master`** (faux) | p06 : 1, même indice faux |
| relative (`../env-59-depot`) | p07 : 0, `<P>` | p08 : 1, indice `file://localhost<P>@master` (juste) | p09 : 1, indice juste |
| absolue | p10 : 0, `<P>` | p11 : 1, indice juste | p12 : 1, indice juste |
| `~/…` développé par bash | p13 : 0 | p14 : 1, indice juste | p15 : 1, indice juste |
| `~<U>/…` développé par bash | p16 : 0 | p17 : 1, indice juste | p18 : 1, indice juste |
| `~inconnu59/…` | p19 : 1, **trace Python** `RuntimeError` (§1.5) | p20 : 1, indice `file://localhost<C>/~inconnu59/…@master` | p21 : 1, même indice |

Dépôt absent `<A>` : même partage. Sans version, « `<A>/scion` absent » (a01, a04 : le chemin du
message est développé, `~` compris) ; avec version, le refus « sans effet » vient avant le contrôle
d'existence (piège du fichier d'étape), avec les mêmes indices que pour `<P>` (a02, a03, a05, a06
faux ; a08 à a18 justes) ; `~inconnu59/…` : a19 trace, a20 et a21 indice.

Les formes développées par bash donnent exactement les lignes de la forme absolue (p13-p18 =
p10-p12, a13-a18 = a10-a12) : D17 ne se reproduit qu'avec `~` transmis tel quel.

Après chaque cas, et après le `seed remove` de chaque ajout réussi : liens, liens cassés, fichiers
réguliers, graine, liste greffée et `depots/` égaux au départ (`avant/*.etat`) ; aucun répertoire
laissé par un clonage en échec (D14, scion 0.6.3.1).

### 1.3 Indice suivi tel quel (cas `-i`)

- Indice juste (p08-i, p09-i, p11-i, p12-i, p14-i, p15-i, p17-i, p18-i) : code 0, clone fait par
  scion (`depots/lepton/library-env59lib/master`), graine `file://localhost<P>` `master` ;
  `seed remove --purge` rend l'état de départ.
- Indice faux (p02-i, p03-i, p05-i, p06-i, p20-i, p21-i ; a02-i, a03-i, a05-i, a06-i, a20-i,
  a21-i) : code 2,
  « échec de « git clone file://localhost<C>/~/… » (code 128) : and the repository exists. »,
  ajout annulé (graine et trunk restaurés).
- Indice juste d'un dépôt absent (a08-i, a09-i, a11-i, a12-i, a14-i, a15-i, a17-i, a18-i) :
  code 2, même échec de `git clone`, attendu.

### 1.4 Autres chemins saisis sans `expanduser()`

`env-59-tilde/autres.sh`, `~` non développé, relevés `autres/` ; `<C>` égal au départ et clones de
`<C>` inchangés après chaque cas (`autres/*.etat`).

| Cas | Chemin (code) | Commande | Résultat | Extension |
| --- | --- | --- | --- | --- |
| o1 | `-C DIR` (`rootstock.py:226`) | `check -C '~/…/env-59-essai'` | 1 : « `<W>/~/…/env-59-essai` n'est pas un rootstock » ; o1d (développé) : 0 | non transmis |
| o2 | `seed new -C DIR` (`seed.py:369`), `--seed-repo DIR` (`seed.py:372`) | `seed new env59new -C '~/…/env-59-new' --seed-repo '~/…/env-59-graine'` | **0** : rootstock et graine créés sous **`<W>/~/lepton-tools-dev/essais/`** (répertoire nommé `~` dans le répertoire courant), 3055 + 3 feuilles greffées ; rien sous `essais/` | non transmis |
| o3 | `scion new --repo DIR` (`scions.py:125`) | `scion new env59repo --repo '~/…/env-59-repo' --no-seed` | **0** : dépôt créé sous `<W>/~/…/env-59-repo` | non transmis (`scionNew` sans `--repo`) |
| o4 | `_locate` (`files.py:94`) | `file owner '~/…/trunk/CMakeLists.txt'` | 1 : « ni dans le trunk `<C>/trunk`, ni dans un greffon greffé » ; o4d : 0, `owned` | **transmis** : chemin saisi de `file add`, `dir add`, destination de `file mv`, cible saisie de `file remove` |
| o5 | `_locate` | `file add '~/…/trunk/sys/root/src/lib/env59-nouveau.c'` | 1, même message, rien d'écrit | transmis (même voie) |
| o6 | `--clangd PATH` (`generate.py:117`, hors liste du fichier d'étape) | `generate --clangd '~/…/outils/clangd'` (lien vers `clangd-mp-21`) | 1 : « --clangd « ~/… » introuvable », rien d'écrit | non transmis (`generate` sans option) |
| o7 | `parse_location` par `seed new --origin` | tapé dans zsh, non cité : `--origin qemu-mps2=~/…/family-qemu-mps2/master@master` | 1 : « sans effet », indice **`file://localhost<W>/~/…@master`** (D17 au terminal) | — |
| o8 | `-C DIR` | tapé dans zsh : `check --rootstock=~/…/env-59-essai` | 1 : « `<W>/~/…` n'est pas un rootstock » | — |

Le shell ne développe pas `~` après un « = » dans ces formes (relevé §1.6) : `NOM=~/…` dont le nom
porte un tiret (`qemu-mps2`, `lepton-noyau`), `--option=~/…`. D17 et les cas o1-o3 se
reproduisent donc aussi au terminal, sans apostrophes. Avec `-C ~/…` ou `--seed-repo ~/…`
(espace), le shell développe et rien de cela n'arrive.

Gravité relevée : o2 et o3 réussissent (code 0) en créant l'arborescence au mauvais endroit, sans
message ; o1, o4 à o8 refusent avec un message qui montre le chemin pris.

### 1.5 Forme `~<utilisateur inconnu>/…`

`Path("~inconnu59/x").expanduser()` lève `RuntimeError: Could not determine home directory.`,
non convertie en `LeptonError` : sans version, `seed add` affiche une trace Python (p19, a19,
code 1). Avec version, le refus survient avant `expanduser()` et l'indice garde `~inconnu59`
(p20, a20). Calculer l'indice par la même expression que le contrôle d'existence ferait passer
p20, p21, a20, a21 du message à la trace : question 2 du §2.

### 1.6 Observations

- Développement du tilde par le shell (bash 5.3.20 MacPorts, premier dans le PATH, celui des
  scripts ; `/bin/bash` 3.2.57 ; zsh 5.9, shell de l'utilisateur ; mêmes résultats) :
  `--origin qemu-mps2=~/x` et `--rootstock=~/y` → `~` laissé ; `-C ~/w` → développé ; bash
  développe `lepton_noyau=~/x` (nom valide de variable), zsh non (sauf `magic_equal_subst`).
- **O-1** (scion, hors D17) : le message d'échec de `git clone` ne garde que la dernière ligne de
  git (« and the repository exists. ») ; la cause (« fatal: '…' does not appear to be a git
  repository ») est perdue. Déjà vu en ENV-53 (C5) et ENV-56 (§3), absent de `HORS-PLAN.md`.
- **O-2** (extension, lu, non essayé) : le réglage `lepton.path` est passé tel quel à `spawn`
  (`resolveLepton`, `lepton.ts:22`) ; une valeur `~/…` y échouerait (exécutable introuvable).
- `README.md` ne décrit pas l'indice ; ses exemples `-C ~/demo` sont tapés au shell (développés) :
  rien n'y devient faux.
- `depots/lepton/.DS_Store` présent dans la copie, venu de la source `essais/env-11/qemu` (hors
  relevé, `etat.sh` ne liste que les répertoires).

## 2. Questions du PA-105

1. **Portée.** D17 est l'indice de la l. 110 (p02, p03, p05, p06, a02, a03, a05, a06, o7). Les
   autres chemins (§1.4 : o1 `-C`, o2 `seed new -C` et `--seed-repo`, o3 `--repo`, o4-o5
   `_locate`, o6 `--clangd`) sont une seconde variable : les corriger changerait des entrées
   acceptées (o2, o3 réussissent aujourd'hui, au mauvais endroit). Options : les inclure ici, les
   traiter dans une étape à part, les reporter au hors-plan (D21). Proposition : indice seul ici ;
   autres chemins au hors-plan, avec les faits du §1.4 (o2 et o3 créent `<cwd>/~/…` en silence,
   joignables au terminal par `--option=~/…`).
2. **`~<utilisateur inconnu>/…`** (§1.5). Options :
   - (a) même expression que le contrôle d'existence, sans plus : p20, p21, a20, a21 passent du
     message à la trace Python ;
   - (b) même expression, et l'échec de `expanduser()` rendu en `LeptonError` (« origine locale
     « ~inconnu59/… » : répertoire personnel de « inconnu59 » introuvable ») pour toutes les
     variantes : p19 et a19 passent aussi de la trace au message ;
   - (c) indice calculé par `expanduser()`, avec repli sur le chemin non développé s'il échoue :
     toutes les sorties de `~inconnu59` inchangées, mais une logique de chemin en plus.
   Proposition : (b), une seule expression calculée avant le refus et une seule conversion
   d'erreur.
3. **Forme de l'indice** : chemin absolu après `expanduser().resolve()`, comme le contrôle
   d'existence. Pour une origine relative ou absolue, l'indice est inchangé (même résultat que
   `resolve()` seul). Proposition : retenue.
4. **Tests** : `tests/test_milestone3.py`, près de `test_d13_*` :
   - `test_d17_hint_expands_tilde`, paramétré : `~/x@v`, `~/x` + `--version v`,
     `~<utilisateur>/x@v` (indice attendu `file://localhost<répertoire personnel>/x@v`, sans
     accès au disque : le refus précède le contrôle d'existence) ; `HOME` remplacé par
     `monkeypatch` pour `~/` ;
   - `test_d17_hint_followed_by_seed_add` : `seed add` d'une origine `~/…@master` (dépôt de test
     sous un `HOME` de test) refusé, puis l'indice suivi tel quel accepté (clone, graine
     `file://localhost/…`), `seed remove --purge` rendant graine et trunk ;
   - `test_d17_hint_unchanged_for_paths` : relatif et absolu, indice inchangé (passe déjà) ;
   - selon la question 2 : `~inconnu…` nu et avec version.
5. **Observations O-1 et O-2** (§1.6) : à ajouter au hors-plan, ou écartées.

## 3. PA-105 (2026-11-17, décisions de l'utilisateur)

| Question | Décision |
| --- | --- |
| Portée | l'indice seul (D17) ; autres chemins du §1.4 au hors-plan (D21) |
| `~<utilisateur inconnu>/…` | (b) : une seule expression `expanduser().resolve()` calculée avant le refus ; l'échec d'`expanduser()` rendu en `LeptonError`, toutes variantes (p19, a19 : trace → message) |
| Forme de l'indice | chemin absolu après `expanduser().resolve()` ; relatif et absolu inchangés |
| Tests | `tests/test_milestone3.py`, près de `test_d13_*` (§2 point 4) |
| O-1, O-2 | au hors-plan : D22 (scion), D23 (extension) |

## 4. Correction (`devenv/env-59`)

| Commit | Contenu |
| --- | --- |
| b6f571b | `tests/test_milestone3.py` : 9 tests `test_d17_*`, écrits avant la correction ; relevé `env-59-tilde/tests-avant-correction.txt` : 8 échecs, 1 réussite (`test_d17_hint_unchanged_for_paths`, garde des formes inchangées) |
| 74c9c97 | `lepton/seed.py`, `parse_location` : le chemin local `expanduser().resolve()` est calculé une fois, avant le refus « sans effet », et sert à l'indice comme au contrôle d'existence ; l'échec d'`expanduser()` (`RuntimeError`, `~utilisateur` sans compte) devient `LeptonError` « origine locale « … » : répertoire personnel de « ~… » introuvable », action « vérifier le nom qui suit « ~ », ou donner un chemin absolu » ; docstring |

L'expression du chemin est celle de l'ancienne l. 111, déplacée ; aucune nouvelle logique de
chemin. Seul `expanduser()` est entouré : une boucle de liens symboliques (`RuntimeError` de
`resolve()` en Python 3.11) garde son comportement d'avant. Les appelants (`seed new`, `seed add`,
`seed replace`, `scion new`) passent tous par `parse_location` ; rien d'autre ne change.
`README.md` et extension : rien à modifier (§1.6).

Tests (`test_d17_*`, PA-105 point 4) : indice de `~/x@v1` et de `~/x` + `--version v1` (`HOME` de
test) ; de `~<utilisateur>/x@v1` (répertoire personnel du compte) ; `seed add` de `~/my-lib@master`
et de `~/my-lib` + `--version master` refusé, indice suivi tel quel accepté, `seed remove --purge`
rendant graine et trunk ; formes absolue et relatives inchangées ; `~<sans compte>/x`, nu, `@master`
et `--version master`.

lepton réinstallé : `pipx install --force ~/lepton-tools-dev/lepton-tools` (règle `allow`), depuis
`devenv/env-59` (74c9c97) ; modules installés identiques à la branche (`seed`, `rootstock`, `files`,
`scions`, `cli`, `errors`, `generate`).

## 5. Contrôles après correction

### 5.1 Tests

`~/lepton-tools-dev/venv-lepton-tools/bin/pytest --junitxml …` (forme couverte, sans redirection) :
**508 passed** (499 d'ENV-58 + 9 `test_d17_*`), 447 s ; avant la correction, le même pytest
complet sur `main` : 499 passed, 473 s.

### 5.2 Table du §1 rejouée (`apres/`)

- `classer.py` (`apres/classer.tsv`) : 14 lignes sur 42 changent, exactement celles du PA-105 :
  - `~/…` et `~<U>/…`, `@master` et `--version master`, présent et absent (8 lignes) : indice
    `file://localhost<P>@master` (ou `<A>`), « même dépôt » ;
  - `~inconnu59/…`, 3 variantes × 2 cibles (6 lignes) : « répertoire personnel de « ~inconnu59 »
    introuvable », au lieu de la trace (nue) ou de l'indice faux (versions).
  Les 28 autres lignes sont identiques ; les 24 indices affichés désignent tous le dépôt visé.
- `essai.sh` (`apres/`, 67 cas) : relevés différents seulement pour p02, p03, p05, p06,
  p19-p21, a02, a03, a05, a06, a19-a21 et leurs cas `-i` ; tous les autres fichiers identiques à
  `avant/`. Codes : p02, p03, p05, p06 restent 1 (refus), indice juste ; leurs indices suivis
  (p02-i, p03-i, p05-i, p06-i) passent de 2 à 0 et leurs relevés (`.cmd`, `.out`, `.err`,
  `.code`, `-status`, `-check`, `-remove`) sont identiques octet pour octet à ceux de p11-i (indice
  de la forme absolue) : même URL, même dépôt ; a02-i, a03-i, a05-i, a06-i identiques à a11-i (échec de
  `git clone` d'un dépôt absent, attendu). p19-p21, a19-a21 : code 1, message de lepton ; plus
  d'indice, donc plus de cas `-i`.
- États : après chaque cas et chaque `seed remove` d'un ajout réussi, liens, liens cassés,
  fichiers réguliers, graine, liste greffée et `depots/` égaux au départ (67 `.etat`) ; aucun
  résidu de clonage.
- `autres.sh` (`autres-apres/`, `<W>` neuf `essais/env-59-cwd-apres`) : identique à `autres/`
  sauf o7, dont l'indice devient `file://localhost<C>/depots/lepton/family-qemu-mps2/master@master`
  (D17 au terminal corrigé), et o6, dont seul le nom du répertoire de travail diffère dans le mot
  `~/…` non normalisé. o1-o3, o4-o5, o6, o8 inchangés (D21).

### 5.3 Extension

Commandes de l'extension rejouées en ligne de commande, sans `--no-cmake` (`apres/x01` à `x03`) :
- x01 `seed add env59lib ~/…/env-59-depot --type bibliotheque --version master` : code 1, indice
  `file://localhost<P>@master` ;
- x02 l'indice suivi, `--version master` : code 0, `env59lib ajouté (lepton@library-env59lib,
  master, file://localhost<P>)`, clone fait par scion ;
- x03 `seed remove env59lib --purge` : code 0, clone supprimé ; état = départ.

`lepton generate` dans `<C>` d'abord (l'`env11.code-workspace` copié visait
`essais/env-11/qemu/build/.active`) : code 0, `CMakeUserPresets.json` « inchangé », espace
« écrit » ; état = départ.

Essai dans VSCodium fait par l'utilisateur (2026-11-17), extension 0.5.2, canal « Lepton »
`apres/vscodium-canal.txt` : « ajouter un greffon à la graine » avec `~/…/env-59-depot` et la
version `master` : refus, indice `file://localhost<P>@master`, identique à x01 ; indice collé
comme origine, version `master` : ajouté, identique à x02 ; « retirer un greffon de la graine »
avec « supprimer aussi le clone (--purge) » : identique à x03. État après : égal au départ, graine
propre, aucun clone `library-env59lib`.

**O-3** (extension, hors D17) : après le retrait `--purge`, l'observateur F2 (`watch.ts`, qui
observe le `scion/` de chaque greffon greffé) a vu la suppression du clone et lancé
`lepton graft --path <C>/depots/lepton/library-env59lib/master/scion` : code 1, « ni dans le
trunk …, ni dans un greffon greffé ». `report` en fait un avertissement « lepton : regreffe
automatique — … » (code 1 = `EXIT_USER`). Sans effet sur l'état ; non relevé auparavant (ENV-55
retirait sans `--purge`).

## 6. Questions du PA-106

1. Rapport accepté ?
2. Sort des essais, par `scripts/supprimer-essai.sh` : `essais/env-59-essai`, `essais/env-59-depot`,
   `essais/env-59-cwd`, `essais/env-59-cwd-apres` (rootstocks et dépôts créés sous `<W>/~/…`
   par o2, o3), `essais/env-59-releves` (relevés bruts ; les normalisés sont versionnés).
   `essais/env-59-absent` n'a jamais existé.
3. O-3 : au hors-plan (D24), ou écarté.
4. PA-P : fusion `--no-ff` de `devenv/env-59` dans `main`, push de `main` et de `devenv/env-59`.
