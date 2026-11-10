#!/usr/bin/env python3
"""ENV-47 : liste « chemin -> cible » attendue après la bascule du F7.

Usage : python3 -I attendu-apres.py <liens-avant.txt> <sortie.txt>

Part de la liste relevée avant la bascule (controler-trunk.py, liens.txt) et réoriente les
201 cibles de la copie F7 vers les clones tiers projetés (PA-81) :
  family-stm32f7xx/master/scion/sys/root/src/kernel/dev/arch/cortexm/stm32f7xx/hal_driver/<rel>
    -> tiers/stm32f7xx-hal-driver/v1.3.3/<rel>   (rel : Inc/…, Src/…, LICENSE.md, README.md)
  family-stm32f7xx/master/scion/sys/root/src/kernel/core/ucore/cmsis-5/Device/ST/STM32F7xx/<rel>
    -> tiers/cmsis-device-f7/v1.2.10/<rel>        (rel : Include/…, LICENSE.md, README.md)
Les LEPTON-PROVENANCE.md restent liés à la famille. Écrit aussi <sortie>.projetes-f7 (201 chemins).
"""
import sys

FAM = "depots/lepton/family-stm32f7xx/master/scion/sys/root/src/kernel/"
REGLES = [
    (FAM + "dev/arch/cortexm/stm32f7xx/hal_driver/", "depots/tiers/stm32f7xx-hal-driver/v1.3.3/"),
    (FAM + "core/ucore/cmsis-5/Device/ST/STM32F7xx/", "depots/tiers/cmsis-device-f7/v1.2.10/"),
]


def main():
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    sortie, projetes = [], []
    for ligne in open(sys.argv[1], encoding="utf-8"):
        ligne = ligne.rstrip("\n")
        chemin, cible = ligne.split(" -> ", 1)
        for avant, apres in REGLES:
            i = cible.find(avant)
            if i >= 0 and not cible.endswith("/LEPTON-PROVENANCE.md"):
                cible = cible[:i] + apres + cible[i + len(avant):]
                projetes.append(chemin)
                break
        sortie.append(f"{chemin} -> {cible}")
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write("\n".join(sortie) + "\n")
    with open(sys.argv[2] + ".projetes-f7", "w", encoding="utf-8") as f:
        f.write("\n".join(projetes) + "\n")
    print(f"{len(sortie)} liens, {len(projetes)} cibles réorientées")
    return 0


if __name__ == "__main__":
    sys.exit(main())
