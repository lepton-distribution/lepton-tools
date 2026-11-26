# Étape EP-8 — Validation Debian groupée (EP-1 à EP-7)

## Contexte
EP-1 à EP-7 ne valident que sur le Mac. Elles changent lepton (type `projet`, génération
portable, fichier de poste, débogage, sondes, D41, D42), scion (fichiers ignorés greffables),
l'extension, le noyau (amputation de `sys/user/tauon-basic`, presets, lecteur CMake), la graine
de référence (greffon `lepton-original-tree-project`). L'étape valide l'ensemble sur la VM Debian
par un seul ordre, puis regreffe les rootstocks d'essai du Mac. Forme : celle d'ENV-72
(`doc/devenv/etapes/ENV-72-validation-debian.md`). Protocole, formes des commandes, variables
d'environnement, contrôle Mac de la consigne, invites simultanées (D39) :
`doc/devenv/ORCHESTRATION.md` §2bis, par référence. Archétype : infrastructure. Cette validation
clôt le plan.

## Prérequis
- EP-1 à EP-7 terminées et poussées, ou abandonnées par décision consignée.
- VM Debian 13 avec sa session Claude Code (`doc/devenv/ORCHESTRATION.md` §2).
- État laissé sur la VM par R72-1 : `doc/devenv/handoff/env-72.md` et
  `doc/devenv/rapports/env-72-debian.md` (outils, règles `allow`, rootstocks d'essai,
  `~/tmp-pytest`). À relire avant d'écrire la consigne ; ne pas le supposer.
- Références : consigne `doc/devenv/consignes/env-72-debian.md` ; oracle Debian
  `doc/devenv/rapports/oracles/env-72-debian/` ; rapports et oracles d'EP-1 à EP-7.
- Outils : `doc/devenv/rapports/env-57-mac/regreffer-essai.sh` et `decisions.py`,
  `scripts/comparer-releves.py`, `ls-remote.sh` d'ENV-72 (`doc/devenv/rapports/env-72-mac/`).
- Branches lepton-tools : `espace-projet/ep-8` (Mac), `espace-projet/ep-8-debian` (VM).

## Tâches

### 1. Préparation (Mac) → PA-E16
- Rapport Mac `doc/espace-projet/rapports/ep-8-mac.md` : préparation, journal des messages §2bis,
  contrôle du rapport VM.
- Attendus versionnés dans `rapports/ep-8-mac/attendu/`, relevés avec le lepton et le scion
  publiés (contrôle Mac de la consigne, §2bis).
- Têtes publiées relevées par `ls-remote.sh`, repris d'ENV-72 avec le nouveau dépôt et le nouveau
  tag de scion.
- Consigne `doc/espace-projet/consignes/ep-8-debian.md` :
  - **§0, préalable (utilisateur), avant l'ordre** : `switch` du dépôt lepton-tools de la VM sur
    `espace-projet/ep-8` ; variables d'environnement selon le §2bis ; session Claude Code
    relancée, son nom communiqué à la session Mac.
  - Critères numérotés, à arrêter au PA-E16 :
    - **C1** — versions : scion, lepton, extension (par `install-debian.sh` et
      `install-vscodium.sh`), git, Claude Code ; variables d'environnement. C1 précède les autres.
    - **C2** — règles et hook : réglages utilisateur relus ; décisions relevées par
      `decisions.py` ; toute invite à refuser annoncée « À REFUSER ».
    - **C3** — regreffe des rootstocks d'essai de la VM : noyau amputé, greffon `lepton-basic`
      pour ceux qui suivent la graine de référence ; sort de ceux à graine `project/` selon le
      PA-E2. Avant toute regreffe, relever la branche de chaque clone et de la graine clonée.
      Après : `CONFORME`, `lepton check` code 0, écarts de liens expliqués.
      `<À CONFIRMER au PA-E16>`.
    - **C4** — scion (EP-2) : fixtures avec et sans déclaration ; `pytest` complet de
      lepton-tools (`venv-test`, `--basetemp`, `--junitxml`).
    - **C5** — lepton : projet neuf par `seed new` avec greffon `projet` (EP-1) ; `generate`
      portable (EP-4) : espace sans chemin absolu, copie du rootstock sans `build/` valable sans
      régénération,
      outils de Debian (`clangd-19`, `gdb-multiarch`) ; D41 et D42 (EP-7) ; comparaison aux
      attendus du Mac par `comparer-releves.py`.
    - **C6** — hôte et 16 presets contre `oracles/env-72-debian/` : binaires identiques
      attendus ; `mklepton-empreintes.sha256` et `net.ping_ftpd` selon le PA-E6 (T10) ; tout
      autre écart expliqué.
    - **C7** — extension par `install-vscodium.sh` ; si l'utilisateur a accès à l'interface de
      la VM : espace généré à la racine ouvert par la ligne de commande et par le gestionnaire de
      fichiers (dossiers résolus), retouche par l'interface puis `generate` selon le PA-E8
      (décision du PA-E1).
      `<À CONFIRMER au PA-E16>`.
    - **C8** — cartes et sondes sur la VM (EP-5, EP-6 ; `lsusb`). `<À CONFIRMER au PA-E16>`.
    - **C9** — nettoyage par `scripts/supprimer-essai.sh`. `<À CONFIRMER au PA-E16>`.
  - Paragraphe « Communication » : nom de la session principale, ID `REP8-1`, remise en échec.
  - Invites (D39) : la consigne liste les critères qui présentent une invite et fait envoyer un
    `AVANCEMENT` « fin des invites de la VM » ; la session Mac ne lance aucune commande à invite
    avant cet `AVANCEMENT` ou le `FIN-*`.
