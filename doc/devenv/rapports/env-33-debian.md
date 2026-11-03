# ENV-33 — Validation Debian groupée (ENV-29 à ENV-32) — 2026-11-03

Session VM Debian (`debian-linux-vm`) conduite selon la consigne `env-33-debian.md` (lepton-tools
`devenv/env-33` e47bc11, blob 8b52718, SHA-256 `ff577d12…5042e557`) ; ordre `R33-1` de la session
Mac `validation-debian-env-33`, décisions PA-53. La session exécute, constate et rapporte ; aucune
correction de code. Journaux : `~/env-33-journaux/` sur la VM (hors git). Rootstocks conservés :
`~/lepton-tools-dev/essais/env-28-debian` (`$U`, mis à jour au §7.1) et `env-33-debian` (`$R`).

Bilan : C1 à C8 conformes. Un `.text` non nul hors du preset du Mac (`nucleo-wl55jc1-freertos`,
+64) vient du seul bourrage d'alignement ; il est admis par le §8.1 et signalé (§4).

## 1. Hôte et versions (§5, §6)

| Élément | Valeur |
| --- | --- |
| Système | Linux x86_64, Debian 13.7, noyau 6.12.107+deb13-amd64, utilisateur `lepton-user` |
| git | 2.47.3 |
| scion | 0.5.3.0 avant ; **0.5.4.0** après `install-debian.sh` (`git+…/seed.scions.git@0.5.4.0`, « == scion 0.5.4.0 ») |
| lepton | 0.1.0 avant (`scion 0.5.3.0 (requis ≥ 0.5.3.0)`) ; 0.1.0 après `pipx install --force` de `devenv/env-33` e47bc11 (`scion 0.5.4.0 (requis ≥ 0.5.4.0)`) |
| `pipx list` | `lepton 0.1.0`, `scion 0.5.4.0` |
| arm-none-eabi-gcc | 14.2.1 20241119 (paquet Debian `15:14.2.rel1-1`) ; gcc hôte 14.2.0 (Debian 14.2.0-19) |
| cmake / ninja | 3.31.6 / 1.12.1 |
| QEMU | 10.0.13 (Debian 1:10.0.13+ds-0+deb13u1) |
| Python | 3.13.5 |
| Outils de débogage | openocd 0.12.0 ; clangd 19.1.7 (3+b1) ; doxygen 1.9.8 |
| VSCodium | 1.135.06055 (dpkg 1.135.06055) ; 12 extensions (`6.2-extensions.txt`), dont `vadimcn.vscode-lldb@1.12.3`, `lepton-distribution.lepton@0.5.1`, `mcu-debug.rtos-views@0.0.16`, `ms-vscode.cmake-tools@1.24.42`, `marus25.cortex-debug@1.13.0-pre6`, `llvm-vs-code-extensions.vscode-clangd@0.6.0` |
| embOS | présent : `LEPTON_EMBOS_ROOT=~/lepton/third_party/embos/cortexm-gcc/5.20.0.0` |
| Espace | `/home` 26 Go (18 Go libres) ; `/tmp` 747 Mo (688 Mo libres) |
| lepton-tools | propre (sur `devenv/env-28-debian`) ; après `fetch`, `devenv/env-33` = e47bc11 |
| Clone noyau | propre, `master` ; avance rapide 0c0cc4f → b3a5415 (7 commits, dont le retrait de `scion/tests/board_radio.py`) ; `install-debian.sh:55` `SCION_REF="${SCION_REF:-0.5.4.0}"` |
| `git ls-remote` | scion tag `0.5.4.0^{}` 99aa973 ; graine `original-tree` 15740f9 ; 13 dépôts `master` aux commits du §1 de la consigne (noyau b3a5415, `bsp-nucleo-wl55jc1` ef51ec1) ; `devenv/env-14` : noyau e5a5689, `famille-stm32f4xx` af964c6 |
| `$U` au §5 | graine 15740f9 propre ; 14 entrées ; 13 clones sur `master`, amont `origin/master`, 0 modification (noyau 0c0cc4f, `bsp-nucleo-wl55jc1` c9183de, autres au §1) ; 3956 liens, 0 cassé, 0 régulier |
| `$P` au §5 | graine `depots/lepton-seed/env11` ; BSP an386 046779e (« Fusion de devenv/env-6 »), manifeste sans `"tests"` |

