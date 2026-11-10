# ENV-48 — Famille STM32WL : copie remplacée par la projection

Rapport de l'étape (session du 2026-11-10). Fichier d'étape : `etapes/ENV-48-wl-projection.md`.
Journaux et listes : `env-48-wl-projection/`.

## 1. Audit (lecture seule) — état au PA-83

### 1.0 Point de départ
- Dépôts propres, aux commits de la passation d'ENV-47 :
  - lepton-tools `main` d2dc475, branche `devenv/env-48` créée depuis ce commit ;
  - `family-stm32wlxx` `master` 2340b25 ;
  - F7 12280a5, F4 acdd24c ; clone noyau 76f28bd ; BSP WL55 4d7cf80 ;
  - graine `original-tree` 15740f9 ; seed.scions `master` 7e8a0cc.
- Outils : scion 0.6.2.0, lepton 0.1.0. `pushInsteadOf` SSH global présent (PA-68).
- Sondes visibles (`ioreg`) : WL55 A (002700253431510837393937) et B (004F003E3431510937393937).
  La STM32F746G-DISCO n'est plus branchée.
- Miroirs WL : aucun n'existe sous `lepton-distribution/` (`gh repo view`). La graine de
  publication `essais/env-40-publication/` déclare 4 miroirs (F4, F7).

### 1.1 Copie actuelle contre l'amont
Révisions : les tags locaux = les tags de l'amont (`git ls-remote`, `audit/revisions.txt`,
`audit/ls-remote-*.txt`). Les 4 tags sont annotés et inchangés depuis ENV-37.

| Ensemble | Révision | Résultat de `verifier-import.sh` (`audit/verifier-*.txt`) |
| --- | --- | --- |
| HAL | `stm32wlxx-hal-driver` `v1.3.0` e3966ab | 155 OK, 1 DIFF (`stm32_hal_legacy.h`), 1 TROP (`LICENSE.txt`) |
| HAL | STM32CubeWL `v1.3.0` 378e461 | 156 OK, 1 TROP (`LICENSE.txt`) |
| CMSIS device | `cmsis-device-wl` `v1.1.1` d248c55 | 5 OK |
| Pile radio | `stm32-mw-subghz-phy` `v1.3.0` 1cad768 | 18 OK, 1 DIFF (`radio.c`), 5 TROP |
| Utilitaires | STM32CubeWL `v1.3.0` 378e461 | 32 OK, 1 DIFF (`stm32_timer.h`), 6 TROP |

Ces résultats sont ceux d'ENV-37 §1.3 : la famille n'a pas changé depuis.

Noms suivis par git dans les 4 ensembles, comparés aux attendus d'ENV-38 (`attendus/wl-*.txt`,
211 chemins) :
- 229 fichiers suivis (`audit/famille-suivis-ensembles.txt`) ;
- les 211 attendus sont tous suivis, casse comprise (tri par octets) ;
- ils restent 18 (`audit/famille-restent.txt`) : 4 `LEPTON-PROVENANCE.md`, 8 `LICENSE.txt`,
  `stm32_hal_legacy.h`, `radio.c`, `stm32_timer.h`, `subghz.h`, `utilities_conf.h`, `platform.h`.
  C'est la liste du §2.3 d'ENV-38.

### 1.2 Trunk de `<ROOTSTOCK>`
`env-43-mac/controler-trunk.py` (lecture seule), contre l'attendu d'après ENV-47 :
- **CONFORME** : 3887 liens, 0 fichier régulier, 0 lien cassé ;
- 407 projetés (F4 206, F7 201), contenu = HEAD, 0 écart de casse ;
- liste `chemin -> cible` `70cc91c2…`, chemins seuls `c65ee399…`, identiques à la fin
  d'ENV-47 (`audit/rootstock/`) ;
- 243 liens visent la famille WL ; les 211 attendus sont tous des liens du trunk, casse comprise.

