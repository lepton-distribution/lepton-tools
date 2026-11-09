# ENV-44 — Résidus d'ENV-37 à ENV-43

Session du 2026-11-09. Branche lepton-tools `devenv/env-44` (depuis `main` 7140e9c). Les fichiers
d'appui sont dans `rapports/env-44-residus/`.

## 0. État de départ
L'état est conforme à `handoff/env-44.md` :

- Dépôts :
  - lepton-tools `main` 7140e9c, égal à `origin/main` ;
  - clone noyau `master` 763dda2 ;
  - BSP an386 5819047 ;
  - F4 7afd7f1, F7 d2d9aa9, WL 2340b25 ;
  - graine 15740f9 ;
  - seed.scions f29fa35 (tag 0.6.1.0) ;
  - clones tiers b6f0ed3 et 3c77349.

  Tous sont propres et égaux à leur amont.
- Trunk : 3982 liens, 0 lien cassé. Il contient 6 fichiers réguliers, tous tolérés (5 `.DS_Store`
  et `.scion.grafted.list`).
- Outils : scion 0.6.1.0, lepton 0.1.0.
- Carte : la NUCLEO-F429ZI est rattachée au Mac (ST-LINK 0672FF…3842). Les WL55 ne sont pas visibles.

## 1. Audit (lecture seule) → PA-75

### 1.1 D1 — `seed replace` / `seed remove` d'un greffon porteur de projections
- **Refus de lepton.**
  - `seed replace` et `seed remove` sont refusés sur la graine de référence
    (`lepton/seed.py:565`, `refuse_reference`).
  - `seed remove` refuse aussi de retirer la famille du BSP de la graine (`lepton/seed.py:658`).
- **Chemin de `seed replace`.** La commande appelle `graft-remove <clé>`, avec `--purge` si
  l'origine est distante, puis `_attach` : `seed-scion-*`, `seed-clone`, `graft`. Elle n'appelle
  jamais `graft-update`.
- **Ce que la spécification prévoit.** P-P6 : `graft-remove <porteur>` retire aussi du trunk les
  clés projetées qu'il porte. La spécification ne dit pas comment elles reviennent au `graft`
  suivant : c'est ce que l'essai doit montrer.
- **Rootstocks d'essai.** Deux copies `rsync -a`, sans `build/` (forme d'ENV-41 §3.3). Aucun essai
  dans `<ROOTSTOCK>` ni dans les rootstocks copiés.
  - **A, `seed replace`** : copie de `essais/env-11/f429zi`. C'est une graine de projet `env11f4`.
    La famille F4 y est porteuse (2 clés « projection », 200 + 6 fichiers), et le rootstock a été
    regreffé en ENV-43. Commande : `lepton seed replace stm32f4xx <URL de la famille>@master`,
    même version, origine changée vers un clone local `file://` de la copie.
    - Attendu au retrait : les 2 clés projetées et leurs 206 liens disparaissent.
    - Attendu au retour : les mêmes clés et des liens `chemin -> cible` identiques à l'état avant,
      hors la racine du clone de la famille.
    - Clés : `seed status` les montre.
  - **B, `seed remove`** : copie de `essais/env-11/qemu`. C'est une graine de projet `env11`, de BSP
    an386, sans F4. Commandes : `lepton seed add stm32f4xx --type famille <URL>`, puis
    `lepton seed remove stm32f4xx`.
    - Attendu après l'ajout : la famille et ses 2 clés projetées sont greffées. À vérifier :
      `graft --scion <clé>` greffe-t-il les clés projetées ?
    - Attendu après le retrait : P-P6, clés et liens retirés, clones tiers conservés.
- **Accords nécessaires.** Aucun `graft-update` ni `seed-update`. Les clones tiers de B se font
  depuis les miroirs publics (réseau).

### 1.2 D2 — Table clone tiers → trunk de l'extension 0.5.2
- **DWARF** (`env-44-residus/d2-dwarf.txt`). Aucun `depots/tiers` dans les 16 `lepton.elf` de
  `<ROOTSTOCK>/build/*`. Les 9 sources HAL F4 compilées (4 presets F4) y figurent par leur chemin du
  trunk.
