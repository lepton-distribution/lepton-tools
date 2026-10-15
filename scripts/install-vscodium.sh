#!/usr/bin/env bash
# install-vscodium.sh — Environnement de développement Lepton : VSCodium, extensions épinglées
# (Open VSX), chaîne de construction (par les scripts du noyau), scion et lepton (ENV-10,
# exigences INS-1 à INS-6).
#
# Usage : scripts/install-vscodium.sh [--dry-run] [--skip-toolchain] [--no-lepton]
#                                     [--lepton-clone DIR] [--seed-scions DIR]
#   --dry-run          affiche les actions sans les exécuter (les contrôles d'état sont faits)
#   --skip-toolchain   n'appelle pas install-macos.sh / install-debian.sh
#   --no-lepton        n'installe pas l'outil lepton
#   --lepton-clone DIR clone du noyau Lepton qui porte scripts/install-{macos,debian}.sh
#                      (défaut : $LEPTON_CLONE, exporté par scripts/lepton-env.sh du noyau)
#   --seed-scions DIR  clone local de seed.scions qui porte le tag SCION_REF (défaut : dépôt GitHub)
#
# Hôtes : macOS x86_64 (Intel), macOS arm64 (Apple Silicon, non validé sur machine), Debian
# x86_64. Tout autre hôte : arrêt.
# - VSCodium : .dmg (macOS) ou .deb (Debian) de la release GitHub VSCodium/vscodium, version
#   épinglée, somme SHA-256 vérifiée. Ni port MacPorts (inexistant), ni cask Homebrew, ni dépôt
#   APT : aucun ne permet d'épingler la version.
# - Gestionnaire de paquets : celui que choisit install-macos.sh (MacPorts sur Intel, Homebrew
#   sur Apple Silicon) ou APT (install-debian.sh) ; ce script n'en appelle aucun lui-même
#   (INS-3, INS-5), sauf APT pour le .deb de VSCodium.
# - Extensions : scripts/extensions.lst (une ligne éditeur.nom@version), depuis Open VSX ;
#   CodeLLDB depuis le paquet de la plateforme de sa release GitHub (somme épinglée ci-dessous).
# - Réglages utilisateur de VSCodium : mises à jour automatiques et télémétrie Red Hat coupées,
#   lemminx natif (PA-10) ; fusion dans settings.json, copie .bak avant écriture.
# - scion (pipx, version SCION_REF) et lepton (pipx install de ce dépôt).
#
# Rejouable : chaque étape teste l'état avant d'agir ; le compte des changements est affiché à la
# fin. Ce que le script ne fait pas : installer MacPorts, Homebrew, pipx hors scripts du noyau,
# remplacer un VSCodium d'une autre version (il s'arrête), désinstaller une extension, créer un
# lien de `codium` dans un répertoire système.
# Code de retour : 0 succès, 1 échec (message avec l'action corrective), 2 usage.
# Compatible bash 3.2.

set -euo pipefail

# --- Versions épinglées (PA-10, 2026-10-15) ------------------------------------
VSCODIUM_VERSION="1.135.06055"
VSCODIUM_SHA256_DARWIN_X64="7a879b8e5d650b3b1143f62339c068022b313402680afb0ee9ff59e869a82dfe"
VSCODIUM_SHA256_DARWIN_ARM64="a012e4f84f447bb3e7fd596331242ded7cae575dbd734147f4f7cb33ea0b9fe4"
VSCODIUM_SHA256_LINUX_AMD64="5f5c00a9da9d232e4c84e9eee68bbdeb4d8737462022626ce3bdb6948f3d8649"
CODELLDB_ID="vadimcn.vscode-lldb"
CODELLDB_SHA256_DARWIN_X64="e25cc716b94c62c07fec268ff2785d2b797245b160502baef8b9c970a0c4d8e8"
CODELLDB_SHA256_DARWIN_ARM64="2f114a990e1b368dd1dbd33c80c0e719767af2d228391ec0df0571c957f9ac91"
CODELLDB_SHA256_LINUX_X64="1cd7f386598022b51a5b93b9ffa23e812b23f519cfe1833384ec4bef4bfd1be1"
SCION_REF="0.5.1.0"

