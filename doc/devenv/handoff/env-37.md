# Passation ENV-37 — Famille STM32WL : audit et provenance du code tiers — session du 2026-11-06

## Statut
terminée — les quatre ensembles tiers de la famille STM32WL sont audités contre l'amont et ont
chacun leur `LEPTON-PROVENANCE.md`, sans rien changer de compilé ; PA-61 et PA-62 tranchés.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` | fusion de `devenv/env-37` (commit de cette passation compris), poussée avec `devenv/env-37` (PA-62) | oui |
| clone noyau `depots/lepton/original/master` | `master` | 2893297 (non touché) | oui |
| `family-stm32wlxx` `depots/lepton/family-stm32wlxx/master` | `master` | 2340b25 « Fusion de devenv/env-37 … PA-62 », poussé avec `devenv/env-37` (6107dd8) | oui |
| BSP `nucleo-wl55jc1`, famille F4, BSP F429/F439, graine, seed.scions | — | non touchés (ef51ec1, 0fd8b2a, b9fe2bf, 314f91b, 15740f9, 1173d6d) | oui |

`<ROOTSTOCK>` : regreffé (`scion graft --scion lepton@family-stm32wlxx`), **3982 liens** (3978 + 4
`LEPTON-PROVENANCE.md`), 0 lien cassé, 0 fichier régulier ; `lepton -C <ROOTSTOCK> check` code 0.
Les répertoires `<ROOTSTOCK>/build/<preset>` sont ceux de l'oracle après (constructions à neuf).

## Fait pendant la session
- §1 audit (`rapports/env-37-wl-provenance.md` §1, listes et diffs `rapports/env-37-wl-provenance/`) :
  - clones amont dans `~/lepton-tools-dev/tiers/` ; tags résolus en commits ;
  - copies remises aux chemins amont (`preparer-copies.sh`, `~/lepton-tools-dev/essais/env-37-compare/`),
    comparées par `scripts/tiers/verifier-import.sh` (inchangé) à chaque tag candidat ;
  - 225 fichiers : 211 `OK`, 2 `DIFF`, 12 `TROP` ; chaque écart qualifié ;
  - HAL = STM32CubeWL `v1.3.0` (= `stm32wlxx-hal-driver` `v1.3.0` sauf `stm32_hal_legacy.h`) ;
    CMSIS device = `cmsis-device-wl` `v1.1.1` (STM32CubeWL `v1.2.0`) : couple hors de tout tag
    unique ; pile radio = `stm32-mw-subghz-phy` `v1.3.0` (dépôt séparé, non connu à la
    préparation) ; utilitaires = STM32CubeWL `v1.3.0` seul ;
  - 5 fichiers modifiés par Lepton : `radio.c` (`RadioIsChannelFree` rend toujours `false`,
    compilé, absent de la documentation de la migration), `stm32_timer.h`, `subghz.h`,
    `utilities_conf.h`, `platform.h` ;
  - compilés et inclus relevés (`compile_commands.json`, `ninja -t deps`), identiques en embOS et
    FreeRTOS ; références hors famille ; licences ; 0 CRLF ; volume du Mac insensible à la casse.
- PA-61 tranché (§1.9 du rapport, `DEVENV-STATUS.md` §Décisions).
- §2 oracle avant `rapports/oracles/env-37-avant/` conforme à `env-35-apres`.
- §3 4 `LEPTON-PROVENANCE.md` (famille 2255483, a6f517f, d2d5e95, 6107dd8) ; regreffe sur la copie
  d'essai `~/lepton-tools-dev/essais/env-37-copie`, puis sur `<ROOTSTOCK>`.
- §4 oracle après `rapports/oracles/env-37-apres/` : `comparer-oracle.py` code 0 ×16 ; KAL, fumée
  (hors date, jeton UART, place de `rcv SIGCHLD`), `ctest -N` 17/17, mklepton identiques.
- Section « Cas d'épreuve pour ENV-38 » : rapport §5.
- PA-62 : fusions et push (famille, lepton-tools).

## Reste à faire dans l'étape
- [x] Rien. Validation Debian : ENV-43.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Plan de session, dont copie remise à la casse amont, relevé de la casse du volume, section « Cas d'épreuve pour ENV-38 » | utilisateur (plan accepté) | oui (journal) |
| PA-61 : révisions citées (HAL dépôt séparé `v1.3.0` + écart ; CMSIS `v1.1.1` ; radio `stm32-mw-subghz-phy` `v1.3.0` ; utilitaires et `stm32_radio_core_inc/` STM32CubeWL `v1.3.0`, exception étroite au 2026-11-04) | utilisateur | oui |
| PA-61 : fichiers modifiés laissés et décrits (option 1) ; `TROP` tous laissés ; 4 provenances ; manifeste inchangé | utilisateur | oui |
| PA-62 : rapport accepté ; fusions et push | utilisateur | oui |
| Listes `ctest -N` comparées hors la ligne « Internal ctest changing into directory » (dépend du répertoire de lancement) | proposition non validée (méthode) | oui (rapport §2) |
| `ninja -t deps` au lieu de `gcc -H` pour les en-têtes lus | proposition non validée (méthode, équivalente) | non (rapport §1.1) |
| Pour ENV-38 : exigences de la projection tirées du cas WL (renommage de casse, aplatissement, sous-arbre, deux amonts pour un répertoire, fichiers locaux modifiés et hors amont) | proposition non validée | non (rapport §5) |
| Sort fonctionnel de la neutralisation de `RadioIsChannelFree` (documentée, non jugée) | à poser à l'utilisateur hors de cette étape | non |

## Pièges rencontrés
- STM32CubeWL cloné en `--filter=blob:none` : `git checkout <tag> -- <chemins>` échoue parfois
  (« could not fetch … from promisor remote ») → relancer ; les `git show` du script rapatrient
  les objets à la demande.
- Jusqu'à STM32CubeWL `v1.3.0`, HAL et CMSIS device sont des arbres, pas des sous-modules :
  `gh api …/contents` n'y rend pas de commit de sous-module ; comparer les arbres directement.
- zsh ne découpe pas `set -- $s` comme bash : boucles à listes composées lancées par `bash <<'EOF'`.
- `lepton check` exige d'être dans un rootstock : `lepton -C <ROOTSTOCK> check`.
- `ctest -N` lancé depuis `<ROOTSTOCK>/trunk` n'affiche pas la ligne « Internal ctest changing
  into directory » des listes d'`env-35-apres`.
- `grep -i lepton` ne trouve pas toutes les modifications Lepton (`radio.c` n'a aucune marque) :
  seule la comparaison à l'amont est probante.

## Critères de validation
- [x] PA-61 et PA-62 tranchés et consignés.
- [x] Binaires identiques sur host et les 16 presets (code 0).
- [x] Chaque fichier des quatre ensembles est classé dans le rapport ; chaque `DIFF` est qualifié.
- [x] Chaque ensemble tiers de la famille a sa provenance, ou la raison de son absence est
      consignée au PA-61.
- [x] Le rapport contient la section « Cas d'épreuve pour ENV-38 ».

## Reprise
Commande ou première action de la session suivante :
```
démarre la session   # ENV-38 : lire cette passation, etapes/ENV-38-scion-projection-conception.md, rapport env-37 §5, puis PA-63
```
