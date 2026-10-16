# Environnement de développement Lepton — spécification fonctionnelle

Version du 2026-10-12, amendée le 2026-10-13 (PA-2, PA-3). Copie de référence pour les sessions Claude Code ; toute modification de la
spécification passe par l'utilisateur (point d'arrêt), puis par une mise à jour de ce fichier.

## Objet et vocabulaire

L'environnement doit permettre à un développeur de créer, configurer, construire, flasher et
déboguer un logiciel embarqué Lepton composé de greffons, sous VSCodium, sur macOS (Intel puis
Apple Silicon) et Debian. Il s'appuie sur l'outil `scion` existant au lieu de le réinventer : la
graine et les greffons du besoin sont exactement le seed et les scions de scion.

| Terme du besoin | Terme scion | Définition retenue |
| --- | --- | --- |
| Graine | seed | Dépôt (git) qui liste les greffons d'un projet et leur version : `.scion.sources.list`. Une graine = un logiciel embarqué. |
| Greffon | scion | Sous-arbre de sources, dans un dépôt git ou un répertoire local, greffé dans le trunk par liens symboliques feuille à feuille. |
| Porte-greffe | rootstock | Répertoire de travail marqué par `.scion.rootstock.signature` ; contient `depots/` (clones) et `trunk/`. |
| Arbre Lepton | trunk | Vue composée, en liens relatifs, jetable : c'est la racine de la construction CMake. |
| Clone | depot | Copie git d'un greffon dans `depots/` : seul endroit où les fichiers sont réellement écrits et versionnés. |

Types de greffons :

| Type | Destination dans le trunk (besoin) | Contenu | Bibliothèque CMake |
| --- | --- | --- | --- |
| Noyau | `kernel/`, `kernel/dev/arch`, `lib/`, `sbin/`, `bin/` de base | Greffons de base Lepton, `main` générique, démarrage générique par ISA (`kernel/core/arch/cortexm`) | `kernel`, `lib`, `sbin`, `bin` |
| Famille | `kernel/dev/arch/<famille>` | Couche Lepton d'une famille de puces, pilotes tiers (HAL/SPL, CMSIS device), table de vecteurs par MCU, remplaçants forts de symboles faibles | `kernel` |
| BSP (carte) | `kernel/dev/bsp/<carte>` | Initialisation d'horloge (`SystemInit`), script d'édition de liens, GPIO, pilotes des composants de la carte (EEPROM, modem, ADC/DAC, NFC…) ; repose sur un greffon famille | `bsp` (bibliothèque distincte) |
| Application | `bin/<appli>` | Programmes de l'utilisateur | `bin` |
| Bibliothèque | `lib/<nom>` | Bibliothèques tierces ou métier | `lib` ou dédiée |

Les chemins du besoin sont relatifs à `sys/root/src/` (décision 1).

Hors périmètre : la refonte du noyau, l'ajout de cœurs (RISC-V, TrustZone) et le backend FreeRTOS,
que l'environnement doit seulement pouvoir accueillir sans modification de structure.

## Acquis du portage

| Acquis | Ce que l'environnement en fait |
| --- | --- |
| `scion` 0.5 (générique, liens relatifs, sans `SCION_ROOTSTOCK`) | Socle de la gestion graine/greffons |
| Graine `lepton-seed.scions`, greffon `lepton-original-tree.scions` | Graine modèle et greffon noyau |
| CMake + `toolchain-arm-none-eabi.cmake`, presets par cible | Construction pilotée par CMake Tools |
| KAL décomposée `arch/` × `backend/`, sélection par variables CMake | Options de configuration noyau exposées |
| `mklepton` 64 bits natif (XML → C, image UFS) via `add_custom_command` | Étape de construction ; maître de la configuration logicielle (CFG-1) |
| QEMU (cible générique), banc KAL | Exécution et tests sans carte |
| OpenOCD + GDB ARM natifs macOS (MacPorts sur Intel) ; cartes NUCLEO-F429ZI, NUCLEO-WL55JC1, SAMD21, Discovery F7, Olimex P407 | Configurations de flash et de débogage par BSP |
| `install-macos.sh`, `install-debian.sh` (`--minimal`, `--with-debug-tools`, `--with-jlink`) | Base du script d'installation de VSCodium |

Règles apprises pendant le portage, à faire respecter par l'outillage :

- On édite dans le clone, jamais dans le trunk : un outil qui écrit par fichier temporaire puis
  renommage (`sed -i`) remplace le lien par un fichier non versionné.
- Un fichier régulier dans le trunk fait échouer `scion graft` ; un fichier nouveau doit être créé
  dans le clone puis regreffé.