LEPTON_TOOLS="$(cd "$(dirname "$0")/.." && pwd)"
EXTENSIONS_LST="$LEPTON_TOOLS/scripts/extensions.lst"

DRY_RUN=0
SKIP_TOOLCHAIN=0
NO_LEPTON=0
LEPTON_CLONE_DIR="${LEPTON_CLONE:-}"
SEED_SCIONS_DIR=""
CHANGES=0
TMP=""
MOUNT=""

usage() { sed -n '6,13p' "$0" | sed 's/^# \{0,1\}//'; }

while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run)        DRY_RUN=1; shift ;;
    --skip-toolchain) SKIP_TOOLCHAIN=1; shift ;;
    --no-lepton)      NO_LEPTON=1; shift ;;
    --lepton-clone)   LEPTON_CLONE_DIR="${2:?--lepton-clone : répertoire manquant}"; shift 2 ;;
    --seed-scions)    SEED_SCIONS_DIR="${2:?--seed-scions : répertoire manquant}"; shift 2 ;;
    -h|--help)        usage; exit 0 ;;
    *) echo "option inconnue : $1" >&2; usage >&2; exit 2 ;;
  esac
done

log()  { printf '\n== %s\n' "$*"; }
info() { printf '  %s\n' "$*"; }
warn() { printf 'AVERTISSEMENT: %s\n' "$*" >&2; }
die()  { printf 'ERREUR: %s\n' "$*" >&2; exit 1; }
have() { command -v "$1" >/dev/null 2>&1; }

# run CMD… : exécute une action qui modifie l'hôte (affichée seulement en --dry-run).
run() {
  CHANGES=$((CHANGES + 1))
  if [ "$DRY_RUN" = 1 ]; then
    printf '  [dry-run]'; printf ' %q' "$@"; printf '\n'
  else
    "$@"
  fi
}

nettoyer() {
  if [ -n "$MOUNT" ]; then hdiutil detach -quiet "$MOUNT" || true; fi
  if [ -n "$TMP" ]; then rm -rf "$TMP"; fi
}
trap nettoyer EXIT

tmpdir() { [ -n "$TMP" ] || TMP="$(mktemp -d)"; }

sha256() {
  if have shasum; then shasum -a 256 "$1" | awk '{print $1}'; else sha256sum "$1" | awk '{print $1}'; fi
}

# telecharger URL FICHIER SHA256 : téléchargement puis contrôle de la somme épinglée.
telecharger() {
  curl -fsSL --retry 3 -o "$2" "$1" || die "téléchargement de $1 impossible : vérifier le réseau, puis rejouer."
  local got
  got="$(sha256 "$2")"
  [ "$got" = "$3" ] || die "SHA-256 de $(basename "$2") inattendu ($got, attendu $3) : rien n'a été installé ; vérifier la version épinglée dans $0."
}

