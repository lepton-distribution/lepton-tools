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

Une décision complémentaire a été prise pendant D1. Le défaut constaté au §3.1 se corrige dans
scion 0.6.2.0, par une nouvelle règle P-G6, plutôt que dans lepton seul. C'est une décision de
l'utilisateur.

## 3. Corrections et essais

### 3.1 D1 — `seed replace` / `seed remove` d'une famille porteuse
Fichiers : `env-44-residus/d1-releve.sh` ; relevés dans `env-44-residus/d1/` (`*-liens.txt` au
format `chemin -> cible`, `*-grafted.txt`, `*-status.txt`, `*-clones.txt`).

- **Essai A, scion 0.6.1.0** (`essais/env-44-d1-replace`, copie de `env-11/f429zi`). Commande :
  `lepton seed replace stm32f4xx file://localhost/…/essais/env-44-d1-sources/lepton-famille-stm32f4xx.git`
  (clone nu de `family-stm32f4xx` 7afd7f1). Elle rend 0.
  - **Défaut** : les liens passent de 3389 à 3183, soit −206. Les 2 clés projetées restent dans la
    liste greffée, avec « 0 fichier(s) » : le trunk n'a plus la HAL ni le CMSIS device F4.
  - **Décomposition** (`essais/env-44-d1-pas`, A2-1 à A2-5) :
    - `graft-remove` du porteur est conforme à P-P6 : il retire les 2 clés et l'annonce ;
    - `seed-clone` réinscrit la famille et ses 2 clés ;
    - `graft --scion lepton@family-stm32f4xx` ne lie que la famille (129 feuilles).
  - **Reprise** : `graft --scion` de chaque clé tiers rend des liens identiques à l'état avant.
- **Essai B, scion 0.6.1.0** (`essais/env-44-d1-remove`, copie de `env-11/qemu`, BSP an386).
  - `lepton seed add stm32f4xx --type famille <URL>` a le même défaut : 3058 + 129 liens, clés
    projetées à 0 fichier.
  - `lepton seed remove stm32f4xx` est conforme à P-P6 : clés et liens reviennent à l'état avant,
    les clones tiers et celui de la famille sont conservés.
- **Correctif, scion 0.6.2.0.** seed.scions, branche `devenv/env-44` :
  - **9c7ba79** :
    - `graft_scions` ajoute aux clés nommées les clés projetées que porte chacune
      (`_carried_entries`, factorisé avec `remove`), et le dit ;
    - règle **P-G6** de `doc/projection-miroir.md` (§A.10, table A.11) ;
    - 3 tests : deux échouent sur le code de 0.6.1.0, le troisième vérifie que P-G5 n'a pas changé.
  - **213d2c0** : version 0.6.2.0, CHANGELOG. Le test de version attendait encore `0.6.0.0` au tag
    0.6.1.0 (O-1).
  - Tag annoté local **0.6.2.0**. Suite complète : 269 tests réussis, 1 sauté (réseau).
  - Installé par `pipx install --force git+file://<SEED_SCIONS>@0.6.2.0`.
- **lepton.**
  - `SCION_MIN_VERSION` (0, 6, 2, 0), README, `SCION_REF` 0.6.2.0 d'`install-vscodium.sh`
    (bca408a). Clone noyau : `install-{macos,debian}.sh`, README, README-PAQUET, BUILDING (54be710).
  - Test `test_seed_replace_porteur_garde_les_projections`.
  - lepton réinstallé par pipx.
- **Essais rejoués en 0.6.2.0.**
  - A : 3389 liens, liste `chemin -> cible` identique à l'avant, 200 + 6 fichiers projetés.
  - B : 3058 + 129 + 206 = 3393 liens à l'ajout ; retour exact à l'état avant au retrait.
- Piège : lepton n'accepte une URL `file://` qu'avec un hôte (`file://localhost/…`, forme
  documentée par `parse_location`). Sans hôte, elle est lue comme un chemin local.

