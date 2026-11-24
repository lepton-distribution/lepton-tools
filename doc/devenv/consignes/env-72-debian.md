# Consigne — session Claude Code sur la VM Debian — ENV-72 (validation Debian groupée)

Fichier autonome : avec `ORCHESTRATION.md` §2bis, il suffit à conduire la session VM. Rédigé le
2026-11-24 par la session Mac `validation-debian-env-72` (tâche 1 d'ENV-72), repris de
`consignes/env-66-debian.md`. **Soumis à l'utilisateur au PA-131** (consigne, §0, C3, C6, C8,
C9). Son texte est envoyé tel quel dans l'ordre `R72-1`.

## 0. Préalable, avant l'ordre (utilisateur) — PA-131

Les réglages utilisateur et les variables d'environnement ne sont lus qu'au démarrage d'une
session (D26, PA-111 ; D38 (1), PA-121). Avant l'envoi de `R72-1`, l'utilisateur, sur la VM,
**session Claude Code fermée** :
1. dans un terminal :
   ```bash
   cd ~/lepton-tools-dev/lepton-tools && git status --short && git fetch origin && git switch devenv/env-72 && git merge --ff-only origin/devenv/env-72 && git log --oneline -1
   ```
2. pose `LEPTON_EMBOS_ROOT` dans le profil de la VM : ajoute à la fin de `~/.bashrc` la ligne
   ```bash
   export LEPTON_EMBOS_ROOT="$HOME/lepton/third_party/embos/cortexm-gcc/5.20.0.0"
   ```
   puis ouvre un **nouveau** terminal et vérifie :
   ```bash
   printenv LEPTON_EMBOS_ROOT; ls "$LEPTON_EMBOS_ROOT/Start/Inc/RTOS.h"; printenv SCION_REF SCION_SPEC LEPTON_CLONE XDG_CONFIG_HOME NM SIZE; echo "fin"
   ```
   Attendu : `/home/lepton-user/lepton/third_party/embos/cortexm-gcc/5.20.0.0`, le fichier
   `RTOS.h` listé, aucune autre ligne avant `fin` (les six autres variables absentes) ;
