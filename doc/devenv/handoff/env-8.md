# Passation ENV-8 — Outil `lepton` — reprise 3 (O3, O4, O14, O17 ; O1 d'ENV-6) — session du 2026-10-16

ENV-8 est terminée depuis le 2026-10-14 (jalons 1-6, `rapports/env-8-interface.md`) ; R2 (N5)
terminée le 2026-10-16 (`rapports/env-8-r2-options.md`). Cette passation remplace celle de R2 et
porte sur la reprise 3 du bilan ENV-11 (`rapports/env-11-bilan.md` §3) : O3, O4 (ENV-8), O1
(ENV-6, lecteur CMake du noyau), O14 (joint) et O17 (relevé pendant la reprise). Rapport :
`rapports/env-8-r3.md`.

## Statut
terminée — O1, O3, O4, O14, O17 corrigés ; non-régression d'O1 validée ; fusions de
`devenv/env-8-r3` et `devenv/env-6-r3` au début de la session suivante.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `devenv/env-8-r3` (depuis `main` b9dd0e8 = fusion `--no-ff` de `devenv/env-8-r2`) | `devenv(env-8-r3): état et passation` ; avant : 9d2cc85 (O17), ef92c8d (oracle, rapport), 40ea155 (O14), 9d851b3 (O4), bfa6ec5 (O3) | oui |
| clone noyau `~/lepton/depots/lepton/original/master` | `devenv/env-6-r3` (extraite ; depuis `master` 50a67c0 = fusion `--no-ff` de `devenv/env-8-r2`) | aee4618 (O1) | oui |
| seed.scions | `master` f1d1f3c, tag 0.5.1.1 | **poussés** le 2026-10-16 (SSH, `origin` HTTPS inchangé) | oui |
| `~/lepton` trunk | — | 4 037 feuilles, aucun fichier régulier, aucun lien cassé ; sans regreffe (seul `scion/CMakeLists.txt` du clone change) | oui |

Poussés le 2026-10-16 (PA-P) : lepton-tools `main` b9dd0e8 et `devenv/env-8-r3` ; clone noyau `master` 50a67c0 et `devenv/env-6-r3` aee4618. La fusion de R3 reste locale à faire, puis à pousser sur accord. lepton
pipx = `main` b9dd0e8 (R2 compris, sans R3) ; R3 se teste par le venv
`~/lepton-tools-dev/venv-lepton-tools` (installation éditable). Rootstocks d'essai (`o14`,
`bout-en-bout`) et copie du rootstock (`copie-r3`) dans le scratchpad de session (jetables).

## Fait pendant la session
- Fusions locales `--no-ff` de `devenv/env-8-r2` : lepton-tools `main` b9dd0e8, clone noyau
  `master` 50a67c0 (extrait, trunk contrôlé) ; `pipx install --force` de lepton depuis `main`.
- O3 (bfa6ec5) : `_left_state` (`lepton/scions.py`) décrit l'état laissé après un échec de
  `scion new` d'après le disque ; 3 tests.
- O4 (9d851b3) : `removal_unprovided` (`lepton/checks.py`) ; avertissement CFG-5 dans
  `seed_remove` (`seed remove`, `scion remove`) ; 2 tests.
- O14 (40ea155) : `_ORIGIN` (`lepton/seed.py`) admet `/` dans VERSION, autorité d'URL dans
  LOCATION, segments vides / `.` / `..` refusés ; scion 0.5.1.1 inchangé (vérifié) ; 2 tests ;
  essai réel `seed new` avec noyau `@devenv/env-6-r3`.
- O1 (clone noyau aee4618) : `FATAL_ERROR` explicite si `LEPTON_BOARD` n'est ni un BSP greffé ni
  un module `cmake/boards` ; essai (`oracles/env-8-r3-apres/essai-o1.log`).
- Oracle `oracles/env-8-r3-apres/` (15 presets) contre `env-8-r2-apres-final/` : sections et
  symboles identiques, banc KAL, mklepton, ctest identiques ; E1 démontré
  (`REVS="50a67c0 aee4618" env-8-r2-preuve-empreintes.sh`) ; fumée E2.