### 3.2 D2 — Table clone tiers → trunk de l'extension
- **Contrôle scripté** (`env-44-residus/d2-table.py`, `d2-table.txt`). On prend le
  `-file-list-exec-source-files` de gdb sur les 4 presets F4. Chaque `fullname` sous
  `depots/tiers/` passe par le `toTrunk` réel (`srcmap.js` recompilé, identique à `out/`), avec la
  table de `seed status --json` construite comme `debug.ts`.
  - Résultat : 10, 9, 10 et 9 sources ou en-têtes tiers, tous ramenés à un lien existant du trunk,
    de même `realpath`.
- **gdb sur la carte**, sans écriture (`env-44-residus/d2-gdb-carte.sh`, `.log`).
  - Arrêt sur `main`, puis sur `HAL_GPIO_Init` (`stm32f4xx_hal_gpio.c:177`).
  - Pile d'appels : `gpio_set_mode` ← `gpio_init` ← `dev_nucleo_f439zi_board_load` ←
    `_kernel_warmup_dev`.
  - Le cadre MI donne `file` = trunk et `fullname` = `…/depots/tiers/stm32f4xx-hal-driver/v1.8.5/Src/stm32f4xx_hal_gpio.c`,
    à l'arrêt comme après deux `next`.
- **Sous VSCodium**, essai de l'utilisateur sur `~/lepton/original-tree.code-workspace`, lancement
  « Déboguer nucleo-f429zi-embos (carte, OpenOCD) », flash par `load` :
  - point d'arrêt de ligne 177, posé onglet fermé ;
  - à l'arrêt, l'onglet ouvert est
    `/Users/cle_d_anton/lepton/trunk/sys/root/src/kernel/dev/arch/cortexm/stm32f4xx/hal_driver/Src/stm32f4xx_hal_gpio.c` ;
  - **conforme**.
- **Incidents de la session de carte** (§4.3) : reset matériel bloqué, et un arrêt inattendu dans
  `ls.c:107`.
- **Image flashée** : `nucleo-f429zi-embos` du Mac. `verify_image` ne montre que les 4 octets de
  bourrage connus, 0x080001ac à 0x080001af.

### 3.3 D3 — Hook
- Commit 48f788c. `.claude/hooks/proteger-trunk.py` analyse chaque commande simple :
  - découpage `shlex` sur le saut de ligne, les parenthèses et les accents graves ;
  - suivi de `cd` et des variables (`X=…`, `for X in …`) ;
  - verbes classés par chemin écrit ;
  - récursion pour `bash -c`, `eval`, `find -exec`/`-delete`, `xargs` et le heredoc d'un shell ;
  - le corps d'un heredoc de données n'est plus jugé ;
  - `git -C` refusé hors des sous-commandes de lecture ;
  - l'ancienne règle s'applique en repli.
- Résultats :
  - les 42 cas de l'audit passent de 14 écarts à 0 ;
  - `tests/test_proteger_trunk.py` : 118 cas, dans les deux sens, en chemin absolu et relatif, vers
    le trunk et vers un clone tiers, plus les 4 outils de fichier.
- Deux faux positifs du nouveau hook sont apparus pendant la session. Ils sont corrigés et couverts
  par des tests :
  - `$` hors des caractères de mot ;
  - le heredoc d'un script Python.
- Documentation : ORCHESTRATION §5bis, `CLAUDE.md`, skill `lepton-rootstock` (7c18954).

### 3.4 D5 — `ARMCM4_FP.h` dans le BSP an386
- `bsp-qemu-mps2-an386` `devenv/env-44`, commit **755e80d** : `#include` et commentaire de
  `qemu_mps2_machine.h`. Aucun fichier ajouté ni retiré.
- **Preuve d'objet** (`env-44-residus/d5-objet.py`, `d5/`). `qemu_mps2_board.c` est le seul objet
  qui inclut l'en-tête. Compilé avec l'ancien et le nouvel en-tête, pour les 4 presets : toutes les
  sections chargées (`.text*`, `.rodata*`, `.data*`, `.bss*`) sont identiques octet pour octet, et
  le désassemblage aussi.

