# Étape ENV-12 — Extension VSCodium (phase 2)

## Contexte
L'extension est une couche mince au-dessus de `lepton` (SPECIFICATION §Architecture) : elle
n'ajoute aucune logique propre à Lepton. Elle couvre ce que les extensions standard ne font pas :
regreffe automatique (FIC-1), vue exécutif → bibliothèques → greffons → fichiers (IDE-1),
redirection des créations faites dans le trunk (FIC-3), commandes de palette (IDE-6). Elle n'est
lancée que si ENV-11 montre que la phase 1 ne suffit pas.

## Prérequis
- ENV-11 terminée.
- Point d'arrêt PA-12 : décision de lancer l'étape, liste des fonctions retenues.
- Node.js 22.15.0 (nvm), typescript 5.9.3, `@types/vscode` 1.134.0, `@types/node` 22.20.5,
  `@vscode/vsce` 4.0.0 (2026-10-20) ; `ovsx` installé seulement pour une publication (PA-P) ; branche
  `devenv/env-12` dans `lepton-tools`.

## Tâches

### 1. Point d'arrêt PA-12
Présenter, à partir du bilan d'ENV-11, les fonctions manquantes et leur coût. Attendre la décision.

### 2. Extension
- Répertoire `extension/` dans `lepton-tools`, TypeScript.
- Toute action appelle `lepton` en sous-processus avec sortie JSON (ajouter une option
  `--json` à `lepton` si nécessaire, dans `lepton`, pas dans l'extension).
- Vue arborescente : construite à partir de `lepton seed status --json` et des manifestes.
- Observateur de fichiers sur les clones de greffons : appel de `lepton graft` (avec temporisation)
  après création ou suppression.
- Création demandée dans le trunk : retrouver le greffon propriétaire par `lepton`, créer dans le
  clone ; s'il n'y en a pas, refuser avec un message.
- Commandes de palette pour les opérations de `lepton` déjà existantes.

### 2bis. Renvois des reprises (décidés)
- CFG-7 (reprise 4, décision du 2026-10-16) : diagnostics de l'extension, à la saisie et en
  **erreur**, pour `lepton-greffon.json`, `lepton-graine.json` (JSON Schema) et le XML mklepton
  (XSD), à partir des schémas du paquet lepton ; le service JSON intégré ne signale qu'en
  avertissement (niveau non réglable, `rapports/env-9-r4.md` §5) ; la tâche « lepton : vérifier »
  reste le contrôle complet à la demande.
- O10 (reprise 4) : relance de clangd quand `build/.active/compile_commands.json` apparaît ou
  change (cas sans preset configuré avant `lepton generate`).
- Autres renvois : R1 (`rapports/env-9-validation.md` §4), O2, O5 (`rapports/env-11-bilan.md` §3).

### 3. Distribution
Paquet `.vsix` local ; publication sur Open VSX soumise à accord (PA-P).

## Critères de validation
- [ ] PA-12 tranché.
- [ ] Aucune logique de graine ou de greffon dans `extension/` (revue : uniquement des appels à
      `lepton`).
- [ ] Création de fichier depuis l'explorateur : lien présent dans le trunk sans action manuelle
      (FIC-1) ; aucun fichier régulier dans le trunk (FIC-3).
- [ ] Vue IDE-1 cohérente avec `lepton seed status`.
- [ ] Installation du `.vsix` par `codium --install-extension` sur Mac et Debian.

## Pièges connus
- Un observateur qui regreffe à chaque événement sature scion : regrouper les événements.
- L'API d'extension évolue : épingler la version minimale de VSCodium dans `package.json`.

## À la fin de l'étape
`DEVENV-STATUS.md` : version de l'extension, statut. Passation `handoff/env-12.md`.
