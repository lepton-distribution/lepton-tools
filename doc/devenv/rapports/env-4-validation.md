# ENV-4 — Validation du format XML 2 de mklepton

Session du 2026-10-13. Clone noyau `devenv/env-4` (depuis `master` 6b62af5) : 51ca49f, 79f1179,
1c8281d, 1570ac1. lepton-tools `devenv/env-4` : script `scripts/migrer-xml-mklepton.py`.
Changements validés en PA-4 : `env-4-changements.md`.

## Commandes

Oracle avant et après : même script, constructions neuves (`rm -rf <ROOTSTOCK>/build/<preset>`) :
preset `host` (ctest, `tests/host/mklepton_empreintes.sh --out`), puis pour chaque preset an386
configuration, construction, `ctest`, `scripts/oracle/capturer-oracle.sh`, copie de
`smoke_lsh_uart0.log`. Comparaison : `scripts/oracle/comparer-oracle.py`. Compilateur identique
(`outils.txt`).

## Sorties de mklepton (6 XML, 38 fichiers)

| Étape | Résultat |
| --- | --- |
| Temps 1 (51ca49f + 79f1179 : format 2, migration) | 37/38 identiques ; `kernel_mkconf.h` d'Olimex : ligne `//#define CPU_ARM7` devenue `CPU_GNU32` (`<cpu type>` retiré) ; empreinte de l'oracle retrouvée en rétablissant cette ligne |
| Temps 2 (1c8281d : retrait de `CPU_*`) | 32/38 identiques ; les 6 `kernel_mkconf.h` perdent la ligne `//#define CPU_…` ; pour chacun, réinsérer la ligne redonne exactement l'empreinte de l'oracle (`env-4-preuve-cpu.sh`) |
| Nouvelle référence | `tests/host/mklepton_empreintes.sha256` régénérée (6 lignes `kernel_mkconf.h`), décision PA-4 ; égale à `oracles/env-4-apres/host/mklepton-empreintes.sha256` |
| 1570ac1 (cpufs automatique) | Aucune sortie changée pour les 6 XML (valeurs imposées) |

## Binaires et comportement

| Preset | Sections/symboles | Empreinte | Fumée | Banc KAL | Écarts expliqués |
| --- | --- | --- | --- | --- | --- |
| qemu-mps2-an386-embos | identiques (code 0) | différente | identique (voir ignorés) | 18/18, même liste | date de compilation |
| qemu-mps2-an386-embos-soft | identiques (code 0) | différente | identique (voir ignorés) | 14/14, même liste | date de compilation |
| qemu-mps2-an386-freertos | identiques (code 0) | différente | identique (voir ignorés) | 18/18, même liste | date de compilation |
| qemu-mps2-an386-freertos-soft | identiques (code 0) | différente | identique (voir ignorés) | 14/14, même liste | date de compilation |
| host | – | – | – | 7/7 (dont `host.mklepton_format`, nouveau) | – |

Empreintes binaires : déjà différentes entre ENV-0 et `env-4-avant` (date et heure de compilation
dans `uname`). Journaux de fumée : ignorés la date et l'heure de compilation, le jeton aléatoire
`lepton-uart1-<n>`, le message asynchrone `rcv SIGCHLD` et le chiffre de processus qui s'entrelace à
l'invite (présents de 0 à 3 fois selon l'exécution, déjà en ENV-0).

Construction des autres presets (PA-2 Q5) : `qemu-mps2-an500-freertos`, `nucleo-f439zi-embos`,
`nucleo-wl55jc1-freertos`, `samd21-xplained-pro-freertos`, `stm32f746g-disco-embos` construits sans
erreur ; `__KERNEL_CPU_FREQ` et `#include` de l'en-tête de carte conformes aux anciennes valeurs XML.

## Format et migration

- `xmllint --schema schemas/mklepton.xsd` : 6/6 XML du clone valides ; aucun `<target>`, `<arch>`,
  `<cpu>`, ni nom de cœur ou de backend.
- `migrer-xml-mklepton.py` rejoué sur les XML migrés : « déjà au format 2 », aucune écriture ;
  `--verifier` code 0. Essai préalable sur copies : deuxième passage identique octet à octet.
- Refus (test `host.mklepton_format`) : version `3` (« unknown format version "3" (expected "2") »),
  version absente, élément `<target>` : code 1.

## Dimensionnement automatique de cpufs (PA-3)

| XML (size et node retirés) | Imposé | Automatique | Relecture |
| --- | --- | --- | --- |
| qemu_mps2, nucleo_f439zi, stm32f746g_disco | 128000 o, 256 nœuds | 5939 o, 22 nœuds | 14 pseudo-binaires |
| nucleo_wl55jc1 | 8000 o, 128 nœuds | 1755 o, 17 nœuds | 10 |
| samd21_xplained_pro | 3072 o, 64 nœuds | 1706 o, 15 nœuds | 9 |

Copie d'essai du rootstock (supprimée), XML qemu_mps2 sans `size`/`node` : `qemu-mps2-an386-embos` et
`-freertos` 18/18 (fumée `lsh` et banc KAL) avec l'image de 5939 octets. Valeurs imposées trop petites
(`size` ou `node` moins un) : refus avec le minimum ; minimum exact : image identique à l'automatique.

Défaut latent corrigé en chemin : au-delà de la fin du disque hôte, `dev_host_fileflash` renvoyait 0
et `_ufs_drv_1_4_readblk` bouclait sans fin (pile relevée par `sample`). Le pilote hôte (preset
`host` seul, `cmake/isa/host.cmake:46`) renvoie désormais -1 et compte l'accès ; mklepton refuse
l'essai. Aucun code compilé pour les cibles n'est modifié.
