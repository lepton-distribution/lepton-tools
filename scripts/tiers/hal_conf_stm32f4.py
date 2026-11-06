#!/usr/bin/env python3
"""hal_conf_stm32f4.py — dérive le stm32f4xx_hal_conf.h d'un BSP du modèle livré avec la HAL F4.

Usage :
  python3 scripts/tiers/hal_conf_stm32f4.py <modèle> <sortie> <HSE_Hz> <MODULE>...
  ex. : python3 scripts/tiers/hal_conf_stm32f4.py \\
          <ROOTSTOCK>/trunk/sys/root/src/kernel/dev/arch/cortexm/stm32f4xx/hal_driver/Inc/stm32f4xx_hal_conf_template.h \\
          <bsp>/stm32f4xx_hal_conf.h 8000000 CORTEX ETH FLASH GPIO PWR RCC

Dérivé de tools/migration/hal_conf_stm32f7.py du clone noyau (ENV-35, PA-57) : copie du modèle
non modifié de la HAL (stm32f4xx-hal-driver ; depuis ENV-41, fichier projeté par scion depuis le
clone tiers, lu par le trunk ; voir LEPTON-PROVENANCE.md de hal_driver/), seuls les
modules nommés restent activés (HAL_MODULE_ENABLED toujours), les autres
`#define HAL_<X>_MODULE_ENABLED` sont mis en commentaire ; valeur de HSE_VALUE remplacée.
Rejouable : le résultat ne dépend que du modèle et des arguments. Code de retour 0, ou 1 avec un
message (module absent du modèle, HSE_VALUE introuvable).
"""
import pathlib
import re
import sys


def main(argv):
    if len(argv) < 5:
        print(__doc__, file=sys.stderr)
        return 1
    template, out = pathlib.Path(argv[1]), pathlib.Path(argv[2])
    hse, modules = int(argv[3]), {m.upper() for m in argv[4:]}
    text = template.read_text(encoding="ascii")
    seen = set()

    def module(m):
        name = m.group(2)
        seen.add(name)
        if name in modules:
            return m.group(0)
        return "/* %s */" % m.group(1).rstrip()

    text = re.sub(r"^(#define HAL_([A-Z0-9]+)_MODULE_ENABLED\s*)$", module, text, flags=re.M)
    unknown = modules - seen
    if unknown:
        print("modules absents du modèle : " + ", ".join(sorted(unknown)), file=sys.stderr)
        return 1
    text, n = re.subn(r"(#define HSE_VALUE\s+)\S+U", r"\g<1>%dU" % hse, text, count=1)
    if n != 1:
        print("HSE_VALUE introuvable dans le modèle", file=sys.stderr)
        return 1
    head =("/* Lepton : généré par lepton-tools scripts/tiers/hal_conf_stm32f4.py depuis\n"
            " * hal_driver/Inc/stm32f4xx_hal_conf_template.h (stm32f4xx-hal-driver v1.8.5) ;\n"
            " * modules : %s ; HSE_VALUE %d. Ne pas éditer : rejouer le script. */\n"
            % (", ".join(sorted(modules)), hse))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(head + text, encoding="utf-8")
    print("%s : %d module(s) activé(s)" % (out, len(modules)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
