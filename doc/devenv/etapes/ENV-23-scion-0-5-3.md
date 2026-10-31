# Étape ENV-23 — Évolutions de scion : mise à jour de la graine, sources non git

## Contexte
ENV-20 et ENV-21 ont relevé deux limites de scion 0.5.2.0, contournées à la main :
1. `scion graft-update` ne met pas à jour le dépôt de la graine, car `sync` lit la graine locale.
   Un rootstock créé depuis la graine de référence ne reçoit donc pas les greffons ajoutés à la
   graine publiée. Parade actuelle : `git -C <graine> pull --ff-only`, puis `graft-update`
   (`handoff/env-21.md`, Pièges).
2. Le filtre E1 d'ENV-15 (fichiers ignorés par git) ne s'applique qu'aux sources git. Les
   `.DS_Store` du Finder présents dans une source non git, `depots/generation/building` (greffon
   `building`), sont greffés comme liens (`handoff/env-20.md`, Pièges).

Cette étape corrige ces deux points dans scion. scion reste générique (NF-2) : aucune chaîne
propre à Lepton dans `seed.scions`. Archétype : infrastructure ; procédure de version d'ENV-15.

## Prérequis
- ENV-22 terminée (`.scion.trunk.tolerated` présent dans `<ROOTSTOCK>`).
- `<SEED_SCIONS>` : `master` 472c12e, tag `0.5.2.0`. Procédure de référence :
  `rapports/env-15-scion.md` §4-§9.
- Skills `lepton-rootstock` et `lepton-oracle`.
- Branches `devenv/env-23` dans `<SEED_SCIONS>` et lepton-tools ; dans le clone noyau seulement
  si `SCION_REF` change (voir le §4).

## Tâches

### 1. Audit (lecture seule) → PA-33
- Code de scion :
  - `sync` et `graft-update` : quelle graine est lue, et à quel moment le dépôt de la graine
    pourrait être avancé ;
  - comportement si la graine locale a des commits non publiés ou des modifications ;
  - filtre E1 et chemin des sources non git.
- Mesures sur les rootstocks existants (`<ROOTSTOCK>`, `essais/env-13-vierge`) :
  - nombre de fichiers étrangers dans les sources non git ;
  - écart entre la graine locale et la graine publiée.
- Usages de ces commandes par lepton : `lepton/scion_runner.py`, purge de `.DS_Store` et `._*`
  avant `scion graft`.
- Rapport `rapports/env-23-scion.md`.
- **PA-33** : l'utilisateur valide :
  - Mise à jour de la graine : <À CONFIRMER au PA-33>.
    - Forme : comportement par défaut de `graft-update` ou option explicite.
    - Garde-fous : avance rapide seulement ; refus si la graine a des modifications locales.
  - Fichiers étrangers des sources non git : <À CONFIRMER au PA-33>.
    - Mécanisme : motifs de `.scion.trunk.tolerated`, fichier d'exclusion propre à la source, ou
      autre.
    - Ce qui arrive aux liens déjà greffés.
  - Le numéro de version : <À CONFIRMER au PA-33 : `0.5.3.0` proposé>.
  - Lepton : <À CONFIRMER au PA-33>.
    - `SCION_MIN_VERSION` relevé ou non.
    - Purge de `.DS_Store` conservée ou retirée.
- Aucune modification avant la réponse.

### 2. Implémentation (`<SEED_SCIONS>`, `devenv/env-23`)
- Écrire les tests de scion d'abord : un test par comportement validé au PA-33. Les 126 tests
  d'ENV-15 restent verts.
- Commits séparés : un par évolution, puis la version.

### 3. Essai sur une copie (skill `lepton-rootstock`)
- Créer une copie d'essai de `<ROOTSTOCK>`, puis installer scion par
  `pipx install --force "git+file://<SEED_SCIONS>@devenv/env-23"`.
- Sur la copie :
  - la graine en retard d'un commit est avancée, ou la commande s'arrête comme décidé au PA-33 ;
  - un fichier étranger de la source `building` n'est plus greffé.
- Liste des liens de la copie identique à celle de `<ROOTSTOCK>`, au fichier étranger près
  (`sha256` de la liste triée). L'arbre composé étant identique, aucune reconstruction n'est
  requise (raisonnement d'ENV-15 §6) ; sinon, oracle.

### 4. Version, lepton, `<ROOTSTOCK>` → PA-34
- Préparer le tag annoté de la version, puis `pipx install --force "git+file://<SEED_SCIONS>@<version>"`.
- lepton-tools : `SCION_MIN_VERSION`, `SCION_REF` d'`install-vscodium.sh`, `README.md` et tests,
  selon le PA-33.
- Clone noyau : `SCION_REF` d'`install-{macos,debian}.sh`, `doc/BUILDING.md` et
  `README-PAQUET.md`, alignés sur la nouvelle version (écart d'ENV-15 §9 à ne pas répéter).
- Regreffer `<ROOTSTOCK>` : 0 fichier régulier, 0 lien cassé.
- `pytest` de lepton vert ; `lepton check` code 0.
- **PA-34** : rapport ; publication (PA-P) : tag et `master` de `<SEED_SCIONS>`, branches
  `devenv/env-23`, fusions. La validation Debian est reportée à ENV-28.

## Critères de validation
- [ ] PA-33 et PA-34 tranchés et consignés.
- [ ] Tests de scion verts, dont les nouveaux ; aucune chaîne propre à Lepton dans `seed.scions`
      (`grep -ri lepton` sur les modules : 0).
- [ ] Copie d'essai : graine avancée ou refus conforme ; fichier étranger de `building` non greffé.
- [ ] Toutes les références de version (lepton, `install-vscodium.sh`, scripts du noyau,
      documentation) désignent la même version.

## Pièges connus
- `scion` installé par pipx avant le PA-34 change l'outil de tous les rootstocks. Point de retour :
  `pipx install --force "git+file://<SEED_SCIONS>@0.5.2.0"` (écart d'ENV-15 §6).
- Les rootstocks créés avant 0.5.2.0 n'ont pas de `.scion.trunk.tolerated` (`essais/env-11/*`
  en ont un depuis ENV-21).
- Le greffon `building` est une source locale non git : ne pas en faire un dépôt dans cette
  étape.
- Un test qui fixe ses exclusions globales (`test_graft_removes_system_files`, ENV-15) peut
  changer de résultat : à signaler au PA-34, pas à adapter en silence.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, branches, §Versions (scion), décisions PA-33 et PA-34, journal.
Passation `handoff/env-23.md`.
