# ENV-64 — Extension : `lepton.path` et regreffe après `--purge` (D23, D24 ; D31 présenté)

Session du 2026-11-19, branche lepton-tools `devenv/env-64` (depuis `main` c5c9183). Extension
0.5.2 (code de `main`), VSCodium 1.135.06055, Node 22.15.0, lepton 0.1.0 (code d'ENV-63), scion
0.6.3.2.

## 1. Audit (avant correction)

### 1.1 D23 : `lepton.path`

Méthode : `env-64-extension/d23.cjs <extension/out/src/lepton.js> [<cwd>]`. Le script appelle
`resolveLepton(valeur)` puis `runLepton(exe, ["--version"], cwd)` hors de l'éditeur. Le `cwd` est
un répertoire temporaire, qui tient la place du rootstock. Relevé : `env-64-extension/d23-avant.tsv`
(`<HOME>`, `<U>`, `<CWD>` normalisés).

| Forme du réglage | Résolu | Code | Sortie |
| --- | --- | --- | --- |
| vide | `<HOME>/.local/bin/lepton` (pipx présent) | 0 | `lepton 0.1.0` |
| absolu `<HOME>/.local/bin/lepton` | tel quel | 0 | `lepton 0.1.0` |
| `~/.local/bin/lepton` | tel quel | 2 | `lepton not found: ~/.local/bin/lepton (setting lepton.path)` |
| `~<U>/.local/bin/lepton` | tel quel | 2 | idem, `~<U>/…` |
| `~inconnu64/.local/bin/lepton` | tel quel | 2 | idem |
| `~` | tel quel | 2 | idem (cherché dans le `PATH`, sans `/`) |
| `${userHome}/.local/bin/lepton` | tel quel | 2 | idem |
| `$HOME/.local/bin/lepton` | tel quel | 2 | idem |
| relatif `../…/.local/bin/lepton` | tel quel | 0 | résolu depuis le `cwd` de lepton, soit le rootstock dans l'éditeur |
| `./lepton` | tel quel | 2 | introuvable dans le `cwd` |
| nom nu `lepton` | tel quel | 0 | trouvé par le `PATH` du processus. Dans l'éditeur, c'est le `PATH` de VSCodium |

- Dans l'éditeur, le message est traduit (`runner.ts:56`, `l10n`) : « lepton introuvable : {0}
  (réglage lepton.path) ».
- Description du réglage (`package.nls.json:22`, `package.nls.fr.json:22`) : « Exécutable
  `lepton`. Vide : `~/.local/bin/lepton` (installation pipx) s'il existe, sinon `lepton` du
  `PATH`. » Elle écrit elle-même `~` pour désigner le défaut, mais une valeur saisie en `~/…` ne
  marche pas.
- Node n'a d'API que pour le dossier personnel de l'utilisateur courant (`os.homedir()`,
  `os.userInfo()`). Pour un autre utilisateur, `~<autre>` ne se résout pas sans un appel système
  externe. lepton (Python, `pwd`) le résout ; c'est un écart possible avec la forme du PA-113.
- Les variables `${…}` ne sont substituées que par les mécanismes de l'éditeur qui les prévoient
  (tâches, lancements). L'extension reçoit la valeur telle quelle par `getConfiguration().get`.
  Lu, non essayé dans l'éditeur.

### 1.2 D31 : chemin saisi ouvert par l'extension

- `commands.ts:258` (`file add`, chemin demandé par `ask`) et `commands.ts:280` (`file mv`,
  destination demandée par `showInputBox`) : `vscode.Uri.file(<saisie>)`, sans développer `~` ni
  résoudre un chemin relatif.
- Depuis ENV-63, lepton développe `~` et résout le relatif depuis son `cwd`, le rootstock
  (`runner.cwd()`). La commande réussit, puis l'extension ouvre un autre chemin : `Uri.file`
  traite `~/x` et `x` comme des chemins absolus de la racine (`/~/x`, `/x`). D'où la boîte
  d'erreur constatée en ENV-63 (`rapports/env-63-tilde.md` §5.4).
- Les autres saisies de chemin (`target`, `pathRemove`, `seed add`, `seed replace`) passent à
  lepton sans être ouvertes : non concernées.

### 1.3 D24 : regreffe automatique après disparition d'un clone

