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
seule à décider. La tâche 3 dira si l'invite reparaît dans cette session. La consigne (§9) demande
de confirmer par « Oui ».

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
