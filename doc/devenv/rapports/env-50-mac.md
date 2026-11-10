# ENV-50 — Validation Debian groupée (ENV-44 à ENV-49) — rapport de la session Mac

Session Mac `lepton-tools-9d`, 2026-11-10. Branche lepton-tools `devenv/env-50` (depuis `main`
c985670). Consigne VM : `consignes/env-50-debian.md`. Journaux Mac :
`~/lepton-tools-dev/essais/env-50-mac/`.

## 1. Préparation (tâche 1)

### 1.1 Écarts Mac `env-42-apres` → `env-49-apres`

`comparer-oracle.py` par preset. `env-42-apres` est la référence Mac de R43-1 ; `env-49-apres` est
l'oracle de référence (PA-86). La croissance du code est relevée par
`env-50-mac/croissance.py`, nouveau et en lecture seule : somme des tailles des symboles `t`, `T`,
`W` et variation des sections chargées. C'est la leçon E-1 de R43-1 : sur Debian, `.text`
varie par pas de 64 octets.

| Preset | Code | Écarts hors `.debug_*` | Code des symboles | `.text` | Étape |
| --- | --- | --- | --- | --- | --- |
| host | — | `mklepton-empreintes.sha256` identique | — | — | — |
| `nucleo-f4{29,39}zi-{embos,freertos}`, `qemu-mps2-an500-*`, `stm32f746g-disco-*`, `samd21-xplained-pro-*` (10) | 0 | aucun | 0 | 0 | ENV-46, 47, 48 : aucun binaire changé |
| `qemu-mps2-an386-{embos,embos-soft,freertos,freertos-soft}` | 1 | aucun (3 sections `.debug_*`) | 0 | 0 | ENV-44 D5 (`ARMCM4_FP.h`) |
| `nucleo-wl55jc1-{embos,freertos}` | 1 | `.text` et 26 symboles (2 ajoutés, 3 retirés, 21 modifiés : HAL SUBGHZ, UART, pile radio) | +36 | +48 | ENV-49 (PA-85) |

Aucune autre section chargée ne change. Attendus versionnés dans `env-50-mac/attendu/` :
- `comparaisons-mac/<preset>.txt` : sorties brutes du comparateur pour les 6 presets qui changent ;
- `nucleo-wl55jc1-{embos,freertos}.noms.txt` : les 26 lignes de symboles normalisées, noms seuls ;
  identiques en embOS et en FreeRTOS. Les lignes `section` sont exclues : la VM lit `.text` par
  `croissance.py` ;
- `croissance-mac.txt` : sortie de `croissance.py` pour les 16 presets.

Contrôle de la méthode sur R36-1 → R43-1 (Debian) : WL55 embOS `code_symboles +16 .text +0`,
F429 embOS `+48 / +64`, an386 embOS `+16 / +64`. On retrouve le tableau E-1 d'`env-43-mac.md` §4.

### 1.2 Têtes publiées (`git ls-remote`, 2026-11-10)

Relevé complet : `env-50-mac/ls-remote-mac.txt`.

| Dépôt | Référence | Commit | En R43-1 |
| --- | --- | --- | --- |
| `seed.scions` | tag `0.6.2.0` (`master` 7e8a0cc) | 213d2c0 | tag `0.6.1.0` 4502a70 |
| `lepton-seed.scions` | `original-tree` | 15740f9 | = |
| `lepton-original-tree.scions` | `master` | 76f28bd | 763dda2 |
| `lepton-bsp-qemu-mps2-an386` | `master` | 10a8889 | 5819047 |
| `lepton-famille-stm32f4xx` | `master` | acdd24c | 7afd7f1 |
| `lepton-famille-stm32f7xx` | `master` | 12280a5 | d2d9aa9 |
| `lepton-famille-stm32wlxx` | `master` | 9349be2 | 2340b25 |
| `lepton-bsp-nucleo-wl55jc1` | `master` | 4d7cf80 | ef51ec1 |
| 7 autres greffons famille/BSP | `master` | inchangés | = |
| miroirs F4 | `v1.8.5` b6f0ed3 ; cmsis `master` 9192c7b (épinglé 3c77349) | | = |
| miroirs F7 | `v1.3.3` e1446fa ; `v1.2.10` 2352e88 | | nouveaux |
| miroirs WL | `v1.6.0` 5c87cf0 ; `v1.4.0` 71a0b78 ; `v1.5.0` 7dc059f ; STM32CubeWL `v1.6.0` f934cd2 | | nouveaux |

