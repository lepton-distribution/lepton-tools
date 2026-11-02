# Passation ENV-28 — Validation Debian groupée (ENV-22 à ENV-27) — session du 2026-11-02

## Statut
terminée — R28-1 conforme sur C1-C8 (Debian 13.7) ; rootstocks d'essai du Mac regreffés ; le
plan ENV-0 à ENV-28 est réalisé.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` (fusion `--no-ff` de `devenv/env-28`, poussées toutes deux) | « Fusion de devenv/env-28 (ENV-28 validation Debian groupée, PA-44) » ; fond : « devenv(env-28): état et passation » | oui |
| lepton-tools `devenv/env-28-debian` (VM) | 1904c83, poussée, fusionnée dans `devenv/env-28` (ee1b62e) | « devenv(env-28): rapport Debian R28-1 et oracle env-28-debian » | — |
| clone noyau `depots/lepton/original/master` | `master` 0c0cc4f, non touché | — | oui |
| graine, greffons, seed.scions | non touchés | — | oui |

Hors dépôts :
- Mac : 7 rootstocks d'essai regreffés (`essais/env-9`, `env-11/{f429zi,qemu,qemu-gra2,wl55jc1}`,
  `env-11/bout-en-bout/rootstock`, `env-13-vierge`), clones aux têtes publiées ; journaux
  `~/lepton-tools-dev/essais/env-28-mac/`.
- VM : scion 0.5.3.0, lepton 0.1.0 (b8ff911) ; rootstocks `essais/env-28-debian` (neuf) et
  `essais/env-14-debian` (graine avancée, clones ramenés sur `master`) conservés, journaux
  `~/env-28-journaux/` ; `essais/env-21-debian` et `~/env-21-journaux` supprimés (C8).

## Fait pendant la session
- Tâche 1 : écarts Mac `env-20-apres` → `env-27-apres` (cpufs seul : `.text`, `filecpu_memory`,
  DWARF ; `rapports/env-28-mac.md` §1) ; têtes publiées ; consigne `consignes/env-28-debian.md` ;
  PA-43 ; push de `devenv/env-28` ; ordre `R28-1` à `debian-linux-vm`.
- Tâche 2 (VM) : ACCUSÉ ; C1-C2 (scion 0.5.2.0 → 0.5.3.0 par `install-debian.sh`,
  `changements 0`) ; E-1 au §7.1 puis correction PA-43 (2) ; C3-C8 conformes ; `FIN-SUCCÈS R28-1`
  (rapport `rapports/env-28-debian.md`).
- Tâche 3 : 7 rootstocks d'essai regreffés, liens ajoutés seulement (SVD, `tests/`), 0 cassé,
  0 régulier ; `check` et `generate` 0 (`qemu-gra2` 1, attendu) ; `env-13-vierge` = `<ROOTSTOCK>`
  (3956 liens, 23 lancements) (`rapports/env-28-mac.md` §3).
- Tâche 4 : rapport VM vérifié, comparaisons refaites sur l'oracle poussé (écarts identiques au
  Mac, preset par preset) ; P-1 écrite dans ORCHESTRATION §2bis ; PA-44 : fusions et push.

## Reste à faire dans l'étape
- Aucune.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-43 : consigne telle quelle, `graft-update` d'`env-14-debian` seul, C5 A puis B, C8, push, ordre | utilisateur | oui |
| PA-43 (2) : option A (`switch master` des 2 clones, 2e `graft-update`) ; constats scion pour plus tard | utilisateur | oui |
| Tâche 3 : les 7 rootstocks, `bout-en-bout` compris | utilisateur | oui |
| PA-44 : fusions et push ; P-1 appliquée (ORCHESTRATION §2bis) ; P-2 retenue, non planifiée | utilisateur | oui |
| Ordre R28-1 envoyé en résumé avec chemin et SHA-256 de la consigne, et non en texte intégral ; la VM a vérifié la somme | proposition de la session, signalée à l'utilisateur | `rapports/env-28-mac.md` §2 |

## Pièges rencontrés
- Clone d'un rootstock VM laissé sur une branche d'étape (`devenv/env-14`) → `graft-update`
  tire cette branche, conflits, trunk vidé → relever la branche des clones au §5 (règle P-1).
- `scion graft-update` refusé par le classifieur de la session VM (« Untrusted Code
  Integration ») → l'utilisateur le lance ; `seed-add`, `graft`, `rejouer-oracle.sh` passent.
- Réponse à l'adresse `bridge:…` du message reçu : livraison non confirmée par le serveur, mais
  reçue.
- `qemu-gra2` : `graft-update` réinscrit le BSP an386 → `scion graft-remove` sans `--purge`.
- zsh : `echo =====` échoue (`=cmd`) ; utiliser des guillemets.

## Critères de validation
- [x] PA-43 et PA-44 tranchés et consignés.
- [x] `FIN-SUCCÈS R28-1` vérifié par la session Mac ; C1 à C8 conformes.
- [x] Rootstocks d'essai regreffés : 0 lien cassé, 0 fichier régulier ; `check` code 0.
- [x] `DEVENV-STATUS.md` §Versions : scion et lepton sur Debian relevés.

## Reprise
Commande ou première action de la session suivante :
```
démarre la session   # aucune étape planifiée : révision du plan (skill lepton-portage-instructions) à partir de P-1 d'ENV-27 et P-2 d'ENV-28
```
