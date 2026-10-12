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
   Le résultat doit être sous `<ROOTSTOCK>/depots/`. Éditer ce chemin-là.
2. Fichier ou répertoire nouveau : le créer dans le clone du greffon propriétaire, sous
   `scion/sys/root/src/…`, puis regreffer :
   ```bash
   cd <ROOTSTOCK> && scion graft
   ```
3. Déplacer ou renommer : `git -C <clone> mv …` puis `scion ungraft && scion graft`.
4. Supprimer : `git -C <clone> rm …` puis `scion ungraft && scion graft`.

Le hook du dépôt refuse les écritures directes sous `trunk/` (Write, Edit, et commandes shell
évidentes). Un refus du hook n'est pas à contourner : il signale une erreur de chemin.

## Interdits

- `sed -i`, `perl -i`, tout outil qui écrit par fichier temporaire puis renommage, appliqué à un
  chemin du trunk : il remplace le lien par un fichier régulier non versionné.
- Répertoire de construction ou sortie de mklepton dans le trunk.
- `scion seed-update`, `scion graft-update` (font un `git pull`) sans accord de l'utilisateur.
- `scion git` pour lire : sa sortie n'est pas affichée en 0.5.0.1. Utiliser `git -C <clone>`.

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
