#!/usr/bin/env bash
# ENV-70 : échecs construits des commandes git que scion lance (gitops.py, mirror.py), pour
# relever l'ordre des lignes du stderr (avertissement ou astuce avant la cause).
# Usage : construits.sh <base vide> <git> <sortie>
# Dépôts temporaires sous <base> ; chaque cas écrit « $ commande », « code N », puis le stderr.
# Chemins de <base> et du HOME normalisés (<B>, <HOME>), empreintes en <sha>.
set -u
export LC_ALL=C GIT_TERMINAL_PROMPT=0
B=$1 G=$2 OUT=$3
mkdir -p "$B" && B=$(cd "$B" && pwd)
OUT=$(cd "$(dirname "$OUT")" && pwd)/$(basename "$OUT")
: >"$OUT"
q() { "$G" "$@" >/dev/null 2>&1; }
cas() {  # <titre> <répertoire> <arguments git…>
  local t=$1 d=$2; shift 2
  { echo "## $t"; echo "\$ git $*"; (cd "$d" && "$G" "$@" 2>&1 >/dev/null); echo "code $?"; echo; } \
    | sed -e "s#$B#<B>#g" -e "s#$HOME#<HOME>#g" -E -e 's/[0-9a-f]{40}/<sha>/g' >>"$OUT"
}
cd "$B"
q init -q amont && q -C amont symbolic-ref HEAD refs/heads/master && q -C amont -c user.name=x -c user.email=x@x.invalid commit -q --allow-empty -m a
q clone -q "file://localhost$B/amont" travail
q -C travail -c user.name=x -c user.email=x@x.invalid commit -q --allow-empty -m local
q -C amont -c user.name=x -c user.email=x@x.invalid commit -q --allow-empty -m distant
q -C travail fetch -q
q init -q --bare nu.git && q -C nu.git symbolic-ref HEAD refs/heads/master
q -C travail push -q "file://localhost$B/nu.git" HEAD:refs/heads/master
q -C amont push -q -f "file://localhost$B/nu.git" HEAD:refs/heads/autre

cas "merge --ff-only, branche divergée (fast_forward)" travail merge --ff-only --quiet '@{u}'
cas "rev-list sans amont (ahead_behind)" amont rev-list --left-right --count 'HEAD...@{u}'
cas "push non rapide (mirror._push)" amont push --porcelain "file://localhost$B/nu.git" HEAD:refs/heads/master
cas "checkout d'un commit absent (checkout_detached)" travail checkout --quiet --detach 0123456789012345678901234567890123456789
cas "clone -b absent --single-branch (clone)" . clone -b nope --quiet --single-branch "file://localhost$B/amont" c1
cas "clone -b absent (clone)" . clone -b nope --quiet "file://localhost$B/amont" c2
cas "clone partiel d'un dépôt absent (clone_partial)" . clone --quiet --filter=blob:none --no-checkout "file://localhost$B/absent" c3
cas "clone --mirror d'un dépôt absent (mirror)" . clone --quiet --mirror "file://localhost$B/absent" c4
cas "fetch d'une origine absente (fetch)" travail fetch --quiet "file://localhost$B/absent"
cas "ls-remote d'une origine absente (remote_tag_commit)" travail ls-remote --tags "file://localhost$B/absent" refs/tags/v1
cas "sparse-checkout set hors d'un dépôt (sparse_set)" . sparse-checkout set --cone x
