# Reprise 3 — ENV-8 O3, O4, O14 + ENV-6 O1

Reprise n° 3 du bilan ENV-11 (`env-11-bilan.md` §3) : O3, O4 (ENV-8), O1 (ENV-6), avec O14
(`env-8-r2-options.md` §5, joint à la reprise par décision de l'utilisateur). Session du
2026-10-16, branches `devenv/env-8-r3` (lepton-tools) et `devenv/env-6-r3` (clone noyau), depuis
`main` b9dd0e8 et `master` 50a67c0 (fusions de `devenv/env-8-r2`).

## 1. Décisions (utilisateur, 2026-10-16)

| Sujet | Décision |
| --- | --- |
| O14 | Joint à la reprise ; vérifier d'abord scion 0.5.1.1, arrêt PA-8 si scion doit changer |
| O4 | Avertir (CFG-5) et continuer : retrait fait, code 0 |
| Non-régression O1 | Référence `oracles/env-8-r2-apres-final/` (même arbre que `master` 50a67c0) ; capture `oracles/env-8-r3-apres/` |
| Branches | `devenv/env-8-r3` (lepton-tools), `devenv/env-6-r3` (clone noyau) |

## 2. Corrections

| ID | Dépôt | Commit | Correction |
| --- | --- | --- | --- |
| O3 | lepton-tools | bfa6ec5 | `lepton/scions.py` `_left_state` : après un échec de l'ajout, l'état laissé est lu sur disque (`.scion.sources.list`, liste greffée, `lepton-graine.json`) : « hors graine (`lepton seed add …`) » ; « greffon ajouté à la graine (corriger la cause, puis `lepton graft`) » si l'échec suit l'ajout (contrôle du trunk, reconfiguration CMake) ; sinon « annulation incomplète » avec ce qui reste et la commande de retrait adaptée (`lepton seed remove`, `scion seed-scion-remove`, ou édition de la graine). Une erreur sans action ne produit plus « None ; ». |
| O4 | lepton-tools | 9d851b3 | `lepton/checks.py` `removal_unprovided` : CFG-5 sur le XML de la graine avec et sans le greffon retiré ; `seed_remove` (donc `seed remove` et `scion remove`) avertit, avant la reconfiguration CMake, de chaque déclaration que seul ce greffon fournissait ; les anomalies antérieures ne sont pas répétées. |
| O14 | lepton-tools | 40ea155 | `lepton/seed.py` `_ORIGIN` : `/` admis dans VERSION (`@devenv/x`) ; l'autorité d'une URL (`scheme://user@hôte`) appartient à LOCATION ; version à segment vide, `.` ou `..` refusée (le clone est rangé sous `depots/<étagère>/<préfixe>/<version>`). |
| O1 | clone noyau | aee4618 | `scion/CMakeLists.txt` : `LEPTON_BOARD` sans manifeste BSP de ce nom ni module `cmake/boards/<nom>.cmake` → `FATAL_ERROR` nommant le BSP manquant, au lieu de l'échec indirect de `include(boards/<nom>)`. |

O14, vérification de scion 0.5.1.1 (aucune évolution, pas de PA-8) : `ScionRef.version` compose le
chemin du clone (`scion/graft.py:59`, `:422`), `git clone -b <version>` puis `checkout` acceptent
une branche à `/`, et `graft-remove --purge` supprime les répertoires parents vides jusqu'à
`depots/` (`scion/graft.py:410`). Prouvé par `test_gra3_version_with_slash` (add, status, lock,
lock --verify, remove --purge) et par l'essai réel §4.

Analyse retenue pour O14 : élargir seulement la classe de VERSION (`[^@:/]` → `[^@:]`) aurait lu
`https://user@hôte/x.git` comme LOCATION `https://user`, VERSION `hôte/x.git` ; d'où l'autorité
isolée dans l'expression. La forme scp (`git@hôte:org/x.git`, sans schéma) n'est pas gérée, comme
avant (hors périmètre, non signalée par un essai).

## 3. Non-régression d'O1 (skill `lepton-oracle`)

Mêmes commandes qu'en R2 : `scripts/oracle/rejouer-oracle.sh ~/lepton oracles/env-8-r3-apres
--qemu …×6 --carte …×8` (noyau aee4618), comparaison avec `oracles/env-8-r2-apres-final/` (noyau
53ceb58, arbre identique à `master` 50a67c0).

| Preset | Sections/symboles | Empreinte | Fumée | Banc KAL | Écarts expliqués |
| --- | --- | --- | --- | --- | --- |
| host | – | – | – | ctest 7/7 = 7/7 ; mklepton identiques | – |
| qemu-mps2-an386-embos | identiques | différente | passée (E2) | 18/18 = 18/18 | E1 |
| qemu-mps2-an386-embos-soft | identiques | différente | passée (E2) | 14/14 = 14/14 | E1 |
| qemu-mps2-an386-freertos | identiques | différente | passée (E2) | 18/18 = 18/18 | E1 (démontré) |
| qemu-mps2-an386-freertos-soft | identiques | différente | passée (E2) | 14/14 = 14/14 | E1 |
| qemu-mps2-an500-embos | identiques | différente | passée (E2) | 18/18 = 18/18 | E1 |
| qemu-mps2-an500-freertos | identiques | différente | passée (E2) | 18/18 = 18/18 | E1 |
| nucleo-f429zi-embos / -freertos | identiques | différentes | – | – | E1 |
| nucleo-wl55jc1-embos / -freertos | identiques | différentes | – | – | E1 |
| stm32f746g-disco-embos / -freertos | identiques | différentes | – | – | E1 |
| samd21-xplained-pro-embos / -freertos | identiques | différentes | – | – | E1 |

`comparer-oracle.py` : code 0 sur les 14 presets croisés. Banc KAL : lignes `Test #` identiques
(durées ignorées) sur les 6 presets QEMU.

**E1** — empreintes différentes, sections et symboles identiques : date de construction embarquée
(`env-8-r2-options.md` §3 E1). Démonstration : `REVS="50a67c0 aee4618"
env-8-r2-preuve-empreintes.sh <copie>` (copie de `~/lepton` sans `build/`, `SOURCE_DATE_EPOCH=1760536800`,
an386-freertos construit à neuf) → `lepton.elf` `3ed42761…`, `lepton.bin` `76cc90b1…`,
`lepton.hex` `0f353cc4…` **identiques** aux deux commits. (Valeurs différentes de celles de R2 :
autre copie, chemins de débogage différents ; seule la comparaison dans une même copie vaut.) Le
changement ne touche qu'une branche d'erreur de la configuration : aucun effet sur les binaires,
comme attendu.

**E2** — `fumee.log` identiques après avoir ignoré les horodatages, les adresses, le jeton aléatoire
de l'essai UART (`lepton-uart1-<n>` et le chiffre de fin du jeton que la console renvoie devant
l'invite suivante), la ligne asynchrone `rcv SIGCHLD` et les lignes vides. Test `smoke` passé
partout.

## 4. Essais

| Essai | Résultat |
| --- | --- |
| O14 : `lepton seed new o14` (rootstock jetable du scratchpad), `--origin lepton-noyau=file://localhost~/lepton/depots/lepton/original/master@devenv/env-6-r3`, famille et BSP `@master` | code 0 ; clone `depots/lepton/original/devenv/env-6-r3` sur la branche `devenv/env-6-r3` ; `seed status` (version et branche `devenv/env-6-r3`) ; `check` : 5 fichiers conformes ; `seed lock` puis `--verify` conformes ; trunk sans fichier régulier ni lien cassé |
| O1 : même rootstock, noyau mis à aee4618, `scion graft-remove lepton@bsp-qemu-mps2-an386`, `cmake --preset qemu-mps2-an386-freertos` | code 1 ; première erreur : `CMakeLists.txt:49` « LEPTON_BOARD=qemu-mps2-an386 : aucun greffon BSP de ce nom greffé (manifeste lepton-greffon.json de nom « qemu-mps2-an386 »), ni carte transitoire cmake/boards/qemu-mps2-an386.cmake. Greffer le BSP de la graine (lepton check). » (journal `oracles/env-8-r3-apres/essai-o1.log`) ; `lepton check` code 1 (GRA-2, CFG-5) |
| O3, O4 | `test_o3_*` (3, `tests/test_milestone4.py`), `test_cfg5_scion_remove_*` (2, `tests/test_milestone6.py`) |
| Ensemble | `pytest` 131 verts (125 + 6), 132 avec O17 ; `scripts/valider-schemas.sh` conforme ; `scripts/bout-en-bout.sh` (lepton de la branche) succès, `~/lepton` inchangé ; trunk de `~/lepton` : 4 037 feuilles, aucun fichier régulier ni lien cassé |

## 5. Observation relevée pendant la reprise

| ID | Constat | Décision |
| --- | --- | --- |
| O17 | `lepton seed status` (texte) : colonnes version (8) et branche (16) de largeur fixe, décalées par une version ou une branche longue (`devenv/env-6-r3`) ; `--json` non concerné | corrigé dans R3 (décision de l'utilisateur) : 9d2cc85, largeurs calculées d'après le contenu (minimums inchangés) ; `test_gra6_status_columns_fit_long_version` (échoue sans la correction) ; essai réel aligné |

## 6. Conclusion

Non-régression d'O1 validée par l'utilisateur (2026-10-16). O1, O3, O4, O14, O17 corrigés ;
`pytest` 132 verts. Reprise 3 terminée ; fusions de `devenv/env-8-r3` (lepton-tools) et
`devenv/env-6-r3` (clone noyau) au début de la session suivante.
