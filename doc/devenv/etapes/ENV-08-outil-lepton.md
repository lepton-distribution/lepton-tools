# Étape ENV-8 — Outil `lepton`

## Contexte
`lepton` est l'outil en ligne de commande, en Python, client de scion, qui porte toute la logique
propre à Lepton (NF-1, NF-2) : graine, greffons, fichiers, vérification. VSCodium et la future
extension ne font que l'appeler. Projet nouveau : archétype création, jalons à critère de sortie.

## Prérequis
- ENV-5 terminée (construction par manifestes) ; ENV-7 terminée (version de scion fixée).
- Schémas d'ENV-3. Branche `devenv/env-8` dans `lepton-tools`.

## Tâches

### 1. Point d'arrêt PA-9 — interface
Proposer l'interface complète avant d'écrire du code : commandes, options, sorties, codes de
retour. Base minimale issue de la spécification :

| Commande | Exigences |
| --- | --- |
| `lepton seed new` | GRA-1, GRA-2 |
| `lepton seed add / remove / replace` | GRA-3, GRA-4 |
| `lepton seed status` | GRA-6 |
| `lepton seed lock` | GRA-5 (P2) |
| `lepton scion new --type bsp\|application\|bibliotheque` | GRF-1 |
| `lepton scion remove` | GRF-4 |
| `lepton file add / remove / mv`, `lepton dir add / remove` | FIC-1, FIC-2, FIC-3, FIC-6 |
| `lepton graft` | regreffe + reconfiguration |
| `lepton check` | CFG-5 (P2), GRF-5 (P2), validation des manifestes |
| `lepton --version` | INS-6 |

Le nom de la sous-commande « greffon » (`scion`, `graft`, `greffon`) est à trancher en PA-9.

### 2. Jalons
Chaque jalon se termine par des tests verts et un commit.
1. Squelette : paquet `lepton/`, `pyproject.toml`, point d'entrée, `--version`, validation des
   manifestes par JSON Schema.
2. Modèles : `templates/` (graine, BSP, application, bibliothèque) conformes aux schémas.
3. Graine : `seed new`, `seed status`, `seed add/remove/replace` par appel de scion.
4. Greffons : `scion new`, `scion remove`.
5. Fichiers : `file`/`dir` — création toujours dans le clone propriétaire, puis regreffe ;
   refus explicite d'un chemin du trunk sans greffon propriétaire.
6. `check` et `seed lock` (P2).

### 3. Tests
`pytest` sur des rootstocks temporaires construits à partir de dépôts git locaux de test (pas de
réseau, NF-8). Un test par exigence citée.

## Critères de validation
- [ ] PA-9 tranché.
- [ ] `pytest` vert ; un test identifié par exigence P1 citée.
- [ ] Bout en bout scripté : `seed new` (noyau + BSP QEMU) → `cmake` → test de fumée QEMU.
- [ ] Après chaque commande : aucun fichier régulier dans le trunk.
- [ ] `lepton` installable par `pipx install <LEPTON_TOOLS>`.

## Pièges connus
- Ne jamais écrire dans le trunk, même temporairement : toute écriture vise un clone.
- Appeler scion par `subprocess.run` avec liste d'arguments, vérifier le code de retour ; ne pas
  importer ses modules internes (couplage de versions).
- Ne pas reproduire dans `lepton` une opération que scion couvre déjà.

## À la fin de l'étape
`DEVENV-STATUS.md` : version de `lepton`, jalons atteints. Passation `handoff/env-8.md`.
