# ENV-57 — Validation Debian groupée (ENV-54 à ENV-56) — rapport de la session Mac

Session Mac `lepton-tools-30`, 2026-11-13. Branche lepton-tools `devenv/env-57` (depuis `main`
6b6b1d6). Consigne VM : `consignes/env-57-debian.md`. Journaux Mac :
`~/lepton-tools-dev/essais/env-57-mac/`. Journal de session Claude Code :
`~/.claude/projects/-Users-cle-d-anton-lepton-tools-dev-lepton-tools/fe11ef73-e5e2-4c59-98a3-0eadfbcaedee.jsonl`.
Outils de la session, en lecture seule, utilisables sur Debian : `env-57-mac/ls-remote.sh`,
`regreffer-essai.sh`, `decisions.py` ; ceux d'`env-53-mac/` restent valables.

## 1. Préparation (tâche 1)

### 1.1 Têtes publiées (`git ls-remote`, 2026-11-13)

Relevé : `env-57-mac/ls-remote-mac.txt` (script `env-57-mac/ls-remote.sh`, repris
d'`env-53-mac/ls-remote.sh` avec le tag 0.6.3.1). Différences avec le relevé d'ENV-53 :

| Dépôt | Référence | Commit | En R53-1 |
| --- | --- | --- | --- |
| `lepton-tools` | `main` | 6b6b1d6 | fb61b9a |
| `seed.scions` | tag `0.6.3.1` (`master` d650414) | c51ee1a | tag `0.6.3.0` 87dc108 (`master` 6416c33) |
| `lepton-original-tree.scions` (noyau) | `master` | ed2a41f | 58e421e |
| graine `original-tree`, 12 autres greffons, 8 miroirs | | inchangés | = |

Le noyau ed2a41f (fusion de 79354a0) ne change que des fichiers hors de `scion/` (`SCION_REF`
0.6.3.1 dans `install-{macos,debian}.sh`, `README.md`, `README-PAQUET.md`, `doc/BUILDING.md`) :
rien n'est greffé, aucun lien ne change. Une regreffe de `$U` et `$E13` (et de `$C5`) n'avance
donc que le clone noyau.

### 1.2 Liens du trunk de `<ROOTSTOCK>`

`controler-trunk.py ~/lepton` contre `env-50-mac/attendu/trunk-liens.txt` : code 0, `CONFORME`
(3889 liens identiques, 0 fichier régulier, 0 lien cassé, 629 projetés = attendu, 0 écart de nom ni
de contenu, 8 clones tiers aux HEAD épinglés, filtre `blob:none`). L'attendu de liens de R50-1 et
celui des clones tiers d'ENV-53 (`env-53-mac/attendu/clones/`) restent valables ; ils ne sont pas
recopiés.

### 1.3 Essai préalable : `graft-update` d'`essais/env-13-vierge` (attendu de C3)

PA-P accordé avec le plan de session. État avant, celui de `$U` et `$E13` sur la VM après R53-1 :
14 clones sur leur branche, amont réglé, propres, noyau 58e421e ; 3889 liens ; 8 clones tiers
partiels (ENV-53). Script `env-57-mac/regreffer-essai.sh avant|apres` : relevés et bilan de celui
d'ENV-53, mais le `graft-update` est lancé à part par la session, pour que la règle `ask` le voie
(lancé depuis un script, il irait au classifieur).

Commande lancée par la session :
`scion graft-update -v ~/lepton-tools-dev/essais/env-13-vierge > …/env-13-vierge-graft-update.log 2>&1; echo "code=$?" >> …`
→ invite de Claude Code (`ask`), confirmée par l'utilisateur (`user_temporary`, `projectSettings`).

| Contrôle | Résultat |
| --- | --- |
| `graft-update -v` (scion 0.6.3.1) | code 0 ; 1 clone avancé : `…/original/master avancé : 58e421e -> ed2a41f` ; 0 `git clone` ; 0 ligne `extraction partielle,` (clones déjà partiels) ; 21 lignes `répertoire extrait` ; 0 conflit ni refus ; « 3889 feuilles liées » ; « 6 chemin(s) ignoré(s) par git » (6 `.DS_Store` du Finder, absents sur la VM) |
| Inventaire | seule la ligne du noyau change |
| Liens | 3889 → 3889, 0 ajouté, 0 retiré ; `controler-trunk.py` `CONFORME` |
| Clones tiers | extraits et `sparse-checkout` = attendu, 0 / 16 ; `depots/tiers` 107 992 → 107 992 Ko |
| `lepton check`, `generate` | 0, 0 (avant et après) ; espace identique |

Attendus versionnés, chemins remplacés par `<R>` et `<HOME>` : `attendu/c3/graft-update-resume.txt`
(82 lignes du journal, hors commandes git, `.DS_Store` et la ligne des chemins ignorés),
`env-13-vierge-bilan.txt`, inventaires avant et après.

### 1.4 Attendus de C4 (D13) et de C5 (D14)

Copie d'essai `~/lepton-tools-dev/essais/env-57-essai` : `rsync -a --exclude /build/`
d'`essais/env-11/qemu` (noyau 58e421e, 3059 liens, 0 cassé, 0 fichier régulier, `check` code 0).
Dépôt présent `essais/env-57-depot` : `lepton scion new env55lib --type bibliotheque --repo … --no-seed
--no-cmake -C <copie>` (un commit, 2d17a36). Dépôt absent `essais/env-57-absent.git`, jamais créé.
scion 0.6.3.1 (pipx), lepton 0.1.0.

**C4** — `rapports/env-55-url-file/essai.sh` rejoué tel quel, relevés dans `attendu/c4/` (242
fichiers) :
- 21 cas (a01 à a10, p01 à p10, s05), tous revenus à l'état de départ, sans aucun `rmdir` ;
- comparaison avec `env-55-url-file/apres/` (même script, scion 0.6.3.0) : seules diffèrent les
  lignes `rmdir depots/lepton/library-absent` des 8 `.etat` d'échec de `git clone` (a01 à a06, a09,
  a10 : D14 corrigé), le nom relatif `../env-57-…` (a08, p09) et le commit du dépôt présent dans
  les 10 `*-status.out`. Les formes normalisées par lepton (PA-97) restent identiques à
  `file://localhost/`.

