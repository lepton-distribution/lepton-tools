# Consignes Claude Code — dépôt lepton-tools

Chantier : environnement de développement Lepton (outil `lepton`, intégration VSCodium).
Langue : français. Ton neutre, objectif, concis.

## Skills du dépôt (`.claude/skills/`)
| Skill | Quand |
| --- | --- |
| `devenv-session` | Début et fin de toute session — obligatoire (sauf session de ticket, ci-dessous) |
| `lepton-rootstock` | Toute écriture, tout git, toute regreffe dans l'arbre Lepton |
| `lepton-oracle` | Avant et après toute modification qui doit être sans régression |
| `lepton-cibles` | Construction, QEMU, banc KAL, flash, débogage |

Ces skills se modifient sur le compte claude.ai (Claude Desktop), jamais directement dans
`.claude/skills/`. Après synchronisation (`~/.claude/skills/synced/`, au démarrage d'une session
Claude Code), `scripts/importer-skills.sh` les copie dans le dépôt ; commit dédié (ORCHESTRATION
§5bis). Dans ce dépôt, invoquer le skill sans préfixe, jamais sa copie `anthropic-skills:<nom>`.

Le hook `.claude/hooks/proteger-trunk.py` refuse les écritures dans `<ROOTSTOCK>/trunk/`
et `<ROOTSTOCK>/depots/tiers/`. Un refus signale une erreur de chemin : ne jamais le contourner.

## Règles permanentes
- Début de session : skill `devenv-session`, puis mode plan et accord de l'utilisateur.
- Exception (décision de l'utilisateur du 2026-11-18) : une session de ticket (skill
  `lepton-ticket-traiter` du plugin `lepton-tickets`) n'est pas une session d'étape.
  `devenv-session` ne s'y applique pas ; elle ne touche ni `DEVENV-STATUS.md` ni `HORS-PLAN.md`
  et ne crée aucune branche `devenv/`. Le hook, les règles de permission et l'interdiction de
  push sans accord s'y appliquent.
- Une session = une étape. Une branche `devenv/env-<N>` par dépôt touché.
- S'arrêter à chaque point d'arrêt d'`doc/devenv/ORCHESTRATION.md` §4 qui concerne l'étape.
- Aucune hypothèse silencieuse : un manque devient une question à l'utilisateur.
- `scion` reste générique : aucune chaîne propre à Lepton dans `seed.scions`.
- Pas de `git push`, pas de `scion seed-update` / `graft-update` sans accord explicite.
- Règles de permission (`.claude/settings.json`, ORCHESTRATION §2bis) : suppressions par
  `scripts/supprimer-essai.sh` ; l'invite de Claude Code sur `graft-update`, `seed-update` et
  `git push` s'ajoute à l'accord de l'utilisateur, sans le remplacer.
- Fin de session, même interrompue : skill `devenv-session` (état, passation, commit).
