# ENV-47 — Famille STM32F7 : copie remplacée par la projection

Session du 2026-11-10. Archétype : migration iso-fonctionnelle (binaires identiques). Modèle :
`rapports/env-41-f4-projection.md`. Relevés : `env-47-f7-projection/`.

## 1. Audit (lecture seule) — état au PA-81

### 1.0 Point de départ
- lepton-tools `main` 3d6304c ; `family-stm32f7xx` `master` d2d9aa9 ; F4 acdd24c ; clone noyau
  76f28bd ; graine `original-tree` 15740f9 (F7 déclarée en `master`,
  `https://github.com/lepton-distribution/lepton-famille-stm32f7xx.git`) ; BSP F746 6266908 ;
  tous propres, = distant.
- scion 0.6.2.0, lepton 0.1.0 ; `pushInsteadOf` global `ssh://git@github.com/` ← `https://github.com/`
  présent (PA-68).
- Sondes visibles : NUCLEO-F429ZI, WL55 A et B. STM32F746G-DISCO **non visible**.

### 1.1 Copie actuelle contre l'amont
| Contrôle | Résultat |
| --- | --- |
| `verifier-import.sh tiers/stm32f7xx-hal-driver v1.3.3 …/hal_driver` | code 0 ; 196 OK, 0 écart (e1446fa) — `audit/verifier-hal.txt` |
| `verifier-import.sh tiers/cmsis_device_f7 v1.2.10 …/STM32F7xx env-34-hal-f4/listes/cmsis-device-f7.txt` | code 0 ; 5 OK (2352e88) — `audit/verifier-cmsis-device.txt` |
| Motifs proposés (§1.3) appliqués à l'amont (`ls-tree` du tag) | 196 + 5 = `env-38-projection/attendus/f7-*.txt` (`cmp`) |
| Noms suivis par git dans la famille, hors `LEPTON-PROVENANCE.md` | 201 = attendus, casse comprise (`audit/famille-suivis.txt`) |
| Restent dans la famille hors projection | 2 `LEPTON-PROVENANCE.md` |

Amonts (2026-11-10, `git ls-remote`) : HAL 8 tags annotés, dernier `v1.3.3` (e1446fa), `master`
e860c4f (`v1.3.3-19`) ; CMSIS device 7 tags annotés, dernier `v1.2.10` = `master` 2352e88. Les
miroirs `lepton-distribution/mirror-stm32f7xx-hal-driver` et `mirror-cmsis_device_f7` n'existent
pas (`gh repo view`). Le clone amont local de la HAL est à HEAD e860c4f, pas au tag : les
comparaisons se font contre le tag.

### 1.2 Trunk de `<ROOTSTOCK>`
`env-43-mac/controler-trunk.py` (lecture seule) : 3887 liens, 0 fichier régulier, 0 lien cassé ;
206 projetés (F4), contenu = HEAD, 0 écart de casse ; liste `chemin -> cible`
`audit/rootstock/liens.txt` (SHA-256 `6cd0c0d4…`, chemins seuls `c65ee399…`). 203 liens visent la
copie F7 (201 fichiers tiers + 2 provenances).

Attendu après bascule : 3887 chemins **identiques** ; 201 cibles changées, de
`depots/lepton/family-stm32f7xx/master/scion/…` vers `depots/tiers/stm32f7xx-hal-driver/v1.3.3/…`
et `depots/tiers/cmsis-device-f7/v1.2.10/…` ; 407 projetés en tout ; les 2 provenances restent
liées à la famille.

### 1.3 `scion/.scion/` proposé pour `family-stm32f7xx`
Même forme que le porteur F4 (ENV-41 §1.1). Les versions sont des tags, qui existent ici, à la
différence du CMSIS device F4.

