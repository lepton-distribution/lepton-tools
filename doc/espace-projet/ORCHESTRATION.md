# Orchestration du chantier « espace-projet »

Fichier de référence de toute session Claude Code de ce chantier. À lire en entier au début de
chaque session, avec `STATUS.md`, le fichier de l'étape courante et la dernière passation.
Chantier distinct du chantier « environnement de développement Lepton » (`doc/devenv/`, étapes
ENV-N, fin du plan le 2026-11-24, en pause).

## 1. Objet et principes

- Objet : `CADRAGE.md` §1 (portabilité entre postes, plusieurs rootstocks, choix de l'outil de
  débogage, plusieurs sondes), porté par l'architecture de projet de `CADRAGE.md` §4.
- Décisions de départ : `CADRAGE.md` §5 (C1 à C10) et `STATUS.md` §Décisions (P1 à P6). Elles ne
  se rediscutent pas dans une étape ; une étape qui les contredit s'arrête et le signale.
- `CADRAGE.md` §6 est une liste de propositions non validées : une étape les présente à son point
  d'arrêt de conception, elle ne les applique pas d'office.
- Une session = une étape (ou un lot borné d'une étape). Jamais deux étapes dans une session.
- `STATUS.md` est la source unique de l'état du chantier. Ce qui n'y est pas consigné n'existe pas
  pour la session suivante.
- Toute décision non actée dans `CADRAGE.md` §5, dans `STATUS.md` §Décisions ou au §4 ci-dessous
  est une question pour l'utilisateur, jamais une hypothèse.
- Numérotation `EP-N` ; points d'arrêt `PA-En`. Les identifiants `ENV-N`, `PA-n`, `Dn`, `An` cités
  renvoient au chantier ENV (`doc/devenv/`).

## 2. Dépôts, emplacements, hôtes

| Élément | Emplacement | Rôle dans ce chantier |
| --- | --- | --- |
| `<LEPTON_TOOLS>` | `STATUS.md` §Emplacements | Outil `lepton`, schémas, extension, scripts, ce dossier |
| `<ROOTSTOCK>` | `STATUS.md` §Emplacements | Rootstock de référence (graine `original-tree`) ; clone noyau `depots/lepton/original/master` |
| `<SEED_SCIONS>` | `STATUS.md` §Emplacements | Évolution générique de scion (EP-2) |
| Graine de référence | clone `<ROOTSTOCK>/depots/lepton-seed.scions/original-tree` | Ajout du greffon projet (EP-3) |
| `lepton-distribution/lepton-original-tree-project` | à créer (EP-3, PA-E7) | Greffon de type `projet`, `scion/sys/user/lepton-basic/` |
| Essais | `~/lepton-tools-dev/essais/ep-<N>…` | Copies et rootstocks d'essai ; suppression par `scripts/supprimer-essai.sh` |
| VM Debian | `doc/devenv/ORCHESTRATION.md` §2 | Validation groupée (EP-8), session Claude Code distincte |

Emplacements et versions du chantier ENV : `doc/devenv/DEVENV-STATUS.md` §Emplacements et
§Versions épinglées, lus **par section** (`grep -n '^## '` puis `sed -n`), jamais en entier
(447 Ko). `STATUS.md` ne recopie que ce que ce chantier ajoute ou change.

Règles reprises par référence, sans recopie (`CADRAGE.md` §8) :

| Règle | Source |
| --- | --- |
| Parallélisme Mac / VM | `doc/devenv/ORCHESTRATION.md` §2 ; branche VM `espace-projet/ep-<N>-debian`, rapport `doc/espace-projet/rapports/ep-<N>-debian.md` |
| Protocole entre sessions, formes des commandes, variables d'environnement, contrôle Mac d'une consigne, invites simultanées (D39) | `doc/devenv/ORCHESTRATION.md` §2bis ; ID d'ordre `REP<N>-<n>` |
| PA-P : tout `git push`, toute action `scion seed-update` / `graft-update`, tout `scion mirror-sync` sans `--dry-run` | `doc/devenv/ORCHESTRATION.md` §4 |
| Règles de travail (où éditer, git, build, scion générique, push) | `doc/devenv/ORCHESTRATION.md` §5 |
| Skills du dépôt, hook `proteger-trunk.py`, skills édités sur le compte, relecture d'une révision du plan | `doc/devenv/ORCHESTRATION.md` §5bis ; `CLAUDE.md` |
| Règles de permission | `.claude/settings.json` |
| Ticket ou hors plan pour un point écarté | en-tête de `doc/devenv/HORS-PLAN.md` ; la ligne s'ajoute à `doc/espace-projet/HORS-PLAN.md` |

## 3. Cycle d'une session

Skill `espace-projet-session` (dérivée de `devenv-session`). Tant qu'elle n'est pas importée dans
`.claude/skills/` (PA-E0), suivre cette section à la lettre.

### Début de session (obligatoire, dans cet ordre)

1. Lire `CLAUDE.md`, ce fichier, `STATUS.md`.
2. Identifier l'étape : la « Prochaine action » de `STATUS.md`. Si l'utilisateur en désigne une
   autre, vérifier au §6 que ses prérequis sont terminés ; sinon le signaler et s'arrêter.
3. Lire la dernière passation : `handoff/ep-<N>.md` si l'étape est en cours, sinon celle de la
   dernière étape terminée.
4. Lire `etapes/EP-<N>-*.md`, les décisions de `CADRAGE.md` qu'il cite, et les sections des
   documents du chantier ENV qu'il cite (par section).
5. Vérifier l'état réel de chaque dépôt touché par l'étape : `git -C <dépôt> status --short`,
   `git -C <dépôt> branch --show-current`, `git -C <dépôt> log --oneline -3`. Tout écart avec la
   passation : le signaler et attendre.
6. Vérifier les versions utiles à l'étape (`STATUS.md` §Versions, sinon
   `doc/devenv/DEVENV-STATUS.md` §Versions épinglées).