# --- Hôte ------------------------------------------------------------------------
detecter_hote() {
  log "Hôte"
  local s m
  s="$(uname -s)"; m="$(uname -m)"
  case "$s-$m" in
    Darwin-x86_64|Darwin-arm64)
      # Sous Rosetta, uname -m répond x86_64 sur Apple Silicon : mauvais .dmg et mauvaise chaîne.
      if [ "$(sysctl -n sysctl.proc_translated 2>/dev/null || echo 0)" = "1" ]; then
        die "shell lancé sous Rosetta : relancer depuis un terminal natif (arch -arm64 bash $0)."
      fi
      OS=macos
      if [ "$m" = x86_64 ]; then PLATEFORME=darwin-x64; else PLATEFORME=darwin-arm64; fi
      APP="/Applications/VSCodium.app"
      CODIUM="$APP/Contents/Resources/app/bin/codium"
      SETTINGS="$HOME/Library/Application Support/VSCodium/User/settings.json"
      TOOLCHAIN_SCRIPT="install-macos.sh" ;;
    Linux-x86_64)
      [ -r /etc/debian_version ] || die "Linux autre que Debian : non pris en charge (hôtes : macOS, Debian x86_64)."
      OS=debian
      PLATEFORME=linux-x64
      CODIUM="codium"
      SETTINGS="${XDG_CONFIG_HOME:-$HOME/.config}/VSCodium/User/settings.json"
      TOOLCHAIN_SCRIPT="install-debian.sh" ;;
    *) die "hôte non pris en charge : $s $m (macOS x86_64 ou arm64, Debian x86_64)." ;;
  esac
  info "$s $m → $OS ($PLATEFORME)"
}

# --- Chaîne de construction (INS-3) ------------------------------------------------
installer_chaine() {
  log "Chaîne de construction ($TOOLCHAIN_SCRIPT du noyau)"
  if [ "$SKIP_TOOLCHAIN" = 1 ]; then info "sautée (--skip-toolchain)"; return; fi
  [ -n "$LEPTON_CLONE_DIR" ] \
    || die "clone du noyau inconnu : passer --lepton-clone <clone du noyau> (ou sourcer scripts/lepton-env.sh), ou --skip-toolchain."
  local script="$LEPTON_CLONE_DIR/scripts/$TOOLCHAIN_SCRIPT"
  [ -f "$script" ] || die "$script introuvable : vérifier --lepton-clone (racine du clone du noyau)."
  # --with-debug-tools : OpenOCD et gdb font partie de la chaîne visée par INS-3.
  # Le script du noyau est rejouable ; il n'est pas compté comme un changement.
  if [ "$DRY_RUN" = 1 ]; then
    printf '  [dry-run] SCION_REF=%q SCION_SPEC=%q bash %q --with-debug-tools\n' "$SCION_REF" "$SCION_SPEC" "$script"
  else
    SCION_REF="$SCION_REF" SCION_SPEC="$SCION_SPEC" bash "$script" --with-debug-tools
  fi
}

# --- scion (INS-6) -------------------------------------------------------------------
installer_scion() {
  log "scion $SCION_REF"
  if have scion && scion version 2>/dev/null | grep -q "scion version: ${SCION_REF}\$"; then
    info "déjà installé ($(command -v scion))"; return
  fi
  have pipx || die "pipx absent : lancer sans --skip-toolchain (le script de la chaîne l'installe), ou installer pipx, puis rejouer."
  run pipx install --force "$SCION_SPEC"
}

# --- VSCodium (INS-1) -----------------------------------------------------------------
version_vscodium() {
  if [ "$OS" = macos ]; then
    [ -f "$APP/Contents/Info.plist" ] && /usr/libexec/PlistBuddy -c 'Print :CFBundleShortVersionString' "$APP/Contents/Info.plist" 2>/dev/null || true
  else
    dpkg-query -W -f='${Version}' codium 2>/dev/null || true
  fi
}

installer_vscodium() {
  log "VSCodium $VSCODIUM_VERSION"
  local v
  v="$(version_vscodium)"
  if [ "$v" = "$VSCODIUM_VERSION" ]; then info "déjà installé"; return; fi
  if [ -n "$v" ]; then
    if [ "$OS" = macos ]; then
      die "VSCodium $v présent dans $APP (attendu $VSCODIUM_VERSION) : le retirer (brew uninstall --cask vscodium s'il vient de Homebrew, sinon le mettre à la corbeille ; réglages et extensions sont conservés), puis rejouer."
    else
      die "codium $v installé (attendu $VSCODIUM_VERSION) : « sudo apt-get remove codium » (réglages et extensions conservés ; retirer aussi le dépôt APT de VSCodium s'il est configuré), puis rejouer."
    fi
  fi
  if [ "$OS" = macos ]; then installer_vscodium_dmg; else installer_vscodium_deb; fi
}

