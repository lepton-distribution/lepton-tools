#!/usr/bin/env bash
# ENV-55 : lecture par git de chaque forme d'URL d'un dépôt local (git ls-remote, lecture seule).
# Usage : git-formes.sh <dépôt présent (chemin absolu)>
# ssh neutralisé (core.sshCommand=false) : une forme lue comme « hôte:chemin » échoue sans réseau.
set -u
p=$1
printf 'git %s\n' "$(git --version)"
for u in "file://$p" "file://localhost$p" "file:$p" "file://autre$p" "FILE://$p" "FILE://localhost$p" \
         "file://127.0.0.1$p" "file://LOCALHOST$p" "$p"; do
  out=$(git -c core.sshCommand=false ls-remote --heads "$u" 2>&1)
  code=$?
  printf '%s\t%s\t%s\n' "$u" "$code" "$(printf '%s' "$out" | tr '\n' ' ' | cut -c1-200)"
done
