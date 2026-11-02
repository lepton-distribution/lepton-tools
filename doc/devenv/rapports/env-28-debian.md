# ENV-28 — Validation Debian groupée (ENV-22 à ENV-27) — 2026-11-02

Session VM Debian (`debian-linux-vm`) conduite selon la consigne `env-28-debian.md` (lepton-tools
`devenv/env-28` b8ff911, blob 61a35cc, SHA-256 `d40a5136…2c92da1` vérifiée ; ordre `R28-1` de la
session Mac `validate-env-22-27-debian`, décisions PA-43). La session exécute, constate et
rapporte ; aucune correction de code. Journaux : `~/env-28-journaux/` sur la VM (hors git) ;
rootstocks conservés : `~/lepton-tools-dev/essais/env-28-debian` (`$R`) et `env-14-debian` (`$U`).

Bilan : C1 à C8 conformes. C3 jugé sur le second `graft-update` de `$U`, après l'écart E-1 (premier
`graft-update` en échec, précondition non vérifiée au §5) et le correctif accordé par PA-43 (2).

## 1. Hôte et versions (§5, §6)

| Élément | Valeur |
| --- | --- |
| Système | Linux x86_64, Debian 13.7, noyau 6.12.107+deb13-amd64, utilisateur `lepton-user` |
| git | 2.47.3 |
| scion | 0.5.2.0 avant ; **0.5.3.0** après `install-debian.sh` (`git+…/seed.scions.git@0.5.3.0`) |
| lepton | 0.1.0 avant (`devenv/env-21` 65b19f7, `scion 0.5.2.0 (requis ≥ 0.5.2.0)`) ; 0.1.0 après `pipx install --force` de `devenv/env-28` b8ff911 (`scion 0.5.3.0 (requis ≥ 0.5.3.0)`) |
| arm-none-eabi-gcc | 14.2.1 20241119 (paquet Debian `15:14.2.rel1-1`) ; gcc hôte 14.2.0 (Debian 14.2.0-19) |
| cmake / ninja | 3.31.6 / 1.12.1 |
| QEMU | 10.0.13 (Debian 1:10.0.13+ds-0+deb13u1) |
| Python | 3.13.5 |
| Outils de débogage | openocd 0.12.0 ; clangd 19.1.7 (3+b1) ; doxygen 1.9.8 ; spatch 1.3 ; cloc 2.04 ; xmllint 20914 |
| VSCodium | 1.135.06055 (dpkg 1.135.06055) ; 12 extensions (`~/env-28-journaux/6.2-extensions.txt`), dont `vadimcn.vscode-lldb@1.12.3`, `lepton-distribution.lepton@0.5.1`, `ms-vscode.cmake-tools@1.24.42`, `marus25.cortex-debug@1.13.0-pre6`, `llvm-vs-code-extensions.vscode-clangd@0.6.0` |
| embOS | présent : `LEPTON_EMBOS_ROOT=~/lepton/third_party/embos/cortexm-gcc/5.20.0.0` |
| Espace | `/home` 26 Go (19 Go libres) ; `/tmp` 747 Mo (687 Mo libres) |
| lepton-tools | propre (sur `devenv/env-21-debian`) ; après `fetch`, `devenv/env-28` = b8ff911 |
| Clone noyau | propre, `master` ; avance rapide 40d7197 → 0c0cc4f (18 commits) ; `install-debian.sh:55` `SCION_REF="${SCION_REF:-0.5.3.0}"` |
| `git ls-remote` | scion tag `0.5.3.0^{}` ad292ee ; graine `original-tree` 15740f9 ; 13 dépôts `master` aux commits du §1 de la consigne |

## 2. Critères (§12)

