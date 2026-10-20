"""Configurations de la graine : seed config add, seed config remove (CFG-6 ; O2, F7 d'ENV-12).

Une configuration = un preset généré `<projet>-<nom>` ; après modification de `lepton-graine.json`,
presets et espace de travail sont régénérés comme par `lepton generate` (sauf `--no-generate`).
"""

import argparse

from lepton import generate, seed
from lepton.errors import EXIT_OK, LeptonError
from lepton.rootstock import Rootstock
from lepton.validation import validate_data

BUILD_TYPES = ["Debug", "Release", "RelWithDebInfo", "MinSizeRel"]   # enum `construction` du schéma
RUNS = ["qemu", "carte"]                                             # enum `execution` du schéma


def _regenerate(rs: Rootstock, no_generate: bool) -> int:
    if no_generate:
        seed._info(f"presets à régénérer : lepton generate -C {rs.path}")
        seed._remind_commit(rs.seed_root())
        return EXIT_OK
    return generate.generate(argparse.Namespace(rootstock=str(rs.path), clangd=None, probe_serial=None))


def config_add(args) -> int:
    rs, seed_root, graine_path, graine = seed._seed_context(args)
    configurations = graine["configurations"]
    if any(c["nom"] == args.name for c in configurations):
        raise LeptonError(f"configuration « {args.name} » déjà dans la graine",
                          f"lepton seed config remove {args.name}, ou choisir un autre nom")
    config = {"nom": args.name, "construction": args.build_type, "execution": args.run}
    bsp = next((m for m in rs.manifests().values() if m.name == graine["bsp"]), None)
    if bsp is None:
        raise LeptonError(f"BSP « {graine['bsp']} » de la graine non greffé", "lepton seed status")
    generate.check_configuration(config, bsp.name, bsp.data,
                                 f"--run {'carte' if args.run == 'qemu' else 'qemu'}, ou changer de BSP")
    configurations.append(config)
    anomalies = validate_data(graine, "seed", str(graine_path))
    if anomalies:
        raise LeptonError(f"NAME « {args.name} » refusé :\n" + "\n".join(f"  {a.location}: {a.message}" for a in anomalies),
                          "minuscules, chiffres, « . », « _ », « - »")
    seed.save_graine(graine_path, graine)
    seed._info(f"configuration {args.name} ajoutée ({args.build_type}, {args.run}) : "
               f"preset {graine['projet']['nom']}-{args.name}")
    return _regenerate(rs, args.no_generate)


def config_remove(args) -> int:
    rs, seed_root, graine_path, graine = seed._seed_context(args)
    configurations = graine["configurations"]
    names = [c["nom"] for c in configurations]
    if args.name not in names:
        raise LeptonError(f"configuration « {args.name} » absente de la graine ({', '.join(names)})",
                          "lepton seed status")
    if len(configurations) == 1:
        raise LeptonError(f"« {args.name} » est la seule configuration de la graine (au moins une)",
                          "lepton seed config add … avant de la retirer")
    graine["configurations"] = [c for c in configurations if c["nom"] != args.name]
    seed.save_graine(graine_path, graine)
    preset = f"{graine['projet']['nom']}-{args.name}"
    seed._info(f"configuration {args.name} retirée (preset {preset})")
    build = rs.build / preset
    if build.exists():
        seed._info(f"répertoire de construction conservé : {build}")
    return _regenerate(rs, args.no_generate)
