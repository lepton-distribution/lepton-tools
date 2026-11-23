#!/usr/bin/env bash
# shellcheck disable=SC2088  # `~` littéral voulu : chemin transmis sans développement (D29)
# ENV-68 (D29, D30) : chemins saisis hors des 6 de D21, par forme, sur des copies d'essai (jamais
# <ROOTSTOCK>). Repris d'env-63-tilde/chemins.sh.
# Usage : chemins.sh <essai E> <phase> <sortie versionnée> [<clangd>]
#   <E>/rs    : rootstock d'essai <C> (copie d'essais/env-11/qemu sans build/, graine de projet env11),
#               jamais modifié (lectures seules : check FILE) ;
#   <E>/M     : modèle de graine non migrée (copie de <C>, XML de la graine hors du greffon du projet),
#               préparé une fois, jamais modifié ; une copie <E>/<phase>/m1-<f> par cas d'import ;
#   <E>/<phase>/G : copie de <C> pour generate --clangd (écrit l'espace de travail) ;
#   <E>/<phase>/w/<cas> : répertoire courant de chaque cas hors rootstock ;
#   <E>/<phase>/t : rootstocks créés par seed new ;  <E>/<phase>/brut : relevés bruts.
# Formes (chemin transmis tel quel, appel en liste : forme de l'extension) :
#   t `~/…`  u `~<U>/…`  x `~inconnu68/…`  a absolu  d `~/…` développé par bash  r relatif
#   (r : au répertoire courant pour check, au trunk pour mkconf ; rc : relatif au répertoire courant,
#   pour mkconf import ; h : chemin hors du trunk, sous depots/)
# Chemins : c1 check FILE (hors trunk : lepton-graine.json)  c2 check FILE (sous le trunk)
#           m1 seed mkconf import PATH   n1 seed new --mkconf PATH   p6 generate --clangd (D30)
set -u
export LC_ALL=C
E=$1 phase=$2 vers=$3 CL=${4:-clangd-mp-21}
here=$(cd "$(dirname "$0")" && pwd)
RL=$here/../env-51-messages/releve.sh
ETAT=$here/../env-55-url-file/etat.sh
U=$(id -un)
C=$E/rs M=$E/M P=$E/$phase
G=$P/G W=$P/w T=$P/t brut=$P/brut
case $E in "$HOME"/lepton-tools-dev/essais/?*) ;; *) echo "$E hors d'essais/" >&2; exit 2 ;; esac
id inconnu68 >/dev/null 2>&1 && { echo "l'utilisateur inconnu68 existe" >&2; exit 2; }
[ -e "$P" ] && { echo "$P existe déjà" >&2; exit 2; }
[ -d "$C/trunk" ] || { echo "$C : rootstock d'essai absent" >&2; exit 2; }
XML=sys/user/tauon-basic/etc/mkconf_tauon_basic_qemu_mps2.xml
SEED=depots/lepton-seed/env11

# Modèle M : graine non migrée (XML de la graine = XML de référence du trunk, pas de XML de projet)
if [ ! -d "$M/trunk" ]; then
  rsync -a "$C/" "$M/"
  git -C "$M/$SEED" rm -q -r project/scion/sys
  python3 - "$M/$SEED/scion/.scion/lepton-graine.json" "$XML" <<'EOF'
