# Étape ENV-54 — Claude Code : règles de permission ciblées (D16)

## Contexte
Révision du plan du 2026-11-12, faite à partir de `HORS-PLAN.md` : D16 est à traiter (décision de
l'utilisateur du 2026-11-12, fin du plan : « règles de permission ciblées »). Le classifieur de
permissions de Claude Code a refusé des commandes que l'utilisateur avait autorisées :
- `scion graft-update` : « Untrusted Code Integration » en R28-1, puis « Modify Shared
  Resources » en R43-1 et R53-1, sur la VM ;
- `rm -rf` : « Irreversible Local Destruction » en R21-1. En R53-1, les suppressions ont donc
  été confiées d'emblée à l'utilisateur ;
- au Mac, en ENV-53 : une commande qui enchaînait les regreffes de trois rootstocks d'essai
  (« Modify Shared Resources »). L'utilisateur a lancé la suite, `rm -rf` compris.

Sources : `rapports/env-53-debian.md` §7 (écart 2) ; `rapports/env-53-mac.md` §3, §4.

Portée élargie à la révision (décision de l'utilisateur, 2026-11-12) : `scion graft-update`,
`rm -rf` dans les essais, `pipx install`, `git clone` et les lancements de tests. Ce sont les
commandes que la règle « Commandes confiées d'emblée à l'utilisateur » d'ORCHESTRATION §2bis
attribue à l'utilisateur.

Principe : une règle lève le refus technique, jamais l'accord. PA-P reste exigé pour tout
`graft-update` et tout `seed-update`. Le hook `proteger-trunk.py` ne protège que `trunk/` et
`depots/tiers/`. Archétype : infrastructure. Aucun fichier de l'arbre Lepton, de scion ou du code
de lepton n'est touché ; aucun binaire ni aucun lien du trunk ne change.

## Prérequis
- ENV-53 terminée. lepton-tools `main` après la fusion de la révision du 2026-11-12 (D13, D14,
  D16).
- Sources des refus et des acceptations :
  - `rapports/env-53-debian.md` §1 et §7, `rapports/env-53-mac.md` §3 et §4 ;
  - `rapports/env-43-debian.md` (§7.1, constat 3) ; `rapports/env-28-debian.md` (E-2) ;
  - `rapports/env-21-debian.md` (E-2), `rapports/env-15-scion.md` §8 ;
  - ORCHESTRATION §2bis (« Commandes confiées d'emblée à l'utilisateur ») ;
  - tout `rapports/` et `consignes/` : `grep -rn classifieur` ;
  - `handoff/env-53.md` (pièges : `!` en premier caractère du prompt).
- Configuration actuelle (relevé du 2026-11-12) :
  - `.claude/settings.json` du dépôt : hook `PreToolUse` seul (`proteger-trunk.py`), aucune
    règle `permissions` ;
  - `.claude/settings.local.json` : absent, et ignoré par `~/.gitignore_global` ;
  - réglages utilisateur `~/.claude/settings.json` : hook de sauvegarde de `~/.claude/` (CLAUDE.md
    de l'utilisateur), déclenché par `Write|Edit|MultiEdit` seulement ;
  - hook `.claude/hooks/proteger-trunk.py` (`zone_protegee`, l. 105-119), tests
    `tests/test_proteger_trunk.py` (118).
- Hôtes : la session VM travaille dans `~/lepton-tools-dev/lepton-tools`, qui reçoit par git le
  `.claude/` du dépôt. Répertoire personnel : `/Users/cle_d_anton` au Mac, `/home/lepton-user`
  sur la VM.
- Documentation de Claude Code : permissions, mode auto, hooks. La lire par l'agent
  `claude-code-guide`, en lecture seule.
- Skills `lepton-rootstock` (copie d'essai) et `lepton-cibles` (formes des tests et des bancs).
- Branche `devenv/env-54` dans lepton-tools seulement.

## Tâches

### 1. Audit → PA-95
Lecture seule, à une exception près : l'essai témoin ci-dessous est la seule écriture admise avant
le PA-95.
- Inventaire au rapport `rapports/env-54-permissions.md` §1, refus et acceptations. Pour chaque
  entrée : date, hôte, commande exacte, décision et catégorie rapportée, source, et qui a lancé la
  commande au final. Une règle n'est utile que pour ce qui a été refusé.
- Formes réellement employées par le chantier, relevées dans les consignes, les rapports et les
  skills :
  - `scion graft-update` (avec ou sans `-v`) : dans quels rootstocks ;
  - `rm -rf` :
    - `~/lepton-tools-dev/essais/<nom>` ;
    - `<ROOTSTOCK>/build/<preset>` (skill `lepton-cibles`, `scripts/oracle/rejouer-oracle.sh`
      l. 42) ;
    - `~/env-N-journaux` et `~/tmp-pytest` sur la VM ;
  - `pipx install` : `pipx install --force <LEPTON_TOOLS>`,
    `pipx install --force "git+file://<SEED_SCIONS>@<version>"`, et les formes des scripts
    d'installation ;
  - `git clone` : sources et destinations ;
  - tests : `pytest`, tests de scion, `rejouer-oracle.sh`, bancs QEMU.
- Mécanisme, établi par la documentation, puis par l'essai témoin :
  - ordre d'évaluation des règles `deny`, `ask` et `allow`, des décisions d'un hook `PreToolUse`
    et du classifieur du mode auto ;
  - une règle `allow` empêche-t-elle le refus du classifieur ? Le mode auto écarte-t-il certaines
    règles, et lesquelles ?
  - syntaxe des motifs `Bash(...)` : préfixe, `:*`, commandes composées (`&&`, `;`, `|`),
    variables, `~` ;
  - fichiers et priorité : projet `.claude/settings.json`, `.claude/settings.local.json`,
    utilisateur `~/.claude/settings.json` ; moment où les réglages sont relus ;
  - version de Claude Code au Mac ; celle de la VM sera relevée en ENV-57.
- Essai témoin au Mac, avant toute règle, sous `~/lepton-tools-dev/essais/env-54-essai/` :
  - `graft-update` : sur accord PA-P, dans la copie `essais/env-54-essai/qemu`, faite d'`essais/env-11/qemu`
    par `rsync -a` sans `build/` ;
  - `rm -rf` : d'un répertoire créé pour l'essai ;
  - `git clone` : d'un dépôt local vers `essais/env-54-essai/` ;
  - `pipx install` : forme à fixer avec l'utilisateur avant l'essai. Les options sont des
    `PIPX_HOME` et `PIPX_BIN_DIR` temporaires sous `essais/env-54-essai/`, ou la réinstallation
    de la même version depuis `main`. <À CONFIRMER avant l'essai>. `pipx install --force`
    remplace l'outil de `~/.local/bin` ;
  - tests : `pytest` de lepton-tools.
  Pour chaque commande : acceptée ou refusée, motif. Ne jamais contourner un refus.
- Analyse des risques au rapport :
  - le hook ne refuse pas un `rm -rf` de la racine d'un rootstock : `<ROOTSTOCK>`, ou un
    rootstock d'essai entier. Seule la règle ou l'enveloppe retenue le borne ;
  - aucune règle ne doit bloquer `rm -rf <ROOTSTOCK>/build/<preset>` (procédure d'oracle) ;
  - les motifs par préfixe face à `..`, aux variables et aux jokers ;
  - aujourd'hui, le classifieur fait aussi respecter PA-P techniquement. Une règle `allow` sur
    `graft-update` supprime cette barrière ; une règle `ask` la garde ;
  - aucun motif `git` ne doit couvrir `git push` ;
  - `pipx install` d'une source inattendue ; `git clone` vers une destination protégée.
- **PA-95** : l'utilisateur tranche :
  - mécanisme : règles de permission, décision d'un hook, ou repli sur la règle du §2bis (D16
    clos sans règle) : <À CONFIRMER au PA-95> ;
  - fichier : projet versionné (commun au Mac et à la VM), `settings.local.json` par hôte, ou
    réglages utilisateur : <À CONFIRMER au PA-95> ;
  - pour chaque commande : `allow` ou `ask`, et le motif ; `ask` est l'option proposée pour
    `graft-update` et `seed-update` (PA-P). <À CONFIRMER au PA-95> ;
  - bornes de `rm -rf` et sort des chemins hors de `essais/` (`build/<preset>`, journaux de la VM,
    `~/tmp-pytest`). Option : un script d'enveloppe qui vérifie la cible. <À CONFIRMER au PA-95> ;
  - commandes laissées à l'utilisateur ;
  - texte de l'amendement du §2bis ; effets sur `CLAUDE.md` du dépôt, les skills et les
    consignes VM.
- Aucune modification avant la réponse.

### 2. Mise en place (`devenv/env-54`)
- Écrire les règles retenues au PA-95. Si la session ne peut pas écrire un fichier de réglages
  (refus, demande de confirmation), elle donne le texte exact au rapport ; l'utilisateur
  l'applique, et la session vérifie le contenu.
- Garder le hook déclaré dans `.claude/settings.json`. Le fichier doit rester du JSON valide :
  `python3 -m json.tool`.
- Script d'enveloppe, s'il est retenu : dans `scripts/`, avec des tests `pytest`. Les tests
  couvrent le refus de chaque cible interdite, dont `<ROOTSTOCK>` et un rootstock d'essai entier,
  et l'acceptation de `build/<preset>` si le PA-95 la garde.
- ORCHESTRATION §2bis : amender « Commandes confiées d'emblée à l'utilisateur » selon le PA-95.
- `CLAUDE.md` du dépôt et skills : seulement si le PA-95 le décide, par un commit dédié et une
  ligne de journal (ORCHESTRATION §5bis).
- Une écriture sous `~/.claude/` par Write ou Edit déclenche la sauvegarde du `CLAUDE.md` de
  l'utilisateur : vérifier que l'archive est créée. Une écriture par Bash ne la déclenche pas :
  lancer alors la commande de sauvegarde à la main.

### 3. Contrôles → PA-96
- Les réglages sont relus au démarrage. Avant le rejeu :
  - commiter l'état sur `devenv/env-54` ;
  - écrire une passation intermédiaire `handoff/env-54.md` ;
  - l'utilisateur relance Claude Code dans `<LEPTON_TOOLS>`. C'est toujours ENV-54 : la session
    reprend par la skill `devenv-session`.
- Rejouer l'essai témoin du §1, `graft-update` sur accord PA-P : chaque commande retenue est
  lancée par la session, sans refus. Une commande encore refusée est consignée, jamais
  contournée ; l'utilisateur la lance, et le PA-96 en tranche le sort.
- Contrôles négatifs, toujours sur des cibles absentes : `rm -rf` hors des bornes, et
  `graft-update` hors des essais. Ils restent refusés, ou soumis à confirmation, selon le PA-95.
  Un contrôle vivant ne vise jamais une cible existante hors des essais jetables.
- Le hook reste actif : une écriture shell sous `essais/env-54-essai/qemu/trunk/`
  (`touch …/trunk/essai-hook`) est refusée par le hook.
- `pytest` complet vert (384 après ENV-53, plus les nouveaux), dont `tests/test_proteger_trunk.py`
  (118).
- **PA-96** : rapport ; sort d'`essais/env-54-essai` ; push et fusion de `devenv/env-54` dans `main`
  (PA-P). La preuve sur la VM est faite en ENV-57.

## Critères de validation
- [ ] PA-95 et PA-96 tranchés et consignés.
- [ ] Inventaire des refus, des acceptations et des formes de commandes au rapport.
- [ ] Mécanisme établi, avec sa source (page de documentation, essai).
- [ ] Essai témoin rejoué après redémarrage : chaque commande retenue est acceptée, chaque
      contrôle négatif est refusé ou soumis à confirmation. Le journal de session est cité.
- [ ] Le hook refuse toujours une écriture sous un `trunk/` ; `settings.json` est du JSON valide.
- [ ] `pytest` complet vert ; hook inchangé, ou modifié et testé selon le PA-95.
- [ ] ORCHESTRATION §2bis amendé.
- [ ] `HORS-PLAN.md` : D16 marqué traité, ou clos selon le PA-95, avec renvoi au rapport.

## Pièges connus
- Le classifieur n'est pas déterministe : la preuve est un essai consigné, pas un test
  automatique. Une acceptation au Mac ne prouve rien pour la VM (ENV-57).
- Une commande composée peut être refusée alors que ses parties, lancées seules, seraient
  acceptées. Exemple : la commande refusée au Mac en ENV-53 enchaînait trois rootstocks et un
  `sed -i` (`rapports/env-53-mac.md` §4). Préférer des commandes simples.
- `!` en premier caractère du prompt lance la commande dans le shell de l'utilisateur. Une espace
  devant `!` en fait un simple message (`handoff/env-53.md`).
- Le hook ne protège que `trunk/` et `depots/tiers/` (`zone_protegee`). `rm -rf /tmp/essai` est
  admis par ses tests (`tests/test_proteger_trunk.py` l. 151), de même que `rm -rf` d'une racine
  de rootstock.
- PA-P : une règle qui accepte `graft-update` ne dispense pas de l'accord de l'utilisateur.
- Les chemins absolus diffèrent entre le Mac et la VM : un motif écrit pour l'un ne vaut pas pour
  l'autre.
- `zsh` ne découpe pas une variable en mots : utiliser `bash -c` ou un script.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, branche, décisions PA-95 et PA-96, journal. `HORS-PLAN.md` : D16.
Passation `handoff/env-54.md`.
