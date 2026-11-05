# ENV-36 — Validation Debian groupée (ENV-34 et ENV-35) — rapport de la session Mac

Session Mac `validate-env-34-35-debian`, 2026-11-05. Branche lepton-tools `devenv/env-36` (depuis
`main` 06cb55d). Consigne VM : `consignes/env-36-debian.md`.

## 1. Préparation (tâche 1)

### 1.1 Écarts Mac `env-32-apres` → `env-35-apres`

`comparer-oracle.py` par preset (`env-32-apres` = binaires de référence de R33-1 au Mac ;
`env-35-apres` = nouvelle référence d'ENV-35) :

| Preset | Code | Écarts (hors empreintes) |
| --- | --- | --- |
| host | — | `mklepton-empreintes.sha256` identique (pas d'`empreintes.txt` pour host : code 2 du comparateur, attendu) |
| 12 presets hors F4 (an386 ×4, an500 ×2, WL55 ×2, SAMD21 ×2, F746 ×2) | 0 | aucun |
| `nucleo-f429zi-embos`, `nucleo-f439zi-embos` | 1 | 89 symboles retirés, 64 ajoutés, 16 modifiés ; `.text` 159864 → 161204 (+1340), `.data` 1056 → 1116 (+60), `.bss` 98568 → 97304 (−1264), DWARF |
| `nucleo-f429zi-freertos`, `nucleo-f439zi-freertos` | 1 | 89 retirés, 60 ajoutés, 16 modifiés ; `.text` 166580 → 167088 (+508), `.data` +60, `.bss` −1264, `.noinit` 4 → 0, DWARF |

Nature des écarts F4 : E-1 à E-5 de `rapports/env-35-hal-f4.md` §5.1. Les listes de symboles
F429 et F439 sont identiques entre elles. `F429 → F439` dans `env-35-apres` : code 1, sections
`.debug_*` seules (3 en embOS, 2 en FreeRTOS : `STM32F439xx` depuis ENV-35) ; 0 dans
`env-33-debian` (avant ENV-35).

Attendus dérivés, versionnés dans `env-36-mac/attendu/` :
- `comparaisons-mac/<preset>.txt` : sorties brutes du comparateur pour les 4 presets F4 ;
- `<preset>.noms.txt` : mêmes écarts normalisés (noms seuls, `.debug_*` exclues ; 172 lignes en
  embOS, 169 en FreeRTOS), comparés par la VM à `env-33-debian` → `env-36-debian` (les tailles
  diffèrent entre la chaîne du Mac et la chaîne APT).

Listes `ctest -N` : `env-32-apres/ctest-N/` ne contient que les variantes WL55 d'ENV-32 ;
`env-35-apres/ctest-N/` a host et les 16 presets. Pas de comparaison `ctest -N` dans la consigne
(chemins propres à l'hôte, `net.ping_ftpd` sous Linux seul) : le banc KAL QEMU est comparé à R33-1.

### 1.2 Têtes publiées (`git ls-remote`, 2026-11-05)

| Dépôt | Référence | Commit | En R33-1 |
| --- | --- | --- | --- |
| `lepton-tools` | `main` | 06cb55d | e47bc11 (`devenv/env-33`) |
| `seed.scions` | tag `0.5.4.0` | 99aa973 | = |
| `lepton-seed.scions` | `original-tree` | 15740f9 | = |
| `lepton-original-tree.scions` | `master` | 2893297 | b3a5415 |
| `lepton-famille-stm32f4xx` | `master` | 0fd8b2a | 8364493 |
| `lepton-bsp-nucleo-f429zi` | `master` | b9fe2bf | 2b2dfdd |
| `lepton-bsp-nucleo-f439zi` | `master` | 314f91b | bdbfa06 |
| 9 autres greffons famille/BSP | `master` | inchangés | = |

Clones de `<ROOTSTOCK>` aux mêmes commits, propres, alignés sur `origin`.

Paquet lepton : `git diff e47bc11 main` hors `doc/` = `scripts/tiers/` seul (3 fichiers, hors
paquet) ; pas de réinstallation sur la VM.

### 1.3 Liens du trunk

`git diff --no-renames --name-status` des 4 clones changés (commit de R33-1 → tête publiée),
limité à `scion/` : 215 ajouts, 194 retraits, 3957 + 21 = **3978** liens, égal au trunk du Mac.
Listes `env-36-mac/attendu/liens-ajoutes.txt` et `liens-retires.txt` (chemins `trunk/…`),
contrôlées sur `<ROOTSTOCK>` : chaque ajout est un lien présent, chaque retrait est absent.

| Clone | Ajouts | Retraits |
| --- | --- | --- |
| noyau | 2 (`core_cm4.h` 5.9.0, `CMSIS/Core/LEPTON-PROVENANCE.md`) | 0 |
| `family-stm32f4xx` | 211 (201 `hal_driver/`, 7 `cmsis-5/Device/ST/STM32F4xx/`, 3 `dev_stm32f4xx/` : `eth_x.{c,h}`, `hal_tick.c`) | 194 (190 `cubemx_hal_driver/`, 4 en-têtes HAL V1.3.0 de `driverlib/`) |
| `bsp-nucleo-f429zi`, `bsp-nucleo-f439zi` | 1 chacun (`stm32f4xx_hal_conf.h`) | 0 |

### 1.4 Consigne

`consignes/env-36-debian.md` : C1 versions ; C2 `graft-update` de `essais/env-28-debian` par
l'utilisateur, puis rootstock neuf `essais/env-36-debian` ; C3 host + 16 presets, comparaison à
`env-33-debian` ; C4 compilation à blanc (`compiler-hal-f4-a-blanc.sh`) ; C5 fichiers générés
(`$R` contre l'espace de `essais/env-33-debian`, `$P` stabilité) ; C6 nettoyage. Points laissés au
PA-59 : cartes, nettoyage, choix de C4 et C5.

## 2. PA-59 (2026-11-05, décisions de l'utilisateur)

- Consigne validée ; C4 et C5 retenus tels que rédigés.
- Carte : NUCLEO-F429ZI sur la VM (première carte sous Debian) ; écriture flash accordée pour les
  3 images d'ENV-35 construites sur la VM ; VM en mode pont, adresse relevée par la VM et
  confirmée par l'utilisateur ; droits de la sonde corrigés par l'utilisateur si besoin. Ajout du
  §10 (C7) à la consigne : commandes en clair, `banc-carte.sh` d'ENV-35 non utilisable sur Debian
  (`caffeinate`, macOS seul).
- Nettoyage C6 accordé (`essais/env-33-debian`, `~/env-33-journaux`).
- Push de `devenv/env-36` et ordre `R36-1` accordés ; `graft-update` dans `essais/env-28-debian`
  seulement, lancé par l'utilisateur.

## 3. Messages §2bis

| Message | Date | Sens | Résumé |
| --- | --- | --- | --- |
| ORDRE R36-1 | 2026-11-05 | Mac → VM (`debian-linux-vm`) | consigne `env-36-debian.md` @ bd7ad59 envoyée en entier ; PA-59 : `graft-update` de `essais/env-28-debian` par l'utilisateur, carte F429 (PA-11, 3 images), nettoyage C6, push sur accord ; envoi réussi, lecture non confirmée |
| ACCUSÉ R36-1 | 2026-11-05 | VM → Mac | premier envoi de l'accusé perdu (ECONNRESET), renvoyé ; `devenv/env-36` = bd7ad59 ; `ls-remote` = §1 ; Debian 13.7, noyau 6.12.107, scion 0.5.4.0, lepton 0.1.0, chaîne APT = R33-1, embOS présent, 18 Go libres ; `$U` conforme (13 clones aux commits de R33-1, 3957 liens) ; aucun écart |
| AVANCEMENT R36-1 (1) | 2026-11-05 | VM → Mac | §5.1 fait (`$P` generate/check 0, graine propre ; `$R33` generate 0, espace copié) ; §6.1 : 3957 liens relevés ; attente du `graft-update` par l'utilisateur |
| AVANCEMENT R36-1 (2) | 2026-11-05 | VM → Mac | §6 terminé, C2 conforme : `graft-update` de `$U` (utilisateur) code 0, 0 conflit, 13 clones aux commits du §1, ajouts 215 et retraits 194 = attendu, `hal_driver` 201, `device_f4` 7, 3978 liens ; rootstock neuf 3978 liens, liste = `$U`. Écart de consigne : « cubemx 157 » — 157 liens sous `stm32wlxx/cubemx_hal_driver/` (famille WL, hors ENV-34), 0 sous `stm32f4xx/` ; vérifié au Mac (157 WL, 0 F4) : défaut de la commande du §6.1, non restreinte à F4 ; critère C2 à lire « 0 sous `stm32f4xx/cubemx_hal_driver/` ». Écart de la VM : liste « avant » relevée en chemins absolus, convertie par `sed` (original conservé). §7 en cours |
| AVANCEMENT R36-1 (3) | 2026-11-05 | VM → Mac | §7 terminé, C3 conforme hors un signe : `rejouer-oracle.sh` 0 ; host 7/7 ; 16 presets ; QEMU 20/20, 16/16, 19/19, `peripheriques` Passed ; mklepton = `env-33-debian` = `env-35-apres` ; `comparer_R33-1` 0 ×12, 1 ×4 F4 avec listes normalisées = attendu ; `f429→f439` hors `.debug_*` 0. Deltas Debian : embOS `.text` +1308 (Mac +1340), FreeRTOS +540 (Mac +508), `.data` +60, `.bss` −1264, `.ccm_bss` 56408 inchangée ; **`.noinit` FreeRTOS 0 → 4 (Mac 4 → 0)**. Contrôle Mac : `.noinit` sans symbole (bourrage `. = ALIGN(0x8)`, E-5 d'ENV-35) ; `.bss + .noinit` après = 97712 sur les deux hôtes (`env-35-apres` : 97712 + 0 ; R36-1 : 97708 + 4) ; avant : Mac 98976 + 4, Debian 98972 + 0. Écart expliqué par l'alignement, proposé comme admis au PA-60 (proposition non validée) |
| AVANCEMENT R36-1 (4) | 2026-11-05 | VM → Mac | §8 (C4) conforme : code 1 attendu ; `cmsis5` 0 échec (F429, F439), `v330` 1 échec `stm32f4xx_ll_usb` (`__UNALIGNED_UINT32_READ/WRITE`), 0 avertissement ; `resume.txt` = Mac hors en-tête. §9 (C5) conforme : `$R` check/generate 0, 23/10/7/4, espace = `$R33` au chemin près ; `$P` identique. §11 : tailles 356 Mo (`env-33-debian`), 16 Mo (`~/env-33-journaux`), attente du `rm -rf` ; §10.1 : attente du rattachement USB de la carte |
| AVANCEMENT R36-1 (5) | 2026-11-05 | VM → Mac | §11 (C6) fait : `rm -rf` par l'utilisateur, `essais/env-33-debian` (356 Mo) et `~/env-33-journaux` (16 Mo) absents. §10.1 : carte rattachée par l'utilisateur ; ST-LINK/V2.1 0483:374b seule sonde, n° 0672FF495252717267243842 → `/dev/ttyACM0` ; OpenOCD 0.12.0 code 0 sans sudo (V2J27M15, 3,23 V, `stm32f4x.cpu`) ; port `root:plugdev` + ACL `uaccess` rw (pas dans `dialout`, sans objet) ; `60-openocd.rules` présente ; aucun sudo. Réseau : `ens37` 192.168.2.20/16, route vers 192.168.2.5 par `ens37`, ping 3/3. Attente de la confirmation de l'adresse par l'utilisateur |
| AVANCEMENT R36-1 (6) | 2026-11-05 | VM → Mac | adresse 192.168.2.20 confirmée par l'utilisateur à la session VM ; §10 (C7) conforme : 3 images, `oracle=0`, `ctest -L board` 20/20, fumée `cortexM4-stm32f4`, ping 3/3, LIST 13, RETR 57 o identique, `ECONNRESET=15` ; remarque : la synthèse de `board_net` est dans `carte-detail.log`, pas dans `reseau-carte.log` (défaut du `grep` de la consigne) |
| AVANCEMENT R36-1 (7) | 2026-11-05 | VM → Mac | rapport commité (683b911) ; push accordé par l'utilisateur, rejeté deux fois par GitHub (« fatal error in commit_refs_rules ») ; arrêt avant FIN |
| FIN-SUCCÈS R36-1 | 2026-11-05 | VM → Mac | C1 à C7 conformes ; `devenv/env-36-debian` 683b911 poussée au 3e essai (accord de l'utilisateur ; refus précédents attribués à une erreur passagère du serveur) ; rapport `rapports/env-36-debian.md` (§8 « Non fait » cite encore le push en attente) ; écarts : comptage cubemx (WL), liste avant convertie, `.noinit` (PA-60), synthèse `board_net` |
| AVANCEMENT R36-1 (8) | 2026-11-05 | VM → Mac | carte rattachée de nouveau au Mac par l'utilisateur, image `nucleo-f439zi-embos` de la VM en flash ; aucune sonde côté VM |

## 4. Vérification du rapport VM (tâche 4)

`origin/devenv/env-36-debian` = 683b911, un commit sur `devenv/env-36` (bd7ad59) ; 117 fichiers,
tous sous `rapports/env-36-debian.md` et `rapports/oracles/env-36-debian/` (aucune autre écriture).
Comparaisons refaites au Mac sur l'oracle poussé (extrait par `git archive`) :

| Contrôle | Résultat Mac | Consigne |
| --- | --- | --- |
| mklepton host | = `env-33-debian` = `env-35-apres` | conforme |
| `comparer_R33-1`, 12 presets hors F4 | 0 ×12 | conforme |
| `comparer_R33-1`, 4 presets F4 | 1 ×4 ; listes normalisées = `attendu/<preset>.noms.txt` ×4 | conforme |
| Deltas F4 | embOS `.text` 164840 → 166148, `.data` +60, `.bss` 98564 → 97300 ; FreeRTOS `.text` 171692 → 172232, `.data` +60, `.bss` 98972 → 97708, `.noinit` 0 → 4 ; F429 = F439 | signe de `.noinit` inverse du Mac : expliqué (§3, AVANCEMENT 3), PA-60 |
| `f429→f439` | code 1, hors `.debug_*` 0 (embOS, FreeRTOS) | conforme |
| `ctest` / banc KAL | host 7/7 ; 20/20 ×2, 16/16 ×2, 19/19 ×2 | conforme |
| Compilation à blanc | `cmsis5` 0 échec, `v330` 1 échec, 0 avertissement (chaîne `15:14.2.rel1-1`) | conforme |
| Carte (3 images) | `carte-oracle.txt` 0 écart ; 20/20 ; `board_net` : ping 3/3, LIST 13, RETR 57 octets identique, `ECONNRESET=15` | conforme |

Rapport VM : critères C1 à C7 présents et conformes ; écarts consignés (comptage cubemx WL, liste
avant convertie, `.noinit`, synthèse `board_net` dans `carte-detail.log`). Son §8 « Non fait »
cite encore le push comme en attente, alors qu'il a été fait depuis (FIN-SUCCÈS). Le rapport n'est
pas corrigé ; le constat est consigné ici.

Défauts de la consigne relevés à l'exécution (sans effet sur les résultats) : `grep -c
cubemx_hal_driver/` non restreint à `stm32f4xx/` (§6.1) ; synthèse de `board_net` cherchée dans
`reseau-carte.log` au lieu de `carte-detail.log` (§10.2).

## 5. Rootstocks d'essai du Mac (tâche 3)

Accord de l'utilisateur (PA-P) : les 7, 2026-11-05. scion 0.5.4.0, lepton 0.1.0 (inchangé).
Journaux : `~/lepton-tools-dev/essais/env-36-mac/` (`<rootstock>-{generate-avant,graft-update,
check,generate}.log`, `-liens-{avant,apres}.txt`, `-espace-avant/`, `-espace.diff`).

Inventaire avant (lecture seule) : tous les clones sur `master`, amont `origin/master`, propres, aux
têtes de R33-1 (noyau b3a5415, `family-stm32f4xx` 8364493, BSP F429 2b2dfdd, F439 bdbfa06) ;
0 lien cassé ; aucun fichier régulier hors `.DS_Store` du Finder (6 ou 7 par trunk, tolérés).
Espaces régénérés par `lepton generate` juste avant le relevé (`qemu-gra2` : code 1, attendu).

| Rootstock | `graft-update` | Liens avant → après | Ajouts / retraits | Entrées | Cassés | `check` | `generate` | Espace | `request` / `lldb` / `svdFile` / tests |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `env-9` | 0 | 3056 → 3058 | 2 (noyau) / 0 | 5 | 0 | 0 | 0 | identique | 3 / 1 / 0 / 2 |
| `env-11/f429zi` | 0 | 3369 → 3389 | 214 / 194 (noyau 2, famille F4 211/194, BSP F429 1) | 5 | 0 | 0 | 0 | identique | 2 / 1 / 1 / 0 |
| `env-11/qemu` | 0 | 3056 → 3058 | 2 / 0 | 5 | 0 | 0 | 0 | identique | 3 / 1 / 0 / 2 |
| `env-11/qemu-gra2` | 0 (BSP an386 réinscrit, +8), puis `graft-remove lepton@bsp-qemu-mps2-an386` sans `--purge` (8 feuilles), code 0 | 3048 → 3050 | 2 / 0 | 4 | 0 | 1 (attendu, CFG-5) | 1 (attendu) | identique | 1 / 0 / 0 / 0 |
| `env-11/wl55jc1` | 0 | 3306 → 3308 | 2 / 0 | 5 | 0 | 0 | 0 | identique | 2 / 1 / 1 / 0 |
| `env-11/bout-en-bout/rootstock` | 0 | 3056 → 3058 | 2 / 0 | 5 | 0 | 0 | 0 | identique | 2 / 1 / 0 / 1 |
| `env-13-vierge` | 0 | 3957 → 3978 | 215 / 194 | 14 | 0 | 0 | 0 | identique | 23 / 7 / 10 / 4 (= `<ROOTSTOCK>`) |

Clones après : tous sur `master`, propres, aux têtes publiées (noyau 2893297, famille F4 0fd8b2a,
F429 b9fe2bf, F439 314f91b). `env-13-vierge` : liste des liens identique à `<ROOTSTOCK>`. Aucun
fichier régulier hors `.DS_Store`, aucun lien cassé.

`env-11/f429zi`, construction à neuf de `host` et `nucleo-f429zi-embos` : code 0 ; contre
`oracles/env-35-apres/nucleo-f429zi-embos` : 0 écart de symboles, sections allouées identiques ;
seules `.debug_line` (306512 → 330785) et `.debug_str` (139384 → 143414) diffèrent, attendu
(chemins des sources propres au rootstock `essais/env-11/f429zi`) ; pas de flash.
