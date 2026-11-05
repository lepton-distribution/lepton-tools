# ENV-36 — Validation Debian groupée (ENV-34 et ENV-35) — rapport de la session Mac

Session Mac `validate-env-34-35-debian`, 2026-11-05. Branche lepton-tools `devenv/env-36` (depuis
`main` 06cb55d). Consigne VM : `consignes/env-36-debian.md`.

## 1. Préparation (tâche 1)

### 1.1 Écarts Mac `env-32-apres` → `env-35-apres`

`comparer-oracle.py` par preset (`env-32-apres` = binaires de référence de R33-1 au Mac ;
`env-35-apres` = nouvelle référence d'ENV-35) :

| Preset | Code | Écarts (hors empreintes) |
| --- | --- | --- |
| host | — | `mklepton-empreintes.sha256` identique (pas d'`empreintes.txt` pour host : code 2 du comparateur, attendu) |
| 12 presets hors F4 (an386 ×4, an500 ×2, WL55 ×2, SAMD21 ×2, F746 ×2) | 0 | aucun |
| `nucleo-f429zi-embos`, `nucleo-f439zi-embos` | 1 | 89 symboles retirés, 64 ajoutés, 16 modifiés ; `.text` 159864 → 161204 (+1340), `.data` 1056 → 1116 (+60), `.bss` 98568 → 97304 (−1264), DWARF |
| `nucleo-f429zi-freertos`, `nucleo-f439zi-freertos` | 1 | 89 retirés, 60 ajoutés, 16 modifiés ; `.text` 166580 → 167088 (+508), `.data` +60, `.bss` −1264, `.noinit` 4 → 0, DWARF |

Nature des écarts F4 : E-1 à E-5 de `rapports/env-35-hal-f4.md` §5.1. Les listes de symboles
F429 et F439 sont identiques entre elles. `F429 → F439` dans `env-35-apres` : code 1, sections
`.debug_*` seules (3 en embOS, 2 en FreeRTOS : `STM32F439xx` depuis ENV-35) ; 0 dans
`env-33-debian` (avant ENV-35).

Attendus dérivés, versionnés dans `env-36-mac/attendu/` :
- `comparaisons-mac/<preset>.txt` : sorties brutes du comparateur pour les 4 presets F4 ;
- `<preset>.noms.txt` : mêmes écarts normalisés (noms seuls, `.debug_*` exclues ; 172 lignes en
  embOS, 169 en FreeRTOS), comparés par la VM à `env-33-debian` → `env-36-debian` (les tailles
  diffèrent entre la chaîne du Mac et la chaîne APT).

Listes `ctest -N` : `env-32-apres/ctest-N/` ne contient que les variantes WL55 d'ENV-32 ;
`env-35-apres/ctest-N/` a host et les 16 presets. Pas de comparaison `ctest -N` dans la consigne
(chemins propres à l'hôte, `net.ping_ftpd` sous Linux seul) : le banc KAL QEMU est comparé à R33-1.

### 1.2 Têtes publiées (`git ls-remote`, 2026-11-05)

| Dépôt | Référence | Commit | En R33-1 |
| --- | --- | --- | --- |
| `lepton-tools` | `main` | 06cb55d | e47bc11 (`devenv/env-33`) |
| `seed.scions` | tag `0.5.4.0` | 99aa973 | = |
| `lepton-seed.scions` | `original-tree` | 15740f9 | = |
| `lepton-original-tree.scions` | `master` | 2893297 | b3a5415 |
| `lepton-famille-stm32f4xx` | `master` | 0fd8b2a | 8364493 |
| `lepton-bsp-nucleo-f429zi` | `master` | b9fe2bf | 2b2dfdd |
| `lepton-bsp-nucleo-f439zi` | `master` | 314f91b | bdbfa06 |
| 9 autres greffons famille/BSP | `master` | inchangés | = |

Clones de `<ROOTSTOCK>` aux mêmes commits, propres, alignés sur `origin`.

Paquet lepton : `git diff e47bc11 main` hors `doc/` = `scripts/tiers/` seul (3 fichiers, hors
paquet) ; pas de réinstallation sur la VM.

### 1.3 Liens du trunk

`git diff --no-renames --name-status` des 4 clones changés (commit de R33-1 → tête publiée),
limité à `scion/` : 215 ajouts, 194 retraits, 3957 + 21 = **3978** liens, égal au trunk du Mac.
Listes `env-36-mac/attendu/liens-ajoutes.txt` et `liens-retires.txt` (chemins `trunk/…`),
contrôlées sur `<ROOTSTOCK>` : chaque ajout est un lien présent, chaque retrait est absent.

| Clone | Ajouts | Retraits |
| --- | --- | --- |
| noyau | 2 (`core_cm4.h` 5.9.0, `CMSIS/Core/LEPTON-PROVENANCE.md`) | 0 |
| `family-stm32f4xx` | 211 (201 `hal_driver/`, 7 `cmsis-5/Device/ST/STM32F4xx/`, 3 `dev_stm32f4xx/` : `eth_x.{c,h}`, `hal_tick.c`) | 194 (190 `cubemx_hal_driver/`, 4 en-têtes HAL V1.3.0 de `driverlib/`) |
| `bsp-nucleo-f429zi`, `bsp-nucleo-f439zi` | 1 chacun (`stm32f4xx_hal_conf.h`) | 0 |

### 1.4 Consigne

`consignes/env-36-debian.md` : C1 versions ; C2 `graft-update` de `essais/env-28-debian` par
l'utilisateur, puis rootstock neuf `essais/env-36-debian` ; C3 host + 16 presets, comparaison à
`env-33-debian` ; C4 compilation à blanc (`compiler-hal-f4-a-blanc.sh`) ; C5 fichiers générés
(`$R` contre l'espace de `essais/env-33-debian`, `$P` stabilité) ; C6 nettoyage. Points laissés au
PA-59 : cartes, nettoyage, choix de C4 et C5.
