#!/usr/bin/env bash
# ENV-68 (D32, D37) : état laissé par un retrait refusé, et greffon déclaré sans clone, sur des copies
# d'essai (jamais <ROOTSTOCK>).
# Usage : graine.sh <essai E> <phase> <sortie versionnée>
#   <E>/rs : rootstock d'essai <C> (copie d'essais/env-11/qemu sans build/), jamais modifié ;
#   <E>/<phase>/<cas>/rs : copie de <C> par cas ; <E>/<phase>/d68, d68b : dépôts du greffon d'essai
#   env68lib (lepton scion new ; d68b : seconde origine, pour seed replace) ;
#   <E>/<phase>/brut : relevés bruts ; <sortie versionnée> : relevés normalisés + resume.tsv.
# Chaque étape relève le code, la première ligne du message, et l'état comparé à « départ » (copie
# avant seed add) et à « ajouté » (après seed add) : liens, cassés, réguliers, graine (empreintes
# de .scion/ et état git), liste greffée, depots/ ; plus la ligne env68lib de lepton-graine.json,
# de .scion.sources.list et de .scion.grafted.list.
set -u
export LC_ALL=C
E=$1 phase=$2 vers=$3
here=$(cd "$(dirname "$0")" && pwd)
RL=$here/../env-51-messages/releve.sh
ETAT=$here/../env-55-url-file/etat.sh
SUP=$here/../../../../scripts/supprimer-essai.sh
C=$E/rs P=$E/$phase brut=$E/$phase/brut
D=$P/d68 D2=$P/d68b
KEY=lepton@library-env68lib CL=depots/lepton/library-env68lib/master
SEED=depots/lepton-seed/env11/scion/.scion
case $E in "$HOME"/lepton-tools-dev/essais/?*) ;; *) echo "$E hors d'essais/" >&2; exit 2 ;; esac
[ -e "$P" ] && { echo "$P existe déjà" >&2; exit 2; }
[ -d "$C/trunk" ] || { echo "$C : rootstock d'essai absent" >&2; exit 2; }
mkdir -p "$brut" "$vers"
printf 'étape\tcode\tvs départ\tvs ajouté\tgraine.json\tsources\tgrafted\tmessage\n' >"$brut/resume.tsv"

# Dépôts du greffon d'essai (sur une copie jetable : scion new --no-seed n'écrit que le dépôt)
rsync -a "$C/" "$P/prep/rs/"
bash "$RL" "$brut" prep-d68 "$P/prep/rs" lepton scion new env68lib --type bibliotheque --repo "$D" \
  --no-seed --no-cmake >>"$brut/journal.txt" 2>&1
bash "$RL" "$brut" prep-d68b "$P/prep/rs" lepton scion new env68lib --type bibliotheque --repo "$D2" \
  --no-seed --no-cmake >>"$brut/journal.txt" 2>&1

ligne() { grep -h "$2" "$1" 2>/dev/null | tr '\t' ' ' | tr -s ' ' | head -1; }
# pas <cas> <étape> <cwd> <commande…> : relevé et comparaison
pas() {
  local cas=$1 nom=$1-$2 dir=$3 R=$P/$1/rs f vd va gj so gr msg
  shift 3
  bash "$RL" "$brut" "$nom" "$dir" "$@" >>"$brut/journal.txt" 2>&1
  bash "$ETAT" "$R" "$brut/etat-$nom" >/dev/null
  for ref in depart ajoute; do
    [ -d "$brut/etat-$cas-$ref" ] || { printf -- '-\n' >"$brut/$nom.vs-$ref"; continue; }
    for f in liens casses reguliers graine grafted depots; do
      cmp -s "$brut/etat-$cas-$ref/$f.txt" "$brut/etat-$nom/$f.txt" || printf '%s≠ ' "$f"
    done >"$brut/$nom.vs-$ref"
    [ -s "$brut/$nom.vs-$ref" ] || echo '=' >"$brut/$nom.vs-$ref"
  done
  vd=$(cat "$brut/$nom.vs-depart") va=$(cat "$brut/$nom.vs-ajoute")
  gj=$(grep -c env68lib "$R/$SEED/lepton-graine.json")
  so=$(grep -c library-env68lib "$R/$SEED/.scion.sources.list")
  gr=$(grep -c library-env68lib "$R/trunk/.scion.grafted.list")
  msg=$(grep -m1 -E 'lepton: (erreur|attention)|scion:.*(refus|erreur|absent)|Traceback' "$brut/$nom.err" | cut -c1-200)
  [ -n "$msg" ] || msg=$(grep -m1 . "$brut/$nom.err" | cut -c1-200)
  [ -n "$msg" ] || msg=$(grep -m1 . "$brut/$nom.out" | cut -c1-200)
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$nom" "$(cat "$brut/$nom.code")" "$vd" "$va" "$gj" "$so" "$gr" \
    "$msg" >>"$brut/resume.tsv"
  printf '%s\tcode %s\tdépart:%s\tajouté:%s\tjson:%s src:%s gr:%s\n' "$nom" "$(cat "$brut/$nom.code")" \
    "$vd" "$va" "$gj" "$so" "$gr"
}
# nouveau <cas> <origine> : copie de <C>, état « départ », seed add env68lib, état « ajouté »
nouveau() {
  local cas=$1 R=$P/$1/rs
  rsync -a "$C/" "$R/"
  bash "$ETAT" "$R" "$brut/etat-$cas-depart" >/dev/null
  pas "$cas" add "$R" lepton seed add env68lib "$2" --type bibliotheque --no-cmake
  cp -R "$brut/etat-$cas-add" "$brut/etat-$cas-ajoute"
}