- Le répertoire de construction est hors du trunk.
- En conteneur, on monte le rootstock entier, sinon les liens ne résolvent plus.
- `seed-update` et `graft-update` font un `git pull` : action explicite, jamais implicite.

## Exigences fonctionnelles

P1 = nécessaire au premier projet utilisateur ; P2 = confort ou extension.

### A. Installation de l'environnement

| ID | Exigence | Vérification | Prio. |
| --- | --- | --- | --- |
| INS-1 | Un script `install-vscodium.sh` installe VSCodium sur macOS Intel, macOS Apple Silicon et Debian, sans passer par le Marketplace Microsoft (extensions depuis Open VSX). | Exécution sur les 3 hôtes ; `codium --version` | P1 |
| INS-2 | Il installe une liste d'extensions épinglées par version, lue dans un fichier séparé (`extensions.lst`), pas codée dans le script. | `codium --list-extensions --show-versions` = liste | P1 |
| INS-3 | Il réutilise `install-macos.sh` / `install-debian.sh` pour la chaîne (GCC, CMake, Ninja, QEMU, OpenOCD, GDB) au lieu de les dupliquer. | Aucune commande de paquet chaîne dans le nouveau script | P1 |
| INS-4 | Il est idempotent et lisible : une fonction par étape, mode `--dry-run` qui affiche sans exécuter. | Deux exécutions successives sans erreur | P1 |
| INS-5 | Gestionnaire de paquets par hôte : MacPorts sur Mac Intel (Homebrew ne fournit plus de binaires pour Intel), Homebrew sur Apple Silicon, APT sur Debian ; aucun préfixe codé en dur (`port`, `brew --prefix`). | Revue + exécution sur Mac Intel ; revue pour Apple Silicon | P1 |
| INS-6 | Il installe les outils Lepton côté hôte : `scion` (version épinglée, `pipx`) et l'outil `lepton`. | `scion version`, `lepton --version` | P1 |

Extensions de départ, à vérifier sur Open VSX : clangd, CMake Tools, Cortex-Debug et ses
dépendances, CodeLLDB (débogage de `mklepton` sur l'hôte), XML avec schéma XSD (configuration
mklepton ; le JSON Schema des manifestes est géré nativement par VSCodium), Claude Code.
L'extension C/C++ de Microsoft est exclue : sa licence l'interdit hors VS Code.

### B. Gestion de la graine

| ID | Exigence | Vérification | Prio. |
| --- | --- | --- | --- |
| GRA-1 | Créer une graine depuis un modèle : nom du projet, version du greffon noyau, cible (BSP), dépôt git de destination ou répertoire local. | `lepton seed new` produit un rootstock greffé et construisible | P1 |
| GRA-2 | La graine référence au moins le greffon noyau et un greffon BSP ; zéro ou plusieurs greffons application ou bibliothèque (un système limité aux binaires de base est valide). | Construction refusée avec message explicite si le noyau ou le BSP manque ; graine sans application construite | P1 |
| GRA-3 | Chaque greffon de la graine est soit un dépôt git (URL + branche ou tag), soit un répertoire local. | Les deux formes greffent | P1 |
| GRA-4 | Ajouter, retirer, remplacer un greffon dans la graine met à jour `.scion.sources.list`, regreffe et reconfigure CMake. | Trunk et cache CMake cohérents après chaque opération | P1 |
| GRA-5 | Figer la graine : enregistrer le commit exact de chaque greffon. | `lepton seed lock` puis reconstruction identique | P2 |
| GRA-6 | Afficher l'état : greffons, origine, branche, modifications locales non commitées. | `lepton seed status` | P1 |

### C. Gestion des greffons

| ID | Exigence | Vérification | Prio. |
| --- | --- | --- | --- |
| GRF-1 | Créer un greffon d'un type donné (BSP, application, bibliothèque) depuis un modèle : arborescence `scion/…`, manifeste, `CMakeLists.txt` facultatif (règles propres au greffon), fichier exemple, dépôt git initialisé. | Greffon neuf greffé et construit sans édition manuelle | P1 |
| GRF-2 | Chaque greffon porte un manifeste déclaratif en JSON, lu directement par CMake (`string(JSON)`, CMake ≥ 3.24) : nom, type, version, destination dans le trunk, bibliothèque cible, dépendances, options configurables. | Validation du manifeste par JSON Schema | P1 |
| GRF-3 | Un greffon BSP déclare : greffon famille, famille de cœur (M0+, M4, M7…), ABI flottante imposée éventuelle, MCU, fréquence du cœur, en-tête de configuration noyau de la carte, script d'édition de liens, démarrage (horloge), configuration OpenOCD/sonde, SVD, cible QEMU éventuelle. Un greffon famille déclare ses cœurs, ses MCU, ses tables de vecteurs et ses remplaçants forts. | Les presets et `launch.json` en sont dérivés | P1 |
| GRF-4 | Supprimer un greffon retire ses liens du trunk et ses cibles CMake, sans toucher à son dépôt. | Trunk sans lien orphelin ; clone intact | P1 |
| GRF-5 | Les dépendances déclarées sont vérifiées (un BSP M4 avec un noyau sans `arch` M4 est refusé). | Message d'erreur avant compilation | P2 |

