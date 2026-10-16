"""Ligne de commande de lepton (interface PA-9 : doc/devenv/rapports/env-8-interface.md).

Usage :
    lepton --version
    lepton check [--json] [FILE...]
    lepton seed new NAME --bsp BSP --mkconf PATH [--backend B] [--seed-repo DIR] [--origin S=L]...
    lepton seed status [--json]
    lepton seed lock [--verify | --restore] [--no-cmake]
    lepton seed add SCION LOCATION --type T [--version V] [--path P] [--no-cmake]
    lepton seed remove SCION [--purge] [--no-cmake]
    lepton seed replace SCION LOCATION [--version V] [--path P] [--no-cmake]
    lepton scion new NAME --type T [--from BSP] [--repo DIR] [--destination D] [--no-seed] [--no-cmake]
    lepton scion remove NAME [--no-cmake]
    lepton file add PATH [--scion NAME] | file remove PATH | file mv SOURCE DESTINATION
    lepton dir add PATH [--scion NAME] | dir remove PATH [--scion NAME]
    lepton graft [--scion NAME]... [--force] [--no-cmake]
    lepton generate [--clangd PATH] [--probe-serial SERIAL]

Codes de retour : 0 succès ; 1 utilisation, refus ou anomalie ; 2 échec ou absence d'un outil
appelé ; 130 interruption.
"""

import argparse
import json
import sys
from pathlib import Path

from lepton import __version__, checks, files, generate, scion_runner, scions, seed
from lepton.errors import EXIT_INTERRUPT, EXIT_OK, EXIT_TOOL, EXIT_USER, LeptonError
from lepton.rootstock import Rootstock
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
    """FILE... : manifestes isolés (jalon 1) ; sans argument : rootstock entier (jalon 6, §3.9)."""
    anomalies, checked = [], []
    if not args.files:
        checked, anomalies = checks.check_rootstock(Rootstock.discover(args.rootstock), _warn)
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

    p = seed_sub.add_parser("lock", parents=[common], help="fige le commit de chaque greffon (GRA-5)")
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--verify", action="store_true", help="compare les clones au verrou (code 1 si écart)")
    mode.add_argument("--restore", action="store_true",
                      help="remet les clones d'origine distante au commit du verrou, puis regreffe")
    _no_cmake(p)
    p.set_defaults(func=seed.seed_lock)

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


def _add_scion_parser(sub, common) -> None:
    scion_p = sub.add_parser("scion", help="greffons du projet (GRF)", parents=[common])
    scion_sub = scion_p.add_subparsers(dest="scion_command", metavar="ACTION", parser_class=_Parser, required=True)

    p = scion_sub.add_parser("new", parents=[common], help="crée un greffon et l'ajoute à la graine (GRF-1)")
    p.add_argument("name", metavar="NAME", help="nom du greffon")
    p.add_argument("--type", required=True, choices=["bsp", "application", "bibliotheque"])
    p.add_argument("--from", dest="from_bsp", metavar="BSP", help="BSP greffé à copier (obligatoire pour un BSP)")
    p.add_argument("--repo", metavar="DIR", help="dépôt git à créer (défaut : depots/lepton-<kind>/NAME)")
    p.add_argument("--destination", metavar="D",
                   help="chemin sous sys/root/src (défaut : kernel/dev/bsp/NAME, bin/NAME, lib/NAME)")
    p.add_argument("--no-seed", action="store_true", help="créer le dépôt sans l'ajouter à la graine")
    _no_cmake(p)
    p.set_defaults(func=scions.scion_new)

    p = scion_sub.add_parser("remove", parents=[common], help="retire un greffon, dépôt conservé (GRF-4)")
    p.add_argument("scion", metavar="NAME")
    _no_cmake(p)
    p.set_defaults(func=scions.scion_remove)


