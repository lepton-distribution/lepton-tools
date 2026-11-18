# Étape ENV-66 — Validation Debian groupée (ENV-62, ENV-63, ENV-64, ENV-65)

## Contexte
ENV-62 à ENV-65 ne valident que sur le Mac. Elles changent :
- ENV-62 (D26, D28, D27) : la règle utilisateur U3 de la VM, la conduite des invites à refuser
  et les outils de comparaison des consignes (ORCHESTRATION §2bis amendé au PA-111). Les
  décisions qui touchent la VM ne sont appliquées et prouvées qu'ici ;
- ENV-63 (D21) : lepton, `~` dans les chemins saisis ;
- ENV-64 (D23, D24) : l'extension, `lepton.path` et la regreffe après `--purge`, dans une
  nouvelle version ;
- ENV-65 (D25, D22) : scion, le clone existant hors version et le message de `git clone`, dans
  une nouvelle version.

Les liens du trunk, les clones et les binaires ne doivent pas changer. Cette étape valide
l'ensemble sur la VM Debian par un seul ordre (§2bis), puis regreffe au besoin les rootstocks
d'essai du Mac. Forme : celle d'ENV-61. Archétype : infrastructure. Décision de l'utilisateur
(révision du 2026-11-18) : cette validation Debian clôt le plan.

## Prérequis
- ENV-62, ENV-63, ENV-64 et ENV-65 terminées et poussées.
- VM Debian 13 avec sa session Claude Code (ORCHESTRATION §2) ; protocole §2bis, remise en échec
  comprise.
- Références :
  - consigne `consignes/env-61-debian.md` ;
  - rapports `rapports/env-61-debian.md` et `rapports/env-61-mac.md` ;
  - oracle Debian `rapports/oracles/env-61-debian/`, oracle Mac `rapports/oracles/env-52-apres/` ;
  - outils `rapports/env-61-mac/ls-remote.sh`, `rapports/env-57-mac/regreffer-essai.sh`,
    `decisions.py` ; outils communs d'ENV-62 s'il y en a (PA-111).
- Règles des consignes VM : ORCHESTRATION §2bis, tel qu'amendé en ENV-62 (PA-111).
- Texte exact des réglages utilisateur attendus sur la VM, s'ils changent : rapport d'ENV-62,
  §D26 (`rapports/env-62-claude-code.md`, PA-111).
- U3 (D26) : `python3 -m unittest discover -s ~/lepton-tools-dev/essais/env-61-absent`, décidé
  par le classifieur en R61-1 au lieu de la règle utilisateur `Bash(python3 -m unittest
  discover *)`.
- Node.js est absent de la VM (`rapports/env-53-debian.md`, l. 30) ; `install-vscodium.sh`
  installe le `.vsix` sans Node.js.
- État laissé sur la VM par R61-1 (`handoff/env-61.md`) :
  - outils : scion 0.6.3.2, lepton 0.1.0, extension 0.5.2, Claude Code 2.1.326 ;
  - `essais/env-28-debian`, `essais/env-13-debian`, `essais/env-53-c5` et `essais/env-53-debian`
    regreffés, noyau dfc960b ; `essais/env-53-c5` : graine de projet de référence (D15) ;
  - journaux `~/env-61-journaux` ; `~/tmp-pytest` ;
  - session VM dans `~/lepton-tools-dev/lepton-tools`, sur `devenv/env-61-debian` ;
  - `~/.claude/settings.json` : 3 règles `allow` (D19, PA-103).
- Passations `handoff/env-62.md` à `handoff/env-65.md` : décisions PA-111, PA-113, PA-115,
  PA-117.
- Branches lepton-tools : `devenv/env-66` (Mac), `devenv/env-66-debian` (VM).

## Tâches

### 1. Préparation (Mac) → PA-119
- Rapport Mac `rapports/env-66-mac.md` : préparation, puis journal des messages §2bis, puis
  contrôle du rapport VM.