### D. Fichiers et répertoires d'un greffon

| ID | Exigence | Vérification | Prio. |
| --- | --- | --- | --- |
| FIC-1 | Créer, ajouter, supprimer un fichier (`.c`, `.cpp`, `.S`, `.h`, `CMakeLists.txt`, `.ld`) dans un greffon le fait apparaître ou disparaître du trunk, sans action manuelle. | Le lien apparaît ou disparaît dans le trunk | P1 |
| FIC-2 | Idem pour un répertoire. | Idem | P1 |
| FIC-3 | La création se fait toujours dans le clone du greffon propriétaire, jamais comme fichier régulier dans le trunk. | Aucun fichier régulier dans `trunk/` | P1 |
| FIC-4 | Un fichier source ajouté entre dans la construction sans éditer de liste CMake (découverte par répertoire déclaré dans le manifeste). | Reconfiguration CMake automatique ; objet compilé | P1 |
| FIC-5 | La sauvegarde d'un fichier ouvert via le trunk écrit dans la cible du lien, pas à la place du lien. | Lien préservé après sauvegarde depuis VSCodium | P1 |
| FIC-6 | Renommer ou déplacer un fichier conserve l'historique git (`git mv` dans le clone). | `git log --follow` | P2 |

### E. Configuration

| ID | Exigence | Vérification | Prio. |
| --- | --- | --- | --- |
| CFG-1 | Deux sources de configuration indépendantes, sans recouvrement, versionnées dans la graine : le XML mklepton pour la configuration logicielle de Lepton et de son système de fichiers racine ; les manifestes de la graine et des greffons (BSP en tête) pour le cœur, l'architecture, le backend et les options de compilation, dont dérivent CMake, les presets et les fichiers de l'éditeur. | Aucune information présente dans les deux sources | P1 |
| CFG-2 | Répartition de la configuration noyau : backend micro-noyau (embOS, FreeRTOS) et architecture dans les manifestes ; systèmes de fichiers, pilotes logiciels et paramètres dimensionnants dans le XML mklepton. | Changement d'option → reconfiguration → construction | P1 |
| CFG-3 | Par greffon : options de compilation (définitions, optimisation, avertissements) avec une portée explicite : privée au greffon, ou publique (visible des greffons qui en dépendent). | `compile_commands.json` montre la portée attendue | P1 |
| CFG-4 | Les options sont typées et documentées dans le manifeste (booléen, entier borné, énumération, chaîne), avec valeur par défaut et champ `description`. Le manifeste de graine peut fixer, par greffon, la valeur d'une option pour tout le projet ; sinon le défaut s'applique. | Valeur hors bornes refusée par `lepton check` et `lepton generate`, et à la configuration CMake | P1 |
| CFG-5 | Aucune génération entre le XML et CMake. Vérification facultative (`lepton check`) : signaler avant l'édition de liens un pilote ou un binaire déclaré dans le XML mais fourni par aucun greffon. | Pilote ou binaire manquant signalé avant l'édition de liens | P2 |
| CFG-6 | Plusieurs configurations par projet (debug, release, cible QEMU, carte réelle) via des presets CMake générés. | `cmake --list-presets` | P1 |
| CFG-7 | Édition de la configuration dans l'éditeur avec complétion et validation : XML mklepton par schéma XSD, manifestes JSON par JSON Schema. | Erreur signalée à la saisie | P2 |
| CFG-8 | Le format XML mklepton est formalisé par un schéma XSD versionné. Inventaire des éléments inutiles (hérités d'IAR, cibles gelées ARM7, ARM9, M16C) à retirer, et des éléments manquants à ajouter. Le XML se limite à la configuration logicielle de Lepton et de son système de fichiers racine : ni cœur, ni architecture matérielle, ni backend. mklepton refuse un XML de version inconnue. Fréquence du cœur et en-tête de configuration noyau de la carte relèvent du manifeste BSP. L'image du système de fichiers racine est dimensionnée automatiquement si sa taille n'est pas imposée. | XML existants validés par le schéma ou migrés | P1 |

### F. Construction

| ID | Exigence | Vérification | Prio. |
| --- | --- | --- | --- |
| BLD-1 | Produire les bibliothèques statiques `kernel` (`kernel/`, `kernel/dev/arch`), `lib`, `sbin`, `bin`, `bsp`, puis l'exécutif lié avec elles : `main` (greffon noyau), table des périphériques et sources générées par mklepton. Démarrage générique (greffon noyau), vecteurs et remplaçants forts (greffon famille), démarrage de la carte (BSP) sont liés comme objets (bibliothèque OBJECT CMake) et non via une archive. | Cibles CMake visibles et nommées ainsi | P1 |
| BLD-2 | Chaque greffon contribue ses sources à la bibliothèque déclarée dans son manifeste, sans modifier les `CMakeLists.txt` du noyau. | Ajout d'un greffon sans toucher au greffon noyau | P1 |
| BLD-3 | `mklepton` s'exécute comme étape de construction et produit l'image du système de fichiers et les sources générées dans le répertoire de construction. | Aucune sortie dans le trunk | P1 |
| BLD-4 | Sorties : ELF, HEX, BIN, MAP, rapport d'occupation mémoire (flash/RAM par bibliothèque). | Fichiers présents ; rapport lisible | P1 |
| BLD-5 | Construction identique en ligne de commande, dans l'éditeur et en CI (mêmes presets). | Même empreinte de binaire | P1 |
| BLD-6 | Ajouter un nouveau cœur ou une nouvelle carte ne demande qu'un greffon BSP et, si besoin, un fichier `arch` : pas de modification du système de construction commun. | Revue lors de l'ajout RISC-V | P2 |

### G. Intégration à l'éditeur

| ID | Exigence | Vérification | Prio. |
| --- | --- | --- | --- |
| IDE-1 | L'architecture logicielle est visible comme sous IAR ou Visual Studio : exécutif → bibliothèques → greffons → répertoires → fichiers. | Vue arborescente dans la barre latérale | P1 |
| IDE-2 | Chaque greffon est éditable avec son propre suivi git dans l'éditeur. | Panneau source control multi-dépôts | P1 |
| IDE-3 | Navigation (définition, références, appels) exacte pour la configuration active, y compris sources générées par mklepton. | Aller à la définition ouvre le bon fichier, une seule fois | P1 |
| IDE-4 | Un même fichier ne s'ouvre jamais sous deux chemins (trunk et clone) ; diagnostics et points d'arrêt sur un chemin canonique. | Point d'arrêt posé via le trunk atteint | P1 |
| IDE-5 | Changer de configuration (cible, debug/release) depuis la barre d'état. | Reconfiguration et réindexation | P1 |
| IDE-6 | Commandes de la palette : créer/ajouter/retirer un greffon, regreffer, état de la graine. | Commandes présentes | P2 |

### H. Exécution et débogage

| ID | Exigence | Vérification | Prio. |
| --- | --- | --- | --- |
| DBG-1 | Lancer l'image sous QEMU depuis l'éditeur, console série dans un terminal intégré. | Invite `lsh` visible | P1 |
| DBG-2 | Déboguer sous QEMU avec GDB (points d'arrêt, pas à pas, registres). | Arrêt sur `main` | P1 |
| DBG-3 | Flasher et déboguer sur carte réelle via OpenOCD (ST-Link, CMSIS-DAP) et J-Link en option ; configuration issue du BSP. | Flash + arrêt sur `main` sur NUCLEO-WL55JC1 (cœur M4, M0+ non utilisé) et NUCLEO-F429ZI | P1 |
| DBG-4 | Vues périphériques (fichier SVD du MCU déclaré par le BSP) et vue des tâches (embOS). | Registres périphériques lisibles | P2 |
| DBG-5 | Déboguer `mklepton` sur l'hôte. | Arrêt dans `mklepton` | P2 |

### I. Tests

| ID | Exigence | Vérification | Prio. |
| --- | --- | --- | --- |
| TST-1 | Lancer le banc KAL QEMU (matrice architecture × backend) depuis l'éditeur et en CI, résultats lisibles dans l'éditeur. | Rapport par case de la matrice | P1 |
| TST-2 | Un greffon peut fournir ses propres tests, découverts sans configuration supplémentaire. | Tests du greffon exécutés | P2 |

## Exigences non fonctionnelles

| ID | Exigence |
| --- | --- |
| NF-1 | Indépendance vis-à-vis de l'éditeur : toute opération (graine, greffon, fichier, configuration, construction, flash) est faisable en ligne de commande. VSCodium n'est qu'une interface. |
| NF-2 | `scion` reste générique : aucune notion Lepton n'y entre. Ce qui est spécifique à Lepton vit dans l'outil `lepton`, client de scion. |
| NF-3 | Hôtes : macOS Intel (MacPorts), Debian x86_64 dès la première version ; macOS Apple Silicon (Homebrew) prévu dès la conception (aucun binaire x86 imposé, aucun préfixe de gestionnaire de paquets codé en dur). |
| NF-4 | Exécution native par défaut (mklepton est 64 bits natif) ; le conteneur Debian reste une option pour la CI, avec montage du rootstock entier. |
| NF-5 | Reproductibilité : versions épinglées des extensions, de scion, de la chaîne ; graine figeable (GRA-5). |
| NF-6 | Lisibilité des scripts : en-tête d'usage, une fonction par étape, messages d'erreur indiquant l'action corrective, code de retour non nul en cas d'échec. |
| NF-7 | Testabilité de l'outillage : l'outil `lepton` a ses tests (`pytest`). |
| NF-8 | Aucun service distant obligatoire : pas de télémétrie, pas de compte, fonctionnement hors ligne une fois les dépôts clonés. |

## Architecture retenue

L'éditeur n'agit jamais directement sur scion ni sur le trunk : tout passe par l'outil `lepton`
(Python, client de scion) ou par CMake.

```
VSCodium ── extensions standard (CMake Tools, clangd, Cortex-Debug, git) ──pilote──► CMake + mklepton ──► build/
   └─ extension Lepton (phase 2) ──appelle──► outil lepton ──délègue──► scion ──► depots/ (clones), trunk/ (liens)
                                              └─ génère presets, .code-workspace, launch.json (depuis les manifestes)
```

Phase 1 (sans extension) : CMake Tools affiche les cibles (exécutif, `kernel`, `lib`, `sbin`,
`bin`, `bsp`) ; un `.code-workspace` multi-racines généré par `lepton` ouvre un dossier par clone de
greffon plus le trunk ; regreffe par tâche `lepton graft`.
Phase 2 (extension) : regreffe automatique, vue exécutif → bibliothèques → greffons → fichiers,
redirection des créations faites dans le trunk, formulaires.

Risques à lever en premier : clangd et liens symboliques (IDE-4) ; sauvegarde VSCodium via un
lien (FIC-5) ; chemins de sources dans l'ELF (`-ffile-prefix-map` ou `substitute-path` de GDB).

## Décisions (2026-10-12)

| # | Question | Décision |
| --- | --- | --- |
| 1 | Chemins `/kernel`, `/lib`, `/bin` du besoin | Arbre actuel conservé ; chemins relatifs à `sys/root/src/`. |
| 2 | BSP dans la bibliothèque `kernel` ? | Bibliothèque `bsp` distincte. La table des périphériques générée par mklepton est placée dans l'exécutif, lié en premier, pour éviter la dépendance croisée kernel ↔ bsp. |
| 3 | `bin` : base + application ? | Une seule `bin` ; binaires de l'image choisis par la configuration mklepton. |
| 4 | Où vit l'exécutif ? | `main` générique et démarrage générique par ISA dans le greffon noyau ; table de vecteurs par MCU et remplaçants forts dans le greffon famille ; initialisation d'horloge dans le BSP ; liaison en OBJECT. (Amendée le 2026-10-13, PA-2 Q2/Q3 ; texte initial : démarrage et vecteurs dans le BSP.) |
| 5 | Source de vérité de la configuration | XML mklepton maître de la configuration logicielle et du système de fichiers racine, indépendant de CMake ; format à faire évoluer (CFG-8). |
| 6 | Graine git obligatoire ? | Oui pour une livraison ; répertoire local toléré en prototypage. |
| 7 | Assembleur | `.S` uniquement. |
| 8 | Évolutions de scion | À vérifier contre scion 0.5 ; génériques (NF-2), sur une branche de `seed.scions`. |
| 9 | Format des manifestes | JSON + JSON Schema. Limite assumée : pas de commentaires, chaque option a un champ `description`. mklepton reste en XML. |
| 10 | Greffon application | Facultatif (GRA-2). |
| 11 | Cartes de validation | QEMU `mps2-an386`, NUCLEO-F429ZI, NUCLEO-WL55JC1 (cœur M4 ; M0+ non utilisé). |
