"""Hors étape (décision de l'utilisateur du 2026-11-17) : `scripts/importer-skills.sh`.

Les skills du dépôt se modifient sur le compte claude.ai ; Claude Code en télécharge une copie dans
`~/.claude/skills/synced/<bucket>/<nom>/`, que le script recopie dans `.claude/skills/<nom>/`.
Contrôles tout ou rien avant écriture (code 2), nom invalide ou option inconnue (code 1). Chaque
test travaille dans un `HOME` et un dépôt git temporaires : rien n'est touché hors de `tmp_path`.
"""

import os
import shutil
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "importer-skills.sh"
BUCKET = "b0000000-0000_c0000000-0000"


def ecrire_skill(d: Path, nom: str, corps: str = "corps\n", name: str | None = None) -> None:
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(f"---\nname: {name or nom}\ndescription: essai {nom}\n---\n\n{corps}")


def contenu(d: Path) -> dict[str, bytes]:
    """Fichiers sous `d` (chemins relatifs → octets)."""
    return {str(p.relative_to(d)): p.read_bytes() for p in sorted(d.rglob("*")) if p.is_file()}


@pytest.fixture()
def e(tmp_path: Path) -> SimpleNamespace:
    """Dépôt git avec les skills `a` et `b` commités ; copie synchronisée identique."""
    home = tmp_path / "home"
    bucket = home / ".claude" / "skills" / "synced" / BUCKET
    bucket.mkdir(parents=True)
    (bucket / "manifest.json").write_text("{}")
    depot = tmp_path / "depot"
    (depot / "scripts").mkdir(parents=True)
    shutil.copy2(SCRIPT, depot / "scripts" / SCRIPT.name)
    skills = depot / ".claude" / "skills"
    for s in ("a", "b"):
        ecrire_skill(skills / s, s)
        ecrire_skill(bucket / s, s)
    (depot / ".gitignore").write_text(".DS_Store\n")
    env = dict(os.environ, HOME=str(home), GIT_CONFIG_NOSYSTEM="1")
    env.pop("XDG_CONFIG_HOME", None)
    ns = SimpleNamespace(home=home, bucket=bucket, depot=depot, skills=skills, env=env)
    git(ns, "init", "-q")
    commit(ns, "init")
    return ns


def git(e: SimpleNamespace, *args: str) -> str:
    r = subprocess.run(
        ["git", "-C", str(e.depot), *args], env=e.env, capture_output=True, text=True, check=True
    )
    return r.stdout


def commit(e: SimpleNamespace, message: str) -> None:
    git(e, "add", "-A")
    git(e, "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false",
        "commit", "-qm", message)


def lancer(e: SimpleNamespace, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["bash", str(e.depot / "scripts" / SCRIPT.name), *args],
        env=e.env, cwd=e.depot, capture_output=True, text=True,
    )


def test_identique_rien_ecrit(e: SimpleNamespace) -> None:
    avant = contenu(e.skills)
    r = lancer(e)
    assert r.returncode == 0, r.stderr
    assert "a : identique" in r.stdout and "b : identique" in r.stdout
    assert "copié" not in r.stdout
    assert contenu(e.skills) == avant
    assert git(e, "status", "--porcelain") == ""


def test_modifie_copie_ajouts_et_retraits(e: SimpleNamespace) -> None:
    (e.skills / "a" / "ancien.md").write_text("retiré sur le compte\n")
    commit(e, "ancien")
    ecrire_skill(e.bucket / "a", "a", corps="corps modifié\n")
    (e.bucket / "a" / "references").mkdir()
    (e.bucket / "a" / "references" / "x.md").write_text("annexe\n")
    r = lancer(e)
    assert r.returncode == 0, r.stderr
    assert "a : modifié" in r.stdout and "b : identique" in r.stdout
    assert "copié : a" in r.stdout and "copié : b" not in r.stdout
    assert contenu(e.skills / "a") == contenu(e.bucket / "a")
    assert not (e.skills / "a" / "ancien.md").exists()
    statut = git(e, "status", "--porcelain", "--untracked-files=all")
    assert " M .claude/skills/a/SKILL.md" in statut
    assert " D .claude/skills/a/ancien.md" in statut
    assert "?? .claude/skills/a/references/x.md" in statut
    assert not list(e.skills.glob(".import-*"))


def test_essai_a_blanc_rien_ecrit(e: SimpleNamespace) -> None:
    ecrire_skill(e.bucket / "a", "a", corps="corps modifié\n")
    ecrire_skill(e.bucket / "c", "c")
    avant = contenu(e.skills)
    r = lancer(e, "-n", "a", "c")
    assert r.returncode == 0, r.stderr
    assert "a : modifié" in r.stdout and "+corps modifié" in r.stdout
    assert "c : nouveau" in r.stdout and "  + SKILL.md" in r.stdout
    assert contenu(e.skills) == avant
    assert git(e, "status", "--porcelain", "--untracked-files=all") == ""