# --- D32 : retrait refusé par scion entre les deux appels -------------------------------------
# Origine URL `file://` : seule une URL (ou un chemin suivi d'une version) donne un clone sous
# depots/ ; un chemin local sans version est greffé en place (version `*`, aucun clone).
# r1 : clone modifié non commité (fichier non suivi), seed remove --purge ; puis relance
nouveau r1 "file://$D"
echo essai >"$P/r1/rs/$CL/env68-non-suivi.txt"
pas r1 purge "$P/r1/rs" lepton seed remove env68lib --purge --no-cmake
pas r1 status "$P/r1/rs" lepton seed status --json
"$SUP" "$P/r1/rs/$CL/env68-non-suivi.txt" >>"$brut/journal.txt" 2>&1
pas r1 relance "$P/r1/rs" lepton seed remove env68lib --purge --no-cmake
# r2 : commit local absent de l'amont, seed remove --purge
nouveau r2 "file://$D"
git -C "$P/r2/rs/$CL" commit -q --allow-empty -m "ENV-68 : commit local"
pas r2 purge "$P/r2/rs" lepton seed remove env68lib --purge --no-cmake
# r3 : sans --purge, clone modifié : graft-remove accepté (rien n'est contrôlé sans --purge)
nouveau r3 "file://$D"
echo essai >"$P/r3/rs/$CL/env68-non-suivi.txt"
pas r3 remove "$P/r3/rs" lepton seed remove env68lib --no-cmake
# r4 : seed replace, origine URL (graft-remove --purge d'abord), clone modifié
nouveau r4 "file://$D"
echo essai >"$P/r4/rs/$CL/env68-non-suivi.txt"
pas r4 replace "$P/r4/rs" lepton seed replace env68lib "file://$D2" --no-cmake
# r5 : origine locale greffée en place (aucun clone), seed remove --purge
nouveau r5 "$D"
pas r5 purge "$P/r5/rs" lepton seed remove env68lib --purge --no-cmake
# r6 : conséquence d'un --purge refusé sur file remove (avant correction : « hors de la graine »)
nouveau r6 "file://$D"
echo essai >"$P/r6/rs/$CL/env68-non-suivi.txt"
pas r6 purge "$P/r6/rs" lepton seed remove env68lib --purge --no-cmake
pas r6 file-remove "$P/r6/rs" lepton file remove trunk/sys/root/src/lib/env68lib/env68lib.c

# --- D37 : greffon déclaré dont le clone a disparu (une copie par retrait) ---------------------
# g1 : constats (status, check, add, replace, graft), puis seed remove sous le nom de la graine, puis
#      réajout ; g3 : suffixe de clé ; g4 : --purge ; g5 : après scion graft-remove ;
# g2 : scion graft-remove --purge
for cas in g1 g2 g3 g4 g5; do
  nouveau $cas "file://$D"
  "$SUP" "$P/$cas/rs/$CL" >>"$brut/journal.txt" 2>&1
  pas $cas sans-clone "$P/$cas/rs" true
done
R=$P/g1/rs
pas g1 status "$R" lepton seed status --json
python3 - "$brut/g1-status.out" >"$brut/g1-status.entree" <<'EOF2'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
for s in d["scions"]:
    if "env68lib" in s["key"]:
        print(json.dumps({k: s[k] for k in ("name", "role", "key", "in_seed", "path")}, ensure_ascii=False))
print("missing", d["missing"], "broken_links", len(d["trunk_check"]["broken_links"]))
EOF2
pas g1 check "$R" lepton check
pas g1 add-refus "$R" lepton seed add env68lib "file://$D" --type bibliotheque --no-cmake
pas g1 replace-nom "$R" lepton seed replace env68lib "file://$D2" --no-cmake
pas g1 replace-suffixe "$R" lepton seed replace library-env68lib "file://$D2" --no-cmake
pas g1 graft "$R" lepton graft --no-cmake
pas g1 remove-nom "$R" lepton seed remove env68lib --no-cmake
pas g1 readd "$R" lepton seed add env68lib "file://$D" --type bibliotheque --no-cmake
pas g3 remove-suffixe "$P/g3/rs" lepton seed remove library-env68lib --no-cmake
pas g4 remove-purge "$P/g4/rs" lepton seed remove env68lib --purge --no-cmake
pas g5 scion-graft-remove "$P/g5/rs" scion graft-remove "$KEY"
pas g5 remove "$P/g5/rs" lepton seed remove env68lib --no-cmake
pas g5 readd "$P/g5/rs" lepton seed add env68lib "file://$D" --type bibliotheque --no-cmake
pas g2 scion-graft-remove-purge "$P/g2/rs" scion graft-remove --purge "$KEY"

U=$(id -un)
for f in "$brut"/*.cmd "$brut"/*.out "$brut"/*.err "$brut"/*.code "$brut"/*.vs-* "$brut"/*.entree \
         "$brut"/resume.tsv; do
  [ -e "$f" ] || continue
  sed -e "s#$P#<P>#g" -e "s#$C#<C>#g" -e "s#$E#<E>#g" -e "s#$HOME#<HOME>#g" -e "s#~$U/#~<U>/#g" \
    "$f" >"$vers/$(basename "$f")"
done
