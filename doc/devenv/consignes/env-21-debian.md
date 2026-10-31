# Consigne — session Claude Code sur la VM Debian — ENV-21 (validation Debian groupée)

Fichier autonome : il suffit, avec `ORCHESTRATION.md` §2bis, à conduire la session VM. Rédigé le
2026-10-31 par la session Mac `validation-debian-groupee-env21` (tâche 1 d'ENV-21), repris de
`consignes/env-15-debian.md` et `consignes/env-14-debian.md` ; son texte est envoyé tel quel dans
l'ordre `R21-1`.

## 1. Objet

Valider sur Debian x86_64 l'état publié après ENV-17 à ENV-20 : lepton réinstallé, scripts
d'installation du noyau avec le défaut `SCION_REF` (scion 0.5.2.0), rootstock neuf depuis la
graine publiée (12 greffons famille/BSP, dont les 5 d'ENV-19 et ENV-20), constructions de host et
des 16 presets croisés, graine de référence lue par lepton (ENV-18), graine de projet existante.

Références publiées (toutes poussées, aucune fusion différée) :

| Dépôt (`https://github.com/lepton-distribution/…`) | Référence | Commit |
| --- | --- | --- |
| `lepton-tools` | `devenv/env-21` (cette consigne ; code Python identique à `main` 84cb75f) | tête après `fetch` |
| `seed.scions` | tag `0.5.2.0` | 472c12e |
| `lepton-seed.scions` | `original-tree` | 15740f9 |
| `lepton-original-tree.scions` (noyau) | `master` | 40d7197 |
| `lepton-famille-qemu-mps2` | `master` | 3954357 |
| `lepton-bsp-qemu-mps2-an386` | `master` | 046779e |
| `lepton-bsp-qemu-mps2-an500` | `master` | e98a482 |
| `lepton-famille-stm32f4xx` | `master` | 2b21340 |
| `lepton-bsp-nucleo-f429zi` | `master` | 8ea7ee5 |
| `lepton-bsp-nucleo-f439zi` (nouveau, ENV-20) | `master` | f866283 |
| `lepton-famille-stm32wlxx` | `master` | 1eccc2f |
| `lepton-bsp-nucleo-wl55jc1` | `master` | a329f4d |
| `lepton-famille-stm32f7xx` (nouveau, ENV-19) | `master` | 34ccaf8 |
| `lepton-bsp-stm32f746g-disco` (nouveau, ENV-19) | `master` | 9f81c1b |
| `lepton-famille-samd21` (nouveau, ENV-19) | `master` | a389592 |
| `lepton-bsp-samd21-xplained-pro` (nouveau, ENV-19) | `master` | 46337d1 |

Référence Mac : oracle `doc/devenv/rapports/oracles/env-20-apres/` (host + 16 presets ; rapports
`rapports/env-19-extraction.md` §7, `rapports/env-20-bsp.md` §7). Trunk de `~/lepton` au Mac :
14 entrées greffées, 3941 liens, 0 cassé, 0 fichier régulier.
Référence Debian : `rapports/env-14-debian.md` et `oracles/env-14-debian/` (host + 14 presets,
dernier oracle Debian complet) ; `rapports/env-15-debian.md` (R15-1).

La session VM ne développe pas : elle exécute, constate et rapporte. Pas de carte sur la VM : les
presets de carte sont construits, jamais flashés.

## 2. Ce que la session VM peut faire, et ne fait pas

| Autorisé | Interdit |
| --- | --- |
| `git fetch` / `switch` de `~/lepton-tools-dev/lepton-tools` (`devenv/env-21`) | Modifier `DEVENV-STATUS.md`, `ORCHESTRATION.md`, `SPECIFICATION.md`, `handoff/*.md`, les consignes |
| `git fetch` puis `switch master` + `merge --ff-only origin/master` du clone noyau `~/lepton-tools-dev/lepton-noyau` (lecture de `scripts/install-debian.sh` à 40d7197) | Toute autre écriture dans ce clone |
| `pipx install --force` de lepton (`devenv/env-21`) ; scripts d'installation lancés **par l'utilisateur** (§6, sudo) | Lancer soi-même une commande `sudo` |
| Créer `~/lepton-tools-dev/essais/env-21-debian` (rootstock neuf) et y tout faire | Écrire un fichier régulier dans un `trunk/` ; corriger quoi que ce soit (consigner l'écart pour la session Mac) |
| Dans `~/lepton-tools-dev/essais/env-11/qemu` : `lepton check`, `lepton generate`, `git status` de la graine `env11` | Regreffer `env-11/qemu`, commiter dans sa graine, toucher aux autres rootstocks (`essais/env-13-debian`, `env-14-debian`, …) |
| Créer `devenv/env-21-debian` (depuis `devenv/env-21`) dans lepton-tools ; y écrire `doc/devenv/rapports/env-21-debian.md` et `doc/devenv/rapports/oracles/env-21-debian/` | Commiter sur une autre branche |
| Supprimer `~/lepton-tools-dev/essais/env-15-debian` et `~/env-15-journaux/` (§10, C7) **si l'ordre le dit** | Supprimer quoi que ce soit d'autre |
| `git push origin devenv/env-21-debian` **après accord explicite de l'utilisateur** (PA-P) | Pousser toute autre branche ; tout `scion seed-update` / `graft-update` |

Tout écart au plan, toute erreur non prévue : s'arrêter, exposer (`AVANCEMENT` ou `QUESTION`),
attendre.

## 3. Communication (ORCHESTRATION §2bis)

- Session principale : `validation-debian-groupee-env21` (session Mac) ; répondre à l'adresse
  `from` du message d'ordre.
- ID : `R21-1`, repris tel quel (`[ACCUSÉ R21-1] ENV-21 — …`, `[AVANCEMENT R21-1] …`,
  `[QUESTION R21-1] …`, `[FIN-SUCCÈS R21-1] …` ou `[FIN-ÉCHEC R21-1] …`).
- `ACCUSÉ` avant toute commande autre que les lectures du §5 : ordre reformulé en une phrase, tête
  réelle de `devenv/env-21` après `fetch`, résultats de `git ls-remote` du §5, étapes prévues
  (§6 à §10), écarts déjà visibles.
- `AVANCEMENT` : quand l'utilisateur doit lancer les scripts (§6.2), après §6, après §7, après §8
  (constructions), après §9, et à chaque arrêt.
- `FIN-SUCCÈS` / `FIN-ÉCHEC` : résultat par critère du §11, commits et branche (poussée ou non),
  chemin du rapport, versions relevées, écarts, ce qui n'a pas été fait.

## 4. Journaux et variables

```bash
mkdir -p ~/env-21-journaux
J=~/env-21-journaux
T=~/lepton-tools-dev/lepton-tools
K=~/lepton-tools-dev/lepton-noyau
R=~/lepton-tools-dev/essais/env-21-debian
P=~/lepton-tools-dev/essais/env-11/qemu
G=https://github.com/lepton-distribution
```
Une commande par journal `$J/<étape>.log`, code de retour en dernière ligne (`code=<n>`).

## 5. Vérifications préalables

```bash
uname -sm; cat /etc/debian_version; id -un; git --version
scion version | tail -1; lepton --version
arm-none-eabi-gcc --version | head -1; cmake --version | head -1; ninja --version
qemu-system-arm --version | head -1; python3 --version
echo "LEPTON_EMBOS_ROOT=${LEPTON_EMBOS_ROOT:-absente}"; ls -d ~/lepton/third_party/embos/cortexm-gcc/5.20.0.0 2>&1
df -h ~ /tmp | tail -2
test -e "$R" && echo "ARRÊT : $R existe déjà"
git -C "$T" status --short | head -5; git -C "$K" status --short | head -5; git -C "$K" branch --show-current
git -C "$T" fetch origin && git -C "$T" switch devenv/env-21 && git -C "$T" merge --ff-only origin/devenv/env-21 && git -C "$T" log --oneline -1
echo "scion tag $(git ls-remote $G/seed.scions.git 'refs/tags/0.5.2.0^{}' | cut -c1-7)"
echo "graine $(git ls-remote $G/lepton-seed.scions.git original-tree | cut -c1-7)"
for r in lepton-original-tree.scions lepton-famille-qemu-mps2 lepton-bsp-qemu-mps2-an386 \
         lepton-bsp-qemu-mps2-an500 lepton-famille-stm32f4xx lepton-bsp-nucleo-f429zi \
         lepton-bsp-nucleo-f439zi lepton-famille-stm32wlxx lepton-bsp-nucleo-wl55jc1 \
         lepton-famille-stm32f7xx lepton-bsp-stm32f746g-disco lepton-famille-samd21 \
         lepton-bsp-samd21-xplained-pro; do
  echo "$r $(git ls-remote $G/$r.git refs/heads/master | cut -c1-7)"
done
```
Attendu : commits du tableau du §1. Arrêts : `$R` existe ; lepton-tools ou clone noyau non
propre ; un commit diffère ; moins de 4 Go libres dans `~`. embOS absent : pas un arrêt ; les
presets `*-embos*` seront en échec attendu, à consigner.

## 6. Installation (C1, C2)

### 6.1 Relevé de la graine de projet avant réinstallation (pour C6)

```bash
lepton check -C "$P" > "$J/6.1-check-P-avant.log" 2>&1; echo "code=$?" >> "$J/6.1-check-P-avant.log"
git -C "$P"/depots/lepton-seed/env11 status --short > "$J/6.1-graine-P-avant.txt"
sha256sum "$P"/depots/lepton-seed/env11/project/scion/CMakeUserPresets.json "$P"/*.code-workspace > "$J/6.1-generes-P-avant.sha256"
```
Si `depots/lepton-seed/env11` n'est pas la graine de `$P` : consigner le chemin réel et l'utiliser.

### 6.2 lepton (C1), puis scripts d'installation (C2) — lancés par l'utilisateur

```bash
pipx install --force "$T" > "$J/6.2-lepton.log" 2>&1; echo "code=$?" >> "$J/6.2-lepton.log"
lepton --version
git -C "$K" fetch origin && git -C "$K" switch master && git -C "$K" merge --ff-only origin/master && git -C "$K" log --oneline -1
grep -n '^SCION_REF=' "$K/scripts/install-debian.sh"
```
Attendu : code 0 ; `lepton 0.1.0`, `scion 0.5.2.0 (requis ≥ 0.5.2.0)` ; clone noyau à 40d7197 ;
`SCION_REF="${SCION_REF:-0.5.2.0}"`.

Puis `AVANCEMENT` : l'**utilisateur** lance, dans un terminal de la VM (sudo avec mot de passe),
**sans** `SCION_REF` dans l'environnement (défaut du noyau) :

```bash
J=~/env-21-journaux; K=~/lepton-tools-dev/lepton-noyau; T=~/lepton-tools-dev/lepton-tools
unset SCION_REF SCION_SPEC
bash "$K/scripts/install-debian.sh" --with-debug-tools 2>&1 | tee "$J/6.2-install-debian.log"; echo "code=${PIPESTATUS[0]}" | tee -a "$J/6.2-install-debian.log"
bash "$T/scripts/install-vscodium.sh" --lepton-clone "$K" 2>&1 | tee "$J/6.2-install-vscodium-1.log"; echo "code=${PIPESTATUS[0]}" | tee -a "$J/6.2-install-vscodium-1.log"
bash "$T/scripts/install-vscodium.sh" --lepton-clone "$K" 2>&1 | tee "$J/6.2-install-vscodium-2.log"; echo "code=${PIPESTATUS[0]}" | tee -a "$J/6.2-install-vscodium-2.log"
```
La session VM lit ensuite les journaux. Attendu : trois codes 0 ; `install-debian.sh` : scion
0.5.2.0 « déjà installé » ou installé depuis `$G/seed.scions.git@0.5.2.0` ; seconde exécution
d'`install-vscodium.sh` : **`changements 0`**. Puis :
```bash
scion version | tail -1; lepton --version; codium --version | head -1
dpkg-query -W -f '${Version}\n' codium; codium --list-extensions --show-versions | LC_ALL=C sort > "$J/6.2-extensions.txt"
```

## 7. Rootstock neuf depuis la graine publiée (C3)

```bash
mkdir "$R" && cd "$R"
scion rootstock-install > "$J/7-rootstock-install.log" 2>&1; echo "code=$?" >> "$J/7-rootstock-install.log"
scion seed-add --version original-tree $G/lepton-seed.scions.git > "$J/7-seed-add.log" 2>&1; echo "code=$?" >> "$J/7-seed-add.log"
scion graft > "$J/7-graft.log" 2>&1; echo "code=$?" >> "$J/7-graft.log"
grep -v '^#' trunk/.scion.grafted.list | grep -c .
for d in depots/lepton/*/master; do echo "$d $(git -C $d rev-parse --short HEAD)"; done
find trunk -type l -exec sh -c 'for l; do printf "%s\t%s\n" "$l" "$(readlink "$l")"; done' _ {} + | LC_ALL=C sort > "$J/7-trunk.tsv"
echo "liens $(find trunk -type l | wc -l) cassés $(find -L trunk -type l | wc -l) réguliers $(find trunk -type f ! -name .scion.grafted.list | wc -l) DS_Store $(find trunk -name .DS_Store | wc -l)"
```
Attendu : codes 0 ; 14 entrées greffées (`original::tree`, `building`, 12 famille/BSP) ; chaque
clone au commit du §1 ; 3941 liens, 0 cassé, 0 fichier régulier, 0 `.DS_Store`. Un nombre de
liens différent de 3941 : relever `comm` contre la liste des fichiers suivis des clones, l'exposer.

## 8. Reconstructions et comparaisons (C4)

Périmètre : host et les 16 presets croisés (QEMU : construction, fumée, banc KAL ; cartes :
construction et capture seulement).

```bash
cd "$T" && git switch -c devenv/env-21-debian devenv/env-21
scripts/oracle/rejouer-oracle.sh "$R" doc/devenv/rapports/oracles/env-21-debian \
  --qemu qemu-mps2-an386-embos --qemu qemu-mps2-an386-embos-soft \
  --qemu qemu-mps2-an386-freertos --qemu qemu-mps2-an386-freertos-soft \
  --qemu qemu-mps2-an500-embos --qemu qemu-mps2-an500-freertos \
  --carte nucleo-f429zi-embos --carte nucleo-f429zi-freertos \
  --carte nucleo-f439zi-embos --carte nucleo-f439zi-freertos \
  --carte nucleo-wl55jc1-embos --carte nucleo-wl55jc1-freertos \
  --carte samd21-xplained-pro-embos --carte samd21-xplained-pro-freertos \
  --carte stm32f746g-disco-embos --carte stm32f746g-disco-freertos > "$J/8-rejouer.log" 2>&1; echo "code=$?" >> "$J/8-rejouer.log"
tail -25 "$J/8-rejouer.log"
grep -h "tests passed" doc/devenv/rapports/oracles/env-21-debian/*/ctest.log doc/devenv/rapports/oracles/env-21-debian/*/banc-kal.log
find -L "$R/trunk" -type l | wc -l; find "$R/trunk" -type f ! -name .scion.grafted.list | wc -l
```
Attendu : code 0 ; host ctest 7/7 ; 16 presets construits ; banc QEMU 19/19 (hard) et 15/15
(soft) sous Debian (`net.ping_ftpd`, Linux seul, en plus des 18 et 14 du Mac), fumée réussie ;
trunk sans fichier régulier ni lien cassé.

Comparaisons. L'arbre a changé depuis R14-1 : la non-régression Debian se lit **par rapport aux
écarts déjà constatés au Mac** entre `env-14-apres` et `env-20-apres`.

```bash
cd "$T"; O=doc/devenv/rapports/oracles
diff -q $O/env-20-apres/host/mklepton-empreintes.sha256 $O/env-21-debian/host/mklepton-empreintes.sha256 && echo "mklepton = Mac env-20-apres"
for p in $(ls $O/env-21-debian | grep -v -e host -e '\.log$'); do
  a=—; [ -d $O/env-14-debian/$p ] && { python3 scripts/oracle/comparer-oracle.py $O/env-14-debian/$p $O/env-21-debian/$p > "$J/8-cmp-R14-$p.txt" 2>&1; a=$?; }
  python3 scripts/oracle/comparer-oracle.py $O/env-20-apres/$p $O/env-21-debian/$p > "$J/8-cmp-Mac-$p.txt" 2>&1; b=$?
  echo "$p comparer_R14-1=$a comparer_Mac=$b symboles=$(wc -l < $O/env-21-debian/$p/symboles.txt)"
done
for s in embos freertos; do
  python3 scripts/oracle/comparer-oracle.py $O/env-21-debian/nucleo-f429zi-$s $O/env-21-debian/nucleo-f439zi-$s > /dev/null 2>&1; echo "f429→f439 $s=$?"
done
```

Attendu (valeurs Mac `env-14-apres` → `env-20-apres`, à retrouver sous Debian `env-14-debian` →
`env-21-debian`) :

| Preset | `comparer_R14-1` attendu | Cause (rapports Mac) |
| --- | --- | --- |
| `qemu-mps2-an386-*` (4), `qemu-mps2-an500-*` (2) | 0 | — |
| `nucleo-wl55jc1-*` (2), `samd21-xplained-pro-embos` | 0 | — |
| `nucleo-f429zi-*` (2) | 1 | table de vecteurs F4 complète (`env-20-bsp.md` E-1) |
| `stm32f746g-disco-*` (2), `samd21-xplained-pro-freertos` | 1 | extraction en greffons : ordre d'édition de liens, sections (`env-19-extraction.md` E-2, E-3) |
| `nucleo-f439zi-*` (2) | — (nouveaux) | `f429→f439` attendu 0 (`env-20-bsp.md` E-2) |

`comparer_Mac` : informatif (chaînes différentes ; 1 attendu partout, comme en R14-1).
Mklepton : empreintes identiques à `env-20-apres` (50 lignes ; R14-1 était identique au Mac).
Pour chaque `comparer_R14-1` à 1 : relever dans le rapport les sections et le nombre de symboles
qui diffèrent (extrait de `$J/8-cmp-R14-<preset>.txt`) et dire s'ils sont de même nature que
l'écart Mac. Un code différent de l'attendu : écart à exposer, pas à corriger.

## 9. lepton sur la graine de référence et sur la graine de projet (C5, C6)

```bash
lepton check -C "$R" > "$J/9-check-R.log" 2>&1; echo "code=$?" >> "$J/9-check-R.log"
lepton seed status -C "$R" > "$J/9-status-R.log" 2>&1; echo "code=$?" >> "$J/9-status-R.log"
lepton seed tree -C "$R" > "$J/9-tree-R.log" 2>&1; echo "code=$?" >> "$J/9-tree-R.log"
lepton generate -C "$R" > "$J/9-generate-R.log" 2>&1; echo "code=$?" >> "$J/9-generate-R.log"
lepton seed add -C "$R" --type bsp x /inexistant-env21 2>&1 | tail -2; echo "code=${PIPESTATUS[0]}"   # refus attendu (ENV-18)
git -C "$R"/depots/lepton-seed.scions/original-tree status --short
grep -c '"request"' "$R"/original-tree.code-workspace; find "$R/trunk" -type f ! -name .scion.grafted.list | wc -l

lepton check -C "$P" > "$J/9-check-P-apres.log" 2>&1; echo "code=$?" >> "$J/9-check-P-apres.log"
lepton generate -C "$P" > "$J/9-generate-P.log" 2>&1; echo "code=$?" >> "$J/9-generate-P.log"
git -C "$P"/depots/lepton-seed/env11 status --short > "$J/9-graine-P-apres.txt"
sha256sum "$P"/depots/lepton-seed/env11/project/scion/CMakeUserPresets.json "$P"/*.code-workspace > "$J/9-generes-P-apres.sha256"
diff "$J/6.1-generes-P-avant.sha256" "$J/9-generes-P-apres.sha256" && echo "générés P identiques"
diff "$J/6.1-graine-P-avant.txt" "$J/9-graine-P-apres.txt" && echo "graine P inchangée"
diff <(grep -v '^code=' "$J/6.1-check-P-avant.log") <(grep -v '^code=' "$J/9-check-P-apres.log") && echo "check P identique"
```
Attendu : sur `$R` : `check`, `seed status`, `seed tree`, `generate` code 0 ; `seed status`
affiche « graine de référence (ni lepton-graine.json ni project/) » ; `generate` écrit
`$R/original-tree.code-workspace` (16 `"request"` au Mac) et rien dans le trunk ; `seed add`
refusé, code 1, message « graine de référence … : lepton seed add modifie la graine, refusé »,
graine propre. Sur `$P` :
`check` et `generate` code 0, sorties et fichiers générés identiques à §6.1, graine inchangée. Une
différence (nouvelle version de lepton) : la relever telle quelle, l'exposer.

## 10. Nettoyage de la VM (C7)

Seulement si l'ordre `R21-1` l'accorde :
```bash
du -sh ~/lepton-tools-dev/essais/env-15-debian ~/env-15-journaux
rm -rf ~/lepton-tools-dev/essais/env-15-debian ~/env-15-journaux
ls -d ~/lepton-tools-dev/essais/env-15-debian ~/env-15-journaux 2>&1
```
Le rootstock `$R` et `$J` sont conservés.

## 11. Critères et rapport

| Critère | Attendu |
| --- | --- |
| C1 lepton | `git ls-remote` conforme au §1 ; `pipx install --force` code 0 ; `lepton 0.1.0`, scion 0.5.2.0 accepté |
| C2 Scripts d'installation | `install-debian.sh` du noyau (40d7197, défaut `SCION_REF` 0.5.2.0) code 0 ; `install-vscodium.sh` code 0 deux fois, `changements 0` à la seconde ; versions relevées |
| C3 Rootstock neuf | 14 entrées, clones aux commits du §1, 3941 liens, 0 cassé, 0 fichier régulier |
| C4 Constructions | host ctest 7/7, empreintes mklepton = `env-20-apres` ; 16 presets construits ; QEMU fumée et banc 19/19 ou 15/15 ; `comparer_R14-1` conforme au tableau du §8 ; `f429→f439` 0 |
| C5 Graine de référence | `check`, `seed status`, `seed tree`, `generate` code 0 ; `seed add` refusé code 1 ; trunk sans fichier régulier |
| C6 Graine de projet `env11` | `check`, `generate` code 0 ; sorties et fichiers générés identiques avant et après réinstallation |
| C7 Nettoyage | selon l'ordre : `env-15-debian` et `~/env-15-journaux` supprimés (taille relevée), ou « non demandé » |

Rapport `doc/devenv/rapports/env-21-debian.md` sur `devenv/env-21-debian`, contenant : hôte et
versions (§5, §6), table des critères, table des presets (construction, fumée, banc KAL, symboles
R21-1 / R14-1, `comparer_R14-1`, `comparer_Mac`), écarts, journal des messages §2bis (ID, date,
résumé). Commit du rapport et de `oracles/env-21-debian/`, puis `QUESTION` à l'utilisateur pour le
push (PA-P), puis `FIN-*`.
