#!/usr/bin/env bash
# Construit les presets dans une copie du rootstock, clone noyau sur <rev-avant> puis <rev-après>,
# même chemin ; relève le contenu des sections (hors *fill*) de chaque MAP.
set -uo pipefail
S="$1"; shift; C="$S/rs-cmp"; out="$S/cmp"; rm -rf "$C" "$out"; mkdir -p "$C" "$out"
cp -RP ~/lepton/depots ~/lepton/.scion.rootstock.signature "$C"/ && cp -RP ~/lepton/trunk "$C"/
K="$C/depots/lepton/original/master"
export LEPTON_EMBOS_ROOT=$HOME/lepton/third_party/embos/cortexm-gcc/5.20.0.0 PYTHONDONTWRITEBYTECODE=1
for etat in avant:49ed8fe apres:devenv/env-5; do
  nom=${etat%%:*}; rev=${etat#*:}
  git -C "$K" checkout -q "$rev" || exit 1
  (cd "$C" && scion graft >/dev/null 2>&1) || { echo "graft $nom"; exit 1; }
  rm -rf "$C/build"
  (cmake -S "$C/trunk" --preset host && cmake --build "$C/build/host") > "$out/$nom-host.log" 2>&1 || echo "échec host $nom"
  for p in "$@"; do
    (cmake -S "$C/trunk" --preset "$p" && cmake --build "$C/build/$p") > "$out/$nom-$p.log" 2>&1 || echo "échec $nom $p"
    python3 "$(dirname "$0")/env-5-contenu-sections.py" "$C/build/$p/lepton.map" > "$out/$nom-$p.sections"
  done
done
git -C "$K" checkout -q devenv/env-5
for p in "$@"; do
  if diff <(sed 's/ taille=.* contenu=/ contenu=/' "$out/avant-$p.sections") <(sed 's/ taille=.* contenu=/ contenu=/' "$out/apres-$p.sections") >/dev/null; then r="contenu identique"; else r="CONTENU DIFFÉRENT"; fi
  echo "$p : $r"
done
