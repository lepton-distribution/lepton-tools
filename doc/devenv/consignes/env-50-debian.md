# Consigne — session Claude Code sur la VM Debian — ENV-50 (validation Debian groupée)

Fichier autonome : avec `ORCHESTRATION.md` §2bis, il suffit à conduire la session VM. Rédigé le
2026-11-10 par la session Mac `lepton-tools-9d` (tâche 1 d'ENV-50), repris de
`consignes/env-43-debian.md`. Son texte est envoyé tel quel dans l'ordre `R50-1`.

## 1. Objet

Valider sur Debian x86_64 l'état publié après ENV-44 à ENV-49 :
- installation de scion **0.6.2.0** (ENV-44 : `graft --scion <porteur>` regreffe ses clés
  projetées, P-G6), de lepton (`main`, correctif d'ENV-48 : propriété dans un clone partagé) ;
  extension Lepton 0.5.2 inchangée ;
- `scion graft-update` de deux rootstocks existants, puis un rootstock neuf depuis la graine
  publiée. Depuis R43-1 :
  - la SPL F4 est retirée (ENV-46, −96 chemins) ;
  - la HAL et le CMSIS device F7 sont **projetés** depuis 2 miroirs (ENV-47, 201 cibles
    réorientées) ;
  - le code tiers WL est projeté depuis 4 miroirs (ENV-48 : −8 `LICENSE.txt`, +9 `LICENSE.md`),
    puis monté au couple de STM32CubeWL `v1.6.0` (ENV-49, +1 `Conf/radio_template.h`) ;
  - un `LEPTON-PROVENANCE.md` est ajouté au CMSIS V3.30 du noyau (ENV-44, D7) ;
  - la VM distingue la casse des noms de fichiers, le Mac non : c'est ici que se prouvent les
    renommages `Inc` → `inc` et `Src` → `src` du WL ;
- contenu projeté identique au commit épinglé, nom de fichier compris (629 fichiers, 8 clones
  tiers) ;
- constructions host et 16 presets : seuls les 2 presets WL55 changent de code (ENV-49) ; an386
  ne change que dans ses sections `.debug_*` (ENV-44, D5) ;
- hook `proteger-trunk.py` et scripts d'ENV-44 sur Debian (pytest de lepton-tools, compilation à
  blanc de la HAL F4) ; fichiers générés par lepton ;
- commande de miroir, à blanc, sur les 8 miroirs ;
- banc sur cartes depuis Debian, **sonde choisie par numéro** (ENV-45) : NUCLEO-F429ZI (réseau
  compris) et la paire NUCLEO-WL55JC1 (radio comprise), les trois sondes rattachées ensemble ;
- regreffe d'`essais/env-13-debian` (D8 de `HORS-PLAN.md`).

Cartes (PA-87) : l'utilisateur rattache à la VM, dans VMware Fusion, la NUCLEO-F429ZI et les deux
NUCLEO-WL55JC1. L'écriture flash est accordée pour cette session (PA-11) pour les seules images
construites sur la VM :
- sur la NUCLEO-F429ZI : `nucleo-f429zi-embos`, `nucleo-f429zi-freertos`, `nucleo-f439zi-embos` ;
- sur les WL55 A et B : `nucleo-wl55jc1-embos` et `nucleo-wl55jc1-freertos`.

Les autres presets de carte sont construits, jamais flashés.

| Carte | Sonde | N° |
| --- | --- | --- |
| NUCLEO-F429ZI (adresse 192.168.2.5 sur le câble Ethernet) | ST-LINK/V2-1 | 0672FF495252717267243842 |
| NUCLEO-WL55JC1 A | STLINK-V3 | 002700253431510837393937 |
| NUCLEO-WL55JC1 B | STLINK-V3 | 004F003E3431510937393937 |

Références publiées (toutes poussées, aucune fusion différée) :

| Dépôt (`https://github.com/lepton-distribution/…`) | Référence | Commit | En R43-1 |
| --- | --- | --- | --- |
| `lepton-tools` | `devenv/env-50` (cette consigne ; code identique à `main` c985670) | tête après `fetch` | f01e735 (`devenv/env-43`) |
| `seed.scions` | tag `0.6.2.0` | **213d2c0** | tag `0.6.1.0` 4502a70 |
| `lepton-seed.scions` | `original-tree` | 15740f9 | = |
| `lepton-original-tree.scions` (noyau) | `master` | **76f28bd** | 763dda2 |
| `lepton-famille-qemu-mps2` | `master` | 3954357 | = |
| `lepton-bsp-qemu-mps2-an386` | `master` | **10a8889** | 5819047 |
| `lepton-bsp-qemu-mps2-an500` | `master` | e98a482 | = |
| `lepton-famille-stm32f4xx` | `master` | **acdd24c** | 7afd7f1 |
| `lepton-bsp-nucleo-f429zi` | `master` | b9fe2bf | = |
| `lepton-bsp-nucleo-f439zi` | `master` | 314f91b | = |
| `lepton-famille-stm32wlxx` | `master` | **9349be2** | 2340b25 |
| `lepton-bsp-nucleo-wl55jc1` | `master` | **4d7cf80** | ef51ec1 |
| `lepton-famille-stm32f7xx` | `master` | **12280a5** | d2d9aa9 |
| `lepton-bsp-stm32f746g-disco` | `master` | 6266908 | = |
| `lepton-famille-samd21` | `master` | a262e81 | = |
| `lepton-bsp-samd21-xplained-pro` | `master` | f3cffa2 | = |
| `mirror-stm32f4xx-hal-driver` | tag `v1.8.5` | b6f0ed3 | = |
| `mirror-cmsis_device_f4` | commit épinglé, sans tag | 3c77349 (`master` 9192c7b) | = |
| `mirror-stm32f7xx-hal-driver` | tag `v1.3.3` | e1446fa | (nouveau) |
| `mirror-cmsis_device_f7` | tag `v1.2.10` | 2352e88 | (nouveau) |
| `mirror-stm32wlxx-hal-driver` | tag `v1.6.0` | 5c87cf0 | (nouveau) |
| `mirror-cmsis-device-wl` | tag `v1.4.0` | 71a0b78 | (nouveau) |
| `mirror-stm32-mw-subghz-phy` | tag `v1.5.0` | 7dc059f | (nouveau) |
| `mirror-STM32CubeWL` | tag `v1.6.0` | f934cd2 | (nouveau) |

Références Mac :
- oracle `doc/devenv/rapports/oracles/env-49-apres/` (host + 16 presets) ;
- écarts `env-42-apres` → `env-49-apres` et attendus : `rapports/env-50-mac.md` §1 et
  `rapports/env-50-mac/attendu/` ;
- trunk de `~/lepton` au Mac, mêmes commits : 23 entrées greffées, 3889 liens, 0 cassé, 629 liens
  vers `depots/tiers/` (8 clones) ; même état obtenu au Mac par `graft-update` d'un rootstock dans
  l'état de `$U` (`rapports/env-50-mac.md` §1.5).

Référence Debian : `rapports/env-43-debian.md` et `oracles/env-43-debian/`.

La session VM ne développe pas : elle exécute, constate et rapporte.

## 2. Ce que la session VM peut faire, et ne fait pas

| Autorisé | Interdit |
| --- | --- |
| `git fetch` / `switch` de `~/lepton-tools-dev/lepton-tools` (`devenv/env-50`) et `git fetch` / `merge --ff-only` du clone noyau `$K` sur `master` | Modifier `DEVENV-STATUS.md`, `ORCHESTRATION.md`, `SPECIFICATION.md`, `handoff/*.md`, les consignes, `rapports/env-50-mac*` |
| Lire les journaux des commandes lancées **par l'utilisateur** : installations (§6), `scion graft-update` (§7.1, §7.3), suppressions (§13), création éventuelle du venv (§9) | Lancer soi-même `sudo`, `pipx install`, `pip install`, les scripts d'installation, `codium --install-extension`, `scion graft-update`, `rm -rf` |
| Lectures dans `$U` et `$E13` ; `lepton check` / `generate` / `seed status` dans `$U`, `$E13`, `$P`, `$R43` et `$R` | Toute écriture dans les clones de `$U` ou de `$E13` ; tout `seed-update` ; regreffer `$P` ou `$R43`, commiter dans leur graine |
| Créer `~/lepton-tools-dev/essais/env-50-debian` (rootstock neuf, **sous ce nom** : même longueur de chemin qu'`env-43-debian`, §8) et y tout faire, `build/` compris | Écrire un fichier régulier dans un `trunk/` ou sous `depots/tiers/` ; corriger quoi que ce soit (consigner l'écart pour la session Mac) |
| `scion mirror-sync --dry-run` dans `$R` (§11) | `scion mirror-sync` **sans** `--dry-run` ; tout envoi vers un miroir |
| pytest de lepton-tools dans `~/lepton-tools-dev/venv-test`, `TMPDIR` sous `~` (§9) ; compilation à blanc dans `$J/9-hal-blanc` (§9) | Flasher une autre image que celles du §1, flasher une autre carte, modifier les octets d'option, effacement de masse, déverrouillage, toucher au démarrage du M0+ de la WL55 |
| §12 : reconfigurer `$R/build/<P>` des 5 presets de carte du §1 avec ports, numéros de sonde et adresse réseau ; `ctest -L board` (écriture flash) ; lecture OpenOCD (`init; targets; shutdown`) | Modifier la configuration réseau de la VM ; `sudo` |
| Créer `devenv/env-50-debian` (depuis `devenv/env-50`) ; y écrire `doc/devenv/rapports/env-50-debian.md` et `doc/devenv/rapports/oracles/env-50-debian/` | Commiter sur une autre branche |
| `git push origin devenv/env-50-debian` **après accord explicite de l'utilisateur** (PA-P) | Pousser toute autre branche |

Règles des consignes VM (ORCHESTRATION §2bis) :
- **Commandes confiées à l'utilisateur.** Les installations (§6), les deux `scion graft-update`
  (§7.1, §7.3), la création éventuelle du venv (§9) et les `rm -rf` (§13) sont lancés par
  l'utilisateur dès le départ ; les commandes exactes sont données plus bas. La session annonce
  l'attente par un `AVANCEMENT`, puis vérifie l'effet et le consigne.
- **Commandes lancées par la session.** `scion rootstock-install`, `seed-add`, `graft` (§7.2) et
  `rejouer-oracle.sh` (§8) ont été acceptés de R28-1 à R43-1. Si le classifieur de permissions les
  refuse, ou refuse pytest (§9), la session ne contourne pas : elle envoie un `AVANCEMENT` avec la
  commande exacte, et l'utilisateur la lance.
- **Régénérer avant de relever** : tout relevé « avant » d'un fichier généré suit immédiatement
  la commande qui le produit (§5.1).
- **Branche des clones d'un rootstock existant** : la branche courante de chaque clone de `$U` et
  de `$E13` est relevée au §5 et consignée. scion 0.6.2.0 refuse lui-même un clone hors de sa
  version déclarée ; un tel refus reste un écart à exposer.
- **scion avant toute regreffe** : aucun `graft-update`, `graft` ni `seed-add` avant que
  `scion version` donne 0.6.2.0 (§6). scion 0.6.1.0 lit les projections, mais lepton exige
  0.6.2.0.

Tout écart au plan, toute erreur non prévue : s'arrêter, exposer (`AVANCEMENT` ou `QUESTION`),
attendre.

## 3. Communication (ORCHESTRATION §2bis)

- Session principale : `lepton-tools-9d` (session Mac). Répondre à l'adresse `from` du message
  d'ordre.
- ID : `R50-1`, repris tel quel : `[ACCUSÉ R50-1] ENV-50 — …`, `[AVANCEMENT R50-1] …`,
  `[QUESTION R50-1] …`, `[FIN-SUCCÈS R50-1] …` ou `[FIN-ÉCHEC R50-1] …`.
- `ACCUSÉ`, avant toute commande autre que les lectures du §5. Il contient :
  - l'ordre reformulé en une phrase ;
  - la tête réelle de `devenv/env-50` après `fetch` ;
  - les résultats de `git ls-remote` du §5 ;
  - les branches et têtes des clones de `$U` et de `$E13` ;
  - les étapes prévues (§6 à §13) et les écarts déjà visibles.
- `AVANCEMENT` : quand l'utilisateur doit agir (§6, §7.1, §7.3, §9 si besoin, §12.1, §13), après
  chacun des §6 à §12, et à chaque arrêt. Au §12.1, donner les ports et l'adresse IP relevés :
  l'utilisateur les confirme avant le banc.
- `FIN-SUCCÈS` / `FIN-ÉCHEC` : résultat par critère du §14, commits et branche (poussée ou non),
  chemin du rapport, versions relevées, écarts, ce qui n'a pas été fait.
- **Remise en échec** (règle D9 du §2bis) : un envoi en erreur (ECONNRESET, « bridge ID is
  stale ») est renvoyé une fois, à l'identique. Si le second envoi échoue, le message entier est
  consigné dans `~/env-50-journaux/0-messages-R50-1.md` et au §Messages du rapport, avec la
  mention « non remis ». La session l'annonce à l'utilisateur, qui le relaie à la session Mac.
  Un message relayé par l'utilisateur et portant l'ID `R50-1` vaut message reçu.

## 4. Journaux et variables

```bash
mkdir -p ~/env-50-journaux
J=~/env-50-journaux
T=~/lepton-tools-dev/lepton-tools
K=~/lepton-tools-dev/lepton-noyau
R=~/lepton-tools-dev/essais/env-50-debian
R43=~/lepton-tools-dev/essais/env-43-debian
U=~/lepton-tools-dev/essais/env-28-debian
E13=~/lepton-tools-dev/essais/env-13-debian
P=~/lepton-tools-dev/essais/env-11/qemu
G=https://github.com/lepton-distribution
O=doc/devenv/rapports/oracles
X=doc/devenv/rapports/env-50-mac
A=$X/attendu
C=doc/devenv/rapports/env-43-mac/controler-trunk.py
```
Une commande par journal `$J/<étape>.log`, code de retour en dernière ligne (`code=<n>`).
Les boucles s'écrivent en bash (`bash -c '…'` ou script), pas en zsh.

## 5. Vérifications préalables (lecture seule) — C1

```bash
uname -sm; cat /etc/debian_version; uname -r; id -un; git --version
scion version | tail -1; lepton --version
arm-none-eabi-gcc --version | head -1; cmake --version | head -1; ninja --version
qemu-system-arm --version | head -1; python3 --version; codium --version | head -1; openocd --version 2>&1 | head -1
echo "LEPTON_EMBOS_ROOT=${LEPTON_EMBOS_ROOT:-absente}"; ls -d ~/lepton/third_party/embos/cortexm-gcc/5.20.0.0 2>&1
df -h ~ /tmp | tail -2
test -e "$R" && echo "ARRÊT : $R existe déjà"
ls ~/lepton-tools-dev/venv-test/bin/python 2>&1
git -C "$T" status --short | head -5
git -C "$T" fetch origin && git -C "$T" switch devenv/env-50 && git -C "$T" merge --ff-only origin/devenv/env-50 && git -C "$T" log --oneline -1
echo "scion tag $(git ls-remote $G/seed.scions.git 'refs/tags/0.6.2.0^{}' | cut -c1-7)"
echo "graine $(git ls-remote $G/lepton-seed.scions.git original-tree | cut -c1-7)"
for r in lepton-original-tree.scions lepton-famille-qemu-mps2 lepton-bsp-qemu-mps2-an386 \
         lepton-bsp-qemu-mps2-an500 lepton-famille-stm32f4xx lepton-bsp-nucleo-f429zi \
         lepton-bsp-nucleo-f439zi lepton-famille-stm32wlxx lepton-bsp-nucleo-wl55jc1 \
         lepton-famille-stm32f7xx lepton-bsp-stm32f746g-disco lepton-famille-samd21 \
         lepton-bsp-samd21-xplained-pro; do
  echo "$r $(git ls-remote $G/$r.git refs/heads/master | cut -c1-7)"
done
while read m t; do
  echo "$m $t $(git ls-remote $G/$m.git "refs/tags/$t^{}" | cut -c1-7)"
done <<EOF
mirror-stm32f4xx-hal-driver v1.8.5
mirror-stm32f7xx-hal-driver v1.3.3
mirror-cmsis_device_f7 v1.2.10
mirror-stm32wlxx-hal-driver v1.6.0
mirror-cmsis-device-wl v1.4.0
mirror-stm32-mw-subghz-phy v1.5.0
mirror-STM32CubeWL v1.6.0
EOF
echo "mirror-cmsis_device_f4 master $(git ls-remote $G/mirror-cmsis_device_f4.git refs/heads/master | cut -c1-7)"
# Rootstocks existants $U et $E13
for Z in "$U" "$E13"; do
  echo "== $Z"
  git -C "$Z"/depots/lepton-seed.scions/original-tree log --oneline -1
  git -C "$Z"/depots/lepton-seed.scions/original-tree status --short | head -5
  grep -v '^#' "$Z"/trunk/.scion.grafted.list | grep -c .
  for d in "$Z"/depots/lepton/*/*; do
    [ -d "$d/.git" ] || continue
    echo "$(basename $(dirname $d))/$(basename $d) $(git -C $d branch --show-current) $(git -C $d rev-parse --short HEAD) $(git -C $d rev-parse --abbrev-ref '@{u}' 2>&1) modifs=$(git -C $d status --short | wc -l)"
  done | tee "$J/5-clones-$(basename $Z).txt"
  echo "liens $(find "$Z"/trunk -type l | wc -l) cassés $(find -L "$Z"/trunk -type l | wc -l) réguliers $(find "$Z"/trunk -type f ! -name .scion.grafted.list | wc -l)"
  ls -d "$Z"/depots/tiers/*/* 2>&1
done
# Autres rootstocks de la VM, graines de projet qui citent les familles F4, F7, WL
ls -d "$R43" "$R43"/original-tree.code-workspace "$P"/depots/lepton-seed/env11 ~/env-43-journaux 2>&1
ls -d ~/lepton-tools-dev/essais/*/ ~/lepton-tools-dev/essais/env-11/*/ 2>&1
grep -l -r --include=.scion.sources.list -E 'stm32f4xx|stm32f7xx|stm32wlxx' ~/lepton-tools-dev/essais/*/depots/lepton-seed* ~/lepton-tools-dev/essais/env-11/*/depots/lepton-seed* 2>/dev/null
```
Attendu :
- commits du tableau du §1 ; lepton-tools propre, à la tête de `origin/devenv/env-50` ;
- scion **0.6.1.0** (avant installation) ; `lepton 0.1.0`, `scion 0.6.1.0 (requis ≥ 0.6.1.0)` ;
- chaîne APT de R43-1 : arm-none-eabi-gcc 14.2.1 (`15:14.2.rel1-1`), cmake 3.31.6, ninja 1.12.1,
  QEMU 10.0.13, Python 3.13.5, OpenOCD 0.12.0, codium 1.135.06055 ;
- `$U` (état laissé par R43-1) :
  - graine à 15740f9, propre ; **16 entrées** ;
  - 13 clones `<clé>/master` sur `master`, amont `origin/master`, aucune modification, aux
    commits de la colonne « En R43-1 » (noyau 763dda2, an386 5819047, F4 7afd7f1, WL 2340b25,
    WL55 ef51ec1, F7 d2d9aa9, les autres égaux) ;
  - 3982 liens, 0 cassé, 0 fichier régulier ;
  - 2 clones tiers : `stm32f4xx-hal-driver/v1.8.5`, `cmsis-device-f4/3c77349…` ;
- `$E13` (non regreffé depuis R13-1, 2026-10-30) : état **relevé** tel quel, sans attendu
  chiffré ; graine `original-tree` propre ;
- `$R43`, son espace, `$P` et sa graine `env11` présents ;
- graines qui citent les familles F4, F7 ou WL : seulement des clones `original-tree` (`$U`, `$R43`,
  `$E13`) ; une graine de projet qui les cite est relevée et consignée, sans arrêt.

Arrêts :
- `$R` existe ;
- lepton-tools non propre ;
- un commit publié diffère ;
- graine de `$U` ou de `$E13` modifiée ;
- un clone de `$U` hors de `master`, sans amont ou modifié ;
- un clone de `$E13` modifié (un clone hors `master` ou sans amont : `QUESTION`, sans
  `graft-update` de `$E13`) ;
- moins de 8 Go libres dans `~`.

Pas des arrêts, à consigner :
- embOS absent : les presets `*-embos*` seront en échec attendu ;
- une version de la chaîne APT différente de R43-1 (elle peut expliquer un écart au §8.1) ;
- `venv-test` absent (§9 le traite).

### 5.1 Fichiers générés : régénération puis relevé avant (pour C5)

Avec le lepton installé avant le §6 :
```bash
lepton generate -C "$P" > "$J/5.1-generate-P-avant.log" 2>&1; echo "code=$?" >> "$J/5.1-generate-P-avant.log"
lepton check -C "$P" > "$J/5.1-check-P-avant.log" 2>&1; echo "code=$?" >> "$J/5.1-check-P-avant.log"
git -C "$P"/depots/lepton-seed/env11 status --short > "$J/5.1-graine-P-avant.txt"
sha256sum "$P"/depots/lepton-seed/env11/project/scion/CMakeUserPresets.json "$P"/*.code-workspace > "$J/5.1-generes-P-avant.sha256"
lepton generate -C "$R43" > "$J/5.1-generate-R43.log" 2>&1; echo "code=$?" >> "$J/5.1-generate-R43.log"
cp "$R43"/original-tree.code-workspace "$J/5.1-R43.code-workspace"
lepton generate -C "$U" > "$J/5.1-generate-U-avant.log" 2>&1; echo "code=$?" >> "$J/5.1-generate-U-avant.log"
cp "$U"/original-tree.code-workspace "$J/5.1-U-avant.code-workspace"
lepton check -C "$E13" > "$J/5.1-check-E13-avant.log" 2>&1; echo "code=$?" >> "$J/5.1-check-E13-avant.log"
```
Attendu : codes 0 pour `$P`, `$R43` et `$U`. `check` de `$E13` : relevé, quel que soit le code.
`$R43` n'est pas regreffé : son espace sert de référence à celui de `$R` (§10.1).

## 6. Installation de scion 0.6.2.0 et de lepton (C1)

D'abord, par la session :
```bash
git -C "$K" status --short | head -5
git -C "$K" fetch origin && git -C "$K" switch master && git -C "$K" merge --ff-only origin/master && git -C "$K" log --oneline -1
grep -n '^SCION_REF=' "$K/scripts/install-debian.sh"; grep -n '^SCION_REF=' "$T/scripts/install-vscodium.sh"
grep -n 'SCION_MIN_VERSION =' "$T/lepton/__init__.py"
grep -n '"version"' "$T/extension/package.json"; ls "$T"/extension/dist/lepton-0.5.2.vsix
```
Attendu :
- clone noyau propre, à 76f28bd (763dda2 avant) ;
- `SCION_REF="${SCION_REF:-0.6.2.0}"` (noyau) et `SCION_REF="0.6.2.0"` (lepton-tools) ;
- `SCION_MIN_VERSION = (0, 6, 2, 0)` ;
- extension 0.5.2, `.vsix` présent.

Puis `AVANCEMENT` : l'**utilisateur** lance, dans un terminal de la VM (sudo avec mot de passe),
**sans** `SCION_REF` dans l'environnement (défaut du noyau), dans cet ordre (scion d'abord : lepton
exige scion ≥ 0.6.2.0) :

