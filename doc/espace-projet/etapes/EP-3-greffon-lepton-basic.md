# Étape EP-3 — Greffon `lepton-original-tree-project` (extraction de `lepton-basic`)

## Contexte
C6, option B : le projet de démonstration du noyau, `sys/user/tauon-basic`, devient le premier
greffon de type `projet` : dépôt GitHub `lepton-distribution/lepton-original-tree-project`,
arbre `scion/sys/user/lepton-basic/`. C7, option (i) : `sys/user/tauon-basic/` reste dans le
noyau, amputé des fichiers repris. C8 : la graine de référence `original-tree` garde son régime ;
le greffon y est ajouté **par scion, dans son dépôt**, comme les BSP en ENV-13, ENV-19, ENV-20.

Repris (15 fichiers, `CADRAGE.md` §2.5) :
- 5 XML, **nom inchangé** : `mkconf_tauon_basic_{qemu_mps2,nucleo_f439zi,nucleo_wl55jc1,
  stm32f746g_disco,samd21_xplained_pro}.xml` ;
- 10 fichiers `etc/<carte>/{.boot,.init}` pour `qemu-mps2`, `nucleo-f439zi`, `nucleo-wl55jc1`,
  `stm32f746g-disco`, `samd21-xplained-pro`.
Leurs `src_file` sont réécrits `sys/user/lepton-basic/…`.

**Non repris, à ne pas toucher** (H5 du hors-plan) : `etc/.boot`, `etc/.init`, `etc/.mount`, les
5 variantes `.init_*`, `src/bin/*`, les 7 `user_kernel_mkconf.h`, et le XML Olimex
`mkconf_tauon_basic_lwip_stm32f4-olimex-p407.xml`, base du test hôte `host.mklepton` : ses
entrées restent au même chemin, et les 8 lignes Olimex de `mklepton_empreintes.sha256` ne
changent pas.

**T10** (relevé à la relecture du plan, contre C7 et `CADRAGE.md` §2.5) : trois consommateurs des
fichiers repris ne sont pas couverts par les décisions. Dans le clone noyau, sous `scion/` :
- `tests/host/CMakeLists.txt` (`host.mklepton_format`) lit
  `sys/user/tauon-basic/etc/mkconf_tauon_basic_qemu_mps2.xml` ;
- `tests/host/mklepton_empreintes.sh` joue mklepton sur chaque `LEPTON_MKCONF` des presets, et
  mklepton écrit le chemin du XML en première ligne de `kernel_mkconf.h`
  (`tools/mklepton/src/mklepton.c`) : les empreintes des cartes portées changent avec le chemin ;
- 5 BSP publiés (`bsp-qemu-mps2-an386`, `bsp-qemu-mps2-an500`, `bsp-nucleo-f429zi`,
  `bsp-nucleo-f439zi`, `bsp-stm32f746g-disco`) posent `LEPTON_NET_TEST_FTP_REFERENCE` sur un
  `sys/user/tauon-basic/etc/<carte>/.boot` repris.
L'étape ne tranche pas : elle les présente au PA-E6.

Archétype : **migration**. Déplacement à l'identique ; aucune correction d'opportunité dans les
XML ni dans les `.boot` et `.init`. Binaires attendus identiques (`CADRAGE.md` §6), à prouver par
l'oracle.

## Prérequis
- EP-1 terminée et publiée (type `projet` connu de lepton et des schémas).
- Clone noyau `master` 0c2e43e ; `scion/CMakePresets.json` : 16 presets de carte, 8
  `LEPTON_MKCONF`.
- Graine de référence : `.scion.sources.list` à 14 entrées.
- Oracle de référence du Mac : `doc/devenv/rapports/oracles/env-52-apres/`, ou le dernier oracle
  Mac valide (à relever).
- Skills `lepton-rootstock`, `lepton-oracle`, `lepton-cibles`. `gh` authentifié (usage au PA-E7).
- Branches `espace-projet/ep-3` : clone noyau, graine de référence, lepton-tools ; clones BSP
  selon le PA-E6.

