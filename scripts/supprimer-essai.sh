#!/usr/bin/env bash
# Enveloppe de suppression des essais (ENV-54, D16, PA-95).
#
# Usage : scripts/supprimer-essai.sh [-n] <cible>...
#   -n  essai à blanc : affiche les cibles acceptées, ne supprime rien.
#
# Chaque cible est résolue (liens des répertoires parents suivis, `.` et `..` réduits ; le dernier
# composant n'est pas suivi, comme `rm`). Cibles acceptées :
#   - un descendant strict de ~/lepton-tools-dev/essais/, hors des références ci-dessous, hors
#     d'un trunk/ et d'un depots/tiers/ ;
#   - <rootstock>/build/<preset>, où <rootstock> (signature scion présente) est ~/lepton ou un
#     descendant d'essais/ (références comprises) ;
#   - ~/env-<N>-journaux, ~/tmp-pytest, ~/tmp-tests.
# Toute autre cible est refusée, de même qu'une cible absente. Tout ou rien : si une cible est
# refusée, rien n'est supprimé.
# Codes de retour : 0 supprimé (ou accepté avec -n), 1 usage, 2 refus.
# Une règle `allow` de .claude/settings.json autorise ce script sans le classifieur de Claude
# Code ; la suppression directe par `rm -rf` reste jugée par le classifieur.
set -u

# Références protégées (premier composant sous essais/) : Mac et VM.
REFERENCES="archives env-9 env-11 env-13-vierge env-40-publication env-40-miroirs env-13-debian env-28-debian env-53-c5"

nom="supprimer-essai"

usage() {
  echo "usage : $nom [-n] <cible>..." >&2
  exit 1
}

# resoudre <chemin> : chemin absolu de l'entrée, répertoires parents résolus par `cd -P`,
# composants absents réduits lexicalement. Le dernier composant n'est pas suivi.
resoudre() {
  local p="$1" cur="/" virt=0 dernier c i n suiv
  case "$p" in /*) ;; *) p="$PWD/$p" ;; esac
  while [ "$p" != "/" ] && [ "${p%/}" != "$p" ]; do p="${p%/}"; done
  dernier="${p##*/}"
  p="${p%/*}"
  local IFS=/
  set -f
  # shellcheck disable=SC2206
  local comps=($p)
  set +f
  unset IFS
  n=${#comps[@]}
  i=0
  while [ "$i" -lt "$n" ]; do
    c="${comps[$i]}"
    i=$((i + 1))
    case "$c" in
      "" | .) continue ;;
      ..)
        if [ "$virt" -gt 0 ]; then
          virt=$((virt - 1)); cur="${cur%/*}"; [ -z "$cur" ] && cur="/"
        else
          cur="$(cd -P "$cur/.." 2>/dev/null && pwd -P)" || return 1
        fi
        ;;
      *)
        # Pas de « // » en tête : bash le garde tel quel dans `pwd`.
        if [ "$cur" = "/" ]; then suiv="/$c"; else suiv="$cur/$c"; fi
        if [ "$virt" -eq 0 ] && [ -d "$suiv" ]; then
          cur="$(cd -P "$suiv" 2>/dev/null && pwd -P)" || return 1
        else
          virt=$((virt + 1))
          cur="$suiv"
        fi
        ;;
    esac
  done
  case "$dernier" in "" | . | ..) return 1 ;; esac
  if [ "$cur" = "/" ]; then echo "/$dernier"; else echo "$cur/$dernier"; fi
}

# canon_rep <répertoire> : chemin physique d'un répertoire existant, sinon le chemin tel quel.
canon_rep() {
  (cd -P "$1" 2>/dev/null && pwd -P) || echo "$1"
}

est_reference() {
  local r
  for r in $REFERENCES; do [ "$1" = "$r" ] && return 0; done
  return 1
}

# build_accepte <cible résolue> : vrai si <cible> = <rootstock>/build/<preset>.
build_accepte() {
  local c="$1" parent rs
  parent="${c%/*}"
  [ "${parent##*/}" = "build" ] || return 1
  rs="${parent%/*}"
  [ -e "$rs/.scion.rootstock.signature" ] || return 1
  [ "$rs" = "$H/lepton" ] && return 0
  case "$rs/" in "$E"/?*) return 0 ;; esac
  return 1
}

# juger <cible brute> : écrit la cible résolue si elle est acceptée, sinon la raison ; code 0/2.
juger() {
  local brute="$1" c rel n1
  [ -n "$brute" ] || { echo "cible vide"; return 2; }
  c="$(resoudre "$brute")" || { echo "cible non résoluble (., .. ou racine)"; return 2; }
  if build_accepte "$c"; then
    :
  else
    case "$c" in
      "$E"/?*)
        rel="${c#"$E"/}"
        n1="${rel%%/*}"
        case "/$rel/" in
          */trunk/* | */depots/tiers/*) echo "sous un trunk/ ou un depots/tiers/ : $c"; return 2 ;;
        esac
        if est_reference "$n1"; then echo "essai de référence protégé ($n1) : $c"; return 2; fi
        ;;
      "$H"/env-*-journaux)
        n1="${c#"$H"/env-}"; n1="${n1%-journaux}"
        case "$n1" in "" | *[!0-9]*) echo "hors des bornes : $c"; return 2 ;; esac
        ;;
      "$H/tmp-pytest" | "$H/tmp-tests") ;;
      *) echo "hors des bornes : $c"; return 2 ;;
    esac
  fi
  if [ ! -e "$c" ] && [ ! -L "$c" ]; then echo "cible absente : $c"; return 2; fi
  echo "$c"
  return 0
}

blanc=0
if [ "${1:-}" = "-n" ]; then blanc=1; shift; fi
[ "$#" -ge 1 ] || usage
[ -n "${HOME:-}" ] || { echo "$nom : HOME non défini" >&2; exit 2; }

H="$(canon_rep "$HOME")"
E="$(canon_rep "$H/lepton-tools-dev/essais")"

acceptees=()
refus=0
for brute in "$@"; do
  if res="$(juger "$brute")"; then
    acceptees+=("$res")
  else
    echo "$nom : refusé : $brute ($res)" >&2
    refus=1
  fi
done
if [ "$refus" -ne 0 ]; then
  echo "$nom : rien n'a été supprimé" >&2
  exit 2
fi

for c in "${acceptees[@]}"; do
  if [ "$blanc" -eq 1 ]; then
    echo "accepté (à blanc) : $c"
  else
    rm -rf -- "$c" || { echo "$nom : échec de rm sur $c" >&2; exit 2; }
    echo "supprimé : $c"
  fi
done
exit 0
