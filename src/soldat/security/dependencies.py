"""Factory-Funktionen für Dependency Injection."""

from soldat.security.token_service import TokenService
from soldat.security.user_service import UserService

_token_service = TokenService()  # Singleton-Objekt


def get_token_service() -> TokenService:
    """Factory-Funktion für TokenService."""
    return _token_service


_user_service = UserService()  # Singleton-Objekt


def get_user_service() -> UserService:
    """Factory-Funktion für UserService."""
    return _user_service
