# lepton-tools

Outillage de l'environnement de développement Lepton : outil en ligne de commande `lepton`
(graine, greffons, configuration, génération des fichiers de l'éditeur), schémas, modèles et
script d'installation de VSCodium.

État : plan de réalisation uniquement. Voir `doc/devenv/`.

| Fichier | Rôle |
| --- | --- |
| `CLAUDE.md` | Consignes permanentes pour Claude Code |
| `.claude/skills/` | Skills : session, rootstock, oracle, cibles |
| `.claude/hooks/proteger-trunk.py`, `.claude/settings.json` | Hook refusant les écritures dans le trunk |
| `scripts/oracle/` | Capture et comparaison d'oracle de non-régression |
| `doc/devenv/SPECIFICATION.md` | Spécification fonctionnelle (exigences et décisions) |
| `doc/devenv/ORCHESTRATION.md` | Organisation : dépôts, hôtes, cycle de session, points d'arrêt, dépendances |
| `doc/devenv/DEVENV-STATUS.md` | État du chantier (source unique) |
| `doc/devenv/handoff/` | Passations entre sessions |
| `doc/devenv/etapes/ENV-*.md` | Instructions par étape |
| `doc/devenv/rapports/` | Rapports produits par les étapes |

Démarrage : ouvrir un terminal à la racine de ce dépôt, lancer `claude`, puis demander
« Démarre la session sur l'étape indiquée dans DEVENV-STATUS ».
