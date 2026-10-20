"""XML mklepton du projet (O5, décision du 2026-10-20) : copie dans la graine, déclaration des applications.

Le XML du projet et les fichiers qu'il copie dans le système de fichiers racine (`<file src_file>`,
ex. `.boot`, `.init`) sont versionnés dans le dépôt de la graine, sous
`project/scion/sys/user/<projet>/etc/`, et greffés par le greffon local du projet (comme
`CMakeUserPresets.json`). Le XML de référence du noyau reste un modèle, jamais modifié par lepton.

Édition textuelle : commentaires et mise en forme du XML sont conservés.
"""

import re
from pathlib import Path, PurePosixPath

from lepton.errors import LeptonError

# Déclaration d'une application (valeurs des binaires du XML de référence ; ajustables dans le XML)
BIN_ATTRS = 'stack="2048" priority="100" timeslice="1"'
BIN_BLOCK = ("bin", "bin")          # <binaries src_path dest_path> des applications (/usr/bin)

_SRC_FILE = re.compile(r'(<file\b[^>]*?\bsrc_file=")([^"]*)(")')
_BINARIES = re.compile(r"<binaries\b([^>]*)>(.*?)</binaries>", re.S)
_ATTR = re.compile(r'\b([a-z_]+)="([^"]*)"')
_INDENT = re.compile(r"^([ \t]*)<bin\b", re.M)


def project_etc(project: str) -> PurePosixPath:
    """Répertoire du XML du projet, relatif au trunk (et à `project/scion/` de la graine)."""
    return PurePosixPath("sys/user") / project / "etc"


def project_xml(project: str) -> str:
    """Chemin du XML du projet, relatif au trunk : motif `**/mkconf_*.xml` associé au XSD (CFG-7)."""
    return str(project_etc(project) / f"mkconf_{project}.xml")


def src_files(text: str) -> list[str]:
    """Chemins `src_file` des `<file>` du XML, relatifs au trunk, dans l'ordre du texte."""
    return [m.group(2) for m in _SRC_FILE.finditer(text)]


def project_copies(text: str, project: str) -> dict[str, str]:
    """`src_file` du XML de référence → copie dans le répertoire du projet (nom de base conservé) ;
    deux fichiers de même nom de base : refus (la copie écraserait l'un par l'autre)."""
    copies, seen = {}, {}
    for src in src_files(text):
        base = PurePosixPath(src).name
        if base in seen and seen[base] != src:
            raise LeptonError(f"XML : « {seen[base]} » et « {src} » ont le même nom de fichier, copie impossible "
                              f"dans {project_etc(project)}",
                              "renommer l'un des fichiers dans le XML de référence, ou copier le XML à la main")
        seen[base] = src
        copies[src] = str(project_etc(project) / base)
    return copies


def rewrite_src_files(text: str, copies: dict[str, str]) -> str:
    return _SRC_FILE.sub(lambda m: m.group(1) + copies.get(m.group(2), m.group(2)) + m.group(3), text)


def _bin_line(name: str) -> re.Pattern:
    return re.compile(r'^[ \t]*<bin\b[^>]*\bname="' + re.escape(name) + r'"[^>]*?(?:/>|>\s*</bin>)[ \t]*\n?', re.M)


def declares_bin(text: str, name: str) -> bool:
    return _bin_line(name).search(text) is not None


def add_bin(text: str, name: str) -> str | None:
    """Déclare le binaire `name` dans `<binaries src_path="bin" dest_path="bin">` (bloc créé avant
    `<files>`, sinon avant `</mklepton>`) ; None s'il est déjà déclaré (dans n'importe quel bloc)."""
    if declares_bin(text, name):
        return None
    for m in _BINARIES.finditer(text):
        attrs = dict(_ATTR.findall(m.group(1)))
        if (attrs.get("src_path"), attrs.get("dest_path")) != BIN_BLOCK:
            continue
        body = m.group(2)
        indent = _INDENT.search(body)
        line = f'{indent.group(1) if indent else "   "}<bin name="{name}" {BIN_ATTRS} />\n'
        close = m.end(2)
        if not body.endswith("\n"):
            line = "\n" + line
        return text[:close] + line + text[close:]
    block = (f"<!-- /usr/bin : applications du projet (lepton) -->\n"
             f'<binaries src_path="{BIN_BLOCK[0]}" dest_path="{BIN_BLOCK[1]}">\n'
             f'   <bin name="{name}" {BIN_ATTRS} />\n</binaries>\n\n')
    anchor = re.search(r"^[ \t]*<files\b", text, re.M) or re.search(r"^[ \t]*</mklepton>", text, re.M)
    if anchor is None:
        raise LeptonError("XML : ni <files> ni </mklepton> en début de ligne, binaire non déclaré",
                          f'déclarer <bin name="{name}" {BIN_ATTRS} /> à la main')
    return text[:anchor.start()] + block + text[anchor.start():]


def remove_bin(text: str, name: str) -> str | None:
    """Retire toute déclaration du binaire `name` ; None s'il n'est pas déclaré."""
    pattern = _bin_line(name)
    if pattern.search(text) is None:
        return None
    return pattern.sub("", text)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as e:
        raise LeptonError(f"{path} : lecture impossible ({e.strerror})", "lepton check") from e
