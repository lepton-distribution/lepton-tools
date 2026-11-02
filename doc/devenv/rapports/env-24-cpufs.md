# ENV-24 — Dimensionnement automatique du cpufs : rapport

Session du 2026-11-02. Branches `devenv/env-24` : lepton-tools (depuis `main` 26c3149), clone noyau
(depuis `master` 0a6df02).

## 1. Audit (lecture seule)

Méthode : chaque XML copié dans le scratchpad de la session, avec ou sans `size`/`node`
(`sed -E 's/<cpufs size="[0-9]+" node="[0-9]+" /<cpufs /'`), passé au mklepton hôte
(`<ROOTSTOCK>/build/host/mklepton`, `SOURCE_DATE_EPOCH=0`) avec les mêmes quadruplets
(sortie, XML, fréquence, en-tête) que `tests/host/mklepton_empreintes.sh`. Aucune écriture dans le
trunk ni dans `build/`.

### 1.1 XML × presets × tailles

| XML (`sys/user/tauon-basic/etc/`) | Presets (`LEPTON_MKCONF`) | Imposé `size`/`node`/`blocksz` | Calculé `size`/`node` | Écart d'image (octets) |
| --- | --- | --- | --- | --- |
| `mkconf_tauon_basic_qemu_mps2.xml` | `qemu-mps2-an386-{embos,freertos}{,-soft}`, `qemu-mps2-an500-{embos,freertos}` (6) ; test `host.mklepton_format` | 128000 / 256 / 256 | 5939 / 22 | −122061 |
| `mkconf_tauon_basic_nucleo_f439zi.xml` | `nucleo-f429zi-{embos,freertos}`, `nucleo-f439zi-{embos,freertos}` (4) | 128000 / 256 / 256 | 5939 / 22 | −122061 |
| `mkconf_tauon_basic_stm32f746g_disco.xml` | `stm32f746g-disco-{embos,freertos}` (2) | 128000 / 256 / 256 | 5939 / 22 | −122061 |
| `mkconf_tauon_basic_nucleo_wl55jc1.xml` | `nucleo-wl55jc1-{embos,freertos}` (2) | 8000 / 128 / 64 | 1755 / 17 | −6245 |
| `mkconf_tauon_basic_samd21_xplained_pro.xml` | `samd21-xplained-pro-{embos,freertos}` (2) | 3072 / 64 / 64 | 1706 / 15 | −1366 |
| `mkconf_tauon_basic_lwip_stm32f4-olimex-p407.xml` | aucun preset ; jeu d'essai de `host.mklepton` (`mklepton_check.cmake`) et de `host.mklepton_empreintes` | 64000 / 256 / 256 | 41399 / 50 | −22601 |

