# ENV-10 — Validation Debian de install-vscodium.sh — passage n° 3 — 2026-10-15

Session VM conduite selon `doc/devenv/consignes/env-10-debian.md` (passage n° 3), sur
`devenv/env-10` 96264cf (corrections 9321eed et 1b43b0b incluses). **Validation conforme** depuis
un hôte vierge : exécution n° 1 code 0 (13 changements), exécution n° 2 code 0, `changements 0` ;
critères INS-1 à INS-6, extensions, binaires natifs et shellcheck conformes (§3).

Un premier essai de l'exécution n° 1 a échoué faute de place dans `/tmp` sur la VM (§2.3, §6.4) :
cause propre à la VM, levée sans modifier le script (accord de l'utilisateur).

Les passages n° 1 et n° 2 sont résumés en historique (§7).

## 1. Hôte

| Élément | Valeur |
| --- | --- |
| Système | Debian GNU/Linux 13 (trixie), `/etc/debian_version` 13.7, Linux x86_64 |
| Noyau | 6.12.107+deb13-amd64 |
| Utilisateur | `lepton-user` |
| sudo | demande un mot de passe : exécutions réelles lancées par l'utilisateur (consigne §5.1) |
| git / curl / python3 / pipx | git 2.47.3, curl présent, Python 3.13.5, pipx 1.7.1 (paquet Debian) |
| `~/.local/bin` dans le `PATH` | oui |
| codium | absent ; pas de dépôt APT VSCodium ; ni `~/.config/VSCodium` ni `~/.vscode-oss` (hôte vierge) |
| scion | 0.5.0.1 (pipx) au départ |
| lepton | absent |
| shellcheck | 0.10.0 |
| `/tmp` | partition séparée de 747 Mo (§6.4) |

Têtes des clones :

| Dépôt | Référence | Tête constatée |
| --- | --- | --- |
| `lepton-tools` | `devenv/env-10` | 96264cf = `origin/devenv/env-10` (conforme) ; rapport sur `devenv/env-10-debian`, recréée depuis 96264cf (rapports n° 1 et n° 2 fusionnés en 61d1a8b) |
| `lepton-noyau` (`lepton-original-tree.scions`) | `devenv/env-10` | 1b2f7b6 (conforme) |
| `seed.scions` | tag `0.5.1.0` | 79f4f96 (conforme) |

## 2. Exécutions

Journaux sur la VM : `~/env-10-journaux/`.

### 2.1 shellcheck et dry-run (Claude)

- `shellcheck` 0.10.0 sur `install-vscodium.sh` et `install-debian.sh` : **sans remarque** (SC2015
  du passage n° 2 levée).
- Dry-run (`0-dry-run.log`) : **code 0**, toutes les sections atteintes ; 16 actions annoncées ;
  spécification scion `scion @ git+file:///home/lepton-user/lepton-tools-dev/seed.scions@0.5.1.0`.

### 2.2 Exécutions n° 1 et n° 2 (utilisateur)

Lancées avec les commandes de la consigne §5.2, précédées de `TMPDIR=$HOME/env-10-tmp` (§2.3).

| Exécution | Code | Changements | Durée |
| --- | --- | --- | --- |
| n° 1 (`1-execution.log`) | 0 | 13 | ≈ 1 min (16:03:24 → 16:04:20) |
| n° 2 (`2-execution.log`) | 0 | **0** | ≈ 15 s |

Exécution n° 1 :
- `install-debian.sh` : `apt-get update`, tous les paquets déjà à jour.
- scion : « déjà installé » (0.5.1.0, installé par l'essai du §2.3).
- VSCodium : `.deb` téléchargé, SHA-256 vérifié, `sudo apt-get install` → `codium (1.135.06055)`.
- 10 extensions installées (9 lignes d'`extensions.lst`, CodeLLDB par `codelldb-linux-x64.vsix`).
  Chaque appel `codium` affiche un avertissement Node `DEP0169` (`url.parse()`), sans effet.
- Réglages : 5 clés ajoutées à `~/.config/VSCodium/User/settings.json`.
- lepton : `pipx install --force` du dépôt → `lepton 0.1.0`.

Exécution n° 2 : chaque section « déjà installé(e) » ou « déjà conformes » ; aucun `sudo` dans le
journal hors `install-debian.sh` (rejoué à chaque exécution, non compté, comportement voulu).

### 2.3 Premier essai de l'exécution n° 1 (échec, cause propre à la VM)

`passage-3-essai-1-execution.log` : `install-debian.sh` installe scion 0.5.1.0 depuis
`scion @ git+file://…` (correction 1b43b0b constatée), puis `installer_vscodium` échoue en code 1 :

```
curl: (23) Failure writing output to destination, passed 16375 returned 3282
ERREUR: téléchargement de https://github.com/VSCodium/vscodium/releases/download/1.135.06055/codium_1.135.06055_amd64.deb impossible : vérifier le réseau, puis rejouer.
```

Cause : `telecharger` écrit dans `mktemp -d`, sous `/tmp` ; `/tmp` est une partition de 747 Mo,
132 Mo libres, pour un `.deb` de 168 Mo. 161 Mo étaient occupés par la copie de contrôle du `.deb`
téléchargée par la session du passage n° 1 et non effacée. Accord de l'utilisateur : copie
supprimée (292 Mo libres) **et** exécutions rejouées avec `TMPDIR=$HOME/env-10-tmp`. Script non
modifié.

## 3. Critères d'ENV-10

| Critère | Attendu | Résultat |
| --- | --- | --- |
| INS-1 | `codium --version` = 1.135.06055 ; `dpkg-query` = `1.135.06055` | **Conforme** : `1.135.06055` / commit `1a46a584…` / `x64` ; `dpkg-query` → `1.135.06055` |
| INS-2 | `diff` attendues / installées vide | **Conforme** : « extensions conformes » (10 extensions, versions épinglées) |
| INS-3 | seul `apt-get install` du `.deb` dans le script ; chaîne par `install-debian.sh` | **Conforme** : `apt-get` du script limité au `.deb` (`installer_vscodium_deb`, lignes 221/227/229, plus le message d'erreur ligne 187) ; chaîne vérifiée par `install-debian.sh` (déjà à jour) |
| INS-4 | deux exécutions code 0, la seconde `changements 0` ; aucun `sudo` effectif à la seconde hors `install-debian.sh` | **Conforme** |
| INS-5 | aucun préfixe `/usr/local`, `/opt/homebrew`, `/opt/local` ; APT | **Conforme** : `grep` vide ; APT seulement |
| INS-6 | `scion version` → 0.5.1.0 ; `lepton --version` → `lepton 0.1.0` | **Conforme** : `scion version: 0.5.1.0` ; `lepton 0.1.0` (suivi de `scion 0.5.1.0 (requis ≥ 0.5.1.0)`) |
| NF-6 / shellcheck | sans remarque | **Conforme** (shellcheck 0.10.0) |
| Binaires au premier lancement | CodeLLDB `adapter/codelldb`, lemminx linux | **Conforme** : `vadimcn.vscode-lldb-1.12.3/adapter/codelldb` présent ; `lemminx-linux-x86_64` (+ `.sha256`) présent |
| Réglages | 5 clés | **Conforme** : `update.mode` `none`, `extensions.autoUpdate` / `autoCheckUpdates` / `redhat.telemetry.enabled` `false`, `xml.server.preferBinary` `true` |

Vérification graphique facultative (ouverture de VSCodium) : non faite.

## 4. Chaîne relevée par install-debian.sh (information)

Aucun paquet ajouté (tout était à jour).

| Outil | Version |
| --- | --- |
| arm-none-eabi-gcc | 14.2.1 20241119 (paquet 15:14.2.rel1-1) ; newlib-nano OK |
| cmake | 3.31.6 |
| ninja | 1.12.1 |
| qemu-system-arm | 10.0.13 (Debian 1:10.0.13+ds-0+deb13u1) |
| openocd | 0.12.0 (paquet 0.12.0-3+b2) |
| gdb | `gdb-multiarch`, GNU gdb (Debian 16.3-1) 16.3 |
| cloc / spatch | 2.04 / 1.3 |
| doxygen | 1.9.8 |

Remarques sur le script du noyau (information, non bloquantes) : la ligne « openocd » de son
récapitulatif est vide (`openocd --version` écrit sur la sortie d'erreur) ; l'installation pip de
Graphify n'aboutit pas (avertissement prévu, étape optionnelle).

## 5. Corrections propres à Debian

Aucune.

## 6. Points ouverts

### 6.1 Arrêt silencieux sans extension installée (passage n° 1) — corrigé, constaté

9321eed : l'exécution n° 1 depuis un hôte sans extension va jusqu'au bilan.

### 6.2 Spécification pipx `git+file://` refusée (passage n° 2) — corrigé, constaté

1b43b0b : pipx 1.7.1 installe scion 0.5.1.0 depuis `scion @ git+file://…@0.5.1.0` (§2.3), par
`install-debian.sh` ; `installer_scion` le trouve ensuite « déjà installé ».

### 6.3 SC2015 sur `version_vscodium` (passage n° 2) — corrigé, constaté

1b43b0b : shellcheck 0.10.0 sans remarque.

### 6.4 Place dans le répertoire temporaire (pour la session Mac, non bloquant)

- Constat propre à la VM (`/tmp` de 747 Mo), mais deux faiblesses du script communes à tous les
  hôtes : `telecharger` attribue tout échec de curl au réseau (« vérifier le réseau ») alors que le
  code 23 est une erreur d'écriture ; le script ne contrôle pas la place libre de `$TMP` avant de
  télécharger le `.deb` (168 Mo) puis le `.vsix`.
- Suggestions (non appliquées, non validées) : message qui cite le chemin de destination et
  `TMPDIR` ; ou contrôle `df` de `$TMP` avant le téléchargement ; documenter `TMPDIR` dans l'aide.

### 6.5 Divers (information)

- Après l'exécution n° 1, un répertoire vide `~/env-10-tmp/BGVft9pN` (créé à 16:04:19, fin de
  l'exécution n° 1) subsiste dans `TMPDIR` ; le `$TMP` du script, lui, est bien supprimé. Origine
  non déterminée (vraisemblablement un appel `codium` ou `pipx`, qui suivent `TMPDIR`) ; sans effet.
- Avertissement Node `DEP0169` à chaque `codium --install-extension` (VSCodium 1.135.06055) ; sans
  effet.

## 7. Historique

### Passage n° 2 (2026-10-15, sur 53355fb) — interrompu

- Dry-run complet (code 0) : défaut du passage n° 1 corrigé.
- Exécution n° 1 en code 1 dans `installer_scion` : pipx 1.7.1 refuse `git+file:///…@0.5.1.0`
  (URL sans hôte, `pipx/package_specifier.py:82`) ; forme PEP 508 nommée acceptée. Défaut commun,
  corrigé en 1b43b0b (§6.2).
- shellcheck 0.10.0 : SC2015 (info) sur `version_vscodium`, branche macOS ; corrigé en 1b43b0b (§6.3).
- État laissé : inchangé hors `apt-get update`.

### Passage n° 1 (2026-10-15, sur 0e287ea) — interrompu

- Dry-run seulement : sortie en code 1 sans message après la dernière extension
  (`installer_extensions`, `grep -v '^$'` sans ligne sous `pipefail`, `$installees` vide sur hôte
  vierge). Défaut commun, corrigé en 9321eed (§6.1).
- Contrôle complémentaire : `.deb` `codium_1.135.06055_amd64.deb`, SHA-256 `5f5c00a9…f3d8649`
  identique à `VSCODIUM_SHA256_LINUX_AMD64` ; `dpkg-deb -f` → `Version: 1.135.06055` (forme dpkg
  exacte, point ouvert du rapport Mac §4 levé). Cette copie, restée dans `/tmp`, a causé l'échec du
  §2.3.
