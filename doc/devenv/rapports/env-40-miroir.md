# ENV-40 — scion : miroir de conservation

Spécification : `<SEED_SCIONS>/doc/projection-miroir.md`, partie B (règles M-D1 à M-D5, M-C1 à
M-C6, M-R1 à M-R9, M-K1, M-K2). Plan de tests : `rapports/env-38-projection.md` §3. Point de
départ : seed.scions `master` f526f25, tag `0.6.0.0` ; version visée 0.6.1.0 (PA-63 Q13).

## 1. Audit (lecture seule) — état au PA-67

### 1.1 Code de départ

| Élément | État en 0.6.0.0 | À créer ou modifier |
| --- | --- | --- |
| `scion/model.py` | `fields()`, `numbered_lines()` ; constantes des formats ; aucun `.scion.mirrors` | constante `MIRRORS` ; lecture stricte (M-D3) |
| `scion/cli.py` | 14 commandes, `ScionError` → code 1, `GitError` → code 2 | sous-commande `mirror-sync` (M-C1, M-C6) |
| `scion/gitops.py` | `run()` lève `GitError` (code 2) ; `clone`, `fetch`, `ls-remote` des tags, `rev-parse` | `clone --mirror`, fetch dans un espace séparé, `merge-base --is-ancestor`, `for-each-ref`, `push --porcelain` de refspecs nommées |
| `scion/graft.py` | `seeds()` (graines de la liste greffée) ; porteurs = clones dont `scion/.scion/` a un `.scion.projections` (`_carried`, `_carrier_dot`) ; `_fetch`, `_pinned`, `_check_clone`, `_check_projected_clone` (échecs de clone et de version) | suggestion de M-D5 dans ces messages |
| nouveau `scion/mirror.py` | — | déclaration, dépôt de travail, comparaison par référence, envoi, bilan |
| aucun code | « mirror » : 0 occurrence dans `scion/` | — |

