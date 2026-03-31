"""Modul für persistente Patientendaten."""

from soldat.entity.ausrüstung import Ausrüstung
from soldat.entity.base import Base
from soldat.entity.geschlecht import Geschlecht
from soldat.entity.rang import Rang
from soldat.entity.schweregrad import Schweregrad
from soldat.entity.soldat import Soldat
from soldat.entity.verletzung import Verletzung
from soldat.entity.waffe import Waffe

# https://docs.python.org/3/tutorial/modules.html#importing-from-a-package
__all__ = [
    "Ausrüstung",
    "Base",
    "Geschlecht",
    "Rang",
    "Schweregrad",
    "Soldat",
    "Verletzung",
    "Waffe",
]
