"""ENV-54 (D16, PA-95) : enveloppe de suppression `scripts/supprimer-essai.sh`.

Le script n'accepte que les descendants d'`~/lepton-tools-dev/essais/` hors des références, les
`<rootstock>/build/<preset>` (`~/lepton` ou un rootstock d'essai) et les répertoires de journaux
de la VM. Tout autre chemin est refusé (code 2), tout ou rien. Chaque test travaille dans un
`HOME` temporaire : rien n'est touché hors de `tmp_path`.
"""

import os
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "supprimer-essai.sh"


@pytest.fixture()
def home(tmp_path: Path) -> Path:
    """HOME factice : rootstock `~/lepton`, essais, références, journaux."""
    h = tmp_path / "home"
    rs = h / "lepton"
    for d in ("trunk/sys", "depots/lepton/original/master", "depots/tiers/lib/v1", "build/debug-qemu"):
        (rs / d).mkdir(parents=True)
    (rs / ".scion.rootstock.signature").write_text("")
    (rs / "trunk" / "sys" / "f").write_text("x")
    e = h / "lepton-tools-dev" / "essais"
    essai = e / "env-99-essai"
    for d in ("trunk", "depots/tiers/lib", "build/release-qemu", "sous/plus"):
        (essai / d).mkdir(parents=True)
    (essai / ".scion.rootstock.signature").write_text("")
    ref = e / "env-11" / "qemu"
    (ref / "build" / "debug-qemu").mkdir(parents=True)
    (ref / "trunk").mkdir()
    (ref / ".scion.rootstock.signature").write_text("")
    (e / "archives").mkdir()
    (e / "lien-lepton").symlink_to(rs)
    (h / "lepton-tools-dev" / "lepton-tools").mkdir()
    for d in ("env-53-journaux", "env-x-journaux", "tmp-pytest", "tmp-tests", "autre/build/p"):
        (h / d).mkdir(parents=True)
    (h / "autre" / ".scion.rootstock.signature").write_text("")
    return h


