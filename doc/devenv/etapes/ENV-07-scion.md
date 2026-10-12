# Étape ENV-7 — Évolutions génériques de scion

## Contexte
L'outil `lepton` délègue à scion toute opération sur la graine et le trunk (NF-2). L'audit
`env-2-scion.md` indique quelles opérations scion 0.5.0.1 ne couvre pas. Cette étape les ajoute à
scion, de façon générique, ou conclut qu'aucune évolution n'est nécessaire. Projet distinct :
`seed.scions`, hors de l'arbre Lepton.

## Prérequis
- ENV-2 terminée ; `env-2-scion.md` validé (PA-2).
- Clone `<SEED_SCIONS>` ; branche de travail créée depuis le tag `0.5.0.1`.

## Tâches

### 1. Point d'arrêt PA-8 — liste et version
Pour chaque manque relevé : commande proposée, comportement, code de retour, test. Numéro de
version cible <À CONFIRMER>. Si aucun manque : consigner « aucune évolution » et clore l'étape.

### 2. Implémentation
- Branche `devenv/env-7` dans `seed.scions`.
- Respecter la structure de la réécriture 0.5 : `pathlib`, `subprocess.run` avec liste
  d'arguments, codes de retour non nuls, aucun `shell=True`.
- Aucune chaîne propre à Lepton : `grep -ri lepton scion/` doit rester vide.
- Tests `pytest` pour chaque commande ajoutée.

### 3. Tag et installation
Après validation de l'utilisateur : tag de la nouvelle version, installation épinglée
(`pipx install "git+…@<version>"`), mise à jour de `DEVENV-STATUS.md` §Versions.

## Critères de validation
- [ ] PA-8 tranché.
- [ ] `pytest` vert ; `grep -ri lepton scion/` vide.
- [ ] Commandes 0.5.0.1 existantes inchangées (tests existants verts).
- [ ] Nouvelle version installée et relevée par `scion version`.

## Pièges connus
- `scion seed-update` / `graft-update` font un `git pull` : interdits sans accord (PA-P).
- Tag et push : soumis à accord (PA-P).

## À la fin de l'étape
`DEVENV-STATUS.md` : version de scion, statut. Passation `handoff/env-7.md`.
