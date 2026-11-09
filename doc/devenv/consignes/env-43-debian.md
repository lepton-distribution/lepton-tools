# Consigne — session Claude Code sur la VM Debian — ENV-43 (validation Debian groupée)

Fichier autonome : avec `ORCHESTRATION.md` §2bis, il suffit à conduire la session VM. Rédigé le
2026-11-09 par la session Mac `validation-debian-env-43` (tâche 1 d'ENV-43), repris de
`consignes/env-36-debian.md`. Son texte est envoyé tel quel dans l'ordre `R43-1`.

## 1. Objet

Valider sur Debian x86_64 l'état publié après ENV-37 à ENV-42 :
- installation de scion 0.6.1.0 (projection d'un dépôt tiers, ENV-39 ; miroir de conservation,
  ENV-40), de lepton (clés projetées, ENV-41) et de l'extension Lepton 0.5.2 ;
- `scion graft-update` d'un rootstock existant. La HAL STM32F4 v1.8.5 et le CMSIS device F4 ne
  viennent plus du clone de la famille : ils sont **projetés** depuis deux clones tiers, créés
  depuis les miroirs `lepton-distribution/mirror-*` (ENV-41). Quatre `LEPTON-PROVENANCE.md` de la
  famille WL sont ajoutés (ENV-37). Puis rootstock neuf depuis la graine publiée. La VM distingue
  la casse des noms de fichiers, le Mac non ;
- contenu projeté identique au commit épinglé, nom de fichier compris ;
- constructions host et 16 presets : seuls les 10 presets Cortex-M4 changent (CMSIS-Core 5.9.0,
  ENV-42), avec les mêmes écarts que sur le Mac ;
- compilation à blanc de la HAL F4 ;
- fichiers générés par lepton ;
- commande de miroir, à blanc ;
- banc sur carte NUCLEO-F429ZI depuis Debian, réseau compris (§12).

Carte (PA-73) : la NUCLEO-F429ZI (ST-LINK/V2-1 0672FF495252717267243842, adresse 192.168.2.5 sur
le câble Ethernet) est rattachée à la VM par l'utilisateur dans VMware Fusion. Elle doit être la
**seule sonde ST** rattachée à la VM. L'écriture flash est accordée pour cette session (PA-11),
pour les seules images `nucleo-f429zi-embos`, `nucleo-f429zi-freertos` et `nucleo-f439zi-embos`
construites sur la VM. Les autres presets de carte sont construits, jamais flashés.

Références publiées (toutes poussées, aucune fusion différée) :

| Dépôt (`https://github.com/lepton-distribution/…`) | Référence | Commit | En R36-1 |
| --- | --- | --- | --- |
| `lepton-tools` | `devenv/env-43` (cette consigne ; code identique à `main` 13109dc) | tête après `fetch` | bd7ad59 (`devenv/env-36`) |
| `seed.scions` | tag `0.6.1.0` | 4502a70 | tag `0.5.4.0` 99aa973 |
| `lepton-seed.scions` | `original-tree` | 15740f9 | = |
| `lepton-original-tree.scions` (noyau) | `master` | **763dda2** | 2893297 |
| `lepton-famille-qemu-mps2` | `master` | 3954357 | = |
| `lepton-bsp-qemu-mps2-an386` | `master` | **5819047** | 09f4943 |
| `lepton-bsp-qemu-mps2-an500` | `master` | e98a482 | = |
| `lepton-famille-stm32f4xx` | `master` | **7afd7f1** | 0fd8b2a |
| `lepton-bsp-nucleo-f429zi` | `master` | b9fe2bf | = |
| `lepton-bsp-nucleo-f439zi` | `master` | 314f91b | = |
| `lepton-famille-stm32wlxx` | `master` | **2340b25** | dbc58d7 |
| `lepton-bsp-nucleo-wl55jc1` | `master` | ef51ec1 | = |
| `lepton-famille-stm32f7xx` | `master` | d2d9aa9 | = |
| `lepton-bsp-stm32f746g-disco` | `master` | 6266908 | = |
| `lepton-famille-samd21` | `master` | a262e81 | = |
| `lepton-bsp-samd21-xplained-pro` | `master` | f3cffa2 | = |
| `mirror-stm32f4xx-hal-driver` | tag `v1.8.5` | b6f0ed3 | (nouveau) |
| `mirror-cmsis_device_f4` | commit épinglé, sans tag | 3c77349 (`master` 9192c7b) | (nouveau) |

Références Mac :
- oracle `doc/devenv/rapports/oracles/env-42-apres/` (host + 16 presets) ;
- écarts `env-35-apres` → `env-42-apres` et attendus : `rapports/env-43-mac.md` §1 et
  `rapports/env-43-mac/attendu/` ;
- trunk de `~/lepton` au Mac, mêmes commits : 16 entrées greffées (14 + 2 clés projetées),
  3982 liens, 0 cassé, 206 liens vers `depots/tiers/`.

Référence Debian : `rapports/env-36-debian.md` et `oracles/env-36-debian/`.

La session VM ne développe pas : elle exécute, constate et rapporte.

## 2. Ce que la session VM peut faire, et ne fait pas

| Autorisé | Interdit |
| --- | --- |
| `git fetch` / `switch` de `~/lepton-tools-dev/lepton-tools` (`devenv/env-43`) et `git fetch` / `merge --ff-only` du clone noyau `$K` sur `master` | Modifier `DEVENV-STATUS.md`, `ORCHESTRATION.md`, `SPECIFICATION.md`, `handoff/*.md`, les consignes, `rapports/env-43-mac*` |
| Lire les journaux des commandes lancées **par l'utilisateur** : installations (§6), `scion graft-update` (§7.1), suppressions (§13) | Lancer soi-même `sudo`, `pipx install`, les scripts d'installation, `codium --install-extension`, `scion graft-update`, `rm -rf` |
| Lectures dans `$U` ; `lepton check` / `generate` / `seed status` dans `$U`, `$P`, `$R36` et `$R` | Toute écriture dans les clones de `$U` ; tout `seed-update` ; regreffer `$P` ou `$R36`, commiter dans leur graine |
| Créer `~/lepton-tools-dev/essais/env-43-debian` (rootstock neuf, **sous ce nom** : même longueur de chemin qu'`env-36-debian`, §8) et y tout faire, `build/` compris | Écrire un fichier régulier dans un `trunk/` ou sous `depots/tiers/` ; corriger quoi que ce soit (consigner l'écart pour la session Mac) |
| `scion mirror-sync --dry-run` dans `$R` (§11) | `scion mirror-sync` **sans** `--dry-run` ; tout envoi vers un miroir |
| Compilation à blanc dans `$J/9-hal-blanc` (§9) | Flasher une autre image que les 3 du §12, flasher une autre carte, modifier les octets d'option, effacement de masse ou déverrouillage |
| §12 : reconfigurer `$R/build/<P>` des 3 presets avec `LEPTON_BOARD_SERIAL_PORT` et `LEPTON_NET_TEST_HOST_IP`, `ctest -L board` (écriture flash), lecture OpenOCD (`init; targets; shutdown`) | Modifier la configuration réseau de la VM ; `sudo` |
| Créer `devenv/env-43-debian` (depuis `devenv/env-43`) ; y écrire `doc/devenv/rapports/env-43-debian.md` et `doc/devenv/rapports/oracles/env-43-debian/` | Commiter sur une autre branche |
| `git push origin devenv/env-43-debian` **après accord explicite de l'utilisateur** (PA-P) | Pousser toute autre branche |

Règles des consignes VM (ORCHESTRATION §2bis) :
- **Commandes confiées à l'utilisateur.** Les installations (§6), `scion graft-update` (§7.1) et
  `rm -rf` (§13) sont lancés par l'utilisateur dès le départ ; les commandes exactes sont données
  plus bas. La session annonce l'attente par un `AVANCEMENT`, puis vérifie l'effet et le consigne.
- **Commandes lancées par la session.** `scion rootstock-install`, `seed-add`, `graft` (§7.2) et
  `rejouer-oracle.sh` (§8) ont été acceptés en R28-1 à R36-1. Si le classifieur de permissions les
  refuse, la session ne contourne pas : elle envoie un `AVANCEMENT` avec la commande exacte, et
  l'utilisateur la lance.
- **Régénérer avant de relever** : tout relevé « avant » d'un fichier généré suit immédiatement
  la commande qui le produit (§5.1).
- **Branche des clones d'un rootstock existant** : la branche courante de chaque clone de `$U`
  est relevée au §5 et consignée. scion 0.6.1.0 refuse lui-même un clone hors de sa version
  déclarée ; un tel refus reste un écart à exposer.
- **scion avant toute regreffe** : aucun `graft-update`, `graft` ni `seed-add` avant que
  `scion version` donne 0.6.1.0 (§6). Un scion antérieur ne lit pas les projections et
  greffe la famille F4 sans HAL.

Tout écart au plan, toute erreur non prévue : s'arrêter, exposer (`AVANCEMENT` ou `QUESTION`),
attendre.

## 3. Communication (ORCHESTRATION §2bis)

- Session principale : `validation-debian-env-43` (session Mac). Répondre à l'adresse `from` du
  message d'ordre.
- ID : `R43-1`, repris tel quel : `[ACCUSÉ R43-1] ENV-43 — …`, `[AVANCEMENT R43-1] …`,
  `[QUESTION R43-1] …`, `[FIN-SUCCÈS R43-1] …` ou `[FIN-ÉCHEC R43-1] …`.
- `ACCUSÉ`, avant toute commande autre que les lectures du §5. Il contient :
  - l'ordre reformulé en une phrase ;
  - la tête réelle de `devenv/env-43` après `fetch` ;
  - les résultats de `git ls-remote` du §5 ;
  - les branches et têtes des clones de `$U` ;
  - les étapes prévues (§6 à §13) et les écarts déjà visibles.
- `AVANCEMENT` : quand l'utilisateur doit agir (§6, §7.1, §12.1, §13), après chacun des §6 à
  §12, et à chaque arrêt. Au §12.1, donner l'adresse IP relevée : l'utilisateur la confirme
  avant le banc.
- `FIN-SUCCÈS` / `FIN-ÉCHEC` : résultat par critère du §14, commits et branche (poussée ou non),
  chemin du rapport, versions relevées, écarts, ce qui n'a pas été fait.
- Premier `ACCUSÉ` perdu deux fois (ECONNRESET, R33-1 et R36-1) : en cas d'erreur d'envoi,
  renvoyer une fois, à l'identique.

## 4. Journaux et variables

```bash
mkdir -p ~/env-43-journaux
J=~/env-43-journaux
T=~/lepton-tools-dev/lepton-tools
K=~/lepton-tools-dev/lepton-noyau
R=~/lepton-tools-dev/essais/env-43-debian
R36=~/lepton-tools-dev/essais/env-36-debian
U=~/lepton-tools-dev/essais/env-28-debian
P=~/lepton-tools-dev/essais/env-11/qemu
G=https://github.com/lepton-distribution
O=doc/devenv/rapports/oracles
X=doc/devenv/rapports/env-43-mac
A=$X/attendu
```
Une commande par journal `$J/<étape>.log`, code de retour en dernière ligne (`code=<n>`).

## 5. Vérifications préalables (lecture seule) — C1

```bash
uname -sm; cat /etc/debian_version; uname -r; id -un; git --version
scion version | tail -1; lepton --version
arm-none-eabi-gcc --version | head -1; cmake --version | head -1; ninja --version
qemu-system-arm --version | head -1; python3 --version; codium --version | head -1
echo "LEPTON_EMBOS_ROOT=${LEPTON_EMBOS_ROOT:-absente}"; ls -d ~/lepton/third_party/embos/cortexm-gcc/5.20.0.0 2>&1
df -h ~ /tmp | tail -2
test -e "$R" && echo "ARRÊT : $R existe déjà"
git -C "$T" status --short | head -5
git -C "$T" fetch origin && git -C "$T" switch devenv/env-43 && git -C "$T" merge --ff-only origin/devenv/env-43 && git -C "$T" log --oneline -1
echo "scion tag $(git ls-remote $G/seed.scions.git 'refs/tags/0.6.1.0^{}' | cut -c1-7)"
echo "graine $(git ls-remote $G/lepton-seed.scions.git original-tree | cut -c1-7)"
for r in lepton-original-tree.scions lepton-famille-qemu-mps2 lepton-bsp-qemu-mps2-an386 \
         lepton-bsp-qemu-mps2-an500 lepton-famille-stm32f4xx lepton-bsp-nucleo-f429zi \
         lepton-bsp-nucleo-f439zi lepton-famille-stm32wlxx lepton-bsp-nucleo-wl55jc1 \
         lepton-famille-stm32f7xx lepton-bsp-stm32f746g-disco lepton-famille-samd21 \
         lepton-bsp-samd21-xplained-pro; do
  echo "$r $(git ls-remote $G/$r.git refs/heads/master | cut -c1-7)"
done
echo "mirror-hal v1.8.5 $(git ls-remote $G/mirror-stm32f4xx-hal-driver.git 'refs/tags/v1.8.5^{}' | cut -c1-7)"
echo "mirror-cmsis master $(git ls-remote $G/mirror-cmsis_device_f4.git refs/heads/master | cut -c1-7)"
# Rootstock existant $U
git -C "$U"/depots/lepton-seed.scions/original-tree log --oneline -1
git -C "$U"/depots/lepton-seed.scions/original-tree status --short | head -5
grep -v '^#' "$U"/trunk/.scion.grafted.list | grep -c .
for d in "$U"/depots/lepton/*/master; do
  echo "$(basename $(dirname $d)) $(git -C $d branch --show-current) $(git -C $d rev-parse --short HEAD) $(git -C $d rev-parse --abbrev-ref '@{u}' 2>&1) modifs=$(git -C $d status --short | wc -l)"
done | tee "$J/5-clones-U.txt"
echo "liens $(find "$U"/trunk -type l | wc -l) cassés $(find -L "$U"/trunk -type l | wc -l) réguliers $(find "$U"/trunk -type f ! -name .scion.grafted.list | wc -l)"
ls -A "$U"; ls -d "$U"/depots/tiers 2>&1
# Autres rootstocks de la VM, graines de projet qui citent la famille F4
ls -d "$R36" "$R36"/original-tree.code-workspace "$P"/depots/lepton-seed/env11 ~/env-36-journaux 2>&1
ls -d ~/lepton-tools-dev/essais/*/ ~/lepton-tools-dev/essais/env-11/*/ 2>&1
grep -l -r --include=.scion.sources.list -e stm32f4xx ~/lepton-tools-dev/essais/*/depots/lepton-seed* ~/lepton-tools-dev/essais/env-11/*/depots/lepton-seed* 2>/dev/null
```
Attendu :
- commits du tableau du §1 ; lepton-tools propre, à la tête de `origin/devenv/env-43` ;
- scion **0.5.4.0** (avant installation) ; `lepton 0.1.0`, `scion 0.5.4.0 (requis ≥ 0.5.4.0)` ;
- chaîne APT de R36-1 : arm-none-eabi-gcc 14.2.1 (`15:14.2.rel1-1`), cmake 3.31.6, ninja 1.12.1,
  QEMU 10.0.13, Python 3.13.5, codium 1.135.06055 ;
- `$U` : graine à 15740f9, propre ; 14 entrées greffées ; **13 clones sur `master`**, amont
  `origin/master`, aucune modification, aux commits de la colonne « En R36-1 » (noyau 2893297,
  `bsp-qemu-mps2-an386` 09f4943, `family-stm32f4xx` 0fd8b2a, `family-stm32wlxx` dbc58d7, les autres
  égaux) ; 3978 liens, 0 cassé, 0 fichier régulier ; pas de `depots/tiers` ;
- `$R36`, son espace, `$P` et sa graine `env11` présents ;
- graines qui citent la famille F4 : seulement des clones `original-tree` (`$U`, `$R36`,
  éventuellement `env-14-debian`) ; une graine de projet qui la cite est relevée et consignée,
  sans arrêt.

Arrêts :
- `$R` existe ;
- lepton-tools non propre ;
- un commit publié diffère ;
- graine de `$U` modifiée ;
- un clone de `$U` hors de `master`, sans amont ou modifié ;
- moins de 8 Go libres dans `~`.

Pas des arrêts, à consigner :
- embOS absent : les presets `*-embos*` seront en échec attendu ;
- une version de la chaîne APT différente de R36-1 (elle peut expliquer un écart au §8.1).

### 5.1 Fichiers générés : régénération puis relevé avant (pour C5)

Avec le lepton installé avant le §6 :
```bash
lepton generate -C "$P" > "$J/5.1-generate-P-avant.log" 2>&1; echo "code=$?" >> "$J/5.1-generate-P-avant.log"
lepton check -C "$P" > "$J/5.1-check-P-avant.log" 2>&1; echo "code=$?" >> "$J/5.1-check-P-avant.log"
git -C "$P"/depots/lepton-seed/env11 status --short > "$J/5.1-graine-P-avant.txt"
sha256sum "$P"/depots/lepton-seed/env11/project/scion/CMakeUserPresets.json "$P"/*.code-workspace > "$J/5.1-generes-P-avant.sha256"
lepton generate -C "$R36" > "$J/5.1-generate-R36.log" 2>&1; echo "code=$?" >> "$J/5.1-generate-R36.log"
cp "$R36"/original-tree.code-workspace "$J/5.1-R36.code-workspace"
lepton generate -C "$U" > "$J/5.1-generate-U-avant.log" 2>&1; echo "code=$?" >> "$J/5.1-generate-U-avant.log"
cp "$U"/original-tree.code-workspace "$J/5.1-U-avant.code-workspace"
```
Attendu : codes 0. `$R36` n'est pas regreffé : son espace sert de référence à celui de `$R` (§10.1).

## 6. Installation de scion 0.6.1.0, de lepton et de l'extension (C1)

D'abord, par la session :
```bash
git -C "$K" status --short | head -5
git -C "$K" fetch origin && git -C "$K" switch master && git -C "$K" merge --ff-only origin/master && git -C "$K" log --oneline -1
grep -n '^SCION_REF=' "$K/scripts/install-debian.sh"; grep -n '^SCION_REF=' "$T/scripts/install-vscodium.sh"
grep -n '"version"' "$T/extension/package.json"; ls "$T"/extension/dist/lepton-0.5.2.vsix
```
Attendu :
- clone noyau propre, à 763dda2 ;
- `SCION_REF="${SCION_REF:-0.6.1.0}"` (noyau) et `SCION_REF="0.6.1.0"` (lepton-tools) ;
- extension 0.5.2, `.vsix` présent.

Puis `AVANCEMENT` : l'**utilisateur** lance, dans un terminal de la VM (sudo avec mot de passe),
**sans** `SCION_REF` dans l'environnement (défaut du noyau), dans cet ordre (scion d'abord : lepton
exige scion ≥ 0.6.1.0) :

