# Étape ENV-57 — Validation Debian groupée (ENV-54, ENV-55, ENV-56)

## Contexte
ENV-54, ENV-55 et ENV-56 ne valident que sur le Mac. Elles changent :
- les règles de permission de Claude Code (ENV-54, D16). Les refus du classifieur ont surtout
  touché la VM (`rapports/env-53-debian.md` §7, écart 2) ;
- lepton : URL `file:///` (ENV-55, D13) ;
- scion : répertoires laissés par un clonage en échec (ENV-56, D14), nouvelle version.

Les liens du trunk, les clones et les binaires ne doivent pas changer. Cette étape valide
l'ensemble sur la VM Debian par un seul ordre (§2bis), puis regreffe au besoin les rootstocks
d'essai du Mac. Forme : celle d'ENV-53. Archétype : infrastructure. Décision de l'utilisateur
(révision du 2026-11-12) : cette validation Debian clôt le plan.

## Prérequis
- ENV-54, ENV-55 et ENV-56 terminées et poussées.
- VM Debian 13 avec sa session Claude Code (ORCHESTRATION §2) ; protocole §2bis, remise en échec
  comprise.
- Consigne de référence : `consignes/env-53-debian.md`. Rapports de référence :
  `rapports/env-53-debian.md`, `rapports/env-53-mac.md`. Oracle Debian de référence :
  `rapports/oracles/env-53-debian/` ; oracle Mac : `rapports/oracles/env-52-apres/`.
- Règles des consignes VM : ORCHESTRATION §2bis, tel qu'amendé en ENV-54 (PA-95).
- État laissé sur la VM par R53-1 (`handoff/env-53.md`) :
  - outils : scion 0.6.3.0, lepton 0.1.0, extension 0.5.2 ;
  - `essais/env-28-debian` et `essais/env-13-debian` regreffés, clones tiers partiels ;
    `essais/env-53-debian` neuf ;
  - `essais/env-53-c5` : graine de projet de référence de la VM (D15) ; `essais/env-11/qemu` :
    à supprimer (D15) ;
  - journaux `~/env-53-journaux` ; `~/tmp-pytest`.
- Passations `handoff/env-54.md`, `handoff/env-55.md`, `handoff/env-56.md` : règles retenues
  (PA-95), forme de l'URL (PA-97), portée et version de scion (PA-99).
- Branches lepton-tools : `devenv/env-57` (Mac), `devenv/env-57-debian` (VM).

## Tâches

### 1. Préparation (Mac) → PA-101
- Rapport Mac `rapports/env-57-mac.md` : préparation, puis journal des messages §2bis, puis
  contrôle du rapport VM.
