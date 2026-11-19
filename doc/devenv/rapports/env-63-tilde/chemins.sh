#!/usr/bin/env bash
# shellcheck disable=SC2088  # `~` littéral voulu : chemin transmis sans développement (D21)
# ENV-63 (D21) : chemins saisis de lepton, par forme, sur un rootstock d'essai (jamais <ROOTSTOCK>).
# Repris d'env-59-tilde/autres.sh. Usage : chemins.sh <essai E> <phase> <sortie versionnée>
#   <E>/rs    : rootstock d'essai <C> (copie d'essais/env-11/qemu sans build/, graine de projet) ;
#   <E>/gen   : copie de <C> pour les `generate --clangd` qui réussissent (ils écrivent) ;
#   <E>/w-<phase>/<cas> : répertoire courant vide de chaque cas hors <C> ;
#   <E>/cibles-<phase>  : chemins visés par seed new -C, --seed-repo, scion new --repo ;
#   <E>/releves/<phase> : relevés bruts ; <sortie versionnée> : relevés normalisés + resume.tsv.
# Formes (chemin transmis tel quel, comme un appel en liste : forme de l'extension) :
#   t `~/…`   u `~<U>/…`   x `~inconnu63/…` (utilisateur sans compte)   r relatif   a absolu
#   d `~/…` développé par bash (mot non cité)   z tapé dans zsh, `--option=~/…` (non développé)
# Chemins : p1 -C (rootstock.py, check)    p2 seed new -C    p3 --seed-repo    p4 scion new --repo
#           p5 _locate (files.py : file owner ; p5add file add, p5dir dir add, p5graft graft --path)
#           p6 generate --clangd    hors des 6 : c1 check FILE, m1 seed mkconf import PATH
# Après chaque cas : état de <C> comparé au départ (env-55-url-file/etat.sh), clones de <C>,
# arborescence du répertoire courant, présence d'un `<cwd>/~*`, existence de la cible.
set -u
export LC_ALL=C
E=$1 phase=$2 vers=$3
here=$(cd "$(dirname "$0")" && pwd)
RL=$here/../env-51-messages/releve.sh
ETAT=$here/../env-55-url-file/etat.sh
U=$(id -un)
C=$E/rs G=$E/gen W=$E/w-$phase T=$E/cibles-$phase brut=$E/releves/$phase
case $E in "$HOME"/lepton-tools-dev/essais/?*) ;; *) echo "$E hors d'essais/" >&2; exit 2 ;; esac
id inconnu63 >/dev/null 2>&1 && { echo "l'utilisateur inconnu63 existe" >&2; exit 2; }
for d in "$W" "$T" "$brut"; do [ -e "$d" ] && { echo "$d existe déjà" >&2; exit 2; }; done
[ -d "$C/trunk" ] || { echo "$C : rootstock d'essai absent" >&2; exit 2; }
[ -d "$G/trunk" ] || rsync -a "$C/" "$G/"
mkdir -p "$W" "$T" "$brut" "$vers" "$W/outils"
ln -s "$(command -v clangd-mp-21)" "$W/outils/clangd"
develop() { bash -c "printf '%s' $1"; }
relpath() { python3 -c 'import os,sys;print(os.path.relpath(sys.argv[1],sys.argv[2]))' "$1" "$2"; }
hT=${T#"$HOME"/} hC=${C#"$HOME"/} hW=${W#"$HOME"/}
bash "$ETAT" "$C" "$brut/etat-depart" >"$brut/depart.etat"
clones() { for c in original family-qemu-mps2 bsp-qemu-mps2-an386; do
  printf '%s %s %s\n' "$c" "$(git -C "$C/depots/lepton/$c/master" rev-parse --short HEAD)" \
    "$(git -C "$C/depots/lepton/$c/master" status --short | wc -l | tr -d ' ')"; done; }
clones >"$brut/clones-depart.txt"
printf 'cas\tchemin\tforme\tcode\tcwd/~*\tcible\tC\tmessage\n' >"$brut/resume.tsv"

# cas <nom> <chemin> <forme> <cwd> <cible ou -> <commande…>
cas() {
  local nom=$1 chemin=$2 forme=$3 dir=$4 cible=$5 f tilde etatC msg
  shift 5
  mkdir -p "$dir"
  bash "$RL" "$brut" "$nom" "$dir" "$@" >>"$brut/journal.txt" 2>&1
  (cd "$dir" && find . -mindepth 1 -maxdepth 6 ! -path '*/.git/*' ! -path './trunk/*' ! -path './depots/*' \
    ! -path './build/*' ! -path './*/*/*/*/*/*/*' | sort) >"$brut/$nom.W"
  tilde=$(cd "$dir" && ls -d ./~* 2>/dev/null | tr '\n' ' '); tilde=${tilde:-non}
  if [ "$cible" = - ]; then cible=-; elif [ -e "$cible" ]; then cible=créée; else cible=absente; fi
  bash "$ETAT" "$C" "$brut/etat-$nom" >/dev/null
  for f in liens casses reguliers graine grafted depots; do
    cmp -s "$brut/etat-depart/$f.txt" "$brut/etat-$nom/$f.txt" && printf '%s = départ\n' "$f" \
      || printf '%s ≠ départ\n' "$f"
  done >"$brut/$nom.etat"
  clones >"$brut/clones-$nom.txt"
  cmp -s "$brut/clones-depart.txt" "$brut/clones-$nom.txt" && echo "clones = départ" >>"$brut/$nom.etat" \
    || echo "clones ≠ départ" >>"$brut/$nom.etat"
  etatC=$(grep -v ' = départ$' "$brut/$nom.etat" | tr '\n' ' '); etatC=${etatC:-=}
  msg=$(grep -m1 -E 'lepton:|Erreur|erreur|Traceback|introuvable|rootstock' "$brut/$nom.err" | cut -c1-160)
  [ -n "$msg" ] || msg=$(head -1 "$brut/$nom.out" | cut -c1-160)
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$nom" "$chemin" "$forme" "$(cat "$brut/$nom.code")" \
    "$tilde" "$cible" "$etatC" "$msg" >>"$brut/resume.tsv"
  printf '%s\tcode %s\t~:%s\tcible:%s\tC:%s\n' "$nom" "$(cat "$brut/$nom.code")" "$tilde" "$cible" "$etatC"
}

F=(t u x a d)
forme() {  # <t|u|x|a|d> <chemin absolu sous HOME> → mot transmis (r calculé par l'appelant)
  local h=${2#"$HOME"/}
  case $1 in t) printf '%s' "~/$h" ;; u) printf '%s' "~$U/$h" ;; x) printf '%s' "~inconnu63/$h" ;;
    a) printf '%s' "$2" ;; d) develop "~/$h" ;; esac
}

