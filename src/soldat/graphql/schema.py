"""Schema für GraphQL durch Strawberry.

Alternative: https://github.com/graphql-python/graphene.
"""

from collections.abc import Sequence
from typing import Final

import strawberry
from fastapi import Request
from loguru import logger
from strawberry.fastapi import GraphQLRouter

from soldat.config.graphql import graphql_ide
from soldat.graphql.graphql_types import (
    Suchparameter,
)
from soldat.repository import Pageable, SoldatRepository
from soldat.service import (
    NotFoundError,
    SoldatDTO,
    SoldatService,
)

__all__ = ["graphql_router"]


# Strawberry ist eine "code-first library":
# - keine Schema-Datei in SDL (schema definition language) notwendig
# - das Schema wird aus Klassen generiert, die mit z.B. @type oder @input dekoriert sind

# type Patient {
#     nachname: String!
# }
# input Suchparameter {...}
# type Query {
#     patient(patient_id: ID!): Patient!
#     patienten(suchparameter: Suchparameter): list[Patient!]!
# }


_repo: Final = SoldatRepository()
_service: SoldatService = SoldatService(repo=_repo)
"""_user_service: UserService = UserService()
_token_service: Final = TokenService()"""


@strawberry.type  # vgl. @dataclass
class Query:
    """Queries, um Patientendaten zu lesen."""

    @strawberry.field
    def patient(self, soldat_id: strawberry.ID) -> SoldatDTO | None:
        """Daten zu einem Soldaten lesen.

        :param soldat_id: ID des gesuchten Soldaten
        :return: Gesuchter Soldat
        :rtype: Soldat
        :raises NotFoundError: Falls kein Soldat gefunden wurde, wird zu GraphQLError
        """
        logger.debug("soldat_id={}", soldat_id)

        """request: Final[Request] = info.context.get("request")
        user: Final = _token_service.get_user_from_request(request=request)
        if user is None:
            return None

        try:
            soldat_dto: Final = _service.find_by_id(
                soldat_id=int(soldat_id),
                user=user,
            )
        except NotFoundError:
            return None"""
        soldat_dto: Final = _service.find_by_id(
                soldat_id=int(soldat_id),
                user=None,  # ty:ignore[invalid-argument-type]
            )
        logger.debug("{}", soldat_dto)
        return soldat_dto

    @strawberry.field
    def patienten(
        self, suchparameter: Suchparameter
    ) -> Sequence[SoldatDTO]:
        """Patienten anhand von Suchparameter suchen.

        :param suchparameter: nachname, email usw.
        :return: Die gefundenen Patienten
        :rtype: list[Patient]
        :raises NotFoundError: Falls kein Patient gefunden wurde, wird zu GraphQLError
        """
        logger.debug("suchparameter={}", suchparameter)

        """request: Final[Request] = info.context["request"]
        user: Final = _token_service.get_user_from_request(request)
        if user is None or Role.ADMIN not in user.roles:
            return []"""

        # suchparameter: input type -> Dictionary
        # https://stackoverflow.com/questions/61517/python-dictionary-from-an-objects-fields
        suchparameter_dict: Final[dict[str, str]] = dict(vars(suchparameter))
        # nicht-gesetzte Suchparameter aus dem Dictionary entfernen
        # Dict Comprehension ab Python 2.7 (2001) https://peps.python.org/pep-0274
        suchparameter_filtered = {
            key: value
            for key, value in suchparameter_dict.items()
            # leerer String "" ist falsy
            if value is not None and value
        }
        logger.debug("suchparameter_filtered={}", suchparameter_filtered)

        pageable: Final = Pageable.create(size=str(0))
        try:
            patienten_dto: Final = _service.find(
                suchparameter=suchparameter_filtered, pageable=pageable
            )
        except NotFoundError:
            return []
        logger.debug("{}", patienten_dto)
        return patienten_dto.content


""" @strawberry.type
class Mutation:
    Mutations, um Patientendaten anzulegen, zu ändern oder zu löschen.

    @strawberry.mutation
    def create(self, patient_input: SoldatInput) -> CreatePayload:
        Einen neuen Patienten anlegen.

        :param patient_input: Daten des neuen Patienten
        :return: ID des neuen Patienten
        :rtype: CreatePayload
        :raises EmailExistsError: Falls die Emailadresse bereits existiert
        :raises UsernameExistsError: Falls der Benutzername bereits existiert

        logger.debug("patient_input={}", patient_input)

        patient_dict = patient_input.__dict__
        patient_dict["adresse"] = patient_input.adresse.__dict__
        # List Comprehension ab Python 2.0 (2000) https://peps.python.org/pep-0202
        patient_dict["rechnungen"] = [
            rechnung.__dict__ for rechnung in patient_input.rechnungen
        ]

        # Dictonary mit Pydantic validieren
        patient_model: Final = SoldatModel.model_validate(patient_dict)

        patient_dto: Final = _write_service.create(patient=patient_model.to_patient())
        payload: Final = CreatePayload(id=patient_dto.id)

        logger.debug("{}", payload)
        return payload

    # Mutation, weil evtl. der Login-Zeitpunkt gespeichert wird
    @strawberry.mutation
    def login(self, username: str, password: str) -> LoginResult:
        Einen Token zu Benutzername und Passwort ermitteln.

        :param username: Benutzername
        :param password: Passwort
        :rtype: LoginResult

        logger.debug("username={}, password={}", username, password)
        token_mapping = _token_service.token(username=username, password=password)

        token = token_mapping["access_token"]
        user = _token_service.get_user_from_token(token)
        # List Comprehension ab Python 2.0 (2000) https://peps.python.org/pep-0202
        roles: Final = [role.value for role in user.roles]
        return LoginResult(token=token, expiresIn="1d", roles=roles) """

schema: Final = strawberry.Schema(query=Query, mutation=None)  # Mutation=Mutation)

Context = dict[str, Request]


# Dependency Injection: Request von FastAPI weiterreichen an den Kontext von Strawberry
def get_context(request: Request) -> Context:
    return {"request": request}


# https://strawberry.rocks/docs/integrations/fastapi
graphql_router: Final = GraphQLRouter[Context](
    schema, context_getter=get_context, graphql_ide=graphql_ide
)