7. Passer en mode plan ; présenter étape, état constaté, tâches de la session, points d'arrêt du
   §4 qui seront rencontrés ; attendre l'accord.
8. Après accord : créer ou extraire la branche `espace-projet/ep-<N>` dans chaque dépôt touché
   (depuis la branche indiquée dans `STATUS.md`) ; passer l'étape à « en cours ».

### Pendant la session

- Commits mécaniques (renommages, déplacements, génération) séparés des commits de fond.
- Point d'arrêt atteint : s'arrêter, exposer la question, attendre ; consigner la réponse dans
  `STATUS.md` §Décisions avec la date et l'identifiant `PA-En`.
- Point écarté : proposer hors plan ou ticket (règle citée au §2) ; ligne dans `HORS-PLAN.md`.
- Résultats volumineux dans `rapports/`, référencés, jamais recopiés dans `STATUS.md`.
- Écriture dans l'arbre Lepton : skill `lepton-rootstock`. État de référence et comparaison :
  skill `lepton-oracle`. Construction, QEMU, flash, débogage : skill `lepton-cibles`.
- Ces skills sont écrites pour le chantier ENV : y lire `espace-projet/ep-<N>` pour
  `devenv/env-N`, `doc/espace-projet/rapports/` pour `doc/devenv/rapports/`, `STATUS.md` pour
  `DEVENV-STATUS.md`. Oracles : `doc/espace-projet/rapports/oracles/ep-<N>-<avant|apres>/`.
- `doc/devenv/` n'est modifié que sur décision consignée (D41 et D42 en EP-7, D45, issue de T9) ;
  le commit de fin de session ajoute alors le fichier explicitement.
- Sous-agents : uniquement sur des ensembles de fichiers disjoints ; `STATUS.md`,
  `ORCHESTRATION.md`, `CADRAGE.md` et les schémas sont réservés à la session principale.

### Fin de session (obligatoire, même si l'étape n'est pas terminée)

1. Mettre à jour `STATUS.md` : statut de l'étape, branches, passation, ligne de journal,
   « Prochaine action » (une phrase exécutable), versions relevées, décisions.
2. Écrire `handoff/ep-<N>.md` d'après `doc/devenv/handoff/TEMPLATE.md` (lire « EP » pour « ENV »,
   `STATUS.md` pour `DEVENV-STATUS`), en remplaçant le précédent. Distinguer les décisions de
   l'utilisateur des propositions non validées.
3. Commiter dans `<LEPTON_TOOLS>`, sur la branche de l'étape :
   `git add doc/espace-projet && git commit -m "espace-projet(ep-N): état et passation"`.
4. Ne rien pousser. Annoncer à l'utilisateur ce qui est fait, ce qui reste, la prochaine action.

## 4. Points d'arrêt humains

