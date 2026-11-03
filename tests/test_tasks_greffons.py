"""ENV-30 : tâche de l'éditeur « tests des greffons » (TST-1 pour les tests de TST-2).

PA-47 : configurations QEMU seules ; tâche présente seulement si un greffon actif de la
configuration déclare `tests` (règle `_lepton_greffon_actif` du lecteur CMake : BSP de la
configuration, sa famille, applications et bibliothèques ; noyau exclu) ; libellé
`lepton : tests des greffons <P>`, `ctest --preset <P> -L greffon: --output-on-failure`, `group`
`test`, `cwd` trunk, `PYTHONDONTWRITEBYTECODE=1`, après `lepton : construire <P>`.
"""

import json
from pathlib import Path

from conftest import assert_trunk_clean
from lepton.cli import main
from lepton.rootstock import Rootstock
from test_generate import _set_graine, _workspace, repos, tools  # noqa: F401  (fixtures : presets du noyau, outils factices)
from test_reference_seed import _workspace as _reference_workspace
from test_reference_seed import reference  # noqa: F401  (fixture : graine de référence)

LABEL = "lepton : tests des greffons"


def _set_tests(root: Path, name: str) -> None:
    """Champ `tests` ajouté au manifeste greffé `name` (dans son clone)."""
    m = next(m for m in Rootstock(root).manifests().values() if m.name == name)
    m.path.write_text(json.dumps({**m.data, "tests": "tests"}, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")


def _tasks(ws: dict) -> dict:
    return {t["label"]: t for t in ws["tasks"]["tasks"]}


def _greffon_tasks(ws: dict) -> list[str]:
    return [label for label in _tasks(ws) if label.startswith(LABEL)]


def test_no_greffon_tests_no_task(project, tools):  # noqa: F811
    """Option 1 : aucun greffon actif ne déclare `tests` → aucune tâche ; fumée et KAL inchangées."""
    assert main(["generate", "-C", str(project)]) == 0
    ws = _workspace(project)
    assert _greffon_tasks(ws) == []
    assert "lepton : banc KAL demo-debug-qemu" in _tasks(ws)


def test_bsp_tests_task(project, tools):  # noqa: F811
    """BSP de la configuration avec `tests` → une tâche par configuration QEMU, forme du PA-47."""
    _set_tests(project, "board-q")
    _set_graine(project, configurations=[
        {"nom": "debug-qemu", "construction": "Debug", "execution": "qemu"},
        {"nom": "release-qemu", "construction": "Release", "execution": "qemu"}])
    assert main(["generate", "-C", str(project)]) == 0
    ws = _workspace(project)
    assert _greffon_tasks(ws) == [f"{LABEL} demo-debug-qemu", f"{LABEL} demo-release-qemu"]
    task = _tasks(ws)[f"{LABEL} demo-debug-qemu"]
    kal = _tasks(ws)["lepton : banc KAL demo-debug-qemu"]
    assert task["args"] == ["--preset", "demo-debug-qemu", "-L", "greffon:", "--output-on-failure"]
    assert task["command"] == kal["command"]                              # même ctest
    assert task["group"] == "test" and task["dependsOn"] == ["lepton : construire demo-debug-qemu"]
    assert task["options"] == {"cwd": str(project / "trunk"), "env": {"PYTHONDONTWRITEBYTECODE": "1"}}
    labels = list(_tasks(ws))                                             # après le banc KAL
    assert labels.index(f"{LABEL} demo-debug-qemu") == labels.index("lepton : banc KAL demo-debug-qemu") + 1
    assert_trunk_clean(project)


def test_family_tests_task(project, tools):  # noqa: F811
    """Famille du BSP de la configuration avec `tests` → tâche."""
    _set_tests(project, "fam-test")
    assert main(["generate", "-C", str(project)]) == 0
    assert _greffon_tasks(_workspace(project)) == [f"{LABEL} demo-debug-qemu"]


def test_application_tests_task(project, repos, tools):  # noqa: F811
    """Application greffée avec `tests` → tâche (application toujours active)."""
    assert main(["seed", "add", "my-app", str(repos["app"]), "--type", "application", "-C", str(project),
                 "--no-cmake"]) == 0
    _set_tests(project, "my-app")
    assert main(["generate", "-C", str(project)]) == 0
    assert _greffon_tasks(_workspace(project)) == [f"{LABEL} demo-debug-qemu"]


def test_board_configuration_no_task(project, repos, tools):  # noqa: F811
    """PA-47 Q1 : configuration carte, BSP avec `tests` → aucune tâche (port série non fourni)."""
    assert main(["seed", "add", "board-c", str(repos["bsp2"]), "--type", "bsp", "-C", str(project),
                 "--no-cmake"]) == 0
    _set_tests(project, "board-c")
    _set_graine(project, bsp="board-c",
                configurations=[{"nom": "debug-board", "construction": "Debug", "execution": "carte"}])
    assert main(["generate", "-C", str(project)]) == 0
    ws = _workspace(project)
    assert "lepton : flasher demo-debug-board" in _tasks(ws)
    assert _greffon_tasks(ws) == []


def test_reference_seed_active_bsp_only(reference, tools):  # noqa: F811
    """Graine de référence : tâche pour les presets QEMU du BSP qui déclare `tests` ; un BSP inactif
    avec `tests` (carte board-c) n'en donne à aucun preset."""
    _set_tests(reference, "board-c")
    assert main(["generate", "-C", str(reference)]) == 0
    assert _greffon_tasks(_reference_workspace(reference)) == []
    _set_tests(reference, "board-q")
    assert main(["generate", "-C", str(reference)]) == 0
    ws = _reference_workspace(reference)
    assert _greffon_tasks(ws) == [f"{LABEL} board-q-freertos", f"{LABEL} board-q-embos"]
    assert _tasks(ws)[f"{LABEL} board-q-embos"]["args"][:2] == ["--preset", "board-q-embos"]
    assert_trunk_clean(reference)
