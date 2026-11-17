# ENV-61 — Validation Debian groupée (ENV-58 à ENV-60) — rapport de la session Mac

Session Mac `validate-env-58-60-debian`, 2026-11-17. Branche lepton-tools `devenv/env-61` (depuis
`main` 7018302). Consigne VM : `consignes/env-61-debian.md`. Journaux Mac :
`~/lepton-tools-dev/essais/env-61-mac/`. Journal de session Claude Code :
`~/.claude/projects/-Users-cle-d-anton-lepton-tools-dev-lepton-tools/65e7c7d6-bbed-4e92-9522-9fbf3ff3df66.jsonl`.
Outils de la session, en lecture seule, utilisables sur Debian : `env-61-mac/ls-remote.sh` ; ceux
d'`env-57-mac/` (`regreffer-essai.sh`, `decisions.py`) et d'`env-53-mac/` restent valables.
Outils Mac : scion 0.6.3.2 et lepton 0.1.0 (pipx), git 2.50.1, Python 3.11.5, Claude Code 2.1.326.

## 1. Préparation (tâche 1)

### 1.1 Têtes publiées (`git ls-remote`, 2026-11-17)

Relevé : `env-61-mac/ls-remote-mac.txt` (script `env-61-mac/ls-remote.sh`, repris
d'`env-57-mac/ls-remote.sh` avec le tag 0.6.3.2). Différences avec le relevé d'ENV-57 :

| Dépôt | Référence | Commit | En R57-1 |
| --- | --- | --- | --- |
| `lepton-tools` | `main` | 7018302 | 6b6b1d6 |
| `seed.scions` | tag `0.6.3.2` (`master` 975caf6) | 08a1460 | tag `0.6.3.1` c51ee1a (`master` d650414) |
| `lepton-original-tree.scions` (noyau) | `master` | dfc960b | ed2a41f |
| graine `original-tree`, 12 autres greffons, 8 miroirs (HEAD et tags) | | inchangés | = |

Le noyau dfc960b (fusion de 8563f90) ne change que 5 fichiers hors de `scion/` : `SCION_REF`
0.6.3.2 dans `install-{macos,debian}.sh`, `README.md`, `README-PAQUET.md`, `doc/BUILDING.md`.
Rien n'est greffé, aucun lien ne change. Une regreffe des rootstocks d'essai n'avance donc que le
clone noyau. lepton-tools depuis R57-1 (6df0de1) : hook (garde G2), `lepton/seed.py` (D17),
`lepton/__init__.py`, `SCION_REF` 0.6.3.2 d'`install-vscodium.sh`, tests.

### 1.2 Liens du trunk de `<ROOTSTOCK>`

`controler-trunk.py ~/lepton` contre `env-50-mac/attendu/trunk-liens.txt` : code 0, `CONFORME`
(3889 liens, 0 fichier régulier, 0 lien cassé, 629 projetés, 0 écart de nom ni de contenu, 8
clones tiers aux HEAD épinglés, filtre `blob:none`). Noyau dfc960b. L'attendu de liens de R50-1 et
celui des clones tiers d'ENV-53 (`env-53-mac/attendu/clones-rootstock-mac.txt`) restent valables.

### 1.3 Essai préalable : `graft-update` d'`essais/env-13-vierge` (attendu de C3)

PA-P accordé avec le plan de session. État avant, celui de `$U` et `$E13` sur la VM après R57-1 :
14 clones sur leur branche, amont réglé, propres, noyau ed2a41f ; 3889 liens ; 8 clones tiers
partiels. `env-57-mac/regreffer-essai.sh avant`, puis, lancée par la session hors script :
`scion graft-update -v ~/lepton-tools-dev/essais/env-13-vierge > …/env-13-vierge-graft-update.log 2>&1; echo "code=$?" >> …`,
puis `apres`.

| Contrôle | Résultat |
| --- | --- |
| `graft-update -v` (scion 0.6.3.2) | code 0 ; 1 clone avancé : `…/original/master avancé : ed2a41f -> dfc960b` ; 0 `git clone` ; 0 ligne `extraction partielle,` ; 0 conflit ni refus ; « 3889 feuilles liées » ; « 6 chemin(s) ignoré(s) par git » (6 `.DS_Store` du Finder, absents sur la VM) |
| Inventaire | seule la ligne du noyau change |
| Liens | 3889 → 3889, 0 ajouté, 0 retiré ; `controler-trunk.py` `CONFORME` |
| Clones tiers | extraits et `sparse-checkout` = attendu, 0 / 16 ; `depots/tiers` 107 992 → 107 992 Ko |
| `lepton check`, `generate` | 0, 0 (avant et après) ; espace identique |

Attendus versionnés (`<R>`, `<HOME>`) : `attendu/c3/graft-update-resume.txt` (82 lignes),
`env-13-vierge-bilan.txt`, inventaires avant et après. Contre `env-57-mac/attendu/c3/` : seules
changent les lignes du noyau (`58e421e -> ed2a41f` devient `ed2a41f -> dfc960b`).

**Constat : décision `user_permanent`.** L'invite a été confirmée par le choix « ne plus
demander », et non par « Oui » (`user_temporary` en ENV-57). Journal de session :
`{"decision": "accept", "source": "user_permanent", "ruleSource": "projectSettings", "reasonCode":
"subcommands:bashMiss:shell-expansion+rule:projectSettings"}`. Aucune règle n'a été écrite :
`.claude/settings.json` garde son empreinte `b01ad557…d235`, relevée après la regreffe ;
`.claude/settings.local.json` date de 15:03, pendant ENV-60 ; `~/.claude/settings.json`, du
10 novembre ; `allowedTools` du projet dans `~/.claude.json` est vide. La règle `ask` reste donc la
seule à décider. La consigne (§9) demande de confirmer par « Oui ». Tâche 3 : l'utilisateur a
choisi de nouveau « ne plus demander » pour `env-9` (sa réponse), et l'invite avait pourtant paru
après le même choix pour `env-13-vierge`. Pour une commande soumise à une règle `ask`, ce choix
n'écrit rien et ne supprime pas l'invite suivante (Claude Code 2.1.326) ; le journal le note
`user_permanent`.

### 1.4 Copie d'essai, dépôts et attendus de C4 (D17)

Copie d'essai `~/lepton-tools-dev/essais/env-61-essai` : `rsync -a --exclude /build/`
d'`essais/env-11/qemu` (noyau ed2a41f, graine `env11` 124db52, 3059 liens, 0 cassé, 0 fichier
régulier, `check` code 0), avant la regreffe de `qemu` (tâche 3). Dépôts présents, créés par
`lepton scion new <nom> --type bibliotheque --repo <P> --no-seed --no-cmake -C <copie>` :
`essais/env-61-depot59` (`env59lib`, 0c71a1c) et `essais/env-61-depot60` (`env60lib`, 4aba71c).
Origine absente `essais/env-61-absent.git`, jamais créée. Graine sans modification.

