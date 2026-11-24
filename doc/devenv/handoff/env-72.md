# Passation ENV-72 — Validation Debian groupée (ENV-67 à ENV-71) — session du 2026-11-24

## Statut
terminée : l'ordre R72-1 a été validé sur la VM Debian. C1 à C7 sont atteints, C8 écarté et C9
fait. D35 est prouvé avec git 2.47.3, en anglais et en français ; D33, D29, D30, D32, D37, D36,
D38 (1) à (3) et D40 sont prouvés sur la VM. Les binaires des 16 presets sont identiques à ceux de
R66-1. C'est la **fin du plan**. `HORS-PLAN.md` a été présenté le 2026-11-24, hors étape, et les
décisions sont consignées. La révision du plan est reportée par l'utilisateur : le chantier est en
pause (voir Reprise).

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `devenv/env-72` (depuis `main` 8cbbf25), fusionnée `--no-ff` dans `main` ; `main`, `devenv/env-72` et `devenv/env-72-debian` poussées (PA-132) | branche : « devenv(env-72): état et passation » ; `main` : fusion de `devenv/env-72` (c060d58, poussée), puis un commit local **non poussé** « devenv(hors-etape): fin du plan après ENV-72, décisions sur HORS-PLAN ; passation » (push sur accord, PA-P) | oui |
| lepton-tools (VM) | `devenv/env-72-debian` (depuis 5411f78) | 9869e39 « devenv(env-72): rapport de validation Debian R72-1 … », fusionnée dans `devenv/env-72` (593769f) | — |
| clone noyau `depots/lepton/original/master` | `master` | 0c2e43e (non touché) | oui |
| seed.scions | `master` | 929c01a, tag 0.6.3.4 (non touché) | oui |
| rootstocks d'essai du Mac | — | `env-13-vierge`, `env-9`, `env-11/{qemu,qemu-gra2,bout-en-bout/rootstock,f429zi,wl55jc1}` regreffés : noyau 0c2e43e | — |
| VM | `~/lepton-tools-dev/lepton-tools` sur `devenv/env-72-debian` | scion 0.6.3.4, lepton 0.1.0 (ENV-68), extension 0.5.4 ; `$U`, `$E13`, `$C5`, `$R53` regreffés (noyau 0c2e43e) ; `~/env-72-journaux`, `~/tmp-pytest/env-72` gardés ; `LEPTON_EMBOS_ROOT` dans `~/.bashrc` | — |

Relever l'état réel de `main` et d'`origin/main` au début de la session suivante.

Outils (Mac) : Claude Code 2.1.331 ; scion 0.6.3.4 ; lepton 0.1.0 ; extension 0.5.4 ; git 2.50.1.

