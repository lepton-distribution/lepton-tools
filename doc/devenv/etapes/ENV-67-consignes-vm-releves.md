# Étape ENV-67 — Consignes VM : relevés, suppressions, contrôle Mac (D38)

## Contexte
Révision du plan du 2026-11-23, faite à partir de `HORS-PLAN.md`. D38 est à traiter pour ses
sous-points (1) à (3) ; le (4), `zsh` absent de la VM, reste hors plan (décision de l'utilisateur
du 2026-11-23, fin du plan, après ENV-66). Ce n'est pas un ticket : il s'agit des outils des
consignes et de lepton-tools. Les trois sous-points viennent de R66-1
(`rapports/env-66-debian.md` §5.1, §7.1, §8 ; `rapports/env-66-mac.md` §3bis) :
1. **`LEPTON_EMBOS_ROOT`** : la consigne d'ENV-53 la relevait (`consignes/env-53-debian.md`
   l. 189). Les consignes suivantes ne le font plus. Une session VM rouverte au §0 ne l'a pas : en
   R66-1, au premier passage du §12.1, les 8 presets embOS ont échoué à la configuration.
2. **`scripts/supprimer-essai.sh`** n'accepte que `~/tmp-pytest` entier (l. 119 : cas
   `"$H/tmp-pytest" | "$H/tmp-tests"`), pas `~/tmp-pytest/<sous-répertoire>`. Le §14 de la
   consigne d'ENV-66 n'était donc pas exécutable tel qu'écrit. En R66-2, `~/tmp-pytest` a été
   supprimé entier, puis recréé vide.
3. **Contrôle Mac d'une consigne** : rejoué sur le même rootstock d'origine que l'attendu, il ne
   peut faire paraître ni la racine, ni la graine, ni les fichiers ignorés propres au Mac
   (`.DS_Store`). C'est ce qui a causé les classes d'écart de C4 et C5 en R66-1.

D39 (invites simultanées) a été traité à la révision : sa parade est au §2bis d'ORCHESTRATION,
paragraphe « Invites simultanées ». Cette étape n'y touche pas.

L'étape vient d'abord, pour que les règles amendées servent aux consignes suivantes. Rien n'est
fait sur la VM : la preuve se fait en ENV-72. Archétype : infrastructure. Une variable par lot :
- (2) change les entrées acceptées par l'enveloppe ;
- (1) et (3) ne changent que le texte des règles.

Aucun binaire, aucun lien du trunk, aucune commande de lepton ou de scion ne change.

## Prérequis
- ENV-66 terminée ; lepton-tools `main` après la fusion de la révision du 2026-11-23 ; `pytest`
  570 verts.
- Règles des consignes VM : ORCHESTRATION §2bis (« Commandes soumises aux règles », « Outils de
  comparaison », « Invites à refuser »).
- Tests de l'enveloppe : `tests/test_supprimer_essai.py`. Règle `allow` de l'enveloppe :
  `.claude/settings.json`, à ne pas toucher (le chemin du script ne change pas).
- Sources : `consignes/env-66-debian.md` (§0, §5, §12.1, §14), `rapports/env-66-mac.md` §1.4,
  §1.5, §3bis.
- Branche `devenv/env-67` dans lepton-tools seulement.

## Tâches

### 1. Audit (lecture seule) → PA-121
Rapport `rapports/env-67-consignes.md`.
- **(1)** Relever où la VM définit `LEPTON_EMBOS_ROOT` : profil de shell, `install-debian.sh`
  du clone noyau (qui ne la pose pas), consigne. `scripts/lepton-env.sh:37` du clone noyau prend par
  défaut `$LEPTON_ROOTSTOCK/third_party/embos/cortexm-gcc/5.20.0.0`, d'où l'échec de R66-1 quand
  la variable manque. La lecture des fichiers de la VM se fait dans les rapports déjà
  poussés ; à défaut, l'utilisateur relève la valeur. Relever aussi les autres variables
  d'environnement dont dépend une consigne : construction, sonde, `TMPDIR`, `LC_ALL`.
- **(2)** Relever, dans `supprimer-essai.sh`, les cibles admises et leurs bornes. Relever les
  formes que les consignes ont dû écrire (§14 d'ENV-66 ; C8 d'ENV-61, §14 de `consignes/env-61-debian.md`), et les tests existants.
- **(3)** Relever les contrôles de correction des consignes d'ENV-57 à ENV-66, et le rootstock sur
  lequel chacun a été rejoué. Relever les classes d'écart qu'un rootstock distinct aurait fait
  paraître au Mac : racine, graine, fichiers ignorés.