3. ne modifie pas `~/.claude/settings.json` (2 règles `allow` depuis le §0 d'ENV-66) ;
4. ouvre, **depuis ce nouveau terminal**, une **nouvelle** session Claude Code **dans
   `~/lepton-tools-dev/lepton-tools`**, en mode auto, avec Remote Control ; approuve le dossier si
   Claude Code le demande ;
5. communique à la session Mac le nom de la nouvelle session (`ListAgents`), à qui l'ordre est
   envoyé.

## 1. Objet

Valider sur Debian x86_64 l'état publié après ENV-67 à ENV-71 :
- **D38 (1)** (ENV-67, PA-121) : variables d'environnement relevées au §5, chacune contre sa
  valeur attendue, arrêt si elle manque ou diffère ;
- **D38 (2)** (ENV-67) : `scripts/supprimer-essai.sh` admet les descendants de `~/tmp-pytest`
  (§8, C9) ;
- **D38 (3)** (ENV-67) : attendus rejoués au Mac sur une copie d'origine distincte ; classes
  d'écart que le Mac ne peut simuler listées (§10) ;
- **D29, D30, D32, D37** (ENV-68) : lepton, chemins saisis (`~` dans `check FILE`,
  `seed mkconf import`, `seed new --mkconf` ; `--clangd` relatif) et cohérence de la graine
  (retrait refusé, greffon déclaré sans clone) ;
- **D36** (ENV-69) : extension **0.5.4**, liste des greffons observés rafraîchie quand
  `trunk/.scion.grafted.list` change ;
- **D35, D33** (ENV-70) : scion **0.6.3.4** ; le message d'échec de git garde la cause
  (`fatal:`/`error:`, en anglais ou en français) et non l'avertissement que git **2.47.3** écrit
  avant elle ; `seed-update` et `graft-update` refusent une graine clonée hors de sa version.
  D35 ne se voit qu'avec le git de la VM : **sa preuve réelle est ici** ;
- **D40** (ENV-71) : miroirs synchronisés, `mirror-sync --dry-run` à 0 ;
- **D39** (révision du 2026-11-23) : aucune invite simultanée Mac et VM (§3) ;
- regreffe de `$U`, `$E13`, `$C5` et `$R53` : seul le clone noyau avance (2b4a647 → **0c2e43e** :
  `SCION_REF` 0.6.3.4, 5 fichiers hors de `scion/`). Aucun lien ne change ;
- constructions host et 16 presets dans `$R53` regreffé : **aucun binaire changé** depuis R66-1.

**Pas de cartes** dans cette session (C8, à confirmer au PA-131). Aucune écriture flash.

Références publiées (toutes poussées) :

| Dépôt (`https://github.com/lepton-distribution/…`) | Référence | Commit | En R66-1 |
| --- | --- | --- | --- |
| `lepton-tools` | `devenv/env-72` (cette consigne) | tête après `fetch` | `devenv/env-66` |
| `seed.scions` | tag `0.6.3.4` | **473b653** (`master` 929c01a) | tag `0.6.3.3` 9615cd5 |
| `lepton-original-tree.scions` (noyau) | `master` | **0c2e43e** | 2b4a647 |
| 8 miroirs `mirror-*` | HEAD | avancés en ENV-71 (D40) ; tags épinglés inchangés | — |
| graine `lepton-seed.scions`, 12 autres greffons | | inchangés | = |

Relevé du Mac : `rapports/env-72-mac/ls-remote-mac.txt` (script `env-72-mac/ls-remote.sh`).

Références Mac (`rapports/env-72-mac.md` §1, `rapports/env-72-mac/attendu/`) :
- liste `chemin -> cible` : `rapports/env-50-mac/attendu/trunk-liens.txt` (3889, inchangée depuis
  R50-1, revérifiée sur `<ROOTSTOCK>` le 2026-11-24) ; clones tiers :
  `rapports/env-53-mac/attendu/clones-rootstock-mac.txt` ;
- C3 : `attendu/c3/` (regreffe d'`essais/env-13-vierge` par scion 0.6.3.4, même état que `$U` et
  `$E13`) ;
- C4 : `attendu/c4-chemins/` (D29, D30 : `env-72-mac/chemins.sh`), `attendu/c4-graine/` (D32,
  D37 : `env-72-mac/graine.sh`), sur une copie d'`essais/env-11/qemu` du Mac ;
- C5 : `attendu/fixture70/` (D33, D35 : `env-72-mac/fixture70.py`), `attendu/fixture65/`,
  `fixture60/`, `fixture56/` (clone de seed.scions au tag 0.6.3.4, base `essais/env-72-fixture`).

Référence Debian : `rapports/env-66-debian.md` et `oracles/env-66-debian/`.

La session VM ne développe pas : elle exécute, constate et rapporte.

## 2. Ce que la session VM peut faire, et ne fait pas

| Autorisé | Interdit |
| --- | --- |
| `git fetch` / `switch` / `merge --ff-only` de `$T` (`devenv/env-72`) et du clone noyau `$K` (`master`) | Modifier `DEVENV-STATUS.md`, `ORCHESTRATION.md`, `SPECIFICATION.md`, `handoff/*.md`, les consignes, `rapports/env-72-mac*`, `.claude/`, `~/.claude/settings.json`, `~/.bashrc` |
| Installations du §6 (`sudo` sans mot de passe sur la VM), dans les formes écrites | Toute autre commande `sudo`, `pip install` hors de `venv-test`, `codium --install-extension` hors `install-vscodium.sh` ; installer Node.js ou rsync |
| `scion graft-update` de `$U`, `$E13`, `$C5`, `$R53` (§9), dans la forme écrite : l'invite est **confirmée** par l'utilisateur | `graft-update` d'un autre rootstock ; tout `seed-update` ; toute écriture dans les clones de `$U`, `$E13`, `$C5`, `$R53` |
| Lectures dans `$U`, `$E13`, `$C5`, `$R53` ; `lepton check` / `generate` / `seed status` dans ces quatre rootstocks ; `rejouer-oracle.sh` dans `$R53` (`build/` compris, §12) | Écrire un fichier régulier dans un `trunk/` ou sous `depots/tiers/` (le hook refuse) ; corriger quoi que ce soit |
| Créer `$W` (§7), `$SS` et `$FX` (§11.2), `~/tmp-pytest/env-72-enveloppe` (§8) et y tout faire, `seed add` / `seed remove` compris | `git config` (même en lecture) et `git sparse-checkout` dans un clone de `depots/tiers/` : relever par `releve-clones.sh` |
| `scion mirror-sync --dry-run` dans `$R53` (§12) | `mirror-sync` sans `--dry-run` ; tout envoi vers un miroir |
| Les contrôles du §8, sur cibles absentes ou protégées | Toute écriture flash, toute commande OpenOCD ; modifier la configuration réseau de la VM |
| Suppressions par `scripts/supprimer-essai.sh` (§8, §11.4, §14) | `rm -rf` direct |
| Créer `devenv/env-72-debian` (depuis `devenv/env-72`) ; y écrire `doc/devenv/rapports/env-72-debian.md`, `doc/devenv/rapports/env-72-debian/` et `doc/devenv/rapports/oracles/env-72-debian/` | Commiter sur une autre branche |
| `git push origin devenv/env-72-debian` **après accord explicite de l'utilisateur** (PA-P ; invite `ask`) | Pousser toute autre branche |

Formes des commandes : **ORCHESTRATION §2bis**, « Commandes soumises aux règles de
`.claude/settings.json` », « Formes », « Invites à refuser » et « Variables d'environnement ».
Chaque commande de cette consigne y est écrite dans la forme couverte par sa règle ; la lancer
**telle qu'écrite, une par appel**. Rappel :
- une commande `allow` lancée seule garde sa règle (`2>&1` admis). Les commandes `allow` de cette
  consigne n'ont ni redirection vers un fichier, ni `| tee`, ni `; echo "code=$?"` ; pytest écrit
  son journal par `--junitxml` ;
- une commande `ask` (`scion graft-update`, `git push`) est lancée **directement**, jamais par un
  script, un `bash -c` ou un `eval` ;
- **invites** (D28) : l'`AVANCEMENT` qui précède immédiatement chaque commande à invite dit
  « À REFUSER » (§8, A1 : cible absente) ou « À CONFIRMER » (§9, push), avec la commande exacte.
  Une invite se confirme par « Oui », pour cette commande seule. Une invite non annoncée : la
  refuser, `AVANCEMENT` ;
- **aucune affectation de variable en tête d'une commande** (`LEPTON_EMBOS_ROOT=… cmd`) : une
  variable absente ou fausse est un arrêt (§5), l'utilisateur la pose dans le profil puis relance
  la session.

Autres règles :
- **Refus.** Toute commande refusée (classifieur, invite, hook) n'est jamais contournée :
  `AVANCEMENT` avec la commande exacte et la décision ; l'utilisateur la lance s'il le décide, la
  session vérifie l'effet et le consigne. Seuls les refus attendus du §8 (A1, H1, R1, R2) ne
  demandent rien à l'utilisateur, sinon de refuser l'invite A1.
- **Refus d'une invite.** Il interrompt le tour de la session. L'utilisateur relance par un
  message dans la session VM (`reprendre R72-1 au §8, H1`).
- **Régénérer avant de relever** : tout relevé « avant » d'un fichier généré suit immédiatement la
  commande qui le produit (`regreffer-essai.sh avant` le fait).
- **Branche des clones d'un rootstock existant** : relevée au §5 pour `$U`, `$E13`, `$C5`, `$R53`,
  **graine clonée comprise** (`depots/lepton-seed.scions/original-tree`, D33). scion 0.6.3.4
  refuse lui-même un clone ou une graine hors de sa version ; un tel refus reste un écart à exposer.
- **scion, lepton et extension avant C4 à C6** : aucun essai des §10 et §11 avant que
  `scion version` donne 0.6.3.4 et que lepton soit réinstallé (§6) ; aucun essai D36 avant
  l'extension 0.5.4.
- **Comparaisons** (D27) : toujours par `scripts/comparer-releves.py` avec `--home-attendu
  /Users/cle_d_anton --home-obtenu "$HOME"` ; jamais un filtre écrit à la main.

Tout écart au plan, toute erreur non prévue : s'arrêter, exposer (`AVANCEMENT` ou `QUESTION`),
attendre.

## 3. Communication (ORCHESTRATION §2bis)

- Session principale : `validation-debian-env-72` (session Mac ; Claude Code peut la renommer).
  Répondre à l'adresse `from` du message d'ordre.
- ID : `R72-1`, repris tel quel : `[ACCUSÉ R72-1] ENV-72 — …`, `[AVANCEMENT R72-1] …`,
  `[QUESTION R72-1] …`, `[FIN-SUCCÈS R72-1] …` ou `[FIN-ÉCHEC R72-1] …`.
- `ACCUSÉ`, avant toute commande autre que les lectures du §5. Il contient :
  - l'ordre reformulé en une phrase ;
  - le nom de la session VM, son répertoire de travail, la version de Claude Code du journal de
    session (champ `version`) ;
  - la tête réelle de `devenv/env-72` ; les empreintes de `.claude/settings.json`, du hook, de
    l'enveloppe et de `comparer-releves.py` ;
  - les variables d'environnement du §5, valeur par valeur ;
  - les résultats de `git ls-remote` du §5 ;
  - les branches et têtes des clones et des graines de `$U`, `$E13`, `$C5` et `$R53` ;
  - les étapes prévues (§6 à §15) et les écarts déjà visibles.
- `AVANCEMENT` : avant chaque commande à invite (§8 A1, §9, push), avant toute action demandée à
  l'utilisateur, à chaque refus non prévu, après chacun des §6 à §12, et à chaque arrêt.
- **Invites simultanées** (D39, §2bis) : les critères qui présentent une invite sont **C2** (§8,
  A1), **C3** (§9, 4 `graft-update`) et le push final (§15). Après la dernière regreffe du §9, la
  session envoie `[AVANCEMENT R72-1] fin des invites de la VM jusqu'au push` ; avant le push du
  §15, un `AVANCEMENT` « À CONFIRMER » l'annonce. La session Mac ne lance aucune commande à
  invite entre l'`ACCUSÉ` et cet `AVANCEMENT`, ni pendant le push.
- `FIN-SUCCÈS` / `FIN-ÉCHEC` : résultat par critère du §15, commits et branche (poussée ou non),
  chemin du rapport, versions relevées, écarts, ce qui n'a pas été fait.
- **Remise en échec** (§2bis) : un envoi en erreur (ECONNRESET, « bridge ID is stale ») est renvoyé
  une fois, à l'identique. Si le second envoi échoue, le message entier est consigné dans
  `~/env-72-journaux/0-messages-R72-1.md` et au §Messages du rapport, avec la mention « non remis ».
  La session l'annonce à l'utilisateur, qui le relaie à la session Mac. Un message relayé par
  l'utilisateur et portant l'ID `R72-1` vaut message reçu.

## 4. Journaux et variables

```bash
mkdir -p ~/env-72-journaux
J=~/env-72-journaux
T=~/lepton-tools-dev/lepton-tools
K=~/lepton-tools-dev/lepton-noyau
E=~/lepton-tools-dev/essais
U=$E/env-28-debian
E13=$E/env-13-debian
C5=$E/env-53-c5
R53=$E/env-53-debian
W=$E/env-72-essai
D72=$W/depot72
SS=$W/seed-scions
FX=$E/env-72-fixture
X=doc/devenv/rapports/env-72-mac
A=$X/attendu
X57=doc/devenv/rapports/env-57-mac
Y=doc/devenv/rapports/env-53-mac
A50=doc/devenv/rapports/env-50-mac/attendu
C=doc/devenv/rapports/env-43-mac/controler-trunk.py
LI=$Y/liens.py
IC=$Y/inventaire-clones.sh
RG=$X57/regreffer-essai.sh
DEC=$X57/decisions.py
cmp_mac() { python3 -I "$T/scripts/comparer-releves.py" --home-attendu /Users/cle_d_anton --home-obtenu "$HOME" "$@"; }
```
`~/lepton-tools-dev/essais/env-72-absent` et `https://github.com/lepton-distribution/env-72-absent.git`
n'existent pas et ne doivent jamais être créés : ce sont les cibles absentes du §8. Les commandes
non couvertes par une règle portent leur journal (`> "$J/<étape>.log" 2>&1; echo "code=$?" >> …`).
Les boucles s'écrivent en bash. Ne pas faire `cd` dans un `trunk/` : revenir à `$T` (le hook juge
le répertoire courant).

`cmp_mac <attendu> <obtenu> [<fichier>…]` compare après normalisation (`scripts/comparer-releves.py`,
D27) : messages de git en français ramenés à l'anglais (table `TRADUCTIONS`, tirée de `po/fr.po`
v2.47.3, U+00A0 compris) ; ancêtres de `<HOME>` sous `depots/.mirrors/<hôte>/`. Sortie : une
ligne par fichier, puis `écarts=<n> / <total>` ; code 0 sans écart, 1 sinon.

Outils de la session Mac, en lecture seule, utilisables tels quels sur Debian :
- `env-53-mac/` : `releve-clones.sh`, `inventaire-clones.sh`, `liens.py` ;
- `env-57-mac/regreffer-essai.sh avant|apres <rootstock> <journaux>` : relevés avant et après une
  regreffe, bilan `<journaux>/<nom>-bilan.txt` ; le `graft-update` est lancé à part par la
  session, entre les deux phases ;
