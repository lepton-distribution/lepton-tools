#!/bin/sh
# liste.sh <rootstock> : (lien, cible) triés du trunk, puis bilan sur stderr
cd "$1/trunk" || exit 1
find . -type l -exec sh -c 'for l; do printf "%s\t%s\n" "$l" "$(readlink "$l")"; done' _ {} + | LC_ALL=C sort
echo "liens=$(find . -type l | wc -l | tr -d ' ') reguliers=$(find . -type f ! -name .scion.grafted.list | wc -l | tr -d ' ') casses=$(find -L . -type l | wc -l | tr -d ' ') ds_store=$(find . -name .DS_Store | wc -l | tr -d ' ')" >&2