Attendu après la bascule : 3887 chemins **identiques**. Les 211 cibles quittent la famille pour
les clones tiers, soit 618 projetés. Les 18 fichiers restants gardent leur cible. La liste est
produite par `env-48-wl-projection/attendu-apres.py`, écrit pour cette étape :
- sortie `attendu-liens-apres.txt` ;
- 211 cibles réorientées, 0 erreur.

Cette liste ne vaut qu'au sort de C2 près (§1.8).

### 1.3 `scion/.scion/` proposé pour `family-stm32wlxx`
Fichiers complets : `env-48-wl-projection/propose/`. Ce sont les lignes du §2.3 d'ENV-38, écrites
en entier, avec les URL des miroirs.

```
# .scion.sources.list (ramifications : mêmes clés et versions)
tiers  stm32wlxx-hal-driver         v1.3.0  https://github.com/lepton-distribution/mirror-stm32wlxx-hal-driver.git
tiers  cmsis-device-wl              v1.1.1  https://github.com/lepton-distribution/mirror-cmsis-device-wl.git
tiers  stm32-mw-subghz-phy          v1.3.0  https://github.com/lepton-distribution/mirror-stm32-mw-subghz-phy.git
tiers  stm32cubewl::utilities       v1.3.0  https://github.com/lepton-distribution/mirror-STM32CubeWL.git
tiers  stm32cubewl::radio-core-inc  v1.3.0  https://github.com/lepton-distribution/mirror-STM32CubeWL.git

# .scion.projections : 25 lignes (D = scion/sys/root/src/kernel/dev/arch/cortexm/stm32wlxx,
# C = scion/sys/root/src/kernel/core/ucore/cmsis/Device/st/stm32wlxx)
stm32wlxx-hal-driver  Inc/** → D/cubemx_hal_driver/inc/ ; Src/** → …/src/ ; README.md, Release_Notes.html → …/
                      !Inc/Legacy/stm32_hal_legacy.h
cmsis-device-wl       Include/{stm32wl55xx,stm32wlxx,system_stm32wlxx}.h, Source/Templates/system_stm32wlxx.c → C/
                      Source/Templates/iar/startup_stm32wl55xx_cm4.s → C/startup/iar/
stm32-mw-subghz-phy   *.h, LICENSE → D/radio_subghz_phy/ ; Conf/* → …/Conf/ ; stm32_radio_driver/* → …/stm32_radio_driver/
                      !stm32_radio_driver/radio.c
stm32cubewl::utilities  Utilities/{conf,Fonts,lcd,lpm/tiny_lpm,misc,sequencer,timer,trace/adv_trace}/*.[ch] → D/Utilities/…/
                      !Utilities/timer/stm32_timer.h
stm32cubewl::radio-core-inc  Projects/NUCLEO-WL55JC/Applications/SubGHz_Phy/SubGHz_Phy_PingPong/Core/Inc/utilities_def.h
                      → D/radio_subghz_phy/stm32_radio_core_inc/

# .scion.mirrors
https://github.com/lepton-distribution/mirror-stm32wlxx-hal-driver.git  https://github.com/STMicroelectronics/stm32wlxx-hal-driver.git
https://github.com/lepton-distribution/mirror-cmsis-device-wl.git       https://github.com/STMicroelectronics/cmsis-device-wl.git
https://github.com/lepton-distribution/mirror-stm32-mw-subghz-phy.git   https://github.com/STMicroelectronics/stm32-mw-subghz-phy.git
https://github.com/lepton-distribution/mirror-STM32CubeWL.git           https://github.com/STMicroelectronics/STM32CubeWL.git
```

Noms des miroirs : `mirror-<nom de l'amont>`, casse de l'amont comprise, comme pour le F4 et le
F7 (`mirror-cmsis_device_f4`). Versions : des tags, comme pour le F7.

### 1.4 Essai à blanc sur la copie d'essai `essais/env-48-copie`
Préparation :
- copie par `rsync -a` de `<ROOTSTOCK>`, sans `build/` ni `third_party/` : 3887 liens, 0 cassé ;
- dans son clone `family-stm32wlxx`, branche `essai/env-48-audit` (b44655d, non publiée) ;
- `scion/.scion/` du §1.3, avec les URL **amont** STMicroelectronics dans
  `.scion.sources.list`, car les miroirs n'existent pas encore ;
