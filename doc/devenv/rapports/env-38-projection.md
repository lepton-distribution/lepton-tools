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

## 2. Cas d'épreuve dans le format final

Spécification : `<SEED_SCIONS>/doc/projection-miroir.md` (branche `devenv/env-38`). Règles citées :
`P-…`, `M-…`. Chaque cas est déclaré dans le `scion/.scion/` de sa famille (porteur, PA-63 Q9).
Noms de clé, shelf `tiers` et URL : **propositions** pour illustrer le format ; ils seront arrêtés
au PA-69 (ENV-41, F4 seul). Les URL deviendront celles des miroirs après le PA-68 (M-D2).

Listes des chemins attendus dans le trunk : `rapports/env-38-projection/attendus/` (618 chemins).
Elles sont tirées des listes git amont (`git ls-tree -r --name-only <révision>`) et, pour le WL, des
fichiers `OK` des classements d'ENV-37, préfixées de la destination. **Contrôle** : chacun des 618
chemins est aujourd'hui un lien du trunk, vers la copie de la famille. F4 et F7 : la liste amont est
identique, fichier par fichier, à la copie (hors `LEPTON-PROVENANCE.md`, qui reste dans la famille).
La projection reproduit donc le trunk actuel.

Abréviations dans les lignes ci-dessous (à écrire en entier dans le fichier réel) :
`K` = `scion/sys/root/src/kernel`, `D` = `K/dev/arch/cortexm`.

### 2.1 F4 (bascule ENV-41) — `family-stm32f4xx/master/scion/.scion/`
```
# .scion.sources.list
tiers  stm32f4xx-hal-driver  v1.8.5                                    https://github.com/STMicroelectronics/stm32f4xx-hal-driver.git
tiers  cmsis-device-f4       3c77349ce04c8af401454cc51f85ea9a50e34fc1  https://github.com/STMicroelectronics/cmsis_device_f4.git
# .scion.ramifications
tiers  stm32f4xx-hal-driver  v1.8.5
tiers  cmsis-device-f4       3c77349ce04c8af401454cc51f85ea9a50e34fc1
# .scion.projections
tiers  stm32f4xx-hal-driver  Inc/**                      D/stm32f4xx/hal_driver/Inc/
tiers  stm32f4xx-hal-driver  Src/**                      D/stm32f4xx/hal_driver/Src/
tiers  stm32f4xx-hal-driver  LICENSE.md                  D/stm32f4xx/hal_driver/
tiers  stm32f4xx-hal-driver  README.md                   D/stm32f4xx/hal_driver/
tiers  cmsis-device-f4       Include/stm32f4xx.h         K/core/ucore/cmsis-5/Device/ST/STM32F4xx/Include/
tiers  cmsis-device-f4       Include/system_stm32f4xx.h  K/core/ucore/cmsis-5/Device/ST/STM32F4xx/Include/
tiers  cmsis-device-f4       Include/stm32f4[23]9xx.h    K/core/ucore/cmsis-5/Device/ST/STM32F4xx/Include/
tiers  cmsis-device-f4       LICENSE.md                  K/core/ucore/cmsis-5/Device/ST/STM32F4xx/
tiers  cmsis-device-f4       README.md                   K/core/ucore/cmsis-5/Device/ST/STM32F4xx/
```
Formes : récursif, fichier, filtre (`[23]`). Version par commit (P-V1). Attendus : `f4-hal.txt`
(200), `f4-cmsis-device.txt` (6). Clones : `depots/tiers/stm32f4xx-hal-driver/v1.8.5`,
`depots/tiers/cmsis-device-f4/3c77349…` (P-V2).

### 2.2 F7 (cas d'épreuve, bascule non planifiée)
Même forme que le F4 : `stm32f7xx-hal-driver` `v1.3.3` (`Inc/**`, `Src/**`, `LICENSE.md`,
`README.md` → `D/stm32f7xx/hal_driver/…`) ; `cmsis-device-f7` `v1.2.10`
(`Include/stm32f7xx.h`, `Include/system_stm32f7xx.h`, `Include/stm32f746xx.h` → `…/STM32F7xx/Include/` ;
`LICENSE.md`, `README.md` → `…/STM32F7xx/`). Attendus : `f7-hal.txt` (196), `f7-cmsis-device.txt` (5).

