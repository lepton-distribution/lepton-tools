#!/usr/bin/env bash
# ENV-51 : relevé d'une commande (stdout, stderr, code de retour), sans rien filtrer.
# Usage : releve.sh <répertoire de sortie> <nom> <répertoire d'exécution> <commande…>
# Écrit <nom>.cmd, <nom>.out, <nom>.err, <nom>.code dans le répertoire de sortie.
set -u
out=$1 nom=$2 dir=$3
shift 3
mkdir -p "$out"
printf '%s\n' "$*" >"$out/$nom.cmd"
( cd "$dir" && "$@" ) >"$out/$nom.out" 2>"$out/$nom.err"
code=$?
echo "$code" >"$out/$nom.code"
printf '== %s (code %s)\n-- stdout\n' "$nom" "$code"; cat "$out/$nom.out"
printf -- '-- stderr\n'; cat "$out/$nom.err"
