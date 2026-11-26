# Étape EP-4 — `lepton generate` portable et fichier de poste

## Contexte
Besoin 1 (`CADRAGE.md` §3) : un espace régénéré ou copié reste valable sur un autre poste, après
réinstallation de lepton, après changement de chaîne. Architecture à trois couches (§4) : graine
et greffon projet = projet (versionnés) ; fichier de poste = machine (non versionné) ; espace de
travail = projection des deux, en chemins relatifs, régénérée sans effet de bord.

Décisions : C2 **révisée au PA-E1** (`STATUS.md` §Décisions) : l'espace reste un fichier régulier
à la racine du rootstock, non versionné, généré depuis le contenu versionné du greffon projet ; il
n'est pas placé derrière un lien du trunk. C3 (un seul espace par projet, plus un fichier de
poste). C5 (fichier de poste dans le greffon projet, ignoré par git, greffé par l'évolution
d'EP-2, créé par lepton, lu par `generate`). C8 (régime de graine de référence conservé ; sa
branche « espace dans le greffon projet » est sans objet depuis le PA-E1 : l'espace est à la racine
dans les deux régimes).

Faits d'EP-0 (`rapports/ep-0-essai-lien.md` §3, tableau), en entrée de la conception ; tout ce
qui n'y figure pas est non essayé :
- `${workspaceFolder:trunk}` : développé dans `tasks` et `launch` (résolus par VSCodium) et dans
  `cmake.copyCompileCommands` ; **non** développé par clangd 0.6.0 (`clangd.arguments`), par
  vscode-xml 0.29.3 (`xml.fileAssociations`) ni dans `json.schemas` ; non essayé dans les réglages
  `cortex-debug.*` ;
- `${workspaceFolder}` (premier dossier, `trunk`) : développé dans les tâches, par clangd et par
  vscode-xml ; non développé dans `json.schemas` ; non essayé dans CMake Tools, Cortex-Debug,
  `launch` ;
- `json.schemas` : seul le chemin absolu fonctionne parmi les formes essayées
  (`${workspaceFolder:trunk}`, `${workspaceFolder}`, relatif depuis `trunk`) ; relatif depuis le
  fichier d'espace non essayé (écarté en EP-0 parce qu'il dépendait du mode d'ouverture, motif
  levé avec un espace régulier à la racine) ;
- `${config:<clé>}` : développé dans les tâches, `launch`, `clangd.arguments`,
  `cortex-debug.gdbPath` et `cortex-debug.armToolchainPath` (clé déclarée ou non, variable
  imbriquée dans la valeur comprise) ; valeurs posées dans les réglages **de l'espace** ; lecture
  depuis les réglages utilisateur de VSCodium non essayée (ils sont communs à tous les rootstocks :
  voir T1) ;
- `${input:<id>}` : développé dans `tasks` et `launch` ; non essayé dans les réglages ;
- `${workspaceFile}` : non développé dans les tâches (seul endroit essayé) ;
- `launch` : variables développées dans `executable`, `gdbPath` et `name` (un `${config:}` sans
  clé dans `name` bloque le lancement) ;
- `cortex-debug.openocdPath` : non essayé (BSP QEMU) ; renvoyé à EP-5.

Existant (`CADRAGE.md` §2.1) : espace écrit à `<rootstock>/<projet>.code-workspace` (chemin codé
en dur) ; chemins absolus partout, y compris vers le venv pipx pour les schémas ; outils hôtes
résolus par le PATH à la génération et figés ; une copie du rootstock garde les chemins de
l'original (D45).

Les directions de `CADRAGE.md` §6 « Portabilité » sont des propositions. Débogage et sondes ne
sont pas de cette étape (EP-5, EP-6) : `launch` garde ses serveurs actuels et
`lepton.probeSerial` son sens. Archétype : infrastructure.

## Prérequis
- EP-0 (rapport `rapports/ep-0-essai-lien.md`, décision PA-E1), EP-1, EP-2 (scion publié avec la
  déclaration des ignorés greffables), EP-3 (greffon `lepton-basic` greffé dans `<ROOTSTOCK>`).