installer_vscodium_dmg() {
  local arch somme nom
  if [ "$PLATEFORME" = darwin-x64 ]; then arch=x64; somme="$VSCODIUM_SHA256_DARWIN_X64"
  else arch=arm64; somme="$VSCODIUM_SHA256_DARWIN_ARM64"; fi
  nom="VSCodium.$arch.$VSCODIUM_VERSION.dmg"
  local url="https://github.com/VSCodium/vscodium/releases/download/$VSCODIUM_VERSION/$nom"
  if [ "$DRY_RUN" = 1 ]; then
    run curl -fL -o "$nom" "$url"
    run ditto "<$nom>/VSCodium.app" "$APP"
    return
  fi
  [ -w "$(dirname "$APP")" ] || die "$(dirname "$APP") non inscriptible : relancer depuis un compte administrateur."
  tmpdir
  telecharger "$url" "$TMP/$nom" "$somme"
  MOUNT="$TMP/montage"
  mkdir -p "$MOUNT"
  hdiutil attach -quiet -nobrowse -readonly -noautoopen -mountpoint "$MOUNT" "$TMP/$nom" \
    || die "montage de $nom impossible : image à vérifier."
  run ditto "$MOUNT/VSCodium.app" "$APP"
  hdiutil detach -quiet "$MOUNT"; MOUNT=""
  [ "$(version_vscodium)" = "$VSCODIUM_VERSION" ] || die "version de $APP inattendue après copie."
}

installer_vscodium_deb() {
  local nom="codium_${VSCODIUM_VERSION}_amd64.deb"
  local url="https://github.com/VSCodium/vscodium/releases/download/$VSCODIUM_VERSION/$nom"
  if [ "$DRY_RUN" = 1 ]; then
    run curl -fL -o "$nom" "$url"
    run sudo apt-get install -y --no-install-recommends "./$nom"
    return
  fi
  tmpdir
  telecharger "$url" "$TMP/$nom" "$VSCODIUM_SHA256_LINUX_AMD64"
  if [ "$(id -u)" -eq 0 ]; then
    run apt-get install -y --no-install-recommends "$TMP/$nom"
  else
    run sudo apt-get install -y --no-install-recommends "$TMP/$nom"
  fi
  [ "$(version_vscodium)" = "$VSCODIUM_VERSION" ] || die "version de codium inattendue après installation."
}

trouver_codium() {
  log "Commande codium"
  if [ "$OS" = macos ]; then
    if [ ! -x "$CODIUM" ]; then
      [ "$DRY_RUN" = 1 ] && { info "$CODIUM (après installation)"; return; }
      die "$CODIUM introuvable : installation de VSCodium incomplète."
    fi
    info "$CODIUM"
    if ! have codium; then
      info "codium n'est pas dans le PATH (aucun lien créé) : ajouter $(dirname "$CODIUM") au PATH,"
      info "ou, dans VSCodium, « Shell Command: Install 'codium' command in PATH »."
    fi
  else
    have codium || { [ "$DRY_RUN" = 1 ] && { info "codium (après installation)"; return; }; die "codium absent du PATH après installation du .deb."; }
    info "$(command -v codium)"
  fi
}

# --- Extensions (INS-2) ---------------------------------------------------------------
lire_extensions() {
  [ -f "$EXTENSIONS_LST" ] || die "$EXTENSIONS_LST introuvable."
  sed -e 's/#.*//' -e 's/[[:space:]]//g' "$EXTENSIONS_LST" | grep -v '^$' || true
}

extensions_installees() {
  if [ -x "$CODIUM" ] || have "$CODIUM"; then
    "$CODIUM" --list-extensions --show-versions 2>/dev/null | tr '[:upper:]' '[:lower:]'
  fi
}