Essai :
- `essais/env-64-essai` : copie `rsync -a` d'`essais/env-11/qemu` sans `build/`, puis
  `lepton generate`. Au départ, 3059 liens, 0 cassé, 0 régulier, `check` 0.
- Greffon `env64lib` : `lepton scion new env64lib --type bibliotheque --repo
  essais/env-64-depot --no-seed --no-cmake`, puis `seed add` par
  `file://localhost<E>/env-64-depot@master`, soit 3062 liens.
- Seconde origine : `essais/env-64-depot2`, clone du premier avec un en-tête de plus.
- L'espace d'essai règle `lepton.path` sur l'enveloppe `env-64-extension/lepton-horodate.sh`, qui
  note chaque appel (début, fin, code, arguments) à la milliseconde. Journal normalisé :
  `env-64-extension/appels-avant.tsv`.
- Canal « Lepton » collé par l'utilisateur : `env-64-extension/vscodium-canal.txt`. Notifications
  relevées : `env-64-extension/vscodium-notifications.txt`.
- À la fin, l'essai est rétabli à l'état « avec env64lib » : les 6 relevés d'`etat.sh` sont
  identiques.

| Cas | Origine | Appels F2 | Code | Avertissement « regreffe automatique » |
| --- | --- | --- | --- | --- |
| U2 `seed replace` → depot2 | extension (utilisateur) | 2 × `graft --path <clone>/scion` | 1, 1 | oui (vu) |
| U3 `seed replace` → depot | extension (utilisateur) | 2 × `graft --path <clone>/scion` | 1, 1 | oui (vu) |
| U4 `seed remove --purge` (O-3) | extension (utilisateur) | 1 × `graft --path <clone>/scion` | 1 | oui (vu) |
| T2 témoin : fichier créé puis supprimé dans `scion/` | terminal | `graft --path <fichier>` à chaque fois | 0, 0 | non (regreffe ordinaire) |
| T4 `scion graft-remove --purge` | terminal | 1 × `graft --path <clone>/scion` | 1 | oui (code 1 → `report`) |
| T4b clone recréé (`scion seed-clone` + `graft --scion`) | terminal | 1 × `graft --path <clone>/scion` | 1 | oui |
| T3 clone supprimé à la main (3 liens cassés laissés) | terminal | 1 × `graft --path <clone>/scion` | 1 | oui |

Pour T4, T4b et T3, l'avertissement est déduit du code 1 (`watch.ts:128`). L'utilisateur l'a vu
pour U2 à U4.

Constats :
- **Cause.** Quand un clone entier disparaît ou réapparaît, l'observateur de l'éditeur ne signale
  que la racine observée, `<clone>/scion`. Il ne signale aucun des fichiers qu'elle contient.
  F2 transmet ce chemin, et lepton refuse par construction la racine `scion/` d'un greffon :
  `lepton/files.py:107`, `owner is None or path == owner.stem`. Le refus a donc lieu même quand
  le greffon est greffé (U2, U3 : le clone est remplacé, puis regreffé par `seed replace` lui-même).
  L'hypothèse du fichier d'étape, « le greffon n'est plus greffé », n'est vraie que pour U4.
- **Délais.** Le `Batcher` F2 regroupe sur `lepton.autoGraft.delay` (1000 ms) après le dernier
  événement. La regreffe passe ensuite par la file (`SerialQueue`), derrière les deux
  `seed status --json` lancés à la fin de la commande : le premier vient d'`onDidRunCommand` (vue
  ou `refresh`), le second d'un autre abonné.
  - U4 : `seed remove` finit à 277,777 s ; la regreffe démarre à 279,599 s, soit 1,8 s après.
  - U2 : `seed replace` finit à 101,532 s ; la première regreffe démarre à 103,582 s (2,1 s) et la
    seconde à 106,855 s (5,3 s). Les deux lots sont séparés de plus de 1 s : la suppression puis la
    création de la racine arrivent l'une après l'autre.
  - U3 : idem, 2,1 s et 5,4 s.
- **`refresh` ne vide pas le lot en attente.** Après U4, le `refresh` passe de 6 à 5 greffons
  observés (« Observation de 5 greffon(s) »). La regreffe du chemin déjà en lot part quand même :
  `clear()` ferme les observateurs, mais `this.grafts` garde ses éléments.