- `git rm` des 211 fichiers attendus, puis un commit : 215 fichiers changés, aucun répertoire vide.

Journaux : `audit/essai/`.

| Action | Résultat |
| --- | --- |
| `scion seed-clone --seed depots/lepton-seed.scions/original-tree` | code 0, 24 s ; 4 clones `depots/tiers/` : `stm32wlxx-hal-driver/v1.3.0`, `cmsis-device-wl/v1.1.1`, `stm32-mw-subghz-phy/v1.3.0`, **un seul** `stm32cubewl/v1.3.0` pour les deux clés (P-V2) ; tous aux commits épinglés, `blob:none` |
| `scion graft -v` | code 0 ; 3887 feuilles ; 23 entrées dans la liste greffée (18 + 5 clés) ; 6ᵉ colonne = porteur WL |
| fichiers par ligne (`-v`) | HAL 81 + 72 + 1 + 1 = 155, `stm32_hal_legacy.h` exclu ; CMSIS 5 × 1 ; radio 4 + 1 + 4 + 9 = 18, `radio.c` exclu ; utilitaires 1 + 6 + 2 + 4 + 10 + 2 + 3 + 4 = 32, `stm32_timer.h` exclu ; `utilities_def.h` 1 |
| `controler-trunk.py` contre `attendu-liens-apres.txt` | **CONFORME** : liste `chemin -> cible` identique (3887) ; 0 régulier, 0 cassé ; 618 projetés ; 0 nom absent du HEAD (casse) ; 0 contenu ≠ blob du HEAD |
| contenu contre `<ROOTSTOCK>` (`cmp`) | 211 projetés : 0 écart ; les 3887 : 0 écart |
| `graft-remove tiers@stm32cubewl::radio-core-inc` | code 0 ; 1 feuille retirée ; les 32 liens de `::utilities` et le clone restent (`audit/essai/partage/`) |
| `graft` complet ensuite | la clé retirée ne revient pas (règle de 0.5.4.0 : la liste greffée fait foi) ; elle revient par `seed-clone` + `graft` |
| `graft-remove --purge tiers@stm32cubewl::radio-core-inc` | **refusé**, code 1 : « clone … partagé avec tiers/stm32cubewl::utilities ; --purge refusé » ; rien n'est touché |
| `graft --scion tiers@stm32cubewl::utilities` (P-G5) | code 0 ; 32 feuilles |
| `graft --scion lepton@family-stm32wlxx` (P-G6) | code 0 ; 243 feuilles ; « clés projetées regreffées avec leur porteur » : les 5 |
| contrôle final | **CONFORME** (`audit/essai/controle-final/`) |
| `lepton check` | code 0 (19 fichiers conformes) |
| `lepton generate` | code 0 ; espace de travail identique à celui de `<ROOTSTOCK>`, aux chemins du rootstock près |

Chaque fonction de scion que le cas sollicite donne la liste attendue :
- renommage de casse `Inc` → `inc` (P-T2) ; P-K2 sans collision ;
- aplatissement et chemin changé (`Source/Templates/iar/` → `startup/iar/`) ;
- exclusions (P-X1) ;
- sélection positive dans un gros dépôt (P-M1, `html/` non désigné) ;
- clone partagé (P-V2), avec retrait et purge sûrs ;
- deux amonts sous `radio_subghz_phy/` (P-G1).

**Aucun défaut de scion constaté. Aucun correctif de scion n'est nécessaire.**

### 1.5 Constat sur lepton : propriété dans un clone partagé (P-G3)
`lepton seed status` sur la copie :
- `stm32cubewl::utilities` : 33 fichiers ;
- `stm32cubewl::radio-core-inc` : 0 fichier ;
- or scion en greffe 32 et 1.

`lepton file owner` attribue `…/stm32_radio_core_inc/utilities_def.h` à
`tiers@stm32cubewl::utilities`. Selon P-G3, il appartient à `::radio-core-inc` : « quand plusieurs
clés projetées partagent un clone, un lien appartient à celle dont la table contient son chemin du
trunk ».

