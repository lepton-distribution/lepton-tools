# ENV-0 — Construction de référence et oracle de départ

Date : 2026-10-12. Hôte : Mac mini Intel, macOS. Rootstock `~/lepton`, clone noyau `master` 6b62af5.
Oracles : `doc/devenv/rapports/oracles/env-0/<preset>/` (choix de l'utilisateur, session 2).

## Commandes exactes

```bash
cd ~/lepton && source depots/lepton/original/master/scripts/lepton-env.sh   # exporte LEPTON_EMBOS_ROOT
P=<preset>
rm -rf ~/lepton/build/$P
cmake -S ~/lepton/trunk -B ~/lepton/build/$P --preset $P
cmake --build ~/lepton/build/$P
ctest --test-dir ~/lepton/build/$P --output-on-failure            # > banc-kal.log
scripts/oracle/capturer-oracle.sh ~/lepton/build/$P/lepton.elf doc/devenv/rapports/oracles/env-0/$P
cp ~/lepton/build/$P/smoke_lsh_uart0.log doc/devenv/rapports/oracles/env-0/$P/fumee.log
```

Compilateur : arm-none-eabi-gcc 14.2.1 (Arm GNU Toolchain 14.2.Rel1), identique pour les 4 presets.

## Résultats

| Preset | Sections/symboles | Empreinte `lepton.elf` (début) | Fumée | Banc KAL (ctest) | Écarts expliqués |
| --- | --- | --- | --- | --- | --- |
| qemu-mps2-an386-embos | capturés (1583 lignes de symboles) | 480d740d775e | OK (`lsh`, `uname -a`) | 18/18 | sans objet (référence) |
| qemu-mps2-an386-freertos | capturés (1623) | 7ecafaa66b4e | OK | 18/18 | sans objet |
| qemu-mps2-an386-embos-soft | capturés (1580) | 8943e75530d9 | OK | 14/14 | sans objet |
| qemu-mps2-an386-freertos-soft | capturés (1622) | 63e63bae0389 | OK | 14/14 | sans objet |

`comparer-oracle.py` appliqué à chaque oracle contre lui-même renvoie le code 0 : les captures sont
complètes.

## Constats

- Un premier passage sans `lepton-env.sh` a fait échouer la configuration des presets embOS avec
  l'erreur `embOS introuvable : LEPTON_EMBOS_ROOT=` : le paquet embOS est hors git, dans
  `~/lepton/third_party/embos/cortexm-gcc/5.20.0.0`. Les presets FreeRTOS, eux, n'en ont pas besoin.
- Dans ce cas, `ctest` affiche « No tests were found!!! » mais **renvoie 0**. Il ne faut donc pas
  se fier à son seul code de retour : contrôler la ligne « 100% tests passed … out of N ».
- `scripts/lepton-env.sh` existe dans le clone noyau mais n'est pas greffé dans le trunk.
- Les sorties de la migration dans `~/lepton/build/qemu-mps2-an386-*` ont été remplacées par ces
  constructions neuves (décision de l'utilisateur).
