# Étape EP-0 — Essai VSCodium : espace ouvert par un lien du trunk ; plusieurs rootstocks

## Contexte
C2 place l'espace de travail à `trunk/sys/user/<projet>/<nom>.code-workspace`, fourni par le
greffon projet : dans le trunk, ce fichier est un lien symbolique vers un clone. Aujourd'hui
l'espace est un fichier régulier à la racine du rootstock (`<rootstock>/<projet>.code-workspace`,
D2 d'ENV-9). Deux comportements de VSCodium décident si C2 tient (`CADRAGE.md` §6) :
- (a) les chemins relatifs de `folders` d'un espace ouvert par un lien sont-ils résolus depuis le
  lien ou depuis sa cible dans le clone ;
- (b) une modification de réglage « espace de travail » depuis l'interface écrit-elle à travers
  le lien, ou remplace-t-elle le lien par un fichier régulier (fichier étranger du trunk).

L'étape répond par l'essai, avant qu'EP-1, EP-2 et EP-4 ne s'appuient sur C2. Elle constate aussi
le besoin 2 (`CADRAGE.md` §3 : plusieurs rootstocks, chacun dans sa fenêtre, « déjà le cas »).
Archétype : infrastructure, levée de risque. **Aucun code n'est modifié** : ni lepton-tools (hors
`doc/espace-projet/`), ni seed.scions, ni greffon publié, ni `<ROOTSTOCK>`.

## Prérequis
- PA-E0 clos : plan commité et fusionné dans `main`.
- Versions de départ : `STATUS.md` §Versions ; VSCodium et extensions épinglées :
  `doc/devenv/DEVENV-STATUS.md` §Versions épinglées (lignes VSCodium, Extensions VSCodium,
  Extension Lepton).
- Un rootstock d'essai existant à graine de projet, à choisir au plan de session parmi
  `~/lepton-tools-dev/essais/env-9` et `~/lepton-tools-dev/essais/env-11/qemu` (état à relever).
- Skill `lepton-rootstock` (copie d'essai, regreffe) ; `scripts/supprimer-essai.sh`.
- Branche `espace-projet/ep-0` de lepton-tools, depuis `main` (rapport seulement).
- L'utilisateur manipule VSCodium ; la session prépare les fichiers et relève les résultats.

## Tâches

### 1. Préparation
- Copier le rootstock choisi, **sans son `build/`**, sous `~/lepton-tools-dev/essais/ep-0/a`
  (skill `lepton-rootstock`), puis y lancer `lepton check` et `lepton generate` : une copie garde
  les chemins de l'original (D45). Relever les codes de retour.
- Relever, dans la copie, où se trouve la cible des liens de `trunk/sys/user/<projet>/` (dépôt de
  la graine, `project/scion/…`) et si scion y pose un lien par fichier ou par répertoire.
- Préparer deux variantes de l'espace généré, en ne changeant que `folders[].path` :
  - `V-lien` : chemins relatifs calculés depuis `trunk/sys/user/<projet>/` ;
  - `V-cible` : chemins relatifs calculés depuis l'emplacement réel du fichier dans le clone.
- Déposer la variante à essayer dans le clone, à l'emplacement qui se greffe sous
  `trunk/sys/user/<projet>/` (fichier non suivi et non ignoré : il est greffé, filtre E1), puis
  `scion graft`. Vérifier par `ls -l` que le trunk porte un lien. La session n'écrit jamais dans
  un trunk.
- Rapport : `doc/espace-projet/rapports/ep-0-essai-lien.md`. Pour chaque essai : manipulation,
  observation, preuve (`ls -l`, contenu du fichier, sortie de commande).

### 2. Essai (a) — résolution des chemins
Pour `V-lien` puis `V-cible`, l'utilisateur ouvre l'espace **par le chemin du trunk**
(`codium <essai>/trunk/sys/user/<projet>/<nom>.code-workspace`, puis par « Fichier > Ouvrir
l'espace de travail à partir d'un fichier »). Relever :
- les dossiers résolus ou en erreur dans l'explorateur ;
- le chemin de l'espace que VSCodium retient (titre de la fenêtre, liste des récents) : lien ou
  cible ;
- la valeur de `${workspaceFolder:trunk}` et de `${workspaceFolder}` vue par une tâche d'écho
  ajoutée à la variante ;
- le répertoire de travail de l'extension Lepton (`runner.ts` `cwd()` = répertoire du fichier
  d'espace) : une action de l'extension (vérifier) trouve-t-elle le rootstock.

### 3. Essai (c) — variables dans les réglages
`CADRAGE.md` §6 avance que `${workspaceFolder:trunk}/..` est accepté par clangd, CMake Tools,
`launch` et `tasks`. Le vérifier réglage par réglage sur la variante qui s'ouvre correctement, en
remplaçant un chemin absolu à la fois dans le fichier du clone : `clangd.arguments`
(`--compile-commands-dir`, `--query-driver`), `cmake.copyCompileCommands`,
`cortex-debug.gdbPath`, `cortex-debug.armToolchainPath`, `cortex-debug.openocdPath`,
`json.schemas`, `xml.fileAssociations`, une entrée de `launch`, une tâche. Relever aussi si
`${config:lepton.<clé>}` et `${input:<id>}` sont développés dans `settings`, `launch` et `tasks`.
Un réglage par ligne dans le rapport : développé, non développé, non essayé.

### 4. Essai (b) — écriture par l'interface
**Dernier essai sur cette copie.** L'utilisateur modifie un réglage d'espace par l'interface
(« Préférences : ouvrir les paramètres de l'espace de travail »), puis ajoute un dossier à
l'espace. Après chaque geste, relever : `ls -l` du chemin du trunk (lien conservé ou fichier
régulier), contenu du fichier du clone, `git -C <clone> status --short`, `lepton check` (code et
message), intervention ou non de la redirection FIC-3 de l'extension.

Si le lien est remplacé par un fichier régulier, la session ne peut pas le retirer : le hook
protège le trunk de tout rootstock, `scripts/supprimer-essai.sh` refuse un chemin `*/trunk/*`, et
`scion graft` s'arrête sur un fichier étranger. L'utilisateur déplace alors le fichier hors du
trunk, ou la suite repart d'une copie neuve.

### 5. Constat du besoin 2 — deux rootstocks, deux fenêtres
Second rootstock d'essai sous `~/lepton-tools-dev/essais/ep-0/b` (copie sans `build/` d'un autre
essai, ou seconde copie régénérée). `<ROOTSTOCK>` n'est pas utilisé. Les deux espaces ouverts en
même temps, relever : chaque action de l'extension Lepton vise son rootstock ; configuration et
construction CMake Tools dans chaque `build/` ; index clangd de chaque `build/.active/` ; deux
sessions de débogage QEMU simultanées (ports) ; toute ressource partagée (`lepton` installé,
`LEPTON_EMBOS_ROOT`, réglages utilisateur de VSCodium). Un défaut constaté va au PA-E1.