Cause : lepton attribue un lien à la première clé dont la racine du clone préfixe sa cible.
- `Rootstock.projection_tables()`, `lepton/rootstock.py:250-267`, s'arrête au premier préfixe
  trouvé (`break`).
- `_owner_of()`, `lepton/files.py:71-75`, fait de même.
- Deux clés de même racine reçoivent donc tout dans la première. Le cas ne s'est jamais présenté
  avant le WL.

Portée, d'après le code et la copie :
- **affectés** : l'attribution affichée par `seed status` (comptes, table par clé), `file owner`
  et `seed tree` (`lepton/tree.py:143-213`) ;
- **non affectés** :
  - la greffe, les binaires et le trunk ;
  - les refus d'écriture de `lepton file …` (les deux clés sont projetées) ;
  - la table clone → trunk de l'extension (`extension/src/srcmap.ts:23-31` fusionne les tables
    par chemin absolu du clone, quelle que soit la clé) ;
  - `seed lock` (une entrée par clé, même commit) ;
  - `lepton check`, `lepton generate`.

### 1.6 STM32CubeWL : taille, miroir, extraction
| Mesure | Valeur |
| --- | --- |
| Dépôt GitHub (taille déclarée) | STM32CubeWL environ 63 Mo ; `stm32wlxx-hal-driver` 4 Mo ; `cmsis-device-wl` 1 Mo ; `stm32-mw-subghz-phy` 0,5 Mo |
| Références de l'amont (M-C3 : branches et tags) | STM32CubeWL : `main` + 8 tags (`v1.0.0` à `v1.6.0`) ; HAL : `main` + 8 ; CMSIS : `main` + 6 ; SubGHz : `main` + 6 ; `refs/pull/*` non traités |
| Arbre de `v1.3.0` | 17 937 fichiers, 261 Mo (API GitHub) : `Drivers` 117 Mo, `Projects` 101 Mo, `Middlewares` 22 Mo, `Utilities` 14 Mo ; aucun sous-module jusqu'à `v1.3.0` (sous-modules HAL et CMSIS à partir de `v1.3.1`) |
| Clone projeté `depots/tiers/stm32cubewl/v1.3.0` | 359 Mo sur disque (`blob:none`, puis extraction complète de `v1.3.0`) pour 33 fichiers projetés |

Faisabilité :
- **Miroir complet** (toutes les branches et tous les tags) : faisable. Environ 63 Mo à envoyer,
  très en deçà des limites de GitHub (2 Go par envoi). La méthode d'ENV-40 et d'ENV-47 s'applique
  telle quelle. Le dépôt de travail `depots/.mirrors/github.com/lepton-distribution/mirror-STM32CubeWL.git`
  occupe la taille de l'historique.
- **Autre forme compatible avec M-*** : M-C1 permet de ne synchroniser que certains miroirs
  (URL données), mais toujours toutes leurs branches et tous leurs tags (M-C3). La spécification
  n'offre aucun miroir partiel par référence ou par chemin.
- **Extraction** : P-V2 extrait l'arbre entier (`git checkout --detach`). Le `sparse-checkout`
  est hors du périmètre de la spécification (§C). Chaque rootstock qui greffe la famille WL
  télécharge donc environ 360 Mo pour 33 fichiers : 24 s ici.

Ce coût est un constat, pas un défaut : le relever ne demande aucun choix dans cette étape.

### 1.7 C1 : raison de la neutralisation de `RadioIsChannelFree`
Faits établis :
1. Le `#if 0` (corps neutralisé, `return false;`) est déjà présent dans le **premier** commit du
   fichier, efa8106 du 2024-05-24 (« added files from stm32cubemx-win-v6-11-0 and
   stm32cubewl-v1-3-0 », clone noyau). Aucun commit ne l'a introduit ensuite : 8d5a082 (ENV-6) est
   un déplacement. Le `git log -S RadioIsChannelFree` ne donne que ces deux commits.
