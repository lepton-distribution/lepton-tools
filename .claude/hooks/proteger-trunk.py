#!/usr/bin/env python3
"""Hook PreToolUse : refuse toute écriture directe dans le trunk d'un rootstock scion, et dans les
clones tiers projetés (`depots/tiers/`, ENV-41).

Le trunk est une vue de liens symboliques ; écrire dedans remplace un lien par un fichier
régulier non versionné et fait échouer `scion graft`. Les écritures se font dans le clone du
greffon (skill lepton-rootstock). Un clone tiers projeté est un dépôt tiers à une version
épinglée : ses fichiers ne se modifient jamais (P-E1 de la projection, PA-69 d'ENV-41).

Entrée : JSON Claude Code sur stdin (tool_name, tool_input, cwd).
Sortie : code 2 + message sur stderr pour bloquer ; code 0 sinon.
Un trunk est un répertoire nommé `trunk` dont le parent contient `.scion.rootstock.signature` ;
un clone tiers est sous `depots/tiers/` de ce même parent.

Commandes shell (ENV-44, D3, PA-75) : la commande est découpée en commandes simples (`;`, `&&`,
`||`, `|`, `&`, saut de ligne, parenthèses, accents graves) ; `cd` est suivi d'une commande à
l'autre. Pour chaque commande simple, seuls les chemins que son verbe écrit sont jugés
(redirections `>`, destination de `cp`, arguments de `rm`, `find -delete`, `git -C` hors lecture…) ;
`bash -c`, `eval`, `find -exec` et `xargs` sont analysés récursivement. Un chemin est protégé s'il
est sous un trunk ou un clone tiers réel (cwd suivi), ou si son texte a `trunk` ou `depots/tiers`
pour composant. Verbe inconnu : l'ancienne règle (verbe d'écriture puis chemin protégé) s'applique à
la seule commande simple ; texte que shlex ne découpe pas : elle s'applique au texte entier.
Limite : le contenu d'un script exécuté (`bash f.sh`, `python3 -c …`) n'est pas lu.
"""
import json
import os
import re
import shlex
import sys

OUTILS_FICHIER = {"Write", "Edit", "MultiEdit", "NotebookEdit"}

# Ancienne règle (jusqu'à ENV-43), gardée en repli : verbe d'écriture suivi d'un chemin protégé.
ECRITURE_SHELL = re.compile(
    r"(^|[;&|(]\s*|\s)(sed\s+(-[a-zA-Z]*\s+)*-i|perl\s+-[a-zA-Z]*i|rm|mv|cp|touch|mkdir|ln|tee|"
    r"truncate|install|chmod|patch|spatch\s[^;&|]*--in-place)\b[^;&|]*\b(trunk|depots/tiers)/"
)
REDIRECTION = re.compile(r">>?\s*['\"]?[^\s;&|]*\b(trunk|depots/tiers)/")

MESSAGE = (
    "Écriture refusée dans le trunk scion ({}). Le trunk est une vue de liens : écrire dans le "
    "clone du greffon (realpath du fichier, sous depots/ mais jamais sous depots/tiers/), puis "
    "`scion graft` pour un fichier nouveau. Voir la skill lepton-rootstock."
)
MESSAGE_TIERS = (
    "Écriture refusée dans un clone tiers projeté ({}). Ses fichiers viennent d'un dépôt tiers à "
    "une version épinglée : ne jamais les modifier. Changer la version ou les motifs dans le "
    "scion/.scion/ du greffon porteur, ou fournir un fichier local par un autre greffon "
    "(exclusion !motif). Voir la skill lepton-rootstock."
)

SEPARATEURS = {";", ";;", "&", "&&", "|", "||", "|&", "\n", "(", ")", "{", "}"}
MOTS_CLES = {"if", "then", "else", "elif", "fi", "do", "done", "while", "until", "for", "in",
             "case", "esac", "!", "function", "select"}
REDIR_SORTIE = {">", ">>", ">|", "&>", "&>>", ">&", "<>"}
REDIR_ENTREE = {"<", "<<", "<<<", "<<-"}
PREFIXES = {"sudo", "env", "command", "builtin", "nice", "nohup", "exec", "time", "stdbuf",
            "caffeinate", "doas"}
COQUILLES = {"bash", "sh", "zsh", "dash", "ksh"}

