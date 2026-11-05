# Passation ENV-35 — Famille STM32F4 : passage de la SPL à la HAL — session du 2026-11-05

## Statut
terminée — famille STM32F4 et BSP `nucleo-f429zi`, `nucleo-f439zi` sur la HAL v1.8.5, SPL hors
compilation, NUCLEO-F429ZI 20/20 réseau compris ; fusionnés et poussés (PA-58).

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` (après fusion) | fusion de `devenv/env-35` (voir `git log`) ; `main` et `devenv/env-35` poussées | oui |
| `family-stm32f4xx` (`depots/lepton/family-stm32f4xx/master`) | `master` | 0fd8b2a « Fusion de devenv/env-35 … » ; `master` et `devenv/env-35` poussées | oui |
| `bsp-nucleo-f429zi` | `master` | b9fe2bf « Fusion de devenv/env-35 … » ; poussées | oui |
| `bsp-nucleo-f439zi` | `master` | 314f91b « Fusion de devenv/env-35 … » ; poussées | oui |
| clone noyau `depots/lepton/original/master` | `master` | 2893297 (non touché) | oui |
| graine, seed.scions, autres greffons | — | non touchés | oui |

`<ROOTSTOCK>` : 3978 liens, 0 cassé, aucun fichier régulier hors `.DS_Store`, `lepton check` 0.
Compile : host et les 16 presets construits à neuf (oracle `env-35-apres`, nouvelle référence).
Carte : image `nucleo-f429zi-embos` d'ENV-35 en flash sur la NUCLEO-F429ZI.

## Fait pendant la session
- Audit (rapport §1) : 13 unités seulement voient un en-tête ST (famille + `nucleo_f439zi_board.c`,
  `audit/hscan-*.tsv`) ; table SPL → HAL/registres ; coexistence SPL/HAL non démontrée
  (`audit/coexistence/resume.tsv`) ; `core_cm4.h` 5.9.0 impossible à placer devant V3.30 sans
  toucher le noyau ; collision `GPIO_MODE_AF_*`.
- PA-57 tranché (rapport §2, `DEVENV-STATUS.md` §Décisions).
- Oracle avant `env-35-avant` = `env-34-apres` ; banc de référence F429 20/20 ×3 (§3).
- Implémentation en un lot (§4) : famille 5 commits, BSP 2 commits chacun ;
  `scripts/tiers/hal_conf_stm32f4.py` ; copie d'essai `essais/env-35-copie`, puis `<ROOTSTOCK>`.
- Oracle après (§5.1) : code 0 sur host et 12 presets ; F4 : 89 symboles SPL/ETH retirés, ajouts
  HAL et pilotes, plus aucun symbole SPL ; `ctest -N` 17/17 ; IRQ fortes (K8).
- Occupation (§5.2) : `.text` +0,84 % (embOS) / +0,30 % (FreeRTOS), SRAM −1,2 %, CCM inchangée.
- Cartes (§5.3) : 20/20 en `nucleo-f429zi-embos`, `-freertos` et `nucleo-f439zi-embos` (en
  `STM32F439xx`, sur F429), ping 3/3, LIST 13, RETR identique.
- `verifier-import.sh` : HAL 200 et CMSIS device 6 identiques, 0 écart (§5.4).
- PA-58 : écarts ETH acceptés, fusions et push.

## Reste à faire dans l'étape
- [ ] Rien. Non fait, signalé au PA-58 : lecture des registres dans la vue des périphériques sous
      VSCodium sur la F429 (SVD désigné et présent ; contrôle graphique non réalisé).

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-57 : architecture mixte, modules HAL, USART par registres, un seul lot, `STM32F439xx`, SPL hors compilation et 4 fragments supprimés, `core_cm4.h` V3.30, critère d'occupation, générateur dans lepton-tools, cartes, hôte 192.168.2.10 (corrigé de .20) | utilisateur | oui |
| PA-58 : écarts ETH E-A (MAC dérivée de l'UID), E-B (PHY adresse 0 fixe), E-C (init à l'ouverture) acceptés ; nouvel oracle ; fusions et push | utilisateur | oui |
| Nom `dev_stm32f4xx_eth_map` gardé dans le BSP pour ne pas modifier le XML mklepton du noyau | choix d'implémentation dans le cadre du PA-57, présenté au PA-58 | rapport §4.2 |
| Critère d'ENV-36 C4 (compilation à blanc : `cmsis5` 0 échec, `v330` identique au Mac) | proposition non validée (rapport ENV-34 §5.3) | non |

## Pièges rencontrés
- La SPL modifiée (`driverlib/stm32f4xx.h`) incluait `kernelconf.h` : sans elle, `gpio.c` ne voyait
  plus `_GPIO_DEFAULT_SPEED` → inclusion explicite de `kernel/core/kernelconf.h`.
- `types.h` de la famille pose `#pragma pack(4)` sans le retirer : inclure `stm32f4xx_hal.h` avant.
- La copie d'essai a ses propres clones : resynchroniser (`rsync -a --delete` des clones touchés)
  puis `scion graft` dans la copie avant chaque construction.
- `git rm` indexe tout de suite : un `git commit` suivant emporte la suppression ; séparer avant.
- Script de banc : un chemin d'oracle relatif est perdu après `cd` dans le trunk (`banc-carte.sh`
  le rend absolu).
- `en0` porte 192.168.2.10 ; 192.168.2.20 figure dans le `.init` de la carte (second argument
  de `net/ifconfig addif`), ce n'est pas l'adresse de l'hôte.
- VMware Fusion actif : la sonde F429 restait visible du Mac ; à revérifier avant tout banc.

## Critères de validation
- [x] PA-57 et PA-58 tranchés et consignés.
- [x] Aucun fichier SPL compilé pour les 4 presets F4 ; `USE_STDPERIPH_DRIVER` absent.
- [x] NUCLEO-F429ZI 20/20 en embOS et en FreeRTOS, réseau compris.
- [x] Binaires inchangés hors F4 (code 0 sur 12 presets et host).
- [x] Aucun fichier de la HAL ni du CMSIS device modifié (règle D1a ; contrôle
      `verifier-import.sh` d'ENV-34).

## Reprise
Commande ou première action de la session suivante :
```
démarre la session   # ENV-36 : lire handoff/env-35.md, consigne consignes/env-36-debian.md, PA-59
```
