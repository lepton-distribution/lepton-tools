# ENV-8 R2 — valeurs d'options fixées par la graine (N5, CFG-4)

Reprise n° 2 du bilan ENV-11 (`env-11-bilan.md` §3, N5 : « aucune valeur d'option fixable dans la
graine ; seul le défaut est contrôlé »). Session du 2026-10-16, branches `devenv/env-8-r2`
(lepton-tools, clone noyau).

## 1. Conception (décisions de l'utilisateur, 2026-10-16)

| Sujet | Décision |
| --- | --- |
| Forme | `options` de `lepton-graine.json` : `{<greffon>: {<NOM>: valeur}}` (noms uniques par greffon seulement) |
| Portée | Tout le projet (pas de valeur par configuration) |
| Transport | `lepton generate` écrit une variable de cache `LEPTON_OPTION_<greffon>_<NOM>` par valeur dans chaque preset de `CMakeUserPresets.json` (booléen : `1`/`0`) |
| Contrôle | `lepton check` et `lepton generate` (graine contre manifestes) ; lecteur CMake (valeur reçue, y compris par `-D`, et défaut du manifeste) |
| Schéma | PA-3 R2 : `schemas/graine.schema.json` (`options`, `$defs/valeurs_options`), exemple `graine.json`, 4 invalides ; CFG-4 amendée |

## 2. Réalisation

