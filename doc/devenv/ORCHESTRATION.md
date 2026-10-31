# Orchestration du chantier « environnement de développement Lepton »

Fichier de référence pour toute session Claude Code de ce chantier. À lire en entier au début de
chaque session, avec `DEVENV-STATUS.md`, le fichier de l'étape courante et la dernière passation.

## 1. Objet et principes

- Objet : réaliser l'environnement décrit dans `SPECIFICATION.md` (exigences INS, GRA, GRF, FIC,
  CFG, BLD, IDE, DBG, TST, NF).
- Une session = une étape (ou un lot borné d'une étape). Jamais deux étapes dans une session.
- `DEVENV-STATUS.md` est la source unique de l'état du chantier. Ce qui n'y est pas consigné
  n'existe pas pour la session suivante.
- Toute décision non actée dans `SPECIFICATION.md` ou au §4 ci-dessous est une question pour
  l'utilisateur, jamais une hypothèse.
- Numérotation `ENV-N`, distincte des étapes `ETAPE-N` de la migration IAR → GCC.

## 2. Dépôts, emplacements, hôtes

| Élément | Emplacement | Rôle |
| --- | --- | --- |
| Dépôt `lepton-tools` | `<LEPTON_TOOLS>` — résolu en ENV-0 (PA-0) : `DEVENV-STATUS.md` §Emplacements ; distant `lepton-distribution/lepton-tools` | Outil `lepton`, schémas, modèles, scripts d'installation, ce dossier `doc/devenv/` |
| Rootstock Lepton | `<ROOTSTOCK>` — résolu en ENV-0 (PA-0) : `DEVENV-STATUS.md` §Emplacements | `depots/`, `trunk/` ; clone noyau `depots/lepton/original/master` |
| Dépôt `seed.scions` | clone à part, `<SEED_SCIONS>` — résolu en ENV-0 (PA-0) : `DEVENV-STATUS.md` §Emplacements | Évolutions génériques de scion (ENV-7, ENV-15) |
| Répertoire de construction | `<ROOTSTOCK>/build/<preset>` | Toujours hors du trunk |

Claude Code est lancé à la racine de `<LEPTON_TOOLS>`. Les chemins `<…>` sont résolus une fois en
ENV-0 et recopiés dans `DEVENV-STATUS.md` §Emplacements ; les fichiers d'étape les utilisent tels
quels.

Hôtes :

| Hôte | Rôle | Étapes |
| --- | --- | --- |
| Mac mini Intel, macOS (hôte principal) | Développement, construction native, flash et débogage | Toutes |
| VM Debian x86_64 (si accès donné) | Validation Debian uniquement, dans une session Claude Code distincte | ENV-10 (partie Debian), ENV-11 (partie Debian), ENV-14 (partie Debian), ENV-15 (partie Debian), ENV-21 |

Règles de parallélisme Mac / VM :

- La VM ne développe pas : elle exécute et valide ce que le Mac a produit et commité.
- Les deux sessions ne modifient jamais les mêmes fichiers. La session VM n'écrit que son rapport
  `doc/devenv/rapports/env-N-debian.md` et ses corrections strictement propres à Debian, sur une
  branche `devenv/env-N-debian`.
- Échange par git uniquement : résolu en ENV-0 (PA-0) : `DEVENV-STATUS.md` §Emplacements (distant GitHub, push soumis à accord).
- `DEVENV-STATUS.md` n'est modifié que par la session Mac ; la session VM y reporte via son
  rapport, que la session Mac intègre.

### 2bis. Protocole entre sessions Claude Code (messages)

S'applique à tout message entre deux sessions (Mac ↔ VM par Remote Control, ou autre). Décision de
l'utilisateur du 2026-10-16 : chaque ordre est accusé, chaque fin est annoncée avec ce qu'il faut
pour agir. Un envoi réussi ne prouve pas la lecture : seul l'accusé compte.

Forme de chaque message :
- Première ligne autonome : `[<TYPE> <ID>] <étape> — <objet en une phrase>`. `ID` = `<étape>-<n>`
  (ex. `R5-1`), repris tel quel par toutes les réponses au même ordre.
- Puis : émetteur (nom de session), destinataire, références vérifiables (branche, commit, fichier
  de consigne), et le contenu lui-même (pas de `@chemin` : le texte est envoyé tel quel).

| Type | Émis par | Quand | Contenu obligatoire |
| --- | --- | --- | --- |
| `ORDRE` | session principale | demande d'exécution | consigne (chemin, branche, commit), périmètre, ce qui exige l'utilisateur (sudo, PA-P), forme de fin attendue |
| `ACCUSÉ` | destinataire | dès réception, avant toute action | ordre reformulé en une phrase, références constatées (têtes de branche réelles), étapes prévues, écarts déjà visibles ; ou `REFUS` + raison |
| `AVANCEMENT` | destinataire | à chaque point d'arrêt, action de l'utilisateur demandée, ou étape longue franchie | étape, état, ce qui est attendu et de qui |
| `QUESTION` | l'une ou l'autre | décision nécessaire | question, options, conséquence ; l'émetteur attend la réponse |
| `FIN-SUCCÈS` | destinataire | travail terminé | résultat par critère de la consigne, commits et branches (poussés ou non), rapport (chemin), versions relevées, écarts et observations, ce qui n'a pas été fait |
| `FIN-ÉCHEC` | destinataire | arrêt sur erreur | étape, commande exacte, code de retour, extrait du message, journal (chemin), composant en cause, état laissé (fichiers modifiés, paquets installés), correction proposée, ce qui est attendu de l'utilisateur |

Règles :
- L'émetteur d'un `ORDRE` n'agit pas sur la suite tant que l'`ACCUSÉ` n'est pas reçu. Sans accusé :
  pas de supposition ; demander à l'utilisateur de vérifier la session destinataire, puis renvoyer
  une fois avec le même `ID`.
- Le destinataire n'exécute rien avant d'avoir envoyé l'`ACCUSÉ`, et termine toujours par
  `FIN-SUCCÈS` ou `FIN-ÉCHEC`, même interrompu.
- Réponse : à l'adresse `from` du message reçu.
- La session principale consigne chaque `ORDRE`, `ACCUSÉ` et `FIN-*` (ID, date, résumé) dans le
  rapport de l'étape, et la fin dans `DEVENV-STATUS.md` §Journal.
- Chaque consigne VM (`consignes/*.md`) contient un paragraphe « Communication » qui renvoie à ce
  paragraphe et fixe les `ID` et le nom de la session principale.

## 3. Cycle d'une session

### Début de session (obligatoire, dans cet ordre)

1. Lire `CLAUDE.md`, ce fichier, `DEVENV-STATUS.md`.
2. Lire la dernière passation `doc/devenv/handoff/env-<N-1>.md` (ou celle de l'étape en cours si
   elle a été interrompue).
3. Lire le fichier d'étape `doc/devenv/etapes/ENV-<N>-*.md` et les exigences qu'il cite dans
   `SPECIFICATION.md`.
4. Vérifier l'état réel : `git -C <dépôt> status` et `git branch --show-current` pour chaque dépôt
   touché par l'étape ; versions épinglées (§Versions de `DEVENV-STATUS.md`).
5. Passer en mode plan ; présenter le plan à l'utilisateur ; attendre son accord.

### Pendant la session

- Une branche par étape et par dépôt touché : `devenv/env-<N>` (créée depuis la branche indiquée
  dans `DEVENV-STATUS.md`).
- Commits mécaniques (renommages, déplacements, génération) séparés des commits de fond.
- S'arrêter à chaque point d'arrêt du §4 qui concerne l'étape, même si la suite semble évidente.
- Résultats volumineux (inventaires, journaux, rapports) dans `doc/devenv/rapports/`, référencés,
  jamais recopiés dans `DEVENV-STATUS.md`.
- Sous-agents : uniquement sur des ensembles de fichiers disjoints ; `DEVENV-STATUS.md`,
  `SPECIFICATION.md`, `ORCHESTRATION.md` et les `CMakeLists.txt` communs sont réservés à la session
  principale. ENV-4, ENV-5 et ENV-6 : session principale seule, aucun sous-agent en écriture.

### Fin de session (obligatoire, même si l'étape n'est pas terminée)

1. Mettre à jour `DEVENV-STATUS.md` : statut de l'étape, ligne de journal, prochaine action,
   décisions nouvelles, versions.
2. Écrire `doc/devenv/handoff/env-<N>.md` d'après `handoff/TEMPLATE.md`.
3. Commiter `doc/devenv/` sur la branche de l'étape.
4. Ne pas pousser. Annoncer à l'utilisateur ce qui reste et la prochaine action.

## 3bis. Passation entre sessions

La passation est le seul vecteur de contexte entre deux sessions. Elle contient : l'état exact
(branches, derniers commits, ce qui compile ou non), ce qui a été fait, ce qui reste, les décisions
prises pendant la session avec leur auteur (utilisateur ou proposition non validée), les pièges
rencontrés, la commande de reprise. Elle se lit seule, sans la conversation d'origine.

## 4. Points d'arrêt humains

La session s'arrête, expose la question et attend la réponse. La réponse est consignée dans
`DEVENV-STATUS.md` §Décisions avant de continuer.

| ID | Étape | Question ou validation | État |
| --- | --- | --- | --- |
| PA-0 | ENV-0 | Emplacements `<LEPTON_TOOLS>`, `<ROOTSTOCK>`, `<SEED_SCIONS>` ; mode d'échange git Mac / VM | ouvert |
| PA-1 | ENV-1 | Lecture des résultats d'essais : mode d'ouverture des fichiers (trunk ou clones), correspondance des chemins de débogage | ouvert |
| PA-2 | ENV-2 | Rapport d'audit : périmètre réel d'ENV-4, ENV-5, ENV-6, ENV-7 ; emplacement du code de carte | ouvert |
| PA-3 | ENV-3 | Validation des schémas (manifeste greffon, manifeste graine, XSD mklepton) avant toute implémentation | ouvert |
| PA-4 | ENV-4 | Liste des éléments XML retirés / ajoutés avant modification de mklepton | ouvert |
| PA-5 | ENV-5 | Oracle capturé (empreintes, test de fumée, banc KAL) avant la première modification CMake du greffon noyau | ouvert |
| PA-6 | ENV-5 | Non-régression constatée avant fusion | ouvert |
| PA-7 | ENV-6 | Liste des fichiers extraits vers chaque greffon BSP | ouvert |
| PA-8 | ENV-7 | Liste des évolutions de scion et numéro de version avant implémentation ; tag avant usage | ouvert |
| PA-9 | ENV-8 | Interface en ligne de commande de `lepton` (commandes, options, codes de retour) avant implémentation | ouvert |
| PA-10 | ENV-10 | Liste des extensions et versions épinglées | ouvert |
| PA-11 | ENV-11 | Autorisation d'écriture flash sur NUCLEO-F429ZI et NUCLEO-WL55JC1 | ouvert |
| PA-12 | ENV-12 | Décision de lancer l'extension (phase 2) | ouvert |
| PA-13 | ENV-13 | Séquence de regreffe de `<ROOTSTOCK>` (clés `family-`/`bsp-`, URL `https://`), éprouvée sur une copie d'essai | ouvert |
| PA-14 | ENV-13 | Push de la graine `original-tree` ; sort des anciens clones `depots/lepton-famille/*` et `depots/lepton-bsp/*` | ouvert |
| PA-15 | ENV-14 | Inventaire du nettoyage : liste des chemins à supprimer, arbitrages, documents à corriger, avant toute suppression | ouvert |
| PA-16 | ENV-14 | Rapport de non-régression : push de `devenv/env-14` du noyau pour la validation Debian ; après `FIN-SUCCÈS R14-1`, fusion dans `master` et push | ouvert |
| PA-17 | ENV-15 | Évolutions de scion avant implémentation : filtre des fichiers ignorés (E1), fichiers étrangers du trunk (E2), comportement des sources non git, numéro de version | ouvert |
| PA-18 | ENV-15 | Rapport : tag et push de `seed.scions`, push de `devenv/env-15` (lepton-tools), ordre R15-1 ; après `FIN-SUCCÈS R15-1`, fusion dans `main` et push | ouvert |
| PA-19 | ENV-16 | Option retenue pour la graine de référence (manifeste dans `original-tree` avec schéma étendu, ou `lepton check` qui admet une graine de référence) avant toute modification | ouvert |
| PA-20 | ENV-16 | Rapport : push de `devenv/env-16` et, le cas échéant, de la graine `original-tree` ; fusion dans `main` | ouvert |
| PA-21 | ENV-17 | Liste des corrections (documents vivants, messages CMake, skill) ; confirmation des propositions en attente (ENV-8 S2-S4, `bsp_demarrage`, §2bis) avant toute modification | ouvert |
| PA-22 | ENV-17 | Rapport : push de `devenv/env-17` (lepton-tools, clone noyau), fusion dans `main` et `master` | ouvert |
| PA-23 | ENV-18 | Commandes de `lepton` acceptées et refusées sur la graine de référence, nom de l'espace, sort de `CMakeUserPresets.json`, presets offerts, comportement de l'extension, avant toute modification | ouvert |
| PA-24 | ENV-18 | Rapport : push de `devenv/env-18`, fusion dans `main` | ouvert |
| PA-25 | ENV-19 | Liste d'extraction F746 et SAMD21, noms des greffons et des dépôts GitHub, sort du repli `cmake/boards`, cartes disponibles, avant toute modification | ouvert |
| PA-26 | ENV-19 | Rapport : push des nouveaux dépôts et des branches `devenv/env-19` ; fusion avant ou après la validation Debian d'ENV-21 | ouvert |
| PA-27 | ENV-20 | Table de vecteurs F4 complète, mode de création du BSP `nucleo-f439zi`, fichiers propres au F439, XML, presets, essai éventuel sur NUCLEO-F429ZI, avant toute modification | ouvert |
| PA-28 | ENV-20 | Rapport : push du dépôt du BSP et des branches `devenv/env-20`, fusions | ouvert |
| PA-29 | ENV-21 | Consigne `consignes/env-21-debian.md` et nettoyage de la VM ; push de `devenv/env-21`, ordre R21-1 | ouvert |
| PA-30 | ENV-21 | Après `FIN-SUCCÈS R21-1` : fusions dans `main` (et fusions différées d'ENV-19 et ENV-20), push | ouvert |
| PA-P | toutes | Tout `git push`, toute action `scion seed-update` / `graft-update` | permanent |

## 5. Règles de travail (rappel des acquis du portage)

| Sujet | Règle |
| --- | --- |
| Où éditer | Dans le clone du greffon (`depots/…/scion/…`), jamais dans `trunk/`. |
| Fichier nouveau dans un greffon | Créé dans le clone, puis `scion graft`. |
| `sed -i` et outils à renommage | Interdits sur le trunk ; dans le clone uniquement (ou `--follow-symlinks`). |
| Git | Commandes git natives `git -C <clone> …` ; jamais `scion git` pour lire (sortie non affichée en 0.5.0.1). |
| Build | `cmake -S <ROOTSTOCK>/trunk -B <ROOTSTOCK>/build/<preset>` ; aucune sortie dans le trunk. |
| Conteneur (option) | Monter le rootstock entier. |
| scion | Reste générique (NF-2) : aucune chaîne propre à Lepton dans `seed.scions`. |
| Push | Jamais sans accord explicite de l'utilisateur. |

## 5bis. Skills et hook

| Élément | Rôle | Étapes |
| --- | --- | --- |
| skill `devenv-session` | Procédure de début et de fin de session, passation | toutes |
| skill `lepton-rootstock` | Écriture dans les clones, regreffe, contrôles du trunk | 1, 5, 6, 8, 9, 11, 13, 14, 15, 17, 19, 20, 21 |
| skill `lepton-oracle` | Capture et comparaison de l'état de référence ; scripts `scripts/oracle/` | 0, 4, 5, 6, 11, 13, 14, 15, 17, 19, 20, 21 |
| skill `lepton-cibles` | Construction, QEMU, banc KAL, flash, débogage ; valeurs complétées en ENV-2 | 0, 5, 6, 9, 11, 13, 14, 17, 18, 19, 20, 21 |
| hook `proteger-trunk.py` | Refuse Write/Edit sous `<ROOTSTOCK>/trunk/` et les commandes shell d'écriture visant `trunk/` | toutes |

Une skill se corrige comme le code : sur la branche de l'étape, commit dédié, ligne de journal
dans `DEVENV-STATUS.md`. La skill `lepton-portage-instructions` (hors de ce dépôt) sert à réviser
ce plan.

## 6. Graphe des étapes

| Étape | Titre | Dépend de |
| --- | --- | --- |
| ENV-0 | Cadrage | — |
| ENV-1 | Levée des risques éditeur | ENV-0 |
| ENV-2 | Audit de l'existant | ENV-0 |
| ENV-3 | Schémas (manifestes JSON, XSD mklepton) | ENV-2 |
| ENV-4 | Évolution du format XML de mklepton | ENV-3 |
| ENV-5 | Restructuration CMake du greffon noyau | ENV-3 |
| ENV-6 | Greffons BSP de référence | ENV-5 |
| ENV-7 | Évolutions génériques de scion | ENV-2 |
| ENV-8 | Outil `lepton` | ENV-5, ENV-7 |
| ENV-9 | Génération des fichiers de l'éditeur | ENV-1, ENV-6, ENV-8 |
| ENV-10 | Script d'installation VSCodium | ENV-0 (indépendante) |
| ENV-11 | Validation de bout en bout | ENV-4, ENV-9, ENV-10 |
| ENV-12 | Extension VSCodium (phase 2) | ENV-11 |
| ENV-13 | Graine de référence publiée | ENV-6, ENV-11 |
| ENV-14 | Nettoyage de l'arbre | ENV-13 |
| ENV-15 | Fichiers ignorés et fichiers étrangers dans scion | ENV-14 |
| ENV-16 | Graine de référence et `lepton check` | ENV-13 (indépendante d'ENV-15) |
| ENV-17 | Cohérence de la documentation et des messages | ENV-16 |
| ENV-18 | Graine de référence gérée par `lepton` | ENV-16 (indépendante d'ENV-17, ENV-19, ENV-20) |
| ENV-19 | Extraction des cartes STM32F746G-DISCO et SAMD21 Xplained Pro | ENV-14 ; ENV-17 conseillée avant |
| ENV-20 | BSP `nucleo-f439zi` | ENV-19 (graine `original-tree` et presets du noyau partagés) |
| ENV-21 | Validation Debian groupée | ENV-17, ENV-18, ENV-19, ENV-20 |

Ordre conseillé : 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12. ENV-1 et ENV-2 sont permutables ;
ENV-4 et ENV-5 aussi ; ENV-7 peut suivre directement ENV-2 si l'audit le justifie.
