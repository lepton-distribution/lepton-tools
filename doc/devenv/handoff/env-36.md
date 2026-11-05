# Passation ENV-36 — Validation Debian groupée (ENV-34 et ENV-35) — session du 2026-11-05

## Statut
terminée — ordre R36-1 : C1 à C7 conformes sur Debian 13.7, première carte (NUCLEO-F429ZI) sur la
VM ; 7 rootstocks d'essai du Mac regreffés ; fusionnée et poussée (PA-60).

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` (après fusion) | fusion de `devenv/env-36` (voir `git log`) ; `main` et `devenv/env-36` poussées ; `devenv/env-36-debian` 683b911 (VM) poussée, fusionnée | oui |
| clone noyau `depots/lepton/original/master` | `master` | 2893297 (non touché) | oui |
| famille, BSP, graine, seed.scions | — | non touchés (têtes : famille F4 0fd8b2a, F429 b9fe2bf, F439 314f91b, graine 15740f9, scion 0.5.4.0) | oui |

`<ROOTSTOCK>` : non regreffé (déjà aux têtes publiées), 3978 liens. Rootstocks d'essai du Mac :
aux têtes publiées, `check` 0 (`qemu-gra2` 1, attendu). VM : `essais/env-28-debian` (3978 liens),
`essais/env-36-debian` (rootstock neuf), `essais/env-11/qemu`, `~/env-36-journaux` conservés ;
`essais/env-33-debian` et `~/env-33-journaux` supprimés. Carte : NUCLEO-F429ZI rattachée au Mac,
image `nucleo-f439zi-embos` construite sur la VM en flash.

## Fait pendant la session
- Tâche 1 : écarts `env-32-apres` → `env-35-apres` (4 presets F4 seuls) ; attendus versionnés
  `rapports/env-36-mac/attendu/` (liens ajoutés 215 et retirés 194, écarts F4 réduits aux noms) ;
  têtes publiées ; consigne `consignes/env-36-debian.md` (C1-C7, §10 banc carte en commandes
  claires) ; `rapports/env-36-mac.md` §1.
- PA-59 (§2 du rapport Mac), push de `devenv/env-36`, ordre R36-1 envoyé en entier.
- Tâche 2 (VM) : `FIN-SUCCÈS R36-1`, `rapports/env-36-debian.md`, `oracles/env-36-debian/`.
- Tâche 4 : comparaisons refaites sur l'oracle poussé (`rapports/env-36-mac.md` §4) : 12 presets 0,
  4 F4 = attendu, `f429→f439` hors `.debug_*` 0, compilation à blanc et carte conformes.
- Tâche 3 : 7 rootstocks regreffés (`rapports/env-36-mac.md` §5, journaux
  `~/lepton-tools-dev/essais/env-36-mac/`) ; `env-11/f429zi` construit, 0 écart de symboles.
- PA-60 : `.noinit` admis, fusions, push.

## Reste à faire dans l'étape
- [ ] Rien. Le plan ENV-0 à ENV-36 est réalisé ; la suite est à décider avec l'utilisateur.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-59 : consigne validée, C4 et C5 retenus (C4 = proposition d'ENV-34, désormais validée), carte F429 sur la VM (PA-11, 3 images), VM en pont, IP confirmée par l'utilisateur (192.168.2.20), nettoyage, push, R36-1 | utilisateur | oui |
| PA-60 : écart `.noinit` FreeRTOS F4 admis (bourrage `ALIGN(0x8)`) ; fusions et push | utilisateur | oui |
| Regreffe des 7 rootstocks d'essai (PA-P) | utilisateur | oui (journal, PA-60) |
| Lecture du critère C2 « 0 lien sous `stm32f4xx/cubemx_hal_driver/` » (157 liens WL hors sujet) | session Mac, sur constat vérifié ; reprise au PA-60 | oui |

## Pièges rencontrés
- `banc-carte.sh` d'ENV-35 appelle `caffeinate` (macOS) → commandes en clair dans la consigne VM.
- `grep -c cubemx_hal_driver/` compte aussi la famille WL (157 liens) → restreindre à
  `stm32f4xx/`.
- La synthèse de `board_net` est dans `LastTest.log` (`carte-detail.log`), pas dans
  `board_net.log` (console série).
- Bourrage d'alignement : `.noinit` (sans symbole) peut passer de 0 à 4 selon la chaîne ; comparer
  `.bss + .noinit`.
- Push de la VM : deux refus GitHub « fatal error in commit_refs_rules », réussi au troisième
  essai (erreur passagère probable).
- Une construction F4 dans un autre rootstock que `<ROOTSTOCK>` diffère de l'oracle en
  `.debug_line`/`.debug_str` (chemins des sources) : attendu.
- Le premier `ACCUSÉ` de la VM a été perdu (ECONNRESET) et renvoyé.

## Critères de validation
- [x] PA-59 et PA-60 tranchés et consignés.
- [x] `FIN-SUCCÈS R36-1` vérifié par la session Mac ; C1 à C6 conformes (et C7, ajouté au PA-59).
- [x] Rootstocks d'essai regreffés : 0 lien cassé, 0 fichier régulier (hors `.DS_Store` tolérés) ;
      `check` code 0 (`qemu-gra2` : 1, attendu).

## Reprise
Commande ou première action de la session suivante :
```
démarre la session   # aucune étape planifiée : décider de la suite (révision du plan, lepton-portage-instructions)
```
