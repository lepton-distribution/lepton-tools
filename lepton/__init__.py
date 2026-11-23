"""Outil lepton : environnement de développement Lepton, client de scion (ENV-8)."""

__version__ = "0.1.0"

# Version minimale de scion (ENV-7 : seed-scion-add/remove, graft --scion, graft-remove ;
# ENV-15 : fichiers ignorés par git non greffés, fichiers tolérés du trunk ;
# ENV-29 : clones à leur version déclarée, trunk rétabli si la regreffe échoue ;
# ENV-41 : projection d'un dépôt tiers (0.6.0.0) portée par un greffon, miroirs (0.6.1.0), PA-69 ;
# ENV-44 : graft --scion <porteur> regreffe ses clés projetées (0.6.2.0, P-G6, PA-75) ;
# ENV-52 : extraction partielle des clones projetés (0.6.3.0, P-V7), sans effet sur lepton : minimum
# inchangé (PA-91) ;
# ENV-56 : un clonage en échec ne laisse aucun répertoire (0.6.3.1, D14), sans effet sur lepton :
# minimum inchangé (PA-99) ;
# ENV-60 : un clone est fait à sa version déclarée ou pas du tout (0.6.3.2, D18), sans effet sur
# lepton : minimum inchangé (PA-107) ;
# ENV-65 : clone existant repris seulement à sa version, première ligne de git dans les messages
# (0.6.3.3, D25, D22), sans effet sur lepton : minimum inchangé (PA-117) ;
# ENV-70 : graine clonée contrôlée par seed-update et graft-update, cause de l'échec de git après
# un avertissement (0.6.3.4, D33, D35), sans effet sur lepton : minimum inchangé (PA-127)
SCION_MIN_VERSION = (0, 6, 2, 0)
