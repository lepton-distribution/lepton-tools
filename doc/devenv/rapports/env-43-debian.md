# ENV-43 — Validation Debian groupée (ENV-37 à ENV-42) — 2026-11-09

Session VM `debian-linux-vm`, ordre `R43-1` de la session Mac `validation-debian-env-43`, consigne
`doc/devenv/consignes/env-43-debian.md` à f01e735. Journaux : `~/env-43-journaux/` sur la VM
(`0-messages-R43-1.md` pour les messages). Rootstock neuf `essais/env-43-debian` (`$R`), rootstock
regreffé `essais/env-28-debian` (`$U`), graine de projet `essais/env-11/qemu` (`$P`).

Résultat : C1 à C8 atteints. Un écart, sans incidence fonctionnelle : la taille de `.text` ne
varie pas sur Debian comme sur le Mac (§4). Deux écarts de procédure, l'un et l'autre décidés
par l'utilisateur : la session a lancé elle-même les installations du §6, et aucun message n'a pu
être remis à la session Mac (§6).

## 1. Hôte et versions (§5, §6)

| Élément | Valeur |
| --- | --- |
| Hôte | Debian 13.7, Linux 6.12.107+deb13-amd64 x86_64, `lepton-user`, git 2.47.3 |
| Espace libre | `/home` 18 Go |
| Chaîne APT | arm-none-eabi-gcc `15:14.2.rel1-1` (14.2.1 20241119), cmake 3.31.6, ninja 1.12.1, QEMU 10.0.13 (`1:10.0.13+ds-0+deb13u1`), Python 3.13.5, gcc 14.2.0, OpenOCD 0.12.0 : identique à R36-1 |
| embOS | `~/lepton/third_party/embos/cortexm-gcc/5.20.0.0` (`LEPTON_EMBOS_ROOT`) |
| scion | 0.5.4.0 → **0.6.1.0** (`install-debian.sh`, `SCION_REF` par défaut, `seed.scions.git@0.6.1.0`) ; `mirror-sync` connu |
| lepton | `lepton 0.1.0`, `scion 0.6.1.0 (requis ≥ 0.6.1.0)` (`pipx install --force`, depuis `devenv/env-43` propre) |
| VSCodium | 1.135.06055 ; `install-vscodium.sh` : 1re exécution `changements 1`, 2e `changements 0` |
| Extensions | `lepton-distribution.lepton@0.5.2`, `vadimcn.vscode-lldb@1.12.3`, `mcu-debug.rtos-views@0.0.16`, `mcu-debug.peripheral-viewer@1.6.4` |
| Clone noyau `$K` | propre, `master` b3a5415 → **763dda2** (avance rapide) |
| lepton-tools | `devenv/env-43` = `origin/devenv/env-43` = f01e735, propre (avant le `switch` : `devenv/env-36-debian`) |

`git ls-remote` : tous les commits du tableau du §1 de la consigne. scion 0.6.1.0 4502a70 ;
graine 15740f9 ; noyau 763dda2 ; famille-qemu-mps2 3954357 ; bsp-an386 5819047 ; bsp-an500
e98a482 ; famille-f4 7afd7f1 ; bsp-f429zi b9fe2bf ; bsp-f439zi 314f91b ; famille-wl 2340b25 ;
bsp-wl55jc1 ef51ec1 ; famille-f7 d2d9aa9 ; bsp-f746g 6266908 ; famille-samd21 a262e81 ;
bsp-samd21 f3cffa2 ; mirror-hal `v1.8.5` b6f0ed3 ; mirror-cmsis `master` 9192c7b.

État de `$U` avant la regreffe :
- graine à 15740f9, propre ; 14 entrées ;
- 13 clones sur `master`, amont `origin/master`, aucune modification, aux commits de la colonne
  « En R36-1 » ;
- 3978 liens, 0 cassé, 0 fichier régulier ; pas de `depots/tiers`.

Graines qui citent `stm32f4xx` : seulement les clones `original-tree` d'`env-28-debian`,
`env-13-debian` et `env-36-debian`. Aucune graine de projet.

## 2. Critères (§14)

