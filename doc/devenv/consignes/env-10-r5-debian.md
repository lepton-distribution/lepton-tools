# Consigne — session Claude Code sur la VM Debian — reprise 5 (ENV-10 D3, D4, O12 ; noyau O9)

Fichier autonome : il suffit, avec `ORCHESTRATION.md` §2, à conduire la session VM. Il prime sur la
procédure générale de la skill `devenv-session` là où il la restreint (§7).
Rédigé le 2026-10-16 par la session Mac (reprise 5), commit sur `devenv/env-10-r5`.

## 1. Objet

Valider sur Debian x86_64 les corrections de la reprise 5 (`doc/devenv/rapports/env-10-r5.md`) :

| ID | Correction | Attendu sur Debian |
| --- | --- | --- |
| D3 | `install-debian.sh` installe `libxml2-utils` | `xmllint` présent ; `lepton check` valide le XML mklepton sans avertissement ; tests `test_milestone1.py` non ignorés |
| D4 | `install-debian.sh` installe `clangd` | `lepton generate` écrit `clangd.path` sans avertissement |
| O12 | `install-vscodium.sh` compare le paquet lepton installé aux sources | 1re exécution : lepton réinstallé ; 2e : 0 changement |
| O9 | `lepton generate` retient un gdb avec Python ; `gdbinit-lepton` gardé | `gdbPath` = `gdb-multiarch` ; `lepton-stacks` définie sous `gdb-multiarch` |

O6 (défaut CMake de `LEPTON_EMBOS_ROOT`) est validé sur le Mac seulement (embOS hors git).
Produire `doc/devenv/rapports/env-10-r5-debian.md` sur la branche `devenv/env-10-r5-debian`. La
session VM ne développe pas : elle exécute, constate et rapporte.

État de la VM attendu : celui de la fin d'ENV-11 (`rapports/env-11-debian.md`) : VSCodium
1.135.06055, extensions épinglées, scion 0.5.1.0, lepton 0.1.0 (depuis 55a55bc), rootstock d'essai
`~/lepton-tools-dev/essais/env-11/qemu` (graine `env11`, FreeRTOS, an386), pas de `xmllint`, pas de
clangd LLVM.

## 2. Ce que la session VM peut faire, et ne fait pas

| Autorisé | Interdit |
| --- | --- |
| Mettre à jour les clones du §3 (`fetch`, `switch`, `pull --ff-only`, `fetch --tags`) | Modifier `DEVENV-STATUS.md`, `ORCHESTRATION.md`, `SPECIFICATION.md`, une passation `handoff/*.md` |
| Créer `devenv/env-10-r5-debian` dans lepton-tools | Commiter sur `devenv/env-10-r5` ou `main` |
| Écrire `doc/devenv/rapports/env-10-r5-debian.md` | Toucher au clone noyau ou à seed.scions de `~/lepton-tools-dev` (lecture seule) |
| `lepton check` et `lepton generate` dans `~/lepton-tools-dev/essais/env-11/qemu` | Modifier un clone du rootstock d'essai |
| Créer un venv de test sous `~/lepton-tools-dev/venv-test` (§5.5) | Retirer un paquet, VSCodium, une extension ; modifier `~/.bashrc`, `~/.profile` sans accord |
| Corriger un script ou lepton **seulement** pour un défaut propre à Debian, après accord de l'utilisateur, commit séparé | Corriger un défaut commun à tous les hôtes : le consigner pour la session Mac |
| `git push origin devenv/env-10-r5-debian` **après accord explicite** (PA-P) | Pousser toute autre branche ou tag |

Tout écart au plan, toute erreur non prévue : s'arrêter, exposer, attendre l'utilisateur.

## 3. Dépôts

| Dépôt | Référence attendue | Emplacement |
| --- | --- | --- |
| `lepton-tools` | branche `devenv/env-10-r5` (tête : le commit qui ajoute ce fichier, ou plus récent) | `~/lepton-tools-dev/lepton-tools` |
| `lepton-original-tree.scions` (clone noyau, porte `install-debian.sh`) | branche `devenv/env-10-r5`, tête ed46f71 | `~/lepton-tools-dev/lepton-noyau` |
| `seed.scions` | tag `0.5.1.1` (f1d1f3c) | `~/lepton-tools-dev/seed.scions` |

