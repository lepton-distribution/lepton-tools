# Étape ENV-53 — Validation Debian groupée (ENV-51, ENV-52)

## Contexte
ENV-51 et ENV-52 ne valident que sur le Mac. Elles changent :
- lepton : relais des messages de scion (ENV-51, D10) ;
- scion : extraction partielle des clones projetés (ENV-52, D11), nouvelle version ;
- les clones projetés des rootstocks ; les liens du trunk, les contenus projetés et les binaires ne
  doivent pas changer.

Cette étape valide l'ensemble sur la VM Debian, par un seul ordre (§2bis), puis regreffe les
rootstocks d'essai du Mac. Forme : celle d'ENV-50. Archétype : infrastructure. Décision de
l'utilisateur (révision du 2026-11-12) : cette validation Debian clôt le plan.

## Prérequis
- ENV-51 et ENV-52 terminées et poussées.
- VM Debian 13 avec sa session Claude Code (ORCHESTRATION §2) ; protocole §2bis, remise en échec
  comprise.
- Consigne de référence : `consignes/env-50-debian.md`. Rapports de référence :
  `rapports/env-50-debian.md`, `rapports/env-50-mac.md`. Oracle Debian de référence :
  `rapports/oracles/env-50-debian/`.
- Règles des consignes VM (ORCHESTRATION §2bis) : régénérer avant de relever ; clonages,
  installations `pipx`, suppressions et `graft-update` confiés à l'utilisateur dès la consigne.
- État laissé sur la VM par R50-1 (`handoff/env-50.md`) : scion 0.6.2.0, lepton 0.1.0 ;
  `essais/env-28-debian` et `essais/env-13-debian` regreffés ; `essais/env-50-debian` neuf ;
  `essais/env-11/qemu` ; journaux `~/env-50-journaux`, `~/tmp-pytest`.
- Passations `handoff/env-51.md` et `handoff/env-52.md` : forme du relais (PA-89), forme de
  l'extraction et sort des clones existants (PA-91).
- Branches lepton-tools : `devenv/env-53` (Mac), `devenv/env-53-debian` (VM).

## Tâches

### 1. Préparation (Mac) → PA-93
- Rapport Mac `rapports/env-53-mac.md` : préparation, puis journal des messages §2bis, contrôle du
  rapport VM.
- Oracle Mac de référence : le dernier (`env-49-apres`, ou celui d'ENV-52 s'il le remplace).
- Attendus versionnés dans `rapports/env-53-mac/attendu/` :
  - liste `chemin -> cible` (aucun changement attendu depuis R50-1), casse comprise ;
  - fichiers extraits par clone projeté, selon le PA-91 ;
  - sortie attendue d'une commande de lepton qui relaie un message de scion (PA-89).
- Têtes publiées relevées par `git ls-remote` : lepton-tools, `seed.scions` (tag), noyau si
  `SCION_REF` a changé, familles F4, F7, WL, graine, 8 miroirs.
- Consigne `consignes/env-53-debian.md`, critères numérotés :
  - **C1** — versions : scion d'ENV-52, lepton, extension, chaîne APT, git. Installation par
    l'utilisateur, en clair dans la consigne, avant toute regreffe. La commande de conversion des
    clones, si le PA-91 en crée une, est aussi confiée à l'utilisateur (refus du classifieur de la
    VM, R28-1).
  - **C2** — regreffe d'`essais/env-28-debian` par l'utilisateur, selon le PA-91 :
    - branche de chaque clone relevée avant (§2bis, « Branche des clones ») ;
    - liste des chemins identique à l'attendu, casse comprise ; contenu projeté identique aux
      commits épinglés ;
    - fichiers extraits par clone conformes à l'attendu ; tailles avant et après ; relevés par
      `git ls-files -t`, `find -type f`, `cat .git/info/sparse-checkout` ;
    - `core.ignoreCase` de chaque clone projeté relevé (comparé au Mac).
    Puis un rootstock neuf `essais/env-53-debian` : aucun lien cassé, aucun fichier régulier,
    nombre de liens celui de `<ROOTSTOCK>` du Mac, clones neufs partiels et leur taille.
  - **C3** — host et les 16 presets ; `comparer-oracle.py` contre `env-50-debian` : code 0, ou
    écarts admis au PA-93 ; fumée et KAL QEMU identiques.
  - **C4** — regreffe d'`essais/env-13-debian` et d'`essais/env-50-debian` par l'utilisateur,
    branche de chaque clone relevée avant (§2bis) ; `lepton check` code 0.
  - **C5** — lepton : `pytest` complet ; relais des messages de scion constaté sur un rootstock
    d'essai à graine de projet (forme de l'essai d'ENV-51) : <À CONFIRMER au PA-93>.
  - **C6** — `scion mirror-sync --dry-run` sur les 8 miroirs : 0 à envoyer. Une référence « à
    envoyer » n'est admise que si une publication amont postérieure l'explique (`git ls-remote`).
  - **C7** — cartes sur la VM : <À CONFIRMER au PA-93> (aucun binaire changé attendu).
  - **C8** — nettoyage, si l'utilisateur l'accorde : <À CONFIRMER au PA-93>.