```
# .scion.sources.list
tiers	stm32f7xx-hal-driver	v1.3.3	https://github.com/lepton-distribution/mirror-stm32f7xx-hal-driver.git
tiers	cmsis-device-f7	v1.2.10	https://github.com/lepton-distribution/mirror-cmsis_device_f7.git

# .scion.ramifications
tiers	stm32f7xx-hal-driver	v1.3.3
tiers	cmsis-device-f7	v1.2.10

# .scion.projections  (écrits en entier dans le fichier)
tiers  stm32f7xx-hal-driver  Inc/**                      scion/sys/root/src/kernel/dev/arch/cortexm/stm32f7xx/hal_driver/Inc/
tiers  stm32f7xx-hal-driver  Src/**                      scion/sys/root/src/kernel/dev/arch/cortexm/stm32f7xx/hal_driver/Src/
tiers  stm32f7xx-hal-driver  LICENSE.md                  scion/sys/root/src/kernel/dev/arch/cortexm/stm32f7xx/hal_driver/
tiers  stm32f7xx-hal-driver  README.md                   scion/sys/root/src/kernel/dev/arch/cortexm/stm32f7xx/hal_driver/
tiers  cmsis-device-f7       Include/stm32f7xx.h         scion/sys/root/src/kernel/core/ucore/cmsis-5/Device/ST/STM32F7xx/Include/
tiers  cmsis-device-f7       Include/system_stm32f7xx.h  scion/sys/root/src/kernel/core/ucore/cmsis-5/Device/ST/STM32F7xx/Include/
tiers  cmsis-device-f7       Include/stm32f746xx.h       scion/sys/root/src/kernel/core/ucore/cmsis-5/Device/ST/STM32F7xx/Include/
tiers  cmsis-device-f7       LICENSE.md                  scion/sys/root/src/kernel/core/ucore/cmsis-5/Device/ST/STM32F7xx/
tiers  cmsis-device-f7       README.md                   scion/sys/root/src/kernel/core/ucore/cmsis-5/Device/ST/STM32F7xx/

# .scion.mirrors
https://github.com/lepton-distribution/mirror-stm32f7xx-hal-driver.git	https://github.com/STMicroelectronics/stm32f7xx-hal-driver.git
https://github.com/lepton-distribution/mirror-cmsis_device_f7.git	https://github.com/STMicroelectronics/cmsis_device_f7.git
```

Clés `cmsis-device-f7` (trait d'union, comme `cmsis-device-f4` et le §2.2 d'ENV-38), miroir au nom
de l'amont (`cmsis_device_f7`, comme le F4). Clones attendus : `depots/tiers/stm32f7xx-hal-driver/v1.3.3`,
`depots/tiers/cmsis-device-f7/v1.2.10`.

### 1.4 Rootstocks et graines qui greffent `family-stm32f7xx`
Tous en version `master` (d2d9aa9). Rien ne change pour eux tant que la famille publiée n'avance
pas. Leur regreffe relève d'ENV-50.

| Hôte | Rootstock | Graine | scion | Remarque |
| --- | --- | --- | --- | --- |
| Mac | `<ROOTSTOCK>` | `original-tree` | 0.6.2.0 | basculé ici (PA-P) |
| Mac | `essais/env-13-vierge` | `original-tree` | 0.6.2.0 | un des 7 regreffés en ENV-43 (`graft-update`) → ENV-50 |
| Mac | `essais/env-41-vierge` | `env-41-vierge-graine` (locale) | 0.6.2.0 | rootstock neuf d'ENV-41 gardé |
| Mac | `essais/env-34-copie`, `env-35-copie`, `env-37-copie`, `env-39-copie` | `original-tree` | 0.6.2.0 | copies d'étape, jamais regreffées (hors des 7 d'ENV-43) |
| VM | `essais/env-28-debian`, `essais/env-43-debian` | `original-tree` | 0.6.1.0 | ENV-50 installe 0.6.2.0 avant toute regreffe |

Les 6 autres rootstocks d'essai du Mac (`env-9`, `env-11/*`) ne greffent pas le F7. Aucune graine
de projet ne greffe le F7 aujourd'hui.