LECTURE = {
    "cat", "less", "more", "head", "tail", "grep", "egrep", "fgrep", "rg", "ag", "ls", "stat",
    "diff", "cmp", "wc", "file", "readlink", "realpath", "readelf", "objdump", "nm", "strings",
    "size", "sha256sum", "sha1sum", "shasum", "md5", "md5sum", "cksum", "test", "[", "[[",
    "echo", "printf", "true", "false", "cd", "pushd", "popd", "pwd", "which", "type", "du",
    "tree", "uniq", "cut", "tr", "column", "basename", "dirname", "xxd", "od", "hexdump", "jq",
    "comm", "nl", "tac", "rev", "zcat", "arm-none-eabi-readelf", "arm-none-eabi-objdump",
    "arm-none-eabi-nm", "arm-none-eabi-size", "arm-none-eabi-strings", "otool", "lsof",
}
ECRIT_TOUT = {"rm", "rmdir", "unlink", "touch", "mkdir", "truncate", "chmod", "chown", "chgrp",
              "chflags", "shred", "tee", "setfacl", "xattr", "mkfifo"}
ECRIT_DESTINATION = {"cp", "ln", "install", "rsync", "scp", "ditto", "gcp", "gln"}
GIT_LECTURE = {"status", "log", "show", "diff", "ls-files", "ls-tree", "rev-parse", "describe",
               "cat-file", "grep", "blame", "shortlog", "rev-list", "ls-remote", "archive",
               "name-rev", "merge-base", "for-each-ref", "show-ref", "count-objects", "whatchanged",
               "help", "version", "var", "check-ignore", "check-attr", "diff-tree", "diff-files",
               "diff-index", "cherry"}
GIT_OPTIONS_LECTURE = {  # branch, tag : lecture si chaque argument est une de ces options
    "branch": {"--show-current", "-a", "-r", "-v", "-vv", "--list", "--all", "--remotes"},
    "tag": {"-l", "--list", "-n"},
}
GIT_MOTS_LECTURE = {  # sous-commande lue si son premier argument non option est l'un de ces mots
    "remote": {"get-url", "show"},
    "stash": {"list", "show"},
    "worktree": {"list"},
    "submodule": {"status"},
}


def git_lecture_selon_args(sous: str, reste: list[str]) -> bool:
    """Vrai si `git <sous> <reste>` ne fait que lire (sous-commandes à double usage)."""
    if sous in GIT_OPTIONS_LECTURE:
        return all(a in GIT_OPTIONS_LECTURE[sous] for a in reste)
    if sous in GIT_MOTS_LECTURE:
        mots = non_options(reste)
        return (not mots and sous == "remote") or bool(mots and mots[0] in GIT_MOTS_LECTURE[sous])
    if sous == "config":
        return any(a in ("--get", "--get-all", "--get-regexp", "--list", "-l") for a in reste)
    return False


# --------------------------------------------------------------------------------------------
# Zones protégées
# --------------------------------------------------------------------------------------------
def zone_protegee(chemin: str, cwd: str) -> str | None:
    """« trunk » si chemin (sans suivre les liens) est sous <rootstock>/trunk/, « tiers » s'il est
    sous <rootstock>/depots/tiers/, None sinon."""
    absolu = os.path.normpath(os.path.join(cwd, os.path.expanduser(chemin)))
    parties = absolu.split(os.sep)
    for i, nom in enumerate(parties):
        if i == 0:
            continue
        parent = os.sep.join(parties[:i]) or os.sep
        if nom == "trunk" and os.path.isfile(os.path.join(parent, ".scion.rootstock.signature")):
            return "trunk"
        if (nom == "depots" and parties[i + 1:i + 2] == ["tiers"]
                and os.path.isfile(os.path.join(parent, ".scion.rootstock.signature"))):
            return "tiers"
    return None


def est_dans_trunk(chemin: str, cwd: str) -> bool:
    """Vrai si chemin (sans suivre les liens) est sous <rootstock>/trunk/."""
    return zone_protegee(chemin, cwd) == "trunk"


TEXTE_TIERS = re.compile(r"(^|/)depots/tiers(/|$)")
TEXTE_TRUNK = re.compile(r"(^|/)trunk(/|$)")


def zone_texte(chemin: str) -> str | None:
    """Zone d'après le seul texte (variables non résolues, rootstock absent du disque)."""
    if TEXTE_TIERS.search(chemin):
        return "tiers"
    if TEXTE_TRUNK.search(chemin):
        return "trunk"
    return None


