# ENV-72 — Validation Debian groupée (ENV-67 à ENV-71) — 2026-11-24

Session VM `debian-linux-vm` (`[1ceb82]`). Ordre `R72-1`, envoyé par la session Mac
`validation-debian-env-72` (nom affiché « Session ENV-72 (handoff ENV-71) », bridge
`bridge:session_01FkeafybTFNebrVA241sNtN`).

- **Consigne** : `doc/devenv/consignes/env-72-debian.md` à 5411f78, sha256 `5556a024…0f36`,
  égal à l'ordre (800 lignes, lue en entier) ; protocole ORCHESTRATION §2bis.
- **Session** : répertoire de travail `/home/lepton-user/lepton-tools-dev/lepton-tools` (`$T`),
  mode auto, Remote Control. Journaux dans `~/env-72-journaux/` (`$J`). Heures en UTC.
- **Rootstocks regreffés** : `essais/env-28-debian` (`$U`), `essais/env-13-debian` (`$E13`),
  `essais/env-53-c5` (`$C5`), `essais/env-53-debian` (`$R53`).
- **Copies d'essai et fixtures** : `essais/env-72-essai` (`$W` : `c4/rs`, `c6/gen`, `depot72`,
  `seed-scions`) et `essais/env-72-fixture` (`$FX`).

**Résultat.** C1 à C7 sont atteints. Les écarts sont tous expliqués ; deux classes ont été admises en cours de session. C8 est écarté
(PA-131). C9 est fait après le commit du rapport, sous la liste corrigée par l'utilisateur (§8 ci-dessous).

Principaux écarts :
- **§5 / §8.2 / §14** : `~/env-66-journaux` et `~/tmp-pytest/env-66` sont absents. R66-2 les a supprimés,
  et la consigne les donnait encore présents. C'est un défaut de la consigne. La liste du §14 a été corrigée par décision de l'utilisateur,
  transmise par la session Mac.
- **A1** (§8.3) : la première invite a été acceptée au lieu d'être refusée (sans effet : cible
  absente) ; relancée sur décision de l'utilisateur, la seconde a été refusée (`rejet-invite`).
- **C3** (§9) : pour `$U`, `$E13` et `$R53`, le résumé du `graft-update` diffère du Mac d'une ligne. git y écrit sa variante
  « point de montage » (D34, hors plan). La consigne ne listait pas cette classe. L'écart est admis.
- **C4** (§10) : un écart de `c4-graine` sort des classes listées. Le champ `location` est en `ssh://…`,
  parce que la graine `env11` de `$C5` déclare ses sources en ssh. La session Mac l'a classé « graine env11 » (défaut de la
  consigne, D38 (3)).
- **C6** (§11.4) : la notification de D36 est émise, mais elle n'est visible que dans le centre de
  notifications de VSCodium. Elle ne s'est pas affichée en surimpression.

## 1. Hôte, versions et session (§5, §6)

| Élément | Relevé |
| --- | --- |
| Hôte | Linux x86_64, Debian 13.7, noyau 6.12.107+deb13-amd64, utilisateur `lepton-user` |
| Claude Code | journal de session : `"version":"2.1.331"` (seule version) ; `claude --version` 2.1.331 |
| `CLAUDE_PROJECT_DIR` | vide dans Bash |
| lepton-tools | propre, `devenv/env-72`, 5411f78, à jour avec `origin/devenv/env-72` |
| `.claude/settings.json` | `b01ad557…d235` (= Mac) |
| `proteger-trunk.py` | `04572df6…6909` (= Mac) |
| `supprimer-essai.sh` | `369dae36…b9c8` (= Mac) |
| `comparer-releves.py` | `2bd102cd…5d8c` (= Mac) |
| `settings.local.json` | absent (utilisateur et dépôt) |
| `git ls-remote` | « têtes publiées = Mac » (24 lignes ; `lepton-tools main 8cbbf25`) |
| git | 2.47.3 |
| scion | 0.6.3.3 avant ; **0.6.3.4** après `install-debian.sh` (code 0, `git+…seed.scions.git@0.6.3.4`) ; `0.6.3.4 True` (`gitops.cause`) |
| lepton | `pipx install --force` : `installed package lepton 0.1.0` ; `lepton 0.1.0`, `scion 0.6.3.4 (requis ≥ 0.6.2.0)` ; 18 modules = dépôt |
| clone noyau `$K` | 2b4a647 → **0c2e43e** (ff-only), propre ; `SCION_REF="${SCION_REF:-0.6.3.4}"` |
| extension | `install-vscodium.sh` code 0 : `lepton-distribution.lepton : 0.5.3 → 0.5.4`, `changements 1` ; `lepton-0.5.4.vsix` `31678dd3…b8d1` |
| extensions VSCodium | `lepton@0.5.4`, `vscode-lldb@1.12.3`, `rtos-views@0.0.16`, `peripheral-viewer@1.6.4` ; `batch.js` présent ; `watch.js` : 2 × `scion.grafted.list` |
| Chaîne | arm-none-eabi-gcc 14.2.1, cmake 3.31.6, ninja 1.12.1, QEMU 10.0.13, Python 3.13.5, codium 1.135.06055 |
| Outils | `shasum`, `realpath`, `tar`, `clangd` (/usr/bin) présents ; `node`, `rsync`, `zsh` absents |
| Espace | `/home` 18 G libres, `/tmp` 689 M |

