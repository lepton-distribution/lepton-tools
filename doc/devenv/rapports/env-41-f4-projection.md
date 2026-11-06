# ENV-41 — Famille STM32F4 : copie d'ENV-34 remplacée par la projection

Spécification : `<SEED_SCIONS>/doc/projection-miroir.md` (P-P1 à P-P7, P-V1 à P-V6, M-D1, M-D2).
Cas d'épreuve : `rapports/env-38-projection.md` §2.1 ; effets sur lepton : §4. Essai à blanc :
`rapports/env-39-scion.md` §3.2. Miroirs : `rapports/env-40-miroir.md` §4.
Point de départ : lepton-tools `main` 96a2ffe, `family-stm32f4xx` `master` 0fd8b2a, scion 0.6.1.0,
graine `original-tree` 15740f9 (non modifiée). Branches `devenv/env-41` créées dans les deux.

## 1. Audit (lecture seule) — état au PA-69

Copie d'audit : `~/lepton-tools-dev/essais/env-41-audit` (`cp -RP` de `essais/env-39-copie`, qui
porte déjà la projection F4 avec des URL `file://`, 206 fichiers retirés du clone famille par
`git rm` non commité). Journaux : `rapports/env-41-f4-projection/audit/`.

### 1.1 `scion/.scion/` proposé pour `family-stm32f4xx`

Lignes du §2.1 d'ENV-38, destinations écrites en entier, URL des miroirs (M-D2) ; shelf `tiers`,
clés `stm32f4xx-hal-driver` et `cmsis-device-f4` (celles de l'essai d'ENV-39).

```
# .scion.sources.list
tiers	stm32f4xx-hal-driver	v1.8.5	https://github.com/lepton-distribution/mirror-stm32f4xx-hal-driver.git
tiers	cmsis-device-f4	3c77349ce04c8af401454cc51f85ea9a50e34fc1	https://github.com/lepton-distribution/mirror-cmsis_device_f4.git
# .scion.ramifications
tiers	stm32f4xx-hal-driver	v1.8.5
tiers	cmsis-device-f4	3c77349ce04c8af401454cc51f85ea9a50e34fc1
# .scion.projections  (K = scion/sys/root/src/kernel, D = K/dev/arch/cortexm, écrits en entier)
tiers  stm32f4xx-hal-driver  Inc/**                      D/stm32f4xx/hal_driver/Inc/
tiers  stm32f4xx-hal-driver  Src/**                      D/stm32f4xx/hal_driver/Src/
tiers  stm32f4xx-hal-driver  LICENSE.md                  D/stm32f4xx/hal_driver/
tiers  stm32f4xx-hal-driver  README.md                   D/stm32f4xx/hal_driver/
tiers  cmsis-device-f4       Include/stm32f4xx.h         K/core/ucore/cmsis-5/Device/ST/STM32F4xx/Include/
tiers  cmsis-device-f4       Include/system_stm32f4xx.h  K/core/ucore/cmsis-5/Device/ST/STM32F4xx/Include/
tiers  cmsis-device-f4       Include/stm32f4[23]9xx.h    K/core/ucore/cmsis-5/Device/ST/STM32F4xx/Include/
tiers  cmsis-device-f4       LICENSE.md                  K/core/ucore/cmsis-5/Device/ST/STM32F4xx/
tiers  cmsis-device-f4       README.md                   K/core/ucore/cmsis-5/Device/ST/STM32F4xx/
# .scion.mirrors  (recopié de ~/lepton-tools-dev/essais/env-40-publication/graine/scion/.scion/)
https://github.com/lepton-distribution/mirror-stm32f4xx-hal-driver.git	https://github.com/STMicroelectronics/stm32f4xx-hal-driver.git
https://github.com/lepton-distribution/mirror-cmsis_device_f4.git	https://github.com/STMicroelectronics/cmsis_device_f4.git
```

