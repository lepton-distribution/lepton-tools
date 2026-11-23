# ENV-67 — Consignes VM : relevés, suppressions, contrôle Mac (D38 (1) à (3))

Audit en lecture seule (tâche 1), 2026-11-23, session Mac. Sources : `consignes/env-53-debian.md`
à `consignes/env-66-debian.md`, `rapports/env-57-mac.md`, `rapports/env-61-mac.md`,
`rapports/env-66-mac.md`, `rapports/env-66-debian.md`, `scripts/supprimer-essai.sh`,
`tests/test_supprimer_essai.py`, scripts du clone noyau `master` 2b4a647. Claude Code 2.1.330.

## 1. D38 (1) — variables d'environnement des consignes

### 1.1 `LEPTON_EMBOS_ROOT`

| Lieu | Constat |
| --- | --- |
| `scripts/lepton-env.sh:37` (clone noyau) | `LEPTON_EMBOS_ROOT="${LEPTON_EMBOS_ROOT:-$LEPTON_ROOTSTOCK/third_party/embos/cortexm-gcc/5.20.0.0}"` : défaut silencieux, relatif au rootstock courant |
| `scion/cmake/kal/embos.cmake:13` (clone noyau) | `set(LEPTON_EMBOS_ROOT "$ENV{LEPTON_EMBOS_ROOT}" CACHE PATH …)` ; erreur l. 22 « embOS introuvable » si le répertoire manque |
| `install-debian.sh`, `install-macos.sh` (clone noyau) | ne la posent pas ; `install-macos.sh:249` demande la copie manuelle du paquet |
| Mac | `~/.zshrc:14` : `export LEPTON_EMBOS_ROOT="$HOME/lepton/third_party/embos/cortexm-gcc/5.20.0.0"` (le rapport d'ENV-11 citait la l. 15) |
| VM | aucun export dans `~/.bashrc`, `~/.profile`, `/etc/profile.d` (`rapports/env-66-debian.md` §7.1) ; paquet dans `~/lepton/third_party/embos/cortexm-gcc/5.20.0.0` |
| Consignes VM | relevé `echo "LEPTON_EMBOS_ROOT=${LEPTON_EMBOS_ROOT:-absente}"; ls -d ~/lepton/third_party/…` au §5 des consignes d'ENV-13 à ENV-53 (`env-53-debian.md:189`) ; **absent** d'ENV-57, ENV-61, ENV-66 |

Effet : en R66-1 (session rouverte au §0), `rejouer-oracle.sh` sur `essais/env-53-debian` a pris le
défaut `<R53>/third_party/…`, absent ; 8 presets embOS en échec. En R57-1 et R61-1 la variable
venait probablement du terminal qui avait lancé la session (`rapports/env-66-debian.md` §7.1).

Une affectation en tête de commande (`LEPTON_EMBOS_ROOT=… cmd`) fait sortir la commande de sa règle
`allow` (§2bis, Formes) ; `rejouer-oracle.sh` est déjà jugé par le classifieur (accepté).

### 1.2 Autres variables lues avec un défaut silencieux

| Variable | Lue par | Défaut | Relevée aujourd'hui |
| --- | --- | --- | --- |
| `SCION_REF`, `SCION_SPEC` | `install-debian.sh:55-56`, `install-macos.sh:126-127` | `0.6.3.3`, URL GitHub | oui, §5 (`printenv SCION_REF SCION_SPEC`, attendu vides) |
| `LEPTON_CLONE` | `install-vscodium.sh:66` | vide | non |
| `XDG_CONFIG_HOME` | `install-vscodium.sh:150` | `~/.config` | non |
| `NM`, `SIZE` | `scripts/oracle/capturer-oracle.sh:16-17` | `arm-none-eabi-nm`, `arm-none-eabi-size` | non |
| `LC_ALL`, `LANG` | git, outils de comparaison | — | non ; `LC_ALL=C` posé dans chaque outil (D27) ; git écrit en français sur la VM même sous `LC_ALL=C` (constat 9 d'`env-57-debian.md`) |
| `TMPDIR` | pytest | `/tmp` | sans objet : `--basetemp ~/tmp-pytest/env-<N>` (§11.3) ; `TMPDIR=` en tête interdit (§2bis) |
| `CLAUDE_PROJECT_DIR` | hook | — | oui, §5 (vide en R66-1, constat mineur) |

`LEPTON_ROOTSTOCK`, `LEPTON_TRUNK`, `LEPTON_CLONE`, `LEPTON_BUILD` sont recalculées par
`lepton-env.sh` à chaque `source` (non héritées). `SOURCE_DATE_EPOCH` n'est plus lue par aucune
consigne depuis ENV-11.

## 2. D38 (2) — `scripts/supprimer-essai.sh`

### 2.1 Cibles admises (en-tête l. 7-15, `juger` l. 100-128)
- descendant strict d'`essais/` hors références (`REFERENCES`, l. 22), hors `trunk/` et
  `depots/tiers/` ;
- `<rootstock>/build/<preset>` (signature scion présente ; `~/lepton` ou descendant d'`essais/`) ;
- `~/env-<N>-journaux` (`N` numérique), **`~/tmp-pytest` et `~/tmp-tests` entiers seulement**
  (l. 119 : `"$H/tmp-pytest" | "$H/tmp-tests") ;;`) ; tout descendant → « hors des bornes ».

Bornes : résolution par `resoudre` (parents suivis par `cd -P`, `.` et `..` réduits, dernier
composant non suivi : un lien final est supprimé sans être suivi), cible absente refusée, `$HOME`
canonisé (`canon_rep`), tout ou rien, code 2. Un `~/tmp-pytest` qui serait un lien se résout vers
sa cible, donc hors des bornes pour ses descendants.

### 2.2 Formes que les consignes ont dû écrire

| Consigne | Forme | Effet |
| --- | --- | --- |
| `env-61-debian.md` §14 (C8) | `~/tmp-pytest/env-57` relevé (`du -sh`) mais **absent** de la liste de suppression ; « Conservés : … `~/tmp-pytest` » | contournement : rien supprimé sous `~/tmp-pytest` |
| `env-66-debian.md` §14 (C9) | `scripts/supprimer-essai.sh … ~/tmp-pytest/env-61` | refus (hors des bornes), tout ou rien : C9 partiel ; en R66-2, `~/tmp-pytest` supprimé entier puis recréé vide (`rapports/env-66-mac.md` §3bis) |

Le pytest des consignes écrit sous `~/tmp-pytest/env-<N>` (`--basetemp`, `env-66-debian.md` §11.3,
421 Mo pour `env-61`) : le besoin réel est de supprimer le sous-répertoire d'une validation
précédente en gardant celui de la validation courante.

### 2.3 Tests existants (`tests/test_supprimer_essai.py`, 14 fonctions)
`ACCEPTES` (l. 54-64) contient `tmp-pytest` et `tmp-tests` entiers ; `REFUSES` (l. 76-106)
contient `env-53-journaux/sous` (descendant de journaux refusé) mais aucun descendant de
`tmp-pytest` ou `tmp-tests`, ni lien sous ces racines. Règle `allow` :
`.claude/settings.json` l. 4-5 (chemin du script seul, inchangé par l'étape).

## 3. D38 (3) — contrôle Mac des consignes

| Étape | Attendu produit sur | Contrôle de la consigne rejoué sur | Ce que la VM avait de différent | Écarts non prévus en R |
| --- | --- | --- | --- | --- |
| ENV-57 | copie `essais/env-57-essai` d'`essais/env-11/qemu` | les **mêmes attendus** (blocs de comparaison éprouvés en bash, `c4 : écarts=0 / 231`) | copie de `$C5` (`essais/env-53-c5`) : graine `env11` (commit, presets), `salut`, clones F7 | `*-status.out` (base de la copie) déclarés « informatifs » d'avance ; rien d'imprévu |
| ENV-61 | copie `essais/env-61-essai` d'`essais/env-11/qemu` | copie des attendus **traduite à la main** (`c4 0 / 528`, `fixture56 0 / 76`) | git 2.47.3 (U+00A0), `localhost/home` | faux 0 / 76 : la simulation avait remplacé U+00A0 par une espace ordinaire ; segment d'hôte non normalisé (corrigés en ENV-62, D27, `comparer-releves.py`) |
| ENV-66 | copie `essais/env-66-essai/c4/rs` d'`essais/env-11/qemu` | essai neuf `c4t`, **même origine** `essais/env-11/qemu`, copie par `tar` (`écarts=1 / 289`) | copie d'`essais/env-53-c5` | C4 : 50 / 289, classes 1 (racine), 3 (`.DS_Store` ignorés dans les clones), 4 (graine `env11`) ; C5 : `depart.etat`, `l03.etat` (empreinte de la graine) |

Classes qu'une copie d'origine distincte aurait fait paraître au Mac :
- **racine** du rootstock : `./.DS_Store` (Finder) et `./.scion.trunk.tolerated` présents dans
  `essais/env-11/qemu`, absents de la racine de `$C5` sur la VM ;
- **graine** : commit de la graine `env11` (`718cccdd25ab` contre `8a6a9d74d306`) et presets
  déclarés (`env11-debug-qemu` seul sur la VM) ;
- **fichiers ignorés par git** propres au Mac : `.DS_Store` dans les clones (noyau 6, BSP an386 7)
  → ligne « N chemin(s) ignoré(s) par git » dans 15 `.err` ;
- hors de ces trois : l'hôte (zsh absent, `clangd` contre `clangd-mp-21`), que seule la VM montre.

Copies distinctes disponibles au Mac : `essais/env-13-vierge` (rootstock neuf depuis la graine
publiée `original-tree`, racine propre, graine `lepton-seed.scions/original-tree`) ; `~/lepton`
(lecture seule, interdit aux essais). Aucune copie du Mac n'a la graine `env11` hors
d'`essais/env-11/qemu`. Une copie distincte se fabrique par `tar` d'`essais/env-11/qemu` en
retirant les `.DS_Store` et en modifiant la graine (commit vide), ou en partant d'`env-13-vierge`
quand l'essai ne dépend pas d'`env11`.

## 4. PA-121 — questions

Voir `DEVENV-STATUS.md` §Décisions (PA-121) pour les réponses.

1. (1) Forme : relevé au §5 avec arrêt si absente, pose au §0 par l'utilisateur, ou texte du
   §2bis ; variables couvertes en plus de `LEPTON_EMBOS_ROOT`.
2. (2) Cibles admises : descendants de `~/tmp-pytest` seuls, de `~/tmp-pytest` et `~/tmp-tests`,
   ou aussi de `~/env-<N>-journaux`.
3. (3) Forme de la règle : contrôle rejoué sur une copie distincte, ou liste des classes d'écart
   attendues écrite dans la consigne.
4. Texte de l'amendement du §2bis ; effets sur `CLAUDE.md` et les skills.

## 5. Mise en place (après le PA-121)

| Lot | Commit | Contenu |
| --- | --- | --- |
| (2) | 7a54b2d | `supprimer-essai.sh` : cas `"$H"/tmp-pytest/?* \| "$H"/tmp-tests/?*` ajouté dans `juger`, en-tête l. 13-15 ; `tests/test_supprimer_essai.py` : docstring, fixture (`tmp-pytest/env-61/sous/plus`, `env-66`, `tmp-tests/a`, `tmp-pytestx`, lien `tmp-pytest/lien-lepton` → `~/lepton`), 18 cas ; ORCHESTRATION §2bis « Suppressions » |
| (1) | 27f5479 | ORCHESTRATION §2bis « Variables d'environnement » |
| (3) | cad0172 | ORCHESTRATION §2bis « Contrôle Mac d'une consigne » |

Tests d'abord (lot (2)), sur le script de `main` : 8 échecs (6 `test_descendant_tmp_accepte`,
`test_descendant_tmp_garde_la_validation_courante`, `test_lien_sous_tmp_supprime_sans_suivre`),
62 réussites, dont les 10 rejets gardés (`REFUSES_TMP` ×7, descendant absent, racine en lien,
tout ou rien). Après correction : 70 / 70 ; shellcheck 0.11.0 sans remarque.

## 6. Contrôles (→ PA-122)

- **pytest complet** (`~/lepton-tools-dev/venv-lepton-tools/bin/pytest -q -p no:cacheprovider`,
  forme seule) : **588 passed** (570 + 18), 8 min 46 s.
- **Enveloppe au Mac** (Claude Code 2.1.330), cibles créées pour l'essai : `~/tmp-pytest/env-67-a/x`,
  `~/tmp-pytest/env-67-b/sous/plus/f`, `~/tmp-tests/env-67-c`, lien `~/tmp-pytest/env-67-lien` →
  `~/lepton`. Chaque forme lancée seule, code lu dans le résultat de l'outil :

  | Essai | Forme | Code | Effet |
  | --- | --- | --- | --- |
  | R1 | `~/tmp-pytest/env-67-lien/trunk` | 2 | « hors des bornes : …/lepton/trunk » |
  | R2 | `~/tmp-pytest/env-67-a/..` | 2 | « non résoluble » |
  | R3 | `~/tmp-pytest/../lepton` | 2 | « hors des bornes : …/lepton » |
  | R4 | `~/tmp-pytestx` | 2 | « hors des bornes » |
  | R5 | `~/tmp-pytest/env-67-a ~/tmp-pytest/env-67-absent` | 2 | « cible absente » ; `env-67-a` gardé (tout ou rien) |
  | A1 | `~/tmp-pytest/env-67-a` | 0 | supprimé |
  | A2 | `~/tmp-pytest/env-67-b/sous/` | 0 | supprimé ; `env-67-b` gardé |
  | A3 | `~/tmp-pytest/env-67-lien` | 0 | lien supprimé, `~/lepton/trunk` intact |
  | A4 | `~/tmp-tests/env-67-c` | 0 | supprimé |
  | N | `~/tmp-pytest ~/tmp-tests` | 0 | nettoyage final, racines absentes ensuite |

  Après R1 à R5 : arbre inchangé (`find`). **Décisions** (`rapports/env-57-mac/decisions.py
  <journal> --motif supprimer-essai`) : les 10 appels `accept config subcommandResults` (règle
  `allow` du dépôt), aucun `classifier`.
- **`.claude/settings.json`** : `b01ad557…d235` avant et après ; `git diff main` vide.
- **Skill `lepton-cibles`** : correction à faire par l'utilisateur sur le compte claude.ai
  (PA-121 (4)), puis `scripts/importer-skills.sh` sur `devenv/env-67`.
