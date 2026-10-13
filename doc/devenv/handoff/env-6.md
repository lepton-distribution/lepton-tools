# Passation ENV-6 — Greffons BSP de référence — session du 2026-10-13

## Statut
en cours — session 1 faite : PA-7 tranché, lecteur famille/BSP, lot QEMU (famille `qemu-mps2`, BSP
`qemu-mps2-an386` et `qemu-mps2-an500`) extrait, greffé et sans régression ; lots F4 et WL restent.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `devenv/env-6` (depuis `main` = 4d22d67, fusion locale de `devenv/env-5`) | `devenv(env-6): état et passation` | oui |
| clone noyau `depots/lepton/original/master` | `devenv/env-6` (depuis `master` = 1551afb, fusion locale de `devenv/env-5`) | cd53527 `devenv(env-6): nouvelle référence des empreintes mklepton (PA-7 Q5)` | oui |
| graine de travail `depots/lepton-seed.scions/original-tree` | `devenv/env-6` (depuis `original-tree` 083c30b) | f6f4805 `devenv(env-6): greffons famille qemu-mps2 et BSP …` | oui |
| `depots/lepton-famille/qemu-mps2` (nouveau) | `devenv/env-6` (sur `master` 516672f, vide) | 0927646 `devenv(env-6): manifeste lepton-greffon.json` | oui |
| `depots/lepton-bsp/qemu-mps2-an386` (nouveau) | `devenv/env-6` (sur `master` c2f6cc5, vide) | d979c6e `devenv(env-6): manifeste …, CMakeLists.txt …` | oui |
| `depots/lepton-bsp/qemu-mps2-an500` (nouveau) | `devenv/env-6` (sur `master` ef70a2e, vide) | eb52230 idem | oui |
| seed.scions | `master` | e0adb2c | oui (non touché) |

Aucun push. Trunk regreffé (4 032 feuilles, `.scion.grafted.list` à 5 lignes), aucun fichier régulier,
aucun lien cassé. `~/lepton/build/` : host et 14 presets croisés reconstruits à neuf sur cd53527.
`devenv/env-5` fusionnée (lepton-tools `main`, clone `master`) ; `devenv/env-6` non fusionnée.

