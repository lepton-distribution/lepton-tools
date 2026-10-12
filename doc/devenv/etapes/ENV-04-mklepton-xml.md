# Étape ENV-4 — Évolution du format XML de mklepton

## Contexte
Le XML mklepton reste maître de la configuration logicielle de Lepton et de son système de
fichiers racine (décision 5), sans lien avec CMake. Son format évolue : retrait des éléments
inutiles, ajout des éléments manquants, version portée par le document (CFG-8). Archétype
migration : les images produites pour les configurations conservées doivent rester identiques.

## Prérequis
- ENV-3 terminée ; `schemas/mklepton.xsd` validé (PA-3).
- `env-2-mklepton.md` : liste des XML existants et de l'analyseur.
- Branche `devenv/env-4` dans le clone noyau.

## Tâches

### 1. Point d'arrêt PA-4 — liste des changements
Présenter le tableau élément × action (conservé, retiré, ajouté, renommé) × justification ×
fichiers XML touchés. Rien n'est modifié avant validation.

### 2. Oracle
Skill `lepton-oracle` §2 : pour chaque XML conservé, avec le mklepton actuel, empreintes des
sources C générées et de l'image UFS par `tests/host/mklepton_empreintes.sh` (script du portage),
dans `doc/devenv/rapports/oracles/env-4-avant/`. Plus l'oracle binaire et le test de fumée du
preset QEMU (§1 et §3).

### 3. Lecture versionnée dans mklepton
- Lire l'attribut `version` de l'élément racine ; refuser un document de version inconnue avec un
  message qui cite la version attendue et un code de retour non nul.
- Retirer la lecture des éléments supprimés ; ajouter celle des éléments nouveaux.
- Ne pas changer d'analyseur XML dans cette étape.

### 4. Migration des XML
Script rejouable `scripts/migrer-xml-mklepton.py` (dans `lepton-tools`) : ancien format → nouveau,
idempotent. L'appliquer dans le clone ; commit mécanique séparé.

### 5. Validation
- Tous les XML migrés passent `xmllint --schema schemas/mklepton.xsd`.
- Le nouveau mklepton produit, pour chaque XML migré, des sorties identiques à l'oracle (même
  empreinte). Tout écart est listé et expliqué ; un écart non expliqué bloque l'étape.
- Construction QEMU complète et test de fumée (`lsh`) inchangés.

## Critères de validation
- [ ] PA-4 tranché.
- [ ] Empreintes identiques à l'oracle pour 100 % des XML conservés (ou écarts validés par
      l'utilisateur).
- [ ] Un XML de version inconnue est refusé (code ≠ 0, message explicite).
- [ ] Script de migration rejoué deux fois sans changement (idempotence).
- [ ] Aucun élément de cœur, d'architecture ou de backend dans les XML migrés.

## Pièges connus
- mklepton est compilé pour l'hôte avec un noyau statique (kernel/core, pilotes logiciels, vfs,
  rootfs, ufs) : une modification d'en-tête partagé avec la cible se répercute sur la construction
  embarquée ; reconstruire les deux.
- Éditer les XML dans le clone, pas dans le trunk.
- Un écart d'empreinte peut venir d'une date ou d'un ordre de parcours de répertoire dans l'image
  UFS : le vérifier avant de conclure à une régression.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, version du format XML, branche. Passation `handoff/env-4.md`.
