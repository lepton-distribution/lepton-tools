# ENV-66 — Validation Debian groupée (ENV-62 à ENV-65) — rapport de la session Mac

Session Mac `validation-debian-env-66`, 2026-11-19. Branche lepton-tools `devenv/env-66` (depuis
`main` 6bc05ad). Consigne VM : `consignes/env-66-debian.md`. Journaux Mac :
`~/lepton-tools-dev/essais/env-66-mac/`. Essais : `~/lepton-tools-dev/essais/env-66-essai/`,
`~/lepton-tools-dev/essais/env-66-fixture/`.
Outils Mac : scion 0.6.3.3 et lepton 0.1.0 (pipx), extension 0.5.3, git 2.50.1, Python 3.11.5,
Claude Code 2.1.328.

## 1. Préparation (tâche 1)

### 1.1 Têtes publiées (`git ls-remote`, 2026-11-19)

Relevé : `env-66-mac/ls-remote-mac.txt` (script `env-66-mac/ls-remote.sh`, repris
d'`env-61-mac/ls-remote.sh` avec le tag 0.6.3.3). Différences avec le relevé d'ENV-61 :

| Dépôt | Référence | Commit | En R61-1 |
| --- | --- | --- | --- |
| `lepton-tools` | `main` | 6bc05ad | 7018302 |
| `seed.scions` | tag `0.6.3.3` (`master` 49ca4ae) | 9615cd5 | tag `0.6.3.2` 08a1460 (`master` 975caf6) |
| `lepton-original-tree.scions` (noyau) | `master` | 2b4a647 | dfc960b |
| graine `original-tree`, 12 autres greffons, 8 miroirs (HEAD et tags) | | inchangés | = |

Le noyau 2b4a647 (fusion d'e589b63) ne change que 5 fichiers hors de `scion/` : `SCION_REF`
0.6.3.3 dans `install-{macos,debian}.sh`, `README.md`, `README-PAQUET.md`, `doc/BUILDING.md`.
Rien n'est greffé, aucun lien ne change : une regreffe des rootstocks d'essai n'avance que le
clone noyau. lepton-tools depuis R61-1 (7018302) : lepton (D21, `expand_user`), extension 0.5.3
(D23, D24, D31), `scripts/comparer-releves.py` (D27), `scripts/importer-skills.sh`, `SCION_REF`
0.6.3.3 d'`install-vscodium.sh`, tests. `.claude/settings.json` (`b01ad557…d235`),
`proteger-trunk.py` (`04572df6…6909`) et `supprimer-essai.sh` (`04323a00…0e15`) sont inchangés
depuis R61-1 (dernier commit qui les touche : f3da447).

### 1.2 Liens du trunk de `<ROOTSTOCK>`

`env-43-mac/controler-trunk.py ~/lepton` contre `env-50-mac/attendu/trunk-liens.txt` : code 0,
`CONFORME` (3889 liens, 0 fichier régulier, 0 lien cassé, 629 projetés, 0 écart de nom ni de
contenu, 8 clones tiers aux HEAD épinglés, filtre `blob:none`). L'attendu de liens de R50-1 et
celui des clones tiers d'ENV-53 restent valables.

### 1.3 Essai préalable : `graft-update` d'`essais/env-13-vierge` (attendu de C3)

PA-P accordé par l'utilisateur pendant la préparation (2026-11-19). État avant : 13 clones de
greffons sur `master`, propres ; 8 clones tiers détachés à leur version, propres ; noyau dfc960b ;
3889 liens. `env-57-mac/regreffer-essai.sh avant`, puis, lancée par la session hors script
(invite `ask` annoncée « à confirmer », confirmée) :
`scion graft-update -v ~/lepton-tools-dev/essais/env-13-vierge > …/env-13-vierge-graft-update.log 2>&1; echo "code=$?" >> …`,
puis `apres`.

| Contrôle | Résultat |
| --- | --- |
| `graft-update -v` (scion 0.6.3.3) | code 0 ; 1 clone avancé : `…/original/master avancé : dfc960b -> 2b4a647` ; 0 `git clone` ; 0 extraction partielle ; 0 conflit ni refus ; « 3889 feuilles liées » ; « 6 chemin(s) ignoré(s) par git » (`.DS_Store` du Finder) |
| Inventaire | seule la ligne du noyau change |
| Liens | 3889 → 3889, 0 ajouté, 0 retiré ; `controler-trunk.py` `CONFORME` |
| Clones tiers | extraits et `sparse-checkout` = attendu, 0 / 16 ; `depots/tiers` 107 992 → 107 992 Ko |
| `lepton check`, `generate` | 0, 0 ; espace identique |

Attendus versionnés (`<R>`, `<HOME>`) : `attendu/c3/graft-update-resume.txt` (83 lignes, filtre
`resume()` de la consigne d'ENV-61, vérifié : il redonne ce fichier), `env-13-vierge-bilan.txt`,
inventaires avant et après. Contre `env-61-mac/attendu/c3/` :
- les lignes du noyau changent (`ed2a41f -> dfc960b` devient `dfc960b -> 2b4a647`) ;
- **une ligne nouvelle** dans le résumé : `fatal: not a git repository (or any of the parent
  directories): .git`. C'est le stderr de `git rev-parse --show-toplevel` sur la source non git
  `depots/generation/building/scion`, que scion 0.6.3.3 écrit sous `-v` (`log.debug` du stderr,
  D22, PA-117 (3)). Écart attendu. Sur la VM, git l'écrit en français : `po/fr.po` l. 21977-21978.

### 1.4 Attendus de C4 (D21)

Copie d'essai `essais/env-66-essai/c4/rs` : `rsync -a --exclude /build/` d'`essais/env-11/qemu`
(noyau dfc960b, graine `env11`, 3059 liens, 0 cassé, 0 fichier régulier, `check` code 0).
`env-63-tilde/chemins.sh <E> apres <sortie>` : code 0, 289 relevés (`attendu/c4/`).

- Contre `env-63-tilde/apres/` : identique, sauf `resume.tsv`. Sa colonne 8 (message) est coupée
  à 160 octets **avant** la normalisation des chemins (`cut -c1-160`, l. 66) : sa fin dépend de la
  longueur des chemins de l'essai. Colonnes 1 à 7 identiques.
- Une première passe avec la phase `mac` a donné en plus le nom de phase dans 5 relevés
  (`cibles-mac`, `w-mac`). Elle a été écartée (déplacée vers `essais/env-66-mac/c4-phase-mac`) au
  profit de la phase `apres`, qui permet la comparaison octet pour octet.
- **Parties propres à l'hôte** de `chemins.sh` :
  - lien `outils/clangd` vers `clangd-mp-21` (MacPorts) et cas `p6-n` (`--clangd clangd-mp-21`).
    Le script prend désormais un 4ᵉ argument facultatif, le nom de clangd, `clangd-mp-21` par
    défaut (`clangd` sur Debian) : comportement du Mac inchangé, shellcheck sans nouvelle remarque
    (13 remarques `info` avant comme après, 0 au niveau `warning`). Écarts attendus sur la VM :
    `p6-n.cmd`, `p6-n.clangd` ;
  - les 19 `*.W` des cas lancés dans `<C>` ou `<G>` listent la racine du rootstock, `./.DS_Store`
    compris ; la copie de la VM vient d'`essais/env-53-c5` : écart admis hors de cette ligne
    seulement si les fichiers de sa racine diffèrent (relevé) ;
  - `<G>` (copie pour `generate --clangd`) est faite par `rsync` quand elle manque. La consigne la
    crée par `tar` (`rsync` non garanti sur la VM).
- **Forme de la VM rejouée au Mac** (contrôle de la consigne, D27) : essai neuf
  `essais/env-66-essai/c4t`, copies `rs` et `gen` par `tar --exclude=./build`, 4ᵉ argument
  `clangd-mp-21` → contre `attendu/c4/` par `scripts/comparer-releves.py` : `écarts=1 / 289`,
  `resume.tsv` seul (troncature). `.W` identiques (même rootstock d'origine).

### 1.5 Attendus de C5 (D25, D22)

**lepton** (`env-65-scion/essai.sh`) sur `essais/env-66-essai/c5/rs` (même copie d'`env-11/qemu`),
dépôt `essais/env-66-essai/depot65` (`lepton scion new env65lib --type bibliotheque --repo …
--no-seed --no-cmake`, `master` 3ac8eca, puis branche `dev` 9b88199 avec `DEV.txt`), scion 0.6.3.3
de pipx. Relevés `attendu/c5/` (28) :
- l01, l02 : code 2, refus de scion (clone adopté hors version), annulation par lepton, état égal
  au départ, clone laissé sur `master` ;
- l03 (clone remis sur `dev`) : `seed add` 0 (4 liens, `DEV.txt` compris), `check` 0,
  `seed remove --purge` 0, état égal au départ ;
- contre `env-65-scion/essai-apres/` : seuls changent l'empreinte de `.scion.sources.list` dans
  `l03.etat` (URL du dépôt) et `scion.txt` (scion de pipx, non du venv d'ENV-65).

Sur la VM, `depart.etat` et `l03.etat` porteront en plus l'empreinte de la graine `env11` de
`essais/env-53-c5`, qui n'est pas celle d'`essais/env-11/qemu`.

**Fixtures** : clone `essais/env-66-essai/seed-scions` (`git clone
https://github.com/lepton-distribution/seed.scions.git`, puis `switch --detach 0.6.3.3`, 9615cd5,
propre). Bases `essais/env-66-fixture/{f65,f60,f56}`, scion `~/.local/bin/scion` :

| Fixture | Code | Relevés | Contre ENV-65 (`*-apres/`) |
| --- | --- | --- | --- |
| `env-65-scion/fixture.py` → `attendu/fixture65/` | 0 | 284 | identique |
| `env-60-scion/fixture.py` → `attendu/fixture60/` | 0 | 179 | identique |
| `env-56-scion/fixture.py` → `attendu/fixture56/` | 0 | 76 | identique, sauf le nom de la base dans f12a, f12b (`env-65-fixture` → `env-66-fixture`) |

La VM utilisera la même base `essais/env-66-fixture` : 0 écart attendu après normalisation.

### 1.6 Attendu de C6 (D23)

`env-64-extension/d23.cjs` sur `~/.vscode-oss/extensions/lepton-distribution.lepton-0.5.3/out/src/lepton.js`
(identique, `cmp`, au `lepton.js` du `.vsix` publié), répertoire de travail
`essais/env-66-essai/d23cwd` → `attendu/d23.tsv`. Contre `env-64-extension/d23-apres.tsv` : seule la
forme relative change (profondeur du répertoire de travail). Le répertoire de la VM a la même
profondeur sous `$HOME` : ligne identique attendue.

Node.js est absent de la VM. **Runtime de VSCodium** : `ELECTRON_RUN_AS_NODE=1
/Applications/VSCodium.app/Contents/MacOS/VSCodium d23.cjs …` (Node 24.18.1, Electron 42.8.1)
donne une sortie identique, octet pour octet, à celle de Node 22.15.0. C'est le runtime qui fait
tourner l'extension : D23 peut se rejouer sur la VM sans installer Node.js
(`/usr/share/codium/codium`). Si le fusible `RunAsNode` y était désactivé, D23 resterait prouvé
au Mac seulement.

### 1.7 Outil de comparaison (D27)

`scripts/comparer-releves.py` a quatre traductions de plus, tirées de `po/fr.po` de git v2.47.3
(téléchargé de `raw.githubusercontent.com/git/git/v2.47.3/po/fr.po`, sha256 `62fbd300…cb8b8`,
identique à ENV-62) :

| Anglais | `fr.po` | Où |
| --- | --- | --- |
| bloc `Could not read from remote repository.` … `and the repository exists.` (l. 15855-15864) | `Impossible de lire le dépôt distant.` … `et que le dépôt existe.` | `*.git-err` de la fixture d'ENV-65 (stderr complet) |
| `Cloning into '%s'...` (l. 4492-4493) | `Clonage dans '%s'...` | idem |
| `unable to access '%s': %s` (l. 20309-20310) | `impossible d'accéder à '%s'⍽: %s` | n04 (`.err`, `.git-err`) |
| `not a git repository (or any of the parent directories): %s` (l. 21977-21978) | `ni ceci ni aucun de ses répertoires parents n'est un dépôt git⍽: %s` | journal `graft-update -v` (C3, §1.3) |

`'%s' does not appear to be a git repository` est absent de `fr.po` : attendu en anglais derrière
`fatal⍽: ` (déduction d'ENV-65, à vérifier sur la VM). Commits cc148f9 et 441c455 ; 3 tests ajoutés,
en échec avant la correction (`env-66-mac/tests-avant-correction.txt`), 13 au total. Inventaire des
lignes de git des attendus (`c4`, `c5`, fixtures) : `fatal:` suivi de « does not appear to be a
git repository », de la branche distante, de « Could not read from remote repository. » ou de
« unable to access » ; « Cloning into » ; toutes couvertes par la table.

pytest complet (`venv-lepton-tools`, `--junitxml`) : **570 passed**, 0 échec (8 min 41) ;
`test_proteger_trunk` 118, `test_garde_ask` 46, `test_supprimer_essai` 52, `test_milestone3` 53,
`test_comparer_releves` 13.

### 1.8 Contrôles de correction de la consigne (D27)

Chaque contrôle d'installation est écrit d'après le code installé au Mac, pas d'après un texte
ancien (piège d'ENV-61) :
- D21 : `lepton.rootstock.expand_user` présent (`True` au Mac, a60ea7c), et `rootstock.py` du
  venv pipx comparé par `cmp` au dépôt, par son chemin réel (`r.__file__`) ;
- scion : `scion.__version__` = `0.6.3.3` lu dans le venv de pipx ;
- extension : `install-vscodium.sh` installe `dist/lepton-<version de package.json>.vsix` et
  affiche `<id> : <actuelle> → <version>` (`installer_extension_lepton`, l. 348-362).

## 2. PA-119 — questions (à trancher par l'utilisateur)

1. **Consigne** `consignes/env-66-debian.md`, dont le **§0** : l'utilisateur retire de
   `~/.claude/settings.json` de la VM la seule entrée `Bash(python3 -m unittest discover *)`,
   session fermée, après relevé du fichier entier, puis ouvre une nouvelle session dans `$T`
   (PA-111). Bloc attendu : 2 règles (rapport d'ENV-62, §D26).
2. **C3** : regreffe de `$U`, `$E13`, `$C5`, `$R53` (le noyau a changé ; PA-P pour les 4
   `graft-update`). Proposition : oui.
3. **C5, fixtures** : les trois (ENV-65, ENV-60, ENV-56), base `essais/env-66-fixture`.
   Proposition : oui (la VM montre pour la première fois la première ligne de git en français).
4. **C6** : extension 0.5.3 par `install-vscodium.sh` ; D23 par le runtime de VSCodium (§1.6),
   sans Node.js. **D24** :
   - (a) dans VSCodium sur la VM, par l'utilisateur : U4 (`seed remove --purge` par l'extension)
     et T3 (clone supprimé à la main) sur `$W/c4/gen` ; l'observateur de fichiers de Linux
     (inotify) n'est pas celui du Mac (FSEvents), c'est la seule preuve sur cette plateforme ;
   - (b) D24 au Mac seulement (ENV-64) ; la logique de filtrage est couverte par `npm test`.
   Proposition : (a) si l'utilisateur a accès à l'interface de la VM, sinon (b).
5. **C7** : host et 16 presets dans `$R53` contre `env-61-debian`, et `mirror-sync --dry-run`.
   Aucune source compilée ne change. Proposition : maintenu (≈ 4 min ; dernier oracle Debian du
   plan).
6. **C8, cartes** : proposition : écarté (ni binaire, ni flash, ni sonde ne changent).
7. **C9, nettoyage** : `essais/env-66-essai`, `essais/env-66-fixture`, `~/env-61-journaux`,
   `~/tmp-pytest/env-61`, par `scripts/supprimer-essai.sh` ; conservés `$U`, `$E13`, `$C5`, `$R53`,
   `~/env-66-journaux`, `~/tmp-pytest/env-66`.
8. **PA-P** : push de `devenv/env-66`, puis envoi de l'ordre `R66-1` à la session VM désignée
   par l'utilisateur après le §0.

## 3. Rootstocks d'essai du Mac (tâche 3)

Accord de l'utilisateur (PA-P), 2026-11-19, pendant R66-1. scion 0.6.3.3, lepton 0.1.0. Branches
relevées avant (`env-53-mac/inventaire-clones.sh`) : clones de greffons sur `master`, propres,
noyau dfc960b partout ; graine `bout-en-bout` : 2 fichiers générés non suivis du 2 novembre
(`CMakeUserPresets.json`, `lepton-graine.lock.json`), déjà présents en ENV-61. Script
`env-57-mac/regreffer-essai.sh avant|apres` ; entre les deux, la session lance
`scion graft-update -v <rootstock> > <journal> 2>&1; echo "code=$?" >> <journal>` (invite `ask`
annoncée « à confirmer », confirmée). Journaux et bilans :
`~/lepton-tools-dev/essais/env-66-mac/regreffes/<rootstock>-*` (`env-13-vierge` :
`~/lepton-tools-dev/essais/env-66-mac/`).

| Rootstock | `graft-update` | Liens avant → après | Ajouts / retraits | `controler-trunk.py` | Clones tiers | `check` | Espace |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `env-13-vierge` (§1.3) | 0 ; noyau dfc960b → 2b4a647 seul | 3889 → 3889 | 0 / 0 | `CONFORME` | 8, = attendu (0 / 16), 107 992 Ko inchangés | 0 | identique |
| `env-9` | 0 ; noyau seul | 3059 → 3059 | 0 / 0 | `CONFORME` | — | 0 | identique |
| `env-11/qemu` | 0 ; noyau seul | 3059 → 3059 | 0 / 0 | `CONFORME` | — | 0 | identique |
| `env-11/qemu-gra2` | 0 ; noyau seul (BSP an386 réinscrit, 3059 feuilles), puis `scion graft-remove lepton@bsp-qemu-mps2-an386 <rootstock>` : « retiré : 8 feuilles », clone conservé | 3051 → 3051 | 0 / 0 | `CONFORME` | — | 1 (attendu, CFG-5) | identique |
| `env-11/bout-en-bout/rootstock` | 0 ; noyau seul | 3059 → 3059 | 0 / 0 | `CONFORME` | — | 0 | identique |
| `env-11/f429zi` | 0 ; noyau seul | 3294 → 3294 | 0 / 0 | `CONFORME` | 2, = attendu (0 / 4), 36 528 Ko inchangés | 0 | identique |
| `env-11/wl55jc1` | 0 ; noyau seul | 3315 → 3315 | 0 / 0 | `CONFORME` | 4, = attendu (0 / 8), 40 684 Ko inchangés | 0 | identique |

Partout : aucun `git clone`, aucune extraction partielle, 0 conflit ni refus, 0 lien cassé,
0 fichier régulier, 0 `.DS_Store` dans les trunks ; `generate` avant et après au même code.

**`graft-remove` refusé par le classifieur.** Lancé par la session (hors règle, comme en ENV-61,
où il avait été accepté), il a été refusé par le mode auto (« Destructive or Unwanted Actions »).
Il n'a pas été contourné : l'utilisateur l'a lancé dans la session Mac (`!`), sans redirection.
La sortie, reportée par la session dans `env-11_qemu-gra2-graft-remove.log`, puis le bilan
`apres` confirment l'état attendu.

**Invites simultanées (constat pour D28).** La regreffe d'`env-9` (invite à confirmer, Mac) a été
présentée à l'utilisateur au moment où la VM lançait A1 (invite à refuser, 19:12 UTC). A1 a été
confirmée par erreur, sans effet (cible absente), puis rejouée et refusée. Parade appliquée pour la
suite de R66-1 : aucune invite au Mac pendant que la VM en présente une.

## 3bis. Contrôle du rapport VM (tâche 4)

Branche `origin/devenv/env-66-debian` = 9f34370, un commit sur 0eca739 (`devenv/env-66`), 984
fichiers, tous sous `rapports/env-66-debian.md`, `rapports/env-66-debian/` et
`rapports/oracles/env-66-debian/` (aucun autre fichier touché). Relevés extraits par
`git archive`, comparaisons refaites au Mac par `scripts/comparer-releves.py --home-attendu
/Users/cle_d_anton --home-obtenu /home/lepton-user` :

| Critère | Refait au Mac | = rapport VM |
| --- | --- | --- |
| C2 | `settings-utilisateur.json` : `permissions.allow` = 2 règles ; `15-decisions.tsv` : `pipx install --force` `rule projectSettings` ; U1, U2 `subcommandResults` ; U3 `classifier` ; A1 `user_temporary` (19:12:22) puis `rejet-invite` (19:13:33) ; H1 `reject hook` ; 4 `graft-update` `user_temporary projectSettings` (19:14:59 à 19:19:27) | oui |
| C3 | `9-resume-<nom>.txt` ×3 contre `attendu/c3/graft-update-resume.txt` : seule la l. 61 diffère, remplacée par les 2 lignes de la variante « point de montage » de git (`po/fr.po` l. 21981-21988) | oui |
| C4 | `10-c4` : écarts=50 / 289, classés au Mac : 19 `.W` (racine sans `.DS_Store` ni `.scion.trunk.tolerated`, rien d'autre), `depart.etat`, 6 relevés `p1-z`, `p4-z` (zsh absent), 15 `.err` `p2-*`, `p3-*`, `p5add-*`, `p5dir-*`, `p5graft-t` (ligne « chemin(s) ignoré(s) par git » seule), 6 `p6-*.out` (`presets : env11-debug-qemu`), `p6-n.cmd`, `p6-n.clangd`, `resume.tsv` | oui |
| C5 | `11-c5` : écarts=2 / 28 (`depart.etat` ; `l03.etat` : 3 empreintes de la graine seules) ; fixtures : 0 / 284, 2 / 179, 1 / 76 ; k07 et f05 : seule la fin du message diffère (`warning: Could not find remote branch nope to clone.`) ; pytest : 570 tests, 0 échec, 0 erreur, 0 ignoré | oui |
| C6 | `11-d23` : écarts=0 / 1 | oui |
| C7 | `oracles/env-66-debian` : `mklepton` = `env-61-debian` ; `comparer-oracle.py` contre `env-61-debian` : 0 pour les 16 presets | oui |

Cause de l'écart de C4 classe 3, vérifiée au Mac : `.DS_Store` du Finder ignorés par git dans les
clones de la copie du Mac (noyau 6, BSP an386 7). Leçon pour les consignes : le contrôle Mac du
§1.4 a été rejoué sur le même rootstock d'origine que l'attendu, il ne pouvait montrer ni la
racine, ni la graine, ni les fichiers ignorés propres au Mac.

`FIN-SUCCÈS R66-1` vérifié : C1 à C7 atteints (C2, C5 avec un écart, C3 avec un écart admis, C6 et
C7 au rejeu), C8 écarté au PA-119, C9 partiel (`~/tmp-pytest/env-61`, 421 Mo, laissé sur la VM :
`supprimer-essai.sh` n'accepte que `~/tmp-pytest` entier, ORCHESTRATION §2bis ; la forme du §14
de la consigne n'était pas exécutable telle qu'écrite).

## 4. Journal des messages (§2bis)

| ID | Date | Type | Sens | Résumé | Remis |
| --- | --- | --- | --- | --- | --- |
| ORDRE R66-1 | 2026-11-19 | Mac (`validation-debian-env-66`, 9ca006) → VM (`debian-linux-vm`, 4f53c0, ouverte après le §0 selon l'utilisateur) | consigne `env-66-debian.md` @ 0eca739 **par référence** (chemin, branche, commit, sha256 `48eb3e5f…561e`, le fichier fait foi, lecture intégrale demandée), et non recopiée comme en R61-1 (52 Ko) : forme du tableau §2bis (« consigne (chemin, branche, commit) ») ; périmètre C1 à C9 du PA-119 ; actions de l'utilisateur : A1 à refuser, 4 `graft-update` à confirmer, D24 (U4, T3), push ; envoi accepté par Remote Control (msg fd9183c0) | oui (envoi) |
| ACCUSÉ R66-1 | 2026-11-19 | VM (`debian-linux-vm`, ref a67d18, adresse `bridge:session_01FkeafxUZjHhFVSETRFL9R9`) → Mac | reçu directement. §5 sans arrêt : `$T` = répertoire de travail, `devenv/env-66` = 0eca739, propre ; sha256 de la consigne = ordre ; Claude Code **2.1.328** (journal `a0115cd5-….jsonl`, première entrée 19:59:38 +0100, après `0-settings-apres.txt` 19:58:25) ; empreintes `settings.json`, hook, enveloppe, `comparer-releves.py` = Mac ; diff du §0 = entrée `unittest` seule retirée ; têtes publiées = Mac ; `$U`, `$E13` : noyau dfc960b, 3889 liens, 8 tiers ; `$C5` : noyau dfc960b, 3059 liens, `salut` modifs=2, 2 tiers F7 ; scion 0.6.3.2 ; écarts sans arrêt : `rsync` absent (prévu, §7), `node` absent (attendu), `CLAUDE_PROJECT_DIR` vide, mtime de `~/.claude/settings.json` postérieure au §0 à contenu identique (cause supposée par la VM : `/model` au démarrage) | oui |
| AVANCEMENT R66-1 (§6, §7) | 2026-11-19 | VM → Mac | §6 conforme : scion 0.6.3.3 (`install-debian.sh`, code 0), lepton réinstallé (`rootstock.py` = dépôt, `expand_user` True), extension `0.5.2 → 0.5.3` (`changements 1`) ; constat : répertoire `lepton-distribution.lepton-0.5.2` resté dans `~/.vscode-oss/extensions` (`extensions.json` ne cite que 0.5.3) ; §7 conforme (3 copies, 3059 liens, `depot65` 3301d15 / f509460) | oui |
| QUESTION R66-1 (§8.2, A1) | 2026-11-19 | VM → Mac et utilisateur | **écart** : invite A1 parue (règle `ask`), annoncée « À REFUSER », mais **confirmée** (`accept user_temporary projectSettings`, 19:12:22 UTC) ; code 1, « n'est pas un rootstock », sans effet. Cause probable (constat Mac) : invites `graft-update` de la tâche 3 au Mac (`env-9`, à confirmer) présentées à l'utilisateur au même moment. Réponse : l'utilisateur décide directement dans la session VM de rejouer A1 | oui |
| AVANCEMENT R66-1 (§8 fin) | 2026-11-19 | VM → Mac | A1 second essai annoncé « À REFUSER » : `rejet-invite` (19:13:33) ; H1 `reject hook hook` ; U1, U2 `subcommandResults` (forme admise), U3 `classifier` (D26 conforme) ; `pipx install --force` `rule projectSettings` ; cible absente, `essai-hook` absent, 0 paquet `env-66`, liens de c5 = départ ; §9 commence | oui |
| AVANCEMENT R66-1 (§9, env-28-debian) | 2026-11-19 | VM → Mac | invite `graft-update` annoncée « À CONFIRMER », confirmée par l'utilisateur | oui |
| QUESTION R66-1 (§9, env-28-debian) | 2026-11-19 | VM → Mac et utilisateur | regreffe conforme (noyau seul, 3889 → 3889, `CONFORME` ×2, tiers 0 / 16, `clones = Mac`, `check` 0, espace identique) ; `cmp_mac` du résumé : écarts=1 / 1, l. 61 : au lieu de « not a git repository (or any of the parent directories): .git », 2 lignes « fatal⍽: ni ceci ni aucun de ses répertoires parents (jusqu'au point de montage /) n'est un dépôt git » et « Arrêt à la limite du système de fichiers (GIT_DISCOVERY_ACROSS_FILESYSTEM n'est pas défini). » ; `/home` est un système de fichiers distinct sur la VM ; arrêt avant `env-13-debian` | oui |
| RÉPONSE R66-1 (§9) | 2026-11-19 | Mac → VM (`bridge:session_01FkeafxUZjHhFVSETRFL9R9`) | analyse : variante de git l. 21981-21988 de `po/fr.po` v2.47.3 (autre msgid, point de montage), propre à l'hôte, hors scion et lepton ; avis Mac : écart admissible, décision laissée à l'utilisateur ; règle de `comparer-releves.py` à ajouter au Mac après R66-1 si retenue | envoi accepté, remise non confirmée |
| AVANCEMENT R66-1 (§9, env-13-debian) | 2026-11-19 | VM → Mac | décision de l'utilisateur, prise dans la session VM : « continue le §9, écart admis pour cause d'hôte » ; `env-13-debian` : relevé avant 3889 liens, invite annoncée « À CONFIRMER » | oui |
| AVANCEMENT R66-1 (§9, env-13-debian, env-53-c5) | 2026-11-19 | VM → Mac | RÉPONSE reçue. `env-13-debian` conforme (noyau seul, 3889 → 3889, `CONFORME`, tiers 0 / 16, `clones = Mac`, `check` 0, espace identique) ; résumé : même écart de point de montage, seul ; `env-53-c5` : relevé avant 3059 liens, invite annoncée « À CONFIRMER » | oui |
| AVANCEMENT R66-1 (§9, env-53-c5, env-53-debian) | 2026-11-19 | VM → Mac | `env-53-c5` conforme (noyau seul, `salut` 71e1641 accepté sans amont `modifs=2`, 3059 → 3059, `CONFORME`, tiers F7 0 / 4, 30 908 Ko inchangés, `check` 0, espace identique) ; `env-53-debian` : relevé avant 3889 liens, invite annoncée « À CONFIRMER » | oui |
| AVANCEMENT R66-1 (§9 fin) | 2026-11-19 | VM → Mac | `env-53-debian` conforme (noyau seul, 3889 → 3889, `CONFORME`, tiers 0 / 16, 87 512 Ko inchangés, `clones = Mac`, `check` 0, espace identique ; résumé : écart de point de montage seul) ; 4 invites confirmées, aucun refus de scion ; §10 commence | oui |
| AVANCEMENT R66-1 (§10) | 2026-11-19 | VM → Mac | D21 confirmé (`~`, `~<U>` développés, `cwd/~*` non ×47, `~inconnu63` refusé par lepton ×6, états = départ) ; `cmp_mac` écarts=50 / 289 : 22 admis (`p6-n` ×2, `resume.tsv`, 19 `.W` : racine sans `.DS_Store` ni `.scion.trunk.tolerated`) ; **non prévus** : (2) zsh absent de la VM, `p1-z`, `p4-z` code 127, forme `z` non exercée (6 fichiers) ; (3) ligne « N chemin(s) ignoré(s) par git » absente sur la VM (15 `.err`) ; (4) graine `env11` de `$C5` : `depart.etat`, 6 `p6-*.out` (`presets : env11-debug-qemu` seul) | oui |
| RÉPONSE R66-1 (§10) | 2026-11-19 | Mac → VM | classe 3 confirmée au Mac : `.DS_Store` du Finder ignorés par git dans les clones de la copie (noyau 6, BSP an386 7 → 13 et 6) ; classes 2 à 4 : manque de la consigne (contrôle du §1.4 rejoué sur le même rootstock d'origine), sans effet sur D21 ; continuer | envoyé |
| AVANCEMENT R66-1 (§11.1, §11.2) | 2026-11-19 | VM → Mac | D25 conforme (l01, l02 code 2, clone laissé sur `master`, graine et liste = départ ; l03 0 / 0 / 0 ; écarts=2 / 28, `depart.etat` et `l03.etat`, admis) ; fixture65 écarts=0 / 284 ; **fixture60 2 / 179 (k07), fixture56 1 / 76 (f05)** : `git clone -b nope --quiet --single-branch`, git 2.47.3 écrit d'abord « warning: Could not find remote branch nope to clone. », que D22 retient au lieu de la cause (git 2.50.1 du Mac : ligne `fatal:` seule) ; fixtures sous `LC_ALL=C` : `.err` en anglais (manque de la consigne), français relevé à part (`11-git-fr.txt`) : n01 « fatal⍽: '…' does not appear to be a git repository » (déduction d'ENV-65 vérifiée), bloc « Impossible de lire le dépôt distant… », n03, n04, « Clonage dans » ; pytest lancé | oui |
| RÉPONSE R66-1 (§11.2) | 2026-11-19 | Mac → VM | k07 / f05 : défaut de scion 0.6.3.3 avec git 2.47.3, limité à `seed-add --single-branch` (`cli.py` l. 366, `gitops.py` l. 119, `_run` l. 41) ; hors périmètre d'ENV-66, présenté au hors-plan ; consigner sans correction ; continuer | envoyé |
| AVANCEMENT R66-1 (§11.3, §11.4 D23, D24 préparé) | 2026-11-19 | VM → Mac | pytest **570 passed**, 0 échec (179,5 s ; modules = Mac) ; D23 par `ELECTRON_RUN_AS_NODE=1 /usr/share/codium/codium` (Node 24.18.1, Electron 42.8.1) : code 0, `d23.tsv identique`, écarts=0 / 1 ; D24 : `env65lib@dev` ajouté à `c4/gen` (3063 liens) ; U4 demandé à l'utilisateur | oui |
| AVANCEMENT R66-1 (§11.4 U4, T3) | 2026-11-19 | VM → Mac | **U4 conforme** : notification unique relevée par l'utilisateur, « lepton : retirer env65lib — terminé » ; 3059 liens, clone absent ; T3 : `seed add` 0, clone `…/library-env65lib/dev` supprimé par `supprimer-essai.sh` ; relevé des notifications demandé à l'utilisateur | oui |
| AVANCEMENT R66-1 (§11.4 T3) | 2026-11-19 | VM → Mac | **écart** : aucune notification en T3 ; état attendu (3063 liens, 4 cassés) ; canal Lepton : aucune entrée après « Observation de 5 greffon(s) » (après U4) ; cause lue par la VM dans `watch.js` : `refresh()` seulement sur commande de l'extension ou changement de réglage, le `seed add` du terminal n'a pas fait observer `library-env65lib` ; aucune notification d'échec de regreffe | oui |
| RÉPONSE R66-1 (§11.4 T3) | 2026-11-19 | Mac → VM | cause confirmée (`watch.ts` l. 50-53) : défaut de la séquence de la consigne (en ENV-64, T3 suivait U2, U3 par l'extension) ; comportement de fond au hors-plan ; rejeu proposé après le §12, sur décision de l'utilisateur (seed remove, seed add, « Lepton : état de la graine » dans VSCodium pour rafraîchir, suppression du clone, relevé) | envoyé |
| RÉPONSE R66-1 (§11.4 T3, décision) | 2026-11-19 | Mac → VM | décision de l'utilisateur : rejouer T3 après le §12 selon la proposition (5 points) ; premier T3 consigné « non probant » | envoyé |
| QUESTION R66-1 (§12.1) | 2026-11-19 | VM → Mac et utilisateur | `rejouer-oracle.sh` code 1 : host 7/7, 8 presets FreeRTOS construits et capturés, banc 20/20, 16/16, 19/19 ; **8 presets embOS en échec de configuration** : `LEPTON_EMBOS_ROOT` absente de l'environnement de la session rouverte au §0 (défaut `<rootstock>/third_party/…` de `lepton-env.sh`, absent de `$R53`) ; embOS présent dans `~/lepton/third_party/embos/cortexm-gcc/5.20.0.0` ; proposition : rejouer le §12.1 avec la variable en tête de ligne | oui |
| RÉPONSE R66-1 (§12.1) | 2026-11-19 | Mac → VM | manque de la consigne (relevé par `consignes/env-53-debian.md` l. 189, plus depuis ENV-57) ; avis favorable : rejeu du §12.1 entier, `LEPTON_EMBOS_ROOT=` en chemin absolu, `RTOS.h` relevé avant ; décision à l'utilisateur | envoyé |
| AVANCEMENT R66-1 (§12.1 rejeu) | 2026-11-19 | VM → Mac | décision de l'utilisateur dans la session VM : « oui, relance le §12.1 avec LEPTON_EMBOS_ROOT » ; `RTOS.h` présent ; premier passage gardé (`12-rejouer-passage1.log`) ; rejeu lancé, chemin absolu | oui |
| AVANCEMENT R66-1 (§12 fin) | 2026-11-19 | VM → Mac | **C7 conforme** après rejeu : « tout a réussi », 16 oracles, host 7/7, banc 20/20, 16/16, 20/20, 16/16, 19/19, 19/19, `peripheriques` ×4 ; mklepton = R61-1 = `env-52-apres` ; `comparer_R61-1` 0 et `hors_debug` 0 ×16 ; `mirror-sync --dry-run` code 0, 0 signalement, 7 références à envoyer sur 4 miroirs, toutes expliquées par l'amont (postérieures au 2026-11-17) : `cmsis_device_f4` v2.6.12 (2026-11-18), `stm32wlxx-hal-driver` `main` e70dfa4 (2026-11-19), `stm32f7xx-hal-driver` v1.3.4 (2026-11-19), `cmsis_device_f7` v1.2.11 (2026-11-19) ; rien envoyé | oui |
| QUESTION R66-1 (T3 rejeu) | 2026-11-19 | VM → Mac et utilisateur | points 1 et 2 refusés par lepton, code 1, sans effet : `seed remove` « greffon « env65lib » non greffé », `seed add` « déjà déclaré dans la graine sans être greffé » (renvoi à `scion seed-scion-remove`) ; options (a) `seed-scion-remove`, (b) T3 non probant | oui |
| RÉPONSE R66-1 (T3 rejeu) | 2026-11-19 | Mac → VM | point 1 de la proposition Mac faux (constat au hors-plan : lepton ne retire pas un greffon déclaré dont le clone a disparu) ; option (c) proposée : `seed add` sur la copie vierge `c5/rs`, VSCodium ouvert ensuite (greffons lus à l'activation, « Observation de 6 greffon(s) »), suppression du clone, relevé ; décision à l'utilisateur | envoyé |
| AVANCEMENT R66-1 (T3 rejeu, option c) | 2026-11-19 | VM → Mac | décision de l'utilisateur dans la session VM : « option (c), rejoue T3 sur c5/rs » ; espace `env11.code-workspace` présent ; `seed add` 0, 3063 liens, clone présent ; VSCodium (fenêtre c4/gen) à fermer, puis ouvert sur c5/rs par l'utilisateur, nombre de greffons observés à relever | oui |
| AVANCEMENT R66-1 (T3 rejeu) | 2026-11-19 | VM → Mac | « Observation de 6 greffon(s) » à l'ouverture, sans rafraîchissement ; clone supprimé par `supprimer-essai.sh` ; **T3 (c) conforme** : une seule notification, « Clone de library-env65lib supprimé hors de lepton : ses liens du trunk sont cassés (lepton seed status) », aucun échec de regreffe ; 3063 liens, 4 cassés | oui |
| QUESTION R66-1 (§15, push) | 2026-11-19 | VM → utilisateur | rapport commité 9f34370 sur `devenv/env-66-debian` (depuis 0eca739 ; 984 fichiers : `env-66-debian.md`, `env-66-debian/`, `oracles/env-66-debian/` ; `15-decisions.tsv` 90 appels) ; push demandé à l'utilisateur dans la session VM | oui |
| FIN-SUCCÈS R66-1 | 2026-11-19 | VM → Mac | C1 à C7 atteints, C8 écarté, C9 partiel (`~/tmp-pytest/env-61` refusé par l'enveloppe) ; `devenv/env-66-debian` 9f34370 poussée sur accord de l'utilisateur ; rapport `rapports/env-66-debian.md`, relevés `rapports/env-66-debian/`, oracle `oracles/env-66-debian/` ; points pour le hors-plan : variante « point de montage », `--single-branch` et git 2.47.3, greffon ajouté hors de l'extension non observé, `seed remove` d'un clone disparu, `LEPTON_EMBOS_ROOT`, `~/tmp-pytest/<sous-répertoire>` ; vérifié par la session Mac (§3bis) | oui |
