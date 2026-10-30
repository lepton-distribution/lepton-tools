# ENV-15 — Validation Debian de scion 0.5.2.0 — 2026-10-30

Session VM Debian (`lepton-vm-debian`) conduite selon la consigne `env-15-debian.md` (lepton-tools
`devenv/env-15` f5e7be8, ordre `R15-1` de la session Mac `fix-scion-ignored-graft-files`). La
session exécute, constate et rapporte ; aucune correction. Journaux : `~/env-15-journaux/` sur la
VM (hors git) ; rootstock conservé : `~/lepton-tools-dev/essais/env-15-debian`.

Bilan : C1 à C8 conformes. scion 0.5.2.0 ne greffe pas les fichiers ignorés par git (E1) ; le
rootstock neuf et les constructions sont inchangés par rapport à R14-1 (`comparer-oracle` code 0
sur les 6 presets QEMU, empreintes mklepton identiques).

## 1. Hôte et versions (§5)

| Élément | Valeur |
| --- | --- |
| Système | Linux x86_64, Debian 13.7, noyau 6.12.107+deb13-amd64, utilisateur `lepton-user` |
| git | 2.47.3 ; `core.excludesFile` global absent (avant et après l'essai) |
| scion / lepton | avant : 0.5.1.1 / 0.1.0 ; après `pipx install --force` : 0.5.2.0 / 0.1.0 (`scion 0.5.2.0 (requis ≥ 0.5.2.0)`) |
| arm-none-eabi-gcc | 14.2.1 20241119 (paquet Debian `15:14.2.rel1-1`) |
| cmake / ninja | 3.31.6 / 1.12.1 |
| QEMU | 10.0.13 (Debian 1:10.0.13+ds-0+deb13u1) |
| Python | 3.13.5 |
| embOS | présent : `LEPTON_EMBOS_ROOT=~/lepton/third_party/embos/cortexm-gcc/5.20.0.0` |
| Espace | `/home` 26 Go (19 Go libres) ; `/tmp` 747 Mo (647 Mo libres) |
| lepton-tools | propre (sur `devenv/env-14-debian`) ; après `fetch`, `devenv/env-15` = f5e7be8 |

## 2. Critères (§9)

| Critère | Attendu | Constaté | Verdict |
| --- | --- | --- | --- |
| C1 Dépôts et installation | `ls-remote` conforme ; scion 0.5.2.0 accepté | seed.scions tag `0.5.2.0^{}` 472c12e (objet tag d838fb1), `master` 472c12e ; graine 0f1275a ; noyau 118912a ; f4 7694ad5 ; autres greffons inchangés depuis R14-1 ; `5-scion.log` et `5-lepton.log` code 0 ; `scion version: 0.5.2.0` ; `lepton --version` accepte | conforme |
| C2 Tests de scion | OK (126, 1 ignoré) | clone au tag 0.5.2.0 (472c12e) : `Ran 126 tests`, `OK (skipped=1)`, code 0 | conforme |
| C3 Rootstock neuf | `.scion.trunk.tolerated` sans motif ; 9 entrées, 3929 liens, 0 cassé, 0 régulier | commentaires seuls ; « 3929 feuilles liées » ; 9 entrées ; 0 cassé, 0 régulier ; clones aux commits de C1 | conforme |
| C4 E1 | `scion graft` code 0 sans conflit, non greffés, trunk identique ; identique après retrait | `check-ignore` côté BSP cite `~/env-15-journaux/excludes:1` ; `scion graft -v` code 0, « 2 chemin(s) ignoré(s) par git, non greffé(s) », lignes `exclu (ignoré par git)` pour `lepton/original::tree` et `lepton/bsp-qemu-mps2-an386` ; 0 `.DS_Store` dans le trunk ; listes avant, E1 et après identiques (sha256 9e16ec37…) ; clones propres après retrait | conforme |
| C5 host | ctest 7/7, empreintes identiques à R14-1 | ctest 7/7 ; `mklepton-empreintes.sha256` (44 lignes) identique (`diff -q` code 0) | conforme |
| C6 Presets QEMU (6) | construits ; banc KAL et fumée réussis (19/15 sous Debian, AVANCEMENT Mac) | 6/6 construits ; hard 19/19, soft 15/15 ; `smoke.lsh` réussi | conforme |
| C7 Non-régression Debian | `comparer-oracle` code 0 contre `env-14-debian` | code 0 sur les 6 presets | conforme |
| C8 Trunk après construction | 0 régulier, 0 cassé | 0 régulier, 0 cassé | conforme |

Fumée (`qemu-mps2-an386-freertos/fumee.log`) : `uname -a` →
`lepton-cortexm4-32  4.10.0.2 Oct 30 2026-22:52:33 cortexM4-qemu-mps2-an386`.

## 3. Presets (§7, §8)

Périmètre fixé au PA-18 : host et les 6 presets QEMU ; presets de carte non reconstruits.

| Preset | Construction | Fumée | Banc KAL | Symboles (R15-1 / R14-1) | `comparer_R14-1` |
| --- | --- | --- | --- | --- | --- |
| host | oui | — | ctest 7/7 | — | empreintes identiques |
| qemu-mps2-an386-embos | oui | oui | 19/19 | 1599 / 1599 | 0 |
| qemu-mps2-an386-embos-soft | oui | oui | 15/15 | 1596 / 1596 | 0 |
| qemu-mps2-an386-freertos | oui | oui | 19/19 | 1639 / 1639 | 0 |
| qemu-mps2-an386-freertos-soft | oui | oui | 15/15 | 1638 / 1638 | 0 |
| qemu-mps2-an500-embos | oui | oui | 19/19 | 1561 / 1561 | 0 |
| qemu-mps2-an500-freertos | oui | oui | 19/19 | 1601 / 1601 | 0 |

## 4. Constats et écarts

- **Banc QEMU 19 et 15 (constat) :** `net.ping_ftpd` (label `net`, Linux seul) s'ajoute aux 18 et
  14 tests du banc KAL, comme en R13-1 et R14-1 ; valeur attendue sous Debian confirmée par
  l'AVANCEMENT de la session Mac.
- **Permissions de la session VM :** l'installation `pipx` (§5) et l'exécution des tests de scion
  (§6, clone et `unittest`) ont été refusées à la session (code externe). Elles ont été lancées
  par l'utilisateur, aux commandes de la consigne, dans les mêmes journaux ; la session en a relu
  les résultats. Le reste du §6 a été exécuté avant les tests de scion (sans dépendance).
- **Méthode E1 :** la vérification de sécurité de la session a refusé le bloc qui contenait `rm` à
  côté d'un `find -exec sh -c`. Les listes de liens ont été produites par
  `find trunk -type l -printf '%p\t%l\n' | LC_ALL=C sort` (vérifiée identique à la forme
  `readlink` sur la liste initiale), et le retrait des deux `.DS_Store` par un `rm` séparé à
  chemins littéraux.
- **E1, clone du noyau :** `check-ignore` y cite `.gitignore:482` (le `.gitignore` du noyau ignore
  déjà `.DS_Store`) et non la règle d'essai ; dans le clone `bsp-qemu-mps2-an386`, c'est bien la
  règle d'essai qui s'applique.

## 5. Non fait

- Presets de carte : non reconstruits (périmètre PA-18) ; aucun flashage.
- Essai E1 avec scion 0.5.1.1 : non rejoué (consigne).
- Push de `devenv/env-15-debian` : soumis à l'accord explicite de l'utilisateur (PA-P).
