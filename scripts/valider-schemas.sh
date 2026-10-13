#!/usr/bin/env bash
# Valide les schémas de schemas/ et leurs exemples (ENV-3).
#  - méta-validation des schémas JSON (draft 2020-12) et du XSD ;
#  - chaque exemple valide de schemas/exemples/ doit passer ;
#  - chaque exemple de schemas/exemples/invalides/ doit échouer (XML : bien formé mais refusé) ;
#  - CFG-1 : aucun nom commun aux schémas JSON et au XSD, aucun élément retiré (CFG-8) dans le XSD.
# Code de retour : 0 si tout est conforme, 1 sinon, 2 si un validateur manque ou n'a pas la
# version épinglée.
set -u

CHECK_JSONSCHEMA_VERSION=0.38.2   # pipx install check-jsonschema==0.38.2
LIBXML_VERSION=21504              # xmllint --version (libxml 2.15.4, MacPorts)

racine=$(cd "$(dirname "$0")/.." && pwd)
schemas=$racine/schemas
exemples=$schemas/exemples
invalides=$exemples/invalides
echecs=0

ok()  { printf 'ok      %s\n' "$1"; }
ko()  { printf 'ÉCHEC   %s\n' "$1"; echecs=$((echecs + 1)); }

# Versions épinglées
command -v check-jsonschema >/dev/null || { echo "check-jsonschema absent" >&2; exit 2; }
command -v xmllint >/dev/null || { echo "xmllint absent" >&2; exit 2; }
v=$(check-jsonschema --version | awk '{print $NF}')
[ "$v" = "$CHECK_JSONSCHEMA_VERSION" ] || { echo "check-jsonschema $v, attendu $CHECK_JSONSCHEMA_VERSION" >&2; exit 2; }
v=$(xmllint --version 2>&1 | sed -n 's/.*libxml version \([0-9]*\).*/\1/p' | head -1)
[ "$v" = "$LIBXML_VERSION" ] || { echo "libxml $v, attendu $LIBXML_VERSION" >&2; exit 2; }

# Schéma applicable à un exemple JSON, d'après le préfixe de son nom
schema_de() {
  case $(basename "$1") in
    graine*) echo "$schemas/graine.schema.json" ;;
    *)       echo "$schemas/greffon.schema.json" ;;
  esac
}

# 1. Méta-validation
for s in "$schemas"/*.schema.json; do
  if check-jsonschema --check-metaschema "$s" >/dev/null 2>&1; then ok "méta  ${s#$racine/}"; else ko "méta  ${s#$racine/}"; fi
done
# XSD : compilé par libxml sur un document quelconque ; l'échec du document est attendu
sortie=$(echo '<mklepton/>' | xmllint --noout --schema "$schemas/mklepton.xsd" - 2>&1)
if ! grep -q 'failed to compile' <<<"$sortie"; then
  ok "méta  schemas/mklepton.xsd"
else
  ko "méta  schemas/mklepton.xsd"
fi

# 2. Exemples valides
for f in "$exemples"/*.json; do
  if check-jsonschema --schemafile "$(schema_de "$f")" "$f" >/dev/null 2>&1; then ok "valide   ${f#$racine/}"
  else ko "valide   ${f#$racine/}"; check-jsonschema --schemafile "$(schema_de "$f")" "$f" 2>&1 | sed 's/^/        /'; fi
done
for f in "$exemples"/*.xml; do
  if xmllint --noout --schema "$schemas/mklepton.xsd" "$f" >/dev/null 2>&1; then ok "valide   ${f#$racine/}"
  else ko "valide   ${f#$racine/}"; xmllint --noout --schema "$schemas/mklepton.xsd" "$f" 2>&1 | sed 's/^/        /'; fi
done

# 3. Exemples invalides : échec attendu
for f in "$invalides"/*.json; do
  python3 -I -c 'import json,sys; json.load(open(sys.argv[1]))' "$f" 2>/dev/null \
    || { ko "invalide ${f#$racine/} (JSON mal formé : échec pour une autre raison)"; continue; }
  if check-jsonschema --schemafile "$(schema_de "$f")" "$f" >/dev/null 2>&1; then ko "invalide ${f#$racine/} accepté"
  else ok "invalide ${f#$racine/} refusé"; fi
done
for f in "$invalides"/*.xml; do
  xmllint --noout "$f" 2>/dev/null \
    || { ko "invalide ${f#$racine/} (XML mal formé : échec pour une autre raison)"; continue; }
  if xmllint --noout --schema "$schemas/mklepton.xsd" "$f" >/dev/null 2>&1; then ko "invalide ${f#$racine/} accepté"
  else ok "invalide ${f#$racine/} refusé"; fi
done

# 4. CFG-1 : recouvrement JSON / XSD
if python3 -I - "$schemas" <<'EOF'
import json, sys, pathlib, xml.etree.ElementTree as ET
d = pathlib.Path(sys.argv[1])
def proprietes(n, acc):
    if isinstance(n, dict):
        for k, v in n.items():
            if k == "properties" and isinstance(v, dict):
                acc.update(x for x in v if x != "$schema")
            proprietes(v, acc)
    elif isinstance(n, list):
        for v in n: proprietes(v, acc)
    return acc
noms_json = set()
for f in d.glob("*.schema.json"):
    proprietes(json.load(open(f)), noms_json)
xs = "{http://www.w3.org/2001/XMLSchema}"
noms_xsd = {e.get("name") for e in ET.parse(d / "mklepton.xsd").iter()
            if e.tag in (xs + "element", xs + "attribute")}
retires = {"target", "arch", "cpu", "freq", "include_absolute_path", "block", "option"}
# Homonymes sans information commune ; toute entrée ajoutée ici doit être justifiée.
homonymes = {
    "max": "JSON : borne d'une option entière ; XSD : maximum de processus, fichiers, descripteurs",
    "type": "JSON : type de greffon ou d'option ; XSD : type de système de fichiers d'un <disk>",
    "version": "JSON : version du greffon ou du projet ; XSD : version du format XML",
}
communs, interdits = (noms_json & noms_xsd) - homonymes.keys(), noms_xsd & retires
for n in sorted(communs): print(f"        nom commun JSON / XSD : {n}")
for n in sorted(interdits): print(f"        élément ou attribut retiré présent dans le XSD : {n}")
sys.exit(1 if communs or interdits else 0)
EOF
then ok "CFG-1 aucun recouvrement JSON / XSD"; else ko "CFG-1 recouvrement JSON / XSD"; fi

echo
if [ "$echecs" -eq 0 ]; then echo "Conforme."; exit 0; fi
echo "$echecs échec(s)."; exit 1