**C5** — `rapports/env-56-scion/essai.sh` (e01 à e06) sur la même copie, relevés dans `attendu/c5/`
(50 fichiers) :
- aucun « résidu » ; e04 et e05 : « préexistant gardé » ;
- comparaison avec `env-56-scion/apres/` (branche `devenv/env-56` en venv) : seuls diffèrent le nom
  `env-57-absent` (e06) et `scion.txt` (scion de pipx, et non du venv). Le scion publié 0.6.3.1 se
  comporte comme la branche.

Sur la VM, la copie part de `$C5` (`essais/env-53-c5`), regreffé à 58e421e en R53-1 : même noyau,
3059 liens. Elle diffère de celle du Mac par la graine `env11` (commit), `salut` (sans amont,
`modifs=2`) et les clones F7 conservés de R53-1. Aucun cas des deux scripts ne touche le F7. Les
`*-status.out` (C4) et `depart.etat` restent donc informatifs ; tout le reste se compare octet
pour octet, après normalisation de la langue de git (« et que le dépôt existe. »). Les blocs de
comparaison de la consigne ont été éprouvés en bash au Mac (`c4 : écarts=0 / 231`, normalisation
française comprise ; `journal = Mac` ; `clones = Mac`).

### 1.5 Formes des commandes (règles d'ENV-54), décisions relevées

Décisions lues dans le journal de session par `env-57-mac/decisions.py` (heures UTC) :

