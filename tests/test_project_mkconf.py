"""ENV-12 lot 2, O5 (CFG-1) : XML mklepton du projet dans la graine, applications déclarées.

Décision du 2026-10-20 : XML et fichiers `src_file` copiés dans `<graine>/project/scion/sys/user/<projet>/etc/`,
greffés par le greffon local du projet ; `<bin>` ajouté / retiré par `scion new/remove` et
`seed add/remove` d'une application ; `lepton seed mkconf import` pour une graine existante.
"""

import json
import subprocess
from pathlib import Path

import pytest

from conftest import MKCONF, PROJECT_XML, assert_trunk_clean, url
from lepton import mkconf
from lepton.cli import main
from lepton.errors import LeptonError

REF = """<?xml version="1.0" encoding="UTF-8"?>
<mklepton version="2">
<kernel>
   <heap size="10000" />
</kernel>
<!-- /usr/sbin -->
<binaries src_path="sbin" dest_path="sbin">
   <bin name="lsh" stack="2048" priority="100" timeslice="1" />
</binaries>
<files>
   <file name=".boot" src_file="sys/user/ref/etc/board/.boot" dest_path="etc" />
   <file name=".init" src_file="sys/user/ref/etc/board/.init" dest_path="etc" />
</files>
</mklepton>
"""


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout


@pytest.fixture
def repos(repos):
    """Noyau de conftest : XML de référence avec `<files>` (.boot, .init)."""
    scion = repos["kernel"] / "scion"
    (scion / MKCONF).write_text(REF)
    (scion / "sys/user/ref/etc/board").mkdir(parents=True)
    (scion / "sys/user/ref/etc/board/.boot").write_text("/dev/hd/hdb\n")
    (scion / "sys/user/ref/etc/board/.init").write_text("lsh &\n")
    _git(repos["kernel"], "add", "-A")
    _git(repos["kernel"], "commit", "-q", "-m", "xml de référence")
    return repos


def _seed(root: Path) -> Path:
    return root / "depots" / "lepton-seed" / "demo"


def _stem(root: Path) -> Path:
    return _seed(root) / "project" / "scion"


def _graine_path(root: Path) -> Path:
    return _seed(root) / "scion" / ".scion" / "lepton-graine.json"


def _graine(root: Path) -> dict:
    return json.loads(_graine_path(root).read_text(encoding="utf-8"))


def _xml(root: Path) -> str:
    return (_stem(root) / PROJECT_XML).read_text(encoding="utf-8")


# --------------------------------------------------------------------------
# mkconf.py (texte)
# --------------------------------------------------------------------------
def test_add_bin_bloc_existant_indentation_conservee():
    text = REF.replace('<files>', '<binaries src_path="bin" dest_path="bin">\n'
                                  '  <bin name="a" stack="1" priority="1" timeslice="1" />\n</binaries>\n<files>')
    new = mkconf.add_bin(text, "salut")
    assert '  <bin name="salut" stack="2048" priority="100" timeslice="1" />\n</binaries>' in new
    assert mkconf.add_bin(new, "salut") is None                  # idempotent
    assert mkconf.add_bin(new, "lsh") is None                    # déclaré dans un autre bloc


def test_add_bin_bloc_cree_avant_files_puis_retire():
    new = mkconf.add_bin(REF, "salut")
    block = ('<binaries src_path="bin" dest_path="bin">\n'
             '   <bin name="salut" stack="2048" priority="100" timeslice="1" />\n</binaries>\n')
    assert block in new and new.index(block) < new.index("<files>")
    removed = mkconf.remove_bin(new, "salut")
    assert "salut" not in removed and '<bin name="lsh"' in removed
    assert mkconf.remove_bin(removed, "salut") is None


def test_add_bin_sans_files_avant_fin():
    text = REF[:REF.index("<files>")] + "</mklepton>\n"
    new = mkconf.add_bin(text, "salut")
    assert new.endswith('timeslice="1" />\n</binaries>\n\n</mklepton>\n')


def test_project_copies_et_reecriture():
    copies = mkconf.project_copies(REF, "demo")
    assert copies == {"sys/user/ref/etc/board/.boot": "sys/user/demo/etc/.boot",
                      "sys/user/ref/etc/board/.init": "sys/user/demo/etc/.init"}
    new = mkconf.rewrite_src_files(REF, copies)
    assert 'src_file="sys/user/demo/etc/.boot"' in new and "etc/board" not in new
    assert 'src_path="sbin"' in new


def test_project_copies_meme_nom_refuse():
    text = REF.replace("board/.init", "autre/.boot")
    with pytest.raises(LeptonError, match="même nom de fichier"):
        mkconf.project_copies(text, "demo")


# --------------------------------------------------------------------------
# seed new
# --------------------------------------------------------------------------
def test_seed_new_copie_xml_et_fichiers(project):
    trunk, stem = project / "trunk", _stem(project)
    assert _graine(project)["mklepton_xml"] == PROJECT_XML
    for rel in (PROJECT_XML, "sys/user/demo/etc/.boot", "sys/user/demo/etc/.init"):
        link = trunk / rel
        assert link.is_symlink() and link.resolve() == (stem / rel).resolve()
    assert 'src_file="sys/user/demo/etc/.init"' in _xml(project)
    assert (stem / "sys/user/demo/etc/.init").read_text() == "lsh &\n"
    ref = (trunk / MKCONF).resolve()
    assert "depots" in ref.parts and ref.read_text() == REF       # modèle du noyau inchangé
    tracked = _git(_seed(project), "ls-files").split()
    assert f"project/scion/{PROJECT_XML}" in tracked and "project/scion/sys/user/demo/etc/.boot" in tracked
    assert not _git(_seed(project), "status", "--porcelain")
    assert_trunk_clean(project)


