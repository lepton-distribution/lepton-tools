#!/usr/bin/env python3
"""Essai du hook proteger-trunk.py sur des commandes types (lecture seule : le hook ne fait que juger)."""
import json
import subprocess
import sys

HOOK = "/Users/cle_d_anton/lepton-tools-dev/lepton-tools/.claude/hooks/proteger-trunk.py"
R = "/Users/cle_d_anton/lepton"
T = R + "/trunk"
X = R + "/depots/tiers/stm32f4xx-hal-driver/v1.8.5"

CAS = [
    # (attendu, commande) attendu : "refus" ou "accepte"
    ("accepte", f"diff -r {X}/Inc /tmp/a"),
    ("accepte", f"grep -rn HAL_Init {X}/Src"),
    ("accepte", f"mkdir -p /tmp/x\ndiff -r {X}/Inc /tmp/x"),
    ("accepte", f"mkdir -p /tmp/x && diff -r {X}/Inc /tmp/x"),
    ("accepte", f"cp {T}/sys/a.c /tmp/a.c"),
    ("accepte", f"grep -rn mkdir {T}/sys"),
    ("accepte", f"find {T} -type l | wc -l"),
    ("accepte", f"readelf --debug-dump=line build/x.elf | grep -c depots/tiers/"),
    ("accepte", f"git -C {X} log --oneline -1"),
    ("accepte", f"ls {T}/ 2>/dev/null > /tmp/liste"),
    ("accepte", f"for f in {T}/a {T}/b; do\n  test -L $f || echo $f\ndone\ntouch /tmp/fin"),
    ("refus", f"echo x > {T}/a"),
    ("refus", f"echo x >> {X}/a"),
    ("refus", f"echo x | tee {T}/a"),
    ("refus", f"sed -i 's/a/b/' {T}/a"),
    ("refus", f"sed -i.bak 's/a/b/' {X}/a"),
    ("refus", f"cp /tmp/a {T}/a"),
    ("refus", f"cp /tmp/a {X}/"),
    ("refus", f"mv {T}/a /tmp/a"),
    ("refus", f"rm -f {T}/a"),
    ("refus", f"rm -rf {X}"),
    ("refus", f"ln -sf /tmp/a {T}/a"),
    ("refus", f"touch {X}/Inc/x.h"),
    ("refus", "cd ~/lepton && rm trunk/a"),
    ("refus", "cd ~/lepton && cp /tmp/a depots/tiers/x/"),
    ("refus", f"cd {T} && touch a"),
    ("refus", f"cd {T} && echo x > a"),
    ("refus", f"cp /tmp/a {T}"),
    ("refus", f"sudo tee {T}/a < /tmp/a"),
    ("refus", f"find {T} -name '*.o' -delete"),
    ("refus", f"find {T} -name '*.o' -exec rm {{}} +"),
    ("refus", f"ls {T}/*.tmp | xargs rm"),
    ("refus", f"bash -c 'rm {T}/a'"),
    ("refus", f"rsync -a /tmp/a/ {T}/"),
    ("refus", f"perl -pi -e 's/a/b/' {T}/a"),
    ("refus", f"truncate -s0 {T}/a"),
    ("refus", f"chmod +w {X}/Inc/a.h"),
    ("refus", f"patch -p1 -d {T} < /tmp/p"),
    ("refus", f"install -m644 /tmp/a {T}/a"),
    ("refus", f"dd if=/tmp/a of={T}/a"),
    ("refus", f"git -C {X} checkout v1.8.4"),
    ("refus", f"ROOT={R}; rm $ROOT/trunk/a"),
]


def juge(commande: str, hook: str) -> str:
    entree = json.dumps({"tool_name": "Bash", "tool_input": {"command": commande}, "cwd": "/tmp"})
    r = subprocess.run([sys.executable, hook], input=entree, capture_output=True, text=True)
    return "refus" if r.returncode == 2 else "accepte"


def main() -> int:
    hook = sys.argv[1] if len(sys.argv) > 1 else HOOK
    ecarts = 0
    for attendu, cmd in CAS:
        obtenu = juge(cmd, hook)
        marque = "ok " if obtenu == attendu else "ÉCART"
        if obtenu != attendu:
            ecarts += 1
        print(f"{marque} attendu={attendu:7} obtenu={obtenu:7} | {cmd.replace(chr(10), ' ⏎ ')[:110]}")
    print(f"{len(CAS)} cas, {ecarts} écarts")
    return 1 if ecarts else 0


if __name__ == "__main__":
    sys.exit(main())
