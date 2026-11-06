# ENV-38 — scion : conception de la projection et du miroir

Rapport propre à Lepton. Le texte générique (spécification) est rédigé après le PA-63, à
l'emplacement qu'il retient. Principes du 2026-11-04 (`DEVENV-STATUS.md` §Décisions), non
rediscutés : projection déclarée dans la graine (`.scion.projections` en colonnes, destinations à
préfixe `scion/`, motifs récursif, non récursif, filtre, fichier) ; miroir de conservation (avance
rapide, tag déplacé signalé, jamais propagé) par une commande générique ; deux dépôts séparés
(HAL, CMSIS device) ; la copie d'ENV-34 sera remplacée (ENV-41) ; NF-2.

## 1. Audit (lecture seule) — état au PA-63

Références : `<SEED_SCIONS>` `master` 1173d6d (tag `0.5.4.0` sur 99aa973), scion 0.5.4.0 installé ;
graine `original-tree` 15740f9 ; rootstock `<ROOTSTOCK>` (14 scions greffés).

### 1.1 Lecture d'une graine (`scion/model.py`, `scion/graft.py` `_wanted`)
- Champs séparés par toute suite d'espaces et de tabulations, `#` ouvre un commentaire, ligne trop
  courte ignorée en silence (`model.fields`, `_lines`).
- `.scion.sources.list` : `shelf nom version emplacement [chemin]` (≥ 4 champs). `.scion.ramifications` :
  `shelf nom version` (≥ 3). Nom `prefix[::suffix]`, clé `shelf/nom`, version exclue.
- `select_source` : version exacte d'abord ; sinon (et toujours pour `?`) la plus haute version
  déclarée pour la clé (`compare`, indulgent : deux versions non comparables sont « égales »).
- **Rôle réel de la 5ᵉ colonne** (« scion location in depot », `SourceEntry.subpath`) : chemin, dans
  le clone, du répertoire qui contient `scion/` (`local = clone/chemin`, `stem = local/scion`). Sert
  à découper plusieurs scions dans un même dépôt. Aucune ligne de `original-tree` ne l'emploie.
