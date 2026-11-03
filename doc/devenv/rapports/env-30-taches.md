# ENV-30 — Tâche de l'éditeur « tests des greffons »

Rapport de l'étape. Session du 2026-11-03, branche lepton-tools `devenv/env-30` (depuis `main`
deaa5ff). lepton 0.1.0 installé depuis a1716f9, scion 0.5.4.0, ctest 3.31.12.

## 1. Tâches de test écrites aujourd'hui (`lepton/generate.py`, `tasks`, l. 467-507)

Toutes les tâches passent par `_task(label, command, args, cwd, **extra)` : `type` `process`,
`options.cwd`, `problemMatcher` vide sauf mention.

| `execution` | Libellé | `command` | `args` | `group` | `options` | `dependsOn` |
| --- | --- | --- | --- | --- | --- | --- |
| toutes | `lepton : configurer <P>` | cmake | `--preset <P>` | — | `cwd` trunk | mklepton (host) |
| toutes | `lepton : construire <P>` | cmake | `--build --preset <P>` | `build` | `cwd` trunk ; matcher gcc | configurer |
| `qemu` | `lepton : QEMU <P> (console série)` | qemu | `-M <machine> -kernel <elf> -nographic -monitor none -serial stdio` | — | `cwd` trunk ; panneau dédié | construire |
| `qemu` | `lepton : test de fumée <P>` | ctest | `--preset <P> -L smoke --output-on-failure` | `test` | `cwd` trunk, `env` `PYTHONDONTWRITEBYTECODE=1` | construire |
| `qemu` | `lepton : banc KAL <P>` | ctest | `--preset <P> -L kal --output-on-failure` | `test` | idem | construire |
| `carte` | `lepton : flasher <P>` | openocd | `-f <cfg>… [-c "adapter serial <S>"] -c "program <elf> verify reset exit"` | — | `cwd` trunk | construire |
| `None` | (configurer et construire seulement) | | | | | |

Constat K1 : aucune tâche `ctest` pour une configuration de carte, ni fumée, ni KAL. Une tâche
« tests des greffons » de carte serait la première tâche de test sur carte.

## 2. Savoir, au moment de `generate`, si un preset a des tests de greffon

| Source | Disponible à `generate` | Exactitude |
| --- | --- | --- |
| Manifestes des greffons greffés (`Rootstock.manifests()`, déjà lus par `Context`) : champ `tests` | toujours | même règle que le lecteur CMake si l'on reprend `_lepton_greffon_actif` |
| `ctest -N` de `build/<P>` | seulement après une configuration ; absent d'un rootstock neuf | exact, mais dépend de l'état de construction |

Règle « actif » du lecteur (`cmake/lepton_greffons.cmake`, `_lepton_greffon_actif`) : noyau
exclu ; famille active si c'est celle du BSP (`LEPTON_BOARD_FAMILLE`) ; BSP actif s'il est
`LEPTON_BOARD` ; application et bibliothèque toujours actives. `Context` connaît déjà le BSP de
chaque configuration (`Configuration.bsp`, `.board`) et les manifestes par nom : la règle se
transpose sans nouvelle lecture (K2). `ctest -N` est écarté : `generate` n'exécute ni CMake ni
CTest aujourd'hui, et l'espace d'un rootstock neuf serait faux.

Corollaire K3 (option 1) : un greffon qui gagne des tests après le dernier `generate` n'a pas de
tâche tant que `generate` n'est pas relancé (comme les lancements DBG-5 et le SVD).

