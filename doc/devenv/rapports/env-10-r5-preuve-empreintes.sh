#!/usr/bin/env bash
# E1 (R5) : même SOURCE_DATE_EPOCH, noyau 9ea1b2a (avant) et ed46f71 (après O6) : empreintes de an386-embos.
set -u
C=$1; cd "$C" || exit 1
set --
source depots/lepton/original/master/scripts/lepton-env.sh "$C" >/dev/null || exit 1
export SOURCE_DATE_EPOCH=1760536800 PYTHONDONTWRITEBYTECODE=1
p=qemu-mps2-an386-embos
for rev in ${REVS:-9ea1b2a ed46f71}; do
  git -C depots/lepton/original/master checkout -q $rev || exit 1
  rm -rf build/host build/$p
  { cmake -S trunk --preset host && cmake --build build/host && cmake -S trunk --preset $p && cmake --build build/$p; } > build-$rev.log 2>&1 || { echo "échec $rev"; exit 1; }
  echo "== $rev"; (cd build/$p && shasum -a 256 lepton.elf lepton.bin lepton.hex)
done
git -C depots/lepton/original/master checkout -q devenv/env-10-r5
