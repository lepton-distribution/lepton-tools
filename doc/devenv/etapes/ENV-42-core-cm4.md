# Étape ENV-42 — `core_cm4.h` : un seul CMSIS-Core pour les Cortex-M4

## Contexte
L'arbre contient deux `core_cm4.h` (clone noyau, sous `sys/root/src/kernel/core/ucore/`) :
- `cmsis/CMSIS/Include/core_cm4.h`, CMSIS-Core V3.30 ;
- `cmsis-5/CMSIS/Core/Include/core_cm4.h`, CMSIS_5 `5.9.0` (V5.1.2), importé en ENV-34.

`cmake/isa/armv7m.cmake:18` ajoute `cmsis/CMSIS/Include` pour tous les presets armv7m, en position
2 des `-I`. `cmake/cpu/cortex-m7.cmake:35` ajoute `cmsis-5/CMSIS/Core/Include` pour le M7 seul. Les
inclusions des familles viennent après (`cmake/lepton_greffons.cmake`). Conséquence : le
`core_cm4.h` 5.9.0 n'est vu par aucun preset ; F4, WL55 et an386 compilent avec V3.30.

Le PA-57 (ENV-35) a conservé V3.30 pour ne pas toucher le noyau. La compilation à blanc de la HAL
F4 échoue dans cet ordre sur un seul fichier, `stm32f4xx_ll_usb.c` (`__UNALIGNED_UINT32_READ`,
`__UNALIGNED_UINT32_WRITE`), que nul preset ne compile.

Cette étape tranche le sort des deux fichiers. Elle est indépendante de la projection scion
(ENV-37 à ENV-41). Archétype : migration à écart borné : les binaires de plusieurs presets peuvent
changer, sous un critère fixé avant toute modification.

Rattaché à cette étape (décision du 2026-11-05) : le contrôle de la vue des périphériques de la
NUCLEO-F429ZI sous VSCodium, non fait en ENV-35 (PA-58).

## Prérequis
- ENV-36 terminée ; ENV-41 conseillée avant (une variable à la fois).
- Clone noyau `<ROOTSTOCK>/depots/lepton/original/master` : `master` 2893297.
- Presets `cortex-m4f` (champ `coeur` des BSP) : `nucleo-f429zi-{embos,freertos}`,
  `nucleo-f439zi-{embos,freertos}`, `nucleo-wl55jc1-{embos,freertos}`,
  `qemu-mps2-an386-{embos,embos-soft,freertos,freertos-soft}`.
- Constats de référence : `rapports/env-34-hal-f4.md` §1.5 et §5.3, `rapports/env-35-hal-f4.md`
  §1.6 ; provenance `cmsis-5/CMSIS/Core/LEPTON-PROVENANCE.md` du noyau.