def test_seed_new_conflit_nom_projet(tmp_path, repos, capsys):
    root = tmp_path / "ref"
    code = main(["seed", "new", "ref", "-C", str(root), "--bsp", "board-q", "--mkconf", MKCONF,
                 "--origin", f"lepton-noyau={url(repos['kernel'])}@master",
                 "--origin", f"fam-test={repos['family']}", "--origin", f"board-q={repos['bsp']}"])
    assert code == 1
    assert "fourni par un autre greffon : conflit avec le XML du projet" in capsys.readouterr().err


def test_check_sans_avertissement_o5(project, capsys):
    capsys.readouterr()
    main(["check", "-C", str(project)])
    assert "O5" not in capsys.readouterr().err


# --------------------------------------------------------------------------
# applications (scion new/remove, seed add/remove)
# --------------------------------------------------------------------------
def test_scion_new_remove_declare_retire(project, capsys):
    assert main(["scion", "new", "mon-outil", "--type", "application", "-C", str(project), "--no-cmake"]) == 0
    assert '<bin name="mon_outil" stack="2048" priority="100" timeslice="1" />' in _xml(project)
    assert '<bin name="mon_outil"' in (project / "trunk" / PROJECT_XML).read_text()
    capsys.readouterr()
    assert main(["scion", "remove", "mon-outil", "-C", str(project), "--no-cmake"]) == 0
    captured = capsys.readouterr()
    assert "mon_outil" not in _xml(project)
    assert "CFG-5" not in captured.err                             # O4 fermé à la source
    assert '<bin name="mon_outil"> retiré' in captured.out
    assert_trunk_clean(project)


def test_seed_add_remove_application(project, repos):
    assert main(["seed", "add", "my-app", str(repos["app"]), "--type", "application", "-C", str(project),
                 "--no-cmake"]) == 0
    assert '<bin name="my_app"' in _xml(project)
    assert main(["seed", "remove", "my-app", "-C", str(project), "--no-cmake"]) == 0
    assert "my_app" not in _xml(project)


def test_bibliotheque_non_declaree(project, repos):
    before = _xml(project)
    assert main(["seed", "add", "my-lib", str(repos["lib"]), "--type", "bibliotheque", "-C", str(project),
                 "--no-cmake"]) == 0
    assert _xml(project) == before


# --------------------------------------------------------------------------
# graine non migrée, lepton seed mkconf import
# --------------------------------------------------------------------------
def _unmigrate(root: Path) -> None:
    """Graine d'avant O5 : XML du noyau, aucun XML dans le greffon projet."""
    for rel in (PROJECT_XML, "sys/user/demo/etc/.boot", "sys/user/demo/etc/.init"):
        (_stem(root) / rel).unlink()
        (root / "trunk" / rel).unlink()
    data = _graine(root)
    data["mklepton_xml"] = MKCONF
    _graine_path(root).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def test_graine_non_migree_avertit_sans_ecrire(project, capsys):
    _unmigrate(project)
    capsys.readouterr()
    assert main(["scion", "new", "salut", "--type", "application", "-C", str(project), "--no-cmake"]) == 0
    err = capsys.readouterr().err
    assert f"{MKCONF} hors du greffon du projet" in err and "lepton seed mkconf import" in err
    assert (project / "trunk" / MKCONF).read_text() == REF       # XML du noyau jamais modifié
    main(["check", "-C", str(project)])
    assert "XML fourni par un greffon partagé, pas par la graine (CFG-1, O5)" in capsys.readouterr().err


def test_mkconf_import(project, capsys):
    _unmigrate(project)
    data = _graine(project)
    data["applications"] = ["salut"]                               # application déjà citée par la graine
    _graine_path(project).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert main(["seed", "mkconf", "import", MKCONF, "-C", str(project)]) == 0
    assert _graine(project)["mklepton_xml"] == PROJECT_XML
    assert (project / "trunk" / PROJECT_XML).resolve() == (_stem(project) / PROJECT_XML).resolve()
    assert '<bin name="salut"' in _xml(project) and 'src_file="sys/user/demo/etc/.boot"' in _xml(project)
    assert "lepton generate" in capsys.readouterr().out
    assert main(["seed", "mkconf", "import", MKCONF, "-C", str(project)]) == 1   # déjà migrée
    assert "déjà fourni par le greffon du projet" in capsys.readouterr().err
    assert_trunk_clean(project)


def test_mkconf_import_chemin_absolu(project, capsys):
    """F7 (palette) : XML désigné par son chemin absolu du trunk, ramené au trunk ; hors trunk refusé."""
    _unmigrate(project)
    outside = (project / "trunk" / MKCONF).resolve()                  # chemin du clone
    assert main(["seed", "mkconf", "import", str(outside), "-C", str(project)]) == 1
    assert "hors du trunk" in capsys.readouterr().err
    assert main(["seed", "mkconf", "import", str(project / "trunk" / MKCONF), "-C", str(project)]) == 0
    assert _graine(project)["mklepton_xml"] == PROJECT_XML
    assert f"copie de {MKCONF}" in capsys.readouterr().out
    assert_trunk_clean(project)
