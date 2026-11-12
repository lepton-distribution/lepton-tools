# ENV-51 — lepton : messages de scion relayés (D10)

## 0. État de départ (2026-11-12)
- lepton-tools `devenv/env-51`, depuis `main` c5eca52. seed.scions `master` 7e8a0cc (0.6.2.0),
  clone noyau 76f28bd, F4 acdd24c, F7 12280a5 : non touchés.
- Outils : scion 0.6.2.0, lepton 0.1.0 (pipx), git 2.50.1.
- Rootstocks d'essai :
  - `essais/env-51-essai` : `rsync -a` d'`essais/env-11/f429zi` sans `build/`. 3294 liens, aucun
    fichier régulier, aucun lien cassé, aucune référence à `env-11`, `lepton check` 0.
  - `essais/env-51-new` : créé par `lepton seed new`, pour l'essai de cette commande.
  - `essais/env-51-sources` : clones nus des sources, origines des essais en
    `file://localhost/…`. Ils sont faits depuis `<ROOTSTOCK>`, en lecture : famille F4 acdd24c,
    famille F7 12280a5, noyau 76f28bd, BSP `nucleo-f429zi` b9fe2bf.
- Écart au fichier d'étape : `seed remove` refuse de retirer la famille F4, qui est la famille du
  BSP `nucleo-f429zi`. L'ajout et le retrait d'un porteur sont donc essayés avec la famille F7
  (porteur de 2 clés projetées), dans le même rootstock d'essai. Ses clones tiers sont tirés des
  miroirs publics `lepton-distribution/mirror-*`, en lecture.
- Relevés bruts : `env-51-messages/avant/<n°>-<nom>.{cmd,out,err,code}`, produits par
  `env-51-messages/releve.sh`. Sorties `--json` : `env-51-messages/avant/json/`.

## 1. Audit (lecture seule) → PA-89

### 1.1 Chemin d'un message de scion
- scion écrit ses messages par `logging` (`scion/cli.py`, `basicConfig`, format `%(message)s`,
  sans préfixe), donc sur stderr. Le niveau est INFO par défaut et DEBUG sous `scion -v`. Les
  erreurs prennent la forme `erreur : …` sur stderr. Pour les commandes lancées par lepton, la
  sortie standard est toujours vide : seuls `version`, `rootstock-information` et `git` écrivent
  sur stdout.
- lepton :
  - `lepton/scion_runner.py`, `run` : `subprocess.run(…, capture_output=True)`. En cas d'échec
    (code ≠ 0), stderr est repris en entier dans la `LeptonError` (code 2), que `cli.main`
    affiche (`lepton: erreur: échec de « … » (code n) :` suivi du stderr de scion). En cas de
    succès, rien n'est affiché : le `CompletedProcess` est rendu.
  - `scion()` passe par `run`, `seed.scion_on_trunk` par `scion()`.
  - Aucun appelant ne lit `.stdout` ni `.stderr` d'un appel de scion. Les seules lectures
    concernent `git` (`seed.py` l. 427-428, `files.py` l. 218, `scions.py` l. 80) et `xmllint`
    (`validation.py` l. 265-270).
  - Sous `-v`, `run` écrit sur stderr `lepton: exécute : <commande>  (dans <rép>)`, pour scion
    comme pour git et xmllint. lepton ne transmet pas `-v` à scion.
- Cause de D10 : les messages de scion d'une commande réussie sont capturés puis abandonnés, avec
  ou sans `-v`. Cela vaut pour toutes les commandes, pas seulement pour P-P6 et P-G6.

### 1.2 Inventaire
La colonne « scion écrit (stderr) » vient des mêmes commandes scion lancées à la main dans
l'essai. La sortie standard de scion est vide dans tous les cas. Toutes les commandes rendent 0.

