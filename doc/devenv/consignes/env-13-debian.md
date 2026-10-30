# Consigne — session Claude Code sur la VM Debian — ENV-13 (graine de référence publiée)

Fichier autonome : il suffit, avec `ORCHESTRATION.md` §2bis, à conduire la session VM. Rédigé le
2026-10-30 par la session Mac `publish-seed-reference-tree` (après clôture d'ENV-13), à la demande de
l'utilisateur ; son texte est envoyé tel quel dans l'ordre `R13-1`.

## 1. Objet

Vérifier sur Debian x86_64 que l'arbre Lepton complet s'assemble depuis GitHub par la seule graine
publiée et que toutes les cibles se reconstruisent :

- graine `https://github.com/lepton-distribution/lepton-seed.scions.git`, branche `original-tree`
  (0f1275a) : noyau `original::tree`, `building`, et 7 greffons famille/BSP désormais publiés ;
- greffons (`master`) : `lepton-famille-qemu-mps2` 3954357, `lepton-bsp-qemu-mps2-an386` 046779e,
  `lepton-bsp-qemu-mps2-an500` e98a482, `lepton-famille-stm32f4xx` 01b5528,
  `lepton-bsp-nucleo-f429zi` 8ea7ee5, `lepton-famille-stm32wlxx` 1eccc2f,
  `lepton-bsp-nucleo-wl55jc1` a329f4d ; noyau `lepton-original-tree.scions` `master` 16a331b.

Référence Mac (`doc/devenv/rapports/env-13-graine.md` §4, §6) : host ctest 7/7 ; 14 presets
construits ; banc KAL 18/18 (hard) et 14/14 (soft) sur les 6 presets QEMU ; rootstock vierge :
4011 liens, 0 cassé.

La session VM ne développe pas : elle exécute, constate et rapporte. Pas de carte sur la VM : les
presets de carte sont construits, jamais flashés. Aucune commande `sudo` n'est prévue.

## 2. Ce que la session VM peut faire, et ne fait pas

| Autorisé | Interdit |
| --- | --- |
| `git fetch` / `switch` / `pull --ff-only` de `~/lepton-tools-dev/lepton-tools` (`main`) | Modifier `DEVENV-STATUS.md`, `ORCHESTRATION.md`, `SPECIFICATION.md`, `handoff/*.md` |
| Créer `~/lepton-tools-dev/essais/env-13-debian` (rootstock neuf) et y tout faire | Toucher aux rootstocks existants (`essais/env-11/*`, …) ou au clone `lepton-noyau` |
| Créer `devenv/env-13-debian` (depuis `main`) dans lepton-tools ; y écrire `doc/devenv/rapports/env-13-debian.md` et les captures `doc/devenv/rapports/oracles/env-13-debian/` | Commiter sur `main` ou une autre branche |
| `git push origin devenv/env-13-debian` **après accord explicite de l'utilisateur** (PA-P) | Pousser toute autre branche ; tout `scion seed-update` / `graft-update` |
| | Écrire un fichier régulier dans `trunk/` ; corriger quoi que ce soit (consigner l'écart pour la session Mac) |

Tout écart au plan, toute erreur non prévue : s'arrêter, exposer, attendre l'utilisateur.

## 3. Communication (ORCHESTRATION §2bis)

- Session principale : `publish-seed-reference-tree` (session Mac) ; répondre à l'adresse `from` du
  message d'ordre.
- ID : `R13-1`, repris tel quel (`[ACCUSÉ R13-1] ENV-13 — …`, `[AVANCEMENT R13-1] …`,
  `[QUESTION R13-1] …`, `[FIN-SUCCÈS R13-1] …` ou `[FIN-ÉCHEC R13-1] …`).
- `ACCUSÉ` avant toute commande : ordre reformulé en une phrase, tête réelle de `main` de
  lepton-tools après `fetch`, résultat de `git ls-remote` des 9 dépôts du §1, étapes prévues (§5 à
  §8), écarts déjà visibles.
- `AVANCEMENT` : après §6 (greffe), après §7 (constructions), et à chaque arrêt.
- `FIN-SUCCÈS` / `FIN-ÉCHEC` : résultat par critère du §9, commits et branche (poussée ou non),
  chemin du rapport, versions relevées, écarts, ce qui n'a pas été fait.

## 4. Journaux et variables

```bash
mkdir -p ~/env-13-journaux
J=~/env-13-journaux
T=~/lepton-tools-dev/lepton-tools
R=~/lepton-tools-dev/essais/env-13-debian
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
git -C "$T" fetch origin && git -C "$T" switch main && git -C "$T" pull --ff-only && git -C "$T" log --oneline -1
for d in lepton-seed.scions lepton-original-tree.scions lepton-famille-qemu-mps2 lepton-bsp-qemu-mps2-an386 \
         lepton-bsp-qemu-mps2-an500 lepton-famille-stm32f4xx lepton-bsp-nucleo-f429zi lepton-famille-stm32wlxx \
         lepton-bsp-nucleo-wl55jc1; do
  echo "$d $(git ls-remote https://github.com/lepton-distribution/$d.git master original-tree | cut -c1-7 | tr '\n' ' ')"
done
```
Arrêts : `$R` existe ; un commit du §1 diffère ; moins de 3 Go libres dans `~`.
embOS absent (`LEPTON_EMBOS_ROOT` vide et répertoire absent) : ce n'est pas un arrêt. Les 7 presets
`*-embos*` seront alors en échec attendu, à consigner comme tel.

## 6. Rootstock neuf depuis la graine publiée

```bash
mkdir "$R" && cd "$R"
scion rootstock-install
scion seed-add --version original-tree https://github.com/lepton-distribution/lepton-seed.scions.git
scion graft
cat trunk/.scion.grafted.list
echo "liens $(find trunk -type l | wc -l) cassés $(find -L trunk -type l | wc -l) réguliers $(find trunk -type f ! -name .scion.grafted.list | wc -l)"
for d in depots/lepton/*/master depots/lepton-seed.scions/original-tree; do
  echo "$d $(git -C $d branch --show-current) $(git -C $d rev-parse --short HEAD) $(git -C $d remote get-url origin)"
done
```
Attendu : 9 entrées (`original::tree`, `building`, `family-qemu-mps2`, `bsp-qemu-mps2-an386`,
`bsp-qemu-mps2-an500`, `family-stm32f4xx`, `bsp-nucleo-f429zi`, `family-stm32wlxx`,
`bsp-nucleo-wl55jc1`), 4011 liens, 0 cassé, 0 fichier régulier ; 9 clones aux commits du §1.

## 7. Reconstruction de toutes les cibles

Le script du dépôt construit à neuf host puis chaque preset, capture les binaires, et lance `ctest`
(fumée + banc KAL) sur les presets QEMU. C'est le même script qu'au Mac.

```bash
cd "$T" && git switch -c devenv/env-13-debian main
scripts/oracle/rejouer-oracle.sh "$R" doc/devenv/rapports/oracles/env-13-debian \
  --qemu qemu-mps2-an386-embos --qemu qemu-mps2-an386-embos-soft \
  --qemu qemu-mps2-an386-freertos --qemu qemu-mps2-an386-freertos-soft \
  --qemu qemu-mps2-an500-embos --qemu qemu-mps2-an500-freertos \
  --carte nucleo-f429zi-embos --carte nucleo-f429zi-freertos \
  --carte nucleo-wl55jc1-embos --carte nucleo-wl55jc1-freertos \
  --carte samd21-xplained-pro-embos --carte samd21-xplained-pro-freertos \
  --carte stm32f746g-disco-embos --carte stm32f746g-disco-freertos > "$J/7-rejouer.log" 2>&1; echo "code=$?" >> "$J/7-rejouer.log"
tail -20 "$J/7-rejouer.log"
grep -h "tests passed" doc/devenv/rapports/oracles/env-13-debian/*/ctest.log doc/devenv/rapports/oracles/env-13-debian/*/banc-kal.log
grep -a "uname" -A1 doc/devenv/rapports/oracles/env-13-debian/qemu-mps2-an386-freertos/fumee.log
find -L "$R/trunk" -type l | wc -l; find "$R/trunk" -type f ! -name .scion.grafted.list | wc -l
```
Attendu : host ctest 7/7 ; 14 presets construits (`lepton.elf`) ; banc KAL 18/18 (hard) et 14/14
(soft) sur les 6 presets QEMU, fumée comprise ; trunk toujours sans fichier régulier ni lien cassé.
Un échec de construction : relever le premier message d'erreur de
`doc/devenv/rapports/oracles/env-13-debian/<preset>/construction.log`, et continuer les autres
presets (le script le fait).

## 8. Comparaison avec le Mac (informative)

Les chaînes diffèrent (Arm GNU Toolchain 14.2.Rel1 sur le Mac, paquet Debian 14.2.1 sur la VM) : une
différence de symboles n'est **pas** un échec. Les captures du Mac sont dans
`doc/devenv/rapports/oracles/env-13-apres/`.

```bash
cd "$T"; O=doc/devenv/rapports/oracles
diff -q $O/env-13-apres/host/mklepton-empreintes.sha256 $O/env-13-debian/host/mklepton-empreintes.sha256
for p in $(ls $O/env-13-debian | grep -v host); do
  python3 scripts/oracle/comparer-oracle.py $O/env-13-apres/$p $O/env-13-debian/$p > /dev/null 2>&1; echo "$p comparer=$?"
done
```
Consigner les codes de retour, sans les interpréter au-delà.

## 9. Critères et rapport

| Critère | Attendu |
| --- | --- |
| C1 Graine et greffons publiés | `git ls-remote` conforme au §1 |
| C2 Greffe depuis GitHub | 9 entrées, 4011 liens, 0 cassé, 0 fichier régulier, 9 clones aux commits du §1 |
| C3 host | construction réussie, ctest 7/7, `mklepton-empreintes.sha256` produit |
| C4 14 presets | construits (embOS : échec attendu seulement si embOS absent, consigné) |
| C5 QEMU | banc KAL 18/18 ou 14/14 et fumée réussie sur chaque preset QEMU construit |
| C6 Trunk après construction | 0 fichier régulier, 0 lien cassé |

Rapport `doc/devenv/rapports/env-13-debian.md` sur `devenv/env-13-debian` (depuis `main`), contenant :
hôte et versions (§5), table des critères, table des presets (construction, fumée, banc KAL,
comparaison §8), écarts. Commit du rapport et de `oracles/env-13-debian/`, puis `QUESTION` à
l'utilisateur pour le push (PA-P), puis `FIN-*`. Le rootstock `$R` est conservé.
