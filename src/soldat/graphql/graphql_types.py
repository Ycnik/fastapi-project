"""Schema für GraphQL."""

from datetime import date

import strawberry

from soldat.entity import Geschlecht, Rang, Schweregrad, Waffe

__all__ = [
    "AusruestungInput",
    "CreatePayload",
    "SoldatInput",
    "Suchparameter",
    "VerletzungInput",
]

# SDL (schema definition language):
# type Soldat {
#     nachname: String!
# }
# type Query {
#     soldat(soldat_id: ID!): Soldat!
#     soldaten(input: Suchparameter): [Soldat!]
# }
# type Mutation {
#     create(soldat_input: SoldatInput!): CreatePayload!
# }


@strawberry.input
class Suchparameter:
    """Suchparameter für die Suche nach Soldaten."""

    nachname: str | None = None
    """Nachname als Suchkriterium."""


@strawberry.input
class AusruestungInput:
    """Ausruestung eines neuen Soldaten."""

    seriennummer: str
    """Seriennummer einer neuen Ausruestung."""

    waffe: Waffe
    """Waffe eines neuen Soldaten."""


@strawberry.input
class VerletzungInput:
    """Verletzung eines neuen Soldaten."""

    verletzungsbezeichnung: str
    """Verletzungsbezeichnung."""

    schweregrad: Schweregrad
    """Schweregrad der Verletzung."""

    behandelt: bool
    """Angabe, ob die Verletzung behandelt wurde."""

    verletzungsdatum: date


@strawberry.input
class SoldatInput:
    """Daten für einen neuen Soldaten."""

    vorname: str
    """Der Vorname."""

    nachname: str
    """Der Nachname"""

    rang: Rang
    """Angabe, des Ranges eines Soldaten"""

    geburtsdatum: date
    """Das Geburtsdatum."""

    geschlecht: Geschlecht
    """Das  Geschlecht."""

    username: str
    """Der Benutzername für Login."""

    ausruestung: AusruestungInput
    """Die Ausrüstung eines neuen Soldaten."""

    verletzungen: list[VerletzungInput]
    """Die Verletzungen eines neuen Soldaten."""


@strawberry.type
class CreatePayload:
    """Resultat-Typ, wenn ein neuer Soldat angelegt wurde."""

    id: int
    """ID des neu angelegten Soldaten"""


@strawberry.type
class LoginResult:
    """Resultat-Typ, wenn ein Login erfolgreich war."""

    token: str
    """Token des eingeloggten Users."""
    expiresIn: str  # noqa: N815  # NOSONAR
    """Gültigkeitsdauer des Tokens."""
    roles: list[str]
    """Rollen des eingeloggten Users."""
