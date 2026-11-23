#!/usr/bin/env bash
# ENV-70 : rejoue les fixtures 70, 65, 60, 56 avec le scion donné, git journalisé (bin/git).
# Usage : rejouer.sh <scion> <avant|apres>
set -u
S=$1 phase=$2
D=$(cd "$(dirname "$0")/../../../../.." && pwd)
R=$D/lepton-tools/doc/devenv/rapports
B=$D/essais/env-70-fixture/$phase
mkdir -p "$B"
python3 "$R/env-70-scion/fixture.py" "$D/seed.scions" "$S" "$B/fixture70" "$R/env-70-scion/fixture70-$phase" >/dev/null
echo "fixture70 code=$?"
for n in 65 60 56; do
  mkdir -p "$B/fixture$n"
  PATH="$R/env-70-scion/bin:$PATH" ENV70_GIT=/usr/bin/git ENV70_GITLOG="$B/fixture$n/gitlog.jsonl" \
    python3 "$R/env-$n-scion/fixture.py" "$D/seed.scions" "$S" "$B/fixture$n/base" "$R/env-70-scion/fixture$n-$phase" >/dev/null
  echo "fixture$n code=$?"
done
