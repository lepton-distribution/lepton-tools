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
| Dépôt `seed.scions` | clone à part, `<SEED_SCIONS>` — résolu en ENV-0 (PA-0) : `DEVENV-STATUS.md` §Emplacements | Évolutions génériques de scion (ENV-7, ENV-15, ENV-23, ENV-29, ENV-39, ENV-40 ; correctif éventuel décidé au PA-75 ou au PA-83, de préférence dans une étape scion insérée) |
| Répertoire de construction | `<ROOTSTOCK>/build/<preset>` | Toujours hors du trunk |

Claude Code est lancé à la racine de `<LEPTON_TOOLS>`. Les chemins `<…>` sont résolus une fois en
ENV-0 et recopiés dans `DEVENV-STATUS.md` §Emplacements ; les fichiers d'étape les utilisent tels
quels.

Hôtes :

| Hôte | Rôle | Étapes |
| --- | --- | --- |
| Mac mini Intel, macOS (hôte principal) | Développement, construction native, flash et débogage | Toutes |
| VM Debian x86_64 (si accès donné) | Validation Debian uniquement, dans une session Claude Code distincte | ENV-10 (partie Debian), ENV-11 (partie Debian), ENV-14 (partie Debian), ENV-15 (partie Debian), ENV-21, ENV-28, ENV-33, ENV-36, ENV-43, ENV-50 |

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
- **Remise en échec** (D9 d'ENV-44, constat de R43-1) : l'émetteur dont l'envoi échoue (erreur
  du canal, ECONNRESET, « bridge ID is stale ») le renvoie une fois. Si le second envoi échoue,
  il consigne le message en entier dans son journal (VM : `rapports/env-N-debian.md` §Messages,
  avec la mention « non remis ») et l'annonce à l'utilisateur. L'utilisateur relaie : il colle
  dans l'autre session la première ligne `[<TYPE> <ID>]` et le corps, inchangés. Le destinataire
  tient un message relayé pour reçu s'il porte le bon `ID`. Il le consigne avec la mention
  « relayé par l'utilisateur » et y répond normalement ; sa réponse peut à son tour être relayée.
  Un `ACCUSÉ` relayé vaut accusé. Si l'utilisateur fait poursuivre le destinataire sans relais,
  c'est sa décision : la session principale la consigne au journal, et les messages manquants
  sont lus dans le rapport du destinataire avant toute fusion.
- Le destinataire n'exécute rien avant d'avoir envoyé l'`ACCUSÉ`, et termine toujours par
  `FIN-SUCCÈS` ou `FIN-ÉCHEC`, même interrompu.
- Réponse : à l'adresse `from` du message reçu.
- La session principale consigne chaque `ORDRE`, `ACCUSÉ` et `FIN-*` (ID, date, résumé) dans le
  rapport de l'étape, et la fin dans `DEVENV-STATUS.md` §Journal.
- Chaque consigne VM (`consignes/*.md`) contient un paragraphe « Communication » qui renvoie à ce
  paragraphe et fixe les `ID` et le nom de la session principale.

