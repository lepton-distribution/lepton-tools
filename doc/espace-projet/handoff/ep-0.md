# Passation EP-0 — Essai VSCodium : espace ouvert par un lien du trunk ; plusieurs rootstocks — session du 2026-11-26

## Statut
terminée — essais (a), (b), (c) et constat du besoin 2 faits sur macOS ; PA-E1 clos ; plan révisé
et relu ; branche non fusionnée.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `espace-projet/ep-0` (depuis `main` cf34908) | commit de fin de session « espace-projet(ep-0): état et passation » (seul commit de la branche) | oui après commit ; non fusionnée, non poussée |
| clone noyau `depots/lepton/original/master` | `master` | 0c2e43e Fusion de devenv/env-70 | oui (inchangé) |
| `<SEED_SCIONS>` | `master` | 929c01a Fusion de devenv/env-70 | oui (inchangé) |
| graine de référence `depots/lepton-seed.scions/original-tree` | `original-tree` | 15740f9 Fusion de devenv/env-20 | oui (inchangé) |
| essais | — | `essais/ep-0/` supprimé (`scripts/supprimer-essai.sh`, rc 0) ; `essais/env-9` et `essais/env-11/qemu` non modifiés | — |

## Fait pendant la session
- Copies sans `build/` (`rsync -a --exclude=/build/ --exclude='/*.log'`) de `essais/env-9` et
  `essais/env-11/qemu` ; `lepton check` et `lepton generate` rc 0 dans chacune.
- Variantes `V-lien`, `V-cible`, puis `V-c` à `V-c6` du fichier d'espace déposées dans le clone de
  la graine de la copie, greffées par lien (`trunk/sys/user/env9/env9.code-workspace`).
- Essai (a) : résolution des `folders` depuis le chemin d'ouverture ; Finder et menu résolvent le
  lien (rapport §2).
- Essai (c) : tableau réglage par réglage (rapport §3).
- Essai (b) : écriture à travers le lien, sur place, lien conservé (rapport §4).
- Besoin 2 : deux rootstocks, deux fenêtres, sans interférence (rapport §5).
- Rapport : `doc/espace-projet/rapports/ep-0-essai-lien.md`.
- PA-E1 clos ; plan révisé (EP-1, EP-2, EP-3, EP-4, EP-5, EP-8, ORCHESTRATION §4 et §5, CADRAGE §4
  à §7) ; relecture indépendante (23 constats, tous appliqués) ; H6 ajouté à `HORS-PLAN.md`.
- Critères vérifiés : `git diff --stat main -- . ':!doc/espace-projet'` vide ; seed.scions et
  clone noyau `status --short` vides, comme au début.

## Reste à faire dans l'étape
- [ ] Rien dans l'étape. Hors étape : fusion d'`espace-projet/ep-0` dans `main` et push (PA-P),
      à demander à l'utilisateur au début de la session suivante.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans STATUS ? |
| --- | --- | --- |
| PA-E1 (C2) : piste P-a, espace régulier à la racine du rootstock, généré depuis le contenu versionné du greffon projet ; C3 maintenue ; branche « espace dans le greffon projet » de C8 sans objet | utilisateur, sur recommandation de la session | oui |
| PA-E1 (révision du plan) : plan révisé dans la session, relu avant commit ; retouches d'EP-1, EP-2, CADRAGE §4 gardées | utilisateur, sur recommandation de la session | oui |
| PA-E1 (Debian) : preuve Debian à EP-8, critère C7 reformulé | utilisateur, sur recommandation de la session | oui |
| PA-E1 (relevé QEMU) : H6 hors plan | utilisateur | oui |
| PA-E1 (essais) : `essais/ep-0/` supprimé | utilisateur | oui |
| PA-E1 (openocdPath) : vérifié en EP-5 | utilisateur, sur recommandation de la session | oui |
| Pistes P-b et P-c (rapport §6) | propositions non retenues | rapport seulement |
| Mécanismes de portabilité, forme du contenu d'équipe, `json.schemas` | ouverts, PA-E8 | EP-4 §1 |

Tickets créés pendant la session : aucun.

## Pièges rencontrés
- Le hook `proteger-trunk.py` refuse une redirection relative (`> ../x.log`) lancée depuis
  `trunk/` → il juge le chemin écrit relativement au trunk → chemins absolus, sans `cd trunk`.
- Un `${config:}` sans clé dans le **nom** d'une configuration `launch` bloque le lancement
  (« impossible de résoudre la variable ») → VSCodium développe tous les champs texte → aucun
  `${…}` littéral dans un nom.
- Le Finder crée des `.DS_Store` dans le trunk d'une copie parcourue → tolérés
  (`.scion.trunk.tolerated`), retirés par la regreffe suivante.
- La liste des récents de VSCodium n'est pas lisible dans `state.vscdb` pendant que VSCodium tourne
  → relevé visuel par l'utilisateur, et `workspaceStorage/*/workspace.json` pour le chemin retenu.

## Critères de validation
- [x] Rapport `rapports/ep-0-essai-lien.md` : (a), (b), (c) et le constat du besoin 2 ont chacun
      une réponse appuyée d'une preuve, ou la mention « non conclu » avec la raison.
- [x] `git -C <LEPTON_TOOLS> diff --stat main -- . ':!doc/espace-projet'` : vide.
- [x] `git -C <SEED_SCIONS> status --short` et `git -C <ROOTSTOCK>/depots/lepton/original/master
      status --short` : inchangés par rapport au relevé de début de session.
- [x] PA-E1 tranché et consigné dans `STATUS.md` §Décisions.

## Reprise
Commande ou première action de la session suivante :
```
démarre EP-1   (skill espace-projet-session ; d'abord : fusion d'espace-projet/ep-0 dans main et push, sur accord)
```
