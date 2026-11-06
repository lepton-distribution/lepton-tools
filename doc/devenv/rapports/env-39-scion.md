# ENV-39 — scion : projection d'un dépôt tiers

Spécification : `<SEED_SCIONS>/doc/projection-miroir.md`, partie A (règles P-*), validée au PA-64.
Cas d'épreuve et plan de tests : `rapports/env-38-projection.md` §2.1 et §3.

## 1. Audit (lecture seule) — état au PA-65

Références : `<SEED_SCIONS>` `devenv/env-39` = `master` 9f2f67d (tag `0.5.4.0` sur 99aa973 ; la
tête n'ajoute que la spécification). scion installé : 0.5.4.0. Base de tests :
`~/lepton-tools-dev/venv-lepton-tools/bin/python -m pytest -q` → **158 réussis, 1 sauté**
(`test_network.py`), 146 s.

### 1.1 Code touché

| Module | Aujourd'hui | À faire pour la projection |
| --- | --- | --- |
| `model.py` | lecteurs indulgents (`_lines` : lignes courtes ignorées, pas de numéro de ligne) ; `GraftedEntry` à 5 colonnes | 6ᵉ colonne `carrier` (P-C2, P-P3) ; lecteurs avec numéro de ligne pour les `.scion/` porteurs et les messages (A.12) ; formats existants inchangés |
| nouveau `projection.py` | — | lecture stricte de `.scion.projections` (P-F1, P-F2) ; grammaire des motifs (P-M1-M3) et des destinations (P-T1-T4) ; résolution d'une clé sur la liste git (P-M4, P-M5, P-X*, P-R*) avec erreurs collectées ; contrôle de casse (P-K2) |
| `gitops.py` | `clone` complet puis `checkout <version>` ; pas de lecture d'arbre | `clone_partial` (`--filter=blob:none --no-checkout`, `checkout --detach`) ; `ls_tree` (`-r -z`, modes 100644/100755/120000/160000) ; `is_full_sha` ; `fetch` déjà présent |
| `graft.py` `sync`, `_wanted`, `_fetch` | une graine ; clone complet ; `stem/` exigé | après les scions de la graine, lecture des porteurs (P-P1-P-P4) ; clone partiel des clés projetées (P-V2) ; `scion/` non exigé pour une clé projetée (P-D2) ; refus 5ᵉ colonne, branche, `*`, `?` (P-D2, P-V1) |
| `graft.py` `clone_updates`, `_check_clone` | branche ou tag ; un commit rend « introuvable » (C1 d'ENV-38) | contrôle d'une clé projetée : tag (règle 0.5.4.0) ou commit (`HEAD` = commit, `fetch` si absent) ; jamais d'avance (P-V4) ; clones des porteurs relus après l'avance (P-P5) |
| `graft.py` `_graft_entries` | parcours du disque `_walk(stem)`, correspondance identité, liens créés au fil du parcours | table (source, chemin du trunk) pour une clé projetée ; pré-passe : état du clone (P-E1), casse sur l'ensemble des chemins prévus (P-K2) ; conflits inchangés (P-G2) ; pas de filtre des ignorés (P-G4) |
| `graft.py` `_owner`, `_unlink`, `_prune`, `remove`, `graft_scions` | propriété d'un répertoire par `(stem/r).is_dir()` ; liens par préfixe de `stem` | propriété par la table pour une clé projetée (P-G3) ; `graft-remove <porteur>` retire ses clés projetées (P-P6) ; `graft --scion <clé projetée>` (P-G5) |
| `cli.py` | `rootstock-information` compte la liste greffée | ligne des clés projetées (A.11) ; `-v` par ligne de projection (A.12) ; `git --key` fonctionne déjà (cwd = racine du clone) |
| `seed.py` | `seed-scion-add/remove` | inchangé (A.11, Q16) |

Tests existants concernés : aucun ne change d'attendu (P-C1). `test_graft.py` (oracle 0.4.1.3) et
`test_clone_versions.py` (contrôles 0.5.4.0) sont la garde de non-régression. Nouveaux tests :
`tests/test_projection.py`, un cas nommé par ligne P-* et A.11/A.12 du plan d'ENV-38 §3 (≈ 70),
fixture d'un dépôt tiers sans `scion/` (tags, commit sans tag, non suivi, sous-module, lien
committé, nom à blanc) ajoutée à `make_fixture.py`.

### 1.2 Essais techniques (bac à sable, hors dépôts)
- `git clone --filter=blob:none --no-checkout file://localhost/<tiers>/cmsis_device_f4` puis
  `checkout --detach 3c77349…` : `HEAD` = 3c77349, `remote.origin.promisor` = true, `ls-tree -r`
  lisible, `status --porcelain --untracked-files=no` vide. Sur `file://`, git avertit « filtering
  not recognized by server, ignoring » et clone en entier : sans effet sur le résultat.

### 1.3 Écarts et précisions relevés (proposés au PA-65)

| # | Règle | Constat | Proposition |
| --- | --- | --- | --- |
| E1 | P-P3, P-V5, `_wanted` | La règle « version greffée plus récente conservée » compare des versions ; un commit (40 hex) ne se compare pas (`compare` rendrait un ordre arbitraire), et la projection doit suivre son porteur | Pour une clé projetée, la version déclarée remplace toujours la version greffée |
| E2 | P-V2, P-G3 | Deux clés projetées de même `prefix` et version partagent le clone : la propriété d'un lien par préfixe du clone ne les distingue pas ; une clé projetée et un scion ordinaire de même `shelf/prefix/version` partageraient aussi le clone (la racine projetée préfixe le `stem` ordinaire) | Propriété d'un lien d'une clé projetée = cible sous la racine du clone **et** chemin du trunk dans la table de la clé ; un lien du clone qui n'est dans aucune table est retiré par la regreffe de toute clé de ce clone. Clone partagé entre une clé projetée et un scion ordinaire : erreur à la résolution |
| E3 | P-P5 | Silence : clé projetée qu'un porteur avancé ne déclare plus. Pour une graine, une clé retirée reste dans la liste greffée (0.5.4.0) | Question au PA-65 |
| E4 | P-T4 | P-T4 interdit `.scion` dans la destination ; un motif `**` peut produire un chemin du trunk qui contient `.scion` (fichier amont sous `x/.scion/`), ou `.scion.grafted.list` à la racine | P-T4 s'applique au chemin du trunk complet : erreur qui nomme la ligne et le fichier |
| E5 | P-V1 | Tag ou branche ne se distinguent qu'une fois le dépôt cloné | Résolution après clonage : `refs/tags/<v>` → tag (même si une branche porte le nom) ; 40 hex → commit ; sinon erreur. Le clone partiel reste en place, comme aujourd'hui un clone de version introuvable |
| E6 | P-V4, A.11 | « Contrôles avant toute modification » : les clones projetés d'un porteur avancé ne sont connus qu'après l'avance | Clones projetés contrôlés avec ceux de la graine avant toute avance ; une version nouvelle est clonée à la synchronisation ; un clone déjà présent pour la version nouvelle est contrôlé à la greffe (P-E1, trunk rétabli) |
| E7 | P-V4 | « un `git fetch` est tenté » | `git fetch --quiet origin` (toutes les références), puis nouveau contrôle ; pas de fetch par empreinte (dépend du serveur) |
| E8 | A.11, P-C1 | `rootstock-information` « compte aussi les clés projetées » ; P-C1 impose une sortie identique sans projection | `scions grafted: N` inchangé (projetées comprises) ; ligne `scions projected: k` ajoutée seulement si k > 0 |
| E9 | P-P4 | Double déclaration identique : quel `.scion/` en 6ᵉ colonne ? | Le premier dans l'ordre P-P3 (la graine avant les porteurs ; 6ᵉ colonne absente si c'est la graine) |
| E10 | P-K2 | Comparaison de casse non précisée ; `graft --scion` ne voit qu'une partie des scions | `str.casefold()` par segment ; `graft --scion` compare aussi aux chemins déjà présents dans le trunk |
| E11 | P-E1 | Moment du contrôle | Avant le dégreffage : le trunk n'est pas touché (compatible avec « trunk rétabli ») |
| E12 | tâche §3 de l'étape | `file:///…` n'a pas de `netloc` : scion le lit comme un chemin local (P-V3, utilisé tel quel, `HEAD` des clones de `tiers/` imposé) | Essai à blanc avec `file://localhost/<chemin>` : clones créés dans `depots/tiers/…` de la copie, comme le ferait une URL `https://` |

### 1.4 Effets sur lepton
Aucun traité ici (PA-63 Q13, `rapports/env-38-projection.md` §4 : tous portés par ENV-41).
`SCION_MIN_VERSION` reste (0, 5, 4, 0). Le critère « toutes les références de version désignent
la même version » vise les références d'installation (`SCION_REF`, documentation), pas le minimum
requis.

### 1.5 Décisions du PA-65 (utilisateur, 2026-11-06)
- E1, E2, E4 à E12 acceptés tels quels ; reportés dans la spécification (P-T4, P-K2, P-V1, P-V2,
  P-V4, nouvelle P-V6, P-E1, P-P4, P-P5, P-G3, A.11), commit séparé de `<SEED_SCIONS>`.
- E3 : clé projetée que son porteur ne déclare plus → retirée de la liste greffée, avec un
  message (nouvelle règle P-P7).
- Version 0.6.0.0 ; `SCION_REF` relevé ici ; `SCION_MIN_VERSION` inchangé ; aucun effet sur lepton.
