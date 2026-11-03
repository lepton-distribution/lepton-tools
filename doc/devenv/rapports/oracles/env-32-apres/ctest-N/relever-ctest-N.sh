#!/usr/bin/env bash
# relever-ctest-N.sh <ROOTSTOCK> <sortie> <scratch> — ENV-32 : listes ctest -N et tests détaillés
# (json-v1) des presets WL55, configurés à neuf hors de <ROOTSTOCK>/build, en quatre variantes :
# banc (ports et sondes du banc), fictif (ports et sondes fictifs), seul (port de A seul), sans.
set -uo pipefail
R="$1"; O="$2"; S="$3"; mkdir -p "$O"
set --
# shellcheck disable=SC1091
source "$R/depots/lepton/original/master/scripts/lepton-env.sh" "$R" >/dev/null || exit 1
export PYTHONDONTWRITEBYTECODE=1
BANC=(-DLEPTON_BOARD_SERIAL_PORT=/dev/cu.usbmodem145103 -DLEPTON_BOARD_STLINK_SERIAL=002700253431510837393937
      -DLEPTON_RADIO_PEER_SERIAL_PORT=/dev/cu.usbmodem1454403 -DLEPTON_RADIO_PEER_STLINK_SERIAL=004F003E3431510937393937)
FICTIF=(-DLEPTON_BOARD_SERIAL_PORT=/dev/fictif-a -DLEPTON_BOARD_STLINK_SERIAL=FICTIFA
        -DLEPTON_RADIO_PEER_SERIAL_PORT=/dev/fictif-b -DLEPTON_RADIO_PEER_STLINK_SERIAL=FICTIFB)
SEUL=(-DLEPTON_BOARD_SERIAL_PORT=/dev/fictif-a)
code=0
for p in nucleo-wl55jc1-embos nucleo-wl55jc1-freertos; do
  for m in banc fictif seul sans; do
    case $m in banc) o=("${BANC[@]}");; fictif) o=("${FICTIF[@]}");; seul) o=("${SEUL[@]}");; sans) o=();; esac
    b="$S/$p-$m"; rm -rf "$b"
    cmake -S "$R/trunk" -B "$b" --preset "$p" "${o[@]}" > "$O/$p-$m.configure.log" 2>&1 || { echo "configure $p $m : échec"; code=1; }
    (cd "$b" && ctest -N) | sed 1d > "$O/$p-$m.ctest-N.txt"
    (cd "$b" && ctest -N -L greffon:) | sed 1d > "$O/$p-$m.ctest-N-greffon.txt"
    # tests détaillés, chemins du répertoire de construction remplacés par <build>
    (cd "$b" && ctest --show-only=json-v1) | python3 -c '
import json,sys
b=sys.argv[1]; d=json.load(sys.stdin)
bs=[b, b.removeprefix("/private")]
def net(x):
    for v in bs:
        x=x.replace(v,"<build>")
    return x
for t in d["tests"]:
    pr={p["name"]:p["value"] for p in t.get("properties",[])}
    pr.pop("WORKING_DIRECTORY",None)
    print(t["name"], net(json.dumps(pr,sort_keys=True,ensure_ascii=False)))
    print("   ", net(" ".join(t.get("command",[]))))
' "$(cd "$b" && pwd -P)" > "$O/$p-$m.tests.txt"
    echo "$p $m : $(grep 'Total Tests' "$O/$p-$m.ctest-N.txt")"
  done
done
exit $code
