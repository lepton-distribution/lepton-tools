# Étape ENV-37 — Famille STM32WL : audit et provenance du code tiers

## Contexte
Le greffon `family-stm32wlxx` embarque du code tiers ST importé en un seul commit (8ea1490, ENV-6),
sans `LEPTON-PROVENANCE.md`, et jamais comparé à l'amont. La famille compile déjà la HAL ST
(`USE_HAL_DRIVER`, 12 sources de `cubemx_hal_driver/src/`) : elle n'a pas de SPL. Le travail
d'ENV-35 (passage de la SPL à la HAL) n'a donc pas d'équivalent ici. Seul le niveau 1 d'ENV-34
s'applique, et seulement en partie.

Décision du 2026-11-05 : audit et provenance **avant** la conception de la projection scion
(ENV-38), **sans recopie ni renommage**. La projection remplacera les copies ; recopier le WL à la
main serait refait aussitôt. L'audit fournit à ENV-38 son cas le plus exigeant : quatre ensembles
tiers, répertoires renommés, fichiers modifiés par Lepton.

**Rien de compilé ne change.** Archétype : migration iso-fonctionnelle. Oracle : binaires
identiques.

Hors périmètre (décisions du 2026-11-05) : montée de version de la HAL WL ; bascule du WL sur la
projection (révision suivante du plan).

## Prérequis
- ENV-36 terminée.
- Clone `<ROOTSTOCK>/depots/lepton/family-stm32wlxx/master` : `master` dbc58d7, propre.
- Relevé du 2026-11-05, à revérifier au §1. Chemins relatifs à `sys/root/src/` de la famille :

| Ensemble | Emplacement | Contenu relevé | Amont présumé |
| --- | --- | --- | --- |
| HAL | `kernel/dev/arch/cortexm/stm32wlxx/cubemx_hal_driver/{inc,src}` | 157 fichiers : 72 `.c`, 82 `.h`, `README.md`, `LICENSE.txt`, `Release_Notes.html` ; `__STM32WLxx_HAL_VERSION` 1.3.0 | `https://github.com/STMicroelectronics/stm32wlxx-hal-driver.git` ; tags `v1.0.0` à `v1.6.0`, dont `v1.3.0` |
| CMSIS device | `kernel/core/ucore/cmsis/Device/st/stm32wlxx` | 5 fichiers : `stm32wl55xx.h`, `stm32wlxx.h`, `system_stm32wlxx.h`, `system_stm32wlxx.c`, `startup/iar/startup_stm32wl55xx_cm4.s` ; `__STM32WLxx_CMSIS_VERSION` 1.1.1 | `https://github.com/STMicroelectronics/cmsis-device-wl.git` ; tags `v1.0.0` à `v1.4.0`, dont `v1.1.1` |
| Pile radio | `kernel/dev/arch/cortexm/stm32wlxx/radio_subghz_phy` | 24 fichiers ; « SubGHz_Phy 1.3.0 » selon le manifeste | à établir au §1 |
| Utilitaires | `kernel/dev/arch/cortexm/stm32wlxx/Utilities` | 39 fichiers : `conf`, `Fonts`, `lcd`, `lpm`, `misc`, `sequencer`, `timer`, `trace` | à établir au §1 |

- Dépôt `https://github.com/STMicroelectronics/STM32CubeWL.git` : tags `v1.0.0` à `v1.6.0`.
- Trois fichiers portent une marque Lepton (`grep -rli 'lepton\|kernelconf\|phlb'`) :
  `radio_subghz_phy/stm32_radio_core_inc/subghz.h`,
  `radio_subghz_phy/stm32_radio_core_inc/utilities_conf.h`, `Utilities/timer/stm32_timer.h`.
- Manifeste de la famille : 21 `sources` (3 `dev_stm32wlxx`, 5 radio, 1 `Utilities`, 12 HAL),
  9 inclusions publiques ; `stm32wlxx_hal_conf.h` dans `dev_stm32wlxx/`.
