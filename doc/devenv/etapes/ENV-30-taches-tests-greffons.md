# Étape ENV-30 — Tâche de l'éditeur « tests des greffons »

## Contexte
ENV-27 a réalisé TST-2 : un greffon déclare ses tests par le champ `tests` de son manifeste.
`lepton_greffon_test` les étiquette `greffon:<nom>`, `arch:<cœur>` et `backend:<b>`.
`ctest --preset <P> -L greffon:` les sélectionne, ainsi que leur fixture (`rapports/env-27-tst2.md`
§7). Aucune tâche de l'éditeur ne les lance : `lepton generate` n'écrit, pour une configuration
QEMU, que « test de fumée » (`-L smoke`) et « banc KAL » (`-L kal`) (`lepton/generate.py`, fonction
`tasks`).

Cette étape ajoute la tâche « tests des greffons » (proposition P-1 d'ENV-27, retenue au PA-42).
Elle complète TST-1 (« résultats lisibles dans l'éditeur ») pour les tests de TST-2. Archétype :
création bornée, limitée à lepton-tools. Binaires et tests inchangés.

## Prérequis
- ENV-28 terminée. Étape indépendante d'ENV-29 et d'ENV-31.
- `lepton/generate.py` (`tasks`, `_task`, `render_workspace`) ; interface `rapports/env-8-interface.md`
  (section `generate`) ; méthode de relevé d'ENV-25 (`rapports/env-25-dbg5.md` §3,
  `essais/env-25-releve/{avant,apres}`).
- Seul greffon qui fournit des tests : `bsp-qemu-mps2-an386` (`qemu-mps2-an386.peripheriques`,
  4 presets an386).
- Branche `devenv/env-30` dans lepton-tools.

## Tâches

### 1. Audit (lecture seule) → PA-47
- Tâches de test écrites aujourd'hui, pour chaque `execution` (`qemu`, `carte`) : libellés,
  arguments, `group`, `options`, `env`.
- Savoir, au moment de `generate`, si un preset a des tests de greffon. Sources possibles :
  - manifestes des greffons actifs (champ `tests`) ;
  - `ctest -N` d'un répertoire de construction, qui n'existe pas forcément.
- Configurations de carte : les tests de greffon y exigent `LEPTON_BOARD_SERIAL_PORT` (fixture
  `board_t0`). Relever comment l'éditeur le fournirait.
- Effet de l'extension Lepton (`extension/`) : lit-elle la liste des tâches ou leurs libellés ?
- Rapport `rapports/env-30-taches.md`.
- **PA-47** : l'utilisateur valide :
  - Configurations visées : <À CONFIRMER au PA-47 : QEMU seules, ou QEMU et carte>.
  - Tâche présente : <À CONFIRMER au PA-47>.
    - Option 1 : seulement si un greffon actif déclare des tests.
    - Option 2 : toujours, et la tâche ne trouve aucun test.
  - Libellé (`lepton : tests des greffons <preset>` proposé), arguments
    (`-L greffon: --output-on-failure` proposé), `group`.
- Aucune modification avant la réponse.

### 2. Implémentation (lepton-tools, `devenv/env-30`)
- Écrire les tests de lepton d'abord, rouges avant l'implémentation ; les 229 tests existants
  restent verts.
- `generate.py`, selon le PA-47 ; commentaires au niveau du code voisin.
- `rapports/env-8-interface.md`, section `generate` : la nouvelle tâche.
- Réinstaller lepton : `pipx install --force <LEPTON_TOOLS>` depuis le commit de l'étape.

### 3. Contrôles → PA-48
- Relevés `essais/env-30-releve/{avant,apres}` des fichiers générés : `<ROOTSTOCK>` et les
  rootstocks d'essai. Régénérer avant de relever (ORCHESTRATION §2bis). Diff limité à l'ajout de la
  tâche, dans les configurations décidées au PA-47.
- Exécuter la tâche en ligne de commande (même `ctest`, même `cwd`, même `env`) sur un preset
  an386 : `qemu-mps2-an386.peripheriques` réussi. Sur un preset sans test de greffon : effet
  conforme au PA-47.
- Essai VSCodium par l'utilisateur : tâche visible dans « Exécuter la tâche », résultat lisible.
- `lepton check` code 0. Aucune reconstruction requise (binaires non touchés) ; ne pas lancer
  d'oracle.
- **PA-48** : rapport ; fusion de `devenv/env-30` dans `main`, push (PA-P). La validation Debian
  est reportée à ENV-33.

## Critères de validation
- [ ] PA-47 et PA-48 tranchés et consignés.
- [ ] `pytest` vert, dont les nouveaux tests.
- [ ] Diff des relevés limité à la nouvelle tâche, configurations conformes au PA-47.
- [ ] Test du greffon d'essai lancé et réussi par la tâche (ligne de commande et VSCodium).

## Pièges connus
- `-L` de `ctest` est une expression régulière : `greffon:` sélectionne tous les greffons. Un
  libellé par greffon exigerait `greffon:<nom>$`. Hors périmètre, sauf décision au PA-47.
- `ctest -L greffon:` sélectionne aussi la fixture `smoke.lsh` : c'est attendu, ne pas l'exclure.
- Les tests sont servis par le trunk : conserver `PYTHONDONTWRITEBYTECODE=1` et `cwd` = trunk, comme
  les tâches voisines.
- Les espaces de travail des rootstocks d'essai écrits avant ENV-30 diffèrent aussi par les
  changements d'ENV-25 à ENV-27 s'ils n'ont pas été régénérés : relever « avant » après
  régénération par le lepton installé avant l'étape.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, branche, §Versions (lepton réinstallé), décisions PA-47 et PA-48,
journal. Passation `handoff/env-30.md`.
