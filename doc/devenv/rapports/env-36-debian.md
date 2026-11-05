# ENV-36 — Validation Debian groupée (ENV-34, ENV-35, HAL STM32F4) — 2026-11-05

Session VM Debian (`debian-linux-vm`) conduite selon la consigne `env-36-debian.md` (lepton-tools
`devenv/env-36` bd7ad59, blob d35bf06, SHA-256 `4f0d1b75…0500a7d7`) ; ordre `R36-1` de la session
Mac `validate-env-34-35-debian`, décisions PA-59 (carte, nettoyage), PA-11 (écriture flash des
3 images du §10), PA-P (push). La session exécute, constate et rapporte ; aucune correction.
Journaux : `~/env-36-journaux/` sur la VM (hors git). Rootstocks conservés :
`~/lepton-tools-dev/essais/env-28-debian` (`$U`, mis à jour au §6.1) et `env-36-debian` (`$R`).

Bilan : C1 à C7 conformes. Deux écarts, expliqués et acceptés par la session Mac en cours de
session : le comptage `cubemx` du §6.1 (défaut de la consigne) et le signe du delta `.noinit` des
presets F4 FreeRTOS (bourrage d'alignement, à trancher au PA-60) ; voir §6.

## 1. Hôte et versions (§5)

| Élément | Valeur |
| --- | --- |
| Système | Linux x86_64, Debian 13.7, noyau 6.12.107+deb13-amd64, utilisateur `lepton-user` |
| git | 2.47.3 |
| scion | 0.5.4.0 (inchangé, aucune réinstallation) |
| lepton | `lepton 0.1.0`, `scion 0.5.4.0 (requis ≥ 0.5.4.0)` |
| arm-none-eabi-gcc | 14.2.1 20241119 (paquet Debian `15:14.2.rel1-1`) |
| cmake / ninja | 3.31.6 / 1.12.1 |
| QEMU | 10.0.13 (Debian 1:10.0.13+ds-0+deb13u1) |
| Python | 3.13.5 |
| VSCodium | 1.135.06055 |
| OpenOCD | 0.12.0 |
| Chaîne APT | identique à R33-1 |
| embOS | présent : `LEPTON_EMBOS_ROOT=~/lepton/third_party/embos/cortexm-gcc/5.20.0.0` |
| Espace | `/home` 26 Go (18 Go libres) ; `/tmp` 747 Mo (691 Mo libres) |
| lepton-tools | propre ; après `fetch`, `devenv/env-36` = bd7ad59 |
| `git ls-remote` | scion tag `0.5.4.0^{}` 99aa973 ; graine `original-tree` 15740f9 ; noyau 2893297 ; `famille-qemu-mps2` 3954357 ; an386 09f4943 ; an500 e98a482 ; `famille-stm32f4xx` 0fd8b2a ; `bsp-nucleo-f429zi` b9fe2bf ; `bsp-nucleo-f439zi` 314f91b ; `famille-stm32wlxx` dbc58d7 ; `bsp-nucleo-wl55jc1` ef51ec1 ; `famille-stm32f7xx` d2d9aa9 ; `bsp-stm32f746g-disco` 6266908 ; `famille-samd21` a262e81 ; `bsp-samd21-xplained-pro` f3cffa2 — tous au §1 |
| `$U` au §5 | graine 15740f9 propre ; 14 entrées ; 13 clones sur `master`, amont `origin/master`, 0 modification, aux commits « En R33-1 » (noyau b3a5415, `family-stm32f4xx` 8364493, `bsp-nucleo-f429zi` 2b2dfdd, `bsp-nucleo-f439zi` bdbfa06) ; 3957 liens, 0 cassé, 0 régulier |
| `$R33`, `$P` au §5 | `$R33` et son espace présents ; graine `$P/depots/lepton-seed/env11` présente ; `~/env-33-journaux` présent |

## 2. Critères (§12)

| Critère | Attendu | Constaté | Verdict |
| --- | --- | --- | --- |
| C1 Versions | `ls-remote` = §1 ; scion 0.5.4.0, lepton 0.1.0 sans réinstallation ; chaîne APT relevée | conforme (§1) | conforme |
| C2 `graft-update` et rootstock | §6.1 : code 0, 0 conflit, noyau, F4, F429, F439 avancés ; ajouts 215 et retraits 194 = attendu ; aucun lien `cubemx_hal_driver/` (F4) ; 201 `hal_driver/`, 7 `Device/ST/STM32F4xx/` ; 3978 liens, 0 cassé, 0 régulier ; §6.2 : 14 entrées, 3978, 0, 0, liste = `$U` | §6.1 (lancé par l'utilisateur) : code 0 ; aucune ligne « graine », « conflit » ou « refus » dans le journal ; graine 15740f9 ; 14 entrées ; 13 clones sur `master`, propres, au §1 (noyau 2893297, F4 0fd8b2a, F429 b9fe2bf, F439 314f91b) ; ajouts = `attendu/liens-ajoutes.txt` (215), retraits = `attendu/liens-retires.txt` (194) ; comptage brut `cubemx 157` (tous `stm32wlxx/`, 157 avant et après), `stm32f4xx/cubemx_hal_driver/` 0 ; `hal_driver 201`, `device_f4 7` ; 3978 liens, 0 cassé, 0 régulier. §6.2 : trois codes 0 ; « greffe : 3978 feuilles liées » ; 14 entrées ; 13 clones sur `master` au §1 ; 3978, 0, 0 ; liste identique à `$U` | conforme (comptage `cubemx` : §6) |
| C3 Constructions | host 7/7 ; mklepton = `env-33-debian` = `env-35-apres` ; 16 presets ; QEMU fumée et banc 20/20, 16/16, 19/19 ; `comparer_R33-1` 12 presets 0, 4 F4 1 avec écarts normalisés = Mac ; `f429→f439` hors `.debug_*` 0 | `rejouer-oracle.sh` code 0 (« tout a réussi ») ; host 7/7 ; empreintes mklepton identiques aux deux (50 lignes) ; 16/16 construits ; fumée `smoke.lsh` Passed (6 QEMU) ; banc an386 20/20, an386 soft 16/16, an500 19/19 ; `peripheriques` Passed dans les 4 an386 ; `comparer_R33-1` : 12 × 0, 4 F4 × 1, listes normalisées identiques à `attendu/` (172, 169, 172, 169 lignes) ; `f429→f439` code 1, `hors_debug=0` (embOS, FreeRTOS) ; trunk : 0 cassé, 0 régulier | conforme (`.noinit` : §4, §6) |
| C4 Compilation à blanc | `cmsis5` 0 échec (2 puces) ; `v330` 1 échec `stm32f4xx_ll_usb` (2 puces) ; trunk sans fichier régulier | code 1 (attendu) ; 90 sources par ligne ; `cmsis5` 0 échec (F429, F439) ; `v330` 1 échec `stm32f4xx_ll_usb` (F429, F439 : `__UNALIGNED_UINT32_READ`, `__UNALIGNED_UINT32_WRITE` non déclarés) ; 0 avertissement ; `core_cm4.h` : `cmsis/CMSIS/Include` (v330), `cmsis-5/CMSIS/Core/Include` (cmsis5) ; `resume.txt` identique à `env-34-hal-f4` hors en-tête ; trunk 0 régulier | conforme |
| C5 Fichiers générés | `$R` : `check`, `generate` 0, espace = `$R33` au chemin près ; `$P` : codes 0, générés, graine et `check` identiques | `$R` : codes 0 ; 23 `"request"`, 10 `"svdFile"`, 7 `"type": "lldb"`, 4 « tests des greffons » ; `diff=0` avec l'espace de `$R33` (régénéré au §5.1). `$P` : codes 0 avant et après ; empreintes identiques (`CMakeUserPresets.json` d5ee81e4…, `env11.code-workspace` b2c7b8a4…) ; graine propre avant et après ; sortie de `check` identique | conforme |
| C6 Nettoyage | `essais/env-33-debian` et `~/env-33-journaux` supprimés par l'utilisateur, taille relevée | 356 Mo et 16 Mo ; `rm -rf` lancé par l'utilisateur ; `ls -d` : absents ; `$U`, `$R`, `$P`, `$J` conservés | conforme |
| C7 Carte NUCLEO-F429ZI | sonde vue, droits sans sudo ; IP confirmée ; 3 `lepton.elf` reconfigurés = oracle ; `ctest -L board` 20/20 ; fumée `cortexM4-stm32f4` ; ping 3/3, LIST 13, RETR 57 octets identique, `ECONNRESET=15` | §5 ci-dessous : sonde seule, OpenOCD code 0 sans sudo ; IP 192.168.2.20 confirmée par l'utilisateur ; 3 × `oracle=0` (empreintes `.bin`/`.elf`/`.hex` identiques, 0 écart) ; 3 × `ctest=0`, 20/20 ; fumée `cortexM4-stm32f4` ; `board_net` : ping 3/3, FTP 220, LIST 13 entrées, RETR `/usr/etc/.boot` 57 octets identique, `ECONNRESET=15` ; trunk 0 régulier, 0 `__pycache__` | conforme |

Fumée QEMU (`qemu-mps2-an386-freertos/fumee.log`) : `uname -a` →
`lepton-cortexm4-32  4.10.0.2 Nov  5 2026-16:57:10 cortexM4-qemu-mps2-an386`.

## 3. Presets (§7)

| Preset | Construction | Fumée | Banc KAL | Symboles (R36-1 / R33-1 / Mac `env-35-apres`) | `comparer_R33-1` | `comparer_Mac` |
| --- | --- | --- | --- | --- | --- | --- |
| host | oui | — | ctest 7/7 | — | empreintes = `env-33-debian` = `env-35-apres` | — |
| qemu-mps2-an386-embos | oui | oui | 20/20 | 1599 / 1599 / 1583 | 0 | 1 |
| qemu-mps2-an386-embos-soft | oui | oui | 16/16 | 1596 / 1596 / 1580 | 0 | 1 |
| qemu-mps2-an386-freertos | oui | oui | 20/20 | 1639 / 1639 / 1623 | 0 | 1 |
| qemu-mps2-an386-freertos-soft | oui | oui | 16/16 | 1638 / 1638 / 1622 | 0 | 1 |
| qemu-mps2-an500-embos | oui | oui | 19/19 | 1561 / 1561 / 1545 | 0 | 1 |
| qemu-mps2-an500-freertos | oui | oui | 19/19 | 1601 / 1601 / 1585 | 0 | 1 |
| nucleo-f429zi-embos | oui | carte | carte 20/20 | 1768 / 1793 / 1752 | 1 | 1 |
| nucleo-f429zi-freertos | oui | carte | carte 20/20 | 1804 / 1833 / 1788 | 1 | 1 |
| nucleo-f439zi-embos | oui | carte | carte 20/20 | 1768 / 1793 / 1752 | 1 | 1 |
| nucleo-f439zi-freertos | oui | — | — | 1804 / 1833 / 1788 | 1 | 1 |
| nucleo-wl55jc1-embos | oui | — | — | 1230 / 1230 / 1215 | 0 | 1 |
| nucleo-wl55jc1-freertos | oui | — | — | 1276 / 1276 / 1261 | 0 | 1 |
| samd21-xplained-pro-embos | oui | — | — | 941 / 941 / 926 | 0 | 1 |
| samd21-xplained-pro-freertos | oui | — | — | 991 / 991 / 976 | 0 | 1 |
| stm32f746g-disco-embos | oui | — | — | 1640 / 1640 / 1624 | 0 | 1 |
| stm32f746g-disco-freertos | oui | — | — | 1676 / 1676 / 1660 | 0 | 1 |

`comparer_Mac` = 1 partout (informatif : chaînes différentes). Symboles F4 : −25 en embOS
(89 retirés, 64 ajoutés), −29 en FreeRTOS (89 retirés, 60 ajoutés), conformément aux listes
`attendu/<preset>.noms.txt`.

## 4. Deltas de sections des 4 presets F4 (R33-1 → R36-1, Debian contre Mac)

Identiques entre F429 et F439 (`f429→f439` hors `.debug_*` : 0).

| Section | embOS Debian | embOS Mac | FreeRTOS Debian | FreeRTOS Mac |
| --- | --- | --- | --- | --- |
| `.text` | 164840 → 166148 (+1308) | 159864 → 161204 (+1340) | 171692 → 172232 (+540) | 166580 → 167088 (+508) |
| `.data` | 1056 → 1116 (+60) | 1056 → 1116 (+60) | 1180 → 1240 (+60) | 1180 → 1240 (+60) |
| `.bss` | 98564 → 97300 (−1264) | 98568 → 97304 (−1264) | 98972 → 97708 (−1264) | 98976 → 97712 (−1264) |
| `.noinit` | inchangée | inchangée | **0 → 4** | **4 → 0** |
| `.ccm_bss` | 45256, inchangée | inchangée | 56408, inchangée | inchangée |

`.text`, `.data`, `.bss` : même signe qu'au Mac. `.noinit` (FreeRTOS) : signe inverse, voir §6.

## 5. Banc sur carte NUCLEO-F429ZI (§10)

| Élément | Valeur |
| --- | --- |
| Rattachement | par l'utilisateur (VMware Fusion) |
| Sonde | `lsusb` : `0483:374b STMicroelectronics ST-LINK/V2.1`, seule ; `/dev/serial/by-id/usb-STMicroelectronics_STM32_STLink_0672FF495252717267243842-if02` → `ttyACM0` |
| OpenOCD | `openocd-nucleo-f439zi.cfg` du BSP F429, `init; targets; shutdown` : code 0 sans sudo ; STLINK V2J27M15, 3,23 V, `[stm32f4x.cpu] Cortex-M4 r0p1` |
| Port | `/dev/ttyACM0`, `crw-rw----+ root:plugdev`, ACL `user:lepton-user:rw-` ; lisible et inscriptible |
| Droits | groupes `… sudo … plugdev …` (pas `dialout`, inutile ici : le port est au groupe `plugdev`) ; `60-openocd.rules` présente ; **aucune commande sudo** |
| Réseau | `ens37` 192.168.2.20/16 (masque /16 et non /24, couvre 192.168.2.0/24) ; `ip route get 192.168.2.5` → `dev ens37 src 192.168.2.20` ; ping de la carte avant banc 3/3 ; `ens33` 172.16.116.134/24 (non utilisée) |
| IP confirmée | 192.168.2.20, par l'utilisateur, avant tout flash |

| Image | `oracle` | `ctest -L board` | Fumée | Réseau (`board_net`) |
| --- | --- | --- | --- | --- |
| nucleo-f429zi-embos | 0 | 0, 20/20 | `cortexM4-stm32f4` | ping 3/3, FTP 220, LIST 13, RETR 57 o identique, `ECONNRESET=15` |
| nucleo-f429zi-freertos | 0 | 0, 20/20 | `cortexM4-stm32f4` | ping 3/3, FTP 220, LIST 13, RETR 57 o identique, `ECONNRESET=15` |
| nucleo-f439zi-embos | 0 | 0, 20/20 | `cortexM4-stm32f4` | ping 3/3, FTP 220, LIST 13, RETR 57 o identique, `ECONNRESET=15` |

Fumée sur carte (f429zi-embos) : `lepton-cortexm4-32  4.10.0.2 Nov  5 2026-16:57:57 cortexM4-stm32f4`.
Aucun test en échec, aucune relance. La carte garde l'image `nucleo-f439zi-embos` de la VM.
Journaux par image dans `oracles/env-36-debian/<P>/` : `carte-config.log`, `carte-oracle.txt`,
`carte.log`, `carte-detail.log`, `fumee-carte.log`, `reseau-carte.log`.

## 6. Écarts et constats

- **Comptage `cubemx` du §6.1 (défaut de la consigne, accepté par la session Mac) :** la commande
  compte `cubemx_hal_driver/` sur tout le trunk : `cubemx 157`, tous sous
  `dev/arch/cortexm/stm32wlxx/cubemx_hal_driver/` (famille WL, non touchée par ENV-34 ; 157 avant
  et après). Sous `stm32f4xx/cubemx_hal_driver/` : 0. Correctif retenu pour C2 : « 0 lien sous
  `stm32f4xx/cubemx_hal_driver/` ». Vérifié au Mac aux mêmes commits.
- **Liste des liens « avant » du §6.1 (écart de la session, accepté) :** relevée d'abord en chemins
  absolus (`find "$U"/trunk`) au lieu de `cd "$U"; find trunk`. Convertie en chemins relatifs par
  `sed "s#^$U/##" | LC_ALL=C sort` (original conservé : `6.1-liens-avant-absolu.txt`, 3957 lignes) ;
  ajouts et retraits calculés sur la liste convertie.
- **`.noinit` des presets F4 FreeRTOS, signe inverse du Mac : expliqué, à trancher au PA-60** (la
  session Mac propose de l'admettre). Debian 0 → 4, Mac 4 → 0. `.noinit` ne contient aucun
  symbole : ses 4 octets sont le bourrage de `. = ALIGN (0x8)` de `ld/common-cortexm.ld` ;
  `lepton.map` (f429zi-freertos, R36-1) :
  `.noinit 0x20018284 0x4` … `*fill* 0x20018284 0x4`. Le `.bss` Debian vaut le `.bss` Mac − 4 avant
  (98972 contre 98976) et après (97708 contre 97712) : le bourrage s'inverse. `.bss + .noinit`
  après ENV-35 = 97712 sur les deux hôtes (E-5 d'ENV-35).
- **Synthèse réseau du §10.2 (forme) :** le `grep 'ping|LIST|RETR|ECONNRESET'` de la consigne sur
  `reseau-carte.log` (copie de `board_net.log`, console série de la carte) ne trouve que
  `tsterrno: connect=-1 errno=15`. La ligne de synthèse `board_net : ping 3/3, …` est dans
  `carte-detail.log` (`LastTest.log`) ; relevée là.
- **Remise des messages (§2bis) :** premier envoi de l'`ACCUSÉ` en `ECONNRESET` ; renvoyé avec
  l'`AVANCEMENT` du §6.1, accepté par le serveur ; envois suivants acceptés.

## 7. Journal des messages (§2bis)

| ID | Date | Sens | Résumé |
| --- | --- | --- | --- |
| ORDRE R36-1 | 2026-11-05 | Mac → VM | consigne `env-36-debian.md` @ bd7ad59 ; PA-59, PA-11 (3 images), PA-P |
| ACCUSÉ R36-1 | 2026-11-05 | VM → Mac | §5 conforme, aucun écart visible — premier envoi en `ECONNRESET` |
| ACCUSÉ + AVANCEMENT R36-1 | 2026-11-05 | VM → Mac | renvoi de l'accusé ; §5.1 fait ; `graft-update` du §6.1 à l'utilisateur |
| AVANCEMENT R36-1 | 2026-11-05 | VM → Mac | §6 conforme (C2) ; écart `cubemx 157` (WL) ; liste avant convertie |
| AVANCEMENT R36-1 | 2026-11-05 | Mac → VM | `cubemx 157` = défaut de consigne ; conversion acceptée ; continuer |
| AVANCEMENT R36-1 | 2026-11-05 | VM → Mac | §7 conforme (C3) ; `.noinit` 0 → 4 (FreeRTOS F4) = bourrage |
| AVANCEMENT R36-1 | 2026-11-05 | Mac → VM | `.noinit` confirmé au Mac ; à consigner « expliqué, à trancher au PA-60 » |
| AVANCEMENT R36-1 | 2026-11-05 | VM → Mac | §8, §9 conformes (C4, C5) ; §11 et §10.1 à l'utilisateur |
| AVANCEMENT R36-1 | 2026-11-05 | VM → Mac | §11 fait (C6) ; §10.1 relevé ; IP 192.168.2.20 à confirmer |
| AVANCEMENT R36-1 | 2026-11-05 | VM → Mac | §10 conforme (C7) |

## 8. Non fait

- Presets de carte autres que les 3 du §10 : construits et capturés seulement, jamais flashés.
- Rattachement de la carte au Mac : non fait à la clôture (à la main de l'utilisateur).
- Push de `devenv/env-36-debian` : soumis à l'accord explicite de l'utilisateur (PA-P).
