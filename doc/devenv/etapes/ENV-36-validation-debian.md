# Étape ENV-36 — Validation Debian groupée (ENV-34 et ENV-35)

## Contexte
ENV-34 et ENV-35 ne valident que sur le Mac. Elles changent :
- les fichiers greffés : `cubemx_hal_driver/` retiré, HAL v1.8.5 et CMSIS device F4 importés,
  `core_cm4.h` ajouté au noyau (ENV-34) ;
- les binaires des 4 presets F4 : passage de la SPL à la HAL (ENV-35).

Cette étape valide l'ensemble sur la VM Debian, par un seul ordre (§2bis). Elle regreffe ensuite
les rootstocks d'essai du Mac. Forme : celle d'ENV-33. Archétype : infrastructure.

## Prérequis
- ENV-34 et ENV-35 terminées et poussées.
- VM Debian 13, avec sa session Claude Code (ORCHESTRATION §2) ; protocole §2bis.
- Consigne de référence : `consignes/env-33-debian.md`. Rapports de référence :
  `rapports/env-33-debian.md`, `rapports/env-33-mac.md`.
- Règles des consignes VM (ORCHESTRATION §2bis), dont : `graft-update` confié à l'utilisateur dès
  la consigne (R28-1).
- Branches lepton-tools : `devenv/env-36` (Mac), `devenv/env-36-debian` (VM).

## Tâches

### 1. Préparation (Mac) → PA-59
- Oracle Mac de référence : `env-35-apres` (host et les 16 presets).
- Écarts Mac `env-32-apres` → `env-35-apres` (`comparer-oracle.py`). Ils fixent l'attendu de la
  comparaison contre `env-33-debian` : 4 presets F4 seuls, mêmes écarts que sur le Mac.
- Têtes publiées relevées par `git ls-remote` : famille, BSP F429 et F439, noyau, graine.
- Consigne `consignes/env-36-debian.md`, critères numérotés :
  - **C1** — versions relevées : scion (0.5.4.0 attendu, inchangé), lepton, chaîne APT.
  - **C2** — `graft-update` d'un rootstock existant de la VM, lancé par l'utilisateur :
    - 0 conflit ;
    - aucun lien sous `cubemx_hal_driver/` ;
    - liens de la HAL et du CMSIS device présents ;
    - puis rootstock neuf depuis la graine publiée : aucun lien cassé, aucun fichier régulier.
  - **C3** — host et les 16 presets construits. `comparer-oracle.py` contre `env-33-debian` :
    écarts limités aux 4 presets F4 et conformes à l'attendu. Fumée et banc KAL QEMU identiques.
  - **C4** — compilation à blanc de la HAL d'ENV-34, si elle a été retenue au PA-55 : 0 erreur
    avec la chaîne APT.
  - **C5** — graine de projet existante de la VM : `check` et `generate` inchangés, à
    `compile_commands.json` près (inclusions de la famille F4).
  - **C6** — nettoyage, si l'utilisateur l'accorde au PA-59 : <À CONFIRMER au PA-59>.
- Cartes : aucune sur la VM, sauf décision contraire au PA-59. L'utilisateur a indiqué le
  2026-11-03 que des cartes peuvent être branchées sous Debian si nécessaire.
- **PA-59** : l'utilisateur valide la consigne, les cartes et le nettoyage ; push de
  `devenv/env-36` (PA-P) ; ordre `R36-1` à la session VM.

### 2. Exécution (VM)
La session VM suit la consigne :
- elle envoie un `ACCUSÉ`, puis un `AVANCEMENT` par critère et par attente de l'utilisateur ;
- elle termine par `FIN-SUCCÈS` ou `FIN-ÉCHEC` ;
- son rapport `rapports/env-36-debian.md` et son oracle `rapports/oracles/env-36-debian/` sont
  écrits sur `devenv/env-36-debian`, puis poussés.

### 3. Rootstocks d'essai (Mac)
- `scion graft-update` des 7 rootstocks d'essai, sur accord (PA-P), selon la procédure de
  `rapports/env-28-mac.md` §3. Relever d'abord la branche de chaque clone.
- `env-11/f429zi` : construction `nucleo-f429zi-embos` comprise.
- Puis `lepton check` et `generate` : code 0 (`qemu-gra2` : 1, attendu).

### 4. Clôture → PA-60
- Session Mac : vérifier le rapport VM contre la consigne (chaque critère, commits cités) et
  refaire les comparaisons sur l'oracle poussé.
- **PA-60** : fusion de `devenv/env-36-debian` dans `devenv/env-36`, puis dans `main` ; push
  (PA-P).

## Critères de validation
- [ ] PA-59 et PA-60 tranchés et consignés.
- [ ] `FIN-SUCCÈS R36-1` vérifié par la session Mac ; C1 à C6 conformes.
- [ ] Rootstocks d'essai regreffés : 0 lien cassé, 0 fichier régulier ; `check` code 0.

## Pièges connus
- Un écart Debian contre l'oracle Mac peut venir de la chaîne APT : comparer d'abord à
  `env-33-debian`. Les écarts propres à Debian sont décrits dans `rapports/env-21-debian.md` §3.
- Le banc QEMU compte 19 et 15 tests sur Debian : `net.ping_ftpd` ne tourne que sous Linux.
- `qemu-gra2` : `graft-update` réinscrit le BSP an386. Le retirer par `scion graft-remove`, sans
  `--purge`.
- Si la VM bloque une suppression, une installation ou `graft-update`, la session ne contourne
  pas le refus : l'utilisateur lance la commande.

## À la fin de l'étape
`DEVENV-STATUS.md` :
- statut ;
- versions Debian ;
- décisions PA-59 et PA-60 ;
- journal (ordre R36-1).

Passation `handoff/env-36.md`.
