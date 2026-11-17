# ENV-61 — Validation Debian groupée (ENV-58 à ENV-60) — 2026-11-17

Session VM `debian-linux-vm`, ordre `R61-1` de la session Mac `validate-env-58-60-debian`
(bridge `bridge:session_01Fkeafydrc3KMBruhxNKjUQ`). Consigne `doc/devenv/consignes/env-61-debian.md`
à ac3b913 (sha256 `5f0cdf6f…2798`, égal à l'ordre). Répertoire de travail
`/home/lepton-user/lepton-tools-dev/lepton-tools` (`$T`), mode auto, Remote Control. Journaux :
`~/env-61-journaux/` sur la VM. Rootstocks regreffés : `essais/env-28-debian` (`$U`),
`essais/env-13-debian` (`$E13`), `essais/env-53-c5` (`$C5`) et `essais/env-53-debian` (`$R53`).
Copie d'essai `essais/env-61-essai` (`$S`) ; dépôts `essais/env-61-depot59` (`$D59`) et
`essais/env-61-depot60` (`$D60`) ; clone `essais/env-61-seed-scions` (`$SS`) ; fixture
`essais/env-61-fixture/f56` (`$FX`).

Résultat : C1 à C6 atteints, avec trois écarts. C7 est écarté (PA-109). C8 vient après le commit
de ce rapport (§14 de la consigne). Écarts :
- **§6 (consigne)** : le contrôle de la correction D17 cherchait le texte de l'ancien code et
  donnait `False`. Le contrôle corrigé donne `True` (RÉPONSE R61-1, option 1).
- **§8** : la première invite d'A1 a été confirmée au lieu d'être refusée, sans effet. A1 a été
  rejoué et refusé. U3 a été décidé par le classifieur, et non par la règle utilisateur.
- **§11.2 (comparaison)** : 4 écarts sur 76 dans la fixture (espace insécable du git français,
  `/home` contre `/Users`). Ils sont retenus comme écarts de comparaison, sur décision de
  l'utilisateur (option 1).

## 1. Hôte, versions et session (§5, §6)

| Élément | Valeur |
| --- | --- |
| Hôte | Debian 13.7, Linux 6.12.107+deb13-amd64 x86_64, `lepton-user`, git 2.47.3 |
| Espace libre | `/home` 17 Go ; `/tmp` 690 Mo |
| Claude Code | 2.1.326 (R57-1 : 2.1.323). Répertoire de travail `$T`. `CLAUDE_PROJECT_DIR` vide dans l'environnement Bash. Session non relancée après le §0 (§9, écart 1) |
| Réglages du dépôt | `.claude/settings.json` b01ad557…d235, `proteger-trunk.py` 04572df6…6909 (G2), `supprimer-essai.sh` 04323a00…0e15 : = Mac. Aucun `settings.local.json` (ni utilisateur, ni dépôt) |
| Réglages utilisateur | `~/.claude/settings.json`, 3903 o, daté du 17 nov. 16:44 (10 nov. en R57-1) ; bloc `permissions.allow` = PA-103 (§3.1) |
| Chaîne APT | arm-none-eabi-gcc `15:14.2.rel1-1` (14.2.1 20241119), cmake 3.31.6, ninja 1.12.1, QEMU 10.0.13 (`1:10.0.13+ds-0+deb13u1`), Python 3.13.5 : = R57-1 |
| Outils | `shasum`, `realpath`, `tar` présents ; `~/tmp-pytest`, `venv-test/bin/pytest` présents ; `id inconnu59` : utilisateur inexistant |
| scion | 0.6.3.1 → **0.6.3.2** par `install-debian.sh --with-debug-tools` (`SCION_REF` par défaut, `git+https://github.com/lepton-distribution/seed.scions.git@0.6.3.2`), code 0 |
| lepton | `pipx install --force ~/lepton-tools-dev/lepton-tools` : « installed package lepton 0.1.0, installed using Python 3.13.5 » ; `lepton 0.1.0`, `scion 0.6.3.2 (requis ≥ 0.6.2.0)` |
| Correction D17 | contrôle de la consigne : `False` (§9, écart 2) ; contrôle corrigé : `True` ; `seed.py` installé identique à `$T/lepton/seed.py` |
| VSCodium | 1.135.06055 ; `install-vscodium.sh` code 0, `changements 0` |
| Extensions | `lepton-distribution.lepton@0.5.2`, `vadimcn.vscode-lldb@1.12.3`, `mcu-debug.rtos-views@0.0.16`, `mcu-debug.peripheral-viewer@1.6.4` |
| Clone noyau `$K` | propre, `master` ed2a41f → **dfc960b** (avance rapide, 5 fichiers hors `scion/`) ; `SCION_REF="${SCION_REF:-0.6.3.2}"` |
| lepton-tools | `devenv/env-61` = `origin/devenv/env-61` = ac3b913, propre ; `SCION_REF="0.6.3.2"` (`install-vscodium.sh`) ; `SCION_MIN_VERSION = (0, 6, 2, 0)` ; `extension/dist/lepton-0.5.2.vsix` présent |

`git ls-remote` : « têtes publiées = Mac » (diff vide avec `env-61-mac/ls-remote-mac.txt`, hors
lepton-tools). lepton-tools `main` 7018302 ; seed.scions tag `0.6.3.2` 08a1460 (`master`
975caf6) ; graine 15740f9 ; noyau dfc960b ; 12 greffons et 8 miroirs = Mac.

État de départ (§5) :
- `$U` et `$E13`, identiques :
  - graine 15740f9 sur `original-tree`, amont réglé, `modifs=0` ; 23 entrées ;
  - 13 clones sur `master`, amont `origin/master`, `modifs=0` ; noyau ed2a41f ;
  - `liens=3889 casses=0 reguliers=0` ; 8 clones tiers, 108 760 Ko ;
- `$C5` :
  - graine `env11` 6d3d2a5 (`master`, sans amont, `modifs=0`) ; 5 entrées ;
  - `salut` 71e1641, sans amont, `modifs=2` ;
  - an386 10a8889, famille QEMU 3954357, famille F7 12280a5, noyau ed2a41f, amont réglé ;
  - `liens=3059 casses=0 reguliers=0` ; 2 clones tiers F7, 30 908 Ko ;
- `$R53` et `~/env-57-journaux` présents ; `essais/env-11` absent ; aucun des chemins du §5
  n'existait.

## 2. Critères (§15)

| Critère | Résultat | Constat |
| --- | --- | --- |
| C1 Versions | **atteint** | ls-remote = Mac ; réglages, hook, enveloppe = Mac ; Claude Code 2.1.326 ; git 2.47.3 ; scion 0.6.3.2 par `install-debian.sh` (défaut `SCION_REF`) ; lepton `pipx` code 0, `scion 0.6.3.2 (requis ≥ 0.6.2.0)` ; correction D17 présente (contrôle corrigé, écart 2) ; extension 0.5.2, `changements 0` ; chaîne = R57-1 |
| C2 D19, D20, G2 | **atteint, avec écarts** | réglages utilisateur relus en entier, `allow` = PA-103 ; U1 et U2 `subcommandResults`, U3 `classifier` (écart 4), sans effet ; F1, F3, F6 `subcommandResults`, F2, F7 `classifier` ; A1 invite par la règle `ask`, A2 et A3 invites (hook G2), toutes refusées (`rejet-invite`) ; H1 `reject hook` ; `pipx install --force` par la règle du dépôt ; `graft-update` ×4 sur invite confirmée ; `git clone` de seed.scions et pytest par la règle ; aucune cible créée ni supprimée à tort. Écart : 1re invite d'A1 confirmée (écart 3) |
| C3 Regreffes | **atteint** | `$U`, `$E13`, `$R53` : code 0, seul le noyau avance (ed2a41f → dfc960b), 0 clone, journal = Mac, 3889 liens inchangés, `CONFORME` (avant et R50-1), tiers 0 / 16, `clones = Mac`, `check` 0, espace = avant. `$C5` : noyau seul, 3059 liens inchangés, `CONFORME`, tiers 0 / 4, `check` 0, espace = avant |
| C4 D17 | **atteint** | `classer = Mac` ; 66 états = départ ; écarts=0 / 528 |
| C5 D18, pytest | **atteint, avec écart de comparaison** | §11.1 : l01 à l03 code 2, aucun clone laissé, écarts=0 / 15. §11.2 : écarts=4 / 76 bruts, 0 / 76 après neutralisation de l'espace insécable et de `/home` (écart 5, option 1 de l'utilisateur) ; f06 code 2, sans clone. §11.3 : 508 passed |
| C6 Constructions, miroir | **atteint** | host 7/7 ; 16 presets construits ; fumée ×6 ; bancs 20/20, 16/16, 20/20, 16/16, 19/19, 19/19 ; `peripheriques` ×4 ; mklepton = `env-57-debian` = `env-52-apres` ; `comparer_R57-1` 0 et `hors_debug=0` pour les 16 presets ; `mirror-sync --dry-run` code 0, 8 miroirs, 0 à envoyer, 0 signalement ; rien envoyé |
| C7 Cartes | écarté (PA-109) | aucune commande OpenOCD, aucune écriture flash |
| C8 Nettoyage | après ce commit | suit le commit du rapport (§14) : résultat dans le `FIN-*` |

