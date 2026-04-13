"""Exceptions in der Geschäftslogik."""

from collections.abc import Mapping

__all__ = [
    "NotFoundError",
    "SeriennummerExistsError",
    "VersionOutdatedError",
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


class LoginError(Exception):
    """Exception, falls Benutzername oder Passwort fehlerhaft ist."""

    def __init__(
        self,
        username: str | None = None,
    ) -> None:
        """Initialisierung von LoginError mit fehlerhaftem Benutzername oder Passwort.

        :param username: Benutzername
        """
        super().__init__(f"Fehlerhafte Benutzerdaten fuer {username}")
        self.username = username


class AuthorizationError(Exception):
    """Exception, falls der "Authorization"-String fehlt oder fehlerhaft ist."""


class SeriennummerExistsError(Exception):
    """Exception, falls die Seriennummer bereits existiert."""

    def __init__(self, seriennummer: str) -> None:
        """Initialisierung mit einer bereits vergebenen Seriennummer."""
        super().__init__(f"Seriennummer existiert bereits: {seriennummer}")
        self.seriennummer = seriennummer