`env-59-tilde/classer.py` (interpréteur pipx de lepton, `-I`) puis `env-59-tilde/essai.sh`,
rejoués tels quels. Relevés dans `attendu/c4/` (548 fichiers) :
- `classer.tsv` (42 formes) : identique à `env-59-tilde/apres/classer.tsv`, une fois remplacés les
  noms des dépôts (`env-61-depot59` → `env-59-depot`, `env-61-absent.git` → `env-59-absent`),
  qui figurent dans la colonne de la saisie ;
- `essai.sh` : code 0 ; 66 cas, tous revenus à l'état de départ (66 lignes `état : ` vides) ;
  contre `env-59-tilde/apres/`, après le même remplacement des noms :
  - 12 `.err` des cas `a*-i` (origine absente, indice suivi) : `git clone …` devient
    `git clone -b master …`. C'est la commande de scion 0.6.3.2 (D18), écart accepté au PA-108 ;
  - 18 `*-status.out` : seul le commit du dépôt présent change (`536b886` → `0c71a1c`) ;
  - absents ici, présents en ENV-59 : `x01` à `x03` et `vscodium-canal.txt`, essais de
    l'extension faits à la main en ENV-59, hors `essai.sh` ;
  - tout le reste est identique octet pour octet.

Le comportement D17 de lepton 0.1.0 publié est donc celui d'ENV-59 après correction.

### 1.5 Attendus de C5 (D18) : cas de lepton et fixture d'ENV-56

`env-60-scion/essai.sh` sur la même copie, avec `env60lib`. Relevés dans `attendu/c5/` (17
fichiers) : l01 (`@scion`), l02 et l03 (`@nope`) en code 2, message `erreur : échec de « git clone
-b nope … » (code 128) : fatal: Remote branch nope not found in upstream origin`, annulation par
lepton ; 6 états = départ après chaque cas ; aucun clone `library-env60lib` laissé. Identique à
`env-60-scion/apres/`, sauf `scion.txt` (scion de pipx et non du venv) : le scion 0.6.3.2 publié
se comporte comme la branche.

Fixture d'ENV-56 : clone de seed.scions par `git clone
https://github.com/lepton-distribution/seed.scions.git ~/lepton-tools-dev/essais/env-61-seed-scions`
(règle `allow`, `subcommandResults`), puis `git -C … switch --detach 0.6.3.2` (08a1460, propre).
`python3 -I env-56-scion/fixture.py <clone> ~/.local/bin/scion <base> attendu/fixture56`, code 0,
76 relevés :
- base `essais/env-61-fixture` : f12a et f12b comptent 10 répertoires au lieu de 11. La base
  d'ENV-60 avait un niveau de plus, dont un ancêtre restait hors de `<B>` ;
