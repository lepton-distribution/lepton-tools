# Passation ENV-13 — Graine de référence publiée — session du 2026-10-30

## Statut
terminée — la graine `original-tree` publiée est le point d'entrée de l'arbre complet (noyau + 7
greffons famille et BSP sur GitHub) ; `<ROOTSTOCK>` est regreffé sans régression.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` (fusion cbfc562 de `devenv/env-13`, poussées toutes deux) | commit d'état après la fusion, sur cbfc562 « Fusion de devenv/env-13 » | oui |
| clone noyau `depots/lepton/original/master` | `master` 16a331b = `origin/master` | non touché | oui |
| graine `depots/lepton-seed.scions/original-tree` | `original-tree` 0f1275a « Fusion de devenv/env-13 » = `origin/original-tree` (poussée) ; `devenv/env-13` 9d72b6b, locale | pushurl SSH | oui |
| 7 greffons `depots/lepton/family-<nom>/master`, `depots/lepton/bsp-<nom>/master` | `master` = `origin/master` (3954357, 046779e, e98a482, 01b5528, 8ea7ee5, 1eccc2f, a329f4d) | clones neufs, pushurl SSH | oui |
| anciens `depots/lepton-famille/*`, `depots/lepton-bsp/*` | supprimés | archive `essais/archives/lepton-anciens-clones-famille-bsp-20261030.tar.gz` | — |

## Fait pendant la session
- PA-13 : séquence de regreffe établie dans le code de scion (`sync` ne retire aucune clé) et
  éprouvée sur une copie, dont le trunk est identique au réel (rapport §2).
- Graine : commit 9d72b6b (7 clés `family-`/`bsp-`, `master`, `https://`), fusionné dans
  `original-tree` (0f1275a) et poussé (`git ls-remote`).
- `<ROOTSTOCK>` regreffé : 9 entrées, 0 lien cassé, 0 lien vers les anciens clones, trunk
  identique à l'état de départ (SHA-256 des 4037 cibles).
- Oracle `env-13-avant` / `env-13-apres` (host + 14 presets, `rejouer-oracle.sh`) :
  `comparer-oracle.py` code 0 partout ; banc KAL et fumée identiques ; E1 démontré
  (`rapports/env-13-preuve-empreintes.sh`, `oracles/env-13-apres/preuve-e1.log`).
- Anciens clones vérifiés (0 commit non publié), archivés puis supprimés.
- Rootstock vierge `~/lepton-tools-dev/essais/env-13-vierge` greffé depuis GitHub ;
  `qemu-mps2-an386-freertos` : ctest 18/18 (fumée comprise) ; écart E3 expliqué (chemin du
  rootstock dans `__FILE__`).
- Rapport complet : `doc/devenv/rapports/env-13-graine.md`.

## Reste à faire dans l'étape
- Aucune tâche du fichier d'étape.
- Fait après la clôture, à la demande de l'utilisateur (PA-P) : `devenv/env-13` fusionnée dans
  `main` (cbfc562) ; `main` et `devenv/env-13` poussées.
- Fait après la clôture, à la demande de l'utilisateur : graines de `essais/env-9` et
  `essais/env-11/{qemu,qemu-gra2,f429zi,wl55jc1}` repointées sur GitHub (greffons famille/BSP ;
  `original::tree` reste en `file://` vers `<ROOTSTOCK>`) ; `origin` des clones en `https://`.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-13 : séquence validée ; accord PA-P pour la regreffe réelle ; `.DS_Store` conservés (`--force`) ; oracle sur les 15 répertoires (host compris) | utilisateur | oui |
| PA-14 : push de la graine avec pushurl SSH ; anciens clones archivés puis supprimés ; rootstock vierge `essais/env-13-vierge` ; copies d'essai supprimées | utilisateur | oui |
| Commit de graine fait dans la copie et rapatrié par `git fetch` (même hash) ; fusion `--no-ff` dans `original-tree` (convention d'ENV-6) | proposition de la session (annoncée au PA-13) | oui (PA-13) |
| Preuve E1 étendue à `nucleo-wl55jc1-freertos` ; capture `oracles/env-13-vierge/` | proposition de la session | non (rapport seulement) |

## Pièges rencontrés
- Trunk de `<ROOTSTOCK>` avec 24 `.DS_Store` du Finder → `graft-remove` et `graft` refusent
  (`_check_stray`) → `--force`, qui les conserve.
- Ancien clone `lepton-bsp/qemu-mps2-an500` avec `.DS_Store` ignorés sous `scion/` → regreffe en
  conflit avec le noyau (« sys/.DS_Store : déjà fourni par original::tree »), annulée par scion → les
  supprimer du clone (fait dans la copie de preuve seulement ; clone depuis supprimé).
- `comparer-oracle` entre deux rootstocks de chemins différents : code 1 (`.text` et sections de
  débogage), à cause des `__FILE__` absolus (E3). Comparer dans le même rootstock.
- `scion seed-clone` n'est pas neutre sur un rootstock où un greffon a été volontairement
  dégreffé (`essais/env-11/qemu-gra2`, GRA-2) : il réinscrit l'entrée dans la liste greffée →
  `graft-remove` de cette clé (0 feuille). Pour contrôler une graine, préférer une copie.
- Le hook `proteger-trunk.py` refuse aussi une commande qui ne fait que lire un fichier du trunk
  avec `cp` → relever une empreinte (`shasum <`) au lieu de copier.
- Le piège prévu par le fichier d'étape (chemin du clone dans le débogage) ne se produit pas : le
  compilateur reçoit les chemins du trunk.

## Critères de validation
- [x] PA-13 et PA-14 tranchés et consignés.
- [x] Graine : 7 clés `family-`/`bsp-`, version `master`, URL `https://` ; `original::tree` et
      `building` inchangés ; 4 commits d'ENV-6 conservés.
- [x] 7 clones sous `depots/lepton/<clé>/master` au commit de la table ; pushurl SSH.
- [x] Trunk : 0 fichier régulier (hors 24 `.DS_Store`, PA-13), 0 lien cassé, 0 lien vers les
      anciens clones.
- [x] `comparer-oracle.py` code 0 sur les 14 presets ; fumée et banc KAL identiques sur les 6
      presets QEMU.
- [x] `original-tree` poussée ; un rootstock vierge greffe l'arbre complet depuis GitHub et le
      preset QEMU passe la fumée.

## Reprise
Première action de la session suivante :
```
cd /Users/cle_d_anton/lepton-tools-dev/lepton-tools && claude
# Aucune étape restante ; au choix de l'utilisateur : repointer les graines d'essai (§Reste).
```
