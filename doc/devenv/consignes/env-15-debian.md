# Consigne — session Claude Code sur la VM Debian — ENV-15 (scion 0.5.2.0)

Fichier autonome : il suffit, avec `ORCHESTRATION.md` §2bis, à conduire la session VM. Rédigé le
2026-10-30 par la session Mac `fix-scion-ignored-graft-files` (tâche 5 d'ENV-15), repris de
`consignes/env-14-debian.md` ; son texte est envoyé tel quel dans l'ordre `R15-1`.

## 1. Objet

Vérifier sur Debian x86_64 scion 0.5.2.0 : fichiers ignorés par git non greffés (E1), fichiers
tolérés du trunk (E2, par les tests de scion), greffe d'un rootstock neuf inchangée, constructions
inchangées par rapport à R14-1.

- scion : tag `0.5.2.0` de `https://github.com/lepton-distribution/seed.scions.git` (commit
  472c12e, poussé par la session Mac, PA-18).
- lepton-tools : branche `devenv/env-15` (cette consigne ; `SCION_MIN_VERSION = (0, 5, 2, 0)`).
- Graine `https://github.com/lepton-distribution/lepton-seed.scions.git`, branche `original-tree`
  (0f1275a), inchangée ; greffons `master` (noyau 118912a, `family-stm32f4xx` 7694ad5, autres
  inchangés depuis R14-1).

Référence Mac (`doc/devenv/rapports/env-15-scion.md`) : 126 tests de scion verts ; trunk de
`~/lepton` identique avant et après 0.5.2.0 (3929 liens) ; `.DS_Store` ignoré au même chemin dans
deux clones : conflit en 0.5.1.1, greffe sans conflit en 0.5.2.0.
Référence Debian : `doc/devenv/rapports/env-14-debian.md` et `oracles/env-14-debian/`.

La session VM ne développe pas : elle exécute, constate et rapporte. Pas de carte sur la VM. Aucune
commande `sudo` n'est prévue. La configuration git de l'utilisateur de la VM n'est pas modifiée :
la règle d'exclusion de l'essai passe par `GIT_CONFIG_GLOBAL`, pour les seules commandes du §6.

## 2. Ce que la session VM peut faire, et ne fait pas

| Autorisé | Interdit |
| --- | --- |
| `git fetch` / `switch` de `~/lepton-tools-dev/lepton-tools` (`devenv/env-15`) | Modifier `DEVENV-STATUS.md`, `ORCHESTRATION.md`, `SPECIFICATION.md`, `handoff/*.md` |
| `pipx install --force` de scion (tag 0.5.2.0) et de lepton (`devenv/env-15`) | Modifier `~/.gitconfig` ou les exclusions globales de la VM |
| Cloner seed.scions au tag 0.5.2.0 dans `~/env-15-journaux/` et y lancer ses tests | Toucher aux rootstocks existants (`essais/env-14-debian`, `essais/env-13-debian`, …) |
| Créer `~/lepton-tools-dev/essais/env-15-debian` (rootstock neuf) et y tout faire, dont créer puis retirer les `.DS_Store` d'essai **dans les clones** (§6) | Écrire un fichier régulier dans `trunk/` ; corriger quoi que ce soit (consigner l'écart pour la session Mac) |
| Créer `devenv/env-15-debian` (depuis `devenv/env-15`) dans lepton-tools ; y écrire `doc/devenv/rapports/env-15-debian.md` et `doc/devenv/rapports/oracles/env-15-debian/` | Commiter sur une autre branche |
| `git push origin devenv/env-15-debian` **après accord explicite de l'utilisateur** (PA-P) | Pousser toute autre branche ; tout `scion seed-update` / `graft-update` |

Tout écart au plan, toute erreur non prévue : s'arrêter, exposer, attendre l'utilisateur.

## 3. Communication (ORCHESTRATION §2bis)

- Session principale : `fix-scion-ignored-graft-files` (session Mac) ; répondre à l'adresse
  `from` du message d'ordre.
- ID : `R15-1`, repris tel quel (`[ACCUSÉ R15-1] ENV-15 — …`, `[AVANCEMENT R15-1] …`,
  `[QUESTION R15-1] …`, `[FIN-SUCCÈS R15-1] …` ou `[FIN-ÉCHEC R15-1] …`).
- `ACCUSÉ` avant toute commande : ordre reformulé en une phrase, tête réelle de `devenv/env-15` de
  lepton-tools après `fetch`, résultat de `git ls-remote` du §5, étapes prévues (§5 à §8), écarts
  déjà visibles.
- `AVANCEMENT` : après §6 (tests de scion, greffe, essai E1), après §7 (constructions), et à
  chaque arrêt.
- `FIN-SUCCÈS` / `FIN-ÉCHEC` : résultat par critère du §9, commits et branche (poussée ou non),
  chemin du rapport, versions relevées, écarts, ce qui n'a pas été fait.

## 4. Journaux et variables