Constat : le répertoire `~/.vscode-oss/extensions/lepton-distribution.lepton-0.5.3` reste après
l'installation de 0.5.4. VSCodium nettoie d'ordinaire ces répertoires à son lancement.

### Variables d'environnement (D38 (1)) — `env-72-debian/5-variables.txt`

```
LEPTON_EMBOS_ROOT=/home/lepton-user/lepton/third_party/embos/cortexm-gcc/5.20.0.0
SCION_REF absente
SCION_SPEC absente
LEPTON_CLONE absente
XDG_CONFIG_HOME absente
NM absente
SIZE absente
LANG=fr_FR.UTF-8
LC_ALL absente
```
`Start/Inc/RTOS.h` est présent sous `LEPTON_EMBOS_ROOT` ; `locale` donne `LC_CTYPE="fr_FR.UTF-8"`. Tout est conforme à
l'attendu.

### Clones et graines avant regreffe (§5)

- `$U`, `$E13` et `$R53`, chacun :
  - 23 entrées ;
  - graine `depots/lepton-seed.scions/original-tree` sur `original-tree`, 15740f9, amont
    `origin/original-tree`, `modifs=0` ;
  - 13 clones `<clé>/master` sur `master`, amont réglé, `modifs=0`, noyau 2b4a647 ;
  - `liens=3889 casses=0 reguliers=0` ; 8 clones tiers.
  - Le répertoire `depots/tiers` occupe 108 760 Ko (`$U`, `$E13`) et 87 512 Ko (`$R53`).
- `$C5` :
  - 5 entrées ;
  - graine locale `depots/lepton-seed/env11` sur `master`, 6d3d2a5, sans amont, `modifs=0` ;
  - `salut` sur `master` 71e1641, sans amont, `modifs=2` ; noyau 2b4a647 ;
  - `liens=3059 casses=0 reguliers=0` ; 2 clones tiers F7.

## 2. Critères (§15)

| Critère | Résultat |
| --- | --- |
| C1 Versions, variables | **Atteint.** ls-remote = Mac ; settings, hook, enveloppe, outil de comparaison = Mac ; Claude Code 2.1.331 ; variables = attendu ; git 2.47.3 ; scion 0.6.3.4, `gitops.cause` ; lepton 18 modules = dépôt ; extension 0.5.3 → 0.5.4 |
| C2 Règles, enveloppe, hook | **Atteint, avec un écart corrigé.** Réglages relus, 2 règles ; U1, U2 sans effet ; R1, R2 code 2, E1 code 0 (voisin gardé) ; H1 hook ; `pipx install --force` par la règle du dépôt ; 4 `graft-update` confirmés ; `git clone`, pytest par la règle. A1 : 1ʳᵉ invite acceptée par erreur (sans effet), 2ᵉ refusée |
| C3 Regreffes | **Atteint, avec un écart admis (D34).** 4 × code 0, seul le noyau avance (2b4a647 → 0c2e43e), aucun clone ; liens inchangés (3889 ; 3059 pour `$C5`) ; `CONFORME` ; tiers 0 / 16 (0 / 4) ; `clones = Mac` ; `check` 0 ; espace = avant. Résumé `cmp_mac` : `écarts=1 / 1` ×3, variante « point de montage » seule |
| C4 D29, D30, D32, D37 | **Atteint.** Deux `code=0` ; `écarts=15 / 165` et `2 / 244`, toutes les différences sont dans des classes admises (dont « graine env11 » élargie à `location`) ; colonnes 1-6 de `resume.tsv` = Mac ; liens de `c4/rs` = 3059 |
| C5 D35, D33, pytest | **Atteint.** Fixtures 65, 60, 56 `écarts=0` ; fixture70 `écarts=2 / 202` (`k01-218`, `k01-250`) ; k01, k02, k03, k07, f05 : la cause `fatal: Remote branch nope not found…` ; g04, g06, g11, g13, g21 code 1 ; cause en français (§11.2) ; pytest 616 passed |
| C6 D36 | **Atteint.** 0.5.4 installée ; « Observation de 5 » → « de 6 » après `seed add` au terminal ; une seule notification après la suppression du clone (dans le centre de notifications) |
| C7 Constructions, miroir | **Atteint.** Premier passage code 0 ; host 7/7 ; 16 presets ; banc 20/20, 16/16, 19/19, `peripheriques` ×4 ; mklepton = R66-1 = env-52-apres ; `comparer_R66-1` 0 ×16 ; `mirror-sync --dry-run` code 0, 8 × 0 à envoyer, 0 signalement |
| C8 Cartes | écarté (PA-131) |
| C9 Nettoyage | voir §8 |

