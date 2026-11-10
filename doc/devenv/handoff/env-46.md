# Passation ENV-46 — Famille STM32F4 : retrait de la SPL — session du 2026-11-10

## Statut
terminée — 96 fichiers retirés de `family-stm32f4xx` : la SPL, l'Ethernet et le SPI écrits sur elle,
et le CMSIS device V3.x F4. Les binaires sont identiques. PA-79 et PA-80 sont tranchés, et tout est
publié.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` | fusion de `devenv/env-46`, poussée, ainsi que la branche | oui |
| clone noyau `depots/lepton/original/master` | `master` | 76f28bd Fusion de devenv/env-46 (note datée…, PA-80) ; branche 44e3e9c poussée | oui |
| `family-stm32f4xx` | `master` | acdd24c Fusion de devenv/env-46 (retrait de la SPL…, PA-80) ; branche 3503e42 poussée ; tag annoté `avant-retrait-spl` sur 7afd7f1, poussé | oui |
| autres (BSP F429 b9fe2bf, F439 314f91b, WL55 4d7cf80, an386 10a8889 ; familles F7 d2d9aa9, WL 2340b25 ; graine 15740f9 ; seed.scions 7e8a0cc) | `master` / `original-tree` | non touchés | oui |

État de `<ROOTSTOCK>` :
- 3887 liens, soit 3983 − 96 ; 0 lien cassé ; aucun fichier régulier hors
  `.scion.grafted.list` ;
- `lepton check` code 0 ;
- tous les clones sur `master`, propres ;
- regreffe faite par `scion graft --scion lepton@family-stm32f4xx`. Après la fusion, la famille est
  repassée sur `master`, avec le même arbre : trunk inchangé.

Outils : scion 0.6.2.0, lepton 0.1.0 (code inchangé). VM : scion 0.6.1.0 (ENV-50).

Oracle de référence Mac : `oracles/env-46-apres/`. Ses binaires sont identiques à ceux
d'`env-45-apres`, mais le trunk a 96 chemins de moins.

Cartes : NUCLEO-F429ZI, WL55 A et WL55 B sont visibles par USB ; F746 et SAMD21 ne le sont pas. La
F429 porte l'image `nucleo-f429zi-freertos` de l'oracle après.

## Fait pendant la session
- **Audit** (rapport §1) :
  - quatre lots : a. `driverlib/` (68) ; b. Ethernet sur la SPL (4) ; c. SPI sur la SPL (4) ;
    d. CMSIS V3.x F4 (20) ;
  - aucun des 16 presets n'inclut ces fichiers (`ninja -t deps`) ;
  - les dépendants hors plan sont tous dans le clone noyau. 6 fichiers de BSP sont déjà cassés
    depuis ENV-35 (`stm32f4xx_hal_gpio_ex.h`) ;
  - `USART_ChangeBaudrate` : son calcul existe déjà dans `uart.c` (`uart_set_brr`) ;
  - `stm32f4-usb-core` dépend de la HAL, pas de la SPL.
- **PA-79** : rapport §1.8.
- **Oracle avant**, contre `env-45-apres` : code 0 ×16 ; KAL, fumée et mklepton identiques ;
  host 7/7 ; `ctest -N` 17/17.
- **Retrait** :
  - lepton-tools 8683faa : schéma et exemple ;
  - famille : tag, puis 0ffae44 (`git rm`, 96 fichiers) et 3503e42 (manifeste ; vecteurs à nombre
    de lignes constant) ;
  - noyau 44e3e9c : une ligne datée dans `MIGRATION-STATUS.md`, rien de réécrit ;
  - regreffe ciblée (PA-P).
- **Contrôles** (§4) :
  - chemins disparus = les 96 retirés, au nom exact ; 0 chemin apparu ; cibles des autres
    inchangées ;
  - oracle après code 0 ×16 ; KAL, fumée et `ctest -N` identiques ;
  - rootstock neuf `essais/env-46-vierge` identique à `<ROOTSTOCK>` (même SHA-256, contenu
    identique), `lepton check` 0 ;
  - F429 20/20 en embOS et en FreeRTOS, réseau compris, identiques à ENV-45 ;
  - pytest 362 ; `valider-schemas.sh` conforme.
- **PA-80** : publication dans l'ordre famille, noyau, lepton-tools ; essais supprimés.
- `HORS-PLAN.md` : A3 (dépendants inventoriés) et B3 (traité).

## Reste à faire dans l'étape
- [x] Rien.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-79 : périmètre 96 fichiers (lots a à d) | utilisateur | oui |
| PA-79 : dépendants hors plan laissés avec des inclusions cassées, inventoriés (A3) | utilisateur | oui |
| PA-79 : `USART_ChangeBaudrate` perdue ; tag annoté `avant-retrait-spl` | utilisateur | oui |
| PA-79 : documents (manifeste, commentaire des vecteurs, schéma et exemple, note datée dans `MIGRATION-STATUS.md` du noyau sans réécriture) | utilisateur | oui |
| PA-P : `scion graft --scion lepton@family-stm32f4xx` | utilisateur | oui |
| PA-11 : flash F429 pour deux bancs, embOS et FreeRTOS | utilisateur | oui |
| PA-80 : publication complète ; référence `env-46-apres` ; essais supprimés | utilisateur | oui |
| Note de migration placée en dernière ligne du tableau « Décisions actées » de `MIGRATION-STATUS.md`, et non sous « Blocages et dette », la section qui termine le fichier | proposition de la session (forme d'une ligne datée) | journal |

## Pièges rencontrés
- **Fichiers ISO-8859** de la famille : un `grep` en UTF-8 les saute sans le signaler. Il faut
  `LC_ALL=C grep -a`.
- **Ninja absorbe les `.d`** : aucun `.d` ne reste dans les constructions. Il faut lire
  `ninja -C <build> -t deps` (entrées `VALID` ou `STALE`).
- **Nombre d'objets** d'un preset de carte : il dépend de `LEPTON_BOARD_SERIAL_PORT`, qui ajoute
  `kal_bench`. Ne pas comparer un répertoire de banc à un répertoire d'oracle.
- **Doc de migration du noyau** : elle est « arrêtée au 2026-10-06 » (`CLAUDE.md` du noyau,
  `ETAPE-8` §4). On ajoute une ligne datée, on ne corrige pas en place.
- **Clone famille d'un rootstock neuf** : il est rangé sous le nom de la version,
  `depots/lepton/family-stm32f4xx/devenv/env-46`, pas sous `…/master`.

## Critères de validation
- [x] PA-79 et PA-80 tranchés et consignés.
- [x] Plus aucun fichier de la SPL dans `family-stm32f4xx`, dans le périmètre retenu.
- [x] Binaires identiques (code 0).
- [x] Dépendants hors plan traités selon le PA-79 et inscrits au rapport et dans `HORS-PLAN.md` A3.

## Reprise
Commande ou première action de la session suivante :
```
démarre la session ENV-47 (skill devenv-session) ; référence oracles/env-46-apres ; bancs sur carte
avec -DLEPTON_BOARD_PROBE_SERIAL=<n°> (DEVENV-STATUS §Emplacements, « Sondes des cartes »)
```
ENV-50 : la regreffe des rootstocks d'essai et de la VM retire 96 liens de la famille F4.
