# Étape ENV-51 — lepton : messages de scion relayés (D10)

## Contexte
Révision du plan du 2026-11-12, faite à partir de `HORS-PLAN.md` : D10 est à traiter (décision de
l'utilisateur du 2026-11-10). lepton ne relaie pas les messages d'information de scion lors de
`seed remove`, `seed replace` et `seed add`, même avec `-v` : « clés projetées retirées avec leur
porteur … » (P-P6) et « … regreffées avec leur porteur … » (P-G6) n'apparaissent pas
(`rapports/env-44-residus.md` §4.3, O-2).

Fait relevé à la révision : `lepton/scion_runner.py`, fonction `run`, lance scion avec
`capture_output=True` et ne rend la sortie qu'en cas d'échec ; `-v` n'affiche que la commande
exécutée. La cause exacte et l'étendue sont à établir par l'audit.

Archétype : infrastructure (outillage). Aucun binaire ni aucun lien du trunk ne doit changer.

## Prérequis
- ENV-50 terminée. lepton-tools `main` : fusion de la révision du 2026-11-12, après a7fcb62 ;
  lepton 0.1.0 ; scion 0.6.2.0.
- Spécification des messages de scion : `<SEED_SCIONS>/doc/projection-miroir.md` §A.9 (P-P6),
  §A.10 (P-G6), §A.12. scion écrit ces messages par `logging` (`log.info`), donc sur stderr
  (`scion/cli.py`, `logging.basicConfig`).
- Code (relevé au 2026-11-12, numéros indicatifs) : `lepton/scion_runner.py` (`run`, `scion`) ;
  `lepton/seed.py` (`scion_on_trunk`, `_info`, `_warn`, `add_scion`, `seed_remove`, `seed_replace`,
  `_attach`, `_restore`) ; `lepton/files.py` (`graft` aux lignes 222 et 415) ; `lepton/scions.py`.
- Extension : `extension/src/commands.ts` lance par `runner.run` `graft`, `seed add`, `remove`,
  `replace`, `lock`, `scion new`, `scion remove`, `file add`, `remove`, `mv`, `dir add`, `remove` ;
  `extension/src/runner.ts` traite à part les commandes `--json`. Ses notifications d'échec
  (`runner.ts`, `watch.ts`, `tree.ts`) prennent sur stderr les lignes qui suivent la dernière
  ligne commençant par `lepton:` (`lastMessage`, `extension/src/lepton.ts`).
- Tests : `tests/test_projection.py` (dont `test_seed_replace_porteur_garde_les_projections`) ;
  venv `~/lepton-tools-dev/venv-lepton-tools`.
- Skill `lepton-rootstock` (rootstock d'essai).
- Branche `devenv/env-51` dans lepton-tools seulement.

## Tâches

### 1. Audit (lecture seule) → PA-89
- Chemin d'un message de scion jusqu'à l'utilisateur : `run` (stdout, stderr, code), puis chaque
  appelant qui lit ou ignore `CompletedProcess`.
- Inventaire, dans `rapports/env-51-messages.md` §1 : chaque commande de lepton qui appelle scion,
  la commande scion lancée, ce que scion écrit (stdout, stderr) et ce que lepton en affiche. Couvrir
  au moins `seed new`, `seed add`, `seed remove`, `seed replace`, `seed lock` (restauration),
  `scion new`, `scion remove`, `file add`, `file remove`, `file mv`, `dir add`, `dir remove` et
  `graft`.
- Essai sur un rootstock d'essai à graine de projet, jamais sur `<ROOTSTOCK>`. Sur la graine de
  référence `original-tree`, `refuse_reference` refuse `seed add` (`lepton/seed.py:600`),
  `seed replace` et `seed remove` (`_seed_context`, l. 575), `seed lock` (l. 823), `scion new` sans
  `--no-seed` (`lepton/scions.py:120`) et `scion remove` (par `seed_remove`). Rootstock d'essai :
  `essais/env-51-essai`, copie d'`essais/env-11/f429zi` (graine de projet, famille F4 porteuse de
  projections) par `rsync -a` sans `build/` ni `third_party/`, forme des essais A et B d'ENV-44
  (`rapports/env-44-residus.md` §3.1). Relever la sortie de lepton, puis celle de la même commande
  scion lancée à la main.
- Effets possibles :
  - commandes à sortie JSON (`seed status --json`, `seed tree --json`, `check --json`,
    `file owner --json`) lues par l'extension ;
  - canal de sortie de l'extension pour les commandes lancées par `runner.run` ;
  - notifications de l'extension : une ligne de scion relayée sur stderr après un `_warn` de lepton
    entre dans le texte de `lastMessage` ;
  - messages de lepton déjà émis (`_info` sur stdout, `_warn` sur stderr).
- **PA-89** : l'utilisateur tranche :
  - commandes couvertes : <À CONFIRMER au PA-89> ;
  - forme du relais : <À CONFIRMER au PA-89>. Options : sortie de scion relayée en entier ; lignes
    d'information seules ; relais sous `-v` seulement ;
  - flux (stdout ou stderr) et ordre par rapport aux messages de lepton : <À CONFIRMER au PA-89> ;
  - préfixe éventuel des lignes relayées, et effet sur `lastMessage` de l'extension si le relais
    passe par stderr : <À CONFIRMER au PA-89> ;
  - tests : forme et emplacement.
- Aucune modification avant la réponse.

### 2. Correction (`devenv/env-51`)
- Écrire les tests d'abord : un test par commande retenue, avec le message de scion attendu :
  P-P6 au retrait d'un porteur et P-G6 à sa regreffe (`seed add`, `remove`, `replace`) ; pour les
  autres commandes retenues, le message relevé par l'inventaire de la tâche 1. Ils échouent sur
  `main`.
- Puis la correction, dans `scion_runner.py` ou chez les appelants, selon le PA-89. Un seul
  mécanisme : ne pas dupliquer le relais commande par commande.
- Mettre à jour `README.md` si le comportement de `-v` ou la sortie des commandes change.
- Réinstaller lepton : `pipx install --force <LEPTON_TOOLS>` depuis la branche.

### 3. Contrôles → PA-90
- `pytest` complet vert (377 tests après ENV-50, plus les nouveaux).
- Essais de la tâche 1 rejoués : les messages P-P6 et P-G6 apparaissent ; codes de retour inchangés.
- Sorties `--json` inchangées : `json.loads` sur la sortie de chaque commande `--json` d'un rootstock
  d'essai, avant et après.
- Extension : sortie des commandes de la tâche 1 lue dans le canal de l'extension, ou raison de ne
  pas l'essayer au rapport.
- **PA-90** : rapport ; sort d'`essais/env-51-essai` ; push et fusion de `devenv/env-51` dans
  `main` (PA-P).

## Critères de validation
- [ ] PA-89 et PA-90 tranchés et consignés.
- [ ] Inventaire de la tâche 1 au rapport, avec la sortie relevée avant et après.
- [ ] Nouveaux tests : échec sur `main`, réussite sur la branche ; `pytest` complet vert.
- [ ] Sorties `--json` identiques avant et après.
- [ ] `HORS-PLAN.md` : D10 marqué traité, avec renvoi au rapport.

## Pièges connus
- Relayer sur stdout une commande `--json` casse sa lecture par l'extension (`json.loads`).
- `scion_on_trunk` affiche déjà « fichier système supprimé du trunk » : garder l'ordre des messages
  lisible.
- `run` sert aussi à `git` et aux autres outils : ne pas relayer leur sortie par effet de bord.
- lepton n'accepte une URL `file://` qu'avec un hôte (`file://localhost/…`) ; sans hôte, elle est lue
  comme un chemin local (piège d'ENV-44).
- Les rootstocks d'essai d'ENV-44 (`essais/env-44-d1-*`) n'existent plus (relevé du 2026-11-12).
  Ne jamais lancer l'essai dans `essais/env-11/f429zi` lui-même : ENV-53 le regreffe.
- `zsh` ne découpe pas une variable en mots : utiliser `bash -c` ou un script.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, branche, §Versions (lepton, s'il est réinstallé), décisions PA-89 et
PA-90, journal. `HORS-PLAN.md` : D10. Passation `handoff/env-51.md`.
