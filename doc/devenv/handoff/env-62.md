# Passation ENV-62 — Claude Code : règle U3, invites à refuser, outils des consignes VM (D26, D28, D27) — session du 2026-11-18 (préparation)

## Statut
À démarrer. Cette session était hors étape : révision du plan après ENV-61, avec la skill
`lepton-portage-instructions`.
- Les étapes ENV-62 à ENV-66 sont rédigées ; aucune tâche d'ENV-62 n'est exécutée.
- Aucun fichier de l'arbre Lepton, de scion, de lepton, de l'extension ou de `.claude/` n'est
  touché.
- Aucune branche `devenv/env-62` n'existe.

La session qui exécutera ENV-62 remplacera cette passation.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main`, à jour avec `origin/main` ; `devenv/revision-2026-11-18` (depuis `main` 24ca20a), fusionnée `--no-ff` dans `main` (c422a41), les deux poussées (PA-P, accord de l'utilisateur) | `main` : le commit « état et passation » de fin de session (non poussé), au-dessus de 949997f (consignation du push) et c422a41 (fusion) ; branche : 16da928 (révision du plan) | oui |
| seed.scions | `master` | 975caf6 (tag 0.6.3.2), non touché | oui |
| clone noyau `depots/lepton/original/master` | `master` | dfc960b, non touché | oui |
| autres | `master` / `original-tree` | non touchés : graine 15740f9 | oui |

Outils :
- Mac : scion 0.6.3.2, lepton 0.1.0, extension 0.5.2, Claude Code 2.1.327 ;
- VM : scion 0.6.3.2, lepton 0.1.0, extension 0.5.2, Claude Code 2.1.326.

VM : état laissé par R61-1 (`handoff/env-61.md`). `~/.claude/settings.json` y garde ses 3 règles
`allow` utilisateur (D19, PA-103). La décision d'ENV-62 sur D26 (PA-111) est appliquée en ENV-66.

## Fait pendant la session
- Début de session : état conforme à `handoff/env-61.md` (`main` 24ca20a, propre).
- Sources de D21 à D28 lues :
  - `HORS-PLAN.md` (D21 à D28) ;
  - `rapports/env-59-tilde.md` §1.4, §1.6, §5.3 ;
  - `rapports/env-60-scion.md` §1.2, §1.3, §1.9, §2 ;
  - `rapports/env-61-debian.md` §3.2, §9 ; `rapports/env-61-mac.md` §1.3, §5 ;
  - `rapports/env-54-permissions.md` §3 ; `consignes/env-61-debian.md` (`fr()`, l. 172) ;
  - `handoff/env-61.md`.
- Relevés en lecture seule, repris dans les fichiers d'étapes :
  - D21 : `lepton/rootstock.py:226`, `seed.py:375` et `378`, `scions.py:125`, `files.py:94`,
    `generate.py:117` ; forme de référence `seed.py:109` ;
  - D23, D24 : `extension/src/lepton.ts:22`, `watch.ts` (F2 l. 96-100 sans filtre, trunk
    l. 107-110 avec `recentlyBusy`), `runner.ts:21`, `commands.ts:120-127`, `package.json:5` ;
  - D22, D25 : `scion/gitops.py:37` (`_run`, dernière ligne de stderr) ; `scion/graft.py:57`
    (`sync`), `275` (`_fetch`), `342` (`clone_updates`), `383` (`_check_clone`) ;
    `scion/cli.py:96` (`_clone_seed`) ;
  - D26 à D28 : `.claude/settings.json` (7 `allow`, 5 `ask`, 5 `deny`) ;
    `rapports/env-57-mac/decisions.py`, `env-56-scion/fixture.py`.
- Décisions de l'utilisateur, sur questions posées :
  - D22 et D25 : une étape, deux lots, un tag ;
  - D23 et D24 : une étape, deux lots, une version de l'extension ;
  - D26 à D28 : une étape en tête, décisions sur la VM appliquées à la validation Debian ;
  - validation Debian groupée en dernière étape.
- Fichiers d'étapes :
  - `etapes/ENV-62-claude-code-regles-consignes.md` ;
  - `ENV-63-lepton-chemins-tilde.md` ;
  - `ENV-64-extension-path-purge.md` ;
  - `ENV-65-scion-clone-existant-message.md` ;
  - `ENV-66-validation-debian.md`.
- Autres documents mis à jour :
  - ORCHESTRATION §2, §4 (PA-111 à PA-120), §5bis et §6 ;
  - `DEVENV-STATUS.md` : étapes, décision, prochaine action, journal ;
  - `HORS-PLAN.md` : D21 à D28 planifiés.
- Relecture par un agent indépendant (ORCHESTRATION §5bis, effort `xhigh`, lecture seule) :
  0 bloquant, 13 à corriger, 14 suggestions. La session a vérifié les principaux constats (n° 1,
  2, 3, 4, 7, 8, 26), tous confirmés ; tous appliqués sur décision de l'utilisateur. Détail au
  journal de `DEVENV-STATUS.md` (2026-11-18).

## Reste à faire dans l'étape
- [ ] Tâche 1 : audit et essai témoin, jusqu'au PA-111.
- [ ] Tâche 2 : amendement du §2bis et mise en place selon le PA-111.
- [ ] Tâche 3 : contrôles, PA-112.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Découpage ENV-62 (D26, D28, D27), ENV-63 (D21), ENV-64 (D23, D24), ENV-65 (D25, D22), ENV-66 (Debian) ; ordre 62, puis 63, 64 et 65 permutables, 66 | utilisateur | oui |
| ENV-62 : lieu de l'essai de D26 (`.claude/settings.local.json` du Mac, réglages utilisateur du Mac, ou VM en ENV-66) | proposition non validée (plan de session d'ENV-62) | non |
| ENV-62 : parades de D28 (annonce « À REFUSER », cible absente, contrôle non interactif) ; sort du défaut « ne plus demander » | proposition non validée (PA-111) | non |
| ENV-62 : amendement du §2bis pour D27 (`LC_ALL=C`, traductions de `po/fr.po`, segment d'hôte, contrôle vérifié contre le code installé) ; outil commun éventuel | proposition non validée (PA-111) | non |
| ENV-63 : `~` développé comme au PA-105, ou refusé ; portée sur les 6 chemins | proposition non validée (PA-113) | non |
| ENV-64 : options de D24 (`recentlyBusy`, relecture de `seed status`, message seul) ; version 0.5.3 | proposition non validée (PA-115) | non |
| ENV-65 : options de D25 (refus forme P-V1, checkout, reclonage) et de D22 (ligne `fatal:`, première ligne, sortie sous `-v`) ; version 0.6.3.3 ou 0.6.4.0 | proposition non validée (PA-117) | non |
| ENV-66 : critères C1 à C9 ; D24 dans VSCodium sur la VM | proposition non validée (PA-119) | non |

## Pièges rencontrés
- Les numéros de ligne de D21 dans `HORS-PLAN.md` (`seed.py:369`, `372`) datent d'avant 74c9c97 :
  ce sont aujourd'hui les lignes 375 et 378.
- Piste pour D26, non vérifiée : le mode auto écarte les « Wildcarded interpreters like
  `Bash(python*)` » (`rapports/env-54-permissions.md` §3, point 2). L'audit d'ENV-62 l'établit ou
  l'écarte.
- Une lecture groupée qui cite une commande `ask` déclenche l'invite (ENV-54 §10.2, O-0) :
  chercher par l'outil Grep.
- `.claude/settings.local.json` du Mac porte 3 `allow` non documentés jusqu'ici
  (`Bash(git fetch *)`, `Bash(echo "code=$?")`, un `Read(…)` sous `essais/env-60-fixture/`) :
  un essai de règles au Mac n'est pas comparable à la VM sans en tenir compte.
- Node.js est absent de la VM : un essai `node` de l'extension n'y tourne pas (PA-119).

## Critères de validation
- [ ] PA-111 et PA-112 tranchés et consignés.
- [ ] D26 : cause établie, ou essai qui la laisse ouverte, et décision relevée au rapport.
- [ ] D28 : inventaire des invites à refuser ; rejeu de « ne plus demander » sous 2.1.327.
- [ ] D27 : chaque défaut avec sa parade au §2bis, ou dans l'outil commun.
- [ ] `settings.json` en JSON valide s'il change ; `pytest` complet vert.
- [ ] `HORS-PLAN.md` : D26 et D28 « décidé, appliqué en ENV-66 », D27 traité, avec renvoi au
      rapport.

## Reprise
Commande ou première action de la session suivante :
```
démarre la session ENV-62 (skill devenv-session) : lire etapes/ENV-62-claude-code-regles-consignes.md
et cette passation ; branche devenv/env-62 de lepton-tools depuis main ; tâche 1 jusqu'au PA-111
```
