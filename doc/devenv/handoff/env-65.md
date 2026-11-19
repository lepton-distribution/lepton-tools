# Passation ENV-65 — scion : clone existant hors version, message de `git clone` (D25, D22) — session du 2026-11-19

## Statut
Terminée. scion 0.6.3.3 corrige D25 et D22, ce que prouvent les tests et les essais au Mac.
PA-117 et PA-118 sont tranchés. Rapport : `rapports/env-65-scion.md`. La preuve sur la VM se
fera en ENV-66.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` : fusion `--no-ff` de `devenv/env-65` (depuis `main` f715f87) ; `main` et `devenv/env-65` poussées (PA-P, accord de l'utilisateur) | branche : « devenv(env-65): état et passation » ; `main` : commit de fusion | oui |
| seed.scions | `master` 49ca4ae (fusion `--no-ff` de `devenv/env-65`), tag annoté 0.6.3.3 sur 9615cd5 ; `master`, tag et `devenv/env-65` poussés | « Fusion de devenv/env-65 (scion 0.6.3.3 : …) » | oui |
| clone noyau `depots/lepton/original/master` | `master` 2b4a647 (fusion `--no-ff` de `devenv/env-65`, e589b63 `SCION_REF` 0.6.3.3) ; `master` et `devenv/env-65` poussés | « Fusion de devenv/env-65 (ENV-65 : SCION_REF 0.6.3.3, …) » | oui |
| autres | graine `original-tree` 15740f9 | non touchée | oui |

Outils :
- Mac : scion **0.6.3.3** (pipx, `git+file://<SEED_SCIONS>@0.6.3.3`, 10 modules identiques au
  tag) ; lepton 0.1.0, non réinstallé (seuls un commentaire et une docstring ont changé) ;
  extension 0.5.3 ; git 2.50.1 ; Claude Code 2.1.328.
- VM : rien n'a été fait dans cette étape. Elle garde scion 0.6.3.2, le lepton d'ENV-61 et
  l'extension 0.5.2 jusqu'à ENV-66.
- `<ROOTSTOCK>` n'est pas regreffé : 0 lien cassé, et 9 `.DS_Store` du Finder tolérés, datés du
  12 et du 18 novembre.

## Fait pendant la session
- Audit (rapport §1-2) :
  - `env-65-scion/inventaire.py` sur les 8 rootstocks du Mac : 65 clones, 2 graines distantes,
    1 orphelin, **0 hors version** ;
  - `env-65-scion/fixture.py` :
    - D25 : `seed-clone` et `graft` donnent le code 0 sur un clone hors de sa version
      (a03 à a05, b01, b02, c01, c02) ; une graine distante déplacée ou préexistante est lue
      telle quelle (d02, d04) ;
    - D22 : messages et stderr complets de git (`*.git-err`).
- Fixtures d'ENV-56 et d'ENV-60 rejouées avec 0.6.3.2 (`fixture56-avant/`, `fixture60-avant/`).
- PA-117 (rapport §3-4) ; puis, dans seed.scions :
  - tests d'abord (eaf0c85 : 27 nouveaux tests, 18 en échec sur 0.6.3.2,
    `tests-avant-correction.txt`) ;
  - D25 (a87cdb5) ;
  - D22 (026d4be) ;
  - version 0.6.3.3 (9615cd5).
  Résultat : **340** tests verts, NF-2 à 0.
- Essais (rapport §6), avec le venv de la branche :
  - fixtures `*-apres/` : D25 refusé, cas non visés identiques au texte D22 près ;
  - lepton (`env-65-scion/essai.sh`) : `seed add` sur un clone préexistant hors version est
    refusé et annulé ; avant, code 0 et greffe fausse ;
  - succès F7 (`succes-0633/`) identique à 0.6.3.2.
- Version :
  - tag, pipx ;
  - `SCION_REF` 0.6.3.3 : lepton-tools 420b2f5, noyau e589b63 ;
  - pytest de lepton-tools : **567**.
- `HORS-PLAN.md` : D22 et D25 traités ; D33 ajouté (graines de `seed-update` et `graft-update`
  non comparées à une version). Aucun ticket : seed.scions n'y est pas éligible.
- Essais supprimés par `scripts/supprimer-essai.sh`. Publication (PA-118).