## 3. Règles de permission (C2, §8)

### 3.1 `~/.claude/settings.json` (§8.1)

Sortie de `python3 -m json.tool` : `env-72-debian/settings-utilisateur.json`, identique à
`rapports/env-66-debian/settings-utilisateur.json`. Le bloc `permissions` contient seulement :
```json
"allow": [
    "Bash(pipx install:*)",
    "Bash(git clone * https://github.com/lepton-distribution/*)"
]
```
Il n'y a ni `ask`, ni `deny`, ni `defaultMode`. Les autres clés (`model`, `modelSettings`, `tui`, `theme`,
`agentPushNotifEnabled`, `autoMode`) sont inchangées depuis ENV-66.

### 3.2 Décisions (`env-72-debian/15-decisions.tsv`, 72 lignes)

| Heure | N° | Commande | Décision | Effet |
| --- | --- | --- | --- | --- |
| 15:25:15 | §6.2 | `pipx install --force ~/lepton-tools-dev/lepton-tools` | `accept config rule projectSettings` | lepton 0.1.0 installé |
| 15:26:40 | U1 | `pipx install ~/lepton-tools-dev/essais/env-72-absent` | `accept config subcommandResults` | code 1 (« Unable to parse package spec ») |
| 15:26:45 | U2 | `git clone --depth 1 https://github.com/lepton-distribution/env-72-absent.git …` | `accept config subcommandResults` | code 128 (« could not read Username »), cible absente |
| 15:26:56 | R1 | `scripts/supprimer-essai.sh ~/tmp-pytest/env-72-enveloppe/..` | `accept config subcommandResults` | code 2, « non résoluble », rien supprimé |
| 15:26:59 | R2 | `scripts/supprimer-essai.sh ~/tmp-pytest/../lepton-tools-dev` | `accept config subcommandResults` | code 2, « hors des bornes », rien supprimé |
| 15:27:08 | E1 | `scripts/supprimer-essai.sh ~/tmp-pytest/env-72-enveloppe/sous` | `accept config subcommandResults` | code 0, `sous/` supprimé, `g` gardé |
| 15:29:07 | A1 | `scion graft-update -v ~/lepton-tools-dev/essais/env-72-absent` | `accept user_temporary projectSettings` | **invite acceptée par erreur** ; code 1, « n'est pas un rootstock », sans effet |
| 15:30:15 | A1 bis | même commande | `rejet-invite` | refusée |
| 15:34:30 | H1 | `touch ~/lepton-tools-dev/essais/env-72-essai/c6/gen/trunk/essai-hook` | `reject hook hook` | refus sans invite |
| 15:35:21 | §9 | `scion graft-update -v …/env-28-debian > … ; echo …` | `accept user_temporary projectSettings` | code 0 |
| 15:37:07 | §9 | `scion graft-update -v …/env-13-debian …` | `accept user_temporary projectSettings` | code 0 |
| 15:39:06 | §9 | `scion graft-update -v …/env-53-c5 …` | `accept user_temporary projectSettings` | code 0 |
| 15:40:09 | §9 | `scion graft-update -v …/env-53-debian …` | `accept user_temporary projectSettings` | code 0 |
| 15:50:32 | §11.1 | `git clone https://github.com/lepton-distribution/seed.scions.git …/seed-scions` | `accept config subcommandResults` | clone fait |
| 15:52:21 | §11.3 | `~/lepton-tools-dev/venv-test/bin/pytest -q -rs …` | `accept config subcommandResults` | 616 passed |
| 16:37:23 | §11.4 | `scripts/supprimer-essai.sh …/c6/gen/depots/lepton/library-env72lib/master` | `accept config subcommandResults` | supprimé |
| — | §15 | `git push origin devenv/env-72-debian` | voir §10 | — |

