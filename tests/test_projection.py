"""ENV-41 (PA-69) : greffon porteur d'une projection scion (dépôt tiers sans `scion/`, scion ≥ 0.6.1.0).

La famille factice porte dans `scion/.scion/` une clé projetée `tiers@tiers-lib` ; ses fichiers
`Inc/t.h` et `Src/t.c` apparaissent dans le trunk sous `<famille>/hal/`, répertoire partagé avec
un fichier de la famille (`hal/NOTE.md`). Exigences : GRF-5 / CFG-5 (`check` par le trunk), GRA-5
(`seed lock`), GRA-6 (`seed status`), FIC-1 à FIC-3 (`file owner`, refus d'écriture), IDE-1
(`seed tree`), IDE-2 / IDE-4 (`generate`).
"""

import json
import os
import subprocess
from pathlib import Path

import pytest

from conftest import assert_trunk_clean, url
from lepton.cli import main
from test_generate import KERNEL_PRESETS, TOOLS, _workspace

FAMILY_DIR = "sys/root/src/kernel/dev/arch/cortexm/fam-test"
HAL = f"trunk/{FAMILY_DIR}/hal"
KEY = "tiers@tiers-lib"


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout


def _tiers_repo(path: Path) -> Path:
    """Dépôt tiers : pas de `scion/`, tag v1.0 ; un second commit après le tag."""
    for rel, text in {"Inc/t.h": "/* t.h */\n", "Src/t.c": "int t(void){return 0;}\n",
                      "Src/u.c": "/* non projeté */\n", "LICENSE.md": "licence\n"}.items():
        (path / rel).parent.mkdir(parents=True, exist_ok=True)
        (path / rel).write_text(text)
    subprocess.run(["git", "init", "-q", "-b", "master", str(path)], check=True)
    _git(path, "add", "-A")
    _git(path, "commit", "-q", "-m", "v1.0")
    _git(path, "tag", "v1.0")
    (path / "Inc/t.h").write_text("/* t.h v1.1 */\n")
    _git(path, "commit", "-q", "-am", "après v1.0")
    return path


@pytest.fixture
def repos(repos, tmp_path):
    """Noyau avec presets (generate) ; famille porteuse de `tiers@tiers-lib`."""
    (repos["kernel"] / "scion" / "CMakePresets.json").write_text(json.dumps(KERNEL_PRESETS))
    _git(repos["kernel"], "add", "-A")
    _git(repos["kernel"], "commit", "-q", "-m", "presets")
    tiers = _tiers_repo(tmp_path / "repos" / "tiers-lib")
    fam = repos["family"]
    dest = f"scion/{FAMILY_DIR}/hal"
    dot = fam / "scion" / ".scion"
    dot.mkdir(parents=True)
    (dot / ".scion.sources.list").write_text(f"tiers\ttiers-lib\tv1.0\t{url(tiers)}\n")
    (dot / ".scion.ramifications").write_text("tiers\ttiers-lib\tv1.0\n")
    (dot / ".scion.projections").write_text(f"tiers tiers-lib Inc/** {dest}/Inc/\n"
                                            f"tiers tiers-lib Src/t.c {dest}/Src/\n")
    (fam / dest / "NOTE.md").parent.mkdir(parents=True)
    (fam / dest / "NOTE.md").write_text("fichier de la famille dans un répertoire partagé\n")
    manifest = fam / "scion" / FAMILY_DIR / "lepton-greffon.json"
    data = json.loads(manifest.read_text())
    data["sources"] = ["uart.c", "hal/Src/t.c"]
    manifest.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    _git(fam, "add", "-A")
    _git(fam, "commit", "-q", "-m", "projection tiers-lib")
    repos["tiers"] = tiers
    return repos


@pytest.fixture
def tools(tmp_path, monkeypatch):
    bindir = tmp_path / "tools"
    bindir.mkdir()
    for name, version in TOOLS.items():
        (bindir / name).write_text(f"#!/bin/sh\necho '{version}'\n")
        (bindir / name).chmod(0o755)
    monkeypatch.setenv("PATH", f"{bindir}{os.pathsep}{os.environ['PATH']}")
    return bindir