### 1.5 Rootstock à graine de projet (tâche 3)
`seed lock` refuse toute graine sans `graine.json` ni `project/` (`refuse_reference`,
`lepton/seed.py:565`). Cela vaut pour `<ROOTSTOCK>` comme pour un rootstock neuf tiré d'une copie
d'`original-tree`. Aucun rootstock existant n'a de graine de projet qui greffe le F7.

Proposition : après la bascule de la copie d'essai (tâche 5.1) et la publication des miroirs
(tâche 2), créer `essais/env-47-projet` par la commande suivante :

```
lepton seed new f746 -C essais/env-47-projet --bsp stm32f746g-disco \
  --mkconf sys/user/tauon-basic/etc/mkconf_tauon_basic_stm32f746g_disco.xml \
  --origin family-stm32f7xx=file://<copie>/depots/lepton/family-stm32f7xx/master@devenv/env-47 \
  --origin bsp-stm32f746g-disco=https://github.com/lepton-distribution/lepton-bsp-stm32f746g-disco.git@master
```

Le noyau vient de l'origine par défaut. Les clones tiers sont créés depuis les miroirs. Ce
rootstock sert à `seed lock` et `seed lock --verify` (clés F7 figées) ; il est supprimé au PA-82.

### 1.6 lepton, extension, hook, skill, scripts
- lepton, extension, hook : aucune mention propre au F4 ou au F7. Les clés projetées sont traitées
  de façon générique depuis ENV-41 (`rootstock.py`, `files.py`, `seed.py`, `generate.py`,
  `srcmap.ts`). Aucune modification n'est nécessaire.
- La skill `lepton-rootstock` cite `family-stm32f4xx` comme exemple de porteur : c'est exact, et
  rien n'est à changer.
- L'aide de `scripts/tiers/verifier-import.sh` (l. 15-17) dit : « Sert aux copies … (familles
  STM32F7 et STM32WL) ». Après la bascule, ce n'est plus vrai pour le F7.
- Le BSP F746 (`stm32f7xx_hal_conf.h`, `stm32f746g_disco.h`) cite le modèle de la HAL et
  STM32CubeF7 v1.17.4. Ces références restent vraies : les modèles sont projetés (`Inc/**`).
- Manifeste de la famille : `description` cite la HAL « STM32CubeF7 1.17.4 (hal_driver) » sans
  dire qu'elle est projetée. `sources` (4 fichiers `hal_driver/Src/…`) et `compilation` restent
  inchangés, car ils sont résolus par le trunk depuis ENV-41.

### 1.7 Propositions soumises au PA-81
1. Lignes du §1.3 : clés, tags `v1.3.3` et `v1.2.10`, motifs, URL des miroirs.
2. Miroirs `lepton-distribution/mirror-stm32f7xx-hal-driver` et
   `lepton-distribution/mirror-cmsis_device_f7`, forme du PA-68 :
   - publics ;
   - description GitHub seule, « Miroir de conservation de <amont> (avance rapide seulement, scion
     mirror-sync) », aucun commit ajouté ;
   - créés par la session (`gh repo create --public`, sans README ni licence) ;
   - première synchronisation par la graine de publication d'ENV-40 (E13) : 2 lignes ajoutées à
     son `.scion.mirrors`, puis `mirror-sync --seed`, et seulement ensuite le porteur (PA-P).
3. `LEPTON-PROVENANCE.md` ×2 conservés dans la famille et réécrits, forme du PA-69 (projection,
   clé, révision, miroir, scion ≥ 0.6.1.0). `LICENSE.md` et `README.md` projetés depuis l'amont.
   Liste des chemins du trunk strictement inchangée.
