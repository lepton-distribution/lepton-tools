# Étape ENV-71 — Miroirs de conservation : synchronisation (D40)

## Contexte
Révision du plan du 2026-11-23, faite à partir de `HORS-PLAN.md`. Pour D40, l'utilisateur a
décidé le 2026-11-23 (fin du plan, après ENV-66) :
- la synchronisation des miroirs (`scion mirror-sync`) entre dans le plan, ici ;
- les montées de version du code tiers sont confiées à des tickets, sur les greffons
  `family-stm32f7xx` (HAL v1.3.3 → v1.3.4, CMSIS device v1.2.10 → v1.2.11) et
  `family-stm32f4xx` (CMSIS device v2.6.12). Elles sont hors de cette étape. Leur état se lit à
  la ligne D40 de `HORS-PLAN.md`.

D40 (`rapports/env-66-debian.md` §7.3, `12-amont-ls-remote.txt`). En R66-1, le
`mirror-sync --dry-run` de la VM (`essais/env-53-debian`) donnait :
- 8 miroirs, code 0, 0 signalement ;
- 7 références à envoyer sur 4 miroirs :

| Miroir | À envoyer (2026-11-19) |
| --- | --- |
| `mirror-cmsis_device_f4` | `master` 9192c7b → 8c79dcf ; tag `v2.6.12` (nouveau) |
| `mirror-stm32wlxx-hal-driver` | `main` 5c87cf0 → e70dfa4 |
| `mirror-stm32f7xx-hal-driver` | `master` e860c4f → e879045 ; tag `v1.3.4` (nouveau) |
| `mirror-cmsis_device_f7` | `master` 2352e88 → 52e4aad ; tag `v1.2.11` (nouveau) |

Les miroirs sont publics, sous `lepton-distribution/`. Ils sont déclarés dans le
`scion/.scion/.scion.mirrors` des familles F4, F7 et WL (DEVENV-STATUS §Emplacements). L'envoi
passe par `url."ssh://git@github.com/".pushInsteadOf "https://github.com/"`, réglage global de
git de l'utilisateur (PA-68), présent au Mac le 2026-11-23.

**`mirror-sync` écrit, même avec `--dry-run`.** `sync_one` (`<SEED_SCIONS>/scion/mirror.py:270-273`)
clone le dépôt de travail `depots/.mirrors/<hôte>/<chemin>` (M-C2) avant de tester `dry_run`.
- `<ROOTSTOCK>` n'a pas de `depots/.mirrors/` (relevé du 2026-11-23). Une première passe y
  créerait 8 dépôts de travail, environ 79 Mo (`rapports/env-50-mac.md:107`), dont
  `mirror-STM32CubeWL` complet.
- `scripts/supprimer-essai.sh` ne pourrait pas les retirer.
- Au Mac, ces dépôts n'existent aujourd'hui que dans `essais/env-13-vierge/depots/.mirrors/`.

L'étape envoie vers des dépôts partagés : chaque envoi est soumis à PA-P. Les projections sont
épinglées (F4 `v1.8.5` et 3c77349…, F7 `v1.3.3` et `v1.2.10`, WL `v1.6.0` et `v1.4.0`), donc
aucun clone tiers, aucun lien du trunk ni aucun binaire ne change. Archétype : infrastructure.

## Prérequis
- ENV-66 terminée ; ENV-67 conseillée avant. Indépendante d'ENV-68, ENV-69, ENV-70.
- scion 0.6.3.3, ou le tag d'ENV-70 s'il est publié avant.
- Spécification du miroir : `<SEED_SCIONS>/doc/projection-miroir.md` (règles M-*) ;
  `rapports/env-40-miroir.md` (E10 : authentification ; E13 : passes depuis `<ROOTSTOCK>`).
- Règles de permission (`.claude/settings.json`) : `scion mirror-sync` n'y figure pas. Décision de
  l'utilisateur (relecture de la révision, 2026-11-23) : **l'envoi est lancé par l'utilisateur au
  terminal**. Aucune règle n'est ajoutée.
- Skill `lepton-rootstock` (écriture de `depots/.mirrors/` dans un rootstock).
- Branche `devenv/env-71` dans lepton-tools seulement (rapport et état).

