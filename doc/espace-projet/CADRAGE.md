# Cadrage du chantier « espace-projet »

Document autonome, écrit le 2026-11-25 à l'issue de deux sessions de réflexion (claude.ai, Claude
Fable 5.1, dossiers `~/lepton-tools-dev/lepton-tools` et `~/lepton` connectés), destiné à la session
Claude Code CLI qui établira le plan du chantier avec la skill `lepton-portage-instructions`.
Rien n'a été modifié ni commité dans les dépôts : ce fichier est le seul produit.

Chantier distinct du chantier « environnement de développement Lepton » (`doc/devenv/`, étapes ENV-0
à ENV-72, terminé et en pause depuis le 2026-11-24). Le terme « chantier » est générique ; il ne
désigne aucun plugin.

## 1. Objet

Rapprocher l'environnement Lepton sous VSCodium du mode de fonctionnement d'un atelier comme IAR
Embedded Workbench, sur quatre axes (décision de l'utilisateur, 2026-11-25) :

1. **Portabilité** d'un poste de développement à l'autre, pour un travail en équipe.
2. **Plusieurs rootstocks** sur une même machine, chacun dans sa propre fenêtre VSCodium.
3. **Choix de l'outil de débogage** dans VSCodium : serveur (OpenOCD, J-Link…) et modèle de sonde
   (ST-LINK, Segger, CMSIS-DAP…).
4. **Plusieurs sondes branchées** (une par carte) : choix de l'interface au lancement.

Et, comme structure porteuse de ces axes, une **architecture de projet** fondée sur une graine et des
greffons (§4), dont le projet de démonstration du noyau (`tauon-basic` → `lepton-basic`) devient le
premier exemple.

## 2. État de départ (relevé le 2026-11-25)

Têtes : lepton-tools `main` e25a414 = `origin/main` ; seed.scions `master` 929c01a, tag 0.6.3.4 ;
noyau `master` 0c2e43e. Mac : scion 0.6.3.4, lepton 0.1.0, extension 0.5.4, git 2.50.1, Claude Code
2.1.331 ; VM Debian : git 2.47.3. Emplacements, versions épinglées et décisions antérieures :
`doc/devenv/DEVENV-STATUS.md` (§Emplacements, §Versions, §Décisions).

### 2.1 Génération de l'espace de travail (`lepton generate`, `lepton/generate.py`)

Lit les manifestes (graine, greffons greffés), jamais le XML mklepton (CFG-1). Écrit :

| Fichier | Emplacement | Versionné |
| --- | --- | --- |
| `CMakeUserPresets.json` | dépôt de la graine, `project/scion/`, greffé à la racine du trunk par le greffon local `lepton@project-<projet>` (version `*`) ; hérite du preset caché `cross` du noyau | oui |
| `<projet>.code-workspace` | `<rootstock>/<projet>.code-workspace` (codé en dur : `rs.path / f"{ctx.project}.code-workspace"`) | non (D2 d'ENV-9, 2026-10-14 : aucun `.vscode/` dans le trunk ni dans un clone) |

Contenu de l'espace (`render_workspace`) : `folders` (`trunk` d'abord — seul chemin d'ouverture, PA-1 —
puis `git · <nom>` par dépôt git distinct, clés projetées omises) ; `settings` (`files.exclude` des
fichiers greffés, CMake Tools avec `cmake.copyCompileCommands` → `build/.active/`, clangd
`--compile-commands-dir=build/.active` et `--query-driver`, Cortex-Debug `gdbPath`,
`armToolchainPath`, `openocdPath`, `json.schemas` et `xml.fileAssociations` vers les schémas du paquet
lepton, `json.validate.enable: false`, `lepton.probeSerial`) ; `launch` (une configuration Cortex-Debug
par configuration : `servertype` `qemu` ou `openocd` seulement, `configFiles` = champ `openocd` du BSP,
SVD ; une configuration CodeLLDB par couple BSP/XML pour mklepton, DBG-5) ; `tasks` (regreffer,
vérifier, configurer/mklepton host, puis par preset configurer, construire, QEMU console série, fumée,
banc KAL, tests greffons, ou flasher) ; `extensions.recommendations`.

Autour : `prime_active` (amorce `build/.active/compile_commands.json`), `write_api_queries` (requête
codemodel par `build/<preset>`), `touch_link` (CMake Tools ne voit pas une réécriture à travers le lien,
L6-5). Outils hôtes (cmake, ctest, arm-none-eabi-gcc, gdb avec Python, clangd LLVM, qemu, openocd)
résolus **par le PATH à la génération** et figés en chemins absolus.

Constats sur `~/lepton/original-tree.code-workspace` : 15 dossiers, 23 lancements, 69 tâches ;
chemins absolus partout, y compris vers le venv pipx
(`…/pipx/venvs/lepton/lib/python3.11/site-packages/lepton/schemas/…`) ; fichier entièrement régénéré
(« ne pas éditer ») ; un seul numéro de série de sonde pour toutes les configurations carte, à redonner
séparément à CMake (`-DLEPTON_BOARD_PROBE_SERIAL`, ENV-45, `cmake/lepton_greffons.cmake`
`_lepton_sonde_cfg`) ; champ `sonde` du BSP (`stlink` | `jlink` | `cmsis-dap`, GRF-3) **jamais lu** par
`generate` ; une copie du rootstock garde les chemins de l'original (D45 du hors-plan d'ENV).

