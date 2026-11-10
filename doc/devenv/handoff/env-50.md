# Passation ENV-50 — Validation Debian groupée (ENV-44 à ENV-49) — session du 2026-11-10

## Statut
Terminée. L'ordre `R50-1` valide sur la VM Debian l'état publié après ENV-44 à ENV-49 :
C1 à C8 atteints, C7 après une reprise. Les 7 rootstocks d'essai du Mac sont regreffés. PA-87 et
PA-88 sont tranchés, et tout est publié. ENV-50 est la dernière étape du plan : la suite est une
révision du plan.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` | fusion de `devenv/env-50` ; `main` et `devenv/env-50` poussés ; `devenv/env-50-debian` (VM) 29835e9, poussée, fusionnée | oui |
| clone noyau `depots/lepton/original/master` | `master` | 76f28bd, non touché | oui |
| autres | `master` / `original-tree` | non touchés : F4 acdd24c, F7 12280a5, WL 9349be2, WL55 4d7cf80, an386 10a8889, graine 15740f9, seed.scions 7e8a0cc (tag 0.6.2.0) ; 8 miroirs inchangés | oui |

`<ROOTSTOCK>` n'a pas été touché : 3889 liens, 629 projetés, `CONFORME` contre
`rapports/env-50-mac/attendu/trunk-liens.txt`.

Outils : scion 0.6.2.0 et lepton 0.1.0, au Mac comme sur la VM. La VM est passée de scion 0.6.1.0
à 0.6.2.0 en R50-1.

Oracles de référence : Mac `oracles/env-49-apres/`, Debian `oracles/env-50-debian/`.

Cartes : les trois cartes sont rendues au Mac par l'utilisateur à 20:03.
- F429 : image `nucleo-f439zi-embos` de la VM.
- WL55 A et B : image `nucleo-wl55jc1-freertos` de la VM.

Ports à relever par `ioreg` avant tout banc ; pendant la panne, le Mac les voyait sur
`/dev/cu.usbmodem14303`, `145103` et `1454303`.

État de la VM :
- `essais/env-28-debian` et `essais/env-13-debian` regreffés ;
- `essais/env-50-debian` neuf ;
- `essais/env-11/qemu` ;
- journaux `~/env-50-journaux` et `~/tmp-pytest` ;
- `essais/env-43-debian` et `~/env-43-journaux` supprimés (C8).

## Fait pendant la session
- **Préparation** (`rapports/env-50-mac.md` §1) :
  - écarts `env-42-apres` → `env-49-apres` : WL55 26 symboles et code +36, an386 `.debug_*` seuls,
    10 presets à 0 ;
  - `env-50-mac/croissance.py`, qui lit la somme des symboles de code (leçon E-1) ;
  - attendus de liens : 3982 + 11 − 104 = 3889, 629 projetés ;
  - essai préalable : `graft-update` d'`essais/env-13-vierge` (PA-P) `CONFORME`, puis
    `mirror-sync --dry-run` sur 8 miroirs, 0 à envoyer ;
  - références de C5 : pytest 377 tests, compilation à blanc code 0 ;
  - consigne `consignes/env-50-debian.md`.
- **PA-87** ; push de `devenv/env-50` ; ordre `R50-1` à `debian-linux-vm`. L'`ACCUSÉ`, les
  `AVANCEMENT` et le `FIN-SUCCÈS` sont tous arrivés directement, sans relais (§3 du rapport Mac).
- **R50-1** (`rapports/env-50-debian.md`) :
  - C1 : installations par l'utilisateur ;
  - C2 : `$U` regreffé et rootstock neuf, `CONFORME`, casse comprise ;
  - C3 : 16 presets dans l'attendu ;
  - C4 : D8 ;
  - C5 : pytest 377 (dont 118 pour le hook), HAL à blanc code 0, fichiers générés identiques ;
  - C6 : 8 miroirs, 0 à envoyer ;
  - C7 : trois sondes choisies par numéro ; F429 20/20 ×3 après la relance de `board.net` ; WL55
    16/16 ×2, radio comprise ;
  - C8 : nettoyage.
- **Tâche 3** (§4 du rapport Mac) :
  - 6 rootstocks regreffés, tous conformes ;
  - `env-11/f429zi` et `env-11/wl55jc1` construits : 0 écart hors `.debug_*` contre `env-49-apres` ;
  - `essais/env-41-vierge*` supprimés.
- **Vérification** (§5 du rapport Mac) : comparaisons refaites au Mac sur l'oracle poussé,
  identiques au rapport VM.
- **PA-88** ; fusions et push. `HORS-PLAN.md` : D8 traité, D12 ajouté.

## Reste à faire dans l'étape
- [x] Rien.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Orientations C5, C7, C8, sort d'`env-41-vierge`, essai préalable (avant PA-87) | utilisateur | oui |
| PA-P : `graft-update` d'`env-13-vierge` et `mirror-sync --dry-run` au Mac | utilisateur | oui |
| PA-87, PA-11, PA-P : consigne validée, flash sur la VM (3 images F429, 2 images WL55), push et ordre | utilisateur | oui |
| PA-P, tâche 3 : regreffe des 6 rootstocks, suppression d'`env-41-vierge*` | utilisateur | oui |
| PA-88, PA-P : `FIN-SUCCÈS` accepté (C7 après reprise), fusions (29835e9 compris) et push | utilisateur | oui |
| Fusion du complément 29835e9 (rapport seul, cartes rendues au Mac) sous l'accord du PA-88 donné pour 88e48b6 | proposition de la session, vérifiée (diff de 4 lignes du rapport) | oui (PA-88) |
| Lecture de la panne Ethernet : cause côté carte, non côté pont VMware (constat Mac) | proposition de la session | rapport Mac §5, D12 |

## Pièges rencontrés
- **Remplacement Python ancré sur une chaîne non unique.** `s[s.index(a):s.index(b)]` avec un `b`
  déjà présent plus haut donne une tranche vide, et `replace('', …)` insère le texte entre chaque
  caractère. Réparé exactement en retirant les insertions. Parade : `assert s.count(ancre) == 1`
  avant tout remplacement.
- **`lepton-env.sh`** cherche le rootstock à partir de `${1:-$PWD}`. Un `set -- …` dans un script
  ou un `source` lancé hors du rootstock donne « aucun rootstock scion au-dessus de … ». C'est un
  défaut de la consigne R50-1 (§12.2). Pour la suite : `source "$R"/…/lepton-env.sh "$R"`.
- **F429 muette en Ethernet au retour de la VM** (D12). La carte n'a répondu ni à la VM ni au
  Mac, alors qu'`en0` était actif. Levé par débranchement, nouveau rattachement et vérification du
  câble. La consigne prévoyait la relance unique d'un test en échec : elle a suffi.
- **Coupure pendant le banc** : VMware Fusion rend les sondes USB à l'hôte. Un `ctest` en cours
  échoue alors à l'ouverture du port, avant tout flash. Il faut relever le port de nouveau et
  relancer.
- **Nom de la session Mac** changé en cours de route (`lepton-tools-9d` → `validate-debian-env-50`).
  Les réponses de la VM, adressées au `from` de l'ordre, sont tout de même arrivées.

## Critères de validation
- [x] PA-87 et PA-88 tranchés et consignés.
- [x] `FIN-SUCCÈS R50-1` vérifié par la session Mac ; C1 à C8 conformes.
- [x] `essais/env-13-debian` regreffé (D8).
- [x] Rootstocks d'essai regreffés : 0 lien cassé, 0 fichier régulier (hors `.DS_Store` tolérés) ;
      `check` code 0 (`qemu-gra2` : 1, attendu).

## Reprise
Commande ou première action de la session suivante :
```
révision du plan (skill devenv-session puis lepton-portage-instructions) en partant de
doc/devenv/HORS-PLAN.md : présenter la liste en entier à l'utilisateur (A1-A4, D4, D10, D11, D12
non traités) ; références Mac oracles/env-49-apres, Debian oracles/env-50-debian
```