NEW=(--bsp qemu-mps2-an386 --backend freertos --mkconf sys/user/tauon-basic/etc/mkconf_tauon_basic_qemu_mps2.xml
     --origin "lepton-noyau=$C/depots/lepton/original/master"
     --origin "qemu-mps2=$C/depots/lepton/family-qemu-mps2/master"
     --origin "qemu-mps2-an386=$C/depots/lepton/bsp-qemu-mps2-an386/master")

# p1 : -C DIR (check, lecture seule)
for f in "${F[@]}"; do cas p1-$f "-C" $f "$W/p1-$f" - lepton check -C "$(forme $f "$C")"; done
cas p1-r "-C" r "$W/p1-r" - lepton check -C "$(relpath "$C" "$W/p1-r")"
cas p1-z "-C" z "$W/p1-z" - zsh -c "lepton check --rootstock=~/$hC"

# p2 : seed new -C DIR (graine par défaut sous DIR)
for f in "${F[@]}"; do v=$(forme $f "$T/n2-$f")
  cas p2-$f "seed new -C" $f "$W/p2-$f" "$T/n2-$f" lepton seed new env63 -C "$v" "${NEW[@]}"; done
mkdir -p "$W/p2-r"
cas p2-r "seed new -C" r "$W/p2-r" "$T/n2-r" lepton seed new env63 -C "$(relpath "$T/n2-r" "$W/p2-r")" "${NEW[@]}"

# p3 : --seed-repo DIR (rootstock -C absolu)
for f in "${F[@]}"; do v=$(forme $f "$T/g3-$f")
  cas p3-$f "--seed-repo" $f "$W/p3-$f" "$T/g3-$f" lepton seed new env63 -C "$T/n3-$f" --seed-repo "$v" "${NEW[@]}"; done
