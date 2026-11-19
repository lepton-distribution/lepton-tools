# ENV-66 — Validation Debian groupée (ENV-62 à ENV-65) — 2026-11-19

Session VM `debian-linux-vm`. Ordre `R66-1`, envoyé par la session Mac `validation-debian-env-66`
(nom affiché « ENV-66 avec la skill devenv-session », bridge
`bridge:session_01FkeafxujKcVVkjsmcjqygQ`).

- **Consigne** : `doc/devenv/consignes/env-66-debian.md` à 0eca739, sha256 `48eb3e5f…f561e`,
  égal à l'ordre (52 490 octets, lue en entier).
- **Session** : répertoire de travail `/home/lepton-user/lepton-tools-dev/lepton-tools` (`$T`),
  mode auto, Remote Control. Journaux dans `~/env-66-journaux/` (`$J`).
- **Rootstocks regreffés** : `essais/env-28-debian` (`$U`), `essais/env-13-debian` (`$E13`),
  `essais/env-53-c5` (`$C5`) et `essais/env-53-debian` (`$R53`).
- **Copies d'essai et fixtures** : `essais/env-66-essai` (`$W` : `c4/`, `c5/`, `depot65`,
  `seed-scions`) et `essais/env-66-fixture` (`$FX`).

**Résultat.** C1 à C7 sont atteints, avec des écarts tous expliqués. C8 est écarté (PA-119). C9
suit le commit de ce rapport. Les décisions de l'utilisateur sont citées à chaque écart (§9).
Principaux écarts :
- **A1** (§8) : la première invite a été acceptée au lieu d'être refusée. Elle est restée sans
  effet (cible absente). Le second essai a été refusé.
- **C3** (§9) : le résumé du `graft-update` diffère du Mac d'une ligne. git y écrit sa variante
  « point de montage », parce que `/home` est un système de fichiers distinct sur la VM. Écart
  admis pour cause d'hôte (décision de l'utilisateur).
- **C4** (§10) : `cmp_mac` donne 50 écarts sur 289. Ils se répartissent en 5 classes, toutes
  propres à l'hôte ou à la graine copiée : zsh absent, `.DS_Store` du Mac, graine `env11` de
  `$C5`, et les écarts admis par la consigne. D21 n'est pas mis en cause.
- **C5** (§11.2) : avec `seed-add --single-branch`, scion retient l'avertissement de git 2.47.3
  au lieu de la cause (k07, f05). C'est un défaut de scion, à présenter au hors-plan. Les
  fixtures fixent `LC_ALL=C` : les lignes de git en français ont été relevées à part.
- **C6** (§11.4) : le premier T3 n'est pas probant. Le greffon avait été ajouté au terminal, et
  l'extension ne l'observait pas. Le rejeu sur `c5/rs` (option (c)) est conforme.
- **C7** (§12) : au premier passage, les 8 presets embOS échouent, car `LEPTON_EMBOS_ROOT` est
  absente de l'environnement de la session. Le rejeu avec la variable est entièrement conforme.

## 1. Hôte, versions et session (§5, §6)

| Élément | Valeur |
| --- | --- |
| Hôte | Debian 13.7, Linux 6.12.107+deb13-amd64 x86_64, `lepton-user`, git 2.47.3 |
| Espace libre | `/home` 17 Go (système de fichiers distinct : `/dev/mapper/debian--linux--vm--vg-home`) ; `/tmp` 690 Mo |
| Claude Code | 2.1.328 (journal : 51 × `"version":"2.1.328"` ; R61-1 : 2.1.326). Session `a0115cd5-…`, première entrée 2026-11-19T18:59:38Z (19:59:38 +0100), après `0-settings-apres.txt` (19:58:25 +0100) : ouverte après le §0. `CLAUDE_PROJECT_DIR` vide dans l'environnement Bash |
| Réglages du dépôt | `.claude/settings.json` b01ad557…d235, `proteger-trunk.py` 04572df6…6909, `supprimer-essai.sh` 04323a00…0e15, `comparer-releves.py` 2bd102cd…5d8c : = Mac. Aucun `settings.local.json` (ni utilisateur, ni dépôt) |
| Réglages utilisateur | `~/.claude/settings.json`, 3876 o, mtime 19:59 (après `0-settings-apres.txt`, contenu identique : diff vide ; probablement la commande `/model` au démarrage) ; bloc `permissions.allow` = 2 règles (§3.1) |
| Têtes publiées | `bash $X/ls-remote.sh` : « têtes publiées = Mac » (24 lignes ; `lepton-tools main 6bc05ad`) |
| Chaîne APT | arm-none-eabi-gcc `15:14.2.rel1-1` (14.2.1 20241119), cmake 3.31.6, ninja 1.12.1, QEMU 10.0.13 (`1:10.0.13+ds-0+deb13u1`), Python 3.13.5 : = R61-1 |
| Outils | `shasum`, `realpath`, `tar`, `/usr/bin/clangd` présents ; `node` absent ; `rsync` absent ; `zsh` absent ; `/usr/share/codium/codium` présent ; `~/tmp-pytest` et `venv-test/bin/pytest` présents ; `id inconnu63` : utilisateur inexistant |
| embOS | `~/lepton/third_party/embos/cortexm-gcc/5.20.0.0` (`Start/Inc/RTOS.h` présent) ; `LEPTON_EMBOS_ROOT` absente de l'environnement de la session (§7, écart 7) |
| Clone noyau `$K` | propre, `master` dfc960b → **2b4a647** (avance rapide, 5 fichiers hors `scion/`) ; `SCION_REF="${SCION_REF:-0.6.3.3}"` |
| lepton-tools | `devenv/env-66` = `origin/devenv/env-66` = 0eca739, propre ; `SCION_REF="0.6.3.3"` (`install-vscodium.sh`) ; `SCION_MIN_VERSION = (0, 6, 2, 0)` ; `extension/dist/` : `lepton-0.5.3.vsix` seul |
| scion | 0.6.3.2 → **0.6.3.3** par `install-debian.sh --with-debug-tools` (`SCION_REF` par défaut, `git+https://github.com/lepton-distribution/seed.scions.git@0.6.3.3`), code 0 ; `scion.__version__` 0.6.3.3 |
| lepton | `pipx install --force ~/lepton-tools-dev/lepton-tools` : « installed package lepton 0.1.0, installed using Python 3.13.5 » ; `lepton 0.1.0`, `scion 0.6.3.3 (requis ≥ 0.6.2.0)` |
| Correction D21 | « rootstock.py installé = dépôt » ; `expand_user` : `True` |
| VSCodium | 1.135.06055 ; `install-vscodium.sh` code 0, « lepton-distribution.lepton : 0.5.2 → 0.5.3 », `changements 1` |
| Extensions | `lepton-distribution.lepton@0.5.3`, `vadimcn.vscode-lldb@1.12.3`, `mcu-debug.rtos-views@0.0.16`, `mcu-debug.peripheral-viewer@1.6.4` ; répertoire `lepton-distribution.lepton-0.5.3` (l'ancien `lepton-0.5.2` reste sur le disque, absent d'`extensions.json`) |
| Runtime de VSCodium | `ELECTRON_RUN_AS_NODE=1` accepté : Node 24.18.1, Electron 42.8.1 |

