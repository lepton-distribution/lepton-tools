#!/usr/bin/env bash
# ENV-59 : autres chemins saisis sans `expanduser()` (hors D17), avec `~` non développé (origine
# passée entre guillemets, comme d'un appel en liste). Rien n'est écrit hors de <W> (répertoire de
# travail vide, sous essais/) et de <C> (rootstock d'essai) ; aucun chemin hors d'essais/.
# Usage : autres.sh <rootstock d'essai> <répertoire de travail W> <sortie brute> <sortie versionnée>
#
#   o1  -C DIR (rootstock.py:226), `check`, dans W ; o1d : même mot développé par bash
#   o2  seed new -C DIR (seed.py:369) et --seed-repo DIR (seed.py:372), dans W ; origines locales
#       en place prises dans <C> (aucun clone, aucun accès réseau)
#   o3  scion new --repo DIR (scions.py:125) --no-seed, dans W, rootstock <C> par -C absolu
#   o4  file owner PATH (files.py:94, _locate), dans <C> ; o4d : même mot développé
#   o5  file add PATH (files.py:94), dans <C>
#   o6  generate --clangd PATH (generate.py:117), dans <C> ; PATH = lien vers le clangd de l'hôte
#       placé dans W ; forme développée non lancée (generate écrirait dans <C>)
# État de <C> comparé au départ (env-55-url-file/etat.sh) après chaque cas qui y touche ;
# arborescence de W relevée après chaque cas.
set -u
export LC_ALL=C
C=$1 W=$2 brut=$3 vers=$4
here=$(cd "$(dirname "$0")" && pwd)
RL=$here/../env-51-messages/releve.sh
ETAT=$here/../env-55-url-file/etat.sh
U=$(id -un)
develop() { bash -c "printf '%s' $1"; }
for d in "$C" "$W"; do case $d in "$HOME"/lepton-tools-dev/essais/?*) ;; *) echo "$d hors d'essais/" >&2; exit 2 ;; esac; done
[ -d "$W" ] && [ -n "$(ls -A "$W")" ] && { echo "$W non vide" >&2; exit 2; }
mkdir -p "$W" "$brut" "$vers"
uC=${C#"$HOME"/} uW=${W#"$HOME"/}
bash "$ETAT" "$C" "$brut/etat-depart" >"$brut/depart.etat"
clones() { for c in original family-qemu-mps2 bsp-qemu-mps2-an386; do
  printf '%s %s %s\n' "$c" "$(git -C "$C/depots/lepton/$c/master" rev-parse --short HEAD)" \
    "$(git -C "$C/depots/lepton/$c/master" status --short | wc -l | tr -d ' ')"; done; }
clones >"$brut/clones-depart.txt"

cas() {  # <nom> <répertoire> <commande…>
  local nom=$1 dir=$2; shift 2
  bash "$RL" "$brut" "$nom" "$dir" "$@" >>"$brut/journal.txt" 2>&1
  printf '%s\tcode %s\t%s\n' "$nom" "$(cat "$brut/$nom.code")" "$*"
  (cd "$W" && find . -mindepth 1 -maxdepth 6 ! -path '*/.git/*' ! -path './*/*/*/*/*/*/*' | sort) >"$brut/$nom.W"
}

etat() {  # <nom> : <C> comparé au départ ; clones de <C> (HEAD, fichiers modifiés)
  local nom=$1 f
  bash "$ETAT" "$C" "$brut/etat-$nom" >/dev/null
  for f in liens casses reguliers graine grafted depots; do
    cmp -s "$brut/etat-depart/$f.txt" "$brut/etat-$nom/$f.txt" && printf '%s = départ\n' "$f" \
      || printf '%s ≠ départ\n' "$f"
  done >"$brut/$nom.etat"
  clones >"$brut/clones-$nom.txt"
  cmp -s "$brut/clones-depart.txt" "$brut/clones-$nom.txt" && echo "clones = départ" >>"$brut/$nom.etat" \
    || echo "clones ≠ départ" >>"$brut/$nom.etat"
  printf '  état : %s\n' "$(grep -v ' = départ$' "$brut/$nom.etat" | tr '\n' ';')"
}

cas o1 "$W" lepton check -C "~/$uC"
cas o1d "$W" lepton check -C "$(develop "~/$uC")"
cas o2 "$W" lepton seed new env59new -C "~/lepton-tools-dev/essais/env-59-new" \
  --seed-repo "~/lepton-tools-dev/essais/env-59-graine" \
  --bsp qemu-mps2-an386 --backend freertos --mkconf sys/user/tauon-basic/etc/mkconf_tauon_basic_qemu_mps2.xml \
  --origin "lepton-noyau=$C/depots/lepton/original/master" \
  --origin "qemu-mps2=$C/depots/lepton/family-qemu-mps2/master" \
  --origin "qemu-mps2-an386=$C/depots/lepton/bsp-qemu-mps2-an386/master"
etat o2
for d in env-59-new env-59-graine; do [ -e "$HOME/lepton-tools-dev/essais/$d" ] && echo "  $d créé sous essais/"; done
cas o3 "$W" lepton scion new env59repo --type bibliotheque --repo "~/lepton-tools-dev/essais/env-59-repo" \
  --no-seed --no-cmake -C "$C"
etat o3
[ -e "$HOME/lepton-tools-dev/essais/env-59-repo" ] && echo "  env-59-repo créé sous essais/"
cas o4 "$C" lepton file owner "~/$uC/trunk/CMakeLists.txt" --json
cas o4d "$C" lepton file owner "$(develop "~/$uC/trunk/CMakeLists.txt")" --json
cas o5 "$C" lepton file add "~/$uC/trunk/sys/root/src/lib/env59-nouveau.c"
etat o5
mkdir -p "$W/outils" && ln -s "$(command -v clangd-mp-21)" "$W/outils/clangd"
cas o6 "$C" lepton generate --clangd "~/$uW/outils/clangd"
etat o6
# formes tapées au shell (zsh, mots non cités) où le shell ne développe pas `~` : après « = »
# (`NOM=~/…` dont le nom porte un tiret ; `--option=~/…`) ; aucune écriture attendue
cas o7 "$W" zsh -c "lepton seed new env59o7 -C $W/o7 --bsp qemu-mps2-an386 --mkconf x.xml \
--origin lepton-noyau=$C/depots/lepton/original/master \
--origin qemu-mps2=~/$uC/depots/lepton/family-qemu-mps2/master@master \
--origin qemu-mps2-an386=$C/depots/lepton/bsp-qemu-mps2-an386/master"
cas o8 "$W" zsh -c "lepton check --rootstock=~/$uC"

for f in "$brut"/*.cmd "$brut"/*.out "$brut"/*.err "$brut"/*.code "$brut"/*.etat "$brut"/*.W; do
  sed -e "s#$C#<C>#g" -e "s#$W#<W>#g" -e "s#$HOME#<HOME>#g" -e "s#~$U/#~<U>/#g" "$f" >"$vers/$(basename "$f")"
done
