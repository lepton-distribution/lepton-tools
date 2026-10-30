# ENV-13 — Graine de référence publiée : rapport

Étape : `etapes/ENV-13-graine-publiee.md`. Session du 2026-10-30.

## 1. État de départ (2026-10-30)

| Élément | État |
| --- | --- |
| lepton-tools | `main` 14d64e9, propre ; branche `devenv/env-13` |
| Clone noyau `depots/lepton/original/master` | `master` 16a331b = `origin/master`, propre |
| Graine `depots/lepton-seed.scions/original-tree` | `original-tree` 43d12e6, 4 commits d'avance sur `origin/original-tree`, propre ; branche `devenv/env-13` |
| 7 greffons `depots/lepton-famille/*`, `depots/lepton-bsp/*` | `master` = `origin/master` = table du fichier d'étape, propres |
| `trunk/.scion.grafted.list` | 9 entrées : `original::tree` (`master`), `building` (`*`), 7 `famille::`/`bsp::` (`*`, chemins locaux) |
| Trunk | 4037 liens, 0 lien cassé ; 24 fichiers réguliers, tous `.DS_Store` du Finder (non versionnés) |
| Outils | scion 0.5.1.1, lepton 0.1.0 |

## 2. Séquence de regreffe (PA-13)

Lecture de `<SEED_SCIONS>/scion/` (f1d1f3c, 0.5.1.1) :
- `graft.sync`, appelé par `seed-clone`, lit la liste greffée, ajoute ou remplace les clés des
  ramifications et réécrit la liste : **il ne retire jamais une clé absente de la graine**. Les
  anciennes clés sont donc retirées par `graft-remove`.
- Source distante → clone dans `depots/<shelf>/<préfixe>/<version>` ; une clé sans `::` a pour
  préfixe la clé entière → `depots/lepton/family-<nom>/master`, `depots/lepton/bsp-<nom>/master`.
- `seed-clone` = `sync(update=False)` : clone ce qui manque, aucun `pull` des clones existants.
- `graft-remove` et `graft` refusent un trunk qui contient des fichiers réguliers (`_check_stray`) :
  les 24 `.DS_Store` imposent `--force`, qui les conserve.

Séquence (depuis `<ROOTSTOCK>`) :
```bash
# 1. graine : commit 9d72b6b sur devenv/env-13 (sources + ramifications)
# 2. retrait des 7 anciennes clés (clones conservés)
scion graft-remove --force lepton@famille::qemu-mps2      # idem bsp::qemu-mps2-an386, bsp::qemu-mps2-an500,
                                                          # famille::stm32f4xx, bsp::nucleo-f429zi,
                                                          # famille::stm32wlxx, bsp::nucleo-wl55jc1
# 3. clonage des 7 sources https://, ajout des 7 nouvelles clés
scion seed-clone --seed depots/lepton-seed.scions/original-tree
# 4. regreffe des 7 nouvelles clés
scion graft --force --scion lepton@family-qemu-mps2 --scion lepton@bsp-qemu-mps2-an386 … (×7)
# 5. pushurl SSH
git -C depots/lepton/<clé>/master remote set-url --push origin ssh://git@github.com/lepton-distribution/lepton-<famille|bsp>-<nom>.git
```

Essai sur la copie `~/lepton-tools-dev/essais/env-13` (`cp -RP ~/lepton`) :

| Étape | Résultat |
| --- | --- |
| `graft-remove` sans `--force` | refus (`.DS_Store` listés), liste greffée inchangée |
| `graft-remove --force` ×7 | 5 + 6 + 6 + 315 + 8 + 236 + 22 = 598 feuilles retirées ; 2 entrées restantes |
| `seed-clone` | 7 clones `https://`, `master` aux commits de la table ; 9 entrées |
| `graft --force --scion` ×7 | 598 feuilles liées |
| pushurl | fetch `https://`, push `ssh://` pour les 7 |
| Contrôles | 9 entrées, 0 lien cassé, 0 fichier régulier hors `.DS_Store`, 0 lien vers `lepton-(famille\|bsp)/`, 598 liens vers `depots/lepton/(family\|bsp)-` |
| Trunk copie / trunk réel | identiques : 4037 liens, mêmes chemins, même SHA-256 des cibles |

Aucun code de lepton-tools (`*.py`, `*.ts`, `*.sh`, `*.json`, `*.cmake`) ne cite les clés
`famille::`/`bsp::`.