Miroirs (`git ls-remote`, 2026-11-06) : `refs/tags/v1.8.5^{}` = b6f0ed3829f3… sur le miroir HAL ;
miroir CMSIS device joignable (3c77349 atteignable, contrôlé en ENV-40 §4.2).

### 1.2 Chemins du trunk

| Relevé | Résultat |
| --- | --- |
| `<ROOTSTOCK>` (liste `./chemin -> cible` triée) | 3982 liens, SHA-256 `05b15192d4d4…5da` = ENV-39/40 (`audit/rootstock-liens.txt`) |
| copie d'audit (projection greffée) | mêmes 3982 chemins (`diff` vide) ; 206 cibles sous `depots/tiers/` |
| `LEPTON-PROVENANCE.md` | les deux restent des liens vers le clone famille ; la liste attendue des chemins est donc **identique**, provenances comprises, s'ils sont conservés |
| clones tiers de la copie | HEAD b6f0ed3 et 3c77349, 0 modification de fichier suivi |

### 1.3 Rootstocks qui greffent `family-stm32f4xx`

| Rootstock | Graine | scion de l'hôte |
| --- | --- | --- |
| `<ROOTSTOCK>` | `original-tree` | Mac 0.6.1.0 |
| `essais/env-13-vierge` | `original-tree` | Mac 0.6.1.0 |
| `essais/env-11/f429zi` | graine de projet `env11f4` (URL de la famille, `master`) | Mac 0.6.1.0 |
| copies `essais/env-34-copie`, `env-35-copie`, `env-37-copie`, `env-39-copie` | `original-tree` | Mac 0.6.1.0 (copies d'étape, hors des 7) |
| rootstocks de la VM (`env-14-debian`, `env-28-debian`, `env-36-debian`…) | `original-tree` | VM **0.5.4.0** (R33-1) : un `graft-update` y greffera la famille sans HAL |

Les 4 autres rootstocks d'essai du Mac (`env-9`, `env-11/qemu`, `qemu-gra2`, `wl55jc1`,
`bout-en-bout`) ne greffent pas la famille F4. Aucun modèle de `lepton seed new` ne cite la
famille. Rien n'est regreffé ici hors `<ROOTSTOCK>` (ENV-43 tâche 3).

### 1.4 lepton devant une famille porteuse (essai sur la copie, et lecture du code)

| Commande / élément | Constat | Effet | Taille |
| --- | --- | --- | --- |
| `check` (`checks.py:73` `check_declared_files`) | `sources` résolues dans le clone famille (`m.path.parent`) ; `inclusions` jamais lues | **code 1** : `/sources/5..8` `hal_driver/Src/*.c` « introuvable » (`audit/check.log`) | P : résoudre par le trunk |
| `seed status` (`seed.py:457`) | clés tiers : rôle « sans manifeste », « (hors graine) », `stem` = `<clone>/scion` inexistant | code 0, affichage faux | P |
| `seed tree` (`tree.py`, `files._owners`) | liens projetés sans propriétaire | famille F4 : 66/54 fichiers au lieu de 162/160 | P |
| `file owner` (`files.py:56`, `_ownership`) | remonte au répertoire `hal_driver/` (lien `LEPTON-PROVENANCE.md`) | répond « family-stm32f4xx », `clone_path` inexistant | P à M |
| `file rm/mv`, `graft --path`, `--scion <clé tiers>` | refus, messages faux ; aucune écriture dans un clone tiers | sans danger | P (message « fichier tiers projeté ») |
| `seed lock` / `--verify` / `--restore` (`seed.py:710`) | lit la seule graine : clés projetées absentes du verrou | GRA-5 tenu indirectement (commit de la famille → version tiers épinglée) ; refusé sur la graine de référence | M |
| `generate` (`generate.py:343`, `:384`) | 2 dossiers « git · » tiers ajoutés ; `files.exclude` `scion/[!.]*` ne masque rien d'un clone tiers | code 0 ; clone tiers éditable depuis l'éditeur (IDE-4) | P : omettre ces dossiers |
| `SCION_MIN_VERSION` (`lepton/__init__.py:8`) | (0, 5, 4, 0) ; `SCION_REF` déjà 0.6.1.0 ; `README.md:10` | un scion 0.5.4.0 ignore le porteur | P |
| extension `srcmap.ts:13`, `debug.ts:29` | correspondance clone → trunk par préfixe de `stem` ; un `fullname` gdb sous `depots/tiers/…` resterait tel quel | à l'arrêt, ouverture du fichier du clone tiers (seulement si gdb rend le chemin réel ; les binaires sont compilés par le trunk) | M (table clone → trunk) |
| extension `pickScion`, `tree.ts:298`, `watch.ts` | clés tiers listées « sans manifeste » ; `stem` inexistant | messages faux | P |
| hook `proteger-trunk.py` | ne protège que `trunk/` ; son message renvoie au `realpath` « sous depots/ » = clone tiers pour un lien projeté | pousse à éditer le clone tiers | P |
| skill `lepton-rootstock` | règle 1 « realpath sous depots/, éditer ce chemin-là » (même piège) ; clé périmée `lepton@bsp::nucleo-f429zi` (l. 26) | idem | P |
| `scripts/tiers/compiler-hal-f4-a-blanc.sh` | chemins du trunk seulement | fonctionne tel quel | — |
| `scripts/tiers/verifier-import.sh` | compare une copie dans un clone de greffon | sans objet pour le F4 ; reste utile au F7 et au WL | texte |
| `scripts/tiers/hal_conf_stm32f4.py` | chemin en argument ; docstring et en-tête supposent la copie dans la famille | texte | P |

