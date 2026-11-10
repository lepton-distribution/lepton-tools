#!/usr/bin/env bash
# banc-sonde.sh — banc sur carte d'un preset, sonde choisie par LEPTON_BOARD_PROBE_SERIAL (forme de
# banc-carte.sh d'ENV-35), ENV-45.
#
# Usage : banc-sonde.sh <ROOTSTOCK> <répertoire-oracle> <preset> <port-série> <n°-sonde> [<ip-hôte>]
#   1. reconfigure <ROOTSTOCK>/build/<preset> avec LEPTON_BOARD_SERIAL_PORT, LEPTON_BOARD_PROBE_SERIAL
#      (et LEPTON_NET_TEST_HOST_IP si donnée), construit (kal_bench compris) : carte-config.log ;
#   2. vérifie la cfg générée build/<preset>/openocd-<bsp>.cfg (adapter serial <n°>) : cfg-sonde.cfg ;
#   3. recapture lepton.elf et la compare à <répertoire-oracle>/<preset> (code 0 exigé) ;
#   4. ctest -L board (flash « verify » par OpenOCD, fumée, banc KAL, réseau si ip) : carte.log,
#      carte-detail.log (LastTest.log), fumee-carte.log, reseau-carte.log.
# Écrit en flash : seulement avec l'accord de l'utilisateur (PA-11, accordé au PA-77 d'ENV-45).
set -u
ROOT=$1 ORACLE=$2 P=$3 PORT=$4 SERIE=$5 HOSTIP=${6:-}
OUTILS=$(cd "$(dirname "$0")/../../../.." && pwd)/scripts/oracle
B=$ROOT/build/$P
BSP=${P%-embos}; BSP=${BSP%-freertos}
mkdir -p "$ORACLE/$P"
D=$(cd "$ORACLE/$P" && pwd)
export PYTHONDONTWRITEBYTECODE=1
# shellcheck disable=SC1091
source "$ROOT/depots/lepton/original/master/scripts/lepton-env.sh" >/dev/null
net=()
[ -n "$HOSTIP" ] && net=(-DLEPTON_NET_TEST_HOST_IP="$HOSTIP")
{
  cmake -S "$ROOT/trunk" -B "$B" --preset "$P" \
        -DLEPTON_BOARD_SERIAL_PORT="$PORT" -DLEPTON_BOARD_PROBE_SERIAL="$SERIE" ${net[@]+"${net[@]}"} &&
  cmake --build "$B"
} > "$D/carte-config.log" 2>&1 || { echo "$P : configuration ou construction en échec"; exit 1; }
CFG=$B/openocd-$BSP.cfg
cp "$CFG" "$D/cfg-sonde.cfg" 2>/dev/null || { echo "$P : $CFG absente"; exit 1; }
grep -qx "adapter serial $SERIE" "$CFG" || { echo "$P : $CFG sans « adapter serial $SERIE »"; exit 1; }
T=$(mktemp -d)
"$OUTILS/capturer-oracle.sh" "$B/lepton.elf" "$T" > /dev/null
python3 "$OUTILS/comparer-oracle.py" "$D" "$T" > "$D/carte-oracle.txt" 2>&1
rc=$?
rm -rf "$T"
[ $rc -eq 0 ] || { echo "$P : lepton.elf différent de l'oracle ($rc)"; exit 1; }
cd "$ROOT/trunk" || exit 1
caffeinate -i ctest --preset "$P" -L board --output-on-failure > "$D/carte.log" 2>&1
rc=$?
cp "$B/Testing/Temporary/LastTest.log" "$D/carte-detail.log" 2>/dev/null
cp "$B/smoke_lsh_board.log" "$D/fumee-carte.log" 2>/dev/null
cp "$B/board_net.log" "$D/reseau-carte.log" 2>/dev/null
grep -E 'tests passed|tests failed' "$D/carte.log"
exit $rc
