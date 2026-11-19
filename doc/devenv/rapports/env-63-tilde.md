# ENV-63 — lepton : `~` dans les chemins saisis (D21) — rapport

Branche lepton-tools `devenv/env-63` (depuis `main` 332babc). lepton 0.1.0 (pipx, code de `main`),
scion 0.6.3.2, Claude Code 2.1.328. Constat d'origine : `rapports/env-59-tilde.md` §1.4 ; D21 de
`HORS-PLAN.md`.

Notations : `<E>` essai `~/lepton-tools-dev/essais/env-63-essai` ; `<C>` = `<E>/rs`, rootstock
d'essai (copie par `rsync -a` d'`essais/env-11/qemu` sans `build/`, graine de projet `env11`,
3059 liens, 0 cassé, `lepton check` code 0) ; `<G>` = `<E>/gen`, copie de `<C>` pour les
`generate` qui écrivent ; `<W>` = `<E>/w-<phase>`, un répertoire courant vide par cas ;
`<T>` = `<E>/cibles-<phase>`, chemins visés ; `<hC>`, `<hT>`, `<hW>` les mêmes, relatifs à
`<HOME>` ; `~<U>` le tilde suivi du nom de l'utilisateur.

## 1. Comportement avant correction

### 1.1 Méthode

- Code lu (`main` 332babc) : `rootstock.py:226` (`Rootstock.discover`, `-C`),
  `seed.py:375` (`seed new -C`), `seed.py:378` (`--seed-repo`), `scions.py:125` (`--repo`),
  `files.py:94` (`_locate`), `generate.py:117` (`find_clangd`) ; forme de référence
  `seed.py:108-112` (`expanduser()`, `RuntimeError` → `LeptonError`, PA-105) ;
  `extension/src/commands.ts`, `runner.ts`.
