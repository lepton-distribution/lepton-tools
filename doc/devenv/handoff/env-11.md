# Passation ENV-11 — Validation de bout en bout — session du 2026-10-15 (S3)

## Statut
terminée — scénarios Mac (S1, S2) et Debian (S3) conformes, écarts P1 acceptés et renvoyés
(`rapports/env-11-bilan.md`).

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `devenv/env-11` | `devenv(env-11): état et passation (S3)` ; avant : 49ff3bd fusion de `devenv/env-11-debian` (55a55bc D1, 4725f32 rapport), 53ca625 projet de bilan, 8cca1c0 consigne VM. Distant : `devenv/env-11` = 8cca1c0, `devenv/env-11-debian` = 4725f32, `main` = 657c395 | oui |
| clone noyau `~/lepton/depots/lepton/original/master` | `devenv/env-11` (extraite) | a572f00 `SCION_REF` 0.5.1.0 ; `master` 1dde0af ; tous deux poussés | oui |
| famille `qemu-mps2`, BSP `qemu-mps2-an386` (`~/lepton/depots/`) | `master` | 3954357, 046779e ; poussés par URL SSH vers `lepton-distribution/lepton-famille-qemu-mps2` et `lepton-bsp-qemu-mps2-an386` (aucun distant configuré localement) | oui |
| seed.scions | `master` 79f4f96, tag 0.5.1.0 | inchangé | oui |
| Rootstocks d'essai | Mac `~/lepton-tools-dev/essais/env-11/{qemu,f429zi,wl55jc1}` ; VM `~/lepton-tools-dev/essais/env-11/qemu` | conservés, hors git | — |

## Fait pendant la session
- Décisions de début de S3 (dépôts GitHub des greffons QEMU, réinstallation explicite de lepton sur
  la VM) ; PA-P accordé et push fait (six références, contrôlées par `git ls-remote`).
- Consigne VM `consignes/env-11-debian.md`, transmise par SendMessage à la session VM (Remote
  Control) à la demande de l'utilisateur.
- Rapport Debian `rapports/env-11-debian.md` intégré : scénario CLI conforme après D1 (correction
  lepton faite par la VM avec accord de l'utilisateur) ; fusion `--no-ff`, `pytest` 118 verts au Mac.
- D2 (erreur de la consigne : `<bin name="salut">` dans le bloc `sbin`) corrigé dans la consigne.
- Bilan `rapports/env-11-bilan.md` : exigences P1 × Mac / Debian, nouveau défaut N5 (CFG-4 : valeurs
  d'options non fixables dans la graine), classement N1, N4, N5, O1-O13, D1-D4.

## Reste à faire dans l'étape
- Rien. Fusions locales de `devenv/env-11` (lepton-tools → `main`, clone noyau → `master`) au début
  de la session suivante.
- Reprises acceptées (bilan §3), hors étape : ENV-7 N1 ; ENV-9 N4, O8, O10, O11 ; ENV-3/5/8 N5 ;
  ENV-8 O3, O4 ; ENV-6 O1 ; ENV-10 D3, D4, O6, O12 ; noyau O9 ; ENV-12 O2, O5. Elles ne figurent
  pas au graphe d'ORCHESTRATION §6 : à planifier (skill `lepton-portage-instructions`) ou à ouvrir
  comme lots bornés des étapes citées.
- Reliquats antérieurs : Apple Silicon (revue seule) ; ligne « openocd » vide du récapitulatif
  d'`install-debian.sh` ; BSP `nucleo-f439zi` reporté.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Greffons QEMU publiés sur deux dépôts GitHub, poussés par URL SSH | utilisateur | oui |
| lepton réinstallé explicitement sur la VM ; O12 | utilisateur | oui |
| Push PA-P de S3 (six références) | utilisateur | oui |
| D1 corrigé dans lepton (`gdb-multiarch` en repli) | utilisateur (session VM) | oui |
| Renvois du bilan §3 tels que proposés | utilisateur | oui |
| Écarts CFG-1, CFG-4, réserves IDE-3, IDE-5 acceptés ; ENV-11 terminée | utilisateur | oui |
| Reprises avant PA-12 | utilisateur | oui |
| lepton du Mac (pipx) non réinstallé après D1 (sans effet sur macOS) | proposition non validée | oui (§Versions) |

## Pièges rencontrés
- `lepton` ne reconnaît une origine distante que si l'URL a un hôte : `ssh://git@github.com/…`,
  jamais `git@github.com:…` (pris pour un chemin local).
- Debian : pas d'`arm-none-eabi-gdb` (D1, corrigé), ni clangd LLVM (D4), ni xmllint (D3) par défaut.
- `/tmp` de la VM (747 Mo) saturé par les venv de test : `TMPDIR` dans `/home` (O13).
- Le commit local 53ca625 n'était pas poussé : la VM a travaillé depuis 8cca1c0 (sans effet).

## Critères de validation
- [x] PA-11 tranché.
- [x] Toutes les exigences P1 conformes sur Mac, ou écart accepté par l'utilisateur.
- [x] Scénario Debian conforme (après D1).
- [x] Aucun fichier régulier dans le trunk à la fin du scénario.

## Reprise
```
cd /Users/cle_d_anton/lepton-tools-dev/lepton-tools && claude
# « Démarre la session sur l'étape indiquée dans DEVENV-STATUS » (fusions d'ENV-11, choix de la première reprise)
```
