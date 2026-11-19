# Passation ENV-62 — Claude Code : règle U3, invites à refuser, outils des consignes VM (D26, D28, D27) — session du 2026-11-19

## Statut
Terminée. D26 et D28 sont décidés et seront appliqués en ENV-66. D27 est traité ; la preuve sur la
VM se fera en ENV-66. PA-111 et PA-112 sont tranchés. Rapport : `rapports/env-62-claude-code.md`.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` : fusion `--no-ff` de `devenv/env-62` (depuis `main` c514033) ; `main` et `devenv/env-62` poussées (PA-P, accord de l'utilisateur) | branche : « devenv(env-62): état et passation » ; `main` : commit de fusion | oui |
| clone noyau `depots/lepton/original/master` | `master` | dfc960b, non touché | oui |
| autres | seed.scions `master` 975caf6 (tag 0.6.3.2), graine `original-tree` 15740f9 | non touchés | oui |

Outils :
- Mac : Claude Code **2.1.328**, scion 0.6.3.2, lepton 0.1.0, extension 0.5.2.
- VM : processus Claude Code **2.1.325** pendant R61-1 (champ `version` du journal), 2.1.326
  installé sur disque ; rien n'a été fait sur la VM dans cette étape.

Réglages du Mac : `~/.claude/settings.json` revenu à son empreinte d'avant (`561789c8…25ce2`).
`.claude/settings.json`, `.claude/settings.local.json` et `~/.claude.json` n'ont pas changé.

## Fait pendant la session
- D26 (rapport §1). Agent `claude-code-guide` pour la documentation et le CHANGELOG. Nouvel
  outil `rapports/env-62-claude-code/raisons.py`, qui relève aussi `reasonCode` et `grantScope`.
  - Essai à chaud T1-T7 : tout passe au classifieur, même le `deny`. Conclusion :
    `~/.claude/settings.json` n'est lu qu'au démarrage de la session.
  - L'utilisateur a relancé Claude Code (`claude --continue`), puis l'essai a été rejoué :
    - règle à joker `Bash(python3 -m unittest discover *)` : classifieur (T1, T2, T3b) ;
    - règle exacte sur la même commande : `subcommandResults` (T5) ;
    - `pipx install` exact : `rule userSettings` (T6) ;
    - `deny` exact : `reject rule userSettings` (T7).
  - Cause : en mode auto, une règle à joker sur un interpréteur est écartée. Le `~` et la source
    de la règle n'y changent rien.
  - Journal U3 de la VM, copié par l'utilisateur dans `~/Documents/` : pas de `reasonCode`, et
    processus en 2.1.325.
- D28 (§2). Inventaire : 4 confirmations par erreur, toutes sans effet, aucune annoncée juste
  avant le lancement.
  - Rejeu sous 2.1.328 : l'invite d'une règle `ask` ne propose plus « ne plus demander »
    (`user_temporary`, `grantScope once`). L'invite suivante paraît ; elle a été refusée.
    Empreintes inchangées.
- D27 (§3). Les 4 défauts sont décrits, avec un tableau des outils (`LC_ALL`, `<HOME>`, segment
  d'hôte, traductions). `po/fr.po` de git v2.47.3 contient U+00A0 après « fatal ».
- Mise en place :
  - `scripts/comparer-releves.py` et `tests/test_comparer_releves.py` (10 tests) ;
  - `rapports/env-56-scion/fixture.py` : `LC_ALL=C` et ancêtres de `<HOME>` sous
    `depots/.mirrors/<hôte>/` en `<HOME/..>`. Rejouée au Mac : 76 relevés, seul le nom de la base
    change ;
  - ORCHESTRATION §2bis : réglages utilisateur de la VM (2 règles), lecture des réglages au
    démarrage, invites à refuser, outils de comparaison.
- Contrôles :
  - sorties réelles de la VM `env-61-debian/11-fixture56/` : **0 / 76** écart avec l'outil ;
  - pytest **537** ; la règle pytest du dépôt reste appliquée sous 2.1.328.
- `HORS-PLAN.md` : D26 et D28 « décidé en ENV-62, appliqué en ENV-66 » ; D27 « traité en ENV-62,
  preuve sur la VM en ENV-66 ». Aucun ticket.
- `essais/env-62-essai` supprimé par `scripts/supprimer-essai.sh`.

## Reste à faire dans l'étape
- Rien.
- Pour ENV-66 :
  - §0 de la consigne : l'utilisateur retire `Bash(python3 -m unittest discover *)` de
    `~/.claude/settings.json` de la VM avant d'ouvrir la session. Bloc attendu : rapport §5 ;
  - U3 attendu au classifieur, avec un contrôle positif d'une règle utilisateur (forme de T6) ;
  - invites à refuser annoncées « À REFUSER » par `AVANCEMENT` avant le lancement ;
  - comparaisons de la fixture par `scripts/comparer-releves.py` (`--home-attendu`,
    `--home-obtenu`), sans `fr()` ;
  - version de Claude Code de la VM lue au champ `version` du journal.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Plan de session : règle d'essai dans `~/.claude/settings.json` ; rejeu sous 2.1.328 ; PA-P pour les invites sur cibles absentes ; journal U3 copié par l'utilisateur | utilisateur | oui |
| Relance de Claude Code pour l'essai D26 | utilisateur | oui (journal) |
| PA-111 : cause de D26, règle de la VM retirée au §0 d'ENV-66, règles du dépôt inchangées ; parade D28 (annonce et cible absente), défaut documenté seulement ; amendement D27 ; fixture et outil commun ; ni `CLAUDE.md` ni skills | utilisateur | oui |
| PA-112 : rapport accepté, essai supprimé, fusion et push | utilisateur | oui |

## Pièges rencontrés
- `~/.claude/settings.json` modifié pendant la session → sans effet, même un `deny` → il n'est lu
  qu'au démarrage : relancer (`claude --continue` garde la conversation et le journal).
- Une règle retirée de `~/.claude/settings.json` reste chargée dans le processus en cours.
- `claude --version` donne la version installée, pas celle du processus → lire le champ
  `version` du journal.
- `touch` sous `essais/` → décision `mode` (écriture dans un répertoire de travail) : ce n'est
  pas un témoin de règle. Prendre une commande hors des répertoires de travail (`pipx install`
  sur une cible absente).
- zsh : un joker non protégé sans correspondance (`-p env62_*.py`) empêche de lancer la
  commande → le protéger par des guillemets.
- Le dossier iCloud de sauvegarde de `~/.claude/` est illisible pour la session (« Operation not
  permitted ») : l'archive du hook n'a pas pu être vérifiée par la session.

## Critères de validation
- [x] PA-111 et PA-112 tranchés et consignés.
- [x] D26 : cause établie, et décision relevée au rapport.
- [x] D28 : inventaire des invites à refuser ; rejeu de « ne plus demander » (sous 2.1.328, décision
      de l'utilisateur).
- [x] D27 : chaque défaut avec sa parade ; 0 écart sur les sorties réelles de la VM.
- [x] Fichiers de réglages du Mac revenus à leur empreinte d'avant ; `settings.json` inchangé ;
      `pytest` complet vert.
- [x] `HORS-PLAN.md` : D26 et D28 « décidé, appliqué en ENV-66 », D27 « traité en ENV-62, preuve
      sur la VM en ENV-66 », avec renvoi au rapport.

## Reprise
Commande ou première action de la session suivante :
```
démarre ENV-63 avec la skill devenv-session (ENV-63, ENV-64, ENV-65 permutables ; ENV-63 conseillée avant ENV-64)
```
