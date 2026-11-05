#!/usr/bin/env bash
# verifier-import.sh — vérifie qu'une copie de code tiers est identique à une révision amont.
#
# Usage : verifier-import.sh [--liste-seule] <clone> <révision> <répertoire> [<liste>]
#
#   <clone>       clone git du dépôt amont (hors du rootstock)
#   <révision>    commit ou tag de la copie (résolu en commit)
#   <répertoire>  racine de la copie dans le clone du greffon ; un fichier <répertoire>/<chemin>
#                 correspond à <révision>:<chemin> de l'amont
#   <liste>       fichier facultatif des chemins attendus, un par ligne, relatifs à la racine de
#                 l'amont ; une ligne terminée par « / » désigne tous les fichiers de l'amont sous
#                 ce répertoire ; lignes vides et « # » ignorées
#   --liste-seule ne contrôle que les fichiers de la liste (le reste du répertoire est ignoré)
#
# Chaque fichier de <répertoire> (hors LEPTON-PROVENANCE.md et .DS_Store) est comparé par
# SHA-256 à « git show <révision>:<chemin> ». Une ligne par fichier :
#   OK      identique octet pour octet
#   CR      identique une fois les CR retirés (fins de ligne différentes)
#   DIFF    contenu différent
#   TROP    absent de l'amont à cette révision
#   MANQUE  attendu par la liste, absent de la copie
# Code de retour : 0 si toutes les lignes sont OK, 1 s'il y a un écart, 2 si usage incorrect.
set -euo pipefail

erreur() { echo "verifier-import: $1" >&2; exit 2; }

liste_seule=0
if [ "${1:-}" = "--liste-seule" ]; then liste_seule=1; shift; fi
[ $# -ge 3 ] && [ $# -le 4 ] || erreur "usage : verifier-import.sh [--liste-seule] <clone> <révision> <répertoire> [<liste>]"
clone="$1"; revision="$2"; repertoire="$3"; liste="${4:-}"
[ "$liste_seule" -eq 0 ] || [ -n "$liste" ] || erreur "--liste-seule exige une liste"
git -C "$clone" rev-parse --git-dir > /dev/null 2>&1 || erreur "pas un clone git : $clone"
commit="$(git -C "$clone" rev-parse --verify --quiet "$revision^{commit}")" || erreur "révision inconnue : $revision"
[ -d "$repertoire" ] || erreur "répertoire absent : $repertoire"
[ -z "$liste" ] || [ -f "$liste" ] || erreur "liste absente : $liste"

if command -v sha256sum > /dev/null; then sha() { sha256sum | cut -d' ' -f1; }
else sha() { shasum -a 256 | cut -d' ' -f1; }; fi

tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT

# Fichiers attendus (liste développée contre l'amont).
: > "$tmp/attendus"
if [ -n "$liste" ]; then
    while IFS= read -r ligne || [ -n "$ligne" ]; do
        case "$ligne" in ''|'#'*) continue ;; esac
        case "$ligne" in
            */) git -C "$clone" ls-tree -r --name-only "$commit" -- "$ligne" >> "$tmp/attendus" ;;
            *)  echo "$ligne" >> "$tmp/attendus" ;;
        esac
    done < "$liste"
fi
LC_ALL=C sort -u -o "$tmp/attendus" "$tmp/attendus"

# Fichiers de la copie.
(cd "$repertoire" && find . -type f ! -name LEPTON-PROVENANCE.md ! -name .DS_Store | sed 's#^\./##') \
    | LC_ALL=C sort > "$tmp/copie"
if [ "$liste_seule" -eq 1 ]; then
    LC_ALL=C comm -12 "$tmp/copie" "$tmp/attendus" > "$tmp/controles"
else
    cp "$tmp/copie" "$tmp/controles"
fi

ok=0; ecarts=0
while IFS= read -r chemin; do
    if ! git -C "$clone" cat-file -e "$commit:$chemin" 2> /dev/null; then
        echo "TROP    $chemin"; ecarts=$((ecarts + 1)); continue
    fi
    local_sha="$(sha < "$repertoire/$chemin")"
    amont_sha="$(git -C "$clone" show "$commit:$chemin" | sha)"
    if [ "$local_sha" = "$amont_sha" ]; then
        echo "OK      $chemin"; ok=$((ok + 1))
    elif [ "$(tr -d '\r' < "$repertoire/$chemin" | sha)" = "$(git -C "$clone" show "$commit:$chemin" | tr -d '\r' | sha)" ]; then
        echo "CR      $chemin"; ecarts=$((ecarts + 1))
    else
        echo "DIFF    $chemin"; ecarts=$((ecarts + 1))
    fi
done < "$tmp/controles"

while IFS= read -r chemin; do
    echo "MANQUE  $chemin"; ecarts=$((ecarts + 1))
done < <(LC_ALL=C comm -13 "$tmp/copie" "$tmp/attendus")

echo "verifier-import: $commit ; $ok identique(s), $ecarts écart(s)"
[ "$ecarts" -eq 0 ]
