# Étape ENV-44 — Résidus d'ENV-37 à ENV-43

## Contexte
Révision du plan du 2026-11-09, faite à partir de `HORS-PLAN.md`. Cette étape traite les résidus
D1, D2, D3, D5, D6, D7 et D9 relevés d'ENV-37 à ENV-43. D4 reste hors plan ; D8 est traité en ENV-50.
Elle consolide l'existant avant les étapes ENV-45 à ENV-49. Comme ENV-22, elle regroupe de petits
sujets indépendants, chacun dans son propre commit.

Archétype : migration iso-fonctionnelle. Une seule exception est attendue : D5 change le binaire des
4 presets an386. Il faut donc un nouvel oracle de référence si D5 est retenu.

## Prérequis
- ENV-43 terminée. Oracles de référence : Mac `oracles/env-42-apres/`, Debian `oracles/env-43-debian/`.
- Sources de chaque résidu :

| # | Point | Source |
| --- | --- | --- |
| D1 | `seed replace` / `seed remove` d'un greffon porteur de projections : jamais essayé | `rapports/env-41-f4-projection.md` §4.4 ; P-P6 de `<SEED_SCIONS>/doc/projection-miroir.md` |
| D2 | Extension 0.5.2 : la table clone tiers → trunk n'agit que si gdb rend le chemin réel ; jamais observée | `rapports/env-41-f4-projection.md` §4.4 |
| D3 | Hook `.claude/hooks/proteger-trunk.py` : refuse les commandes qui citent `trunk/` ou `depots/tiers/` après un verbe d'écriture, même en lecture | `rapports/env-41-f4-projection.md` §4.4 ; `handoff/env-43.md` (pièges) |
| D5 | BSP `qemu-mps2-an386` : en-tête `ucore/cmsis/Device/ARM/ARMCM4` V3.x compilé avec le `core_cm4.h` 5.9.0 ; `ucore/cmsis-5/Device/ARM/` contient un `ARMCM4` CMSIS 5 | `rapports/env-42-core-cm4.md` §1.4, §4.4 (O-3) |
| D6 | `scripts/tiers/compiler-hal-f4-a-blanc.sh` rend 1 tant qu'il essaie l'ordre `v330` | `rapports/env-42-core-cm4.md` §4.1 |
| D7 | CMSIS-Core V3.30 : en-tête `V3.30`, `__CM4_CMSIS_VERSION_SUB` à `0x20`, `cmsis/source.txt` « Version 2.10 » | `rapports/env-42-core-cm4.md` §1.1, §4.4 (O-2) |
| D9 | Les messages VM → Mac ne sont pas remis (ECONNRESET, « bridge ID is stale ») ; l'utilisateur relaie | `rapports/env-43-mac.md` §3 ; `rapports/env-43-debian.md` §9 |

- Dépôts : lepton-tools, clone noyau `master` 763dda2, `bsp-qemu-mps2-an386` `master` 5819047.
- D2 demande une carte F4 sur le Mac. La NUCLEO-F429ZI est restée sur la VM après R43-1 : c'est à
  l'utilisateur de la rattacher.
- Skills `lepton-rootstock`, `lepton-oracle`, `lepton-cibles`.
- Branches `devenv/env-44` : lepton-tools, plus chaque greffon modifié selon le PA-75.

## Tâches

