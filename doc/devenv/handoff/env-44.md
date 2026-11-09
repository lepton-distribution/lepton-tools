# Passation ENV-44 — Résidus d'ENV-37 à ENV-43 — session du 2026-11-09 (préparation)

## Statut
à démarrer — session hors étape : révision du plan après ENV-43 (skill
`lepton-portage-instructions`). Les étapes ENV-44 à ENV-50 sont rédigées, aucune tâche d'ENV-44
n'est exécutée. Aucun fichier de l'arbre Lepton n'est touché, aucune branche `devenv/env-44`
n'existe. La session qui exécutera ENV-44 remplacera cette passation.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` | commit « devenv: révision du plan, étapes ENV-44 à ENV-50 … » sur ce19043 (fusion de `devenv/env-43`) ; non poussé (`origin/main` à ce19043) | oui |
| clone noyau `depots/lepton/original/master` | `master` | 763dda2, non touché | oui |
| familles, BSP, graine, seed.scions | — | non touchés : F4 7afd7f1, F7 d2d9aa9, WL 2340b25, an386 5819047, graine 15740f9, seed.scions `master` f29fa35 (tag 0.6.1.0) | oui |

`<ROOTSTOCK>` : 3982 liens (valeur de la passation ENV-43, non recomptée). Outils : lepton 0.1.0,
scion 0.6.1.0.

Carte NUCLEO-F429ZI : encore sur la VM. WL55 A et B : sur le Mac.

## Fait pendant la session
- Début de session : état des dépôts conforme à `handoff/env-43.md` (`git status`, branches,
  têtes).
- `HORS-PLAN.md` présenté en entier, avec une recommandation par point. Les choix de l'utilisateur
  sont consignés : `DEVENV-STATUS.md` §Décisions, ligne « révision du plan, ENV-44 à ENV-50 ».
- Relevés en lecture seule, repris dans les fichiers d'étapes :
  - cas F7 et WL de `rapports/env-38-projection.md` §2.2 et §2.3 ;
  - F7 `hal_driver/` : 197 fichiers ;
  - `driverlib/` : 68 fichiers ;
  - lecteur `openocd` de `cmake/lepton_greffons.cmake` ;
  - presets visibles du trunk (2 WL55, 4 an386) ;
  - tags amont WL par `git ls-remote`.
- Fichiers d'étapes `etapes/ENV-44-residus.md` à `ENV-50-validation-debian.md`, de 109 à 153 lignes.
- ORCHESTRATION §2, §4 (PA-75 à PA-88), §5bis, §6.
- `DEVENV-STATUS.md` : étapes, décision, journal, prochaine action.
- `HORS-PLAN.md` : colonne « Suite ».
- Contrôle : chaque PA de PA-75 à PA-88 est défini une fois au §4 et cité dans le fichier de son
  étape.
- Relecture par un agent indépendant, à la demande de l'utilisateur : 2 constats bloquants, 11 à
  corriger, 9 suggestions. Les principaux ont été vérifiés par la session (`lepton/seed.py:575`, 658,
  823 ; `rapports/env-41-f4-projection.md` §3.5 ; `rapports/env-40-miroir.md` E13 ; historique de
  `driverlib/` ; sous-modules de STM32CubeWL `v1.6.0`). Tous sont appliqués, sauf un : l'appel de
  l'API SPL par `dev_stm32f4xx_dac_x.c` n'a pas été confirmé (`HAL_DAC_Init`), et le classement est
  laissé à l'audit d'ENV-46.

## Reste à faire dans l'étape
- [ ] Tout ENV-44 (§1 à §4) : rien n'est commencé.
- [ ] Relire les sept fichiers d'étapes : c'est un premier jet (voir les propositions non validées
      ci-dessous).

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| A1 à A4 et D4 restent hors plan ; B1 à B4, D1 à D3, D5 à D9 retenus ; C1 documenté en l'état ; C2 renvoyé à la projection du WL | utilisateur | oui |
| B3 retenu malgré A3 hors plan : sort des dépendants tranché au PA-79 | utilisateur (tension relevée par la session) | oui |
| Découpage ENV-44 à ENV-50 et ordre ; commit direct sur `main` | utilisateur (plan approuvé) | oui |
| ENV-44 : D2 peut être clos sans objet si aucun binaire de construction du trunk ne porte de chemin `depots/tiers` | proposition non validée | non |
| ENV-45 : deux formes à comparer, par BSP (copie du WL55) ou générique dans le lecteur du noyau ; `adapter serial` d'EDBG à vérifier sur la carte | proposition non validée | non |
| ENV-46 : `eth.c` et `dev_stm32f4xx_eth.c` proposés dans le périmètre du retrait ; contrôle par les fichiers `.d` | proposition non validée | non |
| ENV-47 et ENV-48 : banc de carte (F746, WL55) comme contrôle de non-régression d'une bascule iso-fonctionnelle | proposition non validée | non |
| ENV-48 : essai à blanc des fonctions de scion propres au cas WL avant toute décision de correctif | proposition non validée | non |
| ENV-49 : banc WL55 lancé deux fois ; périmètre HAL seule ou ensemble des composants de STM32CubeWL au PA-85 | proposition non validée | non |
| `HORS-PLAN.md` : point traité marqué avec renvoi au rapport, pas retiré | utilisateur | oui |
| Corrections de relecture intégrées aux deux commits de la révision (réécriture locale, rien de poussé) | utilisateur | oui |
| ENV-44 : tests du hook dans les deux sens (écriture refusée, lecture acceptée), emplacement à fixer au PA-75 | proposition non validée | non |
| ENV-44 et ENV-48 : un correctif de scion de préférence dans une étape scion insérée, l'essai ou la bascule suspendus | proposition non validée | non |
| ENV-46 : archive ou tag de l'historique de la SPL avant suppression, au PA-79 | proposition non validée | non |
| ENV-47 et ENV-48 : première synchronisation des miroirs par la graine de publication d'ENV-40 (`--seed`) | proposition non validée (méthode d'ENV-40 E13) | non |
| ENV-48 : faisabilité d'un miroir de STM32CubeWL (taille, sous-modules) relevée, sans choix, avant le PA-83 | proposition non validée | non |

## Pièges rencontrés
- Le WL55 n'a que 2 presets (`nucleo-wl55jc1-embos`, `-freertos`), pas 4 : relevé dans
  `CMakePresets.json` du trunk.
- Regreffe d'un rootstock dont un clone est sur une branche d'étape : `seed-clone` + `graft`, jamais
  `graft-update` (refus hors version déclarée) ; erreur du premier jet, relevée à la relecture.
- `lepton seed replace`, `seed remove`, `seed lock` refusés sur la graine de référence : tout essai
  de commande de graine se fait sur un rootstock à graine de projet.
- La skill `lepton-portage-instructions` est écrite pour `doc/migration/` (ETAPE-N, README). Ce
  chantier utilise `doc/devenv/` (ENV-N, ORCHESTRATION §6, DEVENV-STATUS) : le gabarit est repris
  d'ENV-41 et d'ENV-43.

## Critères de validation
- [ ] PA-75 et PA-76 tranchés et consignés.
- [ ] Chaque point D1, D2, D3, D5, D6, D7, D9 corrigé, essayé ou clos, avec sa preuve au rapport.
- [ ] Binaires : code 0 hors an386 ; an386 dans le critère du PA-75.
- [ ] `HORS-PLAN.md` : chaque point traité marqué, avec renvoi au rapport.

## Reprise
Commande ou première action de la session suivante :
```
démarre la session ENV-44 (skill devenv-session) ; avant D2, rattacher la NUCLEO-F429ZI au Mac
```
