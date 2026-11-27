# Greffon projet {{name}}

Greffon de type `projet` du projet Lepton `{{name}}`, créé par `lepton seed new`. Greffé à la racine
du trunk par sa racine `scion/` :

- `scion/sys/user/{{name}}/lepton-greffon.json` : manifeste du greffon (type `projet`) ;
- `scion/sys/user/{{name}}/etc/` : XML mklepton du projet et fichiers qu'il copie (`.boot`,
  `.init`), copiés par `lepton seed new --mkconf` ou `lepton seed mkconf import` ;
- `scion/CMakeUserPresets.json` : presets du projet, écrits par `lepton generate`.

La graine du projet (`lepton-graine.json`) désigne ce greffon par son nom (`projet.nom`).