Heures des annonces (`SendMessage`) et des lancements qui les suivent :
- A1 « À REFUSER » à 15:27:22, lancement à 15:29:07 ;
- A1 bis « À REFUSER » à 15:30:08, lancement à 15:30:15 ;
- « À CONFIRMER » à 15:34:54, 15:36:38, 15:37:41 et 15:39:34, lancements à 15:35:21, 15:37:07, 15:39:06 et 15:40:09.

Au premier lancement d'A1, l'invite est apparue et a reçu « Oui ». Les deux décisions sont consignées. Sur décision de
l'utilisateur dans la session VM (« relance A1, je refuserai l'invite »), A1 a été relancé après une
nouvelle annonce, et l'invite a été refusée. Même scénario qu'en R66-1.

Hors règle, au classifieur, toutes acceptées (55 décisions `classifier`) : `install-debian.sh`,
`install-vscodium.sh`, préparation du §8.2 (`mkdir … && touch … && find`), `chemins.sh`, `graine.sh`,
fixtures, `seed-add` du §11.2, `lepton seed add` du §11.4, `rejouer-oracle.sh`,
`mirror-sync --dry-run`, relevés. Aucun refus du classifieur.

U1 et U2 sont jugés par `subcommandResults` : `decisions.py` ne nomme pas la règle, utilisateur
ou dépôt, dans ce cas. Aucun n'est passé au classifieur.

Après H1 : `env-72-absent` absent ; `essai-hook` absent ; 0 paquet `env-72` ; « liens de c6 =
départ ». Après E1 : `env-72-enveloppe` et `g` seuls. `~/tmp-pytest/env-66` est absent, ce qui est l'attendu corrigé (§9,
écart 1) ; `~/lepton-tools-dev` est présent.

## 4. Regreffes (C3, §9)

| Rootstock | Graine avant | `graft-update` | Avancé | Liens | Contrôle | Tiers | `check` / espace | Résumé `cmp_mac` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `env-28-debian` | `original-tree` 15740f9 | code 0 ; clone 0 ; conflit 0 | noyau 2b4a647 → 0c2e43e | 3889 → 3889 (+0 −0) | `CONFORME` (avant et R50-1) | 8, 0 / 16, `clones = Mac` | 0 / diff 0 | `écarts=1 / 1` (D34) |
| `env-13-debian` | `original-tree` 15740f9 | code 0 ; clone 0 ; conflit 0 | noyau 2b4a647 → 0c2e43e | 3889 → 3889 | `CONFORME` (avant et R50-1) | 8, 0 / 16, `clones = Mac` | 0 / diff 0 | `écarts=1 / 1` (D34) |
| `env-53-c5` | `env11` locale, `master` 6d3d2a5, « sans amont, laissée telle quelle » | code 0 ; clone 0 ; conflit 0 | noyau 2b4a647 → 0c2e43e ; `salut` accepté (`modifs=2`) | 3059 → 3059 | `CONFORME` (avant) | 2 (F7), 0 / 4 | 0 / diff 0 | — |
| `env-53-debian` | `original-tree` 15740f9 | code 0 ; clone 0 ; conflit 0 | noyau 2b4a647 → 0c2e43e | 3889 → 3889 | `CONFORME` (avant et R50-1) | 8, 0 / 16, `clones = Mac` | 0 / diff 0 | `écarts=1 / 1` (D34) |

Aucun refus de scion (D33 : graine à sa version). « 3889 feuilles liées » (3059 pour `$C5`) ; aucune
ligne `.DS_Store` ; trunk sans fichier régulier ni lien cassé. Bilans : `env-72-debian/<nom>-bilan.txt` ;
journaux : `<nom>-graft-update.log` ; clones tiers : `<nom>-tiers-apres/clones.txt`. `ignorecase` est
vide sur la VM (normalisé dans la comparaison, comme les tailles `ko_hors_git`/`ko_git`).

Diff du résumé, identique pour les trois rootstocks de la graine `original-tree`
(`env-72-debian/9-resume-<nom>-cmp.txt`) :
```
-fatal: not a git repository (or any of the parent directories): .git
+fatal: ni ceci ni aucun de ses répertoires parents (jusqu'au point de montage /) n'est un dépôt git
+Arrêt à la limite du système de fichiers (GIT_DISCOVERY_ACROSS_FILESYSTEM n'est pas défini).
```
Le résumé compte 84 lignes, contre 83 au Mac.

**Cause** : `/home` est un système de fichiers distinct sur la VM. git choisit donc la variante
« or any parent up to mount point » (`po/fr.po` v2.47.3 l. 21981-21988). Cette variante est absente de
`TRADUCTIONS`.

