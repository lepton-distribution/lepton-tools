# Étape ENV-18 — Graine de référence gérée par `lepton`

## Contexte
Depuis ENV-16 (option C), `lepton check` reconnaît la graine de référence `original-tree` (ni
`lepton-graine.json` ni `project/`) et la contrôle par ses greffons. Les autres commandes la
traitent encore comme une graine étrangère (`rapports/env-16-graine.md` §1.2) : `seed status`
affiche « graine hors lepton », `generate` refuse (« la graine n'est pas une graine lepton »).
On ne peut donc pas ouvrir l'arbre de référence `<ROOTSTOCK>` dans VSCodium par `lepton generate`.
Décision de l'utilisateur (2026-10-31) : les commandes de lecture et `generate` acceptent la graine
de référence ; les commandes qui modifient la graine la refusent avec un message explicite.
Archétype : création (prolonge ENV-16).

## Prérequis
- ENV-16 terminée (critère de reconnaissance de la graine de référence dans `lepton/checks.py`).
- lepton 0.1.0, extension 0.5.1 (`DEVENV-STATUS.md` §Versions).
- Rootstock d'essai issu de la graine publiée : `~/lepton-tools-dev/essais/env-13-vierge`.
- Branche `devenv/env-18` : lepton-tools (depuis `main`). Graine `original-tree` non modifiée.

## Tâches

### 1. Audit (lecture seule) → PA-23
- Lire les lecteurs du manifeste recensés en `rapports/env-16-graine.md` §1.2 (`status_data`,
  `seed tree`, `tree._presets`, `generate` / `Context`, `load_graine`) et `rapports/env-9-generation.md`
  (fichiers produits par `generate`).
- Pour la graine de référence, établir ce que chaque commande doit lire à la place du manifeste :
  presets du noyau (`CMakePresets.json`) dont le BSP est greffé, backend et XML par preset (même
  règle qu'ENV-16), greffons et rôles déduits des types de manifeste de greffon.
- Relever les fichiers que `generate` écrit pour une graine de projet et leur emplacement :
  `CMakeUserPresets.json` (greffon local `project-<projet>`), `<ROOTSTOCK>/<projet>.code-workspace`,
  `build/.active/`.
- Relevé de référence avant toute modification : sorties de `seed status --json`, `seed tree`,
  `file owner`, et fichiers produits par `generate` sur les rootstocks d'essai à graine de projet
  (`essais/env-9`, `essais/env-11/*`).
- Présenter au **PA-23** :
  - la liste des commandes acceptées et refusées, et le texte et le code de retour du refus (codes
    de `rapports/env-8-interface.md`) ;
  - le nom de l'espace de travail produit sans `projet.nom` : <À CONFIRMER au PA-23> ;
  - le sort de `CMakeUserPresets.json` sans greffon projet (ne rien écrire dans la graine publiée ;
    presets du noyau utilisés directement, ou autre) : <À CONFIRMER au PA-23> ;
  - l'ensemble des presets offerts (presets à BSP non greffé exclus, `host` compris ou non) ;
  - le comportement attendu de l'extension (vue IDE-1, palette, diagnostics) sur cet espace.
- Aucune modification avant la réponse.

### 2. Implémentation
- Commits séparés : lecture de la graine de référence (`seed status`, `seed tree`, `file owner`),
  `generate`, refus explicites, tests.
- Tests `pytest` (venv `~/lepton-tools-dev/venv-lepton-tools`) : graine de référence acceptée par
  les commandes retenues, refus par les autres, graines de projet inchangées.
- Extension : modification seulement si le PA-23 le demande (règle « aucune logique dans
  `extension/` ») ; sinon relancer et constater.
- Réinstallation de lepton : `pipx install --force <LEPTON_TOOLS>`.

### 3. Contrôles → PA-24
- Sur `essais/env-13-vierge` d'abord, puis sur `<ROOTSTOCK>` : `seed status` sans « graine hors
  lepton » ; `generate` code 0 ; espace ouvert dans VSCodium avec l'utilisateur : configuration et
  construction d'un preset QEMU, clangd sur `build/.active/`, F5 sur `qemu-mps2-an386-freertos`.
- Graines de projet : sorties et fichiers produits identiques au relevé de la tâche 1 (`diff`).
- Rapport `doc/devenv/rapports/env-18-graine.md`.
- **PA-24** : présenter le rapport ; push de `devenv/env-18`, fusion dans `main`, push (PA-P).

## Critères de validation
- [ ] PA-23 et PA-24 tranchés et consignés.
- [ ] Commandes retenues : code 0 sur `<ROOTSTOCK>` et `essais/env-13-vierge` ; commandes refusées : message et code validés.
- [ ] Graines de projet : `diff` vide contre le relevé de référence.
- [ ] Tests de lepton verts ; essai VSCodium sur l'arbre de référence conforme.

## Pièges connus
- Les lecteurs indexent directement les champs de graine de projet (37 accès, `graine["bsp"]`) :
  un chemin de code oublié lève `KeyError` au lieu d'un refus.
- `generate` sur `<ROOTSTOCK>` écrit hors du trunk (`*.code-workspace`, `build/.active/`) : rien
  sous `trunk/`, rien dans la graine publiée.
- lepton n'est pas réinstallé sur Debian par cette étape : validation Debian en ENV-21.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, décisions PA-23 et PA-24, version de lepton réinstallée, journal.
Passation `handoff/env-18.md`.
