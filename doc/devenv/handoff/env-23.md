# Passation ENV-23 — Évolutions de scion : mise à jour de la graine, sources non git — session du 2026-11-02

## Statut
terminée — scion 0.5.3.0 publié (graine avancée par `graft-update`/`seed-update`, sources non git
filtrées par les règles de git), lepton et le clone noyau alignés, `<ROOTSTOCK>` regreffé sans
changement.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` (fusion `--no-ff` de `devenv/env-23`, poussées toutes deux) | « Fusion de devenv/env-23 » ; fond : 016a788 (N-2), 5e03b27 (version), 77c3197 (rapport) | oui |
| seed.scions `<SEED_SCIONS>` | `master` e4d76b2 « Fusion de devenv/env-23 (scion 0.5.3.0) » = origin ; tag `0.5.3.0` sur ad292ee (poussé) ; `devenv/env-23` locale (a2eb0cb, bf6bad3, ad292ee), non poussée | | oui |
| clone noyau `depots/lepton/original/master` | `master` 0a6df02 « Fusion de devenv/env-23 » = origin ; `devenv/env-23` 62f3f86 poussée | | oui |
| graine `depots/lepton-seed.scions/original-tree` | `original-tree` 15740f9 = origin | inchangée | oui |
| `<ROOTSTOCK>` | trunk 3941 liens, liste identique (SHA-256 `9be3357c…`, `rapports/env-15-liste-trunk.sh`) | | oui |

Outils : scion 0.5.3.0 (pipx, tag), lepton 0.1.0 réinstallé (pipx, exige ≥ 0.5.3.0).

## Fait pendant la session
- Audit et propositions : `rapports/env-23-scion.md` §1-§2 ; PA-33 §3.
- seed.scions : N-a (a2eb0cb), G-a (bf6bad3), 0.5.3.0 (ad292ee) ; `python3 -m unittest discover
  -s tests` : 137 tests OK ; `grep -ri lepton scion/` : 2 lignes de métadonnées (PA-2 Q7).
- Copie d'essai (§5) : `.DS_Store` de `building` exclu ; graine reculée avancée et BSP F439
  regreffé ; refus sur graine modifiée, trunk intact ; liste = `<ROOTSTOCK>`.
- lepton-tools : N-2 (défaut `depots/lepton/<kind>-NAME/master`), `SCION_MIN_VERSION`,
  `SCION_REF`, README ; `pytest` 216 verts.
- Clone noyau : `SCION_REF` d'`install-{macos,debian}.sh`, `BUILDING.md`, `README-PAQUET.md`,
  `README.md` à 0.5.3.0.
- `<ROOTSTOCK>` : `scion graft` code 0, 0 régulier, 0 cassé ; `lepton check` code 0.
- PA-34 : fusions et push ; copie et venv d'essai supprimés.

## Reste à faire dans l'étape
- Aucune tâche du fichier d'étape. Validation Debian de 0.5.3.0 : ENV-28.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-33 : G-a (par défaut, avance rapide, refus avant `ungraft`), N-a (règles de git), 0.5.3.0, minimum relevé, purge de lepton conservée, N-2 en ENV-23 | utilisateur | oui |
| PA-34 : points signalés acceptés, publication complète (sauf `devenv/env-23` de seed.scions), suppression copie et venv | utilisateur | oui |
| Essai par venv au lieu de `pipx install` de la branche | proposition de la session, acceptée au PA-34 | oui |
| Tag sur le commit de version (ad292ee) et non sur la fusion | proposition de la session, acceptée au PA-34 | oui |
| Push de seed.scions par l'URL SSH (sans changer `origin`) | proposition de la session, dans le cadre de l'accord PA-34 | oui |
| Commentaire de `tests/test_milestone5.py:142` (« scion ≥ 0.5.2.0 ») conservé | proposition de la session | rapport §6 |

## Pièges rencontrés
- `scion -v graft` ne marche pas : `-v` va après la sous-commande (`scion graft -v`) ; sinon erreur
  d'arguments et rien ne tourne.
- `git merge -F -` ne lit pas l'entrée standard : écrire le message dans un fichier.
- `origin` de `<SEED_SCIONS>` en HTTPS sans identifiants (« could not read Username ») : pousser
  par `git@github.com:lepton-distribution/seed.scions.git` (`gh` configuré en SSH).
- `._*` n'est exclu d'une source non git que si les règles de git de l'hôte le listent
  (`~/.gitignore_global` : `.DS_Store` seul) ; ajout éventuel : décision de l'utilisateur.
- `HEAD~1` de la graine `original-tree` est le premier parent de la fusion (f4ff07b, 2 commits de
  retard).

## Critères de validation
- [x] PA-33 et PA-34 tranchés et consignés.
- [x] Tests de scion verts, dont les nouveaux ; aucune chaîne propre à Lepton dans `seed.scions`
      (`grep -ri lepton` : métadonnées seules, PA-2 Q7).
- [x] Copie d'essai : graine avancée et refus conforme ; fichier étranger de `building` non greffé.
- [x] Toutes les références de version (lepton, `install-vscodium.sh`, scripts du noyau,
      documentation) désignent 0.5.3.0.

## Reprise
Commande ou première action de la session suivante :
```
démarre la session   # skill devenv-session ; ENV-24 (etapes/ENV-24-cpufs-automatique.md), audit jusqu'au PA-35
```
