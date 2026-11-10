#!/usr/bin/env bash
# banc-wl55.sh — banc sur la paire NUCLEO-WL55JC1 d'un preset (forme de banc-carte.sh d'ENV-35,
# variables d'ENV-32), ENV-42.
#
# Usage : banc-wl55.sh <ROOTSTOCK> <répertoire-oracle> <preset> <port-A> <n°-A> <port-B> <n°-B>
#   1. reconfigure <ROOTSTOCK>/build/<preset> avec LEPTON_BOARD_SERIAL_PORT, LEPTON_BOARD_PROBE_SERIAL (ENV-45 ;
#      LEPTON_BOARD_STLINK_SERIAL jusqu'à ENV-44),
#      LEPTON_RADIO_PEER_SERIAL_PORT, LEPTON_RADIO_PEER_STLINK_SERIAL, construit : carte-config.log ;
#   2. recapture lepton.elf et la compare à <répertoire-oracle>/<preset> (code 0 exigé) ;
#   3. ctest -L board (flash « verify » de A, fumée, banc KAL, radio avec flash de B) : carte.log,
#      carte-detail.log (LastTest.log), fumee-carte.log, radio-carte.log.
# Écrit en flash sur les deux cartes : seulement avec l'accord de l'utilisateur (PA-11).
set -u
ROOT=$1 ORACLE=$2 P=$3 PA=$4 SA=$5 PB=$6 SB=$7
OUTILS=$(cd "$(dirname "$0")/../../../.." && pwd)/scripts/oracle
B=$ROOT/build/$P
mkdir -p "$ORACLE/$P"
D=$(cd "$ORACLE/$P" && pwd)
export PYTHONDONTWRITEBYTECODE=1
# shellcheck disable=SC1091
source "$ROOT/depots/lepton/original/master/scripts/lepton-env.sh" >/dev/null
{
  cmake -S "$ROOT/trunk" -B "$B" --preset "$P" \
        -DLEPTON_BOARD_SERIAL_PORT="$PA" -DLEPTON_BOARD_PROBE_SERIAL="$SA" \
        -DLEPTON_RADIO_PEER_SERIAL_PORT="$PB" -DLEPTON_RADIO_PEER_STLINK_SERIAL="$SB" &&
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
cp "$B/board_radio.log" "$D/radio-carte.log" 2>/dev/null
grep -E 'tests passed|tests failed' "$D/carte.log"
exit $rc
