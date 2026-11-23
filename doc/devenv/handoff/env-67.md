# Passation ENV-67 — Consignes VM : relevés, suppressions, contrôle Mac (D38) — session du 2026-11-23

## Statut
terminée — D38 (1) à (3) traités au Mac (règles du §2bis, enveloppe, skill) ; la preuve sur la VM
se fait en ENV-72.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `devenv/env-67` (depuis `main` 052050c), fusionnée `--no-ff` dans `main` ; `main` et la branche poussées (PA-P, PA-122) | branche : « devenv(env-67): état et passation » ; `main` : fusion de `devenv/env-67`, puis consignation du push | oui |
| clone noyau `depots/lepton/original/master` | `master` | 2b4a647, non touché (lecture seule de `scripts/lepton-env.sh`) | oui |
| autres | seed.scions `master` 49ca4ae (tag 0.6.3.3), graine `original-tree` 15740f9 | non touchés | oui |

Relevez l'état réel de `main` et d'`origin/main` au début de la session suivante.

Outils : Mac : Claude Code **2.1.330** (était 2.1.328), scion 0.6.3.3, lepton 0.1.0, extension 0.5.3 ;
VM inchangée depuis ENV-66 (rien n'y a été fait). `~/tmp-pytest` et `~/tmp-tests` absents au Mac.

## Fait pendant la session
- Audit : `rapports/env-67-consignes.md` §1-4 (variables à défaut silencieux, bornes de
  l'enveloppe, contrôles Mac d'ENV-57, ENV-61, ENV-66).
- Lot (2), 7a54b2d : `scripts/supprimer-essai.sh` admet `~/tmp-pytest` et `~/tmp-tests` et leurs
  descendants ; 18 tests (8 en échec sur `main`, 10 rejets gardés déjà verts), shellcheck 0 ;
  §2bis « Suppressions ».
- Lot (1), 27f5479 : §2bis « Variables d'environnement ».
- Lot (3), cad0172 : §2bis « Contrôle Mac d'une consigne ».
- Contrôles, e38bb30 (rapport §6) :
  - pytest **588** verts ;
  - enveloppe essayée au Mac : 4 admises, 5 rejets en code 2, nettoyage ;
  - 10 décisions `subcommandResults` (`decisions.py`) ;
  - `.claude/settings.json` inchangé (`b01ad557…d235`).
- Skill `lepton-cibles`, 3bc4f9f :
  - l. 22 : défaut silencieux de `LEPTON_EMBOS_ROOT` ;
  - texte préparé par la session (`~/Downloads/lepton-cibles.zip`), importé sur le compte par
    l'utilisateur, synchronisé, puis copié par `scripts/importer-skills.sh`.
- `HORS-PLAN.md` : D38 (1) à (3) traités, (4) hors plan.

## Reste à faire dans l'étape
- Rien. Preuve sur la VM en ENV-72 :
  - consigne `consignes/env-72-debian.md` écrite selon les deux nouvelles règles du §2bis ;
  - §5 : relevé des variables ;
  - §14 : `~/tmp-pytest/env-66` supprimé par l'enveloppe.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-121 (1) : §2bis + relevé au §5, arrêt ; variables `LEPTON_EMBOS_ROOT`, `SCION_REF`, `SCION_SPEC`, `LEPTON_CLONE`, `XDG_CONFIG_HOME`, `NM`, `SIZE` ; `LANG`, `LC_ALL` sans arrêt | utilisateur | oui |
| PA-121 (2) : descendants de `~/tmp-pytest` et `~/tmp-tests` | utilisateur | oui |
| PA-121 (3) : copie d'origine distincte + liste des classes d'écart de l'hôte | utilisateur | oui |
| PA-121 (4) : texte du §2bis tel que proposé ; `CLAUDE.md` inchangé ; skill `lepton-cibles` corrigée | utilisateur | oui |
| PA-122 : rapport accepté ; cibles d'essai supprimées ; skill importée avant fusion ; fusion et push | utilisateur | oui |

## Pièges rencontrés
- `decisions.py` exige le chemin du journal `.jsonl` en premier argument (pas de `--help`).
- Claude Code est passé de 2.1.328 à 2.1.330 sans annonce : il faut relever la version au début de
  chaque session (champ `version` du journal).
- Correction d'une skill : l'utilisateur peut importer sur claude.ai un `.zip` du dossier
  `<nom>/SKILL.md` préparé par la session (hors du dépôt, `~/Downloads`). Puis viennent la
  synchronisation (`claude -p` hors du dépôt), le contrôle de l'empreinte et
  `scripts/importer-skills.sh`.

## Critères de validation
- [x] PA-121 et PA-122 tranchés et consignés.
- [x] Nouveaux tests de l'enveloppe : échec sur `main`, réussite sur la branche ; `pytest` complet
      vert (588).
- [x] Enveloppe : formes admises supprimées, formes rejetées refusées (code 2, rien supprimé),
      décision `allow` relevée (`subcommandResults`).
- [x] ORCHESTRATION §2bis : règles (1) et (3) écrites selon le PA-121 ; paragraphe
      « Suppressions » conforme aux cibles admises par l'enveloppe.
- [x] `HORS-PLAN.md` : D38 (1) à (3) marqués traités, avec renvoi au rapport ; (4) hors plan.

Tickets créés pendant la session : aucun. Lignes restées « ticket à créer après publication
d'ENV-67 » : aucune.

## Reprise
Commande ou première action de la session suivante (étape au choix parmi ENV-68 à ENV-71) :
```
démarre la session ENV-68 (lire handoff/env-67.md)
```
