# ENV-43 — Validation Debian groupée (ENV-37 à ENV-42) — rapport de la session Mac

Session Mac `validation-debian-env-43`, 2026-11-09. Branche lepton-tools `devenv/env-43` (depuis
`main` 13109dc). Consigne VM : `consignes/env-43-debian.md`.

## 1. Préparation (tâche 1)

### 1.1 Écarts Mac `env-35-apres` → `env-42-apres`

`comparer-oracle.py` par preset. `env-35-apres` est la référence de R36-1 au Mac ; `env-42-apres`
est l'oracle de référence (PA-72). ENV-37 et ENV-41 ont rendu le code 0 sur les 16 presets : les
écarts sont ceux d'ENV-42. Les sorties sont identiques, hors empreintes et bilan, à
`oracles/env-42-apres/comparaisons/` (avant d'ENV-42 = `env-41-apres` = `env-35-apres` en
binaires).

| Preset | Code | Écarts hors `.debug_*` | `.text` |
| --- | --- | --- | --- |
| host | — | `mklepton-empreintes.sha256` identique | — |
| `qemu-mps2-an500-{embos,freertos}`, `stm32f746g-disco-{embos,freertos}`, `samd21-xplained-pro-{embos,freertos}` | 0 | aucun | = |
| `qemu-mps2-an386-{embos,embos-soft,freertos,freertos-soft}` | 1 | `qemu_mps2_eth_irq_enable`, `qemu_mps2_uart_irq_enable` modifiés | +16 |
| `nucleo-wl55jc1-{embos,freertos}` | 1 | `NVIC_SetPriority.constprop.0` → `__NVIC_SetPriority.constprop.0`, `HAL_NVIC_{Disable,Enable}IRQ` modifiés | +16 |
| `nucleo-f4{29,39}zi-embos` | 1 | `NVIC_{Disable,Enable}IRQ` → `__NVIC_*`, `nucleo_f439zi_eth_irq_enable`, `uart_{close,get_char,irq_handler,open}` modifiés | +32 |
| `nucleo-f4{29,39}zi-freertos` | 1 | idem | +48 |

Aucune autre section chargée ne change. Les empreintes d'an500 diffèrent sans écart de section ni
de symbole (déjà le cas dans `env-42-apres/comparaisons/`).

Attendus versionnés dans `env-43-mac/attendu/` :
- `comparaisons-mac/<preset>.txt` : sorties brutes du comparateur pour les 10 presets M4 ;
- `<preset>.noms.txt` : les mêmes écarts normalisés, noms seuls, `.debug_*` exclues (3 lignes
  an386, 5 WL55, 10 F4). La VM les compare à `env-36-debian` → `env-43-debian`.

### 1.2 Têtes publiées (`git ls-remote`, 2026-11-09)

| Dépôt | Référence | Commit | En R36-1 |
| --- | --- | --- | --- |
| `lepton-tools` | `main` | 13109dc | bd7ad59 (`devenv/env-36`) |
| `seed.scions` | tag `0.6.1.0` (`master` f29fa35) | 4502a70 | tag `0.5.4.0` 99aa973 |
| `lepton-seed.scions` | `original-tree` | 15740f9 | = |
| `lepton-original-tree.scions` | `master` | 763dda2 | 2893297 |
| `lepton-bsp-qemu-mps2-an386` | `master` | 5819047 | 09f4943 |
| `lepton-famille-stm32f4xx` | `master` | 7afd7f1 | 0fd8b2a |
| `lepton-famille-stm32wlxx` | `master` | 2340b25 | dbc58d7 |
| 9 autres greffons famille/BSP | `master` | inchangés | = |
| `mirror-stm32f4xx-hal-driver` | tag `v1.8.5` | b6f0ed3 (= amont STMicroelectronics) | — |
| `mirror-cmsis_device_f4` | `master` | 9192c7b (épinglé : 3c77349, sans tag) | — |

Clones de `<ROOTSTOCK>` aux mêmes commits, propres, alignés sur `origin` ; clones tiers à b6f0ed3
et 3c77349.

### 1.3 Liens du trunk

