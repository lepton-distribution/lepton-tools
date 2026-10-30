# ENV-14 — Validation Debian du nettoyage de l'arbre — 2026-10-30

Session VM Debian (`lepton-vm-debian`) conduite selon la consigne `env-14-debian.md` (lepton-tools
`devenv/env-14` 42d3906, ordre `R14-1` de la session Mac `nettoyage-arbre-env-14`). La session
exécute, constate et rapporte ; aucune correction. Journaux : `~/env-14-journaux/` sur la VM (hors
git) ; rootstock conservé : `~/lepton-tools-dev/essais/env-14-debian`.

Bilan : C1 à C7 conformes. Le nettoyage d'ENV-14 ne change rien aux constructions Debian :
`comparer-oracle` code 0 contre `env-13-debian` sur les 14 presets, empreintes mklepton identiques.

## 1. Hôte et versions (§5)

| Élément | Valeur |
| --- | --- |
| Système | Linux x86_64, Debian 13.7, noyau 6.12.107+deb13-amd64, utilisateur `lepton-user` |
| scion / lepton | 0.5.1.1 / 0.1.0 (`scion 0.5.1.1 (requis ≥ 0.5.1.1)`) |
| arm-none-eabi-gcc | 14.2.1 20241119 (paquet Debian `15:14.2.rel1-1`) |
| cmake / ninja | 3.31.6 / 1.12.1 |
| QEMU | 10.0.13 (Debian 1:10.0.13+ds-0+deb13u1) |
| Python | 3.13.5 |
| embOS | présent : `LEPTON_EMBOS_ROOT=~/lepton/third_party/embos/cortexm-gcc/5.20.0.0` |
| Espace | `/home` 26 Go (19 Go libres) ; `/tmp` 747 Mo (647 Mo libres) |
| lepton-tools | propre (sur `main`) ; après `fetch`, `devenv/env-14` = 42d3906 « devenv(env-14): PA-16 (1) consigné » |

## 2. Critères (§9)

| Critère | Attendu | Constaté | Verdict |
| --- | --- | --- | --- |
| C1 Dépôts publiés | `ls-remote` conforme au §1 | graine `original-tree` 0f1275a ; noyau `master` 16a331b, `devenv/env-14` e5a5689 ; `famille-stm32f4xx` `master` 01b5528, `devenv/env-14` af964c6 ; `famille-qemu-mps2` 3954357 ; `bsp-qemu-mps2-an386` 046779e ; `bsp-qemu-mps2-an500` e98a482 ; `bsp-nucleo-f429zi` 8ea7ee5 ; `famille-stm32wlxx` 1eccc2f ; `bsp-nucleo-wl55jc1` a329f4d | conforme |
| C2 Greffe et bascule | initial 9 entrées, 4011 liens ; bascule sans `--force` 3929 liens ; 0 cassé, 0 régulier, 0 `.DS_Store`, aucun chemin retiré | initial : « 4011 feuilles liées », 9 entrées, 0 cassé, 0 régulier ; clones basculés à e5a5689 et af964c6 ; `scion graft --scion lepton@original::tree --scion lepton@family-stm32f4xx` code 0 (« greffe partielle : 3646 feuilles liées ») ; 3929 liens, 0 cassé, 0 régulier, 0 `.DS_Store` ; aucun des 7 chemins retirés présent | conforme |
| C3 host | construction, ctest 7/7, empreintes identiques à R13-1 | ctest 7/7 ; `mklepton-empreintes.sha256` (44 lignes) identique à `env-13-debian` et à `env-14-apres` (`diff -q` code 0) | conforme |
| C4 14 presets | construits | 14/14 (`lepton.elf`), embOS compris ; `rejouer-oracle: tout a réussi`, code 0 | conforme |
| C5 QEMU | banc KAL et fumée sur chaque preset QEMU | 6/6 : hard 19/19, soft 15/15 (banc KAL 18/18 et 14/14 + `net.ping_ftpd`, comme R13-1) ; `smoke.lsh` réussi | conforme |
| C6 Non-régression Debian | `comparer-oracle` code 0 contre `env-13-debian` | code 0 sur les 14 presets | conforme |
| C7 Trunk après construction | 0 régulier, 0 cassé | 0 régulier, 0 cassé | conforme |

