# ENV-71 — Miroirs de conservation : synchronisation (D40)

Session du 2026-11-24 (Mac). scion 0.6.3.4 ; git 2.50.1 ; `gh` authentifié ;
`url.ssh://git@github.com/.pushinsteadof https://github.com/` (réglage global, PA-68) présent.

## 1. Relevé sans `mirror-sync` (2026-11-24 14:36 +0100)

Relevés bruts : `env-71-miroirs/ls-remote/{amont,miroir}-<nom>.txt` (`LC_ALL=C git ls-remote`,
`refs/pull/*` de l'amont retirés), `env-71-miroirs/amont-commits.txt` (`gh api …/compare`,
`…/git/tags`). Seules `refs/heads/*` et `refs/tags/*` entrent dans le plan de scion
(`<SEED_SCIONS>/scion/mirror.py:32-34`).

### 1.1 Références à envoyer (liste du jour)

| Miroir | Référence | Miroir → amont | Commit(s) de l'amont (date committer, titre) | `compare` |
| --- | --- | --- | --- | --- |
| `mirror-cmsis_device_f4` | `master` | 9192c7b → 8c79dcf | 8c79dcf 2026-11-18 « Release v2.6.12 » | ahead 1, behind 0 |
| | tag `v2.6.12` (nouveau) | — → b760711 (annoté, → 8c79dcf) | tag du 2026-11-18 « Release v2.6.12 » | — |
| `mirror-stm32f7xx-hal-driver` | `master` | e860c4f → e879045 | e879045 2026-11-19 « Release v1.3.4 » | ahead 1, behind 0 |
| | tag `v1.3.4` (nouveau) | — → a91a972 (annoté, → e879045) | tag du 2026-11-19 « Release v1.3.4 » | — |
| `mirror-cmsis_device_f7` | `master` | 2352e88 → 52e4aad | 52e4aad 2026-11-19 « Release v1.2.11 » | ahead 1, behind 0 |
| | tag `v1.2.11` (nouveau) | — → 15393cd (annoté, → 52e4aad) | tag du 2026-11-19 « Release v1.2.11 » | — |
| `mirror-stm32wlxx-hal-driver` | `main` | 5c87cf0 → e388844 | e70dfa4 2026-11-19 « [HAL][RTC] Resolve unsigned arithmetic warning in RTC BCD conversion » ; e388844 2026-11-23 « Release v1.7.0 » | ahead 2, behind 0 |
| | tag `v1.7.0` (nouveau) | — → 6a7fb43 (annoté, → e388844) | tag du 2026-11-23 « Release v1.7.0 » | — |
| `mirror-stm32-mw-subghz-phy` | `main` | 7dc059f → 47c14de | 47c14de 2026-11-23 « Release v1.5.2 » | ahead 1, behind 0 |
| | tag `v1.5.2` (nouveau) | — → f95249e (annoté, → 47c14de) | tag du 2026-11-23 « Release v1.5.2 » | — |
| `mirror-STM32CubeWL` | `main` | f934cd2 → 2259ce0 | 2259ce0 2026-11-20 « [HAL] Upload new fixes » | ahead 1, behind 0 |

À jour : `mirror-stm32f4xx-hal-driver` (l'amont a en plus `refs/for/master` e082595, hors
`heads`/`tags`, ignoré par scion), `mirror-cmsis-device-wl`.

Total : **11 références sur 6 miroirs** (6 branches, 5 tags nouveaux).

### 1.2 Règles M-* (avance rapide, tags nouveaux)
- Chaque branche : le commit du miroir est un ancêtre de celui de l'amont (`status` = `ahead`,
  `behind_by` = 0) : avance rapide.
- Chaque tag à envoyer est absent du miroir ; aucun tag du miroir ne diffère de l'amont ni n'en
  est absent (aucune ligne `<` sur `refs/tags/` dans les différences).
- Chaque référence s'explique par une publication de l'amont (commits et tags datés ci-dessus).

### 1.3 Écart à R66-1 (2026-11-19 : 7 références sur 4 miroirs)
- `mirror-stm32wlxx-hal-driver` : `main` va à e388844 (et non plus e70dfa4) ; tag `v1.7.0` en plus.
- `mirror-stm32-mw-subghz-phy` : nouveau, `main` et tag `v1.5.2` (2026-11-23).
- `mirror-STM32CubeWL` : nouveau, `main` (2026-11-20), sans tag.
- F4 et F7 : identiques à R66-1.

Conséquence hors de l'étape : des versions WL nouvelles sont publiées (HAL `v1.7.0`, SubGHz_Phy
`v1.5.2`) ; les projections WL restent épinglées (`v1.6.0`, `v1.5.0`, STM32CubeWL `v1.6.0`) ; aucun
ticket de montée de version WL n'existe (D40 ne vise que F7 et F4). Point écarté, présenté au PA-129.