2. Aucune trace écrite de la raison :
   - rien dans les messages de commit ;
   - rien dans `doc/` du clone noyau (`MIGRATION-STATUS.md` compris) ;
   - aucune marque dans le fichier.
3. Le corps neutralisé est le **seul** utilisateur, dans `radio.c`, de `TimerGetCurrentTime` et de
   `TimerGetElapsedTime`. `stm32_radio_target/timer.h` les ramène à `UTIL_TIMER_GetCurrentTime` et
   `UTIL_TIMER_GetElapsedTime`, définis seulement dans `Utilities/timer/stm32_timer.c`.
4. En 2024, les projets IAR (`dev_stm32wlxx_*.ewp`, 6e830bb ; `bsp_stm32wl55jci_nucleo_*.ewp`,
   0e600f6) compilaient `radio.c` mais aucun utilitaire, sauf `Utilities/misc/stm32_mem.c`.
   `stm32_timer.c` n'était pas compilé.
5. Dans le même import, `timer.h` neutralise aussi `TimerInit`, `TimerSetValue`, `TimerStart` et
   `TimerStop` : macros vides, version complète sous `#if 0`.
6. Aucun code Lepton n'appelle `Radio.IsChannelFree` : seule l'entrée de la table `Radio` de
   `radio.c` (l. 646) la référence. Le pilote `/dev/radio` émet sans écoute préalable.
7. En migration (10f706d, 2026-10-05), `dev_stm32wlxx_util_timer.c` a été ajouté pour fournir
   `UTIL_TIMER_GetCurrentTime` et `UTIL_TIMER_GetElapsedTime`. Son commentaire dit que `radio.c` en
   a besoin pour l'écoute avant émission. La passation de migration `handoff/etape-6-wl55-1.md`
   l. 48 l'avait relevé sans voir le `#if 0`. Le fichier est compilé, mais ses deux fonctions
   ne sont pas dans `lepton.elf`, car aucun code ne les appelle. Le commentaire est donc inexact.

Raison **probable, non établie par un écrit** : la neutralisation évitait les symboles
`UTIL_TIMER_*` non résolus à l'édition de liens des projets IAR de 2024, qui ne compilaient pas
le serveur de minuteries `stm32_timer.c`. Elle suit la même démarche que les macros vides de
`timer.h`. Effet : `Radio.IsChannelFree` rend toujours `false`. Lepton ne l'appelle pas.

### 1.8 C2 : les 8 `LICENSE.txt`
- Emplacements :
  - `cubemx_hal_driver/`, `radio_subghz_phy/` ;
  - `Utilities/{conf,misc,sequencer,timer,lpm/tiny_lpm,trace/adv_trace}/`.
- Contenu identique (3edc4d1) : un avis court ST. Il renvoie à un fichier « Package_license » et,
  à défaut, à BSD-3-Clause. Il est absent de tous les tags des dépôts amont (ENV-37 §1.4).
- Origine probable : la génération de projet par STM32CubeMX, nommée dans le message d'efa8106
  (« stm32cubemx-win-v6-11-0 »). Non vérifiable sans STM32CubeMX.
- Chaque `LICENSE.txt` jouxte un `LICENSE.md` de l'amont, absent de la copie :
  - HAL `v1.3.0` : `LICENSE.md` c750f6a, BSD-3-Clause ST, = STM32CubeWL ;
  - pile radio `v1.3.0` : `LICENSE.md` 66d657e, BSD-3-Clause ST. `LICENSE` (Clear BSD Semtech)
    est déjà repris ;
  - utilitaires : 6 × `LICENSE.md` identiques (06b2122), BSD-3-Clause ST, aux 6 mêmes
    répertoires ;
  - CMSIS device `v1.1.1` : `LICENSE.md` 261eeb9, **Apache-2.0**. Aucun `LICENSE.txt` à cet
    endroit.
- Effet d'une projection des `LICENSE.md` : +8 chemins, ou +9 avec le CMSIS. Ce sont des
  fichiers non compilés, sans effet sur les binaires. Retirer les `LICENSE.txt` ôte 8 chemins.

