"""Outil lepton : environnement de développement Lepton, client de scion (ENV-8)."""

__version__ = "0.1.0"

# Version minimale de scion (ENV-7 : seed-scion-add/remove, graft --scion, graft-remove ;
# ENV-15 : fichiers ignorés par git non greffés, fichiers tolérés du trunk ;
# ENV-29 : clones à leur version déclarée, trunk rétabli si la regreffe échoue ;
# ENV-41 : projection d'un dépôt tiers (0.6.0.0) portée par un greffon, miroirs (0.6.1.0), PA-69)
SCION_MIN_VERSION = (0, 6, 1, 0)