| Commande | Décision |
| --- | --- |
| `scion graft-update -v <essai> > log 2>&1; echo "code=$?" >> log` | invite `ask`, confirmée (`user_temporary`, `projectSettings`) |
| `~/…/venv-lepton-tools/bin/pytest … --basetemp <d> > log 2>&1; echo "code=$?" >> log` | **classifieur** (accepté) |
| `~/…/venv-lepton-tools/bin/pytest … --basetemp <d> <test> > log 2>&1` | **classifieur** (accepté) |
| `~/…/venv-lepton-tools/bin/pytest … --basetemp <d> <test>` | règle (`subcommandResults`) |
| `~/…/venv-lepton-tools/bin/pytest -q -rs … --basetemp <d> --junitxml <f.xml> <test>` | règle (`subcommandResults`) |
| `git clone https://github.com/lepton-distribution/lepton-bsp-qemu-mps2-an500.git ~/…/env-57-clone` | règle (`subcommandResults`) |
| `scripts/supprimer-essai.sh ~/…/env-57-clone` | règle ; supprimé |
| `scripts/supprimer-essai.sh ~/…/essais/env-11/qemu` | règle ; enveloppe : code 2, « essai de référence protégé (env-11) », rien supprimé |
| `touch ~/…/env-57-essai/trunk/essai-hook` | hook (`reject`, `hook`) |
| `pipx install --force ~/lepton-tools-dev/lepton-tools` | règle (`rule`, `projectSettings`) ; lepton 0.1.0 réinstallé depuis `devenv/env-57` (code = `main`) |

Constats :
- **une redirection vers un fichier fait sortir une commande de sa règle `allow`** : elle va au
  classifieur, qui l'accepte ici. La consigne écrit donc les commandes `allow` sans redirection ;
  pytest écrit son journal par `--junitxml`, qui reste couvert. Une règle `ask`, elle, vaut avec la
  redirection et le `; echo` ;
- `TMPDIR=~/tmp-pytest` (forme de R53-1) n'est pas couvert (affectation en tête) : remplacé par
  `--basetemp ~/tmp-pytest/env-57` (les tests n'utilisent que les répertoires temporaires de
  pytest) ;
- l'enveloppe refuse `essais/env-11/qemu` (référence `env-11`) : sur la VM, sa suppression (D15)
  reste à l'utilisateur ;
- `pytest` complet (`venv-lepton-tools`, Python 3.11.5, scion 0.6.3.1) : **453 passed** en 8 min 36,
  dont 118 du hook et 52 de l'enveloppe.

Extracteur : il ne retient que les entrées `user` du journal. Les entrées `api-request-blob`, qui
reprennent le résultat sans la décision, avaient d'abord donné des décisions vides.

### 1.6 Consigne

`consignes/env-57-debian.md`, reprise d'`env-53-debian.md` :

| Critère | Contenu |
| --- | --- |
| C1 | Versions, `settings.json`, hook et enveloppe = Mac, Claude Code ; scion 0.6.3.1 par `install-debian.sh` (commande `pipx` donnée en clair), lepton par `pipx install --force ~/lepton-tools-dev/lepton-tools` (règle), `install-vscodium.sh` ×1 |
| C2 | D16 : P3 à P5 (`git clone` https et `file://`, enveloppe), N1 à N7 d'ENV-54 sur cibles absentes ou protégées (dont N2b, référence `env-28-debian` à blanc), décisions extraites du journal de la session VM |
| C3 | Regreffe de `$U`, `$E13` et `$C5` par la session, sur invite confirmée par l'utilisateur ; attendu du §1.3 |
| C4 | D13 : `env-55-url-file/essai.sh` sur une copie de `$C5`, = `attendu/c4/` (231 relevés) |
| C5 | D14 : `env-56-scion/essai.sh`, = `attendu/c5/` (48 relevés), aucun résidu ; pytest 453 (`--junitxml`) |
| C6 | regreffe d'`essais/env-53-debian` (`$R53`), host et 16 presets par `rejouer-oracle.sh`, `comparer` 0 ×16 contre `env-53-debian` (PA-101) ; `mirror-sync --dry-run` |
| C7 | écarté |
| C8 | copie et dépôt d'essai, `~/env-53-journaux` par l'enveloppe ; `essais/env-11/qemu` par l'utilisateur |

Préalable (§0) : l'utilisateur fait `git switch devenv/env-57` sur la VM et relance la session VM
dans `~/lepton-tools-dev/lepton-tools`, pour qu'elle lise les règles du dépôt ; le contrôle N7 (hook)
et les décisions `subcommandResults` le prouvent.

