# Consigne — session Claude Code sur la VM Debian — ENV-33 (validation Debian groupée)

Fichier autonome : avec `ORCHESTRATION.md` §2bis, il suffit à conduire la session VM. Rédigé le
2026-11-03 par la session Mac `validation-debian-env-33` (tâche 1 d'ENV-33), repris de
`consignes/env-28-debian.md`. Son texte est envoyé tel quel dans l'ordre `R33-1`.

## 1. Objet

Valider sur Debian x86_64 l'état publié après ENV-29 à ENV-32 :
- scion 0.5.4.0 (ENV-29) par le défaut `SCION_REF` d'`install-debian.sh`, et lepton réinstallé ;
- `scion graft-update` d'un rootstock existant avec 0.5.4.0 : cas nominal, puis refus d'un clone
  hors de sa version déclarée (cas E-1 d'ENV-28) sur une copie, trunk intact ; rootstock neuf
  depuis la graine publiée ;
- constructions host et 16 presets, dont FreeRTOS au TCB étendu (ENV-31) ;
- tâche de l'éditeur « tests des greffons » (ENV-30) ;
- test radio `nucleo-wl55jc1.radio` déclaré par le BSP (ENV-32), découverte seule ;
- graine de projet existante après réinstallation.

Références publiées (toutes poussées, aucune fusion différée) :

| Dépôt (`https://github.com/lepton-distribution/…`) | Référence | Commit | En R28-1 |
| --- | --- | --- | --- |
| `lepton-tools` | `devenv/env-33` (cette consigne ; code Python identique à `main` 60dd6e5) | tête après `fetch` | b8ff911 |
| `seed.scions` | tag `0.5.4.0` | 99aa973 | tag `0.5.3.0` ad292ee |
| `lepton-seed.scions` | `original-tree` | 15740f9 | 15740f9 |
| `lepton-original-tree.scions` (noyau) | `master` | **b3a5415** | 0c0cc4f |
| `lepton-famille-qemu-mps2` | `master` | 3954357 | = |
| `lepton-bsp-qemu-mps2-an386` | `master` | 09f4943 | = |
| `lepton-bsp-qemu-mps2-an500` | `master` | e98a482 | = |
| `lepton-famille-stm32f4xx` | `master` | 8364493 | = |
| `lepton-bsp-nucleo-f429zi` | `master` | 2b2dfdd | = |
| `lepton-bsp-nucleo-f439zi` | `master` | bdbfa06 | = |
| `lepton-famille-stm32wlxx` | `master` | dbc58d7 | = |
| `lepton-bsp-nucleo-wl55jc1` | `master` | **ef51ec1** | c9183de |
| `lepton-famille-stm32f7xx` | `master` | d2d9aa9 | = |
| `lepton-bsp-stm32f746g-disco` | `master` | 6266908 | = |
| `lepton-famille-samd21` | `master` | a262e81 | = |
| `lepton-bsp-samd21-xplained-pro` | `master` | f3cffa2 | = |

Branches `devenv/env-14` publiées (cas E-1, §7.2) : `lepton-original-tree.scions` e5a5689,
`lepton-famille-stm32f4xx` af964c6.

Référence Mac : oracle `doc/devenv/rapports/oracles/env-32-apres/` (host + 16 presets ; binaires
= `env-31-apres`) ; écarts Mac `env-27-apres` → `env-32-apres` : `rapports/env-33-mac.md` §1.
Trunk de `~/lepton` au Mac, mêmes commits : 14 entrées greffées, 3957 liens, 0 cassé.
Référence Debian : `rapports/env-28-debian.md` et `oracles/env-28-debian/` (dernier oracle Debian
complet).

La session VM ne développe pas : elle exécute, constate et rapporte. Pas de carte sur la VM
(PA-53) : les presets de carte sont construits et configurés, jamais flashés.

## 2. Ce que la session VM peut faire, et ne fait pas

| Autorisé | Interdit |
| --- | --- |
| `git fetch` / `switch` de `~/lepton-tools-dev/lepton-tools` (`devenv/env-33`) | Modifier `DEVENV-STATUS.md`, `ORCHESTRATION.md`, `SPECIFICATION.md`, `handoff/*.md`, les consignes |
| `git fetch` puis `switch master` + `merge --ff-only origin/master` du clone noyau `~/lepton-tools-dev/lepton-noyau` | Toute autre écriture dans ce clone |
| Lire les journaux des commandes lancées **par l'utilisateur** : `pipx install`, scripts d'installation (sudo), `scion graft-update`, suppressions (§6.2, §7.1, §7.2, §11) | Lancer soi-même `sudo`, `pipx install`, `scion graft-update`, `rm -rf` |
| Créer la copie `$C` (§7.2) par `cp -RP` ; y faire `git switch` des clones `original` et `family-stm32f4xx` | Toute autre écriture dans les clones de `$U` et `$C` ; tout `seed-update` ; toucher aux autres rootstocks hors §7, §9 |
| Créer `~/lepton-tools-dev/essais/env-33-debian` (rootstock neuf) et y tout faire, `build/` compris | Écrire un fichier régulier dans un `trunk/` ; corriger quoi que ce soit (consigner l'écart pour la session Mac) |
| Dans `~/lepton-tools-dev/essais/env-11/qemu` : `lepton check`, `lepton generate`, `git status` de la graine `env11` | Regreffer `env-11/qemu`, commiter dans sa graine |
| `cmake` de configuration des presets WL55 dans `$J/ctest-N-build` (§10) | Flasher une carte, lancer un test `board` |
| Créer `devenv/env-33-debian` (depuis `devenv/env-33`) ; y écrire `doc/devenv/rapports/env-33-debian.md` et `doc/devenv/rapports/oracles/env-33-debian/` | Commiter sur une autre branche |
| `git push origin devenv/env-33-debian` **après accord explicite de l'utilisateur** (PA-P) | Pousser toute autre branche |

Règles des consignes VM (ORCHESTRATION §2bis) :
- **Commandes confiées à l'utilisateur** : `pipx install`, scripts d'installation, `scion
  graft-update` (refusé à la session en R28-1, « Untrusted Code Integration ») et `rm -rf` sont
  lancés par l'utilisateur dès le départ (commandes exactes ci-dessous) ; la session annonce
  l'attente par un `AVANCEMENT`, puis vérifie l'effet et le consigne. `scion rootstock-install`,
  `seed-add`, `graft` (§7.3) et `rejouer-oracle.sh` (§8) ont été acceptés en R28-1 : la session
  les lance ; si le classifieur de permissions les refuse, elle ne contourne pas, envoie un
  `AVANCEMENT` avec la commande exacte, et l'utilisateur la lance.
- **Régénérer avant de relever** : tout relevé « avant » d'un fichier généré suit immédiatement
  la commande qui le produit (§6.1).
- **Branche des clones d'un rootstock existant** (PA-45) : la branche courante de chaque clone de
  `$U` est relevée au §5 et consignée. Tant que scion 0.5.3.0 est installé, un clone hors de sa
  version déclarée est un arrêt ; aucun `graft-update` n'est lancé avant que `scion version`
  donne 0.5.4.0 (§7.1).

Tout écart au plan, toute erreur non prévue : s'arrêter, exposer (`AVANCEMENT` ou `QUESTION`),
attendre.

## 3. Communication (ORCHESTRATION §2bis)

- Session principale : `validation-debian-env-33` (session Mac) ; répondre à l'adresse `from`
  du message d'ordre.
- ID : `R33-1`, repris tel quel (`[ACCUSÉ R33-1] ENV-33 — …`, `[AVANCEMENT R33-1] …`,
  `[QUESTION R33-1] …`, `[FIN-SUCCÈS R33-1] …` ou `[FIN-ÉCHEC R33-1] …`).
- `ACCUSÉ` avant toute commande autre que les lectures du §5 : ordre reformulé en une phrase, tête
  réelle de `devenv/env-33` après `fetch`, résultats de `git ls-remote` du §5, branches et têtes
  des clones de `$U`, étapes prévues (§6 à §11), écarts déjà visibles.
- `AVANCEMENT` : quand l'utilisateur doit agir (§6.2, §7.1, §7.2, §11), après §6, §7, §8, §9,
  §10, et à chaque arrêt.
- `FIN-SUCCÈS` / `FIN-ÉCHEC` : résultat par critère du §12, commits et branche (poussée ou non),
  chemin du rapport, versions relevées, écarts, ce qui n'a pas été fait.

## 4. Journaux et variables

```bash
mkdir -p ~/env-33-journaux
J=~/env-33-journaux
T=~/lepton-tools-dev/lepton-tools
K=~/lepton-tools-dev/lepton-noyau
R=~/lepton-tools-dev/essais/env-33-debian
U=~/lepton-tools-dev/essais/env-28-debian
C=~/lepton-tools-dev/essais/env-33-copie-e1
P=~/lepton-tools-dev/essais/env-11/qemu
G=https://github.com/lepton-distribution
O=doc/devenv/rapports/oracles
```
Une commande par journal `$J/<étape>.log`, code de retour en dernière ligne (`code=<n>`).

## 5. Vérifications préalables (lecture seule)

```bash
uname -sm; cat /etc/debian_version; id -un; git --version
scion version | tail -1; lepton --version
arm-none-eabi-gcc --version | head -1; cmake --version | head -1; ninja --version
qemu-system-arm --version | head -1; python3 --version
echo "LEPTON_EMBOS_ROOT=${LEPTON_EMBOS_ROOT:-absente}"; ls -d ~/lepton/third_party/embos/cortexm-gcc/5.20.0.0 2>&1
df -h ~ /tmp | tail -2
for d in "$R" "$C"; do test -e "$d" && echo "ARRÊT : $d existe déjà"; done
git -C "$T" status --short | head -5; git -C "$K" status --short | head -5; git -C "$K" branch --show-current
git -C "$T" fetch origin && git -C "$T" switch devenv/env-33 && git -C "$T" merge --ff-only origin/devenv/env-33 && git -C "$T" log --oneline -1
echo "scion tag $(git ls-remote $G/seed.scions.git 'refs/tags/0.5.4.0^{}' | cut -c1-7)"
echo "graine $(git ls-remote $G/lepton-seed.scions.git original-tree | cut -c1-7)"
for r in lepton-original-tree.scions lepton-famille-qemu-mps2 lepton-bsp-qemu-mps2-an386 \
         lepton-bsp-qemu-mps2-an500 lepton-famille-stm32f4xx lepton-bsp-nucleo-f429zi \
         lepton-bsp-nucleo-f439zi lepton-famille-stm32wlxx lepton-bsp-nucleo-wl55jc1 \
         lepton-famille-stm32f7xx lepton-bsp-stm32f746g-disco lepton-famille-samd21 \
         lepton-bsp-samd21-xplained-pro; do
  echo "$r $(git ls-remote $G/$r.git refs/heads/master | cut -c1-7)"
done
for r in lepton-original-tree.scions lepton-famille-stm32f4xx; do
  echo "$r devenv/env-14 $(git ls-remote $G/$r.git refs/heads/devenv/env-14 | cut -c1-7)"
done
# Rootstock existant $U (P-1 / PA-45)
git -C "$U"/depots/lepton-seed.scions/original-tree log --oneline -1
git -C "$U"/depots/lepton-seed.scions/original-tree status --short | head -5
grep -v '^#' "$U"/trunk/.scion.grafted.list | grep -c .
for d in "$U"/depots/lepton/*/master; do
  echo "$(basename $(dirname $d)) $(git -C $d branch --show-current) $(git -C $d rev-parse --short HEAD) $(git -C $d rev-parse --abbrev-ref '@{u}' 2>&1) modifs=$(git -C $d status --short | wc -l)"
done | tee "$J/5-clones-U.txt"
echo "liens $(find "$U"/trunk -type l | wc -l) cassés $(find -L "$U"/trunk -type l | wc -l) réguliers $(find "$U"/trunk -type f ! -name .scion.grafted.list | wc -l)"
ls -A "$U"
# Graine de projet $P (C6)
ls -d "$P"/depots/lepton-seed/env11
grep -c '"tests"' "$P"/trunk/sys/root/src/kernel/dev/bsp/qemu-mps2-an386/lepton-greffon.json
git -C "$P"/depots/lepton/bsp-qemu-mps2-an386/master log --oneline -1 2>&1
ls -d ~/lepton-tools-dev/essais/env-14-debian ~/env-28-journaux 2>&1
```
Attendu : commits du tableau du §1 et branches `devenv/env-14` aux commits indiqués ; `$U` :
graine à 15740f9, propre ; 14 entrées greffées ; **13 clones sur `master`**, amont
`origin/master`, aucune modification, aux commits de la colonne « En R28-1 » (noyau 0c0cc4f,
`bsp-nucleo-wl55jc1` c9183de, les autres égaux) ; 3956 liens, 0 cassé, 0 fichier régulier.

Arrêts : `$R` ou `$C` existe ; lepton-tools ou clone noyau non propre ; un commit publié diffère ;
graine de `$U` modifiée ; un clone de `$U` hors de `master`, sans amont ou modifié ; moins de
6 Go libres dans `~`. embOS absent : pas un arrêt ; les presets `*-embos*` seront en échec
attendu, à consigner. Le chemin réel de la graine de `$P` et la tête de son BSP an386 sont
consignés (ils fixent l'attendu du §9).

## 6. Installation (C1, C2)

### 6.1 Graine de projet : régénération puis relevé avant réinstallation (pour C6)

Avec le lepton actuel de la VM (`devenv/env-28` b8ff911), **régénérer d'abord**, puis relever :
```bash
lepton generate -C "$P" > "$J/6.1-generate-P-avant.log" 2>&1; echo "code=$?" >> "$J/6.1-generate-P-avant.log"
lepton check -C "$P" > "$J/6.1-check-P-avant.log" 2>&1; echo "code=$?" >> "$J/6.1-check-P-avant.log"
git -C "$P"/depots/lepton-seed/env11 status --short > "$J/6.1-graine-P-avant.txt"
sha256sum "$P"/depots/lepton-seed/env11/project/scion/CMakeUserPresets.json "$P"/*.code-workspace > "$J/6.1-generes-P-avant.sha256"
mkdir -p "$J/6.1-P-avant" && cp "$P"/*.code-workspace "$P"/depots/lepton-seed/env11/project/scion/CMakeUserPresets.json "$J/6.1-P-avant/"
```
Si `depots/lepton-seed/env11` n'est pas la graine de `$P` : consigner le chemin réel et l'utiliser.

### 6.2 Commandes de l'utilisateur (C1, C2)

D'abord, par la session :
```bash
git -C "$K" fetch origin && git -C "$K" switch master && git -C "$K" merge --ff-only origin/master && git -C "$K" log --oneline -1
grep -n '^SCION_REF=' "$K/scripts/install-debian.sh"
```
Attendu : clone noyau à b3a5415 ; `SCION_REF="${SCION_REF:-0.5.4.0}"`.

Puis `AVANCEMENT` : l'**utilisateur** lance, dans un terminal de la VM (sudo avec mot de passe),
**sans** `SCION_REF` dans l'environnement (défaut du noyau), dans cet ordre (scion d'abord : lepton
exige scion ≥ 0.5.4.0) :

```bash
J=~/env-33-journaux; K=~/lepton-tools-dev/lepton-noyau; T=~/lepton-tools-dev/lepton-tools
unset SCION_REF SCION_SPEC
bash "$K/scripts/install-debian.sh" --with-debug-tools 2>&1 | tee "$J/6.2-install-debian.log"; echo "code=${PIPESTATUS[0]}" | tee -a "$J/6.2-install-debian.log"
pipx install --force "$T" 2>&1 | tee "$J/6.2-lepton.log"; echo "code=${PIPESTATUS[0]}" | tee -a "$J/6.2-lepton.log"
bash "$T/scripts/install-vscodium.sh" --lepton-clone "$K" 2>&1 | tee "$J/6.2-install-vscodium-1.log"; echo "code=${PIPESTATUS[0]}" | tee -a "$J/6.2-install-vscodium-1.log"
bash "$T/scripts/install-vscodium.sh" --lepton-clone "$K" 2>&1 | tee "$J/6.2-install-vscodium-2.log"; echo "code=${PIPESTATUS[0]}" | tee -a "$J/6.2-install-vscodium-2.log"
```
La session lit ensuite les journaux. Attendu : quatre codes 0 ; `install-debian.sh` : scion
installé depuis `$G/seed.scions.git@0.5.4.0` (0.5.3.0 auparavant) ; seconde exécution
d'`install-vscodium.sh` : **`changements 0`**. Puis :
```bash
scion version | tail -1; lepton --version; codium --version | head -1
pipx list --short | grep -E '^(scion|lepton) '
dpkg-query -W -f '${Version}\n' codium; codium --list-extensions --show-versions | LC_ALL=C sort > "$J/6.2-extensions.txt"
grep -E -i 'lldb|lepton|rtos-views' "$J/6.2-extensions.txt"
```
Attendu : `scion version: 0.5.4.0` ; `lepton 0.1.0`, `scion 0.5.4.0 (requis ≥ 0.5.4.0)` ;
`vadimcn.vscode-lldb@1.12.3`, `lepton-distribution.lepton@0.5.1`, `mcu-debug.rtos-views@0.0.16`.

## 7. `graft-update` d'un rootstock existant, refus E-1, rootstock neuf (C3)

Préalable : `scion version | tail -1` donne 0.5.4.0. Sinon : arrêt, aucun `graft-update`.

### 7.1 Cas nominal sur `$U`

Par la session :
```bash
cd "$U"
find trunk -type l | LC_ALL=C sort > "$J/7.1-liens-avant.txt"; wc -l < "$J/7.1-liens-avant.txt"
sha256sum trunk/.scion.grafted.list > "$J/7.1-grafted-avant.sha256"
```
Puis `AVANCEMENT` : l'**utilisateur** lance :
```bash
J=~/env-33-journaux; cd ~/lepton-tools-dev/essais/env-28-debian
scion graft-update -v > "$J/7.1-graft-update.log" 2>&1; echo "code=$?" >> "$J/7.1-graft-update.log"
```
Puis la session :
```bash
cd "$U"
tail -15 "$J/7.1-graft-update.log"; grep -i -E 'graine|conflit|refus' "$J/7.1-graft-update.log"
git -C depots/lepton-seed.scions/original-tree log --oneline -1
grep -v '^#' trunk/.scion.grafted.list | grep -c .
for d in depots/lepton/*/master; do echo "$(basename $(dirname $d)) $(git -C $d branch --show-current) $(git -C $d rev-parse --short HEAD) modifs=$(git -C $d status --short | wc -l)"; done | tee "$J/7.1-clones-apres.txt"
find trunk -type l | LC_ALL=C sort > "$J/7.1-liens-apres.txt"
diff "$J/7.1-liens-avant.txt" "$J/7.1-liens-apres.txt" > "$J/7.1-liens.diff"; cat "$J/7.1-liens.diff"
echo "liens $(wc -l < $J/7.1-liens-apres.txt) cassés $(find -L trunk -type l | wc -l) réguliers $(find trunk -type f ! -name .scion.grafted.list | wc -l)"
```
Attendu : code 0, 0 conflit ; graine inchangée (15740f9) ; 14 entrées ; 13 clones sur `master`,
propres, aux commits du §1 (noyau 0c0cc4f → b3a5415, `bsp-nucleo-wl55jc1` c9183de → ef51ec1,
avance rapide, aucun `git pull`) ; 3957 liens (3956 avant), 0 cassé, 0 fichier régulier ;
`7.1-liens.diff` limité à :
```
< trunk/tests/board_radio.py
> trunk/sys/root/src/kernel/dev/bsp/nucleo-wl55jc1/tests/CMakeLists.txt
> trunk/sys/root/src/kernel/dev/bsp/nucleo-wl55jc1/tests/radio.py
```
(ordre des lignes selon `diff`). Toute autre ligne : écart à exposer.

### 7.2 Cas E-1 rejoué sur une copie `$C` (PA-53)

Par la session, après le §7.1 :
```bash
mkdir "$C" && cp -RP "$U"/depots "$U"/trunk "$U"/.scion.rootstock.signature "$C"/
test -e "$U"/.scion.trunk.tolerated && cp -P "$U"/.scion.trunk.tolerated "$C"/
cd "$C"
diff <(cd "$U/trunk" && find . -type l | LC_ALL=C sort) <(cd "$C/trunk" && find . -type l | LC_ALL=C sort) && echo "copie : liste identique à \$U"
echo "cassés $(find -L trunk -type l | wc -l)"
git -C depots/lepton/original/master switch devenv/env-14
git -C depots/lepton/family-stm32f4xx/master switch devenv/env-14
for d in depots/lepton/original/master depots/lepton/family-stm32f4xx/master; do echo "$d $(git -C $d branch --show-current) $(git -C $d rev-parse --short HEAD)"; done
find trunk -type l | LC_ALL=C sort > "$J/7.2-liens-avant.txt"; sha256sum trunk/.scion.grafted.list > "$J/7.2-grafted-avant.sha256"
```
Les liens du trunk sont relatifs (`../depots/…`) : la copie est autonome. Des liens cassés
peuvent apparaître le temps que les deux clones restent sur `devenv/env-14` (4 au Mac en
ENV-29) : les compter, ne rien corriger.

Puis `AVANCEMENT` : l'**utilisateur** lance :
```bash
J=~/env-33-journaux; cd ~/lepton-tools-dev/essais/env-33-copie-e1
scion graft-update -v > "$J/7.2-graft-update-e1.log" 2>&1; echo "code=$?" >> "$J/7.2-graft-update-e1.log"
```
Puis la session :
```bash
cd "$C"; cat "$J/7.2-graft-update-e1.log"
find trunk -type l | LC_ALL=C sort > "$J/7.2-liens-apres.txt"
diff "$J/7.2-liens-avant.txt" "$J/7.2-liens-apres.txt" && echo "trunk intact"
sha256sum -c "$J/7.2-grafted-avant.sha256"
for d in depots/lepton/original/master depots/lepton/family-stm32f4xx/master; do echo "$d $(git -C $d branch --show-current) $(git -C $d rev-parse --short HEAD) modifs=$(git -C $d status --short | wc -l)"; done
```
Attendu : code 1 ; message « 2 clone(s) à remettre à leur version déclarée avant la mise à jour
… (trunk et clones inchangés) », chaque clone nommé avec sa branche et la commande
`git -C … switch master` ; aucun dégreffage (pas de conflit listé) ; liste des liens et
`.scion.grafted.list` identiques avant et après ; clones restés sur `devenv/env-14` (e5a5689,
af964c6), propres. En R28-1 (scion 0.5.3.0), le même cas donnait 277 conflits et un trunk vidé.

Puis `AVANCEMENT` : l'**utilisateur** supprime la copie :
```bash
rm -rf ~/lepton-tools-dev/essais/env-33-copie-e1
```
La session vérifie `ls -d "$C" 2>&1` (absente) et que `$U` est inchangé (`diff` de la liste de
`$U` contre `$J/7.1-liens-apres.txt`).

### 7.3 Rootstock neuf depuis la graine publiée

```bash
mkdir "$R" && cd "$R"
scion rootstock-install > "$J/7.3-rootstock-install.log" 2>&1; echo "code=$?" >> "$J/7.3-rootstock-install.log"
scion seed-add --version original-tree $G/lepton-seed.scions.git > "$J/7.3-seed-add.log" 2>&1; echo "code=$?" >> "$J/7.3-seed-add.log"
scion graft > "$J/7.3-graft.log" 2>&1; echo "code=$?" >> "$J/7.3-graft.log"
grep -v '^#' trunk/.scion.grafted.list | grep -c .
for d in depots/lepton/*/master; do echo "$d $(git -C $d branch --show-current) $(git -C $d rev-parse --short HEAD)"; done
find trunk -type l -exec sh -c 'for l; do printf "%s\t%s\n" "$l" "$(readlink "$l")"; done' _ {} + | LC_ALL=C sort > "$J/7.3-trunk.tsv"
echo "liens $(find trunk -type l | wc -l) cassés $(find -L trunk -type l | wc -l) réguliers $(find trunk -type f ! -name .scion.grafted.list | wc -l)"
diff <(cd "$U/trunk" && find . -type l | LC_ALL=C sort) <(cd "$R/trunk" && find . -type l | LC_ALL=C sort) && echo "liste des liens identique à \$U"
```
Attendu : codes 0 ; 14 entrées ; chaque clone sur `master` au commit du §1 ; 3957 liens, 0 cassé,
0 fichier régulier ; liste des liens identique à celle de `$U` après §7.1. Un nombre différent
de 3957 : relever `comm` contre la liste des fichiers suivis des clones, l'exposer.

## 8. Reconstructions et comparaisons (C4)

Périmètre : host et les 16 presets croisés (QEMU : construction, fumée, banc KAL ; cartes :
construction et capture seulement).

```bash
cd "$T" && git switch -c devenv/env-33-debian devenv/env-33
scripts/oracle/rejouer-oracle.sh "$R" $O/env-33-debian \
  --qemu qemu-mps2-an386-embos --qemu qemu-mps2-an386-embos-soft \
  --qemu qemu-mps2-an386-freertos --qemu qemu-mps2-an386-freertos-soft \
  --qemu qemu-mps2-an500-embos --qemu qemu-mps2-an500-freertos \
  --carte nucleo-f429zi-embos --carte nucleo-f429zi-freertos \
  --carte nucleo-f439zi-embos --carte nucleo-f439zi-freertos \
  --carte nucleo-wl55jc1-embos --carte nucleo-wl55jc1-freertos \
  --carte samd21-xplained-pro-embos --carte samd21-xplained-pro-freertos \
  --carte stm32f746g-disco-embos --carte stm32f746g-disco-freertos > "$J/8-rejouer.log" 2>&1; echo "code=$?" >> "$J/8-rejouer.log"
tail -25 "$J/8-rejouer.log"
grep -h "tests passed" $O/env-33-debian/*/ctest.log $O/env-33-debian/*/banc-kal.log
grep -h "peripheriques" $O/env-33-debian/qemu-mps2-an386-*/banc-kal.log
find -L "$R/trunk" -type l | wc -l; find "$R/trunk" -type f ! -name .scion.grafted.list | wc -l
```
Attendu : code 0 ; host ctest 7/7 ; 16 presets construits ; fumée réussie ; banc QEMU **identique
à R28-1** (aucun test QEMU changé depuis) :

| Preset | R28-1 Debian | Mac `env-32-apres` | Attendu R33-1 |
| --- | --- | --- | --- |
| `qemu-mps2-an386-{embos,freertos}` | 20/20 | 19/19 | **20/20** |
| `qemu-mps2-an386-{embos,freertos}-soft` | 16/16 | 15/15 | **16/16** |
| `qemu-mps2-an500-{embos,freertos}` | 19/19 | 18/18 | **19/19** |

(`net.ping_ftpd` ne tourne que sous Linux.) `qemu-mps2-an386.peripheriques` **Passed** dans les
4 `banc-kal.log` an386. Trunk sans fichier régulier ni lien cassé.

### 8.1 Comparaisons

La non-régression Debian se lit **par rapport à R28-1** et aux écarts constatés au Mac entre
`env-27-apres` et `env-32-apres` (`rapports/env-33-mac.md` §1, ENV-31) :

```bash
cd "$T"
diff -q $O/env-32-apres/host/mklepton-empreintes.sha256 $O/env-33-debian/host/mklepton-empreintes.sha256 && echo "mklepton = Mac env-32-apres"
diff -q $O/env-28-debian/host/mklepton-empreintes.sha256 $O/env-33-debian/host/mklepton-empreintes.sha256 && echo "mklepton = R28-1"
for p in $(ls $O/env-33-debian | grep -v -e host -e ctest-N -e '\.log$'); do
  python3 scripts/oracle/comparer-oracle.py $O/env-28-debian/$p $O/env-33-debian/$p > "$J/8.1-cmp-R28-$p.txt" 2>&1; a=$?
  python3 scripts/oracle/comparer-oracle.py $O/env-32-apres/$p $O/env-33-debian/$p > "$J/8.1-cmp-Mac-$p.txt" 2>&1; b=$?
  echo "$p comparer_R28-1=$a comparer_Mac=$b symboles=$(wc -l < $O/env-33-debian/$p/symboles.txt)"
done
for s in embos freertos; do
  python3 scripts/oracle/comparer-oracle.py $O/env-33-debian/nucleo-f429zi-$s $O/env-33-debian/nucleo-f439zi-$s > /dev/null 2>&1; echo "f429→f439 $s=$?"
done
```

Attendu :
- mklepton : empreintes identiques à `env-32-apres` et à `env-28-debian` (50 lignes).
- `comparer_R28-1` des **8 presets embOS** : **0**.
- `comparer_R28-1` des **8 presets FreeRTOS** : **1**, et chaque fichier
  `8.1-cmp-R28-<preset>.txt` ne contient que ce qu'admet le critère du PA-49 (ENV-31), constaté au
  Mac sur les mêmes 8 presets :

| Élément | Admis (delta) | Mac `env-27-apres` → `env-32-apres` |
| --- | --- | --- |
| `xTaskCreateStatic` (T) | +4 | 0x1f8 → 0x1fc (samd21 : 0x1f0 → 0x1f4) |
| `xIdleTaskTCB.3`, `xTimerTaskTCB.1` (b) | 0x54 → 0x58 | idem, 8 presets |
| `.ccm_bss` | +8 | +8, 8 presets |
| `.text` | 0, ou +4 plus le bourrage d'alignement qui en résulte (aucune autre taille de symbole changée) | 0 ; `qemu-mps2-an386-freertos` +16 (bourrage de `__vfscanf` et `_close`) |
| sections `.debug_*`, empreintes `.bin`/`.elf`/`.hex` | libres | — |

  Rien d'autre : aucun symbole ajouté ou retiré, aucune autre taille changée ; `.data`, `.bss`,
  `.noinit` inchangés. Un `.text` différent de 0 sur un autre preset que celui du Mac est admis
  s'il ne vient que du bourrage (aucune autre taille de symbole changée) : à relever et
  signaler, sans arrêt. Toute autre ligne : écart à exposer (extrait du fichier), pas à corriger.
- `comparer_Mac` : informatif (chaînes différentes ; 1 attendu partout).
- `f429→f439` : 0.

## 9. Fichiers générés par lepton (C5, C6)

### 9.1 Rootstock neuf `$R` : tâche « tests des greffons » (C5)

```bash
lepton check -C "$R" > "$J/9.1-check-R.log" 2>&1; echo "code=$?" >> "$J/9.1-check-R.log"
lepton generate -C "$R" > "$J/9.1-generate-R.log" 2>&1; echo "code=$?" >> "$J/9.1-generate-R.log"
W="$R"/original-tree.code-workspace
for k in '"request"' '"svdFile"' '"type": "lldb"'; do echo "$k $(grep -c "$k" "$W")"; done
python3 - "$W" > "$J/9.1-taches-greffons.txt" <<'EOF'
import json, sys
w = json.loads(open(sys.argv[1]).read().split('\n', 1)[1])
for t in w['tasks']['tasks']:
    if t['label'].startswith('lepton : tests des greffons'):
        print(json.dumps(t, ensure_ascii=False, sort_keys=True))
EOF
cut -c1-200 "$J/9.1-taches-greffons.txt"; grep -c . "$J/9.1-taches-greffons.txt"
```
Attendu : `check` et `generate` code 0 ; 23 `"request"`, 10 `"svdFile"`, 7 `"type": "lldb"`
(inchangés depuis R28-1) ; **4 tâches** `lepton : tests des greffons <P>` pour
`qemu-mps2-an386-{embos,embos-soft,freertos,freertos-soft}`, aucune pour an500 ni pour les
10 presets de carte (PA-47 : configurations QEMU seules ; le champ `tests` du BSP WL55 n'en crée
pas). Forme de chaque tâche : `type` `process`, `command` = `ctest` de la VM (chemin absolu),
`args` `["--preset", "<P>", "-L", "greffon:", "--output-on-failure"]`, `options.cwd` = `$R/trunk`,
`options.env` `{"PYTHONDONTWRITEBYTECODE": "1"}`, `dependsOn` `["lepton : construire <P>"]`,
`group` `test`.

Exécution en ligne de commande de la tâche de `qemu-mps2-an386-embos`, avec sa commande, ses
arguments, son répertoire et son environnement (construction déjà faite au §8) :
```bash
python3 - "$W" > "$J/9.1-tache-an386.sh" <<'EOF'
import json, shlex, sys
w = json.loads(open(sys.argv[1]).read().split('\n', 1)[1])
t = [t for t in w['tasks']['tasks'] if t['label'] == 'lepton : tests des greffons qemu-mps2-an386-embos'][0]
print('cd ' + shlex.quote(t['options']['cwd']) + ' && env ' +
      ' '.join(shlex.quote(f'{k}={v}') for k, v in t['options'].get('env', {}).items()) + ' ' +
      shlex.quote(t['command']) + ' ' + ' '.join(shlex.quote(a) for a in t['args']))
EOF
cat "$J/9.1-tache-an386.sh"
bash "$J/9.1-tache-an386.sh" > "$J/9.1-tache-an386.log" 2>&1; echo "code=$?" >> "$J/9.1-tache-an386.log"
grep -E 'Test +#|tests passed|code=' "$J/9.1-tache-an386.log"
find "$R/trunk" -name __pycache__ | wc -l; find "$R/trunk" -type f ! -name .scion.grafted.list | wc -l
```
Attendu : code 0 ; 2 tests, `smoke.lsh` (fixture) et `qemu-mps2-an386.peripheriques`, réussis
(« 100% tests passed, 0 tests failed out of 2 ») ; aucun `__pycache__`, aucun fichier régulier
dans le trunk.

### 9.2 Graine de projet existante `$P` après réinstallation (C6)

```bash
lepton generate -C "$P" > "$J/9.2-generate-P-apres.log" 2>&1; echo "code=$?" >> "$J/9.2-generate-P-apres.log"
lepton check -C "$P" > "$J/9.2-check-P-apres.log" 2>&1; echo "code=$?" >> "$J/9.2-check-P-apres.log"
git -C "$P"/depots/lepton-seed/env11 status --short > "$J/9.2-graine-P-apres.txt"
sha256sum "$P"/depots/lepton-seed/env11/project/scion/CMakeUserPresets.json "$P"/*.code-workspace > "$J/9.2-generes-P-apres.sha256"
diff "$J/6.1-generes-P-avant.sha256" "$J/9.2-generes-P-apres.sha256"
diff "$J/6.1-graine-P-avant.txt" "$J/9.2-graine-P-apres.txt" && echo "graine P inchangée"
diff <(grep -v '^code=' "$J/6.1-check-P-avant.log") <(grep -v '^code=' "$J/9.2-check-P-apres.log") && echo "check P identique"
diff "$J/6.1-P-avant/CMakeUserPresets.json" "$P"/depots/lepton-seed/env11/project/scion/CMakeUserPresets.json && echo "presets P identiques"
diff "$J/6.1-P-avant/"*.code-workspace "$P"/*.code-workspace > "$J/9.2-espace-P.diff"; cat "$J/9.2-espace-P.diff"
```
Attendu : `generate` et `check` code 0 ; graine inchangée ; sortie de `check` et
`CMakeUserPresets.json` identiques ; espace de travail : **différence limitée aux tâches
d'ENV-30**, selon le BSP an386 de `$P` relevé au §5 :
- son manifeste déclare `"tests"` (BSP 09f4943 ou postérieur) : une tâche
  `lepton : tests des greffons <C>` ajoutée par configuration QEMU de la graine `env11` (au Mac :
  2, `env11-debug-qemu` et `env11-release-qemu`), placée après la tâche « banc KAL » de la même
  configuration ; aucune ligne retirée hors virgules de raccord ;
- il ne le déclare pas (BSP antérieur, `$P` non regreffé) : espace **identique**.
Toute autre différence : la relever telle quelle, l'exposer.

## 10. Test radio d'ENV-32 : découverte seule (C7)

Le script de relevé d'ENV-32 configure à neuf les deux presets WL55 hors de `$R/build`, en quatre
variantes (`banc` : ports et sondes du banc du Mac, simples chaînes ici ; `fictif` : ports et
sondes fictifs ; `seul` : port de la carte A seul ; `sans` : aucun port), et relève `ctest -N`,
`ctest -N -L greffon:` et les tests détaillés. Aucun test n'est lancé.
```bash
cd "$T"
bash $O/env-32-apres/ctest-N/relever-ctest-N.sh "$R" $O/env-33-debian/ctest-N "$J/ctest-N-build" > "$J/10-ctest-N.log" 2>&1; echo "code=$?" >> "$J/10-ctest-N.log"
cat "$J/10-ctest-N.log"
cp $O/env-32-apres/ctest-N/relever-ctest-N.sh $O/env-33-debian/ctest-N/
for f in $O/env-32-apres/ctest-N/*.ctest-N*.txt; do
  b=$(basename "$f"); diff -q "$f" $O/env-33-debian/ctest-N/"$b" > /dev/null && echo "$b identique" || echo "$b DIFFÈRE"
done
grep '^nucleo-wl55jc1.radio' $O/env-33-debian/ctest-N/nucleo-wl55jc1-*-fictif.tests.txt
grep -A1 '^nucleo-wl55jc1.radio' $O/env-33-debian/ctest-N/nucleo-wl55jc1-embos-fictif.tests.txt | tail -1 | grep -o -e 'sys/root/src/kernel/dev/bsp/nucleo-wl55jc1/tests/radio.py' -e '--tests-noyau [^ ]*'
ls "$R"/trunk/tests/board_radio.py 2>&1
find "$R/trunk" -name __pycache__ | wc -l
```
Attendu : code 0 ; `Total Tests` : `banc` 16, `fictif` 16, `seul` 15, `sans` 0, pour embOS et
FreeRTOS ; les 16 fichiers `*.ctest-N.txt` et `*.ctest-N-greffon.txt` **identiques** à ceux du
Mac (noms et rangs ; `nucleo-wl55jc1.radio` au rang 16 ; `-L greffon:` : `nucleo-wl55jc1.radio`
seul en `banc` et `fictif`, aucun en `seul` et `sans`) ; dans `*-fictif.tests.txt`, le test
`nucleo-wl55jc1.radio` porte l'étiquette `greffon:nucleo-wl55jc1`, et sa commande lance
`…/sys/root/src/kernel/dev/bsp/nucleo-wl55jc1/tests/radio.py` avec `--tests-noyau <$R>/trunk/tests`
(déclaré par le BSP) ; `trunk/tests/board_radio.py` absent ; aucun `__pycache__` dans le trunk.
Les fichiers `*.tests.txt` contiennent des chemins propres à l'hôte (Python, OpenOCD, trunk) :
comparaison au Mac informative seulement.

## 11. Nettoyage de la VM (C8)

Accordé au PA-53. Relevé par la session :
```bash
du -sh ~/lepton-tools-dev/essais/env-14-debian ~/env-28-journaux
```
Puis `AVANCEMENT` : l'**utilisateur** lance :
```bash
rm -rf ~/lepton-tools-dev/essais/env-14-debian ~/env-28-journaux
```
La session vérifie :
```bash
ls -d ~/lepton-tools-dev/essais/env-14-debian ~/env-28-journaux 2>&1
```
Conservés : `$U` (`essais/env-28-debian`, mis à jour au §7.1), `$R` (`essais/env-33-debian`),
`$P`, `$J`. La copie `$C` est supprimée au §7.2.

## 12. Critères et rapport

| Critère | Attendu |
| --- | --- |
| C1 scion et lepton | `git ls-remote` conforme au §1 ; scion 0.5.4.0 (par `install-debian.sh`, défaut `SCION_REF`) ; `pipx install --force` de lepton code 0 ; `lepton 0.1.0`, scion 0.5.4.0 accepté ; versions relevées |
| C2 Scripts d'installation | `install-debian.sh` du noyau (b3a5415) code 0 ; `install-vscodium.sh` code 0 deux fois, `changements 0` à la seconde |
| C3 `graft-update` et rootstock | §7.1 : `$U` code 0, 0 conflit, noyau et BSP WL55 avancés, 3957 liens, diff limité aux 3 lignes ; §7.2 : `$C` code 1, refus des 2 clones nommés, trunk et `.scion.grafted.list` intacts, clones non déplacés, copie supprimée ; §7.3 : rootstock neuf, 14 entrées, 3957 liens, 0 cassé, 0 régulier, liste identique à `$U` |
| C4 Constructions | host ctest 7/7, empreintes mklepton = `env-32-apres` = `env-28-debian` ; 16 presets construits ; QEMU fumée et banc 20/20, 16/16, 19/19 ; `comparer_R28-1` : embOS 0, FreeRTOS dans le critère du §8.1 ; `f429→f439` 0 |
| C5 Tâche « tests des greffons » | `check`, `generate` code 0 sur `$R` ; 4 tâches (an386), aucune pour an500 ni les cartes ; forme du §9.1 ; tâche de `qemu-mps2-an386-embos` exécutée : 2/2, code 0 ; trunk sans `__pycache__` |
| C6 Graine de projet `env11` | `check`, `generate` code 0 ; `check`, presets et graine identiques ; espace : tâches d'ENV-30 seules (ou identique, selon le BSP de `$P`) |
| C7 Test radio (découverte) | listes `ctest -N` 16/16/15/0 et `-L greffon:` identiques au Mac ; `nucleo-wl55jc1.radio` déclaré par le BSP (étiquette, script, `--tests-noyau`) ; `board_radio.py` absent du trunk |
| C8 Nettoyage | `env-14-debian` et `~/env-28-journaux` supprimés par l'utilisateur (taille relevée) ; copie `$C` supprimée |

Rapport `doc/devenv/rapports/env-33-debian.md` sur `devenv/env-33-debian`, contenant : hôte et
versions (§5, §6), table des critères, table des presets (construction, fumée, banc KAL, symboles
R33-1 / R28-1 / Mac `env-32-apres`, `comparer_R28-1`, `comparer_Mac`), nature des écarts
FreeRTOS (par preset), écarts et constats, journal des messages §2bis (ID, date, résumé), non
fait. Commit du rapport et de `oracles/env-33-debian/` (`ctest-N/` compris), puis `QUESTION` à
l'utilisateur pour le push (PA-P), puis `FIN-*`.
