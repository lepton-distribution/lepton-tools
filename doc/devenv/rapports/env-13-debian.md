# ENV-13 — Reconstruction Debian depuis la graine publiée `original-tree` — 2026-10-30

Session VM Debian (`lepton-portage-debian`) conduite selon la consigne `env-13-debian.md` (ordre
`R13-1` de la session Mac `publish-seed-reference-tree`, texte reçu dans l'ordre ; consigne non
présente dans `main`, commit Mac 2b92666 non poussé). La session exécute, constate et rapporte ;
aucune correction. Journaux : `~/env-13-journaux/` sur la VM (hors git) ; rootstock conservé :
`~/lepton-tools-dev/essais/env-13-debian`.

Bilan : C1 à C6 conformes. Écart informatif : le banc QEMU compte un test de plus qu'au Mac
(`net.ping_ftpd`, label `net` créé sous Debian seulement, §4).

## 1. Hôte et versions (§5)

| Élément | Valeur |
| --- | --- |
| Système | Linux x86_64, Debian 13.7, noyau 6.12.107+deb13-amd64, utilisateur `lepton-user` |
| scion / lepton | 0.5.1.1 / 0.1.0 (`scion 0.5.1.1 (requis ≥ 0.5.1.1)`) |
| arm-none-eabi-gcc | 14.2.1 20241119 (paquet Debian `15:14.2.rel1-1`) ; binutils 2.44 |
| cmake / ninja | 3.31.6 / 1.12.1 |
| QEMU | 10.0.13 (Debian 1:10.0.13+ds-0+deb13u1) |
| Python | 3.13.5 |
| embOS | présent : `LEPTON_EMBOS_ROOT=~/lepton/third_party/embos/cortexm-gcc/5.20.0.0` |
| Espace | `/home` 26 Go (19 Go libres) ; `/tmp` 747 Mo (647 Mo libres) |
| lepton-tools | `main` = `origin/main` d0c54d1 après `fetch` / `pull --ff-only` (copie locale auparavant sur `devenv/env-12-debian`, propre) |

## 2. Critères (§9)

| Critère | Attendu | Constaté | Verdict |
| --- | --- | --- | --- |
| C1 Graine et greffons publiés | `ls-remote` conforme au §1 | `lepton-seed.scions` `original-tree` 0f1275a (`master` f41a23f) ; `lepton-original-tree.scions` 16a331b ; `famille-qemu-mps2` 3954357 ; `bsp-qemu-mps2-an386` 046779e ; `bsp-qemu-mps2-an500` e98a482 ; `famille-stm32f4xx` 01b5528 ; `bsp-nucleo-f429zi` 8ea7ee5 ; `famille-stm32wlxx` 1eccc2f ; `bsp-nucleo-wl55jc1` a329f4d | conforme |
| C2 Greffe depuis GitHub | 9 entrées, 4011 liens, 0 cassé, 0 régulier, 9 clones aux commits du §1 | `rootstock-install`, `seed-add`, `graft` : code 0 ; « 4011 feuilles liées » ; 9 entrées ; liens 4011, cassés 0, réguliers 0 ; 9 clones sur leur branche aux commits de C1, origins `github.com/lepton-distribution` | conforme |
| C3 host | construction, ctest 7/7, empreintes | ctest 7/7 ; `mklepton-empreintes.sha256` (44 fichiers) **identique** à celui du Mac (`diff -q` code 0) | conforme |
| C4 14 presets | construits | 14/14 construits (`lepton.elf`, `.bin`, `.hex`), embOS compris ; `rejouer-oracle: tout a réussi`, code 0 | conforme |
| C5 QEMU | banc KAL et fumée sur chaque preset QEMU | 6/6 : hard 19/19, soft 15/15 (banc KAL 18/18 et 14/14 + `net.ping_ftpd`) ; fumée `smoke.lsh` réussie | conforme |
| C6 Trunk après construction | 0 régulier, 0 cassé | 0 régulier, 0 cassé | conforme |

Fumée (`qemu-mps2-an386-freertos/fumee.log`) : `uname -a` →
`lepton-cortexm4-32  4.10.0.2 Oct 30 2026-19:17:19 cortexM4-qemu-mps2-an386`.

## 3. Presets (§7, §8)

Comparaison : `comparer-oracle.py env-13-apres/<preset> env-13-debian/<preset>` ; code 1 partout
(différences d'empreintes, de sections et de symboles), attendu entre Arm GNU Toolchain 14.2.Rel1
(Mac) et le paquet Debian 14.2.1 ; consigné sans interprétation.

| Preset | Construction | Fumée | Banc (Debian / Mac) | Symboles (Debian / Mac) | Comparaison |
| --- | --- | --- | --- | --- | --- |
| host | oui | — | ctest 7/7 / 7/7 | — | empreintes mklepton identiques |
| qemu-mps2-an386-embos | oui | oui | 19/19 / 18/18 | 1599 / 1583 | 1 |
| qemu-mps2-an386-embos-soft | oui | oui | 15/15 / 14/14 | 1596 / 1580 | 1 |
| qemu-mps2-an386-freertos | oui | oui | 19/19 / 18/18 | 1639 / 1623 | 1 |
| qemu-mps2-an386-freertos-soft | oui | oui | 15/15 / 14/14 | 1638 / 1622 | 1 |
| qemu-mps2-an500-embos | oui | oui | 19/19 / 18/18 | 1561 / 1545 | 1 |
| qemu-mps2-an500-freertos | oui | oui | 19/19 / 18/18 | 1601 / 1585 | 1 |
| nucleo-f429zi-embos | oui | — | — | 1706 / 1690 | 1 |
| nucleo-f429zi-freertos | oui | — | — | 1746 / 1730 | 1 |
| nucleo-wl55jc1-embos | oui | — | — | 1230 / 1215 | 1 |
| nucleo-wl55jc1-freertos | oui | — | — | 1276 / 1261 | 1 |
| samd21-xplained-pro-embos | oui | — | — | 941 / 926 | 1 |
| samd21-xplained-pro-freertos | oui | — | — | 991 / 976 | 1 |
| stm32f746g-disco-embos | oui | — | — | 1640 / 1624 | 1 |
| stm32f746g-disco-freertos | oui | — | — | 1676 / 1660 | 1 |

Presets de carte : construits, jamais flashés (pas de carte sur la VM).

## 4. Écarts

- **Banc QEMU : un test de plus qu'au Mac.** `net.ping_ftpd` (label `net`) est créé et réussi sur
  les 6 presets QEMU sous Debian ; il ne l'est pas sous macOS (`env-13-apres` : 18 et 14 tests).
  Les 18 (hard) et 14 (soft) autres tests sont les mêmes et tous réussis. Conforme à l'étape 9
  (« label `net` non créé sur macOS »).
- **Symboles :** environ 15 à 16 symboles de plus sous Debian sur chaque preset, sans analyse
  (§8 : informatif).
- **Consigne :** `doc/devenv/consignes/env-13-debian.md` absente de `main` ; texte de l'ordre
  `R13-1` utilisé tel quel.
- QEMU 10.0.13 sur la VM (11.1.2 au Mac) : sans effet constaté.

## 5. Non fait

- Aucun flashage (pas de carte).
- Aucune analyse des différences de symboles ou de sections au-delà des codes de retour.
- Push de `devenv/env-13-debian` : soumis à l'accord explicite de l'utilisateur (PA-P).
