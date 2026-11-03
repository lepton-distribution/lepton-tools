# ENV-29 — scion : `graft-update` sûr (version déclarée, trunk préservé) — 2026-11-03

Session Mac. Fichier d'étape : `etapes/ENV-29-scion-graft-update.md`.

Branches `devenv/env-29` :
- lepton-tools, depuis `main` 91e0aa8 ;
- `<SEED_SCIONS>`, depuis `master` e4d76b2.

État de départ :
- lepton-tools `main` 91e0aa8 ;
- seed.scions `master` e4d76b2, tag 0.5.3.0 sur ad292ee ;
- clone noyau `master` 0c0cc4f ;
- graine `original-tree` 15740f9.

Tous ces dépôts sont propres. Outils installés : scion 0.5.3.0 et lepton 0.1.0 (pipx).

## 1. Audit (tâche 1)

### 1.1 Code de scion 0.5.3.0

`cmd_graft_update` (`scion/cli.py:157`) enchaîne les opérations dans cet ordre :
1. `seed_updates` contrôle les graines et fait leur `fetch`, sans rien modifier.
2. **`ungraft` vide le trunk.**
3. `advance_seeds` fait l'avance rapide des graines.
4. `sync(update=True)` est lancé pour chaque graine.
5. `graft` regreffe.

`sync` (`scion/graft.py:44`) :
- réécrit `.scion.grafted.list` ;
- appelle `_fetch` (`graft.py:91`) :
  - clone existant : `gitops.pull(destination)`, c'est-à-dire `git pull` nu sur la branche
    courante. Le résultat dépend de `pull.rebase` / `pull.ff` de l'utilisateur. La version
    déclarée n'est pas lue.
  - clone nouveau : `gitops.clone(url, dest, version)`, puis `checkout <version>`. C'est le seul
    endroit où la version déclarée est appliquée.

`graft` (`graft.py:249`) ne défait, en cas de conflit, que **ce qu'il vient de créer**. Comme
`ungraft` a déjà tout retiré, le trunk ne garde que `.scion.grafted.list`.

Autres commandes :
- **`cmd_graft` (`scion graft`, `cli.py:129`) a le même ordre (`ungraft`, puis `graft`)** : un
  conflit y vide aussi le trunk (essai §1.3).
- `cmd_seed_update` (`cli.py:108`) appelle `advance_seeds` et `sync(update=True)`, sans `ungraft`
  ni `graft`. Le même `git pull` nu le concerne, mais le trunk n'est pas touché.
- `graft --scion` (`graft_scions`) remet déjà les anciens liens en cas d'échec (`_unlink` /
  `_restore`). Il n'est pas concerné.

La version déclarée se lit dans `entry.ref.version` (colonne 3 de `.scion.grafted.list`). Le
répertoire du clone porte cette version (`depots/<étagère>/<préfixe>/<version>`) : un clone a donc
une seule version.

### 1.2 Cas d'un clone hors version déclarée (fixture hors réseau, code de `master` e4d76b2)

Le script de mesure (hors dépôt) construit la fixture des tests de scion (`tests/make_fixture.py`,
7 liens). Il prépare le clone `beta`, avance l'amont d'un commit, puis appelle `graft-update` en
processus, dans un répertoire temporaire. Fixture de test : non soumis à PA-P (comme la suite de
tests). git 2.50.1.

