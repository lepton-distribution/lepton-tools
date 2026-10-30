# Consigne — session Claude Code sur la VM Debian — ENV-14 (nettoyage de l'arbre)

Fichier autonome : il suffit, avec `ORCHESTRATION.md` §2bis, à conduire la session VM. Rédigé le
2026-10-30 par la session Mac `nettoyage-arbre-env-14` (tâche 6 d'ENV-14), repris de
`consignes/env-13-debian.md` ; son texte est envoyé tel quel dans l'ordre `R14-1`.

## 1. Objet

Vérifier sur Debian x86_64 que le nettoyage d'ENV-14 ne change rien aux constructions : rootstock
neuf depuis la graine publiée, puis bascule des deux greffons nettoyés sur leur branche
`devenv/env-14`, reconstruction de toutes les cibles, comparaison avec R13-1 (même chaîne Debian).

- Graine `https://github.com/lepton-distribution/lepton-seed.scions.git`, branche `original-tree`
  (0f1275a), inchangée.
- Branches nettoyées (poussées par la session Mac, PA-16) :
  - noyau `lepton-original-tree.scions` : `devenv/env-14` = e5a5689 (depuis `master` 16a331b ;
    4 commits, 81 fichiers retirés) ;
  - `lepton-famille-stm32f4xx` : `devenv/env-14` = af964c6 (depuis `master` 01b5528 ; 1 fichier
    retiré).
- Autres greffons (`master`) : `lepton-famille-qemu-mps2` 3954357, `lepton-bsp-qemu-mps2-an386`
  046779e, `lepton-bsp-qemu-mps2-an500` e98a482, `lepton-bsp-nucleo-f429zi` 8ea7ee5,
  `lepton-famille-stm32wlxx` 1eccc2f, `lepton-bsp-nucleo-wl55jc1` a329f4d.
- lepton-tools : branche `devenv/env-14` (cette consigne, rapports Mac d'ENV-14).

Référence Mac (`doc/devenv/rapports/env-14-nettoyage.md` §3, §4) : 4011 liens après la greffe
initiale, 3929 après la bascule ; host ctest 7/7, empreintes mklepton identiques avant/après ;
14 presets construits ; banc KAL 18/18 (hard) et 14/14 (soft) sur les 6 presets QEMU.
Référence Debian : `doc/devenv/rapports/env-13-debian.md` et `oracles/env-13-debian/`.

La session VM ne développe pas : elle exécute, constate et rapporte. Pas de carte sur la VM : les
presets de carte sont construits, jamais flashés. Aucune commande `sudo` n'est prévue.

## 2. Ce que la session VM peut faire, et ne fait pas

| Autorisé | Interdit |
| --- | --- |
| `git fetch` / `switch` de `~/lepton-tools-dev/lepton-tools` (`devenv/env-14`) | Modifier `DEVENV-STATUS.md`, `ORCHESTRATION.md`, `SPECIFICATION.md`, `handoff/*.md` |
| Créer `~/lepton-tools-dev/essais/env-14-debian` (rootstock neuf) et y tout faire, dont `git fetch` / `switch` des clones du noyau et de `family-stm32f4xx` | Toucher aux rootstocks existants (`essais/env-13-debian`, `essais/env-11/*`, …) |
| Créer `devenv/env-14-debian` (depuis `devenv/env-14`) dans lepton-tools ; y écrire `doc/devenv/rapports/env-14-debian.md` et les captures `doc/devenv/rapports/oracles/env-14-debian/` | Commiter sur une autre branche |
| `git push origin devenv/env-14-debian` **après accord explicite de l'utilisateur** (PA-P) | Pousser toute autre branche ; tout `scion seed-update` / `graft-update` |
| | Écrire un fichier régulier dans `trunk/` ; corriger quoi que ce soit (consigner l'écart pour la session Mac) |

Tout écart au plan, toute erreur non prévue : s'arrêter, exposer, attendre l'utilisateur.

## 3. Communication (ORCHESTRATION §2bis)

- Session principale : `nettoyage-arbre-env-14` (session Mac) ; répondre à l'adresse `from` du
  message d'ordre.
- ID : `R14-1`, repris tel quel (`[ACCUSÉ R14-1] ENV-14 — …`, `[AVANCEMENT R14-1] …`,
  `[QUESTION R14-1] …`, `[FIN-SUCCÈS R14-1] …` ou `[FIN-ÉCHEC R14-1] …`).
- `ACCUSÉ` avant toute commande : ordre reformulé en une phrase, tête réelle de `devenv/env-14` de
  lepton-tools après `fetch`, résultat de `git ls-remote` du §5, étapes prévues (§5 à §8), écarts
  déjà visibles.
- `AVANCEMENT` : après §6 (greffe et bascule), après §7 (constructions), et à chaque arrêt.
- `FIN-SUCCÈS` / `FIN-ÉCHEC` : résultat par critère du §9, commits et branche (poussée ou non),
  chemin du rapport, versions relevées, écarts, ce qui n'a pas été fait.

## 4. Journaux et variables

```bash
mkdir -p ~/env-14-journaux
J=~/env-14-journaux
T=~/lepton-tools-dev/lepton-tools
R=~/lepton-tools-dev/essais/env-14-debian
G=https://github.com/lepton-distribution
```
Une commande par journal `$J/<étape>.log`, code de retour en dernière ligne.

## 5. Vérifications préalables (lecture seule)

```bash
uname -sm; cat /etc/debian_version; id -un
scion version | tail -1; lepton --version
arm-none-eabi-gcc --version | head -1; cmake --version | head -1; ninja --version
qemu-system-arm --version | head -1; python3 --version
echo "LEPTON_EMBOS_ROOT=${LEPTON_EMBOS_ROOT:-absente}"; ls -d ~/lepton/third_party/embos/cortexm-gcc/5.20.0.0 2>&1
df -h ~ /tmp | tail -2
test -e "$R" && echo "ARRÊT : $R existe déjà"
git -C "$T" status --short | head -5
git -C "$T" fetch origin && git -C "$T" switch devenv/env-14 && git -C "$T" log --oneline -1
echo "graine $(git ls-remote $G/lepton-seed.scions.git original-tree | cut -c1-7)"
echo "noyau master $(git ls-remote $G/lepton-original-tree.scions.git master | cut -c1-7) devenv/env-14 $(git ls-remote $G/lepton-original-tree.scions.git devenv/env-14 | cut -c1-7)"
echo "f4 master $(git ls-remote $G/lepton-famille-stm32f4xx.git master | cut -c1-7) devenv/env-14 $(git ls-remote $G/lepton-famille-stm32f4xx.git devenv/env-14 | cut -c1-7)"
for d in lepton-famille-qemu-mps2 lepton-bsp-qemu-mps2-an386 lepton-bsp-qemu-mps2-an500 \
         lepton-bsp-nucleo-f429zi lepton-famille-stm32wlxx lepton-bsp-nucleo-wl55jc1; do
  echo "$d $(git ls-remote $G/$d.git master | cut -c1-7)"
done
```
Arrêts : `$R` existe ; lepton-tools non propre ; un commit du §1 diffère ; moins de 3 Go libres
dans `~`. embOS absent : ce n'est pas un arrêt ; les 7 presets `*-embos*` seront alors en échec
attendu, à consigner comme tel.

## 6. Rootstock neuf, puis bascule sur `devenv/env-14`

```bash
mkdir "$R" && cd "$R"
scion rootstock-install
scion seed-add --version original-tree $G/lepton-seed.scions.git
scion graft
echo "initial : liens $(find trunk -type l | wc -l) cassés $(find -L trunk -type l | wc -l) réguliers $(find trunk -type f ! -name .scion.grafted.list | wc -l)"
for c in depots/lepton/original/master depots/lepton/family-stm32f4xx/master; do
  git -C $c fetch origin devenv/env-14 && git -C $c switch -c devenv/env-14 --track origin/devenv/env-14
  echo "$c $(git -C $c branch --show-current) $(git -C $c rev-parse --short HEAD)"
done
scion graft --scion lepton@original::tree --scion lepton@family-stm32f4xx
cat trunk/.scion.grafted.list
echo "bascule : liens $(find trunk -type l | wc -l) cassés $(find -L trunk -type l | wc -l) réguliers $(find trunk -type f ! -name .scion.grafted.list | wc -l) DS $(find trunk -name .DS_Store | wc -l)"
for p in tools/bin tools/config tools/host tools/mklepton/prj sys/user/build sys/user/tauon_sampleapp tauon_make_link.bat; do
  test -e trunk/$p && echo "PRÉSENT : $p"
done
```
Attendu : greffe initiale 9 entrées, 4011 liens, 0 cassé, 0 fichier régulier (comme R13-1) ;
bascule : clones à e5a5689 et af964c6, 3929 liens, 0 cassé, 0 fichier régulier, 0 `.DS_Store`,
aucun chemin retiré présent. `scion graft` doit réussir sans `--force`.

## 7. Reconstruction de toutes les cibles

```bash
cd "$T" && git switch -c devenv/env-14-debian devenv/env-14
scripts/oracle/rejouer-oracle.sh "$R" doc/devenv/rapports/oracles/env-14-debian \
  --qemu qemu-mps2-an386-embos --qemu qemu-mps2-an386-embos-soft \
  --qemu qemu-mps2-an386-freertos --qemu qemu-mps2-an386-freertos-soft \
  --qemu qemu-mps2-an500-embos --qemu qemu-mps2-an500-freertos \
  --carte nucleo-f429zi-embos --carte nucleo-f429zi-freertos \
  --carte nucleo-wl55jc1-embos --carte nucleo-wl55jc1-freertos \
  --carte samd21-xplained-pro-embos --carte samd21-xplained-pro-freertos \
  --carte stm32f746g-disco-embos --carte stm32f746g-disco-freertos > "$J/7-rejouer.log" 2>&1; echo "code=$?" >> "$J/7-rejouer.log"
tail -20 "$J/7-rejouer.log"
grep -h "tests passed" doc/devenv/rapports/oracles/env-14-debian/*/ctest.log doc/devenv/rapports/oracles/env-14-debian/*/banc-kal.log
grep -a "uname" -A1 doc/devenv/rapports/oracles/env-14-debian/qemu-mps2-an386-freertos/fumee.log
find -L "$R/trunk" -type l | wc -l; find "$R/trunk" -type f ! -name .scion.grafted.list | wc -l
```
Attendu : host ctest 7/7 ; 14 presets construits (`lepton.elf`) ; banc KAL 18/18 (hard) et 14/14
(soft) sur les 6 presets QEMU, fumée comprise ; trunk toujours sans fichier régulier ni lien cassé.
Un échec de construction : relever le premier message d'erreur de
`doc/devenv/rapports/oracles/env-14-debian/<preset>/construction.log`, et continuer les autres
presets (le script le fait).

## 8. Comparaisons

Avec R13-1 (même chaîne Debian, arbre avant nettoyage) — **c'est la non-régression** : attendu
`comparer=0` partout et empreintes mklepton identiques. Les empreintes binaires (`empreintes.txt`)
diffèrent par la date de construction embarquée (E1, démontrée au Mac) : ce n'est pas un échec.
Avec le Mac (informative ; chaînes différentes) : consigner les codes sans les interpréter.

```bash
cd "$T"; O=doc/devenv/rapports/oracles
diff -q $O/env-13-debian/host/mklepton-empreintes.sha256 $O/env-14-debian/host/mklepton-empreintes.sha256 && echo "mklepton R13-1 identiques"
diff -q $O/env-14-apres/host/mklepton-empreintes.sha256 $O/env-14-debian/host/mklepton-empreintes.sha256 && echo "mklepton Mac identiques"
for p in $(ls $O/env-14-debian | grep -v host); do
  python3 scripts/oracle/comparer-oracle.py $O/env-13-debian/$p $O/env-14-debian/$p > /dev/null 2>&1; a=$?
  python3 scripts/oracle/comparer-oracle.py $O/env-14-apres/$p $O/env-14-debian/$p > /dev/null 2>&1; b=$?
  echo "$p comparer_R13-1=$a comparer_Mac=$b"
done
```
Un `comparer_R13-1` différent de 0 : relever la sortie complète de `comparer-oracle.py` dans le
rapport ; c'est un écart à exposer, pas à corriger.

## 9. Critères et rapport

| Critère | Attendu |
| --- | --- |
| C1 Dépôts publiés | `git ls-remote` conforme au §1 (dont les deux `devenv/env-14`) |
| C2 Greffe et bascule | initial : 9 entrées, 4011 liens ; bascule sans `--force` : 3929 liens ; 0 cassé, 0 fichier régulier, 0 `.DS_Store`, aucun chemin retiré présent |
| C3 host | construction réussie, ctest 7/7, `mklepton-empreintes.sha256` identique à R13-1 |
| C4 14 presets | construits (embOS : échec attendu seulement si embOS absent, consigné) |
| C5 QEMU | banc KAL 18/18 ou 14/14 et fumée réussie sur chaque preset QEMU construit |
| C6 Non-régression Debian | `comparer-oracle` code 0 contre `env-13-debian` sur chaque preset construit |
| C7 Trunk après construction | 0 fichier régulier, 0 lien cassé |

Rapport `doc/devenv/rapports/env-14-debian.md` sur `devenv/env-14-debian` (depuis
`devenv/env-14`), contenant : hôte et versions (§5), table des critères, table des presets
(construction, fumée, banc KAL, comparaisons §8), écarts. Commit du rapport et de
`oracles/env-14-debian/`, puis `QUESTION` à l'utilisateur pour le push (PA-P), puis `FIN-*`. Le
rootstock `$R` est conservé.