```bash
J=~/env-43-journaux; K=~/lepton-tools-dev/lepton-noyau; T=~/lepton-tools-dev/lepton-tools
unset SCION_REF SCION_SPEC
bash "$K/scripts/install-debian.sh" --with-debug-tools 2>&1 | tee "$J/6-install-debian.log"; echo "code=${PIPESTATUS[0]}" | tee -a "$J/6-install-debian.log"
pipx install --force "$T" 2>&1 | tee "$J/6-lepton.log"; echo "code=${PIPESTATUS[0]}" | tee -a "$J/6-lepton.log"
bash "$T/scripts/install-vscodium.sh" --lepton-clone "$K" 2>&1 | tee "$J/6-install-vscodium-1.log"; echo "code=${PIPESTATUS[0]}" | tee -a "$J/6-install-vscodium-1.log"
bash "$T/scripts/install-vscodium.sh" --lepton-clone "$K" 2>&1 | tee "$J/6-install-vscodium-2.log"; echo "code=${PIPESTATUS[0]}" | tee -a "$J/6-install-vscodium-2.log"
```
La session lit ensuite les journaux. Attendu : quatre codes 0. `install-debian.sh` installe scion
depuis `$G/seed.scions.git@0.6.1.0` (0.5.4.0 auparavant). La première exécution
d'`install-vscodium.sh` installe l'extension 0.5.2 (0.5.1 auparavant) ; la seconde donne
**`changements 0`**. Puis :
```bash
scion version | tail -1; lepton --version; codium --version | head -1
pipx list --short | grep -E '^(scion|lepton) '
scion mirror-sync -h | head -3
dpkg-query -W -f '${Version}\n' codium; codium --list-extensions --show-versions | LC_ALL=C sort > "$J/6-extensions.txt"
grep -E -i 'lldb|lepton|rtos-views|peripheral' "$J/6-extensions.txt"
```
Attendu :
- `scion version: 0.6.1.0` ; `scion mirror-sync` connu ;
- `lepton 0.1.0`, `scion 0.6.1.0 (requis ≥ 0.6.1.0)` ;
- `vadimcn.vscode-lldb@1.12.3`, `lepton-distribution.lepton@0.5.2`,
  `mcu-debug.rtos-views@0.0.16`, `mcu-debug.peripheral-viewer@1.6.4`.

