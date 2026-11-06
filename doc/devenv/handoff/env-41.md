# Passation ENV-41 — Famille STM32F4 : copie d'ENV-34 remplacée par la projection — session du 2026-11-06

## Statut
terminée — la HAL v1.8.5 et le CMSIS device F4 3c77349 ne sont plus copiés dans `family-stm32f4xx` :
la famille porte leur projection scion (sources = miroirs) ; rien de compilé n'a changé ; publié.

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `main` | fusion de `devenv/env-41` (fc28997, puis commit de cette passation), poussée avec `devenv/env-41` | oui |
| `family-stm32f4xx` (`<ROOTSTOCK>/depots/lepton/family-stm32f4xx/master`) | `master` | 7afd7f1 « Fusion de devenv/env-41 (ENV-41 HAL v1.8.5 et CMSIS device F4 projetés…) », poussée avec `devenv/env-41` (dfb4528) | oui |
| clones tiers `<ROOTSTOCK>/depots/tiers/stm32f4xx-hal-driver/v1.8.5`, `…/cmsis-device-f4/3c77349…` | HEAD détachée b6f0ed3, 3c77349 | origine = miroirs `lepton-distribution/mirror-*`, `blob:none` | oui |
| clone noyau `depots/lepton/original/master` | `master` | 885696c (non touché) | oui |
| graine `original-tree`, BSP, seed.scions | — | non touchés | oui |

`<ROOTSTOCK>` : 3982 liens, SHA-256 de la liste `d9f4ea56cc06…` (avant : `05b15192…`, mêmes chemins),
206 cibles sous `depots/tiers/`, 0 fichier régulier, 0 lien cassé ; liste greffée 16 entrées, dont
2 à 6 colonnes. Installés : scion 0.6.1.0, lepton (pipx, `devenv/env-41`, exige scion ≥ 0.6.1.0),
extension Lepton 0.5.2 dans VSCodium.

## Fait pendant la session
- §1 audit sur une copie (rapport §1) : `check` cassé (sources cherchées dans le clone famille),
  `seed status/tree`, `file owner`, `generate`, extension faux sans erreur ; hook et skill
  renvoyaient au clone tiers. PA-69 tranché.
- §2 oracle avant `oracles/env-41-avant/` = `env-37-avant`.
- §3 famille : 5218b05 (porteur `scion/.scion/`), a8c7131 et ec15c06 (`git rm`, mécaniques),
  dfb4528 (provenances, description). lepton-tools : 4280c7f (lepton + `tests/test_projection.py`),
  c27fc54 (extension 0.5.2 et `.vsix`), 7a26948 (hook, skill), a1b7b36 (`scripts/tiers/`).
  `pytest` 243 réussis ; `npm test` 22/22 ; hook 10 cas conformes.
- Copie d'essai puis rootstock neuf `essais/env-41-vierge` conformes (rapport §3.3, §3.4) ;
  `<ROOTSTOCK>` basculé avec accord PA-P (§3.5) ; espace de travail identique.
- §4 oracle après `oracles/env-41-apres/` : code 0 ×16, host 7/7, mklepton identiques, `ctest -N`
  17/17, bancs KAL identiques ; aucun `depots/tiers` dans les 4 binaires F4.
- PA-70 : fusions et push, lepton-tools puis famille.

## Reste à faire dans l'étape
- [x] Rien. Pour ENV-43 (graines de projet et rootstocks qui greffent la famille F4) :
  - Mac : `essais/env-13-vierge` (`original-tree`) et `essais/env-11/f429zi` (graine `env11f4`,
    famille `master`) : clone famille encore à 0fd8b2a ; `graft-update` (PA-P) avec scion 0.6.1.0,
    qui clonera les 2 dépôts tiers depuis les miroirs ; contrôle : 206 cibles sous `depots/tiers/`.
  - VM : scion 0.5.4.0 → installer scion 0.6.1.0 et lepton **avant** toute regreffe d'un rootstock
    qui greffe la famille F4 ; sinon la famille est greffée sans HAL (compilation en échec).
  - Extension 0.5.2 à installer sur la VM ; table clone tiers → trunk non observée en session de
    débogage réelle (rapport §4.4).

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Plan de session (audit → PA-69, oracle, bascule copie puis `<ROOTSTOCK>`, contrôles → PA-70) | utilisateur | oui (journal) |
| PA-69 : lignes du §1.1 ; provenances conservées et réécrites ; `SCION_MIN_VERSION` 0.6.1.0, rien ici pour les scion anciens ; lepton **périmètre complet** ; hook, skill, scripts selon §1.5 | utilisateur | oui |
| PA-P : bascule de `<ROOTSTOCK>`, pipx de lepton, extension 0.5.2 installée | utilisateur | oui |
| PA-70 : lepton-tools puis famille ; `env-41-audit` et `env-41-copie` supprimés, `env-41-vierge` gardé | utilisateur | oui |
| Commits de la famille faits dans la copie puis repris dans `<ROOTSTOCK>` par `fetch` + `--ff-only` | choix de session | oui (rapport §3.1, §3.5) |
| Table clone tiers → trunk tirée des liens du trunk (pas de relecture des motifs) | choix de session | oui (rapport §3.2) |
| `file add` dans un répertoire partagé avec une clé projetée : le seul greffon ordinaire est choisi | choix de session | oui (rapport §3.2) |
| `seed lock --restore` ne déplace jamais un clone tiers, signale l'écart (code 1) | choix de session | oui (rapport §3.2) |
| En-tête généré par `hal_conf_stm32f4.py` inchangé (les `stm32f4xx_hal_conf.h` des BSP ne bougent pas) | choix de session | oui (rapport §3.2) |
| Rootstock neuf depuis une graine d'essai locale (famille en `file://` de la branche) | interprétation du fichier d'étape (§4 « graine de la branche ») | oui (rapport §3.4) |

## Pièges rencontrés
- Le hook lit le texte des commandes : un heredoc ou un script en ligne qui contient `trunk/` ou
  `depots/tiers/` après un verbe d'écriture (`install`, `cp`…) est refusé → écrire le script dans un
  fichier du scratchpad, puis l'exécuter.
- `git rm` du `.vsix` supprime `extension/dist/` ; `vsce package --out dist/` écrit alors un fichier
  nommé `dist` → recréer le répertoire avant `npm run package`.
- La fixture `project` de `tests/conftest.py` fait échouer `lepton check` (script de liens du BSP
  factice absent) : un test de `check` ne vise que ses propres anomalies.
- `_info` de lepton écrit sur stdout, pas sur stderr.
- Empreintes `.bin` : différentes à chaque construction à neuf pour tous les presets (non
  reproductible) ; seuls sections et symboles décident.
- `DEVENV-STATUS.md` dépasse 200 Ko : le lire par sections.

## Critères de validation
- [x] PA-69 et PA-70 tranchés et consignés.
- [x] Binaires identiques sur host et les 16 presets (code 0).
- [x] Liste des chemins du trunk identique, aux écarts accordés près (aucun écart).
- [x] Plus aucun fichier de la HAL ni du CMSIS device F4 dans le clone `family-stm32f4xx`.
- [x] Fichiers projetés identiques octet pour octet à `v1.8.5` et à `3c77349`.
- [x] Rootstock neuf conforme depuis la graine de la branche.

## Reprise
Commande ou première action de la session suivante :
```
démarre la session   # ENV-42 : lire cette passation, etapes/ENV-42-core-cm4.md ; PA-71 ; clone noyau master 885696c ; dernier oracle Mac oracles/env-41-apres/
```
