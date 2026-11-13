# ENV-57 — Validation Debian groupée (ENV-54 à ENV-56) — 2026-11-13

Session VM `debian-linux-vm` [153462], ordre `R57-1` de la session Mac `validation-debian-env-57`
(nommée `lepton-tools-30` dans la consigne), consigne `doc/devenv/consignes/env-57-debian.md` à
10b6dd3. Répertoire de travail `/home/lepton-user/lepton-tools-dev/lepton-tools` (`$T`), mode auto,
Remote Control. Journaux : `~/env-57-journaux/` sur la VM. Rootstocks regreffés :
`essais/env-28-debian` (`$U`), `essais/env-13-debian` (`$E13`), `essais/env-53-c5` (`$C5`) et
`essais/env-53-debian` (`$R53`). Copie d'essai `essais/env-57-essai` (`$S`) et dépôt
`essais/env-57-depot` (`$D`).

Résultat : C1 à C6 atteints. C7 écarté (PA-101). C8 après le commit de ce rapport (§14 de la
consigne). Un écart au §8 : la première invite N4 a été confirmée au lieu d'être refusée.
La commande a échoué sans effet, sur une cible absente. N4 a été rejoué à la demande de
l'utilisateur, et l'invite refusée.

## 1. Hôte, versions et session (§5, §6)

| Élément | Valeur |
| --- | --- |
| Hôte | Debian 13.7, Linux 6.12.107+deb13-amd64 x86_64, `lepton-user`, git 2.47.3 |
| Espace libre | `/home` 18 Go ; `/tmp` 690 Mo |
| Claude Code | 2.1.323 ; répertoire de travail `$T` ; `CLAUDE_PROJECT_DIR` vide dans l'environnement Bash |
| Réglages | `.claude/settings.json` b01ad557…d235, `proteger-trunk.py` d7d719f1…fdc, `supprimer-essai.sh` 04323a00…0e15 : = Mac. Aucun `settings.local.json`. `~/.claude/settings.json` (10 nov.) : 3 règles `allow` utilisateur, sans `defaultMode` : `Bash(pipx install:*)`, `Bash(git clone * https://github.com/lepton-distribution/*)`, `Bash(python3 -m unittest discover *)` |
| Chaîne APT | arm-none-eabi-gcc `15:14.2.rel1-1` (14.2.1 20241119), cmake 3.31.6, ninja 1.12.1, QEMU 10.0.13 (`1:10.0.13+ds-0+deb13u1`), Python 3.13.5 : = R53-1 |
| Outils | `shasum`, `realpath`, `tar` présents ; `rsync` absent (non requis) |
| scion | 0.6.3.0 → **0.6.3.1** (`install-debian.sh --with-debug-tools`, `SCION_REF` par défaut, `seed.scions.git@0.6.3.1`), code 0 |
| lepton | `lepton 0.1.0`, `scion 0.6.3.1 (requis ≥ 0.6.2.0)` (`pipx install --force`, Python 3.13.5) |
| VSCodium | 1.135.06055 ; `install-vscodium.sh` code 0, `changements 0` |
| Extensions | `lepton-distribution.lepton@0.5.2`, `vadimcn.vscode-lldb@1.12.3`, `mcu-debug.rtos-views@0.0.16`, `mcu-debug.peripheral-viewer@1.6.4` |
| Clone noyau `$K` | propre, `master` 58e421e → **ed2a41f** (avance rapide, 5 fichiers hors `scion/`) ; `SCION_REF="${SCION_REF:-0.6.3.1}"` |
| lepton-tools | `devenv/env-57` = `origin/devenv/env-57` = 10b6dd3, propre ; `SCION_REF="0.6.3.1"` (`install-vscodium.sh`) ; `SCION_MIN_VERSION = (0, 6, 2, 0)` ; `extension/dist/lepton-0.5.2.vsix` présent |

`git ls-remote` : « têtes publiées = Mac » (diff vide avec `env-57-mac/ls-remote-mac.txt`, hors
lepton-tools). lepton-tools `main` 6b6b1d6 ; seed.scions tag `0.6.3.1` c51ee1a (`master`
d650414) ; graine 15740f9 ; noyau ed2a41f ; 12 greffons et 8 miroirs = Mac.

