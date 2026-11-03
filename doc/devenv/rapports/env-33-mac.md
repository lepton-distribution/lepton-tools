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