| Commande lepton (relevés) | Commandes scion lancées | scion écrit (stderr) | lepton affiche |
| --- | --- | --- | --- |
| `graft` (01, 02 ; main : 16) | `graft` | `greffe : 6 chemin(s) ignoré(s) par git, non greffé(s) (détail avec -v)` ; `greffe : 3294 feuilles liées dans <trunk>` | stdout `regreffe complète faite` ; `-v` : + 1 `lepton: exécute :` |
| `graft --scion stm32f4xx`, porteur (03 ; main : 04) | `graft --scion lepton@family-stm32f4xx` | **P-G6** `clés projetées regreffées avec leur porteur lepton/family-stm32f4xx : tiers/stm32f4xx-hal-driver, tiers/cmsis-device-f4` ; `greffe partielle : 239 feuilles liées dans <trunk>` | stdout `regreffe de stm32f4xx faite` |
| `seed replace stm32f4xx`, porteur d'origine distante (05, 06 ; main : 17-20) | `graft-remove --purge`, `seed-scion-add --replace`, `seed-clone`, `graft --scion` | `scion lepton/family-stm32f4xx retiré : 239 feuilles` ; **P-P6** `clés projetées retirées avec leur porteur … : tiers/…, tiers/…` ; `clone <clone> supprimé` ; `scion … déclaré dans <graine>/scion/.scion (version master)` ; seed-clone : rien ; **P-G6** ; `greffe partielle : 239 feuilles…` | stdout `stm32f4xx remplacé (…)`, `graine modifiée, non commitée : …` ; `-v` : + 4 `lepton: exécute :` |
| `seed add stm32f7xx --type famille`, porteur (07, 09 ; main : 11-13) | `seed-scion-add`, `seed-clone`, `graft --scion` | `scion lepton/family-stm32f7xx déclaré dans …` ; seed-clone : rien ; **P-G6** (`tiers/stm32f7xx-hal-driver, tiers/cmsis-device-f7`) ; `greffe partielle : 212 feuilles…` | stdout `stm32f7xx ajouté (…)`, `graine modifiée…` ; `-v` : + 3 `exécute` ; liens 3294 → 3506 |
| `seed remove stm32f7xx`, porteur (08, 10 ; main : 14, 15) | `seed-scion-remove`, `graft-remove` | `scion … retiré de <graine>/scion/.scion` ; `scion … retiré : 212 feuilles` ; **P-P6** | stdout `stm32f7xx retiré (…)`, `graine modifiée…` ; `-v` : + 2 `exécute` ; liens 3506 → 3294 |
| `scion new app51 --type application` (21) | `seed-scion-add`, `seed-clone`, `graft --scion` ; avant cela, git `init`, `add`, `commit` | `déclaré dans …` ; `greffe partielle : N feuilles…` (forme de 27) | stdout : 4 lignes (dépôt créé, ajouté, XML déclaré, graine modifiée) |
| `file add`, `file mv`, `file remove`, `dir add`, `dir remove` (22-26 ; main : 27) | `graft --scion lepton@application-app51` | `greffe partielle : 3 feuilles liées dans <trunk>` | stdout : 1 ligne (`créé dans`, `déplacé dans`, `retiré de`) ; `-v` (23) : + `exécute` git `ls-files` et scion |
| `scion remove app51` (28) | `seed-scion-remove`, `graft-remove` | `retiré de <graine>/…` ; `scion … retiré : N feuilles` | stdout : 3 lignes ; `-v` : + 2 `exécute` scion, 1 xmllint |
| `seed lock` (29) | aucune | — | stdout : verrou |
| `seed lock --restore`, clone du BSP déplacé à HEAD~1 (30) | git `checkout`, puis scion `graft` | comme 16 | stdout `nucleo-f429zi : b9fe2bf93db3 (HEAD détachée)` ; `-v` : + 13 `exécute` (12 git, 1 scion) |
| `seed new env51 -C env-51-new` (31 ; main : 32, 33) | `rootstock-install`, 3 × `seed-scion-add`, `seed-add`, `graft`, `seed-scion-add` (projet), `seed-clone`, `graft --scion` | `rootstock installé dans <rép> (trunk : trunk)` ; 4 × `déclaré dans …` ; seed-add : aucun message INFO (lecture de `cmd_seed_add`) ; `greffe : 3293 feuilles liées…` ; `greffe partielle : …` | stdout : 6 lignes (XML, rootstock, graine, 3 rôles, `lepton generate`) ; `-v` : + 10 `exécute` scion, 3 git, 1 xmllint |

Commandes `--json` (`seed status`, `seed tree`, `check`, `file owner` sur un fichier projeté et
sur un fichier de la famille), relevées dans `avant/json/` : code 0, `json.loads` réussi et stderr
vide pour toutes. Aucune n'appelle scion (`scion()` n'est appelé que depuis `seed.py`, `files.py` et
`scions.py`, dans les chemins listés ci-dessus).

