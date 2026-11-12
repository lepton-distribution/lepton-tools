# Passation ENV-51 — lepton : messages de scion relayés (D10) — session du 2026-11-12 (préparation)

## Statut
à démarrer — session hors étape : révision du plan après ENV-50 (skill
`lepton-portage-instructions`). Les étapes ENV-51 à ENV-53 sont rédigées ; aucune tâche d'ENV-51
n'est exécutée. Aucun fichier de l'arbre Lepton, de scion ou de lepton n'est touché ; aucune
branche `devenv/env-51` n'existe. La session qui exécutera ENV-51 remplacera cette passation.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `devenv/revision-2026-11-12` (depuis `main` a7fcb62) | commit de la révision du plan ENV-51 à ENV-53 ; fusion dans `main` et push selon l'accord de l'utilisateur (voir `DEVENV-STATUS.md` §Journal) | oui |
| clone noyau `depots/lepton/original/master` | `master` | 76f28bd, non touché | oui |
| autres | `master` / `original-tree` | non touchés : F4 acdd24c, F7 12280a5, WL 9349be2, graine 15740f9, seed.scions `master` 7e8a0cc (tag 0.6.2.0) | oui |

`<ROOTSTOCK>` : 3889 liens, 629 projetés (valeurs d'ENV-50, non recomptées) ; 8 clones sous
`depots/tiers/`, dont `stm32cubewl/v1.6.0` (156 Mo, relevé `du -sh` du 2026-11-12). Anciens clones
WL `v1.3.0` absents.

Outils : scion 0.6.2.0, lepton 0.1.0 ; git 2.50.1 au Mac.

Cartes : rendues au Mac après R50-1 (F429 `nucleo-f439zi-embos`, WL55 A et B
`nucleo-wl55jc1-freertos`). ENV-51 n'en a pas besoin.

## Fait pendant la session
- Début de session : état des dépôts conforme à `handoff/env-50.md` (`git status`, branches,
  têtes de lepton-tools, seed.scions, clone noyau, `family-stm32wlxx`).
- Sources de D10 et D11 lues : `rapports/env-44-residus.md` §3.1, §4.3 ;
  `rapports/env-48-wl-projection.md` §1.6 ; `rapports/env-49-wl-hal.md` §1.2, §1.7, §5 ;
  `<SEED_SCIONS>/doc/projection-miroir.md` §1, §A.8, §A.10 à §A.12, §C.
- Relevés en lecture seule, repris dans les fichiers d'étapes :
  - `lepton/scion_runner.py` (`run` : `capture_output=True`, sortie rendue en cas d'échec
    seulement) ; appels de scion dans `seed.py`, `files.py`, `scions.py` ; sous-commandes de
    `cli.py` ; commandes `--json` lues par l'extension ;
  - `scion/gitops.py` (`clone_partial`, `checkout_detached`), appelés par `scion/graft.py` ;
  - références de version 0.6.2.0 (lepton-tools, clone noyau) ;
  - clones projetés des rootstocks d'essai du Mac ; `essais/env-44-d1-*` absents.
- Décisions de l'utilisateur (questions posées) : ENV-53 Debian en fin de plan ; D11 en une étape.
- Fichiers d'étapes `etapes/ENV-51-lepton-messages-scion.md` (110 lignes),
  `ENV-52-scion-extraction-partielle.md` (151), `ENV-53-validation-debian.md` (136).
- ORCHESTRATION §2, §4 (PA-89 à PA-94), §5bis, §6 ; `DEVENV-STATUS.md` (étapes, décision,
  prochaine action, journal) ; `HORS-PLAN.md` (D10, D11 planifiés).
- Relecture par un agent indépendant (ORCHESTRATION §5bis, effort `xhigh`, lecture seule) :
  0 bloquant, 14 à corriger, 13 suggestions. Principaux constats vérifiés par la session, puis
  tous appliqués sur décision de l'utilisateur, avec deux nuances (n°12 : permutation 51/52 gardée,
  raison déduite retirée ; n°21 : PA-P limité à `graft-update` et `seed-update`). Détail au journal
  de `DEVENV-STATUS.md` (2026-11-12).

