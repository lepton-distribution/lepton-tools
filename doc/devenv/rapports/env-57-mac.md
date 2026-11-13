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
| C6 | `mirror-sync --dry-run` dans `essais/env-53-debian` ; reconstruction écartée |
| C7 | écarté |
| C8 | copie et dépôt d'essai, `~/env-53-journaux` par l'enveloppe ; `essais/env-11/qemu` par l'utilisateur |

Préalable (§0) : l'utilisateur fait `git switch devenv/env-57` sur la VM et relance la session VM
dans `~/lepton-tools-dev/lepton-tools`, pour qu'elle lise les règles du dépôt ; le contrôle N7 (hook)
et les décisions `subcommandResults` le prouvent.

Écarts au fichier d'étape, soumis au PA-101 :
- `$C5` regreffé en C3, en plus de `$U` et `$E13` : sinon la graine de projet de référence de la VM
  resterait à 58e421e quand celle du Mac passe à ed2a41f (tâche 3), la dérive qui a causé la
  QUESTION de R53-1 (D15). La copie de C4 et C5 est faite avant cette regreffe ;
- C6 sans reconstruction des 16 presets (forme d'`env-56-scion.md` §6) ;
- `install-vscodium.sh` lancé une fois (la seconde exécution de R53-1 n'apportait rien :
  `changements 0` dès la première).

## 2. PA-101

(À compléter.)

## 3. Messages §2bis

| Message | Date | Sens | Résumé |
| --- | --- | --- | --- |

## 4. Rootstocks d'essai du Mac (tâche 3)

(À compléter.)

## 5. Vérification du rapport VM (tâche 4)

(À compléter.)
