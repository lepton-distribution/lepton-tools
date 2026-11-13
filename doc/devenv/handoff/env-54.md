# Passation ENV-54 — Claude Code : règles de permission ciblées (D16) — session du 2026-11-13

## Statut
Terminée (2026-11-13). Rejeu après redémarrage fait, écart N5 corrigé et rejoué ; PA-95 et PA-96
tranchés ; branche fusionnée dans `main` et poussée (PA-P).

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `devenv/env-54` (depuis `main` 4bed93c), fusionnée `--no-ff` dans `main`, les deux poussées | commit « état et passation » au-dessus de 053fa2e (rapport §10) et c9d5637 (correction de l'`ask` de `git push`) | oui |
| seed.scions | `master` | 6416c33 (0.6.3.0), non touché | oui |
| clone noyau `depots/lepton/original/master` | `master` | 58e421e, non touché | oui |
| autres | — | non touchés | — |

Outils : scion 0.6.3.0 ; lepton 0.1.0 (réinstallé en R4 depuis `devenv/env-54`, code de lepton
identique à `main`) ; Claude Code 2.1.323, mode auto.

Hors dépôt : `~/lepton-tools-dev/essais/env-54-essai/` supprimé (PA-96, par l'enveloppe).

## Fait pendant la session
- Session 1 (avant redémarrage) : audit, essai témoin, PA-95, mise en place (rapport §1 à §9).
- Session 2 (cette session, journal `40ad5fdf-53aa-4252-854a-ec885c6cebb9.jsonl`) :
  - début conforme à la passation intermédiaire (8b8c629, propre) ; plan de reprise approuvé ;
  - rejeu R1 à R5, N1 à N7 (rapport §10, `rapports/env-54-permissions/rejeu/decisions.tsv`) :
    - R1 `scion graft-update -v <copie>` → invite confirmée, 3059 liens identiques ;
    - R2 à R5 → règles, sans classifieur ; pytest 436 verts ;
    - N1, N2 code 2 de l'enveloppe ; N3 classifieur ; N4 invite refusée ; N6 `deny` ; N7 hook ;
  - écart N5 : `Bash(git * push:*)` ne couvrait pas `git -C <chemin> push` (classifieur,
    accepté, cible absente). Essais Ea à Ec, puis correction `Bash(git * push)` et
    `Bash(git * push *)` (c9d5637) ; N5-bis et Ea-bis : invites refusées ;
  - PA-96 : `deny` de `git clone` confirmés ; essai supprimé ; push et fusion ;
  - `HORS-PLAN.md` : D16 traité.

## Reste à faire dans l'étape
- Rien. La preuve sur la VM est faite en ENV-57 (PA-101 : pose du fichier, relance de la session).

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Plan de reprise ; forme positionnelle de R1 et N4 | utilisateur (plan approuvé) | oui |
| Écart N5 : tester sur cibles absentes, puis corriger | utilisateur | oui |
| Forme de la correction (`git * push`, `git * push *`) | session, d'après les essais (rapport §10.1) | oui |
| PA-96 : 5 `deny` de `git clone` confirmés ; essai supprimé ; push et fusion | utilisateur | oui |

## Pièges rencontrés
- Un motif qui combine un `*` intérieur et le `:*` final (`Bash(git * push:*)`) ne correspond à
  rien ; les jokers purs (`git * push *`) et le `:*` final simple fonctionnent. Vérifier chaque
  motif par un essai sur cible absente, jamais par la seule lecture.
- Une règle `ask` vaut aussi pour `-h` et dans une commande composée : ne pas glisser
  `scion graft-update -h` (ou `git push --help`) dans une lecture groupée.
- Le refus d'une invite interrompt le tour : l'utilisateur relance la session. À prévoir dans la
  consigne VM d'ENV-57 (contrôles négatifs).
- Le journal de session ne porte pas de `permissionDecision` pour une invite refusée :
  `toolUseResult: "User rejected tool use"`.
- Tri des listes de liens : comparer sous `LC_ALL=C sort` (l'ordre dépend de la locale).
- Les heures du `.jsonl` sont en UTC.

## Critères de validation
- [x] PA-95 et PA-96 tranchés et consignés.
- [x] Inventaire des refus, des acceptations et des formes de commandes au rapport.
- [x] Mécanisme établi, avec sa source (page de documentation, essai).
- [x] Essai témoin rejoué après redémarrage : chaque commande retenue est acceptée, chaque
      contrôle négatif est refusé ou soumis à confirmation (après correction de N5). Le journal
      de session est cité.
- [x] Le hook refuse toujours une écriture sous un `trunk/` ; `settings.json` est du JSON valide.
- [x] `pytest` complet vert (436) ; hook inchangé.
- [x] ORCHESTRATION §2bis amendé.
- [x] `HORS-PLAN.md` : D16 marqué traité, avec renvoi au rapport.

## Reprise
Commande ou première action de la session suivante :
```
démarrer ENV-55 (skill devenv-session) : lire DEVENV-STATUS.md (Prochaine action), cette passation
et doc/devenv/etapes/ENV-55-*.md ; branche devenv/env-55 depuis main
```
