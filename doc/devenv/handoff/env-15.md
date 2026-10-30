# Passation ENV-15 — Fichiers ignorés et fichiers étrangers dans scion — session du 2026-10-30

## Statut
terminée — scion 0.5.2.0 ne greffe plus les fichiers ignorés par git (E1) et tolère les fichiers
du trunk déclarés dans `<rootstock>/.scion.trunk.tolerated` (E2) ; validation Debian R15-1
conforme ; lepton exige scion ≥ 0.5.2.0.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` (fusion de `devenv/env-15`, poussées toutes deux) | commit d'état et passation, puis fusion « Fusion de devenv/env-15 » | oui |
| `<SEED_SCIONS>` | `master` 472c12e « Fusion de devenv/env-15 (scion 0.5.2.0) », tag annoté `0.5.2.0` ; `master` et tag poussés | `devenv/env-15` 027d5cd locale, non poussée (contenue dans `master`) | oui |
| clone noyau `depots/lepton/original/master` | `master` 6f1801d « Fusion de devenv/env-15 (scion 0.5.2.0 par défaut) » ; `devenv/env-15` 0ad8a03 ; poussées | | oui |
| 7 autres greffons, graine `original-tree` 0f1275a | `master` / `original-tree`, inchangés (f4 7694ad5) | | oui |
| `<ROOTSTOCK>` trunk | regreffé avec scion 0.5.2.0 | 3929 liens, liste (lien, cible) identique, 0 cassé, 0 fichier régulier ; pas de `.scion.trunk.tolerated` (rootstock antérieur à 0.5.2.0) | oui |

## Fait pendant la session
- Tâche 1 : audit de scion (`rapports/env-15-scion.md` §1-§2) ; PA-17.
- Tâche 2 : `<SEED_SCIONS>` e21d3cf (E1 : `git ls-files --others --ignored --exclude-standard
  --directory` par greffon), 0601792 (E2 : motifs `fnmatch` du rootstock, supprimés au dégreffage),
  027d5cd (0.5.2.0, README, CHANGELOG) ; `python3 -m unittest discover -s tests` : 126 tests,
  OK (skipped=1) ; `grep -ri lepton scion/` vide.
- Tâche 3 : copie `essais/env-15` (venv `essais/env-15-venv`, mesures `essais/env-15-mesures/`) :
  regreffe identique ; conflit de `.DS_Store` ignorés reproduit en 0.5.1.1, résolu en 0.5.2.0 ;
  fichier non suivi greffé ; `.DS_Store` réguliers tolérés sans `--force` (§5).
- Tâche 4 : fusion `master` 472c12e, tag, pipx ; lepton-tools 1e65851 (`SCION_MIN_VERSION`,
  `SCION_REF`, test `test_graft_removes_system_files` adapté) ; `pytest` 198 verts ; `<ROOTSTOCK>`
  regreffé, liste identique (§6) ; PA-18 (1) : pushes, ordre R15-1.
- Tâche 5 : R15-1 (`consignes/env-15-debian.md`, VM `lepton-vm-debian`) : FIN-SUCCÈS, C1 à C8,
  `comparer-oracle` 0 contre R14-1 sur host + 6 presets QEMU (`rapports/env-15-debian.md`) ;
  `devenv/env-15-debian` fe4905f vérifiée et fusionnée ; PA-18 (2).
- Clôture : défaut scion du clone noyau aligné à 0.5.2.0 (§9).

## Reste à faire dans l'étape
- Aucune tâche du fichier d'étape.
- Hors étape, à décider :
  - `<ROOTSTOCK>` et les rootstocks d'essai n'ont pas de `.scion.trunk.tolerated` ; lepton purge
    déjà `.DS_Store` / `._*` du trunk (PA-9 Q8). Créer ce fichier n'a pas été demandé.
  - Les rootstocks d'essai ne profitent d'E1 qu'avec scion 0.5.2.0 à leur prochaine regreffe.
  - Supprimables : `essais/env-15`, `essais/env-15-venv`, `essais/env-15-mesures` ; sur la VM,
    `~/lepton-tools-dev/essais/env-15-debian` et `~/env-15-journaux/`.
  - Le défaut scion 0.5.2.0 des scripts du clone noyau n'a pas été exécuté sur Debian.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-17 : E1 tel que proposé ; E2 option A (motifs du rootstock) ; fichier toléré supprimé au dégreffage ; version 0.5.2.0 ; essai dans un venv | utilisateur | oui |
| PA-18 (1) : push du tag et de `master` de `<SEED_SCIONS>`, de `devenv/env-15` ; R15-1 sur host + 6 presets QEMU ; adaptation du test PA-9 Q8 ; scion 0.5.2.0 conservé malgré l'installation avant le PA-18 | utilisateur | oui |
| PA-18 (2) : fusion de `devenv/env-15` dans `main` et push | utilisateur | oui |
| Alignement du défaut scion du clone noyau à 0.5.2.0, fusion et push | utilisateur | oui |

## Pièges rencontrés
- Hook `proteger-trunk.py` : refus d'une commande qui créait des fichiers dans le trunk de la copie →
  copie par `cp -RP`, fichiers réguliers d'essai créés par l'utilisateur (`! touch`).
- Push https de `<SEED_SCIONS>` refusé (pas d'identifiants) → push par
  `ssh://git@github.com/lepton-distribution/seed.scions.git`, configuration du clone inchangée.
- Session VM : permissions refusant le code externe (`pipx install`, clone et tests de scion) →
  commandes de la consigne lancées par l'utilisateur dans la session VM.
- Clone noyau : `.DS_Store` déjà ignoré par son `.gitignore` (ligne 482) ; l'essai E1 Debian ne
  prouve la règle globale que sur le BSP an386.
- Le relèvement de version doit couvrir aussi le clone noyau (`install-{macos,debian}.sh`,
  `BUILDING.md`, `README-PAQUET.md`), pas seulement lepton-tools.

## Critères de validation
- [x] PA-17 et PA-18 tranchés et consignés.
- [x] Tests de scion verts ; `grep -ri lepton scion/` vide ; tests de lepton verts.
- [x] Copie et `<ROOTSTOCK>` : liste (lien, cible) du trunk identique avant et après la nouvelle version.
- [x] Fichier ignoré au même chemin dans deux clones : greffe sans conflit, non greffé.
- [x] Fichier nouveau non suivi : greffé.
- [x] `.DS_Store` régulier dans le trunk : comportement validé au PA-17, sans `--force`.
- [x] Nouvelle version taguée, installée, relevée par `scion version` ; `SCION_MIN_VERSION` et `SCION_REF` alignés.
- [x] `FIN-SUCCÈS R15-1`.

## Reprise
Commande ou première action de la session suivante :
```
démarre la session ENV-16   # skill devenv-session ; etapes/ENV-16-manifeste-graine.md, tâche 1 jusqu'au PA-19
```
