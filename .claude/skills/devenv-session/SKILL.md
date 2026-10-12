---
name: devenv-session
description: Procédure obligatoire de début et de fin de session du chantier « environnement de développement Lepton » (dépôt lepton-tools). Utiliser au démarrage de toute session (« démarre la session », « reprends l'étape », « on continue ENV-N ») et avant de la clore ou de l'interrompre (« fin de session », « on s'arrête », « fais la passation »).
---

# Session du chantier ENV

Une session traite une seule étape `ENV-N`. Le contexte entre sessions ne passe que par
`doc/devenv/DEVENV-STATUS.md` et `doc/devenv/handoff/env-N.md`.

## Début de session

Exécuter dans cet ordre, sans en sauter :

1. Lire `doc/devenv/ORCHESTRATION.md` en entier, puis `doc/devenv/DEVENV-STATUS.md`.
2. Identifier l'étape : la « Prochaine action » de `DEVENV-STATUS.md`. Si l'utilisateur en désigne
   une autre, vérifier dans le tableau des dépendances (ORCHESTRATION §6) que ses prérequis sont
   terminés ; sinon le signaler et s'arrêter.
3. Lire la dernière passation : `doc/devenv/handoff/env-N.md` si l'étape est en cours, sinon celle
   de l'étape précédente terminée.
4. Lire `doc/devenv/etapes/ENV-NN-*.md` et, dans `doc/devenv/SPECIFICATION.md`, chaque exigence
   qu'il cite.
5. Vérifier l'état réel de chaque dépôt touché par l'étape (chemins dans `DEVENV-STATUS.md`
   §Emplacements) :
   ```bash
   git -C <dépôt> status --short
   git -C <dépôt> branch --show-current
   git -C <dépôt> log --oneline -3
   ```
   Tout écart avec la passation (branche, commit, fichiers non commités) : le signaler et attendre.
6. Vérifier les versions épinglées utiles à l'étape (`DEVENV-STATUS.md` §Versions).
7. Passer en mode plan. Présenter : étape, état constaté, tâches de la session, points d'arrêt
   (ORCHESTRATION §4) qui seront rencontrés. Attendre l'accord.
8. Après accord : créer ou extraire la branche `devenv/env-N` dans chaque dépôt touché ; passer
   l'étape à « en cours » dans `DEVENV-STATUS.md`.

## Pendant la session

- Point d'arrêt atteint : s'arrêter, exposer la question, attendre ; consigner la réponse dans
  `DEVENV-STATUS.md` §Décisions avec la date et l'identifiant PA-x.
- Toute écriture dans l'arbre Lepton : appliquer la skill `lepton-rootstock`.
- Tout état de référence ou toute comparaison : skill `lepton-oracle`.
- Toute construction, exécution QEMU, flash ou débogage : skill `lepton-cibles`.

## Fin de session (même interrompue, même en cas d'échec)

1. Mettre à jour `doc/devenv/DEVENV-STATUS.md` :
   - statut de l'étape (en cours, bloquée + raison, terminée + date) ;
   - colonnes Branche(s) et Passation ;
   - une ligne de journal ;
   - « Prochaine action » : une phrase exécutable par la session suivante ;
   - versions nouvellement relevées ; décisions prises.
2. Écrire `doc/devenv/handoff/env-N.md` d'après `doc/devenv/handoff/TEMPLATE.md`, en remplaçant le
   précédent s'il existe. Distinguer les décisions de l'utilisateur des propositions non validées.
3. Commiter dans `lepton-tools` :
   ```bash
   git add doc/devenv && git commit -m "devenv(env-N): état et passation"
   ```
4. Ne rien pousser. Résumer à l'utilisateur : fait, reste, prochaine action.

## Interdits

- Commencer une seconde étape dans la même session.
- Laisser une session sans passation.
- Recopier un rapport volumineux dans `DEVENV-STATUS.md` : le référencer.
