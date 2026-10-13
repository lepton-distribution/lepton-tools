# Passation ENV-5 — Restructuration CMake du greffon noyau — session du 2026-10-13

## Statut
terminée — bibliothèques `kernel`, `lib`, `sbin`, `bin`, `bsp` et objets OBJECT liés à l'exécutif, lecteur de manifestes, HEX et occupation ; non-régression démontrée (PA-6).

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `devenv/env-5` (depuis `main` = bf95024, fusion locale de `devenv/env-4`) | `devenv(env-5): état et passation` | oui |
| clone noyau `depots/lepton/original/master` | `devenv/env-5` (depuis `master` = 49ed8fe, fusion locale de `devenv/env-4`) | e564714 `devenv(env-5): construction en bibliothèques kernel, lib, sbin, bin, bsp ; manifestes de greffons` | oui |
| seed.scions | `master` | e0adb2c | oui (non touché) |

`devenv/env-5` non fusionnée (fusions locales au début de la session suivante). Aucun push. Trunk
regreffé (4 027 feuilles), aucun fichier régulier hors `.scion.grafted.list`, aucun lien cassé.
`~/lepton/build/` : host et 14 presets croisés reconstruits à neuf sur e564714 (oracle après).

## Fait pendant la session
- Ouverture : fusions locales de `devenv/env-4` (lepton-tools bf95024, clone 49ed8fe).
- Oracle avant : `scripts/oracle/rejouer-oracle.sh` (nouveau, lepton-tools) → `rapports/oracles/env-5-avant/`
  (host + 14 presets ; fumée et banc KAL an386 ×4, an500 ×2). PA-5 tranché.
- Clone noyau (e564714) :
  - `cmake/components/kernel.cmake` : STATIC `kernel` (cœur, KAL, pilotes logiciels, VFS, FS, lwIP,
    `LEPTON_DEV_ARCH_SOURCES`), `lib`, `bsp` ; hôte : `kernel_posix` ; INTERFACE `lepton_kernel` (groupe).
  - `cmake/components/firmware.cmake` : OBJECT `generated`, `kernel_demarrage`, `bsp_objets` ; `sbin`, `bin` ;
    `lepton_greffons_appliquer()` ; `lepton.hex`, `lepton.occupation.txt` ; `enable_language(ASM)`.
  - Axes : `LEPTON_DEV_ARCH_SOURCES` / `LEPTON_BSP_SOURCES` / `LEPTON_BOARD_OBJECT_SOURCES` dans
    `cmake/boards/*.cmake` ; `LEPTON_FIRMWARE_SOURCES` et `LEPTON_BSP_NAME` supprimés ; `tests/kal` adapté.
  - `cmake/lepton_greffons.cmake` (lecteur), `sys/root/src/lepton-greffon.json` (noyau, valide au schéma),
    `tools/occupation/occupation.py`.
- Greffon d'essai sur copie du rootstock (BLD-2, FIC-4, CFG-3), puis retiré : `rapports/env-5-validation.md`.
- Oracle après `rapports/oracles/env-5-apres/` ; preuve du remplissage `rapports/env-5-preuve-remplissage.sh`,
  `env-5-contenu-sections.py`, `oracles/env-5-contenu/`. PA-6 tranché.
- lepton-tools : description de `schemas/greffon.schema.json` (emplacement du manifeste), skill
  `lepton-cibles` (sorties hex, occupation ; noms de cibles), `etapes/ENV-05-cmake.md` (CMake 3.24, nom du manifeste).

