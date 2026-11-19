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

## 3. Journal des messages (§2bis)

| ID | Date | Type | Sens | Résumé | Remis |
| --- | --- | --- | --- | --- | --- |