La session s'arrête, expose la question et attend la réponse. La réponse est consignée dans
`STATUS.md` §Décisions avant de continuer. PA-P (§2) s'applique à toutes les étapes.

| ID | Étape | Question ou validation | État |
| --- | --- | --- | --- |
| PA-E0 | plan | Plan relu par un agent indépendant ; constats retenus ; commit ; `CLAUDE.md` ; fusion d'`espace-projet/plan` dans `main` et push (PA-P) ; import de la skill `espace-projet-session` sur le compte, synchronisation (`claude -p` hors du dépôt), puis `scripts/importer-skills.sh espace-projet-session` et commit dédié | clos (2026-11-25) |
| PA-E1 | EP-0 | Résultats de l'essai VSCodium : C2 et C3 maintenues ou révisées ; effets sur EP-1, EP-2, EP-4 ; essais (a) et (b) sur la VM Debian avant EP-4, ou non ; constat du besoin 2 ; sort des essais | ouvert |
| PA-E2 | EP-1 | Conception du type `projet` avant toute modification : schémas, noms, emplacement du manifeste et modification ou non du lecteur CMake du noyau, interface de `seed new`, régime de référence avec greffon projet (T8), sort des graines existantes à `project/`, versions, où consigner les exigences modifiées (T9) | ouvert |
| PA-E3 | EP-1 | Rapport, essai VSCodium par l'utilisateur, sort des essais, publication | ouvert |
| PA-E4 | EP-2 | Évolution de scion avant implémentation : nom et emplacement de la déclaration, syntaxe, cas limites, numéro de version, `SCION_MIN_VERSION`, `SCION_REF` | ouvert |
| PA-E5 | EP-2 | Rapport, sort des essais, publication (tag et `master` de `<SEED_SCIONS>`) | ouvert |
| PA-E6 | EP-3 | Audit et oracle avant : nom de clé et clone du greffon, arborescence, historique, visibilité et licence du dépôt, presets du noyau et source de `seed new --mkconf` (T4), tests hôte, empreintes et BSP qui citent les fichiers repris (T10), ordre de publication, version du noyau | ouvert |
| PA-E7 | EP-3 | Rapport et oracle après ; création du dépôt GitHub par `gh` ; publication ; application à `<ROOTSTOCK>` | ouvert |
| PA-E8 | EP-4 | Conception de la génération portable : classement projet / poste, mécanisme par valeur, fichier de poste (nom, format, schéma, portée : T1), espace versionné ou non (T2), nom et repli en régime de référence, valeurs de poste quand l'espace est replié (T11), sort de l'ancien espace | ouvert |
| PA-E9 | EP-4 | Rapport, essais de portabilité, essai VSCodium par l'utilisateur, publication | ouvert |
| PA-E10 | EP-5 | Conception du débogage : où se règlent le serveur et l'interface, ce que `generate` émet, modification ou non des BSP (T3), serveurs hors OpenOCD, `jlink` (T6) | ouvert |
| PA-E11 | EP-5 | Autorisation d'écriture flash ; rapport de validation sur cartes ; publication | ouvert |
| PA-E12 | EP-6 | Conception des sondes par carte : clé du réglage (T7), source unique pour CMake, sort de `LEPTON_BOARD_PROBE_SERIAL` et de `--probe-serial`, `lepton probe`, choix au lancement | ouvert |
| PA-E13 | EP-6 | Autorisation d'écriture flash ; rapport de validation à plusieurs sondes ; publication | ouvert |
| PA-E14 | EP-7 | Correction retenue pour D41 et pour D42, avant toute modification | ouvert |
| PA-E15 | EP-7 | Rapport, publication | ouvert |
| PA-E16 | EP-8 | Consigne Debian et critères ; préalable de l'utilisateur ; push ; envoi de l'ordre | ouvert |
| PA-E17 | EP-8 | Clôture : fusion du rapport VM, push ; fin du plan, présentation de `HORS-PLAN.md` | ouvert |

## 5. Tensions relevées au plan, à arbitrer

Relevées à l'analyse du 2026-11-25, non tranchées. Chacune est présentée au point d'arrêt
indiqué, avec les faits de l'audit de l'étape.

