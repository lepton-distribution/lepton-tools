# ENV-52 — scion : extraction partielle des clones projetés (D11)

Rapport d'étape. Session du 2026-11-12, Mac. seed.scions `devenv/env-52` (depuis `master` 7e8a0cc,
tag 0.6.2.0) ; lepton-tools `devenv/env-52` (depuis `main` 2dba564). git 2.50.1 (Apple Git-155).

## 1. Audit (lecture seule)

### 1.1 Clones projetés de `<ROOTSTOCK>` (relevé du 2026-11-12)

Lectures seulement : `git ls-files`, `git ls-tree -r -l HEAD`, `du`, `os.walk` sur le trunk
(liens dont la cible est sous le clone). Scripts : `env-52-scion/clones.py`, `env-52-scion/cone.py`
(copiés du répertoire de session).

| clone | suivis (ls-files ; dont sous-modules) | extraits | arbre extrait (disque) | `.git` | sources projetées = liens du trunk | répertoires parents des sources |
| --- | --- | --- | --- | --- | --- | --- |
| `cmsis-device-f4/3c77349…` | 152 | 152 | 25,9 Mo | 0,5 Mo | 6 | 1 |
| `cmsis-device-f7/v1.2.10` | 113 | 113 | 20,7 Mo | 0,4 Mo | 5 | 1 |
| `cmsis-device-wl/v1.4.0` | 79 | 79 | 4,8 Mo | 0,3 Mo | 6 | 2 |
| `stm32-mw-subghz-phy/v1.5.0` | 147 | 147 | 2,5 Mo | 0,6 Mo | 20 | 2 |
| `stm32cubewl/v1.6.0` | 8 962 (15) | 8 950 | 135,6 Mo | 24,3 Mo | 39 | 9 |
| `stm32f4xx-hal-driver/v1.8.5` | 209 | 209 | 10,5 Mo | 1,6 Mo | 200 | 2 |
| `stm32f7xx-hal-driver/v1.3.3` | 206 | 206 | 9,7 Mo | 1,6 Mo | 196 | 2 |
| `stm32wlxx-hal-driver/v1.6.0` | 168 | 168 | 7,4 Mo | 1,2 Mo | 157 | 2 |
| **total** | 10 036 | 10 024 | 217 Mo | 30 Mo | **629** (= projetés d'ENV-49) | |

Les 8 clones ont `core.ignoreCase=true`, `remote.origin.promisor=true`,
`partialclonefilter=blob:none`, et aucun réglage `core.sparseCheckout`. Les sources projetées sont
l'union des tables des clés qui partagent le clone (P-V2 : `stm32cubewl` porte `::utilities` et
`::radio-core-inc`). Le clone `stm32cubewl` a 21,7 Mio de paquets : il a reçu tous les blobs de
l'arbre extrait.

Ensemble extrait selon le mode (tailles des blobs, `ls-tree -l`) :

| clone | liste exacte (non-cône) | cône : parents des sources | extraction complète |
| --- | --- | --- | --- |
| `cmsis-device-f4` | 6 / 2,7 Mo | 31 / 24,5 Mo | 152 / 26,2 Mo |
| `cmsis-device-f7` | 5 / 1,4 Mo | 22 / 19,6 Mo | 113 / 20,9 Mo |
| `cmsis-device-wl` | 6 / 0,9 Mo | 70 / 4,6 Mo | 79 / 4,7 Mo |
| `stm32-mw-subghz-phy` | 20 / 0,3 Mo | 28 / 0,4 Mo | 147 / 2,3 Mo |
| `stm32cubewl` | 39 / 0,45 Mo | 103 / 1,6 Mo | 8 947 / 118,7 Mo |
| `stm32f4xx-hal-driver` | 200 / 10,0 Mo | 204 / 10,3 Mo | 209 / 10,3 Mo |
| `stm32f7xx-hal-driver` | 196 / 9,3 Mo | 200 / 9,4 Mo | 206 / 9,5 Mo |
| `stm32wlxx-hal-driver` | 157 / 7,2 Mo | 161 / 7,2 Mo | 168 / 7,3 Mo |
| **total** | 629 / 32,3 Mo | 819 / 77,6 Mo | 10 021 / 199,9 Mo |