### 1.9 Rootstocks et graines qui greffent `family-stm32wlxx`
Tous en version `master` (2340b25). Rien ne change pour eux tant que la famille publiée n'avance
pas. Leur regreffe relève d'ENV-50.

| Hôte | Rootstock | Graine | Remarque |
| --- | --- | --- | --- |
| Mac | `<ROOTSTOCK>` | `original-tree` | basculé ici (PA-P) |
| Mac | `essais/env-13-vierge` | `original-tree` | → ENV-50 |
| Mac | `essais/env-41-vierge` | `env-41-vierge-graine` (locale) | rootstock neuf d'ENV-41 gardé |
| Mac | `essais/env-11/wl55jc1` | graine de projet `env11wl` (`lepton-graine.json`, `project/`) | greffe le WL ; ENV-47 §1.4 ne l'avait pas relevé, car il ne greffe pas le F7 |
| Mac | `essais/env-34-copie`, `env-35-copie`, `env-37-copie`, `env-39-copie` | `original-tree` | copies d'étape, hors regreffes |
| VM | `essais/env-28-debian`, `essais/env-43-debian` | `original-tree` | ENV-50 |

Un `graft-update` de ces rootstocks avancera la famille et créera les 4 clones tiers WL (environ
360 Mo, §1.6). Il exige scion ≥ 0.6.1.0.

### 1.10 lepton, extension, hook, skill, scripts
- lepton, extension, hook : aucune mention propre au WL. Défaut d'attribution du clone partagé :
  §1.5.
- Skill `lepton-cibles` : mentions des cartes WL55 seulement, sans rien sur le code tiers.
  Rien à changer.
- Skill `lepton-rootstock` : `family-stm32f4xx` donné en exemple de porteur. C'est exact, rien à
  changer.
- `scripts/tiers/verifier-import.sh` l. 15 : « Sert aux copies dans un clone de greffon (famille
  STM32WL) ». Après la bascule, il ne reste plus aucune copie de famille. Son usage restant est la
  vérification de copies hors projection, par exemple une montée de version préparée à la main.
- Manifeste de la famille :
  - `description` cite « HAL ST STM32CubeWL V1.3.0 (cubemx_hal_driver), pile radio SubGHz_Phy
    1.3.0 et utilitaires ST, CMSIS device ST », sans dire qu'ils sont projetés ;
  - `sources` (`cubemx_hal_driver/src/…`, `radio_subghz_phy/stm32_radio_driver/…`,
    `Utilities/misc/stm32_mem.c`) et `compilation` sont résolus par le trunk depuis ENV-41 et
    restent inchangés (`lepton check` code 0 sur la copie).
- Le BSP `nucleo-wl55jc1` (`stm32_radio_target/`, `stm32wlxx_hal_conf.h`) n'est pas touché.

### 1.11 Propositions soumises au PA-83
1. **Lignes** du §1.3 : 5 clés, tags `v1.3.0` / `v1.1.1` / `v1.3.0` / `v1.3.0`, 25 lignes de
   projection, URL des miroirs.
2. **Miroirs**, forme du PA-81. Il y en a 4 :
   - `lepton-distribution/mirror-stm32wlxx-hal-driver` ;
   - `mirror-cmsis-device-wl` ;
   - `mirror-stm32-mw-subghz-phy` ;
   - `mirror-STM32CubeWL`.

   Tous sont publics, avec la description seule et aucun commit ajouté, et créés par la session
   (`gh repo create --public`). STM32CubeWL est un **miroir complet**, faisable (§1.6).
   Première synchronisation par la graine de publication : 4 lignes ajoutées, `mirror-sync
   --seed`, d'abord en `--dry-run`, puis l'envoi (PA-P).
