#!/usr/bin/env bash
# ENV-69 : fichiers changés par les opérations de graine au terminal (candidats du déclencheur D36).
# Usage : fichiers.sh <rootstock d'essai> <dépôt env69lib> <dépôt env69lib v2> <sortie>
# Pour chaque opération : instantané avant/après (instantane.py), chemins ajoutés, retirés,
# changés ; les liens du trunk sont comptés, pas listés ; stems de `seed status --json` après.
set -u
E=$1 D1=$2 D2=$3 OUT=$4
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$OUT"
n=0
snap() { python3 -I "$here/instantane.py" "$E" "$1"; }
stems() {
  lepton -C "$E" seed status --json 2>/dev/null | python3 -I -c '
import json,sys
d=json.load(sys.stdin)
for s in d.get("scions",[]):
    print(s.get("name"), s.get("stem") or "-", s.get("projected_by") or "")' | sed "s|$E|<E>|g"
}
op() {
  n=$((n+1)); local tag
  tag=$(printf '%02d' "$n")
  snap "$OUT/.avant"
  echo "## $tag $*" >>"$OUT/journal.txt"
  "$@" >>"$OUT/journal.txt" 2>&1
  echo "code=$?" >>"$OUT/journal.txt"
  snap "$OUT/.apres"
  {
    echo "# $tag $*" | sed "s|$E|<E>|g; s|$HOME|<HOME>|g"
    python3 -I - "$OUT/.avant" "$OUT/.apres" <<'PY'
import sys
def load(p):
    d = {}
    for line in open(p):
        k, t, h = line.rstrip("\n").split("\t")
        d[k] = (t, h)
    return d
a, b = load(sys.argv[1]), load(sys.argv[2])
trunk = {"ajouté": 0, "retiré": 0, "changé": 0}
for k in sorted(set(a) | set(b)):
    kind = "ajouté" if k not in a else "retiré" if k not in b else "changé" if a[k] != b[k] else None
    if not kind:
        continue
    if k.startswith("trunk/") and (b.get(k) or a.get(k))[0] == "l":
        trunk[kind] += 1
        continue
    if "/.git/" in k:
        continue
    print(f"{kind}\t{k}")
print(f"liens du trunk\t+{trunk['ajouté']} -{trunk['retiré']} ~{trunk['changé']}")
PY
    echo "stems après :"
    stems
    echo
  } >>"$OUT/fichiers.txt"
}
: >"$OUT/journal.txt"; : >"$OUT/fichiers.txt"
U1="file://localhost$D1@master"; U2="file://localhost$D2@master"
op lepton -C "$E" seed add env69lib "$U1" --type bibliotheque --no-cmake
op lepton -C "$E" seed replace env69lib "$U2" --no-cmake
op lepton -C "$E" seed replace env69lib "$U1" --no-cmake
op lepton -C "$E" seed remove env69lib --purge --no-cmake
op lepton -C "$E" seed add env69lib "$U1" --type bibliotheque --no-cmake
key=$(awk '$2 ~ /env69lib/ {print $1 "@" $2; exit}' "$E/trunk/.scion.grafted.list")
echo "clé : $key" >>"$OUT/journal.txt"
op scion graft-remove --purge "$key" "$E"
op scion graft "$E"
rm -f "$OUT/.avant" "$OUT/.apres"
sed -i '' "s|$E|<E>|g; s|$HOME|<HOME>|g" "$OUT/journal.txt"