Fumée (`qemu-mps2-an386-freertos/fumee.log`) : `uname -a` →
`lepton-cortexm4-32  4.10.0.2 Oct 30 2026-20:18:03 cortexM4-qemu-mps2-an386`.

## 3. Presets (§7, §8)

Comparaisons : `comparer-oracle.py env-13-debian/<preset> env-14-debian/<preset>` (non-régression)
et `comparer-oracle.py env-14-apres/<preset> env-14-debian/<preset>` (Mac, informative : chaînes
différentes ; codes consignés sans interprétation).

| Preset | Construction | Fumée | Banc (Debian / Mac) | Symboles (Debian / Mac) | R13-1 | Mac |
| --- | --- | --- | --- | --- | --- | --- |
| host | oui | — | ctest 7/7 / 7/7 | — | empreintes identiques | empreintes identiques |
| qemu-mps2-an386-embos | oui | oui | 19/19 / 18/18 | 1599 / 1583 | 0 | 1 |
| qemu-mps2-an386-embos-soft | oui | oui | 15/15 / 14/14 | 1596 / 1580 | 0 | 1 |
| qemu-mps2-an386-freertos | oui | oui | 19/19 / 18/18 | 1639 / 1623 | 0 | 1 |
| qemu-mps2-an386-freertos-soft | oui | oui | 15/15 / 14/14 | 1638 / 1622 | 0 | 1 |
| qemu-mps2-an500-embos | oui | oui | 19/19 / 18/18 | 1561 / 1545 | 0 | 1 |
| qemu-mps2-an500-freertos | oui | oui | 19/19 / 18/18 | 1601 / 1585 | 0 | 1 |
| nucleo-f429zi-embos | oui | — | — | 1706 / 1690 | 0 | 1 |
| nucleo-f429zi-freertos | oui | — | — | 1746 / 1730 | 0 | 1 |
| nucleo-wl55jc1-embos | oui | — | — | 1230 / 1215 | 0 | 1 |
| nucleo-wl55jc1-freertos | oui | — | — | 1276 / 1261 | 0 | 1 |
| samd21-xplained-pro-embos | oui | — | — | 941 / 926 | 0 | 1 |
| samd21-xplained-pro-freertos | oui | — | — | 991 / 976 | 0 | 1 |
| stm32f746g-disco-embos | oui | — | — | 1640 / 1624 | 0 | 1 |
| stm32f746g-disco-freertos | oui | — | — | 1676 / 1660 | 0 | 1 |

Les nombres de symboles Debian sont identiques à ceux de R13-1 sur les 14 presets. Presets de
carte : construits, jamais flashés (pas de carte sur la VM).

## 4. Écarts

- **Banc QEMU : 19 et 15 tests au lieu des 18 et 14 de la consigne.** `net.ping_ftpd` (label
  `net`, créé sous Debian seulement) s'ajoute et réussit sur les 6 presets QEMU, comme en R13-1 ;
  les 18 (hard) et 14 (soft) tests du banc KAL réussissent tous.
- **Journal `6a-greffe-initiale.log` :** la ligne `code=` n'a pas été écrite par le bloc (sortie
  prématurée du shell de la session) ; elle a été ajoutée après coup avec une mention explicite.
  La sortie de scion atteste l'installation et la greffe réussies.
- **Constat :** `trunk/.scion.grafted.list` garde la branche `master` pour les deux greffons
  basculés (branche déclarée par la graine, non celle du clone).

## 5. Non fait

- Aucun flashage (pas de carte).
- Aucune analyse des différences avec le Mac au-delà des codes de retour.
- Push de `devenv/env-14-debian` : soumis à l'accord explicite de l'utilisateur (PA-P).
