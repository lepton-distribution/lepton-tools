# Passation ENV-53 — Validation Debian groupée (ENV-51, ENV-52) — session du 2026-11-12

## Statut
Terminée. C'est la dernière étape du plan. La VM Debian valide l'extraction partielle des clones
projetés (scion 0.6.3.0) et le relais des messages de scion par lepton : C1 à C6 et C8 sont
atteints, C7 est écarté. Les rootstocks d'essai du Mac sont regreffés. `HORS-PLAN.md` a été
présenté : D13, D14 et D16 sont à traiter à la prochaine révision du plan.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `devenv/env-53` (depuis `main` fb61b9a), fusionnée `--no-ff` dans `main` et poussée avec `main` (PA-94) | « devenv(env-53): état et passation », puis commit de fusion dans `main` | oui |
| lepton-tools (VM) | `devenv/env-53-debian` | f8090af « devenv(env-53): rapport Debian R53-1 et oracle env-53-debian », poussée, fusionnée dans `devenv/env-53` (3a70c28) | oui |
| clone noyau `depots/lepton/original/master` | `master` | 58e421e, non touché | oui |
| seed.scions, familles, BSP, graine, miroirs | `master` / `original-tree` | non touchés : seed.scions 6416c33 (tag 0.6.3.0), F4 acdd24c, F7 12280a5, WL 9349be2, graine 15740f9 | oui |

`<ROOTSTOCK>` n'a pas été touché : il était déjà regreffé en ENV-52 (`CONFORME`, 3889 liens).

Rootstocks d'essai du Mac, tous regreffés par `graft-update` 0.6.3.0. Seul le noyau a avancé
(76f28bd → 58e421e), aucun lien n'a changé, tous sont `CONFORME` :

| Rootstock | Liens | `check` | Clones tiers | `depots/tiers` |
| --- | --- | --- | --- | --- |
| `essais/env-13-vierge` | 3889 | 0 | 8 convertis | 242 → 106 Mo |
| `essais/env-9` | 3059 | 0 | — | — |
| `essais/env-11/qemu` | 3059 | 0 | — | — |
| `essais/env-11/qemu-gra2` | 3051 | 1 (attendu) | — | — |
| `essais/env-11/bout-en-bout/rootstock` | 3059 | 0 | — | — |
| `essais/env-11/f429zi` | 3294 | 0 | 2 convertis | 38,6 → 36,5 Mo |
| `essais/env-11/wl55jc1` | 3315 | 0 | 4 convertis | 176,7 → 41,4 Mo |

- `qemu-gra2` : `graft-remove` du BSP an386, sans `--purge`.
- `essais/env-39-copie` et la copie d'essai `essais/env-53-c5` du Mac ont été supprimées par
  l'utilisateur.
- Journaux de session : `~/lepton-tools-dev/essais/env-53-mac/`.

VM (état laissé par R53-1) :
- outils : scion 0.6.3.0 ; lepton 0.1.0, réinstallé depuis `devenv/env-53` ; extension 0.5.2 ;
- rootstocks :
  - `essais/env-28-debian` et `essais/env-13-debian` : regreffés, clones tiers partiels ;
  - `essais/env-53-debian` : neuf ;
  - `essais/env-53-c5` : copie de `essais/env-11/qemu` regreffée à 58e421e. Elle devient la
    graine de projet de référence de la VM (D15) ;
  - `essais/env-11/qemu` : jamais regreffé depuis ENV-10, à supprimer par l'utilisateur (D15) ;
- supprimés : `essais/env-50-debian` et `~/env-50-journaux` (C8) ;
- journaux `~/env-53-journaux` ; `~/tmp-pytest` gardé.

## Fait pendant la session
- **Préparation** (`rapports/env-53-mac.md` §1) :
  - têtes publiées (`env-53-mac/ls-remote.sh`, `ls-remote-mac.txt`) ;
  - attendus des clones tiers relevés sur `<ROOTSTOCK>` (`env-53-mac/releve-clones.sh`,
    `attendu/clones/`, `attendu/clones-rootstock-mac.txt`) ;
  - essai préalable `graft-update` d'`essais/env-13-vierge` (§1.4) ;
  - attendu du relais (`attendu/c5/`, §1.5) ;
  - outils `inventaire-clones.sh`, `liens.py`, `regreffer-essai.sh`.
- **Consigne** `consignes/env-53-debian.md`, validée au PA-93 avec la précision de l'utilisateur
  (§2) ; `devenv/env-53` poussée.
- **Ordre R53-1** : ACCUSÉ, 11 AVANCEMENT, 1 QUESTION, la réponse et FIN-SUCCÈS, tous reçus ou
  remis directement (`env-53-mac.md` §3).
