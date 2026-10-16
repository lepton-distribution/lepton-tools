#!/usr/bin/env bash
# Essai fonctionnel N5 (ENV-8 R2) dans un rootstock jetable : valeurs d'options de la graine.
# Usage : essai-r2.sh REPERTOIRE
set -u
dir=$1; root=$dir/rootstock; mkdir -p "$dir"
ref=$HOME/lepton
export PATH="$HOME/opt/arm-gnu-toolchain-14.2.rel1-darwin-x86_64-arm-none-eabi/bin:$PATH"
export PYTHONDONTWRITEBYTECODE=1
export PATH="$HOME/lepton-tools-dev/venv-lepton-tools/bin:$PATH"   # lepton de la branche (éditable)
command -v lepton
mkconf=sys/user/tauon-basic/etc/mkconf_tauon_basic_qemu_mps2.xml
n=0
etape() { n=$((n + 1)); printf '\n== %d. %s\n' "$n" "$*"; }
attendu() {   # attendu <code> <commande>... : code de retour exact
    local c=$1; shift
    printf '$ %s\n' "$*"; "$@"; local r=$?
    printf '[code %s, attendu %s]\n' "$r" "$c"
    [ "$r" = "$c" ] || { echo "ÉCHEC"; exit 1; }
}

etape "copie du noyau sur une branche sans « / » (lepton refuse « / » dans @VERSION)"
noyau=$dir/noyau-r2
attendu 0 git clone -q --branch devenv/env-8-r2 "$ref/depots/lepton/original/master" "$noyau"
attendu 0 git -C "$noyau" checkout -q -b essai-r2
git -C "$noyau" log --oneline -1

etape "seed new (noyau : essai-r2 = devenv/env-8-r2)"
attendu 0 lepton seed new essai -C "$root" --bsp qemu-mps2-an386 --backend freertos --mkconf "$mkconf" \
    --origin "lepton-noyau=file://localhost$noyau@essai-r2" \
    --origin "qemu-mps2=file://localhost$ref/depots/lepton-famille/qemu-mps2@master" \
    --origin "qemu-mps2-an386=file://localhost$ref/depots/lepton-bsp/qemu-mps2-an386@master"
find "$root/depots/lepton" -maxdepth 3 -name .git -exec dirname {} \; | xargs -I{} git -C {} log --oneline -1

etape "application demoopt avec une option de chaque type"
attendu 0 lepton scion new --type application demoopt -C "$root" --no-cmake
manifeste=$(find "$root/depots" -path '*demoopt*' -name lepton-greffon.json | head -1)
echo "manifeste : $manifeste"
python3 -I - "$manifeste" <<'EOF'
import json, sys
p = sys.argv[1]
d = json.load(open(p))
d["options"] = [
    {"nom": "OPT_BOOL", "type": "booleen", "defaut": False, "portee": "privee", "description": "Booléen."},
    {"nom": "OPT_INT", "type": "entier", "defaut": 10, "min": 1, "max": 100, "portee": "publique", "description": "Entier."},
    {"nom": "OPT_ENUM", "type": "enumeration", "defaut": "a", "valeurs": ["a", "b"], "portee": "privee", "description": "Énumération."},
    {"nom": "OPT_STR", "type": "chaine", "defaut": "defaut", "portee": "privee", "description": "Chaîne."}]
json.dump(d, open(p, "w"), ensure_ascii=False, indent=2)
EOF
graine=$(find "$root/depots/lepton-seed" -name lepton-graine.json | head -1)
echo "graine : $graine"
fixer() {   # fixer <json des options>
    python3 -I - "$graine" "$1" <<'EOF'
import json, sys
p = sys.argv[1]
d = json.load(open(p))
d["options"] = json.loads(sys.argv[2])
json.dump(d, open(p, "w"), ensure_ascii=False, indent=2)
EOF
}
fixer '{"demoopt": {"OPT_BOOL": true, "OPT_INT": 42, "OPT_ENUM": "b", "OPT_STR": "bonjour"}}'

