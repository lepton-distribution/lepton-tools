# ENV-15 — Fichiers ignorés et fichiers étrangers dans scion

Session du 2026-10-30. scion de départ : 0.5.1.1 (`master` f1d1f3c de `<SEED_SCIONS>`), branche
`devenv/env-15`.

## 1. Audit (tâche 1, lecture seule)

### 1.1 Code
| Fonction (`scion/graft.py`) | Rôle | Lien avec l'étape |
| --- | --- | --- |
| `_walk(base)` l. 127 | parcourt `scion/` d'un greffon, saute `.scion/`, rend `dir` / `leaf` | aucun filtre : tout fichier présent est une feuille |
| `_graft_entries` l. 209 | crée les liens des greffons choisis, collecte les conflits, annule tout en cas de conflit | seul appelant de `_walk` pour la greffe |
| `graft` l. 168 | greffe complète (après `ungraft` dans `cmd_graft`, `cmd_graft_update`) | |
| `graft_scions` l. 364 | `graft --scion` : `_check_stray`, `_unlink`, `_graft_entries`, `_prune` | |
| `remove` l. 385 | `graft-remove` : `_check_stray`, `_unlink`, `_walk` (répertoires candidats), `_prune` | |
| `ungraft` l. 263 | vide le trunk ; `_check_stray` avant | |
| `_check_stray` l. 285 | tout fichier régulier du trunk (hors `.scion.grafted.list`) bloque, sauf `--force` (conservé) | E2 |
| `sync` l. 43 | résout le seed ; source locale = chemin, distante = clone sous `depots/` | sources non git |

`scion/gitops.py` : toutes les invocations git passent par `run` / `_run` (liste d'arguments,
`check=True`, `GitError` code 2). `cmd_graft_update` (`cli.py`) : `ungraft` puis `sync` puis
`graft` — un échec de `graft` après `ungraft` laisse le trunk vide (constat du 2026-10-30).

Tests : 106 (`python3 -m unittest discover -s tests`), verts, 1 ignoré ; fixture sans réseau
(`tests/make_fixture.py`, dépôts servis en `file://localhost`). Les tests ne fixent pas la
configuration git globale : une règle de `~/.gitignore_global` s'y applique.
`grep -ri lepton scion/` : 2 lignes de métadonnées (`__url__`, `__email__`), tolérées (PA-2 Q7).

### 1.2 Mesures sur les rootstocks existants
| Rootstock | Greffons git | Fichiers ignorés non suivis | Non suivis non ignorés | Source non git |
| --- | --- | --- | --- | --- |
| `~/lepton` (3929 liens) | 8 | 0 | 0 | `building` (`depots/generation/building`, 0 feuille, répertoires seuls) |
| `essais/env-9`, `env-11/{qemu,qemu-gra2,f429zi,wl55jc1}`, `env-13-vierge` | 4 à 9 | 0 | 0 | `building` |

Conséquence : le filtre E1 ne retire aucun lien sur ces rootstocks (somme des feuilles des 8
greffons de `~/lepton` = 3929 = liens du trunk). Le `CMakeUserPresets.json` de la graine de projet
(`essais/env-9`) n'est pas ignoré : il reste greffé.

Le `.gitignore` du clone noyau cite `.DS_Store` (l. 482) ; `~/.gitignore_global`
(`core.excludesfile`) aussi. Git 2.50.1 (Mac).

### 1.3 Essai de `git ls-files` et `git check-ignore` (dépôt jetable)
`git ls-files --others --ignored --exclude-standard --directory -z -- .` lancé dans `scion/` :
un seul appel, sans liste en entrée ; rend les fichiers ignorés non suivis et les répertoires
entièrement ignorés (`a/build/`) ; un fichier suivi qui correspond à une règle (`a/suivi.o`) n'est
pas rendu ; un fichier non suivi non ignoré (`b/nouveau.c`) non plus. `check-ignore --stdin -z`
donne le même ensemble mais exige la liste de tous les chemins ; hors dépôt, les deux sortent en
code 128.

## 2. Propositions (PA-17)

