#!/usr/bin/env bash
# rejouer-oracle.sh — construit à neuf une liste de presets Lepton et en capture l'oracle.
#
# Usage : rejouer-oracle.sh <ROOTSTOCK> <répertoire-oracle> [--qemu <preset>]... [--carte <preset>]...
#   host       : toujours traité en premier (prérequis des presets croisés) : ctest complet
#                (ctest.log) et empreintes mklepton (mklepton-empreintes.sha256).
#   --qemu P   : construction, capture binaire, ctest complet (banc-kal.log, fumée comprise),
#                console de fumée (fumee.log).
#   --carte P  : construction et capture binaire seulement (aucun accès matériel).
#
# Chaque preset : rm -rf <ROOTSTOCK>/build/<P>, configuration, construction (construction.log),
# puis scripts/oracle/capturer-oracle.sh sur <ROOTSTOCK>/build/<P>/lepton.elf.
# Les mêmes commandes servent à l'oracle avant et à l'oracle après (skill lepton-oracle).
# Code de retour : 0 si tout a réussi, 1 sinon (le résumé liste les échecs).
set -uo pipefail

ici="$(cd "$(dirname "$0")" && pwd)"
[ $# -ge 2 ] || { echo "usage : rejouer-oracle.sh <ROOTSTOCK> <répertoire-oracle> [--qemu P]... [--carte P]..." >&2; exit 1; }
rootstock="$(cd "$1" && pwd)"; sortie="$2"; shift 2
mkdir -p "$sortie"; sortie="$(cd "$sortie" && pwd)"
trunk="$rootstock/trunk"; build="$rootstock/build"
clone="$rootstock/depots/lepton/original/master"

qemu=(); cartes=()
while [ $# -gt 0 ]; do
    case "$1" in
        --qemu)  qemu+=("$2"); shift 2 ;;
        --carte) cartes+=("$2"); shift 2 ;;
        *) echo "rejouer-oracle: argument inconnu : $1" >&2; exit 1 ;;
    esac
done

set --   # lepton-env.sh lit "$1" comme chemin de départ
# shellcheck disable=SC1091
source "$clone/scripts/lepton-env.sh" "$rootstock" >/dev/null || exit 1
export PYTHONDONTWRITEBYTECODE=1

echecs=()

construire() {   # construire <preset> <dossier-sortie>
    local p="$1" d="$2"
    rm -rf "${build:?}/$p"
    { cmake -S "$trunk" --preset "$p" && cmake --build "$build/$p"; } > "$d/construction.log" 2>&1
}

d="$sortie/host"; mkdir -p "$d"
if construire host "$d"; then
    ctest --test-dir "$build/host" --output-on-failure > "$d/ctest.log" 2>&1 || echecs+=("host:ctest")
    bash "$trunk/tests/host/mklepton_empreintes.sh" --mklepton "$build/host/mklepton" \
        --trunk "$trunk" --out "$d/mklepton-empreintes.sha256" > "$d/empreintes.log" 2>&1 \
        || echecs+=("host:empreintes")
else
    echecs+=("host:construction"); echo "rejouer-oracle: host non construit, arrêt" >&2
    printf '%s\n' "${echecs[@]}"; exit 1
fi

for p in "${qemu[@]}" "${cartes[@]}"; do
    d="$sortie/$p"; mkdir -p "$d"
    echo "== $p"
    if ! construire "$p" "$d"; then echecs+=("$p:construction"); continue; fi
    "$ici/capturer-oracle.sh" "$build/$p/lepton.elf" "$d" || echecs+=("$p:capture")
done
for p in "${qemu[@]}"; do
    d="$sortie/$p"
    [ -f "$build/$p/lepton.elf" ] || continue
    echo "== $p (ctest)"
    ctest --test-dir "$build/$p" --output-on-failure > "$d/banc-kal.log" 2>&1 || echecs+=("$p:ctest")
    cp "$build/$p/smoke_lsh_uart0.log" "$d/fumee.log" 2>/dev/null || echecs+=("$p:fumee")
done

if [ ${#echecs[@]} -eq 0 ]; then echo "rejouer-oracle: tout a réussi"; exit 0; fi
echo "rejouer-oracle: échecs :"; printf '  %s\n' "${echecs[@]}"; exit 1
