"""Exceptions in der Geschäftslogik."""

from collections.abc import Mapping

__all__ = [
    "NotFoundError",
]


class NotFoundError(Exception):
    """Exception, falls kein Soldat gefunden wurde."""

    def __init__(
        self,
        soldat_id: int | None = None,
        suchparameter: Mapping[str, str] | None = None,
    ) -> None:
        """Initialisierung von NotFoundError mit ID und Suchparameter.

        :param soldat_id: Soldat-ID, zu der nichts gefunden wurde
        :param suchparameter: Suchparameter, zu denen nichts gefunden wurde
        """
        super().__init__("Not Found")
        self.soldat_id = soldat_id
        self.suchparameter = suchparameter


class ForbiddenError(Exception):
    """Exception, falls es der Zugriff nicht erlaubt ist."""

    class VersionOutdatedError(Exception):
        """Exception, falls die Versionsnummer beim Aktualisieren veraltet ist."""

    def __init__(self, version: int) -> None:
        """Initialisierung von VersionOutdatedError mit veralteter Versionsnummer.

        :param version: Veraltete Versionsnummer
        """
        super().__init__(f"Veraltete Version: {version}")
        self.version = version