### 1.3 Effets possibles d'un relais
- **Sorties `--json`.** Elles ne sont pas touchées, puisqu'aucune commande `--json` n'appelle
  scion. Un relais sur stdout serait néanmoins à proscrire : il mêlerait scion aux données
  (`seed status`, `check`) et aux messages `_info` de lepton.
- **Canal de sortie de l'extension** (`runner.ts`, `spawn`). stdout et stderr y sont écrits au fil
  de l'eau. La seule exception est le stdout des appels `exec` avec `--json`. Les lignes relayées
  y apparaîtraient donc pour chaque commande lancée par `runner.run`. L'extension ne passe jamais
  `-v` : un relais réservé à `-v` y resterait invisible.
- **Notifications de l'extension** (`lastMessage`, `lepton.ts` l. 72). Le texte part de la
  dernière ligne de stderr qui commence par `lepton:` et va jusqu'à la fin. Il ne sert qu'en cas
  d'échec : `runner.report` pour un code ≠ 0, `watch.ts` (`file add --adopt`), `tree.ts`
  (`seed tree`, sans scion). Un échec se termine par `lepton: erreur: …`, émis par `cli.main` en
  dernier, donc les lignes relayées avant cette ligne n'entrent pas dans la notification.
  Un seul cas se termine sans `lepton: erreur:` : `seed lock --restore` avec écarts (code 1). Ses
  `_warn` viennent après le `graft`, donc après les lignes relayées : la notification ne change
  pas.
  Si le préfixe relayé commençait par `lepton:`, les cas actuels ne changeraient pas non plus.
  Une ligne relayée deviendrait cependant le début de la notification dès qu'un `_warn` la
  précéderait sans erreur finale. Un préfixe sans `lepton:` (par exemple `scion: `) écarte ce
  risque par construction.
- **Messages de lepton déjà émis.** `_info` va sur stdout, `_warn` et `lepton: information:` sur
  stderr, `lepton: exécute :` sur stderr sous `-v`. Un relais sur stderr, écrit au retour de chaque
  appel de scion, prend sa place chronologique entre ces messages. Dans un pipe, stdout est mis en
  tampon par Python : vider stdout avant d'écrire les lignes relayées garde l'ordre dans le canal
  de l'extension. C'est déjà le cas de `_warn` aujourd'hui, sans vidage.
- **Échec d'un appel.** Le comportement actuel reste : stderr est repris dans `lepton: erreur:`. Ne
  relayer qu'en cas de succès évite d'afficher deux fois les mêmes lignes.
