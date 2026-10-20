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
  choix parmi eux ; aucun : choix d'un greffon ou suppression du fichier ;
- relance de clangd quand le contenu de `compile_commands.json` (`--compile-commands-dir` de
  `clangd.arguments`) change : nouveau preset configuré, changement de preset (O10, R1) ;
- interface en anglais, traduite en français (`package.nls.fr.json`, `l10n/`) ; langue de
  VSCodium (pack de langue et `locale` réglés par `install-vscodium.sh`) ; messages de `lepton`
  en français.

Réglages : `lepton.path` (vide : `~/.local/bin/lepton`, sinon `lepton` du `PATH`) ;
`lepton.autoGraft.enabled`, `lepton.autoGraft.delay` (ms, défaut 1000) ;
`lepton.redirectTrunkCreations` ; `lepton.restartClangd`. Les commandes s'exécutent une à une dans
le répertoire de l'espace ouvert (`<rootstock>/<projet>.code-workspace` généré par
`lepton generate`).

Construction (Node ≥ 22, versions épinglées dans `package.json`) :

```
npm ci
npm test                 # compilation et tests node:test
npm run package          # lepton-0.2.0.vsix
codium --install-extension lepton-0.2.0.vsix
```
