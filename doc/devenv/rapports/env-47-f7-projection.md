# ENV-47 — Famille STM32F7 : copie remplacée par la projection

Session du 2026-11-10. Archétype : migration iso-fonctionnelle (binaires identiques). Modèle :
`rapports/env-41-f4-projection.md`. Relevés : `env-47-f7-projection/`.

## 1. Audit (lecture seule) — état au PA-81

### 1.0 Point de départ
- lepton-tools `main` 3d6304c ; `family-stm32f7xx` `master` d2d9aa9 ; F4 acdd24c ; clone noyau
  76f28bd ; graine `original-tree` 15740f9 (F7 déclarée en `master`,
  `https://github.com/lepton-distribution/lepton-famille-stm32f7xx.git`) ; BSP F746 6266908 ;
  tous propres, = distant.
- scion 0.6.2.0, lepton 0.1.0 ; `pushInsteadOf` global `ssh://git@github.com/` ← `https://github.com/`
  présent (PA-68).
- Sondes visibles : NUCLEO-F429ZI, WL55 A et B. STM32F746G-DISCO **non visible**.

### 1.1 Copie actuelle contre l'amont
| Contrôle | Résultat |
| --- | --- |
| `verifier-import.sh tiers/stm32f7xx-hal-driver v1.3.3 …/hal_driver` | code 0 ; 196 OK, 0 écart (e1446fa) — `audit/verifier-hal.txt` |
| `verifier-import.sh tiers/cmsis_device_f7 v1.2.10 …/STM32F7xx env-34-hal-f4/listes/cmsis-device-f7.txt` | code 0 ; 5 OK (2352e88) — `audit/verifier-cmsis-device.txt` |
| Motifs proposés (§1.3) appliqués à l'amont (`ls-tree` du tag) | 196 + 5 = `env-38-projection/attendus/f7-*.txt` (`cmp`) |
| Noms suivis par git dans la famille, hors `LEPTON-PROVENANCE.md` | 201 = attendus, casse comprise (`audit/famille-suivis.txt`) |
| Restent dans la famille hors projection | 2 `LEPTON-PROVENANCE.md` |

Amonts (2026-11-10, `git ls-remote`) : HAL 8 tags annotés, dernier `v1.3.3` (e1446fa), `master`
e860c4f (`v1.3.3-19`) ; CMSIS device 7 tags annotés, dernier `v1.2.10` = `master` 2352e88. Les
miroirs `lepton-distribution/mirror-stm32f7xx-hal-driver` et `mirror-cmsis_device_f7` n'existent
pas (`gh repo view`). Le clone amont local de la HAL est à HEAD e860c4f, pas au tag : les
comparaisons se font contre le tag.

### 1.2 Trunk de `<ROOTSTOCK>`
`env-43-mac/controler-trunk.py` (lecture seule) : 3887 liens, 0 fichier régulier, 0 lien cassé ;
206 projetés (F4), contenu = HEAD, 0 écart de casse ; liste `chemin -> cible`
`audit/rootstock/liens.txt` (SHA-256 `6cd0c0d4…`, chemins seuls `c65ee399…`). 203 liens visent la
copie F7 (201 fichiers tiers + 2 provenances).

Attendu après bascule : 3887 chemins **identiques** ; 201 cibles changées, de
`depots/lepton/family-stm32f7xx/master/scion/…` vers `depots/tiers/stm32f7xx-hal-driver/v1.3.3/…`
et `depots/tiers/cmsis-device-f7/v1.2.10/…` ; 407 projetés en tout ; les 2 provenances restent
liées à la famille.

### 1.3 `scion/.scion/` proposé pour `family-stm32f7xx`
Même forme que le porteur F4 (ENV-41 §1.1). Les versions sont des tags, qui existent ici, à la
différence du CMSIS device F4.

