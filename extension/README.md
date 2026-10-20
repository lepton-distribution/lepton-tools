# Extension Lepton pour VSCodium

Couche mince au-dessus de l'outil `lepton` (ENV-12, `doc/devenv/etapes/ENV-12-extension.md`) :
chaque action appelle `lepton` en sous-processus ; l'extension ne contient aucune logique de graine
ni de greffon.

Version 0.1.0 (lot 1) : commandes de palette « Lepton : … » (IDE-6) — état, ajout, retrait,
remplacement et verrou de la graine ; création et retrait de greffons ; création, retrait et
déplacement de fichiers et de répertoires (aussi par le menu contextuel de l'explorateur) ;
regreffe ; vérification ; génération. Sortie de `lepton` dans le canal « Lepton ».

Réglage : `lepton.path` (vide : `~/.local/bin/lepton`, sinon `lepton` du `PATH`). Les commandes
s'exécutent dans le répertoire de l'espace ouvert (`<rootstock>/<projet>.code-workspace` généré par
`lepton generate`).

Construction (Node ≥ 22, versions épinglées dans `package.json`) :

```
npm ci
npm test                 # compilation et tests node:test
npm run package          # lepton-0.1.0.vsix
codium --install-extension lepton-0.1.0.vsix
```
