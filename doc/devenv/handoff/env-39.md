# Passation ENV-39 — scion : projection d'un dépôt tiers — session du 2026-11-06

## Statut
terminée — scion 0.6.0.0 implémente la projection (partie A de la spécification), publiée au
PA-66 ; rien n'est basculé dans Lepton (ENV-41).

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` | fusion de `devenv/env-39` (commit de cette passation compris), poussée avec `devenv/env-39` | oui |
| `<SEED_SCIONS>` | `master` | f526f25 « Fusion de devenv/env-39 (scion 0.6.0.0…) », poussée ; tag `0.6.0.0` sur 7634504, publié | oui |
| clone noyau `depots/lepton/original/master` | `master` | 00911b9 « Fusion de devenv/env-39 (ENV-39 SCION_REF à scion 0.6.0.0, PA-66) », poussée avec `devenv/env-39` (8edff56) | oui |
| familles, BSP, graine `original-tree` | — | non touchés (`family-stm32f4xx` 0fd8b2a ; graine 15740f9) | oui |

scion installé : 0.6.0.0 (pipx, `git+file://<SEED_SCIONS>@0.6.0.0`). `<ROOTSTOCK>` regreffé en
0.6.0.0 : 3982 liens, liste identique à avant (sha 05b15192…), aucune projection.

## Fait pendant la session
- §1 audit (`rapports/env-39-scion.md` §1) : base de 158 tests verts ; 12 écarts et précisions
  E1-E12 ; PA-65 tranché.
- Spécification amendée (f5c71ce) :
  - règles précisées : P-T4, P-K2, P-V1, P-V2, P-V4, P-E1, P-P4, P-P5, P-G3, A.11 ;
  - nouvelles règles P-V6 (version déclarée toujours prioritaire) et P-P7 (clé que le porteur ne
    déclare plus : retirée).
- Code (`<SEED_SCIONS>`) :
  - `model.py` : 6ᵉ colonne `carrier` (b82452a) ;
  - `projection.py` (nouveau) et `gitops.py` (8141b53) ;
  - `graft.py` et `cli.py`, tests (a9d8ea5) ;
  - version (7634504).
- Tests : `~/lepton-tools-dev/venv-lepton-tools/bin/python -m pytest -q` dans `<SEED_SCIONS>` →
  229 réussis, 1 sauté. `tests/test_projection.py` en apporte 71. Un contrôle par mutation fait
  échouer 4 tests.
- Copie d'essai `~/lepton-tools-dev/essais/env-39-copie` (§3 du rapport), scion lancé depuis les
  sources :
  - sans projection : sha de la liste des liens identique à 0.5.4.0 ;
  - essai à blanc F4 : 3982 chemins identiques, 206 cibles projetées = `attendus/f4-*.txt`, contenu
    identique (`cmp`), 0 écart ;
  - relevés : `rapports/env-39-scion/essai-f4.diff`, `chemins-projetes.txt`.
- §4 :
  - PA-P : pipx 0.6.0.0, `scion graft` de `<ROOTSTOCK>` (inchangé) ;
  - `pytest` lepton → 235 réussis ; `lepton check` → code 0 ;
  - `SCION_REF` relevé à 0.6.0.0 (lepton-tools ed3eafd, noyau 8edff56) ; `shellcheck` conforme.
- PA-66 : fusions et push dans les trois dépôts. seed.scions a été poussé par l'URL SSH, son
  `origin` étant en `https://`.

## Reste à faire dans l'étape
- [x] Rien. La validation Debian est reportée à ENV-43.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Plan de session (audit, PA-65, implémentation, essai, version, PA-66) | utilisateur | oui (journal) |
| PA-65 : E1, E2, E4-E12 acceptés ; E3 → retrait (P-P7) ; 0.6.0.0 ; `SCION_REF` ici ; aucun effet lepton | utilisateur | oui |
| PA-P : pipx 0.6.0.0 et regreffe de `<ROOTSTOCK>` | utilisateur | oui |
| PA-66 : publication complète | utilisateur | oui |
| Essai sur copie avec scion lancé depuis les sources (`python3 -m scion.cli`) au lieu de `pipx install` de la branche | choix de session, plus prudent que le fichier d'étape ; résultat équivalent | oui (rapport §3) |
| Trois commits de fond au lieu d'un par comportement (code entrelacé dans `graft.py`) | écart de procédure, signalé | oui (rapport §2) |
| `lepton-tools/README.md` : minimum 0.5.4.0 conservé, version installée 0.6.0.0 mentionnée | interprétation du PA-65 | oui (rapport §4) |
| P-P4 vérifié dans la résolution d'une graine (graine et ses porteurs) ; entre deux graines d'un même rootstock, la dernière synchronisée l'emporte (P-V6) | proposition non validée (comportement d'implémentation) | non (ici) |
| Noms de clé `tiers stm32f4xx-hal-driver`, `tiers cmsis-device-f4`, shelf `tiers` de l'essai | proposition d'ENV-38, toujours non validée (PA-69) | non |

## Pièges rencontrés
- `DEVENV-STATUS.md` dépasse 200 Ko : le lire par sections (`grep -n '^#'`, puis `sed -n`).
- `pytest` n'est pas dans le Python système. Utiliser `~/lepton-tools-dev/venv-lepton-tools/bin/python -m pytest`.
  La suite de scion dure environ 3 min 30, celle de lepton environ 6 min 40.
- zsh ne découpe pas une variable qui contient une commande (`$S graft` → « no such file ») :
  utiliser une fonction shell.
- `find -L trunk -type l` liste les liens cassés. Ne pas confondre sa sortie avec celle de
  `find -type f`.
- seed.scions : `origin` est en `https://`, sans identifiants. Pousser par
  `ssh://git@github.com/lepton-distribution/seed.scions.git`, comme en ENV-29.
- Clone partiel par `file://` : git avertit « filtering not recognized by server » et clone en
  entier ; sans effet.
- Copie d'essai : URL `file://localhost/<chemin>`. Un `file:///` serait lu comme un chemin local
  (P-V3).

## Critères de validation
- [x] PA-65 et PA-66 tranchés et consignés.
- [x] Tests de scion verts, un ou plusieurs par cas nommé du plan de tests.
- [ ] `grep -ri lepton scion/` : 0. Critère non tenu littéralement, et déjà avant ENV-39 : URL et
      adresse dans `scion/__init__.py`. Le diff d'ENV-39 n'ajoute aucune occurrence.
- [x] Rootstock sans projection : liste des liens identique avant et après (`sha256`).
- [x] Essai à blanc F4 sur la copie : liste des chemins du trunk identique, aucun écart.
- [x] Références de version d'installation (`install-vscodium.sh`, scripts du noyau,
      documentation) : 0.6.0.0. `SCION_MIN_VERSION` reste 0.5.4.0 jusqu'à ENV-41 (PA-63 Q13).

## Reprise
Commande ou première action de la session suivante :
```
démarre la session   # ENV-40 : lire cette passation, la spécification (partie B), le rapport env-38 §3 (M-*) et §4, puis PA-67 ; départ seed.scions master f526f25, tag 0.6.0.0, version visée 0.6.1.0
```