```
# .scion.sources.list
tiers	stm32f7xx-hal-driver	v1.3.3	https://github.com/lepton-distribution/mirror-stm32f7xx-hal-driver.git
tiers	cmsis-device-f7	v1.2.10	https://github.com/lepton-distribution/mirror-cmsis_device_f7.git

# .scion.ramifications
tiers	stm32f7xx-hal-driver	v1.3.3
tiers	cmsis-device-f7	v1.2.10

# .scion.projections  (écrits en entier dans le fichier)
tiers  stm32f7xx-hal-driver  Inc/**                      scion/sys/root/src/kernel/dev/arch/cortexm/stm32f7xx/hal_driver/Inc/
tiers  stm32f7xx-hal-driver  Src/**                      scion/sys/root/src/kernel/dev/arch/cortexm/stm32f7xx/hal_driver/Src/
tiers  stm32f7xx-hal-driver  LICENSE.md                  scion/sys/root/src/kernel/dev/arch/cortexm/stm32f7xx/hal_driver/
tiers  stm32f7xx-hal-driver  README.md                   scion/sys/root/src/kernel/dev/arch/cortexm/stm32f7xx/hal_driver/
tiers  cmsis-device-f7       Include/stm32f7xx.h         scion/sys/root/src/kernel/core/ucore/cmsis-5/Device/ST/STM32F7xx/Include/
tiers  cmsis-device-f7       Include/system_stm32f7xx.h  scion/sys/root/src/kernel/core/ucore/cmsis-5/Device/ST/STM32F7xx/Include/
tiers  cmsis-device-f7       Include/stm32f746xx.h       scion/sys/root/src/kernel/core/ucore/cmsis-5/Device/ST/STM32F7xx/Include/
tiers  cmsis-device-f7       LICENSE.md                  scion/sys/root/src/kernel/core/ucore/cmsis-5/Device/ST/STM32F7xx/
tiers  cmsis-device-f7       README.md                   scion/sys/root/src/kernel/core/ucore/cmsis-5/Device/ST/STM32F7xx/

# .scion.mirrors
https://github.com/lepton-distribution/mirror-stm32f7xx-hal-driver.git	https://github.com/STMicroelectronics/stm32f7xx-hal-driver.git
https://github.com/lepton-distribution/mirror-cmsis_device_f7.git	https://github.com/STMicroelectronics/cmsis_device_f7.git
```

Clés `cmsis-device-f7` (trait d'union, comme `cmsis-device-f4` et le §2.2 d'ENV-38), miroir au nom
de l'amont (`cmsis_device_f7`, comme le F4). Clones attendus : `depots/tiers/stm32f7xx-hal-driver/v1.3.3`,
`depots/tiers/cmsis-device-f7/v1.2.10`.

### 1.4 Rootstocks et graines qui greffent `family-stm32f7xx`
Tous en version `master` (d2d9aa9). Rien ne change pour eux tant que la famille publiée n'avance
pas. Leur regreffe relève d'ENV-50.

| Hôte | Rootstock | Graine | scion | Remarque |
| --- | --- | --- | --- | --- |
| Mac | `<ROOTSTOCK>` | `original-tree` | 0.6.2.0 | basculé ici (PA-P) |
| Mac | `essais/env-13-vierge` | `original-tree` | 0.6.2.0 | un des 7 regreffés en ENV-43 (`graft-update`) → ENV-50 |
| Mac | `essais/env-41-vierge` | `env-41-vierge-graine` (locale) | 0.6.2.0 | rootstock neuf d'ENV-41 gardé |
| Mac | `essais/env-34-copie`, `env-35-copie`, `env-37-copie`, `env-39-copie` | `original-tree` | 0.6.2.0 | copies d'étape, jamais regreffées (hors des 7 d'ENV-43) |
| VM | `essais/env-28-debian`, `essais/env-43-debian` | `original-tree` | 0.6.1.0 | ENV-50 installe 0.6.2.0 avant toute regreffe |

Les 6 autres rootstocks d'essai du Mac (`env-9`, `env-11/*`) ne greffent pas le F7. Aucune graine
de projet ne greffe le F7 aujourd'hui.

### 1.5 Rootstock à graine de projet (tâche 3)
`seed lock` refuse toute graine sans `graine.json` ni `project/` (`refuse_reference`,
`lepton/seed.py:565`). Cela vaut pour `<ROOTSTOCK>` comme pour un rootstock neuf tiré d'une copie
d'`original-tree`. Aucun rootstock existant n'a de graine de projet qui greffe le F7.

Proposition : après la bascule de la copie d'essai (tâche 5.1) et la publication des miroirs
(tâche 2), créer `essais/env-47-projet` par la commande suivante :