## Tâches

### 1. Relevé sans `mirror-sync` → PA-129
Rapport `rapports/env-71-miroirs.md`.
- `git ls-remote` de chaque amont (`https://github.com/STMicroelectronics/<nom>.git`) et de chaque
  miroir des 8 : liste des références à envoyer. L'amont a pu avancer depuis R66-1 : la liste du
  jour fait foi.
- Date et titre de chaque commit à envoyer :
  `gh api repos/STMicroelectronics/<nom>/commits/<sha> --jq '.commit.committer.date, .commit.message'`
  (lecture). Chaque référence doit être expliquée par une publication de l'amont.
- Avance rapide seulement, tags nouveaux seulement (règles M-*) : pour chaque branche, le commit du
  miroir est un ancêtre de celui de l'amont (`gh api repos/…/compare/<miroir>...<amont>`, champ
  `status` = `ahead`).
- **PA-129** : l'utilisateur tranche :
  - lieu des dépôts de travail. Options :
    - `<ROOTSTOCK>` (forme d'E13 ; création des 8 dépôts, ~79 Mo, non supprimables par
      l'enveloppe) ;
    - `essais/env-13-vierge`, qui les a déjà (référence protégée ; ses `.scion.mirrors` sont
      ceux de sa graine).

    <À CONFIRMER au PA-129> ;
  - envoi accordé, pour tous les miroirs ou une partie (PA-P) ;
  - numéros des tickets de montée de version, cités au rapport.
- Aucun `mirror-sync`, même `--dry-run`, avant la réponse.

### 2. Passe à blanc, puis envoi
- `scion mirror-sync --dry-run -v <lieu>` : lancé par la session, directement. Relever la liste,
  les signalements et le code ; elle doit être égale à celle du §1.
- Envoi : l'utilisateur tape `! scion mirror-sync -v <lieu>` pour tous les miroirs, ou
  `! scion mirror-sync -v <lieu> <url du miroir>…` pour les seuls miroirs accordés
  (`<SEED_SCIONS>/scion/cli.py:351-355`). Le résultat s'affiche dans la conversation : relever le
  code et le journal au rapport.

### 3. Contrôles → PA-130
- `scion mirror-sync --dry-run -v <lieu>` : 0 référence à envoyer pour les miroirs envoyés,
  0 signalement.
- `git ls-remote` des miroirs : chaque référence envoyée est égale à l'amont.
- `<ROOTSTOCK>` : liste `chemin -> cible` inchangée, `CONFORME`, `lepton check` code 0.
- **PA-130** : rapport ; push et fusion de `devenv/env-71` dans `main` (PA-P). La VM relève
  `mirror-sync --dry-run` en ENV-72 ; l'attendu y est 0 référence à envoyer pour ces miroirs, sauf
  nouvelle publication de l'amont.

## Critères de validation
- [ ] PA-129 et PA-130 tranchés et consignés.
- [ ] Références accordées envoyées ; `mirror-sync --dry-run` à 0 référence à envoyer pour elles.
- [ ] Aucune réécriture d'un miroir ; aucun lien du trunk changé.
- [ ] `HORS-PLAN.md` : D40, partie synchronisation, marquée traitée avec renvoi au rapport ;
      partie montées de version renvoyée aux tickets.

## Pièges connus
- `mirror-sync --dry-run` clone les dépôts de travail absents : ce n'est pas une lecture.
- `mirror-sync` sans `--dry-run` envoie aussitôt : ne jamais le lancer pour « voir ».
- La session ne lance pas l'envoi : sans règle, le classifieur en déciderait. Il a déjà refusé
  des envois partagés (« Modify Shared Resources », D16).
- Aucune session VM active pendant l'envoi (ORCHESTRATION §2bis, « Invites simultanées »).
- `mirror-STM32CubeWL` est complet et volumineux : la passe à blanc peut durer.
- Le hook refuse `git config` sous `depots/tiers/`, même en lecture.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, branche, décisions PA-129 et PA-130, journal (références envoyées).
`HORS-PLAN.md` : D40. Passation `handoff/env-71.md`.
