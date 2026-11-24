# ENV-72 — Validation Debian groupée (ENV-67 à ENV-71) — rapport de la session Mac

Session Mac `validation-debian-env-72`, 2026-11-24. Branche lepton-tools `devenv/env-72` (depuis
`main` 8cbbf25). Consigne VM : `consignes/env-72-debian.md`. Journaux Mac :
`~/lepton-tools-dev/essais/env-72-mac/`. Essais : `~/lepton-tools-dev/essais/env-72-essai/`
(`c4/rs`, `c4d/rs`, `seed-scions`), `~/lepton-tools-dev/essais/env-72-fixture/`.
Outils Mac : scion 0.6.3.4 et lepton 0.1.0 (pipx), extension 0.5.4, git 2.50.1 (et 2.18.0 pour
fixture70), Python 3.11.5, Claude Code 2.1.331.

## 1. Préparation (tâche 1)

### 1.1 Têtes publiées (`git ls-remote`, 2026-11-24)

Relevé : `env-72-mac/ls-remote-mac.txt` (script `env-72-mac/ls-remote.sh`, repris
d'`env-66-mac/ls-remote.sh` avec le tag 0.6.3.4). Différences avec le relevé d'ENV-66 :

| Dépôt | Référence | Commit | En R66-1 |
| --- | --- | --- | --- |
| `lepton-tools` | `main` | 8cbbf25 | 6bc05ad |
| `seed.scions` | tag `0.6.3.4` (`master` 929c01a) | 473b653 | tag `0.6.3.3` 9615cd5 (`master` 49ca4ae) |
| `lepton-original-tree.scions` (noyau) | `master` | 0c2e43e | 2b4a647 |
| `mirror-cmsis_device_f4` | HEAD | 8c79dcf | 9192c7b |
| `mirror-stm32f7xx-hal-driver`, `mirror-cmsis_device_f7` | HEAD | e879045, 52e4aad | e860c4f, 2352e88 |
| `mirror-stm32wlxx-hal-driver`, `mirror-stm32-mw-subghz-phy`, `mirror-STM32CubeWL` | HEAD | e388844, 47c14de, 2259ce0 | 5c87cf0, 7dc059f, f934cd2 |
| graine `original-tree`, 12 autres greffons, tags épinglés des 8 miroirs | | inchangés | = |

- Les HEAD des miroirs ont avancé par l'envoi d'ENV-71 (D40) ; les tags épinglés par les
  projections (`v1.8.5`, `v1.3.3`, `v1.2.10`, `v1.6.0`, `v1.4.0`, `v1.5.0`, `v1.6.0`, et
  3c77349 pour `cmsis_device_f4`) sont inchangés : aucun clone tiers ne change.
- Le noyau 0c2e43e (fusion d'e9b52e4, ENV-70) ne change que 5 fichiers hors de `scion/`
  (`git diff --stat 2b4a647 0c2e43e` : `README-PAQUET.md`, `README.md`, `doc/BUILDING.md`,
  `scripts/install-debian.sh`, `scripts/install-macos.sh`, 6 lignes ; 0 sous `scion/`) :
  `SCION_REF` 0.6.3.4. Rien n'est greffé, aucun lien ne change : une regreffe n'avance que le
  clone noyau.
- `.claude/settings.json` (`b01ad557…d235`) et `proteger-trunk.py` (`04572df6…6909`) sont
  inchangés depuis R61-1 ; `supprimer-essai.sh` est `369dae36…b9c8` depuis 7a54b2d (ENV-67,
  D38 (2)) ; `comparer-releves.py` `2bd102cd…5d8c`, inchangé depuis ENV-66.

### 1.2 Liens du trunk de `<ROOTSTOCK>`

`env-43-mac/controler-trunk.py ~/lepton` contre `env-50-mac/attendu/trunk-liens.txt` : code 0,
`CONFORME` (3889 liens, 0 fichier régulier, 0 lien cassé, 629 projetés, 0 écart, 8 clones tiers
aux HEAD épinglés, filtre `blob:none`). `env-72-mac/trunk-avant/liens.txt` = `env-71-miroirs/
trunk-apres/liens.txt` (`cmp`).

### 1.3 Essai préalable : `graft-update` d'`essais/env-13-vierge` (attendu de C3)

PA-P accordé par l'utilisateur pendant la préparation (2026-11-24). État avant : graine
`depots/lepton-seed.scions/original-tree` sur `original-tree` (15740f9, amont réglé, propre : D33
ne la refuse pas) ; 13 clones de greffons sur `master`, propres ; noyau 2b4a647 ; 3889 liens.
`env-57-mac/regreffer-essai.sh avant`, puis, lancée par la session hors script (invite `ask`,
confirmée) : `scion graft-update -v ~/lepton-tools-dev/essais/env-13-vierge > …/env-13-vierge-graft-update.log 2>&1; echo "code=$?" >> …`,
puis `apres`.

| Contrôle | Résultat |
| --- | --- |
| `graft-update -v` (scion 0.6.3.4) | code 0 ; 1 clone avancé : `…/original/master avancé : 2b4a647 -> 0c2e43e` ; 0 `git clone` ; 0 extraction partielle ; 0 conflit ni refus ; « 3889 feuilles liées » ; « 6 chemin(s) ignoré(s) par git » (`.DS_Store` du Finder) |
| Inventaire | seule la ligne du noyau change |
| Liens | 3889 → 3889, 0 ajouté, 0 retiré ; `controler-trunk.py` `CONFORME` |
| Clones tiers | extraits et `sparse-checkout` = attendu, 0 / 16 ; `depots/tiers` 107 992 → 107 992 Ko |
| `lepton check`, `generate` | 0, 0 ; espace identique |

Attendus versionnés (`<R>`, `<HOME>`) : `attendu/c3/graft-update-resume.txt` (83 lignes, filtre
`resume()` de la consigne), `env-13-vierge-bilan.txt`, inventaires avant et après. Contre
`env-66-mac/attendu/c3/` : seule la ligne du noyau change (`dfc960b -> 2b4a647` devient
`2b4a647 -> 0c2e43e`). La ligne `fatal: not a git repository …` (D22) reste : D35 garde la
première ligne `fatal:`, c'est la même.

### 1.4 Attendus de C4 (D29, D30, D32, D37)

Scripts d'ENV-68 repris dans `env-72-mac/` : `chemins.sh` et `graine.sh` ne diffèrent des
originaux que par la copie, faite par `tar` (fonction `copier`, 5 appels `rsync -a` remplacés) :
`rsync` est absent de la VM (`rapports/env-66-debian.md` §9). shellcheck sans remarque au niveau
`warning`.

Copie d'essai `essais/env-72-essai/c4/rs` : `tar --exclude=./build` d'`essais/env-11/qemu`
(noyau 2b4a647, graine `env11` 124db52, 3059 liens). Puis `chemins.sh <E> apres attendu/c4-chemins`
(code 0, 8 min 18 s) et `graine.sh <E> apres-graine attendu/c4-graine` (code 0).

| Attendu | Relevés | Contre ENV-68 (`env-68-lepton/apres/`, `apres-graine/`) |
| --- | --- | --- |
| `attendu/c4-chemins/` | 165 | identique, sauf `resume.tsv` : la colonne du message est tronquée avant la normalisation, sa fin suit la longueur des chemins (`env-68-essai` → `env-72-essai/c4`) |
| `attendu/c4-graine/` | 244 | identique, sauf `r1-status.out` : commit local de la graine après `seed add` (3a7aef0 → f6aed02), recréé à chaque passage |

La copie par `tar` donne donc les mêmes relevés que la copie par `rsync`.

### 1.5 Contrôle de la consigne sur une copie d'origine distincte (D38 (3))

Copie `essais/env-72-essai/c4d/rs` : `tar` d'`essais/env-11/qemu` sans `build/`, sans aucun
`.DS_Store` (20 au départ, racine et clones) ni `./.scion.trunk.tolerated` (racine de `$C5` de la
VM, `rapports/env-67-consignes.md` §3) ; graine `env11` portée à une autre version : configuration
`release-qemu` retirée de `lepton-graine.json` (3b53dda), presets régénérés par `lepton generate`
et commités (da02c79 ; `presets : env11-debug-qemu`, forme de la VM) ; `check` code 0, 3059 liens.
Puis la forme de la consigne : `env-72-mac/chemins.sh <c4d> apres <sortie> clangd-mp-21`,
`env-72-mac/graine.sh <c4d> apres-graine <sortie>` (codes 0), comparés à l'attendu par
`scripts/comparer-releves.py`. Relevés : `essais/env-72-mac/c4d/` ; bilans de comparaison versionnés : `env-72-mac/c4d-cmp/`.

| Sortie | Bilan | Classe | Fichiers |
| --- | --- | --- | --- |
| `c4-chemins` | `écarts=13 / 165` | fichiers ignorés du Mac | `n1-a.err`, `n1-d.err`, `n1-r.err`, `n1-t.err`, `n1-u.err` : ligne « greffe : 13 chemin(s) ignoré(s) par git » absente |
| | | graine (presets) | `p6-a.out`, `p6-n.out`, `p6-r.out`, `p6-rd.out`, `p6-rs.out`, `p6-rw.out`, `p6-t.out` : `presets : env11-debug-qemu` seul |
| | | longueur des chemins | `resume.tsv` : colonne 7 (message) tronquée avant normalisation ; colonnes 1-6 identiques |
| `c4-graine` | `écarts=2 / 244` | graine (commit, configurations) | `g1-status.out`, `r1-status.out` : commit de la graine et de son greffon de projet (124db52 → da02c79), configuration `release-qemu` absente |
| | | commits locaux | `r1-status.out` : commit de `library-env68lib` après `seed add` (f6aed02 → 6d36d14) |

Aucun écart hors de ces classes. Les `.vs-depart`, `.vs-ajoute` (états relatifs) et tous les
codes sont identiques. Les scripts d'ENV-68 ne relèvent pas la racine du rootstock (pas de
`*.W`, à la différence d'`env-63-tilde/chemins.sh`) : la classe « racine » d'ENV-67 ne paraît pas.

Classes que le Mac ne peut simuler, listées dans la consigne (§10, §11) :
- **hôte** : nom et chemin de clangd (`p6-n.cmd`, `p6-n.clangd`) ;
- **langue de git** : messages en français, ramenés par `comparer-releves.py` (une traduction
  absente de la table reste un écart à relever) ;
- **git de la VM** : `k01-218.git-err`, `k01-250.git-err` de fixture70 (sorties brutes) ;
- **shell** : zsh absent de la VM (D38 (4), hors plan) ; aucun script de la consigne ne l'appelle.

Erreur relevée et corrigée dans la consigne par ce contrôle : le message du `resume.tsv` de
`chemins.sh` d'ENV-68 est en colonne 7 (en colonne 8 dans celui d'ENV-63) ; la consigne compare
les colonnes 1 à 6.

### 1.6 Attendus de C5 (D35, D33)

Clone `essais/env-72-essai/seed-scions` (`git clone https://github.com/lepton-distribution/seed.scions.git`,
puis `switch --detach 0.6.3.4`, 473b653, propre). Base `essais/env-72-fixture/{f70,f65,f60,f56}`,
scion `~/.local/bin/scion` (0.6.3.4).

`env-72-mac/fixture70.py` : `env-70-scion/fixture.py` dont le git des appels `--single-branch`
(k01, k02, et la sortie brute `k01-218`) devient le 5ᵉ argument, obligatoire. La version
d'ENV-70 fige `/usr/local/git/bin/git` (git 2.18.0 du Mac), absent de la VM ; sur la VM, le
5ᵉ argument est `/usr/bin/git` (2.47.3), qui écrit l'avertissement de lui-même. L'enveloppe
`env-70-scion/bin/git` et les modules importés restent ceux d'ENV-70.

| Fixture | Code | Relevés | Contre ENV-70 (`env-70-scion/fixture*-apres/`) |
| --- | --- | --- | --- |
| `fixture70.py` (5ᵉ argument `/usr/local/git/bin/git`) → `attendu/fixture70/` | 0 | 202 | identique |
| `env-65-scion/fixture.py` → `attendu/fixture65/` | 0 | 284 | identique |
| `env-60-scion/fixture.py` → `attendu/fixture60/` | 0 | 179 | identique |
| `env-56-scion/fixture.py` → `attendu/fixture56/` | 0 | 76 | identique, sauf la profondeur de la base dans f12a, f12b (`.depots`, `fixture.tsv` : `env-70-fixture/apres/fixture56` → `env-72-fixture`) |

La VM utilise la même base `essais/env-72-fixture` : 0 écart attendu pour 65, 60, 56. Pour
fixture70, deux fichiers diffèrent par nature : `k01-218.git-err` et `k01-250.git-err`, sorties
brutes de git (2.18.0 et 2.50.1 au Mac, 2.47.3 deux fois sur la VM).

**Preuve de D35 attendue sur la VM** : `k01.err`, `k02.err`, `k03.err` (fixture70), `k07.err`
(fixture60) et `f05.err` (fixture56) se terminent tous, au Mac, par `(code 128) : fatal: Remote
branch nope not found in upstream origin`. En R66-1 (scion 0.6.3.3), k07 et f05 portaient
l'avertissement `warning: Could not find remote branch nope to clone.` ; le témoin k03 (git
2.47.3 sur la VM, sans enveloppe) est le cas réel.