### 1. Audit (lecture seule) → PA-75
- D1 : décrire l'essai, jamais sur `<ROOTSTOCK>`. Deux refus de lepton excluent une copie de
  `<ROOTSTOCK>`, qui porte la graine de référence `original-tree` :
  - `seed replace` et `seed remove` y sont refusés (`lepton/seed.py:575`, `refuse_reference`,
    PA-23) ;
  - `seed remove` refuse aussi de retirer la famille du BSP de la graine (`lepton/seed.py:658`).

  Il faut donc un rootstock à graine de projet. Candidats : une copie de `essais/env-11/f429zi`, ou
  une graine créée par `lepton seed new` ; pour le retrait, une graine dont le BSP n'est pas F4.
  Copier par `rsync -a`, sans `build/` ni `third_party/` (forme d'ENV-41 §3.3). Relever l'effet
  attendu sur les clés projetées (P-P6) et les commandes (`lepton seed replace`, `lepton seed remove`,
  puis `scion graft-update`, PA-P).
- D2 : chercher `depots/tiers` dans les DWARF des binaires de carte (`.debug_line`, `.debug_str`) de
  `<ROOTSTOCK>/build/*`. S'il est absent partout, la table n'est jamais sollicitée par une construction
  du trunk. Proposer alors un cas qui la sollicite, ou clore le point comme sans objet. Un essai réel
  est une session de débogage sous VSCodium menée par l'utilisateur, sur une carte flashée avec un
  binaire qui sollicite la table.
- D3 : relever dans `proteger-trunk.py` la règle qui lit le texte des commandes. Présenter les
  refus observés (ENV-41, ENV-43) et une correction possible, sans affaiblir le refus d'écriture.
  Les cas de test du hook couvrent les deux sens : écriture refusée, lecture acceptée. Il n'existe
  aucun test du hook sous `tests/` (ENV-41 : essai manuel sur 10 cas) : proposer un emplacement.
- D5 : diff entre `ucore/cmsis/Device/ARM/ARMCM4` et `ucore/cmsis-5/Device/ARM/ARMCM4` ; ce qui
  l'inclut dans le BSP an386 ; écart de binaire attendu.
- D6 : options pour le script (retirer l'ordre `v330`, le garder sans compter son échec, ou une
  option dédiée).
- D7 : fichiers à corriger et texte proposé (documentation seulement, aucun en-tête amont modifié).
- D9 : texte d'amendement d'ORCHESTRATION §2bis quand la remise échoue (relais par l'utilisateur,
  identification du message relayé, preuve de lecture).
- Rapport `rapports/env-44-residus.md`, §1.
- **PA-75** : l'utilisateur tranche chaque point :
  - D1 : rootstock et graine de projet de l'essai. Conduite si l'essai révèle un défaut :
    <À CONFIRMER au PA-75>. Options : correction de lepton ici ; ou étape scion insérée (forme
    d'ENV-29), l'essai restant suspendu jusqu'à elle. Un correctif de scion entraîne une nouvelle
    version, la publication (PA-P), `SCION_MIN_VERSION` de lepton et `SCION_REF`
    (`install-vscodium.sh` et `install-{macos,debian}.sh` du clone noyau).
  - D2 : essai sur carte par l'utilisateur, ou clôture sans objet : <À CONFIRMER au PA-75>.
  - D3 : correction retenue, emplacement des tests du hook : <À CONFIRMER au PA-75>.
  - D5 : bascule de l'an386 sur `cmsis-5/Device/ARM/ARMCM4`, ou statu quo documenté ; critère
    d'écart des 4 presets an386 : <À CONFIRMER au PA-75>.
  - D6, D7 : forme retenue.
  - D9 : texte du §2bis.
- Aucune modification avant la réponse.

### 2. Oracle avant
Skill `lepton-oracle` : host et les 16 presets → `rapports/oracles/env-44-avant/`. Résultat attendu :
conforme à `env-42-apres` (code 0).

### 3. Corrections
Un commit par point, dans le dépôt qui le porte :
- D9 : `ORCHESTRATION.md` §2bis (session principale seule).
- D6 : `scripts/tiers/`. D7 : documents désignés au PA-75.
- D3 : `.claude/hooks/proteger-trunk.py`, cas de test compris ; ligne « hook » d'ORCHESTRATION
  §5bis, qui ne cite pas encore `depots/tiers/` (protégé depuis ENV-41).
- D5 : clone `bsp-qemu-mps2-an386` (ou noyau, selon le relevé), puis regreffe si un fichier est
  ajouté ou retiré.
- D1, D2 : essais selon le PA-75, résultats au rapport.

### 4. Contrôles → PA-76
- Oracle après : code 0 sur host et les 12 presets hors an386. Pour les 4 presets an386 : écarts
  dans le critère du PA-75, fumée et banc KAL QEMU identiques, `ctest -N` identiques.
- Nouvel oracle de référence `oracles/env-44-apres/` si D5 change un binaire.
- Hook : cas de test verts ; écriture sous `trunk/` et `depots/tiers/` toujours refusée.
- `compiler-hal-f4-a-blanc.sh` : code de retour conforme à la forme retenue.
- `<ROOTSTOCK>` : 0 lien cassé, 0 fichier régulier ; `lepton check` code 0.
- `pytest` de lepton vert si lepton est touché.
- **PA-76** : rapport ; push et fusions des branches `devenv/env-44` (PA-P).

## Critères de validation
- [ ] PA-75 et PA-76 tranchés et consignés.
- [ ] Chaque point D1, D2, D3, D5, D6, D7, D9 corrigé, essayé ou clos, avec sa preuve au rapport.
- [ ] Binaires : code 0 hors an386 ; an386 dans le critère du PA-75.
- [ ] `HORS-PLAN.md` : chaque point traité marqué, avec renvoi au rapport.

## Pièges connus
- D3 : une correction trop large laisse passer une écriture. Tester `>`, `tee`, `sed -i`, `cp`,
  `mv`, `rm`, `ln` vers `trunk/` et vers `depots/tiers/`, en chemin absolu et en chemin relatif.
- Tant que D3 n'est pas corrigé, une commande de lecture qui cite `depots/tiers/` doit passer par un
  fichier de script.
- D5 : si `.debug_line` ou `.debug_str` change seul, chercher d'abord un chemin d'inclusion changé.
- D1 : sur la copie d'essai, relever la branche de chaque clone avant tout `graft-update` (§2bis).
  Ne jamais lancer l'essai dans `<ROOTSTOCK>`, ni dans le rootstock d'essai copié.
- Les rootstocks d'essai du Mac et de la VM ne sont pas regreffés avant ENV-50 : ne pas y lancer
  `graft-update`.
- Les en-têtes amont (V3.30, CMSIS 5) ne se corrigent jamais : D7 ne touche que la documentation
  Lepton.
- `zsh` ne découpe pas une variable en mots : utiliser `bash -c` ou un script.

## À la fin de l'étape
`DEVENV-STATUS.md` :
- statut et branches ;
- décisions PA-75 et PA-76 ;
- oracle de référence s'il change ;
- journal.

`HORS-PLAN.md` : points D traités. Passation `handoff/env-44.md`.
