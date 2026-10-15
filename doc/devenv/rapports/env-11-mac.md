# ENV-11 — Validation de bout en bout, hôte Mac Intel

Session S1 (2026-10-15) : scénario §2 étapes 1 à 4, 8 et 9 (partie ligne de commande), plus la
préparation des étapes 5-6. Étapes 5, 6, 7 et la partie éditeur de 9 : session S2 (VSCodium et cartes).

## 1. Cadre

| Élément | Valeur |
| --- | --- |
| Hôte | Mac mini Intel, macOS (Darwin 24.6.0) |
| Outils | scion 0.5.1.0, lepton 0.1.0 (pipx, depuis `devenv/env-11` après 7d191aa), CMake 3.31.12, GCC 14.2.Rel1, QEMU 11.1.2, OpenOCD 0.12.0, VSCodium 1.135.06055 |
| Rootstocks d'essai (non versionnés) | `~/lepton-tools-dev/essais/env-11/{qemu,f429zi,wl55jc1}` ; journaux `essais/env-11/logs/` |
| Origine des greffons | `file://localhost~/lepton/depots/…@master` (comme `scripts/bout-en-bout.sh`) |
| Graines | `env11` (an386, FreeRTOS), `env11f4` (NUCLEO-F429ZI, embOS), `env11wl` (NUCLEO-WL55JC1, FreeRTOS) : une graine par carte (décision du 2026-10-15) |
| Référence `~/lepton` | HEAD et `status` de 9 dépôts relevés avant et après : identiques (`essais/env-11/ref-{avant,apres}.txt`) |

## 2. Scénario

