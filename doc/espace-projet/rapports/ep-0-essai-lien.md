# EP-0 — Essai VSCodium : espace ouvert par un lien du trunk ; plusieurs rootstocks

Session du 2026-11-26, branche `espace-projet/ep-0` de lepton-tools. macOS (Intel), VSCodium
1.135.06055, extension Lepton 0.5.4, scion 0.6.3.4, lepton 0.1.0. Résultats valables pour macOS
seulement.

## 1. Préparation

### Copies
| Copie | Source | Projet | Commande |
| --- | --- | --- | --- |
| `essais/ep-0/a` | `essais/env-9` | `env9` (noyau, famille et BSP qemu-mps2-an386, `project-env9`) | `rsync -a --exclude=/build/ --exclude='/*.log' <src>/ <dst>/` |
| `essais/ep-0/b` | `essais/env-11/qemu` | `env11` (idem + greffon application) | idem |

`-a` copie les liens sans leur cible (équivalent de `cp -RP`, skill `lepton-rootstock`) ; ni
`build/` ni journaux copiés. Dans les deux copies : `lepton check` rc 0 (« 5 fichier(s)
conforme(s) ») ; `lepton generate` rc 0, espace `<copie>/<projet>.code-workspace` écrit, avec
l'avertissement attendu « `build/.active/compile_commands.json` absent ». L'espace régénéré ne
cite aucun chemin de l'original (0 occurrence de `essais/env-9` ou `essais/env-11`) et 36 chemins
de la copie (D45 levé par la régénération).

Relevé incident : un `.DS_Store` régulier est apparu dans `ep-0/a/trunk/sys/root/src/kernel/`
pendant la copie (horodatage de la copie, absent de la source) ; motif toléré
(`.scion.trunk.tolerated`) ; disparu après le `scion graft` du §1.

### Liens de `trunk/sys/user/<projet>/`
scion pose **un lien par fichier** ; `trunk/sys/user/<projet>/` et `etc/` sont des répertoires
réels du trunk. Cible : `depots/lepton-seed/<projet>/project/scion/sys/user/<projet>/…` (dépôt de
la graine, greffon local `project-<projet>`).

```
trunk/sys/user/env9/etc/mkconf_env9.xml -> ../../../../../depots/lepton-seed/env9/project/scion/sys/user/env9/etc/mkconf_env9.xml
```

Le fichier d'espace placé sous `trunk/sys/user/env9/` est à 4 niveaux sous la racine du
rootstock ; sa cible, `depots/lepton-seed/env9/project/scion/sys/user/env9/`, à 8.

