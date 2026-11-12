# ENV-53 — Validation Debian groupée (ENV-51, ENV-52) — rapport de la session Mac

Session Mac `lepton-tools-3b`, 2026-11-12. Branche lepton-tools `devenv/env-53` (depuis `main`
fb61b9a). Consigne VM : `consignes/env-53-debian.md`. Journaux Mac :
`~/lepton-tools-dev/essais/env-53-mac/`. Outils de la session, en lecture seule, utilisables sur
Debian : `env-53-mac/ls-remote.sh`, `releve-clones.sh`, `inventaire-clones.sh`, `liens.py`.

## 1. Préparation (tâche 1)

### 1.1 Têtes publiées (`git ls-remote`, 2026-11-12)

Relevé complet : `env-53-mac/ls-remote-mac.txt` (script `env-53-mac/ls-remote.sh`).

| Dépôt | Référence | Commit | En R50-1 |
| --- | --- | --- | --- |
| `lepton-tools` | `main` | fb61b9a | c985670 |
| `seed.scions` | tag `0.6.3.0` (`master` 6416c33) | 87dc108 | tag `0.6.2.0` 213d2c0 |
| `lepton-original-tree.scions` (noyau) | `master` | 58e421e | 76f28bd |
| graine `original-tree`, 12 autres greffons, 8 miroirs | | inchangés | = |

Le noyau 58e421e (fusion de 41c9384) ne change que 5 fichiers hors de `scion/` :
`README-PAQUET.md`, `README.md`, `doc/BUILDING.md`, `scripts/install-debian.sh`,
`scripts/install-macos.sh` (`SCION_REF` 0.6.3.0). Rien n'est greffé : aucun lien ne change.

### 1.2 Liens du trunk et clones tiers de `<ROOTSTOCK>`

`<ROOTSTOCK>` (regreffé en ENV-52) : `controler-trunk.py` contre
`env-50-mac/attendu/trunk-liens.txt` → code 0, `CONFORME` :
- 3889 liens identiques, SHA-256 5dbbc69f… (celui de R50-1) ;
- 629 projetés, 0 écart de nom ni de contenu ;
- 0 fichier régulier, 0 lien cassé.

L'attendu de liens de R50-1 reste donc valable : il n'est pas recopié. La consigne cite
`env-50-mac/attendu/trunk-liens.txt` et `projetes.txt`.

Fichiers extraits par clone (`env-53-mac/releve-clones.sh ~/lepton …`), versionnés dans
`env-53-mac/attendu/` :
- `clones/<clé>@<version>.extraits.txt` : fichiers présents sur le disque hors `.git`, triés en
  `LC_ALL=C` ;
- `clones/<clé>@<version>.sparse-checkout` : copie de `.git/info/sparse-checkout` ;
- `clones-rootstock-mac.txt` : une ligne par clone.

Pour les 8 clones :
- `sparseCheckout=true`, `cone=true`, `ignorecase=true` (Mac) ;
- `extraits=H:oui` : les fichiers présents sont exactement les fichiers `H` de
  `git ls-files -t`.

Les motifs du `sparse-checkout` mêlent les casses (`Projects/NUCLEO-WL55JC/…/SubGHz_Phy_PingPong/`,
`Utilities/lpm/tiny_lpm/`). Sur la VM, qui distingue la casse, la comparaison octet pour octet
des listes prouve l'ensemble extrait.

Lecture des clones tiers : le hook du Mac refuse `git config` sous `depots/tiers/`, même en
lecture (constaté en début de session). `releve-clones.sh` lit donc `.git/config.worktree` puis
`.git/config` par `grep`. `git sparse-checkout set` active l'extension `worktreeConfig` et écrit
`core.sparseCheckout*` dans `config.worktree`.

### 1.3 Attendu de C3

Aucun binaire ne change : ENV-51 et ENV-52 ne touchent aucune source compilée, et le Mac a
`env-52-apres` = `env-49-apres` (16 × code 0). Proposé au PA-93 :
- `comparer-oracle.py` contre `env-50-debian` à **0 pour les 16 presets** ;
- mklepton identique à `env-50-debian` et à `env-52-apres` ;
- aucun écart admis.