- **Option `recentlyBusy` (fenêtre de 3 s).**
  - La seconde regreffe de U2 et U3 (5,3 s) tombe hors d'une fenêtre comptée depuis la fin de la
    commande. Elle n'y tomberait que comptée depuis la fin de la regreffe précédente d'F2
    elle-même, ce qui est fortuit.
  - Les cas lancés au terminal (T3, T4, T4b) se produisent sans lepton en cours dans l'éditeur.
  - Enfin, F2 ignorerait pendant tout appel de lepton les modifications réelles de l'utilisateur
    dans un clone, y compris pendant ses propres `seed status` et `file owner`. T2 serait alors
    perdu s'il tombait dans la fenêtre.
- **Option « relire `seed status --json` ».** Elle ne couvre pas U2, U3, T4b : le greffon y est
  greffé et le refus vient de la racine elle-même.
- **Trunk (L3-4)** : en T4, la suppression du répertoire `trunk/…/env64lib` donne un
  `file owner --json` (code 0, pas `unlinked`) et aucune boîte. Observateur du trunk inchangé.

## 2. Questions du PA-115

1. **D23, forme.** Proposition : développer `~` et `~<utilisateur courant>` dans `resolveLepton`
   (`os.homedir()`). `~<autre>` donne un message clair au lieu de « introuvable », faute d'API Node
   (écart au PA-113, où lepton développe tout `~<compte>`). `${userHome}` et `$HOME` ne sont pas
   pris en charge. La description du réglage est complétée (« `~/…` accepté »). Fonction pure dans
   `lepton.ts`, testée par `node:test`.
2. **D31.** Le traiter dans ENV-64, même lot que D23 : `~` développé par la même fonction, chemin
   relatif résolu depuis `runner.cwd()` avant `Uri.file` (`commands.ts:258`, `:280`). Ou le
   laisser hors plan.