| Critère | Attendu | Constaté | Verdict |
| --- | --- | --- | --- |
| C1 scion et lepton | `ls-remote` conforme ; scion 0.5.3.0 par `install-debian.sh` ; `pipx` code 0 ; lepton 0.1.0, scion 0.5.3.0 accepté | `ls-remote` conforme (§1) ; `install-debian.sh` installe scion 0.5.3.0 depuis le tag ; `6.2-lepton.log` code 0 ; `lepton 0.1.0`, `scion 0.5.3.0 (requis ≥ 0.5.3.0)` ; `pipx list` : `lepton 0.1.0`, `scion 0.5.3.0` | conforme |
| C2 Scripts d'installation | `install-debian.sh` (0c0cc4f) code 0 ; `install-vscodium.sh` code 0 deux fois, `changements 0` à la seconde ; CodeLLDB 1.12.3 | lancés par l'utilisateur, sans `SCION_REF` ni `SCION_SPEC` ; quatre codes 0 ; `changements 0` aux deux exécutions d'`install-vscodium.sh` ; `vadimcn.vscode-lldb@1.12.3` | conforme |
| C3 Graine et rootstock | §7.1 : graine 0f1275a → 15740f9 par `graft-update`, 14 entrées, clones au §1, 3956 liens, 0 cassé, 0 régulier ; §7.2 : idem, liste identique à `$U` | §7.1 : 1er `graft-update` code 1 (E-1), graine avancée 0f1275a → 15740f9 ; après correctif, 2e `graft-update` code 0, 0 conflit, 14 entrées, 13 clones au §1 et propres, 3956 liens (3929 avant), 0 cassé, 0 régulier. §7.2 : `rootstock-install`, `seed-add`, `graft` code 0 ; 14 entrées ; 13 clones au §1 (sur `master`) ; 3956 liens, 0 cassé, 0 régulier, 0 `.DS_Store` ; liste des liens identique à `$U` | conforme (sur le 2e `graft-update`) |
| C4 Constructions | host 7/7, empreintes mklepton = `env-27-apres` ; 16 presets ; QEMU fumée, banc 20/20, 16/16, 19/19 ; `comparer_R21-1` limité au tableau §8.2 ; `f429→f439` 0 | `rejouer-oracle.sh` code 0 (« tout a réussi ») ; host 7/7 ; empreintes mklepton identiques à `env-27-apres` (50 lignes), 14 lignes différentes contre `env-21-debian` (7 `.fsflash.o`, 7 `dev_dskimg.c`) ; 16/16 construits ; fumée réussie ; banc an386 20/20, an386 soft 16/16, an500 19/19 ; `comparer_R21-1` 1 partout, écarts limités au tableau (§3) ; `f429→f439` embos 0, freertos 0 ; trunk : 0 cassé, 0 régulier | conforme |
| C5 DBG-5 et DBG-4 | `check`, `generate` code 0 sur `$R` ; 23 lancements, 7 `lldb`, 10 `svdFile`, SVD aux sommes ; sorties `mklepton` = construction ; arrêt dans `main` (A et B) | `check` code 0 (« 19 fichier(s) conforme(s) »), `generate` code 0 ; 23 `"request"`, 7 `"type": "lldb"`, 10 `"svdFile"` (2 par fichier, sous `$R/trunk`) ; 5 sommes SVD identiques ; 0 fichier régulier ; `mklepton` du lancement : code 0, 6 fichiers identiques à `build/qemu-mps2-an386-embos/generated/board` ; forme A et forme B : arrêt dans `main` (§4) | conforme |
| C6 Tests du greffon | `qemu-mps2-an386.peripheriques` listé et réussi dans les 4 presets an386 ; absent d'an500 | an386 (4) : listé une fois, `-L greffon:` = 2, `Passed` (0,70 s) dans chaque `banc-kal.log` ; an500 : 0 test du greffon, liste identique à R21-1 | conforme |
| C7 Graine de projet `env11` | `check`, `generate` code 0 ; `check`, presets, graine identiques ; espace : ajouts DBG-5 seuls | régénération puis relevé au §6.1 (« inchangé ») ; après réinstallation : codes 0 ; graine inchangée, sortie de `check` identique, `CMakeUserPresets.json` identique (d5ee81e4…) ; `env11.code-workspace` 0c06a5f7… → b2c7b8a4…, différence limitée aux ajouts DBG-5 (§5) ; 0 `svdFile` | conforme |
| C8 Nettoyage | `env-21-debian` et `~/env-21-journaux` supprimés par l'utilisateur, taille relevée | tailles 363 Mo et 1,2 Mo ; `rm -rf` lancé par l'utilisateur ; `ls -d` : absents ; `$R`, `$U`, `$J` conservés | conforme |

