"""Enum für Geschlecht."""

from enum import StrEnum

import strawberry


# StrEnum ab Python 3.11 (2022), abgeleitet von str
# zusaetzlich als enum fuer das GraphQL-Schema
@strawberry.enum
class Titan(StrEnum):

    ANGRIFFS_TITAN = "ANGRIFFS-TITAN"

    KOLOSSALER_TITAN = "KOLOSSALER-TITAN"

    GEPANZERTER_TITAN = "GEPANZERTER-TITAN"

    WEIBLICHER_TITAN = "WEIBLICHER-TITAN"

    TIER_TITAN = "TIER-TITAN"

    KRIEGSHAMMER_TITAN = "KRIEGSHAMMER-TITAN"

    KIEFER_TITAN = "KIEFER-TITAN"

    KARRENTITAN = "KARREN-TITAN"

    URTITAN = "UR-TITAN"
  