- Versions : `STATUS.md` §Versions.
- Skills `lepton-rootstock`, `lepton-oracle`, `lepton-cibles`.
- Branche `espace-projet/ep-4` de lepton-tools ; greffon projet d'essai en `file://` ; branche
  du greffon `lepton-original-tree-project` (règle d'ignorance git, déclaration scion) selon le
  PA-E8.

## Tâches

### 1. Audit et conception (lecture seule) → PA-E8
Rapport `doc/espace-projet/rapports/ep-4-generation.md`.

Relever, dans `lepton/generate.py` (`render_workspace`, `prime_active`, `write_api_queries`,
`touch_link`) et dans `CMakeUserPresets.json` : chaque chemin absolu et chaque valeur propre au
poste, avec le réglage qui les porte. Les classer : projet (versionné), poste, dérivé.

Proposer, sans rien modifier, d'après les résultats d'EP-0 :
- pour chaque valeur, le mécanisme : chemin relatif à l'espace, `${workspaceFolder:trunk}`,
  `${config:lepton.…}`, `${input:…}` servi par l'extension, valeur écrite à la génération depuis
  le fichier de poste ; schémas JSON et XML pointés ailleurs que dans le venv ;
- fichier de poste : nom, format, schéma, emplacement dans le greffon projet, règle d'ignorance
  git et déclaration scion (EP-2), commande de création, lecture par `generate`, comportement
  quand il manque ; contenu limité ici à la chaîne et aux outils hôtes ;
- T1 : portée du fichier de poste (rootstock et projet, ou machine) ;
- contenu d'équipe (C2 révisée) : ce que le greffon projet fournit, versionné, pour que
  `generate` le projette dans l'espace — rien au-delà de ce qu'il porte déjà (manifeste, XML,
  presets), ou une couche propre (réglages, préférences de débogage, tâches propres au projet ;
  recouvrement avec EP-5 à dire) avec sa forme, son emplacement dans le greffon et sa règle de
  fusion avec le contenu généré ; cas sans greffon projet greffé ; sort d'une retouche faite par
  l'interface dans l'espace (écrasée par `generate`, état actuel « ne pas éditer », ou conservée) ;
- T11 (reformulée au PA-E1) : source des valeurs de poste quand aucun greffon projet n'est
  greffé, C5 écartant le fichier de poste à la racine ;
- nom de l'espace à la racine (graine de projet et régime de référence, C8) ; sort de l'espace
  actuel `<rootstock>/<projet>.code-workspace` des rootstocks existants si son nom ou son contenu
  change (laissé, signalé, supprimé) ;
- maintien de `trunk` en premier dossier et seul chemin d'ouverture (PA-1) ;
- ce que l'extension doit changer (commandes `inputs` ; `runner.ts` `cwd()` inchangé, l'espace
  restant à la racine, sauf effet du PA-E8) ; versions de lepton et de l'extension :
  `<À CONFIRMER au PA-E8>`.

**PA-E8** : l'utilisateur valide. Aucune modification avant la réponse.

### 2. Implémentation (lepton-tools)
Tests d'abord, qui échouent sur `main`. Commits séparés : schéma et création du fichier de
poste ; lecture par `generate` ; contenu d'équipe du greffon projet ; chemins relatifs et
variables ; `build/.active`. L'extension, si le PA-E8 la touche : commit et version à part.

### 3. Essais (skills `lepton-rootstock`, `lepton-cibles`)
Sur un rootstock d'essai à graine de projet et sur une copie de `<ROOTSTOCK>`, sous
`~/lepton-tools-dev/essais/ep-4/` :
- **régénération** : deux `lepton generate` de suite donnent des fichiers identiques octet pour
  octet ; `git status --short` du greffon projet ne montre aucun fichier versionné modifié ;
- **copie** : rootstock copié sans `build/` à un autre chemin, ouvert sans régénérer : clangd,
  configuration et
  construction CMake Tools, débogage QEMU fonctionnent ; l'espace de la copie ne contient aucune
  occurrence du chemin de l'original ;
