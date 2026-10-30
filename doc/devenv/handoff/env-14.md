# Passation ENV-14 — Nettoyage de l'arbre — session du 2026-10-30

## Statut
terminée — 82 fichiers versionnés et tous les `.DS_Store` retirés de l'arbre, sans régression
(oracle Mac, validation Debian R14-1) ; `master` du noyau et de `family-stm32f4xx` publiés.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` (fusion de `devenv/env-14`, poussées toutes deux) | commit d'état et passation, puis fusion « Fusion de devenv/env-14 » | oui |
| clone noyau `depots/lepton/original/master` | `master` 118912a « Fusion de devenv/env-14 (ENV-14 nettoyage de l'arbre) » = `origin/master` ; `devenv/env-14` e5a5689 poussée | | oui |
| `depots/lepton/family-stm32f4xx/master` | `master` 7694ad5 « Fusion de devenv/env-14 » = `origin/master` ; `devenv/env-14` af964c6 poussée | | oui |
| 6 autres greffons famille/BSP, graine `original-tree` 0f1275a | `master` / `original-tree`, inchangés | | oui |
| `<ROOTSTOCK>` trunk | regreffé sur `master` | 3929 liens, 0 cassé, 0 fichier régulier, 0 `.DS_Store` | oui |

## Fait pendant la session
- Tâche 1 : inventaire des 4063 feuilles du trunk (`rapports/env-14-inventaire.md`, annexe
  `env-14-inventaire-feuilles.tsv`, scripts `env-14-inventaire.py`, `env-14-classer.py`) ; PA-15.
- Tâche 2 : oracle avant `oracles/env-14-avant/` (host + 14 presets), conforme à `env-13-apres`.
- Tâche 3 : 26 `.DS_Store` du trunk retirés par l'utilisateur, 41 des clones et hors git par la
  session ; regreffe sans `--force`.
- Tâche 4 : clone noyau 2c70c9d (L1), 98481ac (L2), e5e0fcd (L3), e5a5689 (A1-A3) ;
  `family-stm32f4xx` af964c6 (A5) ; 82 fichiers, 3 483 360 octets.
- Tâche 5 : oracle après `oracles/env-14-apres/` : `comparer-oracle` code 0 sur 14 presets,
  mklepton identiques, fumée et banc KAL identiques ; E1 démontré (`env-14-preuve-empreintes.sh`,
  `oracles/env-14-apres/preuve-e1.log`) ; `lepton check` : seule anomalie connue ; rapport
  `rapports/env-14-nettoyage.md`.
- Tâche 6 : PA-16 ; ordre R14-1 (consigne `consignes/env-14-debian.md`, VM `lepton-vm-debian`) :
  FIN-SUCCÈS, C1 à C7 ; C6 revérifié côté Mac ; `devenv/env-14-debian` fusionnée ;
  fusion dans `master` et push (noyau, `family-stm32f4xx`).

## Reste à faire dans l'étape
- Aucune tâche du fichier d'étape.
- Hors étape : les rootstocks d'essai (`essais/env-9`, `essais/env-11/*`, `essais/env-13-vierge`)
  ne reçoivent le nettoyage qu'à un `scion graft-update` (PA-P).

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-15 : L1, L2 (A0, tauon_sampleapp en entier), L3, A1, A2, A3, A5 supprimés ; A4 conservé ; documents historiques jamais réécrits, commentaires de provenance (XML samd21, BSP WL) laissés ; pas d'ajout au `.gitignore` des greffons ni de la graine ; `.DS_Store` hors git supprimés | utilisateur | oui |
| PA-16 (1) : push des 3 `devenv/env-14`, ordre R14-1 à `lepton-vm-debian` | utilisateur | oui |
| PA-16 (2) : fusion dans `master` et push (noyau, `family-stm32f4xx`) ; lepton-tools fusionnée dans `main` et poussée ; copie `essais/env-14-preuve` supprimée | utilisateur | oui |
| `build_closure.py` non réutilisé (projets IAR) ; usage = `ninja -t deps` + chemins cités, propagé jusqu'au point fixe | proposition de la session (exposée au PA-15) | rapport seulement |
| `.DS_Store` des répertoires intermédiaires de `depots/` retirés aussi (hors git), au titre de la décision PA-15 ; ceux sous `.git/`, `~/lepton/`, `build/`, `third_party/` laissés | proposition de la session (annoncée) | rapport seulement |
| Construction incrémentale de contrôle après L1, L2 et après A5 (pour L3-A5), non après chaque lot | proposition de la session | rapport seulement |

## Pièges rencontrés
- La lecture de ninja seule manque les fichiers lus par chemin relatif : `tests/host` passe le XML
  Olimex à mklepton, qui embarque 21 fichiers de tauon-basic → propagation par chemins cités.
- `grep -r` ne suit pas les liens : chercher dans les clones, pas dans le trunk.
- Le trunk avait 26 `.DS_Store` réguliers (24 annoncés) : le Finder en recrée dès qu'un dossier est
  ouvert ; et 26 `.DS_Store` ignorés du clone noyau étaient greffés en liens.
- `lepton check` sur `~/lepton` sort en code 1 pour « manifeste de graine absent » (connu, ENV-12).
- `comparer-oracle` sur `host` : pas d'`empreintes.txt` (normal) ; comparer `mklepton-empreintes.sha256`.
- `.scion.grafted.list` garde la version de la graine (`master`) même si le clone est sur une autre
  branche (constat VM, sans effet).

## Critères de validation
- [x] PA-15 et PA-16 tranchés et consignés.
- [x] Inventaire `rapports/env-14-inventaire.md` complet : chaque entrée classée, avec son motif.
- [x] Tous les chemins validés au PA-15 sont absents du clone et du trunk ; aucun autre fichier versionné retiré.
- [x] Code gelé et BSP hors presets intacts (`git diff --stat master..devenv/env-14` limité aux lots).
- [x] Trunk : 0 fichier régulier, 0 lien cassé, 0 `.DS_Store` ; regreffe sans `--force`.
- [x] `comparer-oracle.py` code 0 sur les 14 presets ; empreintes mklepton identiques ; fumée et
      banc KAL identiques sur les 6 presets QEMU.
- [x] `FIN-SUCCÈS R14-1` (Debian) ; `master` du noyau poussé.

## Reprise
Première action de la session suivante :
```
cd /Users/cle_d_anton/lepton-tools-dev/lepton-tools && claude
# Aucune étape restante ; au choix de l'utilisateur : graft-update des rootstocks d'essai (PA-P) ou révision du plan.
```