### 1.4 Lieu des dépôts de travail
- `<ROOTSTOCK>/depots/.mirrors/` : absent.
- `essais/env-13-vierge/depots/.mirrors/github.com/lepton-distribution/` : 8 dépôts, 77 Mo ; ses
  3 `.scion.mirrors` sont identiques à ceux de `<ROOTSTOCK>` (familles F4 acdd24c, F7 12280a5,
  WL 9349be2 dans les deux).
- `sync_one` (`mirror.py:266-289`) clone le dépôt de travail absent, réécrit sa configuration
  (`_configure`) et lance `fetch --prune` du miroir et de l'amont avant de tester `dry_run` : la
  passe à blanc écrit dans le lieu choisi.

## 2. PA-129 (2026-11-24)
Décisions de l'utilisateur : dépôts de travail dans `<ROOTSTOCK>` ; envoi accordé pour les
6 miroirs (11 références), lancé par l'utilisateur ; tickets cités :
lepton-distribution/lepton-famille-stm32f7xx#1 (HAL v1.3.4, CMSIS device v1.2.11) et
lepton-distribution/lepton-famille-stm32f4xx#1 (CMSIS device v2.6.12), ouverts ; point écarté
D43 (versions WL nouvelles) : ticket sur `family-stm32wlxx` ; aucune session VM active.

## 3. Trunk avant
`env-43-mac/controler-trunk.py ~/lepton` contre `env-50-mac/attendu/trunk-liens.txt` : code 0,
`CONFORME` (3889 liens, 0 fichier régulier, 0 lien cassé, 629 projetés, 8 clones tiers à leur
commit, `modifs 0`, `blob:none`) — `env-71-miroirs/trunk-avant/`. `lepton check` : code 0
(19 fichiers conformes).

## 4. Passe à blanc
`LC_ALL=C scion mirror-sync --dry-run -v ~/lepton`, lancée par la session : code 0
(`env-71-miroirs/dry-run-1.txt`).
- Les 8 dépôts de travail sont créés sous `<ROOTSTOCK>/depots/.mirrors/github.com/lepton-distribution/`
  (`clone --mirror`), 85 Mo, dont `mirror-STM32CubeWL.git` 65 Mo.
- Bilan : F4 HAL 0, `cmsis_device_f4` 2, `stm32wlxx-hal-driver` 2, `cmsis-device-wl` 0,
  `stm32-mw-subghz-phy` 2, `STM32CubeWL` 1, `stm32f7xx-hal-driver` 2, `cmsis_device_f7` 2 :
  11 références, 0 signalement ; chaque branche contrôlée par `merge-base --is-ancestor`.
- Le résultat est **égal au §1.1**, référence pour référence, commits compris.
- Trunk après la passe : 0 fichier régulier, 0 lien cassé ; clone noyau propre.

## 5. Envoi (PA-P, accordé au PA-129)
Lancé par l'utilisateur dans la session : `! LC_ALL=C scion mirror-sync -v /Users/cle_d_anton/lepton`.
Un premier essai, `!` précédé d'un caractère, est arrivé comme message sans être exécuté
(`ls-remote` des 6 miroirs : têtes inchangées) ; le second a été exécuté.
- 6 `git push --porcelain` (un par miroir, références nommées `refs/amont/…:refs/…`), par SSH
  (`pushInsteadOf`) ;
- **11 références envoyées, 0 signalement** ; stderr vide. Code de retour non affiché par le mode
  `!` ; le bilan sans signalement et le §6 valent constat de réussite.
- Journal : `env-71-miroirs/envoi.txt` (extrait de la sortie affichée).

## 6. Contrôles → PA-130
| Contrôle | Résultat |
| --- | --- |
| `LC_ALL=C scion mirror-sync --dry-run -v ~/lepton` | code 0 ; **0 référence à envoyer** sur les 8 miroirs, 0 signalement (`env-71-miroirs/dry-run-2.txt`) |
| `git ls-remote` des 8 miroirs | `refs/heads/*` et `refs/tags/*` (`^{}` compris) identiques à l'amont du §1 (`env-71-miroirs/ls-remote-apres/`) |
| Réécriture d'un miroir | aucune : branches en avance rapide (`merge-base --is-ancestor`, `compare` `ahead`), tags nouveaux seulement |
| `controler-trunk.py ~/lepton` | code 0, `CONFORME` ; `liens.txt` avant = après (`cmp`, SHA-256 5dbbc69f…, = `oracles/env-49-apres`), contrôles identiques (`env-71-miroirs/trunk-apres/`) |
| `lepton check` | code 0 (19 fichiers conformes) |
| Clone noyau | propre |
| `<ROOTSTOCK>/depots/.mirrors/` | 8 dépôts de travail, 85 Mo, gardés (passes suivantes depuis `<ROOTSTOCK>`) |

Pour ENV-72 : le `mirror-sync --dry-run` de la VM doit donner 0 référence à envoyer, sauf nouvelle
publication de l'amont après le 2026-11-24 14:36 +0100.
