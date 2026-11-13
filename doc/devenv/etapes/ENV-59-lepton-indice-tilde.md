# Étape ENV-59 — lepton : `~` dans l'indice « version sans effet » (D17)

## Contexte
Révision du plan du 2026-11-13, faite à partir de `HORS-PLAN.md` : D17 est à traiter (décision de
l'utilisateur du 2026-11-13, fin du plan, après ENV-57). Constat O-1 d'ENV-55
(`rapports/env-55-url-file.md` §6), reporté au hors-plan au PA-98.

Une origine locale avec une version (`~/…@master`) est refusée : « version sans effet ». L'indice du
refus propose une URL `file://localhost<chemin>@<version>`. Il calcule le chemin par
`Path(loc).resolve()`, sans `expanduser()`, alors que le contrôle d'existence, à la ligne suivante,
le fait. Transmise sans shell, par exemple saisie dans l'extension, l'origine `~/…@master` donne
donc l'indice faux `file://localhost<cwd>/~/…@master`.

Faits relevés à la révision (`main` 71cba24, numéros indicatifs) :
- `lepton/seed.py` :
  - `parse_location` (l. 89) ;
  - indice (l. 110) : `file://localhost{Path(loc).resolve()}@{ver}` ;
  - chemin local (l. 111) : `Path(loc).expanduser().resolve()`.
- Appelants de `parse_location` :
  - `seed new` (l. 375-377 : noyau, famille, BSP) ;
  - `seed add` (l. 618) ;
  - `seed replace` (l. 711) ;
  - `lepton/scions.py:166` (`scion new`).
- Extension : `extension/src/commands.ts:87`. La version proposée par défaut est `master`, et
  `seedAdd` passe `--version <v>`. Une origine locale saisie dans l'extension aboutit donc à ce
  refus, sauf si l'utilisateur vide le champ.
- Autres chemins saisis par l'utilisateur et résolus sans `expanduser()` (liste non exhaustive) :
  - `lepton/rootstock.py:226` (`-C DIR`) ;
  - `lepton/seed.py:369` (`seed new -C`) ;
  - `lepton/seed.py:372` (`--seed-repo`) ;
  - `lepton/scions.py:125` (`--repo`) ;
  - `lepton/files.py:94` (`_locate`, `os.path.abspath`).
  Hors de D17 ; à classer à l'audit.
- `README.md` ne décrit pas l'indice (aucune occurrence de « sans effet » ni de
  `file://localhost`).

Archétype : infrastructure. Si le PA-105 s'en tient à l'indice, l'étape est iso-fonctionnelle hors
de ce texte : aucune origine acceptée ne change, et aucun binaire ni aucun lien du trunk ne change.
Étendre la correction aux autres chemins saisis changerait des entrées acceptées : c'est une
seconde variable.

## Prérequis
- ENV-57 terminée ; ENV-58 conseillée avant (formes des commandes, §2bis amendé). Indépendante
  d'ENV-60.
- lepton 0.1.0 ; scion 0.6.3.1, ou la version d'ENV-60 si elle a précédé ; `pytest` 453 verts
  (ENV-57), plus les tests d'ENV-60 si elle a précédé.
- Tests : `tests/test_milestone3.py`, dont `test_gra3_parse_location` (l. 98) et `test_d13_*`
  (l. 130-167). Venv `~/lepton-tools-dev/venv-lepton-tools`.
- Méthode d'ENV-55 : `rapports/env-55-url-file.md` §1, et scripts `rapports/env-55-url-file/`
  (`essai.sh`, `etat.sh`, `classer.py`), à reprendre plutôt qu'à réécrire.