**Arrêt** si scion n'est pas 0.6.1.0 : aucun `graft-update` ni `graft`.

## 7. `graft-update` d'un rootstock existant, rootstock neuf (C2)

### 7.1 `$U`

Par la session :
```bash
cd "$U"
find trunk -type l | LC_ALL=C sort > "$J/7.1-liens-avant.txt"; wc -l < "$J/7.1-liens-avant.txt"
```
Puis `AVANCEMENT` : l'**utilisateur** lance :
```bash
J=~/env-43-journaux; cd ~/lepton-tools-dev/essais/env-28-debian
scion graft-update -v > "$J/7.1-graft-update.log" 2>&1; echo "code=$?" >> "$J/7.1-graft-update.log"
```
Puis la session :
```bash
cd "$U"
tail -15 "$J/7.1-graft-update.log"; grep -i -E 'graine|conflit|refus|projet|tiers' "$J/7.1-graft-update.log" | head -20
git -C depots/lepton-seed.scions/original-tree log --oneline -1
grep -v '^#' trunk/.scion.grafted.list | grep -c .
for d in depots/lepton/*/master; do echo "$(basename $(dirname $d)) $(git -C $d branch --show-current) $(git -C $d rev-parse --short HEAD) modifs=$(git -C $d status --short | wc -l)"; done | tee "$J/7.1-clones-apres.txt"
ls -d depots/tiers/*/*
find trunk -type l | LC_ALL=C sort > "$J/7.1-liens-apres.txt"
LC_ALL=C comm -13 "$J/7.1-liens-avant.txt" "$J/7.1-liens-apres.txt" > "$J/7.1-ajoutes.txt"
LC_ALL=C comm -23 "$J/7.1-liens-avant.txt" "$J/7.1-liens-apres.txt" > "$J/7.1-retires.txt"
diff "$T/$A/liens-ajoutes.txt" "$J/7.1-ajoutes.txt" && echo "ajouts = attendu (4)"
diff "$T/$A/liens-retires.txt" "$J/7.1-retires.txt" && echo "retraits = attendu (0)"
python3 -I "$T/$X/controler-trunk.py" "$U" "$T/$A/trunk-liens.txt" "$J/7.1-controle-U" > "$J/7.1-controle-U.log" 2>&1; echo "code=$?" >> "$J/7.1-controle-U.log"
cat "$J/7.1-controle-U.log"
diff "$T/$A/projetes.txt" "$J/7.1-controle-U/projetes.txt" && echo "projetés = attendu (206)"
```
`controler-trunk.py` (lecture seule) relève la liste `./chemin -> cible` du trunk et la compare à
celle du Mac. Il vérifie :
- l'absence de fichier régulier et de lien cassé ;
- pour chaque lien vers `depots/tiers/` : nom suivi par git au HEAD du clone tiers sous cette
  casse exacte, et contenu égal au blob du HEAD ;