## Fait pendant la session
- Ouverture : fusions locales de `devenv/env-5`, branches `devenv/env-6` (lepton-tools, clone, graine).
- Oracle avant `rapports/oracles/env-6-avant/` = `env-5-apres` (code 0 ×14 ; date seule).
- PA-7 : `rapports/env-6-extraction.md` (R1-R9, lots QEMU/F4/WL, Q1-Q12) validé par l'utilisateur.
- lepton-tools 1831232 : schéma (`compilation.<portée>.inclusions`, fichier dans `sources`, portée
  publique famille/BSP = tout l'exécutif), exemples, `valider-schemas.sh` conforme.
- Clone noyau : fa03c8e lecteur (`lepton_greffons_carte`, champs GRF-3, `LEPTON_MKCONF`, `bsp_demarrage`,
  `CMakeLists.txt` facultatif du BSP) ; 1fe7ac0 retrait mécanique ; 7942413 modules `cmake/boards/qemu-*`
  retirés, presets, `mklepton_empreintes.sh` (presets × manifestes BSP) ; cd53527 nouvelle référence.
- Greffons QEMU : import à l'identique (message citant fa03c8e), puis manifestes et `CMakeLists.txt`.
- Graine : 3 lignes `*` ; `scion seed-clone --seed depots/lepton-seed.scions/original-tree` (sans pull),
  `scion graft`.
- Non-régression : `rapports/env-6-validation.md` §Lot QEMU, `rapports/oracles/env-6-lot-qemu/`.

## Reste à faire dans l'étape
- [ ] Lot F4 (`env-6-extraction.md` §3) : trancher Q7 (BSP `nucleo-f439zi`) ; famille `stm32f4xx` (y compris
      `kernel/core/ucore/cmsis/Device/st/stm32f4xx`, vecteurs `nucleo_f439zi_vectors.c` → `vecteurs/`) ;
      BSP `nucleo-f429zi` ; presets renommés `nucleo-f429zi-*` ; `sources` par fichiers (Q2) et `inclusions`
      (Q1) ; `debug/gdbinit-lepton` générique (Q8) ; `debug/openocd-*.cfg` dans le BSP.
- [ ] Lot WL (§4) : famille `stm32wlxx` (remplaçant fort `dev_stm32wlxx_hal_tick.c`), BSP `nucleo-wl55jc1`
      (ABI soft, `stm32_radio_target/` déplacé : Q10 ; cfg OpenOCD générée et `board.radio` dans son
      `CMakeLists.txt`) ; séparation des vecteurs de `stm32wl55jci_nucleo_system.c` à confirmer.
- [ ] Fin d'étape : critères ci-dessous, recherche consignée pour F4 et WL, `DEVENV-STATUS.md`
      (cartes validées), fusions locales.
- [ ] Hors ENV-6, à planifier : extraction F746 et SAMD21 (Q9) ; mise à jour de `doc/migration/ajout-coeur.md`
      et `doc/BUILDING.md` du clone (chemins QEMU périmés) ; correction de la commande d'oracle de
      `rapports/env-5-validation.md` (forme à accolades refusée par le script).

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| ENV-6 par lots (QEMU, F4, WL) ; dépôts locaux sous `depots/`, version `*` ; graine sur `devenv/env-6` | utilisateur | oui |
| PA-7 : liste d'extraction et Q1-Q6, Q8-Q12 | utilisateur | oui |
| PA-7 Q7 : sort du BSP `nucleo-f439zi` | ouverte (début du lot F4) | oui |
| OBJECT `bsp_demarrage` lié par `lepton_link_firmware` (exécutif et banc KAL) ; `bsp_objets` à l'exécutif seul | proposition, appliquée | oui (à confirmer) |
| Destination de la famille `qemu-mps2` : `kernel/dev/arch/cortexm/qemu-mps2` (R3) ; exemple du schéma aligné | utilisateur (R3 validée) | oui |
| Commentaire d'en-tête de `qemu_mps2_board.c` réécrit à nombre de lignes constant (`__LINE__`) | proposition, appliquée | non |
| Sorties de `mklepton_empreintes.sh` des cartes BSP nommées `<mkconf>-<carte>` | proposition, appliquée | non |
| `host.mklepton_format` utilise l'en-tête du BSP an386 (le test hôte dépend du greffon BSP greffé) | proposition (rapport PA-7), appliquée | non |
| `kernelconf.h:68,126` (identifiant et nom `uname` d'an386) laissés dans le noyau | proposition, appliquée (signalé) | non |

## Pièges rencontrés
- `rejouer-oracle.sh` : un `--qemu`/`--carte` par preset ; la forme `--qemu a b c` → « argument inconnu ».
- `kal_bench` ne lie pas `bsp_objets` : un démarrage de carte qui y passerait disparaîtrait du banc KAL →
  `bsp_demarrage` lié par `lepton_link_firmware`.
- `objcopy -O binary --only-section` d'une section non chargée → fichier vide ; utiliser `--dump-section`.
- zsh : `set -- $var` ne découpe pas ; `echo =====` est une expansion ; passer par `bash -c`.
- mklepton ne vérifie pas l'existence de l'en-tête de carte (chemin seulement recopié dans `kernel_mkconf.h`).
- an386 et an500 partagent le XML mais plus l'en-tête : sortie de `mklepton_empreintes.sh` par carte.
- Fumée : la position de `rcv SIGCHLD` varie d'une exécution à l'autre ; ce n'est pas un écart.
- Pièges ENV-5 toujours valables (`grep -r` et liens, hook et copie du rootstock, `string(JSON)` et `""`).

## Critères de validation
- [x] PA-7 tranché.
- [ ] Trois greffons BSP, manifestes valides (`scripts/valider-schemas.sh`) — QEMU fait (an386, an500 + famille) ; F429ZI, WL55JC1 à faire.
- [ ] Plus aucun fichier propre à ces cartes dans le greffon noyau (recherche consignée) — QEMU fait (`env-6-validation.md`).
- [ ] Construction des trois presets réussie ; QEMU identique à l'oracle — QEMU fait.
- [x] Trunk sans fichier régulier ; `scion ungraft && scion graft` sans erreur (après le lot QEMU).

## Reprise
```
cd /Users/cle_d_anton/lepton-tools-dev/lepton-tools && claude
# « Démarre la session sur l'étape indiquée dans DEVENV-STATUS » (ENV-6, lot F4)
# rester sur devenv/env-6 partout (pas de fusion) ; référence = rapports/oracles/env-6-lot-qemu/
# PA-7 Q7 d'abord ; liste F4 revérifiée par : ninja -C ~/lepton/build/nucleo-f439zi-embos -t deps
```