Réutilisable : `model.numbered_lines`, `graft.is_remote` (une URL distante a un hôte ;
`file://localhost/…` en est une, `file:///…` non, comme P-V3), `graft.seeds`,
`graft._carrier_dot`, `projection.has_projections`, `rootstock.Rootstock.depots`, `errors`.
Base de tests : 229 réussis, 1 sauté (fin d'ENV-39), `tests/support.py` (CLI en processus).

### 1.2 Les deux amonts (`git ls-remote`, 2026-11-06)

Relevés complets : `rapports/env-40-miroir/amont-*.ls-remote.txt`.

| Amont | Branches | Tags (tous annotés) | Autres références (hors M-C3) | Épinglé | Taille `.git` |
| --- | --- | --- | --- | --- | --- |
| `STMicroelectronics/stm32f4xx-hal-driver` | `master` 6ef30cf | 15 (`v1.7.6` à `v1.8.6`) | `HEAD`, `refs/for/master`, 15 `refs/pull/*` | tag `v1.8.5` (objet 6b55d2c) → b6f0ed3, atteignable depuis `master` | 4,0 Mo |
| `STMicroelectronics/cmsis_device_f4` | `master` 9192c7b | 8 (`v2.6.3` à `v2.6.11`) | `HEAD`, 5 `refs/pull/*` | 3c77349, sans tag (aucun tag ne le contient), atteignable depuis `master` | 2,3 Mo |

Les clones de `~/lepton-tools-dev/tiers/` sont à jour (`origin/master` = tête de l'amont).
Observation : `v1.8.6` existe en amont ; ENV-41 garde `v1.8.5` (hors étape).

### 1.3 Écarts, ambiguïtés et propositions

| ID | Règle | Constat | Proposition |
| --- | --- | --- | --- |
| E1 | M-C1, M-D1 | « porteurs greffés » : P-C3 ne fait porteur qu'un `.scion/` qui a un `.scion.projections`. | Miroirs lus dans le `.scion/` des graines et des porteurs (au sens de P-C3), rien d'autre. Avec `--seed` : cette graine et les porteurs de la liste greffée qui en viennent (5ᵉ colonne = cette graine). |
| E2 | M-D1 | « Il sert au `.scion/` qui déclare une source pointant vers ce miroir » : rien ne dit si un miroir qu'aucune source ne désigne est admis. | Admis, sans message. Cela permet de remplir un miroir avant que les graines y pointent (cas de la première synchronisation, E13). |
| E3 | M-D2, M-D5 | M-D5 suppose que la greffe sait qu'une URL est un miroir, alors que M-D2 dit qu'elle ne lit jamais `.scion.mirrors`. | La greffe lit le `.scion.mirrors` du `.scion/` qui déclare la source, seulement pour compléter un message d'échec ; jamais pour choisir une URL. Lecture tolérante à cet endroit (ligne mal formée ignorée), stricte dans `mirror-sync`. Messages concernés : échec du clonage, version, tag ou commit introuvable (`_fetch`, `_pinned`, `_check_clone`, `_check_projected_clone`). P-C1 reste tenu : sans `.scion.mirrors`, messages identiques. |
| E4 | M-C2 | `git clone --mirror` pose `remote.origin.mirror=true` : un `git push` lancé à la main dans le dépôt de travail serait un `push --mirror`. Le refspec `+refs/*:refs/*` ramène aussi `refs/pull/*`. | Après le clonage : `remote.origin.mirror` retiré, refspec de `origin` restreint à `refs/heads/*` et `refs/tags/*` (M-C3). Remote `amont` avec `+refs/heads/*:refs/amont/heads/*` et `+refs/tags/*:refs/amont/tags/*`, `tagOpt --no-tags`. Le refspec suit l'URL de l'amont déclarée (mise à jour si elle change). |
| E5 | M-R5, M-R9 | Une référence supprimée dans l'amont ne se voit que si `refs/amont/*` est purgé. | `git fetch --prune amont` : la purge ne touche que `refs/amont/*` du dépôt de travail local, jamais le miroir (M-K2 tenu). |
| E6 | M-R5, M-R9, M-K1 | Le dépôt de travail ne distingue pas « supprimée dans l'amont » de « ajoutée dans le miroir seul ». Une branche ou un tag supprimé en amont donne un signalement, donc un code 1, à **chaque** passe suivante, sans fin. | Comportement littéral : signalement « présente dans le miroir, absente de l'amont » à chaque passe, code 1. Pas de mécanisme d'acquittement (hors spécification). |
| E7 | M-R7, M-R8 | « même objet » : un tag annoté recréé sur le même commit a un autre objet. | Comparaison de l'objet du tag (strict). Message M-R8 : les deux commits, et « même commit, objet de tag différent » le cas échéant. Non propagé dans les deux cas. |
| E8 | M-R4 | Un miroir en avance sur l'amont (amont ancêtre du miroir) n'est pas nommé. | Même cas que M-R4 : le miroir n'est pas ancêtre de l'amont → non envoyé, signalé (« le miroir n'est pas un ancêtre de l'amont »). |
| E9 | M-C4 | « une à une » : un `git push` par référence, ou un seul `git push` qui nomme chaque référence ? | Un `git push --porcelain <url du miroir> <refspec>…` par miroir, chaque refspec nommée (`refs/amont/heads/B:refs/heads/B`, `refs/amont/tags/T:refs/tags/T`), sans `+`, sans `--atomic`. Une référence refusée par le serveur est un signalement ; les autres comptent comme envoyées. Envoi à l'URL, jamais au remote `origin`. |
| E10 | M-C4, M-C5 | Authentification : la graine désignera le miroir par son URL `https://` (lecture sans identifiants, comme les autres greffons). `mirror-sync` envoie à cette URL. Sur ce Mac : aucun `insteadOf`, seul `credential.helper=osxkeychain` (système). Les envois précédents passaient par une URL `ssh://` explicite. | scion ne règle rien (M-C4). L'utilisateur ajoute, avant la publication, `git config --global url."ssh://git@github.com/".pushInsteadOf "https://github.com/"` (ou `gh auth setup-git`). Choix de l'utilisateur au PA-68. |
| E11 | M-C5, M-K1 | Partage entre « inaccessible » (code 1) et « échec git inattendu » (code 2) non défini. | Code 1 : échec réseau ou d'accès sur le miroir ou l'amont (clonage, `fetch`, `ls-remote`, `push` refusé) ; ce miroir est laissé, les autres sont traités. Code 2 : échec local (dépôt de travail illisible, git absent), arrêt. |
| E12 | M-C1, M-K1 | Code d'une URL donnée en argument et inconnue : M-K1 cite « usage incorrect » (2) et « erreur de déclaration » (1). | Code 2 (usage incorrect), signalé avant tout accès réseau, toutes les URL inconnues ensemble. |
| E13 | M-C1 | Première synchronisation des miroirs F4 publiés : `<ROOTSTOCK>` n'a aucun `.scion.mirrors` avant ENV-41 (la famille ne porte pas encore ses projections). | Graine de publication hors des greffons : `~/lepton-tools-dev/essais/env-40-publication/` (rootstock `--bare`, graine locale dont le `.scion/` ne contient que `.scion.mirrors`), `mirror-sync --seed`. ENV-41 recopie les deux lignes dans le `scion/.scion/` de `family-stm32f4xx` ; les passes suivantes partent de `<ROOTSTOCK>`. |
| E14 | M-C2 | Chemin de `depots/.mirrors/<hôte>/<chemin>` : suffixe `.git`, port, utilisateur (`git@`). | Hôte sans utilisateur ni port, chemin de l'URL tel quel (suffixe `.git` gardé s'il y est) : `depots/.mirrors/github.com/lepton-distribution/<nom>.git`. |
| E15 | M-C6 | `--dry-run` et le dépôt de travail. | `--dry-run` crée ou rafraîchit le dépôt de travail local (lecture réseau) ; aucun `push`. |
| E16 | M-K1 | Forme du bilan. | Une ligne par miroir : `miroir <url> : <n> référence(s) envoyée(s), <m> signalement(s)` (`--dry-run` : « à envoyer »), puis code de retour. Messages par référence : info (M-R1, M-R2, M-R6), `-v` (M-R3, M-R7), avertissement (M-R4, M-R5, M-R8, M-R9). |
| E17 | critère d'étape | `grep -ri lepton scion/` n'est pas nul avant ENV-40 (URL et adresse de `scion/__init__.py`). | Critère retenu : le diff d'ENV-40 n'ajoute aucune occurrence. |

### 1.4 Version et références

- Version : **0.6.1.0** (PA-63 Q13, ENV-39 livrée avant).
- `SCION_MIN_VERSION` de lepton : inchangé (0, 5, 4, 0) ; relevé en ENV-41 (PA-63 Q13).
- `SCION_REF` (`install-vscodium.sh`, `install-{macos,debian}.sh` du clone noyau) : proposé à
  0.6.1.0 dans cette étape, comme en ENV-39 (critère « toutes les références désignent la même
  version »), ce qui crée `devenv/env-40` dans le clone noyau.

### 1.5 Décisions du PA-67

Utilisateur, 2026-11-06 (consignées dans `DEVENV-STATUS.md` §Décisions) :
- E1 à E17 acceptés tels quels ; report dans la spécification par un commit séparé.
- E6 : comportement littéral (signalement et code 1 à chaque passe, sans acquittement).
- E13 : graine de publication d'essai `~/lepton-tools-dev/essais/env-40-publication/`.
- Version 0.6.1.0 ; `SCION_REF` relevé ici (lepton-tools, clone noyau) ; `SCION_MIN_VERSION`
  inchangé jusqu'à ENV-41.

## 2. Implémentation (`<SEED_SCIONS>`, `devenv/env-40`)

| Commit | Contenu |
| --- | --- |
| 57061f2 | spécification : précisions du PA-67 (M-D1, M-D4, M-D5, M-C1, M-C2, M-C4, M-C6, M-R4, M-R8, M-K1) |
| 4d113a3 | déclaration `.scion.mirrors` (`scion/mirror.py` : `read_mirrors`, `declared`, `upstream_of`, `hint`), `MIRRORS` (`model.py`), suggestion M-D5 dans `graft.py` (`_fetch`, `_check_clone`, `_check_projected_clone`) ; tests de la greffe |
| b6db24c | `mirror-sync` (`cli.py`), dépôt de travail et règles par référence (`mirror.py` : `sync`, `_plan`, `_push`), `gitops.refs`, `gitops.is_ancestor`, `UsageError` (code 2) ; tests M-D1, M-D3, M-D4, M-C*, M-R*, M-K* |
| 9b0bb9a | version 0.6.1.0 (`__init__.py`, `CHANGELOG.md`, `README.md`) |
| 4502a70 | tests M-R4 et M-R8 renforcés après le contrôle par mutation |

- Écart de procédure : deux commits de fond (déclaration, commande) au lieu d'un par règle ;
  `mirror.py` les porte tous deux. Les tests ont été écrits avant le code (34 échecs sur 36 avant
  implémentation ; les 2 qui passaient vérifient l'absence de changement de la greffe).
- CLI : `mirror-sync [rootstock] [--seed] [--dry-run] [url…]`. Le premier argument positionnel
  est le rootstock s'il n'est pas une URL distante ; les positionnels placés après une option sont
  repris par `parse_known_args` (les autres commandes gardent l'erreur « unrecognized arguments »
  d'argparse, à l'identique).
- `graft.is_remote` est désormais `mirror.is_remote` (même définition).
- NF-2 : `git diff f526f25 -- scion/ | grep -i '^+.*lepton'` → 0 ligne (E17).

Tests : `~/lepton-tools-dev/venv-lepton-tools/bin/python -m pytest -q` dans `<SEED_SCIONS>` →
**265 réussis, 1 sauté** (229 + 36 de `tests/test_mirror.py`), 5 min 16 s. Un test par cas nommé
du plan d'ENV-38 §3 :

| Règle | Test(s) |
| --- | --- |
| M-D1 | `test_mirrors_dans_porteur`, `test_ordinaire_non_porteur_ignore` |
| M-D2 | `test_greffe_ne_lit_pas_mirrors` |
| M-D3 | `test_ligne_mirrors_mal_formee` |
| M-D4 | `test_miroir_deux_amonts_erreur`, `test_meme_amont_deux_miroirs_admis` |
| M-D5 | `test_echec_clone_miroir_suggere_mirror_sync`, `test_echec_clone_miroir_absent_suggere_mirror_sync`, `test_version_introuvable_dans_clone_suggere_mirror_sync`, `test_echec_clone_sans_miroir_message_inchange` (P-C1) |
| M-C1 | `test_mirror_sync_url_inconnue_erreur_avant_tout`, `test_mirror_sync_selection`, `test_rootstock_en_argument_avant_les_url`, `test_sans_miroir_declare` |
| M-C2 | `test_depot_de_travail_refs_amont_separees` |
| M-C3 | `test_seules_branches_et_tags` |
| M-C4 | `test_push_sans_force_ni_suppression`, `test_reference_refusee_signalee` |
| M-C5 | `test_miroir_inaccessible_signale_les_autres_traites`, `test_amont_inaccessible_signale` |
| M-C6 | `test_dry_run_rien_envoye` |
| M-R1 à M-R9 | `test_premiere_synchronisation_miroir_vide`, `test_branche_nouvelle`, `test_branche_avance_rapide`, `test_branche_identique`, `test_branche_reecrite_non_envoyee`, `test_miroir_en_avance_non_envoye` (E8), `test_branche_supprimee_conservee` (E6), `test_tag_nouveau`, `test_tag_identique`, `test_tag_deplace_non_propage`, `test_tag_recree_meme_commit_non_propage` (E7), `test_tag_supprime_conserve` |
| M-K1 | `test_codes_de_retour_mirror_sync` |
| M-K2 | `test_rien_supprime_ni_reecrit_dans_miroir` |
| P-C1 | `test_grafted_list_inchangee` |

Contrôle par mutation (copie du dépôt, `tests/test_mirror.py`) : 8 mutations (M-R4 envoyée, M-R8
propagée, `--prune` retiré, suggestion M-D5 vide, URL inconnue ignorée, M-D4 sans contrôle,
`remote.origin.mirror` conservé, code toujours 0). 7 détectées d'emblée. La mutation M-R8 ne
l'était pas : git refuse lui-même de mettre à jour un tag existant sans `+`, et le miroir restait
intact. Les tests M-R4 et M-R8 vérifient depuis qu'aucun envoi n'est tenté (4502a70) ; mutation
alors détectée.

## 3. Essai local (`~/lepton-tools-dev/essais/env-40-miroirs/`)

Préparation : copies nues des clones `~/lepton-tools-dev/tiers/stm32f4xx-hal-driver` et
`…/cmsis_device_f4` (`git clone --mirror`, `refs/remotes/*` retirées : branches et tags seuls)
dans `amonts/` ; deux miroirs nus vides dans `miroirs/` ; rootstock `rootstock/`
(`scion rootstock-install --bare`) ; graine `graine/scion/.scion/.scion.mirrors` (2 lignes
`file://localhost/…`). scion lancé depuis les sources (`PYTHONPATH=<SEED_SCIONS> python3 -m
scion.cli`, `scion version` → 0.6.1.0). Relevés : `rapports/env-40-miroir/essai/`.

| Passe | Commande | Résultat |
| --- | --- | --- |
| 1 | `mirror-sync --seed graine --dry-run` | code 0 ; 16 et 9 références « à envoyer », 0 signalement ; miroirs toujours vides |
| 2 | `mirror-sync --seed graine` | code 0 ; 16 et 9 références envoyées |
| contrôle | `git ls-remote` des branches et tags | miroir = copie d'amont = relevé GitHub du §1.2 (`cmp`), pour les deux dépôts ; `b6f0ed3…` présent (commit) ; `3c77349…` ancêtre de `master` du miroir |
| 3 | même commande, rien de changé | code 0 ; 0 envoyée, 0 signalement (`passe-2.log`) |
| 4 | `v1.8.5` déplacé dans la copie d'amont (`tag -f -a`, b6f0ed3 → 6ef30cf), puis même commande | code 1 ; « tag « v1.8.5 » déplacé dans l'amont, non propagé : miroir b6f0ed3, amont 6ef30cf » ; `git ls-remote` du miroir identique à avant (`passe-3-tag-deplace.log`) |

La copie d'amont `amonts/stm32f4xx-hal-driver.git` garde son `v1.8.5` déplacé : elle ne sert qu'à
cet essai. Rien n'a été créé sur GitHub.

### Références de version (PA-67)

- lepton-tools `devenv/env-40` 311b18a : `SCION_REF` d'`install-vscodium.sh` et `README.md` à
  0.6.1.0 ; `shellcheck` conforme.
- Clone noyau `devenv/env-40` (depuis `master` 00911b9) 61ce18d : `install-{macos,debian}.sh`,
  `README.md`, `README-PAQUET.md`, `doc/BUILDING.md` à 0.6.1.0 ; `shellcheck` conforme. Trunk :
  aucun fichier régulier, aucun lien cassé.
- Ces références désignent le tag `0.6.1.0` de GitHub, publié au PA-68.
