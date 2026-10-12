# Étape ENV-11 — Validation de bout en bout

## Contexte
Cette étape vérifie l'environnement complet comme le ferait un nouvel utilisateur : installation,
création d'une graine de zéro, construction, exécution sous QEMU, flash et débogage sur les deux
cartes retenues, banc KAL. Elle ne développe rien : chaque défaut trouvé est consigné et renvoyé à
l'étape responsable.

## Prérequis
- ENV-4, ENV-9 et ENV-10 terminées.
- Cartes : NUCLEO-F429ZI ; NUCLEO-WL55JC1 (Lepton sur le cœur M4, M0+ non utilisé).
- VM Debian disponible pour la partie Debian (session distincte), sinon partie Debian reportée.

## Tâches

### 1. Point d'arrêt PA-11
Demander l'autorisation d'écrire la flash des deux cartes.

### 2. Scénario (hôte Mac Intel, depuis un compte où l'environnement est installé)
Consigner chaque commande et son résultat dans `doc/devenv/rapports/env-11-mac.md`. Commandes de
construction, d'exécution et de flash : skill `lepton-cibles`.
1. `install-vscodium.sh` sur l'état courant (doit être sans effet).
2. `lepton seed new` : graine de test, noyau + BSP QEMU, sans application (GRA-2).
3. Construction QEMU, test de fumée (`lsh`), banc KAL (TST-1).
4. `lepton scion new --type application` ; ajouter un `.c` par `lepton file add` ; construction
   sans édition CMake (FIC-4, BLD-2) ; exécution du programme sous QEMU.
5. Ajouter le BSP NUCLEO-F429ZI : construction, flash, arrêt sur `main`, console série (DBG-3).
6. Ajouter le BSP NUCLEO-WL55JC1 : idem.
7. Dans VSCodium : changement de preset, navigation, point d'arrêt depuis un fichier de greffon
   (IDE-1 à IDE-5, DBG-1 à DBG-3).
8. Retirer l'application (`lepton scion remove`) : trunk sans lien orphelin (GRF-4).
9. Même construction en ligne de commande et depuis l'éditeur : même empreinte (BLD-5).

### 3. Scénario Debian (VM)
Étapes 1 à 4 et 9 du scénario Mac. Rapport `doc/devenv/rapports/env-11-debian.md`.

### 4. Bilan
Table exigence × résultat (conforme, non conforme, non testé) pour toutes les exigences P1 de la
spécification. Chaque non-conformité : renvoi à l'étape à reprendre.

## Critères de validation
- [ ] PA-11 tranché.
- [ ] Toutes les exigences P1 conformes sur Mac, ou écart accepté par l'utilisateur.
- [ ] Scénario Debian conforme, ou report consigné.
- [ ] Aucun fichier régulier dans le trunk à la fin du scénario.

## Pièges connus
- STM32WL55 : vérifier que la sonde se connecte au cœur M4 (point d'accès du M4) ; ne pas
  modifier les octets d'option.
- Un échec de flash peut venir de la protection en lecture d'une carte neuve ou d'un firmware
  ST-Link ancien : relever le message d'OpenOCD avant toute autre action.

## À la fin de l'étape
`DEVENV-STATUS.md` : bilan des exigences, étapes à reprendre. Passation `handoff/env-11.md`.