- `scripts/tiers/verifier-import.sh` (ENV-34) ; clones amont dans `~/lepton-tools-dev/tiers/`
  (PA-55). Méthode et modèle de provenance : `rapports/env-34-hal-f4.md`,
  `…/stm32f7xx/hal_driver/LEPTON-PROVENANCE.md` de `family-stm32f7xx`.
- Dernier oracle Mac : `rapports/oracles/env-35-apres/`. `<ROOTSTOCK>` : 3978 liens.
- Skills `lepton-rootstock`, `lepton-oracle`, `lepton-cibles`.
- Branches `devenv/env-37` : lepton-tools, `family-stm32wlxx`.

## Tâches

### 1. Audit (lecture seule) → PA-61
- Cloner les dépôts amont dans `~/lepton-tools-dev/tiers/`, hors de `<ROOTSTOCK>`. Résoudre chaque
  tag en commit (`git rev-parse <tag>^{commit}`).
- Relever les sous-modules de STM32CubeWL à la version qui porte la HAL 1.3.0
  (`gh api repos/STMicroelectronics/STM32CubeWL/contents/<chemin>?ref=<tag>`). Établir le couple
  HAL et CMSIS device réellement copié.
- Établir l'amont de `radio_subghz_phy/` et de `Utilities/` : dépôt ST séparé, ou STM32CubeWL seul
  (`Middlewares/Third_Party/SubGHz_Phy`, `Utilities/`). Relever la révision. La décision du
  2026-11-04 exclut STM32Cube entier comme source : si aucun dépôt séparé n'existe, le consigner
  comme question du PA-61, sans trancher.
- Comparer chaque ensemble à sa révision par `verifier-import.sh`. Le script suppose des chemins
  identiques à l'amont. Pour les répertoires renommés (`inc`, `src`), comparer une copie de
  travail remise à la casse amont dans `~/lepton-tools-dev/essais/env-37-compare/`, sans toucher
  au clone. Toute évolution du script est une proposition au PA-61.
- Classer chaque fichier : `OK`, `CR`, `DIFF`, `TROP`, `MANQUE`. Pour chaque `DIFF`, produire le
  `diff` contre l'amont et le qualifier : modification Lepton, autre version, fin de ligne.
- Chercher les modifications Lepton au-delà des trois fichiers relevés.
- Relever ce qui est réellement compilé et inclus : `compile_commands.json` et `gcc -H` des
  presets `nucleo-wl55jc1-embos` et `nucleo-wl55jc1-freertos`.
- Relever les références à ces répertoires hors de la famille : BSP `nucleo-wl55jc1`, clone
  noyau, lepton-tools (`schemas/exemples/greffon-famille-stm32wlxx.json`, skills, documents).
- Relever la licence de chaque ensemble et les fins de ligne (0 CRLF relevé le 2026-11-05).
- Relever si le volume du Mac distingue la casse (`diskutil info /`). Le noter dans le rapport :
  la VM Debian la distingue.
- Rapport `rapports/env-37-wl-provenance.md` ; listes dans `rapports/env-37-wl-provenance/`.
- **PA-61** : l'utilisateur valide :
  - La révision amont retenue pour chaque ensemble, si la copie ne correspond exactement à aucun
    tag : <À CONFIRMER au PA-61>.
  - Sort des fichiers modifiés par Lepton : <À CONFIRMER au PA-61>.
    - Option 1 : laissés en place, décrits un par un dans la provenance (écart à la règle D1a
      consigné).
    - Option 2 : déplacement hors des répertoires tiers, renvoyé à une étape ultérieure.
  - Sort des fichiers `TROP`, dont le démarrage IAR : <À CONFIRMER au PA-61 : laissés et listés,
    ou supprimés s'ils ne sont ni compilés ni inclus>.
  - Forme de la provenance : un `LEPTON-PROVENANCE.md` par ensemble, sur le modèle du F7 et du
    F4 : <À CONFIRMER au PA-61>.
  - Texte `description` du manifeste, si l'audit contredit « STM32CubeWL V1.3.0 » ou
    « SubGHz_Phy 1.3.0 » : <À CONFIRMER au PA-61>.
  - Source de la pile radio et des utilitaires si STM32CubeWL est leur seul amont :
    <À CONFIRMER au PA-61>.
