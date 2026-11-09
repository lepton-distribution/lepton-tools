#!/usr/bin/env python3
"""D5 d'ENV-44 : compare l'objet qemu_mps2_board.c compilé avec l'ancien en-tête ARMCM4 (V1.05)
et avec le nouveau (ARMCM4_FP.h CMSIS 5), pour chacun des 4 presets an386.

Usage : d5-objet.py <ROOTSTOCK> <répertoire-de-travail>
Lecture seule sur le rootstock : la copie de la source et de l'en-tête « ancien » est faite dans le
répertoire de travail (l'en-tête cité entre guillemets est cherché d'abord à côté de la source).
Compare les sections chargées (.text*, .rodata*, .data*, .bss*) octet pour octet et le
désassemblage ; écrit <travail>/<preset>.txt. Code 0 si identiques partout, 1 sinon.
"""
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

ANCIEN = '#include "kernel/core/ucore/cmsis/Device/ARM/ARMCM4/Include/ARMCM4.h"'
PRESETS = ["qemu-mps2-an386-embos", "qemu-mps2-an386-embos-soft", "qemu-mps2-an386-freertos",
           "qemu-mps2-an386-freertos-soft"]


def compiler(entree: dict, source: Path, sortie: Path) -> None:
    args = shlex.split(entree["command"])
    i = args.index("-o")
    args[i + 1] = str(sortie)
    args = [str(source) if a == entree["file"] else a for a in args]
    subprocess.run(args, cwd=entree["directory"], check=True, capture_output=True, text=True)


def sections(obj: Path) -> dict[str, bytes]:
    texte = subprocess.run(["arm-none-eabi-objdump", "-h", str(obj)], capture_output=True, text=True,
                           check=True).stdout
    noms = [m.group(1) for m in re.finditer(r"^\s*\d+\s+(\S+)", texte, re.M)
            if re.match(r"\.(text|rodata|data|bss)", m.group(1))]
    resultat = {}
    for n in noms:
        tmp = obj.with_suffix(f".{n.strip('.')}.bin")
        subprocess.run(["arm-none-eabi-objcopy", "-O", "binary", f"--only-section={n}", str(obj), str(tmp)],
                       check=True)
        resultat[n] = tmp.read_bytes()
    return resultat


def desassemble(obj: Path) -> str:
    sortie = subprocess.run(["arm-none-eabi-objdump", "-d", "-r", str(obj)], capture_output=True, text=True,
                            check=True).stdout
    return "\n".join(sortie.splitlines()[2:])  # sans la ligne du nom de fichier


def main() -> int:
    rootstock, travail = Path(sys.argv[1]), Path(sys.argv[2])
    travail.mkdir(parents=True, exist_ok=True)
    ecarts = 0
    for p in PRESETS:
        cc = json.loads((rootstock / "build" / p / "compile_commands.json").read_text())
        entree = next(e for e in cc if e["file"].endswith("qemu-mps2-an386/qemu_mps2_board.c"))
        src = Path(entree["file"])
        d = travail / p
        (d / "ancien").mkdir(parents=True, exist_ok=True)
        (d / "ancien" / src.name).write_text(src.read_text())
        machine = (src.parent / "qemu_mps2_machine.h").read_text()
        ligne = next(l for l in machine.splitlines() if l.startswith("#include"))
        (d / "ancien" / "qemu_mps2_machine.h").write_text(machine.replace(ligne, ANCIEN))
        compiler(entree, d / "ancien" / src.name, d / "ancien.o")
        compiler(entree, src, d / "nouveau.o")
        sa, sn = sections(d / "ancien.o"), sections(d / "nouveau.o")
        da, dn = desassemble(d / "ancien.o"), desassemble(d / "nouveau.o")
        lignes = [f"en-tête ancien : {ANCIEN}", f"en-tête nouveau : {ligne}"]
        for n in sorted(set(sa) | set(sn)):
            egal = sa.get(n) == sn.get(n)
            lignes.append(f"{n:24} {len(sa.get(n, b'')):6} -> {len(sn.get(n, b'')):6} {'identique' if egal else 'DIFFÉRENT'}")
            ecarts += 0 if egal else 1
        lignes.append(f"désassemblage : {'identique' if da == dn else 'DIFFÉRENT'}")
        ecarts += 0 if da == dn else 1
        (travail / f"{p}.txt").write_text("\n".join(lignes) + "\n")
        print(p, "identique" if ecarts == 0 else f"{ecarts} écart(s) cumulés")
    return 1 if ecarts else 0


if __name__ == "__main__":
    sys.exit(main())