- `env-57-mac/decisions.py <journal .jsonl> [--motif <texte>]…` : décisions de permission des
  appels Bash de la session (TSV) ;
- `env-72-mac/chemins.sh` (D29, D30 ; 4ᵉ argument : nom de clangd), `env-72-mac/graine.sh` (D32,
  D37) : scripts d'ENV-68 dont les copies se font par `tar` (rsync absent de la VM), seule
  différence ;
- `env-72-mac/fixture70.py` (D33, D35) : fixture d'ENV-70 dont le git des appels `--single-branch`
  est le 5ᵉ argument (`/usr/bin/git` sur la VM) ; `env-65-scion/fixture.py`,
  `env-60-scion/fixture.py`, `env-56-scion/fixture.py`.

## 5. Vérifications préalables (lecture seule) — C1

```bash
pwd; printenv CLAUDE_PROJECT_DIR; claude --version 2>&1 | head -1
F=$(ls -t ~/.claude/projects/*lepton-tools-dev-lepton-tools/*.jsonl | head -1); echo "$F"; grep -o '"version":"[^"]*"' "$F" | sort | uniq -c
for v in LEPTON_EMBOS_ROOT SCION_REF SCION_SPEC LEPTON_CLONE XDG_CONFIG_HOME NM SIZE LANG LC_ALL; do if printenv "$v" > /dev/null; then echo "$v=$(printenv "$v")"; else echo "$v absente"; fi; done
ls -l "$LEPTON_EMBOS_ROOT/Start/Inc/RTOS.h" 2>&1; locale 2>&1 | head -3
git -C "$T" status --short | head -5; git -C "$T" branch --show-current; git -C "$T" log --oneline -1
git -C "$T" fetch origin && git -C "$T" status -sb | head -1
sha256sum "$T/.claude/settings.json" "$T/.claude/hooks/proteger-trunk.py" "$T/scripts/supprimer-essai.sh" "$T/scripts/comparer-releves.py"
ls -la ~/.claude/settings.json ~/.claude/settings.local.json "$T/.claude/settings.local.json" 2>&1
uname -sm; cat /etc/debian_version; uname -r; id -un; git --version
scion version | tail -1; lepton --version
arm-none-eabi-gcc --version | head -1; cmake --version | head -1; ninja --version; qemu-system-arm --version | head -1; python3 --version; codium --version | head -1
command -v shasum realpath tar clangd node rsync zsh; ls -l /usr/share/codium/codium; ls -d ~/tmp-pytest ~/tmp-pytest/* ~/lepton-tools-dev/venv-test/bin/pytest 2>&1
id inconnu68 2>&1 | head -1
df -h ~ /tmp | tail -2
for Z in "$W" "$FX" "$E/env-72-absent" ~/tmp-pytest/env-72 ~/tmp-pytest/env-72-enveloppe; do test -e "$Z" && echo "ARRÊT : $Z existe déjà"; done
cd "$T" && bash $X/ls-remote.sh > "$J/5-ls-remote.txt" 2>&1; diff <(grep -v '^lepton-tools ' $X/ls-remote-mac.txt) <(grep -v '^lepton-tools ' "$J/5-ls-remote.txt") && echo "têtes publiées = Mac"
for Z in "$U" "$E13" "$C5" "$R53"; do
  echo "== $Z"
  grep -v '^#' "$Z"/trunk/.scion.grafted.list | grep -c .
  bash "$T/$IC" "$Z" | tee "$J/5-clones-$(basename $Z).txt"
  python3 -I "$T/$LI" "$Z/trunk" > /dev/null
  ls -d "$Z"/depots/tiers/*/* 2>&1; du -sk "$Z"/depots/tiers 2>&1
done
ls -d ~/env-66-journaux ~/tmp-pytest/env-66 2>&1; ls -d "$E"/*/ 2>&1
```
Attendu :
- répertoire de travail `$T` (`/home/lepton-user/lepton-tools-dev/lepton-tools`) ; lepton-tools
  propre, sur `devenv/env-72`, à jour avec `origin/devenv/env-72` (préalable du §0) ;
- **variables** (D38 (1), PA-121) : `LEPTON_EMBOS_ROOT=/home/lepton-user/lepton/third_party/embos/cortexm-gcc/5.20.0.0`
  et `Start/Inc/RTOS.h` présent sous elle ; `SCION_REF`, `SCION_SPEC`, `LEPTON_CLONE`,
  `XDG_CONFIG_HOME`, `NM`, `SIZE` **absentes** ; `LANG`, `LC_ALL` et `locale` relevées (sans
  arrêt) ;
- `.claude/settings.json` `b01ad557…d235`, `proteger-trunk.py` `04572df6…6909` (inchangés depuis
  R61-1), `supprimer-essai.sh` `369dae36…b9c8` (ENV-67, D38 (2)), `comparer-releves.py`
  `2bd102cd…5d8c` (inchangé depuis ENV-66) ;
- `~/.claude/settings.json` présent (2 règles, §8.1) ;
- `têtes publiées = Mac` ; git **2.47.3** ; scion **0.6.3.3** (avant installation) ;
  `lepton 0.1.0`, `scion 0.6.3.3 (requis ≥ 0.6.2.0)` ;
- chaîne APT de R66-1 : arm-none-eabi-gcc 14.2.1, cmake 3.31.6, ninja 1.12.1, QEMU 10.0.13,
  Python 3.13.5, codium 1.135.06055 ; `shasum`, `realpath`, `tar`, `clangd` présents ; `node`,
  `rsync`, `zsh` absents (relevés) ; `/usr/share/codium/codium` présent ; `~/tmp-pytest`,
  `~/tmp-pytest/env-66` et `venv-test/bin/pytest` présents ; `id inconnu68` : utilisateur inconnu
  (sinon l'essai D29 s'arrête) ;
- `$U`, `$E13` et `$R53` (état laissé par R66-1), chacun : **23 entrées** ; 14 lignes
  d'inventaire, dont la graine `depots/lepton-seed.scions/original-tree` **sur
  `original-tree`** (15740f9, amont `origin/original-tree`, `modifs=0`) et 13 clones
  `<clé>/master` sur `master`, amont réglé, `modifs=0`, noyau **2b4a647** ;
  `liens=3889 casses=0 reguliers=0` ; 8 clones tiers ;
- `$C5` : graine locale `depots/lepton-seed/env11` (branche relevée) ; `liens=3059 casses=0
  reguliers=0` ; noyau 2b4a647 ; `salut` sans amont, `modifs=2` (état d'origine de la VM) ; clones
  F7 conservés de R53-1 ;
- `~/env-66-journaux` et `~/tmp-pytest/env-66` présents.

Arrêts :
- un chemin du `for` initial existe ;
- **une variable absente ou différente de l'attendu** (`LEPTON_EMBOS_ROOT` absente, autre chemin,
  `RTOS.h` absent ; une des six autres présente) : `AVANCEMENT` avec la valeur lue ; l'utilisateur
  corrige le profil et relance la session (§0) ; jamais d'affectation en tête d'une commande ;
- lepton-tools non propre, hors de `devenv/env-72`, ou `settings.json`, hook ou enveloppe
  différent du Mac ;
- un commit publié diffère du Mac (hors HEAD d'un miroir, voir §12.3) ;
- graine de `$U`, `$E13`, `$C5` ou `$R53` modifiée **ou hors de sa branche** ; un clone de greffon
  publié hors de sa branche, sans amont ou modifié ;
- `shasum`, `realpath`, `tar` ou `clangd` absent ; moins de 8 Go libres dans `~`.

Pas des arrêts, à consigner : une version de la chaîne ou de Claude Code différente de R66-1.

## 6. Installation de scion 0.6.3.4, de lepton et de l'extension 0.5.4 (C1)

D'abord, par la session :
```bash
git -C "$K" status --short | head -5
git -C "$K" fetch origin && git -C "$K" switch master && git -C "$K" merge --ff-only origin/master && git -C "$K" log --oneline -1
grep -n '^SCION_REF=' "$K/scripts/install-debian.sh" "$T/scripts/install-vscodium.sh"
grep -n 'SCION_MIN_VERSION =' "$T/lepton/__init__.py"; grep -n '"version"' "$T/extension/package.json"; ls "$T"/extension/dist/; sha256sum "$T"/extension/dist/*.vsix
```
Attendu : clone noyau propre, à **0c2e43e** (2b4a647 avant) ; `SCION_REF="${SCION_REF:-0.6.3.4}"`
(noyau) et `SCION_REF="0.6.3.4"` (lepton-tools) ; `SCION_MIN_VERSION = (0, 6, 2, 0)` ;
extension `0.5.4`, `lepton-0.5.4.vsix` seul dans `dist/` (`31678dd3…b8d1`).

Puis `AVANCEMENT`, et la session lance, une commande par appel, dans cet ordre :
1. scion (hors règle : classifieur ; accepté en R66-1) :
   ```bash
   bash ~/lepton-tools-dev/lepton-noyau/scripts/install-debian.sh --with-debug-tools > ~/env-72-journaux/6-install-debian.log 2>&1; echo "code=$?" >> ~/env-72-journaux/6-install-debian.log
   ```
   Il installe scion par `pipx install --force
   "git+https://github.com/lepton-distribution/seed.scions.git@0.6.3.4"` (défaut `SCION_REF`). En
   cas de refus : `AVANCEMENT` ; l'utilisateur lance la même ligne dans la session VM (`!` en
   **premier** caractère) ou dans un terminal.
