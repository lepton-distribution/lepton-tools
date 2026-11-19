# Consigne — session Claude Code sur la VM Debian — ENV-66 (validation Debian groupée)

Fichier autonome : avec `ORCHESTRATION.md` §2bis, il suffit à conduire la session VM. Rédigé le
2026-11-19 par la session Mac `validation-debian-env-66` (tâche 1 d'ENV-66), repris de
`consignes/env-61-debian.md`. Validé par l'utilisateur au PA-119 (2026-11-19) : préalable du §0
(retrait de la règle `unittest` par l'utilisateur, relance de la session) ; regreffe de `$U`,
`$E13`, `$C5` et `$R53` (C3) ; trois fixtures (C5) ; D23 par le runtime de VSCodium et D24 dans
VSCodium sur la VM, par l'utilisateur (C6, option (a)) ; reconstruction des 16 presets et miroir
à blanc maintenus (C7) ; cartes écartées (C8) ; nettoyage tel qu'écrit (C9).
Son texte est envoyé tel quel dans l'ordre `R66-1`.

## 0. Préalable, avant l'ordre (utilisateur) — PA-119

Les réglages et le hook du dépôt sont lus par une session lancée dans `$T`. Les réglages
utilisateur ne sont lus qu'au démarrage d'une session (D26, PA-111). Avant l'envoi de `R66-1`,
l'utilisateur, sur la VM, **session Claude Code fermée** :
1. dans un terminal :
   ```bash
   cd ~/lepton-tools-dev/lepton-tools && git status --short && git fetch origin && git switch devenv/env-66 && git merge --ff-only origin/devenv/env-66 && git log --oneline -1
   ```
2. relève `~/.claude/settings.json` en entier, avant toute modification :
   ```bash
   mkdir -p ~/env-66-journaux && cp -p ~/.claude/settings.json ~/env-66-journaux/0-settings-avant.json && python3 -m json.tool ~/.claude/settings.json > ~/env-66-journaux/0-settings-avant.txt; echo "code=$?"
   ```
3. retire de `~/.claude/settings.json`, avec un éditeur, **la seule** entrée
   `"Bash(python3 -m unittest discover *)"` de `permissions.allow` (et la virgule qui la précède),
   sans toucher au reste (PA-111 (1)) ;
4. compare :
   ```bash
   python3 -m json.tool ~/.claude/settings.json > ~/env-66-journaux/0-settings-apres.txt; echo "code=$?"; diff ~/env-66-journaux/0-settings-avant.txt ~/env-66-journaux/0-settings-apres.txt
   ```
   Attendu : `code=0` ; le `diff` ne montre que l'entrée retirée et la virgule de la ligne
   `git clone`. Le bloc devient (rapport d'ENV-62, §D26) :
   ```json
   "allow": [
       "Bash(pipx install:*)",
       "Bash(git clone * https://github.com/lepton-distribution/*)"
   ]
   ```
5. ouvre une **nouvelle** session Claude Code **dans `~/lepton-tools-dev/lepton-tools`**, en mode
   auto, avec Remote Control ; approuve le dossier si Claude Code le demande ;
6. communique à la session Mac le nom de la nouvelle session (`ListAgents`), à qui l'ordre est
   envoyé.

## 1. Objet

Valider sur Debian x86_64 l'état publié après ENV-62, ENV-63, ENV-64 et ENV-65 :
- **D26** (ENV-62, PA-111) : règle `Bash(python3 -m unittest discover *)` retirée des réglages
  utilisateur (§0) ; U3 décidé par le classifieur ; une règle utilisateur exacte reste
  appliquée (`userSettings`) ;
- **D28** (ENV-62) : chaque invite à refuser porte sur une cible absente et est annoncée
  « À REFUSER » dans l'`AVANCEMENT` qui précède immédiatement son lancement ;
- **D27** (ENV-62) : comparaisons par `scripts/comparer-releves.py` (traductions de git tirées
  de `po/fr.po` v2.47.3, segment d'hôte) ; 4 traductions ajoutées en ENV-66 ;
- **D21** (ENV-63) : lepton développe `~` et `~<utilisateur>` dans les 6 chemins saisis ;
- **D23, D24** (ENV-64) : extension **0.5.3** (`lepton.path` ; regreffe après disparition d'un
  clone) ;
- **D25, D22** (ENV-65) : scion **0.6.3.3** refuse un clone adopté hors de sa version et une
  graine existante hors de `--version` ; le message d'échec de git garde sa première ligne ;
- regreffe de `$U`, `$E13`, `$C5` et `$R53` : seul le clone noyau avance (dfc960b → **2b4a647** :
  `SCION_REF` 0.6.3.3, hors de `scion/`). Aucun lien ne change ;
- constructions host et 16 presets dans `$R53` regreffé : **aucun binaire changé** depuis R61-1.

**Pas de cartes** dans cette session. Aucune écriture flash.

Références publiées (toutes poussées) :

| Dépôt (`https://github.com/lepton-distribution/…`) | Référence | Commit | En R61-1 |
| --- | --- | --- | --- |
| `lepton-tools` | `devenv/env-66` (cette consigne) | tête après `fetch` | ac3b913 (`devenv/env-61`) |
| `seed.scions` | tag `0.6.3.3` | **9615cd5** (`master` 49ca4ae) | tag `0.6.3.2` 08a1460 |
| `lepton-original-tree.scions` (noyau) | `master` | **2b4a647** | dfc960b |
| graine `lepton-seed.scions`, 12 autres greffons, 8 miroirs | | inchangés | = |

Relevé du Mac : `rapports/env-66-mac/ls-remote-mac.txt` (script `env-66-mac/ls-remote.sh`).

Références Mac (`rapports/env-66-mac.md` §1, `rapports/env-66-mac/attendu/`) :
- liste `chemin -> cible` : `rapports/env-50-mac/attendu/trunk-liens.txt` (3889, inchangée depuis
  R50-1, revérifiée sur `<ROOTSTOCK>` le 2026-11-19) ; clones tiers :
  `rapports/env-53-mac/attendu/clones-rootstock-mac.txt` ;
- C3 : `attendu/c3/` (regreffe d'`essais/env-13-vierge`, même état que `$U` et `$E13`) ;
- C4 : `attendu/c4/` (D21 : `rapports/env-63-tilde/chemins.sh` sur une copie d'`essais/env-11/qemu`
  du Mac ; identique à `env-63-tilde/apres/`, sauf `resume.tsv`, voir §10) ;
- C5 : `attendu/c5/` (D25 : `rapports/env-65-scion/essai.sh`) ; `attendu/fixture65/`,
  `fixture60/`, `fixture56/` (fixtures d'ENV-65, ENV-60, ENV-56, clone de seed.scions au tag
  0.6.3.3 ; identiques aux `*-apres/` d'ENV-65, au nom de la base près) ;
- C6 : `attendu/d23.tsv` (`rapports/env-64-extension/d23.cjs` sur le `lepton.js` de l'extension
  0.5.3 installée ; même sortie sous Node 22 et sous le runtime de VSCodium).

Référence Debian : `rapports/env-61-debian.md` et `oracles/env-61-debian/`.

La session VM ne développe pas : elle exécute, constate et rapporte.

## 2. Ce que la session VM peut faire, et ne fait pas

| Autorisé | Interdit |
| --- | --- |
| `git fetch` / `switch` / `merge --ff-only` de `$T` (`devenv/env-66`) et du clone noyau `$K` (`master`) | Modifier `DEVENV-STATUS.md`, `ORCHESTRATION.md`, `SPECIFICATION.md`, `handoff/*.md`, les consignes, `rapports/env-66-mac*`, `.claude/`, `~/.claude/settings.json` |
| Installations du §6 (`sudo` sans mot de passe sur la VM), dans les formes écrites | Toute autre commande `sudo`, `pip install` hors de `venv-test`, `codium --install-extension` hors `install-vscodium.sh` ; installer Node.js |
| `scion graft-update` de `$U`, `$E13`, `$C5`, `$R53` (§9), dans la forme écrite : l'invite est **confirmée** par l'utilisateur | `graft-update` d'un autre rootstock ; tout `seed-update` ; toute écriture dans les clones de `$U`, `$E13`, `$C5`, `$R53` |
| Lectures dans `$U`, `$E13`, `$C5`, `$R53` ; `lepton check` / `generate` / `seed status` dans ces quatre rootstocks ; `rejouer-oracle.sh` dans `$R53` (`build/` compris, §12) | Écrire un fichier régulier dans un `trunk/` ou sous `depots/tiers/` (le hook refuse) ; corriger quoi que ce soit |
| Créer `$W` (§7), `$SS` et `$FX` (§11.2) et y tout faire, `seed add` / `seed remove` compris | `git config` (même en lecture) et `git sparse-checkout` dans un clone de `depots/tiers/` : relever par `releve-clones.sh` |
| `scion mirror-sync --dry-run` dans `$R53` (§12) | `mirror-sync` sans `--dry-run` ; tout envoi vers un miroir |
| Les contrôles du §8, sur cibles absentes ou protégées | Toute écriture flash, toute commande OpenOCD ; modifier la configuration réseau de la VM |
| Suppressions par `scripts/supprimer-essai.sh` (§11.4 T3, §14) | `rm -rf` direct |
| Créer `devenv/env-66-debian` (depuis `devenv/env-66`) ; y écrire `doc/devenv/rapports/env-66-debian.md`, `doc/devenv/rapports/env-66-debian/` et `doc/devenv/rapports/oracles/env-66-debian/` | Commiter sur une autre branche |
| `git push origin devenv/env-66-debian` **après accord explicite de l'utilisateur** (PA-P ; invite `ask`) | Pousser toute autre branche |

Formes des commandes : **ORCHESTRATION §2bis**, « Commandes soumises aux règles de
`.claude/settings.json` », « Formes » et « Invites à refuser ». Chaque commande de cette consigne
y est écrite dans la forme couverte par sa règle ; la lancer **telle qu'écrite, une par appel**.
Rappel :
- une commande `allow` lancée seule garde sa règle (`2>&1` admis). Les commandes `allow` de cette
  consigne n'ont ni redirection vers un fichier, ni `| tee`, ni `; echo "code=$?"` ; pytest écrit
  son journal par `--junitxml` ;
- une commande `ask` (`scion graft-update`, `git push`) est lancée **directement**, jamais par un
  script, un `bash -c` ou un `eval` ;
- **invites** (D28) : l'`AVANCEMENT` qui précède immédiatement chaque commande à invite dit
  « À REFUSER » (§8, A1 : cible absente) ou « À CONFIRMER » (§9, push), avec la commande exacte.
  Une invite se confirme par « Oui », pour cette commande seule. Une invite non annoncée : la
  refuser, `AVANCEMENT`.

Autres règles :
- **Refus.** Toute commande refusée (classifieur, invite, hook) n'est jamais contournée :
  `AVANCEMENT` avec la commande exacte et la décision ; l'utilisateur la lance s'il le décide, la
  session vérifie l'effet et le consigne. Seuls les refus attendus du §8 (A1, H1) ne demandent
  rien à l'utilisateur, sinon de refuser l'invite A1.
- **Refus d'une invite.** Il interrompt le tour de la session. L'utilisateur relance par un
  message dans la session VM (`reprendre R66-1 au §8, H1`).
- **Régénérer avant de relever** : tout relevé « avant » d'un fichier généré suit immédiatement la
  commande qui le produit (`regreffer-essai.sh avant` le fait).
- **Branche des clones d'un rootstock existant** : relevée au §5 pour `$U`, `$E13`, `$C5`. scion
  refuse lui-même un clone hors de sa version déclarée ; un tel refus reste un écart à exposer.
- **scion, lepton et extension avant C4 à C6** : aucun essai des §10 et §11 avant que
  `scion version` donne 0.6.3.3 et que lepton soit réinstallé (§6) ; aucun essai D23 avant
  l'extension 0.5.3.
- **Comparaisons** (D27) : toujours par `scripts/comparer-releves.py` avec `--home-attendu
  /Users/cle_d_anton --home-obtenu "$HOME"` ; jamais un filtre écrit à la main.

Tout écart au plan, toute erreur non prévue : s'arrêter, exposer (`AVANCEMENT` ou `QUESTION`),
attendre.

## 3. Communication (ORCHESTRATION §2bis)

- Session principale : `validation-debian-env-66` (session Mac ; Claude Code peut la renommer).
  Répondre à l'adresse `from` du message d'ordre.
- ID : `R66-1`, repris tel quel : `[ACCUSÉ R66-1] ENV-66 — …`, `[AVANCEMENT R66-1] …`,
  `[QUESTION R66-1] …`, `[FIN-SUCCÈS R66-1] …` ou `[FIN-ÉCHEC R66-1] …`.
- `ACCUSÉ`, avant toute commande autre que les lectures du §5. Il contient :
  - l'ordre reformulé en une phrase ;
  - le nom de la session VM, son répertoire de travail, la version de Claude Code du journal de
    session (champ `version`) ;
  - la tête réelle de `devenv/env-66` ; les empreintes de `.claude/settings.json` et du hook ;
  - le `diff` du §0 (réglages avant / après) ;
  - les résultats de `git ls-remote` du §5 ;
  - les branches et têtes des clones de `$U`, `$E13` et `$C5` ;
  - les étapes prévues (§6 à §15) et les écarts déjà visibles.
- `AVANCEMENT` : avant chaque commande à invite (§8 A1, §9, push), avant toute action demandée à
  l'utilisateur, à chaque refus non prévu, après chacun des §6 à §12, et à chaque arrêt.
- `FIN-SUCCÈS` / `FIN-ÉCHEC` : résultat par critère du §15, commits et branche (poussée ou non),
  chemin du rapport, versions relevées, écarts, ce qui n'a pas été fait.
- **Remise en échec** (§2bis) : un envoi en erreur (ECONNRESET, « bridge ID is stale ») est renvoyé
  une fois, à l'identique. Si le second envoi échoue, le message entier est consigné dans
  `~/env-66-journaux/0-messages-R66-1.md` et au §Messages du rapport, avec la mention « non remis ».
  La session l'annonce à l'utilisateur, qui le relaie à la session Mac. Un message relayé par
  l'utilisateur et portant l'ID `R66-1` vaut message reçu.

## 4. Journaux et variables

```bash
mkdir -p ~/env-66-journaux
J=~/env-66-journaux
T=~/lepton-tools-dev/lepton-tools
K=~/lepton-tools-dev/lepton-noyau
E=~/lepton-tools-dev/essais
U=$E/env-28-debian
E13=$E/env-13-debian
C5=$E/env-53-c5
R53=$E/env-53-debian
W=$E/env-66-essai
D65=$W/depot65
SS=$W/seed-scions
FX=$E/env-66-fixture
X=doc/devenv/rapports/env-66-mac
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
`~/lepton-tools-dev/essais/env-66-absent` et `https://github.com/lepton-distribution/env-66-absent.git`
n'existent pas et ne doivent jamais être créés : ce sont les cibles absentes du §8. Les commandes
non couvertes par une règle portent leur journal (`> "$J/<étape>.log" 2>&1; echo "code=$?" >> …`).
Les boucles s'écrivent en bash. Ne pas faire `cd` dans un `trunk/` : revenir à `$T` (le hook juge
le répertoire courant).

`cmp_mac <attendu> <obtenu> [<fichier>…]` compare après normalisation (`scripts/comparer-releves.py`,
ENV-62, D27) : messages de git en français ramenés à l'anglais (table `TRADUCTIONS`, tirée de
`po/fr.po` v2.47.3, U+00A0 compris : « fatal : », branche distante, bloc « Could not read from
remote repository », « Cloning into », « unable to access », « not a git repository ») ;
ancêtres de `<HOME>` sous `depots/.mirrors/<hôte>/`. Sortie : une ligne par fichier, puis
`écarts=<n> / <total>` ; code 0 sans écart, 1 sinon.

Outils de la session Mac, en lecture seule, utilisables tels quels sur Debian :
- `env-53-mac/` : `releve-clones.sh`, `inventaire-clones.sh`, `liens.py` ;
- `env-57-mac/regreffer-essai.sh avant|apres <rootstock> <journaux>` : relevés avant et après une
  regreffe, bilan `<journaux>/<nom>-bilan.txt` ; le `graft-update` est lancé à part par la
  session, entre les deux phases ;
- `env-57-mac/decisions.py <journal .jsonl> [--motif <texte>]…` : décisions de permission des
  appels Bash de la session (TSV) ;
- `env-63-tilde/chemins.sh` (D21, 4ᵉ argument : nom de clangd), `env-65-scion/essai.sh` (D25),
  `env-65-scion/fixture.py`, `env-60-scion/fixture.py`, `env-56-scion/fixture.py` (D25, D22),
  `env-64-extension/d23.cjs` (D23) : essais rejoués aux §10, §11 et §11.4.

## 5. Vérifications préalables (lecture seule) — C1

```bash
pwd; printenv CLAUDE_PROJECT_DIR; claude --version 2>&1 | head -1
F=$(ls -t ~/.claude/projects/*lepton-tools-dev-lepton-tools/*.jsonl | head -1); echo "$F"; grep -o '"version":"[^"]*"' "$F" | sort | uniq -c
git -C "$T" status --short | head -5; git -C "$T" branch --show-current; git -C "$T" log --oneline -1
git -C "$T" fetch origin && git -C "$T" status -sb | head -1
sha256sum "$T/.claude/settings.json" "$T/.claude/hooks/proteger-trunk.py" "$T/scripts/supprimer-essai.sh" "$T/scripts/comparer-releves.py"
ls -la ~/.claude/settings.json ~/.claude/settings.local.json "$T/.claude/settings.local.json" 2>&1
cat "$J/0-settings-avant.txt" | head -3; diff "$J/0-settings-avant.txt" "$J/0-settings-apres.txt"
uname -sm; cat /etc/debian_version; uname -r; id -un; git --version
scion version | tail -1; lepton --version; printenv SCION_REF SCION_SPEC
arm-none-eabi-gcc --version | head -1; cmake --version | head -1; ninja --version; qemu-system-arm --version | head -1; python3 --version; codium --version | head -1
command -v shasum realpath tar clangd node rsync; ls -l /usr/share/codium/codium; ls -d ~/tmp-pytest ~/lepton-tools-dev/venv-test/bin/pytest 2>&1
id inconnu63 2>&1 | head -1
df -h ~ /tmp | tail -2
for Z in "$W" "$FX" "$E/env-66-absent"; do test -e "$Z" && echo "ARRÊT : $Z existe déjà"; done
cd "$T" && bash $X/ls-remote.sh > "$J/5-ls-remote.txt" 2>&1; diff <(grep -v '^lepton-tools ' $X/ls-remote-mac.txt) <(grep -v '^lepton-tools ' "$J/5-ls-remote.txt") && echo "têtes publiées = Mac"
for Z in "$U" "$E13" "$C5"; do
  echo "== $Z"
  git -C "$Z"/depots/lepton-seed*/* log --oneline -1
  grep -v '^#' "$Z"/trunk/.scion.grafted.list | grep -c .
  bash "$T/$IC" "$Z" | tee "$J/5-clones-$(basename $Z).txt"
  python3 -I "$T/$LI" "$Z/trunk" > /dev/null
  ls -d "$Z"/depots/tiers/*/* 2>&1; du -sk "$Z"/depots/tiers 2>&1
done
ls -d "$R53" ~/env-61-journaux ~/tmp-pytest/env-61 2>&1; ls -d "$E"/*/ 2>&1
```
Attendu :
- répertoire de travail `$T` (`/home/lepton-user/lepton-tools-dev/lepton-tools`) ; lepton-tools
  propre, sur `devenv/env-66`, à jour avec `origin/devenv/env-66` (préalable du §0) ; session
  **ouverte après le §0** (sa première entrée de journal est postérieure à `0-settings-apres.txt`) ;
- `.claude/settings.json` `b01ad557…d235`, `proteger-trunk.py` `04572df6…6909`,
  `supprimer-essai.sh` `04323a00…0e15` (tous trois inchangés depuis R61-1), `comparer-releves.py`
  `2bd102cd…5d8c` (Mac, ENV-66) ;
- `diff` du §0 : seule l'entrée `unittest` retirée ;
- `têtes publiées = Mac` ; git **2.47.3** ; scion **0.6.3.2** (avant installation) ; `lepton 0.1.0`,
  `scion 0.6.3.2 (requis ≥ 0.6.2.0)` ; `SCION_REF` et `SCION_SPEC` vides ;
- chaîne APT de R61-1 : arm-none-eabi-gcc 14.2.1, cmake 3.31.6, ninja 1.12.1, QEMU 10.0.13,
  Python 3.13.5, codium 1.135.06055 ; `shasum`, `realpath`, `tar`, `clangd` présents ; `node`
  absent (relevé) ; `rsync` relevé ; `/usr/share/codium/codium` présent ; `~/tmp-pytest` et
  `venv-test/bin/pytest` présents ; `id inconnu63` : utilisateur inconnu (sinon l'essai D21
  s'arrête) ;
- `$U` et `$E13` (état laissé par R61-1), chacun : graine 15740f9 ; **23 entrées** ; 14 lignes
  d'inventaire, la graine sur `original-tree`, 13 clones `<clé>/master` sur `master`, amont réglé,
  `modifs=0`, noyau **dfc960b** ; `liens=3889 casses=0 reguliers=0` ; 8 clones tiers ;
- `$C5` : graine `env11` ; `liens=3059 casses=0 reguliers=0` ; noyau dfc960b ; `salut` sans amont,
  `modifs=2` (état d'origine de la VM) ; clones F7 conservés de R53-1 ;
- `$R53`, `~/env-61-journaux` et `~/tmp-pytest/env-61` présents.

Arrêts :
- un chemin du `for` initial existe ;
- lepton-tools non propre, hors de `devenv/env-66`, ou `settings.json` ou hook différent du Mac ;
- session ouverte avant le §0, ou `diff` du §0 autre que l'entrée retirée ;
- un commit publié diffère du Mac ;
- graine de `$U`, `$E13` ou `$C5` modifiée ; un clone de greffon publié hors de sa branche, sans
  amont ou modifié ;
- `shasum`, `realpath`, `tar` ou `clangd` absent ; moins de 8 Go libres dans `~`.

Pas des arrêts, à consigner : une version de la chaîne ou de Claude Code différente de R61-1.

## 6. Installation de scion 0.6.3.3, de lepton et de l'extension 0.5.3 (C1)

D'abord, par la session :
```bash
git -C "$K" status --short | head -5
git -C "$K" fetch origin && git -C "$K" switch master && git -C "$K" merge --ff-only origin/master && git -C "$K" log --oneline -1
grep -n '^SCION_REF=' "$K/scripts/install-debian.sh" "$T/scripts/install-vscodium.sh"
grep -n 'SCION_MIN_VERSION =' "$T/lepton/__init__.py"; grep -n '"version"' "$T/extension/package.json"; ls "$T"/extension/dist/
```
Attendu : clone noyau propre, à **2b4a647** (dfc960b avant) ; `SCION_REF="${SCION_REF:-0.6.3.3}"`
(noyau) et `SCION_REF="0.6.3.3"` (lepton-tools) ; `SCION_MIN_VERSION = (0, 6, 2, 0)` ;
extension `0.5.3`, `lepton-0.5.3.vsix` seul dans `dist/`.

Puis `AVANCEMENT`, et la session lance, une commande par appel, dans cet ordre :
1. scion (hors règle : classifieur ; accepté en R61-1) :
   ```bash
   bash ~/lepton-tools-dev/lepton-noyau/scripts/install-debian.sh --with-debug-tools > ~/env-66-journaux/6-install-debian.log 2>&1; echo "code=$?" >> ~/env-66-journaux/6-install-debian.log
   ```
   Il installe scion par `pipx install --force
   "git+https://github.com/lepton-distribution/seed.scions.git@0.6.3.3"` (défaut `SCION_REF`). En
   cas de refus : `AVANCEMENT` ; l'utilisateur lance la même ligne dans la session VM (`!` en
   premier caractère) ou dans un terminal.
2. lepton (règle `allow` du dépôt, forme exacte, sans redirection) :
   ```bash
   pipx install --force ~/lepton-tools-dev/lepton-tools
   ```
   Sortie lue dans le résultat de l'outil et reportée au rapport. Elle installe le lepton
   d'ENV-63 (D21).
3. VSCodium et extension (hors règle) :
   ```bash
   bash ~/lepton-tools-dev/lepton-tools/scripts/install-vscodium.sh --lepton-clone ~/lepton-tools-dev/lepton-noyau > ~/env-66-journaux/6-install-vscodium.log 2>&1; echo "code=$?" >> ~/env-66-journaux/6-install-vscodium.log
   ```

Puis :
```bash
tail -3 "$J/6-install-debian.log"; grep -n -i 'scion' "$J/6-install-debian.log" | tail -5; tail -12 "$J/6-install-vscodium.log"
scion version | tail -1; lepton --version; codium --version | head -1
pipx list --short | grep -E '^(scion|lepton) '
PYL=$(dirname "$(realpath "$(command -v lepton)")")/python; echo "$PYL"
RP=$("$PYL" -I -c 'import lepton.rootstock as r; print(r.__file__)'); echo "$RP"
cmp "$T/lepton/rootstock.py" "$RP" && echo "rootstock.py installé = dépôt"
"$PYL" -I -c 'import lepton.rootstock as r; print(callable(getattr(r, "expand_user", None)))'
PYS=$(dirname "$(realpath "$(command -v scion)")")/python; "$PYS" -I -c 'import scion; print(scion.__version__)'
codium --list-extensions --show-versions | LC_ALL=C sort > "$J/6-extensions.txt"; grep -E -i 'lldb|lepton|rtos-views|peripheral' "$J/6-extensions.txt"
ls ~/.vscode-oss/extensions/ | grep -i lepton
```
Attendu : codes 0 ; `scion version: 0.6.3.3` ; `lepton 0.1.0`, `scion 0.6.3.3 (requis ≥ 0.6.2.0)` ;
`rootstock.py installé = dépôt` et `True` (correction D21 installée, `expand_user`, contrôle
vérifié contre le code du Mac, D27) ; `0.6.3.3` ; `install-vscodium.sh` : ligne
`lepton-distribution.lepton : 0.5.2 → 0.5.3`, `changements 1` ; `lepton-distribution.lepton@0.5.3`,
`vadimcn.vscode-lldb@1.12.3`, `mcu-debug.rtos-views@0.0.16`, `mcu-debug.peripheral-viewer@1.6.4` ;
répertoire `lepton-distribution.lepton-0.5.3`.

**Arrêt** si scion n'est pas 0.6.3.3, si la correction D21 n'est pas installée ou si l'extension
n'est pas 0.5.3 : ni §9, ni §10, ni §11.

## 7. Copies d'essai et dépôt présent (pour C2, C4, C5)

Avant toute regreffe de `$C5` (§9), pour que les copies partent de l'état de celle du Mac (noyau
dfc960b, 3059 liens) :
```bash
cd "$T"
mkdir -p "$W/c4/rs" "$W/c4/gen" "$W/c5/rs" "$W/d23cwd"
for d in c4/rs c4/gen c5/rs; do tar -C "$C5" --exclude=./build -cf - . | tar -C "$W/$d" -xf -; echo "$d copie=$?"; done
python3 -I "$T/$LI" "$W/c4/rs/trunk"; python3 -I "$T/$LI" "$W/c5/rs/trunk" > "$J/7-liens-depart-c5.txt"
lepton check -C "$W/c4/rs" > "$J/7-check.log" 2>&1; echo "code=$?" >> "$J/7-check.log"; tail -2 "$J/7-check.log"
lepton scion new env65lib --type bibliotheque --repo "$D65" --no-seed --no-cmake -C "$W/c4/gen" > "$J/7-scion-new-65.log" 2>&1; echo "code=$?" >> "$J/7-scion-new-65.log"; cat "$J/7-scion-new-65.log"
git -C "$D65" switch -q -c dev && echo dev > "$D65/scion/sys/root/src/lib/env65lib/DEV.txt" && git -C "$D65" add -A && git -C "$D65" commit -qm "dev : DEV.txt" && git -C "$D65" switch -q master; echo "dev=$?"
git -C "$D65" log --oneline --all; git -C "$D65" ls-tree -r --name-only dev
git -C "$W/c4/gen"/depots/lepton-seed/env11 status --short | wc -l
```
Attendu : 3 `copie=0` ; `liens=3059 casses=0 reguliers=0` (deux fois) ; `check` code 0 ;
`dépôt créé : …/depot65 (lib/env65lib)`, code 0 ; `dev=0` ; 2 commits (`master`, `dev`) ; `dev`
porte `DEV.txt`, `env65lib.c`, `env65lib.h`, `lepton-greffon.json` sous
`scion/sys/root/src/lib/env65lib/` ; graine de `c4/gen` sans modification (0). Les copies ne sont
pas régénérées par `lepton generate` (celles du Mac ne l'ont pas été). `c4/gen` tient lieu de la
copie que `chemins.sh` fait par `rsync` (l. 34) quand elle manque.

## 8. Règles de permission sur la VM (C2 : D26, D28, hook)

Toutes les commandes de ce paragraphe sont lancées par la session, **une par appel, telles
qu'écrites** (chemins `~/…` littéraux). La décision de chacune est relevée à la fin dans le
journal de session.

### 8.1 D26 : réglages utilisateur

```bash
python3 -m json.tool ~/.claude/settings.json
```
Attendu : le fichier entier, reporté au rapport, identique à `$J/0-settings-apres.txt`. Le bloc
`permissions.allow` est exactement celui du §0 (2 règles) ; ni `ask`, ni `deny`, ni
`defaultMode` dans `permissions`. Les autres clés (`autoMode`, `modelSettings`…) sont celles de
R61-1 (`rapports/env-61-debian/settings-utilisateur.json`). Un bloc différent : `QUESTION`.

| N° | Commande | Attendu |
| --- | --- | --- |
| U1 | `pipx install ~/lepton-tools-dev/essais/env-66-absent` | règle utilisateur `Bash(pipx install:*)` (`userSettings`, forme de T6 d'ENV-62) ; code ≠ 0, rien d'installé |
| U2 | `git clone --depth 1 https://github.com/lepton-distribution/env-66-absent.git ~/lepton-tools-dev/essais/env-66-absent` | règle utilisateur `Bash(git clone * https://github.com/lepton-distribution/*)` ; code ≠ 0 (dépôt inexistant), cible absente |
| U3 | `python3 -m unittest discover -s ~/lepton-tools-dev/essais/env-66-absent` | **classifieur** (règle retirée ; PA-111) ; s'il l'accepte : code ≠ 0, aucun test ; s'il la refuse : refus attendu, rien à demander |

### 8.2 D28 : invite à refuser ; hook

| N° | Commande | Attendu |
| --- | --- | --- |
| A1 | `scion graft-update -v ~/lepton-tools-dev/essais/env-66-absent` | règle `ask` : invite ; **l'utilisateur la refuse** |
| H1 | `touch ~/lepton-tools-dev/essais/env-66-essai/c5/rs/trunk/essai-hook` | hook : refus sans invite |

Avant A1 : `AVANCEMENT` « **À REFUSER** : `scion graft-update -v ~/lepton-tools-dev/essais/env-66-absent`
(cible absente) ; après le refus, relancer par « reprendre R66-1 au §8, H1 » ». Aucun autre
message entre cet `AVANCEMENT` et le lancement.

Après H1 :
```bash
cd "$T"
ls -d ~/lepton-tools-dev/essais/env-66-absent "$W/c5/rs/trunk/essai-hook" 2>&1; pipx list --short | grep -c env-66
python3 -I "$T/$LI" "$W/c5/rs/trunk" | cmp - "$J/7-liens-depart-c5.txt" && echo "liens de c5 = départ"
F=$(ls -t ~/.claude/projects/*lepton-tools-dev-lepton-tools/*.jsonl | head -1); echo "$F"
python3 -I "$T/$DEC" "$F" > "$J/8-decisions.tsv"; cut -c1-180 "$J/8-decisions.tsv" | grep -E 'pipx install|git clone|unittest|graft-update|touch'
```
Attendu, dans `8-decisions.tsv` :
- §6.2 `pipx install --force ~/lepton-tools-dev/lepton-tools` : `accept config rule projectSettings`
  (ou `subcommandResults`) ;
- U1, U2 : `accept config rule userSettings` (ou `subcommandResults` avec la règle utilisateur) ;
- U3 : `classifier` (accepté ou refusé) ;
- A1 : `rejet-invite` ; H1 : `reject hook hook` ;
- cible absente, `essai-hook` absent, aucun paquet `env-66` ; liens de c5 = départ.

Écarts, sans arrêt sauf mention :
- U1 ou U2 au classifieur : réglages utilisateur non lus (session ouverte avant le §0 ?), à
  relever ;
- U3 par une règle (`userSettings`) : la règle n'a pas été retirée, à relever ;
- une invite non apparue pour A1 : **arrêt**, `QUESTION` (la commande serait exécutée sans
  accord ; elle reste sans effet, la cible étant absente).

## 9. Regreffe de `$U`, `$E13`, `$C5` (C3) et `$R53` (pour C7)

Pour chaque rootstock de la liste `env-28-debian`, `env-13-debian`, `env-53-c5`,
`env-53-debian`, dans cet ordre (`$C5` après les copies du §7) :
1. par la session, depuis `$T` :
   ```bash
   bash "$T/$RG" avant ~/lepton-tools-dev/essais/<nom> "$J/regreffes"
   ```
2. `AVANCEMENT` « **À CONFIRMER** : `scion graft-update -v ~/lepton-tools-dev/essais/<nom>` »,
   puis la session lance, telle quelle :
   ```bash
   scion graft-update -v ~/lepton-tools-dev/essais/<nom> > ~/env-66-journaux/regreffes/<nom>-graft-update.log 2>&1; echo "code=$?" >> ~/env-66-journaux/regreffes/<nom>-graft-update.log
   ```
   L'utilisateur confirme l'invite par « Oui » (PA-P accordé au PA-119 pour ces quatre
   rootstocks).
3. par la session :
   ```bash
   cd "$T"
   bash "$T/$RG" apres ~/lepton-tools-dev/essais/<nom> "$J/regreffes"
   Z=~/lepton-tools-dev/essais/<nom>; L=$J/regreffes/<nom>-graft-update.log
   resume() { sed -e "s|$Z|<R>|g" -e "s|$HOME|<HOME>|g" "$1" | grep -v -E '^git |\(cwd=|^  |\.DS_Store|chemin\(s\) ignoré\(s\)|^code='; }
   grep -E 'feuilles liées|ignoré' "$L"
   ```
   et, pour `$U`, `$E13` et `$R53` (rootstocks de la graine `original-tree`) :
   ```bash
   mkdir -p "$J/9-resume-<nom>"; resume "$L" > "$J/9-resume-<nom>/graft-update-resume.txt"
   cmp_mac "$T/$A/c3" "$J/9-resume-<nom>" graft-update-resume.txt
   python3 -I "$T/$C" "$Z" "$T/$A50/trunk-liens.txt" "$J/9-<nom>-controle" > "$J/9-<nom>-controle.log" 2>&1; echo "code=$?" >> "$J/9-<nom>-controle.log"; tail -3 "$J/9-<nom>-controle.log"
   normc() { sed -E 's/ ignorecase=[^ ]*//; s/ ko_hors_git=.*//' "$1"; }
   diff <(normc "$T/$Y/attendu/clones-rootstock-mac.txt") <(normc "$J/regreffes/<nom>-tiers-apres/clones.txt") && echo "clones = Mac (hors ignorecase et tailles)"
   ```

Attendu, `$U`, `$E13` et `$R53` (Mac, `essais/env-13-vierge`, `attendu/c3/env-13-vierge-bilan.txt`) :
- `graft-update code=0 ; avancés : 1 ; git clone : 0 ; extraction partielle : 0 ; conflit/refus : 0` ;
  `depots/lepton/original/master avancé : dfc960b -> 2b4a647` ; « 3889 feuilles liées » ; aucune
  ligne `.DS_Store` sur la VM ;
- `graft-update-resume.txt identique`, `écarts=0 / 1` : 83 lignes (avancée du noyau, projections,
  « répertoire extrait » des 8 clones tiers, déjà partiels), dont une ligne nouvelle sous 0.6.3.3 :
  `fatal: not a git repository (or any of the parent directories): .git`, stderr de git écrit par
  `-v` pour la source non git `generation/building` (D22). Sur la VM, elle est en français
  (« ni ceci ni aucun de ses répertoires parents n'est un dépôt git », `po/fr.po` l. 21978) et
  `cmp_mac` la ramène ;
- `clones : 1 ligne(s) changée(s)` (noyau) ; liens 3889 → 3889, ajoutés 0, retirés 0 ;
  `controler-trunk CONFORME code=0` contre les liens d'avant **et** contre l'attendu de R50-1 ;
- `tiers : 8 clone(s)`, extraits et `sparse-checkout` ≠ attendu : **0 / 16** ; `clones = Mac` ;
- `check code=0`, `generate` avant et après code 0, `espace diff=0` ; trunk sans fichier régulier ni
  lien cassé.

Attendu, `$C5` : un seul clone avancé (noyau dfc960b → 2b4a647) ; `salut` accepté (sans amont,
`modifs=2`, comme en R61-1) ; 3059 liens inchangés, `CONFORME` contre les liens d'avant ; les 2
clones tiers F7 conservés de R53-1 ne sont pas greffés, inchangés (0 / 4) ; `check` code 0 ; espace
identique.

Un refus de scion (clone hors version, graine divergée) : écart à exposer, sans contournement.

## 10. D21 : `~` dans les chemins saisis (C4)

Sur `$W/c4` (§7), avec lepton réinstallé (§6) :
```bash
cd "$T"
bash doc/devenv/rapports/env-63-tilde/chemins.sh ~/lepton-tools-dev/essais/env-66-essai/c4 apres "$J/10-c4" clangd > "$J/10-c4.log" 2>&1; echo "code=$?" >> "$J/10-c4.log"
tail -1 "$J/10-c4.log"; grep -c . "$J/10-c4/resume.tsv"; ls "$J/10-c4" | wc -l; ls "$T/$A/c4" | wc -l
cmp_mac "$T/$A/c4" "$J/10-c4" > "$J/10-c4-cmp.txt"; echo "code=$?"; grep -v 'identique$' "$J/10-c4-cmp.txt" | head -40
diff <(cut -f1-7 "$T/$A/c4/resume.tsv") <(cut -f1-7 "$J/10-c4/resume.tsv") && echo "resume.tsv colonnes 1-7 = Mac"
for f in "$T/$A"/c4/*.W; do b=${f##*/}; diff <(grep -v '^\./\.DS_Store$' "$f") "$J/10-c4/$b" > /dev/null || echo "W diffère hors .DS_Store : $b"; done
diff "$T/$A/c4/p5-a.W" "$J/10-c4/p5-a.W"
python3 -I "$T/$LI" "$W/c4/rs/trunk"
```
Attendu (Mac, `attendu/c4/`, `rapports/env-66-mac.md` §1.4) :
- `code=0` ; 289 relevés de chaque côté ; 47 cas (48 lignes de `resume.tsv`) ;
- `cmp_mac` : écarts admis, et eux seuls :
  - `p6-n.cmd`, `p6-n.clangd` : nom et chemin de clangd (`clangd`, `/usr/bin/clangd` contre
    `clangd-mp-21`, `/opt/local/bin/clangd-mp-21`) ;
  - `resume.tsv` : la colonne 8 (message) est tronquée à 160 octets avant normalisation, sa fin
    dépend de la longueur des chemins de l'hôte ; colonnes 1 à 7 = Mac ;
  - les 19 `*.W` des cas lancés dans `<C>` ou `<G>` (`m1-t`, `p5-*`, `p5add-*`, `p5dir-*`,
    `p5graft-t`, `p6-*` sauf `p6-x`) : ils listent la racine du rootstock copié. Celle du Mac porte
    `./.DS_Store` (Finder) ; hors de cette ligne, les fichiers de la racine de `$C5` peuvent
    différer (relevés par le `diff` de `p5-a.W`, informatif) ;
  au Mac, la forme exacte de ce paragraphe (copies `tar`, `c4/gen` vierge, 4ᵉ argument) ne donne
  que l'écart de `resume.tsv` (`rapports/env-66-mac.md` §1.4) ;
- les 7 formes par chemin du PA-113 : `~/…` et `~<U>/…` développés (`cwd/~*` : `non` partout) ;
  `~inconnu63/…` refusé par lepton (« répertoire personnel de « ~inconnu63 » introuvable ») ;
  `C` = départ après chaque cas ;
- liens de `c4/rs` : `liens=3059 casses=0 reguliers=0`.

Tout autre écart : relever le fichier et le `diff`, sans correction.

## 11. D25 et D22 : clone existant hors version, message de git ; pytest (C5)

### 11.1 Cas de lepton d'ENV-65

```bash
cd "$T"
bash doc/devenv/rapports/env-65-scion/essai.sh ~/lepton-tools-dev/essais/env-66-essai/c5/rs ~/lepton-tools-dev/essais/env-66-essai/depot65 "$J/11-c5-brut" "$J/11-c5" > "$J/11-c5.log" 2>&1; echo "code=$?" >> "$J/11-c5.log"
cat "$J/11-c5.log"; cat "$J/11-c5/scion.txt"
cmp_mac "$T/$A/c5" "$J/11-c5"; echo "code=$?"
ls -d "$W/c5/rs"/depots/lepton/library-env65lib/*/ 2>&1
python3 -I "$T/$LI" "$W/c5/rs/trunk" | cmp - "$J/7-liens-depart-c5.txt" && echo "liens de c5 = départ"
```
Attendu (Mac, `attendu/c5/`, `rapports/env-65-scion.md` §6) :
- l01 et l02 (`seed add env65lib <P>@dev` sur un clone préexistant resté sur `master`) : **code 2** ;
  scion refuse « 1 clone(s) existant(s) hors de leur version déclarée, non repris (liste greffée et
  clones inchangés) : … », lepton annule (« graine et trunk restaurés ») ; liens, graine, liste
  greffée = départ ; clone laissé sur `master` ;
- l03 (clone remis sur `dev`) : `seed add` 0 (4 liens, `DEV.txt` compris), `check` 0,
  `seed remove --purge` 0 ; tout égal au départ ensuite ;
- `cmp_mac` sur 28 relevés : écarts admis, et eux seuls :
  - `depart.etat` : empreinte de la graine du rootstock copié (`env11` de `$C5`, et non celle
    d'`essais/env-11/qemu` du Mac) ;
  - `l03.etat` : empreintes des fichiers de la graine avant et après `seed add` (même cause, et
    `.scion.sources.list` porte l'URL de `depot65`, propre à l'hôte) ; ses autres lignes (liens,
    liste greffée, `depots`, branche `dev`, `DEV.txt`) = Mac ;
  - `scion.txt` : `<HOME>/.local/bin/scion`, `0.6.3.3` (= Mac) ;
- liens de c5 = départ.

### 11.2 Fixtures d'ENV-65, d'ENV-60 et d'ENV-56

Les fixtures importent les aides de test de seed.scions : il leur faut un clone au tag. Par la
session, une commande par appel :
```bash
git clone https://github.com/lepton-distribution/seed.scions.git ~/lepton-tools-dev/essais/env-66-essai/seed-scions
```
(règle `allow` du dépôt, forme exacte, sans redirection), puis :
```bash
git -C ~/lepton-tools-dev/essais/env-66-essai/seed-scions switch --detach 0.6.3.3
git -C "$SS" log --oneline -1; git -C "$SS" status --short | wc -l
cd "$T"
python3 -I doc/devenv/rapports/env-65-scion/fixture.py "$SS" "$(command -v scion)" "$FX/f65" "$J/11-fixture65" > "$J/11-fixture65.log" 2>&1; echo "code=$?" >> "$J/11-fixture65.log"; tail -3 "$J/11-fixture65.log"
python3 -I doc/devenv/rapports/env-60-scion/fixture.py "$SS" "$(command -v scion)" "$FX/f60" "$J/11-fixture60" > "$J/11-fixture60.log" 2>&1; echo "code=$?" >> "$J/11-fixture60.log"; tail -3 "$J/11-fixture60.log"
python3 -I doc/devenv/rapports/env-56-scion/fixture.py "$SS" "$(command -v scion)" "$FX/f56" "$J/11-fixture56" > "$J/11-fixture56.log" 2>&1; echo "code=$?" >> "$J/11-fixture56.log"; tail -3 "$J/11-fixture56.log"
for f in 65 60 56; do cmp_mac "$T/$A/fixture$f" "$J/11-fixture$f" > "$J/11-fixture$f-cmp.txt"; echo "fixture$f code=$? $(tail -1 "$J/11-fixture$f-cmp.txt")"; grep -v 'identique$' "$J/11-fixture$f-cmp.txt" | head -30; done
for c in n01 n03 n04 n05 n06b n07b; do echo "== $c"; cat "$J/11-fixture65/$c.err"; done
```
Attendu (Mac, identiques aux `*-apres/` d'ENV-65) : `9615cd5`, propre ; trois `code=0` ;
**écarts=0** pour les trois fixtures (`fixture65`, `fixture60`, `fixture56`, `--home-*` compris :
la base `essais/env-66-fixture` est la même des deux côtés). Les `.err` de la VM portent la
première ligne de git (D22) en français ; `cmp_mac` les ramène. Points à relever au rapport,
octet pour octet (`cat -v`) :
- n01, n05 : `fatal⍽: '<B>/repos/absent' does not appear to be a git repository`. Ce texte est
  absent de `po/fr.po` : il est attendu en anglais derrière `fatal⍽: ` (déduction d'ENV-65,
  **à vérifier ici**) ;
- n03 : la branche distante (`La branche distante nope n'a pas été trouvée…`) ;
- n04 (réseau : `scion-essai.invalid` ne se résout pas) : `impossible d'accéder à '…'⍽: Could not
  resolve host: scion-essai.invalid` ;
- `*.git-err` (stderr complet) : `Clonage dans 'd'...` et le bloc « Impossible de lire le dépôt
  distant. … et que le dépôt existe. ».

Un écart restant après `cmp_mac` : relever le fichier et le `diff` ; si c'est une traduction de
git absente de la table, citer la ligne de `po/fr.po` v2.47.3 qui la donne (pas de correction de
l'outil sur la VM). Le classifieur décide de `switch` et des fixtures (relevé).

### 11.3 pytest de lepton-tools

Par la session, règle `allow`, forme exacte (sans redirection, sans `TMPDIR=` ; le journal est
écrit par `--junitxml`) :
```bash
~/lepton-tools-dev/venv-test/bin/pytest -q -rs -p no:cacheprovider --basetemp ~/tmp-pytest/env-66 --junitxml ~/env-66-journaux/11-pytest.xml
```
Puis :
```bash
cd "$T"
python3 -I -c 'import sys,xml.etree.ElementTree as E; s=E.parse(sys.argv[1]).getroot().find("testsuite"); print({k:s.get(k) for k in ("tests","failures","errors","skipped","time")})' "$J/11-pytest.xml"
for m in test_proteger_trunk test_garde_ask test_supprimer_essai test_milestone3 test_comparer_releves; do echo "$m $(grep -o "classname=\"tests.$m\"" "$J/11-pytest.xml" | wc -l)"; done
~/lepton-tools-dev/venv-test/bin/python -m pip show lepton | grep -i -E '^(version|location|editable)'
git -C "$T" status --short | head -5
```
Attendu (Mac, 2026-11-19, Python 3.11.5, scion 0.6.3.3) : **570 passed**, 0 échec, 0
erreur  ; `test_proteger_trunk` 118, `test_garde_ask` 46, `test_supprimer_essai` 52, `test_milestone3` 53, `test_comparer_releves` 13 (8 min 41) ; lepton en mode éditable depuis `$T` ; lepton-tools propre (hors
rapport). Un test ignoré ou en échec : relever son nom et son message, le relancer seul une fois
(`~/lepton-tools-dev/venv-test/bin/pytest -q -rs -p no:cacheprovider --basetemp
~/tmp-pytest/env-66 <test>`), consigner les deux résultats ; pas de correction.

### 11.4 D23 et D24 : extension 0.5.3 (C6)

D23, hors de l'éditeur, par le runtime Node de VSCodium (Node.js est absent de la VM et n'y est
pas installé ; au Mac, `ELECTRON_RUN_AS_NODE=1` donne une sortie identique à celle de Node 22) :
```bash
cd "$T"
ELECTRON_RUN_AS_NODE=1 /usr/share/codium/codium -e 'console.log(process.versions.node, process.versions.electron)'
mkdir -p "$J/11-d23"; ELECTRON_RUN_AS_NODE=1 /usr/share/codium/codium doc/devenv/rapports/env-64-extension/d23.cjs ~/.vscode-oss/extensions/lepton-distribution.lepton-0.5.3/out/src/lepton.js ~/lepton-tools-dev/essais/env-66-essai/d23cwd > "$J/11-d23/d23.tsv" 2> "$J/11-d23/d23.err"; echo "code=$?"; cat "$J/11-d23/d23.err"
cmp_mac "$T/$A" "$J/11-d23" d23.tsv
```
Attendu : versions de Node et d'Electron relevées ; `code=0` ; `d23.tsv identique`,
`écarts=0 / 1` : `~/…`, `~<U>/…` et `${userHome}/…` lancent lepton (code 0) ; `~inconnu64/…` et
`$HOME/…` : `lepton not found` ; `~` seul : `spawn <HOME> EACCES`. Si le runtime refuse
`ELECTRON_RUN_AS_NODE` (fusible désactivé) : relever le message, D23 reste prouvé au Mac seulement
(écart, sans arrêt).

D24 (PA-119, option (a)) : dans VSCodium sur la VM, par l'utilisateur, sur `$W/c4/gen`, avec le
greffon `env65lib` de `$D65`. Forme réduite de `rapports/env-64-extension.md` §5.3 : U4
(`seed remove --purge` par l'extension) et T3 (clone supprimé à la main). Défaut corrigé par 0.5.3 :
la disparition d'un clone entier faisait regreffer la racine `<clone>/scion`, que lepton refuse,
d'où un avertissement d'échec de regreffe. Sous Linux, l'observateur de fichiers est inotify (au
Mac, FSEvents) : c'est la seule preuve sur cette plateforme.

1. Préparation, par la session :
   ```bash
   cd "$T"
   lepton seed add env65lib "file://localhost$D65@dev" --type bibliotheque --no-cmake -C "$W/c4/gen" > "$J/11-d24-add1.log" 2>&1; echo "code=$?" >> "$J/11-d24-add1.log"; tail -3 "$J/11-d24-add1.log"
   python3 -I "$T/$LI" "$W/c4/gen/trunk"; ls "$W/c4/gen"/*.code-workspace
   ```
   Attendu : code 0 ; `liens=3063 casses=0 reguliers=0` (3059 + 4 de `env65lib@dev`) ; un espace
   de travail `env11.code-workspace`.
2. `AVANCEMENT` à l'utilisateur, **U4** :
   - ouvrir `codium ~/lepton-tools-dev/essais/env-66-essai/c4/gen/env11.code-workspace` et attendre
     la vue Lepton ;
   - palette : « Lepton : retirer un greffon de la graine », choisir `env65lib`, puis « supprimer
     aussi le clone (--purge) », puis confirmer ;
   - relever **toutes** les notifications affichées, mot pour mot, puis répondre « reprendre R66-1
     au §11.4, T3 ».
   La session relève ensuite :
   ```bash
   cd "$T"; python3 -I "$T/$LI" "$W/c4/gen/trunk"; ls -d "$W/c4/gen"/depots/lepton/library-env65lib 2>&1
   ```
   Attendu : une seule notification, « lepton : retirer env65lib — terminé » (aucun avertissement
   de regreffe) ; `liens=3059 casses=0 reguliers=0` ; clone absent.
3. **T3**, VSCodium restant ouvert sur le même espace : la session regreffe le greffon puis
   supprime son clone à la main :
   ```bash
   cd "$T"
   lepton seed add env65lib "file://localhost$D65@dev" --type bibliotheque --no-cmake -C "$W/c4/gen" > "$J/11-d24-add2.log" 2>&1; echo "code=$?" >> "$J/11-d24-add2.log"; tail -1 "$J/11-d24-add2.log"
   ```
   puis, règle `allow`, forme exacte :
   ```bash
   scripts/supprimer-essai.sh ~/lepton-tools-dev/essais/env-66-essai/c4/gen/depots/lepton/library-env65lib/dev
   ```
   puis `AVANCEMENT` à l'utilisateur : relever les notifications parues (attendre 5 s), puis
   répondre « reprendre R66-1 au §11.4, fin ». La session relève :
   ```bash
   cd "$T"; python3 -I "$T/$LI" "$W/c4/gen/trunk"
   ```
   Attendu : une seule notification, « Clone de library-env65lib supprimé hors de lepton : ses
   liens du trunk sont cassés (lepton seed status) » ; aucun avertissement d'échec de regreffe ;
   `liens=3063 casses=4`. `$W/c4/gen` n'est pas rétabli : il est supprimé au §14.
4. L'utilisateur ferme VSCodium.

Une notification d'échec de regreffe (`graft --path …/scion`), ou l'absence de la notification
de T3 : écart à exposer, avec le texte relevé.

## 12. Reconstructions et commande de miroir (C7)

PA-119 : reconstruction et miroir à blanc maintenus, bien qu'aucune source compilée ne change depuis R61-1.

### 12.1 Reconstructions

Périmètre : host et les 16 presets croisés (QEMU : construction, fumée, banc KAL ; cartes :
construction et capture seulement, **aucun flash**), dans `$R53` regreffé au §9. `$R53` garde le
chemin d'`env-53-debian` : les chaînes `__FILE__` des presets FreeRTOS sont celles de l'oracle de
référence. Commande longue (≈ 4 min en R61-1) : `AVANCEMENT` au lancement.

```bash
cd "$T" && git switch -c devenv/env-66-debian devenv/env-66
scripts/oracle/rejouer-oracle.sh ~/lepton-tools-dev/essais/env-53-debian doc/devenv/rapports/oracles/env-66-debian --qemu qemu-mps2-an386-embos --qemu qemu-mps2-an386-embos-soft --qemu qemu-mps2-an386-freertos --qemu qemu-mps2-an386-freertos-soft --qemu qemu-mps2-an500-embos --qemu qemu-mps2-an500-freertos --carte nucleo-f429zi-embos --carte nucleo-f429zi-freertos --carte nucleo-f439zi-embos --carte nucleo-f439zi-freertos --carte nucleo-wl55jc1-embos --carte nucleo-wl55jc1-freertos --carte samd21-xplained-pro-embos --carte samd21-xplained-pro-freertos --carte stm32f746g-disco-embos --carte stm32f746g-disco-freertos > ~/env-66-journaux/12-rejouer.log 2>&1; echo "code=$?" >> ~/env-66-journaux/12-rejouer.log
```
Puis :
```bash
cd "$T"; O=doc/devenv/rapports/oracles
tail -25 "$J/12-rejouer.log"
grep -h "tests passed" $O/env-66-debian/*/ctest.log $O/env-66-debian/*/banc-kal.log
grep -h "peripheriques" $O/env-66-debian/qemu-mps2-an386-*/banc-kal.log
python3 -I "$T/$LI" "$R53/trunk" > /dev/null; find "$R53/trunk" -name __pycache__ | wc -l
```
Attendu : code 0 ; host ctest 7/7 ; 16 presets construits ; fumée réussie ; banc QEMU identique à
R61-1 : an386 20/20, an386 soft 16/16, an500 19/19 ; `qemu-mps2-an386.peripheriques` **Passed**
dans les 4 `banc-kal.log` an386 ; trunk sans fichier régulier, lien cassé ni `__pycache__`.

### 12.2 Comparaisons

```bash
cd "$T"; O=doc/devenv/rapports/oracles
norm() { grep -E '^(section|symbole)' "$1" | sed -E 's/ \[.*$//; s/ +: /: /' | grep -v -E '^section [^:]*: \.debug_' | LC_ALL=C sort; }
diff -q $O/env-61-debian/host/mklepton-empreintes.sha256 $O/env-66-debian/host/mklepton-empreintes.sha256 && echo "mklepton = R61-1"
diff -q $O/env-52-apres/host/mklepton-empreintes.sha256 $O/env-66-debian/host/mklepton-empreintes.sha256 && echo "mklepton = Mac env-52-apres"
for p in $(ls $O/env-66-debian | grep -v -e host -e ctest-N -e compilation -e '\.log$'); do
  python3 scripts/oracle/comparer-oracle.py $O/env-61-debian/$p $O/env-66-debian/$p > "$J/12-cmp-R61-$p.txt" 2>&1; a=$?
  python3 scripts/oracle/comparer-oracle.py $O/env-52-apres/$p $O/env-66-debian/$p > "$J/12-cmp-Mac-$p.txt" 2>&1; b=$?
  echo "$p comparer_R61-1=$a comparer_Mac=$b hors_debug=$(norm $J/12-cmp-R61-$p.txt | wc -l)"
done | tee "$J/12-bilan.txt"
```
Attendu :
- mklepton : empreintes identiques à `env-61-debian` et à `env-52-apres` ;
- `comparer_R61-1` **0** pour les **16 presets**, `hors_debug=0` (aucun écart admis) ;
- `comparer_Mac` : informatif (1 attendu partout, chaînes différentes).

Un `comparer_R61-1` non nul : écart à exposer, avec l'extrait du `12-cmp-R61-<preset>.txt` ; si
seules des sections `.debug_*` changent, le dire (`hors_debug=0`) ; pas de correction.

### 12.3 Commande de miroir, à blanc

```bash
scion mirror-sync --dry-run -v ~/lepton-tools-dev/essais/env-53-debian > ~/env-66-journaux/12-mirror-sync.log 2>&1; echo "code=$?" >> ~/env-66-journaux/12-mirror-sync.log
```
Puis :
```bash
cd "$T"
grep -E 'référence\(s\) à envoyer|signalement' "$J/12-mirror-sync.log"; tail -1 "$J/12-mirror-sync.log"
python3 -I "$T/$C" "$R53" "$T/$A50/trunk-liens.txt" "$J/12-controle-R53" | tail -1
```
Attendu (R61-1) : code 0 ; 8 lignes `miroir … : 0 référence(s) à envoyer, 0 signalement(s)` ; trunk
de `$R53` `CONFORME`. Une référence « à envoyer » n'est admise que si une publication amont
postérieure au 2026-11-17 l'explique : la relever, puis relever la référence de l'amont
(`git ls-remote https://github.com/STMicroelectronics/<nom>.git`), sans arrêt. Un signalement :
écart à exposer. Jamais sans `--dry-run`.

## 13. Cartes (C8)

Écarté au PA-119 : ni binaire, ni flash, ni sonde ne changent. Aucune
commande OpenOCD.

## 14. Nettoyage de la VM (C9)

Après le commit du rapport (§15) seulement. Relevé par la session :
```bash
du -sh "$W" "$FX" ~/env-61-journaux ~/tmp-pytest/env-61 2>&1
```
Puis, par la session, règle `allow` :
```bash
scripts/supprimer-essai.sh ~/lepton-tools-dev/essais/env-66-essai ~/lepton-tools-dev/essais/env-66-fixture ~/env-61-journaux ~/tmp-pytest/env-61
```
Puis la session vérifie l'absence (`ls -d …`) et le consigne. Conservés : `$U`, `$E13`, `$C5`
(regreffés au §9), `$R53`, `$J`, `~/tmp-pytest/env-66`, `$J/0-settings-avant.json` (copie des
réglages d'avant le §0). Périmètre validé au PA-119.

## 15. Critères et rapport

| Critère | Attendu |
| --- | --- |
| C1 Versions | `git ls-remote` = Mac (§5) ; `settings.json`, hook, enveloppe = Mac ; Claude Code relevé (journal) ; git 2.47.3 ; scion 0.6.3.3 par `install-debian.sh` (défaut `SCION_REF`) ; lepton `pipx` code 0, `scion 0.6.3.3 (requis ≥ 0.6.2.0)`, correction D21 présente ; extension 0.5.3 par `install-vscodium.sh` (`0.5.2 → 0.5.3`) ; chaîne relevée |
| C2 D26, D28, hook | §0 fait avant l'ouverture de la session, `diff` = entrée retirée ; réglages relus en entier, bloc `allow` = 2 règles ; U1, U2 par la règle utilisateur, sans effet ; U3 au classifieur ; A1 annoncé « À REFUSER », invite, refusée ; H1 hook ; `pipx install --force` par la règle du dépôt ; `graft-update` ×4 annoncés « À CONFIRMER », invites confirmées ; `git clone` de seed.scions et pytest par la règle ; aucune cible créée ni supprimée à tort |
| C3 Regreffes | `$U`, `$E13` (et `$R53`, pour C7) : code 0, seul le noyau avance (dfc960b → 2b4a647), aucun clone, résumé = Mac (`cmp_mac`), liens inchangés (3889), `CONFORME` (attendu de R50-1), clones tiers 0 / 16, `clones = Mac`, `check` 0, espace = avant ; `$C5` : noyau seul, 3059 liens inchangés, `check` 0 |
| C4 D21 | §10 : écarts limités à `p6-n.cmd`, `p6-n.clangd`, `resume.tsv` (colonne 8) et aux `*.W` de la racine (hors `.DS_Store`, relevés) ; colonnes 1-7 = Mac ; états = départ |
| C5 D25, D22, pytest | §11.1 : l01, l02 code 2, aucune greffe fausse, l03 0 ; écarts limités à `depart.etat` et `l03.etat` (empreintes de la graine) ; §11.2 : trois fixtures écarts=0 ; lignes de git en français relevées ; §11.3 : pytest 570 passed |
| C6 D23, D24 | extension 0.5.3 installée ; D23 `d23.tsv` = Mac par le runtime de VSCodium (ou écart relevé) ; D24 (PA-119, option (a)) : U4 « lepton : retirer env65lib — terminé » seul, T3 « Clone de library-env65lib supprimé hors de lepton… » seul, aucune notification d'échec de regreffe ; états relevés |
| C7 Constructions, miroir | host ctest 7/7 ; 16 presets construits ; QEMU fumée et banc 20/20, 16/16, 19/19, `peripheriques` ×4 ; mklepton = `env-61-debian` = `env-52-apres` ; `comparer_R61-1` 0 pour les 16 presets ; `mirror-sync --dry-run` : code 0, 8 miroirs, 0 à envoyer (ou expliqué par l'amont), 0 signalement ; rien envoyé |
| C8 Cartes | écarté (PA-119) |
| C9 Nettoyage | `$W`, `$FX`, `~/env-61-journaux`, `~/tmp-pytest/env-61` supprimés par l'enveloppe ; absents |

Avant le commit, relevé final des décisions (toute la session) :
```bash
cd "$T"; F=$(ls -t ~/.claude/projects/*lepton-tools-dev-lepton-tools/*.jsonl | head -1)
python3 -I "$T/$DEC" "$F" > "$J/15-decisions.tsv"; wc -l < "$J/15-decisions.tsv"
```

Rapport `doc/devenv/rapports/env-66-debian.md` sur `devenv/env-66-debian`, avec :
- l'hôte, les versions et la session (répertoire de travail, Claude Code du journal, réglages) ;
- la table des critères ;
- C2 : le `diff` du §0 ; le contenu de `~/.claude/settings.json` ; la table des commandes et
  décisions (extrait de `15-decisions.tsv` : U1 à U3, A1, H1, `pipx install`, `graft-update` ×4,
  `git clone`, pytest, push), avec l'heure de chaque `AVANCEMENT` « À REFUSER » / « À CONFIRMER »
  et du lancement qui le suit ;
- la table des presets : construction, fumée, banc KAL, `comparer_R61-1`, `comparer_Mac` ;
- C3 : les quatre bilans, les lignes `clones.txt` après, `ignorecase`, tailles ;
- C4, C5, C6 : bilans `écarts=…` de `cmp_mac`, lignes de git en français (`cat -v`), codes ;
- pytest, miroir, nettoyage ;
- les écarts et constats ;
- le journal des messages §2bis (ID, date, résumé, remis ou non) ;
- ce qui n'a pas été fait.

Sous `doc/devenv/rapports/env-66-debian/` : `15-decisions.tsv` (chemin personnel remplacé par
`<HOME>`), `settings-utilisateur.json` (sortie du §8.1), `0-settings.diff` (diff du §0),
`10-c4/`, `11-c5/`, `11-fixture65/`, `11-fixture60/`, `11-fixture56/`, `11-d23/`,
`11-pytest.xml`, et pour chaque rootstock du §9 `<nom>-bilan.txt`, `<nom>-graft-update.log`,
`<nom>-tiers-apres/clones.txt` ; l'oracle `doc/devenv/rapports/oracles/env-66-debian/` (si C7).
Commit sur `devenv/env-66-debian` (créée au §12.1), puis `QUESTION` à l'utilisateur pour le push
(PA-P ; `AVANCEMENT` « À CONFIRMER : `git push origin devenv/env-66-debian` »), puis le §14, puis
`FIN-*`.
