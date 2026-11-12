#!/usr/bin/env bash
# ENV-53 : relevé des clones tiers projetés d'un rootstock (lecture seule).
# Usage : bash releve-clones.sh <rootstock> <sortie>
#
# Pour chaque clone <rootstock>/depots/tiers/<clé>/<version> (nom de fichier <clé>@<version>) :
#   <nom>.sparse-checkout   copie de .git/info/sparse-checkout (absent : « (aucun) »)
#   <nom>.extraits.txt      fichiers présents sur le disque hors .git et .DS_Store, triés (LC_ALL=C)
#   <nom>.suivis-H.txt      fichiers marqués H par git ls-files -t (extraits), triés
# et clones.txt : une ligne par clone (HEAD, origin, sparseCheckout, cône, ignorecase, nombres H et
# S, fichiers extraits, extraits = H, Ko du clone hors .git, Ko de .git).
# Lit .git/config.worktree et .git/config par grep : le hook du Mac refuse « git config » sous depots/tiers/.
# Bash et outils POSIX seulement : même script sur macOS et sur Debian.
set -u
export LC_ALL=C
R=${1:?rootstock}
S=${2:?sortie}
mkdir -p "$S"
: > "$S/clones.txt"
cfg() { # cfg <.git> <clé> : valeur de « clé = valeur » (casse ignorée), config.worktree d'abord
  # (git sparse-checkout active l'extension worktreeConfig et y écrit core.sparseCheckout*)
  cat "$1/config.worktree" "$1/config" 2>/dev/null | grep -i -m1 "^[[:space:]]*$2[[:space:]]*=" \
    | sed 's/.*=[[:space:]]*//' | tr -d '[:space:]'
}
for c in "$R"/depots/tiers/*/*; do
  [ -d "$c/.git" ] || continue
  rel=${c#"$R"/depots/tiers/}
  nom=${rel%%/*}@${rel#*/}
  g="$c/.git"
  if [ -f "$g/info/sparse-checkout" ]; then cp "$g/info/sparse-checkout" "$S/$nom.sparse-checkout"
  else echo "(aucun)" > "$S/$nom.sparse-checkout"; fi
  (cd "$c" && find . -path ./.git -prune -o -type f ! -name .DS_Store -print | sed 's|^\./||' | sort) > "$S/$nom.extraits.txt"
  git -C "$c" ls-files -t > "$S/.lsft.tmp"
  nH=$(grep -c '^H ' "$S/.lsft.tmp"); nS=$(grep -c '^S ' "$S/.lsft.tmp")
  sed -n 's/^H //p' "$S/.lsft.tmp" | sort > "$S/$nom.suivis-H.txt"
  rm -f "$S/.lsft.tmp"
  if cmp -s "$S/$nom.extraits.txt" "$S/$nom.suivis-H.txt"; then eq=oui; else eq=non; fi
  nE=$(wc -l < "$S/$nom.extraits.txt" | tr -d ' ')
  kT=$(du -sk "$c" | cut -f1); kG=$(du -sk "$g" | cut -f1)
  printf '%s head=%s origin=%s sparseCheckout=%s cone=%s ignorecase=%s H=%s S=%s extraits=%s extraits=H:%s ko_hors_git=%s ko_git=%s\n' \
    "$rel" "$(git -C "$c" rev-parse --short=7 HEAD)" "$(cfg "$g" url)" \
    "$(cfg "$g" sparsecheckout)" "$(cfg "$g" sparsecheckoutcone)" \
    "$(cfg "$g" ignorecase)" "$nH" "$nS" "$nE" "$eq" "$((kT - kG))" "$kG" >> "$S/clones.txt"
done
cat "$S/clones.txt"
