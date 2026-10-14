"""Ligne de commande de lepton (interface PA-9 : doc/devenv/rapports/env-8-interface.md).

Usage :
    lepton --version
    lepton check [--json] FILE...

Codes de retour : 0 succès ; 1 utilisation, refus ou anomalie ; 2 échec ou absence d'un outil
appelé ; 130 interruption.
"""

import argparse
import json
import sys
from pathlib import Path

from lepton import __version__
from lepton.errors import EXIT_INTERRUPT, EXIT_OK, EXIT_TOOL, EXIT_USER, LeptonError
from lepton.scion_runner import scion_status_line
from lepton.validation import validate_file


class _Parser(argparse.ArgumentParser):
    """Erreur d'utilisation : code 1 (argparse rend 2, réservé aux outils appelés)."""

    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(EXIT_USER, f"lepton: erreur: {message}\n  → {self.prog} --help\n")


class _VersionAction(argparse.Action):
    """INS-6 : version de lepton et de scion ; code 0 même si scion manque (diagnostic)."""

    def __init__(self, option_strings, dest, **kwargs):
        super().__init__(option_strings, dest, nargs=0, help="affiche les versions de lepton et de scion")

    def __call__(self, parser, namespace, values, option_string=None):
        print(f"lepton {__version__}")
        print(scion_status_line())
        parser.exit(EXIT_OK)


def _warn(message: str) -> None:
    print(f"lepton: attention: {message}", file=sys.stderr)


def cmd_check(args) -> int:
    anomalies, checked = [], []
    for name in args.files:
        path = Path(name)
        try:
            found = validate_file(path)
        except LeptonError as e:
            if e.code != EXIT_TOOL:
                raise
            _warn(f"{path} : {e.message}" + (f" ({e.action})" if e.action else ""))
            continue
        checked.append(str(path))
        anomalies.extend(found)
    if args.json:
        json.dump({"files": checked, "anomalies": [a.as_dict() for a in anomalies]},
                  sys.stdout, ensure_ascii=False, indent=2)
        print()
    else:
        for a in anomalies:
            print(a)
        if not anomalies:
            print(f"{len(checked)} fichier(s) conforme(s).")
    return EXIT_USER if anomalies else EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    parser = _Parser(prog="lepton",
                     description="Environnement de développement Lepton : graine, greffons, fichiers, vérification.")
    parser.add_argument("--version", action=_VersionAction)
    parser.add_argument("-v", "--verbose", action="store_true", help="affiche les commandes externes exécutées")
    parser.add_argument("-C", "--rootstock", metavar="DIR", help="rootstock (défaut : recherche en remontant)")
    sub = parser.add_subparsers(dest="command", metavar="COMMAND", parser_class=_Parser)

    p = sub.add_parser("check", help="valide des manifestes (JSON Schema, XSD mklepton)")
    p.add_argument("--json", action="store_true", help="sortie JSON")
    p.add_argument("files", nargs="+", metavar="FILE",
                   help="lepton-greffon.json, lepton-graine.json (ou $schema renseigné), XML mklepton")
    p.set_defaults(func=cmd_check)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        if args.command is None:
            parser.print_help(sys.stderr)
            return EXIT_USER
        return args.func(args)
    except LeptonError as e:
        print(f"lepton: erreur: {e.message}", file=sys.stderr)
        if e.action:
            print(f"  → {e.action}", file=sys.stderr)
        return e.code
    except KeyboardInterrupt:
        print("lepton: interrompu", file=sys.stderr)
        return EXIT_INTERRUPT