Écarts au fichier d'étape, soumis au PA-101 :
- `$C5` regreffé en C3, en plus de `$U` et `$E13` : sinon la graine de projet de référence de la VM
  resterait à 58e421e quand celle du Mac passe à ed2a41f (tâche 3), la dérive qui a causé la
  QUESTION de R53-1 (D15). La copie de C4 et C5 est faite avant cette regreffe ;
- C6 : proposé sans reconstruction (forme d'`env-56-scion.md` §6) ; l'utilisateur l'a maintenue au
  PA-101 (§2), d'où la regreffe de `$R53` avant `rejouer-oracle.sh` ;
- `install-vscodium.sh` lancé une fois (la seconde exécution de R53-1 n'apportait rien :
  `changements 0` dès la première).

## 2. PA-101 (2026-11-13, décisions de l'utilisateur)

- C3 : regreffe de `$U`, `$E13` **et `$C5`** (graine de projet de référence de la VM, D15), la copie
  d'essai de C4 et C5 étant faite avant ; écart au fichier d'étape accepté.
- C6 : **reconstruction maintenue** (host et 16 presets), dans `$R53` regreffé au §9 de la consigne
  (même procédure que C3), comparée à `oracles/env-53-debian/` ; puis `mirror-sync --dry-run`. La
  consigne a été complétée en conséquence (§1, §2, §9, §12, §15).
- C7 : écarté (pas de cartes).
- C8 : tel qu'écrit (copie, dépôt et `~/env-53-journaux` par l'enveloppe ; `essais/env-11/qemu` par
  l'utilisateur).
- Lecture des règles : préalable du §0 — l'utilisateur fait `git switch devenv/env-57` sur la VM et
  relance la session Claude Code de la VM dans `~/lepton-tools-dev/lepton-tools` ; l'ordre est
  envoyé à la nouvelle session.
- PA-P : push de `devenv/env-57`, envoi de `R57-1` ; regreffe des 7 rootstocks d'essai du Mac
  pendant R57-1 (tâche 3).

## 3. Messages §2bis

La session Mac a été renommée par Claude Code en cours de session : `lepton-tools-30` (nom de la
consigne) → `validation-debian-env-57` (même session, réf. d67f9e) ; signalé dans l'ordre. La
session VM relancée au §0 garde le nom `debian-linux-vm` (réf. d3fe18 ; l'ancienne, c187af, est
hors ligne).

| Message | Date | Sens | Résumé |
| --- | --- | --- | --- |
| ORDRE R57-1 | 2026-11-13 | Mac (`validation-debian-env-57`) → VM (`debian-linux-vm` d3fe18) | consigne `env-57-debian.md` @ 10b6dd3 envoyée en entier, branche `devenv/env-57` @ 10b6dd3 (poussée) ; préalable §0 fait par l'utilisateur ; actions de l'utilisateur : 4 invites `graft-update`, refus N4 et N5, push, suppression d'`essais/env-11/qemu` ; envoi réussi par Remote Control, lecture non confirmée |
| ACCUSÉ R57-1 | 2026-11-13 | VM (`debian-linux-vm`, réf. 153462, adresse `bridge:session_01Fkeafxop88KcEs5Qbe8stB`) → Mac | reçu directement. §5 sans arrêt : `$T` = répertoire de travail, `devenv/env-57` = 10b6dd3, propre ; Claude Code 2.1.323 ; `CLAUDE_PROJECT_DIR` vide dans le Bash ; empreintes `settings.json`, hook, enveloppe = Mac ; pas de `settings.local.json` ; **3 règles `allow` utilisateur** dans `~/.claude/settings.json` (10 nov.) : `Bash(pipx install:*)`, `Bash(git clone * https://github.com/lepton-distribution/*)`, `Bash(python3 -m unittest discover *)` ; journal `342f0a58-….jsonl` ; Debian 13.7, git 2.47.3, scion 0.6.3.0, chaîne = R53-1, `rsync` absent (non requis), 18 Go libres ; `têtes publiées = Mac` ; `$U`, `$E13` = attendu (3889, 23 entrées, noyau 58e421e, 108 760 Ko) ; `$C5` : graine 6d3d2a5, 5 entrées, `salut` 71e1641 `modifs=2`, 3059 liens, 2 clones tiers F7 ; étapes §6 à §15 prévues |
| AVANCEMENT R57-1 (§6 avant) | 2026-11-13 | VM → Mac | noyau `$K` 58e421e → ed2a41f (avance rapide, 5 fichiers) ; `SCION_REF` 0.6.3.1 (noyau, lepton-tools) ; `SCION_MIN_VERSION` (0, 6, 2, 0) ; `.vsix` 0.5.2 présent ; lancement des 3 installations |
| AVANCEMENT R57-1 (§6, C1) | 2026-11-13 | VM → Mac | `install-debian.sh` code 0, scion 0.6.3.1 depuis `seed.scions.git@0.6.3.1` (Python 3.13.5) ; `pipx install --force ~/lepton-tools-dev/lepton-tools` accepté sans invite, lepton 0.1.0 ; `install-vscodium.sh` code 0, `changements 0` ; `scion 0.6.3.1 (requis ≥ 0.6.2.0)` ; extensions = attendu |
| AVANCEMENT R57-1 (§7, §8 jusqu'à N4) | 2026-11-13 | VM → Mac | §7 : copie 3059 liens, `check` 0, dépôt `$D` créé (edb9d14) ; P3 (e98a482), P4, P5 code 0 ; N1, N2, N2b code 2 ; N3 exécuté sans invite (cible absente) ; N4 lancé, refus attendu de l'utilisateur |
| AVANCEMENT R57-1 (§8, écart N4) | 2026-11-13 | VM → Mac | invite N4 parue mais **confirmée** au lieu d'être refusée (`accept user_temporary projectSettings`) ; scion code 1, « n'est pas un rootstock », sans effet, cible absente ; arrêt, question posée à l'utilisateur dans la session VM |
| AVANCEMENT R57-1 (§8, N4 rejoué) | 2026-11-13 | VM → Mac | N4 rejoué à la demande de l'utilisateur : invite refusée, tour interrompu ; le premier N4 reste un écart ; reprise au N5 |
| AVANCEMENT R57-1 (§8, C2) | 2026-11-13 | VM → Mac | `8-decisions.tsv` : `pipx install` `rule projectSettings` ; P3, P4, P5, N1, N2, N2b `subcommandResults` ; N3 `classifier` (accepté) ; N4 (1er) `user_temporary`, N4 rejoué et N5 `rejet-invite` ; N6 `reject subcommandResults projectSettings` (deny) ; N7 `reject hook hook` ; cibles absentes, liens de `$S` = départ ; `install-debian.sh` et `install-vscodium.sh` : `classifier` (acceptés) |
| AVANCEMENT R57-1 (§9, 1/4 à 4/4, C3) | 2026-11-13 | VM → Mac | 4 `graft-update` sur invite confirmée par l'utilisateur. `env-28-debian`, `env-13-debian`, `env-53-debian` : code 0, noyau seul 58e421e → ed2a41f, 0 clone, 0 conflit, « 3889 feuilles liées », 0 `.DS_Store`, journal = Mac (82), liens inchangés, `CONFORME` (avant et R50-1), tiers 0 / 16, `clones = Mac`, `ignorecase` vide, `check` et `generate` 0, espace identique ; `env-53-c5` : noyau seul, 3059 liens inchangés, `CONFORME`, 2 clones F7 0 / 4, `salut` accepté (`modifs=2`), graine 6d3d2a5 inchangée. `depots/tiers` de `env-53-debian` 87 512 Ko (clones neufs, `.git` de STM32CubeWL 3 588 Ko), informatif |
| AVANCEMENT R57-1 (§10, §11.1 ; C4, C5) | 2026-11-13 | VM → Mac | §10 (D13) : `essai.sh` code 0, 21 `état :` vides, aucun `rmdir` ni `≠ départ`, **c4 : écarts=0 / 231** ; 10 `*-status.out` différents, informatifs (graine `env11` `master` 6d3d2a5 au lieu de `main` 124db52 ; emplacements `ssh://git@github.com/…` au lieu de `https://…` pour les clones de `$C5`) ; liens de `$S` = départ. §11.1 (D14) : codes = attendu, aucun résidu, e04 et e05 préexistants gardés, `scion.txt` 0.6.3.1 (pipx, Python 3.13), **c5 : écarts=0 / 48** ; seul répertoire vide : `depots/origin/scion/sources`, préexistant ; pytest lancé |
| AVANCEMENT R57-1 (§11.2, C5 ; §12.1 lancé) | 2026-11-13 | VM → Mac | pytest `venv-test` (Python 3.13) par `--junitxml` : **453 tests, 0 échec, 0 erreur, 0 ignoré**, 2 min 16 ; hook 118, enveloppe 52 ; lepton éditable depuis `$T` ; lepton-tools propre. `devenv/env-57-debian` créée depuis 10b6dd3 ; `rejouer-oracle.sh` lancé dans `$R53` (host et 16 presets, ≈ 1 h) |
| AVANCEMENT R57-1 (§12, C6) | 2026-11-13 | VM → Mac | `rejouer-oracle.sh` code 0 ; host ctest 7/7 ; 16 oracles (nombres de symboles = R53-1) ; fumée ×6 ; bancs an386 20/20 ×2, soft 16/16 ×2, an500 19/19 ×2 ; `peripheriques` ×4 ; trunk de `$R53` 3889, 0 cassé, 0 régulier, 0 `__pycache__` ; mklepton = R53-1 = `env-52-apres` ; **`comparer_R53-1` 0 et `hors_debug=0` ×16** ; `comparer_Mac` 1 (informatif) ; `mirror-sync --dry-run` code 0, 8 miroirs à 0 référence et 0 signalement, `CONFORME`, rien envoyé ; rédaction du rapport |
| QUESTION R57-1 (push) | 2026-11-13 | VM → Mac et utilisateur | rapport commité sur `devenv/env-57-debian` (6df0de1, sur 10b6dd3) : `rapports/env-57-debian.md`, `rapports/env-57-debian/` (`8-decisions.tsv`, `10-c4/`, `11-c5/`, `11-pytest.xml`, `regreffes/`), `oracles/env-57-debian/` ; C1 à C6 atteints, écart C2 (premier N4), C7 écarté ; accord du push demandé à l'utilisateur dans la session VM (PA-P) ; le §14 suit |
| AVANCEMENT R57-1 (push ; §14, C8) | 2026-11-13 | VM → Mac | push de `devenv/env-57-debian` sur invite confirmée par l'utilisateur, 6df0de1 publié ; relevé avant nettoyage : `env-57-essai` 126 Mo, `env-57-depot` 276 Ko, `~/env-53-journaux` 16 Mo, `env-11/qemu` 160 Mo (seul contenu d'`essais/env-11` ; `salut` 71e1641 sans amont, `modifs=2`, noyau 1dde0af) ; `supprimer-essai.sh` : 3 supprimés ; `rm -rf essais/env-11/qemu` puis `rmdir essais/env-11` demandés à l'utilisateur (D15) |
| FIN-SUCCÈS R57-1 | 2026-11-13 | VM → Mac | reçu. C1 à C6 et C8 atteints, C7 écarté ; rapport `rapports/env-57-debian.md`, relevés `rapports/env-57-debian/`, oracle `oracles/env-57-debian/`, commit 6df0de1 sur 10b6dd3, `devenv/env-57-debian` poussée. Écart C2 : premier N4 confirmé, sans effet, rejoué et refusé. Constats : réf. 153462, 3 règles `allow` utilisateur, `CLAUDE_PROJECT_DIR` vide, installateurs, `rejouer-oracle.sh` et `mirror-sync` par le classifieur, reconstruction ≈ 3 min 30, empreintes binaires différentes de R53-1 (`__DATE__`, `__TIME__`) avec `comparer` 0, tailles de `$R53`, git en français. C8 : `essais/env-11/qemu` et `essais/env-11` supprimés par l'utilisateur ; restent `env-13-debian`, `env-28-debian`, `env-53-c5`, `env-53-debian`. Messages : tous acceptés par le serveur, aucun renvoi. Non fait : C7, `~/tmp-pytest` |

## 4. Rootstocks d'essai du Mac (tâche 3)

Accord de l'utilisateur au PA-101 (PA-P), pendant R57-1. scion 0.6.3.1, lepton 0.1.0. Script
`env-57-mac/regreffer-essai.sh avant|apres` ; entre les deux, la session lance
`scion graft-update -v <rootstock> > <journal> 2>&1; echo "code=$?" >> <journal>`. Attendu des liens :
la liste d'avant du rootstock (ed2a41f ne change rien de greffé). Journaux et bilans :
`~/lepton-tools-dev/essais/env-57-mac/regreffes/<rootstock>-*`.

Inventaire avant : clones de greffons sur `master`, amont réglé, propres, noyau 58e421e partout ;
graines de projet locales sans amont. La graine de `bout-en-bout` porte ses 2 fichiers non suivis
du 2026-11-02 (`modifs=2`, connus depuis ENV-50).

| Rootstock | `graft-update` | Liens avant → après | Ajouts / retraits | `controler-trunk.py` | Clones tiers | `check` | Espace |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `env-13-vierge` (§1.3) | 0 ; noyau 58e421e → ed2a41f seul | 3889 → 3889 | 0 / 0 | `CONFORME` | 8, = attendu (0 / 16), 107 992 Ko inchangés | 0 | identique |
| `env-9` | 0 ; noyau seul | 3059 → 3059 | 0 / 0 | `CONFORME` | — | 0 | identique |
| `env-11/qemu` | 0 ; noyau seul | 3059 → 3059 | 0 / 0 | `CONFORME` | — | 0 | identique |
| `env-11/qemu-gra2` | 0 ; noyau seul (BSP an386 réinscrit), puis `scion graft-remove lepton@bsp-qemu-mps2-an386 <rootstock>` code 0, 8 feuilles, clone conservé | 3051 → 3051 | 0 / 0 | `CONFORME` | — | 1 (attendu, CFG-5) | identique |
| `env-11/bout-en-bout/rootstock` | 0 ; noyau seul | 3059 → 3059 | 0 / 0 | `CONFORME` | — | 0 | identique |
| `env-11/f429zi` | 0 ; noyau seul | 3294 → 3294 | 0 / 0 | `CONFORME` | 2, = attendu (0 / 4), 36 528 Ko inchangés | 0 | identique |
| `env-11/wl55jc1` | 0 ; noyau seul | 3315 → 3315 | 0 / 0 | `CONFORME` | 4, = attendu (0 / 8), 40 684 Ko inchangés | 0 | identique |

Partout : aucun `git clone`, aucune ligne `extraction partielle,` (clones tiers déjà partiels),
0 conflit ni refus, 0 lien cassé, 0 fichier régulier, 0 `.DS_Store` dans les trunks.

Décisions (journal de session, `decisions.py`) : les 7 `graft-update` sur invite `ask` confirmée par
l'utilisateur (`user_temporary`, `projectSettings`), de 15:33 à 16:24 UTC ; le `graft-remove`, hors
règle, accepté par le classifieur. Aucun refus.

## 5. Vérification du rapport VM (tâche 4)

Branche `devenv/env-57-debian` récupérée à 6df0de1 (un commit sur `devenv/env-57` 10b6dd3). Elle
n'ajoute que `rapports/env-57-debian.md`, `rapports/env-57-debian/` (306 fichiers : `10-c4/` 242,
`11-c5/` 50, `regreffes/` 12, `8-decisions.tsv`, `11-pytest.xml`) et `rapports/oracles/env-57-debian/`
(96 fichiers) : 403 ajouts, aucun autre chemin touché. Contrôles refaits au Mac sur le contenu
poussé, extrait par `git archive` dans le répertoire de session :