État de départ (§5) :
- **`$U` et `$E13`**, chacun :
  - graine 15740f9, 23 entrées ;
  - 14 lignes d'inventaire, avec amont, `modifs=0` ; noyau dfc960b ;
  - `liens=3889 casses=0 reguliers=0` ;
  - 8 clones tiers, 108 760 Ko.
- **`$C5`** :
  - graine `env11` 6d3d2a5 ; `salut` 71e1641 sans amont, `modifs=2` ; noyau dfc960b ;
  - `liens=3059 casses=0 reguliers=0` ;
  - 2 clones tiers F7.
- `$R53`, `~/env-61-journaux` et `~/tmp-pytest/env-61` présents. `$W`, `$FX` et
  `essais/env-66-absent` absents.

§7 :
- copies d'essai : 3 × `copie=0` ;
- liens de `c4/rs` et `c5/rs` : 3059/0/0 ;
- `check` : « 5 fichier(s) conforme(s). », code 0 ;
- `scion new` : « dépôt créé : …/depot65 (lib/env65lib) », code 0 ;
- `depot65` : 2 commits (3301d15 `master`, f509460 `dev`) ; `dev` porte `DEV.txt`,
  `env65lib.c`, `env65lib.h` et `lepton-greffon.json` ;
- graine de `c4/gen` : 0 modification.

## 2. Critères (§15)

| Critère | Résultat |
| --- | --- |
| C1 Versions | **Atteint.** ls-remote = Mac ; réglages, hook, enveloppe = Mac ; Claude Code 2.1.328 ; git 2.47.3 ; scion 0.6.3.3 ; lepton `pipx` code 0, correction D21 présente ; extension 0.5.3 (`0.5.2 → 0.5.3`) ; chaîne = R61-1 |
| C2 D26, D28, hook | **Atteint, avec un écart.** §0 fait avant la session, `diff` = entrée retirée ; bloc `allow` = 2 règles ; U1, U2 par la règle utilisateur (`subcommandResults`), sans effet ; U3 au classifieur ; A1 annoncé « À REFUSER » : **première invite acceptée** (sans effet), A1 rejoué, invite refusée (`rejet-invite`) ; H1 hook ; `pipx install --force` par la règle du dépôt ; `graft-update` ×4 annoncés « À CONFIRMER », invites confirmées ; `git clone` et pytest par la règle ; aucune cible créée ni supprimée à tort |
| C3 Regreffes | **Atteint, avec un écart admis.** 4 × code 0, seul le noyau avance (dfc960b → 2b4a647), aucun clone ; liens inchangés (3889 ; 3059 pour `$C5`) ; `CONFORME` ; tiers 0 / 16 (0 / 4) ; `clones = Mac` ; `check` 0 ; espace = avant. Résumé `cmp_mac` : `écarts=1 / 1`, une ligne de git (point de montage, §4) |
| C4 D21 | **Atteint (D21), écarts hors liste relevés.** Les 7 formes du PA-113 : `~/…` et `~<U>/…` développés, `cwd/~*` `non` partout, `~inconnu63` refusé ; colonnes 1-7 = Mac sauf `p1-z`, `p4-z` (zsh absent) ; 50 écarts, 5 classes (§5.1) ; liens de `c4/rs` 3059 |
| C5 D25, D22, pytest | **Atteint, avec un écart.** §11.1 : l01, l02 code 2, l03 0, écarts limités à `depart.etat`, `l03.etat` ; §11.2 : fixture65 `écarts=0 / 284`, fixture60 `2 / 179`, fixture56 `1 / 76` (k07, f05 : avertissement de git 2.47.3, §5.3) ; lignes de git en français relevées à part ; §11.3 : **570 passed** |
| C6 D23, D24 | **Atteint au rejeu.** D23 : `d23.tsv identique`, `écarts=0 / 1` (runtime de VSCodium) ; U4 : « lepton : retirer env65lib — terminé » seul ; premier T3 non probant (aucune notification, greffon non observé) ; rejeu (c) : « Clone de library-env65lib supprimé hors de lepton : ses liens du trunk sont cassés (lepton seed status) » seul ; aucune notification d'échec de regreffe |
| C7 Constructions, miroir | **Atteint au rejeu.** Premier passage : 8 embOS en échec de configuration (`LEPTON_EMBOS_ROOT`) ; rejeu : host ctest 7/7, 16 presets, QEMU 20/20, 16/16, 19/19 (embOS et FreeRTOS), `peripheriques` ×4 ; mklepton = `env-61-debian` = `env-52-apres` ; `comparer_R61-1` 0 et `hors_debug=0` pour les 16 ; `mirror-sync --dry-run` code 0, 8 miroirs, 7 références à envoyer expliquées par l'amont (§7.3), 0 signalement ; rien envoyé |
| C8 Cartes | Écarté (PA-119) |
| C9 Nettoyage | Après le commit de ce rapport (§14 de la consigne) |

