"""Relevé en lecture seule des clones projetés d'un rootstock (ENV-52, tâche 1)."""
import os, subprocess, sys
from collections import defaultdict
from pathlib import Path

root = Path(sys.argv[1]).resolve()
tiers = root / "depots" / "tiers"
clones = sorted(p for p in tiers.glob("*/*") if (p / ".git").exists())
links = defaultdict(set)      # clone -> chemins source (relatifs au clone)
dests = defaultdict(int)
for dirpath, dirnames, filenames in os.walk(root / "trunk"):
    for name in dirnames + filenames:
        p = Path(dirpath) / name
        if p.is_symlink():
            target = Path(os.path.normpath(Path(dirpath) / os.readlink(p)))
            for c in clones:
                if target.is_relative_to(c):
                    links[c].add(str(target.relative_to(c)))
                    dests[c] += 1
def du(path, exclude_git):
    total = 0; n = 0
    for dirpath, dirnames, filenames in os.walk(path):
        if exclude_git and ".git" in dirnames and Path(dirpath) == path:
            dirnames.remove(".git")
        for f in filenames:
            fp = Path(dirpath) / f
            if not fp.is_symlink():
                total += fp.stat().st_size
            n += 1
    return n, total
def git(c, *a):
    return subprocess.run(["git", "-C", str(c), *a], capture_output=True, text=True).stdout
print("| clone | suivis (ls-files) | suivis au commit (ls-tree) | extraits (fichiers hors .git) | arbre extrait (Mo) | .git (Mo) | sources projetées | liens du trunk | répertoires de base | sparse |")
print("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
for c in clones:
    ls = len(git(c, "ls-files").splitlines())
    lt = len(git(c, "ls-tree", "-r", "--name-only", "HEAD").splitlines())
    n, size = du(c, True)
    _, gsize = du(c / ".git", False)
    sparse = git(c, "config", "--get", "core.sparseCheckout").strip() or "—"
    bases = sorted({str(Path(s).parent) for s in links[c]})
    print(f"| `{c.relative_to(tiers)}` | {ls} | {lt} | {n} | {size/1e6:.1f} | {gsize/1e6:.1f} | {len(links[c])} | {dests[c]} | {len(bases)} | {sparse} |")
