# Passation ENV-40 — scion : miroir de conservation — session du 2026-11-06

## Statut
terminée — scion 0.6.1.0 implémente le miroir (partie B de la spécification), publié au PA-68 ;
les deux miroirs F4 existent sur GitHub et ont les mêmes références que leur amont ; rien n'est
basculé dans Lepton (ENV-41).

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` | fusion de `devenv/env-40` (commit de cette passation compris), poussée avec `devenv/env-40` | oui |
| `<SEED_SCIONS>` | `master` | f29fa35 « Fusion de devenv/env-40 (scion 0.6.1.0 : miroir de conservation) », poussée ; tag `0.6.1.0` sur 4502a70, publié | oui |
| clone noyau `depots/lepton/original/master` | `master` | 885696c « Fusion de devenv/env-40 (ENV-40 SCION_REF à scion 0.6.1.0, PA-68) », poussée avec `devenv/env-40` (61ce18d) | oui |
| `lepton-distribution/mirror-stm32f4xx-hal-driver` | `master` 6ef30cf + 15 tags | = `STMicroelectronics/stm32f4xx-hal-driver` (branches et tags) | — |
| `lepton-distribution/mirror-cmsis_device_f4` | `master` 9192c7b + 8 tags | = `STMicroelectronics/cmsis_device_f4` (branches et tags) | — |
| familles, BSP, graine `original-tree` | — | non touchés | oui |

scion installé : 0.6.1.0 (pipx, `git+file://<SEED_SCIONS>@0.6.1.0`). `<ROOTSTOCK>` non regreffé
(rien ne l'exige) : 3982 liens, sha `05b15192…` inchangé.
Configuration git globale de l'utilisateur modifiée (PA-68) :
`url."ssh://git@github.com/".pushInsteadOf "https://github.com/"`.

## Fait pendant la session
- §1 audit (`rapports/env-40-miroir.md` §1) : 17 écarts et précisions E1-E17 ; amonts relevés
  (`rapports/env-40-miroir/amont-*.ls-remote.txt`) ; PA-67 tranché.
- Spécification amendée (57061f2) : M-D1, M-D4, M-D5, M-C1, M-C2, M-C4, M-C6, M-R4, M-R8, M-K1.
- Code (`<SEED_SCIONS>`) :
  - `scion/mirror.py` (nouveau) : déclaration, dépôt de travail `depots/.mirrors/<hôte>/<chemin>`,
    règles par référence, envoi nommé, bilan ;
  - `cli.py` : `mirror-sync [rootstock] [--seed] [--dry-run] [url…]` ;
  - `graft.py` : suggestion de `mirror-sync` (M-D5) ; `gitops.py` : `refs`, `is_ancestor` ;
    `errors.py` : `UsageError` (code 2) ; `model.py` : `MIRRORS` ;
  - commits 4d113a3, b6db24c, 9b0bb9a (version), 4502a70 (tests renforcés).
- Tests : `~/lepton-tools-dev/venv-lepton-tools/bin/python -m pytest -q` dans `<SEED_SCIONS>` →
  265 réussis, 1 sauté (36 dans `tests/test_mirror.py`). Contrôle par mutation : 8 sur 8 détectées
  (M-R8 après renforcement).
- Essai local `~/lepton-tools-dev/essais/env-40-miroirs/` (rapport §3) : miroirs = copies d'amont
  = relevé GitHub ; tag déplacé signalé (code 1), miroir inchangé.
- PA-68 : tag, pipx 0.6.1.0, `pushInsteadOf`, `gh repo create` ×2 (publics, description seule),
  synchronisation depuis `~/lepton-tools-dev/essais/env-40-publication/` (16 et 9 références),
  `git ls-remote` = amont, b6f0ed3 et 3c77349 atteignables, seconde passe code 0 ; `lepton check`
  code 0 ; pytest lepton 235 réussis ; `SCION_REF` 0.6.1.0 (lepton-tools 311b18a, noyau 61ce18d) ;
  fusions et push des trois dépôts.

## Reste à faire dans l'étape
- [x] Rien. La validation Debian est reportée à ENV-43.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Plan de session (audit, PA-67, implémentation, essai, PA-68, publication) | utilisateur | oui (journal) |
| PA-67 : E1-E17 acceptés ; E6 littéral ; E13 graine de publication d'essai ; 0.6.1.0 ; `SCION_REF` ici ; `SCION_MIN_VERSION` en ENV-41 | utilisateur | oui |
| PA-68 : `mirror-<nom amont>`, publics, description seule, création par `gh`, `pushInsteadOf` global, publication complète | utilisateur | oui |
| Deux commits de fond (déclaration, commande) au lieu d'un par règle ; un commit de tests après la version | écart de procédure, signalé | oui (rapport §2) |
| Essai local avec scion lancé depuis les sources | choix de session, comme en ENV-39 | oui (rapport §3) |
| Tag `0.6.1.0` sur 4502a70 (tests renforcés) plutôt que sur le commit de version 9b0bb9a | choix de session | oui (rapport §4) |
| Pas de regreffe de `<ROOTSTOCK>` : aucun `.scion.mirrors` n'y est lu, liste des liens contrôlée par empreinte | choix de session | oui (rapport §4) |
| Les miroirs sont déclarés pour l'instant dans la graine de publication (hors greffons) ; les recopier dans `family-stm32f4xx` en ENV-41 | conséquence du PA-67 E13 ; forme exacte à trancher au PA-69 | oui (prochaine action) |

## Pièges rencontrés
- argparse : un positionnel `nargs="*"` suivi d'une option, puis d'autres positionnels, donne
  « unrecognized arguments ». Parade : `parse_known_args`, les restes ne sont repris que pour
  `mirror-sync`.
- `git clone --mirror` pose `remote.origin.mirror=true` : un `git push` à la main serait un
  `push --mirror`. scion le retire. Ne jamais pousser à la main depuis `depots/.mirrors/`.
- Sans `--prune` sur le remote `amont`, une référence supprimée en amont reste dans
  `refs/amont/*` et n'est pas signalée.
- Un tag déplacé poussé sans `+` est refusé par git lui-même. C'est pour cela que la mutation M-R8
  échappait aux tests. Les tests vérifient maintenant qu'aucun envoi n'est tenté.
- Liste des liens de `<ROOTSTOCK>` : empreinte = SHA-256 des lignes `./chemin -> cible` triées,
  relevées depuis `trunk/` (`os.walk`, liens seulement), terminées par un saut de ligne.
- `DEVENV-STATUS.md` dépasse 200 Ko : le lire par sections.
- Pas de `timeout` sur macOS.

## Critères de validation
- [x] PA-67 et PA-68 tranchés et consignés.
- [x] Tests de scion verts, dont un par cas nommé. Aucune chaîne propre à Lepton ajoutée dans
      `seed.scions` (`git diff f526f25 -- scion/ | grep -i '^+.*lepton'` : 0). `grep -ri lepton scion/`
      reste non nul à cause de `scion/__init__.py` (E17).
- [x] Essai local : tag déplacé signalé, miroir inchangé.
- [x] Les deux miroirs publiés ont les mêmes références que leur amont (`git ls-remote`), et les
      deux commits épinglés y sont atteignables.
- [x] Toutes les références de version désignent 0.6.1.0 (`scion version`, tag, `SCION_REF`,
      documentation). `SCION_MIN_VERSION` reste 0.5.4.0 jusqu'à ENV-41.

## Reprise
Commande ou première action de la session suivante :
```
démarre la session   # ENV-41 : lire cette passation, etapes/ENV-41-f4-projection.md, rapports env-38 §2.1 et §4, env-39 §3, env-40 §4 ; PA-69 ; sources = URL des miroirs, .scion.mirrors à recopier dans family-stm32f4xx
```
