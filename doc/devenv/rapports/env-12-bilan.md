# ENV-12 — Bilan de l'extension VSCodium (phase 2) — 2026-10-28

Lot 6, session S3. Sources : `env-12-lot3.md` à `env-12-lot6.md` (Mac, QEMU et cartes),
`env-12-debian.md` (VM Debian, ordre `R12-1`), décisions de `DEVENV-STATUS.md` (2026-10-20 à
2026-10-28). Extension 0.5.1 (`extension/dist/lepton-0.5.1.vsix`), lepton 0.1.0 de `devenv/env-12`.

## 1. Critères de la fiche (`etapes/ENV-12-extension.md`)

| Critère | Mac | Debian | Preuve |
| --- | --- | --- | --- |
| PA-12 tranché | oui (2026-10-20, F0-F8, O5 dans la graine) | — | `DEVENV-STATUS.md` §Décisions |
| Aucune logique de graine ou de greffon dans `extension/` | conforme (revue des 12 modules ; R-1, R-2 mineurs) | — | `env-12-lot6.md` §12 |
| Création depuis l'explorateur : lien dans le trunk sans action manuelle (FIC-1) ; aucun fichier régulier dans le trunk (FIC-3) | conforme | conforme (inotify) | lot 6 §9 ; Debian §2 (F2, F3, L3-4, §6.11) |
| Vue IDE-1 cohérente avec `lepton seed status` | conforme | conforme | lot 5 §4, lot 6 §9 ; Debian §2 (F6) |
| `.vsix` installé par `codium --install-extension` | conforme (`install-vscodium.sh`, 2 puis 0) | conforme (changements 4 puis 0) | lot 6 §4 ; Debian §2 (INS) |

## 2. Exigences et renvois traités