### 2.3 WL (cas d'épreuve, bascule non planifiée) — `family-stm32wlxx/master/scion/.scion/`
```
# .scion.sources.list (extrait) ; ramifications : mêmes clés et versions
tiers  stm32wlxx-hal-driver        v1.3.0  https://github.com/STMicroelectronics/stm32wlxx-hal-driver.git
tiers  cmsis-device-wl             v1.1.1  https://github.com/STMicroelectronics/cmsis-device-wl.git
tiers  stm32-mw-subghz-phy         v1.3.0  https://github.com/STMicroelectronics/stm32-mw-subghz-phy.git
tiers  stm32cubewl::utilities      v1.3.0  https://github.com/STMicroelectronics/STM32CubeWL.git
tiers  stm32cubewl::radio-core-inc v1.3.0  https://github.com/STMicroelectronics/STM32CubeWL.git
# .scion.projections
tiers  stm32wlxx-hal-driver  Inc/**                          D/stm32wlxx/cubemx_hal_driver/inc/
tiers  stm32wlxx-hal-driver  Src/**                          D/stm32wlxx/cubemx_hal_driver/src/
tiers  stm32wlxx-hal-driver  README.md                       D/stm32wlxx/cubemx_hal_driver/
tiers  stm32wlxx-hal-driver  Release_Notes.html              D/stm32wlxx/cubemx_hal_driver/
tiers  stm32wlxx-hal-driver  !Inc/Legacy/stm32_hal_legacy.h
tiers  cmsis-device-wl  Include/stm32wl55xx.h                         K/core/ucore/cmsis/Device/st/stm32wlxx/
tiers  cmsis-device-wl  Include/stm32wlxx.h                           K/core/ucore/cmsis/Device/st/stm32wlxx/
tiers  cmsis-device-wl  Include/system_stm32wlxx.h                    K/core/ucore/cmsis/Device/st/stm32wlxx/
tiers  cmsis-device-wl  Source/Templates/system_stm32wlxx.c           K/core/ucore/cmsis/Device/st/stm32wlxx/
tiers  cmsis-device-wl  Source/Templates/iar/startup_stm32wl55xx_cm4.s  K/core/ucore/cmsis/Device/st/stm32wlxx/startup/iar/
tiers  stm32-mw-subghz-phy  *.h                    D/stm32wlxx/radio_subghz_phy/
tiers  stm32-mw-subghz-phy  LICENSE                D/stm32wlxx/radio_subghz_phy/
tiers  stm32-mw-subghz-phy  Conf/*                 D/stm32wlxx/radio_subghz_phy/Conf/
tiers  stm32-mw-subghz-phy  stm32_radio_driver/*   D/stm32wlxx/radio_subghz_phy/stm32_radio_driver/
tiers  stm32-mw-subghz-phy  !stm32_radio_driver/radio.c
tiers  stm32cubewl::utilities  Utilities/conf/*.[ch]           D/stm32wlxx/Utilities/conf/
tiers  stm32cubewl::utilities  Utilities/Fonts/*.[ch]          D/stm32wlxx/Utilities/Fonts/
tiers  stm32cubewl::utilities  Utilities/lcd/*.[ch]            D/stm32wlxx/Utilities/lcd/
tiers  stm32cubewl::utilities  Utilities/lpm/tiny_lpm/*.[ch]   D/stm32wlxx/Utilities/lpm/tiny_lpm/
tiers  stm32cubewl::utilities  Utilities/misc/*.[ch]           D/stm32wlxx/Utilities/misc/
tiers  stm32cubewl::utilities  Utilities/sequencer/*.[ch]      D/stm32wlxx/Utilities/sequencer/
tiers  stm32cubewl::utilities  Utilities/timer/*.[ch]          D/stm32wlxx/Utilities/timer/
tiers  stm32cubewl::utilities  Utilities/trace/adv_trace/*.[ch]  D/stm32wlxx/Utilities/trace/adv_trace/
tiers  stm32cubewl::utilities  !Utilities/timer/stm32_timer.h
tiers  stm32cubewl::radio-core-inc  Projects/NUCLEO-WL55JC/Applications/SubGHz_Phy/SubGHz_Phy_PingPong/Core/Inc/utilities_def.h  D/stm32wlxx/radio_subghz_phy/stm32_radio_core_inc/
```
Ce que le cas éprouve :
- renommage de casse `Inc` → `inc` (P-T2) ; P-K2 sans collision, car la famille fournit
  `inc/Legacy/stm32_hal_legacy.h` avec la même casse ;
