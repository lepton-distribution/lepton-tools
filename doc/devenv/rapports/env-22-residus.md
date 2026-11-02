# ENV-22 — Résidus d'ENV-17 à ENV-21 — 2026-11-02

Session Mac. Branche lepton-tools `devenv/env-22` (depuis `main` eec7b60). Fichier d'étape :
`etapes/ENV-22-residus.md`.

État de départ : lepton-tools `main` eec7b60, clone noyau `master` 40d7197, graine `original-tree`
15740f9, seed.scions `master` 472c12e (0.5.2.0), tous propres et alignés sur leurs distants ;
scion 0.5.2.0, lepton 0.1.0. `<ROOTSTOCK>/trunk` : 3941 liens, 0 cassé, 0 fichier régulier hors
`.scion.grafted.list`, 0 `.DS_Store`/`._*`.

## 1. Audit (tâche 1, lecture seule)

### 1.1 `.scion.trunk.tolerated`

- **Format (scion 0.5.2.0)** : `<rootstock>/.scion.trunk.tolerated`, un motif `fnmatch` par ligne,
  appliqué au nom du fichier (sensible à la casse, `fnmatchcase`) ; lignes vides et `#` ignorées
  (`scion/graft.py` `_tolerated_patterns`, `_is_tolerated`). Absent : rien n'est toléré.
  `rootstock-install` (hors `--bare`) l'écrit avec l'en-tête `TOLERATED_HEADER` sans motif
  (`scion/rootstock.py`). `<ROOTSTOCK>`, installé avant 0.5.2.0, n'en a pas.
- **Effet** : un fichier toléré ne bloque ni `ungraft`, `graft`, `graft --scion`, `graft-remove`,
  `graft-clean`, `graft-update` ; `ungraft` le supprime (« supprimé (toléré) »), `graft --scion`
  et `graft-remove` le suppriment avec le répertoire qu'ils retirent (`CHANGELOG.md` 0.5.2.0).
- **Modèle** : le fichier écrit en ENV-21 dans les 6 rootstocks d'essai
  (`essais/env-9/.scion.trunk.tolerated`) : en-tête de scion, puis
  `# Fichiers du Finder (ENV-21, décision de l'utilisateur du 2026-10-31)`, `.DS_Store`, `._*`.
