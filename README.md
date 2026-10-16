# lepton-tools

Outillage de l'environnement de développement Lepton : outil en ligne de commande `lepton`
(graine, greffons, configuration, génération des fichiers de l'éditeur), schémas, modèles et
script d'installation de VSCodium.

État : outil `lepton` 0.1.0 (ENV-8, jalons 1 à 6 ; `lepton generate` ajouté en ENV-9). Voir `doc/devenv/`.

Installation : `pipx install <ce dépôt>` (dépendance `jsonschema` installée par pipx ; scion ≥ 0.5.1.1
requis). Développement : `python3 -m venv ~/lepton-tools-dev/venv-lepton-tools`, puis
`pip install -e '.[test]'` et `python -m pytest`.

Environnement complet (VSCodium épinglé, extensions de `scripts/extensions.lst` depuis Open VSX,
chaîne par les scripts du noyau, scion, lepton ; macOS Intel et Apple Silicon, Debian) :
`scripts/install-vscodium.sh --lepton-clone <clone du noyau> [--seed-scions <clone seed.scions>]`
(`--dry-run` affiche sans exécuter ; `--help` pour les options). Rejouable.

Commandes disponibles (0.1.0) : `lepton --version`, `lepton check [FILE...]` (sans argument :
graine, greffons greffés et XML du rootstock), `lepton seed new | status | add | remove | replace |
lock`, `lepton scion new | remove`,
`lepton file add | remove | mv`, `lepton dir add | remove`, `lepton graft`, `lepton generate`
(`lepton <commande> [<action>] --help`). Exemple :

```
lepton seed new demo -C ~/demo --bsp qemu-mps2-an386 \
    --mkconf sys/user/tauon-basic/etc/mkconf_tauon_basic_qemu_mps2.xml \
    --origin qemu-mps2=<dépôt de la famille> --origin qemu-mps2-an386=<dépôt du BSP>
cd ~/demo/trunk
lepton scion new ma-carte --type bsp --from qemu-mps2-an386   # dépôt depots/lepton-bsp/ma-carte
lepton file add sys/root/src/kernel/dev/bsp/ma-carte/gpio.c    # créé dans le clone, regreffé
lepton check                                                   # GRA-2, GRF-5, CFG-5
lepton seed lock                                               # lepton-graine.lock.json (GRA-5)
lepton generate        # CMakeUserPresets.json (graine, greffé) et ~/demo/demo.code-workspace
codium ~/demo/demo.code-workspace
```

Dans VSCodium, ouvrir les fichiers par le dossier `trunk` (les fichiers greffés sont masqués dans les
dossiers `git · …`). Après un changement de preset, rouvrir les fichiers déjà ouverts (ou
*clangd: Restart language server*) pour qu'ils prennent la nouvelle configuration. À l'arrêt du
débogueur, le source s'affiche sous le chemin du clone (écart accepté en PA-1). Validation :
`doc/devenv/rapports/env-9-validation.md`.

L'espace généré associe `lepton-greffon.json`, `lepton-graine.json` et les XML `mkconf_*.xml` (et
celui de la graine) aux schémas installés avec lepton : fautes signalées à la saisie (CFG-7) ;
relancer `lepton generate` après une réinstallation de lepton. Le sélecteur de preset est affiché
dans la barre d'état. La tâche « lepton : vérifier » lance `lepton check` et inscrit ses anomalies en
erreur dans le panneau *Problems* (manifestes désignés par le trunk). clangd lit `build/.active/compile_commands.json`, que `lepton generate`
amorce depuis le premier preset déjà configuré : configurer un preset (tâche « lepton :
configurer … ») avant la première génération, sinon *clangd: Restart language server* après la
première configuration. Plusieurs sondes branchées : `lepton generate --probe-serial SERIE`
(numéro de la sonde de la carte, `adapter serial` d'OpenOCD ; macOS : `system_profiler
SPUSBDataType`, Debian : `lsusb -v`), conservé dans l'espace aux générations suivantes,
`--probe-serial ""` le retire (`doc/devenv/rapports/env-9-r4.md`). gdb : le premier
`arm-none-eabi-gdb` ou `gdb-multiarch` du PATH construit avec Python (commande `lepton-stacks` de
`debug/gdbinit-lepton`), sinon le premier trouvé, avec un avertissement.

Valeurs d'options (CFG-4) : les options déclarées par un greffon (`options` de son
`lepton-greffon.json`) se fixent pour tout le projet dans le champ `options` de
`lepton-graine.json`, par greffon : `"options": {"mesure": {"MESURE_PERIODE_MS": 500}}` ; option
absente : défaut du manifeste. `lepton check` contrôle type, bornes et valeurs admises ;
`lepton generate` les reporte dans les presets (`LEPTON_OPTION_<greffon>_<NOM>`) : le relancer
après toute modification. CMake refuse une valeur hors bornes, y compris passée par `-D`
(`doc/devenv/rapports/env-8-r2-options.md`).

Bout en bout (construction et fumée QEMU, chaîne Arm et QEMU requis) :
`scripts/bout-en-bout.sh <répertoire jetable>`.

| Fichier | Rôle |
| --- | --- |
| `pyproject.toml`, `lepton/`, `tests/` | Outil `lepton` (interface : `doc/devenv/rapports/env-8-interface.md`) et ses tests `pytest` |
| `lepton/templates/` | Modèles de graine, BSP, application et bibliothèque |
| `schemas/` | Schémas des manifestes (copiés dans le paquet `lepton`) et exemples |
| `CLAUDE.md` | Consignes permanentes pour Claude Code |
| `.claude/skills/` | Skills : session, rootstock, oracle, cibles |
| `.claude/hooks/proteger-trunk.py`, `.claude/settings.json` | Hook refusant les écritures dans le trunk |
| `scripts/oracle/` | Capture et comparaison d'oracle de non-régression |
| `scripts/bout-en-bout.sh` | Bout en bout de `lepton` : graine an386 → check → lock → cmake → fumée QEMU |
| `doc/devenv/SPECIFICATION.md` | Spécification fonctionnelle (exigences et décisions) |
| `doc/devenv/ORCHESTRATION.md` | Organisation : dépôts, hôtes, cycle de session, points d'arrêt, dépendances |
| `doc/devenv/DEVENV-STATUS.md` | État du chantier (source unique) |
| `doc/devenv/handoff/` | Passations entre sessions |
| `doc/devenv/etapes/ENV-*.md` | Instructions par étape |
| `doc/devenv/rapports/` | Rapports produits par les étapes |

Démarrage : ouvrir un terminal à la racine de ce dépôt, lancer `claude`, puis demander
« Démarre la session sur l'étape indiquée dans DEVENV-STATUS ».