### E1 — filtre des fichiers ignorés
- Point d'application : `_graft_entries`, une fois par greffon : ensemble des chemins ignorés
  calculé par un appel `git ls-files --others --ignored --exclude-standard --directory -z -- .`
  dans `scion/` (nouvelle fonction `gitops.ignored(stem)`), passé à `_walk(base, ignored)` qui
  saute les feuilles ignorées et ne descend pas dans un répertoire ignoré (ni répertoire créé dans
  le trunk). Même filtre dans le `_walk` de `remove` (répertoires candidats).
- Règles : celles de git (`.gitignore`, `.git/info/exclude`, `core.excludesFile`) ; un fichier
  suivi n'est jamais exclu ; un fichier non suivi non ignoré reste greffé.
- Source non git (`git rev-parse --show-toplevel` en échec, ex. `building`) : aucun filtre,
  comportement inchangé. Dépôt git qui contient le rootstock lui-même (rootstock versionné) :
  traité comme non git, pour qu'un `depots/` ignoré par ce dépôt ne vide pas la greffe.
- Journal : `-v` (DEBUG) une ligne par chemin exclu (`exclu (ignoré par git) : <scion> <chemin>`) ;
  INFO : le nombre total d'exclus s'il est non nul.
- Liens déjà présents vers un fichier devenu ignoré : retirés sans code dédié, car `graft` est
  toujours précédé d'`ungraft` et `graft --scion` d'`_unlink` (liens reconnus par leur cible).
- Code de retour et messages des conflits : inchangés.

### E2 — fichiers étrangers du trunk
Deux options (mécanisme générique, aucun nom propre à macOS ni à Lepton dans le code) :
- **A (recommandée) : motifs tolérés déclarés par le rootstock.** Fichier
  `<rootstock>/.scion.trunk.tolerated` (à côté de `.scion.rootstock.signature`), un motif
  `fnmatch` par ligne appliqué au nom du fichier, `#` = commentaire, absent = aucun motif. Créé
  vide (commenté) par `rootstock-install` ; un rootstock existant l'ajoute à la main ou par son
  client. Déterministe, testable, indépendant de la configuration de l'utilisateur et de la
  version de git.
- B : fichier toléré s'il est ignoré par les règles git globales de l'utilisateur
  (`core.excludesFile`), évalué par `git check-ignore --no-index` avec un dépôt temporaire dont
  le trunk est l'arbre de travail. Sans configuration, cohérent avec E1, mais dépend de la
  configuration de chaque poste (la VM n'a pas la règle) et du traitement par git des
  `.gitignore` greffés en liens.

Sort d'un fichier toléré (les deux options) : **supprimé** par `ungraft` (donc par `graft`,
`graft-clean`, `graft-update`) et par `_prune` quand il est seul dans un répertoire à retirer
(`graft --scion`, `graft-remove`) ; il ne bloque jamais. Un fichier régulier non toléré garde le
comportement actuel (refus, `--force` le conserve). Journal : `-v` une ligne par fichier supprimé.
Alternative : laissé en place (ses répertoires restent alors dans le trunk vidé, et un futur lien
au même chemin serait en conflit).

### Commun
- Tests : E1 — fichier ignoré au même chemin dans deux greffons (pas de conflit, non greffé),
  répertoire ignoré, fichier suivi correspondant à une règle (greffé), non suivi non ignoré
  (greffé), source non git (inchangé), exclusion globale (`GIT_CONFIG_GLOBAL` pointé sur une
  configuration de test), `graft --scion` qui retire un lien devenu ignoré ; E2 — fichier toléré
  supprimé sans `--force` par `ungraft`, `graft --scion`, `graft-remove` ; non toléré toujours
  refusé ; `rootstock-install` crée le fichier. Les tests existants ne changent pas.
- `README.md` (§Layout, §Utilisation) et `CHANGELOG.md`.
- Version : **0.5.2.0** (comportement de greffe modifié et nouveau fichier de rootstock ; formats
  existants inchangés). 0.5.1.2 si l'on tient E1/E2 pour des corrections.
- Essai (tâche 3) : scion de la branche dans un venv d'essai
  (`<essais>/env-15/venv`, `pip install <SEED_SCIONS>`), `~/.local/bin/scion` 0.5.1.1 inchangé
  jusqu'au PA-18.