## Tâches

### 1. Audit et oracle avant (lecture seule) → PA-E6
Rapport `doc/espace-projet/rapports/ep-3-lepton-basic.md`. Travail sur une copie de
`<ROOTSTOCK>`, sans `build/`, sous `~/lepton-tools-dev/essais/ep-3-copie` (skill
`lepton-rootstock`).
- Recompter : `git -C <clone noyau> ls-files scion/sys/user/tauon-basic | wc -l` (51 attendus) ;
  les 15 fichiers ; chaque `src_file` des 5 XML (seuls `etc/<carte>/.boot` et `.init` attendus).
- Rejouer `grep -rn 'tauon[-_]basic'` sur le clone noyau, lepton-tools, la graine de référence,
  les clones famille et BSP, `.claude/skills/`. Comparer à la liste de `CADRAGE.md` §2.5 et aux
  trois points de T10 ; tout écart est rapporté. Les occurrences de `tests/board_net.py` et de
  `tests/net_qemu.py` sont à classer (exemple de documentation, ou chemin lu).
- Relever tout fichier généré par mklepton qui porte un chemin de XML ou de `src_file`, et si
  l'un d'eux entre dans le binaire.
- Relever quels tests citant un fichier repris sont joués sur macOS, lesquels seulement sur
  Debian ou en CI (`net.ping_ftpd`, `board.net`) : l'oracle du Mac ne couvre que les premiers.
- Relever, sur un rootstock d'essai à graine de projet, que la construction ne lit aucun des 15
  fichiers du noyau (les graines de projet ont leur copie du XML).
- Oracle avant (skill `lepton-oracle`) : hôte et 16 presets, fumée et banc KAL QEMU.

Proposer, sans rien modifier :
- clé scion et emplacement du clone du greffon (convention des BSP :
  `depots/lepton/bsp-<nom>/master`, clé `bsp-<nom>`), branche, manifeste `projet` ;
- arborescence sous `scion/sys/user/lepton-basic/` (sous-répertoire `etc/` conservé ou non) ;
- historique git des 15 fichiers : repris ou copie simple ; visibilité, licence et `README` du
  dépôt : `<À CONFIRMER au PA-E6>` ;
- T4 : presets du noyau citant un chemin fourni par un autre dépôt ; source de
  `seed new --mkconf` pour `tests/test_milestone2.py` et `scripts/bout-en-bout.sh`, une graine de
  projet ne greffant pas ce greffon ;
- T10 : sort de `host.mklepton_format`, des empreintes des cartes portées (régénérées, ou jeu
  réduit), de `LEPTON_NET_TEST_FTP_REFERENCE` des 5 BSP ;
- ordre de publication des dépôts touchés, sans état intermédiaire cassé pour qui met à jour ;
- version ou tag du noyau après amputation : `<À CONFIRMER au PA-E6>`.

**PA-E6** : l'utilisateur valide. Aucune modification avant la réponse.

### 2. Greffon projet (copie d'essai)
- Dépôt git local du greffon, greffé en `file://` dans la copie d'essai.
- Commit mécanique : les 15 fichiers aux chemins retenus, contenu inchangé (`cmp` à la source).
- Commit séparé : `src_file` réécrits par un script rejouable, versionné dans
  `doc/espace-projet/rapports/ep-3-lepton-basic/` ; aucune autre ligne des XML ne change
  (`diff` : lignes `src_file` seulement).
