"""Fixtures : dépôts git locaux de greffons factices et rootstocks temporaires (scion réel, sans réseau)."""

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from lepton.cli import main

MKCONF = "sys/user/demo/etc/mkconf_demo.xml"

KERNEL = {"nom": "lepton-noyau", "type": "noyau", "version": "1.0.0", "destination": "",
          "coeurs": ["cortex-m4f", "cortex-m7"], "backends": ["embos", "freertos"]}
FAMILY = {"nom": "fam-test", "type": "famille", "version": "1.0.0",
          "destination": "kernel/dev/arch/cortexm/fam-test", "bibliotheque": "kernel",
          "coeurs": ["cortex-m4f"], "mcu": ["ARMCM4"]}


def bsp_manifest(name: str, family: str = "fam-test", core: str = "cortex-m4f", qemu: bool = True) -> dict:
    data = {"nom": name, "type": "bsp", "version": "1.0.0", "destination": f"kernel/dev/bsp/{name}",
            "bibliotheque": "bsp", "famille": family, "coeur": core, "mcu": "ARMCM4",
            "frequence_cpu": 25000000, "script_liens": f"ld/mem_{name}.ld", "demarrage": ["board.c"]}
    if qemu:
        data["qemu"] = {"machine": "mps2-an386"}
    else:
        data.update(openocd=[f"openocd/{name}.cfg"], sonde="stlink")
    return data


def app_manifest(name: str, kind: str = "application") -> dict:
    lib = "bin" if kind == "application" else "lib"
    return {"nom": name, "type": kind, "version": "0.1.0", "destination": f"{lib}/{name}",
            "bibliotheque": lib, "sources": [""], "dependances": ["lepton-noyau"]}


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout


def make_scion_repo(path: Path, manifest: dict, files: dict | None = None) -> Path:
    """Dépôt git d'un greffon : scion/sys/root/src/<destination>/lepton-greffon.json et fichiers."""
    dest = path / "scion" / "sys" / "root" / "src" / manifest["destination"]
    dest.mkdir(parents=True)
    (dest / "lepton-greffon.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    for rel, text in (files or {}).items():
        target = path / "scion" / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
    subprocess.run(["git", "init", "-q", "-b", "master", str(path)], check=True)
    _git(path, "add", "-A")
    _git(path, "commit", "-q", "-m", "initial")
    return path


@pytest.fixture(autouse=True)
def git_identity(monkeypatch):
    for var in ("AUTHOR", "COMMITTER"):
        monkeypatch.setenv(f"GIT_{var}_NAME", "lepton-tests")
        monkeypatch.setenv(f"GIT_{var}_EMAIL", "lepton-tests@example.invalid")


@pytest.fixture
def repos(tmp_path):
    """Dépôts git locaux : noyau, famille, deux BSP (QEMU, carte), application, bibliothèque."""
    if shutil.which("scion") is None:
        pytest.skip("scion absent")
    base = tmp_path / "repos"
    r = {
        "kernel": make_scion_repo(base / "kernel", KERNEL, {
            MKCONF: '<mklepton version="2"/>\n', "sys/root/src/kernel/core/kernel.c": "/* noyau */\n"}),
        "family": make_scion_repo(base / "fam-test", FAMILY, {
            "sys/root/src/kernel/dev/arch/cortexm/fam-test/uart.c": "/* uart */\n"}),
        "bsp": make_scion_repo(base / "board-q", bsp_manifest("board-q"), {
            "sys/root/src/kernel/dev/bsp/board-q/board.c": "/* board-q */\n"}),
        "bsp2": make_scion_repo(base / "board-c", bsp_manifest("board-c", qemu=False), {
            "sys/root/src/kernel/dev/bsp/board-c/board.c": "/* board-c */\n"}),
        "app": make_scion_repo(base / "my-app", app_manifest("my-app"), {
            "sys/root/src/bin/my-app/my-app.c": "int my_app_main(void){return 0;}\n"}),
        "lib": make_scion_repo(base / "my-lib", app_manifest("my-lib", "bibliotheque"), {
            "sys/root/src/lib/my-lib/my-lib.c": "int my_lib(void){return 0;}\n"}),
    }
    return r


def url(path: Path) -> str:
    """Forme git d'un dépôt local, clonée par scion (GRA-3)."""
    return f"file://localhost{path}"


@pytest.fixture
def project(tmp_path, repos):
    """Rootstock créé par lepton seed new (noyau en URL git, famille et BSP en répertoires locaux)."""
    root = tmp_path / "project"
    code = main(["seed", "new", "demo", "-C", str(root), "--bsp", "board-q", "--mkconf", MKCONF,
                 "--origin", f"lepton-noyau={url(repos['kernel'])}@master",
                 "--origin", f"fam-test={repos['family']}",
                 "--origin", f"board-q={repos['bsp']}"])
    assert code == 0
    return root


def assert_trunk_clean(root: Path) -> None:
    """Critère ENV-8 / FIC-3 : aucun fichier régulier (hors liste greffée), aucun lien cassé."""
    trunk = root / "trunk"
    for p in trunk.rglob("*"):
        if p.is_symlink():
            assert p.exists(), f"lien cassé : {p}"
        elif p.is_file():
            assert p.name == ".scion.grafted.list", f"fichier régulier dans le trunk : {p}"
