# Étape ENV-68 — lepton : chemins saisis et cohérence de la graine (D29, D30, D32, D37)

## Contexte
Révision du plan du 2026-11-23, faite à partir de `HORS-PLAN.md`. D29, D30, D32 et D37 sont à
traiter. Décision de l'utilisateur, à la fin du plan après ENV-66 : une seule étape lepton, en
deux lots. Ce ne sont pas des tickets : lepton-tools n'est pas un greffon du rootstock.

**Lot 1 — chemins saisis** (`rapports/env-63-tilde.md` §1.3, §1.5)
- D29 : trois chemins sont lus sans `expanduser()`, hors des 6 de D21 :
  - `check FILE` ;
  - `seed mkconf import PATH` ;
  - `seed new --mkconf PATH`.

  Un `~/…` littéral y est refusé. Le message montre le chemin : « fichier introuvable », ou
  « absent du trunk greffé ». Rien n'est créé. L'extension transmet le chemin saisi de
  `seedMkconfImport`.
- D30 : `generate --clangd` avec un chemin relatif écrit `clangd.path` tel que saisi. Ce chemin
  est relatif au répertoire courant de `generate` (cas `p6-r`).

**Lot 2 — cohérence de la graine** (`rapports/env-64-extension.md` §5.4 ;
`rapports/env-66-debian.md` §6bis)
- D32 : `seed remove <g> --purge` peut être refusé par scion, parce que le clone a des
  modifications non commitées. La graine reste alors à moitié modifiée :
  - `seed-scion-remove` passe avant `graft-remove --purge`, et rien n'est rétabli ;
  - `.scion.sources.list` et `.scion.ramifications` n'ont plus le greffon ;
  - `lepton-graine.json` le garde, et il reste greffé avec son clone.
- D37 : un greffon déclaré dans la graine dont le clone a disparu ne peut pas être retiré :
  `seed remove` répond « non greffé ». Il ne peut pas non plus être réajouté : `seed add` répond
  « déjà déclaré dans la graine sans être greffé ». Le message de `seed add` propose
  `lepton seed remove <g>`, qui échoue.

Faits relevés à la révision (`main` 172fb67 ; numéros indicatifs) :
- `lepton/rootstock.py:44` : `expand_user(text, what)`, forme commune de D21 (PA-113).
- `lepton/cli.py:79` : `check`, `path = Path(name)`.
- `lepton/seed.py:262` : `import_mkconf`, avec un chemin absolu ramené au trunk (l. 266-271).
  Il est appelé avec `args.path` (l. 331, `mkconf import`) et `args.mkconf` (l. 420, `seed new` ;
  contrôle préalable l. 416).
- `lepton/generate.py:113` : `find_clangd`. `~` y est développé depuis ENV-63 (l. 117-118), puis
  `shutil.which(explicit) or (explicit if Path(explicit).is_file() else None)` (l. 119).
- `lepton/seed.py:675` : `seed_remove`. `key_of` (`rootstock.py:352`) ne lit que les manifestes
  greffés, d'où `non greffé` (l. 680). `seed-scion-remove` est à la l. 691, avant `graft-remove`
  à la l. 694.
- `lepton/seed.py:614` : `check_new_scion`, message « déjà déclaré … » qui renvoie à
  `lepton seed remove`.
- `lepton/seed.py:479-499` : `status_data`. Pour un greffon sans manifeste (clone absent), le nom
  rendu est `e.name`, suffixe de la clé (`library-env65lib`, `rootstock.py:76-86`), avec le rôle
  « sans manifeste ». `pickScion` de l'extension (`extension/src/commands.ts:72-80`) propose ce
  nom.
- Annulation existante à reprendre : l'annulation d'un `seed add` en échec, l. 660-671
  (« graine et trunk restaurés »).

Archétype : infrastructure. Chaque lot a sa variable :
- lot 1 : des entrées acceptées ;
- lot 2 : l'état laissé après un échec (D32), et l'admission d'un greffon sans clone (D37). Les
  deux points ont chacun leurs tests et leur commit, pour que chaque changement reste imputable.

Ni binaire, ni scion, ni l'extension ne changent. Un besoin de l'extension relevé ici va à ENV-69
(0.5.4) ou au hors-plan. Les liens du trunk ne changent pas, sauf les liens cassés d'un greffon
sans clone retiré selon le PA-123.

## Prérequis
- ENV-66 terminée ; ENV-67 conseillée avant (règles des consignes). Indépendante d'ENV-69, ENV-70, ENV-71.
- lepton 0.1.0 ; scion 0.6.3.3, ou celui d'ENV-70 s'il est publié avant ; `pytest` 570 verts au
  départ, plus ceux des étapes faites avant.
- Outils d'ENV-63 à reprendre : `rapports/env-63-tilde/chemins.sh`, relevés `avant/`, `apres/`,
  `d17/` ; `rapports/env-59-tilde/essai.sh` (D17).
- Skill `lepton-rootstock` (rootstock d'essai). Branche `devenv/env-68` dans lepton-tools seulement.

## Tâches

### 1. Audit (lecture seule) → PA-123
Rapport `rapports/env-68-lepton.md`. Essais sur `essais/env-68-essai`, copie d'`essais/env-11/qemu`
par `rsync -a`, sans `build/`. Jamais sur `<ROOTSTOCK>`.
- **D29, D30** : table, forme d'ENV-63. Pour chaque chemin et chaque forme (`~/…`, `~<U>/…`,
  `~<sans compte>/…`, relatif, absolu, sous le trunk et hors du trunk), relever le message, le
  code et l'état laissé. Scripts versionnés sous `rapports/env-68-lepton/`, pour ENV-72.