## 2. Critères (§12)

| Critère | Attendu | Constaté | Verdict |
| --- | --- | --- | --- |
| C1 scion et lepton | `ls-remote` conforme ; scion 0.5.4.0 par `install-debian.sh` (défaut `SCION_REF`) ; `pipx` code 0 ; lepton 0.1.0, scion 0.5.4.0 accepté | `ls-remote` conforme (§1) ; `install-debian.sh` lancé sans `SCION_REF` ni `SCION_SPEC`, installe scion 0.5.4.0 depuis le tag ; `6.2-lepton.log` code 0 ; `lepton 0.1.0`, `scion 0.5.4.0 (requis ≥ 0.5.4.0)` | conforme |
| C2 Scripts d'installation | `install-debian.sh` (b3a5415) code 0 ; `install-vscodium.sh` code 0 deux fois, `changements 0` à la seconde | lancés par l'utilisateur ; quatre codes 0 ; `changements 0` aux deux exécutions d'`install-vscodium.sh` ; extensions attendues présentes | conforme |
| C3 `graft-update` et rootstock | §7.1 : code 0, 0 conflit, noyau et BSP WL55 avancés, 3957 liens, diff de 3 lignes ; §7.2 : code 1, 2 clones refusés, trunk et liste intacts, clones non déplacés, copie supprimée ; §7.3 : 14 entrées, 3957 liens, 0 cassé, 0 régulier, liste = `$U` | §7.1 : code 0, aucune ligne « conflit » ni « refus » ; `merge --ff-only @{u}` sur `original` et `bsp-nucleo-wl55jc1` seulement, aucun `git pull` ; graine 15740f9 ; 14 entrées ; 13 clones sur `master`, propres, au §1 ; 3957 liens (3956 avant), 0 cassé, 0 régulier ; `.scion.grafted.list` inchangé ; diff = les 3 lignes attendues. §7.2 : code 1, « 2 clone(s) à remettre à leur version déclarée … (trunk et clones inchangés) », chacun nommé avec sa branche et `git -C … switch master` ; aucun conflit ; liste des liens et `.scion.grafted.list` identiques avant et après ; clones sur `devenv/env-14` (e5a5689, af964c6), propres ; copie supprimée par l'utilisateur, `$U` inchangé. §7.3 : trois codes 0 ; 14 entrées ; 13 clones sur `master` au §1 ; 3957 liens, 0 cassé, 0 régulier ; liste identique à `$U` | conforme |
| C4 Constructions | host 7/7, mklepton = `env-32-apres` = `env-28-debian` ; 16 presets ; QEMU fumée et banc 20/20, 16/16, 19/19 ; `comparer_R28-1` embOS 0, FreeRTOS dans le critère §8.1 ; `f429→f439` 0 | `rejouer-oracle.sh` code 0 (« tout a réussi ») ; host 7/7 ; empreintes mklepton identiques aux deux (50 lignes) ; 16/16 construits ; fumée `smoke.lsh` Passed (6 QEMU) ; banc an386 20/20, an386 soft 16/16, an500 19/19 ; `peripheriques` Passed dans les 4 an386 ; `comparer_R28-1` embOS 0 (8), FreeRTOS 1 (8) dans le critère (§4) ; `f429→f439` embos 0, freertos 0 ; trunk : 0 cassé, 0 régulier | conforme (`.text` +64 WL55 FreeRTOS signalé, §4) |
| C5 Tâche « tests des greffons » | `check`, `generate` code 0 sur `$R` ; 4 tâches an386, aucune an500 ni cartes ; forme §9.1 ; tâche `qemu-mps2-an386-embos` 2/2 code 0 ; pas de `__pycache__` | `check` code 0 (« 19 fichier(s) conforme(s) »), `generate` code 0 ; 23 `"request"`, 10 `"svdFile"`, 7 `"type": "lldb"` ; 4 tâches (an386 embos, embos-soft, freertos, freertos-soft), forme conforme (§5) ; exécution : `smoke.lsh` et `qemu-mps2-an386.peripheriques` Passed, « 100% tests passed, 0 tests failed out of 2 », code 0 ; 0 `__pycache__`, 0 fichier régulier | conforme |
| C6 Graine de projet `env11` | `check`, `generate` code 0 ; `check`, presets, graine identiques ; espace : tâches ENV-30 seules ou identique selon le BSP de `$P` | régénération puis relevé au §6.1 (« inchangé ») ; après réinstallation : codes 0 ; empreintes identiques (`CMakeUserPresets.json` d5ee81e4…, `env11.code-workspace` b2c7b8a4…) ; graine, sortie de `check`, presets identiques ; espace **identique** (diff vide), conforme au second cas (BSP 046779e sans `"tests"`) | conforme |
| C7 Test radio (découverte) | `ctest -N` 16/16/15/0 et `-L greffon:` = Mac ; `nucleo-wl55jc1.radio` déclaré par le BSP ; `board_radio.py` absent | `relever-ctest-N.sh` code 0 ; `banc` 16, `fictif` 16, `seul` 15, `sans` 0 (embOS et FreeRTOS) ; 16 fichiers `*.ctest-N*.txt` identiques à `env-32-apres` ; `nucleo-wl55jc1.radio` : étiquettes `greffon:nucleo-wl55jc1`, `board`, `radio`, commande `…/bsp/nucleo-wl55jc1/tests/radio.py` avec `--tests-noyau $R/trunk/tests` ; `trunk/tests/board_radio.py` absent ; 0 `__pycache__` | conforme |
| C8 Nettoyage | `env-14-debian` et `~/env-28-journaux` supprimés par l'utilisateur, taille relevée ; copie `$C` supprimée | tailles 344 Mo et 1,3 Mo ; `rm -rf` lancé par l'utilisateur ; `ls -d` : absents ; `$C` supprimée au §7.2 ; `$U`, `$R`, `$P`, `$J` conservés | conforme |