@pytest.mark.parametrize("sorte", ["modifié", "non suivi"])
def test_non_commite_tout_ou_rien(e: SimpleNamespace, sorte: str) -> None:
    ecrire_skill(e.bucket / "a", "a", corps="corps modifié\n")
    ecrire_skill(e.bucket / "b", "b", corps="corps modifié\n")
    if sorte == "modifié":
        ecrire_skill(e.skills / "b", "b", corps="modification locale\n")
    else:
        (e.skills / "b" / "local.md").write_text("non suivi\n")
    avant = contenu(e.skills)
    r = lancer(e)
    assert r.returncode == 2
    assert "non commitées" in r.stderr and ".claude/skills/b" in r.stderr
    assert contenu(e.skills) == avant


def test_absent_de_la_copie_synchronisee(e: SimpleNamespace) -> None:
    shutil.rmtree(e.bucket / "b")
    ecrire_skill(e.bucket / "a", "a", corps="corps modifié\n")
    avant = contenu(e.skills)
    r = lancer(e)
    assert r.returncode == 2
    assert "b : absent de la copie synchronisée" in r.stderr and "claude -p" in r.stderr
    assert contenu(e.skills) == avant


def test_name_different_du_dossier(e: SimpleNamespace) -> None:
    ecrire_skill(e.bucket / "a", "a", name="autre")
    r = lancer(e)
    assert r.returncode == 2
    assert "name: « autre »" in r.stderr


@pytest.mark.parametrize("arg", ["../x", "Maj", "a/b", "a.b", ""])
def test_nom_invalide(e: SimpleNamespace, arg: str) -> None:
    r = lancer(e, arg)
    assert r.returncode == 1
    assert "nom invalide" in r.stderr


def test_option_inconnue(e: SimpleNamespace) -> None:
    r = lancer(e, "-x")
    assert r.returncode == 1
    assert "usage" in r.stderr


def test_aucune_copie_synchronisee(e: SimpleNamespace) -> None:
    (e.bucket / "manifest.json").unlink()
    r = lancer(e)
    assert r.returncode == 2
    assert "aucune copie synchronisée" in r.stderr


def test_plusieurs_copies_synchronisees(e: SimpleNamespace) -> None:
    autre = e.bucket.parent / "autre-bucket"
    autre.mkdir()
    (autre / "manifest.json").write_text("{}")
    r = lancer(e)
    assert r.returncode == 2
    assert "plusieurs copies synchronisées" in r.stderr and "autre-bucket" in r.stderr


@pytest.mark.parametrize("ou", ["dedans", "dossier"])
def test_lien_symbolique_refuse(e: SimpleNamespace, ou: str, tmp_path: Path) -> None:
    if ou == "dedans":
        (e.bucket / "a" / "lien").symlink_to(e.bucket / "b" / "SKILL.md")
    else:
        ailleurs = tmp_path / "ailleurs" / "a"
        ecrire_skill(ailleurs, "a", corps="corps modifié\n")
        shutil.rmtree(e.bucket / "a")
        (e.bucket / "a").symlink_to(ailleurs)
    avant = contenu(e.skills)
    r = lancer(e)
    assert r.returncode == 2
    assert "lien symbolique" in r.stderr
    assert contenu(e.skills) == avant


def test_nouveau_skill_nomme_en_argument(e: SimpleNamespace) -> None:
    ecrire_skill(e.bucket / "c", "c")
    r = lancer(e)
    assert r.returncode == 0, r.stderr
    assert not (e.skills / "c").exists()
    r = lancer(e, "c")
    assert r.returncode == 0, r.stderr
    assert "c : nouveau" in r.stdout and "copié : c" in r.stdout
    assert contenu(e.skills / "c") == contenu(e.bucket / "c")
    assert "?? .claude/skills/c/SKILL.md" in git(e, "status", "--porcelain", "--untracked-files=all")


def test_ds_store_ni_compare_ni_copie(e: SimpleNamespace) -> None:
    (e.bucket / "a" / ".DS_Store").write_bytes(b"\0finder")
    r = lancer(e, "a")
    assert r.returncode == 0, r.stderr
    assert "a : identique" in r.stdout
    ecrire_skill(e.bucket / "a", "a", corps="corps modifié\n")
    r = lancer(e, "a")
    assert r.returncode == 0, r.stderr
    assert "a : modifié" in r.stdout
    assert not (e.skills / "a" / ".DS_Store").exists()
    assert (e.skills / "a" / "SKILL.md").read_text().endswith("corps modifié\n")