## 3. Règles de permission (C2, §8)

### 3.1 D19 : `~/.claude/settings.json`

Sortie entière de `python3 -m json.tool ~/.claude/settings.json` :
`env-61-debian/settings-utilisateur.json`. Le bloc `permissions` est exactement celui du PA-103 :
```json
"permissions": {
    "allow": [
        "Bash(pipx install:*)",
        "Bash(git clone * https://github.com/lepton-distribution/*)",
        "Bash(python3 -m unittest discover *)"
    ]
}
```
Il n'y a ni `ask`, ni `deny`, ni `defaultMode`. Autres clés relevées :
- `modelSettings` : `claude-opus-5-5`, `effortLevel` `high` ;
- `tui` `fullscreen`, `theme` `dark`, `agentPushNotifEnabled` `true` ;
- `autoMode`, avec deux sous-clés :
  - `soft_deny` : `$defaults`, plus 3 entrées `seed-update`, `graft-update` et `git push` propres
    à `/home/lepton-user/Development/lepton-migration-development` ;
  - `environment` : description de l'environnement pour le classifieur.

La date du fichier (17 nov. 16:44 locale) suit la commande `/model` que l'utilisateur a lancée
dans cette session (« saved as your default »). Le bloc `permissions` n'a pas changé.

### 3.2 Décisions