- **Constat qui change la conclusion prévue.** gdb résout les liens. `arm-none-eabi-gdb` 17.2 a été
  lancé sans carte sur `nucleo-f429zi-embos/lepton.elf`, avec `list HAL_GPIO_Init` :
  - `info source` donne « Located in `<ROOTSTOCK>/depots/tiers/stm32f4xx-hal-driver/v1.8.5/Src/stm32f4xx_hal_gpio.c` » ;
  - `-file-list-exec-source-file` donne `fullname` = ce même chemin.

  C'est le mécanisme décrit en tête de `extension/src/srcmap.ts` (« gdb rend le chemin résolu »).
  La table est donc sollicitée à chaque arrêt dans la HAL F4. La proposition « clore sans objet »
  de la passation de préparation ne tient pas.
- **Table.** `lepton seed status --json` du trunk donne la clé `tiers@stm32f4xx-hal-driver`, de
  racine `…/depots/tiers/stm32f4xx-hal-driver/v1.8.5` et de 200 entrées.
  `Src/stm32f4xx_hal_gpio.c` y correspond à
  `sys/root/src/kernel/dev/arch/cortexm/stm32f4xx/hal_driver/Src/stm32f4xx_hal_gpio.c`. `toTrunk`
  ramènerait donc le `fullname` de gdb au lien du trunk.
- **Essai proposé.**
  1. Contrôle scripté, sans carte : pour chacune des 9 sources HAL compilées, `fullname` de gdb →
     table de `seed status` → lien du trunk existant.
  2. Essai réel sous VSCodium, mené par l'utilisateur :
     - flasher `nucleo-f429zi-embos` (PA-11) ;
     - poser un point d'arrêt sur `HAL_GPIO_Init` ;
     - constater que l'onglet ouvert est le chemin du trunk, pas `depots/tiers/` ;
     - essayer aussi le pas à pas dans la HAL.

### 1.3 D3 — Hook `proteger-trunk.py`
- **Règle actuelle.** Deux expressions sur le texte entier de la commande :
  - `ECRITURE_SHELL` : un verbe d'écriture, puis `[^;&|]*`, puis `trunk/` ou `depots/tiers/` ;
  - `REDIRECTION` : `>` ou `>>` suivi d'un chemin protégé.
- **Essai sur 42 cas** (`env-44-residus/essai_hook.py`, `hook-avant.txt`) : 14 écarts.
- **3 faux positifs** (lecture refusée) :
  - le saut de ligne n'est pas un séparateur : `mkdir /tmp/x` puis, à la ligne suivante, un `diff`
    sur `depots/tiers/`. C'est le refus d'ENV-41 et d'ENV-43 ;
  - un chemin protégé en *source* de `cp` ;
  - un verbe d'écriture cité en argument (`grep -rn mkdir <trunk>/…`).
- **11 écritures non vues** :
  - `cd <trunk> && touch a` et `cd <trunk> && echo x > a` ;
  - `cp /tmp/a <trunk>`, sans barre finale ;
  - `find <trunk> -delete` et `find … -exec rm` ;
  - `… | xargs rm` ;
  - `bash -c 'rm <trunk>/a'` ;
  - `rsync … <trunk>/` ;
  - `patch -d <trunk>` ;
  - `dd of=<trunk>/a` ;
  - `git -C <clone tiers> checkout`.
- **Correction proposée** : une analyse par commande simple, au lieu de l'expression sur le texte
  entier.
  1. Découpage par `shlex`, sur `;`, `&&`, `||`, `|`, `&` et le saut de ligne. `cd` est suivi
     d'une commande à l'autre.
  2. Préfixes sautés : affectations `X=…`, `sudo`, `env`, `command`, `nice`, `time`, `nohup`,
     `exec`.
  3. Analyse récursive de `bash|sh|zsh -c <texte>`, de `find … -exec/-execdir … ;` et de `xargs <verbe>`.
  4. Écriture visée selon le verbe :
     - tous les arguments : `rm`, `rmdir`, `touch`, `mkdir`, `truncate`, `chmod`, `chown`,
       `unlink`, `tee`, `sed -i`/`--in-place`, `perl -i`, `patch` (et son `-d`) ;
     - destination (dernier argument ou `-t`) : `cp`, `ln`, `install`, `rsync`, `scp` ;
     - sources et destination : `mv` ;
     - `dd` : `of=` ;
     - `find` : ses chemins de départ, avec `-delete` ;
     - `git -C <protégé>` : toute sous-commande hors d'une liste de lecture (`status`, `log`,
       `show`, `diff`, `ls-files`, `rev-parse`, `describe`, `cat-file`, `ls-tree`, `grep`,
       `blame`, `branch --show-current`).
  5. Redirections `>`, `>>`, `&>`, `>|` vers un chemin protégé (hors `>&N`).
  6. Un chemin est protégé si `zone_protegee` (signature du rootstock, cwd suivi) le dit, ou si son
     texte contient `trunk` ou `depots/tiers` en composant de chemin (avec ou sans barre finale).
     Le second critère garde le comportement actuel pour les variables (`$ROOT/trunk/a`).
  7. Repli, sans affaiblissement :
     - verbe inconnu : l'ancienne règle s'applique à *cette* commande simple ;
     - texte que `shlex` ne découpe pas (guillemet ouvert, heredoc) : l'ancienne règle s'applique
       au texte entier.
  8. Limite inchangée, à documenter : le contenu d'un script exécuté (`bash f.sh`,
     `python3 -c …`) n'est pas lu.