Fumée (`qemu-mps2-an386-freertos/fumee.log`) : `uname -a` →
`lepton-cortexm4-32  4.10.0.2 Nov  3 2026-18:05:02 cortexM4-qemu-mps2-an386`.

## 3. Presets (§8)

| Preset | Construction | Fumée | Banc KAL | Symboles (R33-1 / R28-1 / Mac `env-32-apres`) | `comparer_R28-1` | `comparer_Mac` |
| --- | --- | --- | --- | --- | --- | --- |
| host | oui | — | ctest 7/7 | — | empreintes = `env-32-apres` = `env-28-debian` | — |
| qemu-mps2-an386-embos | oui | oui | 20/20 | 1599 / 1599 / 1583 | 0 | 1 |
| qemu-mps2-an386-embos-soft | oui | oui | 16/16 | 1596 / 1596 / 1580 | 0 | 1 |
| qemu-mps2-an386-freertos | oui | oui | 20/20 | 1639 / 1639 / 1623 | 1 | 1 |
| qemu-mps2-an386-freertos-soft | oui | oui | 16/16 | 1638 / 1638 / 1622 | 1 | 1 |
| qemu-mps2-an500-embos | oui | oui | 19/19 | 1561 / 1561 / 1545 | 0 | 1 |
| qemu-mps2-an500-freertos | oui | oui | 19/19 | 1601 / 1601 / 1585 | 1 | 1 |
| nucleo-f429zi-embos | oui | — | — | 1793 / 1793 / 1777 | 0 | 1 |
| nucleo-f429zi-freertos | oui | — | — | 1833 / 1833 / 1817 | 1 | 1 |
| nucleo-f439zi-embos | oui | — | — | 1793 / 1793 / 1777 | 0 | 1 |
| nucleo-f439zi-freertos | oui | — | — | 1833 / 1833 / 1817 | 1 | 1 |
| nucleo-wl55jc1-embos | oui | — | — | 1230 / 1230 / 1215 | 0 | 1 |
| nucleo-wl55jc1-freertos | oui | — | — | 1276 / 1276 / 1261 | 1 | 1 |
| samd21-xplained-pro-embos | oui | — | — | 941 / 941 / 926 | 0 | 1 |
| samd21-xplained-pro-freertos | oui | — | — | 991 / 991 / 976 | 1 | 1 |
| stm32f746g-disco-embos | oui | — | — | 1640 / 1640 / 1624 | 0 | 1 |
| stm32f746g-disco-freertos | oui | — | — | 1676 / 1676 / 1660 | 1 | 1 |

