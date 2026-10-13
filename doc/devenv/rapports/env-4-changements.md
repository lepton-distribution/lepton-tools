# ENV-4 — Changements du format XML mklepton (PA-4)

Proposition du 2026-10-13, clone noyau `devenv/env-4` (= `master` 6b62af5). Chemins relatifs à
`scion/`. Contrat : `schemas/mklepton.xsd` (format 2, validé en PA-3). Sources : `rapports/env-2-mklepton.md`.

XML actifs (6) : `sys/user/tauon-basic/etc/mkconf_tauon_basic_{qemu_mps2, nucleo_f439zi,
nucleo_wl55jc1, samd21_xplained_pro, stm32f746g_disco, lwip_stm32f4-olimex-p407}.xml`.

## 1. Éléments × action

| Élément / attribut | Action | Justification | XML actifs touchés | Effet sur les sorties |
| --- | --- | --- | --- | --- |
| `<mklepton version>` | **ajouté**, obligatoire, valeur `2` | CFG-8 ; refus d'une version inconnue | 6 | aucun |
| `<target name>` | **retiré** (contenu `cortexm_lepton` déballé, autres cibles supprimées) ; option `-t` retirée | Seul `cortexm_lepton` sert ; architecture hors XML | 6 (Olimex : branches `win32_lepton` supprimées) | aucun (le contenu retenu est celui de `-t cortexm_lepton`) |
| `<arch dest_path>` | **retiré** | Sortie fixée par `-o` (CMake) ; déjà ignoré quand `-o` est donné | 6 | aucun |
| `<arch include_absolute_path>` | **retiré** → option `--kernel-config-header <chemin>` | Propriété de la carte (manifeste BSP `entete_config_noyau`, ENV-5/8) | 6 | aucun si la même valeur est passée |
| `<cpu freq>` | **retiré** → option `--cpu-freq <Hz>` | Propriété de la carte (manifeste BSP `frequence_cpu`) | 6 | aucun si la même valeur est passée |
| `<cpu type>` + `cpu_type_enum_t`, `cpu_type_list` | **retiré** | Ne produit qu'un commentaire | Olimex (`cpu_arm7`) | **`kernel_mkconf.h`** : disparition de la ligne `//#define CPU_…` (commentaire) |
| `<cpufs block>`, `<cpufs option>` | **retiré** | Lus sans effet | 0 | aucun |
| `<cpufs size>`, `<cpufs node>` | **facultatifs** ; absents ⇒ dimensionnement automatique (PA-3) | CFG-8 | 0 (valeurs conservées à la migration) | aucun pour les 6 ; nouvelle sortie testée à part |
| `MK_DEV_*` M16C/LCD/RTC | **retiré** (code) | Code mort | – | aucun |
| `boot_dev` par défaut `/dev/kb0` | **conservé** (écart à PA-4, à confirmer) | Écrit dans `.boot` quand `<boot dev>` est absent (Olimex) : le retirer change une sortie | – | – |
| `_mk_rtc` | **conservé** (amendement PA-4) | Règle l'horloge depuis `/dev/rtc0` = `dev_host_rtc` (`SOURCE_DATE_EPOCH`) : dates de l'image UFS reproductibles | – | – |
| `heap`, `process`, `thread`, `openfiles`, `descriptors`, `env`, `network`, `devices/dev`, `binaries/bin`, `files/file`, `directories/directory`, `boot/command`, `mount/disk` | **conservés** | Configuration logicielle | – | aucun |
| Deux sections `<devices>` (`cortexm_lepton` + commune) | **fusionnées** en une, ordre conservé | Lisibilité ; ordre de `dev_lst[]` inchangé | 5 cartes | aucun si l'ordre est conservé |

Contrainte de forme pour la migration : `firmware.cmake:26-47` lit `<binaries … src_path>` et
`^[ \t]*<bin name=` ligne à ligne ; le script conserve une balise par ligne.

## 2. Répercussions hors XML

| Fichier | Changement |
| --- | --- |
| `tools/mklepton/src/mklepton.{c,h}` | Lecture `version` ; retraits ci-dessus ; options `--cpu-freq`, `--kernel-config-header` ; cpufs automatique |
| `cmake/mklepton.cmake` | `lepton_generate(… CPU_FREQ … KERNEL_CONFIG_HEADER …)` au lieu de `MKCONF_TARGET` |
| `cmake/boards/*.cmake` (7) | `LEPTON_BOARD_MKCONF_TARGET` → `LEPTON_BOARD_CPU_FREQ`, `LEPTON_BOARD_KERNEL_CONFIG_HEADER` (valeurs reprises des XML) |
| `cmake/components/firmware.cmake` | Appel de `lepton_generate` |
| `tests/host/mklepton_empreintes.sh` | Lit les deux nouvelles variables au lieu de la cible ; valeurs Olimex en dur |
| `tests/host/` (test `host.mklepton`) | Idem |

## 3. Défauts connus (`doc/migration/mklepton.md:21-25`)

| Défaut | Proposition |
| --- | --- |
| Débordement d'un octet `"%s/%s"` (`mklepton.c:1242-1265`) | Déjà corrigé au portage (`mk_join`, +2) ; code de `<mklepton dest_path>` retiré |
| `strncat(…,32)` dans `_mk_dir` | Hors périmètre (aucun `<directory>` en usage) |
| `-r` non analysé seul | Déjà corrigé au portage (`case 'r'`) |
| `kernel_stub.h` désynchronisé | Hors périmètre (ENV-5) |
| `_mk_rtc` exige `/dev/rtc0` | Assumé : `rtc0` toujours fourni par le noyau hôte (`dev_host_rtc`) |

## 4. Constats d'implémentation

- Écritures dans l'image : `_mk_binaries` ignorait les échecs de création et d'écriture ; `_mk_file`
  avançait dans la liste sur une écriture en échec. Corrigé : tout échec ou écriture partielle fait
  échouer mklepton (nécessaire au contrôle des valeurs imposées et au dimensionnement automatique).
- Références restantes aux XML hérités supprimés, laissées en l'état (historique du portage ou outils
  gelés) : `tools/migration/{mass_compile,dep_graph,mkconf_relpaths}.py`, `mklepton_oracle.sh`
  (dépôt parent, `-t` encore utilisé par `mass_compile.py`), `doc/migration/*`,
  `tools/bin/mklepton_gnu.sh`, `tools/config/SConstruct`, `sys/user/tauon-basic/etc/{readme,memo}.txt`.
