# État du chantier « environnement de développement Lepton »

Source unique de l'état. Mis à jour en fin de chaque session (ORCHESTRATION §3).
Dernière mise à jour : 2026-10-12 — création du plan (aucune étape commencée).

## Prochaine action

Lancer une session sur ENV-0 (`doc/devenv/etapes/ENV-00-cadrage.md`).

## Étapes

| Étape | Titre | Statut | Branche(s) | Passation |
| --- | --- | --- | --- | --- |
| ENV-0 | Cadrage | à faire | — | — |
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
| `<LEPTON_TOOLS>` | <À CONFIRMER> |
| `<ROOTSTOCK>` | <À CONFIRMER> |
| `<SEED_SCIONS>` | <À CONFIRMER> |
| Branche de départ du clone noyau | <À CONFIRMER> |
| Échange git Mac / VM | <À CONFIRMER> |

## Versions épinglées

| Outil | Version | Relevé le |
| --- | --- | --- |
| scion | 0.5.0.1 (tag) | acquis migration |
| CMake (minimum requis) | 3.19 | décision 2026-10-12 |
| CMake (hôte Mac) | <à relever en ENV-0> | |
| arm-none-eabi-gcc | <à relever en ENV-0> | |
| QEMU | <à relever en ENV-0> | |
| OpenOCD | <à relever en ENV-0> | |
| Python | <à relever en ENV-0> | |
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

## Journal

| Date | Étape | Résumé (une ligne) |
| --- | --- | --- |
| 2026-10-12 | — | Plan créé : 13 étapes ENV-0 à ENV-12. |
| 2026-10-12 | — | Ajout des skills devenv-session, lepton-rootstock, lepton-oracle, lepton-cibles, du hook proteger-trunk.py et des scripts d'oracle ; MacPorts sur Mac Intel. |