État de départ (§5) :
- `$U` et `$E13`, identiques : graine 15740f9 sur `original-tree`, amont réglé, propre ;
  23 entrées ; 13 clones sur `master`, amont `origin/master`, `modifs=0`, noyau 58e421e ;
  `liens=3889 casses=0 reguliers=0` ; 8 clones tiers, 108 760 Ko ;
- `$C5` : graine `env11` 6d3d2a5 (`master`, sans amont, `modifs=0`) ; 5 entrées ; `salut`
  71e1641 sans amont, `modifs=2` ; an386 10a8889, famille QEMU 3954357, famille F7 12280a5,
  noyau 58e421e, sur `master`, amont réglé, `modifs=0` ; `liens=3059 casses=0 reguliers=0` ;
  2 clones tiers F7, 30 908 Ko ;
- `$R53`, `$P11`, `~/env-53-journaux` présents ; aucun des chemins du §5 n'existait.

## 2. Critères (§15)

| Critère | Résultat | Constat |
| --- | --- | --- |
| C1 Versions | **atteint** | ls-remote = Mac ; réglages, hook, enveloppe = Mac ; Claude Code 2.1.323 ; git 2.47.3 ; scion 0.6.3.1 par `install-debian.sh` (défaut `SCION_REF`) ; lepton `pipx` code 0, `scion 0.6.3.1 (requis ≥ 0.6.2.0)` ; extension 0.5.2, `changements 0` ; chaîne = R53-1 |
| C2 D16 | **atteint, avec un écart** | P3, P4, P5, N1, N2, N2b par la règle (`subcommandResults`) ; `pipx install` par la règle (`rule projectSettings`) ; `graft-update` ×4 sur invite confirmée ; pytest par la règle (`subcommandResults`) ; N3 `classifier` ; N4, N5 invites refusées (`rejet-invite`) ; N6 `deny` ; N7 hook ; aucune cible créée ni supprimée à tort. Écart : 1er N4 confirmé (§7.1) |
| C3 Regreffes | **atteint** | `$U`, `$E13`, `$R53` : code 0, seul le noyau avance (58e421e → ed2a41f), 0 clone, journal = Mac (82 lignes), 3889 liens inchangés, `CONFORME` (avant et R50-1), tiers 0 / 16, `clones = Mac`, `check` 0, espace = avant. `$C5` : noyau seul, 3059 liens inchangés, `CONFORME`, tiers 0 / 4, `check` 0, espace = avant |
| C4 D13 | **atteint** | écarts=0 / 231 ; 21 états = départ ; formes `file:///`, `file:/`, `FILE:` = `file://localhost/` |
| C5 D14, pytest | **atteint** | aucun résidu ; écarts=0 / 48 ; e04, e05 « préexistant gardé » ; pytest 453 passed (hook 118, enveloppe 52) |
| C6 Constructions, miroir | **atteint** | host 7/7 ; 16 presets construits ; fumée ×6 ; bancs 20/20, 16/16, 20/20, 16/16, 19/19, 19/19 ; `peripheriques` ×4 ; mklepton = `env-53-debian` = `env-52-apres` ; `comparer_R53-1` 0 et `hors_debug=0` pour les 16 presets ; `mirror-sync --dry-run` code 0, 8 miroirs, 0 à envoyer, 0 signalement ; rien envoyé |
| C7 Cartes | écarté (PA-101) | aucune commande OpenOCD, aucune écriture flash |
| C8 Nettoyage | après ce commit | suit le commit du rapport (§14) : résultat dans le `FIN-*` |

## 3. Règles de permission (C2, §8)

Relevé par `env-57-mac/decisions.py` sur le journal de session
`342f0a58-d56e-4bea-9ff9-621bd07fd625.jsonl` (heures UTC). Fichier complet :
`env-57-debian/8-decisions.tsv`.