def _json(capsys, *argv: str) -> tuple[int, dict]:
    capsys.readouterr()
    code = main([*argv, "--json"])
    return code, json.loads(capsys.readouterr().out)


def _tiers_clone(project: Path) -> Path:
    return project / "depots" / "tiers" / "tiers-lib" / "v1.0"


def test_projection_grafted(project):
    """Préalable : scion a projeté la clé du porteur (liens vers le clone tiers, au tag)."""
    link = project / HAL / "Inc" / "t.h"
    assert link.is_symlink() and link.resolve() == (_tiers_clone(project) / "Inc" / "t.h").resolve()
    assert link.read_text() == "/* t.h */\n"
    assert not (project / HAL / "Src" / "u.c").exists()
    assert (project / HAL / "NOTE.md").is_symlink()
    assert_trunk_clean(project)


def test_check_resolves_projected_sources_by_trunk(project, repos, capsys):
    """Le BSP factice de conftest n'a pas son script de liens : seules les anomalies `hal/` comptent."""
    capsys.readouterr()
    main(["check", "-C", str(project)])
    out = capsys.readouterr()
    assert "fam-test/lepton-greffon.json" not in out.out + out.err
    # un fichier déclaré absent du clone ET du trunk reste une anomalie
    manifest = repos["family"] / "scion" / FAMILY_DIR / "lepton-greffon.json"
    data = json.loads(manifest.read_text())
    data["sources"].append("hal/Src/absent.c")
    manifest.write_text(json.dumps(data))
    assert main(["check", "-C", str(project)]) == 1
    out = capsys.readouterr()
    assert "« hal/Src/absent.c » introuvable" in out.out + out.err
    assert "« hal/Src/t.c »" not in out.out + out.err


def test_seed_status_projection(project, capsys):
    code, r = _json(capsys, "seed", "status", "-C", str(project))
    assert code == 0
    s = next(s for s in r["scions"] if s["key"] == KEY)
    assert s["role"] == "projection" and s["projected_by"] == "fam-test" and s["in_seed"] is False
    assert s["version"] == "v1.0" and s["location"].endswith("tiers-lib")
    assert s["root"] == str(_tiers_clone(project).resolve())
    assert s["projection"] == {"Inc/t.h": f"{FAMILY_DIR}/hal/Inc/t.h", "Src/t.c": f"{FAMILY_DIR}/hal/Src/t.c"}
    fam = next(s for s in r["scions"] if s["name"] == "fam-test")
    assert "projection" not in fam and fam["role"] == "famille"
    capsys.readouterr()
    assert main(["seed", "status", "-C", str(project)]) == 0
    assert "projeté par fam-test, 2 fichier(s)" in capsys.readouterr().out


def test_file_owner_projected(project, capsys):
    code, r = _json(capsys, "file", "owner", str(project / HAL / "Inc" / "t.h"), "-C", str(project))
    assert code == 0 and r["kind"] == "link" and r["source"] == "link"
    assert r["owner"]["key"] == KEY and r["owner"]["projected_by"] == "fam-test"
    assert r["owner"]["clone_path"] == str((_tiers_clone(project) / "Inc" / "t.h").resolve())
    code, r = _json(capsys, "file", "owner", str(project / HAL / "NOTE.md"), "-C", str(project))
    assert code == 0 and r["owner"]["name"] == "fam-test" and "projected_by" not in r["owner"]


def test_projected_files_never_written(project, repos, capsys):
    """Refus explicite (PA-69) ; un fichier nouveau d'un répertoire partagé va au greffon ordinaire."""
    clone = _tiers_clone(project)
    before = _git(clone, "status", "--porcelain")
    capsys.readouterr()
    assert main(["file", "remove", str(project / HAL / "Inc" / "t.h"), "-C", str(project)]) == 1
    assert "dépôt tiers projeté par fam-test" in capsys.readouterr().err
    assert main(["file", "add", str(project / HAL / "Inc" / "n.h"), "-C", str(project)]) == 1
    assert "dépôt tiers projeté" in capsys.readouterr().err
    assert (project / HAL / "Inc" / "t.h").is_symlink() and _git(clone, "status", "--porcelain") == before
    # hal/ : feuilles de la famille (NOTE.md) et de la clé projetée → la famille
    assert main(["file", "add", str(project / HAL / "local.c"), "-C", str(project)]) == 0
    assert (repos["family"] / "scion" / FAMILY_DIR / "hal" / "local.c").is_file()
    assert (project / HAL / "local.c").is_symlink()
    assert_trunk_clean(project)


