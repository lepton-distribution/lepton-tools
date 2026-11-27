"""EP-1 (chantier espace-projet, PA-E2) : greffon de type projet, dépôt propre, qui remplace `project/`
de la graine ; critère de la graine de référence réduit à « pas de lepton-graine.json » ; graine à
l'ancien format refusée ; T8 : greffon projet greffé en régime de référence, rien n'est écrit."""

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from conftest import MKCONF, PROJECT_XML, _git, url
from lepton.cli import main
from lepton.errors import LeptonError
from lepton.rootstock import Rootstock, find_manifest, project_key
from lepton.scion_runner import scion
from lepton.seed import parse_location
from test_generate import repos, tools  # noqa: F401  (fixtures : noyau à presets, outils factices)
from test_reference_seed import reference  # noqa: F401  (fixture : graine de référence commitée)

PROJECT_MANIFEST = {"nom": "demo", "type": "projet", "version": "0.1.0", "description": "Greffon projet."}
XML_TEXT = '<mklepton version="2">\n<kernel>\n   <heap size="10000" />\n</kernel>\n</mklepton>\n'


def _project_repo(path: Path, manifest: dict = PROJECT_MANIFEST, files: dict | None = None,
                  subpath: str = "") -> Path:
    """Dépôt git d'un greffon projet : scion/sys/user/<nom>/lepton-greffon.json (sous `subpath`)."""
    stem = path / subpath / "scion" if subpath else path / "scion"
    d = stem / "sys" / "user" / manifest["nom"]
    d.mkdir(parents=True)
    (d / "lepton-greffon.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    for rel, text in (files or {}).items():
        (stem / rel).parent.mkdir(parents=True, exist_ok=True)
        (stem / rel).write_text(text)
    subprocess.run(["git", "init", "-q", "-b", "master", str(path)], check=True)
    _git(path, "add", "-A")
    _git(path, "commit", "-q", "-m", "initial")
    return path


def _seed_new(root: Path, repos: dict, *extra: str, mkconf: bool = True) -> int:
    return main(["seed", "new", "demo", "-C", str(root), "--bsp", "board-q",
                 *(["--mkconf", MKCONF] if mkconf else []),
                 "--origin", f"lepton-noyau={url(repos['kernel'])}@master",
                 "--origin", f"fam-test={repos['family']}",
                 "--origin", f"board-q={repos['bsp']}", *extra])


def _ls(repo: Path) -> list[str]:
    return _git(repo, "ls-files").split()


def _status(root: Path, capsys) -> dict:
    capsys.readouterr()
    main(["seed", "status", "--json", "-C", str(root)])
    return json.loads(capsys.readouterr().out)


# --- lecteur de manifeste --------------------------------------------------------------------------
def test_find_manifest_projet_sous_sys_user(tmp_path):
    repo = _project_repo(tmp_path / "p")
    m = find_manifest(repo)
    assert m.kind == "projet" and m.path == repo / "scion/sys/user/demo/lepton-greffon.json"


def test_find_manifest_deux_projets_refuse(tmp_path):
    repo = _project_repo(tmp_path / "p")
    other = repo / "scion/sys/user/autre"
    other.mkdir()
    (other / "lepton-greffon.json").write_text(json.dumps(dict(PROJECT_MANIFEST, nom="autre")))
    with pytest.raises(LeptonError, match="2 manifestes sous scion/sys/user/"):
        find_manifest(repo)


# --- seed new : greffon projet créé ------------------------------------------------------------------
def test_seed_new_cree_le_greffon_projet(project):
    seed_root = project / "depots/lepton-seed/demo"
    repo = project / "depots/lepton-project/demo"
    assert not (seed_root / "project").exists()
    assert not any(p.startswith("project/") for p in _ls(seed_root))
    assert {"README.md", "scion/sys/user/demo/lepton-greffon.json", f"scion/{PROJECT_XML}"} <= set(_ls(repo))
    assert _git(repo, "status", "--porcelain") == ""
    assert "Greffon projet demo créé par lepton seed new" in _git(repo, "log", "--format=%s")
    manifest = json.loads((repo / "scion/sys/user/demo/lepton-greffon.json").read_text())
    assert manifest["type"] == "projet" and manifest["nom"] == "demo"
    src = next(s for s in Rootstock(project).sources() if s.key == project_key("demo"))
    assert (src.key, src.version, src.location, src.subpath) == ("lepton@project-demo", "*",
                                                                  "depots/lepton-project/demo", "")
    assert (project / "trunk" / PROJECT_XML).resolve() == (repo / "scion" / PROJECT_XML).resolve()
    assert (project / "trunk/sys/user/demo/lepton-greffon.json").is_symlink()


def test_seed_new_project_repo(tmp_path, repos):
    repo = tmp_path / "ailleurs" / "demo-projet"
    assert _seed_new(tmp_path / "rs", repos, "--project-repo", str(repo)) == 0
    assert (repo / "scion" / PROJECT_XML).is_file()
    src = next(s for s in Rootstock(tmp_path / "rs").sources() if s.key == project_key("demo"))
    assert src.location == str(repo.resolve())


def test_seed_new_sans_mkconf_refuse(tmp_path, repos, capsys):
    assert _seed_new(tmp_path / "rs", repos, mkconf=False) == 1
    assert "--mkconf absent" in capsys.readouterr().err
    assert not (tmp_path / "rs").exists()


def test_seed_new_nom_du_bsp_refuse(tmp_path, repos, capsys):
    code = main(["seed", "new", "board-q", "-C", str(tmp_path / "rs"), "--bsp", "board-q", "--mkconf", MKCONF,
                 "--origin", f"fam-test={repos['family']}", "--origin", f"board-q={repos['bsp']}"])
    assert code == 1 and "distinct du noyau et du BSP" in capsys.readouterr().err


# --- seed new : greffon projet désigné ---------------------------------------------------------------
def test_seed_new_projet_designe_fournit_son_xml(tmp_path, repos):
    repo = _project_repo(tmp_path / "projet-demo", files={PROJECT_XML: XML_TEXT})
    assert _seed_new(tmp_path / "rs", repos, "--origin", f"demo={url(repo)}@master", mkconf=False) == 0
    rs = Rootstock(tmp_path / "rs")
    graine = json.loads(rs.seed_manifest_path().read_text())
    assert graine["mklepton_xml"] == PROJECT_XML
    src = next(s for s in rs.sources() if s.key == project_key("demo"))
    assert (src.version, src.location) == ("master", url(repo))
    assert (rs.trunk / PROJECT_XML).resolve().is_relative_to(rs.depots / "lepton/project-demo/master")
    assert not (tmp_path / "rs/depots/lepton-project").exists()


def test_seed_new_projet_designe_depot_partage(tmp_path, repos):
    """Dépôt partagé avec BSP et applications : le greffon projet à son propre sous-chemin (:PATH)."""
    repo = _project_repo(tmp_path / "partage", files={PROJECT_XML: XML_TEXT}, subpath="projet")
    assert _seed_new(tmp_path / "rs", repos, "--origin", f"demo={repo}:projet", mkconf=False) == 0
    src = next(s for s in Rootstock(tmp_path / "rs").sources() if s.key == project_key("demo"))
    assert (src.version, src.subpath) == ("*", "projet")


def test_seed_new_projet_designe_sans_xml(tmp_path, repos, capsys):
    repo = _project_repo(tmp_path / "projet-demo")
    assert _seed_new(tmp_path / "rs", repos, "--origin", f"demo={repo}", mkconf=False) == 1
    assert f"greffon projet désigné sans {PROJECT_XML}" in capsys.readouterr().err


def test_seed_new_projet_designe_avec_mkconf(tmp_path, repos, capsys):
    repo = _project_repo(tmp_path / "projet-demo")
    assert _seed_new(tmp_path / "rs", repos, "--origin", f"demo={repo}") == 0
    assert (repo / "scion" / PROJECT_XML).is_file()            # copié dans le dépôt désigné, non commité
    assert "greffon projet modifié, non commité" in capsys.readouterr().out


def test_seed_new_projet_designe_mauvais_type(tmp_path, repos, capsys):
    repo = _project_repo(tmp_path / "projet-demo", manifest=dict(PROJECT_MANIFEST, nom="autre"))
    assert _seed_new(tmp_path / "rs", repos, "--origin", f"demo={repo}") == 1
    assert "manifeste « autre » de type « projet », attendu « demo » de type « projet »" in capsys.readouterr().err


def test_seed_new_project_repo_et_origin_exclusifs(tmp_path, repos, capsys):
    repo = _project_repo(tmp_path / "projet-demo", files={PROJECT_XML: XML_TEXT})
    assert _seed_new(tmp_path / "rs", repos, "--origin", f"demo={repo}", "--project-repo",
                     str(tmp_path / "x"), mkconf=False) == 1
    assert "créé ou désigné, pas les deux" in capsys.readouterr().err


# --- commandes sur une graine de projet ------------------------------------------------------------
def test_generate_presets_dans_le_greffon_projet(project, tools, capsys):  # noqa: F811
    assert main(["generate", "-C", str(project)]) == 0
    out = capsys.readouterr().out
    repo = project / "depots/lepton-project/demo"
    presets = repo / "scion/CMakeUserPresets.json"
    assert (project / "trunk/CMakeUserPresets.json").resolve() == presets.resolve()
    assert f"git -C {repo} add -A" in out
    workspace = json.loads((project / "demo.code-workspace").read_text().split("\n", 1)[1])
    names = [f["name"] for f in workspace["folders"]]
    assert "git · demo" in names and names.index("git · demo") > names.index("git · graine demo")
    assert _git(project / "depots/lepton-seed/demo", "status", "--porcelain") == ""


def test_status_role_projet_et_stem(project, capsys):
    s = next(x for x in _status(project, capsys)["scions"] if x["key"] == project_key("demo"))
    assert s["role"] == "projet" and s["name"] == "demo"
    assert s["stem"] == str((project / "depots/lepton-project/demo/scion").resolve())


def test_seed_remove_greffon_projet_refuse(project, capsys):
    assert main(["seed", "remove", "demo", "-C", str(project), "--no-cmake"]) == 1
    assert "est le greffon projet de la graine" in capsys.readouterr().err


def test_seed_lock_fige_le_greffon_projet(project):
    assert main(["seed", "lock", "-C", str(project), "--no-cmake"]) == 0
    lock = json.loads((Rootstock(project).seed_dot() / "lepton-graine.lock.json").read_text())
    entry = next(e for e in lock["scions"] if e["key"] == project_key("demo"))
    assert entry["commit"] == _git(project / "depots/lepton-project/demo", "rev-parse", "HEAD").strip()


def test_check_greffon_projet_de_la_graine_non_greffe(project, capsys):
    path = Rootstock(project).seed_manifest_path()
    graine = json.loads(path.read_text())
    graine["projet"]["nom"] = "autre"
    path.write_text(json.dumps(graine, indent=2, ensure_ascii=False))
    capsys.readouterr()
    assert main(["check", "-C", str(project)]) == 1
    out = capsys.readouterr().out
    assert "greffon projet « autre » non greffé" in out
    assert "greffon(s) de type projet greffé(s) en plus de « autre » : demo" in out


# --- graine à l'ancien format (project/) -----------------------------------------------------------
@pytest.mark.parametrize("command", [["seed", "status"], ["check"], ["generate"], ["seed", "tree"]])
def test_graine_ancien_format_refusee(project, capsys, command):
    (project / "depots/lepton-seed/demo/project/scion").mkdir(parents=True)
    capsys.readouterr()
    assert main([*command, "-C", str(project)]) == 1
    err = capsys.readouterr().err
    assert "graine à l'ancien format" in err and "lepton seed new" in err


def test_graine_ancien_format_sans_manifeste_refusee(project, capsys):
    """Ancienne « graine de projet abîmée » (project/ sans lepton-graine.json) : refus, pas de bascule
    vers le régime de référence."""
    Rootstock(project).seed_manifest_path().unlink()
    (project / "depots/lepton-seed/demo/project").mkdir()
    capsys.readouterr()
    assert main(["seed", "status", "-C", str(project)]) == 1
    assert "graine à l'ancien format" in capsys.readouterr().err


# --- T8 : greffon projet greffé en régime de référence ----------------------------------------------
@pytest.fixture
def reference_with_project(reference, tmp_path):  # noqa: F811
    repo = _project_repo(tmp_path / "lepton-basic", manifest=dict(PROJECT_MANIFEST, nom="lepton-basic"),
                         files={"sys/user/lepton-basic/etc/mkconf_x.xml": XML_TEXT})
    rs = Rootstock(reference)
    scion("seed-scion-add", "--seed", str(rs.seed_root()), project_key("lepton-basic"),
          *parse_location(str(repo), rootstock=reference).scion_args(), cwd=reference)
    scion("seed-clone", "--seed", str(rs.seed_root()), cwd=reference)
    scion("graft", cwd=reference)
    seed = rs.seed_root()
    _git(seed, "add", "-A")
    _git(seed, "commit", "-q", "-m", "greffon projet")
    return reference, repo


def test_reference_avec_greffon_projet_reste_reference(reference_with_project, tools, capsys):  # noqa: F811
    root, repo = reference_with_project
    rs = Rootstock(root)
    assert rs.is_reference_seed()
    s = next(x for x in _status(root, capsys)["scions"] if x["key"] == project_key("lepton-basic"))
    assert s["role"] == "projet"
    capsys.readouterr()
    assert main(["generate", "-C", str(root)]) == 0
    assert "aucun CMakeUserPresets.json écrit" in capsys.readouterr().out
    assert not (root / "trunk/CMakeUserPresets.json").exists()
    assert _git(repo, "status", "--porcelain") == ""
    assert _git(rs.seed_root(), "status", "--porcelain") == ""
    assert main(["seed", "mkconf", "import", MKCONF, "-C", str(root)]) == 1
    assert "graine de référence" in capsys.readouterr().err