3. **scion** : aucun correctif (§1.4). Ni nouvelle version, ni `SCION_MIN_VERSION`, ni `SCION_REF`.
4. **Défaut de lepton** (§1.5), trois options :
   - (a) **corriger lepton dans cette étape** (recommandé) : attribuer un lien d'un clone partagé
     à la clé dont les lignes de projection désignent son fichier source.
     - Le correctif lit le `.scion.projections` du porteur, déjà lu par
       `read_projection_keys`, et applique les motifs P-M*.
     - Il ne vaut que si plusieurs clés partagent une racine.
     - Il touche `projection_tables` et `_owner_of`, avec des tests pytest, dans un commit dédié
       de lepton-tools.
     - lepton reste en 0.1.0 et réinstallé par pipx ; aucun effet sur la greffe ni sur les
       binaires.
   - (b) **une seule clé `stm32cubewl`** pour les 33 fichiers : lepton est alors correct sans
     changement, mais P-V2 n'a plus de cas réel ;
   - (c) **documenter et reporter** : ajout à `HORS-PLAN.md`, l'attribution affichée restant
     fausse pour `utilities_def.h`.
5. **C1** : écrire dans `radio_subghz_phy/LEPTON-PROVENANCE.md` les faits du §1.7, la raison
   donnée comme **probable, non établie**, et l'absence d'appelant dans Lepton. Le binaire ne
   change pas. Sans rapport direct avec la bascule, le commentaire inexact de
   `dev_stm32wlxx_util_timer.c` (§1.7, fait 7) peut être corrigé ou laissé :
   - corrigé : un commentaire seulement, binaire inchangé ;
   - laissé : à noter au `HORS-PLAN.md`.
6. **C2**, trois options :
   - (a) **retirer les 8 `LICENSE.txt` et projeter les `LICENSE.md` de l'amont** (recommandé) :
     8 lignes de projection, plus 1 pour le CMSIS device (Apache-2.0), soit −8 et +9 chemins
     dans le trunk. Ce sont les écarts accordés de la liste des chemins. Le texte de licence
     vient alors de l'amont épinglé ;
   - (b) garder les `LICENSE.txt` et ajouter les `LICENSE.md` (+9 chemins) ;
   - (c) statu quo : `LICENSE.txt` gardés, rien d'ajouté.
7. **Provenances** :
   - les 4 `LEPTON-PROVENANCE.md` sont conservés et réécrits, forme du PA-81 : projection, clé,
     révision, miroir, « Exige scion ≥ 0.6.1.0 » comme le F4 et le F7, fichiers restés dans la
     famille, C1, C2 ;
   - le `description` du manifeste est réécrit ; `sources` et `compilation` restent inchangés ;
   - l'aide de `verifier-import.sh` est corrigée dans un commit dédié de lepton-tools.
8. **Bascule** comme en ENV-47 :
   - sur la copie d'essai, après `reset` de la branche d'essai ;
   - puis sur un rootstock neuf `essais/env-48-vierge` (graine d'essai locale, famille en
     `file://` de `devenv/env-48`) ;
   - puis sur `<ROOTSTOCK>` (PA-P), par `seed-clone --seed …/original-tree` et `graft`, sans
     `graft-update`.
9. **Rootstock à graine de projet** `essais/env-48-projet` (forme d'ENV-47 §1.5,
   `--origin stm32wlxx=file://…@devenv/env-48`, BSP `nucleo-wl55jc1`) pour `seed lock` et
   `--verify` ; supprimé au PA-84. `essais/env-11/wl55jc1` n'est pas touché.
10. **Banc** WL55 A/B, en embOS et en FreeRTOS, radio comprise (`banc-wl55.sh`) : les deux
    cartes sont branchées. Écriture flash à accorder (PA-11).

### 1.12 Décisions du PA-83 (utilisateur, 2026-11-10)
- Propositions 1 à 3 et 7 à 10 acceptées telles quelles. L'accord vaut PA-P pour `gh repo create`
  des 4 miroirs et leur synchronisation (push), et PA-11 pour l'écriture flash des deux WL55.
- Proposition 4 : option (a), lepton corrigé dans cette étape.
- Proposition 5 : provenance écrite, raison « probable, non établie » ; commentaire de
  `dev_stm32wlxx_util_timer.c` corrigé.
- Proposition 6 : option (a). Les 8 `LICENSE.txt` sont retirés et les 9 `LICENSE.md` de l'amont
  projetés. Les écarts accordés de la liste des chemins du trunk sont −8 et +9.
