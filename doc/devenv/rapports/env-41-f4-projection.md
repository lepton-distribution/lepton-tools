# ENV-41 — Famille STM32F4 : copie d'ENV-34 remplacée par la projection

Spécification : `<SEED_SCIONS>/doc/projection-miroir.md` (P-P1 à P-P7, P-V1 à P-V6, M-D1, M-D2).
Cas d'épreuve : `rapports/env-38-projection.md` §2.1 ; effets sur lepton : §4. Essai à blanc :
`rapports/env-39-scion.md` §3.2. Miroirs : `rapports/env-40-miroir.md` §4.
Point de départ : lepton-tools `main` 96a2ffe, `family-stm32f4xx` `master` 0fd8b2a, scion 0.6.1.0,
graine `original-tree` 15740f9 (non modifiée). Branches `devenv/env-41` créées dans les deux.

## 1. Audit (lecture seule) — état au PA-69

Copie d'audit : `~/lepton-tools-dev/essais/env-41-audit` (`cp -RP` de `essais/env-39-copie`, qui
porte déjà la projection F4 avec des URL `file://`, 206 fichiers retirés du clone famille par
`git rm` non commité). Journaux : `rapports/env-41-f4-projection/audit/`.

### 1.1 `scion/.scion/` proposé pour `family-stm32f4xx`

Lignes du §2.1 d'ENV-38, destinations écrites en entier, URL des miroirs (M-D2) ; shelf `tiers`,
clés `stm32f4xx-hal-driver` et `cmsis-device-f4` (celles de l'essai d'ENV-39).

```
# .scion.sources.list
tiers	stm32f4xx-hal-driver	v1.8.5	https://github.com/lepton-distribution/mirror-stm32f4xx-hal-driver.git
tiers	cmsis-device-f4	3c77349ce04c8af401454cc51f85ea9a50e34fc1	https://github.com/lepton-distribution/mirror-cmsis_device_f4.git
# .scion.ramifications
tiers	stm32f4xx-hal-driver	v1.8.5
tiers	cmsis-device-f4	3c77349ce04c8af401454cc51f85ea9a50e34fc1
# .scion.projections  (K = scion/sys/root/src/kernel, D = K/dev/arch/cortexm, écrits en entier)
tiers  stm32f4xx-hal-driver  Inc/**                      D/stm32f4xx/hal_driver/Inc/
tiers  stm32f4xx-hal-driver  Src/**                      D/stm32f4xx/hal_driver/Src/
tiers  stm32f4xx-hal-driver  LICENSE.md                  D/stm32f4xx/hal_driver/
tiers  stm32f4xx-hal-driver  README.md                   D/stm32f4xx/hal_driver/
tiers  cmsis-device-f4       Include/stm32f4xx.h         K/core/ucore/cmsis-5/Device/ST/STM32F4xx/Include/
tiers  cmsis-device-f4       Include/system_stm32f4xx.h  K/core/ucore/cmsis-5/Device/ST/STM32F4xx/Include/
tiers  cmsis-device-f4       Include/stm32f4[23]9xx.h    K/core/ucore/cmsis-5/Device/ST/STM32F4xx/Include/
tiers  cmsis-device-f4       LICENSE.md                  K/core/ucore/cmsis-5/Device/ST/STM32F4xx/
tiers  cmsis-device-f4       README.md                   K/core/ucore/cmsis-5/Device/ST/STM32F4xx/
# .scion.mirrors  (recopié de ~/lepton-tools-dev/essais/env-40-publication/graine/scion/.scion/)
https://github.com/lepton-distribution/mirror-stm32f4xx-hal-driver.git	https://github.com/STMicroelectronics/stm32f4xx-hal-driver.git
https://github.com/lepton-distribution/mirror-cmsis_device_f4.git	https://github.com/STMicroelectronics/cmsis_device_f4.git
```

Miroirs (`git ls-remote`, 2026-11-06) : `refs/tags/v1.8.5^{}` = b6f0ed3829f3… sur le miroir HAL ;
miroir CMSIS device joignable (3c77349 atteignable, contrôlé en ENV-40 §4.2).

### 1.2 Chemins du trunk