**En français** (consigne §11.2) : la même commande que k03, relancée hors `LC_ALL=C` sur le
rootstock de k03 laissé par la fixture (k03 ne crée rien). Au Mac : code 2, cause anglaise
(git non traduit), `depots` vide. Sur la VM, attendu d'après le PA-127 et la reproduction de
R66-1 (`rapports/env-66-debian.md` §5.3) : `fatal⍽: La branche distante nope n'a pas été trouvée
dans le dépôt amont origin`.

### 1.7 Autres attendus et contrôles de la consigne (D27)

pytest complet (`venv-lepton-tools`, `--junitxml`, scion 0.6.3.4 du PATH) : **616 passed**, 0 échec,
0 erreur, 0 ignoré (11 min 44, en même temps que le contrôle du §1.5) ; `test_proteger_trunk` 118,
`test_garde_ask` 46, `test_supprimer_essai` 70, `test_milestone3` 62, `test_comparer_releves` 13.
= ENV-70 (616).

Contrôles d'installation écrits d'après le code installé au Mac (piège d'ENV-61) :
- lepton : 18 modules `lepton/*.py` ; ceux du venv pipx (`os.path.dirname(lepton.__file__)`)
  sont comparés un à un au dépôt ;
- scion : `scion.__version__` = `0.6.3.4` et `scion.gitops.cause` présent (D35, d987923) ;
- extension : `extension/dist/lepton-0.5.4.vsix` seul (`31678dd3…b8d1`) ; le répertoire installé
  `lepton-distribution.lepton-0.5.4` porte `out/src/batch.js` (nouveau en 0.5.4) et
  `out/src/watch.js` observe `.scion.grafted.list` (D36).

C6 (T3 de D36) : forme de `rapports/env-69-extension.md` §4.1, greffon `env72lib`
(`lepton scion new --no-seed`, 3 fichiers) : 3059 → 3062 liens après `seed add`, 3 cassés après
la suppression du clone par l'enveloppe.

C7 : `LEPTON_EMBOS_ROOT` vient du profil de la VM (§0, PA-121) ; le premier passage de
`rejouer-oracle.sh` doit réussir, contrairement à R66-1 (8 embOS en échec au premier passage).

## 2. PA-131 — questions (à trancher par l'utilisateur)

1. **Consigne** `consignes/env-72-debian.md`, dont le **§0** : `switch` de lepton-tools sur
   `devenv/env-72` ; `export LEPTON_EMBOS_ROOT="$HOME/lepton/third_party/embos/cortexm-gcc/5.20.0.0"`
   ajouté à la fin de `~/.bashrc` de la VM (aucun export aujourd'hui, `rapports/env-67-consignes.md`
   §1.1), vérifié dans un nouveau terminal, puis session ouverte depuis ce terminal ;
   `~/.claude/settings.json` inchangé. Le §5 relève les 7 variables du PA-121 et s'arrête sur
   tout écart.
2. **C3** : regreffe de `$U`, `$E13`, `$C5`, `$R53` (le noyau a changé ; PA-P pour les 4
   `graft-update`), après relevé de la branche de chaque graine clonée (D33). Proposition : oui.
3. **C6** : extension 0.5.4 par `install-vscodium.sh` ; **T3 de D36 dans VSCodium sur la VM**, par
   l'utilisateur (§11.4 : relevé du canal avant et après un `seed add` au terminal, puis
   notification après la suppression du clone ; inotify, seule preuve sur Linux). Proposition :
   oui si vous avez accès à l'interface de la VM, sinon D36 reste prouvé au Mac seulement.