- l'état de chaque clone tiers.

Attendu :
- `graft-update` : code 0, 0 conflit ; graine inchangée (15740f9) ;
- **16 entrées** (14 + `tiers@stm32f4xx-hal-driver`, `tiers@cmsis-device-f4`) ;
- 13 clones sur `master`, propres, aux commits du §1 (noyau, BSP an386, familles F4 et WL avancés
  par avance rapide) ;
- 2 clones tiers : `depots/tiers/stm32f4xx-hal-driver/v1.8.5`,
  `depots/tiers/cmsis-device-f4/3c77349ce04c8af401454cc51f85ea9a50e34fc1` ;
- ajouts identiques à `attendu/liens-ajoutes.txt` (4 `LEPTON-PROVENANCE.md` de la famille WL) ;
  **aucun retrait** ;
- `controler-trunk.py` code 0, `CONFORME` :
  - liste `chemin -> cible` identique à l'attendu (3982 liens), 0 fichier régulier, 0 lien cassé ;
  - 206 projetés = `attendu/projetes.txt`, 0 écart de nom, 0 écart de contenu ;
  - clones tiers : HEAD b6f0ed3829f3… et 3c77349ce04c…, `origin` = miroirs
    `$G/mirror-stm32f4xx-hal-driver.git` et `$G/mirror-cmsis_device_f4.git`, 0 modification,
    filtre `blob:none`.

