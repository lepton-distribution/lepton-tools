# Étape ENV-55 — lepton : URL `file:///` reconnue (D13)

## Contexte
Révision du plan du 2026-11-12, faite à partir de `HORS-PLAN.md` : D13 est à traiter (décision de
l'utilisateur du 2026-11-12, fin du plan). lepton prend une URL `file:///chemin` (trois barres)
pour un chemin local relatif au répertoire courant :

```
lepton seed add absent file:///Users/…/x.git
→ origine locale « file:///… » : <rootstock>/file:/Users/…/scion absent   (code 1)
```

`file://localhost/chemin` est reconnu comme URL. Sources : `rapports/env-53-mac.md` §1.5 (O-1) ;
relevé `~/lepton-tools-dev/essais/env-53-mac/c5/constat-file-3-barres/`.

Faits relevés à la révision (numéros de ligne indicatifs) :
- `lepton/seed.py` distingue une URL d'un chemin par `urlparse(loc).netloc` :
  - dans `parse_location` (l. 73, test l. 88) ;
  - dans la propriété `Origin.remote` (l. 66-67).
  Ce champ est vide pour `file:///…`.
- `Origin.remote` sert aussi :
  - aux l. 698 et 706 : `--purge` de `graft-remove`, dans `seed_replace` ;
  - à la l. 747 : `_locked_entries`, verrou ;
  - à la l. 865 : `_restore`.
- scion fait le même test : `is_remote` (`<SEED_SCIONS>/scion/mirror.py` l. 37-38) sert à
  `scion/mirror.py` (l. 63), `scion/graft.py` (l. 47, 117, 137, 744), `scion/cli.py` (l. 104,
  184) et `scion/seed.py` (l. 63). Une origine `file:///…` transmise telle quelle à scion y serait
  donc lue aussi comme un chemin local. C'est à établir par l'audit.

Archétype : infrastructure. Iso-fonctionnel pour toutes les autres formes d'origine. Aucun binaire
ni aucun lien du trunk ne doit changer.

## Prérequis
- ENV-53 terminée ; ENV-54 conseillée avant (règles de permission pour les essais). Indépendante
  d'ENV-56.
- lepton 0.1.0 ; scion 0.6.3.0.
- Code (relevé au 2026-11-12) :
  - `lepton/seed.py` : `_ORIGIN` (l. 35), `Origin` (l. 60), `parse_location` (l. 73) ; message
    qui conseille `file://localhost…` (l. 91-93) ;
  - appelants de `parse_location` : `seed new` (l. 358-360 : noyau, famille, BSP), `seed add`
    (l. 601), `seed replace` (l. 694), `lepton/scions.py:166` (`scion new`).
- Tests : l'aide `url()` de `tests/conftest.py` (l. 88-90) rend `file://localhost<chemin>`. Elle
  est appelée par `test_milestone3.py`, `test_milestone6.py`, `test_projection.py` et
  `test_project_mkconf.py`, et par la fixture `project` pour le noyau. Venv
  `~/lepton-tools-dev/venv-lepton-tools`.
- Extension : `extension/src/commands.ts` (`seedAdd` lance
  `seed add <nom> <origine> --type <type> --version <v>`, `master` par défaut, l. 87). Par
  l'extension, une origine `file:///` aboutit donc au message des l. 90-93 (version sans effet),
  pas à celui de la l. 97.
- Skill `lepton-rootstock` (rootstock d'essai).
- Branche `devenv/env-55` dans lepton-tools seulement.

## Tâches

### 1. Audit (lecture seule) → PA-97
- Table de comportement dans `rapports/env-55-url-file.md` §1. Pour chaque forme d'origine,
  relever ce que fait lepton (`parse_location`, `Origin.remote`, ce qui est écrit dans la graine),
  puis ce que fait scion de la valeur reçue (`is_remote`, `git clone`). Formes :
  - `file:///abs`, `file://localhost/abs`, `file:/abs`, `file://<autre hôte>/abs` ;
  - `FILE:///abs` (casse du schéma) ;
  - chemin absolu, chemin relatif ;
  - chacune avec `@VERSION` et avec `:PATH`, puis avec les options séparées `--version` et
    `--path`.
- Chaque endroit où lepton relit une origine enregistrée : `seed lock`, restauration, `check`,
  `seed status`, `generate`, `seed replace` (`--purge`).
- Essai sur un rootstock d'essai à graine de projet, jamais sur `<ROOTSTOCK>` :
  - rootstock `essais/env-55-essai`, copie d'`essais/env-11/qemu` par `rsync -a`, sans `build/`
    (forme d'`essais/env-53-c5`, `rapports/env-53-mac.md` §1.5) ;
  - origine absente : `file:///…/env-55-absent.git` et `file://localhost/…/env-55-absent.git` ;
  - origine présente : un dépôt git local d'essai, sous `essais/` ; sa forme est fixée à l'audit.
- Effets possibles :
  - l'extension (origine saisie par l'utilisateur) ;
  - le message d'erreur de la l. 91-93 ;
  - `README.md`, s'il décrit les origines.
- **PA-97** : l'utilisateur tranche :
  - forme retenue : <À CONFIRMER au PA-97>. Options :
    - `file:///` accepté et transmis tel quel ;
    - `file:///` normalisé en `file://localhost/` ;
    - `file:///` refusé, avec un message qui donne la forme `file://localhost/` ;
  - autres formes (`file:/abs`, autre hôte, casse) : <À CONFIRMER au PA-97> ;
  - si scion doit changer (forme transmise telle quelle) : étape scion insérée, avec son propre
    point d'arrêt. ENV-56 ne traite que D14 ;
  - tests : forme et emplacement.
- Aucune modification avant la réponse.

### 2. Correction (`devenv/env-55`)
- Écrire les tests d'abord : un test par forme retenue au PA-97, qui échoue sur `main`. Les
  formes déjà reconnues gardent leur comportement, chacune couverte par un test.
- Puis la correction : une seule fonction de classification, commune à `parse_location` (l. 88)
  et à `Origin.remote` (l. 67). Pas de traitement commande par commande.
- Mettre en cohérence le message de la l. 91-93 et `README.md` si la forme acceptée change.
- Réinstaller lepton : `pipx install --force <LEPTON_TOOLS>`, depuis la branche.

### 3. Contrôles → PA-98
- `pytest` complet vert (384 après ENV-53, plus les nouveaux).
- Table du §1 rejouée sur `essais/env-55-essai` :
  - les lignes `file:///` suivent le PA-97 ;
  - toutes les autres lignes sont identiques à l'avant (codes de retour et sorties) ;
  - liens du trunk et graine égaux à l'avant après l'annulation de chaque essai (`seed remove`
    après un ajout réussi).
- Extension : `seedAdd` avec une origine `file:///`, dans le canal « Lepton » ; sinon, la raison
  de ne pas l'essayer est donnée au rapport.
- **PA-98** : rapport ; sort d'`essais/env-55-essai` et du dépôt d'essai ; push et fusion de
  `devenv/env-55` dans `main` (PA-P). La validation Debian est faite en ENV-57.

## Critères de validation
- [ ] PA-97 et PA-98 tranchés et consignés.
- [ ] Table du §1 au rapport, avant et après.
- [ ] Nouveaux tests : échec sur `main`, réussite sur la branche ; `pytest` complet vert.
- [ ] Formes d'origine autres que celles du PA-97 : comportement inchangé.
- [ ] `HORS-PLAN.md` : D13 marqué traité, avec renvoi au rapport.

## Pièges connus
- `Path("file:///x").resolve()` donne `<cwd>/file:/x`. Le message actuel nomme donc un chemin
  qui n'existe pas : ne pas le prendre pour la cause.
- `_ORIGIN` sépare `@VERSION` et `:PATH`, et l'autorité d'une URL (`scheme://[user@]hôte`) garde
  son `@`. Une autorité vide (`file:///`) peut tromper une correction faite par expression
  régulière.
- scion et lepton doivent classer une origine de la même façon. Une forme acceptée par lepton
  mais lue comme un chemin par scion échoue plus tard (`seed-clone`, `graft`). C'est à vérifier
  à l'audit.
- L'échec d'un `seed add` laisse un répertoire vide `depots/<étagère>/<greffon>` (D14, corrigé en
  ENV-56) : le retirer par `rmdir` après chaque essai et le noter.
- Sur la graine de référence, lepton refuse `seed add` (`refuse_reference`) : tout essai se fait
  sur un rootstock d'essai à graine de projet.
- Ne jamais lancer l'essai dans `essais/env-11/qemu` lui-même.
- `zsh` ne découpe pas une variable en mots : utiliser `bash -c` ou un script.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, branche, §Versions (lepton, s'il est réinstallé), décisions PA-97 et
PA-98, journal. `HORS-PLAN.md` : D13. Passation `handoff/env-55.md`.
