# ENV-69 — Extension : greffons observés rafraîchis (D36)

Session du 2026-11-23, Mac. Branche `devenv/env-69` (lepton-tools, depuis `main` c0fff59).
Extension 0.5.3 au départ ; Node 22.15.0, npm 11.3.0 ; `npm test` 29 verts sur la base.

## 1. Audit (avant correction)

### 1.1 Essai
- `essais/env-69-essai` : `rsync -a` d'`essais/env-11/qemu` sans `build/`, puis `lepton generate`
  (code 0). Au départ : 3059 liens, 0 cassé, 0 régulier, `check` conforme (5 fichiers).
- Greffon d'essai `env69lib` : `lepton scion new env69lib --type bibliotheque --repo
  essais/env-69-depot --no-seed --no-cmake` (27551d4). Seconde origine `essais/env-69-depot2`,
  clone du premier avec `env69_v2.h` en plus (92466b4).
- L'espace d'essai règle `lepton.path` sur l'enveloppe `env-69-extension/lepton-horodate.sh`
  (reprise d'ENV-64) : chaque appel de l'extension est noté à la milliseconde dans
  `essais/env-69-releves/appels.log`.
- Mesures en ligne de commande sur une seconde copie, `essais/env-69-mesures` (même origine).

### 1.2 T3 reproduit (extension 0.5.3)
Relevés : `env-69-extension/t3-avant/` (`canal.txt`, `notifications.txt`, `appels.log`).
1. VSCodium ouvert par l'utilisateur sur `env-69-essai/env11.code-workspace`. Canal : deux
   `seed status --json` (code 0), puis « Observation de 5 greffon(s) et du trunk … ».
2. Terminal : `lepton seed add env69lib file://localhost<E>/env-69-depot@master --type
   bibliotheque --no-cmake`, code 0, 3062 liens, 0 cassé.
3. Terminal, 13,6 s plus tard : `scripts/supprimer-essai.sh …/library-env69lib/master`
   (« supprimé : … »). 3062 liens, 3 cassés.
4. **Aucune notification** (constat de l'utilisateur) ; **aucun appel** de l'extension après
   ceux de l'ouverture (enveloppe et canal). D36 est confirmé : `library-env69lib` n'est pas
   observé, la suppression de son clone n'est pas vue.

### 1.3 Fichiers changés par les opérations de graine
Outil : `env-69-extension/fichiers.sh` (instantanés `instantane.py` avant et après chaque
opération ; contenu comparé). Résultat : `env-69-extension/fichiers/fichiers.txt`, journal
`fichiers/journal.txt` (toutes les opérations rendent le code 0).

| Opération (terminal) | Fichiers de la graine `depots/lepton-seed/env11/scion/.scion/` | `trunk/.scion.grafted.list` | Greffons observés (`seed status`) |
| --- | --- | --- | --- |
| `lepton seed add` | `lepton-graine.json`, `.scion.sources.list`, `.scion.ramifications` | contenu changé | +1 |
| `lepton seed replace` (autre origine) | `.scion.sources.list` | contenu identique, **réécrit** (date changée, même inode) | inchangés (le clone change sous le même `stem`) |
| `lepton seed remove --purge` | les 3 | contenu changé | −1 |
| `scion graft-remove --purge` | **aucun** | contenu changé | −1 |
| `scion graft` (rien à faire) | aucun | non réécrit | inchangés |
| `lepton graft --path` (création, suppression), `scion graft --scion` | aucun | non réécrit (inode, date, taille relevés) | inchangés |
| `lepton generate`, `seed status --json`, `check` | aucun | non réécrit | inchangés |

Conséquences :
- La liste des greffons observés (`stem` des greffons de `seed status --json`) suit
  `.scion.grafted.list`, pas la graine : après `scion graft-remove`, le greffon reste déclaré
  dans la graine mais n'est plus listé. Les fichiers de la graine ratent ce cas, et une graine
  de projet peut porter plusieurs `.scion/` (une par graine).
- `.scion.grafted.list` est unique, à la racine du trunk (`status.trunk`), dans un dossier de
  l'espace. Il est écrit en place (même inode) : l'observateur reçoit un événement de
  modification, pas une création. L'observateur actuel du trunk (F3, L3-4) ignore les
  modifications (`ignoreChangeEvents` vrai, `watch.ts:110-111`) et n'existe que si
  `redirectTrunkCreations` ou `confirmTrunkDeletions` est actif : il ne peut pas servir tel quel.

### 1.4 Appels de `seed status --json` et risque de boucle
- `refresh()` et `clonesChanged()` passent par `runner.exec` ; seul `runner.run` (commande de
  l'utilisateur) émet `onDidRunCommand` (`runner.ts:98`). Un rafraîchissement ne relance donc
  pas de rafraîchissement par ce chemin.
- Aucune opération lancée par F2 ou F3 (`graft --path`, `file owner`, `file add --adopt`,
  `seed status`) ne réécrit `.scion.grafted.list` (§1.3). Un observateur de ce fichier ne crée
  donc pas de boucle.
- `refresh()` ne reconstruit les observateurs, et n'écrit « Observation de … » au canal, que si
  la signature (trunk, stems, réglages) change : un rafraîchissement sans changement coûte un
  `seed status --json` (deux lignes au canal), rien de plus.
- Appels par candidat :
  - **observateur de `.scion.grafted.list`** regroupé par `Batcher` : un appel par opération au
    terminal. `seed replace` réécrit la liste (dégreffe puis regreffe : une ou deux écritures,
    non dénombrées) : un appel si le délai couvre l'écart. Pour une commande de l'extension qui change la liste (`seed add`,
    `remove`, `replace`) : un appel de plus que sur 0.5.3 (celui de `onDidRunCommand` et celui
    de l'observateur), sauf à faire passer les deux par le même `Batcher` ;
  - **fichiers de la graine** : même coût, mais `scion graft-remove` manqué, et un observateur
    par graine ;
  - **périodique** : un appel par période, sans fin, même sans aucun changement, et un retard
    égal à la période.

## 2. PA-125 — questions et propositions

| Question | Proposition de la session |
| --- | --- |
| Déclencheur | Observateur de `trunk/.scion.grafted.list` (création, modification, suppression), créé dès qu'un trunk existe et qu'au moins un des trois réglages est actif ; `onDidRunCommand` et `onDidChangeConfiguration` gardés |
| Regroupement | `Batcher` (`batch.ts`), délai 1000 ms. Variante (a) : seul l'observateur passe par le `Batcher`, `onDidRunCommand` inchangé (un `seed status` de plus après une commande de l'extension qui change la liste). Variante (b) : `onDidRunCommand` passe aussi par le `Batcher` (un seul appel, rafraîchissement retardé d'1 s après une commande de l'extension ; ordre F2/`refresh` de D24 changé) |
| Cas couverts | `seed add`, `seed remove` (avec ou sans `--purge`), `seed replace`, `scion graft-remove`, `scion graft` d'un greffon ajouté à la liste, tous au terminal ; `seed replace` sans effet sur la liste observée (stems inchangés) |
| Tests | Logique de l'éditeur (observateur, `Batcher` déjà testé par `node:test`) : essai VSCodium seul, appels relevés par l'enveloppe ; aucun nouveau test `node:test` |
| Version | 0.5.4 (décision du 2026-11-23) |
