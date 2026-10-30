#!/usr/bin/env python3
"""ENV-14 : classement de chaque feuille du trunk -> TSV annexe (stdout).

Usage : env-14-classer.py <feuilles.tsv de env-14-inventaire.py> <perimetre.csv du clone noyau> <trunk>
1. Jointure avec l'ensemble de la migration (doc/migration/perimetre.csv : actif, différé, hors-projet).
2. Usage indirect : chemin relatif d'une feuille cité dans un fichier texte lu (XML mkconf,
   CMake, scripts de test), par passes jusqu'au point fixe.
3. Classement par les règles RULES.
"""
import collections
import csv
import os
import re
import sys

feuilles, perimetre, trunk = sys.argv[1:4]
per = {}
for r in csv.DictReader(open(perimetre)):
    f = r["fichier"]
    per["sys/root/" + f if f.startswith("src/") else f] = r["ensemble"]
rows = list(csv.DictReader(open(feuilles), delimiter="\t"))
for r in rows:
    r["ensemble"] = per.get(r["chemin"], "absent")

TXT = (".xml", ".cmake", ".sh", ".txt", ".json", ".py", ".ld", ".cfg", ".boot", ".init", ".mount")
used = {r["chemin"] for r in rows if r["lu"] == "oui"}
seen, blob = set(), []
while True:
    for p in sorted(used - seen):
        seen.add(p)
        if p.endswith(TXT) or "gdbinit" in p:
            try:
                blob.append(open(os.path.join(trunk, p), errors="replace").read())
            except OSError:
                pass
    big = "\n".join(blob)
    new = {r["chemin"] for r in rows if r["chemin"] not in used and r["chemin"] in big}
    if not new:
        break
    used |= new
lu_ind = used

# (regex, classement, lot/arbitrage, motif) : première règle qui s'applique, après « lu »
RULES = [
    (r"\.DS_Store$", "supprimer", "DS", "fichier du Finder (tâche 3)"),
    (r"^sys/user/build/", "supprimer", "L1", "SCons hérité ; seul SConstruct (tools/config) le cite"),
    (r"^tools/bin/", "supprimer", "L1", "binaires mklepton Windows/Linux précompilés et DLL ; mklepton construit par le preset host"),
    (r"^tools/config/", "supprimer", "L1", "configuration SCons héritée ; aucune référence vivante"),
    (r"^tools/host/", "supprimer", "L1", "scripts hôte Debian hérités (virtual_cpu gelé, comptage de taille) ; cités par SConstruct seulement"),
    (r"^tools/mklepton/prj/", "supprimer", "L1", "SConstruct de mklepton ; remplacé par CMake"),
    (r"^sys/root/src/kernel/net/lwip/prj/", "supprimer", "L1", "SConscript lwIP ; remplacé par CMake"),
    (r"^tauon_make_link\.bat$", "supprimer", "L1", "jonction Windows c:\\tauon ; aucune référence"),
    (r"^sys/user/tauon_sampleapp/", "supprimer", "L2", "application d'exemple non construite (SCons, K60, AT91SAM9261) ; citée par tools/config/SConstruct seulement — voir A0"),
    (r"^sys/user/tauon-basic/etc/(memo|readme)\.txt$", "supprimer", "L3", "notes Windows/AT91 périmées (fichiers cités absents)"),
    (r"^sys/root/src/bin/bin$", "supprimer", "L3", "fichier factice CVS (« dummy file in order to import obj directory »)"),
    (r"^sys/user/tauon-basic/src/arch/st-stm32wl55jci-nucleo/", "à arbitrer", "A1", "configuration IAR de la WL55, doublon du BSP nucleo-wl55jc1 ; citée en commentaire dans le BSP"),
    (r"^sys/user/tauon-basic/etc/\.init_(stm32_with_net|with_net)$", "à arbitrer", "A2", "script d'init générique, aucune référence"),
    (r"^sys/root/src/bin/net/html/", "à arbitrer", "A3", "pages web dupliquées de tauon-basic ; citées seulement par lhttpd.c (non construit)"),
    (r"^sys/user/tauon-basic/src/bin/net/html/lepton_mini\.", "à arbitrer", "A3", "image non embarquée par le XML Olimex, aucune référence"),
    (r"^sys/root/src/kernel/core/ucore/cmsis/CMSIS/(Documentation/|index\.htm$)", "à arbitrer", "A4", "documentation CMSIS 2.10 embarquée (HTML, images, XSD)"),
    (r"system_stm32f4xx\.c\.old$", "à arbitrer", "A5", "copie .old dans le greffon family-stm32f4xx"),
    # conserver, hors périmètre
    (r"/(LICEN[CS]E|COPYING|LEPTON-PROVENANCE|README|Release_Notes|History|manifest|ReadMe|readme|ChangeLog)[^/]*$|END USER LICENCE|/cmsis/(source\.txt|Version 2\.10)$", "conserver", "C-lic", "licence, provenance ou notice du code tiers"),
    (r"^sys/user/tauon-basic/src/arch/(atmel-at91sam9261-ek|win32)/|\.init_win32", "conserver, hors périmètre", "C-gel", "architecture gelée (ARM9, simulation Windows)"),
    (r"^sys/user/tauon-basic/src/arch/|\.init_samv71", "conserver, hors périmètre", "C-bsp", "BSP hors presets"),
    (r"/dev/bsp/(discovery_f4|discovery_f4-baseboard-modem|olimex_p407|samd20xplained_pro|same70xplained|samv71xplained_ultra|stm32f469i-eval)/", "conserver, hors périmètre", "C-bsp", "BSP hors presets"),
    (r"/dev/arch/(at91|cortexm/(at91samd20|at91samv7x|stellaris|stm32f1xx))/", "conserver, hors périmètre", "C-bsp", "famille sans preset (différée à la migration)"),
    (r"/ucore/freeRTOS_(8-0-0|9-0-0)/", "conserver, hors périmètre", "C-bsp", "FreeRTOS ancien cité par les configurations des BSP hors presets"),
    (r"^(tests/|debug/|cmake/)", "conserver", "C-ref", "référencé par CMake, un BSP, lepton ou BUILDING.md"),
    (r"^sys/root/src/sbin/sh/", "conserver", "C-fonc", "scripts lsh du système, embarquables par une configuration"),
    (r"^sys/", "conserver", "C-fonc", "code du système non configuré par les presets actuels (actif/différé/hors-projet au périmètre de la migration)"),
]

out = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
out.writerow(["chemin", "greffon", "versionne", "lu", "ensemble_migration", "classement", "lot", "motif"])
cnt = collections.Counter()
for r in rows:
    p = r["chemin"]
    lu = "direct" if r["lu"] == "oui" else ("indirect" if p in lu_ind else "non")
    if r["greffon"] == "REGULIER":
        cl, lot, motif = "supprimer", "DS", "fichier régulier du Finder dans le trunk (tâche 3, par l'utilisateur)"
    elif lu != "non" and not p.endswith(".DS_Store"):
        cl, lot, motif = "conserver", "C-lu", "lu par une construction ou un test (" + lu + ")"
    else:
        cl, lot, motif = next(((c, l, m) for rx, c, l, m in RULES if re.search(rx, p)),
                              ("à arbitrer", "A?", "sans règle"))
    cnt[(cl, lot)] += 1
    out.writerow([p, r["greffon"], r["versionne"], lu, r["ensemble"], cl, lot, motif])
for k, v in sorted(cnt.items()):
    print(k, v, file=sys.stderr)