Fumée (`qemu-mps2-an386-freertos/fumee.log`) : `uname -a` →
`lepton-cortexm4-32  4.10.0.2 Nov  2 2026-16:43:10 cortexM4-qemu-mps2-an386`.

## 3. Presets (§8)

| Preset | Construction | Fumée | Banc KAL | Symboles (R28-1 / R21-1 / Mac `env-27-apres`) | `comparer_R21-1` | `comparer_Mac` |
| --- | --- | --- | --- | --- | --- | --- |
| host | oui | — | ctest 7/7 | — | empreintes = `env-27-apres` | — |
| qemu-mps2-an386-embos | oui | oui | 20/20 | 1599 / 1599 / 1583 | 1 | 1 |
| qemu-mps2-an386-embos-soft | oui | oui | 16/16 | 1596 / 1596 / 1580 | 1 | 1 |
| qemu-mps2-an386-freertos | oui | oui | 20/20 | 1639 / 1639 / 1623 | 1 | 1 |
| qemu-mps2-an386-freertos-soft | oui | oui | 16/16 | 1638 / 1638 / 1622 | 1 | 1 |
| qemu-mps2-an500-embos | oui | oui | 19/19 | 1561 / 1561 / 1545 | 1 | 1 |
| qemu-mps2-an500-freertos | oui | oui | 19/19 | 1601 / 1601 / 1585 | 1 | 1 |
| nucleo-f429zi-embos | oui | — | — | 1793 / 1793 / 1777 | 1 | 1 |
| nucleo-f429zi-freertos | oui | — | — | 1833 / 1833 / 1817 | 1 | 1 |
| nucleo-f439zi-embos | oui | — | — | 1793 / 1793 / 1777 | 1 | 1 |
| nucleo-f439zi-freertos | oui | — | — | 1833 / 1833 / 1817 | 1 | 1 |
| nucleo-wl55jc1-embos | oui | — | — | 1230 / 1230 / 1215 | 1 | 1 |
| nucleo-wl55jc1-freertos | oui | — | — | 1276 / 1276 / 1261 | 1 | 1 |
| samd21-xplained-pro-embos | oui | — | — | 941 / 941 / 926 | 1 | 1 |
| samd21-xplained-pro-freertos | oui | — | — | 991 / 991 / 976 | 1 | 1 |
| stm32f746g-disco-embos | oui | — | — | 1640 / 1640 / 1624 | 1 | 1 |
| stm32f746g-disco-freertos | oui | — | — | 1676 / 1676 / 1660 | 1 | 1 |

`f429→f439` (R28-1) : embos 0, freertos 0. Écart de symboles Debian/Mac : 15 ou 16 selon le
preset, inchangé depuis R14-1 (chaînes différentes, `comparer_Mac` 1 attendu).

### Nature des écarts `comparer_R21-1` = 1

Chaque fichier `~/env-28-journaux/8.2-cmp-R21-<preset>.txt` a été lu par script : il ne contient
que les empreintes `.bin`/`.elf`/`.hex`, les sections et le symbole du tableau §8.2 de la consigne,
avec les deltas exacts, et rien d'autre :

| Presets | `.text` | `filecpu_memory` | DWARF | Verdict |
| --- | --- | --- | --- | --- |
| `qemu-mps2-an386-*` (4), `qemu-mps2-an500-*` (2), `nucleo-f429zi-*`, `nucleo-f439zi-*`, `stm32f746g-disco-*` (2 chacun) | −122064 (an386-embos : 279676 → 157612) | `0001f401` → `00001734` | `.debug_abbrev` −17, `.debug_info` −7 | 12/12 conformes |
| `nucleo-wl55jc1-*` (2) | −6248 | `00001f41` → `000006dc` | `.debug_abbrev` −17, `.debug_info` −5 | 2/2 conformes |
| `samd21-xplained-pro-*` (2) | −1368 | `00000c01` → `000006ab` | aucun | 2/2 conformes |

Les variations propres à la chaîne Debian relevées en R21-1 (`.text` de quelques octets,
`.noinit` sur samd21-freertos) sont absentes de `comparer_R21-1` : elles sont inchangées.

## 4. DBG-5 : lancement hôte de `mklepton` (§9.1)

