"""Reconfiguration CMake après changement de la liste des greffons ou d'un manifeste (GRA-4)."""

from pathlib import Path

from lepton.rootstock import Rootstock
from lepton.scion_runner import run


def build_dirs(rootstock: Rootstock) -> list[Path]:
    """Répertoires `<ROOTSTOCK>/build/*` dont le cache CMake désigne le trunk comme source."""
    found = []
    if not rootstock.build.is_dir():
        return found
    for cache in sorted(rootstock.build.glob("*/CMakeCache.txt")):
        for line in cache.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("CMAKE_HOME_DIRECTORY:"):
                home = line.partition("=")[2].strip()
                if home and Path(home).resolve() == rootstock.trunk.resolve():
                    found.append(cache.parent)
                break
    return found


def reconfigure(rootstock: Rootstock) -> list[Path]:
    """`cmake -S <trunk> -B <rép>` pour chaque répertoire de construction du trunk."""
    dirs = build_dirs(rootstock)
    for d in dirs:
        run(["cmake", "-S", str(rootstock.trunk), "-B", str(d)])
    return dirs
