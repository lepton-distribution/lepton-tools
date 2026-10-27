# Consigne — session Claude Code sur la VM Debian — ENV-12 (extension VSCodium, lot 6 S3)

Fichier autonome : il suffit, avec `ORCHESTRATION.md` §2 et §2bis, à conduire la session VM. Il
prime sur la procédure générale de la skill `devenv-session` là où il la restreint (§8).
Rédigé le 2026-10-27 par la session Mac (ENV-12 lot 6 S2), commit sur `devenv/env-12`.

## 1. Objet

Valider sur Debian x86_64 l'extension Lepton 0.5.1 et les évolutions de lepton d'ENV-12 (lots 1 à 6),
validées sur le Mac (`doc/devenv/rapports/env-12-lot3.md` à `env-12-lot6.md`) :

| ID | Fonction | Attendu sur Debian |
| --- | --- | --- |
| INS | `install-vscodium.sh` : pack de langue, locale, extension Lepton de `extension/dist/` | n° 1 : pack `ms-ceintl.vscode-language-pack-fr@1.131.0`, `"locale": "fr"`, `lepton-distribution.lepton@0.5.1`, lepton réinstallé ; n° 2 : `changements 0` |
| O5 | XML mklepton du projet dans la graine (`seed mkconf import`) | graine `env11` migrée, `check` sans avertissement O5 |
| F1 | Palette (IDE-6) | 18 commandes « Lepton : … » en français |
| F2 | Regreffe automatique (FIC-1), observateur sous inotify | fichier créé / supprimé dans un clone : lien ajouté / retiré du trunk |
| F3 | Redirection d'une création faite dans le trunk (FIC-3) | fichier déplacé dans le clone, lien à sa place |
| L3-4 | Lien supprimé du trunk | notification « Supprimer du greffon » / « Restaurer le lien » |
| F4 | Relance de clangd (O10) | « clangd restarted » au changement de preset |
| F5 | Erreurs à la saisie (CFG-7, `check --stdin`) | erreur `lepton` dans *Problèmes* sans enregistrer |
| F6 | Vue Architecture (IDE-1, `seed tree`) | cohérente avec `lepton seed status` |
| F7 | Configurations (palette) et L6-5 | preset ajouté / retiré visible dans CMake Tools **sans recharger la fenêtre** |
| F8 | Sources de l'arrêt par le trunk, sous `gdb-multiarch` (QEMU) ; L6-6 | onglet sous `trunk/` dès la **première** session de la fenêtre |
| L6-7 | Matcher gcc des tâches | aucun « référence de problemMatcher non valide : $gcc » |

Produire `doc/devenv/rapports/env-12-debian.md` sur la branche `devenv/env-12-debian`. La session VM
ne développe pas : elle exécute, constate et rapporte. Pas de carte sur la VM (F8 : QEMU seulement).

Mode mixte : les actions dans VSCodium sont faites par **l'utilisateur** sur l'écran de la VM, une par
une à la demande de la session VM ; la session VM contrôle chaque résultat en ligne de commande
(`lepton seed status`, `find`, `git status`, journaux du canal « Lepton » sous
`~/.config/VSCodium/logs/`).

État de la VM attendu : celui de la reprise 5 (`rapports/env-10-r5-debian.md`) : VSCodium
1.135.06055, extensions épinglées sans pack de langue ni extension Lepton, scion 0.5.1.1, lepton 0.1.0
(sources de c5286be), xmllint et clangd 19 installés, rootstock d'essai
`~/lepton-tools-dev/essais/env-11/qemu` (graine `env11`, FreeRTOS, an386, non migrée O5).

## 2. Ce que la session VM peut faire, et ne fait pas

