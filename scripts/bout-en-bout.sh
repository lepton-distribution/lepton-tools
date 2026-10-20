#!/usr/bin/env bash
# Bout en bout d'ENV-8 (décision S4-3) : lepton seed new (noyau + famille qemu-mps2 + BSP
# qemu-mps2-an386) → lepton check → seed lock / --verify → cmake host puis an386 (freertos) →
# test de fumée QEMU (ctest -L smoke) → trunk sans fichier régulier.
#
# Usage : scripts/bout-en-bout.sh REPERTOIRE
#   REPERTOIRE reçoit le rootstock jetable (REPERTOIRE/rootstock, absent ou vide) et le journal
#   REPERTOIRE/bout-en-bout.log. Les greffons sont clonés par scion depuis le rootstock de
#   référence (URL file://localhost, branche master) : celui-ci est lu seulement, et son état git
#   est comparé avant et après.
# Variables : LEPTON (défaut : lepton), LEPTON_REF_ROOTSTOCK (défaut : ~/lepton), ARM_GCC_BIN
#   (défaut : chaîne Arm 14.2.Rel1 épinglée).
# Code de retour : 0 succès, 1 échec d'une étape, 2 outil absent.
set -u

[ $# -eq 1 ] || { echo "usage : $0 REPERTOIRE" >&2; exit 1; }
mkdir -p "$1" || exit 1
dir=$(cd "$1" && pwd)
root=$dir/rootstock
journal=$dir/bout-en-bout.log
lepton=${LEPTON:-lepton}
ref=${LEPTON_REF_ROOTSTOCK:-$HOME/lepton}
arm=${ARM_GCC_BIN:-$HOME/opt/arm-gnu-toolchain-14.2.rel1-darwin-x86_64-arm-none-eabi/bin}
preset=qemu-mps2-an386-freertos
mkconf=sys/user/tauon-basic/etc/mkconf_tauon_basic_qemu_mps2.xml
xml_projet=sys/user/bout-en-bout/etc/mkconf_bout-en-bout.xml     # copie de $mkconf dans la graine (O5)
depots_ref=(lepton/original/master lepton-famille/qemu-mps2 lepton-bsp/qemu-mps2-an386)

export PATH="$arm:$PATH"
export PYTHONDONTWRITEBYTECODE=1      # smoke_lsh.py est servi par le trunk : aucun __pycache__

for outil in "$lepton" scion cmake ninja ctest qemu-system-arm arm-none-eabi-gcc git; do
    command -v "$outil" >/dev/null || { echo "$outil absent" >&2; exit 2; }
done
if [ -e "$root" ] && [ -n "$(ls -A "$root")" ]; then
    echo "$root existe et n'est pas vide" >&2; exit 1
fi
: >"$journal"

etape() { printf '== %s\n' "$*" | tee -a "$journal"; }
lance() {
    printf '$ %s\n' "$*" >>"$journal"
    "$@" >>"$journal" 2>&1 || { echo "ÉCHEC : $* (journal : $journal)" >&2; exit 1; }
}
etat_ref() {
    for d in "${depots_ref[@]}"; do
        printf '%s %s %s\n' "$d" "$(git -C "$ref/depots/$d" rev-parse HEAD)" \
            "$(git -C "$ref/depots/$d" status --porcelain | wc -l | tr -d ' ')"
    done
}

avant=$(etat_ref)
etape "versions"
lance "$lepton" --version

etape "lepton seed new"
lance "$lepton" seed new bout-en-bout -C "$root" --bsp qemu-mps2-an386 --backend freertos --mkconf "$mkconf" \
    --origin "lepton-noyau=file://localhost$ref/depots/${depots_ref[0]}@master" \
    --origin "qemu-mps2=file://localhost$ref/depots/${depots_ref[1]}@master" \
    --origin "qemu-mps2-an386=file://localhost$ref/depots/${depots_ref[2]}@master"

etape "XML du projet greffé depuis la graine (CFG-1, O5)"
cible=$([ -L "$root/trunk/$xml_projet" ] && readlink -f "$root/trunk/$xml_projet")
case $cible in
    "$(cd "$root" && pwd -P)"/depots/lepton-seed/bout-en-bout/project/scion/*) echo "$xml_projet -> $cible" >>"$journal" ;;
    *) echo "ÉCHEC : $xml_projet absent du trunk ou hors de la graine (journal : $journal)" >&2; exit 1 ;;
esac

etape "lepton check (graine, manifestes, XML : GRA-2, GRF-5, CFG-5)"
lance "$lepton" check -C "$root"

etape "lepton seed lock puis --verify (GRA-5)"
lance "$lepton" seed lock -C "$root"
lance "$lepton" seed lock --verify -C "$root"

etape "cmake host"
cd "$root/trunk" || exit 1
lance cmake --preset host
lance cmake --build "$root/build/host"

etape "cmake $preset"
lance cmake --preset "$preset" -DLEPTON_MKCONF="$xml_projet"
lance cmake --build "$root/build/$preset"

etape "fumée QEMU (ctest -L smoke)"
lance ctest --preset "$preset" -L smoke --output-on-failure
cd "$dir" || exit 1

etape "lepton seed status (trunk sans fichier régulier ni lien cassé)"
lance "$lepton" seed status -C "$root"

etape "rootstock de référence inchangé"
apres=$(etat_ref)
if [ "$avant" != "$apres" ]; then
    printf 'ÉCHEC : état git de %s modifié\navant :\n%s\naprès :\n%s\n' "$ref" "$avant" "$apres" | tee -a "$journal" >&2
    exit 1
fi
printf '%s\n' "$apres" >>"$journal"

etape "bout en bout : succès"