```bash
mkdir -p ~/env-15-journaux
J=~/env-15-journaux
T=~/lepton-tools-dev/lepton-tools
R=~/lepton-tools-dev/essais/env-15-debian
G=https://github.com/lepton-distribution
```
Une commande par journal `$J/<étape>.log`, code de retour en dernière ligne.

## 5. Vérifications préalables et installation

```bash
uname -sm; cat /etc/debian_version; id -un; git --version
scion version | tail -1; lepton --version
arm-none-eabi-gcc --version | head -1; cmake --version | head -1; ninja --version
qemu-system-arm --version | head -1; python3 --version
echo "LEPTON_EMBOS_ROOT=${LEPTON_EMBOS_ROOT:-absente}"; ls -d ~/lepton/third_party/embos/cortexm-gcc/5.20.0.0 2>&1
git config --global --get core.excludesFile || echo "core.excludesFile absent"
df -h ~ /tmp | tail -2
test -e "$R" && echo "ARRÊT : $R existe déjà"
git -C "$T" status --short | head -5
git -C "$T" fetch origin && git -C "$T" switch devenv/env-15 && git -C "$T" log --oneline -1
echo "scion tag $(git ls-remote $G/seed.scions.git 'refs/tags/0.5.2.0^{}' | cut -c1-7)"
echo "graine $(git ls-remote $G/lepton-seed.scions.git original-tree | cut -c1-7)"
echo "noyau master $(git ls-remote $G/lepton-original-tree.scions.git master | cut -c1-7)"
echo "f4 master $(git ls-remote $G/lepton-famille-stm32f4xx.git master | cut -c1-7)"

pipx install --force "git+$G/seed.scions.git@0.5.2.0" > "$J/5-scion.log" 2>&1; echo "code=$?" >> "$J/5-scion.log"
pipx install --force "$T" > "$J/5-lepton.log" 2>&1; echo "code=$?" >> "$J/5-lepton.log"
scion version | tail -1; lepton --version
```
Attendu : tag 472c12e, graine 0f1275a, noyau 118912a, f4 7694ad5 ; `scion version: 0.5.2.0` ;
`lepton --version` → `scion 0.5.2.0 (requis ≥ 0.5.2.0)`.
Arrêts : `$R` existe ; lepton-tools non propre ; un commit diffère ; installation en échec ; moins
de 3 Go libres dans `~`. embOS absent : pas un arrêt ; les presets `*-embos*` seront en échec
attendu, à consigner.

## 6. Tests de scion, rootstock neuf, essai E1

```bash
git clone -q --branch 0.5.2.0 $G/seed.scions.git "$J/seed.scions"
(cd "$J/seed.scions" && python3 -m unittest discover -s tests) > "$J/6-tests-scion.log" 2>&1; echo "code=$?" >> "$J/6-tests-scion.log"
tail -4 "$J/6-tests-scion.log"

mkdir "$R" && cd "$R"
scion rootstock-install
cat .scion.trunk.tolerated
scion seed-add --version original-tree $G/lepton-seed.scions.git
scion graft
find trunk -type l -exec sh -c 'for l; do printf "%s\t%s\n" "$l" "$(readlink "$l")"; done' _ {} + | LC_ALL=C sort > "$J/6-trunk-avant.tsv"
echo "initial : liens $(find trunk -type l | wc -l) cassés $(find -L trunk -type l | wc -l) réguliers $(find trunk -type f ! -name .scion.grafted.list | wc -l)"

# essai E1 : .DS_Store au même chemin dans deux clones, ignorés par une règle globale de test
printf '.DS_Store\n' > "$J/excludes"; printf '[core]\n\texcludesFile = %s\n' "$J/excludes" > "$J/gitconfig"
K=depots/lepton/original/master; B=depots/lepton/bsp-qemu-mps2-an386/master
printf 'essai\n' > $K/scion/sys/.DS_Store; printf 'essai\n' > $B/scion/sys/.DS_Store
GIT_CONFIG_GLOBAL="$J/gitconfig" git -C $B check-ignore -v scion/sys/.DS_Store
GIT_CONFIG_GLOBAL="$J/gitconfig" scion graft -v > "$J/6-graft-e1.log" 2>&1; echo "code=$?" >> "$J/6-graft-e1.log"
grep -v "^git " "$J/6-graft-e1.log"
find trunk -type l -exec sh -c 'for l; do printf "%s\t%s\n" "$l" "$(readlink "$l")"; done' _ {} + | LC_ALL=C sort > "$J/6-trunk-e1.tsv"
cmp "$J/6-trunk-avant.tsv" "$J/6-trunk-e1.tsv" && echo "E1 : trunk identique"
rm $K/scion/sys/.DS_Store $B/scion/sys/.DS_Store
git -C $K status --short; git -C $B status --short
scion graft
find trunk -type l -exec sh -c 'for l; do printf "%s\t%s\n" "$l" "$(readlink "$l")"; done' _ {} + | LC_ALL=C sort > "$J/6-trunk-apres.tsv"
cmp "$J/6-trunk-avant.tsv" "$J/6-trunk-apres.tsv" && echo "retour : trunk identique"
sha256sum "$J"/6-trunk-*.tsv
```
Attendu : tests de scion `OK` (126, 1 ignoré) ; `.scion.trunk.tolerated` présent, commentaires
seuls ; greffe initiale 9 entrées, 3929 liens, 0 cassé, 0 fichier régulier ; `check-ignore` cite
`$J/excludes` ; `scion graft -v` code 0, « 2 chemin(s) ignoré(s) par git, non greffé(s) », lignes
`exclu (ignoré par git)` pour `lepton/original::tree` et `lepton/bsp-qemu-mps2-an386` ; trois
listes identiques ; clones propres après retrait.
Pour mémoire : avec scion 0.5.1.1, le même essai échoue par un conflit sur `sys/.DS_Store` et
laisse le trunk vide (constat Mac) ; il n'est pas rejoué ici.

