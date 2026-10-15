# Consigne — session Claude Code sur la VM Debian — ENV-10 (validation Debian)

Fichier autonome : il suffit, avec `ORCHESTRATION.md` §2, à conduire la session VM. Il prime sur la
procédure générale de la skill `devenv-session` là où il la restreint (§7).
Rédigé le 2026-10-15 par la session Mac (ENV-10 S2), commit sur `devenv/env-10`.

## 1. Objet

Valider `scripts/install-vscodium.sh` sur Debian x86_64 (ENV-10 §3) : deux exécutions successives,
la seconde sans changement, et les critères d'ENV-10 (INS-1 à INS-6). Produire le rapport
`doc/devenv/rapports/env-10-debian.md` sur la branche `devenv/env-10-debian`. La session VM ne
développe pas : elle exécute, constate et rapporte (ORCHESTRATION §2).

Référence Mac Intel (même script) : `doc/devenv/rapports/env-10-validation.md` §2-§4.

### Passage n° 2 (après la correction 9321eed)

Le passage n° 1 (`rapports/env-10-debian.md`) s'est arrêté sur un défaut du script, corrigé sur
`devenv/env-10` (`env-10-validation.md` §5). Pour ce passage :
- mettre à jour les clones en place : `git -C ~/lepton-tools-dev/lepton-tools fetch origin`, puis
  `git switch devenv/env-10 && git pull --ff-only` ; conserver la branche locale
  `devenv/env-10-debian` du passage n° 1 ou la recréer depuis `origin/devenv/env-10` (elle y est
  fusionnée) ; clone noyau et seed.scions inchangés (1b2f7b6, 0.5.1.0) ;
