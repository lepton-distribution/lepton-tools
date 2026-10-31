# ENV-21 — Validation Debian groupée (ENV-17 à ENV-20) — 2026-10-31

Session VM Debian (`lepton-vm-debian`) conduite selon la consigne `env-21-debian.md` (lepton-tools
`devenv/env-21` 65b19f7, ordre `R21-1` de la session Mac `validation-debian-groupee-env21`). La
session exécute, constate et rapporte ; aucune correction. Journaux : `~/env-21-journaux/` sur la
VM (hors git) ; rootstock conservé : `~/lepton-tools-dev/essais/env-21-debian`.

Bilan : C1 à C5 conformes. C6 : `check`, `generate`, graine et `CMakeUserPresets.json` identiques ;
`env11.code-workspace` différent (E-1, cause hors ENV-17 à ENV-20). C7 conforme (suppression
lancée par l'utilisateur, E-2).

## 1. Hôte et versions (§5, §6)

| Élément | Valeur |
| --- | --- |
| Système | Linux x86_64, Debian 13.7, noyau 6.12.107+deb13-amd64, utilisateur `lepton-user` |
| git | 2.47.3 |
| scion / lepton | 0.5.2.0 / 0.1.0 avant et après `pipx install --force` (`scion 0.5.2.0 (requis ≥ 0.5.2.0)`) |
| arm-none-eabi-gcc | 14.2.1 20241119 (paquet Debian `15:14.2.rel1-1`) ; gcc hôte 14.2.0 (Debian 14.2.0-19) |
| cmake / ninja | 3.31.6 / 1.12.1 |
| QEMU | 10.0.13 (Debian 1:10.0.13+ds-0+deb13u1) |
| Python | 3.13.5 |
| Outils de débogage | openocd 0.12.0 ; clangd 19.1.7 (3+b1) ; doxygen 1.9.8 ; spatch 1.3 ; cloc 2.04 ; xmllint 20914 |
| VSCodium | 1.135.06055 (dpkg 1.135.06055) ; 12 extensions (`~/env-21-journaux/6.2-extensions.txt`), dont `lepton-distribution.lepton@0.5.1`, `ms-vscode.cmake-tools@1.24.42`, `marus25.cortex-debug@1.13.0-pre6`, `llvm-vs-code-extensions.vscode-clangd@0.6.0` |
| embOS | présent : `LEPTON_EMBOS_ROOT=~/lepton/third_party/embos/cortexm-gcc/5.20.0.0` |
| Espace | `/home` 26 Go (19 Go libres) ; `/tmp` 747 Mo (688 Mo libres) |
| lepton-tools | propre (sur `devenv/env-15-debian`) ; après `fetch`, `devenv/env-21` = 65b19f7 |
| Clone noyau | propre, `master` ; avance rapide 16a331b → 40d7197 (22 commits) ; `install-debian.sh:55` `SCION_REF="${SCION_REF:-0.5.2.0}"` |

## 2. Critères (§11)

| Critère | Attendu | Constaté | Verdict |
| --- | --- | --- | --- |
| C1 lepton | `ls-remote` conforme au §1 ; `pipx` code 0 ; lepton 0.1.0, scion 0.5.2.0 accepté | scion tag `0.5.2.0^{}` 472c12e ; graine 15740f9 ; 13 dépôts `master` aux commits du §1 ; `6.2-lepton.log` code 0 ; `lepton 0.1.0`, `scion 0.5.2.0 (requis ≥ 0.5.2.0)` | conforme |
| C2 Scripts d'installation | `install-debian.sh` code 0 ; `install-vscodium.sh` code 0 deux fois, `changements 0` à la seconde | lancés par l'utilisateur, sans `SCION_REF` ; `install-debian.sh` code 0, « scion 0.5.2.0 : déjà installé » ; `install-vscodium.sh` code 0 deux fois, `changements 0` aux deux | conforme |
| C3 Rootstock neuf | 14 entrées, clones aux commits du §1, 3941 liens, 0 cassé, 0 régulier | `rootstock-install`, `seed-add`, `graft` code 0 ; 14 entrées ; 13 clones aux commits du §1 ; 3941 liens, 0 cassé, 0 régulier, 0 `.DS_Store` | conforme |
| C4 Constructions | host 7/7, mklepton = `env-20-apres` ; 16 presets ; QEMU 19/19 ou 15/15 ; `comparer_R14-1` conforme ; `f429→f439` 0 | `rejouer-oracle.sh` code 0 ; host 7/7 ; empreintes mklepton identiques à `env-20-apres` (50 lignes) ; 16/16 construits ; QEMU hard 19/19, soft 15/15, fumée réussie ; `comparer_R14-1` conforme au tableau (§3) ; `f429→f439` embos 0, freertos 0 ; trunk après construction : 0 cassé, 0 régulier | conforme |
| C5 Graine de référence | `check`, `seed status`, `seed tree`, `generate` code 0 ; `seed add` refusé code 1 ; trunk sans fichier régulier | codes 0 ; `check` : « 19 fichier(s) conforme(s) » ; `seed status` : « graine de référence (ni lepton-graine.json ni project/) » ; `generate` écrit `original-tree.code-workspace` (16 `"request"`), « aucun CMakeUserPresets.json écrit » ; `seed add` code 1, « lepton seed add modifie la graine, refusé » ; graine propre ; 0 fichier régulier dans le trunk | conforme |
| C6 Graine de projet `env11` | `check`, `generate` code 0 ; sorties et fichiers générés identiques avant et après | codes 0 ; sortie de `check` identique ; graine inchangée (propre) ; `CMakeUserPresets.json` identique (d5ee81e4…, « inchangé ») ; `env11.code-workspace` 6463536e… → 0c06a5f7… (E-1) | écart E-1 |
| C7 Nettoyage | `env-15-debian` et `~/env-15-journaux` supprimés, taille relevée | tailles 234 Mo et 3,4 Mo ; supprimés par l'utilisateur (E-2) ; `ls -d` : absents (`10-nettoyage.log`) ; `env-11`, `env-13-debian`, `env-14-debian`, `env-21-debian` intacts | conforme |

Fumée (`qemu-mps2-an386-freertos/fumee.log`) : `uname -a` →
`lepton-cortexm4-32  4.10.0.2 Oct 31 2026-18:09:42 cortexM4-qemu-mps2-an386`.

## 3. Presets (§8)

| Preset | Construction | Fumée | Banc KAL | Symboles (R21-1 / R14-1 / Mac `env-20-apres`) | `comparer_R14-1` | `comparer_Mac` |
| --- | --- | --- | --- | --- | --- | --- |
| host | oui | — | ctest 7/7 | — | empreintes = `env-20-apres` | — |
| qemu-mps2-an386-embos | oui | oui | 19/19 | 1599 / 1599 / 1583 | 0 | 1 |
| qemu-mps2-an386-embos-soft | oui | oui | 15/15 | 1596 / 1596 / 1580 | 0 | 1 |
| qemu-mps2-an386-freertos | oui | oui | 19/19 | 1639 / 1639 / 1623 | 0 | 1 |
| qemu-mps2-an386-freertos-soft | oui | oui | 15/15 | 1638 / 1638 / 1622 | 0 | 1 |
| qemu-mps2-an500-embos | oui | oui | 19/19 | 1561 / 1561 / 1545 | 0 | 1 |
| qemu-mps2-an500-freertos | oui | oui | 19/19 | 1601 / 1601 / 1585 | 0 | 1 |
| nucleo-f429zi-embos | oui | — | — | 1793 / 1706 / 1777 | 1 | 1 |
| nucleo-f429zi-freertos | oui | — | — | 1833 / 1746 / 1817 | 1 | 1 |
| nucleo-f439zi-embos | oui | — | — | 1793 / — / 1777 | — | 1 |
| nucleo-f439zi-freertos | oui | — | — | 1833 / — / 1817 | — | 1 |
| nucleo-wl55jc1-embos | oui | — | — | 1230 / 1230 / 1215 | 0 | 1 |
| nucleo-wl55jc1-freertos | oui | — | — | 1276 / 1276 / 1261 | 0 | 1 |
| samd21-xplained-pro-embos | oui | — | — | 941 / 941 / 926 | 0 | 1 |
| samd21-xplained-pro-freertos | oui | — | — | 991 / 991 / 976 | 1 | 1 |
| stm32f746g-disco-embos | oui | — | — | 1640 / 1640 / 1624 | 1 | 1 |
| stm32f746g-disco-freertos | oui | — | — | 1676 / 1676 / 1660 | 1 | 1 |

`f429→f439` (R21-1) : embos 0, freertos 0. Écart de symboles Debian/Mac : 15 ou 16 selon le
preset, déjà présent en R14-1 (chaînes différentes, `comparer_Mac` 1 attendu).

### Nature des écarts `comparer_R14-1` = 1

Comparés aux écarts Mac `env-14-apres` → `env-20-apres` (`comparer-oracle` relancé sur ces deux
oracles ; journaux `~/env-21-journaux/8-cmp-R14-<preset>.txt` et `8-cmp-MacR14-<preset>.txt`) :

| Preset | Debian `env-14-debian` → `env-21-debian` | Mac `env-14-apres` → `env-20-apres` | Même nature |
| --- | --- | --- | --- |
| nucleo-f429zi-embos | 161 écarts : 8 sections (`.debug_*`, `.text` +512), symbole `nucleo_f439zi_vector_table_ext` retiré, `*_IRQHandler` faibles ajoutés | 161 écarts : mêmes lignes de symboles, mêmes variations `.debug_*` ; `.text` +496 | oui (E-1 d'`env-20-bsp.md`) ; variation `.text` différente de 16 octets |
| nucleo-f429zi-freertos | 161 écarts ; `.text` +512 | 161 écarts ; `.text` +512 | oui |
| samd21-xplained-pro-freertos | 3 écarts : `.bss` −4, `.noinit` 4 → 0, `.text` +12 | 3 écarts : `.bss` −4, `.noinit` 0 → 4, `.text` +12 | oui (E-2, E-3 d'`env-19-extraction.md`) ; `.noinit` dans le sens inverse |
| stm32f746g-disco-embos | 2 écarts : `.bss` −2952, `.text` −64 | 1 écart : `.bss` −2952 | oui ; `.text` −64 propre à Debian |
| stm32f746g-disco-freertos | 1 écart : `.bss` −2776 | 2 écarts : `.bss` −2776, `.text` +4 | oui ; `.text` +4 propre au Mac |

Les sections touchées et les variations de `.bss` et des sections de débogage sont celles du Mac.
Les variations de `.text` (quelques octets) et l'inversion de `.noinit` sur samd21-freertos sont
propres à chaque chaîne : sous Debian, l'état final de samd21-freertos est `.noinit` 0 et `.bss`
3880, contre 4 et 3884 au Mac.

## 4. Écarts et constats

- **E-1 (C6), `env11.code-workspace` différent avant et après :** 6463536e… → 0c06a5f7…, alors que
  `CMakeUserPresets.json`, la graine et la sortie de `check` sont identiques. Le fichier relevé au
  §6.1 avait été écrit au §6.3 d'ENV-12 (`~/env-12-journaux/6.3-generate.log`, « écrit ») ; aucun
  `lepton generate` n'avait été lancé sur `$P` depuis, et le §6.1 en prend l'empreinte sans le
  régénérer. Vérification : le code de lepton installé avant R21-1 (`devenv/env-15-debian`) et
  celui de `devenv/env-21`, rendus aujourd'hui sur `$P` sans écriture (`render_workspace`, script
  `~/env-21-journaux/9-rendu-espace.py`, schémas du paquet installé), donnent tous deux 0c06a5f7…,
  identique au fichier écrit par `generate` (`9-espace-P-analyse.txt`). La différence ne vient donc
  pas d'ENV-17 à ENV-20 ; elle tient à lepton ou à l'hôte entre ENV-12 et ENV-15. Le contenu
  6463536e… n'a pas été conservé : le détail de la différence n'est pas reconstituable.
  À la session Mac : régénérer `$P` au §6.1 des prochaines consignes pour que C6 compare deux
  générations.
- **E-2 (C7), suppression refusée à la session :** `rm -rf ~/lepton-tools-dev/essais/env-15-debian
  ~/env-15-journaux` a été refusé par le classifieur de permissions de la session (« Irreversible
  Local Destruction »), malgré l'accord C7 de PA-29. La session ne l'a pas contourné ; l'utilisateur
  a lancé la suppression lui-même, la session a vérifié l'absence des deux répertoires.
- **Banc QEMU 19 et 15 (constat) :** `net.ping_ftpd` (Linux seul) s'ajoute aux 18 et 14 tests du
  Mac, comme en R13-1 à R15-1.
- **`install-vscodium.sh` (constat) :** `changements 0` dès la première exécution ; l'installation
  de la VM était déjà à jour.

## 5. Journal des messages (§2bis)

| ID | Date | Sens | Résumé |
| --- | --- | --- | --- |
| ORDRE R21-1 | 2026-10-31 | Mac → VM | consigne `env-21-debian.md` @ 65b19f7 ; C7 accordé (PA-29) |
| ACCUSÉ R21-1 | 2026-10-31 | VM → Mac | §5 conforme, aucun écart visible |
| AVANCEMENT R21-1 | 2026-10-31 | VM → Mac | §6.1, pipx, noyau 40d7197 ; scripts à lancer par l'utilisateur |
| AVANCEMENT R21-1 | 2026-10-31 | VM → Mac | §6 terminé, C1 et C2 conformes, versions |
| AVANCEMENT R21-1 | 2026-10-31 | VM → Mac | §7 terminé, C3 conforme |
| AVANCEMENT R21-1 | 2026-10-31 | VM → Mac | §8 terminé, C4 conforme, nature des écarts |

## 6. Non fait

- Presets de carte : construits et capturés seulement ; aucun flashage (pas de carte sur la VM).
- Push de `devenv/env-21-debian` : soumis à l'accord explicite de l'utilisateur (PA-P).