- O17 (9d2cc85) : colonnes version et branche de `seed status` à la largeur du contenu ; 1 test.
- PA-P : push de seed.scions `master` + tag 0.5.1.1.
- `pytest` 132 verts ; `scripts/valider-schemas.sh` conforme ; `scripts/bout-en-bout.sh` (lepton
  de la branche) succès, `~/lepton` inchangé. Bilan ENV-11 §3 et `env-8-r2-options.md` (O14)
  mis à jour.

## Reste à faire
- [ ] Fusion `--no-ff` : lepton-tools `devenv/env-8-r3` → `main` ; clone noyau `devenv/env-6-r3`
  → `master` (puis `master` extraite dans `~/lepton`, contrôle du trunk, sans regreffe).
- [ ] `pipx install --force <LEPTON_TOOLS>` depuis `main`.
- [ ] Reprise 4 : ENV-9 N4, O8, O10, O11 ; puis reprise 5 (ENV-10 D3, D4, O6, O12 + noyau O9, un
  passage VM) ; puis PA-12.
- [ ] Push des fusions de R3 (`main`, `master`) : à proposer (PA-P), au plus tard avant le passage VM de la reprise 5.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Reprise 3 = O3, O4, O14 + O1 ; branches `devenv/env-8-r3`, `devenv/env-6-r3` | utilisateur | oui |
| O4 : avertir et continuer (code 0) | utilisateur | oui |
| Non-régression O1 sur `env-8-r2-apres-final` ; validée | utilisateur | oui |
| PA-P : push de seed.scions `master` + tag 0.5.1.1 ; puis lepton-tools (`main`, `devenv/env-8-r3`) et clone noyau (`master`, `devenv/env-6-r3`) | utilisateur | oui |
| O17 corrigé dans R3 | utilisateur | oui |
| O14 sans évolution de scion (vérification de 0.5.1.1) | constat, présenté au plan comme condition | oui |
| O3 : cas « ajout fait, échec ensuite » → « corriger la cause, puis lepton graft » | proposition appliquée | non (rapport §2) |
| O4 : avertissement émis avant la reconfiguration CMake (visible même si CMake échoue) ; anomalies CFG-5 antérieures non répétées | proposition appliquée | non (rapport §2) |
| Minimums des colonnes de `seed status` conservés (8, 16) | proposition appliquée | non (rapport §5) |

## Pièges rencontrés
- Élargir seulement la classe de VERSION de `_ORIGIN` aurait cassé `https://user@hôte/x.git`
  (lu comme version `hôte/x.git`) : autorité d'URL isolée dans l'expression.
- Après `seed-clone`, le greffon figure déjà dans la liste greffée : un échec d'`_expect` laisse
  « déclaré et greffé » si l'annulation échoue (test ajusté sur l'état réel).
- `lepton seed new` n'a pas d'option `--no-cmake`.
- Comparaison de `fumee.log` : le dernier chiffre du jeton UART peut être renvoyé devant l'invite
  suivante (`8lepton#2$`) ; à ignorer avec les lignes vides (E2).
- Empreintes de la preuve E1 propres à chaque copie (chemins de débogage) : ne comparer que dans
  une même copie.

## Critères de validation (appliqués à R3)
- [x] O1 : message explicite, première erreur de la configuration CMake.
- [x] O3, O4, O14, O17 : tests dédiés verts ; `pytest` 132 verts.
- [x] Non-régression du `CMakeLists.txt` du noyau (oracle 15 presets) validée par l'utilisateur.
- [x] Bout en bout vert ; rootstock de référence inchangé.

## Reprise
```
cd /Users/cle_d_anton/lepton-tools-dev/lepton-tools && claude
# « Démarre la session sur l'étape indiquée dans DEVENV-STATUS » (fusions de la reprise 3, puis reprise 4)
```