Toute autre ligne : écart à exposer. Si seules les cibles diffèrent (chemins identiques),
consigner les premières lignes ; c'est un écart, pas un arrêt.

### 7.2 Rootstock neuf depuis la graine publiée

```bash
mkdir "$R" && cd "$R"
scion rootstock-install > "$J/7.2-rootstock-install.log" 2>&1; echo "code=$?" >> "$J/7.2-rootstock-install.log"
scion seed-add --version original-tree $G/lepton-seed.scions.git > "$J/7.2-seed-add.log" 2>&1; echo "code=$?" >> "$J/7.2-seed-add.log"
scion graft > "$J/7.2-graft.log" 2>&1; echo "code=$?" >> "$J/7.2-graft.log"
grep -v '^#' trunk/.scion.grafted.list | grep -c .
for d in depots/lepton/*/master; do echo "$d $(git -C $d branch --show-current) $(git -C $d rev-parse --short HEAD)"; done
python3 -I "$T/$X/controler-trunk.py" "$R" "$T/$A/trunk-liens.txt" "$J/7.2-controle-R" > "$J/7.2-controle-R.log" 2>&1; echo "code=$?" >> "$J/7.2-controle-R.log"
cat "$J/7.2-controle-R.log"
diff "$J/7.1-controle-U/liens.txt" "$J/7.2-controle-R/liens.txt" && echo "liste identique à \$U"
```
Attendu :
- codes 0 ; 16 entrées ; chaque clone sur `master` au commit du §1 ;
- `controler-trunk.py` code 0, `CONFORME`, comme au §7.1 ;
- liste identique à celle de `$U`.

## 8. Reconstructions et comparaisons (C3)

Périmètre : host et les 16 presets croisés (QEMU : construction, fumée, banc KAL ; cartes :
construction et capture seulement). `$R` garde le nom `env-43-debian` : les chaînes `__FILE__`
des presets FreeRTOS suivent le chemin du rootstock. `env-36-debian` a la même longueur, sinon
`.text` diffère.

```bash
cd "$T" && git switch -c devenv/env-43-debian devenv/env-43
scripts/oracle/rejouer-oracle.sh "$R" $O/env-43-debian \
  --qemu qemu-mps2-an386-embos --qemu qemu-mps2-an386-embos-soft \
  --qemu qemu-mps2-an386-freertos --qemu qemu-mps2-an386-freertos-soft \
  --qemu qemu-mps2-an500-embos --qemu qemu-mps2-an500-freertos \
  --carte nucleo-f429zi-embos --carte nucleo-f429zi-freertos \
  --carte nucleo-f439zi-embos --carte nucleo-f439zi-freertos \
  --carte nucleo-wl55jc1-embos --carte nucleo-wl55jc1-freertos \
  --carte samd21-xplained-pro-embos --carte samd21-xplained-pro-freertos \
  --carte stm32f746g-disco-embos --carte stm32f746g-disco-freertos > "$J/8-rejouer.log" 2>&1; echo "code=$?" >> "$J/8-rejouer.log"
tail -25 "$J/8-rejouer.log"
grep -h "tests passed" $O/env-43-debian/*/ctest.log $O/env-43-debian/*/banc-kal.log
grep -h "peripheriques" $O/env-43-debian/qemu-mps2-an386-*/banc-kal.log
find -L "$R/trunk" -type l | wc -l; find "$R/trunk" -type f ! -name .scion.grafted.list | wc -l
```
Attendu :
- code 0 ; host ctest 7/7 ; 16 presets construits ; fumée réussie ;
- banc QEMU **identique à R36-1** (aucun test QEMU changé depuis) : an386 20/20, an386 soft
  16/16, an500 19/19 (`net.ping_ftpd` ne tourne que sous Linux) ;
- `qemu-mps2-an386.peripheriques` **Passed** dans les 4 `banc-kal.log` an386 ;
- trunk sans fichier régulier ni lien cassé.

### 8.1 Comparaisons

La non-régression Debian se lit **par rapport à R36-1** et aux écarts constatés au Mac entre
`env-35-apres` et `env-42-apres` (`rapports/env-43-mac.md` §1.1). ENV-37 et ENV-41 n'ont changé
aucun binaire ; ENV-42 change les 10 presets M4. Normalisation : noms seuls (les tailles diffèrent
entre la chaîne du Mac et la chaîne APT), sections `.debug_*` exclues.

```bash
cd "$T"
norm() { grep -E '^(section|symbole)' "$1" | sed -E 's/ \[.*$//; s/ +: /: /' | grep -v -E '^section [^:]*: \.debug_' | LC_ALL=C sort; }
diff -q $O/env-36-debian/host/mklepton-empreintes.sha256 $O/env-43-debian/host/mklepton-empreintes.sha256 && echo "mklepton = R36-1"
diff -q $O/env-42-apres/host/mklepton-empreintes.sha256 $O/env-43-debian/host/mklepton-empreintes.sha256 && echo "mklepton = Mac env-42-apres"
for p in $(ls $O/env-43-debian | grep -v -e host -e ctest-N -e compilation -e '\.log$'); do
  python3 scripts/oracle/comparer-oracle.py $O/env-36-debian/$p $O/env-43-debian/$p > "$J/8.1-cmp-R36-$p.txt" 2>&1; a=$?
  python3 scripts/oracle/comparer-oracle.py $O/env-42-apres/$p $O/env-43-debian/$p > "$J/8.1-cmp-Mac-$p.txt" 2>&1; b=$?
  echo "$p comparer_R36-1=$a comparer_Mac=$b symboles=$(wc -l < $O/env-43-debian/$p/symboles.txt)"
done | tee "$J/8.1-bilan.txt"
for f in $A/*.noms.txt; do
  p=$(basename $f .noms.txt)
  norm "$J/8.1-cmp-R36-$p.txt" > "$J/8.1-$p.noms.txt"
  diff "$f" "$J/8.1-$p.noms.txt" > "$J/8.1-$p.noms.diff" && echo "$p : écarts = Mac ($(wc -l < $f) lignes)" || echo "$p : DIFFÈRE"
  grep -E '^section modifié +: \.(text|data|bss|noinit|ccm|rodata)' "$J/8.1-cmp-R36-$p.txt"
done
for s in embos freertos; do
  python3 scripts/oracle/comparer-oracle.py $O/env-43-debian/nucleo-f429zi-$s $O/env-43-debian/nucleo-f439zi-$s > "$J/8.1-f429-f439-$s.txt" 2>&1; echo "f429→f439 $s=$? hors_debug=$(norm $J/8.1-f429-f439-$s.txt | wc -l)"
done
```

