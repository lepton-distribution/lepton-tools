# Passation ENV-22 — Résidus d'ENV-17 à ENV-21 — session du 2026-11-02

## Statut
terminée — fichier de tolérance de `<ROOTSTOCK>` écrit sans changer le trunk, propositions
confirmées, script de bout en bout réparé et relancé, règles des consignes VM écrites.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` (fusion `--no-ff` de `devenv/env-22`, poussées toutes deux) | commit d'état et passation, puis « Fusion de devenv/env-22 » ; fond : 83fd7b6 (script), 1aa1fa0 (doc) | oui |
| clone noyau `depots/lepton/original/master` | `master` 40d7197 = origin | inchangé | oui |
| graine `depots/lepton-seed.scions/original-tree` | `original-tree` 15740f9 = origin | inchangée | oui |
| seed.scions | `master` 472c12e (0.5.2.0) = origin | inchangé | oui |
| `<ROOTSTOCK>` | `.scion.trunk.tolerated` ajouté à la racine (hors git) ; trunk 3941 liens, liste inchangée | | oui |
| `essais/env-11/bout-en-bout` | rootstock neuf de `scripts/bout-en-bout.sh` (noyau 40d7197, famille 3954357, BSP 046779e ; graine locale 393e945) ; ancien archivé dans `essais/archives/env-11-bout-en-bout-20261102.tar.gz` | | oui (`lepton-graine.lock.json` non suivi, attendu) |

## Fait pendant la session
- Audit (`rapports/env-22-residus.md` §1) ; PA-31 tranché (§1.8).
- `<ROOTSTOCK>/.scion.trunk.tolerated` : `.DS_Store`, `._*` ; `scion graft` code 0 ; liste
  `chemin -> cible` triée identique avant et après (SHA-256 d2393067…, §2.1).
- `scripts/bout-en-bout.sh` (N-1) : `depots_ref` vers `depots/lepton/{family,bsp}-…/master`
  (83fd7b6) ; `shellcheck` 0.
- `essais/env-11/bout-en-bout` : archivé (9033 entrées, 3424 liens), supprimé sur accord, relancé :
  code 0, fumée QEMU réussie, 3054 liens, 0 cassé, 0 régulier (§2.3).
- `ORCHESTRATION.md` §2bis « Règles des consignes VM » (E-1, E-2) ; `etapes/ENV-28-…` y renvoie
  (1aa1fa0).
- Contrôles (§3) : 3941 liens, 0 cassé, 0 régulier, `lepton check` code 0 (19 fichiers conformes).
- PA-32 : fusion dans `main`, push de `main` et `devenv/env-22`.

## Reste à faire dans l'étape
- Aucune tâche du fichier d'étape.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-31 (1) : contenu du fichier de tolérance validé tel quel | utilisateur | oui |
| PA-31 (2) : P-1 à P-8 confirmées en bloc (P-6 ajoutée à la liste du fichier d'étape par la session) | utilisateur | oui |
| PA-31 (3) : corriger le script, archiver, supprimer, relancer `bout-en-bout` | utilisateur | oui |
| Suppression de `essais/env-11/bout-en-bout` après vérification de l'archive | utilisateur (accord explicite) | oui |
| PA-31 (4) : règles des consignes VM dans `ORCHESTRATION.md` §2bis | utilisateur | oui |
| PA-31 (5) : N-2 (défaut `--repo` de `lepton scion new`) consigné pour ENV-23 | utilisateur | oui |
| PA-32 : fusion et push | utilisateur | oui |
| Formulation des règles VM (attribution dès la consigne, `AVANCEMENT` d'attente, effet vérifié) | proposition de la session, appliquée dans le cadre du PA-31 (4) | rapport §2.2 |
| Nom et emplacement de l'archive (`essais/archives/env-11-bout-en-bout-20261102.tar.gz`) | proposition de la session | rapport §2.3 |

## Pièges rencontrés
- `scripts/bout-en-bout.sh` cassé depuis la suppression des anciens clones du 2026-10-30 (ENV-13) :
  aucun contrôle ne l'avait relancé depuis → corrigé, relancé.
- Le fichier de tolérance ne couvre que les fichiers **réguliers** du trunk ; un `.DS_Store` d'une
  source non git (`depots/generation/building`) est greffé en lien → sujet d'ENV-23 (PA-33).
- Un rootstock créé par `rootstock-install` 0.5.2.0 a un `.scion.trunk.tolerated` **sans motif** :
  le nouveau `bout-en-bout` ne tolère donc rien (purge de lepton seule).
- zsh : `echo =====…` est interprété (expansion `=`) → ne pas commencer un argument par `=`.

## Critères de validation
- [x] PA-31 et PA-32 tranchés et consignés.
- [x] `<ROOTSTOCK>/.scion.trunk.tolerated` présent ; `scion graft` code 0 ; liste des liens inchangée.
- [x] Chaque proposition listée au §1 est confirmée ou amendée dans `DEVENV-STATUS.md` §Décisions.
- [x] `essais/env-11/bout-en-bout` traité selon le PA-31.
- [x] Règles des consignes VM écrites ; ENV-28 s'y réfère.

## Reprise
Commande ou première action de la session suivante :
```
démarre la session   # skill devenv-session ; ENV-23 (etapes/ENV-23-scion-0-5-3.md), audit jusqu'au PA-33, N-2 compris
```
