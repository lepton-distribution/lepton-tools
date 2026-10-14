# ENV-8 — Interface de l'outil `lepton` (proposition PA-9)

Rédigé le 2026-10-14. Base : `etapes/ENV-08-outil-lepton.md`, `SPECIFICATION.md` (GRA, GRF, FIC,
CFG-5, INS-6, NF), schémas d'ENV-3 (`schemas/`), scion 0.5.1.0 (`rapports/env-7-evolutions.md`
§2, enchaînements GRA-4), rootstock réel `~/lepton` (lecture seule). Aucun code écrit.

## 1. Principes

| Sujet | Proposition |
| --- | --- |
| Langage, version | Python ≥ 3.11 (3.11.5 sur le Mac, 3.11 sur Debian 12) ; paquet `lepton`, version initiale **0.1.0** |
| Appel de scion | `subprocess.run([...], check=False)` avec liste d'arguments ; aucune importation de modules de scion ; version de scion contrôlée au premier appel (≥ 0.5.1.0, sinon code 2 et commande d'installation suggérée) |
| Lecture des fichiers `.scion.*` | Lecture seule par `lepton` (format texte stable, `env-2-scion.md` §1) ; **toute écriture passe par scion** |
| Rootstock courant | `-C DIR` / `--rootstock DIR`, sinon recherche de `.scion.rootstock.signature` en remontant depuis le répertoire courant (fonctionne depuis le trunk et depuis un clone sous `depots/`) |
| Graine courante | Seed de la liste greffée (5ᵉ colonne de `trunk/.scion.grafted.list`) ; `lepton-graine.json` dans `<seed>/scion/.scion/` (à côté de `.scion.sources.list`) |
| Correspondance greffon ↔ clé scion | Clé `lepton@<préfixe>::<nom>` ; préfixe = type (`famille`, `bsp`, `application`, `bibliotheque`) ; noyau = clé existante `lepton@original::tree`. Le nom et le type réels sont lus dans le manifeste `lepton-greffon.json` du clone (recherche sous `<clone>/<chemin>/scion/sys/root/src/**/`). Shelf `lepton` par défaut (`--shelf` réservé, non exposé en 0.1) |
| Écriture | Jamais dans le trunk ; création dans le clone propriétaire puis `scion graft --scion` (FIC-3) |
| Git | Aucune opération git implicite hors celles listées (§3.5 `file`) ; aucun fetch, aucun push ; `lepton` ne commite pas dans la graine ni dans les clones (sauf commit initial des dépôts qu'il crée : `seed new`, `scion new`) |
| Reconfiguration CMake (GRA-4) | Après toute opération qui change la liste des greffons ou un manifeste : `cmake -S <trunk> -B <rép>` pour chaque `<ROOTSTOCK>/build/*/CMakeCache.txt` dont `CMAKE_HOME_DIRECTORY` est le trunk ; `--no-cmake` pour l'éviter. Ajout ou retrait de fichier source : pas de reconfiguration forcée (GLOB `CONFIGURE_DEPENDS` du lecteur, FIC-4) |
| Contrôle final | Après chaque commande qui modifie : trunk sans fichier régulier (hors `.scion.grafted.list`) ni lien cassé ; sinon code 1 avec la liste (critère ENV-8) |
| Messages (NF-6) | Erreurs sur stderr : `lepton: erreur: <constat>` puis `  → <action corrective>` ; `-v` affiche chaque commande externe exécutée ; données (status, check) sur stdout |
| Sortie machine | `--json` sur `seed status` et `check` (consommés par l'extension, ENV-12) |
| Hors ligne (NF-8) | Aucun accès réseau propre à `lepton` ; seuls les clones demandés par scion (`seed-add`, `seed-clone`) peuvent en faire |

## 2. Codes de retour

Alignés sur scion.

| Code | Sens |
| --- | --- |
| 0 | Succès (`check` : aucune anomalie) |
| 1 | Erreur d'utilisation ou refus : option invalide (argparse ramené de 2 à 1), précondition non remplie, manifeste invalide, anomalie trouvée par `check`, contrôle final du trunk en échec |
| 2 | Échec d'un outil appelé (scion, git, cmake) ou outil absent ; le message reprend la commande et son stderr |
| 130 | Interruption (Ctrl-C) |

Sur échec en cours d'enchaînement, `lepton` annule ce qu'il a fait quand scion le permet (ex. `seed add` : `seed-scion-remove` + `graft-remove`) et indique l'état laissé sinon.

## 3. Commandes

Options globales : `-C/--rootstock DIR`, `-v/--verbose`, `--version`, `-h/--help`.

### 3.1 `lepton --version` (INS-6)
Sortie : `lepton 0.1.0` puis `scion 0.5.1.0 (requis ≥ 0.5.1.0)` ou `scion absent`. Code 0 même
si scion manque (diagnostic d'installation).

### 3.2 `lepton seed new` (GRA-1, GRA-2, GRA-3)
```
lepton seed new NAME --bsp BSP [--backend embos|freertos] [--rootstock DIR]
                [--seed-repo DIR] [--mkconf PATH]
                [--origin SCION=LOCATION[@VERSION][:PATH]]...
```
Enchaînement :
1. `DIR` (défaut : répertoire courant) inexistant ou vide, sinon code 1.
2. `scion rootstock-install` (layout par défaut : conserve `depots/generation/building` attendu
   par la graine Lepton).
3. Dépôt git de la graine créé par `lepton` à `--seed-repo` (défaut
   `<DIR>/depots/lepton-seed/<NAME>`, voir Q3) : `scion/.scion/.scion.sources.list`,
   `.scion.ramifications`, `lepton-graine.json` depuis `templates/seed/`, commit initial.
4. `scion seed-add <dépôt-graine>` puis `scion graft`.
5. Lecture du manifeste du BSP ; contrôle de sa `famille` et de son cœur (§3.10) ;
   `lepton-graine.json` validé par le schéma.
6. Configuration initiale de la graine : `debug-qemu` si le BSP déclare `qemu`, sinon
   `debug-board` ; `mklepton_xml` = `--mkconf` (voir Q5).

Origines : noyau, famille et BSP doivent avoir une origine. Défaut proposé : noyau
`https://github.com/lepton-distribution/lepton-original-tree.scions.git@master` ; famille et BSP :
`--origin` obligatoire (voir Q4). `LOCATION` : URL git, ou chemin local (version `*`).
Sortie : récapitulatif (rootstock, graine, greffons) et la commande cmake suivante à lancer
(presets générés en ENV-9).

### 3.3 `lepton seed status [--json]` (GRA-6)
Une ligne par greffon de la liste greffée, plus la graine elle-même :

| Colonne | Source |
| --- | --- |
| greffon, rôle | manifeste (`nom`, `type`) ; rôle dans la graine (noyau, bsp, famille, application, bibliothèque, hors graine) |
| clé, version demandée, origine | `.scion.sources.list` du seed |
| branche, commit | `git -C <clone> rev-parse --abbrev-ref HEAD`, `--short HEAD` |
| modifications | `git -C <clone> status --porcelain` (nombre, fichiers avec `-v`) |
| avance / retard | `git rev-list --left-right --count @{u}...HEAD` si un amont existe, sans fetch |

Fin de rapport : contrôle du trunk (fichiers réguliers, liens cassés), greffons de la graine non
greffés ou greffés hors graine. Code 0 ; 1 si le rootstock est incohérent.

### 3.4 `lepton seed add / remove / replace` (GRA-3, GRA-4)
```
lepton seed add SCION LOCATION --type famille|bsp|application|bibliotheque
                [--version V] [--path P] [--no-cmake]
lepton seed remove SCION [--purge] [--no-cmake]
lepton seed replace SCION LOCATION [--version V] [--path P] [--no-cmake]
```
| Commande | Appels scion (ENV-7) | Mise à jour de `lepton-graine.json` |
| --- | --- | --- |
| `add` | `seed-scion-add` → `seed-clone` → `graft --scion` ; contrôle : manifeste présent, `nom` = SCION, `type` = `--type`, sinon annulation | application / bibliothèque ajoutée à sa liste ; `bsp` : remplace le BSP de la graine (l'ancien reste greffé, signalé) |
| `remove` | `seed-scion-remove` → `graft-remove [--purge]` | retrait de sa liste ; refus pour le noyau et le BSP courant (GRA-2), et pour une famille utilisée par le BSP courant |
| `replace` | `seed-scion-add --replace` → `graft-remove` → `seed-clone` → `graft --scion` | inchangée (même greffon, autre origine ou version) |

Puis reconfiguration CMake. `--type` est requis pour `add` car la clé scion en dépend avant le
clonage. La graine est laissée modifiée et non commitée ; le message rappelle de la commiter.

### 3.5 `lepton seed lock [--verify]` (GRA-5, P2, jalon 6)
Écrit `lepton-graine.lock.json` à côté de `lepton-graine.json` : pour chaque greffon, clé,
origine, version demandée, commit exact (`git rev-parse HEAD`) et état propre exigé (refus si
modifications non commitées). `--verify` compare l'état des clones au fichier (code 1 si écart).
La reconstruction depuis le verrou (forme exacte de la commande) est arrêtée au jalon 6, selon ce
que scion accepte comme version (commit ou tag).

### 3.6 `lepton scion new / remove` (GRF-1, GRF-4) — nom de la sous-commande : Q1
```
lepton scion new NAME --type bsp|application|bibliotheque [--repo DIR]
                 [--destination D] [--from BSP] [--no-seed] [--no-cmake]
lepton scion remove NAME [--no-cmake]
```
`new` : dépôt git local créé à `--repo` (défaut `<ROOTSTOCK>/depots/lepton-<kind>/<NAME>`, `<kind>` =
`bsp`, `application`, `library` ; voir Q10) depuis `templates/<kind>/` : `scion/sys/root/src/<destination>/lepton-greffon.json`,
`CMakeLists.txt` facultatif, fichier exemple ; commit initial ; puis, sauf `--no-seed`,
`lepton seed add NAME <dépôt> --type <type>` (version `*`). Destination par défaut :
`kernel/dev/bsp/<NAME>` (bsp, PA-7 Q12), `bin/<NAME>` (application) et `lib/<NAME>` (bibliothèque), comme la spécification §types et `schemas/exemples/`. BSP :
`--from BSP` obligatoire, copie le manifeste et les fichiers du BSP existant en renommant
(GRF-1 « construit sans édition manuelle ») (Q6).
`remove` : comme `seed remove` sans `--purge` (le dépôt n'est jamais touché, GRF-4).

### 3.7 `lepton file` et `lepton dir` (FIC-1, FIC-2, FIC-3, FIC-6)
```
lepton file add PATH [--scion SCION]
lepton file remove PATH
lepton file mv SOURCE DESTINATION
lepton dir add PATH [--scion SCION]
lepton dir remove PATH [--scion SCION]
```
`PATH` : chemin dans le trunk (absolu, ou relatif au répertoire courant) ; un chemin dans un
clone est accepté et désigne directement son greffon.

Greffon propriétaire d'un chemin nouveau : `--scion`, sinon le greffon unique qui possède les
feuilles du plus proche répertoire existant du trunk (cible des liens) ; plusieurs greffons →
refus avec la liste et `--scion` suggéré ; aucun → refus « chemin du trunk sans greffon
propriétaire » (ENV-8 tâche 5). Greffon désigné hors de la graine → refus.

| Commande | Action dans le clone | Puis |
| --- | --- | --- |
| `file add` | crée le fichier vide (refus s'il existe dans le trunk ou le clone) ; pas de `git add` (Q7) | `scion graft --scion` |
| `file remove` | le chemin du trunk doit être un lien vers un clone ; `git rm` si suivi, sinon suppression | `scion graft --scion` |
| `file mv` | source et destination dans le même greffon (sinon refus) ; `git mv` si suivi (FIC-6), sinon renommage | `scion graft --scion` |
| `dir add` | crée le répertoire avec un `.gitkeep` (Q7) | `scion graft --scion` |
| `dir remove` | supprime la part du greffon dans ce répertoire (`git rm -r` / suppression) ; plusieurs propriétaires → `--scion` requis | `scion graft --scion` |

`CMakeLists.txt` ou `lepton-greffon.json` ajouté, retiré ou déplacé : reconfiguration CMake.

### 3.8 `lepton graft [--scion SCION]... [--force] [--no-cmake]`
Suppression des fichiers système réguliers du trunk (`.DS_Store`, `._*`, Q8) ; `scion graft`
(complet) ou `scion graft --scion <clé>` ; contrôle final du trunk ; reconfiguration CMake.
`--force` transmis à scion : conserve les autres fichiers réguliers du trunk (règle scion).

### 3.9 `lepton check [--json] [FILE...]` (GRF-2, GRF-5 P2, CFG-5 P2)
Sans argument : graine et tous les manifestes des greffons greffés. Avec `FILE` : manifeste
isolé (`lepton-greffon.json`, `lepton-graine.json`, XML mklepton), type reconnu par le nom ou
`$schema`.

| Contrôle | Jalon |
| --- | --- |
| Schéma JSON (greffon, graine) ; XSD mklepton par `xmllint` s'il est présent (sinon signalé) | 1 |
| Non exprimable en JSON Schema (`handoff/env-3.md`) : défaut d'option dans les bornes et dans les valeurs, unicité des noms, fichiers déclarés présents | 6 |
| GRA-2 : noyau et BSP présents et greffés ; famille du BSP greffée ; configuration `qemu` ⇒ BSP avec `qemu`, `carte` ⇒ BSP avec `openocd` et `sonde` | 6 |
| GRF-5 (P2) : cœur du BSP ∈ `coeurs` du noyau et de la famille ; backend ∈ `backends` du noyau ; dépendances déclarées greffées | 6 |
| CFG-5 (P2) : pilote ou binaire du XML fourni par aucun greffon | 6 |

Sortie : une ligne par anomalie `fichier: chemin JSON: message` ; code 1 s'il y en a.

## 4. Correspondance exigences → commandes → tests

| Exigence | Commande | Test (pytest, rootstock temporaire, dépôts git locaux) |
| --- | --- | --- |
| INS-6 | `--version` | `test_ins6_version` |
| GRA-1 | `seed new` | `test_gra1_seed_new` (trunk greffé, graine valide) |
| GRA-2 | `seed new`, `seed remove`, `check` | `test_gra2_noyau_bsp_obligatoires` |
| GRA-3 | `seed new --origin`, `seed add` | `test_gra3_git_and_local_origin` |
| GRA-4 | `seed add/remove/replace` | `test_gra4_add`, `_remove`, `_replace` (trunk et cache cohérents) |
| GRA-6 | `seed status` | `test_gra6_status` (branche, modifications) |
| GRF-1 | `scion new` | `test_grf1_scion_new_<type>` |
| GRF-2 | `check` | `test_grf2_validation_manifestes` (exemples valides et invalides de `schemas/exemples/`) |
| GRF-4 | `scion remove` | `test_grf4_remove` (aucun lien orphelin, clone intact) |
| FIC-1, FIC-2 | `file`, `dir` | `test_fic1_file_add_remove`, `test_fic2_dir_add_remove` |
| FIC-3 | `file add` | `test_fic3_refus_sans_proprietaire`, contrôle « aucun fichier régulier » après chaque test |
| FIC-6 (P2) | `file mv` | `test_fic6_git_log_follow` |
| GRA-5, GRF-5, CFG-5 (P2) | `seed lock`, `check` | jalon 6 |

Bout en bout (script, hors pytest) : `seed new` (noyau + BSP `qemu-mps2-an386`, dépôts locaux du
rootstock réel en origine) → `cmake` (presets host puis an386) → test de fumée QEMU.

## 5. Organisation du dépôt

```
pyproject.toml          # projet lepton, script « lepton = lepton.cli:main »
lepton/                 # paquet : cli.py, rootstock.py, scion_runner.py (appels de scion),
                        # seed.py, scions.py, files.py, validation.py, cmake.py
lepton/schemas/         # copie installée de schemas/*.json (Q2)
lepton/templates/       # seed/, bsp/, application/, library/
tests/                  # pytest ; fixtures : rootstock temporaire, dépôts git locaux
```

## 5bis. Règle de nommage (demande de l'utilisateur, 2026-10-14)

Options de la ligne de commande, métavariables, modules et répertoires créés par `lepton` : anglais
US. Messages et documentation : français. Restent hors de cette règle, faute de dépendre de
`lepton` seul (voir Q10) :

| Nom | Fixé par | Exemple |
| --- | --- | --- |
| `depots/`, `depots/origin`, `depots/generation/building` | scion (`rootstock-install`, `graft.py`) | inchangé |
| Valeurs de `--type`, `--backend`, `execution` | enums des schémas (PA-3) : `famille`, `bibliotheque`, `qemu`, `carte` | `--type bibliotheque` |
| Noms de fichiers des manifestes | décision ENV-5 : `lepton-greffon.json`, `lepton-graine.json` ; lus par le lecteur CMake du clone noyau | inchangé |
| Préfixes des clés scion existantes | graine de travail (ENV-6) : `famille::…`, `bsp::…`, `original::tree` | inchangé |
| Dépôts des greffons d'ENV-6 | `<ROOTSTOCK>/depots/lepton-famille/*`, `depots/lepton-bsp/*` | inchangé |

## 6. Questions ouvertes (PA-9)

| # | Question | Proposition |
| --- | --- | --- |
| Q1 | Nom de la sous-commande greffon : `scion`, `graft`, `greffon` | `scion` (vocabulaire de la graine et de la table d'ENV-8 ; `graft` est déjà la regreffe) |
| Q2 | Environnement de test et dépendances : `pytest` et `jsonschema` absents de Python 3.11.5 | `jsonschema` dépendance d'exécution épinglée dans `pyproject.toml` (installée par pipx) ; `pytest` en extra `[test]` dans un venv de développement hors dépôt `~/lepton-tools-dev/venv-lepton-tools` (`pip install -e .[test]`, accès PyPI) ; schémas copiés dans le paquet à la construction |
| Q3 | Emplacement du dépôt de la graine créé par `seed new` | `<ROOTSTOCK>/depots/lepton-seed/<NAME>` par défaut, `--seed-repo DIR` sinon ; publication (distant) laissée à l'utilisateur |
| Q4 | Origines par défaut des greffons pour `seed new` | noyau : URL GitHub `@master` ; famille et BSP : `--origin SCION=LOCATION[@VERSION][:PATH]` obligatoire (aucun dépôt publié) ; catalogue d'origines reporté |
| Q5 | XML mklepton de `seed new` : la graine (dépôt seed) n'est pas greffée, le XML doit venir d'un greffon (aujourd'hui le noyau, PA-7 Q4) | `--mkconf PATH` obligatoire en 0.1, chemin relatif au trunk validé (fichier présent après greffe) |
| Q6 | `scion new` : destinations par défaut ; BSP neuf « construit sans édition » | application `bin/<NAME>` (bibliothèque `bin`), bibliothèque `lib/<NAME>` (bibliothèque `lib`), conformes à la spécification et aux exemples ; BSP par `--from BSP` (copie renommée d'un BSP existant) ; type `famille` hors GRF-1, non proposé |
| Q7 | Git dans `file add` / `dir add` | pas de `git add` ; `.gitkeep` pour un répertoire vide ; `git rm` / `git mv` pour un fichier suivi |
| Q8 | Fichiers `.DS_Store` du Finder (bloquent la regreffe complète quand ils sont réguliers dans le trunk) | Liste fixe de fichiers système ignorés par `lepton` : `.DS_Store`, `._*`. (1) Jamais signalés par les contrôles (trunk, `seed status`, `check`) ; (2) avant `scion graft`, `lepton graft` supprime ceux qui sont des fichiers réguliers du trunk (jamais un lien ; aucun clone touché ; contenu recréé par le Finder) ; (3) tout autre fichier régulier reste refusé, liste à l'appui ; (4) les liens `.DS_Store` venus des clones (26 sur `~/lepton`) restent en 0.1. Reliquat, hors ENV-8 : évolution générique de scion (0.5.2) — ne pas greffer les fichiers ignorés par git dans le clone (`git check-ignore`), soumise à un point d'arrêt du type PA-8 |
| Q9 | Découpage d'ENV-8 en sessions | S1 : PA-9 + jalon 1 ; S2 : jalons 2-3 ; S3 : jalons 4-5 ; S4 : jalon 6, bout en bout, `pipx install` |
| Q10 | Noms français hors de `lepton` (§5bis) : valeurs des enums des schémas, noms des manifestes, préfixes de clés, dépôts d'ENV-6 | les garder en 0.1 (changer un enum ou un nom de manifeste amende PA-3 et touche le lecteur CMake du clone noyau et les 7 greffons) ; pour les créations de `lepton` : préfixes de clé `bsp::`, `application::`, `library::`, dépôts `depots/lepton-<kind>/` (`bsp`, `application`, `library`), fichier de verrou `lepton-graine.lock.json` (aligné sur `lepton-graine.json`) ; passage complet à l'anglais = révision séparée à planifier |
| Q11 | Clés `--json` (`seed status`, `check`) | anglais US (`name`, `role`, `key`, `branch`, `commit`, `dirty`, `ahead`, `behind`) |

## 7. Décisions PA-9 (utilisateur, 2026-10-14)

- Règle de nommage du §5bis : options, métavariables, modules et répertoires créés par `lepton` en
  anglais US ; messages et documentation en français.
- Q1 à Q11 : propositions du §6 retenues telles quelles (Q8 dans sa version révisée : fichiers
  système ignorés par `lepton`).

## 8. Amendements de la session S2 (2026-10-14)

Décisions de l'utilisateur :

| # | Décision | Amende |
| --- | --- | --- |
| S2-1 | `--origin` : le noyau est désigné par le nom de son manifeste, `lepton-noyau` (règle unique « SCION = nom du manifeste ») ; clé `lepton@original::tree` inchangée | §3.2 |
| S2-2 | `templates/bsp/` = manifeste squelette à jetons ; champs matériels repris du BSP `--from` (jalon 4) | §5, Q6 |
| S2-3 | Clés scion des greffons créés par lepton : `<kind>-<nom>` sans suffixe (`lepton@bsp-<nom>`, `application-`, `library-`), car scion clone une origine distante dans `depots/<shelf>/<préfixe>/<version>` : avec `bsp::<nom>`, deux BSP distants de même version partageraient un clone | Q10 |
| S2-4 | URL sans `@VERSION` (et `seed add` sans `--version`) : version `master` ; chemin local : version `*`, `@VERSION` refusé | §3.2, §3.4 |

Propositions appliquées, à confirmer :

- Préfixe de clé de la famille : `family-` (règle anglaise des noms créés par lepton, comme
  `library-` pour `bibliotheque`).
- Configuration initiale de `seed new` : `debug-qemu` / `debug-board` (noms du §3.2).
- `seed new` écrit `lepton-graine.json` et commite la graine **après** la greffe et les contrôles
  (configuration déduite du BSP) ; en cas d'échec, rien n'est supprimé : rootstock greffé et
  graine non commitée, signalés dans le message.
- `seed replace` : `graft-remove` (avec `--purge` si l'ancienne origine est distante) avant
  `seed-scion-add --replace` et `seed-clone` ; sinon une origine distante de même clé et de même
  version réutiliserait l'ancien clone. Échec : origine précédente restaurée.
- `seed add` en échec : retrait du trunk et de la graine ; le clone éventuel est conservé.
- `-v` et `-C` acceptés avant ou après la sous-commande ; `seed new -C DIR` désigne le répertoire
  à créer (défaut : répertoire courant).
- Modèles application et bibliothèque sans `CMakeLists.txt` : le lecteur CMake du noyau n'inclut
  ce fichier que pour un BSP (`cmake/lepton_greffons.cmake`) ; sources découvertes par `sources: [""]`.
- Chemin local d'origine rendu relatif au rootstock s'il s'y trouve, absolu sinon.