| Critère | Résultat | Constat |
| --- | --- | --- |
| C1 Versions | **atteint** | ls-remote = §1 ; scion 0.6.1.0 par `install-debian.sh` ; lepton code 0, scion 0.6.1.0 accepté ; extension 0.5.2, 2e exécution `changements 0` ; chaîne APT = R36-1. Installations lancées par la session (accord de l'utilisateur, §6) |
| C2 `graft-update` et rootstock | **atteint** | `$U` : code 0, 0 conflit, graine inchangée ; 16 entrées ; noyau, BSP an386, familles F4 et WL avancés ; 2 clones tiers aux commits épinglés, `origin` = miroirs ; ajouts 4 = attendu, retraits 0 ; `CONFORME`. `$R` : 16 entrées, `CONFORME`, liste identique à `$U` |
| C3 Constructions | **atteint, avec un écart** | host 7/7 ; mklepton = `env-36-debian` = `env-42-apres` ; 16 presets construits ; fumée ×6 ; bancs 20/20, 16/16, 19/19 ; 6 presets hors M4 à 0 ; 10 M4 à 1, symboles = Mac ; `.text` seule section chargée changée ; `f429→f439` hors `.debug_*` 0. Écart : `.text` inchangée sur 5 presets, +64 sur 5 (§4) |
| C4 Contenu projeté, HAL à blanc | **atteint** | 206 projetés = HEAD, 0 écart de casse ni de contenu ; résumé = R36-1 (`cmsis5` 0 échec, `v330` 1 échec `stm32f4xx_ll_usb`) ; trunk sans fichier régulier |
| C5 Fichiers générés | **atteint** | `$R` : codes 0, 2 clés projetées, espace = `$R36` au chemin près ; `$U` : codes 0, espace = avant ; `$P` : générés, graine et `check` identiques |
| C6 Miroir | **atteint** | `mirror-sync --dry-run` code 0 ; 2 miroirs, 0 à envoyer, 0 signalement ; rien envoyé ; trunk `CONFORME` |
| C7 Carte NUCLEO-F429ZI | **atteint** | une seule sonde, droits sans sudo ; IP 192.168.2.20 confirmée par l'utilisateur ; 3 `lepton.elf` = oracle ; 20/20 ×3 ; fumée `cortexM4-stm32f4` ; ping 3/3, LIST 13, RETR 57 octets identique, `ECONNRESET=15` |
| C8 Nettoyage | **atteint** | `essais/env-36-debian` (360 Mo) et `~/env-36-journaux` (4,6 Mo) supprimés par l'utilisateur ; absents |

## 3. Presets (§8)

Fumée : `smoke.lsh` Passed dans les 6 `banc-kal.log` QEMU. `qemu-mps2-an386.peripheriques` Passed
dans les 4 `banc-kal.log` an386. Symboles : R43-1 = R36-1 partout ; le Mac `env-42-apres` en
compte 15 ou 16 de moins (chaîne différente, déjà le cas en R36-1).

| Preset | Construction | Fumée | Banc KAL | Symboles R43-1 / R36-1 / Mac | `comparer_R36-1` | `comparer_Mac` |
| --- | --- | --- | --- | --- | --- | --- |
| qemu-mps2-an386-embos | oui | oui | 20/20 | 1599 / 1599 / 1583 | 1 | 1 |
| qemu-mps2-an386-embos-soft | oui | oui | 16/16 | 1596 / 1596 / 1580 | 1 | 1 |
| qemu-mps2-an386-freertos | oui | oui | 20/20 | 1639 / 1639 / 1623 | 1 | 1 |
| qemu-mps2-an386-freertos-soft | oui | oui | 16/16 | 1638 / 1638 / 1622 | 1 | 1 |
| qemu-mps2-an500-embos | oui | oui | 19/19 | 1561 / 1561 / 1545 | 0 | 1 |
| qemu-mps2-an500-freertos | oui | oui | 19/19 | 1601 / 1601 / 1585 | 0 | 1 |
| nucleo-f429zi-embos | oui | carte | carte | 1768 / 1768 / 1752 | 1 | 1 |
| nucleo-f429zi-freertos | oui | carte | carte | 1804 / 1804 / 1788 | 1 | 1 |
| nucleo-f439zi-embos | oui | carte | carte | 1768 / 1768 / 1752 | 1 | 1 |
| nucleo-f439zi-freertos | oui | — | — | 1804 / 1804 / 1788 | 1 | 1 |
| nucleo-wl55jc1-embos | oui | — | — | 1230 / 1230 / 1215 | 1 | 1 |
| nucleo-wl55jc1-freertos | oui | — | — | 1276 / 1276 / 1261 | 1 | 1 |
| samd21-xplained-pro-embos | oui | — | — | 941 / 941 / 926 | 0 | 1 |
| samd21-xplained-pro-freertos | oui | — | — | 991 / 991 / 976 | 0 | 1 |
| stm32f746g-disco-embos | oui | — | — | 1640 / 1640 / 1624 | 0 | 1 |
| stm32f746g-disco-freertos | oui | — | — | 1676 / 1676 / 1660 | 0 | 1 |

Host : ctest 7/7 ; empreintes mklepton identiques à `env-36-debian` et à `env-42-apres`.
`f429→f439` : code 1, `hors_debug=0` pour embOS et FreeRTOS.

## 4. Deltas de `.text` des 10 presets M4 (R36-1 → R43-1, Debian contre Mac)

| Preset | `.text` Debian R36-1 → R43-1 | Δ Debian | Δ Mac (`env-35-apres` → `env-42-apres`) |
| --- | --- | --- | --- |
| qemu-mps2-an386-embos | 157612 → 157676 | **+64** | +16 |
| qemu-mps2-an386-embos-soft | 157308 → 157308 | **0** | +16 |
| qemu-mps2-an386-freertos | 164528 → 164528 | **0** | +16 |
| qemu-mps2-an386-freertos-soft | 164160 → 164160 | **0** | +16 |
| nucleo-wl55jc1-embos | 106376 → 106376 | **0** | +16 |
| nucleo-wl55jc1-freertos | 111952 → 111952 | **0** | +16 |
| nucleo-f429zi-embos | 166148 → 166212 | **+64** | +32 |
| nucleo-f429zi-freertos | 172232 → 172296 | **+64** | +48 |
| nucleo-f439zi-embos | 166148 → 166212 | **+64** | +32 |
| nucleo-f439zi-freertos | 172232 → 172296 | **+64** | +48 |

Aucun delta négatif. Aucune autre section chargée (`.data`, `.bss`, `.noinit`, `.ccm*`,
`.rodata`) ne change sur les 16 presets. Les lignes de symboles normalisées sont identiques à
`attendu/<preset>.noms.txt` dans les 10 presets. Ce sont les mêmes symboles qu'au Mac, et ils
grossissent de la même façon : `qemu_mps2_{eth,uart}_irq_enable` +8 chacun,
`HAL_NVIC_{Disable,Enable}IRQ` +12 / +4, etc.

Pour les 5 presets à Δ 0, `8.1-<preset>.noms.diff` contient la seule ligne
`1d0 < section modifié: .text` : la ligne est attendue, mais `comparer-oracle.py` ne la produit
pas côté Debian. Lecture probable, non vérifiée : avec la chaîne APT, l'alignement des fonctions
absorbe l'agrandissement (+16) sur ces images, et l'arrondit à +64 sur les autres. Écart à
trancher par la session Mac ; rien n'a été corrigé.

## 5. Contrôles du trunk (§7, `controler-trunk.py`)

Même sortie pour `$U` (§7.1), `$R` (§7.2) et `$R` après `mirror-sync` (§11) :

```
liste chemin -> cible : identique à l'attendu (3982 liens)
fichiers réguliers 0 []
liens cassés 0 []
projetés 206 ; nom non suivi au HEAD (casse) 0 [] ; contenu ≠ HEAD 0 []
depots/tiers/cmsis-device-f4/3c77349ce04c8af401454cc51f85ea9a50e34fc1 HEAD 3c77349ce04c8af401454cc51f85ea9a50e34fc1 origin https://github.com/lepton-distribution/mirror-cmsis_device_f4.git modifs 0 filtre blob:none
depots/tiers/stm32f4xx-hal-driver/v1.8.5 HEAD b6f0ed3829f3829eb358a2e7417d80bba1a42db7 origin https://github.com/lepton-distribution/mirror-stm32f4xx-hal-driver.git modifs 0 filtre blob:none
CONFORME
```

`$U` après `graft-update -v` (lancé par l'utilisateur ; code 0, aucune ligne de conflit ni de refus) :
- graine à 15740f9 ; 16 entrées ;
- 13 clones sur `master`, propres : original 763dda2, bsp-qemu-mps2-an386 5819047,
  family-stm32f4xx 7afd7f1, family-stm32wlxx 2340b25, les autres inchangés ;
- liens 3978 → 3982 : 4 ajouts = `attendu/liens-ajoutes.txt` (les 4 `LEPTON-PROVENANCE.md` de la
  famille WL), 0 retrait ;
- `projetes.txt` = attendu (206).

`$R` (`rootstock-install`, `seed-add`, `graft` : codes 0, « 3982 feuilles liées ») : clones aux
commits du §1 ; liste `chemin -> cible` identique à celle de `$U`.

Fichiers générés (§10) :
- `seed status` de `$R` et de `$U` : `stm32f4xx-hal-driver projection v1.8.5 … (projeté par
  stm32f4xx, 200 fichier(s))`, `cmsis-device-f4 projection 3c77349… (projeté par stm32f4xx,
  6 fichier(s))`, `trunk : aucun fichier régulier, aucun lien cassé` ;
- espace de `$R` : 23 `"request"`, 10 `"svdFile"`, 7 `"type": "lldb"`, 4 « tests des greffons »,
  0 `tiers` ; `diff=0` avec `$R36` au chemin près ;
- espace de `$U` : `diff=0` avec l'avant.

HAL F4 à blanc (§9) : code 1, attendu. Résumé identique à R36-1 :
- 90 sources par ligne, 0 avertissement ;
- STM32F429xx et STM32F439xx en `cmsis5` : 0 échec ;
- STM32F429xx et STM32F439xx en `v330` : 1 échec (`stm32f4xx_ll_usb`).

Copie dans `oracles/env-43-debian/compilation-a-blanc/resume.txt`.

## 6. Commande de miroir (§11)

`scion mirror-sync --dry-run -v` dans `$R` : code 0.
```
miroir https://github.com/lepton-distribution/mirror-stm32f4xx-hal-driver.git : 0 référence(s) à envoyer, 0 signalement(s)
miroir https://github.com/lepton-distribution/mirror-cmsis_device_f4.git : 0 référence(s) à envoyer, 0 signalement(s)
```
2 dépôts de travail sous `depots/.mirrors/github.com/lepton-distribution/`. Rien envoyé ; trunk
`CONFORME`.

## 7. Banc sur carte NUCLEO-F429ZI (§12)

§12.1 :
- La carte était déjà rattachée à la VM à l'arrivée au §12. Une seule sonde ST est visible
  (`0483:374b` ST-LINK/V2.1, n° 0672FF495252717267243842) → `/dev/ttyACM0`.
- Droits : `root:plugdev` et ACL `lepton-user:rw-` ; utilisateur dans `plugdev` ;
  `60-openocd.rules` présent.
- OpenOCD (`init; targets; shutdown`) : code 0 sans sudo ; STLINK V2J27M15, 3,23 V,
  `stm32f4x.cpu` Cortex-M4 r0p1.
- Réseau : `ens37` 192.168.2.20/16, route vers 192.168.2.5 par `ens37`. Ping de la carte 3/3
  avant le banc.
- `PORT=/dev/ttyACM0`, `HOSTIP=192.168.2.20` : adresse confirmée par l'utilisateur.

§12.2 :

| Image | oracle | ctest -L board | Fumée | Réseau |
| --- | --- | --- | --- | --- |
| nucleo-f429zi-embos | 0 | 0, 20/20 | `cortexM4-stm32f4` | ping 3/3, LIST 13 entrées, RETR `/usr/etc/.boot` 57 octets identique, `ECONNRESET=15` |
| nucleo-f429zi-freertos | 0 | 0, 20/20 | `cortexM4-stm32f4` | idem |
| nucleo-f439zi-embos | 0 | 0, 20/20 | `cortexM4-stm32f4` | idem |

Résultats identiques à R36-1, malgré les images changées (`.text` +64, §4). Trunk sans fichier
régulier ni `__pycache__`. La carte garde l'image `nucleo-f439zi-embos` construite sur la VM.
Après le banc, l'utilisateur l'a rattachée de nouveau au Mac (vérifié : plus de sonde ST ni de
`/dev/ttyACM*` sur la VM). Journaux : `oracles/env-43-debian/<preset>/carte*.log`, `fumee-carte.log`,
`reseau-carte.log`.

## 8. Écarts et constats

1. **`.text` (C3)** : voir §4. Sur 5 presets M4, Δ 0 (Mac +16) ; sur 5 autres, Δ +64
   (Mac +16, +32 ou +48). Les symboles changés sont identiques au Mac, aucun delta n'est négatif,
   et aucune autre section chargée ne change. Seule différence dans les `noms.diff` : la ligne
   `section modifié: .text`, absente pour les 5 presets à Δ 0.
2. **Procédure §6** : à la demande de l'utilisateur, la session a lancé elle-même les
   installations : `install-debian.sh` (sudo sans mot de passe), `pipx install --force`,
   `install-vscodium.sh` ×2.
3. **Procédure §7.1** : la session a tenté `scion graft-update -v` ; le classifieur de
   permissions l'a refusé (« Modify Shared Resources »). L'utilisateur l'a lancé avec la commande
   de la consigne.
4. **Relevé §7.1** : la session a pris `7.1-liens-avant.txt` en chemins absolus
   (`find "$U"/trunk`), au lieu de chemins relatifs (`cd "$U"; find trunk`). Il a été converti en
   relatif par `sed` (l'original est gardé : `7.1-liens-avant-absolus.txt`), puis comparé de
   nouveau. Les données ne changent pas.
5. **Communication** : l'`ACCUSÉ` a échoué deux fois (`read ECONNRESET`, « bridge ID is stale ») ;
   la session Mac n'apparaît pas dans `ListAgents`. L'utilisateur a demandé de poursuivre sans
   elle. Tous les messages sont consignés dans `~/env-43-journaux/0-messages-R43-1.md` (§9).
6. Le clone noyau `$K` était à b3a5415 avant le §6, et non à 2893297. Il est propre, et passé à
   763dda2 par avance rapide.
7. Il reste sur la VM `essais/env-13-debian`, dont la graine `original-tree` cite la famille F4.
   Il n'a pas été regreffé.

## 9. Journal des messages (§2bis)

| ID | Date | Sens | Résumé | Remis |
| --- | --- | --- | --- | --- |
| R43-1 ordre | 2026-11-09 | Mac → VM | consigne env-43-debian.md (texte complet) | oui |
| ACCUSÉ R43-1 | 2026-11-09 | VM → Mac | relevés du §5, aucun écart | **non** (ECONNRESET ×2) |
| AVANCEMENT R43-1 (§6) | 2026-11-09 | VM → Mac | C1 conforme | non (consigné) |
| AVANCEMENT R43-1 (§7) | 2026-11-09 | VM → Mac | C2 conforme, `graft-update` par l'utilisateur | non (consigné) |
| AVANCEMENT R43-1 (§8) | 2026-11-09 | VM → Mac | C3 avec l'écart `.text` | non (consigné) |
| AVANCEMENT R43-1 (§9-§11) | 2026-11-09 | VM → Mac | C4, C5, C6 conformes | non (consigné) |
| AVANCEMENT R43-1 (§12.1) | 2026-11-09 | VM → utilisateur | PORT et HOSTIP, confirmation obtenue | oui (utilisateur) |
| FIN-SUCCÈS R43-1 | 2026-11-09 | VM → « Démarrage de session » | critères C1-C8, écart `.text`, contenu de l'ACCUSÉ | envoyé, lecture non confirmée |

## 10. Non fait

- `ACCUSÉ` et `AVANCEMENT` non remis à la session Mac. Le `FIN-SUCCÈS`, qui reprend le contenu de
  l'`ACCUSÉ`, a été envoyé à « Démarrage de session » (Remote Control) : envoi réussi, lecture non
  confirmée.
- `nucleo-f439zi-freertos` et les autres presets de carte : construits, non flashés (hors PA-11).
- `devenv/env-43-debian` : poussée avec l'accord de l'utilisateur (PA-P).