`comparer_Mac` = 1 partout (informatif : chaînes de compilation différentes). `f429→f439` :
embos 0, freertos 0.

## 4. Nature des écarts FreeRTOS (`comparer_R28-1` = 1)

Communs aux 8 presets FreeRTOS (critère du PA-49) :
- `xTaskCreateStatic` (T) 0x1f8 → 0x1fc (+4) ; `samd21-xplained-pro-freertos` 0x1f0 → 0x1f4 ;
- `xIdleTaskTCB.3` et `xTimerTaskTCB.1` (b) 0x54 → 0x58 ;
- `.ccm_bss` +8 (56400 → 56408 ; `nucleo-wl55jc1` 25280 → 25288 ; `qemu-mps2-an386-freertos-soft`
  55840 → 55848 ; `samd21` 13600 → 13608) ;
- sections `.debug_info`, `.debug_line`, `.debug_loclists`, `.debug_str` et empreintes
  `.bin`/`.elf`/`.hex` : différentes (libres).

Aucun symbole ajouté ni retiré, aucune autre taille de symbole changée ; `.data`, `.bss`, `.noinit`
inchangés. `.text` : 0 sur 7 presets, dont `qemu-mps2-an386-freertos` (+16 au Mac, 0 ici).

| Preset | `.text` | Autre ligne |
| --- | --- | --- |
| qemu-mps2-an386-freertos | 0 | — |
| qemu-mps2-an386-freertos-soft | 0 | — |
| qemu-mps2-an500-freertos | 0 | — |
| nucleo-f429zi-freertos | 0 | — |
| nucleo-f439zi-freertos | 0 | — |
| nucleo-wl55jc1-freertos | **111888 → 111952 (+64)** | — |
| samd21-xplained-pro-freertos | 0 | — |
| stm32f746g-disco-freertos | 0 | — |

**`nucleo-wl55jc1-freertos`, `.text` +64 (signalé, admis) :** comparaison `nm -n -S` des ELF de
`$U/build` (construction R28-1 du 2026-11-02 16:44, non reconstruite depuis) et de `$R/build`.
`.text` alignée 2**6 dans les deux. Seule taille changée : `xTaskCreateStatic`. Décalage des
adresses : +0 jusqu'à `xTaskCreateStatic`, +4 dès `vTaskDelete` (0x08008014 → 0x08008018), +8 à
`__dtostr`, +32 à `strcmp`, +64 à `strlen` (0x08017b40 → 0x08017b80) : +4 plus le bourrage
d'alignement qui en résulte. `.ccm_bss` +8 ; tailles de `.data` (0x340), `.bss` (0x1aec), `.noinit`
(4) inchangées. Journaux : `8.1-wl55-freertos-text.txt`, `8.1-wl55-freertos-nm-R28.txt`,
`8.1-wl55-freertos-nm-R33.txt`.

## 5. Tâche « tests des greffons » (§9.1)

Forme relevée pour chacune des 4 tâches (`9.1-taches-greffons.txt`) : `type` `process` ;
`command` `/usr/bin/ctest` ; `args` `["--preset", "<P>", "-L", "greffon:", "--output-on-failure"]` ;
`options.cwd` `$R/trunk` ; `options.env` `{"PYTHONDONTWRITEBYTECODE": "1"}` ;
`dependsOn` `["lepton : construire <P>"]` ; `group` `test` ; `problemMatcher` `[]` (aucune autre clé).

Commande exécutée (`9.1-tache-an386.sh`) :
`cd $R/trunk && env PYTHONDONTWRITEBYTECODE=1 /usr/bin/ctest --preset qemu-mps2-an386-embos -L greffon: --output-on-failure`
→ `smoke.lsh` Passed (3,29 s), `qemu-mps2-an386.peripheriques` Passed (0,83 s), code 0.

