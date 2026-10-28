# ENV-12 — Validation Debian de l'extension 0.5.1 (lot 6 S3) — 2026-10-28

Session VM Debian conduite selon `doc/devenv/consignes/env-12-debian.md` (ordre `R12-1` de la
session Mac lepton-tools-2b), en mode mixte : actions dans VSCodium faites par l'utilisateur,
contrôles en ligne de commande par la session VM. Journaux : `~/env-12-journaux/` sur la VM (hors
git) ; journaux de VSCodium sous `~/.local/state/VSCodium/<horodatage>/` (§5, O-c).

Bilan : INS, O5, F1 à F8, L3-4, L6-5, L6-6, L6-7 conformes ; pytest 191 réussis. F1 n'est conforme
qu'au second lancement de VSCodium (premier lancement en anglais, §5 O-a). Deux défauts communs
relevés et non corrigés (§5, D-a et D-b). Aucune correction propre à Debian.

## 1. Hôte

| Élément | Valeur |
| --- | --- |
| Système | Linux x86_64, Debian 13.7, noyau 6.12.107+deb13-amd64, utilisateur `lepton-user` |
| VSCodium | 1.135.06055 |
| scion | 0.5.1.1 avant et après |
| lepton | 0.1.0 avant et après ; réinstallé depuis les sources de 0b4e96e (INS n° 1) ; `lepton --version` : `lepton 0.1.0` / `scion 0.5.1.1 (requis ≥ 0.5.1.1)` |
| Locale de VSCodium | avant : « pas de locale » ; après : `"locale": "fr"` dans `~/.vscode-oss/argv.json` |
| Outils | `/usr/bin/xmllint`, `/usr/bin/clangd`, `/usr/bin/gdb-multiarch`, `/usr/bin/qemu-system-arm` présents |
| `fs.inotify.max_user_watches` | 30075 avant (< 65536 : arrêt du §5) ; relevé à 524288 par l'utilisateur (`echo 524288 > /proc/sys/fs/inotify/max_user_watches`, sudo, non persistant), décision de l'utilisateur ; rootstock d'essai : 1898 répertoires ; `max_user_instances` 128 |
| Espace | `/tmp` 747 Mo (647 Mo libres) ; `/home` 26 Go (20 Go libres) |
| Rootstock d'essai | `~/lepton-tools-dev/essais/env-11/qemu` (graine `env11`, FreeRTOS, an386) ; `lepton seed status` code 0, 5 greffons, trunk sans fichier régulier ni lien cassé |

Têtes des clones après §4 : lepton-tools `devenv/env-12` = `origin/devenv/env-12` 0b4e96e ;
lepton-noyau `master` = `origin/master` 16a331b ; seed.scions tag `0.5.1.1` = f1d1f3c, copie de
travail laissée détachée sur 79f4f96 (0.5.1.0), sans effet : `install-vscodium.sh` installe scion
depuis le tag (`git+file://…@0.5.1.1`), avis de la session Mac.

Extensions avant : `anthropic.claude-code@2.1.300`, `llvm-vs-code-extensions.vscode-clangd@0.6.0`,
`marus25.cortex-debug@1.13.0-pre6`, `mcu-debug.debug-tracker-vscode@0.0.15`,
`mcu-debug.memory-view@0.0.29`, `mcu-debug.peripheral-viewer@1.6.4`, `mcu-debug.rtos-views@0.0.16`,
`ms-vscode.cmake-tools@1.24.42`, `redhat.vscode-xml@0.29.3`, `vadimcn.vscode-lldb@1.12.3`.
Après : les mêmes, plus `lepton-distribution.lepton@0.5.1` et
`ms-ceintl.vscode-language-pack-fr@1.131.0`.

Graine `env11` au §5 : modifiée, non commitée (arrêt du §5) : `+ lepton project-env11 *` dans
`scion/.scion/.scion.ramifications` et `.scion.sources.list`, `project/scion/CMakeUserPresets.json`
non suivi. Fichiers datés du 2026-10-15 (ENV-11), déjà relevés dans `env-10-r5-debian.md` §2.
Décision de l'utilisateur : commit séparé avant O5 (§2, 5.0).

## 2. Scénario