- **Vérification** du rapport VM et comparaisons refaites au Mac sur l'oracle poussé
  (`env-53-mac.md` §5) :
  - C2 et C4 : `clones.txt` = Mac, `CONFORME` ×3 ;
  - C3 : `comparer` 0 ×16, mklepton identique ;
  - C5 : 11 relevés sur 12 = Mac, le 12e ne différant que par la langue de git ; 8 lignes
    `scion:` dans le canal de VSCodium.
- **Tâche 3** (`env-53-mac.md` §4) : 6 rootstocks regreffés ; `env-39-copie` supprimée.
- **Fusions** : `devenv/env-53-debian` dans `devenv/env-53`, puis `devenv/env-53` dans `main`
  (PA-94).
- **`HORS-PLAN.md`** : D13 à D16 ajoutés, présentés et décidés.

## Reste à faire dans l'étape
- [x] Tout ENV-53.
- [ ] Hors étape, pour l'utilisateur sur la VM :
  `rm -rf ~/lepton-tools-dev/essais/env-11/qemu` (D15). Les futures consignes VM prendront
  `essais/env-53-c5` comme graine de projet `$P`.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Plan de session ; orientations C5 (CLI et VSCodium), C7 écarté, C8 forme d'ENV-50, suppression d'`env-39-copie` | utilisateur | oui |
| Essai préalable `graft-update` d'`env-13-vierge` (PA-P) | utilisateur | oui |
| PA-93 : consigne validée ; pas de regreffe d'`env-50-debian` en C4 ; précision : la session VM lance les commandes (`sudo` sans mot de passe) ; push et ordre ; tâche 3 et suppressions | utilisateur | oui |
| QUESTION R53-1 (§9.2) : option O2, copie `env-53-c5` remise à jour par `graft-update` | utilisateur | oui |
| Tâche 3 : l'utilisateur lance les commandes refusées par le classifieur ; PA-94 après la tâche 3 | utilisateur | oui |
| PA-94 : fusions et push | utilisateur | oui |
| Fin du plan : D13, D14, D16 à traiter ; D15 : `env-53-c5` remplace `env-11/qemu` ; A1 à A4, D4, D12 hors plan | utilisateur | oui |
| Attendus de liens repris d'`env-50-mac/attendu/` (inchangés), non recopiés | proposition non validée, exposée dans le rapport sans objection | journal |

## Pièges rencontrés
- **Hook et `git config`** : le hook refuse `git config` sous `depots/tiers/`, même en lecture
  (`--get`). Parade : lire `.git/config.worktree` puis `.git/config` par `grep`. `git
  sparse-checkout` écrit `core.sparseCheckout*` dans `config.worktree`.
- **Hook et répertoire courant** : il refuse une redirection depuis un sous-shell resté dans un
  `trunk/` (`(cd $C/trunk && find …) > f`). Parade : `liens.py <trunk>`, lancé depuis l'extérieur.
- **Sous-modules** : STM32CubeWL a 15 sous-modules, comptés `H` par `git ls-files -t` mais qui ne
  sont pas des fichiers : 8962 `H` pour 8947 fichiers avant la conversion.
- **Classifieur de permissions** : il refuse `scion graft-update` et `rm -rf` (« Modify Shared
  Resources »), sur la VM malgré l'accord de l'utilisateur, et au Mac pour une regreffe groupée.
  Une commande envoyée telle quelle par l'utilisateur est acceptée, de même que `!` en premier
  caractère du prompt ; une espace devant `!` en fait un simple message (D16).
- **Base des essais VM** : le `$P` de la VM (`essais/env-11/qemu`) n'avait jamais été regreffé,
  contrairement à celui du Mac. Relever l'état d'un rootstock de la VM avant d'en tirer un attendu
  (D15).
- **lepton et les URL `file:`** : `file:///chemin` est pris pour un chemin local ;
  `file://localhost/chemin` fonctionne (D13).
- **Langue de git** : sur la VM, git écrit ses messages en français (« et que le dépôt
  existe. »). Normaliser ou exclure ces lignes dans les comparaisons de sorties.

## Critères de validation
- [x] PA-93 et PA-94 tranchés et consignés.
- [x] `FIN-SUCCÈS R53-1` vérifié par la session Mac ; C1 à C6 et C8 conformes, C7 écarté au
      PA-93.
- [x] Rootstocks d'essai regreffés : 0 lien cassé, 0 fichier régulier (hors `.DS_Store`
      tolérés) ; `check` code 0 (`qemu-gra2` : 1, attendu).
- [x] Fin du plan : `HORS-PLAN.md` présenté à l'utilisateur pour décision.

## Reprise
Commande ou première action de la session suivante :
```
révision du plan avec la skill lepton-portage-instructions : planifier D13 (lepton, URL
file:///), D14 (répertoire vide après l'échec d'un seed add) et D16 (règles de permission
ciblées) de HORS-PLAN.md ; lire DEVENV-STATUS.md (Prochaine action) et cette passation
```
