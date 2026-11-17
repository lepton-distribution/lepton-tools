# Consigne — session Claude Code sur la VM Debian — ENV-61 (validation Debian groupée)

Fichier autonome : avec `ORCHESTRATION.md` §2bis, il suffit à conduire la session VM. Rédigé le
2026-11-17 par la session Mac `validate-env-58-60-debian` (tâche 1 d'ENV-61), repris de
`consignes/env-57-debian.md`. Validé par l'utilisateur au PA-109 (2026-11-17) : regreffe de
`$U`, `$E13`, `$C5` et `$R53` (C3) ; reconstruction des 16 presets maintenue (C6, après regreffe
de `$R53`) ; fixture d'ENV-56 sur la VM (C5) ; cartes écartées (C7) ; nettoyage tel qu'écrit
(C8) ; préalable du §0 (switch et relance de la session VM par l'utilisateur, réglages de la VM
non modifiés).
Son texte est envoyé tel quel dans l'ordre `R61-1`.

## 0. Préalable, avant l'ordre (utilisateur) — PA-109

Les réglages et le hook du dépôt sont lus par une session lancée dans `$T`. Avant l'envoi de
`R61-1`, l'utilisateur, sur la VM :
1. dans un terminal :
   ```bash
   cd ~/lepton-tools-dev/lepton-tools && git status --short && git fetch origin && git switch devenv/env-61 && git merge --ff-only origin/devenv/env-61 && git log --oneline -1
   ```
2. ne modifie pas `~/.claude/settings.json` (PA-103 : ses 3 règles `allow` sont gardées, D19) ;
3. ferme la session Claude Code de la VM et en ouvre une nouvelle **dans ce répertoire**, en mode
   auto, avec Remote Control ; il approuve le dossier si Claude Code le demande ;
4. communique à la session Mac le nom de la nouvelle session (`ListAgents`), à qui l'ordre est
   envoyé.

## 1. Objet

Valider sur Debian x86_64 l'état publié après ENV-58, ENV-59 et ENV-60 :
- **D20** (ENV-58) : formes des commandes (ORCHESTRATION §2bis amendé) et garde **G2** du hook
  `proteger-trunk.py` : une commande `ask` lancée indirectement (script shell, `bash -c`, `eval`)
  fait paraître l'invite ;
- **D19** (ENV-58, PA-103) : les 3 règles `allow` de `~/.claude/settings.json` de la VM sont
  gardées, fichier non modifié ; une décision `userSettings` est attendue pour une commande que
  seule l'une d'elles couvre ;
- **D17** (ENV-59) : lepton calcule l'indice du refus « version sans effet » comme le contrôle
  d'existence (`~` et `~<utilisateur>` développés) ; `~<utilisateur sans compte>/…` donne un
  message de lepton au lieu d'une trace ;
- **D18** (ENV-60) : scion **0.6.3.2** fait un clone à sa version déclarée par
  `git clone -b <version>`, ou n'en fait aucun ;
- regreffe de `$U`, `$E13`, `$C5` et `$R53` : seul le clone noyau avance (ed2a41f → **dfc960b** :
  `SCION_REF` 0.6.3.2 dans les scripts d'installation et la documentation, hors de `scion/`).
  Aucun lien ne change ;
- constructions host et 16 presets dans `$R53` regreffé : **aucun binaire changé** depuis R57-1.

**Pas de cartes** dans cette session (PA-109). Aucune écriture flash.

Références publiées (toutes poussées) :

| Dépôt (`https://github.com/lepton-distribution/…`) | Référence | Commit | En R57-1 |
| --- | --- | --- | --- |
| `lepton-tools` | `devenv/env-61` (cette consigne ; code identique à `main` 7018302) | tête après `fetch` | 10b6dd3 (`devenv/env-57`) |
| `seed.scions` | tag `0.6.3.2` | **08a1460** (`master` 975caf6) | tag `0.6.3.1` c51ee1a |
| `lepton-original-tree.scions` (noyau) | `master` | **dfc960b** | ed2a41f |
| graine `lepton-seed.scions`, 12 autres greffons, 8 miroirs | | inchangés | = |

Relevé du Mac : `rapports/env-61-mac/ls-remote-mac.txt` (script `env-61-mac/ls-remote.sh`).

Références Mac (`rapports/env-61-mac.md` §1, `rapports/env-61-mac/attendu/`) :
- liste `chemin -> cible` : `rapports/env-50-mac/attendu/trunk-liens.txt` (3889, inchangée depuis
  R50-1, revérifiée sur `<ROOTSTOCK>` le 2026-11-17) ; clones tiers :
  `rapports/env-53-mac/attendu/clones-rootstock-mac.txt` ;
- C3 : `attendu/c3/` (regreffe d'`essais/env-13-vierge`, même état que `$U` et `$E13`) ;
- C4 : `attendu/c4/` (D17 : `rapports/env-59-tilde/classer.py` et `essai.sh` sur une copie
  d'`essais/env-11/qemu` du Mac, lepton 0.1.0 et scion 0.6.3.2) ;
- C5 : `attendu/c5/` (D18 : `rapports/env-60-scion/essai.sh`, même copie) et `attendu/fixture56/`
  (`rapports/env-56-scion/fixture.py`, clone de seed.scions au tag 0.6.3.2).

Référence Debian : `rapports/env-57-debian.md` et `oracles/env-57-debian/`.

La session VM ne développe pas : elle exécute, constate et rapporte.

## 2. Ce que la session VM peut faire, et ne fait pas

| Autorisé | Interdit |
| --- | --- |
| `git fetch` / `switch` / `merge --ff-only` de `$T` (`devenv/env-61`) et du clone noyau `$K` (`master`) | Modifier `DEVENV-STATUS.md`, `ORCHESTRATION.md`, `SPECIFICATION.md`, `handoff/*.md`, les consignes, `rapports/env-61-mac*`, `.claude/`, `~/.claude/settings.json` |
| Installations du §6 (`sudo` sans mot de passe sur la VM), dans les formes écrites | Toute autre commande `sudo`, `pip install` hors de `venv-test`, `codium --install-extension` hors `install-vscodium.sh` |
| `scion graft-update` de `$U`, `$E13`, `$C5`, `$R53` (§9), dans la forme écrite : l'invite de Claude Code est confirmée par l'utilisateur | `graft-update` d'un autre rootstock ; tout `seed-update` ; toute écriture dans les clones de `$U`, `$E13`, `$C5`, `$R53` |
| Lectures dans `$U`, `$E13`, `$C5`, `$R53` ; `lepton check` / `generate` / `seed status` dans ces quatre rootstocks ; `rejouer-oracle.sh` dans `$R53` (`build/` compris, §12) | Écrire un fichier régulier dans un `trunk/` ou sous `depots/tiers/` (le hook refuse) ; corriger quoi que ce soit |
| Créer `$S`, `$D59`, `$D60` (§7), `$SS`, `$FX` (§11.2) et y tout faire, `seed add` / `seed remove` compris | `git config` (même en lecture) et `git sparse-checkout` dans un clone de `depots/tiers/` : relever par `releve-clones.sh` |
| `scion mirror-sync --dry-run` dans `$R53` (§12) | `mirror-sync` sans `--dry-run` ; tout envoi vers un miroir |
| Les contrôles du §8, sur cibles absentes ou protégées | Toute écriture flash, toute commande OpenOCD ; modifier la configuration réseau de la VM |
| Suppressions par `scripts/supprimer-essai.sh` (§14) | `rm -rf` direct |
| Créer `devenv/env-61-debian` (depuis `devenv/env-61`) ; y écrire `doc/devenv/rapports/env-61-debian.md`, `doc/devenv/rapports/env-61-debian/` et `doc/devenv/rapports/oracles/env-61-debian/` | Commiter sur une autre branche |
| `git push origin devenv/env-61-debian` **après accord explicite de l'utilisateur** (PA-P ; invite `ask`) | Pousser toute autre branche |

Formes des commandes : **ORCHESTRATION §2bis**, « Commandes soumises aux règles de
`.claude/settings.json` » et « Formes » (ENV-58, PA-103). Chaque commande de cette consigne y est
écrite dans la forme couverte par sa règle ; la lancer **telle qu'écrite, une par appel**. Rappel
des effets attendus ici :
- une commande `allow` lancée seule garde sa règle (`2>&1` admis). Une redirection vers un
  fichier hors de `$T`, un `| tee` ou un `; echo "code=$?"` la font passer au classifieur : les
  commandes `allow` de cette consigne n'en ont pas, et pytest écrit son journal par
  `--junitxml` ;
- une commande `ask` (`scion graft-update`, `git push`) est lancée **directement**, jamais par un
  script, un `bash -c` ou un `eval`. Lancée indirectement, elle fait paraître une invite demandée
  par le hook (G2) : seuls A2 et A3 du §8 le font, exprès, et ces invites sont refusées ;
- depuis G2, lancer un script shell qui contient `scion graft-update`, `seed-update` ou `git push`
  hors commentaire fait paraître une invite, même pour `-h`. Les scripts de cette consigne n'en
  contiennent pas, hors `ask-script.sh` (A2). Une invite inattendue : la refuser, `AVANCEMENT`.

Autres règles :
- **Refus.** Toute commande refusée (classifieur, invite, hook) n'est jamais contournée :
  `AVANCEMENT` avec la commande exacte et la décision, l'utilisateur la lance s'il le décide, la
  session vérifie l'effet et le consigne. Seuls les refus attendus du §8 (A1 à A3, H1) ne
  demandent rien à l'utilisateur, sinon de refuser les invites A1 à A3.
- **Refus d'une invite.** Il interrompt le tour de la session. L'utilisateur relance par un
  message dans la session VM (`reprendre R61-1 au §8, A2`, par exemple).
- **Régénérer avant de relever** : tout relevé « avant » d'un fichier généré suit immédiatement la
  commande qui le produit (`regreffer-essai.sh avant` le fait).
- **Branche des clones d'un rootstock existant** : relevée au §5 pour `$U`, `$E13`, `$C5`. scion
  refuse lui-même un clone hors de sa version déclarée ; un tel refus reste un écart à exposer.
- **scion et lepton avant D17 et D18** : aucun essai du §10 ni du §11 avant que `scion version`
  donne 0.6.3.2 et que lepton soit réinstallé (§6). Avec 0.6.3.1, le défaut D18 demeure ; avec le
  lepton de R57-1, le défaut D17 demeure.

Tout écart au plan, toute erreur non prévue : s'arrêter, exposer (`AVANCEMENT` ou `QUESTION`),
attendre.

## 3. Communication (ORCHESTRATION §2bis)

- Session principale : `validate-env-58-60-debian` (session Mac ; Claude Code peut la renommer).
  Répondre à l'adresse `from` du message d'ordre.
- ID : `R61-1`, repris tel quel : `[ACCUSÉ R61-1] ENV-61 — …`, `[AVANCEMENT R61-1] …`,
  `[QUESTION R61-1] …`, `[FIN-SUCCÈS R61-1] …` ou `[FIN-ÉCHEC R61-1] …`.
- `ACCUSÉ`, avant toute commande autre que les lectures du §5. Il contient :
  - l'ordre reformulé en une phrase ;
  - le nom de la session VM et son répertoire de travail ;
  - la tête réelle de `devenv/env-61` ; les empreintes de `.claude/settings.json` et du hook ;
  - les résultats de `git ls-remote` du §5 ;
  - les branches et têtes des clones de `$U`, `$E13` et `$C5` ;
  - les étapes prévues (§6 à §15) et les écarts déjà visibles.
- `AVANCEMENT` : avant chaque commande soumise à une invite (§8 A1 à A3, §9, push), avant toute
  action demandée à l'utilisateur, à chaque refus non prévu, après chacun des §6 à §12, et à
  chaque arrêt.
- `FIN-SUCCÈS` / `FIN-ÉCHEC` : résultat par critère du §15, commits et branche (poussée ou non),
  chemin du rapport, versions relevées, écarts, ce qui n'a pas été fait.
- **Remise en échec** (§2bis) : un envoi en erreur (ECONNRESET, « bridge ID is stale ») est renvoyé
  une fois, à l'identique. Si le second envoi échoue, le message entier est consigné dans
  `~/env-61-journaux/0-messages-R61-1.md` et au §Messages du rapport, avec la mention « non remis ».
  La session l'annonce à l'utilisateur, qui le relaie à la session Mac. Un message relayé par
  l'utilisateur et portant l'ID `R61-1` vaut message reçu.

## 4. Journaux et variables

```bash
mkdir -p ~/env-61-journaux
J=~/env-61-journaux
T=~/lepton-tools-dev/lepton-tools
K=~/lepton-tools-dev/lepton-noyau
E=~/lepton-tools-dev/essais
U=$E/env-28-debian
E13=$E/env-13-debian
C5=$E/env-53-c5
R53=$E/env-53-debian
S=$E/env-61-essai
D59=$E/env-61-depot59
D60=$E/env-61-depot60
AB=$E/env-61-absent.git
SS=$E/env-61-seed-scions
FX=$E/env-61-fixture/f56
X=doc/devenv/rapports/env-61-mac
A=$X/attendu
X57=doc/devenv/rapports/env-57-mac
Y=doc/devenv/rapports/env-53-mac
A50=doc/devenv/rapports/env-50-mac/attendu
C=doc/devenv/rapports/env-43-mac/controler-trunk.py
LI=$Y/liens.py
IC=$Y/inventaire-clones.sh
RG=$X57/regreffer-essai.sh
DEC=$X57/decisions.py
fr() { sed -e 's/: et que le dépôt existe\.$/: and the repository exists./' -e "s/fatal : La branche distante \(.*\) n'a pas été trouvée dans le dépôt amont \(.*\)\$/fatal: Remote branch \1 not found in upstream \2/" "$1"; }
```
`$AB` et `~/lepton-tools-dev/essais/env-61-absent` n'existent pas et ne doivent jamais être
créés : ce sont l'origine absente des essais et la cible absente des contrôles du §8. Les
commandes non couvertes par une règle portent leur journal
(`> "$J/<étape>.log" 2>&1; echo "code=$?" >> …`). Les boucles s'écrivent en bash. Ne pas faire
`cd` dans un `trunk/` : revenir à `$T` (le hook juge le répertoire courant).

`fr()` ramène à l'anglais les deux messages de git que relaie scion dans les essais, traduits sur
la VM (git 2.47.3, `po/fr.po` : « and the repository exists. », et « Remote branch %s not found in
upstream %s », avec le préfixe « fatal : »). Elle ne touche aucune autre ligne.

Outils de la session Mac, en lecture seule, utilisables tels quels sur Debian :
- `env-53-mac/` : `releve-clones.sh`, `inventaire-clones.sh`, `liens.py` ;
- `env-57-mac/regreffer-essai.sh avant|apres <rootstock> <journaux>` : relevés avant et après une
  regreffe, bilan `<journaux>/<nom>-bilan.txt` ; le `graft-update` est lancé à part par la
  session, entre les deux phases. Ses mentions de `graft-update` sont des noms de fichiers : G2
  ne s'y déclenche pas (essai du Mac) ;
- `env-57-mac/decisions.py <journal .jsonl> [--motif <texte>]…` : décisions de permission des
  appels Bash de la session (TSV : heure UTC, décision, source, `reasonType`, `ruleSource`,
  commande) ;
- `env-59-tilde/classer.py`, `env-59-tilde/essai.sh` (D17), `env-60-scion/essai.sh` (D18),
  `env-56-scion/fixture.py` : essais rejoués aux §10 et §11 ; chaque cas est relevé (`.cmd`,
  `.out`, `.err`, `.code`) et, pour les deux `essai.sh`, l'état du rootstock est comparé au départ
  (`<cas>.etat`).

## 5. Vérifications préalables (lecture seule) — C1

```bash
pwd; printenv CLAUDE_PROJECT_DIR; claude --version 2>&1 | head -1
git -C "$T" status --short | head -5; git -C "$T" branch --show-current; git -C "$T" log --oneline -1
git -C "$T" fetch origin && git -C "$T" status -sb | head -1
sha256sum "$T/.claude/settings.json" "$T/.claude/hooks/proteger-trunk.py" "$T/scripts/supprimer-essai.sh"
ls -la ~/.claude/settings.json ~/.claude/settings.local.json "$T/.claude/settings.local.json" 2>&1
ls -t ~/.claude/projects/*lepton-tools-dev-lepton-tools/*.jsonl 2>&1 | head -2
uname -sm; cat /etc/debian_version; uname -r; id -un; git --version
scion version | tail -1; lepton --version; printenv SCION_REF SCION_SPEC
arm-none-eabi-gcc --version | head -1; cmake --version | head -1; ninja --version; qemu-system-arm --version | head -1; python3 --version; codium --version | head -1
command -v shasum realpath tar; ls -d ~/tmp-pytest ~/lepton-tools-dev/venv-test/bin/pytest 2>&1
id inconnu59 2>&1 | head -1
df -h ~ /tmp | tail -2
for Z in "$S" "$D59" "$D60" "$AB" "$SS" "$E/env-61-fixture" "$E/env-61-absent"; do test -e "$Z" && echo "ARRÊT : $Z existe déjà"; done
cd "$T" && bash $X/ls-remote.sh > "$J/5-ls-remote.txt" 2>&1; diff <(grep -v '^lepton-tools ' $X/ls-remote-mac.txt) <(grep -v '^lepton-tools ' "$J/5-ls-remote.txt") && echo "têtes publiées = Mac"
for Z in "$U" "$E13" "$C5"; do
  echo "== $Z"
  git -C "$Z"/depots/lepton-seed*/* log --oneline -1
  grep -v '^#' "$Z"/trunk/.scion.grafted.list | grep -c .
  bash "$T/$IC" "$Z" | tee "$J/5-clones-$(basename $Z).txt"
  python3 -I "$T/$LI" "$Z/trunk" > /dev/null
  ls -d "$Z"/depots/tiers/*/* 2>&1; du -sk "$Z"/depots/tiers 2>&1
done
ls -d "$R53" ~/env-57-journaux "$E/env-11" 2>&1; ls -d "$E"/*/ 2>&1
```
Attendu :
- répertoire de travail `$T` (`/home/lepton-user/lepton-tools-dev/lepton-tools`) ; lepton-tools
  propre, sur `devenv/env-61`, à jour avec `origin/devenv/env-61` (préalable du §0) ;
- `.claude/settings.json` `b01ad557…d235` (inchangé depuis R57-1), `proteger-trunk.py`
  `04572df6…6909` (garde G2, ENV-58), `supprimer-essai.sh` `04323a00…0e15` (Mac) ; réglages
  utilisateur et locaux relevés (lus en entier au §8, D19) ;
- `têtes publiées = Mac` ; git **2.47.3** ; scion **0.6.3.1** (avant installation) ;
  `lepton 0.1.0`, `scion 0.6.3.1 (requis ≥ 0.6.2.0)` ; `SCION_REF` et `SCION_SPEC` vides ;
- chaîne APT de R57-1 : arm-none-eabi-gcc 14.2.1, cmake 3.31.6, ninja 1.12.1, QEMU 10.0.13,
  Python 3.13.5, codium 1.135.06055 ; `shasum`, `realpath`, `tar` présents ; `~/tmp-pytest` et
  `venv-test/bin/pytest` présents ; `id inconnu59` : utilisateur inconnu (sinon l'essai D17
  s'arrête) ;
- `$U` et `$E13` (état laissé par R57-1), chacun : graine 15740f9 ; **23 entrées** ; 14 lignes
  d'inventaire, la graine sur `original-tree`, 13 clones `<clé>/master` sur `master`, amont réglé,
  `modifs=0`, noyau **ed2a41f** ; `liens=3889 casses=0 reguliers=0` ; 8 clones tiers
  (≈ 108 760 Ko) ;
- `$C5` : graine `env11` 6d3d2a5 ; `liens=3059 casses=0 reguliers=0` ; noyau ed2a41f, an386
  10a8889 ; `salut` sans amont, `modifs=2` (état d'origine de la VM) ; clones F7 conservés de
  R53-1 ;
- `$R53` et `~/env-57-journaux` présents ; `essais/env-11` absent (supprimé en R57-1).

Arrêts :
- un chemin du `for` initial existe ;
- lepton-tools non propre, hors de `devenv/env-61`, ou `settings.json` ou hook différent du Mac ;
- un commit publié diffère du Mac ;
- graine de `$U`, `$E13` ou `$C5` modifiée ; un clone de greffon publié hors de sa branche, sans
  amont ou modifié ;
- `shasum`, `realpath` ou `tar` absent ; moins de 8 Go libres dans `~`.

Pas des arrêts, à consigner : une version de la chaîne ou de Claude Code différente de R57-1 ; un
répertoire de travail autre que `$T` (les règles du dépôt ne seraient pas lues : C2 le montrera,
l'exposer).

## 6. Installation de scion 0.6.3.2 et de lepton (C1)

D'abord, par la session :
```bash
git -C "$K" status --short | head -5
git -C "$K" fetch origin && git -C "$K" switch master && git -C "$K" merge --ff-only origin/master && git -C "$K" log --oneline -1
grep -n '^SCION_REF=' "$K/scripts/install-debian.sh" "$T/scripts/install-vscodium.sh"
grep -n 'SCION_MIN_VERSION =' "$T/lepton/__init__.py"; grep -n '"version"' "$T/extension/package.json"; ls "$T"/extension/dist/lepton-0.5.2.vsix
```
Attendu : clone noyau propre, à **dfc960b** (ed2a41f avant) ; `SCION_REF="${SCION_REF:-0.6.3.2}"`
(noyau) et `SCION_REF="0.6.3.2"` (lepton-tools) ; `SCION_MIN_VERSION = (0, 6, 2, 0)` ;
extension 0.5.2, `.vsix` présent.

Puis `AVANCEMENT`, et la session lance, une commande par appel, dans cet ordre :
1. scion (hors règle : classifieur ; accepté en R57-1) :
   ```bash
   bash ~/lepton-tools-dev/lepton-noyau/scripts/install-debian.sh --with-debug-tools > ~/env-61-journaux/6-install-debian.log 2>&1; echo "code=$?" >> ~/env-61-journaux/6-install-debian.log
   ```
   Il installe scion par `pipx install --force
   "git+https://github.com/lepton-distribution/seed.scions.git@0.6.3.2"` (défaut `SCION_REF`). En
   cas de refus : `AVANCEMENT` ; l'utilisateur lance la même ligne, ou seulement cette commande
   `pipx`, dans la session VM (`!` en premier caractère) ou dans un terminal.
2. lepton (règle `allow` du dépôt, forme exacte, sans redirection) :
   ```bash
   pipx install --force ~/lepton-tools-dev/lepton-tools
   ```
   Sortie lue dans le résultat de l'outil et reportée au rapport. Elle installe le lepton
   d'ENV-59 (D17).
3. VSCodium (hors règle) :
   ```bash
   bash ~/lepton-tools-dev/lepton-tools/scripts/install-vscodium.sh --lepton-clone ~/lepton-tools-dev/lepton-noyau > ~/env-61-journaux/6-install-vscodium.log 2>&1; echo "code=$?" >> ~/env-61-journaux/6-install-vscodium.log
   ```

Puis :
```bash
tail -3 "$J/6-install-debian.log"; grep -n -i 'scion' "$J/6-install-debian.log" | tail -5; tail -12 "$J/6-install-vscodium.log"
scion version | tail -1; lepton --version; codium --version | head -1
pipx list --short | grep -E '^(scion|lepton) '
PYL=$(dirname "$(realpath "$(command -v lepton)")")/python; echo "$PYL"; "$PYL" -I -c 'import lepton.seed as s, inspect; print("expanduser().resolve()" in inspect.getsource(s.parse_location))'
codium --list-extensions --show-versions | LC_ALL=C sort > "$J/6-extensions.txt"; grep -E -i 'lldb|lepton|rtos-views|peripheral' "$J/6-extensions.txt"
```
Attendu : codes 0 ; `scion version: 0.6.3.2` ; `lepton 0.1.0`, `scion 0.6.3.2 (requis ≥ 0.6.2.0)` ;
`True` (correction D17 installée) ; `install-vscodium.sh` : `changements 0` ;
`lepton-distribution.lepton@0.5.2`, `vadimcn.vscode-lldb@1.12.3`, `mcu-debug.rtos-views@0.0.16`,
`mcu-debug.peripheral-viewer@1.6.4`.

**Arrêt** si scion n'est pas 0.6.3.2 ou si la correction D17 n'est pas installée : ni §9, ni §10,
ni §11.

## 7. Copie d'essai et dépôts présents (pour C2, C4, C5)

Avant toute regreffe de `$C5` (§9), pour que la copie parte de l'état de celle du Mac (noyau
ed2a41f, 3059 liens) :
```bash
cd "$T"
mkdir "$S" && tar -C "$C5" --exclude=./build -cf - . | tar -C "$S" -xf -; echo "copie=$?"
python3 -I "$T/$LI" "$S/trunk" > "$J/7-liens-depart.txt"
lepton check -C "$S" > "$J/7-check.log" 2>&1; echo "code=$?" >> "$J/7-check.log"; tail -2 "$J/7-check.log"
lepton scion new env59lib --type bibliotheque --repo "$D59" --no-seed --no-cmake -C "$S" > "$J/7-scion-new-59.log" 2>&1; echo "code=$?" >> "$J/7-scion-new-59.log"; cat "$J/7-scion-new-59.log"
lepton scion new env60lib --type bibliotheque --repo "$D60" --no-seed --no-cmake -C "$S" > "$J/7-scion-new-60.log" 2>&1; echo "code=$?" >> "$J/7-scion-new-60.log"; cat "$J/7-scion-new-60.log"
git -C "$D59" log --oneline; git -C "$D60" log --oneline; git -C "$S"/depots/lepton-seed/env11 status --short | wc -l
```
Attendu : `copie=0` ; `liens=3059 casses=0 reguliers=0` ; `check` code 0 ; `dépôt créé : …`
(`lib/env59lib`, puis `lib/env60lib`), codes 0, un commit chacun ; graine sans modification (0).
La copie n'est pas régénérée par `lepton generate` (la copie du Mac ne l'a pas été).

## 8. Règles de permission sur la VM (C2 : D19, D20, G2)

Toutes les commandes de ce paragraphe sont lancées par la session, **une par appel, telles
qu'écrites** (chemins `~/…` littéraux). La décision de chacune est relevée à la fin dans le
journal de session. Catégories `pipx install --force` (§6.2), `scion graft-update` (§9),
`git clone` (§11.2), tests (§11.3), suppressions (§14) et push : relevées dans les paragraphes
indiqués.

### 8.1 D19 : réglages utilisateur

```bash
python3 -m json.tool ~/.claude/settings.json
```
Attendu : le fichier entier, reporté au rapport. Le bloc `permissions.allow` est exactement
(`rapports/env-58-formes.md` §7) :
```json
"allow": [
  "Bash(pipx install:*)",
  "Bash(git clone * https://github.com/lepton-distribution/*)",
  "Bash(python3 -m unittest discover *)"
]
```
et c'est le seul qui porte des règles (ni `ask`, ni `deny`, ni `defaultMode`), comme en R57-1.
Toute autre clé est relevée. Un bloc différent : `QUESTION` (le PA-103 l'a gardé tel quel).

Commandes que seule une règle utilisateur couvre, sur cibles absentes (attendu : décision
`userSettings`, échec sans effet) :

| N° | Commande | Attendu |
| --- | --- | --- |
| U1 | `pipx install ~/lepton-tools-dev/essais/env-61-absent` | règle `Bash(pipx install:*)` ; code ≠ 0, rien d'installé |
| U2 | `git clone --depth 1 https://github.com/lepton-distribution/env-61-absent.git ~/lepton-tools-dev/essais/env-61-absent` | règle `Bash(git clone * https://github.com/lepton-distribution/*)` ; code ≠ 0 (dépôt inexistant), cible absente |
| U3 | `python3 -m unittest discover -s ~/lepton-tools-dev/essais/env-61-absent` | règle `Bash(python3 -m unittest discover *)` ; code ≠ 0, aucun test |

### 8.2 D20 : formes d'une commande `allow`

Commande de base `P`, forme couverte par `Bash(~/lepton-tools-dev/venv-test/bin/pytest:*)` :
`~/lepton-tools-dev/venv-test/bin/pytest -q -p no:cacheprovider --basetemp ~/tmp-pytest/env-61-f tests/test_proteger_trunk.py::test_entree_illisible`
(lancée depuis `$T`).

| N° | Commande | Attendu (essai d'ENV-58, `rapports/env-58-formes.md` §2) |
| --- | --- | --- |
| F1 | `P` | règle (`subcommandResults`) ; 1 passed |
| F2 | `P > ~/env-61-journaux/8-f2.log` | classifieur (relevé) |
| F3 | `P 2>&1` | règle |
| F6 | `~/lepton-tools-dev/venv-test/bin/pytest -q -p no:cacheprovider --basetemp ~/tmp-pytest/env-61-f --junitxml ~/env-61-journaux/8-f6.xml tests/test_proteger_trunk.py::test_entree_illisible` | règle |
| F7 | `P; echo "code=$?"` | classifieur (relevé) |

### 8.3 D20 et G2 : commande `ask`, directe et indirecte ; hook

| N° | Commande | Attendu |
| --- | --- | --- |
| A1 | `scion graft-update -v ~/lepton-tools-dev/essais/env-61-absent` | règle `ask` : invite ; **l'utilisateur la refuse** |
| A2 | `bash doc/devenv/rapports/env-58-formes/ask-script.sh ~/lepton-tools-dev/essais/env-61-absent` | hook (G2) : invite, motif « commande ask lancée indirectement » ; **l'utilisateur la refuse** |
| A3 | `bash -c 'scion graft-update -v ~/lepton-tools-dev/essais/env-61-absent'` | hook (G2) : invite ; **l'utilisateur la refuse** |
| H1 | `touch ~/lepton-tools-dev/essais/env-61-essai/trunk/essai-hook` | hook : refus sans invite |

Avant A1 : `AVANCEMENT` à l'utilisateur (refuser l'invite A1, puis relancer par « reprendre R61-1
au §8, A2 » ; de même pour A2, puis « reprendre R61-1 au §8, A3 » ; pour A3, puis « reprendre
R61-1 au §8, H1 »). Le motif affiché par l'invite d'A2 et d'A3 est noté par l'utilisateur ou la
session : le journal de session ne garde que le refus.

Après H1 :
```bash
cd "$T"
ls -d ~/lepton-tools-dev/essais/env-61-absent "$S/trunk/essai-hook" 2>&1; pipx list --short | grep -c env-61
python3 -I "$T/$LI" "$S/trunk" | cmp - "$J/7-liens-depart.txt" && echo "liens de \$S = départ"
F=$(ls -t ~/.claude/projects/*lepton-tools-dev-lepton-tools/*.jsonl | head -1); echo "$F"
python3 -I "$T/$DEC" "$F" > "$J/8-decisions.tsv"; cut -c1-180 "$J/8-decisions.tsv" | grep -E 'pipx install|git clone|unittest|pytest|graft-update|ask-script|touch'
```
Attendu, dans `8-decisions.tsv` (forme du Mac, `rapports/env-58-formes/decisions.tsv`) :
- §6.2 `pipx install --force ~/lepton-tools-dev/lepton-tools` : `accept config rule projectSettings`
  (ou `subcommandResults`) ;
- U1 à U3 : `accept config rule userSettings` (ou `subcommandResults` avec la règle utilisateur) ;
- F1, F3, F6 : `accept config subcommandResults` ; F2, F7 : `classifier` (informatif) ;
- A1, A2, A3 : `rejet-invite` ; H1 : `reject hook hook` ;
- cible absente, `essai-hook` absent, aucun paquet `env-61` ; liens de `$S` = départ.

Écarts, sans arrêt sauf mention :
- une acceptation par le classifieur là où une règle est attendue (`reasonType` `classifier`) :
  règles non lues ou dossier non approuvé, à relever ;
- une invite non apparue pour A1, A2 ou A3 : **arrêt**, `QUESTION` (la commande serait exécutée
  sans accord ; elle reste sans effet, la cible étant absente) ;
- une décision `userSettings` pour une commande que couvre aussi une règle du dépôt : à relever
  (D19 l'admet).

## 9. Regreffe de `$U`, `$E13`, `$C5` (C3) et `$R53` (pour C6)

Pour chaque rootstock `Z` de la liste `env-28-debian`, `env-13-debian`, `env-53-c5`,
`env-53-debian`, dans cet ordre (`$C5` après la copie du §7) :
1. par la session, depuis `$T` :
   ```bash
   bash "$T/$RG" avant ~/lepton-tools-dev/essais/<nom> "$J/regreffes"
   ```
2. `AVANCEMENT` (« invite à confirmer »), puis la session lance, telle quelle :
   ```bash
   scion graft-update -v ~/lepton-tools-dev/essais/<nom> > ~/env-61-journaux/regreffes/<nom>-graft-update.log 2>&1; echo "code=$?" >> ~/env-61-journaux/regreffes/<nom>-graft-update.log
   ```
   L'utilisateur confirme l'invite de Claude Code (PA-P accordé au PA-109 pour ces quatre
   rootstocks) par « Oui », pour cette commande seule, jamais par « ne plus demander » (au Mac,
   ce choix a donné la décision `user_permanent`, sans règle écrite : `rapports/env-61-mac.md`
   §1.3).
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
   diff "$T/$A/c3/graft-update-resume.txt" <(resume "$L") && echo "journal = Mac"
   python3 -I "$T/$C" "$Z" "$T/$A50/trunk-liens.txt" "$J/9-<nom>-controle" > "$J/9-<nom>-controle.log" 2>&1; echo "code=$?" >> "$J/9-<nom>-controle.log"; tail -3 "$J/9-<nom>-controle.log"
   normc() { sed -E 's/ ignorecase=[^ ]*//; s/ ko_hors_git=.*//' "$1"; }
   diff <(normc "$T/$Y/attendu/clones-rootstock-mac.txt") <(normc "$J/regreffes/<nom>-tiers-apres/clones.txt") && echo "clones = Mac (hors ignorecase et tailles)"
   ```

Attendu, `$U`, `$E13` et `$R53` (Mac, `essais/env-13-vierge`, `attendu/c3/env-13-vierge-bilan.txt`) :
- `graft-update code=0 ; avancés : 1 ; git clone : 0 ; extraction partielle : 0 ; conflit/refus : 0` ;
  `depots/lepton/original/master avancé : ed2a41f -> dfc960b` ; « 3889 feuilles liées » ; aucune
  ligne `.DS_Store` sur la VM ;
- `journal = Mac` : 82 lignes (avancée du noyau, projections, « répertoire extrait » des 8 clones
  tiers, déjà partiels) ;
- `clones : 1 ligne(s) changée(s)` (noyau) ; liens 3889 → 3889, ajoutés 0, retirés 0 ;
  `controler-trunk CONFORME code=0` contre les liens d'avant **et** contre l'attendu de R50-1 ;
- `tiers : 8 clone(s)`, extraits et `sparse-checkout` ≠ attendu : **0 / 16** ; `clones = Mac` ;
  `ignorecase` vide (relevé) ; tailles relevées ;
- `check code=0`, `generate` avant et après code 0, `espace diff=0` ; trunk sans fichier régulier ni
  lien cassé.

Attendu, `$C5` : un seul clone avancé (noyau ed2a41f → dfc960b) ; `salut` accepté (sans amont,
`modifs=2`, comme en R57-1) ; 3059 liens inchangés, `CONFORME` contre les liens d'avant ; les 2
clones tiers F7 conservés de R53-1 ne sont pas greffés, inchangés (extraits et `sparse-checkout`
≠ attendu : 0 / 4) ; `check` code 0 ; espace identique.

Un refus de scion (clone hors version, graine divergée) : écart à exposer, sans contournement.

## 10. D17 : `~` dans l'indice « version sans effet » (C4)

Sur `$S` (§7), avec lepton réinstallé (§6) :
```bash
cd "$T"
PYL=$(dirname "$(realpath "$(command -v lepton)")")/python
"$PYL" -I doc/devenv/rapports/env-59-tilde/classer.py "$S" "$D59" "$AB" > "$J/10-classer.tsv" 2> "$J/10-classer.err"; echo "code=$?"; cat "$J/10-classer.err"
diff "$T/$A/c4/classer.tsv" "$J/10-classer.tsv" && echo "classer = Mac"
bash doc/devenv/rapports/env-59-tilde/essai.sh "$S" "$D59" "$AB" "$J/10-c4-brut" "$J/10-c4" > "$J/10-c4.log" 2>&1; echo "code=$?" >> "$J/10-c4.log"
grep -c 'état : $' "$J/10-c4.log"; grep 'état : .' "$J/10-c4.log"; tail -1 "$J/10-c4.log"
e=0; n=0; for f in "$T/$A"/c4/*; do b=${f##*/}; case $b in classer.tsv|*-status.out|depart.etat) continue;; esac
  n=$((n+1)); cmp -s "$f" <(fr "$J/10-c4/$b") || { echo "ÉCART $b"; e=$((e+1)); }; done; echo "c4 : écarts=$e / $n"
for b in $(cd "$T/$A/c4" && ls *-status.out); do diff "$T/$A/c4/$b" "$J/10-c4/$b" > /dev/null || echo "$b diffère (informatif)"; done | head -3
ls "$J/10-c4" | wc -l; ls "$T/$A/c4" | wc -l
python3 -I "$T/$LI" "$S/trunk" | cmp - "$J/7-liens-depart.txt" && echo "liens de \$S = départ"
```
Attendu (Mac, `attendu/c4/`, `rapports/env-61-mac.md` §1.4) :
- `classer = Mac` : 42 formes, dont les 14 lignes du PA-105 (indice
  `file://localhost<P>@master` ou `<A>`, « même dépôt » ; `~inconnu59/…` : « répertoire personnel
  de « ~inconnu59 » introuvable ») ; `<HOME>` et `~<U>` normalisent `lepton-user` ;
- 66 lignes `état : ` vides : chaque cas, retrait compris, revient au départ ;
- **écarts=0 / 528** relevés comparés (`.cmd`, `.out`, `.err`, `.code`, `.etat`, hors
  `classer.tsv`, les `*-status.out` et `depart.etat`), après `fr()` ;
- `*-status.out` : peuvent différer (graine `env11`, `salut`, noyau, dépôts) : informatif ;
- liens de `$S` = départ.

Un écart : relever le fichier et le `diff`, sans correction.

## 11. D18 : clone à la version déclarée, fixture, pytest (C5)

### 11.1 Cas de lepton d'ENV-60

```bash
cd "$T"
bash doc/devenv/rapports/env-60-scion/essai.sh "$S" "$D60" "$J/11-c5-brut" "$J/11-c5" > "$J/11-c5.log" 2>&1; echo "code=$?" >> "$J/11-c5.log"
cat "$J/11-c5.log"; cat "$J/11-c5/scion.txt"
e=0; n=0; for f in "$T/$A"/c5/*; do b=${f##*/}; case $b in scion.txt|depart.etat) continue;; esac
  n=$((n+1)); cmp -s "$f" <(fr "$J/11-c5/$b") || { echo "ÉCART $b"; e=$((e+1)); }; done; echo "c5 : écarts=$e / $n"
ls -d "$S"/depots/lepton/library-env60lib 2>&1
python3 -I "$T/$LI" "$S/trunk" | cmp - "$J/7-liens-depart.txt" && echo "liens de \$S = départ"
```
Attendu (Mac, `attendu/c5/`, `rapports/env-60-scion.md` §4) :
- l01 (`@scion`), l02 et l03 (`@nope`) : **code 2**. lepton relaie `erreur : échec de « git clone -b
  … » (code 128) : fatal: Remote branch … not found in upstream origin` (en français sur la VM,
  ramené par `fr()`), puis annule (« graine et trunk restaurés ») ;
- après chaque cas : liens, graine, liste greffée et `depots/` égaux au départ ; aucun clone
  `library-env60lib` ne reste (`ls -d` : absent) ;
- **écarts=0 / 15** après `fr()` ; `scion.txt` : 0.6.3.2, venv pipx ;
- liens de `$S` = départ.

### 11.2 Fixture d'ENV-56 (cas f06)

`fixture.py` importe les aides de test de seed.scions : il lui faut un clone au tag. Par la
session, une commande par appel :
```bash
git clone https://github.com/lepton-distribution/seed.scions.git ~/lepton-tools-dev/essais/env-61-seed-scions
```
(règle `allow` du dépôt, forme exacte, sans redirection), puis :
```bash
git -C ~/lepton-tools-dev/essais/env-61-seed-scions switch --detach 0.6.3.2
git -C ~/lepton-tools-dev/essais/env-61-seed-scions log --oneline -1; git -C ~/lepton-tools-dev/essais/env-61-seed-scions status --short | wc -l
cd "$T"
python3 -I doc/devenv/rapports/env-56-scion/fixture.py "$SS" "$(command -v scion)" "$FX" "$J/11-fixture56" > "$J/11-fixture56.log" 2>&1; echo "code=$?" >> "$J/11-fixture56.log"; tail -17 "$J/11-fixture56.log"
e=0; n=0; for f in "$T/$A"/fixture56/*; do b=${f##*/}
  n=$((n+1)); cmp -s "$f" <(fr "$J/11-fixture56/$b") || { echo "ÉCART $b"; e=$((e+1)); }; done; echo "fixture56 : écarts=$e / $n"
cat "$J/11-fixture56/f06.err" "$J/11-fixture56/f06.code"; wc -c < "$J/11-fixture56/f06.depots"
```
Attendu (Mac, `attendu/fixture56/`, identique à `env-60-scion/fixture56-apres/` au nom de la
base près) : `08a1460`, propre ; `code=0` ; **écarts=0 / 76** après `fr()` ; f06 : code 2, message
de `git clone -b nope`, `.depots` vide (aucun clone) ; f01 à f04 et f10 : `git clone -b master …`
(écart accepté au PA-108). Le classifieur décide de `switch` et de `fixture.py` (relevé).

### 11.3 pytest de lepton-tools

Par la session, règle `allow`, forme exacte (sans redirection, sans `TMPDIR=` ; le journal est
écrit par `--junitxml`) :
```bash
~/lepton-tools-dev/venv-test/bin/pytest -q -rs -p no:cacheprovider --basetemp ~/tmp-pytest/env-61 --junitxml ~/env-61-journaux/11-pytest.xml
```
Puis :
```bash
cd "$T"
python3 -I -c 'import sys,xml.etree.ElementTree as E; s=E.parse(sys.argv[1]).getroot().find("testsuite"); print({k:s.get(k) for k in ("tests","failures","errors","skipped","time")})' "$J/11-pytest.xml"
for m in test_proteger_trunk test_garde_ask test_supprimer_essai test_milestone3; do echo "$m $(grep -o "classname=\"tests.$m\"" "$J/11-pytest.xml" | wc -l)"; done
~/lepton-tools-dev/venv-test/bin/python -m pip show lepton | grep -i -E '^(version|location|editable)'
git -C "$T" status --short | head -5
```
Attendu (Mac, 2026-11-17, Python 3.11.5, scion 0.6.3.2) : **508 passed**, 0 échec, 0
erreur ; `test_proteger_trunk` 118, `test_garde_ask` 46, `test_supprimer_essai` 52, `test_milestone3` 43 (8 min 59) ; lepton en mode éditable depuis `$T` ; lepton-tools propre (hors
rapport). Un test ignoré ou en échec : relever son nom et son message, le relancer seul une fois
(`~/lepton-tools-dev/venv-test/bin/pytest -q -rs -p no:cacheprovider --basetemp
~/tmp-pytest/env-61 <test>`), consigner les deux résultats ; pas de correction.

## 12. Reconstructions et commande de miroir (C6)

PA-109 : reconstruction maintenue, bien qu'aucune source compilée ne change.

### 12.1 Reconstructions

Périmètre : host et les 16 presets croisés (QEMU : construction, fumée, banc KAL ; cartes :
construction et capture seulement, **aucun flash**), dans `$R53` regreffé au §9. `$R53` garde le
chemin d'`env-53-debian` : les chaînes `__FILE__` des presets FreeRTOS sont celles de l'oracle de
référence. Commande longue (≈ 4 min en R57-1) : `AVANCEMENT` au lancement.

```bash
cd "$T" && git switch -c devenv/env-61-debian devenv/env-61
scripts/oracle/rejouer-oracle.sh ~/lepton-tools-dev/essais/env-53-debian doc/devenv/rapports/oracles/env-61-debian --qemu qemu-mps2-an386-embos --qemu qemu-mps2-an386-embos-soft --qemu qemu-mps2-an386-freertos --qemu qemu-mps2-an386-freertos-soft --qemu qemu-mps2-an500-embos --qemu qemu-mps2-an500-freertos --carte nucleo-f429zi-embos --carte nucleo-f429zi-freertos --carte nucleo-f439zi-embos --carte nucleo-f439zi-freertos --carte nucleo-wl55jc1-embos --carte nucleo-wl55jc1-freertos --carte samd21-xplained-pro-embos --carte samd21-xplained-pro-freertos --carte stm32f746g-disco-embos --carte stm32f746g-disco-freertos > ~/env-61-journaux/12-rejouer.log 2>&1; echo "code=$?" >> ~/env-61-journaux/12-rejouer.log
```
Puis :
```bash
cd "$T"; O=doc/devenv/rapports/oracles
tail -25 "$J/12-rejouer.log"
grep -h "tests passed" $O/env-61-debian/*/ctest.log $O/env-61-debian/*/banc-kal.log
grep -h "peripheriques" $O/env-61-debian/qemu-mps2-an386-*/banc-kal.log
python3 -I "$T/$LI" "$R53/trunk" > /dev/null; find "$R53/trunk" -name __pycache__ | wc -l
```
Attendu : code 0 ; host ctest 7/7 ; 16 presets construits ; fumée réussie ; banc QEMU identique à
R57-1 : an386 20/20, an386 soft 16/16, an500 19/19 ; `qemu-mps2-an386.peripheriques` **Passed**
dans les 4 `banc-kal.log` an386 ; trunk sans fichier régulier, lien cassé ni `__pycache__`.

### 12.2 Comparaisons

```bash
cd "$T"; O=doc/devenv/rapports/oracles
norm() { grep -E '^(section|symbole)' "$1" | sed -E 's/ \[.*$//; s/ +: /: /' | grep -v -E '^section [^:]*: \.debug_' | LC_ALL=C sort; }
diff -q $O/env-57-debian/host/mklepton-empreintes.sha256 $O/env-61-debian/host/mklepton-empreintes.sha256 && echo "mklepton = R57-1"
diff -q $O/env-52-apres/host/mklepton-empreintes.sha256 $O/env-61-debian/host/mklepton-empreintes.sha256 && echo "mklepton = Mac env-52-apres"
for p in $(ls $O/env-61-debian | grep -v -e host -e ctest-N -e compilation -e '\.log$'); do
  python3 scripts/oracle/comparer-oracle.py $O/env-57-debian/$p $O/env-61-debian/$p > "$J/12-cmp-R57-$p.txt" 2>&1; a=$?
  python3 scripts/oracle/comparer-oracle.py $O/env-52-apres/$p $O/env-61-debian/$p > "$J/12-cmp-Mac-$p.txt" 2>&1; b=$?
  echo "$p comparer_R57-1=$a comparer_Mac=$b hors_debug=$(norm $J/12-cmp-R57-$p.txt | wc -l)"
done | tee "$J/12-bilan.txt"
```
Attendu :
- mklepton : empreintes identiques à `env-57-debian` et à `env-52-apres` ;
- `comparer_R57-1` **0** pour les **16 presets**, `hors_debug=0` (aucun écart admis) ;
- `comparer_Mac` : informatif (1 attendu partout, chaînes différentes).

Un `comparer_R57-1` non nul : écart à exposer, avec l'extrait du `12-cmp-R57-<preset>.txt` ; si
seules des sections `.debug_*` changent, le dire (`hors_debug=0`) ; pas de correction.

### 12.3 Commande de miroir, à blanc

```bash
scion mirror-sync --dry-run -v ~/lepton-tools-dev/essais/env-53-debian > ~/env-61-journaux/12-mirror-sync.log 2>&1; echo "code=$?" >> ~/env-61-journaux/12-mirror-sync.log
```
Puis :
```bash
cd "$T"
grep -E 'référence\(s\) à envoyer|signalement' "$J/12-mirror-sync.log"; tail -1 "$J/12-mirror-sync.log"
python3 -I "$T/$C" "$R53" "$T/$A50/trunk-liens.txt" "$J/12-controle-R53" | tail -1
```
Attendu (R57-1) : code 0 ; 8 lignes `miroir … : 0 référence(s) à envoyer, 0 signalement(s)` ; trunk
de `$R53` `CONFORME`. Une référence « à envoyer » n'est admise que si une publication amont
postérieure au 2026-11-13 l'explique : la relever, puis relever la référence de l'amont
(`git ls-remote https://github.com/STMicroelectronics/<nom>.git`), sans arrêt. Un signalement :
écart à exposer. Jamais sans `--dry-run`.

## 13. Cartes (C7)

Écarté au PA-109 : ni binaire, ni flash, ni sonde ne changent. Aucune commande OpenOCD.

## 14. Nettoyage de la VM (C8)

Après le commit du rapport (§15) seulement. Relevé par la session :
```bash
du -sh "$S" "$D59" "$D60" "$SS" "$E/env-61-fixture" ~/env-57-journaux ~/tmp-pytest/env-57 2>&1
```
Puis, par la session, règle `allow` :
```bash
scripts/supprimer-essai.sh ~/lepton-tools-dev/essais/env-61-essai ~/lepton-tools-dev/essais/env-61-depot59 ~/lepton-tools-dev/essais/env-61-depot60 ~/lepton-tools-dev/essais/env-61-seed-scions ~/lepton-tools-dev/essais/env-61-fixture ~/env-57-journaux
```
Puis la session vérifie l'absence (`ls -d …`) et le consigne. Conservés : `$U`, `$E13`, `$C5`
(regreffés au §9), `$R53`, `$J`, `~/tmp-pytest`. Périmètre validé au PA-109.

## 15. Critères et rapport

| Critère | Attendu |
| --- | --- |
| C1 Versions | `git ls-remote` = Mac (§5) ; `settings.json`, hook, enveloppe = Mac ; Claude Code relevé ; git 2.47.3 ; scion 0.6.3.2 par `install-debian.sh` (défaut `SCION_REF`) ; lepton `pipx` code 0, `scion 0.6.3.2 (requis ≥ 0.6.2.0)`, correction D17 présente ; extension 0.5.2, `install-vscodium.sh` `changements 0` ; chaîne relevée |
| C2 D19, D20, G2 | réglages utilisateur relus en entier, bloc `allow` = PA-103 ; U1 à U3 par la règle utilisateur, sans effet ; F1, F3, F6 par la règle, F2, F7 relevés ; A1 invite (règle `ask`), A2, A3 invites (hook G2), toutes refusées ; H1 hook ; `pipx install --force` par la règle du dépôt ; `graft-update` ×4 sur invite confirmée ; `git clone` de seed.scions et pytest par la règle ; aucune cible créée ni supprimée à tort |
| C3 Regreffes | `$U`, `$E13` (et `$R53`, pour C6) : code 0, seul le noyau avance (ed2a41f → dfc960b), aucun clone, journal = Mac, liens inchangés (3889), `CONFORME` (attendu de R50-1), clones tiers 0 / 16, `clones = Mac`, `check` 0, espace = avant ; `$C5` : noyau seul, 3059 liens inchangés, `check` 0 |
| C4 D17 | §10 : `classer = Mac` ; écarts=0 / 528 ; états = départ |
| C5 D18, pytest | §11.1 : l01 à l03 code 2, aucun clone laissé, écarts=0 / 15 ; §11.2 : fixture écarts=0 / 76, f06 sans clone ; §11.3 : pytest 508 passed |
| C6 Constructions, miroir | host ctest 7/7 ; 16 presets construits ; QEMU fumée et banc 20/20, 16/16, 19/19, `peripheriques` ×4 ; mklepton = `env-57-debian` = `env-52-apres` ; `comparer_R57-1` 0 pour les 16 presets ; `mirror-sync --dry-run` : code 0, 8 miroirs, 0 à envoyer (ou expliqué par l'amont), 0 signalement ; rien envoyé |
| C7 Cartes | écarté (PA-109) |
| C8 Nettoyage | `$S`, `$D59`, `$D60`, `$SS`, `essais/env-61-fixture`, `~/env-57-journaux` supprimés par l'enveloppe ; absents |

Avant le commit, relevé final des décisions (toute la session) :
```bash
cd "$T"; F=$(ls -t ~/.claude/projects/*lepton-tools-dev-lepton-tools/*.jsonl | head -1)
python3 -I "$T/$DEC" "$F" > "$J/15-decisions.tsv"; wc -l < "$J/15-decisions.tsv"
```

Rapport `doc/devenv/rapports/env-61-debian.md` sur `devenv/env-61-debian`, avec :
- l'hôte, les versions et la session (répertoire de travail, Claude Code, réglages relevés) ;
- la table des critères ;
- C2 : le contenu de `~/.claude/settings.json` (D19) ; la table des commandes et décisions
  (extrait de `15-decisions.tsv` : U1 à U3, F1 à F7, A1 à A3, H1, `pipx install`, `graft-update`
  ×4, `git clone`, pytest, push) ; le motif des invites d'A2 et d'A3 ;
- la table des presets : construction, fumée, banc KAL, `comparer_R57-1`, `comparer_Mac` ;
- C3 : les quatre bilans, les lignes `clones.txt` après, `ignorecase`, tailles ;
- C4, C5 : bilans `écarts=…`, relevés différents (informatifs), codes, lignes ramenées par `fr()` ;
- pytest, miroir, nettoyage ;
- les écarts et constats ;
- le journal des messages §2bis (ID, date, résumé, remis ou non) ;
- ce qui n'a pas été fait.

Sous `doc/devenv/rapports/env-61-debian/` : `15-decisions.tsv` (chemin personnel remplacé par
`<HOME>`), `settings-utilisateur.json` (sortie du §8.1), `10-classer.tsv`, `10-c4/`, `11-c5/`,
`11-fixture56/`, `11-pytest.xml`, et pour chaque rootstock du §9 `<nom>-bilan.txt`,
`<nom>-graft-update.log`, `<nom>-tiers-apres/clones.txt` ; l'oracle
`doc/devenv/rapports/oracles/env-61-debian/`. Commit sur `devenv/env-61-debian` (créée au §12.1),
puis `QUESTION` à l'utilisateur pour le push (PA-P ; la commande `git push origin
devenv/env-61-debian` fait paraître une invite), puis le §14, puis `FIN-*`.