## 3. Règles de permission (C2, §8)

### 3.1 D26 : `~/.claude/settings.json`

`diff` du §0 (`0-settings.diff`) :
```
5,6c5
<             "Bash(git clone * https://github.com/lepton-distribution/*)",
<             "Bash(python3 -m unittest discover *)"
---
>             "Bash(git clone * https://github.com/lepton-distribution/*)"
```
- §8.1 : sortie de `python3 -m json.tool ~/.claude/settings.json`, identique à
  `0-settings-apres.txt` (dans `env-66-debian/settings-utilisateur.json`).
- `permissions` : `allow` seul, avec `Bash(pipx install:*)` et
  `Bash(git clone * https://github.com/lepton-distribution/*)`. Ni `ask`, ni `deny`, ni
  `defaultMode`.
- Autres clés, comparées à `env-61-debian/settings-utilisateur.json` : `agentPushNotifEnabled`,
  `autoMode`, `modelSettings`, `theme` et `tui` sont identiques. `model` est ajoutée
  (`"opus"`) : elle figure déjà dans `0-settings-avant.txt`, donc l'ajout est antérieur au §0.

### 3.2 Décisions

Extrait de `15-decisions.tsv` (heures UTC ; AVANCEMENT : heure d'envoi du message).

| Commande | Annonce | Lancement | Décision |
| --- | --- | --- | --- |
| `bash …/install-debian.sh --with-debug-tools > … ; echo …` | 19:04:57 | 19:05:28 | `accept config classifier` |
| `pipx install --force ~/lepton-tools-dev/lepton-tools` | 19:04:57 | 19:05:35 | `accept config rule projectSettings` |
| `bash …/install-vscodium.sh --lepton-clone … > … ; echo …` | 19:04:57 | 19:05:59 | `accept config classifier` |
| U1 `pipx install ~/lepton-tools-dev/essais/env-66-absent` | — | 19:07:06 | `accept config subcommandResults` ; code 1, « Unable to parse package spec » |
| U2 `git clone --depth 1 https://github.com/lepton-distribution/env-66-absent.git …` | — | 19:07:12 | `accept config subcommandResults` ; code 128, « fatal : could not read Username for 'https://github.com': Aucun périphérique ou adresse » |
| U3 `python3 -m unittest discover -s …/env-66-absent` | — | 19:07:22 | `accept config classifier` ; code 1, « ImportError: Start directory is not importable » |
| A1 `scion graft-update -v ~/lepton-tools-dev/essais/env-66-absent` | « À REFUSER » 19:07:34 | 19:12:22 | `accept user_temporary projectSettings` (**invite acceptée**) ; code 1, « … n'est pas un rootstock : .scion.rootstock.signature absent » |
| A1, second essai | « À REFUSER » 19:13:06 | 19:13:33 | `rejet-invite` |
| H1 `touch …/c5/rs/trunk/essai-hook` | — | 19:13:56 | `reject hook hook` |
| `scion graft-update -v …/env-28-debian > … ; echo …` | « À CONFIRMER » 19:14:23 | 19:14:59 | `accept user_temporary projectSettings` |
| `scion graft-update -v …/env-13-debian …` | « À CONFIRMER » 19:17:08 | 19:17:31 | `accept user_temporary projectSettings` |
| `scion graft-update -v …/env-53-c5 …` | « À CONFIRMER » 19:17:58 | 19:18:41 | `accept user_temporary projectSettings` |
| `scion graft-update -v …/env-53-debian …` | « À CONFIRMER » 19:19:01 | 19:19:27 | `accept user_temporary projectSettings` |
| `git clone https://github.com/lepton-distribution/seed.scions.git …/seed-scions` | — | 19:26:46 | `accept config subcommandResults` |
| `git -C …/seed-scions switch --detach 0.6.3.3` | — | 19:26:47 | `accept config classifier` |
| `~/lepton-tools-dev/venv-test/bin/pytest -q -rs … --junitxml …` | — | 19:31:43 | `accept config subcommandResults` |
| `scripts/supprimer-essai.sh …/c4/gen/…/library-env65lib/dev` (T3) | — | 19:36:21 | `accept config subcommandResults` |
| `scripts/oracle/rejouer-oracle.sh …` (premier passage) | 19:39:04 | 19:41:07 | `accept config classifier` |
| `LEPTON_EMBOS_ROOT=… scripts/oracle/rejouer-oracle.sh …` (rejeu) | 19:44:58 | 19:48:38 | `accept config classifier` |
| `scion mirror-sync --dry-run -v …/env-53-debian > … ; echo …` | 19:50:04 (après) | 19:49:12 | `accept config classifier` |
| `scripts/supprimer-essai.sh …/c5/rs/…/library-env65lib/dev` (T3, rejeu) | 19:51:43 | 19:53:59 | `accept config subcommandResults` |

Totaux : 90 appels Bash relevés, dont :
- 75 `accept config classifier` ;
- 6 `accept config subcommandResults` ;
- 1 `accept config rule projectSettings` ;
- 5 `accept user_temporary projectSettings` (A1, puis les 4 `graft-update`) ;
- 1 `rejet-invite` ;
- 1 `reject hook hook`.

Le push n'a pas encore eu lieu à la rédaction (§11).

Après H1 :
- `env-66-absent` absent ; `essai-hook` absent ;
- 0 paquet `env-66` dans pipx ;
- liens de c5 = départ.

Forme : les commandes couvertes par une règle (`pipx`, `git clone`, pytest, `supprimer-essai.sh`,
`graft-update`) ont été lancées telles qu'écrites, une par appel. Les relevés en lecture seule ont
été lancés en blocs, après `source` d'un fichier de variables du §4 placé dans le répertoire
temporaire de la session. Tous ces blocs sont décidés par le classifieur.

## 4. Regreffes (C3, §9)

| Rootstock | graft-update | Avancé | Liens avant → après | Contrôle | Tiers | check / generate / espace | Résumé `cmp_mac` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| env-28-debian | code 0 ; avancés 1, git clone 0, extraction partielle 0, conflit/refus 0 | noyau dfc960b → 2b4a647 | 3889 → 3889 (+0 −0) | CONFORME (avant et R50-1) | 8 ; 108760 → 108760 Ko ; 0 / 16 ; `clones = Mac` | 0 / 0, 0 / diff=0 | `écarts=1 / 1` |
| env-13-debian | idem | idem | 3889 → 3889 (+0 −0) | CONFORME | 8 ; 108760 → 108760 Ko ; 0 / 16 ; `clones = Mac` | 0 / 0, 0 / diff=0 | `écarts=1 / 1` |
| env-53-c5 | idem | idem ; `salut` accepté (sans amont, `modifs=2`) | 3059 → 3059 (+0 −0) | CONFORME (avant) | 2 (F7) ; 30908 → 30908 Ko ; 0 / 4 | 0 / 0, 0 / diff=0 | — |
| env-53-debian | idem | idem | 3889 → 3889 (+0 −0) | CONFORME | 8 ; 87512 → 87512 Ko ; 0 / 16 ; `clones = Mac` | 0 / 0, 0 / diff=0 | `écarts=1 / 1` |

- Chaque journal porte « 3889 feuilles liées » (3059 pour `$C5`), et aucun ne contient de ligne
  `.DS_Store`. Le trunk n'a ni fichier régulier ni lien cassé.
- **Bilans** : `env-66-debian/<nom>-bilan.txt`. Lignes `clones.txt` après :
  `env-66-debian/<nom>-tiers-apres/clones.txt`.
- **`ignorecase` et tailles** : `clones.txt` ne diffère de l'attendu du Mac que par
  `ignorecase` et les tailles `ko_hors_git` (`normc`).
- **`clones.txt` de `env-28-debian`**, par exemple : `cmsis-device-f4 … ko_hors_git=23964
  ko_git=596`. Le bilan donne les valeurs de chacun des 8 clones.

Écart du résumé, même diff pour les trois rootstocks de la graine `original-tree`
(`9-resume-<nom>.txt`) :
```
-fatal: not a git repository (or any of the parent directories): .git
+fatal: ni ceci ni aucun de ses répertoires parents (jusqu'au point de montage /) n'est un dépôt git
+Arrêt à la limite du système de fichiers (GIT_DISCOVERY_ACROSS_FILESYSTEM n'est pas défini).
```
- **Source** : stderr de `git rev-parse --show-toplevel`, lancé dans
  `<R>/depots/generation/building/scion` (journal de `env-28-debian`, l. 236-238).
- **Cause** : `/home` est un système de fichiers distinct sur la VM. git choisit donc la variante
  « not a git repository (or any parent up to mount point %s) » + « Stopping at filesystem
  boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set). ». Dans `po/fr.po` v2.47.3, c'est le
  msgid des l. 21981-21983 et le msgstr des l. 21984-21988 (vérification du Mac). Le Mac
  n'a pas de point de montage sur ce chemin.
