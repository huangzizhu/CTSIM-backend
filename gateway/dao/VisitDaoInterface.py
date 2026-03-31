from abc import ABC, abstractmethod
from typing import List


from pojo.Visit import VisitCreate, Visit, VisitUpdate


class VisitDaoInterface(ABC):
    def __init__(self,name: str):
        self.name = name

    @abstractmethod
    def addVisit(self, visit: VisitCreate) -> Visit:
        pass

    def getAllVisitsByPid(self, pid: int) -> List[Visit]:
        pass

    def getVisitByPid(self, pid: int) -> Visit | None:
        pass

    def updateVisit(self, visit: VisitUpdate) -> int:
        pass

    def deleteVisitByVisitId(self, visitId: int) -> int:
        pass