## Reste à faire dans l'étape
- Rien.
- Pour ENV-66 (VM) :
  - scion 0.6.3.3 par `install-debian.sh` du noyau `master` 2b4a647 (défaut `SCION_REF`) ;
  - rejouer les trois fixtures, `python3 -I rapports/env-65-scion/fixture.py <seed.scions>
    <scion> <base> <sortie>` et celles d'ENV-56 et d'ENV-60, contre `env-65-scion/fixture*-apres/`
    (`LC_ALL=C` dans `fixture.py` et `env-60-scion/fixture.py` ; pas dans `env-56-scion/fixture.py`,
    d'où le français de git sur la VM, que `scripts/comparer-releves.py` ramène) ;
  - n04 touche le réseau (`scion-essai.invalid`) : sur la VM, son texte en français
    (`impossible d'accéder à '%s'⍽: %s`) n'est pas dans `TRADUCTIONS` ;
  - `essai.sh` : recréer un dépôt `env65lib` (`lepton scion new … --no-seed --no-cmake -C <copie>`,
    puis une branche `dev` qui ajoute `DEV.txt`) ;
  - `inventaire.py` sur les rootstocks de la VM (lecture seule).

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Plan de session : branches `devenv/env-65` (seed.scions, lepton-tools ; noyau si `SCION_REF` change), arrêts PA-117, PA-118, PA-P | utilisateur | oui |
| PA-117 : refus au texte de `_check_clone` ; clones adoptés par `seed-clone` et graine existante de `seed-add` ; `graft`, clone déjà greffé et graines de `seed-update`/`graft-update` non couverts (D33) ; clé projetée exclue ; D22 première ligne non vide, `--quiet`, toutes les commandes, stderr sous `-v` ; 0.6.3.3 ; `SCION_MIN_VERSION` inchangé, `SCION_REF` 0.6.3.3 ; aucun code de lepton | utilisateur | oui |
| PA-118 : rapport accepté ; essais supprimés ; fusions et push (seed.scions et tag, noyau, lepton-tools) | utilisateur | oui |
| Message du refus : « N clone(s) existant(s) hors de leur version déclarée, non repris (liste greffée et clones inchangés) : … » ; graine : « graine existante hors de la version demandée, non reprise (rien n'a été modifié) : … » | session (texte d'implémentation, exposé au rapport §5-6, accepté au PA-118) | oui (rapport) |

## Pièges rencontrés
- Le git d'Apple n'est pas traduit (`LC_ALL=fr_FR.UTF-8` donne l'anglais). Le français de la VM
  se lit dans `po/fr.po` v2.47.3. « '%s' does not appear to be a git repository » n'y figure pas :
  le message reste en anglais derrière `fatal⍽: ` (déduction, à vérifier en ENV-66).
- La liste greffée sépare ses colonnes par des blancs, pas par des tabulations (`model.fields`).
  La première version de `inventaire.py` ne lisait aucun clone.
- Les graines de projet de lepton (`depots/lepton-seed/<projet>`) n'ont pas d'`origin` : elles
  sont données par un chemin, sans version. Ce ne sont pas des graines distantes clonées.
- `test_git_messages.py` lancé seul : il faut importer `support` avant `scion` (`sys.path`).
- zsh ne découpe pas une variable non citée en mots : écrire les boucles d'essai en bash.
- Le chemin du venv pipx contient une espace (`Library/Application Support`) : citer les chemins.

## Critères de validation
- [x] PA-117 et PA-118 tranchés et consignés.
- [x] Aucun nom propre à Lepton ajouté à scion :
      `git diff 0.6.3.2 -- scion tests | grep -ci '^+.*lepton'` → 0.
- [x] Tests de scion verts, nouveaux compris (échec sur `master`, réussite sur la branche).
- [x] k18 et k05 suivent le PA-117 (b01, c01, d02, d04 refusés). Il ne reste aucune greffe fausse
      d'un clone adopté. Un clone déjà greffé puis déplacé (a03, f03) reste greffé, par décision
      du PA-117.
- [x] Message D22 : la cause donnée par git paraît ; une seule ligne `erreur :`.
- [x] Références de version conformes au PA-117 ; `pytest` de lepton-tools vert.
- [x] `HORS-PLAN.md` : D22 et D25 marqués traités, avec renvoi au rapport.

Tickets créés pendant la session : aucun. Lignes de `HORS-PLAN.md` restées « ticket à créer après
publication d'ENV-65 » : aucune.

## Reprise
Commande ou première action de la session suivante :
```
démarre ENV-66 avec la skill devenv-session
```