Le rootstock neuf s'appelle `env-53-debian`, de même longueur qu'`env-50-debian` (chaînes
`__FILE__`).

### 1.4 Essai préalable : `graft-update` d'`essais/env-13-vierge` (PA-P accordé le 2026-11-12)

État avant, celui de `$U` sur la VM :
- 14 clones sur leur branche, amont réglé, propres (`env-13-vierge-clones-avant.txt`) ;
- noyau 76f28bd, les autres aux têtes publiées ; 23 entrées ;
- `CONFORME` contre l'attendu (3889) ;
- 8 clones tiers en extraction complète, `depots/tiers` 247 600 Ko (242 Mo) ;
- espace régénéré par `lepton generate` (code 0) juste avant le relevé.

STM32CubeWL compte 8962 fichiers `H` pour 8947 fichiers sur le disque. L'écart (15) vient de ses
15 sous-modules (mode 160000), suivis mais qui ne sont pas des fichiers.

| Contrôle | Résultat |
| --- | --- |
| `scion graft-update -v` (scion 0.6.3.0) | code 0, 0 conflit ni refus ; un seul clone avancé : `…/original/master avancé : 76f28bd -> 58e421e` ; aucun `git clone` ; 8 lignes `extraction partielle, N répertoire(s)` (F4 HAL 2, CMSIS F4 1, WL HAL 2, CMSIS WL 2, SubGHz 2, STM32CubeWL 9, F7 HAL 2, CMSIS F7 1) ; « 3889 feuilles liées » ; « 6 chemin(s) ignoré(s) par git » (6 `.DS_Store` du Finder) |
| Inventaire | seule la ligne du noyau change |
| `controler-trunk.py` | code 0, `CONFORME` (3889 = attendu, 629 projetés = attendu, 0 écart de nom ni de contenu, 8 clones aux HEAD épinglés, filtre `blob:none`) |
| Extraits et `sparse-checkout` | 16 fichiers identiques à ceux de `<ROOTSTOCK>` ; lignes `clones.txt` identiques, **tailles comprises** |
| `depots/tiers` | 247 600 → 108 724 Ko (242 → 106 Mo) |
| `lepton check`, `generate`, `seed status` | 0 (19 fichiers conformes), 0, 0 ; 9 clés `projection` ; trunk sans fichier régulier ni lien cassé |
| Espace | identique à l'avant (`diff` vide) |

Clones tiers, avant → après (fichiers `H` / `S`, Ko hors `.git`, Ko de `.git`) :

| Clone | Avant | Après |
| --- | --- | --- |
| `cmsis-device-f4/3c77349…` | 152 / 0, 25 932, 520 | 31 / 121, 23 956, 528 |
| `cmsis-device-f7/v1.2.10` | 113 / 0, 20 652, 424 | 22 / 91, 19 128, 432 |
| `cmsis-device-wl/v1.4.0` | 79 / 0, 4 768, 312 | 70 / 9, 4 668, 320 |
| `stm32-mw-subghz-phy/v1.5.0` | 147 / 0, 2 504, 568 | 28 / 119, 436, 576 |
| `stm32cubewl/v1.6.0` | 8962 / 0, 135 584, 24 256 | 103 / 8859, 1 828, 25 012 |
| `stm32f4xx-hal-driver/v1.8.5` | 209 / 0, 10 488, 1 632 | 204 / 5, 10 404, 1 640 |
| `stm32f7xx-hal-driver/v1.3.3` | 206 / 0, 9 724, 1 576 | 200 / 6, 9 636, 1 584 |
| `stm32wlxx-hal-driver/v1.6.0` | 168 / 0, 7 424, 1 220 | 161 / 7, 7 332, 1 228 |

L'attendu de C2 et de C4 est donc confirmé sur un rootstock dans l'état de `$U` et de `$E13`.
Journaux : `env-53-mac/env-13-vierge-*`.

### 1.5 Attendu de C5 (relais des messages)