- **PA-E16** : l'utilisateur valide la consigne et les critères, le §0, le push
  d'`espace-projet/ep-8` (PA-P), puis l'envoi de l'ordre `REP8-1`.

### 2. Exécution (VM)
La session VM suit la consigne : `ACCUSÉ`, un `AVANCEMENT` par critère et à chaque attente de
l'utilisateur, `FIN-SUCCÈS` ou `FIN-ÉCHEC`. Elle écrit `rapports/ep-8-debian.md` et son oracle sur
`espace-projet/ep-8-debian`, puis les pousse (PA-P). Elle ne développe pas.

### 3. Rootstocks d'essai (Mac)
- Regreffer, sur accord (PA-P), les rootstocks d'essai du Mac qui greffent une tête changée par
  le chantier ; liste et procédure : `doc/devenv/etapes/ENV-72-validation-debian.md` tâche 3 et
  `doc/devenv/rapports/env-57-mac.md` §4, complétées des essais gardés par ce chantier. Commencer
  après l'`AVANCEMENT` « fin des invites de la VM » ou le `FIN-*`.
- Puis `lepton check` et `generate` sur chacun ; codes attendus relevés avant la regreffe.

### 4. Clôture → PA-E17
- Session Mac : vérifier le rapport VM contre la consigne, critère par critère et commit par
  commit cité ; refaire les comparaisons sur les relevés poussés.
- **PA-E17** : fusion d'`espace-projet/ep-8-debian` dans `espace-projet/ep-8`, puis dans `main` ;
  push (PA-P). Fin du plan : présenter `HORS-PLAN.md` ligne par ligne (traiter, garder hors plan,
  abandonner) et l'état des tensions T1 à T11.

## Critères de validation
- [ ] PA-E16 et PA-E17 tranchés et consignés.
- [ ] `FIN-SUCCÈS REP8-1` vérifié par la session Mac ; C1 à C9 conformes, ou écartés au PA-E16.
- [ ] Binaires Debian de l'hôte et des 16 presets identiques à `oracles/env-72-debian/` ;
      empreintes de mklepton et `net.ping_ftpd` conformes au PA-E6 ; autres écarts expliqués et
      acceptés.
- [ ] Aucune invite simultanée Mac et VM ; toute confirmation par erreur consignée.
- [ ] Rootstocks d'essai du Mac regreffés : 0 lien cassé, 0 fichier régulier (hors `.DS_Store`
      tolérés) ; `check` aux codes attendus.
- [ ] Fin du plan : `HORS-PLAN.md` présenté à l'utilisateur pour décision.

## Pièges connus
- Sur la VM, git écrit en français, avec une espace insécable dans « fatal : » : comparer par
  `comparer-releves.py`.
- `rsync` est absent de la VM : la consigne écrit les copies en `tar` (forme de
  `doc/devenv/consignes/env-72-debian.md`).
- Les copies d'essai faites par `tar` gardaient les chemins de l'original (D45) : après EP-4, ce
  constat doit disparaître ; le vérifier en C5 plutôt que le supposer.
- Le hook refuse `git config` sous `depots/tiers/`, même en lecture.
- Un rootstock de la VM resté à l'ancien scion ne lit pas la déclaration d'EP-2 : C1 d'abord.
- Si des cartes passent par la VM : NUCLEO-F429ZI muette en Ethernet possible (D12 du hors-plan
  d'ENV ; parade de `doc/devenv/handoff/env-50.md`).

## À la fin de l'étape
`STATUS.md` : statut, versions Debian, décisions PA-E16 et PA-E17, journal (ordre `REP8-1`),
« Prochaine action » : fin du plan, puis révision du plan si des points sont retenus.
`HORS-PLAN.md` : points prouvés sur la VM ou écartés au PA-E16 ; tout point écarté pendant
l'étape. Passation `handoff/ep-8.md`.