### 2.2 Extension Lepton 0.5.4 (`extension/`)

Couche mince : chaque action appelle `lepton`. Répertoire de travail = répertoire du fichier
`.code-workspace` ouvert (`runner.ts` `cwd()`), d'où `lepton` remonte jusqu'au rootstock
(`Rootstock.discover`, signature du rootstock). N'écrit rien dans l'espace. Installée par
`scripts/install-vscodium.sh` (`.vsix` de `extension/dist/`), extensions épinglées dans
`scripts/extensions.lst`.

### 2.3 Graines

- **Graine de projet** (`lepton seed new`) : dépôt git propre (`depots/lepton-seed/<nom>` ou
  `--seed-repo`), manifeste `lepton-graine.json` (requis : `projet`, `noyau`, `bsp`, `backend`,
  `configurations`, `mklepton_xml` ; `applications`, `bibliotheques`), **un seul BSP, un seul
  backend** ; répertoire `project/` = greffon local du projet (presets, XML copié par `--mkconf`,
  `.boot`, `.init`, sous `sys/user/<projet>/etc/`).
- **Graine de référence** `original-tree` (`lepton-distribution/lepton-seed.scions.git`, branche
  `original-tree`) : antérieure à `lepton` ; ni `lepton-graine.json` ni `project/` (critère PA-19 C
  d'ENV-16) ; 14 entrées dans `.scion.sources.list` : noyau `original::tree`
  (`https://github.com/lepton-distribution/lepton-original-tree.scions.git`, clone
  `depots/lepton/original/master`), `building`, 5 familles, 7 BSP ; multi-cartes, pilotée par scion
  dans son dépôt ; presets du noyau (`CMakePresets.json`, 16 presets) utilisés tels quels ; commandes
  `lepton` qui modifient la graine refusées (PA-23 d'ENV-18) ; `generate` n'écrit rien dans la graine.

### 2.4 Greffons et scion

- Types de greffon (`schemas/greffon.schema.json`) : `noyau`, `famille`, `bsp`, `application`,
  `bibliotheque`. Un BSP déclare `openocd` + `sonde`, ou `qemu`.
- Plusieurs greffons dans un même dépôt : déjà possible (colonne « scion location in depot » de
  `.scion.sources.list` ; option `--origin nom=LOCATION[@VERSION][:PATH]` de lepton).
- Filtre E1 (ENV-15, PA-17, scion 0.5.2.0) : un fichier **ignoré par git** dans un clone n'est pas
  greffé (`git ls-files --others --ignored --exclude-standard --directory`) ; un fichier non suivi mais
  non ignoré est greffé. Fichiers étrangers tolérés dans le trunk : `.scion.trunk.tolerated` (ENV-22).

### 2.5 `sys/user/tauon-basic` du noyau (clone `depots/lepton/original/master`)

51 fichiers suivis (+ 3 `.DS_Store`), 292 Ko :

- `etc/` : 6 XML mklepton (`mkconf_tauon_basic_{qemu_mps2,nucleo_f439zi,nucleo_wl55jc1,
  stm32f746g_disco,samd21_xplained_pro,lwip_stm32f4-olimex-p407}.xml`) ; `.boot`, `.init`, `.mount`,
  `.init_olimex`, `.init_olimex_with_net`, `.init_samv71_with_net`, `.init_win32`,
  `.init_win32_with_net` ; `etc/<carte>/{.boot,.init}` pour `qemu-mps2`, `nucleo-f439zi`,
  `nucleo-wl55jc1`, `stm32f746g-disco`, `samd21-xplained-pro` ;
- `src/arch/<carte>/kernel_mkconf/include/user_kernel_mkconf.h` × 7 (at91sam9261-ek, at91samd20,
  at91samv71, olimex-stm32-p407, st-stm32f407-discovery, st-stm32f469i-eval, win32) ;
- `src/bin/` : dhrystone (6), free (2), sdramtest (1), net/cgi-bin (5), net/html (6).

Utilisation depuis le portage :

- les **5 XML de cartes portées** sont cités par les presets du noyau (`CMakePresets.json`, 8
  `LEPTON_MKCONF`) ; leurs `src_file` ne désignent que `etc/<carte>/.boot` et `.init` (10 fichiers) ;
- le XML Olimex n'est cité par aucun preset ; il est la base du test hôte de mklepton
  (`tests/host/CMakeLists.txt` l. 39-46, `tests/host/mklepton_empreintes.sh` l. 44,
  `mklepton_empreintes.sha256`) avec l'en-tête Olimex, `etc/.boot`, `.mount`,
  `.init_olimex_with_net`, `src/bin/net/{cgi-bin,html}` ;
- rien d'autre n'est cité par un XML de carte portée ni par un CMake.

Références hors de ce répertoire : noyau — `CMakePresets.json`, `tests/host/CMakeLists.txt`,
`tests/host/mklepton_empreintes.{sh,sha256}`, `tests/board_net.py`
(`--ftp-reference sys/user/tauon-basic/etc/nucleo-f439zi/.boot`), `tests/net_qemu.py` ;
lepton-tools — `scripts/bout-en-bout.sh` l. 25, `tests/test_milestone2.py` l. 18,
`schemas/exemples/graine.json` et 8 exemples invalides, `README.md` ; skills `.claude/skills/` :
aucune occurrence. Les graines de projet existantes ont **leur copie** du XML (faite par `seed new
--mkconf`) : non concernées.

## 3. Besoins détaillés

1. Portabilité : un espace régénéré ou copié doit rester valable sur un autre poste, après
   réinstallation de lepton, après changement de chaîne ; ce qui est propre à l'équipe (presets,
   configurations, préférences de débogage) séparé de ce qui est propre au poste (chaîne, sondes).
2. Plusieurs rootstocks sur une machine, chacun avec sa fenêtre : **déjà le cas** (rien n'est partagé
   entre rootstocks, hors `lepton` installé et `LEPTON_EMBOS_ROOT` si posée globalement). Aucun
   travail prévu ; à constater dans le plan.
3. Serveur et sonde choisis dans VSCodium, comme la page « Debugger » d'IAR (driver + options).
4. Avec plusieurs sondes branchées, choix de l'interface par carte, mémorisé, ou demandé au
   lancement comme IAR le fait quand plusieurs sondes répondent.

## 4. Architecture cible (énoncée par l'utilisateur, 2026-11-25)

Un projet de développement = une graine à dépôt propre, qui intègre :

| Greffon | Existant | Cible |
| --- | --- | --- |
| Noyau (`lepton-original-tree.scions`) | clé `original::tree` | inchangé (ni dépôt ni clé renommés) |
| Famille du microcontrôleur | type `famille` | inchangé |
| BSP de la carte du projet | type `bsp` | inchangé |
| « bin » des applications du projet | type `application` | inchangé (vocabulaire seulement) |
| **Projet** : `trunk/sys/user/<projet>/` — XML mklepton, `.boot`/`.init`, `.code-workspace`, fichiers de configuration propres au développeur et au poste (non versionnés) | `project/` du dépôt de la graine, greffon local | **nouveau type `projet`**, dépôt propre ou partagé avec BSP et bin ; **remplace** `project/` |

Trois couches : **graine et greffon projet = projet** (versionnés, partagés) ; **fichier de poste =
machine** (non versionné : chaîne, outils, sondes et numéros de série par carte) ; **espace de
travail = projection des deux**, en chemins relatifs, régénérée sans effet de bord.

Note (PA-E1, 2026-11-26) : depuis la révision de C2, le `.code-workspace` n'est plus un fichier du
greffon projet ; celui-ci fournit le contenu versionné que `generate` projette dans l'espace, à la
racine du rootstock.

## 5. Décisions prises (utilisateur, 2026-11-25)

| # | Décision |
| --- | --- |
| C1 | Les quatre axes du §1 sont l'objet du chantier ; référence de comportement : IAR Embedded Workbench. |
| C2 | Emplacement de l'espace : `trunk/sys/user/<projet>/<nom>.code-workspace`, fourni par le greffon projet (revient sur D2 d'ENV-9). — **Révisée au PA-E1 (2026-11-26, `STATUS.md` §Décisions)** : l'espace reste un fichier régulier à la racine du rootstock, généré depuis le contenu versionné du greffon projet (piste P-a, `rapports/ep-0-essai-lien.md` §6) ; D2 d'ENV-9 n'est touchée que si le contenu d'équipe retenu au PA-E8 le demande (T9). |
| C3 | **Un seul** espace par projet, complété par un fichier de poste non versionné (pas plusieurs `.code-workspace` par projet). |
| C4 | Nouveau type de greffon `projet` à dépôt propre (ou partagé avec BSP et bin) ; il **remplace** le `project/` du dépôt de la graine (un seul concept). `seed new` crée ou désigne ce dépôt. Conséquence : le critère de reconnaissance de la graine de référence devient « pas de `lepton-graine.json` ». Sort des graines d'essai existantes : à borner dans l'étape. |
| C5 | Fichiers de poste : solution (a) — scion greffe des motifs ignorés par git **déclarés par le greffon** (évolution générique de scion, NF-2) ; lepton crée le fichier de poste dans le greffon projet, ignoré par git, et `generate` le lit. (b) fichiers tolérés dans le trunk et (c) fichier à la racine du rootstock sont écartés. |
| C6 | `tauon-basic` : **option B** — greffon `lepton-original-tree-project` (type `projet`, dépôt GitHub propre sous `lepton-distribution/`), `scion/sys/user/lepton-basic/`. Les XML **gardent leur nom** (`mkconf_tauon_basic_*.xml`). Repris : les 5 XML des cartes portées et les 10 `etc/<carte>/{.boot,.init}` — 15 fichiers, `src_file` réécrits `sys/user/lepton-basic/…`. Non repris : `etc/.boot`, `.init`, `.mount`, les 5 variantes `.init_*`, `src/bin/*`, les 7 `user_kernel_mkconf.h` (hors plan, comme A3). |
| C7 | Résidu dans le noyau : option (i) — `sys/user/tauon-basic/` reste dans le noyau, amputé des 15 fichiers repris ; le test hôte de mklepton garde ses entrées au même chemin (empreintes inchangées) ; le trunk porte `sys/user/tauon-basic/` (résidu, consigné hors plan) à côté de `sys/user/lepton-basic/` (greffon). Option (ii) — déplacer le jeu Olimex sous `tests/host/` et supprimer le résidu — **pour plus tard**. |
| C8 | **Régime de graine de référence conservé** pour `original-tree` : le greffon `lepton-original-tree-project` y est ajouté par scion, dans son dépôt (comme les BSP en ENV-13/19/20) ; pas de conversion en graine de projet (impossible sans manifeste multi-BSP/multi-backend : hors chantier). `generate` écrit l'espace dans le greffon projet dès qu'un greffon de type `projet` est greffé — le greffon n'est pas la graine, PA-23 Q3 reste respecté — et à la racine du rootstock sinon. — **Annotée au PA-E1 (2026-11-26)** : la branche « espace dans le greffon projet » est sans objet depuis la révision de C2 ; l'espace est à la racine dans les deux régimes. Le reste de C8 est inchangé. |
| C9 | J-Link : **différé** — sera validé plus tard sur une autre carte, avec un projet et un BSP spécifiques. Le schéma garde `jlink` ; le chantier valide OpenOCD avec ST-LINK et CMSIS-DAP. |
| C10 | Chantier propre (`doc/espace-projet/`), plan à établir par la skill `lepton-portage-instructions` depuis une session Claude Code CLI sur la machine de développement ; suivi de l'état à choisir : réutiliser `DEVENV-STATUS.md` ou ouvrir un fichier d'état propre (recommandation §8). |

