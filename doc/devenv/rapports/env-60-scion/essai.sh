#!/usr/bin/env bash
# ENV-60 : `lepton seed add` d'une clé dont le checkout ne mène pas à la version déclarée (D18),
# sur un rootstock d'essai à graine de projet (jamais <ROOTSTOCK>).
# Usage : essai.sh <rootstock d'essai> <dépôt présent> <sortie brute> <sortie versionnée>
#
# Cas :
#   l01 : version qui n'est qu'un chemin du dépôt (@scion) ; s'il réussit : status, check, remove ;
#   l02 : version absente (@nope) : checkout en échec, message relayé, annulation de lepton ;
#   l03 : l02 relancé (passage suivant), clone de l02 en place.
# Le scion lancé est celui du PATH (lepton le trouve aussi par le PATH). Relevés par
# env-51-messages/releve.sh ; état du rootstock (env-55-url-file/etat.sh) comparé au départ après
# chaque cas, et état du clone de la clé (branche, références de HEAD) par git. Le clone laissé
# par l02 n'est pas retiré ici : la session le supprime (scripts/supprimer-essai.sh), puis
# compare l'état au départ. Sortie versionnée : relevés normalisés (<C>, <P>, <HOME>).
set -u
export LC_ALL=C
C=$1 P=$2 brut=$3 vers=$4
here=$(cd "$(dirname "$0")" && pwd)
RL=$here/../env-51-messages/releve.sh
ETAT=$here/../env-55-url-file/etat.sh
URL=file://localhost$P
K=depots/lepton/library-env60lib
mkdir -p "$brut" "$vers"
py=$(dirname "$(realpath "$(command -v scion)")")/python
{ command -v scion; "$py" -c 'import scion; print(scion.__version__)'; } >"$brut/scion.txt"
bash "$ETAT" "$C" "$brut/etat-depart" >"$brut/depart.etat"

cas() {  # <nom> <commande…> : relevé de la commande, lancée dans <C>
  local nom=$1; shift
  bash "$RL" "$brut" "$nom" "$C" "$@" >>"$brut/journal.txt" 2>&1
  printf '%s\tcode %s\t%s\n' "$nom" "$(cat "$brut/$nom.code")" "$*"
}

etat() {  # <nom> : état comparé au départ, puis clones de la clé
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
  printf '  état : %s\n' "$(grep -v ' = départ$' "$brut/$nom.etat" | tr '\n' ';')"
}

# --- l01 : version qui n'est qu'un chemin du dépôt
cas l01 lepton seed add env60lib "$URL@scion" --type bibliotheque --no-cmake
if [ "$(cat "$brut/l01.code")" = 0 ]; then
  etat l01-ajout
  cas l01-status lepton seed status --json
  cas l01-check lepton check
  cas l01-remove lepton seed remove env60lib --no-cmake --purge
fi
etat l01

# --- l02 : version absente
cas l02 lepton seed add env60lib "$URL@nope" --type bibliotheque --no-cmake
etat l02

# --- l03 : passage suivant, clone de l02 en place
cas l03 lepton seed add env60lib "$URL@nope" --type bibliotheque --no-cmake
etat l03

for f in "$brut"/*.cmd "$brut"/*.out "$brut"/*.err "$brut"/*.code "$brut"/*.etat "$brut"/scion.txt; do
  [ -f "$f" ] || continue
  sed -e "s#$C#<C>#g" -e "s#$P#<P>#g" -e "s#$HOME#<HOME>#g" "$f" >"$vers/$(basename "$f")"
done