Rootstocks du Mac où un greffon actif déclare des tests (BSP `qemu-mps2-an386`, `"tests": "tests"`) :
`<ROOTSTOCK>`, `essais/env-13-vierge`, `essais/env-9`, `essais/env-11/qemu`. Aucun :
`essais/env-11/{f429zi,wl55jc1,qemu-gra2}`, `essais/env-26-copie` (BSP an386 d'avant ENV-27),
`essais/env-27-copie` (BSP an386 retiré, aucun espace).

Mesures sur `<ROOTSTOCK>` (répertoires de construction existants) :

| Preset | `ctest -N -L greffon:` | Exécution `ctest -L greffon: --output-on-failure` |
| --- | --- | --- |
| `qemu-mps2-an386-embos` | 2 : `smoke.lsh` (fixture `kal_t0`), `qemu-mps2-an386.peripheriques` | (contrôle de la tâche 3) |
| `qemu-mps2-an500-embos` | 0 | « No tests were found!!! », code 0 |
| `nucleo-f429zi-embos` | 0 | — |

K4 : une tâche présente sans test (option 2) réussit en silence (code 0 et une ligne), sans
signaler l'absence comme une erreur ; `--no-tests=error` la ferait échouer (code 8).

## 3. Configurations de carte : `LEPTON_BOARD_SERIAL_PORT`

- `LEPTON_BOARD_SERIAL_PORT` est une variable du cache CMake lue à la configuration
  (`cmake/components/firmware.cmake` : `board.smoke_lsh`, fixture `board_t0`, n'existe que si le
  port et OpenOCD sont connus) ; aucun preset du noyau ni `CMakeUserPresets.json` généré ne la pose.
- La tâche `lepton : configurer <P>` de l'éditeur (et CMake Tools) configure sans elle : dans un
  `build/<P>` configuré par l'éditeur, aucun test de carte n'est déclaré, de greffon ou du noyau.
- Pour la fournir, il faudrait une donnée nouvelle par configuration (option `--serial-port` de
  `generate`, à l'image de `--probe-serial`, ou réglage de l'espace) écrite dans
  `CMakeUserPresets.json` (graine de projet seulement ; la graine de référence n'en a pas, PA-23)
  ou dans `cmake.configureSettings` de CMake Tools (sans effet sur la tâche `configurer`, qui
  appelle `cmake --preset`).
- Les tests de carte flashent la carte (`--reset-command … program … verify reset exit`) : PA-11.
- Aucun greffon ne déclare aujourd'hui de test de carte. ENV-32 en ajoutera un (`board.radio`
  du BSP WL55, qui exige en plus `LEPTON_RADIO_PEER_STLINK_SERIAL` et `LEPTON_RADIO_PEER_SERIAL_PORT`).

K5 : une tâche de carte écrite comme celle de QEMU ne trouverait aucun test, sauf configuration à
la main avec `-DLEPTON_BOARD_SERIAL_PORT=…` dans le même `build/<P>`. Couvrir la carte demande de
fournir le port à la configuration : c'est une extension de l'interface de `generate`, hors de
l'archétype « création bornée » prévu.

## 4. Extension Lepton (`extension/`)

`extension/src` et `extension/package.json` ne lisent ni la liste des tâches ni leurs libellés
(aucun `vscode.tasks`, `fetchTasks`, `executeTask`, `taskDefinitions`). K6 : la nouvelle tâche
n'a aucun effet sur l'extension ; pas de nouvelle version du `.vsix`.

## 5. Questions du PA-47 et propositions

| # | Question | Proposition de la session |
| --- | --- | --- |
| Q1 | Configurations visées | QEMU seules (K1, K5) ; la carte est reprise en ENV-32 si le test radio doit être lancé de l'éditeur, avec la question du port |
| Q2 | Présence de la tâche | Option 1 : seulement si un greffon actif de la configuration déclare `tests` (K2, K3) ; évite une tâche qui « réussit » sans rien exécuter (K4) |
| Q3 | Libellé | `lepton : tests des greffons <P>`, à côté de « test de fumée » et « banc KAL » |
| Q4 | Arguments | `--preset <P> -L greffon: --output-on-failure` (sélectionne aussi la fixture `smoke.lsh`, attendu) |
| Q5 | `group`, `cwd`, `env`, `dependsOn` | `test`, trunk, `PYTHONDONTWRITEBYTECODE=1`, `construire <P>` : identiques aux tâches voisines |

Décision de l'utilisateur : § 6.

## 6. Décision PA-47 (utilisateur, 2026-11-03)

- Q1 : configurations QEMU seules. La carte est reprise en ENV-32 si le test radio doit se lancer
  de l'éditeur, avec la question du port.
- Q2 : option 1. La tâche n'est présente que si un greffon actif de la configuration déclare
  `tests` (BSP de la configuration, sa famille, applications, bibliothèques ; noyau exclu).
- Q3-Q5 : propositions retenues telles quelles. Une seule tâche par configuration.

## 7. Implémentation (lepton-tools `devenv/env-30`)

| Commit | Contenu |
| --- | --- |
| 63d3642 | Audit (§1-§5), décision PA-47 (§6) |
| c3811b3 | `generate.py` : `Context.greffons`, `Context.greffon_tests(c)` (règle `_lepton_greffon_actif`), tâche ajoutée aux suites QEMU après « banc KAL » ; `tests/test_tasks_greffons.py` (6 tests, écrits d'abord : 4 rouges constatés, les 2 cas sans tâche verts) ; `rapports/env-8-interface.md` §20 |

`pytest` : 235 verts (229 + 6). lepton réinstallé par `pipx install --force` depuis c3811b3.

## 8. Contrôles (PA-48)

### 8.1 Fichiers générés
Relevés `~/lepton-tools-dev/essais/env-30-releve/{avant,apres}/<rootstock>/`, régénérés par
`lepton generate` juste avant chaque relevé (avant : lepton installé de a1716f9, code de `lepton/`
identique à `main` deaa5ff) ; diff : `diff-avant-apres.txt` (276 lignes ajoutées, 0 retirée).

| Rootstock | `generate` avant / après | Tâches ajoutées |
| --- | --- | --- |
| `<ROOTSTOCK>` (`original-tree`) | 0 / 0 | 4 : `qemu-mps2-an386-{embos,embos-soft,freertos,freertos-soft}` ; aucune pour an500 ni les 10 presets de carte |
| `essais/env-13-vierge` | 0 / 0 | 4 (mêmes presets) |
| `essais/env-9` | 0 / 0 | 2 : `env9-debug-qemu`, `env9-release-qemu` |
| `essais/env-11/qemu` | 0 / 0 | 2 : `env11-debug-qemu`, `env11-release-qemu` |
| `essais/env-11/f429zi` | 0 / 0 | 0 (carte), espace identique |
| `essais/env-11/wl55jc1` | 0 / 0 | 0 (carte), espace identique |
| `essais/env-11/qemu-gra2` | 1 / 1 (attendu : BSP retiré, essai GRA-2) | — |

`CMakeUserPresets.json` identiques partout. Forme de la tâche conforme au PA-47 (`command`
`/opt/local/bin/ctest`, `args`, `cwd` trunk, `env`, `dependsOn`, `group`).

### 8.2 Exécution en ligne de commande
- `qemu-mps2-an386-embos` (`<ROOTSTOCK>`), même `command`, `args`, `cwd`, `env` que la tâche :
  `smoke.lsh` (fixture) et `qemu-mps2-an386.peripheriques` réussis, 2/2, code 0.
- Preset sans test de greffon (`qemu-mps2-an500-embos`) : tâche absente (option 1) ; pour mémoire,
  `ctest -L greffon:` y affiche « No tests were found!!! », code 0 (§2).
- `lepton check` code 0 ; trunk : seul fichier régulier `.scion.grafted.list`, 0 lien cassé,
  aucun `__pycache__`. Aucune reconstruction ni oracle (binaires non touchés).

### 8.3 Essai VSCodium (Mac, fait par l'utilisateur, 2026-11-03)
Espace `<ROOTSTOCK>/original-tree.code-workspace`, tâche `lepton : tests des greffons
qemu-mps2-an386-embos` : visible dans « Exécuter la tâche », exécutée après la construction,
`smoke.lsh` et `qemu-mps2-an386.peripheriques` réussis, résultat lisible.
Essai refait par l'utilisateur après la fusion (même espace, même tâche) : visible et verte.

## 9. Bilan (PA-48)
- Critères de l'étape : PA-47 tranché ; `pytest` 235 verts dont 6 nouveaux ; diff des relevés
  limité à la nouvelle tâche, dans les configurations QEMU dont un greffon actif déclare des tests ;
  test du greffon d'essai réussi par la tâche (ligne de commande et VSCodium).
- Extension Lepton non touchée (K6). Validation Debian : ENV-33 (C5).
- Propositions non validées : aucune.