Rootstock d'essai `~/lepton-tools-dev/essais/env-53-c5` : `rsync -a` d'`essais/env-11/qemu` (graine
de projet `env11`, QEMU) sans `build/`. Avant : 3059 liens, 0 cassé, 0 fichier régulier ;
`lepton check` code 0. Relevés par `env-51-messages/releve.sh`, versionnés dans
`env-53-mac/attendu/c5/`, chemins remplacés par `<C>` (la copie) et `<HOME>`.

| Relevé | Commande | Code | `scion:` relayées | Remarques |
| --- | --- | --- | --- | --- |
| 01 | `seed add stm32f7xx --type famille <URL>@master --no-cmake` | 0 | 5 : `déclaré`, P-G6, 2 × `extraction partielle` (2 et 1 répertoires, nouvelles en 0.6.3.0), `greffe partielle : 212 feuilles` | 3271 liens ; 2 clones F7 neufs partiels, extraits et `sparse-checkout` = attendu ; `seed status --json` code 0, JSON valide |
| 02 | `seed remove stm32f7xx --no-cmake` | 0 | 3 : `retiré de`, `retiré : 212 feuilles`, P-P6 | liens = avant (3059) ; graine propre ; clones F7 conservés |
| 03 | `seed add absent file://localhost<HOME>/…/env-53-absent.git --type bibliotheque --no-cmake` | 2 | 2 : `déclaré`, `retiré de` (annulation) | `lepton: attention: … annulé`, puis `lepton: erreur:` avec le stderr de scion une seule fois, non préfixé ; liens = avant |
| 04-06 | mêmes commandes, telles que les lance l'extension (`--version master`, sans `--no-cmake`), sur la même copie | 0, 0, 2 | 3, 3, 2 | seconde passe : clones F7 déjà présents, aucune ligne `extraction partielle` (ensemble inchangé) |

Le stdout de 01 au Mac contient en plus `fichier système supprimé du trunk : …/trunk/.DS_Store`
(fichier du Finder), retiré de l'attendu.