| Relevé | Résultat |
| --- | --- |
| `<ROOTSTOCK>` (liste `./chemin -> cible` triée) | 3982 liens, SHA-256 `05b15192d4d4…5da` = ENV-39/40 (`audit/rootstock-liens.txt`) |
| copie d'audit (projection greffée) | mêmes 3982 chemins (`diff` vide) ; 206 cibles sous `depots/tiers/` |
| `LEPTON-PROVENANCE.md` | les deux restent des liens vers le clone famille ; la liste attendue des chemins est donc **identique**, provenances comprises, s'ils sont conservés |
| clones tiers de la copie | HEAD b6f0ed3 et 3c77349, 0 modification de fichier suivi |

### 1.3 Rootstocks qui greffent `family-stm32f4xx`

| Rootstock | Graine | scion de l'hôte |
| --- | --- | --- |
| `<ROOTSTOCK>` | `original-tree` | Mac 0.6.1.0 |
| `essais/env-13-vierge` | `original-tree` | Mac 0.6.1.0 |
| `essais/env-11/f429zi` | graine de projet `env11f4` (URL de la famille, `master`) | Mac 0.6.1.0 |
| copies `essais/env-34-copie`, `env-35-copie`, `env-37-copie`, `env-39-copie` | `original-tree` | Mac 0.6.1.0 (copies d'étape, hors des 7) |
| rootstocks de la VM (`env-14-debian`, `env-28-debian`, `env-36-debian`…) | `original-tree` | VM **0.5.4.0** (R33-1) : un `graft-update` y greffera la famille sans HAL |

Les 4 autres rootstocks d'essai du Mac (`env-9`, `env-11/qemu`, `qemu-gra2`, `wl55jc1`,
`bout-en-bout`) ne greffent pas la famille F4. Aucun modèle de `lepton seed new` ne cite la
famille. Rien n'est regreffé ici hors `<ROOTSTOCK>` (ENV-43 tâche 3).

### 1.4 lepton devant une famille porteuse (essai sur la copie, et lecture du code)

| Commande / élément | Constat | Effet | Taille |
| --- | --- | --- | --- |
| `check` (`checks.py:73` `check_declared_files`) | `sources` résolues dans le clone famille (`m.path.parent`) ; `inclusions` jamais lues | **code 1** : `/sources/5..8` `hal_driver/Src/*.c` « introuvable » (`audit/check.log`) | P : résoudre par le trunk |
| `seed status` (`seed.py:457`) | clés tiers : rôle « sans manifeste », « (hors graine) », `stem` = `<clone>/scion` inexistant | code 0, affichage faux | P |
| `seed tree` (`tree.py`, `files._owners`) | liens projetés sans propriétaire | famille F4 : 66/54 fichiers au lieu de 162/160 | P |
| `file owner` (`files.py:56`, `_ownership`) | remonte au répertoire `hal_driver/` (lien `LEPTON-PROVENANCE.md`) | répond « family-stm32f4xx », `clone_path` inexistant | P à M |
| `file rm/mv`, `graft --path`, `--scion <clé tiers>` | refus, messages faux ; aucune écriture dans un clone tiers | sans danger | P (message « fichier tiers projeté ») |
| `seed lock` / `--verify` / `--restore` (`seed.py:710`) | lit la seule graine : clés projetées absentes du verrou | GRA-5 tenu indirectement (commit de la famille → version tiers épinglée) ; refusé sur la graine de référence | M |
| `generate` (`generate.py:343`, `:384`) | 2 dossiers « git · » tiers ajoutés ; `files.exclude` `scion/[!.]*` ne masque rien d'un clone tiers | code 0 ; clone tiers éditable depuis l'éditeur (IDE-4) | P : omettre ces dossiers |
| `SCION_MIN_VERSION` (`lepton/__init__.py:8`) | (0, 5, 4, 0) ; `SCION_REF` déjà 0.6.1.0 ; `README.md:10` | un scion 0.5.4.0 ignore le porteur | P |
| extension `srcmap.ts:13`, `debug.ts:29` | correspondance clone → trunk par préfixe de `stem` ; un `fullname` gdb sous `depots/tiers/…` resterait tel quel | à l'arrêt, ouverture du fichier du clone tiers (seulement si gdb rend le chemin réel ; les binaires sont compilés par le trunk) | M (table clone → trunk) |
| extension `pickScion`, `tree.ts:298`, `watch.ts` | clés tiers listées « sans manifeste » ; `stem` inexistant | messages faux | P |
| hook `proteger-trunk.py` | ne protège que `trunk/` ; son message renvoie au `realpath` « sous depots/ » = clone tiers pour un lien projeté | pousse à éditer le clone tiers | P |
| skill `lepton-rootstock` | règle 1 « realpath sous depots/, éditer ce chemin-là » (même piège) ; clé périmée `lepton@bsp::nucleo-f429zi` (l. 26) | idem | P |
| `scripts/tiers/compiler-hal-f4-a-blanc.sh` | chemins du trunk seulement | fonctionne tel quel | — |
| `scripts/tiers/verifier-import.sh` | compare une copie dans un clone de greffon | sans objet pour le F4 ; reste utile au F7 et au WL | texte |
| `scripts/tiers/hal_conf_stm32f4.py` | chemin en argument ; docstring et en-tête supposent la copie dans la famille | texte | P |