Décision de l'utilisateur (PA-13, 2026-10-30) : séquence validée, accord PA-P pour la regreffe
réelle après l'oracle avant ; `.DS_Store` conservés (`--force`) ; commit de graine rapatrié de la
copie ; oracle sur les 15 répertoires d'`env-8-r3-apres` (`host` compris).

## 3. Graine et regreffe de `<ROOTSTOCK>` (2026-10-30)

- Graine : `devenv/env-13` = 9d72b6b (commit de la copie, rapatrié par `git fetch` + avance rapide),
  sur 43d12e6 ; 5 commits d'avance sur `origin/original-tree` (4 d'ENV-6 + celui-ci) ; `master` non
  touché.
- Regreffe : séquence du §2 sur `~/lepton`, après l'oracle avant. Retrait 598 feuilles, 2 entrées ;
  `seed-clone` code 0 ; greffe partielle 598 feuilles.
- 7 clones `depots/lepton/<clé>/master`, `master` aux commits de la table, propres ; fetch
  `https://`, push `ssh://git@github.com/lepton-distribution/…`.
- Contrôles : 9 entrées (`original::tree`, `building`, 7 `family-`/`bsp-`) ; 0 lien cassé ; 0 fichier
  régulier hors les 24 `.DS_Store` ; 0 lien vers `lepton-(famille|bsp)/` ; 598 vers
  `depots/lepton/(family|bsp)-` ; clone noyau propre. Trunk identique à l'état de départ (4037
  liens, mêmes chemins, même SHA-256 des cibles).

## 4. Non-régression (skill `lepton-oracle`)

Mêmes commandes avant et après, répertoires de construction neufs :
`scripts/oracle/rejouer-oracle.sh ~/lepton oracles/env-13-<avant|apres> --qemu …×6 --carte …×8`
(host + 14 presets). Même chaîne (Arm GNU Toolchain 14.2.Rel1) : `outils.txt` ne diffère que par
l'horodatage de capture.

| Preset | Sections/symboles | Empreinte | Fumée | Banc KAL | Écarts expliqués |
| --- | --- | --- | --- | --- | --- |
| host | – | – | – | ctest 7/7 = 7/7 ; mklepton identiques | – |
| qemu-mps2-an386-embos | identiques | différente | identique (E2) | 18/18 = 18/18 | E1 (démontré) |
| qemu-mps2-an386-embos-soft | identiques | différente | identique (E2) | 14/14 = 14/14 | E1 |
| qemu-mps2-an386-freertos | identiques | différente | identique (E2) | 18/18 = 18/18 | E1 |
| qemu-mps2-an386-freertos-soft | identiques | différente | identique (E2) | 14/14 = 14/14 | E1 |
| qemu-mps2-an500-embos | identiques | différente | identique (E2) | 18/18 = 18/18 | E1 |
| qemu-mps2-an500-freertos | identiques | différente | identique (E2) | 18/18 = 18/18 | E1 |
| nucleo-f429zi-embos | identiques | différente | – | – | E1 |
| nucleo-f429zi-freertos | identiques | différente | – | – | E1 |
| nucleo-wl55jc1-embos | identiques | différente | – | – | E1 |
| nucleo-wl55jc1-freertos | identiques | différente | – | – | E1 (démontré) |
| samd21-xplained-pro-embos | identiques | différente | – | – | E1 |
| samd21-xplained-pro-freertos | identiques | différente | – | – | E1 |
| stm32f746g-disco-embos | identiques | différente | – | – | E1 |
| stm32f746g-disco-freertos | identiques | différente | – | – | E1 |

`comparer-oracle.py` : code 0 sur les 14 presets. Banc KAL : mêmes cas, mêmes résultats (durées
ignorées).

**E1** — date de construction embarquée (« kernel compilation date »), comme en R2, R3 et R5 ; elle
touche aussi samd21 et stm32f746, qui n'utilisent aucun greffon déplacé. Démonstration
(`env-13-preuve-empreintes.sh`, copie `essais/env-13-preuve` du rootstock regreffé, sans `build/`,
`SOURCE_DATE_EPOCH=1760536800`, même répertoire de construction) : construction après regreffe, puis
graine ramenée à 43d12e6 et anciennes clés regreffées depuis `depots/lepton-(famille|bsp)/`, puis
construction de nouveau. `lepton.elf`, `.bin` et `.hex` identiques pour `qemu-mps2-an386-embos` et
`nucleo-wl55jc1-freertos` (`oracles/env-13-apres/preuve-e1.log`). L'ELF aussi est identique :
les informations de débogage portent les chemins du trunk, pas ceux des clones. Le piège prévu par
le fichier d'étape (empreintes différentes à cause du chemin du clone) ne se produit pas.

