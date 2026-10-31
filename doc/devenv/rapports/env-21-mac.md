# ENV-21 — Session Mac : ordre R21-1 et rootstocks d'essai — 2026-10-31

Session Mac `validation-debian-groupee-env21`. Rapport VM : `rapports/env-21-debian.md`
(branche `devenv/env-21-debian`).

## 1. Préparation (tâche 1)

- Contrôle préalable : 0 `.DS_Store` dans `~/lepton/trunk` et `depots/generation/building`.
- Têtes publiées relevées par `git ls-remote` (14 dépôts, tag scion) : toutes égales aux clones de
  `~/lepton/depots` (propres). Tableau : `consignes/env-21-debian.md` §1.
- Écarts Mac de référence `env-14-apres` → `env-20-apres` (`comparer-oracle.py`) : 1 sur
  `nucleo-f429zi-*`, `stm32f746g-disco-*`, `samd21-xplained-pro-freertos` ; 0 sur les 9 autres ;
  `nucleo-f439zi-*` = `nucleo-f429zi-*` (code 0) ; empreintes mklepton 50 lignes (44 en ENV-14).
  Ces valeurs fixent l'attendu `comparer_R14-1` de la consigne (§8).
- Consigne `consignes/env-21-debian.md` (bb0702f) ; PA-29 (65b19f7) ; push de `devenv/env-21`.

## 2. Messages §2bis (R21-1)

| Date | Type | Résumé |
| --- | --- | --- |
| 2026-10-31 | ORDRE | Mac → `lepton-vm-debian` : consigne intégrale, `devenv/env-21` 65b19f7, C7 accordé |
| 2026-10-31 | ACCUSÉ | §5 conforme : 15 têtes égales au §1, `devenv/env-21` 65b19f7, embOS présent, aucun écart |
| 2026-10-31 | AVANCEMENT | §6.1 (graine `env11` relevée), lepton réinstallé, noyau 16a331b → 40d7197 ; attente des scripts (sudo) |
| 2026-10-31 | AVANCEMENT | §6 : C1, C2 conformes ; `install-debian.sh` code 0 (scion 0.5.2.0 déjà installé) ; `install-vscodium.sh` 0 changement ×2 |
| 2026-10-31 | AVANCEMENT | §7 : C3 conforme ; 14 entrées, 3941 liens, 0 cassé, 0 régulier |

## 3. Rootstocks d'essai (tâche 3, PA-P)

Décisions de l'utilisateur : les 6 rootstocks d'ENV-14 (`env-11/bout-en-bout` exclu) ; parade E2
pour les `.DS_Store` réguliers des trunks ; mise à jour de la graine d'`env-13-vierge`.

Constat préalable : 10 `.DS_Store` réguliers dans les trunks (5 dans `env-13-vierge`, 1 dans chacun
des autres), recréés par le Finder depuis ENV-14 ; aucun `.scion.trunk.tolerated` (rootstocks
antérieurs à 0.5.2.0). Les `.DS_Store` des clones sont ignorés par `~/.gitignore_global` (E1).

Séquence :
1. `<rootstock>/.scion.trunk.tolerated` écrit dans chacun (en-tête de scion 0.5.2.0, motifs
   `.DS_Store`, `._*`) ; hors trunk.
2. `scion graft-update -v` : code 0 partout ; chaque `.DS_Store` du trunk « supprimé (toléré) » ;
   les `.DS_Store` des clones « exclu (ignoré par git) ».
3. `qemu-gra2` : le BSP an386 réinscrit par `sync` (comme en ENV-14) → `scion graft-remove
   lepton@bsp-qemu-mps2-an386` sans `--purge` (6 feuilles).
4. `env-13-vierge` : `graft-update` n'avance pas le dépôt de la graine (`sync` lit la graine
   locale) ; `git pull --ff-only` de `depots/lepton-seed.scions/original-tree` (0f1275a → 15740f9),
   puis `scion graft-update` : 5 greffons clonés (`bsp-nucleo-f439zi`, `family-stm32f7xx`,
   `bsp-stm32f746g-disco`, `family-samd21`, `bsp-samd21-xplained-pro`).

| Rootstock | Liens avant → après | Entrées | Cassés / réguliers | `check` | `generate` | Lancements |
| --- | --- | --- | --- | --- | --- | --- |
| `env-9` | 3347 → 3055 | 5 | 0 / 0 | 0 | 0 | 2 |
| `env-11/f429zi` | 3658 → 3366 | 5 | 0 / 0 | 0 | 0 | 1 |
| `env-11/qemu` | 3347 → 3055 | 5 | 0 / 0 | 0 | 0 | 2 |
| `env-11/qemu-gra2` | 3341 → 3049 | 4 | 0 / 0 | 1 (attendu) | 1 (attendu) | 1 (inchangé) |
| `env-11/wl55jc1` | 3594 → 3302 | 5 | 0 / 0 | 0 | 0 | 1 |
| `env-13-vierge` | 3929 → 3941 | 9 → 14 | 0 / 0 | 0 | 0 | 16 |

- Clones : noyau 40d7197, `family-stm32f4xx` 2b21340, autres greffons aux têtes du §1 de la
  consigne ; tous propres ; graines de projet propres.
- −292 liens dans les rootstocks de projet : tous retirés, aucun ajouté (détail `env-9`) ; ce sont
  les fichiers F746/SAMD21 sortis du noyau en ENV-19 (`kernel/dev/arch` 204, `kernel/core/ucore`
  73, `kernel/dev/bsp` 5, `ld`, `debug`, `cmake/boards`, `tauon-basic/src/arch`), absents de ces
  graines.
- `env-13-vierge` : trunk identique à celui de `~/lepton` (chemins et cibles, `cmp`).
- `qemu-gra2` : `check` et `generate` à 1, comme aux relevés d'ENV-18 avant et après (essai GRA-2,
  BSP non greffé : « BSP « qemu-mps2-an386 » de la graine non greffé », pilotes CFG-5).
- Journaux : scratchpad de la session (non versionnés).
