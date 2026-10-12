# Étape ENV-0 — Cadrage

## Contexte
Première étape du chantier « environnement de développement Lepton » (voir `SPECIFICATION.md`).
Elle installe le dépôt `lepton-tools`, résout les emplacements de travail et relève les versions
des outils de l'hôte macOS Intel. Aucun code n'est écrit ; aucun dépôt existant n'est modifié.

## Prérequis
- Le portage GCC de Lepton est terminé (dépôts `lepton-distribution/lepton-seed.scions`,
  `lepton-distribution/lepton-original-tree.scions`, `lepton-distribution/seed.scions`).
- `scion` 0.5.0.1 installé (`pipx install "git+https://github.com/lepton-distribution/seed.scions.git@0.5.0.1"`).
- Les fichiers de ce plan sont présents dans un répertoire `lepton-tools/`.

## Tâches

### 1. Point d'arrêt PA-0 — emplacements
Demander à l'utilisateur, et ne rien créer avant sa réponse :
- `<LEPTON_TOOLS>` : chemin du dépôt `lepton-tools` sur le Mac.
- `<ROOTSTOCK>` : réutiliser le rootstock de la migration (donner son chemin) ou en créer un neuf.
- `<SEED_SCIONS>` : chemin d'un clone de `seed.scions` pour ENV-7.
- Branche de départ du clone noyau (`git -C <ROOTSTOCK>/depots/lepton/original/master branch -a`
  pour lui montrer les branches existantes).
- Échange git Mac / VM Debian : dépôt nu local partagé, ou distant GitHub (push soumis à accord),
  ou pas de VM.

### 2. Initialiser le dépôt `lepton-tools`
```bash
cd <LEPTON_TOOLS>
git init -b main
mkdir -p doc/devenv/rapports
git add . && git commit -m "devenv: plan de réalisation (ENV-0 à ENV-12)"
git switch -c devenv/env-0
```
Ne pas créer de distant ; ne pas pousser.

### 3. Vérifier le rootstock
```bash
cd <ROOTSTOCK>
scion version                      # attendu : 0.5.0.1
scion rootstock-information        # scions greffés
find -L trunk -name kal.h          # doit résoudre
find trunk -type f ! -name .scion.grafted.list   # attendu : vide
git -C depots/lepton/original/master status       # attendu : propre
```
Toute anomalie : arrêter et la signaler, ne pas corriger.

### 4. Relever les versions de l'hôte
`cmake --version`, `arm-none-eabi-gcc --version`, `qemu-system-arm --version`,
`openocd --version`, `python3 --version`, `ninja --version`, `port version`, et `command -v` de
chaque outil (le Mac Intel utilise MacPorts ; signaler tout outil venant d'un autre gestionnaire).
Vérifier `cmake` ≥ 3.19 (décision 9 de la spécification) ; sinon point d'arrêt.

### 5. Vérifier le hook
Depuis la session, tenter un `Write` d'un fichier factice sous `<ROOTSTOCK>/trunk/` : le refus du
hook `proteger-trunk.py` est attendu. S'il n'y a pas de refus, s'arrêter (`.claude/settings.json`
non pris en compte, ou `python3` absent du `PATH`).

### 6. Construction de référence
Construire l'image QEMU actuelle depuis le trunk avec le preset existant (le relever par
`cmake --list-presets` dans le trunk), dans `<ROOTSTOCK>/build/<preset>`. Consigner la commande
exacte et le résultat. Capturer son oracle avec la skill `lepton-oracle` dans
`doc/devenv/rapports/oracles/env-0/<preset>/` : c'est l'état de départ du chantier.

## Critères de validation
- [ ] PA-0 tranché ; valeurs recopiées dans `DEVENV-STATUS.md` §Emplacements.
- [ ] `lepton-tools` est un dépôt git, branche `devenv/env-0`, arbre propre.
- [ ] Contrôles de la tâche 3 conformes.
- [ ] Versions de la tâche 4 consignées dans `DEVENV-STATUS.md` §Versions.
- [ ] Hook vérifié (refus constaté).
- [ ] Construction QEMU de référence réussie ; commande consignée ; oracle capturé.

## Pièges connus
- Le clone noyau est dans un répertoire nommé `master` même si une autre branche y est extraite :
  se fier à `git branch --show-current`.
- `scion git` n'affiche pas la sortie de git en 0.5.0.1 : utiliser `git -C`.
- Plusieurs `arm-none-eabi-gcc` possibles sur macOS (MacPorts, Arm GNU Toolchain, ancien Homebrew) :
  `command -v` et consigner celui qui répond.

## À la fin de l'étape
Mettre à jour `DEVENV-STATUS.md` (emplacements, versions, statut ENV-0, journal, prochaine action
ENV-1 ou ENV-2) ; écrire `handoff/env-0.md`.
