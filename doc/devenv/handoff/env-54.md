# Passation ENV-54 — Claude Code : règles de permission ciblées (D16) — session du 2026-11-13 (intermédiaire, avant redémarrage)

## Statut
En cours — tâches 1 (audit, PA-95) et 2 (mise en place) faites ; tâche 3 (rejeu après
redémarrage de Claude Code, PA-96) à faire. La session reprend ENV-54, pas une nouvelle étape.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `devenv/env-54` (depuis `main` 4bed93c), non poussée | commit « état et passation intermédiaire » au-dessus de d089fb9 (skill lepton-cibles), 56b8955 (CLAUDE.md), 99ab64d (règles, enveloppe, §2bis), 35ccc10 (audit) | oui |
| seed.scions | `master` | 6416c33 (0.6.3.0), non touché | oui |
| clone noyau `depots/lepton/original/master` | `master` | 58e421e, non touché | oui |
| autres | — | non touchés | — |

Outils : scion 0.6.3.0 ; lepton 0.1.0 (réinstallé par `pipx install --force` depuis `main`, même
code, essai T5) ; Claude Code 2.1.323.

Hors dépôt : `~/lepton-tools-dev/essais/env-54-essai/` = `qemu` (copie d'`env-11/qemu` sans
`build/`, regreffée en T2 : rien n'a bougé), `clone-seed` (T4), `journaux/` (T2, T4 à T6,
`liens-avant.txt`, `liens-apres.txt` identiques).

## Fait pendant la session
- Début : état conforme à la passation de préparation ; plan approuvé ; branche créée ; étape
  « en cours ». Décisions au plan : forme réelle de `pipx install` ; PA-P pour `graft-update`
  dans `essais/env-54-essai/qemu` (passes §1 et §3).
- Audit : `rapports/env-54-permissions.md` §1 à §7.
  - Inventaire : refus `graft-update` (VM ×4, Mac ×1 en commande groupée), `rm -rf` (VM ×2),
    `pipx`, `git clone` et tests de scion (VM, R15-1 seul).
  - Mécanisme établi : documentation vérifiée mot pour mot (§3), et `claude auto-mode defaults`
    (annexe `env-54-permissions/auto-mode-defaults-2.1.323.json`). Diagnostic (§5) : sur la VM,
    l'accord arrive dans un `ORDRE` d'une autre session, que le classifieur ne tient pas pour un
    accord de l'utilisateur.
  - Essai témoin, sans règle : 6 commandes acceptées, toutes `reasonType: "classifier"` au
    journal de session (`~/.claude/projects/-Users-cle-d-anton-lepton-tools-dev-lepton-tools/75453a27-c3e9-424e-b2a5-1c6bbad93490.jsonl`).
- PA-95 tranché (`DEVENV-STATUS.md` §Décisions, rapport §8).
- Mise en place (rapport §9) :
  - `.claude/settings.json` : 7 `allow`, 4 `ask`, 5 `deny`, hook gardé, JSON valide ;
  - `scripts/supprimer-essai.sh` et `tests/test_supprimer_essai.py` : 52 tests verts (bash 5.3
    et 3.2), shellcheck propre ;
  - ORCHESTRATION §2bis amendé ; `CLAUDE.md` (commit 56b8955) ; skill `lepton-cibles`
    (commit d089fb9) ; hook : 118 tests verts.

