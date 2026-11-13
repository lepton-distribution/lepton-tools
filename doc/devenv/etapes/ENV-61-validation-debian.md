# Étape ENV-61 — Validation Debian groupée (ENV-58, ENV-59, ENV-60)

## Contexte
ENV-58, ENV-59 et ENV-60 ne valident que sur le Mac. Elles changent :
- ENV-58 (D20, D19) : les formes des commandes (ORCHESTRATION §2bis amendé) et la décision sur les
  règles `allow` utilisateur de la VM. Ces règles ne sont modifiées et prouvées qu'ici, sur la VM ;
- ENV-59 (D17) : lepton, l'indice « version sans effet » et `~` ;
- ENV-60 (D18) : scion, le clone gardé après un checkout en échec, dans une nouvelle version.

Les liens du trunk, les clones et les binaires ne doivent pas changer. Cette étape valide
l'ensemble sur la VM Debian par un seul ordre (§2bis), puis regreffe au besoin les rootstocks
d'essai du Mac. Forme : celle d'ENV-57. Archétype : infrastructure. Décision de l'utilisateur
(révision du 2026-11-13) : cette validation Debian clôt le plan.

## Prérequis
- ENV-58, ENV-59 et ENV-60 terminées et poussées.
- VM Debian 13 avec sa session Claude Code (ORCHESTRATION §2) ; protocole §2bis, remise en échec
  comprise.
- Références :
  - consigne `consignes/env-57-debian.md` ;
  - rapports `rapports/env-57-debian.md` et `rapports/env-57-mac.md` ;
  - oracle Debian `rapports/oracles/env-57-debian/`, oracle Mac `rapports/oracles/env-52-apres/` ;
  - outils `rapports/env-57-mac/` : `ls-remote.sh`, `regreffer-essai.sh`, `decisions.py`.
- Règles des consignes VM : ORCHESTRATION §2bis, tel qu'amendé en ENV-58 (PA-103).
- Texte exact des réglages utilisateur attendus sur la VM : rapport d'ENV-58 (D19, PA-103).
- État laissé sur la VM par R57-1 (`handoff/env-57.md`) :
  - outils : scion 0.6.3.1, lepton 0.1.0, extension 0.5.2, Claude Code 2.1.323 ;
  - `essais/env-28-debian`, `essais/env-13-debian`, `essais/env-53-c5` et `essais/env-53-debian`
    regreffés, noyau ed2a41f ;
  - `essais/env-53-c5` : graine de projet de référence (D15) ; `essais/env-11/` supprimé ;
  - journaux `~/env-57-journaux` ; `~/tmp-pytest` ;
  - session VM dans `~/lepton-tools-dev/lepton-tools`, sur `devenv/env-57-debian` ;
  - `~/.claude/settings.json` (10 nov.) : 3 règles `allow` (D19).
- Passations `handoff/env-58.md`, `handoff/env-59.md`, `handoff/env-60.md` : formes et règles
  (PA-103), portée de D17 (PA-105), correction et version de scion (PA-107).
- Branches lepton-tools : `devenv/env-61` (Mac), `devenv/env-61-debian` (VM).

## Tâches

### 1. Préparation (Mac) → PA-109
- Rapport Mac `rapports/env-61-mac.md` : préparation, puis journal des messages §2bis, puis
  contrôle du rapport VM.
