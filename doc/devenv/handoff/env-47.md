# Passation ENV-47 — Famille STM32F7 : copie remplacée par la projection — session du 2026-11-10

## Statut
Terminée. La HAL F7 (`v1.3.3`) et le CMSIS device F7 (`v1.2.10`) sont maintenant projetés par scion
depuis deux miroirs neufs. Les binaires sont identiques et le banc F746 donne 20/20 en embOS comme en
FreeRTOS. PA-81 et PA-82 sont tranchés, et tout est publié.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` | fusion de `devenv/env-47` ; `main` et la branche poussés | oui |
| `family-stm32f7xx` | `master` | 12280a5 Fusion de devenv/env-47 (HAL v1.3.3 et CMSIS device v1.2.10 F7 projetés…, PA-82). Branche a13b162, poussée | oui |
| clone noyau `depots/lepton/original/master` | `master` | 76f28bd, non touché | oui |
| autres | `master` / `original-tree` | non touchés : F4 acdd24c, WL 2340b25, BSP F746 6266908, WL55 4d7cf80, an386 10a8889, graine 15740f9, seed.scions 7e8a0cc | oui |
| miroirs GitHub | — | `lepton-distribution/mirror-stm32f7xx-hal-driver`, `mirror-cmsis_device_f7` : publics, égaux à l'amont | — |

État de `<ROOTSTOCK>` :
- liens : 3887, avec les mêmes chemins qu'avant (`c65ee399…`) ;
- cibles : liste `chemin -> cible` `70cc91c2…`, dont 407 projetées (F4 206, F7 201) ;
- 0 lien cassé, 0 fichier régulier ;
- liste greffée : 18 entrées ;
- clones tiers F7 : `depots/tiers/stm32f7xx-hal-driver/v1.3.3` (e1446fa) et
  `depots/tiers/cmsis-device-f7/v1.2.10` (2352e88), origine = miroirs ;
- `lepton check` code 0 ; tous les clones sont sur `master` et propres.

Outils : scion 0.6.2.0 et lepton 0.1.0 (code inchangé). La VM a scion 0.6.1.0 (ENV-50).

Oracle de référence Mac : `oracles/env-47-apres/`. Ses binaires sont identiques à ceux
d'`env-46-apres`, mais 201 cibles du trunk ont changé.

Cartes : en fin de session, seule la STM32F746G-DISCO est branchée, sur `/dev/cu.usbmodem1454303`.
Elle porte l'image `stm32f746g-disco-freertos` du banc. Le câble Ethernet est sur la F746.

## Fait pendant la session
- **Audit** (rapport §1) :
  - la copie F7 est égale aux tags amont : 196 + 5 fichiers OK (`verifier-import.sh`) ;
  - les noms suivis par git correspondent aux attendus d'ENV-38, casse comprise ;
  - lepton, l'extension et le hook sont génériques.
- **PA-81** : rapport §1.8.
- **Miroirs** (§2) :
  - `gh repo create` des deux dépôts ; 2 lignes ajoutées à la graine de publication ;
  - `mirror-sync --seed` : 9 et 8 références envoyées ; seconde passe à 0 ;
  - `ls-remote` des miroirs = amont.
- **Oracle avant** (§4) : code 0 ×16 contre `env-46-apres`.
- **Bascule** (§5) :
  - 4 commits dans la famille ;
  - contrôles conformes sur la copie d'essai, le rootstock neuf et `<ROOTSTOCK>` (PA-P) ;
  - rootstock à graine de projet (§3) : `seed lock` et `--verify` reconnaissent les clés F7.
- **lepton-tools** : 637e7f6, aide de `verifier-import.sh`.
- **Contrôles** (§6) :
  - oracle après : code 0 ×16 ; KAL, fumée et `ctest -N` identiques ;
  - F746 20/20 ×2, réseau compris (ping 3/3, `LIST` 13, `RETR` 57 octets).
- **PA-82** : publication et suppression des essais.
- `HORS-PLAN.md` B1 : le F7 est traité.

## Reste à faire dans l'étape
- [x] Rien.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-81 : lignes du `scion/.scion/` (tags `v1.3.3`, `v1.2.10`), miroirs publics créés par la session, synchronisation E13 (PA-P) | utilisateur | oui |
| PA-81 : provenances conservées et réécrites, description du manifeste réécrite, chemins inchangés | utilisateur | oui |
| PA-81 : aucune modification de lepton ; aide de `verifier-import.sh` ; rootstock de projet `env-47-projet` | utilisateur | oui |
| PA-11 : flash F746 (embOS et FreeRTOS) | utilisateur | oui |
| PA-P : bascule de `<ROOTSTOCK>` (`fetch`, `--ff-only`, `seed-clone`, `graft`) | utilisateur | oui |
| PA-82 : publication complète (famille puis lepton-tools), référence `env-47-apres`, 4 essais supprimés | utilisateur | oui |
| Provenances : en-têtes « Exige scion ≥ 0.6.1.0 » (minimum technique, comme le F4), alors que lepton exige 0.6.2.0 | proposition de la session (forme du PA-69, acceptée au PA-81) | rapport §1.7 |

## Pièges rencontrés
- **`lepton seed new --origin`** attend le **nom** du greffon (`stm32f7xx=…`), pas sa clé scion
  (`family-stm32f7xx=…`). Sinon : « origine du BSP … absente », code 1, sans rien créer.
- **`lepton file owner -C <rootstock>`** résout un chemin relatif depuis le répertoire courant, pas
  depuis le trunk. Il faut lui donner le chemin absolu du trunk.
- **`git merge -F -`** ne lit pas l'entrée standard. Il faut écrire le message dans un fichier,
  et enchaîner les fusions et les push sous `set -euo pipefail` (incident du §6.6 du rapport).
- **Rootstock neuf** : 11 cibles diffèrent de `<ROOTSTOCK>`, celles des fichiers propres à la
  famille, car le clone y est rangé sous `devenv/env-47`. C'est attendu.
- **Graft** : « 26 chemins ignorés par git », tous des `.DS_Store`.
- **`mirror-sync` depuis la graine de publication** : la forme est `scion mirror-sync rootstock
  --seed graine`, depuis `essais/env-40-publication/`. Le premier argument est le rootstock, qui
  n'est pas un parent du répertoire courant.

## Critères de validation
- [x] PA-81 et PA-82 tranchés et consignés.
- [x] Miroirs F7 créés, égaux à l'amont.
- [x] Binaires identiques (code 0) ; liste des chemins identique, aux écarts accordés près (aucun).
- [x] Plus aucun fichier de la HAL ni du CMSIS device F7 dans le clone `family-stm32f7xx`.

## Rootstocks à regreffer en ENV-50
Tous ont aujourd'hui la famille F7 en `master` d2d9aa9. Un `graft-update` avance la famille à
12280a5 et crée les 2 clones tiers F7 depuis les miroirs. Il réoriente alors 201 cibles, sans
ajouter ni retirer de chemin. Il exige scion ≥ 0.6.1.0.
- Mac : `essais/env-13-vierge`, et `essais/env-41-vierge` s'il est gardé.
- VM : `essais/env-28-debian` et `essais/env-43-debian`, après l'installation de scion 0.6.2.0.
- Copies d'étape `env-34-copie`, `env-35-copie`, `env-37-copie`, `env-39-copie` : hors des regreffes.

## Reprise
Commande ou première action de la session suivante :
```
démarre la session ENV-48 (skill devenv-session) ; référence oracles/env-47-apres ; méthode et
scripts de rapports/env-47-f7-projection.md ; rebrancher les deux WL55 (banc radio)
```