```bash
J=~/env-50-journaux; K=~/lepton-tools-dev/lepton-noyau; T=~/lepton-tools-dev/lepton-tools
unset SCION_REF SCION_SPEC
bash "$K/scripts/install-debian.sh" --with-debug-tools 2>&1 | tee "$J/6-install-debian.log"; echo "code=${PIPESTATUS[0]}" | tee -a "$J/6-install-debian.log"
pipx install --force "$T" 2>&1 | tee "$J/6-lepton.log"; echo "code=${PIPESTATUS[0]}" | tee -a "$J/6-lepton.log"
bash "$T/scripts/install-vscodium.sh" --lepton-clone "$K" 2>&1 | tee "$J/6-install-vscodium-1.log"; echo "code=${PIPESTATUS[0]}" | tee -a "$J/6-install-vscodium-1.log"
bash "$T/scripts/install-vscodium.sh" --lepton-clone "$K" 2>&1 | tee "$J/6-install-vscodium-2.log"; echo "code=${PIPESTATUS[0]}" | tee -a "$J/6-install-vscodium-2.log"
```
La session lit ensuite les journaux. Attendu : quatre codes 0. `install-debian.sh` installe scion
depuis `$G/seed.scions.git@0.6.2.0` (0.6.1.0 auparavant). La première exécution
d'`install-vscodium.sh` : nombre de changements relevé (extension inchangée depuis R43-1) ; la
seconde donne **`changements 0`**. Puis :
```bash
scion version | tail -1; lepton --version; codium --version | head -1
pipx list --short | grep -E '^(scion|lepton) '
dpkg-query -W -f '${Version}\n' codium; codium --list-extensions --show-versions | LC_ALL=C sort > "$J/6-extensions.txt"
grep -E -i 'lldb|lepton|rtos-views|peripheral' "$J/6-extensions.txt"
```
Attendu :
- `scion version: 0.6.2.0` ;
- `lepton 0.1.0`, `scion 0.6.2.0 (requis ≥ 0.6.2.0)` ;
- `vadimcn.vscode-lldb@1.12.3`, `lepton-distribution.lepton@0.5.2`,
  `mcu-debug.rtos-views@0.0.16`, `mcu-debug.peripheral-viewer@1.6.4`.

