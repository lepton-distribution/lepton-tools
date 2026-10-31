# Étape ENV-28 — Validation Debian groupée (ENV-22 à ENV-27)

## Contexte
ENV-22 à ENV-27 ne valident que sur le Mac (décision du 2026-10-31). Elles changent :
- scion : nouvelle version (ENV-23) ;
- les images mklepton : cpufs automatique (ENV-24) ;
- les fichiers générés par lepton : DBG-5 et DBG-4 (ENV-25, ENV-26) ;
- la découverte des tests : TST-2 (ENV-27).

Cette étape valide l'ensemble sur une VM Debian par un seul ordre (§2bis), puis remet à jour les
rootstocks d'essai du Mac. Elle reprend la forme d'ENV-21. Archétype : infrastructure.

## Prérequis
- ENV-22 à ENV-27 terminées et poussées.
- VM Debian 13 et sa session Claude Code (ORCHESTRATION §2) ; protocole §2bis.
- Consigne de référence : `consignes/env-21-debian.md`. Rapports de référence :
  `rapports/env-21-debian.md`, `rapports/env-21-mac.md`.
- Règles des consignes VM écrites en ENV-22 (régénérer avant de relever ; suppressions et
  installations `pipx` confiées à l'utilisateur).
- Branches lepton-tools : `devenv/env-28` (Mac), `devenv/env-28-debian` (VM).

## Tâches

### 1. Préparation (Mac) → PA-43
- Oracle Mac de référence : le dernier oracle « après » des étapes 24 à 27 (host et tous les
  presets).
- Écarts Mac `env-20-apres` → oracle de référence (`comparer-oracle.py`) : ils fixent l'attendu
  de la comparaison contre `env-21-debian`.
- Têtes publiées relevées par `git ls-remote` : dépôts et tag de scion.
- Consigne `consignes/env-28-debian.md`, critères numérotés :
  - C1 scion à la version d'ENV-23 et lepton réinstallés (par l'utilisateur si les permissions de
    la VM le refusent), versions relevées ;
  - C2 `install-debian.sh` du clone noyau avec le défaut `SCION_REF`, puis `install-vscodium.sh` :
    0 changement à la seconde exécution ;
  - C3 graine du rootstock de la VM mise à jour par le mécanisme d'ENV-23, sans `git pull` à la
    main. Rootstock neuf depuis la graine publiée : trunk sans lien cassé ni fichier régulier ;
  - C4 host et tous les presets construits ; `comparer-oracle.py` contre `env-21-debian`, écarts
    conformes à l'attendu ; fumée et banc KAL QEMU ;
  - C5 lancement DBG-5 généré pour gdb ; arrêt dans `mklepton`, constaté en ligne de commande
    (`gdb -batch`) ou par l'utilisateur sous VSCodium : <À CONFIRMER au PA-43> ;
  - C6 tests du greffon d'essai d'ENV-27 découverts (`ctest -N`) et réussis ;
  - C7 graine de projet existante de la VM : régénérée, puis `check` et `generate` inchangés ;
  - C8 nettoyage : `~/lepton-tools-dev/essais/env-21-debian` et `~/env-21-journaux/`, à
    supprimer si l'utilisateur l'accorde au PA-43.
- **PA-43** : l'utilisateur valide la consigne et le nettoyage ; push de `devenv/env-28` (PA-P) ;
  ordre `R28-1` à la session VM.

### 2. Exécution (VM)
La session VM suit la consigne :
- elle envoie un `ACCUSÉ`, puis un `AVANCEMENT` par critère ;
- elle termine par `FIN-SUCCÈS` ou `FIN-ÉCHEC`, avec les informations d'action ;
- son rapport `rapports/env-28-debian.md` est écrit sur `devenv/env-28-debian`, puis poussé.

### 3. Rootstocks d'essai (Mac)
- `scion graft-update` des rootstocks d'essai : la liste suit la décision d'ENV-22 sur
  `env-11/bout-en-bout`. Se fait sur accord (PA-P) et suit la procédure de
  `rapports/env-21-mac.md` §3. Une graine en retard est avancée par scion (ENV-23).
- Puis `lepton check` et `generate` : code 0 (`qemu-gra2` : 1, attendu) ; espaces relevés.

### 4. Clôture → PA-44
- Session Mac : vérifier le rapport VM contre la consigne (chaque critère, commits cités) et
  refaire les comparaisons sur l'oracle poussé.
- **PA-44** : fusion de `devenv/env-28-debian` dans `devenv/env-28`, puis dans `main` ; push
  (PA-P).

## Critères de validation
- [ ] PA-43 et PA-44 tranchés et consignés.
- [ ] `FIN-SUCCÈS R28-1` vérifié par la session Mac ; C1 à C8 conformes.
- [ ] Rootstocks d'essai regreffés : 0 lien cassé, 0 fichier régulier ; `check` code 0.
- [ ] `DEVENV-STATUS.md` §Versions : scion et lepton sur Debian relevés.

## Pièges connus
- Un écart Debian contre l'oracle Mac peut venir de la chaîne APT : comparer d'abord à
  `env-21-debian`. Les variations de `.text` de quelques octets et l'inversion de `.noinit` sur
  SAMD21 FreeRTOS sont propres à la chaîne Debian (`rapports/env-21-debian.md` §3).
- Le banc QEMU passe à 19 et 15 tests sur Debian : `net.ping_ftpd` ne tourne que sous Linux.
- Si la VM bloque une suppression ou une installation, la session ne la contourne pas :
  l'utilisateur la lance.
- Hors périmètre : Apple Silicon (pas de machine) ; flash de cartes (pas de carte sur la VM).

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, versions Debian, décisions PA-43 et PA-44, journal (ordre R28-1).
Passation `handoff/env-28.md`.
