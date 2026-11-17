# Passation ENV-61 — Validation Debian groupée (ENV-58 à ENV-60) — session du 2026-11-17

## Statut
Terminée (2026-11-17). C'est la dernière étape du plan. La VM Debian valide quatre points :
- D19 : les règles utilisateur de la VM sont gardées ;
- D20 : formes des commandes et garde G2 du hook ;
- D17 : `~` dans l'indice « version sans effet » ;
- D18 : scion 0.6.3.2 et `git clone -b`.

C1 à C6 sont atteints, avec des écarts consignés ; C7 est écarté et C8 est fait. Les 7 rootstocks
d'essai du Mac sont regreffés. `HORS-PLAN.md` a été présenté : D21 à D28 sont à traiter à la
prochaine révision du plan.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `devenv/env-61` (depuis `main` 7018302), fusionnée `--no-ff` dans `main`, les deux poussées (PA-110) | « devenv(env-61): état et passation », au-dessus de f383704 (fusion de `devenv/env-61-debian`), 352e575 (tâche 4), 342d660 (tâche 3), ac3b913 (PA-109, consigne), 088c291 (préparation), 11a11dc (étape en cours) | oui |
| lepton-tools, hors étape (2026-11-17) | `devenv/skills-compte` (depuis `main` 09b2693), fusionnée `--no-ff` dans `main` (fa8a200), les deux poussées (PA-P) | `main` : le commit « état et passation » de la session hors étape, au-dessus de ba117b9 (journal du push) et fa8a200 (fusion) ; branche : f16634a (état et journal), 8ae6fa9 (règle), e8bc60b (script et tests) | oui |
| lepton-tools (VM) | `devenv/env-61-debian` | 2771213 « devenv(env-61-debian): rapport R61-1… », poussée, fusionnée dans `devenv/env-61` | oui |
| clone noyau `depots/lepton/original/master` | `master` | dfc960b, non touché | oui |
| seed.scions, graine, familles, BSP, miroirs | `master` / `original-tree` | non touchés : seed.scions 975caf6 (tag 0.6.3.2), graine 15740f9 | oui |

`<ROOTSTOCK>` n'a pas été touché. Il est `CONFORME` (3889 liens, 629 projetés), et son noyau est
déjà à dfc960b.

Outils :
- Mac : scion 0.6.3.2, lepton 0.1.0 (non réinstallés), Claude Code 2.1.326 ;
- VM : scion 0.6.3.2 et lepton 0.1.0 (réinstallés en R61-1), extension 0.5.2, Claude Code 2.1.326.

Rootstocks d'essai du Mac, tous regreffés par `graft-update` 0.6.3.2. Seul le noyau a avancé
(ed2a41f → dfc960b), aucun lien n'a changé, et tous sont `CONFORME` :

| Rootstock | Liens | `check` |
| --- | --- | --- |
| `essais/env-13-vierge` | 3889 | 0 |
| `essais/env-9` | 3059 | 0 |
| `essais/env-11/qemu` | 3059 | 0 |
| `essais/env-11/qemu-gra2` | 3051 | 1 (attendu) |
| `essais/env-11/bout-en-bout/rootstock` | 3059 | 0 |
| `essais/env-11/f429zi` | 3294 | 0 |
| `essais/env-11/wl55jc1` | 3315 | 0 |

`qemu-gra2` : le BSP an386 a été retiré par `graft-remove`, sans `--purge`.

Copies d'essai du Mac, base des attendus versionnés : `essais/env-61-essai`,
`essais/env-61-depot59`, `essais/env-61-depot60`, `essais/env-61-seed-scions`,
`essais/env-61-fixture`, `essais/env-61-releves`. Elles ont été supprimées après la clôture par
`scripts/supprimer-essai.sh`, à la demande de l'utilisateur (2026-11-17). Restent les journaux
`essais/env-61-mac/` (dont `pytest-tmp`), que l'enveloppe accepte.

VM (état laissé par R61-1) :
- `essais/env-28-debian`, `essais/env-13-debian`, `essais/env-53-c5`, `essais/env-53-debian` :
  regreffés, noyau dfc960b ; `essais/env-53-c5` reste la graine de projet de référence (D15) ;
