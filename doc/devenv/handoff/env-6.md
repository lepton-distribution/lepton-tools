# Passation ENV-6 — Greffons BSP de référence — session du 2026-10-13 (session 2, lot F4)

## Statut
en cours — sessions 1 et 2 faites : PA-7 tranché (Q7 compris), lots QEMU et F4 extraits, greffés et sans
régression ; reste le lot WL et la fin d'étape.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `devenv/env-6` (depuis `main` = 4d22d67) | `devenv(env-6): état et passation` (session 2) | oui |
| clone noyau `depots/lepton/original/master` | `devenv/env-6` (depuis `master` = 1551afb) | e0895ee `devenv(env-6): nouvelle référence des empreintes mklepton (lot F4, PA-7 Q5)` | oui |
| graine de travail `depots/lepton-seed.scions/original-tree` | `devenv/env-6` (depuis `original-tree` 083c30b) | 268c0e8 `devenv(env-6): greffons famille stm32f4xx et BSP nucleo-f429zi (dépôts locaux)` | oui |
| `depots/lepton-famille/qemu-mps2` | `devenv/env-6` | 0927646 (inchangé en session 2) | oui |
| `depots/lepton-bsp/qemu-mps2-an386` / `-an500` | `devenv/env-6` | d979c6e / eb52230 (inchangés) | oui |
| `depots/lepton-famille/stm32f4xx` (nouveau) | `devenv/env-6` (sur `master` 1c3d789, vide) | fc8b5b9 `devenv(env-6): manifeste lepton-greffon.json (…)` | oui |
| `depots/lepton-bsp/nucleo-f429zi` (nouveau) | `devenv/env-6` (sur `master` a279c7a, vide) | 702adda `devenv(env-6): manifeste lepton-greffon.json, CMakeLists.txt (…), gdbinit de carte` | oui |
| seed.scions | `master` | e0adb2c | oui (non touché) |

Aucun push. Trunk regreffé (4 034 feuilles, `.scion.grafted.list` à 7 lignes), aucun fichier régulier,
aucun lien cassé. `~/lepton/build/` : host et 14 presets croisés reconstruits à neuf sur e0895ee ;
`build/nucleo-f439zi-*` supprimés (presets renommés `nucleo-f429zi-*`). Aucune fusion de `devenv/env-6`.

## Fait pendant la session
- PA-7 Q7 tranché par l'utilisateur : BSP `nucleo-f439zi` reporté après ENV-6 ; presets renommés.
- Liste F4 revérifiée (`ninja -t deps`) : identique à `env-6-extraction.md` §3.
- Famille `stm32f4xx` : import à l'identique depuis cd53527 (3ef8e46), manifeste (fc8b5b9).
- BSP `nucleo-f429zi` : import (7203f76), manifeste, `CMakeLists.txt`, gdbinit de carte (702adda).
- Clone noyau : c34d53e retrait (mécanique) ; 78878f9 module `cmake/boards/nucleo-f439zi.cmake` retiré,
  presets, lecteur `openocd`, `debug/gdbinit-lepton`, `ci/run.sh`, exemples `tests/*.py` ; e0895ee
  référence mklepton (contre-épreuve faite).
- Graine 268c0e8 ; `scion ungraft`, `seed-clone --seed …`, `scion graft` ; `ungraft && graft` final.
- Non-régression : `rapports/env-6-validation.md` §Lot F4, `rapports/oracles/env-6-lot-f4/` : 12 presets
  code 0 ; F429ZI ×2 : `.debug_line`/`.debug_str` +12 (chemin des vecteurs, démontré) ; fumée et banc KAL
  identiques ; host 7/7 ; avertissements en même nombre.
- lepton-tools 053cc43 : skill `lepton-cibles` (presets, chemins OpenOCD/gdbinit du BSP).

## Reste à faire dans l'étape
- [ ] Lot WL (`env-6-extraction.md` §4) : famille `stm32wlxx` (remplaçant fort `dev_stm32wlxx_hal_tick.c`,
      CMSIS device `st/stm32wlxx`), BSP `nucleo-wl55jc1` (ABI soft, `stm32_radio_target/` déplacé : Q10 ;
      `board.radio` et cfg OpenOCD générée dans son `CMakeLists.txt`) ; séparation des vecteurs de
      `stm32wl55jci_nucleo_system.c` à confirmer ; `debug/gdbinit-nucleo-wl55jc1` et
      `debug/openocd-nucleo-wl55jc1.cfg` dans le BSP. La cfg générée doit poser `LEPTON_BOARD_OPENOCD_CFG`
      après le lecteur (le `CMakeLists.txt` du BSP est inclus après `lepton_greffons_carte`).
