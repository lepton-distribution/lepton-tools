# Étape ENV-10 — Script d'installation de VSCodium

## Contexte
Le script installe VSCodium, les extensions nécessaires depuis Open VSX, scion et `lepton`, sur
macOS Intel, macOS Apple Silicon et Debian (INS-1 à INS-6). Il réutilise les scripts d'installation
de la chaîne au lieu de les dupliquer. Étape indépendante : peut être faite à tout moment après
ENV-0 ; `lepton` n'est installable qu'après ENV-8.

## Prérequis
- ENV-0 terminée. `env-2-outillage.md` (emplacement de `install-macos.sh` / `install-debian.sh`)
  si ENV-2 est faite ; sinon relever cet emplacement en début d'étape.
- Branche `devenv/env-10` dans `lepton-tools`.

## Tâches

### 1. Liste d'extensions — point d'arrêt PA-10
Pour chaque extension, vérifier sur Open VSX (`https://open-vsx.org/api/<éditeur>/<nom>`) : nom
exact, dernière version stable, dépendances. Liste de départ (SPECIFICATION §A) : clangd, CMake
Tools, Cortex-Debug et ses dépendances, CodeLLDB, une extension XML avec XSD, Claude Code.
Pour l'extension XML : vérifier qu'elle fonctionne sans Java sur les trois hôtes (binaire natif
macOS x86_64, macOS arm64, Linux x86_64). Présenter la liste avec versions ; attendre PA-10.
Écrire `scripts/extensions.lst` (une ligne `éditeur.nom@version`).

### 2. `scripts/install-vscodium.sh`
- En-tête : usage, options, hôtes (NF-6). Une fonction par étape ; `set -euo pipefail`.
- Options : `--dry-run` (affiche sans exécuter), `--skip-toolchain`, `--no-lepton`.
- Détection de l'hôte : `uname -s` et `uname -m` (Darwin x86_64, Darwin arm64, Linux x86_64) ;
  tout autre hôte → arrêt avec message.
- Mac Intel : gestionnaire MacPorts, comme `install-macos.sh` du portage (Homebrew ne fournit plus
  de binaires pour Intel). VSCodium : port MacPorts s'il existe <À CONFIRMER : `port info vscodium`>,
  sinon image `.dmg` officielle (GitHub `VSCodium/vscodium`) épinglée par version et vérifiée par
  sa somme SHA-256 publiée, copiée dans `/Applications`.
- Mac Apple Silicon : Homebrew (`brew install --cask vscodium`), préfixe par `brew --prefix`.
- Aucun préfixe (`/opt/local`, `/usr/local`, `/opt/homebrew`) codé en dur (INS-5).
- Debian : dépôt APT officiel de VSCodium <À CONFIRMER : méthode et clé relevées au moment de
  l'écriture> ou paquet `.deb` épinglé.
- Chaîne : appel de `install-macos.sh` / `install-debian.sh` (INS-3), sauf `--skip-toolchain`.
- Extensions : `codium --install-extension <id>@<version>` pour chaque ligne de `extensions.lst`.
- scion : `pipx install` de la version épinglée dans `DEVENV-STATUS.md` ; `lepton` :
  `pipx install <LEPTON_TOOLS>`.
- Idempotent : chaque fonction teste l'état avant d'agir.

### 3. Validation
- Mac Intel : exécution complète, puis seconde exécution sans changement.
- VM Debian (session distincte, ORCHESTRATION §2) : même procédure ; rapport
  `doc/devenv/rapports/env-10-debian.md`.
- Apple Silicon : revue seulement (pas de machine) ; consigner les points non testés.

## Critères de validation
- [ ] PA-10 tranché ; `extensions.lst` épinglé.
- [ ] `codium --list-extensions --show-versions` = `extensions.lst` sur Mac et Debian.
- [ ] Deux exécutions successives sans erreur ni changement (INS-4).
- [ ] `grep -n '/usr/local\|/opt/homebrew\|/opt/local' scripts/install-vscodium.sh` vide (INS-5).
- [ ] Le gestionnaire de paquets utilisé est celui d'`install-macos.sh` sur le même hôte.
- [ ] Aucune commande d'installation de la chaîne dans le script (INS-3).
- [ ] `shellcheck` sans erreur.

## Pièges connus
- L'identifiant d'une extension sur Open VSX peut différer de celui du Marketplace Microsoft.
- `codium` n'est pas dans le `PATH` sur macOS après une installation par `.dmg` (et parfois par
  cask) : la commande est dans le paquet de l'application ; vérifier et le signaler, ne pas créer
  de lien dans un répertoire système sans accord.
- Ne pas mélanger MacPorts et Homebrew sur le Mac Intel : deux `openocd` ou deux `cmake` dans le
  `PATH` faussent les versions épinglées.
- Une extension qui télécharge un binaire au premier lancement (serveur de langage) contourne
  l'épinglage : le noter dans le rapport.

## À la fin de l'étape
`DEVENV-STATUS.md` : version de VSCodium, liste d'extensions, hôtes validés. Passation
`handoff/env-10.md`.