- aplatissement et chemin changé (`Source/Templates/iar/` → `startup/iar/`) ;
- exclusion des fichiers modifiés par Lepton, fournis par la famille (P-X1, P-G2) ;
- sélection positive dans un gros dépôt, `html/` exclu par le motif non récursif ;
- deux clés de même préfixe et de même version partagent un clone :
  `depots/tiers/stm32cubewl/v1.3.0` (P-V2), partiel (`blob:none`) ;
- deux dépôts amont pour `radio_subghz_phy/` (P-G1).

Attendus : `wl-hal.txt` (155), `wl-cmsis-device.txt` (5), `wl-radio.txt` (18), `wl-stm32cubewl.txt`
(32 + 1). Restent dans la famille : `stm32_hal_legacy.h` (autre révision), `radio.c`,
`stm32_timer.h`, 3 fichiers de `stm32_radio_core_inc/` (modifiés), `LICENSE.txt` ×8 (hors amont),
les 4 `LEPTON-PROVENANCE.md`.

## 3. Plan de tests pour ENV-39 et ENV-40

Un cas nommé par règle, sur des dépôts de test fabriqués par `tests/make_fixture.py` (dépôt tiers
sans `scion/`, tags, commit sans tag, fichiers non suivis, sous-module, lien committé), sans réseau
sauf `tests/test_network.py`. Fichiers proposés : `tests/test_projection.py`, `tests/test_mirror.py`.

