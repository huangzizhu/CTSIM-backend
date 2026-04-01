from abc import ABC, abstractmethod
from typing import List
from pojo.CT import CT
from pojo.CTOrder import CTOrderCreate,CTOrderUpdate,CTOrder
class CTDaoInterface(ABC):
    def __init__(self,name: str):
        self.name = name

    def getAllCT(self) -> List[CT]:
        pass

    def addCTOrder(self, order: CTOrderCreate) -> CTOrder:
        pass

    def getAllCTOrdersByPID(self, pid: int) -> List[CTOrder]:
        pass

    def getNewestCTOrderByPID(self, pid: int) -> CTOrder | None:
        pass

    def getCTOrderByID(self, CtorId: int) -> CTOrder | None:
        pass

    def updateOrder(self, order: CTOrderUpdate) -> int:
        pass
