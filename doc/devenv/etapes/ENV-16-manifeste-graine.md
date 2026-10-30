# Étape ENV-16 — Graine de référence et `lepton check`

## Contexte
`lepton check` sur `<ROOTSTOCK>` rend le code 1 avec une seule anomalie : « manifeste de graine
absent (graine hors lepton) » (`lepton/checks.py`, constat d'ENV-12, admis en ENV-14). La graine
publiée `original-tree` (ENV-13) est une graine de référence : elle assemble le noyau, 3 familles,
4 BSP et sert 14 presets. Or `schemas/graine.schema.json` décrit une graine de projet : `projet`,
`noyau`, `bsp`, `backend`, `configurations` et `mklepton_xml` sont requis, avec un seul BSP, un
seul backend et un seul XML. Cette étape fait rendre 0 à `lepton check` sur `<ROOTSTOCK>`, sans
affaiblir le contrôle des graines de projet. Archétype : infrastructure.

## Prérequis
- ENV-13 terminée (graine `original-tree` publiée). ENV-15 non requise (indépendante).
- lepton 0.1.0 ; schémas `schemas/graine.schema.json`, `schemas/greffon.schema.json`.
- Décision de l'utilisateur du 2026-10-30 : étape séparée d'ENV-15 (`DEVENV-STATUS.md` §Décisions).
- Branche `devenv/env-16` : lepton-tools (depuis `main`) ; graine `original-tree` seulement si le
  PA-19 retient un manifeste dans la graine.

## Tâches

### 1. Audit (lecture seule) → PA-19
- Lire `lepton/checks.py` (contrôle de la graine, `check_seed`), `schemas/graine.schema.json` et
  ses exemples (`schemas/exemples/`), `rapports/env-8-interface.md` (code de retour de `check`).
- Recenser ce qu'un manifeste devrait déclarer pour `original-tree` : greffons, rôles, presets, XML
  mkconf (`CMakePresets.json` du noyau, `LEPTON_MKCONF`).
- Présenter au **PA-19** les options, avec leurs conséquences sur le schéma, sur `lepton check`, sur
  les autres commandes de `lepton` qui lisent le manifeste (`seed status`, `generate`, extension) et
  sur la graine publiée :
  - A : manifeste `lepton-graine.json` dans `original-tree`, avec un schéma étendu (type de graine
    « référence » : plusieurs BSP, configurations portées par les presets) ;
  - B : `lepton check` reconnaît une graine sans manifeste comme graine de référence (critère
    <À CONFIRMER au PA-19>) et rend 0, avec un message d'information ;
  - C : autre proposition issue de l'audit.
- Aucune modification avant la réponse.

### 2. Implémentation
Selon le PA-19 ; commits séparés : schéma, code, exemples et tests, graine.
- Schéma modifié : `scripts/valider-schemas.sh` vert, exemples valides et invalides complétés.
- `lepton` : tests `pytest` (venv `~/lepton-tools-dev/venv-lepton-tools`) verts ; réinstallation
  pipx de lepton.
- Graine (option A) : commit sur `devenv/env-16` du clone `depots/lepton-seed.scions/original-tree`.

### 3. Contrôles → PA-20
- `lepton check` sur `<ROOTSTOCK>` : code 0.
- `lepton check` sur les rootstocks d'essai `essais/env-9` et `essais/env-11/*` (graines de projet) :
  mêmes résultats qu'avant l'étape (relevés avant toute modification).
- Une graine de projet invalide reste refusée (test).
- Rapport `doc/devenv/rapports/env-16-graine.md`.
- **PA-20** : push de `devenv/env-16` (lepton-tools) et, pour l'option A, de la graine
  `original-tree` (PA-P) ; fusion dans `main`.

## Critères de validation
- [ ] PA-19 et PA-20 tranchés et consignés.
- [ ] `lepton check` sur `<ROOTSTOCK>` : code 0.
- [ ] Graines de projet des rootstocks d'essai : résultats de `lepton check` inchangés.
- [ ] Schémas valides (`valider-schemas.sh`) ; tests de lepton verts.
- [ ] Commandes de `lepton` qui lisent le manifeste : comportement sur `<ROOTSTOCK>` relevé et sans régression.

## Pièges connus
- Un manifeste ajouté à `original-tree` est lu par tout rootstock greffé depuis la graine publiée :
  `seed status`, `generate` et l'extension changent de comportement. Les relever avant le PA-19.
- `lepton check` rend 1 aujourd'hui pour cette seule anomalie : ne pas masquer d'autres anomalies
  en assouplissant le code de retour en bloc.
- Push de la graine : PA-P ; `original-tree` est la graine de référence publique (ENV-13).

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, décisions PA-19 et PA-20, journal ; version de lepton si elle change.
Passation `handoff/env-16.md`.