- lepton : inchangé dans l'étape hormis `SCION_MIN_VERSION` et `SCION_REF` (sa purge des
  `.DS_Store` / `._*` avant `scion graft`, PA-9 Q8, reste ; son retrait éventuel est hors étape).

## 3. Décisions PA-17
Réponse de l'utilisateur du 2026-10-30 : les quatre recommandations sont retenues.
- E1 validé tel que proposé au §2 (dépôt englobant le rootstock traité comme non git compris).
- E2 : option A, fichier `<rootstock>/.scion.trunk.tolerated` (motifs `fnmatch` sur le nom),
  créé vide par `rootstock-install`.
- Fichier toléré supprimé au dégreffage (`ungraft`, `_prune`), sans `--force`.
- Version 0.5.2.0 ; essai dans un venv d'essai, `~/.local/bin/scion` inchangé jusqu'au PA-18.

## 4. Implémentation (tâche 2)
`<SEED_SCIONS>` `devenv/env-15` (depuis `master` f1d1f3c) :

| Commit | Contenu | Tests ajoutés |
| --- | --- | --- |
| e21d3cf | E1 : `gitops.toplevel`, `gitops.ignored` (`git ls-files --others --ignored --exclude-standard --directory -z`), `graft._ignored`, `_walk(base, ignored)` ; appliqué dans `_graft_entries` et `remove` ; INFO du nombre d'exclus, DEBUG (`-v`) du détail | `tests/test_ignored.py` (9) |
| 0601792 | E2 : `rootstock.TOLERATED` (`.scion.trunk.tolerated`), écrit sans motif par `rootstock-install` (pas par `--bare`) ; `_check_stray(rootstock, force)` rend les tolérés, supprimés par `ungraft` ; `_drop_tolerated` dans `_prune` ; message de refus qui cite le fichier | `tests/test_tolerated.py` (11) |
| 027d5cd | 0.5.2.0 : `__version__`, `CHANGELOG.md`, `README.md` (filtre, layout, fichier toléré) ; `test_cli` : version attendue 0.5.2.0 (seule modification d'un test existant, mise à jour à chaque version comme en 0.5.1.1) | — |

`python3 -m unittest discover -s tests` : 126 tests, OK (1 ignoré, comme avant) ; 106 avant. Les
tests nouveaux fixent la configuration git globale (`GIT_CONFIG_GLOBAL`) ; sans le filtre, 5 des 9
tests E1 échouent (les 4 autres gardent la non-régression) ; sans les motifs, 7 des 11 tests E2
échouent. `grep -ri lepton scion/` : les 2 lignes de métadonnées seules (PA-2 Q7).

Fusion `--no-ff` dans `master` (472c12e « Fusion de devenv/env-15 (scion 0.5.2.0) »), tag annoté
local `0.5.2.0` « scion 0.5.2.0 » ; rien n'est poussé.

## 5. Essai sur une copie (tâche 3)
Copie `~/lepton-tools-dev/essais/env-15` (`cp -RP ~/lepton`, puis `build/`, `third_party/` et le
`.DS_Store` de la racine retirés ; 120 Mo) ; scion de la branche dans le venv
`~/lepton-tools-dev/essais/env-15-venv` (`pip install <SEED_SCIONS>`, `scion version` 0.5.2.0).
Listes (lien, cible) triées par `rapports/env-15-liste-trunk.sh`, rangées dans
`~/lepton-tools-dev/essais/env-15-mesures/` (non versionnées) ; référence : SHA-256
`449ec204…2504971`, 3929 liens.

| Essai | Action | Résultat |
| --- | --- | --- |
| E0 | `scion graft` (0.5.2.0) sur la copie | 3929 liens, liste identique octet pour octet |
| E1 (défaut) | `.DS_Store` non suivi dans `scion/sys/` du clone noyau et du BSP an386 (ignorés : `.gitignore` du noyau l. 482, `~/.gitignore_global` l. 2) ; `scion graft` 0.5.1.1 | `1 conflit(s) de greffe` sur `sys/.DS_Store` (noyau / BSP an386), trunk laissé vide (0 lien) : défaut du 2026-10-30 reproduit |
| E1 | même état, `scion graft` 0.5.2.0 | code 0, « 2 chemin(s) ignoré(s) par git, non greffé(s) », 3929 liens, liste identique ; `-v` nomme les deux exclus |
| E1 bis | fichier nouveau non suivi `essai_env15.c` dans le BSP an386 ; `scion graft --scion lepton@bsp-qemu-mps2-an386` | code 0, lien créé (3930 liens) |
| E2 (refus) | 2 `.DS_Store` réguliers dans le trunk (`sys/`, `…/bsp/qemu-mps2-an386/`, créés par l'utilisateur : le hook interdit l'écriture à la session) ; pas de `.scion.trunk.tolerated` ; `scion graft` | code 1, les deux fichiers listés, message qui cite `.scion.trunk.tolerated` ; trunk intact |
| E2 | `.scion.trunk.tolerated` = `.DS_Store`, `._*` ; `scion graft` sans `--force` | code 0, les deux fichiers supprimés (`-v`), 3930 liens, 0 fichier régulier, 0 `.DS_Store` |
| Retour | fichiers d'essai retirés des clones (clones propres) ; `scion ungraft` puis `scion graft` (à la place de `graft-update`) | 3929 liens, liste identique à la référence |

## 6. Version, lepton, `<ROOTSTOCK>` (tâche 4)
- `pipx install --force "git+file://<SEED_SCIONS>@0.5.2.0"` : `scion version` 0.5.2.0 ; modules
  installés identiques au tag (`cmp` des 8 modules).
- lepton-tools `devenv/env-15` 1e65851 : `SCION_MIN_VERSION = (0, 5, 2, 0)`,
  `SCION_REF="0.5.2.0"`, `README.md` ; `tests/test_milestone5.py::test_graft_removes_system_files`
  adapté : un `.DS_Store` ignoré par git dans un clone n'est plus greffé (il l'était en 0.1,
  PA-9 Q8 « liens venus des clones conservés ») ; le test fixe ses exclusions globales. Ce test
  échouait avec scion 0.5.2.0 (197/198) : conséquence directe d'E1, signalée au PA-18.
