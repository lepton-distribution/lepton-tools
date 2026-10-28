# ENV-12 lot 5 — F6 : vue IDE-1 (exécutif → bibliothèques → greffons → répertoires → fichiers) et L3-4

Session du 2026-10-27, branche `devenv/env-12` de lepton-tools. Décisions : `DEVENV-STATUS.md`
§Décisions (2026-10-27). Interface de lepton : `rapports/env-8-interface.md` §14.

## 1. Forme retenue

| Sujet | Décision |
| --- | --- |
| Niveaux exécutif et bibliothèques | Réponse de l'API fichier CMake (codemodel-v2) du preset actif, lue par lepton (`lepton seed tree`) ; sans réponse : vue réduite greffons → répertoires → fichiers, avec un message |
| Fichiers | Sources compilées, en-têtes `.h` des mêmes répertoires du greffon, et (essai, point 5) sources de ces répertoires compilées par aucune cible, « hors construction » ; ouverture par le trunk |
| Greffons | Entrées de `seed status` (calcul partagé) : état git en description et infobulle ; nœud « Greffons de la graine » pour les greffons qui ne compilent rien (projet, `building`) |
| Actions | Ouvrir, rafraîchir, nouveau fichier (répertoire), retirer du greffon (fichier), révéler dans le clone (gestionnaire de fichiers), sélectionner le dépôt git dans l'explorateur (essai, point 7) |
| L3-4 | Lien greffé supprimé du trunk par l'utilisateur : « Retirer du greffon » (`file remove`) ou « Restaurer le lien » (`graft --path`) |
| Preset actif | `build/.active/compile_commands.json` (CMake Tools), sinon premier preset configuré ; affiché sur le nœud exécutif (essai, point 1) |

## 2. Réalisation

| Commit | Contenu |
| --- | --- |
| ebda1d9 | lepton : `lepton/tree.py` (`seed tree [--preset] [--json]`), `seed.status_data`, requête `client-lepton` déposée par `generate`, `file owner` `kind: unlinked`, `file remove` / `graft --path` d'un lien absent ; tests `test_tree.py`, `test_owner.py`, `test_generate.py` ; interface §14 |
| c84ea49 | Extension 0.4.0 : conteneur « Lepton », vue `lepton.architecture` (`src/tree.ts`, `src/layout.ts`), L3-4 dans `src/watch.ts` (réglage `lepton.confirmTrunkDeletions`), activité de lepton dans `src/runner.ts` ; traductions ; test `layout.test.ts` |
| a7df487 | Essai : preset sur le nœud exécutif ; sources `unbuilt` (lepton) affichées « hors construction » |
| fc9a647 | Essai : « révéler dans le clone » par le gestionnaire de fichiers ; action « sélectionner le dépôt git dans l'explorateur » |

Rafraîchissement de la vue : après chaque commande lepton de l'extension, après une regreffe
automatique (F2) ou une adoption (F3), à la copie de la base du preset actif dans `build/.active` et à
toute nouvelle réponse `build/*/.cmake/api/v1/reply/index-*.json` ; différé tant que la vue est masquée.

L3-4 : les suppressions survenues pendant un lepton lancé par l'extension et dans les 3 s qui suivent
sont ignorées (liens retirés par lepton ou scion) ; au-delà de 20 suppressions groupées (suppression en
masse), aucune question, ligne dans le canal « Lepton ».

## 3. Contrôles

- `pytest` : 187 verts après ebda1d9 (180 avant le lot), 187 verts après a7df487.
- `npm test` : 17 verts (compactage des répertoires, résumé git, complétude des traductions).
- `scripts/bout-en-bout.sh` (lepton du venv) vert ; `~/lepton` inchangé.
- `lepton seed tree` sur `essais/env-11/qemu` (preset actif `env11-release-qemu`) : `lepton` →
  `lepton` (sources propres, noyau), `lib`, `generated` (généré), `kernel` (`lepton-noyau`,
  `qemu-mps2`), `kernel_demarrage`, `bsp_demarrage` (`qemu-mps2-an386`), `sbin`, `bin` ; `kal_bench`
  de même ; 1,1 s (`seed status` : 0,9 s).
- P3 : `essais/env-11/wl55jc1`, configuré en ligne de commande, sans réponse (vue réduite) ; après
  `lepton generate` et `cmake --preset env11wl-debug-board`, réponse lue (`kernel` : `lepton-noyau`,
  `stm32wlxx`).
- lepton réinstallé par pipx depuis l'arbre de `devenv/env-12` ; extension 0.4.0 installée ; espaces
  `essais/env-11/{qemu,f429zi,wl55jc1}` et `essais/env-9` régénérés (code 0).

## 4. Essai VSCodium (mode mixte, `essais/env-11/qemu`)

| # | Essai | Résultat |
| --- | --- | --- |
| 1 | Vue Lepton → Architecture, exécutif déplié, état git, nom du preset | Conforme après a7df487 : la description de la vue n'est pas affichée quand la vue est seule dans son conteneur (titre fondu `LEPTON: ARCHITECTURE`) ; preset déplacé sur le nœud exécutif |
| 2 | Vue comparée à `lepton seed tree` et `lepton seed status` | Conforme |
| 3 | Ouverture d'un fichier par son chemin du trunk | Conforme |
| 4 | Changement de preset (CMake Tools, debug ↔ release) : vue rafraîchie, preset changé | Conforme |
| 5 | Nouveau fichier `essai.c` dans un répertoire du BSP `qemu-mps2-an386` | Conforme après a7df487 : fichier créé dans le clone et lié dans le trunk, mais absent de la vue (non configuré, et hors des `sources` du BSP : jamais compilé) ; affiché « hors construction » |
| 6 | Retrait du fichier depuis la vue | Conforme |
| 7 | Révéler dans le clone | Conforme après fc9a647 : l'explorateur ne sélectionnait pas le fichier (masqué par `files.exclude` `scion/[!.]*`, P5) ; gestionnaire de fichiers + sélection du dossier « git · … » |
| 8 | L3-4 : lien supprimé dans l'explorateur, « Restaurer le lien » puis « Retirer du greffon » | Conforme, les deux réponses |

État laissé : clones du rootstock d'essai sans modification, graine `env11` à 107cd57, `essai.c` et
`essai2.c` absents, `lepton check` code 0, trunk sans fichier régulier ni lien cassé.

Critère d'ENV-12 « Vue IDE-1 cohérente avec `lepton seed status` » : satisfait (mêmes entrées, test
`test_tree_scions_are_seed_status`, essai 2).

## 5. Observations

| Id | Constat | Proposition |
| --- | --- | --- |
| L5-1 | Le noyau a aussi des sources « hors construction » (exclues par les listes de `cmake/components`, ex. 25 dans `sbin/` pour an386) : la vue les montre, comme IAR grise les fichiers exclus | Laissé (effet de la décision du point 5) |
| L5-2 | `lepton generate` crée `build/<preset>/` (requête `client-lepton`) avant toute configuration ; `seed config remove` annonce alors « répertoire de construction conservé » pour un preset jamais configuré | Laissé |
| L5-3 | L3-4 ne traite que les fichiers : un répertoire du trunk supprimé dans l'explorateur revient à la regreffe suivante, sans question (`file owner` : `absent`) | Laissé ; à revoir si l'usage le demande |
| L5-4 | `file add` d'une source ne reconfigure pas CMake (§3.7) : un fichier compilable reste « hors construction » jusqu'à la prochaine configuration (construction), puis la vue se rafraîchit | Laissé (décision du point 5, option sans reconfiguration) |
