# Étape ENV-6 — Greffons BSP de référence

## Contexte
Un BSP est un greffon distinct (décision 2) qui porte démarrage, vecteurs, script d'édition de
liens, GPIO, pilotes de carte et configuration de débogage (GRF-3). Cette étape extrait le code de
carte existant vers trois greffons BSP : QEMU `mps2-an386`, NUCLEO-F429ZI, NUCLEO-WL55JC1 (cœur
M4, M0+ non utilisé). Les trois cartes sont supportées et testées depuis le portage : c'est un
déplacement de code, pas une réécriture, et leur comportement actuel fait foi.

## Prérequis
- ENV-5 terminée (manifestes BSP transitoires, construction par manifestes).
- `env-2-cartes.md` : fichiers propres à chaque carte ; support STM32WL existant ou non.
- Branche `devenv/env-6` dans le clone noyau.

## Tâches

### 1. Point d'arrêt PA-7 — liste d'extraction
Pour chaque carte : fichiers à déplacer, destination `kernel/dev/bsp/<carte>/` dans le nouveau
greffon, fichiers génériques qui restent dans le noyau. Attendre la validation.

### 2. Créer les greffons
- Un dépôt git local par BSP, `<À CONFIRMER : emplacement et noms des dépôts>`, arborescence
  `scion/sys/root/src/kernel/dev/bsp/<carte>/` et manifeste conforme à `greffon.schema.json`.
- Déplacer les fichiers par `git mv` dans le clone noyau vers un répertoire d'export, puis les
  importer dans le dépôt BSP (historique : consigner le commit d'origine dans le message).
- Ajouter les greffons BSP à une graine de travail (`.scion.sources.list`), `scion graft`.

### 3. Configurations de débogage portées par le BSP
Dans chaque manifeste BSP : fichiers OpenOCD (`interface/stlink.cfg`, `target/stm32f4x.cfg`,
`target/stm32wlx.cfg` : reprendre exactement ceux du portage, relevés en ENV-2), sonde, fichier
SVD, machine QEMU.
Ces valeurs servent à ENV-9 ; ne rien générer ici.

### 4. Validation
- Skill `lepton-oracle` : comparaison avec `oracles/env-5-apres/` pour les trois presets ;
  QEMU : test de fumée et banc KAL identiques.
- Flash et test de fumée série des deux cartes : en ENV-11 (PA-11).

## Critères de validation
- [ ] PA-7 tranché.
- [ ] Trois greffons BSP, manifestes valides (`scripts/valider-schemas.sh`).
- [ ] Plus aucun fichier propre à ces cartes dans le greffon noyau (recherche consignée).
- [ ] Construction des trois presets réussie ; QEMU identique à l'oracle.
- [ ] Trunk sans fichier régulier ; `scion ungraft && scion graft` sans erreur.

## Pièges connus
- STM32WL55 : le M4 démarre seul ; ne rien écrire dans les options de démarrage du M0+.
- Un fichier « de carte » inclus par du code générique : le signaler, ne pas inverser la
  dépendance sans décision.
- Créer les fichiers dans les clones des BSP, puis `scion graft` ; jamais dans le trunk.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, emplacements des dépôts BSP, cartes validées. Passation
`handoff/env-6.md`.