- Manifeste de type `projet` (schéma d'EP-1).

### 3. Noyau, graine de référence, BSP (copie d'essai seulement)
Les clones de `<ROOTSTOCK>` ne sont touchés qu'après le PA-E7.
- Clone noyau de la copie : `git rm` des 15 fichiers ; `LEPTON_MKCONF` de `CMakePresets.json`,
  tests hôte : selon le PA-E6, forme des chemins inchangée. Commits séparés.
- BSP de la copie : `LEPTON_NET_TEST_FTP_REFERENCE` selon le PA-E6.
- Graine de référence de la copie : greffon ajouté par scion (15 entrées dans
  `.scion.sources.list`).
- `scion graft` ; `lepton check` code 0.

### 4. Références de lepton-tools
Selon le PA-E6 : `scripts/bout-en-bout.sh`, `tests/test_milestone2.py`, `schemas/exemples/`,
`README.md`. `pytest` et `scripts/valider-schemas.sh` verts.

### 5. Oracle après
Hôte et 16 presets : binaires identiques à l'oracle avant ; tests hôte verts, écarts
d'empreintes limités à ceux retenus au PA-E6 ; fumée et banc KAL QEMU. Liste `chemin -> cible` du
trunk : 15 chemins retirés, ceux du greffon ajoutés, aucun autre écart.

### 6. Clôture → PA-E7
**PA-E7** : rapport et oracle ; création du dépôt GitHub par `gh` (accord explicite, commande
montrée avant) ; report des commits sur les clones de `<ROOTSTOCK>` ; pushs dans l'ordre du PA-E6
(PA-P) ; `graft-update` de `<ROOTSTOCK>` (PA-P) ; sort de la copie d'essai. Cartes : validées en
EP-5 et EP-6 ; ici, aucune écriture flash.

## Critères de validation
- [ ] PA-E6 et PA-E7 tranchés et consignés ; T10 arbitrée.
- [ ] `git -C <clone noyau> ls-files scion/sys/user/tauon-basic | wc -l` → 36.
- [ ] `git -C <clone noyau> diff --stat master -- scion/tests/host` : seules les modifications
      retenues au PA-E6 ; les 8 lignes Olimex de `mklepton_empreintes.sha256` inchangées ;
      `ctest -L host` vert.
- [ ] `LEPTON_MKCONF` de `CMakePresets.json` conformes au PA-E6.
- [ ] Les 5 XML du greffon ne diffèrent de leur source que par les lignes `src_file`.
- [ ] Binaires de l'hôte et des 16 presets identiques à l'oracle avant ; tout écart expliqué.
- [ ] `lepton check` code 0 sur `<ROOTSTOCK>` après application ; `pytest` de lepton-tools vert.
- [ ] Un rootstock d'essai à graine de projet, regreffé sur le noyau amputé, construit comme avant.

## Pièges connus
- Les fichiers du clone noyau sont sous `scion/` : `git ls-files sys/user/tauon-basic` rend 0.
- Le répertoire s'appelle `lepton-basic`, les XML gardent `tauon_basic` dans leur nom (C6) : ne
  pas les renommer.
- 3 `.DS_Store` traînent sous `sys/user/tauon-basic` : ni repris ni commités.
- Un clone sur `espace-projet/ep-3` est hors de sa version déclarée : `graft-update` le refuse
  jusqu'à la fusion dans sa branche par défaut (`doc/devenv/rapports/env-29-scion.md` §4).
- Tant que le noyau amputé n'est pas publié avec la graine et les BSP, un rootstock mis à jour à
  moitié a des presets sans XML : d'où l'ordre du PA-E6.
- En régime de référence, `generate` écrit l'espace à la racine du rootstock (C2 révisée, C8
  annotée au PA-E1) ; le comportement de lepton avec ce greffon est celui retenu au PA-E2 (T8).
- Les rootstocks de la VM et les rootstocks d'essai du Mac se regreffent en EP-8, pas ici.

## À la fin de l'étape
`STATUS.md` : statut, branches, §Emplacements (dépôt, clé et clone du greffon), §Versions
(noyau, graine de référence, BSP), décisions PA-E6 et PA-E7, journal. `HORS-PLAN.md` : H2 et H5
mis à jour (compte réel du résidu). Passation `handoff/ep-3.md`.