| ID (§1) | Étape | Commande ou action (résumé) | Résultat |
| --- | --- | --- | --- |
| — | 5.0 | `git -C …/env11 commit` des trois éléments d'ENV-11 | commit 8539dfa « presets générés (lepton generate) » : `CMakeUserPresets.json` +44, `.scion.ramifications` +1, `.scion.sources.list` +1 ; identique au 74f6e20 du Mac ; graine propre |
| INS | 6.1 | `install-vscodium.sh --lepton-clone … --seed-scions …` (lancé par l'utilisateur) | code 0, `changements 4` : `ms-ceintl.vscode-language-pack-fr` v1.131.0 installé ; « Extension 'lepton-0.5.1.vsix' was successfully installed » ; `locale : (absente) → 'fr'` ; « lepton 0.1.0 : paquet installé différent des sources (ou hors pipx) : réinstallation » → pipx « installed package lepton 0.1.0, Python 3.13.5 ». Ligne « Extension Lepton … : (absente) → 0.5.1 » absente (§5, O-d) |
| INS | 6.2 | même commande | code 0, « lepton 0.1.0 : déjà installé, identique aux sources », **`changements 0`** |
| O5 | 6.3 | `lepton check` avant | code 0, « attention : … mkconf_tauon_basic_qemu_mps2.xml : XML fourni par un greffon partagé, pas par la graine (CFG-1, O5) » |
| O5 | 6.3 | `lepton seed mkconf import sys/user/tauon-basic/etc/mkconf_tauon_basic_qemu_mps2.xml` | code 0, « XML du projet : sys/user/env11/etc/mkconf_env11.xml (copie de …, avec .boot, .init) » ; `trunk/sys/user/env11/etc/{mkconf_env11.xml,.boot,.init}` : liens vers la graine |
| O5 | 6.3 | `lepton generate` ; commit de la graine | code 0 ; commit 6d3d2a5 « XML mklepton du projet dans la graine (lepton seed mkconf import, O5) ; presets régénérés » (5 fichiers, +86 −2 ; `mklepton_xml` → `sys/user/env11/etc/mkconf_env11.xml`) |
| O5 | 6.3 | `lepton check` après | code 0, « 5 fichier(s) conforme(s) », aucun avertissement O5 |
| — | 6.3 | `seed status`, `seed tree --json` | `configurations : debug-qemu (Debug, qemu)` (pas de `release-qemu` sur la VM) ; avant configuration CMake : `env11-debug-qemu`, source `manifests`, `executables []`, « preset env11-debug-qemu non configuré (aucune réponse de l'API fichier CMake …) », comportement voulu (avis Mac) ; après configuration par CMake Tools (6.4) : source `codemodel`, `[kal_bench, lepton]` |
| F5 | 6.3 | `check --json --stdin` (`"noyau"` → `"xyz"`) | une anomalie `/type`, ligne 3, colonnes 11-16, « valeur "xyz" hors de la liste […] » ; md5 du fichier inchangé |
| L6-7 | 6.3 | `grep -c '$gcc'` / `'lepton-gcc'` dans `env11.code-workspace` | 0 / 2 |
| F1 | 6.4 | palette `Lepton :` (premier lancement après INS) | **non conforme** : 20 commandes en anglais ; cache `extensions.user.cache` et `extensions.builtin.cache` : `"language": "en"`, aucune traduction (§5, O-a) |
| F1 | 6.4 | VSCodium quitté puis relancé | **conforme** : interface en français, 18 commandes « Lepton : … » en français (compte de l'utilisateur) ; `~/.config/VSCodium/clp/…fr` créé ; caches `language fr`, 94 traductions ; « Lepton : état de la graine » → canal « Lepton », code 0. Le package.json déclare 19 commandes visibles : 18 opérations + « rafraîchir la vue Architecture », plus la commande de focus de la vue générée par VSCodium (20 au premier lancement) |
| F6 | 6.4 | vue Lepton › Architecture | conforme : greffons de la graine identiques à `lepton seed status` (5 entrées, graine 6d3d2a5) ; canal : « Observation de 5 greffon(s) et du trunk … » |
| F2 | 6.5 | `touch` / `rm` de `essai_s3.c` dans le clone BSP (shell de la VM et non terminal intégré, même événement inotify) | lien créé en 2 à 3 s, retiré en 2 à 3 s ; canal : `lepton graft --path …/essai_s3.c` → « regreffe de qemu-mps2-an386 faite », code 0 |
| F3 | 6.5 | explorateur, trunk, Nouveau fichier (nom saisi « ␠essai_s3_trunk.c », espace en tête) | conforme : `lepton file add … --adopt` → « déplacé dans qemu-mps2-an386 », puis graft code 0 ; fichier régulier dans le clone, lien relatif dans le trunk ; nom avec espace bien géré. Notification de CMake Tools (§5, O-b) |
| L3-4 | 6.5 | suppression du lien dans l'explorateur | notification « essai_s3_trunk.c n'a été supprimé que du trunk : le greffon qemu-mps2-an386 le contient toujours, et la prochaine regreffe le rétablit. » ; « Supprimer du greffon » → absent du clone et du trunk ; clone BSP propre |
| F5 | 6.6 | `lepton-greffon.json` du BSP, `"type": "xyz"` sans enregistrer | conforme : une erreur `lepton` en ligne 3 ; annulation → retirée. Premier essai (clé `"type"` renommée par erreur) : 20 erreurs distinctes (§5, D-b) |
| F5 | 6.6 | `mkconf_env11.xml`, `<inconnu/>` + Ctrl+S, puis retrait + Ctrl+S | conforme : erreur `lepton` (« lepton check ») et erreur `xml` (lemminx, cvc-complex-type.2.4.a, 9:5-12) ; après retrait : fichier réel enregistré, lien du trunk conservé, graine propre, `lepton check --json` sans anomalie. Erreur `lepton` placée en 1:1 avec le préfixe « 9: » (§5, D-a). Sans Ctrl+S, seule l'erreur `xml` paraît (conception : le XML reste à lemminx pendant la saisie) |
| F7, L6-5 | 6.7 | « ajouter une configuration à la graine » `essai-s3`, `MinSizeRel`, `qemu` | conforme : `lepton seed config add essai-s3 --build-type MinSizeRel --run qemu` → « preset env11-essai-s3 » ; présent dans « Sélectionner une présélection de configuration » sans recharger |
| F4 | 6.7 | présélection `env11-debug-qemu` → `env11-essai-s3` → `env11-debug-qemu` (essai-s3 faute de `release-qemu`, décision de l'utilisateur) | conforme : deux fois « …/build/.active/compile_commands.json a changé : clangd relancé » |
| F7, L6-5 | 6.7 | « retirer une configuration de la graine » `essai-s3` | conforme : « configuration essai-s3 retirée (preset env11-essai-s3) » ; absent de la liste sans recharger ; graine = HEAD 6d3d2a5 |
| — | 6.7 | `build/env11-essai-s3/` | configuré par CMake Tools pendant F4 (41 fichiers, 1,8 Mo, `CMakeCache.txt`, `build.ninja`, aucun binaire), donc plus que la requête `client-lepton` ; supprimé avec l'accord de l'utilisateur (§5, O-e) |
| F7 | 6.7 | clic droit sur `mkconf_tauon_basic_qemu_mps2.xml` → importer | refus : « lepton: erreur: XML de la graine déjà fourni par le greffon du projet (sys/user/env11/etc/mkconf_env11.xml) → le modifier en place » |
| L6-7 | 6.8 | construction lancée par le débogage, fenêtre neuve | aucune notification `$gcc` (utilisateur) ; aucune trace `problemMatcher`/`$gcc` dans les journaux |
| F8, L6-6 | 6.8 | point d'arrêt sur `if(qemu_mps2_uart_irq_users++ > 0)` (ligne 49, et non 48 : §5, O-f), « Déboguer env11-debug-qemu (QEMU mps2-an386) », première session de la fenêtre | conforme : arrêt sur `main` puis ligne 49 ; onglet sous `…/qemu/trunk/…`, cadres de la pile sous `trunk/` ; canal : « Session de débogage Déboguer env11-debug-qemu (QEMU mps2-an386) : sources affichées par le trunk (5 greffon(s)) » ; `gdbPath` de la session : `/usr/bin/gdb-multiarch` |
| F8 | 6.9 | témoin `lepton.debug.trunkPaths: false` | onglet de l'arrêt sous `depots/` (R3 reproduit), sans message « par le trunk » ; réglage retiré ensuite (défaut `true`) |
| — | 6.10 | `pytest -q -rs` (venv `~/lepton-tools-dev/venv-test`, `TMPDIR` sous ~) | **191 passed** en 98,9 s ; aucun test ignoré |
| — | 6.11 | `find trunk -type f`, `find -L trunk -type l`, `git status` des clones | trunk : vides ; graine, noyau, famille, BSP : propres. `depots/lepton-application/salut` : ` M salut.c`, `?? salut_message.c`, datés du 2026-10-15 (ENV-11), antérieurs, hors graine, non touchés (déjà dans `env-10-r5-debian.md` §2) |

## 3. Versions relevées

| Outil | Version |
| --- | --- |
| Pack de langue | `ms-ceintl.vscode-language-pack-fr@1.131.0` |
| Extension Lepton | `lepton-distribution.lepton@0.5.1` (`extension/dist/lepton-0.5.1.vsix` de 0b4e96e) |
| lepton | 0.1.0 (pipx, Python 3.13.5) |
| scion | 0.5.1.1 |
| gdb-multiarch | GNU gdb (Debian 16.3-1) 16.3 |
| clangd | Debian clangd version 19.1.7 (3+b1) |
| QEMU | 10.0.13 (Debian 1:10.0.13+ds-0+deb13u1) |
| xmllint | libxml 20914 |
| CMake Tools | 1.24.42 |

## 4. Corrections propres à Debian

Aucune.

## 5. Défauts et observations

Défauts communs (pour la session Mac, non corrigés) :

- **D-a** (lepton, `lepton/checks.py` l. 393) : au contrôle complet, `Anomaly(xml_label,
  a.location, a.message)` ne recopie pas `a.line` donnée par `validate_xml`. Dans *Problèmes*,
  l'erreur XML est placée en 1:1 (ligne 1 entière), et non en ligne 9, et garde son préfixe
  « 9: » (`diagnosticMessage` ne le retire que si `line` est renseignée). `check --stdin` donne
  bien `line: 9`. Correction suggérée : recopier `a.line` (ou `dataclasses.replace(a,
  file=xml_label)`), plus un test. Confirmé par la session Mac à la lecture.
- **D-b** (lepton check, schéma greffon) : si la clé discriminante `type` est absente (ici
  renommée en `xyz`), `check --stdin` rend 45 anomalies (20 distinctes) : « champ obligatoire
  absent : type », une série de « False schema does not allow '…' » non traduits et placés en
  1:1, puis les erreurs des branches `oneOf` des autres types (`/destination` motifs
  `^kernel/dev/arch/`, `^bin/`, `^lib/` ; `/bibliotheque` ≠ `kernel`/`bin` ; `/mcu` type attendu
  array). Suggestion : sans discriminant valide, ne rendre que l'erreur du discriminant, et
  traduire le message des schémas `false`.

Observations :

- **O-a** (VSCodium) : le premier lancement après l'installation du pack par la CLI se fait en
  anglais. Chronologie : codium démarré à 14:49:19, `argv.json` réécrit par VSCodium à 14:49:20
  (ajout de `crash-reporter-id`), `languagepacks.json` écrit à 14:49:24, donc après la
  résolution de la langue. Second lancement en français, avec création de `clp/`. Pas de
  correction : comportement de VSCodium. Piste possible pour `install-vscodium.sh` : annoncer
  dans le bilan qu'une relance est nécessaire.
- **O-b** (CMake Tools 1.24.42) : à la création d'un fichier source (F3), notification « Aucun
  appel de commande source n'a été trouvé. L'élément essai_s3_trunk.c n'a pas été ajouté au
  système de build. » (`cmake.modifyLists.addNewSourceFiles`). Le réglage n'apparaît ni dans
  l'espace ni dans les réglages utilisateur. Suggestion : `lepton generate` écrit
  `"cmake.modifyLists.addNewSourceFiles": "no"` (construction par manifestes). Pas de
  notification à la suppression.
- **O-c** (consigne) : VSCodium 1.135 écrit ses journaux sous
  `~/.local/state/VSCodium/<horodatage>/` (canal Lepton :
  `window1/exthost/output_logging_*/N-Lepton.log`), et non sous `~/.config/VSCodium/logs/`.
- **O-d** (consigne / `install-vscodium.sh` l. 355-361) : la ligne « id : ancienne → nouvelle »
  ne s'affiche que si une version est déjà installée. À l'état absent, le journal ne montre que
  la sortie de codium, et `run` n'écrit pas la commande `--install-extension` hors `--dry-run`.
  Écart de libellé, sans effet.
- **O-e** (F4 sur preset éphémère) : `lepton seed config remove` ne retire pas le dossier de
  construction que CMake Tools a configuré pour ce preset.
- **O-f** (consigne) : sur la VM (BSP 046779e), `if(qemu_mps2_uart_irq_users++ > 0)` est en
  ligne 49 de `qemu_mps2_board.c`, et non en 48.
- **O-g** (consigne, F1) : « 18 commandes » compte les opérations de lepton ; la palette en
  montre 19 de l'extension (plus « rafraîchir la vue Architecture »), plus la commande de focus de
  la vue.
- Lignes préexistantes et non bloquantes d'`install-vscodium.sh` : « AVERTISSEMENT: installation
  pip de Graphify non aboutie » ; « rehash: warning: skipping ca-certificates.crt » ;
  DeprecationWarning DEP0169 de codium.

Questions pour l'utilisateur : correction de D-a et D-b, et suite à donner à O-a et O-b, à
décider au bilan de la session Mac.

## 6. Messages

| Date | Sens | ID | Résumé |
| --- | --- | --- | --- |
| 2026-10-28 | Mac → VM | ORDRE R12-1 | validation Debian de l'extension 0.5.1 selon `consignes/env-12-debian.md` |
| 2026-10-28 | VM → Mac | ACCUSÉ R12-1 | ordre reformulé ; têtes 0b4e96e / 16a331b / f1d1f3c ; écart seed.scions détaché sur 0.5.1.0 |
| 2026-10-28 | Mac → VM | AVANCEMENT R12-1 | écart seed.scions sans effet (pip extrait le tag) |
| 2026-10-28 | VM → Mac | AVANCEMENT R12-1 | arrêts du §5 : `max_user_watches` 30075, graine non commitée |
| 2026-10-28 | Mac → VM | AVANCEMENT R12-1 | avis : commit séparé « presets générés (lepton generate) » ; inotify : 30075 suffit, relèvement acceptable |
| 2026-10-28 | VM → Mac | AVANCEMENT R12-1 | décisions de l'utilisateur : commit 8539dfa, relèvement à 524288 ; avant §6.1 |
| 2026-10-28 | VM → Mac | AVANCEMENT R12-1 | §6.1 conforme (changements 4) ; avant §6.2 ; O-d |
| 2026-10-28 | VM → Mac | AVANCEMENT R12-1 | §6.2 (changements 0) et §6.3 conformes ; seed tree en manifests |
| 2026-10-28 | Mac → VM | AVANCEMENT R12-1 | seed tree : comportement voulu ; F4 à soumettre à l'utilisateur au §6.7 |
| 2026-10-28 | VM → Mac | AVANCEMENT R12-1 | arrêt au §6.4 : F1 en anglais, 20 commandes ; F6 conforme |
| 2026-10-28 | Mac → VM | AVANCEMENT R12-1 | 20 = 18 opérations + rafraîchir + focus ; test de relance |
| 2026-10-28 | VM → Mac | AVANCEMENT R12-1 | F1 conforme au second lancement ; avant §6.5 |
| 2026-10-28 | VM → Mac | AVANCEMENT R12-1 | §6.5 conforme ; O-b |
| 2026-10-28 | VM → Mac | AVANCEMENT R12-1 | §6.6 conforme ; D-a, D-b ; ordre proposé pour le §6.7 |
| 2026-10-28 | Mac → VM | AVANCEMENT R12-1 | D-a confirmé, D-b noté ; ordre du §6.7 accepté |
| 2026-10-28 | VM → Mac | AVANCEMENT R12-1 | §6.7 conforme ; O-e |
| 2026-10-28 | VM → Mac | AVANCEMENT R12-1 | §6.8, §6.9 conformes ; O-f |
| 2026-10-28 | VM → Mac | FIN-SUCCÈS R12-1 | voir le Bilan en tête de ce rapport |