| Cas | Code | Liens | Clone après | Message |
| --- | --- | --- | --- | --- |
| A1 autre branche locale, propre, sans amont | 2 | 7 → **0** | reste sur `ancienne` | `git pull` : pas d'amont |
| A2 autre branche publiée, en retard (forme d'E-1) | **0** | 7 → 7 | **reste sur `ancienne`, sans avertissement** | — |
| B1 autre branche, commits non publiés | 2 | 7 → **0** | reste sur `travail` | `git pull` : pas d'amont |
| B2 branche déclarée, commits non publiés, amont avancé | 2 | 7 → **0** | `master` divergée | « Need to specify how to reconcile divergent branches » |
| C1 modifications non commitées, sans recouvrement | 0 | 7 → 8 | avancé, modification gardée | — |
| C2 modifications non commitées, en conflit avec l'amont | 2 | 7 → **0** | inchangé | `git pull` : « Aborting » |
| D `HEAD` détaché | 2 | 7 → **0** | détaché | `git pull` : pas sur une branche |
| E version déclarée = tag (`v1`) | 2 | 7 → **0** | détaché sur `v1` | `git pull` : pas sur une branche |
| F amont injoignable | 2 | 7 → **0** | inchangé | `git pull` : dépôt absent |
| G l'amont introduit un conflit de greffe | 1 | 7 → **0** | avancé | « 1 conflit(s) de greffe » |

Constats :
- **K1** : 8 cas sur 10 laissent le trunk vide. Le défaut 2 d'ENV-28 n'est pas propre au conflit :
  tout échec survenu après `ungraft` le provoque (git, réseau, conflit).
- **K2** : un greffon déclaré par un **tag** fait échouer `graft-update` à chaque fois (cas E),
  car `git pull` est impossible sur un `HEAD` détaché. Aucun rootstock actuel n'en déclare : tous
  les greffons distants sont en `master`, et `original-tree` est une branche.
- **K3** : un clone sur une autre branche publiée est tiré **en silence** (A2). En l'absence de
  conflit, la commande réussit avec le code 0. C'est le mécanisme d'E-1.
- **K4** : `git pull` nu dépend de la configuration de l'utilisateur. Les graines, elles, avancent
  par `merge --ff-only` depuis ENV-23 (G-a).

### 1.3 Reproduction sur une copie de `<ROOTSTOCK>`

Copie `~/lepton-tools-dev/essais/env-29` :
- `cp -RP` de `depots/`, `trunk/`, de la signature et de `.scion.trunk.tolerated`, sans `build/`
  ni `third_party/` (135 Mo).
- Listes produites par `rapports/env-15-liste-trunk.sh` dans `~/lepton-tools-dev/essais/env-29-mesures/`
  (non versionné).
- Référence `<ROOTSTOCK>` : 3956 liens, 0 fichier régulier, 0 lien cassé ; SHA-256 de la liste
  triée `a7afbc1db34448cd…`. Copie identique.

| Essai | Action | Résultat |
| --- | --- | --- |
| `graft` | clones `original` (e5a5689) et `family-stm32f4xx` (af964c6) sur `devenv/env-14`, puis `scion graft` | code 1, 277 conflits, **0 lien**, seul `.scion.grafted.list` reste |
| retour | les 2 clones sur `master`, puis `scion graft` | code 0, liste = référence |
| E-1 (PA-P accordé le 2026-11-03, copie seule) | mêmes 2 clones sur `devenv/env-14`, puis `scion graft-update` | code 1, 277 conflits (comme R28-1), **0 lien**, clones **restés** sur `devenv/env-14` |
| retour | les 2 clones sur `master`, puis `scion graft` | code 0, liste = référence (`a7afbc1d…`) ; têtes et branches des 14 clones identiques à `<ROOTSTOCK>`, clones propres |

### 1.4 Usages par lepton et par l'extension

lepton :
- Il n'appelle **ni `graft-update` ni `seed-update`** (`grep` sur `lepton/`, `extension/src`).
- Il appelle **`scion graft` complet** à trois endroits :
  - `lepton graft` (`files.py:368`), qui sert aussi à la commande « regreffer » de l'extension ;
  - `seed.py:374` ;
  - `seed.py:840`, qui remet les clones au verrou puis regreffe.
- Il appelle aussi `graft --scion`, `graft-remove`, `seed-add`, `seed-scion-add/remove`.
- La seule dépendance de version est `SCION_MIN_VERSION`, (0, 5, 3, 0) dans `lepton/__init__.py`,
  contrôlée par `scion_runner.py`.

Codes de retour de scion, inchangés par cette étape : 1 pour `ScionError`, 2 pour `GitError`.
lepton les relaie tels quels, et l'extension affiche la sortie.

Conséquence : corriger `scion graft` (K1) protège aussi `lepton graft` et l'extension.

### 1.5 Propositions pour le PA-45

**Q1. Clone hors version déclarée**
- Recommandation : **option 2**, refuser toujours. Le message nomme le clone, sa branche ou son
  `HEAD`, et la commande de remise (`git -C <clone> switch <version>`).
- Tous les clones sont contrôlés avant tout dégreffage, et « rien n'a été modifié » à l'arrêt.
- Raisons :
  - un développeur place volontairement un clone sur une branche d'étape, et le déplacer change le
    trunk sous ses pieds ;
  - c'est la règle déjà appliquée aux graines (`seed_updates`) ;
  - c'est la plus simple à tester.

Définition de « à la version » :
- branche déclarée : branche courante = version ;
- tag déclaré : `HEAD` = commit du tag ;
- sinon, le clone est hors version, `HEAD` détaché compris.

**Q2. Trunk en cas d'échec**
- Recommandation : **option 2**, restaurer l'état antérieur, avec deux compléments :
  - (a) toutes les opérations git (contrôles, `fetch`, avance des clones) passent **avant**
    `ungraft`, ce qui couvre K1 pour les cas git et réseau ;
  - (b) si la regreffe échoue, les liens relevés avant `ungraft` sont remis (`_restore`, qui
    existe déjà), ainsi que l'ancienne `.scion.grafted.list`.
- L'option 1 exigerait un second algorithme de détection des conflits, parallèle à
  `_graft_entries`.
- Limite commune aux deux options : les clones ont déjà avancé. La liste des liens est identique
  (SHA-256 de la liste triée), mais un lien peut pointer vers un fichier retiré en amont. Le
  message le signale, et la prochaine regreffe réussie le corrige.

**Q2 bis, à confirmer : même protection pour `scion graft`**
- Proposé : `scion graft` reçoit la même protection (b).
- Raison : il a le même défaut (§1.3), et c'est la commande qu'utilisent lepton et l'extension.

**Q3. Version** : **0.5.4.0** recommandée. Le contrat de `graft-update` et de `seed-update`
change :
- nouveaux refus ;
- `--ff-only` à la place de `pull` ;
- tags pris en charge.

Ce n'est pas un simple correctif.

**Q4. `SCION_MIN_VERSION`** : le relever à la nouvelle version, ce qui protège `lepton graft`
(§1.4). L'étape exige que toutes les références de version désignent la même version.

**Q5. Règle P-1 d'ORCHESTRATION §2bis** : **l'alléger**.
- Garder le relevé de la branche des clones dans les consignes VM, parce qu'il est informatif.
- Supprimer l'arrêt manuel, puisque scion ≥ 0.5.4.0 refuse lui-même.
- Rappeler que la VM reste en 0.5.3.0 jusqu'à ENV-33.

**Propositions de détail, à valider en bloc**

P-1. Avance d'un clone à la version, pour `graft-update` et `seed-update` :
- remplacer `git pull` par `fetch` puis `merge --ff-only @{u}`, comme pour les graines ;
- refuser une branche divergée, ou sans amont ;
- laisser telle quelle une branche seulement en avance (journal) ;
- refuser des modifications suivies si le clone est en retard, et les laisser sinon ;
- tag : `fetch --tags`, puis refus si le tag a bougé.

P-2. Les nouveaux refus sont des `ScionError` (code 1). Ils listent **tous** les clones fautifs
avant de s'arrêter, comme le rapport de conflits.

P-3. `seed-clone` (sans mise à jour) reste inchangé.

P-4. Tests, un par cas du §1.2 :
- A1 et A2 refusés, trunk intact ;
- B1 refusé, commits gardés, clone non déplacé ;
- B2 refusé (divergé) ;
- C1 et C2 refusés (clone en retard avec modifications) ;
- modifications sur un clone à jour : laissées, code 0 ;
- D refusé ;
- E à jour, code 0 ;
- F trunk intact ;
- G trunk restauré, liste identique ;
- `scion graft` sur conflit, trunk restauré.

Les 137 tests existants restent verts.

### 1.6 Décisions du PA-45 (utilisateur, 2026-11-03)

Toutes les propositions du §1.5 sont retenues :
- Q1 : option 2, refus toujours.
- Q2 : option 2, `scion graft` compris.
- Q3 : 0.5.4.0.
- Q4 : `SCION_MIN_VERSION` = (0, 5, 4, 0).
- Q5 : règle P-1 allégée.
- P-1 à P-4 validées en bloc.

Consigné dans `DEVENV-STATUS.md` §Décisions.