Aucune exception, aucune écriture de lepton dans `depots/tiers/`. Seul `check` casse ; le reste
est faux sans le signaler.

### 1.5 Propositions soumises au PA-69

1. Lignes du §1.1 telles quelles, `.scion.mirrors` compris (M-D1 : porteur).
2. `LEPTON-PROVENANCE.md` : conservés dans la famille, réécrits (projection, clé, révision,
   miroir ; plus de « copie ») ; `LICENSE.md` et `README.md` : projetés depuis l'amont. Liste des
   chemins du trunk inchangée.
3. `SCION_MIN_VERSION` = (0, 6, 1, 0), aligné sur `SCION_REF` et sur la seule version essayée ;
   rootstocks à scion ancien : aucun traitement ici, lepton refuse un scion < 0.6.1.0, ENV-43
   installe 0.6.1.0 sur la VM avant toute regreffe ; le message du commit de la famille le dit.
4. lepton : `check` par le trunk ; `seed status`, `seed tree`, `file owner` reconnaissent une clé
   projetée (rôle « projection », propriétaire = clé tiers, refus d'écriture explicite) ;
   `generate` omet les dossiers « git · » des clones tiers ; tests. Hors étape, consignés en
   résidus : `seed lock` des clés projetées, table de correspondance de l'extension.
5. Hook : refuser aussi `<rootstock>/depots/tiers/`, message corrigé ; skill : règle « jamais
   sous `depots/tiers/` », clé d'exemple corrigée ; `verifier-import.sh` conservé (F7, WL),
   texte de `hal_conf_stm32f4.py` corrigé ; `compiler-hal-f4-a-blanc.sh` inchangé.

### 1.6 Décisions du PA-69 (utilisateur, 2026-11-06)

1. Lignes du §1.1 acceptées, `.scion.mirrors` compris.
2. `LEPTON-PROVENANCE.md` conservés et réécrits ; `LICENSE.md`, `README.md` projetés ; liste des
   chemins du trunk strictement inchangée.
3. `SCION_MIN_VERSION` = (0, 6, 1, 0) ; rootstocks à scion ancien : rien ici (ENV-43).
4. lepton : **périmètre complet** — proposition 4 plus `seed lock`/`--verify`/`--restore` des clés
   projetées et, dans l'extension, la table clone tiers → trunk (`srcmap`, `debug`), `pickScion`,
   `watch`, `revealInClone`.
5. Proposition 5 acceptée (hook, skill, scripts).