Les deux modes traitent STM32CubeWL, le cas de D11 : 118,7 Mo extraits deviennent 1,6 Mo en cône,
0,45 Mo en liste exacte. Les écarts entre les deux modes viennent des répertoires `Include/` des
CMSIS device, qui contiennent les en-têtes de toutes les puces. Pour STM32CubeWL, les répertoires
parents des sources sont `Utilities/{conf,Fonts,lcd,lpm/tiny_lpm,misc,sequencer,timer,
trace/adv_trace}` et `Projects/NUCLEO-WL55JC/Applications/SubGHz_Phy/SubGHz_Phy_PingPong/Core/Inc`.
Avec les lignes actuelles, ce sont aussi les répertoires de base des motifs (§A.3), car aucun motif
ne parcourt plus large que ses fichiers.

### 1.2 Chemin du code (seed.scions 0.6.2.0)

- **Création** : `seed-add` et `seed-clone` passent par `graft.sync`. `seed-update` et
  `graft-update` passent par `graft.update_sources`, puis par `sync`.
  - `sync` appelle `_fetch` pour les scions de la graine. Il appelle ensuite `_carried`, qui relit
    les porteurs une fois clonés, puis `_fetch` pour les clés projetées.
  - Dans `_fetch` (`scion/graft.py:274`), pour chaque clone distant absent :
    `gitops.clone_partial` (`--filter=blob:none --no-checkout`), puis `_pinned` (tag ou commit,
    P-V1), puis `gitops.checkout_detached` (P-V2). L'arbre entier est extrait.
  - `seed-add` et `seed-clone` ne greffent pas : les liens ne sont posés que par `graft`.
- **Greffe complète** : `graft` sans `--scion`, et `graft-update`, appellent `regraft`
  (`graft.py:864`). `regraft` commence par `_projections`, qui fait le contrôle P-E1 dans
  `_projected_state`, puis résout chaque clé par `Listing.from_tree(gitops.ls_tree(root,
  commit))` et `resolve_projection`.
  - La résolution lit la liste git et jamais le disque (P-M4) : la table est connue sans aucun
    blob.
  - Viennent ensuite `ungraft`, puis `graft` et `_graft_entries`, qui appelle
    `target.symlink_to(...)` sans vérifier que la source existe.
  - En cas d'échec, `_put_back` rétablit le trunk et la liste greffée.
- **Greffe partielle** : `graft --scion` appelle `graft_scions` (`graft.py:1076`), avec
  `_projections(strict=clés choisies)`.
  - Les autres clés d'un clone partagé sont résolues « au mieux ».
  - Un lien du clone qui n'est dans aucune table est retiré (P-G3).
- **Avance** : P-P5 et P-P7 relisent le porteur après l'avance. Une version nouvelle est clonée
  par `_fetch` (P-V5), et l'ancien clone reste. Les clones existants sont contrôlés par
  `clone_updates` et `_check_projected_clone` (P-V4), qui ne lisent que `HEAD` et les tags.
- **Retrait** : `graft-remove` (P-G3, P-P6) et `ungraft` ne touchent pas les clones tiers.

Conséquence : l'ensemble à extraire est connu exactement là où la greffe en a besoin, c'est-à-dire
après P-E1 et avant la pose des liens. Comme la pose ne vérifie pas les sources, un ensemble trop
petit donnerait des liens cassés sans aucun message. Comme `regraft` rétablit les anciens liens
quand il échoue, un ensemble réduit avant la pose laisserait ces liens rétablis pointer vers des
fichiers retirés.

### 1.3 Règles touchées

| Règle | Effet de l'extraction partielle |
| --- | --- |
| P-V2 | création : `clone --no-checkout`, extraction partielle sans répertoire (racine seule), puis `checkout --detach` ; le clone partagé prend l'union des tables |
| P-V4 | inchangée : `HEAD` et tags seulement |
| P-V5 | nouveau clone créé comme P-V2 ; l'ancien reste tel quel (son ensemble n'est plus recalculé) |
| P-E1 | inchangée : `git status --porcelain --untracked-files=no` ignore les fichiers hors de l'ensemble (`skip-worktree`) ; essai : sortie vide sur un clone épars propre |
| P-M4 | inchangée : la liste git (`ls-tree -r`) est indépendante de l'extraction (8 962 entrées sur le clone épars) |
| P-G3 | inchangée : la propriété se lit sur les liens ; aucun lien ne vise un fichier non extrait si l'ensemble est recalculé à chaque greffe |
| P-V3 | un emplacement local est utilisé tel quel : jamais d'extraction partielle |
| P-C1 | inchangée : sans projection, aucun clone tiers |

