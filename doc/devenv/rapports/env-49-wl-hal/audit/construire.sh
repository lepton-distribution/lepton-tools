#!/bin/bash
# construire.sh <rootstock> <journal-dir> <preset>...
RS=$1; J=$2; shift 2; mkdir -p "$J"
source "$RS/depots/lepton/original/master/scripts/lepton-env.sh" >/dev/null 2>&1
for p in "$@"; do
  rm -rf "$RS/build/$p"
  cmake -S "$RS/trunk" --preset "$p" > "$J/$p.configure.log" 2>&1; c=$?
  if [ $c -eq 0 ]; then cmake --build "$RS/build/$p" > "$J/$p.build.log" 2>&1; c=$?; fi
  w=$(grep -c 'warning:' "$J/$p.build.log" 2>/dev/null)
  echo "$p : code $c ; avertissements $w"
done