- **réinstallation de lepton** (`pipx install --force`) : l'espace reste valable sans
  régénération ;
- **changement de chaîne** : fichier de poste modifié, `generate` : aucun fichier versionné ne
  change ;
- **référence** : avec et sans greffon projet greffé, l'espace est à la racine du rootstock, et
  les valeurs de poste viennent de la source retenue pour T11 ;
- **contenu d'équipe** (si le PA-E8 en retient un) : modifié dans le greffon projet, puis
  `generate` : la modification paraît dans l'espace, et dans celui d'une copie régénérée ; cas
  sans greffon projet greffé conforme au PA-E8 ;
- **VSCodium, par l'utilisateur** : ouverture de l'espace par `codium <espace>`, par double-clic
  dans le Finder et par « Fichier > Ouvrir l'espace de travail à partir d'un fichier » (dossiers
  résolus dans les trois cas) ; modification d'un réglage d'espace par l'interface puis
  `lepton generate` : comportement retenu au PA-E8.
- `lepton check` code 0 après chaque `generate`. Binaires : pas d'oracle si les presets générés
  sont identiques (raisonnement consigné) ; sinon oracle avant et après.

### 4. Clôture → PA-E9
**PA-E9** : rapport ; sort des essais ; D45 du hors-plan d'ENV levé ou non ; fusion et
publication (PA-P), greffon projet compris si le PA-E8 le touche ; réinstallation de lepton et
de l'extension sur le Mac.

## Critères de validation
- [ ] PA-E8 et PA-E9 tranchés et consignés.
- [ ] L'espace généré ne contient aucun chemin absolu, hors exceptions listées et acceptées au
      PA-E8 ; contrôle par un test de `pytest`.
- [ ] Aucune valeur de poste dans un fichier versionné du greffon projet ou de la graine.
- [ ] Deux générations successives : fichiers identiques.
- [ ] Essais « copie », « réinstallation », « changement de chaîne », « référence », « contenu
      d'équipe » (s'il y a lieu) et VSCodium conformes.
- [ ] `lepton check` code 0 : le fichier de poste n'est pas un fichier étranger du trunk.
- [ ] `pytest` vert ; `scripts/valider-schemas.sh` vert (schéma du fichier de poste).

## Pièges connus
- CMake Tools ne voit pas une réécriture à travers un lien (L6-5) : garder `touch_link` ou son
  équivalent.
- Un fichier créé après la greffe ne paraît dans le trunk qu'après une regreffe : la commande de
  création du fichier de poste en tient compte (comportement relevé en EP-2).
- Copier un rootstock copie aussi son fichier de poste (T1).
- `json.validate.enable: false` est posé aujourd'hui : ne pas le changer sans le dire au PA-E8.
- Un `build/` copié garde le cache CMake et le `build/.active/compile_commands.json` aux chemins
  de l'original : l'essai « copie » se fait sans `build/`.
- État gardé par VSCodium pour un chemin d'espace : un état par chemin d'ouverture
  (`workspaceStorage/<empreinte>/workspace.json`, relevé d'EP-0) ; un espace renommé ou déplacé
  peut le perdre (déduit, non essayé).
- Une retouche par l'interface (réglage, dossier ajouté) est écrite dans le fichier d'espace, sur
  place, commentaires conservés ; un dossier ajouté y est inscrit relativement au chemin
  d'ouverture (EP-0, essai b, ouverture par le lien ; fichier régulier non essayé) : le PA-E8 dit
  ce que `generate` en fait.
- Les chemins des outils diffèrent sur Debian (`clangd-19`, `gdb-multiarch`) : preuve en EP-8.

## À la fin de l'étape
`STATUS.md` : statut, branche, §Emplacements (espace, fichier de poste), §Versions, décisions
PA-E8 et PA-E9, journal. `HORS-PLAN.md` : tout point écarté. Passation `handoff/ep-4.md`.