- **git, xmllint, cmake.** Ils passent aussi par `run`. Un relais placé dans `scion()`, et non dans
  `run`, les laisse inchangés (piège de l'étape).
- **Tests existants.** Aucun n'exige un stderr vide pour ces commandes. La recherche de
  `err == ""` et de ses variantes ne trouve rien. Le seul test sur stderr,
  `test_project_mkconf.py:161`, porte sur `CFG-5`.

### 1.4 Options soumises au PA-89
1. **Commandes couvertes.** Le relais se place dans `scion_runner.scion()`, ce qui couvre d'un
   coup toutes les commandes du §1.2. L'autre voie est une liste de commandes chez les appelants,
   ce qui ferait plusieurs mécanismes.
2. **Forme.**
   - (a) stderr de scion relayé en entier, en cas de succès ;
   - (b) lignes d'information seules : lepton filtrerait sur le texte de scion, ce qui le lierait
     à sa rédaction (fragile ; NF-2 côté lepton) ;
   - (c) relais sous `-v` seulement : la sortie par défaut ne change pas, mais P-P6 et P-G6 restent
     invisibles sans `-v`, et toujours dans l'extension.
3. **Flux et ordre.** stderr (flux de scion ; stdout reste réservé aux résultats et au JSON),
   écrit au retour de chaque appel, après un vidage de stdout.
4. **Préfixe.** `scion: ` sur chaque ligne (origine lisible, sans effet sur `lastMessage`), ou
   aucun, ou `lepton: scion: ` (risque du §1.3).
5. **Tests.**
   - P-P6 et P-G6 dans `tests/test_projection.py`, qui dispose déjà du porteur `fam-test` : `seed
     replace` du porteur (retrait et regreffe), plus `graft --scion` du porteur.
   - Un test d'un fichier (`file add`) : la ligne `greffe partielle` est relayée.
   - Un test d'un appel git : rien n'est relayé.
   - Un test d'une commande `--json` : stdout est inchangé.
   - Le fixture `fam-test` est la famille du BSP : `seed add` et `seed remove` d'un porteur
     demanderaient un second porteur dans le fixture. À confirmer.

Recommandation de la session : 1 dans `scion()` ; 2 (a) ; 3 stderr, après vidage de stdout ; 4
préfixe `scion: ` ; 5 comme ci-dessus, avec en plus `seed add` et `seed remove` d'un second
porteur ajouté au fixture. Effet visible : 1 à 9 lignes `scion: …` de plus par commande sur stderr
(§1.2), dont les lignes de comptage `greffe : N feuilles liées`.

## 2. PA-89 (2026-11-12, décisions de l'utilisateur)
1. Commandes couvertes : tout appel de scion, par un seul point, `scion_runner.scion()`. git,
   xmllint et cmake ne sont pas relayés.
2. Forme : stderr de scion relayé en entier, après chaque appel réussi. En cas d'échec, rien ne
   change : il reste repris dans `lepton: erreur:`.
3. Flux et ordre : stderr, écrit au retour de l'appel, après vidage de stdout.
4. Préfixe : `scion: ` sur chaque ligne.
5. Tests (`tests/test_projection.py`) :
   - `seed replace` et `graft --scion` du porteur `fam-test` (P-P6, P-G6) ;
   - `seed add` et `seed remove` d'un second porteur, ajouté au fixture ;
   - `file add` : ligne relayée ;
   - appel git : rien n'est relayé ;
   - commande `--json` : stdout inchangé.

## 3. Correction (`devenv/env-51`)
- **Tests d'abord**, a9144e9, `tests/test_projection.py`, section ENV-51 (7 tests) :
  - `test_seed_replace_porteur_relaie_p_p6_p_g6` : P-P6, puis P-G6, relayés dans cet ordre ;
    stdout sans ligne `scion:` ;
  - `test_graft_porteur_relaie_p_g6` : P-G6 et `greffe partielle` ;
  - `test_seed_add_remove_porteur_relaie_p_g6_p_p6` : second porteur, la bibliothèque `lib-p`
    qui porte `tiers@tiers-b` (`_carrier_lib`). P-G6 à l'ajout, P-P6 au retrait, trunk propre ;
  - `test_file_add_relaie_la_greffe` ;
  - garde-fous : `test_echec_de_scion_sans_double_affichage` (une seule ligne `erreur :` de
    scion, non préfixée, dans `lepton: erreur: échec de « scion seed-clone …`),
    `test_git_non_relaye` (`git checkout v1.0` écrit sur stderr et n'est pas relayé),
    `test_json_inchange`.
  - Sur le code de `main`, les 4 premiers échouent, chacun sur l'assertion du relais (liste des
    lignes relayées vide), alors que la commande elle-même rend 0. Les 3 garde-fous réussissent
    déjà, ce qu'implique leur objet : ils protègent un comportement qui ne doit pas changer.
- **Correction**, `lepton/scion_runner.py` :
  - `scion()` appelle `relay(res.stderr)` après `run`, qui a déjà levé l'erreur si l'appel a
    échoué ;
  - `relay` vide stdout, puis écrit sur stderr `RELAY_PREFIX` (`scion: `) devant chaque ligne non
    vide ;
  - `run` et `git` sont inchangés.
  - Les lignes vides du stderr de scion sont omises : un préfixe seul ne porte rien.
- **Documentation** :
  - `README.md`, paragraphe « Messages » ;
  - `rapports/env-8-interface.md`, ligne « Messages (NF-6) » du §1 et §21 « Amendement
    d'ENV-51 » ;
  - `HORS-PLAN.md` : D10 marqué traité.
- **lepton réinstallé** par `pipx install --force <LEPTON_TOOLS>` depuis la branche :
  0.1.0, version inchangée.

## 4. Contrôles → PA-90
- **pytest complet** (venv `venv-lepton-tools`, arbre de 8e71b51) : 384 réussis (377 + 7) en
  7 min 31 s.
- **Essais de la tâche 1 rejoués** avec le lepton réinstallé : relevés
  `env-51-messages/apres/`, mêmes numéros qu'avant.
  - Codes de retour : tous 0, identiques à l'avant.
  - stdout : identique, à deux écarts près, qui viennent de l'état et non de lepton :
    - 05, `seed replace` : l'origine précédente est `https://…` avant et `file://localhost/…`
      après, puisque l'essai d'avant l'a changée ;
    - 31, `seed new` : seul le nom du rootstock diffère, `env-51-new` puis `env-51-new-apres`.
  - stderr : identique, augmenté des seules lignes `scion:`. Exception de relevé : 30
    (`seed lock --restore`) et 31 (`seed new`) avaient été relevés avant sous `-v` et ne le sont
    pas après. Hors lignes `lepton: exécute :` et `scion:`, ils sont identiques.
  - Lignes relayées par commande : `graft` 2 ; `graft --scion stm32f4xx` 2 (P-G6) ;
    `seed replace` 6 (P-P6, puis P-G6) ; `seed add stm32f7xx` 3 (P-G6) ; `seed remove stm32f7xx` 3
    (P-P6) ; `scion new` 2 ; `file add`, `mv`, `remove`, `dir add`, `remove` 1 chacune ;
    `scion remove` 2 ; `seed lock --restore` 2 ; `seed new` 7.
  - Sous `-v`, chaque groupe de lignes `scion:` suit sa ligne `lepton: exécute : scion …` (06,
    23, 28).
  - État final : `env-51-essai` 3294 liens, `env-51-new-apres` 3293 liens, aucun lien cassé ni
    fichier régulier dans le trunk.
  - Manipulation de l'essai : le dépôt `depots/lepton/application-app51` du premier `scion new`
    est supprimé avant le rejeu. `scion remove` ne touche jamais le dépôt (GRF-4), et `scion new`
    refuse un dépôt existant.
- **Échec d'un appel** (40, `seed add absent …` d'une URL absente, code 2) :
  - relayés : `déclaré` (seed-scion-add), puis `retiré de` (annulation) ;
  - le stderr de `seed-clone` en échec apparaît une seule fois, dans `lepton: erreur: échec de
    « scion seed-clone … » (code 2) :`, non préfixé.