**Décision** (RÉPONSE de la session Mac, 15:36) : option (a). D34 est hors plan (PA-120,
`HORS-PLAN.md` l. 95). Le fichier d'étape porte : « La variante « point de montage » (D34, hors plan)
reste un écart admis à la main. » La règle appliquée admet `écarts=1 / 1` seulement si le diff se limite à ces
lignes ; c'est le cas pour les trois rootstocks. La consigne ne listait pas cette classe au §9 :
c'est un défaut de la consigne.

## 5. D29, D30, D32, D37 (C4, §10)

`chemins.sh` : `code=0`, 165 relevés. `graine.sh` : `code=0`, 244 relevés. Les deux scripts sont passés par le classifieur, sans refus.
`resume.tsv` colonnes 1 à 6 = Mac. Liens de `c4/rs` : `liens=3059 casses=0 reguliers=0`. Racine de
`c4/rs` : `depots`, `env11.code-workspace`, `.scion.rootstock.signature`, `trunk` ; 0 `.DS_Store`.

### 5.1 `c4-chemins` : `écarts=15 / 165` (`env-72-debian/10-c4-chemins-cmp.txt`)

Le Mac attend 13 écarts sur sa copie distincte, plus 2 de la classe hôte.

| Fichier | Classe |
| --- | --- |
| `p6-n.cmd`, `p6-n.clangd` | hôte : `clangd`, `/usr/bin/clangd` contre `clangd-mp-21`, `/opt/local/bin/clangd-mp-21` |
| `resume.tsv` | longueur des chemins : colonne 7 tronquée (`m1-h`, `m1-th`, `p6-*`) ; colonnes 1-6 = Mac |
| `n1-a.err`, `n1-d.err`, `n1-r.err`, `n1-t.err`, `n1-u.err` | fichiers ignorés du Mac : ligne « 13 chemin(s) ignoré(s) par git » absente |
| `p6-a.out`, `p6-n.out`, `p6-r.out`, `p6-rd.out`, `p6-rs.out`, `p6-rw.out`, `p6-t.out` | graine `env11` : `presets : env11-debug-qemu` seul |

D29 : `check FILE`, `seed mkconf import` et `seed new --mkconf` en `~/…` et `~<U>/…` acceptés (code 0) ;
`~inconnu68/…` refusé par lepton (`n1-x`, code 1, « répertoire personnel … introuvable »). D30 :
`p6-r`, `p6-rs`, `p6-rw`, `p6-rd` donnent un `clangd.path` absolu. Ce sont les mêmes fichiers que chez le Mac, hors classes.

### 5.2 `c4-graine` : `écarts=2 / 244` (`env-72-debian/10-c4-graine-cmp.txt`)

`g1-status.out` et `r1-status.out` diffèrent du Mac sur les points suivants :
- graine et projet : `branch` `main` → `master`, `commit` `124db52` → `6d3d2a5` (graine `env11`) ;
- configuration `release-qemu` absente (graine `env11`) ;
- `r1` : commit de `library-env68lib` `f6aed02` → `98ec8ea` (commits locaux) ;
- `location` des greffons noyau, `family-qemu-mps2` et `bsp-qemu-mps2-an386` :
  `https://github.com/lepton-distribution/<dépôt>.git` au Mac,
  `ssh://git@github.com/lepton-distribution/<dépôt>.git` sur la VM.

Le champ `location` ne figurait dans aucune classe de la consigne. La session Mac l'a classé (RÉPONSE de 15:53) : `location` est l'URL que la graine
déclare, pas l'origine du clone. Celle de `$C5` (`env-72-debian/10-sources-list-c5.txt`) :
```
4:lepton	original::tree	master	ssh://git@github.com/lepton-distribution/lepton-original-tree.scions.git
5:lepton	family-qemu-mps2	master	ssh://git@github.com/lepton-distribution/lepton-famille-qemu-mps2.git
6:lepton	bsp-qemu-mps2-an386	master	ssh://git@github.com/lepton-distribution/lepton-bsp-qemu-mps2-an386.git
```
Classe « graine env11 », que la consigne n'a pas détaillée : c'est un défaut de la consigne (D38 (3)). Condition
vérifiée : g1 et r1 ne diffèrent que par les commits, les configurations et les `location`. Les 83 autres fichiers `g1-*`/`r1-*` (codes, `.vs-depart`, `.vs-ajoute`) sont
identiques. D32 (r1, r2, r5 `--purge` refusés, code 2) et D37 (g1 à g5) : mêmes résultats que chez le Mac.

## 6. D35, D33 et pytest (C5, §11)

### 6.1 Fixtures (§11.1)

