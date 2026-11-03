# Passation ENV-33 — Validation Debian groupée (ENV-29 à ENV-32) — session du 2026-11-03

## Statut
terminée — ordre R33-1 conforme sur la VM Debian (C1-C8), vérifié par la session Mac ; 7 rootstocks
d'essai du Mac regreffés ; fusions et push faits (PA-54). Dernière étape du plan ENV-0 à ENV-33.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` : fusion `--no-ff` de `devenv/env-33` ; `main` et `devenv/env-33` poussées ; `devenv/env-33-debian` (VM, bd14555) poussée, fusionnée | « Fusion de devenv/env-33 (ENV-33 validation Debian groupée ENV-29 à ENV-32, PA-54) » | oui |
| clone noyau `depots/lepton/original/master` | `master` b3a5415 (non touché) | « Fusion de devenv/env-32 … » | oui |
| autres (seed.scions, graine, greffons) | non touchés | — | oui |

Hors dépôts :
- VM : `essais/env-28-debian` mis à jour (3957 liens), `essais/env-33-debian` neuf (3957 liens,
  `build/` des 16 presets + host), `~/env-33-journaux/` ; supprimés : `essais/env-14-debian`,
  `~/env-28-journaux`, copie `essais/env-33-copie-e1`. scion 0.5.4.0, lepton 0.1.0 (e47bc11).
- Mac : 7 rootstocks d'essai regreffés (`env-9`, `env-11/{f429zi,qemu,qemu-gra2,wl55jc1}`,
  `env-11/bout-en-bout/rootstock`, `env-13-vierge`), clones aux têtes publiées ; journaux
  `~/lepton-tools-dev/essais/env-33-mac/` (non versionnés). `bout-en-bout/rootstock/.scion.trunk.tolerated`
  complété (`.DS_Store`, `._*`). `<ROOTSTOCK>` non touché.
- `essais/env-26-copie` et `essais/env-27-copie` (Mac) : toujours présents, hors périmètre.

## Fait pendant la session
- Tâche 1 : `rapports/env-33-mac.md` §1 (écarts `env-27-apres` → `env-32-apres` : embOS 0, FreeRTOS
  = ENV-31), §2 (`git ls-remote`) ; consigne `consignes/env-33-debian.md` ; PA-53 (1) et PA-53.
- Tâche 2 : ordre R33-1 ; messages consignés (`rapports/env-33-mac.md` §4) ; `FIN-SUCCÈS R33-1` ;
  rapport VM `rapports/env-33-debian.md`, oracle `oracles/env-33-debian/` (bd14555).
- Tâche 3 : regreffe des 7 rootstocks d'essai, `check`/`generate` (§5).
- Tâche 4 : vérification du rapport VM, comparaisons refaites sur l'oracle poussé (§6) ; PA-54.

## Reste à faire dans l'étape
- Aucun.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-53 (1) : C7 découverte seule, E-1 sur copie de `env-28-debian`, C8 (`env-14-debian`, `~/env-28-journaux`) | utilisateur (recommandations retenues) | oui |
| PA-53 : consigne validée, push de `devenv/env-33`, ordre R33-1 | utilisateur | oui |
| Accord de la tâche 3 (7 rootstocks, PA-P) | utilisateur | oui (journal) |
| PA-53 (2) : motifs `.DS_Store`/`._*` dans le `.scion.trunk.tolerated` de `bout-en-bout`, puis `graft` | utilisateur | oui |
| Push de `devenv/env-33-debian` (accordé sur la VM) | utilisateur | oui (PA-54) |
| PA-54 : fusions `--no-ff` et push | utilisateur | oui |
| AVANCEMENT §6.2 accepté comme ACCUSÉ (accusé non remis, ECONNRESET) | session Mac, l'utilisateur ayant décidé côté VM de poursuivre | oui (journal) |
| Mention « la VM jusqu'à ENV-33 » d'ORCHESTRATION §2bis à actualiser | proposition non validée | oui (Prochaine action) |

## Pièges rencontrés
- Messages VM → Mac en `ECONNRESET` au début : l'ACCUSÉ n'arrive pas. Parade : la VM journalise et
  reprend le contenu dans le message suivant ; la session Mac confirme la réception.
- Rootstock recréé par script sans motifs Finder dans `.scion.trunk.tolerated` : `graft-update`
  refusé (scion 0.5.4.0 rétablit le trunk, mais le clone noyau est déjà avancé, 1 lien cassé jusqu'à
  la regreffe). Parade : vérifier ce fichier avant une regreffe sur le Mac.
- Le Finder recrée des `.DS_Store` dans les trunks pendant les opérations : tolérés, ne pas les
  compter comme écart.
- Le bourrage d'alignement du `.text` se répartit différemment selon la chaîne : +16 sur
  an386-freertos au Mac, +64 sur wl55jc1-freertos sous Debian ; vérifier qu'aucune autre taille de
  symbole ne change.
- `comparer-oracle.py` sur `host` rend 2 (pas d'ELF) : comparer ses fichiers (`mklepton-empreintes`).

## Critères de validation
- [x] PA-53 et PA-54 tranchés et consignés.
- [x] `FIN-SUCCÈS R33-1` vérifié par la session Mac ; C1 à C8 conformes.
- [x] Rootstocks d'essai regreffés : 0 lien cassé, aucun fichier régulier hors `.DS_Store` tolérés ;
  `check` code 0 (`qemu-gra2` : 1, attendu).
- [x] `DEVENV-STATUS.md` §Versions : scion et lepton sur Debian relevés.

## Reprise
Commande ou première action de la session suivante :
```
démarre la session   # aucune étape planifiée : décider d'un nouveau lot ou de la clôture
```
