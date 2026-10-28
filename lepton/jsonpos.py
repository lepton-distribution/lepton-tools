"""Positions dans un texte JSON par pointeur (CFG-7, ENV-12 lot 4) : diagnostics de l'éditeur.

Le texte est d'abord accepté par `json.loads` ; l'analyse ne relève que les portées des clés et des
valeurs. Positions : (ligne, colonne) comptées à partir de 1, colonne en caractères ; fin exclue.
"""

import json
from dataclasses import dataclass

_WS = " \t\n\r"


@dataclass(frozen=True)
class Span:
    start: int                    # indices dans le texte, fin exclue
    end: int


@dataclass(frozen=True)
class Member:
    value: Span
    key: Span | None              # absente pour la racine et les éléments de liste
    container: bool               # objet ou liste : portée réduite à la clé ou au crochet ouvrant


def _escape(token: str) -> str:
    return token.replace("~", "~0").replace("/", "~1")


class _Scanner:
    def __init__(self, text: str):
        self.text, self.i, self.found = text, 0, {}

    def ws(self) -> None:
        while self.i < len(self.text) and self.text[self.i] in _WS:
            self.i += 1

    def string(self) -> str:
        start = self.i
        self.i += 1
        while self.text[self.i] != '"':
            self.i += 2 if self.text[self.i] == "\\" else 1
        self.i += 1
        return json.loads(self.text[start:self.i])

    def value(self, pointer: str, key: Span | None) -> None:
        self.ws()
        start, c = self.i, self.text[self.i]
        if c == "{":
            self.i += 1
            self.ws()
            while self.text[self.i] != "}":
                k_start = self.i
                name = self.string()
                k_span = Span(k_start, self.i)
                self.ws()
                self.i += 1                     # :
                self.value(f"{pointer}/{_escape(name)}", k_span)
                self.ws()
                if self.text[self.i] == ",":
                    self.i += 1
                    self.ws()
            self.i += 1
        elif c == "[":
            self.i += 1
            self.ws()
            n = 0
            while self.text[self.i] != "]":
                self.value(f"{pointer}/{n}", None)
                n += 1
                self.ws()
                if self.text[self.i] == ",":
                    self.i += 1
                    self.ws()
            self.i += 1
        elif c == '"':
            self.string()
        else:
            while self.i < len(self.text) and self.text[self.i] not in _WS + ",]}":
                self.i += 1
        self.found[pointer] = Member(Span(start, self.i), key, c in "{[")


def members(text: str) -> dict[str, Member]:
    """Pointeur JSON (« » pour la racine) → portées ; texte déjà reconnu comme JSON valide."""
    scanner = _Scanner(text)
    scanner.value("", None)
    return scanner.found


def line_col(text: str, index: int) -> tuple[int, int]:
    line = text.count("\n", 0, index) + 1
    return line, index - (text.rfind("\n", 0, index) + 1) + 1


def span_of(found: dict[str, Member], pointer: str, on_key: bool = False) -> Span | None:
    """Portée d'un pointeur : la clé si `on_key` ou si la valeur est un objet ou une liste (crochet
    ouvrant à défaut de clé), la valeur sinon ; pointeur absent : plus proche ancêtre présent."""
    pointer = "" if pointer == "/" else pointer
    while pointer not in found and pointer:
        pointer = pointer.rsplit("/", 1)[0]
    m = found.get(pointer)
    if m is None:
        return None
    if (on_key or m.container) and m.key is not None:
        return m.key
    if m.container:
        return Span(m.value.start, m.value.start + 1)
    return m.value
