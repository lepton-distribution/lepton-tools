"""Jalon 6 d'ENV-8 : check sans argument (GRA-2, GRF-5, CFG-5, contrôles non exprimables) et
seed lock (GRA-5) ; interface §3.5, §3.9, décisions S4-1 et S4-2."""

import json
import subprocess
from pathlib import Path

import pytest

from conftest import MKCONF, assert_trunk_clean
from lepton.cli import main
from lepton.rootstock import KERNEL_KEY, Rootstock

XML = """<?xml version="1.0" encoding="UTF-8"?>
<mklepton version="2">
<kernel>
   <heap size="10000" />
</kernel>
<devices>
   <dev name="dev_null_map" use="on"/>
   <dev name="dev_fam_uart_map" use="on"/>
   <dev name="dev_fam_spi_0_map" use="on"/>
   <dev name="dev_absent_map" use="off"/>
   {extra_dev}
</devices>
<binaries src_path="sbin" dest_path="sbin">
   <bin name="lsh" stack="2048" priority="100" timeslice="1" />
   {extra_bin}
</binaries>
</mklepton>
"""

KERNEL_FILES = {
    MKCONF: XML.format(extra_dev="", extra_bin=""),
    "sys/root/src/kernel/dev/dev_null/dev_null.c": "dev_map_t dev_null_map={\n   \"null\",\n};\n",
    "sys/root/src/sbin/lsh.c": "int lsh_main(int argc, char* argv[])\n{\n   return 0;\n}\n",
    # déclarations seules : ne fournissent ni pilote ni binaire (CFG-5)
    "sys/root/src/kernel/core/decl.c": "extern dev_map_t dev_ghost_map;\nint ls_main(int argc, char* argv[]);\n",
}


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout


def _commit_files(repo: Path, files: dict) -> None:
    for rel, text in files.items():
        target = repo / "scion" / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "jalon 6")


@pytest.fixture
def repos(repos):
    """Dépôts de conftest complétés : XML valide, définitions de pilotes et binaires, fichiers déclarés."""
    _commit_files(repos["kernel"], KERNEL_FILES)
    _commit_files(repos["family"], {
        "sys/root/src/kernel/dev/arch/cortexm/fam-test/uart.c": "dev_map_t dev_fam_uart_map = {\n};\n",
        # définition par collage de lexèmes dans une macro (forme de dev_cmsdk_uart_x)
        "sys/root/src/kernel/dev/arch/cortexm/fam-test/spi.c":
            "#define SPI_DEV(n) \\\n   dev_map_t dev_fam_spi_##n##_map = { \\\n   };\nSPI_DEV(0)\n"})
    for key, name in (("bsp", "board-q"), ("bsp2", "board-c")):
        files = {f"sys/root/src/kernel/dev/bsp/{name}/ld/mem_{name}.ld": "MEMORY {}\n"}
        if key == "bsp2":
            files[f"sys/root/src/kernel/dev/bsp/{name}/openocd/{name}.cfg"] = "source [find board/st.cfg]\n"
        _commit_files(repos[key], files)
    return repos


def _check(project: Path, capsys, *extra: str) -> tuple[int, str]:
    capsys.readouterr()
    code = main(["check", "-C", str(project), *extra])
    return code, capsys.readouterr().out


def _manifest_path(project: Path, name: str) -> Path:
    return next(m.path for m in Rootstock(project).manifests().values() if m.name == name)


def _edit_json(path: Path, **changes) -> None:
    data = json.loads(path.read_text())
    data.update(changes)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2))


def _graine_path(project: Path) -> Path:
    return Rootstock(project).seed_manifest_path()


# --- check sans argument -------------------------------------------------------------------------
def test_check_rootstock_conforme(project, capsys):
    code, out = _check(project, capsys)
    assert code == 0, out
    assert "5 fichier(s) conforme(s)." in out       # 3 manifestes, graine, XML

    code, out = _check(project, capsys, "--json")
    report = json.loads(out)
    assert code == 0 and report["anomalies"] == []
    assert any(f.endswith("lepton-graine.json") for f in report["files"])