| Dépôt | Commit | Contenu |
| --- | --- | --- |
| lepton-tools | 86732eb | Schéma de graine, exemples, `SPECIFICATION.md` CFG-4 |
| lepton-tools | 843f0fb | `lepton/checks.py` : `check_seed_options` (appelé par `check_seed`), `seed_scions` ; `lepton/generate.py` : `option_cache`, refus dans `Context` ; tests `test_cfg4_check_valeurs_options_graine`, `test_cfg4_option_values_in_presets` |
| clone noyau | 82a6700 | `scion/cmake/lepton_greffons.cmake` : `_lepton_option_controle` ; `LEPTON_OPTION_<greffon>_<NOM>` remplace le défaut ; défaut contrôlé ; variable sans option : avertissement |
| clone noyau | 53ceb58 | O16 : chaîne échappée (`"`, `\`), `;` `#` et saut de ligne refusés ; O15 : libellé « (valeur fixée : graine ou -D) » |
| lepton-tools | e7d695b | O16 : motif `^[^;#\n\r]*$` du défaut `chaine` (schéma de greffon, exemple invalide `option-chaine-diese.json`), refus dans `lepton check` / `generate` (`UNSENDABLE`) ; test |

Contrôles de lepton : greffon absent de la graine (noyau, BSP, famille du BSP, applications,
bibliothèques), option non déclarée par ce greffon, type, entier hors `[min, max]`, énumération
hors `valeurs`. Contrôles de CMake : booléen reconnu par CMake (`1 0 ON OFF YES NO TRUE FALSE Y
N`), entier `^-?[0-9]+$` dans les bornes, énumération dans les valeurs, chaîne sans `;` `#` ni saut
de ligne ; refus par `FATAL_ERROR`
citant le manifeste et la variable. Une variable `LEPTON_OPTION_*` sans option correspondante ne
donne qu'un avertissement : retirer une valeur de la graine ne l'efface pas du cache CMake.

Chaînes (O16, décision de l'utilisateur) : le lecteur échappe `"` et `\` (la chaîne C est celle
du JSON). `;` (séparateur de liste de CMake : valeur coupée) et `#` (définition retirée par CMake,
« CMake is dropping a preprocessor definition ») ne sont pas transmissibles par une définition de
compilation, même échappés (essai sur projet minimal, Ninja ; `%`, `$`, `'`, `` ` ``, espace
transmis tels quels) : refusés, avec les sauts de ligne.

## 3. Non-régression (oracle avant / après, skill `lepton-oracle`)

Mêmes commandes : `scripts/oracle/rejouer-oracle.sh ~/lepton <oracle> --qemu …×6 --carte …×8` ;
avant : `oracles/env-8-r2-avant/` (noyau 66676b6, validé par l'utilisateur), après :
`oracles/env-8-r2-apres/` (noyau 82a6700), puis `oracles/env-8-r2-apres-final/` (noyau 53ceb58,
après O15 et O16 : mêmes résultats que la colonne ci-dessous). Arm GNU Toolchain 14.2.Rel1.

| Preset | Sections/symboles | Empreinte | Fumée | Banc KAL | Écarts expliqués |
| --- | --- | --- | --- | --- | --- |
| host | – | mklepton : 44 identiques | – | ctest 7/7 = 7/7 | – |
| qemu-mps2-an386-embos | identiques | différente | passée (E2) | 18/18 = 18/18 | E1 |
| qemu-mps2-an386-embos-soft | identiques | différente | passée (E2) | 14/14 = 14/14 | E1 |
| qemu-mps2-an386-freertos | identiques | différente | passée (E2) | 18/18 = 18/18 | E1 (démontré) |
| qemu-mps2-an386-freertos-soft | identiques | différente | passée (E2) | 14/14 = 14/14 | E1 |
| qemu-mps2-an500-embos | identiques | différente | passée (E2) | 18/18 = 18/18 | E1 |
| qemu-mps2-an500-freertos | identiques | différente | passée (E2) | 18/18 = 18/18 | E1 |
| nucleo-f429zi-embos / -freertos | identiques | différentes | – | – | E1 |
| stm32f746g-disco-embos / -freertos | identiques | différentes | – | – | E1 |
| samd21-xplained-pro-embos / -freertos | identiques | différentes | – | – | E1 |
| nucleo-wl55jc1-embos / -freertos | identiques | différentes | – | – | E1 |

`comparer-oracle.py` : code 0 sur les 14 presets croisés. Banc KAL : lignes `Test #` identiques
(durées ignorées) sur les 6 presets QEMU.

**E1** — empreintes ELF/BIN/HEX différentes, sections et symboles identiques. `rejouer-oracle.sh`
ne fixe pas `SOURCE_DATE_EPOCH` : le binaire embarque la date de construction (chaîne « kernel
compilation date » du noyau, dates de l'image UFS). Démonstration
(`env-8-r2-preuve-empreintes.sh`, copie du rootstock sans `build/`) : `SOURCE_DATE_EPOCH=1760536800`,
an386-freertos construit à neuf au commit 66676b6 puis 82a6700, et 66676b6 puis 53ceb58
(`REVS="66676b6 53ceb58"`) → `lepton.elf` `28722270…`,
`lepton.bin` `b50826ae…`, `lepton.hex` `b3d8d68f…` **identiques**. Aucun manifeste réel ne
déclare d'options : le changement est sans effet sur les binaires, comme attendu.

**E2** — `fumee.log` comparés en ignorant les horodatages (date de compilation affichée au
démarrage et par `uname -a`) et les adresses : restent le jeton aléatoire de l'essai UART
(`echo lepton-uart1-<n>`) et, sur certains presets, la ligne asynchrone `rcv SIGCHLD` capturée
ou non selon l'instant d'arrêt de la console (présente aussi bien dans des oracles avant
qu'après depuis ENV-0, ex. `env-8-r2-avant/qemu-mps2-an386-freertos`). Test `smoke` passé
partout.

## 4. Essai fonctionnel

`env-8-r2-essai.sh` (journal : `oracles/env-8-r2-apres-final/essai-fonctionnel.log`), rootstock
jetable, lepton de la branche (venv), noyau 53ceb58 (clone d'essai sur une branche `essai-r2`, voir O14) :
application `demoopt` créée par `lepton scion new`, une option de chaque type (`OPT_INT` publique,
les autres privées), graine `{"demoopt": {OPT_BOOL: true, OPT_INT: 42, OPT_ENUM: "b", OPT_STR:
"dit \"bonjour\" C:\\temp"}}` ; `demoopt.c` complété par `const char demoopt_str[] = OPT_STR;` et un
`_Static_assert` sur la taille.

| Étape | Résultat |
| --- | --- |
| `lepton check` | code 0 (6 fichiers conformes) |
| `lepton generate` | 4 variables `LEPTON_OPTION_demoopt_*` dans `essai-debug-qemu` |
| Construction host + preset | code 0 |
| `compile_commands.json` | `demoopt.c` : `OPT_BOOL=1 OPT_ENUM=b OPT_INT=42 OPT_STR` ; aucune autre source ne porte `OPT_*` |
| Préprocesseur (commande de `compile_commands.json`, `-E`) | `const char demoopt_str[] = "dit \"bonjour\" C:\\temp";` = attendu ; `_Static_assert` passé |
| Fumée QEMU | passée |
| Graine `OPT_INT: 101`, `OPT_ENUM: "c"` | `check` code 1 (« 101 hors des bornes [1, 100] », « « c » absent des valeurs (a, b) ») ; `generate` code 1, rien écrit |
| Graine `OPT_STR: "a;b#c"` | `check` code 1 (« caractère(s) '#' ';' non transmissible(s) ») |
| `-DLEPTON_OPTION_demoopt_OPT_INT=101` / `OPT_ENUM=c` / `OPT_BOOL=peut-etre` / `OPT_STR=a#b` | configuration refusée (code 1), message citant le manifeste et la variable « (valeur fixée : graine ou -D) » |
| Retour à 42 | configuration code 0 |
| Trunk | aucun fichier régulier, aucun lien cassé |

Tests : `pytest` 125 verts (venv). `scripts/valider-schemas.sh` conforme. `scripts/bout-en-bout.sh`
(lepton de la branche, noyau `master` de `~/lepton`) : succès, rootstock de référence inchangé.

## 5. Résultat CFG-4

Conforme : options typées et documentées dans le manifeste ; valeurs fixables dans la graine ;
valeur hors bornes refusée par `lepton check`, `lepton generate` et la configuration CMake.

## 6. Observations

| ID | Constat | Suite (décision de l'utilisateur, 2026-10-16) |
| --- | --- | --- |
| O14 | `--origin LOC@VERSION` : `_ORIGIN` (`lepton/seed.py:31`) refuse `/` dans la version ; `@devenv/env-8-r2` reste collé à l'URL et `git clone` échoue (une branche à `/` ne peut pas servir d'origine ; scion range le clone sous `depots/<…>/<version>`) | renvoyé : ENV-8 (lepton) avec ENV-7 (scion) |
| O15 | Message CMake « (valeur de la graine) » aussi pour une valeur passée par `-D` | corrigé dans R2 (53ceb58) |
| O16 | Option `chaine` contenant `"` ou `\` : définition mal citée (défaut comme valeur de la graine, comportement antérieur pour le défaut) ; `;` et `#` non transmissibles | corrigé dans R2 : `"` `\` échappés, `;` `#` saut de ligne refusés (53ceb58, e7d695b) |
