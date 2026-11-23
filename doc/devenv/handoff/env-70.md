# Passation ENV-70 — scion : cause de l'échec de git, version de la graine clonée (D35, D33) — session du 2026-11-23

## Statut
terminée — scion 0.6.3.4 publié (D33, D35), `SCION_REF` 0.6.3.4 dans lepton-tools et le clone noyau ;
la preuve avec git 2.47.3 se fait sur la VM en ENV-72.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `devenv/env-70` (depuis `main` fa7b883), fusionnée `--no-ff` dans `main` ; `main` et la branche poussées (PA-128) | branche : « devenv(env-70): état et passation » ; `main` : fusion de `devenv/env-70` | oui |
| clone noyau `depots/lepton/original/master` | `master` (revenu de `devenv/env-70`) | 0c2e43e « Fusion de devenv/env-70 (ENV-70 : SCION_REF 0.6.3.4, …) », poussé | oui |
| seed.scions | `master` | 929c01a « Fusion de devenv/env-70 (scion 0.6.3.4 …) » ; tag annoté `0.6.3.4` sur 473b653 ; `master`, tag et `devenv/env-70` poussés | oui |
| autres | graine `original-tree` 15740f9 | non touchée | oui |

Relever l'état réel de `main` et d'`origin/main` au début de la session suivante.

Outils (Mac) : Claude Code 2.1.330 ; scion **0.6.3.4** (pipx `git+file://<SEED_SCIONS>@0.6.3.4`,
10 modules identiques au tag) ; lepton 0.1.0 (ENV-68) ; extension 0.5.4 ; git 2.50.1 (et 2.18.0
sous `/usr/local/git/bin`, utilisé par l'audit). La VM est inchangée (scion 0.6.3.3).

## Fait pendant la session
Rapport : `rapports/env-70-scion.md` ; outils et relevés `rapports/env-70-scion/`.
- **Audit** 50b1012 (§1-2) :
  - D35 reproduit au Mac par git 2.18.0 : `warning:` avant `fatal:` (k01, k02) ;
  - même défaut avec git 2.50.1 sur `merge --ff-only` divergé (9 `hint:`) ;
  - D33 : graine hors version avancée ou lue sans message (g04, g06, g11, g13, g21) ;
  - 5 graines distantes du Mac à leur version ; branche de la graine de la VM jamais relevée.
- **PA-127** tranché (d8482cd), propositions du §3 retenues.
- **seed.scions** : tests a0521d9, D35 d987923 (`gitops.cause`), D33 a598cd8
  (`graft.cloned_seed_version`, contrôle dans `seed_updates`), version 473b653 ; 359 tests verts,
  1 sauté ; NF-2 0.
- **Essai** (§6) : seuls les cas visés changent ; fixtures 65 et 60 identiques ; 56 au chemin
  de base près.
- **Version** (§7) : tag, pipx ; `SCION_REF` lepton-tools 4e9e7ce, noyau e9b52e4 ; pytest 616.
- **PA-128** tranché ; essais `env-70-fixture`, `env-70-venv` supprimés par `supprimer-essai.sh` ;
  `HORS-PLAN.md` : D33, D35 traités ; publication des trois dépôts.

## Reste à faire dans l'étape
- Rien. En ENV-72 (consigne VM) :
  - scion 0.6.3.4 par `install-debian.sh` (défaut `SCION_REF`) ;
  - rejouer `rapports/env-70-scion/fixture.py` et les fixtures 56, 60, 65 (k07, f05 avec git
    2.47.3 : la cause `fatal⍽: La branche distante…` attendue, admise par
    `comparer-releves.py`) ;
  - relever la branche de `depots/lepton-seed.scions/original-tree` de chaque rootstock avant
    C3 (une graine hors version y est maintenant refusée par `graft-update`).

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-127 : D35 première ligne `fatal:`/`error:` (anglais, français), sinon première ligne non vide, toutes les commandes de `_run` | utilisateur | oui |
| PA-127 : D33 refus au texte de `version_fault`, code 1 ; graines `depots/<base de l'URL origin>/<version>`, branche ou tag ; graines par chemin ou sans `origin` non couvertes | utilisateur | oui |
| PA-127 : documentation, 0.6.3.4, `SCION_MIN_VERSION` inchangé, `SCION_REF` 0.6.3.4, aucun code de lepton, relevé de la graine en ENV-72 | utilisateur | oui |
| PA-128 : rapport accepté, écart compris (graine à tag vérifiée, jamais avancée) ; essais supprimés ; publication complète | utilisateur | oui |

## Pièges rencontrés
- Une graine à tag remise sur une branche encore au commit du tag passe `version_fault` : sans la
  règle « tag jamais avancé », `seed-update` l'aurait avancée au-delà du tag (trouvé par le test).
- `zsh` ne découpe pas une variable non protégée en mots : passer une liste de chemins par
  `xargs`, pas par `$VAR`.
- git 2.18.0 n'a pas `init -b` : `init` puis `symbolic-ref HEAD refs/heads/master`.
- Les fixtures d'ENV-56 listent les ancêtres du miroir : leur `.depots` change avec le chemin de
  la base (écart admis, sans cause scion).
- Un `rm -rf` sur un répertoire de sortie de la session lui-même : passer par
  `scripts/supprimer-essai.sh` même pour ses propres fichiers.

## Critères de validation
- [x] PA-127 et PA-128 tranchés et consignés.
- [x] Aucun nom propre à Lepton ajouté à scion : `git diff 0.6.3.3 -- scion tests | grep -ci '^+.*lepton'` → 0.
- [x] Tests de scion verts, dont les nouveaux (échec sur `master`, réussite sur la branche).
- [x] D35 : avec un stderr à avertissement d'abord (cas simulé, et réel par git 2.18.0), la cause paraît ; une seule ligne `erreur :`.
- [x] D33 : une graine clonée hors de sa version est refusée ; à sa version, elle avance comme avant.
- [x] Références de version conformes au PA-127 ; `pytest` de lepton-tools vert (616).
- [x] `HORS-PLAN.md` : D33 et D35 marqués traités, avec renvoi au rapport.

Tickets créés pendant la session : aucun. Lignes restées « ticket à créer après publication
d'ENV-70 » : aucune.

## Reprise
Commande ou première action de la session suivante :
```
démarre la session ENV-71 (lire handoff/env-70.md)
```
