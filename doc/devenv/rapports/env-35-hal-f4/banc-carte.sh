#!/usr/bin/env bash
# banc-carte.sh — banc sur carte d'un preset NUCLEO-F429ZI (forme d'ENV-24 §6), ENV-35.
#
# Usage : banc-carte.sh <ROOTSTOCK> <répertoire-oracle> <preset> <port-série> <ip-hôte>
#   1. reconfigure <ROOTSTOCK>/build/<preset> avec LEPTON_BOARD_SERIAL_PORT et
#      LEPTON_NET_TEST_HOST_IP, construit (kal_bench compris) : carte-config.log ;
#   2. recapture lepton.elf et la compare à <répertoire-oracle>/<preset> (code 0 exigé) ;
#   3. ctest -L board (flash « verify » par OpenOCD, fumée, banc KAL, réseau) : carte.log,
#      carte-detail.log (LastTest.log), fumee-carte.log, reseau-carte.log.
# Écrit en flash : à lancer seulement avec l'accord de l'utilisateur pour la session (PA-11).
set -u
ROOT=$1 ORACLE=$2 P=$3 PORT=$4 HOSTIP=$5
OUTILS=$(cd "$(dirname "$0")/../../../.." && pwd)/scripts/oracle
B=$ROOT/build/$P
mkdir -p "$ORACLE/$P"
D=$(cd "$ORACLE/$P" && pwd)
export PYTHONDONTWRITEBYTECODE=1
# shellcheck disable=SC1091
source "$ROOT/depots/lepton/original/master/scripts/lepton-env.sh" >/dev/null
{
  cmake -S "$ROOT/trunk" -B "$B" --preset "$P" \
        -DLEPTON_BOARD_SERIAL_PORT="$PORT" -DLEPTON_NET_TEST_HOST_IP="$HOSTIP" &&
  cmake --build "$B"
} > "$D/carte-config.log" 2>&1 || { echo "$P : configuration ou construction en échec"; exit 1; }
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