- **Tests.**
  - Emplacement proposé : `tests/test_proteger_trunk.py`, dans le `pytest` de lepton-tools (même
    venv, lancé avec les 243 tests). Rootstock factice (`.scion.rootstock.signature`) dans
    `tmp_path`. Il reprend les 42 cas, dans les deux sens, en chemin absolu et relatif, vers
    `trunk/` et `depots/tiers/`.
  - Ligne « hook » d'ORCHESTRATION §5bis : ajouter `depots/tiers/`.

### 1.4 D5 — En-tête de périphérique `ARMCM4` du BSP an386
- **Inclusion.** Une seule : `qemu_mps2_machine.h:10` (greffon `bsp-qemu-mps2-an386`) inclut
  `kernel/core/ucore/cmsis/Device/ARM/ARMCM4/Include/ARMCM4.h`, V1.05 du 26 juillet 2011
  (CMSIS 2.10). Son `system_ARMCM4.h` est en V1.05.
- **Précédent.** L'an500 inclut déjà `cmsis-5/Device/ARM/ARMCM7/Include/ARMCM7_DP.h`.
- **Comparaison** (macros et symboles) :

| | V1.05 `ARMCM4.h` | CMSIS 5 `ARMCM4.h` | CMSIS 5 `ARMCM4_FP.h` |
| --- | --- | --- | --- |
| `__FPU_PRESENT` | 1 | **0** (« without FPU ») | 1 |
| `__MPU_PRESENT`, `__NVIC_PRIO_BITS`, `__CM4_REV`, `__Vendor_SysTickConfig` | 1, 3, 0x0001, 0 | idem (suffixe `U`) | idem |
| `__VTOR_PRESENT` | absent | 1 | 1 |
| IRQ propres | `GPIO_IRQn` = 0 | 0..31 (WDT…SPI) | idem |
| Périphériques | `ARM_GPIO*` | `ARM_UART*`, `ARM_TIM*`, … | idem |

  - Le BSP et la famille `qemu-mps2` n'utilisent aucun `*_IRQn` ni `ARM_*` de l'en-tête.
  - Ils n'utilisent que `SystemCoreClock`, `SystemCoreClockUpdate`, `SystemInit` (prototypes
    identiques) et `__NVIC_PRIO_BITS`.
  - `__VTOR_PRESENT` ne sert dans `core_cm4.h` 5.9.0 qu'à un avertissement sous
    `__CHECK_DEVICE_DEFINES` : aucun avertissement aujourd'hui (`-fsyntax-only` de
    `qemu_mps2_board.c`).
- **Équivalent pour un M4F** : `ARMCM4_FP.h`. `ARMCM4.h` de CMSIS 5 passerait `__FPU_PRESENT` à 0,
  ce qui serait faux pour un M4F.
- **Écart de binaire attendu.**
  - Code et données identiques : mêmes macros utilisées, mêmes prototypes.
  - `.debug_*` changés : chemin d'en-tête, et énumération `IRQn` plus longue dans `.debug_info`.
  - À confirmer par l'oracle après.
- **Modification** : `#include` et commentaire de `qemu_mps2_machine.h`, dans le seul greffon
  `bsp-qemu-mps2-an386`. Aucun fichier n'est ajouté ni retiré, donc pas de regreffe.

### 1.5 D6 — `scripts/tiers/compiler-hal-f4-a-blanc.sh`
- **Constat.** Le script compile les ordres `v330` et `cmsis5` pour F429 et F439. L'ordre `v330`
  échoue toujours sur `stm32f4xx_ll_usb.c` (ENV-34), donc le script rend 1. Son en-tête annonce
  « 0 si aucune erreur ».
