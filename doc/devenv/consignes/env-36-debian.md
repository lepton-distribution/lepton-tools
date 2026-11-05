# Consigne — session Claude Code sur la VM Debian — ENV-36 (validation Debian groupée)

Fichier autonome : avec `ORCHESTRATION.md` §2bis, il suffit à conduire la session VM. Rédigé le
2026-11-05 par la session Mac `validate-env-34-35-debian` (tâche 1 d'ENV-36), repris de
`consignes/env-33-debian.md`. Son texte est envoyé tel quel dans l'ordre `R36-1`.

## 1. Objet

Valider sur Debian x86_64 l'état publié après ENV-34 et ENV-35 :
- `scion graft-update` d'un rootstock existant : `cubemx_hal_driver/` retiré, HAL STM32F4 v1.8.5
  et CMSIS device F4 importés, `core_cm4.h` 5.9.0 ajouté au noyau ; rootstock neuf depuis la
  graine publiée ;
- constructions host et 16 presets : seuls les 4 presets F4 changent (passage de la SPL à la HAL,
  ENV-35), avec les mêmes écarts que sur le Mac ;
- compilation à blanc de la HAL F4 importée avec la chaîne APT ;
- fichiers générés par lepton inchangés.

Aucune réinstallation : scion 0.5.4.0 est inchangé ; le paquet lepton est identique à celui
installé en R33-1 (`devenv/env-33` e47bc11 → `main` 06cb55d : seuls `scripts/tiers/` et `doc/`
changent, hors paquet).

Références publiées (toutes poussées, aucune fusion différée) :

| Dépôt (`https://github.com/lepton-distribution/…`) | Référence | Commit | En R33-1 |
| --- | --- | --- | --- |
| `lepton-tools` | `devenv/env-36` (cette consigne ; code identique à `main` 06cb55d) | tête après `fetch` | e47bc11 |
| `seed.scions` | tag `0.5.4.0` | 99aa973 | = |
| `lepton-seed.scions` | `original-tree` | 15740f9 | = |
| `lepton-original-tree.scions` (noyau) | `master` | **2893297** | b3a5415 |
| `lepton-famille-qemu-mps2` | `master` | 3954357 | = |
| `lepton-bsp-qemu-mps2-an386` | `master` | 09f4943 | = |
| `lepton-bsp-qemu-mps2-an500` | `master` | e98a482 | = |
| `lepton-famille-stm32f4xx` | `master` | **0fd8b2a** | 8364493 |
| `lepton-bsp-nucleo-f429zi` | `master` | **b9fe2bf** | 2b2dfdd |
| `lepton-bsp-nucleo-f439zi` | `master` | **314f91b** | bdbfa06 |
| `lepton-famille-stm32wlxx` | `master` | dbc58d7 | = |
| `lepton-bsp-nucleo-wl55jc1` | `master` | ef51ec1 | = |
| `lepton-famille-stm32f7xx` | `master` | d2d9aa9 | = |
| `lepton-bsp-stm32f746g-disco` | `master` | 6266908 | = |
| `lepton-famille-samd21` | `master` | a262e81 | = |
| `lepton-bsp-samd21-xplained-pro` | `master` | f3cffa2 | = |

Référence Mac : oracle `doc/devenv/rapports/oracles/env-35-apres/` (host + 16 presets) ; écarts
Mac `env-32-apres` → `env-35-apres` et attendus dérivés : `rapports/env-36-mac.md` §1 et
`rapports/env-36-mac/attendu/`. Trunk de `~/lepton` au Mac, mêmes commits : 14 entrées greffées,
3978 liens, 0 cassé. Référence Debian : `rapports/env-33-debian.md` et `oracles/env-33-debian/`
(dernier oracle Debian complet ; binaires F4 = SPL).

La session VM ne développe pas : elle exécute, constate et rapporte. <CARTES : à fixer au PA-59 ;
par défaut, pas de carte sur la VM : les presets de carte sont construits, jamais flashés.>

## 2. Ce que la session VM peut faire, et ne fait pas

| Autorisé | Interdit |
| --- | --- |
| `git fetch` / `switch` de `~/lepton-tools-dev/lepton-tools` (`devenv/env-36`) | Modifier `DEVENV-STATUS.md`, `ORCHESTRATION.md`, `SPECIFICATION.md`, `handoff/*.md`, les consignes, `rapports/env-36-mac*` |
| Lire les journaux des commandes lancées **par l'utilisateur** : `scion graft-update`, suppressions (§6, §10) | Lancer soi-même `sudo`, `pipx install`, `scion graft-update`, `rm -rf` |
| Lectures dans `$U` (§5, §6) | Toute écriture dans les clones de `$U` ; tout `seed-update` ; toucher aux autres rootstocks hors §6, §9 |
| Créer `~/lepton-tools-dev/essais/env-36-debian` (rootstock neuf) et y tout faire, `build/` compris | Écrire un fichier régulier dans un `trunk/` ; corriger quoi que ce soit (consigner l'écart pour la session Mac) |
| `lepton check` / `generate` dans `$P` (`essais/env-11/qemu`) et dans `$R` | Regreffer `$P`, commiter dans sa graine |
| Compilation à blanc dans `$J/8-hal-blanc` (§8) | Flasher une carte, lancer un test `board` |
| Créer `devenv/env-36-debian` (depuis `devenv/env-36`) ; y écrire `doc/devenv/rapports/env-36-debian.md` et `doc/devenv/rapports/oracles/env-36-debian/` | Commiter sur une autre branche |
| `git push origin devenv/env-36-debian` **après accord explicite de l'utilisateur** (PA-P) | Pousser toute autre branche |

Règles des consignes VM (ORCHESTRATION §2bis) :
- **Commandes confiées à l'utilisateur** : `scion graft-update` (refusé à la session en R28-1,
  « Untrusted Code Integration ») et `rm -rf` sont lancés par l'utilisateur dès le départ
  (commandes exactes ci-dessous) ; la session annonce l'attente par un `AVANCEMENT`, puis vérifie
  l'effet et le consigne. `scion rootstock-install`, `seed-add`, `graft` (§6.2) et
  `rejouer-oracle.sh` (§7) ont été acceptés en R28-1 et R33-1 : la session les lance ; si le
  classifieur de permissions les refuse, elle ne contourne pas, envoie un `AVANCEMENT` avec la
  commande exacte, et l'utilisateur la lance.
- **Régénérer avant de relever** : tout relevé « avant » d'un fichier généré suit immédiatement
  la commande qui le produit (§5.1).
- **Branche des clones d'un rootstock existant** : la branche courante de chaque clone de `$U`
  est relevée au §5 et consignée. scion 0.5.4.0 refuse lui-même un clone hors de sa version
  déclarée ; un tel refus reste un écart à exposer.

Tout écart au plan, toute erreur non prévue : s'arrêter, exposer (`AVANCEMENT` ou `QUESTION`),
attendre.

## 3. Communication (ORCHESTRATION §2bis)

- Session principale : `validate-env-34-35-debian` (session Mac) ; répondre à l'adresse `from`
  du message d'ordre.
- ID : `R36-1`, repris tel quel (`[ACCUSÉ R36-1] ENV-36 — …`, `[AVANCEMENT R36-1] …`,
  `[QUESTION R36-1] …`, `[FIN-SUCCÈS R36-1] …` ou `[FIN-ÉCHEC R36-1] …`).
- `ACCUSÉ` avant toute commande autre que les lectures du §5 : ordre reformulé en une phrase, tête
  réelle de `devenv/env-36` après `fetch`, résultats de `git ls-remote` du §5, branches et têtes
  des clones de `$U`, étapes prévues (§6 à §10), écarts déjà visibles.
- `AVANCEMENT` : quand l'utilisateur doit agir (§6.1, §10), après §6, §7, §8, §9, et à chaque
  arrêt.
- `FIN-SUCCÈS` / `FIN-ÉCHEC` : résultat par critère du §11, commits et branche (poussée ou non),
  chemin du rapport, versions relevées, écarts, ce qui n'a pas été fait.

## 4. Journaux et variables

```bash
mkdir -p ~/env-36-journaux
J=~/env-36-journaux
T=~/lepton-tools-dev/lepton-tools
R=~/lepton-tools-dev/essais/env-36-debian
R33=~/lepton-tools-dev/essais/env-33-debian
U=~/lepton-tools-dev/essais/env-28-debian
P=~/lepton-tools-dev/essais/env-11/qemu
G=https://github.com/lepton-distribution
O=doc/devenv/rapports/oracles
A=doc/devenv/rapports/env-36-mac/attendu
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
git -C "$T" fetch origin && git -C "$T" switch devenv/env-36 && git -C "$T" merge --ff-only origin/devenv/env-36 && git -C "$T" log --oneline -1
echo "scion tag $(git ls-remote $G/seed.scions.git 'refs/tags/0.5.4.0^{}' | cut -c1-7)"
echo "graine $(git ls-remote $G/lepton-seed.scions.git original-tree | cut -c1-7)"
for r in lepton-original-tree.scions lepton-famille-qemu-mps2 lepton-bsp-qemu-mps2-an386 \
         lepton-bsp-qemu-mps2-an500 lepton-famille-stm32f4xx lepton-bsp-nucleo-f429zi \
         lepton-bsp-nucleo-f439zi lepton-famille-stm32wlxx lepton-bsp-nucleo-wl55jc1 \
         lepton-famille-stm32f7xx lepton-bsp-stm32f746g-disco lepton-famille-samd21 \
         lepton-bsp-samd21-xplained-pro; do
  echo "$r $(git ls-remote $G/$r.git refs/heads/master | cut -c1-7)"
done
# Rootstock existant $U
git -C "$U"/depots/lepton-seed.scions/original-tree log --oneline -1
git -C "$U"/depots/lepton-seed.scions/original-tree status --short | head -5
grep -v '^#' "$U"/trunk/.scion.grafted.list | grep -c .
for d in "$U"/depots/lepton/*/master; do
  echo "$(basename $(dirname $d)) $(git -C $d branch --show-current) $(git -C $d rev-parse --short HEAD) $(git -C $d rev-parse --abbrev-ref '@{u}' 2>&1) modifs=$(git -C $d status --short | wc -l)"
done | tee "$J/5-clones-U.txt"
echo "liens $(find "$U"/trunk -type l | wc -l) cassés $(find -L "$U"/trunk -type l | wc -l) réguliers $(find "$U"/trunk -type f ! -name .scion.grafted.list | wc -l)"
ls -A "$U"
# Rootstock neuf de R33-1 et graine de projet $P (C5)
ls -d "$R33" "$R33"/original-tree.code-workspace 2>&1
ls -d "$P"/depots/lepton-seed/env11
ls -d ~/env-33-journaux 2>&1
```
Attendu : commits du tableau du §1 ; scion 0.5.4.0 ; `lepton 0.1.0`, `scion 0.5.4.0 (requis ≥
0.5.4.0)` ; chaîne APT de R33-1 (arm-none-eabi-gcc 14.2.1, cmake 3.31.6, ninja 1.12.1, QEMU
10.0.13, Python 3.13.5, codium 1.135.06055) ; `$U` : graine à 15740f9, propre ; 14 entrées
greffées ; **13 clones sur `master`**, amont `origin/master`, aucune modification, aux commits de
la colonne « En R33-1 » (noyau b3a5415, `family-stm32f4xx` 8364493, `bsp-nucleo-f429zi` 2b2dfdd,
`bsp-nucleo-f439zi` bdbfa06, les autres égaux) ; 3957 liens, 0 cassé, 0 fichier régulier.

Arrêts : `$R` existe ; lepton-tools non propre ; un commit publié diffère ; scion différent de
0.5.4.0 ; graine de `$U` modifiée ; un clone de `$U` hors de `master`, sans amont ou modifié ;
moins de 6 Go libres dans `~`. embOS absent : pas un arrêt ; les presets `*-embos*` seront en
échec attendu, à consigner. Une version de la chaîne APT différente de R33-1 : pas un arrêt, à
consigner (elle peut expliquer un écart au §7.1).

### 5.1 Fichiers générés : régénération puis relevé avant (pour C5)

```bash
lepton generate -C "$P" > "$J/5.1-generate-P-avant.log" 2>&1; echo "code=$?" >> "$J/5.1-generate-P-avant.log"
lepton check -C "$P" > "$J/5.1-check-P-avant.log" 2>&1; echo "code=$?" >> "$J/5.1-check-P-avant.log"
git -C "$P"/depots/lepton-seed/env11 status --short > "$J/5.1-graine-P-avant.txt"
sha256sum "$P"/depots/lepton-seed/env11/project/scion/CMakeUserPresets.json "$P"/*.code-workspace > "$J/5.1-generes-P-avant.sha256"
lepton generate -C "$R33" > "$J/5.1-generate-R33.log" 2>&1; echo "code=$?" >> "$J/5.1-generate-R33.log"
cp "$R33"/original-tree.code-workspace "$J/5.1-R33.code-workspace"
```
`$R33` n'a pas été regreffé depuis R33-1 : son espace sert de référence pour celui de `$R` (§9).

## 6. `graft-update` d'un rootstock existant, rootstock neuf (C2)

### 6.1 `$U`

Par la session :
```bash
cd "$U"
find trunk -type l | LC_ALL=C sort > "$J/6.1-liens-avant.txt"; wc -l < "$J/6.1-liens-avant.txt"
```
Puis `AVANCEMENT` : l'**utilisateur** lance :
```bash
J=~/env-36-journaux; cd ~/lepton-tools-dev/essais/env-28-debian
scion graft-update -v > "$J/6.1-graft-update.log" 2>&1; echo "code=$?" >> "$J/6.1-graft-update.log"
```
Puis la session :
```bash
cd "$U"
tail -15 "$J/6.1-graft-update.log"; grep -i -E 'graine|conflit|refus' "$J/6.1-graft-update.log"
git -C depots/lepton-seed.scions/original-tree log --oneline -1
grep -v '^#' trunk/.scion.grafted.list | grep -c .
for d in depots/lepton/*/master; do echo "$(basename $(dirname $d)) $(git -C $d branch --show-current) $(git -C $d rev-parse --short HEAD) modifs=$(git -C $d status --short | wc -l)"; done | tee "$J/6.1-clones-apres.txt"
find trunk -type l | LC_ALL=C sort > "$J/6.1-liens-apres.txt"
LC_ALL=C comm -13 "$J/6.1-liens-avant.txt" "$J/6.1-liens-apres.txt" > "$J/6.1-ajoutes.txt"
LC_ALL=C comm -23 "$J/6.1-liens-avant.txt" "$J/6.1-liens-apres.txt" > "$J/6.1-retires.txt"
diff "$T/$A/liens-ajoutes.txt" "$J/6.1-ajoutes.txt" && echo "ajouts = attendu (215)"
diff "$T/$A/liens-retires.txt" "$J/6.1-retires.txt" && echo "retraits = attendu (194)"
echo "cubemx $(grep -c cubemx_hal_driver/ "$J/6.1-liens-apres.txt") hal_driver $(grep -c 'stm32f4xx/hal_driver/' "$J/6.1-liens-apres.txt") device_f4 $(grep -c 'cmsis-5/Device/ST/STM32F4xx/' "$J/6.1-liens-apres.txt")"
echo "liens $(wc -l < $J/6.1-liens-apres.txt) cassés $(find -L trunk -type l | wc -l) réguliers $(find trunk -type f ! -name .scion.grafted.list | wc -l)"
```
Attendu : code 0, 0 conflit ; graine inchangée (15740f9) ; 14 entrées ; 13 clones sur `master`,
propres, aux commits du §1 (noyau, famille F4, BSP F429 et F439 avancés par avance rapide) ;
ajouts et retraits **identiques** aux listes `attendu/liens-ajoutes.txt` (215 : 201 sous
`hal_driver/`, 7 sous `cmsis-5/Device/ST/STM32F4xx/`, `core_cm4.h` et `LEPTON-PROVENANCE.md` de
`cmsis-5/CMSIS/Core/`, 3 sources `dev_stm32f4xx_eth_x.{c,h}` et `dev_stm32f4xx_hal_tick.c`,
2 `stm32f4xx_hal_conf.h` des BSP) et `attendu/liens-retires.txt` (194 : 190 sous
`cubemx_hal_driver/`, 4 en-têtes HAL V1.3.0 de `driverlib/`) ; `cubemx 0 hal_driver 201
device_f4 7` ; 3978 liens, 0 cassé, 0 fichier régulier. Toute autre ligne : écart à exposer.

### 6.2 Rootstock neuf depuis la graine publiée

```bash
mkdir "$R" && cd "$R"
scion rootstock-install > "$J/6.2-rootstock-install.log" 2>&1; echo "code=$?" >> "$J/6.2-rootstock-install.log"
scion seed-add --version original-tree $G/lepton-seed.scions.git > "$J/6.2-seed-add.log" 2>&1; echo "code=$?" >> "$J/6.2-seed-add.log"
scion graft > "$J/6.2-graft.log" 2>&1; echo "code=$?" >> "$J/6.2-graft.log"
grep -v '^#' trunk/.scion.grafted.list | grep -c .
for d in depots/lepton/*/master; do echo "$d $(git -C $d branch --show-current) $(git -C $d rev-parse --short HEAD)"; done
echo "liens $(find trunk -type l | wc -l) cassés $(find -L trunk -type l | wc -l) réguliers $(find trunk -type f ! -name .scion.grafted.list | wc -l)"
diff <(cd "$U/trunk" && find . -type l | LC_ALL=C sort) <(cd "$R/trunk" && find . -type l | LC_ALL=C sort) && echo "liste des liens identique à \$U"
```
Attendu : codes 0 ; 14 entrées ; chaque clone sur `master` au commit du §1 ; 3978 liens, 0 cassé,
0 fichier régulier ; liste des liens identique à celle de `$U` après §6.1.

## 7. Reconstructions et comparaisons (C3)

Périmètre : host et les 16 presets croisés (QEMU : construction, fumée, banc KAL ; cartes :
construction et capture seulement).

```bash
cd "$T" && git switch -c devenv/env-36-debian devenv/env-36
scripts/oracle/rejouer-oracle.sh "$R" $O/env-36-debian \
  --qemu qemu-mps2-an386-embos --qemu qemu-mps2-an386-embos-soft \
  --qemu qemu-mps2-an386-freertos --qemu qemu-mps2-an386-freertos-soft \
  --qemu qemu-mps2-an500-embos --qemu qemu-mps2-an500-freertos \
  --carte nucleo-f429zi-embos --carte nucleo-f429zi-freertos \
  --carte nucleo-f439zi-embos --carte nucleo-f439zi-freertos \
  --carte nucleo-wl55jc1-embos --carte nucleo-wl55jc1-freertos \
  --carte samd21-xplained-pro-embos --carte samd21-xplained-pro-freertos \
  --carte stm32f746g-disco-embos --carte stm32f746g-disco-freertos > "$J/7-rejouer.log" 2>&1; echo "code=$?" >> "$J/7-rejouer.log"
tail -25 "$J/7-rejouer.log"
grep -h "tests passed" $O/env-36-debian/*/ctest.log $O/env-36-debian/*/banc-kal.log
grep -h "peripheriques" $O/env-36-debian/qemu-mps2-an386-*/banc-kal.log
find -L "$R/trunk" -type l | wc -l; find "$R/trunk" -type f ! -name .scion.grafted.list | wc -l
```
Attendu : code 0 ; host ctest 7/7 ; 16 presets construits ; fumée réussie ; banc QEMU
**identique à R33-1** (aucun test QEMU changé depuis) : an386 20/20, an386 soft 16/16, an500
19/19 (`net.ping_ftpd` ne tourne que sous Linux ; Mac : 19, 15, 18) ;
`qemu-mps2-an386.peripheriques` **Passed** dans les 4 `banc-kal.log` an386. Trunk sans fichier
régulier ni lien cassé.

### 7.1 Comparaisons

La non-régression Debian se lit **par rapport à R33-1** et aux écarts constatés au Mac entre
`env-32-apres` et `env-35-apres` (`rapports/env-36-mac.md` §1). Normalisation : noms seuls (les
tailles diffèrent entre la chaîne du Mac et la chaîne APT), sections `.debug_*` exclues.

```bash
cd "$T"
norm() { grep -E '^(section|symbole)' "$1" | sed -E 's/ \[.*$//; s/ +: /: /' | grep -v -E '^section [^:]*: \.debug_' | LC_ALL=C sort; }
diff -q $O/env-33-debian/host/mklepton-empreintes.sha256 $O/env-36-debian/host/mklepton-empreintes.sha256 && echo "mklepton = R33-1"
diff -q $O/env-35-apres/host/mklepton-empreintes.sha256 $O/env-36-debian/host/mklepton-empreintes.sha256 && echo "mklepton = Mac env-35-apres"
for p in $(ls $O/env-36-debian | grep -v -e host -e ctest-N -e '\.log$'); do
  python3 scripts/oracle/comparer-oracle.py $O/env-33-debian/$p $O/env-36-debian/$p > "$J/7.1-cmp-R33-$p.txt" 2>&1; a=$?
  python3 scripts/oracle/comparer-oracle.py $O/env-35-apres/$p $O/env-36-debian/$p > "$J/7.1-cmp-Mac-$p.txt" 2>&1; b=$?
  echo "$p comparer_R33-1=$a comparer_Mac=$b symboles=$(wc -l < $O/env-36-debian/$p/symboles.txt)"
done | tee "$J/7.1-bilan.txt"
for p in nucleo-f429zi-embos nucleo-f429zi-freertos nucleo-f439zi-embos nucleo-f439zi-freertos; do
  norm "$J/7.1-cmp-R33-$p.txt" > "$J/7.1-$p.noms.txt"
  diff "$A/$p.noms.txt" "$J/7.1-$p.noms.txt" > "$J/7.1-$p.noms.diff" && echo "$p : écarts = Mac ($(wc -l < $A/$p.noms.txt) lignes)" || echo "$p : DIFFÈRE"
  grep -E '^section modifié +: \.(text|data|bss|noinit|ccm)' "$J/7.1-cmp-R33-$p.txt"
done
for s in embos freertos; do
  python3 scripts/oracle/comparer-oracle.py $O/env-36-debian/nucleo-f429zi-$s $O/env-36-debian/nucleo-f439zi-$s > "$J/7.1-f429-f439-$s.txt" 2>&1; echo "f429→f439 $s=$? hors_debug=$(norm $J/7.1-f429-f439-$s.txt | wc -l)"
done
```

Attendu :
- mklepton : empreintes identiques à `env-33-debian` et à `env-35-apres` (50 lignes).
- `comparer_R33-1` des **12 presets hors F4** : **0**.
- `comparer_R33-1` des **4 presets F4** : **1**, et la liste normalisée **identique** à
  `attendu/<preset>.noms.txt` (172 lignes en embOS, 169 en FreeRTOS : 89 symboles retirés — SPL,
  `eth.c`, `dev_stm32f4xx_eth.c` —, 64 (embOS) ou 60 (FreeRTOS) ajoutés — HAL GPIO et ETH,
  `dev_stm32f4xx_eth_x_*`, tick HAL, aides USART/DMA —, 16 modifiés ; sections `.text`, `.data`,
  `.bss`, et `.noinit` en FreeRTOS). Sens des deltas au Mac (`attendu/comparaisons-mac/`) :
  `.text` +1340 (embOS) / +508 (FreeRTOS), `.data` +60, `.bss` −1264, `.noinit` 4 → 0 (FreeRTOS) ;
  `.ccm_bss` inchangée. Les valeurs Debian sont relevées ; un delta d'un autre signe, ou `.ccm_bss`
  changée : écart à exposer. Toute ligne de `7.1-<preset>.noms.diff` : écart à exposer (extrait),
  pas à corriger.
- `comparer_Mac` : informatif (chaînes différentes ; 1 attendu partout).
- `f429→f439` : code 1, `hors_debug=0` (depuis ENV-35, le BSP F439 compile en `STM32F439xx` :
  seules des sections `.debug_*` diffèrent ; au Mac, 3 en embOS, 2 en FreeRTOS).

## 8. Compilation à blanc de la HAL F4 (C4)

```bash
cd "$T"
scripts/tiers/compiler-hal-f4-a-blanc.sh "$R" "$J/8-hal-blanc" > "$J/8-hal-blanc.log" 2>&1; echo "code=$?" >> "$J/8-hal-blanc.log"
cat "$J/8-hal-blanc/resume.txt"; cat "$J"/8-hal-blanc/*/echecs.txt 2>/dev/null
mkdir -p $O/env-36-debian/compilation-a-blanc && cp "$J/8-hal-blanc/resume.txt" $O/env-36-debian/compilation-a-blanc/
cp "$J"/8-hal-blanc/STM32F429xx-v330/stm32f4xx_ll_usb.log $O/env-36-debian/compilation-a-blanc/STM32F429xx-v330-stm32f4xx_ll_usb.log 2>/dev/null
find "$R/trunk" -type f ! -name .scion.grafted.list | wc -l
```
Attendu (Mac : `rapports/env-34-hal-f4/compilation-a-blanc/resume.txt`) : code 1 (l'ordre `v330`
échoue par construction) ; 90 sources par ligne ; lignes `cmsis5` (STM32F429xx, STM32F439xx) :
**0 en échec** ; lignes `v330` : **1 en échec, `stm32f4xx_ll_usb`** (`__UNALIGNED_UINT32_READ`,
`__UNALIGNED_UINT32_WRITE` non déclarés), comme au Mac ; `core_cm4.h` retenu : V3.30 pour `v330`,
`cmsis-5/CMSIS/Core/Include` pour `cmsis5` ; aucun fichier régulier ajouté au trunk. Nombre
d'avertissements : 0 au Mac ; tout autre nombre est relevé (fichiers, premières lignes), sans
arrêt.

## 9. Fichiers générés par lepton (C5)

### 9.1 Rootstock neuf `$R` contre le rootstock neuf de R33-1

```bash
lepton check -C "$R" > "$J/9.1-check-R.log" 2>&1; echo "code=$?" >> "$J/9.1-check-R.log"
lepton generate -C "$R" > "$J/9.1-generate-R.log" 2>&1; echo "code=$?" >> "$J/9.1-generate-R.log"
W="$R"/original-tree.code-workspace
for k in '"request"' '"svdFile"' '"type": "lldb"' 'tests des greffons'; do echo "$k $(grep -c "$k" "$W")"; done
diff <(sed "s#$R33#<R>#g" "$J/5.1-R33.code-workspace") <(sed "s#$R#<R>#g" "$W") > "$J/9.1-espace.diff"; echo "diff=$?"; head -40 "$J/9.1-espace.diff"
```
Attendu : `check` et `generate` code 0 ; 23 `"request"`, 10 `"svdFile"`, 7 `"type": "lldb"`,
4 tâches « tests des greffons » (inchangés depuis R33-1) ; espace **identique** à celui de `$R33`
au chemin du rootstock près (`diff=0`). Une différence (par exemple série de sonde, chemin
d'outil) : la relever telle quelle, l'exposer.

### 9.2 Graine de projet existante `$P`

```bash
lepton generate -C "$P" > "$J/9.2-generate-P-apres.log" 2>&1; echo "code=$?" >> "$J/9.2-generate-P-apres.log"
lepton check -C "$P" > "$J/9.2-check-P-apres.log" 2>&1; echo "code=$?" >> "$J/9.2-check-P-apres.log"
git -C "$P"/depots/lepton-seed/env11 status --short > "$J/9.2-graine-P-apres.txt"
sha256sum "$P"/depots/lepton-seed/env11/project/scion/CMakeUserPresets.json "$P"/*.code-workspace > "$J/9.2-generes-P-apres.sha256"
diff "$J/5.1-generes-P-avant.sha256" "$J/9.2-generes-P-apres.sha256" && echo "générés P identiques"
diff "$J/5.1-graine-P-avant.txt" "$J/9.2-graine-P-apres.txt" && echo "graine P inchangée"
diff <(grep -v '^code=' "$J/5.1-check-P-avant.log") <(grep -v '^code=' "$J/9.2-check-P-apres.log") && echo "check P identique"
```
Attendu : codes 0 ; générés, graine et sortie de `check` identiques (lepton et trunk de `$P`
inchangés : contrôle de stabilité). `$P` est QEMU seul : `build/.active/compile_commands.json`
n'est pas comparé (il ne suit que le preset configuré ; les inclusions de la famille F4 n'y
figurent que pour un preset F4).

## 10. Nettoyage de la VM (C6)

<À fixer au PA-59.> Proposition : après le §9.1, relevé par la session :
```bash
du -sh "$R33" ~/env-33-journaux
```
Puis `AVANCEMENT` : l'**utilisateur** lance :
```bash
rm -rf ~/lepton-tools-dev/essais/env-33-debian ~/env-33-journaux
```
La session vérifie `ls -d ~/lepton-tools-dev/essais/env-33-debian ~/env-33-journaux 2>&1`
(absents). Conservés : `$U` (`essais/env-28-debian`, mis à jour au §6.1), `$R`
(`essais/env-36-debian`), `$P`, `$J`.

## 11. Critères et rapport

| Critère | Attendu |
| --- | --- |
| C1 Versions | `git ls-remote` conforme au §1 ; scion 0.5.4.0, `lepton 0.1.0` (scion accepté), sans réinstallation ; chaîne APT relevée (§5) |
| C2 `graft-update` et rootstock | §6.1 : `$U` code 0, 0 conflit, noyau, famille F4, BSP F429 et F439 avancés ; ajouts (215) et retraits (194) = attendu ; aucun lien sous `cubemx_hal_driver/` ; 201 liens `hal_driver/`, 7 `Device/ST/STM32F4xx/` ; 3978 liens, 0 cassé, 0 régulier ; §6.2 : rootstock neuf, 14 entrées, 3978 liens, 0 cassé, 0 régulier, liste identique à `$U` |
| C3 Constructions | host ctest 7/7, mklepton = `env-33-debian` = `env-35-apres` ; 16 presets construits ; QEMU fumée et banc 20/20, 16/16, 19/19 ; `comparer_R33-1` : 12 presets 0, 4 presets F4 1 avec écarts normalisés = Mac ; `f429→f439` hors `.debug_*` 0 |
| C4 Compilation à blanc | `cmsis5` 0 échec (2 puces) ; `v330` 1 échec `stm32f4xx_ll_usb` (2 puces), comme au Mac ; trunk sans fichier régulier |
| C5 Fichiers générés | `$R` : `check`, `generate` 0, espace = `$R33` au chemin près ; `$P` : `check`, `generate` 0, générés, graine et `check` identiques |
| C6 Nettoyage | <selon PA-59> |

Rapport `doc/devenv/rapports/env-36-debian.md` sur `devenv/env-36-debian`, contenant : hôte et
versions (§5), table des critères, table des presets (construction, fumée, banc KAL, symboles
R36-1 / R33-1 / Mac `env-35-apres`, `comparer_R33-1`, `comparer_Mac`), deltas de sections des
4 presets F4 (Debian contre Mac), écarts et constats, journal des messages §2bis (ID, date,
résumé), non fait. Commit du rapport et de `oracles/env-36-debian/` (`compilation-a-blanc/`
compris), puis `QUESTION` à l'utilisateur pour le push (PA-P), puis `FIN-*`.
