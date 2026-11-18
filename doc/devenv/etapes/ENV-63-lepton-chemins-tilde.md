# Étape ENV-63 — lepton : `~` dans les chemins saisis (D21)

## Contexte
Révision du plan du 2026-11-18, faite à partir de `HORS-PLAN.md`. D21 est à traiter (décision de
l'utilisateur du 2026-11-17, fin du plan, après ENV-61). Ce n'est pas un ticket : lepton-tools
n'est pas un greffon du rootstock (décision du 2026-11-18). Le constat vient d'ENV-59
(`rapports/env-59-tilde.md` §1.4), où il a été écarté comme seconde variable de D17, et a été
ajouté au hors-plan au PA-105.

ENV-59 a corrigé `parse_location` : `~` et `~<utilisateur>` y sont développés, et
`~<utilisateur sans compte>/…` devient un message de lepton au lieu d'une trace. Six autres
chemins saisis sont résolus sans `expanduser()`. Avec `~` non développé :
- `seed new -C`, `--seed-repo` et `scion new --repo` réussissent (code 0) en créant `<cwd>/~/…`,
  sans message ;
- `-C`, `_locate` et `--clangd` refusent, en montrant le chemin pris.

Le cas se produit au terminal sans apostrophes : `--option=~/…`, car zsh et bash ne développent
pas `~` après « = ». Il se produit aussi depuis l'extension, qui transmet sans shell les chemins
saisis de `file …` et `dir …`.

Faits relevés à la révision (`main` 24ca20a ; numéros indicatifs) :
- `lepton/rootstock.py:226` : `-C DIR`, `Path(explicit).resolve()` (`Rootstock.discover`) ;
- `lepton/seed.py:375` : `seed new -C`, `Path(args.rootstock or ".").resolve()` ;
- `lepton/seed.py:378` : `--seed-repo`, `Path(args.seed_repo).resolve()` ;
- `lepton/scions.py:125` : `scion new --repo`, `Path(args.repo).resolve()` ;
- `lepton/files.py:94` : `_locate`, `Path(os.path.abspath(raw))` ;
- `lepton/generate.py:117` : `--clangd`, `shutil.which(explicit)`, puis
  `Path(explicit).is_file()` ;
- forme de référence : `lepton/seed.py:109`, `expanded = Path(loc).expanduser()`, avec
  `RuntimeError` → `LeptonError` (74c9c97, PA-105).
`HORS-PLAN.md` donne `seed.py:369` et `seed.py:372` : ce sont les numéros d'avant 74c9c97.

Archétype : infrastructure. L'étape change des entrées acceptées : dans la portée du PA-113, un
`~` littéral ne crée plus `<cwd>/~/…`. C'est la variable de l'étape, et elle seule. Aucune autre entrée acceptée ne change ;
aucun binaire ni aucun lien du trunk ne change.

## Prérequis
- ENV-62 terminée (règles du §2bis amendées). Indépendante d'ENV-64 et d'ENV-65 ; conseillée avant
  ENV-64 : la forme retenue ici sert de référence au PA-115 (D23).
- lepton 0.1.0 ; scion 0.6.3.2 ; `pytest` 527 verts au départ, plus ceux d'ENV-62.
- Méthode et outils d'ENV-59 à reprendre plutôt qu'à réécrire : `rapports/env-59-tilde.md` §1 ;
  `rapports/env-59-tilde/essai.sh`, `autres.sh` et `classer.py`. Les relevés `autres/` et
  `autres-apres/` d'ENV-59 servent de point de départ.
- Tests : `tests/test_milestone3.py` (`test_d17_*`, `test_d13_*`), et les tests de `file …`,
  `dir …` et `generate`, à situer à l'audit. Venv `~/lepton-tools-dev/venv-lepton-tools`.
- Skill `lepton-rootstock` (rootstock d'essai).
- Branche `devenv/env-63` dans lepton-tools seulement.

## Tâches

### 1. Audit (lecture seule) → PA-113
- Rapport `rapports/env-63-tilde.md` §1. Une table : pour chacun des 6 chemins et chaque forme
  (`~/…`, `~<utilisateur>/…`, `~<utilisateur sans compte>/…`, relatif, absolu), le message, le
  code et l'état laissé (répertoire `<cwd>/~` créé ou non). Scripts versionnés sous
  `rapports/env-63-tilde/`, pour être repris en ENV-66.
- Origine transmise sans développement : `'~/…'` entre apostrophes, `--option=~/…`, ou appel en
  liste (forme de l'extension). Puis la même entrée développée par le shell, pour comparaison.
- Essai sur `essais/env-63-essai`, copie d'`essais/env-11/qemu` par `rsync -a`, sans `build/`
  (forme d'`essais/env-59-essai`). Jamais sur `<ROOTSTOCK>`, jamais dans `essais/env-11/qemu`
  lui-même. Les créations de `seed new` et `scion new` se font dans des répertoires sous
  `essais/env-63-essai/`.
- Relever les autres chemins saisis que l'audit trouverait (options `Path`, `type=Path`,
  `os.path.abspath`), hors des 6. Ils restent hors de l'étape, sauf décision au PA-113.
- Extension : relever lesquels de ces chemins `commands.ts` transmet. D23 (`lepton.path`) relève
  d'ENV-64.
- **PA-113** : l'utilisateur tranche :
  - forme : `~` développé comme dans `parse_location` (PA-105), ou refusé avec un message ;
    <À CONFIRMER au PA-113> ;
  - portée : les 6 chemins, ou une partie ; chemins trouvés en plus ;
  - `~<utilisateur sans compte>/…` : message de lepton (forme du PA-105) ;
  - `--clangd` : nom d'exécutable cherché dans le PATH, ou chemin développé ;
  - factorisation : une fonction commune de lepton, ou une expression par site ;
    <À CONFIRMER au PA-113> ;
  - tests : forme et emplacement ;
  - `README.md` : un texte qui décrit ces options change-t-il ?
- Aucune modification avant la réponse.

### 2. Correction (`devenv/env-63`)
- Tests d'abord : un test par chemin et par forme retenus au PA-113, qui échoue sur `main`. Les
  formes inchangées (absolu, relatif, `~` développé par le shell) sont couvertes par un test qui
  passe déjà.
- Puis la correction, selon le PA-113, sans nouvelle logique de chemin hors de la forme retenue.
- Réinstaller lepton : `pipx install --force ~/lepton-tools-dev/lepton-tools`, écrit tel quel
  (règle `allow`).

### 3. Contrôles → PA-114
- `pytest` complet vert, dans la forme couverte par la règle (ORCHESTRATION §2bis).
- Table du §1 rejouée sur `essais/env-63-essai` :
  - les lignes visées par le PA-113 suivent la décision ; aucun `<cwd>/~` créé dans sa portée ;
  - toutes les autres lignes sont identiques à l'avant (codes et sorties) ;
  - liens du trunk et graine égaux au départ après chaque essai.
- Rejouer `rapports/env-59-tilde/essai.sh` : D17 inchangé (relevé égal à `env-59-tilde/apres/`,
  aux chemins d'essai près).
- Extension : l'utilisateur lance dans VSCodium une commande `file …` ou `dir …` avec un chemin
  `~/…`, et relève le canal « Lepton ». Sinon, la raison de ne pas l'essayer est donnée au
  rapport.
- **PA-114** : rapport ; sort d'`essais/env-63-essai` (par `scripts/supprimer-essai.sh`) ; push et
  fusion de `devenv/env-63` dans `main` (PA-P). La validation Debian est faite en ENV-66.

## Critères de validation
- [ ] PA-113 et PA-114 tranchés et consignés.
- [ ] Table du §1 au rapport, avant et après.
- [ ] Nouveaux tests : échec sur `main`, réussite sur la branche ; `pytest` complet vert.
- [ ] Aucun `<cwd>/~` créé par `seed new -C`, `--seed-repo` ou `scion new --repo`, dans la portée
      du PA-113.
- [ ] Formes hors du PA-113, et D17 : comportement inchangé.
- [ ] `HORS-PLAN.md` : D21 marqué traité, avec renvoi au rapport.

## Pièges connus
- Le shell développe `~` avant lepton : un essai écrit `~/…` sans apostrophes ne reproduit pas
  D21. zsh et bash ne développent pas `~` après « = » (`--repo=~/…`), sauf `magic_equal_subst` de
  zsh ; bash développe `nom=~/x` quand `nom` est un nom de variable valide
  (`rapports/env-59-tilde.md` §1.6).
- Un répertoire `~` créé par l'essai dans le répertoire courant se supprime par
  `scripts/supprimer-essai.sh`, seulement s'il est sous `essais/`. Toujours lancer les essais
  depuis un répertoire sous `essais/env-63-essai/`.
- `Path("~x").expanduser()` lève `RuntimeError` pour un utilisateur sans compte (Python 3.11) :
  forme traitée en ENV-59.
- Sur la graine de référence, lepton refuse `seed add` et `scion new` sans `--no-seed`
  (`refuse_reference`) : tout essai se fait sur un rootstock d'essai à graine de projet.
- Une redirection fait sortir `pytest` de sa règle `allow` (D20) : journal par `--junitxml`.
- zsh ne découpe pas une variable en mots : utiliser `bash -c` ou un script.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, branche, §Versions (lepton réinstallé), décisions PA-113 et PA-114,
journal. `HORS-PLAN.md` : D21. Passation `handoff/env-63.md`.