On compare l'état de R36-1 à l'état actuel. L'état de R36-1 est la liste de `essais/env-13-vierge`
après sa regreffe d'ENV-36 (`essais/env-36-mac/env-13-vierge-liens-apres.txt`, 3978 liens). Ce
rootstock n'a pas bougé depuis : sa liste actuelle lui est identique.

L'état actuel est celui de `<ROOTSTOCK>` : 3982 liens.

| Relevé | Résultat |
| --- | --- |
| ajouts | 4 : `LEPTON-PROVENANCE.md` de la famille WL (ENV-37) sous `cmsis/Device/st/stm32wlxx/`, `stm32wlxx/Utilities/`, `stm32wlxx/cubemx_hal_driver/`, `stm32wlxx/radio_subghz_phy/` |
| retraits | 0 (ENV-41 laisse les chemins inchangés, PA-69) |
| liste `./chemin -> cible` de `<ROOTSTOCK>` | 3982, SHA-256 `d9f4ea56…` = `env-41-f4-projection/rootstock/trunk-liens.txt` (ENV-42 n'a pas regreffé) |
| cibles sous `depots/tiers/` | 206 = `env-41-f4-projection/rootstock/chemins-projetes.txt` |

Attendus :
- `attendu/liens-ajoutes.txt` (4, chemins `trunk/…`) et `attendu/liens-retires.txt` (vide) ;
- `attendu/trunk-liens.txt` : liste `./chemin -> cible` triée par octets ; les cibles relatives ne
  dépendent pas de l'hôte ;
- `attendu/projetes.txt` (206).

### 1.4 Contrôle du trunk et du contenu projeté

`env-43-mac/controler-trunk.py` (nouveau, lecture seule) reprend en un script les contrôles faits
à la main en ENV-41 §3.3-3.5 :
- liste `chemin -> cible` contre l'attendu, casse comprise ;
- fichiers réguliers, liens cassés ;
- pour chaque lien vers `depots/tiers/` : nom présent au `ls-tree -r HEAD` du clone, et
  `git hash-object --no-filters` égal au blob du HEAD ;
- état des clones tiers.

Essais au Mac :

| Rootstock | Résultat |
| --- | --- |
| `<ROOTSTOCK>` | code 0, `CONFORME` : 3982 = attendu, 0 régulier, 0 cassé, 206 projetés, 0 écart de nom, 0 de contenu ; clones tiers b6f0ed3 / 3c77349, `origin` = miroirs, 0 modification, `blob:none` |
| `essais/env-41-vierge` | code 1, chemins identiques, 129 cibles différentes (famille en version `devenv/env-41`) : le script détecte un écart de cible |

### 1.5 Commande de miroir

Essai à blanc au Mac, `scion mirror-sync --dry-run -v` dans `essais/env-41-vierge` (le rootstock
porte la famille avec `.scion.mirrors`). Résultat : code 0 ; `mirror-stm32f4xx-hal-driver` et
`mirror-cmsis_device_f4` ont 0 référence à envoyer et 0 signalement ; branches et tags
identiques à l'amont. La commande a créé les dépôts de travail sous
`essais/env-41-vierge/depots/.mirrors/` ; rien n'a été envoyé.

Dans `essais/env-40-publication/rootstock` (`--bare`, non greffé), la commande rend « aucun
miroir déclaré ». Ce lieu n'est donc pas utilisable pour cet essai.

### 1.6 Consigne

`consignes/env-43-debian.md` :

| Critère | Contenu |
| --- | --- |
| C1 | Versions ; installation par l'utilisateur de scion 0.6.1.0 (`install-debian.sh` du noyau 763dda2), de lepton (`pipx`) et de l'extension 0.5.2 (`install-vscodium.sh` ×2), avant toute regreffe |
| C2 | `graft-update` de `essais/env-28-debian` par l'utilisateur, puis rootstock neuf `essais/env-43-debian` ; `controler-trunk.py` contre l'attendu |
| C3 | Host et 16 presets, comparaison à `env-36-debian` : 6 presets à 0, 10 presets M4 aux écarts du Mac |
| C4 | Contenu projeté (§7) et compilation à blanc, résumé = R36-1 |
| C5 | Rootstock neuf contre `env-36-debian` ; `$U` regreffé ; `$P` (stabilité) |
| C6 | `mirror-sync --dry-run` dans le rootstock neuf (proposition) |
| C7 | Cartes (à trancher) |
| C8 | Nettoyage (proposition : `essais/env-36-debian`, `~/env-36-journaux`) |

Le nom `essais/env-43-debian` est imposé. Les chaînes `__FILE__` des presets FreeRTOS suivent le
chemin du rootstock (piège d'ENV-42) ; `env-36-debian` a la même longueur.

Points laissés au PA-73 : C6, C7, C8. Il faut aussi décider d'un essai préalable de
`graft-update` au Mac.

## 2. PA-73 (2026-11-09, décisions de l'utilisateur)

- C7 : NUCLEO-F429ZI seule sur la VM, une seule sonde ST ; écriture flash accordée (PA-11) pour
  les 3 images `nucleo-f429zi-embos`, `nucleo-f429zi-freertos`, `nucleo-f439zi-embos` construites
  sur la VM. §12 de la consigne écrit en clair (forme de R36-1 §10). La synthèse de `board_net`
  est lue dans `carte-detail.log`.
- C6 : `scion mirror-sync --dry-run -v` dans `essais/env-43-debian`.
- C8 : `rm -rf essais/env-36-debian ~/env-36-journaux` par l'utilisateur, après le §10.1.
- Avant l'ordre : `graft-update` d'`essais/env-13-vierge` au Mac (PA-P), puis push de
  `devenv/env-43` et ordre `R43-1` à `debian-linux-vm`.

## 3. Messages §2bis

| Message | Date | Sens | Résumé |
| --- | --- | --- | --- |

## 4. Vérification du rapport VM (tâche 4)

À faire après `FIN-* R43-1`.

## 5. Rootstocks d'essai du Mac (tâche 3)

Accord de l'utilisateur (PA-73, PA-P) pour `essais/env-13-vierge`, le 2026-11-09, avant l'ordre
R43-1. Les 6 autres suivent la VM. scion 0.6.1.0, lepton 0.1.0 (pipx, `devenv/env-41`).
Journaux : `~/lepton-tools-dev/essais/env-43-mac/` (`<rootstock>-{clones-avant,clones-apres,
generate-avant,graft-update,check,generate}.log|txt`, `-liens-{avant,apres}.txt`,
`-espace-avant.code-workspace`, `-espace.diff`, `-controle/`).

Inventaire avant d'`env-13-vierge` : 13 clones sur `master`, amont `origin/master`, propres, aux
têtes de R36-1 ; graine 15740f9, propre ; 14 entrées ; 3978 liens, 0 cassé, 0 fichier régulier.
Espace régénéré par `lepton generate` (code 0) juste avant le relevé.

| Rootstock | `graft-update` | Liens avant → après | Ajouts / retraits | Entrées | `controler-trunk.py` | `check` | `generate` | Espace |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `env-13-vierge` | 0 ; noyau 2893297 → 763dda2, an386 09f4943 → 5819047, F4 0fd8b2a → 7afd7f1, WL dbc58d7 → 2340b25 ; 2 clones tiers `--filter=blob:none` depuis les miroirs ; projections 102 + 96 + 1 + 1 et 1 + 1 fichiers | 3978 → 3982 | 4 / 0 = attendu | 16 | `CONFORME` (= attendu, 206 projetés, 0 écart de nom ni de contenu, tiers b6f0ed3 / 3c77349, `blob:none`) | 0 | 0 | identique (`diff` vide) |

`seed status` : 2 clés « projection » (200 et 6 fichiers), trunk sans fichier régulier ni lien
cassé. Le passage d'une famille copiée à une famille porteuse par `graft-update` (jamais fait
auparavant : ENV-41 avait fait `seed-clone` + `graft`) est donc conforme. L'attendu de C2 est
confirmé sur un rootstock dans l'état de `$U`.