## Reste à faire dans l'étape
- Rien.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Oracle : host + 14 presets ; fumée et KAL an386 ×4, an500 ×2 ; pas de matériel | utilisateur | oui |
| Nom du manifeste `lepton-greffon.json` (graine `lepton-graine.json`) | utilisateur | oui |
| PA-5 : oracle avant validé | utilisateur | oui |
| Code de famille (`kernel/dev/arch`) dans `kernel` dès ENV-5 | utilisateur | oui |
| Manifestes BSP transitoires reportés à ENV-6 (amende « métadonnées seules ») | utilisateur | oui |
| Emplacement `sys/root/src/<destination>/lepton-greffon.json` | utilisateur (validé après proposition) | oui |
| PA-6 : non-régression validée, ENV-5 terminée, fusions au début de la session suivante | utilisateur | oui |
| Noms des OBJECT : `generated`, `kernel_demarrage`, `bsp_objets` (transitoire jusqu'à ENV-6) | proposition, appliquée | non (journal) |
| Version du manifeste noyau = `__LEPTON_VERSION` 4.10.0.2 (le `project(VERSION 4.9.0.2)` de CMake est périmé, non modifié) | proposition, appliquée | non |
| Lecteur : contrôle des seuls champs utilisés ; validation complète par check-jsonschema ; dépendance inconnue refusée ; `.cpp` refusé (pas de C++) | proposition, appliquée | non |
| Option privée du noyau posée sur les sources de `kernel`, `lib`, `sbin`, `bin`, `kernel_demarrage` (pas sur `generated`) | proposition, appliquée | non |
| Occupation : chaînes fusionnées attribuées à la première section qui les couvre ; remplissage non attribué | proposition, appliquée | non |
| `f746` : `dev_stm32f7xx_hal_tick.c` laissé dans `kernel` (archive), comme avant | proposition, appliquée (non-régression) | non |

## Pièges rencontrés
- `grep -r` ne suit pas les liens du trunk → chercher dans le clone, ou `grep -R`.
- Hook `proteger-trunk.py` : refuse aussi une commande visant `trunk/` d'une **copie** du rootstock → pour
  un essai, écrire dans un greffon déjà inscrit (`depots/generation/building`, local `*`), pas dans
  `.scion.grafted.list`.
- scion ne greffe que les greffons de `.scion.grafted.list` / du seed : un clone ajouté sous `depots/` est ignoré.
- `string(JSON)` : élément `""` d'un tableau perdu dans une liste CMake → traduit en « . ».
- `file(GLOB … CONFIGURE_DEPENDS)` ne suit pas le contenu d'un fichier → manifeste ajouté à `CMAKE_CONFIGURE_DEPENDS`.
- `target_compile_definitions(<bib> PRIVATE)` s'applique aussi aux sources ajoutées par un greffon à la même
  bibliothèque → options privées par propriété de source.
- MAP GNU ld : sections `.str1.1` listées avant fusion, plusieurs à la même adresse → compter l'union.
- Comparaison de sections entre arbres de chemins différents : `__FILE__` et `.debug_*` changent ; comparer
  dans une même copie (`env-5-preuve-remplissage.sh`).
- F746 : `.bss.eth_dma` aligné sur 16 Kio → la taille de `.bss` varie avec l'ordre d'édition de liens.
- macOS : `awk` sans `strtonum` → Python.

## Critères de validation
- [x] `cmake --build` réussit pour les presets QEMU, NUCLEO-F429ZI et NUCLEO-WL55JC1 (et les 14 croisés).
- [x] Cibles `kernel`, `lib`, `sbin`, `bin`, `bsp` et exécutif visibles (`cmake --build … --target help`).
- [x] Banc KAL et test de fumée QEMU identiques à l'oracle.
- [x] Ensemble des symboles de la MAP identique (aucun écart ; écarts de sections = remplissage, démontré).
- [x] Greffon d'essai (un `.c` + manifeste) compilé sans toucher aux `CMakeLists.txt` du noyau, puis retiré.
- [x] PA-5 et PA-6 tranchés.

## Reprise
```
cd /Users/cle_d_anton/lepton-tools-dev/lepton-tools && claude
# « Démarre la session sur l'étape indiquée dans DEVENV-STATUS » (ENV-6)
# au démarrage : fusion locale de devenv/env-5 → main (lepton-tools) et → master (clone noyau)
# ENV-6 : oracle avant par scripts/oracle/rejouer-oracle.sh (mêmes arguments qu'en env-5-validation.md) ;
#         manifestes BSP (destination kernel/dev/bsp/<carte>/), démarrage de carte en OBJECT, PA-7
```
