#!/usr/bin/env bash
# ENV-69 : cas couverts et regreffe ordinaire, au terminal, VSCodium (0.5.4) ouvert sur <E>.
# Usage : cas.sh <rootstock d'essai> <dépôt env69lib> <dépôt env69lib v2> <journal terminal>
# Chaque étape est horodatée dans le journal (même horloge que lepton-horodate.sh), puis suivie
# d'une pause de 4 s (regroupements de 1000 ms de F2 et de la liste greffée écoulés).
set -u
E=$1 D1=$2 D2=$3 J=$4
ms() { perl -MTime::HiRes=time -e 'printf "%d", time()*1000'; }
pas() {
  echo "$(ms) terminal $*" | sed "s|$E|<E>|g" >>"$J"
  "$@" >/dev/null 2>&1
  echo "$(ms) terminal code=$? liens=$(find "$E/trunk" -type l | wc -l | tr -d ' ') casses=$(find -L "$E/trunk" -type l | wc -l | tr -d ' ')" >>"$J"
  sleep 4
}
bsp=$E/depots/lepton/bsp-qemu-mps2-an386/master/scion/sys/root/src/kernel/dev/bsp/qemu-mps2-an386
U1="file://localhost$D1@master"; U2="file://localhost$D2@master"
pas lepton -C "$E" seed remove env69lib --no-cmake          # déclaré sans clone (D37) : 6 → 5 observés
pas rmdir "$E/depots/lepton/library-env69lib"               # répertoire vide laissé (D42)
pas touch "$bsp/env69_temoin.h"                             # regreffe ordinaire : création
pas rm "$bsp/env69_temoin.h"                                # regreffe ordinaire : suppression
pas lepton -C "$E" seed add env69lib "$U1" --type bibliotheque --no-cmake   # 5 → 6
pas lepton -C "$E" seed replace env69lib "$U2" --no-cmake  # observés inchangés
pas lepton -C "$E" seed replace env69lib "$U1" --no-cmake
pas scion graft-remove --purge lepton@library-env69lib "$E"  # 6 → 5, aucune notification attendue
pas lepton -C "$E" seed remove env69lib --no-cmake          # déclaré, non greffé
pas rmdir "$E/depots/lepton/library-env69lib"
pas lepton -C "$E" seed add env69lib "$U1" --type bibliotheque --no-cmake   # 5 → 6, pour U4