## 6. Directions techniques (propositions de la session, non validées une à une)

Note (PA-E1, 2026-11-26) : texte historique. L'essai (a)/(b) a été fait en EP-0 et C2 révisée ;
la phrase « `${workspaceFolder:trunk}/..`, acceptés par clangd, CMake Tools, `launch`, `tasks` »
est réfutée pour clangd (`rapports/ep-0-essai-lien.md` §3).

- **Portabilité** : l'espace cesse de figer le poste. Chemins relatifs à l'espace
  (`${workspaceFolder:trunk}/..`, acceptés par clangd, CMake Tools, `launch`, `tasks`) ; valeurs de
  poste par variables (`${config:lepton.…}` posées dans les réglages utilisateur de VSCodium, ou
  `${input:…}` servi par l'extension depuis le fichier de poste) ; schémas pointés dans le rootstock
  plutôt que dans le venv. À prouver d'abord par essai VSCodium : (a) les chemins relatifs de
  `folders` d'un `.code-workspace` ouvert **par un lien** du trunk sont-ils résolus depuis le lien
  (`trunk/sys/user/<projet>/`, 4 niveaux sous le rootstock) ou depuis la cible dans le clone (7
  niveaux) ? (b) une modification de réglage « espace de travail » depuis l'interface écrit-elle à
  travers le lien, ou remplace-t-elle le lien par un fichier régulier (fichier étranger du trunk,
  signalé par `lepton check`, peut-être intercepté par la redirection FIC-3 de l'extension) ?
- **Débogage** : le BSP décrit la cible (MCU, cfg OpenOCD de carte, SVD, cœur) ; serveur et sonde sont
  un réglage de projet/poste. `sonde` du BSP → liste des sondes admises ; cfg OpenOCD du BSP scindée
  en cible et interface, l'interface choisie à la génération ou au lancement ; `generate` émet une
  configuration par serveur admis (Cortex-Debug : `openocd`, `jlink`, `stlink`, `pyocd`) ou une seule
  avec `${input:…}` ; préréglage dans la graine (`configurations[].debug`).
- **Sondes** : numéro de série **par carte** dans le fichier de poste (`sondes: {<bsp>: <série>}`),
  lu par `generate` **et** par le lecteur CMake du noyau (fin du double réglage
  `LEPTON_BOARD_PROBE_SERIAL`) ; à défaut, choix au lancement par un `inputs` de type `command` de
  l'extension (`lepton.pickProbe`, sondes connectées listées par OpenOCD, `system_profiler`, `lsusb`)
  qui mémorise le choix ; en ligne de commande (NF-1) : `lepton probe list` / `lepton probe set`.
- **Extraction de `lepton-basic`** : oracle avant/après (binaires attendus identiques : seuls les
  chemins `src_file` changent) ; presets du noyau → `sys/user/lepton-basic/…` ; références
  lepton-tools (§2.5) ; graine de référence ; validation Debian.

## 7. Étapes candidates et dépendances (entrée de `lepton-portage-instructions`)

Note (PA-E1, 2026-11-26) : texte historique, entrée du plan ; l'emplacement de l'espace décrit
pour E-C est révisé (C2, `STATUS.md` §Décisions).

Préfixe et numérotation à fixer par le plan. Ordre des dépendances :

| Étape | Objet | Dépôts | Dépend de |
| --- | --- | --- | --- |
| E-A | Greffon de type `projet` dans lepton : schémas (type `projet`, slot dans la graine), `seed new` (dépôt du greffon projet créé ou désigné, partageable), remplacement de `project/`, `CMakeUserPresets.json` au stem du greffon, `seed mkconf import`, `check`, `seed status/tree`, critère de référence réduit, extension, tests ; graines d'essai existantes (PA) | lepton-tools | — |
| E-B | scion : motifs ignorés greffables déclarés par le greffon (générique), documentation, version, `SCION_MIN_VERSION`, `SCION_REF`, effets sur lepton | seed.scions, lepton-tools | — |
| E-C | `lepton generate` portable : tâche 1 = essai VSCodium du lien (§6 (a), (b)) avant toute décision ; espace relatif dans `sys/user/<projet>/`, fichier de poste (nom, schéma, création, lecture), schémas, `build/.active`, repli racine pour la référence | lepton-tools | E-A, E-B |
| E-D | Débogage : serveur et interface par configuration (ST-LINK, CMSIS-DAP validés ; `jlink` émis, non validé, hors plan), sondes par carte, source unique pour CMake, `lepton probe`, choix au lancement par l'extension ; cartes NUCLEO-F429ZI, F746G-DISCO, WL55JC1 (2 sondes), SAMD21 | lepton-tools, noyau (lecteur CMake) | E-C |
| E-E | Greffon `lepton-original-tree-project` : dépôt GitHub (`gh`, accord), 15 fichiers, `src_file`, graine de référence par scion, noyau amputé, presets du noyau, références lepton-tools, oracle avant/après | noyau, graine de référence, nouveau dépôt, lepton-tools | E-A (type `projet`) |
| E-F | Résidus D41, D42 du hors-plan d'ENV, si ce chantier les reprend (décision à prendre) | lepton-tools | — |
| E-G | Validation Debian groupée (protocole `doc/devenv/ORCHESTRATION.md` §2bis) | VM | toutes |

Points d'arrêt attendus : avant implémentation de chaque étape (interface, schémas, noms), avant
tout push et toute publication (PA-P), création du dépôt GitHub, `gh`, essai VSCodium par
l'utilisateur, autorisation d'écriture flash.

## 8. Cadre du chantier

- Dépôts : lepton-tools (outil, schémas, extension, scripts), seed.scions (générique, NF-2), clone
  noyau, graine de référence `lepton-seed.scions` (`original-tree`), nouveau dépôt
  `lepton-distribution/lepton-original-tree-project` ; rootstock `~/lepton` ; VM Debian pour la
  validation.
- Règles reprises **par référence** du chantier ENV (ne pas recopier) : `doc/devenv/ORCHESTRATION.md`
  §2bis (protocole Mac/VM, formes des commandes, variables d'environnement, contrôle Mac d'une
  consigne), §4 PA-P, §5 règles de travail, hook `.claude/hooks/proteger-trunk.py`, règles de
  permission `.claude/settings.json`, skills `lepton-rootstock`, `lepton-oracle`, `lepton-cibles`.
- Skill de session : `devenv-session` est liée en dur à `doc/devenv/`, `DEVENV-STATUS.md`,
  `handoff/env-N.md` ; un chantier propre demande une skill de session dérivée (corrigée sur le
  compte claude.ai, importée par `scripts/importer-skills.sh`, règle d'ORCHESTRATION §5bis) ou
  l'adaptation de `CLAUDE.md`.
- Suivi de l'état — recommandation de la session : **fichier d'état propre** (`doc/espace-projet/`
  : ORCHESTRATION, STATUS, étapes, passations, rapports), parce que l'objet diffère de la
  spécification d'ENV (INS/GRA/IDE…), que `ORCHESTRATION.md` (59 Ko) et `DEVENV-STATUS.md` (84 Ko)
  lus en entier à chaque session sont devenus le premier coût, et qu'ENV est formellement « fin du
  plan, en pause ». Réutiliser ENV (ENV-73+) reste la voie sans outillage nouveau si la skill de
  session n'est pas dérivée.
- Relecture de toute révision du plan par un agent indépendant (effort `xhigh`, lecture seule),
  constats présentés à l'utilisateur (règle du 2026-11-09).

## 9. Points ouverts pour la session de plan

1. Nom du chantier, préfixe des étapes, nom et format du fichier de poste, nom de l'évolution de
   scion (motifs ignorés greffables).
2. Sort des graines d'essai existantes avec `project/` (`essais/env-9`, `env-11/*`, `env-13-vierge`…)
   : migrées ou laissées.
3. D41 et D42 (hors-plan d'ENV, « à traiter ») : repris par ce chantier (E-F) ou laissés à ENV.
4. Hors plan de ce chantier, à consigner : J-Link (C9), option (ii) du résidu `tauon-basic` (C7),
   graine multi-BSP (C8), publication de l'extension sur Open VSX (A4 d'ENV).
5. Lancement : `claude` à la racine de `~/lepton-tools-dev/lepton-tools`, lire ce fichier, puis
   `lepton-portage-instructions` ; aucune branche ni aucun commit n'existe encore pour ce chantier.
