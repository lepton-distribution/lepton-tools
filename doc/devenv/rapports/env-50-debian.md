# ENV-50 — Validation Debian groupée (ENV-44 à ENV-49) — 2026-11-10

Session VM `debian-linux-vm`, ordre `R50-1` de la session Mac `lepton-tools-9d` (`ENV-50`),
consigne `doc/devenv/consignes/env-50-debian.md` à 42fc79e (inchangée jusqu'à 93e1aa6). Journaux :
`~/env-50-journaux/` sur la VM (`0-messages-R50-1.md` pour les messages). Rootstock neuf
`essais/env-50-debian` (`$R`), rootstocks regreffés `essais/env-28-debian` (`$U`) et
`essais/env-13-debian` (`$E13`), graine de projet `essais/env-11/qemu` (`$P`).

Résultat : C1 à C8 atteints. Deux incidents de banc, liés à une coupure internet signalée par
l'utilisateur pendant le §12 : le lien Ethernet de la F429 était coupé au premier passage
(`board.net` en échec ×3, réussi à la relance unique), puis les trois sondes ont été détachées de la
VM pendant le premier essai WL55 (rien flashé, essai 2 complet). Deux écarts de procédure : le §8
a tourné pendant l'attente du §7.3, et le §10 et le §11 pendant le §9.1 (§8 de ce rapport).

## 1. Hôte et versions (§5, §6)

| Élément | Valeur |
| --- | --- |
| Hôte | Debian 13.7, Linux 6.12.107+deb13-amd64 x86_64, `lepton-user`, git 2.47.3, 2 CPU, 3 Go |
| Espace libre | `/home` 17 Go |
| Chaîne APT | arm-none-eabi-gcc `15:14.2.rel1-1` (14.2.1 20241119), cmake 3.31.6, ninja 1.12.1, QEMU 10.0.13 (`1:10.0.13+ds-0+deb13u1`), Python 3.13.5, OpenOCD 0.12.0 : identique à R43-1 ; `install-debian.sh` : 0 paquet mis à jour ni installé |
| embOS | `~/lepton/third_party/embos/cortexm-gcc/5.20.0.0` (`LEPTON_EMBOS_ROOT`) |
| scion | 0.6.1.0 → **0.6.2.0** (`install-debian.sh`, `SCION_REF` par défaut, `seed.scions.git@0.6.2.0`) |
| lepton | `lepton 0.1.0`, `scion 0.6.2.0 (requis ≥ 0.6.2.0)` (`pipx install --force`, depuis `devenv/env-50` propre) |
| VSCodium | 1.135.06055 ; `install-vscodium.sh` : 1re exécution `changements 0`, 2e `changements 0` |
| Extensions | `lepton-distribution.lepton@0.5.2`, `vadimcn.vscode-lldb@1.12.3`, `mcu-debug.rtos-views@0.0.16`, `mcu-debug.peripheral-viewer@1.6.4` |
| Clone noyau `$K` | propre, `master` 763dda2 → **76f28bd** (avance rapide) ; `SCION_REF="${SCION_REF:-0.6.2.0}"` |
| lepton-tools | `devenv/env-50` = `origin/devenv/env-50` = 93e1aa6, propre (avant le `switch` : `devenv/env-43-debian`) ; `lepton/`, `scripts/`, `extension/`, `tests/`, `pyproject.toml` identiques à `origin/main` c985670 ; `SCION_MIN_VERSION = (0, 6, 2, 0)` |

Les quatre installations ont été lancées par l'utilisateur (codes 0).

`git ls-remote` : tous les commits du tableau du §1 de la consigne. scion `0.6.2.0` 213d2c0 ;
graine 15740f9 ; noyau 76f28bd ; famille-qemu-mps2 3954357 ; bsp-an386 10a8889 ; bsp-an500
e98a482 ; famille-f4 acdd24c ; bsp-f429zi b9fe2bf ; bsp-f439zi 314f91b ; famille-wl 9349be2 ;
bsp-wl55jc1 4d7cf80 ; famille-f7 12280a5 ; bsp-f746g 6266908 ; famille-samd21 a262e81 ;
bsp-samd21 f3cffa2 ; mirror-stm32f4xx-hal-driver `v1.8.5` b6f0ed3 ; mirror-stm32f7xx-hal-driver
`v1.3.3` e1446fa ; mirror-cmsis_device_f7 `v1.2.10` 2352e88 ; mirror-stm32wlxx-hal-driver `v1.6.0`
5c87cf0 ; mirror-cmsis-device-wl `v1.4.0` 71a0b78 ; mirror-stm32-mw-subghz-phy `v1.5.0` 7dc059f ;
mirror-STM32CubeWL `v1.6.0` f934cd2 ; mirror-cmsis_device_f4 `master` 9192c7b (épinglé 3c77349).

État de départ :
- `$U` : graine 15740f9 propre ; 16 entrées ; 13 clones sur `master`, amont `origin/master`,
  0 modification, aux commits « En R43-1 » ; 3982 liens, 0 cassé, 0 régulier ; 2 clones tiers.
- `$E13` : graine 0f1275a (ancêtre de 15740f9), propre, sur `original-tree` ; 9 entrées ; 8 clones
  sur `master`, amont `origin/master`, 0 modification (original 16a331b, bsp-nucleo-f429zi 8ea7ee5,
  bsp-nucleo-wl55jc1 a329f4d, bsp-qemu-mps2-an386 046779e, bsp-qemu-mps2-an500 e98a482,
  family-qemu-mps2 3954357, family-stm32f4xx 01b5528, family-stm32wlxx 1eccc2f) ; 4011 liens,
  0 cassé, 0 régulier ; aucun clone tiers.
- `$R43`, son espace, `$P` et sa graine `env11`, `~/env-43-journaux` présents ; `$R` absent ;
  `venv-test` présent.
- Graines qui citent F4, F7 ou WL : seulement les clones `original-tree` de `$U`, `$R43` et `$E13`.

§5.1 : `generate` de `$P`, `$R43` et `$U` codes 0 ; `check` de `$P` 0 ; `check` de `$E13` 0.

## 2. Critères (§14)

| Critère | Résultat | Constat |
| --- | --- | --- |
| C1 Versions | **atteint** | ls-remote = §1 ; scion 0.6.2.0 par `install-debian.sh` (défaut `SCION_REF`) ; lepton `pipx` code 0, scion 0.6.2.0 accepté ; extension 0.5.2, 2e exécution `changements 0` ; chaîne APT = R43-1 |
| C2 `graft-update` et rootstock | **atteint** | `$U` : code 0, 0 conflit, graine inchangée ; 6 clones avancés ; 6 clones tiers créés depuis les miroirs aux commits épinglés ; ajouts 11 et retraits 104 = attendu ; `CONFORME` (3889 liens, 0 cassé, 0 régulier, 629 projetés = HEAD) ; 23 entrées. `$R` : 23 entrées, `CONFORME`, liste identique à `$U` |
| C3 Constructions | **atteint** | host 7/7 ; mklepton = `env-43-debian` = `env-49-apres` ; 16 presets construits ; fumée ×6 ; bancs 20/20, 16/16, 19/19 ; 10 presets à 0 ; an386 ×4 `hors_debug=0` ; WL55 ×2 symboles = Mac, `code_symboles +36`, `.text` +64 / +0, aucune autre section chargée changée ; `f429→f439` hors `.debug_*` 0 |
| C4 `essais/env-13-debian` (D8) | **atteint** | `graft-update` par l'utilisateur code 0, 0 conflit ; graine 0f1275a → 15740f9 ; 23 entrées ; `CONFORME` ; `lepton check` code 0 |
| C5 Hook, scripts, fichiers générés | **atteint** | pytest 377 passed (hook 118) ; compilation à blanc code 0, résumé = Mac hors ligne du compilateur ; `$R` : codes 0, 9 clés projetées, espace = `$R43` au chemin près ; `$U` : codes 0, espace = avant ; `$P` : générés, graine et `check` identiques |
| C6 Miroir | **atteint** | `mirror-sync --dry-run` code 0 ; 8 miroirs, 0 à envoyer, 0 signalement ; rien envoyé ; trunk `CONFORME` |
| C7 Cartes, sonde par numéro | **atteint, après relance** | 3 sondes, chacune choisie par son numéro, droits sans sudo ; numéro faux refusé ; ports et IP confirmés par l'utilisateur ; 5 `lepton.elf` = oracle ; F429 : 19/20 ×3, puis `board.net` relancé une fois ×3 : réussi (ping 3/3, LIST 13, RETR 57 octets identique, `ECONNRESET=15`) ; fumée `cortexM4-stm32f4` ; WL55 : 16/16 ×2 (essai 2), fumée `cortexM4-stm32wlxx`, radio 20/20 dans les deux sens et en ping-pong ; seule la sonde demandée est utilisée |
| C8 Nettoyage | **atteint** | `essais/env-43-debian` (392 Mo) et `~/env-43-journaux` (7,3 Mo) supprimés par l'utilisateur ; absents. Conservés : `$U`, `$E13`, `$R`, `$P`, `$J`, `~/tmp-pytest` |

## 3. Presets (§8)

`rejouer-oracle.sh` : code 0, « tout a réussi ». Fumée : `smoke.lsh` Passed dans les 6
`banc-kal.log` QEMU. `qemu-mps2-an386.peripheriques` Passed dans les 4 `banc-kal.log` an386.
Symboles : R50-1 = R43-1 partout sauf la WL55 (2 ajoutés, 3 retirés) ; le Mac `env-49-apres` en
compte 15 ou 16 de moins (chaîne différente, déjà le cas en R43-1).

| Preset | Construction | Fumée | Banc KAL | Symboles R50-1 / R43-1 / Mac | `comparer_R43-1` | `comparer_Mac` | `code_symboles` | `.text` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| qemu-mps2-an386-embos | oui | oui | 20/20 | 1599 / 1599 / 1583 | 1 (`.debug_*`) | 1 | +0 | +0 |
| qemu-mps2-an386-embos-soft | oui | oui | 16/16 | 1596 / 1596 / 1580 | 1 (`.debug_*`) | 1 | +0 | +0 |
| qemu-mps2-an386-freertos | oui | oui | 20/20 | 1639 / 1639 / 1623 | 1 (`.debug_*`) | 1 | +0 | +0 |
| qemu-mps2-an386-freertos-soft | oui | oui | 16/16 | 1638 / 1638 / 1622 | 1 (`.debug_*`) | 1 | +0 | +0 |
| qemu-mps2-an500-embos | oui | oui | 19/19 | 1561 / 1561 / 1545 | 0 | 1 | +0 | +0 |
| qemu-mps2-an500-freertos | oui | oui | 19/19 | 1601 / 1601 / 1585 | 0 | 1 | +0 | +0 |
| nucleo-f429zi-embos | oui | carte | carte | 1768 / 1768 / 1752 | 0 | 1 | +0 | +0 |
| nucleo-f429zi-freertos | oui | carte | carte | 1804 / 1804 / 1788 | 0 | 1 | +0 | +0 |
| nucleo-f439zi-embos | oui | carte | carte | 1768 / 1768 / 1752 | 0 | 1 | +0 | +0 |
| nucleo-f439zi-freertos | oui | — | — | 1804 / 1804 / 1788 | 0 | 1 | +0 | +0 |
| nucleo-wl55jc1-embos | oui | carte | carte | 1229 / 1230 / 1214 | 1 | 1 | **+36** | **+64** (106376 → 106440) |
| nucleo-wl55jc1-freertos | oui | carte | carte | 1275 / 1276 / 1260 | 1 | 1 | **+36** | **+0** (111952) |
| samd21-xplained-pro-embos | oui | — | — | 941 / 941 / 926 | 0 | 1 | +0 | +0 |
| samd21-xplained-pro-freertos | oui | — | — | 991 / 991 / 976 | 0 | 1 | +0 | +0 |
| stm32f746g-disco-embos | oui | — | — | 1640 / 1640 / 1624 | 0 | 1 | +0 | +0 |
| stm32f746g-disco-freertos | oui | — | — | 1676 / 1676 / 1660 | 0 | 1 | +0 | +0 |

Host : ctest 7/7 ; empreintes mklepton identiques à `env-43-debian` et à `env-49-apres`.

an386 ×4 (D5 d'ENV-44) : `hors_debug=0`, seules des sections `.debug_*` changent.

WL55 ×2 (ENV-49) : les lignes de symboles normalisées sont identiques à
`attendu/<preset>.noms.txt` (26 lignes : 2 ajoutés, 3 retirés, 21 modifiés). `code_symboles +36`,
comme au Mac. `.text` : +64 en embOS et 0 en FreeRTOS, au lieu de +48 au Mac. C'est le bourrage
d'alignement par pas de 64 octets de la chaîne APT (E-1, PA-74). Seule ligne de section hors
`.debug_*` : `section modifié : .text ['106376'] -> ['106440']` (embOS). Aucune autre section
chargée ne change, et aucun delta n'est négatif.

`f429→f439` : code 1, `hors_debug=0` pour embOS et FreeRTOS.

## 4. Contrôles du trunk (§7, `controler-trunk.py`)

Même sortie pour `$U` (§7.1), `$R` (§7.2), `$E13` (§7.3) et `$R` après `mirror-sync` (§11) :

```
liste chemin -> cible : identique à l'attendu (3889 liens)
fichiers réguliers 0 []
liens cassés 0 []
projetés 629 ; nom non suivi au HEAD (casse) 0 [] ; contenu ≠ HEAD 0 []
depots/tiers/cmsis-device-f4/3c77349ce04c8af401454cc51f85ea9a50e34fc1 HEAD 3c77349ce04c8af401454cc51f85ea9a50e34fc1 origin https://github.com/lepton-distribution/mirror-cmsis_device_f4.git modifs 0 filtre blob:none
depots/tiers/cmsis-device-f7/v1.2.10 HEAD 2352e888e821aa0f4fe549bd5ea81d29c67a3222 origin https://github.com/lepton-distribution/mirror-cmsis_device_f7.git modifs 0 filtre blob:none
depots/tiers/cmsis-device-wl/v1.4.0 HEAD 71a0b7860e700f7ca11afe4c4afd6cef684ad9bb origin https://github.com/lepton-distribution/mirror-cmsis-device-wl.git modifs 0 filtre blob:none
depots/tiers/stm32-mw-subghz-phy/v1.5.0 HEAD 7dc059f353f359ec65c60a0549d53c1ebeaafa79 origin https://github.com/lepton-distribution/mirror-stm32-mw-subghz-phy.git modifs 0 filtre blob:none
depots/tiers/stm32cubewl/v1.6.0 HEAD f934cd298bf82d45f96aac2f335c0bbd26d0b946 origin https://github.com/lepton-distribution/mirror-STM32CubeWL.git modifs 0 filtre blob:none
depots/tiers/stm32f4xx-hal-driver/v1.8.5 HEAD b6f0ed3829f3829eb358a2e7417d80bba1a42db7 origin https://github.com/lepton-distribution/mirror-stm32f4xx-hal-driver.git modifs 0 filtre blob:none
depots/tiers/stm32f7xx-hal-driver/v1.3.3 HEAD e1446fa12ffda80ea1016faf349e45b2047fff12 origin https://github.com/lepton-distribution/mirror-stm32f7xx-hal-driver.git modifs 0 filtre blob:none
depots/tiers/stm32wlxx-hal-driver/v1.6.0 HEAD 5c87cf00992c6e4ecf56c7c129b8dcfc6aa6f88e origin https://github.com/lepton-distribution/mirror-stm32wlxx-hal-driver.git modifs 0 filtre blob:none
CONFORME
```

Les liens vers `depots/tiers/` sont suivis par git au HEAD sous la même casse (0 écart de nom) :
les renommages `Inc` → `inc` et `Src` → `src` du WL sont établis sur un système de fichiers qui
distingue la casse.

`$U` après `graft-update -v` (lancé par l'utilisateur ; code 0, aucune ligne de conflit, de refus
ni de chemin ignoré) :
- graine à 15740f9 ; 23 entrées ;
- 6 clones avancés : original 763dda2 → 76f28bd, bsp-qemu-mps2-an386 5819047 → 10a8889,
  family-stm32f4xx 7afd7f1 → acdd24c, family-stm32wlxx 2340b25 → 9349be2,
  bsp-nucleo-wl55jc1 ef51ec1 → 4d7cf80, family-stm32f7xx d2d9aa9 → 12280a5 ; 13 clones sur
  `master`, propres ;
- 6 clones tiers créés (`git clone --filter=blob:none --no-checkout` depuis les miroirs) :
  `stm32wlxx-hal-driver/v1.6.0`, `cmsis-device-wl/v1.4.0`, `stm32-mw-subghz-phy/v1.5.0`,
  `stm32cubewl/v1.6.0`, `stm32f7xx-hal-driver/v1.3.3`, `cmsis-device-f7/v1.2.10` ;
- liens 3982 → 3889 : 11 ajouts = `attendu/liens-ajoutes.txt`, 104 retraits =
  `attendu/liens-retires.txt` ; `projetes.txt` = attendu (629).

`$R` (`rootstock-install`, `seed-add`, `graft` : codes 0, « 3889 feuilles liées ») : 23 entrées ;
clones aux commits du §1 ; 8 clones tiers ; liste `chemin -> cible` identique à celle de `$U`.

`$E13` après `graft-update -v` (lancé par l'utilisateur ; code 0, aucune ligne de conflit, de refus
ni de chemin ignoré) :
- graine avancée 0f1275a → 15740f9 ; 23 entrées ;
- 6 clones avancés : original 16a331b → 76f28bd, bsp-qemu-mps2-an386 046779e → 10a8889,
  family-stm32f4xx 01b5528 → acdd24c, bsp-nucleo-f429zi 8ea7ee5 → b9fe2bf,
  family-stm32wlxx 1eccc2f → 9349be2, bsp-nucleo-wl55jc1 a329f4d → 4d7cf80 ;
- 5 greffons clonés : bsp-nucleo-f439zi, family-stm32f7xx, bsp-stm32f746g-disco, family-samd21,
  bsp-samd21-xplained-pro ; 13 clones sur `master`, propres, aux commits du §1 ;
- 8 clones tiers créés ; liens 4011 → 3889 ; liste identique à celle de `$U` ;
- `lepton check` code 0 (« 19 fichier(s) conforme(s) », graine de référence) ; `generate` code 0.

## 5. Hook, scripts d'ENV-44, fichiers générés (§9, §10)

pytest (`venv-test`, Python 3.13.5, pytest 9.1.1, lepton 0.1.0 éditable depuis `$T`,
`TMPDIR=~/tmp-pytest`) :
- suite complète : code 0, **377 passed** en 2 min 42 s, aucun test ignoré ni en échec ;
- `tests/test_proteger_trunk.py` : **118 passed** ;
- lepton-tools propre hors `oracles/env-50-debian/`.

HAL F4 à blanc (`compiler-hal-f4-a-blanc.sh`) : **code 0**. Résumé identique à celui du Mac hors la
ligne du compilateur :
- STM32F429xx et STM32F439xx en `cmsis5` : 90 sources, 0 échec, 0 avertissement ;
- `core_cm4.h` = `kernel/core/ucore/cmsis-5/CMSIS/Core/Include/core_cm4.h` ;
- plus aucune ligne `v330`.

Copie dans `oracles/env-50-debian/compilation-a-blanc/resume.txt`. Trunk sans fichier régulier.

Fichiers générés :
- `$R` : `check`, `generate`, `seed status` codes 0. `seed status` montre 9 lignes `projection`
  aux versions du §1 et HEAD épinglés : `stm32f4xx-hal-driver` 200, `cmsis-device-f4` 6,
  `stm32wlxx-hal-driver` 157, `cmsis-device-wl` 6, `stm32-mw-subghz-phy` 20,
  `stm32cubewl::utilities` 38, `stm32cubewl::radio-core-inc` 1, `stm32f7xx-hal-driver` 196,
  `cmsis-device-f7` 5. Il donne aussi `trunk : aucun fichier régulier, aucun lien cassé`.
- Espace de `$R` : 23 `"request"`, 10 `"svdFile"`, 7 `"type": "lldb"`, 4 « tests des greffons »,
  0 `tiers` ; `diff=0` avec `$R43` au chemin près.
- `$U` : codes 0 ; mêmes 9 projections ; espace `diff=0` avec l'avant.
- `$P` : `generate` et `check` codes 0 ; générés (`CMakeUserPresets.json` d5ee81e4…,
  `env11.code-workspace` b2c7b8a4…), graine et sortie de `check` identiques à l'avant.

## 6. Commande de miroir (§11)

`scion mirror-sync --dry-run -v` dans `$R` : code 0.
```
miroir https://github.com/lepton-distribution/mirror-stm32f4xx-hal-driver.git : 0 référence(s) à envoyer, 0 signalement(s)
miroir https://github.com/lepton-distribution/mirror-cmsis_device_f4.git : 0 référence(s) à envoyer, 0 signalement(s)
miroir https://github.com/lepton-distribution/mirror-stm32wlxx-hal-driver.git : 0 référence(s) à envoyer, 0 signalement(s)
miroir https://github.com/lepton-distribution/mirror-cmsis-device-wl.git : 0 référence(s) à envoyer, 0 signalement(s)
miroir https://github.com/lepton-distribution/mirror-stm32-mw-subghz-phy.git : 0 référence(s) à envoyer, 0 signalement(s)
miroir https://github.com/lepton-distribution/mirror-STM32CubeWL.git : 0 référence(s) à envoyer, 0 signalement(s)
miroir https://github.com/lepton-distribution/mirror-stm32f7xx-hal-driver.git : 0 référence(s) à envoyer, 0 signalement(s)
miroir https://github.com/lepton-distribution/mirror-cmsis_device_f7.git : 0 référence(s) à envoyer, 0 signalement(s)
```
8 dépôts de travail sous `depots/.mirrors/github.com/lepton-distribution/` (78 Mo). Rien envoyé ;
trunk `CONFORME`.

## 7. Banc sur cartes, sonde choisie par numéro (§12)

§12.1 (19:29) :
- Les 3 cartes étaient déjà rattachées à la VM à l'arrivée au §12.1. Trois sondes ST :
  `0483:374b` ST-LINK/V2.1 n° 0672FF… → `/dev/ttyACM0` ; `0483:374e` STLINK-V3 n° 0027… →
  `/dev/ttyACM1` ; `0483:374e` STLINK-V3 n° 004F… → `/dev/ttyACM2`. Chacune est nommée par son
  numéro sous `/dev/serial/by-id/`.
- Droits : `root:plugdev` et ACL `lepton-user:rw-` sur les 3 ports ; utilisateur dans `plugdev` ;
  `60-openocd.rules` présent.
- OpenOCD (`adapter serial <n°>`, `init; targets; shutdown`) : codes 0 sans sudo. F429 : STLINK
  V2J27M15, 3,23 V, `stm32f4x.cpu` Cortex-M4 r0p1. WL55 A et B : STLINK V3J7M3, 3,28 V et 3,27 V,
  `stm32wlx.cpu0` Cortex-M4 r0p1. Numéro faux : code 1, « No device matches the serial string »,
  `Error: open failed`.
- Réseau : `ens37` 192.168.2.20/16, route vers 192.168.2.5 par `ens37`. Ping de la carte 0/3
  (« Destination Host Unreachable », voisin ARP `FAILED`).
- Ports (`/dev/serial/by-id/usb-STMicroelectronics_STM32_STLink_0672FF495252717267243842-if02`,
  `…STLINK-V3_002700253431510837393937-if02`, `…STLINK-V3_004F003E3431510937393937-if02`) et
  `HOSTIP=192.168.2.20` confirmés par l'utilisateur.

§12.2, NUCLEO-F429ZI :

| Image | oracle | ctest -L board (19:31-19:35) | Relance `board.net` (19:48-19:50) | Fumée |
| --- | --- | --- | --- | --- |
| nucleo-f429zi-embos | 0 | 8, 19/20 : `board.net` en échec, ping 0/3 | 0, 2/2 : ping 3/3, LIST 13 entrées, RETR `/usr/etc/.boot` 57 octets identique, `ECONNRESET=15` | `cortexM4-stm32f4` |
| nucleo-f429zi-freertos | 0 | 8, 19/20 : `board.net` en échec, ping 0/3 | 0, 2/2 : idem | `cortexM4-stm32f4` |
| nucleo-f439zi-embos | 0 | 8, 19/20 : `board.net` en échec, ping 0/3 | 0, 2/2 : idem | `cortexM4-stm32f4` |

- cfg générées `openocd-nucleo-f429zi.cfg` (ou `openocd-nucleo-f439zi.cfg`) avec
  `adapter serial 0672FF495252717267243842` ; « Lepton : sonde demandée 0672FF… » 18 fois par image
  au premier passage, jamais un autre numéro.
- Banc KAL sur carte (`kal.board_flash`, T1 à T8, T1F, T4F, T6F, T7F, TICI, TCLK, TSBRK, IRQ,
  `harness_fail`) : Passed sur les 3 images.
- Relance : `ctest --preset <P> -R '^board\.net$'`, qui tire `board.smoke_lsh` en dépendance et
  reflashe l'image. Elle a été faite après la vérification du câble par l'utilisateur. Journaux :
  `carte-relance-board-net.log`, `carte-detail-relance-board-net.log`, `reseau-carte-relance.log`.

§12.3, paire NUCLEO-WL55JC1 :
- Essai 1 (19:45) : configuration code 0, oracle=0 pour les 2 images, puis ctest 0/16. `board.smoke_lsh`
  et `nucleo-wl55jc1.radio` sont en échec (`FileNotFoundError` sur le port de A) ; les 14 autres
  tests ne sont pas lancés. Les 3 sondes avaient disparu de la VM (`lsusb`, `/dev/ttyACM*` absents à
  19:45:50). `smoke_lsh.py` ouvre le port avant la commande de flash : rien n'a été flashé.
  Journaux : `carte-essai1.log`, `carte-detail-essai1.log`.
- Rattachement par l'utilisateur : F429 à 19:47 (`/dev/ttyACM0`), puis A et B à 19:49
  (`/dev/ttyACM1`, `/dev/ttyACM2`), sur les mêmes ports `by-id` que ceux confirmés. OpenOCD par
  numéro : codes 0.
- Essai 2 (19:50-19:54) :

| Image | oracle | ctest -L board | Fumée | Radio |
| --- | --- | --- | --- | --- |
| nucleo-wl55jc1-embos | 0 | 0, 16/16 | `cortexM4-stm32wlxx` | A→B et B→A : `emis=20/20`, `recus=20/20 perdus=0 desordre=0 doublons=0` ; `ping : reponses=20/20 perdues=0`, `pong : reponses=20/20` ; 2 jetons |
| nucleo-wl55jc1-freertos | 0 | 0, 16/16 | `cortexM4-stm32wlxx` | idem |

- cfg générées `openocd-nucleo-wl55jc1.cfg` (`adapter serial 0027…`) et
  `openocd-nucleo-wl55jc1-paire.cfg` (`adapter serial 004F…`).
- « Lepton : sonde demandée » ne cite que 002700253431510837393937 (14 fois par image, comme au Mac).
- 16 tests : `board.smoke_lsh`, `kal.board_flash`, 13 tests KAL, `nucleo-wl55jc1.radio`.

Trunk sans fichier régulier ni `__pycache__`. Les cartes gardent les dernières images de la VM :
`nucleo-f439zi-embos` sur la F429, `nucleo-wl55jc1-freertos` sur A et B. Elles restent rattachées à
la VM. Les autres presets de carte ont été construits, jamais flashés.

## 8. Écarts et constats

1. **Lien Ethernet de la F429 (C7)** : `board.net` en échec sur les 3 images au premier passage
   (ping 0/3, ARP non résolu), déjà 0/3 au relevé du §12.1 avant tout flash. L'utilisateur a signalé
   une coupure internet pendant la session et a vérifié le câble. La relance unique de `board.net`
   a réussi ×3. Lecture probable, non vérifiée côté Mac : le pont VMware de `ens37` ou le lien de la
   carte était coupé pendant la panne. Rien n'a été corrigé côté VM.
2. **Sondes détachées (C7)** : entre 19:35 et 19:45, les 3 sondes ont disparu de la VM ; le premier
   essai WL55 a échoué à l'ouverture du port, sans flash. Après le rattachement par l'utilisateur,
   l'essai 2 a été complet. Même cause probable que le point 1.
3. **Ordre (procédure)** : le §8 (`rejouer-oracle` sur `$R`) a tourné pendant l'attente du
   `graft-update` de `$E13` (§7.3) ; il ne touche ni `$E13` ni `$U`. Le §10 et le §11 ont été faits
   pendant le pytest du §9.1, le §9.2 après. Les attendus ne dépendent pas de cet ordre. L'espace de
   `$R43` a été copié au §5.1, et le §10.1 a précédé le §13.
4. **`lepton-env.sh` (§12.2)** : le premier `source` a été lancé depuis un répertoire hors rootstock
   (« lepton-env: aucun rootstock scion au-dessus de … »). Les constructions ont `-S "$R/trunk"`
   explicite et sont égales à l'oracle (`oracle=0`). Aux §12.2 (relance) et §12.3, `cd "$R"`
   précède le `source`. La consigne pourrait le préciser.
5. **Trace de sonde à la relance** : « Lepton : sonde demandée » n'apparaît pas dans
   `carte-detail-relance-board-net.log` (0 ligne) ; la cfg générée porte
   `adapter serial 0672FF495252717267243842` et une seule sonde F4 est branchée.
6. **`.text` WL55 (C3, attendu)** : +64 (embOS) et 0 (FreeRTOS) contre +48 au Mac ; `code_symboles +36`
   des deux côtés (E-1, PA-74).
7. **Communication** : tous les envois ont reçu `success` du bridge. À partir du 3e, l'outil
   indique « accepted by the server … delivery is not confirmed » (la session `ENV-50` n'a pas
   déclaré pouvoir recevoir de messages). Aucun envoi n'a été en erreur, la règle D9 ne s'est donc
   pas appliquée. Aucune réponse de la session Mac n'a été reçue après l'ordre.

## 9. Journal des messages (§2bis)

| ID | Date | Sens | Résumé | Remis |
| --- | --- | --- | --- | --- |
| ORDRE R50-1 | 2026-11-10 | Mac → VM | consigne env-50-debian.md (texte complet) | oui |
| ACCUSÉ R50-1 | 2026-11-10 | VM → Mac | relevés du §5, aucun écart | oui |
| AVANCEMENT R50-1 (§5.1, §6) | 2026-11-10 | VM → Mac | attente des installations | oui |
| AVANCEMENT R50-1 (§6, §7.1) | 2026-11-10 | VM → Mac | C1 conforme, attente du `graft-update` de `$U` | accepté, non confirmé |
| AVANCEMENT R50-1 (§7.1, §7.2) | 2026-11-10 | VM → Mac | C2 conforme, attente du `graft-update` de `$E13`, §8 lancé | accepté, non confirmé |
| AVANCEMENT R50-1 (§7.3) | 2026-11-10 | VM → Mac | C4 conforme | accepté, non confirmé |
| AVANCEMENT R50-1 (§8) | 2026-11-10 | VM → Mac | C3 conforme | accepté, non confirmé |
| AVANCEMENT R50-1 (§9-§11) | 2026-11-10 | VM → Mac | C5, C6 conformes | accepté, non confirmé |
| AVANCEMENT R50-1 (§12.1) | 2026-11-10 | VM → Mac | ports et IP relevés | accepté, non confirmé |
| AVANCEMENT R50-1 (§12.1) | 2026-11-10 | VM → utilisateur | ports et IP confirmés | oui (utilisateur) |
| AVANCEMENT R50-1 (§12.2) | 2026-11-10 | VM → Mac | `board.net` en échec ×3 | accepté, non confirmé |
| AVANCEMENT R50-1 (§12.3) | 2026-11-10 | VM → Mac | arrêt, sondes détachées | accepté, non confirmé |
| AVANCEMENT R50-1 (§12.2) | 2026-11-10 | VM → Mac | relance `board.net` réussie ×3 | accepté, non confirmé |
| AVANCEMENT R50-1 (§12, §13) | 2026-11-10 | VM → Mac | C7 atteint, attente du `rm -rf` | accepté, non confirmé |
| QUESTION R50-1 (push) | 2026-11-10 | VM → utilisateur | push de `devenv/env-50-debian` (PA-P) | oui (utilisateur) |

## 10. Non fait

- `nucleo-f439zi-freertos`, `samd21-xplained-pro-*`, `stm32f746g-disco-*` : construits, non flashés
  (hors PA-11).
- Push de `devenv/env-50-debian` : soumis à l'accord de l'utilisateur (PA-P).
- Cartes non rattachées de nouveau au Mac : laissé à l'utilisateur.
- `~/tmp-pytest` conservé (à vider par l'utilisateur s'il le souhaite).
