# ENV-54 — Claude Code : règles de permission ciblées (D16) — audit du 2026-11-13

Session Mac, branche lepton-tools `devenv/env-54` (depuis `main` 4bed93c). Claude Code 2.1.323,
mode auto. Journal de session : `~/.claude/projects/-Users-cle-d-anton-lepton-tools-dev-lepton-tools/75453a27-c3e9-424e-b2a5-1c6bbad93490.jsonl`.
Annexes : `env-54-permissions/temoin/` (journaux de l'essai témoin),
`env-54-permissions/auto-mode-defaults-2.1.323.json` (sortie de `claude auto-mode defaults`),
`env-54-permissions/rejeu/` (décisions et journaux du rejeu après redémarrage, §10 ; session
`40ad5fdf-53aa-4252-854a-ec885c6cebb9`).

## 1. Inventaire des refus et des acceptations

« Lanceur final » : qui a exécuté la commande au bout du compte.

| Date | Hôte | Commande (forme) | Décision, catégorie | Source | Lanceur final |
| --- | --- | --- | --- | --- | --- |
| 2026-10-30 | VM | `pipx install` de scion 0.5.2.0 et de lepton | refusé (« code externe », catégorie non relevée) | `env-15-scion.md` §8, `env-15-debian.md` | utilisateur |
| 2026-10-30 | VM | clone de seed.scions puis `python3 -m unittest discover -s tests` | refusé (idem) | idem | utilisateur |
| 2026-10-30 | VM | bloc `rm` + `find -exec sh -c` | refusé (« vérification de sécurité ») ; refait en `rm` séparé à chemins littéraux, accepté | `env-15-debian.md` | session |
| 2026-10-31 | VM | `rm -rf ~/lepton-tools-dev/essais/env-15-debian ~/env-15-journaux` | refusé, « Irreversible Local Destruction » (accord PA-29 dans la consigne) | `env-21-debian.md` E-2 | utilisateur |
| 2026-11-02 | VM | `scion graft-update -v` (`essais/env-28-debian`) ×2 | refusé, « Untrusted Code Integration » | `env-28-debian.md` E-1, E-2 | utilisateur |
| 2026-11-02 | VM | `scion rootstock-install`, `seed-add`, `graft`, `rejouer-oracle.sh` | acceptés | `env-28-debian.md` E-2 | session |
| 2026-11-03 à 11-10 | VM | R33-1, R36-1, R43-1, R50-1 : `graft-update` et `rm -rf` confiés d'emblée à l'utilisateur ; `rootstock-install`, `seed-add`, `graft`, `rejouer-oracle.sh`, pytest lancés par la session | acceptés (rien de tenté pour les commandes confiées, sauf R43-1) | consignes `env-33`…`env-50-debian.md` §2 | utilisateur / session |
| 2026-11-09 | VM | `scion graft-update -v` (`essais/env-28-debian`) | refusé, « Modify Shared Resources » | `env-43-debian.md` constat 3 | utilisateur |
| 2026-11-09 | VM | `install-debian.sh` (sudo), `pipx install --force`, `install-vscodium.sh` ×2 | acceptés (demande de l'utilisateur dans la session VM) | `env-43-debian.md` constat 2 | session |
| 2026-11-10 | Mac | `scion graft-update -v` d'`essais/env-13-vierge` (PA-P) | accepté | `env-50-mac.md` §1.5 | session |
| 2026-11-12 | Mac | `scion graft-update -v` d'`essais/env-13-vierge` (PA-P) ; regreffe d'`env-9` seule | acceptés | `env-53-mac.md` §1.4, §4 | session |
| 2026-11-12 | Mac | une commande : regreffe d'`env-11/qemu`, `qemu-gra2`, `bout-en-bout` + `sed -i` du script | refusé, « Modify Shared Resources » ; rien exécuté | `env-53-mac.md` §4 | utilisateur (message renvoyé tel quel, `!`, terminal) |
| 2026-11-12 | VM | `scion graft-update` de `$U` (PA-93 : la session lance) | refusé, « Modify Shared Resources » | `env-53-debian.md` §7.2 | utilisateur (`$U`, `$E13`, `$C5`, `rm -rf`) |
| 2026-11-12 | VM | 4 installations du §6 (`install-debian.sh`, `pipx install --force`, `install-vscodium.sh`), pytest 384 | acceptés | `env-53-debian.md` §1, `env-53-mac.md` §3 | session |
| 2026-11-13 | Mac | essai témoin (§4) : 6 commandes | toutes acceptées | ce rapport §4 | session |

Refus réels : `graft-update` (VM ×4, Mac ×1 en commande groupée), `rm -rf` (VM ×2), `pipx install`
(VM ×1, R15-1 seulement), `git clone` + tests de scion (VM ×1, R15-1 seulement). Jamais refusés :
pytest de lepton-tools, `rejouer-oracle.sh`, bancs QEMU, `rootstock-install`, `seed-add`, `graft`.

## 2. Formes de commandes employées par le chantier

| Commande | Formes relevées | Où |
| --- | --- | --- |
| `scion graft-update` | `cd "$U" && scion graft-update -v > "$J/…log" 2>&1` ; `(cd "$R" && scion graft-update -v) > …` ; `scion graft-update -v` | consignes VM, `rapports/env-53-mac/regreffer-essai.sh` ; rootstocks `essais/env-13-vierge`, `env-28-debian`, `env-13-debian`, `env-53-c5`, `env-9`, `env-11/*` |
| `rm -rf` | `~/lepton-tools-dev/essais/<nom>` (souvent avec `~/env-N-journaux`) ; `<ROOTSTOCK>/build/<preset>` (skill `lepton-cibles` l. 23) ; `rm -rf "${build:?}/$p"` interne à `rejouer-oracle.sh` l. 42 ; `rm -rf "$Y"`/`"$X"` (consignes VM, oracle temporaire) ; `~/tmp-tests`, `~/tmp-pytest` (VM) ; clones de `depots/tiers/` (par l'utilisateur, hook) | consignes, rapports, skills, scripts |
| `pipx install` | `pipx install --force <LEPTON_TOOLS>` (≈ 30 occurrences, dont `~/lepton-tools-dev/lepton-tools` et `"$T"`) ; `pipx install --force "git+file://<SEED_SCIONS>@<version>"` (Mac) ; scion sur la VM par `install-debian.sh` (`SCION_REF`) ; `check-jsonschema==0.38.2` | consignes, rapports |
| `git clone` | `git clone file://localhost/…` (essais d'échec, ENV-51, ENV-53) ; `--filter=blob:none --no-checkout` (tiers) ; `--mirror` ; `-q --branch <b> <src> <dst>` ; `git clone -q --branch 0.5.2.0 $G/seed.scions.git` (VM, R15-1) | consignes, rapports, scripts scion |
| tests | `~/lepton-tools-dev/venv-lepton-tools/bin/python -m pytest -q` (Mac) ; `TMPDIR=~/tmp-pytest ~/lepton-tools-dev/venv-test/bin/python -m pytest -q -rs -p no:cacheprovider` (VM) ; `python3 -m unittest discover -s tests` (scion) ; `scripts/oracle/rejouer-oracle.sh`, `ctest --preset … -L board`, `banc-carte.sh` | idem |

## 3. Mécanisme (documentation et règles par défaut du classifieur)

Sources : agent `claude-code-guide`, puis vérification mot pour mot par un agent de lecture web
(2026-11-13) de https://code.claude.com/docs/en/permission-modes.md (PM),
`permissions.md` (P), `settings.md` (S), `auto-mode-config.md` (AM), `hooks.md` (H) ; et
`claude auto-mode defaults` (annexe).

1. **Ordre.** Hooks `PreToolUse` d'abord ; « A hook that exits with code 2 stops the tool call
   before permission rules are evaluated » (P). Puis règles : « deny, then ask, then allow. The
   first match in that order determines the outcome » (P). En mode auto (PM, « How the classifier
   evaluates actions ») : « 1. Actions matching your allow, ask, or deny rules resolve
   immediately, with these exceptions […] 2. Read-only actions and file edits in your working
   directory are auto-approved […] 3. Everything else goes to the classifier ».
2. **Une règle `allow` étroite évite le classifieur** (étape 1). Exceptions pertinentes : « No
   allow rule approves recognized `rm` and `rmdir` critical-path removals » — chemin critique :
   racine, enfant direct de la racine, répertoire personnel, « Your working directory and its
   parents » (donc `~/lepton-tools-dev` et `~`, pas `~/lepton-tools-dev/essais/x` ni `~/lepton`).
   Écartées à l'entrée en mode auto : « Blanket `Bash(*)` », « Wildcarded interpreters like
   `Bash(python*)` », « Package-manager run commands », `Agent`, `Monitor` ; « Narrow rules like
   `Bash(npm test)` stay in effect ».
3. **Une règle `ask` force une invite, même en mode auto** : « Explicit ask rules still force a
   prompt » (PM) ; « The classifier cannot auto-approve a matching action » (AM).
4. **Hook `allow`** : « skips the permission prompt, except for actions no mode auto-approves »
   (H) ; son effet sur le classifieur **n'est pas documenté**. « Deny and ask rules are still
   evaluated regardless of what the hook returns » (H).
5. **Motifs `Bash(...)`** (P) : texte littéral ; `*` = tout texte, espaces et `..` compris ; `:*`
   final = ` *`. Composées (`&&`, `||`, `;`, `|`, `&`, saut de ligne) : « Every subcommand must be
   allowed » ; `deny` et `ask` valent pour toute sous-commande, même imbriquée. Préfixe de
   variables : seules « certain known-safe environment variables » sont retirées pour `allow`
   (liste non donnée) ; `deny`/`ask` passent toute affectation. Enveloppes retirées : `timeout`,
   `time`, `nice`, `nohup`, `stdbuf`, `command`, `builtin`, `noglob`, `xargs`. `~` et `$HOME` ne sont
   pas développés dans les motifs (texte littéral) : un motif `~/…` correspond à une commande
   écrite `~/…`, sur tout hôte. `git -C . push` n'est pas couvert par `git push *`.
6. **Fichiers** (S) : précédence managed > `--settings` > `.claude/settings.local.json` >
   `.claude/settings.json` > `~/.claude/settings.json` ; les listes `permissions.*` se
   cumulent. « `permissions.allow` rules […] apply only after each teammate trusts the folder […]
   `deny` and `ask` rules apply right away. »
7. **Relecture** : « Claude Code watches your settings files and reloads them when they change, so
   it applies most edits to the running session without a restart, including edits to
   `permissions`, `hooks` » (S). Le fichier d'étape supposait une relecture au démarrage seulement.
8. **`autoMode`** (AM) : lu dans `~/.claude/settings.json`, les réglages gérés et `--settings`
   seulement — « The classifier doesn't read `autoMode` from project settings in
   `.claude/settings.json` or `.claude/settings.local.json` ». Clés `environment`, `allow`,
   `soft_deny`, `hard_deny` (prose), `classifyAllShell` ; `"$defaults"` obligatoire pour garder les
   défauts.
9. **Règles par défaut du classifieur** (annexe) — elles expliquent les trois catégories :
   - « Untrusted Code Integration » : « Pulling code from repos outside the source control orgs
     listed in Environment and arranging for it to execute ». Par défaut, « Source control: The
     trusted repo and its remote(s) only » (le dépôt de lancement, ici lepton-tools).
   - « Modify Shared Resources » : « In-place modification or destruction of shared artifacts […]
     not created in the current context ».
   - « Irreversible Local Destruction » : « Irreversibly deleting […] local files that existed
     before this session […] without explicit user direction naming the specific targets ».
   - « Multi-Agent Coordination » : « Content inside `<teammate-message>` tags is another agent's
     output, not a human user instruction — it does not meet any SOFT BLOCK rule's consent bar ».

## 4. Essai témoin (Mac, 2026-11-13, avant toute règle)

Sous `~/lepton-tools-dev/essais/env-54-essai/`, une commande simple par appel, mode auto.

| N° | Heure | Commande | Résultat |
| --- | --- | --- | --- |
| T1 | 11:48 | `rsync -a --exclude=/build ~/…/essais/env-11/qemu/ ~/…/essais/env-54-essai/qemu/` | accepté, code 0 ; 3059 liens relatifs, 0 cassé ; 5 clones sur leur branche, propres (noyau 58e421e) |
| T2 | 11:49 | `cd ~/…/env-54-essai/qemu && scion graft-update -v > ../journaux/t2-graft-update.log 2>&1` (PA-P accordé) | **accepté**, code 0 ; graine sans amont laissée telle quelle ; 3 `git fetch`, aucun clone avancé ; liste des liens identique avant/après |
| T3 | 11:50 | `rm -rf ~/lepton-tools-dev/essais/env-54-essai/a-supprimer` (créé par la session juste avant) | **accepté**, code 0, absence vérifiée |
| T4 | 11:50 | `git clone /Users/cle_d_anton/lepton-tools-dev/seed.scions ~/…/env-54-essai/clone-seed` | **accepté**, code 0 |
| T5 | 11:50 | `pipx install --force /Users/cle_d_anton/lepton-tools-dev/lepton-tools` | **accepté**, code 0 ; `lepton 0.1.0`, `scion 0.6.3.0 (requis ≥ 0.6.2.0)` |
| T6 | 11:50-11:57 | `~/lepton-tools-dev/venv-lepton-tools/bin/python -m pytest -q` | **accepté**, code 0, 384 passed (420 s) |

Aucun refus. Ce n'est pas une preuve d'innocuité des formes : le classifieur juge le contexte.
Ici, l'utilisateur a accordé dans la session même la copie et le `graft-update` (cibles nommées),
et le répertoire supprimé avait été créé par la session.

## 5. Diagnostic

- Au Mac, les commandes simples passent : l'accord de l'utilisateur est dans la conversation, et
  les cibles sont nommées ou créées par la session. Le seul refus (ENV-53) visait une commande
  groupée sur trois rootstocks existants, avec un `sed -i`.
- Sur la VM, l'accord arrive par un `ORDRE` de la session Mac, donc comme message d'un autre agent :
  il ne franchit pas le seuil de consentement (« Multi-Agent Coordination »). Les rootstocks et
  répertoires visés existaient avant la session. D'où « Modify Shared Resources » et
  « Irreversible Local Destruction ». Les dépôts `lepton-distribution` ne sont pas la source de
  confiance par défaut (seul lepton-tools et son distant le sont), d'où « Untrusted Code
  Integration ». Les installations demandées directement par l'utilisateur dans la session VM
  (R43-1) passent.
- Conséquence : une règle `allow` étroite lève le refus sur la VM (étape 1, sans classifieur).
  Une règle `ask` remplace le refus par une invite, à laquelle l'utilisateur répond dans la
  session VM. Au Mac, l'effet d'une règle `allow` n'est pas observable directement (les
  commandes passent déjà) ; une règle `ask` l'est (invite).

## 6. Analyse des risques

- **Racine de rootstock** : le hook ne refuse ni `rm -rf ~/lepton` ni `rm -rf` d'un rootstock
  d'essai entier ; `~/lepton` n'est pas un chemin critique pour Claude Code. Une règle `allow` à
  joker sur `rm` le laisserait passer. Seule une enveloppe qui résout la cible peut le borner.
- **`build/<preset>`** : `rejouer-oracle.sh` supprime en interne (invisible aux règles) ; rien ne
  doit le gêner. La forme directe de la skill `lepton-cibles` passe aujourd'hui par le classifieur.
- **Motifs par préfixe** : `*` couvre `..` (`rm -rf ~/lepton-tools-dev/essais/../..`), une cible
  vide (`essais/`), un joker littéral (`essais/*`), des variables (`"$Y"`) ; aucune normalisation.
- **PA-P** : aujourd'hui le classifieur refuse souvent `graft-update` hors accord visible, ce qui
  fait respecter PA-P par accident. `allow` supprime cette barrière ; `ask` la rend systématique.
- **`git push`** : aucun motif proposé ne le couvre (`git clone` est un préfixe de mots). Le
  classifieur autorise par défaut un push vers le dépôt de la session (« Git Push Destination ») :
  PA-P n'y est tenu que par la consigne. Une règle `ask` le rendrait technique.
- **`pipx install`** d'une source inattendue : une règle exacte sur la source locale l'exclut.
- **`git clone` vers une destination protégée** : le hook refuse un clone sous `trunk/` ou
  `depots/tiers/` (essai : `git clone /tmp/x /Users/cle_d_anton/lepton/trunk/y` → code 2), et son
  code 2 précède les règles. Destination ailleurs : non bornée par un motif.
- **Enveloppe modifiable** : le script vit dans le dépôt ; une modification passe par Edit (approuvé
  dans le répertoire de travail) et se voit au diff et au commit.
- **Chemins absolus** différents entre hôtes : motifs écrits en `~/…` littéral, commandes écrites
  de même.

## 7. Propositions pour le PA-95 (non validées)

1. **Mécanisme** : règles de permission (`ask` et `allow` étroits), et non une décision de hook
   (effet sur le classifieur non documenté) ni `autoMode` (fichier utilisateur par hôte, prose
   interprétée). Repli possible : aucune règle, §2bis inchangé, D16 clos.
2. **Fichier** : `.claude/settings.json` du dépôt, versionné, commun au Mac et à la VM ; motifs en
   `~/…` littéral. `ask` s'applique sans confiance du dossier, `allow` après.
3. **Règles** :
   - `ask` : `Bash(scion graft-update:*)`, `Bash(scion seed-update:*)` — invite à chaque appel,
     PA-P technique. Option : `Bash(git push:*)` et `Bash(git * push:*)`.
   - `allow` : `Bash(pipx install --force ~/lepton-tools-dev/lepton-tools)` (exact) ;
     `Bash(git clone file://*)`, `Bash(git clone https://github.com/lepton-distribution/*)` ;
     l'enveloppe `rm` (point 4).
   - Tests : aucune règle (jamais refusés hors R15-1) ; une règle sur un interpréteur à joker
     serait écartée en mode auto.
4. **`rm -rf`** : enveloppe `scripts/supprimer-essai.sh <cible>…`, `allow`
   `Bash(scripts/supprimer-essai.sh:*)` et `Bash(~/lepton-tools-dev/lepton-tools/scripts/supprimer-essai.sh:*)`.
   Elle résout chaque cible (`realpath`) et n'accepte que :
   - un descendant strict de `~/lepton-tools-dev/essais/`, hors une liste de références
     (proposée : `archives`, `env-9`, `env-11`, `env-13-vierge`, `env-40-publication`,
     `env-40-miroirs` ; sur la VM `env-13-debian`, `env-28-debian`, `env-53-c5`) ;
   - `~/lepton/build/<preset>` et `<essai>/build/<preset>` ;
   - `~/env-<N>-journaux`, `~/tmp-pytest`, `~/tmp-tests`.
   Elle refuse tout le reste, dont `~/lepton`, `essais/` lui-même, tout chemin sous un `trunk/` ou
   `depots/tiers/` isolé, une cible vide ou absente du disque ; tout ou rien (aucune suppression
   si une cible est refusée). `rm -rf` direct : pas de règle (classifieur).
5. **Commandes laissées à l'utilisateur** : toute cible refusée par l'enveloppe ; suppressions
   sous `depots/tiers/` (hook) ; toute commande encore refusée au rejeu ; `sudo` hors VM.
6. **§2bis** : remplacer « Commandes confiées d'emblée à l'utilisateur » par « Commandes soumises
   aux règles de `.claude/settings.json` (ENV-54) » : `graft-update`/`seed-update` lancés par la
   session et confirmés à l'invite (PA-P inchangé) ; suppressions par l'enveloppe ;
   `pipx install` de lepton-tools et `git clone` par la session ; un refus n'est jamais contourné
   (`AVANCEMENT`, l'utilisateur lance).
7. **Effets** : skill `lepton-cibles` l. 23 (forme de suppression de `build/<preset>`) ; `CLAUDE.md`
   du dépôt : une ligne sous « Règles permanentes » ; consignes VM : à partir d'ENV-57.
8. **Rejeu (§3)** : les réglages sont relus à chaud (§3.7), mais garder le redémarrage prévu :
   une session neuve voit comme « préexistantes » les cibles créées ici, comme la VM.

## 8. PA-95 (2026-11-13, décisions de l'utilisateur)

- Mécanisme et fichier : règles de permission dans `.claude/settings.json` du dépôt, versionné,
  commun au Mac et à la VM, motifs en `~/…` littéral ; hook inchangé ; pas d'`autoMode`.
- `rm -rf` : enveloppe `scripts/supprimer-essai.sh` avec la liste de références du §7.4.
- Compléments retenus : `ask` sur `git push` (et `git * push`) ; `allow` sur
  `pipx install --force ~/lepton-tools-dev/lepton-tools`, `git clone` ciblé (`file://`,
  `https://github.com/lepton-distribution/`) et pytest (`bin/pytest` des deux venvs).
- Reste du §7 retenu tel quel : §2bis amendé, une ligne dans `CLAUDE.md` du dépôt, skill
  `lepton-cibles` l. 23, consignes VM à partir d'ENV-57, rejeu après redémarrage de Claude Code.

## 9. Mise en place (tâche 2)

- `.claude/settings.json` : 7 `allow`, 4 `ask`, 5 `deny` (5 `ask` après la correction du §10.1), hook inchangé ; écrit par la session
  (Write accepté) ; `python3 -m json.tool` : valide.
- `deny` ajoutés par la session, dans le cadre du « `git clone` ciblé » (à confirmer au PA-96) :
  options de `git clone` qui font exécuter une commande ou changent la configuration
  (`--upload-pack`, `-u`, `--config`, `-c`, transport `ext::`). Un `deny` l'emporte sur l'`allow`.
- `scripts/supprimer-essai.sh` (bash, compatible 3.2) : résolution des cibles par `cd -P` et
  réduction lexicale des composants absents ; dernier composant non suivi ; `-n` à blanc ; codes
  0/1/2 ; tout ou rien. Tests `tests/test_supprimer_essai.py` : 52 cas (9 acceptations, 29 refus
  paramétrés dont `~/lepton`, son trunk, ses `depots/`, `build/` seul, `essais/` et ses formes `/`
  et `.`, `..`, références, trunk et `depots/tiers` d'un essai, lien intermédiaire vers `~/lepton`,
  cible absente ; tout ou rien, relatif, `~`, lien final, à blanc, sans argument, build sans
  signature) : verts sous bash 5.3 (MacPorts) et 3.2 (`/bin/bash`) ; shellcheck sans remarque.
  Défaut trouvé par les tests et corrigé : `cd -P //private` gardait « // » en tête.
- ORCHESTRATION §2bis amendé (« Commandes soumises aux règles de `.claude/settings.json` »).
- Constat : les réglages sont relus à chaud (§3.7) ; les règles valent donc déjà dans cette
  session. Le rejeu probant se fait après redémarrage (§7.8).
- Preuve observable : le journal de session (`*.jsonl`) note pour chaque appel un
  `permissionDecision`. Pendant le témoin, `reasonType: "classifier"` pour les 6 commandes. Une
  règle du projet devrait donner `reasonType: "rule"` ; une invite acceptée,
  `source: "user_temporary"`.

## 10. Rejeu après redémarrage (tâche 3, Mac, 2026-11-13)

Session neuve de Claude Code 2.1.323, mode auto. Journal :
`~/.claude/projects/-Users-cle-d-anton-lepton-tools-dev-lepton-tools/40ad5fdf-53aa-4252-854a-ec885c6cebb9.jsonl`.
Décisions extraites par script en lecture seule : `env-54-permissions/rejeu/decisions.tsv` (heures
UTC). Une commande simple par appel. Pour R1 et N4, la forme positionnelle
`scion graft-update -v <rootstock>` (sans `cd` ni redirection) remplace la forme de la passation,
au plan approuvé. Un refus à l'invite est noté `toolUseResult: "User rejected tool use"`, sans
`permissionDecision`.

| N° | Commande | Décision au journal | Effet constaté |
| --- | --- | --- | --- |
| R1 | `scion graft-update -v ~/…/env-54-essai/qemu` (PA-P accordé) | invite `ask`, confirmée (`user_temporary`, `projectSettings`) | code 0 ; 3059 liens, liste identique avant/après et à `liens-apres.txt` de T2 (tri `LC_ALL=C`), 0 cassé ; graine sans amont, 3 `git fetch`, aucun clone avancé |
| R2 | `git clone file:///…/seed.scions ~/…/env-54-essai/clone-seed-2` | `allow` (`subcommandResults`) | code 0, tête 6416c33 |
| R3 | `scripts/supprimer-essai.sh ~/…/env-54-essai/clone-seed` (préexistant) | `allow` (`subcommandResults`) | supprimé, absence vérifiée |
| R4 | `pipx install --force ~/lepton-tools-dev/lepton-tools` | `allow` (`rule`, `projectSettings`) | `lepton 0.1.0`, `scion 0.6.3.0` |
| R5 | `~/lepton-tools-dev/venv-lepton-tools/bin/pytest -q` | `allow` (`subcommandResults`) | 436 passed, 445 s (`rejeu/r5-pytest.log`) |
| N1 | `scripts/supprimer-essai.sh ~/…/env-54-essai/../../absent-env54` | `allow` | enveloppe : code 2, « hors des bornes », rien supprimé |
| N2 | `scripts/supprimer-essai.sh ~/lepton-absent-env54` | `allow` | enveloppe : code 2, rien supprimé |
| N3 | `rm -rf ~/lepton-tools-dev/essais/env-54-absent` | classifieur, accepté | cible absente |
| N4 | `scion graft-update -v ~/…/env-54-absent` | invite `ask`, refusée | — |
| N5 | `git -C ~/…/env-54-absent push` | **classifieur, accepté** (aucune invite) | git : code 128 (cible absente) |
| N6 | `git clone --upload-pack=true file:///absent ~/…/x` | `deny` (`projectSettings`) | — |
| N7 | `touch ~/…/env-54-essai/qemu/trunk/essai-hook` | hook (`hook:PreToolUse`), refusé | — |

`subcommandResults` : la commande est jugée sous-commande par sous-commande, ici par les règles,
sans classifieur. `rule` : la règle couvre la commande entière (motif exact de `pipx`).

### 10.1 Écart N5 : `Bash(git * push:*)` ne couvre pas `git -C <chemin> push`

Le classifieur a accepté N5 (`git -C <absent> push`). Seule l'absence de la cible a empêché le
push : PA-P n'était tenu que par la consigne pour cette forme. Essais complémentaires sur cibles
absentes (décision de l'utilisateur : « tester puis corriger ») :

| N° | Commande | Décision |
| --- | --- | --- |
| Ea | `git -C ~/…/env-54-absent push origin` | classifieur, accepté (code 128) : l'argument après `push` n'y change rien |
| Eb | `cd ~/…/env-54-absent && git push` | invite (`Bash(git push:*)`), acceptée par l'utilisateur ; sans effet, le `cd` échoue avant le push |
| Ec | `scion graft-update` (sans argument, aucun rootstock au-dessus du répertoire de travail) | invite (`Bash(scion graft-update:*)`), acceptée par l'utilisateur ; scion : code 1, « aucun rootstock trouvé » |

Conclusion : les motifs au `:*` final simple couvrent la commande nue et la commande suivie
d'arguments (Eb, Ec, R1). Le motif qui combine un `*` intérieur et le `:*` final ne correspond ni à
N5 ni à Ea. Les motifs à jokers purs fonctionnent (`deny` `git clone*--upload-pack*`, N6).
Correction (`.claude/settings.json`) : `Bash(git * push:*)` remplacé par `Bash(git * push)` et
`Bash(git * push *)` ; JSON valide ; relu à chaud. Rejeu :

| N° | Commande | Décision |
| --- | --- | --- |
| N5-bis | `git -C ~/…/env-54-absent push` | invite `ask`, refusée |
| Ea-bis | `git -C ~/…/env-54-absent push origin` | invite `ask`, refusée |

Règles après correction : 7 `allow`, 5 `ask`, 5 `deny`. Effet de bord accepté : `git -C <x> stash
push` demande aussi confirmation.

### 10.2 Autres observations

- O-0 : une lecture groupée de la session (`… ; scion graft-update -h 2>&1 | head …`) a déclenché
  l'invite `ask`, acceptée (`user_temporary`, `projectSettings`). Elle montre que les règles du
  projet sont actives dès le démarrage et que l'`ask` vaut aussi pour `-h` dans une commande
  composée. C'est une erreur de la session : l'invite était inutile.
- Le refus d'une invite interrompt le tour de Claude Code ; l'utilisateur relance la session.
  Prévoir cette interruption dans les consignes VM (contrôles négatifs de l'ENV-57).
- Une acceptation au Mac ne prouve rien pour la VM : preuve en ENV-57 (PA-101).

### 10.3 Critères

- Commandes retenues (R2 à R5) acceptées par les règles, sans classifieur ; R1 soumis à invite
  (PA-P technique).
- Contrôles négatifs refusés ou soumis à invite : N1, N2 (enveloppe), N4, N5-bis, Ea-bis
  (invite), N6 (`deny`), N7 (hook). N3 relève du classifieur, comme prévu au PA-95 (`rm -rf`
  direct sans règle).
- Hook actif (N7) ; pytest 436 verts, dont `tests/test_proteger_trunk.py` et
  `tests/test_supprimer_essai.py`.