| ID | Tension | Arbitrage |
| --- | --- | --- |
| T1 | C5 (a) place le fichier de poste dans le clone du greffon projet : il est propre au rootstock et au projet, alors que `CADRAGE.md` §4 le dit propre à la machine (chaîne, sondes). Plusieurs rootstocks = plusieurs saisies ; une copie de rootstock l'emporte. | PA-E8 |
| T2 | C2 : espace « fourni par le greffon projet » ; §4 : espace = projection régénérée. Versionné ou ignoré par git (donc dépendant d'EP-2) : non dit. | PA-E8 |
| T3 | `CADRAGE.md` §7 donne à E-D les dépôts lepton-tools et noyau ; scinder la cfg OpenOCD et faire de `sonde` une liste touche le schéma et les manifestes des BSP (7 dépôts publiés, dont 5 portent `openocd` et `sonde`). | PA-E10 |
| T4 | Après EP-3, les presets du noyau citeraient `sys/user/lepton-basic/…`, fourni par un autre dépôt ; source de `seed new --mkconf` pour une graine sans ce greffon ; publication sur plusieurs dépôts avec état intermédiaire cassé. | PA-E6 |
| T5 | `CADRAGE.md` §6 : propositions « non validées une à une ». | règle du §1 |
| T6 | C9 : `jlink` émis par `generate` sans validation. | PA-E10 |
| T7 | `CADRAGE.md` §6 propose `sondes: {<bsp>: <série>}` ; deux cartes NUCLEO-WL55JC1 (A et B) ont le même BSP. | PA-E12 |
| T8 | C8 ne dit que le sort de l'espace quand un greffon `projet` est greffé sans `lepton-graine.json` ; celui de `CMakeUserPresets.json` et des commandes de PA-23 n'est pas dit. | PA-E2 |
| T9 | Le chantier revient sur D2 d'ENV-9 et sur le critère PA-19 C, et lit le champ `sonde` de GRF-3 : `doc/devenv/SPECIFICATION.md` amendée, ou exigences consignées dans ce dossier. | PA-E2 |
| T10 | C7 dit les empreintes du test hôte inchangées et `CADRAGE.md` §2.5 qu'aucun CMake ne cite les fichiers repris. Or, dans le clone noyau, `scion/tests/host/CMakeLists.txt` (`host.mklepton_format`) lit `mkconf_tauon_basic_qemu_mps2.xml` ; mklepton écrit le chemin du XML en tête de `kernel_mkconf.h`, donc les empreintes des cartes portées de `mklepton_empreintes.sha256` changent ; 5 BSP publiés posent `LEPTON_NET_TEST_FTP_REFERENCE` sur un `.boot` repris. Relevé à la relecture du plan (2026-11-25). | PA-E6 |
| T11 | C8 replie l'espace à la racine du rootstock quand aucun greffon projet n'est greffé ; C5 écarte le fichier de poste à la racine : la source des valeurs de poste dans ce cas n'est pas dite. | PA-E8 |

## 6. Graphe des étapes

| Étape | Titre | Dépôts | Dépend de |
| --- | --- | --- | --- |
| EP-0 | Essai VSCodium : espace ouvert par un lien du trunk ; plusieurs rootstocks | essais | — |
| EP-1 | Greffon de type `projet` dans lepton | lepton-tools | EP-0 |
| EP-2 | scion : fichiers ignorés greffables déclarés par le greffon | seed.scions, lepton-tools, noyau (`SCION_REF`) | — (conseillée après le PA-E1) |
| EP-3 | Greffon `lepton-original-tree-project` (extraction de `lepton-basic`) | nouveau dépôt, noyau, graine de référence, lepton-tools ; BSP selon PA-E6 | EP-1 |
| EP-4 | `lepton generate` portable et fichier de poste | lepton-tools ; greffon projet selon PA-E8 | EP-0, EP-1, EP-2, EP-3 |
| EP-5 | Débogage : serveur et interface par configuration | lepton-tools ; BSP et noyau selon PA-E10 | EP-4 |
| EP-6 | Sondes par carte | lepton-tools, noyau | EP-5 |
| EP-7 | lepton : trunk déjà incohérent, répertoire vide (D41, D42) | lepton-tools | — (conseillée après EP-1) |
| EP-8 | Validation Debian groupée | VM, lepton-tools | EP-1 à EP-7 |

```
EP-0 ──► EP-1 ──► EP-3 ──┐
                         ├──► EP-4 ──► EP-5 ──► EP-6 ──┐
EP-2 ────────────────────┘                             ├──► EP-8
EP-7 ──────────────────────────────────────────────────┘
```

EP-1 et EP-2 sont d'ordre interchangeable ; EP-7 se place à tout moment avant EP-8.
