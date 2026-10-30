# Étape ENV-13 — Graine de référence publiée

## Contexte
Depuis ENV-6, le code des cartes est porté par 7 greffons famille et BSP, absents du noyau
`lepton-original-tree.scions`. Publiés sur GitHub (`lepton-distribution`) le 2026-10-30, ils restent
désignés dans la graine de travail `<ROOTSTOCK>/depots/lepton-seed.scions/original-tree` par des
chemins locaux en version `*` (4 commits d'ENV-6, non poussés) : la graine publiée ne donne qu'un
noyau sans carte. Cette étape fait de cette graine le point d'entrée de l'arbre complet sur toute
machine. Migration iso-fonctionnelle : seul l'assemblage du rootstock change ; le trunk et les
binaires restent identiques à l'oracle.

## Prérequis
- ENV-6 et ENV-11 terminées. scion 0.5.1.1, lepton 0.1.0 (`DEVENV-STATUS.md` §Versions).
- Décisions de l'utilisateur du 2026-10-30 (`DEVENV-STATUS.md` §Décisions) : clés renommées selon
  la convention de `lepton` (`family-<nom>`, `bsp-<nom>`) ; URL en `https://` ; sort des anciens
  clones tranché au PA-14 ; numérotation ENV-13.
- Dépôts GitHub publics, `master` égal au `master` local (`git ls-remote`, 2026-10-30) :

| Clé actuelle | Clé cible | Dépôt `https://github.com/lepton-distribution/…` | `master` |
| --- | --- | --- | --- |
| `famille::qemu-mps2` | `family-qemu-mps2` | `lepton-famille-qemu-mps2.git` | 3954357 |
| `bsp::qemu-mps2-an386` | `bsp-qemu-mps2-an386` | `lepton-bsp-qemu-mps2-an386.git` | 046779e |
| `bsp::qemu-mps2-an500` | `bsp-qemu-mps2-an500` | `lepton-bsp-qemu-mps2-an500.git` | e98a482 |
| `famille::stm32f4xx` | `family-stm32f4xx` | `lepton-famille-stm32f4xx.git` | 01b5528 |
| `bsp::nucleo-f429zi` | `bsp-nucleo-f429zi` | `lepton-bsp-nucleo-f429zi.git` | 8ea7ee5 |
| `famille::stm32wlxx` | `family-stm32wlxx` | `lepton-famille-stm32wlxx.git` | 1eccc2f |
| `bsp::nucleo-wl55jc1` | `bsp-nucleo-wl55jc1` | `lepton-bsp-nucleo-wl55jc1.git` | a329f4d |

- Entrées inchangées : `original::tree` (URL `https://`, `master`) et `building` (`*`,
  `depots/generation/building`, créé par `scion rootstock-install` sur toute machine).
- Branches `devenv/env-13` : lepton-tools (depuis `main`), graine (depuis `original-tree` 43d12e6).

## Tâches

### 1. PA-13 — état de départ et séquence de regreffe
- Relever : `trunk/.scion.grafted.list` de `<ROOTSTOCK>` (9 entrées), têtes des 7 clones locaux
  (`master` égal à la table ci-dessus, aucune modification non commitée), `git status` du clone
  noyau et de la graine.
- Établir, depuis le code de `<SEED_SCIONS>` (`scion/cli.py`, `scion/graft.py`), la séquence
  qui retire les 7 anciennes clés et greffe les 7 nouvelles : retrait (`graft-remove` sans
  `--purge`, clé `/` → `@`), clonage des sources distantes, regreffe. Préciser si `sync`
  retire de lui-même une clé absente des ramifications.
- La rejouer sur une copie d'essai `cp -RP <ROOTSTOCK> <copie>` (skill `lepton-rootstock`),
  graine de la copie modifiée comme au §3, et y appliquer les contrôles du §5.
- Présenter : séquence exacte, résultat sur la copie, commandes qui relèvent de PA-P. Attendre.

### 2. Oracle avant
Skill `lepton-oracle`, répertoires de construction neufs, sur les 14 presets de
`oracles/env-8-r3-apres/` → `doc/devenv/rapports/oracles/env-13-avant/<preset>/`. Fumée et banc
KAL sur les 6 presets QEMU (skill `lepton-cibles`). Aucune modification avant la fin de la capture.

### 3. Graine
Sur `devenv/env-13` de la graine, un seul commit : dans `scion/.scion/.scion.sources.list` et
`scion/.scion/.scion.ramifications`, remplacer les 7 lignes selon la table (clé cible, version
`master`, URL `https://`) ; mettre à jour le commentaire d'ENV-6. Ne pas réécrire les 4 commits
d'ENV-6. Ne pas toucher `master` de la graine.

### 4. Regreffe de `<ROOTSTOCK>` (PA-P)
Après accord : appliquer la séquence validée au §1. Clones attendus :
`depots/lepton/family-<nom>/master` et `depots/lepton/bsp-<nom>/master`, chacun sur `master` au
commit de la table. Dans chaque nouveau clone : `git remote set-url --push origin
ssh://git@github.com/lepton-distribution/<dépôt>.git`.

### 5. Contrôles et oracle après
- Contrôles du trunk (skill `lepton-rootstock`) : aucun fichier régulier, aucun lien cassé ;
  `trunk/.scion.grafted.list` : 9 entrées, les 7 nouvelles clés, aucune ancienne.
- Aucun lien du trunk vers `depots/lepton-famille/` ou `depots/lepton-bsp/` :
  `find trunk -type l -exec readlink {} + | grep -c -E 'lepton-(famille|bsp)/'` → 0.
- Oracle après sur les 14 presets (`env-13-apres/`), mêmes commandes ; comparaison ; fumée et banc
  KAL identiques. Rapport `doc/devenv/rapports/env-13-graine.md` (table de la skill oracle).

### 6. PA-14 — publication et anciens clones
Présenter le rapport, puis demander :
- push de `devenv/env-13` fusionnée dans `original-tree` de la graine (PA-P) ;
- sort de `<ROOTSTOCK>/depots/lepton-famille/*` et `depots/lepton-bsp/*` (suppression,
  archivage ou conservation), sachant que `essais/env-9` et `essais/env-11/{f429zi,wl55jc1}` les
  désignent en `file://` dans leurs graines ; vérifier avant toute suppression qu'aucun commit local
  n'est absent de GitHub (`git -C <clone> log origin/master..` sur toutes les branches).

### 7. Clôture
Clone d'essai frais de la graine publiée dans un rootstock vierge
(`<À CONFIRMER au PA-14 : emplacement>`) : `scion` greffe les 9 entrées depuis GitHub ; construction
d'un preset QEMU et fumée. Mettre à jour `DEVENV-STATUS.md` §Emplacements (greffons et graine).

## Critères de validation
- [ ] PA-13 et PA-14 tranchés et consignés.
- [ ] Graine : 7 clés `family-`/`bsp-`, version `master`, URL `https://` ; `original::tree` et
      `building` inchangés ; 4 commits d'ENV-6 conservés.
- [ ] 7 clones sous `depots/lepton/<clé>/master` au commit de la table ; pushurl SSH.
- [ ] Trunk : 0 fichier régulier, 0 lien cassé, 0 lien vers les anciens clones.
- [ ] `comparer-oracle.py` code 0 sur les 14 presets, ou chaque écart expliqué ; fumée et banc KAL
      identiques sur les 6 presets QEMU.
- [ ] `original-tree` poussée (si accordé) ; un rootstock vierge greffe l'arbre complet depuis
      GitHub et le preset QEMU passe la fumée.

## Pièges connus
- Clés `famille::<nom>` gardées avec une URL : scion clone dans `depots/<shelf>/<préfixe avant
  ::>/<version>` (`scion/graft.py`) → les 3 familles dans `depots/lepton/famille/master`, les 4 BSP
  dans `depots/lepton/bsp/master`, un seul dépôt cloné par groupe. D'où le renommage.
- `graft-update` et `seed-update` font des `git pull` : PA-P à chaque emploi.
- Empreintes différentes avec sections et symboles identiques : chemin du clone dans les
  informations de débogage ; l'expliquer, ne pas le corriger dans cette étape.
- Deux clones du même greffon coexistent jusqu'au PA-14 : n'éditer que le clone greffé
  (`realpath` depuis le trunk).
- `lepton check` sur `<ROOTSTOCK>` signale « manifeste de graine absent » (graine hors lepton,
  constat d'ENV-12) : sans rapport avec l'étape, ne pas le traiter ici.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, emplacements des greffons et de la graine, décisions PA-13 et PA-14,
journal. Passation `handoff/env-13.md`.