mkdir -p "$W/p3-r"
cas p3-r "--seed-repo" r "$W/p3-r" "$T/g3-r" lepton seed new env63 -C "$T/n3-r" \
  --seed-repo "$(relpath "$T/g3-r" "$W/p3-r")" "${NEW[@]}"

# p4 : scion new --repo DIR --no-seed (rootstock <C> par -C absolu)
for f in "${F[@]}"; do v=$(forme $f "$T/r4-$f")
  cas p4-$f "scion new --repo" $f "$W/p4-$f" "$T/r4-$f" lepton scion new env63$f --type bibliotheque \
    --repo "$v" --no-seed --no-cmake -C "$C"; done
mkdir -p "$W/p4-r"
cas p4-r "scion new --repo" r "$W/p4-r" "$T/r4-r" lepton scion new env63r --type bibliotheque \
  --repo "$(relpath "$T/r4-r" "$W/p4-r")" --no-seed --no-cmake -C "$C"
cas p4-z "scion new --repo" z "$W/p4-z" "$T/r4-z" zsh -c "lepton scion new env63z --type bibliotheque \
--repo=~/$hT/r4-z --no-seed --no-cmake -C $C"

# p5 : _locate (cwd <C>) : file owner (lecture), puis écritures refusées attendues (forme t)
for f in "${F[@]}"; do v=$(forme $f "$C/trunk/CMakeLists.txt")
  cas p5-$f "_locate (file owner)" $f "$C" - lepton file owner "$v" --json; done
cas p5-r "_locate (file owner)" r "$C" - lepton file owner trunk/CMakeLists.txt --json
cas p5add-t "_locate (file add)" t "$C" "$C/trunk/sys/root/src/lib/env63-nouveau.c" \
  lepton file add "~/$hC/trunk/sys/root/src/lib/env63-nouveau.c"
cas p5dir-t "_locate (dir add)" t "$C" "$C/trunk/sys/root/src/lib/env63-rep" \
  lepton dir add "~/$hC/trunk/sys/root/src/lib/env63-rep"
cas p5graft-t "_locate (graft --path)" t "$C" - lepton graft --path "~/$hC/trunk/CMakeLists.txt" --no-cmake

# p6 : generate --clangd PATH ; refus attendus dans <C> (t, u, x), réussites dans <G> (a, d, r, nom)
for f in "${F[@]}"; do v=$(forme $f "$W/outils/clangd")
  case $f in t|u|x) dir=$C ;; *) dir=$G ;; esac
  cas p6-$f "generate --clangd" $f "$dir" - lepton generate --clangd "$v"
  [ "$dir" = "$G" ] && grep -h '"clangd.path"' "$G"/*.code-workspace >"$brut/p6-$f.clangd"; done
cas p6-r "generate --clangd" r "$G" - lepton generate --clangd "$(relpath "$W/outils/clangd" "$G")"
grep -h '"clangd.path"' "$G"/*.code-workspace >"$brut/p6-r.clangd"
cas p6-n "generate --clangd" nom "$G" - lepton generate --clangd clangd-mp-21
grep -h '"clangd.path"' "$G"/*.code-workspace >"$brut/p6-n.clangd"

# hors des 6 : check FILE (lecture), seed mkconf import PATH (forme t : refus attendu)
GJ=depots/lepton-seed/env11/scion/.scion/lepton-graine.json
cas c1-t "check FILE" t "$W/c1-t" - lepton check "~/$hC/$GJ"
cas c1-a "check FILE" a "$W/c1-a" - lepton check "$C/$GJ"
cas m1-t "seed mkconf import" t "$C" - lepton seed mkconf import \
  "~/$hC/trunk/sys/user/tauon-basic/etc/mkconf_tauon_basic_qemu_mps2.xml"

for f in "$brut"/*.cmd "$brut"/*.out "$brut"/*.err "$brut"/*.code "$brut"/*.etat "$brut"/*.W \
         "$brut"/*.clangd "$brut"/resume.tsv; do
  [ -e "$f" ] || continue
  sed -e "s#$W#<W>#g" -e "s#$T#<T>#g" -e "s#$G#<G>#g" -e "s#$C#<C>#g" -e "s#$hW#<hW>#g" -e "s#$hT#<hT>#g" \
      -e "s#$hC#<hC>#g" -e "s#$HOME#<HOME>#g" -e "s#~$U/#~<U>/#g" -e "s#/~$U#/~<U>#g" "$f" >"$vers/$(basename "$f")"
done