Règles des consignes VM (décision PA-31 d'ENV-22, 2026-11-02 ; leçons de R15-1 et R21-1) :
- **Régénérer avant de relever** (E-1 de `rapports/env-21-debian.md`) : l'empreinte « avant » d'un
  fichier généré (espace de travail, presets, verrou) se relève juste après l'avoir régénéré par la
  commande qui le produit, jamais sur un fichier écrit lors d'une étape antérieure. Sinon la
  comparaison mesure les changements de l'outil ou de l'hôte survenus entre-temps.
- **Commandes confiées d'emblée à l'utilisateur** (E-2 de `rapports/env-21-debian.md`,
  `rapports/env-15-scion.md` §8) : le classifieur de permissions de la session VM peut refuser les
  suppressions (`rm -rf`), les installations `pipx install`, les clonages et les lancements de
  tests, même accordés au point d'arrêt. La consigne les attribue à l'utilisateur dès sa rédaction
  (colonne « Autorisé » du §2 et étape concernée), avec la commande exacte à lancer. La session VM
  annonce l'attente par un `AVANCEMENT`, vérifie ensuite l'effet (absence, version, code de
  retour) et le consigne. Un refus n'est jamais contourné. R28-1 : `scion graft-update` a été
  refusé à la session VM (« Untrusted Code Integration ») ; `rootstock-install`, `seed-add`,
  `graft` et `rejouer-oracle.sh` acceptés.
- **Branche des clones d'un rootstock existant** (P-1 d'ENV-28, E-1 de `rapports/env-28-debian.md`,
  décision du 2026-11-02 ; allégée au PA-45 d'ENV-29, 2026-11-03) : avant tout `graft-update` ou
  toute lecture d'un rootstock existant, les vérifications préalables de la consigne relèvent la
  branche courante de chaque clone (`git -C <clone> branch --show-current`) et la consignent dans
  le rapport. Depuis scion 0.5.4.0, `graft-update`, `seed-update` et `seed-add` refusent eux-mêmes
  un clone hors de sa version déclarée, avant tout dégreffage. `graft` et `graft-update` rétablissent
  le trunk si la regreffe échoue. L'arrêt manuel n'est donc plus requis. Exception : sur un hôte qui a
  encore scion 0.5.3.0, un clone hors version reste un arrêt : 0.5.3.0 tire la branche courante et
  vide le trunk sur un conflit (cas de la VM jusqu'à R33-1 d'ENV-33 ; elle a 0.5.4.0 depuis).

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
| PA-31 | ENV-22 | Contenu de `<ROOTSTOCK>/.scion.trunk.tolerated`, confirmation des propositions non validées d'ENV-17 à ENV-20, sort d'`essais/env-11/bout-en-bout`, emplacement des règles des consignes VM, avant toute modification | ouvert |
| PA-32 | ENV-22 | Rapport : fusion de `devenv/env-22` dans `main`, push | ouvert |
| PA-33 | ENV-23 | Forme de la mise à jour de la graine par `graft-update`, filtrage des fichiers étrangers des sources non git, numéro de version, effets sur lepton, avant toute modification | ouvert |
| PA-34 | ENV-23 | Rapport : publication du tag et de `master` de `seed.scions`, branches `devenv/env-23`, fusions | ouvert |
| PA-35 | ENV-24 | XML passés au cpufs automatique, contrôle `mklepton_format_check.cmake`, critère de non-régression, cartes disponibles, avant toute modification | ouvert |
| PA-36 | ENV-24 | Rapport : fusion et push de `devenv/env-24` (lepton-tools, clone noyau) | ouvert |
| PA-37 | ENV-25 | Lancements hôtes de `mklepton` (nombre, arguments, débogueur Debian, tâche préalable), avant toute modification | ouvert |
| PA-38 | ENV-25 | Rapport : fusion et push de `devenv/env-25` | ouvert |
| PA-39 | ENV-26 | Fichiers SVD (source, licence, emplacement, champ `svd`), vue des tâches (embOS, FreeRTOS), cartes disponibles, avant toute modification | ouvert |
| PA-40 | ENV-26 | Rapport : push des greffons et des branches `devenv/env-26`, fusions | ouvert |
| PA-41 | ENV-27 | Forme de la découverte des tests des greffons, schéma, types de tests, greffon d'essai, modèles de `scion new`, avant toute modification | ouvert |
| PA-42 | ENV-27 | Rapport : push et fusions des branches `devenv/env-27` | ouvert |
| PA-43 | ENV-28 | Consigne `consignes/env-28-debian.md` et nettoyage de la VM ; push de `devenv/env-28`, ordre R28-1 | ouvert |
| PA-44 | ENV-28 | Après `FIN-SUCCÈS R28-1` : fusions dans `main`, push | ouvert |
| PA-45 | ENV-29 | Comportement de `graft-update` sur un clone hors version déclarée, préservation du trunk en cas d'échec, numéro de version, effets sur lepton, sort de la règle P-1 (§2bis), avant toute modification | ouvert |
| PA-46 | ENV-29 | Rapport : publication du tag et de `master` de `seed.scions`, branches `devenv/env-29`, fusions | ouvert |
| PA-47 | ENV-30 | Tâche « tests des greffons » : configurations visées, présence sans test de greffon, libellé et arguments, avant toute modification | ouvert |
| PA-48 | ENV-30 | Rapport : fusion et push de `devenv/env-30` | ouvert |
| PA-49 | ENV-31 | Options FreeRTOS activées, portée (presets), critère d'écart accepté des binaires FreeRTOS, cartes disponibles, avant toute modification | ouvert |
| PA-50 | ENV-31 | Rapport : nouvel oracle de référence ; fusion et push de `devenv/env-31` (lepton-tools, clone noyau) | ouvert |
| PA-51 | ENV-32 | Test radio fourni par le BSP `nucleo-wl55jc1` : emplacement du script, accès à `smoke_lsh`, nom et étiquettes du test, sort du script du noyau, cartes disponibles, avant toute modification | ouvert |
| PA-52 | ENV-32 | Rapport : push et fusions des branches `devenv/env-32` (lepton-tools, clone noyau, BSP) | ouvert |
| PA-53 | ENV-33 | Consigne `consignes/env-33-debian.md` et nettoyage de la VM ; push de `devenv/env-33`, ordre R33-1 | ouvert |
| PA-54 | ENV-33 | Après `FIN-SUCCÈS R33-1` : fusions dans `main`, push | ouvert |
| PA-55 | ENV-34 | Import de la HAL F4 v1.8.5 et du CMSIS device F4 : destination, contenu repris, sous-ensemble de puces, `core_cm4.h` (fins de ligne, provenance), sort des fichiers hors amont, clones amont, script de vérification et compilation à blanc, avant toute modification | ouvert |
| PA-56 | ENV-34 | Rapport : push et fusions des branches `devenv/env-34` (lepton-tools, famille, clone noyau) | ouvert |
| PA-57 | ENV-35 | Passage de la SPL à la HAL : architecture (API Lepton F4 conservée ou structure F7), modules HAL, USART, découpage en lots (coexistence SPL/HAL), `STM32F439xx`, sort de la SPL, critère d'occupation, cartes, avant toute modification | ouvert |
| PA-58 | ENV-35 | Rapport : nouvel oracle de référence ; push et fusions des branches `devenv/env-35` | ouvert |
| PA-59 | ENV-36 | Consigne `consignes/env-36-debian.md`, cartes et nettoyage de la VM ; push de `devenv/env-36`, ordre R36-1 | ouvert |
| PA-60 | ENV-36 | Après `FIN-SUCCÈS R36-1` : fusions dans `main`, push | ouvert |
| PA-61 | ENV-37 | Code tiers de la famille STM32WL : révisions amont retenues, sort des fichiers modifiés par Lepton et des fichiers hors amont, forme de la provenance, texte du manifeste, source de la pile radio et des utilitaires, avant toute modification | ouvert |
| PA-62 | ENV-37 | Rapport : push et fusions des branches `devenv/env-37` (lepton-tools, famille WL) | ouvert |
| PA-63 | ENV-38 | Projection et miroir de scion : syntaxe de `.scion.projections`, sémantique des motifs, motif sans correspondance, révision épinglée, emplacement des clones tiers, articulation avec la graine, dépendance d'un greffon envers une projection, commande de miroir, versions, provenance, emplacement de la spécification, avant toute rédaction | ouvert |
| PA-64 | ENV-38 | Spécification validée ; push et fusions des branches `devenv/env-38` | ouvert |
| PA-65 | ENV-39 | Projection : écarts à la spécification, numéro de version, `SCION_MIN_VERSION`, effets sur lepton traités ici ou en ENV-41, avant toute modification | ouvert |
| PA-66 | ENV-39 | Rapport : publication du tag et de `master` de `seed.scions`, branches `devenv/env-39`, fusions | ouvert |
| PA-67 | ENV-40 | Miroir : écarts à la spécification, numéro de version, `SCION_MIN_VERSION`, avant toute modification | ouvert |
| PA-68 | ENV-40 | Miroirs sous `lepton-distribution/` : noms, visibilité, contenu, périmètre, auteur de la création, avant toute création ; publication du tag et de `master` de `seed.scions`, fusions | ouvert |
| PA-69 | ENV-41 | Bascule du F4 : lignes de projection, sort des provenances et licences, graines de projet qui référencent la famille, modifications de lepton, scripts `scripts/tiers/`, skill et hook, avant toute modification | ouvert |
| PA-70 | ENV-41 | Rapport : ordre de publication de la graine `original-tree` et de la famille F4 ; push et fusions des branches `devenv/env-41` | ouvert |
| PA-71 | ENV-42 | `core_cm4.h` : option (5.9.0 pour les Cortex-M4, retrait du 5.9.0, statu quo), sort de V3.30, critère d'écart par preset, cartes et écriture flash, avant toute modification | ouvert |
| PA-72 | ENV-42 | Rapport : nouvel oracle de référence si des binaires ont changé ; push et fusions des branches `devenv/env-42` (lepton-tools, clone noyau) | ouvert |
| PA-73 | ENV-43 | Consigne `consignes/env-43-debian.md`, critères C6 à C8 (miroir, cartes, nettoyage de la VM) ; push de `devenv/env-43`, ordre R43-1 | ouvert |
| PA-74 | ENV-43 | Après `FIN-SUCCÈS R43-1` : fusions dans `main`, push | ouvert |
| PA-75 | ENV-44 | Résidus D1, D2, D3, D5, D6, D7, D9 : essai d'un porteur dans `seed replace`/`remove`, débogage réel de la table tiers → trunk, correction du hook, `ARMCM4` CMSIS 5 de l'an386 et critère d'écart, script, documentation V3.30, amendement du §2bis, avant toute modification | ouvert |
| PA-76 | ENV-44 | Rapport : nouvel oracle de référence si l'an386 change ; push et fusions des branches `devenv/env-44` | ouvert |
| PA-77 | ENV-45 | Choix de la sonde : forme (par BSP ou générique dans le lecteur du noyau), nom de la variable, sort de `LEPTON_BOARD_STLINK_SERIAL`, lien avec `lepton generate --probe-serial`, cartes et numéros, avant toute modification | ouvert |
| PA-78 | ENV-45 | Rapport : push et fusions des branches `devenv/env-45` | ouvert |
| PA-79 | ENV-46 | Retrait de la SPL F4 : périmètre (`driverlib/`, `eth.c`, `dev_stm32f4xx_eth.c`), sort des dépendants hors plan (A3), `USART_ChangeBaudrate`, conservation de l'historique, avant toute modification | ouvert |
| PA-80 | ENV-46 | Rapport : push et fusions des branches `devenv/env-46` | ouvert |
| PA-81 | ENV-47 | Bascule du F7 : lignes de projection, miroirs (noms, visibilité, création), sort des provenances, modifications de lepton, avant toute modification | ouvert |
| PA-82 | ENV-47 | Rapport : ordre de publication (miroirs, famille) ; push et fusions des branches `devenv/env-47` | ouvert |
| PA-83 | ENV-48 | Bascule du WL : lignes de projection, 4 miroirs (dont STM32CubeWL), correctif éventuel de scion, raison de la neutralisation de `RadioIsChannelFree` (C1), `LICENSE.txt` (C2), provenances, avant toute modification | ouvert |
| PA-84 | ENV-48 | Rapport : publication (miroirs, scion le cas échéant, famille) ; push et fusions des branches `devenv/env-48` | ouvert |
| PA-85 | ENV-49 | Montée de version du code tiers WL : versions cibles et périmètre, report des fichiers modifiés par Lepton, couche Lepton, critère d'écart des presets WL55, cartes, avant toute modification | ouvert |
| PA-86 | ENV-49 | Rapport : nouvel oracle de référence ; publication, push et fusions des branches `devenv/env-49` | ouvert |
| PA-87 | ENV-50 | Consigne `consignes/env-50-debian.md`, critères C5, C7, C8 (hook et scripts, cartes et sonde, nettoyage de la VM) ; push de `devenv/env-50`, ordre R50-1 | ouvert |
| PA-88 | ENV-50 | Après `FIN-SUCCÈS R50-1` : fusions dans `main`, push | ouvert |
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
| skill `lepton-rootstock` | Écriture dans les clones, regreffe, contrôles du trunk | 1, 5, 6, 8, 9, 11, 13, 14, 15, 17, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 31, 32, 33, 34, 35, 36, 37, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50 |
| skill `lepton-oracle` | Capture et comparaison de l'état de référence ; scripts `scripts/oracle/` | 0, 4, 5, 6, 11, 13, 14, 15, 17, 19, 20, 21, 23, 24, 26, 27, 28, 29, 31, 32, 33, 34, 35, 36, 37, 39, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50 |
| skill `lepton-cibles` | Construction, QEMU, banc KAL, flash, débogage ; valeurs complétées en ENV-2 | 0, 5, 6, 9, 11, 13, 14, 17, 18, 19, 20, 21, 24, 25, 26, 27, 28, 30, 31, 32, 33, 34, 35, 36, 37, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50 |
| hook `proteger-trunk.py` | Refuse Write/Edit sous `<ROOTSTOCK>/trunk/` et `<ROOTSTOCK>/depots/tiers/` (ENV-41), et les commandes shell qui y écrivent (analyse par commande simple depuis ENV-44 ; tests `tests/test_proteger_trunk.py`) | toutes |

Une skill se corrige comme le code : sur la branche de l'étape, commit dédié, ligne de journal
dans `DEVENV-STATUS.md`. La skill `lepton-portage-instructions` (hors de ce dépôt) sert à réviser
ce plan.

Relecture d'une révision du plan (décision de l'utilisateur du 2026-11-09) : avant tout commit,
toute révision du plan est relue par un agent indépendant.
- L'agent a l'effort `xhigh` et travaille en lecture seule.
- Il reçoit les fichiers, les décisions de l'utilisateur et les sources des faits, mais pas les
  conclusions de la session.