`seed-scions` est à 473b653 (tag 0.6.3.4) et propre. Quatre `code=0`.

| Fixture | `cmp_mac` |
| --- | --- |
| fixture70 | `écarts=2 / 202` : `k01-218.git-err`, `k01-250.git-err` seuls |
| fixture65 | `écarts=0 / 284` |
| fixture60 | `écarts=0 / 179` |
| fixture56 | `écarts=0 / 76` |

Sur la VM, `k01-218.git-err` et `k01-250.git-err` sont identiques, tous deux produits par `/usr/bin/git` 2.47.3 :
```
$ /usr/bin/git clone -b nope --quiet --single-branch file://localhost<B>/repos/plain d
code 128
warning: Could not find remote branch nope to clone.
fatal: Remote branch nope not found in upstream origin
```

D35, preuve (`cat -v`) : `k01.err`, `k02.err`, `k03.err` (fixture70), `k07.err` (fixture60) et
`f05.err` (fixture56) se terminent tous par
`(code 128) : fatal: Remote branch nope not found in upstream origin`. Ils portent donc la cause, et non l'avertissement
relevé en R66-1.

D33 : g04, g06, g11, g13 et g21 donnent le code 1 ; g01 à g21 sont identiques au Mac.

### 6.2 D35 en français (§11.2) — `env-72-debian/11-d35-fr.log`