class Repertoire:
    """Répertoire courant simulé : chemin connu (ou None) et zone protégée qu'il désigne."""

    def __init__(self, chemin: str | None, zone: str | None = None):
        self.chemin, self.zone = chemin, zone

    def cd(self, cible: str | None) -> "Repertoire":
        if cible is None or cible == "-":
            return Repertoire(None)
        zone = zone_texte(cible)
        if "$" in cible or "`" in cible:
            return Repertoire(None, zone or (self.zone if not os.path.isabs(cible) else None))
        base = self.chemin
        if base is None and not (os.path.isabs(cible) or cible.startswith("~")):
            return Repertoire(None, zone or self.zone)
        chemin = os.path.normpath(os.path.join(base or "/", os.path.expanduser(cible)))
        return Repertoire(chemin, zone or zone_protegee(chemin, "/"))

    def zone_de(self, chemin: str) -> str | None:
        if not chemin:
            return None
        zone = zone_texte(chemin)
        if zone:
            return zone
        relatif = not (os.path.isabs(chemin) or chemin.startswith(("~", "$")))
        if relatif and self.zone:
            return self.zone
        if "$" in chemin:
            return None
        if self.chemin is not None or not relatif:
            return zone_protegee(chemin, self.chemin or "/")
        return None


# --------------------------------------------------------------------------------------------
# Découpage
# --------------------------------------------------------------------------------------------
def jetons(texte: str) -> list[str] | None:
    """Jetons shell (POSIX) ; le saut de ligne reste un jeton. None si le texte ne se découpe pas."""
    lex = shlex.shlex(texte.replace("`", " ; "), posix=True, punctuation_chars=";&|()<>\n")
    lex.whitespace = " \t\r"
    lex.commenters = ""
    lex.wordchars += "#{}+,:@%^!$[]"
    lex.whitespace_split = False
    try:
        return list(lex)
    except ValueError:
        return None


HEREDOC = re.compile(r"<<-?[ \t]*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")


def retirer_heredocs(texte: str) -> tuple[str, list[str]]:
    """Retire le corps des heredocs (données, pas des commandes) ; rend aussi les corps donnés à un
    shell (`bash <<FIN`), à analyser comme des commandes."""
    lignes = texte.split("\n")
    gardees, shells, k = [], [], 0
    while k < len(lignes):
        ligne = lignes[k]
        gardees.append(ligne)
        k += 1
        for m in HEREDOC.finditer(ligne):
            corps = []
            while k < len(lignes) and lignes[k].strip() != m.group(2):
                corps.append(lignes[k])
                k += 1
            k += 1                                              # ligne du délimiteur
            avant = (jetons(ligne[:m.start()]) or [""])
            mots = sans_prefixes([j for j in avant if j not in SEPARATEURS])
            if mots and os.path.basename(mots[0]) in COQUILLES:
                shells.append("\n".join(corps))
    return "\n".join(gardees), shells


def commandes_simples(liste: list[str]) -> list[list[str]]:
    resultat, courante = [], []
    for j in liste:
        if j in SEPARATEURS or (not courante and j in MOTS_CLES and j not in ("for", "select")):
            if courante:
                resultat.append(courante)
            courante = []
            continue
        courante.append(j)
    if courante:
        resultat.append(courante)
    return resultat


# --------------------------------------------------------------------------------------------
# Analyse d'une commande simple
# --------------------------------------------------------------------------------------------
def non_options(args: list[str]) -> list[str]:
    return [a for a in args if not a.startswith("-") or a == "-"]


def sans_prefixes(mots: list[str]) -> list[str]:
    i = 0
    while i < len(mots):
        m = mots[i]
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", m):          # affectation X=…
            i += 1
        elif os.path.basename(m) in PREFIXES:
            i += 1
            while i < len(mots) and (mots[i].startswith("-") or "=" in mots[i]):
                i += 1
        elif os.path.basename(m) == "timeout":
            i += 1
            while i < len(mots) and mots[i].startswith("-"):
                i += 1
            i += 1                                              # durée
        else:
            break
    return mots[i:]


