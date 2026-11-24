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
