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

### 1.5 Choix de la consigne (validés au PA-43, 2026-11-02 : consigne telle quelle, C5 forme A puis B, C8 accordé, push et ordre)

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
| ORDRE R28-1 | 2026-11-02 | Mac → VM (`debian-linux-vm`) | consigne `env-28-debian.md` @ b8ff911 (blob 61a35cc, SHA-256 d40a5136…) ; décisions PA-43 ; texte de la consigne résumé, référence au fichier poussé avec sa somme (écart à la règle « texte tel quel », signalé à l'utilisateur) |
| ACCUSÉ R28-1 | 2026-11-02 | VM → Mac | `devenv/env-28` b8ff911, SHA-256 de la consigne identique ; `ls-remote` conformes au §1 ; graine d'`env-14-debian` 0f1275a, propre, amont `origin/original-tree`, 9 entrées ; hôte Debian 13.7, scion 0.5.2.0, lepton 0.1.0 (ancien), embOS présent, 19 Go libres ; `env-21-debian` et `~/env-21-journaux` présents ; CodeLLDB 1.12.3 ; aucun écart |
| AVANCEMENT R28-1 | 2026-11-02 | VM → Mac | §6.1 : `env-11/qemu` régénéré (ancien lepton, « inchangé »), `check` 0 (5 fichiers), graine propre, presets d5ee81e4…, espace 0c06a5f7… (= valeur de R21-1) ; noyau 40d7197 → 0c0cc4f, `SCION_REF` 0.5.3.0 ; attente des 4 commandes de l'utilisateur (§6.2) |
| AVANCEMENT R28-1 | 2026-11-02 | VM → Mac | §6 conforme (C1, C2) : 4 codes 0 ; scion 0.5.2.0 → 0.5.3.0 par `install-debian.sh` ; lepton 0.1.0 accepte scion 0.5.3.0 ; `changements 0` aux deux exécutions d'`install-vscodium.sh` ; codium 1.135.06055, CodeLLDB 1.12.3. §7.1 : 3929 liens avant ; `scion graft-update -v` refusé par le classifieur de la VM (« Untrusted Code Integration »), non contourné, remis à l'utilisateur |
| QUESTION R28-1 | 2026-11-02 | VM → Mac | §7.1 lancé par l'utilisateur : `graft-update` code 1 ; graine avancée 0f1275a → 15740f9, 14 entrées, 5 greffons clonés sur `master` ; mais clones `original` (e5a5689) et `family-stm32f4xx` (af964c6) restés sur `devenv/env-14` (checkout de la validation ENV-14 Debian, 2026-10-30) : `pull` sans retour à la version déclarée `master` ; 277 conflits (208 `family-stm32f7xx`, 69 `family-samd21`) ; trunk vidé (0 lien, 3929 avant) ; clones propres. Options A (`switch master` des 2 clones, puis relance par l'utilisateur) ou B (échec partiel consigné) |
| RÉPONSE R28-1 | 2026-11-02 | Mac → VM | option A (PA-43 (2), utilisateur) : `switch master` des 2 clones propres (`merge --ff-only` si besoin), relance par l'utilisateur (`7.1-graft-update-2.log`), §7.2 poursuivi ; écart E-x et 2 constats scion au rapport VM |
| AVANCEMENT R28-1 | 2026-11-02 | VM → Mac | §7 conforme (C3) : clones propres, `switch master`, HEAD 16a331b / 01b5528 (le `pull` n'avait avancé que `origin/master`) → `merge --ff-only` 0c0cc4f / 8364493 ; 2e `graft-update` (utilisateur) code 0, 0 conflit, 14 entrées, 13 clones au §1, 3956 liens, 0 cassé, 0 régulier ; §7.2 par la session (pas de refus) : codes 0, 14 entrées, 3956 liens, 0 cassé, 0 régulier, 0 `.DS_Store`, liste = `$U` ; §8 lancé |
| AVANCEMENT R28-1 | 2026-11-02 | VM → Mac | §11 conforme (C8) : `env-21-debian` 363M, `~/env-21-journaux` 1,2M, supprimés par l'utilisateur, absence vérifiée ; `$R`, `$U`, `$J` conservés ; §8 (`rejouer-oracle.sh`) en cours sur `devenv/env-28-debian`, non refusé |
| AVANCEMENT R28-1 | 2026-11-02 | VM → Mac | §8 conforme (C4, C6) : `rejouer-oracle` code 0 ; host 7/7 ; 16 presets ; fumée ; banc an386 20/20, soft 16/16, an500 19/19 ; `peripheriques` listé, `-L greffon:` = 2, Passed dans les 4 an386, absent d'an500 ; mklepton = `env-27-apres`, 14 lignes contre R21-1 ; `comparer_R21-1` 1 ×16, écarts du tableau seuls (deltas vérifiés), symboles en nombre identique à R21-1 ; `comparer_Mac` 1 ; f429→f439 0 |
| AVANCEMENT R28-1 | 2026-11-02 | VM → Mac | §9 forme A et §10 conformes (C7) : `check` 0 (19), `generate` 0 ; 23 request, 10 svdFile, 7 lldb, SVD aux sommes ; `mklepton` hors débogueur = construction (6 fichiers) ; lldb 1.12.3 : breakpoint 1.1, `main(argc=10)` à `mklepton.c:2383`, unité de compilation sous `$R/trunk` ; `env-11/qemu` : diff limité aux ajouts DBG-5 ; attente de la forme B |
| AVANCEMENT R28-1 | 2026-11-02 | VM → Mac | §9 forme B (utilisateur) conforme (C5) : arrêt dans `main`, `argc`/`argv` lisibles, source par le trunk ; tâche préalable exécutée (répertoires `build/.mklepton/<BSP>` créés, `.ninja_log` du host écrit) ; rapport et oracle (97 fichiers) commités 1904c83 sur `devenv/env-28-debian`, non poussé ; QUESTION du push à l'utilisateur |
| FIN-SUCCÈS R28-1 | 2026-11-02 | VM → Mac | C1 à C8 conformes (C3 sur le 2e `graft-update`, E-1) ; `devenv/env-28-debian` 1904c83 (depuis b8ff911), poussée avec l'accord de l'utilisateur ; rapport `rapports/env-28-debian.md`, oracle `oracles/env-28-debian/` ; écarts E-1, E-2 ; proposition : branche des clones au §5 des consignes ; non fait : flashage |

Constat pour la tâche 3 : avant tout `graft-update` d'un rootstock d'essai du Mac, relever la
branche courante de chaque clone (`git -C <clone> branch --show-current`) ; un clone hors de sa
version déclarée reproduit l'échec du §7.1.

## 3. Rootstocks d'essai (tâche 3)

### 3.1 Inventaire avant (lecture seule, 2026-11-02)

Tous les clones de greffons sont sur `master`, propres, amont `origin/master` (aucun clone hors de
sa version déclarée, contrairement à `env-14-debian` de la VM).

| Rootstock | Entrées | Liens | Cassés / réguliers | `.scion.trunk.tolerated` | Graine | Clones (têtes) |
| --- | --- | --- | --- | --- | --- | --- |
| `env-9` | 5 | 3055 | 0 / 0 | oui | `env9` dc343d8, locale sans amont | noyau 40d7197, qemu-mps2 3954357, an386 046779e |
| `env-11/f429zi` | 5 | 3366 | 0 / 0 | oui | `env11f4` e4129d2, sans amont | noyau 40d7197, f429zi 8ea7ee5, stm32f4xx 2b21340 |
| `env-11/qemu` | 5 | 3055 | 0 / 0 | oui | `env11` 124db52, sans amont ; application `salut` 4e1df4c | noyau 40d7197, qemu-mps2 3954357, an386 046779e |
| `env-11/qemu-gra2` | 4 | 3049 | 0 / 0 | oui | `env11` d7e3a55, sans amont | noyau 40d7197, qemu-mps2 3954357, an386 046779e (BSP retiré, GRA-2) |
| `env-11/wl55jc1` | 5 | 3302 | 0 / 0 | oui | `env11wl` aec1483, sans amont | noyau 40d7197, stm32wlxx 1eccc2f, wl55jc1 a329f4d |
| `env-11/bout-en-bout/rootstock` (recréé en ENV-22) | 5 | 3054 | 0 / 0 | oui | `bout-en-bout` 393e945, sans amont, 1 fichier non suivi (`lepton-graine.lock.json`, connu) | noyau 40d7197, qemu-mps2 3954357, an386 046779e (amont `file://` vers `<ROOTSTOCK>/depots`) |
| `env-13-vierge` | 14 | 3941 | 0 / 0 | oui | `original-tree` 15740f9 = publiée (pas d'avance attendue) | 13 clones aux têtes d'ENV-20/21 (noyau 40d7197…) |

Têtes attendues après `graft-update` : celles du §1.3.

### 3.2 Regreffe (décision de l'utilisateur : les 7, PA-P) et contrôles

Journaux : `~/lepton-tools-dev/essais/env-28-mac/` (`<rootstock>-{liens-avant,liens-apres}.txt`,
`-graft-update.log`, `-check.log`, `-generate.log`). `scion graft-update -v` : code 0 partout ;
graines locales « sans amont, laissée telle quelle » ; `env-13-vierge` : graine déjà à 15740f9.
`qemu-gra2` : BSP an386 réinscrit par `sync` (comme en ENV-14 et ENV-21) →
`scion graft-remove lepton@bsp-qemu-mps2-an386` sans `--purge` (8 feuilles), code 0.

| Rootstock | Liens avant → après | Liens ajoutés / retirés | Entrées | Cassés / réguliers | `check` | `generate` | Lancements (`request` / `lldb` / `svdFile`) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `env-9` | 3055 → 3057 | +2 (`tests/` an386) / 0 | 5 | 0 / 0 | 0 | 0 | 3 / 1 / 0 |
| `env-11/f429zi` | 3366 → 3370 | +4 (`svd/` stm32f4xx) / 0 | 5 | 0 / 0 | 0 | 0 | 2 / 1 / 1 |
| `env-11/qemu` | 3055 → 3057 | +2 / 0 | 5 | 0 / 0 | 0 | 0 | 3 / 1 / 0 |
| `env-11/qemu-gra2` | 3049 → 3049 | 0 / 0 | 4 | 0 / 0 | 1 (attendu, CFG-5) | 1 (attendu : BSP non greffé) | 1 / 0 / 0 (inchangé) |
| `env-11/wl55jc1` | 3302 → 3305 | +3 (`svd/` stm32wlxx) / 0 | 5 | 0 / 0 | 0 | 0 | 2 / 1 / 1 |
| `env-11/bout-en-bout/rootstock` | 3054 → 3056 | +2 / 0 | 5 | 0 / 0 | 0 | 0 | 2 / 1 / 0 |
| `env-13-vierge` | 3941 → 3956 | +15 (5 SVD, 4 × LICENSE/README, `tests/` an386) / 0 | 14 | 0 / 0 | 0 | 0 | 23 / 7 / 10 (= `<ROOTSTOCK>`) |

Clones : tous sur `master`, propres, aux têtes du §1.3. Graines inchangées ; `bout-en-bout` :
`project/scion/CMakeUserPresets.json` écrit par `generate`, non suivi dans cette graine créée par
le script (s'ajoute au `lepton-graine.lock.json` non suivi déjà connu) : constat, sans effet.

## 4. Vérification du rapport VM (tâche 4)

`git fetch` : `origin/devenv/env-28-debian` 1904c83, descendante de b8ff911 ; 97 fichiers ajoutés,
tous sous `rapports/env-28-debian.md` et `rapports/oracles/env-28-debian/` (périmètre du §2 de la
consigne respecté).

Comparaisons refaites au Mac sur l'oracle poussé :
- `mklepton-empreintes.sha256` : identique à `env-27-apres` ; 14 lignes différentes contre
  `env-21-debian`.
- `ctest.log` host 7/7 ; `banc-kal.log` : 20/20 ×2, 16/16 ×2, 19/19 ×2 ; `peripheriques` Passed
  dans les 4 an386.
- `comparer-oracle.py` `env-21-debian` → `env-28-debian` : code 1 sur les 16 presets ; pour chaque
  preset, l'ensemble des écarts (sections avec leur delta, `filecpu_memory` avant → après) est
  **identique** à celui du Mac `env-20-apres` → `env-27-apres` (comparaison par script) ; bilans :
  14 × 4 écarts, 2 × 2 (SAMD21).
- `f429→f439` : 0 en embOS et FreeRTOS.

Rapport VM (`rapports/env-28-debian.md`) : table des critères C1-C8 conforme à la consigne, chaque
constat chiffré ; E-1 (cause, correction PA-43 (2), deux constats scion) et E-2 décrits ; journal
§2bis conforme aux messages reçus. Verdict : `FIN-SUCCÈS R28-1` vérifié, C1 à C8 conformes.

Propositions non validées issues de R28-1 :
- P-1 : règle des consignes VM (ORCHESTRATION §2bis) : relever au §5 la branche courante de chaque
  clone d'un rootstock existant ; un clone hors de sa version déclarée est un arrêt.
- P-2 : étape scion ultérieure : (a) `graft-update` ramène un clone existant à la version déclarée
  (ou refuse s'il n'y est pas), (b) une regreffe en échec ne laisse pas le trunk vide.
