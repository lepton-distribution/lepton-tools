---
name: lepton-cibles
description: Construire Lepton, l'exécuter sous QEMU (mps2-an386), le flasher et le déboguer sur NUCLEO-F429ZI et NUCLEO-WL55JC1 (cœur M4) depuis l'hôte macOS Intel ou Debian. Utiliser pour toute construction, test de fumée, lancement du banc KAL, écriture flash ou session GDB.
---

# Construire, exécuter, flasher, déboguer

Les commandes de ce fichier reprennent celles du portage. Les valeurs marquées `<RELEVÉ ENV-2>`
sont complétées en ENV-2 à partir de `doc/devenv/rapports/env-2-outillage.md` et
`env-2-cartes.md` ; tant qu'elles ne le sont pas, les relever dans le dépôt, ne jamais les
deviner.

## Construire

```bash
cmake -S <ROOTSTOCK>/trunk --list-presets
cmake -S <ROOTSTOCK>/trunk -B <ROOTSTOCK>/build/<preset> --preset <preset>
cmake --build <ROOTSTOCK>/build/<preset>
```
Répertoire de construction neuf pour un oracle (`rm -rf <ROOTSTOCK>/build/<preset>` avant).
Jamais de répertoire de construction dans le trunk.

| Cible | Preset | Exécutable |
| --- | --- | --- |
| QEMU `mps2-an386` | `<RELEVÉ ENV-2>` | `<RELEVÉ ENV-2>` |
| NUCLEO-F429ZI | `<RELEVÉ ENV-2>` | `<RELEVÉ ENV-2>` |
| NUCLEO-WL55JC1 (M4) | `<RELEVÉ ENV-2>` | `<RELEVÉ ENV-2>` |

## QEMU

```bash
<RELEVÉ ENV-2 : commande qemu-system-arm -M mps2-an386 … du portage>
```
Test de fumée : attendre l'invite `lsh`, taper `uname -a`, conserver la console complète.
Banc KAL : `<RELEVÉ ENV-2 : commande du banc>`.
Débogage : QEMU avec `-s -S`, puis `arm-none-eabi-gdb <elf>` et `target remote :1234`.

## Cartes réelles

Écriture flash : uniquement après autorisation de l'utilisateur pour la session (PA-11 ou point
d'arrêt de l'étape). Vérifier d'abord quelle carte est branchée :
```bash
openocd -f <interface> -f <target> -c "init; targets; shutdown"
```

| Carte | Fichiers OpenOCD | Console série |
| --- | --- | --- |
| NUCLEO-F429ZI | `<RELEVÉ ENV-2>` | `<RELEVÉ ENV-2>` |
| NUCLEO-WL55JC1 | `<RELEVÉ ENV-2>` (cœur M4 uniquement) | `<RELEVÉ ENV-2>` |

Flash puis vérification :
```bash
openocd -f <interface> -f <target> -c "program <elf> verify reset exit"
```
Débogage : `openocd -f <interface> -f <target>` dans un terminal, puis
`arm-none-eabi-gdb <elf> -ex "target extended-remote :3333" -ex "monitor reset halt"`.

## Pièges

- NUCLEO-WL55JC1 : Lepton tourne sur le cœur M4 ; ne jamais modifier les octets d'option ni le
  démarrage du M0+.
- Hôte Mac Intel : les outils viennent de MacPorts (pas de binaires Homebrew sur Intel) ; utiliser
  ceux qui répondent à `command -v` et consignés dans `DEVENV-STATUS.md` §Versions.
- Un échec de connexion de la sonde : relever le message OpenOCD complet avant toute autre action ;
  ne pas tenter de déverrouillage ni d'effacement de masse sans accord.