## Reste à faire dans l'étape
- [ ] Tâche 3, après redémarrage (§3 du fichier d'étape). PA-P déjà accordé pour le
      `graft-update` de la copie. Une commande simple par appel ; relever ensuite
      `permissionDecision` dans le `.jsonl` de la nouvelle session.
  - Acceptations attendues :
    - R1 `cd ~/lepton-tools-dev/essais/env-54-essai/qemu && scion graft-update -v > ../journaux/r1-graft-update.log 2>&1` → invite (`ask`) ; l'utilisateur confirme.
    - R2 `git clone file:///Users/cle_d_anton/lepton-tools-dev/seed.scions ~/lepton-tools-dev/essais/env-54-essai/clone-seed-2` → règle.
    - R3 `scripts/supprimer-essai.sh ~/lepton-tools-dev/essais/env-54-essai/clone-seed` (créé par la session précédente, donc préexistant) → règle.
    - R4 `pipx install --force ~/lepton-tools-dev/lepton-tools` → règle ; vérifier `lepton --version`.
    - R5 `~/lepton-tools-dev/venv-lepton-tools/bin/pytest -q` → règle ; 436 attendus (384 + 52).
  - Contrôles négatifs, sur cibles absentes :
    - N1 `scripts/supprimer-essai.sh ~/lepton-tools-dev/essais/env-54-essai/../../absent-env54` → code 2.
    - N2 `scripts/supprimer-essai.sh ~/lepton-absent-env54` → code 2.
    - N3 `rm -rf ~/lepton-tools-dev/essais/env-54-absent` → classifieur, constater.
    - N4 `cd ~/lepton-tools-dev/essais/env-54-absent && scion graft-update -v` → invite ; l'utilisateur refuse.
    - N5 `git -C ~/lepton-tools-dev/essais/env-54-absent push` → invite ; l'utilisateur refuse.
    - N6 `git clone --upload-pack=true file:///absent ~/lepton-tools-dev/essais/env-54-essai/x` → refus (`deny`).
  - Hook : N7 `touch ~/lepton-tools-dev/essais/env-54-essai/qemu/trunk/essai-hook` → refus du hook.
  - Facultatif : l'utilisateur ouvre `/permissions` et vérifie qu'aucune règle n'est écartée.
- [ ] PA-96 : rapport (§10 à écrire), confirmation des `deny` sur `git clone` (ajoutés par la
      session), sort d'`essais/env-54-essai`, push et fusion de `devenv/env-54` (PA-P).
- [ ] `HORS-PLAN.md` : D16 traité, renvoi au rapport ; fin de session (statut, journal, passation).

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Forme témoin de `pipx install` = forme réelle, même version depuis `main` | utilisateur | oui |
| PA-P : `graft-update` dans `essais/env-54-essai/qemu`, passes §1 et §3 | utilisateur | oui |
| PA-95 : règles projet versionnées, enveloppe avec références, `ask` sur `git push`, `allow` pipx, `git clone` ciblé et pytest, reste du §7 (dont redémarrage) | utilisateur | oui |
| `deny` sur les options dangereuses de `git clone` (`--upload-pack`, `-u`, `--config`, `-c`, `ext::`) | proposition non validée (session), à confirmer au PA-96 | rapport §9 |
| Liste des formes de rejeu R1 à R5, N1 à N7 | proposition non validée | non |

## Pièges rencontrés
- `echo ========` dans zsh : `=` en tête de mot déclenche l'expansion `=cmd` (« ======= not
  found »). Parade : guillemets.
- `cd -P //private` garde « // » en tête dans `pwd` (bash) : corrigé dans l'enveloppe, et couvert
  par les tests.
- pathlib retire `/` et `.` finaux : les tests passent les chemins en texte brut.
- Le dossier iCloud de sauvegarde de `~/.claude` n'est pas lisible par la session (« Operation not
  permitted », sandbox). Je n'ai pas pu vérifier l'archive créée par le hook de l'utilisateur
  pour le fichier de plan.
- Réglages relus à chaud (documenté) : les règles valent déjà dans cette session.

## Critères de validation
- [x] PA-95 tranché et consigné ; [ ] PA-96.
- [x] Inventaire des refus, des acceptations et des formes de commandes au rapport.
- [x] Mécanisme établi, avec sa source (page de documentation, essai).
- [ ] Essai témoin rejoué après redémarrage : chaque commande retenue est acceptée, chaque
      contrôle négatif est refusé ou soumis à confirmation. Le journal de session est cité.
- [ ] Le hook refuse toujours une écriture sous un `trunk/` (rejeu) ; [x] `settings.json` est du JSON valide.
- [ ] `pytest` complet vert (rejeu) ; [x] hook inchangé (118 verts).
- [x] ORCHESTRATION §2bis amendé.
- [ ] `HORS-PLAN.md` : D16 marqué traité, avec renvoi au rapport.

## Reprise
Commande ou première action de la session suivante :
```
reprendre ENV-54 (skill devenv-session) après redémarrage de Claude Code : lire cette passation
et rapports/env-54-permissions.md §9 ; tâche 3 (rejeu R1 à R5, N1 à N7) puis PA-96
```
