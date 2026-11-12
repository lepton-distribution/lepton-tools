# ENV-53 — Validation Debian groupée (ENV-51 et ENV-52) — 2026-11-12

Session VM `debian-linux-vm`, ordre `R53-1` de la session Mac `lepton-tools-3b` (`ENV-53`),
consigne `doc/devenv/consignes/env-53-debian.md` à 087dd49, complétée par la réponse à la
QUESTION du §9.2 (option O2, retenue par l'utilisateur). Journaux : `~/env-53-journaux/` sur la
VM (`0-messages-R53-1.md` pour les messages). Rootstock neuf `essais/env-53-debian` (`$R`),
rootstocks regreffés `essais/env-28-debian` (`$U`) et `essais/env-13-debian` (`$E13`), graine de
projet `essais/env-11/qemu` (`$P`, non regreffée), copie d'essai `essais/env-53-c5` (`$C5`).

Résultat : C1 à C6 et C8 atteints, C7 écarté (PA-93). Un écart de base au §9.2 : le `$P` de la VM
n'avait jamais été regreffé depuis ENV-10 (noyau 1dde0af). Le premier essai d'ajout de la famille
F7 a donc échoué sur 208 conflits. La copie `$C5` a été refaite, puis regreffée seule (O2) ; le
§9.2 et le §9.3 ont ensuite été conformes. Les trois `scion graft-update` et les `rm -rf` ont été
lancés par l'utilisateur : le classifieur a refusé le premier `graft-update` lancé par la session.

## 1. Hôte et versions (§5, §6)

| Élément | Valeur |
| --- | --- |
| Hôte | Debian 13.7, Linux 6.12.107+deb13-amd64 x86_64, `lepton-user`, git 2.47.3, 2 CPU, 3 Go |
| Espace libre | `/home` 17 Go |
| Chaîne APT | arm-none-eabi-gcc `15:14.2.rel1-1` (14.2.1 20241119), cmake 3.31.6, ninja 1.12.1, QEMU 10.0.13 (`1:10.0.13+ds-0+deb13u1`), Python 3.13.5, OpenOCD 0.12.0, gcc hôte 14.2.0-19 ; binutils 2.44 : identique à R50-1 |
| embOS | `~/lepton/third_party/embos/cortexm-gcc/5.20.0.0` (`LEPTON_EMBOS_ROOT`) |
| scion | 0.6.2.0 → **0.6.3.0** (`install-debian.sh`, `SCION_REF` par défaut, `seed.scions.git@0.6.3.0`) |
| lepton | `lepton 0.1.0`, `scion 0.6.3.0 (requis ≥ 0.6.2.0)` (`pipx install --force`, depuis `devenv/env-53` propre) |
| VSCodium | 1.135.06055 ; `install-vscodium.sh` : 1re exécution `changements 0`, 2e `changements 0` |
| Extensions | `lepton-distribution.lepton@0.5.2`, `vadimcn.vscode-lldb@1.12.3`, `mcu-debug.rtos-views@0.0.16`, `mcu-debug.peripheral-viewer@1.6.4` |
| Clone noyau `$K` | propre, `master` 76f28bd → **58e421e** (avance rapide, 5 fichiers hors `scion/`) ; `SCION_REF="${SCION_REF:-0.6.3.0}"` |
| lepton-tools | `devenv/env-53` = `origin/devenv/env-53` = 087dd49, propre (avant le `switch` : `devenv/env-50-debian`) ; `SCION_REF="0.6.3.0"` (`install-vscodium.sh`) ; `SCION_MIN_VERSION = (0, 6, 2, 0)` ; `extension/dist/lepton-0.5.2.vsix` présent |
| node | absent (sans effet) |

Les quatre installations du §6 ont été lancées par la session (PA-93), codes 0.

`git ls-remote` : « têtes publiées = Mac » (diff vide avec `env-53-mac/ls-remote-mac.txt`, hors
lepton-tools). lepton-tools `main` fb61b9a ; scion `0.6.3.0` 87dc108 (`master` 6416c33) ; graine
15740f9 ; noyau 58e421e ; greffons et miroirs aux commits du §1 de la consigne.

État de départ de `$U` et de `$E13`, identique pour les deux :
- graine 15740f9 sur `original-tree`, amont réglé, propre ; 23 entrées ;
- 13 clones sur `master`, amont `origin/master`, `modifs=0`, aux commits « En R50-1 » (noyau 76f28bd) ;
- `liens=3889 casses=0 reguliers=0` ; 8 clones tiers ; `du depots/tiers` 259792 Ko.

`$R50`, son espace, `$P` et sa graine `env11`, `~/env-50-journaux` : présents. `$R`, `$C5` :
absents. `venv-test` : présent.

§5.1 : `generate` de `$P`, `$R50`, `$U` et `$E13` et `check` de `$P` : codes 0. Graine `env11` :
0 modification.

## 2. Critères (§14)

| Critère | Résultat | Constat |
| --- | --- | --- |
| C1 Versions | **atteint** | ls-remote = Mac ; git 2.47.3 ; scion 0.6.3.0 par `install-debian.sh` (défaut `SCION_REF`) ; lepton `pipx` code 0, `lepton 0.1.0`, scion 0.6.3.0 accepté ; extension 0.5.2, 2e exécution `changements 0` ; chaîne APT = R50-1 |
| C2 `graft-update` et rootstock neuf | **atteint** | `$U` : code 0, 0 conflit ; seul le noyau avancé (76f28bd → 58e421e) ; 8 clones tiers convertis ; liens inchangés ; `CONFORME` (3889 = attendu, 0 cassé, 0 régulier, 629 projetés = HEAD, 0 écart de casse) ; 23 entrées ; extraits et `sparse-checkout` = Mac (16 fichiers) ; `clones = Mac` ; `ignorecase` vide. `$R` : 23 entrées, mêmes contrôles, liste identique à `$U` |
| C3 Constructions | **atteint** | host 7/7 ; mklepton = `env-50-debian` = `env-52-apres` ; 16 presets construits ; fumée ×6 ; bancs 20/20, 16/16, 19/19 ; `peripheriques` ×4 ; `comparer_R50-1` 0 et `hors_debug=0` pour les 16 presets |
| C4 `essais/env-13-debian` | **atteint** | `graft-update` (utilisateur) code 0, 0 conflit ; mêmes contrôles qu'au §7.1, tous conformes ; `lepton check` code 0 ; espace = avant |
| C5 pytest, relais, fichiers générés | **atteint, après reprise O2** | pytest 384 passed (hook 118) ; §9.2, sur la copie regreffée : 11 relevés sur 12 = Mac, le 12e ne diffère que par la langue de git ; 5, 3 et 2 lignes `scion: ` ; échec non préfixé une seule fois ; clones F7 partiels = Mac ; `--json` valide ; liens et graine restaurés. §9.3 : notifications attendues (utilisateur), 8 lignes `scion: ` dans le canal, aucune dans la notification d'échec. §10 : `$R` codes 0, 9 clés projetées, espace = `$R50` au chemin près ; `$U` : espace = avant ; `$P` : générés, graine et `check` identiques |
| C6 Miroir | **atteint** | `mirror-sync --dry-run` code 0 ; 8 miroirs, 0 à envoyer, 0 signalement ; rien envoyé ; trunk `CONFORME` |
| C7 Cartes | écarté (PA-93) | aucune commande OpenOCD, aucun `ctest -L board`, aucune écriture flash |
| C8 Nettoyage | **atteint** | `essais/env-50-debian` (655 Mo) et `~/env-50-journaux` (6,5 Mo) supprimés par l'utilisateur ; absents. Conservés : `$U`, `$E13`, `$R`, `$P`, `$C5`, `$J`, `~/tmp-pytest` |

## 3. Presets (§8)

`rejouer-oracle.sh` : code 0, « rejouer-oracle: tout a réussi ». Fumée (`uname -a` sur `lsh`)
réussie sur les 6 presets QEMU. `qemu-mps2-an386.peripheriques` Passed dans les 4 `banc-kal.log`
an386. Trunk de `$R` après le §8 : `liens=3889 casses=0 reguliers=0`, 0 `__pycache__`. Nombres de
symboles identiques à R50-1 pour les 16 presets.

| Preset | Construction | Fumée | Banc KAL | Symboles | `comparer_R50-1` | `hors_debug` | `comparer_Mac` |
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

Host : ctest 7/7 ; empreintes mklepton identiques à `env-50-debian` et à `env-52-apres`.

`comparer_Mac` est informatif : les deux chaînes diffèrent. Par exemple, `.comment` passe de 137
à 144 octets et `.bss` de −4 octets en an386 embOS, d'`env-52-apres` vers la VM.

Bilan : `env-53-debian/8.1-bilan.txt` ; oracle : `oracles/env-53-debian/`.

## 4. Contrôles du trunk et clones tiers (§7)

`controler-trunk.py` donne la même sortie pour `$U` (§7.1), `$R` (§7.2), `$E13` (§7.3) et `$R`
après `mirror-sync` (§11) :
```
liste chemin -> cible : identique à l'attendu (3889 liens)
fichiers réguliers 0 []
liens cassés 0 []
projetés 629 ; nom non suivi au HEAD (casse) 0 [] ; contenu ≠ HEAD 0 []
depots/tiers/<clé>/<version> HEAD <épinglé> origin https://github.com/lepton-distribution/mirror-….git modifs 0 filtre blob:none   (×8)
CONFORME
```
Sorties complètes : `env-53-debian/7.1-U-controle.log`, `7.2-R-controle.log`,
`7.3-E13-controle.log`.

`graft-update` de `$U` et de `$E13` : journaux de 288 lignes chacun, avec le même contenu.
- Code 0, 0 conflit, aucun refus, aucun `git clone`, aucune ligne « chemin(s) ignoré(s) par git ».
- Graine inchangée (15740f9) ; 23 entrées.
- Un seul clone avancé : `…/original/master avancé : 76f28bd -> 58e421e`.
- 8 lignes `extraction partielle, N répertoire(s)` : `stm32f4xx-hal-driver` 2, `cmsis-device-f4` 1,
  `stm32wlxx-hal-driver` 2, `cmsis-device-wl` 2, `stm32-mw-subghz-phy` 2, `stm32cubewl` 9,
  `stm32f7xx-hal-driver` 2, `cmsis-device-f7` 1.
- « 3889 feuilles liées ».
- Inventaire : seule la ligne du noyau change (`head=58e421e`). Liste des liens inchangée (`cmp`).

Pour les trois rootstocks :
- extraits et `sparse-checkout` : **écarts=0** sur les 16 fichiers d'`attendu/clones/` ;
- `clones = Mac`, hors `ignorecase` et tailles ;
- `ignorecase` **vide** sur les 8 clones : la VM distingue la casse ;
- au Mac, `ignorecase=true`.

Lignes `clones.txt` : `env-53-debian/7.1-U-avant.clones.txt`, `7.1-U-apres.clones.txt`,
`7.2-R.clones.txt`, `7.3-E13-avant.clones.txt`, `7.3-E13-apres.clones.txt`. `H` / `S` et tailles
en Ko :

| Clone | Avant (`$U`, `$E13`) : H / S, hors `.git`, `.git` | Converti (`$U` = `$E13`) : H / S, hors `.git`, `.git` | Neuf (`$R`) : hors `.git`, `.git` |
| --- | --- | --- | --- |
| `cmsis-device-f4/3c77349…` | 152 / 0, 25972, 588 | 31 / 121, 23964, 596 | 23964, 524 |
| `cmsis-device-f7/v1.2.10` | 113 / 0, 20696, 492 | 22 / 91, 19136, 500 | 19136, 468 |
| `cmsis-device-wl/v1.4.0` | 79 / 0, 4820, 380 | 70 / 9, 4708, 388 | 4708, 372 |
| `stm32-mw-subghz-phy/v1.5.0` | 147 / 0, 2592, 636 | 28 / 119, 448, 644 | 448, 324 |
| `stm32cubewl/v1.6.0` | 8962 / 0, 146900, 24324 | 103 / 8859, 1908, 24348 | 1908, 3588 |
| `stm32f4xx-hal-driver/v1.8.5` | 209 / 0, 10516, 1700 | 204 / 5, 10424, 1708 | 10424, 1692 |
| `stm32f7xx-hal-driver/v1.3.3` | 206 / 0, 9756, 1644 | 200 / 6, 9656, 1652 | 9656, 1636 |
| `stm32wlxx-hal-driver/v1.6.0` | 168 / 0, 7452, 1288 | 161 / 7, 7348, 1296 | 7348, 1280 |

`du -sk depots/tiers` :
- `$U` et `$E13` : 259792 → **108760** Ko (Mac : 242 → 106 Mo) ;
- `$R` : **87512** Ko (Mac, ENV-52 : ≈ 85 Mo).

Les nombres `H` / `S` sont ceux du Mac. Les tailles diffèrent un peu : système de fichiers et
taille de bloc.

## 5. pytest, relais des messages, fichiers générés (§9, §10)

### 5.1 pytest (§9.1)

`venv-test` présent : lepton 0.1.0 installé en mode modifiable depuis `$T`, pytest 9.1.1,
Python 3.13.5.
- Suite complète : code 0, **384 passed** en 177,56 s, aucun test ignoré ni en échec (`-rs` vide).
- `tests/test_proteger_trunk.py` : code 0, **118 passed**.
- lepton-tools propre, hors oracle et rapport de la session.

### 5.2 Relais en ligne de commande (§9.2)

**Premier essai, écart de base.** Copie de `$P` (`tar`, sans `build/`) : `liens=3428 casses=0
reguliers=0` (Mac : 3059). `generate` et `check` : codes 0.

Inventaire de `$P` sur la VM :

| Clone | Commit | Amont | Modifications |
| --- | --- | --- | --- |
| noyau `original/master` | 1dde0af (2026-10-15, « Fusion de devenv/env-10 ») | `origin/master` | 0 |
| `bsp-qemu-mps2-an386` | 046779e | `origin/master` | 0 |
| `family-qemu-mps2` | 3954357 | `origin/master` | 0 |
| graine `env11` | 6d3d2a5 | aucun | 0 |
| application `salut` | 71e1641 | aucun | 2 (`M …/salut.c`, `?? …/salut_message.c`) |

Le noyau 1dde0af porte encore les fichiers F7 dans `lepton/original::tree`. Relevé 01
(`seed add stm32f7xx`) : code 2, stdout vide. Stderr, dans l'ordre :
- 4 lignes `scion: ` : `déclaré dans …`, `retiré : 0 feuilles`, P-P6, `retiré de …` ;
- `lepton: attention: ajout de lepton@family-stm32f7xx annulé (graine et trunk restaurés)` ;
- `lepton: erreur: échec de « scion graft --scion lepton@family-stm32f7xx » (code 1) :` ;
- le stderr de scion non préfixé, une seule fois : P-G6, `erreur : 208 conflit(s) de greffe,
  aucun fichier n'a été laissé :`, puis la liste des conflits « déjà fourni par
  « lepton/original::tree », réclamé par « lepton/family-stm32f7xx » / « tiers/… » ».

Après l'échec : liens = avant, graine sans modification. Restent dans la copie les clones créés
avant l'échec : `family-stm32f7xx` et les deux clones tiers F7. Le relais de l'échec est donc
conforme, mais 01 et 02 ne pouvaient pas reproduire l'attendu du Mac. Ce défaut de la consigne a
été reconnu par la session Mac. Relevés : `env-53-debian/9.2-essai1/`.

**Reprise (O2).** La copie a été supprimée par l'utilisateur, puis refaite à l'identique
(3428 liens). L'utilisateur a lancé `scion graft-update -v` dans la copie seule :
- code 0, aucun conflit, refus ni `git clone` ;
- noyau 1dde0af → 58e421e, `bsp-qemu-mps2-an386` 046779e → 10a8889 ; `family-qemu-mps2` reste à
  3954357 ; clone `salut` accepté tel quel ;
- « 3059 feuilles liées » ; `liens=3059 casses=0 reguliers=0`, comme au Mac ;
- `generate` code 0, 0 référence à `env-11/qemu` ; `check` code 0 (« 5 fichier(s) conforme(s) »).

`$P` n'a pas été touché.

§9.2 repris tel qu'écrit :

| Relevé | Code | stdout | `scion: ` | Remarques |
| --- | --- | --- | --- | --- |
| 01 `seed add stm32f7xx …@master --no-cmake` | 0 | 2 lignes | 5 : `déclaré`, P-G6, `extraction partielle` 2 puis 1, `greffe partielle : 212 feuilles liées` | 3271 liens ; `cmsis-device-f7` H=22 S=91, `stm32f7xx-hal-driver` H=200 S=6, `sparseCheckout=true cone=true` ; extraits et `sparse-checkout` = Mac (4 fichiers) ; `seed status --json` code 0, `json ok`, stderr vide |
| 02 `seed remove stm32f7xx --no-cmake` | 0 | 2 lignes | 3 : `retiré de`, `retiré : 212 feuilles`, P-P6 | — |
| 03 `seed add absent file://localhost…/env-53-absent.git …` | 2 | vide | 2 : `déclaré`, `retiré de` | `lepton: attention: … annulé (graine et trunk restaurés)`, puis `lepton: erreur: échec de « scion seed-clone --seed … » (code 2) :`, suivi du stderr de scion non préfixé, une seule fois, puis `→ corriger la cause signalée par scion, puis relancer` |

Après les trois relevés : liens = avant (3059) ; graine `env11` sans modification.

Comparaison au Mac (`attendu/c5/`, après remplacement par `<C>` et `<HOME>`) : 11 fichiers sur
12 identiques. `03-seed-add-echec.err` ne diffère qu'à la ligne 5, par la langue du message de
git : `et que le dépôt existe.` sur la VM, `and the repository exists.` au Mac. Ce n'est pas un
écart de lepton (§9.2).

Comme au Mac, un répertoire vide `depots/lepton/library-absent` reste après 03. Il a été retiré
par `rmdir`. Relevés : `env-53-debian/9.2-releves/`.

### 5.3 Relais dans VSCodium (§9.3, essai de l'utilisateur)

Les étapes 1 à 7 ont été faites par l'utilisateur sur `$C5`. Il a rapporté les notifications
attendues aux étapes 3 et 4, sans en recopier le texte. Texte exact de la notification d'erreur
de l'étape 5 :

> lepton : ajouter absent — échec (code 2) lepton: erreur: échec de « scion seed-clone --seed
> /home/lepton-user/lepton-tools-dev/essais/env-53-c5/depots/lepton-seed/env11 » (code 2) :
> erreur : échec de « git clone file://localhost/home/lepton-user/lepton-tools-dev/essais/env-53-absent.git
> /home/lepton-user/lepton-tools-dev/essais/env-53-c5/depots/lepton/library-absent/master » (code 128) :
> et que le dépôt existe. → corriger la cause signalée par scion, puis relancer

Cette notification ne contient aucune ligne `scion:`.

Canal « Lepton » (`env-53-debian/9.3-sortie-lepton.txt`, 60 lignes) :
- **8 lignes `scion: `** : 3 à l'ajout (`déclaré`, P-G6, `greffe partielle : 212 feuilles`),
  3 au retrait (`retiré de`, `retiré : 212 feuilles`, P-P6), 2 à l'échec (`déclaré`, `retiré de`) ;
- les trois actions finissent par `→ code 0`, `→ code 0` et `→ code 2`. Les 6 autres
  `→ code 0` du canal viennent des `lepton seed status --json` que l'extension lance d'elle-même
  autour des actions ;
- les lignes de `04-ext-seed-add-f7` (3 `.err`, 2 `.out`) et de `05-ext-seed-remove-f7` (3 et 2)
  sont toutes présentes dans le canal. Pour `06-ext-seed-add-echec`, 5 lignes `.err` sur 6 sont
  présentes ; la 6e ne diffère que par la langue de git, comme au §9.2.

Après l'essai : liens = avant (3059), graine sans modification. Le répertoire vide
`library-absent` était de nouveau présent ; il a été retiré.

### 5.4 Fichiers générés (§10)

- §10.1 `$R` :
  - `check`, `generate` et `seed status` : codes 0 ;
  - 9 lignes `projection` aux versions du §1 (200, 6, 157, 6, 20, 38, 1, 196 et 5 fichiers) ;
    `trunk : aucun fichier régulier, aucun lien cassé` ;
  - espace : 23 `"request"`, 10 `"svdFile"`, 7 `"type": "lldb"`, 4 « tests des greffons »,
    0 `tiers` ; identique à celui de `$R50` au chemin près (`diff=0`).
- §10.2 `$U` : codes 0 ; mêmes 9 clés projetées ; espace identique à l'avant (`diff=0`).
- §10.3 `$P` : codes 0 ; générés (`CMakeUserPresets.json` d5ee81e4…, `env11.code-workspace`
  b2c7b8a4…), graine et sortie de `check` identiques à l'avant.

## 6. Commande de miroir (§11)

`scion mirror-sync --dry-run -v` dans `$R` :
- code 0 ;
- 8 lignes `miroir https://github.com/lepton-distribution/mirror-… : 0 référence(s) à envoyer,
  0 signalement(s)` ;
- 8 dépôts de travail sous `depots/.mirrors/github.com/lepton-distribution/` (78 Mo) ;
- trunk `CONFORME`. Rien n'a été envoyé.

## 7. Écarts et constats

1. **Base de `$P` (§9.2).** Le `$P` de la VM n'avait jamais été regreffé depuis ENV-10 :
   - noyau 1dde0af, `bsp-qemu-mps2-an386` 046779e ; 3428 liens contre 3059 au Mac ;
   - premier essai 01 : 208 conflits, relais de l'échec conforme ;
   - reprise par l'option O2, retenue par l'utilisateur : copie refaite, puis regreffée seule.
2. **Classifieur de permissions.** Il a refusé le `scion graft-update` de `$U` lancé par la session
   (« Modify Shared Resources »), sans rien exécuter. Les `graft-update` de `$U`, de `$E13` et de
   `$C5`, ainsi que les `rm -rf` de `$C5` et du §13, ont donc été lancés par l'utilisateur. Les
   installations du §6 ont été lancées par la session (PA-93).
3. **Ordre.** Le §10.2 et le §10.3 ont tourné pendant le §8 : ils ne touchent pas `$R`. Le §9.1,
   le §10.1 et le §11 ont tourné pendant l'attente de la réponse à la QUESTION du §9.2. La
   session Mac a accepté cet ordre.
4. **Langue de git.** Sur la VM, les messages de git sont en français (03 et `06-ext`). C'est la
   seule différence avec les sorties du Mac.
5. **`ignorecase`.** Vide sur les 40 lignes `clones.txt` du §7 (8 clones × 5 relevés) ; `true`
   au Mac. Les extraits sont identiques octet pour octet.
6. **Tailles.** `du depots/tiers` avant conversion : 259792 Ko (≈ 254 Mio), contre « ≈ 242 Mo »
   à la consigne. Après conversion : 108760 Ko (Mac 106 Mo) ; rootstock neuf 87512 Ko (Mac 85 Mo).
7. **Canal « Lepton ».** En plus des trois actions, il contient 6 `lepton seed status --json`
   lancés par l'extension. La consigne attendait « trois `→ code` » : ce sont ceux des actions.
8. **`library-absent`.** Le répertoire vide laissé après un ajout en échec est revenu après 03 et
   après l'étape 5 du §9.3, comme au Mac. Il a été retiré par `rmdir` les deux fois.

## 8. Journal des messages (§2bis)

Tous les envois au bridge ont été acceptés par le serveur, avec la réponse « delivery not
confirmed » (pas une erreur, D9 non appliquée). Aucun renvoi.

| Date (UTC) | Sens | Type | Résumé |
| --- | --- | --- | --- |
| 16:29 | reçu | ORDRE | R53-1, consigne à 087dd49 |
| 16:31 | envoyé | ACCUSÉ | lectures §5 conformes, étapes prévues, écarts (taille tiers, node) |
| 16:31 | envoyé | AVANCEMENT | §5.1, pré-contrôles §6, lancement des installations |
| 16:34 | envoyé | AVANCEMENT | §6 conforme ; pré-relevés §7.1 ; lancement `graft-update` `$U` |
| 16:34 | envoyé | AVANCEMENT | refus du classifieur ; `graft-update` `$U` confié à l'utilisateur |
| 16:46 | envoyé | AVANCEMENT | §7.1, §7.2 conformes ; `graft-update` `$E13` confié à l'utilisateur |
| 16:48 | envoyé | AVANCEMENT | §7.3 conforme ; §8 lancé |
| 16:53 | envoyé | AVANCEMENT | §8 conforme ; §10.2, §10.3 conformes ; §9.1 lancé |
| 16:55 | envoyé | QUESTION | §9.2 01 : 208 conflits, base `$P` ancienne ; options O1, O2, O3 |
| 16:56 | envoyé | AVANCEMENT | §10.1, §11 conformes |
| 16:56 | reçu | ORDRE (complément) | O2 retenue par l'utilisateur |
| 16:57 | envoyé | AVANCEMENT | §9.1 conforme ; O2 étape 1 ; `rm -rf` confiés à l'utilisateur |
| 16:57 | envoyé | AVANCEMENT | §13 fait ; copie refaite ; `graft-update` de `$C5` confié à l'utilisateur |
| 17:00 | envoyé | AVANCEMENT | O2 faite ; §9.2 conforme ; §9.3 confié à l'utilisateur |

Détail : `~/env-53-journaux/0-messages-R53-1.md` sur la VM.

## 9. Non fait

- C7 (cartes) : écarté au PA-93. Aucune commande OpenOCD, aucun `ctest -L board`, aucun flash.
- `$P` (`essais/env-11/qemu`) reste non regreffé (noyau 1dde0af), comme le demandait la consigne.
- `~/tmp-pytest` n'est pas vidé (hors critère).
- Push de `devenv/env-53-debian` : soumis à l'accord de l'utilisateur (PA-P).
