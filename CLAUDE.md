# Consignes Claude Code — dépôt lepton-tools

Chantiers : environnement de développement Lepton (`doc/devenv/`, étapes ENV-N ; outil `lepton`,
intégration VSCodium) ; espace-projet (`doc/espace-projet/`, étapes EP-N).
Langue : français. Ton neutre, objectif, concis.

## Skills du dépôt (`.claude/skills/`)
| Skill | Quand |
| --- | --- |
| `devenv-session` | Début et fin de toute session du chantier ENV — obligatoire (sauf session de ticket, ci-dessous) |
| `espace-projet-session` | Début et fin de toute session du chantier espace-projet — obligatoire ; tant qu'elle n'est pas importée dans le dépôt, suivre `doc/espace-projet/ORCHESTRATION.md` §3 |
| `lepton-rootstock` | Toute écriture, tout git, toute regreffe dans l'arbre Lepton |
| `lepton-oracle` | Avant et après toute modification qui doit être sans régression |
| `lepton-cibles` | Construction, QEMU, banc KAL, flash, débogage |

Ces skills se modifient sur le compte claude.ai (Claude Desktop), jamais directement dans
`.claude/skills/`. Après synchronisation (`~/.claude/skills/synced/`, au démarrage d'une session
Claude Code), `scripts/importer-skills.sh` les copie dans le dépôt ; commit dédié
(`doc/devenv/ORCHESTRATION.md` §5bis). Dans ce dépôt, invoquer le skill sans préfixe, jamais sa
copie `anthropic-skills:<nom>`.

Le hook `.claude/hooks/proteger-trunk.py` refuse les écritures dans `<ROOTSTOCK>/trunk/`
et `<ROOTSTOCK>/depots/tiers/`. Un refus signale une erreur de chemin : ne jamais le contourner.

## Règles permanentes
- Début de session : skill de session du chantier (`devenv-session` pour ENV-N,
  `espace-projet-session` pour EP-N), puis mode plan et accord de l'utilisateur.
- Exception (décision de l'utilisateur du 2026-11-18) : une session de ticket (skill
  `lepton-ticket-traiter` du plugin `lepton-tickets`) n'est pas une session d'étape.
  Aucune skill de session ne s'y applique ; elle ne touche ni `DEVENV-STATUS.md`, ni
  `doc/espace-projet/STATUS.md`, ni un `HORS-PLAN.md`, et ne crée aucune branche `devenv/` ni
  `espace-projet/`. Le hook, les règles de permission et l'interdiction de
  push sans accord s'y appliquent.
- Une session = une étape. Une branche `devenv/env-<N>` (ENV) ou `espace-projet/ep-<N>`
  (espace-projet) par dépôt touché.
- S'arrêter à chaque point d'arrêt du §4 de l'`ORCHESTRATION.md` du chantier (`doc/devenv/` ou
  `doc/espace-projet/`) qui concerne l'étape.
- Aucune hypothèse silencieuse : un manque devient une question à l'utilisateur.
- `scion` reste générique : aucune chaîne propre à Lepton dans `seed.scions`.
- Pas de `git push`, pas de `scion seed-update` / `graft-update` sans accord explicite.
- Règles de permission (`.claude/settings.json`, `doc/devenv/ORCHESTRATION.md` §2bis) :
  suppressions par
  `scripts/supprimer-essai.sh` ; l'invite de Claude Code sur `graft-update`, `seed-update` et
  `git push` s'ajoute à l'accord de l'utilisateur, sans le remplacer.
- Fin de session, même interrompue : skill de session du chantier (état, passation, commit).
