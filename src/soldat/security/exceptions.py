"""Exceptions beim Zugriffsschutz."""


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
