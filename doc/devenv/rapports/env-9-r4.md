# Reprise 4 — ENV-9 N4, O8, O10, O11

Reprise n° 4 du bilan ENV-11 (`env-11-bilan.md` §3) : N4 (CFG-7), O8 (DBG-3), O10 (IDE-3), O11
(IDE-5), constatés en ENV-11 S2 (`env-11-mac.md` §2bis, §3-§4). Session du 2026-10-16, branche
`devenv/env-9-r4` (lepton-tools seul), depuis `main` 4c93b8e (fusion `--no-ff` de `devenv/env-8-r3`).

## 1. Décisions (utilisateur, 2026-10-16)

| Sujet | Décision |
| --- | --- |
| N4 | Associations vers les schémas du paquet lepton (`schemas_dir()`), chemin absolu résolu à la génération |
| O8 | `lepton generate --probe-serial SERIAL`, conservé dans l'espace ; `""` le retire |
| O10 | `lepton generate` amorce `build/.active` depuis le premier preset configuré ; `cmake.configureOnOpen` inchangé (`false`) |
| Validation | Mode mixte, éditeur et deux cartes branchées dans la session |
| Gravité des fautes JSON (après A3) | (1) avertissement du service intégré accepté ; (2) tâche « lepton : vérifier » en erreur ; (3) diagnostics en erreur à la saisie inscrits pour ENV-12 (`etapes/ENV-12-extension.md` §2bis) |

## 2. Corrections (lepton-tools 0ede3ee ; f4e9bb8 pour la tâche « lepton : vérifier »)

