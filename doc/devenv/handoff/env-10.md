# Passation ENV-10 — Script d'installation de VSCodium — session du 2026-10-15 (S2)

## Statut
terminée (2026-10-15) — script validé sur Mac Intel et Debian 13 (VM vierge, passage n° 3) ;
Apple Silicon en revue seule ; trois défauts communs corrigés en cours de validation.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `devenv/env-10` (poussée, `origin` = `git@github.com:lepton-distribution/lepton-tools.git`) | `devenv(env-10): état et passation` (clôture), précédé de e9b5518 ; `main` = f6bb974 (poussée) | oui |
| lepton-tools | `devenv/env-10-debian` (VM, distante seulement) | e45f746 rapport passage n° 3 — fusionnée dans `devenv/env-10` (25ff090) | — |
| clone noyau `depots/lepton/original/master` | `devenv/env-10` (extraite dans `~/lepton`, poussée) | 1b2f7b6 `SCION_REF` et `SCION_SPEC` surchargeables ; `master` = 42733ce (poussée, avance rapide depuis 6b62af5) | oui |
| seed.scions | `master` 79f4f96 + tag `0.5.1.0` (poussés par l'URL SSH ; `origin` HTTPS inchangé) | — | oui |
| BSP, familles, graine de travail | inchangés depuis S1 | — | oui |

## Fait pendant la session
- PA-P : dépôt GitHub `lepton-tools` créé par l'utilisateur ; push des trois dépôts (`git ls-remote`
  = têtes locales).
- Consigne VM autonome `doc/devenv/consignes/env-10-debian.md` (passages n° 1 à n° 3) ; transmise
  par git puis par Remote Control (SendMessage) au passage n° 3.
- Passage VM n° 1 → défaut `installer_extensions` sur hôte sans extension (code 1 muet) ;
  reproduit sur le Mac (`HOME` vide, dry-run) ; corrigé 9321eed.
- Passage VM n° 2 → `--seed-scions` produisait `git+file://…@REF`, refusé par pipx 1.7.1 ;
  reproduit avec pipx 1.7.1 dans un venv jetable ; forme `scion @ git+file://…` + SC2015 : 1b43b0b.
  Essai « hôte vierge » réel sur le Mac (pipx 1.7.1, `PIPX_HOME` temporaire) : 12 puis 0
  changement (`env-10-validation.md` §6).
- Passage VM n° 3 conforme (`rapports/env-10-debian.md`) : 13 puis 0 changement, INS-1 à INS-6.
- Rapport Debian §6.4 : message curl 23 et place temporaire documentée (e9b5518) ; essais des deux
  chemins d'erreur, exécution Mac 0 changement, `shellcheck` sans remarque, `pytest -q` 116 passed
  (`env-10-validation.md` §7).

## Reste à faire dans l'étape
- Rien. Reliquats pour la suite :
  - [ ] ENV-11 : choix effectif de lemminx natif dans l'éditeur (Java présent sur le Mac, CFG-7).
  - [ ] Défaut `SCION_REF` 0.5.0.1 d'`install-macos.sh` / `install-debian.sh` (clone noyau) à
        relever en 0.5.1.0 (tag désormais sur GitHub).
  - [ ] Information, non traitée : ligne « openocd » vide dans le récapitulatif d'`install-debian.sh`
        (`--version` sur la sortie d'erreur) ; Graphify non installé sous Debian (optionnel).
  - [ ] Apple Silicon : aucune exécution réelle (revue seule, `env-10-validation.md` §4).

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Plan de session S2 (push, attente du rapport VM, clôture) | utilisateur | oui |
| PA-P : création du dépôt GitHub, push `main` + `devenv/env-10` (lepton-tools), `master` + `devenv/env-10` (noyau), `master` + tag (seed.scions) ; puis chaque push de `devenv/env-10` | utilisateur | oui |
| Consigne VM écrite dans le dépôt | utilisateur (demande) | oui (journal) |
| Corrections 9321eed, 1b43b0b (+ SC2015), e9b5518 ; protocole « hôte vierge » | utilisateur | oui |
| `--with-debug-tools` toujours passé | utilisateur (validée) | oui |
| Commentaire de 1b43b0b limité aux versions constatées (pipx 1.7.1 refuse, 1.17.12 accepte) | proposition appliquée | non (commit) |

## Pièges rencontrés
- pipx : `git+file:///chemin@REF` refusé par pipx 1.7.1 (URL sans hôte), accepté par 1.17.12 →
  toujours la forme nommée `nom @ git+file://…`.
- Un essai sur un Mac déjà installé ne parcourt pas les chemins « première installation » (scion
  trouvé, extensions présentes) → essai « hôte vierge » : `HOME`, `PIPX_HOME`, `PIPX_BIN_DIR`
  temporaires, pipx de la version cible en tête du `PATH`, `~/.local/bin` hors `PATH`.
- `--dry-run` n'appelle pas pipx : il ne révèle pas un refus de spécification.
- VM : `/tmp` de 747 Mo → curl code 23 sur le `.deb` (168 Mo) ; parade `TMPDIR=$HOME/…`.
- Remote Control : la remise d'un message à la session VM n'est pas confirmée ; la réponse arrive
  comme message inter-sessions.

## Critères de validation
- [x] PA-10 tranché ; `extensions.lst` épinglé.
- [x] `codium --list-extensions --show-versions` = `extensions.lst` sur Mac et Debian.
- [x] Deux exécutions successives sans erreur ni changement (INS-4) : Mac et Debian (hôte vierge).
- [x] `grep -n '/usr/local\|/opt/homebrew\|/opt/local' scripts/install-vscodium.sh` vide (INS-5).
- [x] Le gestionnaire de paquets utilisé est celui d'`install-macos.sh` sur le même hôte.
- [x] Aucune commande d'installation de la chaîne dans le script (INS-3).
- [x] `shellcheck` sans erreur (0.11.0 Mac, 0.10.0 Debian).

## Reprise
```
cd /Users/cle_d_anton/lepton-tools-dev/lepton-tools && claude
# « Démarre la session sur l'étape indiquée dans DEVENV-STATUS » (ENV-11 : fusions locales de devenv/env-10 d'abord)
```