Relevé par `env-57-mac/decisions.py` sur le journal de session
`3498db03-cbec-4248-9c02-7e12b5aab1d2.jsonl` (heures UTC). Fichier complet :
`env-61-debian/15-decisions.tsv`.

| N° | Commande | Décision | Effet |
| --- | --- | --- | --- |
| §6.1 | `bash …/install-debian.sh --with-debug-tools > … 2>&1; echo …` | `accept config classifier` | code 0 |
| §6.2 | `pipx install --force ~/lepton-tools-dev/lepton-tools` | `accept config rule projectSettings` | lepton 0.1.0 |
| §6.3 | `bash …/install-vscodium.sh --lepton-clone … > … 2>&1; echo …` | `accept config classifier` | code 0 |
| U1 | `pipx install ~/lepton-tools-dev/essais/env-61-absent` | `accept config subcommandResults` | code 1, « Unable to parse package spec », rien installé |
| U2 | `git clone --depth 1 https://github.com/lepton-distribution/env-61-absent.git …/env-61-absent` | `accept config subcommandResults` | code 128, « could not read Username » (dépôt inexistant), cible absente |
| U3 | `python3 -m unittest discover -s ~/lepton-tools-dev/essais/env-61-absent` | `accept config classifier` | code 1, `ImportError: Start directory is not importable` ; **règle utilisateur non appliquée** (écart 4) |
| F1 | `P` | `accept config subcommandResults` | 1 passed |
| F2 | `P > ~/env-61-journaux/8-f2.log` | `accept config classifier` | 1 passed (journal) |
| F3 | `P 2>&1` | `accept config subcommandResults` | 1 passed |
| F6 | `P` avec `--junitxml ~/env-61-journaux/8-f6.xml` | `accept config subcommandResults` | 1 passed |
| F7 | `P; echo "code=$?"` | `accept config classifier` | 1 passed, code=0 |
| A1 (1er) | `scion graft-update -v ~/lepton-tools-dev/essais/env-61-absent` | `accept user_temporary projectSettings` | invite parue, **confirmée** ; code 1, « n'est pas un rootstock : .scion.rootstock.signature absent » |
| A1 (rejoué) | même commande | `rejet-invite` | refusée par l'utilisateur, tour interrompu |
| A2 | `bash doc/devenv/rapports/env-58-formes/ask-script.sh ~/lepton-tools-dev/essais/env-61-absent` | `rejet-invite` | invite (hook G2), refusée par l'utilisateur |
| A3 | `bash -c 'scion graft-update -v ~/lepton-tools-dev/essais/env-61-absent'` | `rejet-invite` | invite (hook G2), refusée par l'utilisateur |
| H1 | `touch ~/lepton-tools-dev/essais/env-61-essai/trunk/essai-hook` | `reject hook hook` | « Écriture refusée dans le trunk scion » |
| §9 | `scion graft-update -v …/env-28-debian > … 2>&1; echo …` | `accept user_temporary projectSettings` | invite confirmée, code 0 |
| §9 | `scion graft-update -v …/env-13-debian > … 2>&1; echo …` | `accept user_temporary projectSettings` | invite confirmée, code 0 |
| §9 | `scion graft-update -v …/env-53-c5 > … 2>&1; echo …` | `accept user_temporary projectSettings` | invite confirmée, code 0 |
| §9 | `scion graft-update -v …/env-53-debian > … 2>&1; echo …` | `accept user_temporary projectSettings` | invite confirmée, code 0 |
| §11.2 | `git clone https://github.com/lepton-distribution/seed.scions.git …/env-61-seed-scions` | `accept config subcommandResults` | code 0 |
| §11.2 | `git -C …/env-61-seed-scions switch --detach 0.6.3.2` | `accept config classifier` | 08a1460 |
| §11.3 | `~/lepton-tools-dev/venv-test/bin/pytest -q -rs … --junitxml …` | `accept config subcommandResults` | 508 passed |
| §12.1 | `git switch -c devenv/env-61-debian devenv/env-61` (précédé de `cd $T &&`) | `accept config classifier` | branche créée |
| §12.1 | `scripts/oracle/rejouer-oracle.sh …` | `accept config classifier` | code 0 |
| §12.3 | `scion mirror-sync --dry-run -v … > … 2>&1; echo …` | `accept config classifier` | code 0 |
| push | `git push origin devenv/env-61-debian` | après ce commit | relevé dans le `FIN-*` |