- Skill `lepton-rootstock` (rootstock d'essai).
- Branche `devenv/env-59` dans lepton-tools seulement.

## Tâches

### 1. Audit (lecture seule) → PA-105
- Table au rapport `rapports/env-59-tilde.md` §1 : message et code de `parse_location`, puis de
  `lepton seed add`, pour chaque forme d'origine :
  - `~/…`, `~<utilisateur>/…`, chemin relatif, chemin absolu ;
  - chacune avec `@VERSION`, avec `--version`, et sans version.
  Origine transmise sans développement par le shell : `'~/…'` entre apostrophes, ou appel en
  liste (forme de l'extension). Puis la même origine développée par le shell, pour comparaison.
- Essai sur un rootstock d'essai à graine de projet, jamais sur `<ROOTSTOCK>` :
  - `essais/env-59-essai`, copie d'`essais/env-11/qemu` par `rsync -a`, sans `build/` (forme
    d'`essais/env-55-essai`) ;
  - dépôt d'essai présent sous `essais/` (forme du dépôt `env55lib` d'ENV-55).
- Autres chemins saisis sans `expanduser()` (liste du contexte) : relever le comportement de
  chacun avec `~` non développé. Noter lesquels l'extension transmet sans shell.
- **PA-105** : l'utilisateur tranche :
  - portée : l'indice de la l. 110 seul (D17). Les autres chemins saisis sont une seconde
    variable. Options : les inclure ici, les traiter dans une étape à part, ou les reporter au
    hors-plan. <À CONFIRMER au PA-105> ;
  - forme de l'indice pour une origine relative (absolu après `expanduser().resolve()`, comme le
    contrôle d'existence) ;
  - tests : forme et emplacement (proposition : `tests/test_milestone3.py`, près de
    `test_d13_*`).
- Aucune modification avant la réponse.

### 2. Correction (`devenv/env-59`)
- Tests d'abord : un test par forme retenue au PA-105, qui échoue sur `main`. Les formes
  inchangées sont couvertes par un test qui passe déjà.
- Puis la correction : le chemin de l'indice est calculé comme celui du contrôle d'existence. Une
  seule expression, pas de nouvelle logique de chemin.
- Réinstaller lepton : `pipx install --force ~/lepton-tools-dev/lepton-tools`, écrit tel quel
  (règle `allow`), depuis la branche.

### 3. Contrôles → PA-106
- `pytest` complet vert (453 après ENV-57, plus ceux d'ENV-60 si elle a précédé, plus les
  nouveaux), dans la forme couverte par la règle (ORCHESTRATION §2bis).
- Table du §1 rejouée sur `essais/env-59-essai` :
  - les lignes visées par le PA-105 suivent la décision ;
  - toutes les autres lignes sont identiques à l'avant (codes et sorties) ;
  - l'indice affiché pour `~/…@VERSION`, suivi tel quel, est accepté par `seed add` et désigne le
    même dépôt ;
  - liens du trunk et graine égaux au départ après chaque essai, et après chaque `seed remove`
    d'un ajout réussi.
- Extension : l'utilisateur lance, dans VSCodium, « ajouter un greffon à la graine » avec une
  origine `~/…` et la version `master` (forme d'ENV-55 §5). Le canal « Lepton » est relevé.
  Sinon, la raison de ne pas l'essayer est donnée au rapport.
- **PA-106** : rapport ; sort d'`essais/env-59-essai` et du dépôt d'essai (par
  `scripts/supprimer-essai.sh`) ; push et fusion de `devenv/env-59` dans `main` (PA-P). La
  validation Debian est faite en ENV-61.

## Critères de validation
- [ ] PA-105 et PA-106 tranchés et consignés.
- [ ] Table du §1 au rapport, avant et après.
- [ ] Nouveaux tests : échec sur `main`, réussite sur la branche ; `pytest` complet vert.
- [ ] L'indice affiché pour `~/…@VERSION` est une URL que `seed add` accepte.
- [ ] Formes hors du PA-105 : comportement inchangé.
- [ ] `HORS-PLAN.md` : D17 marqué traité, avec renvoi au rapport.

## Pièges connus
- Le shell développe `~` avant lepton : un essai écrit `~/…` sans apostrophes ne reproduit pas
  D17. Seule l'origine passée telle quelle (apostrophes, appel en liste, extension) le reproduit.
- Le refus « version sans effet » (l. 107-110) survient avant le contrôle d'existence (l. 113) :
  une origine absente avec `@VERSION` donne le même message.
- L'espace `env11.code-workspace` de la copie vise `essais/env-11/qemu/build/.active` : lancer
  `lepton generate` dans la copie avant l'essai dans VSCodium (`rapports/env-55-url-file.md`
  §5).
- Sur la graine de référence, lepton refuse `seed add` (`refuse_reference`) : tout essai se fait
  sur un rootstock d'essai à graine de projet. Jamais dans `essais/env-11/qemu` lui-même.
- L'échec d'un `git clone` ne laisse plus de répertoire depuis scion 0.6.3.1 (D14) ; un résidu
  serait un écart à consigner.
- Une redirection fait sortir `pytest` de sa règle `allow` (D20) : journal par `--junitxml`.
- `zsh` ne découpe pas une variable en mots : utiliser `bash -c` ou un script.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, branche, §Versions (lepton réinstallé), décisions PA-105 et PA-106,
journal. `HORS-PLAN.md` : D17. Passation `handoff/env-59.md`.