### 6. Point d'arrêt → PA-E1
Présenter le rapport. L'utilisateur tranche :
- C2 et C3 maintenues, ou révisées (emplacement de l'espace, mode d'ouverture) ;
- effets sur EP-1, EP-2 et EP-4, et révision du plan s'il y a lieu ;
- essais (a) et (b) refaits à la main sur la VM Debian avant EP-4, ou preuve Debian laissée à
  EP-8 ;
- suite d'un défaut du constat du besoin 2 (étape, hors plan) ;
- sort des essais `essais/ep-0/` (suppression par `scripts/supprimer-essai.sh`).

## Critères de validation
- [ ] Rapport `rapports/ep-0-essai-lien.md` : (a), (b), (c) et le constat du besoin 2 ont chacun
      une réponse appuyée d'une preuve, ou la mention « non conclu » avec la raison.
- [ ] `git -C <LEPTON_TOOLS> diff --stat main -- . ':!doc/espace-projet'` : vide.
- [ ] `git -C <SEED_SCIONS> status --short` et `git -C <ROOTSTOCK>/depots/lepton/original/master
      status --short` : inchangés par rapport au relevé de début de session.
- [ ] PA-E1 tranché et consigné dans `STATUS.md` §Décisions.

## Pièges connus
- VSCodium peut garder un état par chemin d'espace : fermer la fenêtre entre deux variantes,
  noter le chemin exact ouvert, et relever si un état est gardé.
- Un lien remplacé par un fichier régulier est un fichier étranger du trunk : le relever avant
  toute autre manipulation.
- Le filtre E1 ne greffe pas un fichier ignoré par git : vérifier par `git check-ignore` que la
  variante déposée n'est couverte par aucun `.gitignore` du clone.
- Le hook `proteger-trunk.py` protège le `trunk/` et le `depots/tiers/` de tout rootstock, essais
  compris : un refus signale une erreur de chemin, ne pas le contourner.
- Une copie faite avec `build/` garde le cache CMake de l'original : le constat du besoin 2 en
  serait faussé.
- Résultat valable pour VSCodium sur macOS seulement ; Debian : selon le PA-E1, sinon EP-8.

## À la fin de l'étape
`STATUS.md` : statut, branche, décision PA-E1, journal, « Prochaine action » (EP-1 ou EP-2, ou
révision du plan). `HORS-PLAN.md` : tout point écarté. Passation `handoff/ep-0.md`.