```bash
cd ~/lepton-tools-dev
git -C lepton-tools fetch origin && git -C lepton-tools switch devenv/env-10-r5 && git -C lepton-tools pull --ff-only
git -C lepton-noyau fetch origin && git -C lepton-noyau switch devenv/env-10-r5 && git -C lepton-noyau pull --ff-only
git -C seed.scions fetch --tags origin && git -C seed.scions rev-parse 0.5.1.1^{commit}     # f1d1f3c…
git -C lepton-tools log --oneline -1; git -C lepton-noyau log --oneline -1                  # ed46f71
```

## 4. Vérifications préalables (lecture seule)

Consigner dans le rapport (§1) :

```bash
uname -sm; cat /etc/debian_version; id -un
codium --version | head -1; scion version | tail -1; lepton --version
command -v xmllint clangd gdb-multiarch arm-none-eabi-gdb || true
gdb-multiarch --version | head -1
gdb-multiarch -nx -batch -ex "python print('ok')"                     # ok attendu (gdb Debian avec Python)
"$(pipx environment --value PIPX_LOCAL_VENVS)"/lepton/bin/python -c 'import lepton, os; print(os.path.dirname(lepton.__file__))'
df -h /tmp ~ | tail -2
ls ~/lepton-tools-dev/essais/env-11/qemu/trunk >/dev/null && echo "rootstock d'essai présent"
```

Arrêts : `gdb-multiarch` sans Python ; rootstock d'essai absent ; un clone ne suit pas sa branche.

## 5. Scénario

Journaux : `~/env-10-r5-journaux/<étape>.log` (une commande par fichier, code de retour en dernière
ligne). Variables :

```bash
mkdir -p ~/env-10-r5-journaux
R=~/lepton-tools-dev/essais/env-11/qemu
J=~/env-10-r5-journaux
```

### 5.1 Installation n° 1 (D3, D4, O12 ; INS-4)
`install-vscodium.sh` appelle `sudo apt-get` par `install-debian.sh` : **l'utilisateur** lance la
commande (sudo avec mot de passe), Claude lit le journal.

```bash
cd ~/lepton-tools-dev/lepton-tools
bash scripts/install-vscodium.sh --lepton-clone ~/lepton-tools-dev/lepton-noyau \
  --seed-scions ~/lepton-tools-dev/seed.scions 2>&1 | tee ~/env-10-r5-journaux/5.1-install-1.log
echo "code=${PIPESTATUS[0]}" | tee -a ~/env-10-r5-journaux/5.1-install-1.log
```
Attendu : code 0 ; section « Environnement de développement (xmllint, clangd) » d'`install-debian.sh`
installant `libxml2-utils` et `clangd` ; scion 0.5.1.0 → 0.5.1.1 ; « lepton 0.1.0 : paquet installé
différent des sources (ou hors pipx) : réinstallation » ; récapitulatif d'`install-debian.sh` avec
les versions de `xmllint` et `clangd` (à relever) ; `changements` ≥ 1.

### 5.2 Installation n° 2 (INS-4, O12)
Même commande, journal `5.2-install-2.log`. Attendu : code 0, **`changements 0`**, « lepton 0.1.0 :
déjà installé, identique aux sources ».

### 5.3 D3 : `lepton check` valide le XML
```bash
xmllint --version 2>&1 | head -1
lepton check -C "$R" 2>&1 | tee $J/5.3-check.log; echo "code=${PIPESTATUS[0]}" | tee -a $J/5.3-check.log
```
Attendu : code 0, XML mklepton validé, **aucun** avertissement « xmllint absent ».