**E2** — `fumee.log` identiques après avoir ignoré la date de compilation du noyau (E1), les
horodatages, les adresses, le jeton aléatoire de l'essai UART (`lepton-uart1-<n>` et le chiffre de
fin que la console renvoie devant l'invite suivante), la ligne asynchrone `rcv SIGCHLD` et les
lignes vides (même normalisation qu'en R3).

**Constat (anciens clones)** — dans la copie de preuve, la regreffe des anciennes clés a d'abord
échoué (« sys/.DS_Store : déjà fourni par lepton/original::tree, réclamé par
lepton/bsp::qemu-mps2-an500 »), et scion a annulé la greffe. L'ancien clone `lepton-bsp/qemu-mps2-an500`
contient deux `.DS_Store` ignorés par git sous `scion/` (`scion/.DS_Store`, `scion/sys/.DS_Store`).
Ils ont été supprimés dans la copie seulement. Les nouveaux clones n'en contiennent pas.

## 5. Publication et anciens clones (PA-14, 2026-10-30)

Décision de l'utilisateur : push de la graine (pushurl SSH) ; anciens clones archivés puis
supprimés ; rootstock vierge `essais/env-13-vierge` ; copies d'essai supprimées en fin d'étape.

- Graine : `devenv/env-13` fusionnée dans `original-tree` (0f1275a, « Fusion de devenv/env-13 ») ;
  `remote.origin.pushurl` = `ssh://git@github.com/lepton-distribution/lepton-seed.scions.git` ;
  `git push origin original-tree` : 083c30b..0f1275a. `git ls-remote` : `original-tree` 0f1275a,
  `master` f41a23f (inchangé). `devenv/env-13` de la graine non poussée.
- Anciens clones : sur toutes les branches et tous les tags, aucun commit absent d'`origin/master` ;
  `devenv/env-6` (7 dépôts) et `devenv/env-9` (`nucleo-wl55jc1`) contenues dans `master` ; seuls des
  `.DS_Store` ignorés. Archive `~/lepton-tools-dev/essais/archives/lepton-anciens-clones-famille-bsp-20261030.tar.gz`
  (8,4 Mo, 2517 entrées, SHA-256 7741048128ac2cc38e7134232e709c1f546a52a26a6db5f4ea11227447867a87), puis
  `rm -rf depots/lepton-famille depots/lepton-bsp`. Trunk : 0 lien cassé après suppression.
- Graines d'essai qui les désignent en `file://` (`essais/env-9`, `essais/env-11/{qemu,qemu-gra2,f429zi,wl55jc1}`) :
  leurs clones existent déjà et restent utilisables ; un nouveau `seed-clone` ou `graft-update` y
  échouerait (archive à restaurer, ou graine à repointer sur GitHub).
- Copies `essais/env-13` et `essais/env-13-preuve` supprimées (résultats dans ce rapport et
  `oracles/env-13-apres/preuve-e1.log`).

## 6. Rootstock vierge (tâche 7)

`~/lepton-tools-dev/essais/env-13-vierge` :
```bash
scion rootstock-install
scion seed-add --version original-tree https://github.com/lepton-distribution/lepton-seed.scions.git
scion graft
```
- 9 entrées ; 9 clones `https://` (noyau 16a331b, graine 0f1275a, 7 greffons aux commits de la
  table) ; 4011 liens, 0 cassé, 0 fichier régulier. Les 26 liens de plus de `~/lepton` (4037) sont
  tous des `.DS_Store` ignorés du clone noyau local.
- `qemu-mps2-an386-freertos` (avec `host`) : construction réussie ; `ctest` 18/18, dont `smoke.lsh`
  (`uname -a` : `cortexM4-qemu-mps2-an386`). Capture `oracles/env-13-vierge/qemu-mps2-an386-freertos/`.
- Comparaison avec `env-13-apres` : symboles identiques ; `.text` +156, `.debug_line` +28892,
  `.debug_str` +4030 (code 1). **E3** : chemin absolu du rootstock dans les chaînes `__FILE__`
  (5 dans le `.bin` : `tasks.c`, `queue.c`, `timers.c`, `event_groups.c`, `port.c` de FreeRTOS) et dans
  les informations de débogage ; `/Users/cle_d_anton/lepton-tools-dev/essais/env-13-vierge` a 31
  caractères de plus que `/Users/cle_d_anton/lepton` : 5 × 31 = 155, 156 avec l'alignement. Effet
  connu de l'absence de `-ffile-prefix-map` (PA-1) ; pas de changement de code.

## 7. Critères de validation

- [x] PA-13 et PA-14 tranchés et consignés.
- [x] Graine : 7 clés `family-`/`bsp-`, version `master`, URL `https://` ; `original::tree` et
      `building` inchangés ; 4 commits d'ENV-6 conservés.
- [x] 7 clones sous `depots/lepton/<clé>/master` au commit de la table ; pushurl SSH.
- [x] Trunk : 0 fichier régulier (hors 24 `.DS_Store` conservés, PA-13), 0 lien cassé, 0 lien vers
      les anciens clones.
- [x] `comparer-oracle.py` code 0 sur les 14 presets ; fumée et banc KAL identiques sur les 6
      presets QEMU.
- [x] `original-tree` poussée ; un rootstock vierge greffe l'arbre complet depuis GitHub et le
      preset QEMU passe la fumée.

## 8. Validation Debian (ordre R13-1, après clôture)

Demande de l'utilisateur : reconstruire toutes les cibles sur la VM Debian depuis la graine publiée.
Consigne `consignes/env-13-debian.md` (2b92666), texte envoyé tel quel dans l'ordre.

| Date | Message | Résumé |
| --- | --- | --- |
| 2026-10-30 | `ORDRE R13-1` → `lepton-portage-debian` | rootstock neuf `~/lepton-tools-dev/essais/env-13-debian` depuis `original-tree`, host + 14 presets, fumée et banc KAL QEMU, rapport sur `devenv/env-13-debian` (push sur accord) |
| 2026-10-30 | `ACCUSÉ R13-1` ← `lepton-portage-debian` | ordre reformulé conforme ; lepton-tools `main` d0c54d1 ; `git ls-remote` des 9 dépôts conforme ; Debian 13.7, scion 0.5.1.1, lepton 0.1.0, gcc 14.2.1 (paquet Debian), cmake 3.31.6, QEMU 10.0.13, embOS présent ; écarts non bloquants : consigne non poussée (texte de l'ordre fait foi), QEMU 10.0.13 contre 11.1.2, `/tmp` 647 Mo libres |
| 2026-10-30 | `AVANCEMENT R13-1` ×2 ← `lepton-portage-debian` | §6 : greffe conforme (C2) ; §7-§8 : C1 à C6 conformes, rapport f8aec03 en local |
| 2026-10-30 | `FIN-SUCCÈS R13-1` ← `lepton-portage-debian` | C1 à C6 conformes ; `devenv/env-13-debian` f8aec03 poussée (accord de l'utilisateur sur la VM), fusionnée dans `main` par la session Mac ; rapport `rapports/env-13-debian.md`, captures `oracles/env-13-debian/` |

Résultat (`rapports/env-13-debian.md`) : rootstock neuf depuis `original-tree` (9 entrées, 4011 liens,
0 cassé) ; host ctest 7/7, empreintes mklepton **identiques** au Mac ; 14/14 presets construits
(embOS compris) ; 6 presets QEMU : fumée réussie, banc 19/19 (hard) et 15/15 (soft) ; trunk propre
après construction.

Écarts :
- `net.ping_ftpd` en plus sous Debian : test réseau (tap en espace de noms) créé seulement hors
  macOS (`cmake/components/firmware.cmake:202-208` du noyau, décision du 2026-10-08) ; attendu.
- `comparer-oracle.py` code 1 Mac/Debian sur les 14 presets (+15/16 symboles côté Debian, sections
  `.debug_*`) : chaînes différentes (Arm GNU Toolchain 14.2.Rel1 / paquet Debian 14.2.1, binutils
  2.44) ; comparaison informative, non analysée.
- QEMU 10.0.13 (Debian) contre 11.1.2 (Mac) : sans effet sur les résultats.