import json, sys
p, xml = sys.argv[1], sys.argv[2]
d = json.load(open(p, encoding="utf-8")); d["mklepton_xml"] = xml
open(p, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
EOF
  git -C "$M/$SEED" commit -q -am "ENV-68 : graine non migrée (essai de seed mkconf import)"
  (cd "$M" && scion graft --scion lepton@project-env11) >"$E/M-preparation.log" 2>&1 \
    || { echo "préparation de M en échec ($E/M-preparation.log)" >&2; exit 2; }
fi
mkdir -p "$W" "$T" "$brut" "$vers" "$W/outils"
rsync -a "$C/" "$G/"
ln -s "$(command -v "$CL")" "$W/outils/clangd"
develop() { bash -c "printf '%s' $1"; }
relpath() { python3 -c 'import os,sys;print(os.path.relpath(sys.argv[1],sys.argv[2]))' "$1" "$2"; }
hP=${P#"$HOME"/} hC=${C#"$HOME"/} hE=${E#"$HOME"/}
printf 'cas\tchemin\tforme\tcode\tcwd/~*\tR\tmessage\n' >"$brut/resume.tsv"

# cas <nom> <chemin> <forme> <cwd> <rootstock comparé ou -> <commande…>
cas() {
  local nom=$1 chemin=$2 forme=$3 dir=$4 R=$5 tilde etatR msg f
  shift 5
  mkdir -p "$dir"
  [ "$R" = - ] || bash "$ETAT" "$R" "$brut/etat-$nom-avant" >/dev/null
  bash "$RL" "$brut" "$nom" "$dir" "$@" >>"$brut/journal.txt" 2>&1
  tilde=$(cd "$dir" && ls -d ./~* 2>/dev/null | tr '\n' ' '); tilde=${tilde:-non}
  etatR=-
  if [ "$R" != - ]; then
    bash "$ETAT" "$R" "$brut/etat-$nom-apres" >/dev/null
    for f in liens casses reguliers graine grafted depots; do
      cmp -s "$brut/etat-$nom-avant/$f.txt" "$brut/etat-$nom-apres/$f.txt" || printf '%s≠ ' "$f"
    done >"$brut/$nom.etat"
    etatR=$(cat "$brut/$nom.etat"); etatR=${etatR:-=}
  fi
  msg=$(grep -m1 -E 'lepton:|Erreur|erreur|Traceback|introuvable|refusée' "$brut/$nom.err" | cut -c1-170)
  [ -n "$msg" ] || msg=$(grep -m1 . "$brut/$nom.out" | cut -c1-170)
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$nom" "$chemin" "$forme" "$(cat "$brut/$nom.code")" \
    "$tilde" "$etatR" "$msg" >>"$brut/resume.tsv"
  printf '%s\tcode %s\t~:%s\tR:%s\n' "$nom" "$(cat "$brut/$nom.code")" "$tilde" "$etatR"
}

forme() {  # <t|u|x|a|d> <chemin absolu sous HOME> → mot transmis
  local h=${2#"$HOME"/}
  case $1 in t) printf '%s' "~/$h" ;; u) printf '%s' "~$U/$h" ;; x) printf '%s' "~inconnu68/$h" ;;
    a) printf '%s' "$2" ;; d) develop "~/$h" ;; esac
}

# c1 : check FILE hors du trunk (manifeste de graine, lecture seule) ; c2 : sous le trunk (lien)
GJ=$C/$SEED/scion/.scion/lepton-graine.json
for f in t u x a d; do cas c1-$f "check FILE" $f "$W/c1-$f" "$C" lepton check "$(forme $f "$GJ")"; done
cas c1-r "check FILE" r "$W/c1-r" "$C" lepton check "$(relpath "$GJ" "$W/c1-r")"
TJ=$C/trunk/sys/root/src/lepton-greffon.json
for f in t a; do cas c2-$f "check FILE (trunk)" $f "$W/c2-$f" "$C" lepton check "$(forme $f "$TJ")"; done
cas c2-r "check FILE (trunk)" r "$C" "$C" lepton check trunk/sys/root/src/lepton-greffon.json

# m1 : seed mkconf import PATH, une copie de M par cas (une réussite écrit dans la graine)
m1() {  # <forme> <mot ou - pour calcul> <cwd relatif à la copie>
  local f=$1 R=$P/m1-$1/rs v=$2
  rsync -a "$M/" "$R/"
  cas m1-$f "seed mkconf import" $f "$R/$3" "$R" lepton seed mkconf import "$v"
  grep -h '"mklepton_xml"' "$R/$SEED/scion/.scion/lepton-graine.json" >"$brut/m1-$f.graine"
}
for f in t u x a d; do m1 $f "$(forme $f "$P/m1-$f/rs/trunk/$XML")" .; done
m1 r "$XML" .
m1 rc "$(basename "$XML")" "trunk/$(dirname "$XML")"
K=depots/lepton/original/master/scion   # clone propriétaire du XML (lien du trunk)
m1 h "$P/m1-h/rs/$K/$XML" .
m1 th "~/$hP/m1-th/rs/$K/$XML" .