2. lepton (règle `allow` du dépôt, forme exacte, sans redirection) :
   ```bash
   pipx install --force ~/lepton-tools-dev/lepton-tools
   ```
   Sortie lue dans le résultat de l'outil et reportée au rapport. Elle installe le lepton
   d'ENV-68 (D29, D30, D32, D37).
3. VSCodium et extension (hors règle) :
   ```bash
   bash ~/lepton-tools-dev/lepton-tools/scripts/install-vscodium.sh --lepton-clone ~/lepton-tools-dev/lepton-noyau > ~/env-72-journaux/6-install-vscodium.log 2>&1; echo "code=$?" >> ~/env-72-journaux/6-install-vscodium.log
   ```

Puis :
```bash
tail -3 "$J/6-install-debian.log"; grep -n -i 'scion' "$J/6-install-debian.log" | tail -5; tail -12 "$J/6-install-vscodium.log"
scion version | tail -1; lepton --version; codium --version | head -1
pipx list --short | grep -E '^(scion|lepton) '
PYL=$(dirname "$(realpath "$(command -v lepton)")")/python; echo "$PYL"
PL=$("$PYL" -I -c 'import lepton, os; print(os.path.dirname(lepton.__file__))'); echo "$PL"
n=0; for f in "$T"/lepton/*.py; do n=$((n+1)); cmp -s "$f" "$PL/$(basename "$f")" || echo "diffère : $(basename "$f")"; done; echo "modules comparés $n"
PYS=$(dirname "$(realpath "$(command -v scion)")")/python; "$PYS" -I -c 'import scion, scion.gitops as g; print(scion.__version__, hasattr(g, "cause"))'
codium --list-extensions --show-versions | LC_ALL=C sort > "$J/6-extensions.txt"; grep -E -i 'lldb|lepton|rtos-views|peripheral' "$J/6-extensions.txt"
XL=~/.vscode-oss/extensions/lepton-distribution.lepton-0.5.4; ls ~/.vscode-oss/extensions/ | grep -i lepton; ls "$XL/out/src/batch.js"; grep -c 'scion.grafted.list' "$XL/out/src/watch.js"
```
Attendu : codes 0 ; `scion version: 0.6.3.4` ; `lepton 0.1.0`, `scion 0.6.3.4 (requis ≥ 0.6.2.0)` ;
`modules comparés 18`, aucune ligne « diffère » (lepton d'ENV-68 installé ; contrôle écrit d'après
le Mac, 18 modules) ; `0.6.3.4 True` (`gitops.cause`, D35) ; `install-vscodium.sh` : ligne
`lepton-distribution.lepton : 0.5.3 → 0.5.4`, `changements 1` ; `lepton-distribution.lepton@0.5.4`,
`vadimcn.vscode-lldb@1.12.3`, `mcu-debug.rtos-views@0.0.16`, `mcu-debug.peripheral-viewer@1.6.4` ;
répertoire `lepton-distribution.lepton-0.5.4`, `batch.js` présent, `watch.js` observe
`.scion.grafted.list` (compte ≥ 1).

**Arrêt** si scion n'est pas 0.6.3.4, si un module de lepton diffère ou si l'extension n'est pas
0.5.4 : ni §9, ni §10, ni §11.

## 7. Copies d'essai et dépôt présent (pour C2, C4, C6)

