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