- **Interaction avec la purge de lepton** : `lepton.seed.scion_on_trunk` supprime les fichiers
  système réguliers du trunk (`is_system_file` : `.DS_Store`, `._*`, `lepton/rootstock.py`) avant
  tout `scion graft` / `graft-remove` lancé par lepton ; `check_trunk` ne les compte pas comme
  réguliers. Les deux mécanismes visent les mêmes noms : ils sont redondants et compatibles. Le
  fichier de tolérance couvre les appels directs de scion (`scion graft`, `graft-update`, que les
  sessions lancent d'après la skill `lepton-rootstock`), qui ont bloqué en ENV-17 et ENV-21.
  Aucune modification de lepton n'est nécessaire.
- **Limite** : la tolérance ne vise que les fichiers **réguliers** du trunk. Un `.DS_Store` créé
  dans une source non git (`depots/generation/building`) est greffé en **lien** (incident du début
  d'ENV-20) ; il n'est pas couvert. C'est l'objet du filtrage des sources non git d'ENV-23 (PA-33).
- **`.DS_Store` hors trunk** (constat, sans effet sur le greffage) : `<ROOTSTOCK>/.DS_Store`,
  `<ROOTSTOCK>/depots/.DS_Store`.

Proposition de contenu pour `<ROOTSTOCK>/.scion.trunk.tolerated` : identique au modèle, avec la
ligne de commentaire `# Fichiers du Finder (ENV-22, décision de l'utilisateur du <date PA-31>)`.

### 1.2 Propositions appliquées sans validation séparée

| ID | Étape | Proposition | État constaté (2026-11-02) |
| --- | --- | --- | --- |
| P-1 | ENV-17 | `ORCHESTRATION.md` §2 : distant `lepton-distribution/lepton-tools` (« prévu » retiré) ; rôle de `seed.scions` avec ses étapes | présent (§2 ; étapes ENV-7, ENV-15, ENV-23 depuis la révision du 2026-10-31) |
| P-2 | ENV-17 | Commentaire au-dessus du message M-1 de `kernel.cmake` (« BSP par manifeste … sources dans la bibliothèque du greffon BSP ; hôte : aucune carte ») | présent, 350d914 dans `master` 40d7197 |
| P-3 | ENV-18 | Information de `generate` : « BSP « X » non greffé : preset(s) … : tâches configurer et construire seulement, sans lancement » | présent, `lepton/generate.py` (fonction d'affichage, boucle `ctx.ungrafted`) |
| P-4 | ENV-18 | `build_type` vide quand un preset n'a pas `CMAKE_BUILD_TYPE` | présent, `lepton/generate.py` (`variables.get("CMAKE_BUILD_TYPE", "")`) |
| P-5 | ENV-19 | Branche par défaut GitHub remise à `master` sur `lepton-famille-{stm32f7xx,samd21}`, `lepton-bsp-{stm32f746g-disco,samd21-xplained-pro}` | `master` sur les 4 (`gh repo view`) ; constat : leurs distants gardent `devenv/env-19` |
| P-6 | ENV-19 | Contrôle `LEPTON_CPU` du module SAMD21 retiré (redondant avec le cœur du manifeste) ; message FPU de F746 conservé | retiré (aucune occurrence dans `family-samd21`) ; proposition du rapport d'ENV-19 §3.4, « non contestée au PA-25 » : ajoutée à la liste du fichier d'étape |
| P-7 | ENV-20 | Alias faibles vers un relais local `stm32f4xx_irq_default` ; table étendue renommée `stm32f4xx_vector_table_ext` | présents, `family-stm32f4xx` 2fb7cfe, `stm32f429xx_vectors.c` |
| P-8 | ENV-20 | Description GitHub « lepton bsp nucleo f439zi » | présente ; même forme que les 5 autres dépôts relevés ; constat : le distant garde `devenv/env-20` |

Aucune n'a d'effet sur les binaires (oracles d'ENV-17 à ENV-20).

### 1.3 `essais/env-11/bout-en-bout`

| Élément | Relevé |
| --- | --- |
| Origine | sortie de `scripts/bout-en-bout.sh essais/env-11/bout-en-bout` (ENV-11, `rapports/env-11-mac.md`) : `rootstock/` « jetable » et `bout-en-bout.log` ; le script refuse un `rootstock/` non vide |
| Espace | 105 Mo (`rootstock/`), journal 93 Ko |
| Graine | `depots/lepton-seed/bout-en-bout` d6c9548 (« créée par lepton seed new »), sans distant ; 1 fichier non suivi (`scion/.scion/lepton-graine.lock.json`) ; sans `lepton-graine.json` (antérieure, `env-16-graine.md`) |
| Entrées | 4 : `building`, `original::tree`, `family-qemu-mps2`, `bsp-qemu-mps2-an386` |
| Clones | noyau a572f00 (ENV-11) ; famille 3954357 et BSP 046779e (ENV-6) ; origines `file://localhost~/lepton/depots/lepton-famille/qemu-mps2` et `…/lepton-bsp/qemu-mps2-an386`, **supprimées le 2026-10-30** |
| Trunk | 3424 liens, 0 cassé ; 5 `.DS_Store` réguliers (`trunk/`, `sys/`, `sys/root/`, `sys/root/src/`, `sys/root/src/kernel/`) ; pas de `.scion.trunk.tolerated` |
| Constructions | `build/host`, `build/qemu-mps2-an386-freertos` |
| Usage | ENV-11 (bout en bout) ; ENV-12 lots 3 à 6 (`scripts/bout-en-bout.sh` relancé, rootstocks jetables) ; ENV-16 et ENV-18 (relevés `check`, `seed status`, `tree`, `owner` en lecture) ; exclu du regreffe d'ENV-21 (décision de l'utilisateur) |

Conséquences : un `graft-update` ne peut pas rafraîchir la famille et le BSP (origines absentes) ;
un regreffe suppose de réécrire les sources (clés inchangées, URL vers
`~/lepton/depots/lepton/{family,bsp}-…/master` ou GitHub) et d'ajouter le fichier de tolérance.

### 1.4 Constat nouveau N-1 : `scripts/bout-en-bout.sh` cassé

`scripts/bout-en-bout.sh` ligne 27 : `depots_ref=(lepton/original/master lepton-famille/qemu-mps2
lepton-bsp/qemu-mps2-an386)`. Les deux derniers dépôts ont été supprimés le 2026-10-30 (ENV-13,
PA-14) ; le script échoue depuis (relevé d'état `git -C … rev-parse` et clonage
`file://localhost…`). Correction proposée (lepton-tools, hors binaire) :
`lepton/family-qemu-mps2/master` et `lepton/bsp-qemu-mps2-an386/master`.

### 1.5 Constat nouveau N-2 : défaut de `lepton scion new --repo`

Défaut `depots/lepton-<kind>/NAME` (`lepton/cli.py`, `lepton/scions.py`), différent de la
convention d'ENV-13 `depots/lepton/<kind>-<nom>/master` (déjà relevé au fichier d'ENV-20 ; ENV-20 a
passé `--repo`). `README.md` ligne 31 décrit ce défaut. Hors du périmètre d'ENV-22 (code de lepton,
tests) : à consigner pour une étape ultérieure, sauf décision contraire.

### 1.6 Règles des consignes VM

- **E-1** (`rapports/env-21-debian.md` §4) : C6 a comparé une empreinte de
  `env11.code-workspace` écrit en ENV-12 à une régénération ; la différence ne vient pas des
  étapes validées. Règle : régénérer un fichier généré avant d'en relever l'empreinte « avant ».
- **E-2** (`rapports/env-21-debian.md` §4, `rapports/env-15-scion.md` §8) : le classifieur de
  permissions de la session VM refuse `rm -rf` (R21-1) et `pipx install`, le clonage et les tests
  de scion (R15-1), malgré l'accord du point d'arrêt. Règle : la consigne attribue d'emblée ces
  commandes à l'utilisateur, avec la commande exacte, et la session VM vérifie leur effet.
- **Emplacements** : `consignes/MODELE.md` n'existe pas. Les consignes reprennent chacune un §2
  « Ce que la session VM peut faire, et ne fait pas » et un §3 « Communication » qui renvoie à
  `ORCHESTRATION.md` §2bis. `etapes/ENV-28-validation-debian.md` cite « Règles des consignes VM
  écrites en ENV-22 » sans emplacement.
  - Option A : paragraphe « Règles des consignes VM » dans `ORCHESTRATION.md` (§2bis ou à sa
    suite), lu en entier à chaque session ; aucun fichier nouveau.
  - Option B : `consignes/MODELE.md`, squelette de consigne (§1 à §11) avec les règles ; plus long à
    tenir à jour, utile à la rédaction.
  - Proposition : option A ; ENV-28 y renvoie par son titre.

### 1.7 Questions du PA-31

1. Contenu de `<ROOTSTOCK>/.scion.trunk.tolerated` (§1.1).
2. Propositions P-1 à P-8 : confirmation en bloc ou une par une (§1.2).
3. Sort de `essais/env-11/bout-en-bout` (§1.3) et correction N-1 (§1.4).
4. Emplacement des règles des consignes VM (§1.6).
5. N-2 : consigner pour plus tard (§1.5).

### 1.8 Décisions du PA-31 (2026-11-02)

1. Fichier de tolérance validé tel quel.
2. P-1 à P-8 confirmées en bloc.
3. `bout-en-bout` : corriger le script (N-1), archiver, supprimer (accord explicite donné après
   vérification de l'archive), relancer au même endroit.
4. Règles des consignes VM : `ORCHESTRATION.md` §2bis.
5. N-2 : consigné pour ENV-23 (PA-33, « effets sur lepton »), aucune modification en ENV-22.

## 2. Application (tâche 2)

### 2.1 `<ROOTSTOCK>/.scion.trunk.tolerated`

- Écrit à la racine de `~/lepton` (hors trunk) : en-tête `TOLERATED_HEADER` de scion 0.5.2.0,
  `# Fichiers du Finder (ENV-22, décision de l'utilisateur du 2026-11-02)`, `.DS_Store`, `._*` ;
  identique au fichier d'`essais/env-9` hors la ligne de commentaire.
- Trunk avant : 0 `.DS_Store`/`._*`. `scion graft` : code 0, « 3941 feuilles liées », 11 chemins
  ignorés par git (E1 d'ENV-15, comme avant).
- Liste triée `chemin -> cible` des liens : 3941 avant et après, SHA-256
  `d2393067a5c9bb67f791b83af7c64932fbb67192999c59e4bda0058eb011aca3` des deux côtés (`cmp` :
  identiques).

### 2.2 Règles des consignes VM

`ORCHESTRATION.md` §2bis, paragraphe « Règles des consignes VM » (régénérer avant de relever ;
suppressions, `pipx install`, clonages et tests confiés d'emblée à l'utilisateur, effet vérifié
par la session VM). `etapes/ENV-28-validation-debian.md` §Prérequis y renvoie.

### 2.3 `scripts/bout-en-bout.sh` et `essais/env-11/bout-en-bout`

- N-1 : `depots_ref=(lepton/original/master lepton/family-qemu-mps2/master
  lepton/bsp-qemu-mps2-an386/master)` ; `shellcheck` 0.11.0 : aucun avertissement.
- Archive `~/lepton-tools-dev/essais/archives/env-11-bout-en-bout-20261102.tar.gz` (33 Mo) :
  9033 entrées comme sur le disque, 3424 liens ; seul contenu unique : la graine locale
  `bout-en-bout` d6c9548 (sans distant).
- Suppression de `essais/env-11/bout-en-bout` (105 Mo) après accord explicite de l'utilisateur.
- `scripts/bout-en-bout.sh ~/lepton-tools-dev/essais/env-11/bout-en-bout` (lepton 0.1.0 installé,
  scion 0.5.2.0) : code 0 en 26 s, toutes les étapes (seed new, XML du projet greffé, `check`,
  `seed lock` et `--verify`, cmake host et `qemu-mps2-an386-freertos`, fumée QEMU
  `smoke.lsh` réussie, trunk sain, rootstock de référence inchangé).
- Nouveau rootstock : 89 Mo ; 5 entrées (`building`, `original::tree`, `family-qemu-mps2`,
  `bsp-qemu-mps2-an386`, `project-bout-en-bout`) ; 3054 liens, 0 cassé, 0 fichier régulier ;
  noyau 40d7197, famille 3954357, BSP 046779e (têtes de `<ROOTSTOCK>`), clones propres ; graine
  393e945, `lepton-graine.lock.json` non suivi (écrit par `seed lock`, comme avant) ;
  `.scion.trunk.tolerated` écrit par `rootstock-install` sans motif (défaut de scion 0.5.2.0).

## 3. Contrôles (tâche 3)

| Contrôle | Attendu | Constaté |
| --- | --- | --- |
| Liens du trunk de `<ROOTSTOCK>` | 3941 | 3941 |
| Liens cassés | 0 | 0 |
| Fichiers réguliers (hors `.scion.grafted.list`) | 0 | 0 |
| Liste des liens | inchangée | SHA-256 identique (§2.1) |
| `lepton check` sur `<ROOTSTOCK>` | code 0 | code 0, « 19 fichier(s) conforme(s) », information « graine de référence » |
| Clones de `<ROOTSTOCK>` et graine | propres | propres |

Binaires et images mklepton : aucun code ni fichier de construction modifié ; aucune
reconstruction de `<ROOTSTOCK>` nécessaire (arbre composé identique).
