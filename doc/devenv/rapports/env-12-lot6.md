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
| 7 | F7 : ajout `essai-f7` (`MinSizeRel`, `qemu`) | conforme : preset `env11-essai-f7`, presets et espace régénérés (premier essai : nom saisi « essai-f7, MinSizeRel, qemu », refusé par lepton, L6-1) |
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
  `lepton.debug.trunkPaths` (défaut vrai), table relue à chaque session.
- `install-vscodium.sh` : extension installée même avec `--no-lepton` ; comparaison par numéro de
  version seulement (un `.vsix` reconstruit à version égale n'est pas réinstallé : changer la version).
- `vscode:prepublish` : `npm run package` compile toujours avant d'empaqueter.

## 8. Pièges

- `vsce package` n'empaquette que `out/` existant : sans `vscode:prepublish`, le premier `.vsix` 0.5.0
  contenait le code compilé du lot 5. Corrigé avant tout commit.
- Le `README.md` de l'extension est inclus dans le `.vsix` : réempaqueter après l'avoir modifié.