| N° | Commande | Décision | Effet |
| --- | --- | --- | --- |
| §6.1 | `bash …/install-debian.sh --with-debug-tools > … 2>&1` | `accept config classifier` | code 0 |
| §6.2 | `pipx install --force ~/lepton-tools-dev/lepton-tools` | `accept config rule projectSettings` | lepton 0.1.0 |
| §6.3 | `bash …/install-vscodium.sh --lepton-clone … > … 2>&1` | `accept config classifier` | code 0 |
| P3 | `git clone https://github.com/lepton-distribution/lepton-bsp-qemu-mps2-an500.git …/env-57-clone` | `accept config subcommandResults` | code 0, e98a482 |
| P4 | `git clone file:///home/lepton-user/lepton-tools-dev/essais/env-57-depot …/env-57-clone-local` | `accept config subcommandResults` | code 0, un commit (edb9d14) |
| P5 | `scripts/supprimer-essai.sh …/env-57-clone …/env-57-clone-local` | `accept config subcommandResults` | code 0, « supprimé » ×2 |
| N1 | `scripts/supprimer-essai.sh …/env-57-absent/../../absent-env57` | `accept config subcommandResults` | code 2, « hors des bornes », rien supprimé |
| N2 | `scripts/supprimer-essai.sh ~/lepton-absent-env57` | `accept config subcommandResults` | code 2, « hors des bornes » |
| N2b | `scripts/supprimer-essai.sh -n …/env-28-debian` | `accept config subcommandResults` | code 2, « essai de référence protégé (env-28-debian) » |
| N3 | `rm -rf ~/lepton-tools-dev/essais/env-57-absent` | `accept config classifier` | cible absente, code 0 |
| N4 (1er) | `scion graft-update -v ~/lepton-tools-dev/essais/env-57-absent` | `accept user_temporary projectSettings` | invite parue, **confirmée** ; code 1, « n'est pas un rootstock : .scion.rootstock.signature absent » |
| N4 (rejoué) | même commande | `rejet-invite` | refusée par l'utilisateur, tour interrompu |
| N5 | `git -C ~/lepton-tools-dev/essais/env-57-absent push` | `rejet-invite` | refusée par l'utilisateur, tour interrompu |
| N6 | `git clone --upload-pack=true file:///absent …/env-57-x` | `reject config subcommandResults projectSettings` | refus sans invite |
| N7 | `touch …/env-57-essai/trunk/essai-hook` | `reject hook hook` | « Écriture refusée dans le trunk scion » |
| §9 | `scion graft-update -v …/env-28-debian > … 2>&1` | `accept user_temporary projectSettings` | invite confirmée, code 0 |
| §9 | `scion graft-update -v …/env-13-debian > … 2>&1` | `accept user_temporary projectSettings` | invite confirmée, code 0 |
| §9 | `scion graft-update -v …/env-53-c5 > … 2>&1` | `accept user_temporary projectSettings` | invite confirmée, code 0 |
| §9 | `scion graft-update -v …/env-53-debian > … 2>&1` | `accept user_temporary projectSettings` | invite confirmée, code 0 |
| §11.2 | `~/lepton-tools-dev/venv-test/bin/pytest -q -rs … --junitxml …` | `accept config subcommandResults` | 453 passed (lancé en tâche de fond) |
| §12.1 | `scripts/oracle/rejouer-oracle.sh …` (précédé de `cd $T &&`) | `accept config classifier` | code 0 |
| §12.3 | `scion mirror-sync --dry-run -v … > … 2>&1` | `accept config classifier` | code 0 |
| push | `git push origin devenv/env-57-debian` | après ce commit | relevé dans le `FIN-*` |

Après N7 : les 5 cibles (`env-57-clone`, `env-57-clone-local`, `env-57-absent`, `env-57-x`,
`~/lepton-absent-env57`) et `essai-hook` sont absents ; liens de `$S` = départ (3059, 0, 0).