- base `essais/env-61-fixture/f56` (retenue) : identique à `env-60-scion/fixture56-apres/`, sauf
  le nom de la base dans 2 `.depots` (f12a, f12b : `env-60-fixture` → `env-61-fixture`), même
  exception qu'au §1.8 d'ENV-60 ;
- f06 : code 2, message de `git clone -b nope`, `.depots` vide ; f01 à f04 et f10 :
  `git clone -b master …` (PA-108).

**Langue de git sur la VM.** git y écrit en français, même sous `LC_ALL=C` (constat 9 de
`rapports/env-57-debian.md`). Les relevés de C4 et C5 portent deux messages de git relayés par
scion : « and the repository exists. » (23 `.err`) et « fatal: Remote branch %s not found in
upstream %s » (5 `.err`). Traductions de git 2.47.3 (`po/fr.po` du tag v2.47.3) : « et que le
dépôt existe. » (déjà normalisée en ENV-57) et « fatal : La branche distante %s n'a pas été
trouvée dans le dépôt amont %s ». La consigne définit `fr()`, qui ramène ces deux formes à
l'anglais. Ses blocs de comparaison ont été éprouvés en bash au Mac, sur une copie des attendus
traduite dans la forme de git : `c4 : écarts=0 / 528`, `c5 : écarts=0 / 15`,
`fixture56 : écarts=0 / 76`.

### 1.6 Formes des commandes et garde G2

Décisions de cette session (`env-57-mac/decisions.py`, heures UTC) :

| Commande | Décision |
| --- | --- |
| `scion graft-update -v ~/…/env-13-vierge > log 2>&1; echo "code=$?" >> log` | invite `ask`, confirmée (`user_permanent`, `projectSettings`, §1.3) |
| `git clone https://github.com/lepton-distribution/seed.scions.git ~/…/env-61-seed-scions` | règle (`subcommandResults`) |
| `~/…/venv-lepton-tools/bin/pytest -q -rs -p no:cacheprovider --basetemp <d> --junitxml <f.xml>` (tâche de fond) | règle (`subcommandResults`) |
| `bash env-57-mac/regreffer-essai.sh avant|apres …` | classifieur (accepté) ; pas d'invite G2 |
| `git -C … switch --detach 0.6.3.2`, `python3 -I fixture.py …`, `bash env-59-tilde/essai.sh …`, `bash env-60-scion/essai.sh …` | classifieur (accepté) |

Garde G2 : elle fait paraître une invite pour tout script shell lancé qui contient
`scion graft-update`, `seed-update` ou `git push` hors commentaire. Parmi les scripts que lance la
consigne, seul `env-58-formes/ask-script.sh` en contient (A2, voulu). `regreffer-essai.sh` ne cite
`graft-update` que dans des noms de fichiers et des `echo` (4 lignes), que G2 ne retient pas :
aucune invite à la regreffe du §1.3. `ls-remote.sh`, les deux `essai.sh`, `releve.sh`, `etat.sh`,
`releve-clones.sh`, `inventaire-clones.sh`, `rejouer-oracle.sh`, `install-vscodium.sh`,
`supprimer-essai.sh` et `install-debian.sh` du noyau : aucune occurrence.

A2, dans la forme exacte de la consigne (§8.3) :
`bash doc/devenv/rapports/env-58-formes/ask-script.sh ~/lepton-tools-dev/essais/env-61-absent`
→ invite demandée par le hook (G2), **confirmée** par l'utilisateur au lieu d'être refusée
(`accept user_temporary`, sans `ruleSource`). Elle est restée sans effet, la cible étant absente :
code 1, « n'est pas un rootstock ». C'est la même manipulation que N4 d'ENV-57 et A1 d'ENV-58.
Le hook, rejoué hors session sur la même entrée, répond `permissionDecision: "ask"`, motif
« Commande soumise à invite lancée indirectement (bash …/ask-script.sh) : scion graft-update -v
$cible. Règle d'ORCHESTRATION §2bis : la lancer directement. Ne confirmer que si l'utilisateur
l'a accordée (PA-P). » G2 vaut donc aussi avec la cible en argument. Sur la VM, seules les cibles
absentes rendent une telle erreur bénigne : la consigne les garde pour A1 à A3.

Le Mac n'a ni `venv-test` ni règle utilisateur : F1 à F7 avec `venv-test` et U1 à U3 ne
s'éprouvent que sur la VM. Leurs formes sont celles d'ENV-58 (`rapports/env-58-formes.md` §2,
§7), au chemin de l'exécutable près.

### 1.7 pytest

