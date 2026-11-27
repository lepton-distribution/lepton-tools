# EP-1 — Greffon de type `projet` : audit et conception (PA-E2)

Session du 2026-11-27, branche `espace-projet/ep-1` de lepton-tools (depuis `main` c76612d).
Lecture seule : aucun fichier hors de `doc/espace-projet/` n'est modifié avant la réponse au PA-E2.
Base : lepton 0.1.0, extension 0.5.4, scion 0.6.3.4, clone noyau `master` 0c2e43e.

## 1. Relevé

### 1.1 `lepton/` : ce qui crée, lit ou teste `project/`

| Endroit | Rôle aujourd'hui |
| --- | --- |
| `rootstock.py:33-34` `PROJECT_SUBPATH = "project"` ; `:60` `project_key()` → `lepton@project-<projet>` | sous-répertoire du dépôt de la graine et clé du greffon local |
| `rootstock.py:282` `is_reference_seed()` | « ni `lepton-graine.json` ni `project/` » (PA-19 C) |
| `rootstock.py:199` `find_manifest()` | manifeste cherché seulement sous `<clone>/scion/sys/root/src/` |
| `rootstock.py:30` `KEY_PREFIX` | préfixe de clé par type ; pas d'entrée pour un type `projet` |
| `seed.py:208` `project_stem()` = `<graine>/project/scion/` | racine greffée du greffon local |
| `seed.py:222` `graft_project()` | déclare (`seed-scion-add … * <graine> project`), inscrit (`seed-clone`), greffe |
| `seed.py:243` `in_project()` | « fichier du greffon projet » = sous `project_stem` |
| `seed.py:263` `import_mkconf()` | copie le XML et ses `src_file` sous `project_stem`, puis `graft_project` |
| `seed.py:304` `declare_application()` | écrit `<bin>` dans le XML s'il est sous `project_stem` |
| `seed.py:327` `seed_mkconf_import()` | cible : `project_stem` ; écrit `mklepton_xml` dans la graine |
| `seed.py:368` `seed_new()` | `import_mkconf(…, seed_repo, …)` : le XML va dans la graine ; un seul commit (graine + `project/`) |
| `seed.py:491`, `:519` `status_data()` | rôle « projet » par **égalité de clé** avec `project_key(projet.nom)` |
| `seed.py:559`, `:613` messages de `seed status` et de `refuse_reference` | citent « ni lepton-graine.json ni project/ » |
| `seed.py:818`, `:870` `seed lock` | la clé du projet est exclue du verrou (« dépôt de la graine elle-même ») |
| `checks.py:510-513` | information « graine de référence » |
| `checks.py:535` | avertissement O5 si le XML n'est pas sous `<graine>/project/scion/` |
| `generate.py:629-633` | `CMakeUserPresets.json` écrit sous `project_stem`, puis `graft_project` ; rien en graine de référence |
| `generate.py:354` `workspace_folders()` | clé du projet omise des dossiers « git · … » (même dépôt que la graine) |
| `generate.py:391-392` `files.exclude` | `project/scion` masqué |
| `mkconf.py:26-33` `project_etc()`, `project_xml()` | `sys/user/<projet>/etc/mkconf_<projet>.xml` (relatif au trunk : inchangé par l'étape) |
| `tree.py:40` | presets de la graine de référence (critère `is_reference_seed`) |
| `scions.py:121` | `scion new` sans `--no-seed` refusé en graine de référence |

`seed tree` ne lit `project/` que par `status_data` et le critère de référence. `configs.py`,
`files.py`, `cli.py` : aucune occurrence.

### 1.2 Les deux lecteurs de manifeste

- lepton, `find_manifest` : un manifeste par clone, le moins profond sous `scion/sys/root/src/`.
- CMake du noyau, `scion/cmake/lepton_greffons.cmake` : `file(GLOB_RECURSE … ${LEPTON_SRC}/lepton-greffon.json)`
  avec `LEPTON_SRC = scion/sys/root/src` (`CMakeLists.txt:27`) ; type hors de
  `noyau famille bsp application bibliotheque` → `FATAL_ERROR` (l. 138) ; `destination` doit égaler
  l'emplacement relatif à `sys/root/src` (l. 146).
- Conséquence vérifiée : un manifeste sous `sys/user/<projet>/` est **invisible du lecteur CMake**
  (hors du `GLOB`) ; un manifeste sous `sys/root/src/` casse toute configuration. Le premier
  emplacement n'exige aucune modification du noyau ; il exige d'étendre `find_manifest`.

### 1.3 Schémas et exemples

- `schemas/greffon.schema.json` : `type` enum de 5 valeurs ; un `allOf` de `if type = … then …`
  par type ; `destination` décrite relative à `sys/root/src/` ; `additionalProperties: false`.
- `schemas/graine.schema.json` : requis `projet`, `noyau`, `bsp`, `backend`, `configurations`,
  `mklepton_xml` ; `projet` = identité (`nom`, `version`, `description`) ; aucun champ ne désigne
  le porteur des fichiers du projet.
- `schemas/exemples/` : aucun exemple ne cite `project/`. `scripts/valider-schemas.sh` associe
  l'exemple au schéma par le préfixe du nom (`graine*` → graine, autre `*.json` → greffon) ;
  un invalide doit être du JSON bien formé, refusé par son schéma. Mêmes répertoires lus par
  `tests/test_milestone1.py` et `tests/test_diagnostics.py`.

### 1.4 Extension, tests, scripts, README

- **Extension** : aucune dépendance à `project/`, `lepton@project-`, `CMakeUserPresets.json`, ni
  au critère de référence. `role` de `seed status --json` est une chaîne affichée telle quelle
  (`tree.ts:238`, `:246`, `commands.ts:79`) ; l'observation des racines suit le champ `stem`
  (`watch.ts:32`, `:163`). Elle reste correcte si `stem` désigne la racine du greffon projet.
- **Tests** : la fixture `conftest.py:96` `project` (`seed new demo`) est la seule qui construit
  une graine de projet ; la graine de référence vient de `test_milestone6.py:355` `_reference`.
  Tests qui vérifient `project/` ou la clé : §3.10.
- **`scripts/bout-en-bout.sh` l. 63-67** : la cible du lien du XML doit être sous
  `depots/lepton-seed/bout-en-bout/project/scion/`. **`README.md` l. 40, 45-49** : emplacement
  du XML et de `CMakeUserPresets.json` « dans la graine, sous `project/scion/` ».

### 1.5 Compte de départ de `pytest`

**616 verts** en 9 min 13 s (venv `~/lepton-tools-dev/venv-lepton-tools`, pytest 9.1.1, branche = `main` c76612d).

### 1.6 Graines à `project/` existantes

| Où | Graines | Distant |
| --- | --- | --- |
| Mac, `essais/env-9` | `env9` | aucun |
| Mac, `essais/env-11/{qemu,qemu-gra2,f429zi,wl55jc1,bout-en-bout/rootstock}` | `env11` ×2, `env11f4`, `env11wl`, `bout-en-bout` | aucun |
| Mac, `essais/env-72-essai/{c4,c4d}/{rs,M}` | `env11` ×4 | aucun |
| VM, `essais/env-53-c5` (`rapports/env-72-debian.md` l. 85-87, 359 : conservée) | `env11` (greffon `salut`) | aucun |
| Publiées sur un distant (`DEVENV-STATUS.md`, grep) | aucune | — |

`<ROOTSTOCK>` : graine `original-tree` sans `project/` ni `lepton-graine.json` (graine de
référence, inchangée par le critère réduit). Toutes les graines à `project/` sont des essais
locaux, régénérables par `seed new`.

## 2. Exigences touchées (T9)

- PA-19 C d'ENV-16 (critère de référence) et PA-23 d'ENV-18 (messages des refus) : énoncés dans
  `doc/devenv/DEVENV-STATUS.md` §Décisions et `doc/devenv/rapports/env-8-interface.md` §3.9,
  §11 (XML du projet), §16.
- `doc/devenv/SPECIFICATION.md` : aucune exigence ne cite `project/` (GRA-1 dit « dépôt git de
  destination ou répertoire local »).

## 3. Propositions (non validées)

### 3.1 Manifeste du greffon `projet`
- **(recommandé)** `lepton-greffon.json` de type `projet` à `scion/sys/user/<nom>/lepton-greffon.json`
  du greffon ; champs : `nom` (= nom du projet), `type`, `version`, `description` ; `destination`,
  `sources`, `bibliotheque`, `dependances`, `compilation`, `options` et champs matériels refusés par
  le schéma (le répertoire est imposé par `nom`). `find_manifest` : sous `sys/root/src/` d'abord,
  sinon l'unique `scion/sys/user/*/lepton-greffon.json` de type `projet` ; deux manifestes de type
  `projet` dans un clone : erreur. **Noyau non modifié** (le `GLOB` ne voit pas `sys/user/`).
- Écartée : manifeste sous `sys/root/src/` (modification et publication du noyau, configuration
  cassée tant que le lecteur n'est pas publié).
- Écartée : pas de manifeste (greffon reconnu par sa clé) : le régime de référence d'EP-3 (greffon
  projet sans `lepton-graine.json`) n'aurait aucun moyen de le reconnaître.

### 3.2 Désignation dans `lepton-graine.json`
- **(recommandé)** aucune nouvelle clé : le greffon projet est le greffon greffé de type `projet`
  dont `nom` = `projet.nom` (comme `noyau` et `bsp` désignent un greffon par son nom, mais sans
  dédoubler le nom du projet) ; requis pour une graine de projet ; `check` signale son absence, un
  nom différent, ou deux greffons `projet`. Schéma de graine : description de `projet.nom` et de
  `mklepton_xml` seulement.
- Variante : clé requise `greffon_projet` (nom du greffon), si l'utilisateur veut un nom de greffon
  distinct du nom du projet ; elle introduit `sys/user/<greffon>/` ≠ `sys/user/<projet>/`.

### 3.3 Interface de `seed new`
- **(recommandé)** greffon projet **créé** par défaut : dépôt git local `--project-repo DIR`
  (défaut `<rootstock>/depots/lepton-project/<nom>`, indépendant de `--seed-repo`), modèle
  `templates/project/` (manifeste + `.gitignore` vide), XML de `--mkconf` copié dedans, commit
  initial « Greffon projet <nom> créé par lepton seed new » ; déclaré dans la graine par chemin
  local, version `*` (utilisé en place, comme aujourd'hui), clé `lepton@project-<nom>`
  (`KEY_PREFIX["projet"] = "project"` : même clé qu'aujourd'hui).
- Greffon projet **désigné** : `--origin <nom>=LOCATION[@VERSION][:PATH]` (syntaxe existante ; `:PATH`
  pour un dépôt partagé avec BSP et applications, chaque greffon à son propre sous-chemin) ; le
  manifeste doit être de type `projet`, de nom `<nom>`. `--mkconf` : si le XML
  `sys/user/<nom>/etc/mkconf_<nom>.xml` existe dans le greffon, `--mkconf` est refusé (XML déjà
  fourni) ; sinon `--mkconf` est requis et copié dans le clone (non commité, rappel affiché).
- Publication ultérieure d'un greffon créé : `lepton seed replace <nom> URL@VERSION` (existant),
  hors étape.

### 3.4 Autres commandes
- `generate` : `CMakeUserPresets.json` à `<greffon projet>/scion/` ; rappel de commit dans le dépôt
  du greffon projet (et dans la graine si `graft_project` l'a changée). Dossiers : le greffon projet
  apparaît comme « git · <nom> » (dépôt distinct : IDE-2) ; `files.exclude` `project/scion` laissé
  tel quel (espace de la graine de référence inchangé ; retrait à EP-4).
- `seed mkconf import` : cible la racine du greffon projet ; écrit `mklepton_xml` dans la graine.
- `check` : greffon projet requis en graine de projet (§3.2) ; avertissement O5 si le XML n'est pas
  sous la racine du greffon projet ; manifeste `projet` validé par le schéma.
- `seed status` : rôle « projet » d'après le **type** du manifeste ; colonne d'origine du dépôt du
  greffon ; `stem` = sa racine `scion/`.
- `seed tree` : inchangé (suit `status_data`).
- `seed lock` : le greffon projet est figé comme les autres (dépôt distinct ; local hors git :
  rien à figer, règle existante).
- `seed remove <nom>` du greffon projet : refusé (« greffon du projet »), comme le noyau et le BSP.

### 3.5 Critère de la graine de référence
- **(recommandé)** `is_reference_seed()` = « pas de `lepton-graine.json` » (C4) ; messages de
  `seed status`, `check` et des refus : « (pas de lepton-graine.json) ». `<ROOTSTOCK>` ne change
  pas de régime.
- Graine contenant encore `project/` (ancien format) : §3.7.

### 3.6 T8 — greffon `projet` greffé sans `lepton-graine.json` (cas d'EP-3)
- **(recommandé)** `generate` n'écrit **aucun** `CMakeUserPresets.json` : les presets du noyau
  servent tels quels (PA-23 Q3 inchangé, rien n'est écrit dans un greffon) ; toutes les commandes
  du refus PA-23 restent refusées (`seed mkconf import` écrit dans la graine) ; `check` valide le
  manifeste `projet` et, par les presets du noyau, les XML qu'il fournit ; `seed status` lui donne
  le rôle « projet ».
- Variante : `generate` écrit des presets utilisateur dans le greffon projet (dédoublerait les 16
  presets du noyau ; à examiner avec T4 au PA-E6 seulement).

### 3.7 Sort des graines à `project/`
- **(recommandé)** refus explicite, sans migration : toute commande sur un rootstock dont la graine
  a un `project/` (avec ou sans `lepton-graine.json`) s'arrête, code 1 : « graine à l'ancien format
  (project/) : … », action : recréer le projet par `lepton seed new` (ou procédure manuelle décrite
  dans le README : créer le dépôt du greffon projet depuis `project/`, `seed replace`). Graines
  d'essai du §1.6 abandonnées (ligne au hors-plan) ; `essais/env-53-c5` de la VM : sort décidé en
  EP-8. Critère « graine migrée, binaires identiques » : sans objet ; l'oracle se fait sur un projet
  neuf (fumée QEMU) et sur la copie de `<ROOTSTOCK>`.
- Variante : commande `lepton seed migrate` (dépôt du greffon créé depuis `project/`, historique
  non repris, déclaration remplacée), avec oracle avant/après sur une copie d'`essais/env-11/qemu`.

### 3.8 T9 — où consigner les exigences modifiées
- **(recommandé)** `doc/espace-projet/EXIGENCES.md`, créé par l'étape : amendements au critère PA-19 C,
  aux messages de PA-23, à `env-8-interface.md` §3.2, §3.9, §3.10, §11 et §16, sous la forme des
  amendements de l'interface (décision, avant, après) ; `doc/devenv/` non modifié. Le même fichier
  reçoit ensuite les exigences d'EP-4 à EP-6 (champ `sonde` de GRF-3).
- Variante : nouvelle section « §22. Amendements d'EP-1 » dans `doc/devenv/rapports/env-8-interface.md`
  (modification de `doc/devenv/`, ajoutée à la liste de l'ORCHESTRATION §3).

### 3.9 Versions
- **(recommandé)** lepton **0.2.0** (format de graine incompatible : `project/` refusé) ;
  `SCION_MIN_VERSION` inchangé ; extension **non touchée** (0.5.4 : §1.4).

### 3.10 Tests inversés ou réécrits (si §3.1 à §3.7 retenus)
Réécrits, même intention, emplacement déplacé vers le greffon projet : `test_generate.py`
(`_snapshot`, `test_generate_presets_grafted_in_trunk`, `test_status_and_lock_with_project_scion`),
`test_project_mkconf.py` (`_stem`, `test_seed_new_copie_xml_et_fichiers`, `test_mkconf_import`,
`test_graine_non_migree_avertit_sans_ecrire`), `test_milestone3.py` (`test_gra1_seed_new`,
`test_gra6_status`, `test_d37_greffon_du_projet_non_retire`), `test_milestone6.py`
(`test_cfg5_check_pilote_binaire_non_fournis`), `test_diagnostics.py` (2 tests, chemin résolu).
Inversé : `test_milestone6.py::test_check_graine_projet_sans_manifeste_refusee` (graine sans
manifeste avec `project/` : refus « ancien format » au lieu de l'anomalie « manifeste absent ») ;
messages de `test_reference_seed.py` (`test_reference_status_et_tree`, `test_reference_refus`).
Inchangés : `test_workspace_folders_settings_launch_tasks` sauf le dossier « git · demo » ajouté.

## 4. Occurrences restantes attendues du grep du critère

`grep -rnE 'PROJECT_SUBPATH|project_key|project_stem|graft_project|project/' lepton --include='*.py'`
après l'étape (§3 recommandé) : `PROJECT_SUBPATH` gardé pour détecter l'ancien format (§3.7) et
pour `files.exclude` (§3.4) ; `project_key` conservé (clé du greffon créé) ; `project_stem` et
`graft_project` renommés ou remplacés (racine du greffon projet). Justification ligne à ligne dans
une section ajoutée en fin d'étape.

## 5. Décision PA-E2 (utilisateur, 2026-11-27)

Toutes les propositions recommandées du §3 sont retenues (§3.1 à §3.9) ; variantes écartées.
Consignée dans `STATUS.md` §Décisions.
