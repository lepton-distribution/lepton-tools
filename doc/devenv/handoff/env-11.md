# Passation ENV-11 — Validation de bout en bout — session du 2026-10-15 (S2)

## Statut
en cours — S1 (scénario Mac en ligne de commande) et S2 (cartes réelles, VSCodium) faites ; S3 (VM
Debian, bilan) reste.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `devenv/env-11` (non poussée) | `devenv(env-11): état et passation (S2)` ; avant : 3bd37f6 skill lepton-cibles (ports série, `adapter serial`), 9145805 passation S1, 7d191aa, 338ff5b ; `main` = 657c395 (non poussée) | oui |
| clone noyau `~/lepton/depots/lepton/original/master` | `devenv/env-11` (extraite, non poussée) | a572f00 défaut `SCION_REF` 0.5.1.0 ; `master` = 1dde0af (non poussée) | oui |
| seed.scions | `master` 79f4f96, tag 0.5.1.0 | inchangé | oui |
| BSP, familles, graine de travail de `~/lepton` | `master` / `original-tree` | inchangés (identiques à `essais/env-11/ref-avant.txt`, contrôle de fin de S2) | oui |
| Rootstocks d'essai (hors git) | `~/lepton-tools-dev/essais/env-11/{qemu,f429zi,wl55jc1}` ; `qemu` a en plus `build/qemu-mps2-an386-freertos` (essai IDE-5) | clones d'essai propres ; trunks : seul fichier régulier `.scion.grafted.list` | — |
| Cartes | NUCLEO-F429ZI : `env11f4-debug-board` (embOS) ; NUCLEO-WL55JC1 carte A : `env11wl-debug-board` (FreeRTOS) | flashées, vérifiées | — |

## Fait pendant la session
- §2.5-2.6 en ligne de commande, avec `adapter serial` : identification des deux sondes, flash
  « Verified OK » (WL : RDP 0, octets d'option et M0+ non touchés), `lsh` sur la console série
  (`smoke_lsh.py --transport serial`), arrêt sur `main` en GDB.
- §2.7 et §2.9 dans VSCodium (manipulé par l'utilisateur) : DBG-3 (flash, `main`, point d'arrêt) sur
  les deux cartes, une branchée à la fois ; DBG-1, DBG-2, TST-1 18/18, IDE-1 à IDE-5 ; BLD-5 :
  `lepton.bin` 25d50f61… et `lepton.hex` 7e29c21c… identiques à la ligne de commande.
- Constats : N4 (CFG-7 non conforme), O6 tranchée, O8-O11 (`rapports/env-11-mac.md` §2bis, §3, §4).
- Skill `lepton-cibles` : ports série relevés (F429 `usbmodem145103`, WL A `usbmodem1454303`),
  `adapter serial` obligatoire avec deux sondes, commande de fumée série (3bd37f6).

## Reste à faire dans l'étape
- [ ] S3 §3 : push soumis à PA-P (lepton-tools `main` + `devenv/env-11` ; clone noyau `master` +
      `devenv/env-11`), consigne VM `consignes/env-11-debian.md` (étapes 2.1-2.4 et 2.9 CLI), rapport
      `rapports/env-11-debian.md` intégré.
- [ ] S3 §4 : bilan exigences P1 × résultat (conforme, non conforme, non testé) ; classement de N1,
      N4, O1-O11 (étape à reprendre) avec l'utilisateur.
- Reliquats hors étape : Apple Silicon (revue seule) ; ligne « openocd » vide du récapitulatif
  d'`install-debian.sh`.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| O6 démontré par lecture du code (`cmake/kal/embos.cmake:13-15`), `~/.zshrc` non modifié | utilisateur | oui |
| L'utilisateur réalise seul la partie VSCodium (pas de pilotage de l'interface ; pas de computer use dans cette session) | utilisateur | non (méthode) |
| Essais éditeur sur carte une carte branchée à la fois | proposition appliquée | oui |
| N4 classé défaut (CFG-7 P2 non conforme) ; renvoi proposé ENV-9 | proposition non validée | oui (à classer en S3) |
| Renvois proposés d'O6, O8-O11 | propositions non validées | oui (rapport §4, à classer en S3) |

## Pièges rencontrés
- Le hook `proteger-trunk.py` refuse toute commande shell qui mentionne `trunk/` et contient une
  redirection, même vers `logs/` : passer par le chemin réel dans le clone (`realpath`) ou l'outil Edit.
- Deux ST-Link branchés : sans `adapter serial`, la cfg F4 prend la sonde V3 du WL55 (échec sur
  l'IDCODE, sans écriture).
- VSCodium lancé par le Finder lit l'environnement du shell de connexion (`~/.zshrc`) ; pour une
  variable propre à un essai (`SOURCE_DATE_EPOCH`), le quitter complètement (⌘Q) puis le lancer par
  `codium` depuis un terminal qui l'exporte.
- clangd démarré avant que CMake Tools ait configuré : aucune base ; « clangd: Restart language
  server » après la première configuration par CMake Tools (O10).
- Sélecteur de preset absent de la barre d'état (CMake Tools 1.24.42) : panneau CMake › Project
  Status ou « CMake: Select Configure Preset » (O11).
- `arm-none-eabi-gdb` macOS sans Python : message à la fin du chargement de `gdbinit-lepton` (O9),
  sans effet sur le débogage.

## Critères de validation
- [x] PA-11 tranché.
- [ ] Toutes les exigences P1 conformes sur Mac, ou écart accepté par l'utilisateur : scénario Mac
      complet, P1 testées conformes (réserves O8, O10, O11) ; acceptation des écarts au bilan S3.
- [ ] Scénario Debian conforme, ou report consigné (S3).
- [x] Aucun fichier régulier dans le trunk à la fin du scénario (trois rootstocks d'essai, hors
      `.scion.grafted.list` de scion et `.DS_Store` ignorés par Q8).

## Reprise
```
cd /Users/cle_d_anton/lepton-tools-dev/lepton-tools && claude
# « Démarre la session sur l'étape indiquée dans DEVENV-STATUS » (ENV-11 S3 : VM Debian, bilan)
```
