# Exigences modifiées par le chantier « espace-projet »

Décision T9 (PA-E2, 2026-11-27) : les exigences et l'interface du chantier ENV que ce chantier
amende sont consignées ici ; `doc/devenv/` n'est pas modifié. Références : `doc/devenv/SPECIFICATION.md`
(exigences), `doc/devenv/rapports/env-8-interface.md` (interface de lepton, sections d'amendements),
`doc/devenv/DEVENV-STATUS.md` §Décisions. Une ligne par amendement : décision, avant, après.

## EP-1 — Greffon de type `projet` (lepton 0.2.0)

Rapport : `rapports/ep-1-type-projet.md`. Décision : PA-E2 (`STATUS.md` §Décisions).

| Réf. amendée | Avant | Après |
| --- | --- | --- |
| GRF-2, `schemas/greffon.schema.json` | types `noyau`, `famille`, `bsp`, `application`, `bibliotheque` ; manifeste sous `sys/root/src/<destination>/` | type `projet` ajouté : manifeste `scion/sys/user/<nom>/lepton-greffon.json`, champs `nom`, `type`, `version`, `description` seuls ; non lu par le lecteur CMake du noyau (son `GLOB` ne couvre que `sys/root/src/`) |
| GRA-1, interface §3.2 (`seed new`) | graine `depots/lepton-seed/<nom>` ou `--seed-repo` ; greffon local `lepton@project-<projet>` (version `*`) = `project/` du dépôt de la graine ; `--mkconf` requis | greffon projet **créé** (dépôt git propre `--project-repo DIR`, défaut `<rootstock>/depots/lepton-project/<nom>`, version `*`, clé `lepton@project-<nom>`, commit initial) ou **désigné** (`--origin <nom>=LOCATION[@VERSION][:PATH]`, type `projet` et nom `<nom>` exigés) ; `--mkconf` requis sauf greffon désigné qui fournit `sys/user/<nom>/etc/mkconf_<nom>.xml` ; `--project-repo` et `--origin <nom>` exclusifs ; nom du projet distinct du noyau et du BSP |
| GRA-2, `schemas/graine.schema.json` | aucun champ ne désigne le porteur des fichiers du projet | le greffon projet est le greffon de type `projet` de nom `projet.nom` (pas de nouvelle clé) ; `check` : absent → « greffon projet « <nom> » non greffé (GRA-2) » ; autre greffon `projet` greffé → anomalie |
| CFG-1, O5, interface §11 (XML du projet) | `<graine>/project/scion/sys/user/<projet>/etc/mkconf_<projet>.xml` | `<greffon projet>/scion/sys/user/<projet>/etc/mkconf_<projet>.xml` ; chemin dans le trunk inchangé ; avertissement de `check` « XML fourni par un greffon partagé, pas par le greffon projet » |
| CFG-6, interface §3.10 (`generate`) | `CMakeUserPresets.json` dans `project/scion/` de la graine ; clé du projet omise des dossiers « git · … » | `CMakeUserPresets.json` à la racine `scion/` du greffon projet, rappel de commit dans son dépôt ; dossier « git · <nom> » ajouté (dépôt distinct, IDE-2) ; `files.exclude` inchangé (`project/scion` retiré à EP-4) |
| GRA-5, interface §3.5 (`seed lock`) | clé du projet exclue du verrou (dépôt de la graine) | greffon projet figé comme les autres (son commit) ; un greffon projet modifié non commité rend la graine non figeable |
| GRA-4, interface §3.4 (`seed remove`) | noyau et BSP refusés | greffon projet refusé aussi (« est le greffon projet de la graine ») |
| GRA-6, interface §3.3 (`seed status`) | rôle « projet » par égalité de clé avec `lepton@project-<projet>` ; nom affiché `project-<projet>` | rôle « projet » d'après le type du manifeste ; nom affiché = nom du manifeste ; `stem` = racine `scion/` du greffon projet |
| PA-19 C d'ENV-16, interface §3.9 et §16 (graine de référence) | « ni `lepton-graine.json` ni `project/` » ; graine avec `project/` sans manifeste : anomalie « manifeste de graine absent » | « pas de `lepton-graine.json` » (C4) ; messages « (pas de lepton-graine.json) » |
| T8 (régime de référence avec greffon projet) | — | `generate` n'écrit aucun `CMakeUserPresets.json` ; refus de PA-23 inchangés (dont `seed mkconf import`) ; `seed status` : rôle « projet » |
| Ancien format | — | graine dont le dépôt contient `project/` : refusée par toute commande qui découvre le rootstock, code 1, « graine à l'ancien format » ; procédure manuelle au `README.md` |
| INS-6 (`lepton --version`) | 0.1.0 | 0.2.0 |
