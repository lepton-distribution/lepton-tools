#!/usr/bin/env bash
# ENV-56 : clonages en échec sur un rootstock d'essai à graine de projet (jamais <ROOTSTOCK>).
# Usage : essai.sh <rootstock d'essai> <dépôt absent> <sortie brute> <sortie versionnée>
#
# Le scion lancé est celui du PATH (lepton le trouve aussi par le PATH) : pour la branche, mettre
# le bin/ du venv en tête du PATH de la commande. Chaque cas est relevé par
# env-51-messages/releve.sh (.cmd, .out, .err, .code). Après chaque cas, l'état du rootstock
# (env-55-url-file/etat.sh) est comparé à l'état de départ. Un répertoire nouveau et vide (D14)
# est noté « résidu » dans <cas>.etat, puis retiré par rmdir, pour que le cas suivant parte du
# même état. Ce que le cas a préparé lui-même (parent préexistant) est noté « préexistant
# gardé » ou « préexistant retiré », puis défait.
# La sortie versionnée reçoit les relevés, chemins remplacés par <C> (rootstock), <A> (dépôt
# absent) et <HOME>.
set -u
export LC_ALL=C
C=$1 A=$2 brut=$3 vers=$4
here=$(cd "$(dirname "$0")" && pwd)
RL=$here/../env-51-messages/releve.sh
ETAT=$here/../env-55-url-file/etat.sh
SEED=depots/lepton-seed/env11
URL=file://localhost$A
mkdir -p "$brut" "$vers"
py=$(dirname "$(realpath "$(command -v scion)")")/python  # python du venv (pipx ou essai)
{ command -v scion; "$py" -c 'import scion; print(scion.__version__, scion.__file__)'; } >"$brut/scion.txt"
bash "$ETAT" "$C" "$brut/etat-depart" >"$brut/depart.etat"

cas() {  # <nom> <commande…> : relevé de la commande, lancée dans <C>
  local nom=$1; shift
  bash "$RL" "$brut" "$nom" "$C" "$@" >>"$brut/journal.txt" 2>&1
  printf '%s\tcode %s\t%s\n' "$nom" "$(cat "$brut/$nom.code")" "$*"
}

preparer() {  # <nom> <répertoire relatif à <C>> [vide|temoin] : parent préexistant du cas
  local nom=$1 d=$2 forme=${3:-vide}
  mkdir -p "$C/$d"
  [ "$forme" = temoin ] && printf 'autre version\n' >"$C/$d/temoin"
  printf '%s\t%s\n' "$d" "$forme" >"$brut/$nom.prep"
}

defaire() {  # <nom> : défait ce que preparer a créé, après le relevé
  local nom=$1 d forme
  [ -f "$brut/$nom.prep" ] || return 0
  IFS=$'\t' read -r d forme <"$brut/$nom.prep"
  [ "$forme" = temoin ] && rm -f "$C/$d/temoin"
  while [ "$d" != depots ] && [ -d "$C/$d" ] && [ -z "$(ls -A "$C/$d")" ] \
        && ! grep -qx "$d" "$brut/etat-depart/depots.txt"; do
    rmdir "$C/$d"; d=$(dirname "$d")
  done
}