**Arrêt** si scion n'est pas 0.6.2.0 : aucun `graft-update` ni `graft`.

## 7. `graft-update` des rootstocks existants, rootstock neuf (C2, C4)

### 7.1 `$U`

Par la session :
```bash
cd "$U"
find trunk -type l | LC_ALL=C sort > "$J/7.1-liens-avant.txt"; wc -l < "$J/7.1-liens-avant.txt"
```
Le relevé se fait **depuis `$U`**, chemins relatifs (`trunk/…`), comme les attendus.

Puis `AVANCEMENT` : l'**utilisateur** lance :
```bash
J=~/env-50-journaux; cd ~/lepton-tools-dev/essais/env-28-debian
scion graft-update -v > "$J/7.1-graft-update.log" 2>&1; echo "code=$?" >> "$J/7.1-graft-update.log"
```
Puis la session :
```bash
cd "$U"
tail -4 "$J/7.1-graft-update.log"; grep -i -E 'conflit|refus|avancé|git clone' "$J/7.1-graft-update.log" | head -20
git -C depots/lepton-seed.scions/original-tree log --oneline -1
grep -v '^#' trunk/.scion.grafted.list | grep -c .
for d in depots/lepton/*/master; do echo "$(basename $(dirname $d)) $(git -C $d branch --show-current) $(git -C $d rev-parse --short HEAD) modifs=$(git -C $d status --short | wc -l)"; done | tee "$J/7.1-clones-apres.txt"
ls -d depots/tiers/*/*
find trunk -type l | LC_ALL=C sort > "$J/7.1-liens-apres.txt"
LC_ALL=C comm -13 "$J/7.1-liens-avant.txt" "$J/7.1-liens-apres.txt" > "$J/7.1-ajoutes.txt"
LC_ALL=C comm -23 "$J/7.1-liens-avant.txt" "$J/7.1-liens-apres.txt" > "$J/7.1-retires.txt"
diff "$T/$A/liens-ajoutes.txt" "$J/7.1-ajoutes.txt" && echo "ajouts = attendu (11)"
diff "$T/$A/liens-retires.txt" "$J/7.1-retires.txt" && echo "retraits = attendu (104)"
python3 -I "$T/$C" "$U" "$T/$A/trunk-liens.txt" "$J/7.1-controle-U" > "$J/7.1-controle-U.log" 2>&1; echo "code=$?" >> "$J/7.1-controle-U.log"
cat "$J/7.1-controle-U.log"
diff "$T/$A/projetes.txt" "$J/7.1-controle-U/projetes.txt" && echo "projetés = attendu (629)"
```
`controler-trunk.py` (lecture seule, ENV-43) relève la liste `./chemin -> cible` du trunk et la
compare à celle du Mac. Il vérifie :
- l'absence de fichier régulier et de lien cassé ;
- pour chaque lien vers `depots/tiers/` : nom suivi par git au HEAD du clone tiers sous cette
  casse exacte, et contenu égal au blob du HEAD ;
