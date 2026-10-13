# ENV-2 — Scripts et bancs existants

Relevé du 2026-10-13, lecture seule, clone noyau `master` 6b62af5. Chemins relatifs au clone (racine `master/`, sauf mention `scion/`) ;
`$LEPTON_BUILD` = `<ROOTSTOCK>/build`.

## 1. Scripts d'installation (`scripts/`)

| Script | Installe | Usage |
| --- | --- | --- |
| `scripts/install-macos.sh` (238 l. ; Mac Intel visé, Apple Silicon non validé, l. 3-4) | MacPorts par défaut sur Intel (l. 63-69) : cmake, ninja, python313, pipx ; scion 0.5.0.1 par pipx (l. 124-131) ; cloc, doxygen, graphviz, coccinelle facultatifs ; `qemu +target_arm` (l. 149) ; Arm GNU Toolchain 14.2.Rel1 dans `~/opt`, SHA-256 vérifié (l. 155-173). `--with-debug-tools` : `openocd +ftdi +cmsis`, texinfo, `arm-none-eabi-gdb +python313`, lien `~/.local/bin/gdb-multiarch` (l. 184-204). | `./install-macos.sh [--with-debug-tools] [--toolchain-dir <dir>] [--pkg-manager macports\|brew]` ; n'édite pas le shell (affiche la ligne `PATH`, l. 232-233) ; embOS copié à la main (l. 235-236) |
| `scripts/install-debian.sh` (126 l.) | build-essential, gdb, clang, cmake, ninja, python3, pipx, libexpat1-dev ; scion 0.5.0.1 ; cloc, coccinelle ; gcc-arm-none-eabi, libnewlib, gdb-multiarch ; qemu-system-arm, iproute2, iputils-ping ; doxygen, graphviz. `--with-debug-tools` : openocd + rappel udev (l. 101-107) ; `--with-riscv`. | `./install-debian.sh [--with-debug-tools] [--with-riscv]` (`doc/BUILDING.md:28`) |

## 2. Environnement

| Script | Rôle |
| --- | --- |
| `scripts/lepton-env.sh` (44 l., à sourcer) | Remonte jusqu'à `.scion.rootstock.signature` ; exporte `LEPTON_ROOTSTOCK`, `LEPTON_TRUNK`, `LEPTON_CLONE` (`<root>/depots/lepton/original/master`), `LEPTON_BUILD` (`<root>/build`), `LEPTON_EMBOS_ROOT` (défaut `<root>/third_party/embos/cortexm-gcc/5.20.0.0`, l. 35-38), lu par le preset `cross` (`scion/CMakePresets.json:36`) |
| `scripts/claude-lepton.sh` (14 l.) | Lance `claude … --add-dir $LEPTON_TRUNK $LEPTON_BUILD` depuis le clone |

## 3. Presets et produits

Répertoire de construction : `${sourceDir}/../build/<preset>` (`scion/CMakePresets.json:13`), soit
`$LEPTON_BUILD/<preset>/`. Le preset `host` (mklepton hôte, `$LEPTON_BUILD/host/mklepton`) est
prérequis de tous les presets croisés (`CMakePresets.json:37`).
Produits par preset (`scion/cmake/components/firmware.cmake:66-86`) : `lepton.elf`, `lepton.bin`,
`lepton.map`, `kal_bench.map`, `tests/kal/kal_bench.elf`. Aucun `.hex`.

| Cible | Presets | Exécutable |
| --- | --- | --- |
| QEMU mps2-an386 | `qemu-mps2-an386-embos`, `-embos-soft`, `-freertos`, `-freertos-soft` | `$LEPTON_BUILD/<preset>/lepton.elf` |
| NUCLEO-F429ZI | `nucleo-f439zi-embos`, `nucleo-f439zi-freertos` | idem ; cible `flash` |
| NUCLEO-WL55JC1 | `nucleo-wl55jc1-embos`, `nucleo-wl55jc1-freertos` | idem ; + `openocd-nucleo-wl55jc1{,-paire}.cfg` générés |

## 4. Test de fumée QEMU

- Script : `scion/tests/smoke_lsh.py` (213 l.). Commande QEMU (l. 143-144) :
  ```
  qemu-system-arm -M mps2-an386 -kernel <lepton.elf> -nographic -monitor none -serial stdio -serial file:<tmp>/uart1.log
  ```
- Invite : `any key to continue` (initd) ou regex `lepton#\d+\$ ` (l. 29, 163). Contrôles : `uname -a`
  contient `cortexM4-qemu-mps2-an386` (`scion/cmake/boards/qemu-mps2-an386.cmake:18`), `ls`, `ps`,
  écho vers `/dev/ttys1` retrouvé sur UART1 ; délais 30 s au démarrage, 10 s par commande.
- ctest (`firmware.cmake:131-143`) : test `smoke.lsh`, labels `smoke;kal;arch:…;backend:…`,
  TIMEOUT 120, fixture `kal_t0`.
- Lancement : `PYTHONDONTWRITEBYTECODE=1 ctest --preset qemu-mps2-an386-embos -L smoke`
  (`doc/BUILDING.md:66` ; variable : `CLAUDE.md:75`).
- QEMU : `/opt/local/bin/qemu-system-arm` 11.1.2 (macOS), 10.0.13 (Debian).

## 5. Banc KAL

- Spécification : `doc/migration/BANC-TEST-KAL-QEMU.md` (critères l. 61-67).
- Implémentation : `scion/tests/kal/CMakeLists.txt`, exécutable `kal_bench`. Commande QEMU (l. 44-45) :
  ```
  qemu-system-arm -M <machine> -kernel tests/kal/kal_bench.elf -nographic -monitor none -serial null -semihosting-config enable=on,target=native,arg=kal_bench,arg=<T>
  ```
- Tests (l. 41) : T1-T8, T1F/T4F/T6F/T7F (ABI hard), TICI, TCLK, TSBRK, IRQ ; `kal.harness_fail`
  (WILL_FAIL). 20 s par test sous QEMU, 60 s sur carte ; fixture `kal_t0` (fumée).
- Lancement : `ctest --preset <preset-qemu> -L kal` (`ci/run.sh:111-113`) ; 18 tests en hard,
  14 en soft. Sur carte : `ctest --preset <carte> -L board`.
- Durées (journaux hors clone `$LEPTON_BUILD/etape9-ci-run.log`, `etape10-f429-*-ctest*.log`) :
  `-L kal` 4,7-5,5 s par preset ; `-L smoke` ~3,4 s ; `-L board` F429 50-55 s.

## 6. CI et autres bancs

| Élément | Rôle |
| --- | --- |
| `ci/run.sh` (135 l.) | Non-régression : outils, `host` (gcc, clang), 6 presets QEMU (smoke, net sauf Darwin, kal), build seul des 8 presets carte ; `$LEPTON_BUILD/ci/memoire.csv`, `ci/artefacts/<preset>/` ; `--no-kal` ; binaires reproductibles avec `SOURCE_DATE_EPOCH` |
| `ci/memoire.py`, `ci/Dockerfile` | Seuil mémoire ; conteneur jamais construit (`CLAUDE.md:215`) |
| `scion/tests/endurance_board.py`, `board_net.py`, `board_radio.py`, `net_qemu.py` (tap, Linux) | Bancs carte et réseau |
