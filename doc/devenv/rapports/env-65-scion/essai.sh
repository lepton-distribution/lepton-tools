#!/usr/bin/env bash
# ENV-65 : `lepton seed add` d'une clé dont le clone existe déjà hors de sa version (D25), sur un
# rootstock d'essai à graine de projet (jamais <ROOTSTOCK>).
# Usage : essai.sh <rootstock d'essai> <dépôt env65lib> <sortie brute> <sortie versionnée>
#
# Le dépôt a deux branches : master et dev. Préparation (hors scion, consignée dans prep.txt) :
# clone de <P> sans -b sous depots/lepton/library-env65lib/dev, donc sur master (forme du clone
# laissé par scion ≤ 0.6.3.1, l03 d'ENV-60). Cas :
#   l01 : lepton seed add env65lib <P>@dev : le clone existant est repris (0.6.3.2) ou refusé ;
#   l02 : l01 relancé ;
#   l03 : clone remis sur dev (témoin à sa version) : seed add, puis seed remove --purge.
# Le scion lancé est celui du PATH (lepton le trouve aussi par le PATH). Relevés par
# env-51-messages/releve.sh ; état du rootstock (env-55-url-file/etat.sh) comparé au départ, pris
# avant la préparation, et état du clone de la clé. Sortie versionnée : relevés normalisés
# (<C>, <P>, <HOME>).
set -u
export LC_ALL=C
C=$1 P=$2 brut=$3 vers=$4
here=$(cd "$(dirname "$0")" && pwd)
RL=$here/../env-51-messages/releve.sh
ETAT=$here/../env-55-url-file/etat.sh
URL=file://localhost$P
K=depots/lepton/library-env65lib
mkdir -p "$brut" "$vers"
py=$(dirname "$(realpath "$(command -v scion)")")/python
{ command -v scion; "$py" -c 'import scion; print(scion.__version__)'; } >"$brut/scion.txt"
bash "$ETAT" "$C" "$brut/etat-depart" >"$brut/depart.etat"

cas() {  # <nom> <commande…> : relevé de la commande, lancée dans <C>
  local nom=$1; shift
  bash "$RL" "$brut" "$nom" "$C" "$@" >>"$brut/journal.txt" 2>&1
  printf '%s\tcode %s\t%s\n' "$nom" "$(cat "$brut/$nom.code")" "$*"
}

etat() {  # <nom> : état comparé au départ, puis clones de la clé et contenu greffé
  local nom=$1 f d
  bash "$ETAT" "$C" "$brut/etat-$nom" >/dev/null
  for f in liens casses reguliers graine grafted depots; do
    if cmp -s "$brut/etat-depart/$f.txt" "$brut/etat-$nom/$f.txt"; then
      printf '%s = départ\n' "$f"
    else
      printf '%s ≠ départ (%s lignes de diff)\n' "$f" "$(diff "$brut/etat-depart/$f.txt" "$brut/etat-$nom/$f.txt" | grep -c '^[<>]')"
      diff "$brut/etat-depart/$f.txt" "$brut/etat-$nom/$f.txt" | grep '^[<>]' | head -5 | sed 's/^/    /'
    fi
  done >"$brut/$nom.etat"
  for d in "$C/$K"/*/; do
    [ -d "$d/.git" ] || continue
    printf 'clone %s : branche %s ; HEAD = %s\n' "${d%/}" \
      "$(git -C "$d" branch --show-current || true)" \
      "$(git -C "$d" for-each-ref --points-at HEAD --format='%(refname)' | tr '\n' ' ')"
  done >>"$brut/$nom.etat"
  find "$C/trunk" -name DEV.txt -type l >>"$brut/$nom.etat"   # présent : contenu de dev greffé
  printf '  état : %s\n' "$(grep -v ' = départ$' "$brut/$nom.etat" | tr '\n' ';')"
}

# --- préparation : clone sans -b, sur master, à l'emplacement de la version dev
mkdir -p "$C/$K"
git -C "$C/$K" clone -q "$URL" dev
printf '(cd %s) git clone -q %s dev\n' "$C/$K" "$URL" >"$brut/prep.txt"
etat prep

# --- l01, l02 : clone existant hors de sa version
cas l01 lepton seed add env65lib "$URL@dev" --type bibliotheque --no-cmake
etat l01
cas l02 lepton seed add env65lib "$URL@dev" --type bibliotheque --no-cmake
etat l02

# --- l03 : témoin, clone remis à sa version (seulement si l01 a été refusé)
if [ "$(cat "$brut/l01.code")" != 0 ]; then
  git -C "$C/$K/dev" checkout -q dev
  printf '(cd %s) git checkout -q dev\n' "$C/$K/dev" >>"$brut/prep.txt"
  cas l03 lepton seed add env65lib "$URL@dev" --type bibliotheque --no-cmake
  etat l03
  cas l03-check lepton check
  cas l03-remove lepton seed remove env65lib --no-cmake --purge
  etat l03-remove
fi

for f in "$brut"/*.cmd "$brut"/*.out "$brut"/*.err "$brut"/*.code "$brut"/*.etat "$brut"/scion.txt \
         "$brut"/prep.txt; do
  [ -f "$f" ] || continue
  sed -e "s#$C#<C>#g" -e "s#$P#<P>#g" -e "s#$HOME#<HOME>#g" "$f" >"$vers/$(basename "$f")"
done
