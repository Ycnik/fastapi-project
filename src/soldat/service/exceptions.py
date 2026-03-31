"""Exceptions in der Geschäftslogik."""

__all__ = [
    "NotFoundError",
]

class NotFoundError(Exception):
    """Exception, falls kein Soldat gefunden wurde."""

    def __init__(
        self,
        soldat_id: int | None = None,
    ) -> None:
        """Initialisierung von NotFoundError mit ID und Suchparameter.

        :param soldat_id: Soldat-ID, zu der nichts gefunden wurde
        """
        super().__init__("Not Found")
        self.soldat_id = soldat_id