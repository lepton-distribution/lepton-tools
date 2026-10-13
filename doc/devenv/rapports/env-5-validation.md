# ENV-5 — Restructuration CMake du greffon noyau : validation

Session du 2026-10-13. Clone noyau `devenv/env-5` depuis `master` 49ed8fe (fusion de `devenv/env-4`).
lepton-tools `devenv/env-5` depuis `main` bf95024.

## Commandes

Oracle avant et après : `scripts/oracle/rejouer-oracle.sh` (lepton-tools), constructions neuves
(`rm -rf <ROOTSTOCK>/build/<preset>`) :

```
scripts/oracle/rejouer-oracle.sh ~/lepton doc/devenv/rapports/oracles/env-5-<avant|apres> \
  --qemu qemu-mps2-an386-{embos,embos-soft,freertos,freertos-soft} --qemu qemu-mps2-an500-{embos,freertos} \
  --carte nucleo-f439zi-{embos,freertos} --carte nucleo-wl55jc1-{embos,freertos} \
  --carte stm32f746g-disco-{embos,freertos} --carte samd21-xplained-pro-{embos,freertos}
```

- `host` : construction, `ctest` complet (`ctest.log`), empreintes mklepton (`mklepton-empreintes.sha256`).
- Chaque preset : construction (`construction.log`), `scripts/oracle/capturer-oracle.sh` sur `lepton.elf`.
- Presets QEMU : `ctest` complet (`banc-kal.log` : fumée `smoke.lsh` = T0, puis banc KAL),
  console de fumée (`fumee.log` = `smoke_lsh_uart0.log`).
- Pas de matériel (décision 2026-10-13) ; NUCLEO-F429ZI = presets `nucleo-f439zi-*`.
- Compilateur : Arm GNU Toolchain 14.2.Rel1 (binutils 2.43.1), identique pour toutes les captures (`outils.txt`).

## Oracle avant (`oracles/env-5-avant/`, état de départ 49ed8fe)

| Preset | Symboles | Sections | Sorties | Fumée | Banc KAL (ctest) |
| --- | --- | --- | --- | --- | --- |
| host | – | – | – | – | 7/7 ; empreintes mklepton = `tests/host/mklepton_empreintes.sha256` |
| qemu-mps2-an386-embos | 1583 | 22 | elf, bin, map | OK | 18/18 |
| qemu-mps2-an386-embos-soft | 1580 | 22 | elf, bin, map | OK | 14/14 |
| qemu-mps2-an386-freertos | 1623 | 21 | elf, bin, map | OK | 18/18 |
| qemu-mps2-an386-freertos-soft | 1622 | 21 | elf, bin, map | OK | 14/14 |
| qemu-mps2-an500-embos | 1545 | 22 | elf, bin, map | OK | 18/18 |
| qemu-mps2-an500-freertos | 1585 | 21 | elf, bin, map | OK | 18/18 |
| nucleo-f439zi-embos | 1690 | 22 | elf, bin, map | – | – |
| nucleo-f439zi-freertos | 1730 | 21 | elf, bin, map | – | – |
| nucleo-wl55jc1-embos | 1215 | 22 | elf, bin, map | – | – |
| nucleo-wl55jc1-freertos | 1261 | 21 | elf, bin, map | – | – |
| stm32f746g-disco-embos | 1624 | 22 | elf, bin, map | – | – |
| stm32f746g-disco-freertos | 1660 | 21 | elf, bin, map | – | – |
| samd21-xplained-pro-embos | 926 | 22 | elf, bin, map | – | – |
| samd21-xplained-pro-freertos | 976 | 21 | elf, bin, map | – | – |