Attendu :
- mklepton : empreintes identiques à `env-36-debian` et à `env-42-apres`.
- `comparer_R36-1` des **6 presets hors M4** (`qemu-mps2-an500-{embos,freertos}`,
  `stm32f746g-disco-{embos,freertos}`, `samd21-xplained-pro-{embos,freertos}`) : **0**.
- `comparer_R36-1` des **10 presets M4** : **1**, et la liste normalisée **identique** à
  `attendu/<preset>.noms.txt` :
  - an386 ×4 (3 lignes) : `.text`, `qemu_mps2_eth_irq_enable` et `qemu_mps2_uart_irq_enable`
    modifiés ;
  - WL55 ×2 (5 lignes) : `.text`, `NVIC_SetPriority.constprop.0` → `__NVIC_SetPriority.constprop.0`,
    `HAL_NVIC_{Disable,Enable}IRQ` modifiés ;
  - F429 et F439 ×4 (10 lignes) : `.text`, `NVIC_{Disable,Enable}IRQ` → `__NVIC_*`,
    `nucleo_f439zi_eth_irq_enable` et 4 `uart_*` modifiés.
- Seule `.text` change parmi les sections chargées. Deltas au Mac (`attendu/comparaisons-mac/`) :
  +16 (an386, WL55), +32 (F4 embOS), +48 (F4 FreeRTOS). Les valeurs Debian sont relevées. Les cas
  suivants sont des écarts à exposer, pas à corriger : un delta négatif ; une autre section
  chargée (`.data`, `.bss`, `.noinit`, `.ccm*`, `.rodata`) changée ; toute ligne d'un
  `8.1-<preset>.noms.diff` (en donner l'extrait).
- `comparer_Mac` : informatif (chaînes différentes ; 1 attendu partout).
- `f429→f439` : code 1, `hors_debug=0`.

## 9. Contenu projeté et compilation à blanc de la HAL F4 (C4)

Contenu projeté : contrôlé au §7 (`controler-trunk.py`). C'est le contrôle d'ENV-41 : 206
fichiers égaux au blob du HEAD des clones épinglés, noms suivis par git sous la même casse.

```bash
cd "$T"
scripts/tiers/compiler-hal-f4-a-blanc.sh "$R" "$J/9-hal-blanc" > "$J/9-hal-blanc.log" 2>&1; echo "code=$?" >> "$J/9-hal-blanc.log"
cat "$J/9-hal-blanc/resume.txt"; cat "$J"/9-hal-blanc/*/echecs.txt 2>/dev/null
diff $O/env-36-debian/compilation-a-blanc/resume.txt "$J/9-hal-blanc/resume.txt" && echo "résumé = R36-1"
mkdir -p $O/env-43-debian/compilation-a-blanc && cp "$J/9-hal-blanc/resume.txt" $O/env-43-debian/compilation-a-blanc/
find "$R/trunk" -type f ! -name .scion.grafted.list | wc -l
```
Attendu :
- code 1 : la ligne `v330`, gardée pour comparaison, échoue par construction ;
- résumé **identique** à celui de R36-1 : 90 sources par ligne ; `cmsis5` (STM32F429xx,
  STM32F439xx) **0 en échec** ; `v330` 1 en échec (`stm32f4xx_ll_usb`) ; 0 avertissement ;
- depuis ENV-42, les presets M4 compilent dans l'ordre `cmsis5` ;
- aucun fichier régulier ajouté au trunk. La HAL est lue par le trunk à travers les liens vers
  `depots/tiers/`.

## 10. Fichiers générés par lepton (C5)

Aucune graine de projet de la VM ne remplace la famille F4 (relevé du §5). La conduite d'ENV-41
(PA-69) s'applique : regreffe avec scion 0.6.1.0, puis `check` et `generate` à code 0 ; `seed
status` montre les 2 clés projetées ; l'espace de travail ne gagne aucun dossier « git · » des
clones tiers.

### 10.1 Rootstock neuf `$R` contre `$R36`

```bash
lepton check -C "$R" > "$J/10.1-check-R.log" 2>&1; echo "code=$?" >> "$J/10.1-check-R.log"
lepton generate -C "$R" > "$J/10.1-generate-R.log" 2>&1; echo "code=$?" >> "$J/10.1-generate-R.log"
lepton seed status -C "$R" > "$J/10.1-seed-status-R.log" 2>&1; echo "code=$?" >> "$J/10.1-seed-status-R.log"
grep -E 'projection|^trunk' "$J/10.1-seed-status-R.log"
W="$R"/original-tree.code-workspace
for k in '"request"' '"svdFile"' '"type": "lldb"' 'tests des greffons' 'tiers'; do echo "$k $(grep -c "$k" "$W")"; done
diff <(sed "s#$R36#<R>#g" "$J/5.1-R36.code-workspace") <(sed "s#$R#<R>#g" "$W") > "$J/10.1-espace.diff"; echo "diff=$?"; head -40 "$J/10.1-espace.diff"
```
Attendu :
- `check`, `generate`, `seed status` code 0 ;
- `seed status` : `stm32f4xx-hal-driver projection v1.8.5 … (projeté par stm32f4xx, 200 fichier(s))`,
  `cmsis-device-f4 projection 3c77349… (projeté par stm32f4xx, 6 fichier(s))`,
  `trunk : aucun fichier régulier, aucun lien cassé` ;
- espace : 23 `"request"`, 10 `"svdFile"`, 7 `"type": "lldb"`, 4 tâches « tests des greffons »,
  0 `tiers` ;
- espace **identique** à celui de `$R36` au chemin du rootstock près (`diff=0`).

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
Attendu : codes 0 ; mêmes 2 clés projetées qu'au §10.1 ; espace identique à l'avant (`diff=0`).

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

Retenu au PA-73 : contrôle des 2 miroirs F4 contre leur amont, sans envoi. `$R` porte les
déclarations de miroir (`scion/.scion/.scion.mirrors` de `family-stm32f4xx`).

```bash
cd "$R"
scion mirror-sync --dry-run -v > "$J/11-mirror-sync.log" 2>&1; echo "code=$?" >> "$J/11-mirror-sync.log"
grep -E 'référence\(s\) à envoyer|signalement|à envoyer' "$J/11-mirror-sync.log"; tail -1 "$J/11-mirror-sync.log"
ls -d depots/.mirrors/*/*/* 2>&1
python3 -I "$T/$X/controler-trunk.py" "$R" "$T/$A/trunk-liens.txt" "$J/11-controle-R" | tail -1
```
Attendu (essai au Mac le 2026-11-09, `essais/env-41-vierge`) :
- code 0 ;
- `mirror-stm32f4xx-hal-driver : 0 référence(s) à envoyer, 0 signalement(s)` et de même pour
  `mirror-cmsis_device_f4` ;
- 2 dépôts de travail sous `depots/.mirrors/github.com/lepton-distribution/` ;
- trunk toujours `CONFORME`.

Une référence « à envoyer » (l'amont a avancé depuis le 2026-11-06) est relevée, sans arrêt : elle
ne sera pas envoyée. Un signalement (tag déplacé, branche réécrite ou supprimée) est un écart à
exposer. Jamais sans `--dry-run`.

## 12. Banc sur carte NUCLEO-F429ZI (C7)

Retenu au PA-73 : forme de R36-1 (`consignes/env-36-debian.md` §10), commandes en clair.
`rapports/env-35-hal-f4/banc-carte.sh` appelle `caffeinate` (macOS seul) : ne pas le lancer sur la
VM. Référence Debian (R36-1, `rapports/env-36-debian.md`) : 20/20 pour les 3 images, fumée
`cortexM4-stm32f4`, ping 3/3, LIST 13 entrées, RETR 57 octets identique, `ECONNRESET=15`. Les
images ont changé depuis (`.text` +32 / +48, ENV-42) ; les résultats du banc doivent rester les
mêmes.

### 12.1 Sonde, port série, droits, réseau

`AVANCEMENT` : l'**utilisateur** rattache la NUCLEO-F429ZI à la VM (VMware Fusion, menu des
périphériques USB ; le Mac ne la voit plus). **Aucune autre sonde ST** ne doit être rattachée à la
VM : le BSP `nucleo-f429zi` ne choisit pas sa sonde par numéro (O-1 d'ENV-42), OpenOCD prend la
première. Puis la session, en lecture seule :
```bash
id -nG; ls -l /dev/ttyACM* 2>&1; ls /dev/serial/by-id/ 2>&1
lsusb 2>&1 | grep -i -E 'st-?link|0483:' ; ls /etc/udev/rules.d/ /usr/lib/udev/rules.d/ 2>/dev/null | grep -i openocd
CFG="$R"/trunk/sys/root/src/kernel/dev/bsp/nucleo-f429zi/debug/openocd-nucleo-f439zi.cfg
openocd -f "$CFG" -c "init; targets; shutdown" > "$J/12.1-openocd-targets.log" 2>&1; echo "code=$?" >> "$J/12.1-openocd-targets.log"
cat "$J/12.1-openocd-targets.log"
ip -4 -o addr show | awk '{print $2, $4}'
ip route get 192.168.2.5
ping -c 3 -W 2 192.168.2.5 > "$J/12.1-ping-carte.log" 2>&1; echo "code=$?" >> "$J/12.1-ping-carte.log"
```
Attendu (R36-1) :
- **une seule** sonde ST, n° 0672FF495252717267243842 → `/dev/ttyACM0` ;
- OpenOCD voit `stm32f4x.cpu`, code 0 sans sudo ;
- port lisible et inscriptible par l'utilisateur (R36-1 : `root:plugdev` + ACL `uaccess`) ;
- une interface de la VM sur 192.168.2.0/24 (R36-1 : `ens37` 192.168.2.20/16) ;
- le ping de la carte peut échouer si l'image en flash ne répond pas (pas un arrêt).

Deux sondes ST visibles : arrêt, `AVANCEMENT` pour que l'utilisateur détache l'autre.

Si un droit manque (OpenOCD : `LIBUSB_ERROR_ACCESS` ; port : `Permission denied`) :
`AVANCEMENT` avec la commande exacte pour l'**utilisateur**, selon le cas :
```bash
sudo usermod -aG dialout,plugdev "$USER"          # puis fermer et rouvrir la session de la VM
sudo cp /usr/lib/udev/rules.d/60-openocd.rules /etc/udev/rules.d/ 2>/dev/null; sudo udevadm control --reload-rules && sudo udevadm trigger
```
La seconde commande ne sert que si aucune règle `60-openocd.rules` n'est active. La session
revérifie, consigne la commande lancée et son effet. Si c'est toujours bloqué : `QUESTION`, sans
contournement (ni `sudo openocd`, ni `chmod` du périphérique).

Puis `AVANCEMENT` : port relevé (`PORT`) et adresse IPv4 de la VM sur 192.168.2.0/24 (`HOSTIP`).
**L'utilisateur confirme l'adresse** avant tout flash. Aucune interface sur 192.168.2.0/24 :
arrêt et `QUESTION` (pas de modification réseau par la session).

### 12.2 Banc des 3 images

Après confirmation, dans cet ordre :
```bash
PORT=/dev/ttyACM<n>; HOSTIP=<adresse confirmée>
export PYTHONDONTWRITEBYTECODE=1
source "$R"/depots/lepton/original/master/scripts/lepton-env.sh > /dev/null
cd "$T"
for P in nucleo-f429zi-embos nucleo-f429zi-freertos nucleo-f439zi-embos; do
  D=$T/$O/env-43-debian/$P; B=$R/build/$P
  { cmake -S "$R/trunk" -B "$B" --preset "$P" -DLEPTON_BOARD_SERIAL_PORT="$PORT" -DLEPTON_NET_TEST_HOST_IP="$HOSTIP" && cmake --build "$B"; } > "$D/carte-config.log" 2>&1; echo "code=$?" >> "$D/carte-config.log"
  Y=$(mktemp -d); scripts/oracle/capturer-oracle.sh "$B/lepton.elf" "$Y" > /dev/null
  python3 scripts/oracle/comparer-oracle.py "$D" "$Y" > "$D/carte-oracle.txt" 2>&1; rc=$?; echo "$P oracle=$rc"; rm -rf "$Y"
  [ "$rc" -eq 0 ] || { echo "ARRÊT : $P différent de l'oracle"; break; }
  (cd "$R/trunk" && ctest --preset "$P" -L board --output-on-failure) > "$D/carte.log" 2>&1; echo "$P ctest=$?"
  cp "$B/Testing/Temporary/LastTest.log" "$D/carte-detail.log" 2>/dev/null
  cp "$B/smoke_lsh_board.log" "$D/fumee-carte.log" 2>/dev/null
  cp "$B/board_net.log" "$D/reseau-carte.log" 2>/dev/null
  grep -E 'tests passed|tests failed' "$D/carte.log"
done
```
Un `oracle=` non nul veut dire que l'image reconfigurée diffère de celle du §8. Dans ce cas :
arrêt avant `ctest` pour ce preset, `AVANCEMENT` avec l'extrait de `carte-oracle.txt`. Puis :
```bash
for P in nucleo-f429zi-embos nucleo-f429zi-freertos nucleo-f439zi-embos; do
  D=$T/$O/env-43-debian/$P
  echo "== $P"; grep -E 'Total Tests|tests passed' "$D/carte.log"
  grep -a -o 'cortexM4-stm32f4' "$D/fumee-carte.log" | head -1
  grep -a -i -E 'ping|LIST|RETR|ECONNRESET' "$D/carte-detail.log" | head -12
done
find "$R/trunk" -type f ! -name .scion.grafted.list | wc -l; find "$R/trunk" -name __pycache__ | wc -l
```
La synthèse de `board_net` est dans `carte-detail.log` (`LastTest.log`), pas dans
`reseau-carte.log` (défaut de la consigne de R36-1).

Attendu, pour chacune des 3 images :
- `oracle=0` ; `ctest=0`, **20/20** (`board.smoke_lsh`, banc KAL sur carte, `board.net`) ;
- fumée `cortexM4-stm32f4` ;
- réseau : ping 3/3, LIST 13 entrées, RETR 57 octets identique à la référence, `ECONNRESET=15` ;
- trunk sans fichier régulier ni `__pycache__`.

Un test en échec : relever `carte-detail.log` (extrait), relancer ce test une fois seul
(`ctest --preset <P> -R <test>`) et consigner les deux résultats ; pas de correction. La carte
garde l'image `nucleo-f439zi-embos` de la VM. Après le banc, l'utilisateur peut rattacher de
nouveau la carte au Mac (à consigner).

## 13. Nettoyage de la VM (C8)

Accordé au PA-73. Après le §10.1 (l'espace de `$R36` est copié au §5.1), relevé par la
session :
```bash
du -sh "$R36" ~/env-36-journaux
```
Puis `AVANCEMENT` : l'**utilisateur** lance :
```bash
rm -rf ~/lepton-tools-dev/essais/env-36-debian ~/env-36-journaux
```
La session vérifie `ls -d ~/lepton-tools-dev/essais/env-36-debian ~/env-36-journaux 2>&1` (absents).
Conservés : `$U` (`essais/env-28-debian`, regreffé au §7.1), `$R` (`essais/env-43-debian`), `$P`,
`$J`.

## 14. Critères et rapport

| Critère | Attendu |
| --- | --- |
| C1 Versions | `git ls-remote` conforme au §1 ; scion 0.6.1.0 par `install-debian.sh` (défaut `SCION_REF`) ; lepton `pipx` code 0, `lepton 0.1.0`, scion 0.6.1.0 accepté ; extension 0.5.2, seconde exécution d'`install-vscodium.sh` `changements 0` ; chaîne APT relevée |
| C2 `graft-update` et rootstock | §7.1 : `$U` code 0, 0 conflit ; noyau, BSP an386, familles F4 et WL avancés ; 2 clones tiers créés depuis les miroirs aux commits épinglés ; ajouts (4) et retraits (0) = attendu ; `controler-trunk.py` `CONFORME` (3982 liens = attendu, casse et cibles comprises, 0 cassé, 0 régulier) ; 16 entrées ; §7.2 : rootstock neuf, 16 entrées, `CONFORME`, liste identique à `$U` |
| C3 Constructions | host ctest 7/7, mklepton = `env-36-debian` = `env-42-apres` ; 16 presets construits ; QEMU fumée et banc 20/20, 16/16, 19/19 ; `comparer_R36-1` : 6 presets 0, 10 presets M4 1 avec écarts normalisés = Mac, `.text` seule section chargée changée ; `f429→f439` hors `.debug_*` 0 |
| C4 Contenu projeté et compilation à blanc | 206 projetés = HEAD des clones épinglés, 0 écart de casse (§7) ; résumé de la compilation à blanc = R36-1 (`cmsis5` 0 échec, `v330` 1 échec) ; trunk sans fichier régulier |
| C5 Fichiers générés | `$R` : `check`, `generate`, `seed status` 0, 2 clés projetées, espace = `$R36` au chemin près ; `$U` : codes 0, espace = avant ; `$P` : générés, graine et `check` identiques |
| C6 Miroir | `mirror-sync --dry-run` dans `$R` : code 0, 2 miroirs, 0 à envoyer (ou références « à envoyer » relevées), 0 signalement ; rien envoyé ; trunk `CONFORME` |
| C7 Carte NUCLEO-F429ZI | une seule sonde vue de la VM, droits sans sudo ; IP de la VM confirmée par l'utilisateur ; 3 `lepton.elf` reconfigurés = oracle `env-43-debian` (code 0) ; `ctest -L board` 20/20 pour chacun ; fumée `cortexM4-stm32f4` ; réseau ping 3/3, LIST 13 entrées, RETR 57 octets identique, `ECONNRESET=15` |
| C8 Nettoyage | `essais/env-36-debian` et `~/env-36-journaux` supprimés par l'utilisateur (taille relevée), absents |

Rapport `doc/devenv/rapports/env-43-debian.md` sur `devenv/env-43-debian`. Il contient :
- l'hôte et les versions (§5, §6) ;
- la table des critères ;
- la table des presets : construction, fumée, banc KAL, symboles R43-1 / R36-1 / Mac
  `env-42-apres`, `comparer_R36-1`, `comparer_Mac` ;
- les deltas de `.text` des 10 presets M4 (Debian contre Mac) ;
- les contrôles du trunk (§7, sortie de `controler-trunk.py`) ;
- la commande de miroir (§11) ; les cartes (§12) ;
- les écarts et constats ;
- le journal des messages §2bis (ID, date, résumé) ;
- ce qui n'a pas été fait.

Commit du rapport et de `oracles/env-43-debian/` (`compilation-a-blanc/` et, le cas échéant,
journaux de carte compris), puis `QUESTION` à l'utilisateur pour le push (PA-P), puis `FIN-*`.