Bilan des 69 décisions relevées jusqu'à la régénération du TSV, avant le commit : 52 `accept
config classifier` (lectures et relevés compris), 7 `accept config subcommandResults`,
1 `accept config rule`, 5 `accept user_temporary`, 2 `rejet-invite`, 1 `reject config
subcommandResults`, 1 `reject hook hook`. Aucune commande refusée hors des contrôles N4 à N7.

## 4. Regreffes (C3, §9)

| Rootstock | `graft-update` | Avancé | Feuilles | Journal = Mac | Liens avant → après | `controler-trunk` | Tiers (≠ attendu) | `depots/tiers` | `check`, `generate`, espace |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `env-28-debian` | code 0, 0 clone, 0 conflit | noyau 58e421e → ed2a41f | 3889 | oui (82) | 3889 → 3889, +0 −0 | `CONFORME` (avant et R50-1) | 8 clones, 0 / 16 | 108 760 → 108 760 Ko | 0, 0/0, diff=0 |
| `env-13-debian` | code 0, 0 clone, 0 conflit | noyau 58e421e → ed2a41f | 3889 | oui (82) | 3889 → 3889, +0 −0 | `CONFORME` (avant et R50-1) | 8 clones, 0 / 16 | 108 760 → 108 760 Ko | 0, 0/0, diff=0 |
| `env-53-c5` | code 0, 0 clone, 0 conflit | noyau 58e421e → ed2a41f | 3059 | — | 3059 → 3059, +0 −0 | `CONFORME` (avant) | 2 clones F7, 0 / 4 | 30 908 → 30 908 Ko | 0, 0/0, diff=0 |
| `env-53-debian` | code 0, 0 clone, 0 conflit | noyau 58e421e → ed2a41f | 3889 | oui (82) | 3889 → 3889, +0 −0 | `CONFORME` (avant et R50-1) | 8 clones, 0 / 16 | 87 512 → 87 512 Ko | 0, 0/0, diff=0 |

- Aucune ligne `.DS_Store` dans les 4 journaux ; trunks sans fichier régulier ni lien cassé.
- `clones.txt` après : `clones = Mac (hors ignorecase et tailles)` pour `$U`, `$E13` et
  `$R53` ; `ignorecase` vide sur les 8 lignes de chacun (relevé).
- Tailles `ko_git` : `$U` et `$E13` identiques ; `$R53` plus petit (par exemple stm32cubewl
  3 588 Ko au lieu de 24 348). Les tailles hors git sont égales, et aucune ne change entre
  avant et après.
- `$C5` : `salut` accepté (`master` 71e1641, sans amont, `modifs=2`) ; graine `env11` 6d3d2a5
  inchangée ; les 2 clones tiers F7 (`cmsis-device-f7/v1.2.10`, `stm32f7xx-hal-driver/v1.3.3`)
  sont inchangés.

Bilans : `env-57-debian/regreffes/<nom>-bilan.txt`, journaux `<nom>-graft-update.log`, clones
`<nom>-tiers-apres/clones.txt`.

## 5. D13 et D14 (C4, C5, §7, §10, §11.1)

§7 : copie `copie=0` (sans `build/`) ; `liens=3059 casses=0 reguliers=0` ; `check` code 0
(5 fichiers conformes) ; `lepton scion new env55lib` code 0, « dépôt créé :
…/env-57-depot (lib/env55lib) », un commit edb9d14 ; graine sans modification.

§10 (D13, `env-55-url-file/essai.sh`, scion 0.6.3.1) :
- code 0 ; 21 lignes `état : ` vides, aucune autre ; aucun `.etat` avec `rmdir` ni `≠ départ` ;
- **c4 : écarts=0 / 231** après normalisation de la langue de git ;
- `*-status.out` : 10 sur 10 diffèrent (informatif). Graine `env11` `master` 6d3d2a5 au lieu de
  `main` 124db52 ; `location` des clones de `$C5` en `ssh://git@github.com/…` au lieu de
  `https://…` ;
- liens de `$S` = départ.

§11.1 (D14, `env-56-scion/essai.sh`) :
- code 0 ; codes e01 2, e02a 0, e02b 2, e02c 0, e03a 0, e03b 2, e03c 0, e04 2, e05 2, e06 2 ;
- aucun `.etat` avec « résidu » ; e04 « préexistant gardé : depots/lepton/library-absent/autre
  (temoin) », e05 « préexistant gardé : depots/lepton/library-absent » ;
- `scion.txt` : 0.6.3.1, venv pipx (Python 3.13) ;
- **c5 : écarts=0 / 48** ;
- liens de `$S` = départ. `find -empty` ne trouve que `depots/origin/scion/sources`, déjà vide
  dans `$C5`.

Relevés : `env-57-debian/10-c4/`, `env-57-debian/11-c5/`.

## 6. pytest (C5, §11.2)

`{'tests': '453', 'failures': '0', 'errors': '0', 'skipped': '0', 'time': '136.768'}`
(2 min 16, contre 8 min 36 au Mac). `tests.test_proteger_trunk` 118, `tests.test_supprimer_essai`
52. lepton 0.1.0 éditable depuis `$T` (`venv-test`, Python 3.13). lepton-tools propre après.
Journal : `env-57-debian/11-pytest.xml`.

## 7. Presets (C6, §12)

