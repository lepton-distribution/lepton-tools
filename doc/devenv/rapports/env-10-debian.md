# ENV-10 — Validation Debian de install-vscodium.sh — passage n° 2 — 2026-10-15

Session VM conduite selon `doc/devenv/consignes/env-10-debian.md` (passage n° 2), sur
`devenv/env-10` 53355fb (correction 9321eed incluse). **Validation interrompue à l'exécution
n° 1** : le script sort en code 1 dans `installer_scion`, pipx refusant la spécification
`git+file://…` construite par `--seed-scions` (défaut commun à tous les hôtes, §6.2). Le défaut du
passage n° 1 (§6.1) est corrigé : le dry-run va désormais jusqu'au bilan. Décision de
l'utilisateur : arrêter et rapporter, sans correction sur la VM ni écart à la consigne (§5.3).

Le passage n° 1 est conservé en historique (§7).

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
| scion | 0.5.0.1 (pipx) — remplacement par 0.5.1.0 accepté, non abouti (§6.2) |
| lepton | absent |
| shellcheck | 0.10.0 (installé par l'utilisateur depuis le passage n° 1) |

Têtes des clones :

| Dépôt | Référence | Tête constatée |
| --- | --- | --- |
| `lepton-tools` | `devenv/env-10` | 53355fb = `origin/devenv/env-10` (conforme) ; rapport sur `devenv/env-10-debian`, recréée depuis 53355fb (l'ancienne tête 4161720 y est fusionnée) |
| `lepton-noyau` (`lepton-original-tree.scions`) | `devenv/env-10` | 1b2f7b6 (conforme) |
| `seed.scions` | tag `0.5.1.0` | 79f4f96 (conforme) |

## 2. Exécutions

Journaux sur la VM : `~/env-10-journaux/`.

- **shellcheck** (Claude) : `install-debian.sh` sans remarque ; `install-vscodium.sh` : une remarque
  SC2015 (info), ligne 170 (§6.3).
- **Dry-run** (Claude, sans sudo, `0-dry-run.log`) : **code 0**, toutes les sections atteintes
  (chaîne, scion, VSCodium, extensions, réglages, lepton, bilan) ; 16 actions annoncées :
  `install-debian.sh --with-debug-tools`, `pipx install --force` de scion, téléchargement et
  `sudo apt-get install` du `.deb`, 9 extensions (CodeLLDB par le `.vsix` linux-x64), 5 réglages
  ajoutés à `settings.json`, `pipx install --force` de lepton. Le dry-run n'appelle pas pipx et ne
  pouvait donc pas révéler §6.2.
- **Exécution n° 1** (utilisateur, `1-execution.log`) : **code 1**, après environ 1 min.
  - `install-debian.sh` : `apt-get update`, paquets déjà à jour (0 installé) ; scion :
    `Unable to parse package spec: git+file:///home/lepton-user/lepton-tools-dev/seed.scions@0.5.1.0`,
    signalé en avertissement, le script du noyau poursuit jusqu'à « Terminé. ».
  - `installer_scion` : même erreur pipx → sortie en code 1 (`set -e`). VSCodium, extensions,
    réglages et lepton non atteints.
  - État de la VM après l'échec : inchangé hors `apt-get update` (codium absent, aucune extension,
    scion 0.5.0.1, lepton absent).
- **Exécution n° 2** : non lancée.

## 3. Critères d'ENV-10

| Critère | Attendu | Résultat |
| --- | --- | --- |
| INS-1 | `codium --version` / `dpkg-query` = 1.135.06055 | Non vérifié (installation non atteinte). Forme dpkg du `.deb` : `1.135.06055` exactement (passage n° 1) |
| INS-2 | `diff` attendues / installées vide | Non vérifié |
| INS-3 | seul `apt-get install` du `.deb` dans le script ; chaîne par `install-debian.sh` | Conforme d'après le dry-run ; chaîne installée par `install-debian.sh` à l'exécution n° 1 (déjà présente, 0 paquet ajouté) |
| INS-4 | deux exécutions code 0, la seconde `changements 0` | **Non conforme** : exécution n° 1 en code 1 (§6.2) |
| INS-5 | aucun préfixe `/usr/local`, `/opt/homebrew`, `/opt/local` ; APT | Non vérifié par `grep` ; dry-run et exécution n° 1 n'emploient que `apt-get` |
| INS-6 | scion 0.5.1.0, lepton 0.1.0 | **Non conforme** : scion reste 0.5.0.1 (§6.2) ; lepton non atteint |
| NF-6 / shellcheck | sans remarque | Une remarque SC2015 (info) avec shellcheck 0.10.0 (§6.3) |
| Binaires au premier lancement | CodeLLDB `adapter/codelldb`, lemminx linux | Non vérifié |

## 4. Chaîne relevée par install-debian.sh (information)

`install-debian.sh` exécuté à l'exécution n° 1 ; aucun paquet ajouté (tout était à jour).

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

### 6.1 Arrêt silencieux sans extension installée (passage n° 1) — corrigé

Corrigé en 9321eed sur `devenv/env-10` (`{ grep -v '^$' || true; }`). Constaté sur la VM vierge :
le dry-run atteint réglages, lepton et bilan, code 0. Le chemin réel d'`installer_extensions` sur
hôte vierge reste à exercer (exécution n° 1 arrêtée avant).

### 6.2 Défaut commun à tous les hôtes — spécification pipx `git+file://` refusée (pour la session Mac)

- Lieu : `scripts/install-vscodium.sh:415`, branche `--seed-scions` :
  `SCION_SPEC="git+file://$(cd "$SEED_SCIONS_DIR" && pwd)@$SCION_REF"`, consommé par
  `installer_scion` (ligne 164) et transmis à `install-debian.sh` (et `install-macos.sh`).
- Cause : pipx n'accepte une URL nue que si elle a un hôte (`pipx/package_specifier.py:82`,
  `if parsed_url.scheme and parsed_url.netloc`) ; `git+file:///chemin` a un hôte vide → « Unable to
  parse package spec ».