`P` = `~/lepton-tools-dev/venv-test/bin/pytest -q -p no:cacheprovider --basetemp
~/tmp-pytest/env-61-f tests/test_proteger_trunk.py::test_entree_illisible`, lancé depuis `$T`.

Motif des invites d'A2 et d'A3 : non relevé. La session ne voit pas le texte de l'invite, et
l'utilisateur ne l'a pas communiqué. Le journal ne garde que le refus.

Après H1 : `env-61-absent` et `essai-hook` sont absents ; aucun paquet `env-61` dans `pipx` ;
liens de `$S` = départ (3059, 0, 0).

Les 68 décisions relevées jusqu'à la régénération du TSV, avant le commit, se répartissent ainsi
(lectures et relevés compris) :
- 51 `accept config classifier` ;
- 7 `accept config subcommandResults` ;
- 1 `accept config rule` ;
- 5 `accept user_temporary` ;
- 3 `rejet-invite` ;
- 1 `reject hook hook`.

Aucune décision `user_permanent`. Aucune commande refusée hors des contrôles A1 à A3 et H1.

## 4. Regreffes (C3, §9)

| Rootstock | `graft-update` | Avancé | Feuilles | Journal = Mac | Liens avant → après | `controler-trunk` | Tiers (≠ attendu) | `depots/tiers` | `check`, `generate`, espace |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `env-28-debian` | code 0, 0 clone, 0 conflit | noyau ed2a41f → dfc960b | 3889 | oui | 3889 → 3889, +0 −0 | `CONFORME` (avant et R50-1) | 8 clones, 0 / 16 | 108 760 → 108 760 Ko | 0, 0/0, diff=0 |
| `env-13-debian` | code 0, 0 clone, 0 conflit | noyau ed2a41f → dfc960b | 3889 | oui | 3889 → 3889, +0 −0 | `CONFORME` (avant et R50-1) | 8 clones, 0 / 16 | 108 760 → 108 760 Ko | 0, 0/0, diff=0 |
| `env-53-c5` | code 0, 0 clone, 0 conflit | noyau ed2a41f → dfc960b | 3059 | — | 3059 → 3059, +0 −0 | `CONFORME` (avant) | 2 clones F7, 0 / 4 | 30 908 → 30 908 Ko | 0, 0/0, diff=0 |
| `env-53-debian` | code 0, 0 clone, 0 conflit | noyau ed2a41f → dfc960b | 3889 | oui | 3889 → 3889, +0 −0 | `CONFORME` (avant et R50-1) | 8 clones, 0 / 16 | 87 512 → 87 512 Ko | 0, 0/0, diff=0 |

