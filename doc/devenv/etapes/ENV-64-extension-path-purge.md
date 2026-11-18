# Étape ENV-64 — Extension : `lepton.path` et regreffe après `--purge` (D23, D24)

## Contexte
Révision du plan du 2026-11-18, faite à partir de `HORS-PLAN.md`. D23 et D24 sont à traiter
(décision de l'utilisateur du 2026-11-17, fin du plan, après ENV-61). Ce ne sont pas des tickets :
l'extension est dans lepton-tools (décision du 2026-11-18). Les deux constats viennent d'ENV-59 :
- **D23** (O-2, `rapports/env-59-tilde.md` §1.6, lu, non essayé). Le réglage `lepton.path` est
  passé tel quel à `spawn` (`resolveLepton`). Une valeur `~/…` n'est pas développée : on attend
  « exécutable introuvable ». Ajouté au hors-plan au PA-105.
- **D24** (O-3, `rapports/env-59-tilde.md` §5.3, vu par l'utilisateur dans VSCodium). Après
  « retirer un greffon de la graine » avec « supprimer aussi le clone (--purge) », l'observateur
  F2 voit la suppression du clone. Il lance `lepton graft --path <clone>/scion`, qui sort avec le
  code 1 : « ni dans le trunk …, ni dans un greffon greffé ». L'avertissement « lepton : regreffe
  automatique — … » s'affiche. L'état du rootstock ne change pas. Ajouté au hors-plan au PA-106.

Décision de l'utilisateur (révision du 2026-11-18) : une seule étape, deux lots, une version de
l'extension. Les deux points touchent des fichiers différents (`lepton.ts`, `watch.ts`).

Faits relevés à la révision (`main` 24ca20a ; numéros indicatifs) :
- `extension/src/lepton.ts:22` : `resolveLepton(configured, home = homedir())` rend `configured`
  tel quel (l. 24). Sinon il rend `~/.local/bin/lepton` s'il existe, ou `lepton`. Appelé par
  `runner.ts:39`. Tests : `extension/test/lepton.test.ts:54-58`.
- `extension/src/watch.ts` :
  - F2 (l. 96-100) : un observateur par `stem` de greffon greffé. `onDidCreate` et `onDidDelete`
    → `this.grafts.add(u.fsPath)`, **sans filtre** ;
  - trunk (l. 107-110) : une suppression n'est prise que si
    `!this.runner.recentlyBusy(LEPTON_QUIET_MS)`. `LEPTON_QUIET_MS` vaut 3000 (l. 20) ;
    `recentlyBusy` est défini dans `runner.ts:21` (L3-4) ;
  - `graft()` (l. 120-130) : code ≠ 0 → `runner.report(t("automatic regraft"), …)`.
- `extension/src/commands.ts:120-127` : choix « also delete the clone (--purge) », puis
  `seed remove <greffon> [--purge]`.
- Version : `extension/package.json:5` `0.5.2` ; `extension/dist/lepton-0.5.2.vsix`, installé par
  `scripts/install-vscodium.sh` (l. 347 et suivantes) ; `README.md:8` ;
  `extension/README.md:44` (« Version 0.5.2 (ENV-41) … »). Contrôle existant :
  `extension/test/package.test.ts:19` (« un seul .vsix, celui de la version de package.json »).
- Tests : `npm test` dans `extension/` (`tsc -p . && node --test out/test/*.test.js`).
  `watch.ts` dépend de l'API de l'éditeur et n'a pas de test `node:test`.

Archétype : infrastructure. D23 change une entrée acceptée (`lepton.path` avec `~`). D24 change
un comportement : l'observateur ne lance plus une regreffe vouée à l'échec. Aucun binaire ni
aucun lien du trunk ne change, ni aucune commande de lepton.

## Prérequis
- ENV-62 terminée ; ENV-63 conseillée avant (forme de `~` du PA-113). Indépendante d'ENV-65.
- Node 22.15.0 (nvm), npm 11.3.0, outillage `extension/package-lock.json` (DEVENV-STATUS
  §Versions). VSCodium 1.135.06055 au Mac.
- Méthode d'essai de l'extension : `rapports/env-59-tilde.md` §5 (x01 à x03, essai VSCodium par
  l'utilisateur) ; `rapports/env-55-url-file.md` §5.
- Skill `lepton-rootstock` (rootstock d'essai).
- Branche `devenv/env-64` dans lepton-tools seulement.

## Tâches

### 1. Audit (lecture seule) → PA-115
Rapport `rapports/env-64-extension.md`.
- **D23** : relever l'effet de `lepton.path` = `~/.local/bin/lepton`, `~<utilisateur>/…`,
  `${userHome}/…`, chemin relatif, nom nu. L'essai se fait sur `resolveLepton` et `runLepton`,
  par un script `node` hors de l'éditeur, versionné sous `rapports/env-64-extension/` pour être
  repris en ENV-66. Relever le message rendu par `notFound`, et ce que dit la description du
  réglage (`%config.path%`, `package.nls*.json`).
- **D24** : reproduire O-3 sur `essais/env-64-essai`, copie d'`essais/env-11/qemu` par
  `rsync -a`, sans `build/`. On y ajoute un greffon de bibliothèque d'essai (forme d'`env59lib`),
  puis on le retire avec `--purge` depuis VSCodium : action de l'utilisateur, canal « Lepton »
  relevé. Puis relever :
  - l'ordre des événements : fin de `seed remove`, suppressions vues par F2, appel de `graft` ;
  - le délai entre la fin de lepton et la regreffe (`Batcher`) ;
  - les autres cas où un clone greffé disparaît : `seed replace`, suppression à la main du
    clone, `graft-remove --purge` par scion au terminal.
- **PA-115** : l'utilisateur tranche :
  - D23 : `~` développé (forme du PA-113 pour lepton), ou refusé avec un message ; `${userHome}`
    pris en charge ou non. <À CONFIRMER au PA-115> ;
  - D24, correction. Options :
    - F2 ignore les suppressions pendant une commande de lepton et juste après, avec le
      mécanisme du trunk (`recentlyBusy`) ;
    - F2 ne regreffe pas un chemin dont le greffon n'est plus greffé (relire
      `seed status --json`) ;
    - seul le message change (information au lieu d'avertissement).
    <À CONFIRMER au PA-115> ;
  - D24, cas couverts : retrait `--purge` seul, ou aussi les autres cas du relevé ;
  - numéro de version : <À CONFIRMER au PA-115 : `0.5.3` proposé (corrections, commandes
    inchangées)> ;
  - tests : D23 dans `lepton.test.ts` ; D24, test `node:test` si la logique se sépare de l'API de
    l'éditeur, ou essai VSCodium seul.
- Aucune modification avant la réponse.

### 2. Correction (`devenv/env-64`)
- Lot D23 : tests d'abord, qui échouent sur `main`, puis la correction de `resolveLepton` et, s'il
  y a lieu, de la description du réglage (`package.nls.json`, `package.nls.fr.json`).
- Lot D24 : test d'abord si le PA-115 en prévoit un, puis la correction dans `watch.ts`.
- Commits séparés : un par lot, puis un pour la version : `package.json`, `package-lock.json`,
  `README.md:8`, `extension/README.md:44`, nouveau `.vsix` dans `extension/dist/` et retrait de
  `lepton-0.5.2.vsix` dans le même commit, pour que `package.test.ts` (un seul `.vsix`) reste vert.
- `npm test` vert ; `npm run package` ; installation du `.vsix` au Mac par
  `scripts/install-vscodium.sh` ou `codium --install-extension`.

### 3. Contrôles → PA-116
- D23 : le script du §1 rejoué ; les formes retenues au PA-115 lancent lepton, les autres sont
  inchangées.
- D24 : l'utilisateur rejoue dans VSCodium le retrait `--purge` du §1. Attendu : aucun
  avertissement « regreffe automatique » ; graine, trunk et liens égaux au départ. Puis une
  regreffe automatique ordinaire : un fichier créé dans le `scion/` d'un greffon greffé est
  greffé. F2 est ainsi inchangé hors du cas visé.
- **PA-116** : rapport ; sort d'`essais/env-64-essai` et du dépôt d'essai (par
  `scripts/supprimer-essai.sh`) ; push et fusion de `devenv/env-64` dans `main` (PA-P). La
  validation Debian (installation du `.vsix`) est faite en ENV-66.

## Critères de validation
- [ ] PA-115 et PA-116 tranchés et consignés.
- [ ] `npm test` vert, nouveaux tests compris (échec sur `main`, réussite sur la branche).
- [ ] D23 : `lepton.path` `~/…` lance lepton, ou donne le message retenu.
- [ ] D24 : aucun avertissement après le retrait `--purge` ; regreffe automatique ordinaire
      inchangée.
- [ ] `.vsix` de la nouvelle version construit, versionné, installé au Mac.
- [ ] `HORS-PLAN.md` : D23 et D24 marqués traités, avec renvoi au rapport.

## Pièges connus
- `recentlyBusy` ne couvre que 3 s après la fin de lepton. Un `Batcher` qui regroupe les
  événements plus longtemps, ou un observateur lent sur un gros clone, peut dépasser cette
  fenêtre. Mesurer avant de retenir l'option.
- Le trunk et F2 n'ont pas le même rôle : le trunk ignore les suppressions de lepton (L3-4). Une
  correction de F2 ne doit pas toucher l'observateur du trunk.
- Les clés projetées sont exclues de F2 (ENV-41, l. 87-88) : ne pas les réintroduire.
- Un `.vsix` installé reste actif jusqu'au rechargement de la fenêtre de VSCodium.
- L'espace `env11.code-workspace` de la copie vise `essais/env-11/qemu/build/.active` : lancer
  `lepton generate` dans la copie avant l'essai dans VSCodium (`rapports/env-55-url-file.md` §5).
- `npm run package` supprime `dist/*.vsix` (`rm -f`) : la version précédente doit être retirée
  par un commit, pas perdue sans trace.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, branche, §Versions (extension Lepton), décisions PA-115 et PA-116,
journal. `HORS-PLAN.md` : D23, D24. Passation `handoff/env-64.md`.