def test_check_non_exprimable_json_schema(project, capsys):
    bsp = _manifest_path(project, "board-q")
    _edit_json(bsp, script_liens="ld/absent.ld", options=[
        {"nom": "BAUDS", "type": "entier", "defaut": 300, "min": 1200, "max": 115200,
         "portee": "privee", "description": "Débit."},
        {"nom": "MODE", "type": "enumeration", "defaut": "turbo", "valeurs": ["lent", "rapide"],
         "portee": "privee", "description": "Mode."},
        {"nom": "MODE", "type": "booleen", "defaut": True, "portee": "privee", "description": "Doublon."}])
    graine = _graine_path(project)
    data = json.loads(graine.read_text())
    _edit_json(graine, configurations=data["configurations"] * 2)

    code, out = _check(project, capsys)
    assert code == 1
    assert "/options/0/defaut: défaut 300 hors des bornes [1200, 115200]" in out
    assert "/options/1/defaut: défaut « turbo » absent des valeurs (lent, rapide)" in out
    assert "/options/2/nom: option « MODE » déclarée deux fois" in out
    assert "/script_liens: fichier « ld/absent.ld » introuvable" in out
    assert "/configurations/1/nom: configuration « debug-qemu » déclarée deux fois" in out


BSP_OPTIONS = [
    {"nom": "BAUDS", "type": "entier", "defaut": 9600, "min": 1200, "max": 115200,
     "portee": "privee", "description": "Débit."},
    {"nom": "MODE", "type": "enumeration", "defaut": "lent", "valeurs": ["lent", "rapide"],
     "portee": "publique", "description": "Mode."},
    {"nom": "TRACE", "type": "booleen", "defaut": False, "portee": "privee", "description": "Traces."},
    {"nom": "NOM_CARTE", "type": "chaine", "defaut": "q", "portee": "privee", "description": "Nom."}]


def test_cfg4_check_valeurs_options_graine(project, capsys):
    """CFG-4 (N5) : valeurs fixées par la graine contrôlées contre le manifeste du greffon."""
    _edit_json(_manifest_path(project, "board-q"), options=BSP_OPTIONS)
    graine = _graine_path(project)
    _edit_json(graine, options={"board-q": {"BAUDS": 115200, "MODE": "rapide", "TRACE": True,
                                            "NOM_CARTE": "carte q"}})
    code, out = _check(project, capsys)
    assert code == 0, out

    _edit_json(graine, options={
        "board-q": {"BAUDS": 115201, "MODE": "turbo", "TRACE": 1, "NOM_CARTE": 3, "ABSENTE": 1},
        "lepton-noyau": {"X": True},
        "inconnu": {"X": True}})
    code, out = _check(project, capsys)
    assert code == 1
    assert "/options/board-q/BAUDS: valeur refusée : 115201 hors des bornes [1200, 115200]" in out
    assert "/options/board-q/MODE: valeur refusée : « turbo » absent des valeurs (lent, rapide)" in out
    assert "/options/board-q/TRACE: valeur refusée : booléen attendu" in out
    assert "/options/board-q/NOM_CARTE: valeur refusée : chaîne attendue" in out
    assert "/options/board-q/ABSENTE: option « ABSENTE » non déclarée par board-q (BAUDS, MODE, TRACE, NOM_CARTE)" in out
    assert "/options/lepton-noyau/X: option « X » non déclarée par lepton-noyau (aucune option)" in out
    assert "/options/inconnu: « inconnu » n'est pas un greffon de la graine" in out

    _edit_json(graine, options={"fam-test": {"BAUDS": True}, "board-q": {"BAUDS": True}})
    code, out = _check(project, capsys)           # famille du BSP : greffon de la graine
    assert "/options/fam-test/BAUDS: option « BAUDS » non déclarée par fam-test" in out
    assert "/options/board-q/BAUDS: valeur refusée : entier attendu" in out

    _edit_json(graine, options={"board-q": {"bauds": 9600}})
    code, out = _check(project, capsys)           # forme : schéma de graine
    assert code == 1 and "/options/board-q" in out


def test_gra2_check_noyau_bsp_famille(project, repos, capsys):
    graine = _graine_path(project)
    _edit_json(graine, bsp="board-absent", applications=["app-absente"])
    code, out = _check(project, capsys)
    assert code == 1
    assert "/bsp: BSP « board-absent » non greffé (GRA-2)" in out
    assert "/applications/0: application « app-absente » non greffé (GRA-2)" in out

    # famille du BSP non greffée ; exécution carte sans openocd ni sonde
    _edit_json(graine, bsp="board-q", applications=[],
               configurations=[{"nom": "debug-board", "construction": "Debug", "execution": "carte"}])
    _edit_json(_manifest_path(project, "board-q"), famille="fam-absente")
    code, out = _check(project, capsys)
    assert code == 1
    assert "famille « fam-absente » du BSP board-q non greffée (GRA-2)" in out
    assert "exécution carte : le BSP board-q ne déclare pas openocd, sonde" in out


