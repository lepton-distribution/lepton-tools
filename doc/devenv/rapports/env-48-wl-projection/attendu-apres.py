#!/usr/bin/env python3
"""ENV-48 : liste « chemin -> cible » attendue après la bascule du WL.

Usage : python3 -I attendu-apres.py <liens-avant.txt> <attendus-wl.txt> <sortie.txt>

Part de la liste relevée avant la bascule (controler-trunk.py, liens.txt) et réoriente vers les
clones tiers projetés les cibles des seuls chemins de <attendus-wl.txt> (les 211 chemins des
attendus d'ENV-38, relatifs à la racine du trunk). Les fichiers qui restent dans la famille
(modifiés, hors amont, LEPTON-PROVENANCE.md) gardent leur cible. Règles (préfixes sous
depots/lepton/family-stm32wlxx/master/scion/sys/root/src/kernel/) :
  dev/arch/cortexm/stm32wlxx/cubemx_hal_driver/inc/  -> tiers/stm32wlxx-hal-driver/v1.3.0/Inc/
  dev/arch/cortexm/stm32wlxx/cubemx_hal_driver/src/  -> tiers/stm32wlxx-hal-driver/v1.3.0/Src/
  dev/arch/cortexm/stm32wlxx/cubemx_hal_driver/      -> tiers/stm32wlxx-hal-driver/v1.3.0/
  core/ucore/cmsis/Device/st/stm32wlxx/startup/iar/  -> tiers/cmsis-device-wl/v1.1.1/Source/Templates/iar/
  core/ucore/cmsis/Device/st/stm32wlxx/system_stm32wlxx.c -> …/Source/Templates/system_stm32wlxx.c
  core/ucore/cmsis/Device/st/stm32wlxx/              -> tiers/cmsis-device-wl/v1.1.1/Include/
  dev/arch/cortexm/stm32wlxx/radio_subghz_phy/stm32_radio_core_inc/utilities_def.h
      -> tiers/stm32cubewl/v1.3.0/Projects/NUCLEO-WL55JC/Applications/SubGHz_Phy/SubGHz_Phy_PingPong/Core/Inc/utilities_def.h
  dev/arch/cortexm/stm32wlxx/radio_subghz_phy/       -> tiers/stm32-mw-subghz-phy/v1.3.0/
  dev/arch/cortexm/stm32wlxx/Utilities/              -> tiers/stm32cubewl/v1.3.0/Utilities/
Écrit aussi <sortie>.projetes-wl (chemins réorientés). Code 1 si un attendu n'est pas un lien de
la liste, ou si un attendu ne relève d'aucune règle.
"""
import sys

FAM = "depots/lepton/family-stm32wlxx/master/scion/sys/root/src/kernel/"
T = "depots/tiers/"
PING = "Projects/NUCLEO-WL55JC/Applications/SubGHz_Phy/SubGHz_Phy_PingPong/Core/Inc/"
D = "dev/arch/cortexm/stm32wlxx/"
C = "core/ucore/cmsis/Device/st/stm32wlxx/"
REGLES = [  # du plus précis au plus général
    (D + "cubemx_hal_driver/inc/", T + "stm32wlxx-hal-driver/v1.3.0/Inc/"),
    (D + "cubemx_hal_driver/src/", T + "stm32wlxx-hal-driver/v1.3.0/Src/"),
    (D + "cubemx_hal_driver/", T + "stm32wlxx-hal-driver/v1.3.0/"),
    (C + "startup/iar/", T + "cmsis-device-wl/v1.1.1/Source/Templates/iar/"),
    (C + "system_stm32wlxx.c", T + "cmsis-device-wl/v1.1.1/Source/Templates/system_stm32wlxx.c"),
    (C, T + "cmsis-device-wl/v1.1.1/Include/"),
    (D + "radio_subghz_phy/stm32_radio_core_inc/utilities_def.h",
     T + "stm32cubewl/v1.3.0/" + PING + "utilities_def.h"),
    (D + "radio_subghz_phy/", T + "stm32-mw-subghz-phy/v1.3.0/"),
    (D + "Utilities/", T + "stm32cubewl/v1.3.0/Utilities/"),
]


def main():
    if len(sys.argv) != 4:
        print(__doc__, file=sys.stderr)
        return 2
    attendus = {l.strip() for l in open(sys.argv[2], encoding="utf-8") if l.strip()}
    sortie, projetes, vus, erreurs = [], [], set(), []
    for ligne in open(sys.argv[1], encoding="utf-8"):
        ligne = ligne.rstrip("\n")
        chemin, cible = ligne.split(" -> ", 1)
        rel = chemin[2:] if chemin.startswith("./") else chemin
        if rel in attendus:
            vus.add(rel)
            i = cible.find(FAM)
            if i < 0:
                erreurs.append(f"cible hors famille : {ligne}")
            else:
                reste = cible[i + len(FAM):]
                for avant, apres in REGLES:
                    if reste.startswith(avant):
                        cible = cible[:i] + apres + reste[len(avant):]
                        projetes.append(chemin)
                        break
                else:
                    erreurs.append(f"aucune règle : {ligne}")
        sortie.append(f"{chemin} -> {cible}")
    erreurs += [f"attendu absent de la liste : {a}" for a in sorted(attendus - vus)]
    with open(sys.argv[3], "w", encoding="utf-8") as f:
        f.write("\n".join(sortie) + "\n")
    with open(sys.argv[3] + ".projetes-wl", "w", encoding="utf-8") as f:
        f.write("\n".join(projetes) + "\n")
    for e in erreurs:
        print(e, file=sys.stderr)
    print(f"{len(sortie)} liens, {len(projetes)} cibles réorientées, {len(erreurs)} erreur(s)")
    return 1 if erreurs else 0


if __name__ == "__main__":
    sys.exit(main())