- Attendus versionnés dans `rapports/env-61-mac/attendu/`, relevés sur une copie d'essai de la
  graine de projet du Mac (forme d'`essais/env-57-essai`) :
  - D17 : sorties de lepton pour les formes du PA-105 (scripts d'ENV-59) ;
  - D18 : cas de lepton d'ENV-60 (dépôt d'essai, version absente) selon le PA-107 ;
  - liste `chemin -> cible` : aucun changement attendu depuis R57-1.
- Têtes publiées relevées par `rapports/env-61-mac/ls-remote.sh`. C'est la reprise de
  `rapports/env-57-mac/ls-remote.sh`, qui a le tag `0.6.3.1` en dur (l. 9), avec le tag
  d'ENV-60. Relevés : lepton-tools, `seed.scions` (tag), noyau et autres greffons, graine,
  8 miroirs. Ils décident C3 et la tâche 3.
- Consigne `consignes/env-61-debian.md` :
  - **§0, préalable (utilisateur), avant l'ordre** :
    - `switch` de `~/lepton-tools-dev/lepton-tools` sur `devenv/env-61` ;
    - s'il y a lieu, `~/.claude/settings.json` de la VM modifié par la personne et au moment que
      désigne le PA-103. Seul le bloc `permissions.allow` du rapport d'ENV-58 change : le
      fichier entier est relu avant (`python3 -m json.tool`), puis comparé après ;
    - session Claude Code relancée dans ce répertoire. Précaution, tranchée au PA-109 : les
      réglages sont relus à chaud (`rapports/env-54-permissions.md` §3, point 7) ;
    - nom de la nouvelle session communiqué à la session Mac (forme du §0 de
      `consignes/env-57-debian.md`).
  - Critères numérotés :
    - **C1** — versions : scion d'ENV-60, lepton, extension, git, Claude Code. Si `SCION_REF`
      n'a pas changé au PA-107, la commande `pipx` de scion est donnée en clair. Chaque
      commande est écrite dans la forme du §2bis amendé. C1 précède C4 et C5 : D17 et D18
      dépendent du lepton et du scion installés.
    - **C2** — D19 et D20 sur la VM, décisions relevées par `decisions.py` :
      - contenu des réglages utilisateur, lu par `python3 -m json.tool ~/.claude/settings.json` ;
      - `pipx install --force ~/lepton-tools-dev/lepton-tools` accepté par la règle du dépôt
        (`projectSettings`) ;
      - formes de l'essai témoin d'ENV-58 : commande `allow` nue et avec redirection ; commande
        `ask` lancée directement, depuis un script et par `bash -c`, sur une cible absente
        seulement ;
      - toute règle ajoutée au PA-103 ;
      - contrôle négatif pour chaque règle utilisateur retirée ou restreinte au PA-103 : une
        commande que seule cette règle couvrait, sur une cible absente ou sans effet. Exemples :
        `pipx install ~/lepton-tools-dev/essais/env-61-absent`,
        `git clone --depth 1 https://github.com/lepton-distribution/x ~/lepton-tools-dev/essais/env-61-absent`.
        Attendu : aucune décision par une règle utilisateur (`userSettings`) ;
      - scripts de l'essai témoin repris de `rapports/env-58-formes/` ;
      - le hook refuse une écriture shell sous le `trunk/` d'un rootstock d'essai.
    - **C3** — regreffe d'`essais/env-28-debian`, `essais/env-13-debian`, `essais/env-53-c5` et
      `essais/env-53-debian`, si une tête qu'ils greffent a changé. Le noyau change si
      `SCION_REF` a changé. <À CONFIRMER au PA-109>. Avant toute regreffe, relever la branche de
      chaque clone (§2bis). Après : liens inchangés, `CONFORME`, `lepton check` code 0.
    - **C4** — D17 : formes du PA-105 sur une copie d'`essais/env-53-c5`, comparées à l'attendu
      du Mac. Les chemins personnels (`~<utilisateur>`, `$HOME` : `cle_d_anton`, `lepton-user`)
      sont normalisés dans l'attendu et dans le relevé.
    - **C5** — D18 :
      - cas de lepton sur la même copie, comparé à l'attendu du Mac ; liens et graine égaux à
        l'avant ;
      - `pytest` complet de lepton-tools (`venv-test`, `--basetemp`, `--junitxml`, forme du §11.2
        de `consignes/env-57-debian.md`) ;
      - cas f06 de la fixture d'ENV-56 : `fixture.py` demande un clone de seed.scions. La
        préparation relève s'il en existe un sur la VM ; R57-1 n'y installe scion que par pipx,
        depuis l'URL GitHub (`rapports/env-57-debian.md` §1). Un `git clone
        https://github.com/lepton-distribution/seed.scions.git` est couvert par la règle
        `allow` ; `python3 fixture.py` passe au classifieur. <À CONFIRMER au PA-109>.
    - **C6** — host et 16 presets contre `env-57-debian`, et `mirror-sync --dry-run`.
      <À CONFIRMER au PA-109 : aucun binaire changé attendu>.
    - **C7** — cartes sur la VM. <À CONFIRMER au PA-109>.
    - **C8** — nettoyage : `~/env-57-journaux`, copies et dépôts d'essai de R61-1, par
      `scripts/supprimer-essai.sh`. <À CONFIRMER au PA-109>.
  - Paragraphe « Communication » : nom de la session principale, ID `R61-1`, conduite quand un
    message n'est pas remis (§2bis, « Remise en échec »).
- **PA-109** : l'utilisateur valide :
  - la consigne et les critères C3, C5 (fixture), C6, C7, C8 ;
  - le bloc des réglages de la VM, la personne qui le modifie, et le §0 ;
  - le push de `devenv/env-61` (PA-P), puis l'envoi de l'ordre `R61-1` à la session VM.

### 2. Exécution (VM)
La session VM suit la consigne :
- elle envoie un `ACCUSÉ`, puis un `AVANCEMENT` par critère et à chaque attente de l'utilisateur ;
- elle termine par `FIN-SUCCÈS` ou `FIN-ÉCHEC` ;
- elle écrit son rapport `rapports/env-61-debian.md`, et son oracle si C6 en produit un, sur
  `devenv/env-61-debian`, puis les pousse (PA-P).

### 3. Rootstocks d'essai (Mac)
- Regreffer, sur accord (PA-P), les rootstocks d'essai qui greffent une tête changée depuis R57-1
  (`git ls-remote` de la tâche 1) :
  - liste : `essais/env-13-vierge`, `essais/env-9`, et sous `essais/env-11/` : `qemu`,
    `qemu-gra2`, `bout-en-bout/rootstock`, `f429zi`, `wl55jc1` ;
  - procédure : `rapports/env-57-mac.md` §4. `regreffer-essai.sh avant`, puis le
    `scion graft-update` lancé par la session hors script (invite `ask`), puis
    `regreffer-essai.sh apres`.
- Puis `lepton check` et `generate` : code 0 (`qemu-gra2` : 1, attendu).

### 4. Clôture → PA-110
- Session Mac : vérifier le rapport VM contre la consigne (chaque critère, commits cités) ;
  refaire les comparaisons sur les relevés poussés.
- **PA-110** : fusion de `devenv/env-61-debian` dans `devenv/env-61`, puis dans `main` ; push
  (PA-P).

## Critères de validation
- [ ] PA-109 et PA-110 tranchés et consignés.
- [ ] `FIN-SUCCÈS R61-1` vérifié par la session Mac ; C1 à C8 conformes, ou écartés au PA-109.
- [ ] D19 : réglages utilisateur de la VM conformes au PA-103 ; chaque règle retirée ou
      restreinte a son contrôle négatif ; aucune décision relevée n'est due à une règle écartée.
- [ ] D20 : décisions des formes de l'essai témoin, sur la VM, au rapport.
- [ ] Rootstocks d'essai regreffés, s'il y a lieu : 0 lien cassé, 0 fichier régulier (hors
      `.DS_Store` tolérés) ; `check` code 0 (`qemu-gra2` : 1, attendu).
- [ ] Fin du plan : `HORS-PLAN.md` présenté à l'utilisateur pour décision.

## Pièges connus
- Les réglages utilisateur de la VM sont hors du dépôt : la session Mac ne les lit pas. Relire
  leur contenu au début de C2, avant tout contrôle.
- Le nom de la session VM change à chaque relance (R57-1 : d3fe18 annoncé, 153462 vu). Le nom
  et l'adresse `from` suffisent.
- Confirmer par erreur une invite `ask` sur une cible existante a un effet réel : contrôles sur
  cibles absentes seulement (N4 d'ENV-57).
- Le classifieur de la VM peut accepter ce que la règle ne couvre pas. Seules comptent les
  décisions marquées règle ou invite.
- D17 et D18 dépendent du lepton et du scion installés, pas de l'état du rootstock : aucun essai
  de C4 ni de C5 avant C1.
- Sur la VM, git écrit ses messages en français : normaliser ces lignes dans les comparaisons de
  sorties (`consignes/env-57-debian.md` §11.1).
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
- décisions PA-109 et PA-110 ;
- journal (ordre R61-1) ;
- « Prochaine action » : fin du plan, présentation de `HORS-PLAN.md`, puis révision du plan si des
  points sont retenus.

`HORS-PLAN.md` : D17, D18, D19 et D20 prouvés sur la VM (C4, C5, C2) ; ajouter tout point
écarté pendant l'étape. Passation
`handoff/env-61.md`.