class Analyse:
    def __init__(self, texte_entier: str, cwd: str | None):
        self.texte = texte_entier
        self.rep = Repertoire(cwd, zone_protegee(cwd, "/") if cwd else None)
        self.vars: dict[str, str | None] = {}
        self.profondeur = 0

    def zone(self, chemin: str) -> str | None:
        """Zone d'un chemin : texte, répertoire courant simulé, puis variables affectées."""
        z = self.rep.zone_de(chemin)
        if z:
            return z
        for nom in re.findall(r"\$\{?([A-Za-z_][A-Za-z0-9_]*)", chemin):
            if self.vars.get(nom):
                return self.vars[nom]
        return None

    def zone_quelconque(self) -> str | None:
        """Zone citée n'importe où dans la commande (contexte de `xargs`)."""
        for j in jetons(self.texte) or self.texte.split():
            z = zone_texte(j) or (self.zone(j) if "/" in j else None)
            if z:
                return z
        return None

    def texte_complet(self, texte: str) -> str | None:
        self.profondeur += 1
        try:
            if self.profondeur > 8:
                return ancienne_regle(texte)
            sans_corps, shells = retirer_heredocs(texte)
            liste = jetons(sans_corps)
            if liste is None:
                return ancienne_regle(texte)
            for cmd in commandes_simples(liste):
                zone = self.commande(cmd)
                if zone:
                    return zone
            for corps in shells:
                zone = self.texte_complet(corps)
                if zone:
                    return zone
            return None
        finally:
            self.profondeur -= 1

    def commande(self, cmd: list[str]) -> str | None:
        if cmd[0] in ("for", "select"):                         # for X in valeurs
            if len(cmd) > 2:
                valeurs = cmd[3:] if cmd[2] == "in" else []
                self.vars[cmd[1]] = next((z for z in map(self.zone, valeurs) if z), None)
            return None
        for j in cmd:                                           # affectations en tête X=…
            m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)=(.*)$", j)
            if not m:
                break
            self.vars[m.group(1)] = self.zone(m.group(2)) if m.group(2) else None
        mots, cibles = [], []
        i = 0
        while i < len(cmd):
            j = cmd[i]
            if j in REDIR_SORTIE:
                suite = cmd[i + 1] if i + 1 < len(cmd) else ""
                if not (j == ">&" and re.fullmatch(r"\d+|-", suite)):
                    cibles.append(suite)
                i += 2
                continue
            if j in REDIR_ENTREE:
                i += 2
                continue
            if j.isdigit() and i + 1 < len(cmd) and cmd[i + 1] in REDIR_SORTIE | REDIR_ENTREE:
                i += 1                                          # descripteur 2>…
                continue
            mots.append(j)
            i += 1
        for c in cibles:
            zone = self.zone(c)
            if zone:
                return zone
        mots = sans_prefixes(mots)
        if not mots:
            return None
        return self.verbe(os.path.basename(mots[0]), mots[1:], mots)

    def verbe(self, v: str, args: list[str], mots: list[str]) -> str | None:
        rep = self.rep
        if v in ("cd", "pushd"):
            na = non_options(args)
            self.rep = rep.cd(na[0] if na else os.path.expanduser("~"))
            return None
        if v in COQUILLES and "-c" in args:
            k = args.index("-c")
            return self.texte_complet(args[k + 1]) if k + 1 < len(args) else None
        if v == "eval":
            return self.texte_complet(" ".join(args))
        if v == "sed":
            if any(re.match(r"^-[a-zA-Z]*i", a) or a.startswith("--in-place") for a in args):
                return self.premiere_zone(non_options(args))
            return None
        if v == "perl" and any(re.match(r"^-[a-zA-Z]*i", a) for a in args):
            return self.premiere_zone(non_options(args))
        if v in ECRIT_TOUT:
            return self.premiere_zone(non_options(args))
        if v == "mv":
            return self.premiere_zone(non_options(args))
        if v in ECRIT_DESTINATION:
            return self.destination(v, args)
        if v == "dd":
            return self.premiere_zone([a[3:] for a in args if a.startswith("of=")])
        if v == "patch":
            return self.patch(args)
        if v == "find":
            return self.find(args)
        if v == "xargs":
            return self.xargs(args)
        if v == "git":
            return self.git(args)
        if v in LECTURE:
            return None
        return ancienne_regle(" ".join(mots))

    def premiere_zone(self, chemins: list[str]) -> str | None:
        for c in chemins:
            zone = self.zone(c)
            if zone:
                return zone
        return None

    def destination(self, v: str, args: list[str]) -> str | None:
        if v == "rsync" and "--remove-source-files" in args:
            return self.premiere_zone(non_options(args))
        if v == "install" and any(re.match(r"^-[a-zA-Z]*d", a) for a in args):
            return self.premiere_zone(non_options(args))
        cible = None
        for k, a in enumerate(args):
            if a in ("-t", "--target-directory") and k + 1 < len(args):
                cible = args[k + 1]
            elif a.startswith("--target-directory="):
                cible = a.split("=", 1)[1]
        if cible is None:
            na = non_options(args)
            if not na:
                return None
            cible = na[-1] if (len(na) > 1 or v not in ("ln", "gln")) else "."
        return self.zone(cible)

    def patch(self, args: list[str]) -> str | None:
        repertoire, fichiers, k = ".", [], 0
        while k < len(args):
            a = args[k]
            if a in ("-d", "--directory", "-o", "--output") and k + 1 < len(args):
                if a in ("-d", "--directory"):
                    repertoire = args[k + 1]
                else:
                    fichiers.append(args[k + 1])
                k += 2
                continue
            if a.startswith(("--directory=", "-d")) and a not in ("-d",):
                repertoire = a.split("=", 1)[1] if "=" in a else a[2:]
            elif a.startswith("-i") or a.startswith("--input"):
                pass
            elif not a.startswith("-"):
                fichiers.append(a)
            k += 1
        return self.premiere_zone([repertoire] + fichiers)

    def find(self, args: list[str]) -> str | None:
        depart = []
        for a in args:
            if a.startswith("-") or a in ("(", "!", ")"):
                break
            depart.append(a)
        depart = depart or ["."]
        for k, a in enumerate(args):
            if a == "-delete":
                zone = self.premiere_zone(depart)
                if zone:
                    return zone
            if a in ("-fprint", "-fprint0", "-fprintf", "-fls") and k + 1 < len(args):
                zone = self.zone(args[k + 1])
                if zone:
                    return zone
            if a in ("-exec", "-execdir", "-ok", "-okdir"):
                sous = []
                for b in args[k + 1:]:
                    if b in (";", "+"):
                        break
                    sous.append(b)
                for d in depart:
                    texte = " ".join(shlex.quote(d) if b == "{}" else shlex.quote(b) for b in sous)
                    zone = self.texte_complet(texte)
                    if zone:
                        return zone
        return None

    def xargs(self, args: list[str]) -> str | None:
        k, remplace = 0, None
        avec_valeur = {"-I", "-n", "-P", "-L", "-d", "-s", "-E", "-a", "--max-args", "--max-procs",
                       "--delimiter", "--arg-file", "-J", "-R", "-S"}
        while k < len(args) and args[k].startswith("-"):
            if args[k] in ("-I", "-J") and k + 1 < len(args):
                remplace = args[k + 1]
            k += 2 if args[k] in avec_valeur else 1
        sous = args[k:] or ["echo"]
        zone_flux = self.zone_quelconque()
        if zone_flux:
            fictif = "trunk/__xargs__" if zone_flux == "trunk" else "depots/tiers/__xargs__"
            sous = [fictif if (remplace and b == remplace) else b for b in sous]
            if not remplace:
                sous = sous + [fictif]
        return self.texte_complet(" ".join(shlex.quote(b) for b in sous))

    def git(self, args: list[str]) -> str | None:
        repertoires, k = [], 0
        while k < len(args) and args[k].startswith("-"):
            a = args[k]
            if a in ("-C", "--git-dir", "--work-tree", "-c", "--namespace") and k + 1 < len(args):
                if a != "-c" and a != "--namespace":
                    repertoires.append(args[k + 1])
                k += 2
                continue
            if a.startswith(("--git-dir=", "--work-tree=")):
                repertoires.append(a.split("=", 1)[1])
            k += 1
        if k >= len(args):
            return None
        sous, reste = args[k], args[k + 1:]
        if sous in GIT_LECTURE:
            return None
        if git_lecture_selon_args(sous, reste):
            return None
        return self.premiere_zone((repertoires or ["."]) + non_options(reste))