- Les 4 journaux n'ont aucune ligne `.DS_Store`. Les trunks n'ont ni fichier régulier ni lien
  cassé.
- `clones.txt` après :
  - `clones = Mac (hors ignorecase et tailles)` pour `$U`, `$E13` et `$R53` ;
  - `ignorecase` vide sur les 26 lignes des 4 rootstocks.
- Tailles `ko_git` :
  - `$U` et `$E13` identiques ;
  - `$R53` plus petit (stm32cubewl 3 588 Ko au lieu de 24 348), comme en R57-1 ;
  - aucune ne change entre avant et après.
- `$C5` :
  - `salut` accepté (`master` 71e1641, sans amont, `modifs=2`) ;
  - graine `env11` 6d3d2a5 inchangée ;
  - noyau dfc960b ;
  - les 2 clones tiers F7 (`cmsis-device-f7/v1.2.10`, `stm32f7xx-hal-driver/v1.3.3`) sont
    inchangés.

Bilans : `env-61-debian/regreffes/<nom>-bilan.txt` ; journaux `<nom>-graft-update.log` ;
clones `<nom>-tiers-apres/clones.txt`.

## 5. D17 et D18 (C4, C5, §7, §10, §11.1, §11.2)

§7 :
- copie `copie=0` (sans `build/`) ; `liens=3059 casses=0 reguliers=0` ;
- `check` code 0 (5 fichiers conformes) ;
- `lepton scion new env59lib`, code 0, « dépôt créé : …/env-61-depot59 (lib/env59lib) », commit
  7e2812f ;
- `lepton scion new env60lib`, code 0, « …/env-61-depot60 (lib/env60lib) », commit c61b3dc ;
- graine sans modification (0).

§10 (D17, `env-59-tilde/classer.py` et `essai.sh`) :
- `classer.py` code 0, sans erreur ; `classer = Mac` (42 formes) ;
- `essai.sh` code 0 : 66 lignes `état : ` vides, aucune autre ;
- **c4 : écarts=0 / 528** ;
- `*-status.out` : différents (informatif ; p01, p02-i, p03-i en tête) ;
- 547 relevés, contre 548 au Mac (`classer.tsv` est rangé à part sur la VM) ;
- liens de `$S` = départ.

§11.1 (D18, `env-60-scion/essai.sh`) :
- l01 (`@scion`), l02 et l03 (`@nope`) : code 2. Message : « échec de « git clone -b … » (code
  128) : fatal: Remote branch … not found in upstream origin », puis « ajout … annulé (graine et
  trunk restaurés) » ;
- les 3 `état : ` sont vides ; `library-env60lib` est absent ;
- `scion.txt` : `<HOME>/.local/bin/scion`, 0.6.3.2 ;
- **c5 : écarts=0 / 15** ;
- liens de `$S` = départ.

`fr()` n'a ramené aucune ligne aux §10 et §11.1, car les deux `essai.sh` exportent `LC_ALL=C`.