- Vérification avec l'analyseur de pipx 1.7.1 (`_parse_specifier`) :

  | Spécification | Résultat |
  | --- | --- |
  | `git+file:///…/seed.scions@0.5.1.0` | refusée |
  | `scion @ git+file:///…/seed.scions@0.5.1.0` (PEP 508 nommée) | acceptée |
  | `git+https://github.com/lepton-distribution/seed.scions.git@0.5.1.0` | acceptée |

- Portée : tout hôte où scion n'est pas déjà à `SCION_REF`, avec `--seed-scions`. Non vu sur le Mac,
  où scion était déjà en 0.5.1.0 (« déjà installé », pipx non appelé, y compris dans l'essai
  `HOME` vide puisque scion est trouvé par le `PATH`). Le dry-run ne l'expose pas.
- Correction suggérée (non appliquée, non validée) :
  `SCION_SPEC="scion @ git+file://$(cd "$SEED_SCIONS_DIR" && pwd)@$SCION_REF"` ; vérifier que
  `install-debian.sh` / `install-macos.sh` transmettent la valeur entre guillemets (c'est le cas,
  `"${SCION_SPEC}"`). Pour la validation Mac : exercer réellement `pipx install` (scion à une autre
  version, ou `PIPX_HOME`/`PIPX_BIN_DIR` temporaires).
- Effet secondaire : `install-debian.sh` traite l'échec de scion en avertissement et poursuit ;
  seul `installer_scion` arrête le script.

### 6.3 shellcheck 0.10.0 : SC2015 sur `version_vscodium` (pour la session Mac)

`scripts/install-vscodium.sh:170`, branche macOS :
`[ -f "$APP/Contents/Info.plist" ] && /usr/libexec/PlistBuddy … || true` → SC2015 (info, « A && B
|| C is not if-then-else »). Sans effet sur le comportement (`|| true` voulu). Non signalé par
shellcheck 0.11.0 sur le Mac. Non propre à Debian : non corrigé. Une forme `if … fi` lèverait la
remarque pour les deux versions.

### 6.4 Suite

- Après correction sur `devenv/env-10` : passage n° 3 sur la VM selon la même consigne. État de la VM
  inchangé (hôte vierge : codium, extensions et lepton absents ; scion 0.5.0.1 ; shellcheck 0.10.0) ;
  clones en place dans `~/lepton-tools-dev/`.
- Accords déjà donnés par l'utilisateur : remplacement de scion 0.5.0.1 par 0.5.1.0 ; shellcheck
  installé.

## 7. Historique — passage n° 1 (2026-10-15, sur 0e287ea)

- Hôte et clones identiques au §1 ; shellcheck absent.
- Dry-run seulement (Claude) : sortie en **code 1 sans message** après la dernière extension, avant
  « Réglages utilisateur ». Exécutions n° 1 et n° 2 non lancées.
- Cause : `installer_extensions`, signalement des extensions hors liste
  (`printf '%s\n' "$installees" | sed 's/@.*//' | grep -v '^$' | while …`) ; `$installees` vide sur
  hôte vierge → `grep` rend 1 → `pipefail` + `set -e`. Défaut commun, corrigé depuis en 9321eed
  (§6.1).
- Contrôle complémentaire : `.deb` `codium_1.135.06055_amd64.deb` téléchargé, SHA-256 `5f5c00a9…f3d8649`
  identique à `VSCODIUM_SHA256_LINUX_AMD64` ; `dpkg-deb -f` → `Package: codium`,
  `Version: 1.135.06055`, `Architecture: amd64` (point ouvert du rapport Mac §4 levé).
- Chaîne présente sur la VM avant le passage : versions identiques au §4.
