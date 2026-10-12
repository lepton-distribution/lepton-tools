#!/usr/bin/env bash
# capturer-oracle.sh — capture l'état de référence d'un exécutable Lepton construit.
#
# Usage : capturer-oracle.sh <fichier.elf> <répertoire-de-sortie>
#
# Produit dans <répertoire-de-sortie> :
#   empreintes.txt  SHA-256 de l'ELF et des .bin/.hex voisins de même nom
#   sections.txt    taille de chaque section (size -A), triée par nom
#   symboles.txt    symboles définis : nom, type, taille (nm -S), triés par nom
#   outils.txt      versions des outils utilisés
#
# Variables : NM, SIZE (défaut arm-none-eabi-nm, arm-none-eabi-size).
# Code de retour : 0 si succès, 1 si argument manquant ou outil absent, 2 si ELF absent.
set -euo pipefail

NM="${NM:-arm-none-eabi-nm}"
SIZE="${SIZE:-arm-none-eabi-size}"

erreur() { echo "capturer-oracle: $1" >&2; exit "${2:-1}"; }

verifier_arguments() {
    [ $# -eq 2 ] || erreur "usage : capturer-oracle.sh <fichier.elf> <répertoire-de-sortie>"
    [ -f "$1" ] || erreur "ELF introuvable : $1" 2
    command -v "$NM" >/dev/null || erreur "outil absent : $NM (définir NM)"
    command -v "$SIZE" >/dev/null || erreur "outil absent : $SIZE (définir SIZE)"
}

sha256() {
    if command -v sha256sum >/dev/null; then sha256sum "$@"; else shasum -a 256 "$@"; fi
}

capturer_empreintes() {
    local elf="$1" sortie="$2" base
    base="${elf%.elf}"
    local fichiers=("$elf")
    for ext in bin hex; do [ -f "$base.$ext" ] && fichiers+=("$base.$ext"); done
    (cd "$(dirname "$elf")" && sha256 $(for f in "${fichiers[@]}"; do basename "$f"; done)) \
        > "$sortie/empreintes.txt"
}

capturer_sections() {
    "$SIZE" -A "$1" | awk 'NR>2 && NF>=2 && $1 ~ /^\./ {print $1, $2}' | LC_ALL=C sort \
        > "$2/sections.txt"
}

capturer_symboles() {
    # nm -S --defined-only : adresse [taille] type nom ; on retire l'adresse.
    "$NM" -S --defined-only "$1" | awk '
        NF==4 {print $4, $3, $2}
        NF==3 {print $3, $2, "-"}' | LC_ALL=C sort > "$2/symboles.txt"
}

capturer_outils() {
    { "$NM" --version | head -1; "$SIZE" --version | head -1; date -u +%Y-%m-%dT%H:%M:%SZ; } \
        > "$1/outils.txt"
}

main() {
    verifier_arguments "$@"
    local elf="$1" sortie="$2"
    mkdir -p "$sortie"
    capturer_empreintes "$elf" "$sortie"
    capturer_sections "$elf" "$sortie"
    capturer_symboles "$elf" "$sortie"
    capturer_outils "$sortie"
    echo "oracle capturé dans $sortie ($(wc -l < "$sortie/symboles.txt" | tr -d ' ') symboles)"
}

main "$@"
