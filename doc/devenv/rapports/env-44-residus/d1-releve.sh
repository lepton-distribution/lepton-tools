#!/usr/bin/env bash
# D1 d'ENV-44 : relevé d'un rootstock d'essai (lecture seule).
# Usage : d1-releve.sh <rootstock> <sortie-préfixe>
# Produit <préfixe>-liens.txt (chemin -> cible, triés), <préfixe>-status.txt (lepton seed status),
# <préfixe>-grafted.txt (clés greffées), <préfixe>-clones.txt (clones : branche, commit, modifs).
set -uo pipefail
r="$(cd "$1" && pwd)"; p="$2"
( cd "$r/trunk" && find . -type l -exec sh -c 'for l; do printf "%s -> %s\n" "$l" "$(readlink "$l")"; done' _ {} + | sort ) > "$p-liens.txt"
( cd "$r/trunk" && lepton seed status 2>&1 ) > "$p-status.txt"
awk '{print $1"@"$2, $3}' "$r/trunk/.scion.grafted.list" | sort > "$p-grafted.txt"
for c in $(find "$r/depots" -maxdepth 5 -name .git | sed 's#/.git$##' | sort); do
    printf '%s %s %s %s\n' "${c#"$r"/}" "$(git -C "$c" branch --show-current)" \
        "$(git -C "$c" rev-parse --short HEAD)" "$(git -C "$c" status --short | wc -l | tr -d ' ')"
done > "$p-clones.txt"
printf 'liens %s ; cassés %s ; réguliers %s\n' "$(wc -l < "$p-liens.txt" | tr -d ' ')" \
    "$(find -L "$r/trunk" -type l | wc -l | tr -d ' ')" \
    "$(find "$r/trunk" -type f ! -name .scion.grafted.list ! -name .DS_Store | wc -l | tr -d ' ')"
