#!/usr/bin/env bash
# ENV-59 : `lepton seed add` des origines locales (`~/…`, `~<U>/…`, relative, absolue, formes `~`
# développées par bash, `~inconnu59/…` d'un utilisateur sans compte), nues, avec `@master` et avec
# `--version master` (cas p01-p21, a01-a21), sur un rootstock d'essai
# à graine de projet (jamais <ROOTSTOCK>). Reprend env-55-url-file/essai.sh (D17).
# Usage : essai.sh <rootstock d'essai> <dépôt présent> <dépôt absent> <sortie brute> <sortie versionnée>
#
# L'origine est passée entre guillemets : lepton la reçoit telle quelle, comme d'un appel en liste
# (forme de l'extension). Les formes « développé » sont le mot développé par bash (non cité).
# Un refus qui porte un indice `file://localhost…` est suivi tel quel (cas `<nom>-i`).
# Chaque cas est relevé par env-51-messages/releve.sh ; un ajout réussi est annulé par `seed remove`
# (`--purge` si scion a cloné) ; l'état du rootstock (env-55-url-file/etat.sh) est comparé au départ
# après chaque cas. Sortie versionnée : relevés normalisés (<C>, <P>, <A>, <HOME>, ~<U>).
set -u
export LC_ALL=C
C=$1 P=$2 A=$3 brut=$4 vers=$5
here=$(cd "$(dirname "$0")" && pwd)
RL=$here/../env-51-messages/releve.sh
ETAT=$here/../env-55-url-file/etat.sh
U=$(id -un)
case $P in "$HOME"/*) ;; *) echo "dépôt présent hors de HOME" >&2; exit 2 ;; esac
case $A in "$HOME"/*) ;; *) echo "dépôt absent hors de HOME" >&2; exit 2 ;; esac
id inconnu59 >/dev/null 2>&1 && { echo "l'utilisateur inconnu59 existe" >&2; exit 2; }
relpath() { python3 -c 'import os,sys;print(os.path.relpath(sys.argv[1],sys.argv[2]))' "$1" "$2"; }
develop() { bash -c "printf '%s' $1"; }   # mot développé par bash, non cité
mkdir -p "$brut" "$vers"
bash "$ETAT" "$C" "$brut/etat-depart" >"$brut/depart.etat"

cas() {  # <nom> <commande…> : relevé de la commande, lancée dans <C>
  local nom=$1; shift
  bash "$RL" "$brut" "$nom" "$C" "$@" >>"$brut/journal.txt" 2>&1
  printf '%s\tcode %s\t%s\n' "$nom" "$(cat "$brut/$nom.code")" "$*"
}

etat() {  # <nom> : état comparé au départ (liens, cassés, réguliers, graine, grafted, depots/)
  local nom=$1 f
  bash "$ETAT" "$C" "$brut/etat-$nom" >/dev/null
  for f in liens casses reguliers graine grafted depots; do
    if cmp -s "$brut/etat-depart/$f.txt" "$brut/etat-$nom/$f.txt"; then
      printf '%s = départ\n' "$f"
    else
      printf '%s ≠ départ (%s lignes de diff)\n' "$f" "$(diff "$brut/etat-depart/$f.txt" "$brut/etat-$nom/$f.txt" | grep -c '^[<>]')"
    fi
  done >"$brut/$nom.etat"
  printf '  état : %s\n' "$(grep -v ' = départ$' "$brut/$nom.etat" | tr '\n' ';')"
}

ajout() {  # <nom> <origine> [options…] : seed add de env59lib, annulé par seed remove s'il réussit
  local nom=$1 origine=$2 purge=""; shift 2
  cas "$nom" lepton seed add env59lib "$origine" --type bibliotheque --no-cmake "$@"
  if [ "$(cat "$brut/$nom.code")" = 0 ]; then
    [ -d "$C/depots/lepton/library-env59lib/master/.git" ] && purge=--purge
    cas "$nom-status" lepton seed status --json
    cas "$nom-check" lepton check
    cas "$nom-remove" lepton seed remove env59lib --no-cmake $purge
  fi
  etat "$nom"
}

absent() {  # <nom> <origine> [options…]
  local nom=$1; shift
  cas "$nom" lepton seed add absent "$@" --type bibliotheque --no-cmake
  etat "$nom"
}

suivre() {  # <nom> <fonction> : indice du refus <nom> suivi tel quel, s'il y en a un
  local nom=$1 f=$2 url
  url=$(grep -o 'file://localhost[^[:space:]]*' "$brut/$nom.err" | head -1)
  [ -n "$url" ] && "$f" "$nom-i" "$url"
  return 0
}

serie() {  # <préfixe p|a> <fonction ajout|absent> <cible absolue>
  # par forme : nue, @master, --version master ; formes « dev » : mot entier développé par bash
  local px=$1 f=$2 t=$3 under n=0 forme base dev v arg nom
  under=${t#"$HOME"/}
  for forme in tilde tilde-u relatif absolu tilde-dev tilde-u-dev tilde-inconnu; do
    dev=""
    case $forme in
      tilde-inconnu) base="~inconnu59/$under" ;;   # utilisateur sans compte (id inconnu59 : échec)
      tilde) base="~/$under" ;;
      tilde-u) base="~$U/$under" ;;
      relatif) base=$(relpath "$t" "$C") ;;
      absolu) base=$t ;;
      tilde-dev) base="~/$under" dev=1 ;;
      tilde-u-dev) base="~$U/$under" dev=1 ;;
    esac
    for v in nue at opt; do
      n=$((n + 1)); nom=$(printf '%s%02d' "$px" "$n")
      arg=$base; [ "$v" = at ] && arg="$base@master"
      [ -n "$dev" ] && arg=$(develop "$arg")
      if [ "$v" = opt ]; then "$f" "$nom" "$arg" --version master; else "$f" "$nom" "$arg"; fi
      [ "$v" = nue ] || suivre "$nom" "$f"
    done
  done
}

serie p ajout "$P"
serie a absent "$A"

# --- sortie versionnée : relevés normalisés
for f in "$brut"/*.cmd "$brut"/*.out "$brut"/*.err "$brut"/*.code "$brut"/*.etat; do
  sed -e "s#$C#<C>#g" -e "s#$P#<P>#g" -e "s#$A#<A>#g" -e "s#$HOME#<HOME>#g" -e "s#~$U/#~<U>/#g" \
    "$f" >"$vers/$(basename "$f")"
done
