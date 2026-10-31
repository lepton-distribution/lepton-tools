# Étape ENV-24 — Dimensionnement automatique du cpufs

## Contexte
Décision PA-3 (2026-10-13) : dans `<cpufs>`, les attributs `size` et `node` deviennent
facultatifs.
- Absents : mklepton dimensionne l'image au plus juste (cpufs en lecture seule).
- Présents : les valeurs imposées sont refusées si elles sont trop petites.

ENV-4 a implémenté ce comportement. Les 6 XML ont pourtant gardé des valeurs imposées, pour
garder les empreintes identiques. Le passage au dimensionnement automatique a été reporté, « à
décider avec essai sur cartes » (`DEVENV-STATUS.md` §Décisions, 2026-10-13).

Cette étape fait ce passage. Elle change volontairement les images. Archétype : migration avec
changement voulu. L'écart admis se limite au cpufs ; l'oracle fait foi pour le reste.

## Prérequis
- ENV-22 terminée ; ENV-23 conseillée avant.
- XML portant `<cpufs>`, dans `scion/sys/user/tauon-basic/etc/` du clone noyau
  `<ROOTSTOCK>/depots/lepton/original/master` :
  - `mkconf_tauon_basic_qemu_mps2.xml`
  - `mkconf_tauon_basic_nucleo_f439zi.xml`
  - `mkconf_tauon_basic_nucleo_wl55jc1.xml`
  - `mkconf_tauon_basic_stm32f746g_disco.xml`
  - `mkconf_tauon_basic_samd21_xplained_pro.xml`
  - `mkconf_tauon_basic_lwip_stm32f4-olimex-p407.xml`
- `scion/tests/host/mklepton_format_check.cmake:19` exige `size` et `node`
  (« `<cpufs size=… node=…> attendu` »). Référence des empreintes :
  `scion/tests/host/mklepton_empreintes.sha256`.
- Skills `lepton-oracle`, `lepton-cibles` et `lepton-rootstock`.
- Branches `devenv/env-24` : lepton-tools et clone noyau.

## Tâches

### 1. Audit (lecture seule) → PA-35
- Pour chaque XML :
  - presets qui l'utilisent (`LEPTON_MKCONF`) ;
  - valeurs imposées (`size`, `node`, `blocksz`) et taille calculée par mklepton sans elles ;
  - contenu du cpufs.
- Écritures dans le cpufs au cours de l'exécution : tests de fumée, banc KAL, `lsh`. Une écriture
  rend le dimensionnement au plus juste incompatible avec ce XML.
- XML des graines de projet des rootstocks d'essai (`seed mkconf import`) : hors périmètre ou
  non, <À CONFIRMER au PA-35>.
- Rapport `rapports/env-24-cpufs.md` : tableau XML × taille imposée × taille calculée × écart de
  `.rodata`/`.data` attendu.
- **PA-35** : l'utilisateur valide :
  - la liste des XML qui passent au dimensionnement automatique, et ceux qui gardent des valeurs
    imposées, avec leur raison ;
  - le traitement de `mklepton_format_check.cmake` (contrôle retiré, ou contrôle de cohérence) ;
  - le critère de non-régression : écarts de sections et de symboles limités à l'image cpufs ;
    fumée et banc KAL identiques ;
  - les cartes disponibles pour les essais : <À CONFIRMER au PA-35 : NUCLEO-F429ZI,
    NUCLEO-WL55JC1, STM32F746G-DISCO, SAMD21 Xplained Pro> ;
  - le sort de `mkconf_tauon_basic_lwip_stm32f4-olimex-p407.xml` s'il ne sert à aucun preset.
- Aucune modification avant la réponse.

### 2. Oracle avant
Skill `lepton-oracle` : host et les 16 presets → `rapports/oracles/env-24-avant/`, conforme à
`env-20-apres`.

### 3. Modification (un lot par XML)
- Clone noyau : retirer `size` et `node` des XML retenus. Un commit par XML ; `blocksz` reste
  inchangé, sauf décision contraire.
- Adapter `mklepton_format_check.cmake` selon le PA-35, puis générer la nouvelle référence
  `mklepton_empreintes.sha256` et vérifier que `host.mklepton_empreintes` passe.
- Après chaque lot :
  - oracle partiel des presets du XML, puis `comparer-oracle.py` ;
  - classer chaque écart : image cpufs, ou autre (un « autre » arrête le lot).

### 4. Contrôles → PA-36
- Oracle après (`env-24-apres/`) ; `comparer-oracle.py` sur host et les 16 presets.
- QEMU : fumée et banc KAL identiques (filtre d'ENV-19 E-4).
- Cartes : fumée et banc KAL sur chaque carte accordée au PA-35, mêmes nombres qu'en ENV-19 et
  ENV-20 (F429 19/19, F746 19/19, SAMD21 15/15). Remettre ensuite l'image d'origine en flash
  (« Verified OK »).
- `lepton check` code 0.
- **PA-36** : rapport ; fusion et push (PA-P). La validation Debian est reportée à ENV-28.

## Critères de validation
- [ ] PA-35 et PA-36 tranchés et consignés.
- [ ] XML retenus sans `size` ni `node` ; `host.mklepton_empreintes` vert avec la nouvelle référence.
- [ ] Écarts de l'oracle limités à l'image cpufs, chacun classé dans le rapport.
- [ ] Fumée et banc KAL identiques sur QEMU et sur les cartes accordées.

## Pièges connus
- Les empreintes des binaires changent à chaque construction (`__DATE__`/`__TIME__`) : seules
  les sections et les symboles comptent.
- Un cpufs dimensionné au plus juste ne laisse plus de place : un test qui écrit dans le cpufs
  échoue. Il s'agit alors d'une erreur de l'audit, pas d'un écart à accepter.
- SAMD21 sous FreeRTOS : la fumée échoue déjà (écart hérité, RAM). Le banc se lance par
  `-FS board_t0 -E board.smoke_lsh`.
- `ctest -L board` prend la première sonde ST-LINK : brancher une seule carte ST à la fois.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, branches, décisions PA-35 et PA-36, journal. Passation
`handoff/env-24.md`.
