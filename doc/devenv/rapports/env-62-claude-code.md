# ENV-62 — Claude Code : règle U3, invites à refuser, outils des consignes VM (D26, D28, D27) — rapport

Tâche 1 (audit), présenté au PA-111. Mac, Claude Code **2.1.328** (2.1.327 à la
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

### 1.3 Journal de la VM (R61-1)

Copie fournie par l'utilisateur : `<HOME>/Documents/3498db03-cbec-4248-9c02-7e12b5aab1d2.jsonl`
(856 lignes, sha256 `39f35cae…14ad`, non versionnée), lue par `raisons.py` :

| Heure UTC | Commande | `permissionDecision` |
| --- | --- | --- |
| 15:52:39 | `pipx install --force ~/lepton-tools-dev/lepton-tools` | `accept config rule projectSettings` |
| 15:56:03 | U1 `pipx install ~/…/env-61-absent` | `{"decision": "accept", "source": "config", "reasonType": "subcommandResults"}` |
| 15:56:09 | U2 `git clone --depth 1 https://github.com/lepton-distribution/env-61-absent.git ~/…` | `subcommandResults` |
| 15:56:14 | U3 `python3 -m unittest discover -s ~/…/env-61-absent` | `{"decision": "accept", "source": "config", "reasonType": "classifier"}` : ni `reasonCode` ni `ruleSource` |
| 15:58:28 | A1 (1er) | `accept user_temporary projectSettings`, `reasonCode` `rule:projectSettings`, `grantScope` `once` |

- L'entrée U3 ne porte que le champ `serverClassifierContext` en plus : état git, `live_cwd`,
  `platform`, sans motif. Le journal ne donne donc pas la cause.
- **Version** : les 451 entrées qui portent un champ `version` disent **2.1.325**, depuis le début
  de la session (11:29:14 UTC). Le rapport VM relève 2.1.326 par `claude --version` (version
  installée sur disque, pas celle du processus en cours). D26 est donc constaté sous 2.1.325,
  avant le changement de 2.1.326 (« ignore some wildcard shell allow rules »).
- Les règles utilisateur de la VM datent de R57-1 (10 nov.) : elles étaient en place au démarrage
  de la session. La réécriture du fichier par `/model` (17 nov. 16:44 locale) n'a pas changé le
  bloc `permissions`. Ce n'est donc pas le défaut de relecture à chaud du §1.2.
- U1 et U2 portent `subcommandResults`, la même forme que les règles du dépôt (F1, F3, F6) ; U3
  seul va au classifieur. Piste : la règle d'interpréteur `python3 -m …` est écartée en mode auto
  (« broad allow rules that grant arbitrary code execution ») déjà sous 2.1.325. À établir par
  l'essai après relance (§1.4).

### 1.4 Essai témoin après relance (2026-11-19, 07:41 UTC, processus 2.1.328)

Session reprise par `claude --continue` (même journal ; entrées `version` 2.1.328), règles du §1.2
présentes au démarrage :

| N° | Commande | Règle utilisateur | Décision |
| --- | --- | --- | --- |
| T1 | `python3 -m unittest discover -s ~/…/env-62-absent` (forme d'U3) | `Bash(python3 -m unittest discover *)` | `accept config classifier` |
| T2 | idem, `<HOME>/…` absolu | idem | `classifier` |
| T3b | `python3 -m unittest discover -p 'env62_absent_*.py'` | idem | `classifier` |
| T5 | `python3 -m unittest discover -p 'env62_temoin_*.py'` | règle exacte `Bash(python3 -m unittest discover -p 'env62_temoin_*.py')` | `accept config subcommandResults` |
| T6 | `pipx install <HOME>/…/env-62-absent` | règle exacte | `accept config rule userSettings` ; code 1, rien installé |
| T7 | `pipx install <HOME>/…/env-62-absent-deny` | `deny` exact | `reject config rule userSettings`, `reasonCode` `rule:userSettings` |

Conclusions :
- **`~/.claude/settings.json` n'est lu qu'au démarrage de la session** (T6, T7 après relance,
  contre §1.2 à chaud). Les règles du dépôt, elles, sont relues à chaud (ENV-54).
- **Cause de D26** : en mode auto, la règle à joker `Bash(python3 -m unittest discover *)` est
  écartée, avec ou sans `~`, avec ou sans `-s` (T1, T2, T3b). Une règle exacte sur la même
  commande reste appliquée (T5), comme une règle exacte hors interpréteur (T6). C'est la règle
  documentée (« broad allow rules that grant arbitrary code execution are dropped […] Narrow
  rules like `Bash(npm test)` stay in effect », `permission-modes`) : `python3 -m <module> *`
  exécute du code arbitraire. Constaté sous 2.1.325 (VM, §1.3) et 2.1.328 (Mac) ; la source de la
  règle n'y change rien (`userSettings` ici et sur la VM).
- Le `~` n'est pas en cause (T1 et T2 identiques).
- U1 (`Bash(pipx install:*)`) et U2 (`Bash(git clone * https://…/*)`) restent appliquées sur la
  VM (`subcommandResults`, §1.3).
- Dépendance des étapes suivantes : seul `etapes/ENV-66-validation-debian.md:32-33` cite la
  commande, pour le contrôle U3 lui-même. Aucune commande d'ENV-63 à ENV-66 ne dépend de la règle.

Remise en état : règles retirées par l'outil Edit ; empreinte de `~/.claude/settings.json`
revenue à `561789c8…25ce2` (avant). Les règles retirées restent chargées dans le processus en
cours jusqu'à son arrêt (cibles absentes, sans effet).

## 2. D28 — invites à refuser

### 2.1 Inventaire

| Étape | Invite à refuser | Annonce faite à l'utilisateur | Décision relevée |
| --- | --- | --- | --- |
| ENV-54 (Mac) | N4 `scion graft-update -v ~/…/env-54-absent` (règle `ask`) | au plan de session | refusée (`rapports/env-54-permissions.md` §9) |
| ENV-57 (VM) | N4, idem `env-57-absent` | `AVANCEMENT` « N4 lancé, refus attendu de l'utilisateur » (après le lancement) | 1re **confirmée** `user_temporary projectSettings`, sans effet ; rejouée, refusée |
| ENV-58 (Mac) | A1 directe `env-58-absent` | plan de session | **confirmée** `user_temporary projectSettings`, sans effet (`rapports/env-58-formes.md` §2) |
| ENV-61 (Mac) | A2 `bash …/ask-script.sh ~/…/env-61-absent` (hook G2) | préparation, §1.6 | **confirmée** `user_temporary`, sans effet (`rapports/env-61-mac.md` §1.6) |
| ENV-61 (VM) | A1, A2, A3 (`consignes/env-61-debian.md` §8.3) | `AVANCEMENT` avant A1 (consigne l. 381-384) | A1 1re **confirmée** `user_temporary projectSettings` (15:58:28 UTC), sans effet ; A1 rejouée, A2, A3 `rejet-invite` |
| ENV-62 (Mac) | n° 2 `scion graft-update -v ~/…/env-62-absent` | « À REFUSER », dans le message qui précède le lancement | `rejet-invite` (07:44:31 UTC) |
| ENV-66 (VM, prévu) | invites à refuser « dans la forme décidée au PA-111 » (`etapes/ENV-66-validation-debian.md:78`) | — | — |

Les quatre confirmations par erreur ont toutes porté sur une cible absente : aucun effet. Aucune
n'était précédée d'une annonce placée juste avant le lancement, dans le même message ; l'annonce
était au plan, dans la consigne, ou dans un `AVANCEMENT` envoyé après le lancement.

### 2.2 Rejeu de « ne plus demander » (Mac, 2.1.328, 2026-11-19)

| N° | Annonce | Décision | Effet |
| --- | --- | --- | --- |
| 1 | « À CONFIRMER par « Oui, et ne plus demander » » | `accept user_temporary projectSettings`, `reasonCode` `rule:projectSettings`, `grantScope` `once` | code 1, « n'est pas un rootstock » ; cible absente |
| 2 | « À REFUSER » | `rejet-invite` | aucun |

- Réponse de l'utilisateur : l'invite n° 1 **ne proposait pas** « ne plus demander » ; il a choisi
  « Oui ». Sous 2.1.326 (ENV-61, `rapports/env-61-mac.md` §1.3), l'option paraissait et était
  relevée `user_permanent` sans rien écrire.
- L'invite n° 2 a paru : une confirmation n'en dispense pas la suivante.
- Empreintes avant et après identiques (`essais/env-62-essai/empreintes-d28-avant.txt`) :
  `.claude/settings.json` `b01ad557…d235`, `.claude/settings.local.json` `83833a45…21e2`,
  `~/.claude/settings.json` `561789c8…25ce2`, `~/.claude.json` `58b6009e…4edf` ; `allowedTools`
  du projet vide.
- Documenté (`permissions`) : « ne plus demander » écrit la règle dans
  `.claude/settings.local.json` ; « Rules are evaluated in order: deny, then ask, then allow » ;
  « a matching ask rule prompts even when a more specific allow rule also matches the same
  call ». Une règle `allow` écrite n'aurait donc pas supprimé l'invite. CHANGELOG 2.1.323 : un
  `allow` qui serait écrit dans un `settings.local.json` suivi par git ne vaut que pour la
  session ; ici, `.claude/settings.local.json` n'est pas suivi (`~/.gitignore_global:5`).
- Conclusion : le défaut de Claude Code relevé en ENV-61 ne se reproduit plus en 2.1.328, faute
  d'option. Le reste de D28 est une erreur de manipulation, que la conduite des invites doit
  parer.

## 3. D27 — outils de comparaison des consignes VM

### 3.1 Défauts

| Défaut | Fichier, ligne | Effet en R61-1 | Parade appliquée |
| --- | --- | --- | --- |
| `fr()` n'admet pas U+00A0 | `consignes/env-61-debian.md:172` | `f05.err`, `f06.err` non ramenés (`fatal\xa0: La branche distante…`) | QUESTION R61-1, option 1 : variante à espace insécable, écart de comparaison accepté |
| `LC_ALL` non fixé | `env-56-scion/fixture.py` (aucune ligne ; `subprocess` sans `env`) | git en français dans `f05.err`, `f06.err` | même parade |
| segment d'hôte non normalisé | `env-56-scion/fixture.py:81-83` (`norm()` : `<B>`, `<HOME>`) | `f12a.depots`, `f12b.depots` l. 3 : `depots/.mirrors/localhost/home` (VM) contre `…/Users` (Mac), le parent de `<HOME>` | `/home` → `/Users`, écart accepté |
| contrôle D17 sur l'ancien texte | `consignes/env-61-debian.md:296` (`"expanduser().resolve()" in inspect.getsource(…)`) | `False` sur le code corrigé (74c9c97) | QUESTION R61-1, option 1 : identité de `seed.py` + `local = expanded.resolve()` et `file://localhost{local}` (`env-61-debian/6-controle-d17.txt`) |

Source des traductions : `po/fr.po` de git `v2.47.3` (sha256 `62fbd300…cb8b8`) :
`msgstr "fatal : "` (U+00A0), « La branche distante %s n'a pas été trouvée dans le dépôt
amont %s », « et que le dépôt existe. ». `fr()` en reprend les textes, mais avec une espace
ordinaire : la consigne cite `po/fr.po` (l. 180-182) sans l'avoir lu octet pour octet.

### 3.2 Outils de comparaison des consignes

| Outil | `LC_ALL` | `<HOME>` | segment d'hôte | traductions de git |
| --- | --- | --- | --- | --- |
| `fr()` (`consignes/env-61-debian.md:172`) | sans objet (filtre) | non | non | écrites à la main (espace ordinaire) |
| `env-56-scion/fixture.py` | **non** | oui (l. 83) | **non** | aucune |
| `env-60-scion/fixture.py` | `C` (l. 32) | oui (l. 91) | sans objet (aucun miroir) | aucune |
| `env-56-scion/essai.sh` | `C` (l. 15) | oui (l. 127) | sans objet | aucune |
| `env-59-tilde/essai.sh` | `C` (l. 15) | oui (l. 103) | sans objet | aucune |
| `env-60-scion/essai.sh` | `C` (l. 16) | oui (l. 74) | sans objet | aucune |
| `env-59-tilde/classer.py` | non (seul `printf` par `bash -c`, l. 44, sans texte traduit) | oui (l. 60) | sans objet | aucune |
| `env-57-mac/decisions.py` | sans objet (lit le journal) | non (commandes brutes) | sans objet | aucune |

Seule la fixture d'ENV-56 lance scion sans `LC_ALL=C` et crée des miroirs ; c'est l'outil que
reprend le C5 d'ENV-66.

## 4. PA-111 — propositions (à trancher par l'utilisateur)

1. **D26** :
   - cause : §1.4 (règle à joker sur un interpréteur écartée en mode auto, source et `~` sans effet) ;
   - réglages utilisateur lus au démarrage seulement ; la version en cours se lit au champ
     `version` du journal, pas par `claude --version` ;
   - règle `Bash(python3 -m unittest discover *)` de la VM : **retirée** (sans effet en mode auto,
     aucune commande d'ENV-63 à ENV-66 n'en dépend), ou gardée avec une note ;
   - qui et quand : l'utilisateur, au §0 de la consigne d'ENV-66, avant d'ouvrir la session ;
     U3 attendu alors au classifieur, et contrôle positif d'une règle utilisateur (forme de T6) ;
   - règles du dépôt : aucune changée (les règles pytest `~/…/bin/pytest:*` sont restées
     appliquées, F1 en R61-1 ; à recontrôler au pytest de la tâche 3).
2. **D28** : annonce « À REFUSER » dans le message qui précède immédiatement chaque invite à
   refuser (`AVANCEMENT` côté VM, avant le lancement) **et** cible absente obligatoire (déjà la
   règle) ; contrôle interactif gardé. Défaut de Claude Code : documenté au §2bis seulement
   (plus reproductible en 2.1.328).
3. **D27**, amendement des « Règles des consignes VM » :
   - `LC_ALL=C` dans chaque outil qui lance un programme dont la sortie est comparée ;
   - toute traduction de git tirée de `po/fr.po` de la version de la VM, octet pour octet ;
   - normalisation de `<HOME>` et de ses ancêtres sous `depots/.mirrors/<hôte>/` ;
   - un contrôle de correction est vérifié contre le code installé au Mac avant d'écrire la
     consigne.
4. **D27, forme** : correction d'`env-56-scion/fixture.py` (`LC_ALL=C`, segment d'hôte), et outil
   commun de comparaison sous `scripts/` (normalisation des traductions et du segment, tests sous
   `tests/`), appliqué aux sorties réelles de la VM en tâche 3 ; ou règles seules.
5. `CLAUDE.md` et skills : inchangés.

PA-111 tranché le 2026-11-19 : les propositions 1 à 5 sont retenues telles quelles
(`DEVENV-STATUS.md` §Décisions).

## 5. Mise en place (tâche 2)

- `scripts/comparer-releves.py` : compare deux répertoires de relevés après normalisation
  (table `TRADUCTIONS` tirée de `po/fr.po` v2.47.3, U+00A0 compris ; ancêtres de `<HOME>` sous
  `depots/.mirrors/<hôte>/` en `<HOME/..>`, avec le HOME de chaque côté) ; codes 0, 1, 2.
  Tests `tests/test_comparer_releves.py` (10).
- `env-56-scion/fixture.py` : `LC_ALL=C` pour `git init` et scion ; `norm()` remplace les ancêtres
  de `<HOME>` sous `depots/.mirrors/<hôte>/`. Rejoué au Mac (`essais/env-62-essai/f56`, clone
  seed.scions au tag 0.6.3.2, 08a1460, scion 0.6.3.2 de pipx) : code 0, 76 relevés ; contre
  `env-61-mac/attendu/fixture56/` par l'outil commun : seul le nom de la base change
  (`essais/env-61-fixture` → `essais/env-62-essai`, f12a et f12b l. 7), comme en ENV-61 ;
  l. 3 de f12a : `depots/.mirrors/localhost<HOME/..>`.
- ORCHESTRATION §2bis : réglages utilisateur de la VM (2 règles), lecture des réglages au
  démarrage, invites à refuser, outils de comparaison.
- `.claude/settings.json`, `CLAUDE.md`, skills : inchangés.

### D26 : bloc attendu sur la VM après le §0 d'ENV-66

```json
"permissions": {
    "allow": [
        "Bash(pipx install:*)",
        "Bash(git clone * https://github.com/lepton-distribution/*)"
    ]
}
```

## 6. Contrôles (tâche 3)

- D26 : aucune règle du dépôt n'a changé ; la règle de la VM change en ENV-66 (§0). Pas de rejeu
  au Mac au-delà du §1.4.
- D27, sur les sorties réelles de la VM (pas de simulation au Mac) :
  `python3 -I scripts/comparer-releves.py --home-attendu <HOME Mac> --home-obtenu <HOME VM>
  env-61-mac/attendu/fixture56 env-61-debian/11-fixture56` → f05.err, f06.err, f12a.depots,
  f12b.depots `identique`, **écarts=0 / 4** ; les 76 fichiers : **écarts=0 / 76**, code 0. Témoin
  sans `--home-*` : f12a.depots en écart (`écarts=1 / 1`).
- Fichiers de réglages du Mac : `~/.claude/settings.json` revenu à `561789c8…25ce2` (§1.4) ;
  `.claude/settings.json`, `.claude/settings.local.json`, `~/.claude.json` inchangés pendant le
  rejeu de D28 (§2.2). `.claude/settings.json` n'a pas changé (pas de `json.tool` requis).
- pytest complet : `~/lepton-tools-dev/venv-lepton-tools/bin/pytest -q -rs -p no:cacheprovider
  --basetemp <essai>/pytest --junitxml <essai>/pytest.xml` (forme couverte) → **537 passed**
  (527 + 10 de `test_comparer_releves.py`), 7 min 46 ; décision `accept config
  subcommandResults` : la règle `Bash(~/lepton-tools-dev/venv-lepton-tools/bin/pytest:*)` reste
  appliquée en mode auto sous 2.1.328.

## 7. PA-112

À trancher : rapport ; sort d'`essais/env-62-essai` (empreintes, relevés de la fixture, clone de
seed.scions, pytest) par `scripts/supprimer-essai.sh` ; fusion `--no-ff` de `devenv/env-62` dans
`main` et push (PA-P). Copie du journal de la VM dans `<HOME>/Documents/` : hors du dépôt, à
supprimer par l'utilisateur. Preuve sur la VM en ENV-66.