- `pytest` (venv `~/lepton-tools-dev/venv-lepton-tools`, scion 0.5.2.0) : 198 passés (dont le test adapté).
- `pipx install --force <LEPTON_TOOLS>` depuis 1e65851 : `lepton --version` → `scion 0.5.2.0
  (requis ≥ 0.5.2.0)`.
- Regreffe de `<ROOTSTOCK>` (`scion graft`, 0.5.2.0) : 3929 liens, liste identique octet pour
  octet à celle d'avant (même SHA-256), 0 fichier régulier, 0 lien cassé, 8 clones propres.
  L'arbre composé étant identique, aucune reconstruction (oracle) n'a été jugée nécessaire.
- `<ROOTSTOCK>` n'a pas de `.scion.trunk.tolerated` (installé avant 0.5.2.0) : rien n'y est
  toléré ; lepton continue de purger `.DS_Store` et `._*` avant `scion graft`.

### Écart à signaler
La question PA-17 annonçait `~/.local/bin/scion` inchangé jusqu'au PA-18 ; la tâche 4 du fichier
d'étape (et le plan de session accepté) l'installe avant le PA-18. Il a été installé (0.5.2.0) et
`<ROOTSTOCK>` regreffé avec lui avant le PA-18. Retour possible : `pipx install --force
"git+file://<SEED_SCIONS>@0.5.1.1"`.

## 7. Décisions PA-18 (1)
Réponse de l'utilisateur du 2026-10-30 :
- Publication (PA-P) : tag `0.5.2.0` et `master` de `<SEED_SCIONS>`, `devenv/env-15` de
  lepton-tools ; puis ordre `R15-1` à la session VM `lepton-vm-debian`.
- Périmètre Debian : host et les 6 presets QEMU (`consignes/env-15-debian.md` §7).
- Adaptation de `test_graft_removes_system_files` validée : PA-9 Q8 amendé, un fichier ignoré par
  git dans un clone n'est plus greffé.
- scion 0.5.2.0 installé par pipx avant le PA-18 : conservé.

