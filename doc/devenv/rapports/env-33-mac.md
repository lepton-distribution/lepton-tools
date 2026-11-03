# ENV-33 — Validation Debian groupée (ENV-29 à ENV-32) — partie Mac — 2026-11-03

Session Mac `validation-debian-env-33`. Branche lepton-tools `devenv/env-33` (depuis `main` 60dd6e5).
Consigne VM : `consignes/env-33-debian.md` (ordre `R33-1`).

## 1. Écarts Mac `env-27-apres` → `env-32-apres` (attendu de la comparaison Debian)

`python3 scripts/oracle/comparer-oracle.py oracles/env-27-apres/<P> oracles/env-32-apres/<P>`, les
16 presets ; `host` comparé par ses fichiers (pas d'ELF).

| Presets | Code | Écarts |
| --- | --- | --- |
| `host` | — | `mklepton-empreintes.sha256` identique (50 fichiers) ; ctest 7/7 des deux côtés |
| 8 embOS (`qemu-mps2-an386-embos`, `-embos-soft`, `qemu-mps2-an500-embos`, `nucleo-f429zi-embos`, `nucleo-f439zi-embos`, `nucleo-wl55jc1-embos`, `samd21-xplained-pro-embos`, `stm32f746g-disco-embos`) | 0 | empreintes seules |
| 8 FreeRTOS | 1 | `xTaskCreateStatic` +4 (0x1f8 → 0x1fc ; samd21 0x1f0 → 0x1f4) ; `xIdleTaskTCB.3` et `xTimerTaskTCB.1` 0x54 → 0x58 ; `.ccm_bss` +8 ; `.debug_*` ; empreintes |
| `qemu-mps2-an386-freertos` (en plus) | 1 | `.text` 159400 → 159416 (+16 : +4 de code et bourrage d'alignement, E-2 d'ENV-31, critère amendé PA-49 (2)) |

Aucun autre écart. Ce sont exactement les écarts d'ENV-31 (`rapports/env-31-freertos.md` §7) ;
ENV-32 n'a changé aucun binaire (`env-32-apres` = `env-31-apres`, code 0 ×16). Attendu de R33-1
contre `env-28-debian` : embOS 0, FreeRTOS dans le critère du PA-49 (consigne §8.1).

## 2. Têtes publiées (`git ls-remote`, 2026-11-03)

Têtes distantes = têtes locales, clones sur `master`, sans modification suivie.

| Dépôt | Publié | En R28-1 |
| --- | --- | --- |
| `seed.scions` | tag `0.5.4.0` 99aa973, `master` 1173d6d | tag `0.5.3.0` ad292ee |
| `lepton-tools` | `main` 60dd6e5 | `devenv/env-28` b8ff911 |
| `lepton-seed.scions` `original-tree` | 15740f9 | 15740f9 |
| `lepton-original-tree.scions` (noyau) | b3a5415 | 0c0cc4f |
| `lepton-bsp-nucleo-wl55jc1` | ef51ec1 | c9183de |
| 11 autres greffons famille/BSP | inchangés (3954357, 09f4943, e98a482, 8364493, 2b2dfdd, bdbfa06, dbc58d7, d2d9aa9, 6266908, a262e81, f3cffa2) | = |
| `devenv/env-14` (noyau ; `lepton-famille-stm32f4xx`) | e5a5689 ; af964c6 (cas E-1) | = |

Changements de fichiers greffés entre R28-1 et R33-1 : noyau `scion/tests/board_radio.py` retiré ;
BSP WL55 `tests/CMakeLists.txt` et `tests/radio.py` ajoutés. Trunk attendu : 3956 → 3957 liens
(`<ROOTSTOCK>` du Mac : 3957). Défaut `SCION_REF` d'`install-debian.sh` (b3a5415) : 0.5.4.0.
Code de lepton (`lepton/`, `pyproject.toml`, `scripts/`) inchangé depuis c3811b3 (installé au Mac).

## 3. Décisions du PA-53 (utilisateur, 2026-11-03)

- C7 : découverte seule (pas de carte sur la VM) ; script `relever-ctest-N.sh` d'ENV-32.
- C3 : cas E-1 rejoué sur une copie de `essais/env-28-debian` ; `graft-update` lancé par
  l'utilisateur ; copie supprimée ensuite.
- C8 : `essais/env-14-debian` et `~/env-28-journaux` supprimés par l'utilisateur ;
  `essais/env-28-debian` conservé (cas nominal de C3).
- PA-53 : consigne validée telle quelle ; push de `devenv/env-33` (e47bc11) ; ordre `R33-1`.

## 4. Journal des messages (§2bis)

| ID | Date | Sens | Résumé |
| --- | --- | --- | --- |
| ORDRE R33-1 | 2026-11-03 | Mac (`validation-debian-env-33`) → VM (`debian-linux-vm`) | consigne `env-33-debian.md` @ e47bc11 ; accords du PA-53 ; texte des §1-§3 recopié, §4-§12 renvoyés au fichier poussé (variables recopiées) |
| ACCUSÉ R33-1 | 2026-11-03 | VM → Mac | non remis (ECONNRESET), journalisé sur la VM `~/env-33-journaux/0-messages-R33-1.md` ; résumé reçu avec l'AVANCEMENT suivant : §5 conforme au §1, `devenv/env-33` e47bc11, `$U` conforme (13 clones sur `master`, 3956 liens), BSP an386 de `$P` à 046779e sans `tests` (espace attendu identique au §9.2), scion 0.5.3.0 ; l'utilisateur a décidé de poursuivre |
| AVANCEMENT R33-1 | 2026-11-03 | VM → Mac | §6.1 fait (`generate`/`check` code 0, presets d5ee81e4…, espace b2c7b8a4…) ; clone noyau b3a5415, `SCION_REF` 0.5.4.0 ; commandes du §6.2 à l'utilisateur |

## 5. Rootstocks d'essai du Mac (tâche 3)

Accord de l'utilisateur (PA-P) : les 7, 2026-11-03. Journaux : `~/lepton-tools-dev/essais/env-33-mac/`
(`inventaire-{avant,apres}.txt`, `<rootstock>-{liens-avant,liens-apres}.txt`, `-graft-update.log`,
`-check.log`, `-generate.log`, `-espace.diff`). scion 0.5.4.0.

### 5.1 Inventaire avant (P-1)
Les 13 + 9 × 3 clones : sur `master`, amont `origin/master`, propres, aux têtes de R28-1 (noyau
0c0cc4f, `bsp-nucleo-wl55jc1` c9183de). 0 lien cassé. Fichiers réguliers : 5 `.DS_Store` du Finder
par trunk (3 nov. 08:45, tolérés par `.scion.trunk.tolerated` sauf dans `bout-en-bout`).

### 5.2 Regreffe et contrôles

| Rootstock | `graft-update` | Liens avant → après | Liens retirés / ajoutés | Entrées | Cassés | `check` | `generate` | Espace | `request` / `lldb` / `svdFile` / tâches « tests des greffons » |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `env-9` | 0 | 3057 → 3056 | `tests/board_radio.py` / — | 5 | 0 | 0 | 0 | identique | 3 / 1 / 0 / 2 |
| `env-11/f429zi` | 0 | 3370 → 3369 | idem / — | 5 | 0 | 0 | 0 | identique | 2 / 1 / 1 / 0 |
| `env-11/qemu` | 0 | 3057 → 3056 | idem / — | 5 | 0 | 0 | 0 | identique | 3 / 1 / 0 / 2 |
| `env-11/qemu-gra2` | 0, puis `graft-remove lepton@bsp-qemu-mps2-an386` sans `--purge` (8 feuilles), code 0 | 3049 → 3048 | idem / — | 4 | 0 | 1 (attendu, CFG-5) | 1 (attendu) | identique | 1 / 0 / 0 / 0 |
| `env-11/wl55jc1` | 0 | 3305 → 3306 | idem / BSP `tests/CMakeLists.txt`, `tests/radio.py` | 5 | 0 | 0 | 0 | identique | 2 / 1 / 1 / 0 |
| `env-11/bout-en-bout/rootstock` | **1** (E-1, §5.3), puis `scion graft` code 0 | 3057 → 3056 | idem / — | 5 | 0 | 0 | 0 | +23 lignes : tâche `lepton : tests des greffons bout-en-bout-debug-qemu` (ENV-30 ; ce rootstock n'était pas dans le relevé d'ENV-30) | 2 / 1 / 0 / 1 |
| `env-13-vierge` | 0 | 3956 → 3957 | idem / BSP `tests/CMakeLists.txt`, `tests/radio.py` | 14 | 0 | 0 | 0 | identique | 23 / 7 / 10 / 4 (= `<ROOTSTOCK>`) |

Clones après : tous sur `master`, propres, aux têtes publiées (noyau b3a5415, `bsp-nucleo-wl55jc1`
ef51ec1). Graines locales « sans amont, laissée telle quelle » ; `env-13-vierge` : graine déjà à
15740f9. Les espaces identiques le sont parce qu'ils avaient été régénérés en ENV-30 avec le même lepton
(c3811b3) ; le champ `tests` du BSP WL55 ne crée pas de tâche (configurations de carte, PA-47).

### 5.3 Écarts et constats
- **E-1 (`bout-en-bout/rootstock`)** : `graft-update` code 1, « le trunk … contient des fichiers
  qui ne sont pas des greffes » (5 `.DS_Store`) ; son `.scion.trunk.tolerated` n'avait que des
  commentaires (rootstock recréé en ENV-22 par le script). scion 0.5.4.0 a avancé le clone noyau
  (0c0cc4f → b3a5415), refusé le dégreffage et rétabli le trunk (3057 liens, 1 lien cassé
  `tests/board_radio.py`) : comportement d'ENV-29. Décision de l'utilisateur : motifs `.DS_Store`
  et `._*` ajoutés à ce fichier (comme les 6 autres, décision d'ENV-21), puis `scion graft` :
  code 0, 3056 liens, 0 cassé.
- **O-1 (`.DS_Store`)** : après regreffe, le Finder a recréé 6 à 7 `.DS_Store` par trunk
  (17:50-17:52). Tolérés, ils ne bloquent pas scion et disparaissent au dégreffage ; aucun autre
  fichier régulier, aucun `__pycache__`. Le critère « 0 fichier régulier » se lit ici « aucun fichier
  régulier hors fichiers tolérés ».