Aucune exception, aucune écriture de lepton dans `depots/tiers/`. Seul `check` casse ; le reste
est faux sans le signaler.

### 1.5 Propositions soumises au PA-69

1. Lignes du §1.1 telles quelles, `.scion.mirrors` compris (M-D1 : porteur).
2. `LEPTON-PROVENANCE.md` : conservés dans la famille, réécrits (projection, clé, révision,
   miroir ; plus de « copie ») ; `LICENSE.md` et `README.md` : projetés depuis l'amont. Liste des
   chemins du trunk inchangée.
3. `SCION_MIN_VERSION` = (0, 6, 1, 0), aligné sur `SCION_REF` et sur la seule version essayée ;
   rootstocks à scion ancien : aucun traitement ici, lepton refuse un scion < 0.6.1.0, ENV-43
   installe 0.6.1.0 sur la VM avant toute regreffe ; le message du commit de la famille le dit.
4. lepton : `check` par le trunk ; `seed status`, `seed tree`, `file owner` reconnaissent une clé
   projetée (rôle « projection », propriétaire = clé tiers, refus d'écriture explicite) ;
   `generate` omet les dossiers « git · » des clones tiers ; tests. Hors étape, consignés en
   résidus : `seed lock` des clés projetées, table de correspondance de l'extension.
5. Hook : refuser aussi `<rootstock>/depots/tiers/`, message corrigé ; skill : règle « jamais
   sous `depots/tiers/` », clé d'exemple corrigée ; `verifier-import.sh` conservé (F7, WL),
   texte de `hal_conf_stm32f4.py` corrigé ; `compiler-hal-f4-a-blanc.sh` inchangé.

### 1.6 Décisions du PA-69 (utilisateur, 2026-11-06)

1. Lignes du §1.1 acceptées, `.scion.mirrors` compris.
2. `LEPTON-PROVENANCE.md` conservés et réécrits ; `LICENSE.md`, `README.md` projetés ; liste des
   chemins du trunk strictement inchangée.
3. `SCION_MIN_VERSION` = (0, 6, 1, 0) ; rootstocks à scion ancien : rien ici (ENV-43).
4. lepton : **périmètre complet** — proposition 4 plus `seed lock`/`--verify`/`--restore` des clés
   projetées et, dans l'extension, la table clone tiers → trunk (`srcmap`, `debug`), `pickScion`,
   `watch`, `revealInClone`.
5. Proposition 5 acceptée (hook, skill, scripts).

## 2. Oracle avant

`rapports/oracles/env-41-avant/` : `rejouer-oracle.sh <ROOTSTOCK> … --qemu` ×6 `--carte` ×10
(constructions à neuf, `rejouer-oracle.log`) : « tout a réussi ». Contre `env-37-avant`
(`env-41-avant/comparaisons/`) : `comparer-oracle.py` code 0 ×16 ; host 7/7 ; empreintes mklepton
identiques ; bancs KAL QEMU identiques (mêmes cas et résultats, rangs et durées ignorés). Listes
`ctest -N` (`env-41-avant/ctest-N/`, `ctest --preset <P> -N` depuis `<ROOTSTOCK>/trunk`) : 17/17
identiques.

Relevés de `<ROOTSTOCK>` juste avant la bascule (`env-41-f4-projection/avant/`) : espace de travail
régénéré par `lepton generate` (code 0) puis copié ; `lepton check` code 0 ; liste des liens
3982, SHA-256 `05b15192…` (`trunk-liens.txt`).

## 3. Bascule

### 3.1 Famille (`family-stm32f4xx`, branche `devenv/env-41`)

Commits faits dans le clone de la copie d'essai, puis repris dans `<ROOTSTOCK>` (§3.5) :

| Commit | Contenu |
| --- | --- |
| 5218b05 | `scion/.scion/` : `.scion.sources.list`, `.scion.ramifications`, `.scion.projections` (§1.1), `.scion.mirrors` recopié de la graine de publication d'ENV-40 ; message : scion ≥ 0.6.1.0 exigé |
| a8c7131 | mécanique : `git rm -r` de `hal_driver/Inc`, `Src`, `LICENSE.md`, `README.md` (200 fichiers) |
| ec15c06 | mécanique : `git rm -r` du CMSIS device `Include/`, `LICENSE.md`, `README.md` (6 fichiers) |
| dfb4528 | `LEPTON-PROVENANCE.md` ×2 réécrits (projection, clé, révision, miroir) ; `description` du manifeste ; `sources` et `compilation` inchangés |

Aucun répertoire résiduel après `git rm` (pas de `.DS_Store` sous `Inc/`, `Src/`, `Include/`).

### 3.2 lepton-tools (`devenv/env-41`), PA-69 point 4 et 5

- `lepton/rootstock.py` : 6ᵉ colonne (`GraftedEntry.porter`, `dot`) ; `projected_keys()`,
  `porter_of()`, `projection_tables()` (table clone tiers → trunk tirée des liens du trunk, sans
  relire les motifs) ; `Manifest.trunk_dir`.
- `lepton/checks.py` : un fichier déclaré absent du clone est cherché dans le trunk (`_declared`),
  pour `sources`, champs de fichiers et `scion_c_files`.
- `lepton/files.py` : propriétaire d'une clé projetée = racine du clone tiers ; `clone_path` = cible
  du lien ; refus explicite d'écrire (`refuse_projected`) ; dans un répertoire partagé, un fichier
  nouveau va au seul greffon ordinaire ; `file owner --json` : `projected_by`.
- `lepton/seed.py` : `seed status` rôle « projection », origine et version du porteur,
  `projected_by`, `root`, `projection` ; `seed lock` fige les clés projetées (`projected_by`),
  `--verify` les compare, `--restore` ne les déplace jamais et signale l'écart.
- `lepton/generate.py` : pas de dossier « git · » pour une clé projetée.
- `lepton/__init__.py` : `SCION_MIN_VERSION` (0, 6, 1, 0) ; `README.md`.
- Extension : `srcmap.ts` (table fichier par fichier des clés projetées), `debug.ts`, `lepton.ts`
  (types), `watch.ts` (pas d'observateur sur un clone tiers), `tree.ts` (`revealInClone`),
  `commands.ts` (`pickScion` sans clé projetée).
- Hook `proteger-trunk.py` : refuse aussi `<rootstock>/depots/tiers/` (message propre), message du
  trunk corrigé ; essai sur 10 cas conforme. Le hook lit le texte des commandes : un script qui
  contient ces chemins passe par un fichier (constaté deux fois pendant la session).
- Skill `lepton-rootstock` : section « Projection », règle 1 corrigée, clé `lepton@bsp-nucleo-f429zi`.
- `scripts/tiers/` : aide de `hal_conf_stm32f4.py` et de `verifier-import.sh` ; en-tête généré
  inchangé (les `stm32f4xx_hal_conf.h` des BSP ne changent pas) ; `compiler-hal-f4-a-blanc.sh`
  inchangé.
- Tests : `tests/test_projection.py` (8 tests, scion réel, dépôt tiers factice) ; extension :
  `srcmap.test.ts` (22/22).

### 3.3 Copie d'essai `~/lepton-tools-dev/essais/env-41-copie`

`rsync -a` de `<ROOTSTOCK>` sans `build/` ni `third_party/` ; commits du §3.1 ; `scion seed-clone
--seed depots/lepton-seed.scions/original-tree` (clones tiers depuis les miroirs GitHub) puis
`scion graft` : code 0, 3982 feuilles (`env-41-f4-projection/copie/`).

| Contrôle | Résultat |
| --- | --- |
| chemins du trunk | 3982, identiques à l'avant (0 retiré, 0 ajouté) ; SHA-256 de la liste `d9f4ea56…` = essai à blanc d'ENV-39 |
| cibles changées | 206, toutes sous `depots/tiers/` ; liste = `env-38-projection/attendus/f4-*.txt` |
| fichiers réguliers, liens cassés | 0, 0 |
| contenu des 206 | = `git cat-file HEAD:<chemin>` du clone tiers, et = fichier du trunk de `<ROOTSTOCK>` (copie d'ENV-34) : 0 écart |
| casse | nom du lien = nom suivi par git dans le clone : 0 écart |
| clones tiers | HEAD b6f0ed3 et 3c77349, `origin` = miroirs, 0 modification, `partialclonefilter` `blob:none` |
| `lepton check` / `generate` (sources) | code 0 / code 0 ; espace = avant aux chemins des schémas près (lepton de développement contre pipx) |
| `seed status` / `seed tree` | 2 clés « projection » (200 et 6 fichiers) ; F4 66/54 + HAL 96/102 + CMSIS 0/4 = 162/160 comme avant |

### 3.4 Rootstock neuf `~/lepton-tools-dev/essais/env-41-vierge`

Graine d'essai locale `essais/env-41-vierge-graine` (clone d'`original-tree`, branche
`devenv/env-41` c85ba56, jamais publiée) : `family-stm32f4xx` en `file://` de la branche
`devenv/env-41` du clone de la copie. `scion rootstock-install`, `seed-add --version devenv/env-41
file://…`, `graft` : code 0, 3982 feuilles, 16 entrées dont 2 à 6 colonnes. Chemins identiques à
l'avant ; 0 lien cassé, 0 fichier régulier ; 206 fichiers projetés = HEAD des clones tiers ; les
3 seuls contenus différents de `<ROOTSTOCK>` sont les 3 fichiers modifiés du §3.1 ; `lepton check`
code 0 (`env-41-f4-projection/vierge/`).

### 3.5 `<ROOTSTOCK>` (accord PA-P de l'utilisateur, 2026-11-06)

Journaux : `env-41-f4-projection/rootstock/`.

| Action | Résultat |
| --- | --- |
| `git fetch` des 4 commits du clone de la copie, `merge --ff-only` | `family-stm32f4xx` `devenv/env-41` = dfb4528, propre, aucun répertoire résiduel |
| `scion seed-clone --seed depots/lepton-seed.scions/original-tree` | code 0 ; `depots/tiers/stm32f4xx-hal-driver/v1.8.5`, `depots/tiers/cmsis-device-f4/3c77349…` (origine = miroirs) |
| `scion graft` (ni `graft-update` ni `seed-update`) | code 0, 3982 feuilles ; liste greffée 16 entrées, 2 à 6 colonnes |
| liste des liens | 3982 chemins identiques à l'avant, SHA-256 `d9f4ea56…` (= copie) ; 206 cibles vers `depots/tiers/` ; 0 fichier régulier, 0 lien cassé ; clone noyau propre |
| contenu, casse | 206 fichiers = `HEAD` des clones tiers (b6f0ed3, 3c77349), 0 écart ; 0 écart de casse |
| `pipx install --force "git+file://<LEPTON_TOOLS>@devenv/env-41"` | `lepton --version` : scion 0.6.1.0 (requis ≥ 0.6.1.0) |
| `codium --install-extension extension/dist/lepton-0.5.2.vsix --force` | `lepton-distribution.lepton@0.5.2` |
| `lepton check`, `lepton generate`, `seed status` | code 0, 0, 0 ; espace de travail **identique** à celui régénéré avant la bascule |

## 4. Contrôles (PA-70)

### 4.1 Oracle après

`rapports/oracles/env-41-apres/` : mêmes commandes qu'au §2, constructions à neuf sur `<ROOTSTOCK>`
basculé : « tout a réussi ». Contre `env-41-avant` (`env-41-apres/comparaisons/`) :

| Preset | Sections/symboles | Empreinte | Fumée | Banc KAL | Écarts expliqués |
| --- | --- | --- | --- | --- | --- |
| host | — | mklepton identiques | — | ctest 7/7 | — |
| qemu-mps2-an386-embos, -embos-soft, -freertos, -freertos-soft | code 0 ×4 | différente (attendu) | ok | 19, 15, 19, 15 ; mêmes cas, 100 % | aucun |
| qemu-mps2-an500-embos, -freertos | code 0 ×2 | différente (attendu) | ok | 18, 18 ; mêmes cas, 100 % | aucun |
| nucleo-f429zi, nucleo-f439zi (embos, freertos) | code 0 ×4 | différente (attendu) | — | — | aucun ; `depots/tiers` absent des 4 binaires (`strings`) |
| nucleo-wl55jc1, stm32f746g-disco, samd21-xplained-pro (×2) | code 0 ×6 | différente (attendu) | — | — | aucun |

Listes `ctest -N` : 17/17 identiques. Empreintes : les `.bin` diffèrent entre deux constructions à
neuf pour **tous** les presets, touchés ou non, et différaient déjà entre `env-37-avant` et
`env-41-avant` : constructions non reproductibles octet pour octet, admis par la skill
`lepton-oracle` (sections et symboles décident). Rangs et durées des bancs ignorés.

### 4.2 Bilan des critères

| Critère | Résultat |
| --- | --- |
| PA-69 et PA-70 tranchés et consignés | PA-69 oui (§1.6) ; PA-70 : ce rapport |
| Binaires identiques sur host et les 16 presets (code 0) | oui |
| Liste des chemins du trunk identique, aux écarts accordés près | oui, aucun écart (3982 chemins ; provenances conservées) |
| Plus aucun fichier de la HAL ni du CMSIS device F4 dans le clone `family-stm32f4xx` | oui : il reste les 2 `LEPTON-PROVENANCE.md` (PA-69) |
| Fichiers projetés identiques octet pour octet à `v1.8.5` et `3c77349` | oui : 206/206 = `git cat-file HEAD:` des clones épinglés |
| Rootstock neuf conforme depuis la graine de la branche | oui (§3.4) |
| `lepton check` / `generate` sur `<ROOTSTOCK>`, espace identique ; `pytest` vert | oui ; 243 réussis (235 + 8) ; extension 22/22 |

### 4.3 Graines de projet à traiter en ENV-43

- Rootstocks du Mac qui greffent `family-stm32f4xx` : `essais/env-13-vierge` (`original-tree`),
  `essais/env-11/f429zi` (graine `env11f4`). Leur clone famille est sur `master` 0fd8b2a : rien ne
  change tant que la famille publiée n'avance pas ; un `graft-update` après publication exige
  scion ≥ 0.6.1.0 (installé sur le Mac) et clonera les 2 dépôts tiers depuis les miroirs.
- VM : scion 0.5.4.0 → installer 0.6.1.0 (et lepton) **avant** toute regreffe d'un rootstock qui
  greffe la famille, sinon la famille est greffée sans HAL.
- Copies d'étape (`env-34-copie`, `env-35-copie`, `env-37-copie`, `env-39-copie`) : hors des 7.

### 4.4 Résidus et observations

- `seed replace`/`seed remove` d'un greffon porteur : retrait et regreffe des clés projetées laissés
  à scion (P-P6) ; non essayé ici (aucune graine de projet ne remplace la famille F4).
- Extension 0.5.2 : la table clone tiers → trunk n'agit que si gdb rend le chemin réel ; les
  binaires F4 sont compilés par le trunk (aucun `depots/tiers` dans les binaires), l'effet n'a pas
  été observé en session de débogage réelle (pas de carte flashée dans cette étape).
- Hook : il lit le texte des commandes shell ; un script qui contient `trunk/` ou `depots/tiers/`
  après un verbe d'écriture est refusé même s'il n'écrit pas dans ces chemins (deux fois ici) ;
  parade : passer par un fichier.
