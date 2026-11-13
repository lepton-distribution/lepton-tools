# Étape ENV-58 — Claude Code : formes des commandes et règles de la VM (D20, D19)

## Contexte
Révision du plan du 2026-11-13, faite à partir de `HORS-PLAN.md` : D20 et D19 sont à traiter
(décision de l'utilisateur du 2026-11-13, fin du plan, après ENV-57). Les règles de permission du
dépôt (`.claude/settings.json`, ENV-54, D16) sont prouvées au Mac et sur la VM. Deux constats
d'ENV-57 restent :
- **D20** : une redirection vers un fichier (`> f 2>&1`) fait sortir une commande de sa règle
  `allow` ; elle passe alors au classifieur. Une règle `ask` vaut avec la redirection
  (`rapports/env-57-mac.md` §1.5). La règle d'écriture « commandes `allow` sans redirection,
  journal par une option de l'outil (`--junitxml`) » figure dans `consignes/env-57-debian.md` §2,
  pas dans ORCHESTRATION §2bis.
- **Portée étendue de D20** (décision de l'utilisateur, révision du 2026-11-13) : un
  `scion graft-update` lancé depuis un script échapperait à la règle `ask`, et irait au
  classifieur. C'est pourquoi `regreffer-essai.sh avant|apres` laisse le `graft-update` à la
  session (`rapports/env-57-mac.md` §1.3, §4 ; `handoff/env-57.md`, pièges). Ce comportement est
  déduit, pas essayé : la garde technique de PA-P en dépend. Le cas `bash -c` est un ajout de la
  révision, soumis au PA-103.
- **D19** : `~/.claude/settings.json` de la VM (10 nov.), hors du dépôt, porte 3 règles `allow`.
  Elles s'ajoutent aux règles du dépôt. Aucune décision relevée en R57-1 ne leur revient
  (`rapports/env-57-debian.md` §1, §9 constat 3 ; `rapports/env-57-mac.md` §5) :
  - `Bash(pipx install:*)`, plus large que la règle exacte du dépôt ;
  - `Bash(git clone * https://github.com/lepton-distribution/*)` ;
  - `Bash(python3 -m unittest discover *)`.

Archétype : infrastructure. Aucun fichier de l'arbre Lepton, de scion ni du code de lepton n'est
touché ; aucun binaire ni aucun lien du trunk ne change. Cette étape décide et écrit. La décision
sur le fichier de la VM est appliquée et prouvée en ENV-61.

## Prérequis
- ENV-57 terminée. lepton-tools `main` après la fusion de la révision du 2026-11-13.
- Règles en place (`.claude/settings.json`, relevé du 2026-11-13) :
  - `allow` : `scripts/supprimer-essai.sh` (deux formes), `pipx install --force
    ~/lepton-tools-dev/lepton-tools`, `git clone file://*`,
    `git clone https://github.com/lepton-distribution/*`, `bin/pytest` des deux venvs ;
  - `ask` : `scion graft-update`, `scion seed-update`, `git push`, `git * push`, `git * push *` ;
  - `deny` : options dangereuses de `git clone` ; hook `PreToolUse` `proteger-trunk.py`.
- Mécanisme établi en ENV-54 (`rapports/env-54-permissions.md` §3) :
  - ordre : hook, puis `deny`, `ask`, `allow`, puis classifieur ;
  - commandes composées : chaque sous-commande doit être couverte ;
  - les listes `permissions.*` des fichiers se cumulent, utilisateur compris ;
  - réglages relus à chaud.
  Le §3 ne dit rien des redirections.
- Outils : `rapports/env-57-mac/decisions.py` (décisions lues dans le journal de session,
  `python3 -I decisions.py <journal .jsonl> [--motif <texte>]`) ;
  `rapports/env-57-mac/regreffer-essai.sh`.
- Textes à confronter :
  - ORCHESTRATION §2bis (« Commandes soumises aux règles de `.claude/settings.json` ») ;
  - `consignes/env-57-debian.md` §2 ;
  - `CLAUDE.md` du dépôt ;
  - skills `.claude/skills/{devenv-session,lepton-rootstock,lepton-oracle,lepton-cibles}`.
- Claude Code 2.1.323 au Mac, mode auto. Documentation : agent `claude-code-guide`, en lecture
  seule.
- Skills `lepton-cibles` (formes des tests et des bancs) et `lepton-rootstock` (copie d'essai pour
  le contrôle du hook).
- Branche `devenv/env-58` dans lepton-tools seulement.

## Tâches

### 1. Audit → PA-103
Lecture seule, sauf l'essai témoin ci-dessous.
- Inventaire au rapport `rapports/env-58-formes.md` §1 :
  - chaque commande couverte par une règle `allow` et écrite avec une redirection, un `| tee` ou un
    `; echo "code=$?"` ;
  - chaque commande `ask` (`graft-update`, `seed-update`, `git push`) écrite dans un script ou
    dans un `bash -c`.
  Où chercher : les skills, `scripts/`, `scripts/oracle/`, les outils de `rapports/*/`, et la
  consigne d'ENV-57, modèle des suivantes. Pour chacune : fichier, ligne, forme.
  - Chercher par l'outil Grep, jamais par une commande Bash qui cite une commande `ask`. Une telle
    recherche déclenche l'invite, ou un refus du classifieur, comme à la relecture de cette
    révision (« Undermining Oversight »). À défaut, utiliser un motif qui ne la cite pas
    (`graft.update`).
  - Un refus n'est pas contourné : il est consigné.
- Essai témoin au Mac, sous `~/lepton-tools-dev/essais/env-58-essai/`. Les décisions sont
  relevées par `decisions.py` et citées au rapport. Les scripts de l'essai sont versionnés sous
  `rapports/env-58-formes/`, pour que la VM les reprenne tels quels en ENV-61 (C2).
  - Commande `allow` (pytest d'un seul test, forme couverte) : nue, `> f`, `2>&1`, `> f 2>&1`,
    `| tee f`, puis `--junitxml f.xml`.
  - Commande `ask` lancée sur une cible absente uniquement : directement, depuis un script de
    l'essai, puis par `bash -c '…'`.
    - Cible : `scion graft-update -v ~/lepton-tools-dev/essais/env-58-absent`.
    - Attendus :
      - forme directe : une invite ;
      - script et `bash -c` : à établir (invite ou classifieur).
    - Toute invite est **refusée** par l'utilisateur. Le refus interrompt le tour ; la session
      reprend sur un message de l'utilisateur.
  - Ne jamais viser une cible existante.
- D19, pour chaque règle utilisateur de la VM :
  - ce qu'elle couvre de plus que les règles du dépôt ;
  - si une commande prévue d'ENV-59 à ENV-61 en dépend. Exemple : sur la VM, scion s'installe
    par `install-debian.sh`, accepté par le classifieur. Le repli de la consigne, la commande
    `pipx install --force "git+https://github.com/lepton-distribution/seed.scions.git@<version>"`
    lancée directement (`consignes/env-57-debian.md` §6), n'est couvert que par
    `Bash(pipx install:*)`, pas par la règle exacte du dépôt ;
  - si le mode auto l'écarte : liste « Wildcarded interpreters » (ENV-54 §3, point 2).
  La session Mac ne lit pas le fichier de la VM. Elle ne connaît que les 3 règles et l'absence de
  `defaultMode` (`rapports/env-57-debian.md` §1) ; les autres clés du fichier sont inconnues.
- **PA-103** : l'utilisateur tranche :
  - texte de l'amendement du §2bis. Contenu proposé :
    - commandes `allow` écrites sans redirection, journal par une option de l'outil ;
    - commandes `ask` lancées hors script et hors `bash -c` ;
    - conduite pour un script qui en a besoin : deux phases, forme de `regreffer-essai.sh`.
    <À CONFIRMER au PA-103> ;
  - garde technique : aucune, une règle de plus, ou une analyse par le hook des scripts lancés.
    <À CONFIRMER au PA-103> ;
  - sort de chaque règle utilisateur de la VM : retirée, gardée, restreinte, ou remplacée par une
    règle du dépôt. <À CONFIRMER au PA-103> ;
  - qui modifie `~/.claude/settings.json` de la VM, et quand. Proposition : l'utilisateur, au
    préalable §0 de la consigne d'ENV-61, d'après le bloc `permissions.allow` donné au rapport.
    La VM n'écrit que son rapport (ORCHESTRATION §2) ;
  - règles du dépôt ajoutées ou changées ;
  - effets sur `CLAUDE.md` du dépôt et sur les skills.
- Aucune modification avant la réponse.

### 2. Mise en place (`devenv/env-58`)
- Amender ORCHESTRATION §2bis selon le PA-103, dans le paragraphe « Commandes soumises aux règles
  de `.claude/settings.json` ».
- Règles du dépôt, si le PA-103 en change : `.claude/settings.json` reste du JSON valide
  (`python3 -m json.tool`) ; hook toujours déclaré.
- Skills, `CLAUDE.md` du dépôt, scripts dont l'inventaire relève une forme fautive : seulement si
  le PA-103 le décide. Un commit dédié et une ligne de journal par objet (ORCHESTRATION §5bis).
- Rapport §D19 :
  - le bloc `permissions.allow` attendu dans `~/.claude/settings.json` de la VM, et lui seul.
    Jamais un fichier complet, qui écraserait des réglages inconnus ;
  - la conduite : le fichier entier est relu avant la modification
    (`python3 -m json.tool ~/.claude/settings.json`), puis comparé après. Seul ce bloc doit
    différer.
- Ne jamais écrire dans `~/.claude/` du Mac pour cette étape. Si le PA-103 le décide malgré tout,
  vérifier que le hook de sauvegarde du `CLAUDE.md` utilisateur a créé l'archive.

### 3. Contrôles → PA-104
- Si `.claude/settings.json` change : rejouer l'essai témoin, plus un contrôle par règle ajoutée.
  Les réglages sont relus à chaud (ENV-54 §3, point 7). Si le rejeu montre le contraire :
  - commiter ;
  - écrire une passation intermédiaire ;
  - l'utilisateur relance Claude Code ;
  - la session reprend ENV-58 par la skill `devenv-session`.
- Le hook refuse toujours une écriture shell sous un `trunk/`. Contrôle : `touch` sous
  `essais/env-58-essai/qemu/trunk/`. La copie `qemu` est faite d'`essais/env-11/qemu` par
  `rsync -a`, sans `build/`.
- `pytest` complet vert (453 après ENV-57, plus les nouveaux), par
  `~/lepton-tools-dev/venv-lepton-tools/bin/pytest`, dans la forme couverte.
- **PA-104** : rapport ; sort d'`essais/env-58-essai` (par `scripts/supprimer-essai.sh`) ; push et
  fusion de `devenv/env-58` dans `main` (PA-P). La preuve sur la VM est faite en ENV-61.

## Critères de validation
- [ ] PA-103 et PA-104 tranchés et consignés.
- [ ] Inventaire des formes fautives au rapport (fichier, ligne).
- [ ] Essai témoin consigné, avec les décisions du journal de session :
      - redirection : règle ou classifieur, pour chaque forme ;
      - `ask` direct, depuis un script et par `bash -c` : invite ou classifieur.
- [ ] ORCHESTRATION §2bis amendé ; `consignes/env-57-debian.md` §2 n'est plus la seule source de
      la règle.
- [ ] Bloc `permissions.allow` attendu sur la VM, et conduite de modification, au rapport (D19).
- [ ] `pytest` complet vert ; `settings.json` en JSON valide s'il change.
- [ ] `HORS-PLAN.md` : D20 marqué traité ; D19 « décidé, appliqué en ENV-61 », avec renvoi au
      rapport.

## Pièges connus
- Le classifieur n'est pas déterministe : une acceptation par lui n'établit pas une règle. Seules
  comptent les décisions marquées règle (`rule`, `subcommandResults`) ou invite
  (`user_temporary`, `rejet-invite`).
- Confirmer par erreur une invite sur une cible existante a un effet réel. D'où les cibles
  absentes. Précédent : N4 d'ENV-57, confirmé sans effet.
- Le refus d'une invite interrompt le tour (ENV-54 §10.2) : prévoir une reprise par message.
- `decisions.py` ne lit que les entrées `user` du journal. Les entrées `api-request-blob` n'ont pas
  la décision (`handoff/env-57.md`).
- Une lecture groupée qui cite `scion graft-update` (`-h` compris) déclenche l'invite
  (ENV-54 §10.2, O-0) : ne pas citer les commandes `ask` dans des lectures.
- Un motif `~/…` est littéral : il ne couvre que les commandes écrites `~/…` (ENV-54 §3, point 5).
- zsh : `echo ====` échoue ; utiliser `echo ---`. zsh ne découpe pas une variable en mots :
  utiliser `bash -c` ou un script, sauf pour les commandes `ask`.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, branche, décisions PA-103 et PA-104, journal. `HORS-PLAN.md` : D20,
D19. Passation `handoff/env-58.md`.