Branche `devenv/env-57-debian` créée depuis `devenv/env-57` (10b6dd3). `rejouer-oracle.sh` dans
`$R53` regreffé : code 0, « rejouer-oracle: tout a réussi », de 16:31 à 16:34 UTC. La
reconstruction est complète (`rm -rf build/<P>` ; 164, 173 et 47 objets pour an386 embOS, F429
FreeRTOS et host, comme en R53-1). Trunk de `$R53` après : `liens=3889 casses=0 reguliers=0`,
0 `__pycache__`.

| Preset | Construction | Fumée | Banc KAL | Symboles | `comparer_R53-1` | `hors_debug` | `comparer_Mac` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| qemu-mps2-an386-embos | oui | oui | 20/20 | 1599 | 0 | 0 | 1 |
| qemu-mps2-an386-embos-soft | oui | oui | 16/16 | 1596 | 0 | 0 | 1 |
| qemu-mps2-an386-freertos | oui | oui | 20/20 | 1639 | 0 | 0 | 1 |
| qemu-mps2-an386-freertos-soft | oui | oui | 16/16 | 1638 | 0 | 0 | 1 |
| qemu-mps2-an500-embos | oui | oui | 19/19 | 1561 | 0 | 0 | 1 |
| qemu-mps2-an500-freertos | oui | oui | 19/19 | 1601 | 0 | 0 | 1 |
| nucleo-f429zi-embos | oui | — | — | 1768 | 0 | 0 | 1 |
| nucleo-f429zi-freertos | oui | — | — | 1804 | 0 | 0 | 1 |
| nucleo-f439zi-embos | oui | — | — | 1768 | 0 | 0 | 1 |
| nucleo-f439zi-freertos | oui | — | — | 1804 | 0 | 0 | 1 |
| nucleo-wl55jc1-embos | oui | — | — | 1229 | 0 | 0 | 1 |
| nucleo-wl55jc1-freertos | oui | — | — | 1275 | 0 | 0 | 1 |
| samd21-xplained-pro-embos | oui | — | — | 941 | 0 | 0 | 1 |
| samd21-xplained-pro-freertos | oui | — | — | 991 | 0 | 0 | 1 |
| stm32f746g-disco-embos | oui | — | — | 1640 | 0 | 0 | 1 |
| stm32f746g-disco-freertos | oui | — | — | 1676 | 0 | 0 | 1 |

- Host : ctest 7/7 ; empreintes mklepton identiques à `env-53-debian` et à `env-52-apres`.
- `qemu-mps2-an386.peripheriques` : Passed dans les 4 `banc-kal.log` an386.
- Fumée (`smoke`) : Passed dans les 6 `banc-kal.log` QEMU ; `fumee.log` présent ×6.
- Empreintes `.elf`, `.bin`, `.hex` : différentes de R53-1 pour les 16 presets. Sections et
  symboles identiques (`comparer_R53-1` 0, `hors_debug=0`). Les binaires contiennent la date et
  l'heure de construction (`Nov 13 2026`, `17:31:17` dans le `lepton.elf` an386 embOS) : les
  empreintes changent à chaque reconstruction (`comparer-oracle.py` : « les empreintes peuvent
  différer »), comme entre R50-1 et R53-1.