`~/lepton-tools-dev/venv-lepton-tools/bin/pytest -q -rs -p no:cacheprovider --basetemp
~/lepton-tools-dev/essais/env-61-mac/pytest-tmp --junitxml …/6-pytest.xml` (forme couverte, tâche
de fond) : **508 passed** en 8 min 59, 0 échec, 0 ignoré. Par module : `test_proteger_trunk` 118,
`test_garde_ask` 46, `test_supprimer_essai` 52, `test_milestone3` 43.

### 1.8 Consigne

`consignes/env-61-debian.md`, reprise d'`env-57-debian.md`. Elle reporte les points de
`handoff/env-58.md` (§Effets) et de `handoff/env-60.md` (« Reste à faire ») :

| Critère | Contenu |
| --- | --- |
| §0 | `switch` sur `devenv/env-61` ; `~/.claude/settings.json` non modifié (PA-103) ; session relancée dans `$T` ; nom communiqué |
| C1 | têtes = Mac ; empreintes (`settings.json` `b01ad557…`, hook `04572df6…`, enveloppe `04323a00…`) ; scion 0.6.3.2 par `install-debian.sh` du noyau dfc960b (défaut `SCION_REF`) ; lepton par `pipx install --force` (règle), correction D17 vérifiée ; extension 0.5.2 |
| C2 | §8.1 D19 : fichier utilisateur lu en entier, bloc `allow` du PA-103 ; U1 à U3 (`userSettings`, cibles absentes). §8.2 D20 : F1, F3, F6 (règle), F2, F7 (classifieur). §8.3 : A1 (règle `ask`), A2, A3 (hook G2), invites refusées ; H1 (hook) |
| C3 | regreffe de `$U`, `$E13`, `$C5`, `$R53` : noyau seul (ed2a41f → dfc960b), journal = `attendu/c3/` |
| C4 | D17 : `classer.py` = Mac ; `essai.sh` écarts=0 / 528 après `fr()` |
| C5 | D18 : `env-60-scion/essai.sh` écarts=0 / 15 ; fixture écarts=0 / 76, f06 sans clone ; pytest 508 |
| C6 | host et 16 presets contre `env-57-debian` ; `mirror-sync --dry-run` |
| C7, C8 | cartes ; nettoyage par l'enveloppe |

Questions du PA-109 : §2.

## 2. PA-109 (2026-11-17, décisions de l'utilisateur)

Questions posées ; options retenues :
1. C3 et C6 : regreffe d'`env-28-debian`, `env-13-debian`, `env-53-c5` et `env-53-debian` (PA-P,
   invites confirmées par « Oui »), reconstruction de host et des 16 presets dans
   `env-53-debian`, comparés à `env-57-debian` ; `mirror-sync --dry-run`.
2. C5 : fixture d'ENV-56 sur la VM (clone de seed.scions au tag 0.6.3.2).
3. C7 écarté (ni binaire, ni flash, ni sonde ne changent) ; C8 tel qu'écrit.
4. §0 tel qu'écrit, push de `devenv/env-61`, ordre `R61-1`, regreffes des 6 rootstocks d'essai
   du Mac pendant R61-1.

Consigne complétée (ac3b913) et poussée (`git push -u origin devenv/env-61`, invite confirmée).
§0 fait par l'utilisateur sur la VM ; session VM désignée par l'utilisateur : `debian-linux-vm`
(réf. 7348f6, seule en ligne ; déjà en ligne avant le push, confirmée par l'utilisateur comme
la session relancée).

## 3. Messages §2bis