```
lepton seed new f746 -C essais/env-47-projet --bsp stm32f746g-disco \
  --mkconf sys/user/tauon-basic/etc/mkconf_tauon_basic_stm32f746g_disco.xml \
  --origin family-stm32f7xx=file://<copie>/depots/lepton/family-stm32f7xx/master@devenv/env-47 \
  --origin bsp-stm32f746g-disco=https://github.com/lepton-distribution/lepton-bsp-stm32f746g-disco.git@master
```

Le noyau vient de l'origine par défaut. Les clones tiers sont créés depuis les miroirs. Ce
rootstock sert à `seed lock` et `seed lock --verify` (clés F7 figées) ; il est supprimé au PA-82.

### 1.6 lepton, extension, hook, skill, scripts
- lepton, extension, hook : aucune mention propre au F4 ou au F7. Les clés projetées sont traitées
  de façon générique depuis ENV-41 (`rootstock.py`, `files.py`, `seed.py`, `generate.py`,
  `srcmap.ts`). Aucune modification n'est nécessaire.
- La skill `lepton-rootstock` cite `family-stm32f4xx` comme exemple de porteur : c'est exact, et
  rien n'est à changer.
- L'aide de `scripts/tiers/verifier-import.sh` (l. 15-17) dit : « Sert aux copies … (familles
  STM32F7 et STM32WL) ». Après la bascule, ce n'est plus vrai pour le F7.
- Le BSP F746 (`stm32f7xx_hal_conf.h`, `stm32f746g_disco.h`) cite le modèle de la HAL et
  STM32CubeF7 v1.17.4. Ces références restent vraies : les modèles sont projetés (`Inc/**`).
- Manifeste de la famille : `description` cite la HAL « STM32CubeF7 1.17.4 (hal_driver) » sans
  dire qu'elle est projetée. `sources` (4 fichiers `hal_driver/Src/…`) et `compilation` restent
  inchangés, car ils sont résolus par le trunk depuis ENV-41.

### 1.7 Propositions soumises au PA-81
1. Lignes du §1.3 : clés, tags `v1.3.3` et `v1.2.10`, motifs, URL des miroirs.
2. Miroirs `lepton-distribution/mirror-stm32f7xx-hal-driver` et
   `lepton-distribution/mirror-cmsis_device_f7`, forme du PA-68 :
   - publics ;
   - description GitHub seule, « Miroir de conservation de <amont> (avance rapide seulement, scion
     mirror-sync) », aucun commit ajouté ;
   - créés par la session (`gh repo create --public`, sans README ni licence) ;
   - première synchronisation par la graine de publication d'ENV-40 (E13) : 2 lignes ajoutées à
     son `.scion.mirrors`, puis `mirror-sync --seed`, et seulement ensuite le porteur (PA-P).
3. `LEPTON-PROVENANCE.md` ×2 conservés dans la famille et réécrits, forme du PA-69 (projection,
   clé, révision, miroir, scion ≥ 0.6.1.0). `LICENSE.md` et `README.md` projetés depuis l'amont.
   Liste des chemins du trunk strictement inchangée.
4. `description` du manifeste réécrite, forme du F4 ; `sources` et `compilation` inchangés.
5. lepton, extension, hook, skill : aucune modification. lepton-tools : l'aide de
   `verifier-import.sh` est corrigée (F7 projeté depuis ENV-47, WL seul en copie jusqu'à ENV-48),
   dans un commit dédié.
6. Rootstock à graine de projet du §1.5.
7. Regreffe comme en ENV-41 §3.5 : sur la copie d'essai d'abord, puis sur un rootstock neuf (graine
   d'essai locale, famille en `file://` de `devenv/env-47`), puis sur `<ROOTSTOCK>` (PA-P), par
   `seed-clone --seed …/original-tree` et `graft`, sans `graft-update` ni `seed-update`.
8. Banc STM32F746G-DISCO : uniquement si la carte est branchée (PA-11).

### 1.8 Décisions du PA-81 (utilisateur, 2026-11-10)
- Propositions 1 à 7 acceptées telles quelles. Cela comprend l'accord PA-P pour `gh repo create`
  des deux miroirs et leur synchronisation (push).
- Proposition 8 : la STM32F746G-DISCO sera branchée par l'utilisateur ; écriture flash accordée
  (PA-11) pour le banc du §6.