| Critère | Contrôle refait au Mac | Résultat |
| --- | --- | --- |
| C2 | `8-decisions.tsv` | `pipx install` `rule projectSettings` ; P3, P4, P5, N1, N2, N2b, pytest `subcommandResults` ; 4 `graft-update` `user_temporary projectSettings` ; N3, installateurs, `rejouer-oracle.sh`, `mirror-sync` `classifier` (acceptés) ; premier N4 `user_temporary` (écart), N4 rejoué et N5 `rejet-invite` ; N6 `reject projectSettings` ; N7 `reject hook` |
| C3 | journaux `graft-update` de `env-28-debian`, `env-13-debian`, `env-53-debian` normalisés contre `attendu/c3/graft-update-resume.txt` ; `clones.txt` contre `env-53-mac/attendu/clones-rootstock-mac.txt` (hors `ignorecase` et tailles) ; bilans | journal = Mac ×3 ; clones = Mac ×3 ; noyau seul, 3889 → 3889, `CONFORME`, 0 / 16, `check` 0, espace identique ; `env-53-c5` : 3059 → 3059, `CONFORME`, 0 / 4, `check` 0 |
| C4 | `10-c4/` contre `attendu/c4/` (langue de git normalisée) | **0 / 231** ; aucun `rmdir` ni `≠ départ` dans les `.etat` ; les 10 `*-status.out` diffèrent par la base de la copie (graine `env11` `master` 6d3d2a5 contre `main` 124db52, emplacements `ssh://` contre `https://`, dépôt `$D` edb9d14 contre 2d17a36, et un preset `release-qemu` de moins dans la graine de la VM), informatif |
| C5 | `11-c5/` contre `attendu/c5/` ; `11-pytest.xml` | **0 / 48**, aucun résidu ; pytest 453 tests, 0 échec, 0 erreur, 0 ignoré ; hook 118 |
| C6 | `comparer-oracle.py` `env-53-debian` → `env-57-debian`, 16 presets ; `mklepton-empreintes.sha256` ; `construction.log` ; `banc-kal.log` | **0 ×16** ; mklepton = `env-53-debian` = `env-52-apres` ; reconstruction complète (configuration faite, autant d'objets compilés qu'en R53-1 : 164, 140, 163 pour an386 embOS, WL55 FreeRTOS, F746 embOS) ; `peripheriques` Passed ×4 |

