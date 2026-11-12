# Passation ENV-52 — scion : extraction partielle des clones projetés (D11) — session du 2026-11-12

## Statut
Terminée. scion 0.6.3.0 (règle P-V7) n'extrait, dans un clone distant de clé projetée, que les
répertoires parents des fichiers projetés, au mode cône de git. Le trunk et les binaires ne
changent pas (oracle `env-52-apres` = `env-49-apres`). Version, branches et fusions sont publiées
(PA-92).

## État exact des dépôts
| Dépôt | Branche | Dernier commit (hash court + titre) | Propre ? |
| --- | --- | --- | --- |
| lepton-tools | `devenv/env-52` (depuis `main` 2dba564), fusionnée `--no-ff` dans `main` et poussée avec `main` (PA-92) | « devenv(env-52): état et passation », puis commit de fusion dans `main` | oui |
| clone noyau `depots/lepton/original/master` | `master` | 58e421e, fusion de `devenv/env-52` (41c9384 : `SCION_REF` 0.6.3.0) ; `master` et la branche poussés | oui |
| seed.scions | `master` | 6416c33, fusion de `devenv/env-52` ; tag annoté `0.6.3.0` sur 87dc108 ; `master`, la branche et le tag poussés | oui |
| autres | `master` / `original-tree` | non touchés : F4 acdd24c, F7 12280a5, WL 9349be2, graine 15740f9 | oui |

`<ROOTSTOCK>` est regreffé par `scion graft` 0.6.3.0, sur accord de l'utilisateur :
- 3 889 liens ;
- liste `chemin -> cible` identique à celle d'ENV-49 (SHA-256 5dbbc69f…) ;
- 629 projetés, `CONFORME` au contrôleur ;
- les 8 clones tiers sont en extraction partielle ;
- `depots/tiers` passe de 242 à 106 Mo.

Le trunk contient 61 `.DS_Store` du Finder, apparus le 2026-11-12 à 15:37 sans que la session les
crée. Ils sont tolérés et sans effet.

Outils et essais :
- scion 0.6.3.0 installé par pipx (`git+file://<SEED_SCIONS>@0.6.3.0`) ;
- lepton 0.1.0 non réinstallé : seuls un commentaire et le `README` ont changé ;
- git 2.50.1 ;
- VM non sollicitée : elle a encore scion 0.6.2.0, qui sera mis à jour en ENV-53 ;
- essais `env-52-copie`, `env-52-vierge` et `env-52-venv` supprimés (PA-92).

## Fait pendant la session
- **Audit** (`rapports/env-52-scion.md` §1) :
  - tableau des 8 clones ;
  - chemin du code ;
  - règles touchées ;
  - essais de `git sparse-checkout` sur des clones temporaires des miroirs : cône, non-cône, casse,
    caractères spéciaux, conversion, git 2.18 ;
  - versions de git, effets hors de scion, projet d'amendement.
- **PA-91** tranché (§2).
- **seed.scions** (§3) :
  - amendement 5c8c217 et précision 0b4e83d ;
  - tests 51b6421 (13, dont 11 échouent sur 0.6.2.0) ;
  - `gitops` 950981d ;
  - `graft` eefd23c ;
  - version 87dc108 ;
  - suite : 282 réussis, 1 sauté ; NF-2 : 0 ligne Lepton ajoutée.
- **Essais** (§4) : copie d'essai et rootstock neuf `CONFORME`, `lepton check` et `generate` à 0,
  et l'espace de travail identique, aux chemins près.
- **Références de version** (§5.1) :
  - `SCION_REF` 0.6.3.0 dans lepton-tools (b0c3f75) et dans le clone noyau (41c9384) ;
  - skill `lepton-rootstock` (9aa62a6) ;
  - `pytest` : 384 réussis.
- **`<ROOTSTOCK>`** regreffé (§5.2) et oracle après (§5.3) : 16 presets à code 0, banc KAL et
  fumée identiques, mklepton identiques, `ctest -N` 17/17.
- **Fin** : `HORS-PLAN.md`, D11 marqué traité ; PA-92 tranché ; publication faite.

## Reste à faire dans l'étape
- [x] Tout ENV-52.
- [ ] Hors étape, en ENV-53 :
  - installer scion 0.6.3.0 sur la VM (`install-debian.sh` du noyau 58e421e) ;
  - prouver la casse sur un système qui la distingue (`core.ignoreCase` faux sur la VM, à relever) ;
  - regreffer les rootstocks d'essai du Mac qui ont des clones projetés : `essais/env-13-vierge`,
    `essais/env-11/f429zi`, `essais/env-11/wl55jc1`, `essais/env-39-copie`. `scion graft` suffit à
    convertir leurs clones.