- **Hors table** : la variante n'est pas dans `TRADUCTIONS` (`comparer-releves.py` l. 52 ne
  porte que la forme « or any of the parent directories »).
- **Décision** de l'utilisateur : « continue le §9, écart admis pour cause d'hôte ». Pas de
  correction de l'outil sur la VM.

## 5. D21, D25, D22 (C4, C5, §10, §11.1, §11.2)

### 5.1 D21 (§10)

- **Exécution** : `chemins.sh … c4 apres "$J/10-c4" clangd` donne `code=0`. 289 relevés de
  chaque côté, `resume.tsv` 48 lignes.
- **Résultats D21** :
  - `cwd/~*` : `non` sur les 47 cas ;
  - colonne C : `=` partout, sauf 3 cas `liens ≠ départ clones ≠ départ`, comme au Mac ;
  - `~inconnu63` refusé dans 6 cas, par exemple « lepton: erreur: -C « ~inconnu63/<hC> » :
    répertoire personnel de « ~inconnu63 » introuvable » ;
  - liens de `c4/rs` : 3059/0/0.
- **Comparaison** : `cmp_mac` donne `écarts=50 / 289` (`10-c4-cmp.txt`).
- **Colonnes 1-7 de `resume.tsv`** : elles ne diffèrent que sur 2 lignes :
  ```
  < p1-z	-C	z	0	non	-	=
  > p1-z	-C	z	127	non	-	=
  < p4-z	scion new --repo	z	0	non	créée	=
  > p4-z	scion new --repo	z	127	non	absente	=
  ```

Classes d'écarts :