def test_seed_tree_counts_projected_files(project, capsys):
    capsys.readouterr()
    assert main(["seed", "tree", "-C", str(project)]) == 0
    out = capsys.readouterr()
    text = out.out + out.err
    assert "tiers-lib : 1 source(s), 1 en-tête(s)" in text


def test_generate_omits_projected_clones(project, tools):
    assert main(["generate", "-C", str(project)]) == 0
    paths = [f["path"] for f in _workspace(project)["folders"]]
    assert not any("depots/tiers" in p for p in paths)
    assert any("fam-test" in p for p in paths)


def test_seed_lock_projected(project, capsys):
    assert main(["seed", "lock", "-C", str(project), "--no-cmake"]) == 0
    lock = json.loads(next((project / "depots").rglob("lepton-graine.lock.json")).read_text())
    entry = next(e for e in lock["scions"] if e["key"] == KEY)
    head = _git(_tiers_clone(project), "rev-parse", "HEAD").strip()
    assert entry["commit"] == head and entry["version"] == "v1.0"
    assert entry["projected_by"].endswith("fam-test")
    assert main(["seed", "lock", "--verify", "-C", str(project), "--no-cmake"]) == 0
    # clone tiers déplacé hors du commit figé : écart signalé, --restore ne le déplace pas
    _git(_tiers_clone(project), "checkout", "-q", "master")
    capsys.readouterr()
    assert main(["seed", "lock", "--verify", "-C", str(project), "--no-cmake"]) == 1
    assert "tiers-lib : commit" in capsys.readouterr().out
    assert main(["seed", "lock", "--restore", "-C", str(project), "--no-cmake"]) == 1
    out = capsys.readouterr()
    assert "clé projetée au commit" in out.out + out.err
    assert _git(_tiers_clone(project), "rev-parse", "HEAD").strip() != head


def _projected_links(project: Path) -> dict[str, str]:
    trunk = project / "trunk"
    return {str(p.relative_to(trunk)): os.readlink(p) for p in trunk.rglob("*")
            if p.is_symlink() and "depots/tiers" in os.readlink(p)}


def test_seed_replace_porteur_garde_les_projections(project, repos):
    """ENV-44 (D1, P-G6 de scion 0.6.2.0) : seed replace du porteur rend ses fichiers projetés."""
    before = _projected_links(project)
    assert before
    code = main(["seed", "replace", "fam-test", f"{url(repos['family'])}@master", "-C", str(project),
                 "--no-cmake"])
    assert code == 0
    assert _projected_links(project) == before
    assert (project / HAL / "Inc" / "t.h").read_text() == "/* t.h */\n"
    assert_trunk_clean(project)


# --- clone partagé par deux clés projetées (P-V2, P-G3 ; ENV-48, cas STM32CubeWL) ------------------

KEY2 = "tiers@tiers-lib::extra"


def _share_clone(project: Path, repos) -> None:
    """Seconde clé `tiers-lib::extra` (même préfixe, même version : même clone) qui projette
    `LICENSE.md` à côté des fichiers de la première ; regreffe par scion."""
    fam = repos["family"]
    dot = fam / "scion" / ".scion"
    dest = f"scion/{FAMILY_DIR}/hal"
    with open(dot / ".scion.sources.list", "a") as f:
        f.write(f"tiers\ttiers-lib::extra\tv1.0\t{url(repos['tiers'])}\n")
    with open(dot / ".scion.ramifications", "a") as f:
        f.write("tiers\ttiers-lib::extra\tv1.0\n")
    with open(dot / ".scion.projections", "a") as f:
        f.write(f"tiers tiers-lib::extra LICENSE.md {dest}/\n")
    _git(fam, "add", "-A")
    _git(fam, "commit", "-q", "-m", "clé partagée")
    grafted = (project / "trunk" / ".scion.grafted.list").read_text().split()
    seed = next(f for f in grafted if f.endswith("/scion/.scion"))[: -len("/scion/.scion")]
    for argv in (["seed-clone", "--seed", seed], ["graft"]):
        subprocess.run(["scion", *argv], cwd=project, check=True, capture_output=True, text=True)


