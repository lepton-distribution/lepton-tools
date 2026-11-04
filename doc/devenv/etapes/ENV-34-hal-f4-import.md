# Étape ENV-34 — HAL et CMSIS device STM32F4 importés par la méthode du F7

## Contexte
Le greffon `family-stm32f4xx` embarque sous `kernel/dev/arch/cortexm/stm32f4xx/cubemx_hal_driver/`
une HAL ST V1.7.1 (avril 2017) et des en-têtes CMSIS device V2.6.1 (février 2017), sans
provenance. Ces versions sont antérieures aux premiers tags des dépôts ST (`v1.7.6`, `v2.6.3`).
Cette copie n'est pas compilée : la famille utilise la SPL (`driverlib/`, `USE_STDPERIPH_DRIVER`).

Le F7 suit une autre méthode (migration étape 6, extraction ENV-19, `rapports/env-19-extraction.md`
§3) : copie non modifiée de dépôts ST à des commits taggés, ceux de la dernière version de
STM32CubeF7, avec `LEPTON-PROVENANCE.md`, `LICENSE.md` et `README.md` à côté (règle D1a, code tiers
non modifié).

Cette étape applique cette méthode au F4. Elle constitue le niveau 1 de la décision du 2026-11-04 ;
le niveau 2 (passage de la SPL à la HAL) fait l'objet d'ENV-35. **Rien de compilé ne change.**
Archétype : migration iso-fonctionnelle de code tiers non compilé. Oracle : binaires identiques.

## Prérequis
- ENV-33 terminée.
- Clones de `<ROOTSTOCK>` :
  - `depots/lepton/family-stm32f4xx/master` (famille) ;
  - `depots/lepton/original/master` (noyau, `cmsis-5/CMSIS/Core/Include`).
- Références relevées le 2026-11-04, à revérifier par `git ls-remote` au §1 :

| Élément | Dépôt | Révision | Référence du couple |
| --- | --- | --- | --- |
| HAL | `https://github.com/STMicroelectronics/stm32f4xx-hal-driver.git` | `b6f0ed3829f3829eb358a2e7417d80bba1a42db7` = tag `v1.8.5` | sous-module de STM32CubeF4 `v1.28.3` |
| CMSIS device | `https://github.com/STMicroelectronics/cmsis_device_f4.git` | `3c77349ce04c8af401454cc51f85ea9a50e34fc1` (`v2.6.11-1`, sans tag) | sous-module de STM32CubeF4 `v1.28.3` |
| CMSIS Core | `https://github.com/ARM-software/CMSIS_5.git` | tag `5.9.0`, `CMSIS/Core/Include/core_cm4.h` V5.1.2 | les 7 fichiers actuels de `cmsis-5/CMSIS/Core/Include` sont identiques à `5.9.0` aux fins de ligne près (CRLF dans Lepton) |

- Skills `lepton-rootstock`, `lepton-oracle`, `lepton-cibles`.
- Branches `devenv/env-34` : lepton-tools, `family-stm32f4xx`, clone noyau.

## Tâches

### 1. Audit (lecture seule) → PA-55
- Clones de travail des trois dépôts amont, hors de `<ROOTSTOCK>` : <À CONFIRMER au PA-55 :
  emplacement, par exemple `~/lepton-tools-dev/tiers/`>. Relever les têtes par `git ls-remote` et
  vérifier les sous-modules de STM32CubeF4 `v1.28.3` (`git ls-tree v1.28.3 Drivers/…`).
- Contenu actuel de `cubemx_hal_driver/` : nombre de fichiers par répertoire. Lister les fichiers
  absents du dépôt HAL : 6 relevés le 2026-11-04 (`inc/stm32f4xx.h`, `inc/stm32f407xx.h`,
  `inc/stm32f429xx.h`, `inc/stm32f469xx.h`, `inc/system_stm32f4xx.h`,
  `inc/Legacy/stm32f4xx_hal_conf.h`).
- Toutes les références à `cubemx_hal_driver` et à `stm32f4xx_hal.h`, dans la famille, les BSP
  `nucleo-f429zi` et `nucleo-f439zi`, le clone noyau (code hors plan compris), `lepton-tools`
  (skills, documents vivants) et le manifeste de la famille (`description`). Huit fichiers non
  compilés de la famille incluent `stm32f4xx_hal.h` : `dev_stm32f4xx/dev_stm32f4xx_{cpu_x,
  cubemx_eth,dac_x,flash,i2c_x,sdio,sdio-1.16}.c` et `flash_if.h`.
