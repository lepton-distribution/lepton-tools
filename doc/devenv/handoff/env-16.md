# Passation ENV-16 — Graine de référence et `lepton check` — session du 2026-10-31

## Statut
terminée — `lepton check` reconnaît une graine de référence (ni `lepton-graine.json` ni
`project/`) et la contrôle à partir des greffons greffés et des presets du noyau ; code 0 sur
`<ROOTSTOCK>` ; graines de projet inchangées.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` (fusion `--no-ff` de `devenv/env-16`, poussées toutes deux) | commit d'état et passation, puis « Fusion de devenv/env-16 » | oui |
| graine `depots/lepton-seed.scions/original-tree` | `original-tree` 0f1275a, inchangée (option C) | | oui |
| clone noyau et 7 greffons famille/BSP | `master`, inchangés | | oui |
| `<ROOTSTOCK>` trunk | non regreffé, inchangé | | oui |

## Fait pendant la session
- Tâche 1 : audit (`rapports/env-16-graine.md` §1) : contrôle actuel, lecteurs du manifeste,
  inventaire d'`original-tree`, mesure en lecture seule (GRF-5 et CFG-5 : 0 anomalie), relevé de
  référence de `check` et `seed status` sur `<ROOTSTOCK>` et 7 rootstocks d'essai ; PA-19.
- Tâche 2 : lepton-tools d7b814c (`checks.py` : `check_bsp`, `_xml_anomalies`, `kernel_presets`,
  `check_reference_seed` ; `cli.py` : `lepton: information:`), a0e58cb (4 tests), 6a40859
  (interface §3.9) ; `pytest` 202 verts ; `scripts/valider-schemas.sh` conforme ; `pipx install
  --force` (Mac).
- Tâche 3 : `check` 1 → 0 sur `<ROOTSTOCK>` et `essais/env-13-vierge` ; les autres rootstocks
  d'essai et tous les `seed status` sont identiques à l'octet près au relevé (§3) ; PA-20.

## Reste à faire dans l'étape
- Aucune tâche du fichier d'étape.
- Hors étape, non demandé :
  - `seed status` affiche toujours « graine hors lepton » sur `<ROOTSTOCK>` ;
  - `generate`, `seed config`, `seed add/remove` refusent toujours une graine sans manifeste ;
  - lepton n'est pas réinstallé sur la VM Debian depuis `devenv/env-16` (aucune validation Debian
    prévue) ;
  - l'extension n'a pas été relancée : les formes JSON qu'elle lit n'ont pas changé.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-19 : option C (graine de référence reconnue sans manifeste, critère « ni `lepton-graine.json` ni `project/` », contrôles déduits des greffons) ; presets à BSP non greffé : information | utilisateur | oui |
| PA-20 : état et passation commités, fusion dans `main`, push de `main` et `devenv/env-16` | utilisateur | oui |
| CFG-5 d'un XML de référence limité aux greffons hors BSP et famille, plus les BSP qui citent ce XML et leurs familles | proposition intégrée à l'implémentation (dans l'esprit du PA-19), non validée séparément | non (rapport §2) |
| Information sur stderr avec le préfixe `lepton: information:` ; `--json` inchangé | proposition non validée séparément | non (rapport §2) |

## Pièges rencontrés
- `scion rootstock-install` refuse un répertoire non vide → dans les tests, le dépôt de la graine
  est créé hors du rootstock.
- zsh : `echo =====` est interprété comme une expansion `=cmd` → ne pas l'utiliser comme
  séparateur.

## Critères de validation
- [x] PA-19 et PA-20 tranchés et consignés.
- [x] `lepton check` sur `<ROOTSTOCK>` : code 0.
- [x] Graines de projet des rootstocks d'essai : résultats de `lepton check` inchangés.
- [x] Schémas valides (`valider-schemas.sh`) ; tests de lepton verts.
- [x] Commandes de `lepton` qui lisent le manifeste : comportement sur `<ROOTSTOCK>` relevé et sans régression (`seed status` identique, `seed tree` 0 ; `generate` non exécuté, code inchangé).

## Reprise
Commande ou première action de la session suivante :
```
démarre la session   # skill devenv-session ; aucune étape planifiée après ENV-16 : demander la suite
```
