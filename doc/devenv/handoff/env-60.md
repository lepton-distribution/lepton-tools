# Passation ENV-60 — scion : clone gardé après un checkout en échec (D18) — session du 2026-11-17

## Statut
Terminée. scion 0.6.3.2 fait un clone à sa version déclarée par `git clone -b <version>`, ou ne
fait aucun clone. Publié.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` (fusion `--no-ff` de `devenv/env-60`) ; `devenv/env-60` | branche : a4ecaad étape en cours, c273628 audit, 1c05c10 PA-107, e7a589f `SCION_REF` 0.6.3.2, 032804a implémentation et essais, puis le commit d'état et de passation ; `main` et `devenv/env-60` poussés (PA-108) | oui |
| seed.scions | `master` 975caf6 (fusion `--no-ff` de `devenv/env-60`) | branche : cd1ed8a tests, 0fc156c correction, fb4d55d 0.6.3.2, 08a1460 NF-2 ; tag annoté `0.6.3.2` sur 08a1460 ; `master`, tag et `devenv/env-60` poussés | oui |
| clone noyau `depots/lepton/original/master` | `master` dfc960b (fusion `--no-ff` de `devenv/env-60`) | 8563f90 `SCION_REF` 0.6.3.2 ; `master` et `devenv/env-60` poussés ; clone remis sur `master` | oui |
| autres | — | graine `original-tree` 15740f9 non touchée ; `<ROOTSTOCK>` non regreffé (0 lien cassé, 7 `.DS_Store` tolérés du 12 novembre) ; `essais/env-11/qemu` intact | oui |

Outils (Mac) :
- scion **0.6.3.2**, installé par `pipx install --force "git+file://<SEED_SCIONS>@0.6.3.2"` ;
  10 modules identiques au tag. Point de retour : même commande avec `@0.6.3.1`.
- lepton 0.1.0, non réinstallé : seule une docstring change.
- Claude Code 2.1.326 ; extension 0.5.2.
- VM : scion 0.6.3.1 et lepton antérieur ; tous deux à monter en ENV-61.

## Fait pendant la session
- Début : état conforme à `handoff/env-59.md`. Bases : tests de scion 298 (1 sauté), pytest 508.
  Le fichier d'étape cite 453, valeur d'ENV-57.
- Audit (`rapports/env-60-scion.md` §1). Scripts `env-60-scion/fixture.py` (cas k01 à k19, u01)
  et `etat.py`. `essai.sh` sur une copie d'`essais/env-11/qemu`, avec le dépôt `env60lib`.
  - D18 confirmé : k01, u01.
  - Le fichier d'étape affirmait « jamais de greffe fausse ». C'est faux sur deux chemins :
    - `seed-clone` réutilise sans contrôle le clone resté sur `master` (k18). Par lepton, la
      seconde tentative de `seed add …@nope` réussit et greffe `master` (l03) ;
    - une graine distante est relue sur `master` (k05, k06) ; aucun contrôle ne le signale.
  - Une version qui n'est qu'un chemin du dépôt (`scion`) réussit en silence : k08, k17, l01.
  - Une branche homonyme d'un répertoire échoue au checkout (k11).
  - Une origine vide se comporte comme D18 (k15).
  - Un commit complet est accepté, puis refusé au passage suivant (k19).
  - `git clone -b` sondé (§1.6).
- PA-107 et PA-108 tranchés (§2, §8).
- Tests d'abord (cd1ed8a : `tests/test_clone_checkout.py`, 15 tests, et un test inversé). Sur
  0.6.3.1 : 11 échecs, 5 réussites (`env-60-scion/tests-avant-correction.txt`).
- Correction 0fc156c ; version fb4d55d ; NF-2 08a1460. 313 tests verts. NF-2 à 0.
- Essais (§4, venv de la branche) :
  - cas visés conformes : l01 à l03 en code 2 et état égal au départ ; u01 : trunk et clones
    égaux au départ ;
  - `seed add` réussi identique à 0.6.3.1 ;
  - fixture d'ENV-56 : écarts acceptés au PA-108.
- Tag local, puis pipx. `SCION_REF` passé à 0.6.3.2 dans lepton-tools (e7a589f) et dans le noyau
  (8563f90). pytest 508 avec 0.6.3.2.
- Essais supprimés par `scripts/supprimer-essai.sh`. Publication des trois dépôts.
  `HORS-PLAN.md` : D18 traité, D25 ajouté.

## Reste à faire dans l'étape
- Rien. Validation Debian en ENV-61 : monter scion 0.6.3.2 et lepton sur la VM, puis rejouer le
  cas D18. Le fichier d'étape d'ENV-61 a été écrit avant ENV-60 ; sa préparation doit reprendre :
  - C1 : scion 0.6.3.2, par `install-debian.sh` du noyau dfc960b (défaut `SCION_REF`) ;
  - attendu D18 : `rapports/env-60-scion/essai.sh`. l01 à l03 donnent le code 2 et le message
    `git clone -b … : fatal: Remote branch … not found in upstream origin`, puis l'annulation de
    lepton ; liens, graine, liste greffée et `depots/` égaux au départ. Relevé du Mac :
    `env-60-scion/apres/` ;
  - f06 de la fixture d'ENV-56 : aucun clone. f01 à f04 et f10 nomment `git clone -b master`
    (`env-60-scion/fixture56-apres/`). `fixture.py` d'ENV-60 peut aussi servir : `fixture-apres/`
    (u01 demande deux `graft-update` sur invite) ;
  - `ls-remote.sh` : tag 0.6.3.2, `master` 975caf6 de seed.scions, noyau dfc960b.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Plan de session, accord PA-P pour `graft-update` sur rootstocks temporaires | utilisateur | oui |
| PA-107 (1) : `git clone -b <version>` dans `gitops.clone` | utilisateur | oui |
| PA-107 (2), (3), (4), (6), (9) : cas couverts ; commit complet refusé d'emblée ; message de git ; documentation (P-V1 inchangé, test inversé) ; lepton : docstring seule | utilisateur | oui |
| PA-107 (5) : clones déjà laissés, réutilisés sans contrôle par `seed-clone` et `_clone_seed`, au hors-plan (D25) | utilisateur | oui |
| PA-107 (7), (8) : 0.6.3.2 ; `SCION_MIN_VERSION` inchangé ; `SCION_REF` 0.6.3.2 (lepton-tools, noyau) | utilisateur | oui |
| PA-108 : écarts du §7 acceptés (`-b master` dans 5 `.err` d'ENV-56, `test_seed.py:124` adapté, pas de branche locale de l'origine dans un clone de tag) ; essais supprimés ; publication | utilisateur | oui |
| Cas k08 à k19 (version-chemin, branche homonyme, origine vide, commit) et k18 (`seed-clone`) ajoutés à l'audit | proposition de la session, mise en œuvre pendant l'audit | rapport §1 |
| Tag posé sur 08a1460 (tête de branche, après le commit de version) plutôt que sur le commit de version | proposition de la session, mise en œuvre | rapport §5 |
| u01 « après » lancé avec le scion de pipx (tag local), pour garder la forme exacte de la règle `ask` | proposition de la session, mise en œuvre | rapport §4 |

## Pièges rencontrés
- Premier `graft-update` de l'audit lancé avec `cd … && LC_ALL=C` en tête : la forme sort de la
  règle `ask` (ORCHESTRATION §2bis). Lancer `scion graft-update <rootstock>` seul (redirections et
  `; echo` admis), sans `cd` ni variable en tête. Base refaite.
- Un exécutable de venv appelé par son chemin (`…/env-60-venv/bin/scion graft-update`) n'est pas
  couvert par la règle `ask`. Pour un `graft-update` avec la branche, poser d'abord le tag local et
  installer par pipx.
- Le hook refuse une commande shell qui crée un répertoire `trunk` (rootstock temporaire en
  scratchpad). Bâtir les rootstocks temporaires par `fixture.py`, forme établie en ENV-56.
- `git checkout <x>` sans `--` : si `x` n'est pas une ref mais un chemin, il restaure des fichiers
  et réussit (code 0) ; si `x` est une branche distante et un chemin, il échoue (« could be both »).
- La liste greffée sépare ses champs par des espaces, pas des tabulations.
- Docstring de test qui nomme lepton : le contrôle NF-2 compte aussi les tests.
- zsh : `echo ======` est une expansion `=commande`, pas un séparateur.
- `etat.py` normalise `<SHA>` : le commit des dépôts de la fixture change à chaque construction.

## Critères de validation
- [x] PA-107 et PA-108 tranchés et consignés.
- [x] Aucun nom propre à Lepton ajouté à scion : `git diff 0.6.3.1 -- scion tests | grep -ci '^+.*lepton'` → 0.
- [x] Tests de scion verts, dont les nouveaux (11 échecs sur `master`, réussite sur la branche) : 313.
- [x] f06 suit le PA-107 ; cas d'ENV-56 non visés identiques à l'avant, sauf l'écart du message
      (`-b master`) de f01 à f04 et f10, accepté au PA-108.
- [x] `seed add` réussi identique à 0.6.3.1.
- [x] Références de version conformes au PA-107 ; `pytest` de lepton-tools vert (508).
- [x] `HORS-PLAN.md` : D18 marqué traité, avec renvoi au rapport.

## Reprise
Commande ou première action de la session suivante :
```
démarre la session ENV-61 (skill devenv-session) : lire etapes/ENV-61-validation-debian.md et
handoff/env-60.md ; branche devenv/env-61 de lepton-tools (depuis main) ; tâche 1 (préparation
Mac) jusqu'au PA-109, en reportant les points « Reste à faire » de handoff/env-60.md
```
