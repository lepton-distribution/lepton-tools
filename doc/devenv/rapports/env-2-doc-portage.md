# ENV-2 — Lecture de la documentation du portage IAR → GCC

Relevé du 2026-10-13, lecture seule, clone noyau `master` 6b62af5. Lecture intégrale de
`doc/BUILDING.md`, `CLAUDE.md`, `README.md`, `README-PAQUET.md`, de `doc/migration/*.md` (sauf
`inventaire-projets.md` l. 202-797, détail des `.ewp` supprimés, balayé par mots-clés) et des 37
passations `doc/migration/handoff/etape-*.md`. Abréviations : `MS` = `doc/migration/MIGRATION-STATUS.md`,
`C` = `CLAUDE.md` (racine du clone), `B` = `doc/BUILDING.md`, `AC` = `doc/migration/ajout-coeur.md`,
`H/` = `doc/migration/handoff/`.

## 1. Décisions du portage qui contraignent ce chantier

| Sujet | Décision (source) | Incidence |
| --- | --- | --- |
| Découpage | Bibliothèques statiques par composant ; `bin`, `sbin`, `lib` hors de `kernel/` (2026-09-30, MS:80) | Cohérent avec BLD-1 |
| Cycle de liaison | Cycle core ↔ kal ↔ vfs ↔ fs ↔ dev ↔ libc (15 composants, 376 symboles) traité par `$<LINK_GROUP:RESCAN>`, « pas de fusion » (AC:127-129, `doc/migration/dependances.md:326`, H/etape-1.md:47-48) ; le noyau rappelle la libc par 7 symboles (`dependances.md:371-375`) | ENV-5 : `lib` séparée de `kernel` reste dans le cycle → groupe RESCAN conservé ou dépendance à casser |
| CMake | ≥ 3.24 pour `LINK_GROUP` (`doc/migration/ETAPE-2-build-cmake.md:20`, C:30) ; groupe RESCAN vide sous Apple (MS:177, B:120) | Minimum effectif du chantier = 3.24 |
| Démarrage | Démarrage et RTOSInit propres à Lepton ; « un démarrage par famille, une table de vecteurs par MCU » (MS:96-98, `ETAPE-6-generalisation.md:65`) ; emplacement prescrit `src/kernel/core/arch/<famille>/startup_<isa>.c` (AC:60-61) | Contredit en partie la décision 4 de la spécification (démarrage dans le BSP) |
| Vecteurs | Table prolongée par le BSP F4 (IRQ 64-90, 2026-10-02, MS:119) | Seule la F4 a un `*_vectors.c` |
| Symboles faibles | Remplaçants forts (`*_vectors.c`, `HAL_GetTick`/`HAL_Delay` WL) liés comme objets de l'exécutable, sinon l'archive n'est pas tirée (AC:92-95, `validation-nucleo-f439zi.md:33`, `validation-nucleo-wl55jc1.md:55`) | La bibliothèque OBJECT d'ENV-5 doit couvrir vecteurs **et** remplaçants HAL |
| mklepton | `CPU_TYPE_M16C62` conservé : le retirer décale l'énumération lue dans le XML (2026-10-01, MS:121) | ENV-4 : retrait de `<cpu type>` à coupler au retrait de l'énumération |
| Empreintes mklepton | `tests/host/mklepton_empreintes.sha256` : 38 sorties de référence `-m32`, à ne jamais régénérer (H/etape-8.md:9-11, :44) ; toute sortie qui change d'un octet = point d'arrêt (`doc/migration/ORCHESTRATION.md:82`) | ENV-4 : nouvelle référence à décider explicitement si une sortie change |
| Sorties mklepton | Dans le build, `-o` prime sur `dest_path` (2026-09-30, MS:90) | Déjà conforme à BLD-3 |
| F439 / F429 | NUCLEO-F439ZI reste la carte de base nominale ; **noms `nucleo-f439zi` et presets conservés** ; validation sur F429ZI, puce `STM32F429xx` ; paliers à rejouer sur F439ZI (2026-10-01, MS:110) | Le chantier (carte de validation « NUCLEO-F429ZI ») s'écarte de cette décision : renommer = décision à acter |
| Cartes maintenues | an386, an500, F439 (F429), F746, SAMD21, WL55 ; embOS et FreeRTOS de premier rang (B:10-18, C:26, MS:158) | ENV-5 / ENV-6 ne visent que 3 cartes : sort des 3 autres à trancher |
| Hors périmètre | ARM7, ARM9, M16C, simulations (2026-09-29, MS:68, 77) ; M3 `mps2-an385` (C:17) ; Olimex (MS:134) ; RISC-V reporté | Code gelé supprimé à l'étape 6 (tags locaux `legacy`, `legacy-iar`, jamais poussés, C:38-39) |
| WL55 | ABI soft imposée par la carte ; M0+ jamais démarré (`C2BOOT = 0`) ; flash interne seulement, ni option bytes ni protection (2026-10-08, `validation-macos.md:18`) | Reprendre dans ENV-6 / ENV-11 |
| embOS | Licence SFL : hors git, `LEPTON_EMBOS_ROOT`, jamais téléchargé ni redistribué (`embos-inventaire.md:130-150`) | ENV-10 : le script d'installation ne télécharge pas embOS |
| seed.scions | « Hors périmètre — défauts signalés par issue, jamais corrigés ici » (C:169) | Règle du chantier de migration ; ce chantier a décidé l'inverse (spécification, décision 8) : pas de conflit, mais à garder en tête |

## 2. Dettes et résiduels pertinents

