# ENV-28 — Validation Debian groupée : session Mac

Session principale `validate-env-22-27-debian`, 2026-11-02. Branche lepton-tools `devenv/env-28`
(depuis `main` d4351bc). Consigne VM : `consignes/env-28-debian.md` (ordre `R28-1`).

## 1. Préparation (tâche 1)

### 1.1 Oracle Mac de référence

`oracles/env-27-apres/` : host + 16 presets croisés (dernier oracle « après » complet d'ENV-24 à
ENV-27 ; ENV-25 et ENV-26 n'ont pas modifié les binaires, ENV-27 a ajouté un test sans modifier
les binaires : `rapports/env-27-tst2.md` §8).

### 1.2 Écarts Mac `env-20-apres` → `env-27-apres`

`comparer-oracle.py` sur les 16 presets : **code 1 partout**, écarts limités au cpufs automatique
d'ENV-24 (`rapports/env-24-cpufs.md`) :

| Presets | `.text` | `filecpu_memory` (T, taille) | DWARF |
| --- | --- | --- | --- |
| `qemu-mps2-an386-*` (4), `qemu-mps2-an500-*` (2), `nucleo-f429zi-*` (2), `nucleo-f439zi-*` (2), `stm32f746g-disco-*` (2) | −122064 | `0001f401` → `00001734` | `.debug_abbrev` −17, `.debug_info` −7 |
| `nucleo-wl55jc1-*` (2) | −6248 | `00001f41` → `000006dc` | `.debug_abbrev` −17, `.debug_info` −5 |
| `samd21-xplained-pro-*` (2) | −1368 | `00000c01` → `000006ab` | aucun |

Aucune autre section, aucun autre symbole. `f429→f439` (`env-27-apres`) : 0 en embOS et FreeRTOS.

Host :
- `mklepton-empreintes.sha256` : 50 lignes ; 14 différentes (`.fsflash.o` et `dev_dskimg.c` des 7
  combinaisons BSP × XML : image du cpufs) ; `env-21-debian` = `env-20-apres` (R21-1), donc attendu
  Debian : `env-28-debian` = `env-27-apres`.
- ctest 7/7 dans les deux oracles ; `construction.log` : ordre de compilation seul.

Banc QEMU (`banc-kal.log`) :

| Preset | Mac `env-20-apres` | Mac `env-27-apres` | Debian `env-21-debian` | Attendu R28-1 |
| --- | --- | --- | --- | --- |
| `qemu-mps2-an386-{embos,freertos}` | 18 | 19 (+ `qemu-mps2-an386.peripheriques`) | 19 (+ `net.ping_ftpd`) | 20 |
| `qemu-mps2-an386-*-soft` | 14 | 15 | 15 | 16 |
| `qemu-mps2-an500-*` | 18 | 18 | 19 | 19 |

`ctest -N -L greffon:` (an386, Mac) : 2 tests (`qemu-mps2-an386.peripheriques` et sa fixture
`smoke.lsh`).

### 1.3 Têtes publiées (`git ls-remote`, 2026-11-02)

Toutes égales aux têtes locales des clones de `<ROOTSTOCK>` : lepton-tools `main` d4351bc ;
`seed.scions` `master` e4d76b2, tag `0.5.3.0` → ad292ee ; `lepton-seed.scions` `original-tree`
15740f9 ; noyau 0c0cc4f ; `famille-qemu-mps2` 3954357, `bsp-qemu-mps2-an386` 09f4943,
`bsp-qemu-mps2-an500` e98a482, `famille-stm32f4xx` 8364493, `bsp-nucleo-f429zi` 2b2dfdd,
`bsp-nucleo-f439zi` bdbfa06, `famille-stm32wlxx` dbc58d7, `bsp-nucleo-wl55jc1` c9183de,
`famille-stm32f7xx` d2d9aa9, `bsp-stm32f746g-disco` 6266908, `famille-samd21` a262e81,
`bsp-samd21-xplained-pro` f3cffa2.

### 1.4 Relevés Mac repris dans la consigne

- Trunk `<ROOTSTOCK>` : 14 entrées, 3956 liens, 0 cassé, 0 fichier régulier.
- `original-tree.code-workspace` de `<ROOTSTOCK>` : 23 `"request"`, 7 `"type": "lldb"`,
  10 `"svdFile"` ; sommes SHA-256 des 5 SVD (consigne §9).
- Lancement « Déboguer mklepton qemu-mps2-an386 (…) » : 9 arguments, `env`
  `SOURCE_DATE_EPOCH=0` ; sorties de `build/.mklepton/qemu-mps2-an386` (6 fichiers, `.fsflash.o`
  compris) identiques à `build/qemu-mps2-an386-embos/generated/board/`.

### 1.5 Choix de la consigne (à valider au PA-43)

- C3 : la graine en retard est celle de `essais/env-14-debian` de la VM (0f1275a, ENV-14) ;
  `graft-update` y est accordé au titre de PA-P, seul `graft-update` de l'ordre. Rootstock neuf :
  `essais/env-28-debian`.
- C1-C2 : `pipx install` de lepton et scripts d'installation lancés par l'utilisateur, scion
  d'abord (`install-debian.sh`), lepton ensuite (exige scion ≥ 0.5.3.0).
- Commandes scion qui clonent et `rejouer-oracle.sh` : lancées par la session VM (acceptées en
  R21-1), remises à l'utilisateur en cas de refus.
- C5 : forme de l'arrêt dans `main` (A : lldb embarqué par CodeLLDB en mode batch, par la
  session ; B : l'utilisateur sous VSCodium).
- C7 : `env-11/qemu` régénéré par l'ancien lepton avant le relevé (E-1 de R21-1) ; différence
  attendue limitée aux ajouts DBG-5.
- C8 : suppression d'`essais/env-21-debian` et `~/env-21-journaux` par l'utilisateur.

## 2. Messages (§2bis)

| ID | Date | Sens | Résumé |
| --- | --- | --- | --- |

## 3. Rootstocks d'essai (tâche 3)

## 4. Vérification du rapport VM (tâche 4)
