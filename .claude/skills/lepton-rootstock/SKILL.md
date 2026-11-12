---
name: lepton-rootstock
description: Règles d'écriture et de contrôle dans un rootstock scion de Lepton (trunk composé de liens symboliques, clones git dans depots/). Utiliser avant toute création, modification, suppression ou déplacement de fichier de l'arbre Lepton, avant toute commande git sur un greffon, pour regreffer, ou pour préparer une copie d'essai du rootstock.
---

# Travailler dans un rootstock scion

Le trunk (`<ROOTSTOCK>/trunk/`) est une vue composée de liens symboliques relatifs. Les fichiers
réels et l'historique git sont dans les clones (`<ROOTSTOCK>/depots/…`). Chemins `<…>` : voir
`doc/devenv/DEVENV-STATUS.md` §Emplacements.

## Écrire

1. Trouver le fichier réel :
   ```bash
   realpath <ROOTSTOCK>/trunk/<chemin>     # macOS : realpath disponible depuis macOS 13 ; sinon python3 -c 'import os,sys;print(os.path.realpath(sys.argv[1]))'
   ```
   Le résultat doit être sous `<ROOTSTOCK>/depots/`. Éditer ce chemin-là, **sauf** s'il est sous
   `<ROOTSTOCK>/depots/tiers/` : c'est un clone tiers projeté (voir « Projection » ci-dessous),
   jamais modifié.
2. Fichier ou répertoire nouveau : le créer dans le clone du greffon propriétaire, sous
   `scion/sys/root/src/…`, puis regreffer :
   ```bash
   cd <ROOTSTOCK> && scion graft
   ```
   Depuis scion 0.5.1.0, regreffe du seul greffon touché (clé de `.scion.grafted.list`, `/` → `@`) :
   ```bash
   cd <ROOTSTOCK> && scion graft --scion lepton@bsp-nucleo-f429zi
   ```
3. Déplacer ou renommer : `git -C <clone> mv …` puis `scion graft` (ou `scion graft --scion <clé>`).
4. Supprimer : `git -C <clone> rm …` puis `scion graft` (ou `scion graft --scion <clé>`).

Le hook du dépôt refuse les écritures directes sous `trunk/` et sous `depots/tiers/` (Write, Edit,
et commandes shell évidentes). Un refus du hook n'est pas à contourner : il signale une erreur de
chemin. Depuis ENV-44, il analyse chaque commande simple et ne juge que les chemins qu'elle écrit :
une lecture qui cite `trunk/` ou `depots/tiers/` (`diff`, `grep`, `cp` depuis le trunk, script
sur plusieurs lignes) passe. Le contenu d'un script exécuté (`bash f.sh`, `python3 -c`) n'est
pas lu. Tests : `tests/test_proteger_trunk.py`.

## Projection (scion ≥ 0.6.0.0, ENV-41)

- Un greffon **porteur** (ex. `family-stm32f4xx`) déclare dans son `scion/.scion/`
  (`.scion.sources.list`, `.scion.ramifications`, `.scion.projections`, `.scion.mirrors`) des clés
  projetées (shelf `tiers`) : des dépôts tiers sans `scion/`, clonés sous
  `<ROOTSTOCK>/depots/tiers/<clé>/<version>` à un tag ou un commit, dont certains fichiers sont liés
  dans le trunk. La 6ᵉ colonne de `.scion.grafted.list` désigne le `.scion/` du porteur.
- **Ne jamais éditer un clone tiers**, ni y changer de commit : la greffe refuse un clone hors de son
  commit épinglé ou modifié (P-E1). Pour changer une version ou un motif : éditer le `scion/.scion/`
  du porteur dans son clone, commiter, puis `scion graft --scion <porteur>` (ou `scion graft`).
  Depuis scion 0.6.2.0, `graft --scion <porteur>` regreffe aussi ses clés projetées (P-G6). En
  0.6.1.0, il les laissait sans aucun lien.
  Pour remplacer un fichier tiers : l'exclure (`!motif`) et le fournir par un greffon ordinaire.
- Regreffe d'une seule clé projetée : `scion graft --scion tiers@<clé>`.
- **Extraction partielle** (scion ≥ 0.6.3.0, P-V7, ENV-52) : un clone tiers n'extrait que les
  répertoires parents des fichiers projetés, plus les fichiers de sa racine et de leurs répertoires
  ancêtres (`git sparse-checkout`, mode cône, git ≥ 2.35). C'est scion qui tient cet ensemble à
  chaque greffe : il l'élargit avant de poser les liens, puis le réduit après la greffe. Un clone
  encore extrait en entier est converti par sa prochaine greffe.
  - Un fichier non projeté est absent du disque. Il se lit par `git -C <clone> show HEAD:<chemin>`
    ou dans le miroir.
  - Ne jamais lancer `git sparse-checkout` à la main, même `list` : le hook le refuse, et la greffe
    suivante réécrirait l'ensemble.
  - Lectures admises : `git -C <clone> ls-files -t` (`H` extrait, `S` hors de l'ensemble),
    `cat <clone>/.git/info/sparse-checkout`, `find <clone> -type f`.
- Les sources des clés projetées désignent les miroirs `lepton-distribution/mirror-*` ; `scion
  mirror-sync` les tient à jour (jamais de `git push` à la main depuis `depots/.mirrors/`).
- `lepton file owner` nomme la clé projetée et son porteur ; `lepton file …` refuse d'y écrire.

## Interdits

- `sed -i`, `perl -i`, tout outil qui écrit par fichier temporaire puis renommage, appliqué à un
  chemin du trunk : il remplace le lien par un fichier régulier non versionné.
- Répertoire de construction ou sortie de mklepton dans le trunk.
- `scion seed-update`, `scion graft-update` (font un `git pull`) sans accord de l'utilisateur.
- `scion graft-remove --purge`, `scion seed-scion-add` / `seed-scion-remove` sur `<ROOTSTOCK>` sans
  accord : ils modifient la graine ou suppriment un clone.
- Git : préférer `git -C <clone>` (la sortie de `scion git` n'est affichée qu'à partir de 0.5.1.0).

## Contrôles (à lancer après toute série d'écritures)

```bash
cd <ROOTSTOCK>
find trunk -type f ! -name .scion.grafted.list     # attendu : vide
find -L trunk -type l                              # attendu : vide (aucun lien cassé)
git -C depots/lepton/original/master status --short
```
Un fichier régulier dans le trunk : ne pas le supprimer à l'aveugle. Le comparer à la cible du
lien attendu (`git -C <clone> diff`), reporter la modification dans le clone, puis le retirer et
regreffer.

## Copie d'essai du rootstock

```bash
cp -RP <ROOTSTOCK> <copie>      # -P : copier les liens, pas leur cible
```
Les liens sont relatifs au rootstock : la copie reste cohérente. Ne jamais monter ou copier le
trunk seul.

## Git

- Une branche `devenv/env-N` par clone touché ; se fier à `git branch --show-current`, pas au nom
  du répertoire (le clone noyau s'appelle `master` quelle que soit la branche extraite).
- Commits mécaniques (déplacements, génération) séparés des commits de fond.
- Pas de push sans accord.