- Configuration de carte répartie en **trois lieux** : `cmake/boards` + `ld/` + BSP ;
  `sys/user/tauon-basic/etc/` (mkconf, `.boot`, `.init`) ; `sys/user/tauon-basic/src/arch/<carte>/`
  (`user_kernel_mkconf.h`) ; plus `debug/` et les tests de carte (C:51-53, H/etape-6-wl55-1.md:32-35).
- Code de carte encore dans le noyau : 12 directives `__tauon_cpu_device__` (`kernelconf.h`,
  `rootfscore.h`) (MS:341, H/etape-4.md:58-59).
- `perimetre.csv` / `audit_iar.py` classent par chemin : tout déplacement (ENV-5, ENV-6) impose
  `perimetre_complement.py` (MS:328-330).
- `__KERNEL_UCORE_EMBOS` défini à la fois par CMake et par les `user_kernel_mkconf.h` (MS:317).
- `kernelconf.h` inclut en dur `kernel/core/arch/cortexm/kernel_mkconf.h` dans des branches GCC
  croisées (MS:318, H/etape-2.md:34-35).
- `mklepton_empreintes.sh:43` relit `cmake/boards/*.cmake` par `sed` (`set(LEPTON_BOARD_MKCONF …)`) :
  fragile si ENV-5/6 change la syntaxe ou l'emplacement des modules de carte.
- Défauts connus de mklepton : débordement d'un octet (`mklepton.c:1242-1265`), `strncat(…,32)`,
  `-r` non analysée, `kernel_stub.h` désynchronisé (`doc/migration/mklepton.md:21-25`) ; commentaire
  dans `<binaries>` = « Parse error » (H/etape-4-kernel-net.md:38) ; défaut rootfs `/usr/bin/net`
  sans `/usr/bin` (MS:272-275).
- BSP `qemu_mps2` commun an386 / an500 (H/etape-6-m7-qemu.md:13-16).
- `.gitignore` hérité VS/IAR ignore `[Dd]ebug/`, `[B]in/`, `*.bin`, `*.a` (C:115) : piège pour les
  répertoires `debug/` et `bin/` des futurs greffons BSP.
- Dockerfile jamais construit ; rejeu Debian de `ci/run.sh` avant fusion de l'étape 10 non attesté.

## 3. Pièges opératoires (complètent `handoff/env-1.md`)

- scion : liens orphelins non retirés par `graft` seul dans un cas observé (H/etape-6.md:42-43) —
  le code 0.5.0.1 fait `ungraft` avant `graft` (`env-2-scion.md` §2.d) ; à revérifier à l'extraction.
- `.DS_Store` (Finder) et `__pycache__` (sans `PYTHONDONTWRITEBYTECODE=1`) dans le trunk bloquent
  `ci/run.sh` et la regreffe. Un `.DS_Store` ignoré existe dans le clone :
  `scion/sys/user/tauon-basic/etc/.DS_Store` (greffé comme lien).
- Sources Latin-1 : l'outil Edit les réécrit en UTF-8 → éditer par script `encoding="latin-1"`
  (H/etape-4-kernel-core.md:42-44) ; `grep -a`, `grep -R`.
- Commit par chemin (`git commit -- <f>`) après un `git rm` scripté (H/etape-6.md:44-46).
- Ordre de liaison : fusion de littéraux → `.bin` reproductibles seulement avec
  `SOURCE_DATE_EPOCH` et après `clean` (H/etape-8.md:59-68) : un changement d'ordre (ENV-5) peut
  déplacer des octets.
- Cartes : `monitor resume` avant `detach` ; un seul client par sonde ; `kal_bench` reste en flash
  après `ctest -L board` ; ports `/dev/cu.*` dépendants du port USB (même nom pour plusieurs cartes) ;
  `caffeinate -i` ; gdb avec Python requis (`arm-none-eabi-gdb` MacPorts `+python313`).

## 4. Documents périmés ou contradictoires (ne pas s'y fier)

| Document | Écart |
| --- | --- |
| `README.md` (racine) | Installation Windows, ARM7/ARM9, FreeRTOS 9.0 |
| `README-PAQUET.md`, `doc/migration/README.md` | État d'amorçage, décisions « à venir » déjà prises |
| `doc/migration/ajout-coeur.md:15-16, 136` | Ne cite que an386 / F439 ; `-m32` (retiré à l'étape 8) |
| `doc/migration/mklepton-ref.md:7-11` | Référence sous `kernel/core/arch/win32/` (supprimé) ; oracle effectif = `mklepton_empreintes.sha256` |
| `doc/migration/mass-compile.md`, `audit-iar.md` | Antérieurs au retrait du code gelé (386/386, `-m32`, `legacy/`) |
| `doc/migration/ETAPE-3-socle-qemu.md:56,60` | `armv7m-gcc.cmake` (réel : `arm-none-eabi.cmake`), `-Og` (réel : `-Os`) |
| Options courtes de mklepton (`-s`, `-o`) | Non documentées (`mklepton.md:47` décrit l'ancienne ligne de commande) |

## 5. Procédures à reprendre par l'outillage

- `doc/migration/ajout-coeur.md:26-113` (ajout de cœur, famille, carte, micro-noyau) : base naturelle
  du manifeste de greffon BSP (ENV-3, ENV-6).
- `doc/BUILDING.md:24-55` (installation, scion `pipx …@0.5.0.1`, `rootstock-install`, `seed-add`,
  `graft`), `:57-90` (presets, ctest, `ci/run.sh`), `:135-275` (flash et tests par carte).
- Contrôles d'intégrité du trunk : `find -xtype l` vide, `find -type f ! -name .scion.grafted.list`
  vide, idempotence de `graft` (`ETAPE-0-arbre-sources.md:81-85`).