4. **C8, cartes** : proposition : écarté (ni binaire, ni flash, ni sonde ne changent).
5. **C9, nettoyage** : `essais/env-72-essai`, `essais/env-72-fixture`, `~/env-66-journaux`,
   `~/tmp-pytest/env-66`, `~/tmp-pytest/env-72-enveloppe` par `scripts/supprimer-essai.sh`
   (descendants de `~/tmp-pytest`, D38 (2)) ; conservés `$U`, `$E13`, `$C5`, `$R53`,
   `~/env-72-journaux`, `~/tmp-pytest/env-72`.
6. **C7** maintenu : host et 16 presets contre `env-66-debian` (aucune source compilée ne change ;
   prouve aussi `LEPTON_EMBOS_ROOT` au premier passage) ; `mirror-sync --dry-run` : 0 attendu.
7. **Noms des sessions** : session Mac `validation-debian-env-72` (à confirmer, ou nom réel de
   cette session) ; nom de la session VM après le §0.
8. **PA-P** : push de `devenv/env-72`, puis envoi de l'ordre `R72-1` à la session VM désignée
   après le §0.

Rootstocks d'essai du Mac (tâche 3) : `essais/env-13-vierge` est déjà regreffé (§1.3) ; restent
`essais/env-9` et, sous `essais/env-11/`, `qemu`, `qemu-gra2`, `bout-en-bout/rootstock`, `f429zi`,
`wl55jc1`, après l'`AVANCEMENT` « fin des invites de la VM » ou le `FIN-*` (D39), sur accord.