- La session vérifie elle-même les constats principaux, les présente à l'utilisateur et n'applique
  que ceux qu'il retient.
- Le résultat (constats appliqués, écartés, non confirmés) est consigné au journal.

Précédent : révision du 2026-11-09, ENV-44 à ENV-50. La même règle figure à l'étape 8 de la skill.

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
| ENV-22 | Résidus d'ENV-17 à ENV-21 | ENV-21 |
| ENV-23 | Évolutions de scion : mise à jour de la graine, sources non git | ENV-22 |
| ENV-24 | Dimensionnement automatique du cpufs | ENV-22 ; ENV-23 conseillée avant |
| ENV-25 | DBG-5 : déboguer `mklepton` sur l'hôte | ENV-22 |
| ENV-26 | DBG-4 : vues des périphériques et des tâches | ENV-25 (`generate.py` partagé) |
| ENV-27 | TST-2 : tests fournis par un greffon | ENV-26 (schéma du greffon partagé) |
| ENV-28 | Validation Debian groupée | ENV-23, ENV-24, ENV-25, ENV-26, ENV-27 |
| ENV-29 | scion : `graft-update` sûr (version déclarée, trunk préservé) | ENV-28 |
| ENV-30 | Tâche de l'éditeur « tests des greffons » | ENV-28 (indépendante d'ENV-29, ENV-31) |
| ENV-31 | Piles FreeRTOS lisibles par rtos-views | ENV-28 (indépendante d'ENV-29, ENV-30) |
| ENV-32 | Test `board.radio` fourni par le BSP `nucleo-wl55jc1` | ENV-28 ; ENV-30 conseillée avant |
| ENV-33 | Validation Debian groupée | ENV-29, ENV-30, ENV-31, ENV-32 |
| ENV-34 | HAL et CMSIS device STM32F4 importés par la méthode du F7 | ENV-33 |
| ENV-35 | Famille STM32F4 : passage de la SPL à la HAL | ENV-34 (HAL, CMSIS device et `core_cm4.h` importés) |
| ENV-36 | Validation Debian groupée | ENV-34, ENV-35 |
| ENV-37 | Famille STM32WL : audit et provenance du code tiers | ENV-36 |
| ENV-38 | scion : conception de la projection et du miroir | ENV-37 (cas d'épreuve WL) |
| ENV-39 | scion : projection d'un dépôt tiers | ENV-38 |
| ENV-40 | scion : miroir de conservation | ENV-38 (indépendante d'ENV-39) |
| ENV-41 | Famille STM32F4 : copie d'ENV-34 remplacée par la projection | ENV-39, ENV-40 |
| ENV-42 | `core_cm4.h` : un seul CMSIS-Core pour les Cortex-M4 | ENV-36 (indépendante d'ENV-37 à ENV-41 ; ENV-41 conseillée avant) |
| ENV-43 | Validation Debian groupée | ENV-37, ENV-38, ENV-39, ENV-40, ENV-41, ENV-42 |
| ENV-44 | Résidus d'ENV-37 à ENV-43 | ENV-43 |
| ENV-45 | Sonde choisie par numéro de série | ENV-44 (indépendante d'ENV-46, ENV-47) |
| ENV-46 | Famille STM32F4 : retrait de la SPL | ENV-44 (indépendante d'ENV-45, ENV-47) |
| ENV-47 | Famille STM32F7 : copie remplacée par la projection | ENV-44 (indépendante d'ENV-45, ENV-46) |
| ENV-48 | Famille STM32WL : copie remplacée par la projection | ENV-47 (méthode et miroirs éprouvés sur le F7) |
| ENV-49 | Famille STM32WL : montée de version de la HAL | ENV-48 (code tiers WL projeté) |
| ENV-50 | Validation Debian groupée | ENV-44, ENV-45, ENV-46, ENV-47, ENV-48, ENV-49 |

Ordre conseillé : 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12. ENV-1 et ENV-2 sont permutables ;
ENV-4 et ENV-5 aussi ; ENV-7 peut suivre directement ENV-2 si l'audit le justifie.
Révision du 2026-10-31 : 22, 23, 24, 25, 26, 27, 28 (consolidation, puis fonctions P2, puis
validation Debian).
Révision du 2026-11-02 : 29, 30, 31, 32, 33 (31 et 32 permutables ; ENV-29 d'abord, pour que les
regreffes d'ENV-33 profitent du correctif de scion ; ENV-30 avant ENV-32, tâche de l'éditeur
réutilisable pour les tests de carte).
Révision du 2026-11-04 : 34, 35, 36, strictement dans cet ordre (niveau 1 : import tracé sans
changement de compilation ; niveau 2 : passage à la HAL ; puis validation Debian).
Révision du 2026-11-05 : 37, 38, 39, 40, 41, 42, 43 (39 et 40 permutables ; ENV-37 d'abord, pour
que la conception de la projection dispose du cas WL ; ENV-42 après ENV-41, une variable à la
fois ; seule la famille F4 bascule sur la projection, le F7 et le WL à la révision suivante).
Révision du 2026-11-09 (fin du plan précédent, à partir de `HORS-PLAN.md`) : 44, 45, 46, 47, 48, 49,
50 (45, 46 et 47 permutables ; ENV-44 d'abord, consolidation ; WL après le F7, le cas simple
d'abord ; montée de version de la HAL WL après sa projection).