## Reste à faire dans l'étape
- [ ] Tout ENV-51 (§1 à §3) : rien n'est commencé.
- [ ] Les trois fichiers d'étapes sont un premier jet : relire les propositions non validées
      ci-dessous avant de s'y fier.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| D10 et D11 à traiter ; A1 à A4, D4, D12 hors plan (2026-11-10) | utilisateur | oui |
| Découpage ENV-51 (D10), ENV-52 (D11), ENV-53 (Debian) ; ordre 51, 52, 53, 51 et 52 permutables | utilisateur (plan approuvé) | oui |
| ENV-53 : validation Debian groupée en fin de plan | utilisateur | oui |
| D11 en une seule étape, amendement de la spécification validé au PA-91 avant tout code | utilisateur | oui |
| Révision sur la branche `devenv/revision-2026-11-12`, fusion dans `main` | utilisateur (plan approuvé) | oui |
| Constats de la relecture : tous appliqués (nuances n°12 et n°21) | utilisateur | oui |
| ENV-51 : pas d'oracle (aucun binaire touché) ; un seul mécanisme de relais ; sorties `--json` contrôlées par `json.loads` avant et après ; rootstock d'essai `essais/env-51-essai`, copie d'`essais/env-11/f429zi` | proposition non validée | non |
| ENV-52 : essai du mécanisme git sur un clone temporaire hors rootstock ; scion de la branche dans un venv (pas de pipx avant le tag) ; mesure du gain de téléchargement sur un rootstock neuf `essais/env-52-vierge` | proposition non validée (venv : relecture, forme d'ENV-29) | non |
| ENV-52 : rootstocks d'essai du Mac regreffés en ENV-53, pas en ENV-52 | proposition non validée | non |
| ENV-53 : sort d'`essais/env-39-copie` au PA-93 ; rootstocks d'essai du Mac sans clone projeté regreffés seulement si une tête a changé | proposition non validée (relecture) | non |

## Pièges rencontrés
- La skill `lepton-portage-instructions` cite `references/archetypes-portage.md`, absent de sa copie
  locale (`~/.claude/skills/synced/…/lepton-portage-instructions/`). La révision s'est faite sans.
- La skill est écrite pour `doc/migration/` (ETAPE-N, README) ; ce chantier utilise `doc/devenv/`
  (ENV-N, ORCHESTRATION §6, DEVENV-STATUS) : gabarit repris d'ENV-44, ENV-29 et ENV-50.
- `zsh` : `echo ====` échoue (« = not found », option EQUALS) ; citer la chaîne.
- Sur la graine de référence, lepton refuse `seed add`, `seed replace`, `seed remove`, `seed lock`,
  `scion new` sans `--no-seed` et `scion remove` (`refuse_reference`) : tout essai d'ENV-51 se fait
  sur un rootstock d'essai à graine de projet.
- Premier jet : « `grep -ri lepton scion/` → 0 » ne peut pas tenir (métadonnées de
  `scion/__init__.py`, PA-2 Q7) ; corrigé à la relecture par la forme d'ENV-39.

## Critères de validation
- [ ] PA-89 et PA-90 tranchés et consignés.
- [ ] Inventaire de la tâche 1 au rapport, avec la sortie relevée avant et après.
- [ ] Nouveaux tests : échec sur `main`, réussite sur la branche ; `pytest` complet vert.
- [ ] Sorties `--json` identiques avant et après.
- [ ] `HORS-PLAN.md` : D10 marqué traité, avec renvoi au rapport.

## Reprise
Commande ou première action de la session suivante :
```
démarrer ENV-51 (skill devenv-session) : lire etapes/ENV-51-lepton-messages-scion.md et cette
passation ; branche devenv/env-51 de lepton-tools depuis main ; tâche 1 (audit, lecture seule)
jusqu'au PA-89
```
