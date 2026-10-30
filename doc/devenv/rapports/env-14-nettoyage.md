# ENV-14 — Nettoyage de l'arbre : retraits et non-régression

Session du 2026-10-30. Inventaire et décisions : `env-14-inventaire.md`, PA-15
(`DEVENV-STATUS.md` §Décisions).

## 1. Commits

| Dépôt | Branche | Commit | Lot | Fichiers | Octets |
| --- | --- | --- | --- | ---: | ---: |
| clone noyau `depots/lepton/original/master` | `devenv/env-14` (depuis `master` 16a331b) | 2c70c9d | L1 : `tools/bin/`, `tools/config/`, `tools/host/`, `tools/mklepton/prj/`, `sys/user/build/`, `sys/root/src/kernel/net/lwip/prj/`, `tauon_make_link.bat` | 16 | 2 374 930 |
| | | 98481ac | L2 : `sys/user/tauon_sampleapp/` (A0) | 51 | 1 027 020 |
| | | e5e0fcd | L3 : `tauon-basic/etc/memo.txt`, `readme.txt`, `sys/root/src/bin/bin` | 3 | 697 |
| | | e5a5689 | A1 : `tauon-basic/src/arch/st-stm32wl55jci-nucleo/` (1) ; A2 : `tauon-basic/etc/.init_stm32_with_net`, `.init_with_net` (2) ; A3 : `sys/root/src/bin/net/html/` (6), `tauon-basic/src/bin/net/html/lepton_mini.{gif,png}` (2) | 11 | 61 883 |
| greffon `depots/lepton/family-stm32f4xx/master` | `devenv/env-14` (depuis `master` 01b5528) | af964c6 | A5 : `…/cmsis/Device/st/stm32f4xx/system_stm32f4xx.c.old` | 1 | 18 830 |
| **Total versionné** | | | | **82** | **3 483 360** |

Commits mécaniques (`git rm`), un par lot ; aucun autre fichier modifié
(`git diff --stat master..devenv/env-14` = 81 fichiers, 25 140 lignes retirées, rien d'ajouté ;
1 fichier dans le greffon famille). Après chaque lot : `scion graft --scion <clé>` sans `--force`,
puis contrôles `lepton-rootstock` (0 fichier régulier, 0 lien cassé). Construction incrémentale
de `host` (ctest 7/7), `qemu-mps2-an386-freertos`, `nucleo-wl55jc1-freertos` après L1, après L2,
et après A5 pour L3, A1-A3 et A5 ensemble (avec `nucleo-f429zi-freertos`) : toutes réussies,
aucun lot rétabli.

## 2. `.DS_Store` (tâche 3)

| Emplacement | Retirés | Par |
| --- | ---: | --- |
| Trunk, fichiers réguliers | 26 | l'utilisateur (`find … -type f -delete`, hook `proteger-trunk.py`) |
| Clone noyau (ignorés ; 26 greffés dans le trunk en liens) | 30 | la session |
| Graine `original-tree` (`./`, `scion/`) | 2 | la session |
| `depots/generation/`, `depots/origin/` | 5 | la session |
| Répertoires intermédiaires de `depots/` (`depots/`, `depots/lepton/`, `depots/lepton/original/`, `depots/lepton-seed.scions/`) | 4 | la session (même décision PA-15, hors git) |

Laissés : 4 sous des répertoires `.git/` ; `~/lepton/`, `build/`, `third_party/` (hors arbre).
Aucun `.gitignore` modifié (PA-15). Regreffe `original::tree` sans `--force` : les 26 liens vers
les `.DS_Store` du clone disparaissent.

## 3. État du trunk

| Moment | Liens | Fichiers réguliers | Liens cassés | `.DS_Store` |
| --- | ---: | ---: | ---: | ---: |
| Départ | 4 037 | 26 | 0 | 52 |
| Après tâche 3 | 4 011 | 0 | 0 | 0 |
| Après L1 | 3 995 | 0 | 0 | 0 |
| Après L2 | 3 944 | 0 | 0 | 0 |
| Après L3, A1-A3 | 3 930 | 0 | 0 | 0 |
| Après A5 | 3 929 | 0 | 0 | 0 |

4 011 = nombre de liens du rootstock Debian neuf de R13-1 (sans `.DS_Store`).

