# ENV-10 — Script d'installation de VSCodium : relevés et validation

Session du 2026-10-15, Mac mini Intel (macOS 15.8.1, x86_64). Script :
`scripts/install-vscodium.sh` ; liste : `scripts/extensions.lst` (lepton-tools `devenv/env-10`,
d78afcf). Scripts de la chaîne : `scripts/install-{macos,debian}.sh` du clone noyau
(`devenv/env-10`, 1b2f7b6).

## 1. Relevé Open VSX (PA-10)

| Extension | Retenue | Dernière publiée | Plateformes | Observations |
| --- | --- | --- | --- | --- |
| `llvm-vs-code-extensions.vscode-clangd` | 0.6.0 | 0.6.0 | universelle | clangd pris sur l'hôte (PA-1) ; sans `clangd.path` valide, l'extension propose de télécharger clangd |
| `ms-vscode.cmake-tools` | 1.24.42 | 1.24.42 | universelle | pack déclarant `ms-vscode.cpp-devtools`, absent d'Open VSX : ignoré par `codium` |
| `mcu-debug.debug-tracker-vscode` | 0.0.15 | 0.0.15 | universelle | dépendance de Cortex-Debug |
| `mcu-debug.memory-view` | 0.0.29 | 0.0.29 | universelle | idem |
| `mcu-debug.rtos-views` | 0.0.16 | 0.0.16 | universelle | idem |
| `mcu-debug.peripheral-viewer` | 1.6.4 | 1.6.5 (2026-10-15, VSCodium ≥ 1.107) | universelle | version validée en ENV-1 / ENV-9 |
| `marus25.cortex-debug` | 1.13.0-pre6 | 1.13.0-pre6 | universelle | servie comme `latest` sans marque de pré-version ; stable précédente 1.12.1 |
| `vadimcn.vscode-lldb` | 1.12.3 | 1.12.3 | Open VSX : amorce seule | l'amorce (10 fichiers, sans adaptateur) télécharge `codelldb-<plateforme>.vsix` depuis GitHub au premier lancement ; le script installe ce paquet lui-même (release v1.12.3, SHA-256 épinglé) |
| `redhat.vscode-xml` | 0.29.3 | 0.29.2026101508 (pré-version quotidienne) | darwin-x64, darwin-arm64, linux-x64 | chaque VSIX de plateforme embarque lemminx natif (`lemminx-osx-x86_64`, `lemminx-osx-aarch_64`, `lemminx-linux-x86_64`) et sa somme ; Mach-O x86_64 vérifié, somme conforme : fonctionne sans Java |
| `anthropic.claude-code` | 2.1.300 | 2.1.300 | darwin-x64, darwin-arm64, linux-x64 | une version paraît presque chaque jour |

VSCodium : releases GitHub `VSCodium/vscodium` ; 1.135.06055 retenue (validée en ENV-1 / ENV-9),
dernière 1.140.06880 (2026-10-13). Sommes publiées (`.sha256`) reprises dans le script :
`.dmg` x64 et arm64, `.deb` amd64. Le dépôt APT `download.vscodium.com/debs` ne sert que la dernière
version (épinglage impossible) ; le cask Homebrew non plus ; pas de port MacPorts `vscodium`.

## 2. Exécution sur Mac Intel

État de départ : VSCodium 1.135.06055 installé par Homebrew cask, 7 extensions (ENV-1),
réglages utilisateur sans les clés PA-10.

1. `shellcheck` 0.11.0 (MacPorts) : `install-vscodium.sh`, `install-macos.sh`,
   `install-debian.sh` sans remarque.
2. `--dry-run` : contrôles d'état seuls, 5 actions annoncées ; `--bogus` → code 2 et usage ;
   sans `--lepton-clone` ni `$LEPTON_CLONE` → arrêt avec la marche à suivre.
