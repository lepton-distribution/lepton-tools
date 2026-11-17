"""ENV-58 (D20, PA-103, garde G2) : le hook `.claude/hooks/proteger-trunk.py` demande l'invite
quand une commande soumise à la règle `ask` (`scion graft-update`, `scion seed-update`,
`git push`) est lancée hors de la forme directe : script shell, `bash -c`, `eval`, `find -exec`,
`xargs`, heredoc donné à un shell. Sortie attendue : JSON `permissionDecision: "ask"`, code 0.
La forme directe reste à la règle `ask` de `.claude/settings.json` : le hook n'écrit rien.
Le hook est lancé comme Claude Code le lance : JSON sur l'entrée standard.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

DEPOT = Path(__file__).resolve().parents[1]
HOOK = DEPOT / ".claude" / "hooks" / "proteger-trunk.py"


@pytest.fixture(scope="module")
def s(tmp_path_factory) -> dict[str, str]:
    """Scripts d'essai : avec et sans commande `ask`, appelés directement ou par un autre."""
    rep = tmp_path_factory.mktemp("garde") / "scripts"
    rep.mkdir()
    fichiers = {
        "regreffe.sh": '#!/usr/bin/env bash\nset -u\nscion graft-update -v "$1"\necho "code=$?"\n',
        "sous-shell.sh": '#!/bin/bash\n(cd "$R" && scion graft-update -v) > "$P.log" 2>&1; echo x\n',
        "pousse.sh": "#!/bin/sh\ngit -C /x -c a=b push origin main\n",
        "graine.sh": "scion seed-update -v /x\n",                 # sans shebang : shell
        "appelant.sh": f"#!/bin/bash\nbash {rep}/regreffe.sh /x\n",
        "relatif.sh": "#!/bin/bash\nbash regreffe.sh /x\n",
        "sain.sh": "#!/bin/bash\nscion graft -v /x\ngit status\necho scion graft-update\n",
        "commente.sh": "#!/bin/bash\n# scion graft-update -v /x ; git push\n  # git push\nls\n",
        "outil.py": '#!/usr/bin/env python3\nimport subprocess\nsubprocess.run("scion graft-update /x; git push", shell=True)\n',
    }
    for nom, contenu in fichiers.items():
        p = rep / nom
        p.write_text(contenu)
        p.chmod(0o755)
    return {"S": str(rep)}


def juge(commande: str, cwd: str) -> tuple[int, str]:
    donnees = json.dumps({"tool_name": "Bash", "tool_input": {"command": commande}, "cwd": cwd})
    r = subprocess.run([sys.executable, str(HOOK)], input=donnees, capture_output=True, text=True)
    return r.returncode, r.stdout


def decision(sortie: str) -> str | None:
    if not sortie.strip():
        return None
    return json.loads(sortie)["hookSpecificOutput"]["permissionDecision"]


INVITE = [
    "bash -c 'scion graft-update -v /x'",
    "sh -c \"scion seed-update\"",
    "bash -lc 'git -C /x push'",
    "zsh -c 'cd /x && git push origin main'",
    "bash -c 'echo a; scion graft-update -v /x > /tmp/l 2>&1'",
    "timeout 60 bash -c 'scion graft-update'",
    "eval scion graft-update -v /x",
    "eval 'git push'",
    "bash {S}/regreffe.sh /x",
    "bash -x {S}/regreffe.sh /x",
    "{S}/regreffe.sh /x",
    "source {S}/regreffe.sh",
    ". {S}/graine.sh",
    "{S}/graine.sh",
    "bash {S}/sous-shell.sh",
    "sh {S}/pousse.sh",
    "bash {S}/appelant.sh",
    "cd {S} && bash regreffe.sh /x",
    "cd {S} && ./regreffe.sh /x",
    "cd {S} && bash relatif.sh",
    "bash <<'FIN'\nscion graft-update -v /x\nFIN",
    "echo /x | xargs scion graft-update -v",
    "find /x -maxdepth 0 -exec scion graft-update -v {{}} \\;",
    "bash {S}/regreffe.sh /x > /tmp/journal 2>&1; echo \"code=$?\"",
]

RIEN = [
    "scion graft-update -v /x",                                 # forme directe : règle `ask`
    "scion graft-update -v /x > /tmp/l 2>&1; echo \"code=$?\"",
    "git push origin main",
    "git -C /x push",
    "cd /x && scion seed-update",
    "bash -c 'scion graft -v /x'",
    "bash -c 'git -C /x status'",
    "bash -c 'git log --grep push'",
    "bash -c 'echo scion graft-update'",
    "bash {S}/sain.sh",
    "bash {S}/commente.sh",
    "bash {S}/absent.sh",
    "{S}/outil.py",                                             # autre langage : limite admise
    "python3 -I {S}/outil.py",
    "grep -rn 'scion graft-update' {S}",
    "cat {S}/regreffe.sh",
    "bash relatif.sh",                                          # cwd « / » : script absent
    "ls -la",
]


@pytest.mark.parametrize("gabarit", INVITE)
def test_invite_demandee(s, gabarit):
    commande = gabarit.format(**s)
    code, sortie = juge(commande, "/")
    assert code == 0, commande
    assert decision(sortie) == "ask", commande
    raison = json.loads(sortie)["hookSpecificOutput"]["permissionDecisionReason"]
    assert "ORCHESTRATION §2bis" in raison


@pytest.mark.parametrize("gabarit", RIEN)
def test_rien_demande(s, gabarit):
    commande = gabarit.format(**s)
    code, sortie = juge(commande, "/")
    assert code == 0, commande
    assert decision(sortie) is None, commande


def test_refus_du_trunk_prioritaire(tmp_path):
    racine = tmp_path / "rs"
    (racine / "trunk").mkdir(parents=True)
    (racine / ".scion.rootstock.signature").write_text("")
    code, sortie = juge(f"bash -c 'touch {racine}/trunk/a; scion graft-update -v {racine}'", "/")
    assert code == 2 and not sortie.strip()


def test_scripts_du_depot():
    """Le script de l'essai témoin d'ENV-58 déclenche l'invite ; les outils en deux phases
    d'ENV-57 (commande dans un commentaire seulement) non."""
    assert decision(juge("bash doc/devenv/rapports/env-58-formes/ask-script.sh", str(DEPOT))[1]) == "ask"
    assert decision(juge("bash doc/devenv/rapports/env-53-mac/regreffer-essai.sh /x /y",
                         str(DEPOT))[1]) == "ask"
    assert decision(juge("bash doc/devenv/rapports/env-57-mac/regreffer-essai.sh avant /x /y",
                         str(DEPOT))[1]) is None
    assert decision(juge("scripts/supprimer-essai.sh -n /x", str(DEPOT))[1]) is None


def test_script_trop_gros(tmp_path):
    gros = tmp_path / "gros.sh"
    gros.write_text("scion graft-update /x\n" + "#" * 1_000_001)
    assert decision(juge(f"bash {gros}", "/")[1]) is None


def test_boucle_d_appels(tmp_path):
    a, b = tmp_path / "a.sh", tmp_path / "b.sh"
    a.write_text(f"bash {b}\n")
    b.write_text(f"bash {a}\n")
    code, sortie = juge(f"bash {a}", "/")
    assert code == 0 and decision(sortie) is None