## 3. Rootstocks d'essai du Mac (tâche 3)

Accord de l'utilisateur (PA-P), 2026-11-24, après l'`AVANCEMENT` « fin des invites de la VM
jusqu'au push » de R72-1 (D39) : aucune invite de la VM n'était possible pendant ces regreffes.
scion 0.6.3.4, lepton 0.1.0. Script `env-57-mac/regreffer-essai.sh avant|apres` ; entre les deux,
la session lance `scion graft-update -v <rootstock> > <journal> 2>&1; echo "code=$?" >> <journal>`.
Journaux et bilans : `~/lepton-tools-dev/essais/env-72-mac/regreffes/<rootstock>-*`.

Inventaire avant : clones de greffons sur `master`, amont réglé, propres, noyau 2b4a647 partout ;
graines de projet locales sans amont (`env9`, `env11` ×2, `bout-en-bout`, `env11f4`, `env11wl`) ;
la graine de `bout-en-bout` porte ses 2 fichiers non suivis du 2026-11-02 (`modifs=2`, connus).

| Rootstock | `graft-update` | Liens avant → après | Ajouts / retraits | `controler-trunk.py` | Clones tiers | `check` | Espace |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `env-13-vierge` (§1.3) | 0 ; noyau 2b4a647 → 0c2e43e seul | 3889 → 3889 | 0 / 0 | `CONFORME` | 8, = attendu (0 / 16), 107 992 Ko inchangés | 0 | identique |
| `env-9` | 0 ; noyau seul | 3059 → 3059 | 0 / 0 | `CONFORME` | — | 0 | identique |
| `env-11/qemu` | 0 ; noyau seul | 3059 → 3059 | 0 / 0 | `CONFORME` | — | 0 | identique |
| `env-11/qemu-gra2` | 0 ; noyau seul (BSP an386 réinscrit, 3059 feuilles), puis `scion graft-remove lepton@bsp-qemu-mps2-an386 <rootstock>` code 0, 8 feuilles, clone conservé | 3051 → 3051 | 0 / 0 | `CONFORME` | — | 1 (attendu, CFG-5) | identique |
| `env-11/bout-en-bout/rootstock` | 0 ; noyau seul | 3059 → 3059 | 0 / 0 | `CONFORME` | — | 0 | identique |
| `env-11/f429zi` | 0 ; noyau seul | 3294 → 3294 | 0 / 0 | `CONFORME` | 2, = attendu (0 / 4), 36 528 Ko inchangés | 0 | identique |
| `env-11/wl55jc1` | 0 ; noyau seul | 3315 → 3315 | 0 / 0 | `CONFORME` | 4, = attendu (0 / 8), 40 684 Ko inchangés | 0 | identique |

