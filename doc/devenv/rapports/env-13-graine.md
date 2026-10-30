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
