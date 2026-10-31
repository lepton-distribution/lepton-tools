# ENV-16 — Graine de référence et `lepton check` : rapport

Session du 2026-10-31, hôte Mac. lepton 0.1.0 (pipx, depuis `devenv/env-15` 1e65851), scion 0.5.2.0.

## 1. Audit (tâche 1, lecture seule)

### 1.1 Contrôle actuel
- `lepton/checks.py` `check_rootstock` : contrôle du trunk (FIC-3), manifestes de greffons
  (schéma, options, fichiers déclarés), `check_dependencies` (GRF-5 : dépendances déclarées, noms
  uniques), puis graine. Graine sans `lepton-graine.json` → anomalie « manifeste de graine absent
  (graine hors lepton) » et arrêt : `check_seed` (GRA-2, GRF-5 cœur et backend, CFG-4), XSD et
  CFG-5 du XML ne sont pas exécutés.
- Code de retour (`rapports/env-8-interface.md` §2) : 1 dès qu'une anomalie est trouvée ; les
  avertissements `lepton: attention:` ne changent pas le code (cas O5).
- `schemas/graine.schema.json` : `projet`, `noyau`, `bsp`, `backend`, `configurations`,
  `mklepton_xml` requis ; un BSP, un backend, un XML ; `additionalProperties: false`.