## 7. Reconstructions

Périmètre fixé au PA-18 (décision de l'utilisateur du 2026-10-30) : host et les 6 presets QEMU
(l'arbre composé est identique à R14-1 ; les presets de carte ne sont pas reconstruits).

```bash
cd "$T" && git switch -c devenv/env-15-debian devenv/env-15
scripts/oracle/rejouer-oracle.sh "$R" doc/devenv/rapports/oracles/env-15-debian \
  --qemu qemu-mps2-an386-embos --qemu qemu-mps2-an386-embos-soft \
  --qemu qemu-mps2-an386-freertos --qemu qemu-mps2-an386-freertos-soft \
  --qemu qemu-mps2-an500-embos --qemu qemu-mps2-an500-freertos > "$J/7-rejouer.log" 2>&1; echo "code=$?" >> "$J/7-rejouer.log"
tail -20 "$J/7-rejouer.log"
grep -h "tests passed" doc/devenv/rapports/oracles/env-15-debian/*/ctest.log doc/devenv/rapports/oracles/env-15-debian/*/banc-kal.log
find -L "$R/trunk" -type l | wc -l; find "$R/trunk" -type f ! -name .scion.grafted.list | wc -l
```
Attendu : host ctest 7/7 ; chaque preset construit ; banc KAL 18/18 (hard) et 14/14 (soft),
fumée comprise, sur les presets QEMU ; trunk sans fichier régulier ni lien cassé.

## 8. Comparaisons

Avec R14-1 (même chaîne Debian, même arbre) — **c'est la non-régression** : attendu `comparer=0`
et empreintes mklepton identiques. Les empreintes binaires diffèrent par la date de construction
embarquée (E1 de l'oracle, démontrée au Mac) : ce n'est pas un échec.

```bash
cd "$T"; O=doc/devenv/rapports/oracles
diff -q $O/env-14-debian/host/mklepton-empreintes.sha256 $O/env-15-debian/host/mklepton-empreintes.sha256 && echo "mklepton R14-1 identiques"
for p in $(ls $O/env-15-debian | grep -v host); do
  python3 scripts/oracle/comparer-oracle.py $O/env-14-debian/$p $O/env-15-debian/$p > /dev/null 2>&1
  echo "$p comparer_R14-1=$?"
done
```
Un `comparer_R14-1` différent de 0 : relever la sortie complète de `comparer-oracle.py` dans le
rapport ; c'est un écart à exposer, pas à corriger.

## 9. Critères et rapport

| Critère | Attendu |
| --- | --- |
| C1 Dépôts publiés et installation | `git ls-remote` conforme au §5 ; `scion version` 0.5.2.0 ; lepton accepte la version |
| C2 Tests de scion | `python3 -m unittest discover -s tests` au tag 0.5.2.0 : OK (126, 1 ignoré) |
| C3 Rootstock neuf | `.scion.trunk.tolerated` sans motif ; 9 entrées, 3929 liens, 0 cassé, 0 fichier régulier |
| C4 E1 | `.DS_Store` ignoré au même chemin dans deux clones : `scion graft` code 0 sans conflit, non greffés, trunk identique ; identique après retrait |
| C5 host | ctest 7/7, `mklepton-empreintes.sha256` identique à R14-1 |
| C6 Presets QEMU (6) | construits ; banc KAL 18/18 ou 14/14 et fumée réussis (embOS : échec attendu seulement si embOS absent, consigné) |
| C7 Non-régression Debian | `comparer-oracle` code 0 contre `env-14-debian` sur chaque preset construit |
| C8 Trunk après construction | 0 fichier régulier, 0 lien cassé |

Rapport `doc/devenv/rapports/env-15-debian.md` sur `devenv/env-15-debian`, contenant : hôte et
versions (§5), table des critères, table des presets (construction, fumée, banc KAL,
comparaisons), écarts. Commit du rapport et de `oracles/env-15-debian/`, puis `QUESTION` à
l'utilisateur pour le push (PA-P), puis `FIN-*`. Le rootstock `$R` est conservé.