# Le paquet de la plateforme contient l'adaptateur ; l'amorce d'Open VSX non.
codelldb_complet() {
  local d
  for d in "$HOME/.vscode-oss/extensions/$CODELLDB_ID-$1"*; do
    [ -x "$d/adapter/codelldb" ] && return 0
  done
  return 1
}

installer_codelldb() {
  local version="$1" somme
  case "$PLATEFORME" in
    darwin-x64)   somme="$CODELLDB_SHA256_DARWIN_X64" ;;
    darwin-arm64) somme="$CODELLDB_SHA256_DARWIN_ARM64" ;;
    linux-x64)    somme="$CODELLDB_SHA256_LINUX_X64" ;;
  esac
  local nom="codelldb-$PLATEFORME.vsix"
  local url="https://github.com/vadimcn/codelldb/releases/download/v$version/$nom"
  if [ "$DRY_RUN" = 1 ]; then
    run curl -fL -o "$nom" "$url"
    run "$CODIUM" --install-extension "$nom" --force
    return
  fi
  tmpdir
  telecharger "$url" "$TMP/$nom" "$somme"
  run "$CODIUM" --install-extension "$TMP/$nom" --force
}

installer_extensions() {
  log "Extensions ($EXTENSIONS_LST)"
  local installees ligne id version actuelle
  installees="$(extensions_installees)"
  for ligne in $(lire_extensions); do
    id="$(printf '%s' "${ligne%@*}" | tr '[:upper:]' '[:lower:]')"
    version="${ligne#*@}"
    case "$ligne" in
      ?*.?*@?*) ;;
      *) die "ligne invalide dans $EXTENSIONS_LST : « $ligne » (attendu éditeur.nom@version)." ;;
    esac
    actuelle="$(printf '%s\n' "$installees" | awk -F@ -v id="$id" '$1 == id { print $2 }')"
    if [ "$id" = "$CODELLDB_ID" ]; then
      if [ "$actuelle" = "$version" ] && codelldb_complet "$version"; then
        info "$id@$version : déjà installée (paquet $PLATEFORME)"
      else
        installer_codelldb "$version"
      fi
      continue
    fi
    if [ "$actuelle" = "$version" ]; then
      info "$id@$version : déjà installée"
    elif [ -n "$actuelle" ]; then
      info "$id : $actuelle → $version"
      run "$CODIUM" --install-extension "$id@$version" --force
    else
      run "$CODIUM" --install-extension "$id@$version"
    fi
  done
  # Extensions présentes hors liste : signalées, jamais retirées.
  local liste
  liste="$(lire_extensions | sed 's/@.*//' | tr '[:upper:]' '[:lower:]')"
  printf '%s\n' "$installees" | sed 's/@.*//' | grep -v '^$' | while read -r id; do
    printf '%s\n' "$liste" | grep -qx "$id" || info "hors liste (conservée) : $id"
  done
}

# --- Réglages utilisateur (PA-10) --------------------------------------------------------
# Fusion JSON par python3 : code 0 = rien à changer, 10 = changements à faire (mode verifier),
# 11 = fichier illisible (commentaires JSONC, syntaxe).
fusion_reglages() {
  python3 -I - "$1" "$2" <<'EOF'
import json, os, shutil, sys
mode, chemin = sys.argv[1], sys.argv[2]
voulus = {
    "update.mode": "none",
    "extensions.autoUpdate": False,
    "extensions.autoCheckUpdates": False,
    "redhat.telemetry.enabled": False,
    "xml.server.preferBinary": True,
}
actuels = {}
if os.path.exists(chemin):
    try:
        with open(chemin, encoding="utf-8") as f:
            texte = f.read()
        actuels = json.loads(texte) if texte.strip() else {}
    except ValueError as e:
        print(f"  {chemin} illisible en JSON strict ({e})")
        sys.exit(11)
    if not isinstance(actuels, dict):
        sys.exit(11)
diff = {k: v for k, v in voulus.items() if actuels.get(k, object()) != v}
for k, v in diff.items() if mode == "verifier" else ():
    print(f"  {k} : {json.dumps(actuels.get(k)) if k in actuels else '(absent)'} → {json.dumps(v)}")
if not diff:
    sys.exit(0)
if mode == "verifier":
    sys.exit(10)
if os.path.exists(chemin):
    shutil.copy2(chemin, chemin + ".bak")
os.makedirs(os.path.dirname(chemin), exist_ok=True)
actuels.update(diff)
with open(chemin, "w", encoding="utf-8") as f:
    json.dump(actuels, f, indent=4, ensure_ascii=False)
    f.write("\n")
EOF
}

