# Passation ENV-44 — Résidus d'ENV-37 à ENV-43 — session du 2026-11-09

## Statut
terminée — D1, D2, D3, D5, D6, D7 et D9 sont traités et prouvés (`rapports/env-44-residus.md`).
D1 a révélé un défaut de scion, corrigé et publié en 0.6.2.0. PA-75 et PA-76 sont tranchés, tout
est publié.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` | fusion de `devenv/env-44` (poussée, ainsi que la branche) | oui |
| seed.scions | `master` | 7e8a0cc Fusion de devenv/env-44 (scion 0.6.2.0 …) ; tag `0.6.2.0` sur 213d2c0, publié | oui |
| clone noyau `depots/lepton/original/master` | `master` | cde728f Fusion de devenv/env-44 (provenance CMSIS V3.30, `SCION_REF` 0.6.2.0) | oui |
| `bsp-qemu-mps2-an386` | `master` | 10a8889 Fusion de devenv/env-44 (`ARMCM4_FP.h`) | oui |
| familles F4, F7, WL ; graine | `master` / `original-tree` | 7afd7f1, d2d9aa9, 2340b25 ; 15740f9 (non touchés) | oui |

`<ROOTSTOCK>` :
- 3983 liens (+1 : `ucore/cmsis/LEPTON-PROVENANCE.md`), 0 lien cassé, fichiers réguliers tolérés
  seulement ;
- `lepton check` code 0 ;
- tous les clones sur `master`.

Outils sur le Mac : scion 0.6.2.0 (pipx depuis le tag), lepton 0.1.0, qui exige 0.6.2.0. Sur la VM,
scion est encore en 0.6.1.0.

Oracle de référence Mac : `oracles/env-44-apres/`.

Cartes : la NUCLEO-F429ZI est sur le Mac, flashée avec `nucleo-f429zi-embos` du Mac. Les WL55 A et B
n'étaient pas visibles par USB.

## Fait pendant la session
- **Audit** (rapport §1) puis **PA-75**.
  - Proposition de la préparation écartée : clore D2 « sans objet ». gdb rend `fullname` = clone
    tiers, ce qui sollicite la table.
- **Oracle avant** : code 0 ×16 contre `env-42-apres`, mklepton identiques, `ctest -N` 17/17.
- **D9** : règle « Remise en échec » d'ORCHESTRATION §2bis.
- **D3** : hook par commande simple. Les 42 cas de l'audit passent de 14 écarts à 0.
  `tests/test_proteger_trunk.py` compte 118 cas. Mises à jour de §5bis, `CLAUDE.md` et de la skill
  `lepton-rootstock`.
- **D6** : `compiler-hal-f4-a-blanc.sh` sans l'ordre `v330`, code 0.
- **D5** : BSP an386 sur `cmsis-5/…/ARMCM4_FP.h`. L'objet `qemu_mps2_board.c` est identique octet
  pour octet (`d5-objet.py`). Dans l'oracle après, seules `.debug_*` changent, et les journaux sont
  identiques.
- **D7** : `kernel/core/ucore/cmsis/LEPTON-PROVENANCE.md`, puis `scion graft --scion
  lepton@original::tree`.
- **D1** :
  - essais A (`seed replace`) et B (`seed add` puis `seed remove`) sur des copies ;
  - défaut de scion 0.6.1.0 ;
  - scion 0.6.2.0 (P-G6, 3 tests, 269 réussis) ;
  - lepton : `SCION_MIN_VERSION` 0.6.2.0, `SCION_REF`, test `seed replace` ; 362 tests pytest
    réussis ;
  - essais rejoués, conformes.
- **D2** :
  - contrôle scripté (`d2-table.py`) ;
  - gdb sur la carte (`d2-gdb-carte.sh`) ;
  - essai VSCodium par l'utilisateur : l'onglet de `stm32f4xx_hal_gpio.c` est le chemin du trunk.
- **Publication (PA-76)** : seed.scions, noyau, BSP an386, lepton-tools.
- **Nettoyage** : rootstocks d'essai `essais/env-44-d1-*` supprimés.
- **`HORS-PLAN.md`** : D1 à D3, D5 à D7 et D9 renvoient au rapport ; D10 ajouté.

## Reste à faire dans l'étape
- [x] Rien. Point ajouté hors plan : D10 (lepton ne relaie pas les messages de scion lors de
  `seed add`, `seed replace` et `seed remove`).

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-75 : D1 à D9 selon le rapport §2 (tout défaut corrigé ici, lepton comme scion) | utilisateur | oui |
| D1 : correctif dans scion 0.6.2.0 (P-G6) plutôt que dans lepton seul | utilisateur | oui |
| D2 : coupure d'alimentation de la carte pour lever le reset bloqué | utilisateur | oui |
| PA-76 : publication complète, essais D1 supprimés, nouvel oracle de référence `env-44-apres` | utilisateur | oui |
| ENV-50 : installer scion 0.6.2.0 sur la VM avant toute regreffe (la consigne R50-1 doit le dire) | proposition non validée | non |
| D10 : faire relayer par lepton les messages d'information de scion (`-v` ou toujours) | proposition non validée | non (HORS-PLAN) |

## Pièges rencontrés
- **Reset bloqué de la NUCLEO-F429ZI.**
  - Symptômes : la carte revenait de la VM. Cortex-Debug affichait « Protocol error with Rcmd: FC »
    (`monitor reset halt`). Une fois, OpenOCD a planté au `load` sur l'assertion
    `stm32f2x.c:1221` (taille de flash lue 0x2003).
  - Cause : le `reset halt` par NRST expirait (3 fois sur 3), alors que le reset logiciel marchait.
  - Parade : couper l'alimentation de la carte, remesurer le `reset halt`, puis vérifier l'image par
    `verify_image`. Voir la skill `lepton-cibles`, section Pièges.
- **Arrêt inattendu dans `sbin/ls.c:107`** au premier lancement VSCodium : cause non établie
  (O-4).
- **URL `file://` sans hôte** : lepton la lit comme un chemin local. Utiliser `file://localhost/…`.
- **Nouveau hook** : deux faux positifs, corrigés pendant la session (`$` dans un mot, heredoc d'un
  script Python). La limite reste : le contenu d'un script exécuté n'est pas lu.
- **Empreintes `.bin`** : elles diffèrent à chaque reconstruction, car l'heure de compilation est
  incluse dans l'image. Seules comptent les sections et les symboles.
- **Test de version de seed.scions** : il était resté à `0.6.0.0` en 0.6.1.0 (O-1). Lancer toute la
  suite (`python3 -m unittest discover -s tests`) avant de taguer.

## Critères de validation
- [x] PA-75 et PA-76 tranchés et consignés.
- [x] Chaque point D1, D2, D3, D5, D6, D7, D9 corrigé, essayé ou clos, avec sa preuve au rapport.
- [x] Binaires : code 0 hors an386 ; an386 dans le critère du PA-75 (`.debug_*` seuls).
- [x] `HORS-PLAN.md` : chaque point traité marqué, avec renvoi au rapport.

## Reprise
Commande ou première action de la session suivante :
```
démarre la session ENV-45 (skill devenv-session) ; rebrancher les NUCLEO-WL55JC1 A et B avant les
essais de sonde ; si Cortex-Debug échoue sur « Rcmd: FC », couper l'alimentation de la carte
```