etape "check et generate"
attendu 0 lepton check -C "$root"
attendu 0 lepton generate -C "$root"
presets=$root/trunk/CMakeUserPresets.json
python3 -I -c 'import json,sys; d=json.load(open(sys.argv[1]))
for p in d["configurePresets"]:
    print(p["name"], {k: v for k, v in p["cacheVariables"].items() if k.startswith("LEPTON_OPTION_")})' "$presets"
preset=$(python3 -I -c 'import json,sys; print(json.load(open(sys.argv[1]))["configurePresets"][0]["name"])' "$presets")

etape "cmake host, $preset, construction"
cd "$root/trunk" || exit 1
attendu 0 cmake --preset host > "$dir/host.log" 2>&1
attendu 0 cmake --build "$root/build/host" >> "$dir/host.log" 2>&1
attendu 0 cmake --preset "$preset" > "$dir/preset.log" 2>&1
attendu 0 cmake --build "$root/build/$preset" >> "$dir/preset.log" 2>&1

etape "compile_commands.json : définitions par portée"
python3 -I - "$root/build/$preset/compile_commands.json" <<'EOF'
import json, re, sys
cmds = json.load(open(sys.argv[1]))
def defs(e):
    return sorted(set(re.findall(r'-D(OPT_[A-Z]+=(?:\\"[^\\]*\\"|"[^"]*"|\S+))', e["command"])))
app = [e for e in cmds if "/bin/demoopt/" in e["file"]]
autres = [e for e in cmds if "/bin/demoopt/" not in e["file"]]
print("sources de demoopt :", len(app))
for e in app:
    print("  ", e["file"].split("/sys/root/src/")[-1], defs(e))
fuites = [e["file"] for e in autres if defs(e)]
print("autres sources portant OPT_* :", len(fuites), fuites[:3])
ok = app and all(set(defs(e)) == {'OPT_BOOL=1', 'OPT_INT=42', 'OPT_ENUM=b', 'OPT_STR=\\"bonjour\\"'} for e in app) and not fuites
print("CONFORME" if ok else "NON CONFORME")
sys.exit(0 if ok else 1)
EOF
[ $? = 0 ] || exit 1

etape "fumée QEMU"
attendu 0 ctest --preset "$preset" -L smoke --output-on-failure > "$dir/fumee.log" 2>&1
tail -3 "$dir/fumee.log"

etape "valeur hors bornes dans la graine : check et generate refusent"
fixer '{"demoopt": {"OPT_INT": 101, "OPT_ENUM": "c"}}'
attendu 1 lepton check -C "$root"
attendu 1 lepton generate -C "$root"

etape "valeur hors bornes passée à CMake par -D : configuration refusée"
fixer '{"demoopt": {"OPT_BOOL": true, "OPT_INT": 42, "OPT_ENUM": "b", "OPT_STR": "bonjour"}}'
attendu 1 cmake --preset "$preset" "-DLEPTON_OPTION_demoopt_OPT_INT=101" > "$dir/hors-bornes.log" 2>&1
grep -A2 "CMake Error" "$dir/hors-bornes.log" | head -6
attendu 1 cmake --preset "$preset" "-DLEPTON_OPTION_demoopt_OPT_ENUM=c" > "$dir/hors-valeurs.log" 2>&1
grep -A2 "CMake Error" "$dir/hors-valeurs.log" | head -6
attendu 1 cmake --preset "$preset" "-DLEPTON_OPTION_demoopt_OPT_BOOL=peut-etre" > "$dir/non-booleen.log" 2>&1
grep -A2 "CMake Error" "$dir/non-booleen.log" | head -6
attendu 0 cmake --preset "$preset" "-DLEPTON_OPTION_demoopt_OPT_INT=42" > "$dir/retour.log" 2>&1

etape "trunk sans fichier régulier ni lien cassé"
cd "$dir" || exit 1
find "$root/trunk" -type f ! -name .scion.grafted.list
find -L "$root/trunk" -type l
attendu 0 lepton seed status -C "$root" > "$dir/status.log" 2>&1
echo "essai : succès"
