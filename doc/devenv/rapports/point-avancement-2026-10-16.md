# Point d'avancement — environnement de développement Lepton

État au 16 octobre 2026 · export de la page partagée
[Point d'avancement chantier Lepton](https://claude.ai/code/artifact/7726206d-1507-4ddc-867f-230694845a9a)
(la page en ligne fait foi si elle a été modifiée depuis)

12 étapes sur 13 sont terminées et 3 des 5 lots de corrections issus de la validation finale sont faits. Restent les reprises 4 et 5, puis la décision PA-12 de lancer ou non l'extension VSCodium (ENV-12).

## Étapes du plan

Les étapes ENV-0 à ENV-11 sont terminées entre le 12 et le 15 octobre 2026. ENV-12 n'est lancée que sur décision (PA-12) : la validation de bout en bout a conclu que la phase 1 suffit, avec des écarts acceptés.

| Étape | Objet | Statut |
| --- | --- | --- |
| ENV-0 | Cadrage (emplacements, oracle de départ) | terminée le 12/10 |
| ENV-1 | Levée des risques éditeur (clangd, liens, GDB, git multi-racines) | terminée le 12/10 |
| ENV-2 | Audit de l'existant | terminée le 13/10 |
| ENV-3 | Schémas (manifestes JSON, XSD mklepton) | terminée le 13/10 |
| ENV-4 | Format XML 2 de mklepton | terminée le 13/10 |
| ENV-5 | Restructuration CMake du greffon noyau | terminée le 13/10 |
| ENV-6 | Greffons famille et BSP (QEMU, NUCLEO-F429ZI, NUCLEO-WL55JC1) | terminée le 13/10 ; reprise 3 le 16/10 |
| ENV-7 | Évolutions génériques de scion (0.5.1.0) | terminée le 13/10 ; reprise 1 le 15/10 (0.5.1.1) |
| ENV-8 | Outil en ligne de commande `lepton` | terminée le 14/10 ; reprises 2 et 3 le 16/10 |
| ENV-9 | Fichiers générés pour VSCodium (presets, espace de travail) | terminée le 14/10 ; reprise 4 à faire |
| ENV-10 | Script d'installation VSCodium (Mac Intel, Debian 13) | terminée le 15/10 ; reprise 5 à faire |
| ENV-11 | Validation de bout en bout (Mac, cartes, VM Debian) | terminée le 15/10 |
| ENV-12 | Extension VSCodium (phase 2) | à faire, sous réserve de PA-12 |

## Reprises du bilan ENV-11

Les défauts (N, D) et observations (O) du bilan ENV-11 sont traités en 5 reprises bornées, chacune sur une branche `devenv/env-<N>-r<k>`, avant PA-12. Les reprises 1 à 3 sont faites.

| # | Étape | Contenu | Statut |
| --- | --- | --- | --- |
| 1 | ENV-7 | N1 : scion clonait un greffon sans se placer sur la version demandée | terminée le 15/10 (scion 0.5.1.1) |
| 2 | ENV-3, 5, 8 | N5 : valeurs d'options fixées dans la graine, contrôlées par `lepton` et CMake (CFG-4 conforme) | terminée le 16/10 |
| 3 | ENV-8, ENV-6 | O3 message de reprise de `scion new` ; O4 avertissement au retrait d'un greffon ; O14 version d'origine contenant « / » ; O17 colonnes de `seed status` ; O1 message CMake si le BSP manque | terminée le 16/10, fusions locales à faire |
| 4 | ENV-9 | N4, O8, O10, O11 (fichiers de l'éditeur) | à faire |
| 5 | ENV-10 + noyau | D3, D4, O6, O12, O9 (installation), un passage VM Debian | à faire |

Chaque modification du système de construction a été vérifiée par un oracle de non-régression sur 15 configurations (sections et symboles identiques, banc de tests KAL identique), validé par l'utilisateur.

## Reste à faire

Deux reprises restent : la 4 sur les fichiers générés pour l'éditeur, la 5 sur les scripts d'installation, conclue par un passage sur la VM Debian.

| Reprise | ID | Problème | Exigence touchée |
| --- | --- | --- | --- |
| 4 | N4 | Aucune association de schémas dans l'éditeur : XML mklepton et manifestes JSON non validés à la saisie | CFG-7 (non conforme) |
| 4 | O8 | Numéro de série de la sonde absent de l'espace généré : deux cartes branchées se confondent | DBG-3 |
| 4 | O10 | clangd démarre avant la configuration CMake, sans base de compilation, navigation inopérante | IDE-3 (réserve) |
| 4 | O11 | Sélecteur de preset masqué par défaut dans la barre d'état | IDE-5 (réserve) |
| 5 | D3 | xmllint installé par aucun script : XML mklepton non validé par `lepton check` | INS-3 |
| 5 | D4 | Pas de clangd LLVM installé sur Debian | INS-3 |
| 5 | O6 | `LEPTON_EMBOS_ROOT` non transmis à un rootstock neuf | INS-3 |
| 5 | O12 | lepton non réinstallé quand la version est égale | INS-6 |
| 5 | O9 | Bloc Python de `gdbinit-lepton` refusé par le GDB Arm du Mac | DBG-3 |

La reprise 4 demande une validation dans VSCodium avec l'utilisateur et un essai avec les deux cartes branchées (O8).

## Écarts acceptés et décisions en attente

Quatre sujets sont acceptés en phase 1 mais restent à trancher, au plus tard en PA-12.

| Sujet | Constat | Se décide en |
| --- | --- | --- |
| CFG-1 (O5) | Le XML mklepton est porté par le greffon noyau, pas par la graine : modifier les applications d'un projet touche un greffon partagé | conception, ENV-8 ou ENV-12 |
| O2 | `lepton seed new` ne crée qu'une configuration | ENV-8 ou ENV-12 |
| IDE-4 (PA-1) | Au débogage, le source s'affiche sous le chemin du clone et non du trunk | éventuellement ENV-12 |
| R1 (ENV-9) | Après un changement de preset, les fichiers déjà ouverts gardent l'ancienne commande de compilation | ENV-12 |

## Reports hors reprises

Ces sujets sont consignés dans l'état du chantier mais n'ont aucune échéance.

- **BSP `nucleo-f439zi`** : nominal pour le portage, reporté après ENV-6 (la carte de validation est la NUCLEO-F429ZI).
- **Cartes transitoires STM32F746G-DISCO et SAMD21 Xplained Pro** : encore décrites dans le greffon noyau (`cmake/boards`), non extraites en greffons BSP.
- **Dimensionnement automatique de cpufs** : implémenté en ENV-4, utilisé par aucun des 6 XML ; essai sur cartes à décider.
- **Hôte Apple Silicon** : scripts relus, jamais exécutés.
- **Exigences P2 non testées** : BLD-6, IDE-6, DBG-4, DBG-5, TST-2 (phase 2 ou ENV-12).

## Dépôts et publication

Les trois dépôts du chantier sont à jour sur GitHub depuis le 16/10, reprise 3 comprise sur ses branches ; seule la fusion de la reprise 3 dans `main` et `master` reste locale à faire.

| Dépôt | Sur GitHub | Reste local |
| --- | --- | --- |
| seed.scions (scion) | `master` f1d1f3c + tag 0.5.1.1, poussés le 16/10 | — |
| lepton-tools | `main` b9dd0e8 (reprise 2 comprise) + `devenv/env-8-r3`, poussés le 16/10 | fusion de la reprise 3 dans `main` |
| greffon noyau (lepton-original-tree.scions) | `master` 50a67c0 (reprise 2 comprise) + `devenv/env-6-r3`, poussés le 16/10 | fusion de la reprise 3 dans `master` |
| famille `qemu-mps2`, BSP `qemu-mps2-an386` | `master`, poussés le 15/10 | — |

Les fusions de la reprise 3 seront à pousser avant le passage VM de la reprise 5 ; chaque push reste soumis à accord (PA-P).

## Chemin restant

Quatre temps mènent à la décision PA-12, chacun en session distincte.

1. **Fusions de la reprise 3** puis **reprise 4** (ENV-9) : probablement deux sessions, l'une en ligne de commande, l'autre de validation VSCodium et cartes avec l'utilisateur.
2. **Push** des fusions de la reprise 3, sur accord (PA-P).
3. **Reprise 5** (ENV-10 et noyau) : une session sur le Mac, puis une session sur la VM Debian.
4. **PA-12** : bilan des fonctions encore manquantes et de leur coût, avec les sujets en attente ci-dessus ; décision de lancer ENV-12 ou de clore à la phase 1.

Sources : `doc/devenv/DEVENV-STATUS.md`, `doc/devenv/rapports/env-11-bilan.md`, `doc/devenv/rapports/env-8-r3.md` (dépôt lepton-tools, branche `devenv/env-8-r3`).