| Message | Date | Sens | Résumé |
| --- | --- | --- | --- |
| ORDRE R61-1 | 2026-11-17 | Mac (`validate-env-58-60-debian`, 14bbb2) → VM (`debian-linux-vm`, 7348f6) | consigne `env-61-debian.md` @ ac3b913 envoyée en entier, avec son sha256 (`5f0cdf6f…2798`, le fichier fait foi) ; branche `devenv/env-61` @ ac3b913 (poussée) ; actions de l'utilisateur : refus A1 à A3, 4 invites `graft-update` (« Oui »), push ; envoi accepté par Remote Control, lecture non confirmée |
| ACCUSÉ R61-1 | 2026-11-17 | VM (`debian-linux-vm`, adresse `bridge:session_01FkeafxfusANbF1yYsZwt53`) → Mac | reçu directement. §5 sans arrêt : `$T` = répertoire de travail, `devenv/env-61` = ac3b913, propre ; sha256 de la consigne = ordre ; Claude Code **2.1.326** (2.1.323 en R57-1) ; `CLAUDE_PROJECT_DIR` vide dans le Bash ; empreintes `settings.json`, hook, enveloppe = Mac ; pas de `settings.local.json` ; `~/.claude/settings.json` **3903 o, modifié le 17 nov. à 16:44** (10 nov. en R57-1 ; lu au §8.1) ; journal `3498db03-….jsonl` ; Debian 13.7, git 2.47.3, scion 0.6.3.1, chaîne = R57-1, 17 Go libres ; `têtes publiées = Mac` ; `$U`, `$E13` = attendu (3889, 23 entrées, noyau ed2a41f, 108 760 Ko) ; `$C5` : graine 6d3d2a5, `salut` 71e1641 `modifs=2`, 3059 liens, 2 clones F7 30 908 Ko. **Écart §0.3** : session non relancée après le `switch` (démarrée sur `devenv/env-57-debian`) ; répertoire `$T`, `settings.json` identique sur les deux branches, hook relu à chaque appel : effet attendu nul, C2 le vérifiera. Étapes §6 à §15 prévues ; §6 commencé |
| AVANCEMENT R61-1 (§6 avant) | 2026-11-17 | VM → Mac | noyau `$K` ed2a41f → dfc960b (avance rapide) ; `SCION_REF` 0.6.3.2 (noyau, lepton-tools) ; `SCION_MIN_VERSION` (0, 6, 2, 0) ; `.vsix` 0.5.2 présent ; lancement des 3 installations |
| QUESTION R61-1 (§6, contrôle D17) | 2026-11-17 | VM → Mac | §6 conforme (`install-debian.sh` code 0, scion 0.6.3.2 depuis `seed.scions.git@0.6.3.2` ; `pipx install --force` lepton 0.1.0, Python 3.13.5 ; `install-vscodium.sh` code 0, `changements 0` ; `scion 0.6.3.2 (requis ≥ 0.6.2.0)` ; extensions = attendu), mais le contrôle D17 de la consigne donne `False` : il cherche `expanduser().resolve()`, texte de l'ancien code, alors que 74c9c97 écrit `expanded = Path(loc).expanduser()` puis `local = expanded.resolve()` ; `seed.py` installé identique à `$T` ; arrêt du §6 appliqué ; options proposées |
| RÉPONSE R61-1 (§6) | 2026-11-17 | Mac → VM | erreur de la consigne confirmée (Mac : ancien contrôle `False`, contrôle proposé `True`) ; décision de l'utilisateur, option 1 : contrôle remplacé par l'identité de `seed.py` et `"local = expanded.resolve()" in src and "file://localhost{local}" in src`, écart consigné, suite de la consigne entière, le §10 faisant foi pour C4 ; envoi accepté par le serveur, remise non confirmée |
| AVANCEMENT R61-1 (§7, §8.1, §8.2) | 2026-11-17 | VM → Mac | contrôle D17 corrigé `True`, ancien `False`, `seed.py` installé = dépôt (`6-controle-d17.txt`) ; §7 : copie 3059 liens, `check` 0, `env59lib` 7e2812f, `env60lib` c61b3dc, graine sans modification ; §8.1 : `permissions.allow` = PA-103 (3 règles), ni `ask`, ni `deny`, ni `defaultMode` ; autres clés `modelSettings`, `tui`, `theme`, `agentPushNotifEnabled`, `autoMode` (`soft_deny`) ; fichier du 17 nov. 16:44, vraisemblablement écrit par `/model` (bloc `permissions` inchangé) ; U1 code 1, U2 code 128 (« could not read Username »), U3 code 1, cibles absentes ; F1, F3, F6, F7 : 1 passed, F2 vers `8-f2.log` ; A1 lancé, refus attendu de l'utilisateur |
| AVANCEMENT R61-1 (§8, A1) | 2026-11-17 | VM → Mac | **écart** : invite A1 parue (règle `ask`) mais **confirmée** au lieu d'être refusée (`accept user_temporary projectSettings`, 15:58:28 UTC) ; code 1, « n'est pas un rootstock », rien créé ; décisions jusque-là : `pipx install --force` `rule projectSettings` ; U1, U2 `subcommandResults` ; **U3 `classifier`** au lieu de la règle utilisateur attendue (écart relevé, sans arrêt) ; F1, F3, F6 `subcommandResults` ; F2, F7 `classifier` ; arrêt, l'utilisateur décide de la suite (A2) dans la session VM |

## 4. Rootstocks d'essai du Mac (tâche 3)

Accord de l'utilisateur au PA-109 (PA-P), pendant R61-1. scion 0.6.3.2, lepton 0.1.0. Script
`env-57-mac/regreffer-essai.sh avant|apres` ; entre les deux, la session lance
`scion graft-update -v <rootstock> > <journal> 2>&1; echo "code=$?" >> <journal>`. Attendu des liens :
la liste d'avant du rootstock (dfc960b ne change rien de greffé). Journaux et bilans :
`~/lepton-tools-dev/essais/env-61-mac/regreffes/<rootstock>-*`. Inventaire avant : clones de
greffons sur `master`, amont réglé, noyau ed2a41f partout.

