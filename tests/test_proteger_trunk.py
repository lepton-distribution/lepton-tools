"""ENV-44 (D3, PA-75) : hook PreToolUse `.claude/hooks/proteger-trunk.py`.

Le hook refuse toute écriture dans `<rootstock>/trunk/` et `<rootstock>/depots/tiers/` (code 2) et
laisse passer les lectures et les écritures ailleurs (code 0). Les cas couvrent les deux sens, en
chemin absolu et relatif, vers le trunk et vers un clone tiers. Le hook est lancé comme Claude Code
le lance : JSON sur l'entrée standard.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

HOOK = Path(__file__).resolve().parents[1] / ".claude" / "hooks" / "proteger-trunk.py"


@pytest.fixture(scope="module")
def rs(tmp_path_factory) -> dict[str, str]:
    """Rootstock factice : signature, trunk, clone tiers, clone de greffon."""
    racine = tmp_path_factory.mktemp("hook") / "rs"
    (racine / "trunk" / "sys").mkdir(parents=True)
    (racine / "depots" / "tiers" / "lib" / "v1" / "Inc").mkdir(parents=True)
    (racine / "depots" / "lepton" / "fam" / "master" / "scion").mkdir(parents=True)
    (racine / ".scion.rootstock.signature").write_text("")
    return {
        "R": str(racine),
        "T": str(racine / "trunk"),
        "X": str(racine / "depots" / "tiers" / "lib" / "v1"),
        "C": str(racine / "depots" / "lepton" / "fam" / "master" / "scion"),
    }


def juge(outil: str, entree: dict, cwd: str) -> int:
    donnees = json.dumps({"tool_name": outil, "tool_input": entree, "cwd": cwd})
    return subprocess.run([sys.executable, str(HOOK)], input=donnees, capture_output=True,
                          text=True).returncode


# (commande, cwd) ; cwd « R » = racine du rootstock, « / » sinon.
REFUS = [
    ("echo x > {T}/a", "/"),
    ("echo x >> {X}/a", "/"),
    ("echo x | tee {T}/a", "/"),
    ("echo x | tee -a {X}/Inc/a.h", "/"),
    ("sed -i 's/a/b/' {T}/a", "/"),
    ("sed -i.bak 's/a/b/' {X}/a", "/"),
    ("sed -Ei 's/a/b/' {T}/a", "/"),
    ("perl -pi -e 's/a/b/' {T}/a", "/"),
    ("cp /tmp/a {T}/a", "/"),
    ("cp /tmp/a {T}", "/"),
    ("cp /tmp/a {X}/", "/"),
    ("cp -t {T} /tmp/a", "/"),
    ("mv {T}/a /tmp/a", "/"),
    ("mv /tmp/a {X}/a", "/"),
    ("rm -f {T}/a", "/"),
    ("rm -rf {X}", "/"),
    ("rmdir {T}/sys", "/"),
    ("ln -sf /tmp/a {T}/a", "/"),
    ("touch {X}/Inc/x.h", "/"),
    ("mkdir -p {T}/nouveau", "/"),
    ("truncate -s0 {T}/a", "/"),
    ("chmod +w {X}/Inc/a.h", "/"),
    ("install -m644 /tmp/a {T}/a", "/"),
    ("rsync -a /tmp/a/ {T}/", "/"),
    ("dd if=/tmp/a of={T}/a", "/"),
    ("patch -p1 -d {T} < /tmp/p", "/"),
    ("patch {X}/a /tmp/p", "/"),
    ("find {T} -name '*.o' -delete", "/"),
    ("find {T} -name '*.o' -exec rm {{}} +", "/"),
    ("find {X} -name '*.h' -exec sed -i s/a/b/ {{}} \\;", "/"),
    ("ls {T}/*.tmp | xargs rm", "/"),
    ("ls {X} | xargs -I F cp /tmp/a F", "/"),
    ("bash -c 'rm {T}/a'", "/"),
    ("sh -c \"echo x > {X}/a\"", "/"),
    ("eval rm {T}/a", "/"),
    ("sudo tee {T}/a < /tmp/a", "/"),
    ("env A=1 rm {T}/a", "/"),
    ("A=1 B=2 touch {T}/a", "/"),
    ("git -C {X} checkout v0", "/"),
    ("git -C {X} reset --hard", "/"),
    ("git -C {X} branch -D x", "/"),
    ("git -C {X} tag v2", "/"),
    ("git -C {X} config user.name x", "/"),
    ("git -C {X} remote add o /tmp/o", "/"),
    ("git -C {X} fetch", "/"),
    ("git rm {T}/a", "/"),
    ("ROOT={R}; rm $ROOT/trunk/a", "/"),
    ("rm $ROOT/depots/tiers/lib/a", "/"),
    ("cd {R} && rm trunk/a", "/"),
    ("cd {R} && cp /tmp/a depots/tiers/lib/", "/"),
    ("cd {T} && touch a", "/"),
    ("cd {T}; echo x > a", "/"),
    ("cd {T}/sys && ln -s /tmp/a", "/"),
    ("cd {X} && git checkout v0", "/"),
    ("cd {R}/depots && rm tiers/lib/v1/a", "/"),
    ("rm trunk/a", "R"),
    ("cp /tmp/a depots/tiers/lib/v1/", "R"),
    ("mkdir -p /tmp/x\nrm -rf {T}/sys", "/"),
    ("for f in {T}/a {T}/b; do\n  rm $f\ndone", "/"),
    ("if true; then touch {X}/a; fi", "/"),
    ("echo $(rm {T}/a)", "/"),
    ("echo `rm {T}/a`", "/"),
    ("(cd {T} && touch a)", "/"),
    ("cat > {T}/a <<'FIN'\nx\nFIN", "/"),
    ("cat <<FIN > {X}/a\nx\nFIN", "/"),
    ("bash <<'FIN'\nrm {T}/a\nFIN", "/"),
    ("cat <<'FIN' > /tmp/a\nx\nFIN\nrm {T}/a", "/"),
    ("python3 x.py > {X}/sortie.txt", "/"),
    ("unknowncmd --force; cp /tmp/a {T}/a", "/"),
    ("echo 'non fermé > {T}/a", "/"),          # shlex échoue : ancienne règle sur le texte
]

ACCEPTE = [
    ("diff -r {X}/Inc /tmp/a", "/"),
    ("grep -rn HAL_Init {X}", "/"),
    ("mkdir -p /tmp/x\ndiff -r {X}/Inc /tmp/x", "/"),
    ("mkdir -p /tmp/x && diff -r {X}/Inc /tmp/x", "/"),
    ("cp {T}/sys/a.c /tmp/a.c", "/"),
    ("cp -R {X}/Inc /tmp/inc", "/"),
    ("grep -rn mkdir {T}/sys", "/"),
    ("grep -rn 'rm -rf' {T}", "/"),
    ("find {T} -type l | wc -l", "/"),
    ("find {T} -type l ! -exec test -e {{}} \\; -print", "/"),
    ("find {X} -name '*.h' -exec cp {{}} /tmp/ \\;", "/"),
    ("readelf --debug-dump=line build/x.elf | grep -c depots/tiers/", "/"),
    ("git -C {X} log --oneline -1", "/"),
    ("git -C {X} status --short", "/"),
    ("git -C {X} branch --show-current", "/"),
    ("git -C {X} rev-parse --short HEAD", "/"),
    ("git -C {X} remote -v", "/"),
    ("git -C {X} remote get-url origin", "/"),
    ("git -C {X} config --get remote.origin.url", "/"),
    ("git -C {X} tag -l", "/"),
    ("git -C {X} branch", "/"),
    ("git -C {C} commit -m 'corrige trunk/ et depots/tiers/'", "/"),
    ("ls {T}/ 2>/dev/null > /tmp/liste", "/"),
    ("ls {T} 2>&1 | head", "/"),
    ("for f in {T}/a {T}/b; do\n  test -L $f || echo $f\ndone\ntouch /tmp/fin", "/"),
    ("cd {T} && ls -la && cat sys/a", "/"),
    ("cd {T} && cmake -S . -B ../build/p", "/"),
    ("cd {T} && O=/tmp/o; mkdir -p $O/x; ctest -N > $O/x/l.txt 2>&1", "/"),
    ("cd {T} && cd /tmp && touch a", "/"),
    ("cat trunk/sys/a", "R"),
    ("cp /tmp/a {C}/a", "/"),
    ("sed -i 's/a/b/' {C}/f", "/"),
    ("echo x > /tmp/trunk.log", "/"),
    ("echo x > {C}/trunkless.txt", "/"),
    ("mv /tmp/a /tmp/b", "/"),
    ("rm -rf /tmp/essai", "/"),
    ("arm-none-eabi-readelf -S {T}/../build/x.elf", "/"),
    ("sha256sum {X}/Inc/*.h > /tmp/sommes", "/"),
    ("bash -c 'grep -rn x {T}'", "/"),
    ("ls {T} | xargs -n1 echo", "/"),
    ("python3 -I script.py {X}", "/"),
    ("python3 -I - <<'FIN'\np = '<ROOTSTOCK>/trunk/' ; rm = 1 > 0\nFIN", "/"),
    ("cat <<'FIN' > /tmp/note.md\necho x > {T}/a ; rm -rf {X}\nFIN", "/"),
]


def _cas(gabarit: str, cwd: str, rs: dict[str, str]) -> tuple[str, str]:
    return gabarit.format(**rs), rs["R"] if cwd == "R" else "/"


@pytest.mark.parametrize("gabarit,cwd", REFUS)
def test_ecriture_refusee(rs, gabarit, cwd):
    commande, rep = _cas(gabarit, cwd, rs)
    assert juge("Bash", {"command": commande}, rep) == 2, commande


@pytest.mark.parametrize("gabarit,cwd", ACCEPTE)
def test_lecture_acceptee(rs, gabarit, cwd):
    commande, rep = _cas(gabarit, cwd, rs)
    assert juge("Bash", {"command": commande}, rep) == 0, commande


@pytest.mark.parametrize("outil,cle", [("Write", "file_path"), ("Edit", "file_path"),
                                       ("MultiEdit", "file_path"), ("NotebookEdit", "notebook_path")])
def test_outils_fichier(rs, outil, cle):
    assert juge(outil, {cle: rs["T"] + "/sys/a.c"}, "/") == 2
    assert juge(outil, {cle: rs["X"] + "/Inc/a.h"}, "/") == 2
    assert juge(outil, {cle: "trunk/sys/a.c"}, rs["R"]) == 2
    assert juge(outil, {cle: rs["C"] + "/a.c"}, "/") == 0


def test_entree_illisible():
    r = subprocess.run([sys.executable, str(HOOK)], input="pas du json", capture_output=True, text=True)
    assert r.returncode == 0