- l'état de chaque clone tiers.

Attendu (constaté au Mac sur `essais/env-13-vierge`, même état de départ que `$U`) :
- `graft-update` : code 0, 0 conflit ; graine inchangée (15740f9) ; 6 clones avancés (noyau,
  an386, F4, WL, WL55, F7) ;
- **23 entrées** (16 + 2 clés F7 + 5 clés WL ; la 6ᵉ colonne des clés projetées désigne le
  porteur) ;
- 13 clones sur `master`, propres, aux commits du §1 ;
- **8 clones tiers** : les 2 du F4 (inchangés) et 6 nouveaux, `--filter=blob:none` depuis les
  miroirs : `stm32f7xx-hal-driver/v1.3.3`, `cmsis-device-f7/v1.2.10`,
  `stm32wlxx-hal-driver/v1.6.0`, `cmsis-device-wl/v1.4.0`, `stm32-mw-subghz-phy/v1.5.0`,
  `stm32cubewl/v1.6.0` (partagé par `stm32cubewl::utilities` et `::radio-core-inc`, ≈ 156 Mo) ;
- ajouts = `attendu/liens-ajoutes.txt` (**11** : D7, 9 `LICENSE.md` WL, `Conf/radio_template.h`) ;
  retraits = `attendu/liens-retires.txt` (**104** : 96 SPL F4, 8 `LICENSE.txt` WL) ;
- `controler-trunk.py` code 0, `CONFORME` :
  - liste `chemin -> cible` identique à l'attendu (**3889** liens), 0 fichier régulier, 0 lien
    cassé ;
  - 629 projetés = `attendu/projetes.txt`, 0 écart de nom, 0 écart de contenu ;
  - 8 clones tiers aux HEAD épinglés (§1), `origin` = miroirs `$G/mirror-*.git`, 0 modification,
    filtre `blob:none`.

Toute autre ligne : écart à exposer. Si seules les cibles diffèrent (chemins identiques),
consigner les premières lignes ; c'est un écart, pas un arrêt. Une ligne « chemin(s) ignoré(s)
par git » du journal est relevée telle quelle (au Mac : 6 `.DS_Store`).

### 7.2 Rootstock neuf depuis la graine publiée

```bash
mkdir "$R" && cd "$R"
scion rootstock-install > "$J/7.2-rootstock-install.log" 2>&1; echo "code=$?" >> "$J/7.2-rootstock-install.log"
scion seed-add --version original-tree $G/lepton-seed.scions.git > "$J/7.2-seed-add.log" 2>&1; echo "code=$?" >> "$J/7.2-seed-add.log"
scion graft > "$J/7.2-graft.log" 2>&1; echo "code=$?" >> "$J/7.2-graft.log"
tail -2 "$J/7.2-graft.log"
grep -v '^#' trunk/.scion.grafted.list | grep -c .
for d in depots/lepton/*/master; do echo "$d $(git -C $d branch --show-current) $(git -C $d rev-parse --short HEAD)"; done
python3 -I "$T/$C" "$R" "$T/$A/trunk-liens.txt" "$J/7.2-controle-R" > "$J/7.2-controle-R.log" 2>&1; echo "code=$?" >> "$J/7.2-controle-R.log"
cat "$J/7.2-controle-R.log"
diff "$J/7.1-controle-U/liens.txt" "$J/7.2-controle-R/liens.txt" && echo "liste identique à \$U"
```
Attendu :
- codes 0 ; « 3889 feuilles liées » ; 23 entrées ; chaque clone sur `master` au commit du §1 ;
- `controler-trunk.py` code 0, `CONFORME`, comme au §7.1 ;
- liste identique à celle de `$U`.

### 7.3 `$E13` (D8) — C4

Le relevé du §5 donne l'état de départ. Si un clone de `$E13` est hors `master`, sans amont ou
modifié : `QUESTION`, pas de `graft-update`. Sinon, par la session :
```bash
cd "$E13"
find trunk -type l | LC_ALL=C sort > "$J/7.3-liens-avant.txt"; wc -l < "$J/7.3-liens-avant.txt"
```
Puis `AVANCEMENT` : l'**utilisateur** lance :
```bash
J=~/env-50-journaux; cd ~/lepton-tools-dev/essais/env-13-debian
scion graft-update -v > "$J/7.3-graft-update.log" 2>&1; echo "code=$?" >> "$J/7.3-graft-update.log"
```
Puis la session :
```bash
cd "$E13"
tail -4 "$J/7.3-graft-update.log"; grep -i -E 'conflit|refus|graine|avancé' "$J/7.3-graft-update.log" | head -20
git -C depots/lepton-seed.scions/original-tree log --oneline -1
grep -v '^#' trunk/.scion.grafted.list | grep -c .
for d in depots/lepton/*/master; do echo "$(basename $(dirname $d)) $(git -C $d branch --show-current) $(git -C $d rev-parse --short HEAD) modifs=$(git -C $d status --short | wc -l)"; done | tee "$J/7.3-clones-apres.txt"
python3 -I "$T/$C" "$E13" "$T/$A/trunk-liens.txt" "$J/7.3-controle-E13" > "$J/7.3-controle-E13.log" 2>&1; echo "code=$?" >> "$J/7.3-controle-E13.log"
cat "$J/7.3-controle-E13.log"
lepton check -C "$E13" > "$J/7.3-check-E13.log" 2>&1; echo "code=$?" >> "$J/7.3-check-E13.log"; tail -3 "$J/7.3-check-E13.log"
lepton generate -C "$E13" > "$J/7.3-generate-E13.log" 2>&1; echo "code=$?" >> "$J/7.3-generate-E13.log"; tail -1 "$J/7.3-generate-E13.log"
```
Attendu :
- `graft-update` code 0, 0 conflit ; graine avancée par avance rapide jusqu'à 15740f9 (si elle
  était en retard) ; nouveaux greffons de la graine clonés ;
