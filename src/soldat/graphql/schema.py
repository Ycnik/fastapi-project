"""Schema für GraphQL durch Strawberry.

Alternative: https://github.com/graphql-python/graphene.
"""

from collections.abc import Sequence
from typing import Final

import strawberry
from fastapi import Request
from loguru import logger
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info

from soldat.config.graphql import graphql_ide
from soldat.graphql.graphql_types import (
    CreatePayload,
    LoginResult,
    SoldatInput,
    Suchparameter,
)
from soldat.repository import Pageable, SoldatRepository
from soldat.router.soldat_model import SoldatModel
from soldat.security import Role, TokenService, UserService
from soldat.service import (
    NotFoundError,
    SoldatDTO,
    SoldatService,
    SoldatWriteService,
)

__all__ = ["graphql_router"]


# Strawberry ist eine "code-first library":
# - keine Schema-Datei in SDL (schema definition language) notwendig
# - das Schema wird aus Klassen generiert, die mit z.B. @type oder @input dekoriert sind

# type Soldat {
#     nachname: String!
# }
# input Suchparameter {...}
# type Query {
#     Soldat(Soldat_id: ID!): Soldat!
#     Soldaten(suchparameter: Suchparameter): list[Soldat!]!
# }


_repo: Final = SoldatRepository()
_service: SoldatService = SoldatService(repo=_repo)
_user_service: UserService = UserService()
_write_service: SoldatWriteService = SoldatWriteService(
    repo=_repo
)
_token_service: Final = TokenService()


@strawberry.type  # vgl. @dataclass
class Query:
    """Queries, um Soldatendaten zu lesen."""

    @strawberry.field
    def soldat(self, soldat_id: strawberry.ID, info: Info) -> SoldatDTO | None:
        """Daten zu einem Soldaten lesen.

        :param soldat_id: ID des gesuchten Soldaten
        :return: Gesuchter Soldat
        :rtype: Soldat
        :raises NotFoundError: Falls kein Soldat gefunden wurde, wird zu GraphQLError
        """
        logger.debug("soldat_id={}", soldat_id)

        request: Final[Request] = info.context.get("request")
        user: Final = _token_service.get_user_from_request(request=request)
        if user is None:
            return None

        try:
            soldat_dto: Final = _service.find_by_id(
                soldat_id=int(soldat_id),
                user=user
            )
        except NotFoundError:
            return None
        logger.debug("{}", soldat_dto)
        return soldat_dto

    @strawberry.field
    def soldaten(
        self, suchparameter: Suchparameter, info: Info
    ) -> Sequence[SoldatDTO]:
        """Soldaten anhand von Suchparameter suchen.

        :param suchparameter: nachname, email usw.
        :return: Die gefundenen Soldaten
        :rtype: list[Soldat]
        :raises NotFoundError: Falls kein Soldat gefunden wurde, wird zu GraphQLError
        """
        logger.debug("suchparameter={}", suchparameter)

        request: Final[Request] = info.context["request"]
        user: Final = _token_service.get_user_from_request(request)
        if user is None or Role.ADMIN not in user.roles:
            return []

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
            soldaten_dto: Final = _service.find(
                suchparameter=suchparameter_filtered, pageable=pageable
            )
        except NotFoundError:
            return []
        logger.debug("{}", soldaten_dto)
        return soldaten_dto.content


@strawberry.type
class Mutation:
    """Mutations, um Soldatendaten anzulegen, zu ändern oder zu löschen."""

    @strawberry.mutation
    def create(self, soldat_input: SoldatInput) -> CreatePayload:
        """Einen neuen Soldaten anlegen.

        :param soldat_input: Daten des neuen Soldaten
        :return: ID des neuen Soldaten
        :rtype: CreatePayload
        :raises UsernameExistsError: Falls der Benutzername bereits existiert
        """
        logger.debug("soldat_input={}", soldat_input)

        soldat_dict = soldat_input.__dict__
        soldat_dict["ausruestung"] = soldat_input.ausruestung.__dict__
        # List Comprehension ab Python 2.0 (2000) https://peps.python.org/pep-0202
        soldat_dict["verletzungen"] = [
            verletzung.__dict__ for verletzung in soldat_input.verletzungen
        ]

        # Dictonary mit Pydantic validieren
        soldat_model: Final = SoldatModel.model_validate(soldat_dict)

        soldat_dto: Final = _write_service.create(soldat=soldat_model.to_soldat())
        payload: Final = CreatePayload(id=soldat_dto.id)  # pyright: ignore[reportArgumentType ]

        logger.debug("{}", payload)
        return payload

    # Mutation, weil evtl. der Login-Zeitpunkt gespeichert wird
    @strawberry.mutation
    def login(self, username: str, password: str) -> LoginResult:
        """Einen Token zu Benutzername und Passwort ermitteln.

        :param username: Benutzername
        :param password: Passwort
        :Returntype: LoginResult
        """
        logger.debug("username={}, password={}", username, password)
        token_mapping = _token_service.token(username=username, password=password)

        token = token_mapping["access_token"]
        user = _token_service.get_user_from_token(token)
        # List Comprehension ab Python 2.0 (2000) https://peps.python.org/pep-0202
        roles: Final = [role.value for role in user.roles]
        return LoginResult(token=token, expiresIn="1d", roles=roles)


schema: Final = strawberry.Schema(query=Query, mutation=Mutation)


Context = dict[str, Request]


# Dependency Injection: Request von FastAPI weiterreichen an den Kontext von Strawberry
def get_context(request: Request) -> Context:
    return {"request": request}


# https://strawberry.rocks/docs/integrations/fastapi
graphql_router: Final = GraphQLRouter[Context](
    schema, context_getter=get_context, graphql_ide=graphql_ide
)
