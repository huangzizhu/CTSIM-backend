from abc import ABC, abstractmethod
from typing import List
from pojo.CT import CT

class CTDaoInterface(ABC):
    def __init__(self,name: str):
        self.name = name

    def getAllCT(self) -> List[CT]:
        pass
