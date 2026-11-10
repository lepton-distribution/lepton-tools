# Passation ENV-48 — Famille STM32WL : copie remplacée par la projection — session du 2026-11-10

## Statut
Terminée. Le code tiers WL est maintenant projeté par scion depuis quatre miroirs neufs :
- HAL `v1.3.0` ;
- CMSIS device `v1.1.1` ;
- SubGHz_Phy `v1.3.0` ;
- utilitaires et `utilities_def.h` de STM32CubeWL `v1.3.0`.

Les binaires sont identiques, et le banc WL55 A/B donne 16/16 en embOS comme en FreeRTOS, radio
comprise. PA-83 et PA-84 sont tranchés, et tout est publié.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` | fusion de `devenv/env-48` ; `main` et la branche poussés | oui |
| `family-stm32wlxx` | `master` | dfaf331 Fusion de devenv/env-48 (… projetés par scion depuis les miroirs …, PA-84). Branche 205387c, poussée | oui |
| clone noyau `depots/lepton/original/master` | `master` | 76f28bd, non touché | oui |
| autres | `master` / `original-tree` | non touchés : F7 12280a5, F4 acdd24c, WL55 4d7cf80, graine 15740f9, seed.scions 7e8a0cc | oui |
| miroirs GitHub | — | `lepton-distribution/mirror-stm32wlxx-hal-driver`, `mirror-cmsis-device-wl`, `mirror-stm32-mw-subghz-phy`, `mirror-STM32CubeWL` : publics, complets (`main` + tous les tags), égaux à l'amont | — |

État de `<ROOTSTOCK>` :
- liens : 3888, chemins `2d317c4b…`. C'est l'état d'avant, avec −8 `LICENSE.txt` et
  +9 `LICENSE.md` (C2) ;
- cibles : liste `chemin -> cible` `c3e20325…`, dont 627 projetées (F4 206, F7 201, WL 220) ;
- 0 lien cassé, 0 fichier régulier ;
- liste greffée : 23 entrées ;
- clones tiers WL : `depots/tiers/stm32wlxx-hal-driver/v1.3.0`, `cmsis-device-wl/v1.1.1`,
  `stm32-mw-subghz-phy/v1.3.0`, `stm32cubewl/v1.3.0`. Le dernier est partagé par
  `stm32cubewl::utilities` et `::radio-core-inc` ;
- `lepton check` code 0 ; tous les clones sont sur `master` et propres.

Outils :
- scion 0.6.2.0, inchangé ;
- lepton 0.1.0, avec le correctif 2a8900a, réinstallé par pipx depuis `devenv/env-48` ;
- la VM a toujours scion 0.6.1.0 (ENV-50).

Oracle de référence Mac : `oracles/env-48-apres/`. Ses sections et symboles sont identiques à ceux
d'`env-48-avant` sur les 16 presets.

Cartes : les deux NUCLEO-WL55JC1 sont branchées, avec l'image `nucleo-wl55jc1-freertos`.
- A 002700253431510837393937 : `/dev/cu.usbmodem1454303` ;
- B 004F003E3431510937393937 : `/dev/cu.usbmodem145103`.

Les ports sont **inversés** depuis ENV-45 §1.7 : il faut les relever par `ioreg` à chaque banc.

## Fait pendant la session
- **Audit** (rapport §1) :
  - la copie est égale aux tags amont ;
  - essai à blanc conforme sur une copie d'essai (3887 chemins, 618 projetés, casse, clone
    partagé ; `--purge` est refusé sur ce clone) ;
  - aucun défaut de scion ;
  - défaut de lepton : la propriété dans un clone partagé ne respectait pas P-G3 ;
  - STM32CubeWL : miroir complet faisable (63 Mo), extraction d'environ 360 Mo (§1.6) ;
  - C1 (§1.7), C2 (§1.8).
- **PA-83** : rapport §1.11 et §1.12.
- **Miroirs** (§2) :
  - `gh repo create` ×4 ;
  - 4 lignes ajoutées à la graine de publication `essais/env-40-publication/`, qui en compte 8 ;
  - `mirror-sync --seed` : 9, 7, 7 et 9 références envoyées ; seconde passe à 0 ;
  - `ls-remote` des miroirs = amont.
- **Oracle avant** (§3) : code 0 ×16 contre `env-47-apres`.
- **lepton-tools** (§4.1) :
  - 2a8900a : `projection_tables` et `_owner_of` attribuent le lien d'un clone partagé d'après
    les motifs du porteur ; 15 tests ; 377 réussis ;
  - 2403711 : aide de `verifier-import.sh`.
- **Famille** (§4.2) : 8 commits :
  - le porteur `scion/.scion/` (34 lignes) ;
  - 5 commits mécaniques `git rm` (4 ensembles, plus les `LICENSE.txt`) ;
  - les provenances et le manifeste ;
  - le commentaire de `dev_stm32wlxx_util_timer.c`.
- **Bascule** (§4.2 à §4.5) : conforme sur la copie d'essai, le rootstock neuf `env-48-vierge`,
  le rootstock de projet `env-48-projet` (`seed lock` et `--verify` reconnaissent les 5 clés WL)
  et `<ROOTSTOCK>` (PA-P). L'espace de travail généré est inchangé.
- **Contrôles** (§5) :
  - oracle après : code 0 ×16 ; KAL, fumée, mklepton et `ctest -N` identiques ;
  - WL55 16/16 ×2 ; radio 20/20 A→B et B→A, ping-pong 20/20.
- **PA-84** (§5.6) : publication, 5 essais supprimés, `HORS-PLAN.md` (B1, C1, C2 traités ; D11).

## Reste à faire dans l'étape
- [x] Rien.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-83 : lignes du porteur (5 clés, tags, miroirs), aucun correctif de scion | utilisateur | oui |
| PA-83 (PA-P) : 4 miroirs publics créés par la session, STM32CubeWL complet, synchronisation par la graine de publication | utilisateur | oui |
| PA-83 : lepton corrigé dans l'étape (P-G3, clone partagé) | utilisateur | oui |
| PA-83 : C1, provenance avec raison « probable, non établie » ; commentaire de `dev_stm32wlxx_util_timer.c` corrigé | utilisateur | oui |
| PA-83 : C2, 8 `LICENSE.txt` retirés, 9 `LICENSE.md` projetés (écarts accordés −8, +9) | utilisateur | oui |
| PA-83 : provenances réécrites, manifeste, aide du script, bascule et rootstock de projet ; PA-11 pour les deux WL55 | utilisateur | oui |
| PA-84 (PA-P) : référence `env-48-apres`, publication (famille puis lepton-tools), essais supprimés, `HORS-PLAN.md` | utilisateur | oui |
| Commentaire de `dev_stm32wlxx_util_timer.c` réécrit avec le même nombre de lignes (numéros de ligne du débogage inchangés) | proposition de la session (mise en œuvre de C1) | rapport §4.2 |
| Mise à jour de la version : les deux clés `stm32cubewl::*` changent ensemble (même clone) ; `stm32_hal_legacy.h` et `stm32_timer.h` sont à reporter à la main | proposition de la session (texte des provenances) | rapport §4.2 |

## Pièges rencontrés
- **Ports des WL55 inversés** depuis ENV-45 : A est sur `…1454303`, B sur `…145103`. La lecture
  d'`ioreg` doit associer `IOCalloutDevice` au dernier `USB Serial Number` vu, car le port est
  dans un nœud enfant.
- **Empreintes des binaires** : elles diffèrent d'un oracle à l'autre même sans aucune
  modification (`env-47-apres` → `env-48-avant` : 16/16). Seul le code de `comparer-oracle.py`
  compte. Le banc, qui reconstruit dans le même arbre, retrouve des empreintes identiques.
- **`graft-remove` d'une clé projetée** : un `graft` complet ne la rend pas, car la liste greffée
  fait foi. Il faut `seed-clone`, puis `graft`.
- **Rootstock neuf** : 24 cibles diffèrent de `<ROOTSTOCK>`, celles des fichiers propres à la
  famille, car le clone y est rangé sous `devenv/env-48`. C'est attendu.
- **zsh** : `set -- $var` ne découpe pas les mots ; passer par `bash -c`. Dans un `bash -c '…'`,
  une apostrophe du message de commit casse la citation : écrire les messages dans des fichiers.
- **`--origin`** de `lepton seed new` attend le nom du greffon (`stm32wlxx=…`), comme en ENV-47.

## Critères de validation
- [x] PA-83 et PA-84 tranchés et consignés.
- [x] Binaires identiques (code 0) ; liste des chemins identique, casse comprise, aux écarts
  accordés près (−8 `LICENSE.txt`, +9 `LICENSE.md`).
- [x] Ne restent dans la famille que les fichiers modifiés ou hors amont, et la provenance
  (10 fichiers sous les 4 ensembles).
- [x] `RadioIsChannelFree` documentée dans la provenance (C1) ; C2 tranché et appliqué.

## Rootstocks à regreffer en ENV-50
Tous ont aujourd'hui la famille WL en `master` 2340b25. Un `graft-update` avance la famille à
dfaf331 et crée les 4 clones tiers WL depuis les miroirs (STM32CubeWL : environ 360 Mo). Il
réoriente 211 cibles, retire 8 chemins et en ajoute 9. Il exige scion ≥ 0.6.1.0.
- Mac :
  - `essais/env-13-vierge` ;
  - `essais/env-41-vierge`, s'il est gardé ;
  - `essais/env-11/wl55jc1` (graine de projet `env11wl`, nouveau dans la liste).
- VM : `essais/env-28-debian` et `essais/env-43-debian`, après l'installation de scion 0.6.2.0.
  Il faut aussi installer lepton depuis `main` (correctif 2a8900a) avant les contrôles de
  `seed status` et `file owner`.
- Copies d'étape `env-34-copie`, `env-35-copie`, `env-37-copie`, `env-39-copie` : hors des regreffes.

## Reprise
Commande ou première action de la session suivante :
```
démarre la session ENV-49 (skill devenv-session) ; référence oracles/env-48-apres ; porteur
family-stm32wlxx/master/scion/.scion/ ; méthode et scripts de rapports/env-48-wl-projection.md
(attendu-apres.py, bancs.sh) ; relever les ports des WL55 par ioreg avant le banc
```
