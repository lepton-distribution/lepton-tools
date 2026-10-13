# ENV-2 — Audit de scion 0.5.0.1

Relevé du 2026-10-13, lecture seule. Chemins de code relatifs à `<SEED_SCIONS>`
(`~/lepton-tools-dev/seed.scions`). Les tests de `seed.scions` n'ont pas été lancés (ils créent des
répertoires temporaires ; hors périmètre lecture seule).

## 0. Version

| Contrôle | Résultat |
| --- | --- |
| `scion version` | `scion version: 0.5.0.1` (Python 3.11.5) |
| `git -C <SEED_SCIONS> describe --tags` | `0.5.0.1-4-ge0adb2c` ; tag `0.5.0.1` = `54dc319` |
| `git diff 0.5.0.1 master --stat` | `.gitignore`, `README.md`, `doc/migration/MIGRATION-STATUS.md` seulement ; rien sous `scion/` ni `tests/` |
| `~/.local/bin/scion` | venv pipx installé depuis la révision `0.5.0.1` (`direct_url.json`, commit `54dc3193…`) ; modules identiques à `scion/*.py` (`diff -q`) |

## 1. Modèle

| Notion | Définition (code) |
| --- | --- |
| rootstock | Répertoire portant `.scion.rootstock.signature` ; trouvé en remontant depuis le cwd ou par argument (`scion/rootstock.py:17`, `:78-88`) |
| trunk | Sous-répertoire contenant `.scion.grafted.list` (`find_trunk`, `rootstock.py:97-114`) |
| seed | Dépôt ou répertoire contenant `scion/.scion/` avec `.scion.ramifications` et `.scion.sources.list` (`cli.py:34-45`) |
| scion | `shelf prefix[::suffix]` + version ; contenu greffé = `<emplacement>/<chemin>/scion/` (`model.py:61-82`, `graft.py:62,79`) |
| clone | `depots/<shelf>/<prefix>/<version>` pour un scion distant (`graft.py:57-59`) |
| greffe | Répertoires réels, feuilles = liens symboliques relatifs ; `.scion/` ignorés ; lien versionné copié comme lien (`graft.py:1-6`, `:126-141`, `:200` ; `rootstock.py:130-136`) |

Fichiers d'état (colonnes séparées par blancs, `#` = commentaire, ligne trop courte ignorée sans
message — `model.py:21-26`, `:114-119`) :

| Fichier | Emplacement | Colonnes |
| --- | --- | --- |
| `.scion.rootstock.signature` | racine du rootstock | vide |
| `.scion.ramifications` | `<seed>/scion/.scion/` | `shelf name version` (`?` = plus haute, `*` = local) |
| `.scion.sources.list` | `<seed>/scion/.scion/` | `shelf name version emplacement [chemin]` |
| `.scion.grafted.list` | `<ROOTSTOCK>/trunk/` | `shelf name version chemin_local [.scion du seed]` ; écrit par `sync` (`graft.py:86`) |

Aucun autre état (pas de `~/.scion.settings/`, aucune variable d'environnement lue :
`CHANGELOG.md:25-27`, `rootstock.py:51-57`).

État réel de `~/lepton` :

```
# trunk/.scion.grafted.list
lepton original::tree master depots/lepton/original/master depots/lepton-seed.scions/original-tree/scion/.scion
lepton building * depots/generation/building depots/lepton-seed.scions/original-tree/scion/.scion

# depots/lepton-seed.scions/original-tree/scion/.scion/.scion.sources.list
lepton  original::tree  master  https://github.com/lepton-distribution/lepton-original-tree.scions.git
lepton  building  *  depots/generation/building
```

`depots/generation/building` est un répertoire local hors git. Trunk : 4019 liens, 0 lien absolu,
0 lien cassé, un seul fichier régulier (`.scion.grafted.list`).

## 2. Couverture des besoins