def _add_files_parsers(sub, common) -> None:
    owner_help = "greffon propriétaire (défaut : celui des feuilles du répertoire)"
    file_p = sub.add_parser("file", help="fichiers des greffons (FIC)", parents=[common])
    file_sub = file_p.add_subparsers(dest="file_command", metavar="ACTION", parser_class=_Parser, required=True)
    p = file_sub.add_parser("add", parents=[common], help="crée un fichier vide dans le clone propriétaire (FIC-1)")
    p.add_argument("path", metavar="PATH", help="chemin du trunk ou d'un clone")
    p.add_argument("--scion", metavar="NAME", help=owner_help)
    p.set_defaults(func=files.file_add)
    p = file_sub.add_parser("remove", parents=[common], help="retire un fichier de son clone (FIC-1)")
    p.add_argument("path", metavar="PATH")
    p.set_defaults(func=files.file_remove)
    p = file_sub.add_parser("mv", parents=[common], help="déplace un fichier dans son clone (FIC-6)")
    p.add_argument("source", metavar="SOURCE")
    p.add_argument("destination", metavar="DESTINATION")
    p.set_defaults(func=files.file_mv)

    dir_p = sub.add_parser("dir", help="répertoires des greffons (FIC)", parents=[common])
    dir_sub = dir_p.add_subparsers(dest="dir_command", metavar="ACTION", parser_class=_Parser, required=True)
    p = dir_sub.add_parser("add", parents=[common], help="crée un répertoire (avec .gitkeep) dans le clone (FIC-2)")
    p.add_argument("path", metavar="PATH")
    p.add_argument("--scion", metavar="NAME", help=owner_help)
    p.set_defaults(func=files.dir_add)
    p = dir_sub.add_parser("remove", parents=[common], help="retire la part d'un greffon dans un répertoire (FIC-2)")
    p.add_argument("path", metavar="PATH")
    p.add_argument("--scion", metavar="NAME", help="greffon dont la part est retirée (si plusieurs)")
    p.set_defaults(func=files.dir_remove)

    p = sub.add_parser("graft", parents=[common], help="regreffe (fichiers système du trunk supprimés)")
    p.add_argument("--scion", action="append", metavar="NAME", help="ne regreffer que ce greffon (répétable)")
    p.add_argument("--force", action="store_true", help="transmis à scion : conserve les autres fichiers réguliers")
    _no_cmake(p)
    p.set_defaults(func=files.graft)


def build_parser() -> argparse.ArgumentParser:
    parser = _Parser(prog="lepton",
                     description="Environnement de développement Lepton : graine, greffons, fichiers, vérification.")
    parser.add_argument("--version", action=_VersionAction)
    parser.add_argument("-v", "--verbose", action="store_true", help="affiche les commandes externes exécutées")
    parser.add_argument("-C", "--rootstock", metavar="DIR", help="rootstock (défaut : recherche en remontant)")
    sub = parser.add_subparsers(dest="command", metavar="COMMAND", parser_class=_Parser)
    common = _common_options()
    _add_seed_parser(sub, common)
    _add_scion_parser(sub, common)
    _add_files_parsers(sub, common)

    p = sub.add_parser("generate", parents=[common],
                       help="presets CMake (graine) et espace de travail VSCodium (CFG-6, IDE, DBG)")
    p.add_argument("--clangd", metavar="PATH", help="clangd à utiliser (défaut : clangd LLVM le plus récent du PATH)")
    p.add_argument("--probe-serial", metavar="SERIAL",
                   help="numéro de série de la sonde (adapter serial d'OpenOCD), conservé dans l'espace ; "
                        "\"\" le retire")
    p.set_defaults(func=generate.generate)

    p = sub.add_parser("check", parents=[common],
                       help="valide les manifestes ; sans FILE : graine, greffons greffés, XML (GRA-2, GRF-5, CFG-5)")
    p.add_argument("--json", action="store_true", help="sortie JSON")
    p.add_argument("files", nargs="*", metavar="FILE",
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