Sorties de mklepton avec et sans `size`/`node` : `kernel_mkconf.h`, `dev_mkconf.c`,
`bin_mkconf.c`, `.boot`, `.mount` identiques (hors la ligne `//generated from <chemin>`, propre
à l'essai) ; seuls `dev_dskimg.c` et `.fsflash.o` changent. `dev_dskimg.h` inchangé.

### 1.2 Placement de l'image et écart de sections attendu

- `dev_dskimg.c` : `const unsigned char filecpu_memory[]` et `const unsigned long
  filecpu_memory_size`. L'oracle `env-20-apres` relève `filecpu_memory T 0001f401` (128001)
  pour `qemu-mps2-an386-embos`, `T 00001f41` (8001) pour WL55, `T 00000c01` (3073) pour SAMD21 :
  l'image est en `.text` (flash), pas en `.rodata` séparée ni en `.data`.
- Écart attendu par preset : `.text` diminuée de l'écart d'image (±alignement) ;
  `filecpu_memory` de même taille que l'image + 1 ; `.data`, `.bss` et les autres symboles
  inchangés. Aucune RAM libérée (image en flash).

### 1.3 Contenu du cpufs (identique pour les 5 XML des presets, à la carte près)

`/usr/sbin` : `initd lsh mount umount ls ps kill cat uname pwd echo` ; `qemu_mps2`, `f439zi`,
`f746` ajoutent `/usr/sbin/net` (`ifconfig`, `tsterrno`) et `/usr/bin/net` (`ftpd`). Fichiers :
`/usr/etc/.boot`, `/usr/etc/.init` (WL55, SAMD21 : `echo <carte>` ; autres : `ifconfig addif …`,
`ftpd&`). Olimex : en plus `.mount` et les pages `bin/net/html`, `bin/net/cgi-bin`.

### 1.4 Écritures dans le cpufs à l'exécution

- Montage (`core-segger/kernel.c:461`, `core-freertos/kernel.c:464`) : `/` est le rootfs en RAM
  (`_kernel_warmup_rootfs`), le cpufs est monté en `ufs` sur `/usr` depuis `/dev/hd/hda`.
- Pilote `dev/dev_cpufs/dev_cpufs.c:180` : `dev_cpufs_write` renvoie toujours −1 (« read only
  mode ») ; l'image est `const` en flash. Aucune écriture n'aboutit, quelle que soit la taille.
- Tests : fumée (`tests/smoke_lsh.py` : `uname -a`, `echo <jeton> > /dev/ttys1`) ; réseau
  (`net_qemu.py`, `board_net.py` : FTP `LIST` et `RETR`, `net/tsterrno`, `ps`) ; radio
  (`board_radio.py` : `/dev/radio`) ; endurance (`ls /usr/sbin`, `cat /usr/etc/.boot`, `pwd`) ;
  banc KAL (semihosting, sans système de fichiers). Aucune écriture sous `/usr`.
- Conclusion : aucun XML n'est incompatible avec le dimensionnement au plus juste.

### 1.5 Contrôle `mklepton_format_check.cmake`

Ligne 18-19 : exige `<cpufs size="…" node="…" ` dans le XML de base (`qemu_mps2`), puis les
retire pour la variante automatique. Une fois `qemu_mps2` sans `size`/`node`, le test échoue.
Les variantes 2 (automatique relu par `ufs_check`) et 3 (trop petit refusé, minimum exact
accepté et identique) restent pertinentes.

### 1.6 Graines de projet des rootstocks d'essai

Copies (`seed mkconf import` / `seed new --mkconf`) avec valeurs imposées :
`essais/env-9` (`mkconf_env9.xml`, 128000/256), `essais/env-11/{qemu,qemu-gra2,f429zi}`
(128000/256), `essais/env-11/wl55jc1` (8000/128), `essais/env-11/bout-en-bout`
(128000/256 ; `scripts/bout-en-bout.sh` recopie `mkconf_tauon_basic_qemu_mps2.xml` du trunk à
chaque exécution, donc suivra le noyau à la prochaine relance).

### 1.7 Autres mentions

- `doc/migration/mklepton.md:60` (clone noyau) : `<cpufs size node blocksz …>` sans indiquer
  que `size` et `node` sont facultatifs.
- lepton-tools `schemas/exemples/*.xml` : `size`/`node` imposés ; exemples du schéma XSD (qui
  admet les deux formes), sans lien avec les images construites.

## 2. Propositions soumises au PA-35

| # | Objet | Proposition |
| --- | --- | --- |
| P-1 | XML passés au dimensionnement automatique | Les 5 XML des presets : `qemu_mps2`, `nucleo_f439zi`, `stm32f746g_disco`, `nucleo_wl55jc1`, `samd21_xplained_pro` (cpufs en lecture seule par construction, aucun test n'écrit). |
| P-2 | XML Olimex | Garder `size`/`node` imposés : seul XML à valeurs imposées, il continue d'exercer ce chemin dans `host.mklepton` et les empreintes ; empreintes Olimex inchangées. |
| P-3 | `mklepton_format_check.cmake` | Contrôle de cohérence : accepter un XML de base avec ou sans `size`/`node` (retrait s'ils sont présents) ; variantes 2 et 3 conservées ; commentaire d'en-tête mis à jour. |
| P-4 | Critère de non-régression | Par preset : seuls `.text` (écart = écart d'image ± alignement) et la taille de `filecpu_memory` changent ; tous les autres symboles et sections identiques ; fumée et banc KAL identiques (QEMU, cartes). |
| P-5 | Graines d'essai | Hors périmètre (copies figées d'essais clos) ; `bout-en-bout` suit le noyau à sa prochaine relance. |
| P-6 | `doc/migration/mklepton.md` | Préciser `size`/`node` facultatifs (commit de documentation dans le clone noyau). |
| P-7 | `blocksz` | Inchangé (256, ou 64 pour WL55 et SAMD21). |

## 3. Décisions du PA-35 (utilisateur, 2026-11-02)

- P-1 retenue : les 5 XML des presets passent au dimensionnement automatique.
- P-2 retenue : l'Olimex garde `size`/`node` imposés.
- P-3 retenue : contrôle de cohérence.
- P-4, P-5, P-6 retenues ; P-7 (`blocksz` inchangé) implicite dans la question des XML.
- Cartes accordées (écriture flash) : NUCLEO-F429ZI, NUCLEO-WL55JC1, STM32F746G-DISCO,
  SAMD21 Xplained Pro.
- Amendement (utilisateur, 2026-11-02, après le lot 1) : l'écart admis comprend aussi les
  sections `.debug_*` lorsque leur écart est exactement celui de `dev_dskimg.o`.

## 4. Modification par lots

Contrôle de format : clone noyau 1d1db90 (`mklepton_format_check.cmake`, contrôle de cohérence) ;
essayé sur le XML actuel (conforme), une copie sans `size`/`node` (conforme) et une copie avec
`node` seul (refus « avec size et node, dans cet ordre, ou sans aucun des deux attendu »).

Pour chaque lot : un commit du XML, un commit de génération de `mklepton_empreintes.sha256`
(`mklepton_empreintes.sh --out`), puis `rejouer-oracle.sh` des presets du lot
(`rapports/oracles/env-24-lot-<xml>/`) et `comparer-oracle.py` contre `env-24-avant`. Écart
DWARF attendu : `dev_dskimg.c` imposé et automatique compilés seuls avec la commande du preset
(`compile_commands.json`), `arm-none-eabi-size -A`.

### Lot 1 — `qemu_mps2` (7f3dd51, empreintes 0788892)

Empreintes mklepton : seuls `.fsflash.o` et `dev_dskimg.c` des sorties an386 et an500 changent.
host `ctest` 7/7 ; banc KAL (fumée comprise) 18/18 (an386, an500) et 14/14 (`-soft`).

| Preset | `.text` | `filecpu_memory` | `.debug_info` / `.debug_abbrev` | Autres | Classement |
| --- | --- | --- | --- | --- | --- |
| `qemu-mps2-an386-embos` | 274716 → 152652 (−122064) | 0x1f401 → 0x1734 | −7 / −17 | aucun | cpufs |
| `qemu-mps2-an386-freertos` | 281464 → 159400 (−122064) | idem | −7 / −17 | aucun | cpufs |
| `qemu-mps2-an386-embos-soft` | 274428 → 152364 (−122064) | idem | −7 / −17 | aucun | cpufs |
| `qemu-mps2-an386-freertos-soft` | 281128 → 159064 (−122064) | idem | −7 / −17 | aucun | cpufs |
| `qemu-mps2-an500-embos` | 271916 → 149852 (−122064) | idem | −7 / −17 | aucun | cpufs |
| `qemu-mps2-an500-freertos` | 278664 → 156600 (−122064) | idem | −7 / −17 | aucun | cpufs |

`.text` : −122061 (image) −3 (alignement). DWARF : `dev_dskimg.o` seul, `.debug_info` 123 → 116,
`.debug_abbrev` 90 → 73 (`DW_AT_upper_bound` 0x1f400 → 5939).

### Lots 2 à 5 — cartes (construction et capture)

| Lot | XML (commit, empreintes) | Presets | `.text` | `filecpu_memory` | DWARF (`.debug_info` / `.debug_abbrev`) = `dev_dskimg.o` | Classement |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | `nucleo_f439zi` (3194f19, 977da08) | `nucleo-f429zi-{embos,freertos}`, `nucleo-f439zi-{embos,freertos}` | −122064 | 0x1f401 → 0x1734 | −7 / −17 (oui) | cpufs |
| 3 | `stm32f746g_disco` (46f3e02, 792c188) | `stm32f746g-disco-{embos,freertos}` | −122064 | 0x1f401 → 0x1734 | −7 / −17 (oui) | cpufs |
| 4 | `nucleo_wl55jc1` (233ec3c, 324d2eb) | `nucleo-wl55jc1-{embos,freertos}` | −6248 (image −6245, alignement −3) | 0x1f41 → 0x6dc | −5 / −17 (oui : 121 → 116, 90 → 73) | cpufs |
| 5 | `samd21_xplained_pro` (9db0630, 816715b) | `samd21-xplained-pro-{embos,freertos}` | −1368 (image −1366, alignement −2) | 0xc01 → 0x6ab | aucun (oui : 116 et 73 inchangés) | cpufs |

Chaque lot : seuls `.fsflash.o` et `dev_dskimg.c` des sorties du XML changent dans les empreintes
mklepton ; host `ctest` 7/7 ; aucun écart « autre ».

Documentation : `doc/migration/mklepton.md` (7a32352, P-6) ; commentaire du contrôle précisé
(f3ecf8c) : mklepton accepte `size` ou `node` seul (l'autre est calculé), la règle « tous deux ou
aucun » ne vaut que pour le mkconf de base du test.

## 5. Contrôles (PA-36)

Oracle après `rapports/oracles/env-24-apres/` (construction à neuf, host d'abord, mêmes arguments
que l'oracle avant) : « tout a réussi ». `comparer-oracle.py` `env-24-avant` → `env-24-apres` :
sur les 16 presets, écarts identiques à ceux des lots (§4), tous classés cpufs. Empreintes
mklepton : 14 lignes changées (`.fsflash.o` et `dev_dskimg.c` des 7 sorties de presets) ;
Olimex inchangé ; `mklepton-empreintes.sha256` de l'oracle = référence du clone (816715b).

Fumée QEMU : filtre E-4 d'ENV-19 (date de compilation, jeton `lepton-uart1-<n>`, chiffre devant
l'invite, `rcv SIGCHLD`, lignes vides) : 0 ligne d'écart sur 6 presets. Banc KAL QEMU : même
liste de cas, mêmes résultats (18/18 an386 et an500, 14/14 `-soft`).

| Preset | Sections/symboles | Empreinte | Fumée | Banc KAL | Écarts expliqués |
| --- | --- | --- | --- | --- | --- |
| `host` | — | — | — | `ctest` 7/7 | empreintes mklepton (§4) |
| `qemu-mps2-an386-{embos,freertos}` | cpufs seul | diffère | identique | 18/18, même liste | lot 1 |
| `qemu-mps2-an386-{embos,freertos}-soft` | cpufs seul | diffère | identique | 14/14, même liste | lot 1 |
| `qemu-mps2-an500-{embos,freertos}` | cpufs seul | diffère | identique | 18/18, même liste | lot 1 |
| `nucleo-f429zi-*`, `nucleo-f439zi-*` | cpufs seul | diffère | carte : voir §6 | carte : voir §6 | lot 2 |
| `stm32f746g-disco-*` | cpufs seul | diffère | carte : voir §6 | carte : voir §6 | lot 3 |
| `nucleo-wl55jc1-*` | cpufs seul | diffère | carte : voir §6 | carte : voir §6 | lot 4 |
| `samd21-xplained-pro-*` | cpufs seul | diffère | carte : voir §6 | carte : voir §6 | lot 5 |

## 6. Cartes (PA-35 : F429, WL55, F746, SAMD21)

Procédure (forme d'ENV-20) : reconfiguration de `<ROOTSTOCK>/build/<P>` avec
`-DLEPTON_BOARD_SERIAL_PORT` (et `-DLEPTON_NET_TEST_HOST_IP` pour le réseau), `cmake --build`
(construit `tests/kal/kal_bench.elf`, absent des constructions `--carte` de l'oracle),
recapture de `lepton.elf` comparée à `env-24-apres/<P>` (code 0 exigé), puis
`ctest --preset <P> -L board`. Journaux : `env-24-apres/<P>/carte.log`, `carte-detail.log`
(`LastTest.log`), `fumee-carte.log`, `reseau-carte.log`, `carte-config.log`.

Réseau (ajout au plan, décision de l'utilisateur, 2026-11-02) : `board.net` (ping, FTP `LIST`,
`RETR /usr/etc/.boot` comparé à la source, errno) lit le cpufs ; Mac en 192.168.2.10 sur `en0`
(câble direct), carte en 192.168.2.5 (`.init`).

### NUCLEO-F429ZI (ST-LINK/V2-1 0672FF495252717267243842, `/dev/cu.usbmodem1454403`)

| Binaire | `lepton.elf` / oracle après | Résultat | Fumée | Réseau |
| --- | --- | --- | --- | --- |
| `nucleo-f429zi-embos` | 0 écart | 20/20 | `cortexM4-stm32f4` | ping 3/3, LIST 13 entrées, RETR 57 octets identique, ECONNRESET=15 |
| `nucleo-f429zi-freertos` | 0 écart | 20/20 | `cortexM4-stm32f4` | idem |
| `nucleo-f439zi-embos` (sur F429, comme ENV-20 E-5) | 0 écart | 20/20 | `cortexM4-stm32f4` | idem |

Fin : image `nucleo-f429zi-embos` d'ENV-24 remise en flash (« Verified OK ») ; l'image d'avant
ENV-24 n'existe plus (oracle construit à neuf).

Incidents :
- Premier passage : `kal.board_flash` en échec (« couldn't open … kal_bench.elf ») :
  `kal_bench` non construit ; aucun écrit en flash du banc ; construction ajoutée au script.
- Réseau, premier essai en échec (ARP « incomplete ») : erreur de la session. L'adresse avait été
  ajoutée en alias sur `en17` (adaptateur à lien actif, sans rapport avec la carte) au lieu de
  `en0` ; la route /24 d'`en17` l'emportait. Un essai témoin (XML d'avant ENV-24, construit dans
  `<ROOTSTOCK>/build/env-24-temoin`, même code qu'`env-24-avant` à `.debug_line`/`.debug_str`
  près) a échoué de même, d'où une conclusion erronée (« défaut antérieur ») retirée depuis.
  Correction par l'utilisateur (`sudo ifconfig en17 -alias 192.168.2.10`) ; route par `en0`,
  ping 3/3, puis 20/20. Répertoires du témoin supprimés. Précision de l'utilisateur : le câble
  Ethernet n'était pas non plus branché lors du premier essai.
- `ls /usr/bin/net` : erreur, dette connue de la migration (`MIGRATION-STATUS.md:272`, `/usr/bin/net`
  créé sans `/usr/bin`) ; sans lien avec ENV-24.

### STM32F746G-DISCO (ST-LINK/V2-1, `/dev/cu.usbmodem1454303`)

| Binaire | `lepton.elf` / oracle après | Résultat | Fumée | Réseau |
| --- | --- | --- | --- | --- |
| `stm32f746g-disco-embos` | 0 écart | 20/20 | `cortexM7-stm32f7` | ping 3/3, LIST 13 entrées, RETR 57 octets identique, ECONNRESET=15 |
| `stm32f746g-disco-freertos` | 0 écart | 20/20 | `cortexM7-stm32f7` | idem |

Fin : image `stm32f746g-disco-embos` remise en flash (« Verified OK »). Incident : premier
lancement sur l'ancien port (`1454403`, réénumération USB) : `smoke_lsh` en échec à l'ouverture
du port, avant tout reset ou flash ; relancé sur `1454303`.
