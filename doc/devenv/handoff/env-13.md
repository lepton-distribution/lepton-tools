# Passation ENV-13 — Graine de référence publiée — session du 2026-10-30 (préparation)

## Statut
à faire — étape préparée (publication des greffons, révision du plan) ; aucune tâche du fichier
d'étape commencée, aucune branche `devenv/env-13` créée.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` (poussée jusqu'à bf4d9ed) | commit de cette passation, sur bf4d9ed « devenv: révision du plan — étape ENV-13 » | oui |
| clone noyau `depots/lepton/original/master` | `master` 16a331b | non touché | oui |
| graine `depots/lepton-seed.scions/original-tree` | `original-tree` 43d12e6, 4 commits d'avance sur `origin` (ENV-6), non poussée | non touchée | oui |
| 7 greffons `depots/lepton-famille/*`, `depots/lepton-bsp/*` | `master` = `origin/master` (table du fichier d'étape) | distant `origin` SSH ajouté, `master` suivi | oui |

## Fait pendant la session
- 5 dépôts publics créés par `gh` dans `lepton-distribution` (stm32f4xx, stm32wlxx, nucleo-f429zi,
  nucleo-wl55jc1, qemu-mps2-an500), `master` poussé ; `origin` ajouté aux 7 dépôts locaux ;
  `git ls-remote` : `master` identique pour les 7 (PA-P, 5f816a2).
- Description GitHub de `lepton-bsp-qemu-mps2-an386` corrigée (« bcp » → « bsp »).
- `gh` 2.103.3 installé (Homebrew) et authentifié (`lepton-phlb`, admin de l'organisation).
- Constats : noyau publié sans code des 4 cartes ; collision des clés `famille::`/`bsp::` avec des
  URL (`scion/graft.py`) ; `building` portable (`INSTALL_LAYOUT` de scion).
- Plan révisé (skill `lepton-portage-instructions`) : `etapes/ENV-13-graine-publiee.md`, PA-13,
  PA-14, graphe, skills (bf4d9ed, poussé).

## Reste à faire dans l'étape
- [ ] Tâches 1 à 7 de `etapes/ENV-13-graine-publiee.md`.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Publier les 5 greffons : publics, `master` seul, `origin` dans les 7 dépôts, graine laissée de côté | utilisateur | oui |
| Nouvelle étape ENV-13 ; clés `family-`/`bsp-` ; URL `https://` ; anciens clones au PA-14 | utilisateur | oui |
| Essai de la regreffe sur une copie d'essai ; pushurl SSH ; essai final en rootstock vierge | proposition de la session (dans le fichier d'étape), non validée à part | non |

## Pièges rencontrés
- Homebrew : « Permission denied @ apply2files - /usr/local/lib/pcsc/drivers/SCLGENERIC.bundle »
  → liens `root` cassés de 2015 (pilotes de carte à puce) → sans effet sur `gh` ;
  `sudo rm -r /usr/local/lib/pcsc` à la main si l'utilisateur le souhaite.
- La skill `lepton-portage-instructions` renvoie à `references/archetypes-portage.md`, absent.

## Critères de validation
- [ ] PA-13 et PA-14 tranchés et consignés.
- [ ] Graine : 7 clés `family-`/`bsp-`, version `master`, URL `https://` ; `original::tree` et
      `building` inchangés ; 4 commits d'ENV-6 conservés.
- [ ] 7 clones sous `depots/lepton/<clé>/master` au commit de la table ; pushurl SSH.
- [ ] Trunk : 0 fichier régulier, 0 lien cassé, 0 lien vers les anciens clones.
- [ ] `comparer-oracle.py` code 0 sur les 14 presets, ou chaque écart expliqué ; fumée et banc KAL
      identiques sur les 6 presets QEMU.
- [ ] `original-tree` poussée (si accordé) ; un rootstock vierge greffe l'arbre complet depuis
      GitHub et le preset QEMU passe la fumée.

## Reprise
```
cd /Users/cle_d_anton/lepton-tools-dev/lepton-tools && claude
# « démarre la session ENV-13 » : skill devenv-session, mode plan, puis tâche 1 jusqu'au PA-13.
```
