# Étape EP-7 — lepton : trunk déjà incohérent, répertoire vide (D41, D42)

## Contexte
Décision P4 du 2026-11-25 : ce chantier reprend D41 et D42 de `doc/devenv/HORS-PLAN.md`, marqués
« à traiter » à la fin du plan ENV (2026-11-24). Ce ne sont pas des tickets : lepton-tools n'est
pas un greffon du rootstock. Les deux lots sont sans lien avec les axes du chantier ; l'étape est
indépendante et d'ordre libre avant EP-8.

- **D41** (`doc/devenv/rapports/env-68-lepton.md` §4.5, O-1) : une opération lancée sur un trunk
  déjà incohérent (lien cassé, fichier régulier) est faite, puis signalée en échec par le
  contrôle final (`finish` : « trunk incohérent après l'opération »), sans annulation, sans dire
  qu'elle a été faite, et sans distinguer l'incohérence antérieure de celle que l'opération
  aurait créée. Cas relevé : `seed mkconf import` par l'extension, XML importé mais notification
  d'erreur seule (liens cassés d'un greffon sans clone). Ce lot change un comportement.
- **D42** (`doc/devenv/rapports/env-68-lepton.md` §4.2, §4.5) : après `seed remove` d'un greffon
  déclaré dont le clone a été supprimé hors de lepton (D37), le répertoire vide
  `depots/<shelf>/<préfixe>-<nom>/` reste ; lepton ne le crée pas, un réajout le réutilise. À
  décider : le retirer lors du retrait.

Archétype : infrastructure. Sur un trunk cohérent, rien ne change.

## Prérequis
- Conseillée après EP-1, qui modifie les mêmes commandes (`seed mkconf import`, `check`).
- lepton et `pytest` : `STATUS.md` §Versions, `doc/devenv/DEVENV-STATUS.md` §Versions épinglées.
- Scripts et relevés d'ENV-68 : `doc/devenv/rapports/env-68-lepton/`.
- Skill `lepton-rootstock`. Branche `espace-projet/ep-7` de lepton-tools.

## Tâches

### 1. Audit (lecture seule) → PA-E14
Rapport `doc/espace-projet/rapports/ep-7-lepton.md`. Essais sur une copie d'un rootstock d'essai
sous `~/lepton-tools-dev/essais/ep-7/`.
- **D41** : reproduire le cas d'ENV-68 (greffon déclaré sans clone, puis `seed mkconf import`).
  Relever toutes les commandes qui passent par `finish`, et pour chacune : ce qui est écrit avant
  le contrôle, le message, le code de retour, ce que l'extension affiche.
- **D42** : reproduire (clone supprimé hors de lepton, `seed remove`). Relever qui crée le
  répertoire intermédiaire, et s'il peut contenir autre chose (autre version du même greffon).
- **PA-E14** : l'utilisateur tranche.
  - D41, options : contrôle du trunk avant l'opération, avec refus et message ; contrôle avant,
    avec avertissement, puis opération et message final qui distingue l'état antérieur ;
    message final seul, corrigé pour dire que l'opération est faite. Code de retour dans chaque
    cas. `<À CONFIRMER au PA-E14>`.
  - D42, options : retirer le répertoire s'il est vide ; le laisser et le dire.
    `<À CONFIRMER au PA-E14>`.
  - Version de lepton et de l'extension : `<À CONFIRMER au PA-E14>`.
- Aucune modification avant la réponse.

### 2. Implémentation (lepton-tools)
Tests d'abord, pour chaque cas retenu, qui échouent sur la branche de départ. Plus un test qui
prouve qu'une opération sur un trunk cohérent se termine comme avant (message et code). Commits
séparés : lot D41, lot D42. Extension : seulement si l'affichage de D41 le demande.

### 3. Essai
Cas d'ENV-68 rejoués sur la copie, avant et après, comparés par `scripts/comparer-releves.py`.
Si le PA-E14 touche l'affichage : essai dans VSCodium par l'utilisateur.

### 4. Clôture → PA-E15
**PA-E15** : rapport ; sort des essais ; fusion et publication (PA-P).

## Critères de validation
- [ ] PA-E14 et PA-E15 tranchés et consignés.
- [ ] D41 : sur un trunk déjà incohérent, le comportement suit le PA-E14 ; l'utilisateur sait si
      l'opération a été faite.
- [ ] D42 : le répertoire suit le PA-E14 ; un répertoire non vide n'est jamais retiré.
- [ ] Trunk cohérent : messages et codes identiques à ceux d'avant l'étape.
- [ ] `pytest` vert, dont les nouveaux tests.
- [ ] `doc/devenv/HORS-PLAN.md` : lignes D41 et D42 complétées (« traité en EP-7 du chantier
      espace-projet », renvoi au rapport) ; modification de `doc/devenv/` consignée
      (ORCHESTRATION §3), commitée par `git add doc/espace-projet doc/devenv/HORS-PLAN.md`.

## Pièges connus
- `test_echec_de_scion_sans_double_affichage` (lepton-tools) casse si un message contient une
  seconde ligne `erreur :`.
- Un contrôle avant l'opération ne doit pas bloquer les commandes qui servent à réparer un trunk
  incohérent (`seed remove` d'un greffon sans clone, D37 ; `check`).
- Ne pas supprimer par `rm` : les suppressions d'essai passent par `scripts/supprimer-essai.sh` ;
  le retrait du répertoire vide par lepton est du code de lepton, testé.

## À la fin de l'étape
`STATUS.md` : statut, branche, §Versions (lepton), décisions PA-E14 et PA-E15, journal.
`doc/devenv/HORS-PLAN.md` : D41, D42. Passation `handoff/ep-7.md`.
