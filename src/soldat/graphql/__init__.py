"""Modul für die GraphQL-Schnittstelle."""

from soldat.graphql.graphql_types import (
    AusruestungInput,
    CreatePayload,
    SoldatInput,
    Suchparameter,
    VerletzungInput,
)
from soldat.graphql.schema import Query, graphql_router

__all__ = [
    "AusruestungInput",
    "CreatePayload",
    "Query",
    "SoldatInput",
    "Suchparameter",
    "VerletzungInput",
    "graphql_router",
]