- La consigne donne en clair les commandes confiées à l'utilisateur, et un paragraphe
  « Communication » : nom de la session principale, ID `R53-1`, conduite quand un message n'est pas
  remis (§2bis, « Remise en échec »).
- **PA-93** : l'utilisateur valide la consigne, C3 (écarts admis), C5, les cartes, le nettoyage et
  le sort d'`essais/env-39-copie` (tâche 3) ; push de `devenv/env-53` (PA-P) ; ordre `R53-1` à la
  session VM.

### 2. Exécution (VM)
La session VM suit la consigne :
- elle envoie un `ACCUSÉ`, puis un `AVANCEMENT` par critère et par attente de l'utilisateur ;
- elle termine par `FIN-SUCCÈS` ou `FIN-ÉCHEC` ;
- son rapport `rapports/env-53-debian.md` et son oracle `rapports/oracles/env-53-debian/` sont
  écrits sur `devenv/env-53-debian`, puis poussés.

### 3. Rootstocks d'essai (Mac)
- Regreffe des rootstocks d'essai, sur accord (PA-P), selon la procédure de
  `rapports/env-50-mac.md` §4. Toujours : les rootstocks à clones projetés `essais/env-13-vierge`,
  `essais/env-11/f429zi`, `essais/env-11/wl55jc1`. `essais/env-9`, `essais/env-11/qemu`,
  `essais/env-11/qemu-gra2`, `essais/env-11/bout-en-bout/rootstock` (aucun clone projeté) :
  seulement si une tête qu'ils greffent a changé depuis R50-1 (`git ls-remote` de la tâche 1).
  Relever d'abord la branche de chaque clone.
- Rootstocks à clones projetés (`env-13-vierge`, `env-11/f429zi`, `env-11/wl55jc1`) : fichiers
  extraits et tailles, avant et après.
- Puis `lepton check` et `generate` : code 0 (`qemu-gra2` : 1, attendu).
- Sort d'`essais/env-39-copie` (copie d'essai d'ENV-39, 2 clones projetés) : <À CONFIRMER au PA-93>.

### 4. Clôture → PA-94
- Session Mac : vérifier le rapport VM contre la consigne (chaque critère, commits cités) ; refaire
  les comparaisons sur l'oracle poussé.
- **PA-94** : fusion de `devenv/env-53-debian` dans `devenv/env-53`, puis dans `main` ; push
  (PA-P).

## Critères de validation
- [ ] PA-93 et PA-94 tranchés et consignés.
- [ ] `FIN-SUCCÈS R53-1` vérifié par la session Mac ; C1 à C8 conformes, ou écartés au PA-93.
- [ ] Rootstocks d'essai regreffés : 0 lien cassé, 0 fichier régulier (hors `.DS_Store` tolérés) ;
      `check` code 0 (`qemu-gra2` : 1, attendu).
- [ ] Fin du plan : `HORS-PLAN.md` présenté à l'utilisateur pour décision.

## Pièges connus
- La VM distingue la casse : un ensemble extrait écrit avec une autre casse que la liste git donne
  un lien cassé sur Debian seulement ; `core.ignoreCase` peut changer la lecture des motifs de
  `sparse-checkout` entre le Mac et la VM.
- `git sparse-checkout list` n'est pas une lecture admise par le hook du Mac : relever les
  fichiers extraits par `git ls-files -t` ou `find`.
- Un rootstock de la VM resté en scion 0.6.2.0 ne connaît pas l'extraction partielle : installer
  scion (C1) avant toute regreffe.
- Un écart Debian contre l'oracle Mac peut venir de la chaîne APT : comparer d'abord à
  `env-50-debian` ; écarts propres à Debian : `rapports/env-21-debian.md` §3.
- Le banc QEMU compte 19 et 15 tests sur Debian : `net.ping_ftpd` ne tourne que sous Linux.
- `qemu-gra2` : `graft-update` réinscrit le BSP an386. Le retirer par `scion graft-remove`, sans
  `--purge`.
- `lepton-env.sh` cherche le rootstock à partir de `${1:-$PWD}` : `source "$R"/…/lepton-env.sh "$R"`
  (défaut de la consigne R50-1, `handoff/env-50.md`).
- Si des cartes passent par la VM : la NUCLEO-F429ZI peut revenir muette en Ethernet (D12, hors
  plan) ; parade de `handoff/env-50.md` (débranchement, nouveau rattachement, câble).
- Le nom du rootstock neuf garde la longueur d'`essais/env-50-debian` (chemins `__FILE__`,
  `rapports/env-43-mac.md` §1.6).
- Si la VM bloque un clonage, une suppression, une installation ou `graft-update`, ne pas contourner
  le refus : l'utilisateur lance la commande.

## À la fin de l'étape
`DEVENV-STATUS.md` :
- statut ;
- versions Debian ;
- décisions PA-93 et PA-94 ;
- journal (ordre R53-1) ;
- « Prochaine action » : fin du plan, présentation de `HORS-PLAN.md`, puis révision du plan si des
  points sont retenus.

`HORS-PLAN.md` : ajouter tout point écarté pendant l'étape. Passation `handoff/env-53.md`.
