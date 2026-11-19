# Passation ENV-66 — Validation Debian groupée (ENV-62 à ENV-65) — session du 2026-11-19

## Statut
Terminée, et avec elle le plan. R66-1 donne `FIN-SUCCÈS`, vérifié par la session Mac :
- C1 à C7 atteints ;
- C8 écarté ;
- C9 partiel.

D21 à D28 sont prouvés sur la VM, D28 avec un écart. PA-119 et PA-120 sont tranchés.

Rapports :
- `rapports/env-66-mac.md` (préparation, tâche 3, contrôle §3bis, journal des messages §4) ;
- `rapports/env-66-debian.md` (VM).

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` : fusion `--no-ff` de `devenv/env-66` (depuis `main` 6bc05ad), qui contient la fusion de `devenv/env-66-debian` (9f34370, VM) ; `main` 7f9e9c0 et `devenv/env-66` 4bbd23f poussées (PA-120). Puis, sur `main`, un commit local **non poussé** « devenv(hors-etape): fin du plan, A3 reconfirmé hors plan ; passation » (push à faire sur accord, PA-P) | `main` : ce commit | oui |
| clone noyau `depots/lepton/original/master` | `master` 2b4a647 (inchangé dans l'étape) | « Fusion de devenv/env-65 (…) » | oui |
| autres | seed.scions `master` 49ca4ae, tag 0.6.3.3 ; graine `original-tree` 15740f9 ; non touchés | — | oui |

Outils :
- Mac : scion 0.6.3.3, lepton 0.1.0, extension 0.5.3, git 2.50.1, Claude Code 2.1.328.
- VM :
  - scion 0.6.3.3, lepton 0.1.0 (D21), extension 0.5.3 ; le répertoire 0.5.2 reste dans `~/.vscode-oss/extensions` ;
  - git 2.47.3, Claude Code 2.1.328 ;
  - `~/.claude/settings.json` à 2 règles `allow`.
- Rootstocks regreffés (noyau 2b4a647) :
  - VM : `essais/env-28-debian`, `env-13-debian`, `env-53-c5`, `env-53-debian` ;
  - Mac : `essais/env-13-vierge`, `env-9`, `env-11/{qemu,qemu-gra2,bout-en-bout/rootstock,f429zi,wl55jc1}`.
- `<ROOTSTOCK>` n'est pas regreffé : 3889 liens, `CONFORME`.

Laissé en place :
- Mac :
  - `~/lepton-tools-dev/essais/env-66-essai` (copies c4, c4t, c5, d23cwd, `depot65`, clone de seed.scions, `vsix`) ;
  - `~/lepton-tools-dev/essais/env-66-fixture` ;
  - `~/lepton-tools-dev/essais/env-66-mac` (journaux, `git-po/fr.po`, regreffes).
  Ils sont à supprimer par `scripts/supprimer-essai.sh` si l'utilisateur le décide.
- VM : `~/env-66-journaux`, `~/tmp-pytest/env-66` et `~/tmp-pytest/env-61` (D38).

## Fait pendant la session
- **Préparation** (`rapports/env-66-mac.md` §1) :
  - `env-66-mac/ls-remote.sh` : seul le noyau change côté greffons (2b4a647, hors `scion/`) ;
  - attendus `env-66-mac/attendu/` : C3 (`graft-update` d'`essais/env-13-vierge`), C4 (`chemins.sh`, 4ᵉ argument ajouté : nom de clangd), C5 (`essai.sh`, 3 fixtures = `*-apres/` d'ENV-65), D23 (`d23.cjs`, même sortie sous le runtime de VSCodium) ;
  - `scripts/comparer-releves.py` : 4 traductions tirées de `po/fr.po` v2.47.3, tests d'abord (13) ;
  - pytest 570 ; consigne `consignes/env-66-debian.md`.
- **R66-1** : ORDRE (consigne par chemin, commit et sha256), ACCUSÉ, FIN-SUCCÈS ; détail au §4 du rapport Mac. Tous les relevés poussés ont été recomparés au Mac (§3bis).
- **Tâche 3** : 7 rootstocks d'essai du Mac regreffés. Seul le noyau avance, les liens sont inchangés, `check` donne 0 (`qemu-gra2` : 1, attendu). Le `graft-remove` de `qemu-gra2` a été lancé par l'utilisateur.
- **Fusions et push** (PA-120).
- **`HORS-PLAN.md`** : D21 à D28 prouvés sur la VM ; D34 à D40 ajoutés.

## Reste à faire dans l'étape
- Rien dans l'étape. Fin du plan : présentation de `HORS-PLAN.md` commencée. A3 a été
  reconfirmé hors plan. Restent A1, A2, A4, D4, D12, D29, D30, D32, D33 et D35 à D40, que
  l'utilisateur reporte à la session suivante. D34 est hors plan depuis le PA-120 ; D31 a été
  traité en ENV-64.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Plan de session ; PA-P pour le `graft-update` d'`essais/env-13-vierge` en préparation | utilisateur | oui |
| PA-119 : consigne validée, §0 (règle `unittest` retirée de la VM par l'utilisateur), C3, C5 (3 fixtures), C6 (D23 par le runtime de VSCodium, D24 sur la VM), C7 maintenu, C8 écarté, C9 ; push et ordre | utilisateur | oui |
| Pendant R66-1 : regreffe des 6 rootstocks du Mac ; A1 rejouée ; ligne de git « point de montage » admise ; §12.1 rejoué avec `LEPTON_EMBOS_ROOT` ; T3 rejoué (option c) ; push de `devenv/env-66-debian` | utilisateur | oui |
| PA-120 : fusions et push ; D34 hors plan | utilisateur | oui |
| Fin du plan : A3 reconfirmé hors plan ; autres points reportés à la session suivante | utilisateur | oui |
| Ordre envoyé par référence (chemin, commit, sha256) et non recopié (52 Ko) | session (forme du tableau §2bis ; non contestée) | oui (rapport Mac §4) |
| D35 à D40 : constats inscrits pour la présentation de fin du plan ; pistes (première ligne `fatal:`, relevé de `LEPTON_EMBOS_ROOT`, invites non simultanées) | proposition non validée | oui (`HORS-PLAN.md`) |

## Pièges rencontrés
- **Deux invites de sens opposé en même temps** : une regreffe à confirmer au Mac, A1 à refuser sur la VM. A1 a été confirmée par erreur. Parade : aucune invite au Mac pendant que la VM en présente (D39).
- **`LEPTON_EMBOS_ROOT`** est absente d'une session VM rouverte : les presets embOS échouent à la configuration. À relever au §5 des consignes (D38).
- **Contrôle Mac d'une consigne rejoué sur le même rootstock d'origine** : il ne révèle ni la racine, ni la graine, ni les `.DS_Store` propres au Mac (D38).
- **T3 de D24** : un greffon ajouté au terminal pendant que VSCodium est ouvert n'est pas observé. Ouvrir VSCodium après le `seed add` (D36).
- **Greffon déclaré dont le clone a disparu** : lepton ne le retire ni ne le réajoute (D37).
- **git 2.47.3 avec `--single-branch`** : la première ligne de stderr est un avertissement (D35).
- **`/home` sur un système de fichiers distinct (VM)** : git change de message (D34).
- **`supprimer-essai.sh`** refuse `~/tmp-pytest/<sous-répertoire>` (D38).
- **Hook du plugin `lepton-tickets`** : il n'analyse pas un heredoc Python qui contient des guillemets. Passer par un script dans le répertoire temporaire de la session.
- **Edit sur un fichier qui contient des U+00A0 littéraux** : la chaîne ne correspond pas. Passer par un script Python.

## Critères de validation
- [x] PA-119 et PA-120 tranchés et consignés.
- [x] `FIN-SUCCÈS R66-1` vérifié par la session Mac ; C1 à C9 conformes, ou écartés au PA-119 (C8). Exception : C9 partiel, `~/tmp-pytest/env-61`, D38.
- [x] D26 : U3 décidé par le classifieur, conforme au PA-111 ; réglages de la VM conformes (2 règles).
- [x] D28 : la confirmation par erreur d'A1 est consignée (première invite), puis A1 a été refusée au rejeu.
- [x] D27 : les comparaisons sont faites par `comparer-releves.py`. Aucune n'est faussée par la langue ou par le segment d'hôte. La variante « point de montage » est admise à la main (D34).
- [x] Rootstocks d'essai regreffés : 0 lien cassé, 0 fichier régulier ; `check` 0 (`qemu-gra2` : 1).
- [ ] Fin du plan : `HORS-PLAN.md` présenté à l'utilisateur pour décision. La présentation est
      commencée (A3 tranché) ; les autres points sont à la session suivante.

Tickets créés pendant la session : aucun. Lignes de `HORS-PLAN.md` restées « ticket à créer après
publication d'ENV-66 » : aucune.

## Reprise
Commande ou première action de la session suivante :
```
poursuis la présentation de HORS-PLAN.md pour décision (fin du plan ; A3 déjà tranché), puis révise le plan si des points sont retenus
```
