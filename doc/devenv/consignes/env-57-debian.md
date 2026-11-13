# Consigne — session Claude Code sur la VM Debian — ENV-57 (validation Debian groupée)

Fichier autonome : avec `ORCHESTRATION.md` §2bis, il suffit à conduire la session VM. Rédigé le
2026-11-13 par la session Mac `lepton-tools-30` (tâche 1 d'ENV-57), repris de
`consignes/env-53-debian.md`. À valider par l'utilisateur au PA-101. Son texte est envoyé tel quel
dans l'ordre `R57-1`.

## 0. Préalable, avant l'ordre (utilisateur) — PA-101

Les réglages du dépôt sont lus par une session lancée dans `$T`. Avant l'envoi de `R57-1`,
l'utilisateur, sur la VM :
1. dans un terminal :
   ```bash
   cd ~/lepton-tools-dev/lepton-tools && git status --short && git fetch origin && git switch devenv/env-57 && git merge --ff-only origin/devenv/env-57 && git log --oneline -1
   ```
2. ferme la session Claude Code de la VM et en ouvre une nouvelle **dans ce répertoire**, en mode
   auto, avec Remote Control ; il approuve le dossier si Claude Code le demande ;
3. communique à la session Mac le nom de la nouvelle session (`ListAgents`), à qui l'ordre est
   envoyé.

## 1. Objet

Valider sur Debian x86_64 l'état publié après ENV-54, ENV-55 et ENV-56 :
- **D16** (ENV-54) : règles de permission de Claude Code dans `.claude/settings.json` du dépôt
  (versionné, commun au Mac et à la VM). `ask` : `scion graft-update`, `scion seed-update`,
  `git push`. `allow` : `scripts/supprimer-essai.sh`, `pipx install --force
  ~/lepton-tools-dev/lepton-tools`, `git clone file://…` et `git clone
  https://github.com/lepton-distribution/…`, pytest par `~/lepton-tools-dev/venv-test/bin/pytest`.
  `deny` : options dangereuses de `git clone`. Le hook `proteger-trunk.py` est inchangé ;
- **D13** (ENV-55) : lepton normalise `file:///abs`, `file:/abs` et `FILE:…` en
  `file://localhost/abs` ;
- **D14** (ENV-56) : scion **0.6.3.1** ne laisse plus de répertoire dans `depots/` après un clonage
  en échec ;
- regreffe de `$U`, `$E13` et `$C5` : seul le clone noyau avance (58e421e → **ed2a41f** : scripts
  d'installation et documentation, hors de `scion/`). Aucun lien ne change.

**Pas de cartes, pas de reconstruction** dans cette session (PA-101) : aucune source compilée ne
change. Aucune écriture flash.

Références publiées (toutes poussées) :

| Dépôt (`https://github.com/lepton-distribution/…`) | Référence | Commit | En R53-1 |
| --- | --- | --- | --- |
| `lepton-tools` | `devenv/env-57` (cette consigne ; code identique à `main` 6b6b1d6) | tête après `fetch` | 087dd49 (`devenv/env-53`) |
| `seed.scions` | tag `0.6.3.1` | **c51ee1a** (`master` d650414) | tag `0.6.3.0` 87dc108 |
| `lepton-original-tree.scions` (noyau) | `master` | **ed2a41f** | 58e421e |
| graine `lepton-seed.scions`, 12 autres greffons, 8 miroirs | | inchangés | = |

Relevé du Mac : `rapports/env-57-mac/ls-remote-mac.txt` (script `env-57-mac/ls-remote.sh`).

Références Mac (`rapports/env-57-mac.md` §1, `rapports/env-57-mac/attendu/`) :
- liste `chemin -> cible` : `rapports/env-50-mac/attendu/trunk-liens.txt` (3889, inchangée depuis
  R50-1, revérifiée sur `<ROOTSTOCK>` le 2026-11-13) ; projetés : `env-50-mac/attendu/projetes.txt`
  (629) ; clones tiers : `rapports/env-53-mac/attendu/clones/`, `clones-rootstock-mac.txt` ;
- C3 : `attendu/c3/` (regreffe d'`essais/env-13-vierge`, même état que `$U` et `$E13`) ;
- C4 : `attendu/c4/` (D13, `rapports/env-55-url-file/essai.sh` sur une copie d'`essais/env-11/qemu`
  du Mac, scion 0.6.3.1) ;
- C5 : `attendu/c5/` (D14, `rapports/env-56-scion/essai.sh`, même copie).

Référence Debian : `rapports/env-53-debian.md`.

La session VM ne développe pas : elle exécute, constate et rapporte.

## 2. Ce que la session VM peut faire, et ne fait pas

| Autorisé | Interdit |
| --- | --- |
| `git fetch` / `switch` / `merge --ff-only` de `$T` (`devenv/env-57`) et du clone noyau `$K` (`master`) | Modifier `DEVENV-STATUS.md`, `ORCHESTRATION.md`, `SPECIFICATION.md`, `handoff/*.md`, les consignes, `rapports/env-57-mac*`, `.claude/` |
| Installations du §6 (`sudo` sans mot de passe sur la VM), dans les formes écrites | Toute autre commande `sudo`, `pip install` hors de `venv-test`, `codium --install-extension` hors `install-vscodium.sh` |
| `scion graft-update` de `$U`, `$E13`, `$C5` (§9), dans la forme écrite : l'invite de Claude Code est confirmée par l'utilisateur | `graft-update` d'un autre rootstock ; tout `seed-update` ; toute écriture dans les clones de `$U`, `$E13`, `$C5` |
| Lectures dans `$U`, `$E13`, `$C5`, `$R53`, `$P11` ; `lepton check` / `generate` / `seed status` dans `$U`, `$E13`, `$C5` | Écrire un fichier régulier dans un `trunk/` ou sous `depots/tiers/` (le hook refuse) ; corriger quoi que ce soit |
| Créer `$S`, `$D` (§7), `essais/env-57-clone`, `essais/env-57-clone-local` (§8) et y tout faire, `seed add` / `seed remove` compris | `git config` (même en lecture) et `git sparse-checkout` dans un clone de `depots/tiers/` : relever par `releve-clones.sh` |
| `scion mirror-sync --dry-run` dans `$R53` (§12) | `mirror-sync` sans `--dry-run` ; tout envoi vers un miroir |
| Les contrôles négatifs du §8 (cibles absentes) | Toute écriture flash, toute commande OpenOCD ; modifier la configuration réseau de la VM |
| Suppressions par `scripts/supprimer-essai.sh` (§8, §14) | `rm -rf` direct, hors du contrôle N3 (§8, cible absente) |
| Créer `devenv/env-57-debian` (depuis `devenv/env-57`) ; y écrire `doc/devenv/rapports/env-57-debian.md` et `doc/devenv/rapports/env-57-debian/` | Commiter sur une autre branche |
| `git push origin devenv/env-57-debian` **après accord explicite de l'utilisateur** (PA-P ; invite `ask`) | Pousser toute autre branche |

Règles des consignes VM (ORCHESTRATION §2bis, amendé en ENV-54) :
- **Commandes soumises aux règles de `.claude/settings.json`.** Chaque commande est écrite dans la
  forme couverte par sa règle. Essais du Mac (`rapports/env-57-mac.md` §1.5) :
  - une redirection vers un fichier (`> f 2>&1`) fait sortir une commande de sa règle `allow` : elle
    va au classifieur. Les commandes `allow` sont donc écrites **sans redirection** : leur sortie se
    lit dans le résultat de l'outil et se reporte au rapport ; pytest écrit son journal par
    `--junitxml` ;
  - une règle `ask` vaut avec ou sans redirection : l'invite paraît, l'utilisateur la confirme
    (ou la refuse, contrôles N4 et N5) ;
  - pas de variable ni d'affectation en tête (`TMPDIR=…`) ; une commande simple par appel pour les
    commandes couvertes.
- **Refus.** Toute commande refusée (classifieur, invite, hook) n'est jamais contournée :
  `AVANCEMENT` avec la commande exacte et la décision, l'utilisateur la lance s'il le décide, la
  session vérifie l'effet et le consigne. Seuls les refus attendus du §8 (N4 à N7) ne demandent rien
  à l'utilisateur, sinon de refuser les invites N4 et N5.
- **Refus d'une invite.** Il interrompt le tour de la session (constat d'ENV-54). L'utilisateur
  relance par un message dans la session VM (`reprendre R57-1 au §8, contrôle N5`, par exemple).
- **Régénérer avant de relever** : tout relevé « avant » d'un fichier généré suit immédiatement la
  commande qui le produit (`regreffer-essai.sh avant` le fait).
- **Branche des clones d'un rootstock existant** : relevée au §5 pour `$U`, `$E13`, `$C5`. scion
  refuse lui-même un clone hors de sa version déclarée ; un tel refus reste un écart à exposer.
- **scion avant tout essai de D14** : aucun essai du §10 ni du §11 avant que `scion version` donne
  0.6.3.1 (§6). Avec 0.6.3.0, le défaut D14 demeure.

Tout écart au plan, toute erreur non prévue : s'arrêter, exposer (`AVANCEMENT` ou `QUESTION`),
attendre.

## 3. Communication (ORCHESTRATION §2bis)

- Session principale : `lepton-tools-30` (session Mac). Répondre à l'adresse `from` du message
  d'ordre.
- ID : `R57-1`, repris tel quel : `[ACCUSÉ R57-1] ENV-57 — …`, `[AVANCEMENT R57-1] …`,
  `[QUESTION R57-1] …`, `[FIN-SUCCÈS R57-1] …` ou `[FIN-ÉCHEC R57-1] …`.
- `ACCUSÉ`, avant toute commande autre que les lectures du §5. Il contient :
  - l'ordre reformulé en une phrase ;
  - le nom de la session VM et son répertoire de travail ;
  - la tête réelle de `devenv/env-57` ; l'empreinte de `.claude/settings.json` ;
  - les résultats de `git ls-remote` du §5 ;
  - les branches et têtes des clones de `$U`, `$E13` et `$C5` ;
  - les étapes prévues (§6 à §15) et les écarts déjà visibles.
- `AVANCEMENT` : avant chaque commande soumise à une invite (§9, §8 N4 et N5, push), avant toute
  action demandée à l'utilisateur (§14), à chaque refus non prévu, après chacun des §6 à §12, et à
  chaque arrêt.
- `FIN-SUCCÈS` / `FIN-ÉCHEC` : résultat par critère du §15, commits et branche (poussée ou non),
  chemin du rapport, versions relevées, écarts, ce qui n'a pas été fait.
- **Remise en échec** (§2bis) : un envoi en erreur (ECONNRESET, « bridge ID is stale ») est renvoyé
  une fois, à l'identique. Si le second envoi échoue, le message entier est consigné dans
  `~/env-57-journaux/0-messages-R57-1.md` et au §Messages du rapport, avec la mention « non remis ».
  La session l'annonce à l'utilisateur, qui le relaie à la session Mac. Un message relayé par
  l'utilisateur et portant l'ID `R57-1` vaut message reçu.

## 4. Journaux et variables

```bash
mkdir -p ~/env-57-journaux
J=~/env-57-journaux
T=~/lepton-tools-dev/lepton-tools
K=~/lepton-tools-dev/lepton-noyau
E=~/lepton-tools-dev/essais
U=$E/env-28-debian
E13=$E/env-13-debian
C5=$E/env-53-c5
R53=$E/env-53-debian
P11=$E/env-11/qemu
S=$E/env-57-essai
D=$E/env-57-depot
AB=$E/env-57-absent.git
G=https://github.com/lepton-distribution
X=doc/devenv/rapports/env-57-mac
A=$X/attendu
Y=doc/devenv/rapports/env-53-mac
A50=doc/devenv/rapports/env-50-mac/attendu
C=doc/devenv/rapports/env-43-mac/controler-trunk.py
LI=$Y/liens.py
IC=$Y/inventaire-clones.sh
RG=$X/regreffer-essai.sh
DEC=$X/decisions.py
```
`$AB` n'existe pas et ne doit jamais être créé : c'est l'origine absente des essais. Les commandes
non couvertes par une règle portent leur journal (`> "$J/<étape>.log" 2>&1; echo "code=$?" >> …`).
Les boucles s'écrivent en bash. Ne pas faire `cd` dans un `trunk/` : revenir à `$T` (le hook juge
le répertoire courant).

Outils de la session Mac, en lecture seule, utilisables tels quels sur Debian :
- `env-53-mac/` : `releve-clones.sh`, `inventaire-clones.sh`, `liens.py` (formes de
  `consignes/env-53-debian.md` §4) ;
- `env-57-mac/regreffer-essai.sh avant|apres <rootstock> <journaux>` : relevés avant et après une
  regreffe (inventaire, liens, `controler-trunk.py` contre les liens d'avant, clones tiers contre
  `env-53-mac/attendu/clones/`, `check`, `generate`, espace), bilan `<journaux>/<nom>-bilan.txt` ;
  le `graft-update` est lancé à part par la session, entre les deux phases ;
- `env-57-mac/decisions.py <journal .jsonl> [--motif <texte>]…` : décisions de permission des
  appels Bash de la session (TSV : heure UTC, décision, source, `reasonType`, `ruleSource`,
  commande) ;
- `env-55-url-file/essai.sh` (D13) et `env-56-scion/essai.sh` (D14) : essais rejoués aux §10 et
  §11 ; chaque cas est relevé (`.cmd`, `.out`, `.err`, `.code`) et l'état du rootstock est comparé
  au départ (`<cas>.etat`).

## 5. Vérifications préalables (lecture seule) — C1

```bash
pwd; printenv CLAUDE_PROJECT_DIR; claude --version 2>&1 | head -1
git -C "$T" status --short | head -5; git -C "$T" branch --show-current; git -C "$T" log --oneline -1
git -C "$T" fetch origin && git -C "$T" status -sb | head -1
sha256sum "$T/.claude/settings.json" "$T/.claude/hooks/proteger-trunk.py" "$T/scripts/supprimer-essai.sh"
ls -la ~/.claude/settings.json ~/.claude/settings.local.json "$T/.claude/settings.local.json" 2>&1
python3 -I -c 'import json,sys
for f in sys.argv[1:]:
    try: d=json.load(open(f))
    except OSError: continue
    p=d.get("permissions",{}); print(f, {k:len(v) for k,v in p.items() if isinstance(v,list)}, "defaultMode", p.get("defaultMode"))' ~/.claude/settings.json "$T/.claude/settings.local.json"
ls -t ~/.claude/projects/*lepton-tools-dev-lepton-tools/*.jsonl 2>&1 | head -2
uname -sm; cat /etc/debian_version; uname -r; id -un; git --version
scion version | tail -1; lepton --version; printenv SCION_REF SCION_SPEC
arm-none-eabi-gcc --version | head -1; cmake --version | head -1; ninja --version; qemu-system-arm --version | head -1; python3 --version; codium --version | head -1
command -v shasum realpath rsync tar; ls -d ~/tmp-pytest ~/lepton-tools-dev/venv-test/bin/pytest 2>&1
df -h ~ /tmp | tail -2
for Z in "$S" "$D" "$AB" "$E/env-57-clone" "$E/env-57-clone-local" "$E/env-57-absent"; do test -e "$Z" && echo "ARRÊT : $Z existe déjà"; done
cd "$T" && bash $X/ls-remote.sh > "$J/5-ls-remote.txt" 2>&1; diff <(grep -v '^lepton-tools ' $X/ls-remote-mac.txt) <(grep -v '^lepton-tools ' "$J/5-ls-remote.txt") && echo "têtes publiées = Mac"
for Z in "$U" "$E13" "$C5"; do
  echo "== $Z"
  git -C "$Z"/depots/lepton-seed*/* log --oneline -1
  grep -v '^#' "$Z"/trunk/.scion.grafted.list | grep -c .
  bash "$T/$IC" "$Z" | tee "$J/5-clones-$(basename $Z).txt"
  python3 -I "$T/$LI" "$Z/trunk" > /dev/null
  ls -d "$Z"/depots/tiers/*/* 2>&1; du -sk "$Z"/depots/tiers 2>&1
done
ls -d "$R53" "$P11" ~/env-53-journaux 2>&1; ls -d "$E"/*/ "$E"/env-11/*/ 2>&1
```
Attendu :
- répertoire de travail `$T` (`/home/lepton-user/lepton-tools-dev/lepton-tools`) ; lepton-tools
  propre, sur `devenv/env-57`, à jour avec `origin/devenv/env-57` (préalable du §0) ;
- `.claude/settings.json` `b01ad557…d235`, `proteger-trunk.py` `d7d719f1…fdc`,
  `supprimer-essai.sh` `04323a00…0e15` (Mac) ; réglages utilisateur et locaux relevés (une règle
  utilisateur s'ajoute à celles du dépôt : la consigner) ;
- `têtes publiées = Mac` ; git **2.47.3** ; scion **0.6.3.0** (avant installation) ;
  `lepton 0.1.0`, `scion 0.6.3.0 (requis ≥ 0.6.2.0)` ; `SCION_REF` et `SCION_SPEC` vides ;
- chaîne APT de R53-1 : arm-none-eabi-gcc 14.2.1, cmake 3.31.6, ninja 1.12.1, QEMU 10.0.13,
  Python 3.13.5, codium 1.135.06055 ; `shasum`, `realpath`, `tar` présents ; `~/tmp-pytest` et
  `venv-test/bin/pytest` présents ;
- `$U` et `$E13` (état laissé par R53-1), chacun : graine 15740f9 ; **23 entrées** ; 14 lignes
  d'inventaire, la graine sur `original-tree`, 13 clones `<clé>/master` sur `master`, amont réglé,
  `modifs=0`, noyau **58e421e** ; `liens=3889 casses=0 reguliers=0` ; 8 clones tiers
  (≈ 108 760 Ko) ;
- `$C5` : graine `env11` ; `liens=3059 casses=0 reguliers=0` ; noyau 58e421e, an386 10a8889 ;
  `salut` sans amont, `modifs=2` (état d'origine de la VM) ; clones F7 conservés de R53-1 ;
- `$R53`, `$P11`, `~/env-53-journaux` présents.

Arrêts :
- un chemin du `for` initial existe ;
- lepton-tools non propre, hors de `devenv/env-57`, ou `settings.json` différent du Mac ;
- un commit publié diffère du Mac ;
- graine de `$U`, `$E13` ou `$C5` modifiée ; un clone de greffon publié hors de sa branche, sans
  amont ou modifié ;
- `shasum`, `realpath` ou `tar` absent ; moins de 8 Go libres dans `~`.

Pas des arrêts, à consigner : une version de la chaîne différente de R53-1 ; un répertoire de
travail autre que `$T` (les règles du dépôt ne seraient pas lues : C2 le montrera, l'exposer).

## 6. Installation de scion 0.6.3.1 et de lepton (C1)

D'abord, par la session :
```bash
git -C "$K" status --short | head -5
git -C "$K" fetch origin && git -C "$K" switch master && git -C "$K" merge --ff-only origin/master && git -C "$K" log --oneline -1
grep -n '^SCION_REF=' "$K/scripts/install-debian.sh" "$T/scripts/install-vscodium.sh"
grep -n 'SCION_MIN_VERSION =' "$T/lepton/__init__.py"; grep -n '"version"' "$T/extension/package.json"; ls "$T"/extension/dist/lepton-0.5.2.vsix
```
Attendu : clone noyau propre, à **ed2a41f** (58e421e avant) ; `SCION_REF="${SCION_REF:-0.6.3.1}"`
(noyau) et `SCION_REF="0.6.3.1"` (lepton-tools) ; `SCION_MIN_VERSION = (0, 6, 2, 0)` ;
extension 0.5.2, `.vsix` présent.

Puis `AVANCEMENT`, et la session lance, une commande par appel, dans cet ordre :
1. scion (hors règle : classifieur ; accepté en R53-1) :
   ```bash
   bash ~/lepton-tools-dev/lepton-noyau/scripts/install-debian.sh --with-debug-tools > ~/env-57-journaux/6-install-debian.log 2>&1; echo "code=$?" >> ~/env-57-journaux/6-install-debian.log
   ```
   Il installe scion par `pipx install --force
   "git+https://github.com/lepton-distribution/seed.scions.git@0.6.3.1"` (défaut `SCION_REF`). En
   cas de refus : `AVANCEMENT` ; l'utilisateur lance la même ligne, ou seulement cette commande
   `pipx`, dans la session VM (`!` en premier caractère) ou dans un terminal.
2. lepton (règle `allow`, forme exacte, sans redirection) :
   ```bash
   pipx install --force ~/lepton-tools-dev/lepton-tools
   ```
   Sortie lue dans le résultat de l'outil et reportée au rapport.
3. VSCodium (hors règle) :
   ```bash
   bash ~/lepton-tools-dev/lepton-tools/scripts/install-vscodium.sh --lepton-clone ~/lepton-tools-dev/lepton-noyau > ~/env-57-journaux/6-install-vscodium.log 2>&1; echo "code=$?" >> ~/env-57-journaux/6-install-vscodium.log
   ```

Puis :
```bash
tail -3 "$J/6-install-debian.log"; grep -n -i 'scion' "$J/6-install-debian.log" | tail -5; tail -12 "$J/6-install-vscodium.log"
scion version | tail -1; lepton --version; codium --version | head -1
pipx list --short | grep -E '^(scion|lepton) '
codium --list-extensions --show-versions | LC_ALL=C sort > "$J/6-extensions.txt"; grep -E -i 'lldb|lepton|rtos-views|peripheral' "$J/6-extensions.txt"
```
Attendu : codes 0 ; `scion version: 0.6.3.1` ; `lepton 0.1.0`, `scion 0.6.3.1 (requis ≥ 0.6.2.0)` ;
`install-vscodium.sh` : `changements 0` ; `lepton-distribution.lepton@0.5.2`,
`vadimcn.vscode-lldb@1.12.3`, `mcu-debug.rtos-views@0.0.16`, `mcu-debug.peripheral-viewer@1.6.4`.

**Arrêt** si scion n'est pas 0.6.3.1 : ni §9, ni §10, ni §11.

## 7. Copie d'essai et dépôt présent (pour C2, C4, C5)

Avant toute regreffe de `$C5` (§9), pour que la copie parte de l'état de celle du Mac (noyau
58e421e, 3059 liens) :
```bash
cd "$T"
mkdir "$S" && tar -C "$C5" --exclude=./build -cf - . | tar -C "$S" -xf -; echo "copie=$?"
python3 -I "$T/$LI" "$S/trunk" > "$J/7-liens-depart.txt"
lepton check -C "$S" > "$J/7-check.log" 2>&1; echo "code=$?" >> "$J/7-check.log"; tail -2 "$J/7-check.log"
lepton scion new env55lib --type bibliotheque --repo "$D" --no-seed --no-cmake -C "$S" > "$J/7-scion-new.log" 2>&1; echo "code=$?" >> "$J/7-scion-new.log"; cat "$J/7-scion-new.log"
git -C "$D" log --oneline; git -C "$S"/depots/lepton-seed/env11 status --short | wc -l
```
Attendu : `copie=0` ; `liens=3059 casses=0 reguliers=0` ; `check` code 0 ; `dépôt créé : …/env-57-depot
(lib/env55lib)`, code 0, un commit ; graine sans modification (0). La copie n'est pas régénérée par
`lepton generate` (la copie du Mac ne l'a pas été).

## 8. Règles de permission sur la VM (C2)

Toutes les commandes de ce paragraphe sont lancées par la session, **une par appel, telles
qu'écrites** (chemins littéraux, `lepton-user` compris). La décision de chacune est relevée à la
fin dans le journal de session. Catégories `pipx install` (§6.2), `scion graft-update` (§9) et
tests (§11) : relevées dans les paragraphes indiqués.

Acceptations attendues (règle `allow`, sans classifieur) :

| N° | Commande | Attendu |
| --- | --- | --- |
| P3 | `git clone https://github.com/lepton-distribution/lepton-bsp-qemu-mps2-an500.git ~/lepton-tools-dev/essais/env-57-clone` | code 0 |
| P4 | `git clone file:///home/lepton-user/lepton-tools-dev/essais/env-57-depot ~/lepton-tools-dev/essais/env-57-clone-local` | code 0, un commit |
| P5 | `scripts/supprimer-essai.sh ~/lepton-tools-dev/essais/env-57-clone ~/lepton-tools-dev/essais/env-57-clone-local` | code 0, « supprimé » ×2, absents |

Contrôles négatifs (cibles absentes ou protégées ; rien ne doit être supprimé ni écrit) :

| N° | Commande | Attendu |
| --- | --- | --- |
| N1 | `scripts/supprimer-essai.sh ~/lepton-tools-dev/essais/env-57-absent/../../absent-env57` | règle `allow` ; enveloppe : code 2, refus, rien supprimé |
| N2 | `scripts/supprimer-essai.sh ~/lepton-absent-env57` | règle `allow` ; code 2 |
| N2b | `scripts/supprimer-essai.sh -n ~/lepton-tools-dev/essais/env-28-debian` | règle `allow` ; code 2, « essai de référence protégé (env-28-debian) » |
| N3 | `rm -rf ~/lepton-tools-dev/essais/env-57-absent` | hors règle : classifieur (décision relevée) ; cible absente |
| N4 | `scion graft-update -v ~/lepton-tools-dev/essais/env-57-absent` | règle `ask` : invite ; **l'utilisateur la refuse** |
| N5 | `git -C ~/lepton-tools-dev/essais/env-57-absent push` | règle `ask` (`git * push`) : invite ; **l'utilisateur la refuse** |
| N6 | `git clone --upload-pack=true file:///absent ~/lepton-tools-dev/essais/env-57-x` | règle `deny` : refus sans invite |
| N7 | `touch ~/lepton-tools-dev/essais/env-57-essai/trunk/essai-hook` | hook `proteger-trunk.py` : refus |

Avant N4 : `AVANCEMENT` à l'utilisateur (refuser l'invite N4, puis relancer par « reprendre R57-1
au §8, N5 » ; de même pour N5, puis « reprendre R57-1 au §8, N6 »).

Après N7 :
```bash
cd "$T"
ls -d ~/lepton-tools-dev/essais/env-57-clone ~/lepton-tools-dev/essais/env-57-clone-local ~/lepton-tools-dev/essais/env-57-absent ~/lepton-tools-dev/essais/env-57-x ~/lepton-absent-env57 "$S/trunk/essai-hook" 2>&1
python3 -I "$T/$LI" "$S/trunk" | cmp - "$J/7-liens-depart.txt" && echo "liens de \$S = départ"
F=$(ls -t ~/.claude/projects/*lepton-tools-dev-lepton-tools/*.jsonl | head -1); echo "$F"
python3 -I "$T/$DEC" "$F" > "$J/8-decisions.tsv"; cut -c1-160 "$J/8-decisions.tsv" | grep -E 'git clone|supprimer-essai|rm -rf|graft-update|push|touch|pipx install|pytest'
```
Attendu, dans `8-decisions.tsv` (forme du Mac, `rapports/env-54-permissions.md` §10) :
- P3, P4, P5, N1, N2, N2b : `accept config subcommandResults` (règle du projet) ;
- §6.2 `pipx install` : `accept config rule` ou `subcommandResults` ;
- N3 : `accept` ou `reject`, `classifier` (informatif) ;
- N4, N5 : `rejet-invite` ; N6 : `reject … projectSettings` (règle `deny`) ; N7 : `reject hook hook` ;
- les 5 cibles absentes, `essai-hook` absent ; liens de `$S` = départ.

Une acceptation par le classifieur là où une règle est attendue (`reasonType` `classifier`) :
écart à exposer (règles non lues ou dossier non approuvé : le relever), sans arrêt. Une invite non
apparue pour N4 ou N5 : arrêt, `QUESTION` (la commande serait exécutée sans accord).

## 9. Regreffe de `$U`, `$E13` et `$C5` (C3)

Pour chaque rootstock `Z` de la liste `env-28-debian`, `env-13-debian`, `env-53-c5` :
1. par la session, depuis `$T` :
   ```bash
   bash "$T/$RG" avant ~/lepton-tools-dev/essais/<nom> "$J/regreffes"
   ```
2. `AVANCEMENT` (« invite à confirmer »), puis la session lance, telle quelle :
   ```bash
   scion graft-update -v ~/lepton-tools-dev/essais/<nom> > ~/env-57-journaux/regreffes/<nom>-graft-update.log 2>&1; echo "code=$?" >> ~/env-57-journaux/regreffes/<nom>-graft-update.log
   ```
   L'utilisateur confirme l'invite de Claude Code (PA-P accordé au PA-101 pour ces trois
   rootstocks).
3. par la session :
   ```bash
   cd "$T"
   bash "$T/$RG" apres ~/lepton-tools-dev/essais/<nom> "$J/regreffes"
   Z=~/lepton-tools-dev/essais/<nom>; L=$J/regreffes/<nom>-graft-update.log
   resume() { sed -e "s|$Z|<R>|g" -e "s|$HOME|<HOME>|g" "$1" | grep -v -E '^git |\(cwd=|^  |\.DS_Store|chemin\(s\) ignoré\(s\)|^code='; }
   grep -E 'feuilles liées|ignoré' "$L"
   ```
   et, pour `$U` et `$E13` seulement :
   ```bash
   diff "$T/$A/c3/graft-update-resume.txt" <(resume "$L") && echo "journal = Mac"
   python3 -I "$T/$C" "$Z" "$T/$A50/trunk-liens.txt" "$J/9-<nom>-controle" > "$J/9-<nom>-controle.log" 2>&1; echo "code=$?" >> "$J/9-<nom>-controle.log"; tail -3 "$J/9-<nom>-controle.log"
   normc() { sed -E 's/ ignorecase=[^ ]*//; s/ ko_hors_git=.*//' "$1"; }
   diff <(normc "$T/$Y/attendu/clones-rootstock-mac.txt") <(normc "$J/regreffes/<nom>-tiers-apres/clones.txt") && echo "clones = Mac (hors ignorecase et tailles)"
   ```

Attendu, `$U` et `$E13` (Mac, `essais/env-13-vierge`, `attendu/c3/env-13-vierge-bilan.txt`) :
- `graft-update code=0 ; avancés : 1 ; git clone : 0 ; extraction partielle : 0 ; conflit/refus : 0` ;
  `depots/lepton/original/master avancé : 58e421e -> ed2a41f` ; « 3889 feuilles liées » ; aucune
  ligne `.DS_Store` sur la VM ;
- `journal = Mac` : 82 lignes (avancée du noyau, projections, « répertoire extrait » des 8 clones
  tiers, déjà partiels) ;
- `clones : 1 ligne(s) changée(s)` (noyau) ; liens 3889 → 3889, ajoutés 0, retirés 0 ;
  `controler-trunk CONFORME code=0` contre les liens d'avant **et** contre l'attendu de R50-1 ;
- `tiers : 8 clone(s)`, extraits et `sparse-checkout` ≠ attendu : **0 / 16** ; `clones = Mac` ;
  `ignorecase` vide (relevé) ; tailles relevées ;
- `check code=0`, `generate` avant et après code 0, `espace diff=0` ; trunk sans fichier régulier ni
  lien cassé.

Attendu, `$C5` : un seul clone avancé (noyau 58e421e → ed2a41f) ; `salut` accepté (sans amont,
`modifs=2`, comme en R53-1) ; 3059 liens inchangés, `CONFORME` contre les liens d'avant ; les 2
clones tiers F7 conservés de R53-1 ne sont pas greffés, inchangés (extraits et `sparse-checkout`
≠ attendu : 0 / 4) ; `check` code 0 ; espace identique.

Un refus de scion (clone hors version, graine divergée) : écart à exposer, sans contournement.

## 10. D13 : formes d'origine de lepton (C4)

Sur `$S` (§7), avec scion 0.6.3.1 :
```bash
cd "$T"
bash doc/devenv/rapports/env-55-url-file/essai.sh "$S" "$D" "$AB" "$J/10-c4-brut" "$J/10-c4" > "$J/10-c4.log" 2>&1; echo "code=$?" >> "$J/10-c4.log"
grep -c 'état : $' "$J/10-c4.log"; grep 'état : .' "$J/10-c4.log"; grep -l 'rmdir\|≠ départ' "$J/10-c4"/*.etat
fr() { sed -e 's/: et que le dépôt existe\.$/: and the repository exists./' "$1"; }
e=0; n=0; for f in "$T/$A"/c4/*; do b=${f##*/}; case $b in *-status.out|depart.etat) continue;; esac
  n=$((n+1)); cmp -s "$f" <(fr "$J/10-c4/$b") || { echo "ÉCART $b"; e=$((e+1)); }; done; echo "c4 : écarts=$e / $n"
for b in $(cd "$T/$A/c4" && ls *-status.out); do diff "$T/$A/c4/$b" "$J/10-c4/$b" > /dev/null || echo "$b diffère (informatif)"; done | head -3
python3 -I "$T/$LI" "$S/trunk" | cmp - "$J/7-liens-depart.txt" && echo "liens de \$S = départ"
```
Attendu (Mac, `attendu/c4/`, `rapports/env-57-mac.md` §1.4) :
- 21 lignes `état : ` vides (a01 à a10, p01 à p10, s05 : chaque cas, annulation comprise, revient
  au départ) ; aucun `.etat` avec `rmdir` ni `≠ départ` : D14 corrigé, aucun résidu après un
  clonage en échec ;
- **écarts=0 / 231** relevés comparés (`.cmd`, `.out`, `.err`, `.code`, `.etat`, hors les 10
  `*-status.out` et `depart.etat`), après normalisation de la langue de git :
  - `file:///A`, `file:/A`, `FILE:///A` (a01, a03, a05, a09) : code 2, relevés identiques à
    `file://localhost/A` (a02) ;
  - `file:///P`, `file:/P`, `FILE:///P`, `FILE://localhost/P` (p01, p02, p05 à p07) : code 0,
    `env55lib ajouté (lepton@library-env55lib, master, file://localhost<P>)`, relevés identiques à
    p03 ; `seed remove --purge` code 0 ;
  - autres formes et s01 à s05 (scion seul) : identiques au Mac ;
- `*-status.out` : peuvent différer (commit de la graine `env11`, `salut`, noyau, dépôt `$D`) :
  informatif ;
- liens de `$S` = départ.

Un écart : relever le fichier et le `diff`, sans correction.

## 11. D14 : clonages en échec, pytest (C5)

### 11.1 Cas d'ENV-56

```bash
cd "$T"
bash doc/devenv/rapports/env-56-scion/essai.sh "$S" "$AB" "$J/11-c5-brut" "$J/11-c5" > "$J/11-c5.log" 2>&1; echo "code=$?" >> "$J/11-c5.log"
cat "$J/11-c5.log" | grep -E '^e0|état'; grep -l 'résidu' "$J/11-c5"/*.etat; cat "$J/11-c5/scion.txt"
fr() { sed -e 's/: et que le dépôt existe\.$/: and the repository exists./' "$1"; }
e=0; n=0; for f in "$T/$A"/c5/*; do b=${f##*/}; case $b in scion.txt|depart.etat) continue;; esac
  n=$((n+1)); cmp -s "$f" <(fr "$J/11-c5/$b") || { echo "ÉCART $b"; e=$((e+1)); }; done; echo "c5 : écarts=$e / $n"
python3 -I "$T/$LI" "$S/trunk" | cmp - "$J/7-liens-depart.txt" && echo "liens de \$S = départ"
find "$S/depots" -maxdepth 3 -type d -empty
```
Attendu (Mac, `attendu/c5/`) :
- codes : e01 2 ; e02a 0, e02b 2, e02c 0 ; e03a 0, e03b 2, e03c 0 ; e04 2 ; e05 2 ; e06 2 ;
- aucun `.etat` avec « résidu » ; e04 et e05 : « préexistant gardé » (répertoires préparés par le
  script, puis défaits) ; `scion.txt` : 0.6.3.1, venv pipx ;
- **écarts=0** sur 48 relevés (hors `scion.txt`, `depart.etat`) après normalisation de la langue de
  git ;
- liens de `$S` = départ ; `find -empty` : seuls les répertoires vides qui préexistaient dans `$C5`
  (les relever).

### 11.2 pytest de lepton-tools

Par la session, règle `allow`, forme exacte (sans redirection, sans `TMPDIR=` ; le journal est
écrit par `--junitxml`) :
```bash
~/lepton-tools-dev/venv-test/bin/pytest -q -rs -p no:cacheprovider --basetemp ~/tmp-pytest/env-57 --junitxml ~/env-57-journaux/11-pytest.xml
```
Puis :
```bash
cd "$T"
python3 -I -c 'import sys,xml.etree.ElementTree as E; s=E.parse(sys.argv[1]).getroot().find("testsuite"); print({k:s.get(k) for k in ("tests","failures","errors","skipped","time")})' "$J/11-pytest.xml"
grep -o 'classname="tests.test_proteger_trunk"' "$J/11-pytest.xml" | wc -l; grep -o 'classname="tests.test_supprimer_essai"' "$J/11-pytest.xml" | wc -l
~/lepton-tools-dev/venv-test/bin/python -m pip show lepton | grep -i -E '^(version|location|editable)'
git -C "$T" status --short | head -5
```
Attendu (Mac, 2026-11-13, Python 3.11.5, scion 0.6.3.1, 8 min 36) : **453 passed**, 0 échec, 0 erreur ;
hook 118 ; enveloppe 52 ; lepton en mode éditable depuis `$T` ; lepton-tools propre (hors rapport).
Un test ignoré ou en échec : relever son nom et son message, le relancer seul une fois
(`~/lepton-tools-dev/venv-test/bin/pytest -q -rs -p no:cacheprovider --basetemp
~/tmp-pytest/env-57 <test>`), consigner les deux résultats ; pas de correction.

## 12. Commande de miroir, à blanc (C6)

```bash
scion mirror-sync --dry-run -v ~/lepton-tools-dev/essais/env-53-debian > ~/env-57-journaux/12-mirror-sync.log 2>&1; echo "code=$?" >> ~/env-57-journaux/12-mirror-sync.log
```
Puis :
```bash
cd "$T"
grep -E 'référence\(s\) à envoyer|signalement' "$J/12-mirror-sync.log"; tail -1 "$J/12-mirror-sync.log"
python3 -I "$T/$C" "$R53" "$T/$A50/trunk-liens.txt" "$J/12-controle-R53" | tail -1
```
Attendu (R53-1) : code 0 ; 8 lignes `miroir … : 0 référence(s) à envoyer, 0 signalement(s)` ; trunk
de `$R53` `CONFORME`. Une référence « à envoyer » n'est admise que si une publication amont
postérieure au 2026-11-12 l'explique : la relever, puis relever la référence de l'amont
(`git ls-remote https://github.com/STMicroelectronics/<nom>.git`), sans arrêt. Un signalement :
écart à exposer. Jamais sans `--dry-run`.

Reconstruction des presets : écartée au PA-101 (aucune source compilée ne change ; liens prouvés
inchangés au §9).

## 13. Cartes (C7)

Écarté au PA-101 : ni binaire, ni flash, ni sonde ne changent. Aucune commande OpenOCD.

## 14. Nettoyage de la VM (C8)

Après le commit du rapport (§15) seulement. Relevé par la session :
```bash
du -sh "$S" "$D" ~/env-53-journaux "$P11"; ls -A "$E/env-11"
bash "$T/$IC" "$P11"; git -C "$P11"/depots/lepton-application/salut status --short 2>&1 | head
```
Puis, par la session, règle `allow` :
```bash
scripts/supprimer-essai.sh ~/lepton-tools-dev/essais/env-57-essai ~/lepton-tools-dev/essais/env-57-depot ~/env-53-journaux
```
Puis `AVANCEMENT` : `essais/env-11/qemu` est une référence de l'enveloppe, qui la refuse (essai du
Mac). D15 confie sa suppression à l'**utilisateur**, qui lance, s'il le confirme au vu du relevé
(`salut` modifié localement depuis ENV-10) :
```bash
rm -rf ~/lepton-tools-dev/essais/env-11/qemu
```
et, si `essais/env-11` est alors vide, `rmdir ~/lepton-tools-dev/essais/env-11`. La session
vérifie l'absence (`ls -d …`) et le consigne. Conservés : `$U`, `$E13`, `$C5` (regreffés au §9),
`$R53`, `$J`, `~/tmp-pytest`.

## 15. Critères et rapport

| Critère | Attendu |
| --- | --- |
| C1 Versions | `git ls-remote` = Mac (§5) ; `settings.json`, hook, enveloppe = Mac ; Claude Code relevé ; git 2.47.3 ; scion 0.6.3.1 par `install-debian.sh` (défaut `SCION_REF`) ; lepton `pipx` code 0, `scion 0.6.3.1 (requis ≥ 0.6.2.0)` ; extension 0.5.2, `install-vscodium.sh` `changements 0` ; chaîne relevée |
| C2 D16 | `8-decisions.tsv` : P3 à P5, N1, N2, N2b par la règle (`subcommandResults`) ; `pipx install` par la règle ; `graft-update` ×3 sur invite confirmée ; pytest par la règle ; N3 relevé ; N4, N5 invites refusées ; N6 `deny` ; N7 hook ; aucune cible créée ni supprimée à tort |
| C3 Regreffes | `$U`, `$E13` : code 0, seul le noyau avance (58e421e → ed2a41f), aucun clone, journal = Mac, liens inchangés (3889), `CONFORME` (attendu de R50-1), clones tiers 0 / 16, `clones = Mac`, `check` 0, espace = avant ; `$C5` : noyau seul, 3059 liens inchangés, `check` 0 |
| C4 D13 | §10 : écarts=0 ; formes `file:///`, `file:/`, `FILE:` = `file://localhost/` ; états = départ |
| C5 D14, pytest | §11.1 : aucun résidu, écarts=0 sur 48 ; préexistants gardés ; §11.2 : pytest 453 passed (hook 118, enveloppe 52) |
| C6 Miroir | `mirror-sync --dry-run` : code 0, 8 miroirs, 0 à envoyer (ou expliqué par l'amont), 0 signalement ; rien envoyé ; reconstruction écartée (PA-101) |
| C7 Cartes | écarté (PA-101) |
| C8 Nettoyage | `$S`, `$D`, `~/env-53-journaux` supprimés par l'enveloppe ; `essais/env-11/qemu` supprimé par l'utilisateur (D15) ; absents |

Rapport `doc/devenv/rapports/env-57-debian.md` sur `devenv/env-57-debian`, avec :
- l'hôte, les versions et la session (répertoire de travail, Claude Code, réglages relevés) ;
- la table des critères ;
- C2 : la table des commandes et décisions (extrait de `8-decisions.tsv`, plus `pipx install`,
  `graft-update` ×3, pytest, push) ;
- C3 : les trois bilans, les lignes `clones.txt` après, `ignorecase`, tailles ;
- C4, C5 : bilans `écarts=…`, relevés différents (informatifs), codes ;
- pytest, miroir, nettoyage ;
- les écarts et constats ;
- le journal des messages §2bis (ID, date, résumé, remis ou non) ;
- ce qui n'a pas été fait.

Sous `doc/devenv/rapports/env-57-debian/` : `8-decisions.tsv`, `10-c4/`, `11-c5/`,
`11-pytest.xml`, et pour chaque rootstock du §9 `<nom>-bilan.txt`, `<nom>-graft-update.log`,
`<nom>-tiers-apres/clones.txt`. Commit sur `devenv/env-57-debian`, puis `QUESTION` à l'utilisateur
pour le push (PA-P ; la commande `git push origin devenv/env-57-debian` fait paraître une invite),
puis le §14, puis `FIN-*`.