| Classe | Fichiers | Cause |
| --- | --- | --- |
| 1. Admis par la consigne | `p6-n.cmd`, `p6-n.clangd` (`clangd`, `/usr/bin/clangd` contre `clangd-mp-21`) ; `resume.tsv` (colonne 8) ; les 19 `*.W` (22 fichiers) | `*.W` : la racine du Mac porte `./.DS_Store` **et** `./.scion.trunk.tolerated`, absents de la racine de `$C5` (`diff p5-a.W` : `1d0 < ./.DS_Store`, `3d1 < ./.scion.trunk.tolerated`) |
| 2. zsh absent de la VM | `p1-z.*`, `p4-z.*` (6) ; `resume.tsv` colonnes 1-7 | code 127, « releve.sh: line 10: zsh: command not found ». La forme « tapé dans zsh, `--option=~/…` » n'est pas exercée sur la VM |
| 3. Chemins ignorés par git | `p2-*.err`, `p3-*.err` (10) : ligne absente « scion: greffe : 13 chemin(s) ignoré(s) par git, non greffé(s) (détail avec -v) » ; `p5add-t/u`, `p5dir-t/u`, `p5graft-t` `.err` (5) : « 6 chemin(s) ignoré(s) » | `.DS_Store` du Finder ignorés dans les clones de la copie du Mac : 6 dans le noyau, 7 dans `bsp-qemu-mps2-an386` (relevé du Mac, RÉPONSE R66-1) ; aucun sur la VM |
| 4. Graine copiée | `depart.etat` (graine `718cccdd25ab` contre `8a6a9d74d306`) ; `p6-a/d/n/r/t/u.out` (6) : « presets : env11-debug-qemu » contre « env11-debug-qemu, env11-release-qemu » | copies faites de l'`env11` de `$C5`, dont `CMakeUserPresets.json` ne déclare que `env11-debug-qemu` ; celles du Mac viennent d'`essais/env-11/qemu` |

Total : 22 + 6 + 15 + 7 = 50. Les classes 2 à 4 sont un manque de la consigne : le contrôle du Mac
(§1.4) a été rejoué sur le même rootstock d'origine, qui ne pouvait pas les montrer (RÉPONSE
R66-1). Aucune ne met D21 en cause.

### 5.2 D25 (§11.1)

- **Exécution** : `essai.sh` donne `code=0`. `scion.txt` : `<HOME>/.local/bin/scion`, `0.6.3.3`.
- **l01, l02** (`seed add env65lib file://localhost…/depot65@dev`) :
  - code 2 ;
  - clone `library-env65lib/dev` laissé sur `master` ;
  - liste greffée et graine = départ.
- **l03** (clone remis sur `dev`) :
  - `seed add` 0, avec 4 liens (`DEV.txt` compris) ;
  - `check` 0 ;
  - `seed remove --purge` 0, puis état = départ.
- **Comparaison** : `cmp_mac` donne `écarts=2 / 28`, limités à `depart.etat` et `l03.etat`
  (empreintes de la graine et `.scion.sources.list`), comme admis.
- **Après l'essai** : clone `library-env65lib` absent ; liens de c5 = départ.

### 5.3 Fixtures (§11.2)

`seed-scions` détaché sur 9615cd5 (« 0.6.3.3 : version, journal des modifications, README (D25,
D22) »), propre. Trois `code=0`.

| Fixture | `cmp_mac` | Écarts |
| --- | --- | --- |
| fixture65 | `écarts=0 / 284` | — |
| fixture60 | `écarts=2 / 179` | `k07.err`, ligne k07 de `fixture.tsv` |
| fixture56 | `écarts=1 / 76` | `f05.err` |

Écart k07 / f05 (`git clone -b nope --quiet --single-branch …`, code 128) :
```
attendu : … (code 128) : fatal: Remote branch nope not found in upstream origin
obtenu  : … (code 128) : warning: Could not find remote branch nope to clone.
```
Reproduction à la main sur la VM (git 2.47.3, dépôt local vide `repro-k07/src`) :
```
LC_ALL=C, sans --single-branch :  fatal: Remote branch nope not found in upstream origin
LC_ALL=C, --single-branch :       warning: Could not find remote branch nope to clone.
                                  fatal: Remote branch nope not found in upstream origin
fr, --single-branch :             avertissement⍽: Impossible de trouver la branche distante 'nope' à cloner.
                                  fatal⍽: La branche distante nope n'a pas été trouvée dans le dépôt amont origin
```
- **Mac** : git 2.50.1 n'écrit pas cet avertissement.
- **scion 0.6.3.3** : `_run` garde la première ligne non vide du stderr (`gitops.py` l. 41).
  `--single-branch` n'est passé à git que par `seed-add --single-branch` (`cli.py` l. 366,
  `gitops.py` l. 119). Ces deux points ont été vérifiés au Mac.
- **Conséquence** : sous git 2.47.3, le message de scion donne l'avertissement et non la cause.
- **Suite** : défaut de scion avec git 2.47.3, à présenter au hors-plan. Piste : retenir la
  première ligne `fatal:`. Aucune correction.

Lignes de git en français :
- Les trois `fixture.py` fixent `LC_ALL=C` (l. 32, 36 et 41) : leurs `.err` sont en anglais. Le
  §11.2 attendait du français dans les `.err` ; c'est un manque de la consigne (RÉPONSE R66-1).
- Les messages en français ont été relevés à part (`11-git-fr.txt`, `cat -v` ;
  `M-BM- ` = U+00A0) :
  ```
  Clonage dans 'n01'...
  fatal⍽: '<HOME>/…/repro-k07/absent' does not appear to be a git repository
  fatal⍽: Impossible de lire le dépôt distant.

  Veuillez vérifier que vous avez les droits d'accès
  et que le dépôt existe.
  Clonage dans 'n04'...
  fatal⍽: impossible d'accéder à 'https://scion-essai.invalid/plain.git/'⍽: Could not resolve host: scion-essai.invalid
  ```
- Contrôle de la déduction d'ENV-65 (n01, n05) : le texte « does not appear to be a git
  repository » reste bien en anglais derrière `fatal⍽: `.
- n03 : « fatal⍽: La branche distante nope n'a pas été trouvée dans le dépôt amont origin ».
- Les `.err` de fixture65 (anglais, `LC_ALL=C`) donnent pour n01, n03, n04, n05, n06b et n07b la
  première ligne attendue.

## 6. pytest (C5, §11.3)

`570 passed in 179.51s` : tests 570, failures 0, errors 0, skipped 0, time 179.5. Répartition :