3. **D24, correction.** Options :
   - (a) F2 ignore un événement dont le chemin est la racine `scion/` d'un greffon observé
     (création ou suppression du clone entier). C'est le seul chemin que lepton refuse par
     construction. Le lot en attente est aussi filtré au `refresh`. La règle est déterministe et ne
     dépend d'aucun délai ; elle couvre les 6 cas et laisse T2 inchangé. Effet : T3 (clone
     supprimé à la main, liens cassés) devient silencieux dans l'éditeur.
   - (a′) comme (a), plus, pour la seule suppression d'une racine dont le greffon reste déclaré,
     une information « clone supprimé hors de lepton : liens du trunk cassés → `lepton seed
     status` ». Plus de code et une lecture de lepton de plus.
   - (b) `recentlyBusy` sur F2 : ne couvre pas la seconde regreffe de U2 et U3, ni les cas du
     terminal, et masque des modifications réelles (§1.3).
   - (c) relire `seed status --json` avant la regreffe : ne couvre pas U2, U3, T4b.
   - (d) message seul (information au lieu d'avertissement) : l'appel voué à l'échec demeure.
   Proposition : (a).
4. **D24, cas couverts** : les 6 cas du tableau, avec l'option (a).
5. **Version** : `0.5.3` (corrections, commandes inchangées).
6. **Tests** :
   - D23 et D31 : `lepton.test.ts`, par la fonction pure ;
   - D24 : le filtre (chemin, racines observées) séparé dans un module sans API de l'éditeur
     (`batch.ts` ou voisin), testé par `node:test`, plus le rejeu VSCodium du §3 du fichier
     d'étape (U4, puis la regreffe ordinaire T2 ; U2 ajouté).

## 3. PA-115 (2026-11-19, décisions de l'utilisateur)

1. **D23** : `~`, `~<utilisateur courant>` et `${userHome}` sont développés dans `lepton.path`.
   Pour `~<autre compte>`, lepton n'est pas lancé et le message d'introuvable est précisé (« seuls
   ~, ~<U> et ${userHome} sont développés »), traduit. `$HOME` n'est pas pris en charge. La
   description du réglage est complétée.
2. **D31** est traité dans ENV-64, dans le même lot que D23. Avant d'ouvrir le fichier après
   `file add` et `file mv`, l'extension développe `~` et `~<moi>` et résout un chemin relatif depuis
   `runner.cwd()`. Elle ne développe pas `${userHome}`, que lepton ne développe pas dans les
   chemins. Pour `~<autre compte>`, le fichier n'est pas ouvert et une information le dit.
3. **D24**, option (a′). Au vidage du lot, F2 sépare les racines `scion/` des autres chemins, qui
   restent regreffés comme avant. S'il y a une racine, `seed status --json` passe dans la file (donc
   après la commande de lepton en cours). Ensuite, pour chaque racine :
   - présente → rien ;
   - absente et greffon encore greffé → information « clone supprimé hors de lepton… » ;
   - absente et greffon non greffé → rien.

   Le filtrage du lot au `refresh` est gardé en complément (décision de l'utilisateur), bien que
   son effet ait été nul dans les cas mesurés (§1.3).
4. **Cas couverts** : les 6 cas du §1.3.
5. **Version** : 0.5.3.
6. **Tests** : `node:test` d'abord, avec échec sur `main`. D23 et D31 vont dans `lepton.test.ts` ;
   le filtre de D24 va dans un module sans API de l'éditeur. Rejeu VSCodium : `--purge`,
   `seed replace`, regreffe ordinaire.

## 4. Correction (`devenv/env-64`)

| Commit | Contenu |
| --- | --- |
| 4cac85d | Tests D23 et D31, `test/lepton.test.ts` (3 tests). Sur le code de `main` : compilation en échec (TS2305, exports absents) ; tests émis : 3 en échec (`env-64-extension/tests-avant-correction-d23.txt`) |
| c17be86 | `lepton.ts` : `expandHome`, `foreignHome`, `inputPath` ; `resolveLepton` développe `~`, `~<U>` et `${userHome}`. `runner.ts` : message d'introuvable précisé pour `~<autre>`. `commands.ts` : `open()` après `file add` et `file mv`, avec information pour `~<autre>`. Description du réglage et traductions complétées |
| d066a18 | Tests D24, `test/batch.test.ts` (4 tests). Sur le code de `main` : compilation en échec (TS2305, TS2339) ; tests émis : 4 en échec (`env-64-extension/tests-avant-correction-d24.txt`) |
| 8e81559 | `batch.ts` : `Batcher.retain`, `isUnder`, `splitRoots`, `deletedClones`. `watch.ts` : racines observées depuis l'activation (`roots`), filtrage du lot au `refresh`, `clonesChanged` (`seed status --json` dans la file, puis information si un clone a été supprimé hors de lepton) ; les autres chemins sont regreffés comme avant |
| 56cd33f | Version 0.5.3 : `package.json`, `package-lock.json`, `README.md:8`, `extension/README.md` ; `dist/lepton-0.5.3.vsix` ajouté et `lepton-0.5.2.vsix` retiré dans le même commit |

- `npm test` : **29** tests réussis, 0 échec (`package.test.ts` compris : un seul `.vsix`).
- `npm run package` : `dist/lepton-0.5.3.vsix` (19 fichiers, 37,77 Ko).
- Installation au Mac par `codium --install-extension extension/dist/lepton-0.5.3.vsix --force` :
  `lepton-distribution.lepton@0.5.3`.

## 5. Contrôles

### 5.1 D23
- Script rejoué : `env-64-extension/d23-apres.tsv`. Seules 4 lignes changent : `~/…`, `~<U>/…` et
  `${userHome}/…` lancent lepton (code 0) ; `~` est développé en `<HOME>`, un répertoire, d'où
  `spawn <HOME> EACCES` (même effet qu'un chemin absolu de répertoire sur `main`). Les autres
  formes sont inchangées.
- Essai dans l'éditeur : l'espace d'essai règle `lepton.path` en
  `~/lepton-tools-dev/essais/env-64-releves/lepton-horodate.sh`. Après rechargement de la fenêtre,
  tous les appels de l'extension passent par l'enveloppe (`env-64-extension/appels-apres.tsv`).

### 5.2 D31
« Créer un fichier dans le greffon » avec
`~/lepton-tools-dev/essais/env-64-essai/trunk/sys/root/src/lib/env64lib/env64_d31.h` : `file add`
rend le code 0, puis le fichier s'ouvre dans l'éditeur, sans boîte d'erreur (constat de
l'utilisateur). La création est ensuite regreffée par F2 (code 0).

### 5.3 D24
Journal : `env-64-extension/appels-apres.tsv`. Notifications relevées par l'utilisateur.

| Cas | Appels F2 après la commande | Notification |
| --- | --- | --- |
| U2 `seed replace` → depot2 (extension) | 2 × `seed status --json` (contrôle des racines) ; aucun `graft --path` | « remplacer env64lib — terminé » seulement |
| U3 `seed replace` → depot (extension) | idem | idem |
| U4 `seed remove --purge` (extension) | aucun : racine écartée par le filtrage au `refresh` | « retirer env64lib — terminé » seulement |
| `seed remove --purge` relancé au terminal (§5.4) | 1 × `seed status --json` ; aucun `graft --path` | aucune |
| T2 témoin créé puis supprimé (terminal) | `graft --path <fichier>`, code 0, deux fois | aucune (regreffe ordinaire inchangée) |
| T4 `scion graft-remove --purge` (terminal) | 1 × `seed status --json` (code 1 : greffon déclaré non greffé, JSON lu) | aucune |
| T4b clone recréé (terminal) | 1 × `seed status --json` | aucune |
| T3 clone supprimé à la main (terminal) | 1 × `seed status --json` (code 1 : 3 liens cassés) | « Clone de library-env64lib supprimé hors de lepton : ses liens du trunk sont cassés (lepton seed status) », seule notification des essais au terminal (constat de l'utilisateur) |

- Après U2 à U4, l'état est égal au départ : 3059 liens, 0 cassé, 0 régulier, graine identique
  (`etat.sh`, 6 relevés).
- Le filtrage au `refresh`, sans effet à l'audit, a servi pour U4 : l'ordre entre le vidage du
  lot et la fin du `refresh` varie d'un essai à l'autre. Sans lui, le contrôle des racines aurait
  conclu de même.
- En T3, le nom affiché est `library-env64lib`, la feuille de la clé. Avec le clone supprimé,
  lepton ne lit plus le manifeste du greffon (`seed status --json`, champ `name`).

### 5.4 Écart de la séquence d'essai, et constat O-1 (hors périmètre)
- **Écart de séquence.** Au premier passage des contrôles, le fichier créé pour D31
  (`env64_d31.h`, non commité dans le clone) a fait refuser par scion les trois actions suivantes :
  `graft-remove --purge` refusé, « contient des modifications non commitées ; --purge refusé », code
  2. L'erreur venait de la séquence proposée par la session. Après retrait du fichier, la graine a
  été rétablie (voir O-1), puis U2 à U4 rejoués.
- **O-1** : `lepton seed remove <g> --purge` refusé par scion laisse la graine à moitié modifiée.
  `seed_remove` (`lepton/seed.py:688-692`) lance `seed-scion-remove` **avant**
  `graft-remove --purge`, et ne rétablit rien quand ce dernier échoue. Résultat :
  `.scion.sources.list` et `.scion.ramifications` n'ont plus le greffon, `lepton-graine.json` le
  garde (`bibliotheques`), et il reste greffé avec son clone. `lepton file remove` refuse alors :
  « greffon … hors de la graine ». Le relancement conseillé par le message (« corriger la cause…
  puis relancer ») aboutit : avertissement « greffé hors de la graine : retiré du trunk seulement »,
  code 0, état égal au départ. `seed replace` n'est pas touché : son `graft-remove` vient en
  premier et l'échec ne laisse rien. lepton est dans lepton-tools, donc O-1 n'est pas éligible au
  ticket (règle de `HORS-PLAN.md`).

## 6. Questions du PA-116

1. Rapport accepté (§4, §5) ?
2. O-1 : à ajouter à `HORS-PLAN.md` (D32), à traiter plus tard ? Il n'est pas éligible au ticket.
3. `essais/env-64-essai`, `essais/env-64-depot`, `essais/env-64-depot2` et `essais/env-64-releves`
   (journal brut, enveloppe, états ; les relevés utiles sont versionnés sous `env-64-extension/`) :
   suppression par `scripts/supprimer-essai.sh` ?
4. Fusion `--no-ff` de `devenv/env-64` dans `main`, puis push de `main` et de `devenv/env-64`
   (PA-P). La validation Debian (installation du `.vsix` 0.5.3, rejeu de `d23.cjs`) se fera en ENV-66.
