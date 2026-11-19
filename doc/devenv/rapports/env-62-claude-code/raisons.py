#!/usr/bin/env python3
"""ENV-62 : décisions de permission d'une session Claude Code, avec leur raison (lecture seule).

Usage : python3 -I raisons.py <journal .jsonl> [--motif <texte>]... [--home <chemin>]

Même lecture que rapports/env-57-mac/decisions.py (laissé tel quel), avec en plus les champs que
celui-ci ne relève pas : reasonCode, grantScope, et la liste des autres clés de
permissionDecision. Une ligne TSV par appel d'outil Bash : heure UTC, décision, source,
reasonType, ruleSource, reasonCode, grantScope, autres clés, commande (une ligne, 200 caractères
au plus). Un refus à l'invite apparaît en « rejet-invite » ; un appel n'est compté qu'une fois.
Avec --motif, seules les commandes qui contiennent l'un des textes sont gardées.
Avec --home, ce chemin est remplacé par <HOME> dans la commande (défaut : le HOME courant).
"""
import json
import os
import sys

CONNUES = {"decision", "source", "reasonType", "ruleSource", "reasonCode", "grantScope"}


def main(argv):
    if not argv:
        print(__doc__, file=sys.stderr)
        return 1
    chemin, motifs, home = argv[0], [], os.path.expanduser("~")
    reste = argv[1:]
    while reste:
        if reste[0] in ("--motif", "--home") and len(reste) > 1:
            if reste[0] == "--motif":
                motifs.append(reste[1])
            else:
                home = reste[1]
            reste = reste[2:]
        else:
            print(f"argument inconnu : {reste[0]}", file=sys.stderr)
            return 1
    outils = {}
    vus = set()
    print("heure_utc\tdecision\tsource\treasonType\truleSource\treasonCode\tgrantScope\tautres\tcommande")
    with open(chemin, encoding="utf-8") as f:
        for ligne in f:
            try:
                o = json.loads(ligne)
            except ValueError:
                continue
            msg = o.get("message") or {}
            contenu = msg.get("content")
            if not isinstance(contenu, list):
                continue
            for it in contenu:
                if not isinstance(it, dict):
                    continue
                if it.get("type") == "tool_use":
                    entree = it.get("input") or {}
                    outils[it.get("id")] = (it.get("name"), entree.get("command", ""))
                elif it.get("type") == "tool_result" and o.get("type") == "user":
                    ident = it.get("tool_use_id")
                    nom, cmd = outils.get(ident, (None, ""))
                    if nom != "Bash" or ident in vus:
                        continue
                    vus.add(ident)
                    if motifs and not any(m in cmd for m in motifs):
                        continue
                    pd = o.get("permissionDecision") or {}
                    res = o.get("toolUseResult")
                    decision = pd.get("decision", "")
                    if not pd and isinstance(res, str) and "User rejected tool use" in res:
                        decision = "rejet-invite"
                    heure = (o.get("timestamp") or "")[11:19]
                    autres = ",".join(sorted(k for k in pd if k not in CONNUES))
                    un = " ".join(cmd.split()).replace(home, "<HOME>")[:200]
                    print("\t".join([heure, decision, pd.get("source", ""), pd.get("reasonType", ""),
                                     pd.get("ruleSource", ""), str(pd.get("reasonCode", "")),
                                     str(pd.get("grantScope", "")), autres, un]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
