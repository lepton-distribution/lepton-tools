# Passation ENV-57 — Validation Debian groupée (ENV-54 à ENV-56) — session du 2026-11-13

## Statut
Terminée (2026-11-13). C'est la dernière étape du plan. La VM Debian valide :
- les règles de permission du dépôt (D16) ;
- la normalisation des URL `file:///` par lepton (D13) ;
- scion 0.6.3.1 (D14).

C1 à C6 et C8 sont atteints, C7 est écarté. Les 7 rootstocks d'essai du Mac sont regreffés.
`HORS-PLAN.md` a été présenté : D17 à D20 sont à traiter à la prochaine révision du plan.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `devenv/env-57` (depuis `main` 6b6b1d6), fusionnée `--no-ff` dans `main`, les deux poussées (PA-102) | « devenv(env-57): état et passation », au-dessus de 37c7276 (fusion de `devenv/env-57-debian`), 9bed696 (vérification, HORS-PLAN), 33f5e90 (tâche 3), 10b6dd3 (PA-101, consigne), f82af16 (préparation) | oui |
| lepton-tools (VM) | `devenv/env-57-debian` | 6df0de1 « devenv(env-57-debian): rapport R57-1… », poussée, fusionnée dans `devenv/env-57` | oui |
| clone noyau `depots/lepton/original/master` | `master` | ed2a41f, non touché | oui |
| seed.scions, graine, familles, BSP, miroirs | `master` / `original-tree` | non touchés : seed.scions d650414 (tag 0.6.3.1), graine 15740f9 | oui |

`<ROOTSTOCK>` n'a pas été touché : il est `CONFORME` (3889 liens, 629 projetés) et son noyau est
déjà à ed2a41f.

Outils :
- Mac : scion 0.6.3.1 ; lepton 0.1.0, réinstallé par `pipx install --force
  ~/lepton-tools-dev/lepton-tools` (essai de la règle) ; Claude Code 2.1.323 ;
- VM : scion 0.6.3.1 ; lepton 0.1.0 ; extension 0.5.2 ; Claude Code 2.1.323.

Rootstocks d'essai du Mac, tous regreffés par `graft-update` 0.6.3.1. Seul le noyau a avancé
(58e421e → ed2a41f), aucun lien n'a changé, tous sont `CONFORME` :

| Rootstock | Liens | `check` |
| --- | --- | --- |
| `essais/env-13-vierge` | 3889 | 0 |
| `essais/env-9` | 3059 | 0 |
| `essais/env-11/qemu` | 3059 | 0 |
| `essais/env-11/qemu-gra2` | 3051 | 1 (attendu) |
| `essais/env-11/bout-en-bout/rootstock` | 3059 | 0 |
| `essais/env-11/f429zi` | 3294 | 0 |
| `essais/env-11/wl55jc1` | 3315 | 0 |

`qemu-gra2` : BSP an386 retiré par `graft-remove`, sans `--purge`.

Copies d'essai du Mac `essais/env-57-essai` (base des attendus C4 et C5, versionnés) et
`essais/env-57-depot` (dépôt `env55lib`) : supprimées après la clôture par
`scripts/supprimer-essai.sh`, à la demande de l'utilisateur (2026-11-13). Restent les journaux
`essais/env-57-mac/` (dont `pytest-tmp*`), acceptés par l'enveloppe.

VM (état laissé par R57-1) :
- `essais/env-28-debian`, `essais/env-13-debian`, `essais/env-53-c5`, `essais/env-53-debian` :
  regreffés, noyau ed2a41f. `essais/env-53-c5` reste la graine de projet de référence (D15) ;
- supprimés :
  - `essais/env-11/qemu` et `essais/env-11`, par l'utilisateur ;
  - `essais/env-57-essai`, `essais/env-57-depot` et `~/env-53-journaux`, par l'enveloppe ;
- journaux `~/env-57-journaux` ; `~/tmp-pytest` gardé ;
- la session VM tourne dans `~/lepton-tools-dev/lepton-tools`, sur `devenv/env-57-debian`.

## Fait pendant la session
- **Préparation** (`rapports/env-57-mac.md` §1) :
  - têtes publiées (`env-57-mac/ls-remote.sh`) ;
  - `<ROOTSTOCK>` `CONFORME` ;
  - essai préalable `graft-update` d'`essais/env-13-vierge`, d'où l'attendu de C3 :
    `attendu/c3/graft-update-resume.txt`, 82 lignes ;
  - attendus D13 (`attendu/c4/`, 242 fichiers) et D14 (`attendu/c5/`, 50 fichiers), relevés en
    rejouant les scripts d'ENV-55 et d'ENV-56 sur `essais/env-57-essai` ;
  - formes des commandes éprouvées par rapport aux règles (§1.5) ;
  - pytest 453 ;
  - outils `regreffer-essai.sh avant|apres` et `decisions.py` (extracteur des décisions de
    permission du journal de session).
- **Consigne** `consignes/env-57-debian.md` : validée au PA-101 avec C3 étendu à `env-53-c5`, C6
  avec reconstruction et le préalable §0 ; `devenv/env-57` poussée.