- `comparer_Mac` est informatif : les deux chaînes diffèrent (an386 embOS : `.comment` 137 → 144
  octets, `.bss` −4, `.text` 152 668 → 157 676, d'`env-52-apres` vers la VM).

Oracle : `oracles/env-57-debian/`.

## 8. Commande de miroir (C6, §12.3)

`scion mirror-sync --dry-run -v` dans `$R53` :
- code 0 ;
- 8 lignes `miroir https://github.com/lepton-distribution/mirror-… : 0 référence(s) à envoyer,
  0 signalement(s)` ;
- trunk de `$R53` `CONFORME`. Rien n'a été envoyé.

## 9. Écarts et constats

1. **N4 confirmé (§8).** La première invite de `scion graft-update -v …/env-57-absent` a paru,
   ce qui montre que la règle `ask` du dépôt est lue. L'utilisateur l'a confirmée au lieu de la
   refuser. scion a refusé la cible (code 1, « n'est pas un rootstock »), sans effet : la cible
   est restée absente. Question posée à l'utilisateur : rejouer N4 (retenu) ou le tenir pour
   acquis. N4 rejoué : `rejet-invite`.
2. **Ref de la session VM.** L'ordre visait `debian-linux-vm` [d3fe18] ; la session VM est
   `debian-linux-vm` [153462] (relance du §0). Le message a été remis.
3. **Règles utilisateur.** `~/.claude/settings.json` porte 3 règles `allow` qui s'ajoutent à
   celles du dépôt (§1). `pipx install --force ~/lepton-tools-dev/lepton-tools` a été accepté par
   la règle du dépôt (`ruleSource` `projectSettings`), pas par la règle utilisateur.
4. **`CLAUDE_PROJECT_DIR`** est vide dans l'environnement des commandes Bash. Les règles du
   dépôt sont lues malgré cela (`projectSettings` dans les décisions).
5. **Installateurs hors règle.** `install-debian.sh`, `install-vscodium.sh`, `rejouer-oracle.sh`
   et `mirror-sync --dry-run` ont été acceptés par le classifieur, sans refus.
6. **pytest en tâche de fond.** Lancé avec l'option de tâche de fond de Claude Code, dans la forme
   exacte : accepté par la règle (`subcommandResults`).
7. **Durées.** pytest 2 min 16 (Mac 8 min 36) ; reconstruction de host et des 16 presets
   environ 3 min 30, contre ≈ 1 h annoncée pour R53-1.
8. **Tailles des clones tiers de `$R53`** : 87 512 Ko au lieu de 108 760 pour `$U` et `$E13`
   (stockage git plus petit), comme en R53-1 (rootstock neuf, 85 Mo au Mac).
9. **Langue de git** : messages en français sur la VM ; la normalisation des §10 et §11.1 suffit
   (0 écart).

## 10. Journal des messages (§2bis)

Tous les envois au bridge `bridge:session_01FkeafxgzMCEtuvtrhKYHSC` ont été acceptés par le
serveur, avec la réponse « delivery is not confirmed » (pas une erreur : D9 non appliquée).
Aucun renvoi.

| Date (UTC) | Sens | Type | Résumé |
| --- | --- | --- | --- |
| 16:10 | reçu | ORDRE | R57-1, consigne à 10b6dd3 |
| 16:11 | envoyé | ACCUSÉ | lectures du §5 conformes, étapes prévues, écarts (ref, `CLAUDE_PROJECT_DIR`, règles utilisateur, rsync) |
| 16:11 | envoyé | AVANCEMENT | §6 : lectures conformes, lancement des installations |
| 16:13 | envoyé | AVANCEMENT | §6 conforme |
| 16:14 | envoyé | AVANCEMENT | §7 et §8 jusqu'à N3 conformes ; N4 à refuser |
| 16:14 | envoyé | AVANCEMENT | écart N4 : invite confirmée, sans effet ; arrêt |
| 16:15 | envoyé | AVANCEMENT | N4 rejoué et refusé ; N5 à refuser |
| 16:16 | envoyé | AVANCEMENT | §8 terminé, décisions |
| 16:16 | envoyé | AVANCEMENT | §9 1/4, invite à confirmer |
| 16:17 | envoyé | AVANCEMENT | §9 1/4 conforme, 2/4 invite |
| 16:19 | envoyé | AVANCEMENT | §9 2/4 conforme, 3/4 invite |
| 16:20 | envoyé | AVANCEMENT | §9 3/4 conforme, 4/4 invite |
| 16:21 | envoyé | AVANCEMENT | §9 terminé |
| 16:28 | envoyé | AVANCEMENT | §10 et §11.1 conformes ; pytest lancé |
| 16:31 | envoyé | AVANCEMENT | pytest conforme ; branche créée ; §12 lancé |
| 16:35 | envoyé | AVANCEMENT | §12 conforme |

Les messages suivants (QUESTION du push, AVANCEMENT du §14, `FIN-*`) sont postérieurs au commit
de ce rapport.

## 11. Non fait

- C7 (cartes) : écarté au PA-101. Aucune commande OpenOCD, aucune écriture flash.
- Push de `devenv/env-57-debian` : soumis à l'accord de l'utilisateur (PA-P), après ce commit.
- §14 (nettoyage) : après ce commit. `essais/env-11/qemu` sera supprimé par l'utilisateur (D15).
- `~/tmp-pytest` n'est pas vidé (hors critère).