- **Emplacement d'un clone** : URL distante → `depots/<shelf>/<prefix>/<version>` ; le suffixe
  `::x` n'entre pas dans le chemin, donc deux scions de même `prefix` et de même version partagent
  un clone (« seize scions découpés dans un même dépôt le clonent une fois »). Chemin local →
  résolu par rapport au rootstock (aucune variable d'environnement).
- `sync` exige `<local>/scion/` : un dépôt sans `scion/` est refusé (« Vérifiez la colonne « chemin
  dans le dépôt » »). C'est exactement ce que la projection doit lever.
- `.scion.grafted.list` (dans le trunk) : `shelf nom version chemin_local graine` ; un scion déjà
  greffé dans une version plus récente est conservé (`_wanted`).

### 1.2 Greffe (`graft.py`)
- `_walk(stem)` : parcours du **système de fichiers** du clone (`os.walk`, pas `git ls-files`),
  `.scion/` sauté à tout niveau, lien committé traité comme une feuille.
- Trunk : répertoires réels, feuilles = liens relatifs (`relative_link`) ; **correspondance
  identité** `trunk/<r>` → `<stem>/<r>`. Aucun renommage possible aujourd'hui.
- Conflit : toute feuille déjà présente (ou un répertoire qui rencontre un fichier) est un conflit ;
  **aucune superposition ni priorité** : l'ordre des ramifications ne change que le message. Les
  conflits sont tous collectés, la greffe est annulée (`_rollback`). Des répertoires sont partagés
  sans conflit entre scions (cas de `stm32f4xx/` entre noyau et famille).
- Filtre des fichiers ignorés (ENV-15, 0.5.2.0 ; hors git 0.5.3.0) : `git ls-files --others --ignored
  --exclude-standard` sur le `stem` ; scion contenu dans le dépôt du rootstock : aucun filtre.
- `.scion.trunk.tolerated` : motifs `fnmatchcase` sur le **nom** d'un fichier régulier du trunk
  (`.DS_Store`, `._*` dans `<ROOTSTOCK>`) ; ne bloquent pas le dégreffage.
- Propriétaire d'un chemin du trunk (`_owner`) : pour un lien, préfixe de la cible = `stem` du scion ;
  **pour un répertoire, `(<stem>/<r>).is_dir()`** — suppose la correspondance identité.
- Greffe partielle (`graft --scion`, `graft_scions`) et retrait (`graft-remove`, `remove`) :
  `_unlink` reconnaît les liens par **préfixe de cible** (indépendant de la correspondance) ;
  `_prune` garde un répertoire si **`(<stem>/<r>).is_dir()`** pour un scion restant — identité
  supposée ; `remove` calcule les répertoires candidats par `_walk(stem)` — identité supposée.
- `regraft` (0.5.4.0) : relevé du trunk et de la liste greffée, remise en place si la résolution,
  le dégreffage ou la greffe échoue.
- `--purge` : seulement un clone sous `depots/<shelf>/<prefix>/<version>`, non partagé, propre,
  sans commit local.

### 1.3 Versions et mises à jour (`graft.py` `update_sources`, `_check_clone` ; `gitops.py`)
- `gitops.clone` : `git clone` complet (ou `--single-branch`), puis `git checkout <version>` ;
  aucun clone partiel (`--filter`) ni `sparse-checkout`.
- Version **branche** : branche courante = version, amont présent, pas de divergence ; en retard avec
  modifications suivies → arrêt ; avance par `fetch` + `merge --ff-only @{u}`.
- Version **tag** : `HEAD` doit être le commit du tag ; tag déplacé dans `origin`
  (`ls-remote` déréférencé `^{}`) → arrêt « tag déplacé » ; tag absent de l'amont → laissé.
- Version **commit** : non prévue. `checkout <sha>` réussit au clonage, mais `_check_clone` rend
  « version déclarée introuvable » (ni branche ni tag) : `graft-update` / `seed-update` échoueraient.
- Version `*` (source locale) : jamais clonée ni avancée.
- `seed-update` (`update_sources` + `sync` d'une graine), `graft-update` (toutes les graines de la
  liste greffée, puis `regraft`), `seed-add` (clone de la graine, puis idem). Contrôles avant toute
  modification ; messages groupés.
- `seed-scion-add` / `seed-scion-remove` (`seed.py`) : écrivent une ligne de sources et une de
  ramifications (`rewrite_key`, commentaires conservés) ; ne clonent rien.

### 1.4 Clients de scion (lepton-tools, hook, skill)
Relevé par un sous-agent en lecture seule, points sensibles contrôlés à la main
(`rootstock.py:177-186`, `checks.py:73-93`, `seed.py` `rs.sources()`, `generate.py:384`).
lepton suppose partout « clone + `scion/` = racine du trunk, même chemin relatif » et un
`lepton-greffon.json` par greffon. Une projection serait greffée sans erreur, mais :

| Client | Hypothèse actuelle | Effet d'une projection | Étape porteuse probable |
| --- | --- | --- | --- |
| `lepton/__init__.py:8` `SCION_MIN_VERSION` (0, 5, 4, 0) ; `install-vscodium.sh:56` `SCION_REF` ; `README.md:10` | — | à relever | ENV-39 / ENV-40 |
| `scion_runner.py` | ne lit que `scion version` et les codes de retour | aucun | — |
| `rootstock.py:85-95` (lit lui-même `.scion.grafted.list`, `.scion.sources.list`) | 5ᵉ colonne des sources = sous-chemin ; 5ᵉ colonne de la liste greffée = graine | une colonne de plus dans `.scion.sources.list` serait mal lue ; une seconde valeur de graine dans la liste greffée bloque `seed_dot()` (« N graine(s), une seule attendue ») | ENV-39 (format) |
| `checks.py:73-113, 261-276` (`check_declared_files`, `check_family_files`, `scion_c_files`) | `sources` et `inclusions` cherchées **dans le clone du manifeste** | la famille F4 déclare `hal_driver/Src/*.c` : « introuvable » alors que CMake les trouve par le trunk | ENV-41 |
| `rootstock.py:222-231` `check_trunk`, `is_system_file` | motifs `.DS_Store`, `._*` en dur, `.scion.trunk.tolerated` non lu | aucun (un lien projeté est un lien valide) | — |
| `seed status` (`seed.py:438-486`) | `stem` = `<clone>/scion`, rôle du manifeste | projection « sans manifeste », `stem` inexistant, « hors graine » si déclarée ailleurs que dans les sources | ENV-41 |
| `seed lock`, `--verify`, `--restore` (`seed.py:715-846`) | parcourent `rs.sources()` | si la projection n'est pas dans les sources : **ni figée ni vérifiée** (GRA-5, NF-5) | ENV-41 |
| `seed new`, modèle `lepton/templates/seed/` ; `seed add/remove/replace` (`_expect` exige un manifeste) | noyau + famille + BSP | la projection dont la famille dépend manque au nouveau projet | ENV-41 |
| `seed tree` (`tree.py`) | propriétaire par préfixe de `stem` | sources HAL rangées « (hors greffon) » | ENV-41 |
| `lepton generate` (`generate.py:343-385`) | dossier « git · » par greffon ; `files.exclude` masque `scion/[!.]*` | clone tiers ouvert en entier dans l'espace, fichiers non masqués (IDE-4) | ENV-41 |
| `file owner`, `file add [--adopt]`, `graft --path`, `file rm/mv`, `dir *` (`files.py`) | `clone_path = stem / rel` | propriétaire faux (famille) dans un répertoire mixte ; `file add --scion <projection>` créerait `scion/` dans le clone tiers | ENV-41 |
| extension (`srcmap.ts:13-26`, `watch.ts`, `commands.ts:69-80`, `tree.ts:298`) | via `seed status` / `file owner` | gdb rend le chemin du clone tiers → ouvert hors trunk ; projection proposée comme propriétaire | ENV-41 |
| hook `proteger-trunk.py` | ne protège que le trunk | aucun refus d'écriture dans un clone tiers | ENV-41 |
| skill `lepton-rootstock` (l. 14-29) | « éditer le realpath sous `depots/` », « créer sous `scion/` du clone », `git mv` dans le clone ; exemple de clé périmé (`lepton@bsp::nucleo-f429zi`) | règle fausse pour un clone tiers | ENV-41 (exemple périmé : ici ou ENV-41) |
| `cmake/lepton_greffons.cmake:550` (noyau) | lit le trunk | aucun tant que les destinations sont celles d'aujourd'hui | — |
| `scripts/tiers/verifier-import.sh` | copie aux chemins amont, `find -type f` | sans objet pour une projection (le clone est l'amont) ; sur le trunk il ne verrait que des liens | ENV-41 |
| `scripts/tiers/hal_conf_stm32f4.py`, `compiler-hal-f4-a-blanc.sh` | texte de provenance ; chemins du trunk | texte à revoir ; script valable | ENV-41 |

### 1.5 Cas d'épreuve écrits sous une forme candidate
Forme candidate utilisée **pour l'audit seulement** (rien n'est acté) : le dépôt tiers est déclaré
comme un scion ordinaire dans `.scion.sources.list` et `.scion.ramifications` (clé, version, URL) ;
`.scion.projections` porte, par clé, des lignes `shelf nom motif destination`. Motifs : `d/**`
récursif, `d/*` non récursif, `d/*.h` filtre, `d/f` fichier, `!motif` exclusion. Destination :
répertoire (`/` final) auquel s'ajoute le chemin relatif à la base du motif, ou fichier. Préfixe
`scion/` retiré pour obtenir le chemin du trunk. `F4` = `scion/sys/root/src/kernel/dev/arch/cortexm/stm32f4xx`,
`UC` = `scion/sys/root/src/kernel/core/ucore`, `WL` = `…/cortexm/stm32wlxx`.

**F4 — HAL** (`stm32f4xx-hal-driver` `v1.8.5` b6f0ed3) :
```
tiers  hal-f4   Inc/**       F4/hal_driver/Inc/
tiers  hal-f4   Src/**       F4/hal_driver/Src/
tiers  hal-f4   LICENSE.md   F4/hal_driver/
tiers  hal-f4   README.md    F4/hal_driver/
```
Exprimable. 200 fichiers, chemins identiques à `rapports/env-34-hal-f4/listes/hal.txt`.

**F4 — CMSIS device** (`cmsis_device_f4` 3c77349, **sans tag** : `git tag --contains` vide) :
```
tiers  cmsis-f4  Include/stm32f4xx.h          UC/cmsis-5/Device/ST/STM32F4xx/Include/
tiers  cmsis-f4  Include/system_stm32f4xx.h   UC/cmsis-5/Device/ST/STM32F4xx/Include/
tiers  cmsis-f4  Include/stm32f4[23]9xx.h     UC/cmsis-5/Device/ST/STM32F4xx/Include/
tiers  cmsis-f4  LICENSE.md                   UC/cmsis-5/Device/ST/STM32F4xx/
tiers  cmsis-f4  README.md                    UC/cmsis-5/Device/ST/STM32F4xx/
```
Exprimable, à une condition : **épinglage par commit** (non pris en charge, §1.3).

**F7 — CMSIS device** (`cmsis_device_f7` `v1.2.10` 2352e88) : même forme que le F4, sous-ensemble
de 3 en-têtes + `LICENSE.md`, `README.md` (`listes/cmsis-device-f7.txt`). Exprimable. HAL F7
(`v1.3.3` e1446fa) : même forme que la HAL F4.

**WL — HAL** (`stm32wlxx-hal-driver` `v1.3.0` e3966ab) :
```
tiers  hal-wl   Inc/**                         WL/cubemx_hal_driver/inc/
tiers  hal-wl   Src/**                         WL/cubemx_hal_driver/src/
tiers  hal-wl   README.md                      WL/cubemx_hal_driver/
tiers  hal-wl   Release_Notes.html             WL/cubemx_hal_driver/
tiers  hal-wl   !Inc/Legacy/stm32_hal_legacy.h
```
Renommage `Inc` → `inc` : naturel si la destination remplace la base du motif. Sur le volume du
Mac (insensible à la casse), `inc/` et `Inc/` désignent le même répertoire du trunk ; sur Debian,
deux. `stm32_hal_legacy.h` est d'une autre révision (STM32CubeWL `v1.3.0`) : exclu ici, il resterait
dans la famille — ou la HAL entière viendrait de STM32CubeWL, ce que la décision du 2026-11-04 exclut.
`LICENSE.txt` (hors amont) resterait dans la famille, à côté des liens projetés.

**WL — CMSIS device** (`cmsis-device-wl` `v1.1.1` d248c55) — aplatissement et chemin changé :
```
tiers  cmsis-wl  Include/stm32wl55xx.h                       UC/cmsis/Device/st/stm32wlxx/
tiers  cmsis-wl  Include/stm32wlxx.h                         UC/cmsis/Device/st/stm32wlxx/
tiers  cmsis-wl  Include/system_stm32wlxx.h                  UC/cmsis/Device/st/stm32wlxx/
tiers  cmsis-wl  Source/Templates/system_stm32wlxx.c         UC/cmsis/Device/st/stm32wlxx/
tiers  cmsis-wl  Source/Templates/iar/startup_stm32wl55xx_cm4.s  UC/cmsis/Device/st/stm32wlxx/startup/iar/
```
Exprimable (forme fichier, destination répertoire).

**WL — pile radio** (`stm32-mw-subghz-phy` `v1.3.0` 1cad768) : racine → `WL/radio_subghz_phy/`
sans renommage, sauf `radio.c` (modifié par Lepton) exclu et fourni par la famille ;
`stm32_radio_core_inc/` vient d'un **autre dépôt** (STM32CubeWL, application PingPong), 3 fichiers
sur 4 modifiés : il resterait dans la famille. Deux sources pour un même répertoire du trunk :
possible, car les répertoires sont partagés entre scions et seules les feuilles entrent en conflit.

**WL — utilitaires** (STM32CubeWL `v1.3.0` 378e461, 116 Mo partiel) : `Utilities/<d>/**` →
`WL/Utilities/<d>/` pour 8 sous-répertoires, avec exclusions (`html/`, `_htmresc/`, notes, `LICENSE.md`,
`PC_Software/`) et `timer/stm32_timer.h` modifié exclu. Exprimable ; un sous-arbre d'un gros dépôt
appelle un clone partiel (`--filter=blob:none`) et peut-être un `sparse-checkout`.

### 1.6 Ce que la forme candidate ne sait pas dire, ou ce que scion ne sait pas faire
| # | Constat | Cas | Point du PA-63 |
| --- | --- | --- | --- |
| C1 | Épinglage par commit absent (`_check_clone`) | CMSIS F4 3c77349 | Révision épinglée |
| C2 | Greffe par correspondance identité ; `_owner` (répertoires), `_prune`, `remove` aussi | toutes les projections renommantes | Articulation (implémentation ENV-39) |
| C3 | Pas de superposition : un fichier projeté et un fichier de la famille au même chemin = conflit | `radio.c`, `stm32_timer.h`, `stm32_hal_legacy.h` | Fichier modifié ; exclusion |
| C4 | Casse : `Inc` et `inc` confondus sur le Mac, distincts sur Debian | HAL WL | Casse des noms |
| C5 | Parcours par le système de fichiers : un fichier non suivi du clone tiers serait projeté | tous | Fichier modifié localement |
| C6 | Clone complet seulement | Utilitaires WL (116 Mo partiel) | Emplacement et profondeur du clone |
| C7 | La graine déclare la projection, mais la famille en dépend ; 13 lignes de graine aujourd'hui | toute graine qui référence une famille | Dépendance |
| C8 | Un fichier dérivé de l'amont et modifié (patch) n'a pas de forme : il reste une copie de la famille, sa provenance reste écrite à la main | `radio.c`, `stm32_timer.h`, 3 fichiers de `stm32_radio_core_inc/` | Rapport §5 |
| C9 | Provenance réelle d'un fichier `TROP` (`LICENSE.txt` ×8) : hors format | WL | Rapport §5 |

| C10 | lepton lit les sources pour `seed lock` et le statut ; il cherche les fichiers d'un manifeste dans le clone (§1.4) | toute famille projetée | Articulation ; effets ENV-41 |

### 1.7 Décisions du PA-63 (utilisateur, 2026-11-06)
Une ligne par point dans `DEVENV-STATUS.md` §Décisions (PA-63 Q1 à Q16).

| Point | Décision |
| --- | --- |
| Q1 articulation | dépôt tiers = scion ordinaire (sources, ramifications) ; `.scion.projections` : `shelf nom motif destination` |
| Q2 révision | tag ou commit complet ; branche refusée ; tag déplacé = arrêt |
| Q3 sans correspondance | erreur, exclusion comprise |
| Q4 casse | stricte, sur la liste git ; collision de casse dans le trunk = erreur partout |
| Q5 motifs | `d/**`, `d/*`, jokers dans le dernier segment, fichier ; destination `/` = répertoire remplaçant la base ; `!motif` |
| Q6 recouvrement | même source, même destination = un lien ; sinon erreur ; conflit inter-scions inchangé |
| Q7 clone modifié | fichiers suivis au commit seulement ; modification = greffe refusée |
| Q8 clone | `depots/<shelf>/<prefix>/<version>`, `--filter=blob:none` |
| Q9 dépendance | **greffon porteur** (écart au principe du 2026-11-04) : `scion/.scion/` complet, un niveau, projections seules ; double déclaration = erreur sauf identité |
| Q10 miroir | graine → miroir ; `.scion.mirrors` à côté de la ligne de sources (graine ou greffon) |
| Q11 conduite | branche réécrite non mise à jour, tag supprimé conservé, signalés ; code 1 si signalement |
| Q12 commande | `mirror-sync [--seed] [--dry-run] [miroir…]`, `depots/.mirrors/` |
| Q13 versions | 0.6.0.0 puis 0.6.1.0 ; `SCION_MIN_VERSION` en ENV-41 |
| Q14 provenance | renvoyée au PA-69 |
| Q15 emplacement | `<SEED_SCIONS>/doc/projection-miroir.md` |
| Q16 édition | aucune commande |

Conséquence de Q9 sur C7 et C10 : la projection d'une famille voyage avec la famille ; une graine
de projet qui référence la famille n'a rien à ajouter. `lepton seed lock` et `seed status`, qui ne
lisent que les sources de la graine, ne voient pas les sources d'un `.scion/` de greffon (effet
ENV-41, §4).
