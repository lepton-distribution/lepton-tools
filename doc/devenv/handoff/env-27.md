# Passation ENV-27 — TST-2 : tests fournis par un greffon — session du 2026-11-02

## Statut
terminée — un greffon déclare ses tests par le champ `tests` de son manifeste ; découverte par le
lecteur CMake du noyau ; test d'essai QEMU du BSP `qemu-mps2-an386` vert ; binaires inchangés.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` (fusion `--no-ff` de `devenv/env-27`, poussées toutes deux) | « Fusion de devenv/env-27 » ; fond : « devenv(env-27): état et passation » | oui |
| clone noyau `depots/lepton/original/master` | `master` 0c0cc4f (fusion de `devenv/env-27` 62ff71a, poussées) | « Fusion de devenv/env-27 (ENV-27 TST-2 : tests fournis par un greffon, PA-42) » | oui |
| `bsp-qemu-mps2-an386` | `master` 09f4943 (fusion de `devenv/env-27` 902b557, poussées) | idem | oui |
| graine `original-tree`, autres greffons | inchangés | | oui |
| `<ROOTSTOCK>` | regreffé (`lepton@bsp-qemu-mps2-an386`, 8 feuilles, dont `tests/`) ; `lepton check` code 0 (19 fichiers) ; trunk : seul fichier régulier `.scion.grafted.list`, 0 lien cassé | | oui |

Hors dépôts : copie d'essai `~/lepton-tools-dev/essais/env-27-copie` (dépôts et trunk copiés,
`third_party` lié), laissée **sans** le BSP an386 (`scion graft-remove`, sans `--purge`) : témoin
« rootstock sans le greffon d'essai » ; `<ROOTSTOCK>/build/` reconstruit à neuf pour `host` et les
16 presets croisés (oracle après) ; `<ROOTSTOCK>/build/env-27-port/<P>` : configurations des
10 presets de carte avec port série fictif (listes `ctest -N`) ; lepton réinstallé par pipx depuis
6880f61.

## Fait pendant la session
- Audit (`rapports/env-27-tst2.md` §1-§5) : déclaration des tests du noyau, `board.radio` déjà
  déclaré par le `CMakeLists.txt` du BSP WL55 (K1), presets de carte sans test sans port série (K3),
  imports de `smoke_lsh` par `realpath` (K4) ; formes A (convention), B (champ), C (liste).
- PA-41 (§6) puis oracle `oracles/env-27-avant/` (17 constructions, `ctest-N.txt`,
  `ctest-N-port.txt`).
- Noyau 62ff71a : `lepton_greffons_tests()`, `lepton_greffon_test()`, `_lepton_greffon_actif` ;
  un appel dans `CMakeLists.txt` racine. BSP an386 902b557 : `tests/peripheriques.py`
  (`ls /dev` : `ttys0`, `ttys1`, `eth0`). lepton-tools 6880f61 : schéma, exemples, `check`,
  modèles, `scion new --from` ; 7 tests écrits d'abord ; `pytest` 229 verts ;
  `env-8-interface.md` §19.
- Contrôles (§8) : `comparer-oracle.py` code 0 ×16, host identique ; `ctest -N` = avant +
  `qemu-mps2-an386.peripheriques` (4 presets an386), vert ; sans le greffon : listes inchangées ;
  squelettes vérifiés par `cmake -P`.
- PA-42 : fusions et push.

## Reste à faire dans l'étape
- Aucune tâche du fichier d'étape. Validation Debian : ENV-28 (P-2).

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-41 : champ `tests` (répertoire avec `CMakeLists.txt`, noyau exclu), `lepton_greffon_test`, types QEMU et carte, test QEMU neuf dans an386, squelettes `application` et `bsp` | utilisateur | oui |
| PA-42 : fusions et push | utilisateur | oui |
| P-1 : tâche de l'éditeur « tests des greffons » (`ctest -L greffon:`) par `lepton generate` | utilisateur (retenue, étape ultérieure non planifiée) | oui (prochaine action) |
| P-2 : validation Debian du champ `tests` en ENV-28 | utilisateur | oui |
| `bibliotheque` sans squelette ; `scion new --from` : tests du BSP source copiés, sinon squelette ; étiquette `qemu` ou `board` posée par le test | proposition de la session | `env-8-interface.md` §19 |

## Pièges rencontrés
- `pytest` complet dure ~7 min : au-delà du délai d'une commande au premier plan → lancer en
  arrière-plan ; ne pas modifier lepton-tools pendant une série en cours.
- `cmake --preset P -B <dir>` : le répertoire parent doit exister avant de rediriger le journal à
  côté (`mkdir -p`).
- Copie d'essai : `cp -RP depots trunk` ne copie pas `.scion.rootstock.signature` ni
  `.scion.trunk.tolerated` (fichiers cachés de la racine) : les copier aussi.
- Après `scion graft-remove`, `scion graft` ne regreffe pas le scion retiré (il n'est plus dans la
  liste greffée).
- `ls /dev` par `run_command` : l'écho de la commande reste dans la sortie (`ls`, `/dev` parmi les
  mots) ; sans effet sur un contrôle de présence.

## Critères de validation
- [x] PA-41 et PA-42 tranchés et consignés.
- [x] Tests du greffon d'essai découverts sans configuration de la graine, et exécutés avec succès.
- [x] `comparer-oracle.py` code 0 sur 17 constructions (16 ELF ; host par ses empreintes et
  `ctest`) ; tests existants inchangés.
- [x] Modification du lecteur limitée à la découverte : constat dans le rapport (BLD-6, §7).

## Reprise
Commande ou première action de la session suivante :
```
démarre la session   # skill devenv-session ; ENV-28 (etapes/ENV-28-validation-debian.md), consigne jusqu'au PA-43
```
