# ENV-7 — Évolutions de scion proposées (PA-8)

Rédigé le 2026-10-13. Base : audit `env-2-scion.md`, périmètre PA-2 (`env-2-synthese.md`
§Périmètres validés), code de `<SEED_SCIONS>` `master` e0adb2c (= tag `0.5.0.1` + doc).
Suite de tests de référence : `python3 -m unittest discover -s tests` → 69 tests, 1 ignoré
(réseau), verts.

Besoin client (ENV-8, GRA-4) : ajouter, retirer, remplacer un greffon dans la graine, puis
regreffer, sans éditer les fichiers `.scion.*` à la main et sans `git pull` implicite.

## 1. Constat complémentaire : conflits fichier / répertoire (reproduits)

Script `scratchpad/essai-e6.sh` (rootstocks d'essai jetables, deux scions locaux `t/a`, `t/b`) :

| Cas | `a` | `b` | Résultat 0.5.0.1 |
| --- | --- | --- | --- |
| 1 | fichier `X` | répertoire `X/` | trace Python `FileExistsError` (`graft.py:153`), code 1, **pas d'annulation** |
| 2 | lien versionné `X -> d` | répertoire `X/` | **code 0** ; la feuille `y` de `b` est écrite **dans le clone de `a`** (`depots/a/scion/d/y`) via le lien du trunk |
| 3 | répertoire `X/` | fichier `X` | conflit détecté, code 1, annulation ; message « déjà fourni par « trunk » » au lieu de « t/a » |

Le cas 2 viole la garantie de 0.5 « rien n'est jamais écrit dans un clone ».

## 2. Évolutions proposées

Conventions communes : clé d'un scion `shelf@nom` (forme déjà utilisée par `scion git --key`) ;
codes de retour 0 succès, 1 erreur utilisateur, 2 échec git (inchangés) ; les fichiers `.scion.*`
modifiés gardent leurs commentaires et l'ordre des autres lignes ; aucun fetch, aucun `git pull`
implicite.

| # | Commande proposée | Comportement | Codes | Tests |
| --- | --- | --- | --- | --- |
| E1 | `scion seed-scion-add [--seed S] [--replace] CLÉ VERSION EMPLACEMENT [CHEMIN]` | Ajoute la ligne à `.scion.sources.list` et `shelf nom VERSION` à `.scion.ramifications` du seed. Clé déjà présente : refus, sauf `--replace` qui remplace toutes les lignes de la clé dans les deux fichiers (remplacement de GRA-4). Ne clone ni ne greffe : suite = `seed-clone` puis `graft`. `--seed` facultatif dans un `scion/` de seed (comme `seed-clone`). | 0 ; 1 (seed introuvable, clé présente sans `--replace`, `$` dans un chemin local) | ajout, refus de doublon, `--replace`, commentaires conservés, `seed-clone` + `graft` du scion ajouté |
| E2 | `scion seed-scion-remove [--seed S] CLÉ` | Retire toutes les lignes de la clé des deux fichiers du seed. Ne touche ni la liste greffée ni le trunk. | 0 ; 1 (clé absente) | retrait, clé absente, autres lignes intactes |
| E3 | `scion graft-remove [--purge] [--force] CLÉ [rootstock]` | Retire l'entrée de `trunk/.scion.grafted.list` et les seules feuilles de ce scion (liens dont la cible est sous son `scion/`), puis les répertoires devenus vides. `--purge` supprime aussi le clone sous `depots/` si : scion distant (cloné par scion), clone non partagé avec une autre entrée, `git status --porcelain` vide, aucun commit absent de l'amont. Scion local (`*`, emplacement hors `depots/<shelf>/…`) : `--purge` refusé (non géré par scion). | 0 ; 1 (clé absente, fichier régulier sous les chemins du scion sans `--force`, purge refusée) ; 2 (git) | feuilles retirées seules, autres scions intacts, clones propres, purge acceptée / refusée (sale, partagé, local) |
| E4 | `scion graft --scion CLÉ` (répétable) | Regreffe partielle : retire les feuilles du scion désigné, puis le greffe sur le trunk existant. Conflit avec un autre scion : signalé, annulation de ce que l'appel a créé, code 1. Sans `--scion` : inchangé (ungraft complet + graft). Usage : fichier créé dans un clone, regreffé sans reconstruire les 4 037 liens. | 0 ; 1 | fichier ajouté dans un clone visible après `graft --scion` ; autres feuilles non recréées (inode) ; conflit et annulation |
| E5 | `scion git` (inchangée en surface) | La sortie standard de git est réécrite sur stdout ; en échec, le stderr complet de git sur stderr (aujourd'hui : dernière ligne seulement, avec `-v`). Sortie bufferisée (pas de pager ni de couleur). | 0 ; 1 ; 2 (inchangés) | stdout de `log -1 --format=%s` affiché ; stderr d'une commande en échec affiché |
| E6 | `graft` (toutes formes) | Cas 1 et 2 : conflits signalés avec leurs deux origines, code 1, annulation complète ; jamais d'écriture à travers un lien du trunk (un répertoire du trunk doit être un vrai répertoire). Cas 3 : origine exacte dans le message. | 1 | les trois cas du §1 ; clones propres après échec |

Remarque NF-2 : aucune de ces commandes ne connaît Lepton ; la correspondance greffon Lepton →
clé scion (`lepton@famille::stm32f4xx`, …) reste dans l'outil `lepton`.

Enchaînements pour ENV-8 (GRA-4) :
- ajout : `seed-scion-add` → `seed-clone` → `graft --scion` ;
- retrait : `seed-scion-remove` → `graft-remove [--purge]` ;
- remplacement : `seed-scion-add --replace` → `graft-remove` → `seed-clone` → `graft --scion`.

## 3. `INSTALL_LAYOUT` de `rootstock-install` (E7)

`rootstock-install` crée `depots/origin/scion/sources` et
`depots/generation/building/scion/building/{projects,staging/lib,output}`, attendus par la graine
Lepton (`lepton building * depots/generation/building`). Options :

| Option | Effet |
| --- | --- |
| A — conserver en 0.5.1 | Aucune rupture ; couplage signalé, résorption à une version ultérieure |
| B — option `--bare` | Layout conservé par défaut, `--bare` crée signature et trunk seuls ; l'outil `lepton` pourra créer lui-même ce dont la graine a besoin |
| C — retrait | Rupture : la graine Lepton doit fournir `building` autrement (ex. dépôt local créé par `lepton seed new`) |

Recommandation : A (critère NF-2 limité au code fonctionnel, PA-2 Q7 ; aucun nom propre à Lepton
dans le code).

## 4. Version, branche, tests

- Version cible proposée : **0.5.1.0** (ajouts compatibles, corrections ; schéma à 4 nombres de
  0.5.0.1). Seule source : `scion/__init__.py`. `CHANGELOG.md` et `README.md` mis à jour.
- Branche `devenv/env-7` de `<SEED_SCIONS>` : depuis `master` e0adb2c recommandé (tag + doc
  seulement, dont les routes d'installation du README), au lieu du tag `0.5.0.1` du fichier d'étape.
- pytest absent de Python 3.11.5. Les tests sont `unittest`, compatibles pytest
  (`tests/support.py`). Options : critère « pytest vert » remplacé par
  `python3 -m unittest discover -s tests` ; ou environnement virtuel de test hors dépôt
  (`~/lepton-tools-dev/venv-seed-scions`) avec pytest épinglé.
- Installation après tag (PA-P) : `pipx install --force "git+file://<SEED_SCIONS>@0.5.1.0"`.

## 5. Décisions PA-8 (utilisateur, 2026-10-13)

- E1 à E6 retenues telles que décrites au §2.
- E7 : option B — `scion rootstock-install --bare` crée la signature et le trunk seuls ; sans
  `--bare`, layout inchangé.
- Version 0.5.1.0 ; branche `devenv/env-7` depuis `master` e0adb2c.
- Critère de test : `python3 -m unittest discover -s tests` (pytest non installé).

## 6. Réalisation et validation (2026-10-13)

Commits de `<SEED_SCIONS>` sur `devenv/env-7` (depuis `master` e0adb2c), fusionnés dans `master`
(79f4f96, tag annoté `0.5.1.0`) :

| Commit | Objet |
| --- | --- |
| 1fc3096 | E6 : conflits fichier / répertoire, greffe factorisée (`_graft_entries`) |
| 6cbcd05 | E5 : sortie de `scion git` (`gitops.run_verbatim`, flux portés par `GitError`) |
| 8c8064d | E4 `graft --scion`, E3 `graft-remove [--purge] [--force]` (un seul commit : code de retrait commun `_unlink`, `_prune`) |
| ecccbb2 | E1 `seed-scion-add [--replace]`, E2 `seed-scion-remove` (module `scion/seed.py`, `model.rewrite_key`) |
| 0b9f19d | E7 : `rootstock-install --bare` |
| 0c2fe0c | test du remplacement de bout en bout |
| b2b2014 | version 0.5.1.0, `CHANGELOG.md`, `README.md` |

Écart à la proposition : E3 `--force` porte sur les fichiers réguliers du trunk (même règle
qu'`ungraft`) ; les fichiers réguliers ne sont jamais supprimés.

| Critère | Résultat |
| --- | --- |
| Tests | `python3 -m unittest discover -s tests` : 104 tests, 1 ignoré (réseau), verts ; 69 d'origine inchangés hors numéro de version (`test_cli.py`) |
| Contre-épreuve E6 | les 3 tests de conflit échouent sur le code 0.5.0.1 (2 échecs, 1 erreur) |
| NF-2 | `grep -ri lepton scion/` : `__init__.py` `__url__` et `__email__` seulement (métadonnées tolérées, PA-2 Q7) ; aucun `shell=True` ni `os.system` |
| Copie du rootstock (code non installé) | greffe complète : 4 037 feuilles, cibles identiques à `<ROOTSTOCK>` ; `graft --scion lepton@bsp::nucleo-f429zi` : 8 feuilles, autres liens non recréés ; `graft-remove` : 4 029 feuilles, 8 lignes, aucun lien cassé ; `--purge` d'un greffon local refusé (code 1) ; clones propres |
| Installation | `scion version` = 0.5.1.0 ; `direct_url.json` : commit 79f4f96, révision `0.5.1.0` ; modules identiques au dépôt |
| `<ROOTSTOCK>` réel | `scion graft` : code 0, liste greffée inchangée (9 lignes), 4 037 feuilles, 0 fichier régulier, 0 lien cassé, cibles identiques à avant ; clones propres |

Constat hors périmètre : 26 `.DS_Store` du Finder, ignorés par git dans les clones, sont greffés
comme feuilles (comportement identique en 0.5.0.1).
