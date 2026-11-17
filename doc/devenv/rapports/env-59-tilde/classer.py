#!/usr/bin/env python3
"""ENV-59 : classement des origines locales par `lepton.seed.parse_location` (lecture seule, D17).

Reprend `env-55-url-file/classer.py`. Formes : `~/…`, `~<U>/…`, relative (au rootstock), absolue,
puis les deux formes `~` développées par bash (mot non cité), pour comparaison. Variantes : nue,
`@master`, `--version master`. Cibles : dépôt présent, dépôt absent. L'origine est passée telle
quelle à `parse_location`, comme un appel en liste (forme de l'extension).

Pour un refus qui porte un indice `file://localhost…`, l'indice est relu par `parse_location` et
son chemin comparé au dépôt visé (colonne `indice→dépôt`).

Usage : <python de lepton> -I classer.py <rootstock> <dépôt présent> <dépôt absent>
Répertoire courant fixé au rootstock (chemins relatifs). Sortie TSV normalisée sur stdout
(`<C>`, `<P>`, `<A>`, `<HOME>`, `~<U>`) ; rien n'est écrit sur disque.
"""
import os
import pwd
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

from lepton import seed
from lepton.errors import LeptonError

rootstock = Path(sys.argv[1]).resolve()
present, absent = sys.argv[2], sys.argv[3]
os.chdir(rootstock)
home = os.path.expanduser("~")
user = pwd.getpwuid(os.getuid()).pw_name
HINT = re.compile(r"file://localhost\S+")
UNKNOWN = "inconnu59"          # utilisateur sans compte : `expanduser()` lève RuntimeError
try:
    pwd.getpwnam(UNKNOWN)
    raise SystemExit(f"l'utilisateur {UNKNOWN} existe")
except KeyError:
    pass
VARIANTS = [("nue", "", None), ("@master", "@master", None), ("--version master", "", "master")]


def bash_word(word: str) -> str:
    """Mot développé par bash, non cité (développement du tilde compris)."""
    return subprocess.run(["bash", "-c", f"printf '%s' {word}"], capture_output=True, text=True,
                          check=True).stdout


def forms(target: str) -> list[tuple[str, str, bool]]:
    if not target.startswith(home + "/"):
        raise SystemExit(f"{target} : hors de {home}")
    under = target[len(home) + 1:]
    tilde, tilde_user = f"~/{under}", f"~{user}/{under}"
    return [("~/…", tilde, False), ("~<U>/…", tilde_user, False),
            ("relatif", os.path.relpath(target, rootstock), False), ("absolu", target, False),
            ("~/… développé", tilde, True), ("~<U>/… développé", tilde_user, True),
            ("~inconnu/…", f"~{UNKNOWN}/{under}", False)]


def normalize(text: str) -> str:
    for value, token in ((str(rootstock), "<C>"), (present, "<P>"), (absent, "<A>"), (home, "<HOME>"),
                         (f"~{user}/", "~<U>/")):
        text = text.replace(value, token)
    return text


cols = ["cible", "forme", "variante", "argument", "lepton", "location", "version", "message",
        "indice", "indice→dépôt"]
print("\t".join(cols))
for target_label, target in (("présent", present), ("absent", absent)):
    real = os.path.realpath(target)
    for form, text, developed in forms(target):
        for vlabel, suffix, version in VARIANTS:
            arg = bash_word(text + suffix) if developed else text + suffix
            row = dict.fromkeys(cols, "")
            row.update({"cible": target_label, "forme": form, "variante": vlabel, "argument": arg})
            try:
                o = seed.parse_location(arg, version, rootstock=rootstock)
                row.update({"lepton": "origine", "location": o.location, "version": o.version})
            except LeptonError as e:
                row.update({"lepton": "erreur", "message": f"{e.message} → {e.action}"})
                m = HINT.search(e.action)
                if m:
                    row["indice"] = m.group(0)
                    h = seed.parse_location(m.group(0), rootstock=rootstock)
                    path = urlparse(h.location).path
                    row["indice→dépôt"] = ("même dépôt" if path == real else f"autre : {path}") + \
                        f" ({h.version})"
            except Exception as e:   # hors LeptonError : trace Python pour l'utilisateur
                row.update({"lepton": "exception", "message": f"{type(e).__name__}: {e}"})
            print("\t".join(normalize(row[c]) for c in cols))
