# Passation ENV-8 — Outil `lepton` — reprise R2 (N5) — session du 2026-10-16

ENV-8 elle-même est terminée depuis le 2026-10-14 (jalons 1-6, `rapports/env-8-interface.md`).
Cette passation remplace la précédente et porte sur la reprise R2 : défaut N5 du bilan ENV-11
(`rapports/env-11-bilan.md` §3, CFG-4), et les observations O15 et O16 relevées pendant la reprise.
Rapport : `rapports/env-8-r2-options.md`.

## Statut
terminée — valeurs d'options fixables dans la graine, contrôlées par lepton et CMake ; CFG-4
conforme ; non-régression validée ; fusions de `devenv/env-8-r2` au début de la session suivante.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `devenv/env-8-r2` (depuis `main` 4ac04bd = fusion `--no-ff` de `devenv/env-7-r1`) | `devenv(env-8-r2): état et passation` ; avant : e7d695b (O16), 33d140a (rapport), b77665d (oracle avant), 843f0fb (lepton), 86732eb (schéma) | oui |
| clone noyau `~/lepton/depots/lepton/original/master` | `devenv/env-8-r2` (extraite ; depuis `master` 66676b6 = fusion `--no-ff` de `devenv/env-7-r1`) | 53ceb58 (O15, O16) ; avant : 82a6700 (lecteur, N5) | oui |
| seed.scions | `master` f1d1f3c, tag 0.5.1.1 | non touché ; non poussé (PA-P refusé pour l'instant) | oui |
| `~/lepton` trunk | — | 4 037 feuilles, aucun fichier régulier, aucun lien cassé, sans regreffe (seul `scion/cmake/lepton_greffons.cmake` du clone change) | oui |

Aucun push. lepton pipx = `main` 4ac04bd (sans R2) ; la branche se teste par le venv
`~/lepton-tools-dev/venv-lepton-tools` (installation éditable). Rootstocks d'essai, copie du
rootstock et mini-projet CMake dans le scratchpad de session (jetables).

## Fait pendant la session
- Fusions locales `--no-ff` de `devenv/env-7-r1` : lepton-tools `main` 4ac04bd, clone noyau `master`
  66676b6 (extrait, trunk contrôlé) ; `pipx install --force` de lepton depuis `main` (requis ≥ 0.5.1.1).
- PA-P : push de seed.scions 0.5.1.1 proposé, refusé pour l'instant.
- PA-3 R2 : `schemas/graine.schema.json` champ `options` ; exemple et 4 invalides ; CFG-4 amendée
  (86732eb) ; `scripts/valider-schemas.sh` conforme.
- lepton (843f0fb) : `check_seed_options` (`lepton/checks.py`), `option_cache` et refus dans
  `Context` (`lepton/generate.py`) ; tests.
- Oracle avant (b77665d, validé), lecteur CMake (82a6700), oracle après ; O15, O16 (53ceb58,
  e7d695b) ; oracle final `oracles/env-8-r2-apres-final/` : sections/symboles identiques
  (14 presets), banc KAL, mklepton, ctest identiques ; E1 démontré (`env-8-r2-preuve-empreintes.sh`).
- Essai fonctionnel `rapports/env-8-r2-essai.sh` (journal dans `oracles/env-8-r2-apres-final/`) :
  conforme (portées, chaîne échappée vérifiée au préprocesseur, refus par check / generate / CMake).
- `pytest` 125 verts ; `scripts/bout-en-bout.sh` (lepton de la branche) succès, `~/lepton` inchangé.

## Reste à faire
- [ ] Fusion `--no-ff` de `devenv/env-8-r2` : lepton-tools → `main` ; clone noyau → `master` (puis
  `master` extraite dans `~/lepton`, contrôle du trunk).
- [ ] `pipx install --force <LEPTON_TOOLS>` depuis `main` (schéma de graine à jour).
- [ ] Reprise 3 : ENV-8 O3, O4 + ENV-6 O1 ; proposer d'y joindre O14 (renvoyé ENV-8 avec ENV-7).
- [ ] PA-P à reproposer : seed.scions `master` + tag 0.5.1.1 (et lepton-tools, clone noyau).

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| N5 : forme par greffon, projet seulement, transport par presets, branche `devenv/env-8-r2` | utilisateur | oui |
| PA-P : aucun push | utilisateur | oui |
| PA-3 R2 : schéma, exemples, amendement CFG-4 | utilisateur | oui |
| Oracle avant validé ; non-régression validée | utilisateur | oui |
| O14 renvoyé ENV-8 / ENV-7 | utilisateur | oui |
| O15 corrigé (libellé) ; O16 : échapper `"` `\`, refuser `;` `#` saut de ligne | utilisateur | oui |
| Variable `LEPTON_OPTION_*` sans option : avertissement CMake, pas erreur (cache non vidé au retrait) | proposition appliquée (présentée avant application du lecteur) | non (détail du rapport §2) |
| Oracle refait sur l'état final (`env-8-r2-apres-final`) après O15/O16 | proposition appliquée | non (rapport §3) |

## Pièges rencontrés
- `--origin …@devenv/env-8-r2` : version à `/` refusée par lepton (O14) → clone du noyau dans le
  scratchpad sur une branche `essai-r2`.
- Essai lancé avec le lepton de pipx (`main`) : « champ non autorisé : options » → `PATH` du venv
  en tête dans le script d'essai.
- Empreintes de l'oracle toujours différentes sans `SOURCE_DATE_EPOCH` (date embarquée) : comparer
  sections et symboles, prouver l'identité binaire à `SOURCE_DATE_EPOCH` égal sur une copie.
- Patch Python contenant des échappements bash/JSON/C imbriqués : fragile ; éditer le fichier
  directement.
- `#` dans une définition : CMake la retire avec un simple avertissement ; `;` coupe la valeur.

## Critères de validation (appliqués à R2)
- [x] CFG-4 : valeur hors bornes refusée (`lepton check`, `lepton generate`, configuration CMake).
- [x] Tests pytest verts (125) ; schémas conformes.
- [x] Non-régression du lecteur CMake (oracle 15 presets) validée par l'utilisateur.
- [x] Bout en bout vert ; rootstock de référence inchangé.

## Reprise
```
cd /Users/cle_d_anton/lepton-tools-dev/lepton-tools && claude
# « Démarre la session sur l'étape indiquée dans DEVENV-STATUS » (fusions de devenv/env-8-r2, puis reprise 3)
```
