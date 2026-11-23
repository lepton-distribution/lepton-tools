# Passation de préparation ENV-67 — révision du plan du 2026-11-23

## Statut
ENV-67 n'est pas commencée. Ce fichier est la passation de la session de révision du plan
(hors étape), écrite pour la session qui démarrera ENV-67 ; il sera remplacé par la passation de
cette étape.

La présentation de `HORS-PLAN.md` a été achevée (fin du plan, après ENV-66), puis le plan a été
révisé : ENV-67 à ENV-72, PA-121 à PA-132.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `devenv/revision-2026-11-23` (depuis `main` 172fb67) | commit de la révision du plan | oui |
| clone noyau `depots/lepton/original/master` | `master` | 2b4a647, non touché | oui |
| autres | seed.scions `master` 49ca4ae (tag 0.6.3.3), graine `original-tree` 15740f9 | non touchés | oui |

Fusion de `devenv/revision-2026-11-23` dans `main` et push : sur accord de l'utilisateur (PA-P).
Relevez l'état réel de `main` au début d'ENV-67.

Outils (inchangés depuis ENV-66) :
- Mac et VM : scion 0.6.3.3, lepton 0.1.0, extension 0.5.3, Claude Code 2.1.328 ;
- git : 2.50.1 au Mac, 2.47.3 sur la VM ;
- VM : `~/.claude/settings.json` à 2 règles `allow` ; `essais/` réduit à `env-13-debian`,
  `env-28-debian`, `env-53-c5`, `env-53-debian` ; `~/tmp-pytest` vide.

## Fait pendant la session
- Décisions sur `HORS-PLAN.md` (questions posées ; consignées dans `DEVENV-STATUS.md`
  §Décisions, 2026-11-23).
- Étapes `etapes/ENV-67-…` à `ENV-72-…` ; ORCHESTRATION :
  - §2 : seed.scions, VM ;
  - §2bis : « Invites simultanées », D39 ;
  - §4 : PA-121 à PA-132 ;
  - §5bis et §6.
- `HORS-PLAN.md` mis à jour.
- Relecture par un agent indépendant : voir le journal de `DEVENV-STATUS.md` (2026-11-23).

## Reste à faire
- ENV-67 à ENV-72, dans l'ordre 67, puis 68 à 71 (permutables), puis 72.
- Tickets des montées de version de D40, sur `family-stm32f7xx` (HAL v1.3.4, CMSIS device
  v1.2.11) et `family-stm32f4xx` (CMSIS device v2.6.12). Décision de l'utilisateur : la session
  de révision les crée après relance avec le plugin `lepton-tickets`. S'ils ne le sont pas (ligne
  D40 de `HORS-PLAN.md`), ils sont créés avant ENV-71, par une session lancée avec
  `claude --plugin-dir ~/lepton-tools-dev/plugins/lepton-tickets` (skill `lepton-ticket-creer`,
  mode « depuis un chantier », texte soumis à l'accord).

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| A1, A2, A4, D4, D12 reconfirmés hors plan | utilisateur | oui |
| D29, D30, D32, D37 en une étape lepton (ENV-68) | utilisateur | oui |
| D35, D33 en un tag de scion 0.6.3.4 (ENV-70) | utilisateur | oui |
| D36, extension 0.5.4 (ENV-69) | utilisateur | oui |
| D38 (1) à (3) traités (ENV-67), (4) hors plan | utilisateur | oui |
| D39 : parade écrite au §2bis à la révision | utilisateur (texte de la session, relu) | oui |
| D40 : `mirror-sync` en étape (ENV-71), montées de version en tickets | utilisateur | oui |
| Tickets D40 créés par la session de révision relancée avec le plugin | utilisateur | oui |
| Relecture indépendante : les 22 constats appliqués ; ENV-71 : lieu des dépôts de travail au PA-129, envoi par l'utilisateur seul | utilisateur | oui |
| Découpage ENV-67 à ENV-72, ordre, PA-121 à PA-132 | utilisateur (plan de session approuvé) | oui |
| Options écrites dans les fichiers d'étape et `<À CONFIRMER>` (PA-121, PA-123, PA-125, PA-127, PA-129, PA-131) | proposition non validée, à trancher à chaque point d'arrêt | non (fichiers d'étape) |

## Pièges rencontrés
- Le plugin `lepton-tickets` n'était pas chargé dans la session de révision : la skill
  `lepton-ticket-creer` était absente.
- D35 ne se reproduit pas au Mac (git 2.50.1 n'écrit pas l'avertissement) : test par stderr
  simulé en ENV-70, preuve réelle sur la VM en ENV-72.
- `scion mirror-sync` n'est couvert par aucune règle de `.claude/settings.json`. L'envoi est fait
  par l'utilisateur. Même `--dry-run` clone les 8 dépôts de travail absents (`mirror.py:270-273`) :
  le lieu est tranché au PA-129.
- `~/tmp-pytest` n'existe pas au Mac (ENV-67).

## Critères de validation
- [x] Chaque point retenu de `HORS-PLAN.md` est planifié ou consigné (D39 écrit, tickets de D40).
- [x] PA-121 à PA-132 présents au §4 et dans les fichiers d'étape.
- [ ] Fusion et push de la révision (PA-P).

Tickets créés pendant la session : voir la ligne D40 de `HORS-PLAN.md` (à défaut, à créer avant
ENV-71). Lignes restées « ticket à créer après publication d'ENV-N » : aucune.

## Reprise
```
démarre la session ENV-67 (lire handoff/env-67.md, passation de préparation)
```