| Besoin | Couvert | Commande / implémentation | Contournement |
| --- | --- | --- | --- |
| a. Ajout / retrait d'un scion dans `.scion.sources.list` | **Non** | Aucune commande n'édite les listes (`graft-add`/`-remove` supprimés, `CHANGELOG.md:30-32`). `sync` parcourt `.scion.ramifications` (une ligne seulement dans `sources.list` n'est jamais greffée) et fusionne sans jamais retirer de clé (`graft.py:42-86`). | Ajout : éditer `sources.list` **et** `ramifications` du seed, puis `scion seed-update --seed <seed>` et `scion graft`. Retrait : retirer aussi la ligne de `trunk/.scion.grafted.list` (ou `graft-clean` puis `seed-update`). Le seed de `~/lepton` est un clone git : l'éditer le rend sale. |
| b. Regreffe d'un seul chemin | **Non** | `graft` sans argument de chemin : `cmd_graft` = `ungraft` complet puis `graft` complet (`cli.py:113-117`). | `scion graft` complet (4019 liens), ou lien relatif manuel, recréé au prochain `graft`. |
| c. Greffon local hors git | **Oui** | Version `*`, emplacement sans netloc → `rootstock.resolve(location)` (`graft.py:35-36`, `:61`) ; pas de fetch (`graft.py:74`, `:93`) ; `<chemin>/scion/` requis (`graft.py:79-84`). Déjà utilisé : `lepton building *`. | Piège : `file:///x` est pris pour un chemin local. |
| d. Regreffe idempotente après création d'un fichier dans un clone | **Oui** (reconstruction complète) | `graft` commence par `ungraft` : refuse tout fichier régulier du trunk hors `.scion.grafted.list` sauf `--force` (`graft.py:228-241`), supprime tous les liens et répertoires vides (`graft.py:242-251`), puis reparcourt chaque `scion/`. Résultat indépendant de l'ordre (`tests/test_graft.py:71-79`). | Un fichier régulier dans le trunk (y compris `.DS_Store` du Finder) bloque la regreffe. |
| e. Suppression propre d'un greffon | **Non** | `graft-clean` oublie tous les scions (`cli.py:125-129`, `graft.py:113-120`) ; clones jamais touchés (`graft.py:114`). | Retirer la ligne de `trunk/.scion.grafted.list` et du seed (sinon `seed-update`/`graft-update` la réinscrit), `scion graft`, supprimer le clone à la main. |

Note : `sync` conserve une version déjà greffée plus récente et ignore la nouvelle, avec un simple
message (`graft.py:65-71`).

## 3. Conflits

| Point | Comportement |
| --- | --- |
| Détection | Feuille dont la cible existe (`os.path.lexists`) → conflit `(chemin, premier, réclamant)` (`graft.py:195-199`) |
| Priorité | Aucune : tous les conflits collectés, échec code 1, annulation de ce que l'appel a créé (`graft.py:203-216`, `_rollback` `:157-164`) ; « premier gagne » supprimé (`CHANGELOG.md:46-48`) |
| Cas non couvert (déduit du code, non testé) | Fichier X dans A, répertoire X dans B : `FileExistsError` non capturée → trace Python, pas d'annulation (`graft.py:144-154`). Lien versionné vers répertoire X dans A, répertoire X dans B : `is_dir()` suit le lien → écritures à travers le lien, potentiellement dans un clone (`graft.py:146`). |

Conséquence pour ENV-6 : un greffon BSP ne peut pas surcharger un fichier du greffon noyau ; les
fichiers extraits doivent être retirés du noyau dans le même mouvement.

## 4. `scion git`

Bug confirmé : `gitops.run` capture stdout (`gitops.py:22-29`, renvoi `:40`) ; `cmd_git` ignore la
valeur (`cli.py:147`). stderr visible seulement avec `-v` ; en échec, dernière ligne seulement
(`gitops.py:32-39`). Tests limités aux codes de retour (`tests/test_cli.py:97-128`).
Contournement acquis : `git -C <clone> …`.

## 5. Chaînes propres à Lepton (NF-2)

| Emplacement | Nature |
| --- | --- |
| `scion/__init__.py:4,6`, `pyproject.toml:12,25` | Métadonnées (URL du projet, auteur) |
| `scion/rootstock.py:23-29` (`INSTALL_LAYOUT`) | **Couplage fonctionnel** : `rootstock-install` crée `depots/origin/scion/sources` et `depots/generation/building/scion/building/{projects,staging/lib,output}`, layout attendu par le seed Lepton (`building *`). Qualifié de générique par `CHANGELOG.md:35-38`. |
| `README.md:210-223`, `CHANGELOG.md` | Exemples documentaires |
| `tests/test_network.py:26`, `tests/test_seed.py`, `tests/test_model.py`, `tests/data/` | Jeux de tests sur le seed Lepton réel |

Aucune autre occurrence (`grep -i 'lepton|embos|kernel'` sous `scion/`).

## 6. Tests de seed.scions

`tests/test_cli.py` (21), `test_graft.py` (21), `test_model.py` (17), `test_seed.py` (9),
`test_network.py` (1, désactivé sans `SCION_TEST_NETWORK=1`). Fixture `tests/make_fixture.py` :
dépôts git locaux en `file://localhost`, répertoire temporaire supprimé en fin de test.
Lancement (`README.md:244-248`) : `python3 -m unittest discover -s tests` depuis `<SEED_SCIONS>`.
Non couverts : sortie de `scion git`, conflit fichier / répertoire, greffe partielle, retrait d'un
scion.

## Conclusion pour ENV-7

Évolutions candidates (génériques) : commande d'ajout / retrait d'un scion ; regreffe d'un chemin ;
suppression d'un greffon ; affichage de la sortie de `scion git` ; traitement propre du conflit
fichier / répertoire ; éventuellement sortie du layout `INSTALL_LAYOUT` de `rootstock-install`.
Déjà couverts : greffon local hors git, regreffe idempotente.
