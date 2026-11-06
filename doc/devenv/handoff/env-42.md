# Passation ENV-42 — `core_cm4.h` : un seul CMSIS-Core pour les Cortex-M4 — session du 2026-11-06

## Statut
terminée — chaque cœur choisit son CMSIS-Core : les 10 presets M4 compilent avec le `core_cm4.h`
5.9.0 (V5.1.2), V3.30 n'est plus posé que pour le M3 ; écarts bornés et identiques à l'essai ;
publié.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` | fusion de `devenv/env-42`, poussée avec `devenv/env-42` (commit de cette passation compris) | oui |
| clone noyau `depots/lepton/original/master` | `master` | 763dda2 « Fusion de devenv/env-42 (ENV-42 CMSIS-Core choisi par le cœur…, PA-72) », poussée avec `devenv/env-42` (484c44e, eb6c6c5) | oui |
| `bsp-qemu-mps2-an386` (`depots/lepton/bsp-qemu-mps2-an386/master`) | `master` | 5819047 « Fusion de devenv/env-42 (ENV-42 commentaire de qemu_mps2_machine.h…) », poussée avec `devenv/env-42` (21ca883) | oui |
| famille F4, WL, graine `original-tree`, seed.scions, autres BSP | — | non touchés | oui |

`<ROOTSTOCK>` : 3982 liens, 0 fichier régulier hors `.scion.grafted.list`, 0 lien cassé,
`lepton check` code 0 ; aucun fichier ajouté ni retiré (pas de regreffe). Copie d'essai
`essais/env-42-copie` supprimée (PA-72). Installés, inchangés : scion 0.6.1.0, lepton (pipx,
`devenv/env-41`), extension 0.5.2. Cartes rattachées au Mac : F429 avec `nucleo-f429zi-embos`
ENV-42 ; WL55 A et B avec `nucleo-wl55jc1-freertos` ENV-42.

## Fait pendant la session
- §1 audit (`rapports/env-42-core-cm4.md` §1 ; scripts `env-42-core-cm4/audit/`) : en-têtes par
  `ninja -t deps`, ordre des `-I`, API CMSIS utilisées, essais 1a et 1b sur copie (16 presets) ;
  PA-71 tranché.
- §2 oracle avant `oracles/env-42-avant/` = `env-41-apres` (16× code 0) ; bancs de référence F429
  20/20 ×2 (`banc-carte.sh`, WL55 débranchées), WL55 16/16 ×2 (`env-42-core-cm4/banc-wl55.sh`,
  nouveau).
- §3 noyau 484c44e (`cortex-m4f.cmake`, `armv7m.cmake`, `cortex-m3.cmake`, commentaire
  `cortex-m7.cmake`), eb6c6c5 (`LEPTON-PROVENANCE.md` du CMSIS-Core 5, `doc/migration/ajout-coeur.md`) ;
  BSP an386 21ca883 ; lepton-tools c67b409 (aide de `compiler-hal-f4-a-blanc.sh`). Commits faits
  dans la copie, repris dans `<ROOTSTOCK>` par `fetch` + `--ff-only`.
- §4 oracle après `oracles/env-42-apres/` : écarts identiques à l'essai (`.text` +16 an386/WL55,
  +32 F4 embOS, +48 F4 FreeRTOS), hors périmètre code 0, mklepton identiques, `ctest -N` 17/17,
  fumée et KAL QEMU identiques, bancs cartes identiques à la référence, XPERIPHERALS F429 `RCC` et
  `GPIOB` lisibles (utilisateur), HAL F4 à blanc 0 échec dans l'ordre `cmsis5`.
- PA-72 : fusions et push (noyau, BSP, lepton-tools).

## Reste à faire dans l'étape
- [x] Rien. Pour ENV-43 : l'attendu Debian contre `env-36-debian` inclut les écarts M4 d'ENV-42
  (`rapports/env-42-core-cm4.md` §4.1 ; deltas de `.text` et symboles NVIC, identiques d'un hôte à
  l'autre si la chaîne est la même) ; C4 : ordre `cmsis5` à 0 échec ; le script rend 1 tant que la
  ligne `v330` échoue (attendu).

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Plan de session (audit sur copie → PA-71, oracle et bancs avant, modification, contrôles → PA-72) | utilisateur | oui (journal) |
| PA-71 : option 1b ; V3.30 conservé dans l'arbre ; critère = écarts mesurés exacts ; F429 + 2 WL55, flash accordé ; commentaire du BSP an386 corrigé | utilisateur | oui |
| Vue XPERIPHERALS F429 lisible | utilisateur (constat) | oui |
| PA-72 : rapport accepté, oracle de référence `env-42-apres`, fusions et push noyau → BSP → lepton-tools, copie supprimée, O-1 hors plan | utilisateur | oui |
| Mise à jour de `doc/migration/ajout-coeur.md` et de l'aide de `compiler-hal-f4-a-blanc.sh` (conséquences du PA-71) | choix de session, présenté au PA-72 | oui (rapport §3.3) |
| Pas de regreffe (aucun fichier ajouté ni retiré) | choix de session | oui (rapport §3.3) |
| Bancs F429 passés WL55 débranchées (O-1) | choix de session, accepté par l'utilisateur | oui |

## Pièges rencontrés
- zsh ne découpe pas une variable en mots : `$Q $C` passé en un seul argument à
  `rejouer-oracle.sh` → arguments dans un script bash (`env-42-core-cm4/audit/oracle-16.sh`).
- Copie d'essai sans `.scion.rootstock.signature` : `lepton-env.sh` refuse (« aucun rootstock
  scion ») → copier aussi les fichiers cachés de la racine.
- Copie d'essai : `.debug_line`/`.debug_str` et, en FreeRTOS, `.text` (−152 octets, `__FILE__`)
  dépendent du chemin → comparer copie contre copie, puis deltas sur `<ROOTSTOCK>`.
- Le BSP `nucleo-f429zi` n'a pas `LEPTON_BOARD_STLINK_SERIAL` : avec plusieurs sondes, OpenOCD prend
  la première → débrancher les WL55 pour le banc F429 (O-1).
- Après la session de débogage VSCodium, l'OpenOCD de Cortex-Debug reste actif et tient la sonde →
  l'arrêter avant un banc.
- `grep -c` sur `radio-carte.log` ne rend rien (contenu binaire) → `grep -a`.

## Critères de validation
- [x] PA-71 et PA-72 tranchés et consignés.
- [x] Un preset `cortex-m4f` ne voit plus qu'un `core_cm4.h` possible.
- [x] Presets hors périmètre : binaires identiques (code 0).
- [x] Presets concernés : écarts dans le critère du PA-71 ; cartes accordées conformes au banc de
      référence.
- [x] Vue des périphériques F429 : résultat consigné.

## Reprise
Commande ou première action de la session suivante :
```
démarre la session   # ENV-43 : lire cette passation, handoff/env-41.md §Reste, etapes/ENV-43-validation-debian.md ; PA-73 ; oracle Mac de référence oracles/env-42-apres/
```