```
erreur : M-CM-)chec de M-BM-+ git clone -b nope --quiet --single-branch file://localhost/home/lepton-user/lepton-tools-dev/essais/env-72-fixture/f70/repos/plain /home/lepton-user/lepton-tools-dev/essais/env-72-fixture/f70/k03/rootstock/depots/own/plain/nope M-BM-; (code 128) : fatalM-BM- : La branche distante nope n'a pas M-CM-)tM-CM-) trouvM-CM-)e dans le dM-CM-)pM-CM-4t amont origin
code=2
```
La cause s'affiche en français (`fatal⍽: La branche distante nope n'a pas été trouvée dans le dépôt amont
origin`), et non l'avertissement. `depots` : 0 entrée, inchangé.

### 6.3 pytest (§11.3) — `env-72-debian/11-pytest.xml`

`{'tests': '616', 'failures': '0', 'errors': '0', 'skipped': '0', 'time': '178.880'}` :
**616 passed** en 2 min 59.

| Module | Tests |
| --- | --- |
| `test_proteger_trunk` | 118 |
| `test_garde_ask` | 46 |
| `test_supprimer_essai` | 70 |
| `test_milestone3` | 62 |
| `test_comparer_releves` | 13 |

lepton est en mode éditable depuis `$T` (`Editable project location`), et lepton-tools est propre. Pendant ce
temps, le T3 du §11.4 s'est déroulé en concurrence.

## 7. D36 : extension 0.5.4 (C6, §11.4)

Le T3 a été fait sur `$W/c6/gen`, dans VSCodium sur la VM, par l'utilisateur (inotify).

| Étape | Relevé |
| --- | --- |
| Ouverture | canal « Lepton » : « Observation de 5 greffon(s) et du trunk …/c6/gen/trunk » |
| 16:34:41, `lepton seed add env72lib "file://localhost$D72@master" …` au terminal | code 0 ; `liens=3062 casses=0 reguliers=0` ; canal : `lepton seed status --json → code 0`, puis « Observation de **6** greffon(s) … » |
| 16:37:30, `supprimer-essai.sh …/library-env72lib/master` | supprimé ; `liens=3062 casses=3` ; canal : `lepton seed status --json → code 1` |
| Notification | une seule, « Clone de library-env72lib supprimé hors de lepton : ses liens du trunk sont cassés (lepton seed status) » |

Le défaut de 0.5.3 est corrigé : un greffon ajouté au terminal entre dans la liste observée, et la
suppression de son clone est signalée.

Constats :
- La notification ne s'est pas affichée en surimpression : l'utilisateur l'a trouvée dans le
  centre de notifications (cloche de la barre d'état). Un AVANCEMENT envoyé à 16:39 la donnait d'abord absente, et il a été corrigé
  à 16:41.
- À l'ouverture, le canal affichait « clangd relancé quand
  …/essais/env-53-c5/build/.active/compile_commands.json change ». `env11.code-workspace` a été
  copié de `$C5` par `tar` avec son chemin absolu, et il désigne donc toujours `$C5`. C'est sans effet sur T3.

## 8. Presets et miroir (C7, §12)

### 8.1 Reconstructions (§12.1)

`git switch -c devenv/env-72-debian devenv/env-72`, puis `rejouer-oracle.sh` dans `$R53` regreffé :
« rejouer-oracle: tout a réussi », `code=0` **au premier passage**. `LEPTON_EMBOS_ROOT` venait du
profil (D38 (1)). Journal : `env-72-debian/12-rejouer.log`. Oracle : `rapports/oracles/env-72-debian/`
(2,8 Mo).

| Preset | Construction | Fumée / banc KAL | `comparer_R66-1` | `comparer_Mac` |
| --- | --- | --- | --- | --- |
| host | ctest 7/7 | — | mklepton = R66-1 | mklepton = env-52-apres |
| qemu-mps2-an386-embos | oui | 20/20, `peripheriques` Passed | 0 | 1 |
| qemu-mps2-an386-embos-soft | oui | 16/16, `peripheriques` Passed | 0 | 1 |
| qemu-mps2-an386-freertos | oui | 20/20, `peripheriques` Passed | 0 | 1 |
| qemu-mps2-an386-freertos-soft | oui | 16/16, `peripheriques` Passed | 0 | 1 |
| qemu-mps2-an500-embos | oui | 19/19 | 0 | 1 |
| qemu-mps2-an500-freertos | oui | 19/19 | 0 | 1 |
| nucleo-f429zi-embos / -freertos | oui (1768 / 1804 symboles) | — | 0 / 0 | 1 / 1 |
| nucleo-f439zi-embos / -freertos | oui (1768 / 1804) | — | 0 / 0 | 1 / 1 |
| nucleo-wl55jc1-embos / -freertos | oui (1229 / 1275) | — | 0 / 0 | 1 / 1 |
| samd21-xplained-pro-embos / -freertos | oui (941 / 991) | — | 0 / 0 | 1 / 1 |
| stm32f746g-disco-embos / -freertos | oui (1640 / 1676) | — | 0 / 0 | 1 / 1 |

`hors_debug=0` pour les 16 presets (`env-72-debian/12-bilan.txt`) : aucun binaire n'a changé depuis R66-1.
`comparer_Mac` donne 1 partout, ce qui est attendu (chaînes différentes, informatif). Le trunk de `$R53` est à `liens=3889 casses=0
reguliers=0`, avec 0 `__pycache__`. Aucun flash, aucune commande OpenOCD.

### 8.2 Commande de miroir (§12.3) — `env-72-debian/12-mirror-sync.log`

`scion mirror-sync --dry-run -v …/env-53-debian` : `code=0`. Chacun des 8 miroirs suivants donne
`0 référence(s) à envoyer, 0 signalement(s)` : `mirror-stm32f4xx-hal-driver`, `mirror-cmsis_device_f4`,
`mirror-stm32wlxx-hal-driver`, `mirror-cmsis-device-wl`, `mirror-stm32-mw-subghz-phy`,
`mirror-STM32CubeWL`, `mirror-stm32f7xx-hal-driver`, `mirror-cmsis_device_f7`. Le trunk de `$R53` est
`CONFORME` contre l'attendu de R50-1. Rien n'a été envoyé.

## 9. Nettoyage (C9, §14)

**Correction de la consigne** (RÉPONSE de la session Mac, 15:25, décision de l'utilisateur) : la consigne
donnait `~/env-66-journaux` et `~/tmp-pytest/env-66` présents. Ils ont été supprimés par R66-2, nettoyage final d'ENV-66, puis
`~/tmp-pytest` a été recréé vide (`handoff/env-66.md` l. 38). L'enveloppe procède en tout ou rien. Les deux cibles
sont donc retirées de la commande, qui devient :
```
scripts/supprimer-essai.sh ~/lepton-tools-dev/essais/env-72-essai ~/lepton-tools-dev/essais/env-72-fixture ~/tmp-pytest/env-72-enveloppe
```
Elle est lancée après le commit de ce rapport et le push. Son résultat figure dans le `FIN-*` de `R72-1`, il n'est pas commité.
Sont conservés : `$U`, `$E13`, `$C5`, `$R53`, `$J`, `~/tmp-pytest`, `~/tmp-pytest/env-72`.

## 10. Écarts et constats

1. **Cibles d'ENV-66 absentes (§5, §8.2, §14)** : `~/env-66-journaux` et `~/tmp-pytest/env-66` ont été supprimés
   par R66-2. C'est un défaut de la consigne, et le §14 a été corrigé par l'utilisateur.
2. **A1 accepté par erreur (§8.3)** : sans effet (cible absente). Sur décision de l'utilisateur, A1 a été relancé et
   l'invite refusée. Même scénario qu'en R66-1.
3. **Variante git « point de montage » (§9, D34)** : propre à l'hôte, puisque `/home` est un système de fichiers distinct. Elle manque dans
   `TRADUCTIONS`. Elle est admise selon la règle stricte du diff, et la classe manquait à la consigne.
4. **`location` en ssh dans `g1-status`/`r1-status` (§10)** : URL déclarée par la graine `env11` de
   `$C5`. L'écart a été classé « graine env11 » ; c'est un défaut de la consigne (D38 (3)).
5. **Notification D36 hors surimpression (§11.4)** : elle est visible seulement dans le centre de
   notifications. Le comportement attendu de l'extension est atteint.
6. **`env11.code-workspace` copié de `$C5`** : il désigne `…/env-53-c5/build/.active/compile_commands.json`
   (chemin absolu). Sans effet sur les essais.
7. **Répertoire de l'extension 0.5.3** : il reste dans `~/.vscode-oss/extensions/` après l'installation
   de 0.5.4.
8. **`CLAUDE_PROJECT_DIR`** : vide dans Bash (relevé informatif).

## 11. Journal des messages (§2bis)

| Heure | Type | Sens | Résumé | Remis |
| --- | --- | --- | --- | --- |
| 15:21:51 | (avis) | VM → Mac | session VM prête | oui (non confirmé) |
| 15:22:37 | ORDRE | Mac → VM | R72-1, consigne env-72-debian.md à 5411f78 | reçu |
| 15:24:21 | ACCUSÉ | VM → Mac | ordre reformulé, références, écart 1 (cibles d'ENV-66) | oui |
| 15:24:36 | AVANCEMENT | VM → Mac | §6 : lancement des installations | oui |
| 15:24:43 | RÉPONSE | Mac → VM | écart 1 : défaut de la consigne, poursuivre | reçu |
| 15:25:25 | RÉPONSE | Mac → VM | §14 corrigé par décision de l'utilisateur | reçu |
| 15:26:28 | AVANCEMENT | VM → Mac | §6 et §7 conformes | oui |
| 15:27:22 | AVANCEMENT | VM → Mac | À REFUSER A1 | oui |
| 15:29:25 | QUESTION | VM → Mac | A1 accepté par erreur | oui ; tranché par l'utilisateur dans la session VM |
| 15:30:08 | AVANCEMENT | VM → Mac | À REFUSER A1, relance | oui |
| 15:34:54 | AVANCEMENT | VM → Mac | §8 terminé ; À CONFIRMER env-28-debian | oui |
| 15:36:05 | QUESTION | VM → Mac | écart du résumé (point de montage) | oui |
| 15:36:23 | RÉPONSE | Mac → VM | option (a), D34 admis selon la règle stricte | reçu |
| 15:36:38 | AVANCEMENT | VM → Mac | À CONFIRMER env-13-debian | oui |
| 15:37:41 | AVANCEMENT | VM → Mac | À CONFIRMER env-53-c5 | oui |
| 15:39:34 | AVANCEMENT | VM → Mac | À CONFIRMER env-53-debian | oui |
| 15:40:30 | AVANCEMENT | VM → Mac | fin des invites de la VM jusqu'au push | oui |
| 15:50:29 | AVANCEMENT | VM → Mac | §10 terminé | **non remis** (ECONNRESET) |
| 15:50:43 | AVANCEMENT | VM → Mac | §10 terminé, renvoi à l'identique | **non remis** (ECONNRESET) ; texte : `env-72-debian/0-messages-R72-1.md` |
| 15:52:32 | AVANCEMENT | VM → Mac | §11.1, §11.2 conformes, avec le résumé du §10 | oui |
| 15:53:03 | RÉPONSE | Mac → VM | résumé du §10 reçu, relais inutile ; `location` classé | reçu |
| 16:39:25 | AVANCEMENT | VM → Mac | §11.4 : notification non vue (écart) | oui |
| 16:41:16 | AVANCEMENT | VM → Mac | §11 terminé : T3 conforme (correction) ; §12 lancé | oui |
| 16:45:34 | AVANCEMENT | VM → Mac | §12 conforme ; rédaction du rapport | oui |

« oui » signifie que le serveur a accepté le message ; la lecture n'est pas confirmée par cette voie. La QUESTION sur
A1 n'a pas reçu de RÉPONSE de la session Mac : l'utilisateur a tranché dans la session VM.

## 12. Non fait

- C8 (cartes) : écarté au PA-131 ; aucun flash, aucune commande OpenOCD.
- Aucune correction d'outil, de consigne ou d'extension : `TRADUCTIONS` n'a pas reçu la variante « point de
  montage » (D34, hors plan).
- Le résultat du nettoyage (§14) et celui du push figurent dans le `FIN-*` et ne sont pas commités.
