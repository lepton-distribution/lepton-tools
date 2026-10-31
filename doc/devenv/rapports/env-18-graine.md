# ENV-18 — Graine de référence gérée par `lepton` : rapport

Session du 2026-10-31, branche lepton-tools `devenv/env-18` (depuis `main` b57d456). Graine
`original-tree` (0f1275a) non modifiée. lepton 0.1.0 installé par pipx depuis 6a40859 (code de
`lepton/` identique à `main`).

## 1. Audit (tâche 1, lecture seule)

### 1.1 Critère de reconnaissance (ENV-16)
`checks.check_rootstock` : graine de référence ⇔ ni `<graine>/scion/.scion/lepton-graine.json` ni
`<graine>/project/`. Graine sans manifeste mais avec `project/` : anomalie (graine de projet
abîmée), inchangé. Le critère est aujourd'hui écrit en ligne dans `check_rootstock` ; seul `check`
l'utilise.

### 1.2 Comportement actuel sur `essais/env-13-vierge` et `<ROOTSTOCK>`
| Commande | Résultat | Code |
| --- | --- | --- |
| `check` | graine de référence reconnue (ENV-16) | 0 |
| `seed status` | « lepton-graine.json absent : rôles non déterminés (graine hors lepton) » ; rôles = type du manifeste de chaque greffon ; `configurations` vide | 0 |
| `seed tree` | « aucun preset configuré » : `tree._presets` lit le manifeste, liste vide ; repli par greffon | 0 |
| `file owner` | ne lit pas le manifeste de graine | 0 |
| `generate` | « lepton-graine.json absent : la graine n'est pas une graine lepton » → « créer le projet par lepton seed new » | 1 |
| `seed lock --verify` | « lepton-graine.lock.json absent » → « lepton seed lock » (commande qui écrirait dans la graine) | 1 |
| `seed add/remove/replace`, `seed mkconf import`, `seed config add/remove`, `scion new` (sans `--no-seed`), `scion remove` | refus par `load_graine` (même texte que `generate`) | 1 |
| `graft`, `file add/remove/mv`, `dir add/remove`, `scion new --no-seed` | ne lisent pas le manifeste de graine ; écrivent dans les clones et le trunk, jamais dans la graine | — |

