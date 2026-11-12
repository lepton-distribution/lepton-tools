# Passation ENV-54 — Claude Code : règles de permission ciblées (D16) — session du 2026-11-12 (préparation)

## Statut
À démarrer. Cette session était hors étape : révision du plan après ENV-53, avec la skill
`lepton-portage-instructions`.
- Les étapes ENV-54 à ENV-57 sont rédigées ; aucune tâche d'ENV-54 n'est exécutée.
- Aucun fichier de l'arbre Lepton, de scion, de lepton ou de `.claude/` n'est touché.
- Aucune branche `devenv/env-54` n'existe.

La session qui exécutera ENV-54 remplacera cette passation.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `devenv/revision-2026-11-12b` (depuis `main` a709e8c) | commit de la révision du plan ENV-54 à ENV-57 ; fusion dans `main` et push selon l'accord de l'utilisateur (voir `DEVENV-STATUS.md` §Journal) | oui |
| seed.scions | `master` | 6416c33 (tag 0.6.3.0), non touché | oui |
| clone noyau `depots/lepton/original/master` | `master` | 58e421e, non touché | oui |
| autres | `master` / `original-tree` | non touchés : F4 acdd24c, F7 12280a5, WL 9349be2, graine 15740f9 | oui |

Outils : scion 0.6.3.0 et lepton 0.1.0, au Mac et sur la VM ; extension 0.5.2.

VM : état laissé par R53-1 (`handoff/env-53.md`). `essais/env-11/qemu` y est encore, sauf si
l'utilisateur l'a supprimé depuis (D15).

## Fait pendant la session
- Début de session : état conforme à `handoff/env-53.md` (`main` a709e8c, propre).
- Sources de D13, D14 et D16 lues :
  - `rapports/env-53-mac.md` §1.5 et §4 ;
  - `rapports/env-53-debian.md` §5.2, §5.3 et §7 ;
  - `handoff/env-53.md` ; ORCHESTRATION §2bis.
- Relevés en lecture seule, repris dans les fichiers d'étapes :
  - D13 : `lepton/seed.py`, `parse_location` et `Origin.remote` (`urlparse(...).netloc`) ;
    appelants de `parse_location` ; `scion/mirror.py`, `is_remote` (même test) et ses
    appelants ;
  - D14 : `scion/gitops.py`, `clone` et `clone_partial` (`dest.parent.mkdir`) ; appelants
    (`cli.py` `_clone_seed`, `graft.py` `_fetch`) ; `mirror.py` `sync_one` ; `lepton/seed.py`
    `add_scion` et `_undo_add` ;
  - D16 : `.claude/settings.json` (hook seul, aucune règle) ; `settings.local.json` ignoré par
    `~/.gitignore_global`.
- Décisions de l'utilisateur, sur questions posées :
  - D14 corrigé dans scion ;
  - portée de D16 étendue ;
  - validation Debian ENV-57 ;
  - ordre D16 d'abord.
- Fichiers d'étapes :
  - `etapes/ENV-54-permissions-classifieur.md` ;
  - `ENV-55-lepton-url-file.md` ;
  - `ENV-56-scion-clonage-echec.md` ;
  - `ENV-57-validation-debian.md`.
- Autres documents mis à jour :
  - ORCHESTRATION §2, §4 (PA-95 à PA-102), §5bis et §6 ;
  - `DEVENV-STATUS.md` : étapes, décision, prochaine action, journal ;
  - `HORS-PLAN.md` : D13, D14 et D16 planifiés.
- Relecture par un agent indépendant (ORCHESTRATION §5bis, effort `xhigh`, lecture seule) :
  0 bloquant, 11 à corriger, 14 suggestions. La session a vérifié les principaux constats
  (n°3, 4, 8, 9, 10, 16, 17, 21). Tous ont été appliqués sur décision de l'utilisateur. Pour le
  n°1, la part scion éventuelle de D13 ira dans une étape scion insérée. Détail au journal de
  `DEVENV-STATUS.md` (2026-11-12).

## Reste à faire dans l'étape
- [ ] Tout ENV-54 (§1 à §3) : rien n'est commencé.
- [ ] Les quatre fichiers d'étapes sont un premier jet : relire les propositions non validées
      ci-dessous avant de s'y fier.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| D13, D14, D16 à traiter ; D15 : `essais/env-53-c5` remplace `essais/env-11/qemu` (2026-11-12, fin du plan) | utilisateur | oui |
