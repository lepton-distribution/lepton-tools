# ENV-58 — Claude Code : formes des commandes et règles de la VM (D20, D19) — audit du 2026-11-17

Session Mac, Claude Code **2.1.326** (épinglé : 2.1.323, version des constats d'ENV-54 et
d'ENV-57), mode auto. Règles du dépôt inchangées depuis ENV-54 (`.claude/settings.json` :
7 `allow`, 5 `ask`, 5 `deny`, hook `proteger-trunk.py`). Réglages du Mac : `~/.claude/settings.json`
sans clé `permissions` ; aucun `settings.local.json` (dépôt, utilisateur).

## 1. Inventaire des formes (tâche 1)

Recherche par `grep` en Bash, sans outil Grep dans la session. Les motifs ne citent pas les
commandes `ask` (`graft.update`, `seed.update`, `\bpu[s]h\b`). Aucun refus. Périmètre :
`.claude/skills/*/SKILL.md`, `CLAUDE.md`, `scripts/` (dont `oracle/`, `tiers/`), outils
`rapports/**/*.{sh,py}` hors `oracles/`, `consignes/env-57-debian.md`, étapes ENV-59 à ENV-61,
code de `lepton/` et `extension/src/`.

### 1.1 Commandes `allow` avec redirection, `| tee` ou `; echo "code=$?"`

Aucune dans les textes à faire taper par une session : skills, `CLAUDE.md`, consigne d'ENV-57,
étapes ENV-59 à ENV-61. Les correspondances du motif sont des faux positifs :
- `<cible>` et `<preset>` contiennent un `>` (`scripts/supprimer-essai.sh:4`,
  `lepton-cibles/SKILL.md:23`) ;
- `ls … 2>&1` (`consignes/env-57-debian.md:196`) et `python3 … > …` (`:338`) sont hors règle.

La consigne d'ENV-57 écrit ses commandes `allow` nues :
- `pipx install` : l. 264 ;
- `git clone` : l. 312, 313, 326 ;
- `supprimer-essai.sh` : l. 314, 320 à 322, 552 ;
- pytest par `--junitxml` : l. 460, 473-474.

Commandes `allow` placées dans un script : la règle ne voit que le lancement du script, qui va au
classifieur. La forme de la commande intérieure est donc sans effet sur la règle.
- `scripts/install-vscodium.sh:181`, `:499` : `run pipx install --force …` ;
- `rapports/env-8-r2-essai.sh:23` : `git clone`, outil historique.

### 1.2 Commandes `ask` dans un script ou dans un `bash -c`

| Fichier, ligne | Forme | Sort |
| --- | --- | --- |
| `rapports/env-53-mac/regreffer-essai.sh:31` | `(cd "$R" && scion graft-update -v) > "$P-graft-update.log" 2>&1; echo …`, dans un script et un sous-shell | outil d'ENV-53, antérieur aux règles d'ENV-54 ; remplacé par `env-57-mac/regreffer-essai.sh` (deux phases) |
| `rapports/env-57-mac/regreffer-essai.sh:3`, `:10` | commentaires : la commande est lancée par la session entre `avant` et `apres` | conforme |

Aucun `bash -c` ne porte une commande `ask` dans le périmètre. `lepton/` et l'extension n'appellent
aucune de ces commandes. La consigne d'ENV-57 (l. 361) lance le `graft-update` directement, avec
redirection et `; echo` : c'est conforme, une règle `ask` valant avec la redirection
(`rapports/env-57-mac.md` §1.5). ENV-61 (l. 124) prévoit aussi la forme directe.

Non inventoriés : les scripts du clone noyau (`install-macos.sh`, `install-debian.sh`), hors du
périmètre du fichier d'étape. Ils lancent `pipx install` à l'intérieur d'un script.

## 2. Essai témoin (Mac, 2026-11-17)

