# Étape ENV-3 — Schémas

## Contexte
Les formats sont fixés par la spécification : manifestes de greffon et de graine en JSON validés
par JSON Schema (décision 9), configuration mklepton en XML validé par XSD (CFG-8). Cette étape
écrit les trois schémas, sans implémentation, pour que ENV-4, ENV-5 et ENV-8 partent d'un
contrat validé.

## Prérequis
- ENV-2 terminée ; rapports `env-2-cmake.md`, `env-2-mklepton.md`, `env-2-cartes.md` validés (PA-2).

## Tâches
Fichiers dans `<LEPTON_TOOLS>/schemas/`.

### 1. Manifeste de greffon → `greffon.schema.json`
Champs exigés par GRF-2, GRF-3, CFG-3, CFG-4 :
- `nom`, `type` (`noyau`, `bsp`, `application`, `bibliotheque`), `version`.
- `destination` (relative à `sys/root/src/`), `bibliotheque` (`kernel`, `lib`, `sbin`, `bin`,
  `bsp` ou dédiée), `sources` (répertoires découverts, FIC-4), `dependances`.
- `options` : tableau d'objets {`nom`, `type` (booléen, entier, énumération, chaîne), `defaut`,
  bornes ou valeurs, `portee` (`privee`, `publique`), `description` obligatoire}.
- Pour `type = bsp` : `coeur`, `mcu`, `script_liens`, `demarrage` (fichiers liés en OBJECT,
  BLD-1), `openocd` (fichiers de configuration), `sonde`, `svd`, `qemu` (machine, facultatif).
Draft JSON Schema : 2020-12, sauf contre-indication relevée en ENV-1 (version gérée par VSCodium).

### 2. Manifeste de graine → `graine.schema.json`
Projet, greffons (noyau et BSP obligatoires, application et bibliothèque facultatifs, GRA-2),
backend micro-noyau, configurations (debug, release, QEMU, carte — CFG-6), chemin du XML
mklepton. Aucun champ de configuration logicielle (CFG-1).

### 3. XSD mklepton → `mklepton.xsd`
À partir de `env-2-mklepton.md` : éléments conservés, élément racine portant un attribut
`version`. Aucun élément de cœur, d'architecture ou de backend (CFG-8).

### 4. Exemples et validation
- `schemas/exemples/` : un manifeste par type de greffon (dont les BSP `mps2-an386`,
  NUCLEO-F429ZI, NUCLEO-WL55JC1), une graine, un XML.
- Script `scripts/valider-schemas.sh` (`check-jsonschema` et `xmllint --schema`, versions
  épinglées) qui valide tous les exemples ; exemples invalides dans `schemas/exemples/invalides/`
  qui doivent échouer.

### 5. Point d'arrêt PA-3
Présenter les trois schémas et les exemples. Aucune implémentation avant validation.

## Critères de validation
- [ ] `scripts/valider-schemas.sh` : code 0 sur les valides, échec attendu sur chaque invalide.
- [ ] Aucun champ présent à la fois dans le XSD et dans un schéma JSON (CFG-1).
- [ ] Chaque champ cité ci-dessus est rattaché à son exigence dans un commentaire `$comment` ou
      `xs:annotation`.
- [ ] PA-3 tranché.

## Pièges connus
- JSON n'accepte pas de commentaires : la documentation passe par `description` et `$comment`.
- `string(JSON)` de CMake lit le JSON mais ne valide pas le schéma : la validation reste
  l'affaire de `lepton` et de l'éditeur.
- Ne pas introduire de champ « par prudence » : tout champ doit servir une exigence.

## À la fin de l'étape
`DEVENV-STATUS.md` : statut, versions des validateurs. Passation `handoff/env-3.md`.