- Dernier oracle Mac de référence (celui d'ENV-41 si elle est faite, sinon `env-35-apres`).
- Cartes : NUCLEO-F429ZI ; deux NUCLEO-WL55JC1 pour `board.radio` (ENV-32). Écriture flash
  soumise au PA-11, à redemander.
- Scripts : `scripts/tiers/compiler-hal-f4-a-blanc.sh` ; banc carte
  `rapports/env-35-hal-f4/banc-carte.sh`.
- Skills `lepton-rootstock`, `lepton-oracle`, `lepton-cibles`.
- Branches `devenv/env-42` : lepton-tools, clone noyau.

## Tâches

### 1. Audit (lecture seule) → PA-71
- Pour chaque preset armv7m : en-têtes CMSIS-Core réellement retenus (`gcc -H -fsyntax-only` sur
  une unité du noyau, une de la famille, une du micro-noyau), et position des `-I`
  (`compile_commands.json`).
- `cmsis/CMSIS/Include` contient aussi `core_cm3.h`, `core_cmFunc.h`, `core_cmInstr.h`,
  `core_cm4_simd.h`, `arm_math.h` et d'autres : relever lesquels sont inclus, par quels presets,
  M7 compris (ce répertoire précède `cmsis-5` dans leur ordre).
- Différences entre V3.30 et 5.9.0 qui touchent le code compilé : macros d'accès, fonctions
  `NVIC_*` et `SCB`, abstraction du compilateur (`cmsis_gcc.h`), FPU.
- Ports embOS et FreeRTOS : ce qu'ils incluent de CMSIS.
- Code non configuré par les presets qui dépend de V3.30 : le relever, ne pas le traiter (hors
  plan).
- Essai de chaque option sur une copie d'essai (`cp -RP`), construction des presets armv7m et
  `comparer-oracle.py` : écarts par preset. Compilation à blanc de la HAL F4 dans chaque cas.
- Rapport `rapports/env-42-core-cm4.md`, §1.
- **PA-71** : l'utilisateur tranche :
  - L'option : <À CONFIRMER au PA-71>.
    - Option 1 : CMSIS_5 `5.9.0` pour tous les presets `cortex-m4f` (inclusion ajoutée devant
      V3.30 par le CMake du cœur) ; binaires F4, WL55 et an386 susceptibles de changer.
    - Option 2 : V3.30 conservé ; `core_cm4.h` 5.9.0 retiré du noyau et provenance corrigée.
    - Option 3 : statu quo, les deux fichiers restent, la raison est écrite dans la provenance.
    - Une condition propre à une famille dans le CMake commun a été relevée en ENV-35 comme
      contraire à BLD-6 : ne la proposer que si l'audit ne laisse rien d'autre.
  - Si l'option 1 : sort de `cmsis/CMSIS/Include` V3.30 : <À CONFIRMER au PA-71>.
  - Critère d'écart admis par preset : <À CONFIRMER au PA-71>. Précédents : PA-49 (FreeRTOS),
    PA-57 (occupation : `.text` ≤ +10 %, SRAM et CCM ≤ +5 %).
  - Cartes disponibles et écriture flash (PA-11) : <À CONFIRMER au PA-71>.
- Aucune modification avant la réponse.

### 2. Oracle avant et banc de référence
- Skill `lepton-oracle` : host et les 16 presets → `rapports/oracles/env-42-avant/`.
- Si le PA-71 retient une option qui change des binaires : banc de référence sur les cartes
  accordées, avant modification (F429 : fumée, banc KAL, réseau ; WL55 : fumée, banc KAL,
  `board.radio`).

### 3. Modification (clone noyau, `devenv/env-42`)
- Selon le PA-71 : CMake du cœur ou retrait du fichier, puis provenance. Commits séparés.
- Regreffe du noyau (skill `lepton-rootstock`) sur la copie d'essai, puis sur `<ROOTSTOCK>`.

### 4. Contrôles → PA-72
- Oracle après, host et les 16 presets :
  - presets hors du périmètre de l'option : code 0 ;
  - presets concernés : écarts expliqués et dans le critère du PA-71.
- QEMU an386 : fumée et banc KAL identiques. `ctest -N` identiques partout.
- Compilation à blanc de la HAL F4 : résultat consigné pour l'ordre retenu (0 échec attendu avec
  l'option 1).
- Cartes accordées : mêmes résultats qu'au banc de référence du §2.
- Vue des périphériques : session de débogage `nucleo-f429zi-embos` sous VSCodium, panneau
  XPERIPHERALS ; l'utilisateur lit un registre (par exemple un `GPIOx` et `RCC`) et confirme à
  l'écran. Résultat consigné. Référence : `rapports/env-26-dbg4.md` (registres lisibles le
  2026-11-02, SVD inchangé depuis).
- `lepton check` code 0 ; aucun lien cassé, aucun fichier régulier.
- **PA-72** : rapport ; nouvel oracle de référence si des binaires ont changé ; fusions et push des
  branches `devenv/env-42` (PA-P). Validation Debian : ENV-43.

## Critères de validation
- [ ] PA-71 et PA-72 tranchés et consignés.
- [ ] Un preset `cortex-m4f` ne voit plus qu'un `core_cm4.h` possible, ou la raison du statu quo
      est écrite dans la provenance (option 3).
- [ ] Presets hors périmètre : binaires identiques (code 0).
- [ ] Presets concernés : écarts dans le critère du PA-71 ; cartes accordées conformes au banc de
      référence.
- [ ] Vue des périphériques F429 : résultat consigné.

## Pièges connus
- `cmake/isa/armv7m.cmake` vaut pour le M3, le M4 et le M7 : une modification à ce niveau touche
  aussi les 4 presets M7 (`qemu-mps2-an500-*`, `stm32f746g-disco-*`). Préférer le niveau du cœur si l'option 1 est retenue.
- Les 7 autres en-têtes de `cmsis-5/CMSIS/Core/Include` viennent du paquet embOS et sont en CRLF ;
  `core_cm4.h` est en LF (PA-55). Ne pas normaliser.
- `banc-carte.sh` appelle `caffeinate` (macOS seulement).
- VMware Fusion actif peut garder la sonde de la carte : vérifier qu'elle est rattachée au Mac
  avant tout banc.
- L'hôte du test réseau est l'adresse d'`en0` (192.168.2.10 le 2026-11-05), pas 192.168.2.20, qui
  figure dans le `.init` de la carte.
- `.noinit` peut passer de 0 à 4 par bourrage d'alignement : comparer `.bss + .noinit` (PA-60).
- Empreintes et console de fumée varient d'une construction à l'autre : comparer hors de ces
  éléments.
- La NUCLEO-F429ZI porte l'image `nucleo-f439zi-embos` construite sur la VM (ENV-36) : reflasher
  avant le banc de référence.

## À la fin de l'étape
`DEVENV-STATUS.md` :
- statut et branches ;
- décisions PA-71 et PA-72 ;
- §Emplacements et §Versions : ligne CMSIS-Core mise à jour ;
- oracle de référence ;
- journal.

Passation `handoff/env-42.md`.
