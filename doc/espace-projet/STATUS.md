# État du chantier « espace-projet »

Source unique de l'état. Mis à jour en fin de chaque session (ORCHESTRATION §3).
Dernière mise à jour : 2026-11-26 — EP-0 terminée : essai VSCodium du lien, PA-E1 clos (C2
révisée, piste P-a), plan révisé et relu ; branche `espace-projet/ep-0` non fusionnée.

## Prochaine action

EP-1 (`etapes/EP-1-greffon-type-projet.md`), dans une nouvelle session, par la skill
`espace-projet-session` (EP-2 possible à la place : ordre interchangeable, ORCHESTRATION §6).
Avant de créer `espace-projet/ep-1` : demander à l'utilisateur la fusion d'`espace-projet/ep-0`
dans `main` et son push (PA-P), non faits en EP-0 ; la branche de l'étape part de `main`
après cette fusion.

## Étapes

| Étape | Titre | Statut | Branche(s) | Passation |
| --- | --- | --- | --- | --- |
| plan | Plan du chantier (skill `lepton-portage-instructions`) | terminée (2026-11-25) | lepton-tools `espace-projet/plan` (depuis `main` e25a414 ; fusionnée `--no-ff` dans `main`) | — |
| EP-0 | Essai VSCodium : espace ouvert par un lien du trunk ; plusieurs rootstocks | terminée (2026-11-26) | lepton-tools `espace-projet/ep-0` (depuis `main` cf34908 ; non fusionnée, non poussée) | `handoff/ep-0.md` |
| EP-1 | Greffon de type `projet` dans lepton | à faire | | |
| EP-2 | scion : fichiers ignorés greffables déclarés par le greffon | à faire | | |
| EP-3 | Greffon `lepton-original-tree-project` (extraction de `lepton-basic`) | à faire | | |
| EP-4 | `lepton generate` portable et fichier de poste | à faire | | |
| EP-5 | Débogage : serveur et interface par configuration | à faire | | |
| EP-6 | Sondes par carte | à faire | | |
| EP-7 | lepton : trunk déjà incohérent, répertoire vide (D41, D42) | à faire | | |
| EP-8 | Validation Debian groupée | à faire | | |

Statuts possibles : à faire, en cours, bloquée (raison), terminée (date), abandonnée (décision).

## Emplacements

Valeurs recopiées de `doc/devenv/DEVENV-STATUS.md` §Emplacements le 2026-11-25. Le reste (greffons
famille et BSP, graine de référence, sondes des cartes, SVD, clones de code tiers) s'y lit par
section.

| Clé | Valeur |
| --- | --- |
| `<LEPTON_TOOLS>` | `/Users/cle_d_anton/lepton-tools-dev/lepton-tools` |
| `<ROOTSTOCK>` | `/Users/cle_d_anton/lepton` |
| `<SEED_SCIONS>` | `/Users/cle_d_anton/lepton-tools-dev/seed.scions` |
| Clone noyau | `<ROOTSTOCK>/depots/lepton/original/master`, branche `master` |
| Graine de référence | `<ROOTSTOCK>/depots/lepton-seed.scions/original-tree`, branche `original-tree` |
| Essais du chantier | `~/lepton-tools-dev/essais/ep-<N>…` |

## Versions

État de départ (`CADRAGE.md` §2, relevé le 2026-11-25). Les autres versions épinglées :
`doc/devenv/DEVENV-STATUS.md` §Versions épinglées. Une étape qui change une version l'écrit ici.

| Élément | Valeur de départ | Changé par |
| --- | --- | --- |
| lepton-tools | `main` e25a414 = `origin/main` | |
| seed.scions | `master` 929c01a, tag 0.6.3.4 | |
| Clone noyau | `master` 0c2e43e | |
| scion | 0.6.3.4 (Mac) | |
| lepton | 0.1.0 | |
| Extension Lepton | 0.5.4 | |
| git | Mac 2.50.1 ; VM Debian 2.47.3 | |
| Claude Code | Mac 2.1.331 (`CADRAGE.md`) ; `claude --version` : 2.1.332 le 2026-11-25 | |

## Décisions

C1 à C10 (utilisateur, 2026-11-25) : `CADRAGE.md` §5, non recopiées.