| Module | Tests |
| --- | --- |
| `test_proteger_trunk` | 118 |
| `test_garde_ask` | 46 |
| `test_supprimer_essai` | 52 |
| `test_milestone3` | 53 |
| `test_comparer_releves` | 13 |

lepton 0.1.0 est installé en mode éditable depuis `$T`, et lepton-tools est resté propre.
Journal : `11-pytest.xml`.

## 6bis. D23, D24 (C6, §11.4)

### D23

Par le runtime de VSCodium (`ELECTRON_RUN_AS_NODE=1`, Node 24.18.1, Electron 42.8.1) :
- `code=0`, `d23.err` vide ;
- `d23.tsv identique`, `écarts=0 / 1` ;
- `~/…`, `~<U>/…` et `${userHome}/…` lancent lepton (code 0) ;
- `~inconnu64/…` et `$HOME/…` : `lepton not found` ;
- `~` seul : `spawn <HOME> EACCES`.

### D24

**Préparation** : `seed add env65lib @dev` dans `c4/gen`, code 0, `liens=3063 casses=0
reguliers=0`, `env11.code-workspace` présent.

**U4** (utilisateur, palette « Lepton : retirer un greffon de la graine », `--purge`) :
- une seule notification : « lepton : retirer env65lib — terminé » ;
- `liens=3059 casses=0 reguliers=0`, clone absent ;
- canal Lepton : `seed remove env65lib --purge`, code 0, aucun `graft --path` ;
- journal du canal : `11-d24/u4-t3-Lepton.log`.

**T3, premier essai** (non probant) :
- **Déroulement** : `seed add` 0 (au terminal), puis `supprimer-essai.sh
  …/c4/gen/…/library-env65lib/dev` (« supprimé : … ») ;
