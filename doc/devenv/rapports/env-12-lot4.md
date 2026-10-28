# ENV-12 lot 4 — F5 : diagnostics en erreur à la saisie (CFG-7 §2bis) et L3-5

Session du 2026-10-23, branche `devenv/env-12` (lepton-tools). Décisions de l'utilisateur :
`DEVENV-STATUS.md` §Décisions (2026-10-23, lot 4).

## 1. Forme retenue

| Sujet | Retenu |
| --- | --- |
| Source des diagnostics | `lepton check --json --stdin FICHIER` : contenu non enregistré sur l'entrée standard, positions fournies par lepton (`line`, `column`, `end_line`, `end_column`) ; l'extension relaie en erreur, sans logique propre |
| Doublons | JSON validé par lepton seul : `lepton generate` écrit `json.validate.enable: false` (complétion et survol par `json.schemas` gardés) ; XML : lemminx seul à la saisie (portée exacte) |
| Saisie | `lepton-greffon.json`, `lepton-graine.json` : schéma du seul fichier, temporisation 400 ms (`lepton.diagnostics.delay`), appel hors file (lecture seule), le dernier gagne |
| Contrôle complet | `lepton check --json` à l'enregistrement d'un manifeste ou du XML mklepton (motifs de `xml.fileAssociations`), et par la palette « Lepton : vérifier » (L3-5) ; notification avec « Afficher les problèmes » |
| Exclusion | un document porte soit les diagnostics de la saisie (depuis sa dernière modification), soit ceux du contrôle complet (depuis son dernier enregistrement) |
| Réglage | `lepton.diagnostics.enabled` (défaut vrai) |

Interface de lepton : `rapports/env-8-interface.md` §13.

## 2. Réalisation

| Dépôt | Commit | Contenu |
| --- | --- | --- |
| lepton-tools | ce09596 | `lepton/jsonpos.py` (portées par pointeur JSON), `validation.py` (positions, contenu fourni, xmllint sur stdin, une anomalie par champ non autorisé), `checks.py` (contrôles du rootstock situés, ligne des `<dev>`/`<bin>` CFG-5), `cli.py` (`--stdin`), `generate.py` (`json.validate.enable`), `scion_runner.run(input=…)` ; `tests/test_diagnostics.py` |
| lepton-tools | 0136c63 | extension 0.3.0 : `src/diagnostics.ts`, `runLepton` avec entrée standard, `placeOf`, `diagnosticMessage`, palette « vérifier » vers *Problèmes*, réglages, traductions |

## 3. Contrôles

| Contrôle | Résultat |
| --- | --- |
| `pytest` (venv de développement) | 180 verts (170 au lot 3) |
| `npm test` | 15 verts (11 au lot 3) |
| `scripts/bout-en-bout.sh` (lepton de la branche) | succès |
| `check --stdin` à la main (`essais/env-11/qemu`) | graine : champ absent 1:1, champ non autorisé sur sa clé (ligne 11) ; JSON mal formé situé ; XML : ligne 9, colonne nulle ; deux FILE : refus, code 1 |
| `check --stdin` | ≈ 0,2 s par appel |
| Réinstallation | lepton par `pipx install --force` ; `lepton-distribution.lepton@0.3.0` par `codium --install-extension --force` |
| Espaces régénérés | `essais/env-11/{qemu,f429zi,wl55jc1}`, `essais/env-9` : code 0, `json.validate.enable: false`, graines inchangées ; `essais/env-11/qemu-gra2` non régénéré (BSP absent exprès, essai GRA-2 : code 1 comme avant) |

## 4. Essai VSCodium (mode mixte, `essais/env-11/qemu`)

| # | Essai | Résultat |
| --- | --- | --- |
| 1 | Graine : `backend` → `xyz` sans enregistrer | conforme : 2 erreurs `lepton` (champ absent sur `{`, champ non autorisé sur la clé), aucun avertissement ; disparues à l'annulation |
| 2 | Manifeste noyau (trunk) : virgule supprimée | conforme : « JSON mal formé » situé, puis effacé |
| 3 | Complétion et survol dans la graine | conforme (observation L4-1) |
| 4 | XML : `<inconnu/>` sans enregistrer | conforme : erreur lemminx seule, sans doublon |
| 5 | Graine : `"bsp": "absent"` enregistré | conforme : erreur GRA-2 sur la valeur dans *Problèmes* |
| 6 | Palette « Lepton : vérifier » dans cet état | conforme : « 1 anomalie(s), voir Problèmes », *Problèmes* ouvert, clic → graine (L3-5 fermé) |
| 7 | Retour à `qemu-mps2-an386` enregistré, « vérifier » | conforme : erreur effacée, « terminé » |
| 8 | `lepton.diagnostics.enabled` faux (Utilisateur) | conforme : aucune erreur à la saisie ; rétablie au retour du réglage |

État après l'essai : graine `107cd57` propre, `lepton check` code 0, réglage revenu au défaut.

CFG-7 : erreur signalée à la saisie pour les manifestes JSON (lepton) et le XML (lemminx) —
conforme sans réserve ; la tâche « lepton : vérifier » reste disponible.

## 5. Observations

| Id | Constat | Proposition |
| --- | --- | --- |
| L4-1 | Sur le Mac de l'utilisateur, Ctrl+Espace ouvre Spotlight (raccourci système) au lieu de la complétion | Documenter ⌥Échap, Ctrl+I ou « Déclencher la suggestion » ; aucun changement |
| L4-2 | `json.validate.enable: false` coupe aussi la validation intégrée des autres JSON de l'espace (décision 2, effet accepté) | Laissé |
| L4-3 | Un manifeste ouvert sous le chemin d'un clone (et non du trunk) garde les diagnostics de la saisie après enregistrement ; le contrôle complet les rapporte sous le chemin du trunk (PA-1 : ouverture par le trunk) | Laissé |
