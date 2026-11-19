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
