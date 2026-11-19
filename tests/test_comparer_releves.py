"""ENV-62 (D27, PA-111) : `scripts/comparer-releves.py`.

Normalisation des relevés avant comparaison : messages de git traduits (`po/fr.po`, espace
insécable après « fatal »), ancêtres de `<HOME>` sous `depots/.mirrors/<hôte>/`. Chaque test
travaille sous `tmp_path`.
"""

import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "comparer-releves.py"
NBSP = " "


def lancer(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-I", str(SCRIPT), *args],
                          capture_output=True, text=True)


def ecrire(d: Path, fichiers: dict[str, str]) -> Path:
    d.mkdir(parents=True, exist_ok=True)
    for nom, texte in fichiers.items():
        (d / nom).write_text(texte, encoding="utf-8")
    return d


def test_branche_distante_et_espace_insecable(tmp_path):
    mac = ecrire(tmp_path / "a", {"f05.err": "erreur : (code 128) : fatal: Remote branch nope not found in upstream origin\n"})
    vm = ecrire(tmp_path / "o", {"f05.err": f"erreur : (code 128) : fatal{NBSP}: La branche distante nope n'a pas été trouvée dans le dépôt amont origin\n"})
    p = lancer(str(mac), str(vm))
    assert p.returncode == 0, p.stdout
    assert "f05.err\tidentique" in p.stdout and "écarts=0 / 1" in p.stdout


def test_espace_ordinaire_non_ramenee(tmp_path):
    """Le motif suit `po/fr.po` octet pour octet : une espace ordinaire n'est pas un texte de git."""
    mac = ecrire(tmp_path / "a", {"f.err": "fatal: Remote branch x not found in upstream origin\n"})
    vm = ecrire(tmp_path / "o", {"f.err": "fatal : La branche distante x n'a pas été trouvée dans le dépôt amont origin\n"})
    p = lancer(str(mac), str(vm))
    assert p.returncode == 1
    assert "f.err\técart" in p.stdout and "écarts=1 / 1" in p.stdout


def test_depot_existe_et_prefixe_seul(tmp_path):
    mac = ecrire(tmp_path / "a", {"f.err": "échec (code 128) : and the repository exists.\nfatal: autre\n"})
    vm = ecrire(tmp_path / "o", {"f.err": f"échec (code 128) : et que le dépôt existe.\nfatal{NBSP}: autre\n"})
    assert lancer(str(mac), str(vm)).returncode == 0


def test_acces_impossible_n04(tmp_path):
    """ENV-66 : `unable to access '%s': %s` (fr.po l. 20309-20310, U+00A0 avant « : »)."""
    mac = ecrire(tmp_path / "a", {"n04.err": "erreur : (code 128) : fatal: unable to access 'https://h.invalid/p.git/': Could not resolve host: h.invalid\n"})
    vm = ecrire(tmp_path / "o", {"n04.err": f"erreur : (code 128) : fatal{NBSP}: impossible d'accéder à 'https://h.invalid/p.git/'{NBSP}: Could not resolve host: h.invalid\n"})
    p = lancer(str(mac), str(vm))
    assert p.returncode == 0, p.stdout
    ordinaire = ecrire(tmp_path / "o2", {"n04.err": f"erreur : (code 128) : fatal{NBSP}: impossible d'accéder à 'https://h.invalid/p.git/' : Could not resolve host: h.invalid\n"})
    assert lancer(str(mac), str(ordinaire)).returncode == 1


def test_stderr_complet_de_git(tmp_path):
    """ENV-66 : `*.git-err` de la fixture d'ENV-65 (stderr complet) : « Cloning into » (l. 4492-4493)
    et le bloc « Could not read from remote repository. » (l. 15855-15864)."""
    anglais = ("Cloning into 'd'...\n"
               "fatal: '<B>/repos/absent' does not appear to be a git repository\n"
               "fatal: Could not read from remote repository.\n\n"
               "Please make sure you have the correct access rights\n"
               "and the repository exists.\n")
    francais = ("Clonage dans 'd'...\n"
                f"fatal{NBSP}: '<B>/repos/absent' does not appear to be a git repository\n"
                f"fatal{NBSP}: Impossible de lire le dépôt distant.\n\n"
                "Veuillez vérifier que vous avez les droits d'accès\n"
                "et que le dépôt existe.\n")
    mac = ecrire(tmp_path / "a", {"n01.git-err": anglais})
    vm = ecrire(tmp_path / "o", {"n01.git-err": francais})
    p = lancer(str(mac), str(vm))
    assert p.returncode == 0, p.stdout


def test_segment_hote_des_miroirs(tmp_path):
    mac = ecrire(tmp_path / "a", {"f12a.depots": "depots/.mirrors\ndepots/.mirrors/localhost\ndepots/.mirrors/localhost/Users\ndepots/.mirrors/localhost<HOME>\n"})
    vm = ecrire(tmp_path / "o", {"f12a.depots": "depots/.mirrors\ndepots/.mirrors/localhost\ndepots/.mirrors/localhost/home\ndepots/.mirrors/localhost<HOME>\n"})
    p = lancer("--home-attendu", "/Users/u", "--home-obtenu", "/home/v", str(mac), str(vm))
    assert p.returncode == 0, p.stdout
    sans = lancer(str(mac), str(vm))
    assert sans.returncode == 1 and "-depots/.mirrors/localhost/Users" in sans.stdout


def test_ancetres_multiples_et_hors_miroir(tmp_path):
    """Ancêtres plus lointains : `<HOME/../..>` ; un `/home` hors `depots/.mirrors/` n'est pas touché."""
    mac = ecrire(tmp_path / "a", {"d": "depots/.mirrors/localhost/Users\nchemin /Users\n"})
    vm = ecrire(tmp_path / "o", {"d": "depots/.mirrors/localhost/srv\ndepots/.mirrors/localhost/srv/home\nchemin /srv\n"})
    p = lancer("--home-attendu", "/Users/u", "--home-obtenu", "/srv/home/v", str(mac), str(vm))
    assert p.returncode == 1
    assert "+depots/.mirrors/localhost<HOME/../..>\n" in p.stdout
    assert " depots/.mirrors/localhost<HOME/..>\n" in p.stdout
    assert "-chemin /Users" in p.stdout and "+chemin /srv" in p.stdout


def test_fichier_absent_et_selection(tmp_path):
    mac = ecrire(tmp_path / "a", {"x": "1\n", "y": "2\n"})
    vm = ecrire(tmp_path / "o", {"x": "1\n"})
    p = lancer(str(mac), str(vm))
    assert p.returncode == 1 and "y\tabsent" in p.stdout and "écarts=1 / 2" in p.stdout
    assert lancer(str(mac), str(vm), "x").returncode == 0


@pytest.mark.parametrize("args", [[], ["seul"], ["/nexiste/pas", "/nexiste/pas2"]])
def test_usage(tmp_path, args):
    assert lancer(*args).returncode == 2


def test_fichier_nomme_absent_de_l_attendu(tmp_path):
    mac = ecrire(tmp_path / "a", {"x": "1\n"})
    vm = ecrire(tmp_path / "o", {"x": "1\n"})
    assert lancer(str(mac), str(vm), "z").returncode == 2