## 4. Non-régression (skill `lepton-oracle`)

Mêmes commandes avant et après, répertoires de construction neufs :
`scripts/oracle/rejouer-oracle.sh ~/lepton oracles/env-14-<avant|apres> --qemu …×6 --carte …×8`
(host + 14 presets ; liste de `env-13-graine.md` §4). Avant : état de départ, avant la tâche 3 ;
après : les 5 lots retirés. L'oracle avant est conforme à `env-13-apres` (`comparer-oracle`
code 0 sur les 14 presets, empreintes mklepton identiques).

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
| nucleo-f429zi-freertos | identiques | différente | – | – | E1 (démontré) |
| nucleo-wl55jc1-embos | identiques | différente | – | – | E1 |
| nucleo-wl55jc1-freertos | identiques | différente | – | – | E1 (démontré) |
| samd21-xplained-pro-embos | identiques | différente | – | – | E1 |
| samd21-xplained-pro-freertos | identiques | différente | – | – | E1 |
| stm32f746g-disco-embos | identiques | différente | – | – | E1 |
| stm32f746g-disco-freertos | identiques | différente | – | – | E1 |

`comparer-oracle.py` : code 0 sur les 14 presets. Banc KAL : mêmes cas, mêmes résultats (durées
ignorées).

**E1** — date de construction embarquée (« kernel compilation date »), comme en ENV-13, R2, R3 et
R5. Démonstration (`env-14-preuve-empreintes.sh`, copie `~/lepton-tools-dev/essais/env-14-preuve`
du rootstock, sans `build/`) : `SOURCE_DATE_EPOCH` fixé, host puis `qemu-mps2-an386-embos`,
`nucleo-f429zi-freertos` (greffon touché par A5) et `nucleo-wl55jc1-freertos` construits dans
l'état après (3 929 liens), puis clone noyau et `family-stm32f4xx` ramenés sur `master` et regreffés
(4 011 liens, 0 cassé), et reconstruits : `lepton.elf`, `.bin`, `.hex` identiques au bit près
(`oracles/env-14-apres/preuve-e1.log`).

**E2** — `fumee.log` identiques après avoir ignoré la date de compilation du noyau (E1), les
horodatages, les adresses, le jeton aléatoire de l'essai UART (`lepton-uart1-<n>` et le chiffre de
fin renvoyé devant l'invite suivante), la ligne asynchrone `rcv SIGCHLD` et les lignes vides
(normalisation d'ENV-13).

## 5. Contrôles finaux

- `lepton check` sur `~/lepton` : code 1, seule anomalie « manifeste de graine absent (graine hors
  lepton) » — identique au constat d'ENV-12 (`handoff/env-12.md`), admise par le fichier d'étape.
- Références restantes aux chemins retirés (mêmes `grep` qu'en tâche 1) : `DEVENV-STATUS.md` et
  `etapes/ENV-14-nettoyage.md` (plan, décisions) ; commentaire de provenance de
  `mkconf_tauon_basic_samd21_xplained_pro.xml` (cite `tauon_sampleapp/etc/…`) et en-tête de
  `include/user_kernel_mkconf.h` du BSP `nucleo-wl55jc1` (cite `src/arch/st-stm32wl55jci-nucleo`),
  laissés au PA-15 ; `net/html` dans le XML Olimex et `lhttpd.c` désigne
  `tauon-basic/src/bin/net/html/`, conservé. Aucune autre.

## 6. Validation Debian (ordre R14-1, ORCHESTRATION §2bis)

Consigne `consignes/env-14-debian.md` ; branches poussées au PA-16 (1) : clone noyau
`devenv/env-14` e5a5689, `family-stm32f4xx` `devenv/env-14` af964c6, lepton-tools `devenv/env-14`
42d3906 (`git ls-remote` conforme).

| Date | Message | Résumé |
| --- | --- | --- |
| 2026-10-30 | `ORDRE R14-1` | `nettoyage-arbre-env-14` → `lepton-vm-debian` (Remote Control) : rootstock neuf depuis `original-tree`, bascule noyau et `family-stm32f4xx` sur `devenv/env-14`, 15 presets, non-régression contre R13-1 ; texte intégral de la consigne |