### 3.5 D6 — Script de compilation à blanc
- Commit ad165b4 : l'ordre `v330` est retiré, la boucle est simplifiée, `shellcheck` est propre.
- Résultat : code 0. F429 et F439 : 90 sources, 0 échec, 0 avertissement, `core_cm4.h` CMSIS 5.
  Identique à `env-42-core-cm4/compilation-a-blanc-apres` (`env-44-residus/d6/resume.txt`).

### 3.6 D7 — Provenance de CMSIS V3.30
- Clone noyau `devenv/env-44`, commit **253be2a** : `kernel/core/ucore/cmsis/LEPTON-PROVENANCE.md`.
  Il décrit le paquet mixte, la macro 0x20, les utilisateurs restants et `source.txt`, conservé.
  Aucun en-tête n'est modifié.
- `scion graft --scion lepton@original::tree` : 3982 → 3983 liens (+1, ce fichier), 0 lien cassé.

### 3.7 D9 — §2bis
- Commit b7393b4 : règle « Remise en échec » d'ORCHESTRATION §2bis, texte du §1.7.

## 4. Contrôles → PA-76

### 4.1 Oracle
- **Avant** (`oracles/env-44-avant/`, `rejouer-oracle.sh` aux arguments d'ENV-41, 6 QEMU et
  10 cartes, constructions à neuf) :
  - code 0 sur les 16 presets contre `env-42-apres` ;
  - empreintes mklepton identiques ;
  - host 7/7 ;
  - `ctest -N` 17/17 identiques.
- **Après** (`oracles/env-44-apres/`, comparaisons dans `comparaisons/`) :

| Preset | Sections/symboles | Empreinte | Fumée | Banc KAL | Écarts expliqués |
| --- | --- | --- | --- | --- | --- |
| `qemu-mps2-an386-embos` | code 1 : `.debug_info` +132, `.debug_line` +5, `.debug_str` +219 | différente | identique | 19/19 identique | oui (D5) |
| `qemu-mps2-an386-embos-soft` | code 1 : mêmes 3 sections, mêmes deltas | différente | identique | 15/15 identique | oui (D5) |
| `qemu-mps2-an386-freertos` | code 1 : idem | différente | identique | 19/19 identique | oui (D5) |
| `qemu-mps2-an386-freertos-soft` | code 1 : idem | différente | identique | 15/15 identique | oui (D5) |
| `qemu-mps2-an500-{embos,freertos}` | code 0 | différente | identique | 18/18 identique | — |
| 10 presets de carte | code 0 | différente | — | — | — |
| `host` | mklepton identiques | | | ctest 7/7 | — |

