# lepton-tools

Outillage de l'environnement de développement Lepton : outil en ligne de commande `lepton`
(graine, greffons, configuration, génération des fichiers de l'éditeur), schémas, modèles et
script d'installation de VSCodium.

État : outil `lepton` 0.1.0 (ENV-8, jalons 1 à 6 ; `lepton generate` ajouté en ENV-9). Voir `doc/devenv/`.

Installation : `pipx install <ce dépôt>` (dépendance `jsonschema` installée par pipx ; scion ≥ 0.5.1.0
requis). Développement : `python3 -m venv ~/lepton-tools-dev/venv-lepton-tools`, puis
`pip install -e '.[test]'` et `python -m pytest`.

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