### Variantes
Dérivées de `ep-0/a/env9.code-workspace` (généré) par un script de la session, en ne changeant que
`folders[].path` (relatifs à la racine du rootstock dans l'espace généré), plus une tâche
« EP-0 : écho » (`${workspaceFolder:trunk}`, `${workspaceFolder}`, `${workspaceFile}`, `$PWD`) :

| Variante | Préfixe de `folders[].path` | Résout `trunk` depuis le lien | depuis la cible |
| --- | --- | --- | --- |
| `V-lien` | `../../../../` | `ep-0/a/trunk` (existe) | `…/env9/project/trunk` (absent) |
| `V-cible` | `../../../../../../../../` | `/Users/cle_d_anton/trunk` (absent) | `ep-0/a/trunk` (existe) |

Dépôt de `V-lien` : `ep-0/a/depots/lepton-seed/env9/project/scion/sys/user/env9/env9.code-workspace`,
non suivi (`?? project/scion/sys/user/env9/env9.code-workspace`), non ignoré
(`git check-ignore` rc 1). `scion graft` rc 0 (« 6 chemin(s) ignoré(s) par git, non
greffé(s) », « 3060 feuilles liées »). Résultat :

```
trunk/sys/user/env9/env9.code-workspace -> ../../../../depots/lepton-seed/env9/project/scion/sys/user/env9/env9.code-workspace
```

Contrôles : aucun fichier régulier dans le trunk, aucun lien cassé.

## 2. Essai (a) — résolution des chemins

### `V-lien`, ouvert par `codium <ep-0/a>/trunk/sys/user/env9/env9.code-workspace`
Relevés de l'utilisateur, sauf mention contraire :

| Point | Observation |
| --- | --- |
| Explorateur | 5 dossiers, tous résolus et visibles |
| Chemin retenu | titre de la fenêtre et récents : `…/essais/ep-0/a/trunk/sys/user/env9/…` (lien). Relevé de la session : `workspaceStorage/21803a51…/workspace.json` = `file:///Users/cle_d_anton/lepton-tools-dev/essais/ep-0/a/trunk/sys/user/env9/env9.code-workspace` |
| Tâche d'écho | « Exécution de la tâche dans le dossier trunk » ; `workspaceFolder:trunk=…/ep-0/a/trunk`, `workspaceFolder=…/ep-0/a/trunk`, `cwd=…/ep-0/a/trunk` ; `${workspaceFile}` **non développé** par VSCodium (ligne de commande affichée `workspaceFile=${workspaceFile}`, sortie `workspaceFile=` : vidé par le shell) |
| Extension Lepton, « vérifier » | « lepton : vérifier — terminé » ; `lepton seed status --json` et `lepton check --json` lancés dans `…/ep-0/a/trunk/sys/user/env9` (répertoire du lien, non résolu), code 0 ; « Observation de 5 greffon(s) et du trunk …/ep-0/a/trunk » ; surveillance de `…/ep-0/a/build/.active/compile_commands.json` |

### `V-lien`, ouvert par « Fichier > Ouvrir l'espace de travail à partir d'un fichier »
Sélecteur de macOS, navigation jusqu'à `ep-0/a/trunk/sys/user/env9/env9.code-workspace`.

| Point | Observation |
| --- | --- |
| Explorateur | 5 dossiers grisés, vides |
| Chemin retenu | récents : `…/essais/ep-0/a/depots/lepton-seed/env9/project/scion/sys/user/env9/env9` (cible). Relevé de la session : second état, `workspaceStorage/7a602e53…/workspace.json` = `file:///Users/cle_d_anton/lepton-tools-dev/essais/ep-0/a/depots/lepton-seed/env9/project/scion/sys/user/env9/env9.code-workspace` (16:07), distinct de `21803a51…` (chemin du lien, 15:51) |
| Tâche d'écho | `workspaceFolder:trunk=…/ep-0/a/depots/lepton-seed/env9/project/trunk` (absent), `workspaceFolder` idem, `cwd` idem ; `${workspaceFile}` non développé |
| Extension Lepton, « vérifier » | `lepton seed status --json` et `lepton check --json` lancés dans `…/ep-0/a/depots/lepton-seed/env9/project/scion/sys/user/env9` (cible), code 0 ; « Observation de 5 greffon(s) et du trunk …/ep-0/a/trunk » : `lepton` remonte au rootstock depuis la cible aussi (le clone est sous `<rootstock>/depots/`) |

Le sélecteur de fichiers de macOS résout le lien : VSCodium reçoit le chemin de la cible, le garde
comme identité de l'espace (état distinct) et résout les `folders` depuis la cible.

### `V-lien`, autres modes d'ouverture

| Mode | Explorateur | Chemin retenu (récents) |
| --- | --- | --- |
| Double-clic dans le Finder sur `ep-0/a/trunk/sys/user/env9/env9.code-workspace` | 5 dossiers grisés | cible (`…/depots/lepton-seed/env9/project/scion/sys/user/env9/env9`) |
| « Fichier > Ouvrir récent », entrée du chemin du lien | 5 dossiers résolus | lien |

Le Finder résout le lien comme le sélecteur. Seuls `codium <chemin du lien>` et l'entrée récente
créée par lui gardent le chemin du lien.

### `V-cible` (même lien du trunk ; fichier du clone remplacé, fenêtre fermée avant)
Avant remplacement : fichier du clone identique à `V-lien` (aucune écriture de VSCodium).

| Mode | Explorateur | Chemin retenu (récents) | Tâche d'écho | « vérifier » |
| --- | --- | --- | --- | --- |
| `codium <ep-0/a>/trunk/sys/user/env9/env9.code-workspace` | 5 dossiers grisés | lien | — | — |
| Double-clic dans le Finder sur le même chemin | 5 dossiers résolus | cible | `workspaceFolder:trunk=…/ep-0/a/trunk`, `workspaceFolder=…/ep-0/a/trunk`, `cwd=…/ep-0/a/trunk` ; `${workspaceFile}` non développé | `lepton seed status --json`, `lepton check --json` dans `…/project/scion/sys/user/env9` (cible), code 0, trunk `…/ep-0/a/trunk` |

### Réponse à (a)
Les chemins relatifs de `folders` sont résolus **depuis le chemin par lequel l'espace a été
ouvert**, tel que VSCodium le reçoit, sans résolution du lien par VSCodium lui-même :
- `codium <chemin du lien>` (et l'entrée récente qu'il crée) : depuis le lien
  (`trunk/sys/user/<projet>/`, 4 niveaux) ;
- Finder (double-clic) et « Ouvrir l'espace de travail à partir d'un fichier » : macOS résout le
  lien avant de passer le chemin ; depuis la cible (8 niveaux ici).

Aucune des deux variantes ne s'ouvre correctement par tous les modes. Chaque mode crée son propre
état VSCodium (`workspaceStorage` distinct par chemin). L'extension Lepton trouve le rootstock
dans les deux cas (`lepton` remonte depuis le lien comme depuis la cible, celle-ci étant sous
`<rootstock>/depots/`). Une fois les dossiers résolus, `${workspaceFolder:trunk}` désigne
`<rootstock>/trunk` quel que soit le mode.

Conclusion partielle : ouvert par le chemin du lien, VSCodium résout les `folders` relatifs depuis
le répertoire du lien, garde ce chemin comme identité de l'espace, et l'extension remonte au bon
rootstock depuis ce répertoire.

## 3. Essai (c) — variables dans les réglages

Fenêtre de `V-cible` ouverte par le Finder (dossiers résolus). Variantes successives écrites dans
le fichier du clone (scripts de la session `variante_c.py` et remplacements ciblés), fenêtre
rechargée entre deux. Écart à la consigne de l'étape (« un chemin absolu à la fois ») : un
remplacement **par consommateur** (clangd, CMake Tools, JSON, XML, Cortex-Debug, launch, tasks),
chaque extension ne lisant que ses réglages. Schémas copiés dans `ep-0/a/schemas-ep0/` (hors
trunk). Valeurs « de poste » posées pour l'essai dans les réglages de l'espace :
`lepton.ep0.chaine` (chaîne ARM), `lepton.ep0.gdb` (clés non déclarées par l'extension).
`ep-0/a/build/.active/` créé vide avant l'essai de `V-c2`.

| Réglage | Forme | Variante | Résultat | Preuve |
| --- | --- | --- | --- | --- |
| tâche, `args` | `${workspaceFolder:trunk}` | V-c | développé | `workspaceFolder:trunk=…/ep-0/a/trunk` |
| tâche, `args` | `${config:cmake.copyCompileCommands}` (clé déclarée, valeur contenant `${workspaceFolder:trunk}`) | V-c | développé, variable imbriquée comprise | `cfgDeclaree=…/ep-0/a/trunk/../build/.active/compile_commands.json` |
| tâche, `args` | `${config:lepton.ep0.chaine}` (clé non déclarée) | V-c | développé | `cfgNonDeclaree=/Users/cle_d_anton/opt/arm-gnu-toolchain-14.2.rel1-…/bin` |
| tâche, `args` | `${input:ep0Choix}` (`pickString`) | V-c | développé | choix proposé, `input=valeur-a` |
| tâche, `options.cwd` | `${workspaceFolder:trunk}/..` | V-c | développé | « Exécution de la tâche dans le dossier .. » ; `cwd=…/ep-0/a` |
| tâche `lepton : vérifier`, `options.cwd` | `${workspaceFolder:trunk}/..` | V-c | accepté, non discriminant (la commande porte `-C <absolu>`) | `lepton check -C …/ep-0/a` : « 5 fichier(s) conforme(s) » |
| `tasks` | `${workspaceFile}` | V-lien, V-cible | **non développé** | `workspaceFile=${workspaceFile}` sur la ligne de commande |
| `clangd.arguments`, `--compile-commands-dir` | `${workspaceFolder:trunk}/../build/.active` | V-c | **non développé** | `argv[1]: --compile-commands-dir=${workspaceFolder:trunk}/../build/.active` ; `E … Path specified by --compile-commands-dir does not exist. The argument will be ignored.` |
| `clangd.arguments`, `--compile-commands-dir` | `${workspaceFolder}/../build/.active` | V-c2, V-c3 | développé (premier dossier de l'espace, `trunk`) | `argv[1]: --compile-commands-dir=…/ep-0/a/trunk/../build/.active` |
| `clangd.arguments`, `--query-driver` | `${config:lepton.ep0.chaine}/arm-none-eabi-gcc` | V-c à V-c3 | développé | `argv[3]: --query-driver=/Users/cle_d_anton/opt/arm-gnu-toolchain-14.2.rel1-…/bin/arm-none-eabi-gcc` |
| `json.schemas[].url` | `${workspaceFolder:trunk}/../schemas-ep0/…` | V-c | **non développé** | aucune info-bulle sur `"nom"` de `trunk/…/bsp/qemu-mps2-an386/lepton-greffon.json` |
| `json.schemas[].url` | témoin : `file://…/ep-0/a/schemas-ep0/…` (absolu) | V-c3 | fonctionne | info-bulle « Nom du greffon, unique dans une graine … » |
| `xml.fileAssociations[].systemId` | `${workspaceFolder:trunk}/../schemas-ep0/mklepton.xsd` | V-c | **non développé** | info-bulle « Cannot find the declaration of element … » (aucune grammaire) sur `trunk/sys/user/env9/etc/mkconf_env9.xml` |
| `xml.fileAssociations[].systemId` | témoin : `…/ep-0/a/schemas-ep0/mklepton.xsd` (absolu) | V-c3 | fonctionne | info-bulle sur `mklepton` : « Racine … attribut version obligatoire … » |

| `json.schemas[].url` | `${workspaceFolder}/../schemas-ep0/…` | V-c4 | **non développé** | aucune info-bulle |
| `json.schemas[].url` | relatif sans variable `../schemas-ep0/…` (juste depuis `trunk`) | V-c5 | **non résolu** depuis le premier dossier | aucune info-bulle |
| `json.schemas[].url` | relatif depuis le fichier d'espace | — | non essayé : dépendrait du mode d'ouverture (§2) | — |
| `xml.fileAssociations[].systemId` | `${workspaceFolder}/../schemas-ep0/mklepton.xsd` | V-c4 | développé | info-bulle de documentation sur `mklepton` |
| `cmake.copyCompileCommands` | `${workspaceFolder:trunk}/../build/.active/compile_commands.json` | V-c5 | développé | après « CMake: Configure » (preset `env9-debug-qemu`) : `ep-0/a/build/.active/compile_commands.json` créé (459 581 octets, 17:15), taille de `build/env9-debug-qemu/compile_commands.json` ; aucun chemin littéral `${workspaceFolder…}` créé |
| `cortex-debug.gdbPath` (réglage ; `gdbPath` retiré du lancement) | `${config:lepton.ep0.gdb}` | V-c5 | développé | `Launching GDB: /opt/local/bin/arm-none-eabi-gdb -q --interpreter=mi2` |
| `cortex-debug.armToolchainPath` | `${config:lepton.ep0.chaine}` | V-c5 | développé | `Reading symbols from /Users/cle_d_anton/opt/arm-gnu-toolchain-14.2.rel1-…/bin/arm-none-eabi-objdump …`, `…-nm …` |
| `launch`, `executable` | `${workspaceFolder:trunk}/../build/env9-debug-qemu/lepton.elf` | V-c5 | développé | `-kernel /Users/cle_d_anton/lepton-tools-dev/essais/ep-0/a/build/env9-debug-qemu/lepton.elf` ; arrêt dans `main` |
| `launch`, `gdbPath` et `executable` | `${config:lepton.ep0.gdb}`, `${input:ep0Elf}` (`pickString`, option `${workspaceFolder:trunk}/…`) | V-c6 | développés | liste « EP-0 : ELF à déboguer » proposée ; arrêt dans `main` |
| `launch`, `name` | `… (${config:} et ${input:})` (texte de la session) | V-c5 | développé lui aussi : boîte « impossible de résoudre la variable ${config:} » au lancement ; nom corrigé en V-c6 | relevé de l'utilisateur |
| `cortex-debug.openocdPath` | — | — | non essayé : absent de l'espace (BSP QEMU seulement) ; à reprendre en EP-5 | — |

Construction pour le lot 2 : `mklepton` hôte construit par la session dans la copie
(`cmake -S <ep-0/a>/trunk -B <ep-0/a>/build/host --preset host`, puis `--target mklepton`, rc 0) ;
preset `env9-debug-qemu` configuré et construit par CMake Tools (code 0). Port gdb de QEMU choisi
par Cortex-Debug : `tcp::50000`.

### Réponse à (c)
- **Tâches et `launch`** (résolus par VSCodium lui-même) : `${workspaceFolder:trunk}`,
  `${config:<clé>}` (clé déclarée ou non, variable imbriquée dans la valeur comprise) et
  `${input:<id>}` sont développés, dans tous les champs texte (nom compris) ;
  `${workspaceFile}` ne l'est pas.
- **Réglages** (résolus par chaque extension) : selon l'extension.
  - CMake Tools 1.24.42 : `${workspaceFolder:trunk}` développé (`cmake.copyCompileCommands`,
    seul réglage essayé).
  - Cortex-Debug 1.13.0-pre6 : `${config:}` développé (`gdbPath`, `armToolchainPath`) ;
    `${workspaceFolder:trunk}` non essayé dans ses réglages (seulement dans `launch`, résolu par
    VSCodium).
  - clangd 0.6.0 : `${workspaceFolder}` et `${config:}` développés, **`${workspaceFolder:trunk}`
    non** ; `${workspaceFolder}` vaut le premier dossier (`trunk`, PA-1).
  - vscode-xml 0.29.3 : `${workspaceFolder}` développé, `${workspaceFolder:trunk}` non.
  - JSON (VSCodium 1.135) : aucune des formes essayées (`${workspaceFolder:trunk}`,
    `${workspaceFolder}`, relatif) ; seul le chemin absolu fonctionne.
- La proposition de `CADRAGE.md` §6 (« `${workspaceFolder:trunk}/..` accepté par clangd, CMake
  Tools, `launch`, `tasks` ») est donc fausse pour clangd, vraie pour les trois autres.
  `${workspaceFolder}` (sans nom) : développé dans les tâches, clangd et vscode-xml ; non essayé
  dans CMake Tools, Cortex-Debug et `launch` ; inopérant dans `json.schemas`. Aucune forme unique
  n'a été prouvée pour tous les réglages.

## 4. Essai (b) — écriture par l'interface

`V-lien` réinstallé dans le clone (`cp`, écriture sur place) ; fenêtre ouverte par
`codium <ep-0/a>/trunk/sys/user/env9/env9.code-workspace` (chemin du lien), 5 dossiers résolus.

| Moment | Lien du trunk | Fichier du clone | `git status --short` (graine) | `lepton check` | Trunk |
| --- | --- | --- | --- | --- | --- |
| Départ | inode 391822316, `-> ../../../../depots/lepton-seed/env9/project/scion/sys/user/env9/env9.code-workspace` | inode 391818639, 16 447 o, sha256 `eb457455…` | `?? project/scion/sys/user/env9/env9.code-workspace` | rc 0, « 5 fichier(s) conforme(s) » | aucun fichier régulier (hors `.DS_Store` tolérés) |
| Geste 1 : « Préférences : ouvrir les paramètres de l'espace de travail » (interface), onglet Espace de travail, `editor.tabSize` = 3 | inchangé (même inode, même cible) | même inode, 16 472 o, sha256 `7c4929ef…` ; `"editor.tabSize": 3` ajouté ; commentaire de tête conservé | inchangé | rc 0 | inchangé |
| Geste 2 : « Fichier > Ajouter un dossier à l'espace de travail », `ep-0/a/schemas-ep0` | inchangé | même inode, 16 525 o, sha256 `5532c2f2…` ; entrée `"path": "../../../../schemas-ep0"` ajoutée | inchangé | rc 0 | inchangé, aucun lien cassé |

Redirection FIC-3 de l'extension : aucune notification signalée par l'utilisateur (aucun fichier
créé dans le trunk). Mode Finder (chemin de la cible) : non essayé ; VSCodium y écrit directement
le fichier du clone, et un dossier ajouté y serait inscrit relativement à la cible (§2).

### Réponse à (b)
Ouvert par le chemin du lien, VSCodium écrit **à travers le lien**, sur place (même inode, ni
fichier temporaire ni renommage) : le lien du trunk est conservé, aucun fichier étranger n'apparaît,
`lepton check` reste à 0. Les commentaires (`//`) sont conservés. Un dossier ajouté par
l'interface est inscrit en chemin relatif **depuis le chemin d'ouverture** (ici le lien). Le
fichier modifié est celui du clone : il devient une modification non commitée du greffon (ici
fichier non suivi).

## 5. Constat du besoin 2 — deux rootstocks, deux fenêtres

Espaces générés actuels (fichiers réguliers à la racine, régénérés au §1) :
`codium <ep-0/a>/env9.code-workspace` et `codium <ep-0/b>/env11.code-workspace`, ouverts en même
temps. `mklepton` hôte de `ep-0/b` construit par la session (rc 0). Aucun des deux espaces ne cite
l'autre copie (0 occurrence croisée).

| Point | `ep-0/a` (env9) | `ep-0/b` (env11) |
| --- | --- | --- |
| Extension Lepton, « vérifier » | `lepton seed status`, `seed tree`, `check` dans `…/ep-0/a`, code 0 ; trunk `…/ep-0/a/trunk` | `lepton seed status`, `check` dans `…/ep-0/b`, code 0 ; trunk `…/ep-0/b/trunk` |
| CMake Tools | Build (preset `env9-debug-qemu`, configuré au §3) : code 0 | Configure + Build `env11-debug-qemu` : code 0 |
| `build/.active/compile_commands.json` (session) | 459 581 o, 18:13, `directory` = `…/ep-0/a/build/env9-debug-qemu` | 459 929 o, 18:16, `directory` = `…/ep-0/b/build/env11-debug-qemu` |
| clangd | `argv[1]: --compile-commands-dir=…/ep-0/a/build/.active` ; « Loaded compilation database from …/ep-0/a/build/.active/compile_commands.json » ; processus 46796 | idem pour `…/ep-0/b/…` ; processus 46866 |
| Débogage QEMU simultané | arrêt dans `main` ; `qemu-system-arm … -gdb "tcp::50000" -S -kernel …/ep-0/a/build/env9-debug-qemu/lepton.elf` | arrêt dans `main` ; `… -gdb "tcp::50001" … -kernel …/ep-0/b/build/env11-debug-qemu/lepton.elf` |
| Processus (session, `ps`, `lsof`) | QEMU 47043, `TCP *:50000 (LISTEN)` | QEMU 47257, `TCP *:50001 (LISTEN)` |

Ressources partagées :
- `lepton` : un seul installé (`~/.local/bin/lepton`), sans état propre à un rootstock (il
  remonte depuis son répertoire de travail) ;
- `LEPTON_EMBOS_ROOT` : non utilisée ici (deux projets FreeRTOS) ; une valeur globale vaudrait pour
  tous les rootstocks (constat du cadrage, non rejoué avec embOS) ;
- réglages utilisateur de VSCodium (`~/Library/Application Support/VSCodium/User/settings.json`) :
  aucun réglage propre à un rootstock (confiance, démarrage, mises à jour, télémétrie, lemminx
  binaire, format naturel de Cortex-Debug) ;
- ports gdb de QEMU : alloués par Cortex-Debug (50000, puis 50001), sans conflit.

### Réponse au besoin 2
Constaté : deux rootstocks, chacun dans sa fenêtre, travaillent sans interférence (extension,
CMake Tools, clangd, deux débogages QEMU simultanés). Aucun défaut. Relevé incident, hors besoin 2 :
QEMU lancé par Cortex-Debug écoute sur toutes les interfaces (`*:50000`).

## 6. Synthèse pour le PA-E1

### Faits
1. **(a)** Les `folders` relatifs sont résolus depuis le chemin d'ouverture tel que VSCodium le
   reçoit. `codium <lien>` et l'entrée récente qu'il crée : depuis le lien. Finder (double-clic) et
   « Ouvrir l'espace de travail à partir d'un fichier » : macOS résout le lien, VSCodium reçoit la
   cible. Un même fichier d'espace placé derrière un lien du trunk n'est donc juste que pour un
   des deux groupes de modes ; chaque chemin a son propre état VSCodium. L'extension Lepton trouve
   le rootstock dans les deux cas.
2. **(b)** Ouvert par le lien, VSCodium écrit à travers le lien, sur place (inode conservé) ; le
   lien reste, `lepton check` reste à 0. Un dossier ajouté est inscrit relativement au chemin
   d'ouverture. Toute modification par l'interface change le fichier du clone du greffon (fichier
   versionné ou non selon T2).
3. **(c)** Développement des variables inégal selon le consommateur (tableau du §3) :
   `${workspaceFolder:trunk}` refusé par clangd et vscode-xml ; `${workspaceFolder}` (= `trunk`,
   premier dossier) accepté par clangd et vscode-xml ; `json.schemas` n'accepte aucune forme
   essayée (absolu seulement) ; `${config:}` accepté partout où il a été essayé (tâches, `launch`,
   clangd, Cortex-Debug) ; `${input:}` dans tâches et `launch` ; `${workspaceFile}` jamais. La
   phrase de `CADRAGE.md` §6 sur `${workspaceFolder:trunk}/..` est fausse pour clangd.
4. **Besoin 2** : constaté, aucun défaut.

### Questions du PA-E1 (à trancher par l'utilisateur)
- C2 (espace à `trunk/sys/user/<projet>/<nom>.code-workspace`, derrière un lien) et C3 (un seul
  espace) : maintenues ou révisées, au vu du fait 1.
- Effets sur EP-1, EP-2, EP-4 (le fait 3 touche EP-4 : `json.schemas`, clangd ; le fait 2 touche
  T2).
- Essais (a) et (b) refaits sur la VM Debian avant EP-4, ou preuve Debian laissée à EP-8.
- Suite du relevé incident du besoin 2 (QEMU sur toutes les interfaces) : hors plan, ou rien.
- Sort de `essais/ep-0/`.

### Pistes relevées par la session (propositions non validées)
- (P-a) Espace régulier hors du trunk, à la racine du rootstock (état actuel, D2 d'ENV-9),
  généré depuis le contenu versionné du greffon projet : `folders` relatifs à la racine, justes
  par tous les modes d'ouverture ; revient à réviser C2.
- (P-b) Espace derrière le lien (C2) avec `folders` calculés depuis le lien, et ouverture
  canalisée par `codium <lien>`, une commande de l'extension ou les récents ; le double-clic du
  Finder et le menu d'ouverture restent faux.
- (P-c) Espace derrière le lien avec `folders` calculés depuis la cible : juste par le Finder et
  le menu, faux par `codium <lien>` ; profondeur de la cible propre au dépôt du greffon projet.
- `json.schemas` : chemin absolu écrit par `generate` (valeur de poste), ou schémas désignés
  autrement (`$schema` dans les fichiers, association par l'extension) ; à instruire en EP-4.