## 8. Validation Debian (R15-1)
| Date | Message | Résumé |
| --- | --- | --- |
| 2026-10-30 | `ORDRE R15-1` | envoyé à `lepton-vm-debian` (Remote Control) par `fix-scion-ignored-graft-files` ; consigne `consignes/env-15-debian.md` (lepton-tools `devenv/env-15` f5e7be8), texte joint tel quel |
| 2026-10-30 | `ACCUSÉ R15-1` | reçu de `lepton-vm-debian` : §5 conforme (Debian 13.7, git 2.47.3, embOS 5.20.0.0 présent, `core.excludesFile` absent ; `devenv/env-15` f5e7be8 ; tag 0.5.2.0 472c12e, graine 0f1275a, noyau 118912a, f4 7694ad5, 6 autres greffons inchangés) ; écart prévu : banc 19/15 au lieu de 18/14 (`net.ping_ftpd` Linux seul, comme R13-1 et R14-1) |
| 2026-10-30 | `AVANCEMENT R15-1` (Mac) | accusé reçu ; banc 19/15 attendu sur Debian, à consigner comme constat |
| 2026-10-30 | `AVANCEMENT R15-1` (VM) | arrêt au §5 : `pipx install` de scion 0.5.2.0 et de lepton refusé par les permissions de la session VM, rien installé ni lancé ; attend l'utilisateur |
| 2026-10-30 | reprise R15-1 | installations pipx de scion 0.5.2.0 et de lepton faites sur la VM par l'utilisateur ; la VM reprend au §5 |
| 2026-10-30 | `AVANCEMENT R15-1` (VM) | §6 : C3 et C4 conformes (3929 liens, 0 cassé, 0 régulier ; « 2 chemin(s) ignoré(s) par git », listes avant / E1 / après identiques, sha256 9e16ec37…) ; côté noyau, `.DS_Store` déjà ignoré par le `.gitignore` du clone (ligne 482) ; C2 non lancé : clonage et tests de scion refusés par les permissions de la session VM, demandés à l'utilisateur ; listes produites par `find -printf` (équivalence vérifiée) ; §7 lancé |
| 2026-10-30 | `AVANCEMENT R15-1` (VM) | C2 conforme (tests lancés par l'utilisateur : 126 tests, OK (skipped=1), code 0) ; §7-§8 : `rejouer-oracle` code 0 (host ctest 7/7, 6/6 presets QEMU, banc 19/19 hard et 15/15 soft, `smoke.lsh` réussi), `comparer-oracle` code 0 contre `env-14-debian` partout, empreintes mklepton et symboles identiques (1599, 1596, 1639, 1638, 1561, 1601) ; trunk : 0 lien cassé, 0 fichier régulier ; suite : rapport, commit, question de push |
| 2026-10-30 | `FIN-SUCCÈS R15-1` | C1 à C8 conformes ; `devenv/env-15-debian` fe4905f (depuis f5e7be8, 47 fichiers, tous sous `rapports/`) poussée par la VM avec l'accord de l'utilisateur ; rapport `rapports/env-15-debian.md`, captures `rapports/oracles/env-15-debian/` ; vérifiés côté Mac, fusionnés dans `devenv/env-15` (0d3e38f) |

## 9. Clôture (PA-18 (2))

- `devenv/env-15-debian` fe4905f vérifiée (parent f5e7be8 ; 47 fichiers ajoutés, tous sous
  `rapports/`) et fusionnée dans `devenv/env-15` (0d3e38f) ; `devenv/env-15` fusionnée dans `main`
  et poussée (décision PA-18 (2)).
- Écart relevé en fin de session : le clone noyau gardait scion 0.5.1.1 par défaut
  (`scripts/install-{macos,debian}.sh` `SCION_REF`, `doc/BUILDING.md`, `README-PAQUET.md`), alors
  que lepton exige ≥ 0.5.2.0. Aligné avec l'accord de l'utilisateur, comme en ENV-7 R1 : clone
  noyau `devenv/env-15` 0ad8a03 (depuis `master` 118912a), fusionnée dans `master` 6f1801d ;
  `master` et la branche poussés. Ces fichiers sont hors du trunk : aucune regreffe ; trunk de
  `<ROOTSTOCK>` : 0 fichier régulier, 0 lien cassé. Non validé sur Debian (la VM a installé
  scion par la commande de la consigne, sans ces scripts).
