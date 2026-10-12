# Consignes Claude Code — dépôt lepton-tools

Chantier : environnement de développement Lepton (outil `lepton`, intégration VSCodium).
Langue : français. Ton neutre, objectif, concis.

## Skills du dépôt (`.claude/skills/`)
| Skill | Quand |
| --- | --- |
| `devenv-session` | Début et fin de toute session — obligatoire |
| `lepton-rootstock` | Toute écriture, tout git, toute regreffe dans l'arbre Lepton |
| `lepton-oracle` | Avant et après toute modification qui doit être sans régression |
| `lepton-cibles` | Construction, QEMU, banc KAL, flash, débogage |

Le hook `.claude/hooks/proteger-trunk.py` refuse les écritures dans `<ROOTSTOCK>/trunk/`. Un refus
signale une erreur de chemin : ne jamais le contourner.

## Règles permanentes
- Début de session : skill `devenv-session`, puis mode plan et accord de l'utilisateur.
- Une session = une étape. Une branche `devenv/env-<N>` par dépôt touché.
- S'arrêter à chaque point d'arrêt d'`doc/devenv/ORCHESTRATION.md` §4 qui concerne l'étape.
- Aucune hypothèse silencieuse : un manque devient une question à l'utilisateur.
- `scion` reste générique : aucune chaîne propre à Lepton dans `seed.scions`.
- Pas de `git push`, pas de `scion seed-update` / `graft-update` sans accord explicite.
- Fin de session, même interrompue : skill `devenv-session` (état, passation, commit).
