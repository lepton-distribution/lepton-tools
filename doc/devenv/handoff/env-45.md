# Passation ENV-45 — Sonde choisie par numéro de série — session du 2026-11-10

## Statut
terminée — tout BSP à champ `openocd` choisit sa sonde par `LEPTON_BOARD_PROBE_SERIAL` ; bancs verts
avec cinq sondes branchées ensemble ; PA-77 et PA-78 tranchés, tout est publié.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` | fusion de `devenv/env-45` (poussée, ainsi que la branche) | oui |
| clone noyau `depots/lepton/original/master` | `master` | 6a56d4c Fusion de devenv/env-45 (…LEPTON_BOARD_PROBE_SERIAL, PA-78) ; branche 36ef800 poussée | oui |
| `bsp-nucleo-wl55jc1` | `master` | 4d7cf80 Fusion de devenv/env-45 (sonde par le lecteur du noyau) ; branche 93ddcec poussée | oui |
| autres (BSP F429 b9fe2bf, F439 314f91b, F746 6266908, SAMD21 f3cffa2, an386 10a8889 ; familles ; graine 15740f9 ; seed.scions 7e8a0cc) | `master` / `original-tree` | non touchés | oui |

`<ROOTSTOCK>` : 3983 liens, 0 lien cassé, aucun fichier régulier hors tolérés ; `lepton check`
code 0 ; tous les clones sur `master`. Aucune regreffe (aucun fichier ajouté).

Outils : scion 0.6.2.0, lepton 0.1.0 (code inchangé). VM : scion 0.6.1.0 (ENV-50).

Oracle de référence Mac : `oracles/env-45-apres/` (binaires identiques à `env-44-apres`).

Cartes : les cinq sur le Mac, branchées ensemble. Images `lepton` embOS en flash sur F429, F746,
SAMD21, WL55 A ; WL55 B porte `nucleo-wl55jc1-freertos`.

## Fait pendant la session
- **Audit** (rapport §1) : seul le WL55 choisissait sa sonde ; consommateurs de
  `LEPTON_BOARD_OPENOCD_CFG` et de l'ancien nom ; cinq sondes relevées (§1.7), EDBG accepte
  `adapter serial` (OpenOCD 0.12.0, sur la carte) ; défaut reproduit : sans numéro, la cfg F429
  prend le ST-LINK du F746.
- **PA-77** (§1.8).
- **Oracle avant** : code 0 ×16 contre `env-44-apres`, mklepton identiques, host 7/7, KAL et
  fumée identiques, `ctest -N` 17/17.
- **Noyau** (36ef800) : `_lepton_sonde_cfg` dans `cmake/lepton_greffons.cmake` ; cfg générée
  seulement si le numéro est posé (`echo` du numéro, `source {cfg BSP}`, `adapter serial`) ; contrôle
  du format ; alias `LEPTON_BOARD_STLINK_SERIAL` (`DEPRECATION`) ; `LEPTON_BOARD_OPENOCD_CFG_BSP`.
- **BSP WL55** (93ddcec) : mécanisme propre retiré ; cfg de la paire sur `LEPTON_BOARD_OPENOCD_CFG_BSP`.
- **lepton-tools** : skill `lepton-cibles` (34ddabe), README, `banc-wl55.sh` au nouveau nom,
  `env-45-sonde/banc-sonde.sh` et `bancs.sh` (7f50880) ; pytest 362.
- **Oracle après** : code 0 ×16 contre l'avant, tout identique.
- **Bancs à cinq sondes** (§4.2) : F429 20/20 ×2, F439 sur F429 20/20, F746 19/19 ×2, SAMD21
  embOS 15/15, FreeRTOS KAL 14/14 (fumée E-5 héritée d'ENV-19), WL55 16/16 ×2 radio comprise.
- **Numéro faux** (§4.3) : « No device matches the serial string », init en échec, code 1, aucune
  écriture.
- **PA-78** : publication (noyau, WL55, lepton-tools) ; `HORS-PLAN.md` B4 traité.

## Reste à faire dans l'étape
- [x] Rien.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-77 : forme générique, `LEPTON_BOARD_PROBE_SERIAL`, alias transitoire de l'ancien nom, deux réglages (construction, éditeur), F439 par son image sur la F429, `echo` du numéro dans la cfg, flash autorisé sur les cinq cartes | utilisateur | oui |
| PA-78 : publication complète ; nouvel oracle de référence `env-45-apres` | utilisateur | oui |
| `LEPTON_RADIO_PEER_STLINK_SERIAL` (paire radio WL55) gardé sous ce nom | utilisateur (option retenue au PA-77) | oui |
| Retrait de l'alias `LEPTON_BOARD_STLINK_SERIAL` : à une étape future, non planifié | proposition non validée | non |
| ENV-50 : la consigne R50-1 relève les numéros des sondes de la VM et passe `LEPTON_BOARD_PROBE_SERIAL` | proposition non validée | non |

## Pièges rencontrés
- **Ports série** : ils ont changé depuis la skill (topologie USB). Les relever à chaque banc :
  `ioreg -lrw0 -c IOUSBHostDevice | grep -E '"USB Serial Number"|"IOCalloutDevice"'`.
- **zsh** : `echo ====` échoue (`=mot` est développé en chemin de commande) ; une variable qui
  contient une liste n'est pas découpée (`${=Q}` ou liste écrite en clair).
- **SAMD21 FreeRTOS** : la fumée échoue toujours (E-5 d'ENV-19). Le banc KAL se passe par
  `ctest -L board -FS board_t0 -E board.smoke_lsh`.
- **`git rev-parse --short a b`** : refuse plusieurs révisions (`--short` implique `--verify`).

## Critères de validation
- [x] PA-77 et PA-78 tranchés et consignés.
- [x] Chaque BSP de carte visé choisit sa sonde par numéro ; bancs F429, F746, SAMD21 et WL55 verts
      avec plusieurs sondes branchées ; `nucleo-f439zi` selon le PA-77.
- [x] Binaires identiques (code 0).
- [x] Variable vide : comportement inchangé.

## Reprise
Commande ou première action de la session suivante :
```
démarre la session ENV-46 (ou ENV-47, permutables) (skill devenv-session) ; bancs sur carte avec
-DLEPTON_BOARD_PROBE_SERIAL=<n°> (DEVENV-STATUS §Emplacements, « Sondes des cartes »)
```