regler_vscodium() {
  log "Réglages utilisateur ($SETTINGS)"
  local rc=0
  fusion_reglages verifier "$SETTINGS" || rc=$?
  case "$rc" in
    0)  info "déjà conformes" ;;
    10) run fusion_reglages ecrire "$SETTINGS" ;;
    11) warn "réglages non modifiés : ajouter à la main dans $SETTINGS : update.mode \"none\", extensions.autoUpdate false, extensions.autoCheckUpdates false, redhat.telemetry.enabled false, xml.server.preferBinary true." ;;
    *)  die "fusion des réglages en échec (code $rc) : python3 est-il installé ?" ;;
  esac
}

# --- lepton (INS-6) ----------------------------------------------------------------------
installer_lepton() {
  log "lepton ($LEPTON_TOOLS)"
  if [ "$NO_LEPTON" = 1 ]; then info "sauté (--no-lepton)"; return; fi
  local attendue
  attendue="$(sed -n 's/^__version__ *= *"\(.*\)"/\1/p' "$LEPTON_TOOLS/lepton/__init__.py" | head -1)"
  [ -n "$attendue" ] || die "version introuvable dans $LEPTON_TOOLS/lepton/__init__.py."
  if have lepton && [ "$(lepton --version 2>/dev/null | head -1)" = "lepton $attendue" ]; then
    info "lepton $attendue : déjà installé ($(command -v lepton))"; return
  fi
  have pipx || die "pipx absent : lancer sans --skip-toolchain (le script de la chaîne l'installe), ou installer pipx, puis rejouer."
  run pipx install --force "$LEPTON_TOOLS"
}

# --- Bilan ---------------------------------------------------------------------------------
bilan() {
  log "Bilan"
  printf '  %-12s %s\n' "VSCodium" "$(version_vscodium)"
  if [ -x "$CODIUM" ] || have "$CODIUM"; then
    "$CODIUM" --list-extensions --show-versions 2>/dev/null | sed 's/^/               /'
  fi
  printf '  %-12s %s\n' "scion" "$(scion version 2>/dev/null | tail -1 || echo absent)"
  printf '  %-12s %s\n' "lepton" "$(lepton --version 2>/dev/null | head -1 || echo absent)"
  if [ "$DRY_RUN" = 1 ]; then
    printf '  %-12s %s\n' "changements" "$CHANGES (à faire, --dry-run)"
  else
    printf '  %-12s %s\n' "changements" "$CHANGES"
  fi
}

# --- Principal -----------------------------------------------------------------------------
if [ -n "$SEED_SCIONS_DIR" ]; then
  [ -d "$SEED_SCIONS_DIR/.git" ] || die "$SEED_SCIONS_DIR n'est pas un clone git de seed.scions."
  SCION_SPEC="git+file://$(cd "$SEED_SCIONS_DIR" && pwd)@$SCION_REF"
else
  SCION_SPEC="git+https://github.com/lepton-distribution/seed.scions.git@$SCION_REF"
fi

detecter_hote
installer_chaine
installer_scion
installer_vscodium
trouver_codium
installer_extensions
regler_vscodium
installer_lepton
bilan