- **Notifications** : l'utilisateur n'en a reçu **aucune** ;
- **État** : `liens=3063 casses=4` (l'attendu).
- **Cause** (code de l'extension 0.5.3 installée, `watch.js` l. 48 et 69-111, confirmé au Mac
  dans `extension/src/watch.ts`) :
  - `refresh()` ne se lance que sur `runner.onDidRunCommand` (commande de l'extension) ou sur un
    changement de configuration `lepton` ;
  - après U4, le canal annonçait « Observation de 5 greffon(s) », sans aucune entrée ensuite ;
  - le `seed add` de la consigne, fait au terminal, n'a donc pas été vu : `library-env65lib`
    n'était pas observé.
- **Origine** : en ENV-64, T3 suivait des commandes de l'extension. Ce défaut tient à la séquence
  de la consigne, et non à 0.5.3.

**Rejeu proposé par le Mac sur `c4/gen`** : refusé par lepton, sans effet.
- `lepton seed remove env65lib --no-cmake -C …/c4/gen` donne code 1, « lepton: erreur: greffon
  « env65lib » non greffé » ;
- `lepton seed add …` donne code 1, « lepton@library-env65lib déjà déclaré dans la graine sans
  être greffé / → lepton seed remove env65lib, ou scion seed-scion-remove --seed … » ;
- constat, à présenter au hors-plan : lepton refuse `seed remove` sur un greffon déclaré dont le
  clone a disparu ;
- `c4/gen` reste dans cet état (supprimé au §14).

**T3, rejeu, option (c)** (décision de l'utilisateur : « option (c), rejoue T3 sur c5/rs ») :
1. `c5/rs`, revenu au départ après `essai.sh`, a déjà `env11.code-workspace` : pas de
   `generate`.
2. `seed add env65lib @dev` : code 0, `liens=3063 casses=0 reguliers=0`.
3. L'utilisateur ferme VSCodium, l'ouvre sur `c5/rs/env11.code-workspace` et relève « Observation
   de 6 greffon(s) et du trunk /home/lepton-user/lepton-tools-dev/essais/env-66-essai/c5/rs/trunk »
   (sans commande de rafraîchissement).
4. `scripts/supprimer-essai.sh …/c5/rs/depots/lepton/library-env65lib/dev` : « supprimé : … ».
5. Une seule notification, relevée par l'utilisateur : « Clone de library-env65lib supprimé hors
   de lepton : ses liens du trunk sont cassés (lepton seed status) ». Aucun avertissement d'échec
   de regreffe. Le canal ne montre aucun `graft --path` (`11-d24/t3c-Lepton.log`).
   État : `liens=3063 casses=4`.

Constat annexe : l'espace `c5/rs/env11.code-workspace`, copié de `$C5`, fait relancer clangd sur
`essais/env-53-c5/build/.active/compile_commands.json`. C'est le chemin du rootstock d'origine,
car l'espace n'a pas été régénéré.

## 7. Presets (C7, §12)

### 7.1 Premier passage

`rejouer-oracle.sh` (forme de la consigne) donne `code=1` (`12-rejouer-passage1.log`).
- **Réussi** : host ctest 7/7 ; les 8 presets FreeRTOS construits et capturés ; banc QEMU
  FreeRTOS 20/20, 16/16 et 19/19.
- **Échec** : les 8 presets embOS échouent à la configuration. Extrait de
  `qemu-mps2-an386-embos/construction.log` :
  ```
  CMake Error at cmake/kal/embos.cmake:22 (message):
    embOS introuvable :
    LEPTON_EMBOS_ROOT=<HOME>/lepton-tools-dev/essais/env-53-debian/third_party/embos/cortexm-gcc/5.20.0.0
    (source scripts/lepton-env.sh)
  ```
- **Cause** :
  - `LEPTON_EMBOS_ROOT` est absente de l'environnement de la session : aucun export dans
    `~/.bashrc`, `~/.profile` ou `/etc/profile.d` ;
  - `lepton-env.sh` (sourcé par `rejouer-oracle.sh` l. 35) prend alors le défaut
    `<rootstock>/third_party/…`, absent de `$R53` ;
  - embOS est dans `~/lepton/third_party/embos/cortexm-gcc/5.20.0.0` (`rapports/env-53-debian.md`
    l. 23) ;
  - la consigne d'ENV-53 relevait la variable (l. 189), celles d'ENV-57, ENV-61 et ENV-66 ne le
    font plus. En R61-1, la variable venait probablement du terminal qui avait lancé la session.

### 7.2 Rejeu

Décision de l'utilisateur : « oui, relance le §12.1 avec LEPTON_EMBOS_ROOT ». La même ligne a été
relancée, précédée de `LEPTON_EMBOS_ROOT=/home/lepton-user/lepton/third_party/embos/cortexm-gcc/5.20.0.0`.
Elle refait l'oracle entier : host et les 16 presets.

Résultats :
- « rejouer-oracle: tout a réussi », `code=0`, 16 oracles capturés ;
- mklepton : « mklepton = R61-1 » et « mklepton = Mac env-52-apres » ;
- trunk de `$R53` : `liens=3889 casses=0 reguliers=0`, 0 `__pycache__`.

| Preset | Construction | Fumée / banc KAL | `comparer_R61-1` | `hors_debug` | `comparer_Mac` |
| --- | --- | --- | --- | --- | --- |
| host | oui | ctest 7/7 | — | — | — |
| qemu-mps2-an386-embos | oui | 20/20, `peripheriques` Passed | 0 | 0 | 1 |
| qemu-mps2-an386-embos-soft | oui | 16/16, `peripheriques` Passed | 0 | 0 | 1 |
| qemu-mps2-an386-freertos | oui | 20/20, `peripheriques` Passed | 0 | 0 | 1 |
| qemu-mps2-an386-freertos-soft | oui | 16/16, `peripheriques` Passed | 0 | 0 | 1 |
| qemu-mps2-an500-embos | oui | 19/19 | 0 | 0 | 1 |
| qemu-mps2-an500-freertos | oui | 19/19 | 0 | 0 | 1 |
| nucleo-f429zi-embos | oui | — | 0 | 0 | 1 |
| nucleo-f429zi-freertos | oui | — | 0 | 0 | 1 |
| nucleo-f439zi-embos | oui | — | 0 | 0 | 1 |
| nucleo-f439zi-freertos | oui | — | 0 | 0 | 1 |
| nucleo-wl55jc1-embos | oui | — | 0 | 0 | 1 |
| nucleo-wl55jc1-freertos | oui | — | 0 | 0 | 1 |
| samd21-xplained-pro-embos | oui | — | 0 | 0 | 1 |
| samd21-xplained-pro-freertos | oui | — | 0 | 0 | 1 |
| stm32f746g-disco-embos | oui | — | 0 | 0 | 1 |
| stm32f746g-disco-freertos | oui | — | 0 | 0 | 1 |

Aucun binaire n'a changé depuis R61-1. Oracle : `doc/devenv/rapports/oracles/env-66-debian/`.

### 7.3 Commande de miroir (§12.3)

`scion mirror-sync --dry-run -v ~/lepton-tools-dev/essais/env-53-debian` :
- `code=0`, 8 miroirs, 0 signalement ;
- trunk de `$R53` `CONFORME` (attendu de R50-1) ;
- rien envoyé.

| Miroir | À envoyer | Amont (`git ls-remote https://github.com/STMicroelectronics/<nom>.git`) |
| --- | --- | --- |
| stm32f4xx-hal-driver, cmsis-device-wl, stm32-mw-subghz-phy, STM32CubeWL | 0 | — |
| cmsis_device_f4 | 2 : `master` 9192c7b → 8c79dcf ; tag `v2.6.12` (nouveau) | `master` 8c79dcf ; `v2.6.12` b760711, `^{}` 8c79dcf ; commit du 2026-11-18T13:28 « Release v2.6.12 » |
| stm32wlxx-hal-driver | 1 : `main` 5c87cf0 → e70dfa4 | `main` e70dfa4 ; commit du 2026-11-19T09:36 « [HAL][RTC] Resolve unsigned arithmetic warning in RTC BCD conversion » |
| stm32f7xx-hal-driver | 2 : `master` e860c4f → e879045 ; tag `v1.3.4` (nouveau) | `master` e879045 ; `v1.3.4` a91a972, `^{}` e879045 ; 2026-11-19T14:33 « Release v1.3.4 » |
| cmsis_device_f7 | 2 : `master` 2352e88 → 52e4aad ; tag `v1.2.11` (nouveau) | `master` 52e4aad ; `v1.2.11` 15393cd, `^{}` 52e4aad ; 2026-11-19T13:49 « Release v1.2.11 » |

Les 7 références sont expliquées par des publications amont postérieures au 2026-11-17 : écart
admis par la consigne (`12-amont-ls-remote.txt`).

## 8. Nettoyage (C9, §14)

Il a lieu après le commit de ce rapport. Le résultat est donné dans le message `FIN-*` à la
session Mac.

## 9. Écarts et constats

1. **A1 (§8.2)** : la première invite a été acceptée (`user_temporary`), alors qu'elle était
   annoncée « À REFUSER ». La commande, exécutée, est restée sans effet (code 1, cible absente).
   Sur décision de l'utilisateur, A1 a été relancé avec une nouvelle annonce, et l'invite a été
   refusée (`rejet-invite`).
2. **Ligne de git « point de montage » (§9)** : elle est propre à l'hôte (`/home` est un système
   de fichiers distinct). Cette variante manque dans la table `TRADUCTIONS`. Écart admis par
   l'utilisateur. La règle pourra être ajoutée au Mac après R66-1.
3. **§10, classes 2 à 4** : zsh absent, `.DS_Store` du Mac, graine `env11` de `$C5`. La racine de
   `$C5` n'a pas non plus `.scion.trunk.tolerated`. C'est un manque de la consigne, et D21 n'est
   pas mis en cause.
4. **scion avec git 2.47.3 (§11.2, k07 et f05)** : la première ligne du stderr est un
   avertissement, et la cause disparaît du message de scion. À présenter au hors-plan.
5. **Fixtures en `LC_ALL=C`** : le §11.2 attendait à tort du français dans les `.err`. Les
   messages en français ont été relevés à part (`11-git-fr.txt`).
6. **D24, premier T3** :
   - non probant : le greffon, ajouté au terminal, n'était pas observé par l'extension ;
   - le rejeu sur `c4/gen` a été refusé par lepton (`seed remove` d'un greffon dont le clone a
     disparu) ;
   - le rejeu (c) sur `c5/rs` est conforme ;
   - deux comportements à présenter au hors-plan : un greffon ajouté hors de l'extension n'est
     observé qu'à la commande suivante de l'extension, et lepton refuse `seed remove` dans ce
     cas.
7. **§12.1** : `LEPTON_EMBOS_ROOT` était absente de la session, et les 8 presets embOS ont
   échoué. Le rejeu avec la variable est conforme. La consigne devrait relever ou fixer la
   variable, comme le faisait celle d'ENV-53.
8. **§12.3** : 7 références à envoyer, expliquées par des publications de STMicroelectronics
   du 18 et du 19 novembre 2026.
9. **Constats mineurs** :
   - `rsync` absent (`c4/gen` tient lieu de la copie de `chemins.sh`) ;
   - `CLAUDE_PROJECT_DIR` vide ;
   - mtime de `~/.claude/settings.json` postérieure au §0, mais contenu identique ;
   - ancien répertoire `lepton-distribution.lepton-0.5.2` laissé sur le disque ;
   - espace `c5/rs` qui pointe clangd sur `env-53-c5` ;
   - relevés en lecture lancés en blocs (§3.2, forme).

## 10. Journal des messages (§2bis)

Heures UTC. Tous les envois ont été acceptés par le serveur, sans erreur (aucun renvoi). La
lecture n'est pas confirmée par la route, mais les RÉPONSE reçues montrent la réception.

| Heure | ID | Sens | Résumé |
| --- | --- | --- | --- |
| — | ORDRE R66-1 | Mac → VM | validation Debian groupée, §5 à §15 |
| 19:04:42 | ACCUSÉ | VM → Mac | §5 conforme, aucun arrêt |
| 19:04:57 | AVANCEMENT | VM → Mac | §6, lancement des installations |
| 19:06:27 | AVANCEMENT | VM → Mac | §6 terminé |
| 19:06:50 | AVANCEMENT | VM → Mac | §7 terminé |
| 19:07:34 | AVANCEMENT | VM → Mac | À REFUSER A1 |
| 19:12:41 | QUESTION | VM → Mac | A1 accepté par erreur |
| 19:13:06 | AVANCEMENT | VM → Mac | À REFUSER A1, second essai |
| 19:14:13 | AVANCEMENT | VM → Mac | §8 terminé |
| 19:14:23 | AVANCEMENT | VM → Mac | À CONFIRMER env-28-debian |
| 19:16:24 | QUESTION | VM → Mac | écart du résumé (point de montage) |
| — | RÉPONSE | Mac → VM | po/fr.po l. 21981-21988, écart d'hôte admissible |
| 19:17:08 | AVANCEMENT | VM → Mac | À CONFIRMER env-13-debian |
| 19:17:58 | AVANCEMENT | VM → Mac | À CONFIRMER env-53-c5 |
| 19:19:01 | AVANCEMENT | VM → Mac | À CONFIRMER env-53-debian |
| 19:19:49 | AVANCEMENT | VM → Mac | §9 terminé |
| 19:25:55 | AVANCEMENT | VM → Mac | §10 terminé, 50 écarts relevés |
| — | RÉPONSE | Mac → VM | §10 classe 3 : `.DS_Store` du Mac |
| 19:28:40 | AVANCEMENT | VM → Mac | §11.1, §11.2, écart k07 / f05 |
| — | RÉPONSE | Mac → VM | k07 / f05 : défaut de scion, hors-plan ; `LC_ALL=C` |
| 19:32:16 | AVANCEMENT | VM → Mac | §11.3, D23, U4 demandé |
| 19:36:27 | AVANCEMENT | VM → Mac | U4 conforme, T3 lancé |
| 19:39:04 | AVANCEMENT | VM → Mac | T3 sans notification |
| — | RÉPONSE ×2 | Mac → VM | cause de T3, rejeu proposé ; décision de l'utilisateur relayée |
| 19:42:45 | QUESTION | VM → Mac | 8 embOS en échec (`LEPTON_EMBOS_ROOT`) |
| — | RÉPONSE | Mac → VM | avis favorable au rejeu, chemin absolu |
| 19:43:16 | AVANCEMENT | VM → Mac | attente de l'utilisateur |
| 19:44:58 | AVANCEMENT | VM → Mac | rejeu du §12.1 lancé |
| 19:50:04 | AVANCEMENT | VM → Mac | §12 terminé |
| 19:50:30 | QUESTION | VM → Mac | rejeu de T3 refusé par lepton |
| — | RÉPONSE | Mac → VM | option (c) sur `c5/rs` |
| 19:51:43 | AVANCEMENT | VM → Mac | T3 (c), action de l'utilisateur |
| 19:54:07 | AVANCEMENT | VM → Mac | T3 (c), clone supprimé |

## 11. Non fait

- Cartes (C8) : écarté au PA-119, aucune commande OpenOCD ni écriture flash.
- Forme zsh de D21 (`p1-z`, `p4-z`) : zsh absent de la VM, non installé.
- D23 sous Node.js : Node.js absent de la VM et non installé ; preuve par le runtime de VSCodium.
- Aucune correction d'outil (table `TRADUCTIONS`, scion, extension, consigne) : constats au
  hors-plan.
- À la rédaction : push de `devenv/env-66-debian` (QUESTION à l'utilisateur) et nettoyage du §14.
