# Passation ENV-58 — Claude Code : formes des commandes et règles de la VM (D20, D19) — session du 2026-11-13 (préparation)

## Statut
À démarrer. Cette session était hors étape : révision du plan après ENV-57, avec la skill
`lepton-portage-instructions`.
- Les étapes ENV-58 à ENV-61 sont rédigées ; aucune tâche d'ENV-58 n'est exécutée.
- Aucun fichier de l'arbre Lepton, de scion, de lepton ou de `.claude/` n'est touché.
- Aucune branche `devenv/env-58` n'existe.

La session qui exécutera ENV-58 remplacera cette passation.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` | 1ae63da « devenv: consignation de la fusion et du push de la révision du plan (ENV-58 à ENV-61) », au-dessus de 4a04b6c (fusion `--no-ff` de `devenv/revision-2026-11-13`, 2cc8a0f, depuis 71cba24) ; `main` et la branche poussés (PA-P) ; puis le commit de cette passation, non poussé | oui |
| seed.scions | `master` | d650414 (tag 0.6.3.1), non touché | oui |
| clone noyau `depots/lepton/original/master` | `master` | ed2a41f, non touché | oui |
| autres | `master` / `original-tree` | non touchés : graine 15740f9 | oui |

Outils : scion 0.6.3.1 et lepton 0.1.0, au Mac et sur la VM ; extension 0.5.2 ; Claude Code
2.1.323.

VM : état laissé par R57-1 (`handoff/env-57.md`). `~/.claude/settings.json` y porte ses 3 règles
`allow` utilisateur (D19). La décision d'ENV-58 (PA-103) est appliquée en ENV-61.

## Fait pendant la session
- Début de session : état conforme à `handoff/env-57.md` (`main` 71cba24 = `origin/main`, propre).
- Sources de D17 à D20 lues :
  - `rapports/env-55-url-file.md` §2, §3, §6 ;
  - `rapports/env-56-scion.md` §1.3 à §1.8, §2 à §6 ;
  - `rapports/env-57-mac.md` §1.3, §1.5, §4, §5 ; `rapports/env-57-debian.md` §1, §3, §9 ;
  - `consignes/env-57-debian.md` §0, §2, §11, §13, §14 ; `rapports/env-54-permissions.md` §3, §8,
    §10.2 ;
  - `handoff/env-57.md`.
- Relevés en lecture seule, repris dans les fichiers d'étapes :
  - D17 : `lepton/seed.py` (`parse_location`, l. 110-111 ; appelants) ; autres
    `Path(<saisie>).resolve()` sans `expanduser` ; `extension/src/commands.ts:87` ;
  - D18 : `scion/gitops.py` `clone()` (l. 94-110) ; `scion/graft.py` `_fetch` (l. 275-301),
    contrôle de version (l. 377, 410) ; `scion/cli.py` `_clone_seed` (l. 96-110) ; P-V1 ;
    `rapports/env-56-scion/fixture-avant/f06.*` ;
  - D19, D20 : `.claude/settings.json` (règles d'ENV-54) ; `rapports/env-57-mac/decisions.py`.
- Décisions de l'utilisateur, sur questions posées :
  - découpage en quatre étapes ;
  - portée de D20 étendue au lancement des commandes `ask` hors script.
- Fichiers d'étapes :
  - `etapes/ENV-58-claude-code-formes-commandes.md` ;
  - `ENV-59-lepton-indice-tilde.md` ;
  - `ENV-60-scion-checkout-echec.md` ;
  - `ENV-61-validation-debian.md`.
- Autres documents mis à jour :
  - ORCHESTRATION §2, §4 (PA-103 à PA-110), §5bis et §6 ;
  - `DEVENV-STATUS.md` : étapes, décision, prochaine action, journal ;
  - `HORS-PLAN.md` : D17 à D20 planifiés.
- Relecture par un agent indépendant (ORCHESTRATION §5bis, effort `xhigh`, lecture seule) :
  0 bloquant, 11 à corriger, 13 suggestions. La session a vérifié les principaux constats : n°1 à
  12 et 16 sont confirmés, n°19 et 20 le sont en partie. Tous ont été appliqués sur décision de
  l'utilisateur, n°19 et 20 ramenés à ce qui est confirmé. Détail au journal de
  `DEVENV-STATUS.md` (2026-11-13).

## Reste à faire dans l'étape
- [ ] Tâche 1 : audit et essai témoin, jusqu'au PA-103.
- [ ] Tâche 2 : amendement du §2bis et mise en place selon le PA-103.
- [ ] Tâche 3 : contrôles, PA-104.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Découpage ENV-58 (D20, D19), ENV-59 (D17), ENV-60 (D18), ENV-61 (Debian) ; ordre 58, 59 et 60 permutables, 61 | utilisateur | oui |
| Portée de D20 : redirections et commandes `ask` lancées hors script | utilisateur | oui |
| ENV-58 : contenu de l'amendement du §2bis (redirection, journal par une option de l'outil, deux phases pour un script) ; cas `bash -c` ajouté à la portée de D20 | proposition non validée (PA-103) | non |
| ENV-58 : essai témoin (formes de redirection, `ask` direct, par script et par `bash -c` sur `essais/env-58-absent`, invites refusées) ; scripts versionnés sous `rapports/env-58-formes/` | proposition non validée (plan de session d'ENV-58) | non |
| ENV-58 : bloc `permissions.allow` seul pour la VM, modifié par l'utilisateur au §0 de la consigne d'ENV-61 | proposition non validée (PA-103) | non |
| ENV-59 : portée limitée à l'indice ; autres chemins saisis traités à part ou reportés ; copie `essais/env-59-essai` | proposition non validée (PA-105) | non |
| ENV-60 : options de correction de D18 (message forme P-V1, retrait du clone, contrôle de la version) ; version 0.6.3.2 ou 0.6.4.0 ; ni oracle ni regreffe de `<ROOTSTOCK>` ; copie `essais/env-60-essai` | proposition non validée (PA-107) | non |
| ENV-61 : contenu de C2 (contrôles négatifs par règle retirée) et de C5 (fixture conditionnelle à un clone de seed.scions sur la VM) ; relance de la session au §0 | proposition non validée (PA-109) | non |

## Pièges rencontrés
- Le constat « un `graft-update` lancé depuis un script échappe à la règle `ask` » est déduit
  (`rapports/env-57-mac.md` §1.3), jamais essayé. L'essai d'ENV-58 vise une cible absente
  seulement, et l'invite éventuelle est refusée.
- Une lecture groupée qui cite `scion graft-update` déclenche l'invite `ask` (ENV-54 §10.2, O-0) :
  ne pas citer les commandes `ask` dans des lectures. Pendant la relecture de la révision, une
  recherche Bash d'un motif `git … push` a été refusée par le classifieur (« Undermining
  Oversight ») : chercher par l'outil Grep.

## Critères de validation
- [ ] PA-103 et PA-104 tranchés et consignés.
- [ ] Inventaire des formes fautives au rapport (fichier, ligne).
- [ ] Essai témoin consigné, avec les décisions du journal de session :
      - redirection : règle ou classifieur, pour chaque forme ;
      - `ask` direct, depuis un script et par `bash -c` : invite ou classifieur.
- [ ] ORCHESTRATION §2bis amendé ; `consignes/env-57-debian.md` §2 n'est plus la seule source de
      la règle.
- [ ] Bloc `permissions.allow` attendu sur la VM, et conduite de modification, au rapport (D19).
- [ ] `pytest` complet vert ; `settings.json` en JSON valide s'il change.
- [ ] `HORS-PLAN.md` : D20 marqué traité ; D19 « décidé, appliqué en ENV-61 », avec renvoi au
      rapport.

## Reprise
Commande ou première action de la session suivante :
```
démarre la session ENV-58 (skill devenv-session) : lire etapes/ENV-58-claude-code-formes-commandes.md
et cette passation ; branche devenv/env-58 de lepton-tools depuis main ; tâche 1 jusqu'au PA-103
```