Partout : aucun `git clone`, aucune extraction partielle (clones tiers déjà partiels), 0 conflit
ni refus, 0 lien cassé, 0 fichier régulier, 0 `.DS_Store` dans les trunks ; `generate` avant et
après : 0 (`qemu-gra2` : 1, attendu).

Décisions (journal de session, `decisions.py --motif graft-update --motif graft-remove`) : les 7
`graft-update` sur invite `ask` confirmée par l'utilisateur (`user_temporary`, `projectSettings`) :
`env-13-vierge` à 14:36 UTC (préparation, avant l'ordre), les 6 autres de 15:42 à 15:48 UTC
(après la fin des invites de la VM) ; le `graft-remove`, hors règle, accepté par le classifieur.
Aucun refus.

## 3bis. Contrôle du rapport VM (tâche 4)

`FIN-SUCCÈS R72-1` reçu. Branche `origin/devenv/env-72-debian` 9869e39, un commit sur 5411f78
(`devenv/env-72`) ; 1278 fichiers ajoutés, tous sous `rapports/env-72-debian*` et
`rapports/oracles/env-72-debian/` (aucun autre fichier touché). Relevés extraits par `git archive`
dans le répertoire temporaire de la session ; comparaisons refaites au Mac par
`scripts/comparer-releves.py --home-attendu /Users/cle_d_anton --home-obtenu /home/lepton-user`.

| Critère | Refait au Mac sur les relevés poussés | Verdict |
| --- | --- | --- |
| C1 | `5-variables.txt` : `LEPTON_EMBOS_ROOT` = attendu, six absentes, `LANG=fr_FR.UTF-8`, `LC_ALL` absente ; versions du `FIN` (scion 0.6.3.4, 18 modules, extension 0.5.4) | conforme |
| C2 | `15-decisions.tsv` : `pipx install --force` `rule projectSettings` ; U1, U2, R1, R2, E1, `git clone`, pytest, suppression de T3 `subcommandResults` ; A1 `accept user_temporary` (15:29:07, confirmée par erreur, sans effet) puis `rejet-invite` (15:30:15) ; H1 `reject hook` ; 4 `graft-update` `user_temporary projectSettings` (15:35:21 à 15:40:09) ; chemin personnel normalisé (`<HOME>`) | conforme (incident A1 consigné, décision (a) de l'utilisateur) |
| C3 | résumés régénérés des 3 journaux `graft-update` (filtre `resume()`) contre `attendu/c3/` : `écarts=1 / 1` ×3, diff limité à la variante « point de montage » (D34) ; bilans : noyau 2b4a647 → 0c2e43e seul ; `$C5` `CONFORME`, F7 0 / 4, `check` 0 | conforme (D34 admis, plan) |
| C4 | `c4-chemins` `écarts=15 / 165` : les 13 de la copie distincte (§1.5) + `p6-n.cmd`, `p6-n.clangd` (hôte) ; lignes changées : 7 `presets`, 5 « 13 chemin(s) ignoré(s) par git », clangd ; `resume.tsv` colonnes 1-6 identiques. `c4-graine` `écarts=2 / 244` (`g1-status.out`, `r1-status.out`) : commits, configuration `release-qemu` absente, branche de la graine (`master` sur la VM, `main` au Mac) et `location` des 3 greffons publiés (`ssh://git@github.com/…` contre `https://…`) | conforme (classe « graine `env11` », plus large que listé : défaut de la consigne) |
| C5 | fixture65 0 / 284, fixture60 0 / 179, fixture56 0 / 76, fixture70 2 / 202 (`k01-218.git-err`, `k01-250.git-err` : `warning` puis `fatal` par `/usr/bin/git` 2.47.3) ; k01, k02, k03, k07, f05 finissent par `fatal: Remote branch nope not found in upstream origin` ; `11-d35-fr.log` : `fatal` + U+00A0 + `: La branche distante nope…` (vérifié par `od`), code 2 ; pytest 616, 0 échec | conforme — **D35 prouvé avec git 2.47.3** |
| C6 | rapport et `FIN` : « Observation de 5 » → « de 6 » après `seed add` au terminal, une seule notification après la suppression du clone (centre de notifications, non affichée en surimpression) | conforme (constat d'affichage) |
| C7 | mklepton = `env-66-debian` = `env-52-apres` ; `comparer-oracle.py env-66-debian` code 0 pour les 16 presets ; ctest 7/7, banc 20/20, 16/16, 19/19 (×2), `peripheriques` ×4 ; `12-mirror-sync.log` : 8 × « 0 référence(s) à envoyer, 0 signalement(s) », code 0 | conforme |
| C8 | écarté (PA-131) | — |
| C9 | `FIN` : `env-72-essai`, `env-72-fixture`, `~/tmp-pytest/env-72-enveloppe` supprimés par l'enveloppe (liste corrigée) | conforme (hors commit, par le message) |

D39 : dernière invite de la VM avant le push à 15:40:09 UTC ; regreffes du Mac de 15:42:45 à
15:48:32 UTC, après l'`AVANCEMENT` « fin des invites » ; aucune commande à invite au Mac pendant le
push (16:49:10 UTC). Aucune invite simultanée.

Défauts de la consigne relevés pendant R72-1 (tous expliqués, aucun ne change un résultat) :
1. `~/env-66-journaux`, `~/tmp-pytest/env-66` donnés présents (supprimés par R66-2) ; §14 corrigé
   par décision de l'utilisateur ;
2. variante « point de montage » (D34) non listée au §9, bien qu'admise par le fichier d'étape ;
3. classe « graine `env11` » non détaillée : branche et URL déclarées de la graine de `$C5`, que la
   copie distincte du Mac (même URL, même branche qu'`essais/env-11/qemu`) ne pouvait pas montrer.

Constats de la VM, sans écart de critère : notification de D36 visible seulement dans le centre de
notifications ; `env11.code-workspace` copié de `$C5` avec son chemin absolu (clangd relancé sur
`$C5`, déjà vu en R66-1) ; répertoire de l'extension 0.5.3 laissé par VSCodium (comme au Mac) ;
`CLAUDE_PROJECT_DIR` vide dans Bash (déjà vu en R66-1).

## 4. Journal des messages (§2bis)

| ID | Type | Sens | Date (heure locale) | Résumé | Remis |
| --- | --- | --- | --- | --- | --- |
| — | annonce | VM → Mac | 2026-11-24 | session `debian-linux-vm` prête : `devenv/env-72`, tête 5411f78, arbre propre | reçu |
| R72-1 | ORDRE | Mac → VM | 2026-11-24 16:22 | consigne par chemin, commit 5411f78 et sha256 `5556a024…0f36` ; décisions du PA-131 ; invites à refuser et à confirmer ; D39 ; forme de fin | accepté par le serveur ; accusé reçu |
| R72-1 | ACCUSÉ | VM → Mac | 2026-11-24 | ordre reformulé ; Claude Code 2.1.331 ; tête 5411f78, sha256 de la consigne = ordre ; 4 empreintes = Mac ; variables du PA-121 conformes (`LANG=fr_FR.UTF-8`, `LC_ALL` absente) ; têtes = Mac ; `$U`, `$E13`, `$R53` : graine sur `original-tree` 15740f9, noyau 2b4a647, 3889 liens ; `$C5` : graine locale `env11` sur `master` 6d3d2a5, 3059 liens ; écart 1 : `~/env-66-journaux`, `~/tmp-pytest/env-66` absents | reçu |
| R72-1 | RÉPONSE | Mac → VM | 2026-11-24 | écart 1 = défaut de la consigne (chemins supprimés par R66-2, `handoff/env-66.md` l. 38) ; §5 et §8.2 : absence attendue ; §14 : correction à venir après décision de l'utilisateur ; poursuivre | accepté par le serveur |
| R72-1 | AVANCEMENT | VM → Mac | 2026-11-24 | §6 : noyau 2b4a647 → 0c2e43e, `SCION_REF` 0.6.3.4 (noyau et lepton-tools), `.vsix` 0.5.4 `31678dd3…b8d1` ; lancement des 3 installations | reçu |
| R72-1 | RÉPONSE | Mac → VM | 2026-11-24 | §14 corrigé (décision de l'utilisateur) : `supprimer-essai.sh` sur `env-72-essai`, `env-72-fixture`, `~/tmp-pytest/env-72-enveloppe` ; C9 en conséquence | accepté par le serveur |
| R72-1 | AVANCEMENT | VM → Mac | 2026-11-24 | §6 conforme (scion 0.6.3.4, `gitops.cause` ; lepton 18 modules = dépôt ; extension 0.5.3 → 0.5.4, `batch.js`, `watch.js` observe la liste ; ancien répertoire 0.5.3 resté, comme au Mac) ; §7 conforme (2 copies, 3059 liens, `check` 0, `depot72` bf69c9b, racine de `c4/rs` sans `.DS_Store`) ; deux RÉPONSES reçues | reçu |
| R72-1 | AVANCEMENT | VM → Mac | 2026-11-24 | §8.1-8.2 : réglages = R66-1 (2 règles) ; U1 code 1, U2 code 128, cibles absentes ; R1, R2 code 2, rien supprimé ; E1 code 0 (`sous/` supprimé, `g` gardé) ; A1 annoncé « À REFUSER » | reçu |
| R72-1 | QUESTION | VM → Mac | 2026-11-24 | A1 confirmée par erreur dans la session VM (`accept user_temporary projectSettings`, 15:29:07 UTC), sans effet (code 1, « n'est pas un rootstock », cible absente) ; options (a) relancer A1 pour la refuser, (b) consigner et poursuivre | reçu |
| R72-1 | AVANCEMENT | VM → Mac | 2026-11-24 | option (a) choisie par l'utilisateur dans la session VM ; A1 relancée, annoncée « À REFUSER » | reçu |
| R72-1 | AVANCEMENT | VM → Mac | 2026-11-24 | §8 terminé : A1 relancée `rejet-invite` (15:30:15 UTC) ; H1 `reject hook hook` ; cibles absentes, liens de c6 = départ ; U1, U2, R1, R2, E1 `subcommandResults` ; préparation du §8.2 au classifieur (hors règle, accepté) ; §9 : `graft-update` d'`env-28-debian` annoncé « À CONFIRMER » (1 sur 4), graine sur `original-tree` 15740f9 | reçu |
| R72-1 | QUESTION | VM → Mac | 2026-11-24 | `env-28-debian` regreffé, conforme hors du résumé : `écarts=1 / 1`, variante « point de montage » de git (D34) au lieu de la ligne « not a git repository » ; options (a) admettre pour `$U`, `$E13`, `$R53`, (b) arrêt | reçu |
| R72-1 | RÉPONSE | Mac → VM | 2026-11-24 | (a) : écart déjà admis par le plan (D34 hors plan, PA-120 ; fichier d'étape, Pièges connus), omis par la consigne ; admis seulement si le diff se limite à cette ligne ; poursuivre | accepté par le serveur |
| R72-1 | AVANCEMENT | VM → Mac | 2026-11-24 | RÉPONSE (a) reçue ; `graft-update` d'`env-13-debian` annoncé « À CONFIRMER » (2 sur 4), graine sur `original-tree` 15740f9, 3889 liens | reçu |
| R72-1 | AVANCEMENT | VM → Mac | 2026-11-24 | `env-13-debian` conforme (noyau seul, 3889 liens, `CONFORME`, 0 / 16, `check` 0 ; résumé : écart D34 seul) ; `graft-update` d'`env-53-c5` annoncé « À CONFIRMER » (3 sur 4), graine locale `env11` sur `master` 6d3d2a5, 3059 liens | reçu |
| R72-1 | AVANCEMENT | VM → Mac | 2026-11-24 | `env-53-c5` conforme (noyau seul ; `salut` accepté ; graine `env11` sans amont laissée ; 3059 liens, `CONFORME`, F7 0 / 4, `check` 0) ; `graft-update` d'`env-53-debian` annoncé « À CONFIRMER » (4 sur 4), graine sur `original-tree` 15740f9 | reçu |
| R72-1 | AVANCEMENT | VM → Mac | 2026-11-24 | **fin des invites de la VM jusqu'au push** (D39) ; §9 terminé : 4 regreffes, 4 invites confirmées, 4 codes 0 ; `env-53-debian` conforme (écart D34 seul) ; `$U`, `$E13`, `$R53` : même diff, la variante seule ; `$C5` sans écart ; passage au §10 | reçu |
| R72-1 | AVANCEMENT | VM → Mac | 2026-11-24 | §10 : deux codes 0 ; c4-chemins `écarts=15 / 165` (classes listées) ; c4-graine `écarts=2 / 244` (g1, r1-status), « location » des greffons en `ssh://` sur la VM | **non remis** (ECONNRESET ×2), consigné par la VM dans `~/env-72-journaux/0-messages-R72-1.md` ; contenu reçu par le message suivant |
| R72-1 | AVANCEMENT | VM → Mac | 2026-11-24 | §11.1 : fixtures 65, 60, 56 `écarts=0` ; fixture70 `écarts=2 / 202` (`k01-218.git-err`, `k01-250.git-err`) ; **D35 prouvé** (k01, k02, k03, k07, f05 : `fatal: Remote branch nope…`) ; g04, g06, g11, g13, g21 code 1 ; §11.2 : `fatal⍽: La branche distante nope…`, code 2, `depots` vide ; pytest lancé 15:53 UTC ; §11.4 étape 1 demandée à l'utilisateur | reçu |
| R72-1 | RÉPONSE | Mac → VM | 2026-11-24 | relais du §10 inutile ; 15 = 13 de la copie distincte + 2 de l'hôte ; « location » = URL déclarée par la graine `env11` de `$C5` (classe « graine », non détaillée par la consigne : défaut D38 (3)), admis si g1, r1 ne diffèrent que par commits, configurations et « location » ; relever `.scion.sources.list` | accepté par le serveur |
| R72-1 | AVANCEMENT | VM → Mac | 2026-11-24 | §11.3 pytest 616 passed (178,9 s), modules = Mac ; §11.4 T3 : « Observation de 5 » puis « de 6 » après `seed add` au terminal (16:34:41 UTC) ; suppression du clone (16:37:30) : aucune notification vue ; hypothèse inotify | reçu |
| R72-1 | AVANCEMENT | VM → Mac | 2026-11-24 | correction : une seule notification « Clone de library-env72lib supprimé hors de lepton… », trouvée par l'utilisateur dans le centre de notifications (non affichée en surimpression) ; T3 conforme ; hypothèse retirée ; §12.1 lancé sur `devenv/env-72-debian` | reçu |
| R72-1 | AVANCEMENT | VM → Mac | 2026-11-24 | §12 conforme : `rejouer-oracle` code 0 au premier passage (variable du profil) ; host 7/7 ; 16 presets ; banc 20/20, 16/16, 19/19 ×2, `peripheriques` ×4 ; mklepton = R66-1 = `env-52-apres` ; `comparer_R66-1` 0 et `hors_debug=0` ×16 ; `mirror-sync --dry-run` 8 × 0 référence, 0 signalement ; rédaction du rapport | reçu |
| R72-1 | QUESTION | VM → Mac | 2026-11-24 | rapport commité 9869e39 sur `devenv/env-72-debian` (depuis 5411f78 : rapport, pièces, oracle) ; C1-C7 atteints, C8 écarté, C9 après le push ; accord de push demandé à l'utilisateur dans la session VM | reçu |
| R72-1 | AVANCEMENT | VM → Mac | 2026-11-24 | push annoncé « À CONFIRMER », accord de l'utilisateur dans la session VM | reçu |
| R72-1 | FIN-SUCCÈS | VM → Mac | 2026-11-24 | C1-C7 atteints, C8 écarté, C9 fait ; `devenv/env-72-debian` 9869e39 poussée (16:49:10 UTC, invite confirmée) ; 8 écarts et constats ; 1 message non remis (§10) | reçu |

§0 (utilisateur) : `LEPTON_EMBOS_ROOT` absente au premier essai (l'`export` n'avait été tapé que
dans un terminal) ; ligne ajoutée à la fin de `~/.bashrc` (shell `/bin/bash`, pas de
`~/.bash_profile`), vérifiée dans un nouveau terminal ; session VM ouverte depuis ce terminal
(confirmé par l'utilisateur avant l'envoi de l'ordre).

Défaut de la consigne relevé par l'ACCUSÉ : §5 et §8.2 donnaient `~/env-66-journaux` et
`~/tmp-pytest/env-66` présents, et le §14 les supprimait. Ils avaient été supprimés par `R66-2`
(`handoff/env-66.md` l. 38 ; le fichier d'étape disait « `~/tmp-pytest` vide »). Décision de
l'utilisateur (2026-11-24, pendant R72-1) : liste du §14 réduite à `env-72-essai`,
`env-72-fixture`, `~/tmp-pytest/env-72-enveloppe`, transmise à la VM ; la consigne versionnée n'est
pas modifiée en cours d'ordre.

Second défaut de la consigne (QUESTION au §9) : le §9 attendait `écarts=0 / 1` sur le résumé de
`graft-update` sans lister la variante « point de montage » de git (D34, `/home` distinct sur la
VM), alors que le fichier d'étape la donne pour « écart admis à la main ». Réponse de la session
Mac fondée sur cette décision existante (PA-120) ; l'utilisateur en est informé.

Troisième défaut de la consigne (§10, AVANCEMENT non remis puis résumé) : la classe « graine
`env11` » ne citait que le commit et les presets ; sur la VM, `g1-status.out` et `r1-status.out`
portent aussi les URL déclarées par la graine de `$C5` (`ssh://git@github.com/…`, contre
`https://…` au Mac). La copie distincte du Mac gardait les URL d'`essais/env-11/qemu` : le
contrôle D38 (3) ne pouvait pas la faire paraître, faute d'en avoir changé aussi les URL.