| Règle | Cas de test |
| --- | --- |
| P-C1 | `test_sans_projection_greffe_identique_0_5_4_0` (fixture actuelle, trunk et liste greffée comparés) |
| P-C2 | `test_liste_greffee_sans_sixieme_colonne_hors_porteur` |
| P-C3 | `test_scion_dot_scion_sans_projections_ignore` |
| P-D1 | `test_cle_projetee_declaree_comme_scion` |
| P-D2 | `test_cle_projetee_greffe_sans_repertoire_scion` ; `test_cle_projetee_chemin_dans_depot_refuse` |
| P-D3 | `test_projection_sans_ligne_de_sources_erreur` |
| P-F1 | `test_ligne_projection_mal_formee_erreur_avec_numero` |
| P-F2 | `test_fichier_tiers_a_blanc_projete_par_joker` |
| P-M1 | `test_joker_dernier_segment` ; `test_joker_segment_interieur_refuse` ; `test_joker_point_initial` |
| P-M2 | `test_double_etoile_dernier_segment_seulement` |
| P-M3 | `test_motif_point_point_refuse` |
| P-M4 | `test_non_suivi_jamais_projete` ; `test_sous_module_ignore_par_recursif` ; `test_lien_committe_projete_comme_feuille` |
| P-M5 | `test_forme_fichier_sur_repertoire_refusee` |
| P-T1 | `test_destination_sans_prefixe_scion_refusee` |
| P-T2 | `test_renommage_de_base_repertoire` |
| P-T3 | `test_renommage_de_fichier` ; `test_destination_fichier_pour_recursif_refusee` |
| P-T4 | `test_destination_segment_dot_scion_refusee` ; `test_destination_liste_greffee_refusee` |
| P-X1 | `test_exclusion_toutes_inclusions_ordre_indifferent` |
| P-X2 | `test_exclusion_porte_sur_la_source` |
| P-R1 | `test_inclusion_sans_correspondance_erreur_trunk_retabli` |
| P-R2 | `test_exclusion_sans_correspondance_erreur` |
| P-R3 | `test_meme_source_meme_destination_un_lien` |
| P-R4 | `test_deux_sources_meme_destination_erreur` |
| P-R5 | `test_une_source_deux_destinations` |
| P-R6 | `test_fichier_projete_contre_repertoire_erreur` |
| P-K1 | `test_motif_sensible_a_la_casse` |
| P-K2 | `test_collision_de_casse_projection_contre_scion_erreur` ; `test_collision_de_casse_sur_repertoire` |
| P-V1 | `test_version_tag` ; `test_version_commit` ; `test_version_branche_refusee` ; `test_version_etoile_et_point_d_interrogation_refusees` |
| P-V2 | `test_clone_partiel_blob_none_head_detache` ; `test_meme_prefixe_meme_version_clone_partage` |
| P-V3 | `test_emplacement_local_git_utilise_tel_quel` ; `test_emplacement_local_hors_git_refuse` |
| P-V4 | `test_tag_deplace_arrete_graft_update` ; `test_commit_absent_fetch_puis_erreur` |
| P-V5 | `test_changement_de_version_nouveau_clone` |
| P-E1 | `test_clone_modifie_greffe_refusee` ; `test_clone_hors_commit_refuse` ; `test_non_suivi_ne_bloque_pas` |
| P-P1 | `test_porteur_lu_dot_scion_non_greffe` |
| P-P2 | `test_porteur_scion_ordinaire_refuse` |
| P-P3 | `test_porteur_sixieme_colonne` ; `test_ordre_des_porteurs` |
| P-P4 | `test_double_declaration_identique_admise` ; `test_double_declaration_differente_erreur` |
| P-P5 | `test_porteur_avance_projection_suit` |
| P-P6 | `test_graft_remove_porteur_retire_ses_projections` |
| P-G1 | `test_liens_relatifs_vers_clone_tiers_repertoires_partages` |
| P-G2 | `test_conflit_projection_contre_scion` ; `test_remplacement_local_par_exclusion` |
| P-G3 | `test_proprietaire_repertoire_projete` ; `test_elagage_apres_graft_remove_projection` |
| P-G4 | `test_filtre_ignore_sans_effet_sur_projection` |
| P-G5 | `test_graft_scion_cle_projetee_seule` |
| A.11 | `test_seed_add_clone_projections` ; `test_rootstock_information_compte_projections` ; `test_git_key_cle_projetee` |
| A.12 | `test_messages_citent_fichier_et_ligne` ; `test_verbose_liste_par_ligne` |
| M-D1 | `test_mirrors_dans_porteur` |
| M-D2 | `test_greffe_ne_lit_pas_mirrors` |
| M-D3 | `test_ligne_mirrors_mal_formee` |
| M-D4 | `test_miroir_deux_amonts_erreur` |
| M-D5 | `test_echec_clone_miroir_suggere_mirror_sync` |
| M-C1 | `test_mirror_sync_url_inconnue_erreur_avant_tout` ; `test_mirror_sync_selection` |
| M-C2 | `test_depot_de_travail_refs_amont_separees` |
| M-C3 | `test_seules_branches_et_tags` |
| M-C4 | `test_push_sans_force_ni_suppression` |
| M-C5 | `test_miroir_inaccessible_signale_les_autres_traites` |
| M-C6 | `test_dry_run_rien_envoye` |
| M-R1 à M-R9 | `test_branche_nouvelle`, `test_branche_avance_rapide`, `test_branche_identique`, `test_branche_reecrite_non_envoyee`, `test_branche_supprimee_conservee`, `test_tag_nouveau`, `test_tag_identique`, `test_tag_deplace_non_propage`, `test_tag_supprime_conserve` |
| M-K1 | `test_codes_de_retour_mirror_sync` |
| M-K2 | `test_rien_supprime_ni_reecrit_dans_miroir` |

Contrôle de bout en bout, côté Lepton (ENV-41) : greffe du F4 par projection sur une copie d'essai.
On compare les liens du trunk à `attendus/f4-*.txt`, puis l'oracle (`comparer-oracle.py`, code 0).

## 4. Effets à traiter hors de scion

