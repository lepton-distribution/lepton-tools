# Consigne — session Claude Code sur la VM Debian — ENV-53 (validation Debian groupée)

Fichier autonome : avec `ORCHESTRATION.md` §2bis, il suffit à conduire la session VM. Rédigé le
2026-11-12 par la session Mac `lepton-tools-3b` (tâche 1 d'ENV-53), repris de
`consignes/env-50-debian.md`. Validé par l'utilisateur au PA-93 (2026-11-12), avec une précision
reportée au §2 : la session VM lance elle-même les commandes marquées « l'utilisateur lance ».
Son texte est envoyé tel quel dans l'ordre `R53-1`.

## 1. Objet

Valider sur Debian x86_64 l'état publié après ENV-51 et ENV-52 :
- installation de scion **0.6.3.0** (ENV-52, règle P-V7 : un clone distant de clé projetée n'extrait
  que les répertoires parents des fichiers projetés, au mode cône de `git sparse-checkout` ; un
  clone existant est converti par sa prochaine greffe) et de lepton (`main`, ENV-51 : le stderr de
  scion d'un appel réussi est relayé sur stderr, une ligne `scion: …` par ligne) ; extension
  Lepton 0.5.2 inchangée ;
- `scion graft-update` de deux rootstocks existants (`$U`, `$E13`), puis un rootstock neuf depuis
  la graine publiée. Depuis R50-1, seul le clone noyau avance (76f28bd → 58e421e : scripts
  d'installation et documentation, hors de `scion/`, rien de greffé). On attend donc :
  - **aucun** lien ajouté, retiré ni réorienté (3889 liens, 629 projetés) ;
  - les 8 clones tiers convertis en extraction partielle, avec les fichiers extraits du Mac ;
  - la VM distingue la casse des noms de fichiers, le Mac non : c'est ici que se prouve
    l'ensemble extrait (motifs de répertoires écrits par scion, comparés octet pour octet) ;
- constructions host et 16 presets : **aucun binaire changé** depuis R50-1 ;
- pytest de lepton-tools ; relais des messages de scion, en ligne de commande et dans VSCodium ;
  fichiers générés par lepton ;
- commande de miroir, à blanc, sur les 8 miroirs.

**Pas de cartes** dans cette session (PA-93) : aucun binaire ne change. Aucune écriture flash.

Références publiées (toutes poussées, aucune fusion différée) :

| Dépôt (`https://github.com/lepton-distribution/…`) | Référence | Commit | En R50-1 |
| --- | --- | --- | --- |
| `lepton-tools` | `devenv/env-53` (cette consigne ; code identique à `main` fb61b9a) | tête après `fetch` | 93e1aa6 (`devenv/env-50`) |
| `seed.scions` | tag `0.6.3.0` | **87dc108** (`master` 6416c33) | tag `0.6.2.0` 213d2c0 |
| `lepton-seed.scions` | `original-tree` | 15740f9 | = |
| `lepton-original-tree.scions` (noyau) | `master` | **58e421e** | 76f28bd |
| `lepton-famille-qemu-mps2` | `master` | 3954357 | = |
| `lepton-bsp-qemu-mps2-an386` | `master` | 10a8889 | = |
| `lepton-bsp-qemu-mps2-an500` | `master` | e98a482 | = |
| `lepton-famille-stm32f4xx` | `master` | acdd24c | = |
| `lepton-bsp-nucleo-f429zi` | `master` | b9fe2bf | = |
| `lepton-bsp-nucleo-f439zi` | `master` | 314f91b | = |
| `lepton-famille-stm32wlxx` | `master` | 9349be2 | = |
| `lepton-bsp-nucleo-wl55jc1` | `master` | 4d7cf80 | = |
| `lepton-famille-stm32f7xx` | `master` | 12280a5 | = |
| `lepton-bsp-stm32f746g-disco` | `master` | 6266908 | = |
| `lepton-famille-samd21` | `master` | a262e81 | = |
| `lepton-bsp-samd21-xplained-pro` | `master` | f3cffa2 | = |
| `mirror-stm32f4xx-hal-driver` | tag `v1.8.5` | b6f0ed3 | = |
| `mirror-cmsis_device_f4` | commit épinglé, sans tag | 3c77349 (`master` 9192c7b) | = |
| `mirror-stm32f7xx-hal-driver` | tag `v1.3.3` | e1446fa | = |
| `mirror-cmsis_device_f7` | tag `v1.2.10` | 2352e88 | = |
| `mirror-stm32wlxx-hal-driver` | tag `v1.6.0` | 5c87cf0 | = |
| `mirror-cmsis-device-wl` | tag `v1.4.0` | 71a0b78 | = |
| `mirror-stm32-mw-subghz-phy` | tag `v1.5.0` | 7dc059f | = |
| `mirror-STM32CubeWL` | tag `v1.6.0` | f934cd2 | = |

Relevé du Mac : `rapports/env-53-mac/ls-remote-mac.txt`.

Références Mac (`rapports/env-53-mac.md` §1, `rapports/env-53-mac/attendu/`) :
- oracle `doc/devenv/rapports/oracles/env-52-apres/` (= `env-49-apres`, host + 16 presets) ;
- liste `chemin -> cible` : `rapports/env-50-mac/attendu/trunk-liens.txt` (3889, inchangée depuis
  R50-1) ; projetés : `rapports/env-50-mac/attendu/projetes.txt` (629) ;
- fichiers extraits par clone tiers : `attendu/clones/<clé>@<version>.extraits.txt` et
  `.sparse-checkout`, relevés sur `~/lepton` au Mac ; ligne par clone :
  `attendu/clones-rootstock-mac.txt` ;
- même état obtenu au Mac par `graft-update` d'un rootstock dans l'état de `$U`
  (`essais/env-13-vierge`, `rapports/env-53-mac.md` §1.4) ;
- sorties attendues du relais : `attendu/c5/` (chemins remplacés par `<C>` et `<HOME>`).

Référence Debian : `rapports/env-50-debian.md` et `oracles/env-50-debian/`.

La session VM ne développe pas : elle exécute, constate et rapporte.

## 2. Ce que la session VM peut faire, et ne fait pas

| Autorisé | Interdit |
| --- | --- |
| `git fetch` / `switch` de `~/lepton-tools-dev/lepton-tools` (`devenv/env-53`) et `git fetch` / `merge --ff-only` du clone noyau `$K` sur `master` | Modifier `DEVENV-STATUS.md`, `ORCHESTRATION.md`, `SPECIFICATION.md`, `handoff/*.md`, les consignes, `rapports/env-53-mac*` |
| Lancer soi-même (PA-93, voir ci-dessous) les commandes de la consigne marquées « l'**utilisateur** lance » : installations (§6, `sudo` sans mot de passe sur la VM), venv (§9.1), les deux `scion graft-update` (§7.1, §7.3), `rm -rf` (§13), telles qu'écrites ; lire les journaux de l'essai dans VSCodium (§9.3), fait par l'utilisateur | Toute autre commande `sudo`, tout autre `rm -rf`, `pip install` hors du venv du §9.1, `codium --install-extension` hors `install-vscodium.sh`, `graft-update` d'un autre rootstock que `$U` et `$E13` |
| Lectures dans `$U`, `$E13`, `$P`, `$R50` ; `lepton check` / `generate` / `seed status` dans `$U`, `$E13`, `$P`, `$R50` et `$R` | Toute écriture dans les clones de `$U` ou de `$E13` ; tout `seed-update` ; regreffer `$P` ou `$R50`, commiter dans leur graine |
| Créer `~/lepton-tools-dev/essais/env-53-debian` (rootstock neuf, **sous ce nom** : même longueur de chemin qu'`env-50-debian`, §8) et y tout faire, `build/` compris | Écrire un fichier régulier dans un `trunk/` ou sous `depots/tiers/` ; corriger quoi que ce soit (consigner l'écart pour la session Mac) |
| Créer `~/lepton-tools-dev/essais/env-53-c5` (copie de `$P`, §9.2) et y tout faire, `seed add` / `seed remove` compris | `git config` (même en lecture) et `git sparse-checkout` (même `list`) dans un clone de `depots/tiers/` : relever par `releve-clones.sh` (§7) |
| `scion mirror-sync --dry-run` dans `$R` (§11) | `scion mirror-sync` **sans** `--dry-run` ; tout envoi vers un miroir |
| pytest de lepton-tools dans `~/lepton-tools-dev/venv-test`, `TMPDIR` sous `~` (§9.1) | Toute écriture flash, toute commande OpenOCD (pas de cartes) ; modifier la configuration réseau de la VM |
| Créer `devenv/env-53-debian` (depuis `devenv/env-53`) ; y écrire `doc/devenv/rapports/env-53-debian.md` et `doc/devenv/rapports/oracles/env-53-debian/` | Commiter sur une autre branche |
| `git push origin devenv/env-53-debian` **après accord explicite de l'utilisateur** (PA-P) | Pousser toute autre branche |

Règles des consignes VM (ORCHESTRATION §2bis) :
- **Commandes marquées « l'utilisateur lance » — précision de l'utilisateur au PA-93
  (2026-11-12), pour R53-1 seulement.** Les installations (§6), les deux `scion graft-update`
  (§7.1, §7.3), la création éventuelle du venv (§9.1) et les `rm -rf` (§13) peuvent être lancés
  **par la session VM elle-même**, exactement comme écrits (bloc entier, mêmes journaux) ; `sudo`
  ne demande pas de mot de passe sur la VM. La session annonce chaque commande par un
  `AVANCEMENT` avant de la lancer, puis vérifie l'effet et le consigne. Si le classifieur de
  permissions en refuse une, la session ne contourne pas : `AVANCEMENT` avec la commande exacte,
  et l'utilisateur la lance. L'essai dans VSCodium (§9.3, interface graphique) reste fait par
  l'utilisateur.
- **Commandes lancées par la session.** `scion rootstock-install`, `seed-add`, `graft` (§7.2) et
  `rejouer-oracle.sh` (§8) ont été acceptés de R28-1 à R50-1. `lepton seed add` (§9.2) clone
  depuis GitHub. Si le classifieur de permissions refuse l'une de ces commandes, ou pytest
  (§9.1), la session ne contourne pas : elle envoie un `AVANCEMENT` avec la commande exacte, et
  l'utilisateur la lance.
- **Régénérer avant de relever** : tout relevé « avant » d'un fichier généré suit immédiatement
  la commande qui le produit (§5.1).
- **Branche des clones d'un rootstock existant** : la branche courante de chaque clone de `$U` et
  de `$E13` est relevée au §5 et consignée. scion refuse lui-même un clone hors de sa version
  déclarée ; un tel refus reste un écart à exposer.
- **scion avant toute regreffe** : aucun `graft-update`, `graft`, `seed-add` ni `lepton seed add`
  avant que `scion version` donne 0.6.3.0 (§6). scion 0.6.2.0 ne connaît pas l'extraction
  partielle.

Tout écart au plan, toute erreur non prévue : s'arrêter, exposer (`AVANCEMENT` ou `QUESTION`),
attendre.

## 3. Communication (ORCHESTRATION §2bis)

- Session principale : `lepton-tools-3b` (session Mac). Répondre à l'adresse `from` du message
  d'ordre.
- ID : `R53-1`, repris tel quel : `[ACCUSÉ R53-1] ENV-53 — …`, `[AVANCEMENT R53-1] …`,
  `[QUESTION R53-1] …`, `[FIN-SUCCÈS R53-1] …` ou `[FIN-ÉCHEC R53-1] …`.
- `ACCUSÉ`, avant toute commande autre que les lectures du §5. Il contient :
  - l'ordre reformulé en une phrase ;
  - la tête réelle de `devenv/env-53` après `fetch` ;
  - les résultats de `git ls-remote` du §5 ;
  - les branches et têtes des clones de `$U` et de `$E13` ;
  - les étapes prévues (§6 à §13) et les écarts déjà visibles.
- `AVANCEMENT` : avant chaque commande marquée « l'utilisateur lance » (§6, §7.1, §7.3, §9.1 si
  besoin, §13 ; lancée par la session, §2), quand l'utilisateur doit agir (§9.2 si refus, §9.3,
  tout refus du classifieur), après chacun des §6 à §11, et à chaque arrêt.
- `FIN-SUCCÈS` / `FIN-ÉCHEC` : résultat par critère du §14, commits et branche (poussée ou non),
  chemin du rapport, versions relevées, écarts, ce qui n'a pas été fait.
- **Remise en échec** (règle D9 du §2bis) : un envoi en erreur (ECONNRESET, « bridge ID is
  stale ») est renvoyé une fois, à l'identique. Si le second envoi échoue, le message entier est
  consigné dans `~/env-53-journaux/0-messages-R53-1.md` et au §Messages du rapport, avec la
  mention « non remis ». La session l'annonce à l'utilisateur, qui le relaie à la session Mac.
  Un message relayé par l'utilisateur et portant l'ID `R53-1` vaut message reçu.

## 4. Journaux et variables

```bash
mkdir -p ~/env-53-journaux
J=~/env-53-journaux
T=~/lepton-tools-dev/lepton-tools
K=~/lepton-tools-dev/lepton-noyau
R=~/lepton-tools-dev/essais/env-53-debian
R50=~/lepton-tools-dev/essais/env-50-debian
U=~/lepton-tools-dev/essais/env-28-debian
E13=~/lepton-tools-dev/essais/env-13-debian
P=~/lepton-tools-dev/essais/env-11/qemu
C5=~/lepton-tools-dev/essais/env-53-c5
G=https://github.com/lepton-distribution
O=doc/devenv/rapports/oracles
X=doc/devenv/rapports/env-53-mac
A=$X/attendu
A50=doc/devenv/rapports/env-50-mac/attendu
C=doc/devenv/rapports/env-43-mac/controler-trunk.py
RC=$X/releve-clones.sh
IC=$X/inventaire-clones.sh
LI=$X/liens.py
RL=doc/devenv/rapports/env-51-messages/releve.sh
```
Une commande par journal `$J/<étape>.log`, code de retour en dernière ligne (`code=<n>`).
Les boucles s'écrivent en bash (`bash -c '…'` ou script), pas en zsh. Ne pas faire `cd` dans un
`trunk/` avant d'écrire un journal : revenir à `$T` (le hook juge le répertoire courant).

Outils de la session Mac, en lecture seule, utilisables tels quels sur Debian :
- `releve-clones.sh <rootstock> <sortie>` : pour chaque clone de `depots/tiers/`, fichiers extraits
  (`find -type f` hors `.git`), fichiers `H` de `git ls-files -t`, copie de
  `.git/info/sparse-checkout`, et une ligne de `clones.txt` (HEAD, origin, `sparseCheckout`,
  cône, `ignorecase`, nombres `H` et `S`, `extraits=H`, Ko hors `.git`, Ko de `.git`). Lit
  `.git/config.worktree` et `.git/config` par `grep`.
- `inventaire-clones.sh <rootstock>` : branche, HEAD, amont et modifications de chaque clone de
  greffon et de graine (hors `depots/tiers`, `depots/.mirrors`).
- `liens.py <trunk>` : liste `./chemin -> cible` triée par octets sur stdout ; nombres de liens,
  de liens cassés et de fichiers réguliers sur stderr.
- `releve.sh <sortie> <nom> <répertoire> <commande…>` (ENV-51) : `<nom>.cmd`, `.out`, `.err`,
  `.code`, sans filtre.

## 5. Vérifications préalables (lecture seule) — C1

```bash
uname -sm; cat /etc/debian_version; uname -r; id -un; git --version
scion version | tail -1; lepton --version
arm-none-eabi-gcc --version | head -1; cmake --version | head -1; ninja --version
qemu-system-arm --version | head -1; python3 --version; codium --version | head -1; node --version 2>&1
echo "LEPTON_EMBOS_ROOT=${LEPTON_EMBOS_ROOT:-absente}"; ls -d ~/lepton/third_party/embos/cortexm-gcc/5.20.0.0 2>&1
df -h ~ /tmp | tail -2
test -e "$R" && echo "ARRÊT : $R existe déjà"; test -e "$C5" && echo "ARRÊT : $C5 existe déjà"
ls ~/lepton-tools-dev/venv-test/bin/python 2>&1
git -C "$T" status --short | head -5
git -C "$T" fetch origin && git -C "$T" switch devenv/env-53 && git -C "$T" merge --ff-only origin/devenv/env-53 && git -C "$T" log --oneline -1
cd "$T" && bash $X/ls-remote.sh > "$J/5-ls-remote.txt" 2>&1; diff <(grep -v '^lepton-tools ' $X/ls-remote-mac.txt) <(grep -v '^lepton-tools ' "$J/5-ls-remote.txt") && echo "têtes publiées = Mac"
# Rootstocks existants $U et $E13
for Z in "$U" "$E13"; do
  echo "== $Z"
  git -C "$Z"/depots/lepton-seed.scions/original-tree log --oneline -1
  grep -v '^#' "$Z"/trunk/.scion.grafted.list | grep -c .
  bash "$T/$IC" "$Z" | tee "$J/5-clones-$(basename $Z).txt"
  python3 -I "$T/$LI" "$Z/trunk" > /dev/null
  ls -d "$Z"/depots/tiers/*/* 2>&1; du -sk "$Z"/depots/tiers
done
# Autres rootstocks de la VM
ls -d "$R50" "$R50"/original-tree.code-workspace "$P"/depots/lepton-seed/env11 ~/env-50-journaux 2>&1
ls -d ~/lepton-tools-dev/essais/*/ ~/lepton-tools-dev/essais/env-11/*/ 2>&1
```
Attendu :
- `têtes publiées = Mac` ; lepton-tools propre, à la tête de `origin/devenv/env-53` ;
- git **2.47.3** (≥ 2.35, minimum de scion 0.6.3.0 pour l'extraction partielle) ;
- scion **0.6.2.0** (avant installation) ; `lepton 0.1.0`, `scion 0.6.2.0 (requis ≥ 0.6.2.0)` ;
- chaîne APT de R50-1 : arm-none-eabi-gcc 14.2.1 (`15:14.2.rel1-1`), cmake 3.31.6, ninja 1.12.1,
  QEMU 10.0.13, Python 3.13.5, codium 1.135.06055 ;
- `$U` et `$E13` (état laissé par R50-1), chacun :
  - graine à 15740f9 ; **23 entrées** ;
  - 14 lignes d'inventaire : la graine sur `original-tree`, 13 clones `<clé>/master` sur
    `master`, amont réglé, `modifs=0`, aux commits de la colonne « En R50-1 » (noyau **76f28bd**) ;
  - `liens=3889 casses=0 reguliers=0` ;
  - 8 clones tiers, ≈ 242 Mo (`du`) ;
- `$R50`, son espace, `$P` et sa graine `env11`, `~/env-50-journaux` présents.

Arrêts :
- `$R` ou `$C5` existe ;
- lepton-tools non propre ;
- un commit publié diffère du Mac ;
- graine de `$U` ou de `$E13` modifiée ;
- un clone de `$U` ou de `$E13` hors de sa branche, sans amont ou modifié ;
- git < 2.35 ;
- moins de 8 Go libres dans `~`.

Pas des arrêts, à consigner :
- embOS absent : les presets `*-embos*` seront en échec attendu ;
- une version de la chaîne APT différente de R50-1 (elle peut expliquer un écart au §8.1) ;
- `venv-test` absent (§9.1 le traite) ;
- `node` absent (sans effet : l'essai de l'extension passe par VSCodium, §9.3).

### 5.1 Fichiers générés : régénération puis relevé avant (pour C5)

Avec le lepton installé avant le §6 :
```bash
lepton generate -C "$P" > "$J/5.1-generate-P-avant.log" 2>&1; echo "code=$?" >> "$J/5.1-generate-P-avant.log"
lepton check -C "$P" > "$J/5.1-check-P-avant.log" 2>&1; echo "code=$?" >> "$J/5.1-check-P-avant.log"
git -C "$P"/depots/lepton-seed/env11 status --short > "$J/5.1-graine-P-avant.txt"
sha256sum "$P"/depots/lepton-seed/env11/project/scion/CMakeUserPresets.json "$P"/*.code-workspace > "$J/5.1-generes-P-avant.sha256"
lepton generate -C "$R50" > "$J/5.1-generate-R50.log" 2>&1; echo "code=$?" >> "$J/5.1-generate-R50.log"
cp "$R50"/original-tree.code-workspace "$J/5.1-R50.code-workspace"
lepton generate -C "$U" > "$J/5.1-generate-U-avant.log" 2>&1; echo "code=$?" >> "$J/5.1-generate-U-avant.log"
cp "$U"/original-tree.code-workspace "$J/5.1-U-avant.code-workspace"
lepton generate -C "$E13" > "$J/5.1-generate-E13-avant.log" 2>&1; echo "code=$?" >> "$J/5.1-generate-E13-avant.log"
cp "$E13"/original-tree.code-workspace "$J/5.1-E13-avant.code-workspace"
```
Attendu : codes 0. `$R50` n'est pas regreffé : son espace sert de référence à celui de `$R`
(§10.1), puis `$R50` est supprimé (§13).

## 6. Installation de scion 0.6.3.0 et de lepton (C1)

D'abord, par la session :
```bash
git -C "$K" status --short | head -5
git -C "$K" fetch origin && git -C "$K" switch master && git -C "$K" merge --ff-only origin/master && git -C "$K" log --oneline -1
grep -n '^SCION_REF=' "$K/scripts/install-debian.sh"; grep -n '^SCION_REF=' "$T/scripts/install-vscodium.sh"
grep -n 'SCION_MIN_VERSION =' "$T/lepton/__init__.py"
grep -n '"version"' "$T/extension/package.json"; ls "$T"/extension/dist/lepton-0.5.2.vsix
```
Attendu :
- clone noyau propre, à **58e421e** (76f28bd avant) ;
- `SCION_REF="${SCION_REF:-0.6.3.0}"` (noyau) et `SCION_REF="0.6.3.0"` (lepton-tools) ;
- `SCION_MIN_VERSION = (0, 6, 2, 0)` (inchangé, PA-91) ;
- extension 0.5.2, `.vsix` présent.

Puis `AVANCEMENT` : l'**utilisateur** lance (ou la session, §2, PA-93 ; sudo sans mot de passe),
**sans** `SCION_REF` dans l'environnement (défaut du noyau), dans cet ordre :

```bash
J=~/env-53-journaux; K=~/lepton-tools-dev/lepton-noyau; T=~/lepton-tools-dev/lepton-tools
unset SCION_REF SCION_SPEC
bash "$K/scripts/install-debian.sh" --with-debug-tools 2>&1 | tee "$J/6-install-debian.log"; echo "code=${PIPESTATUS[0]}" | tee -a "$J/6-install-debian.log"
pipx install --force "$T" 2>&1 | tee "$J/6-lepton.log"; echo "code=${PIPESTATUS[0]}" | tee -a "$J/6-lepton.log"
bash "$T/scripts/install-vscodium.sh" --lepton-clone "$K" 2>&1 | tee "$J/6-install-vscodium-1.log"; echo "code=${PIPESTATUS[0]}" | tee -a "$J/6-install-vscodium-1.log"
bash "$T/scripts/install-vscodium.sh" --lepton-clone "$K" 2>&1 | tee "$J/6-install-vscodium-2.log"; echo "code=${PIPESTATUS[0]}" | tee -a "$J/6-install-vscodium-2.log"
```
La session lit ensuite les journaux. Attendu : quatre codes 0. `install-debian.sh` installe scion
depuis `$G/seed.scions.git@0.6.3.0` (0.6.2.0 auparavant). Première exécution
d'`install-vscodium.sh` : nombre de changements relevé (extension inchangée depuis R43-1) ;
seconde : **`changements 0`**. Puis :
```bash
scion version | tail -1; lepton --version; codium --version | head -1
pipx list --short | grep -E '^(scion|lepton) '
dpkg-query -W -f '${Version}\n' codium; codium --list-extensions --show-versions | LC_ALL=C sort > "$J/6-extensions.txt"
grep -E -i 'lldb|lepton|rtos-views|peripheral' "$J/6-extensions.txt"
```
Attendu :
- `scion version: 0.6.3.0` ;
- `lepton 0.1.0`, `scion 0.6.3.0 (requis ≥ 0.6.2.0)` ;
- `vadimcn.vscode-lldb@1.12.3`, `lepton-distribution.lepton@0.5.2`,
  `mcu-debug.rtos-views@0.0.16`, `mcu-debug.peripheral-viewer@1.6.4`.

**Arrêt** si scion n'est pas 0.6.3.0 : aucun `graft-update`, `graft` ni `seed add`.

## 7. `graft-update` des rootstocks existants, rootstock neuf (C2, C4)

Contrôles communs, après chaque greffe d'un rootstock `Z` (session, depuis `$T`) :
```bash
# n = 7.1-U, 7.2-R ou 7.3-E13
python3 -I "$T/$C" "$Z" "$T/$A50/trunk-liens.txt" "$J/$n-controle" > "$J/$n-controle.log" 2>&1; echo "code=$?" >> "$J/$n-controle.log"
cat "$J/$n-controle.log"
diff "$T/$A50/projetes.txt" "$J/$n-controle/projetes.txt" && echo "projetés = attendu (629)"
bash "$T/$RC" "$Z" "$J/$n-tiers-apres" > /dev/null
e=0; for f in "$T/$A"/clones/*; do cmp -s "$f" "$J/$n-tiers-apres/${f##*/}" || { echo "ÉCART ${f##*/}"; e=$((e+1)); }; done; echo "extraits et sparse-checkout : écarts=$e (16 fichiers)"
normc() { sed -E 's/ ignorecase=[^ ]*//; s/ ko_hors_git=.*//' "$1"; }
diff <(normc "$T/$A/clones-rootstock-mac.txt") <(normc "$J/$n-tiers-apres/clones.txt") && echo "clones = Mac (hors ignorecase et tailles)"
awk '{print $1, $6, $(NF-1), $NF}' "$J/$n-tiers-apres/clones.txt"; du -sk "$Z"/depots/tiers
```
Attendu, pour chaque rootstock :
- `controler-trunk.py` code 0, `CONFORME` :
  - liste `chemin -> cible` identique à l'attendu (**3889** liens), 0 fichier régulier, 0 lien
    cassé ;
  - 629 projetés = attendu, 0 écart de nom (casse), 0 écart de contenu ;
  - 8 clones tiers aux HEAD épinglés, `origin` = miroirs `$G/mirror-*.git`, 0 modification,
    filtre `blob:none` ;
- extraits et `sparse-checkout` : **écarts=0** sur les 16 fichiers. Les listes du Mac sont triées
  en `LC_ALL=C` et comparées octet pour octet : un écart de casse s'y voit ;
- `clones = Mac` : pour les 8 clones, `sparseCheckout=true cone=true`, mêmes nombres `H` et `S`,
  `extraits=H:oui` (Mac : `cmsis-device-f4` 31 / 121, `cmsis-device-f7` 22 / 91,
  `cmsis-device-wl` 70 / 9, `stm32-mw-subghz-phy` 28 / 119, `stm32cubewl` 103 / 8859,
  `stm32f4xx-hal-driver` 204 / 5, `stm32f7xx-hal-driver` 200 / 6, `stm32wlxx-hal-driver` 161 / 7) ;
- `ignorecase` : **vide** ou `false` sur la VM (git ne le pose que sur un système qui confond la
  casse ; Mac : `true`) — relevé et consigné ;
- tailles relevées (Ko hors `.git`, Ko de `.git`, `du` de `depots/tiers`). Mac, clone converti :
  `depots/tiers` 242 → 106 Mo ; rootstock neuf (ENV-52) : ≈ 85 Mo.

### 7.1 `$U` — C2

Par la session :
```bash
cd "$T"
python3 -I "$T/$LI" "$U/trunk" > "$J/7.1-liens-avant.txt"
bash "$T/$RC" "$U" "$J/7.1-U-tiers-avant" | awk '{print $1, $4, $5, $7, $8, $(NF-1), $NF}'
du -sk "$U"/depots/tiers
```
Attendu : 3889 liens ; 8 clones, `sparseCheckout=` vide (extraction complète).

Puis `AVANCEMENT` : l'**utilisateur** lance :
```bash
J=~/env-53-journaux; cd ~/lepton-tools-dev/essais/env-28-debian
scion graft-update -v > "$J/7.1-graft-update.log" 2>&1; echo "code=$?" >> "$J/7.1-graft-update.log"
```
Puis la session :
```bash
cd "$T"
tail -3 "$J/7.1-graft-update.log"; grep -i -E 'conflit|refus|avancé|git clone|extraction partielle,' "$J/7.1-graft-update.log"
git -C "$U"/depots/lepton-seed.scions/original-tree log --oneline -1
grep -v '^#' "$U"/trunk/.scion.grafted.list | grep -c .
bash "$T/$IC" "$U" > "$J/7.1-clones-apres.txt"; diff "$J/5-clones-env-28-debian.txt" "$J/7.1-clones-apres.txt"
python3 -I "$T/$LI" "$U/trunk" > "$J/7.1-liens-apres.txt"; cmp "$J/7.1-liens-avant.txt" "$J/7.1-liens-apres.txt" && echo "liens inchangés"
Z=$U; n=7.1-U   # puis les contrôles communs ci-dessus
```
Attendu (constaté au Mac sur `essais/env-13-vierge`, même état de départ que `$U`) :
- `graft-update` : code 0, 0 conflit ; graine inchangée (15740f9) ; **un seul** clone avancé :
  `…/original/master avancé : 76f28bd -> 58e421e` ; aucun `git clone` ;
- 8 lignes `clone …/depots/tiers/<clé>/<version> : extraction partielle, N répertoire(s)` :
  `stm32f4xx-hal-driver` 2, `cmsis-device-f4` 1, `stm32wlxx-hal-driver` 2, `cmsis-device-wl` 2,
  `stm32-mw-subghz-phy` 2, `stm32cubewl` 9, `stm32f7xx-hal-driver` 2, `cmsis-device-f7` 1 ;
- « 3889 feuilles liées » ; **23 entrées** ;
- inventaire : seule la ligne du noyau change (`head=58e421e`) ;
- **liens inchangés** (aucun ajout, retrait ni changement de cible) ;
- contrôles communs conformes.

Toute autre ligne : écart à exposer. Une ligne « chemin(s) ignoré(s) par git » du journal est
relevée telle quelle (au Mac : 6 `.DS_Store`, absents sur la VM).

### 7.2 Rootstock neuf depuis la graine publiée — C2

```bash
mkdir "$R" && cd "$R"
scion rootstock-install > "$J/7.2-rootstock-install.log" 2>&1; echo "code=$?" >> "$J/7.2-rootstock-install.log"
scion seed-add --version original-tree $G/lepton-seed.scions.git > "$J/7.2-seed-add.log" 2>&1; echo "code=$?" >> "$J/7.2-seed-add.log"
scion graft > "$J/7.2-graft.log" 2>&1; echo "code=$?" >> "$J/7.2-graft.log"
cd "$T"
tail -2 "$J/7.2-graft.log"
grep -v '^#' "$R"/trunk/.scion.grafted.list | grep -c .
bash "$T/$IC" "$R" > "$J/7.2-clones.txt"; cat "$J/7.2-clones.txt"
Z=$R; n=7.2-R   # contrôles communs
diff "$J/7.1-U-controle/liens.txt" "$J/7.2-R-controle/liens.txt" && echo "liste identique à \$U"
```
Attendu :
- codes 0 ; « 3889 feuilles liées » ; 23 entrées ; chaque clone sur sa branche au commit du §1 ;
- contrôles communs conformes ; liste identique à celle de `$U` ;
- tailles des `.git` des clones neufs relevées (Mac, ENV-52 : `stm32cubewl` 3,5 Mo,
  `stm32-mw-subghz-phy` 0,1 Mo, `cmsis-device-f4` 0,3 Mo) ; `depots/tiers` ≈ 85 Mo.

### 7.3 `$E13` — C4

Le relevé du §5 donne l'état de départ. Si un clone de `$E13` est hors de sa branche, sans amont
ou modifié : `QUESTION`, pas de `graft-update`. Sinon, par la session :
```bash
cd "$T"
python3 -I "$T/$LI" "$E13/trunk" > "$J/7.3-liens-avant.txt"
bash "$T/$RC" "$E13" "$J/7.3-E13-tiers-avant" > /dev/null; du -sk "$E13"/depots/tiers
```
Puis `AVANCEMENT` : l'**utilisateur** lance :
```bash
J=~/env-53-journaux; cd ~/lepton-tools-dev/essais/env-13-debian
scion graft-update -v > "$J/7.3-graft-update.log" 2>&1; echo "code=$?" >> "$J/7.3-graft-update.log"
```
Puis la session :
```bash
cd "$T"
tail -3 "$J/7.3-graft-update.log"; grep -i -E 'conflit|refus|avancé|git clone|extraction partielle,' "$J/7.3-graft-update.log"
bash "$T/$IC" "$E13" > "$J/7.3-clones-apres.txt"; diff "$J/5-clones-env-13-debian.txt" "$J/7.3-clones-apres.txt"
python3 -I "$T/$LI" "$E13/trunk" > "$J/7.3-liens-apres.txt"; cmp "$J/7.3-liens-avant.txt" "$J/7.3-liens-apres.txt" && echo "liens inchangés"
Z=$E13; n=7.3-E13   # contrôles communs
lepton check -C "$E13" > "$J/7.3-check-E13.log" 2>&1; echo "code=$?" >> "$J/7.3-check-E13.log"; tail -3 "$J/7.3-check-E13.log"
lepton generate -C "$E13" > "$J/7.3-generate-E13.log" 2>&1; echo "code=$?" >> "$J/7.3-generate-E13.log"; tail -1 "$J/7.3-generate-E13.log"
diff "$J/5.1-E13-avant.code-workspace" "$E13"/original-tree.code-workspace > "$J/7.3-espace.diff"; echo "diff=$?"
```
Attendu : comme au §7.1 (un seul clone avancé, 8 conversions, liens inchangés, contrôles communs
conformes) ; `lepton check` **code 0** ; `generate` code 0 ; espace identique à l'avant (`diff=0`).

Un refus de scion (clone hors version, graine divergée) : écart à exposer, sans contournement.

## 8. Reconstructions et comparaisons (C3)

Périmètre : host et les 16 presets croisés (QEMU : construction, fumée, banc KAL ; cartes :
construction et capture seulement, **aucun flash**). `$R` s'appelle `env-53-debian` : les chaînes
`__FILE__` des presets FreeRTOS suivent le chemin du rootstock. `env-50-debian` a la même longueur,
sinon `.text` diffère.

```bash
cd "$T" && git switch -c devenv/env-53-debian devenv/env-53
scripts/oracle/rejouer-oracle.sh "$R" $O/env-53-debian \
  --qemu qemu-mps2-an386-embos --qemu qemu-mps2-an386-embos-soft \
  --qemu qemu-mps2-an386-freertos --qemu qemu-mps2-an386-freertos-soft \
  --qemu qemu-mps2-an500-embos --qemu qemu-mps2-an500-freertos \
  --carte nucleo-f429zi-embos --carte nucleo-f429zi-freertos \
  --carte nucleo-f439zi-embos --carte nucleo-f439zi-freertos \
  --carte nucleo-wl55jc1-embos --carte nucleo-wl55jc1-freertos \
  --carte samd21-xplained-pro-embos --carte samd21-xplained-pro-freertos \
  --carte stm32f746g-disco-embos --carte stm32f746g-disco-freertos > "$J/8-rejouer.log" 2>&1; echo "code=$?" >> "$J/8-rejouer.log"
tail -25 "$J/8-rejouer.log"
grep -h "tests passed" $O/env-53-debian/*/ctest.log $O/env-53-debian/*/banc-kal.log
grep -h "peripheriques" $O/env-53-debian/qemu-mps2-an386-*/banc-kal.log
python3 -I "$T/$LI" "$R/trunk" > /dev/null; find "$R/trunk" -name __pycache__ | wc -l
```
Attendu :
- code 0 ; host ctest 7/7 ; 16 presets construits ; fumée réussie ;
- banc QEMU **identique à R50-1** : an386 20/20, an386 soft 16/16, an500 19/19
  (`net.ping_ftpd` ne tourne que sous Linux) ;
- `qemu-mps2-an386.peripheriques` **Passed** dans les 4 `banc-kal.log` an386 ;
- trunk sans fichier régulier, lien cassé ni `__pycache__`.

### 8.1 Comparaisons

La non-régression Debian se lit **par rapport à R50-1** : ENV-51 et ENV-52 ne touchent aucune
source compilée, et le Mac a `env-52-apres` = `env-49-apres` (code 0 ×16).

```bash
cd "$T"
norm() { grep -E '^(section|symbole)' "$1" | sed -E 's/ \[.*$//; s/ +: /: /' | grep -v -E '^section [^:]*: \.debug_' | LC_ALL=C sort; }
diff -q $O/env-50-debian/host/mklepton-empreintes.sha256 $O/env-53-debian/host/mklepton-empreintes.sha256 && echo "mklepton = R50-1"
diff -q $O/env-52-apres/host/mklepton-empreintes.sha256 $O/env-53-debian/host/mklepton-empreintes.sha256 && echo "mklepton = Mac env-52-apres"
for p in $(ls $O/env-53-debian | grep -v -e host -e ctest-N -e compilation -e '\.log$'); do
  python3 scripts/oracle/comparer-oracle.py $O/env-50-debian/$p $O/env-53-debian/$p > "$J/8.1-cmp-R50-$p.txt" 2>&1; a=$?
  python3 scripts/oracle/comparer-oracle.py $O/env-52-apres/$p $O/env-53-debian/$p > "$J/8.1-cmp-Mac-$p.txt" 2>&1; b=$?
  echo "$p comparer_R50-1=$a comparer_Mac=$b hors_debug=$(norm $J/8.1-cmp-R50-$p.txt | wc -l)"
done | tee "$J/8.1-bilan.txt"
```
Attendu :
- mklepton : empreintes identiques à `env-50-debian` et à `env-52-apres` ;
- `comparer_R50-1` **0** pour les **16 presets**, `hors_debug=0` (PA-93 : aucun écart admis) ;
- `comparer_Mac` : informatif (chaînes différentes ; 1 attendu partout).

Un `comparer_R50-1` non nul : écart à exposer, avec l'extrait du `8.1-cmp-R50-<preset>.txt` ; si
seules des sections `.debug_*` changent, le dire (`hors_debug=0`) ; pas de correction.

## 9. pytest et relais des messages de scion (C5)

### 9.1 pytest de lepton-tools

Si `~/lepton-tools-dev/venv-test/bin/python` est absent (§5), ou si pytest y manque :
`AVANCEMENT`, et l'**utilisateur** lance :
```bash
T=~/lepton-tools-dev/lepton-tools; python3 -m venv ~/lepton-tools-dev/venv-test && ~/lepton-tools-dev/venv-test/bin/pip install -e "$T[test]"
```
Puis la session :
```bash
cd "$T"; mkdir -p ~/tmp-pytest
~/lepton-tools-dev/venv-test/bin/python -m pip show lepton | grep -i -E '^(version|location|editable)'
TMPDIR=~/tmp-pytest ~/lepton-tools-dev/venv-test/bin/python -m pytest -q -rs -p no:cacheprovider > "$J/9.1-pytest.log" 2>&1; echo "code=$?" >> "$J/9.1-pytest.log"
tail -4 "$J/9.1-pytest.log"
TMPDIR=~/tmp-pytest ~/lepton-tools-dev/venv-test/bin/python -m pytest -q -p no:cacheprovider tests/test_proteger_trunk.py > "$J/9.1-pytest-hook.log" 2>&1; echo "code=$?" >> "$J/9.1-pytest-hook.log"
tail -2 "$J/9.1-pytest-hook.log"
git -C "$T" status --short | head -5
```
Attendu (Mac, ENV-51 et ENV-52, Python 3.11.5, scion 0.6.3.0) :
- suite complète : code 0, **384 passed** (environ 7 min 30) ; les 7 tests du relais d'ENV-51
  compris (`tests/test_projection.py`) ;
- `tests/test_proteger_trunk.py` : **118 passed** ;
- lepton-tools reste propre (hors rapport et oracle de la session).

Un test ignoré ou en échec : relever son nom et son message (`-rs`), relancer ce test seul une
fois, consigner les deux résultats ; pas de correction.

### 9.2 Relais en ligne de commande (copie de `$P`)

Forme de l'essai d'ENV-51 (`rapports/env-51-messages.md` §1.2, §4), sur une copie de la graine de
projet `$P` (QEMU, famille `qemu-mps2`) : ajout puis retrait d'un porteur de clés projetées, la
famille F7, puis échec d'un ajout. Le Mac a fait les mêmes commandes sur une copie de son
`essais/env-11/qemu` (`rapports/env-53-mac.md` §1.5) : sorties dans `$A/c5/`, chemins remplacés
par `<C>` (la copie) et `<HOME>`.

```bash
cd "$T"
mkdir "$C5" && tar -C "$P" --exclude=./build -cf - . | tar -C "$C5" -xf -; echo "copie=$?"
python3 -I "$T/$LI" "$C5/trunk" > "$J/9.2-liens-avant.txt"
lepton generate -C "$C5" > "$J/9.2-generate.log" 2>&1; echo "code=$?" >> "$J/9.2-generate.log"; grep -c 'env-11/qemu' "$C5"/env11.code-workspace
lepton check -C "$C5" > "$J/9.2-check.log" 2>&1; echo "code=$?" >> "$J/9.2-check.log"; tail -1 "$J/9.2-check.log"
S=$J/9.2-releves
bash $RL $S 01-seed-add-f7 "$C5" lepton seed add stm32f7xx --type famille $G/lepton-famille-stm32f7xx.git@master --no-cmake
bash "$T/$RC" "$C5" "$J/9.2-tiers" | awk '{print $1, $4, $5, $7, $8, $9}'
for b in stm32f7xx-hal-driver@v1.3.3 cmsis-device-f7@v1.2.10; do for s in extraits.txt sparse-checkout; do cmp -s "$T/$A/clones/$b.$s" "$J/9.2-tiers/$b.$s" && echo "$b.$s = Mac" || echo "$b.$s ÉCART"; done; done
lepton seed status -C "$C5" --json > "$J/9.2-seed-status.json" 2> "$J/9.2-seed-status.err"; echo "code=$?"; python3 -c 'import json,sys; json.load(open(sys.argv[1])); print("json ok")' "$J/9.2-seed-status.json"
bash $RL $S 02-seed-remove-f7 "$C5" lepton seed remove stm32f7xx --no-cmake
bash $RL $S 03-seed-add-echec "$C5" lepton seed add absent "file://localhost$HOME/lepton-tools-dev/essais/env-53-absent.git" --type bibliotheque --no-cmake
ls -d "$C5"/depots/lepton/library-absent 2>&1; find "$C5"/depots/lepton/library-absent 2>/dev/null | wc -l
python3 -I "$T/$LI" "$C5/trunk" > "$J/9.2-liens-apres.txt"; cmp "$J/9.2-liens-avant.txt" "$J/9.2-liens-apres.txt" && echo "liens = avant"
git -C "$C5"/depots/lepton-seed/env11 status --short | wc -l
for n in 01-seed-add-f7 02-seed-remove-f7 03-seed-add-echec; do for s in cmd out err code; do
  sed -e "s|$C5|<C>|g" -e "s|$HOME|<HOME>|g" "$S/$n.$s" | diff -q "$T/$A/c5/$n.$s" - > /dev/null && echo "$n.$s = Mac" || echo "$n.$s DIFFÈRE"
done; done
rmdir "$C5"/depots/lepton/library-absent 2>&1
```
Attendu :
- copie : code 0 ; `liens=3059 casses=0 reguliers=0` (au Mac : 3059 ; la VM peut différer si
  `$P` diffère, le relever) ; après `generate`, 0 référence à `env-11/qemu` dans l'espace ;
  `check` code 0 ;
- **01** (`seed add`) : code 0 ; stdout de lepton inchangé (2 lignes : `stm32f7xx ajouté (…)`,
  `graine modifiée, non commitée : …`) ; stderr : **5 lignes `scion: `**, dans cet ordre :
  `déclaré dans …`, P-G6 `clés projetées regreffées avec leur porteur lepton/family-stm32f7xx :
  tiers/stm32f7xx-hal-driver, tiers/cmsis-device-f7`, 2 lignes `extraction partielle` (2 et 1
  répertoires, nouvelles en 0.6.3.0), `greffe partielle : 212 feuilles liées …` ;
- clones F7 neufs en extraction partielle, extraits et `sparse-checkout` = Mac ; `seed status
  --json` : code 0, `json ok`, stderr vide ;
- **02** (`seed remove`) : code 0 ; 2 lignes de stdout ; **3 lignes `scion: `**, dont P-P6
  `clés projetées retirées avec leur porteur … : tiers/…, tiers/…` ;
- **03** (échec) : code **2** ; stdout vide ; 2 lignes `scion: ` (`déclaré`, puis `retiré de`,
  annulation), puis `lepton: attention: ajout … annulé (graine et trunk restaurés)`, puis
  `lepton: erreur: échec de « scion seed-clone … » (code 2) :` suivi du stderr de scion **non
  préfixé**, une seule fois ;
- liens = avant ; graine `env11` sans modification (0 ligne) ;
- les 12 fichiers = Mac (`.cmd`, `.out`, `.err`, `.code` des trois relevés). Une différence due à
  la seule langue d'un message de git (03) : la relever, ce n'est pas un écart de lepton.

Constat du Mac, à relever sur la VM sans arrêt : après l'échec 03, un répertoire **vide**
`depots/lepton/library-absent` reste dans la copie (résidu du clonage avorté). La session le
retire par `rmdir` (copie de la session), et le consigne.

Si le classifieur refuse `lepton seed add` (clonage depuis GitHub) : `AVANCEMENT`, l'utilisateur
lance la même ligne `bash $RL …` dans un terminal, après avoir posé les variables du §4.

### 9.3 Relais dans VSCodium (essai par l'utilisateur)

Renvoi du PA-90 d'ENV-51 : la notification de l'extension (`lastMessage`) ne doit pas changer
avec les lignes `scion:`, qui vont dans le canal de sortie. L'essai porte sur la même copie
`$C5`, revenue à son état de départ au §9.2. Les clones F7 y restent (ni `seed remove` ni
`graft-remove` ne les suppriment) : l'ajout ne réextrait rien et n'écrit donc pas de ligne
`extraction partielle`. Sorties de la ligne de commande équivalente, relevées au Mac :
`$A/c5/04-ext-seed-add-f7.*`, `05-ext-seed-remove-f7.*`, `06-ext-seed-add-echec.*`.

`AVANCEMENT` : l'**utilisateur**, dans la session graphique de la VM :
1. ouvre l'espace : `codium ~/lepton-tools-dev/essais/env-53-c5/env11.code-workspace` ;
2. ouvre le canal de sortie : Affichage → Sortie, canal « Lepton » ;
3. palette (Ctrl+Maj+P) → **« Lepton : ajouter un greffon à la graine »**, réponses dans l'ordre :
   - nom : `stm32f7xx` ;
   - origine : `https://github.com/lepton-distribution/lepton-famille-stm32f7xx.git` ;
   - type : `famille` ;
   - version : `master` (valeur proposée) ;
   - chemin : vide (Entrée) ;
4. palette → **« Lepton : retirer un greffon de la graine »** : `stm32f7xx`, « conserver le
   clone », « Retirer » ;
5. palette → **« Lepton : ajouter un greffon à la graine »** : nom `absent` ; origine
   `file://localhost/home/<utilisateur>/lepton-tools-dev/essais/env-53-absent.git` (chemin absent ;
   `<utilisateur>` = `id -un`) ; type `bibliotheque` ; version `master` ; chemin vide ;
6. note le texte exact des trois notifications, et copie le canal « Lepton » dans
   `~/env-53-journaux/9.3-sortie-lepton.txt` (clic droit dans le canal → tout sélectionner,
   copier, coller dans un éditeur, enregistrer) ;
7. ferme VSCodium.

Attendu :
- étape 3 : notification d'information **« lepton : ajouter stm32f7xx — terminé »** ; dans le
  canal : les 2 lignes de stdout et les **3 lignes `scion: `** de `04-ext-seed-add-f7.err`
  (`déclaré`, P-G6, `greffe partielle`) ;
- étape 4 : **« lepton : retirer stm32f7xx — terminé »** ; canal : les 3 lignes `scion: ` de
  `05-ext-seed-remove-f7.err` (P-P6 comprise) ;
- étape 5 : notification d'erreur **« lepton : ajouter absent — échec (code 2) lepton: erreur:
  échec de « scion seed-clone --seed … » (code 2) : erreur : échec de « git clone … » (code 128) :
  … → corriger la cause signalée par scion, puis relancer »** : aucune ligne `scion:` dans la
  notification ; dans le canal, les lignes de `06-ext-seed-add-echec.err`.

Puis la session :
```bash
cd "$T"
grep -c '^scion: ' "$J/9.3-sortie-lepton.txt"; grep -n -E '^scion: |^lepton: (erreur|attention)|→ code' "$J/9.3-sortie-lepton.txt"
python3 -I "$T/$LI" "$C5/trunk" > "$J/9.3-liens-apres.txt"; cmp "$J/9.2-liens-avant.txt" "$J/9.3-liens-apres.txt" && echo "liens = avant"
git -C "$C5"/depots/lepton-seed/env11 status --short | wc -l
ls -d "$C5"/depots/lepton/library-absent 2>&1 && rmdir "$C5"/depots/lepton/library-absent
```
Attendu : 8 lignes `scion: ` en tout (3 + 3 + 2) ; trois `→ code` (0, 0, 2) ; liens = avant ;
graine sans modification ; le répertoire vide `library-absent` est de nouveau présent, puis
retiré.

## 10. Fichiers générés par lepton (C5)

### 10.1 Rootstock neuf `$R` contre `$R50`

```bash
lepton check -C "$R" > "$J/10.1-check-R.log" 2>&1; echo "code=$?" >> "$J/10.1-check-R.log"
lepton generate -C "$R" > "$J/10.1-generate-R.log" 2>&1; echo "code=$?" >> "$J/10.1-generate-R.log"
lepton seed status -C "$R" > "$J/10.1-seed-status-R.log" 2>&1; echo "code=$?" >> "$J/10.1-seed-status-R.log"
grep -E 'projection|^trunk' "$J/10.1-seed-status-R.log"
W="$R"/original-tree.code-workspace
for k in '"request"' '"svdFile"' '"type": "lldb"' 'tests des greffons' 'tiers'; do echo "$k $(grep -c "$k" "$W")"; done
diff <(sed "s#$R50#<R>#g" "$J/5.1-R50.code-workspace") <(sed "s#$R#<R>#g" "$W") > "$J/10.1-espace.diff"; echo "diff=$?"; head -40 "$J/10.1-espace.diff"
```
Attendu :
- `check`, `generate`, `seed status` code 0 ;
- `seed status` : 9 lignes `projection` aux versions du §1 : `stm32f4xx-hal-driver` (200
  fichiers), `cmsis-device-f4` (6), `stm32wlxx-hal-driver` (157), `cmsis-device-wl` (6),
  `stm32-mw-subghz-phy` (20), `stm32cubewl::utilities` (38), `stm32cubewl::radio-core-inc` (1),
  `stm32f7xx-hal-driver` (196), `cmsis-device-f7` (5) ; `trunk : aucun fichier régulier, aucun
  lien cassé` ;
- espace : 23 `"request"`, 10 `"svdFile"`, 7 `"type": "lldb"`, 4 tâches « tests des greffons »,
  0 `tiers` ;
- espace **identique** à celui de `$R50` au chemin du rootstock près (`diff=0`).

### 10.2 Rootstock regreffé `$U`

```bash
lepton check -C "$U" > "$J/10.2-check-U.log" 2>&1; echo "code=$?" >> "$J/10.2-check-U.log"
lepton generate -C "$U" > "$J/10.2-generate-U.log" 2>&1; echo "code=$?" >> "$J/10.2-generate-U.log"
lepton seed status -C "$U" > "$J/10.2-seed-status-U.log" 2>&1; echo "code=$?" >> "$J/10.2-seed-status-U.log"
grep -E 'projection|^trunk' "$J/10.2-seed-status-U.log"
diff "$J/5.1-U-avant.code-workspace" "$U"/original-tree.code-workspace > "$J/10.2-espace.diff"; echo "diff=$?"; head -40 "$J/10.2-espace.diff"
```
Attendu : codes 0 ; mêmes 9 clés projetées qu'au §10.1 ; espace identique à l'avant (`diff=0`).

### 10.3 Graine de projet existante `$P`

```bash
lepton generate -C "$P" > "$J/10.3-generate-P-apres.log" 2>&1; echo "code=$?" >> "$J/10.3-generate-P-apres.log"
lepton check -C "$P" > "$J/10.3-check-P-apres.log" 2>&1; echo "code=$?" >> "$J/10.3-check-P-apres.log"
git -C "$P"/depots/lepton-seed/env11 status --short > "$J/10.3-graine-P-apres.txt"
sha256sum "$P"/depots/lepton-seed/env11/project/scion/CMakeUserPresets.json "$P"/*.code-workspace > "$J/10.3-generes-P-apres.sha256"
diff "$J/5.1-generes-P-avant.sha256" "$J/10.3-generes-P-apres.sha256" && echo "générés P identiques"
diff "$J/5.1-graine-P-avant.txt" "$J/10.3-graine-P-apres.txt" && echo "graine P inchangée"
diff <(grep -v '^code=' "$J/5.1-check-P-avant.log") <(grep -v '^code=' "$J/10.3-check-P-apres.log") && echo "check P identique"
```
Attendu : codes 0 ; générés, graine et sortie de `check` identiques. `$P` n'est pas regreffé : ce
contrôle établit la stabilité du nouveau lepton.

## 11. Commande de miroir, à blanc (C6)

Contrôle des 8 miroirs contre leur amont, sans envoi. `$R` porte les déclarations de miroir
(`scion/.scion/.scion.mirrors` des familles F4, F7 et WL).

```bash
cd "$R"
scion mirror-sync --dry-run -v > "$J/11-mirror-sync.log" 2>&1; echo "code=$?" >> "$J/11-mirror-sync.log"
cd "$T"
grep -E 'référence\(s\) à envoyer|signalement' "$J/11-mirror-sync.log"; tail -1 "$J/11-mirror-sync.log"
ls -d "$R"/depots/.mirrors/*/*/* 2>&1
python3 -I "$T/$C" "$R" "$T/$A50/trunk-liens.txt" "$J/11-controle-R" | tail -1
```
Attendu (R50-1 et Mac, 2026-11-10) :
- code 0 ;
- 8 lignes `miroir … : 0 référence(s) à envoyer, 0 signalement(s)` ;
- 8 dépôts de travail sous `depots/.mirrors/github.com/lepton-distribution/` (≈ 80 Mo) ;
- trunk toujours `CONFORME`.

Une référence « à envoyer » n'est admise que si une publication amont postérieure au 2026-11-12
l'explique : la relever, puis relever la référence de l'amont
(`git ls-remote https://github.com/STMicroelectronics/<nom>.git`), sans arrêt ; elle ne sera pas
envoyée. Un signalement (tag déplacé, branche réécrite ou supprimée) est un écart à exposer.
Jamais sans `--dry-run`.

## 12. Cartes (C7)

Écarté au PA-93 : aucun binaire ne change (§8.1), et ENV-51 et ENV-52 ne touchent ni le flash ni
la sonde. Les cartes restent rattachées au Mac. Aucune commande OpenOCD, aucun `ctest -L board`.

## 13. Nettoyage de la VM (C8)

Accordé au PA-93. Après le §10.1 (l'espace de `$R50` est copié au §5.1), relevé par la session :
```bash
du -sh "$R50" ~/env-50-journaux
```
Puis `AVANCEMENT` : l'**utilisateur** lance :
```bash
rm -rf ~/lepton-tools-dev/essais/env-50-debian ~/env-50-journaux
```
La session vérifie `ls -d ~/lepton-tools-dev/essais/env-50-debian ~/env-50-journaux 2>&1`
(absents). Conservés : `$U` (`essais/env-28-debian`), `$E13` (`essais/env-13-debian`), regreffés
au §7 ; `$R` (`essais/env-53-debian`) ; `$P` ; `$C5` (`essais/env-53-c5`) ; `$J` ; `~/tmp-pytest`
(à vider par l'utilisateur s'il le souhaite, hors critère).

## 14. Critères et rapport

| Critère | Attendu |
| --- | --- |
| C1 Versions | `git ls-remote` = Mac (§5) ; git 2.47.3 (≥ 2.35) ; scion 0.6.3.0 par `install-debian.sh` (défaut `SCION_REF`) ; lepton `pipx` code 0, `lepton 0.1.0`, scion 0.6.3.0 accepté ; extension 0.5.2, seconde exécution d'`install-vscodium.sh` `changements 0` ; chaîne APT relevée |
| C2 `graft-update` et rootstock neuf | §7.1 : `$U` code 0, 0 conflit ; seul le noyau avancé (76f28bd → 58e421e) ; 8 clones tiers convertis ; liens inchangés ; `CONFORME` (3889 liens = attendu, casse et cibles comprises, 0 cassé, 0 régulier, 629 projetés = HEAD) ; 23 entrées ; extraits et `sparse-checkout` = Mac (16 fichiers) ; `clones = Mac` hors `ignorecase` et tailles ; `ignorecase` et tailles relevés ; §7.2 : rootstock neuf, 23 entrées, mêmes contrôles, liste identique à `$U`, tailles relevées |
| C3 Constructions | host ctest 7/7, mklepton = `env-50-debian` = `env-52-apres` ; 16 presets construits ; QEMU fumée et banc 20/20, 16/16, 19/19, `peripheriques` ×4 ; `comparer_R50-1` 0 pour les 16 presets |
| C4 `essais/env-13-debian` | `graft-update` (session ou utilisateur, §2) code 0, 0 conflit ; mêmes contrôles qu'au §7.1 ; `lepton check` code 0 ; espace = avant |
| C5 pytest, relais, fichiers générés | pytest 384 passed (hook 118) ; §9.2 : 12 relevés = Mac (5, 3 et 2 lignes `scion: `, échec non préfixé une seule fois), clones F7 partiels = Mac, `--json` valide, liens et graine restaurés ; §9.3 : 3 notifications attendues, 8 lignes `scion: ` dans le canal, aucune dans la notification d'échec ; §10 : `$R` codes 0, 9 clés projetées, espace = `$R50` au chemin près ; `$U` : espace = avant ; `$P` : générés, graine et `check` identiques |
| C6 Miroir | `mirror-sync --dry-run` dans `$R` : code 0, 8 miroirs, 0 à envoyer (ou références « à envoyer » expliquées par l'amont), 0 signalement ; rien envoyé ; trunk `CONFORME` |
| C7 Cartes | écarté (PA-93) |
| C8 Nettoyage | `essais/env-50-debian` et `~/env-50-journaux` supprimés (session ou utilisateur, §2 ; taille relevée), absents |

Rapport `doc/devenv/rapports/env-53-debian.md` sur `devenv/env-53-debian`. Il contient :
- l'hôte et les versions (§5, §6) ;
- la table des critères ;
- la table des presets : construction, fumée, banc KAL, `comparer_R50-1`, `comparer_Mac` ;
- pour `$U`, `$R`, `$E13` : contrôles du trunk (sortie de `controler-trunk.py`), lignes
  `clones.txt` avant et après, `ignorecase`, tailles (hors `.git`, `.git`, `depots/tiers`) ;
- pytest (§9.1), le relais en ligne de commande (§9.2) et dans VSCodium (§9.3, texte des
  notifications) ; la commande de miroir (§11) ;
- les écarts et constats ;
- le journal des messages §2bis (ID, date, résumé, remis ou non) ;
- ce qui n'a pas été fait.

Commit du rapport et de `oracles/env-53-debian/`, avec, sous
`doc/devenv/rapports/env-53-debian/` : `9.2-releves/`, `9.3-sortie-lepton.txt` et les
`clones.txt` du §7. Puis `QUESTION` à l'utilisateur pour le push (PA-P), puis `FIN-*`.