- Attendus versionnés dans `rapports/env-57-mac/attendu/`, relevés sur une copie d'essai de la
  graine de projet du Mac (forme d'`essais/env-53-c5`) :
  - sorties de lepton pour les formes d'origine du PA-97 (D13) ;
  - `seed add` en échec, sans répertoire résiduel (D14) ;
  - liste `chemin -> cible` : aucun changement attendu depuis R53-1.
- Têtes publiées relevées par `git ls-remote`, comme `rapports/env-53-mac/ls-remote.sh` :
  lepton-tools, `seed.scions` (tag), noyau et autres greffons, graine, 8 miroirs. Elles décident
  C3 et la tâche 3.
- Consigne `consignes/env-57-debian.md`, critères numérotés :
  - **C1** — versions : scion d'ENV-56, lepton, extension, git, Claude Code de la VM. Les
    installations (`pipx install`) sont lancées par la session VM selon les règles d'ENV-54. La
    commande `pipx` de scion est donnée en clair : si `SCION_REF` n'a pas changé au PA-99,
    `install-debian.sh` installe encore 0.6.3.0. Pour chaque commande, la consigne prévoit la
    conduite en cas de refus : un `AVANCEMENT`, puis l'utilisateur lance la commande.
  - **C2** — D16 sur la VM. Chaque catégorie retenue au PA-95 est lancée par la session VM, et le
    résultat (acceptée ou refusée, motif) est journalisé. Catégories : `scion graft-update`,
    `rm -rf` dans les essais, `pipx install`, `git clone`, tests. Ajouter :
    - les contrôles négatifs d'ENV-54, sur des cibles absentes ;
    - le contrôle vivant du hook : une écriture shell sous le `trunk/` d'un rootstock d'essai
      est refusée.
  - **C3** — regreffe d'`essais/env-28-debian` et d'`essais/env-13-debian` si une tête qu'ils
    greffent a changé (noyau si `SCION_REF` a changé) : <À CONFIRMER au PA-101>. Avant toute
    regreffe, relever la branche de chaque clone (§2bis). Après : liens inchangés, `CONFORME`,
    `lepton check` code 0.
  - **C4** — D13 : formes d'origine du PA-97 sur une copie d'`essais/env-53-c5`, comparées à
    l'attendu du Mac.
  - **C5** — D14 : `seed add` en échec sur la même copie, sans répertoire résiduel ; liens et
    graine égaux à l'avant ; `pytest` complet de lepton-tools.
  - **C6** — host et 16 presets contre `env-53-debian`, et `mirror-sync --dry-run` :
    <À CONFIRMER au PA-101 : aucun binaire changé attendu>.
  - **C7** — cartes sur la VM : <À CONFIRMER au PA-101>.
  - **C8** — nettoyage : `essais/env-11/qemu`, journaux `~/env-53-journaux`, rootstocks et copies
    devenus inutiles. D15 confie la suppression d'`essais/env-11/qemu` à l'utilisateur ; la
    session VM ne lance une suppression que si les règles d'ENV-54 le permettent et que
    l'utilisateur l'accorde : <À CONFIRMER au PA-101>.
- Lecture des règles par la VM : <À CONFIRMER au PA-101>. À trancher :
  - si le PA-95 a retenu un fichier propre à chaque hôte, qui le pose sur la VM. Proposition :
    l'utilisateur, d'après le texte exact donné dans la consigne. La VM n'écrit que son rapport
    (ORCHESTRATION §2) ;
  - si la session VM est relancée après le `switch` sur `devenv/env-57`, avant C2, puisque les
    réglages sont lus au démarrage ;
  - la conduite §2bis qui en découle : nouvel `ACCUSÉ`, nom de la session.
- La consigne contient un paragraphe « Communication » : nom de la session principale, ID
  `R57-1`, conduite quand un message n'est pas remis (§2bis, « Remise en échec »).
- **PA-101** : l'utilisateur valide :
  - la consigne et les critères C3, C6, C7, C8 ;
  - la lecture des règles par la VM ;
  - le push de `devenv/env-57` (PA-P) et l'envoi de l'ordre `R57-1` à la session VM.

### 2. Exécution (VM)
La session VM suit la consigne :
- elle envoie un `ACCUSÉ`, puis un `AVANCEMENT` par critère et à chaque attente de l'utilisateur ;
- elle termine par `FIN-SUCCÈS` ou `FIN-ÉCHEC` ;
- elle écrit son rapport `rapports/env-57-debian.md`, et son oracle si C6 en produit un, sur
  `devenv/env-57-debian`, puis les pousse (PA-P).

### 3. Rootstocks d'essai (Mac)
- Regreffer, sur accord (PA-P), les rootstocks d'essai qui greffent une tête changée depuis R53-1
  (`git ls-remote` de la tâche 1). Procédure : `rapports/env-53-mac.md` §4, script
  `rapports/env-53-mac/regreffer-essai.sh`.
- Commandes lancées par la session selon les règles d'ENV-54. Consigner chaque refus éventuel.
- Puis `lepton check` et `generate` : code 0 (`qemu-gra2` : 1, attendu).

### 4. Clôture → PA-102
- Session Mac : vérifier le rapport VM contre la consigne (chaque critère, commits cités) ;
  refaire les comparaisons sur les relevés poussés.
- **PA-102** : fusion de `devenv/env-57-debian` dans `devenv/env-57`, puis dans `main` ; push
  (PA-P).

## Critères de validation
- [ ] PA-101 et PA-102 tranchés et consignés.
- [ ] `FIN-SUCCÈS R57-1` vérifié par la session Mac ; C1 à C8 conformes, ou écartés au PA-101.
- [ ] D16 : journal des commandes lancées par la session VM (acceptées, refusées) au rapport.
- [ ] Rootstocks d'essai regreffés, s'il y a lieu : 0 lien cassé, 0 fichier régulier (hors
      `.DS_Store` tolérés) ; `check` code 0 (`qemu-gra2` : 1, attendu).
- [ ] Fin du plan : `HORS-PLAN.md` présenté à l'utilisateur pour décision.

## Pièges connus
- Le classifieur de la VM peut refuser ce que celui du Mac accepte, et sa version de Claude Code
  peut différer. Ne jamais contourner un refus : `AVANCEMENT`, puis l'utilisateur lance la
  commande.
- La graine de projet de référence de la VM est `essais/env-53-c5`, pas `essais/env-11/qemu`,
  jamais regreffé depuis ENV-10 (D15). Relever l'état d'un rootstock de la VM avant d'en tirer un
  attendu.
- Sur la VM, git écrit ses messages en français : normaliser ou exclure ces lignes dans les
  comparaisons de sorties (`rapports/env-53-debian.md` §5.2).
- D14 dépend du scion installé, pas de l'état du rootstock : tant que la VM a scion 0.6.3.0, le
  défaut reste. Installer scion (C1) avant tout essai de C5.
- Le `essais/env-53-c5` de la VM garde les clones F7 de R53-1 (`seed remove` conserve les
  clones). Un attendu du Mac relevé sur une copie neuve diffère si l'essai touche au F7 : éviter
  le F7 dans C4 et C5, ou en tenir compte dans l'attendu.
- Le hook refuse `git config` sous `depots/tiers/`, même en lecture : lire `.git/config.worktree`,
  puis `.git/config`, par `grep` (`handoff/env-53.md`).
- `qemu-gra2` : `graft-update` réinscrit le BSP an386. Le retirer par `scion graft-remove`, sans
  `--purge`.
- `lepton-env.sh` cherche le rootstock à partir de `${1:-$PWD}` : `source "$R"/…/lepton-env.sh "$R"`.
- Si des cartes passent par la VM : la NUCLEO-F429ZI peut revenir muette en Ethernet (D12, hors
  plan) ; parade de `handoff/env-50.md`.
- Un rootstock neuf garde la longueur de chemin d'`essais/env-53-debian` (chemins `__FILE__`,
  `rapports/env-43-mac.md` §1.6).

## À la fin de l'étape
`DEVENV-STATUS.md` :
- statut ;
- versions Debian ;
- décisions PA-101 et PA-102 ;
- journal (ordre R57-1) ;
- « Prochaine action » : fin du plan, présentation de `HORS-PLAN.md`, puis révision du plan si des
  points sont retenus.

`HORS-PLAN.md` : ajouter tout point écarté pendant l'étape. Passation `handoff/env-57.md`.