| Autorisé | Interdit |
| --- | --- |
| Mettre à jour les clones du §4 (`fetch`, `switch`, `pull --ff-only`, `fetch --tags`) | Modifier `DEVENV-STATUS.md`, `ORCHESTRATION.md`, `SPECIFICATION.md`, une passation `handoff/*.md` |
| Créer `devenv/env-12-debian` dans lepton-tools | Commiter sur `devenv/env-12` ou `main` |
| Écrire `doc/devenv/rapports/env-12-debian.md` | Toucher au clone noyau ou à seed.scions de `~/lepton-tools-dev` (lecture seule) |
| Dans `~/lepton-tools-dev/essais/env-11/qemu` : commandes lepton du §6, fichiers d'essai `essai_s3*` créés puis retirés, commit de migration O5 dans la graine | Modifier un clone de greffon autrement que par les essais du §6 ; écrire un fichier régulier dans `trunk/` |
| Créer un venv de test sous `~/lepton-tools-dev/venv-test` (§6.10) | Retirer un paquet, VSCodium, une extension ; modifier `~/.bashrc`, `~/.profile` sans accord |
| Corriger un script, lepton ou l'extension **seulement** pour un défaut propre à Debian, après accord de l'utilisateur, commit séparé | Corriger un défaut commun à tous les hôtes : le consigner pour la session Mac |
| `git push origin devenv/env-12-debian` **après accord explicite** (PA-P) | Pousser toute autre branche ou tag |

Tout écart au plan, toute erreur non prévue : s'arrêter, exposer, attendre l'utilisateur.

## 3. Communication (ORCHESTRATION §2bis)

- Session principale : la session Mac d'ENV-12 qui envoie l'ordre `R12-1` ; répondre à l'adresse
  `from` de ce message.
- ID unique de l'ordre : `R12-1`, repris tel quel par toutes les réponses
  (`[ACCUSÉ R12-1] ENV-12 — …`, `[AVANCEMENT R12-1] …`, `[QUESTION R12-1] …`, `[FIN-SUCCÈS R12-1] …`
  ou `[FIN-ÉCHEC R12-1] …`).
- `ACCUSÉ` avant toute commande : ordre reformulé en une phrase, têtes réelles des trois clones après
  `fetch` (§4), étapes prévues (§6.1 à §6.11), écarts déjà visibles.