- 23 entrées ; 13 clones sur `master` aux commits du §1, propres ;
- `controler-trunk.py` code 0, `CONFORME` (même liste que `$U`) ;
- `lepton check` **code 0** ; `generate` code 0.

Un refus de scion (clone hors version, graine divergée) : écart à exposer, sans contournement.

## 8. Reconstructions et comparaisons (C3)

Périmètre : host et les 16 presets croisés (QEMU : construction, fumée, banc KAL ; cartes :
construction et capture seulement). `$R` s'appelle `env-50-debian` : les chaînes `__FILE__` des
presets FreeRTOS suivent le chemin du rootstock. `env-43-debian` a la même longueur, sinon `.text`
diffère.

```bash
cd "$T" && git switch -c devenv/env-50-debian devenv/env-50
scripts/oracle/rejouer-oracle.sh "$R" $O/env-50-debian \
  --qemu qemu-mps2-an386-embos --qemu qemu-mps2-an386-embos-soft \
  --qemu qemu-mps2-an386-freertos --qemu qemu-mps2-an386-freertos-soft \
  --qemu qemu-mps2-an500-embos --qemu qemu-mps2-an500-freertos \
  --carte nucleo-f429zi-embos --carte nucleo-f429zi-freertos \
  --carte nucleo-f439zi-embos --carte nucleo-f439zi-freertos \
  --carte nucleo-wl55jc1-embos --carte nucleo-wl55jc1-freertos \
  --carte samd21-xplained-pro-embos --carte samd21-xplained-pro-freertos \
  --carte stm32f746g-disco-embos --carte stm32f746g-disco-freertos > "$J/8-rejouer.log" 2>&1; echo "code=$?" >> "$J/8-rejouer.log"
tail -25 "$J/8-rejouer.log"
grep -h "tests passed" $O/env-50-debian/*/ctest.log $O/env-50-debian/*/banc-kal.log
grep -h "peripheriques" $O/env-50-debian/qemu-mps2-an386-*/banc-kal.log
find -L "$R/trunk" -type l | wc -l; find "$R/trunk" -type f ! -name .scion.grafted.list | wc -l
```
Attendu :
- code 0 ; host ctest 7/7 ; 16 presets construits ; fumée réussie ;
- banc QEMU **identique à R43-1** : an386 20/20, an386 soft 16/16, an500 19/19
  (`net.ping_ftpd` ne tourne que sous Linux) ;
- `qemu-mps2-an386.peripheriques` **Passed** dans les 4 `banc-kal.log` an386 ;
- trunk sans fichier régulier ni lien cassé.

### 8.1 Comparaisons

La non-régression Debian se lit **par rapport à R43-1** et aux écarts constatés au Mac entre
`env-42-apres` et `env-49-apres` (`rapports/env-50-mac.md` §1.1). Normalisation : noms seuls (les
tailles diffèrent entre la chaîne du Mac et la chaîne APT), sections `.debug_*` exclues. Leçon
E-1 de R43-1 (PA-74) : sur Debian, `.text` varie par pas de 64 octets (bourrage d'alignement) ; la
croissance du code se lit sur la somme des symboles (`croissance.py`), pas sur la seule ligne
`.text`.

```bash
cd "$T"
norm() { grep -E '^(section|symbole)' "$1" | sed -E 's/ \[.*$//; s/ +: /: /' | grep -v -E '^section [^:]*: \.debug_' | LC_ALL=C sort; }
diff -q $O/env-43-debian/host/mklepton-empreintes.sha256 $O/env-50-debian/host/mklepton-empreintes.sha256 && echo "mklepton = R43-1"
diff -q $O/env-49-apres/host/mklepton-empreintes.sha256 $O/env-50-debian/host/mklepton-empreintes.sha256 && echo "mklepton = Mac env-49-apres"
for p in $(ls $O/env-50-debian | grep -v -e host -e ctest-N -e compilation -e '\.log$'); do
  python3 scripts/oracle/comparer-oracle.py $O/env-43-debian/$p $O/env-50-debian/$p > "$J/8.1-cmp-R43-$p.txt" 2>&1; a=$?
  python3 scripts/oracle/comparer-oracle.py $O/env-49-apres/$p $O/env-50-debian/$p > "$J/8.1-cmp-Mac-$p.txt" 2>&1; b=$?
  echo "$p comparer_R43-1=$a comparer_Mac=$b hors_debug=$(norm $J/8.1-cmp-R43-$p.txt | wc -l) $(python3 $X/croissance.py $O/env-43-debian/$p $O/env-50-debian/$p)"
done | tee "$J/8.1-bilan.txt"
for p in nucleo-wl55jc1-embos nucleo-wl55jc1-freertos; do
  norm "$J/8.1-cmp-R43-$p.txt" | grep -v '^section ' > "$J/8.1-$p.noms.txt"
  diff "$A/$p.noms.txt" "$J/8.1-$p.noms.txt" > "$J/8.1-$p.noms.diff" && echo "$p : symboles = Mac (26 lignes)" || echo "$p : DIFFÈRE"
  grep -E '^section ' "$J/8.1-cmp-R43-$p.txt" | grep -v '\.debug_'
done
for s in embos freertos; do
  python3 scripts/oracle/comparer-oracle.py $O/env-50-debian/nucleo-f429zi-$s $O/env-50-debian/nucleo-f439zi-$s > "$J/8.1-f429-f439-$s.txt" 2>&1; echo "f429→f439 $s=$? hors_debug=$(norm $J/8.1-f429-f439-$s.txt | wc -l)"
done
```

Attendu :
- mklepton : empreintes identiques à `env-43-debian` et à `env-49-apres`.
- `comparer_R43-1` des **10 presets** sans changement de code (`nucleo-f4{29,39}zi-{embos,freertos}`,
  `qemu-mps2-an500-{embos,freertos}`, `stm32f746g-disco-{embos,freertos}`,
  `samd21-xplained-pro-{embos,freertos}`) : **0**. ENV-46, ENV-47 et ENV-48 n'ont changé aucun
  binaire au Mac (code 0 ×16).
- `qemu-mps2-an386-*` ×4 (D5 d'ENV-44, `ARMCM4_FP.h`) : code 0 ou 1, **`hors_debug=0`** (seules
  des sections `.debug_*` changent), `code_symboles +0 .text +0`.
- `nucleo-wl55jc1-{embos,freertos}` (ENV-49) : code **1** ;
  - lignes de symboles normalisées **identiques** à `attendu/<preset>.noms.txt` (26 : 2 ajoutés,
    3 retirés, 21 modifiés ; HAL SUBGHZ et UART, pile radio) ;
  - `code_symboles +36` (Mac +36) ;
  - `.text` : 0 ou un multiple positif de 64 (Mac +48) ;
  - aucune autre section chargée (`.data`, `.bss`, `.isr_vector`, `.rodata`…) ne change.
- Écarts à exposer, pas à corriger : un delta négatif ; une autre section chargée changée ; une
  ligne d'un `8.1-<preset>.noms.diff` (en donner l'extrait) ; un `code_symboles` ≠ +36 pour la
  WL55 ou ≠ 0 ailleurs.
- `comparer_Mac` : informatif (chaînes différentes ; 1 attendu partout).
- `f429→f439` : code 1, `hors_debug=0`.

## 9. Hook, scripts d'ENV-44 et contenu projeté (C5)

Contenu projeté : contrôlé au §7 (`controler-trunk.py`), 629 fichiers égaux au blob du HEAD des
clones épinglés, noms suivis par git sous la même casse.

