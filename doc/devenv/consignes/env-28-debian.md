# Consigne — session Claude Code sur la VM Debian — ENV-28 (validation Debian groupée)

Fichier autonome : avec `ORCHESTRATION.md` §2bis, il suffit à conduire la session VM. Rédigé le
2026-11-02 par la session Mac `validate-env-22-27-debian` (tâche 1 d'ENV-28), repris de
`consignes/env-21-debian.md`. Son texte est envoyé tel quel dans l'ordre `R28-1`.

## 1. Objet

Valider sur Debian x86_64 l'état publié après ENV-22 à ENV-27 :
- scion 0.5.3.0 (ENV-23) par le défaut `SCION_REF` d'`install-debian.sh`, et lepton réinstallé ;
- mise à jour d'une graine en retard par `scion graft-update` (ENV-23), puis rootstock neuf depuis
  la graine publiée ;
- constructions host et 16 presets avec le cpufs automatique (ENV-24) ;
- lancement hôte de `mklepton` généré par `lepton generate` (DBG-5, ENV-25) et arrêt dans `main` ;
- champ `svd` des familles et fichiers SVD (DBG-4, ENV-26) ;
- tests fournis par un greffon : `qemu-mps2-an386.peripheriques` (TST-2, ENV-27) ;
- graine de projet existante après réinstallation.

Références publiées (toutes poussées, aucune fusion différée) :

| Dépôt (`https://github.com/lepton-distribution/…`) | Référence | Commit |
| --- | --- | --- |
| `lepton-tools` | `devenv/env-28` (cette consigne ; code Python identique à `main` d4351bc) | tête après `fetch` |
| `seed.scions` | tag `0.5.3.0` | ad292ee |
| `lepton-seed.scions` | `original-tree` | 15740f9 (inchangée depuis ENV-20) |
| `lepton-original-tree.scions` (noyau) | `master` | 0c0cc4f |
| `lepton-famille-qemu-mps2` | `master` | 3954357 |
| `lepton-bsp-qemu-mps2-an386` | `master` | 09f4943 |
| `lepton-bsp-qemu-mps2-an500` | `master` | e98a482 |
| `lepton-famille-stm32f4xx` | `master` | 8364493 |
| `lepton-bsp-nucleo-f429zi` | `master` | 2b2dfdd |
| `lepton-bsp-nucleo-f439zi` | `master` | bdbfa06 |
| `lepton-famille-stm32wlxx` | `master` | dbc58d7 |
| `lepton-bsp-nucleo-wl55jc1` | `master` | c9183de |
| `lepton-famille-stm32f7xx` | `master` | d2d9aa9 |
| `lepton-bsp-stm32f746g-disco` | `master` | 6266908 |
| `lepton-famille-samd21` | `master` | a262e81 |
| `lepton-bsp-samd21-xplained-pro` | `master` | f3cffa2 |

Référence Mac : oracle `doc/devenv/rapports/oracles/env-27-apres/` (host + 16 presets ; écarts
attendus : `rapports/env-28-mac.md` §1). Trunk de `~/lepton` au Mac, mêmes commits : 14 entrées
greffées, 3956 liens, 0 cassé, 0 fichier régulier.
Référence Debian : `rapports/env-21-debian.md` et `oracles/env-21-debian/` (host + 16 presets,
dernier oracle Debian complet).

La session VM ne développe pas : elle exécute, constate et rapporte. Pas de carte sur la VM : les
presets de carte sont construits, jamais flashés.

## 2. Ce que la session VM peut faire, et ne fait pas

| Autorisé | Interdit |
| --- | --- |
| `git fetch` / `switch` de `~/lepton-tools-dev/lepton-tools` (`devenv/env-28`) | Modifier `DEVENV-STATUS.md`, `ORCHESTRATION.md`, `SPECIFICATION.md`, `handoff/*.md`, les consignes |
| `git fetch` puis `switch master` + `merge --ff-only origin/master` du clone noyau `~/lepton-tools-dev/lepton-noyau` | Toute autre écriture dans ce clone |
| Lire les journaux des commandes lancées **par l'utilisateur** : `pipx install`, scripts d'installation (sudo), suppressions (§6, §11) | Lancer soi-même `sudo`, `pipx install`, `rm -rf` |
| `scion graft-update -v` dans `~/lepton-tools-dev/essais/env-14-debian` **seulement** (§7.1, accordé par l'ordre au titre de PA-P) | Tout autre `graft-update` ou `seed-update` ; toucher aux autres rootstocks hors §7.1, §10 |
| Créer `~/lepton-tools-dev/essais/env-28-debian` (rootstock neuf) et y tout faire, `build/` compris | Écrire un fichier régulier dans un `trunk/` ; corriger quoi que ce soit (consigner l'écart pour la session Mac) |
| Dans `~/lepton-tools-dev/essais/env-11/qemu` : `lepton check`, `lepton generate`, `git status` de la graine `env11` | Regreffer `env-11/qemu`, commiter dans sa graine |
| Lancer `lldb` (embarqué par CodeLLDB) ou `mklepton` sur `$R/build/host/mklepton` (§9) | Modifier l'espace de travail généré |
| Créer `devenv/env-28-debian` (depuis `devenv/env-28`) ; y écrire `doc/devenv/rapports/env-28-debian.md` et `doc/devenv/rapports/oracles/env-28-debian/` | Commiter sur une autre branche |
| `git push origin devenv/env-28-debian` **après accord explicite de l'utilisateur** (PA-P) | Pousser toute autre branche |

Règles des consignes VM (ORCHESTRATION §2bis, PA-31) :
- **Commandes confiées à l'utilisateur** : `pipx install`, scripts d'installation, `rm -rf` sont
  lancés par l'utilisateur dès le départ (commandes exactes ci-dessous) ; la session annonce
  l'attente par un `AVANCEMENT`, puis vérifie l'effet et le consigne. Les commandes scion qui
  clonent (§7) et `rejouer-oracle.sh` (§8) ont été acceptées par la session en R21-1 : la session
  les lance ; si le classifieur de permissions les refuse, elle ne contourne pas, envoie un
  `AVANCEMENT` avec la commande exacte, et l'utilisateur la lance.
- **Régénérer avant de relever** : tout relevé « avant » d'un fichier généré suit immédiatement
  la commande qui le produit (§6.1).

Tout écart au plan, toute erreur non prévue : s'arrêter, exposer (`AVANCEMENT` ou `QUESTION`),
attendre.

## 3. Communication (ORCHESTRATION §2bis)

- Session principale : `validate-env-22-27-debian` (session Mac) ; répondre à l'adresse `from`
  du message d'ordre.
- ID : `R28-1`, repris tel quel (`[ACCUSÉ R28-1] ENV-28 — …`, `[AVANCEMENT R28-1] …`,
  `[QUESTION R28-1] …`, `[FIN-SUCCÈS R28-1] …` ou `[FIN-ÉCHEC R28-1] …`).
- `ACCUSÉ` avant toute commande autre que les lectures du §5 : ordre reformulé en une phrase, tête
  réelle de `devenv/env-28` après `fetch`, résultats de `git ls-remote` du §5, tête de la graine
  de `essais/env-14-debian`, étapes prévues (§6 à §11), écarts déjà visibles.
- `AVANCEMENT` : quand l'utilisateur doit lancer une commande (§6.2, §11), après §6, §7, §8, §9,
  §10, et à chaque arrêt.
- `FIN-SUCCÈS` / `FIN-ÉCHEC` : résultat par critère du §12, commits et branche (poussée ou non),
  chemin du rapport, versions relevées, écarts, ce qui n'a pas été fait.

## 4. Journaux et variables

```bash
mkdir -p ~/env-28-journaux
J=~/env-28-journaux
T=~/lepton-tools-dev/lepton-tools
K=~/lepton-tools-dev/lepton-noyau
R=~/lepton-tools-dev/essais/env-28-debian
U=~/lepton-tools-dev/essais/env-14-debian
P=~/lepton-tools-dev/essais/env-11/qemu
G=https://github.com/lepton-distribution
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
test -e "$R" && echo "ARRÊT : $R existe déjà"
git -C "$T" status --short | head -5; git -C "$K" status --short | head -5; git -C "$K" branch --show-current
git -C "$T" fetch origin && git -C "$T" switch devenv/env-28 && git -C "$T" merge --ff-only origin/devenv/env-28 && git -C "$T" log --oneline -1
echo "scion tag $(git ls-remote $G/seed.scions.git 'refs/tags/0.5.3.0^{}' | cut -c1-7)"
echo "graine $(git ls-remote $G/lepton-seed.scions.git original-tree | cut -c1-7)"
for r in lepton-original-tree.scions lepton-famille-qemu-mps2 lepton-bsp-qemu-mps2-an386 \
         lepton-bsp-qemu-mps2-an500 lepton-famille-stm32f4xx lepton-bsp-nucleo-f429zi \
         lepton-bsp-nucleo-f439zi lepton-famille-stm32wlxx lepton-bsp-nucleo-wl55jc1 \
         lepton-famille-stm32f7xx lepton-bsp-stm32f746g-disco lepton-famille-samd21 \
         lepton-bsp-samd21-xplained-pro; do
  echo "$r $(git ls-remote $G/$r.git refs/heads/master | cut -c1-7)"
done
git -C "$U"/depots/lepton-seed.scions/original-tree log --oneline -1
git -C "$U"/depots/lepton-seed.scions/original-tree status --short | head -5
git -C "$U"/depots/lepton-seed.scions/original-tree rev-parse --abbrev-ref '@{u}'
grep -v '^#' "$U"/trunk/.scion.grafted.list | grep -c .
ls -d ~/lepton-tools-dev/essais/env-21-debian ~/env-21-journaux 2>&1
ls -d ~/.vscode-oss/extensions/vadimcn.vscode-lldb-* 2>&1
```
Attendu : commits du tableau du §1 ; graine de `$U` à 0f1275a (ENV-14), propre, amont
`origin/original-tree` ; 9 entrées greffées dans `$U`. Arrêts : `$R` existe ; lepton-tools ou
clone noyau non propre ; un commit diffère ; graine de `$U` modifiée ou sans amont ; moins de
4 Go libres dans `~`. embOS absent : pas un arrêt ; les presets `*-embos*` seront en échec
attendu, à consigner. Graine de `$U` déjà à 15740f9 : pas un arrêt, consigner que l'avance n'est
pas exercée (§7.1).

## 6. Installation (C1, C2)

### 6.1 Graine de projet : régénération puis relevé avant réinstallation (pour C7)

Avec le lepton actuel de la VM (`devenv/env-21` 65b19f7), **régénérer d'abord**, puis relever :
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
Attendu : clone noyau à 0c0cc4f ; `SCION_REF="${SCION_REF:-0.5.3.0}"`.

Puis `AVANCEMENT` : l'**utilisateur** lance, dans un terminal de la VM (sudo avec mot de passe),
**sans** `SCION_REF` dans l'environnement (défaut du noyau), dans cet ordre (scion d'abord : lepton
exige scion ≥ 0.5.3.0) :

```bash
J=~/env-28-journaux; K=~/lepton-tools-dev/lepton-noyau; T=~/lepton-tools-dev/lepton-tools
unset SCION_REF SCION_SPEC
bash "$K/scripts/install-debian.sh" --with-debug-tools 2>&1 | tee "$J/6.2-install-debian.log"; echo "code=${PIPESTATUS[0]}" | tee -a "$J/6.2-install-debian.log"
pipx install --force "$T" 2>&1 | tee "$J/6.2-lepton.log"; echo "code=${PIPESTATUS[0]}" | tee -a "$J/6.2-lepton.log"
bash "$T/scripts/install-vscodium.sh" --lepton-clone "$K" 2>&1 | tee "$J/6.2-install-vscodium-1.log"; echo "code=${PIPESTATUS[0]}" | tee -a "$J/6.2-install-vscodium-1.log"
bash "$T/scripts/install-vscodium.sh" --lepton-clone "$K" 2>&1 | tee "$J/6.2-install-vscodium-2.log"; echo "code=${PIPESTATUS[0]}" | tee -a "$J/6.2-install-vscodium-2.log"
```
La session lit ensuite les journaux. Attendu : quatre codes 0 ; `install-debian.sh` : scion
installé depuis `$G/seed.scions.git@0.5.3.0` (0.5.2.0 auparavant) ; seconde exécution
d'`install-vscodium.sh` : **`changements 0`**. Puis :
```bash
scion version | tail -1; lepton --version; codium --version | head -1
pipx list --short | grep -E '^(scion|lepton) '
dpkg-query -W -f '${Version}\n' codium; codium --list-extensions --show-versions | LC_ALL=C sort > "$J/6.2-extensions.txt"
grep -i lldb "$J/6.2-extensions.txt"
```
Attendu : `scion version: 0.5.3.0` ; `lepton 0.1.0`, `scion 0.5.3.0 (requis ≥ 0.5.3.0)` ;
`vadimcn.vscode-lldb@1.12.3`.

## 7. Graine en retard, puis rootstock neuf (C3)

### 7.1 Mise à jour de la graine de `$U` par scion (sans `git pull`)

```bash
cd "$U"
find trunk -type l | wc -l > "$J/7.1-liens-avant.txt"
scion graft-update -v > "$J/7.1-graft-update.log" 2>&1; echo "code=$?" >> "$J/7.1-graft-update.log"
grep -i 'graine' "$J/7.1-graft-update.log"
git -C depots/lepton-seed.scions/original-tree log --oneline -1
grep -v '^#' trunk/.scion.grafted.list | grep -c .
for d in depots/lepton/*/master; do echo "$d $(git -C $d rev-parse --short HEAD) $(git -C $d status --short | wc -l)"; done
echo "liens $(find trunk -type l | wc -l) cassés $(find -L trunk -type l | wc -l) réguliers $(find trunk -type f ! -name .scion.grafted.list | wc -l)"
```
Attendu : code 0 ; « graine … avancée : 0f1275a -> 15740f9 » ; 14 entrées (5 greffons clonés :
`bsp-nucleo-f439zi`, `family-stm32f7xx`, `bsp-stm32f746g-disco`, `family-samd21`,
`bsp-samd21-xplained-pro`) ; chaque clone au commit du §1 et propre ; 3956 liens, 0 cassé,
0 fichier régulier. Aucun `git pull` à la main.

### 7.2 Rootstock neuf depuis la graine publiée

```bash
mkdir "$R" && cd "$R"
scion rootstock-install > "$J/7.2-rootstock-install.log" 2>&1; echo "code=$?" >> "$J/7.2-rootstock-install.log"
scion seed-add --version original-tree $G/lepton-seed.scions.git > "$J/7.2-seed-add.log" 2>&1; echo "code=$?" >> "$J/7.2-seed-add.log"
scion graft > "$J/7.2-graft.log" 2>&1; echo "code=$?" >> "$J/7.2-graft.log"
grep -v '^#' trunk/.scion.grafted.list | grep -c .
for d in depots/lepton/*/master; do echo "$d $(git -C $d rev-parse --short HEAD)"; done
find trunk -type l -exec sh -c 'for l; do printf "%s\t%s\n" "$l" "$(readlink "$l")"; done' _ {} + | LC_ALL=C sort > "$J/7.2-trunk.tsv"
echo "liens $(find trunk -type l | wc -l) cassés $(find -L trunk -type l | wc -l) réguliers $(find trunk -type f ! -name .scion.grafted.list | wc -l) DS_Store $(find trunk -name .DS_Store | wc -l)"
diff <(cd "$U/trunk" && find . -type l | LC_ALL=C sort) <(cd "$R/trunk" && find . -type l | LC_ALL=C sort) && echo "liste des liens identique à \$U"
```
Attendu : codes 0 ; 14 entrées ; chaque clone au commit du §1 ; 3956 liens, 0 cassé, 0 fichier
régulier, 0 `.DS_Store` ; liste des liens identique à celle de `$U` après §7.1. Un nombre
différent de 3956 : relever `comm` contre la liste des fichiers suivis des clones, l'exposer.

## 8. Reconstructions et comparaisons (C4, C6)

Périmètre : host et les 16 presets croisés (QEMU : construction, fumée, banc KAL ; cartes :
construction et capture seulement).

```bash
cd "$T" && git switch -c devenv/env-28-debian devenv/env-28
scripts/oracle/rejouer-oracle.sh "$R" doc/devenv/rapports/oracles/env-28-debian \
  --qemu qemu-mps2-an386-embos --qemu qemu-mps2-an386-embos-soft \
  --qemu qemu-mps2-an386-freertos --qemu qemu-mps2-an386-freertos-soft \
  --qemu qemu-mps2-an500-embos --qemu qemu-mps2-an500-freertos \
  --carte nucleo-f429zi-embos --carte nucleo-f429zi-freertos \
  --carte nucleo-f439zi-embos --carte nucleo-f439zi-freertos \
  --carte nucleo-wl55jc1-embos --carte nucleo-wl55jc1-freertos \
  --carte samd21-xplained-pro-embos --carte samd21-xplained-pro-freertos \
  --carte stm32f746g-disco-embos --carte stm32f746g-disco-freertos > "$J/8-rejouer.log" 2>&1; echo "code=$?" >> "$J/8-rejouer.log"
tail -25 "$J/8-rejouer.log"
grep -h "tests passed" doc/devenv/rapports/oracles/env-28-debian/*/ctest.log doc/devenv/rapports/oracles/env-28-debian/*/banc-kal.log
find -L "$R/trunk" -type l | wc -l; find "$R/trunk" -type f ! -name .scion.grafted.list | wc -l
```
Attendu : code 0 ; host ctest 7/7 ; 16 presets construits ; fumée réussie ; banc QEMU sous
Debian (`net.ping_ftpd`, Linux seul, et `qemu-mps2-an386.peripheriques`, ENV-27, en plus du
banc de R21-1) :

| Preset | R21-1 Debian | Mac `env-27-apres` | Attendu R28-1 |
| --- | --- | --- | --- |
| `qemu-mps2-an386-{embos,freertos}` | 19/19 | 19/19 | **20/20** |
| `qemu-mps2-an386-{embos,freertos}-soft` | 15/15 | 15/15 | **16/16** |
| `qemu-mps2-an500-{embos,freertos}` | 19/19 | 18/18 | **19/19** |

Trunk sans fichier régulier ni lien cassé.

### 8.1 Tests du greffon d'essai (C6)

```bash
for p in qemu-mps2-an386-embos qemu-mps2-an386-embos-soft qemu-mps2-an386-freertos qemu-mps2-an386-freertos-soft qemu-mps2-an500-embos qemu-mps2-an500-freertos; do
  (cd "$R/build/$p" && ctest -N > "$J/8.1-ctest-N-$p.txt" 2>&1; echo "$p total=$(grep -c 'Test *#' $J/8.1-ctest-N-$p.txt) greffon=$(ctest -N -L 'greffon:' | grep -c 'Test *#') peripheriques=$(grep -c 'qemu-mps2-an386.peripheriques' $J/8.1-ctest-N-$p.txt)")
done
grep -h "peripheriques" doc/devenv/rapports/oracles/env-28-debian/qemu-mps2-an386-*/banc-kal.log
```
Attendu : an386 (4 presets) : `qemu-mps2-an386.peripheriques` listé une fois, `-L greffon:` = 2
(le test et sa fixture `smoke.lsh`), et le test **Passed** dans `banc-kal.log` ; an500 : 0 test
du greffon, liste = celle de R21-1.

### 8.2 Comparaisons (C4)

L'arbre a changé depuis R21-1 : la non-régression Debian se lit **par rapport aux écarts déjà
constatés au Mac** entre `env-20-apres` et `env-27-apres` (`rapports/env-28-mac.md` §1).

```bash
cd "$T"; O=doc/devenv/rapports/oracles
diff -q $O/env-27-apres/host/mklepton-empreintes.sha256 $O/env-28-debian/host/mklepton-empreintes.sha256 && echo "mklepton = Mac env-27-apres"
diff $O/env-21-debian/host/mklepton-empreintes.sha256 $O/env-28-debian/host/mklepton-empreintes.sha256 | grep -c '^>'
for p in $(ls $O/env-28-debian | grep -v -e host -e '\.log$'); do
  python3 scripts/oracle/comparer-oracle.py $O/env-21-debian/$p $O/env-28-debian/$p > "$J/8.2-cmp-R21-$p.txt" 2>&1; a=$?
  python3 scripts/oracle/comparer-oracle.py $O/env-27-apres/$p $O/env-28-debian/$p > "$J/8.2-cmp-Mac-$p.txt" 2>&1; b=$?
  echo "$p comparer_R21-1=$a comparer_Mac=$b symboles=$(wc -l < $O/env-28-debian/$p/symboles.txt)"
done
for s in embos freertos; do
  python3 scripts/oracle/comparer-oracle.py $O/env-28-debian/nucleo-f429zi-$s $O/env-28-debian/nucleo-f439zi-$s > /dev/null 2>&1; echo "f429→f439 $s=$?"
done
```

Attendu : mklepton : empreintes identiques à `env-27-apres` (50 lignes) ; contre `env-21-debian`,
14 lignes différentes (`.fsflash.o` et `dev_dskimg.c` des 7 combinaisons, cpufs d'ENV-24).
`comparer_R21-1` : **1 partout**, et chaque fichier `8.2-cmp-R21-<preset>.txt` ne contient que
les écarts du cpufs relevés au Mac (`rapports/env-28-mac.md` §1) :

| Presets | `.text` (delta exact attendu) | `filecpu_memory` (taille, avant → après) | DWARF |
| --- | --- | --- | --- |
| `qemu-mps2-an386-*` (4), `qemu-mps2-an500-*` (2), `nucleo-f429zi-*`, `nucleo-f439zi-*`, `stm32f746g-disco-*` (2 chacun) | −122064 | `0001f401` → `00001734` | `.debug_abbrev` −17, `.debug_info` −7 |
| `nucleo-wl55jc1-*` (2) | −6248 | `00001f41` → `000006dc` | `.debug_abbrev` −17, `.debug_info` −5 |
| `samd21-xplained-pro-*` (2) | −1368 | `00000c01` → `000006ab` | aucun |

Une section ou un symbole hors de ce tableau, ou un delta différent : écart à exposer (extrait du
fichier `8.2-cmp-R21-<preset>.txt`), pas à corriger. Les variations propres à la chaîne Debian
(`rapports/env-21-debian.md` §3 : `.text` de quelques octets, `.noinit` sur SAMD21 FreeRTOS)
doivent se retrouver **inchangées** par rapport à R21-1, donc absentes de `comparer_R21-1`.
`comparer_Mac` : informatif (chaînes différentes ; 1 attendu partout). `f429→f439` : 0.

## 9. Fichiers générés par lepton sur `$R` (C5)

```bash
lepton check -C "$R" > "$J/9-check-R.log" 2>&1; echo "code=$?" >> "$J/9-check-R.log"
lepton generate -C "$R" > "$J/9-generate-R.log" 2>&1; echo "code=$?" >> "$J/9-generate-R.log"
W="$R"/original-tree.code-workspace
for k in '"request"' '"svdFile"' '"type": "lldb"'; do echo "$k $(grep -c "$k" "$W")"; done
grep -o '"svdFile": "[^"]*"' "$W" | sort | uniq -c
sha256sum "$R"/trunk/sys/root/src/kernel/dev/arch/cortexm/*/svd/*.svd
find "$R/trunk" -type f ! -name .scion.grafted.list | wc -l
```
Attendu : `check` et `generate` code 0 ; 23 `"request"` (16 lancements de cible + 7 lancements
hôtes de `mklepton`), 10 `"svdFile"` (2 par fichier, chemins sous `$R/trunk`), 7 `"type": "lldb"` ;
sommes SHA-256 des SVD :

| Fichier | SHA-256 |
| --- | --- |
| `samd21/svd/ATSAMD21J18A.svd` | `1fba37ed6aacf9694fd801b46b7b86a5fd569e8c50eeb0179f4c8b6d34ff1328` |
| `stm32f4xx/svd/STM32F429.svd` | `185ddfe09ebec697628850d3c262092c477924ff618d29cf3a2d6e453b44336b` |
| `stm32f4xx/svd/STM32F439.svd` | `c3de4e42c9fa2e0196f364efa25d163e4a9813b6c6b2fd0f5a8ffb64158851c9` |
| `stm32f7xx/svd/STM32F746.svd` | `6fc35eb5b44199f5e85c5e8d7994a4c50177c74354f690e6837b852d65d8daee` |
| `stm32wlxx/svd/STM32WL5x_CM4.svd` | `bc8642b4f6c1de77af9686476693ab42976dd574e54872e8787f4e7e82768c75` |

Trunk sans fichier régulier.

### 9.1 Lancement DBG-5 : `mklepton` hors débogueur, puis arrêt dans `main`

Extraction du lancement « Déboguer mklepton qemu-mps2-an386 (…) » de l'espace (la première ligne
est un commentaire) :
```bash
python3 - "$W" > "$J/9.1-lancement-an386.sh" <<'EOF'
import json, shlex, sys
w = json.loads(open(sys.argv[1]).read().split('\n', 1)[1])
c = [c for c in w['launch']['configurations']
     if c.get('type') == 'lldb' and 'mklepton qemu-mps2-an386' in c['name']][0]
print('CWD=' + shlex.quote(c['cwd']))
print('PROG=' + shlex.quote(c['program']))
print('ARGS=(' + ' '.join(shlex.quote(a) for a in c['args']) + ')')
print('ENVS=(' + ' '.join(shlex.quote(f'{k}={v}') for k, v in c.get('env', {}).items()) + ')')
print('TACHE=' + shlex.quote(c.get('preLaunchTask', '')))
EOF
cat "$J/9.1-lancement-an386.sh"; . "$J/9.1-lancement-an386.sh"
```
Attendu : `PROG=$R/build/host/mklepton`, `CWD=$R/build/.mklepton/qemu-mps2-an386`, `ARGS`
commençant par `-s $R/trunk -o $CWD`, `ENVS=(SOURCE_DATE_EPOCH=0)`, `TACHE` = « lepton : préparer
le débogage de mklepton ».

Hors débogueur (ce que fait la tâche préalable, puis le lancement) :
```bash
mkdir -p "$CWD" && (cd "$CWD" && env "${ENVS[@]}" "$PROG" "${ARGS[@]}") > "$J/9.1-mklepton.log" 2>&1; echo "code=$?" >> "$J/9.1-mklepton.log"
diff -r "$CWD" "$R/build/qemu-mps2-an386-embos/generated/board" && echo "sorties = construction"
```
Attendu : code 0 ; fichiers identiques octet pour octet à ceux de la construction (6 au Mac).

Arrêt dans `main` : **<forme tranchée au PA-43, reportée dans l'ordre R28-1>**.
- Forme A (session, lldb embarqué par CodeLLDB) :
  ```bash
  LLDB=$(ls -d ~/.vscode-oss/extensions/vadimcn.vscode-lldb-1.12.3*/lldb/bin/lldb | head -1); echo "$LLDB"
  (cd "$CWD" && env "${ENVS[@]}" "$LLDB" -b -o 'breakpoint set -n main' -o 'process launch' \
     -o 'frame variable argc' -o 'frame info' -o 'process kill' -- "$PROG" "${ARGS[@]}") > "$J/9.1-lldb.log" 2>&1; echo "code=$?" >> "$J/9.1-lldb.log"
  grep -E 'stop reason|argc|frame #0' "$J/9.1-lldb.log"
  ```
  Attendu : `stop reason = breakpoint 1.1` ; `frame #0` dans `main` de
  `$R/trunk/tools/mklepton/src/mklepton.c` (chemin du trunk) ; `(int) argc = 10`.
- Forme B (utilisateur, VSCodium) : `codium "$R"/original-tree.code-workspace`, point d'arrêt dans
  `main` de `trunk/tools/mklepton/src/mklepton.c`, lancement « Déboguer mklepton qemu-mps2-an386
  (mkconf_tauon_basic_qemu_mps2.xml) » ; l'utilisateur rapporte : arrêt atteint, `argc`/`argv`
  lisibles, fichier source ouvert par le trunk, tâche préalable exécutée ou non.

## 10. Graine de projet existante après réinstallation (C7)

```bash
lepton generate -C "$P" > "$J/10-generate-P-apres.log" 2>&1; echo "code=$?" >> "$J/10-generate-P-apres.log"
lepton check -C "$P" > "$J/10-check-P-apres.log" 2>&1; echo "code=$?" >> "$J/10-check-P-apres.log"
git -C "$P"/depots/lepton-seed/env11 status --short > "$J/10-graine-P-apres.txt"
sha256sum "$P"/depots/lepton-seed/env11/project/scion/CMakeUserPresets.json "$P"/*.code-workspace > "$J/10-generes-P-apres.sha256"
diff "$J/6.1-generes-P-avant.sha256" "$J/10-generes-P-apres.sha256"
diff "$J/6.1-graine-P-avant.txt" "$J/10-graine-P-apres.txt" && echo "graine P inchangée"
diff <(grep -v '^code=' "$J/6.1-check-P-avant.log") <(grep -v '^code=' "$J/10-check-P-apres.log") && echo "check P identique"
diff "$J/6.1-P-avant/CMakeUserPresets.json" "$P"/depots/lepton-seed/env11/project/scion/CMakeUserPresets.json && echo "presets P identiques"
diff "$J/6.1-P-avant/"*.code-workspace "$P"/*.code-workspace > "$J/10-espace-P.diff"; cat "$J/10-espace-P.diff"
```
Attendu : `generate` et `check` code 0 ; graine inchangée ; sortie de `check` et
`CMakeUserPresets.json` identiques ; espace de travail : **différence limitée aux ajouts de
DBG-5**, comme au Mac sur `env-11/qemu` (`rapports/env-25-dbg5.md` §3.1) : 1 lancement hôte
`lldb` en fin de `launch`, la tâche « lepton : préparer le débogage de mklepton » après
« lepton : mklepton (preset host) », `vadimcn.vscode-lldb` dans les recommandations ; seule ligne
retirée admise : `"marus25.cortex-debug"` réécrite avec une virgule. Aucun `svdFile` (QEMU). Toute
autre différence : la relever telle quelle, l'exposer.

## 11. Nettoyage de la VM (C8)

Seulement si l'ordre `R28-1` l'accorde. Relevé par la session :
```bash
du -sh ~/lepton-tools-dev/essais/env-21-debian ~/env-21-journaux
```
Puis `AVANCEMENT` : l'**utilisateur** lance :
```bash
rm -rf ~/lepton-tools-dev/essais/env-21-debian ~/env-21-journaux
```
La session vérifie :
```bash
ls -d ~/lepton-tools-dev/essais/env-21-debian ~/env-21-journaux 2>&1
```
Le rootstock `$R`, `$U` et `$J` sont conservés.

## 12. Critères et rapport

| Critère | Attendu |
| --- | --- |
| C1 scion et lepton | `git ls-remote` conforme au §1 ; scion 0.5.3.0 (par `install-debian.sh`) ; `pipx install --force` de lepton code 0 ; `lepton 0.1.0`, scion 0.5.3.0 accepté ; versions relevées |
| C2 Scripts d'installation | `install-debian.sh` du noyau (0c0cc4f, défaut `SCION_REF` 0.5.3.0) code 0 ; `install-vscodium.sh` code 0 deux fois, `changements 0` à la seconde ; CodeLLDB 1.12.3 présent |
| C3 Graine et rootstock | §7.1 : graine de `$U` avancée par `graft-update` (0f1275a → 15740f9), 14 entrées, clones au §1, 3956 liens, 0 cassé, 0 régulier ; §7.2 : rootstock neuf, 14 entrées, 3956 liens, 0 cassé, 0 régulier, liste identique à `$U` |
| C4 Constructions | host ctest 7/7, empreintes mklepton = `env-27-apres` ; 16 presets construits ; QEMU fumée et banc 20/20, 16/16, 19/19 ; `comparer_R21-1` limité au tableau du §8.2 ; `f429→f439` 0 |
| C5 DBG-5 et DBG-4 | `check`, `generate` code 0 sur `$R` ; 23 lancements, 7 `lldb`, 10 `svdFile`, SVD aux sommes du §9 ; `mklepton` du lancement : sorties = construction ; arrêt dans `main` constaté (forme du PA-43) |
| C6 Tests du greffon | `qemu-mps2-an386.peripheriques` listé et réussi dans les 4 presets an386 ; absent d'an500 |
| C7 Graine de projet `env11` | `check`, `generate` code 0 ; `check`, presets et graine identiques ; espace : ajouts DBG-5 seuls |
| C8 Nettoyage | selon l'ordre : `env-21-debian` et `~/env-21-journaux` supprimés par l'utilisateur (taille relevée), ou « non demandé » |

Rapport `doc/devenv/rapports/env-28-debian.md` sur `devenv/env-28-debian`, contenant : hôte et
versions (§5, §6), table des critères, table des presets (construction, fumée, banc KAL, symboles
R28-1 / R21-1, `comparer_R21-1`, `comparer_Mac`), écarts, journal des messages §2bis (ID, date,
résumé). Commit du rapport et de `oracles/env-28-debian/`, puis `QUESTION` à l'utilisateur pour le
push (PA-P), puis `FIN-*`.
