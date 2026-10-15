# ENV-11 — Validation de bout en bout, hôte Debian — 2026-10-15

Session VM Debian (ENV-11 S3), conduite par `consignes/env-11-debian.md` : étapes 2.1 à 2.4, 2.8 et
2.9 (ligne de commande) du scénario d'ENV-11. Journaux (non versionnés) : `~/env-11-journaux/`
(une commande par fichier, code de retour en dernière ligne). Rootstock d'essai conservé :
`~/lepton-tools-dev/essais/env-11/qemu`.

## 1. Hôte

| Élément | Valeur |
| --- | --- |
| Système | Debian 13.7 (trixie), Linux x86_64 (6.12.107+deb13-amd64), utilisateur `lepton-user` |
| Outils | VSCodium 1.135.06055, scion 0.5.1.0, arm-none-eabi-gcc 14.2.1 (15:14.2.rel1-1), cmake 3.31.6, ninja 1.12.1, QEMU 10.0.13 (Debian 1:10.0.13+ds-0+deb13u1), gdb-multiarch 16.3, Python 3.13.5 |
| Environnement | `LEPTON_EMBOS_ROOT=~/lepton/third_party/embos/cortexm-gcc/5.20.0.0` (définie, sans effet sur le scénario FreeRTOS) ; `SOURCE_DATE_EPOCH` absente |
| Espace | `/tmp` 747 Mo (292 Mo libres) ; `/home` 26 Go (20 Go libres) |
| `lepton-tools` | `devenv/env-11` 8cca1c0 (le commit qui ajoute la consigne ; le 53ca625 annoncé par la session Mac n'existe pas sur `origin`) ; rapport et correction sur `devenv/env-11-debian` |
| Clone noyau `~/lepton-tools-dev/lepton-noyau` | `devenv/env-11` a572f00 |
| `seed.scions` | tag `0.5.1.0` |
| Greffons (`git ls-remote`, SSH) | `lepton-original-tree.scions` 1dde0af, `lepton-famille-qemu-mps2` 3954357, `lepton-bsp-qemu-mps2-an386` 046779e : conformes |
| `lepton --version` | avant §5.2 : `lepton 0.1.0` (ENV-10) ; après : `lepton 0.1.0` depuis 8cca1c0, puis depuis 55a55bc (§4) |

## 2. Scénario

| Étape | Commande (résumé) | Résultat | Exigences |
| --- | --- | --- | --- |
| 2.1 | `scripts/install-vscodium.sh --lepton-clone ~/lepton-tools-dev/lepton-noyau --seed-scions ~/lepton-tools-dev/seed.scions` (lancé par l'utilisateur, sudo) | code 0, **changements 0** ; `lepton 0.1.0 : déjà installé` (**O12** constaté) ; Graphify non abouti (avertissement connu, ENV-10) | INS-4 |
| 5.2 | `pipx install --force ~/lepton-tools-dev/lepton-tools` | code 0 ; `direct_url` = clone local ; paquet installé identique à `lepton/` de 8cca1c0 (contient N2 338ff5b et N3 7d191aa) ; version inchangée 0.1.0 | — |
| 2.2 | `lepton seed new env11 -C …/qemu --bsp qemu-mps2-an386 --backend freertos --mkconf …qemu_mps2.xml --origin …=ssh://git@github.com/lepton-distribution/…@master` (×3) | code 0 ; graine 9cfdadc ; trois clones sur `master` aux commits attendus (N1 sans effet) | GRA-1, GRA-3, GRA-6 |
| 2.2 | `lepton check` ; `lepton seed status` | `check` code 0, 5 fichiers conformes, avertissement « xmllint absent : XML mklepton non validé » (**D3**) ; `status` code 0 : rôles, versions, commits, origines SSH, trunk propre | GRA-1 |
| 2.2 | `lepton seed remove qemu-mps2-an386` ; `lepton seed remove lepton-noyau` | refus code 1 : « est le BSP / le noyau de la graine, obligatoire (GRA-2) » | GRA-2 |
| 2.3 | `lepton generate` (1ᵉʳ essai) | **code 2** : « arm-none-eabi-gdb absent du PATH (débogage) » : **défaut D1**, propre à Debian, corrigé (§4) | CFG-6 |
| 2.3 | `lepton generate` (après 55a55bc) ; `cmake --list-presets` | code 0 ; `CMakeUserPresets.json` greffé ; `env11-debug-qemu` + 15 presets du noyau ; `gdbPath` = `/usr/bin/gdb-multiarch` ; avertissement « aucun clangd LLVM trouvé » (**D4**) | CFG-6 |
| 2.3 | `cmake --preset host` + `--build` ; `cmake --preset env11-debug-qemu` + `--build` | code 0 ; `lepton.{elf,bin,hex,map,occupation.txt}` ; trunk sans fichier régulier | BLD-1, BLD-3, BLD-4 |
| 2.3 | `ctest --preset env11-debug-qemu -L smoke` puis `-L kal` | fumée réussie ; banc KAL **18/18** (fumée + T1-T8, T1F, T4F, T6F, T7F, TICI, TCLK, TSBRK, IRQ, harness_fail) | TST-1 (CLI) |
| 2.4 | `lepton scion new --type application salut` ; `cmake --build` | code 0, reconfiguration de `env11-debug-qemu` et `host` ; `salut.c.obj` compilé sans retouche | GRF-1 |
| 2.4 | `lepton file add <trunk>/sys/root/src/bin/salut/salut_message.c` ; contenu écrit dans le clone | code 0, fichier créé dans le clone `salut` (non suivi), lien dans le trunk | FIC-1, FIC-4 |
| 2.4 | `<bin name="salut">` dans le XML du clone noyau d'essai, **après `pwd` comme le dit la consigne** ; `cmake --build` | code 1 : « Cannot find source file …/sbin/salut.c » : la ligne est dans le bloc `src_path="sbin"` : **défaut D2** de la consigne | — |
| 2.4 | bloc `<binaries src_path="bin" dest_path="bin">` ajouté après `bin/net` (accord de l'utilisateur) ; `lepton check` ; `cmake --build` ; `smoke_lsh.py --command "ls /usr/bin" --command salut` | `check` code 0 (6 fichiers) ; « Re-running CMake », `salut.c.obj` et `salut_message.c.obj` compilés, aucune liste CMake éditée ; `/usr/bin` : `net  salut` ; sortie `salut depuis salut_message.c` ; trunk sans fichier régulier | FIC-3, BLD-2, CFG-5 |
| 2.8 | `lepton scion remove salut` | « salut retiré », puis code 2 : reconfiguration CMake en échec (« Cannot find source file …/bin/salut.c ») tant que le XML déclare `salut` (**O4**, identique au Mac) ; aucun lien orphelin ; clone `salut` présent (HEAD 71e1641) | GRF-4 |
| 2.8 | `lepton check` | code 1 : « binaire déclaré dans le XML, salut_main défini par aucun greffon greffé (CFG-5) » | CFG-5 |
| 2.8 | bloc `bin` retiré du XML ; `cmake --build` ; `ctest -L smoke` ; `lepton check` | code 0 ; fumée 1/1 ; `check` code 0 ; clone noyau d'essai propre | GRF-4 |
| 2.9 (CLI) | `SOURCE_DATE_EPOCH=1760536800` ; `cmake --preset env11-debug-qemu -B build/bld5-a` puis `-B build/bld5-b` ; construction | code 0 ×4 ; `lepton.bin` `ac30ba3e8f5c14db…` et `lepton.hex` `24b8315d529e354f…` **identiques** entre a et b | BLD-5 (CLI) |
| fin | `find trunk -type f` ; `find -L trunk -type l` ; état des clones | trunk : aucun fichier régulier, aucun lien cassé ; clones noyau, famille, BSP propres ; graine : 3 entrées (`.scion.ramifications`, `.scion.sources.list`, `project/` : non commitées, `lepton` le rappelle) ; `salut` : 2 entrées (`salut.c` modifié, `salut_message.c` non suivi) | — |

## 3. Comparaison avec le Mac

| Étape | Écart Debian / Mac (`env-11-mac.md` §2) |
| --- | --- |
| 2.1 | Debian passe par `install-debian.sh` (sudo, APT) ; même bilan `changements 0` |
| 2.2 | Origines SSH GitHub (Mac : `file://localhost~/lepton/…`) ; N1 sans effet ici (branche par défaut `master`) |
| 2.3 | `lepton generate` en échec jusqu'à la correction D1 (Mac : réussi) ; pas de clangd LLVM (D4) ; résultat ensuite identique, KAL 18/18 |
| 2.4 | N2 et N3 absents (lepton installé après 338ff5b et 7d191aa) ; échec D2 dû à la consigne, puis résultat identique (`/usr/bin` : `net salut`, `salut depuis salut_message.c`) |
| 2.8 | Identique (O4, `check` code 1). Le Mac note le clone `salut` propre (HEAD 4e1df4c) ; ici il porte les modifications de 2.4 non commitées : le scénario ne prévoit pas de commit |
| 2.9 | BLD-5 tenu sur chaque hôte. Empreintes (information, chaînes différentes) : Debian `lepton.bin` `ac30ba3e…`, `lepton.hex` `24b8315d…` ; Mac `25d50f61…`, `7e29c21c…` |

## 4. Corrections propres à Debian

| Commit | Défaut | Correction | Accord |
| --- | --- | --- | --- |
| 55a55bc (`devenv/env-11-debian`) | **D1** : `lepton generate` exige un exécutable nommé `arm-none-eabi-gdb` (`lepton/generate.py`, `host_tools`) ; Debian 13 n'en fournit pas, le débogueur ARM y est `gdb-multiarch` (installé par `install-debian.sh`). Jamais vu avant : `generate` (ENV-9) n'avait pas été exécuté sur Debian en ENV-10 | `require_tool` accepte des noms de repli ; `arm-none-eabi-gdb` reste prioritaire (Mac inchangé), `gdb-multiarch` à défaut ; message « installer arm-none-eabi-gdb ou gdb-multiarch ». Tests : `test_missing_tool_is_exit_2` adapté, `test_gdb_multiarch_when_no_arm_gdb` ajouté ; suite : 107 réussis, 11 ignorés (xmllint absent) | utilisateur, 2026-10-15 |

La correction touche `lepton` lui-même : la session Mac doit l'intégrer à `devenv/env-11`.

## 5. Défauts et observations

Défauts et observations pour la session Mac :

| Id | Constat | Proposition |
| --- | --- | --- |
| D2 | `consignes/env-11-debian.md` §5.5 place `<bin name="salut">` « après `<bin name="pwd" …/>` », donc dans le bloc `src_path="sbin"` : `firmware.cmake` cherche `sbin/salut.c`, reconfiguration en échec. La forme utilisée au Mac n'est pas consignée dans `env-11-mac.md` | Consigner la forme exacte (bloc `<binaries src_path="bin" dest_path="bin">`) dans `env-11-mac.md` §2 et dans toute consigne future |
| D3 | `xmllint` absent sur la VM : `lepton check` n'a pas validé le XML mklepton (avertissement prévu, ENV-8), 11 tests de `test_milestone1.py` ignorés. Ni `install-debian.sh` (`libxml2-utils`) ni `install-macos.sh` (`libxml2`) ne l'installent ; au Mac il vient d'une installation MacPorts manuelle (ENV-3) | Ajouter libxml2 aux deux scripts d'installation (défaut commun) |
| D4 | Aucun clangd LLVM sur la VM (`clang-19`, `clang-tools-19` installés, pas `clangd-19`) : `generate` omet `clangd.path` (avertissement) | Ajouter `clangd` à `install-debian.sh` (propre à Debian, non corrigé : clone noyau en lecture seule) |
| O12 | Constaté : `install-vscodium.sh` répond « lepton 0.1.0 : déjà installé » et ne réinstalle pas ; réinstallation forcée nécessaire (§5.2, puis encore après 55a55bc) | Déjà ouvert |
| O13 | `/tmp` de la VM limité à 747 Mo : un venv de test et les répertoires `pytest-of-*` l'ont saturé, `pipx install` a échoué (« No space left on device ») ; nettoyé, relancé | Information (prévoir `TMPDIR` pour les tests sur la VM) |

Questions pour l'utilisateur : classement de D2-D4 et O13 au bilan d'ENV-11 (session Mac).