- Attendus versionnés dans `rapports/env-66-mac/attendu/`, relevés sur une copie d'essai de la
  graine de projet du Mac, avec le lepton et le scion publiés :
  - D21 : formes du PA-113 (scripts d'ENV-63) ;
  - D25 et D22 : cas du PA-117 (scripts d'ENV-65) ;
  - D23 : formes du PA-115 (script `node` d'ENV-64) ;
  - liste `chemin -> cible` : aucun changement attendu depuis R61-1.
- Têtes publiées relevées par `rapports/env-66-mac/ls-remote.sh`, reprise de
  `rapports/env-61-mac/ls-remote.sh` avec le tag d'ENV-65. Elles décident C3 et la tâche 3.
- Contrôles de correction de la consigne : écrits selon le PA-111 (D27 ; piège d'ENV-61, contrôle
  D17 écrit d'après l'ancien code).
- Consigne `consignes/env-66-debian.md` :
  - **§0, préalable (utilisateur), avant l'ordre** :
    - `switch` de `~/lepton-tools-dev/lepton-tools` sur `devenv/env-66` ;
    - s'il y a lieu (PA-111), `~/.claude/settings.json` de la VM modifié par la personne et au
      moment que désigne le PA-111. Le fichier entier est relu avant
      (`python3 -m json.tool`), puis comparé après ;
    - session Claude Code relancée, et son nom communiqué à la session Mac. En R61-1, la
      session n'avait pas été relancée (`rapports/env-61-debian.md` §9, écart 1).
  - Critères numérotés :
    - **C1** — versions : scion d'ENV-65, lepton, extension d'ENV-64, git, Claude Code. Chaque
      commande est écrite dans la forme du §2bis. C1 précède C4 et C5.
    - **C2** — D26 et D28 sur la VM, décisions relevées par `decisions.py` :
      - contenu des réglages utilisateur, lu par `python3 -m json.tool ~/.claude/settings.json` ;
      - U3 (voir Prérequis), et la commande de l'essai témoin d'ENV-62, sous la règle décidée au
        PA-111 ;
      - toute invite à refuser, dans la forme décidée au PA-111 (annonce, cible absente) ;
      - le hook refuse une écriture shell sous le `trunk/` d'un rootstock d'essai.
    - **C3** — regreffe d'`essais/env-28-debian`, `essais/env-13-debian`, `essais/env-53-c5` et
      `essais/env-53-debian`, si une tête qu'ils greffent a changé. Avant toute regreffe,
      relever la branche de chaque clone (§2bis). Après : liens inchangés, `CONFORME`,
      `lepton check` code 0. <À CONFIRMER au PA-119>.
    - **C4** — D21 : formes du PA-113 sur une copie d'`essais/env-53-c5`, comparées à l'attendu
      du Mac, normalisé selon les règles d'ENV-62 (D27).
    - **C5** — D25 et D22 :
      - cas de lepton sur la même copie, comparés à l'attendu du Mac ; liens et graine égaux à
        l'avant ;
      - `pytest` complet de lepton-tools (`venv-test`, `--basetemp`, `--junitxml`) ;
      - cas de fixture d'ENV-65, si le PA-119 les retient. <À CONFIRMER au PA-119>.
    - **C6** — extension (D23, D24) : `.vsix` installé par `install-vscodium.sh`. Node.js étant
      absent de la VM, le script `node` de D23 n'y tourne pas. Options : installer Node.js sur la
      VM (variable nouvelle), essayer D23 dans VSCodium, ou relever D23 au Mac seulement. D24
      dans VSCodium sur la VM, par l'utilisateur, s'il a accès à l'interface.
      <À CONFIRMER au PA-119>.
    - **C7** — host et 16 presets contre `env-61-debian`, et `mirror-sync --dry-run`.
      <À CONFIRMER au PA-119 : aucun binaire changé attendu>.
    - **C8** — cartes sur la VM. <À CONFIRMER au PA-119>.
    - **C9** — nettoyage : `~/env-61-journaux`, copies et dépôts d'essai de R66-1, par
      `scripts/supprimer-essai.sh`. <À CONFIRMER au PA-119>.
  - Paragraphe « Communication » : nom de la session principale, ID `R66-1`, conduite quand un
    message n'est pas remis (§2bis, « Remise en échec »).
- **PA-119** : l'utilisateur valide :
  - la consigne et les critères C3, C5 (fixture), C6, C7, C8, C9 ;
  - le §0, dont le bloc des réglages de la VM s'il change ;
  - le push de `devenv/env-66` (PA-P), puis l'envoi de l'ordre `R66-1` à la session VM.

### 2. Exécution (VM)
La session VM suit la consigne :
- elle envoie un `ACCUSÉ`, puis un `AVANCEMENT` par critère et à chaque attente de l'utilisateur ;
- elle termine par `FIN-SUCCÈS` ou `FIN-ÉCHEC` ;
- elle écrit son rapport `rapports/env-66-debian.md`, et son oracle si C7 en produit un, sur
  `devenv/env-66-debian`, puis les pousse (PA-P).

### 3. Rootstocks d'essai (Mac)
- Regreffer, sur accord (PA-P), les rootstocks d'essai qui greffent une tête changée depuis R61-1
  (`git ls-remote` de la tâche 1) :
  - liste : `essais/env-13-vierge`, `essais/env-9`, et sous `essais/env-11/` : `qemu`,
    `qemu-gra2`, `bout-en-bout/rootstock`, `f429zi`, `wl55jc1` ;
  - procédure : `rapports/env-57-mac.md` §4. `regreffer-essai.sh avant`, puis le
    `scion graft-update` lancé par la session hors script (invite `ask`), puis
    `regreffer-essai.sh apres`.
- Puis `lepton check` et `generate` : code 0 (`qemu-gra2` : 1, attendu).

### 4. Clôture → PA-120
- Session Mac : vérifier le rapport VM contre la consigne (chaque critère, commits cités) ;
  refaire les comparaisons sur les relevés poussés.
- **PA-120** : fusion de `devenv/env-66-debian` dans `devenv/env-66`, puis dans `main` ; push
  (PA-P).

## Critères de validation
- [ ] PA-119 et PA-120 tranchés et consignés.
- [ ] `FIN-SUCCÈS R66-1` vérifié par la session Mac ; C1 à C9 conformes, ou écartés au PA-119.
- [ ] D26 : décision de U3 conforme au PA-111 ; réglages de la VM conformes au PA-111.
- [ ] D28 : aucune invite à refuser confirmée, ou chaque confirmation consignée.
- [ ] D27 : aucune comparaison faussée par la langue, l'espace insécable ou le segment d'hôte.
- [ ] Rootstocks d'essai regreffés, s'il y a lieu : 0 lien cassé, 0 fichier régulier (hors
      `.DS_Store` tolérés) ; `check` code 0 (`qemu-gra2` : 1, attendu).
- [ ] Fin du plan : `HORS-PLAN.md` présenté à l'utilisateur pour décision.

## Pièges connus
- Les réglages utilisateur de la VM sont hors du dépôt : la session Mac ne les lit pas. Relire
  leur contenu au début de C2, avant tout contrôle.
- Une session VM non relancée garde son nom (`ListAgents`) : seul l'ACCUSÉ montre la branche et
  l'état réels (R61-1).
- Confirmer par erreur une invite `ask` sur une cible existante a un effet réel : contrôles sur
  cibles absentes seulement.
- Le classifieur de la VM peut accepter ce que la règle ne couvre pas. Seules comptent les
  décisions marquées règle ou invite.
- D21, D22 et D25 dépendent du lepton et du scion installés : aucun essai de C4 ni de C5 avant C1.
- Sur la VM, git écrit ses messages en français, avec une espace insécable dans « fatal : ».
  Comparer selon les règles d'ENV-62 (D27). Le message de D22 change ce que l'ancien `fr()`
  ramenait.
- Le `essais/env-53-c5` de la VM garde les clones F7 de R53-1 (`seed remove` conserve les
  clones) : éviter le F7 dans C4 et C5.
- Le hook refuse `git config` sous `depots/tiers/`, même en lecture : lire `.git/config.worktree`,
  puis `.git/config`, par `grep`.
- `qemu-gra2` : `graft-update` réinscrit le BSP an386. Le retirer par `scion graft-remove`, sans
  `--purge`.
- Si des cartes passent par la VM : la NUCLEO-F429ZI peut revenir muette en Ethernet (D12, hors
  plan) ; parade de `handoff/env-50.md`.

## À la fin de l'étape
`DEVENV-STATUS.md` :
- statut ;
- versions Debian ;
- décisions PA-119 et PA-120 ;
- journal (ordre R66-1) ;
- « Prochaine action » : fin du plan, présentation de `HORS-PLAN.md`, puis révision du plan si des
  points sont retenus.

`HORS-PLAN.md` : D21 à D28 prouvés sur la VM, ou écartés au PA-119 (renvois aux critères) ; ajouter tout point écarté
pendant l'étape. Passation `handoff/env-66.md`.