| ID | Correction (`lepton/generate.py`, sauf mention) |
| --- | --- |
| O11 | Réglage `"cmake.options.statusBarVisibility": "visible"` (défaut `hidden` de CMake Tools 1.24.42). |
| N4 | `schema_settings` : `json.schemas` (`**/lepton-greffon.json` → `greffon.schema.json`, `**/lepton-graine.json` → `graine.schema.json`, URI `file://`) ; `xml.fileAssociations` (`**/mkconf_*.xml`, plus `**/<mklepton_xml de la graine>` si celui-ci sort du motif → `mklepton.xsd`). |
| O8 | Option `--probe-serial` (`lepton/cli.py`) ; valeur conservée dans le réglage `lepton.probeSerial` de l'espace et reprise sans l'option ; refus d'une valeur à espace, guillemet ou `\` (code 1, rien d'écrit). Configurations carte : `openOCDLaunchCommands: ["adapter serial S"]` (Cortex-Debug 1.13.0-pre6 n'applique pas `serialNumber` à OpenOCD) ; tâche « flasher » : `-c "adapter serial S"` après les `-f`. Sans série : avertissement (une carte à la fois). |
| O10 | `prime_active` : `build/.active/compile_commands.json` absent → copie de celui du premier preset de la graine déjà configuré ; jamais écrasé (CMake Tools le tient à jour) ; aucun preset configuré → avertissement (configurer, puis relancer clangd ou `lepton generate`). |

| CFG-7 (option 2) | f4e9bb8 : tâche « lepton : vérifier » (`lepton check -C <rootstock>`), `problemMatcher` en erreur (`CHECK_MATCHER` : fichier, ligne xmllint facultative, message ; `fileLocation` autoDetect sur le rootstock). `lepton/checks.py` `_manifest_label` : manifeste greffé désigné par son chemin du trunk quand le lien y mène (sinon le clone), pour que *Problems* ouvre le chemin canonique (IDE-4, PA-1) ; manifeste de graine inchangé (dépôt de la graine seul). |

README : usage (schémas, sélecteur, amorce, `--probe-serial`, relevé du numéro de série, tâche « lepton : vérifier »).
Tests : `test_probe_serial_kept_in_workspace`, `test_schema_associations`,
`test_active_compile_commands_primed`, assertion O11 (0ede3ee : `pytest` 135 verts, 132 avant) ;
`test_check_task_reports_errors`, `test_check_names_grafted_manifests_by_trunk` (f4e9bb8 : 137 verts).

## 3. Essai clangd préalable (O10)

`env-9-r4-essai-clangd.py` (client LSP minimal, clangd 21.1.8 `--compile-commands-dir` vide au
démarrage, base écrite ensuite, projet C de 3 fichiers) :

| Instant | Définition de `compte()` |
| --- | --- |
| base absente | `src/main.c` (déclaration implicite) |
| base écrite, + 30 s | `src/main.c` |
| après une modification du fichier ouvert | `src/def.c` |

clangd ne relit la base qu'à la reconstruction d'un fichier ouvert : conforme à l'hypothèse du plan,
l'amorce est nécessaire. Limite : sans aucun preset configuré avant l'ouverture, la relance de
clangd reste nécessaire (relance automatique : ENV-12).

## 4. Preuves en ligne de commande

| Contrôle | Résultat |
| --- | --- |
| `lepton generate` sur `essais/env-11/{qemu,f429zi,wl55jc1}` | presets « inchangé » ; espace : seuls les réglages changent (diff hors `settings` vide) |
| deuxième génération | « inchangé » ×2 |
| amorce | `qemu` (`.active` supprimé) et `wl55jc1` (absent) : « amorcé … (preset env11-…) », copie identique (`cmp`) |
| O8 sans série, deux cartes | cfg F4 : sonde V3 prise, `Error: expected 1 of 1: 0x2ba01477`, code 1 (O8 reproduit) |
| O8 avec `-c "adapter serial …"` après `-f` | F4 : STLINK V2J27M15 0483:374B, Cortex-M4 détecté, code 0 ; WL : STLINK V3J7M3 0483:374E, code 0 |
| `--probe-serial` puis génération sans l'option | série conservée (« sonde : adapter serial … ») |
| `scripts/bout-en-bout.sh` (lepton de la branche), après 0ede3ee puis après f4e9bb8 | succès ; `~/lepton` inchangé (0 fichier régulier, 0 lien cassé, clone noyau propre) |
| `lepton check` sur `essais/env-11/qemu`, fautes enregistrées dans les clones d'essai (`"type": "xyz"` du noyau, `<inconnu/>` ligne 9 du XML), puis retirées (`git checkout`) | 3 anomalies au format du motif ; manifestes désignés par `trunk/…` après f4e9bb8 ; après retrait : 5 fichiers conformes, clone propre |

Sondes : F429ZI ST-LINK/V2-1 0672FF495252717267243842 ; WL55JC1 carte A STLINK-V3
002700253431510837393937 (`lepton-cibles`).

## 5. Validation dans VSCodium (mode mixte)

Espaces générés par le lepton de la branche (installation éditable : schémas sous
`lepton-tools/schemas/` ; après fusion et `pipx install`, sous le paquet installé).

| Essai | Résultat | Exigence |
| --- | --- | --- |
| A1 — `essais/env-11/qemu`, `.active` amorcé, F12 sur `bin_lst` (`kernel/core/bin.c`) sans relance de clangd | définition ouverte | IDE-3 (O10) |
| A2 — sélecteur de preset dans la barre d'état ; `qemu-mps2-an386-freertos` puis retour | visible, reconfiguration | IDE-5 (O11) |
| A3 — XML : `<inconnu/>` sous `<mklepton>` | erreur signalée à la saisie | CFG-7 (N4) |
| A3 — `lepton-graine.json`, clé `backend` renommée `xyz` | `Missing property "backend"` (portée : objet racine, document entier souligné) et `Property xyz is not allowed` (ligne 11) ; gravité avertissement | CFG-7 (N4) |
| A3 — `lepton-greffon.json`, clé `type` renommée `xyz` | même comportement | CFG-7 (N4) |
| C1, D1 — deux cartes branchées, tâche « flasher » | F4 : `STLINK V2J27M15 (API v2) 0483:374B` ; WL : `STLINK V3J7M3 (API v3) 0483:374E` ; écriture vérifiée | DBG-3 (O8) |
| C2, D2 — débogage carte, deux cartes branchées | arrêt sur `main` sur chaque carte | DBG-3 (O8) |
| D3 — `essais/env-11/wl55jc1` amorcé, F12 sans relance | définition ouverte | IDE-3 (O10) |
| E1 — tâche « lepton : vérifier », fautes enregistrées | échec de la tâche, 3 erreurs rouges dans *Problems* (manifeste du noyau, graine, XML ligne 9) | CFG-7 |
| E2 — clic sur l'erreur du manifeste | 1er essai : ouvert sous `depots/…` (la tâche appelait le lepton pipx de `main`, sans `_manifest_label`) ; espace régénéré avec le venv de la branche en tête du PATH : ouvert sous `trunk/sys/root/src/lepton-greffon.json` | IDE-4 |
| E3 — clic sur l'erreur XML | ouvert ligne 9, sous le trunk | IDE-4 |

Écart : le service JSON intégré signale les fautes de schéma en avertissement (orange), le XML
(lemminx) en erreur ; aucun réglage de l'espace ne change cette gravité (VSCodium 1.135 : le
serveur lit `json.validate.schemaValidation`, mais le client ne transmet que
`json.validate.enable`). Décision de l'utilisateur : accepté, complété par la tâche « lepton :
vérifier » (erreurs, à la demande) ; diagnostics en erreur à la saisie renvoyés à ENV-12.

## 6. Conclusion

| Renvoi | Résultat |
| --- | --- |
| N4 | corrigé ; CFG-7 conforme (P2) : avertissement à la saisie (JSON), erreur (XML), erreurs à la demande par « lepton : vérifier » ; erreur à la saisie : ENV-12 |
| O8 | corrigé ; DBG-3 sans restriction « une carte à la fois » |
| O10 | corrigé si un preset est configuré avant `lepton generate` ; sinon relance de clangd (ENV-12) |
| O11 | corrigé ; réserve IDE-5 levée |