### 9.1 pytest de lepton-tools (hook D3 d'ENV-44 compris)

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
Attendu (Mac, 2026-11-10, Python 3.11.5) :
- suite complète : code 0, **377 passed** (environ 7 min) ;
- `tests/test_proteger_trunk.py` : **118 passed** ;
- lepton-tools reste propre (hors rapport et oracle de la session).

Un test ignoré ou en échec : relever son nom et son message (`-rs`), relancer ce test seul une
fois, consigner les deux résultats ; pas de correction.

### 9.2 Compilation à blanc de la HAL F4 (D6 d'ENV-44)

```bash
cd "$T"
scripts/tiers/compiler-hal-f4-a-blanc.sh "$R" "$J/9.2-hal-blanc" > "$J/9.2-hal-blanc.log" 2>&1; echo "code=$?" >> "$J/9.2-hal-blanc.log"
tail -1 "$J/9.2-hal-blanc.log"; cat "$J/9.2-hal-blanc/resume.txt"; cat "$J"/9.2-hal-blanc/*/echecs.txt 2>/dev/null
diff <(grep -v '^# arm-none-eabi-gcc' "$A/compilation-a-blanc-resume.txt") <(grep -v '^# arm-none-eabi-gcc' "$J/9.2-hal-blanc/resume.txt") && echo "résumé = Mac (hors ligne du compilateur)"
mkdir -p $O/env-50-debian/compilation-a-blanc && cp "$J/9.2-hal-blanc/resume.txt" $O/env-50-debian/compilation-a-blanc/
find "$R/trunk" -type f ! -name .scion.grafted.list | wc -l
```
Attendu :
- **code 0** (en R43-1 : 1, la ligne `v330`, retirée en ENV-44) ;
- résumé identique à celui du Mac hors la ligne du compilateur : STM32F429xx et STM32F439xx,
  ordre `cmsis5`, 90 sources, 0 échec, 0 avertissement, `core_cm4.h` de
  `cmsis-5/CMSIS/Core/Include` ; plus aucune ligne `v330` ;
- aucun fichier régulier ajouté au trunk.

## 10. Fichiers générés par lepton (C5)

Aucune graine de projet de la VM ne remplace les familles F4, F7 ou WL (relevé du §5). Conduite
d'ENV-41 (PA-69) : regreffe avec scion 0.6.2.0, puis `check` et `generate` à code 0 ; `seed
status` montre les 9 clés projetées ; l'espace de travail ne gagne aucun dossier « git · » des
clones tiers.

### 10.1 Rootstock neuf `$R` contre `$R43`

```bash
lepton check -C "$R" > "$J/10.1-check-R.log" 2>&1; echo "code=$?" >> "$J/10.1-check-R.log"
lepton generate -C "$R" > "$J/10.1-generate-R.log" 2>&1; echo "code=$?" >> "$J/10.1-generate-R.log"
lepton seed status -C "$R" > "$J/10.1-seed-status-R.log" 2>&1; echo "code=$?" >> "$J/10.1-seed-status-R.log"
grep -E 'projection|^trunk' "$J/10.1-seed-status-R.log"
W="$R"/original-tree.code-workspace
for k in '"request"' '"svdFile"' '"type": "lldb"' 'tests des greffons' 'tiers'; do echo "$k $(grep -c "$k" "$W")"; done
diff <(sed "s#$R43#<R>#g" "$J/5.1-R43.code-workspace") <(sed "s#$R#<R>#g" "$W") > "$J/10.1-espace.diff"; echo "diff=$?"; head -40 "$J/10.1-espace.diff"
```
Attendu (Mac, `essais/env-13-vierge` regreffé) :
- `check`, `generate`, `seed status` code 0 ;
- `seed status` : 9 lignes `projection`, aux versions du §1 et HEAD épinglés :
  `stm32f4xx-hal-driver` (200 fichiers), `cmsis-device-f4` (6), `stm32wlxx-hal-driver` (157),
  `cmsis-device-wl` (6), `stm32-mw-subghz-phy` (20), `stm32cubewl::utilities` (38),
  `stm32cubewl::radio-core-inc` (1), `stm32f7xx-hal-driver` (196), `cmsis-device-f7` (5) ;
  `trunk : aucun fichier régulier, aucun lien cassé` ;
- espace : 23 `"request"`, 10 `"svdFile"`, 7 `"type": "lldb"`, 4 tâches « tests des greffons »,
  0 `tiers` ;
- espace **identique** à celui de `$R43` au chemin du rootstock près (`diff=0`).

Une différence (série de sonde, chemin d'outil, dossier de clone) : la relever telle quelle,
l'exposer.

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
Attendu : codes 0 ; générés, graine et sortie de `check` identiques. `$P` n'est pas regreffé et
est QEMU seul : ce contrôle établit la stabilité du nouveau lepton.

## 11. Commande de miroir, à blanc (C6)

Contrôle des 8 miroirs contre leur amont, sans envoi. `$R` porte les déclarations de miroir
(`scion/.scion/.scion.mirrors` des familles F4, F7 et WL).

```bash
cd "$R"
scion mirror-sync --dry-run -v > "$J/11-mirror-sync.log" 2>&1; echo "code=$?" >> "$J/11-mirror-sync.log"
grep -E 'référence\(s\) à envoyer|signalement' "$J/11-mirror-sync.log"; tail -1 "$J/11-mirror-sync.log"
ls -d depots/.mirrors/*/*/* 2>&1
python3 -I "$T/$C" "$R" "$T/$A/trunk-liens.txt" "$J/11-controle-R" | tail -1
```
Attendu (essai au Mac le 2026-11-10, `essais/env-13-vierge`) :
- code 0 ;
- 8 lignes `miroir … : 0 référence(s) à envoyer, 0 signalement(s)` ;
- 8 dépôts de travail sous `depots/.mirrors/github.com/lepton-distribution/` (≈ 80 Mo) ;
- trunk toujours `CONFORME`.

Une référence « à envoyer » n'est admise que si une publication amont postérieure au 2026-11-10
l'explique : la relever, puis relever la référence de l'amont
(`git ls-remote https://github.com/STMicroelectronics/<nom>.git`), sans arrêt ; elle ne sera pas
envoyée. Un signalement (tag déplacé, branche réécrite ou supprimée) est un écart à exposer.
Jamais sans `--dry-run`.

## 12. Banc sur cartes, sonde choisie par numéro (C7)

Forme de R43-1 (§12), commandes en clair. Les scripts de banc du Mac
(`rapports/env-35-hal-f4/banc-carte.sh`, `rapports/env-42-core-cm4/banc-wl55.sh`) appellent
`caffeinate` (macOS seul) : ne pas les lancer sur la VM. Depuis ENV-45, `-DLEPTON_BOARD_PROBE_SERIAL`
fait générer `<build>/openocd-<bsp>.cfg`, qui annonce « Lepton : sonde demandée <n°> » et ajoute
`adapter serial <n°>`. Les trois sondes sont rattachées ensemble : la consigne d'R43-1 (une seule
sonde ST) ne s'applique plus.

Références :
- NUCLEO-F429ZI, Debian R43-1 (`rapports/env-43-debian.md` §7) : 20/20 pour les 3 images, fumée
  `cortexM4-stm32f4`, ping 3/3, LIST 13 entrées, RETR 57 octets identique, `ECONNRESET=15`.
  Images inchangées depuis (code 0, §8.1).
- Paire WL55, Mac `env-49-apres` (`rapports/env-49-wl-hal/bancs-apres.out`) : 16/16 en embOS et
  en FreeRTOS, fumée `cortexM4-stm32wlxx`, radio : `emis=20/20` et `recus=20/20 perdus=0` dans
  les deux sens, `reponses=20/20 perdues=0` en ping-pong, 2 jetons reçus. Images changées
  depuis R43-1 (§8.1).

### 12.1 Sondes, ports série, droits, réseau

