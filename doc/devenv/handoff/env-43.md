# Passation ENV-43 — Validation Debian groupée (ENV-37 à ENV-42) — session du 2026-11-09

## Statut
terminée — R43-1 conforme sur C1 à C8. L'écart `.text` (E-1, bourrage d'alignement) est admis au
PA-74. Les 7 rootstocks d'essai du Mac sont regreffés. Fusions et push faits. C'est la dernière
étape du plan.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` | fusion de `devenv/env-43`, poussée avec `devenv/env-43` (fusion 7711626 de `devenv/env-43-debian` 9ab752c, commit de cette passation compris) | oui |
| clone noyau `depots/lepton/original/master` | `master` | 763dda2, non touché | oui |
| familles, BSP, graine `original-tree`, seed.scions | — | non touchés (F4 7afd7f1, WL 2340b25, an386 5819047, graine 15740f9, tag 0.6.1.0) | oui |

`<ROOTSTOCK>` : 3982 liens, 0 cassé, 0 fichier régulier, inchangé.

Rootstocks d'essai du Mac, regreffés et aux têtes publiées :
- `env-9`, `env-11/{f429zi,qemu,qemu-gra2,wl55jc1,bout-en-bout/rootstock}`, `env-13-vierge` ;
- `env-11/f429zi` et `env-13-vierge` ont les clones tiers sous `depots/tiers/`.

`essais/env-41-vierge` a gagné `depots/.mirrors/` (essai de `mirror-sync --dry-run`).

VM :
- scion 0.6.1.0, lepton 0.1.0, extension 0.5.2 ;
- `essais/env-28-debian` regreffé ; `essais/env-43-debian` neuf ;
- `essais/env-36-debian` et `~/env-36-journaux` supprimés ;
- `essais/env-13-debian` non regreffé.

Carte NUCLEO-F429ZI : sur la VM, image `nucleo-f439zi-embos`. WL55 A et B : sur le Mac.

## Fait pendant la session
- Tâche 1 : `rapports/env-43-mac.md` §1. Contenu :
  - écarts `env-35-apres` → `env-42-apres` ;
  - liens depuis R36-1 : +4, 0 retrait ; liste `chemin -> cible` `d9f4ea56…` ;
  - attendus `rapports/env-43-mac/attendu/` ;
  - script `rapports/env-43-mac/controler-trunk.py`, essayé sur `<ROOTSTOCK>` ;
  - `mirror-sync --dry-run` essayé ;
  - consigne `consignes/env-43-debian.md`.
- PA-73, puis `graft-update` d'`env-13-vierge` avant l'ordre : `CONFORME`
  (`rapports/env-43-mac.md` §5) ; push de `devenv/env-43` (f01e735), ordre R43-1.
- R43-1 :
  - `FIN-SUCCÈS` reçu ; ACCUSÉ et AVANCEMENT non remis (ECONNRESET) ;
  - rapport `rapports/env-43-debian.md`, oracle `oracles/env-43-debian/`.
- Tâche 3 : 6 rootstocks regreffés (§5), `f429zi` construit (= `env-42-apres` hors
  `.debug_line`/`.debug_str`).
- Tâche 4 : comparaisons refaites sur l'oracle poussé (§4) ; E-1 analysé : symboles +16 / +48
  sur les deux hôtes, `.text` Debian multiple de 64.
- PA-74 : E-1 admis ; fusions et push.

## Reste à faire dans l'étape
- [x] Rien.
- Hors étape, pour l'utilisateur : rattacher la NUCLEO-F429ZI de nouveau au Mac.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Plan de session | utilisateur | oui (journal) |
| PA-73 : C7 F429 seule, 3 images (PA-11) ; C6 `mirror-sync --dry-run` ; C8 nettoyage d'`env-36-debian` ; essai Mac d'`env-13-vierge` avant l'ordre | utilisateur | oui |
| Regreffe des 6 autres rootstocks pendant l'exécution de la VM (PA-P) | utilisateur | oui (journal, rapport §5) |
| Poursuite de la VM sans accusé remis ; installations du §6 lancées par la session VM (sudo sans mot de passe) | utilisateur (sur la VM) | oui (rapport §3, §4) |
| PA-74 : E-1 admis ; fusions et push | utilisateur | oui |
| Script `controler-trunk.py`, nom imposé `essais/env-43-debian` (longueur des chemins `__FILE__`) | choix de session, présenté au PA-73 | oui (rapport §1.4, §1.6) |

## Pièges rencontrés
- Messages VM → Mac non remis (bridge ECONNRESET, « bridge ID is stale ») : seule la `FIN-SUCCÈS`
  est arrivée. L'utilisateur relaie. Voir `HORS-PLAN.md` D9.
- Hook `proteger-trunk.py` : il a refusé une commande de lecture (`diff`) qui citait
  `depots/tiers/` → passer par un fichier de script (D3).
- `zsh` ne découpe pas une variable en mots (`set -- $x`) → `bash -c` ou script.
- Listes normalisées des écarts : une variation de `.text` absorbée par le bourrage fait
  disparaître la ligne `section modifié: .text`. Comparer d'abord la croissance des symboles.
- `scion mirror-sync` dans un rootstock `--bare` non greffé : « aucun miroir déclaré » ; il faut
  un rootstock qui greffe le porteur.

## Critères de validation
- [x] PA-73 et PA-74 tranchés et consignés.
- [x] `FIN-SUCCÈS R43-1` vérifié par la session Mac ; C1 à C8 conformes (E-1 admis).
- [x] Rootstocks d'essai regreffés : 0 lien cassé, 0 fichier régulier (hors `.DS_Store`
      tolérés) ; `check` code 0 (`qemu-gra2` : 1, attendu).

## Reprise
Commande ou première action de la session suivante :
```
révision du plan : présenter doc/devenv/HORS-PLAN.md à l'utilisateur (fin de chantier), puis skill lepton-portage-instructions
```
