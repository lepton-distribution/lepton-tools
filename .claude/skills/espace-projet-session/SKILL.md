---
name: "espace-projet-session"
description: "Procédure obligatoire de début et de fin de session du chantier « espace-projet » (dépôt lepton-tools, doc/espace-projet/, étapes EP-N). Utiliser au démarrage de toute session de ce chantier (« démarre EP-N », « reprends EP-N », « on continue l'espace-projet ») et avant de la clore ou de l'interrompre (« fin de session », « on s'arrête », « fais la passation »). Ne pas utiliser pour une étape ENV-N (skill devenv-session) ni pour une session de ticket."
---

# Session du chantier espace-projet

Une session traite une seule étape `EP-N`. Le contexte entre sessions ne passe que par
`doc/espace-projet/STATUS.md` et `doc/espace-projet/handoff/ep-N.md`. La règle de référence est
`doc/espace-projet/ORCHESTRATION.md` §3 ; en cas d'écart, elle l'emporte sur ce fichier.

## Début de session

Exécuter dans cet ordre, sans en sauter :

1. Lire `doc/espace-projet/ORCHESTRATION.md` en entier, puis `doc/espace-projet/STATUS.md`.
2. Identifier l'étape : la « Prochaine action » de `STATUS.md`. Si l'utilisateur en désigne une
   autre, vérifier dans le graphe (ORCHESTRATION §6) que ses prérequis sont terminés ; sinon le
   signaler et s'arrêter.
3. Lire la dernière passation : `doc/espace-projet/handoff/ep-N.md` si l'étape est en cours,
   sinon celle de la dernière étape terminée.
4. Lire `doc/espace-projet/etapes/EP-N-*.md`, puis les décisions de
   `doc/espace-projet/CADRAGE.md` qu'il cite. Les documents du chantier ENV qu'il cite
   (`doc/devenv/ORCHESTRATION.md`, `DEVENV-STATUS.md`, `HORS-PLAN.md`, rapports) se lisent **par
   section** (`grep -n '^## '` puis `sed -n`), jamais en entier.
5. Vérifier l'état réel de chaque dépôt touché par l'étape (chemins dans `STATUS.md`
   §Emplacements) :
   ```bash
   git -C <dépôt> status --short
   git -C <dépôt> branch --show-current
   git -C <dépôt> log --oneline -3
   ```
   Tout écart avec la passation (branche, commit, fichiers non commités) : le signaler et attendre.
6. Vérifier les versions utiles à l'étape (`STATUS.md` §Versions, sinon
   `doc/devenv/DEVENV-STATUS.md` §Versions épinglées).
7. Passer en mode plan. Présenter : étape, état constaté, tâches de la session, points d'arrêt
   (ORCHESTRATION §4) qui seront rencontrés. Attendre l'accord.
8. Après accord : créer ou extraire la branche `espace-projet/ep-N` dans chaque dépôt touché ;
   passer l'étape à « en cours » dans `STATUS.md`.

## Pendant la session

- Point d'arrêt atteint : s'arrêter, exposer la question, attendre ; consigner la réponse dans
  `STATUS.md` §Décisions avec la date et l'identifiant `PA-En`.
- `doc/espace-projet/CADRAGE.md` §6 est une liste de propositions non validées : les présenter au
  point d'arrêt de conception de l'étape, ne pas les appliquer d'office. Les décisions C1 à C10 et
  P1 à P6 ne se rediscutent pas ; une étape qui les contredit s'arrête et le signale.
- Tension T1 à T11 (ORCHESTRATION §5) rencontrée : la présenter au point d'arrêt indiqué, avec les
  faits de l'audit ; ne pas la trancher.
- Point écarté du plan : au point d'arrêt où il est présenté, proposer le choix hors plan ou
  ticket (règle en tête de `doc/devenv/HORS-PLAN.md`). Ticket seulement pour un défaut ou une
  fonctionnalité du code d'un greffon du rootstock (ni `lepton-tools` ni `seed.scions`) : skill
  `lepton-ticket-creer` (plugin `lepton-tickets`), publication sur accord du texte. La ligne est
  ajoutée à `doc/espace-projet/HORS-PLAN.md` dans les deux cas.
- Toute écriture dans l'arbre Lepton : skill `lepton-rootstock`.
- Tout état de référence ou toute comparaison : skill `lepton-oracle`.
- Toute construction, exécution QEMU, flash ou débogage : skill `lepton-cibles`.
- Ces trois skills sont écrites pour le chantier ENV : y lire `espace-projet/ep-N` pour
  `devenv/env-N`, `doc/espace-projet/rapports/` pour `doc/devenv/rapports/`, `STATUS.md` pour
  `DEVENV-STATUS.md`. Oracles : `doc/espace-projet/rapports/oracles/ep-N-<avant|apres>/`.
- Tout `git push`, toute action `scion seed-update` / `graft-update`, tout `scion mirror-sync` sans
  `--dry-run` : accord explicite de l'utilisateur (PA-P, `doc/devenv/ORCHESTRATION.md` §4).
- Tout message vers ou depuis une autre session Claude Code (VM, Remote Control) : protocole de
  `doc/devenv/ORCHESTRATION.md` §2bis (`ORDRE` → `ACCUSÉ` → `AVANCEMENT` → `FIN-SUCCÈS` /
  `FIN-ÉCHEC`) ; rien n'est tenu pour reçu sans accusé.

## Fin de session (même interrompue, même en cas d'échec)

1. Mettre à jour `doc/espace-projet/STATUS.md` :
   - statut de l'étape (en cours, bloquée + raison, terminée + date) ;
   - colonnes Branche(s) et Passation ;
   - une ligne de journal ;
   - « Prochaine action » : une phrase exécutable par la session suivante ;
   - versions nouvellement relevées ; décisions prises.
2. Écrire `doc/espace-projet/handoff/ep-N.md` d'après `doc/devenv/handoff/TEMPLATE.md` (lire
   « EP » pour « ENV », `STATUS.md` pour `DEVENV-STATUS`), en remplaçant le précédent s'il existe.
   Distinguer les décisions de l'utilisateur des propositions non validées. Lister les tickets
   créés pendant la session.
3. Commiter dans `lepton-tools`, sur la branche de l'étape :
   ```bash
   git add doc/espace-projet && git commit -m "espace-projet(ep-N): état et passation"
   ```
   Un fichier de `doc/devenv/` modifié sur décision consignée s'ajoute explicitement.
4. Ne rien pousser. Résumer à l'utilisateur : fait, reste, prochaine action.

## Interdits

- Commencer une seconde étape dans la même session.
- Laisser une session sans passation.
- Recopier un rapport volumineux dans `STATUS.md` : le référencer.
- Lire `doc/devenv/DEVENV-STATUS.md` en entier.
- Modifier `doc/devenv/` sans décision consignée (ORCHESTRATION §3 : D41 et D42 en EP-7, D45,
  issue de T9).
