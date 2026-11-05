# Étape ENV-43 — Validation Debian groupée (ENV-37 à ENV-42)

## Contexte
ENV-37 à ENV-42 ne valident que sur le Mac. Elles changent :
- les fichiers greffés : provenance du WL (ENV-37) ; HAL et CMSIS device F4 projetés depuis des
  dépôts tiers au lieu d'être copiés dans la famille (ENV-41) ;
- l'outil : scion avec la projection et le miroir (ENV-39, ENV-40) ;
- éventuellement les binaires des presets Cortex-M4, selon le PA-71 (ENV-42).

Cette étape valide l'ensemble sur la VM Debian, par un seul ordre (§2bis). Elle regreffe ensuite
les rootstocks d'essai du Mac. Forme : celle d'ENV-36. Archétype : infrastructure.

Point propre à cette validation : la VM distingue la casse des noms de fichiers, et un rootstock
neuf y clone des dépôts tiers depuis les miroirs.

## Prérequis
- ENV-37 à ENV-42 terminées et poussées.
- VM Debian 13, avec sa session Claude Code (ORCHESTRATION §2) ; protocole §2bis.
- Consigne de référence : `consignes/env-36-debian.md`. Rapports de référence :
  `rapports/env-36-debian.md`, `rapports/env-36-mac.md`. Oracle Debian de référence :
  `rapports/oracles/env-36-debian/`.
- Règles des consignes VM (ORCHESTRATION §2bis) : régénérer avant de relever ; clonages,
  installations `pipx`, suppressions et `graft-update` confiés à l'utilisateur dès la consigne.
- État laissé sur la VM par R36-1 : `essais/env-28-debian`, `essais/env-36-debian`,
  `essais/env-11/qemu`, `~/env-36-journaux`.
- `handoff/env-41.md` : liste des graines de projet qui référencent `family-stm32f4xx`.
- Branches lepton-tools : `devenv/env-43` (Mac), `devenv/env-43-debian` (VM).

## Tâches

