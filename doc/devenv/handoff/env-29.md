# Passation ENV-29 — scion : `graft-update` sûr (version déclarée, trunk préservé) — session du 2026-11-03

## Statut
terminée — scion 0.5.4.0 publié. Un clone hors version déclarée est refusé avant tout dégreffage,
et le trunk est rétabli si la regreffe échoue. lepton exige 0.5.4.0.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` (fusion `--no-ff` de `devenv/env-29`, poussées toutes deux) | « Fusion de devenv/env-29 (ENV-29 scion 0.5.4.0, PA-46) » ; fond : « devenv(env-29): état et passation » | oui |
| clone noyau `depots/lepton/original/master` | `master` be25cd0 (fusion de `devenv/env-29` c1af6c3), poussées | « Fusion de devenv/env-29 (ENV-29 scion 0.5.4.0 par défaut, PA-46) » | oui |
| seed.scions | `master` 1173d6d (fusion de `devenv/env-29`), tag `0.5.4.0` sur 99aa973 ; `master` et tag poussés, branche non poussée | « Fusion de devenv/env-29 (scion 0.5.4.0) » | oui |
| graine `original-tree`, greffons famille et BSP | non touchés | — | oui |

Hors dépôts :
- scion 0.5.4.0 par pipx (`git+file://<SEED_SCIONS>@0.5.4.0`) ;
- lepton réinstallé par pipx depuis a1716f9 ;
- copie et venv d'essai supprimés ; mesures dans `~/lepton-tools-dev/essais/env-29-mesures/`.

## Fait pendant la session
- Tâche 1 : audit (`rapports/env-29-scion.md` §1) :
  - fixture hors réseau : 10 cas de clone ; 8 vident le trunk ; un tag échoue toujours ; E-1 est
    tiré en silence ;
  - E-1 reproduit sur la copie : `graft-update`, 277 conflits, 0 lien ;
  - `scion graft` seul a le même défaut ;
  - PA-45 et PA-45 (2) tranchés.
- Tâche 2 : seed.scions, tests écrits d'abord (`tests/test_clone_versions.py`, 22 tests) :
  - 045b250 : clones à la version déclarée, `--ff-only` ;
  - ad99094 : trunk rétabli si la regreffe échoue ;
  - 99aa973 : version 0.5.4.0 ;
  - 159 tests verts.
- Tâche 3 : copie et scion du venv (§3) :
  - (a) refus avant dégreffage ;
  - (b) et `graft` sur conflit : trunk rétabli, `sha256` de la liste triée identique (`a7afbc1d…`) ;
  - (c) nominal = `<ROOTSTOCK>`.
- Tâche 4 (§4) :
  - tag et pipx ;
  - lepton-tools a1716f9, `pytest` 229 verts ;
  - clone noyau c1af6c3 ;
  - `<ROOTSTOCK>` regreffé par `scion graft` (liste inchangée, `lepton check` 0) ;
  - ORCHESTRATION §2bis allégée.
- PA-46 : fusions et push (§5).

## Reste à faire dans l'étape
- Aucune. La validation Debian de scion 0.5.4.0 relève d'ENV-33 : `install-debian.sh` du noyau
  be25cd0, avec `SCION_REF` 0.5.4.0 par défaut.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-P : `graft-update` 0.5.3.0 sur la copie pour reproduire E-1 | utilisateur | oui |
| PA-45 : refus toujours ; rétablissement du trunk, `graft` compris ; 0.5.4.0 ; `SCION_MIN_VERSION` relevé ; règle P-1 allégée ; P-1 à P-4 du rapport | utilisateur | oui |
| PA-45 (2) : `seed-add` suit la même règle ; plus aucun `git pull` dans scion | utilisateur | oui |
| PA-P : trois `graft-update` 0.5.4.0 sur la copie (a, b, c) | utilisateur | oui |
| PA-46 : fusions et push des trois dépôts ; copie et venv supprimés | utilisateur | oui |
| scion de la branche essayé dans un venv, et non par `pipx install --force`, pour la tâche 3 | proposition de la session, signalée à l'utilisateur | `rapports/env-29-scion.md` §3 |
| Regreffe de `<ROOTSTOCK>` par `scion graft` (pas de `graft-update`) | proposition de la session | `rapports/env-29-scion.md` §4 |
| Push de seed.scions par l'URL SSH (précédent d'ENV-23) | proposition de la session, dans le cadre de l'accord PA-46 | `rapports/env-29-scion.md` §5 |

## Pièges rencontrés
- Hook `proteger-trunk.py` :
  - symptôme : refus d'une commande de mesure qui contenait `cp trunk/.scion.grafted.list …`,
    avec le trunk en source seulement ;
  - parade : `shasum` du fichier en lecture seule.
- `.DS_Store` du Finder :
  - symptôme : fichiers apparus dans les trunks quelques secondes après chaque commande, et même
    pendant le `rm -rf` de la copie ;
  - cause : une fenêtre du Finder ouverte sur le trunk ;
  - effet : tolérés par `.scion.trunk.tolerated`, sans effet sur la liste des liens ; le bilan
    « reguliers » de `env-15-liste-trunk.sh` les compte.
- `git push` HTTPS de seed.scions :
  - symptôme : « could not read Username » ;
  - parade : URL SSH `git@github.com:lepton-distribution/seed.scions.git`.
- `git rev-parse --short A B` :
  - symptôme : « Needed a single revision » ;
  - parade : un appel par révision.
- Avec scion ≥ 0.5.4.0, `graft-update` refuse un rootstock dont un clone est sur une branche
  d'étape (`devenv/env-N`). Pour regreffer pendant une étape, utiliser `scion graft`.

## Critères de validation
- [x] PA-45 et PA-46 tranchés et consignés.
- [x] Tests de scion verts, dont les nouveaux (159) ; aucune chaîne propre à Lepton dans
      `seed.scions` (`grep -ri lepton scion/` : 2 lignes de métadonnées, tolérées par PA-2 Q7).
- [x] Copie d'essai : E-1 reproduit avant le correctif, et ne se produit plus après ; trunk intact
      sur conflit (`sha256` de la liste triée).
- [x] Toutes les références de version (lepton, `install-vscodium.sh`, scripts du noyau,
      documentation) désignent la même version, 0.5.4.0.

## Reprise
Commande ou première action de la session suivante :
```
démarre la session   # ENV-30 (etapes/ENV-30-taches-tests-greffons.md), audit jusqu'au PA-47
```