- **Sorties `--json`** (`apres/json/`, même état du rootstock que `avant/json/`) : `seed status`,
  `seed tree`, `check`, `file owner` (fichier projeté, fichier de la famille). stdout, stderr et
  code sont identiques octet pour octet, et `json.loads` réussit. `seed-tree.out` (1,5 Mo, identique avant et
  après selon `cmp`) n'est pas conservé : seuls restent son SHA-256 (`seed-tree.out.sha256`) et sa taille.
- **Extension** : pas d'essai dans VSCodium, faute de pilotage de l'interface depuis la session.
  Contrôle par le code et par le code compilé de l'extension 0.5.2 :
  - `runner.ts` (`spawn`) écrit stdout et stderr dans le canal de sortie, sauf le stdout des
    appels `--json`. Les lignes `scion:` y apparaissent donc.
  - `lastMessage` (`out/src/lepton.js`), exécuté par node sur le stderr de l'échec 40, donne le
    même texte avec ou sans les lignes `scion:` : `lepton: erreur: échec de « scion seed-clone … »
    … → corriger la cause signalée par scion, puis relancer`.
  - En cas de succès, `runner.report` n'utilise pas `lastMessage` (notification « done »).
  - L'essai dans l'éditeur reste à faire à la validation Debian (ENV-53, C5) ou par
    l'utilisateur.
- **Aucun binaire touché** : pas d'oracle (décision du début de session). Aucun lien de
  `<ROOTSTOCK>` touché.
- **Rootstocks d'essai** (sort au PA-90) :
  - `essais/env-51-essai` (155 Mo) ;
  - `essais/env-51-new` (117 Mo) ;
  - `essais/env-51-new-apres` (117 Mo) ;
  - `essais/env-51-sources` (29 Mo, 4 clones nus).
- **Branches et commits** (rien de poussé) : lepton-tools `devenv/env-51`, a9144e9 (tests),
  8e71b51 (correction et documentation), suivis du commit d'état et de passation.

## 5. PA-90 (2026-11-12, décisions de l'utilisateur)
- Rapport accepté. L'essai dans VSCodium (canal de sortie de l'extension) est renvoyé à la
  validation Debian (ENV-53, C5) ou à l'utilisateur.
- Rootstocks d'essai supprimés : `essais/env-51-essai`, `env-51-new`, `env-51-new-apres`,
  `env-51-sources`. Les relevés restent sous `env-51-messages/`.
- Publication (PA-P) : commit d'état et de passation, fusion `--no-ff` de `devenv/env-51` dans
  `main`, push de `main` et de `devenv/env-51`.