- **Options.**
  - **a** : retirer l'ordre `v330`. Depuis ENV-42, aucun preset M4 ne le voit. Le résultat
    historique reste dans les rapports d'ENV-34 et d'ENV-42.
  - **b** : garder `v330` sans compter son échec : il reste dans `resume.txt`, marqué « comparaison ».
  - **c** : option `--avec-v330`, absente par défaut.
- **Recommandation** : a, la plus simple. ENV-46 (retrait de la SPL) et ENV-50 n'ont besoin que de
  l'ordre des presets.

### 1.6 D7 — Documentation de CMSIS-Core V3.30
- **Constat.** `ucore/cmsis/` est un paquet mixte :
  - base CMSIS **2.10** du 25 juillet 2011 : `CMSIS/README.txt`, `Device/ARM/ARMCM{0,3,4}` en
    V1.05 ;
  - en-têtes `CMSIS/Include/core_*.h` remplacés par des **V3.30** de février 2014. Leur macro
    `__CM4_CMSIS_VERSION_SUB` vaut `0x20`, soit 3.20. Rien ne permet de vérifier contre l'amont :
    aucun clone de CMSIS 3.x n'est disponible.
  - `source.txt` (« Version 2.10 », `onarm.com`) décrit la base, pas les en-têtes.
  - Aucun fichier ne relie ces faits. Un seul commit : 037cd59, « initial commit ».
- **Proposition.**
  - Nouveau `ucore/cmsis/LEPTON-PROVENANCE.md` dans le clone noyau, sur le modèle de
    `cmsis-5/CMSIS/Core/LEPTON-PROVENANCE.md`. Contenu : composition du paquet, versions par
    ensemble, incohérence de la macro, qui l'utilise encore depuis ENV-42 (M3 sans preset,
    armv6m masqué, D5), aucun en-tête modifié.
  - `source.txt` inchangé (fichier d'origine), cité par la provenance.
  - Un fichier ajouté, donc `scion graft` : +1 lien.

### 1.7 D9 — Messages non remis (§2bis)
- **Constat** (R43-1). `ORDRE` remis. `ACCUSÉ` et 4 `AVANCEMENT` non remis (bridge ECONNRESET,
  « bridge ID is stale »). L'utilisateur a fait poursuivre la VM. Seule la `FIN-SUCCÈS` est arrivée.
- **Texte proposé** pour ORCHESTRATION §2bis, nouvelle règle après « Sans accusé … » :
  > **Remise en échec** (D9 d'ENV-44, constat de R43-1) : l'émetteur dont l'envoi échoue (erreur
  > du canal, ECONNRESET, « bridge ID is stale ») le renvoie une fois. Si le second envoi échoue,
  > il consigne le message en entier dans son journal (VM : `rapports/env-N-debian.md` §Messages,
  > avec la mention « non remis ») et l'annonce à l'utilisateur. L'utilisateur relaie : il colle
  > dans l'autre session la première ligne `[<TYPE> <ID>]` et le corps, inchangés. Le destinataire
  > tient un message relayé pour reçu s'il porte le bon `ID`. Il le consigne avec la mention
  > « relayé par l'utilisateur » et y répond normalement ; sa réponse peut à son tour être relayée.
  > Un `ACCUSÉ` relayé vaut accusé. Si l'utilisateur fait poursuivre le destinataire sans relais,
  > c'est sa décision : la session principale la consigne au journal, et les messages manquants
  > sont lus dans le rapport du destinataire avant toute fusion.

## 2. PA-75 (2026-11-09, décisions de l'utilisateur)
| Point | Décision |
| --- | --- |
| D1 | Essais A (`seed replace`) et B (`seed add` puis `seed remove`) du §1.1. Tout défaut révélé est corrigé dans ENV-44, que ce soit dans lepton ou dans scion. Pour scion : nouvelle version, publication (PA-P), `SCION_MIN_VERSION`, `SCION_REF`. |
| D2 | Contrôle scripté sans carte, puis essai réel sous VSCodium par l'utilisateur : NUCLEO-F429ZI, `nucleo-f429zi-embos`. |
| D3 | Analyse par commande simple (§1.3). Tests dans `tests/test_proteger_trunk.py`. |
| D5 | Bascule vers `ARMCM4_FP.h`. Critère : code 0 hors `.debug_*` ; écarts `.debug_*` expliqués ; fumée, KAL et `ctest -N` identiques. Nouvel oracle de référence. |
| D6 | Option a : ordre `v330` retiré. |
| D7 | `ucore/cmsis/LEPTON-PROVENANCE.md` ; `source.txt` inchangé. |
| D9 | Texte du §1.7 tel quel. |
