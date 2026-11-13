#!/usr/bin/env python3
"""ENV-57 : décisions de permission d'une session Claude Code (lecture seule).

Usage : python3 -I decisions.py <journal .jsonl> [--motif <texte>]...

Lit le journal de session (~/.claude/projects/<projet>/<session>.jsonl) et écrit sur stdout une
ligne TSV par appel d'outil Bash : heure UTC, décision, source, reasonType, ruleSource, commande
(une ligne, 200 caractères au plus). Un refus à l'invite apparaît en « rejet-invite » (pas de
permissionDecision, toolUseResult « User rejected tool use ») ; un refus du hook porte la source
« hook ». Un appel n'est compté qu'une fois (identifiant de l'outil).
Avec --motif, seules les commandes qui contiennent l'un des textes sont gardées.
Forme des champs : rapports/env-54-permissions.md §9, §10.
"""
import json
import sys


def main(argv):
    if not argv:
        print(__doc__, file=sys.stderr)
        return 1
    chemin, motifs = argv[0], []
    reste = argv[1:]
    while reste:
        if reste[0] == "--motif" and len(reste) > 1:
            motifs.append(reste[1])
            reste = reste[2:]
        else:
            print(f"argument inconnu : {reste[0]}", file=sys.stderr)
            return 1
    outils = {}
    vus = set()
    print("heure_utc\tdecision\tsource\treasonType\truleSource\tcommande")
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
                    # les copies de requête (« api-request-blob ») reprennent le résultat sans la
                    # décision : seule l'entrée « user » la porte
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
                    un = " ".join(cmd.split())[:200]
                    print("\t".join([heure, decision, pd.get("source", ""),
                                     pd.get("reasonType", ""), pd.get("ruleSource", ""), un]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