- Script `env-63-tilde/chemins.sh <E> <phase> <sortie>` (repris d'`env-59-tilde/autres.sh` ;
  relevé `env-51-messages/releve.sh`, état `env-55-url-file/etat.sh`, `LC_ALL=C`). Chaque chemin
  est transmis tel quel (comme un appel en liste : forme de l'extension), dans 7 formes : `t`
  `~/…`, `u` `~<U>/…`, `x` `~inconnu63/…` (utilisateur sans compte), `r` relatif, `a` absolu,
  `d` `~/…` développé par bash (mot non cité), `z` tapé dans zsh `--option=~/…` (non développé).
- Après chaque cas : état de `<C>` comparé au départ (liens, cassés, réguliers, graine, liste
  greffée, `depots/`), HEAD et fichiers modifiés des 3 clones, arborescence du répertoire courant,
  présence d'un `<cwd>/~*`, existence de la cible. Relevés bruts `<E>/releves/avant/`, normalisés
  dans `env-63-tilde/avant/` (`resume.tsv` : une ligne par cas).
- 45 cas. `<C>` égal au départ et clones inchangés après **chaque** cas (`avant/*.etat`).

### 1.2 Table par chemin et par forme

Code de retour ; `~` : répertoire `<cwd>/~…` créé ; cible : chemin visé créé.

| Chemin (code) | `t` `~/…` | `u` `~<U>/…` | `x` `~inconnu63/…` | `r` relatif | `a` absolu | `d` développé | `z` zsh `=~/…` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| p1 `-C` (`check`) | 1 « `<W>/p1-t/~/<hC>` n'est pas un rootstock » | 1, idem `~<U>` | 1, idem `~inconnu63` | 0 | 0 | 0 | 1, comme `t` |
| p2 `seed new -C` | **0**, `~` créé, rootstock sous `<W>/p2-t/~/<hT>/n2-t` ; cible absente | **0**, `~<U>` créé | **0**, `~inconnu63` créé | 0, cible | 0, cible | 0, cible | — |
| p3 `--seed-repo` | **0**, graine sous `<W>/p3-t/~/…/g3-t`, rootstock `<T>/n3-t` | **0**, `~<U>` créé | **0**, `~inconnu63` créé | 0, cible | 0, cible | 0, cible | — |
| p4 `scion new --repo` | **0**, « dépôt créé : `<W>/p4-t/~/<hT>/r4-t` » | **0**, `~<U>` créé | **0**, `~inconnu63` créé | 0, cible | 0, cible | 0, cible | **0**, `~` créé |
| p5 `_locate` (`file owner`) | 1 « `~/<hC>/trunk/CMakeLists.txt` : ni dans le trunk `<C>/trunk`, ni dans un greffon greffé » | 1, idem | 1, idem | 0 `owned` | 0 `owned` | 0 `owned` | — |
| p5 `file add` / `dir add` / `graft --path` | 1, même message, rien d'écrit | — | — | — | — | — | — |
| p6 `generate --clangd` | 1 « --clangd « ~/<hW>/outils/clangd » introuvable » | 1, idem | 1, idem | 0 | 0 | 0 | — |

`p6-n` (nom d'exécutable `clangd-mp-21`, cherché dans le PATH) : 0, `clangd.path`
`/opt/local/bin/clangd-mp-21`. Les `p6` qui réussissent écrivent dans `<G>` (espace de travail,
presets), jamais dans `<C>`.

Gravité : p2, p3, p4 réussissent (code 0) au mauvais endroit, sans message, pour les trois formes
`~` ; `~inconnu63` y est pris comme un nom de répertoire. p1, p5, p6 refusent, avec un message qui
montre le chemin pris (p1 : chemin résolu sous `<cwd>` ; p5, p6 : texte saisi).

### 1.3 Autres chemins saisis (hors des 6)

Recherche dans `lepton/*.py` : `type=Path`, `Path(args.…)`, `os.path.abspath`, `expanduser`,
arguments `metavar` `PATH`/`DIR`/`FILE`.

| Chemin | Code | Forme `t` | Remarque |
| --- | --- | --- | --- |
| `graft --path P` | `files.py:407` → `_locate` | 1 (cas `p5graft-t`), message de p5 | suit `_locate` : corrigé avec lui, sans code propre |
| `check FILE…` | `cli.py:79`, `Path(name)` | 1 « `~/<hC>/…/lepton-graine.json`: fichier introuvable » (cas `c1-t` ; `c1-a` : 0) | lecture seule ; l'extension transmet le chemin du document ouvert (absolu) |
| `seed mkconf import PATH`, `seed new --mkconf PATH` | `seed.py:269`, `seed.py:418` | lu : `~/…` non absolu → pris relatif au trunk → « absent du trunk greffé » ; cas `m1-t` refusé avant, pour une autre raison (« XML de la graine déjà fourni ») | chemin relatif au trunk ou absolu sous le trunk ; l'extension transmet le chemin saisi de `seedMkconfImport` |
| `--destination D`, `--path P` (`seed add`) | chemins relatifs au greffon | non concernés | pas des chemins de l'hôte |

Aucun de ces chemins ne crée `<cwd>/~` : ils refusent, ou lisent.

### 1.4 Extension (`commands.ts`)

| Chemin | Transmis ? |
| --- | --- |
| `-C`, `seed new -C`, `--seed-repo`, `--repo`, `--clangd` | non (`scionNew` sans `--repo`, `generate` sans option, cwd = dossier de l'espace) |
| `_locate` | **oui** : chemin saisi de `file add` / `dir add` (sans désignation dans l'explorateur), `file owner` qui les précède (`ownerOption`), cible saisie de `file remove` / `dir remove`, source et destination saisies de `file mv` |
| `seed mkconf import PATH` | oui, si saisi (`seedMkconfImport`, sans désignation ni fichier actif) |

Lu, non essayé : après un `file add` ou un `file mv` réussi, l'extension ouvre
`vscode.Uri.file(<chemin saisi>)` (`commands.ts:258`, `:280`), sans développer `~`. Si lepton
développe `~`, la commande réussirait et l'extension ouvrirait `~/…` pris tel quel (O-2).

### 1.5 Observations

- **O-1** (`--clangd` relatif) : `shutil.which()` rend un chemin qui contient `/` tel qu'il est
  saisi ; `p6-r` écrit `"clangd.path": "../w-avant/outils/clangd"` dans l'espace de travail
  (`avant/p6-r.clangd`), relatif au répertoire courant de `generate`. Les formes absolue et nom
  d'exécutable donnent un chemin absolu. Hors de D21 (pas de `~`).
- **O-2** (extension) : ouverture du fichier par le chemin saisi (§1.4).
- `README.md` : seul exemple, `seed new demo -C ~/demo` (espace : développé par le shell) ;
  aucune option n'y est décrite avec un `~` littéral. Rien n'y devient faux, quelle que soit la
  forme retenue.
- Tests existants à côté desquels écrire : `tests/test_milestone3.py` (`test_d17_*`, `test_d13_*`,
  `test_gra1_seed_new*`), `tests/test_milestone4.py` (`scion new`), `tests/test_milestone5.py`
  (`test_fic1_*`, `test_fic2_*` : `file`, `dir`), `tests/test_generate.py`
  (`test_find_clangd`).

## 2. Questions du PA-113

1. **Forme.** (a) `~` et `~<utilisateur>` développés, comme `parse_location` (PA-105) ; (b) refus
   avec un message (« `~` non développé : … »). (a) aligne lepton sur le shell et sur l'origine
   de `seed add` ; (b) refuse une entrée dont le sens est clair. Proposition : (a).
2. **Portée.** Les 6 chemins (`graft --path` suit `_locate`). Chemins du §1.3 (`check FILE`,
   `seed mkconf import PATH`, `--mkconf`) : ils refusent déjà avec un message qui montre le chemin,
   sans rien créer. Options : inclus ici (une entrée refusée devient acceptée), ou hors de l'étape
   (ligne au hors-plan). Proposition : les 6 seuls ; §1.3 au hors-plan.
3. **`~<utilisateur sans compte>/…`** : message de lepton, forme du PA-105 :
   « `<option>` « ~inconnu63/… » : répertoire personnel de « ~inconnu63 » introuvable », action
   « vérifier le nom qui suit « ~ », ou donner un chemin absolu ». Proposition : retenue. p2-x,
   p3-x, p4-x passent de « créé sous `<cwd>/~inconnu63` » à ce refus ; p1-x, p5-x, p6-x changent
   de message.
4. **`--clangd`.** Un mot sans `/` reste un nom d'exécutable cherché dans le PATH (`p6-n`
   inchangé) ; un mot qui commence par `~` est développé, puis traité comme aujourd'hui
   (`shutil.which`, sinon fichier). Proposition : retenue. O-1 (relatif gardé relatif) : hors de
   l'étape.
5. **Factorisation.** (a) Une fonction commune, `expand_user(text, what) -> Path` dans
   `lepton/rootstock.py` (module déjà importé par `seed`, `scions`, `files`, `generate`), qui
   rend `Path(text).expanduser()` ou lève la `LeptonError` du point 3 ; `parse_location` la
   reprend avec `what = "origine locale"`, pour un message identique (D17 inchangé). (b) Une
   expression par site. Proposition : (a).
6. **Tests.** Un test paramétré par chemin, formes `~/…` (`HOME` remplacé par `monkeypatch`),
   `~<U>/…`, `~inconnu…/…`, dans le fichier des tests de la commande :
   `test_milestone3.py` (`seed new -C`, `--seed-repo`), `test_milestone4.py` (`--repo`),
   `test_milestone5.py` (`_locate` : `file owner`, `file add`), `test_generate.py` (`--clangd`),
   et un pour `-C` (`check`). Attendus : aucun `<cwd>/~` créé, cible créée sous le `HOME` de test
   (p2-p4), refus levés (p1, p5, p6 acceptés après). Formes relative et absolue : tests existants
   (`test_gra1_seed_new`, `test_fic1_*`, `test_find_clangd`) ; un test `parse_location` existant
   (`test_d17_unknown_user_home`) garde son message.
7. **`README.md`** : aucun changement (§1.5). Proposition : inchangé.
8. **O-1, O-2** : au hors-plan, ou écartées. Proposition : O-1 au hors-plan (lepton) ; O-2
   présenté au PA-115 d'ENV-64 (extension, même famille que D23).

## 3. PA-113 (2026-11-19, décisions de l'utilisateur)

| Question | Décision |
| --- | --- |
| Forme | `~` et `~<utilisateur>` développés, comme `parse_location` (PA-105) |
| Portée | les 6 chemins (`graft --path` suit `_locate`) ; §1.3 au hors-plan (D29) |
| `~<utilisateur sans compte>/…` | message de lepton, forme du PA-105 (§2 point 3) |
| `--clangd` | nom sans `/` cherché dans le PATH ; valeur en `~` développée, puis traitement actuel |
| Factorisation | fonction commune `expand_user(text, what)` dans `lepton/rootstock.py`, reprise par `parse_location` (message identique) |
| Tests | un test paramétré par chemin, dans le fichier de la commande (§2 point 6) |
| `README.md` | inchangé |
| O-1, O-2 | O-1 au hors-plan (D30) ; O-2 au hors-plan (D31), présenté au PA-115 d'ENV-64 |
