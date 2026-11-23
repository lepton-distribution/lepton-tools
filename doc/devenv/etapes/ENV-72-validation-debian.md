# Étape ENV-72 — Validation Debian groupée (ENV-67 à ENV-71)

## Contexte
ENV-67 à ENV-71 ne valident que sur le Mac. Elles changent :
- ENV-67 (D38) : l'enveloppe `scripts/supprimer-essai.sh` et les règles des consignes VM,
  amendées au §2bis (PA-121) ;
- ENV-68 (D29, D30, D32, D37) : lepton, chemins saisis et cohérence de la graine ;
- ENV-69 (D36) : l'extension, greffons observés, version 0.5.4 ;
- ENV-70 (D35, D33) : scion 0.6.3.4, cause de l'échec de git et version de la graine clonée. D35
  ne se voit qu'avec git 2.47.3, l'hôte de la VM : sa preuve réelle est ici ;
- ENV-71 (D40) : les miroirs de conservation, synchronisés.

D39 (révision du 2026-11-23) s'applique pour la première fois : aucune invite au Mac pendant que
la VM peut en présenter une (ORCHESTRATION §2bis, « Invites simultanées »).

Les liens du trunk, les clones et les binaires ne doivent pas changer. L'étape valide l'ensemble
sur la VM Debian par un seul ordre (§2bis), puis regreffe au besoin les rootstocks d'essai du Mac.
Forme : celle d'ENV-66. Archétype : infrastructure. Cette validation Debian clôt le plan.

## Prérequis
- ENV-67 à ENV-71 terminées et poussées.
- VM Debian 13 avec sa session Claude Code (ORCHESTRATION §2) ; protocole §2bis, remise en échec
  comprise.
- Références :
  - consigne `consignes/env-66-debian.md` ;
  - rapports `rapports/env-66-debian.md` et `rapports/env-66-mac.md` ;
  - oracle Debian `rapports/oracles/env-66-debian/` ; oracle Mac `rapports/oracles/env-52-apres/`.
- Outils :
  - `rapports/env-66-mac/ls-remote.sh` ;
  - `rapports/env-57-mac/regreffer-essai.sh` et `decisions.py` ;
  - `scripts/comparer-releves.py` ;
  - scripts d'ENV-68 et d'ENV-70.
- Règles des consignes VM : ORCHESTRATION §2bis, tel qu'amendé en ENV-67 selon le PA-121 : relevé
  des variables d'environnement (D38 (1)), contrôle Mac de la consigne (D38 (3)).
- État laissé sur la VM par R66-1 et R66-2 (`handoff/env-66.md`) :
  - outils : scion 0.6.3.3, lepton 0.1.0 (D21), extension 0.5.3, git 2.47.3, Claude Code
    2.1.328 ;
  - `~/.claude/settings.json` : 2 règles `allow` ;
  - `essais/` : `env-13-debian`, `env-28-debian`, `env-53-c5` (graine de projet de référence,
    D15), `env-53-debian`, regreffés au noyau 2b4a647 ;
  - `~/tmp-pytest` vide ;
  - zsh absent (D38 (4), hors plan).
- Branches lepton-tools : `devenv/env-72` (Mac), `devenv/env-72-debian` (VM).

## Tâches

### 1. Préparation (Mac) → PA-131
- Rapport Mac `rapports/env-72-mac.md` : préparation, puis journal des messages §2bis, puis
  contrôle du rapport VM.