Répertoire `~/lepton-tools-dev/essais/env-58-essai/`. Décisions lues dans le journal de session
par `env-57-mac/decisions.py` (heures UTC) : `env-58-formes/decisions.tsv` (chemin personnel
remplacé par `<HOME>`). Commande de base, forme couverte par
`Bash(~/lepton-tools-dev/venv-lepton-tools/bin/pytest:*)` :
`~/lepton-tools-dev/venv-lepton-tools/bin/pytest -q -p no:cacheprovider --basetemp ~/lepton-tools-dev/essais/env-58-essai/tmp-pytest tests/test_proteger_trunk.py::test_entree_illisible`
(noté `P`). F7 à F9 s'ajoutent aux formes du fichier d'étape.

| Forme | Commande | Décision | Effet |
| --- | --- | --- | --- |
| F1 nue | `P` | **règle** (`subcommandResults`) | 1 passed |
| F2 `> f` | `P > ~/…/env-58-essai/f2.log` | classifieur (accepté) | 1 passed |
| F3 `2>&1` | `P 2>&1` | **règle** (`subcommandResults`) | 1 passed |
| F4 `> f 2>&1` | `P > ~/…/f4.log 2>&1` | classifieur (accepté) | 1 passed |
| F5 `\| tee f` | `P \| tee ~/…/f5.log` | classifieur (accepté) | 1 passed |
| F6 `--junitxml` | `P` avec `--junitxml ~/…/f6.xml` | **règle** (`subcommandResults`) | 1 passed |
| F7 `; echo` | `P; echo "code=$?"` | classifieur (accepté) | 1 passed, `code=0` |
| F8 `>` dans le répertoire de travail | `P > env58-f8.log` (racine de lepton-tools) | `mode` (ni règle ni classifieur) | 1 passed ; fichier déplacé dans l'essai |
| F9 `>` absolu hors du répertoire de travail | `P > /Users/…/env-58-essai/f9.log` | classifieur (accepté) | 1 passed |
| A1 directe | `scion graft-update -v ~/lepton-tools-dev/essais/env-58-absent` | **invite** `ask` (`user_temporary`, `projectSettings`), **confirmée** | code 1 : « n'est pas un rootstock », aucun effet |
| A2 script | `bash doc/devenv/rapports/env-58-formes/ask-script.sh` (même commande, garde : cible absente) | **classifieur** (accepté), **aucune invite** | code 1, aucun effet |
| A3 `bash -c` | `bash -c 'scion graft-update -v ~/lepton-tools-dev/essais/env-58-absent'` | **classifieur** (accepté), **aucune invite** | code 1, aucun effet |

Constats :
- **Redirection** :
  - une redirection vers un fichier fait sortir la commande de sa règle `allow`, que la cible
    soit écrite `~/…` (F2, F4) ou en absolu hors du répertoire de travail (F9) ;
  - vers un fichier du répertoire de travail (F8), elle est acceptée par le mode : ni règle ni
    classifieur ;
  - `2>&1` seul garde la règle (F3) ;
  - la documentation dit la même chose (§3) : la cible d'une redirection est contrôlée comme une
    écriture de fichier, et les formes à descripteur ne le sont pas.
- **`| tee f` et `; echo "code=$?"`** : classifieur (F5, F7). Le code de retour d'un échec
  s'affiche déjà dans le résultat de l'outil (« Exit code 1 », A1, A3).
- **`--junitxml`** : règle (F6), comme en ENV-57.
- **Commande `ask`** :
  - lancée directement : invite (A1) ;
  - depuis un script (A2) ou par `bash -c` (A3) : ni règle ni invite. Le classifieur décide ; il
    a accepté et la commande s'est exécutée ;
  - le constat déduit en ENV-57 (§1.3) est donc établi : **PA-P n'a pas de garde technique hors
    de la forme directe**.
- **Écart A1** : l'invite a été confirmée au lieu d'être refusée. C'est la même manipulation que
  le premier N4 d'ENV-57. Elle est restée sans effet, la cible étant absente.

## 3. Documentation (agent `claude-code-guide`, 2026-11-17, lecture seule)

