"""Ligne de commande de lepton (interface PA-9 : doc/devenv/rapports/env-8-interface.md).

Usage :
    lepton --version
    lepton check [--json] FILE...
    lepton seed new NAME --bsp BSP --mkconf PATH [--backend B] [--seed-repo DIR] [--origin S=L]...
    lepton seed status [--json]
    lepton seed add SCION LOCATION --type T [--version V] [--path P] [--no-cmake]
    lepton seed remove SCION [--purge] [--no-cmake]
    lepton seed replace SCION LOCATION [--version V] [--path P] [--no-cmake]

Codes de retour : 0 succès ; 1 utilisation, refus ou anomalie ; 2 échec ou absence d'un outil
appelé ; 130 interruption.
"""

import argparse
import json
import sys
from pathlib import Path

from lepton import __version__, scion_runner, seed
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


def _common_options() -> argparse.ArgumentParser:
    """-v et -C acceptés avant ou après la sous-commande (SUPPRESS : la valeur globale est gardée)."""
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("-v", "--verbose", action="store_true", default=argparse.SUPPRESS,
                        help="affiche les commandes externes exécutées")
    common.add_argument("-C", "--rootstock", metavar="DIR", default=argparse.SUPPRESS,
                        help="rootstock (défaut : recherche en remontant ; seed new : répertoire à créer)")
    return common


def _no_cmake(p) -> None:
    p.add_argument("--no-cmake", action="store_true", help="ne pas reconfigurer les répertoires build/*")


def _origin_options(p) -> None:
    p.add_argument("--version", metavar="V", help="branche ou tag d'une URL (défaut : master)")
    p.add_argument("--path", metavar="P", help="chemin du greffon dans le dépôt")


def _add_seed_parser(sub, common) -> None:
    seed_p = sub.add_parser("seed", help="graine du projet (GRA)", parents=[common])
    seed_sub = seed_p.add_subparsers(dest="seed_command", metavar="ACTION", parser_class=_Parser, required=True)

    p = seed_sub.add_parser("new", parents=[common], help="crée un rootstock greffé depuis une graine neuve (GRA-1)")
    p.add_argument("name", metavar="NAME", help="nom du projet")
    p.add_argument("--bsp", required=True, metavar="BSP", help="greffon BSP de la carte")
    p.add_argument("--mkconf", required=True, metavar="PATH", help="XML mklepton, chemin relatif au trunk")
    p.add_argument("--backend", default="embos", choices=["embos", "freertos"], help="backend (défaut : embos)")
    p.add_argument("--seed-repo", metavar="DIR", help="dépôt git de la graine (défaut : depots/lepton-seed/NAME)")
    p.add_argument("--origin", action="append", metavar="SCION=LOCATION[@VERSION][:PATH]",
                   help="origine d'un greffon (BSP et famille obligatoires ; noyau : lepton-noyau, "
                        f"défaut {seed.DEFAULT_KERNEL_ORIGIN})")
    p.set_defaults(func=seed.seed_new)

    p = seed_sub.add_parser("status", parents=[common], help="état des greffons de la graine (GRA-6)")
    p.add_argument("--json", action="store_true", help="sortie JSON")
    p.set_defaults(func=seed.seed_status)

    p = seed_sub.add_parser("add", parents=[common], help="ajoute un greffon à la graine (GRA-4)")
    p.add_argument("scion", metavar="SCION", help="nom du greffon (champ nom de son manifeste)")
    p.add_argument("location", metavar="LOCATION", help="URL git[@VERSION][:PATH] ou répertoire local")
    p.add_argument("--type", required=True, choices=["famille", "bsp", "application", "bibliotheque"])
    _origin_options(p)
    _no_cmake(p)
    p.set_defaults(func=seed.seed_add)

    p = seed_sub.add_parser("remove", parents=[common], help="retire un greffon de la graine (GRA-4)")
    p.add_argument("scion", metavar="SCION")
    p.add_argument("--purge", action="store_true", help="supprime aussi le clone fait par scion (propre, poussé)")
    _no_cmake(p)
    p.set_defaults(func=seed.seed_remove)

    p = seed_sub.add_parser("replace", parents=[common], help="change l'origine ou la version d'un greffon (GRA-4)")
    p.add_argument("scion", metavar="SCION")
    p.add_argument("location", metavar="LOCATION")
    _origin_options(p)
    _no_cmake(p)
    p.set_defaults(func=seed.seed_replace)


def build_parser() -> argparse.ArgumentParser:
    parser = _Parser(prog="lepton",
                     description="Environnement de développement Lepton : graine, greffons, fichiers, vérification.")
    parser.add_argument("--version", action=_VersionAction)
    parser.add_argument("-v", "--verbose", action="store_true", help="affiche les commandes externes exécutées")
    parser.add_argument("-C", "--rootstock", metavar="DIR", help="rootstock (défaut : recherche en remontant)")
    sub = parser.add_subparsers(dest="command", metavar="COMMAND", parser_class=_Parser)
    common = _common_options()
    _add_seed_parser(sub, common)

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
        scion_runner.VERBOSE = args.verbose
        return args.func(args)
    except LeptonError as e:
        print(f"lepton: erreur: {e.message}", file=sys.stderr)
        if e.action:
            print(f"  → {e.action}", file=sys.stderr)
        return e.code
    except KeyboardInterrupt:
        print("lepton: interrompu", file=sys.stderr)
        return EXIT_INTERRUPT