| Exigence ou renvoi | Avant ENV-12 | Après ENV-12 | Fonction, preuve |
| --- | --- | --- | --- |
| FIC-1 (P1) | tâche « regreffer » manuelle | conforme | F2, observateur regroupé ; Mac et Debian |
| FIC-3 (P1) | — | conforme | F3 (`file add --adopt`), L3-4 ; Mac et Debian |
| IDE-1 (P1) | — | conforme | F6, `seed tree` (codemodel du preset actif) |
| IDE-6 (P2) | non testée | conforme | F1, 18 opérations de lepton en palette, français |
| CFG-7 (P2) | JSON en avertissement (reprise 4) | conforme | F5, `check --stdin` ; D-a corrigé (§3) ; D-b corrigé en R1 (§3) |
| CFG-1 / O5 (P1) | écart accepté (XML dans le greffon noyau) | conforme | lot 2, `seed mkconf import` ; graines d'essai migrées (Mac lot 2, Debian 6d3d2a5) |
| O2 (une configuration par `seed new`) | renvoyé | clos | F7, `seed config add/remove` (lot 2, palette lot 6) |
| R1 (fichiers ouverts gardant l'ancienne commande après changement de preset) | documenté (ENV-9) | clos | F4, relance de clangd (lot 3) |
| O10 / réserve IDE-3 (clangd avant configuration) | corrigé si preset configuré avant `generate` | clos | F4, relance à l'apparition ou au changement de `build/.active/compile_commands.json` |
| R3 / écart PA-1 (source de l'arrêt sous le chemin du clone) | écart accepté en phase 1 | résorbé | F8 : QEMU Mac et Debian, NUCLEO-F429ZI et NUCLEO-WL55JC1 ; témoin `trunkPaths: false` |
| DBG-4 (P2, vue périphériques) | non testée | non vérifiable | aucun BSP ne déclare `svd` (`generate` écrit `svdFile` s'il est déclaré) ; hors F0-F8 |

## 3. Défauts ouverts (communs aux hôtes)

| ID | Constat | Suite (décision de l'utilisateur, 2026-10-28) |
| --- | --- | --- |
| D-a | `lepton/checks.py` l. 393 : au contrôle complet, l'anomalie XML perd `line` ; l'erreur paraît en 1:1 avec le préfixe « 9: » (`check --stdin` correct) | **Corrigé** (c0374c9) : anomalie recopiée entière (`dataclasses.replace`) ; test `test_rootstock_xml_xsd_line` (échoue sans la correction) ; réserve CFG-7 levée |
| D-b | Clé `type` absente ou inconnue dans un manifeste de greffon : cascade `oneOf` (≈ 20 erreurs, « False schema does not allow » non traduit, placé en 1:1) | **Renvoyé** après ENV-12 : sans discriminant valide, ne rendre que l'erreur de `type` ; traduire le message des schémas `false`. **Corrigé** en R1 (2026-10-28, `devenv/env-12-r1`) : chaque `if` sur `type` du schéma exige `type` (e2e6cf8 ; `type` absent : 20 → 1 anomalie ; `type` inconnu : déjà 1) ; champ interdit par un schéma `false` nommé, situé sur sa clé, en français, références locales comprises ; `anyOf` / `oneOf` traduits (4e636aa) ; 3 tests, `pytest` 195 |

## 4. Observations

| ID | Constat | Suite proposée |
| --- | --- | --- |
| O-a | Debian : premier lancement de VSCodium après l'installation du pack par la CLI en anglais ; français au second | Laissé (VSCodium) — décision de l'utilisateur |
| O-b | CMake Tools 1.24.42 : « … non ajouté au système de build » à chaque création de source (`cmake.modifyLists.addNewSourceFiles`) ; Mac et Debian | **Corrigé** (7e74c6d, décision de l'utilisateur) : `generate` écrit `cmake.modifyLists.addNewSourceFiles` et `removeDeletedSourceFiles` à `"no"` (le second, défaut `ask`, ajouté par la session : même cause à la suppression) ; essai Mac : création et suppression par le trunk sans notification |
| O-d | `install-vscodium.sh` n'écrit pas « (absente) → version » à la première installation de l'extension | Laisser (libellé) |
| O-e / L5-2 | `seed config remove` ne retire pas `build/<preset>/` (configuré ou non) | Laisser (lepton n'efface pas de construction) |
| O-c, O-f, O-g | Écarts de la consigne VM (chemin des journaux, ligne 49, compte des commandes) | Aucune (consigne close) |
| L3-1 à L3-6, L4-1 à L4-3, L5-1 à L5-4, L6-1 à L6-4 | Rapports des lots (§4, §5, §5, §6) | Laissés, comme proposé dans chaque rapport ; L6-4 à revérifier à chaque changement de version de VSCodium (PA-10) |
| L6-8 | 188 avertissements du code Lepton visibles dans *Problèmes* depuis le matcher gcc | Hors environnement (noyau) |
| L6-9, L6-10 | F2 par un terminal (dossiers greffés masqués) ; flash prouvé par `verify_image` | Laisser ; L6-10 à noter dans la skill `lepton-cibles` |
| R-1, R-2 | Correspondance `stem` ↔ `trunk` recalculée par l'extension ; énumérations de la CLI recopiées | Laisser (lepton refuse toute valeur hors liste) |
| O-r1 | Relevée en R1 (D-b) : `minProperties` (« {} should be non-empty »), `minimum` non traduits ; `type` affiché en liste Python, noms anglais | **Corrigé** en R1 (cadeb0e, demande de l'utilisateur) : tous les mots-clés des schémas traduits, test de couverture des mots-clés ; `pytest` 197 |

## 5. Propositions appliquées en cours d'étape (confirmées en bloc par l'utilisateur le 2026-10-28)

Lot 1 : répertoire de travail = dossier de l'espace ; `lepton.path` ; listes `--type` de la CLI ;
tests `node:test` sur un faux lepton. Lot 2 : `<bin>` = identifiant C du greffon ; retrait de la
déclaration de tout `<binaries>` ; bloc vide laissé ; graine non migrée : avertissement sans
écriture ; avertissement O5 sans code d'erreur ; greffon projet dès `seed new` ; migration des
graines d'essai. Lot 3 : événements non absorbés pendant lepton ; base clangd scrutée par
`fs.watchFile` (2 s) ; `kind: ignored`. Lot 4 : une anomalie par champ non autorisé ; délai 400 ms ;
diagnostics de saisie ou de contrôle complet par document ; aucun contrôle à l'activation ; XML
reconnu par `xml.fileAssociations`. Lot 5 : nœud « Greffons de la graine » ; preset sur le nœud
exécutif ; L3-4 : suppressions ignorées pendant lepton et 3 s après, plafond 20, fichiers seuls.
Lot 6 : `configurations` de `seed status` ; `mkconf import` d'un chemin absolu et menu contextuel ;
traceur F8 sur tous les types de débogage, réglage `lepton.debug.trunkPaths` ; `install-vscodium.sh`
installe l'extension même avec `--no-lepton`, comparaison par version ; `vscode:prepublish`.

Toutes les suites « laisser » de ce paragraphe : confirmées en bloc par l'utilisateur (2026-10-28).

## 5bis. Contrôles après corrections (Mac)

`pytest` 192 verts (191 + 1) ; `install-vscodium.sh --skip-toolchain` : 1 changement (lepton) puis 0 ;
espaces `essais/env-11/{qemu,f429zi,wl55jc1}` régénérés (réglages `modifyLists` présents, graines
inchangées) ; essai VSCodium `qemu` : création par le trunk (`essai_s3_ob.c`, lien dans le trunk,
fichier dans le clone) et « Supprimer du greffon » sans notification de CMake Tools ; trunk et clones
propres. Pas de nouveau passage Debian (corrections communes, sans effet propre à l'hôte).

## 6. Messages R12-1

Table complète : `env-12-debian.md` §6 (ORDRE, ACCUSÉ, 15 AVANCEMENT, FIN-SUCCÈS, 2026-10-28).
Branche `devenv/env-12-debian` (a1a7dbe, puis bc95a6a : `max_user_watches` remis à 30075 ; poussée sous
PA-P) fusionnée dans `devenv/env-12` (a6fc55a, c89d963). Après la FIN, accusé de la session Mac :
ordre clos.

## 7. Clôture

ENV-12 terminée le 2026-10-28 (décision de l'utilisateur) ; `devenv/env-12` fusionnée dans `main` et
poussée (PA-P accordé). Renvoi D-b corrigé le 2026-10-28 (R1, `devenv/env-12-r1`, fusionnée dans `main` et
poussée, PA-P accordé).