| Étape | Commande (résumé) | Résultat | Exigences |
| --- | --- | --- | --- |
| 2.1 | `scripts/install-vscodium.sh --lepton-clone ~/lepton/depots/lepton/original/master --seed-scions ~/lepton-tools-dev/seed.scions` | code 0, `install-macos.sh` appelé, **0 changement**, aucun `sudo` (5 s) | INS-1 à INS-6 |
| 2.2 | `lepton seed new env11 -C …/qemu --bsp qemu-mps2-an386 --backend freertos --mkconf sys/user/tauon-basic/etc/mkconf_tauon_basic_qemu_mps2.xml --origin …` (noyau, famille, BSP ; aucune application) | code 0 ; `lepton check` 5 fichiers conformes ; `seed status` : rôles, versions, commits, trunk propre. **Défaut N1** : noyau sur `devenv/env-11` au lieu de `master` (§3) ; contourné par `git checkout master` dans le clone d'essai | GRA-1, GRA-2, GRA-3, GRA-6 |
| 2.2 (GRA-2, copie) | `lepton seed remove qemu-mps2-an386` ; `lepton seed remove lepton-noyau` | refus code 1 : « est le BSP / le noyau de la graine, obligatoire (GRA-2) » | GRA-2 |
| 2.2 (GRA-2, copie) | BSP dégreffé (`scion graft-remove`), puis `lepton check` et `cmake --preset` | `lepton check` code 1 : « BSP « qemu-mps2-an386 » non greffé (GRA-2) » ; CMake code 1 mais message indirect (`boards/qemu-mps2-an386` introuvable, `LEPTON_BOARD_CPU_FREQ non défini`) : **O1** | GRA-2 |
| 2.3 | `lepton generate` ; `cmake --list-presets` | `env11-debug-qemu` + 15 presets du noyau ; `CMakeUserPresets.json` greffé (lien) ; `.DS_Store` du Finder supprimés (Q8) | CFG-6, GRF-3 |
| 2.3 | `cmake --preset host`, `cmake --preset env11-debug-qemu`, `cmake --build` | code 0 ; `lepton.{elf,bin,hex,map,occupation.txt}` ; cibles `kernel`, `lib`, `sbin`, `bin`, `generated`, `kernel_demarrage`, `bsp_demarrage` (pas de `bsp` ni `bsp_objets` pour an386 : un seul fichier de démarrage, comme la référence `~/lepton/build/qemu-mps2-an386-freertos`) ; aucune sortie dans le trunk | BLD-1, BLD-3, BLD-4 |
| 2.3 | `ctest --preset env11-debug-qemu -L smoke` puis `-L kal` | fumée : réussie ; banc KAL : **18/18** (`arch:cortex-m4f`, `backend:freertos`) | TST-1 (CLI) |
| 2.4 | `lepton scion new --type application salut` | 1ᵉʳ essai : **défaut N2** (refus de scion à cause des `.DS_Store`, annulation incomplète) ; corrigé (338ff5b), relancé : code 0, reconfiguration CMake | GRF-1 |
| 2.4 | `cmake --build` du modèle d'application | **défaut N3** : `kernel/libstd.h` introuvable ; modèle corrigé (7d191aa), greffon recréé : `salut.c.obj` compilé sans retouche | GRF-1 |
| 2.4 | `lepton file add <trunk>/sys/root/src/bin/salut/salut_message.c` ; contenu écrit dans le clone | lien créé dans le trunk, fichier non suivi dans le clone (pas de `git add`, PA-9) ; `cmake --build` : « Re-running CMake », `salut_message.c.obj` compilé, aucune liste CMake éditée | FIC-1, FIC-3, FIC-4, BLD-2 |
| 2.4 | `<bin name="salut">` ajouté au XML **du clone noyau d'essai** (PA-9 Q5) ; `lepton check` ; construction ; `smoke_lsh.py --command "ls /usr/bin" --command salut` | `salut_main`, `salut_message` liés ; `/usr/bin` : `net salut` ; sortie `salut depuis salut_message.c` : **O5** | CFG-1, CFG-5 |
| 2.8 | `lepton scion remove salut` | liens retirés, aucun lien orphelin ni fichier régulier, clone `salut` intact (HEAD 4e1df4c, propre) ; puis reconfiguration CMake en échec (code 2) tant que le XML déclare `salut` ; `lepton check` code 1 (CFG-5) : **O4**. Déclaration retirée du XML : construction et fumée réussies | GRF-4, CFG-5 |
| 2.9 (CLI) | `SOURCE_DATE_EPOCH=1760536800` ; `cmake --preset env11-debug-qemu -B build/bld5-a` puis `-B build/bld5-b`, et `--fresh` + `--clean-first` dans `build/env11-debug-qemu` | `lepton.bin` sha256 `25d50f61…` et `lepton.hex` `7e29c21c…` identiques sur les trois constructions ; partie éditeur en S2 | BLD-5 (CLI) |
| 5-6 (préparation) | `lepton seed new env11f4 … --bsp nucleo-f429zi --backend embos --mkconf …nucleo_f439zi.xml` ; `env11wl … --bsp nucleo-wl55jc1 --backend freertos --mkconf …nucleo_wl55jc1.xml` ; `lepton generate` ; construction | `env11f4-debug-board` et `env11wl-debug-board` construits (`openocd-nucleo-wl55jc1.cfg` généré) ; F429 embOS : échec tant que `LEPTON_EMBOS_ROOT` n'est pas exporté (**O6**), puis réussi ; espaces de travail : lancement OpenOCD et tâche « flasher » présents | GRA-1, GRF-3, CFG-6 |

Non-régression de `lepton` après N2 et N3 : `pytest -q` **117 passed** (116 + 1 nouveau) ;
`scripts/bout-en-bout.sh essais/env-11/bout-en-bout` : succès.

## 3. Défauts