- supprimés par l'enveloppe : les essais de R61-1 et `~/env-57-journaux` ;
- journaux `~/env-61-journaux` ; `~/tmp-pytest` gardé ;
- la session VM tourne dans `~/lepton-tools-dev/lepton-tools`, sur `devenv/env-61-debian`.

## Fait pendant la session
- **Préparation** (`rapports/env-61-mac.md` §1) :
  - `env-61-mac/ls-remote.sh` (tag 0.6.3.2) ; `<ROOTSTOCK>` `CONFORME` ;
  - essai préalable `graft-update` d'`essais/env-13-vierge` : `attendu/c3/`, 82 lignes ;
  - attendus D17 (`attendu/c4/`, 548 fichiers, 528 comparés), D18 (`attendu/c5/`, 15) et fixture
    d'ENV-56 (`attendu/fixture56/`, 76), relevés sur `essais/env-61-essai` ; tous égaux à ceux
    d'ENV-59 et d'ENV-60, aux noms près et au `-b master` du PA-108 ;
  - `fr()` pour les messages de git traduits sur la VM ; pytest 508.
- **Consigne** `consignes/env-61-debian.md` : validée au PA-109 (toutes options recommandées) ;
  `devenv/env-61` poussée.
- **Ordre R61-1** : ACCUSÉ, 11 AVANCEMENT, 3 QUESTION, FIN-SUCCÈS, tous reçus directement ;
  RÉPONSE de la session Mac à la QUESTION du §6 (`env-61-mac.md` §3).
- **Tâche 3** (`env-61-mac.md` §4) : 6 rootstocks regreffés (plus `env-13-vierge` à la tâche 1) ;
  7 invites `ask` confirmées.
- **Tâche 4** (`env-61-mac.md` §5) : contrôles refaits sur 2771213 :
  - C3 : journal = Mac ×3 ;
  - C4 : 0 / 528 ;
  - C5 : 0 / 15 ; fixture 4 / 76, 0 / 76 après neutralisation ;
  - C6 : `comparer` 0 ×16, mklepton = `env-57-debian` = `env-52-apres`.
- **PA-110** : fusions et push.
- **`HORS-PLAN.md`** :
  - D17 à D20 prouvés sur la VM ;
  - D26 à D28 ajoutés ;
  - D21 à D28 à traiter ;
  - A1 à A4, D4 et D12 reconfirmés hors plan.