`AVANCEMENT` : l'**utilisateur** rattache à la VM (VMware Fusion, menu des périphériques USB) la
NUCLEO-F429ZI et les deux NUCLEO-WL55JC1 ; le Mac ne les voit plus. Puis la session, en lecture
seule :
```bash
id -nG; ls -l /dev/ttyACM* 2>&1; ls -l /dev/serial/by-id/ 2>&1
lsusb 2>&1 | grep -i -E 'st-?link|0483:' ; ls /etc/udev/rules.d/ /usr/lib/udev/rules.d/ 2>/dev/null | grep -i openocd
F429CFG="$R"/trunk/sys/root/src/kernel/dev/bsp/nucleo-f429zi/debug/openocd-nucleo-f439zi.cfg
WLCFG="$R"/trunk/sys/root/src/kernel/dev/bsp/nucleo-wl55jc1/debug/openocd-nucleo-wl55jc1.cfg
while read cfg n nom; do
  openocd -f "$cfg" -c "adapter serial $n" -c "init; targets; shutdown" > "$J/12.1-openocd-$nom.log" 2>&1; echo "code=$?" >> "$J/12.1-openocd-$nom.log"
  echo "== $nom"; grep -E -i 'serial|target voltage|cortex|Error|code=' "$J/12.1-openocd-$nom.log"
done <<EOF
$F429CFG 0672FF495252717267243842 f429
$WLCFG 002700253431510837393937 wl55-A
$WLCFG 004F003E3431510937393937 wl55-B
EOF
openocd -f "$WLCFG" -c "adapter serial 000000000000000000000000" -c "init; shutdown" > "$J/12.1-openocd-numero-faux.log" 2>&1; echo "code=$?" >> "$J/12.1-openocd-numero-faux.log"; tail -3 "$J/12.1-openocd-numero-faux.log"
ip -4 -o addr show | awk '{print $2, $4}'
ip route get 192.168.2.5
ping -c 3 -W 2 192.168.2.5 > "$J/12.1-ping-carte.log" 2>&1; echo "code=$?" >> "$J/12.1-ping-carte.log"
```
Attendu :
- **trois** sondes ST : ST-LINK/V2-1 (`0483:374b`) n° 0672FF…, deux STLINK-V3 (`0483:374e`,
  `rapports/env-45-sonde.md` §1.7) n° 0027… et 004F… ; trois ports `/dev/ttyACM*`, chacun nommé
  par son numéro de série sous `/dev/serial/by-id/` ;
- OpenOCD, pour chaque numéro, code 0 sans sudo : `stm32f4x.cpu` (F429), `stm32wlx.cpu0` (WL55 A
  et B, cœur M4) ;
- numéro faux : code non nul, aucune sonde prise (ST-LINK `Error: open failed`) ;
- ports lisibles et inscriptibles par l'utilisateur (R43-1 : `root:plugdev` + ACL `uaccess`) ;
- une interface de la VM sur 192.168.2.0/24 (R43-1 : `ens37` 192.168.2.20/16) ;
- le ping de la carte peut échouer si l'image en flash ne répond pas (pas un arrêt).

Une sonde absente ou une sonde de plus : arrêt, `AVANCEMENT` pour que l'utilisateur corrige le
rattachement.

Si un droit manque (OpenOCD : `LIBUSB_ERROR_ACCESS` ; port : `Permission denied`) :
`AVANCEMENT` avec la commande exacte pour l'**utilisateur**, selon le cas :
```bash
sudo usermod -aG dialout,plugdev "$USER"          # puis fermer et rouvrir la session de la VM
sudo cp /usr/lib/udev/rules.d/60-openocd.rules /etc/udev/rules.d/ 2>/dev/null; sudo udevadm control --reload-rules && sudo udevadm trigger
```
La seconde commande ne sert que si aucune règle `60-openocd.rules` n'est active. La session
revérifie, consigne la commande lancée et son effet. Si c'est toujours bloqué : `QUESTION`, sans
contournement (ni `sudo openocd`, ni `chmod` du périphérique).

Puis `AVANCEMENT` : ports relevés, sous la forme `/dev/serial/by-id/…` (`F429_PORT`, `WLA_PORT`,
`WLB_PORT`, avec le `/dev/ttyACM<n>` de chacun), et adresse IPv4 de la VM sur 192.168.2.0/24
(`HOSTIP`). **L'utilisateur confirme ports et adresse** avant tout flash. Aucune interface sur
192.168.2.0/24 : arrêt et `QUESTION` (pas de modification réseau par la session).

### 12.2 NUCLEO-F429ZI : 3 images

Après confirmation, dans cet ordre :
```bash
F429=0672FF495252717267243842; F429_PORT=<port confirmé>; HOSTIP=<adresse confirmée>
export PYTHONDONTWRITEBYTECODE=1
source "$R"/depots/lepton/original/master/scripts/lepton-env.sh > /dev/null
cd "$T"
for P in nucleo-f429zi-embos nucleo-f429zi-freertos nucleo-f439zi-embos; do
  D=$T/$O/env-50-debian/$P; B=$R/build/$P
  { cmake -S "$R/trunk" -B "$B" --preset "$P" -DLEPTON_BOARD_SERIAL_PORT="$F429_PORT" -DLEPTON_BOARD_PROBE_SERIAL="$F429" -DLEPTON_NET_TEST_HOST_IP="$HOSTIP" && cmake --build "$B"; } > "$D/carte-config.log" 2>&1; echo "code=$?" >> "$D/carte-config.log"
  ls "$B"/openocd-*.cfg; grep -h 'adapter serial' "$B"/openocd-*.cfg
  Y=$(mktemp -d); scripts/oracle/capturer-oracle.sh "$B/lepton.elf" "$Y" > /dev/null
  python3 scripts/oracle/comparer-oracle.py "$D" "$Y" > "$D/carte-oracle.txt" 2>&1; rc=$?; echo "$P oracle=$rc"; rm -rf "$Y"
  [ "$rc" -eq 0 ] || { echo "ARRÊT : $P différent de l'oracle"; break; }
  (cd "$R/trunk" && ctest --preset "$P" -L board --output-on-failure) > "$D/carte.log" 2>&1; echo "$P ctest=$?"
  cp "$B/Testing/Temporary/LastTest.log" "$D/carte-detail.log" 2>/dev/null
  cp "$B/smoke_lsh_board.log" "$D/fumee-carte.log" 2>/dev/null
  cp "$B/board_net.log" "$D/reseau-carte.log" 2>/dev/null
  grep -E 'tests passed|tests failed' "$D/carte.log"
done
for P in nucleo-f429zi-embos nucleo-f429zi-freertos nucleo-f439zi-embos; do
  D=$T/$O/env-50-debian/$P
  echo "== $P"; grep -E 'Total Tests|tests passed' "$D/carte.log"
  grep -a -o 'Lepton : sonde demandée [0-9A-F]*' "$D/carte-detail.log" | sort | uniq -c
  grep -a -o 'cortexM4-stm32f4' "$D/fumee-carte.log" | head -1
  grep -a -i -E 'ping|LIST|RETR|ECONNRESET' "$D/carte-detail.log" | head -12
done
```
Un `oracle=` non nul veut dire que l'image reconfigurée diffère de celle du §8 : arrêt avant
`ctest` pour ce preset, `AVANCEMENT` avec l'extrait de `carte-oracle.txt`. La synthèse de
`board_net` est dans `carte-detail.log` (`LastTest.log`).

Attendu, pour chacune des 3 images :
- cfg générée `openocd-nucleo-f429zi.cfg` (ou `openocd-nucleo-f439zi.cfg`) avec
  `adapter serial 0672FF495252717267243842` ; « Lepton : sonde demandée 0672FF… » dans
  `carte-detail.log`, jamais un autre numéro ;
- `oracle=0` ; `ctest=0`, **20/20** (`board.smoke_lsh`, banc KAL sur carte, `board.net`) ;
- fumée `cortexM4-stm32f4` ;
- réseau : ping 3/3, LIST 13 entrées, RETR 57 octets identique à la référence, `ECONNRESET=15`.

### 12.3 Paire NUCLEO-WL55JC1 : 2 images, radio comprise