def lancer(home: Path, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    env = dict(os.environ, HOME=str(home))
    return subprocess.run(
        ["bash", str(SCRIPT), *args], env=env, cwd=cwd or home, capture_output=True, text=True
    )


E = "lepton-tools-dev/essais"

ACCEPTES = [
    f"{E}/env-99-essai",
    f"{E}/env-99-essai/sous",
    f"{E}/env-99-essai/sous/plus/",
    f"{E}/env-99-essai/build/release-qemu",
    f"{E}/env-11/qemu/build/debug-qemu",
    "lepton/build/debug-qemu",
    "env-53-journaux",
    "tmp-pytest",
    "tmp-tests",
]


@pytest.mark.parametrize("rel", ACCEPTES)
def test_cible_acceptee_est_supprimee(home: Path, rel: str) -> None:
    cible = home / rel
    r = lancer(home, f"{home}/{rel}")  # texte brut : pathlib retirerait « / » et « . » finaux
    assert r.returncode == 0, r.stderr
    assert not cible.exists()
    assert "supprimé : " in r.stdout


REFUSES = [
    ("lepton", "hors des bornes"),
    ("lepton/", "hors des bornes"),
    ("lepton/trunk", "hors des bornes"),
    ("lepton/trunk/sys", "hors des bornes"),
    ("lepton/depots", "hors des bornes"),
    ("lepton/depots/tiers/lib/v1", "hors des bornes"),
    ("lepton/build", "hors des bornes"),
    ("lepton-tools-dev", "hors des bornes"),
    ("lepton-tools-dev/lepton-tools", "hors des bornes"),
    (E, "hors des bornes"),
    (f"{E}/", "hors des bornes"),
    (f"{E}/.", "non résoluble"),
    (f"{E}/env-99-essai/..", "non résoluble"),
    (f"{E}/env-99-essai/../..", "non résoluble"),
    (f"{E}/env-99-essai/../../lepton-tools", "hors des bornes"),
    (f"{E}/env-99-essai/trunk", "trunk"),
    (f"{E}/env-99-essai/depots/tiers", "depots/tiers"),
    (f"{E}/env-99-essai/depots/tiers/lib", "depots/tiers"),
    (f"{E}/env-11", "référence"),
    (f"{E}/env-11/qemu", "référence"),
    (f"{E}/env-11/qemu/trunk", "trunk"),
    (f"{E}/archives", "référence"),
    (f"{E}/lien-lepton/trunk", "hors des bornes"),
    (f"{E}/lien-lepton/build", "hors des bornes"),
    (f"{E}/absent", "cible absente"),
    ("absent", "hors des bornes"),
    ("env-x-journaux", "hors des bornes"),
    ("env-53-journaux/sous", "hors des bornes"),
    ("autre/build/p", "hors des bornes"),
]


@pytest.mark.parametrize("rel,raison", REFUSES)
def test_cible_refusee_rien_supprime(home: Path, rel: str, raison: str) -> None:
    cible = home / rel
    existait = cible.exists()
    r = lancer(home, f"{home}/{rel}")
    assert r.returncode == 2, r.stdout
    assert raison in r.stderr
    assert "rien n'a été supprimé" in r.stderr
    assert cible.exists() == existait
    assert (home / "lepton" / "trunk" / "sys" / "f").exists()


@pytest.mark.parametrize("brute", ["", "/", "."])
def test_cibles_degenerees_refusees(home: Path, brute: str) -> None:
    r = lancer(home, brute, cwd=home / E)
    assert r.returncode == 2
    assert (home / E).is_dir()


def test_home_lui_meme_refuse(home: Path) -> None:
    r = lancer(home, str(home))
    assert r.returncode == 2
    assert home.is_dir()


def test_tout_ou_rien(home: Path) -> None:
    bon = home / E / "env-99-essai" / "sous"
    r = lancer(home, str(bon), str(home / "lepton"))
    assert r.returncode == 2
    assert bon.is_dir()
    assert (home / "lepton").is_dir()


def test_plusieurs_cibles_acceptees(home: Path) -> None:
    a = home / E / "env-99-essai"
    b = home / "env-53-journaux"
    r = lancer(home, str(a), str(b))
    assert r.returncode == 0, r.stderr
    assert not a.exists() and not b.exists()


def test_chemin_relatif(home: Path) -> None:
    r = lancer(home, "env-99-essai/sous", cwd=home / E)
    assert r.returncode == 0, r.stderr
    assert not (home / E / "env-99-essai" / "sous").exists()


def test_tilde_developpe_par_le_shell(home: Path) -> None:
    """Forme écrite par la session : `~/…`, développée par le shell appelant."""
    env = dict(os.environ, HOME=str(home))
    r = subprocess.run(
        ["bash", "-c", f'bash "{SCRIPT}" ~/{E}/env-99-essai'],
        env=env, cwd=home, capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr
    assert not (home / E / "env-99-essai").exists()


def test_lien_final_supprime_sans_suivre(home: Path) -> None:
    lien = home / E / "lien-lepton"
    r = lancer(home, str(lien))
    assert r.returncode == 0, r.stderr
    assert not lien.is_symlink()
    assert (home / "lepton" / "trunk" / "sys" / "f").exists()


def test_a_blanc(home: Path) -> None:
    cible = home / E / "env-99-essai"
    r = lancer(home, "-n", str(cible))
    assert r.returncode == 0, r.stderr
    assert "accepté (à blanc)" in r.stdout
    assert cible.is_dir()


def test_a_blanc_refus(home: Path) -> None:
    r = lancer(home, "-n", str(home / "lepton"))
    assert r.returncode == 2


def test_sans_argument(home: Path) -> None:
    assert lancer(home).returncode == 1
    assert lancer(home, "-n").returncode == 1


def test_build_sans_signature_refuse(home: Path) -> None:
    (home / "lepton" / ".scion.rootstock.signature").unlink()
    cible = home / "lepton" / "build" / "debug-qemu"
    r = lancer(home, str(cible))
    assert r.returncode == 2
    assert cible.is_dir()


def test_executable() -> None:
    assert os.access(SCRIPT, os.X_OK)