Contrôle de cohérence : `comparer-oracle.py oracles/env-4-apres/<p> oracles/env-5-avant/<p>` = code 0
pour les 4 presets an386 (la fusion de `devenv/env-4` n'a rien changé). Aucun `.hex` produit
aujourd'hui (BLD-4 : à ajouter).

## Changements (clone noyau e564714, aucun code C modifié)

| Élément | Avant | Après |
| --- | --- | --- |
| Bibliothèques | `lepton_core`, `lepton_kal_<b>`, `lepton_dev`, `lepton_vfs`, `lepton_fs_*`, `lepton_net_lwip`, `lepton_libc`, `lepton_bsp_<carte>`, `lepton_sbin`, `lepton_bin`, `lepton_generated` | STATIC `kernel` (kernel/ et kernel/dev/arch), `lib`, `sbin`, `bin`, `bsp` (kernel/dev/bsp) ; hôte : `kernel_posix` |
| Objets liés à l'exécutif | sources de `lepton` | OBJECT `generated` (sources de mklepton), `kernel_demarrage` (démarrage générique, `_sbrk`), `bsp_objets` (vecteurs F439, `hal_tick` WL55) ; `main` et matériel KAL restent sources de `lepton` |
| Groupe d'édition de liens | `RESCAN` : generated, sbin, bin, 7 à 9 archives noyau, libc, bsp | `RESCAN` : sbin, bin, kernel, lib, bsp (+ bibliothèques créées par un greffon) |
| Manifestes | – | `cmake/lepton_greffons.cmake` ; `sys/root/src/lepton-greffon.json` (greffon noyau) |
| Sorties | elf, bin, map | elf, bin, **hex**, map, **occupation.txt** (`tools/occupation/occupation.py`) |
| Variables d'axe | `LEPTON_BSP_NAME`, `LEPTON_BSP_SOURCES` mixtes, `LEPTON_FIRMWARE_SOURCES` | `LEPTON_DEV_ARCH_SOURCES` (→ kernel), `LEPTON_BSP_SOURCES` (→ bsp), `LEPTON_BOARD_OBJECT_SOURCES` (→ bsp_objets), `LEPTON_DEV_ARCH_HOST_SOURCES` |

## Oracle après (`oracles/env-5-apres/`, clone e564714)

| Preset | Sections/symboles (`comparer-oracle.py`) | Empreinte | Fumée | Banc KAL | Écarts expliqués |
| --- | --- | --- | --- | --- | --- |
| host | – | – | – | 7/7 ; empreintes mklepton identiques | – |
| qemu-mps2-an386-embos | code 0 | différente | identique | 18/18, même liste | date de compilation |
| qemu-mps2-an386-embos-soft | code 0 | différente | identique | 14/14, même liste | date |
| qemu-mps2-an386-freertos | `.text` 281476→281464 | différente | identique | 18/18, même liste | remplissage, date |
| qemu-mps2-an386-freertos-soft | `.text` +4 | différente | identique | 14/14, même liste | remplissage, date |
| qemu-mps2-an500-embos | code 0 | différente | identique | 18/18, même liste | date |
| qemu-mps2-an500-freertos | `.text` +4 | différente | identique | 18/18, même liste | remplissage, date |
| nucleo-f439zi-embos | `.text` +4 | différente | – | – | remplissage |
| nucleo-f439zi-freertos | `.bss` +4, `.noinit` 0→4, `.text` +8 | différente | – | – | remplissage |
| nucleo-wl55jc1-embos | `.bss` +8 | différente | – | – | remplissage |
| nucleo-wl55jc1-freertos | `.bss` +4, `.noinit` 4→0, `.text` +4 | différente | – | – | remplissage |
| stm32f746g-disco-embos | `.bss` 110384→112952, `.text` +4 | différente | – | – | remplissage (`.bss.eth_dma` aligné sur 16 Kio) |
| stm32f746g-disco-freertos | `.bss` 110384→112780, `.noinit` 0→4, `.text` +20 | différente | – | – | idem |
| samd21-xplained-pro-embos | `.text` +8 | différente | – | – | remplissage |
| samd21-xplained-pro-freertos | `.bss` +8, `.ccm_bss` +8, `.text` −4 | différente | – | – | remplissage |

**Symboles** : aucun écart sur les 14 presets (même ensemble nom, type, taille).

**Écarts de taille de section : remplissage d'alignement seul, démontré.** L'ordre des objets à
l'édition de liens change (objets OBJECT en tête, une archive `kernel` au lieu de sept à neuf), donc
les adresses et le remplissage `*fill*` entre sections d'entrée. Preuve : `env-5-preuve-remplissage.sh`
construit les 14 presets dans une même copie du rootstock (même chemin, donc mêmes `__FILE__`),
clone noyau sur 49ed8fe puis sur `devenv/env-5`, et relève par section de sortie taille, remplissage et
contenu (`env-5-contenu-sections.py`, sorties `oracles/env-5-contenu/`) : **contenu (taille − *fill*)
identique pour toutes les sections des 14 presets** ; `.noinit` (4 octets) n'est que remplissage.
Cas F746 : `.bss.eth_dma` (tampons DMA Ethernet) est aligné sur 0x4000 ; le remplissage qui le précède
passe de 12726 à 15122 octets (freertos) selon la fin des `.bss` qui précèdent.

**Fumée** : identique après normalisation de la date de compilation (bannière et `uname`), du jeton
`lepton-uart1-<n>`, des messages asynchrones `rcv SIGCHLD` et du chiffre de processus intercalé à
l'invite, et des lignes vides qu'ils laissent (comportement présent depuis ENV-0, 1 à 3 occurrences
selon l'exécution, avant comme après).

**Banc KAL** : même liste de tests, tous verts (18 en ABI hard, 14 en soft), an386 et an500.

## Critères de l'étape

| Critère | Résultat |
| --- | --- |
| `cmake --build` réussit (QEMU, F429ZI, WL55JC1) | 14 presets croisés + host construits à neuf (`rejouer-oracle.sh`, code 0) |
| Cibles `kernel`, `lib`, `sbin`, `bin`, `bsp`, exécutif visibles | `cmake --build <build> --target help` : `kernel`, `lib`, `sbin`, `bin`, `bsp`, `lepton` (an386) ; `bsp` absente si la carte n'a pas de source BSP (aucun cas), `bin` absente si le mkconf n'en déclare pas (samd21), comme avant |
| Banc KAL et fumée identiques | oui (ci-dessus) |
| Symboles de la MAP identiques | oui, 14/14 ; écarts de sections = remplissage, démontré |
| Greffon d'essai (BLD-2) | voir ci-dessous |
| BLD-3 | mklepton inchangé (`add_custom_command`, sorties sous `<build>/generated/board`) ; empreintes host identiques |
| BLD-4 | `lepton.hex`, `lepton.occupation.txt` produits sur les 14 presets ; totaux = `size` au remplissage près |

## Greffon d'essai (BLD-2, FIC-4, CFG-3)

Copie du rootstock (`cp -RP`, supprimée ensuite) ; fichiers ajoutés au greffon local déjà inscrit
`lepton building *` (`depots/generation/building/scion/sys/root/src/bin/essai/` : `essai.c` +
`lepton-greffon.json`, type `application`, bibliothèque `bin`, `sources: [""]`, définition privée
`ESSAI_PRIVEE`, option entière `ESSAI_VALEUR=42` privée ; valide au schéma), `scion graft`, aucun
`CMakeLists.txt` modifié. (Un clone `depots/essai/…` inscrit dans `.scion.grafted.list` a été refusé
par le hook : écriture visant `trunk/` de la copie ; non contourné.)

| Essai | Résultat |
| --- | --- |
| an386-freertos : greffon découvert et compilé | `greffons : essai;lepton-noyau` ; `essai.c.obj` dans `libbin.a` ; `#error` du fichier non déclenché |
| Portée privée | `-DESSAI_PRIVEE -DESSAI_VALEUR=42` sur `essai.c` seul (`compile_commands.json`) |
| Fichier ajouté (`essai2.c`) + `scion graft`, `cmake --build` seul | reconfiguration automatique, `essai2.c.obj` dans `libbin.a` |
| Noyau : définition publique et privée (manifeste noyau de la copie) | publique : toutes les sources (y compris `dev_mkconf.c`, `essai.c`) ; privée : sources du noyau seules (`bin.c`, `libc.c`, `ls.c`, `startup_armv7m.c`), pas `essai.c` |
| Champ `version` retiré | reconfiguration, `FATAL_ERROR` : « manifeste …/bin/essai/lepton-greffon.json : champ obligatoire « version » absent » |
| samd21-freertos (pas de `bin` du mkconf) | bibliothèque `bin` créée par le greffon et liée |
| ELF avec greffon (non référencé) | symboles identiques à l'oracle ; tailles de sections plus grandes, attribuées au chemin plus long de la copie (`__FILE__`, `.debug_*`) ; non démontré octet à octet (greffon retiré) |

Défauts trouvés et corrigés pendant l'essai : élément `""` de `sources` perdu (liste CMake vide → « . ») ;
manifeste modifié sans reconfiguration (ajout à `CMAKE_CONFIGURE_DEPENDS`) ; options privées du noyau
appliquées aux sources d'un greffon partageant la cible (posées sur les sources du noyau).
