# Étape ENV-29 — scion : `graft-update` sûr (version déclarée, trunk préservé)

## Contexte
R28-1 (ENV-28) a révélé deux comportements de scion 0.5.3.0 (`rapports/env-28-debian.md` §6,
E-1 ; proposition P-2 de `rapports/env-28-mac.md` §4, retenue au PA-44) :
1. `graft-update` fait `git pull` sur la **branche courante** d'un clone existant, sans revenir à
   la version déclarée dans `.scion.grafted.list`. Pour un clone nouveau, il fait pourtant le
   `checkout` de cette version. Sur la VM, deux clones laissés sur `devenv/env-14` ont gardé
   l'ancien noyau : 277 conflits.
2. Quand la regreffe échoue sur un conflit, le **trunk est vidé** : il ne restait que
   `.scion.grafted.list`, 0 lien contre 3929 avant.

La parade actuelle est procédurale : la règle « branche des clones d'un rootstock existant »
d'ORCHESTRATION §2bis. Cette étape corrige scion lui-même.

scion reste générique (NF-2) : aucune chaîne propre à Lepton dans `seed.scions`. Archétype :
infrastructure. La procédure de version est celle d'ENV-15 et d'ENV-23.

## Prérequis
- ENV-28 terminée.
- `<SEED_SCIONS>` : `master` e4d76b2, tag `0.5.3.0` sur ad292ee ; 137 tests.
- Procédures de référence : `rapports/env-23-scion.md` et `rapports/env-15-scion.md` §4-§9.
- Code : `scion/graft.py` (`_fetch`, `seed_updates`, `ungraft`), `scion/cli.py`
  (`cmd_seed_update`, `cmd_graft`), `scion/gitops.py`.
- Skills `lepton-rootstock` et `lepton-oracle`.
- Branches `devenv/env-29` dans `<SEED_SCIONS>` et lepton-tools. Dans le clone noyau, seulement si
  `SCION_REF` change (§4).

## Tâches

### 1. Audit (lecture seule) → PA-45
- Code de scion :
  - Chemin de `graft-update` : où le clone existant est mis à jour (`pull`), et où un clone
    nouveau reçoit le `checkout` de la version déclarée.
  - À quel moment le trunk est dégreffé (`ungraft`) par rapport à la détection des conflits.
  - Même lecture pour `seed-update`, si ce chemin est commun.
- Cas d'un clone hors version déclarée, à distinguer :
  - autre branche, propre ;
  - autre branche, avec des commits non publiés ;
  - modifications non commitées ;
  - `HEAD` détaché ;
  - version déclarée qui est un tag.
- Reproduire E-1 sur une copie d'essai de `<ROOTSTOCK>` (skill `lepton-rootstock`) : un clone
  passé sur une branche ancienne, puis `graft-update`. Ne jamais le faire sur `<ROOTSTOCK>`.
- Usages par lepton : `lepton/scion_runner.py` ; messages et codes de retour attendus par
  l'extension.
- Rapport `rapports/env-29-scion.md`.
- **PA-45** : l'utilisateur valide :
  - Clone hors version déclarée : <À CONFIRMER au PA-45>.
    - Option 1 : le ramener à la version déclarée s'il est propre, refuser sinon.
    - Option 2 : refuser toujours, en nommant le clone et sa branche.
    - Dans les deux cas, contrôle de tous les clones avant tout dégreffage.
  - Trunk en cas d'échec de la regreffe : <À CONFIRMER au PA-45>.
    - Option 1 : détecter les conflits avant de dégreffer.
    - Option 2 : regreffer l'état antérieur après l'échec.
  - Le numéro de version : <À CONFIRMER au PA-45 : `0.5.3.1` (correctif) ou `0.5.4.0`>.
  - Lepton : `SCION_MIN_VERSION` relevé ou non : <À CONFIRMER au PA-45>.
  - Règle P-1 d'ORCHESTRATION §2bis : conservée, allégée ou retirée après le correctif :
    <À CONFIRMER au PA-45>.
- Aucune modification avant la réponse.

### 2. Implémentation (`<SEED_SCIONS>`, `devenv/env-29`)
- Écrire les tests de scion d'abord : un test par cas validé au PA-45, dont la reproduction
  d'E-1 (clone sur une autre branche, conflit, trunk conservé). Les 137 tests existants restent
  verts.
- Commits séparés : un par comportement, puis un pour la version (`CHANGELOG.md`).

### 3. Essai sur une copie (skill `lepton-rootstock`)
- Créer une copie d'essai de `<ROOTSTOCK>`, puis installer scion par
  `pipx install --force "git+file://<SEED_SCIONS>@devenv/env-29"`.
- Sur la copie, constater :
  - un clone sur une autre branche est ramené à la version déclarée, ou la commande refuse avant
    tout dégreffage (selon le PA-45) ;
  - un conflit provoqué laisse le trunk dans son état antérieur : même nombre de liens, et
    `sha256` de la liste triée identique ;
  - le cas nominal, c'est-à-dire des clones à la version déclarée et une graine à jour, donne une
    liste de liens identique à celle de `<ROOTSTOCK>`.
- L'arbre composé est identique : aucune reconstruction n'est requise (raisonnement d'ENV-15 §6) ;
  sinon, oracle.

### 4. Version, lepton, `<ROOTSTOCK>` → PA-46
- Préparer le tag annoté de la version, puis
  `pipx install --force "git+file://<SEED_SCIONS>@<version>"`.
- lepton-tools, selon le PA-45 : `SCION_MIN_VERSION`, `SCION_REF` d'`install-vscodium.sh`,
  `README.md` et tests.
- Clone noyau, si la version change le défaut : `SCION_REF` d'`install-{macos,debian}.sh`,
  `doc/BUILDING.md` et `README-PAQUET.md`.
- Regreffer `<ROOTSTOCK>` (PA-P) : liste inchangée, 0 fichier régulier, 0 lien cassé.
- `pytest` de lepton vert ; `lepton check` code 0.
- ORCHESTRATION §2bis : règle P-1, selon le PA-45.
- **PA-46** : rapport ; publication (PA-P) : tag et `master` de `<SEED_SCIONS>`, branches
  `devenv/env-29`, fusions. La validation Debian est reportée à ENV-33.

## Critères de validation
- [ ] PA-45 et PA-46 tranchés et consignés.
- [ ] Tests de scion verts, dont les nouveaux ; aucune chaîne propre à Lepton dans `seed.scions`
      (`grep -ri lepton scion/` : 0).
- [ ] Copie d'essai : E-1 reproduit avant le correctif, et ne se produit plus après ; trunk
      intact sur conflit (`sha256` de la liste triée).
- [ ] Toutes les références de version (lepton, `install-vscodium.sh`, scripts du noyau,
      documentation) désignent la même version.

## Pièges connus
- `scion` installé par pipx avant le PA-46 change l'outil de **tous** les rootstocks. Point de
  retour : `pipx install --force "git+file://<SEED_SCIONS>@0.5.3.0"`.
- `graft-update` est soumis à PA-P : sur `<ROOTSTOCK>` et sur chaque rootstock d'essai, attendre
  l'accord.
- Un clone avec des commits non publiés sur une branche d'étape ne doit jamais être déplacé en
  silence : vérifier que le test le couvre.
- Le refus du classifieur de la VM pour `graft-update` (E-2 de R28-1) ne concerne pas le Mac.
  Ne pas en tirer de règle ici.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, branches, §Versions (scion), décisions PA-45 et PA-46, journal.
Passation `handoff/env-29.md`.
