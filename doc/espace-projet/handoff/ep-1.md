# Passation EP-1 — Greffon de type `projet` dans lepton — session du 2026-11-27

## Statut
terminée — lepton 0.2.0 et extension 0.5.5 ; PA-E2 et PA-E3 clos ; branche fusionnée dans `main`
et poussée sur accord.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `espace-projet/ep-1` (depuis `main` c76612d) | commit de fin de session « espace-projet(ep-1): état et passation » (après c1aa189 extension 0.5.5) | oui ; fusionnée `--no-ff` dans `main`, poussée (accord du 2026-11-27) |
| clone noyau `depots/lepton/original/master` | `master` | 0c2e43e Fusion de devenv/env-70 | oui (inchangé : noyau non modifié, PA-E2) |
| `<SEED_SCIONS>` | `master` | 929c01a Fusion de devenv/env-70 | oui (inchangé) |
| graine de référence `original-tree` | `original-tree` | 15740f9 Fusion de devenv/env-20 | oui (inchangé) |
| essais | — | `essais/ep-1/` supprimé (`scripts/supprimer-essai.sh`, rc 0) | — |

## Fait pendant la session
- Audit et propositions : `rapports/ep-1-type-projet.md` §1 à §4 ; pytest de départ 616 verts.
- Schémas : type `projet` (`schemas/greffon.schema.json`), exemples valide et invalides ;
  `scripts/valider-schemas.sh` conforme (9c688fa).
- lepton 0.2.0 (dbc6b86) : `find_manifest` lit `scion/sys/user/<nom>/` ; `seed new` crée
  (`--project-repo`, défaut `depots/lepton-project/<nom>`) ou désigne (`--origin <nom>=…`) le
  greffon projet ; `seed mkconf import`, `generate`, `check`, `seed status`, `seed lock`,
  `seed remove` ; graine de référence = pas de `lepton-graine.json` ; ancien format refusé.
- Tests (ee65f4f) : `tests/test_project_scion.py` (23 ; 23 échecs sur `main`) ; tests adaptés et
  inversés listés au rapport §6.3 ; **642 verts**.
- Non-régression (rapport §6.4) : bout-en-bout et fumée QEMU du preset généré verts ; copie de
  `<ROOTSTOCK>` : `check` 0, espace de `main` et de la branche identiques (`diff` vide) ;
  procédure manuelle de l'ancien format essayée (`README.md`).
- `doc/espace-projet/EXIGENCES.md` (T9) ; `HORS-PLAN.md` H7, H8.
- PA-E3 : essai VSCodium de l'utilisateur conforme ; extension 0.5.5 (libellé, e054348, c1aa189),
  installée dans VSCodium ; pipx réinstallé (`lepton --version` 0.2.0, 18 modules identiques).

## Reste à faire dans l'étape
- [ ] Rien dans l'étape. Hors session : l'utilisateur retire le réglage `lepton.path` ajouté pour
      l'essai (venv de développement).

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans STATUS ? |
| --- | --- | --- |
| PA-E2 : propositions recommandées (1) à (8) du rapport §3 | utilisateur, sur recommandation de la session | oui |
| PA-E3 (essai) : conforme | utilisateur | oui |
| PA-E3 (libellé) : extension corrigée maintenant, 0.5.5 (revient sur PA-E2 (8)) | utilisateur, contre la recommandation (hors plan) | oui |
| PA-E3 (essais) : `essais/ep-1/` supprimé | utilisateur, sur recommandation | oui |
| PA-E3 (pipx) : lepton 0.2.0 réinstallé | utilisateur, sur recommandation | oui |
| PA-P (EP-1) : fusion `--no-ff` et push de `main` | utilisateur, sur recommandation | oui |
| Variantes du rapport §3 (clé `greffon_projet`, migration par commande, presets en régime de référence, §22 d'`env-8-interface.md`) | propositions non retenues | rapport seulement |

Tickets créés pendant la session : aucun.

## Pièges rencontrés
- `python -m lepton` lancé depuis le dépôt charge le lepton du répertoire courant, pas celui de
  `PYTHONPATH` → première comparaison `main` / branche faussée (les deux en 0.2.0) → lancer hors du
  dépôt et afficher `lepton.__version__` à chaque passe.
- Comparer l'espace de deux versions de lepton : les chemins des schémas y sont absolus → les deux
  passes depuis le même worktree (`main`, puis la tête de la branche).
- Procédure manuelle de l'ancien format : après `seed-scion-remove` / `seed-scion-add`, la liste
  greffée garde l'ancien emplacement et `graft` échoue (« project/scion est absent ») →
  `scion seed-clone --seed <graine>` avant `lepton graft`.
- `seed add` d'une application écrit `<bin>` dans le XML du greffon projet → `seed lock` refuse
  tant que ce dépôt n'est pas commité (règle « clone modifié »).
- `git stash pop` en conflit sur deux lignes voisines du README → résolu à la main, stash supprimé.

## Critères de validation
- [x] PA-E2 et PA-E3 tranchés et consignés.
- [x] `pytest` vert : 616 de départ + 3 exemples + 23 nouveaux = 642 ; tests inversés listés (rapport §6.3).
- [x] `scripts/valider-schemas.sh` vert ; un greffon `projet` valide et deux invalides.
- [x] `grep -rnE 'PROJECT_SUBPATH|project_key|project_stem|graft_project|project/' lepton --include='*.py'` :
      occurrences justifiées (rapport §6.5).
- [x] Graine migrée : sans objet (PA-E2 : refus et abandon) ; procédure manuelle essayée.
- [x] Projet neuf : fumée QEMU verte.
- [x] Copie de `<ROOTSTOCK>` : `check` code 0 ; espaces générés par `main` et par la branche identiques.
- [x] `git -C <SEED_SCIONS> status --short` : vide.

## Reprise
Commande ou première action de la session suivante :
```
démarre EP-2   (skill espace-projet-session ; vérifier main = origin/main ; EP-3 ou EP-7 possibles)
```