Contrôle de `lastMessage` (code compilé de l'extension, `extension/out/src/lepton.js`, par node)
sur le stderr de 03 : même texte avec ou sans les lignes `scion:` (`lepton: erreur: échec de
« scion seed-clone … » … → corriger la cause signalée par scion, puis relancer`).

Commandes de l'extension (`extension/src/commands.ts`) : `seedAdd` lance `seed add <nom>
<origine> --type <type> --version <v>` ; `seedRemove` lance `seed remove <nom>`. Libellés
français : « Lepton : ajouter un greffon à la graine », « retirer un greffon de la graine » ;
notifications « lepton : ajouter stm32f7xx — terminé », « lepton : {0} — échec (code {1}) {2} ».

Constats, hors du périmètre de l'étape (pour `HORS-PLAN.md`) :
- **O-1** : `lepton seed add absent file:///Users/…/env-53-absent.git` (trois barres) donne
  `lepton: erreur: origine locale « file:///… » : <C>/file:/Users/…/scion absent` (code 1).
  lepton prend `file:///…` pour un chemin local relatif au répertoire courant ; `file://localhost/…`
  est reconnu comme URL. Relevé : `env-53-mac/c5/constat-file-3-barres/`.
- **O-2** : après l'échec d'un `seed add` (03, 06), un répertoire vide
  `depots/lepton/library-absent` reste dans le rootstock (résidu du clonage avorté). L'entrée de
  la graine et le trunk sont, eux, restaurés. Retiré par `rmdir` dans la copie d'essai.

### 1.6 Consigne

`consignes/env-53-debian.md`, reprise d'`env-50-debian.md`.

| Critère | Contenu |
| --- | --- |
| C1 | Versions, git ≥ 2.35 ; installation par l'utilisateur de scion 0.6.3.0 (`install-debian.sh` du noyau 58e421e, défaut `SCION_REF`), de lepton (`pipx`) et de VSCodium (`install-vscodium.sh` ×2), avant toute regreffe |
| C2 | `graft-update` de `essais/env-28-debian` par l'utilisateur ; seul le noyau avance ; liens inchangés, `CONFORME` ; extraits et `sparse-checkout` = Mac (16 fichiers) ; `ignorecase` et tailles relevés ; puis rootstock neuf `essais/env-53-debian` (mêmes contrôles) |
| C3 | Host et 16 presets contre `env-50-debian` : code 0 ×16, mklepton identique ; QEMU 20/20, 16/16, 19/19 |
| C4 | `graft-update` d'`essais/env-13-debian` par l'utilisateur, mêmes contrôles, `check` 0, espace = avant |
| C5 | pytest 384 (hook 118) ; relais en ligne de commande sur `essais/env-53-c5` (copie de `$P`) : 12 relevés = Mac ; essai dans VSCodium par l'utilisateur (3 notifications, 8 lignes `scion:` dans le canal) ; fichiers générés (`$R` contre `$R50`, `$U`, `$P`) |
| C6 | `mirror-sync --dry-run` dans `$R`, 8 miroirs, 0 à envoyer |
| C7 | écarté (aucune carte) |
| C8 | `rm -rf essais/env-50-debian ~/env-50-journaux` par l'utilisateur, après le §10.1 |

Écart au fichier d'étape, soumis au PA-93 : l'étape prévoit la regreffe d'`essais/env-50-debian`
en C4. La consigne ne la fait pas : ce rootstock sert de référence d'espace au §10.1, puis il est
supprimé en C8 (orientation de l'utilisateur). La conversion d'un rootstock existant est prouvée
par `$U` (C2) et `$E13` (C4).

Les blocs de contrôle de la consigne (contrôles communs du §7, comparaison des relevés du §9.2)
ont été éprouvés en bash au Mac, sur `env-13-vierge` et `env-53-c5` : `CONFORME`, écarts=0,
`clones = Mac`, 12 relevés = Mac.

## 2. PA-93 (2026-11-12, décisions de l'utilisateur)

- Consigne `consignes/env-53-debian.md` validée telle quelle, C1 à C8 : C3 sans écart admis ;
  C5 en ligne de commande et dans VSCodium ; C7 écarté ; C8 forme d'ENV-50.
- Écart au fichier d'étape accepté : pas de regreffe d'`essais/env-50-debian` en C4.
- Précision : pour R53-1, la session VM lance elle-même les commandes marquées « l'utilisateur
  lance » (`sudo` sans mot de passe sur la VM). Reportée au §2 de la consigne avant l'envoi ;
  un refus du classifieur reste confié à l'utilisateur ; l'essai dans VSCodium reste à
  l'utilisateur.
- PA-P : push de `devenv/env-53`, ordre `R53-1` à `debian-linux-vm`.
- PA-P (tâche 3) : regreffe des 6 autres rootstocks d'essai pendant R53-1 ; suppression
  d'`essais/env-39-copie` et d'`essais/env-53-c5`.

## 3. Messages §2bis

| Message | Date | Sens | Résumé |
| --- | --- | --- | --- |
| ORDRE R53-1 | 2026-11-12 | Mac (`lepton-tools-3b`) → VM (`debian-linux-vm`) | consigne `env-53-debian.md` @ 087dd49 envoyée en entier, branche `devenv/env-53` @ 087dd49 (poussée) ; précision du PA-93 (la session VM lance les commandes, `sudo` sans mot de passe ; refus du classifieur → utilisateur) ; essai VSCodium par l'utilisateur ; pas de cartes ; envoi réussi par Remote Control, lecture non confirmée |
| ACCUSÉ R53-1 | 2026-11-12 | VM → Mac | reçu directement (non relayé). §5 sans arrêt : `devenv/env-53` = 087dd49 ; `têtes publiées = Mac` ; Debian 13.7, noyau 6.12.107, utilisateur `lepton-user`, git 2.47.3 ; scion 0.6.2.0 et lepton 0.1.0 avant installation ; chaîne = R50-1 ; embOS et `venv-test` présents, node absent ; 17 Go libres ; `$U` et `$E13` identiques : graine 15740f9, 23 entrées, 13 clones sur `master` aux commits de R50-1 (noyau 76f28bd), `modifs=0`, 3889 liens, 8 clones tiers, `depots/tiers` 259 792 Ko (Mac : 247 600 Ko, écart de système de fichiers, sans effet sur les critères) ; `$R50`, `$P`, `~/env-50-journaux` présents, `$R` et `$C5` absents ; 13 étapes prévues, commandes lancées par la session avec `AVANCEMENT` préalable |
| AVANCEMENT R53-1 (§5.1, §6) | 2026-11-12 | VM → Mac | §5.1 : `generate` et `check` de `$P`, `$R50`, `$U`, `$E13` à code 0 ; graine `env11` propre ; §6 : noyau 76f28bd → 58e421e par avance rapide, `SCION_REF` 0.6.3.0 (noyau, lepton-tools), `SCION_MIN_VERSION` (0, 6, 2, 0), `.vsix` 0.5.2 présent ; installations du §6 lancées par la session (PA-93) |
| AVANCEMENT R53-1 (§6, C1 ; §7.1 avant) | 2026-11-12 | VM → Mac | 4 commandes du §6 à code 0, lancées par la session : scion 0.6.3.0 depuis `seed.scions.git@0.6.3.0`, lepton 0.1.0 (« scion 0.6.3.0 (requis ≥ 0.6.2.0) »), `install-vscodium.sh` ×2 `changements 0` (la première comprise) ; chaîne = R50-1, OpenOCD 0.12.0 ; codium 1.135.06055 ; extensions = attendu. §7.1 avant : `$U` 3889 liens, 8 clones tiers en extraction complète (`sparseCheckout`, `ignorecase` vides, `S=0`), `depots/tiers` 259 792 Ko ; `graft-update` de `$U` lancé par la session |
| AVANCEMENT R53-1 (§7.1, refus) | 2026-11-12 | VM → Mac | `graft-update` de `$U` refusé par le classifieur de la VM (« Modify Shared Resources », comme R28-1) ; rien exécuté, `$U` intact ; pas de contournement ; attente de l'utilisateur pour la commande exacte du §7.1 ; refus attendu aussi pour `$E13` (§7.3) |
| AVANCEMENT R53-1 (§7.1, §7.2, C2) | 2026-11-12 | VM → Mac | `$U` (`graft-update` par l'utilisateur) : code 0, 0 conflit, aucun `git clone` ; seul le noyau avancé (76f28bd → 58e421e) ; 8 lignes `extraction partielle` aux nombres attendus ; 3889 feuilles, 23 entrées ; liens inchangés ; `CONFORME` ; extraits et `sparse-checkout` : écarts=0 sur 16 ; `clones = Mac` ; `ignorecase` vide ×8 ; `depots/tiers` 259 792 → 108 760 Ko. `$R` neuf : codes 0, mêmes conversions, `CONFORME`, écarts=0, liste = `$U`, `.git` neufs (STM32CubeWL 3 588 Ko), `depots/tiers` 87 512 Ko. §7.3 avant : `$E13` conforme au §5 ; `graft-update` confié à l'utilisateur |
| AVANCEMENT R53-1 (§7.3, C4 ; §8 lancé) | 2026-11-12 | VM → Mac | `$E13` (`graft-update` par l'utilisateur) : code 0, 0 conflit, aucun `git clone` ; seul le noyau avancé ; 8 conversions ; 3889 feuilles, 23 entrées ; liens inchangés ; `CONFORME`, écarts=0 sur 16, `clones = Mac`, `ignorecase` vide ; tailles = `$U` ; `depots/tiers` 259 792 → 108 760 Ko ; `check` 0 (19 fichiers), `generate` 0, espace = avant. §8 : `devenv/env-53-debian` créée depuis 087dd49 ; `rejouer-oracle.sh` en cours |
| AVANCEMENT R53-1 (§8, C3 ; §10.2, §10.3) | 2026-11-12 | VM → Mac | `rejouer-oracle.sh` code 0 ; host 7/7 ; 16 presets ; fumée ×6 ; bancs an386 20/20 ×2, soft 16/16 ×2, an500 19/19 ×2 ; `peripheriques` ×4 ; trunk de `$R` 3889, 0 cassé, 0 régulier, 0 `__pycache__` ; §8.1 : mklepton = R50-1 = `env-52-apres` ; `comparer_R50-1` 0 et `hors_debug=0` ×16 ; `comparer_Mac` 1 (informatif). Réordonnancement annoncé : §10.2 (`$U` : codes 0, 9 projections, espace = avant) et §10.3 (`$P` : générés, graine, `check` identiques) faits pendant le §8 ; relevé du §13 : `$R50` 655 Mo, `~/env-50-journaux` 6,5 Mo ; pytest (§9.1) lancé |
| QUESTION R53-1 (§9.2) | 2026-11-12 | VM → Mac | 01 (`seed add stm32f7xx`) code 2 : 208 conflits de greffe (« déjà fourni par lepton/original::tree »). Cause : `$P` de la VM pas dans l'état du `$P` du Mac. Sur la VM, `$P` n'a pas été regreffé depuis ENV-10 : noyau 1dde0af (2026-10-15), qui porte encore le F7 ; an386 046779e ; `salut` `modifs=2` ; copie à 3428 liens (Mac : 3059). Défaut de la consigne : elle supposait cet état sans l'avoir relevé. Le relais de l'échec est conforme (4 lignes `scion:` préfixées, stderr de l'erreur une seule fois, non préfixé) ; liens et graine restaurés ; restent dans `$C5` les clones F7 créés avant l'échec. Options : O1 C5 partiel, O2 remettre `$C5` à la base du Mac, O3 autre. La VM poursuit §9.1, §10.1 et §11 en attendant |
| ORDRE R53-1 (réponse à la QUESTION du §9.2) | 2026-11-12 | Mac → VM | option O2, décision de l'utilisateur : premier essai conservé dans `$J/9.2-essai1/` (écart de base) ; `rm -rf` de `$C5` par l'utilisateur ; nouvelle copie par la session ; `graft-update -v` de la copie seule par l'utilisateur (noyau → 58e421e, an386 → 10a8889), contrôles, puis §9.2 et §9.3 en entier ; `$P` non touché ; envoi réussi, lecture non confirmée |
| AVANCEMENT R53-1 (§10.1, §11, C6) | 2026-11-12 | VM → Mac | (croisé avec la réponse) §10.1 : `$R` `check`, `generate`, `seed status` 0, 9 projections, espace 23/10/7/4/0, espace = `$R50` au chemin près ; §11 : `mirror-sync --dry-run` code 0, 8 miroirs à 0 référence et 0 signalement, 78 Mo sous `depots/.mirrors`, trunk `CONFORME`, rien envoyé ; §13 possible ; attente de la réponse et de pytest |
| AVANCEMENT R53-1 (§9.1 ; O2 étape 1 ; §13) | 2026-11-12 | VM → Mac | complément O2 reçu ; pytest (`venv-test`, pytest 9.1.1) : 384 passed en 177,56 s, rien d'ignoré ; hook 118 passed ; lepton-tools propre hors `oracles/env-53-debian/` ; premier essai rangé dans `$J/9.2-essai1/` (avec l'inventaire final de la copie : `family-stm32f7xx` résiduel, noyau 1dde0af, 143 Mo) ; suppressions confiées à l'utilisateur en une fois, le classifieur ayant déjà refusé des `rm -rf` : `env-53-c5`, puis `env-50-debian` (655 Mo) et `~/env-50-journaux` (6,5 Mo) |
| AVANCEMENT R53-1 (§13, C8 ; O2 étapes 2 et 3) | 2026-11-12 | VM → Mac | `rm -rf` lancés par l'utilisateur ; `env-53-c5`, `env-50-debian`, `~/env-50-journaux` absents (C8). Copie refaite (`copie=0`) : 3428 liens, 0 cassé, 0 régulier ; `salut` 71e1641, sans amont, `modifs=2` (`salut.c` modifié, `salut_message.c` non suivi : état d'origine de `$P` ; au Mac, `salut` 4e1df4c, `modifs=0`) ; graine `env11` 6d3d2a5 ; an386 046779e, noyau 1dde0af ; `graft-update` de la copie confié à l'utilisateur (étape 4) |
| AVANCEMENT R53-1 (O2 étapes 4 à 6 ; §9.2) | 2026-11-12 | VM → Mac | `graft-update` de `$C5` par l'utilisateur : code 0, 0 conflit ; noyau 1dde0af → 58e421e, an386 046779e → 10a8889 ; `salut` accepté (sans amont, `modifs=2`) ; 3059 feuilles ; liens 3059 = Mac ; `generate` et `check` 0. §9.2 repris : 01 code 0, 5 `scion:` dans l'ordre attendu, 3271 liens, clones F7 partiels = Mac ; `--json` valide ; 02 code 0, 3 `scion:` (P-P6) ; 03 code 2, 2 `scion:`, erreur non préfixée une seule fois ; liens et graine restaurés ; 11 relevés sur 12 = Mac, `03-seed-add-echec.err` ligne 5 = message de git en français (« et que le dépôt existe. »), prévu au §9.2 ; résidu `library-absent` retiré. §9.3 en cours avec l'utilisateur |
| AVANCEMENT R53-1 (§9.3, C5 ; rapport) | 2026-11-12 | VM → Mac | essai dans VSCodium par l'utilisateur : 3 notifications attendues ; texte de l'échec relevé, sans ligne `scion:` ; canal « Lepton » de 60 lignes, dont 8 `scion:` (3 + 3 + 2) ; `→ code` 0, 0, 2 pour les actions, plus 6 `→ code 0` des `seed status --json` que l'extension lance d'elle-même ; lignes de 04-ext et 05-ext présentes, 06-ext 5 sur 6 (langue de git) ; liens et graine restaurés ; `library-absent` retiré. Rapport et oracle commités en f8090af sur `devenv/env-53-debian`, non poussés ; accord du push demandé à l'utilisateur (PA-P) |
| FIN-SUCCÈS R53-1 | 2026-11-12 | VM → Mac | reçu. C1 à C6 et C8 atteints, C7 écarté ; C5 après la reprise O2 ; commit f8090af sur `devenv/env-53-debian`, poussé avec l'accord de l'utilisateur ; rapport `rapports/env-53-debian.md`. Écarts déclarés : base de `$P` (premier essai conservé), `graft-update` et `rm -rf` lancés par l'utilisateur après refus du classifieur (installations par la session), ordre (§10.2, §10.3 pendant le §8 ; §9.1, §10.1, §11 pendant la QUESTION), git en français, `ignorecase` vide, tailles, 6 `seed status --json` de l'extension, `library-absent` ×2. Non fait : C7, regreffe de `$P`, `~/tmp-pytest` |

## 4. Rootstocks d'essai du Mac (tâche 3)

Accord de l'utilisateur (PA-P, PA-93) : regreffe des 6 autres rootstocks pendant R53-1 ;
suppression d'`essais/env-39-copie` et d'`essais/env-53-c5`. scion 0.6.3.0, lepton 0.1.0.
Script `env-53-mac/regreffer-essai.sh` (forme d'`env-50-mac.md` §4, plus le relevé des clones
tiers avant et après). Attendu des liens : la liste d'avant du rootstock, puisque 58e421e ne
change rien de greffé. Journaux : `~/lepton-tools-dev/essais/env-53-mac/regreffes/`.

Inventaire avant (`inventaire-clones.sh`) :
- clones de greffons sur `master`, amont `origin/master`, propres ;
- graines de projet locales sur `main`, sans amont, propres ;
- noyau à 76f28bd partout, les autres aux têtes publiées.

La graine de `bout-en-bout` porte 2 fichiers non suivis du 2026-11-02 :
`project/scion/CMakeUserPresets.json` et `scion/.scion/lepton-graine.lock.json`. Ils étaient
déjà là en ENV-50 et scion ne les compte pas.

| Rootstock | `graft-update` | Liens avant → après | Ajouts / retraits | `controler-trunk.py` | Clones tiers | `check` | `generate` | Espace |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `env-9` | 0 ; noyau 76f28bd → 58e421e seul | 3059 → 3059 | 0 / 0 | `CONFORME` | — | 0 | 0 | identique |

Le classifieur de permissions du Mac a refusé la commande suivante (« Modify Shared
Resources »). Elle enchaînait `env-11/qemu`, `qemu-gra2` et `bout-en-bout`, avec un `sed -i` du
script. Elle n'a rien exécuté : les noyaux de ces rootstocks sont restés à 76f28bd. Le refus
n'est pas contourné : la suite est soumise à l'utilisateur.

`essais/env-39-copie`, relevé avant suppression (2026-11-12) :
- 169 Mo ;
- clone noyau à 2893297, sur `master`, propre ;
- `family-stm32f4xx` sur `master` avec 207 suppressions non commitées (`git rm` d'ENV-39), sans
  rien de publié à garder ;
- 2 clones tiers d'origine `file://localhost/…/tiers/…`, en extraction complète (42 Mo). Ils
  ne relèvent pas de P-V7, qui exclut les emplacements locaux.

## 5. Vérification du rapport VM (tâche 4)

Branche `devenv/env-53-debian` récupérée à f8090af (un commit sur `devenv/env-53` 087dd49). Elle
n'ajoute que `rapports/env-53-debian.md`, `rapports/env-53-debian/` et
`rapports/oracles/env-53-debian/` (124 fichiers), et ne touche à aucun autre chemin. Contrôles
refaits au Mac sur le contenu poussé, extrait par `git archive` dans le répertoire de session :

| Critère | Contrôle refait au Mac | Résultat |
| --- | --- | --- |
| C2, C4 | `clones.txt` de `$U`, `$R`, `$E13` après la greffe, contre `attendu/clones-rootstock-mac.txt` (hors `ignorecase` et tailles) | identiques ×3 ; `ignorecase` vide pour les 8 clones ×3 ; avant la greffe, `$U` et `$E13` : 8 × `sparseCheckout=` vide, `S=0` |
| C2, C4 | `controle.log` de `$U`, `$R`, `$E13` | `CONFORME`, code 0 ×3 : 3889 liens identiques à l'attendu, 0 régulier, 0 cassé, 629 projetés, 0 écart de casse ni de contenu |
| C3 | `comparer-oracle.py` `env-50-debian` → `env-53-debian`, 16 presets | **0 ×16** ; contre `env-52-apres` : 1 ×16 (chaînes différentes, informatif) |
| C3 | `mklepton-empreintes.sha256` | = `env-50-debian` et = `env-52-apres` |
| C3 | `ctest.log`, `banc-kal.log` | host 7/7 ; 20/20 ×2, 16/16 ×2, 19/19 ×2 ; `peripheriques` Passed ×4 |
| C5 | `9.2-releves/` normalisés (`/home/lepton-user/…/env-53-c5` → `<C>`, `/home/lepton-user` → `<HOME>`) contre `attendu/c5/` | 11 sur 12 identiques ; `03-seed-add-echec.err` ligne 5 : seule la fin du message de git diffère (« et que le dépôt existe. » au lieu de « and the repository exists. ») |
| C5 | `9.3-sortie-lepton.txt` | 8 lignes `scion: ` ; `→ code` : 11 × 0 (3 actions et 8 appels `--json` de l'extension) et 1 × 2 |

Le rapport VM a bien les rubriques demandées au §14 de la consigne : hôte et versions, critères,
presets, contrôles du trunk et des clones, pytest, relais, fichiers générés, miroir, écarts,
messages, non fait.

Écarts retenus pour la clôture :
- **Défaut de la consigne** (session Mac) : l'état de `$P` sur la VM n'avait pas été relevé.
  La reprise O2, décidée par l'utilisateur, a fourni la preuve complète. Le premier essai est
  conservé (`env-53-debian/9.2-essai1/`) : il montre le relais d'un échec conforme sur une
  autre base.
- `graft-update` et `rm -rf` refusés par le classifieur de la VM malgré la précision du PA-93,
  puis lancés par l'utilisateur, comme en R28-1. Les installations du §6 ont été lancées par la
  session.
- Messages de git localisés en français sur la VM.
- `core.ignoreCase` non posé sur la VM (attendu).

Les constats O-1 et O-2 (§1.5) sont confirmés sur la VM pour O-2 : `library-absent` vide, deux
fois.
