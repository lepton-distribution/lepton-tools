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