## Fait pendant la session
Rapports : `rapports/env-72-mac.md` (préparation §1, PA-131 §2, rootstocks du Mac §3, contrôle du
rapport VM §3bis, messages §4) et `rapports/env-72-debian.md`. Consigne :
`consignes/env-72-debian.md`.
- **Préparation** :
  - `env-72-mac/ls-remote.sh` : seuls le noyau (0c2e43e) et les HEAD des miroirs ont changé ;
  - trunk de `<ROOTSTOCK>` `CONFORME` ;
  - scripts d'ENV-68 refaits avec des copies par `tar` (`env-72-mac/chemins.sh`, `graine.sh`) ;
  - `env-72-mac/fixture70.py` (git de `--single-branch` passé en argument) ;
  - attendus C3 (regreffe d'`essais/env-13-vierge`), C4, C5 ;
  - contrôle de la consigne sur la copie distincte `essais/env-72-essai/c4d` (D38 (3)) : 4 classes
    d'écart ; erreur de colonne de `resume.tsv` corrigée ;
  - pytest au Mac : 616.
- **PA-131** tranché ; push de `devenv/env-72` (5411f78).
- **R72-1** : messages consignés au §4 du rapport Mac.
  - §0 : `LEPTON_EMBOS_ROOT` a été ajoutée à `~/.bashrc` (l'export n'avait d'abord été tapé que
    dans un terminal).
  - Trois défauts de la consigne :
    - cibles d'ENV-66 absentes : §14 corrigé par décision de l'utilisateur ;
    - D34 non listé au §9 ;
    - classe « graine `env11` » trop étroite.
  - Incident A1 : invite confirmée par erreur, sans effet, puis refusée (décision (a) de
    l'utilisateur).
- **Tâche 3** : 7 rootstocks d'essai du Mac regreffés (`rapports/env-72-mac.md` §3) ;
  `qemu-gra2` : BSP an386 retiré par `graft-remove`.
- **Tâche 4** : comparaisons refaites sur les relevés poussés ; bilans identiques à ceux de la VM.
- **PA-132** tranché : fusions et push. `HORS-PLAN.md` : 9 points marqués prouvés sur la VM.

## Reste à faire dans l'étape
- Rien dans l'étape. La présentation de fin du plan de `HORS-PLAN.md` est faite (2026-11-24) :
  - tickets relevés : lepton-famille-stm32f7xx#1, lepton-famille-stm32f4xx#1 et
    lepton-famille-stm32wlxx#1 sont ouverts ;
  - A1 à A4, D4, D12, D34 et D38 (4) restent hors plan ;
  - D41 et D42 sont **à traiter** ;
  - les constats de R72-1 sont inscrits en D44 à D47, suite non décidée.
- Reste, à la reprise : la révision du plan (voir Reprise).

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| PA-P : regreffe d'`essais/env-13-vierge` pendant la préparation (attendu de C3) | utilisateur | oui (PA-131) |
| PA-131 : consigne et §0 validés ; C3 4 regreffes ; C6 T3 dans VSCodium sur la VM ; C7 maintenu ; C8 écarté ; C9 tel qu'écrit ; push et ordre | utilisateur | oui |
| §14 réduit à `env-72-essai`, `env-72-fixture`, `~/tmp-pytest/env-72-enveloppe` | utilisateur | oui |
| A1 confirmée par erreur : option (a), relancer et refuser (prise dans la session VM) | utilisateur | oui |
| D34 admis au résumé de C3 (application du fichier d'étape, PA-120) | session Mac, sur décision existante ; utilisateur informé | oui |
| Classe « graine `env11` » étendue (branche, URL `ssh://` déclarées) | session Mac (défaut de la consigne) | oui |
| Tâche 3 : 6 regreffes après la fin des invites de la VM | utilisateur | oui (journal) |
| PA-132 : fusions `--no-ff` et push des trois branches | utilisateur | oui |
| Fin du plan : A1 à A4, D4, D12, D34, D38 (4) hors plan ; D41, D42 à traiter ; D44 à D47 inscrits ; révision du plan reportée, chantier en pause | utilisateur | oui |
| D44 à D47 : « suite non décidée, à présenter à la prochaine révision du plan » ; rubriques « non éligible au ticket » | proposition non validée (session) | oui (`HORS-PLAN.md`) |

## Pièges rencontrés
- Variable « posée » par un `export` tapé dans un terminal → absente des nouveaux terminaux. Parade : l'écrire dans `~/.bashrc` (shell `/bin/bash`, pas de `~/.bash_profile` sur la VM), vérifier dans un nouveau terminal.
- Attendus de présence repris d'une consigne précédente (ENV-66) → la VM avait été nettoyée par R66-2. Parade : relire la passation de la validation précédente (état laissé) avant d'écrire le §5.
- Copie distincte du Mac encore trop proche de l'origine (mêmes URL et branche de graine) → une classe d'écart non simulée. Parade : changer aussi les URL déclarées et la branche de la graine dans la copie distincte.
- Le hook du plugin `lepton-tickets` refuse une commande qui contient `gh` avec des apostrophes non appariées (texte français dans un heredoc) → écrire le script dans le répertoire temporaire, puis le lancer.
- `ECONNRESET` ×2 sur un `AVANCEMENT` de la VM → la remise en échec du §2bis a suffi (message consigné, contenu repris dans le suivant).
- Notification de VSCodium non affichée en surimpression sur la VM → la chercher dans le centre de notifications (cloche) avant de conclure à son absence.

## Critères de validation
- [x] PA-131 et PA-132 tranchés et consignés.
- [x] `FIN-SUCCÈS R72-1` vérifié par la session Mac ; C1 à C9 conformes, C8 écarté au PA-131.
- [x] D35 : cause de git montrée avec git 2.47.3 ; D33, D29, D30, D32, D37 conformes à l'attendu.
- [x] D38 : variables traitées selon le PA-121 ; nettoyage de sous-répertoires par l'enveloppe.
- [x] D39 : aucune invite simultanée Mac et VM ; toute confirmation par erreur consignée (A1).
- [x] Rootstocks d'essai regreffés : 0 lien cassé, 0 fichier régulier ; `check` code 0 (`qemu-gra2` : 1).
- [x] Fin du plan : `HORS-PLAN.md` présenté à l'utilisateur et décisions consignées (2026-11-24).

Tickets créés pendant la session : aucun.
Lignes restées « ticket à créer après publication d'ENV-72 » : aucune.

## Reprise
Le chantier est en pause par décision de l'utilisateur. Rien n'est à lancer sans sa demande.

À faire à la reprise : réviser le plan pour planifier D41 et D42, et présenter D44 à D47 pour
décision (traiter, hors plan, abandonner).

Procédure de relance :
1. Avant la révision, relever l'état :
   - lepton-tools : `main` = `origin/main`, et l'éventuel commit hors étape non poussé ;
   - seed.scions : `master` 929c01a, tag 0.6.3.4 ;
   - noyau : `master` 0c2e43e ;
   - Mac et VM : scion 0.6.3.4, lepton 0.1.0, extension 0.5.4, Claude Code, git ;
   - les tickets lepton-famille-stm32f4xx#1, lepton-famille-stm32f7xx#1 et
     lepton-famille-stm32wlxx#1 : un ticket fermé sans correction revient en décision ;
   - l'amont ST, pour savoir si un STM32CubeWL `v1.7.0` est publié (D43).
2. Réviser le plan avec la skill `lepton-portage-instructions` (hors de ce dépôt). Les fichiers
   d'étape sont numérotés à partir d'ENV-73. Avant le commit, la révision est relue par un agent
   indépendant (ORCHESTRATION §5bis), et les constats retenus sont consignés au journal.
3. Ensuite, sessions d'étape ordinaires : skill `devenv-session`, une branche `devenv/env-<N>`.

Commande de la session suivante :
```
révise le plan (fin du plan après ENV-72, lire handoff/env-72.md) : planifier D41 et D42, présenter D44 à D47
```
