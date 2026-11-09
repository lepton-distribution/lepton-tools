# Étape ENV-50 — Validation Debian groupée (ENV-44 à ENV-49)

## Contexte
ENV-44 à ENV-49 ne valident que sur le Mac. Elles changent :
- les fichiers greffés : SPL F4 retirée (ENV-46) ; HAL et CMSIS device F7 (ENV-47) et code tiers WL
  (ENV-48) projetés depuis des miroirs ;
- les binaires : an386 si D5 est retenu (ENV-44) ; WL55 (ENV-49) ;
- la configuration OpenOCD des BSP de carte (ENV-45) ;
- le hook, les scripts et le protocole entre sessions (ENV-44) ;
- éventuellement scion (correctif décidé au PA-75 ou au PA-83).

Cette étape valide l'ensemble sur la VM Debian, par un seul ordre (§2bis), puis regreffe les
rootstocks d'essai du Mac. Forme : celle d'ENV-43. Archétype : infrastructure.

Elle traite aussi D8 de `HORS-PLAN.md` : la regreffe d'`essais/env-13-debian` sur la VM.

## Prérequis
- ENV-44 à ENV-49 terminées et poussées.
- VM Debian 13 avec sa session Claude Code (ORCHESTRATION §2) ; protocole §2bis, avec l'amendement
  D9 d'ENV-44 (relais par l'utilisateur).
- Consigne de référence : `consignes/env-43-debian.md`. Rapports de référence :
  `rapports/env-43-debian.md`, `rapports/env-43-mac.md`. Oracle Debian de référence :
  `rapports/oracles/env-43-debian/`.
- Règles des consignes VM (ORCHESTRATION §2bis) : régénérer avant de relever ; clonages,
  installations `pipx`, suppressions et `graft-update` confiés à l'utilisateur dès la consigne.
- État laissé sur la VM par R43-1 : scion 0.6.1.0 ; `essais/env-28-debian`, `essais/env-43-debian`
  à jour ; `essais/env-13-debian` non regreffé.
- Passations `handoff/env-47.md` et `handoff/env-48.md` : rootstocks et graines à regreffer.
- Branches lepton-tools : `devenv/env-50` (Mac), `devenv/env-50-debian` (VM).

## Tâches

### 1. Préparation (Mac) → PA-87
- Rapport Mac `rapports/env-50-mac.md` : préparation, puis journal des messages §2bis (ORDRE,
  ACCUSÉ, FIN-*, messages relayés), contrôle du rapport VM.
- Oracle Mac de référence : le dernier (ENV-49).
- Écarts Mac `env-42-apres` → oracle de référence : ils fixent l'attendu contre `env-43-debian`.
- Attendus versionnés dans `rapports/env-50-mac/attendu/` :
  - liens ajoutés et retirés depuis R43-1 (SPL retirée, F7 et WL projetés, montée WL) ;
  - liste `chemin -> cible`, casse comprise ;
  - écarts de symboles.
- Têtes publiées relevées par `git ls-remote` : familles F4, F7, WL ; BSP touchés ; noyau ; graine ;
  `seed.scions` (tag) ; miroirs F4, F7, WL.
- Consigne `consignes/env-50-debian.md`, critères numérotés :
  - **C1** — versions : scion en vigueur après ENV-49, lepton, extension, chaîne APT. Installation
    par l'utilisateur, en clair dans la consigne (forme de C1 en R43-1), de lepton, de scion s'il a
    changé et de l'extension, avant toute regreffe.
  - **C2** — `graft-update` de `essais/env-28-debian`, lancé par l'utilisateur :
    - branche de chaque clone relevée avant (§2bis, « Branche des clones ») ;
    - 0 conflit ;
    - clones tiers F7 et WL créés depuis les miroirs, à la révision épinglée ;
    - liste des chemins conforme à l'attendu, casse comprise ;
    - contenu projeté F7 et WL identique aux commits épinglés (équivalent de C4 en R43-1).
    Puis un rootstock neuf : aucun lien cassé, aucun fichier régulier, nombre de liens celui de
    `<ROOTSTOCK>` du Mac.
  - **C3** — host et les 16 presets ; `comparer-oracle.py` contre `env-43-debian` : écarts conformes
    à l'attendu ; fumée et KAL QEMU identiques.
  - **C4** — regreffe d'`essais/env-13-debian` (D8), lancée par l'utilisateur ; `lepton check`
    code 0.
  - **C5** — hook et scripts d'ENV-44 sur Debian, selon le PA-75 : <À CONFIRMER au PA-87>.
  - **C6** — `scion mirror-sync --dry-run` sur les miroirs F4, F7 et WL : 0 à envoyer. Une référence
    « à envoyer » n'est admise que si une publication amont postérieure à la dernière synchronisation
    l'explique (`git ls-remote` de l'amont).
  - **C7** — cartes sur la VM et choix de la sonde par numéro (ENV-45) : <À CONFIRMER au PA-87>.
  - **C8** — nettoyage, si l'utilisateur l'accorde : <À CONFIRMER au PA-87>.
