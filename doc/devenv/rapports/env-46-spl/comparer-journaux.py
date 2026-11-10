#!/usr/bin/env python3
"""ENV-44 : compare fumee.log et banc-kal.log de deux oracles, preset par preset.

Usage : comparer-journaux.py <oracle-avant> <oracle-après> <preset>...
Banc KAL : liste (rang, nom, résultat) des tests et ligne de bilan ; durées ignorées.
Fumée : lignes de la console après normalisation. Sont ignorés : la date de compilation
(« Nov  9 2026 - 17:19:02 »), le jeton aléatoire de l'écho UART (`lepton-uart1-<n>`), les
messages asynchrones `rcv SIGCHLD` et le numéro d'invite qui les suit, les lignes vides.
"""
import re
import sys
from pathlib import Path

DATE = re.compile(r"[A-Z][a-z]{2} +\d+ \d{4} ?- ?\d{2}:\d{2}:\d{2}")


def kal(chemin: Path) -> list[str]:
    lignes = []
    for l in chemin.read_text(errors="replace").splitlines():
        m = re.match(r"\s*(\d+/\d+) Test +#\d+: (\S+) \.+\**\s*(\w+)", l)
        if m:
            lignes.append(" ".join(m.groups()))
        elif "tests passed" in l:
            lignes.append(l.strip())
    return lignes


def fumee(chemin: Path) -> list[str]:
    lignes = []
    for l in chemin.read_text(errors="replace").splitlines():
        l = DATE.sub("DATE", l)
        l = re.sub(r"lepton-uart1-\d+", "lepton-uart1-N", l)
        l = re.sub(r"^\d+(lepton#)", r"\1", l)
        if not l.strip() or l.strip() == "rcv SIGCHLD":
            continue
        lignes.append(l.rstrip())
    return lignes


def main() -> int:
    avant, apres, presets = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3:]
    ecarts = 0
    for p in presets:
        k = kal(avant / p / "banc-kal.log") == kal(apres / p / "banc-kal.log")
        f = fumee(avant / p / "fumee.log") == fumee(apres / p / "fumee.log")
        n = len(kal(apres / p / "banc-kal.log")) - 1
        print(f"{p:32} banc KAL {'identique' if k else 'DIFFÉRENT'} ({n} tests)   fumée {'identique' if f else 'DIFFÉRENTE'}")
        ecarts += (not k) + (not f)
    return 1 if ecarts else 0


if __name__ == "__main__":
    sys.exit(main())