- Attendus versionnés dans `rapports/env-72-mac/attendu/`, relevés avec le lepton et le scion
  publiés, selon la forme du contrôle Mac retenue au PA-121 (D38 (3)) :
  - D29, D30, D32, D37 : cas du PA-123 (scripts d'ENV-68) ;
  - D35, D33 : cas du PA-127 (fixtures d'ENV-70). Pour D35, l'attendu de la VM n'est pas celui du
    Mac, puisque git diffère : il est écrit d'après le PA-127 ;
  - liste `chemin -> cible` : aucun changement attendu depuis R66-1.
- Têtes publiées relevées par `rapports/env-72-mac/ls-remote.sh`, reprise d'ENV-66 avec le tag
  d'ENV-70. Elles décident C3 et la tâche 3.
- Consigne `consignes/env-72-debian.md` :
  - **§0, préalable (utilisateur), avant l'ordre** :
    - `switch` de `~/lepton-tools-dev/lepton-tools` sur `devenv/env-72` ;
    - variables d'environnement selon la forme retenue au PA-121 (`LEPTON_EMBOS_ROOT` comprise) ;
    - session Claude Code relancée, et son nom communiqué à la session Mac.
  - Critères numérotés :
    - **C1** — versions (scion 0.6.3.4, lepton, extension 0.5.4, git, Claude Code) et variables
      d'environnement du PA-121. C1 précède C4 et C5.
    - **C2** — règles et hook : réglages utilisateur relus (2 règles attendues) ; décisions
      relevées par `decisions.py` ; enveloppe d'ENV-67 sur une cible `~/tmp-pytest/<sous-rép>`
      d'essai (règle `allow`) ; hook. Toute invite à refuser est annoncée « À REFUSER ».
    - **C3** — regreffe des 4 rootstocks d'essai de la VM, si une tête qu'ils greffent a changé.
      Avant toute regreffe, relever la branche de chaque clone (§2bis) et celle de la graine clonée
      de chaque rootstock (`depots/lepton-seed.scions/original-tree`, D33). Après : liens inchangés,
      `CONFORME`, `lepton check` code 0. <À CONFIRMER au PA-131>.
    - **C4** — lepton (D29, D30, D32, D37) sur une copie d'`essais/env-53-c5`, comparé à
      l'attendu du Mac par `comparer-releves.py`.
    - **C5** — scion :
      - D35 : k07 et f05 de la fixture d'ENV-65, et cas d'ENV-70, avec git 2.47.3. La cause
        paraît, et non l'avertissement ;
      - D33 : cas d'ENV-70 ;
      - `pytest` complet de lepton-tools (`venv-test`, `--basetemp`, `--junitxml`).
    - **C6** — extension 0.5.4 par `install-vscodium.sh`. Si l'utilisateur a accès à l'interface,
      T3 de D36 dans VSCodium sur la VM. <À CONFIRMER au PA-131>.
    - **C7** — host et 16 presets contre `env-66-debian` ; `mirror-sync --dry-run` : 0 référence
      à envoyer attendue (ENV-71), sauf nouvelle publication de l'amont, à expliquer.
    - **C8** — cartes sur la VM. <À CONFIRMER au PA-131>.
    - **C9** — nettoyage par `scripts/supprimer-essai.sh`, sous-répertoires de `~/tmp-pytest`
      compris (D38 (2)). <À CONFIRMER au PA-131>.
  - Paragraphe « Communication » : nom de la session principale, ID `R72-1`, remise en échec.
  - Invites (D39) : la consigne liste les critères qui présentent une invite (C2, C3, push final)
    et fait envoyer un `AVANCEMENT` « fin des invites de la VM » après le dernier d'entre eux ;
    la session Mac ne lance aucune commande à invite avant cet `AVANCEMENT` ou le `FIN-*`.
- **PA-131** : l'utilisateur valide :
  - la consigne et les critères C3, C6, C8, C9 ;
  - le §0 ;
  - le push de `devenv/env-72` (PA-P), puis l'envoi de l'ordre `R72-1`.

### 2. Exécution (VM)
La session VM suit la consigne :
- elle envoie un `ACCUSÉ`, puis un `AVANCEMENT` par critère et à chaque attente de l'utilisateur ;
- elle termine par `FIN-SUCCÈS` ou `FIN-ÉCHEC` ;
- elle écrit son rapport `rapports/env-72-debian.md`, et son oracle si C7 en produit un, sur
  `devenv/env-72-debian`, puis les pousse (PA-P).

### 3. Rootstocks d'essai (Mac)
- Regreffer, sur accord (PA-P), les rootstocks d'essai qui greffent une tête changée depuis
  R66-1 :
  - liste : `essais/env-13-vierge`, `essais/env-9` et, sous `essais/env-11/`, `qemu`,
    `qemu-gra2`, `bout-en-bout/rootstock`, `f429zi`, `wl55jc1` ;
  - procédure : `rapports/env-57-mac.md` §4. Commencée après l'`AVANCEMENT` « fin des invites de
    la VM » ou le `FIN-*` (D39).
- Puis `lepton check` et `generate` : code 0 (`qemu-gra2` : 1, attendu).

### 4. Clôture → PA-132
- Session Mac : vérifier le rapport VM contre la consigne, critère par critère et commit par
  commit cité ; refaire les comparaisons sur les relevés poussés.
- **PA-132** : fusion de `devenv/env-72-debian` dans `devenv/env-72`, puis dans `main` ; push
  (PA-P).

## Critères de validation
- [ ] PA-131 et PA-132 tranchés et consignés.
- [ ] `FIN-SUCCÈS R72-1` vérifié par la session Mac ; C1 à C9 conformes, ou écartés au PA-131.
- [ ] D35 : cause de git montrée avec git 2.47.3 ; D33, D29, D30, D32, D37 conformes à l'attendu.
- [ ] D38 : variables traitées selon le PA-121 ; nettoyage de sous-répertoires par l'enveloppe.
- [ ] D39 : aucune invite simultanée Mac et VM ; toute confirmation par erreur consignée.
- [ ] Rootstocks d'essai regreffés, s'il y a lieu : 0 lien cassé, 0 fichier régulier (hors
      `.DS_Store` tolérés) ; `check` code 0 (`qemu-gra2` : 1).
- [ ] Fin du plan : `HORS-PLAN.md` présenté à l'utilisateur pour décision.

## Pièges connus
- Sur la VM, git écrit en français, avec une espace insécable dans « fatal : ». Comparer par
  `comparer-releves.py`. La variante « point de montage » (D34, hors plan) reste un écart admis à
  la main.
- Le `essais/env-53-c5` de la VM garde les clones F7 de R53-1 : éviter le F7 dans C4.
- `rsync` est absent de la VM (`rapports/env-66-debian.md` §9) : les copies y sont faites par
  `tar`, alors que les scripts d'ENV-68 suivent la forme `rsync -a`. La consigne écrit la forme
  `tar` (forme de `consignes/env-66-debian.md:343-344`).
- Le hook refuse `git config` sous `depots/tiers/`, même en lecture.
- `qemu-gra2` : `graft-update` réinscrit le BSP an386 ; le retirer par `scion graft-remove`, sans
  `--purge`.
- Si des cartes passent par la VM : la NUCLEO-F429ZI peut revenir muette en Ethernet (D12, hors
  plan) ; parade de `handoff/env-50.md`.

## À la fin de l'étape
`DEVENV-STATUS.md` :
- statut ;
- versions Debian ;
- décisions PA-131 et PA-132 ;
- journal (ordre R72-1) ;
- « Prochaine action » : fin du plan, présentation de `HORS-PLAN.md`, puis révision du plan si des
  points sont retenus.

`HORS-PLAN.md` : points d'ENV-67 à ENV-71 prouvés sur la VM, ou écartés au PA-131 ; ajouter tout
point écarté pendant l'étape. Passation `handoff/env-72.md`.
