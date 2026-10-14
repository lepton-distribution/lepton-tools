"""Appels de scion par sous-processus (jamais d'importation de ses modules, ENV-8)."""

import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

from lepton import SCION_MIN_VERSION
from lepton.errors import EXIT_TOOL, LeptonError

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


# Affichage des commandes externes exécutées (option -v), positionné par la ligne de commande
VERBOSE = False


def run(cmd: list[str], cwd: Path | None = None, tool: str | None = None,
        check: bool = True) -> subprocess.CompletedProcess:
    """Exécute un outil externe (liste d'arguments) ; absence, ou échec si `check` → LeptonError code 2."""
    tool = tool or cmd[0]
    exe = shutil.which(cmd[0])
    if exe is None:
        raise LeptonError(f"{tool} absent", f"installer {tool} et vérifier le PATH", EXIT_TOOL)
    if VERBOSE:
        print(f"lepton: exécute : {shlex.join(cmd)}" + (f"  (dans {cwd})" if cwd else ""), file=sys.stderr)
    res = subprocess.run([exe, *cmd[1:]], cwd=cwd, capture_output=True, text=True, check=False)
    if check and res.returncode != 0:
        detail = (res.stderr or res.stdout).strip()
        raise LeptonError(f"échec de « {shlex.join(cmd)} » (code {res.returncode})"
                          + (f" :\n{detail}" if detail else ""),
                          f"corriger la cause signalée par {tool}, puis relancer", EXIT_TOOL)
    return res


def require_scion() -> None:
    """scion présent et de version suffisante (≥ SCION_MIN_VERSION), sinon code 2."""
    v = scion_version()
    requis = format_version(SCION_MIN_VERSION)
    if v is None or v < SCION_MIN_VERSION:
        etat = "absent" if v is None else f"en version {format_version(v)}"
        raise LeptonError(f"scion {etat} (requis ≥ {requis})",
                          f"pipx install --force 'git+<dépôt seed.scions>@{requis}'", EXIT_TOOL)


def scion(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    """Appel de scion par sous-processus (version contrôlée une fois par processus)."""
    global _SCION_CHECKED
    if not _SCION_CHECKED:
        require_scion()
        _SCION_CHECKED = True
    return run(["scion", *args], cwd=cwd)


_SCION_CHECKED = False


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return run(["git", "-C", str(repo), *args])
