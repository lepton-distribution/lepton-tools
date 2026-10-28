# ENV-12 lot 6 — session S1 : F7 en palette, `.vsix` installé, F8 (sources de l'arrêt par le trunk)

Session du 2026-10-27, branche `devenv/env-12` de lepton-tools. Décisions : `DEVENV-STATUS.md`
§Décisions (2026-10-27, lot 6). Interface de lepton : `rapports/env-8-interface.md` §15. Sessions
suivantes du lot : S2 (validation VSCodium F1-F8 et cartes, revue, push, consigne VM), S3 (VM Debian,
bilan).

## 1. Forme retenue

| Sujet | Forme |
| --- | --- |
| F7 en palette | « Lepton : ajouter une configuration à la graine » (nom, type de construction, cible : choix de la CLI) ; « … retirer une configuration de la graine » (choix parmi les configurations données par `seed status --json`, confirmation) ; « … importer un XML mklepton de référence dans la graine » (palette, ou menu contextuel d'un `.xml`) |
| `.vsix` (décision de l'utilisateur) | `extension/dist/lepton-<version>.vsix` versionné ; `install-vscodium.sh` l'installe si la version installée diffère de `extension/package.json` |
| F8 | Correspondance clone → trunk faite par l'extension sur les messages de l'adaptateur de débogage, d'après `stem` et `trunk` de `seed status --json` ; réglage `lepton.debug.trunkPaths` (défaut vrai) |

## 2. F8 — diagnostic (essai borné, plan §3)

| Étape | Constat |
| --- | --- |
| DWARF (`arm-none-eabi-readelf --debug-dump=info`/`=line`, `essais/env-11/qemu`, `env11-debug-qemu`) | `DW_AT_name` et table des lignes : chemins du **trunk** (`…/qemu/trunk/sys/root/src/…`), aucun chemin `depots/` ; `DW_AT_comp_dir` = répertoire de construction |
| gdb 17.2 (`info source`, MI `-break-insert`) | `Located in` / `fullname` = chemin du **clone** (`depots/lepton/bsp-qemu-mps2-an386/master/scion/…`) : gdb résout le lien à l'ouverture du fichier ; `set basenames-may-differ on` sans effet |
| Conséquence | `set substitute-path` (étape 2) sans objet : il réécrit le chemin du DWARF, déjà celui du trunk, avant la résolution ; `-ffile-prefix-map` non plus (même raison) |
| Cortex-Debug 1.13.0-pre6 | aucune option de correspondance de chemins (`package.json` : ni `sourceFileMap` ni `pathMappings`) ; il relaie `fullname` tel quel |
| Voie retenue (étape 3) | `DebugAdapterTracker` (`vscode.debug.registerDebugAdapterTrackerFactory("*")`) : `onDidSendMessage` réécrit en place tout `source.path` et `sources[].path` d'un message (pile, points d'arrêt, sources chargées) ; chemin sous un `stem` → `trunk/<relatif>` s'il existe, sinon inchangé ; table lue par `lepton seed status --json` à la création de chaque session |

## 3. Réalisation

| Commit | Contenu |
| --- | --- |
| 888b3d7 | lepton : champ `configurations` de `seed status --json` (et ligne du texte) ; `seed mkconf import` d'un chemin absolu du trunk (ramené au trunk ; hors trunk, chemin de clone compris : refus) ; tests `test_config_status_json`, `test_mkconf_import_chemin_absolu` ; interface §15 |
| 27e697f | Extension 0.5.0 : trois commandes F7 (`src/commands.ts`), F8 (`src/srcmap.ts` pur, `src/debug.ts`), réglage `lepton.debug.trunkPaths` ; `vscode:prepublish` (compilation avant `vsce`) ; `npm run package` → `dist/` ; `dist/lepton-0.5.0.vsix` ; tests `srcmap.test.ts`, `package.test.ts` (commandes déclarées enregistrées, un seul `.vsix` de la version) ; README |
| 085141f | `install-vscodium.sh` : `installer_extension_lepton` (après les extensions d'Open VSX), extension Lepton exclue du signalement « hors liste » ; README du dépôt |

## 4. Contrôles

- `pytest` : 189 verts (187 + 2).
- `npm test` : 21 verts (17 + 4).
- `shellcheck` 0.11.0 : `install-vscodium.sh` sans remarque.
- `install-vscodium.sh --dry-run --lepton-clone … --seed-scions …` : 2 changements annoncés
  (extension 0.4.0 → 0.5.0, lepton différent des sources), aucun « hors liste » ; puis exécution
  `--skip-toolchain` (chaîne non concernée, pas de `sudo`) : 2 changements, puis 0.
- `scripts/bout-en-bout.sh` (lepton du venv) : succès (cmake, fumée QEMU, trunk sain, `~/lepton`
  inchangé).
- lepton réinstallé par pipx (par `install-vscodium.sh`) ; extension 0.5.0 installée.

## 5. Essai VSCodium (mode mixte, `essais/env-11/qemu`)

| # | Essai | Résultat |
| --- | --- | --- |
| 1-4 | F8 : point d'arrêt ligne 48 de `qemu_mps2_board.c` posé par le trunk ; lancement « Déboguer env11-debug-qemu » ; arrêt sur `main` puis ligne 48 | conforme : un seul onglet, chemin du trunk, point rouge visible |
| 5 | F8 : cadres de la pile d'appels | conforme : fichiers ouverts sous `trunk/` |
| 6 | F8 : canal « Lepton » | conforme : `seed status --json` (code 0) puis « Session de débogage Déboguer env11-debug-qemu (QEMU mps2-an386) : sources affichées par le trunk (5 greffon(s)) » |
| B | Témoin : `lepton.debug.trunkPaths: false`, points 2 à 5 | tous les chemins de l'arrêt sous le clone (R3 reproduit) : l'effet est bien celui de F8 |
| 7 | F7 : ajout `essai-f7` (`MinSizeRel`, `qemu`) | conforme côté lepton : preset `env11-essai-f7` écrit (CMake Tools ne le liste qu'après rechargement de la fenêtre : L6-5, constaté et corrigé en S2 §11), presets et espace régénérés (premier essai : nom saisi « essai-f7, MinSizeRel, qemu », refusé par lepton, L6-1) |
| 8 | F7 : retrait `essai-f7` (liste avec type et cible, confirmation) | conforme ; graine identique à `HEAD` ensuite ; `build/env11-essai-f7/` (requête `client-lepton` seule, L5-2) supprimé après l'essai |
| 9 | F7 : import d'un XML (menu contextuel) sur la graine migrée | conforme : refus de lepton « déjà fourni par le greffon du projet » affiché |

R3 (`rapports/env-9-validation.md` §3, écart accepté en PA-1) est résorbé sur le Mac, sans
`-ffile-prefix-map`, sans `substitute-path` et sans modification du noyau. Cartes et Debian : S2, S3.

## 6. Observations

| ID | Observation | Suite proposée |
| --- | --- | --- |
| L6-1 | Palette F7 : la saisie du nom accepte toute chaîne ; un nom invalide est refusé par lepton (motif du schéma, message clair, aucune écriture) | Laissé (lepton contrôle) |
| L6-2 | `seed config remove` (et `add`) annonce « graine modifiée, non commitée » même quand la graine revient au contenu de `HEAD` | Laissé ; à revoir si gênant |
| L6-3 | Chaque lancement de débogage attend la lecture de `seed status --json` (≈ 1 s) avant de démarrer l'adaptateur | Laissé |
| L6-4 | F8 repose sur la modification en place du message par `onDidSendMessage` : l'hôte d'extensions de VSCodium 1.135 transmet le message après le traceur ; l'API ne le garantit pas | À revérifier à chaque changement de version de VSCodium (épinglée, PA-10) ; témoin B ci-dessus |

## 7. Propositions appliquées, à confirmer

- Champ `configurations` de `seed status --json` et ligne `configurations :` du texte.
- `seed mkconf import` d'un chemin absolu sous le trunk ; commande aussi au menu contextuel d'un `.xml`.
- F8 : traceur sur tous les types de débogage (`*` : Cortex-Debug, CodeLLDB pour mklepton), réglage
  `lepton.debug.trunkPaths` (défaut vrai) ; table lue à l'activation, après chaque commande et au début
  de chaque session, sans attente (0.5.1, L6-6 ; « relue à chaque session » en 0.5.0).
- `install-vscodium.sh` : extension installée même avec `--no-lepton` ; comparaison par numéro de
  version seulement (un `.vsix` reconstruit à version égale n'est pas réinstallé : changer la version).
- `vscode:prepublish` : `npm run package` compile toujours avant d'empaqueter.

## 8. Pièges

- `vsce package` n'empaquette que `out/` existant : sans `vscode:prepublish`, le premier `.vsix` 0.5.0
  contenait le code compilé du lot 5. Corrigé avant tout commit.
- Le `README.md` de l'extension est inclus dans le `.vsix` : réempaqueter après l'avoir modifié.

---

# Session S2 (2026-10-27) : validation VSCodium F1-F8, cartes, revue, consigne VM

Mode mixte (l'utilisateur agit dans VSCodium, la session contrôle en ligne de commande). Rootstocks
`essais/env-11/qemu` (`env11`), `f429zi` (`env11f4`), `wl55jc1` (`env11wl`) ; journaux
`essais/env-11/logs/s2-env12-*.log` (hors git).

## 9. Grille QEMU (`essais/env-11/qemu`)

| # | Fonction | Essai | Résultat |
| --- | --- | --- | --- |
| A1 | F1 (IDE-6) | palette `Lepton :`, « état de la graine » | conforme : 18 commandes en français, canal « Lepton » |
| A2 | F6 (IDE-1) | vue Architecture | conforme : exécutif `lepton · env11-debug-qemu`, 5 greffons identiques à `seed status` |
| A3 | F2 (FIC-1) | `touch` / `rm` de `essai_s2.c` dans le clone du BSP (terminal intégré : l'explorateur masque `scion/` des dossiers « git · … ») | conforme : lien ajouté puis retiré, liste greffée propre |
| A4 | F3 (FIC-3) | Nouveau fichier `essai_s2_trunk.c` dans le trunk | conforme : déplacé dans le clone, lien à sa place |
| A5 | L3-4 | lien supprimé du trunk, « Supprimer du greffon » | conforme : absent du clone et du trunk |
| A6 | F5 JSON (CFG-7) | `"type": "xyz"` sans enregistrer | conforme : erreur `lepton` à la saisie, retirée à l'annulation |
| A7 | F5 XML | `<inconnu/>` enregistré puis retiré | conforme |
| B1 | F4 (O10) | changement de preset CMake Tools | conforme |
| B2-B3 | F7 | ajout / retrait de `essai-s2` | lepton conforme ; **CMake Tools ne relit pas les presets sans rechargement : L6-5** ; après correction (480cf83) : conforme sans rechargement |
| B4 | F7 | import du XML `mkconf_tauon_basic_qemu_mps2.xml` (menu contextuel) | conforme : refus « déjà fourni par le greffon du projet », code 1 |
| B5-B7 | F8, DBG-1, DBG-2 | point d'arrêt ligne 48 de `qemu_mps2_board.c`, pile, pas à pas, registres | 1er lancement après rechargement : onglet sous `depots/` (**L6-6**) ; lancements suivants : conforme |

Contrôle après la grille : aucun `essai_s2*`, clones et graine propres, `seed status` « aucun fichier
régulier, aucun lien cassé », `lepton check` code 0 ; `build/env11-essai-s2/` (requête
`client-lepton` seule, L5-2) supprimé.

## 10. Cartes (PA-11 accordé pour la session)

| Carte | Sonde | Essai | Résultat |
| --- | --- | --- | --- |
| NUCLEO-F429ZI | ST-LINK/V2-1 0672FF495252717267243842, `/dev/cu.usbmodem145103`, 3,23 V | « Déboguer env11f4-debug-board (carte, OpenOCD) », point d'arrêt ligne 187 de `nucleo_f439zi_board.c` (`dev_nucleo_f439zi_board_load`) | arrêt sur `main` et ligne 187 ; 1re session : onglet sous `depots/` (L6-6) ; après 0.5.1, fenêtre neuve : sous `trunk/` dès la 1re session ; registres lisibles |
| NUCLEO-F429ZI | — | `verify_image` (OpenOCD, lecture seule) de `lepton.elf` | conforme : seuls 4 octets `0x080001ac-af` diffèrent (bourrage d'alignement entre `.isr_vector` et `.text`, non écrit par `load` de gdb qui écrit les sections ; `verify_image` compare le segment) |
| NUCLEO-WL55JC1 (M4) | STLINK-V3 002700253431510837393937 (carte A), `/dev/cu.usbmodem1454303`, 3,28 V | même lancement, fenêtre neuve, point d'arrêt ligne 128 de `dev_stm32wl55jci_nucleo_usart_2.c` (`…_usart_2_load`) | conforme dès la 1re session (onglet sous `trunk/`) ; registres lisibles ; octets d'option et M0+ non touchés |
| NUCLEO-WL55JC1 | — | `verify_image` | conforme, code 0 (aucun bourrage : `.text` suit `.isr_vector`) |

Premier point d'arrêt WL55 (ligne 120 de `dev_stm32wl55jci_nucleo_board.c`) non atteint : le pilote
de carte n'est pas dans le XML `mkconf_env11wl.xml` (non compilé, symbole absent) ; erreur de la grille,
pas de l'extension. DBG-4 (vue Périphériques) non vérifiable : aucun BSP ne déclare `svd`
(`rapports/env-9-generation.md`, PA-7 Q11), hors F0-F8.

## 11. Défauts constatés et corrigés (décisions de l'utilisateur, 2026-10-27)

| ID | Défaut | Cause | Correction |
| --- | --- | --- | --- |
| L6-5 | Preset ajouté / retiré par `seed config add/remove` (ou `generate`) invisible dans CMake Tools jusqu'au rechargement de la fenêtre | CMake Tools 1.24.42 observe `trunk/CMakeUserPresets.json` (`createFileSystemWatcher(RelativePattern(trunk, …))`) ; l'observateur de VSCodium ne suit pas les liens : la réécriture de la cible dans le greffon projet n'émet rien sur le chemin du lien. Preuve : `touch -h` du lien (lancé par l'utilisateur, le hook refusant toute écriture sous `trunk/`) → presets relus | 480cf83 : `generate` avance la date du lien (`os.utime(…, follow_symlinks=False)`) quand les presets changent ; test `test_presets_link_touched_when_changed` ; interface §15 |
| L6-6 | F8 sans effet à la 1re session de débogage d'une fenêtre (QEMU B5, F429), message « sources affichées par le trunk » pourtant écrit | VSCodium 1.135 (`extensionHostProcess.js`) : `Promise.race([Promise.all(trackers), setTimeout(…, 1e3)])` — un traceur rendu après 1 s est abandonné sans signal ; la fabrique attendait `seed status --json` dans la file de lepton, chargée à l'ouverture | 009a049, extension 0.5.1 : table lue à l'activation, après chaque commande et au début de chaque session en arrière-plan ; traceur rendu immédiatement ; règle aussi L6-3 |
| L6-7 | « Erreur : référence de problemMatcher non valide : $gcc » ; erreurs de compilation des tâches hors *Problèmes* (depuis ENV-9) | `$gcc` est fourni par l'extension C/C++ de Microsoft, absente (clangd, Open VSX) | 0733006 : `GCC_MATCHER` écrit dans les tâches « construire » et « mklepton » ; test `test_build_tasks_gcc_matcher` ; espaces d'essai régénérés ; essai F429 : erreur injectée vue dans *Problèmes* (source `gcc`), retirée |

Contrôles : `pytest` 191 verts ; `npm test` 21 verts ; `.vsix` 0.5.1 (`dist/`, 0.5.0 retiré) ;
`install-vscodium.sh --skip-toolchain` : 2 changements (extension 0.5.0 → 0.5.1, lepton) puis 0.

## 12. Revue « aucune logique de graine ou de greffon dans `extension/` »

Lecture des 12 modules de `extension/src/` (≈ 1 790 lignes, 0.5.1). Toute décision sur la graine,
les greffons, le propriétaire d'un fichier, les configurations ou les refus vient de lepton
(`seed status|tree --json`, `file owner --json`, `check --json [--stdin]`) ; l'extension recueille
les arguments, appelle lepton en sous-processus (`lepton.ts`, file unique `runner.ts`) et affiche.
Critère respecté. Deux écarts mineurs, sans décision propre :

| ID | Constat | Suite proposée |
| --- | --- | --- |
| R-1 | Correspondance `stem/<relatif>` ↔ `trunk/<relatif>` (`srcmap.ts` F8, `tree.ts` « révéler dans le clone » d'un répertoire) : convention de greffe de scion à la racine, recalculée par l'extension (F8 vérifie l'existence du lien) | Laisser (donnée de `seed status`, même règle que la vue) ; à défaut, champ de lepton donnant la correspondance |
| R-2 | Énumérations recopiées de la CLI dans les saisies : types de greffon (`seedAdd`, `scionNew`), types de construction et cibles (`seedConfigAdd`) | Laisser (lepton refuse une valeur hors liste) ; à défaut, exposer ces listes par lepton |
| — | Heuristiques d'éditeur sans rapport avec la graine : délais de regroupement, `UNLINK_MAX` (20), `LEPTON_QUIET_MS` (3 s) ; noms `lepton-greffon.json` / `lepton-graine.json` fixés par la spécification ; motif XML pris dans `xml.fileAssociations` écrit par `generate` | Conforme |

## 13. Observations

| ID | Observation | Suite proposée |
| --- | --- | --- |
| L6-8 | Le matcher gcc (L6-7) fait apparaître dans *Problèmes* les avertissements existants du code Lepton : 188 sur une construction complète de `env11f4-debug-board` (140 `struct _reent` dans `~/lepton/third_party`, 25 `struct stat` dans `kernel/fs`, 10 `-Wpointer-compare`, macros redéfinies) | Hors environnement : code du noyau ; journal `logs/s2-env12-f429-warnings.log` |
| L6-9 | L'essai F2 passe par un terminal : l'espace masque `scion/[!.]*` des dossiers « git · … » (voulu, P5 / PA-1) ; l'explorateur ne crée pas dans un clone | Laisser ; la création par le trunk (F3) ou la vue (F6) couvre l'usage |
| L6-10 | Cortex-Debug écrit l'image par `load` de gdb : pas de « verified » dans la console ; la preuve du flash est `verify_image` | Laisser ; noter dans `lepton-cibles` si utile |

## 14. Consigne VM

`consignes/env-12-debian.md` (S3, ordre `R12-1`, §2bis) : installation n° 1 et n° 2 (pack de langue,
locale, extension 0.5.1, lepton), migration O5 de la graine `env11` de la VM, F1-F8, L3-4, L6-5,
L6-6, L6-7 sous Debian (F8 sous `gdb-multiarch`, QEMU), témoin F8, `pytest` 191.