Avant toute regreffe de `$C5` (§9), pour que les copies partent de l'état de celle du Mac (noyau
2b4a647, 3059 liens) :
```bash
cd "$T"
mkdir -p "$W/c4/rs" "$W/c6/gen"
for d in c4/rs c6/gen; do tar -C "$C5" --exclude=./build -cf - . | tar -C "$W/$d" -xf -; echo "$d copie=$?"; done
python3 -I "$T/$LI" "$W/c4/rs/trunk"; python3 -I "$T/$LI" "$W/c6/gen/trunk" > "$J/7-liens-depart-c6.txt"
lepton check -C "$W/c4/rs" > "$J/7-check.log" 2>&1; echo "code=$?" >> "$J/7-check.log"; tail -2 "$J/7-check.log"
lepton scion new env72lib --type bibliotheque --repo "$D72" --no-seed --no-cmake -C "$W/c6/gen" > "$J/7-scion-new-72.log" 2>&1; echo "code=$?" >> "$J/7-scion-new-72.log"; cat "$J/7-scion-new-72.log"
git -C "$D72" log --oneline --all; git -C "$W/c6/gen"/depots/lepton-seed/env11 status --short | wc -l
ls -a "$W/c4/rs"; find "$W/c4/rs" -name .DS_Store | wc -l
```
Attendu : 2 `copie=0` ; `liens=3059 casses=0 reguliers=0` ; `check` code 0 ;
`dépôt créé : …/depot72 (lib/env72lib)`, code 0 ; 1 commit (`master`) ; graine de `c6/gen` sans
modification (0) ; racine de `c4/rs` et nombre de `.DS_Store` relevés (§10, classes d'écart).

## 8. Règles de permission sur la VM (C2 : réglages, D28, D38 (2), hook)

Toutes les commandes de ce paragraphe sont lancées par la session, **une par appel, telles
qu'écrites** (chemins `~/…` littéraux). La décision de chacune est relevée à la fin dans le
journal de session.

### 8.1 Réglages utilisateur

```bash
python3 -m json.tool ~/.claude/settings.json
```
Attendu : le fichier entier, reporté au rapport, identique à
`rapports/env-66-debian/settings-utilisateur.json`. Le bloc `permissions.allow` a exactement 2
règles, `Bash(pipx install:*)` et `Bash(git clone * https://github.com/lepton-distribution/*)` ;
ni `ask`, ni `deny`, ni `defaultMode` dans `permissions`. Un bloc différent : `QUESTION`.

| N° | Commande | Attendu |
| --- | --- | --- |
| U1 | `pipx install ~/lepton-tools-dev/essais/env-72-absent` | règle utilisateur `Bash(pipx install:*)` (`userSettings`) ; code ≠ 0, rien d'installé |
| U2 | `git clone --depth 1 https://github.com/lepton-distribution/env-72-absent.git ~/lepton-tools-dev/essais/env-72-absent` | règle utilisateur `Bash(git clone * https://github.com/lepton-distribution/*)` ; code ≠ 0 (dépôt inexistant), cible absente |

### 8.2 D38 (2) : enveloppe sur un descendant de `~/tmp-pytest`

Préparation, par la session :
```bash
mkdir -p ~/tmp-pytest/env-72-enveloppe/sous/plus && touch ~/tmp-pytest/env-72-enveloppe/sous/plus/f ~/tmp-pytest/env-72-enveloppe/g && find ~/tmp-pytest/env-72-enveloppe | sort
```
Puis, règle `allow`, une par appel, forme exacte, code lu dans le résultat de l'outil :

| N° | Commande | Attendu |
| --- | --- | --- |
| R1 | `scripts/supprimer-essai.sh ~/tmp-pytest/env-72-enveloppe/..` | code 2, « non résoluble » ; rien supprimé |
| R2 | `scripts/supprimer-essai.sh ~/tmp-pytest/../lepton-tools-dev` | code 2, « hors des bornes » ; rien supprimé |
| E1 | `scripts/supprimer-essai.sh ~/tmp-pytest/env-72-enveloppe/sous` | code 0 ; `sous/` supprimé, `env-72-enveloppe/g` gardé |

Après E1 : `find ~/tmp-pytest/env-72-enveloppe | sort` → `env-72-enveloppe` et `g` seuls ;
`ls -d ~/tmp-pytest/env-66 ~/lepton-tools-dev` présents. `env-72-enveloppe` est supprimé au §14.

### 8.3 D28 : invite à refuser ; hook

| N° | Commande | Attendu |
| --- | --- | --- |
| A1 | `scion graft-update -v ~/lepton-tools-dev/essais/env-72-absent` | règle `ask` : invite ; **l'utilisateur la refuse** |
| H1 | `touch ~/lepton-tools-dev/essais/env-72-essai/c6/gen/trunk/essai-hook` | hook : refus sans invite |

Avant A1 : `AVANCEMENT` « **À REFUSER** : `scion graft-update -v ~/lepton-tools-dev/essais/env-72-absent`
(cible absente) ; après le refus, relancer par « reprendre R72-1 au §8.3, H1 » ». Aucun autre
message entre cet `AVANCEMENT` et le lancement.

Après H1 :
```bash
cd "$T"
ls -d ~/lepton-tools-dev/essais/env-72-absent "$W/c6/gen/trunk/essai-hook" 2>&1; pipx list --short | grep -c env-72
python3 -I "$T/$LI" "$W/c6/gen/trunk" | cmp - "$J/7-liens-depart-c6.txt" && echo "liens de c6 = départ"
F=$(ls -t ~/.claude/projects/*lepton-tools-dev-lepton-tools/*.jsonl | head -1); echo "$F"
python3 -I "$T/$DEC" "$F" > "$J/8-decisions.tsv"; cut -c1-180 "$J/8-decisions.tsv" | grep -E 'pipx install|git clone|supprimer-essai|graft-update|touch'
```
Attendu, dans `8-decisions.tsv` :
- §6.2 `pipx install --force ~/lepton-tools-dev/lepton-tools` : `accept config rule projectSettings`
  (ou `subcommandResults`) ;
- U1, U2 : `accept config rule userSettings` (ou `subcommandResults` avec la règle utilisateur) ;
- R1, R2, E1 : `accept config` par la règle `allow` du dépôt (`subcommandResults`), aucun
  `classifier` ;
- A1 : `rejet-invite` ; H1 : `reject hook hook` ;
- cible absente, `essai-hook` absent, aucun paquet `env-72` ; liens de c6 = départ.

Écarts, sans arrêt sauf mention :
- U1 ou U2 au classifieur : réglages utilisateur non lus (session ouverte avant le §0 ?), à
  relever ;
- R1, R2 ou E1 au classifieur, ou un code différent : à relever ;
- une invite non apparue pour A1 : **arrêt**, `QUESTION` (la commande serait exécutée sans
  accord ; elle reste sans effet, la cible étant absente).

## 9. Regreffe de `$U`, `$E13`, `$C5` (C3) et `$R53` (pour C7)

Pour chaque rootstock de la liste `env-28-debian`, `env-13-debian`, `env-53-c5`,
`env-53-debian`, dans cet ordre (`$C5` après les copies du §7) :
1. par la session, depuis `$T` :
   ```bash
   bash "$T/$RG" avant ~/lepton-tools-dev/essais/<nom> "$J/regreffes"
   for g in ~/lepton-tools-dev/essais/<nom>/depots/lepton-seed*/*; do echo "graine $g branche=$(git -C "$g" branch --show-current) head=$(git -C "$g" rev-parse --short HEAD)"; done
   ```
   (branche de la graine clonée avant la regreffe, D33 : `original-tree` attendu pour `$U`,
   `$E13`, `$R53`) ;
2. `AVANCEMENT` « **À CONFIRMER** : `scion graft-update -v ~/lepton-tools-dev/essais/<nom>` »,
   puis la session lance, telle quelle :
   ```bash
   scion graft-update -v ~/lepton-tools-dev/essais/<nom> > ~/env-72-journaux/regreffes/<nom>-graft-update.log 2>&1; echo "code=$?" >> ~/env-72-journaux/regreffes/<nom>-graft-update.log
   ```
   L'utilisateur confirme l'invite par « Oui » (PA-P pour ces quatre rootstocks, PA-131).
3. par la session :
   ```bash
   cd "$T"
   bash "$T/$RG" apres ~/lepton-tools-dev/essais/<nom> "$J/regreffes"
   Z=~/lepton-tools-dev/essais/<nom>; L=$J/regreffes/<nom>-graft-update.log
   resume() { sed -e "s|$Z|<R>|g" -e "s|$HOME|<HOME>|g" "$1" | grep -v -E '^git |\(cwd=|^  |\.DS_Store|chemin\(s\) ignoré\(s\)|^code='; }
   grep -E 'feuilles liées|ignoré|graine' "$L"
   ```
   et, pour `$U`, `$E13` et `$R53` (rootstocks de la graine `original-tree`) :
   ```bash
   mkdir -p "$J/9-resume-<nom>"; resume "$L" > "$J/9-resume-<nom>/graft-update-resume.txt"
   cmp_mac "$T/$A/c3" "$J/9-resume-<nom>" graft-update-resume.txt
   python3 -I "$T/$C" "$Z" "$T/$A50/trunk-liens.txt" "$J/9-<nom>-controle" > "$J/9-<nom>-controle.log" 2>&1; echo "code=$?" >> "$J/9-<nom>-controle.log"; tail -3 "$J/9-<nom>-controle.log"
   normc() { sed -E 's/ ignorecase=[^ ]*//; s/ ko_hors_git=.*//' "$1"; }
   diff <(normc "$T/$Y/attendu/clones-rootstock-mac.txt") <(normc "$J/regreffes/<nom>-tiers-apres/clones.txt") && echo "clones = Mac (hors ignorecase et tailles)"
   ```

Après la quatrième regreffe : `[AVANCEMENT R72-1] fin des invites de la VM jusqu'au push` (D39).

Attendu, `$U`, `$E13` et `$R53` (Mac, `essais/env-13-vierge`, `attendu/c3/env-13-vierge-bilan.txt`) :
- graine sur `original-tree` avant ; aucun refus de scion (D33 : graine à sa version) ;
- `graft-update code=0 ; avancés : 1 ; git clone : 0 ; extraction partielle : 0 ; conflit/refus : 0` ;
  `depots/lepton/original/master avancé : 2b4a647 -> 0c2e43e` ; « 3889 feuilles liées » ; aucune
  ligne `.DS_Store` sur la VM ;
- `graft-update-resume.txt identique`, `écarts=0 / 1` : 83 lignes, dont
  `fatal: not a git repository (or any of the parent directories): .git` (stderr de git écrit par
  `-v` pour la source non git `generation/building`, D22 ; en français sur la VM, ramené par
  `cmp_mac`). Contre ENV-66, seule la ligne du noyau change ;
- `clones : 1 ligne(s) changée(s)` (noyau) ; liens 3889 → 3889, ajoutés 0, retirés 0 ;
  `controler-trunk CONFORME code=0` contre les liens d'avant **et** contre l'attendu de R50-1 ;
- `tiers : 8 clone(s)`, extraits et `sparse-checkout` ≠ attendu : **0 / 16** ; `clones = Mac` ;
- `check code=0`, `generate` avant et après code 0, `espace diff=0` ; trunk sans fichier régulier ni
  lien cassé.

Attendu, `$C5` : un seul clone avancé (noyau 2b4a647 → 0c2e43e) ; `salut` accepté (sans amont,
`modifs=2`, comme en R66-1) ; graine locale `env11` relevée (graine par chemin : non contrôlée par
D33, PA-127 (3)) ; 3059 liens inchangés, `CONFORME` contre les liens d'avant ; les 2 clones tiers
F7 conservés de R53-1 ne sont pas greffés, inchangés (0 / 4) ; `check` code 0 ; espace identique.

Un refus de scion (clone hors version, graine hors version, graine divergée) : écart à exposer,
sans contournement.

## 10. D29, D30, D32, D37 : lepton (C4)

Sur `$W/c4` (§7), avec lepton réinstallé (§6) :
```bash
cd "$T"
bash $X/chemins.sh ~/lepton-tools-dev/essais/env-72-essai/c4 apres "$J/10-c4-chemins" clangd > "$J/10-c4-chemins.log" 2>&1; echo "code=$?" >> "$J/10-c4-chemins.log"
bash $X/graine.sh ~/lepton-tools-dev/essais/env-72-essai/c4 apres-graine "$J/10-c4-graine" > "$J/10-c4-graine.log" 2>&1; echo "code=$?" >> "$J/10-c4-graine.log"
tail -1 "$J/10-c4-chemins.log" "$J/10-c4-graine.log"; ls "$J/10-c4-chemins" | wc -l; ls "$J/10-c4-graine" | wc -l
cmp_mac "$T/$A/c4-chemins" "$J/10-c4-chemins" > "$J/10-c4-chemins-cmp.txt"; echo "code=$?"; grep -v 'identique$' "$J/10-c4-chemins-cmp.txt" | head -60
cmp_mac "$T/$A/c4-graine" "$J/10-c4-graine" > "$J/10-c4-graine-cmp.txt"; echo "code=$?"; grep -v 'identique$' "$J/10-c4-graine-cmp.txt" | head -60
diff <(cut -f1-6 "$T/$A/c4-chemins/resume.tsv") <(cut -f1-6 "$J/10-c4-chemins/resume.tsv") && echo "resume.tsv colonnes 1-6 = Mac"
python3 -I "$T/$LI" "$W/c4/rs/trunk"
```
Attendu (Mac, `attendu/c4-chemins/` 165 relevés, `attendu/c4-graine/` 244 relevés ;
`rapports/env-72-mac.md` §1.4) :
- deux `code=0` ; 165 et 244 relevés ;
- **D29** : `check FILE`, `seed mkconf import`, `seed new --mkconf` en `~/…` et `~<U>/…` acceptés
  (code 0) ; `~inconnu68/…` refusé par lepton (« répertoire personnel de « ~inconnu68 »
  introuvable ») ; **D30** : `p6-r`, `p6-rs`, `p6-rw`, `p6-rd` donnent un `clangd.path` absolu ;
  **D32** : r1, r2, r5 `--purge` refusé, code 2, état = ajouté ; **D37** : g1 à g5 selon
  `rapports/env-68-lepton.md` §4.2 ;
- `cmp_mac` : écarts admis, et eux seuls (classes d'écart relevées sur la copie distincte du Mac,
  `rapports/env-72-mac.md` §1.5, D38 (3)) :
  - **hôte** — `p6-n.cmd`, `p6-n.clangd` : nom et chemin de clangd (`clangd`, `/usr/bin/clangd`
    contre `clangd-mp-21`, `/opt/local/bin/clangd-mp-21`) ; seule classe que le Mac ne simule pas ;
  - **longueur des chemins** — `resume.tsv` de `c4-chemins` : la colonne 7 (message) est tronquée
    avant normalisation ; colonnes 1 à 6 = Mac ;
  - **fichiers ignorés du Mac** — `n1-a.err`, `n1-d.err`, `n1-r.err`, `n1-t.err`, `n1-u.err` : la
    ligne « 13 chemin(s) ignoré(s) par git » (`.DS_Store` des clones du Mac) manque sur la VM ;
  - **graine `env11`** — `p6-*.out` (7 fichiers) : liste des presets de la graine de `$C5`
    (`env11-debug-qemu` seul sur la VM, R66-1) ; `g1-status.out`, `r1-status.out` : commit de la
    graine et de ses presets, configurations déclarées ;
  - **commits locaux** — `r1-status.out` : commit du clone `library-env68lib` après `seed add`,
    différent à chaque passage ;
  - **langue de git** — ramenée par `cmp_mac` ; une traduction absente de la table : relever la
    ligne de `po/fr.po` v2.47.3 ;
  au Mac, la copie distincte (`tar`, sans `.DS_Store`, autre graine, une configuration) donne
  `écarts=13 / 165` et `écarts=2 / 244`, tous dans ces classes ;
- liens de `c4/rs` : `liens=3059 casses=0 reguliers=0`.

Les deux scripts sont hors règle (classifieur ; acceptés au Mac) ; `graine.sh` appelle
`scripts/supprimer-essai.sh` de l'intérieur, dans `$W` seulement. Un refus : `AVANCEMENT`, sans
contournement.

Tout autre écart : relever le fichier et le `diff`, sans correction. Le F7 n'est pas touché (les
clones F7 de `$C5` ne sont pas greffés et les scripts n'utilisent que l'an386).