| Rootstock | `graft-update` | Liens avant → après | Ajouts / retraits | `controler-trunk.py` | Clones tiers | `check` | Espace |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `env-13-vierge` (§1.3) | 0 ; noyau ed2a41f → dfc960b seul | 3889 → 3889 | 0 / 0 | `CONFORME` | 8, = attendu (0 / 16), 107 992 Ko inchangés | 0 | identique |
| `env-9` | 0 ; noyau seul | 3059 → 3059 | 0 / 0 | `CONFORME` | — | 0 | identique |
| `env-11/qemu` | 0 ; noyau seul | 3059 → 3059 | 0 / 0 | `CONFORME` | — | 0 | identique |
| `env-11/qemu-gra2` | 0 ; noyau seul (BSP an386 réinscrit, 3059 feuilles), puis `scion graft-remove lepton@bsp-qemu-mps2-an386 <rootstock>` code 0, 8 feuilles, clone conservé | 3051 → 3051 | 0 / 0 | `CONFORME` | — | 1 (attendu, CFG-5) | identique |
| `env-11/bout-en-bout/rootstock` | 0 ; noyau seul | 3059 → 3059 | 0 / 0 | `CONFORME` | — | 0 | identique |
| `env-11/f429zi` | 0 ; noyau seul | 3294 → 3294 | 0 / 0 | `CONFORME` | 2, = attendu (0 / 4), 36 528 Ko inchangés | 0 | identique |
| `env-11/wl55jc1` | 0 ; noyau seul | 3315 → 3315 | 0 / 0 | `CONFORME` | 4, = attendu (0 / 8), 40 684 Ko inchangés | 0 | identique |

Partout : aucun `git clone`, aucune ligne `extraction partielle,`, 0 conflit ni refus, 0 lien
cassé, 0 fichier régulier, 0 `.DS_Store` dans les trunks.