## Reste à faire dans l'étape
- [x] Tout ENV-61.
- [x] Hors étape : copies d'essai du Mac `essais/env-61-*` supprimées par
  `scripts/supprimer-essai.sh` (demande de l'utilisateur). Journaux `essais/env-61-mac/`
  conservés.
- [x] Hors étape (décision de l'utilisateur du 2026-11-17) : les skills du dépôt se modifient sur
  le compte claude.ai (Claude Desktop) ; `scripts/importer-skills.sh` copie la version
  synchronisée dans `.claude/skills/`, commit dédié (CLAUDE.md, ORCHESTRATION §5bis). Branche
  `devenv/skills-compte`, fusionnée dans `main` ; les deux poussées sur accord (PA-P). Le commit
  « état et passation » qui suit le push n'est pas poussé. Pytest 527 (508 + 19 tests du script).

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Plan de session ; essai préalable `graft-update` d'`env-13-vierge` (PA-P) | utilisateur (plan approuvé) | oui |
| PA-109 : regreffes ×4 et reconstruction (C3, C6) ; fixture sur la VM (C5) ; C7 écarté ; C8 tel qu'écrit ; §0, push, ordre, regreffes du Mac pendant R61-1 | utilisateur | oui |
| Envoi de l'ordre à `debian-linux-vm` [7348f6] | utilisateur (la session n'avait pas été relancée, ACCUSÉ) | oui (journal, rapport) |
| QUESTION §6 : contrôle D17 corrigé, suite de la consigne | utilisateur | oui |
| QUESTION §11.2 : écarts de comparaison de la fixture acceptés | utilisateur (dans la session VM) | oui |
| A1 rejoué et refusé | utilisateur (dans la session VM) | oui |
| PA-110 : fusions et push | utilisateur | oui |
| Fin du plan : D26 à D28 ajoutés ; D21 à D28 à traiter ; A1 à A4, D4, D12 hors plan | utilisateur | oui |
| `fr()`, base `env-61-fixture/f56`, comptes des attendus, contrôles de la consigne | session, d'après les essais du Mac (rapport §1) | oui (rapport ; défauts en D27) |
| Hors étape : skills édités sur le compte claude.ai, importés par `scripts/importer-skills.sh` ; branche dédiée ; sans argument, skills déjà présents ; push | utilisateur (questions posées, plan approuvé) | oui |

## Pièges rencontrés
- **Skills synchronisés depuis le compte** : la copie `~/.claude/skills/synced/` se met à jour au
  démarrage d'une session Claude Code (`claude -p` lancé hors du dépôt suffit) ; une session déjà
  ouverte ne la met pas à jour (constaté le 2026-11-17 : aucun passage entre 20:26 et 20:32:59,
  téléversement fait entre les deux). Lancer `scripts/importer-skills.sh -n` avant la copie.
- **Contrôle d'une correction par un texte du code** : le §6 de la consigne cherchait
  `expanduser().resolve()`, texte de l'ancien code, alors que 74c9c97 l'écrit en deux lignes.
  Parade : vérifier le contrôle contre le code installé au Mac avant d'écrire la consigne.
- **Espace insécable** : git 2.47.3 en français écrit « fatal » + U+00A0 + « : ». Une simulation
  de la traduction écrite à la main avec une espace ordinaire passe à côté. Parade : tirer les
  traductions de `po/fr.po` octet pour octet, ou `LC_ALL=C` dans tous les outils (le fait déjà
  `essai.sh`, pas `fixture.py`).
- **Segment d'hôte** : les chemins absolus rangés sous `depots/.mirrors/localhost/…` commencent par
  `/Users` (Mac) ou `/home` (Debian) ; `<HOME>` ne couvre pas ce segment seul.
- **« Ne plus demander »** sur une commande `ask` : relevé `user_permanent`, sans règle écrite ;
  l'invite suivante paraît quand même (Claude Code 2.1.326).
- **Invites à refuser** : confirmées par erreur deux fois (A2 au Mac, premier A1 sur la VM), sans
  effet grâce aux cibles absentes (D28).
- **Session VM « relancée »** : `ListAgents` montrait la même réf. (7348f6) avant et après le §0 ;
  l'ACCUSÉ a montré qu'elle ne l'était pas. Le répertoire de travail suffit aux règles du dépôt.
- **`git merge-tree --write-tree`** permet de vérifier l'absence de conflit avant une fusion, sans
  rien écrire dans l'arbre de travail.

## Critères de validation
- [x] PA-109 et PA-110 tranchés et consignés.
- [x] `FIN-SUCCÈS R61-1` vérifié par la session Mac ; C1 à C6 conformes (écarts consignés), C7
      écarté au PA-109, C8 fait.
- [x] D19 : réglages utilisateur de la VM conformes au PA-103 ; aucune règle retirée ni
      restreinte (PA-103), donc aucun contrôle négatif ; U1 et U2 acceptés par les règles
      utilisateur, U3 non (D26).
- [x] D20 : décisions des formes de l'essai témoin, sur la VM, au rapport
      (`rapports/env-61-debian.md` §3.2).
- [x] Rootstocks d'essai regreffés : 0 lien cassé, 0 fichier régulier ; `check` code 0
      (`qemu-gra2` : 1, attendu).
- [x] Fin du plan : `HORS-PLAN.md` présenté à l'utilisateur pour décision.

## Reprise
Commande ou première action de la session suivante :
```
révision du plan avec la skill lepton-portage-instructions : planifier D21 à D28 de HORS-PLAN.md
(D21 et D23 expanduser ; D22 et D25 scion ; D24 extension --purge ; D26 à D28 Claude Code et
consignes VM) ; lire DEVENV-STATUS.md (Prochaine action) et handoff/env-61.md
```
