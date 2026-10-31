---
name: lepton-oracle
description: Capture et comparaison d'un état de référence (oracle) d'une construction Lepton pour prouver la non-régression — empreintes, sections, symboles, test de fumée, banc KAL. Utiliser avant toute modification du système de construction, de mklepton ou de l'emplacement du code (ENV-0, ENV-4, ENV-5, ENV-6, ENV-11), et pour tout « est-ce que ça marche toujours pareil ? ».
---

# Oracle de non-régression

Un oracle se capture **avant** la première modification, sur l'état de départ, et se rejoue
**après**, avec exactement les mêmes commandes. Sans oracle capturé avant, aucune affirmation de
non-régression n'est recevable : le dire et s'arrêter.

Emplacement : `doc/devenv/rapports/oracles/<étape>-<avant|apres>/<preset>/`.

## 1. Binaire

```bash
scripts/oracle/capturer-oracle.sh <ROOTSTOCK>/build/<preset>/<exécutable>.elf \
    doc/devenv/rapports/oracles/env-N-avant/<preset>
```
Produit `empreintes.txt`, `sections.txt`, `symboles.txt`, `outils.txt`. Le nom de l'exécutable
est relevé dans le répertoire de construction (ne pas le supposer).

Comparaison :
```bash
python3 scripts/oracle/comparer-oracle.py \
    doc/devenv/rapports/oracles/env-N-avant/<preset> \
    doc/devenv/rapports/oracles/env-N-apres/<preset>
```
- Code 0 : mêmes sections, mêmes symboles (nom, type, taille). Les empreintes peuvent différer
  (ordre d'édition de liens) : ce n'est pas une régression.
- Code 1 : chaque écart est listé ; chacun doit être expliqué dans le rapport de l'étape. Un écart
  non expliqué bloque l'étape.
- Code 2 : capture incomplète.

Série complète (construction à neuf, `host` d'abord, fumée et banc KAL des presets QEMU,
capture binaire de chaque preset) :
```bash
scripts/oracle/rejouer-oracle.sh <ROOTSTOCK> doc/devenv/rapports/oracles/env-N-avant \
    --qemu <preset>... --carte <preset>...
```
Liste des 14 presets (6 QEMU, 8 carte) : `doc/devenv/rapports/env-13-graine.md` §4. Les mêmes
arguments servent à l'oracle après.

## 2. Sorties de mklepton (ENV-4)

Utiliser le script du portage `tests/host/mklepton_empreintes.sh` (dans le clone noyau ; vérifier
son usage dans `doc/devenv/rapports/env-2-outillage.md`). Ne pas en écrire un second.
Attendu : empreintes identiques des sources générées et de l'image UFS.

## 3. Comportement

- **Test de fumée** : démarrage jusqu'à l'invite `lsh`, puis `uname -a`. Conserver la sortie
  console complète dans `fumee.log` à côté de la capture binaire. Commandes : skill
  `lepton-cibles`.
- **Banc KAL** (QEMU, matrice architecture × backend) : conserver le rapport complet dans
  `banc-kal.log`. Attendu après modification : même liste de cas, mêmes résultats.

Comparer les journaux en ignorant uniquement les horodatages et adresses, et dire lesquels ont été
ignorés.

## 4. Rapport

Dans le rapport de l'étape (`doc/devenv/rapports/env-N-*.md`), une table :

| Preset | Sections/symboles | Empreinte | Fumée | Banc KAL | Écarts expliqués |
| --- | --- | --- | --- | --- | --- |

Puis la liste des écarts et leur explication. Présenter ce rapport au point d'arrêt de l'étape.

## Pièges

- Capturer l'oracle et la nouvelle version avec le même compilateur : vérifier `outils.txt`.
- Une construction incrémentale peut laisser des objets périmés : oracle et comparaison sur des
  répertoires de construction neufs.
- Un symbole `static` de même nom dans deux fichiers apparaît deux fois : c'est normal.
