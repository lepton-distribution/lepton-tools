#!/usr/bin/env bash
# Même SOURCE_DATE_EPOCH, noyau aux commits REVS (défaut : 66676b6 avant, 82a6700 après) : empreintes de an386-freertos.
set -u
C=$1; cd "$C" || exit 1
set --
source depots/lepton/original/master/scripts/lepton-env.sh "$C" >/dev/null || exit 1
export SOURCE_DATE_EPOCH=1760536800 PYTHONDONTWRITEBYTECODE=1
p=qemu-mps2-an386-freertos
for rev in ${REVS:-66676b6 82a6700}; do
  git -C depots/lepton/original/master checkout -q $rev || exit 1
  rm -rf build/host build/$p
  { cmake -S trunk --preset host && cmake --build build/host && cmake -S trunk --preset $p && cmake --build build/$p; } > build-$rev.log 2>&1 || { echo "échec $rev"; exit 1; }
  echo "== $rev"; (cd build/$p && shasum -a 256 lepton.elf lepton.bin lepton.hex)
done
git -C depots/lepton/original/master checkout -q devenv/env-8-r2