def test_grf5_check_coeur_backend_dependances(project, capsys):
    _edit_json(_manifest_path(project, "fam-test"), coeurs=["cortex-m7"], dependances=["absent"])
    _edit_json(_manifest_path(project, "lepton-noyau"), backends=["freertos"])
    code, out = _check(project, capsys)
    assert code == 1
    assert "cœur « cortex-m4f » du BSP board-q absent des cœurs de fam-test (cortex-m7) (GRF-5)" in out
    assert "/backend: backend « embos » non fourni par lepton-noyau (freertos) (GRF-5)" in out
    assert "/dependances/0: dépendance « absent » non greffée (GRF-5)" in out


def test_cfg5_check_pilote_binaire_non_fournis(project, capsys):
    xml = (project / "trunk" / MKCONF).resolve()          # fichier du clone noyau, jamais le trunk
    assert "depots" in xml.parts
    xml.write_text(XML.format(extra_dev='<dev name="dev_ghost_map" use="on"/>',
                              extra_bin='<bin name="ls" stack="2048" priority="100" timeslice="1" />'))
    code, out = _check(project, capsys)
    assert code == 1
    assert "devices/dev[@name='dev_ghost_map']: pilote déclaré dans le XML, défini par aucun greffon" in out
    assert "binaries/bin[@name='ls']: binaire déclaré dans le XML, ls_main défini par aucun greffon" in out
    assert "dev_absent_map" not in out                     # use="off" : non contrôlé
    assert "dev_fam_uart_map" not in out and "dev_fam_spi_0_map" not in out and "lsh" not in out


def test_check_fichiers_isoles_inchanges(project, capsys):
    code, out = _check(project, capsys, str(_graine_path(project)))
    assert code == 0 and "1 fichier(s) conforme(s)." in out


# --- GRA-5 : seed lock ---------------------------------------------------------------------------
def _kernel_clone(project: Path) -> Path:
    rs = Rootstock(project)
    return next(rs.clone(e) for e in rs.grafted() if e.key == KERNEL_KEY)


def test_gra5_seed_lock_verify_restore(project, repos, capsys):
    assert main(["seed", "lock", "-C", str(project)]) == 0
    rs = Rootstock(project)
    lock = json.loads((rs.seed_dot() / "lepton-graine.lock.json").read_text())
    kernel = _kernel_clone(project)
    locked_kernel = _git(kernel, "rev-parse", "HEAD").strip()
    assert {e["name"]: e["commit"] for e in lock["scions"]} == {
        "building": None,                                  # répertoire local hors git de scion
        "lepton-noyau": locked_kernel,
        "fam-test": _git(repos["family"], "rev-parse", "HEAD").strip(),
        "board-q": _git(repos["bsp"], "rev-parse", "HEAD").strip()}
    assert main(["seed", "lock", "--verify", "-C", str(project)]) == 0

    # origine distante : nouveau commit dans le clone → écart → restauration au commit figé
    (kernel / "scion/sys/root/src/kernel/core/kernel.c").write_text("/* noyau v2 */\n")
    _git(kernel, "commit", "-qam", "v2")
    capsys.readouterr()
    assert main(["seed", "lock", "--verify", "-C", str(project)]) == 1
    assert "lepton-noyau : commit" in capsys.readouterr().out
    assert main(["seed", "lock", "--restore", "--no-cmake", "-C", str(project)]) == 0
    assert _git(kernel, "rev-parse", "HEAD").strip() == locked_kernel
    assert (project / "trunk/sys/root/src/kernel/core/kernel.c").read_text() == "/* noyau */\n"
    assert main(["seed", "lock", "--verify", "-C", str(project)]) == 0
    assert_trunk_clean(project)

    # origine locale (version *) : signalée, jamais modifiée
    _commit_files(repos["bsp"], {"sys/root/src/kernel/dev/bsp/board-q/board.c": "/* board-q v2 */\n"})
    local_head = _git(repos["bsp"], "rev-parse", "HEAD").strip()
    capsys.readouterr()
    assert main(["seed", "lock", "--restore", "--no-cmake", "-C", str(project)]) == 1
    assert "origine locale" in capsys.readouterr().err
    assert _git(repos["bsp"], "rev-parse", "HEAD").strip() == local_head


def test_gra5_seed_lock_refuse_clone_modifie(project, capsys):
    (_kernel_clone(project) / "scion/sys/root/src/kernel/core/kernel.c").write_text("/* modifié */\n")
    capsys.readouterr()
    assert main(["seed", "lock", "-C", str(project)]) == 1
    assert "graine non figeable" in capsys.readouterr().err
    assert not (Rootstock(project).seed_dot() / "lepton-graine.lock.json").exists()