Les clones de `<ROOTSTOCK>` sont aux mêmes commits, propres et alignés sur `origin`. Les 8 clones
tiers sont aux révisions épinglées.

### 1.3 Liens du trunk

L'état de R43-1 est celui d'`essais/env-13-vierge` avant sa regreffe : regreffé avant R43-1, il n'a
pas bougé depuis. `controler-trunk.py` y donne `CONFORME` contre `env-43-mac/attendu/trunk-liens.txt`
(3982 liens, 206 projetés). L'état actuel est celui de `<ROOTSTOCK>` : 3889 liens.

| Relevé | Résultat |
| --- | --- |
| ajouts | **11** : `ucore/cmsis/LEPTON-PROVENANCE.md` (ENV-44 D7) ; 9 `LICENSE.md` WL (ENV-48, C2) ; `radio_subghz_phy/Conf/radio_template.h` (ENV-49, PA-85 Q2) |
| retraits | **104** : 96 de la SPL F4 (ENV-46 ; 76 sous `dev/arch/cortexm/stm32f4xx/`, 20 sous `ucore/cmsis/Device/st/stm32f4xx/`) ; 8 `LICENSE.txt` WL (ENV-48) |
| cibles changées, chemins égaux | F7 (201, ENV-47) et WL (ENV-48, ENV-49) : 424 lignes `chemin -> cible` diffèrent en tout |
| liste `./chemin -> cible` de `<ROOTSTOCK>` | 3889, SHA-256 `5dbbc69f…` (= `chemins-cibles.txt` d'ENV-49) |
| cibles sous `depots/tiers/` | 629 (F4 206, F7 201, WL 222), 8 clones |

3982 + 11 − 104 = 3889. Attendus :
- `attendu/liens-ajoutes.txt` (11) et `attendu/liens-retires.txt` (104), chemins `trunk/…` ;
- `attendu/trunk-liens.txt` (3889) ;
- `attendu/projetes.txt` (629).

`env-43-mac/controler-trunk.py` est repris sans modification. Il gère le clone partagé
`stm32cubewl/v1.6.0` (clé = 2 premiers composants sous `depots/tiers/`). Sur `<ROOTSTOCK>` :
code 0, `CONFORME`. Résultat : 3889 = attendu, 0 fichier régulier, 0 lien cassé, 629 projetés,
0 écart de nom, 0 écart de contenu. Les 8 clones tiers ont `origin` = miroirs, 0 modification
et le filtre `blob:none`.

### 1.4 Références de C5

- pytest de lepton-tools (venv `~/lepton-tools-dev/venv-lepton-tools`, Python 3.11.5) :
  **377 passed** en 6 min 37 ; `tests/test_proteger_trunk.py` : 118 passed.
- `compiler-hal-f4-a-blanc.sh ~/lepton` : code 0. F429 et F439 : `cmsis5`, 90 sources, 0 échec,
  0 avertissement. Le résumé est identique à `env-44-residus/d6/resume.txt` : le retrait de la
  SPL (ENV-46) ne change rien. Copié dans `attendu/compilation-a-blanc-resume.txt` ; seule la
  ligne du compilateur différera sur Debian.

### 1.5 Essai préalable : `graft-update` d'`essais/env-13-vierge` (PA-P accordé le 2026-11-10)

État avant (`env-13-vierge-clones-avant.txt`) : celui de `$U` sur la VM.
- 13 clones sur `master`, amont `origin/master`, propres ;
- noyau 763dda2, an386 5819047, F4 7afd7f1, WL 2340b25, WL55 ef51ec1, F7 d2d9aa9 ;
- graine 15740f9, propre ; 16 entrées ; 3982 liens ;
- espace régénéré par `lepton generate` (code 0) juste avant le relevé.

| Contrôle | Résultat |
| --- | --- |
| `scion graft-update -v` | code 0, 0 conflit ni refus ; 6 clones avancés par avance rapide (noyau → 76f28bd, an386 → 10a8889, F4 → acdd24c, WL → 9349be2, WL55 → 4d7cf80, F7 → 12280a5) ; 6 clones tiers `--filter=blob:none` depuis les miroirs ; « 3889 feuilles liées » ; « 6 chemin(s) ignoré(s) par git » = 6 `.DS_Store` du Finder (déjà en ENV-43) |
| Clones | = `<ROOTSTOCK>`, propres |
| Entrées | 23 |
| Ajouts / retraits | 11 / 104 = attendu |
| `controler-trunk.py` | code 0, `CONFORME` (3889, 629 projetés = attendu, 0 écart de nom ni de contenu, 8 clones tiers aux HEAD épinglés) |
| `lepton check`, `generate`, `seed status` | 0, 0, 0 ; 9 clés `projection` (200, 6, 157, 6, 20, 38, 1, 196, 5 fichiers) ; trunk sans fichier régulier ni lien cassé |
| Espace | identique à l'avant (`diff` vide) ; 23 `request`, 10 `svdFile`, 7 `lldb`, 4 tâches de tests, 0 `tiers` |
| `scion mirror-sync --dry-run -v` | code 0 ; 8 miroirs, 0 référence à envoyer, 0 signalement ; 8 dépôts de travail sous `depots/.mirrors/` (79 Mo) ; rien envoyé |
| Clones tiers | 242 Mo par rootstock |

L'attendu de C2 et de C6 est donc confirmé sur un rootstock dans l'état de `$U`. Le passage direct
de l'état de R43-1 à celui d'ENV-49, sans étape intermédiaire, est conforme.

### 1.6 Consigne

`consignes/env-50-debian.md`, reprise d'`env-43-debian.md`.

| Critère | Contenu |
| --- | --- |
| C1 | Versions ; installation par l'utilisateur de scion 0.6.2.0 (`install-debian.sh` du noyau 76f28bd, défaut `SCION_REF`), de lepton (`pipx`) et de VSCodium (`install-vscodium.sh` ×2), avant toute regreffe |
| C2 | `graft-update` de `essais/env-28-debian` par l'utilisateur, puis rootstock neuf `essais/env-50-debian` ; `controler-trunk.py` contre l'attendu |
| C3 | Host et 16 presets contre `env-43-debian` : 10 presets à 0, an386 `.debug_*` seuls, WL55 aux symboles du Mac et `code_symboles +36` |
| C4 | D8 : `graft-update` d'`essais/env-13-debian` par l'utilisateur, `CONFORME`, `lepton check` code 0 |
| C5 | pytest complet (`venv-test`, hook compris), compilation à blanc code 0, fichiers générés (`$R` contre `$R43`, `$U`, `$P`) |
| C6 | `mirror-sync --dry-run` dans `$R`, 8 miroirs |
| C7 | F429 (3 images, réseau) et paire WL55 (2 images, radio) rattachées ensemble, sonde choisie par numéro, numéro faux refusé |
| C8 | `rm -rf essais/env-43-debian ~/env-43-journaux` par l'utilisateur, après le §10.1 |

Le nom `essais/env-50-debian` a la même longueur qu'`env-43-debian` : les chaînes `__FILE__` des
presets FreeRTOS suivent le chemin du rootstock.

C5, C7 et C8 suivent les orientations données par l'utilisateur au début de la session, à
confirmer au PA-87.

## 2. PA-87 (2026-11-10, décisions de l'utilisateur)

- Consigne `consignes/env-50-debian.md` (42fc79e) validée telle qu'écrite, C1 à C8.
- PA-11 : écriture flash sur la VM pour `nucleo-f429zi-embos`, `nucleo-f429zi-freertos`,
  `nucleo-f439zi-embos` (NUCLEO-F429ZI) et `nucleo-wl55jc1-{embos,freertos}` (WL55 A et B),
  construites sur la VM, sonde choisie par numéro.
- C8 : `rm -rf essais/env-43-debian ~/env-43-journaux` par l'utilisateur, après le §10.1.
- PA-P : push de `devenv/env-50` (93e1aa6), ordre `R50-1` à `debian-linux-vm`.
- PA-P (tâche 3) : regreffe des 6 autres rootstocks d'essai pendant R50-1 ; suppression
  d'`essais/env-41-vierge` et `essais/env-41-vierge-graine`.

## 3. Messages §2bis

| Message | Date | Sens | Résumé |
| --- | --- | --- | --- |
| ORDRE R50-1 | 2026-11-10 | Mac (`lepton-tools-9d`) → VM (`debian-linux-vm`) | consigne `env-50-debian.md` @ 42fc79e envoyée en entier, branche `devenv/env-50` @ 93e1aa6 ; actions de l'utilisateur (installations, 2 `graft-update`, venv, cartes, `rm -rf`, push) et flash accordé (PA-11) ; envoi réussi par Remote Control, lecture non confirmée |
| ACCUSÉ R50-1 | 2026-11-10 | VM → Mac | reçu directement (non relayé). §5 sans écart : `devenv/env-50` = 93e1aa6, ls-remote = §1 ; scion 0.6.1.0 avant installation, chaîne APT = R43-1, embOS présent, 17 Go libres, `venv-test` présent ; `$U` dans l'état de R43-1 (16 entrées, 3982 liens, 2 clones tiers F4) ; `$E13` : graine 0f1275a (ancêtre de 15740f9), 9 entrées, 8 clones sur `master` propres (noyau 16a331b, F4 01b5528, WL 1eccc2f…), 4011 liens, aucun clone tiers ; graines citant F4/F7/WL : les 3 clones `original-tree` seuls |
| AVANCEMENT R50-1 (§5.1, §6) | 2026-11-10 | VM → Mac | §5.1 : `generate` `$P`, `$R43`, `$U` et `check` `$P`, `$E13` à code 0 ; espaces copiés ; §6 : `$K` 763dda2 → 76f28bd, `SCION_REF` 0.6.2.0 (noyau, lepton-tools), `SCION_MIN_VERSION` (0, 6, 2, 0), `.vsix` 0.5.2 présent ; attente des installations par l'utilisateur |

## 4. Rootstocks d'essai du Mac (tâche 3)

Accord de l'utilisateur (PA-P) le 2026-11-10 : `env-13-vierge` avant l'ordre (§1.5) ; les 6 autres
pendant R50-1. scion 0.6.2.0, lepton 0.1.0. Journaux : `~/lepton-tools-dev/essais/env-50-mac/`
(`<rootstock>-{clones-avant,clones-apres,generate-avant,graft-update,check,generate}.*`,
`-liens-{avant,apres}.txt`, `-ajoutes.txt`, `-retires.txt`, `-espace-avant.code-workspace`,
`-espace.diff`, `-controle/`, `regreffes-bilan.txt`).

Inventaire avant :
- clones de greffons sur leur branche (`master`, graines sur la leur), amont réglé, propres ;
- têtes de R43-1 : noyau 763dda2, an386 5819047, F4 7afd7f1, WL 2340b25, WL55 ef51ec1 ;
- 0 lien cassé ; aucun fichier régulier hors `.DS_Store` du Finder (0 à 2 par trunk, tolérés) ;
- espaces régénérés par `lepton generate` juste avant le relevé.

Procédure (script de session, forme d'`env-43-mac.md` §5) :
1. `generate` avant, puis copie de l'espace ;
2. relevé `chemin -> cible` ;
3. `scion graft-update -v` ; pour `qemu-gra2`, `graft-remove lepton@bsp-qemu-mps2-an386` sans
   `--purge` ;
4. relevé après, comparé à l'avant ;
5. `controler-trunk.py` (noms et contenus projetés) ;
6. `check`, `generate`, `diff` de l'espace.

| Rootstock | `graft-update` | Liens avant → après | Ajouts / retraits | Cibles changées | Entrées | Projetés (clones tiers) | `check` | `generate` | Espace |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `env-13-vierge` | 0 (§1.5) | 3982 → 3889 | 11 / 104 = attendu | — | 16 → 23 | 629 (8) | 0 | 0 | identique |
| `env-9` | 0 ; noyau, an386 avancés | 3058 → 3059 | 1 / 0 (D7) | 0 | 5 | 0 | 0 | 0 | identique |
| `env-11/qemu` | 0 | 3058 → 3059 | 1 / 0 (D7) | 0 | 5 | 0 | 0 | 0 | identique |
| `env-11/qemu-gra2` | 0 (BSP an386 réinscrit), puis `graft-remove` code 0, 8 feuilles | 3050 → 3051 | 1 / 0 (D7) | 0 | 4 | 0 | 1 (attendu, CFG-5) | 1 (attendu) | identique |
| `env-11/bout-en-bout/rootstock` | 0 | 3058 → 3059 | 1 / 0 (D7) | 0 | 5 | 0 | 0 | 0 | identique |
| `env-11/f429zi` | 0 ; noyau, F4 avancés | 3389 → 3294 | 1 / 96 (D7 ; SPL : 76 + 20) | 0 | 7 | 206 (2, inchangés) | 0 | 0 | identique |
| `env-11/wl55jc1` | 0 ; noyau, WL, WL55 avancés ; 4 clones tiers `blob:none` depuis les miroirs | 3312 → 3315 | 11 / 8 (D7, 9 `LICENSE.md`, `radio_template.h` ; 8 `LICENSE.txt`) | 212 (WL vers `depots/tiers/`) | 5 → 10 | 222 (4) | 0 | 0 | identique |

Partout : `controler-trunk.py` donne 0 écart de nom (casse) et 0 écart de contenu des projetés ;
0 lien cassé ; 0 fichier régulier hors `.DS_Store`. Les clones sont sur leur branche, propres,
aux têtes publiées. Pour `env-11/wl55jc1`, 212 = 222 projetés − 10 nouveaux chemins projetés.

Constructions à neuf (`cmake --fresh`, `--clean-first`), comparées à `oracles/env-49-apres/` :

| Rootstock | Presets | Construction | Écarts hors `.debug_*` | `.debug_line` | `.debug_str` |
| --- | --- | --- | --- | --- | --- |
| `env-11/f429zi` | host, `nucleo-f429zi-embos` | 0, 0 | 0 | 306684 → 330957 (+24273, = ENV-43) | 139391 → 143421 (+4030, = ENV-43) |
| `env-11/wl55jc1` | host, `nucleo-wl55jc1-embos` | 0, 0 | 0 | 233731 → 250883 (+17152) | 134112 → 137248 (+3136) |

Les chemins des sources sont propres au rootstock, d'où les deltas `.debug_*`. Pas de flash. Les
trunks restent sans fichier régulier ni `__pycache__`.

Constat : `scripts/lepton-env.sh` a écrit « aucun rootstock scion au-dessus de env-11/… ». La
cause est le script de session : `set -- $couple` y laissait `$1` égal au chemin relatif
`env-11/<rootstock>`, et `lepton-env.sh` cherche le rootstock à partir de `${1:-$PWD}` (l. 21).
Ce n'est pas un défaut de `lepton-env.sh`. embOS est trouvé sans ce script, et les binaires sont
identiques à la référence.

`essais/env-41-vierge` et `essais/env-41-vierge-graine` sont supprimés (accord de l'utilisateur).
Ils ne contenaient que le commit d'essai local c85ba56 d'ENV-41, non publié.