- [ ] Fin d'étape : critères ci-dessous, `DEVENV-STATUS.md` (cartes validées), fusions locales.
- [ ] Hors ENV-6, à planifier : BSP `nucleo-f439zi` (Q7) ; extraction F746 et SAMD21 (Q9) ;
      `kernel/usb/stm32f4-usb-core/` et démos FreeRTOS F4 (signalés) ; table de vecteurs F4 complète avant
      un second BSP F4 ; `doc/migration/ajout-coeur.md`, `doc/BUILDING.md` du clone (chemins QEMU et F4
      périmés) ; commande d'oracle de `rapports/env-5-validation.md` (forme à accolades).

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-7 Q7 : BSP `nucleo-f439zi` reporté après ENV-6 ; presets `nucleo-f429zi-*` | utilisateur | oui |
| Lecteur : `openocd` → `LEPTON_BOARD_OPENOCD_CFG`, un seul fichier jusqu'à ENV-9 | proposition (plan accepté), appliquée | oui (à confirmer) |
| Famille : `mcu` = `STM32F429xx` seul ; `STM32F429xx`, `HSE_VALUE`, `__tauon_cpu_device__` dans le BSP ; `USE_STDPERIPH_DRIVER` et inclusions dans la famille ; inclusion du répertoire BSP abandonnée (inutile, binaires identiques) | proposition (plan accepté), appliquée | non (détail du manifeste) |
| Noms de fichiers du BSP conservés (R3) | utilisateur (R3 validée) | oui |
| `.DS_Store` non suivi supprimé du clone noyau (répertoire `stm32f4xx` vidé) | proposition, appliquée | non |
| USB F4 et démos FreeRTOS F4 laissés dans le noyau ; vecteurs liés par symbole au BSP | signalé, à décider plus tard | oui |
| OBJECT `bsp_demarrage` (session 1) | proposition, appliquée | oui (à confirmer) |

## Pièges rencontrés
- Hook `proteger-trunk.py` : une commande shell qui écrit hors du trunk mais dont le texte contient
  `…/trunk/…` est refusée (faux positif) → écrire ces fichiers avec l'outil Edit/Write (chemin réel contrôlé).
- `mklepton_empreintes.sh --mklepton` attend l'exécutable `build/host/mklepton` (fichier), pas un répertoire.
- Fumée : le chiffre qui suit `rcv SIGCHLD` préfixe parfois l'invite (`6lepton#2$`) ; à neutraliser avec la
  position de `rcv SIGCHLD`.
- zsh : `echo ######` provoque une erreur de motif ; utiliser `printf`.
- Pièges de la session 1 toujours valables (`rejouer-oracle.sh` un drapeau par preset, `kal_bench` et
  `bsp_objets`, `objcopy --dump-section`, mklepton sans contrôle d'existence de l'en-tête).

## Critères de validation
- [x] PA-7 tranché (Q7 compris).
- [ ] Trois greffons BSP, manifestes valides (`scripts/valider-schemas.sh`) — QEMU et F429ZI faits ; WL55JC1 à faire.
- [ ] Plus aucun fichier propre à ces cartes dans le greffon noyau (recherche consignée) — QEMU et F4 faits (`env-6-validation.md`).
- [ ] Construction des trois presets réussie ; QEMU identique à l'oracle — QEMU et F4 faits.
- [x] Trunk sans fichier régulier ; `scion ungraft && scion graft` sans erreur (après le lot F4).

## Reprise
```
cd /Users/cle_d_anton/lepton-tools-dev/lepton-tools && claude
# « Démarre la session sur l'étape indiquée dans DEVENV-STATUS » (ENV-6, lot WL)
# rester sur devenv/env-6 partout (pas de fusion) ; référence = rapports/oracles/env-6-lot-f4/
# liste WL revérifiée par : ninja -C ~/lepton/build/nucleo-wl55jc1-embos -t deps
```