## 11. D35, D33 : scion ; pytest (C5)

### 11.1 Fixtures d'ENV-70, d'ENV-65, d'ENV-60 et d'ENV-56

Les fixtures importent les aides de test de seed.scions : il leur faut un clone au tag. Par la
session, une commande par appel :
```bash
git clone https://github.com/lepton-distribution/seed.scions.git ~/lepton-tools-dev/essais/env-72-essai/seed-scions
```
(règle `allow` du dépôt, forme exacte, sans redirection), puis :
```bash
git -C ~/lepton-tools-dev/essais/env-72-essai/seed-scions switch --detach 0.6.3.4
git -C "$SS" log --oneline -1; git -C "$SS" status --short | wc -l
cd "$T"
python3 -I $X/fixture70.py "$SS" "$(command -v scion)" "$FX/f70" "$J/11-fixture70" /usr/bin/git > "$J/11-fixture70.log" 2>&1; echo "code=$?" >> "$J/11-fixture70.log"; tail -3 "$J/11-fixture70.log"
python3 -I doc/devenv/rapports/env-65-scion/fixture.py "$SS" "$(command -v scion)" "$FX/f65" "$J/11-fixture65" > "$J/11-fixture65.log" 2>&1; echo "code=$?" >> "$J/11-fixture65.log"; tail -3 "$J/11-fixture65.log"
python3 -I doc/devenv/rapports/env-60-scion/fixture.py "$SS" "$(command -v scion)" "$FX/f60" "$J/11-fixture60" > "$J/11-fixture60.log" 2>&1; echo "code=$?" >> "$J/11-fixture60.log"; tail -3 "$J/11-fixture60.log"
python3 -I doc/devenv/rapports/env-56-scion/fixture.py "$SS" "$(command -v scion)" "$FX/f56" "$J/11-fixture56" > "$J/11-fixture56.log" 2>&1; echo "code=$?" >> "$J/11-fixture56.log"; tail -3 "$J/11-fixture56.log"
for f in 70 65 60 56; do cmp_mac "$T/$A/fixture$f" "$J/11-fixture$f" > "$J/11-fixture$f-cmp.txt"; echo "fixture$f code=$? $(tail -1 "$J/11-fixture$f-cmp.txt")"; grep -v 'identique$' "$J/11-fixture$f-cmp.txt" | head -30; done
for c in k01-218.git-err k01-250.git-err k01.err k02.err k03.err; do echo "== $c"; cat -v "$J/11-fixture70/$c"; done
cat -v "$J/11-fixture60/k07.err" "$J/11-fixture56/f05.err"
```
Attendu (Mac, identiques aux `*-apres/` d'ENV-70, au nom de la base près) : `473b653`, propre ;
quatre `code=0` ; base `essais/env-72-fixture` des deux côtés :
- **fixture65, fixture60, fixture56 : écarts=0** ;
- **fixture70 : écarts=2 / 202**, `k01-218.git-err` et `k01-250.git-err` seuls : ce sont les
  sorties brutes de git (`git clone -b nope --quiet --single-branch`), par git 2.18.0 et 2.50.1
  au Mac, par git 2.47.3 deux fois sur la VM (première ligne `$ /usr/bin/git …` ; corps
  `warning: Could not find remote branch nope to clone.` puis
  `fatal: Remote branch nope not found in upstream origin`) ;
- **D35, preuve** : `k01.err`, `k02.err`, `k03.err` (fixture70), `k07.err` (fixture60) et
  `f05.err` (fixture56) se terminent par `(code 128) : fatal: Remote branch nope not found in
  upstream origin` — la cause, **non** l'avertissement (R66-1 : `warning: Could not find remote
  branch nope to clone.`) ;
- **D33** : g01-g21 de fixture70 = Mac (g04, g06, g11, g13, g21 : code 1, « graine hors de la
  version demandée, non mise à jour (rien n'a été modifié) » ; témoins inchangés).

Un écart restant après `cmp_mac` : relever le fichier et le `diff` ; si c'est une traduction de
git absente de la table, citer la ligne de `po/fr.po` v2.47.3 qui la donne (pas de correction de
l'outil sur la VM).

### 11.2 D35 en français

Les fixtures fixent `LC_ALL=C`. La cause en français se relève à part, dans la locale de la
session (sans `LC_ALL`), sur le rootstock de k03 laissé par la fixture (k03 : code 2, rien n'est
créé) :
```bash
cd ~/lepton-tools-dev/essais/env-72-fixture/f70/k03/rootstock && scion seed-add --single-branch ~/lepton-tools-dev/essais/env-72-fixture/f70/k03/seed > ~/env-72-journaux/11-d35-fr.log 2>&1; echo "code=$?" >> ~/env-72-journaux/11-d35-fr.log
cd "$T"; cat -v "$J/11-d35-fr.log"; ls -A "$FX/f70/k03/rootstock/depots" | wc -l
```
Attendu : `code=2` ; message `erreur : échec de « git clone -b nope --quiet --single-branch … » (code
128) : fatal⍽: La branche distante nope n'a pas été trouvée dans le dépôt amont origin`
(`cat -v` : `fatalM-BM- :`) — la cause en français, **non** `avertissement⍽: Impossible de
trouver la branche distante 'nope' à cloner.` (forme relevée en R66-1, `rapports/env-66-debian.md`
§5.3) ; `depots` inchangé. Au Mac (git non traduit), la même commande donne la cause anglaise.
Si git écrit en anglais : relever `LANG`, `LC_ALL`, `locale` (§5), sans arrêt ; la preuve en
français reste à faire par l'utilisateur.

### 11.3 pytest de lepton-tools

Par la session, règle `allow`, forme exacte (sans redirection, sans `TMPDIR=` ; le journal est
écrit par `--junitxml`) :
```bash
~/lepton-tools-dev/venv-test/bin/pytest -q -rs -p no:cacheprovider --basetemp ~/tmp-pytest/env-72 --junitxml ~/env-72-journaux/11-pytest.xml
```
Puis :
```bash
cd "$T"
python3 -I -c 'import sys,xml.etree.ElementTree as E; s=E.parse(sys.argv[1]).getroot().find("testsuite"); print({k:s.get(k) for k in ("tests","failures","errors","skipped","time")})' "$J/11-pytest.xml"
for m in test_proteger_trunk test_garde_ask test_supprimer_essai test_milestone3 test_comparer_releves; do echo "$m $(grep -o "classname=\"tests.$m\"" "$J/11-pytest.xml" | wc -l)"; done
~/lepton-tools-dev/venv-test/bin/python -m pip show lepton | grep -i -E '^(version|location|editable)'
git -C "$T" status --short | head -5
```
Attendu (Mac, 2026-11-24, Python 3.11.5, scion 0.6.3.4) : **616 passed**, 0 échec, 0 erreur, 0 ignoré ; `test_proteger_trunk` 118, `test_garde_ask` 46,
`test_supprimer_essai` 70, `test_milestone3` 62, `test_comparer_releves` 13 (11 min 44, avec un essai
concurrent) ; lepton en mode
éditable depuis `$T` ; lepton-tools propre (hors rapport). Un test ignoré ou en échec : relever
son nom et son message, le relancer seul une fois (`~/lepton-tools-dev/venv-test/bin/pytest -q -rs
-p no:cacheprovider --basetemp ~/tmp-pytest/env-72 <test>`), consigner les deux résultats ; pas
de correction.

### 11.4 D36 : extension 0.5.4 (C6)

T3 de D36 (`rapports/env-69-extension.md` §4.1), dans VSCodium sur la VM, par l'utilisateur
(PA-131), sur `$W/c6/gen`, avec le greffon `env72lib` de `$D72`. Défaut corrigé par 0.5.4 : un
greffon ajouté **au terminal** n'entrait pas dans la liste observée ; la suppression de son clone
ne donnait alors aucune notification. Sous Linux, l'observateur de fichiers est inotify (au Mac,
FSEvents) : c'est la seule preuve sur cette plateforme.

