from abc import ABC, abstractmethod
from typing import List

from pojo.Log import Log
class LogDaoInterface(ABC):
    def __init__(self,name: str):
        self.name = name

    def insertLog(self, log: Log):
        pass

    def getAllLogs(self) -> List[Log]:
        pass