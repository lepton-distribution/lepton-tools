# Passation ENV-3 — Schémas — session du 2026-10-13

## Statut
terminée — trois schémas validés en PA-3 (avec amendement cpufs), exemples et script de validation conformes, spécification amendée.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `devenv/env-3` (non fusionnée ; `main` = dbbf03e, fusion locale de `devenv/env-2`) | commit `devenv(env-3): état et passation` | oui |
| clone noyau `depots/lepton/original/master` | `master` | 6b62af5 | oui (lecture seule) |
| seed.scions (`~/lepton-tools-dev/seed.scions`) | `master` | e0adb2c | oui (non touché) |

Aucun push. Trunk : aucun fichier régulier hors `.scion.grafted.list`.

## Fait pendant la session
- Fusion locale `devenv/env-2` → `main` (dbbf03e) ; branche `devenv/env-3`.
- `check-jsonschema` 0.38.2 installé par pipx ; xmllint libxml 2.15.4 (MacPorts) ; versions consignées.
- `schemas/greffon.schema.json` (draft 2020-12, types noyau, famille, bsp, application, bibliotheque ;
  champs requis / interdits par type ; options typées CFG-4 ; `compilation` CFG-3), commit 774e501.
- `schemas/graine.schema.json` (projet, noyau, bsp, applications, bibliotheques, backend,
  configurations, mklepton_xml), commit 774e501.
- `schemas/mklepton.xsd` format 2 (`version="2"` obligatoire, `<kernel>` en tête ; retirés `<target>`,
  `<arch>`, `<cpu>`, `cpufs block/option`), commits 774e501 et 133bcfc (cpufs `size`/`node` facultatifs).
- `schemas/exemples/` : 12 valides (noyau, 3 familles, 3 BSP an386 / F429ZI / WL55, application,
  bibliothèque, graine, 2 XML) ; `invalides/` : 28, chacun refusé pour la raison visée (motifs vérifiés).
- `scripts/valider-schemas.sh` : versions épinglées, méta-validation, valides / invalides, contrôle
  CFG-1 (noms communs JSON / XSD hors homonymes justifiés `max`, `type`, `version` ; aucun élément retiré
  dans le XSD) → `Conforme.`, code 0. Commit e3bc7fb.
- Essai hors dépôt : les 6 XML actifs du portage, migrés mécaniquement (déballage de `<target>`, retrait
  `<arch>`, `<cpu>`, `cpufs block/option`, ajout `version="2"`), valident tous le XSD.
- `SPECIFICATION.md` amendée (types avec Famille, GRF-2 CMake 3.24, GRF-3, CFG-8, BLD-1, décision 4),
  commit 6e1ef34, diff approuvé par l'utilisateur.

## Reste à faire dans l'étape
- Rien.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Fusion locale de `devenv/env-2`, `devenv/env-3` depuis `main` | utilisateur | oui |
| Type de greffon `famille` | utilisateur | oui |
| `<cpu freq>` et `include_absolute_path` hors XSD, dans le manifeste BSP (confirmation finale PA-4) | utilisateur | oui |
| `check-jsonschema` par pipx, version épinglée | utilisateur | oui |
| PA-3 : schémas validés | utilisateur | oui |
| PA-3 : cpufs — `block`/`option` retirés ; `size`/`node` absents ⇒ dimensionnement automatique (ENV-4) | utilisateur | oui |
| PA-3 : origine des greffons dans `.scion.sources.list` seul | utilisateur | oui |
| PA-3 : `abi_flottante`, `frequence_cpu`, `entete_config_noyau`, `compilation` retenus | utilisateur | oui |
| Amendement de `SPECIFICATION.md` | utilisateur | oui |
| Version de format XML `2` (format 1 = implicite, sans attribut) | proposition validée avec PA-3 | oui (PA-3) |
| Noms de fichiers `lepton-greffon.json` (racine `scion/` du greffon), `lepton-graine.json` (à côté de `.scion.sources.list`) : cités dans les `description` des schémas | proposition non validée explicitement — à confirmer en ENV-5 / ENV-8 | non |

## Pièges rencontrés
- Motif de chemin à anticipation (`(?!…)`) : remplacé par un motif sans anticipation pour rester
  portable entre validateurs (ECMA-262, Python, VSCodium).
- Contrôle CFG-1 purement lexical : faux positifs `max`, `type`, `version` → liste d'homonymes
  justifiés dans le script ; toute nouvelle entrée doit être justifiée.
- Non exprimable en JSON Schema, à contrôler par `lepton` (ENV-8) : défaut dans les bornes ou les
  valeurs d'une option, unicité des noms de configuration, cohérence `execution` qemu/carte avec le BSP.
- Les exemples BSP citent des chemins futurs (`debug/*.svd`, `vecteurs/*.c`, `debug/openocd-nucleo-f429zi.cfg`) :
  aucun SVD n'existe dans l'arbre ; à créer en ENV-6.
- zsh : `${PIPESTATUS[0]}` vide ; utiliser `$?` sans tube.

## Critères de validation
- [x] `scripts/valider-schemas.sh` : code 0 sur les valides, échec attendu sur chaque invalide.
- [x] Aucun champ présent à la fois dans le XSD et dans un schéma JSON (CFG-1).
- [x] Chaque champ rattaché à son exigence (`$comment` / `xs:annotation`).
- [x] PA-3 tranché.

## Reprise
```
cd /Users/cle_d_anton/lepton-tools-dev/lepton-tools && claude
# puis : « Démarre la session sur l'étape indiquée dans DEVENV-STATUS » (ENV-4 ; ENV-5 permutable)
# demander la base de devenv/env-4 (devenv/env-3 non fusionnée dans main)
# ENV-4 : implémenter version="2", retraits, cpufs automatique ; nouvelle référence d'empreintes = point d'arrêt
```