# n1 : seed new --mkconf PATH (rootstock neuf sous <T>, origines prises dans les clones de <C>)
NEW=(--bsp qemu-mps2-an386 --backend freertos
     --origin "lepton-noyau=$C/depots/lepton/original/master"
     --origin "qemu-mps2=$C/depots/lepton/family-qemu-mps2/master"
     --origin "qemu-mps2-an386=$C/depots/lepton/bsp-qemu-mps2-an386/master")
for f in t u x a d; do
  cas n1-$f "seed new --mkconf" $f "$W/n1-$f" - lepton seed new env68 -C "$T/n1-$f" \
    --mkconf "$(forme $f "$T/n1-$f/trunk/$XML")" "${NEW[@]}"
  [ -d "$T/n1-$f" ] && echo créé >"$brut/n1-$f.cible" || echo absent >"$brut/n1-$f.cible"
done
cas n1-r "seed new --mkconf" r "$W/n1-r" - lepton seed new env68 -C "$T/n1-r" --mkconf "$XML" "${NEW[@]}"
[ -d "$T/n1-r" ] && echo créé >"$brut/n1-r.cible" || echo absent >"$brut/n1-r.cible"

# p6 : generate --clangd (D30) dans <G> ; chemin écrit relevé, et sa résolution depuis la racine
clangd_path() { python3 - "$G" <<'EOF'
import json, os, sys, glob, re
ws = glob.glob(os.path.join(sys.argv[1], "*.code-workspace"))[0]
text = re.sub(r"^\s*//.*$", "", open(ws, encoding="utf-8").read(), flags=re.M)
v = json.loads(text)["settings"].get("clangd.path")
print(f"clangd.path={v}\tdepuis la racine : {'trouvé' if v and os.path.isfile(os.path.join(sys.argv[1], v)) else 'introuvable'}")
EOF
}
p6() { local nom=$1 forme=$2 dir=$3; shift 3
  cas "$nom" "generate --clangd" "$forme" "$dir" - "$@"; clangd_path >"$brut/$nom.clangd"; }
p6 p6-a a "$G" lepton generate --clangd "$W/outils/clangd"
p6 p6-t t "$G" lepton generate --clangd "$(forme t "$W/outils/clangd")"
p6 p6-n nom "$G" lepton generate --clangd "$CL"
p6 p6-r r "$G" lepton generate --clangd "$(relpath "$W/outils/clangd" "$G")"
p6 p6-rs r "$G/trunk/sys" lepton generate --clangd "$(relpath "$W/outils/clangd" "$G/trunk/sys")"
mkdir -p "$W/p6-rw"
p6 p6-rw r "$W/p6-rw" lepton generate -C "$G" --clangd ../outils/clangd
p6 p6-rd r "$W" lepton generate -C "$G" --clangd ./outils/clangd

for f in "$brut"/*.cmd "$brut"/*.out "$brut"/*.err "$brut"/*.code "$brut"/*.etat "$brut"/*.graine \
         "$brut"/*.cible "$brut"/*.clangd "$brut"/resume.tsv; do
  [ -e "$f" ] || continue
  sed -e "s#$P#<P>#g" -e "s#$M#<M>#g" -e "s#$C#<C>#g" -e "s#$E#<E>#g" -e "s#$hP#<hP>#g" -e "s#$hC#<hC>#g" \
      -e "s#$hE#<hE>#g" -e "s#$HOME#<HOME>#g" -e "s#~$U/#~<U>/#g" "$f" >"$vers/$(basename "$f")"
done
