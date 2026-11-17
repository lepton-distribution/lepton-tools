#!/usr/bin/env bash
# Import des skills du compte claude.ai dans le dépôt (hors étape, décision de l'utilisateur du
# 2026-11-17).
#
# Usage : scripts/importer-skills.sh [-n] [<nom>...]
#   -n  essai à blanc : affiche l'état de chaque skill et le diff dépôt → compte, n'écrit rien.
#
# Les skills du dépôt se modifient sur le compte claude.ai (Claude Desktop). Claude Code en
# télécharge une copie dans ~/.claude/skills/synced/<bucket>/<nom>/ au démarrage d'une session
# (`claude -p` lancé hors du dépôt suffit). Ce script recopie cette copie dans
# .claude/skills/<nom>/ du dépôt, fichiers retirés sur le compte compris.
# Sans argument : les skills déjà présents dans .claude/skills/. Un nouveau skill se nomme en
# argument ; les autres skills du compte ne sont jamais copiés.
# Contrôles, pour tous les skills avant toute écriture (tout ou rien) : nom en [a-z0-9-], une seule
# copie synchronisée (<bucket>), SKILL.md présent côté compte, `name:` du frontmatter égal au nom,
# aucun lien symbolique, aucune modification non commitée ni fichier non suivi sous
# .claude/skills/<nom>/. Les .DS_Store ne sont ni comparés ni copiés. Le script ne commite pas.
# Codes de retour : 0 copié ou rien à copier (ou accepté avec -n), 1 usage, 2 refus ou échec.
set -u
export LC_ALL=C

nom="importer-skills"

usage() {
  echo "usage : $nom [-n] [<nom>...]" >&2
  exit 1
}

refus() {
  printf '%s : refus : %s\n' "$nom" "$*" >&2
  exit 2
}

blanc=0
while [ $# -gt 0 ]; do
  case "$1" in
    -n) blanc=1; shift ;;
    --) shift; break ;;
    -*) usage ;;
    *) break ;;
  esac
done

racine="$(cd "$(dirname "$0")/.." && pwd -P)" || refus "racine du dépôt introuvable"
haut="$(git -C "$racine" rev-parse --show-toplevel 2>/dev/null)" || refus "$racine n'est pas un dépôt git"
haut="$(cd "$haut" && pwd -P)"
[ "$haut" = "$racine" ] || refus "$racine n'est pas la racine du dépôt git ($haut)"
skills="$racine/.claude/skills"
[ -L "$skills" ] && refus "$skills est un lien symbolique"

# Copie synchronisée du compte : un seul <bucket> porteur d'un manifest.json.
synced="$HOME/.claude/skills/synced"
relance="lancer une session Claude Code, ou claude -p hors du dépôt"
buckets=()
for m in "$synced"/*/manifest.json; do
  [ -f "$m" ] && buckets+=("${m%/manifest.json}")
done
case ${#buckets[@]} in
  0) refus "aucune copie synchronisée dans $synced ($relance)" ;;
  1) compte="${buckets[0]}" ;;
  *) refus "plusieurs copies synchronisées dans $synced : $(printf '%s ' "${buckets[@]##*/}")" ;;
esac

noms=()
if [ $# -gt 0 ]; then
  noms=("$@")
else
  for f in "$skills"/*/SKILL.md; do
    [ -f "$f" ] || continue
    d="${f%/SKILL.md}"
    noms+=("${d##*/}")
  done
  [ ${#noms[@]} -gt 0 ] || refus "aucun skill dans $skills ; nommer le skill à importer"
fi
for s in "${noms[@]}"; do
  case "$s" in
    "" | -* | *[!a-z0-9-]*)
      echo "$nom : nom invalide : « $s » (attendu : [a-z0-9-])" >&2
      usage
      ;;
  esac
done

# name: du frontmatter (bloc --- … --- en tête du fichier).
nom_frontmatter() {
  awk '
    { sub(/\r$/, "") }
    NR == 1 { if ($0 != "---") exit; next }
    /^---[[:space:]]*$/ { exit }
    /^name:/ {
      sub(/^name:[[:space:]]*/, ""); sub(/[[:space:]]*$/, "")
      gsub(/^["\047]|["\047]$/, "")
      print; exit
    }' "$1"
}

# Contrôles : tous les skills avant toute écriture.
for s in "${noms[@]}"; do
  src="$compte/$s"
  [ -L "$src" ] && refus "$s : $src est un lien symbolique"
  [ -f "$src/SKILL.md" ] || refus "$s : absent de la copie synchronisée $compte (téléversé sur claude.ai ? $relance)"
  n="$(nom_frontmatter "$src/SKILL.md")"
  [ "$n" = "$s" ] || refus "$s : le frontmatter de $src/SKILL.md porte name: « $n »"
  [ -z "$(find "$src" -type l -print)" ] || refus "$s : lien symbolique dans $src"
  [ -L "$skills/$s" ] && refus "$s : $skills/$s est un lien symbolique"
  sale="$(git -C "$racine" status --porcelain --untracked-files=all -- ".claude/skills/$s")" \
    || refus "$s : git status en échec"
  [ -z "$sale" ] || refus "$s : modifications non commitées ou fichiers non suivis dans .claude/skills/$s :
$sale"
done

# Comparaison dépôt → compte.
etats=()
i=0
for s in "${noms[@]}"; do
  src="$compte/$s"
  dst="$skills/$s"
  if [ ! -e "$dst" ]; then
    e="nouveau"
  else
    diff -rq -x .DS_Store "$dst" "$src" >/dev/null 2>&1
    case $? in
      0) e="identique" ;;
      1) e="modifié" ;;
      *) refus "$s : comparaison impossible ($dst, $src)" ;;
    esac
  fi
  etats[i]="$e"
  i=$((i + 1))
  echo "$s : $e"
  if [ "$blanc" -eq 1 ]; then
    case "$e" in
      modifié) diff -ru -x .DS_Store "$dst" "$src" ;;
      nouveau) (cd "$src" && find . -type f ! -name .DS_Store | sort | sed 's|^\./|  + |') ;;
    esac
  fi
done

[ "$blanc" -eq 1 ] && exit 0

# Copie : dossier temporaire, puis remplacement du dossier du dépôt.
tmp=""
trap '[ -n "$tmp" ] && rm -rf "$tmp"' EXIT
i=0
for s in "${noms[@]}"; do
  e="${etats[i]}"
  i=$((i + 1))
  [ "$e" = "identique" ] && continue
  mkdir -p "$skills" || refus "création de $skills impossible"
  tmp="$skills/.import-$s.$$"
  cp -R "$compte/$s" "$tmp" || refus "$s : copie vers $tmp en échec"
  find "$tmp" -name .DS_Store -type f -exec rm -f {} + || refus "$s : retrait des .DS_Store en échec"
  rm -rf "${skills:?}/$s" || refus "$s : retrait de l'ancien $skills/$s en échec"
  mv "$tmp" "$skills/$s" || refus "$s : remplacement de $skills/$s en échec"
  tmp=""
  echo "copié : $s"
done

git -C "$racine" status --short --untracked-files=all -- .claude/skills