## Décisions
| Décision | Auteur (utilisateur / proposition non validée) | Consignée dans DEVENV-STATUS ? |
| --- | --- | --- |
| Plan de session (audit en lecture seule jusqu'au PA-91, accord avant tout `graft-update` ou `seed-update`) | utilisateur | oui |
| PA-91 : cône, parents des sources ; par défaut sans option ; clones convertis par la prochaine greffe ; git ≥ 2.35, sinon erreur ; aucun code lepton ; 0.6.3.0 ; `SCION_MIN_VERSION` inchangé, `SCION_REF` relevé ; oracle après ; amendement validé | utilisateur | oui |
| Regreffe de `<ROOTSTOCK>` par `scion graft` | utilisateur | oui |
| PA-92 : rapport accepté, précision 0b4e83d comprise ; 3 essais supprimés ; publication dans l'ordre seed.scions, noyau, lepton-tools | utilisateur | oui |
| Message de niveau info seulement si l'ensemble change ; `-v` liste toujours les répertoires | proposition non validée (texte du §1.7 validé ; détail d'implémentation) | non |
| `graft-remove` ne réduit pas l'ensemble (excédent sans effet) | validé dans le texte du PA-91 | oui (PA-91) |
| Relevé du trunk rangé dans `rapports/env-52-scion/rootstock/` et non dans `oracles/env-52-apres/trunk/` (le hook refuse une écriture shell dans `…/trunk/`) | proposition non validée, exposée au PA-92 sans objection | journal |
| Hook non modifié : `git sparse-checkout list` reste refusé ; la skill indique les lectures admises | PA-91 (effets : hook inchangé) | oui |

## Pièges rencontrés
- `logging.basicConfig` de scion ne s'installe qu'une fois par processus de test. Le stderr capturé
  par `support.run` ne contient donc pas les messages de niveau info : les tests les lisent par
  `assertLogs`.
- Le mode cône extrait aussi les fichiers placés directement dans les répertoires ancêtres. Un
  test qui compte les fichiers extraits doit les inclure (`Src/x.c` pour `Src/deep/*`).
- `git sparse-checkout set` active l'extension `worktreeConfig`. git 2.18.0
  (`/usr/local/git/bin/git`, plus loin dans le PATH du Mac) refuse alors d'ouvrir le clone.
- Le hook refuse toute écriture shell dans un chemin qui contient `trunk/`, même sous
  `doc/devenv/rapports/oracles/…/trunk/`. Il la refuse aussi quand le répertoire courant est
  resté dans un tel répertoire : revenir à la racine de lepton-tools.
- `ctest --test-dir` ajoute la ligne « Internal ctest changing into directory ». Pour comparer à
  `ctest-N` d'ENV-49, lancer `ctest -N` depuis le répertoire de construction.
- `scion rootstock-install` ne prend pas de chemin : il se lance dans un répertoire vide.
- zsh n'a pas `PIPESTATUS` : relever le code de retour sans tube.

## Critères de validation
- [x] PA-91 et PA-92 tranchés et consignés.
- [x] Amendement de `projection-miroir.md` commité avant le code ; aucun nom propre à Lepton
      ajouté : `git diff 0.6.2.0 -- scion tests | grep -ci '^+.*lepton'` → 0.
- [x] Tests de scion verts, dont les nouveaux (282, 1 sauté).
- [x] Copie d'essai, rootstock neuf et `<ROOTSTOCK>` : liste `chemin -> cible` identique, contenu
      projeté identique, fichiers extraits conformes au PA-91.
- [x] Références de version conformes au PA-91.
- [x] `HORS-PLAN.md` : D11 marqué traité, avec renvoi au rapport.

## Reprise
Commande ou première action de la session suivante :
```
démarrer ENV-53 (skill devenv-session) : lire etapes/ENV-53-validation-debian.md et cette
passation ; consigne consignes/env-53-debian.md (PA-93) : scion 0.6.3.0 et lepton sur la VM,
relais des messages (C5), extraction partielle (casse, git 2.47.3), cartes ; regreffer les
rootstocks d'essai du Mac qui ont des clones projetés
```