§11.2 (fixture d'ENV-56, `env-56-scion/fixture.py`) :
- `$SS` cloné, puis `switch --detach 0.6.3.2` : 08a1460, propre ; `fixture.py` code 0 ;
- tableau des 15 cas : f01 à f07, f09b, f09c et f10 en code 2 ; f08, f11, f12a et f12b en
  code 1 ; f09a en code 0. Les chemins créés concordent avec le Mac ;
- f06 : code 2, « échec de « git clone -b nope … » (code 128) », `.depots` vide (0 octet,
  aucun clone) ;
- **fixture56 : écarts=4 / 76** bruts, détaillés à l'écart 5 (§9) ; diffs bruts dans
  `env-61-debian/11-fixture56-ecarts.diff`. Après neutralisation, les 4 fichiers sont identiques
  au Mac : **0 / 76**.

Relevés : `env-61-debian/10-classer.tsv`, `10-c4/`, `11-c5/`, `11-fixture56/`.

## 6. pytest (C5, §11.3)

`{'tests': '508', 'failures': '0', 'errors': '0', 'skipped': '0', 'time': '174.233'}`, soit
2 min 54 (Mac : 8 min 59). Par module :
- `test_proteger_trunk` 118 ;
- `test_garde_ask` 46 ;
- `test_supprimer_essai` 52 ;
- `test_milestone3` 43.

lepton 0.1.0 est éditable depuis `$T` (`venv-test`, Python 3.13). lepton-tools est propre
après. Journal : `env-61-debian/11-pytest.xml`.

## 7. Presets (C6, §12)

La branche `devenv/env-61-debian` est créée depuis `devenv/env-61` (ac3b913).
`rejouer-oracle.sh` dans `$R53` regreffé : code 0, « rejouer-oracle: tout a réussi », d'environ
16:25 à 16:29 UTC. Trunk de `$R53` après : `liens=3889 casses=0 reguliers=0`, 0 `__pycache__`.

| Preset | Construction | Fumée | Banc KAL | Symboles | `comparer_R57-1` | `hors_debug` | `comparer_Mac` |
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

- Host : ctest 7/7 ; empreintes mklepton identiques à `env-57-debian` et à `env-52-apres`.
- `qemu-mps2-an386.peripheriques` : Passed dans les 4 `banc-kal.log` an386.
- Fumée (`smoke`) : Passed dans les 6 `banc-kal.log` QEMU ; `fumee.log` présent ×6.
- Les nombres de symboles sont égaux à ceux de R57-1. Sections et symboles sont identiques
  (`comparer_R57-1` 0, `hors_debug=0`) : aucun binaire n'a changé, à la date de construction
  près.
- `comparer_Mac` est informatif : les deux chaînes diffèrent.

Bilan : `env-61-debian/12-bilan.txt`. Oracle : `oracles/env-61-debian/`.

## 8. Commande de miroir (C6, §12.3)

`scion mirror-sync --dry-run -v` dans `$R53` :
- code 0 ;
- 8 lignes `miroir https://github.com/lepton-distribution/mirror-… : 0 référence(s) à envoyer,
  0 signalement(s)` ;
- trunk de `$R53` `CONFORME`. Rien n'a été envoyé.

## 9. Écarts et constats

1. **Session non relancée après le §0.**
   - La session `debian-linux-vm` a démarré avant le switch, sur `devenv/env-57-debian`
     (6df0de1). L'utilisateur a ensuite fait le switch vers `devenv/env-61`, sans fermer ni
     rouvrir la session.
   - `.claude/settings.json` a la même empreinte sur les deux branches, et le hook est relu à
     chaque appel. Les décisions montrent que les règles du dépôt ont été appliquées : `rule
     projectSettings`, invites `ask`, hook G2.
   - Signalé dans l'ACCUSÉ.
2. **Contrôle D17 de la consigne (§6).**
   - Le contrôle `"expanduser().resolve()" in inspect.getsource(s.parse_location)` donne
     `False`.
   - Depuis 74c9c97, `parse_location` écrit la correction en deux lignes :
     `expanded = Path(loc).expanduser()` (avec `RuntimeError` → `LeptonError`), puis
     `local = expanded.resolve()`, et l'indice emploie `file://localhost{local}@{ver}`. Le texte
     cherché n'existe que dans l'ancien code (`env-59-tilde/avant/p19.err:12`).
   - QUESTION R61-1, puis RÉPONSE R61-1 (option 1, décision de l'utilisateur). Contrôle
     retenu : `seed.py` installé identique à `$T/lepton/seed.py`, et
     `"local = expanded.resolve()" in src and "file://localhost{local}" in src` → `True`
     (`env-61-debian/6-controle-d17.txt`).
   - C'est un écart de la consigne, pas de l'installation. Le §10 fait foi pour C4.
3. **A1 confirmé (§8).**
   - La première invite d'A1 est apparue : la règle `ask` du dépôt est bien lue. L'utilisateur
     l'a confirmée au lieu de la refuser.
   - scion a refusé la cible (code 1, « n'est pas un rootstock »), sans effet.
   - À la demande de l'utilisateur, A1 a été rejoué et refusé (`rejet-invite`), puis A2 et A3
     ont été refusés à leur tour.
4. **U3 par le classifieur.**
   - `python3 -m unittest discover -s ~/lepton-tools-dev/essais/env-61-absent` a été accepté
     par le classifieur. La règle utilisateur `Bash(python3 -m unittest discover *)` n'a pas été
     appliquée.
   - U1 et U2 ont été acceptés par `subcommandResults`. Aucune décision ne porte
     `ruleSource userSettings`.
   - Relevé sans arrêt (§8.3).
5. **Fixture 56, 4 écarts de comparaison (§11.2).**
   - `f05.err` et `f06.err` : `fixture.py` ne fixe pas `LC_ALL`. Le git 2.47.3 en français écrit
     « fatal » suivi d'une **espace insécable** (U+00A0) puis de « : La branche distante nope
     n'a pas été trouvée dans le dépôt amont… ». Le motif de `fr()` n'admet qu'une espace
     ordinaire, si bien que la ligne n'est pas ramenée.
   - `f12a.depots` et `f12b.depots`, ligne 3 : `depots/.mirrors/localhost/home` sur la VM,
     `…/Users` au Mac. Le miroir est rangé sous le chemin absolu de la base, et `<B>` ne
     normalise pas ce premier segment.
   - Avec la variante à espace insécable et `/home` → `/Users`, les 4 fichiers sont égaux au
     Mac.
   - Le comportement D18 est conforme. L'utilisateur a choisi l'option 1 : écart de
     comparaison, poursuite.
6. **Réglages utilisateur modifiés hors permissions.** Voir §3.1 : `modelSettings` et le reste
   des clés, avec la date du 17 nov. Le bloc `permissions` est inchangé.
7. **`CLAUDE_PROJECT_DIR`** est vide dans l'environnement des commandes Bash. Les règles du
   dépôt sont lues malgré cela, comme en R57-1.
8. **Durées.** pytest 2 min 54 (Mac 8 min 59) ; reconstruction de host et des 16 presets
   environ 4 min.

## 10. Journal des messages (§2bis)

Tous les envois au bridge `bridge:session_01Fkeafydrc3KMBruhxNKjUQ` ont été acceptés par le
serveur, avec la réponse « delivery is not confirmed », qui n'est pas une erreur (D9 non
appliquée). Aucun renvoi.

| Heure (UTC) | Sens | Type | Résumé |
| --- | --- | --- | --- |
| 15:49 | reçu | ORDRE | R61-1, consigne à ac3b913 |
| 15:51 | envoyé | ACCUSÉ | lectures du §5 conformes, étapes prévues ; écart : session non relancée après le §0 |
| 15:51 | envoyé | AVANCEMENT | §6 : contrôles conformes, lancement des installations |
| 15:53 | envoyé | QUESTION | §6 : contrôle D17 `False`, correction installée ; options |
| 15:55 | reçu | RÉPONSE | option 1 (décision de l'utilisateur), contrôle corrigé, arrêt levé |
| 15:56 | envoyé | AVANCEMENT | §7 et §8.1-8.2 conformes ; A1 à refuser |
| 15:58 | envoyé | AVANCEMENT | écart A1 : invite confirmée, sans effet ; arrêt |
| 16:02 | envoyé | AVANCEMENT | A1 rejoué, A2, A3 refusés, H1 hook ; §9 1/4, invite |
| 16:03 | envoyé | AVANCEMENT | §9 1/4 conforme, 2/4 invite |
| 16:05 | envoyé | AVANCEMENT | §9 2/4 conforme, 3/4 invite |
| 16:07 | envoyé | AVANCEMENT | §9 3/4 conforme, 4/4 invite |
| 16:09 | envoyé | AVANCEMENT | §9 terminé |
| 16:19 | envoyé | QUESTION | §10, §11.1 conformes ; fixture 56 écarts=4 / 76, causes, options |
| 16:22 | envoyé | AVANCEMENT | option 1 choisie par l'utilisateur dans la session VM ; pytest lancé |
| 16:25 | envoyé | AVANCEMENT | pytest conforme ; branche créée ; §12 lancé |
| 16:30 | envoyé | AVANCEMENT | §12 conforme |

Les messages suivants (QUESTION du push, AVANCEMENT du §14, `FIN-*`) sont postérieurs au commit
de ce rapport.

## 11. Non fait

- C7 (cartes) : écarté au PA-109. Aucune commande OpenOCD, aucune écriture flash.
- Push de `devenv/env-61-debian` : soumis à l'accord de l'utilisateur (PA-P), après ce commit.
- §14 (nettoyage) : après ce commit.
- Motif des invites d'A2 et d'A3 : non relevé (§3.2).
- `~/tmp-pytest` n'est pas vidé (hors critère).