- Aucune modification avant la réponse.

### 2. Oracle avant
Skill `lepton-oracle` : host et les 16 presets → `rapports/oracles/env-37-avant/`, listes
`ctest -N` comprises. Doit être conforme à `rapports/oracles/env-35-apres/`.

### 3. Provenance (clone de la famille, `devenv/env-37`)
- Un commit par ensemble : `LEPTON-PROVENANCE.md` avec dépôt, commit, tag, version de
  STM32CubeWL, licence, règle D1a, et la liste des écarts constatés (fichiers modifiés, hors
  amont, manquants).
- Suppressions accordées au PA-61 : commits mécaniques séparés.
- Texte du manifeste, si accordé : commit séparé ; `sources` et `compilation` inchangés.
- Aucun fichier tiers n'est déplacé, renommé ni recopié.
- Regreffe : `scion graft --scion lepton@family-stm32wlxx`, d'abord sur une copie d'essai
  (`cp -RP`), puis sur `<ROOTSTOCK>`.

### 4. Contrôles → PA-62
- Oracle après : `comparer-oracle.py` code 0 sur host et les 16 presets ; listes `ctest -N`
  identiques ; fumée et banc KAL QEMU identiques.
- Liens de `<ROOTSTOCK>` : seuls ajouts, les `LEPTON-PROVENANCE.md` ; seuls retraits, ceux du
  PA-61. Nombre de liens consigné.
- `lepton check` code 0 ; aucun lien cassé, aucun fichier régulier.
- Rapport, section « Cas d'épreuve pour ENV-38 » : pour chaque ensemble, le dépôt, la révision,
  la correspondance chemin amont → chemin dans la famille, et les exceptions (fichiers modifiés,
  hors amont, renommés). Cette section est l'entrée d'ENV-38.
- **PA-62** : rapport ; push et fusions des branches `devenv/env-37` (PA-P). Validation Debian :
  ENV-43.

## Critères de validation
- [ ] PA-61 et PA-62 tranchés et consignés.
- [ ] Binaires identiques sur host et les 16 presets (code 0).
- [ ] Chaque fichier des quatre ensembles est classé dans le rapport ; chaque `DIFF` est qualifié.
- [ ] Chaque ensemble tiers de la famille a sa provenance, ou la raison de son absence est
      consignée au PA-61.
- [ ] Le rapport contient la section « Cas d'épreuve pour ENV-38 ».

## Pièges connus
- `git ls-remote --tags` rend l'objet tag pour un tag annoté : le commit est sur la ligne
  `<tag>^{}`. Ne citer que des commits résolus.
- Un `diff` propre sur le Mac ne prouve rien sur la casse des noms si le volume ne la distingue
  pas : comparer les listes de noms, pas seulement les contenus.
- Ne pas copier depuis STM32CubeWL sans décision : la source de chaque ensemble se tranche au
  PA-61.
- Ne rien changer aux chemins d'inclusion ni à `sources` du manifeste : c'est la HAL compilée.
- `sed -i` est interdit sur le trunk. Les liens apparaissent après `scion graft` ; un fichier créé
  directement dans le trunk est refusé par le hook.
- `git status --ignored` liste un `.DS_Store` par répertoire visité par le Finder : les ignorer
  dans les contrôles.
- Empreintes et console de fumée varient d'une construction à l'autre (date, jeton UART) :
  comparer hors de ces éléments (`rapports/env-34-hal-f4.md` §5.1, E-1, E-2).

## À la fin de l'étape
`DEVENV-STATUS.md` :
- statut et branches ;
- décisions PA-61 et PA-62 ;
- §Emplacements : clones amont ajoutés à `~/lepton-tools-dev/tiers/` ;
- §Versions : révisions HAL, CMSIS device, pile radio et utilitaires du WL ;
- journal.

Passation `handoff/env-37.md`.
