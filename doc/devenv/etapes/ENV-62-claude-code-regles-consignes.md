# Étape ENV-62 — Claude Code : règle U3, invites à refuser, outils des consignes VM (D26, D28, D27)

## Contexte
Révision du plan du 2026-11-18, faite à partir de `HORS-PLAN.md`. D26, D27 et D28 sont à traiter
(décision de l'utilisateur du 2026-11-17, fin du plan, après ENV-61). Ce ne sont pas des tickets :
aucun ne porte sur le code d'un greffon du rootstock (décision du 2026-11-18). Les trois constats
viennent d'ENV-61 et ont été ajoutés au hors-plan au PA-110 :
- **D26** : sur la VM, la règle utilisateur `Bash(python3 -m unittest discover *)` (D19, gardée
  au PA-103) n'a pas décidé de U3, `python3 -m unittest discover -s
  ~/lepton-tools-dev/essais/env-61-absent`. Décision : `accept config classifier`. U1 et U2 ont été
  décidés par `subcommandResults`. Aucune décision ne porte `ruleSource userSettings`. Cause non
  établie (`rapports/env-61-debian.md` §3.2, §9 écart 4 ; `rapports/env-61-mac.md` §5).
- **D28** : des invites à refuser ont été confirmées par erreur, chaque fois sans effet grâce à
  une cible absente : N4 (ENV-57), A1 (ENV-58), A2 au Mac et A1 sur la VM (ENV-61). Choisir « ne
  plus demander » sur une commande soumise à une règle `ask` est relevé `user_permanent`. Rien
  n'est écrit, et l'invite suivante paraît quand même (Claude Code 2.1.326 ;
  `rapports/env-61-mac.md` §1.3, §1.6, §4 ; `rapports/env-61-debian.md` §9 écart 3).
- **D27** : les outils de comparaison des consignes VM ont quatre défauts, tous corrigés ou
  contournés pendant R61-1 (`rapports/env-61-debian.md` §9 écarts 2 et 5 ;
  `rapports/env-61-mac.md` §5) :
  - `fr()` (`consignes/env-61-debian.md:172`) n'admet pas l'espace insécable (U+00A0) que git
    2.47.3 en français écrit dans « fatal : » ;
  - `rapports/env-56-scion/fixture.py` ne fixe pas `LC_ALL`. `rapports/env-56-scion/essai.sh`
    (l. 15) et `rapports/env-60-scion/fixture.py` (l. 32) le fixent ;
  - le segment d'hôte `depots/.mirrors/localhost/Users` (Mac) ou `…/home` (Debian) n'est pas
    normalisé dans les `.depots` de f12a et f12b ;
  - le contrôle D17 du §6 cherchait un texte de l'ancien code (`expanduser().resolve()`).

Faits relevés à la révision (`main` 24ca20a) :
- règles du dépôt, `.claude/settings.json` : 7 `allow`, 5 `ask` (`scion graft-update`,
  `scion seed-update`, `git push`, `git * push`, `git * push *`), 5 `deny` (formes de
  `git clone`) ;
- écarts entre le Mac et la VM, qui pèsent sur le lieu de l'essai de D26 :
  - Mac : aucune règle utilisateur (`rapports/env-61-mac.md` §1.6) ; `~/.claude/settings.json`
    sans `permissions` ni `autoMode` ;
  - Mac : `.claude/settings.local.json` (non versionné) porte 3 `allow` que le dépôt ne documente
    pas : `Bash(git fetch *)`, `Bash(echo "code=$?")`, et un `Read(…)` sous
    `essais/env-60-fixture/`. Il porte aussi 4 `ask` `gh` et 2 `additionalDirectories`
    (`handoff/env-61.md`). Au Mac, `cmd; echo "code=$?"` peut donc être accepté par
    `localSettings`, alors que sur la VM il va au classifieur ;
  - VM : aucun `settings.local.json` ; `~/.claude/settings.json` porte un bloc `autoMode`
    (`rapports/env-61-debian.md` §3.1) ;
  - Claude Code : 2.1.327 au Mac (relevé le 2026-11-18), 2.1.326 sur la VM. D26 et D28 datent de
    2.1.326 ;
- sources sur D26, non concluantes :
  - notes de version 2.1.325-2.1.326 : « Changed auto mode to ignore some wildcard shell allow
    rules », sans dire lesquelles (`rapports/env-58-formes.md` §3) ;
  - pour `Bash(python3 -m unittest discover *)` : « Non documenté (`python3` littéral, le joker
    est dans les arguments) » (`rapports/env-58-formes.md` §4) ;
  - les « Wildcarded interpreters like `Bash(python*)` » sont écartés à l'entrée en mode auto
    (`rapports/env-54-permissions.md` §3, point 2) ;
  - le journal porte un `reasonCode` (exemple `subcommands:bashMiss:shell-expansion+rule:…`,
    `rapports/env-61-mac.md` §1.3) que `rapports/env-57-mac/decisions.py` ne relève pas. U3
    contient un `~/…`.

Archétype : infrastructure. Aucun fichier de l'arbre Lepton, de scion ni du code de lepton n'est
touché ; aucun binaire ni aucun lien du trunk ne change. Cette étape décide et écrit. Les
décisions sur la VM sont appliquées et prouvées en ENV-66 (même partage qu'ENV-58 et ENV-61).
Les trois points sont indépendants : un lot par point, chacun avec sa décision au PA-111.

## Prérequis
- ENV-61 terminée ; lepton-tools `main` après la fusion de la révision du 2026-11-18.
- Mécanisme des règles : `rapports/env-54-permissions.md` §3 ; formes : ORCHESTRATION §2bis
  (PA-103, `rapports/env-58-formes.md` §2).
- Outils à réutiliser plutôt qu'à réécrire :
  - `rapports/env-57-mac/decisions.py` : `python3 -I decisions.py <journal .jsonl> [--motif …]` ;
  - `rapports/env-58-formes/ask-script.sh` ;
  - relevés réels de la VM et du Mac : `rapports/env-61-debian/11-fixture56/`,
    `rapports/env-61-mac/attendu/fixture56/`.
- Accord PA-P donné au plan de session pour toute invite `ask` de l'étape (cibles absentes).
- Documentation de Claude Code : agent `claude-code-guide`, en lecture seule, qui cite les notes
  de version.
- Skill `lepton-cibles` (forme des tests).
- Branche `devenv/env-62` dans lepton-tools seulement.

## Tâches

### 1. Audit → PA-111
Lecture seule, sauf l'essai témoin de D26 et le rejeu de D28 ci-dessous. Rapport
`rapports/env-62-claude-code.md`.
- **D26**. Établir la cause de la décision U3 :
  - documentation : traitement des règles d'interpréteur et des jokers en mode auto, et des
    arguments `~/…` dans une règle `*` ;
  - `reasonCode` des décisions : outil nouveau, versionné sous `rapports/env-62-claude-code/`
    (`decisions.py` est un relevé, il n'est pas modifié). Entrée U3 du journal de la VM
    `3498db03-….jsonl`, si elle existe encore : demandée à l'utilisateur ;
  - essai témoin sous `~/lepton-tools-dev/essais/env-62-essai/` : U3 et une commande voisine
    (sans `~`, sans `-s`), décisions relevées. Lieu de la règle d'essai, au plan de session :
    `.claude/settings.local.json` du Mac, réglages utilisateur du Mac, ou rien au Mac (relevé
    sur la VM en ENV-66). <À CONFIRMER au plan de session>. Pour toute écriture dans un fichier
    de réglages du Mac :
    - empreinte du fichier avant et après ;
    - règle retirée à la fin de l'essai, empreinte revenue à l'avant ;
    - pour `~/.claude/`, vérifier que le hook de sauvegarde a créé l'archive (`CLAUDE.md`
      utilisateur) ;
  - pour la règle de la VM : ce qu'elle couvre en mode auto ; si une commande prévue d'ENV-63 à
    ENV-66 en dépend.
- **D28**. Inventaire de chaque invite à refuser prévue par une consigne ou une étape (A1 à A3,
  N4, contrôles négatifs), avec la forme de l'annonce faite à l'utilisateur. Puis :
  - les invites confirmées par erreur : moment, texte de l'annonce, décision relevée ;
  - « ne plus demander », rejoué une fois au Mac sous 2.1.327 :
    `scion graft-update -v ~/lepton-tools-dev/essais/env-62-absent`, lancé par la session hors
    script, cible absente. Relever la décision, l'invite suivante, et les empreintes de
    `.claude/settings.json`, `.claude/settings.local.json`, `~/.claude/settings.json` et
    `~/.claude.json`, avant et après. Si un fichier change : la règle écrite est retirée, le
    fichier et les empreintes vont au rapport, et l'archive est vérifiée pour `~/.claude/`.
- **D27**. Pour chaque défaut : fichier, ligne, effet en R61-1, parade appliquée. Lister les
  outils de comparaison des consignes, avec leur chemin, et dire lesquels fixent `LC_ALL`,
  normalisent `<HOME>` et le segment d'hôte, et d'où viennent les traductions de git :
  - `fr()` (`consignes/env-61-debian.md:172`) ;
  - `rapports/env-56-scion/fixture.py`, `rapports/env-60-scion/fixture.py` ;
  - `rapports/env-56-scion/essai.sh`, `rapports/env-59-tilde/essai.sh`,
    `rapports/env-60-scion/essai.sh` ;
  - `rapports/env-59-tilde/classer.py` ;
  - `rapports/env-57-mac/decisions.py`.
- **PA-111** : l'utilisateur tranche :
  - D26 : la cause retenue ; le sort de la règle de la VM (gardée, réécrite dans une forme que
    le mode auto garde, ou retirée) ; la personne qui modifie `~/.claude/settings.json` de la VM,
    et quand (proposition : forme du §0 d'ENV-61 ; la VM n'écrit que son rapport,
    ORCHESTRATION §2). <À CONFIRMER au PA-111> ;
  - règles du dépôt (`.claude/settings.json`) ajoutées ou changées ;
  - D28, parade côté consignes. Options :
    - annoncer chaque invite à refuser par un `AVANCEMENT` « À REFUSER », avant de la lancer ;
    - garder la cible absente obligatoire (déjà la règle des étapes et des consignes : ENV-58,
      `consignes/env-61-debian.md:175`) ;
    - remplacer le contrôle interactif par la lecture de la règle `ask` (`settings.json`), et
      ne plus lancer l'invite.
    <À CONFIRMER au PA-111> ;
  - D28, défaut de Claude Code : le documenter au §2bis seulement, le signaler à Anthropic (envoi
    externe, fait par l'utilisateur ou sur son accord), ou le garder hors plan ;
  - D27 : texte de l'amendement des « Règles des consignes VM » (§2bis). Contenu proposé :
    - `LC_ALL=C` dans chaque outil qui compare des sorties ;
    - traductions de git tirées de `po/fr.po`, octet pour octet ;
    - normalisation du segment d'hôte sous `depots/.mirrors/<hôte>/` ;
    - un contrôle de correction est vérifié contre le code installé au Mac avant d'écrire la
      consigne.
    <À CONFIRMER au PA-111> ;
  - D27, forme : outil commun sous `scripts/`, outils des `rapports/env-*/` corrigés, ou règles
    seules. <À CONFIRMER au PA-111> ;
  - effets sur `CLAUDE.md` du dépôt et sur les skills.
- Aucune modification avant la réponse.

### 2. Mise en place (`devenv/env-62`)
- Amender ORCHESTRATION §2bis selon le PA-111 : le paragraphe des réglages de la VM (D26), les
  règles des consignes VM (D27, D28).
- Règles du dépôt, si le PA-111 en change : `.claude/settings.json` reste du JSON valide
  (`python3 -m json.tool`) ; hook toujours déclaré.
- Outil commun, si le PA-111 en crée un : tests sous `tests/`, shellcheck s'il s'agit d'un script
  shell.
- Skills et `CLAUDE.md` du dépôt, seulement si le PA-111 le décide. Une skill se corrige sur le
  compte claude.ai, puis `scripts/importer-skills.sh` la copie : un commit dédié et une ligne de
  journal par objet (ORCHESTRATION §5bis).
- Rapport §D26 : le bloc `permissions.allow` attendu sur la VM, et lui seul, si le PA-111 le
  change (forme du rapport d'ENV-58).

### 3. Contrôles → PA-112
- Rejouer l'essai témoin de D26 si une règle a changé, et relever la décision.
- D27 : passer les outils retenus sur les sorties réelles de la VM,
  `rapports/env-61-debian/11-fixture56/` (U+00A0 dans `f05.err` et `f06.err`,
  `depots/.mirrors/localhost/home` en l. 3 de `f12a.depots`). Comparer à
  `rapports/env-61-mac/attendu/fixture56/` : 0 écart pour f05, f06, f12a et f12b. Pas de
  simulation au Mac : c'est le piège d'ENV-61 (`rapports/env-61-mac.md` §5).
- `pytest` complet vert (527 au départ, plus les nouveaux), dans la forme couverte.
- **PA-112** : rapport ; sort d'`essais/env-62-essai` (par `scripts/supprimer-essai.sh`) ; push et
  fusion de `devenv/env-62` dans `main` (PA-P). La preuve sur la VM est faite en ENV-66.

## Critères de validation
- [ ] PA-111 et PA-112 tranchés et consignés.
- [ ] D26 : cause établie, ou essai qui la laisse ouverte, et décision relevée au rapport.
- [ ] D28 : inventaire des invites à refuser ; rejeu de « ne plus demander » sous 2.1.327.
- [ ] D27 : chaque défaut avec sa parade ; 0 écart sur les sorties réelles de la VM.
- [ ] Fichiers de réglages du Mac revenus à leur empreinte d'avant ; `settings.json` en JSON
      valide s'il change ; `pytest` complet vert.
- [ ] `HORS-PLAN.md` : D26 et D28 « décidé, appliqué en ENV-66 », D27 « traité en ENV-62,
      preuve sur la VM en ENV-66 », avec renvoi au rapport.

## Pièges connus
- Le classifieur n'est pas déterministe : une acceptation par lui n'établit pas une règle. Seules
  comptent les décisions marquées règle ou invite.
- Une invite `ask` confirmée par erreur sur une cible existante a un effet réel : jamais de cible
  existante dans un essai de refus.
- Le refus d'une invite interrompt le tour : la session reprend sur un message de l'utilisateur.
- Une lecture groupée qui cite une commande `ask` déclenche l'invite (ENV-54 §10.2, O-0) :
  chercher par l'outil Grep, ou par un motif qui ne la cite pas (`graft.update`).
- Une règle écrite dans `~/.claude/settings.json` du Mac s'applique à toutes les sessions du Mac
  tant qu'elle n'est pas retirée.
- Les `allow` de `.claude/settings.local.json` du Mac faussent la comparaison avec la VM : un
  essai au Mac relève `localSettings` là où la VM relève le classifieur.
- Le constat D28 sous 2.1.326 peut ne plus valoir sous 2.1.327 : relever la version à chaque
  essai.
- L'espace insécable ne se voit pas au terminal : comparer par `od -c` ou par Python.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, branche, §Versions (Claude Code), décisions PA-111 et PA-112,
journal. `HORS-PLAN.md` : D26, D27, D28. Passation `handoff/env-62.md`.