| ID | Composant (étape responsable) | Constat | Suite |
| --- | --- | --- | --- |
| N1 | scion `gitops.clone` (ENV-7 ; présent depuis 0.5.0.1) | Version `master` → `git clone` sans `checkout` : le clone reste sur la branche par défaut de l'origine (ici `devenv/env-11`, extraite dans `~/lepton`). Même effet avec une origine dont la branche par défaut est `main`. `seed lock` figerait un commit qui n'est pas celui de la version déclarée | Consigné, renvoyé à ENV-7 (correctif et version de scion à décider) ; contournement : `git -C <clone> checkout master` après `seed new` |
| N2 | lepton (ENV-8, PA-9 Q8) | Purge des `.DS_Store` faite par `lepton graft` et `generate` seulement ; `seed add/remove/replace`, `seed lock --restore`, `scion new/remove`, `file add` appelaient `scion graft` / `graft-remove` sans purge et échouaient dès que le Finder avait parcouru le trunk | **Corrigé** dans ENV-11 (décision de l'utilisateur) : `Rootstock.purge_system_files()` et `seed.scion_on_trunk()`, test `test_gra4_add_remove_with_finder_files` (échoue sans la correction) ; commit 338ff5b |
| N3 | lepton, modèle d'application (ENV-8) | `#include "kernel/libstd.h"` et `"stdio/stdio.h"` introuvables : l'application créée ne compile pas (tests d'ENV-8 à construction simulée) | **Corrigé** dans ENV-11 (décision de l'utilisateur) : `kernel/core/libstd.h`, `lib/libc/stdio/stdio.h` (forme de `sbin/uname.c`), assertion dans `test_grf1_scion_new_application` ; commit 7d191aa ; compilation réelle prouvée |

## 4. Observations (à classer au bilan)

| ID | Constat | Renvoi proposé (non validé) |
| --- | --- | --- |
| O1 | BSP de la graine non greffé : CMake refuse, mais par un message indirect (fichier `boards/<bsp>` absent, fréquence non définie) ; `lepton check` est explicite | ENV-6 (lecteur `cmake/lepton_greffons.cmake` : message « aucun manifeste BSP `<nom>` greffé ») |
| O2 | `lepton seed new` crée une seule configuration (`debug-qemu` ou `debug-board`, PA-9) ; aucune commande pour en ajouter (édition de `lepton-graine.json`) | ENV-8 / ENV-12 (commande ou palette) |
| O3 | Après annulation incomplète, le message de reprise de `scion new` annonce « hors graine » alors que le greffon reste dans `.scion.sources.list` et la liste greffée (cas devenu rare avec N2) | ENV-8 |
| O4 | `lepton scion remove` d'une application déclarée dans le XML : retrait fait, puis reconfiguration CMake en échec (« Cannot find source file …/salut.c ») sans avertissement préalable ; `lepton check` le signale | ENV-8 (avertissement CFG-5 dans `scion remove`) |
| O5 | Exécuter une application impose d'éditer le XML mklepton porté par le **greffon noyau** (PA-9 Q5) : une modification propre au projet entre dans un greffon partagé ; CFG-1 demande un XML versionné dans la graine | Décision de conception (ENV-8 / ENV-12) |
| O6 | Rootstock neuf : `LEPTON_EMBOS_ROOT` doit être exporté à la main (embOS hors git, `lepton-env.sh` le cherche sous `<rootstock>/third_party`) ; l'espace de travail généré ne le transmet pas : une construction embOS depuis VSCodium lancé sans cette variable échouera | À vérifier en S2 ; ENV-9 si confirmé |
| O7 | Le Finder recrée des `.DS_Store` dans les trunks d'essai pendant la session | Traité par N2 (PA-9 Q8) |

## 5. Reste (S2, S3)

- S2 : étapes 5-6 (flash, arrêt sur `main`, console série ; PA-11 accordé), 7 (VSCodium : IDE-1 à
  IDE-5, DBG-1 à DBG-3, lemminx natif CFG-7), 9 partie éditeur (empreinte comparée à `25d50f61…`
  avec `SOURCE_DATE_EPOCH=1760536800`), O6.
- S3 : scénario Debian (étapes 1-4 et 9, VM ; push soumis à PA-P), bilan des exigences P1.
