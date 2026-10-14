"""Erreurs de lepton et codes de retour (rapports/env-8-interface.md §2)."""

EXIT_OK = 0
EXIT_USER = 1       # utilisation, refus, manifeste invalide, anomalie trouvée
EXIT_TOOL = 2       # échec ou absence d'un outil appelé (scion, git, cmake, xmllint)
EXIT_INTERRUPT = 130


class LeptonError(Exception):
    """Erreur signalée à l'utilisateur : constat, action corrective, code de retour (NF-6)."""

    def __init__(self, message: str, action: str | None = None, code: int = EXIT_USER):
        super().__init__(message)
        self.message = message
        self.action = action
        self.code = code