def ancienne_regle(texte: str) -> str | None:
    trouve = ECRITURE_SHELL.search(texte) or REDIRECTION.search(texte)
    if not trouve:
        return None
    return "tiers" if trouve.group(trouve.re.groups) == "depots/tiers" else "trunk"


def juger_commande(commande: str, cwd: str | None) -> str | None:
    """Zone protégée qu'une commande shell écrirait (« trunk », « tiers ») ou None."""
    return Analyse(commande, cwd).texte_complet(commande)


def main() -> int:
    try:
        donnees = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0  # entrée illisible : ne pas bloquer le travail, le hook ne juge pas
    outil = donnees.get("tool_name", "")
    entree = donnees.get("tool_input", {}) or {}
    cwd = donnees.get("cwd") or os.getcwd()

    if outil in OUTILS_FICHIER:
        chemin = entree.get("file_path") or entree.get("notebook_path") or ""
        zone = zone_protegee(chemin, cwd) if chemin else None
        if zone:
            print((MESSAGE_TIERS if zone == "tiers" else MESSAGE).format(chemin), file=sys.stderr)
            return 2
    elif outil == "Bash":
        commande = entree.get("command", "")
        zone = juger_commande(commande, cwd)
        if zone:
            message = MESSAGE_TIERS if zone == "tiers" else MESSAGE
            print(message.format(commande.strip()[:200]), file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