Lancement extrait de `original-tree.code-workspace` (`~/env-28-journaux/9.1-lancement-an386.sh`) :
`PROG=$R/build/host/mklepton`, `CWD=$R/build/.mklepton/qemu-mps2-an386`,
`ARGS=(-s $R/trunk -o $CWD --cpu-freq 25000000 --kernel-config-header
sys/root/src/kernel/dev/bsp/qemu-mps2-an386/include/user_kernel_mkconf.h
sys/user/tauon-basic/etc/mkconf_tauon_basic_qemu_mps2.xml)`, `ENVS=(SOURCE_DATE_EPOCH=0)`,
`TACHE` = « lepton : préparer le débogage de mklepton ».

- Hors débogueur : code 0 ; `diff -r` identique à la construction : 6 fichiers (`bin_mkconf.c`,
  `dev_dskimg.c`, `dev_dskimg.h`, `dev_mkconf.c`, `.fsflash.o`, `kernel_mkconf.h`).
- Forme A, par la session, avec le lldb embarqué par CodeLLDB 1.12.3, en mode batch
  (`9.1-lldb.log`, code 0) : `stop reason = breakpoint 1.1` ; `frame #0: mklepton`main(argc=10,
  argv=…) at mklepton.c:2383:10` ; `(int) argc = 10`. `image lookup -v -n main`
  (`9.1-lldb-source.log`) donne `CompileUnit … file =
  "$R/trunk/tools/mklepton/src/mklepton.c"`, c'est-à-dire le chemin du trunk (le lien pointe vers
  `depots/lepton/original/master/scion/tools/mklepton/src/mklepton.c`).
- Forme B, par l'utilisateur, sous VSCodium (« Déboguer mklepton qemu-mps2-an386
  (mkconf_tauon_basic_qemu_mps2.xml) ») : arrêt dans `main` atteint ; `argc` et `argv` lisibles ;
  source ouvert par le chemin du trunk, dans un seul onglet. Tâche préalable exécutée, vérifiée par
  la session sur le disque : les 6 répertoires `build/.mklepton/<carte>` autres que
  `qemu-mps2-an386` (créé à 16:47 par la session) sont apparus à 16:51:28.59, juste après
  l'écriture de `build/host/.ninja_log` à 16:51:28.24 (tâche dépendante « lepton : mklepton
  (preset host) » ; `mklepton` resté à 16:42, rien à reconstruire).

## 5. Graine de projet `env11` (§10)

`~/env-28-journaux/10-espace-P.diff`. Ajouts seulement :
- lancement `lldb` « Déboguer mklepton qemu-mps2-an386 (mkconf_env11.xml) » en fin de `launch`
  (`program` `$P/build/host/mklepton`, `args` `-s $P/trunk -o $P/build/.mklepton/qemu-mps2-an386 …
  sys/user/env11/etc/mkconf_env11.xml`, `env` `SOURCE_DATE_EPOCH=0`, `preLaunchTask` « lepton :
  préparer le débogage de mklepton ») ;
- tâche « lepton : préparer le débogage de mklepton » juste après « lepton : mklepton (preset
  host) », dont elle dépend ;
- `vadimcn.vscode-lldb` dans les recommandations ; seule ligne retirée :
  `"marus25.cortex-debug"`, réécrite avec une virgule.

## 6. Écarts et constats

- **E-1 (C3, §7.1), premier `graft-update` de `$U` en échec :**
  - Commande : `scion graft-update -v`, lancée par l'utilisateur (le classifieur de la session
    l'avait refusée, E-2), journal `~/env-28-journaux/7.1-graft-update.log` (conservé, code 1).
  - Constaté : graine avancée « 0f1275a -> 15740f9 » ; 14 entrées dans `.scion.grafted.list` ; les
    5 greffons nouveaux clonés puis `git checkout master`, aux commits du §1. Mais `original` est
    resté à e5a5689 (« ENV-14 arbitrages A1 à A3 ») et `family-stm32f4xx` à af964c6 (« ENV-14
    arbitrage A5 ») : les deux clones étaient sur la branche `devenv/env-14` (reflog : « checkout:
    moving from master to devenv/env-14 », 2026-10-30 20:17, validation ENV-14 Debian). Le
    `git pull` de scion a mis à jour `origin/master` sans faire avancer `HEAD`.
  - Effet : l'ancien noyau fournit encore les fichiers depuis déplacés dans les familles :
    **277 conflits** « déjà fourni par « lepton/original::tree », réclamé par … » (208
    `family-stm32f7xx`, 69 `family-samd21`) ; la regreffe échoue et le **trunk est vidé** (il ne
    reste que `.scion.grafted.list` : 0 lien, contre 3929 avant). Clones propres, aucune perte.
  - Cause : précondition non vérifiée au §5 de la consigne (branche courante des clones de `$U`).
  - Correction (PA-43 (2), accordée par l'utilisateur) : clones propres vérifiés ;
    `git -C $U/depots/lepton/{original,family-stm32f4xx}/master switch master` ; `HEAD` encore à
    16a331b et 01b5528, donc `merge --ff-only origin/master` → 0c0cc4f et 8364493, propres. Second
    `graft-update -v` lancé par l'utilisateur (`7.1-graft-update-2.log`) : code 0, 0 conflit,
    3956 liens. La branche `devenv/env-14` reste en local et sur `origin`.
  - Constats sur scion 0.5.3.0, pour une étape ultérieure (aucune modification de scion en
    ENV-28) : (a) `graft-update` fait `git pull` sur la branche courante d'un clone existant, sans
    revenir à la version déclarée (`master` dans `.scion.grafted.list`), alors qu'il fait
    `checkout` de cette version pour les clones nouveaux ; (b) il vide le trunk quand la regreffe
    échoue sur un conflit.
  - À la session Mac : ajouter au §5 des consignes la branche courante de chaque clone d'un
    rootstock existant (`git -C <clone> branch --show-current`).
- **E-2 (§7.1), `graft-update` refusé à la session :** le classifieur de permissions (mode auto)
  a refusé `scion graft-update -v` (« Untrusted Code Integration »). La session ne l'a pas
  contourné ; l'utilisateur l'a lancé les deux fois. En revanche, `scion rootstock-install`,
  `seed-add` et `graft` (§7.2) et `rejouer-oracle.sh` (§8) ont été acceptés.
- **`install-vscodium.sh` (constat) :** `changements 0` dès la première exécution ; l'installation
  de la VM (R21-1) était déjà à jour, CodeLLDB 1.12.3 compris.
- **§11 (constat) :** suppression lancée par l'utilisateur pendant le §8, avant le §9 (pas de
  dépendance) ; absence vérifiée par `ls -d`.

## 7. Journal des messages (§2bis)

| ID | Date | Sens | Résumé |
| --- | --- | --- | --- |
| ORDRE R28-1 | 2026-11-02 | Mac → VM | consigne `env-28-debian.md` @ b8ff911 ; PA-43 : §7.1 accordé, C5 A puis B, C8 accordé, push sur accord |
| ACCUSÉ R28-1 | 2026-11-02 | VM → Mac | §5 conforme, aucun écart visible |
| AVANCEMENT R28-1 | 2026-11-02 | VM → Mac | §6.1 fait, noyau 0c0cc4f ; commandes du §6.2 à l'utilisateur |
| AVANCEMENT R28-1 | 2026-11-02 | VM → Mac | §6 conforme (C1, C2) ; `graft-update` refusé par le classifieur |
| QUESTION R28-1 | 2026-11-02 | VM → Mac | §7.1 en échec (E-1) : options A (switch master + 2e `graft-update`) ou B |
| RÉPONSE R28-1 | 2026-11-02 | Mac → VM | option A accordée (PA-43 (2)) ; §7.2 à poursuivre ; E-1 au rapport |
| AVANCEMENT R28-1 | 2026-11-02 | VM → Mac | §7 conforme (C3, 2e `graft-update`) |
| AVANCEMENT R28-1 | 2026-11-02 | VM → Mac | §11 conforme (C8) |
| AVANCEMENT R28-1 | 2026-11-02 | VM → Mac | §8 conforme (C4, C6) |
| AVANCEMENT R28-1 | 2026-11-02 | VM → Mac | §9 forme A et §10 conformes ; forme B demandée |

## 8. Non fait

- Presets de carte : construits et capturés seulement ; aucun flashage (pas de carte sur la VM).
- Push de `devenv/env-28-debian` : soumis à l'accord explicite de l'utilisateur (PA-P).
