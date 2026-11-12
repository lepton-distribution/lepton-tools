#!/usr/bin/env bash
# ENV-53 : inventaire des clones de greffons et de graines d'un rootstock (lecture seule ; §2bis,
# « Branche des clones »). Usage : bash inventaire-clones.sh <rootstock>
# Une ligne par clone : chemin, branche courante, HEAD, amont, nombre de modifications.
# Les clones tiers (depots/tiers) et les dépôts de travail des miroirs (depots/.mirrors) sont exclus.
set -u
export LC_ALL=C
R=${1:?rootstock}
cd "$R" || exit 2
find depots -name .git -type d -prune 2>/dev/null | grep -v -e '^depots/tiers/' -e '^depots/\.mirrors/' | sort |
while read -r g; do
  c=${g%/.git}
  printf '%s branche=%s head=%s amont=%s modifs=%s\n' "$c" \
    "$(git -C "$c" branch --show-current)" "$(git -C "$c" rev-parse --short=7 HEAD)" \
    "$(git -C "$c" rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null || echo aucun)" \
    "$(git -C "$c" status --porcelain | wc -l | tr -d ' ')"
done
