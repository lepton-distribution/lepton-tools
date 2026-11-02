# Passation ENV-24 — Dimensionnement automatique du cpufs — session du 2026-11-02

## Statut
terminée — les 5 XML des presets laissent mklepton dimensionner le cpufs au plus juste ; écarts de
l'oracle limités à l'image cpufs ; QEMU et les 4 cartes conformes, réseau et radio compris.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` (fusion `--no-ff` de `devenv/env-24`, poussées toutes deux) | « Fusion de devenv/env-24 » ; fond : « devenv(env-24): état et passation » | oui |
| clone noyau `depots/lepton/original/master` | `master` 0bdce87 « Fusion de devenv/env-24 (ENV-24 cpufs dimensionné automatiquement, PA-36) » = origin ; `devenv/env-24` f3ecf8c poussée | | oui |
| graine `depots/lepton-seed.scions/original-tree`, familles, BSP | inchangés | | oui |
| `<ROOTSTOCK>` | trunk : 0 fichier régulier, 0 lien cassé ; `lepton check` code 0 (19 fichiers) | | oui |

Cartes : images `*-embos` d'ENV-24 en flash (F429, F746, WL55 A et B, SAMD21), « Verified OK ».
Répertoires de construction des presets carte reconfigurés avec `LEPTON_BOARD_SERIAL_PORT` (et
`LEPTON_NET_TEST_HOST_IP`, sondes WL55) : hors trunk, sans effet sur `lepton.elf` (recapture 0 écart).

## Fait pendant la session
- Audit : `rapports/env-24-cpufs.md` §1 (tailles calculées : 5939 o / 22 nœuds pour qemu, F439,
  F746 ; 1755/17 WL55 ; 1706/15 SAMD21 ; 41399/50 Olimex ; image `const` en `.text` ;
  `dev_cpufs_write` renvoie −1 ; aucun test n'écrit sous `/usr`).
- Oracle avant `rapports/oracles/env-24-avant/` = `env-20-apres` (16 presets code 0).
- Clone noyau : contrôle de cohérence de `mklepton_format_check.cmake` (1d1db90, f3ecf8c) ;
  5 lots XML + empreintes (7f3dd51…816715b) ; `doc/migration/mklepton.md` (7a32352).
- Oracles partiels `env-24-lot-*` et oracle après `env-24-apres` : écarts classés cpufs (§4, §5).
- QEMU : fumée identique (filtre E-4), banc 18/18 et 14/14 même liste.
- Cartes (§6) : F429 20/20 (f429zi embOS et FreeRTOS, f439zi embOS) ; F746 20/20 (×2) ;
  WL55 16/16 (×2, radio 20/20 dans les deux sens) ; SAMD21 embOS 15/15, FreeRTOS banc 14/14 et
  fumée E-5 identique à ENV-19.
- PA-36 : fusions et push (lepton-tools `main` et `devenv/env-24` ; noyau `master` et `devenv/env-24`).

## Reste à faire dans l'étape
- Aucune tâche du fichier d'étape. Validation Debian du cpufs automatique : ENV-28.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-35 : 5 XML des presets, Olimex conservé, contrôle de cohérence, critère P-4, graines d'essai hors périmètre, doc `mklepton.md`, 4 cartes accordées | utilisateur | oui |
| Amendement de P-4 : sections `.debug_*` admises si leur écart est celui de `dev_dskimg.o` | utilisateur | oui |
| `board.net` (F429, F746) et `board.radio` (WL55) ajoutés aux essais | utilisateur | oui |
| PA-36 : fusion et push | utilisateur | oui |
| Un commit de génération d'empreintes par lot (consistance de chaque commit) | proposition de la session | rapport §4 |
| Binaire `nucleo-f439zi-embos` essayé sur la F429 (comme ENV-20) | proposition de la session | rapport §6 |
| Images d'ENV-24 (et non d'avant ENV-24, disparues) remises en flash | proposition de la session | rapport §6, §7 |

## Pièges rencontrés
- zsh ne découpe pas une variable contenant plusieurs arguments : `rejouer-oracle.sh $args` a reçu
  un seul argument (« argument inconnu »), rien construit → tableau bash (`bash -c`, `"${args[@]}"`).
- Constructions `--carte` de l'oracle : `kal_bench.elf` absent tant que `LEPTON_BOARD_SERIAL_PORT`
  n'est pas configuré → `kal.board_flash` « couldn't open » ; reconfigurer puis `cmake --build`.
- `ctest --output-log` ne contient pas le détail : copier `Testing/Temporary/LastTest.log`.
- Réseau : l'hôte doit être en 192.168.2.10 sur l'interface du câble (`en0`), câble branché ; une
  adresse sur une autre interface (`en17`, route /24 plus précise) détourne le trafic ;
  `route -n get 192.168.2.5` avant tout essai.
- Ports série réénumérés au changement de carte (F746 : `1454403` → `1454303`) : relever
  `ls /dev | grep cu.usbmodem` à chaque branchement ; WL55 : port déduit du Location ID de la sonde.
- Hook `proteger-trunk.py` : une commande combinant un chemin du trunk (lecture d'une cfg) et une
  redirection est refusée ; désigner la cfg par son chemin réel dans le clone (`realpath`).
- `source lepton-env.sh` lit `$1` : ne pas le sourcer dans un script qui a des arguments
  positionnels (avertissement « aucun rootstock au-dessus de -FS »).

## Critères de validation
- [x] PA-35 et PA-36 tranchés et consignés.
- [x] XML retenus sans `size` ni `node` ; `host.mklepton_empreintes` vert avec la nouvelle référence.
- [x] Écarts de l'oracle limités à l'image cpufs, chacun classé dans le rapport.
- [x] Fumée et banc KAL identiques sur QEMU et sur les cartes accordées.

## Reprise
Commande ou première action de la session suivante :
```
démarre la session   # skill devenv-session ; ENV-25 (etapes/ENV-25-dbg5-mklepton.md), audit jusqu'au PA-37
```