### 1.3 Ce que lit chaque commande à la place du manifeste
| Champ de graine de projet | Lecteurs | Pour la graine de référence |
| --- | --- | --- |
| `projet.nom` | `generate` (nom de l'espace, préfixe des presets, libellé « graine … »), `seed status` | nom de l'espace : à décider (Q2) ; aucun préfixe (presets du noyau tels quels) |
| `bsp`, `configurations` | `generate` (presets, `launch`, tâches), `seed tree` (`_presets`), `seed status` | presets de configuration visibles de `<trunk>/CMakePresets.json` (`checks.kernel_presets`, héritage résolu) dont `LEPTON_BOARD` est un BSP greffé ; BSP = ce greffon ; exécution `qemu` si le BSP déclare `qemu.machine`, `carte` s'il déclare `openocd` ; construction = `CMAKE_BUILD_TYPE` du preset |
| `backend`, `mklepton_xml`, `options` | `generate` (variables de cache), `schema_settings` | portés par les presets du noyau (`LEPTON_KAL_BACKEND`, `LEPTON_MKCONF`) ; associations XML par `**/mkconf_*.xml` seul ; aucune option de graine |
| `noyau`, `applications`, `bibliotheques` | `seed status` (rôles) | rôle = type du manifeste de greffon (comportement actuel) |

Presets du noyau (clone 8ba904b) : 15 visibles, plus `base` et `cross` cachés ; les build et
test presets existent pour chacun ; `binaryDir` = `${sourceDir}/../build/${presetName}`, soit
`<ROOTSTOCK>/build/<preset>` — même convention que `generate` (`build/<preset>`).

| BSP | Presets | Greffé | Exécution déclarée |
| --- | --- | --- | --- |
| `qemu-mps2-an386` | `-embos`, `-embos-soft`, `-freertos-soft`, `-freertos` | oui | qemu `mps2-an386` |
| `nucleo-f429zi` | `-embos`, `-freertos` | oui | carte (`debug/openocd-nucleo-f439zi.cfg`) |
| `qemu-mps2-an500` | `-embos`, `-freertos` | oui | qemu `mps2-an500` |
| `nucleo-wl55jc1` | `-embos`, `-freertos` | oui | carte (`debug/openocd-nucleo-wl55jc1.cfg`) |
| `stm32f746g-disco`, `samd21-xplained-pro` | 2 + 2 | non (repli `cmake/boards`, ENV-19) | — |
| — | `host` | — | mklepton et tests hôte |

Le BSP varie d'un preset à l'autre (cœur M4F ou M7, machine QEMU, OpenOCD) : `generate.Context`
suppose un BSP unique pour toute la graine (`ctx.bsp`, `ctx.core`) ; il faut un BSP par
configuration.

### 1.4 Fichiers écrits par `generate` (graine de projet) et leur sort ici
| Fichier | Graine de projet | Graine de référence |
| --- | --- | --- |
| `<graine>/project/scion/CMakeUserPresets.json`, greffé à la racine du trunk (`graft_project` : `seed-scion-add`, `seed-clone`, `graft --scion lepton@project-<projet>`) | écrit si changé | rien : écrirait dans la graine publiée et y déclarerait un greffon. Un `CMakeUserPresets.json` hors graine est impossible (racine du trunk = liens greffés, FIC-3) |
| `<ROOTSTOCK>/<projet>.code-workspace` | écrit si changé | écrit, hors du trunk (nom : Q2) |
| `build/.active/compile_commands.json` (amorce, O10) | copie du premier preset configuré | idem, parmi les presets offerts |
| `build/<preset>/.cmake/api/v1/query/client-lepton/query.json` | un par configuration | un par preset offert (fichier de requête seul, binaires inchangés) |
| contrôle du trunk (`finish`) | oui | oui |

### 1.5 Extension 0.5.1
Aucune logique propre aux graines de projet : la vue IDE-1 lit `seed tree --json`, le traceur de
débogage et l'observateur de greffe lisent `trunk` et `scions[].stem` de `seed status --json`
(déjà fournis pour la graine de référence), la palette transmet les commandes à lepton et affiche
son refus, `seed config remove` liste `configurations` (vide ici). Les diagnostics portent sur les
manifestes de greffon et les XML (associations écrites par `generate`).

## 2. Relevé de référence (avant toute modification)
Script `~/lepton-tools-dev/essais/env-18-releve/releve.sh <dossier>` (hors dépôt), sorties dans
`~/lepton-tools-dev/essais/env-18-releve/avant/<rootstock>/` : `seed status` (texte, `--json`),
`seed tree` (texte, `--json`), `check`, `file owner --json` sur 5 chemins, et rendu de `generate`
sans écriture (`render_presets`, `render_workspace` dans le dossier de relevé). Code de retour de
chaque commande dans `*.code`.

| Rootstock | Graine | `generate` (rendu) | Remarque |
| --- | --- | --- | --- |
| `essais/env-9` | `env9` | 0 | presets identiques au disque ; espace sur disque produit par un lepton antérieur |
| `essais/env-11/qemu`, `f429zi`, `wl55jc1` | `env11`, `env11f4`, `env11wl` | 0 | idem |
| `essais/env-11/bout-en-bout/rootstock` | `bout-en-bout` | 0 | presets et espace absents du disque |
| `essais/env-11/qemu-gra2` | `env11` | 1 (BSP de la graine non greffé) | `status` et `check` à 1 (état d'essai d'ENV-11) |
| `essais/env-13-vierge`, `<ROOTSTOCK>` | référence | 1 (refus) | état à faire évoluer |

Critère d'ENV-18 pour les graines de projet : `diff -r avant apres` vide sur les six premiers.

## 3. Propositions (PA-23)

### Q1. Commandes acceptées et refusées
- Acceptées, lecture : `check` (inchangé), `seed status`, `seed tree`, `file owner` (inchangé).
- Acceptée, écriture hors graine : `generate` (§1.4).
- Acceptées sans changement (n'écrivent pas dans la graine ; modifient clones et trunk comme
  pour un projet) : `graft`, `file add/remove/mv`, `dir add/remove`, `scion new --no-seed`.
- Refusées (écrivent dans la graine) : `seed add`, `seed remove`, `seed replace`, `seed lock`
  (tous modes : le verrou s'écrit dans la graine, `--verify` et `--restore` n'ont pas de verrou à
  lire), `seed mkconf import`, `seed config add`, `seed config remove`, `scion new` sans
  `--no-seed`, `scion remove`. Refus avant toute action, code 1 (refus, `env-8-interface.md` §2) :

  ```
  lepton: erreur: graine de référence <graine> (ni lepton-graine.json ni project/) : lepton seed add modifie la graine, refusé
    → créer un projet par lepton seed new, ou modifier la graine de référence par scion dans son dépôt
  ```
  `scion new` : action « lepton scion new … --no-seed, puis l'ajouter à une graine de projet ».

### Q2. Nom de l'espace de travail
Proposition : nom du répertoire de la graine, `original-tree` →
`<ROOTSTOCK>/original-tree.code-workspace` (identique sur tous les rootstocks issus de la graine
publiée ; dossier « git · graine original-tree »). Variante : nom du rootstock
(`lepton.code-workspace`, `env-13-vierge.code-workspace`).

### Q3. `CMakeUserPresets.json`
Proposition : aucun fichier écrit, aucun greffon projet déclaré ; CMake Tools lit directement
`<trunk>/CMakePresets.json` du noyau (`cmake.useCMakePresets: always`, déjà dans l'espace) ;
tâches et `launch` citent les presets du noyau par leur nom.

### Q4. Presets offerts
Proposition : les 10 presets croisés à BSP greffé (§1.3, ordre du fichier du noyau) reçoivent
`launch` et tâches (configurer, construire ; QEMU, fumée, banc KAL pour qemu ; flasher pour
carte) ; `host` garde ses tâches actuelles (configurer host, mklepton), sans `launch` ; les 4
presets F746 et SAMD21 sont exclus avec une ligne d'information (« BSP … non greffé : preset(s) …
sans tâche ni lancement »), comme dans `check`. Ils restent visibles dans le sélecteur de CMake
Tools (le fichier du noyau ne peut pas être filtré) et constructibles par le repli
`cmake/boards` jusqu'à ENV-19.

### Q5. `seed status` et extension
- `seed status` : la ligne « graine hors lepton » devient « graine de référence (ni
  lepton-graine.json ni project/) : rôles d'après les manifestes des greffons, presets du noyau » ;
  sortie `--json` inchangée (pas de champ nouveau : les sorties des graines de projet restent
  identiques à l'octet), `configurations` vide.
- `seed tree` : presets lus = presets offerts (Q4) ; preset de `build/.active`, sinon premier
  preset offert configuré.
- Extension : aucune modification ; à constater en tâche 3 : vue IDE-1 (repli par greffon puis
  codemodel après configuration), palette (commandes refusées : message de lepton), diagnostics
  des manifestes de greffon et des XML, F5 sur `qemu-mps2-an386-freertos`.

### Décision PA-23 (utilisateur, 2026-10-31)
Q1, Q2, Q3 et Q5 validées telles que proposées. Q4 amendée : les 4 presets F746 et SAMD21 (BSP
non greffé) reçoivent les tâches configurer et construire, sans `launch` ; les 10 presets à BSP
greffé ont tâches et `launch` ; `host` garde ses tâches mklepton. Consignée dans
`DEVENV-STATUS.md` §Décisions.

## 4. Implémentation (tâche 2)
| Commit (lepton-tools) | Contenu |
| --- | --- |
| 1f44baf | `Rootstock.is_reference_seed` (critère repris par `check`) ; `checks.board_presets` ; `seed status` (ligne « graine de référence ») ; `seed tree` (`tree._presets` : presets de carte du noyau) |
| eedb572 | `generate` : `Configuration` (un BSP par configuration), `Context._reference_seed` ; aucun `CMakeUserPresets.json` ni `graft_project` ; espace `<répertoire de la graine>.code-workspace` ; BSP non greffé : tâches configurer et construire seules, ligne d'information |
| b308d7f | `seed.refuse_reference`, appelé par `seed add/remove/replace/lock/mkconf import`, `seed config add/remove`, `scion new` (sans `--no-seed`), `scion remove` |
| 26e46f3 | `tests/test_reference_seed.py` : 14 tests (status, tree, owner ; generate ; 11 refus ; `scion new --no-seed`) |
| c2685c6 | `rapports/env-8-interface.md` §16 |

Extension : non modifiée (PA-23 Q5). lepton réinstallé par `pipx install --force <LEPTON_TOOLS>`
depuis `devenv/env-18` c2685c6 (Mac ; Debian en ENV-21).

## 5. Contrôles (tâche 3)
- `pytest` : 216 tests verts (202 + 14).
- Graines de projet : `releve.sh apres` puis `diff -r avant apres` vide sur `env-9`,
  `env-11/{qemu,qemu-gra2,f429zi,wl55jc1}`, `env-11/bout-en-bout` (status, tree, check, owner,
  presets et espace rendus). Le script de relevé a reçu une branche pour la graine de référence
  (rendu de l'espace seul), sans effet sur les graines de projet.
- Graine de référence, `essais/env-13-vierge` puis `<ROOTSTOCK>` : `seed status` code 0, ligne
  « graine de référence » ; `generate` code 0, `original-tree.code-workspace` écrit, `build/.active`
  amorcé, requêtes de l'API fichier écrites pour les 14 presets de carte ; graine : 0 changement,
  HEAD 0f1275a, pas de `project/` ; trunk : liste greffée inchangée, aucun lien cassé, aucun fichier
  créé (les 5 `.DS_Store` du trunk d'`env-13-vierge`, créés le 2026-10-31 à 12:48, préexistaient).
- Refus : les 11 commandes du PA-23 Q1 rendent 1 avec le message validé ; graine et liste greffée
  inchangées, aucun dépôt créé.
- `env-13-vierge`, en ligne de commande : `cmake --preset qemu-mps2-an386-freertos` puis
  `--build` code 0 ; `seed tree` lit la réponse codemodel du preset actif (exécutif → bibliothèques
  → greffons).
- VSCodium, `<ROOTSTOCK>/original-tree.code-workspace` (essai de l'utilisateur) : conforme —
  preset `qemu-mps2-an386-freertos` configuré et construit, clangd sur `build/.active`, vue IDE-1,
  F5 (arrêt sur `main`, source par le trunk), refus affiché par la palette. Après l'essai : trunk
  sans fichier régulier ni lien cassé, graine et 8 clones sans modification, `check` code 0.

## 6. Observations hors étape
- `seed status` rend 2 (« git rev-parse --abbrev-ref HEAD » en échec) sur un dépôt de graine sans
  aucun commit ; constaté par les tests (fixture corrigée en commitant la graine), sans effet sur
  les graines réelles.
- Le sélecteur de CMake Tools présente les 15 presets du noyau, F746 et SAMD21 compris
  (constructibles par le repli `cmake/boards` jusqu'à ENV-19).
