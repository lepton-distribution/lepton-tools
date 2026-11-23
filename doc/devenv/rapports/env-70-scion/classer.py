#!/usr/bin/env python3
"""ENV-70 : classe les lignes du stderr des appels git en échec (audit de D35).

Usage : classer.py <sortie.tsv> <base> <journal.jsonl>…

Chaque journal vient de bin/git. Pour chaque appel de code non nul : arguments (chemins de
<base> et du HOME normalisés, empreintes de 40 caractères remplacées), code, suite des classes de
ses lignes non vides, première ligne non vide (règle de 0.6.3.3) et première ligne `fatal:` ou
`error:` (règle proposée), et si elles diffèrent.

Classes, en anglais (LC_ALL=C) et en français (po/fr.po v2.47.3, U+00A0 avant le deux-points) :
F fatal, E error, W warning, H hint, U usage, R remote (ligne de l'autre côté), - autre.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

NBSP = "\u00a0"
PREFIXES = [
    ("F", ("fatal: ", f"fatal{NBSP}: ")),
    ("E", ("error: ", f"erreur{NBSP}: ")),
    ("W", ("warning: ", f"avertissement{NBSP}: ")),
    ("H", ("hint:", f"astuce{NBSP}:")),
    ("U", ("usage: ", f"usage{NBSP}: ")),
    ("R", ("remote: ",)),  # non traduit dans fr.po v2.47.3
]
SHA = re.compile(r"\b[0-9a-f]{40}\b")


def klass(line: str) -> str:
    for k, forms in PREFIXES:
        if line.startswith(forms):
            return k
    return "-"


def main() -> None:
    out, base, logs = Path(sys.argv[1]), str(Path(sys.argv[2]).resolve()), sys.argv[3:]
    home = str(Path.home())

    def norm(text: str) -> str:
        return SHA.sub("<sha>", text.replace(base, "<B>").replace(home, "<HOME>"))

    rows = ["journal\tn°\tcommande\tcode\tclasses\tpremière ligne\tpremière F/E\tdiffère"]
    total = differ = 0
    for log in logs:
        name = Path(log).parent.name
        for i, raw in enumerate(Path(log).read_text().splitlines(), 1):
            call = json.loads(raw)
            if call["code"] == 0:
                continue
            total += 1
            lines = [l.strip() for l in call["stderr"].splitlines() if l.strip()]
            classes = " ".join(klass(l) for l in lines) or "(vide)"
            first = lines[0] if lines else ""
            cause = next((l for l in lines if klass(l) in "FE"), "")
            diff = "oui" if cause and cause != first else ""
            differ += bool(diff)
            git = "" if call["git"] == "/usr/bin/git" else f"[{call['git']}] "
            rows.append("\t".join([name, str(i), norm(git + "git " + " ".join(call["args"])),
                                   str(call["code"]), classes, norm(first)[:160],
                                   norm(cause)[:160], diff]))
    out.write_text("\n".join(rows) + "\n")
    print(f"{total} appel(s) en échec, {differ} où la première ligne n'est pas la cause F/E")


if __name__ == "__main__":
    main()