| Découpage ENV-54 (D16), ENV-55 (D13), ENV-56 (D14), ENV-57 (Debian) ; ordre 54, 55, 56, 57 ; 55 et 56 permutables | utilisateur (questions, plan approuvé) | oui |
| D14 corrigé dans scion, et non dans lepton | utilisateur | oui |
| D16 : `scion graft-update`, `rm -rf` des essais, `pipx install`, `git clone`, tests | utilisateur | oui |
| ENV-57 : validation Debian groupée en fin de plan | utilisateur | oui |
| Révision sur la branche `devenv/revision-2026-11-12b`, fusion dans `main` | utilisateur (plan approuvé) | oui |
| Constats de la relecture : tous appliqués ; n°1, part scion éventuelle de D13 dans une étape scion insérée (ENV-56 ne traite que D14) | utilisateur | oui |
| ENV-54 : mécanisme établi par la documentation (agent `claude-code-guide`) et par un essai témoin, seule écriture avant le PA-95 ; `graft-update` témoin sur accord PA-P dans la copie `essais/env-54-essai/qemu` ; forme témoin de `pipx install` à fixer avec l'utilisateur avant l'essai (`PIPX_HOME` temporaire ou même version depuis `main`) | proposition non validée | non |
| ENV-54 : option `ask` pour `graft-update` et `seed-update` ; option d'un script d'enveloppe pour borner `rm -rf` ; contrôles négatifs sur des cibles absentes ; contrôle vivant du hook ; rejeu après redémarrage, avec passation intermédiaire | proposition non validée | non |
| ENV-55 : rootstock d'essai `essais/env-55-essai`, copie d'`essais/env-11/qemu` (Mac) ; dépôt git local d'essai sous `essais/`, forme fixée à l'audit ; une seule fonction de classification pour `parse_location` et `Origin.remote` | proposition non validée | non |
| ENV-56 : pas de regreffe de `<ROOTSTOCK>` ni d'oracle (chemins d'échec seulement) ; copie `essais/env-56-essai` et venv `essais/env-56-venv` ; clé projetée et miroir sur un rootstock temporaire construit comme les fixtures de `<SEED_SCIONS>/tests/` ; version `0.6.3.1` ou `0.6.4.0` au PA-99 | proposition non validée | non |
| ENV-57 : D16 prouvé par les commandes que lance la session VM elle-même ; pose d'un fichier de réglages propre à la VM par l'utilisateur ; regreffes, presets, cartes, nettoyage et relance de la session VM tranchés au PA-101 | proposition non validée | non |

## Pièges rencontrés
- La skill `lepton-portage-instructions` cite `references/archetypes-portage.md`.
  - Il manque dans sa copie synchronisée : `~/.claude/skills/synced/…/lepton-portage-instructions/`
    ne contient que `SKILL.md`, du 9 novembre.
  - Il existe dans le clone noyau :
    `<ROOTSTOCK>/depots/lepton/original/master/.claude/skills/lepton-portage-instructions/references/archetypes-portage.md`
    (version du 8 octobre, commit 1996d6b).
  - La révision a été rédigée sans lui, puis relue contre lui : rien à changer.
  - Rétabli le 2026-11-12 : l'utilisateur a republié la skill sur claude.ai avec `references/`.
    Depuis 19:47, la copie synchronisée contient `references/archetypes-portage.md`, identique à
    celui du clone noyau.
- `regreffer-essai.sh` d'ENV-53 est versionné sous `rapports/env-53-mac/`, pas sous
  `essais/env-53-mac/`. Ce dernier ne contient que les journaux.
- Le piège « lepton n'accepte une URL `file://` qu'avec un hôte » figurait déjà dans ENV-51 : c'est
  D13.

## Critères de validation
- [ ] PA-95 et PA-96 tranchés et consignés.
- [ ] Inventaire des refus, des acceptations et des formes de commandes au rapport.
- [ ] Mécanisme établi, avec sa source (page de documentation, essai).
- [ ] Essai témoin rejoué après redémarrage : chaque commande retenue est acceptée, chaque
      contrôle négatif est refusé ou soumis à confirmation. Le journal de session est cité.
- [ ] Le hook refuse toujours une écriture sous un `trunk/` ; `settings.json` est du JSON valide.
- [ ] `pytest` complet vert ; hook inchangé, ou modifié et testé selon le PA-95.
- [ ] ORCHESTRATION §2bis amendé.
- [ ] `HORS-PLAN.md` : D16 marqué traité, ou clos selon le PA-95, avec renvoi au rapport.

## Reprise
Commande ou première action de la session suivante :
```
démarrer ENV-54 (skill devenv-session) : lire etapes/ENV-54-permissions-classifieur.md et cette
passation ; branche devenv/env-54 de lepton-tools depuis main ; tâche 1 (audit, lecture seule)
jusqu'au PA-95
```