| ID | Date | Décision | Auteur |
| --- | --- | --- | --- |
| P1 | 2026-11-25 | Découpage EP-0 à EP-8. Écarts avec `CADRAGE.md` §7 : essai VSCodium du lien avancé en étape EP-0 (était la tâche 1 d'E-C) ; E-D scindée en EP-5 (serveur et interface) et EP-6 (sondes) ; E-E (EP-3) placée avant E-C (EP-4). | utilisateur, sur proposition de la session |
| P2 | 2026-11-25 | État propre sous `doc/espace-projet/` (ORCHESTRATION, STATUS, HORS-PLAN, `etapes/`, `handoff/`, `rapports/`, `consignes/`) ; skill de session dérivée de `devenv-session`, préparée dans `~/Downloads/` pour import sur le compte (forme d'ENV-67). | utilisateur, sur proposition de la session |
| P3 | 2026-11-25 | Branches `espace-projet/plan` pour le plan, puis `espace-projet/ep-<N>` par dépôt touché. | utilisateur, sur proposition de la session |
| P4 | 2026-11-25 | D41 et D42 du hors-plan d'ENV repris par ce chantier, en EP-7. | utilisateur, sur proposition de la session |
| P5 | 2026-11-25 | Nom et format du fichier de poste, nom de la déclaration de scion, sort des graines d'essai à `project/` : décidés au point d'arrêt de l'étape concernée (PA-E8, PA-E4, PA-E2). | utilisateur, sur proposition de la session |
| P6 | 2026-11-25 | J-Link, option (ii) du résidu `tauon-basic`, graine multi-BSP et publication sur Open VSX : consignés dans `HORS-PLAN.md`. | utilisateur, sur proposition de la session |
| PA-E0 (relecture) | 2026-11-25 | Constats 1 à 11 de la relecture indépendante, constats mineurs et suggestion d'un essai sur la VM avant EP-4 : retenus et appliqués. | utilisateur |
| PA-E0 (clôture) | 2026-11-25 | Fusion d'`espace-projet/plan` dans `main` et push de `main` accordés (PA-P). Skill `espace-projet-session` importée sur le compte par l'utilisateur, puis copiée dans le dépôt. | utilisateur |
| PA-E1 (C2) | 2026-11-26 | **C2 révisée, piste P-a** : l'espace reste un fichier régulier à la racine du rootstock (emplacement actuel, D2 d'ENV-9 ; nom décidé au PA-E8), généré depuis le contenu versionné du greffon projet ; il n'est plus placé derrière un lien du trunk. **C3 maintenue.** **C8** : la branche « espace dans le greffon projet s'il y en a un de greffé » devient sans objet ; l'espace est à la racine dans les deux régimes. Motif (`rapports/ep-0-essai-lien.md` §2) : derrière un lien, les `folders` relatifs ne sont justes que pour un groupe de modes d'ouverture (`codium <lien>` et récents ; ou Finder et menu, qui résolvent le lien — menu essayé sur `V-lien` seulement). | utilisateur, sur recommandation de la session |
| PA-E1 (révision du plan) | 2026-11-26 | Plan révisé dans la session d'EP-0, relu par un agent indépendant avant commit (journal). Fichiers révisés : EP-4 (décisions, faits d'EP-0, §1, essais, critères, pièges), ORCHESTRATION §4 (PA-E1 clos, PA-E8) et §5 (en-tête, T2 sans objet, T9, T11 reformulée), `CADRAGE.md` §5 (C2 et C8 annotées), §4, §6 et §7 (notes de renvoi), EP-1 (contexte, piège), EP-2 (prérequis), EP-3 (piège), EP-5 (contenu d'équipe, `openocdPath`), EP-8 (critère C7). Retouches d'EP-1, d'EP-2 et du §4 du cadrage, hors de la liste approuvée d'abord : gardées. | utilisateur, sur recommandation de la session |
| PA-E1 (Debian) | 2026-11-26 | Essais d'EP-0 non refaits sur la VM Debian avant EP-4 ; preuve Debian laissée à EP-8, critère C7 : espace généré à la racine ouvert par la ligne de commande et par le gestionnaire de fichiers (dossiers résolus), retouche par l'interface puis `generate` selon le PA-E8. | utilisateur, sur recommandation de la session |
| PA-E1 (relevé QEMU) | 2026-11-26 | Relevé incident du constat du besoin 2 (QEMU lancé par Cortex-Debug à l'écoute sur toutes les interfaces) : hors plan, H6. Le besoin 2 est constaté sans défaut (rapport §5). | utilisateur |
| PA-E1 (essais) | 2026-11-26 | `essais/ep-0/` (copies `a` et `b`, relevés `*.out` et journaux de construction) à supprimer en fin de session par `scripts/supprimer-essai.sh`. | utilisateur |
| PA-E1 (openocdPath) | 2026-11-26 | Forme portable de `cortex-debug.openocdPath`, non essayée en EP-0 (BSP QEMU) : vérifiée en EP-5. | utilisateur, sur recommandation de la session |

## Journal

- 2026-11-25 — `CADRAGE.md` écrit (claude.ai, deux sessions de réflexion). Session Claude Code :
  analyse de faisabilité validée par l'utilisateur (P1 à P6) ; plan écrit sur
  `espace-projet/plan` (ORCHESTRATION, STATUS, HORS-PLAN, EP-0 à EP-8) ; skill
  `espace-projet-session` préparée dans `~/Downloads/`. `devenv-session` non appliquée : session de
  plan d'un chantier distinct (`CADRAGE.md` §8).
- 2026-11-25 — Relecture du plan par un agent indépendant (effort `xhigh`, lecture seule), règle
  de `doc/devenv/ORCHESTRATION.md` §5bis. Constats appliqués sur décision de l'utilisateur :
  (1) T10, trois consommateurs des fichiers repris contre C7 et `CADRAGE.md` §2.5 ; (2) préfixe
  `scion/` des chemins du clone noyau ; (3) fusion dans `main` au PA-E0 ; (4) lecteurs de
  manifeste et type inconnu de CMake en EP-1 ; (5) lecture des skills du dépôt, oracles,
  règle sur `doc/devenv/` ; (6) ordre des essais d'EP-0, copies sans `build/`, hook ; (7) T11,
  dépôt du greffon projet en EP-4 ; (8) critère des numéros de série et propositions du §6 en
  EP-6 ; (9) critères d'EP-1 ; (10) tâche 3 d'EP-3 ; (11) `CLAUDE.md` ; mineurs (version de
  Claude Code, 5 BSP sur 7 à `openocd`, D12, état gardé par VSCodium) ; essai Debian proposé au
  PA-E1. Écartés : aucun. Vérifiés par la session dans les dépôts : 1, 2, 4, 5, 6, 8, 9 ; 3 et
  11 lus dans les fichiers ; 7, 10 et le cache CMake d'un `build/` copié non rejoués. Suggestions
  non présentées à l'utilisateur, non appliquées : liste attendue du grep d'EP-3, carte absente
  en EP-5, formulations d'EP-2, forme de `pipx install` en EP-1, description de `devenv-session`.
  Ajouts hors source de la session : essai (c) d'EP-0, critères d'oracle d'EP-1.
- 2026-11-25 — Plan commité sur `espace-projet/plan` (764974f, c09e7d6). Skill
  `espace-projet-session` : copie synchronisée du compte identique à la version préparée
  (SHA-256 0fa50811…), copiée par `scripts/importer-skills.sh espace-projet-session`, commit
  dédié. PA-E0 clos : fusion `--no-ff` dans `main`, push de `main` accordé par l'utilisateur.
- 2026-11-26 — EP-0. Copies sans `build/` de `essais/env-9` (`ep-0/a`) et `essais/env-11/qemu`
  (`ep-0/b`) ; variantes de l'espace déposées dans le clone de la graine, greffées par lien
  (`scion graft`). Essai (a) : `folders` résolus depuis le chemin d'ouverture (lien par `codium`,
  cible par Finder et menu). Essai (c) : variables selon le consommateur (clangd et vscode-xml
  refusent `${workspaceFolder:trunk}`, `json.schemas` absolu seulement). Essai (b) : écriture à
  travers le lien, sur place. Besoin 2 constaté sans défaut. Rapport
  `rapports/ep-0-essai-lien.md`. PA-E1 clos (décisions ci-dessus) ; H6 ajouté au hors-plan.
  Écart à la consigne de l'étape : essai (c) par un remplacement par consommateur, et non un
  chemin à la fois (rapport §3).
- 2026-11-26 — Révision du plan (PA-E1) relue par un agent indépendant (effort `xhigh`, lecture
  seule ; règle de `doc/devenv/ORCHESTRATION.md` §5bis). 23 constats, aucun bloquant ; constats
  1 à 4 et 23 vérifiés par la session dans les fichiers, 9 à 22 contre le rapport. Appliqués sur
  décision de l'utilisateur : tous (faits d'EP-0 ramenés au prouvé dans EP-4, nom de l'espace
  laissé au PA-E8, signalement des retouches non imposé, option « rien de plus » et essai du
  contenu d'équipe, T9, EP-1, EP-3, EP-5, EP-8 C7, notes du cadrage §6 et §7, mentions
  anticipées de STATUS) ; retouches d'EP-1, d'EP-2 et du §4 du cadrage, hors de la liste approuvée
  d'abord : gardées. Écartés : aucun. Non confirmés : aucun.
- 2026-11-26 — `essais/ep-0/` supprimé par `scripts/supprimer-essai.sh` (rc 0). Restent dans
  VSCodium les états `workspaceStorage` des chemins d'essai (sans effet).
