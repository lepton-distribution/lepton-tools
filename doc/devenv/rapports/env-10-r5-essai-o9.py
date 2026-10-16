"""O9 : attache GDB à la NUCLEO-F429ZI (sans écriture flash), gdb avec et sans Python."""
import socket, subprocess, sys, time
trunk = "/Users/cle_d_anton/lepton/trunk"
bsp = "sys/root/src/kernel/dev/bsp/nucleo-f429zi/debug"
elf = "/Users/cle_d_anton/lepton-tools-dev/essais/env-11/f429zi/build/env11f4-debug-board/lepton.elf"
gdbs = {"arm-14.2": "/Users/cle_d_anton/opt/arm-gnu-toolchain-14.2.rel1-darwin-x86_64-arm-none-eabi/bin/arm-none-eabi-gdb",
        "macports-17.2": "/opt/local/bin/arm-none-eabi-gdb"}
for label, gdb in gdbs.items():
    ocd = subprocess.Popen(["openocd", "-f", f"{bsp}/openocd-nucleo-f439zi.cfg", "-c", "adapter serial 0672FF495252717267243842"],
                           cwd=trunk, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(100):
            try:
                socket.create_connection(("localhost", 3333), timeout=0.2).close(); break
            except OSError:
                time.sleep(0.1)
        r = subprocess.run([gdb, "-nx", "-batch", "-x", f"{bsp}/gdbinit-nucleo-f439zi",
                            "-ex", "lepton-stacks", "-ex", "monitor resume", elf],
                           cwd=trunk, capture_output=True, text=True, timeout=120)
        print(f"===== {label} ({gdb}) code {r.returncode}")
        print(r.stdout[-2500:]); print("--- stderr"); print(r.stderr[-1500:])
    finally:
        ocd.terminate(); ocd.wait()