Sources : `permissions.md`, lu en entier par l'agent ; `permission-modes.md`,
`auto-mode-config.md`, `settings.md`, `hooks.md`, par un extracteur (sens fidèle, mot à mot non
garanti) ; notes de version (`CHANGELOG.md`, début du fichier). Les citations s'accordent avec
les essais du §2.

- **Redirections** (`permissions.md`, « Redirections ») :
  - « When a command redirects output or input, Claude Code checks the redirect target against
    your file rules as if Claude wrote or read that file directly » ;
  - « A rule such as `Bash(git commit *)` allows the command, not the target. A target that
    starts with `~` or contains a glob character needs your approval » ;
  - « Targets with no file behind them aren't checked: `/dev/null`, file-descriptor forms such as
    `2>&1` » ;
  - `tee` : « Claude Code also checks the files a `tee` command writes ».
- **Scripts et `bash -c`** (`permissions.md`, « What a Bash rule doesn't match ») :
  - « A Bash rule matches the command text Claude writes, after Claude Code splits compound
    commands and strips wrappers. It doesn't match the same program invoked in a different form,
    so a deny or ask rule covers the invocation Claude usually produces and isn't a security
    boundary around the program » ;
  - exemple de la page : `Bash(rm *)` en `deny` « doesn't stop » `bash -c 'rm -rf build/'`.
  - La lecture du contenu d'un script par le classifieur n'est pas documentée. Il « sees user
    messages, tool calls […] and your CLAUDE.md content » (`permission-modes.md`).
- **Règles écartées en mode auto** (`permission-modes.md`) : « Blanket `Bash(*)` », « Wildcarded
  interpreters like `Bash(python*)` », « Package-manager run commands », `Agent`, `Monitor` ;
  « Narrow rules like `Bash(npm test)` stay in effect ». Les 3 règles de la VM n'y sont pas
  nommées ; leur sort n'est pas documenté.
- **Cumul** (`settings.md`) : les listes `permissions.allow` se cumulent entre fichiers. Aucun
  moyen documenté, côté projet, d'ignorer les `allow` de l'utilisateur. Une règle `deny` ou
  `ask` du projet passe avant elles.
- **Notes de version 2.1.325 et 2.1.326** (à confirmer dans le fichier brut) :
  - « Fixed some deny and ask rules not applying to certain Bash commands » ;
  - « Changed auto mode to ignore some wildcard shell allow rules » (lesquelles : non dit) ;
  - « Improved Bash permission checks: some commands now ask first » ;
  - « Changed auto mode to stop some shell commands that ran before ».
  Les constats d'ENV-54 et d'ENV-57 (2.1.323) restent vrais en 2.1.326 pour F1, F3, F4, F6 et A1.
- **Option `autoMode.classifyAllShell`** : suspend toutes les règles `allow` Bash en mode auto.
  Elle n'est lue que dans `~/.claude/settings.json` ou `--settings`, jamais dans le dépôt.

## 4. D19 : règles utilisateur de la VM

Connu au Mac : les 3 règles et l'absence de `defaultMode` (`rapports/env-57-debian.md` §1). Les
autres clés du fichier ne sont pas connues.

| Règle de la VM | Couvre en plus des règles du dépôt | Commande prévue d'ENV-59 à ENV-61 qui en dépend | Écartée en mode auto ? |
| --- | --- | --- | --- |
| `Bash(pipx install:*)` | Tout `pipx install`, de toute source : le repli de scion `pipx install --force "git+https://github.com/lepton-distribution/seed.scions.git@<v>"` (consigne d'ENV-57 §6), mais aussi n'importe quel paquet, donc du code arbitraire | Aucune, sauf le repli de C1 d'ENV-61 si `install-debian.sh` est refusé. Ce script, hors règle, a été accepté par le classifieur en R53-1 et R57-1. ENV-61 C2 prévoit déjà le contrôle négatif `pipx install ~/lepton-tools-dev/essais/env-61-absent` | Non documenté (« package-manager run commands » ne nomme pas `install`) |
| `Bash(git clone * https://github.com/lepton-distribution/*)` | `git clone` avec options avant l'URL (`--depth`, `--filter`, `--branch`). Les options dangereuses restent refusées par les `deny` du dépôt, évalués d'abord. Le premier `*` admet aussi un dépôt quelconque suivi d'un chemin qui commence par l'URL | Aucune : `git clone https://github.com/lepton-distribution/seed.scions.git` (C5) a l'URL en premier, couvert par le dépôt. ENV-61 C2 prévoit le contrôle négatif `git clone --depth 1 …` | Non documenté |
| `Bash(python3 -m unittest discover *)` | L'exécution de tout test `unittest`, donc du code des répertoires visés. Origine probable : les tests de scion sur la VM (ENV-15 ; `rapports/env-54-permissions.md` §1, 2026-10-30) | Aucune : ENV-61 ne lance pas les tests de scion. C5 lance `python3 fixture.py`, hors règle | Non documenté (`python3` littéral, le joker est dans les arguments) |

## 5. Propositions pour le PA-103 (non validées)

1. **Amendement d'ORCHESTRATION §2bis**, paragraphe « Commandes soumises aux règles… ». Ajout
   d'une sous-liste « Formes » :
   - commande `allow` écrite seule : ni redirection vers un fichier hors du répertoire de travail,
     ni `| tee`, ni `; echo "code=$?"`, chacune la faisant passer au classifieur. `2>&1` est
     admis. Le journal passe par une option de l'outil (`--junitxml`), ou se lit dans le
     résultat de l'outil, code de retour compris ;
   - commande `ask` (`scion graft-update`, `scion seed-update`, `git push`) : lancée directement
     par la session (redirection et `; echo` admis). Jamais dans un script, un `bash -c` ou un
     `eval` : la règle ne la voit pas, le classifieur en décide (A2, A3) ;
   - un script qui en a besoin se coupe en deux phases ; la session lance la commande entre les
     deux (forme de `rapports/env-57-mac/regreffer-essai.sh`).
   Le §2 des consignes VM renverra au §2bis au lieu de porter seul la règle.
2. **Garde technique**. Options :
   - G0 : aucune ; la règle écrite seule ;
   - G1 : règles `ask` du dépôt sur les enveloppes de shell qui citent une commande `ask`
     (`Bash(bash -c *graft-update*)`, `…seed-update…`, `…push…`, et `sh -c`, `zsh -c`). Elles
     couvrent A3, pas A2 ;
   - G2 : le hook demande l'invite (`permissionDecision: "ask"`) quand une commande lance un
     script, ou un `-c`/`eval`, qui contient une commande `ask`. Le hook sait déjà analyser
     `bash -c`, `eval`, `find -exec` et `xargs`. Il faut lire le fichier du script, écrire des
     tests, et prouver qu'une décision `ask` d'un hook fait paraître l'invite en mode auto (non
     documenté). Couvre A2 et A3, pas les scripts lancés par un autre programme.
   Recommandation : G2 avec la règle écrite, si l'invite par hook est prouvée sur une cible
   absente. Sinon G1 et la règle écrite. Aucune n'est une frontière de sécurité (§3) ; PA-P
   reste l'accord de l'utilisateur.
3. **Règles utilisateur de la VM** : retirer les trois. Aucune commande prévue n'en dépend (§4).
   Le repli `pipx` de scion reste à l'utilisateur en cas de refus (forme actuelle de la
   consigne).
4. **Qui et quand** : l'utilisateur, au §0 de la consigne d'ENV-61, d'après le bloc
   `permissions.allow` du rapport. Il relit le fichier entier avant et après ; seul ce bloc
   change. La VM n'écrit que son rapport.
5. **Règles du dépôt** : aucune nouvelle règle `allow`. G1 ou G2 selon le point 2.
6. **`CLAUDE.md` et skills** :
   - `CLAUDE.md` : une ligne dans « Règles permanentes » (commandes `ask` lancées directement,
     jamais par un script ou un `bash -c`). Le classifieur lit ce fichier ;
   - `lepton-rootstock` (« Interdits ») : la même précision ;
   - `env-53-mac/regreffer-essai.sh` : laissé tel quel, outil historique cité au §1.2.