etat() {  # <nom> : résidus relevés puis retirés ; état comparé au départ
  local nom=$1 d f prep=""
  [ -f "$brut/$nom.prep" ] && prep=$(cut -f1 "$brut/$nom.prep")
  bash "$ETAT" "$C" "$brut/etat-$nom" >/dev/null
  : >"$brut/$nom.etat"
  if [ -n "$prep" ]; then
    if [ -d "$C/$prep" ]; then
      printf 'préexistant gardé : %s (%s)\n' "$prep" "$(ls -A "$C/$prep" | tr '\n' ' ')"
    else
      printf 'préexistant retiré : %s\n' "$prep"
    fi >>"$brut/$nom.etat"
  fi
  comm -13 "$brut/etat-depart/depots.txt" "$brut/etat-$nom/depots.txt" | while IFS= read -r d; do
    if [ -n "$prep" ]; then  # la préparation, ses ancêtres et son contenu ne sont pas du cas
      case "$prep/" in "${d% (vide)}/"*) continue ;; esac
      case "${d% (vide)}" in "$prep"/*) continue ;; esac
    fi
    case $d in
      *" (vide)") printf 'résidu : %s\n' "${d% (vide)}" ;;
      *) printf 'nouveau répertoire non vide : %s\n' "$d" ;;
    esac
  done >>"$brut/$nom.etat"
  defaire "$nom"
  # résidus vides : retirés du plus profond au moins profond (hors préparation, déjà défaite)
  for d in $(comm -13 "$brut/etat-depart/depots.txt" "$brut/etat-$nom/depots.txt" \
             | grep ' (vide)$' | sed 's/ (vide)$//' | sort -r); do
    while [ "$d" != depots ] && [ -d "$C/$d" ] && [ -z "$(ls -A "$C/$d")" ] \
          && ! grep -qx "$d" "$brut/etat-depart/depots.txt"; do
      rmdir "$C/$d" && printf 'rmdir %s\n' "$d" >>"$brut/$nom.etat"
      d=$(dirname "$d")
    done
  done
  bash "$ETAT" "$C" "$brut/etat-$nom-fin" >/dev/null
  for f in liens casses reguliers graine grafted depots; do
    if cmp -s "$brut/etat-depart/$f.txt" "$brut/etat-$nom-fin/$f.txt"; then
      printf '%s = départ\n' "$f"
    else
      printf '%s ≠ départ (%s lignes de diff)\n' "$f" "$(diff "$brut/etat-depart/$f.txt" "$brut/etat-$nom-fin/$f.txt" | grep -c '^[<>]')"
    fi
  done >>"$brut/$nom.etat"
  printf '  état : %s\n' "$(grep -v ' = départ$' "$brut/$nom.etat" | tr '\n' ';')"
}

# --- e01 : lepton seed add, étagère existante (lepton), greffon nouveau
cas e01 lepton seed add absent "$URL" --type bibliotheque --no-cmake
etat e01

# --- e02 : même ajout par scion lancé à la main, annulé par seed-scion-remove
cas e02a scion seed-scion-add --seed "$SEED" lepton@library-absent master "$URL"
cas e02b scion seed-clone --seed "$SEED"
cas e02c scion seed-scion-remove --seed "$SEED" lepton@library-absent
etat e02c

# --- e03 : scion à la main, étagère nouvelle (essai)
cas e03a scion seed-scion-add --seed "$SEED" essai@absent master "$URL"
cas e03b scion seed-clone --seed "$SEED"
cas e03c scion seed-scion-remove --seed "$SEED" essai@absent
etat e03c

# --- e04 : parent préexistant qui porte une autre version (non vide)
preparer e04 depots/lepton/library-absent/autre temoin
cas e04 lepton seed add absent "$URL" --type bibliotheque --no-cmake
etat e04

# --- e05 : parent préexistant vide (résidu d'un échec antérieur)
preparer e05 depots/lepton/library-absent vide
cas e05 lepton seed add absent "$URL" --type bibliotheque --no-cmake
etat e05

# --- e06 : graine distante absente (seed-add, _clone_seed)
cas e06 scion seed-add "$URL"
etat e06

# --- sortie versionnée : relevés normalisés
for f in "$brut"/*.cmd "$brut"/*.out "$brut"/*.err "$brut"/*.code "$brut"/*.etat "$brut"/*.prep "$brut"/scion.txt; do
  [ -f "$f" ] || continue
  sed -e "s#$C#<C>#g" -e "s#$A#<A>#g" -e "s#$HOME#<HOME>#g" "$f" >"$vers/$(basename "$f")"
done
