# Passation ENV-12 — Extension VSCodium (phase 2) — session du 2026-10-28 (renvoi R1 : D-b)

## Statut
terminée (2026-10-28) ; renvoi R1 (D-b) terminé le 2026-10-28 — `lepton check` d'un manifeste de
greffon sans `type` ne rend que l'erreur du discriminant ; champ interdit pour le type nommé, situé
et en français. Aucun renvoi ouvert. Passation précédente (lot 6 S3) : historique git de ce fichier
(c5a3852) et `rapports/env-12-bilan.md`.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `devenv/env-12-r1` (depuis `main` e8a9d9a), fusionnée `--no-ff` dans `main` après ce commit, les deux poussées (PA-P) | `devenv(env-12-r1): état et passation` ; avant : 4e636aa validation et tests, e2e6cf8 schéma | oui |
| clone noyau `~/lepton/depots/lepton/original/master` | `master` 16a331b | non touché | oui |
| seed.scions | `master` f1d1f3c (tag 0.5.1.1) | non touché | oui |
| lepton (pipx, Mac) | `~/.local/bin/lepton` | `pipx install --force` depuis 4e636aa | — |
| lepton (Debian) | 0.1.0 depuis 0b4e96e | non réinstallé (D-b non revalidé sur la VM, comportement indépendant de l'hôte) | — |

## Fait pendant la session
- Cause de D-b établie : (1) `type` absent → chaque `if {"properties": {"type": {"const": …}}}` vrai
  par vacuité, tous les `then` appliqués (≈ 20 anomalies) ; `type` inconnu : déjà 1 anomalie (`enum`) ;
  (2) jsonschema 4.26 émet l'erreur d'un schéma `false` sans nom ni chemin du champ
  (`validator=None`, chemin de schéma terminé par `properties`, `$ref` omis) → `/`, message anglais,
  y compris sur un manifeste dont le `type` est valide.
- e2e6cf8 `schemas/greffon.schema.json` : `"required": ["type"]` dans les 9 `if` sur `type`
  (5 types de greffon, 4 types d'option) ; langage accepté inchangé (`type` requis à la racine et dans
  une option) ; exemples invalides : anomalies identiques avant / après (diff vide).
- 4e636aa `lepton/validation.py` : `_forbidden_keys` (champs `false` retrouvés dans le schéma, références
  locales `#/$defs/…` comprises, et dans l'objet), une anomalie par champ, pointeur `/<champ>`, située
  sur la clé, « champ non autorisé pour le type « <type> » : <champ> », dédoublonnée ; `_message` :
  `anyOf` / `oneOf` → « champ obligatoire absent : openocd et sonde, ou qemu » (branches de `required`
  seuls) ou « valeur ne correspondant à aucune des formes admises ».
- Tests `tests/test_diagnostics.py` : `test_scion_without_type_single_anomaly`,
  `test_scion_field_forbidden_for_type`, `test_invalid_examples_messages_translated` ; rouges sans la
  correction (schéma ou code), verts avec ; `pytest` complet 195 verts (deux passes, la seconde sur le
  code final).
- Contrôles : exemples valides de `schemas/exemples/` conformes ; 8 `lepton-greffon.json` de
  `~/lepton/depots` conformes ; graines d'essai `essais/env-11/{qemu,f429zi,wl55jc1}` et
  `essais/env-9` : `lepton check` 0. `~/lepton` : `lepton check` 1 « manifeste de graine absent
  (graine hors lepton) », identique avec le lepton d'avant la correction (graine de la migration).
- Bilan `rapports/env-12-bilan.md` §3 (D-b corrigé), §2 (CFG-7), §7.

## Reste à faire dans l'étape
- Rien.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Traiter D-b plutôt que réviser le plan | utilisateur | oui |
| Correction par le schéma (`required` dans les `if`) + traduction du schéma `false` ; PA-3 non rouvert (langage inchangé) | utilisateur (plan accepté) | oui |
| Traduction d'`anyOf` / `oneOf` | proposition de la session, acceptée avec le plan | oui |
| Extension aux 4 `if` des types d'option (même défaut, même correction) | proposition de la session, appliquée (signalée) | oui |
| Fusion `--no-ff` dans `main`, push de `devenv/env-12-r1` et `main` (PA-P) | utilisateur | oui |

## Observations (non décidées)
- O-r1 : `minProperties` non traduit (« {} should be non-empty », exemple
  `invalides/graine-option-greffon-vide.json`) ; d'autres mots-clés peuvent rester en anglais
  (`_message` ne couvre que les plus courants). Proposition : traduire au besoin.

## Pièges rencontrés
- jsonschema omet `$ref` du chemin de schéma : l'erreur de `sans_champ_materiel` paraît sous
  `allOf/3/then/properties`, dont les `properties` propres ne contiennent pas le champ → suivre le
  `$ref` du même nœud.
- zsh : `echo ====…` échoue (« = » en tête de mot = expansion de commande) ; citer la chaîne.

## Critères de validation
- [x] `type` absent : une seule anomalie, « champ obligatoire absent : type ».
- [x] Aucun « False schema does not allow » ni « is not valid under » sur les exemples invalides.
- [x] Champ interdit situé sur sa clé (diagnostic de l'éditeur à la bonne place).
- [x] `pytest` vert (195).

## Reprise
```
cd /Users/cle_d_anton/lepton-tools-dev/lepton-tools && claude
# Chantier terminé (ENV-0 à ENV-12, renvoi D-b fermé). Suite sur décision de l'utilisateur
# (skill lepton-portage-instructions) ; observation O-r1 ci-dessus.
# Tests de lepton : ~/lepton-tools-dev/venv-lepton-tools/bin/python -m pytest -q (≈ 5 min)
```