3. `brew uninstall --cask vscodium` (accord de l'utilisateur, D3). **Effet de bord** : Homebrew a
   enchaîné son nettoyage automatique et retiré des formules jugées inutilisées, au moins
   `imath` 3.1.12 (3.1.4 reste) et `libdeflate` 1.22 (absente depuis) ; liste complète non
   conservée. Sans effet sur la chaîne (MacPorts). Le lien `codium` du cask a disparu.
4. Exécution n° 1 (`--lepton-clone ~/lepton/depots/lepton/original/master --seed-scions
   ~/lepton-tools-dev/seed.scions`) : code 0, **5 changements** — `.dmg` téléchargé, somme
   vérifiée, `VSCodium.app` copiée (signature `com.vscodium`, équipe VC39D2VNQ7) ; CodeLLDB
   `codelldb-darwin-x64.vsix` (adaptateur présent) ; vscode-xml et Claude Code (VSIX darwin-x64) ;
   réglages fusionnés (`settings.json.bak` créé). `install-macos.sh --with-debug-tools` : tout
   « déjà installé », aucun `port install`, scion laissé en 0.5.1.0 (`SCION_REF`/`SCION_SPEC`).
5. Exécution n° 2 : code 0, **0 changement**, aucune commande `sudo`.

## 3. Critères d'ENV-10

| Critère | Résultat |
| --- | --- |
| PA-10 tranché ; `extensions.lst` épinglé | oui (`DEVENV-STATUS.md` §Décisions, 2026-10-15) |
| `codium --list-extensions --show-versions` = `extensions.lst` | Mac : identique (`diff` vide) ; Debian : à faire |
| Deux exécutions successives sans erreur ni changement (INS-4) | Mac : oui (5 puis 0) ; Debian : à faire |
| `grep -n '/usr/local\|/opt/homebrew\|/opt/local'` vide (INS-5) | oui |
| Gestionnaire = celui d'`install-macos.sh` | oui : le script n'appelle aucun gestionnaire sur macOS ; `install-macos.sh` choisit MacPorts sur Intel |
| Aucune commande d'installation de la chaîne (INS-3) | oui : seul `apt-get install` du `.deb` de VSCodium (Debian) |
| `shellcheck` sans erreur | oui |
| INS-6 : `scion version`, `lepton --version` | 0.5.1.0 ; lepton 0.1.0 |

`pytest -q` (lepton-tools) : 116 passed.

## 4. Points ouverts et non testés

- **`codium` hors du PATH** après installation par `.dmg` : signalé par le script, aucun lien créé.
  Le cask en créait un dans le préfixe Homebrew. Choix à faire par l'utilisateur : PATH (ligne
  affichée) ou commande « Install 'codium' command in PATH » de VSCodium.
- **lemminx natif** : binaire présent, `xml.server.preferBinary` réglé ; Java (JDK 25) présent sur
  ce Mac, le choix effectif du binaire à l'exécution reste à constater dans l'éditeur (ENV-11,
  CFG-7).
- **scion 0.5.1.0 hors réseau local** : le tag n'est pas sur GitHub. Sans `--seed-scions`, la source
  par défaut (`github.com/lepton-distribution/seed.scions@0.5.1.0`) échoue tant qu'il n'est pas
  poussé (PA-P). Lancé seul, `install-macos.sh` / `install-debian.sh` gardent leur défaut 0.5.0.1 et
  rétrogradent scion : défaut à relever après le push.
- **Binaires téléchargés au premier lancement** (contournement de l'épinglage) : aucun pour
  CodeLLDB (paquet complet), vscode-xml (lemminx embarqué), Claude Code (VSIX de plateforme) ;
  clangd seulement si `clangd.path` est invalide.
- **Apple Silicon** (revue seule, pas de machine) : `.dmg` arm64 et `codelldb-darwin-arm64.vsix`
  (sommes relevées, non téléchargés) ; garde Rosetta ; `install-macos.sh` choisit Homebrew et
  `brew --prefix` ; `PlistBuddy` et `hdiutil` identiques ; extensions de plateforme darwin-arm64
  publiées pour vscode-xml et Claude Code.
- **Debian** (session VM distincte) : version renvoyée par `dpkg-query` pour le `.deb` GitHub à
  confirmer égale à `1.135.06055` ; `install-debian.sh` relancé à chaque exécution
  (`apt-get update`, `apt-get install` sans effet si à jour) ; rapport attendu
  `rapports/env-10-debian.md`.
