# Extension Lepton pour VSCodium

Couche mince au-dessus de l'outil `lepton` (ENV-12, `doc/devenv/etapes/ENV-12-extension.md`) :
chaque action appelle `lepton` en sous-processus ; l'extension ne contient aucune logique de graine
ni de greffon.

Version 0.1.0 (lot 1) : commandes de palette « Lepton : … » (IDE-6) — état, ajout, retrait,
remplacement et verrou de la graine ; création et retrait de greffons ; création, retrait et
déplacement de fichiers et de répertoires (aussi par le menu contextuel de l'explorateur) ;
regreffe ; vérification ; génération. Sortie de `lepton` dans le canal « Lepton ».

Version 0.2.0 (lot 3), active dès l'ouverture d'un espace :
- regreffe automatique (FIC-1) : création ou suppression de fichiers sous `scion/` d'un clone
  greffé (éditeur, terminal, git) → `lepton graft --path …`, événements regroupés ;
- redirection des créations du trunk (FIC-3) : un fichier régulier créé dans le trunk
  (« Nouveau fichier » de l'explorateur) est déplacé dans le clone de son greffon
  (`lepton file owner --json`, puis `lepton file add --adopt`) ; plusieurs greffons possibles :
  choix parmi eux ; aucun : choix d'un greffon ou suppression du fichier ; fichier laissé dans le
  trunk : notification d'erreur avec « Supprimer du trunk » (toute regreffe est bloquée tant qu'il
  reste ; `lepton check` le signale) ;
- relance de clangd quand le contenu de `compile_commands.json` (`--compile-commands-dir` de
  `clangd.arguments`) change : nouveau preset configuré, changement de preset (O10, R1) ; et quand
  un en-tête est créé sous un répertoire de construction de cette base (en-têtes générés à la
  première construction d'un preset, que clangd ne relit pas de lui-même) ;
- interface en anglais, traduite en français (`package.nls.fr.json`, `l10n/`) ; langue de
  VSCodium (pack de langue et `locale` réglés par `install-vscodium.sh`) ; messages de `lepton`
  en français.

Version 0.3.0 (lot 4) : erreurs des manifestes à la saisie (CFG-7, `lepton check --json --stdin`)
et contrôle complet à l'enregistrement d'un manifeste ou du XML mklepton, dans *Problèmes*.

Version 0.4.0 (lot 5) : vue « Architecture » (IDE-1, `lepton seed tree --json`) — exécutif →
bibliothèques → greffons → répertoires → fichiers ; suppression d'un lien greffé dans le trunk :
« Supprimer du greffon » ou « Restaurer le lien » (L3-4).

Version 0.5.0 (lot 6) :
- palette : ajout et retrait d'une configuration de la graine (`lepton seed config add/remove`),
  import d'un XML mklepton de référence (`lepton seed mkconf import`, aussi par le menu contextuel
  d'un `.xml`) ;
- débogage (F8) : à l'arrêt, sources de la pile et des points d'arrêt ouvertes par leur lien du
  trunk, et non sous le chemin du clone que rend gdb (`stem` et `trunk` de
  `lepton seed status --json`).

Version 0.5.1 (lot 6 S2) : traceur F8 sans attente (L6-6).

Réglages : `lepton.path` (vide : `~/.local/bin/lepton`, sinon `lepton` du `PATH`) ;
`lepton.autoGraft.enabled`, `lepton.autoGraft.delay` (ms, défaut 1000) ;
`lepton.redirectTrunkCreations` ; `lepton.confirmTrunkDeletions` ; `lepton.restartClangd` ;
`lepton.diagnostics.enabled`, `lepton.diagnostics.delay` (ms, défaut 400) ;
`lepton.debug.trunkPaths`. Les commandes s'exécutent une à une dans le répertoire de l'espace
ouvert (`<rootstock>/<projet>.code-workspace` généré par `lepton generate`).

Installation : `scripts/install-vscodium.sh` installe `dist/lepton-<version>.vsix`, versionné dans
ce dépôt, si la version installée diffère.

Construction (Node ≥ 22, versions épinglées dans `package.json`) ; à chaque changement de version,
commiter le `.vsix` de `dist/` (un seul, celui de la version : contrôlé par `npm test`) :

```
npm ci
npm test                 # compilation et tests node:test
npm run package          # compilation, puis dist/lepton-<version>.vsix (remplace le précédent)
codium --install-extension dist/lepton-<version>.vsix --force
```
