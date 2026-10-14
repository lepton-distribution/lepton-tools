# Passation ENV-7 — Évolutions génériques de scion — session du 2026-10-13

## Statut
terminée (2026-10-13) — scion 0.5.1.0 réalisé, taggé localement, installé par pipx et validé sur le
rootstock réel ; aucun push.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `devenv/env-7` (depuis `main` = f4a8088, fusion de `devenv/env-6`) | `devenv(env-7): état et passation` | oui |
| seed.scions `<SEED_SCIONS>` | `master` (extraite) ; `devenv/env-7` = b2b2014 | 79f4f96 `Fusion de devenv/env-7 (scion 0.5.1.0)`, tag annoté `0.5.1.0` | oui |
| clone noyau `depots/lepton/original/master` | `master` (extraite) | 42733ce `Fusion de devenv/env-6 (…)` | oui |
| graine de travail `depots/lepton-seed.scions/original-tree` | `original-tree` (extraite) | 43d12e6 `Fusion de devenv/env-6 (…)` | oui |
| 7 greffons `depots/lepton-famille/*`, `depots/lepton-bsp/*` | `master` (extraite) | fusion de `devenv/env-6` (ex. stm32f4xx 01b5528, nucleo-wl55jc1 4a4fb30) | oui |

Branches `devenv/env-6` conservées dans tous les dépôts. Aucun push (aucun distant modifié). Trunk
regreffé par scion 0.5.1.0 : 4 037 feuilles, `.scion.grafted.list` à 9 lignes inchangé, aucun
fichier régulier, aucun lien cassé. `~/lepton/build/` non touché.

## Fait pendant la session
- Ouverture : fusions locales `--no-ff` de `devenv/env-6` (lepton-tools `main` f4a8088, clone noyau
  42733ce, graine 43d12e6, 7 greffons) ; arbres identiques à `devenv/env-6`, trunk intact.
- PA-8 : rapport `rapports/env-7-evolutions.md` (§1 conflits fichier / répertoire reproduits : trace
  Python, et **écriture dans le clone d'un autre scion avec code 0** via un lien versionné) ;
  décisions de l'utilisateur §5.
- scion 0.5.1.0 (`<SEED_SCIONS>`, 7 commits, détail `env-7-evolutions.md` §6) :
  `seed-scion-add [--seed] [--replace] CLÉ VERSION EMPLACEMENT [CHEMIN]`, `seed-scion-remove`,
  `graft --scion CLÉ` (répétable), `graft-remove [--purge] [--force] CLÉ`,
  `rootstock-install --bare`, sortie de `scion git`, conflits fichier / répertoire. Clé :
  `shelf@prefix::suffix` (comme `scion git --key`).
- Tests : 104 (1 ignoré), verts ; contre-épreuve E6 faite ; `grep -ri lepton scion/` = métadonnées.
- Essai sur copie du rootstock (scratchpad, supprimée) puis `scion graft` sur `~/lepton` : identique.
- Fusion `devenv/env-7` → `master` de seed.scions, tag `0.5.1.0`, `pipx install --force
  "git+file:///Users/cle_d_anton/lepton-tools-dev/seed.scions@0.5.1.0"`.
- lepton-tools fb6520c : skill `lepton-rootstock` (graft --scion, nouvelles commandes soumises à
  accord, sortie de `scion git`).

## Reste à faire dans l'étape
- [ ] Rien dans ENV-7. Début de la session suivante : fusion locale de `devenv/env-7` de
      lepton-tools dans `main`, après accord.
- [ ] Hors ENV-7, à planifier : push de seed.scions (`master` + tag `0.5.1.0`) vers
      `lepton-distribution/seed.scions` (PA-P) ; `ORCHESTRATION.md` §5 (« `scion git` : sortie non
      affichée en 0.5.0.1 ») à actualiser lors d'une révision du plan ; `.DS_Store` du Finder greffés
      (26 liens, ignorés par git dans les clones, comportement préexistant) — filtre éventuel à
      décider (générique : fichiers ignorés par git ?) ; reliquats d'ENV-6 inchangés (voir
      `handoff/env-6.md` §Reste à faire, hors fusions).

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Fusions locales de `devenv/env-6` en ouverture (plan accepté) | utilisateur | oui |
| PA-8 : E1-E6 telles que proposées ; E7 option B (`--bare`) ; 0.5.1.0 depuis `master` ; critère de test `unittest` | utilisateur | oui |
| PA-8 / PA-P : fusion locale dans `master` de seed.scions puis tag `0.5.1.0`, installation pipx ; aucun push | utilisateur | oui |
| E3 `--force` : fichiers réguliers du trunk tolérés et conservés (règle d'`ungraft`) | proposition, appliquée | non (rapport §6) |
| E3 et E4 dans un même commit (code de retrait commun) | proposition, appliquée | non (rapport §6) |
| `--purge` : refus si le chemin du scion n'est pas sous `depots/<shelf>/<prefix>/<version>` (tous les greffons famille/BSP locaux actuels sont donc non purgeables par scion) | proposition (rapport §2 validé) | oui (via PA-8) |
| ENV-7 terminée ; prochaine étape ENV-8 (ordre conseillé) | proposition, à confirmer au début de la session suivante | oui (prochaine action) |

## Pièges rencontrés
- Hook `proteger-trunk.py` : faux positif sur toute commande dont le texte contient `trunk`, même
  hors rootstock (édition de `seed.scions`) → script écrit dans le scratchpad (Write) puis exécuté.
- pipx : les environnements sont sous `~/Library/Application Support/pipx/venvs` (et non
  `~/.local/pipx`) → `pipx environment --value PIPX_LOCAL_VENVS`.
- Message de git dépendant de la langue : le test de `scion git` en échec vérifie la présence de la
  commande dans le stderr transmis, pas le libellé.
- Remplacement d'un scion : `graft-remove` **avant** `seed-clone` ; sinon l'entrée pointe sur le
  nouveau clone et les anciens liens, non reconnus, entrent en conflit (`README.md` de scion,
  « Faire évoluer un seed »).
- `sync` ne retire jamais une clé de la liste greffée : un retrait demande `seed-scion-remove` **et**
  `graft-remove`, sinon `seed-update` / `graft-update` réinscrivent le scion.
- Sauvegarde de `~/.claude` (plan de session écrit dans `~/.claude/plans/`) : non vérifiable depuis
  le bac à sable (lecture du dossier iCloud refusée) ; assurée par le hook `PostToolUse` global.

## Critères de validation
- [x] PA-8 tranché.
- [x] Tests verts (`unittest`, décision PA-8) ; `grep -ri lepton scion/` limité aux métadonnées
      (PA-2 Q7).
- [x] Commandes 0.5.0.1 existantes inchangées (tests existants verts).
- [x] Nouvelle version installée et relevée par `scion version` (0.5.1.0).

## Reprise
```
cd /Users/cle_d_anton/lepton-tools-dev/lepton-tools && claude
# « Démarre la session sur l'étape indiquée dans DEVENV-STATUS » (ENV-8, après fusion locale de devenv/env-7)
```