- **PA-121** : l'utilisateur tranche :
  - (1) : forme, qui est l'une de ces trois :
    - relevé de la variable au §5 de chaque consigne, avec arrêt si elle est absente ;
    - pose de la variable au §0 par l'utilisateur ;
    - texte du §2bis qui l'impose.

    Variables couvertes en plus de `LEPTON_EMBOS_ROOT`. <À CONFIRMER au PA-121> ;
  - (2) : cibles admises, qui sont l'une de ces trois :
    - descendants de `~/tmp-pytest` seuls ;
    - descendants de `~/tmp-pytest` et de `~/tmp-tests` ;
    - descendants de `~/env-<N>-journaux` en plus.

    Rejets à garder : lien symbolique, `..`, la racine elle-même si elle doit rester. La règle
    « tout ou rien » est gardée. <À CONFIRMER au PA-121> ;
  - (3) : forme de la règle, qui est l'une de ces deux :
    - contrôle rejoué sur une copie distincte, qui a une autre racine, sa propre graine et ses
      fichiers ignorés ;
    - liste des classes d'écart attendues, écrite dans la consigne.

    <À CONFIRMER au PA-121> ;
  - texte de l'amendement du §2bis ; effets sur `CLAUDE.md` et les skills (une skill se corrige
    sur le compte claude.ai, ORCHESTRATION §5bis).
- Aucune modification avant la réponse.

### 2. Mise en place (`devenv/env-67`)
- Lot (2) : tests d'abord, dans `tests/test_supprimer_essai.py` :
  - un test par forme admise au PA-121, qui échoue sur `main` ;
  - un test par rejet gardé, qui passe déjà.

  Puis l'enveloppe, son en-tête (l. 11-13), la docstring de `tests/test_supprimer_essai.py`, et
  le paragraphe « Suppressions » d'ORCHESTRATION §2bis, qui énumère les cibles admises.
- Lots (1) et (3) : ORCHESTRATION §2bis amendé selon le PA-121, sans recopier de forme de commande
  déjà écrite ailleurs.
- Commits séparés : un par lot.

### 3. Contrôles → PA-122
- `pytest` complet vert, dans la forme couverte par la règle (ORCHESTRATION §2bis).
- Enveloppe essayée au Mac. `~/tmp-pytest` n'existe pas au Mac (relevé du 2026-11-23) : le créer
  pour l'essai, avec des cibles `~/tmp-pytest/env-67-*`, puis le supprimer en fin d'essai par
  l'enveloppe. Chaque forme admise est supprimée ; chaque forme rejetée donne le code 2 et ne
  supprime rien. Décision relevée par `rapports/env-57-mac/decisions.py` : règle `allow`, et non
  classifieur.
- `.claude/settings.json` inchangé (empreinte avant, empreinte après).
- **PA-122** : rapport ; sort des cibles d'essai ; push et fusion de `devenv/env-67` dans `main`
  (PA-P). La preuve sur la VM se fait en ENV-72.

## Critères de validation
- [ ] PA-121 et PA-122 tranchés et consignés.
- [ ] Nouveaux tests de l'enveloppe : échec sur `main`, réussite sur la branche ; `pytest` complet
      vert.
- [ ] Enveloppe : formes admises supprimées, formes rejetées refusées (code 2, rien supprimé),
      décision `allow` relevée.
- [ ] ORCHESTRATION §2bis : règles (1) et (3) écrites selon le PA-121 ; paragraphe
      « Suppressions » conforme aux cibles admises par l'enveloppe.
- [ ] `HORS-PLAN.md` : D38 (1) à (3) marqués traités, avec renvoi au rapport ; (4) hors plan.

## Pièges connus
- Une redirection, `| tee` ou `; echo` fait sortir l'enveloppe de sa règle `allow` (D20) : essayer
  chaque forme seule, et lire le code de retour dans le résultat de l'outil.
- `rm -rf` direct reste jugé par le classifieur : jamais de suppression hors de l'enveloppe.
- Élargir les cibles de l'enveloppe élargit ce que la règle `allow` laisse passer sans invite. Les
  rejets (liens, `..`, chemins hors de `$HOME`) sont prouvés avant tout élargissement.
- `$HOME` diffère entre le Mac (`/Users/…`) et la VM (`/home/…`) : les tests ne figent aucun des
  deux.
- Une règle de consigne qui n'est pas dans le §2bis n'est pas lue par la session suivante (D20,
  ENV-57) : le texte va au §2bis, pas dans une consigne seule.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, branche, décisions PA-121 et PA-122, journal. `HORS-PLAN.md` : D38.
Passation `handoff/env-67.md`.
