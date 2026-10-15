# ENV-10 — Validation Debian de install-vscodium.sh — 2026-10-15

Session VM conduite selon `doc/devenv/consignes/env-10-debian.md`. **Validation interrompue avant
l'exécution n° 1** : le script s'arrête en code 1, sans message, sur un hôte sans extension
VSCodium (défaut commun à tous les hôtes, §6). Décision de l'utilisateur : arrêter et rapporter,
sans correction sur la VM (consigne §5.3).

## 1. Hôte

| Élément | Valeur |
| --- | --- |
| Système | Debian GNU/Linux 13 (trixie), `/etc/debian_version` 13.7, Linux x86_64 |
| Noyau | 6.12.107+deb13-amd64 |
| Utilisateur | `lepton-user` |
| sudo | demande un mot de passe (les exécutions réelles reviennent à l'utilisateur, consigne §5.1) |
| git / curl / python3 / pipx | git 2.47.3, curl présent, Python 3.13.5, pipx 1.7.1 |
| `~/.local/bin` dans le `PATH` | oui |
| codium | absent ; pas de dépôt APT VSCodium ; ni `~/.config/VSCodium` ni `~/.vscode-oss` |
| scion | 0.5.0.1 (pipx) — remplacement par 0.5.1.0 accepté par l'utilisateur, non effectué |
| lepton | absent |
| shellcheck | absent — installation acceptée par l'utilisateur, non faite (session arrêtée avant) |

Têtes des clones :

| Dépôt | Référence | Tête constatée |
| --- | --- | --- |
| `lepton-tools` | `devenv/env-10` | 0e287ea (conforme) ; rapport sur `devenv/env-10-debian` |
| `lepton-noyau` (`lepton-original-tree.scions`) | `devenv/env-10` | 1b2f7b6 (conforme) |
| `seed.scions` | tag `0.5.1.0` | 79f4f96 (conforme) |

## 2. Exécutions

Lancé par Claude : dry-run seulement (sans sudo). Journal : `~/env-10-journaux/0-dry-run.log` (VM).

- Dry-run : actions annoncées — `install-debian.sh --with-debug-tools`, `pipx install --force`
  de scion 0.5.1.0 (depuis le clone local), téléchargement et `sudo apt-get install` du `.deb`,
  installation des 9 extensions de `extensions.lst` (CodeLLDB par le `.vsix` linux-x64). Puis
  **sortie en code 1 sans message**, après la dernière extension, avant « Réglages utilisateur »,
  « lepton » et « Bilan ».
- Exécutions n° 1 et n° 2 : **non lancées** (même arrêt attendu après l'installation des
  extensions, voir §6).

Contrôle complémentaire hors script (lecture seule) : le `.deb` épinglé
`codium_1.135.06055_amd64.deb` a été téléchargé dans le répertoire temporaire de la session :
SHA-256 `5f5c00a9…f3d8649`, identique à `VSCODIUM_SHA256_LINUX_AMD64` ; `dpkg-deb -f` →
`Package: codium`, `Version: 1.135.06055`, `Architecture: amd64`.

## 3. Critères d'ENV-10

| Critère | Attendu | Résultat |
| --- | --- | --- |
| INS-1 | `codium --version` / `dpkg-query` = 1.135.06055 | Non vérifié (pas d'installation). Forme de la version dpkg du `.deb` : `1.135.06055` exactement → la comparaison stricte de `version_vscodium` convient (point ouvert du rapport Mac §4 levé) |
| INS-2 | `diff` attendues / installées vide | Non vérifié |
| INS-3 | seul `apt-get install` du `.deb` dans le script | Conforme d'après le dry-run et la lecture du script ; installation de la chaîne non exécutée |
| INS-4 | deux exécutions code 0, la seconde `changements 0` | **Non conforme attendu** : défaut §6, la n° 1 s'arrêterait en code 1 |
| INS-5 | aucun préfixe `/usr/local`, `/opt/homebrew`, `/opt/local` ; APT | Non vérifié par `grep` (session arrêtée) ; le dry-run n'emploie que `apt-get` |
| INS-6 | scion 0.5.1.0, lepton 0.1.0 | Non vérifié |
| NF-6 / shellcheck | sans remarque | Non vérifié (shellcheck absent) |
| Binaires au premier lancement | CodeLLDB `adapter/codelldb`, lemminx linux | Non vérifié |

## 4. Chaîne présente sur la VM (information)

Présente avant la session ; `install-debian.sh` n'a pas été exécuté.

| Outil | Version |
| --- | --- |
| arm-none-eabi-gcc | 14.2.1 20241119 (paquet 15:14.2.rel1-1) |
| cmake | 3.31.6 |
| ninja | 1.12.1 |
| qemu-system-arm | 10.0.13 (Debian 1:10.0.13+ds-0+deb13u1) |
| openocd | 0.12.0 |
| gdb | `gdb-multiarch`, GNU gdb (Debian 16.3-1) 16.3 |

## 5. Corrections propres à Debian

Aucune.

## 6. Points ouverts

### 6.1 Défaut commun à tous les hôtes — arrêt silencieux sans extension installée (pour la session Mac)

- Lieu : `installer_extensions`, signalement des extensions hors liste
  (`scripts/install-vscodium.sh:322`) :
  `printf '%s\n' "$installees" | sed 's/@.*//' | grep -v '^$' | while read -r id; do …`
- Cause : `$installees` vide (aucune extension, ou codium absent en dry-run) → `grep -v '^$'` ne
  sélectionne rien et rend 1 → avec `set -euo pipefail`, le pipeline échoue et le script sort en
  code 1 sans message.
- Reproduction minimale : `bash -c 'set -euo pipefail; i=""; printf "%s\n" "$i" | sed "s/@.*//" | grep -v "^\$" | while read -r x; do :; done; echo atteint'` → code 1, « atteint » non affiché.
- Portée : tout premier passage sur un hôte vierge (macOS comme Debian), en dry-run comme en
  exécution réelle, car `$installees` est lu avant l'installation des extensions. L'exécution
  n° 1 installerait VSCodium et les extensions, puis s'arrêterait sans appliquer les réglages ni
  installer lepton ; la n° 2 terminerait, avec des changements. Non vu sur le Mac, qui partait de
  7 extensions installées (rapport `env-10-validation.md` §2).
- Correction suggérée (non appliquée, non validée) : `{ grep -v '^$' || true; }` dans ce pipeline,
  et ajouter au protocole de validation un passage depuis un état sans extension.

### 6.2 Suite

- Après correction sur `devenv/env-10` : nouvelle session VM selon la même consigne. État de la VM
  inchangé (codium, extensions et lepton absents ; scion 0.5.0.1) ; clones `lepton-noyau` et
  `seed.scions` en place dans `~/lepton-tools-dev/`.
- Accords déjà donnés par l'utilisateur pour cette validation : remplacement de scion 0.5.0.1 par
  0.5.1.0 ; installation de shellcheck par l'utilisateur.
