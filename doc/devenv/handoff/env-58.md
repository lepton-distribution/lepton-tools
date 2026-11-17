# Passation ENV-58 — Claude Code : formes des commandes et règles de la VM (D20, D19) — session du 2026-11-17

## Statut
Terminée. ORCHESTRATION §2bis porte les formes des commandes. Le hook demande l'invite pour une
commande `ask` lancée indirectement (garde G2, prouvée au Mac). Les règles utilisateur de la VM
sont gardées.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` (fusion `--no-ff` de `devenv/env-58`) ; `devenv/env-58` | branche : c5f1c87 audit, f3da447 garde G2, 40fd14e ORCHESTRATION, 17b7ca7 contrôles, puis le commit d'état et de passation ; `main` et `devenv/env-58` poussés (PA-104) | oui |
| clone noyau `depots/lepton/original/master` | `master` | ed2a41f, non touché | oui |
| seed.scions | `master` | d650414 (tag 0.6.3.1), non touché | oui |
| autres | — | graine `original-tree` 15740f9, non touchée ; `<ROOTSTOCK>` non touché | oui |

Outils : scion 0.6.3.1 et lepton 0.1.0 (non réinstallés) ; Claude Code **2.1.326** au Mac.
`.claude/settings.json` est inchangé.

## Fait pendant la session
- Début : état conforme à la passation de préparation, sauf deux écarts consignés au journal :
  - 75c1167 avait été poussé le 2026-11-13 (reflog), alors que la passation le disait non
    poussé ;
  - Claude Code est en 2.1.326, pour 2.1.323 épinglé.
- Inventaire (`rapports/env-58-formes.md` §1) :
  - aucune commande `allow` avec redirection dans les skills, `CLAUDE.md`, la consigne d'ENV-57
    ni les étapes 59 à 61 ;
  - une seule commande `ask` dans un script : `rapports/env-53-mac/regreffer-essai.sh:31`, outil
    historique laissé tel quel.
- Essai témoin (§2 ; décisions dans `rapports/env-58-formes/decisions.tsv`, lues par
  `env-57-mac/decisions.py`), sur un pytest d'un seul test dans la forme couverte :
  - règle : forme nue, `2>&1`, `--junitxml` ;
  - classifieur : `> f` (cible `~/…` ou absolue hors du répertoire de travail), `> f 2>&1`,
    `| tee f`, `; echo "code=$?"` ;
  - `mode` : `>` vers un fichier du répertoire de travail ;
  - `scion graft-update -v ~/lepton-tools-dev/essais/env-58-absent` : invite en direct (A1). Par
    script (A2) et par `bash -c` (A3) : classifieur, exécutée sans invite.
- Documentation (§3), relevée par un agent `claude-code-guide` : une règle `ask` ou `deny`
  « isn't a security boundary » ; la cible d'une redirection est contrôlée comme une écriture de
  fichier.
- PA-103 tranché (§6). Mise en place :
  - garde G2 dans `.claude/hooks/proteger-trunk.py` (f3da447), tests `tests/test_garde_ask.py`
    (46). Preuve : A2 et A3 sur invite, refusées par l'utilisateur, motif du hook affiché ;
  - ORCHESTRATION §2bis et §5bis (40fd14e).
- Contrôles (§8) :
  - rejeu de F1 et F6 : règle ;
  - `touch` sous le trunk d'une copie `qemu` : refusé par le hook ;
  - pytest complet : **499 passed** (`venv-lepton-tools`, `--junitxml`, forme couverte).
- PA-104 tranché :
  - `essais/env-58-essai` supprimé par `scripts/supprimer-essai.sh` ;
  - `HORS-PLAN.md` : D20 traité, D19 décidé (gardé) ;
  - fusion et push.

## Reste à faire dans l'étape
- Rien. La preuve sur la VM se fait en ENV-61 (rapport §7).

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Plan de session ; écarts du début (75c1167 poussé, Claude Code 2.1.326, recherche par `grep` sans outil Grep) | utilisateur | oui |
| PA-103 (1) : amendement du §2bis, texte du rapport §5 point 1 ; le §2 des consignes VM renvoie au §2bis | utilisateur | oui |
| PA-103 (2) : garde G2, sinon G1 ; condition remplie, G2 retenue | utilisateur (condition constatée par la session) | oui |
| PA-103 (3) : les 3 règles `allow` de la VM gardées, fichier non modifié, D19 clos comme accepté | utilisateur | oui |
| PA-103 (4) : ni `CLAUDE.md` ni skills ; `env-53-mac/regreffer-essai.sh` laissé tel quel | utilisateur | oui |
| PA-104 : rapport accepté, essai supprimé, fusion et push ; fichier d'étape d'ENV-61 non corrigé, les effets passant par cette passation | utilisateur | oui |
| Formes F7 à F9 ajoutées à l'essai ; motif exact et périmètre de G2 (shells, `eval`, `find -exec`, `xargs`, heredoc, scripts shell lus récursivement, limites) | proposition de la session, mise en œuvre avec G2 | rapport §2, §6 |

## Effets à reprendre par ENV-61 (rapport §7)
- Réglages de la VM : aucune modification au §0. C2 relit `~/.claude/settings.json` ; une
  décision `userSettings` pour une commande que seule une règle utilisateur couvre est attendue.
- C2 : aucun contrôle négatif « règle retirée ». Formes de l'essai d'ENV-58 attendues sur la VM :
  - pytest nu, `2>&1`, `--junitxml` → règle ; `> f` hors du répertoire de travail → classifieur ;
  - `graft-update` direct → invite (règle `ask`) ;
  - par script et par `bash -c` → **invite, demandée par le hook (G2)**, à refuser ;
  - `bash doc/devenv/rapports/env-58-formes/ask-script.sh ~/lepton-tools-dev/essais/env-61-absent`
    (cible en argument).
- Le hook de la VM est celui du dépôt : G2 y est actif dès le `git switch` sur la branche
  d'ENV-61.

## Pièges rencontrés
- Invite A1 confirmée au lieu d'être refusée : sans effet, la cible étant absente. C'est la même
  manipulation qu'au N4 d'ENV-57 ; seules les cibles absentes rendent l'erreur bénigne.
- Pas d'outil Grep dans la session. Recherche par `grep` en Bash, avec les motifs `graft.update`,
  `seed.update` et `\bpu[s]h\b` : aucun refus.
- zsh ne découpe pas `$F` en mots pour `grep … $F`. Utiliser `find … -exec grep … {} +`.
- `decisions.py --motif` retient aussi ses propres appels qui citent le motif. Les filtrer avant
  de verser le relevé.
- Depuis G2, toute commande qui lance un script shell contenant `scion graft-update`,
  `seed-update` ou `git push` (hors commentaires) fait paraître une invite, même en lecture
  (`bash f.sh -h`). `cat`, `grep` et les lectures n'en déclenchent pas.
- Le journal de session ne garde pas le motif du hook, seulement le refus
  (`toolDenialKind: user-rejected`).

## Critères de validation
- [x] PA-103 et PA-104 tranchés et consignés.
- [x] Inventaire des formes fautives au rapport (fichier, ligne).
- [x] Essai témoin consigné, avec les décisions du journal de session :
      - redirection : règle ou classifieur, pour chaque forme ;
      - `ask` direct, depuis un script et par `bash -c` : invite ou classifieur.
- [x] ORCHESTRATION §2bis amendé ; `consignes/env-57-debian.md` §2 n'est plus la seule source de
      la règle.
- [x] Bloc `permissions.allow` attendu sur la VM, et conduite de modification, au rapport (D19) :
      inchangé, aucune modification.
- [x] `pytest` complet vert (499) ; `settings.json` inchangé, JSON valide.
- [x] `HORS-PLAN.md` : D20 marqué traité ; D19 décidé (gardé) plutôt qu'« appliqué en ENV-61 »,
      avec renvoi au rapport.

## Reprise
Commande ou première action de la session suivante :
```
démarre la session ENV-59 (skill devenv-session) : lire etapes/ENV-59-lepton-indice-tilde.md et
handoff/env-58.md ; branche devenv/env-59 de lepton-tools depuis main ; tâche 1 jusqu'au PA-105
```