### 5.4 D4 et O9 : `lepton generate`
```bash
cp "$R"/env11.code-workspace $J/env11.code-workspace.avant
lepton generate -C "$R" 2>&1 | tee $J/5.4-generate.log; echo "code=${PIPESTATUS[0]}" | tee -a $J/5.4-generate.log
grep -n -E '"clangd.path"|"gdbPath"|"cortex-debug.gdbPath"|"cortex-debug.armToolchainPath"' "$R"/env11.code-workspace
diff $J/env11.code-workspace.avant "$R"/env11.code-workspace > $J/5.4-diff.log; echo "diff=$?"
lepton generate -C "$R" >/dev/null 2>&1 && cp "$R"/env11.code-workspace $J/w2 && lepton generate -C "$R" >/dev/null 2>&1 \
  && diff -q $J/w2 "$R"/env11.code-workspace && echo "idempotent"
```
Attendu : code 0 ; **aucun** avertissement « aucun clangd LLVM » ni « aucun gdb avec Python » ;
`clangd.path` = `/usr/bin/clangd` (ou `clangd-19`) ; `gdbPath` = `/usr/bin/gdb-multiarch` ;
`armToolchainPath` = `/usr/bin` (dossier d'`arm-none-eabi-gcc`) ; diff limité à ces clés, aux
schémas et à la tâche « lepton : vérifier » (ajoutée en reprise 4) ; idempotent.

### 5.5 O9 : `gdbinit-lepton` sous `gdb-multiarch`
```bash
grep -v '^target extended-remote' ~/lepton-tools-dev/lepton-noyau/scion/debug/gdbinit-lepton > $J/gdbinit-sans-cible.gdb
gdb-multiarch -nx -batch -x $J/gdbinit-sans-cible.gdb -ex 'help lepton-stacks' -ex 'help lepton-fault' 2>&1 | tee $J/5.5-gdb.log
```
Attendu : aucune ligne « gdb sans Python » ; l'aide de `lepton-stacks` est la docstring Python
(« Par tâche embOS : taille de pile, … »).

### 5.6 D3 : tests de lepton avec `xmllint`
`/tmp` de la VM est petit (O13) : `TMPDIR` dans le home.
```bash
mkdir -p ~/tmp-tests; export TMPDIR=~/tmp-tests
[ -x ~/lepton-tools-dev/venv-test/bin/python ] || python3 -m venv ~/lepton-tools-dev/venv-test
~/lepton-tools-dev/venv-test/bin/pip install -q -e "$HOME/lepton-tools-dev/lepton-tools[test]"
cd ~/lepton-tools-dev/lepton-tools && ~/lepton-tools-dev/venv-test/bin/python -m pytest -q -rs 2>&1 | tail -15 | tee $J/5.6-pytest.log
rm -rf ~/tmp-tests; unset TMPDIR
```
Attendu : 139 tests verts ; aucun test ignoré pour « xmllint absent » (le Mac : 139 verts).
Si `pip install` exige un accès réseau refusé : le noter et passer.

### 5.7 Fin de scénario
```bash
find "$R/trunk" -type f ! -name .scion.grafted.list                  # vide attendu
find -L "$R/trunk" -type l                                           # vide attendu
```

## 6. En cas d'échec
S'arrêter. Relever la commande, le message, le code, le composant (script du noyau, install-vscodium,
lepton, paquet Debian). Comparer au rapport Mac (`env-10-r5.md` §3). Défaut propre à Debian :
proposer une correction à l'utilisateur, l'appliquer seulement avec son accord, commit séparé
`devenv(env-10-r5-debian): …`, puis rejouer l'étape. Défaut commun : le consigner (§5 du rapport)
sans corriger.

## 7. Fin de session VM (remplace la fin de session de `devenv-session`)

1. `git -C ~/lepton-tools-dev/lepton-tools switch -c devenv/env-10-r5-debian` (depuis `devenv/env-10-r5`).
2. Écrire `doc/devenv/rapports/env-10-r5-debian.md` selon le §8.
3. `git add doc/devenv/rapports/env-10-r5-debian.md && git commit -m "devenv(env-10-r5-debian): rapport de validation Debian"`.
4. Demander l'accord PA-P à l'utilisateur, puis `git push -u origin devenv/env-10-r5-debian`.
5. Ne pas écrire de passation ni toucher à `DEVENV-STATUS.md`. Résumer à l'utilisateur : étapes
   conformes ou non, commit poussé.

## 8. Plan du rapport `doc/devenv/rapports/env-10-r5-debian.md`

```markdown
# Reprise 5 — Validation Debian (D3, D4, O9, O12) — <date>

## 1. Hôte
Debian, noyau, utilisateur, versions (§4), têtes des trois clones, `lepton --version` avant / après.

## 2. Scénario
| Étape | Commande (résumé) | Résultat | Correction validée |
Une ligne par commande significative de §5.1 à §5.7 (code, extrait utile du journal).

## 3. Versions relevées
xmllint (libxml2-utils), clangd, scion, gdb-multiarch.

## 4. Corrections propres à Debian
Aucune, ou : commit, défaut, correction, accord de l'utilisateur.

## 5. Défauts et observations
Défauts communs (pour la session Mac), autres observations ; questions pour l'utilisateur.
```