### 1. Préparation (Mac) → PA-73
- Oracle Mac de référence : le dernier (ENV-42, ou ENV-41 si le PA-71 n'a rien changé).
- Écarts Mac `env-35-apres` → oracle de référence (`comparer-oracle.py`). Ils fixent l'attendu de
  la comparaison contre `env-36-debian` : aucun écart hors des presets visés au PA-71.
- Attendus versionnés dans `rapports/env-43-mac/attendu/` : liens ajoutés et retirés, liste des
  chemins du trunk, écarts de symboles (précédent : `rapports/env-36-mac/attendu/`).
- Têtes publiées relevées par `git ls-remote` : famille F4, famille WL, noyau, graine,
  `seed.scions` (tag), miroirs.
- Consigne `consignes/env-43-debian.md`, critères numérotés :
  - **C1** — versions relevées : scion (version d'ENV-39 et d'ENV-40), lepton, chaîne APT.
  - **C2** — `graft-update` d'un rootstock existant de la VM, lancé par l'utilisateur :
    - 0 conflit ;
    - clones des dépôts tiers créés depuis les miroirs, à la révision épinglée ;
    - liste des chemins du trunk conforme à l'attendu, casse comprise ;
    - puis rootstock neuf depuis la graine publiée : aucun lien cassé, aucun fichier régulier ;
    - nombre de liens fixé dans la consigne : celui de `<ROOTSTOCK>` du Mac après ENV-42.
  - **C3** — host et les 16 presets construits. `comparer-oracle.py` contre `env-36-debian` :
    écarts conformes à l'attendu. Fumée et banc KAL QEMU identiques.
  - **C4** — contenu projeté identique à l'amont, par le contrôle retenu au PA-69 ; compilation à
    blanc de la HAL F4 dans l'ordre retenu au PA-71.
  - **C5** — graine de projet existante de la VM : `check` et `generate` selon la conduite fixée
    au PA-69 pour les graines qui référencent la famille F4.
  - **C6** — commande de miroir, en lecture seule (contrôle d'un miroir contre son amont, sans
    push) : <À CONFIRMER au PA-73>.
  - **C7** — cartes sur la VM : <À CONFIRMER au PA-73>. Précédent : NUCLEO-F429ZI rattachée à la
    VM pour R36-1, trois images, écriture flash accordée (PA-11).
  - **C8** — nettoyage, si l'utilisateur l'accorde : <À CONFIRMER au PA-73>.
- La consigne donne en clair les commandes confiées à l'utilisateur, et un paragraphe
  « Communication » : nom de la session principale, ID `R43-1`.
- **PA-73** : l'utilisateur valide la consigne, les cartes et le nettoyage ; push de
  `devenv/env-43` (PA-P) ; ordre `R43-1` à la session VM.

### 2. Exécution (VM)
La session VM suit la consigne :
- elle envoie un `ACCUSÉ`, puis un `AVANCEMENT` par critère et par attente de l'utilisateur ;
- elle termine par `FIN-SUCCÈS` ou `FIN-ÉCHEC` ;
- son rapport `rapports/env-43-debian.md` et son oracle `rapports/oracles/env-43-debian/` sont
  écrits sur `devenv/env-43-debian`, puis poussés.

### 3. Rootstocks d'essai (Mac)
- `scion graft-update` des 7 rootstocks d'essai, sur accord (PA-P), selon la procédure de
  `rapports/env-28-mac.md` §3. Relever d'abord la branche de chaque clone.
- Graines de projet qui référencent `family-stm32f4xx` (`env-11/f429zi` au moins) : appliquer la
  conduite du PA-69 avant la regreffe.
- `env-11/f429zi` : construction `nucleo-f429zi-embos` comprise.
- Puis `lepton check` et `generate` : code 0 (`qemu-gra2` : 1, attendu).

### 4. Clôture → PA-74
- Session Mac : vérifier le rapport VM contre la consigne (chaque critère, commits cités) et
  refaire les comparaisons sur l'oracle poussé.
- **PA-74** : fusion de `devenv/env-43-debian` dans `devenv/env-43`, puis dans `main` ; push
  (PA-P).

## Critères de validation
- [ ] PA-73 et PA-74 tranchés et consignés.
- [ ] `FIN-SUCCÈS R43-1` vérifié par la session Mac ; C1 à C8 conformes, ou écartés au PA-73.
- [ ] Rootstocks d'essai regreffés : 0 lien cassé, 0 fichier régulier (hors `.DS_Store`
      tolérés) ; `check` code 0 (`qemu-gra2` : 1, attendu).

## Pièges connus
- Un écart Debian contre l'oracle Mac peut venir de la chaîne APT : comparer d'abord à
  `env-36-debian`. Les écarts propres à Debian sont décrits dans `rapports/env-21-debian.md` §3.
- Le banc QEMU compte 19 et 15 tests sur Debian : `net.ping_ftpd` ne tourne que sous Linux.
- `qemu-gra2` : `graft-update` réinscrit le BSP an386. Le retirer par `scion graft-remove`, sans
  `--purge`.
- Si la VM bloque un clonage, une suppression, une installation ou `graft-update`, la session ne
  contourne pas le refus : l'utilisateur lance la commande.
- Un rootstock de la VM resté en scion antérieur à la projection ne sait pas lire la graine
  publiée : installer scion (C1) avant tout `graft-update`.
- Compter les liens d'un répertoire en le restreignant à la famille visée : `cubemx_hal_driver/`
  existe aussi dans la famille WL (157 liens, défaut de la consigne de R36-1).
- La synthèse de `board_net` est dans `LastTest.log`, pas dans `board_net.log`.
- Le premier `ACCUSÉ` a été perdu deux fois (ECONNRESET, R33-1 et R36-1) : sans accusé, appliquer
  la règle du §2bis, ne rien supposer.

## À la fin de l'étape
`DEVENV-STATUS.md` :
- statut ;
- versions Debian ;
- décisions PA-73 et PA-74 ;
- journal (ordre R43-1) ;
- « Prochaine action » : révision du plan (bascule du F7 et du WL sur la projection, sujets
  restés hors plan).

Passation `handoff/env-43.md`.