- **D32** : reproduire `seed remove --purge` avec un clone aux modifications non commitées, puis
  relever les fichiers de la graine, la liste greffée et le trunk. Relever les autres échecs entre
  les deux appels de scion : `graft-remove` sans `--purge`, `seed replace` (l. 725-733). Relever
  si scion contrôle le clone avant tout changement.
- **D37** : supprimer le clone d'un greffon déclaré (par `scripts/supprimer-essai.sh`, forme de
  R66-1), puis relever `seed remove` (sous le nom de la graine et sous le suffixe de clé),
  `seed add`, `seed replace`, `seed status --json`, `check`. Relever `scion graft-remove <clé>`
  sans clone : code, liste greffée (`.scion.grafted.list`), liens cassés du trunk. Relever aussi
  ce que montre et transmet l'extension (`pickScion`).
- **PA-123** : l'utilisateur tranche :
  - D29 : forme d'ENV-63 (`expand_user`) pour les 3 chemins. Pour `--mkconf` et
    `mkconf import`, le chemin développé suit la règle « absolu sous le trunk » d'`import_mkconf`.
    <À CONFIRMER au PA-123> ;
  - D30 : chemin relatif rendu absolu depuis le répertoire courant, ou refusé avec un message.
    <À CONFIRMER au PA-123> ;
  - D32 : correction, qui est l'une de ces trois :
    - contrôle préalable, avant toute modification ;
    - ordre inversé : `graft-remove` d'abord ;
    - graine rétablie après l'échec (forme des l. 660-671).

    Cas couverts (`seed remove`, `seed replace`). <À CONFIRMER au PA-123> ;
  - D37 : forme :
    - `seed remove` admet un greffon déclaré sans clone, et retire alors sa déclaration et sa
      ligne de `lepton-graine.json` ;
    - nom accepté : nom de la graine, suffixe de clé (celui que montre `seed status`), ou les deux ;
    - sort de l'entrée de la liste greffée et des liens cassés du trunk ;
    - message de `seed add` corrigé ;
    - sort de `seed replace` ;
    - extension inchangée dans cette étape.

    <À CONFIRMER au PA-123> ;
  - tests : forme et emplacement ; `README.md` touché ou non.
- Aucune modification avant la réponse.

### 2. Correction (`devenv/env-68`)
- Tests d'abord, pour chaque cas retenu, qui échouent sur `main`. Les formes inchangées sont
  couvertes par un test qui passe déjà.
- Commits séparés : lot 1, puis D32, puis D37. Réinstaller lepton par
  `pipx install --force ~/lepton-tools-dev/lepton-tools`, écrit tel quel (règle `allow`).

### 3. Contrôles → PA-124
- `pytest` complet vert.
- Table du §1 rejouée : les lignes visées suivent le PA-123, les autres sont identiques à l'avant.
  Après chaque essai, les liens du trunk et la graine sont égaux au départ.
- Table d'ENV-63 (`chemins.sh`) rejouée : D21 inchangé. `rapports/env-59-tilde/essai.sh`
  rejoué : D17 inchangé (relevé égal à `env-63-tilde/d17/`, aux chemins d'essai près).
- D32 et D37 rejoués sur la copie : graine cohérente après l'échec ; greffon sans clone retiré,
  puis réajouté.
- Extension : l'utilisateur relance dans VSCodium `seedMkconfImport` avec un chemin `~/…`, puis le
  retrait d'un greffon sans clone. Sinon, la raison de ne pas l'essayer est donnée au rapport.
- **PA-124** : rapport ; sort d'`essais/env-68-essai` (par `scripts/supprimer-essai.sh`) ; push et
  fusion de `devenv/env-68` dans `main` (PA-P). La validation Debian se fait en ENV-72.

## Critères de validation
- [ ] PA-123 et PA-124 tranchés et consignés.
- [ ] Nouveaux tests : échec sur `main`, réussite sur la branche ; `pytest` complet vert.
- [ ] D29 et D30 suivent le PA-123 ; D21 et D17 inchangés.
- [ ] D32 : après un `--purge` refusé, les fichiers de la graine, `lepton-graine.json` et le trunk
      sont cohérents entre eux.
- [ ] D37 : un greffon déclaré sans clone se retire par lepton (forme du PA-123).
- [ ] `HORS-PLAN.md` : D29, D30, D32, D37 marqués traités, avec renvoi au rapport.

## Pièges connus
- Le shell développe `~` avant lepton : essayer `'~/…'` entre apostrophes, `--option=~/…` ou en
  liste (forme de l'extension ; `rapports/env-59-tilde.md` §1.6).
- Un clone modifié sous `depots/` de la copie seulement. Jamais sous `<ROOTSTOCK>`, jamais sous
  `depots/tiers/` (le hook refuse).
- `seed remove` conserve le clone sans `--purge`. Le D37 de la VM a été produit sur une copie
  `tar` d'`essais/env-53-c5` (`essais/env-66-essai/c4/gen`), dont le clone avait été supprimé par
  l'enveloppe (`rapports/env-66-debian.md` §6bis).
- Sur la graine de référence, lepton refuse `seed add` sans `--no-seed` (`refuse_reference`) :
  utiliser la graine de projet de la copie.
- Une redirection fait sortir `pytest` de sa règle `allow` (D20) : journal par `--junitxml`.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, branche, §Versions (lepton réinstallé), décisions PA-123 et PA-124,
journal. `HORS-PLAN.md` : D29, D30, D32, D37. Passation `handoff/env-68.md`.