1. `AVANCEMENT` à l'utilisateur :
   - ouvrir `codium ~/lepton-tools-dev/essais/env-72-essai/c6/gen/env11.code-workspace`, attendre
     la vue Lepton, ouvrir le canal de sortie « Lepton » ;
   - relever la dernière ligne « Observation de N greffon(s) », puis répondre « reprendre R72-1
     au §11.4, ajout ».
2. Par la session, VSCodium restant ouvert, **au terminal** (aucune commande de l'extension) :
   ```bash
   cd "$T"
   lepton seed add env72lib "file://localhost$D72@master" --type bibliotheque --no-cmake -C "$W/c6/gen" > "$J/11-d36-add.log" 2>&1; echo "code=$?" >> "$J/11-d36-add.log"; tail -3 "$J/11-d36-add.log"
   python3 -I "$T/$LI" "$W/c6/gen/trunk"
   ```
   Attendu : code 0 ; `liens=3062 casses=0 reguliers=0` (3059 + 3 de `env72lib`). `AVANCEMENT` à
   l'utilisateur : attendre 5 s, relever la nouvelle ligne « Observation de N+1 greffon(s) » du
   canal (sans commande de l'extension) et toute notification, puis répondre « reprendre R72-1
   au §11.4, suppression ».
3. Par la session, règle `allow`, forme exacte :
   ```bash
   scripts/supprimer-essai.sh ~/lepton-tools-dev/essais/env-72-essai/c6/gen/depots/lepton/library-env72lib/master
   ```
   puis `AVANCEMENT` à l'utilisateur : relever les notifications parues (attendre 5 s), puis
   répondre « reprendre R72-1 au §11.4, fin ». La session relève :
   ```bash
   cd "$T"; python3 -I "$T/$LI" "$W/c6/gen/trunk"
   ```
   Attendu : **une seule notification**, « Clone de library-env72lib supprimé hors de lepton : ses
   liens du trunk sont cassés (lepton seed status) » ; `liens=3062 casses=3`. `$W/c6/gen` n'est pas
   rétabli : il est supprimé au §14.
4. L'utilisateur ferme VSCodium.

« Observation de N+1 » absente après l'ajout, ou aucune notification après la suppression : écart
à exposer, avec le texte relevé (comportement de 0.5.3).

## 12. Reconstructions et commande de miroir (C7)

### 12.1 Reconstructions

Périmètre : host et les 16 presets croisés (QEMU : construction, fumée, banc KAL ; cartes :
construction et capture seulement, **aucun flash**), dans `$R53` regreffé au §9. `$R53` garde le
chemin d'`env-53-debian` : les chaînes `__FILE__` des presets FreeRTOS sont celles de l'oracle de
référence. `LEPTON_EMBOS_ROOT` vient du profil (§0, §5) : jamais en tête de la commande.
Commande longue (≈ 4 min en R66-1) : `AVANCEMENT` au lancement.

```bash
cd "$T" && git switch -c devenv/env-72-debian devenv/env-72
scripts/oracle/rejouer-oracle.sh ~/lepton-tools-dev/essais/env-53-debian doc/devenv/rapports/oracles/env-72-debian --qemu qemu-mps2-an386-embos --qemu qemu-mps2-an386-embos-soft --qemu qemu-mps2-an386-freertos --qemu qemu-mps2-an386-freertos-soft --qemu qemu-mps2-an500-embos --qemu qemu-mps2-an500-freertos --carte nucleo-f429zi-embos --carte nucleo-f429zi-freertos --carte nucleo-f439zi-embos --carte nucleo-f439zi-freertos --carte nucleo-wl55jc1-embos --carte nucleo-wl55jc1-freertos --carte samd21-xplained-pro-embos --carte samd21-xplained-pro-freertos --carte stm32f746g-disco-embos --carte stm32f746g-disco-freertos > ~/env-72-journaux/12-rejouer.log 2>&1; echo "code=$?" >> ~/env-72-journaux/12-rejouer.log
```
Puis :
```bash
cd "$T"; O=doc/devenv/rapports/oracles
tail -25 "$J/12-rejouer.log"
grep -h "tests passed" $O/env-72-debian/*/ctest.log $O/env-72-debian/*/banc-kal.log
grep -h "peripheriques" $O/env-72-debian/qemu-mps2-an386-*/banc-kal.log
python3 -I "$T/$LI" "$R53/trunk" > /dev/null; find "$R53/trunk" -name __pycache__ | wc -l
```
Attendu : code 0 au **premier passage** (embOS trouvé par la variable du profil, D38 (1)) ; host
ctest 7/7 ; 16 presets construits ; fumée réussie ; banc QEMU identique à R66-1 : an386 20/20,
an386 soft 16/16, an500 19/19 ; `qemu-mps2-an386.peripheriques` **Passed** dans les 4
`banc-kal.log` an386 ; trunk sans fichier régulier, lien cassé ni `__pycache__`.

### 12.2 Comparaisons

```bash
cd "$T"; O=doc/devenv/rapports/oracles
norm() { grep -E '^(section|symbole)' "$1" | sed -E 's/ \[.*$//; s/ +: /: /' | grep -v -E '^section [^:]*: \.debug_' | LC_ALL=C sort; }
diff -q $O/env-66-debian/host/mklepton-empreintes.sha256 $O/env-72-debian/host/mklepton-empreintes.sha256 && echo "mklepton = R66-1"
diff -q $O/env-52-apres/host/mklepton-empreintes.sha256 $O/env-72-debian/host/mklepton-empreintes.sha256 && echo "mklepton = Mac env-52-apres"
for p in $(ls $O/env-72-debian | grep -v -e host -e ctest-N -e compilation -e '\.log$'); do
  python3 scripts/oracle/comparer-oracle.py $O/env-66-debian/$p $O/env-72-debian/$p > "$J/12-cmp-R66-$p.txt" 2>&1; a=$?
  python3 scripts/oracle/comparer-oracle.py $O/env-52-apres/$p $O/env-72-debian/$p > "$J/12-cmp-Mac-$p.txt" 2>&1; b=$?
  echo "$p comparer_R66-1=$a comparer_Mac=$b hors_debug=$(norm $J/12-cmp-R66-$p.txt | wc -l)"
done | tee "$J/12-bilan.txt"
```
Attendu :
- mklepton : empreintes identiques à `env-66-debian` et à `env-52-apres` ;
- `comparer_R66-1` **0** pour les **16 presets**, `hors_debug=0` (aucun écart admis) ;
- `comparer_Mac` : informatif (1 attendu partout, chaînes différentes).

Un `comparer_R66-1` non nul : écart à exposer, avec l'extrait du `12-cmp-R66-<preset>.txt` ; si
seules des sections `.debug_*` changent, le dire (`hors_debug=0`) ; pas de correction.

### 12.3 Commande de miroir, à blanc (D40)

```bash
scion mirror-sync --dry-run -v ~/lepton-tools-dev/essais/env-53-debian > ~/env-72-journaux/12-mirror-sync.log 2>&1; echo "code=$?" >> ~/env-72-journaux/12-mirror-sync.log
```
Puis :
```bash
cd "$T"
grep -E 'référence\(s\) à envoyer|signalement' "$J/12-mirror-sync.log"; tail -1 "$J/12-mirror-sync.log"
python3 -I "$T/$C" "$R53" "$T/$A50/trunk-liens.txt" "$J/12-controle-R53" | tail -1
```
Attendu (ENV-71, miroirs synchronisés le 2026-11-24 à 14:36 +0100) : code 0 ; 8 lignes
`miroir … : 0 référence(s) à envoyer, 0 signalement(s)` ; trunk de `$R53` `CONFORME`. Une
référence « à envoyer » n'est admise que si une publication de l'amont postérieure au
2026-11-24 14:36 +0100 l'explique : la relever, puis relever la référence de l'amont
(`git ls-remote https://github.com/STMicroelectronics/<nom>.git`), sans arrêt ; rien n'est envoyé
(PA-P). Un signalement : écart à exposer. Jamais sans `--dry-run`.

## 13. Cartes (C8)

Proposé écarté au PA-131 : ni binaire, ni flash, ni sonde ne changent. Aucune commande OpenOCD.

## 14. Nettoyage de la VM (C9)

Après le commit du rapport (§15) seulement. Relevé par la session :
```bash
du -sh "$W" "$FX" ~/env-66-journaux ~/tmp-pytest/env-66 ~/tmp-pytest/env-72-enveloppe 2>&1
```
Puis, par la session, règle `allow` :
```bash
scripts/supprimer-essai.sh ~/lepton-tools-dev/essais/env-72-essai ~/lepton-tools-dev/essais/env-72-fixture ~/env-66-journaux ~/tmp-pytest/env-66 ~/tmp-pytest/env-72-enveloppe
```
Puis la session vérifie l'absence (`ls -d …`) et le consigne. Conservés : `$U`, `$E13`, `$C5`
(regreffés au §9), `$R53`, `$J`, `~/tmp-pytest` et `~/tmp-pytest/env-72`. Périmètre à valider au
PA-131.

## 15. Critères et rapport

| Critère | Attendu |
| --- | --- |
| C1 Versions, variables | `git ls-remote` = Mac (§5) ; `settings.json`, hook, enveloppe, outil de comparaison = Mac ; Claude Code relevé (journal) ; **variables du PA-121 = attendu** (`LEPTON_EMBOS_ROOT` et `RTOS.h`, six absentes ; `LANG`, `LC_ALL` relevées) ; git 2.47.3 ; scion 0.6.3.4 par `install-debian.sh` (défaut `SCION_REF`), `gitops.cause` présent ; lepton `pipx` code 0, `scion 0.6.3.4 (requis ≥ 0.6.2.0)`, 18 modules = dépôt ; extension 0.5.4 par `install-vscodium.sh` (`0.5.3 → 0.5.4`) ; chaîne relevée |
| C2 Règles, enveloppe, hook | réglages relus en entier, bloc `allow` = 2 règles ; U1, U2 par la règle utilisateur, sans effet ; R1, R2 code 2 sans effet, E1 code 0 (descendant de `~/tmp-pytest` supprimé, voisin gardé), les trois par la règle du dépôt ; A1 annoncé « À REFUSER », invite, refusée ; H1 hook ; `pipx install --force` par la règle du dépôt ; `graft-update` ×4 annoncés « À CONFIRMER », invites confirmées ; `git clone` de seed.scions et pytest par la règle ; aucune cible créée ni supprimée à tort |
| C3 Regreffes | graines clonées relevées avant, sur leur version ; `$U`, `$E13` (et `$R53`, pour C7) : code 0, seul le noyau avance (2b4a647 → 0c2e43e), aucun clone, résumé = Mac (`cmp_mac`), liens inchangés (3889), `CONFORME` (attendu de R50-1), clones tiers 0 / 16, `clones = Mac`, `check` 0, espace = avant ; `$C5` : noyau seul, 3059 liens inchangés, `check` 0 |
| C4 D29, D30, D32, D37 | §10 : deux `code=0` ; écarts limités aux classes listées (hôte, longueur des chemins, fichiers ignorés du Mac, graine `env11`, commits locaux) ; colonnes 1-6 de `resume.tsv` = Mac ; liens de `c4/rs` = départ |
| C5 D35, D33, pytest | §11.1 : fixtures 65, 60, 56 écarts=0 ; fixture70 écarts limités à `k01-218.git-err`, `k01-250.git-err` ; k01, k02, k03, k07, f05 : la cause `fatal: Remote branch nope not found in upstream origin` ; g04, g06, g11, g13, g21 code 1 ; §11.2 : la cause en français (`fatal⍽: La branche distante…`) ; §11.3 : pytest 616 passed |
| C6 D36 | extension 0.5.4 installée ; T3 : « Observation de N+1 greffon(s) » après `seed add` au terminal, une seule notification « Clone de library-env72lib supprimé hors de lepton… » après la suppression du clone ; états relevés |
| C7 Constructions, miroir | premier passage code 0 (variable du profil) ; host ctest 7/7 ; 16 presets construits ; QEMU fumée et banc 20/20, 16/16, 19/19, `peripheriques` ×4 ; mklepton = `env-66-debian` = `env-52-apres` ; `comparer_R66-1` 0 pour les 16 presets ; `mirror-sync --dry-run` : code 0, 8 miroirs, 0 à envoyer (ou expliqué par l'amont), 0 signalement ; rien envoyé |
| C8 Cartes | écarté (à confirmer au PA-131) |
| C9 Nettoyage | `$W`, `$FX`, `~/env-66-journaux`, `~/tmp-pytest/env-66`, `~/tmp-pytest/env-72-enveloppe` supprimés par l'enveloppe (descendants de `~/tmp-pytest` compris, D38 (2)) ; absents |

Avant le commit, relevé final des décisions (toute la session) :
```bash
cd "$T"; F=$(ls -t ~/.claude/projects/*lepton-tools-dev-lepton-tools/*.jsonl | head -1)
python3 -I "$T/$DEC" "$F" > "$J/15-decisions.tsv"; wc -l < "$J/15-decisions.tsv"
```

Rapport `doc/devenv/rapports/env-72-debian.md` sur `devenv/env-72-debian`, avec :
- l'hôte, les versions, les variables d'environnement et la session (répertoire de travail, Claude
  Code du journal, réglages) ;
- la table des critères ;
- C2 : le contenu de `~/.claude/settings.json` ; la table des commandes et décisions (extrait de
  `15-decisions.tsv` : U1, U2, R1, R2, E1, A1, H1, `pipx install`, `graft-update` ×4, `git clone`,
  pytest, push), avec l'heure de chaque `AVANCEMENT` « À REFUSER » / « À CONFIRMER » et du
  lancement qui le suit ;
- la table des presets : construction, fumée, banc KAL, `comparer_R66-1`, `comparer_Mac` ;
- C3 : les quatre bilans, les branches des graines avant, les lignes `clones.txt` après,
  `ignorecase`, tailles ;
- C4, C5, C6 : bilans `écarts=…` de `cmp_mac`, lignes de git (`cat -v`), codes, notifications ;
- pytest, miroir, nettoyage ;
- les écarts et constats ;
- le journal des messages §2bis (ID, date, résumé, remis ou non) ;
- ce qui n'a pas été fait.

Sous `doc/devenv/rapports/env-72-debian/` : `15-decisions.tsv` (chemin personnel remplacé par
`<HOME>`), `settings-utilisateur.json` (sortie du §8.1), `5-variables.txt` (relevé des variables
du §5), `10-c4-chemins/`, `10-c4-graine/`, `11-fixture70/`, `11-fixture65/`, `11-fixture60/`,
`11-fixture56/`, `11-d35-fr.log`, `11-pytest.xml`, et pour chaque rootstock du §9
`<nom>-bilan.txt`, `<nom>-graft-update.log`, `<nom>-tiers-apres/clones.txt` ; l'oracle
`doc/devenv/rapports/oracles/env-72-debian/` (C7). Commit sur `devenv/env-72-debian` (créée au
§12.1), puis `QUESTION` à l'utilisateur pour le push (PA-P ; `AVANCEMENT` « À CONFIRMER :
`git push origin devenv/env-72-debian` »), puis le §14, puis `FIN-*`.