Le rapport VM a les rubriques demandées au §15 de la consigne. Les messages postérieurs à son
commit (QUESTION du push, §14, `FIN-SUCCÈS`) figurent au §3 ci-dessus.

Écarts retenus pour la clôture :
- **Premier N4 confirmé** au lieu d'être refusé (erreur de manipulation à l'invite, sans effet :
  cible absente). L'invite a paru, ce qui prouve la règle `ask` ; le refus a été obtenu au rejeu.
- **Règles `allow` utilisateur sur la VM** (`~/.claude/settings.json` du 10 nov.), hors du dépôt :
  `Bash(pipx install:*)`, plus large que la règle du dépôt, `Bash(git clone * https://github.com/lepton-distribution/*)`,
  `Bash(python3 -m unittest discover *)`. Aucune décision relevée ne leur revient ; ajouté au
  hors-plan (D19).
- **Une redirection vers un fichier fait sortir une commande de sa règle `allow`** (§1.5) : écrit
  dans la consigne, pas encore dans ORCHESTRATION §2bis ; ajouté au hors-plan (D20).
- Durée de la reconstruction mal annoncée dans la consigne (« ≈ 1 h ») : environ 3 min 30 sur la
  VM ; sans effet.
- Empreintes binaires différentes de R53-1 pour les 16 presets (`__DATE__`, `__TIME__`), `comparer`
  à 0 : forme attendue, comme aux validations précédentes.

## 6. PA-102 et fin du plan (2026-11-13, décisions de l'utilisateur)

- PA-102 (PA-P) : rapport VM accepté (vérifié au §5). Fusion `--no-ff` de `devenv/env-57-debian`
  (6df0de1) dans `devenv/env-57`, commit d'état et de passation, fusion `--no-ff` de
  `devenv/env-57` dans `main`, push de `main` et de `devenv/env-57`.
- `HORS-PLAN.md` présenté (fin du plan) : D17, D18, D19 et D20 **à traiter**, à planifier à la
  prochaine révision du plan ; A1 à A4, D4 et D12 reconfirmés hors plan ; D14, D16 prouvés sur la
  VM et D15 clos par ENV-57.
