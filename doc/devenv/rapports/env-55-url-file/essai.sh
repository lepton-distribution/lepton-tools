#!/usr/bin/env bash
# ENV-55 : essai des formes d'origine sur un rootstock d'essai à graine de projet (jamais <ROOTSTOCK>).
# Usage : essai.sh <rootstock d'essai> <dépôt présent> <dépôt absent> <sortie brute> <sortie versionnée>
#
# Chaque cas est relevé par env-51-messages/releve.sh (.cmd, .out, .err, .code). Après chaque cas
# (et après l'annulation d'un ajout réussi), l'état du rootstock (etat.sh) est comparé à l'état de
# départ : liens du trunk, liens cassés, fichiers réguliers, graine, répertoires de depots/. Un
# répertoire vide nouveau (D14, corrigé en ENV-56) est retiré par rmdir et noté dans <cas>.etat.
# La sortie versionnée reçoit les relevés, chemins remplacés par <C> (rootstock), <P> (dépôt
# présent), <A> (dépôt absent) et <HOME>.
set -u
export LC_ALL=C
C=$1 P=$2 A=$3 brut=$4 vers=$5
here=$(cd "$(dirname "$0")" && pwd)
RL=$here/../env-51-messages/releve.sh
ETAT=$here/etat.sh
SEED=depots/lepton-seed/env11
KEY=lepton@library-env55lib
relpath() { python3 -c 'import os,sys;print(os.path.relpath(sys.argv[1],sys.argv[2]))' "$1" "$2"; }
relA=$(relpath "$A" "$C") relP=$(relpath "$P" "$C")
mkdir -p "$brut" "$vers"
bash "$ETAT" "$C" "$brut/etat-depart" >"$brut/depart.etat"

cas() {  # <nom> <commande…> : relevé de la commande, lancée dans <C>
  local nom=$1; shift
  bash "$RL" "$brut" "$nom" "$C" "$@" >>"$brut/journal.txt" 2>&1
  printf '%s\tcode %s\t%s\n' "$nom" "$(cat "$brut/$nom.code")" "$*"
}

etat() {  # <nom> : état comparé au départ ; répertoires vides nouveaux retirés (D14)
  local nom=$1 d f
  bash "$ETAT" "$C" "$brut/etat-$nom" >/dev/null
  : >"$brut/$nom.etat"
  comm -13 "$brut/etat-depart/depots.txt" "$brut/etat-$nom/depots.txt" | while IFS= read -r d; do
    case $d in
      *" (vide)") d=${d% (vide)}; rmdir "$C/$d" && printf 'rmdir %s (vide, laissé par le cas)\n' "$d" ;;
      *) printf 'nouveau répertoire conservé : %s\n' "$d" ;;
    esac
  done >>"$brut/$nom.etat"
  # parents devenus vides après rmdir
  for d in $(comm -13 "$brut/etat-depart/depots.txt" "$brut/etat-$nom/depots.txt" | sed 's/ (vide)$//' | sort -r); do
    while [ "$d" != "depots" ] && [ -d "$C/$d" ] && [ -z "$(ls -A "$C/$d")" ] && ! grep -qx "$d" "$brut/etat-depart/depots.txt"; do
      rmdir "$C/$d" && printf 'rmdir %s (devenu vide)\n' "$d" >>"$brut/$nom.etat"
      d=$(dirname "$d")
    done
  done
  bash "$ETAT" "$C" "$brut/etat-$nom" >/dev/null
  for f in liens casses reguliers graine grafted depots; do
    if cmp -s "$brut/etat-depart/$f.txt" "$brut/etat-$nom/$f.txt"; then
      printf '%s = départ\n' "$f"
    else
      printf '%s ≠ départ (%s lignes de diff)\n' "$f" "$(diff "$brut/etat-depart/$f.txt" "$brut/etat-$nom/$f.txt" | grep -c '^[<>]')"
    fi
  done >>"$brut/$nom.etat"
  printf '  état : %s\n' "$(grep -v ' = départ$' "$brut/$nom.etat" | tr '\n' ';')"
}

ajout() {  # <nom> <origine> [options…] : seed add de env55lib, annulé par seed remove s'il réussit
  local nom=$1 origine=$2 purge=$3; shift 3
  cas "$nom" lepton seed add env55lib "$origine" --type bibliotheque --no-cmake "$@"
  if [ "$(cat "$brut/$nom.code")" = 0 ]; then
    cas "$nom-status" lepton seed status --json
    cas "$nom-check" lepton check
    cas "$nom-remove" lepton seed remove env55lib --no-cmake $purge
  fi
  etat "$nom"
}

absent() {  # <nom> <origine> [options…]
  local nom=$1; shift
  cas "$nom" lepton seed add absent "$@" --type bibliotheque --no-cmake
  etat "$nom"
}

# --- origine absente
absent a01 "file://$A"
absent a02 "file://localhost$A"
absent a03 "file:$A"
absent a04 "file://autre$A"
absent a05 "FILE://$A"
absent a06 "FILE://localhost$A"
absent a07 "$A"
absent a08 "$relA"
absent a09 "file://$A" --version master            # forme de l'extension (seedAdd)
absent a10 "file://localhost$A" --version master   # forme de l'extension (seedAdd)

# --- origine présente (ajout annulé s'il réussit ; --purge pour un clone fait par scion)
ajout p01 "file://$P" ""
ajout p02 "file://$P" "" --version master
ajout p03 "file://localhost$P" --purge
ajout p04 "file://autre$P" --purge
ajout p05 "FILE://localhost$P" --purge
ajout p06 "FILE://$P" ""
ajout p07 "file:$P" ""
ajout p08 "$P" ""
ajout p09 "$relP" ""
ajout p10 "file://localhost$P" --purge --version master   # forme de l'extension (seedAdd)

# --- scion seul, origine file:/// transmise telle quelle (ce que ferait lepton sans normalisation)
cas s01 scion seed-scion-add --seed "$SEED" "$KEY" master "file://$P"
cas s02 scion seed-clone --seed "$SEED"
cas s03 scion graft --scion "$KEY"
cas s04 scion graft-remove "$KEY"
cas s05 scion seed-scion-remove --seed "$SEED" "$KEY"
etat s05

# --- sortie versionnée : relevés normalisés
for f in "$brut"/*.cmd "$brut"/*.out "$brut"/*.err "$brut"/*.code "$brut"/*.etat; do
  sed -e "s#$C#<C>#g" -e "s#$P#<P>#g" -e "s#$A#<A>#g" -e "s#$HOME#<HOME>#g" "$f" >"$vers/$(basename "$f")"
done