- **Ordre R57-1** : ACCUSÉ, 15 AVANCEMENT, 1 QUESTION et FIN-SUCCÈS, tous reçus directement
  (`env-57-mac.md` §3).
- **Tâche 3** (`env-57-mac.md` §4) : 7 rootstocks regreffés, 7 invites `ask` confirmées.
- **Tâche 4** (`env-57-mac.md` §5) : contrôles refaits sur 6df0de1 :
  - C2 : décisions conformes ;
  - C3 : journal et clones identiques au Mac ×3 ;
  - C4 : 0 / 231 ;
  - C5 : 0 / 48, pytest 453 ;
  - C6 : `comparer` 0 ×16, reconstruction complète.
- **PA-102** : fusions et push.
- **`HORS-PLAN.md`** :
  - D19 et D20 ajoutés ;
  - D14 et D16 prouvés sur la VM, D15 clos ;
  - D17 à D20 décidés « à traiter » ;
  - A1 à A4, D4 et D12 reconfirmés hors plan.

## Reste à faire dans l'étape
- [x] Tout ENV-57.
- [x] Hors étape : `essais/env-57-essai` et `essais/env-57-depot` supprimés au Mac (demande de
  l'utilisateur). Journaux `essais/env-57-mac/` conservés.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Plan de session ; essai préalable `graft-update` d'`env-13-vierge` (PA-P) | utilisateur (plan approuvé) | oui |
| PA-101 : C3 avec `env-53-c5` ; C6 avec reconstruction (regreffe de `env-53-debian`) ; C7 écarté ; C8 tel qu'écrit ; préalable §0 ; push, ordre, regreffes du Mac pendant R57-1 | utilisateur | oui |
| Écart N4 : rejouer pour relever un refus | utilisateur (session VM) | oui |
| Push de `devenv/env-57-debian` ; suppression d'`essais/env-11/qemu` | utilisateur (session VM) | oui |
| PA-102 : fusions et push | utilisateur | oui |
| Fin du plan : D17 à D20 à traiter ; A1 à A4, D4, D12 hors plan | utilisateur | oui |
| Formes des commandes de la consigne : `allow` sans redirection, pytest par `--junitxml` et `--basetemp`, `graft-update` lancé hors script | session, d'après les essais du Mac (rapport §1.5) | oui (rapport ; D20 au hors-plan) |
| Copies d'essai du Mac `env-57-essai`, `env-57-depot` supprimées après la clôture | utilisateur | oui (journal) |

## Pièges rencontrés
- **Redirection et règle `allow`** : une commande couverte par une règle `allow` passe au
  classifieur dès qu'elle redirige vers un fichier (`> f 2>&1`). Parade : écrire la commande nue,
  ou faire écrire le journal par l'outil (`pytest --junitxml`). Une règle `ask` vaut avec la
  redirection (D20).
- **`graft-update` dans un script** : lancé depuis un script, il échappe à la règle `ask` (le motif
  porte sur la ligne de commande). Parade : le script en deux phases, `regreffer-essai.sh
  avant|apres`, avec le `graft-update` lancé par la session entre les deux.
- **Journal de session** : les entrées `api-request-blob` reprennent le résultat d'outil sans la
  décision ; `decisions.py` ne lit que les entrées `user`.
- **Nom des sessions** : Claude Code a renommé la session Mac en cours de route (`lepton-tools-30`
  → `validation-debian-env-57`), et la réf. d'une session relancée change (d3fe18 annoncée,
  153462 vue par la VM). Le nom et l'adresse `from` suffisent.
- **Invite à refuser** : une confirmation par erreur passe inaperçue tant que la cible existe.
  D'où les contrôles négatifs sur cibles absentes (N4 confirmé : code 1, sans effet).
- **Règles utilisateur de la VM** : `~/.claude/settings.json` porte 3 règles `allow` antérieures,
  dont `Bash(pipx install:*)` (D19).
- **zsh au Mac** : une ligne `echo ====` échoue (« = » développé) ; utiliser `echo ---` dans les
  commandes composées.

## Critères de validation
- [x] PA-101 et PA-102 tranchés et consignés.
- [x] `FIN-SUCCÈS R57-1` vérifié par la session Mac ; C1 à C6 et C8 conformes, C7 écarté au
      PA-101.
- [x] D16 : journal des commandes lancées par la session VM (acceptées, refusées) au rapport
      (`rapports/env-57-debian.md` §3, `env-57-debian/8-decisions.tsv`).
- [x] Rootstocks d'essai regreffés : 0 lien cassé, 0 fichier régulier (hors `.DS_Store` tolérés) ;
      `check` code 0 (`qemu-gra2` : 1, attendu).
- [x] Fin du plan : `HORS-PLAN.md` présenté à l'utilisateur pour décision.

## Reprise
Commande ou première action de la session suivante :
```
révision du plan avec la skill lepton-portage-instructions : planifier D17 (lepton, indice du
message « version sans effet » sans expanduser), D18 (scion, clone gardé sans le dire après un
checkout en échec), D19 (règles allow utilisateur de la VM) et D20 (ORCHESTRATION §2bis :
commandes allow sans redirection) de HORS-PLAN.md ; lire DEVENV-STATUS.md (Prochaine action) et
cette passation
```