4. `description` du manifeste réécrite, forme du F4 ; `sources` et `compilation` inchangés.
5. lepton, extension, hook, skill : aucune modification. lepton-tools : l'aide de
   `verifier-import.sh` est corrigée (F7 projeté depuis ENV-47, WL seul en copie jusqu'à ENV-48),
   dans un commit dédié.
6. Rootstock à graine de projet du §1.5.
7. Regreffe comme en ENV-41 §3.5 : sur la copie d'essai d'abord, puis sur un rootstock neuf (graine
   d'essai locale, famille en `file://` de `devenv/env-47`), puis sur `<ROOTSTOCK>` (PA-P), par
   `seed-clone --seed …/original-tree` et `graft`, sans `graft-update` ni `seed-update`.
8. Banc STM32F746G-DISCO : uniquement si la carte est branchée (PA-11).

### 1.8 Décisions du PA-81 (utilisateur, 2026-11-10)
- Propositions 1 à 7 acceptées telles quelles. Cela comprend l'accord PA-P pour `gh repo create`
  des deux miroirs et leur synchronisation (push).
- Proposition 8 : la STM32F746G-DISCO sera branchée par l'utilisateur ; écriture flash accordée
  (PA-11) pour le banc du §6.

## 2. Miroirs (accord PA-P du PA-81)

Journaux : `env-47-f7-projection/miroirs/`.

| Action | Résultat |
| --- | --- |
| `gh repo create lepton-distribution/mirror-stm32f7xx-hal-driver`, `…/mirror-cmsis_device_f7` (`--public`, description seule) | créés, vides, publics ; branche par défaut `master` après envoi |
| 2 lignes F7 ajoutées au `.scion.mirrors` de `essais/env-40-publication/graine/scion/.scion/` (avant : `audit/publication-mirrors-avant.txt`) | 4 lignes (F4, F7) |
| `scion mirror-sync rootstock --seed graine --dry-run` | code 0 ; F7 : 9 et 8 références « à envoyer » (`master` + 8 tags, `master` + 7 tags) ; F4 : 0 |
| `scion mirror-sync rootstock --seed graine` | code 0 ; 9 et 8 références envoyées, 0 signalement ; F4 : 0 |
| seconde passe | code 0 ; 0 référence envoyée sur les 4 miroirs |
| `git ls-remote --heads --tags` miroir contre amont | identiques (`cmp`) : 17 et 15 lignes ; `v1.3.3^{}` = e1446fa, `v1.2.10^{}` = 2352e88 |

## 3. Rootstock à graine de projet `essais/env-47-projet`

Créé après la bascule de la copie (§5.1) et la publication des miroirs (§2). Journaux :
`env-47-f7-projection/projet/`.

| Action | Résultat |
| --- | --- |
| `lepton seed new f746 -C essais/env-47-projet --bsp stm32f746g-disco --mkconf sys/user/tauon-basic/etc/mkconf_tauon_basic_stm32f746g_disco.xml --origin stm32f7xx=file://localhost/…/env-47-copie/depots/lepton/family-stm32f7xx/master@devenv/env-47 --origin stm32f746g-disco=https://github.com/lepton-distribution/lepton-bsp-stm32f746g-disco.git@master` | code 0. Un premier essai avec les clés scion (`family-stm32f7xx=…`) a été refusé (code 1) avant toute création : `--origin` attend le **nom** du greffon |
| liste greffée | 7 entrées, dont `tiers stm32f7xx-hal-driver v1.3.3` et `tiers cmsis-device-f7 v1.2.10` à 6 colonnes ; 3266 liens, 0 cassé, 0 fichier régulier |
| `lepton check` / `seed status` | code 0 (5 fichiers conformes) / code 0 : 2 clés « projection » (196 et 5 fichiers, projetées par `stm32f7xx`) |
| `lepton seed lock --no-cmake` | code 0 ; `lepton-graine.lock.json` : `tiers@stm32f7xx-hal-driver` `v1.3.3` e1446fa et `tiers@cmsis-device-f7` `v1.2.10` 2352e88, `projected_by` `lepton@family-stm32f7xx` (`projet/verrou.json`) |
| `lepton seed lock --verify` | code 0, « clones conformes au verrou » |

## 4. Oracle avant

`rapports/oracles/env-47-avant/` : `env-46-spl/oracle-complet.sh <ROOTSTOCK>`, repris sans
changement. Il relève les chemins du trunk, lance `rejouer-oracle.sh` (6 presets QEMU, 10 de carte,
constructions à neuf ; « tout a réussi »), puis `ctest -N`. La comparaison à `oracles/env-46-apres/`
se fait par `env-46-spl/comparer.sh` (journal `env-47-f7-projection/oracle-avant.out`) :

| Preset | Sections/symboles | Fumée | Banc KAL |
| --- | --- | --- | --- |
| host | mklepton identiques ; ctest 7/7 | — | — |
| 6 QEMU (an386 ×4, an500 ×2) | code 0 ×6 | identique | identique (19, 15, 19, 15, 18, 18) |
| 10 de carte (F429, F439, WL55, F746, SAMD21 ; embOS et FreeRTOS) | code 0 ×10 | — | — |

- `ctest -N` : 17/17 identiques.
- Trunk : 3887 chemins (`c65ee399…`), liste `chemin -> cible` `6cd0c0d4…`, égale au relevé de
  l'audit (§1.2) ; 0 anomalie.
- Éléments ignorés par `comparer-journaux.py` : date de compilation, jeton `lepton-uart1-<n>`,
  `rcv SIGCHLD`, lignes vides.

## 5. Bascule

### 5.1 Famille (`family-stm32f7xx`, branche `devenv/env-47`) et copie d'essai

La copie d'essai `essais/env-47-copie` est faite par `rsync -a` de `<ROOTSTOCK>`, sans `build/` ni
`third_party/` : 3887 liens, 0 cassé. Commits dans son clone famille :

| Commit | Contenu |
| --- | --- |
| 0c640c0 | `scion/.scion/` : `.scion.sources.list`, `.scion.ramifications`, `.scion.projections`, `.scion.mirrors` (§1.3), même nombre de champs que le F4 ; le message dit que scion ≥ 0.6.1.0 est exigé |
| bf5a669 | mécanique : `git rm -r` de `hal_driver/Inc`, `Src`, `LICENSE.md`, `README.md` (196 fichiers) |
| 91f2328 | mécanique : `git rm -r` du CMSIS device `Include/`, `LICENSE.md`, `README.md` (5 fichiers) |
| a13b162 | `LEPTON-PROVENANCE.md` ×2 réécrits (projection, clé, révision, miroir, scion ≥ 0.6.1.0) ; `description` du manifeste ; `sources` et `compilation` inchangés |

Aucun répertoire résiduel après `git rm`. Ne restent sous `hal_driver/` et `STM32F7xx/` que les
2 `LEPTON-PROVENANCE.md`.

Regreffe de la copie (journaux `env-47-f7-projection/copie/`) :
- `scion seed-clone --seed depots/lepton-seed.scions/original-tree` : code 0. Il crée
  `depots/tiers/stm32f7xx-hal-driver/v1.3.3` et `depots/tiers/cmsis-device-f7/v1.2.10` depuis les
  miroirs.
- `scion graft` : code 0 ; 3887 feuilles ; 18 entrées dans la liste greffée. 26 chemins sont
  ignorés par git, tous des `.DS_Store` (`copie/graft-ignores.txt`).

| Contrôle | Résultat |
| --- | --- |
| `controler-trunk.py` contre `attendu-liens-apres.txt` (liste du §1.2, 201 cibles réorientées par `attendu-apres.py`) | **CONFORME** : liste `chemin -> cible` identique (3887, `70cc91c2…`) ; chemins seuls `c65ee399…` = avant |
| fichiers réguliers, liens cassés | 0, 0 |
| projetés | 407 (206 F4 + 201 F7) ; 0 nom absent du HEAD (casse) ; 0 contenu ≠ blob du HEAD |
| clones tiers F7 | HEAD e1446fa et 2352e88 ; `origin` = miroirs ; 0 modification ; filtre `blob:none` |
| contenu des 201 contre l'ancienne copie (trunk de `<ROOTSTOCK>`) | 201 comparés (`cmp`), 0 écart |
| `lepton check` | code 0 (19 fichiers conformes) |
| `lepton seed status` | `stm32f7xx-hal-driver` projection v1.3.3 e1446fa (196 fichiers) ; `cmsis-device-f7` projection v1.2.10 2352e88 (5) ; « projeté par stm32f7xx » |
| `lepton file owner` (chemins absolus du trunk) | `…/hal_driver/Src/stm32f7xx_hal_gpio.c` → `tiers@stm32f7xx-hal-driver, projeté par stm32f7xx` ; `…/Include/stm32f746xx.h` → `tiers@cmsis-device-f7` ; `…/hal_driver/LEPTON-PROVENANCE.md` → `lepton@family-stm32f7xx` |
| `lepton generate` | code 0 ; aucun dossier « git · » pour les clés projetées |

### 5.2 Rootstock neuf `essais/env-47-vierge`

La graine d'essai locale `essais/env-47-vierge-graine` est un clone de `original-tree` 15740f9
depuis GitHub. Sa branche `devenv/env-47` (4651fbe) n'est pas publiée. La famille F7 y est déclarée
en version `devenv/env-47`, en `file://localhost/…/env-47-copie/depots/lepton/family-stm32f7xx/master`.

Commandes, toutes à code 0 : `scion rootstock-install`, `seed-add --version devenv/env-47
file://localhost/…/env-47-vierge-graine`, `graft`. Résultat : 3887 feuilles, 18 entrées.

| Contrôle | Résultat |
| --- | --- |
| chemins | 3887, identiques à l'avant (`c65ee399…`) ; 0 ajouté, 0 retiré |
| cibles | 11 lignes diffèrent de l'attendu : les 11 fichiers propres à la famille F7, liés sous `depots/lepton/family-stm32f7xx/devenv/env-47/` (clone rangé sous le nom de la version, comme en ENV-46) ; `vierge/cibles-differentes.txt` |
| projetés | 407, mêmes chemins que la copie ; contenu = HEAD ; 0 écart de casse ; clones tiers aux commits épinglés, `origin` = miroirs |
| contenu des 3887 fichiers contre la copie | 0 écart |
| fichiers réguliers, liens cassés | 0, 0 |
| `lepton check` | code 0 |

### 5.3 `<ROOTSTOCK>` (accord PA-P de l'utilisateur, 2026-11-10)

Journaux : `env-47-f7-projection/rootstock/`.

Relevé juste avant la bascule (`rootstock/avant/`) : `lepton generate` code 0, espace copié ;
`lepton check` code 0 (19 fichiers conformes).

| Action | Résultat |
| --- | --- |
| `git fetch` des 4 commits du clone de la copie, `switch -c devenv/env-47`, `merge --ff-only` | `family-stm32f7xx` `devenv/env-47` = a13b162, propre ; seuls les 2 `LEPTON-PROVENANCE.md` restent sous `hal_driver/` et `STM32F7xx/` |
| `scion seed-clone --seed depots/lepton-seed.scions/original-tree` | code 0 ; `depots/tiers/stm32f7xx-hal-driver/v1.3.3`, `depots/tiers/cmsis-device-f7/v1.2.10` (origine = miroirs) |
| `scion graft` (ni `graft-update` ni `seed-update`) | code 0 ; 3887 feuilles ; 18 entrées ; 26 `.DS_Store` ignorés |
| `controler-trunk.py` contre `attendu-liens-apres.txt` | **CONFORME** : liste = attendu = copie (`70cc91c2…`) ; 0 régulier, 0 cassé ; 407 projetés, contenu = HEAD, 0 écart de casse ; clones tiers e1446fa / 2352e88, `origin` = miroirs, 0 modification, `blob:none` |
| contenu des 3887 fichiers contre la copie | 0 écart |
| autres clones | tous sur `master`, propres (seul `family-stm32f7xx` sur `devenv/env-47`) |
| `lepton check`, `lepton generate`, `seed status` | code 0, 0, 0 ; espace de travail **identique** à celui de l'avant (`cmp`) ; 2 clés « projection » F7 (196 et 5 fichiers) |
| `lepton file owner` | `…/hal_driver/Src/stm32f7xx_hal_eth.c` → `tiers@stm32f7xx-hal-driver` ; `…/STM32F7xx/README.md` → `tiers@cmsis-device-f7` ; `…/STM32F7xx/LEPTON-PROVENANCE.md` → `lepton@family-stm32f7xx` |

## 6. Contrôles (PA-82)

### 6.1 Oracle après

`rapports/oracles/env-47-apres/` est produit par les mêmes commandes qu'au §4, avec des
constructions à neuf sur `<ROOTSTOCK>` basculé ; `rejouer-oracle.sh` rend « tout a réussi ». La
comparaison à `env-47-avant` (`env-47-apres/comparaisons/`, journal
`env-47-f7-projection/oracle-apres.out`) donne :

| Preset | Sections/symboles | Empreinte | Fumée | Banc KAL | Écarts expliqués |
| --- | --- | --- | --- | --- | --- |
| host | — | mklepton identiques | — | ctest 7/7 | — |
| qemu-mps2-an386-embos, -embos-soft, -freertos, -freertos-soft | code 0 ×4 | non comparée (constructions non reproductibles, ENV-41 §4.1) | identique | 19, 15, 19, 15 ; mêmes cas, mêmes résultats | aucun |
| qemu-mps2-an500-embos, -freertos | code 0 ×2 | idem | identique | 18, 18 | aucun |
| stm32f746g-disco-embos, -freertos | code 0 ×2 | idem | banc carte §6.2 | banc carte §6.2 | aucun ; 0 `depots/tiers` dans les binaires (`strings`), 11 chemins `…/stm32f7xx/hal_driver` du trunk |
| nucleo-f429zi, nucleo-f439zi, nucleo-wl55jc1, samd21-xplained-pro (embOS, FreeRTOS) | code 0 ×8 | idem | — | — | aucun |

- Listes `ctest -N` : 17/17 identiques.
- Trunk relevé par l'oracle : 3887 chemins, égaux à ceux de l'avant (`c65ee399…`) ; liste
  `chemin -> cible` = `attendu-liens-apres.txt` (`70cc91c2…`) ; 0 anomalie.

### 6.2 Banc STM32F746G-DISCO (PA-11)

Le banc est lancé par `env-47-f7-projection/bancs.sh`, qui appelle `env-45-sonde/banc-sonde.sh`
pour chaque preset. Seule la sonde F746 est branchée, sur le port `/dev/cu.usbmodem1454303`
(relevé par `ioreg`) ; hôte 192.168.2.10 (`en0`). Pour chaque preset, le script :
- reconfigure `<ROOTSTOCK>/build/<preset>` avec `LEPTON_BOARD_SERIAL_PORT`,
  `LEPTON_BOARD_PROBE_SERIAL=0671FF495351885087181231` et `LEPTON_NET_TEST_HOST_IP` ;
- vérifie que `lepton.elf` reste égal à l'oracle après ;
- lance `ctest -L board`.

Journaux : `oracles/env-47-apres/<preset>/carte*.log`, `fumee-carte.log`, `reseau-carte.log`.

| Preset | cfg générée | `lepton.elf` contre l'oracle | Flash | Résultat | Réseau | Référence |
| --- | --- | --- | --- | --- | --- | --- |
| stm32f746g-disco-embos | `adapter serial 0671FF…1231` | 0 écart | `** Verified OK **` | **20/20** (fumée, réseau, flash, T1-T8, T1F-T7F, TICI, TCLK, TSBRK, IRQ, harness_fail) | ping 3/3, `LIST` 13 entrées, `RETR /usr/etc/.boot` 57 octets identique, ECONNRESET=15 | 20/20 d'ENV-31, mêmes valeurs réseau |
| stm32f746g-disco-freertos | idem | 0 écart | `** Verified OK **` | **20/20** | idem | idem |

Fumée : `uname -a` → `lepton-cortexm7-32 4.10.0.2 … cortexM7-stm32f7`. La carte porte l'image
`stm32f746g-disco-freertos` du banc.

### 6.3 Bilan des critères

| Critère | Résultat |
| --- | --- |
| PA-81 et PA-82 tranchés et consignés | PA-81 : oui (§1.8, `DEVENV-STATUS.md`) ; PA-82 : ce rapport |
| Miroirs F7 créés, égaux à l'amont | oui (§2) : `git ls-remote` identiques ; e1446fa et 2352e88 atteignables |
| Binaires identiques (code 0) | oui : host et les 16 presets (§6.1) |
| Liste des chemins identique, aux écarts accordés près | oui, aucun écart : 3887 chemins `c65ee399…`, provenances conservées ; 201 cibles → `depots/tiers/`, 407 projetés en tout |
| Plus aucun fichier de la HAL ni du CMSIS device F7 dans le clone `family-stm32f7xx` | oui : restent les 2 `LEPTON-PROVENANCE.md` (PA-81) |
| Contenu projeté = commits épinglés, octet pour octet | oui : 201/201 = blob du HEAD des clones (e1446fa, 2352e88), et = ancienne copie (`cmp`) |
| Rootstock neuf `essais/env-47-vierge` | mêmes chemins ; contenu identique ; `lepton check` 0 (§5.2) |
| `check`, `generate`, `seed status`, `file owner` sur `<ROOTSTOCK>` | code 0 ; espace de travail identique ; clés F7 reconnues (§5.3) |
| `seed lock`, `--verify` sur une graine de projet | clés F7 figées (`projected_by`), `--verify` 0 (§3) |
| Banc STM32F746G-DISCO 20/20, réseau compris | oui, embOS et FreeRTOS (§6.2) |

Autres contrôles :
- lepton-tools : seule l'aide de `scripts/tiers/verifier-import.sh` change (637e7f6, `bash -n`) ;
  aucun code de lepton modifié, donc `pytest` n'a pas été relancé.
- La graine `original-tree`, le clone noyau, les BSP, le F4 et le WL ne sont pas touchés.

### 6.4 Rootstocks à regreffer en ENV-50
Ils sont tous en version `master` de `family-stm32f7xx`. Après la publication, un `graft-update`
avance la famille et crée les 2 clones tiers F7 depuis les miroirs, ce qui exige scion ≥ 0.6.1.0 :
- Mac : `essais/env-13-vierge`. `essais/env-41-vierge` aussi s'il est gardé ; sa graine d'essai
  pointe vers une copie supprimée, voir §Emplacements.
- VM (scion 0.6.1.0, puis 0.6.2.0 en ENV-50) : `essais/env-28-debian`, `essais/env-43-debian`.
- Les copies d'étape `env-34-copie`, `env-35-copie`, `env-37-copie` et `env-39-copie` sont hors
  des regreffes, comme en ENV-43.

### 6.5 Propositions soumises au PA-82
1. Rapport accepté. Nouvel oracle de référence Mac : `oracles/env-47-apres/`. Ses binaires sont
   identiques à ceux d'`env-46-apres`, mais les cibles de 201 liens changent.
2. Publication (PA-P), dans l'ordre suivant ; les miroirs sont déjà publiés (§2) :
   1. `family-stm32f7xx` : fusion `--no-ff` de `devenv/env-47` dans `master`, push de `master` et
      de la branche ; le clone de `<ROOTSTOCK>` repasse sur `master`, même arbre, trunk inchangé ;
   2. lepton-tools : fusion `--no-ff` de `devenv/env-47` dans `main`, push de `main` et de la
      branche.

   La graine `original-tree` n'est pas touchée : elle déclare la famille en `master`.
3. Essais supprimés : `env-47-copie`, `env-47-projet` (PA-81), `env-47-vierge` et
   `env-47-vierge-graine`, ces deux derniers parce que la graine d'essai pointe vers la copie.
   La graine de publication `env-40-publication`, désormais à 4 miroirs, est gardée pour les
   miroirs WL d'ENV-48.
4. Validation Debian : ENV-50.
