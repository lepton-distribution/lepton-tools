"""Appels de scion par sous-processus (jamais d'importation de ses modules, ENV-8)."""

import re
import shutil
import subprocess

from lepton import SCION_MIN_VERSION

_VERSION = re.compile(r"scion version:\s*(\d+(?:\.\d+)*)")


def scion_version() -> tuple[int, ...] | None:
    """Version de scion installée, ou None si scion est absent ou muet."""
    exe = shutil.which("scion")
    if exe is None:
        return None
    try:
        res = subprocess.run([exe, "version"], capture_output=True, text=True, check=False)
    except OSError:
        return None
    m = _VERSION.search(res.stdout + res.stderr)
    if res.returncode != 0 or m is None:
        return None
    return tuple(int(x) for x in m.group(1).split("."))


def format_version(v: tuple[int, ...]) -> str:
    return ".".join(str(x) for x in v)


def scion_status_line() -> str:
    """Ligne « scion … » de lepton --version (INS-6)."""
    requis = format_version(SCION_MIN_VERSION)
    v = scion_version()
    if v is None:
        return f"scion absent (requis ≥ {requis})"
    etat = "" if v >= SCION_MIN_VERSION else " — trop ancien"
    return f"scion {format_version(v)} (requis ≥ {requis}){etat}"