- Fins de ligne : amont (LF), copie F7 (`hal_driver/`), `cmsis-5/CMSIS/Core/Include` (CRLF).
- Rapport `rapports/env-34-hal-f4.md`.
- **PA-55** : l'utilisateur valide :
  - Destination de la HAL : <À CONFIRMER au PA-55>.
    - Option 1 : `stm32f4xx/hal_driver/{Inc,Src}`, convention F7 (casse de l'amont).
    - Option 2 : `cubemx_hal_driver/{inc,src}` conservé.
  - Contenu repris de la HAL : `Inc/`, `Src/` complets (`Legacy/` et modèles `*_template.*`
    compris), `LICENSE.md`, `README.md` ; notes de version non reprises (précédent F7).
  - Sous-ensemble CMSIS device, sous `kernel/core/ucore/cmsis-5/Device/ST/STM32F4xx/Include` de
    la famille : `stm32f4xx.h`, `system_stm32f4xx.h`, `stm32f429xx.h`, `stm32f439xx.h`, plus
    `LICENSE.md` et `README.md` à `STM32F4xx/` ; modèles `Source/Templates` non repris.
  - `core_cm4.h` dans le noyau : version `5.9.0`, fins de ligne de l'amont ou alignées sur les
    7 fichiers voisins (CRLF) <À CONFIRMER au PA-55> ; ajout d'un `LEPTON-PROVENANCE.md` pour
    `cmsis-5/CMSIS/Core/` <À CONFIRMER au PA-55>.
  - Sort des 6 fichiers hors amont : supprimés avec la copie (proposition : ils ne sont pas
    compilés, et le CMSIS device à jour les remplace).
  - Proposition hors source : script `scripts/tiers/verifier-import.sh` (voir §3).
  - Proposition hors source : compilation à blanc de la HAL importée (voir §4).
- Aucune modification avant la réponse.

### 2. Oracle avant
Skill `lepton-oracle` : host et les 16 presets → `rapports/oracles/env-34-avant/`, listes
`ctest -N` comprises. Doit être conforme à `rapports/oracles/env-32-apres/` (dernier oracle Mac).

### 3. Import
Chaque point fait l'objet d'un commit distinct, mécanique, dans le clone du greffon :
1. `git rm -r` de `cubemx_hal_driver/` (famille).
2. HAL : copie depuis `git archive <révision>` du clone amont, pas depuis un arbre de travail.
3. CMSIS device : sous-ensemble du PA-55, même procédure.
4. `LEPTON-PROVENANCE.md` dans chaque répertoire importé, sur le modèle du F7 : dépôt, commit,
   tag, version STM32CubeF4, licence, règle D1a, consigne pour ajouter une autre puce depuis le
   même commit.
5. Description du manifeste de la famille (texte seul ; `sources` et `compilation` inchangés).
6. Noyau : `core_cm4.h`, et la provenance si le PA-55 l'accorde.

Si le PA-55 l'accorde, `scripts/tiers/verifier-import.sh <clone> <révision> <répertoire>
[<liste>]` compare chaque fichier importé à `git show <révision>:<chemin>` (SHA-256) et liste les
fichiers manquants et en trop. Il sert à la famille F4, à la vérification rétroactive du F7 et au
futur lot de projection scion.

Regreffe : `scion graft --scion lepton@family-stm32f4xx`, puis la même commande pour le noyau ;
d'abord sur une copie d'essai (`cp -RP`), puis sur `<ROOTSTOCK>`.

### 4. Contrôles → PA-56
- Oracle après : `comparer-oracle.py` code 0 sur host et les 16 presets ; listes `ctest -N`
  identiques ; fumée et banc KAL QEMU identiques.
- `verifier-import.sh` : 0 écart pour la HAL et le CMSIS device, plus le F7 en lecture seule. Un
  écart sur le F7 n'est pas corrigé ici : il est consigné.
- Si le PA-55 l'accorde, compilation à blanc hors du trunk et hors des presets :
  - chaque `Src/*.c` de la HAL, sauf les modèles et `Legacy/` ;
  - avec `-DSTM32F429xx -DUSE_HAL_DRIVER`, puis `-DSTM32F439xx` ;
  - avec un `stm32f4xx_hal_conf.h` tiré du modèle, placé dans le répertoire de construction ;
  - avec les inclusions `hal_driver/Inc`, `cmsis-5/Device/ST/STM32F4xx/Include` et
    `cmsis-5/CMSIS/Core/Include`.
  Résultat attendu : 0 erreur. C'est la preuve que l'ensemble importé est complet pour ENV-35.
- `lepton check` code 0 ; aucun lien cassé ni fichier régulier dans le trunk ; plus aucun lien
  sous `cubemx_hal_driver/` (option 1 du PA-55).
- **PA-56** : rapport ; push et fusions des branches `devenv/env-34` (PA-P). Validation Debian :
  ENV-36.

## Critères de validation
- [ ] PA-55 et PA-56 tranchés et consignés.
- [ ] Binaires identiques sur host et les 16 presets (code 0).
- [ ] HAL et CMSIS device identiques octet pour octet à leurs révisions amont, provenance à côté.
- [ ] Aucune copie de HAL F4 sans provenance dans l'arbre.

## Pièges connus
- `3c77349` n'a pas de tag : la provenance cite le commit et sa description (`v2.6.11-1`), comme
  le F7 cite ses commits.
- Ne pas copier depuis STM32CubeF4 : seuls les deux sous-modules sont repris, à leurs commits.
- Les dépôts amont n'ont pas de `.gitattributes` (relevé du 2026-11-04). Comparer quand même la
  liste issue de `git archive` à `git ls-tree -r <révision>`.
- `sed -i` est interdit sur le trunk. Les liens apparaissent après `scion graft` ; un fichier créé
  directement dans le trunk est refusé par le hook.
- Ne rien changer à `driverlib/` (dont `driverlib/stm32f4xx.h` V1.0.2 et `stm32f429xx.h` V2.3.0),
  ni à `kernel/core/ucore/cmsis/Device/st/stm32f4xx/` : c'est la SPL compilée.
- Les fichiers ignorés par git ne sont pas greffés (E1). La famille n'a pas de `.gitignore`,
  mais `core.excludesFile` (`~/.gitignore_global`) s'applique aussi. Contrôle :
  `git -C <clone famille> status --ignored` doit être vide sous les répertoires importés.

## À la fin de l'étape
`DEVENV-STATUS.md` :
- statut et branches ;
- décisions PA-55 et PA-56 ;
- §Emplacements : clones amont ;
- §Versions : révisions HAL, CMSIS device, CMSIS Core ;
- journal.

Passation `handoff/env-34.md`.
