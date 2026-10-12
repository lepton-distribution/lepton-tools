# État du chantier « environnement de développement Lepton »

Source unique de l'état. Mis à jour en fin de chaque session (ORCHESTRATION §3).
Dernière mise à jour : 2026-10-12 — ENV-0 session 1 interrompue (hook inactif).

## Prochaine action

Relancer Claude Code depuis `/Users/cle_d_anton/lepton-tools-dev/lepton-tools`, puis reprendre ENV-0 à la tâche 5 (test du hook) d'après `handoff/env-0.md`.

## Étapes

| Étape | Titre | Statut | Branche(s) | Passation |
| --- | --- | --- | --- | --- |
| ENV-0 | Cadrage | bloquée (hook inactif : session lancée hors de `<LEPTON_TOOLS>`) | lepton-tools `devenv/env-0` | `handoff/env-0.md` |
| ENV-1 | Levée des risques éditeur | à faire | — | — |
| ENV-2 | Audit de l'existant | à faire | — | — |
| ENV-3 | Schémas | à faire | — | — |
| ENV-4 | Format XML de mklepton | à faire | — | — |
| ENV-5 | Restructuration CMake | à faire | — | — |
| ENV-6 | Greffons BSP de référence | à faire | — | — |
| ENV-7 | Évolutions de scion | à faire | — | — |
| ENV-8 | Outil `lepton` | à faire | — | — |
| ENV-9 | Fichiers de l'éditeur | à faire | — | — |
| ENV-10 | Script d'installation VSCodium | à faire | — | — |
| ENV-11 | Validation de bout en bout | à faire | — | — |
| ENV-12 | Extension VSCodium | à faire | — | — |

Statuts possibles : à faire, en cours, bloquée (raison), terminée (date), abandonnée (décision).

## Emplacements (résolus en ENV-0)

| Clé | Valeur |
| --- | --- |
| `<LEPTON_TOOLS>` | `/Users/cle_d_anton/lepton-tools-dev/lepton-tools` |
| `<ROOTSTOCK>` | `/Users/cle_d_anton/lepton` (rootstock de la migration) |
| `<SEED_SCIONS>` | `/Users/cle_d_anton/lepton-tools-dev/seed.scions` (clone neuf, `master` e0adb2c, tags jusqu'à 0.5.0.1) |
| Branche de départ du clone noyau | `master` (6b62af5) |
| Échange git Mac / VM | Distant GitHub ; chaque push soumis à accord (PA-P) |

## Versions épinglées

| Outil | Version | Relevé le |
| --- | --- | --- |
| scion | 0.5.0.1 (tag) | acquis migration |
| CMake (minimum requis) | 3.19 | décision 2026-10-12 |
| CMake (hôte Mac) | 3.31.12 — `/opt/local/bin/cmake` (MacPorts) | 2026-10-12 |
| arm-none-eabi-gcc | 14.2.Rel1 (14.2.1 20241119) — Arm GNU Toolchain, `~/opt/arm-gnu-toolchain-14.2.rel1-darwin-x86_64-arm-none-eabi` (hors MacPorts) | 2026-10-12 |
| QEMU | 11.1.2 — `/opt/local/bin` (MacPorts) | 2026-10-12 |
| OpenOCD | 0.12.0 — `/opt/local/bin` (MacPorts) | 2026-10-12 |
| Python | 3.11.5 — python.org, `/Library/Frameworks/Python.framework` (hors MacPorts) | 2026-10-12 |
| ninja | 1.13.2 — `/opt/local/bin` (MacPorts) | 2026-10-12 |
| MacPorts | 2.12.6 | 2026-10-12 |
| VSCodium | <à relever en ENV-10> | |

## Décisions

Décisions de la spécification : voir `SPECIFICATION.md` §Décisions (1 à 11).
Décisions prises pendant le chantier (une ligne chacune, avec date et point d'arrêt) :

| Date | Point d'arrêt | Décision |
| --- | --- | --- |
| 2026-10-12 | — | Outil `lepton` en Python, dans un nouveau dépôt `lepton-tools` ; orchestration dans `doc/devenv/` de ce dépôt. |
| 2026-10-12 | — | Développement sur l'hôte macOS Intel ; VM Debian réservée à la validation. |
| 2026-10-12 | — | NUCLEO-WL55JC1 : Lepton sur le cœur M4, M0+ non utilisé. Carte supportée et testée pendant le portage. |
| 2026-10-12 | — | Carte STM32F4 de validation : NUCLEO-F429ZI (et non F439ZI). |
| 2026-10-12 | PA-0 | `<LEPTON_TOOLS>` = `~/lepton-tools-dev/lepton-tools` ; `<ROOTSTOCK>` = `~/lepton` (réutilisé) ; `<SEED_SCIONS>` = clone neuf `~/lepton-tools-dev/seed.scions` ; branche noyau `master` ; échange Mac/VM par distant GitHub, push soumis à accord. |

## Journal

| Date | Étape | Résumé (une ligne) |
| --- | --- | --- |
| 2026-10-12 | — | Plan créé : 13 étapes ENV-0 à ENV-12. |
| 2026-10-12 | — | Ajout des skills devenv-session, lepton-rootstock, lepton-oracle, lepton-cibles, du hook proteger-trunk.py et des scripts d'oracle ; MacPorts sur Mac Intel. |
| 2026-10-12 | ENV-0 | Session 1 : PA-0 tranché, dépôt git initialisé, seed.scions cloné, rootstock et versions vérifiés ; arrêt en tâche 5 (hook non chargé, session lancée depuis le dossier parent). |
