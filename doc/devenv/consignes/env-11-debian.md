# Consigne — session Claude Code sur la VM Debian — ENV-11 (validation de bout en bout, Debian)

Fichier autonome : il suffit, avec `ORCHESTRATION.md` §2, à conduire la session VM. Il prime sur la
procédure générale de la skill `devenv-session` là où il la restreint (§7).
Rédigé le 2026-10-15 par la session Mac (ENV-11 S3), commit sur `devenv/env-11`.

## 1. Objet

Rejouer sur Debian x86_64 les étapes 2.1 à 2.4, 2.8 et 2.9 (ligne de commande) du scénario
d'ENV-11 (`etapes/ENV-11-validation.md` §2-§3) : installation sans effet, graine neuve sans
application, construction, QEMU, banc KAL, application ajoutée sans édition CMake, retrait,
reproductibilité. Produire `doc/devenv/rapports/env-11-debian.md` sur la branche
`devenv/env-11-debian`. La session VM ne développe pas : elle exécute, constate et rapporte.

Référence Mac Intel (mêmes commandes) : `doc/devenv/rapports/env-11-mac.md` §2.
État de la VM attendu : celui de la fin d'ENV-10 (`rapports/env-10-debian.md`, passage n° 3) :
VSCodium 1.135.06055, extensions épinglées, scion 0.5.1.0, lepton 0.1.0 (version d'ENV-10), chaîne
APT (arm-none-eabi-gcc 14.2.1, cmake 3.31.6, ninja 1.12.1, QEMU 10.0.13).

## 2. Ce que la session VM peut faire, et ne fait pas

| Autorisé | Interdit |
| --- | --- |
| Mettre à jour les clones du §3 (`fetch`, `switch`, `pull --ff-only`) | Modifier `DEVENV-STATUS.md`, `ORCHESTRATION.md`, `SPECIFICATION.md`, une passation `handoff/*.md` |
| Créer `devenv/env-11-debian` dans lepton-tools | Commiter sur `devenv/env-11` ou `main` |
| Écrire `doc/devenv/rapports/env-11-debian.md` | Toucher au clone noyau ou à seed.scions de `~/lepton-tools-dev` (lecture seule) |
| Créer le rootstock d'essai `~/lepton-tools-dev/essais/env-11/qemu` et y modifier les clones d'essai (application `salut`, XML du clone noyau d'essai) | Pousser un clone d'essai, modifier un dépôt GitHub autre que par la branche du §7 |
| `pipx install --force ~/lepton-tools-dev/lepton-tools` (§5.2, décision de l'utilisateur) | Retirer un paquet, VSCodium, une extension ; modifier `~/.bashrc`, `~/.profile` sans accord |
| Corriger un script ou lepton **seulement** pour un défaut propre à Debian, après accord de l'utilisateur, commit séparé | Corriger un défaut commun à tous les hôtes : le consigner pour la session Mac |
| `git push origin devenv/env-11-debian` **après accord explicite** (PA-P) | Pousser toute autre branche ou tag |

Tout écart au plan, toute erreur non prévue : s'arrêter, exposer, attendre l'utilisateur.

## 3. Dépôts

Clones de la VM (déjà présents depuis ENV-10) :

| Dépôt | Référence attendue | Emplacement |
| --- | --- | --- |
| `lepton-tools` | branche `devenv/env-11` (tête : le commit qui ajoute ce fichier, ou plus récent) | `~/lepton-tools-dev/lepton-tools` |
| `lepton-original-tree.scions` (clone noyau, porte `install-debian.sh`) | branche `devenv/env-11`, tête a572f00 | `~/lepton-tools-dev/lepton-noyau` |
| `seed.scions` | tag `0.5.1.0` (79f4f96) | `~/lepton-tools-dev/seed.scions` |

```bash
cd ~/lepton-tools-dev
git -C lepton-tools fetch origin && git -C lepton-tools switch devenv/env-11 && git -C lepton-tools pull --ff-only
git -C lepton-noyau fetch origin && git -C lepton-noyau switch devenv/env-11 && git -C lepton-noyau pull --ff-only
git -C lepton-tools log --oneline -1; git -C lepton-noyau log --oneline -1   # a572f00
git -C seed.scions describe --tags                                          # 0.5.1.0
```

Greffons clonés par `lepton seed new` (§5.3), par SSH, branche `master` :

| Greffon (nom du manifeste) | URL d'origine | `master` attendu |
| --- | --- | --- |
| `lepton-noyau` | `ssh://git@github.com/lepton-distribution/lepton-original-tree.scions.git` | 1dde0af |
| `qemu-mps2` (famille) | `ssh://git@github.com/lepton-distribution/lepton-famille-qemu-mps2.git` | 3954357 |
| `qemu-mps2-an386` (BSP) | `ssh://git@github.com/lepton-distribution/lepton-bsp-qemu-mps2-an386.git` | 046779e |

Forme `ssh://` obligatoire : `lepton` ne reconnaît une URL que si elle a un hôte (`git@github.com:…`
serait pris pour un chemin local). Vérification préalable :
`git ls-remote ssh://git@github.com/lepton-distribution/<dépôt>.git master` pour chacun.

## 4. Vérifications préalables (lecture seule)

Consigner dans le rapport (§1) :

```bash
uname -sm; cat /etc/debian_version; id -un
command -v codium scion lepton cmake ninja qemu-system-arm arm-none-eabi-gcc python3
codium --version | head -1; scion version | tail -1; lepton --version
arm-none-eabi-gcc --version | head -1; cmake --version | head -1; ninja --version; qemu-system-arm --version | head -1
echo "LEPTON_EMBOS_ROOT=${LEPTON_EMBOS_ROOT-<absente>}"; echo "SOURCE_DATE_EPOCH=${SOURCE_DATE_EPOCH-<absente>}"
ls ~/lepton-tools-dev/essais/env-11 2>/dev/null || echo "rootstock d'essai absent (attendu)"
df -h /tmp ~ | tail -2
```

Arrêts : rootstock d'essai déjà présent et non vide ; un outil absent ; `git ls-remote` en échec.

## 5. Scénario

Journaux : `~/env-11-journaux/<étape>.log` (une commande par fichier, code de retour en dernière
ligne, comme en ENV-10). Variables :

```bash
mkdir -p ~/env-11-journaux ~/lepton-tools-dev/essais/env-11
R=~/lepton-tools-dev/essais/env-11/qemu
GH=ssh://git@github.com/lepton-distribution
```

### 5.1 Étape 2.1 — installation sans effet (INS-4)
`install-vscodium.sh` appelle `sudo apt-get` par `install-debian.sh` : **l'utilisateur** lance les
deux commandes (sudo avec mot de passe, `rapports/env-10-debian.md` §1), Claude lit les journaux.

```bash
cd ~/lepton-tools-dev/lepton-tools
bash scripts/install-vscodium.sh --lepton-clone ~/lepton-tools-dev/lepton-noyau \
  --seed-scions ~/lepton-tools-dev/seed.scions 2>&1 | tee ~/env-11-journaux/2.1-install.log
echo "code=${PIPESTATUS[0]}" | tee -a ~/env-11-journaux/2.1-install.log
```
Attendu : code 0, `changements 0`. Point d'attention : `install-debian.sh` du clone noyau
`devenv/env-11` porte `SCION_REF` 0.5.1.0 (a572f00) ; scion déjà en 0.5.1.0 → aucun changement.

### 5.2 lepton depuis `devenv/env-11` (décision de l'utilisateur, observation O12)
lepton 0.1.0 installé en ENV-10 ne contient pas les corrections N2 (338ff5b) et N3 (7d191aa) ;
le script ne le réinstalle pas (même numéro de version : c'est O12, à constater).

```bash
lepton --version                                     # lepton 0.1.0 (avant)
pipx install --force ~/lepton-tools-dev/lepton-tools 2>&1 | tee ~/env-11-journaux/5.2-pipx.log
pipx runpip lepton show lepton | sed -n '1,3p'
```

### 5.3 Étape 2.2 — graine neuve sans application (GRA-1, GRA-2, GRA-3, GRA-6)
```bash
lepton seed new env11 -C "$R" --bsp qemu-mps2-an386 --backend freertos \
  --mkconf sys/user/tauon-basic/etc/mkconf_tauon_basic_qemu_mps2.xml \
  --origin "lepton-noyau=$GH/lepton-original-tree.scions.git@master" \
  --origin "qemu-mps2=$GH/lepton-famille-qemu-mps2.git@master" \
  --origin "qemu-mps2-an386=$GH/lepton-bsp-qemu-mps2-an386.git@master"
lepton check -C "$R"
lepton seed status -C "$R"
for d in "$R"/depots/lepton/*/master; do echo "$d $(git -C "$d" branch --show-current) $(git -C "$d" log --oneline -1)"; done
lepton seed remove qemu-mps2-an386 -C "$R"; echo "code=$?"      # refus attendu, code 1 (GRA-2)
lepton seed remove lepton-noyau -C "$R"; echo "code=$?"         # refus attendu, code 1 (GRA-2)
```
Attendu : chaque clone sur `master` au commit du §3 (défaut N1 de scion sans effet ici : la
branche par défaut des dépôts GitHub est `master`) ; si un clone est sur une autre branche, le
noter (N1) et faire `git -C <clone> checkout master`.

### 5.4 Étape 2.3 — construction, QEMU, banc KAL (CFG-6, BLD-1, BLD-3, BLD-4, TST-1)
```bash
lepton generate -C "$R"
cd "$R/trunk"
cmake --list-presets
cmake --preset host && cmake --build "$R/build/host"
cmake --preset env11-debug-qemu && cmake --build "$R/build/env11-debug-qemu"
ls "$R"/build/env11-debug-qemu/lepton.{elf,bin,hex,map,occupation.txt}
find "$R/trunk" -type f ! -name .scion.grafted.list | head          # vide attendu (BLD-3)
ctest --preset env11-debug-qemu -L smoke --output-on-failure
ctest --preset env11-debug-qemu -L kal --output-on-failure           # 18/18 attendu
```

### 5.5 Étape 2.4 — application sans édition CMake (GRF-1, FIC-1, FIC-3, FIC-4, BLD-2, CFG-5)
```bash
lepton scion new --type application salut -C "$R"
cmake --build "$R/build/env11-debug-qemu"                            # salut.c.obj compilé
lepton file add -C "$R" "$R/trunk/sys/root/src/bin/salut/salut_message.c"
```
Écrire dans le **clone** (chemin affiché par `file add`, `depots/lepton-application/salut/scion/…`),
jamais par le trunk :
- `salut_message.c` :
  ```c
  /* Fichier ajouté par lepton file add (ENV-11, FIC-4). */
  const char* salut_message(void)
  {
     return "salut depuis salut_message.c";
  }
  ```
- `salut.c` : déclarer `const char* salut_message(void);` et remplacer le corps de `salut_main` par
  `printf("%s\r\n", salut_message());` (forme du rapport Mac).

Puis déclarer le binaire dans le XML **du clone noyau d'essai** (PA-9 Q5) :
`$R/depots/lepton/original/master/scion/sys/user/tauon-basic/etc/mkconf_tauon_basic_qemu_mps2.xml`
(chemin réel à vérifier par `realpath` du lien du trunk), ligne après `<bin name="pwd" …/>` :
`<bin name="salut" stack="2048" priority="100" timeslice="1" />`.

```bash
lepton check -C "$R"
cmake --build "$R/build/env11-debug-qemu"                            # « Re-running CMake », salut_message.c.obj
python3 "$R/trunk/tests/smoke_lsh.py" --machine mps2-an386 \
  --kernel "$R/build/env11-debug-qemu/lepton.elf" --expect-machine cortexM4-qemu-mps2-an386 \
  --command "ls /usr/bin" --command salut --log ~/env-11-journaux/5.5-salut-console.log
grep -n 'salut depuis salut_message.c' ~/env-11-journaux/5.5-salut-console.log
find "$R/trunk" -type f ! -name .scion.grafted.list | head          # vide attendu (FIC-3)
```

### 5.6 Étape 2.8 — retrait de l'application (GRF-4)
```bash
lepton scion remove salut -C "$R"; echo "code=$?"
find -L "$R/trunk" -type l | head                                    # aucun lien orphelin
git -C "$R/depots/lepton-application/salut" log --oneline -1         # clone intact
```
Comportement connu (O4 du rapport Mac) : la reconfiguration échoue tant que le XML déclare `salut`.
Retirer alors la ligne `<bin name="salut" …/>` du XML du clone noyau d'essai, puis :
```bash
cmake --build "$R/build/env11-debug-qemu" && ctest --preset env11-debug-qemu -L smoke
git -C "$R/depots/lepton/original/master" status --short             # propre attendu
```

### 5.7 Étape 2.9 (ligne de commande) — reproductibilité (BLD-5)
```bash
cd "$R/trunk"; export SOURCE_DATE_EPOCH=1760536800
cmake --preset env11-debug-qemu -B "$R/build/bld5-a" && cmake --build "$R/build/bld5-a"
cmake --preset env11-debug-qemu -B "$R/build/bld5-b" && cmake --build "$R/build/bld5-b"
sha256sum "$R"/build/bld5-{a,b}/lepton.{bin,hex}
unset SOURCE_DATE_EPOCH
```
Attendu : empreintes identiques entre `bld5-a` et `bld5-b`. Les relever aussi pour comparaison
avec le Mac (`lepton.bin` 25d50f61…, `lepton.hex` 7e29c21c…) : information seulement, l'égalité
n'est pas attendue (chaîne APT 14.2.1 contre Arm GNU Toolchain 14.2.Rel1).

### 5.8 Fin de scénario
```bash
find "$R/trunk" -type f ! -name .scion.grafted.list                  # vide attendu
find -L "$R/trunk" -type l                                           # vide attendu
find "$R/depots" -maxdepth 4 -name .git | while read -r g; do d=${g%/.git}; echo "$d $(git -C "$d" status --porcelain | wc -l)"; done
```
Ne pas supprimer le rootstock d'essai.

## 6. En cas d'échec
S'arrêter. Relever la commande, le message, le code, le composant (scion, lepton, CMake du greffon
noyau, BSP, chaîne Debian). Comparer à l'étape Mac correspondante (`env-11-mac.md` §2). Défaut propre
à Debian : proposer une correction à l'utilisateur, l'appliquer seulement avec son accord, commit
séparé `devenv(env-11-debian): …`, puis rejouer l'étape. Défaut commun : le consigner (§6 du
rapport) sans corriger.

## 7. Fin de session VM (remplace la fin de session de `devenv-session`)

1. `git -C ~/lepton-tools-dev/lepton-tools switch -c devenv/env-11-debian` (depuis `devenv/env-11`).
2. Écrire `doc/devenv/rapports/env-11-debian.md` selon le §8.
3. `git add doc/devenv/rapports/env-11-debian.md && git commit -m "devenv(env-11-debian): rapport de validation Debian"`.
4. Demander l'accord PA-P à l'utilisateur, puis `git push -u origin devenv/env-11-debian`.
5. Ne pas écrire de passation ni toucher à `DEVENV-STATUS.md`. Résumer à l'utilisateur : étapes
   conformes ou non, commit poussé.

## 8. Plan du rapport `doc/devenv/rapports/env-11-debian.md`

```markdown
# ENV-11 — Validation de bout en bout, hôte Debian — <date>

## 1. Hôte
Debian, noyau, utilisateur, versions (§4), têtes des trois clones, `lepton --version` avant / après §5.2.

## 2. Scénario
| Étape | Commande (résumé) | Résultat | Exigences |
Une ligne par commande significative de §5.1 à §5.8 (code, extrait utile du journal), sur le modèle
de `env-11-mac.md` §2.

## 3. Comparaison avec le Mac
Écarts de comportement étape par étape ; empreintes BLD-5 Debian / Mac (information).

## 4. Corrections propres à Debian
Aucune, ou : commit, défaut, correction, accord de l'utilisateur.

## 5. Défauts et observations
Défauts communs (pour la session Mac), constat O12 (lepton non réinstallé par le script), autres
observations ; questions pour l'utilisateur.
```
