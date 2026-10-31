# Étape ENV-22 — Résidus d'ENV-17 à ENV-21

## Contexte
Les étapes ENV-17 à ENV-21 sont closes (2026-10-31), mais il en reste des résidus (analyse du
2026-10-31) :
- `<ROOTSTOCK>` n'a pas de `.scion.trunk.tolerated`, alors que les 6 rootstocks d'essai en ont un
  depuis ENV-21. Les `.DS_Store` créés par le Finder dans le trunk ont bloqué des regreffes en
  ENV-17 et ENV-21.
- Des propositions ont été appliquées sans être validées séparément.
- `essais/env-11/bout-en-bout` n'a pas été regreffé.
- Deux leçons de la VM ne sont pas inscrites dans les règles des consignes (E-1 et E-2
  d'`rapports/env-21-debian.md`).

Cette étape solde ces points sans changer ni binaire ni image mklepton. Archétype :
infrastructure.

## Prérequis
- ENV-21 terminée ; tous les dépôts propres et alignés sur leurs distants.
- Skills `devenv-session` et `lepton-rootstock`.
- Branche `devenv/env-22` dans lepton-tools. Aucun autre dépôt n'est touché, sauf si le PA-31 en
  décide autrement.

## Tâches

### 1. Audit (lecture seule) → PA-31
- **`.scion.trunk.tolerated`.**
  - Format attendu par scion 0.5.2.0 : en-tête et motifs. Modèle : le fichier écrit en ENV-21
    dans les rootstocks d'essai (`rapports/env-21-mac.md` §3).
  - Lepton purge déjà `.DS_Store` et `._*` avant `scion graft` (`rapports/env-15-scion.md` §6).
    Vérifier comment cette purge interagit avec le fichier de tolérance.
- **Propositions non validées séparément.** Les recopier depuis les passations :
  - ENV-17 : `ORCHESTRATION.md` §2 ; commentaire au-dessus du message M-1 dans `kernel.cmake`
    (350d914).
  - ENV-18 : texte de l'information « BSP non greffé » de `generate` ; `build_type` vide quand un
    preset n'a pas de `CMAKE_BUILD_TYPE`.
  - ENV-19 : branche par défaut GitHub des 4 dépôts remise à `master`.
  - ENV-20 : relais local `stm32f4xx_irq_default`, table renommée `stm32f4xx_vector_table_ext` ;
    description du dépôt `lepton-bsp-nucleo-f439zi`.
- **`essais/env-11/bout-en-bout`.** Relever son contenu (graine, entrées, liens, espace occupé)
  et son usage dans les rapports d'ENV-11 et d'ENV-12.
- **Règles des consignes VM.** Leçons de R15-1 et R21-1 :
  - régénérer un fichier généré avant d'en relever l'empreinte (E-1) ;
  - les suppressions (`rm -rf`) et les installations par `pipx` peuvent être refusées par les
    permissions de la session VM : les confier à l'utilisateur dès la consigne (E-2,
    `rapports/env-15-scion.md` §8).
- **PA-31** : l'utilisateur valide :
  - le contenu de `<ROOTSTOCK>/.scion.trunk.tolerated` ;
  - la confirmation des propositions, en bloc ou une par une ;
  - le sort de `essais/env-11/bout-en-bout` : <À CONFIRMER au PA-31 : regreffer, archiver ou
    supprimer> ;
  - l'emplacement des règles des consignes : <À CONFIRMER au PA-31 : `ORCHESTRATION.md` §2bis ou
    modèle `consignes/MODELE.md`>.
- Aucune modification avant la réponse.

### 2. Application
- `<ROOTSTOCK>/.scion.trunk.tolerated` : il est écrit à la racine du rootstock, hors du trunk.
  Ne jamais écrire dans `trunk/` (hook) et ne pas créer de `.DS_Store` pour faire un essai.
- `scion graft` sur `<ROOTSTOCK>` : code 0 ; liste des liens identique à celle d'avant
  (`sha256` de la liste triée).
- `essais/env-11/bout-en-bout` : appliquer la décision du PA-31. Un regreffe suit la procédure
  d'ENV-21 (`rapports/env-21-mac.md` §3) et passe par PA-P. Toute suppression attend un accord
  explicite.
- Règles des consignes VM : les écrire à l'emplacement choisi au PA-31.
- `DEVENV-STATUS.md` §Décisions : consigner les propositions confirmées.

### 3. Contrôles → PA-32
- Trunk de `<ROOTSTOCK>` : 0 fichier régulier, 0 lien cassé, même nombre de liens qu'avant
  (3941 au 2026-10-31).
- `lepton check` sur `<ROOTSTOCK>` : code 0.
- **PA-32** : rapport `rapports/env-22-residus.md` ; fusion dans `main` et push (PA-P).

## Critères de validation
- [ ] PA-31 et PA-32 tranchés et consignés.
- [ ] `<ROOTSTOCK>/.scion.trunk.tolerated` présent ; `scion graft` code 0 ; liste des liens inchangée.
- [ ] Chaque proposition listée au §1 est confirmée ou amendée dans `DEVENV-STATUS.md` §Décisions.
- [ ] `essais/env-11/bout-en-bout` traité selon le PA-31.
- [ ] Règles des consignes VM écrites ; ENV-28 s'y réfère.

## Pièges connus
- Le hook refuse toute redirection vers un `trunk/`, même celui d'une copie. Pour retirer un
  greffon d'une copie, utiliser `scion graft-remove` (sans `--purge`).
- Les `.DS_Store` reviennent même après une suppression (processus macOS). Contrôler le trunk
  avant chaque regreffe.
- Les rapports et passations des étapes closes ne sont pas modifiés (règle d'ENV-17). Une
  correction se consigne dans le rapport d'ENV-22.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, branche, décisions PA-31 et PA-32, journal. Passation
`handoff/env-22.md`.
