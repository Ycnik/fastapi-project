from dataclasses import dataclass
from soldat.entity import Soldat

@dataclass(eq=False, slots=True, kw_only=True)
class SoldatDTO:
    """Not implemented yet"""
    test: str = "testSoldat"
    version: int = 0

    def __init__(self, soldat: Soldat):
        """Not implemented yet"""
        self.test = soldat.nachname
        self.version = soldat.version