- La consigne donne en clair les commandes confiées à l'utilisateur, et un paragraphe
  « Communication » : nom de la session principale, ID `R50-1`, conduite quand un message n'est pas
  remis (D9).
- **PA-87** : l'utilisateur valide la consigne, les cartes et le nettoyage ; push de
  `devenv/env-50` (PA-P) ; ordre `R50-1` à la session VM.

### 2. Exécution (VM)
La session VM suit la consigne :
- elle envoie un `ACCUSÉ`, puis un `AVANCEMENT` par critère et par attente de l'utilisateur ;
- elle termine par `FIN-SUCCÈS` ou `FIN-ÉCHEC` ;
- son rapport `rapports/env-50-debian.md` et son oracle `rapports/oracles/env-50-debian/` sont
  écrits sur `devenv/env-50-debian`, puis poussés.

### 3. Rootstocks d'essai (Mac)
- `scion graft-update` des 7 rootstocks d'essai, sur accord (PA-P), selon la procédure de
  `rapports/env-28-mac.md` §3. Relever d'abord la branche de chaque clone.
- Rootstocks qui greffent les familles F7 ou WL (`env-11/wl55jc1` au moins) : clones tiers créés
  depuis les miroirs.
- `env-11/f429zi` et `env-11/wl55jc1` : construction comprise.
- Puis `lepton check` et `generate` : code 0 (`qemu-gra2` : 1, attendu).

### 4. Clôture → PA-88
- Session Mac : vérifier le rapport VM contre la consigne (chaque critère, commits cités) ; refaire
  les comparaisons sur l'oracle poussé.
- **PA-88** : fusion de `devenv/env-50-debian` dans `devenv/env-50`, puis dans `main` ; push
  (PA-P).

## Critères de validation
- [ ] PA-87 et PA-88 tranchés et consignés.
- [ ] `FIN-SUCCÈS R50-1` vérifié par la session Mac ; C1 à C8 conformes, ou écartés au PA-87.
- [ ] `essais/env-13-debian` regreffé (D8).
- [ ] Rootstocks d'essai regreffés : 0 lien cassé, 0 fichier régulier (hors `.DS_Store` tolérés) ;
      `check` code 0 (`qemu-gra2` : 1, attendu).

## Pièges connus
- La VM distingue la casse : c'est ici que se prouve le renommage `Inc` → `inc` du WL (ENV-48).
- Un rootstock de la VM resté en scion antérieur ne sait pas lire les porteurs F7 et WL : installer
  scion (C1) avant tout `graft-update` (piège d'ENV-43).
- Un écart Debian contre l'oracle Mac peut venir de la chaîne APT : comparer d'abord à
  `env-43-debian`. Les écarts propres à Debian sont décrits dans `rapports/env-21-debian.md` §3.
- `.text` multiple de 64 sur Debian : un écart de quelques octets peut disparaître ou apparaître
  par bourrage (E-1 de R43-1).
- Le banc QEMU compte 19 et 15 tests sur Debian : `net.ping_ftpd` ne tourne que sous Linux.
- `qemu-gra2` : `graft-update` réinscrit le BSP an386. Le retirer par `scion graft-remove`, sans
  `--purge`.
- Si la VM bloque un clonage, une suppression, une installation ou `graft-update`, ne pas contourner
  le refus : l'utilisateur lance la commande.
- Le nom `essais/env-43-debian` a été imposé par la longueur des chemins `__FILE__` : un nouveau
  rootstock neuf garde un nom de même longueur (`rapports/env-43-mac.md` §1.6).

## À la fin de l'étape
`DEVENV-STATUS.md` :
- statut ;
- versions Debian ;
- décisions PA-87 et PA-88 ;
- journal (ordre R50-1) ;
- « Prochaine action » : révision du plan, en partant de `HORS-PLAN.md`.

`HORS-PLAN.md` : D8. Passation `handoff/env-50.md`.
