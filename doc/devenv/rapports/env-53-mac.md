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

## 2. PA-93

En attente.

## 3. Messages §2bis

| Message | Date | Sens | Résumé |
| --- | --- | --- | --- |

## 4. Rootstocks d'essai du Mac (tâche 3)

En attente de l'accord (PA-P).

## 5. Vérification du rapport VM (tâche 4)

En attente.