La même image est flashée sur A (cfg générée `openocd-nucleo-wl55jc1.cfg`) et sur B (cfg
`openocd-nucleo-wl55jc1-paire.cfg`, par `LEPTON_RADIO_PEER_STLINK_SERIAL`) ; le test
`nucleo-wl55jc1.radio`, fourni par le BSP, passe en dernier.
```bash
WLA=002700253431510837393937; WLA_PORT=<port A confirmé>
WLB=004F003E3431510937393937; WLB_PORT=<port B confirmé>
export PYTHONDONTWRITEBYTECODE=1
source "$R"/depots/lepton/original/master/scripts/lepton-env.sh > /dev/null
cd "$T"
for P in nucleo-wl55jc1-embos nucleo-wl55jc1-freertos; do
  D=$T/$O/env-50-debian/$P; B=$R/build/$P
  { cmake -S "$R/trunk" -B "$B" --preset "$P" -DLEPTON_BOARD_SERIAL_PORT="$WLA_PORT" -DLEPTON_BOARD_PROBE_SERIAL="$WLA" \
      -DLEPTON_RADIO_PEER_SERIAL_PORT="$WLB_PORT" -DLEPTON_RADIO_PEER_STLINK_SERIAL="$WLB" && cmake --build "$B"; } > "$D/carte-config.log" 2>&1; echo "code=$?" >> "$D/carte-config.log"
  ls "$B"/openocd-*.cfg; grep -h 'adapter serial' "$B"/openocd-*.cfg
  Y=$(mktemp -d); scripts/oracle/capturer-oracle.sh "$B/lepton.elf" "$Y" > /dev/null
  python3 scripts/oracle/comparer-oracle.py "$D" "$Y" > "$D/carte-oracle.txt" 2>&1; rc=$?; echo "$P oracle=$rc"; rm -rf "$Y"
  [ "$rc" -eq 0 ] || { echo "ARRÊT : $P différent de l'oracle"; break; }
  (cd "$R/trunk" && ctest --preset "$P" -L board --output-on-failure) > "$D/carte.log" 2>&1; echo "$P ctest=$?"
  cp "$B/Testing/Temporary/LastTest.log" "$D/carte-detail.log" 2>/dev/null
  cp "$B/smoke_lsh_board.log" "$D/fumee-carte.log" 2>/dev/null
  cp "$B/board_radio.log" "$D/radio-carte.log" 2>/dev/null
  grep -E 'tests passed|tests failed' "$D/carte.log"
done
for P in nucleo-wl55jc1-embos nucleo-wl55jc1-freertos; do
  D=$T/$O/env-50-debian/$P
  echo "== $P"; grep -E 'Total Tests|tests passed' "$D/carte.log"
  grep -a -o 'Lepton : sonde demandée [0-9A-F]*' "$D/carte-detail.log" | sort | uniq -c
  grep -a -o 'cortexM4-stm32wlxx' "$D/fumee-carte.log" | head -1
  LC_ALL=C grep -a -hE 'radiotst (tx|rx|ping|pong) :' "$D/radio-carte.log"
  LC_ALL=C grep -a -cE '^lepton#[0-9]+\$ +lepton-radio-(A-vers-B|B-vers-A)' "$D/radio-carte.log"
done
find "$R/trunk" -type f ! -name .scion.grafted.list | wc -l; find "$R/trunk" -name __pycache__ | wc -l
```
Attendu, pour chacune des 2 images :
- cfg générées `openocd-nucleo-wl55jc1.cfg` (`adapter serial 0027…`) et
  `openocd-nucleo-wl55jc1-paire.cfg` (`adapter serial 004F…`) ;
- `oracle=0` ; `ctest=0`, **16/16** (`board.smoke_lsh`, `kal.board_flash`, 13 tests KAL,
  `nucleo-wl55jc1.radio`) ;
- « Lepton : sonde demandée » ne cite que 002700253431510837393937 (au Mac : 14 fois) ;
- fumée `cortexM4-stm32wlxx` ;
- radio : `emis=20/20` et `recus=20/20 perdus=0 desordre=0 doublons=0` deux fois (A vers B, B
  vers A), `reponses=20/20 perdues=0` et `pong : reponses=20/20` ; 2 jetons reçus ;
- trunk sans fichier régulier ni `__pycache__`.

Un test en échec : relever `carte-detail.log` (extrait), relancer ce test une fois seul
(`ctest --preset <P> -R <test>`) et consigner les deux résultats ; pas de correction. Les cartes
gardent les dernières images de la VM (`nucleo-f439zi-embos` sur la F429, `nucleo-wl55jc1-freertos`
sur A et B). Après le banc, l'utilisateur peut les rattacher de nouveau au Mac (à consigner).

## 13. Nettoyage de la VM (C8)

Accordé au PA-87. Après le §10.1 (l'espace de `$R43` est copié au §5.1), relevé par la session :
```bash
du -sh "$R43" ~/env-43-journaux
```
Puis `AVANCEMENT` : l'**utilisateur** lance :
```bash
rm -rf ~/lepton-tools-dev/essais/env-43-debian ~/env-43-journaux
```
La session vérifie `ls -d ~/lepton-tools-dev/essais/env-43-debian ~/env-43-journaux 2>&1` (absents).
Conservés : `$U` (`essais/env-28-debian`), `$E13` (`essais/env-13-debian`), regreffés au §7 ; `$R`
(`essais/env-50-debian`) ; `$P` ; `$J` ; `~/tmp-pytest` (à vider par l'utilisateur s'il le
souhaite, hors critère).

## 14. Critères et rapport

| Critère | Attendu |
| --- | --- |
| C1 Versions | `git ls-remote` conforme au §1 ; scion 0.6.2.0 par `install-debian.sh` (défaut `SCION_REF`) ; lepton `pipx` code 0, `lepton 0.1.0`, scion 0.6.2.0 accepté ; extension 0.5.2, seconde exécution d'`install-vscodium.sh` `changements 0` ; chaîne APT relevée |
| C2 `graft-update` et rootstock | §7.1 : `$U` code 0, 0 conflit ; 6 clones avancés ; 6 clones tiers créés depuis les miroirs aux commits épinglés ; ajouts (11) et retraits (104) = attendu ; `controler-trunk.py` `CONFORME` (3889 liens = attendu, casse et cibles comprises, 0 cassé, 0 régulier, 629 projetés = HEAD) ; 23 entrées ; §7.2 : rootstock neuf, 23 entrées, `CONFORME`, liste identique à `$U` |
| C3 Constructions | host ctest 7/7, mklepton = `env-43-debian` = `env-49-apres` ; 16 presets construits ; QEMU fumée et banc 20/20, 16/16, 19/19 ; `comparer_R43-1` : 10 presets 0, an386 ×4 `hors_debug=0`, WL55 ×2 symboles = Mac et `code_symboles +36`, `.text` 0 ou +64·k, aucune autre section chargée changée ; `f429→f439` hors `.debug_*` 0 |
| C4 `essais/env-13-debian` (D8) | `graft-update` par l'utilisateur code 0, 0 conflit ; 23 entrées ; `CONFORME` ; `lepton check` code 0 |
| C5 Hook, scripts, fichiers générés | pytest 377 passed (hook 118) ; compilation à blanc code 0, résumé = Mac hors ligne du compilateur ; `$R` : `check`, `generate`, `seed status` 0, 9 clés projetées, espace = `$R43` au chemin près ; `$U` : codes 0, espace = avant ; `$P` : générés, graine et `check` identiques |
| C6 Miroir | `mirror-sync --dry-run` dans `$R` : code 0, 8 miroirs, 0 à envoyer (ou références « à envoyer » expliquées par l'amont), 0 signalement ; rien envoyé ; trunk `CONFORME` |
| C7 Cartes, sonde par numéro | trois sondes vues de la VM, chacune choisie par son numéro, droits sans sudo ; numéro faux refusé ; ports et IP confirmés par l'utilisateur ; 5 `lepton.elf` reconfigurés = oracle `env-50-debian` (code 0) ; F429 : 20/20 ×3, fumée `cortexM4-stm32f4`, réseau ping 3/3, LIST 13, RETR 57 octets identique, `ECONNRESET=15` ; WL55 : 16/16 ×2, fumée `cortexM4-stm32wlxx`, radio 20/20 dans les deux sens et en ping-pong ; seule la sonde demandée est utilisée |
| C8 Nettoyage | `essais/env-43-debian` et `~/env-43-journaux` supprimés par l'utilisateur (taille relevée), absents |

Rapport `doc/devenv/rapports/env-50-debian.md` sur `devenv/env-50-debian`. Il contient :
- l'hôte et les versions (§5, §6) ;
- la table des critères ;
- la table des presets : construction, fumée, banc KAL, symboles R50-1 / R43-1 / Mac
  `env-49-apres`, `comparer_R43-1`, `comparer_Mac`, `code_symboles` et `.text` ;
- les contrôles du trunk (§7, sortie de `controler-trunk.py`) pour `$U`, `$R`, `$E13` ;
- pytest et la compilation à blanc (§9) ; la commande de miroir (§11) ; les cartes (§12) ;
- les écarts et constats ;
- le journal des messages §2bis (ID, date, résumé, remis ou non) ;
- ce qui n'a pas été fait.

Commit du rapport et de `oracles/env-50-debian/` (`compilation-a-blanc/` et journaux de carte
compris), puis `QUESTION` à l'utilisateur pour le push (PA-P), puis `FIN-*`.
