# Étape ENV-21 — Validation Debian groupée

## Contexte
Plusieurs changements n'ont pas été rejoués sur Debian : lepton n'y est pas réinstallé depuis
`devenv/env-16` ; les scripts d'installation du noyau, avec scion 0.5.2.0 par défaut (6f1801d),
n'y ont jamais été exécutés (R15-1 installait scion par pipx) ; ENV-17 à ENV-20 changent le
noyau, lepton, la graine publiée et ajoutent des greffons. Les rootstocks d'essai du Mac sont au
niveau d'ENV-14. Cette étape valide l'ensemble sur une VM Debian par un seul ordre (§2bis) et
remet les rootstocks d'essai à jour. Archétype : infrastructure.

## Prérequis
- ENV-17 à ENV-20 terminées et poussées (ou leurs branches poussées, selon le PA-26).
- VM Debian 13 et session Claude Code de la VM (ORCHESTRATION §2) ; protocole §2bis.
- Consigne de référence : `consignes/env-15-debian.md` ; références Debian :
  `rapports/env-13-debian.md`, `rapports/env-15-debian.md`.
- Branches : lepton-tools `devenv/env-21` (Mac), `devenv/env-21-debian` (VM).

## Tâches

### 1. Préparation (Mac) → PA-29
- Oracle Mac de référence : dernier oracle « après » des étapes 19 et 20 (host + tous les presets).
- Consigne `consignes/env-21-debian.md`, critères numérotés :
  - C1 lepton réinstallé depuis `main` (`pipx install --force`), version relevée ;
  - C2 `scripts/install-debian.sh` du clone noyau exécuté avec le défaut `SCION_REF` (scion
    0.5.2.0), puis `install-vscodium.sh` : 0 changement à la seconde exécution ;
  - C3 rootstock neuf depuis la graine publiée (`scion rootstock-install`, `seed-add --version
    original-tree`, `graft`) : greffons d'ENV-19 et ENV-20 compris ; trunk 0 lien cassé ;
  - C4 host + tous les presets construits ; `comparer-oracle.py` contre l'oracle Mac ; fumée et
    banc KAL QEMU ;
  - C5 `lepton check` code 0 ; `seed status` et `generate` sur la graine de référence (ENV-18) ;
  - C6 une graine de projet existante de la VM : `check`, `generate` inchangés ;
  - C7 nettoyage : `~/lepton-tools-dev/essais/env-15-debian`, `~/env-15-journaux/` supprimés si
    l'utilisateur l'accorde au PA-29.
- **PA-29** : l'utilisateur valide la consigne et le nettoyage de la VM ; push de `devenv/env-21`
  (PA-P) ; ordre `R21-1` à la session VM.

### 2. Exécution (VM)
La session VM suit la consigne : `ACCUSÉ`, un `AVANCEMENT` par critère, `FIN-SUCCÈS` ou
`FIN-ÉCHEC` avec les informations d'action ; rapport `rapports/env-21-debian.md` sur
`devenv/env-21-debian`, poussé.

### 3. Rootstocks d'essai (Mac)
- `scion graft-update` des rootstocks d'essai (`essais/env-9`, `essais/env-11/*`,
  `essais/env-13-vierge`) sur accord (PA-P) ; procédure et parades de l'après-clôture d'ENV-14
  (`DEVENV-STATUS.md` §Journal, 2026-10-30).
- Puis `lepton check` et `generate` : code 0, espaces relevés.

### 4. Clôture → PA-30
- Session Mac : vérifier le rapport VM contre la consigne (chaque critère, commits cités).
- **PA-30** : fusion de `devenv/env-21-debian` dans `devenv/env-21`, puis dans `main` ; fusions
  différées d'ENV-19 et ENV-20 si le PA-26 l'a prévu ; push (PA-P).

## Critères de validation
- [ ] PA-29 et PA-30 tranchés et consignés.
- [ ] `FIN-SUCCÈS R21-1` vérifié par la session Mac ; C1 à C7 conformes.
- [ ] Rootstocks d'essai regreffés : 0 lien cassé, 0 fichier régulier ; `check` code 0.
- [ ] `DEVENV-STATUS.md` §Versions : lepton et scion sur Debian relevés.

## Pièges connus
- Un écart Debian contre l'oracle Mac peut venir de la chaîne APT (versions de
  `rapports/env-10-debian.md` §1) : comparer d'abord à l'oracle Debian précédent (R15-1).
- `graft-update` de `env-11/qemu` a échoué en ENV-14 (conflit de `.DS_Store`) : scion 0.5.2.0 (E1)
  doit l'éviter ; sinon appliquer la parade consignée.
- Hors périmètre : Apple Silicon (pas de machine).

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, versions Debian, décisions PA-29 et PA-30, journal (ordre R21-1).
Passation `handoff/env-21.md`.
