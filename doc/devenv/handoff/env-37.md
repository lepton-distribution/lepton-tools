# Passation ENV-37 — Famille STM32WL : audit et provenance du code tiers — session du 2026-11-05 (préparation)

## Statut
à démarrer — session hors étape : révision du plan après ENV-36 (skill
`lepton-portage-instructions`). Étapes ENV-37 à ENV-43 rédigées. Aucune tâche d'ENV-37 exécutée,
aucun fichier de l'arbre Lepton touché, aucune branche `devenv/env-37`. Cette passation sera
remplacée par celle de la session qui exécutera ENV-37.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` | 98d8063 « devenv: révision du plan, étapes ENV-37 à ENV-43 … », puis 30d9536 (cette passation) ; poussés le 2026-11-05 (PA-P), ainsi que le commit de consignation du push | oui |
| clone noyau `depots/lepton/original/master` | `master` | 2893297 (non touché) | oui |
| famille `depots/lepton/family-stm32wlxx/master` | `master` | dbc58d7 « Fusion de devenv/env-26 … » (non touché) | oui |
| famille F4, BSP F429 et F439, BSP WL55, graine, seed.scions | — | non touchés (0fd8b2a, b9fe2bf, 314f91b, ef51ec1, 15740f9, 1173d6d et tag `0.5.4.0`) | oui |

`<ROOTSTOCK>` : non regreffé, 3978 liens (valeur de la passation ENV-36, non recomptée).

## Fait pendant la session
- Début de session : état des dépôts conforme à `handoff/env-36.md` (`git status`, branches,
  têtes) ; `lepton --version` : lepton 0.1.0, scion 0.5.4.0.
- Sujets en attente présentés avec recommandation ; choix de l'utilisateur consignés
  (`DEVENV-STATUS.md` §Décisions, ligne « révision du plan, ENV-37 à ENV-43 »).
- Relevé en lecture seule de la famille WL, repris dans `etapes/ENV-37-wl-provenance.md`
  §Prérequis : HAL `__STM32WLxx_HAL_VERSION` 1.3.0, 157 fichiers ; CMSIS device 1.1.1, 5 fichiers ;
  `radio_subghz_phy/` 24 ; `Utilities/` 39 ; aucun `LEPTON-PROVENANCE.md` ; 0 CRLF ; 21 `sources`
  au manifeste ; tags amont par `git ls-remote --tags` (HAL `v1.0.0` à `v1.6.0`, CMSIS device
  `v1.0.0` à `v1.4.0`, STM32CubeWL `v1.0.0` à `v1.6.0`).
- Fichiers d'étapes ENV-37 à ENV-43 ; ORCHESTRATION §2, §4 (PA-61 à PA-74), §5bis, §6 ;
  `DEVENV-STATUS.md` (étapes, décision, journal, prochaine action). Commit 98d8063 sur `main`.
- Contrôle : chaque PA-61 à PA-74 figure une fois au §4 et dans le fichier de son étape ; fichiers
  d'étapes de 101 à 147 lignes.

## Reste à faire dans l'étape
- [ ] Tout ENV-37 (§1 à §4) : rien n'est commencé.
- [ ] Relire les sept fichiers d'étapes : c'est un premier jet (voir les propositions non validées
      ci-dessous).

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Retenus : projection scion et miroir ; sort de `core_cm4.h` | utilisateur | oui |
| WL : audit et provenance avant la conception de la projection, sans recopie | utilisateur | oui |
| Bascule sur la projection : F4 seul, en pilote ; F7 et WL à la révision suivante | utilisateur | oui |
| Non retenus : SPL de `driverlib/` ; montée de version de la HAL WL | utilisateur | oui |
| Découpage ENV-37 à ENV-43, conception séparée (ENV-38), contrôle de la vue des périphériques F429 rattaché à ENV-42, commit direct sur `main` | utilisateur (plan approuvé) | oui |
| ENV-37 : comparaison des répertoires renommés sur une copie de travail remise à la casse amont ; relevé de la sensibilité à la casse du volume ; section « Cas d'épreuve pour ENV-38 » | proposition non validée | non |
| ENV-38 : question « dépendance d'un greffon envers une projection » (graines de projet, `lepton seed new`) ajoutée au PA-63 | proposition non validée | non |
| ENV-39 : essai à blanc de la projection F4 sur une copie d'essai ; candidats de version `0.5.5.0` ou `0.6.0.0` | proposition non validée | non |
| ENV-40 : cas de test « historique réécrit » et « tag supprimé » ; essai sur miroirs nus locaux avant toute création sur GitHub | proposition non validée | non |
| ENV-41 : rootstock neuf `essais/env-41-vierge` ; ordre de publication graine / famille posé au PA-70 | proposition non validée | non |
| ENV-42 : trois options du PA-71 ; mode opératoire du contrôle de la vue des périphériques | proposition non validée | non |
| ENV-43 : critère C6 (commande de miroir en lecture seule) ; « Prochaine action » finale | proposition non validée | non |
| ORCHESTRATION §5bis : étapes attribuées à chaque skill | proposition non validée | non |

## Pièges rencontrés
- `git ls-remote --tags` filtré sans les lignes `^{}` rend l'objet tag d'un tag annoté : les
  hachages relevés pendant la session ne sont pas des commits et ne sont cités dans aucun fichier.
  ENV-37 §1 résout chaque tag par `git rev-parse <tag>^{commit}`.
- Les trois fichiers « à marque Lepton » du WL viennent d'un `grep` : ce n'est pas une preuve de
  modification, ni une liste complète. ENV-37 §1 compare à l'amont.
- L'amont de `radio_subghz_phy/` et de `Utilities/` n'a pas été cherché : il peut n'exister que
  dans STM32CubeWL, ce que la décision du 2026-11-04 exclut comme source. Question du PA-61.
- Les 159 tests de scion viennent de `grep -c 'def test_'`, pas de `pytest`.
- La skill `lepton-portage-instructions` synchronisée ne contient que `SKILL.md` :
  `references/archetypes-portage.md` est absent. Gabarit repris d'ENV-29, ENV-34 et ENV-36.
- zsh : `echo =====` échoue ; utiliser `echo '---'`.

## Critères de validation
- [ ] PA-61 et PA-62 tranchés et consignés.
- [ ] Binaires identiques sur host et les 16 presets (code 0).
- [ ] Chaque fichier des quatre ensembles est classé dans le rapport ; chaque `DIFF` est qualifié.
- [ ] Chaque ensemble tiers de la famille a sa provenance, ou la raison de son absence est
      consignée au PA-61.
- [ ] Le rapport contient la section « Cas d'épreuve pour ENV-38 ».

## Reprise
Commande ou première action de la session suivante :
```
démarre la session   # ENV-37 : lire cette passation, etapes/ENV-37-wl-provenance.md, audit §1 jusqu'au PA-61
```