Décisions (journal de session, `decisions.py`, heures UTC) : les 7 `graft-update` sur invite
`ask` confirmée par l'utilisateur, de 15:11 à 16:01 : `user_temporary` ×4 (« Oui ») et
`user_permanent` ×3 (`env-13-vierge`, `env-9`, `f429zi`), tous `projectSettings`. Pour `env-9`,
l'utilisateur a confirmé avoir choisi « ne plus demander » ; pour les deux autres, le même code
le laisse supposer, sans confirmation. L'invite a paru à chaque fois, même après un « ne plus demander » (§1.3). Le
`graft-remove`, hors règle, a été accepté par le classifieur. Aucun refus.
| AVANCEMENT R61-1 (§8 fin, §9 début) | 2026-11-17 | VM → Mac | A1 rejoué à la demande de l'utilisateur : `rejet-invite` (15:59:48) ; A2 `rejet-invite` (16:00:46) ; A3 `rejet-invite` (16:01:20) ; H1 `reject hook` ; cible absente, `essai-hook` absent, 0 paquet `env-61`, liens de `$S` = départ ; écart restant U3 (classifieur) ; motifs d'A2 et A3 demandés à l'utilisateur ; §9 : relevé avant d'`env-28-debian` (3889), `graft-update` lancé sur invite |
| AVANCEMENT R61-1 (§9, 1/4) | 2026-11-17 | VM → Mac | `env-28-debian` : invite confirmée (`user_temporary projectSettings`, 16:02:35) ; code 0, noyau seul ed2a41f → dfc960b, 0 clone, 0 conflit, 3889 feuilles, journal = Mac, liens 3889 → 3889, `CONFORME` (avant et R50-1), tiers 0 / 16, `clones = Mac`, `check` 0, espace identique ; `env-13-debian` : relevé avant, `graft-update` lancé sur invite |
| AVANCEMENT R61-1 (§9, 2/4) | 2026-11-17 | VM → Mac | `env-13-debian` : code 0, noyau seul ed2a41f → dfc960b, 0 clone, 3889 feuilles, journal = Mac, liens 3889 → 3889, `CONFORME`, tiers 0 / 16, `clones = Mac`, `check` 0, espace identique ; `env-53-c5` : relevé avant (3059), `graft-update` lancé sur invite |
| AVANCEMENT R61-1 (§9, 3/4) | 2026-11-17 | VM → Mac | `env-53-c5` : code 0, noyau seul ed2a41f → dfc960b, 0 clone, 3059 feuilles, 3059 → 3059, `CONFORME`, 2 clones F7 0 / 4, 30 908 Ko inchangés, `salut` sans amont `modifs=2` inchangé, `check` 0, espace identique ; `env-53-debian` : relevé avant (3889), `graft-update` lancé sur invite |
| AVANCEMENT R61-1 (§9, 4/4, C3) | 2026-11-17 | VM → Mac | `env-53-debian` : code 0, noyau seul ed2a41f → dfc960b, 0 clone, 3889 feuilles, journal = Mac, liens 3889 → 3889, `CONFORME` (avant et R50-1), tiers 0 / 16, 87 512 Ko inchangés, `clones = Mac`, `check` 0, espace identique ; les 4 `graft-update` `accept user_temporary projectSettings` (16:02:35, 16:05:08, 16:06:55, 16:09:28), aucun `user_permanent` ; §10 lancé |
| QUESTION R61-1 (§11.2, fixture) | 2026-11-17 | VM → Mac | §10 conforme (`classer = Mac`, 66 états = départ, écarts=0 / 528, `*-status.out` informatifs) ; §11.1 conforme (l01 à l03 code 2, écarts=0 / 15, `fr()` sans effet : `essai.sh` exporte `LC_ALL=C`) ; fixture : **écarts=4 / 76** : `f05.err`, `f06.err` (git français, **espace insécable** U+00A0 avant « : » dans « fatal : », que `fr()` ne prend pas ; `fixture.py` sans `LC_ALL`) et `f12a.depots`, `f12b.depots` (ligne `depots/.mirrors/localhost/home` contre `/Users`, segment d'hôte non normalisé) ; une fois ces deux points neutralisés, 76 / 76 identiques ; f06 code 2, `.depots` vide ; options proposées |
| (décision) | 2026-11-17 | utilisateur | causes vérifiées au Mac (`po/fr.po` : `fatal : ` ; attendu `f12a.depots` l. 3 `localhost/Users`) ; option 1 retenue par l'utilisateur, répondue directement dans la session VM ; aucune réponse de la session Mac envoyée |
| AVANCEMENT R61-1 (§11.2, option 1) | 2026-11-17 | VM → Mac | 4 écarts retenus comme écarts de comparaison, documentés au rapport ; §11.3 lancé |
| AVANCEMENT R61-1 (§11.3, C5) | 2026-11-17 | VM → Mac | pytest 508 passed, 0 échec, 0 erreur, 0 ignoré, 174 s ; 118 / 46 / 52 / 43 ; lepton éditable depuis `$T` ; lepton-tools propre ; §12.1 lancé |
| AVANCEMENT R61-1 (§12, C6) | 2026-11-17 | VM → Mac | `rejouer-oracle` code 0 ; host 7/7 ; 16 presets ; bancs 20/20 ×2, 16/16 ×2, 19/19 ×2, `peripheriques` ×4 ; trunk de `$R53` 3889, 0 cassé, 0 régulier, 0 `__pycache__` ; mklepton = R57-1 = `env-52-apres` ; `comparer_R57-1` 0 et `hors_debug=0` ×16 ; `comparer_Mac` 1 ; `mirror-sync --dry-run` code 0, 8 miroirs, 0 à envoyer, 0 signalement, `CONFORME` |
| QUESTION R61-1 (push) | 2026-11-17 | VM → Mac et utilisateur | rapport commité (2771213 sur `devenv/env-61-debian`) ; accord du push demandé à l'utilisateur dans la session VM (PA-P) |
| FIN-SUCCÈS R61-1 | 2026-11-17 | VM → Mac | reçu. C1 à C6 atteints (écarts consignés), C7 écarté, C8 fait (6 chemins supprimés par l'enveloppe, `subcommandResults`) ; `devenv/env-61-debian` 2771213 **poussée** (invite confirmée, `user_temporary projectSettings`) ; clone noyau à dfc960b ; écarts du rapport §9 : (1) session non relancée, (2) contrôle D17 faux, corrigé, (3) 1re invite A1 confirmée, sans effet, (4) U3 par le classifieur, (5) fixture : 4 écarts de comparaison, correction proposée (`fr()` à espace insécable ou `LC_ALL=C` dans `fixture.py`, normalisation du segment d'hôte), (6) clés hors `permissions` dans `~/.claude/settings.json` (`/model`) ; non fait : C7, motif des invites A2 et A3, messages postérieurs au commit absents du §10 du rapport VM, `~/tmp-pytest` non vidé |

## 5. Vérification du rapport VM (tâche 4)

`devenv/env-61-debian` 2771213 (sur ac3b913), poussée : 756 fichiers ajoutés, tous sous
`rapports/env-61-debian.md`, `rapports/env-61-debian/` et `rapports/oracles/env-61-debian/` ;
aucun autre fichier touché. Comparaisons refaites au Mac sur les relevés poussés (extraits par
`git archive`) :

| Critère | Refait au Mac | Résultat |
| --- | --- | --- |
| C1 | rapport §1, `6-controle-d17.txt` | scion 0.6.3.2 par `install-debian.sh`, lepton réinstallé, contrôle D17 corrigé `True` (ancien `False`), `seed.py` = dépôt ; extension 0.5.2 ; conforme |
| C2 | `15-decisions.tsv` (69 lignes, chemin personnel normalisé), `settings-utilisateur.json` | `permissions` = PA-103 (3 règles `allow`), autres clés `agentPushNotifEnabled`, `autoMode`, `modelSettings`, `theme`, `tui` ; `pipx install --force` `rule projectSettings` ; U1, U2 `subcommandResults` ; U3 `classifier` ; F1, F3, F6 `subcommandResults`, F2, F7 `classifier` ; A1 1er `user_temporary`, A1 rejoué, A2, A3 `rejet-invite` ; H1 `reject hook` ; 4 `graft-update` `user_temporary` ; `git clone` de seed.scions et pytest `subcommandResults` ; conforme, avec les écarts 3 et 4 du rapport VM |
| C3 | journaux `graft-update` normalisés contre `attendu/c3/graft-update-resume.txt` ; bilans ; `clones.txt` contre `env-53-mac/attendu/clones-rootstock-mac.txt` | journal = Mac ×3 ; noyau seul ed2a41f → dfc960b ×4 ; 3889 → 3889 ×3, 3059 → 3059 ; `CONFORME` ×4 ; tiers 0 / 16 ×3, 0 / 4 ; `clones = Mac` ×3 ; `check` 0 ×4 ; espace identique ×4 |
| C4 | `10-classer.tsv`, `10-c4/` contre `attendu/c4/`, `fr()` de la consigne | `classer = Mac` ; écarts=0 / 528 |
| C5 | `11-c5/` contre `attendu/c5/` ; `11-fixture56/` contre `attendu/fixture56/` | 0 / 15 ; fixture : 4 / 76 avec le `fr()` de la consigne (`f05.err`, `f06.err`, `f12a.depots`, `f12b.depots`), **0 / 76** une fois admise l'espace insécable (`fatal[  ]:`) et `localhost/home` ramené à `localhost/Users` ; f06 code 2, `.depots` vide ; pytest 508 |
| C6 | `comparer-oracle.py` `env-57-debian` contre `env-61-debian` ; empreintes mklepton | `comparer` 0 pour les 16 presets ; mklepton = `env-57-debian` = `env-52-apres` ; `12-bilan.txt` : 16 × `comparer_R57-1=0`, `hors_debug=0` |
| C7, C8 | `FIN-SUCCÈS` | C7 écarté (PA-109) ; C8 : 6 chemins supprimés par l'enveloppe (`subcommandResults`), absents |

Constats de la vérification :
- **D19, U1 et U2** : `subcommandResults` sans `ruleSource`. Aucune règle du dépôt ne couvre
  `pipx install <chemin>` sans `--force`, ni `git clone --depth 1 <URL>` (la règle du dépôt veut
  l'URL en premier argument) : seules les règles utilisateur `Bash(pipx install:*)` et
  `Bash(git clone * https://github.com/lepton-distribution/*)` ont pu les accepter. D19 vaut donc
  pour U1 et U2. **U3** : la règle `Bash(python3 -m unittest discover *)` n'a pas décidé de
  `python3 -m unittest discover -s ~/…`, c'est le classifieur qui l'a fait. La cause n'est pas
  établie.
- **Comparaison de la fixture** : deux défauts de la consigne (session Mac). `fr()` ne prend pas
  l'espace insécable (U+00A0) que git 2.47.3 écrit dans « fatal : » (`po/fr.po`). Ma simulation
  au Mac l'avait remplacée par une espace ordinaire, d'où un faux 0 / 76 au §1.5. Le segment
  d'hôte `localhost/Users` (Mac) ou `localhost/home` (Debian) n'est pas normalisé.
  `fixture.py` d'ENV-56 ne fixe pas `LC_ALL`, contrairement aux deux `essai.sh`.
- **Contrôle D17 du §6** : faux dans la consigne, corrigé par la RÉPONSE R61-1 ; le §10 a mesuré
  la correction (0 / 528).
- **Invites à refuser** : la première invite d'A1 a été confirmée sur la VM, comme A2 au Mac
  (§1.6), N4 en ENV-57 et A1 en ENV-58. Les cibles absentes ont rendu chaque erreur sans effet.
- **Session VM non relancée** (§0.3) : aucune conséquence constatée. Règles du dépôt
  (`projectSettings`), invites `ask` et hook G2 appliqués.
- Les messages postérieurs au commit 2771213 (QUESTION du push, `FIN-SUCCÈS`) figurent au §3
  ci-dessus, pas au §10 du rapport VM.

Résultat : `FIN-SUCCÈS R61-1` vérifié. C1 à C6 conformes, avec les écarts consignés ; C7 écarté
au PA-109 ; C8 fait.