### 1.2 Lecteurs du manifeste de graine
| Lecteur | Sans manifeste (cas de `<ROOTSTOCK>` aujourd'hui) | Champs lus |
| --- | --- | --- |
| `check` | anomalie, code 1 | tous |
| `seed status` (`status_data`) | code 0 ; « rôles non déterminés (graine hors lepton) » ; rôle = type du manifeste du greffon | `projet.nom`, `noyau`, `bsp`, `applications`, `bibliotheques`, `backend`, `mklepton_xml`, `configurations` |
| `seed tree`, extension (vue, palette) | via `status_data` : `configurations` vide, rôles = types | idem |
| `tree._presets` (`file owner`) | liste vide | `projet.nom`, `configurations` |
| `generate` (`Context`) | refus : « absent : la graine n'est pas une graine lepton » | `projet`, `bsp`, `configurations`, `options` |
| `seed config add/remove`, `seed add/remove/replace`, `scion add` (état laissé), `seed lock` | refus (`load_graine`) ou greffon projet non exclu | `projet.nom`, `bsp`, listes, `mklepton_xml` |
| extension, diagnostics | aucun fichier à valider | schéma du fichier |

Tous ces lecteurs accèdent aux champs de graine de projet par indexation directe (`graine["bsp"]`,
`graine["projet"]["nom"]`, 37 accès) : un manifeste d'un autre type les ferait échouer
(`KeyError`) tant qu'ils ne sont pas adaptés, y compris dans les lepton déjà installés (Debian).

### 1.3 Inventaire de `original-tree` (0f1275a)
- `.scion.sources.list` : `original::tree` (noyau `lepton-noyau`), `building` (local, sans
  manifeste), familles `qemu-mps2`, `stm32f4xx`, `stm32wlxx`, BSP `qemu-mps2-an386`,
  `qemu-mps2-an500`, `nucleo-f429zi`, `nucleo-wl55jc1`. Pas de répertoire `project/` (aucun greffon
  local de projet), pas de `lepton-graine.json`.
- Presets du noyau (`CMakePresets.json`) : `host` + 14 presets croisés ; backend par preset
  (`embos` / `freertos`, `LEPTON_KAL_BACKEND`) ; 3 XML (`LEPTON_MKCONF`) :
  `mkconf_tauon_basic_qemu_mps2.xml` (an386, an500), `…_nucleo_f439zi.xml` (nucleo-f429zi),
  `…_nucleo_wl55jc1.xml`. 4 presets visent des BSP non greffés (`stm32f746g-disco-*`,
  `samd21-xplained-pro-*`, sans `LEPTON_MKCONF`).
- Mesure en lecture seule des contrôles qu'une graine de référence pourrait recevoir
  (`check_mkconf_provided`, `validate_xml`, cœurs) : chaque BSP greffé a sa famille greffée, son
  cœur dans les cœurs de sa famille et du noyau (GRF-5) ; les 3 XML : XSD 0 anomalie, CFG-5
  0 anomalie.

### 1.4 Relevé de référence (avant toute modification)
Sorties complètes : scratchpad de session `avant/` (non versionné) ; résumé :

| Rootstock | `check` | Contenu | `seed status` |
| --- | --- | --- | --- |
| `<ROOTSTOCK>` | 1 | 1 anomalie : manifeste de graine absent | 0 |
| `essais/env-13-vierge` | 1 | même anomalie | 0 |
| `essais/env-9` | 0 | 5 fichiers conformes | 0 |
| `essais/env-11/f429zi`, `qemu`, `wl55jc1` | 0 | 5 fichiers conformes | 0 |
| `essais/env-11/qemu-gra2` | 1 | BSP non greffé (GRA-2) + 3 pilotes CFG-5 (essai de refus voulu) | 1 |
| `essais/env-11/bout-en-bout/rootstock` | 0 | 5 conformes, avertissement O5 | 0 |

Toutes les graines de projet ont `lepton-graine.json` ; toutes sauf `bout-en-bout` (antérieure à
ENV-9) ont `project/`.

### 1.5 Options (PA-19)
| | A — manifeste de référence dans `original-tree` | B — graine de référence reconnue sans manifeste | C — B + contrôles de référence déduits des greffons |
| --- | --- | --- | --- |
| Critère | champ `type: "reference"` du manifeste | pas de `lepton-graine.json` **et** pas de `project/` dans la graine | idem B |
| Schéma | étendu : branche `reference` (`noyau`, `bsps`, `backends`, `mklepton_xml` multiples) ; branche projet inchangée | inchangé | inchangé |
| `check` | contrôles GRA-2/GRF-5 par BSP, XSD et CFG-5 par XML | information, code 0 ; aucun contrôle de graine | information ; GRF-5 par BSP greffé ; XSD + CFG-5 des XML cités par les presets du noyau dont le BSP est greffé ; presets à BSP non greffé : information |
| Autres lecteurs | tous à adapter (`status`, `tree`, `generate`, `config`, `seed add/remove`, `lock`, `scions`) ; refus explicite des commandes de projet | inchangés (message « hors lepton » de `seed status` ajustable) | idem B |
| Graine publiée | commit + push d'`original-tree` (PA-P) ; tout rootstock la reçoit à sa mise à jour ; lepton antérieur → `KeyError` (réinstallation Debian) | inchangée | inchangée |
| Graine de projet sans manifeste | anomalie conservée | anomalie conservée (`project/` présent) | idem |
| Coût | élevé | faible | moyen |

Proposition non validée : C.

PA-19 (2026-10-31, décision de l'utilisateur) : option C ; presets à BSP non greffé : information.

## 2. Implémentation (tâche 2)
Branche `devenv/env-16` de lepton-tools (depuis `main` 08adee9) ; schémas et graine `original-tree`
inchangés (aucun commit de schéma ni de graine).

| Commit | Objet |
| --- | --- |
| d7b814c | `lepton/checks.py` : `check_bsp` (famille et cœur d'un BSP, extrait de `check_seed`, messages identiques ; ordre : famille et cœur avant les configurations), `_xml_anomalies` (XSD + CFG-5, partagé), `kernel_presets` (presets visibles, `inherits` résolu, premier parent prioritaire), `check_reference_seed` ; `check_rootstock(rs, warn, info)` ; `KERNEL_PRESETS` déplacé de `generate.py` ; `cli.py` : `_note` → `lepton: information:` sur stderr |
| a0e58cb | `tests/test_milestone6.py` : rootstock de référence greffé par scion seul (`_reference`) ; conforme (code 0, information, fichiers contrôlés) ; anomalies GRF-5 par BSP, CFG-5 limité aux BSP du XML (avec contre-épreuve), `LEPTON_MKCONF` absent ; graine de projet sans manifeste refusée ; graine de projet invalide refusée |
| 6a40859 | `rapports/env-8-interface.md` §3.9, docstring de `checks.py` |

- Critère de graine de référence : ni `lepton-graine.json` ni `project/` dans la racine de la graine.
- Sortie `--json` inchangée dans sa forme (`files`, `anomalies`) ; les informations ne vont que sur
  stderr (préfixe `lepton: `, exclu du filtre de la tâche « lepton : vérifier »).
- Non modifiés (hors décision) : message « graine hors lepton » de `seed status`, refus de
  `generate`, `seed config`, `seed add/remove` sur une graine sans manifeste.
- `pytest` : 202 verts (198 + 4) ; `scripts/valider-schemas.sh` : conforme ; lepton réinstallé
  par `pipx install --force` depuis `devenv/env-16` 6a40859 (version 0.1.0 inchangée).

## 3. Contrôles (tâche 3)
lepton installé (pipx) ; comparaison octet à octet avec §1.4 (`check`, `check --json`,
`seed status`) :

| Rootstock | `check` avant → après | Sorties | `seed status` |
| --- | --- | --- | --- |
| `<ROOTSTOCK>` | 1 → **0** | 12 fichiers conformes (8 manifestes, presets du noyau, 3 XML) ; informations : graine de référence, BSP `samd21-xplained-pro` et `stm32f746g-disco` non greffés (4 presets) | identique (0) |
| `essais/env-13-vierge` | 1 → **0** | idem | identique (0) |
| `essais/env-9`, `env-11/f429zi`, `qemu`, `wl55jc1`, `bout-en-bout/rootstock` | 0 → 0 | identiques | identiques |
| `essais/env-11/qemu-gra2` | 1 → 1 | identiques (4 anomalies voulues) | identique (1) |

- `seed tree --json` sur `<ROOTSTOCK>` : code 0 (`tree.py` non modifié).
- `generate` : code non modifié (refus sur graine sans manifeste) ; non exécuté sur `<ROOTSTOCK>`
  (écrit l'espace de travail).
- Extension : consomme `check --json` et `seed status --json`, de forme inchangée ; non relancée.
- Graine de projet invalide refusée : tests `test_check_graine_projet_sans_manifeste_refusee`,
  `test_check_graine_projet_invalide_refusee`.

## 4. Points restants
- PA-20 : push de `devenv/env-16` (lepton-tools), fusion dans `main` ; pas de push de graine
  (option C).
- Debian : lepton non réinstallé depuis `devenv/env-16` ; aucune validation Debian prévue par
  l'étape.