| Élément | Effet | Étape |
| --- | --- | --- |
| `lepton/__init__.py` `SCION_MIN_VERSION`, `install-vscodium.sh` `SCION_REF`, `README.md` | relever à la version qui porte la projection (Q13) | ENV-41 |
| `lepton/rootstock.py` | lire `.scion.projections` et le `.scion/` des porteurs ; 6ᵉ colonne de la liste greffée (P-P3) ; `seed_dot()` inchangé (5ᵉ colonne = graine) | ENV-41 |
| `seed lock`, `--verify`, `--restore` | inclure les clés projetées des porteurs (commit), sinon GRA-5 n'est pas tenu | ENV-41 |
| `seed status` (`stem`, `role`, `in_seed`) et extension (`srcmap.ts`, `watch.ts`, `pickScion`, `tree.ts:298`) | rôle « projection », `stem` = racine du clone ; correspondance trunk ↔ clone par la table de projection (gdb rend le chemin du clone tiers) | ENV-41 |
| `checks.py` (`check_declared_files`, `check_family_files`, `scion_c_files`) | résoudre `sources` et `inclusions` par le trunk, ou par le porteur et ses projections | ENV-41 |
| `files.py` (`file owner`, `file add [--adopt]`, `file rm/mv`, `dir *`, `graft --path`) | propriétaire d'un lien projeté ; refuser une clé projetée comme cible d'écriture | ENV-41 |
| `seed tree` | propriétaire par la table de projection | ENV-41 |
| `lepton generate` | dossier « git · » d'un clone tiers et `files.exclude` (IDE-4) | ENV-41 |
| `seed new`, `seed add/replace` | rien à recopier : la projection voyage avec la famille (Q9) ; contrôle seulement | ENV-41 |
| hook `proteger-trunk.py` | refuser aussi l'écriture dans un clone projeté (`depots/tiers/…`) | ENV-41 |
| skill `lepton-rootstock` | règle « ne jamais éditer un clone tiers » ; regreffe d'une projection ; exemple de clé périmé (`lepton@bsp::nucleo-f429zi` → `lepton@bsp-nucleo-f429zi`) | ENV-41 |
| `scripts/tiers/verifier-import.sh`, `hal_conf_stm32f4.py` | sans objet pour une projection ; texte de provenance | ENV-41 (PA-69) |
| `LEPTON-PROVENANCE.md`, licences | renvoyés au PA-69 (Q14) ; la ligne de sources du porteur et `seed lock` portent la provenance | ENV-41 |
| miroirs sous `lepton-distribution/` | noms, visibilité, création (hors scion, M-C5) | ENV-40 (PA-68) |
| `ORCHESTRATION.md` §4 PA-63 | libellé « projection dans la graine » : Q9 retient le greffon porteur | ENV-38 (fin de session, PA-64) |
| `etapes/ENV-39`, `ENV-40`, `ENV-41` | relire selon la spécification (porteur, version 0.6.x) avant leur démarrage | début de chacune |

## 5. Ce que le format ne couvre pas

| Cas | Constat | Conséquence |
| --- | --- | --- |
| Fichiers dérivés et modifiés (`radio.c`, `stm32_timer.h`, `subghz.h`, `utilities_conf.h`, `platform.h`) | aucune forme « fichier amont + correctif » | copie dans la famille, exclue de la projection, provenance écrite à la main |
| `stm32_hal_legacy.h` du WL (révision STM32CubeWL, pas celle du dépôt séparé) | une clé n'a qu'une révision | exclu, reste copie ; ou une clé `stm32cubewl::hal-legacy` en forme fichier, ce qui ferait de STM32CubeWL une source de la HAL (contraire à la décision du 2026-11-04) |
| `LICENSE.txt` ×8 du WL | hors amont, origine non établie | restent dans la famille |
| Fichier à blanc dans le nom (`_htmresc/Add button.svg`) | ne s'écrit pas en forme fichier (P-F2) | désignable par joker seulement ; sans objet ici (exclu) |
| Paquet logiciel tiers non git (embOS, archive Segger) | une projection exige un dépôt git (P-V3, P-M4) | hors format |
| Vérification de contenu de la copie par empreinte | n'a plus d'objet : le clone est l'amont | `verifier-import.sh` reste utile pour les copies |
