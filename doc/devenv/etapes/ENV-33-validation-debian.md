# Étape ENV-33 — Validation Debian groupée (ENV-29 à ENV-32)

## Contexte
ENV-29 à ENV-32 ne valident que sur le Mac (décision de la révision du 2026-11-02). Elles
changent :
- scion : nouvelle version, `graft-update` sûr (ENV-29) ;
- les fichiers générés par lepton : tâche « tests des greffons » (ENV-30) ;
- les binaires FreeRTOS : TCB étendu pour rtos-views (ENV-31) ;
- la déclaration du test radio : fournie par le BSP `nucleo-wl55jc1` (ENV-32).

Cette étape valide l'ensemble sur une VM Debian, par un seul ordre (§2bis). Elle remet ensuite à
jour les rootstocks d'essai du Mac. Forme : celle d'ENV-28. Archétype : infrastructure.

## Prérequis
- ENV-29, ENV-30, ENV-31 et ENV-32 terminées et poussées.
- VM Debian 13, avec sa session Claude Code (ORCHESTRATION §2) ; protocole §2bis.
- Consigne de référence : `consignes/env-28-debian.md`.
- Rapports de référence : `rapports/env-28-debian.md` et `rapports/env-28-mac.md`.
- Règles des consignes VM (ORCHESTRATION §2bis) :
  - régénérer avant de relever ;
  - commandes confiées d'emblée à l'utilisateur ;
  - branche des clones d'un rootstock existant (P-1 d'ENV-28), sous la forme fixée au PA-45.
- R28-1 : `scion graft-update` a été refusé à la session VM ; il est donc confié à l'utilisateur
  dès la consigne.
- Branches lepton-tools : `devenv/env-33` (Mac), `devenv/env-33-debian` (VM).

## Tâches

### 1. Préparation (Mac) → PA-53
- Oracle Mac de référence : le dernier oracle « après » d'ENV-31 et ENV-32 (host et les 16
  presets).
- Écarts Mac `env-27-apres` → oracle de référence (`comparer-oracle.py`). Ils fixent l'attendu de la
  comparaison contre `env-28-debian` : FreeRTOS seuls.
- Têtes publiées relevées par `git ls-remote` : dépôts, et tag de scion d'ENV-29.
- Consigne `consignes/env-33-debian.md`, critères numérotés :
  - **C1** — scion à la version d'ENV-29 par `install-debian.sh` du clone noyau (défaut
    `SCION_REF`) ; lepton réinstallé (`pipx install --force`, par l'utilisateur) ; versions
    relevées.
  - **C2** — `install-vscodium.sh` : 0 changement.
  - **C3** — `graft-update` d'un rootstock existant de la VM, avec la nouvelle version :
    - cas nominal : 0 conflit, liste des liens relevée ;
    - cas E-1 rejoué sur une copie, si le PA-53 l'accorde : un clone sur une autre branche est
      ramené ou refusé selon le PA-45, et le trunk reste intact.
    - Puis rootstock neuf depuis la graine publiée : trunk sans lien cassé ni fichier régulier.
  - **C4** — host et les 16 presets construits ; `comparer-oracle.py` contre `env-28-debian`,
    écarts conformes à l'attendu ; fumée et banc KAL QEMU, FreeRTOS compris.
  - **C5** — tâche « tests des greffons » d'ENV-30 :
    - présente dans l'espace régénéré, dans les configurations du PA-47 ;
    - exécutée en ligne de commande : `qemu-mps2-an386.peripheriques` réussi.
  - **C6** — graine de projet existante de la VM : régénérée, puis `check` et `generate`
    inchangés hors la tâche d'ENV-30.
  - **C7** — test radio d'ENV-32, découverte seulement (pas de carte sur la VM) : preset WL55
    configuré avec des ports fictifs, `ctest -N` liste le test sous le nom du PA-51, déclaré
    par le BSP.
  - **C8** — nettoyage, si l'utilisateur l'accorde au PA-53 : <À CONFIRMER au PA-53 : rootstocks
    `essais/env-14-debian`, `essais/env-28-debian` et `~/env-28-journaux/` conservés ou supprimés>.
- **PA-53** : l'utilisateur valide la consigne et le nettoyage ; push de `devenv/env-33` (PA-P) ;
  ordre `R33-1` à la session VM.

### 2. Exécution (VM)
La session VM suit la consigne :
- elle envoie un `ACCUSÉ`, puis un `AVANCEMENT` par critère et par attente de l'utilisateur ;
- elle termine par `FIN-SUCCÈS` ou `FIN-ÉCHEC`, avec les informations d'action ;
- son rapport `rapports/env-33-debian.md` et son oracle `rapports/oracles/env-33-debian/` sont
  écrits sur `devenv/env-33-debian`, puis poussés.

### 3. Rootstocks d'essai (Mac)
- `scion graft-update` des 7 rootstocks d'essai, sur accord (PA-P) :
  - `env-9` ;
  - `env-11/{f429zi,qemu,qemu-gra2,wl55jc1}` ;
  - `env-11/bout-en-bout/rootstock` ;
  - `env-13-vierge`.
- Procédure : `rapports/env-28-mac.md` §3. Relever d'abord la branche de chaque clone.
- Puis `lepton check` et `generate` : code 0 (`qemu-gra2` : 1, attendu) ; espaces relevés.

### 4. Clôture → PA-54
- Session Mac : vérifier le rapport VM contre la consigne (chaque critère, commits cités).
  Refaire les comparaisons sur l'oracle poussé.
- **PA-54** : fusion de `devenv/env-33-debian` dans `devenv/env-33`, puis dans `main` ; push
  (PA-P).

## Critères de validation
- [ ] PA-53 et PA-54 tranchés et consignés.
- [ ] `FIN-SUCCÈS R33-1` vérifié par la session Mac ; C1 à C8 conformes.
- [ ] Rootstocks d'essai regreffés : 0 lien cassé, 0 fichier régulier ; `check` code 0.
- [ ] `DEVENV-STATUS.md` §Versions : scion et lepton sur Debian relevés.

## Pièges connus
- Un écart Debian contre l'oracle Mac peut venir de la chaîne APT : comparer d'abord à
  `env-28-debian`. Les écarts propres à Debian sont décrits dans `rapports/env-21-debian.md` §3.
- Le banc QEMU passe à 19 et 15 tests sur Debian : `net.ping_ftpd` ne tourne que sous Linux.
- `qemu-gra2` : `graft-update` réinscrit le BSP an386. Le retirer par `scion graft-remove`, sans
  `--purge` (ENV-21, ENV-28).
- Si la VM bloque une suppression, une installation ou `graft-update`, la session ne contourne
  pas le refus : l'utilisateur lance la commande.
- Hors périmètre : Apple Silicon (pas de machine) ; flash de cartes (pas de carte sur la VM).

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, versions Debian, décisions PA-53 et PA-54, journal (ordre R33-1).
Passation `handoff/env-33.md`.