- `AVANCEMENT` : avant §6.1 et §6.2 (sudo par l'utilisateur), avant chaque groupe d'actions dans
  VSCodium (§6.4 à §6.9), et à chaque arrêt.
- `FIN-SUCCÈS` / `FIN-ÉCHEC` : contenu du tableau de §2bis (résultat par ID du §1, commits et
  branches poussés ou non, chemin du rapport, versions relevées, écarts, ce qui n'a pas été fait).

## 4. Dépôts

| Dépôt | Référence attendue | Emplacement |
| --- | --- | --- |
| `lepton-tools` | branche `devenv/env-12` (tête : le commit qui ajoute ce fichier, ou plus récent) | `~/lepton-tools-dev/lepton-tools` |
| `lepton-original-tree.scions` (clone noyau, porte `install-debian.sh`) | branche `master`, tête 16a331b | `~/lepton-tools-dev/lepton-noyau` |
| `seed.scions` | tag `0.5.1.1` (f1d1f3c) | `~/lepton-tools-dev/seed.scions` |

```bash
cd ~/lepton-tools-dev
git -C lepton-tools fetch origin && git -C lepton-tools switch devenv/env-12 && git -C lepton-tools pull --ff-only
git -C lepton-noyau fetch origin && git -C lepton-noyau switch master && git -C lepton-noyau pull --ff-only
git -C seed.scions fetch --tags origin && git -C seed.scions rev-parse 0.5.1.1^{commit}     # f1d1f3c…
git -C lepton-tools log --oneline -1; git -C lepton-noyau log --oneline -1                  # 16a331b
ls ~/lepton-tools-dev/lepton-tools/extension/dist/                                           # lepton-0.5.1.vsix
```

## 5. Vérifications préalables (lecture seule)

Consigner dans le rapport (§1) :

```bash
uname -sm; cat /etc/debian_version; id -un
codium --version | head -1; scion version | tail -1; lepton --version
codium --list-extensions --show-versions
cat ~/.vscode-oss/argv.json 2>/dev/null | grep -n locale || echo "pas de locale"
command -v xmllint clangd gdb-multiarch qemu-system-arm
cat /proc/sys/fs/inotify/max_user_watches
df -h /tmp ~ | tail -2
R=~/lepton-tools-dev/essais/env-11/qemu
lepton seed status -C "$R"; git -C "$R"/depots/lepton-seed/env11 status --short
```

Arrêts : rootstock d'essai absent ; un clone ne suit pas sa branche ; graine `env11` modifiée non
commitée ; `max_user_watches` < 65536 (le signaler : réglage système, accord de l'utilisateur).

## 6. Scénario

Journaux : `~/env-12-journaux/<étape>.log` (une commande par fichier, code de retour en dernière
ligne). Variables :

```bash
mkdir -p ~/env-12-journaux
R=~/lepton-tools-dev/essais/env-11/qemu
J=~/env-12-journaux
```

### 6.1 Installation n° 1 (INS)
`install-vscodium.sh` appelle `sudo apt-get` par `install-debian.sh` : **l'utilisateur** lance la
commande (sudo avec mot de passe), la session VM lit le journal.

```bash
cd ~/lepton-tools-dev/lepton-tools
bash scripts/install-vscodium.sh --lepton-clone ~/lepton-tools-dev/lepton-noyau \
  --seed-scions ~/lepton-tools-dev/seed.scions 2>&1 | tee ~/env-12-journaux/6.1-install-1.log
echo "code=${PIPESTATUS[0]}" | tee -a ~/env-12-journaux/6.1-install-1.log
```
Attendu : code 0 ; `ms-ceintl.vscode-language-pack-fr@1.131.0` installé ; `locale : (absente) → 'fr'`
dans `~/.vscode-oss/argv.json` ; « Extension Lepton … : (absente) → 0.5.1 » puis
`codium --install-extension …/extension/dist/lepton-0.5.1.vsix` ; « lepton 0.1.0 : paquet installé
différent des sources … : réinstallation » ; `changements` ≥ 3.

### 6.2 Installation n° 2
Même commande, journal `6.2-install-2.log`. Attendu : code 0, **`changements 0`**.

### 6.3 Migration O5 de la graine, puis contrôles en ligne de commande
```bash
lepton check -C "$R" 2>&1 | tee $J/6.3-check-avant.log                    # avertissement O5 attendu
lepton seed mkconf import sys/user/tauon-basic/etc/mkconf_tauon_basic_qemu_mps2.xml -C "$R" 2>&1 | tee $J/6.3-import.log
lepton generate -C "$R" 2>&1 | tee $J/6.3-generate.log
git -C "$R"/depots/lepton-seed/env11 add -A && git -C "$R"/depots/lepton-seed/env11 commit -qm \
  "XML mklepton du projet dans la graine (lepton seed mkconf import, O5) ; presets régénérés"
lepton check -C "$R" 2>&1 | tee $J/6.3-check-apres.log; echo "code=${PIPESTATUS[0]}" | tee -a $J/6.3-check-apres.log
lepton seed status -C "$R" | grep configurations
lepton seed tree --json -C "$R" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["preset"], d["source"], [e["name"] for e in d["executables"]])'
G="$R"/depots/lepton/original/master/scion/sys/root/src/lepton-greffon.json
sed 's/"noyau"/"xyz"/' "$G" | lepton check --json --stdin "$G" -C "$R" | python3 -m json.tool | head -20
grep -c '\$gcc' "$R"/env11.code-workspace; grep -c 'lepton-gcc' "$R"/env11.code-workspace
```
Attendu : import code 0 (XML et `.boot`, `.init` copiés dans `project/scion/sys/user/env11/etc/`) ;
check après : code 0, sans avertissement O5 ; `configurations : debug-qemu (Debug, qemu)` (et
`release-qemu` si présente) ; `seed tree` : preset et exécutifs `lepton`, `kal_bench` (source `codemodel` si
un preset est configuré, sinon `manifests`) ; `check --stdin` : une anomalie `/type` située (ligne,
colonne), fichier non modifié sur disque ; `$gcc` : 0, `lepton-gcc` : ≥ 2.

### 6.4 VSCodium : ouverture, F1, F6 (utilisateur)
Ouvrir `~/lepton-tools-dev/essais/env-11/qemu/env11.code-workspace` (interface en français).
- F1 : palette, `Lepton :` → 18 commandes ; « Lepton : état de la graine » → canal « Lepton ».
- F6 : vue Lepton › Architecture : exécutif `lepton · env11-debug-qemu`, « Greffons de la graine » :
  5 entrées, branches et commits identiques à `lepton seed status -C "$R"`.

### 6.5 F2, F3, L3-4 sous inotify
Clone du BSP : `B="$R"/depots/lepton/bsp-qemu-mps2-an386/master/scion/sys/root/src/kernel/dev/bsp/qemu-mps2-an386`,
trunk : `T="$R"/trunk/sys/root/src/kernel/dev/bsp/qemu-mps2-an386`.
- F2 (terminal intégré de VSCodium ; l'explorateur masque `scion/` des dossiers « git · … ») :
  `touch "$B"/essai_s3.c`, attendre 2 s → `ls -l "$T"/essai_s3.c` lien ; `rm "$B"/essai_s3.c`, 2 s →
  lien absent.
- F3 : explorateur, dossier « trunk », `sys/root/src/kernel/dev/bsp/qemu-mps2-an386/`, Nouveau fichier
  `essai_s3_trunk.c` → `"$B"/essai_s3_trunk.c` fichier régulier, `"$T"/essai_s3_trunk.c` lien.
- L3-4 : supprimer le lien `essai_s3_trunk.c` du trunk dans l'explorateur → notification ; choisir
  « Supprimer du greffon » → absent du clone et du trunk.
- Contrôle : `find "$R"/trunk -type f ! -name .scion.grafted.list` vide ; `git -C "$R"/depots/lepton/bsp-qemu-mps2-an386/master status --short` vide.

### 6.6 F5 (CFG-7)
- `trunk/sys/root/src/kernel/dev/bsp/qemu-mps2-an386/lepton-greffon.json` : valeur de `"type"` →
  `"xyz"` sans enregistrer → erreur `lepton` dans *Problèmes* ; annuler → disparaît.
- `trunk/sys/user/env11/etc/mkconf_env11.xml` : `<inconnu/>` après `<mklepton …>`, enregistrer →
  erreur dans *Problèmes* ; annuler, enregistrer → disparaît ; `git -C "$R"/depots/lepton-seed/env11 status --short` vide.

### 6.7 F4 et F7 (L6-5)
- F4 : preset de configuration CMake Tools `env11-debug-qemu` → `env11-release-qemu` (si présent)
  puis retour → canal « Lepton » : « … compile_commands.json changed: clangd restarted ».
- F7 : « Lepton : ajouter une configuration à la graine » `essai-s3`, `MinSizeRel`, `qemu` → sans
  recharger, « CMake: Select Configure Preset » liste `env11 — essai-s3 …` ; « Lepton : retirer une
  configuration de la graine » `essai-s3` → sans recharger, absent de la liste.
- Contrôle : graine identique à `HEAD` ; supprimer `"$R"/build/env11-essai-s3/` s'il ne contient que
  `.cmake/api/v1/query/client-lepton/query.json`.
- F7 : clic droit sur `trunk/sys/user/tauon-basic/etc/mkconf_tauon_basic_qemu_mps2.xml` → « Lepton :
  importer un XML mklepton de référence dans la graine » → refus « déjà fourni par le greffon du projet ».

### 6.8 L6-7 et F8 sous `gdb-multiarch` (QEMU), première session de la fenêtre
- Quitter VSCodium, le rouvrir sur l'espace (fenêtre neuve).
- Ouvrir par le trunk `sys/root/src/kernel/dev/bsp/qemu-mps2-an386/qemu_mps2_board.c`, point d'arrêt
  ligne 48 (`if(qemu_mps2_uart_irq_users++ > 0)`).
- Lancer aussitôt « Déboguer env11-debug-qemu (QEMU mps2-an386) » : construction sans message
  « référence de problemMatcher non valide : $gcc » ; arrêt sur `main` puis, après Continuer, ligne
  48 : onglets **sous `…/qemu/trunk/…`** dès cette première session ; cadres de la pile sous `trunk/`.
- Canal « Lepton » : « Session de débogage … : sources affichées par le trunk (5 greffon(s)) ».
- Relever `gdbPath` de la configuration de lancement (`gdb-multiarch` attendu).

### 6.9 Témoin F8
Réglage utilisateur `lepton.debug.trunkPaths: false`, relancer la session : onglet de l'arrêt sous
`depots/` (R3 reproduit). Remettre le réglage à `true` (ou le retirer).

### 6.10 Tests
`/tmp` de la VM est petit (O13) : `TMPDIR` dans le home.
```bash
mkdir -p ~/tmp-tests; export TMPDIR=~/tmp-tests
[ -x ~/lepton-tools-dev/venv-test/bin/python ] || python3 -m venv ~/lepton-tools-dev/venv-test
~/lepton-tools-dev/venv-test/bin/pip install -q -e "$HOME/lepton-tools-dev/lepton-tools[test]"
cd ~/lepton-tools-dev/lepton-tools && ~/lepton-tools-dev/venv-test/bin/python -m pytest -q -rs 2>&1 | tail -15 | tee $J/6.10-pytest.log
rm -rf ~/tmp-tests; unset TMPDIR
```
Attendu : 191 tests verts (Mac : 191). `npm test` de l'extension n'est pas demandé (Node non
installé sur la VM ; le `.vsix` est construit sur le Mac).

### 6.11 Fin de scénario
```bash
find "$R/trunk" -type f ! -name .scion.grafted.list                  # vide attendu
find -L "$R/trunk" -type l                                           # vide attendu
for c in "$R"/depots/*/*/*/ "$R"/depots/lepton-seed/env11; do git -C "$c" status --short; done   # vide
```

## 7. En cas d'échec
S'arrêter (`AVANCEMENT` ou `FIN-ÉCHEC R12-1`). Relever la commande, le message, le code, le composant
(install-vscodium, lepton, extension, VSCodium, paquet Debian). Comparer au rapport Mac
(`env-12-lot6.md`). Défaut propre à Debian : proposer une correction à l'utilisateur, l'appliquer
seulement avec son accord, commit séparé `devenv(env-12-debian): …`, puis rejouer l'étape. Défaut
commun : le consigner (§5 du rapport) sans corriger.

## 8. Fin de session VM (remplace la fin de session de `devenv-session`)

1. `git -C ~/lepton-tools-dev/lepton-tools switch -c devenv/env-12-debian` (depuis `devenv/env-12`).
2. Écrire `doc/devenv/rapports/env-12-debian.md` selon le §9.
3. `git add doc/devenv/rapports/env-12-debian.md && git commit -m "devenv(env-12-debian): rapport de validation Debian"`.
4. Demander l'accord PA-P à l'utilisateur, puis `git push -u origin devenv/env-12-debian`.
5. Ne pas écrire de passation ni toucher à `DEVENV-STATUS.md`. Envoyer `FIN-SUCCÈS R12-1` ou
   `FIN-ÉCHEC R12-1` à la session principale.

## 9. Plan du rapport `doc/devenv/rapports/env-12-debian.md`

```markdown
# ENV-12 — Validation Debian de l'extension 0.5.1 (lot 6 S3) — <date>

## 1. Hôte
Debian, noyau, utilisateur, versions (§5), têtes des trois clones, extensions avant / après,
`max_user_watches`.

## 2. Scénario
| ID (§1) | Étape | Commande ou action (résumé) | Résultat |
Une ligne par essai de §6.1 à §6.11 (code, extrait utile du journal ou constat).

## 3. Versions relevées
Pack de langue, extension Lepton, lepton, scion, gdb-multiarch, clangd.

## 4. Corrections propres à Debian
Aucune, ou : commit, défaut, correction, accord de l'utilisateur.

## 5. Défauts et observations
Défauts communs (pour la session Mac), autres observations ; questions pour l'utilisateur.

## 6. Messages
ORDRE, ACCUSÉ, AVANCEMENT, FIN (ID, date, résumé).
```