def test_shared_clone_tables_and_owner(project, repos, capsys):
    _share_clone(project, repos)
    link = project / HAL / "LICENSE.md"
    assert link.is_symlink() and link.resolve() == (_tiers_clone(project) / "LICENSE.md").resolve()
    code, r = _json(capsys, "seed", "status", "-C", str(project))
    assert code == 0
    tables = {s["key"]: s["projection"] for s in r["scions"] if s.get("role") == "projection"}
    assert tables[KEY] == {"Inc/t.h": f"{FAMILY_DIR}/hal/Inc/t.h", "Src/t.c": f"{FAMILY_DIR}/hal/Src/t.c"}
    assert tables[KEY2] == {"LICENSE.md": f"{FAMILY_DIR}/hal/LICENSE.md"}
    for trunk_path, key in ((link, KEY2), (project / HAL / "Inc" / "t.h", KEY)):
        code, o = _json(capsys, "file", "owner", str(trunk_path), "-C", str(project))
        assert code == 0 and o["owner"]["key"] == key
    # fichier du clone qu'aucune clé ne projette : première clé, écriture refusée
    code, o = _json(capsys, "file", "owner", str(_tiers_clone(project) / "Src" / "u.c"), "-C", str(project))
    assert code == 0 and o["owner"]["key"] == KEY
    assert_trunk_clean(project)


@pytest.mark.parametrize("motif, dest, rel, attendu", [
    ("Inc/**", "scion/a/inc/", "Inc/Legacy/x.h", {"a/inc/Legacy/x.h"}),
    ("Inc/**", "scion/a/inc/", "Src/x.c", set()),
    ("**", "scion/t/", "d/e.c", {"t/d/e.c"}),
    ("Conf/*", "scion/r/Conf/", "Conf/a.h", {"r/Conf/a.h"}),
    ("Conf/*", "scion/r/Conf/", "Conf/sub/a.h", set()),
    ("*.h", "scion/r/", "radio.h", {"r/radio.h"}),
    ("*.h", "scion/r/", "Conf/a.h", set()),
    ("Utilities/conf/*.[ch]", "scion/u/conf/", "Utilities/conf/x.c", {"u/conf/x.c"}),
    ("Utilities/conf/*.[ch]", "scion/u/conf/", "Utilities/conf/LICENSE.md", set()),
    ("Include/stm32f4[23]9xx.h", "scion/i/", "Include/stm32f439xx.h", {"i/stm32f439xx.h"}),
    ("Inc/a.h", "scion/x/", "inc/a.h", set()),                     # casse exacte (P-K1)
    ("Source/Templates/iar/s.s", "scion/c/startup/iar/", "Source/Templates/iar/s.s", {"c/startup/iar/s.s"}),
    ("LICENSE", "scion/r/COPYING", "LICENSE", {"r/COPYING"}),     # forme fichier renommée (P-T3)
])
def test_projected_paths(motif, dest, rel, attendu):
    from lepton.rootstock import ProjectionLine, projected_paths
    assert projected_paths([ProjectionLine("tiers@k", motif, dest)], rel) == attendu


def test_projected_paths_exclusion():
    from lepton.rootstock import ProjectionLine, projected_paths
    lines = [ProjectionLine("tiers@k", "Inc/**", "scion/a/inc/"),
             ProjectionLine("tiers@k", "Inc/Legacy/stm32_hal_legacy.h")]
    assert projected_paths(lines, "Inc/Legacy/stm32_hal_legacy.h") == set()
    assert projected_paths(lines, "Inc/a.h") == {"a/inc/a.h"}
