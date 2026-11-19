# ENV-62 — Claude Code : règle U3, invites à refuser, outils des consignes VM (D26, D28, D27) — rapport

Brouillon (tâche 1, audit en cours, avant le PA-111). Mac, Claude Code **2.1.328** (2.1.327 à la
passation ; rejeu sous 2.1.328, décision du plan de session), mode auto. Journal de session :
`46a64b00-d1cd-456d-a1e0-63283036b6cc.jsonl`. Décisions relevées par
`env-62-claude-code/raisons.py` (forme d'`env-57-mac/decisions.py`, avec `reasonCode`,
`grantScope` et les autres clés de `permissionDecision`). Chemin personnel normalisé `<HOME>`.

## 1. D26 — règle utilisateur U3

### 1.1 Documentation (agent `claude-code-guide`, lecture seule, 2026-11-19)

Sources brutes : pages `permission-modes`, `permissions`, `auto-mode-config`, `hooks`,
`settings`, CHANGELOG d'`anthropics/claude-code` (`main`, première section 2.1.328).

- Documenté (`permission-modes`, « How auto mode evaluates actions ») : à l'entrée en mode auto,
  « broad allow rules that grant arbitrary code execution are dropped, including » `Bash(*)`,
  « Wildcarded interpreters like `Bash(python*)` », une enveloppe suivie d'un seul joker
  (`Bash(timeout *)`), une règle qui commence par un joker, certains chemins à joker
  (`Bash($HOME/bin/*)`), les commandes « run » des gestionnaires de paquets. « Narrow rules like
  `Bash(npm test)` stay in effect. » Liste non exhaustive (« including »).
- CHANGELOG 2.1.326 : « Changed auto mode to ignore some wildcard shell allow rules, such as ones
  that name no program or that start with `$HOME`, so the safety check decides those commands ».
  2.1.327 : « ignore more allow rules that run any package, like `Bash(pnpm dlx *)` ». Rien en
  2.1.325 ni en 2.1.328.
- Non documenté : le sort de `Bash(python3 -m unittest discover *)` (interpréteur littéral, joker
  dans les arguments), de `Bash(pipx install:*)` et de `Bash(git clone * https://…/*)` ; la
  dépendance à la source de la règle ; le sens de `reasonCode` (`shell-expansion`, `bashMiss`) ;
  le format du journal `.jsonl`.
- Documenté : `autoMode.classifyAllShell` suspend toutes les règles `allow` du shell en mode
  auto (`auto-mode-config`). Le bloc `autoMode` n'est pas lu dans les réglages de projet.

### 1.2 Essai témoin au Mac, règles posées à chaud (2026-11-19, 07:29-07:30 UTC)

Règles ajoutées à `~/.claude/settings.json` pendant la session (empreinte avant
`561789c8…25ce2`), toutes sur des cibles absentes :

| N° | Commande | Règle utilisateur | Décision |
| --- | --- | --- | --- |
| T1 | `python3 -m unittest discover -s ~/lepton-tools-dev/essais/env-62-absent` (forme d'U3) | `Bash(python3 -m unittest discover *)` | `accept config classifier` (deux fois) ; code 1, `ImportError` |
| T2 | idem, `<HOME>/…` absolu | idem | `classifier` ; code 1 |
| T3 | `python3 -m unittest discover -p env62_absent_*.py` | idem | `classifier` ; zsh « no matches found », non lancé |
| T3b | `python3 -m unittest discover -p 'env62_absent_*.py'` | idem | `classifier` ; 0 test |
| T4 | `touch <HOME>/lepton-tools-dev/essais/env-62-essai/temoin-u` | règle exacte | `mode` (écriture dans un répertoire de travail) : témoin sans valeur |
| T5 | `python3 -m unittest discover -p 'env62_temoin_*.py'` | règle exacte, sans joker | `classifier` ; 0 test |
| T6 | `pipx install <HOME>/lepton-tools-dev/essais/env-62-absent` | règle exacte | `classifier` ; code 1, rien installé |
| T7 | `pipx install <HOME>/lepton-tools-dev/essais/env-62-absent-deny` | **`deny`** exact | `classifier` ; code 1 : le `deny` n'a pas été appliqué |

Constat : une modification de `~/.claude/settings.json` en cours de session n'est pas prise en
compte (T7). Les règles de projet le sont (ENV-54, `rapports/env-54-permissions.md`). L'essai à
chaud ne conclut donc pas sur D26. Décision de l'utilisateur : relancer Claude Code, règles
d'essai laissées en place, rejouer T1 à T7 au démarrage, puis retirer les règles.

## 2. D28 — invites à refuser

À compléter : inventaire, rejeu de « ne plus demander ».

Documenté (`permissions`) : « ne plus demander » écrit la règle dans `.claude/settings.local.json` ;
« Rules are evaluated in order: deny, then ask, then allow » ; « a matching ask rule prompts even
when a more specific allow rule also matches the same call ». CHANGELOG 2.1.323 : un `allow` qui
serait écrit dans un `settings.local.json` suivi par git ne vaut que pour la session.
`.claude/settings.local.json` n'est pas suivi ici (ignoré par `~/.gitignore_global:5`).

## 3. D27 — outils de comparaison des consignes VM

À compléter. Relevés faits :
- `po/fr.po` de git `v2.47.3` (sha256 `62fbd300…cb8b8`) : `msgstr "fatal : "` (U+00A0) ;
  « La branche distante %s n'a pas été trouvée dans le dépôt amont %s » ; « et que le dépôt
  existe. ». Le motif de `fr()` (`consignes/env-61-debian.md:172`) porte une espace ordinaire.
- `env-61-debian/11-fixture56/f05.err`, `f06.err` : `fatal\xa0: La b…`.
- `f12a.depots`, `f12b.depots` l. 3 : `depots/.mirrors/localhost/home` (VM) contre `…/Users`
  (Mac) : le parent de `<HOME>`, que `norm()` (`env-56-scion/fixture.py:81-83`) ne remplace pas.
- `LC_ALL=C` : fixé par `env-56-scion/essai.sh:15`, `env-59-tilde/essai.sh:15`,
  `env-60-scion/essai.sh:16`, `env-60-scion/fixture.py:32` ; absent d'`env-56-scion/fixture.py`.
