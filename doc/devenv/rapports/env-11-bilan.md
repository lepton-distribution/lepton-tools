# ENV-11 — Bilan des exigences — 2026-10-15 (S3)

Sources : `env-11-mac.md` (scénario Mac S1-S2), `env-11-debian.md` (scénario Debian S3), rapports
des étapes antérieures cités. « Conforme (ENV-n) » : non rejoué en ENV-11, preuve de l'étape n.
Hôte Apple Silicon : revue seule (NF-3), hors bilan d'exécution.

## 1. Exigences P1

| Exigence | Mac Intel | Debian | Preuve | Écart |
| --- | --- | --- | --- | --- |
| INS-1 VSCodium sans Marketplace | conforme | conforme (ENV-10) ; 2.1 : à venir | `env-11-mac.md` 2.1 ; `env-10-validation.md`, `env-10-debian.md` | Apple Silicon en revue |
| INS-2 extensions épinglées (`extensions.lst`) | conforme | conforme (ENV-10) | idem | — |
| INS-3 chaîne par `install-*.sh` | conforme | conforme (ENV-10) | idem | — |
| INS-4 idempotent, `--dry-run` | conforme (0 changement) | à venir (2.1) | `env-11-mac.md` 2.1 | — |
| INS-5 gestionnaire par hôte, aucun préfixe | conforme | conforme (ENV-10) | `env-10-validation.md` | Apple Silicon en revue |
| INS-6 scion et lepton | conforme | à venir | `env-11-mac.md` §1 | O12 (lepton non réinstallé à version égale) |
| GRA-1 `seed new` | conforme | à venir (2.2) | 2.2, 5-6 (préparation) | N1 (scion : branche du clone) |
| GRA-2 noyau + BSP obligatoires, graine sans application | conforme | à venir | 2.2 (GRA-2, copie) | O1 (message CMake indirect) |
| GRA-3 greffon git ou local | conforme (git `file://`) | à venir (git `ssh://`) | 2.2 ; local : tests ENV-8 | — |
| GRA-4 ajouter, retirer, remplacer + reconfiguration | conforme (ajout / retrait par `scion new` / `remove`) ; remplacement : tests ENV-8 | à venir | 2.4, 2.8 ; `test_gra4_*` | O3, O4 |
| GRA-6 `seed status` | conforme | à venir | 2.2 | — |
| GRF-1 greffon depuis un modèle | conforme après N3 | à venir | 2.4 | N3 corrigé |
| GRF-2 manifeste JSON, JSON Schema | conforme | à venir | 2.2 (`lepton check`) | — |
| GRF-3 BSP → presets et `launch` | conforme | sans objet (pas de carte) ; presets : à venir | 2.3, 5-6, §2bis B1-B2 | O8 (série de sonde) |
| GRF-4 retrait sans lien orphelin, clone intact | conforme | à venir (2.8) | 2.8 | O4 |
| FIC-1 fichier ajouté / retiré | conforme (ajout) ; retrait : tests ENV-8 | à venir | 2.4 ; `test_fic1_*` | — |
| FIC-2 répertoire | conforme (ENV-8, tests) | — | `test_fic2_dir_*` | non rejoué en ENV-11 |
| FIC-3 création dans le clone, jamais dans le trunk | conforme | à venir | 2.4, fin de scénario | — |
| FIC-4 source découvert sans liste CMake | conforme | à venir | 2.4 | — |
| FIC-5 sauvegarde à travers le lien | conforme (ENV-1) | — | `env-1-essais.md` essai 2 | non rejoué en ENV-11 |
| CFG-1 deux sources sans recouvrement, versionnées dans la graine | écart | — | 2.4 | O5 : XML porté par le greffon noyau (PA-9 Q5), pas par la graine |
| CFG-2 répartition, option → reconfiguration → construction | conforme | à venir | 2.4 (XML), §2bis B3 (preset) | — |
| CFG-3 portée privée / publique | conforme (ENV-5) | — | `env-5-validation.md` greffon d'essai | non rejoué en ENV-11 |
| CFG-4 options typées, valeur hors bornes refusée | partiel | — | `lepton check` (défaut hors bornes refusé, `test_milestone6`) | **N5** : aucune valeur d'option fixable dans la graine (schéma de graine sans `options`) ; seul le défaut est contrôlé |
| CFG-6 presets générés | conforme | à venir | 2.3 | O2 (une configuration par `seed new`) |
| CFG-8 XSD versionné, refus de version inconnue | conforme (ENV-4) | — | `env-4-validation.md` | cpufs automatique non utilisé par les 6 XML (décision ENV-4) |
| BLD-1 bibliothèques et OBJECT | conforme | à venir | 2.3 | — |
| BLD-2 greffon sans modifier le noyau CMake | conforme | à venir | 2.4 | — |
| BLD-3 mklepton hors trunk | conforme | à venir | 2.3 | — |
| BLD-4 ELF, HEX, BIN, MAP, occupation | conforme | à venir | 2.3 | — |
| BLD-5 même empreinte CLI / éditeur | conforme | à venir (CLI) | 2.9, §2bis | — |
| IDE-1 arborescence | conforme | — (éditeur non testé sur Debian) | §2bis B3 | — |
| IDE-2 git multi-dépôts | conforme | — | §2bis B3 | — |
| IDE-3 navigation exacte | conforme avec réserve | — | §2bis B3 | O10 (clangd avant configuration) |
| IDE-4 chemin canonique, point d'arrêt via le trunk | conforme | — | §2bis B1-B3 | écart PA-1 (`fullname` GDB) |
| IDE-5 changement de configuration depuis la barre d'état | conforme avec réserve | — | §2bis B3 | O11 (sélecteur masqué par défaut) |
| DBG-1 QEMU, console intégrée | conforme | — | §2bis B3 | — |
| DBG-2 GDB sous QEMU | conforme | — | §2bis B3 | — |
| DBG-3 flash et débogage sur carte | conforme (F429ZI, WL55JC1 cœur M4) | — | §2bis, 2.5-2.6 | O8, O9 |
| TST-1 banc KAL CLI et éditeur | conforme (18/18) | à venir (CLI) | 2.3, §2bis B3 | — |

