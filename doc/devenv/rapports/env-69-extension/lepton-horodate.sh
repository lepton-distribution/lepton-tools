#!/usr/bin/env bash
# ENV-69 : enveloppe de lepton pour l'essai VSCodium (réglage lepton.path de l'espace d'essai),
# reprise d'env-64-extension/lepton-horodate.sh.
# Journal : <ms depuis l'époque> début|fin <pid> <code> <arguments>.
journal=/Users/cle_d_anton/lepton-tools-dev/essais/env-69-releves/appels.log
ms() { perl -MTime::HiRes=time -e 'printf "%d", time()*1000'; }
echo "$(ms) début $$ - $*" >>"$journal"
/Users/cle_d_anton/.local/bin/lepton "$@"
code=$?
echo "$(ms) fin $$ $code $*" >>"$journal"
exit $code
