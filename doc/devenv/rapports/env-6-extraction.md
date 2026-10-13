# ENV-6 — Liste d'extraction (PA-7)

Relevé du 2026-10-13, lecture seule, clone noyau `devenv/env-6` 1551afb (= ENV-5 fusionnée).
Chemins relatifs à `scion/` du clone ; `src/…` = `scion/sys/root/src/…`. Fichiers réellement utilisés :
`ninja -t deps` des constructions de l'oracle `env-6-avant` et listes de `cmake/boards/*.cmake`.
Les tables F4 et WL fixent le découpage ; la liste fichier par fichier de ces deux lots sera
revérifiée au début de leur session.

## 1. Règles communes proposées

| # | Sujet | Proposition |
| --- | --- | --- |
| R1 | Dépôts | Un dépôt git local par greffon : `<ROOTSTOCK>/depots/lepton-famille/<nom>`, `<ROOTSTOCK>/depots/lepton-bsp/<nom>` ; `master` (commit initial vide) puis `devenv/env-6`. Contenu sous `scion/sys/root/src/<destination>/`. |
| R2 | Graine | Graine de travail, branche `devenv/env-6` : `lepton famille::<nom> * depots/lepton-famille/<nom>` et `lepton bsp::<nom> * depots/lepton-bsp/<nom>` dans `.scion.sources.list` et `.scion.ramifications` ; puis `scion seed-clone --seed depots/lepton-seed.scions/original-tree` (inscription dans `.scion.grafted.list`, aucun `git pull` ni fetch pour une version `*`) et `scion graft`. |
| R3 | Destinations | Famille : `kernel/dev/arch/cortexm/<famille>` (chemin actuel, inchangé pour F4 et WL) ; `qemu-mps2` : `kernel/dev/arch/cortexm/qemu-mps2`. BSP : `kernel/dev/bsp/<nom>` (renommage des répertoires `qemu_mps2`, `nucleo_f439zi`, `stm32wl55jci_nucleo` ; noms de fichiers conservés). |
| R4 | Fichiers de carte | Dans le BSP, relatifs à la destination (schéma) : `ld/mem_<carte>.ld` (`script_liens`), `include/user_kernel_mkconf.h` (`entete_config_noyau`), `debug/openocd-<carte>.cfg`, `debug/gdbinit-<carte>` ; démarrage de carte (`demarrage`) lié en OBJECT (`bsp_objets`). |
| R5 | Restent dans le noyau | `startup_armv7m.c`, `startup_armv6m.c`, `sbrk_cortexm.c`, `ld/common-cortexm.ld` (PA-2 Q3) ; CMSIS cœur et `Device/ARM/ARMCM*` (`kernel/core/ucore/cmsis*`, génériques) ; pilotes `kernel/dev/arch/all/*` autres que CMSDK UART et LAN9118 ; `sys/user/tauon-basic` (XML mkconf, `.boot`, `.init`) ; `cmake/{isa,cpu,kal,toolchains}`. |
| R6 | Lecteur CMake | Lecture des manifestes avant le choix de la carte ; BSP choisi par `LEPTON_BOARD` = `nom` du manifeste (sinon repli sur `cmake/boards/<carte>.cmake`, cartes transitoires) ; famille = champ `famille` du BSP ; contrôle `coeur` = `LEPTON_CPU`, `abi_flottante` = `LEPTON_FLOAT_ABI`, cœur du BSP ∈ `coeurs` de la famille ; `frequence_cpu`, `entete_config_noyau`, `script_liens`, `qemu.machine` remplacent `LEPTON_BOARD_CPU_FREQ`, `…_KERNEL_CONFIG_HEADER`, `…_MEMORY_LD`, `LEPTON_QEMU_MACHINE` ; `demarrage`, `vecteurs`, `remplacants_forts` exclus de la découverte et liés en OBJECT ; seuls la famille et le BSP choisis sont appliqués (les autres manifestes de type famille/bsp du trunk sont lus et ignorés). |
| R7 | Portée publique d'une famille ou d'un BSP | Options publiques posées sur `lepton_options` (tout l'exécutif) : elles servent au noyau (`__tauon_cpu_device__`, `STM32F429xx`…), qui ne dépend pas de la carte. |
| R8 | Historique | Déplacement : `git rm` dans le clone noyau, import dans le greffon ; message citant le commit d'origine (`<hash> du clone noyau`) ; commits mécaniques séparés des commits de fond. |
| R9 | Cartes hors périmètre | BSP hérités sans module CMake (`discovery_f4`, `discovery_f4-baseboard-modem`, `olimex_p407`, `stm32f469i-eval`, `samd20xplained_pro`, `same70xplained`, `samv71xplained_ultra`) laissés dans le noyau, non construits ; ils incluent des fichiers F4 qui partiront dans la famille (ils restent non construisibles, comme aujourd'hui). |

## 2. Lot QEMU (session 1)

### Famille `qemu-mps2` (destination `kernel/dev/arch/cortexm/qemu-mps2`, bibliothèque `kernel`)

| Origine (clone noyau) | Destination dans le greffon |
| --- | --- |
| `src/kernel/dev/arch/all/uart/dev_cmsdk_uart/dev_cmsdk_uart_x.{c,h}` | `…/qemu-mps2/uart/dev_cmsdk_uart_x.{c,h}` |
| `src/kernel/dev/arch/all/eth/dev_eth_lan9118/dev_eth_lan9118_x.{c,h}` | `…/qemu-mps2/eth/dev_eth_lan9118_x.{c,h}` |
| — | `…/qemu-mps2/lepton-greffon.json` : `sources` `uart`, `eth` ; `coeurs` cortex-m4f, cortex-m7 ; `mcu` ARMCM4, ARMCM7 |

Conséquence : les deux `#include "kernel/dev/arch/all/…"` de `qemu_mps2_board.c` changent de chemin
(seule modification de contenu de ce fichier). Seul utilisateur des deux pilotes : ce BSP.

### BSP `qemu-mps2-an386` (destination `kernel/dev/bsp/qemu-mps2-an386`)

| Origine | Destination |
| --- | --- |
| `src/kernel/dev/bsp/qemu_mps2/qemu_mps2_board.c` | `qemu_mps2_board.c` (`demarrage` : SystemInit, UART, Ethernet, IRQ) |
| `src/kernel/dev/bsp/qemu_mps2/an386/qemu_mps2_machine.h` | `qemu_mps2_machine.h` (à côté du `.c` : plus de répertoire d'inclusion) |
| `ld/mem_qemu-mps2-an386.ld` | `ld/mem_qemu-mps2-an386.ld` |
| `sys/user/tauon-basic/src/arch/qemu-mps2/kernel_mkconf/include/user_kernel_mkconf.h` | `include/user_kernel_mkconf.h` |
| `cmake/boards/qemu-mps2-an386.cmake` | supprimé : manifeste (fréquence 25 MHz, cœur, machine QEMU, `__tauon_cpu_device__` en définition publique) + `CMakeLists.txt` du BSP (Q3) |

### BSP `qemu-mps2-an500` (proposé dans le même lot, Q6)

Même découpage : copie de `qemu_mps2_board.c` et de `user_kernel_mkconf.h`, `an500/qemu_mps2_machine.h`,
`ld/mem_qemu-mps2-an500.ld`, `cmake/boards/qemu-mps2-an500.cmake` supprimé. Après le lot, plus rien de
`kernel/dev/bsp/qemu_mps2` ni de `sys/user/tauon-basic/src/arch/qemu-mps2` dans le noyau.

### Effets de bord connus

- `kernel_mkconf.h` généré par mklepton contient le chemin de l'en-tête de carte : une ligne change →
  nouvelle référence `tests/host/mklepton_empreintes.sha256` (écart démontré, comme en PA-4).
- `tests/host/mklepton_empreintes.sh` lit les triplets dans `cmake/boards/*.cmake` : à adapter (manifestes
  BSP + XML de chaque preset) ; `host.mklepton_format` cite l'en-tête QEMU : nouveau chemin.
- Binaires : le démarrage de carte passe de l'archive `bsp` à l'objet `bsp_objets` → ordre d'édition de
  liens modifié ; attendu : symboles identiques, écarts de sections = remplissage (méthode ENV-5).

## 3. Lot F4 (session suivante)

| Greffon | Contenu |
| --- | --- |
| famille `stm32f4xx` (`kernel/dev/arch/cortexm/stm32f4xx`) | tout le répertoire actuel (couche Lepton `gpio`, `uart`, `eth`, `dev_stm32f4xx/`, en-têtes ; SPL `driverlib/` ; `cubemx_hal_driver/` inutilisé) + `src/kernel/core/ucore/cmsis/Device/st/stm32f4xx` (même chemin de trunk) ; vecteurs : `nucleo_f439zi_vectors.c` (IRQ 12, 39, 57, 61) → `vecteurs/stm32f429xx_vectors.c` |
| BSP `nucleo-f429zi` (`kernel/dev/bsp/nucleo-f429zi`) | `nucleo_f439zi_board.c` (SystemInit HSE/PLL 168 MHz, GPIO, Ethernet), `nucleo_f439zi.h`, `ld/mem_nucleo-f439zi.ld`, `user_kernel_mkconf.h`, `debug/openocd-nucleo-f439zi.cfg` (`board/st_nucleo_f4.cfg`), `debug/gdbinit-…` (Q8) ; presets renommés `nucleo-f429zi-{embos,freertos}` |
| BSP `nucleo-f439zi` | Q7 |

Compilés aujourd'hui : SPL 7 `.c` sur 32 ; `dev_stm32f4xx/` 2 sur 10 (`sdio` et `sdio-1.16`, `eth` et
`cubemx_eth` définissent les mêmes symboles) ; racine 3 sur 5 → Q2.

## 4. Lot WL (session suivante)

| Greffon | Contenu |
| --- | --- |
| famille `stm32wlxx` (`kernel/dev/arch/cortexm/stm32wlxx`) | `dev_stm32wlxx/` (dont `dev_stm32wlxx_hal_tick.c` → `remplacants_forts`), `cubemx_hal_driver/`, `radio_subghz_phy/` (sauf `stm32_radio_target`, Q10), `Utilities/` + `src/kernel/core/ucore/cmsis/Device/st/stm32wlxx` ; vecteurs : IRQ 11, 12, 37, 50 aujourd'hui dans `stm32wl55jci_nucleo_system.c` → `vecteurs/stm32wl55xx_vectors.c` (séparation du fichier : à confirmer en début de lot) |
| BSP `nucleo-wl55jc1` (`kernel/dev/bsp/nucleo-wl55jc1`) | `stm32wl55jci_nucleo_system.c` (MSI 48 MHz), `stm32wl55jci_nucleo.h`, `dev_stm32wl55jci_nucleo_peripherals/`, `dev_stm32wl55jci_nucleo_radio/`, `dev_stm32wl55jci_nucleo_board/` (non compilé, conservé), `ld/mem_nucleo-wl55jc1.ld`, `user_kernel_mkconf.h`, `debug/openocd-nucleo-wl55jc1.cfg` (`target/stm32wlx.cfg`), `debug/gdbinit-…` ; ABI `soft` ; génération de la cfg OpenOCD avec `adapter serial` et test `board.radio` dans le `CMakeLists.txt` du BSP (Q3) |

Compilés aujourd'hui : HAL 12 `.c` sur 72 ; `dev_stm32wlxx/` 4 sur 5 ; `Utilities/` 1 (`stm32_mem.c`) → Q2.

## 5. Cartes transitoires (Q9)

`stm32f746g-disco` (famille `stm32f7xx`) et `samd21-xplained-pro` (famille `samd21`) : modules
`cmake/boards`, `ld/mem_*`, `debug/*` et BSP laissés dans le noyau pendant ENV-6, construits par le repli
de R6 ; le `gdbinit` commun (Q8) les concerne aussi.

## 6. Questions pour PA-7

| Q | Sujet | Constat | Proposition |
| --- | --- | --- | --- |
| Q1 | Répertoires d'inclusion | Les modules `cmake/boards` posent des `include_directories` (BSP, `driverlib`, `dev_stm32f4xx`, HAL `inc`, CMSIS device, 5 répertoires radio WL). Le schéma (`compilation`) n'a que `definitions` et `drapeaux`. | Ajouter `inclusions` à `compilation.<portée>` : chemins relatifs à `sys/root/src` (forme des `#include` de Lepton). Amendement du schéma, d'un exemple invalide et de `valider-schemas.sh`. Inutile pour QEMU (en-tête de machine à côté du `.c`). |
| Q2 | Sources partielles d'un répertoire | Pilotes tiers et couche F4 : une minorité des `.c` d'un répertoire est compilée ; plusieurs fichiers d'un même répertoire définissent les mêmes symboles. | `sources` accepte aussi un fichier (`.c`/`.S`) : un répertoire est découvert, un fichier est pris tel quel. Amendement du schéma (description) et du lecteur. Variante : champ `exclusions`. |
| Q3 | Paramètres hors schéma | Variables de test (`LEPTON_NET_TEST_*`, `LEPTON_BOARD_UNAME_MACHINE`, `LEPTON_NET_STACK`), cfg OpenOCD générée et test `board.radio` (WL), caches `LEPTON_BOARD_SERIAL_PORT`, `…_STLINK_SERIAL`. | `CMakeLists.txt` facultatif du greffon (GRF-1), à la racine de la destination, inclus par le lecteur (`include()`, variables visibles) pour le BSP choisi seulement. |
| Q4 | XML mkconf, `.boot`, `.init` | Configuration logicielle, versionnée dans la graine (CFG-1), partagée an386/an500. | Restent dans `sys/user/tauon-basic` du noyau ; choisis par une variable de preset `LEPTON_MKCONF` (dans `CMakePresets.json` jusqu'aux presets générés d'ENV-8). |
| Q5 | `user_kernel_mkconf.h` | Schéma : dans le BSP (`entete_config_noyau`) ; contient aussi des choix applicatifs (profil, FS, lwIP). | Dans le BSP, conformément au schéma (PA-3/PA-4) ; nouvelle référence d'empreintes mklepton (une ligne de `kernel_mkconf.h`). |
| Q6 | an500 | Partage `qemu_mps2_board.c` (139 l.), mkconf et en-tête avec an386. | BSP `qemu-mps2-an500` dans le lot QEMU, `qemu_mps2_board.c` et `user_kernel_mkconf.h` dupliqués. |
| Q7 | F429ZI / F439ZI | Un seul code (puce déclarée `STM32F429xx`, en-tête `stm32f439xx.h` absent de la SPL). PA-2 Q4 : deux BSP. | Lot F4 : BSP `nucleo-f429zi` (code actuel) ; BSP `nucleo-f439zi` : à décider (copie déclarant `STM32F429xx`, ou report après ENV-6). |
| Q8 | `debug/gdbinit-nucleo-f439zi` | Commandes génériques (`lepton-load`, `lepton-fault`, `lepton-stacks`) sourcées par les gdbinit WL55, F746, SAMD21. | Partie générique → noyau `debug/gdbinit-lepton` ; partie de carte dans chaque BSP (lot F4). |
| Q9 | F746, SAMD21 | Hors des trois cartes d'ENV-6 ; doivent rester construisibles (PA-2 Q5). | Transitoires dans le noyau pendant ENV-6 ; extraction ultérieure à planifier. |
| Q10 | Inclusion famille → carte | `stm32wlxx/radio_subghz_phy/stm32_radio_target/radio_board_if.h:40` inclut `kernel/dev/bsp/stm32wl55jci_nucleo/…/stm32wlxx_nucleo_radio.h`. `stm32_radio_target` est, chez ST, l'adaptation à la carte. | Déplacer `stm32_radio_target/` dans le BSP WL (pas d'inversion de dépendance ; la famille ne référence plus la carte). |
| Q11 | SVD | Aucun SVD ST dans l'arbre (seulement `cmsis-5/Device/ARM/SVD/ARMCM*.svd`). | Champ `svd` omis en ENV-6 (facultatif) ; source des SVD décidée en ENV-9. |
| Q12 | Noms de répertoires BSP | Actuels : `qemu_mps2`, `nucleo_f439zi`, `stm32wl55jci_nucleo`. | `kernel/dev/bsp/<nom du greffon>` ; inclusions `kernel/dev/bsp/nucleo_f439zi/…` des en-têtes de carte mises à jour dans les fichiers déplacés. |