## 6. Écarts et constats

- **Remise des messages (§2bis) :** l'`ACCUSÉ R33-1` n'a pas pu être remis (`ECONNRESET`, deux
  essais ; émetteur absent de `ListAgents`). Il a été journalisé (`0-messages-R33-1.md`) ;
  l'utilisateur a décidé de poursuivre. Le premier `AVANCEMENT` (§6.2) en reprenait le contenu ; la
  session Mac l'a accepté comme accusé. Les envois suivants ont été acceptés par le serveur.
- **§7.1 (constat) :** scion 0.5.4.0 fait `fetch` de chaque clone puis `merge --ff-only @{u}`
  seulement sur les clones en retard (`original`, `bsp-nucleo-wl55jc1`) ; aucun `git pull`.
- **§7.2 (constat) :** après les deux `switch devenv/env-14`, 4 liens cassés dans la copie
  (`dev/arch/cortexm/stm32f4xx/svd/` : `STM32F429.svd`, `STM32F439.svd`, `README.md`,
  `LICENSE-Apache-2.0`), comme au Mac en ENV-29 ; non corrigés, toujours 4 après le refus. scion
  n'a pas fait `fetch` des deux clones refusés (seulement de la graine et des 11 autres).
- **§7.3 (forme) :** `7.3-trunk.tsv` produit par `find trunk -type l -exec readlink -n {} \;
  -printf '\t%p\n'` remis en ordre (chemin, cible), au lieu de la boucle `sh -c` de la consigne ;
  contenu équivalent (3957 lignes).
- **§9.2 (constat) :** sortie de `generate` de `$P` : « inchangé » ; un seul preset listé
  (`env11-debug-qemu`) avant et après réinstallation.
- **`.text` +64 de `nucleo-wl55jc1-freertos`** : §4.

## 7. Journal des messages (§2bis)

| ID | Date | Sens | Résumé |
| --- | --- | --- | --- |
| ORDRE R33-1 | 2026-11-03 | Mac → VM | consigne `env-33-debian.md` @ e47bc11 ; PA-53 : deux `graft-update` par l'utilisateur, C7 découverte seule, C8 accordé, push sur accord |
| ACCUSÉ R33-1 | 2026-11-03 | VM → Mac | §5 conforme, aucun écart visible — **non remis** (`ECONNRESET`), journalisé |
| AVANCEMENT R33-1 | 2026-11-03 | VM → Mac | contenu de l'ACCUSÉ ; §6.1 fait, noyau b3a5415 ; commandes du §6.2 à l'utilisateur |
| AVANCEMENT R33-1 | 2026-11-03 | Mac → VM | AVANCEMENT §6.2 accepté comme accusé ; poursuivre |
| AVANCEMENT R33-1 | 2026-11-03 | VM → Mac | §6 conforme (C1, C2) ; `graft-update` §7.1 à l'utilisateur |
| AVANCEMENT R33-1 | 2026-11-03 | VM → Mac | §7.1 conforme ; copie `$C` prête ; `graft-update` E-1 à l'utilisateur |
| AVANCEMENT R33-1 | 2026-11-03 | VM → Mac | §7.2 conforme (refus E-1) ; suppression de `$C` à l'utilisateur |
| AVANCEMENT R33-1 | 2026-11-03 | VM → Mac | §7 conforme (C3) ; §8 lancé |
| AVANCEMENT R33-1 | 2026-11-03 | VM → Mac | §8 conforme (C4) ; `.text` +64 WL55 FreeRTOS = bourrage, signalé |
| AVANCEMENT R33-1 | 2026-11-03 | VM → Mac | §9 et §10 conformes (C5, C6, C7) ; suppression du §11 à l'utilisateur |

## 8. Non fait

- Presets de carte : construits, capturés et configurés (§10) seulement ; aucun flashage, aucun
  test `board` (pas de carte sur la VM, PA-53).
- Push de `devenv/env-33-debian` : soumis à l'accord explicite de l'utilisateur (PA-P).