- **Explication des écarts an386.** Seules les sections DWARF changent :
  - `.debug_str` porte le nouveau chemin d'en-tête et les noms de l'énumération `IRQn` de CMSIS 5
    (23 interruptions propres au lieu d'une, `GPIO_IRQn`) ;
  - `.debug_info` porte les types correspondants ;
  - `.debug_line` porte le chemin `cmsis-5/Device/ARM/ARMCM4/Include`.

  Sections chargées et symboles : identiques (code 0 hors `.debug_*`). La preuve d'objet du §3.4 le
  confirme : critère du PA-75 atteint.
- **Empreintes.** Elles diffèrent pour **tous** les presets, an500 et cartes compris, entre deux
  constructions de la même source : l'heure de compilation est incluse dans l'image (« kernel
  compilation date »). Ce n'est pas un écart.
- **Journaux** (`env-44-residus/comparer-journaux.py`, `comparaisons/journaux.txt`). Ignorés :
  - la date et l'heure de compilation ;
  - les durées de ctest ;
  - le jeton aléatoire `lepton-uart1-<n>` ;
  - les lignes asynchrones `rcv SIGCHLD` et le numéro d'invite qui les suit ;
  - les lignes vides.
- `ctest -N` : 17/17 identiques à l'avant.
- **Nouvel oracle de référence** : `oracles/env-44-apres/`.

### 4.2 Autres contrôles
- `<ROOTSTOCK>` : 3983 liens, 0 lien cassé ; fichiers réguliers tolérés seulement ; `lepton check`
  code 0 (19 fichiers conformes) ; `seed status` : 200 + 6 fichiers projetés.
- Tests :
  - `pytest` de lepton : 362 réussis (243 + 118 du hook + 1) ;
  - scion : 269 réussis, 1 sauté.
- Hook : écriture sous `trunk/` et `depots/tiers/` toujours refusée (tests `test_ecriture_refusee`).
- `compiler-hal-f4-a-blanc.sh` : code 0.

### 4.3 Observations
- **O-1** : le test de version de seed.scions attendait `0.6.0.0` au tag 0.6.1.0. Il échouait donc
  en 0.6.1.0, alors que le rapport d'ENV-40 annonce 265 réussis. Il est corrigé en 0.6.2.0.
- **O-2** : lepton ne relaie pas les messages d'information de scion, même avec `-v` : « clés
  projetées retirées… » (P-P6), « … regreffées… » (P-G6). Point ajouté à `HORS-PLAN.md` (D10), non
  traité.
- **O-3, NUCLEO-F429ZI revenue de la VM.** La carte gardait l'image `nucleo-f439zi-embos` de
  Debian.
  - État initial : cœur bloqué dans le HardFault, HFSR = 0x80000000 (DEBUGEVT).
  - Le `reset halt` par NRST (`srst_only` de `board/st_nucleo_f4.cfg`) expirait. Mesure : 3 échecs
    sur 3, alors que le reset logiciel (`reset_config none`) réussissait 2 fois sur 2.
  - Conséquences :
    - Cortex-Debug échoue sur « Protocol error with Rcmd: FC » (`monitor reset halt`) ;
    - une fois, OpenOCD 0.12.0 s'est arrêté au `load` sur l'assertion `stm32f2x.c:1221`. La taille
      de flash a été lue 0x2003, pendant que le programme de flashage tournait en RAM
      (pc 0x20000044). Après un reset logiciel, la valeur lue est la bonne (0x0800).
  - Parade : une coupure d'alimentation (USB débranché). Ensuite, 3 resets matériels sur 3
    réussissent.
  - Consigné dans la skill `lepton-cibles` (b1cc378). Cause matérielle exacte non établie.
- **O-4** : au premier lancement sous VSCodium, la session s'est arrêtée dans `sbin/ls.c:107`
  (`return -1` après `opendir`). Aucun point d'arrêt n'était enregistré pour l'espace de travail.
  Cause non établie. L'onglet affichait le chemin du trunk.
- **O-5** : rootstocks d'essai créés dans `~/lepton-tools-dev/essais/` : `env-44-d1-replace`,
  `env-44-d1-pas`, `env-44-d1-remove`, `env-44-d1-sources`. Leur sort se décide au PA-76.

### 4.4 Branches et commits (rien de poussé)
| Dépôt | Branche | Depuis | Commits |
| --- | --- | --- | --- |
| lepton-tools | `devenv/env-44` | `main` 7140e9c | audit, D9, oracle avant, D3, D6, oracle après, D1 lepton, skills, D1/D2 relevés, rapport |
| seed.scions | `devenv/env-44` | `master` f29fa35 | 9c7ba79 (P-G6), 213d2c0 (0.6.2.0) ; tag local `0.6.2.0` |
| clone noyau | `devenv/env-44` | `master` 763dda2 | 253be2a (D7), 54be710 (`SCION_REF`) |
| `bsp-qemu-mps2-an386` | `devenv/env-44` | `master` 5819047 | 755e80d (D5) |

Ordre de publication proposé :
1. seed.scions : fusion dans `master`, puis tag `0.6.2.0` poussé avec `master`.
2. Clone noyau et BSP an386 : fusion dans `master`, push.
3. lepton-tools : fusion dans `main`, push.

`<ROOTSTOCK>` est déjà greffé sur les branches d'étape. Après les fusions, il suffit de remettre
chaque clone sur `master` : le contenu est identique, et aucune regreffe n'est nécessaire.