### 1.4 Essai de `git sparse-checkout` (clones temporaires dans le répertoire de session)

Clones de `https://github.com/lepton-distribution/mirror-STM32CubeWL.git` et
`mirror-cmsis_device_f4.git` (`--filter=blob:none --no-checkout`). Aucun clone de `<ROOTSTOCK>`
n'a été touché.

| Essai | Résultat |
| --- | --- |
| Clone sans blobs ni extraction (STM32CubeWL) | 48 commits, 8 tags, 9 710 arbres, 1,65 Mio |
| Cône `set --cone --stdin` (9 répertoires) avant `checkout --detach v1.6.0` | `set` sur un index vide n'extrait rien ; puis 103 fichiers (84 blobs) ; paquets 1,85 Mio (au lieu de 21,7 Mio) ; `status` vide ; `ls-files -t` : 103 `H`, 8 859 `S` |
| Non-cône `set --no-cone --stdin` (39 chemins `/…`) puis `checkout` | 39 fichiers, 1,72 Mio ; `status` vide ; aucun avertissement affiché |
| Cône sans répertoire (`set --cone`) puis `checkout` | racine seule : 10 fichiers, 184 Ko, 1,68 Mio |
| Ensemble changé (non-cône : −`Utilities/lcd`, +`README.md`) | fichiers retirés et ajoutés, blobs reçus à la demande, `status` vide |
| Élargir puis réduire (cône) | 10 → 25 → 20 fichiers ; `set` identique : 0,05 s |
| Fichier suivi modifié qui sort de l'ensemble | laissé en place, avertissement « not up to date and were left despite sparse patterns », code 0 → P-E1 doit précéder |
| Fichier non suivi dans un répertoire qui sort | laissé en place, code 0 |
| Clone extrait en entier puis converti (CMSIS F4) | 152 → 6 fichiers (exact) ou 31 (cône `Include`), arbre 25,9 → 2,6 Mo ; `.git` inchangé (520 → 528 Ko) ; `disable` → 152 |
| Autre version dans un clone épars (`checkout v1.3.0`) | ensemble appliqué au nouveau commit (217 fichiers), `status` vide |
| `core.ignoreCase` (dépôt local, `Inc/a.h`) | non-cône `/inc/a.h` et cône `inc` : extraits avec `true`, rien avec `false`. Sans tenir compte de la casse, l'ensemble ne peut que grossir ; scion donne les chemins exacts de la liste git |
| Caractères spéciaux, non-cône, chemins non échappés | `/a[1].h` extrait `a1.h` (classe `[…]`) et non `a[1].h` ; `/tr ` (espace final) n'extrait rien. Le mode non-cône impose d'échapper `\`, `*`, `?`, `[` et l'espace final |
| Caractères spéciaux, cône | git échappe lui-même (`/a\*b/`) ; `sp ace` correct ; les fichiers de la racine sont toujours extraits |
| Configuration écrite | `extensions.worktreeConfig=true` ; `.git/config.worktree` : `core.sparseCheckout`, `core.sparseCheckoutCone` ; `.git/info/sparse-checkout` |
| git 2.18.0 (`/usr/local/git/bin/git`) sur un clone épars | refus : « unknown repository extensions found: worktreeconfig », pour `status` comme pour `sparse-checkout` |

### 1.5 Version de git (notes de version et manuels de git, relevés le 2026-11-12)

| Fonction | Depuis |
| --- | --- |
| `git sparse-checkout` (`init`, `list`, `set`, `disable`), `set --stdin`, `clone --sparse` | 2.25.0 |
| `sparse-checkout reapply` | 2.27.0 |
| `set --cone` / `--no-cone` sans `init` ; `init` déprécié | 2.35.0 |
| cône par défaut ; mode non-cône déprécié (« non-cone mode is deprecated. Please switch to using cone mode. ») | 2.37.0 ; aucun retrait annoncé |

Hôtes :
- Mac : 2.50.1 (`/usr/bin/git`, en tête du PATH), qui convient ; 2.18.0 (`/usr/local/git/bin`),
  qui ne convient pas et ne pourrait même plus ouvrir un clone épars ;
- VM : 2.47.3, qui convient.

### 1.6 Effets hors de scion

| Élément | Effet |
| --- | --- |
| lepton `projection_tables`, `file owner`, `seed tree` | lus sur les liens du trunk : inchangés |
| lepton `seed status` (`git status --porcelain -- .` du clone) | inchangé : les fichiers hors de l'ensemble ne sont pas signalés |
| lepton `seed lock` (commit du clone) | inchangé |
| lepton `check`, `generate` | lisent le trunk : inchangés (à constater sur la copie, tâche 3) |
| extension, table clone tiers → trunk (`srcmap.ts`, `debug.ts`) | lue dans `seed status --json`, donc sur les liens : inchangée. Le débogueur ne voit que des fichiers liés, tous extraits |
| `mirror-sync` | travaille dans `depots/.mirrors/` (dépôts `--mirror`) : non touché |
| hook `proteger-trunk.py` | inchangé : scion écrit dans `depots/tiers/` par son propre processus ; à la main, toute commande `sparse-checkout` reste interdite |
| `controler-trunk.py` | `ls-tree`, `hash-object` des cibles, `status` : inchangé (cibles toutes extraites) |
| skill `lepton-rootstock`, section Projection | à compléter : clone tiers épars ; un fichier non projeté se lit par `git -C <clone> show HEAD:<chemin>` ou dans le miroir |
| `README.md` de seed.scions (l. 266), `CHANGELOG.md` | à compléter dans le commit de version |

Aucune modification de code n'est nécessaire dans lepton ni dans l'extension.

### 1.7 Projet d'amendement de `projection-miroir.md` (à valider au PA-91)

En-tête, ligne « Versions » : ajouter « Évolution **0.6.3.0** : règle P-V7 (extraction partielle
des clones distants). »

§A.8, P-V2, deuxième phrase remplacée par :
> Il est créé par `git clone --filter=blob:none --no-checkout`, mis en extraction partielle sans
> répertoire (P-V7), puis `git checkout --detach <version>`.

§A.8, règle nouvelle après P-V6 :
> - **P-V7** (0.6.3.0). Un clone distant de clé projetée (P-V2) est en extraction partielle, au mode
>   cône de git (`git sparse-checkout set --cone`). Son **ensemble extrait** est formé de deux
>   parties :
>   - les fichiers de la racine du clone, que le mode cône extrait toujours ;
>   - tout le contenu des **répertoires parents des fichiers sources** des tables (§A.6) de toutes
>     les clés de la liste greffée qui partagent le clone (P-V2).
>
>   Un répertoire contenu dans un autre de l'ensemble est omis. L'ensemble se calcule sur les tables,
>   jamais sur le disque. Les autres fichiers de ces répertoires sont extraits aussi, même exclus ou
>   non désignés : ils ne sont jamais liés.
>   - À la création (`seed-add`, `seed-clone`, `seed-update`, `graft-update`), le clone n'extrait
>     que la racine jusqu'à sa première greffe.
>   - À la greffe (`graft`, `graft --scion`, regreffe de `graft-update`), l'extraction se fait en
>     deux temps :
>     1. Après le contrôle P-E1 et avant la pose des liens, l'ensemble est **élargi** à l'union de
>        l'ensemble en place et de l'ensemble calculé : des fichiers s'ajoutent, et aucun ne part.
>     2. Après la greffe réussie, il est **réduit** à l'ensemble calculé.
>
>     Une greffe qui échoue laisse l'ensemble élargi. Le trunk rétabli ne vise donc jamais un
>     fichier non extrait.
>   - Un clone extrait en entier, créé avant 0.6.3.0, est converti par sa prochaine greffe. Les
>     objets déjà reçus restent dans `.git`.
>   - `graft-remove`, `ungraft` et `graft-clean` ne changent pas l'ensemble : il peut rester trop
>     large, sans effet. Un clone qui n'est plus greffé (P-V5, P-P7) reste tel quel.
>   - Un emplacement local (P-V3) n'est jamais mis en extraction partielle.
>   - Les contrôles ne changent pas. P-V4 lit `HEAD` et les tags. P-E1 ne voit pas les fichiers hors
>     de l'ensemble. Les motifs portent sur la liste git (P-M4). Un fichier non suivi reste en place
>     quand son répertoire sort de l'ensemble.
>   - L'extraction partielle écrit `.git/info/sparse-checkout` et la configuration propre au clone
>     (`.git/config.worktree`, extension `worktreeConfig`). Ces fichiers ne s'éditent pas à la main :
>     la greffe suivante les réécrit.
>   - Elle exige git ≥ 2.35. <Conduite si git est plus ancien : à trancher au PA-91.>
>   - Un message (niveau info) nomme chaque clone dont l'ensemble change, avec son nombre de
>     répertoires. `-v` liste les répertoires.

§A.11, table :
- ligne `seed-add`, `seed-clone` : ajouter « ; clone extrait à la racine seule (P-V7) » ;
- ligne `graft` : ajouter « ; ensemble extrait élargi avant la pose, réduit après (P-V7) » ;
- ligne `seed-update`, `graft-update` : ajouter « ; regreffe : P-V7 ».

§C : la ligne « `sparse-checkout` du clone tiers. » devient « Extraction partielle d'un emplacement
local (P-V3) ; extraction partielle au mode non-cône (liste exacte des fichiers) : mode déprécié par
git depuis 2.37, qui imposerait d'échapper les chemins (rapport d'ENV-52 du chantier Lepton). »

### 1.8 Propositions pour le PA-91

| Point | Proposition | Raison |
| --- | --- | --- |
| Défaut ou option | par défaut, pour tout clone distant de clé projetée ; aucune option | D11 vise chaque rootstock ; une option ajoute un chemin à tester sans besoin constaté ; le reste d'un dépôt tiers se lit par `git show` ou dans le miroir |
| Ensemble extrait | mode cône, répertoires parents des sources des tables | mode recommandé par git (le non-cône est déprécié) ; git échappe les chemins ; STM32CubeWL passe de 118,7 à 1,6 Mo ; écart au non-cône : 45 Mo sur 8 clones, venu des `Include/` des CMSIS device |
| Clones existants | convertis par la prochaine greffe (règle P-V7, sans commande ajoutée) ; `<ROOTSTOCK>` : `scion graft` sur accord, sans `graft-update` | la greffe recalcule l'ensemble de toute façon ; aucun réseau (blobs déjà présents) ; arbre extrait de 217 à 78 Mo environ ; `.git` inchangé (30 Mo) |
| git minimal | 2.35 ; plus ancien : erreur explicite (code 1), avant tout clonage ou toute greffe d'une clé projetée distante | un seul comportement à tester ; un repli sur l'extraction complète ne protège pas un clone déjà épars, que git < 2.20 refuse d'ouvrir |
| lepton et extension | aucun code ; skill `lepton-rootstock` et documentation dans cette étape | §1.6 |
| Version | 0.6.3.0 | évolution compatible des formats, comme 0.6.1.0 (miroir) ; seule l'exigence sur git augmente |
| `SCION_MIN_VERSION`, `SCION_REF` | `SCION_MIN_VERSION` inchangé (0.6.2.0) ; `SCION_REF` 0.6.3.0 dans `install-vscodium.sh` et `install-{macos,debian}.sh` du clone noyau (branche `devenv/env-52`) | lepton ne dépend pas de P-V7 ; les installations neuves en profitent |
| Binaires | raisonnement de `rapports/env-15-scion.md` §6, sans oracle | liste `chemin -> cible` identique et contenu projeté identique au commit épinglé (`controler-trunk.py`) prouvent un trunk identique, octet pour octet, donc les mêmes entrées de construction |

## 2. PA-91 (2026-11-12, décision de l'utilisateur)

| Point | Décision |
| --- | --- |
| Ensemble extrait | mode cône, répertoires parents des fichiers sources des tables, union des clés qui partagent le clone, plus la racine |
| Défaut ou option | par défaut pour tout clone distant de clé projetée, sans option ; jamais un emplacement local (P-V3) |
| Clones existants | convertis par leur prochaine greffe (P-V7) ; `<ROOTSTOCK>` : `scion graft` sur accord, sans `graft-update` |
| git minimal | 2.35 ; plus ancien : erreur explicite, code 1, avant tout clonage ou toute greffe d'une clé projetée distante |
| lepton et extension | aucun correctif de code ; skill `lepton-rootstock` et documentation dans cette étape |
| Version | 0.6.3.0 |
| `SCION_MIN_VERSION`, `SCION_REF` | `SCION_MIN_VERSION` inchangé (0.6.2.0) ; `SCION_REF` 0.6.3.0 dans `install-vscodium.sh` et dans `install-{macos,debian}.sh` du clone noyau (branche `devenv/env-52`) |
| Binaires | oracle après : `oracles/env-52-apres/` comparé à `oracles/env-49-apres/` (code 0 attendu) |
| Amendement | texte du §1.7 validé tel quel ; le point git est complété par l'erreur explicite |