## 2. Exigences P2 relevées en passant

| Exigence | Résultat | Écart |
| --- | --- | --- |
| CFG-5 `lepton check` | conforme | O4 |
| CFG-7 validation à la saisie | non conforme | N4 |
| GRA-5, GRF-5, FIC-6 | conformes (ENV-8, tests, bout en bout) | — |
| BLD-6, IDE-6, DBG-4, DBG-5, TST-2 | non testées (hors phase 1 ou ENV-12) | — |

## 3. Classement des défauts et observations

À trancher avec l'utilisateur (renvois proposés : `env-11-mac.md` §3-§4).

| ID | Objet | Renvoi proposé | Décision |
| --- | --- | --- | --- |
| N1 | scion `gitops.clone` sans `checkout` de la version | ENV-7 (correctif, scion 0.5.1.1) | à trancher |
| N4 | CFG-7 : aucune association de schéma | ENV-9 (`xml.fileAssociations`, `json.schemas` générés) | à trancher |
| N5 | CFG-4 : valeurs d'options non fixables dans la graine | ENV-3 (schéma de graine) + ENV-8 (lepton) + ENV-5 (lecteur CMake) | à trancher |
| O1 | message CMake indirect si BSP absent | ENV-6 (lecteur) | à trancher |
| O2 | une configuration par `seed new` | ENV-8 / ENV-12 | à trancher |
| O3 | message de reprise de `scion new` | ENV-8 | à trancher |
| O4 | `scion remove` sans avertissement CFG-5 | ENV-8 | à trancher |
| O5 | XML mklepton dans le greffon noyau (CFG-1) | décision de conception (ENV-8 / ENV-12) | à trancher |
| O6 | `LEPTON_EMBOS_ROOT` non transmis | ENV-10 ou ENV-9 | à trancher |
| O7 | `.DS_Store` recréés | traité par N2 | clos |
| O8 | espace sans série de sonde | ENV-9 | à trancher |
| O9 | `gdbinit-lepton` : bloc Python | noyau | à trancher |
| O10 | clangd avant configuration | ENV-9 / ENV-12 | à trancher |
| O11 | sélecteur de preset masqué | ENV-9 | à trancher |
| O12 | lepton non réinstallé à version égale | ENV-10 (comparaison du commit ou numéro de version) | à trancher |