- accords déjà donnés par l'utilisateur : remplacement de scion 0.5.0.1 par 0.5.1.0 (par le
  script) ; installation de `shellcheck` (`sudo apt-get install shellcheck`, par l'utilisateur) ;
- la VM part d'un état sans VSCodium ni extension : c'est l'essai « hôte vierge » attendu ;
- compléter `doc/devenv/rapports/env-10-debian.md` (ne pas créer d'autre fichier) : titre
  « passage n° 2 », §2 et §3 renseignés, §6.1 marqué corrigé ; garder le passage n° 1 en historique.

## 2. Ce que la session VM peut faire, et ne fait pas

| Autorisé | Interdit |
| --- | --- |
| Cloner les trois dépôts du §3 | Modifier `DEVENV-STATUS.md`, `ORCHESTRATION.md`, `SPECIFICATION.md`, une passation `handoff/*.md` |
| Créer `devenv/env-10-debian` dans lepton-tools | Commiter sur `devenv/env-10` ou `main` |
| Écrire `doc/devenv/rapports/env-10-debian.md` | Toucher au clone noyau ou à seed.scions (lecture seule) |
| Corriger `scripts/install-vscodium.sh` **seulement** pour un défaut propre à Debian, après accord de l'utilisateur, commit séparé | Retirer un VSCodium déjà installé, un paquet, un dépôt APT, sans accord |
| `git push origin devenv/env-10-debian` **après accord explicite** (PA-P) | Pousser toute autre branche ou tag ; modifier les fichiers de démarrage du shell (`~/.bashrc`, `~/.profile`) sans accord |

Tout écart au plan, toute erreur non prévue : s'arrêter, exposer, attendre l'utilisateur.

## 3. Dépôts à cloner (GitHub, `lepton-distribution`)

| Dépôt | Référence | Emplacement proposé sur la VM |
| --- | --- | --- |
| `lepton-tools` | branche `devenv/env-10` (tête attendue : le commit qui ajoute ce fichier, ou plus récent) | `~/lepton-tools-dev/lepton-tools` |
| `lepton-original-tree.scions` (clone noyau, porte `scripts/install-debian.sh`) | branche `devenv/env-10`, tête 1b2f7b6 | `~/lepton-tools-dev/lepton-noyau` |
| `seed.scions` | tag `0.5.1.0` (commit 79f4f96) | `~/lepton-tools-dev/seed.scions` |

```bash
mkdir -p ~/lepton-tools-dev && cd ~/lepton-tools-dev
git clone -b devenv/env-10 git@github.com:lepton-distribution/lepton-tools.git
git clone -b devenv/env-10 git@github.com:lepton-distribution/lepton-original-tree.scions.git lepton-noyau
git clone git@github.com:lepton-distribution/seed.scions.git && git -C seed.scions checkout -q 0.5.1.0
git -C lepton-noyau log --oneline -1      # 1b2f7b6
git -C seed.scions describe --tags        # 0.5.1.0
```

Si `lepton-tools` est déjà cloné (cas où Claude Code est lancé dedans), vérifier la branche et la
tête au lieu de recloner. Accès SSH à GitHub requis (clé de la VM) ; à défaut, HTTPS avec jeton :
le signaler à l'utilisateur, ne pas créer de clé ni de jeton soi-même.

## 4. Vérifications préalables (lecture seule)

Consigner chaque résultat dans le rapport (§1 Hôte) :

```bash
uname -sm; cat /etc/debian_version; . /etc/os-release && echo "$PRETTY_NAME"
id -un; sudo -n true && echo "sudo sans mot de passe" || echo "sudo demande un mot de passe"
command -v git curl python3 pipx codium scion lepton shellcheck || true
dpkg-query -W -f='${Version}\n' codium 2>/dev/null || echo "codium absent"
ls /etc/apt/sources.list.d/ | grep -i vscodium || echo "pas de dépôt APT VSCodium"
echo "$PATH" | tr ':' '\n' | grep -n "$HOME/.local/bin" || echo "~/.local/bin hors PATH"
ls ~/.config/VSCodium/User/settings.json 2>/dev/null; ls ~/.vscode-oss/extensions 2>/dev/null | head
```

Arrêts possibles :
- Hôte autre que `Linux x86_64` Debian : arrêt, le signaler.
- `codium` installé dans une autre version que `1.135.06055` : le script s'arrêtera ; demander à
  l'utilisateur s'il accepte `sudo apt-get remove codium` (réglages et extensions conservés).
- `~/.local/bin` hors `PATH` : pipx y installe scion et lepton ; le signaler, proposer
  `pipx ensurepath` (modifie le shell : accord requis).

## 5. Exécutions

### 5.1 Qui lance le script
Le script appelle `sudo apt-get` (par `install-debian.sh` et pour le `.deb` de VSCodium). Claude
Code ne peut pas saisir un mot de passe sudo :
- `sudo -n true` réussit → Claude peut lancer les commandes du §5.2 lui-même ;
- sinon → **l'utilisateur** lance les commandes du §5.2 dans un terminal de la VM, puis Claude lit
  les journaux.

### 5.2 Commandes
```bash
cd ~/lepton-tools-dev/lepton-tools
mkdir -p ~/env-10-journaux
shellcheck scripts/install-vscodium.sh ../lepton-noyau/scripts/install-debian.sh   # si shellcheck présent
bash scripts/install-vscodium.sh --dry-run \
  --lepton-clone ~/lepton-tools-dev/lepton-noyau --seed-scions ~/lepton-tools-dev/seed.scions \
  2>&1 | tee ~/env-10-journaux/0-dry-run.log
# Exécution n° 1
bash scripts/install-vscodium.sh \
  --lepton-clone ~/lepton-tools-dev/lepton-noyau --seed-scions ~/lepton-tools-dev/seed.scions \
  2>&1 | tee ~/env-10-journaux/1-execution.log; echo "code=${PIPESTATUS[0]}" | tee -a ~/env-10-journaux/1-execution.log
# Exécution n° 2 (rien ne doit changer)
bash scripts/install-vscodium.sh \
  --lepton-clone ~/lepton-tools-dev/lepton-noyau --seed-scions ~/lepton-tools-dev/seed.scions \
  2>&1 | tee ~/env-10-journaux/2-execution.log; echo "code=${PIPESTATUS[0]}" | tee -a ~/env-10-journaux/2-execution.log
```
Si `~/.local/bin` n'est pas dans le `PATH`, l'ajouter pour la durée de la commande seulement :
`PATH="$HOME/.local/bin:$PATH" bash scripts/install-vscodium.sh …`.

Attendu : n° 1 code 0, plusieurs changements ; n° 2 code 0, ligne `changements 0`.
`install-debian.sh` est rejoué à chaque exécution (`apt-get update`) ; il n'est pas compté comme un
changement (comportement voulu, rapport Mac §4).

### 5.3 En cas d'échec
S'arrêter. Relever le message, la fonction du script concernée, la cause. Proposer une correction à
l'utilisateur ; ne l'appliquer qu'avec son accord, uniquement si elle est propre à Debian, en
commit séparé `devenv(env-10-debian): …` ; rejouer ensuite les deux exécutions. Un défaut commun à
tous les hôtes : ne pas corriger, le consigner pour la session Mac.

## 6. Critères à vérifier après l'exécution n° 2

```bash
cd ~/lepton-tools-dev/lepton-tools
codium --version
dpkg-query -W -f='${Version}\n' codium                                   # 1.135.06055
codium --list-extensions --show-versions | tr '[:upper:]' '[:lower:]' | sort > /tmp/installees.txt
sed -e 's/#.*//' -e 's/[[:space:]]//g' scripts/extensions.lst | grep -v '^$' | tr '[:upper:]' '[:lower:]' | sort > /tmp/attendues.txt
diff /tmp/attendues.txt /tmp/installees.txt && echo "extensions conformes"
ls -d ~/.vscode-oss/extensions/vadimcn.vscode-lldb-1.12.3*/adapter/codelldb   # CodeLLDB complet
ls ~/.vscode-oss/extensions/redhat.vscode-xml-0.29.3*/server/ | grep -i lemminx-linux   # lemminx natif
grep -E 'update.mode|autoUpdate|autoCheckUpdates|redhat.telemetry|preferBinary' ~/.config/VSCodium/User/settings.json
scion version; lepton --version
grep -n '/usr/local\|/opt/homebrew\|/opt/local' scripts/install-vscodium.sh || echo "INS-5 : aucun préfixe"
arm-none-eabi-gcc --version | head -1; cmake --version | head -1; ninja --version; qemu-system-arm --version | head -1; openocd --version 2>&1 | head -1; gdb-multiarch --version 2>/dev/null | head -1
```
Les outils de la chaîne (dernière ligne) sont relevés pour information : ils viennent
d'`install-debian.sh`, pas du script testé. Si une commande diffère sur Debian (nom de gdb, par
exemple), noter le nom réel.

| Critère | Attendu |
| --- | --- |
| INS-1 | `codium --version` = 1.135.06055 ; `dpkg-query` = `1.135.06055` (vérifier la forme exacte, point ouvert du rapport Mac §4) |
| INS-2 | `diff` attendues / installées vide |
| INS-3 | seul `apt-get install` du `.deb` de VSCodium dans le script ; chaîne installée par `install-debian.sh` |
| INS-4 | deux exécutions code 0, la seconde `changements 0` ; aucune commande `sudo` effective à la seconde, hors `install-debian.sh` |
| INS-5 | `grep` des préfixes vide ; APT sur Debian |
| INS-6 | `scion version` → 0.5.1.0 ; `lepton --version` → `lepton 0.1.0` |
| NF-6 / shellcheck | sans remarque |
| Binaires au premier lancement | CodeLLDB complet (`adapter/codelldb`), lemminx linux présent |

Facultatif, si l'utilisateur a un affichage graphique sur la VM : ouvrir VSCodium une fois et
constater qu'aucune extension ne demande de téléchargement ni de mise à jour.

## 7. Fin de session VM (remplace la fin de session de `devenv-session`)

1. `git -C ~/lepton-tools-dev/lepton-tools switch -c devenv/env-10-debian` (si pas déjà fait).
2. Écrire `doc/devenv/rapports/env-10-debian.md` selon le plan du §8.
3. Commit : `git add doc/devenv/rapports/env-10-debian.md && git commit -m "devenv(env-10-debian): rapport de validation Debian"`
   (corrections éventuelles : commits séparés, déjà faits au §5.3).
4. Demander à l'utilisateur l'accord PA-P, puis `git push -u origin devenv/env-10-debian`.
5. Ne pas écrire de passation ni toucher à `DEVENV-STATUS.md` : la session Mac intègre le rapport
   et clôt ENV-10. Résumer à l'utilisateur : critères conformes ou non, commit poussé.

## 8. Plan du rapport `doc/devenv/rapports/env-10-debian.md`

```markdown
# ENV-10 — Validation Debian de install-vscodium.sh — <date>

## 1. Hôte
Debian <version>, noyau, utilisateur, sudo (avec / sans mot de passe), état de départ
(codium, extensions, scion, lepton, pipx, PATH), têtes des trois clones.

## 2. Exécutions
Qui a lancé (Claude / utilisateur), dry-run (actions annoncées), n° 1 (code, nombre et liste des
changements, durée approximative), n° 2 (code, changements). Extraits utiles des journaux seulement.

## 3. Critères d'ENV-10
Tableau du §6 de la consigne, colonne Résultat.

## 4. Chaîne installée par install-debian.sh (information)
Versions relevées.

## 5. Corrections propres à Debian
Aucune, ou : commit, défaut, correction, accord de l'utilisateur.

## 6. Points ouverts
Écarts, défauts communs à tous les hôtes (pour la session Mac), questions pour l'utilisateur.
```
